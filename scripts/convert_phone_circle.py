#!/usr/bin/env python3
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Install with: python3 -m pip install --user Pillow")
    sys.exit(2)

def make_square(image_path: Path):
    """
    Makes an image square by padding it with a transparent background.
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size

        if width == height:
            print(f"Image is already square: {image_path}")
            return

        # Get the new size
        new_size = max(width, height)

        # Create a new image with a transparent background
        new_img = Image.new("RGBA", (new_size, new_size), (0, 0, 0, 0))

        # Paste the original image into the center of the new image
        paste_position = ((new_size - width) // 2, (new_size - height) // 2)
        new_img.paste(img, paste_position)

        # Save the new image, overwriting the original
        new_img.save(image_path)
        print(f"Image successfully converted to square: {image_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    image_path = Path("assets/profile-pic.png")

    if not image_path.is_file():
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)

    make_square(image_path)
