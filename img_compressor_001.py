import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor")

        # Variables
        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.target_size_mb = tk.DoubleVar()
        self.target_size_mb.set(1.0)  # Default target size is 1.0 MB

        # GUI components
        self.create_widgets()

    def create_widgets(self):
        # Input folder selection
        tk.Label(self.root, text="Select Input Folder:").pack()
        tk.Button(self.root, text="Browse", command=self.browse_input_folder).pack()
        tk.Entry(self.root, textvariable=self.input_folder_path, state="readonly").pack()

        # Output folder selection
        tk.Label(self.root, text="Select Output Folder:").pack()
        tk.Button(self.root, text="Browse", command=self.browse_output_folder).pack()
        tk.Entry(self.root, textvariable=self.output_folder_path, state="readonly").pack()

        # Target size input
        tk.Label(self.root, text="Target Size (MB):").pack()
        tk.Entry(self.root, textvariable=self.target_size_mb).pack()

        # Compress button
        tk.Button(self.root, text="Compress Images", command=self.compress_images).pack()

    def browse_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_folder_path.set(folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_path.set(folder_path)

    def compress_images(self):
        input_folder = self.input_folder_path.get()
        output_folder = self.output_folder_path.get()
        target_size_mb = self.target_size_mb.get()

        # Check if output folder exists, create it if not
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                with Image.open(input_path) as img:
                    quality = 85
                    max_iterations = 10  # Prevent infinite loop
                    for _ in range(max_iterations):
                        img.save(output_path, quality=quality, optimize=True)
                        if os.path.getsize(output_path) <= target_size_mb * 1024 * 1024:
                            break
                        quality -= 5
                    else:
                        messagebox.showwarning("Warning", f"Could not compress {filename} to target size.")
            except FileNotFoundError:
                # Skip file not found and continue with other files
                messagebox.showwarning("Warning", f"Skipping {filename}: Input file not found.")
                continue
            except Image.UnidentifiedImageError:
                # Skip unsupported image format and continue with other files
                messagebox.showwarning("Warning", f"Skipping {filename}: Unsupported image format.")
                continue
            except Exception as e:
                # Catch remaining errors and display an error message
                messagebox.showerror("Error", f"Unexpected error compressing {filename}: {e}")

        messagebox.showinfo("Compression Complete", "Image compression completed successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressorApp(root)
    root.mainloop()
