#!/usr/bin/env python3
"""
Generate social media preview images for v9n consulting and Just Do AI
Size: 1200x630px (Open Graph standard)
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_v9n_preview():
    """Create v9n consulting social preview image"""
    # Create image with gradient background
    img = Image.new('RGB', (1200, 630), color='#f8f9fa')
    draw = ImageDraw.Draw(img)

    # Add subtle gradient effect by drawing rectangles with varying opacity
    for i in range(630):
        # Calculate color gradient from #f8f9fa to #e9ecef
        r = int(248 - (248 - 233) * (i / 630))
        g = int(249 - (249 - 236) * (i / 630))
        b = int(250 - (250 - 239) * (i / 630))
        draw.rectangle([(0, i), (1200, i+1)], fill=(r, g, b))

    # Try to use system fonts, fall back to default
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    # Draw title
    title_line1 = "Technology Strategies"
    title_line2 = "for Small Business"

    # Center the title
    bbox1 = draw.textbbox((0, 0), title_line1, font=title_font)
    title1_width = bbox1[2] - bbox1[0]
    bbox2 = draw.textbbox((0, 0), title_line2, font=title_font)
    title2_width = bbox2[2] - bbox2[0]

    draw.text(((1200 - title1_width) // 2, 180), title_line1, fill='#1a1a1a', font=title_font)
    draw.text(((1200 - title2_width) // 2, 270), title_line2, fill='#2a2a2a', font=title_font)

    # Draw subtitle
    subtitle = "Independent consulting without the enterprise complexity"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox_sub[2] - bbox_sub[0]
    draw.text(((1200 - subtitle_width) // 2, 390), subtitle, fill='#666666', font=subtitle_font)

    # Draw brand name
    brand = "v9n consulting"
    draw.text((60, 550), brand, fill='#1a1a1a', font=brand_font)

    # Save
    img.save('/home/trick/src/github.com/trickv/v9n-consulting/images/v9n-social-preview.jpg', 'JPEG', quality=95, optimize=True)
    print("✓ Created v9n-social-preview.jpg")

def create_justdoai_preview():
    """Create Just Do AI social preview image"""
    # Create image with dark gradient background
    img = Image.new('RGB', (1200, 630), color='#0a0a0a')
    draw = ImageDraw.Draw(img)

    # Add gradient effect
    for i in range(630):
        # Calculate color gradient from #0a0a0a to #1a1a1a
        brightness = int(10 + (26 - 10) * (i / 630))
        draw.rectangle([(0, i), (1200, i+1)], fill=(brightness, brightness, brightness))

    # Try to use system fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    # Draw title
    title_line1 = "Navigate the AI Revolution"
    title_line2 = "with Confidence"

    bbox1 = draw.textbbox((0, 0), title_line1, font=title_font)
    title1_width = bbox1[2] - bbox1[0]
    bbox2 = draw.textbbox((0, 0), title_line2, font=title_font)
    title2_width = bbox2[2] - bbox2[0]

    draw.text(((1200 - title1_width) // 2, 200), title_line1, fill='#ffffff', font=title_font)
    draw.text(((1200 - title2_width) // 2, 280), title_line2, fill='#e8e8e8', font=title_font)

    # Draw subtitle
    subtitle = "Practical AI guidance for small businesses cutting through the hype"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox_sub[2] - bbox_sub[0]
    draw.text(((1200 - subtitle_width) // 2, 390), subtitle, fill='#888888', font=subtitle_font)

    # Draw brand name
    brand = "Just Do AI"
    draw.text((60, 550), brand, fill='#ffffff', font=brand_font)

    # Save
    img.save('/home/trick/src/github.com/trickv/v9n-consulting/just-do-ai/images/justdoai-social-preview.jpg', 'JPEG', quality=95, optimize=True)
    print("✓ Created justdoai-social-preview.jpg")

if __name__ == '__main__':
    create_v9n_preview()
    create_justdoai_preview()
    print("\n✓ All social preview images created successfully!")
    print("  - v9n: /images/v9n-social-preview.jpg")
    print("  - Just Do AI: /just-do-ai/images/justdoai-social-preview.jpg")
