# Claude Code Knowledge Base

This repository contains a multi-site consulting business structure with V9N Consulting as the parent company and Just Do AI as a specialized service offering.

## Site Architecture

The repository hosts two related but distinct consulting sites:

### Root Site: V9N Consulting (`/index.html`)
**Parent Company** - Independent technology consulting for small businesses

**Design**: Clean, professional light theme with subtle gradients
- Light background (#ffffff, #f8f9fa)
- Dark text (#1a1a1a, #666)
- Minimalist aesthetic targeting broader business audience

**Services Offered**:
1. AI Strategy & Implementation (links to `/just-do-ai/`)
2. Technology Consulting
3. Digital Transformation
4. Team Training & Education
5. Technology Evaluation
6. Process Automation

**Key Sections**:
- Hero with value proposition for small business technology
- Services overview grid (6 cards)
- About section emphasizing independent consulting approach
- Contact box with professional styling
- Smooth scrolling navigation

### Sub-Site: Just Do AI (`/just-do-ai/index.html`)
**Specialized AI Consulting** - Focused AI services for small businesses

**Design**: Modern dark theme with high contrast
- Dark backgrounds (#0a0a0a, #111)
- Light text (#e8e8e8, #b8b8b8)
- Emotional storytelling with imagery

**AI-Specific Services**:
1. AI Training & Education
2. Productivity Tool Evaluation (Microsoft Copilot, ChatGPT Pro, Claude Pro)
3. Marketing & Lead Generation Strategy (GEO - Generative Engine Optimization)
4. Custom AI Strategy Development
5. Implementation Support
6. AI Risk Assessment

**Key Sections**:
- Hero: "Feeling Lost in the AI Revolution?"
- Problem section with "trees-no-path" image
- Solution section with "path-through-woods" image
- Services grid (6 AI-focused cards)
- Contact box matching V9N style but dark themed

**Images Used**:
- `just-do-ai/images/sunset-0.5x-crop.jpg` - Hero section (126KB, optimized)
- `just-do-ai/images/trees-no-path.jpg` - Problem section (2.09MB)
- `just-do-ai/images/path-through-woods.jpg` - Solution section (1.95MB)

**Technical Details** (both sites):
- Single HTML files with embedded CSS and JavaScript
- Modern CSS Grid and Flexbox layouts
- Progressive JPEG images
- No external dependencies
- SEO optimized with meta descriptions
- Smooth scrolling navigation
- Responsive mobile design

## 1. Business Card Printing System

**Location**: `/just-do-ai/b-cards/`

Complete system for converting SVG business card designs to print-ready PDFs.

### Core Files
- `business_card_printer.py` - Main script to generate print-ready PDFs
- `business_card_template.ps` - PostScript template with N-up layout and crop marks
- `svg_to_ps.py` - Converts SVG files to PostScript procedures
- `example_front.svg` & `example_back.svg` - Sample business card designs

### HTML Templates
- `business-cards.html` - Web-based business card layout (double-sided)
- `business_cardsv5.html` - Enhanced version with improved styling
- `business-card-template.md` - Design guidelines and specifications

### Usage
```bash
# Single-sided cards
python3 business_card_printer.py --front front.svg

# Double-sided cards  
python3 business_card_printer.py --front front.svg --back back.svg
```

### HTML Alternative (Recommended)
For cleaner, more reliable printing use the HTML templates:
- `business_cards_front.html` - References `example_front.svg`
- `business_cards_back.html` - References `example_back.svg`

**Print Settings for Perfect Alignment:**
- When printing from Chrome, set print margins to **0.25" left margin only**, all other margins set to 0
- This centers the card grid properly for double-sided printing alignment
- Print front page first, then flip paper and print back page

### Features
- Prints 10 cards per letter-size sheet (2×5 grid)
- Professional crop marks for accurate cutting
- Double-sided printing with proper alignment
- High-quality PDF output via Ghostscript
- SVG input support with 252pt × 144pt dimensions
- HTML templates with external SVG references for easier editing

## 2. QR Code Generator

**Location**: `/just-do-ai/b-cards/qr-generator.html`

Web-based QR code generator with customization options.

### Features
- Real-time QR code generation
- Customizable size and error correction levels
- Download as PNG
- Clean, responsive interface
- No server dependencies - runs entirely in browser

## 3. Image Assets

### V9N Consulting Images (`/images/`)
- Currently uses placeholder visual in About section
- Future: Professional consulting imagery

### Just Do AI Images (`/just-do-ai/images/`)
- `sunset-0.5x-crop.jpg` - 126KB, 1066×828px, progressive JPEG (well optimized) - Hero section
- `trees-no-path.jpg` - 2.09MB, 2000×1500px, progressive JPEG - "Feeling lost" section
- `path-through-woods.jpg` - 1.95MB, 2000×1500px, progressive JPEG - "Finding your way" section

### Source Images (`/just-do-ai/input-images/`)
- Contains original iPhone photos (IMG_*.jpg files)
- Python HEIC converter utilities (`convert_heic.py`, `convert_heic_portable.py`)
- Virtual environment for HEIC processing (`heic_converter/`)

## 4. Deployment & Infrastructure

**Note**: Deployment configuration may need updating to reflect new two-site structure

### Deployment Path
- Repository deploys to: `/var/www/html/just-do-ai`
- V9N Consulting accessible at root (`/`)
- Just Do AI accessible at (`/just-do-ai/`)

### GitHub Actions Workflow
**File**: `.github/workflows/deploy.yml` (if exists)
- Triggers on push to main branch
- Webhook-based deployment system

### Webhook Server
**File**: `webhook-server.py` (if exists)
- Python webhook server for GitHub deployment
- Port 8080
- HMAC signature verification
- Auto-deployment capability

## 5. Development Tools

### Dependencies
- **Python 3.6+** - For business card printing and HEIC conversion
- **Ghostscript** - For PDF generation from PostScript
- **Virtual Environment** - For HEIC image processing (`just-do-ai/input-images/heic_converter/`)

### Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 ghostscript
```

## 6. Contact Information

**Business Owner**: Patrick "Trick" VanStaveren
- **Email**: trick@vanstaveren.us (highlighted on both websites)
- **Phone**: 312-469-0036
- **Businesses**:
  - V9N Consulting - Independent Technology Consulting
  - Just Do AI - Small Business AI Consulting (specialized service)

## 7. Recent Development History

- ✅ **Oct 2024**: Restructured into parent/sub-site architecture
  - Created V9N Consulting as parent site (light theme, broad tech consulting)
  - Moved Just Do AI to `/just-do-ai/` subdirectory (dark theme, AI-focused)
  - Established clear brand hierarchy and service differentiation
- ✅ **Sep 2024**: Just Do AI initial development
  - Comprehensive contact box with photo placeholder
  - Image optimization and selection
  - Business card printing system
  - Dark theme styling
  - Problem/solution narrative flow

## 8. Technical Architecture

### Frontend
- **V9N Consulting Site**: Pure HTML/CSS/JavaScript (no frameworks, light theme)
- **Just Do AI Site**: Pure HTML/CSS/JavaScript (no frameworks, dark theme)
- **Business Cards**: HTML/CSS print layouts
- **QR Generator**: Client-side JavaScript application

### Backend
- **Deployment**: Python webhook server (if configured)
- **Processing**: PostScript/Ghostscript pipeline for PDF generation
- **CI/CD**: GitHub Actions with webhook triggers (if configured)

### File Organization
```
just-do-ai/                       # Repository root
├── index.html                    # V9N Consulting (parent site)
├── images/                       # V9N Consulting images (placeholder)
├── just-do-ai/                   # Just Do AI sub-site
│   ├── index.html                # Just Do AI main page
│   ├── images/                   # Just Do AI website images
│   │   ├── sunset-0.5x-crop.jpg
│   │   ├── trees-no-path.jpg
│   │   └── path-through-woods.jpg
│   ├── b-cards/                  # Business card printing system
│   │   ├── business_card_printer.py
│   │   ├── business_card_template.ps
│   │   ├── svg_to_ps.py
│   │   ├── example_front.svg
│   │   ├── example_back.svg
│   │   ├── business-cards.html
│   │   ├── business_cardsv5.html
│   │   ├── business_cards_front.html
│   │   ├── business_cards_back.html
│   │   └── qr-generator.html
│   └── input-images/             # Source photos
│       ├── IMG_*.jpg             # iPhone photos
│       ├── convert_heic.py
│       ├── convert_heic_portable.py
│       └── heic_converter/       # Virtual environment
├── .github/                      # Git configuration
│   └── workflows/                # CI/CD (if exists)
├── .claude/                      # Claude Code config
├── CLAUDE.md                     # This knowledge base
└── README-website.md             # Website documentation
```

## 9. Brand Strategy & Positioning

### V9N Consulting (Parent Brand)
- **Target Audience**: Small businesses needing general technology guidance
- **Positioning**: Independent consultant alternative to enterprise consulting firms
- **Tone**: Professional, direct, no-nonsense
- **Visual Identity**: Clean, light, minimalist, approachable
- **Key Message**: "Technology strategies without enterprise complexity"

### Just Do AI (Specialized Service)
- **Target Audience**: Small businesses overwhelmed by AI hype
- **Positioning**: Practical AI guide cutting through marketing noise
- **Tone**: Empathetic, problem-solving, reassuring
- **Visual Identity**: Modern, dark, high-tech, emotional storytelling
- **Key Message**: "Navigate AI confidently with practical guidance"

### Cross-Linking Strategy
- V9N site links to Just Do AI for AI-specific needs
- Both sites share same contact information
- Consistent voice but different visual branding
- Clear service differentiation while maintaining brand relationship