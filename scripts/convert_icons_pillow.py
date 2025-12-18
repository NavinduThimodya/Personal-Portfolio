#!/usr/bin/env python3
"""
Batch-convert near-black pixels in PNG icons to white while preserving alpha.
If a path to an image is provided, it converts that single image and saves it
with a '_white' suffix in the assets directory.
Otherwise, it batch-converts all PNGs in the assets directory, backing them up first.

Usage:
  python3 scripts/convert_icons_pillow.py [PATH_TO_IMAGE]

This script requires Pillow: `python3 -m pip install --user Pillow`
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime
import shutil

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Install with: python3 -m pip install --user Pillow")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
THRESH = 200  # threshold for 'near-black' for each RGB channel

def process_pixels(im):
    pixels = im.getdata()
    new_pixels = []
    changed = 0
    for r, g, b, a in pixels:
        # consider pixel if sufficiently opaque
        if a > 10 and r <= THRESH and g <= THRESH and b <= THRESH:
            new_pixels.append((255, 255, 255, a))
            changed += 1
        else:
            new_pixels.append((r, g, b, a))
    return new_pixels, changed

def convert_image(path: Path, output_path: Path):
    """Converts near-black pixels in an image to white and saves it."""
    try:
        im = Image.open(path).convert("RGBA")
        new_pixels, changed = process_pixels(im)

        if changed > 0:
            im.putdata(new_pixels)
            im.save(output_path)
            print(f"Saved converted image to: {output_path}")
            print(f"  converted {changed} pixel(s)")
        else:
            print("No pixels were dark enough to convert.")
        return changed
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return 0

def batch_convert():
    """Backs up and converts all PNG files in the assets directory."""
    if not ASSETS.exists():
        print(f"No assets directory found at: {ASSETS}")
        sys.exit(1)

    TS = datetime.now().strftime("%Y%m%d%H%M%S")
    BACKUP = ASSETS / f"backup-icons-{TS}"
    BACKUP.mkdir(parents=True, exist_ok=True)

    png_files = list(ASSETS.rglob("*.png"))
    if not png_files:
        print("No PNG files found under assets/. Nothing to do.")
        sys.exit(0)

    print(f"Backing up {len(png_files)} PNG(s) to: {BACKUP}")
    for p in png_files:
        dest = BACKUP / p.relative_to(ASSETS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)

    total_changed = 0
    for p in png_files:
        print(f"Processing: {p}")
        try:
            im = Image.open(p).convert("RGBA")
            new_pixels, changed = process_pixels(im)
            if changed:
                im.putdata(new_pixels)
                im.save(p) # Overwrite original
                print(f"  converted {changed} pixel(s)")
            total_changed += changed
        except Exception as e:
            print(f"  error processing {p}: {e}")


    print(f"\nDone. Total pixels converted: {total_changed}. Originals backed up to {BACKUP}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert near-black pixels in PNG icons to white.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a single image and save it to assets/my_icon_white.png
  python3 scripts/convert_icons_pillow.py path/to/my_icon.png

  # Run in batch mode on all PNGs in the assets/ directory
  python3 scripts/convert_icons_pillow.py
"""
    )
    parser.add_argument('image_path', nargs='?', default=None, help='Optional path to a single image to convert.')
    args = parser.parse_args()

    if args.image_path:
        input_path = Path(args.image_path)
        if not input_path.is_file():
            print(f"Error: Image file not found or is not a file: {input_path}")
            sys.exit(1)

        output_filename = f"{input_path.stem}_white{input_path.suffix}"
        output_path = ASSETS / output_filename
        
        print(f"Converting single image: {input_path}")
        convert_image(input_path, output_path)
    else:
        print("No image path provided. Running in batch mode on all assets.")
        batch_convert()

if __name__ == "__main__":
    main()
