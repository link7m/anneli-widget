#!/usr/bin/env python3
"""
Download free sample images for testing dental veneer AI models.
Uses Unsplash source for royalty-free smile/teeth photos.
"""

import requests
import sys
from pathlib import Path

INPUT_DIR = Path(__file__).parent / "inputs"
INPUT_DIR.mkdir(exist_ok=True)

# Free, royalty-free sample images from Unsplash (direct links to specific photos)
# These are portrait/smile photos with visible teeth
SAMPLE_IMAGES = {
    "smile1": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&q=80",
    "smile2": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "smile3": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&q=80",
}


def download_images():
    print("Downloading sample test images...\n")
    for name, url in SAMPLE_IMAGES.items():
        output_path = INPUT_DIR / f"{name}.jpg"
        if output_path.exists():
            print(f"  SKIP {name} (already exists)")
            continue
        try:
            print(f"  Downloading {name}...")
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(resp.content)
            size_kb = len(resp.content) / 1024
            print(f"  ✓ {name}.jpg ({size_kb:.0f} KB)")
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    # Check what we have
    images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
    print(f"\nTotal test images available: {len(images)}")
    for img in sorted(images):
        print(f"  {img.name} ({img.stat().st_size / 1024:.0f} KB)")

    if not images:
        print("\nNo images available. Please manually add selfie photos to:")
        print(f"  {INPUT_DIR}/")
        sys.exit(1)


if __name__ == "__main__":
    download_images()
