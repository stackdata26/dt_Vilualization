

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.current_image = None
        self.brightness_value = tk.DoubleVar(value=1.0)
        self.contrast_value = tk.DoubleVar(value=1.0)
        self.sharpness_value = tk.DoubleVar(value=1.0)
        
        # Create GUI
        self.create_gui()
        
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Load button
        ttk.Button(button_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5)
        
        # Save button
        ttk.Button(button_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=5)
        
        # Reset button
        ttk.Button(button_frame, text="Reset", command=self.reset_image).grid(row=0, column=2, padx=5)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Image Controls", padding="5")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Brightness control
        ttk.Label(control_frame, text="Brightness:").grid(row=0, column=0, sticky=tk.W)
        brightness_scale = ttk.Scale(control_frame, from_=0.0, to=2.0, variable=self.brightness_value,
                                   orient=tk.HORIZONTAL, command=self.update_image)
        brightness_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Contrast control
        ttk.Label(control_frame, text="Contrast:").grid(row=1, column=0, sticky=tk.W)
        contrast_scale = ttk.Scale(control_frame, from_=0.0, to=2.0, variable=self.contrast_value,
                                 orient=tk.HORIZONTAL, command=self.update_image)
        contrast_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Sharpness control
        ttk.Label(control_frame, text="Sharpness:").grid(row=2, column=0, sticky=tk.W)
        sharpness_scale = ttk.Scale(control_frame, from_=0.0, to=2.0, variable=self.sharpness_value,
                                  orient=tk.HORIZONTAL, command=self.update_image)
        sharpness_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Filter buttons
        filter_frame = ttk.LabelFrame(main_frame, text="Filters", padding="5")
        filter_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Button(filter_frame, text="Blur", command=lambda: self.apply_filter("blur")).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(filter_frame, text="Emboss", command=lambda: self.apply_filter("emboss")).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(filter_frame, text="Contour", command=lambda: self.apply_filter("contour")).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(filter_frame, text="Edge Enhance", command=lambda: self.apply_filter("edge_enhance")).grid(row=0, column=3, padx=5, pady=2)
        
        # Image display
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=3, column=0, pady=5)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.processed_image = self.original_image.copy()
            self.display_image()
            
    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"),
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")])
            if file_path:
                self.processed_image.save(file_path)
                
    def reset_image(self):
        if self.original_image:
            self.brightness_value.set(1.0)
            self.contrast_value.set(1.0)
            self.sharpness_value.set(1.0)
            self.processed_image = self.original_image.copy()
            self.display_image()
            
    def update_image(self, event=None):
        if self.original_image:
            # Apply adjustments
            self.processed_image = self.original_image.copy()
            
            # Brightness
            enhancer = ImageEnhance.Brightness(self.processed_image)
            self.processed_image = enhancer.enhance(self.brightness_value.get())
            
            # Contrast
            enhancer = ImageEnhance.Contrast(self.processed_image)
            self.processed_image = enhancer.enhance(self.contrast_value.get())
            
            # Sharpness
            enhancer = ImageEnhance.Sharpness(self.processed_image)
            self.processed_image = enhancer.enhance(self.sharpness_value.get())
            
            self.display_image()
            
    def apply_filter(self, filter_name):
        if self.processed_image:
            if filter_name == "blur":
                self.processed_image = self.processed_image.filter(ImageFilter.BLUR)
            elif filter_name == "emboss":
                self.processed_image = self.processed_image.filter(ImageFilter.EMBOSS)
            elif filter_name == "contour":
                self.processed_image = self.processed_image.filter(ImageFilter.CONTOUR)
            elif filter_name == "edge_enhance":
                self.processed_image = self.processed_image.filter(ImageFilter.EDGE_ENHANCE)
            
            self.display_image()
            
    def display_image(self):
        # Resize image to fit display (max size 800x600)
        display_size = (800, 600)
        self.processed_image.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.current_image = ImageTk.PhotoImage(self.processed_image)
        self.image_label.configure(image=self.current_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
