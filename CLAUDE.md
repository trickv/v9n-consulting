# Claude Code Knowledge Base

This repository contains multiple projects and tools for the "Just Do AI" business and various utility applications.

## 1. Main Website - Just Do AI Business Site

**File**: `index.html`

A complete single-page website for "Just Do AI" - a small business AI consulting company.

### Features
- **Modern Dark Theme**: Professional dark design with gradients and smooth animations
- **Responsive Design**: Mobile-friendly layout that adapts to all screen sizes
- **Contact Box**: Custom contact section with photo placeholder, phone (312-469-0036), and highlighted email (trick@vanstaveren.us)
- **Services Section**: Six main service offerings for AI consulting
- **Hero Section**: Compelling value proposition with call-to-action
- **Problem/Solution Flow**: Visual storytelling with paired images and text
- **Smooth Navigation**: Fixed header with scroll effects and smooth scrolling

### Content Areas
- AI Training & Education
- Productivity Tool Evaluation (Microsoft Copilot, ChatGPT Pro, Claude Pro)
- Marketing & Lead Generation Strategy (GEO - Generative Engine Optimization)
- Custom AI Strategy Development
- Implementation Support
- AI Risk Assessment

### Images Used
- `images/sunset-0.5x-crop.jpg` - Hero section (126KB, optimized)
- `images/trees-no-path.jpg` - "Feeling lost" section (2.09MB)
- `images/path-through-woods.jpg` - "Finding your way" section (1.95MB)

### Technical Details
- Single HTML file with embedded CSS and JavaScript
- Uses modern CSS Grid and Flexbox for layouts
- Progressive JPEG images for better loading
- No external dependencies
- SEO optimized with meta descriptions

## 2. Business Card Printing System

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

### Features
- Prints 10 cards per letter-size sheet (2×5 grid)
- Professional crop marks for accurate cutting
- Double-sided printing with proper alignment
- High-quality PDF output via Ghostscript
- SVG input support with 252pt × 144pt dimensions

## 3. QR Code Generator

**File**: `qr-generator.html`

Web-based QR code generator with customization options.

### Features
- Real-time QR code generation
- Customizable size and error correction levels
- Download as PNG
- Clean, responsive interface
- No server dependencies - runs entirely in browser

## 4. Deployment & Infrastructure

### GitHub Actions Workflow
**File**: `.github/workflows/deploy.yml`
- Triggers on push to main/master branches
- Simple webhook-based deployment system
- No SSH access required

### Webhook Server
**File**: `webhook-server.py`
- Python webhook server for GitHub deployment
- Runs on port 8080
- Handles GitHub webhook events
- Includes HMAC signature verification
- Auto-deployment to `/var/www/html/just-do-ai`

### Configuration
- Repository path: `/var/www/html/just-do-ai`
- Secret-based authentication for webhooks
- Logging and error handling

## 5. Image Assets

### Web-Optimized Images (`/images/`)
- `path-through-woods.jpg` - 1.95MB, 2000×1500px, progressive JPEG
- `trees-no-path.jpg` - 2.09MB, 2000×1500px, progressive JPEG
- `sunset-0.5x-crop.jpg` - 126KB, 1066×828px, progressive JPEG (well optimized)

### Source Images (`/input-images/`)
- Contains original iPhone photos (IMG_*.jpg files)
- Python HEIC converter utility (`convert_heic.py`)
- Virtual environment for HEIC processing (`heic_converter/`)

## 6. Development Tools

### Dependencies
- **Python 3.6+** - For business card printing and webhook server
- **Ghostscript** - For PDF generation from PostScript
- **Virtual Environment** - For HEIC image conversion

### Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 ghostscript
```

## 7. Contact Information

**Business Owner**: Trick VanStaveren
- **Email**: trick@vanstaveren.us (highlighted on website)
- **Phone**: 312-469-0036
- **Business**: Just Do AI - Small Business AI Consulting

## 8. Recent Development History

- ✅ Added comprehensive contact box with photo placeholder
- ✅ Image optimization analysis and recommendations
- ✅ Website styling improvements
- ✅ Deployment pipeline setup
- ✅ Business card printing system development

## 9. Technical Architecture

### Frontend
- **Main Site**: Pure HTML/CSS/JavaScript (no frameworks)
- **Business Cards**: HTML/CSS print layouts
- **QR Generator**: Client-side JavaScript application

### Backend
- **Deployment**: Python webhook server
- **Processing**: PostScript/Ghostscript pipeline for PDF generation
- **CI/CD**: GitHub Actions with webhook triggers

### File Organization
```
just-do-ai/
├── index.html                    # Main website
├── business_card_printer.py      # PDF generation
├── business_card_template.ps     # PostScript template  
├── svg_to_ps.py                 # SVG converter
├── business-cards.html          # Card layout templates
├── qr-generator.html            # QR code tool
├── webhook-server.py            # Deployment server
├── images/                      # Web assets
├── input-images/                # Source photos
├── .github/workflows/           # CI/CD
└── *.svg                       # Design examples
```