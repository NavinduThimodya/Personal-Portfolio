#!/usr/bin/env python3
"""
Crops an image by a specified fraction from all sides.

Usage:
  python3 scripts/crop_image.py <image_path> <fraction_to_crop>
"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Install with: python3 -m pip install --user Pillow")
    sys.exit(2)

def crop_image(image_path: Path, fraction: float):
    """
    Crops an image by a given fraction from all sides.
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size

        # Calculate the amount to crop from each side
        crop_width = int(width * fraction)
        crop_height = int(height * fraction)

        # Define the crop box (left, upper, right, lower)
        left = crop_width
        upper = crop_height
        right = width - crop_width
        lower = height - crop_height
        
        # Check if the crop dimensions are valid
        if left >= right or upper >= lower:
            print(f"Error: Crop dimensions are invalid. The fraction {fraction} is too large.")
            sys.exit(1)

        # Crop the image
        cropped_img = img.crop((left, upper, right, lower))

        # Save the new image, overwriting the original
        cropped_img.save(image_path)
        print(f"Image successfully cropped by {fraction} from all sides: {image_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/crop_image.py <image_path> <fraction_to_crop>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    
    try:
        fraction = float(sys.argv[2])
    except ValueError:
        print("Error: Invalid fraction provided. Please provide a number (e.g., 0.125 for 1/8).")
        sys.exit(1)


    if not image_path.is_file():
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)

    crop_image(image_path, fraction)
