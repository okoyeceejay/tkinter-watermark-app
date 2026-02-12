import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk
from watermark_engine import WatermarkEngine
import os


class WatermarkItApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Watermark It!")
        self.geometry("600x800")

        # App state
        self.engine = None
        self.result_image = None
        self.preview_photo = None

        # Variables
        self.selected_path = tk.StringVar(value="No file selected")
        self.watermark_text = tk.StringVar()
        self.font_size = tk.IntVar(value=20)

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self._build_file_section()
        self._build_controls()
        self._build_preview()

    def _build_file_section(self):
        tk.Button(
            self, text="Browse Image",
            command=self.open_file_selector,
            bg="#4CAF50", fg="white"
        ).grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        tk.Label(
            self, textvariable=self.selected_path,
            fg="blue", wraplength=500
        ).grid(row=1, column=0, padx=20)

    def _build_controls(self):
        frame = tk.Frame(self)
        frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Watermark Text").grid(sticky="w")
        self.text_entry = tk.Entry(frame, textvariable=self.watermark_text)
        self.text_entry.grid(sticky="ew")
        self.text_entry.bind("<KeyRelease>", self.update_preview)

        

        tk.Label(frame, text="Position").grid(sticky="w", pady=(10, 0))
        self.position = ttk.Combobox(
            frame,
            values=[
                "top-left", "top-center", "top-right",
                "center",
                "bottom-left", "bottom-center", "bottom-right"
            ],
            state="readonly"
        )
        self.position.bind("<<ComboboxSelected>>", self.update_preview)
        self.position.set("center")
        self.position.grid(sticky="ew")

        tk.Label(frame, text="Padding").grid(sticky="w", pady=(10, 0))
        self.slider_padding = tk.Scale(
            frame,
            from_=0,
            to=50,
            orient="horizontal",
            command=self.update_preview
        )

        self.slider_padding.set(10)
        self.slider_padding.grid(sticky="ew")

        tk.Label(frame, text="Font Size").grid(sticky="w", pady=(10, 0))
        self.font_size_spin = tk.Spinbox(
            frame, from_=8, to=100,
            textvariable=self.font_size,
            command=self.update_preview)
        self.font_size_spin.grid(sticky="ew")
        self.font_size_spin.bind("<KeyRelease>", self.update_preview)



        tk.Label(frame, text="Opacity").grid(sticky="w", pady=(10, 0))
        self.opacity = tk.Scale(frame, from_=0, to=255, orient="horizontal", command=self.update_preview)
        self.opacity.set(128)
        self.opacity.grid(sticky="ew")

        tk.Button(
            frame, text="Apply Watermark",
            command=self.apply_watermark,
            bg="#2196F3", fg="white"
        ).grid(pady=15, sticky="ew")

        self.status = tk.Label(frame, fg="red")
        self.status.grid()
        
        tk.Button(
        frame,
        text="Save Watermarked Image",
        command=self.save_image,
        bg="#673AB7",
        fg="white" ).grid(pady=5, sticky="ew")

    def _build_preview(self):
        self.preview_label = tk.Label(self)
        self.preview_label.grid(row=3, column=0, pady=15)
        
    def update_preview(self, *_):
        if not self.engine:
            return

        text = self.watermark_text.get()
        if not text:
            return  # Don't preview empty watermark

        position = self.position.get()
        padding = self.slider_padding.get()
        font_size = self.font_size.get()
        opacity = self.opacity.get()


        self.result_image = self.engine.add_watermark(
            text=text,
            position=position,
            font_size=font_size,
            padding=padding,
            opacity=opacity
        )

        self.show_preview(self.result_image)


    def open_file_selector(self):
        ALLOWED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")

        paths = filedialog.askopenfilenames(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )

        if not paths:
            return

        # VALIDATION
        for path in paths:
            if not path.lower().endswith(ALLOWED_EXTENSIONS):
                messagebox.showerror(
                    "Invalid file",
                    f"Unsupported file format:\n{os.path.basename(path)}\n\n"
                    f"Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
                )
                return  

        # If we reach here → all files are valid
        self.selected_paths = list(paths)
        self.engines = [WatermarkEngine(p) for p in self.selected_paths]

        self.selected_path.set(f"{len(paths)} images selected")
        self.status.config(text="Images loaded ✔", fg="green")


    def apply_watermark(self):
        if not self.engines:
            messagebox.showerror("Error", "No images loaded")
            return

        self.result_images = []

        for engine in self.engines:
            img = engine.add_watermark(
                text=self.watermark_text.get(),
                position=self.position.get(),
                font_size=self.font_size.get(),
                padding=self.slider_padding.get(),
                opacity=self.opacity.get()
            )
            self.result_images.append(img)

        # Show preview of first image
        self.show_preview(self.result_images[0])


    def save_image(self):
        if not self.result_images:
            messagebox.showerror("Error", "No watermarked images to save")
            return

        output_dir = os.path.join(os.getcwd(), "watermarked_images")
        os.makedirs(output_dir, exist_ok=True)

        for img, path in zip(self.result_images, self.selected_paths):
            base = os.path.basename(path)
            name, _ = os.path.splitext(base)
            output_path = os.path.join(output_dir, f"{name}_watermarked.png")
            img.save(output_path, format="PNG")

        messagebox.showinfo(
            "Saved",
            f"{len(self.result_images)} images saved successfully!"
        )



    def show_preview(self, image):
        preview = image.copy()
        preview.thumbnail((450, 450))
        self.preview_photo = ImageTk.PhotoImage(preview)
        self.preview_label.config(image=self.preview_photo)


if __name__ == "__main__":
    WatermarkItApp().mainloop()
