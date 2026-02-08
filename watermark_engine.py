from PIL import Image, ImageTk, ImageDraw, ImageFont
class WatermarkEngine:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img_copy = self.load_image(image_path)
        self.watermark_position = {
            "top-left": ("left", "top"),
            "top-center": ("center", "top"),
            "top-right": ("right", "top"),
            "center": ("center", "center"),
            "bottom-left": ("left", "bottom"),
            "bottom-center": ("center", "bottom"),
            "bottom-right": ("right", "bottom"),
        }
        

    def load_image(self, image_path):
        img  = Image.open(f"{image_path}")
        img_copy = img.copy()
        img_copy = img_copy.convert("RGBA")
        return img_copy
        
    
    def find_font(self, font_size):
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        return font
    
    def add_watermark(self, text, position="center", font_size=36, padding=10,  opacity=128):
        if font_size is None:
            font_size = int(self.img_copy.width * 0.05)
        font = self.find_font(font_size)
        overlay = Image.new('RGBA', self.img_copy.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        user_position = position.lower()
        t_position = self.watermark_position.get(user_position, (self.img_copy.width / 2, self.img_copy.height / 2))
        
        # Adjust position based on alignment
        x = t_position[0]
        y = t_position[1]
        
        if "left" in user_position:
            x = padding
        elif "right" in user_position:
            x = self.img_copy.width - text_width - padding
        else:  # center
            x = (self.img_copy.width - text_width) / 2
        if "top" in user_position:
            y = padding
        elif "bottom" in user_position:
            y = self.img_copy.height - text_height - padding
        else:  # center
            y = (self.img_copy.height - text_height) / 2
        
        
        # Constrain to bounds
        x = max(0, min(x, self.img_copy.width - text_width))
        y = max(0, min(y, self.img_copy.height - text_height))
                 
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
        watermarked_image = Image.alpha_composite(self.img_copy.convert("RGBA"), overlay)
        return watermarked_image
    