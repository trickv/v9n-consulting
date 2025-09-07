# Claude Code Knowledge Base

## Business Card Printing System

This repository includes a complete business card printing system for home/office printing:

### Files
- `business_card_printer.py` - Main script to generate print-ready PDFs
- `business_card_template.ps` - PostScript template with N-up layout and crop marks
- `svg_to_ps.py` - Converts SVG files to PostScript procedures
- `example_front.svg` & `example_back.svg` - Sample business card designs

### Usage
```bash
# Single-sided cards
python3 business_card_printer.py --front front.svg

# Double-sided cards  
python3 business_card_printer.py --front front.svg --back back.svg
```

### SVG Requirements
- Dimensions: 252pt × 144pt (3.5" × 2")
- Aspect ratio: 1.75:1
- Use standard fonts (Helvetica, Arial, Times)
- Keep text ≥0.125" from edges

### Features
- Prints 10 cards per letter-size sheet (2×5 grid)
- Professional crop marks for accurate cutting
- Double-sided printing with proper alignment
- High-quality PDF output via Ghostscript

### Dependencies
- Python 3.6+
- Ghostscript (`gs` command)

Install on Ubuntu/Debian:
```bash
sudo apt install python3 ghostscript
```