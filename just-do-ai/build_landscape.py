#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Build ai_tools_landscape.html from ai_tools_landscape.yaml."""

import html
import sys
from datetime import date
from pathlib import Path

import yaml


def h(text: str) -> str:
    """HTML-escape text."""
    return html.escape(text)


def render_tool_card(tool: dict, cat_colors: dict) -> str:
    lines = ['      <div class="tool-card">']
    if star := tool.get("star"):
        lines.append(f'        <span class="tool-star {star}">★</span>')
    lines.append('        <div class="tool-header">')
    if url := tool.get("url"):
        lines.append(f'          <a class="tool-name" href="{h(url)}">{h(tool["name"])}</a>')
    else:
        lines.append(f'          <span class="tool-name">{h(tool["name"])}</span>')
    lines.append(f'          <span class="tool-type">{h(tool["type"])}</span>')
    lines.append('        </div>')
    lines.append(f'        <div class="tool-desc">{tool["desc"]}</div>')
    if hl := tool.get("highlight"):
        lines.append(f'        <div class="tool-highlight">{h(hl)}</div>')
    lines.append('      </div>')
    return "\n".join(lines)


def render_more_box(more: list, border_color: str, more_urls: dict | None = None) -> str:
    urls = more_urls or {}
    parts = []
    for t in more:
        if url := urls.get(t):
            parts.append(f'<a class="more-link" href="{h(url)}">{h(t)}</a>')
        else:
            parts.append(h(t))
    return f"""\
      <div class="more-box">
        <strong>And many more:</strong> {", ".join(parts)} …
      </div>"""


def render_infra_note(note: dict) -> str:
    # text contains intentional HTML (<strong> tags), pass through
    return f"""\
      <div class="infra-sub">
        <div class="infra-sub-label">{h(note["label"])}</div>
        <div class="infra-sub-desc">{note["text"].strip()}</div>
      </div>"""


def render_category_css(cat: dict) -> str:
    cid = cat["id"]
    c = cat["colors"]
    layout = cat.get("layout", {})
    cols = layout.get("tools_columns")

    lines = []
    lines.append(
        f"  .cat-{cid} {{ background: linear-gradient(135deg, {c['bg_gradient'][0]} 0%, {c['bg_gradient'][1]} 100%); "
        f"border: 1px solid {c['border']}; "
        f"grid-column: {layout.get('grid_column', '1')}; "
        f"grid-row: {layout.get('grid_row', 'auto')}; }}"
    )
    lines.append(
        f"  .cat-{cid}::before {{ background: linear-gradient(90deg, {c['accent'][0]}, {c['accent'][1]}); }}"
    )
    lines.append(f"  .cat-{cid} .cat-label {{ color: {c['label']}; }}")
    lines.append(
        f"  .cat-{cid} .tool-card {{ border-color: {c['border']}; background: {c['card_bg']}; }}"
    )
    lines.append(
        f"  .cat-{cid} .tool-card:hover {{ border-color: {c['accent'][1]}; background: {c['card_hover_bg']}; }}"
    )
    if cat.get("more"):
        lines.append(f"  .cat-{cid} .more-box {{ border-color: {c['border']}; }}")
    if cols:
        lines.append(
            f"  .cat-{cid} .tools-grid {{ grid-template-columns: repeat({cols}, 1fr); }}"
        )
    return "\n".join(lines)


def render_category(cat: dict) -> str:
    cid = cat["id"]
    c = cat["colors"]

    badge_html = ""
    if badge := cat.get("badge"):
        style_cls = f' {badge["style"]}' if badge.get("style") else ""
        badge_html = f'    <div class="bootcamp-badge{style_cls}">{h(badge["text"])}</div>\n'

    tools_html = "\n".join(render_tool_card(t, c) for t in cat["tools"])

    more_html = ""
    if more := cat.get("more"):
        more_html = render_more_box(more, c["border"], cat.get("more_urls"))

    infra_html = ""
    if note := cat.get("infra_note"):
        infra_html = render_infra_note(note)

    grid_items = [tools_html]
    if more_html:
        grid_items.append(more_html)
    if infra_html:
        grid_items.append(infra_html)
    grid_content = "\n".join(grid_items)

    return f"""\
  <div class="category cat-{cid}">
{badge_html}\
    <div class="cat-label">{h(cat["label"])}</div>
    <div class="cat-title">{h(cat["title"])}</div>
    <div class="cat-tagline">"{h(cat["tagline"])}"</div>
    <div class="cat-audience"><strong>Best for:</strong> {h(cat["audience"])}</div>
    <div class="tools-grid">
{grid_content}
    </div>
  </div>"""


def render_star_legend(legends: list) -> str:
    spans = []
    for legend in legends:
        if legend["style"] == "gold":
            star = '<span style="color:#fbbf24; font-size:16px; filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.4));">★</span>'
        else:
            star = '<span style="color:#6b6560; font-size:16px;">★</span>'
        spans.append(f"  <span>{star} {h(legend['label'])}</span>")
    return "\n".join(spans)


def build(data: dict) -> str:
    today = date.today().strftime("%-d %B %Y")

    category_css = "\n\n".join(render_category_css(cat) for cat in data["categories"])
    category_html = "\n\n".join(render_category(cat) for cat in data["categories"])
    star_legend = render_star_legend(data["star_legend"])
    # footer_note contains intentional HTML (<strong> tags), pass through
    footer_note = data["footer_note"].strip().replace("\n", "<br>\n  ")

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WXEF9TG8WK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-WXEF9TG8WK');
</script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h(data["title"])}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;600&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'DM Sans', sans-serif; background: #0f0f13; color: #e8e4df; min-height: 100vh; padding: 48px 40px; }}
  .header {{ text-align: center; margin-bottom: 48px; }}
  .header h1 {{ font-size: 32px; font-weight: 700; letter-spacing: -0.5px; color: #fff; margin-bottom: 8px; }}
  .header .subtitle {{ font-size: 15px; color: #8a8680; font-weight: 400; }}
  .landscape {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .category {{ border-radius: 16px; padding: 28px; position: relative; overflow: hidden; }}
  .category::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }}

{category_css}

  .infra-sub {{ margin-top: 4px; padding: 12px 14px; border-radius: 10px; background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.04); grid-column: 1 / -1; }}
  .infra-sub-label {{ font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #6b6560; margin-bottom: 6px; }}
  .infra-sub-desc {{ font-size: 12px; color: #7a7570; line-height: 1.55; }}
  .infra-sub-desc strong {{ color: #9a9590; font-weight: 600; }}

  .cat-label {{ font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }}
  .cat-title {{ font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 4px; }}
  .cat-tagline {{ font-size: 13px; color: #8a8680; font-style: italic; margin-bottom: 20px; }}
  .cat-audience {{ font-size: 12px; color: #6b6560; margin-bottom: 16px; padding: 8px 12px; background: rgba(0,0,0,0.2); border-radius: 8px; display: inline-block; }}
  .cat-audience strong {{ color: #a09890; font-weight: 500; }}
  .tools-grid {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
  .tool-card {{ border: 1px solid; border-radius: 10px; padding: 14px 16px; transition: all 0.2s ease; cursor: default; position: relative; }}
  .tool-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }}
  .tool-name {{ font-size: 15px; font-weight: 700; color: #fff; text-decoration: none; }}
  a.tool-name:hover {{ color: #fff; }}
  .more-link {{ color: inherit; text-decoration: none; }}
  .more-link:hover {{ color: inherit; }}
  .tool-type {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #6b6560; background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 4px; }}
  .tool-desc {{ font-size: 12.5px; color: #9a9590; line-height: 1.5; }}
  .tool-highlight {{ font-size: 11px; margin-top: 8px; padding: 6px 10px; border-radius: 6px; background: rgba(255,255,255,0.03); color: #7a7570; font-family: 'JetBrains Mono', monospace; }}
  .tool-star {{ position: absolute; top: 10px; right: 12px; font-size: 18px; line-height: 1; }}
  .tool-star.gray {{ color: #6b6560; }}
  .tool-star.gold {{ color: #fbbf24; filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.4)); }}
  .more-box {{ border: 1px dashed; border-radius: 10px; padding: 12px 16px; font-size: 12.5px; color: #6b6560; line-height: 1.5; text-align: center; grid-column: 1 / -1; }}
  .more-box strong {{ color: #8a8680; font-weight: 500; }}
  .bootcamp-badge {{ position: absolute; top: 12px; right: 12px; font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; padding: 4px 10px; border-radius: 6px; background: rgba(255,255,255,0.08); color: #b0a8a0; }}
  .bootcamp-badge.primary {{ background: rgba(139, 30, 30, 0.3); color: #f0a0a0; border: 1px solid rgba(139, 30, 30, 0.5); }}
  .footer-note {{ text-align: center; margin-top: 36px; font-size: 12px; color: #5a5550; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6; }}
  .star-legend {{ display: flex; justify-content: center; gap: 24px; margin-top: 14px; font-size: 12px; color: #6b6560; }}
  .star-legend span {{ display: flex; align-items: center; gap: 5px; }}
</style>
</head>
<body>

<div class="header">
  <h1>{h(data["title"])}</h1>
  <div class="subtitle">{h(data["subtitle"])} · updated {today} · <a href="https://v9n.us/" style="color:#8a8680; text-decoration:none;">Patrick van Staveren</a></div>
</div>

<div class="landscape">

{category_html}

</div>

<div class="footer-note">
  {footer_note}
</div>
<div class="star-legend">
{star_legend}
</div>
<div style="text-align:center; margin-top:24px; font-size:11px; color:#3a3530;">© 2026 <a href="https://v9n.us/" style="color:#5a5550; text-decoration:none; border-bottom:1px solid #3a3530;">V9N Consulting</a></div>

</body>
</html>
"""


def main():
    script_dir = Path(__file__).parent
    yaml_path = script_dir / "ai_tools_landscape.yaml"
    html_path = script_dir / "ai_tools_landscape.html"

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    output = build(data)
    html_path.write_text(output)
    print(f"Built {html_path} ({len(output)} bytes)")


if __name__ == "__main__":
    main()
