#!/usr/bin/env python3
"""
SVG to PostScript converter for business card printing.
Converts SVG files to PostScript procedures that can be embedded in the business card template.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import base64
import subprocess

class SVGToPS:
    def __init__(self):
        self.fonts_used = set()
        self.images_embedded = []
        
    def parse_transform(self, transform_str):
        """Parse SVG transform attribute into PostScript operations."""
        if not transform_str:
            return ""
        
        operations = []
        
        # Handle translate(x,y)
        translate_match = re.search(r'translate\(([^)]+)\)', transform_str)
        if translate_match:
            coords = translate_match.group(1).split(',')
            x = float(coords[0].strip())
            y = float(coords[1].strip()) if len(coords) > 1 else 0
            operations.append(f"{x} {y} translate")
        
        # Handle scale(x,y)
        scale_match = re.search(r'scale\(([^)]+)\)', transform_str)
        if scale_match:
            scales = scale_match.group(1).split(',')
            sx = float(scales[0].strip())
            sy = float(scales[1].strip()) if len(scales) > 1 else sx
            operations.append(f"{sx} {sy} scale")
        
        # Handle rotate(angle)
        rotate_match = re.search(r'rotate\(([^)]+)\)', transform_str)
        if rotate_match:
            angle = float(rotate_match.group(1).strip())
            operations.append(f"{angle} rotate")
        
        return "\n".join(operations)
    
    def convert_color(self, color_str):
        """Convert SVG color to PostScript color values."""
        if not color_str or color_str == "none":
            return None
        
        # Handle hex colors
        if color_str.startswith('#'):
            hex_color = color_str[1:]
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            return f"{r:.3f} {g:.3f} {b:.3f} setrgbcolor"
        
        # Handle named colors (basic set)
        color_map = {
            'black': '0 0 0 setrgbcolor',
            'white': '1 1 1 setrgbcolor',
            'red': '1 0 0 setrgbcolor',
            'green': '0 1 0 setrgbcolor',
            'blue': '0 0 1 setrgbcolor',
            'yellow': '1 1 0 setrgbcolor',
            'cyan': '0 1 1 setrgbcolor',
            'magenta': '1 0 1 setrgbcolor',
        }
        
        return color_map.get(color_str.lower(), '0 setgray')
    
    def convert_rect(self, elem):
        """Convert SVG rect to PostScript."""
        x = float(elem.get('x', 0))
        y = float(elem.get('y', 0))
        width = float(elem.get('width', 0))
        height = float(elem.get('height', 0))
        
        ps_code = []
        ps_code.append("newpath")
        ps_code.append(f"{x} {y} moveto")
        ps_code.append(f"{x + width} {y} lineto")
        ps_code.append(f"{x + width} {y + height} lineto")
        ps_code.append(f"{x} {y + height} lineto")
        ps_code.append("closepath")
        
        # Handle fill and stroke
        fill = elem.get('fill')
        stroke = elem.get('stroke')
        
        if fill and fill != 'none':
            fill_color = self.convert_color(fill)
            if fill_color:
                ps_code.append("gsave")
                ps_code.append(fill_color)
                ps_code.append("fill")
                ps_code.append("grestore")
        
        if stroke and stroke != 'none':
            stroke_color = self.convert_color(stroke)
            stroke_width = elem.get('stroke-width', '1')
            if stroke_color:
                ps_code.append("gsave")
                ps_code.append(f"{stroke_width} setlinewidth")
                ps_code.append(stroke_color)
                ps_code.append("stroke")
                ps_code.append("grestore")
        
        return "\n".join(ps_code)
    
    def convert_circle(self, elem):
        """Convert SVG circle to PostScript."""
        cx = float(elem.get('cx', 0))
        cy = float(elem.get('cy', 0))
        r = float(elem.get('r', 0))
        
        ps_code = []
        ps_code.append("newpath")
        ps_code.append(f"{cx} {cy} {r} 0 360 arc")
        
        # Handle fill and stroke
        fill = elem.get('fill')
        stroke = elem.get('stroke')
        
        if fill and fill != 'none':
            fill_color = self.convert_color(fill)
            if fill_color:
                ps_code.append("gsave")
                ps_code.append(fill_color)
                ps_code.append("fill")
                ps_code.append("grestore")
        
        if stroke and stroke != 'none':
            stroke_color = self.convert_color(stroke)
            stroke_width = elem.get('stroke-width', '1')
            if stroke_color:
                ps_code.append("gsave")
                ps_code.append(f"{stroke_width} setlinewidth")
                ps_code.append(stroke_color)
                ps_code.append("stroke")
                ps_code.append("grestore")
        
        return "\n".join(ps_code)
    
    def convert_text(self, elem):
        """Convert SVG text to PostScript."""
        x = float(elem.get('x', 0))
        y = float(elem.get('y', 0))
        text = elem.text or ""
        # Clean up text: remove newlines and extra whitespace
        text = ' '.join(text.split())
        
        # Extract font information
        font_family = elem.get('font-family', 'Helvetica')
        font_size = elem.get('font-size', '12')
        # Remove 'px' suffix if present
        if font_size.endswith('px'):
            font_size = font_size[:-2]
        font_weight = elem.get('font-weight', 'normal')
        
        # Convert font family to PostScript font name
        ps_font = font_family.replace(' ', '-')
        if font_weight == 'bold':
            ps_font += '-Bold'
        
        self.fonts_used.add(ps_font)
        
        ps_code = []
        ps_code.append(f"/{ps_font} findfont {font_size} scalefont setfont")
        
        # Handle text color
        fill = elem.get('fill', 'black')
        fill_color = self.convert_color(fill)
        if fill_color:
            ps_code.append(fill_color)
        
        ps_code.append(f"{x} {y} moveto")
        ps_code.append(f"({text}) show")
        
        return "\n".join(ps_code)
    
    def convert_path(self, elem):
        """Convert SVG path to PostScript (basic support)."""
        d = elem.get('d', '')
        if not d:
            return ""
        
        ps_code = ["newpath"]
        
        # Very basic path parsing - you may want to expand this
        commands = re.findall(r'[MmLlHhVvCcSsQqTtAaZz][^MmLlHhVvCcSsQqTtAaZz]*', d)
        
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd:
                continue
                
            op = cmd[0]
            coords = re.findall(r'-?\d*\.?\d+', cmd[1:])
            coords = [float(c) for c in coords]
            
            if op.upper() == 'M':  # Move to
                if len(coords) >= 2:
                    ps_code.append(f"{coords[0]} {coords[1]} moveto")
            elif op.upper() == 'L':  # Line to
                if len(coords) >= 2:
                    ps_code.append(f"{coords[0]} {coords[1]} lineto")
            elif op.upper() == 'Z':  # Close path
                ps_code.append("closepath")
        
        # Handle fill and stroke
        fill = elem.get('fill')
        stroke = elem.get('stroke')
        
        if fill and fill != 'none':
            fill_color = self.convert_color(fill)
            if fill_color:
                ps_code.append("gsave")
                ps_code.append(fill_color)
                ps_code.append("fill")
                ps_code.append("grestore")
        
        if stroke and stroke != 'none':
            stroke_color = self.convert_color(stroke)
            stroke_width = elem.get('stroke-width', '1')
            if stroke_color:
                ps_code.append("gsave")
                ps_code.append(f"{stroke_width} setlinewidth")
                ps_code.append(stroke_color)
                ps_code.append("stroke")
                ps_code.append("grestore")
        
        return "\n".join(ps_code)
    
    def convert_element(self, elem):
        """Convert a single SVG element to PostScript."""
        ps_code = []
        
        # Handle transforms
        transform = elem.get('transform')
        if transform:
            ps_code.append("gsave")
            ps_code.append(self.parse_transform(transform))
        
        # Convert based on element type
        tag = elem.tag.lower()
        if tag.endswith('rect'):
            ps_code.append(self.convert_rect(elem))
        elif tag.endswith('circle'):
            ps_code.append(self.convert_circle(elem))
        elif tag.endswith('text'):
            ps_code.append(self.convert_text(elem))
        elif tag.endswith('path'):
            ps_code.append(self.convert_path(elem))
        elif tag.endswith('g'):  # Group
            for child in elem:
                ps_code.append(self.convert_element(child))
        
        if transform:
            ps_code.append("grestore")
        
        return "\n".join(filter(None, ps_code))
    
    def convert_svg_file(self, svg_path, procedure_name="cardcontent"):
        """Convert entire SVG file to PostScript procedure."""
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Get SVG dimensions
            width = root.get('width', '252')  # Default to business card width
            height = root.get('height', '144')  # Default to business card height
            
            # Remove units if present
            width = re.sub(r'[^\d.]', '', str(width))
            height = re.sub(r'[^\d.]', '', str(height))
            
            ps_code = []
            ps_code.append(f"% Generated from {svg_path}")
            ps_code.append(f"/{procedure_name} {{")
            ps_code.append("    gsave")
            
            # Scale to fit business card if needed
            if width and height:
                scale_x = 252 / float(width) if float(width) > 252 else 1
                scale_y = 144 / float(height) if float(height) > 144 else 1
                scale = min(scale_x, scale_y)
                if scale != 1:
                    ps_code.append(f"    {scale} {scale} scale")
            
            # Convert all child elements
            for elem in root:
                elem_ps = self.convert_element(elem)
                if elem_ps:
                    # Indent the converted code
                    indented = "\n".join(f"    {line}" for line in elem_ps.split("\n") if line.strip())
                    ps_code.append(indented)
            
            ps_code.append("    grestore")
            ps_code.append("} def")
            
            return "\n".join(ps_code)
        
        except ET.ParseError as e:
            print(f"Error parsing SVG file {svg_path}: {e}", file=sys.stderr)
            return f"% Error parsing {svg_path}: {e}"
        except Exception as e:
            print(f"Error converting {svg_path}: {e}", file=sys.stderr)
            return f"% Error converting {svg_path}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Convert SVG files to PostScript procedures")
    parser.add_argument("svg_file", help="Input SVG file")
    parser.add_argument("-o", "--output", help="Output PostScript file")
    parser.add_argument("-p", "--procedure", default="cardcontent", 
                       help="PostScript procedure name (default: cardcontent)")
    
    args = parser.parse_args()
    
    converter = SVGToPS()
    ps_code = converter.convert_svg_file(args.svg_file, args.procedure)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(ps_code)
        print(f"Converted {args.svg_file} -> {args.output}")
    else:
        print(ps_code)
    
    if converter.fonts_used:
        print(f"Fonts used: {', '.join(converter.fonts_used)}", file=sys.stderr)

if __name__ == "__main__":
    main()