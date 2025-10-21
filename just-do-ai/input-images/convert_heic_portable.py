#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "Pillow",
#     "pillow_heif",
# ]
# ///
import argparse
import os
import sys
from PIL import Image
import pillow_heif

def convert_heic_file(heic_file):
    """Convert a single HEIC file to JPEG."""
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
            return True
            
    except Exception as e:
        print(f"✗ Failed to convert {heic_file}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert HEIC files to JPEG format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s image.HEIC                    # Convert single file
  %(prog)s *.HEIC                       # Convert all HEIC files in current dir
  %(prog)s file1.HEIC file2.HEIC        # Convert specific files
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='HEIC files to convert'
    )
    
    args = parser.parse_args()
    
    # Register HEIF opener with Pillow
    pillow_heif.register_heif_opener()
    
    # Filter out non-existent files and warn about them
    existing_files = []
    for file in args.files:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            print(f"Warning: File not found: {file}", file=sys.stderr)
    
    if not existing_files:
        print("Error: No valid files to convert", file=sys.stderr)
        sys.exit(1)
    
    print(f"Converting {len(existing_files)} file(s)...")
    
    converted = 0
    failed = 0
    
    for heic_file in existing_files:
        if convert_heic_file(heic_file):
            converted += 1
        else:
            failed += 1
    
    print(f"\nConversion complete: {converted} successful, {failed} failed")
    
    # Exit with error code if any conversions failed
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()