import os
from PIL import Image, ImageDraw, ImageFont

def generate():
    # 32x32 image
    width, height = 32, 32
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw rounded rectangle with gradient
    for y in range(height):
        # Interpolate color from #00f2fe (0, 242, 254) to #00b8d4 (0, 184, 212)
        r = 0
        g = int(242 - (242 - 184) * (y / height))
        b = int(254 - (254 - 212) * (y / height))
        for x in range(width):
            # Check if (x, y) is inside rounded rect with radius 8
            inside = True
            if x < 8 and y < 8:
                if (x-8)**2 + (y-8)**2 > 64: inside = False
            elif x > 24 and y < 8:
                if (x-24)**2 + (y-8)**2 > 64: inside = False
            elif x < 8 and y > 24:
                if (x-8)**2 + (y-24)**2 > 64: inside = False
            elif x > 24 and y > 24:
                if (x-24)**2 + (y-24)**2 > 64: inside = False
            
            if inside:
                image.putpixel((x, y), (r, g, b, 255))

    # Try loading Arial Bold or Helvetica Bold
    font = None
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 12)
                break
            except Exception as e:
                print(f"Failed to load font {path}: {e}")
    if font is None:
        font = ImageFont.load_default()

    # Draw GH text centered
    text = "GH"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    # Adjust vertical centering offset slightly
    y = (height - text_height) // 2 - 1
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as favicon.ico
    image.save("favicon.ico", format="PNG")
    print("favicon.ico generated successfully.")

if __name__ == "__main__":
    generate()
