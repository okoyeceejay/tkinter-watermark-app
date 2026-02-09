# from tkinter import *
# from tkinter import ttk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from watermark_engine import WatermarkEngine
from PIL import ImageTk


class WatermarkItApp(tk.Tk):
    def __init__(self):
        super().__init__()

        #Window Configuration
        self.title("Watermark It!")
        self.geometry("600x550")
        self.engine = None          # WatermarkEngine instance
        self.original_image = None # PIL Image
        self.result_image = None   # Watermarked PIL Image
        self.preview_photo = None  # ImageTk.PhotoImage (must be stored!)

        
        self.watermark_text = tk.StringVar()
        
        #Initialize variables
        self.spin_val = tk.IntVar(value=10)
        
         # Variable to store the path string
        self.selected_path = tk.StringVar(value="No file selected")
        
        #Initialize UI Components
        self._setup_widgets()
        

    def _setup_widgets(self):
        # Configure grid weights for responsive layout
        for i in range(14):
            self.grid_rowconfigure(i, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # Browse button
        self.browse_btn = tk.Button(
            self, 
            text="Browse Image", 
            command=self.open_file_selector,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white"
        )
        self.browse_btn.grid(row=0, column=0, pady=7, sticky="ew", padx=20)
        
        # Path label
        self.path_label = tk.Label(
            self, 
            textvariable=self.selected_path, 
            wraplength=400, 
            fg="blue",
            font=("Arial", 10)
        )
        self.path_label.grid(row=1, column=0, pady=7, sticky="ew", padx=20)

        # Watermark text label
        self.text_label = tk.Label(self, text="Watermark Text", font=("Arial", 12, "bold"))
        self.text_label.grid(row=2, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # Watermark text entry
        self.text_entry = tk.Entry(self, textvariable=self.watermark_text, font=("Arial", 12))
        self.text_entry.grid(row=3, column=0, pady=5, sticky="ew", padx=20)
        
        # Position label
        self.position_label = tk.Label(self, text="Watermark Position", font=("Arial", 12, "bold"))
        self.position_label.grid(row=4, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # Dropdown
        self.positions_options = ["top-left", "top-right", "top-center", "center", "bottom-left", "bottom-right", "bottom-center"]
        self.dropdown = ttk.Combobox(self, values=self.positions_options, state="readonly", font=("Arial", 11))
        self.dropdown.set("Select Position")
        self.dropdown.grid(row=5, column=0, pady=5, sticky="ew", padx=20)

        # Padding label
        self.padding_label = tk.Label(self, text="Padding", font=("Arial", 12, "bold"))
        self.padding_label.grid(row=6, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # Padding slider
        self.slider_padding = tk.Scale(self, from_=0, to=50, orient="horizontal", font=("Arial", 10))
        self.slider_padding.set(10)
        self.slider_padding.grid(row=7, column=0, pady=5, sticky="ew", padx=20)

        # Font size label
        self.font_label = tk.Label(self, text="Font Size", font=("Arial", 12, "bold"))
        self.font_label.grid(row=8, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # Font size spinbox
        self.font_size_spin = tk.Spinbox(
            self, 
            from_=8, 
            to=100, 
            increment=5,
            textvariable=self.spin_val, 
            command=self.update_label,
            font=("Arial", 11)
        )
        self.font_size_spin.grid(row=9, column=0, pady=5, sticky="ew", padx=20)
        
        # Current size display
        self.display = tk.Label(self, text="Current: 10", font=("Arial", 10), fg="gray")
        self.display.grid(row=10, column=0, pady=5, sticky="w", padx=20)
        
        # Opacity label
        self.opacity_label = tk.Label(self, text="Opacity", font=("Arial", 12, "bold"))
        self.opacity_label.grid(row=11, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # Opacity slider
        self.slider_opacity = tk.Scale(self, from_=0, to=255, orient="horizontal", font=("Arial", 10))
        self.slider_opacity.set(128)
        self.slider_opacity.grid(row=12, column=0, pady=5, sticky="ew", padx=20)

        # Submit button
        self.submit_btn = tk.Button(self, text="Apply Watermark", command=self.handle_submit, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.submit_btn.grid(row=13, column=0, pady=5, sticky="ew", padx=20)
        
        # status label (for image preview)
        self.status = tk.Label(self, text="", font=("Arial", 10))
        self.status.grid(row=14, column=0, pady=5, sticky="ew", padx=20)
    
    def open_file_selector(self):
        """Method to handle file dialog logic"""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]

        # Call the dialog
        # 'self' is passed as the parent so the dialog centers on this window
        path = filedialog.askopenfilename(
            parent=self,
            title="Choose an image",
            filetypes=file_types
        )

        # Check if the user actually picked a file (didn't click cancel)
        if path:
            self.selected_path.set(path)
            print(f"File saved to variable: {path}")
            self.engine = WatermarkEngine(path)
            self.status.config(text="Image loaded ✔", fg="green")

    def update_label(self):
        """Update the display label with current spinbox value"""
        self.display.config(text=f"Current: {self.spin_val.get()}")

    def handle_submit(self):
        """Logic for the button click"""
        if not self.engine:
            return

        text = self.watermark_text.get()
        position = self.dropdown.get()
        padding = self.slider_padding.get()
        font_size = self.spin_val.get()
        opacity = self.slider_opacity.get()

        self.result_image = self.engine.add_watermark(
            text=text,
            position=position,
            font_size=font_size,
            padding=padding,
            opacity=opacity
        )

        self.show_preview(self.result_image)
    
    def show_preview(self, image):
        image.thumbnail((400, 400))
        self.preview_photo = ImageTk.PhotoImage(image)
        self.status.config(image=self.preview_photo)


if __name__ == "__main__":
    app = WatermarkItApp()
    app.mainloop()





