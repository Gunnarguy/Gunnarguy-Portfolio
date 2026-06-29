import os
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

IMAGES_TO_OPTIMIZE = [
    "ragmlcore-icon.png",
    "opencone-icon.png",
    "openassistant-icon.png",
    "openresponses-icon.png",
    "openclinic-icon.png"
]

def optimize_images():
    for filename in IMAGES_TO_OPTIMIZE:
        img_path = os.path.join(ASSETS_DIR, filename)
        if not os.path.exists(img_path):
            print(f"Skipping {filename}: Not found")
            continue

        original_size = os.path.getsize(img_path) / 1024
        print(f"Processing {filename} (Original size: {original_size:.2f} KB)...")

        try:
            img = Image.open(img_path)
            # Resize to 512x512 (which is plenty for 306x306 display on mobile/desktop)
            w, h = img.size
            if w > 512 or h > 512:
                resized_img = img.resize((512, 512), Image.Resampling.LANCZOS)
            else:
                resized_img = img
            
            # Save optimized PNG
            resized_img.save(img_path, "PNG", optimize=True)
            
            new_size = os.path.getsize(img_path) / 1024
            print(f"Optimized {filename}: {new_size:.2f} KB (Reduced by {((original_size - new_size)/original_size)*100:.1f}%)")
        except Exception as e:
            print(f"Error optimizing {filename}: {e}")

if __name__ == "__main__":
    optimize_images()
