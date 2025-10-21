#!/usr/bin/env python3
"""
Business Card Printer - Convert SVG business cards to print-ready PDF with crop marks
"""

import argparse
import subprocess
import sys
from pathlib import Path
import tempfile
import os

def run_command(cmd, description=""):
    """Run a shell command and handle errors."""
    if description:
        print(f"⚡ {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {description}")
            print(f"Command: {cmd}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def check_dependencies():
    """Check if required tools are available."""
    tools = ['gs', 'python3']
    missing = []
    
    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0:
            missing.append(tool)
    
    if missing:
        print(f"Missing required tools: {', '.join(missing)}")
        print("Please install:")
        if 'gs' in missing:
            print("  - Ghostscript (gs): sudo apt install ghostscript")
        return False
    
    return True

def create_print_file(front_svg=None, back_svg=None, output_pdf="business_cards.pdf", 
                     copies_per_sheet=10, paper_size="letter"):
    """Create a print-ready PDF from SVG business card files."""
    
    if not check_dependencies():
        return False
    
    script_dir = Path(__file__).parent
    template_file = script_dir / "business_card_template.ps"
    svg_converter = script_dir / "svg_to_ps.py"
    
    if not template_file.exists():
        print(f"Error: Template file not found: {template_file}")
        return False
    
    if not svg_converter.exists():
        print(f"Error: SVG converter not found: {svg_converter}")
        return False
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        # Convert SVG files to PostScript procedures
        front_ps = ""
        back_ps = ""
        
        if front_svg and Path(front_svg).exists():
            front_ps_file = temp_dir / "front.ps"
            if not run_command(f"python3 '{svg_converter}' '{front_svg}' -p frontcard -o '{front_ps_file}'",
                             f"Converting front SVG: {front_svg}"):
                return False
            front_ps = front_ps_file.read_text()
        
        if back_svg and Path(back_svg).exists():
            back_ps_file = temp_dir / "back.ps"
            if not run_command(f"python3 '{svg_converter}' '{back_svg}' -p backcard -o '{back_ps_file}'",
                             f"Converting back SVG: {back_svg}"):
                return False
            back_ps = back_ps_file.read_text()
        
        # Create the complete PostScript file
        ps_file = temp_dir / "complete.ps"
        
        with open(ps_file, 'w') as f:
            # Write the template
            f.write(template_file.read_text())
            f.write("\n\n")
            
            # Write the converted SVG procedures
            if front_ps:
                f.write(front_ps)
                f.write("\n\n")
            
            if back_svg and back_ps:
                f.write(back_ps)
                f.write("\n\n")
                
                # Create double-sided printing layout
                f.write("% Front page\n")
                f.write("(front) layoutcards\n")
                f.write("printinfo\n")
                f.write("showpage\n\n")
                
                f.write("% Back page (flipped for proper alignment)\n")
                f.write("gsave\n")
                f.write("pagewidth 0 translate\n")
                f.write("-1 1 scale  % Flip horizontally for back-to-back printing\n")
                f.write("(back) layoutcards\n")
                f.write("grestore\n")
                f.write("printinfo\n")
                f.write("showpage\n")
            else:
                # Single-sided printing
                f.write("% Single-sided layout\n")
                f.write("(front) layoutcards\n")
                f.write("printinfo\n")
                f.write("showpage\n")
        
        # Convert PostScript to PDF using Ghostscript
        gs_cmd = (
            f"gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite "
            f"-dPDFSETTINGS=/prepress "
            f"-dColorImageResolution=300 "
            f"-dGrayImageResolution=300 "
            f"-dMonoImageResolution=1200 "
            f"-sOutputFile='{output_pdf}' "
            f"'{ps_file}'"
        )
        
        if not run_command(gs_cmd, f"Generating PDF: {output_pdf}"):
            return False
        
        print(f"✅ Successfully created: {output_pdf}")
        
        if front_svg and back_svg:
            print(f"📄 Double-sided business cards (front: {Path(front_svg).name}, back: {Path(back_svg).name})")
        elif front_svg:
            print(f"📄 Single-sided business cards (front: {Path(front_svg).name})")
        
        print(f"🖨️  {copies_per_sheet} cards per sheet, print on {paper_size.upper()} paper")
        print(f"✂️  Cut along crop marks for professional results")
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Generate print-ready business card PDF from SVG files",
        epilog="""
Examples:
  # Single-sided cards
  python3 business_card_printer.py --front my_front.svg
  
  # Double-sided cards
  python3 business_card_printer.py --front my_front.svg --back my_back.svg
  
  # Custom output name
  python3 business_card_printer.py --front card.svg -o my_cards.pdf
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--front", "-f", required=True,
                       help="Front side SVG file (required)")
    parser.add_argument("--back", "-b", 
                       help="Back side SVG file (optional, for double-sided)")
    parser.add_argument("--output", "-o", default="business_cards.pdf",
                       help="Output PDF file (default: business_cards.pdf)")
    parser.add_argument("--copies", "-c", type=int, default=10,
                       help="Cards per sheet (default: 10)")
    parser.add_argument("--paper", choices=["letter", "a4"], default="letter",
                       help="Paper size (default: letter)")
    
    args = parser.parse_args()
    
    # Validate input files
    if not Path(args.front).exists():
        print(f"Error: Front SVG file not found: {args.front}")
        sys.exit(1)
    
    if args.back and not Path(args.back).exists():
        print(f"Error: Back SVG file not found: {args.back}")
        sys.exit(1)
    
    # Create the print file
    success = create_print_file(
        front_svg=args.front,
        back_svg=args.back,
        output_pdf=args.output,
        copies_per_sheet=args.copies,
        paper_size=args.paper
    )
    
    if not success:
        print("❌ Failed to create business cards")
        sys.exit(1)

if __name__ == "__main__":
    main()