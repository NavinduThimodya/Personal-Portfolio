#!/usr/bin/env bash
set -euo pipefail

# Batch-convert black PNG icons to white while preserving transparency.
# Creates a timestamped backup directory under the same `assets/` folder.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS_DIR="$ROOT_DIR/assets"

if [ ! -d "$ASSETS_DIR" ]; then
  echo "No assets directory found at: $ASSETS_DIR"
  exit 1
fi

# Find ImageMagick binary (magick preferred)
if command -v magick >/dev/null 2>&1; then
  IM_CMD="magick"
elif command -v convert >/dev/null 2>&1; then
  IM_CMD="convert"
else
  echo "ImageMagick not found. Install it with: brew install imagemagick"
  exit 2
fi

TS=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="$ASSETS_DIR/backup-icons-$TS"
mkdir -p "$BACKUP_DIR"

echo "Backing up PNGs from $ASSETS_DIR to $BACKUP_DIR"
find "$ASSETS_DIR" -type f -iname '*.png' -print0 | while IFS= read -r -d '' file; do
  relpath="${file#$ROOT_DIR/}"
  mkdir -p "$BACKUP_DIR/$(dirname "$relpath")"
  cp "$file" "$BACKUP_DIR/$relpath"
done

echo "Converting PNG icons to white (this will overwrite originals)."
COUNT=0
find "$ASSETS_DIR" -type f -iname '*.png' -print0 | while IFS= read -r -d '' file; do
  # Use fuzz to catch near-black anti-aliased pixels; preserve alpha
  echo "Processing: $file"
  if [ "$IM_CMD" = "magick" ]; then
    magick "$file" -alpha set -fuzz 20% -fill white -opaque black "$file"
  else
    convert "$file" -alpha set -fuzz 20% -fill white -opaque black "$file"
  fi
  COUNT=$((COUNT+1))
done

echo "Done. Converted $COUNT PNG(s). Originals backed up to: $BACKUP_DIR"

echo "If some icons still look off (contain dark circles etc.), consider using the mask technique or providing original SVGs for cleaner recoloring." 

exit 0
