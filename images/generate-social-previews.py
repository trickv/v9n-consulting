#!/usr/bin/env python3
"""
Generate social media preview images for v9n consulting and Just Do AI
Size: 1200x630px (Open Graph standard)
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap

import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Font files differ per OS; try each candidate until one loads. The original
# script hardcoded Linux DejaVu paths, so it could not run on macOS.
_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]
_REGULAR_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]


def load_font(size, bold=False):
    for path in (_BOLD_CANDIDATES if bold else _REGULAR_CANDIDATES):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_centered(draw, y, text, font, fill, width=1200):
    """Horizontally centre text, accounting for the glyph bearing."""
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (bbox[2] - bbox[0])) // 2 - bbox[0], y), text, fill=fill, font=font)


def draw_tracked(draw, y, text, font, fill, tracking=6, width=1200):
    """PIL has no letter-spacing, so lay out glyphs manually and centre them."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (width - total) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, fill=fill, font=font)
        x += w + tracking


def vertical_gradient(img, top, bottom):
    draw = ImageDraw.Draw(img)
    h = img.height
    for i in range(h):
        draw.rectangle(
            [(0, i), (img.width, i + 1)],
            fill=tuple(int(top[c] - (top[c] - bottom[c]) * (i / h)) for c in range(3)),
        )


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
    title_font = load_font(80, bold=True)
    subtitle_font = load_font(32)
    brand_font = load_font(36, bold=True)

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
    img.save(os.path.join(REPO, 'images', 'v9n-social-preview.jpg'), 'JPEG', quality=95, optimize=True)
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
    title_font = load_font(70, bold=True)
    subtitle_font = load_font(28)
    brand_font = load_font(36, bold=True)

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
    img.save(os.path.join(REPO, 'just-do-ai', 'images', 'justdoai-social-preview.jpg'), 'JPEG', quality=95, optimize=True)
    print("✓ Created justdoai-social-preview.jpg")

def create_whats_new_preview():
    """Create the preview for the recurring Agentic AI & Coding session.

    Deliberately names the *cadence* rather than a specific date: whats-new.html
    rolls its session date forward automatically each week, so a baked-in date
    would go stale in the link preview while the page itself stayed correct.
    """
    img = Image.new('RGB', (1200, 630), color='#f8f9fa')
    vertical_gradient(img, (248, 249, 250), (233, 236, 239))
    draw = ImageDraw.Draw(img)

    eyebrow_font = load_font(26, bold=True)
    title_font = load_font(76, bold=True)
    when_font = load_font(38)
    brand_font = load_font(32, bold=True)

    draw_tracked(draw, 118, "FREE  \u00b7  RECURRING  \u00b7  ONLINE", eyebrow_font, '#7a7a7a', tracking=5)

    draw_centered(draw, 198, "Agentic AI & Coding:", title_font, '#1a1a1a')
    draw_centered(draw, 292, "What's New", title_font, '#1a1a1a')

    # Accent rule between the title and the cadence line
    draw.rectangle([(540, 418), (660, 422)], fill='#1a1a1a')

    draw_centered(draw, 456, "Thursdays \u00b7 2:00 PM Central", when_font, '#555555')

    draw.text((60, 550), "v9n consulting", fill='#1a1a1a', font=brand_font)

    out = os.path.join(REPO, 'images', 'whats-new-social-preview.jpg')
    img.save(out, 'JPEG', quality=95, optimize=True)
    print("\u2713 Created whats-new-social-preview.jpg")


GENERATORS = {
    'v9n': create_v9n_preview,
    'justdoai': create_justdoai_preview,
    'whats-new': create_whats_new_preview,
}

if __name__ == '__main__':
    import sys
    # Name one or more generators to regenerate just those; default is all.
    wanted = sys.argv[1:] or list(GENERATORS)
    for name in wanted:
        if name not in GENERATORS:
            sys.exit("Unknown preview '%s'. Choose from: %s" % (name, ', '.join(GENERATORS)))
        GENERATORS[name]()
    print("\n✓ Done.")
