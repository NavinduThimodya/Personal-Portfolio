#!/usr/bin/env python3
"""
Batch-convert near-black pixels in PNG icons to white while preserving alpha.
Creates a timestamped backup of original PNGs under assets/backup-icons-<ts>/

Usage:
  python3 scripts/convert_icons_pillow.py

This script requires Pillow: `python3 -m pip install --user Pillow`
"""
import sys
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
except Exception:
    print("Pillow is not installed. Install with: python3 -m pip install --user Pillow")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

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
    import shutil
    shutil.copy2(p, dest)

THRESH = 60  # threshold for 'near-black' for each RGB channel

def convert_image(path: Path):
    im = Image.open(path).convert("RGBA")
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
    if changed:
        im.putdata(new_pixels)
        im.save(path)
    return changed

total_changed = 0
for p in png_files:
    print(f"Processing: {p}")
    try:
        c = convert_image(p)
        if c:
            print(f"  converted {c} pixel(s)")
        total_changed += c
    except Exception as e:
        print(f"  error processing {p}: {e}")

print(f"Done. Total pixels converted: {total_changed}. Originals backed up to {BACKUP}")
