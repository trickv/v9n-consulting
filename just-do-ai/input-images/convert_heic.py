#!/usr/bin/env python3
import glob
import os
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Get all HEIC files in current directory
heic_files = glob.glob("*.HEIC")

if not heic_files:
    print("No HEIC files found in current directory")
    exit()

print(f"Found {len(heic_files)} HEIC files to convert")

converted = 0
failed = 0

for heic_file in heic_files:
    try:
        # Open HEIC file
        with Image.open(heic_file) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create output filename
            jpg_file = os.path.splitext(heic_file)[0] + '.jpg'
            
            # Save as JPEG with high quality
            img.save(jpg_file, 'JPEG', quality=95)
            print(f"✓ Converted {heic_file} -> {jpg_file}")
            converted += 1
            
    except Exception as e:
        print(f"✗ Failed to convert {heic_file}: {str(e)}")
        failed += 1

print(f"\nConversion complete: {converted} successful, {failed} failed")