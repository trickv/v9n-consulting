# Business Card Printer

A complete system for converting SVG business card designs to print-ready PDFs with crop marks and proper N-up layout for home printing.

## Features

- 🎨 **SVG Input**: Design your cards in any SVG editor (Inkscape, Adobe Illustrator, etc.)
- 📐 **Standard Size**: Supports standard 3.5" × 2" business card dimensions  
- 🖨️ **N-up Layout**: Fits 10 cards per letter-size sheet (2×5 grid)
- ✂️ **Crop Marks**: Professional crop marks for accurate cutting
- 🔄 **Double-sided**: Supports front/back printing with proper alignment
- 📄 **Print Ready**: High-quality PDF output optimized for home/office printers

## Quick Start

1. **Create your SVG files** with dimensions 252pt × 144pt (3.5" × 2"):
   - `front.svg` - Front side of your business card
   - `back.svg` - Back side (optional)

2. **Generate print-ready PDF**:
   ```bash
   # Single-sided cards
   python3 business_card_printer.py --front front.svg
   
   # Double-sided cards  
   python3 business_card_printer.py --front front.svg --back back.svg
   ```

3. **Print and cut**:
   - Print the generated `business_cards.pdf`
   - Use the crop marks to cut your cards accurately

## Requirements

- Python 3.6+
- Ghostscript (`gs` command)

### Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 ghostscript
```

### Installation (macOS)
```bash
brew install ghostscript
```

## Usage

### Basic Usage
```bash
python3 business_card_printer.py --front my_card_front.svg
```

### Full Options
```bash
python3 business_card_printer.py \
  --front front_design.svg \
  --back back_design.svg \
  --output my_cards.pdf \
  --copies 10 \
  --paper letter
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--front` | `-f` | Front side SVG file (required) | - |
| `--back` | `-b` | Back side SVG file (optional) | - |
| `--output` | `-o` | Output PDF filename | `business_cards.pdf` |
| `--copies` | `-c` | Cards per sheet | `10` |
| `--paper` | - | Paper size (`letter` or `a4`) | `letter` |

## SVG Design Guidelines

### Dimensions
- **Width**: 252 points (3.5 inches)
- **Height**: 144 points (2 inches)  
- **Aspect Ratio**: 1.75:1

### Design Tips
1. **Keep text at least 0.125" from edges** to account for cutting tolerances
2. **Use high-contrast colors** for better print quality
3. **Avoid very thin lines** (< 1pt) that may not print well
4. **Test print** a single sheet before printing multiple copies

### Example SVG Template
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="252" height="144" viewBox="0 0 252 144" xmlns="http://www.w3.org/2000/svg">
  <!-- Your design here -->
  <rect width="252" height="144" fill="white"/>
  <text x="20" y="30" font-family="Helvetica-Bold" font-size="16">Your Name</text>
  <text x="20" y="50" font-family="Helvetica" font-size="12">Your Title</text>
</svg>
```

## File Structure

```
business-card-printer/
├── business_card_printer.py    # Main script
├── business_card_template.ps   # PostScript template
├── svg_to_ps.py               # SVG converter
├── example_front.svg          # Example front design
├── example_back.svg           # Example back design
└── README.md                  # This file
```

## How It Works

1. **SVG Parsing**: Your SVG files are parsed and converted to PostScript procedures
2. **Template Application**: The PostScript template positions cards in an N-up layout
3. **Crop Mark Generation**: Professional crop marks are added around each card
4. **PDF Generation**: Ghostscript converts everything to a high-quality PDF

## Printing Tips

### For Best Results
- **Paper**: Use 100-110gsm cardstock for professional feel
- **Printer Settings**: 
  - Quality: High/Best
  - Paper Type: Cardstock
  - Print Scale: 100% (no scaling)
- **Cutting**: Use a paper cutter or sharp craft knife with metal ruler

### Double-sided Printing
1. Print page 1 (fronts)
2. Flip paper and feed back into printer
3. Print page 2 (backs)
4. The template automatically handles proper alignment

## Troubleshooting

### Common Issues

**SVG not displaying correctly?**
- Check that your SVG uses standard elements (rect, circle, text, path)
- Complex features like gradients or filters may need manual conversion

**Cards not aligned when cutting?**
- Ensure printer is not scaling the document
- Check that paper is loaded straight
- Verify print margins are set correctly

**Text appears garbled?**
- Use standard fonts (Helvetica, Arial, Times)
- Avoid system-specific or custom fonts

### Getting Help
- Check the example SVG files for reference
- Ensure all dependencies are installed correctly
- Verify your SVG dimensions match the business card size

## License

This project is released into the public domain. Feel free to use, modify, and distribute as needed.

---

Happy printing! 🎉