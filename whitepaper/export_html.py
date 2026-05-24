#!/usr/bin/env python3
"""
export_html.py  --  Convert RIMT Markdown documents to print-ready HTML files.

Usage:
    python export_html.py

Outputs:
    github-repo/whitepaper/RIMT-whitepaper.html
    github-repo/comparison/RIMT-vs-conventional-comparison.html
    github-repo/comparison/RIMT-infographic-data.html

Each generated .html is print-ready: open in Chrome, Ctrl+P, Save as PDF.

Requirements:
    pip install markdown
"""

import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Install the markdown library first:  pip install markdown")

# ---------------------------------------------------------------------------
# Paths and document list
# ---------------------------------------------------------------------------
# This script lives at <repo>/github-repo/whitepaper/export_html.py
# parents[0] = whitepaper, parents[1] = github-repo, parents[2] = repo root
REPO_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS = [
    {
        "md": REPO_ROOT / "github-repo" / "whitepaper" / "RIMT-whitepaper.md",
        "html": REPO_ROOT / "github-repo" / "whitepaper" / "RIMT-whitepaper.html",
        "title": "Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer (RIMT)",
    },
    {
        "md": REPO_ROOT / "github-repo" / "comparison" / "RIMT-vs-conventional-comparison.md",
        "html": REPO_ROOT / "github-repo" / "comparison" / "RIMT-vs-conventional-comparison.html",
        "title": "RIMT vs. Conventional Marine Propulsion -- Comparative Analysis",
    },
    {
        "md": REPO_ROOT / "github-repo" / "comparison" / "RIMT-infographic-data.md",
        "html": REPO_ROOT / "github-repo" / "comparison" / "RIMT-infographic-data.html",
        "title": "RIMT Infographic Data Package",
    },
]


# ---------------------------------------------------------------------------
# Conversion pipeline
# ---------------------------------------------------------------------------
def convert(md_path: Path, html_path: Path, title: str) -> None:
    """Render one Markdown file to a print-ready, MathJax-enabled HTML file."""
    if not md_path.exists():
        print(f"SKIP (not found): {md_path}")
        return

    md_text = md_path.read_text(encoding="utf-8")

    # Pre-process: escape currency dollar signs BEFORE math stashing, so the
    # math-pair regex below cannot accidentally treat "$30B ... $50k" as math.
    # Match $ immediately followed by a digit, then any digits / commas / dots
    # / SI-suffix letters / trailing '+'. LaTeX math also CAN start with a
    # digit (e.g. $2(w+g)$, $1.08 \times 10^{-3}$, $10^2$, $20$), so the
    # trailing negative lookahead `(?!\s*[\\(^_${])` excludes those by checking
    # that the character immediately after the captured number is NOT a
    # math-token continuation: backslash (LaTeX cmd), open-paren, caret
    # (superscript), underscore (subscript), $ (closing math delim), or {
    # (LaTeX grouping). Possessive quantifiers `*+` are mandatory: without
    # them the greedy `[\d,.]*` backtracks when the lookahead fails, eating
    # one digit at a time until the match succeeds, which still corrupts the
    # math expression by stripping the opening $. Requires Python 3.11+.
    md_text = re.sub(
        r'\$(?=\d)(\d[\d,.]*+[a-zA-Z]*+\+?)(?!\s*[\\(^_${])',
        r'&#36;\1',
        md_text,
    )

    # Pre-process: protect LaTeX math from the Markdown parser by stashing
    # $...$ and $$...$$ spans behind placeholders.
    math_blocks: list[str] = []

    def stash_math(m):
        idx = len(math_blocks)
        math_blocks.append(m.group(0))
        return f"MATHPLACEHOLDER{idx}ENDMATH"

    protected = re.sub(r'\$\$.+?\$\$', stash_math, md_text, flags=re.DOTALL)
    protected = re.sub(r'\$.+?\$',     stash_math, protected, flags=re.DOTALL)

    # 'nl2br' is intentionally excluded -- it breaks the 'tables' extension when
    # tables appear back-to-back (the comparison document has 16 of them).
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    body_html = md.convert(protected)

    for idx, math in enumerate(math_blocks):
        body_html = body_html.replace(f"MATHPLACEHOLDER{idx}ENDMATH", math)

    html_out = HTML_TEMPLATE.format(title=title, body=body_html)
    html_path.write_text(html_out, encoding="utf-8")
    print(f"Written: {html_path}")


# ---------------------------------------------------------------------------
# HTML template (shared across all documents)
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>

  <!-- MathJax -- renders LaTeX math in the browser -->
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath:  [['$', '$']],
        displayMath: [['$$', '$$']],
        processEscapes: true
      }},
      options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre'] }}
    }};
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>

  <style>
    /* ---- Page layout ---- */
    /* Page numbering uses CSS Paged Media @bottom-center.  In Chrome's
       print dialog, enable "Headers and footers" so margin boxes render;
       the empty top/bottom boxes below override Chrome's default URL/title
       headers, leaving only the centered page counter. */
    @page {{
      size: A4;
      margin: 25mm 20mm 25mm 20mm;
      @top-left     {{ content: ""; }}
      @top-center   {{ content: ""; }}
      @top-right    {{ content: ""; }}
      @bottom-left  {{ content: ""; }}
      @bottom-right {{ content: ""; }}
      @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: "Times New Roman", Times, serif;
        font-size: 9pt;
        color: #666;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: "Times New Roman", Times, serif;
      font-size: 11pt;
      line-height: 1.6;
      color: #111;
      max-width: 170mm;
      margin: 0 auto;
      padding: 10mm 0;
    }}

    /* ---- Title block ---- */
    h1 {{
      font-size: 16pt;
      font-weight: bold;
      text-align: center;
      margin-bottom: 4pt;
    }}
    /* Metadata block directly under the H1 title (author/date/version/...).
       Left-aligned, slightly smaller than body, line-height tight so that
       the stacked <br>-separated lines read as a compact author block. */
    h1 + p {{
      text-align: left;
      font-size: 10pt;
      color: #333;
      line-height: 1.4;
      margin-top: 8pt;
      margin-bottom: 12pt;
    }}

    /* ---- Section headings ---- */
    h2 {{
      font-size: 13pt;
      font-weight: bold;
      border-bottom: 1px solid #aaa;
      padding-bottom: 2pt;
      margin-top: 18pt;
      page-break-after: avoid;
    }}
    h3 {{
      font-size: 11pt;
      font-weight: bold;
      margin-top: 12pt;
      page-break-after: avoid;
    }}

    /* ---- Abstract ---- */
    h2#abstract + p,
    h2:first-of-type + p {{
      margin: 8pt 12mm;
      font-size: 10pt;
    }}

    /* ---- Keywords ---- */
    p strong:first-child {{
      font-weight: bold;
    }}

    /* ---- Tables ---- */
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5pt;
      margin: 10pt 0;
      page-break-inside: avoid;
    }}
    th {{
      background: #e8e8e8;
      border: 1px solid #999;
      padding: 4pt 6pt;
      text-align: left;
      font-weight: bold;
    }}
    td {{
      border: 1px solid #bbb;
      padding: 3pt 6pt;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{
      background: #f7f7f7;
    }}

    /* ---- Code / equations ---- */
    pre, code {{
      font-family: "Courier New", Courier, monospace;
      font-size: 9pt;
      background: #f4f4f4;
      padding: 2pt 4pt;
      border-radius: 2px;
    }}
    pre {{
      padding: 8pt;
      overflow-x: auto;
      page-break-inside: avoid;
    }}

    /* ---- Horizontal rules ---- */
    hr {{
      border: none;
      border-top: 1px solid #ccc;
      margin: 12pt 0;
    }}

    /* ---- Blockquotes ---- */
    blockquote {{
      border-left: 3px solid #aaa;
      margin: 8pt 0 8pt 12pt;
      padding: 4pt 8pt;
      color: #444;
      font-style: italic;
    }}

    /* ---- Print overrides ---- */
    @media print {{
      body {{ padding: 0; }}
      h2, h3 {{ page-break-after: avoid; }}
      p, li {{ orphans: 3; widows: 3; }}
      table {{ page-break-inside: avoid; }}
      a {{ color: #111; text-decoration: none; }}
    }}
  </style>
</head>
<body>

{body}

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Drive the loop
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for doc in DOCUMENTS:
        convert(doc["md"], doc["html"], doc["title"])

    print()
    print("Next steps for each generated HTML file:")
    print("  1. Open the .html file in Google Chrome")
    print("  2. Press Ctrl+P  (or Cmd+P on Mac)")
    print("  3. Destination -> Save as PDF")
    print("  4. Paper size: A4,  Margins: Default")
    print("  5. Tick 'Background graphics' (table shading + borders)")
    print("  6. Tick 'Headers and footers' -- the CSS @page rule then")
    print("     replaces Chrome's URL/title defaults with just a centered")
    print("     'Page N of M' counter at the bottom")
    print("  7. Save the .pdf alongside the .html in the same folder")
