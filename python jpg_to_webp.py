import os
from tkinter import Tk, filedialog
from PIL import Image

def convert_jpg_to_webp(input_folder, output_folder, quality=80):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.lower().endswith(".jpg"):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".webp")

            img = Image.open(input_path).convert("RGB")
            img.save(output_path, "webp", quality=quality)
            print(f"Converted: {file} -> {os.path.basename(output_path)}")

if __name__ == "__main__":
    # GUI folder picker
    root = Tk()
    root.withdraw()
    input_folder = filedialog.askdirectory(title="Select folder with JPG images")
    output_folder = filedialog.askdirectory(title="Select output folder for WebP images")

    if input_folder and output_folder:
        convert_jpg_to_webp(input_folder, output_folder, quality=80)
        print("All images converted successfully.")
    else:
        print("No folder selected.")
