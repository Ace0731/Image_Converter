import os
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

# --- Detect Windows version ---
win_version = platform.release()
use_ctk = False
if win_version not in ["7", "Vista", "XP"]:  # CTk safe only on Win 8+
    try:
        import customtkinter as ctk
        use_ctk = True
    except ImportError:
        pass  # fallback to normal tkinter

# --- Core logic (same for both UIs) ---
def shrink_to_fullhd(input_path, output_folder, target_format="webp", quality=85, log_widget=None):
    try:
        img = Image.open(input_path)
        img.thumbnail((1920, 1080), Image.LANCZOS)
        if target_format.lower() in ["jpeg", "jpg", "webp"]:
            img = img.convert("RGB")
        save_kwargs = {}
        if target_format.lower() in ["jpeg", "jpg", "webp"]:
            save_kwargs.update({"quality": quality, "optimize": True})
        filename = os.path.splitext(os.path.basename(input_path))[0] + f".{target_format.lower()}"
        output_path = os.path.join(output_folder, filename)
        img.save(output_path, target_format.upper(), **save_kwargs)
        orig_size = os.path.getsize(input_path)/(1024*1024)
        new_size = os.path.getsize(output_path)/(1024*1024)
        log_widget.insert("end", f"{os.path.basename(input_path)}: {orig_size:.2f}→{new_size:.2f} MB\n")
        log_widget.see("end")
    except Exception as e:
        log_widget.insert("end", f"Error: {input_path} - {e}\n")
        log_widget.see("end")

def select_files():
    files = filedialog.askopenfilenames(title="Select image files")
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
    total_files = len(files)
    for idx, file in enumerate(files, start=1):
        shrink_to_fullhd(file, output_folder, target_format, quality, log_box)
        progress_value = idx / total_files
        if use_ctk:
            progress_bar.set(progress_value)
        else:
            progress_bar["value"] = progress_value * 100
        root.update_idletasks()
    messagebox.showinfo("Done", "All images converted successfully!")

# --- UI (switch dynamically) ---
if use_ctk:
    # --- CustomTkinter UI ---
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Image Resizer & Converter")
    root.geometry("750x600")
    root.resizable(False, False)

    input_files_var = ctk.StringVar()
    output_var = ctk.StringVar()
    quality_var = ctk.IntVar(value=85)
    format_var = ctk.StringVar(value="webp")

    ctk.CTkLabel(root, text="Input Files:").pack(anchor="w", padx=10, pady=(10, 0))
    ctk.CTkEntry(root, textvariable=input_files_var, width=600).pack(anchor="w", padx=10)
    ctk.CTkButton(root, text="Browse Files...", command=select_files).pack(anchor="w", padx=10, pady=5)

    ctk.CTkLabel(root, text="Output Folder:").pack(anchor="w", padx=10, pady=(10, 0))
    ctk.CTkEntry(root, textvariable=output_var, width=600).pack(anchor="w", padx=10)
    ctk.CTkButton(root, text="Browse Folder...", command=select_output).pack(anchor="w", padx=10, pady=5)

    ctk.CTkLabel(root, text="Output Format:").pack(anchor="w", padx=10, pady=(10, 0))
    ctk.CTkOptionMenu(root, variable=format_var, values=["webp", "jpeg", "png"]).pack(anchor="w", padx=10, pady=(0, 10))

    ctk.CTkLabel(root, text="Quality (1-100):").pack(anchor="w", padx=10)
    ctk.CTkSlider(root, from_=10, to=100, number_of_steps=90, variable=quality_var).pack(anchor="w", padx=10, pady=(0, 10))

    ctk.CTkButton(root, text="Convert Images", command=start_conversion, fg_color="#4CAF50").pack(pady=10)

    progress_bar = ctk.CTkProgressBar(root, width=700)
    progress_bar.pack(padx=10, pady=10)
    progress_bar.set(0)

    log_box = ctk.CTkTextbox(root, width=700, height=200)
    log_box.pack(padx=10, pady=10)

else:
    # --- Tkinter fallback for Win7 ---
    root = tk.Tk()
    root.title("Image Resizer & Converter (Legacy Mode)")
    root.geometry("750x600")
    root.resizable(False, False)

    input_files_var = tk.StringVar()
    output_var = tk.StringVar()
    quality_var = tk.IntVar(value=85)
    format_var = tk.StringVar(value="webp")

    tk.Label(root, text="Input Files:").pack(anchor="w", padx=10, pady=(10, 0))
    tk.Entry(root, textvariable=input_files_var, width=100).pack(anchor="w", padx=10)
    tk.Button(root, text="Browse Files...", command=select_files).pack(anchor="w", padx=10, pady=5)

    tk.Label(root, text="Output Folder:").pack(anchor="w", padx=10)
    tk.Entry(root, textvariable=output_var, width=100).pack(anchor="w", padx=10)
    tk.Button(root, text="Browse Folder...", command=select_output).pack(anchor="w", padx=10, pady=5)

    tk.Label(root, text="Output Format:").pack(anchor="w", padx=10)
    tk.OptionMenu(root, format_var, "webp", "jpeg", "png").pack(anchor="w", padx=10)

    tk.Label(root, text="Quality (1-100):").pack(anchor="w", padx=10)
    tk.Scale(root, from_=10, to=100, orient="horizontal", variable=quality_var).pack(anchor="w", padx=10)

    tk.Button(root, text="Convert Images", command=start_conversion, bg="#4CAF50", fg="white").pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
    progress_bar.pack(padx=10, pady=10)

    log_box = tk.Text(root, width=90, height=15)
    log_box.pack(padx=10, pady=10)

root.mainloop()
