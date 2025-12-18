#!/usr/bin/env python3
"""
Convert a black phone JPEG to a white PNG with transparent background.
Saves result to: assets/phone-white.png
"""
from pathlib import Path
import sys

try:
    from PIL import Image
except Exception:
    print("Pillow is not installed. Install with: python3 -m pip install --user Pillow")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = ROOT / "assets" / "backup-icons-20251218110938"
INPUT = BACKUP_DIR / "phone.jpeg"
OUT = ROOT / "assets" / "phone-white.png"

if not INPUT.exists():
    print(f"Input not found: {INPUT}")
    sys.exit(1)

print(f"Processing {INPUT} -> {OUT}")

im = Image.open(INPUT).convert("RGBA")
px = im.load()
W, H = im.size

# sample corner pixel as background color
bg = im.getpixel((0, 0))[:3]

BG_THRESH = 30  # tolerance for background
BLACK_THRESH = 80  # threshold for 'near-black'

for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        # if pixel close to background color -> make transparent
        if abs(r - bg[0]) <= BG_THRESH and abs(g - bg[1]) <= BG_THRESH and abs(b - bg[2]) <= BG_THRESH:
            px[x, y] = (255, 255, 255, 0)
            continue
        # if near black -> make white (opaque)
        if r <= BLACK_THRESH and g <= BLACK_THRESH and b <= BLACK_THRESH:
            px[x, y] = (255, 255, 255, 255)

# ensure output dir exists
OUT.parent.mkdir(parents=True, exist_ok=True)
im.save(OUT)
print("Done. Saved:", OUT)
