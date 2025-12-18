import sys
from PIL import Image, ImageDraw

def crop_to_circle(image, zoom=1.0):
    """
    Crops the image to a circle, with an optional zoom.
    The output image will have a transparent background.
    """
    width, height = image.size
    
    # Apply zoom by cropping the center of the image
    if zoom != 1.0:
        # Ensure zoom is not zero or negative
        if zoom <= 0:
            raise ValueError("Zoom factor must be a positive number.")
            
        new_width = width / zoom
        new_height = height / zoom
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2
        image = image.crop((left, top, right, bottom))
        width, height = image.size

    # Create a circular mask. The mask should be a square based on the smallest dimension.
    size = min(width, height)
    
    # Crop the input image to a square before creating the mask.
    # This ensures the circle is not distorted if the zoomed image is not perfectly square.
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    image = image.crop((left, top, right, bottom))
    
    # Create the circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Create the final circular image with a transparent background
    output = Image.new('RGBA', (size, size))
    output.paste(image, (0, 0), mask)
    
    return output

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="""
    Crop an image to a circle with an optional zoom.
    The output image will be a square PNG with the circular-cropped image and a transparent background.
    
    Example Usage:
    python scripts/crop_to_circle.py assets/profile-pic.png assets/profile-pic-circular.png --zoom 1.2
    """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Path to the input image file (e.g., 'assets/profile-pic.png').")
    parser.add_argument("output_file", help="Path to save the circular output image (e.g., 'assets/output.png').")
    parser.add_argument(
        "--zoom", 
        type=float, 
        default=1.0, 
        help="Zoom factor. > 1 to zoom in, < 1 to zoom out. Default is 1.0 (no zoom)."
    )

    args = parser.parse_args()

    try:
        with Image.open(args.input_file) as img:
            # Convert to RGBA to ensure it has an alpha channel for transparency
            img = img.convert("RGBA")
            circular_image = crop_to_circle(img, args.zoom)
            circular_image.save(args.output_file, "PNG")
            print(f"✅ Successfully created circular image at: {args.output_file}")
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
