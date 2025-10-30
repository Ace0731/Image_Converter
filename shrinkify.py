import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

def shrink_to_fullhd(input_path, output_folder, target_format="webp", quality=85, log_widget=None):
    """
    Shrink any image to Full HD (1920x1080 max) and save in chosen format.
    """
    try:
        img = Image.open(input_path)

        # Resize while keeping aspect ratio
        img.thumbnail((1920, 1080), Image.LANCZOS)

        # Convert to RGB if saving in lossy format
        if target_format.lower() in ["jpeg", "jpg", "webp"]:
            img = img.convert("RGB")

        # Save options
        save_kwargs = {}
        if target_format.lower() in ["jpeg", "jpg", "webp"]:
            save_kwargs.update({"quality": quality, "optimize": True, "method": 6})

        # Build output path
        filename = os.path.splitext(os.path.basename(input_path))[0] + f".{target_format.lower()}"
        output_path = os.path.join(output_folder, filename)

        # Save image
        img.save(output_path, target_format.upper(), **save_kwargs)

        # Log size difference
        orig_size = os.path.getsize(input_path) / (1024 * 1024)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        log_widget.insert("end", f"✔ {os.path.basename(input_path)}: {orig_size:.2f} MB → {new_size:.2f} MB "
                                 f"[{target_format.upper()}]\n")
        log_widget.see("end")

    except Exception as e:
        log_widget.insert("end", f"✖ Error: {input_path} - {e}\n")
        log_widget.see("end")

def select_files():
    files = filedialog.askopenfilenames(
        title="Select image files",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.gif"), ("All files", "*.*")]
    )
    if files:
        input_files_var.set("; ".join(files))

def select_output():
    folder = filedialog.askdirectory(title="Select output folder")
    if folder:
        output_var.set(folder)

def start_conversion():
    files = input_files_var.get().split("; ")
    output_folder = output_var.get()
    target_format = format_var.get()
    quality = int(quality_var.get())

    if not files or not output_folder:
        messagebox.showwarning("Missing Selection", "Please select files and output folder.")
        return

    log_box.delete("1.0", "end")
    log_box.insert("end", "--- Starting Conversion ---\n")

    total_files = len(files)
    for idx, file in enumerate(files, start=1):
        shrink_to_fullhd(file, output_folder, target_format, quality, log_box)

        # Update progress bar
        progress = idx / total_files
        progress_bar.set(progress)
        root.update_idletasks()

    log_box.insert("end", "\n--- Conversion Finished ---\n")
    progress_bar.set(1)  # 100%
    messagebox.showinfo("Done", "All images converted successfully!")

# --- GUI Setup ---
ctk.set_appearance_mode("system")  # light/dark/system
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Image Resizer & Converter")
root.geometry("750x600")
root.resizable(False, False)

input_files_var = ctk.StringVar()
output_var = ctk.StringVar()
quality_var = ctk.IntVar(value=85)
format_var = ctk.StringVar(value="webp")

# Input files
ctk.CTkLabel(root, text="Input Files:").pack(anchor="w", padx=10, pady=(10, 0))
ctk.CTkEntry(root, textvariable=input_files_var, width=600).pack(anchor="w", padx=10)
ctk.CTkButton(root, text="Browse Files...", command=select_files).pack(anchor="w", padx=10, pady=5)

# Output folder
ctk.CTkLabel(root, text="Output Folder:").pack(anchor="w", padx=10, pady=(10, 0))
ctk.CTkEntry(root, textvariable=output_var, width=600).pack(anchor="w", padx=10)
ctk.CTkButton(root, text="Browse Folder...", command=select_output).pack(anchor="w", padx=10, pady=5)

# Format dropdown
ctk.CTkLabel(root, text="Output Format:").pack(anchor="w", padx=10, pady=(10, 0))
format_dropdown = ctk.CTkOptionMenu(root, variable=format_var, values=["webp", "jpeg", "png"])
format_dropdown.pack(anchor="w", padx=10, pady=(0, 10))

# Quality slider
ctk.CTkLabel(root, text="Quality (1-100, applies to JPEG/WEBP):").pack(anchor="w", padx=10, pady=(10, 0))
ctk.CTkSlider(root, from_=10, to=100, number_of_steps=90, variable=quality_var).pack(anchor="w", padx=10, pady=(0, 10))

# Convert button
ctk.CTkButton(root, text="Convert Images", command=start_conversion, fg_color="#4CAF50").pack(pady=10)

# Progress bar
progress_bar = ctk.CTkProgressBar(root, width=700)
progress_bar.pack(padx=10, pady=10)
progress_bar.set(0)

# Log box
log_box = ctk.CTkTextbox(root, width=700, height=200)
log_box.pack(padx=10, pady=10)

root.mainloop()
