import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

def convert_to_webp(files, output_folder, quality=80, log_widget=None):
    """
    Converts selected image files to WebP format in output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")

    for file in files:
        if file.lower().endswith(image_extensions):
            try:
                filename = os.path.basename(file)
                output_filename = os.path.splitext(filename)[0] + ".webp"
                output_path = os.path.join(output_folder, output_filename)

                # Convert
                img = Image.open(file).convert("RGB")
                img.save(output_path, "webp", quality=int(quality), method=6)

                log_widget.insert("end", f"✔ {filename} → {output_filename}\n")
                log_widget.see("end")

            except Exception as e:
                log_widget.insert("end", f"✖ Error converting {file}: {e}\n")
                log_widget.see("end")

def select_files():
    files = filedialog.askopenfilenames(
        title="Select one or multiple image files",
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("All files", "*.*")
        ]
    )
    if files:
        input_files_var.set("; ".join(files))
        return files
    return []

def select_output():
    folder = filedialog.askdirectory(title="Select folder for WebP images")
    if folder:
        output_var.set(folder)

def start_conversion():
    files = input_files_var.get().split("; ")
    output_folder = output_var.get()
    quality = int(quality_var.get())

    if not files or not output_folder:
        messagebox.showwarning("Missing Selection", "Please select files and output folder.")
        return

    log_box.delete("1.0", "end")
    log_box.insert("end", "--- Starting Conversion ---\n")
    convert_to_webp(files, output_folder, quality, log_box)
    log_box.insert("end", "\n--- Conversion Finished ---\n")
    messagebox.showinfo("Done", "All selected images converted successfully!")

# --- Modern GUI Setup ---
ctk.set_appearance_mode("system")   # "light", "dark", or "system"
ctk.set_default_color_theme("blue") # themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Modern WebP Converter")
root.geometry("700x500")
root.resizable(False, False)

input_files_var = ctk.StringVar()
output_var = ctk.StringVar()
quality_var = ctk.IntVar(value=80)   # FIXED: use IntVar, not StringVar

# Input files
ctk.CTkLabel(root, text="Input Files:").pack(anchor="w", padx=10, pady=(10,0))
ctk.CTkEntry(root, textvariable=input_files_var, width=550).pack(anchor="w", padx=10)
ctk.CTkButton(root, text="Browse Files...", command=select_files).pack(anchor="w", padx=10, pady=5)

# Output folder
ctk.CTkLabel(root, text="Output Folder:").pack(anchor="w", padx=10, pady=(10,5))
ctk.CTkEntry(root, textvariable=output_var, width=550).pack(anchor="w", padx=10)
ctk.CTkButton(root, text="Browse Folder...", command=select_output).pack(anchor="w", padx=10, pady=5)

# Quality slider
ctk.CTkLabel(root, text="Quality (1-100):").pack(anchor="w", padx=10, pady=(10,0))
quality_slider = ctk.CTkSlider(root, from_=10, to=100, number_of_steps=90, variable=quality_var)
quality_slider.pack(anchor="w", padx=10, pady=(0,10))

# Convert button
ctk.CTkButton(root, text="Convert to WebP", command=start_conversion, fg_color="#4CAF50").pack(pady=10)

# Log box
log_box = ctk.CTkTextbox(root, width=650, height=200)
log_box.pack(padx=10, pady=10)

root.mainloop()
