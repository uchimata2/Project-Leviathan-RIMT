#!/usr/bin/env python3
"""
build_infographic.py -- Build the interactive RIMT infographic HTML.

Reads the canonical fenced ```json block from RIMT-infographic-data.md and
renders a self-contained interactive HTML page. The page uses CDN-loaded
ECharts (charts), GSAP (hero animation), and AOS (scroll reveals). CSS and
inlined data are embedded; only the JS libraries come from CDN.

Usage:
    python build_infographic.py

Input:
    github-repo/comparison/RIMT-infographic-data.md      (fenced ```json block)

Output:
    github-repo/comparison/RIMT-infographic.html

Data invariants:
    Every numeric claim in the JSON block carries a `source` field. The
    project-rimt-data-sync-registry memory enumerates the cross-document
    consistency rules (WP, comparison, infographic). When any source value
    changes, update the JSON block here and re-run this script.
"""

import json
import re
import sys
from pathlib import Path

# parents[2] = repo root from github-repo/comparison/
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_MD = REPO_ROOT / "github-repo" / "comparison" / "RIMT-infographic-data.md"
OUT_HTML = REPO_ROOT / "github-repo" / "comparison" / "RIMT-infographic.html"

REQUIRED_KEYS = [
    "doc_meta", "hero_numbers", "before_after", "where_it_shines",
    "build_path", "caveat", "figures", "links",
]
REQUIRED_FIGURES = [
    "energy_chain", "scorecard_radar", "application_quadrant",
    "co2_sensitivity", "trl_pathway", "acoustic_spectrum",
]


def extract_json_block(md_text: str) -> dict:
    """Find the canonical ```json fenced block in the MD source."""
    match = re.search(r"```json\s*\n(.*?)\n```", md_text, flags=re.DOTALL)
    if not match:
        sys.exit(f"ERROR: no ```json fenced block found in {SRC_MD}")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: JSON parse failed in {SRC_MD}: {exc}")


def validate(data: dict) -> None:
    """Cheap structural sanity check. Fails loud on missing required keys."""
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        sys.exit(f"ERROR: top-level keys missing: {missing}")
    missing_figs = [f for f in REQUIRED_FIGURES if f not in data["figures"]]
    if missing_figs:
        sys.exit(f"ERROR: figures missing: {missing_figs}")
    if not data["hero_numbers"]:
        sys.exit("ERROR: hero_numbers is empty")


def main() -> None:
    if not SRC_MD.exists():
        sys.exit(f"Source MD not found: {SRC_MD}")
    md_text = SRC_MD.read_text(encoding="utf-8")
    data = extract_json_block(md_text)
    validate(data)

    payload = json.dumps(data, ensure_ascii=False, indent=2)
    # Single embed point. The placeholder is a JS-safe token that won't collide
    # with any user content (no `__` patterns in any input field by construction).
    html_out = HTML_TEMPLATE.replace("__INFOGRAPHIC_DATA_JSON__", payload)
    OUT_HTML.write_text(html_out, encoding="utf-8")

    print(f"Written: {OUT_HTML}")
    print(f"  Hero numbers     : {len(data['hero_numbers'])}")
    print(f"  Before/after rows: {len(data['before_after'])}")
    print(f"  Application cards: {len(data['where_it_shines'])}")
    print(f"  Build-path steps : {len(data['build_path'])}")
    print(f"  Figures embedded : {len(data['figures'])}")


# ---------------------------------------------------------------------------
# HTML template. Triple-quoted; no Python f-string substitution (the page
# uses plenty of literal {} in CSS and JS). Single replacement point:
# __INFOGRAPHIC_DATA_JSON__ becomes the JSON literal.
# ---------------------------------------------------------------------------
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RIMT - A Silent Solid-State Marine Engine</title>
<meta name="description" content="An interactive infographic for Resonant Ionic Momentum Transfer (RIMT) - a proposed solid-state marine propulsion concept. CC BY-SA 4.0.">

<!-- CDN-loaded JS libraries (charts + animation + scroll reveals) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Source+Serif+4:wght@400;600&display=swap">

<style>
:root {
  --bg-deep: #0a1929;
  --bg-mid: #102841;
  --bg-card: rgba(255, 255, 255, 0.04);
  --bg-card-hi: rgba(255, 255, 255, 0.07);
  --teal: #4dd0e1;
  --teal-soft: rgba(77, 208, 225, 0.18);
  --teal-glow: rgba(77, 208, 225, 0.45);
  --grey-conv: #b0bec5;
  --amber: #ffb74d;
  --amber-soft: rgba(255, 183, 77, 0.15);
  --red: #ef5350;
  --red-soft: rgba(239, 83, 80, 0.15);
  --white: #ffffff;
  --muted: rgba(255, 255, 255, 0.65);
  --hairline: rgba(255, 255, 255, 0.12);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg-deep);
  color: var(--white);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  line-height: 1.6;
  overflow-x: hidden;
}

a { color: var(--teal); text-decoration: none; transition: color 0.2s; }
a:hover { color: var(--amber); }

section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 90px 24px;
}

h1, h2, h3 { font-weight: 700; letter-spacing: -0.01em; line-height: 1.2; }
h2 { font-size: clamp(1.8rem, 3.5vw, 2.6rem); margin-bottom: 1.5rem; }
h3 { font-size: 1.2rem; margin-bottom: 0.5rem; font-weight: 600; color: var(--teal); }
.section-lead { color: var(--muted); font-size: 1.05rem; max-width: 780px; margin-bottom: 32px; }

/* ============ Hero ============ */
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(77, 208, 225, 0.12), transparent 60%),
    radial-gradient(ellipse at 80% 70%, rgba(255, 183, 77, 0.08), transparent 50%),
    var(--bg-deep);
  position: relative;
  overflow: hidden;
  padding: 40px 24px 120px;
  max-width: none;
}
.hero h1 {
  font-size: clamp(2rem, 5.5vw, 4rem);
  margin-bottom: 1.4rem;
  background: linear-gradient(135deg, var(--teal) 0%, var(--amber) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  max-width: 1000px;
  padding: 0 16px;
}
.hero .subtitle {
  color: var(--muted);
  font-size: clamp(1rem, 1.7vw, 1.25rem);
  max-width: 720px;
  padding: 0 16px;
}
.hero .badge-row {
  margin-top: 28px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}
.badge {
  background: var(--bg-card);
  border: 1px solid var(--hairline);
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 0.85rem;
  color: var(--muted);
}
.badge.trl { color: var(--amber); border-color: rgba(255, 183, 77, 0.4); }
.badge.licence { color: var(--teal); border-color: rgba(77, 208, 225, 0.4); }

.scroll-cue {
  position: absolute;
  bottom: 36px;
  left: 50%;
  transform: translateX(-50%);
  color: var(--muted);
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  animation: cue 2.4s ease-in-out infinite;
}
.scroll-cue::after { content: " v"; }
@keyframes cue {
  0%, 100% { transform: translate(-50%, 0); opacity: 0.6; }
  50%      { transform: translate(-50%, 8px); opacity: 1; }
}

/* Animated wave at bottom of hero */
.hero-wave {
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 80px;
  opacity: 0.6;
}

/* ============ Hero number tiles ============ */
.hero-numbers {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 18px;
}
.hero-tile {
  background: var(--bg-card);
  border: 1px solid var(--hairline);
  border-radius: 14px;
  padding: 30px 18px 50px;
  text-align: center;
  transition: transform 0.3s, border-color 0.3s, background 0.3s;
  position: relative;
  overflow: hidden;
}
.hero-tile::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--teal), var(--amber));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}
.hero-tile:hover {
  transform: translateY(-6px);
  border-color: var(--teal);
  background: var(--bg-card-hi);
}
.hero-tile:hover::before { transform: scaleX(1); }
.hero-tile .value-row { white-space: nowrap; }
.hero-tile .value {
  font-size: clamp(2.4rem, 4.5vw, 3.2rem);
  font-weight: 800;
  color: var(--amber);
  line-height: 1;
  display: inline-block;
}
.hero-tile .unit {
  font-size: 1.2rem;
  color: var(--amber);
  font-weight: 600;
  opacity: 0.9;
}
.hero-tile .label {
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 12px;
  line-height: 1.35;
}
.hero-tile .source {
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.32);
  padding: 0 12px;
  font-style: italic;
}

/* ============ Before/After ============ */
.ba-grid { display: flex; flex-direction: column; gap: 16px; }
.ba-row {
  display: grid;
  grid-template-columns: 1fr 140px 1fr;
  gap: 16px;
  align-items: stretch;
}
.ba-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 18px 22px;
  display: flex;
  align-items: center;
  transition: transform 0.25s, background 0.25s;
}
.ba-card:hover { transform: translateY(-3px); background: var(--bg-card-hi); }
.ba-card.conventional {
  border-left: 4px solid var(--grey-conv);
  color: var(--grey-conv);
}
.ba-card.rimt {
  border-left: 4px solid var(--teal);
  color: var(--white);
  background: linear-gradient(135deg, var(--teal-soft), var(--bg-card));
}
.ba-aspect {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: 700;
  color: var(--amber);
  font-size: 0.95rem;
  background: var(--amber-soft);
  border-radius: 999px;
  padding: 12px 8px;
}

/* ============ Where it shines (app cards) ============ */
.app-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}
.app-card {
  background: linear-gradient(135deg, var(--bg-mid), var(--bg-card));
  border: 1px solid var(--hairline);
  border-radius: 14px;
  padding: 26px 22px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.app-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, var(--teal-soft), transparent 60%);
  opacity: 0;
  transition: opacity 0.4s;
  pointer-events: none;
}
.app-card:hover {
  transform: translateY(-6px) scale(1.02);
  border-color: var(--teal);
  box-shadow: 0 20px 50px rgba(77, 208, 225, 0.18);
}
.app-card:hover::after { opacity: 1; }
.app-card .summary { color: var(--muted); font-size: 0.95rem; margin-top: 8px; }
.app-card .more {
  color: var(--amber);
  font-size: 0.85rem;
  margin-top: 14px;
  display: inline-block;
  font-weight: 600;
}

/* ============ Chart blocks ============ */
.charts-intro { margin-bottom: 30px; }
.chart-container {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 28px 24px;
  margin-bottom: 28px;
  border: 1px solid var(--hairline);
}
.chart-container .source-tag {
  display: inline-block;
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.35);
  margin-top: 10px;
  font-style: italic;
}
.chart-canvas { width: 100%; height: 420px; }
.chart-canvas.tall { height: 520px; }
.chart-caption { color: var(--muted); font-size: 0.92rem; margin: 6px 0 18px; }

/* ============ Staircase (build path) ============ */
.staircase {
  display: flex;
  align-items: flex-end;
  gap: 6px;
  height: 340px;
  margin-top: 24px;
  padding: 0 4px;
}
.step {
  flex: 1;
  background: linear-gradient(180deg, var(--teal) 0%, var(--bg-mid) 100%);
  border-radius: 8px 8px 0 0;
  padding: 14px 10px;
  color: var(--white);
  font-size: 0.82rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  position: relative;
  transition: transform 0.25s, filter 0.25s;
  cursor: default;
  min-height: 60px;
}
.step:hover {
  transform: translateY(-6px);
  filter: brightness(1.15) saturate(1.2);
}
.step .year {
  font-weight: 800;
  font-size: 1.05rem;
  color: var(--amber);
  margin-bottom: 6px;
}
.step .label { line-height: 1.3; margin-bottom: 6px; }
.step .spend { font-size: 0.85rem; color: var(--white); font-weight: 600; opacity: 0.9; }
.staircase-axis {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  color: var(--muted);
  font-size: 0.78rem;
  padding: 0 4px;
}

/* ============ Caveat ============ */
.caveat {
  background: var(--red-soft);
  border-left: 4px solid var(--red);
  padding: 22px 26px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.88);
  font-size: 0.95rem;
  line-height: 1.7;
}

/* ============ Footer ============ */
footer {
  text-align: center;
  padding: 50px 24px;
  color: var(--muted);
  font-size: 0.88rem;
  border-top: 1px solid var(--hairline);
  margin-top: 80px;
}
footer p { margin: 6px 0; }
footer .links { margin-top: 14px; }
footer .links a { margin: 0 8px; }

/* ============ Modal ============ */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(10, 25, 41, 0.92);
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 24px;
  backdrop-filter: blur(6px);
}
.modal.active { display: flex; animation: modal-fade 0.25s ease; }
@keyframes modal-fade { from { opacity: 0; } to { opacity: 1; } }
.modal-content {
  background: var(--bg-mid);
  border: 1px solid var(--teal);
  border-radius: 18px;
  padding: 36px 32px;
  max-width: 620px;
  width: 100%;
  position: relative;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6);
}
.modal-close {
  position: absolute;
  top: 14px;
  right: 18px;
  background: none;
  border: none;
  color: var(--muted);
  font-size: 1.6rem;
  cursor: pointer;
  line-height: 1;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  transition: all 0.2s;
}
.modal-close:hover { background: var(--bg-card); color: var(--white); }
.modal-title { color: var(--teal); margin-bottom: 12px; font-size: 1.4rem; }
.modal-detail { color: var(--white); line-height: 1.7; }
.modal-source {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid var(--hairline);
  font-size: 0.78rem;
  color: var(--muted);
  font-style: italic;
}

/* ============ Mobile ============ */
@media (max-width: 720px) {
  section { padding: 60px 16px; }
  .ba-row { grid-template-columns: 1fr; }
  .ba-aspect { padding: 8px; font-size: 0.9rem; }
  .staircase { height: 260px; }
  .step { font-size: 0.72rem; }
}

/* ============ Print ============ */
@media print {
  body { background: white; color: black; }
  .hero { min-height: auto; padding: 40px 16px; }
  .modal { display: none !important; }
  .chart-canvas { height: 340px; }
}
</style>
</head>
<body>

<!-- ====================== HERO ====================== -->
<section class="hero">
  <h1 id="hero-headline"></h1>
  <p class="subtitle" id="hero-subtitle"></p>
  <div class="badge-row">
    <span class="badge trl">TRL 2 - first-order analytical concept</span>
    <span class="badge licence" id="hero-licence-badge"></span>
    <span class="badge">Project Leviathan</span>
  </div>
  <div class="scroll-cue">Explore</div>
  <svg class="hero-wave" viewBox="0 0 1440 80" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <path fill="#4dd0e1" fill-opacity="0.22" d="M0,32 C240,80 480,0 720,40 C960,80 1200,8 1440,40 L1440,80 L0,80 Z">
      <animate attributeName="d" dur="9s" repeatCount="indefinite"
        values="M0,32 C240,80 480,0 720,40 C960,80 1200,8 1440,40 L1440,80 L0,80 Z;
                M0,40 C240,8 480,72 720,40 C960,8 1200,72 1440,40 L1440,80 L0,80 Z;
                M0,32 C240,80 480,0 720,40 C960,80 1200,8 1440,40 L1440,80 L0,80 Z" />
    </path>
    <path fill="#4dd0e1" fill-opacity="0.12" d="M0,40 C320,72 640,8 960,40 C1200,64 1320,16 1440,40 L1440,80 L0,80 Z">
      <animate attributeName="d" dur="12s" repeatCount="indefinite"
        values="M0,40 C320,72 640,8 960,40 C1200,64 1320,16 1440,40 L1440,80 L0,80 Z;
                M0,48 C320,16 640,72 960,40 C1200,16 1320,64 1440,40 L1440,80 L0,80 Z;
                M0,40 C320,72 640,8 960,40 C1200,64 1320,16 1440,40 L1440,80 L0,80 Z" />
    </path>
  </svg>
</section>

<!-- ====================== HERO NUMBERS ====================== -->
<section>
  <h2 data-aos="fade-up">The numbers that matter</h2>
  <p class="section-lead" data-aos="fade-up">Five facts that bound the design space - the modelled performance ceiling on one side, the regulatory and economic pressures on the conventional incumbent on the other.</p>
  <div class="hero-numbers" id="hero-numbers"></div>
</section>

<!-- ====================== BEFORE / AFTER ====================== -->
<section>
  <h2 data-aos="fade-up">Conventional today vs. RIMT if validated</h2>
  <p class="section-lead" data-aos="fade-up">The differences are categorical rather than incremental - RIMT doesn't propose a better engine, it proposes a different mechanism.</p>
  <div class="ba-grid" id="before-after"></div>
</section>

<!-- ====================== WHERE IT SHINES ====================== -->
<section>
  <h2 data-aos="fade-up">Where this shines</h2>
  <p class="section-lead" data-aos="fade-up">Five application classes where RIMT's profile fits naturally. Click any card for the deeper story.</p>
  <div class="app-grid" id="app-grid"></div>
</section>

<!-- ====================== APPLICATION QUADRANT ====================== -->
<section>
  <h2 data-aos="fade-up">Where to start</h2>
  <p class="section-lead" data-aos="fade-up">Each dot is one application from the comparison document, plotted by the value RIMT brings (x) and the customer's risk tolerance for an unvalidated technology (y). The amber zone is the "natural early adopters" sweet-spot.</p>
  <div class="chart-container" data-aos="fade-up">
    <h3 id="quadrant-title"></h3>
    <p class="chart-caption" id="quadrant-caption"></p>
    <div id="quadrant" class="chart-canvas tall"></div>
    <span class="source-tag" id="quadrant-source"></span>
  </div>
</section>

<!-- ====================== ENERGY CHAIN ====================== -->
<section>
  <h2 data-aos="fade-up">Where the energy goes</h2>
  <p class="section-lead" data-aos="fade-up">Track one unit of primary energy through each propulsion stack. The conventional stack drops to ~33% by the time it reaches the water; the RIMT stack is modelled at 83%.</p>
  <div class="chart-container" data-aos="fade-up">
    <h3 id="energy-title"></h3>
    <p class="chart-caption" id="energy-caption"></p>
    <div id="energy" class="chart-canvas tall"></div>
    <span class="source-tag" id="energy-source"></span>
  </div>
</section>

<!-- ====================== SCORECARD RADAR ====================== -->
<section>
  <h2 data-aos="fade-up">The 20-axis scorecard</h2>
  <p class="section-lead" data-aos="fade-up">Qualitative scoring across 20 categories. RIMT's modelled profile is strongest exactly where conventional propulsion is most pressured (environment, regulation, maintenance, safety); RIMT's weakest cells are exactly where conventional is strongest (TRL, supply chain, installed base).</p>
  <div class="chart-container" data-aos="fade-up">
    <h3 id="radar-title"></h3>
    <p class="chart-caption" id="radar-caption"></p>
    <div id="radar" class="chart-canvas tall"></div>
    <span class="source-tag" id="radar-source"></span>
  </div>
</section>

<!-- ====================== CO2 SENSITIVITY ====================== -->
<section>
  <h2 data-aos="fade-up">Decarbonisation upside</h2>
  <p class="section-lead" data-aos="fade-up">An illustrative sensitivity analysis: what does shipping CO2 look like if RIMT (paired with renewable grid electricity) gradually displaces a share of the world fleet between now and 2050?</p>
  <div class="chart-container" data-aos="fade-up">
    <h3 id="co2-title"></h3>
    <p class="chart-caption" id="co2-caption"></p>
    <div id="co2" class="chart-canvas"></div>
    <span class="source-tag" id="co2-source"></span>
  </div>
</section>

<!-- ====================== ACOUSTIC SPECTRUM ====================== -->
<section>
  <h2 data-aos="fade-up">The acoustic story</h2>
  <p class="section-lead" data-aos="fade-up">A container ship is roughly 180 dB at low frequency, dominated by propeller cavitation. RIMT removes propeller cavitation by construction; what is left is the hull-flow noise of the displacement hull itself. Whale-vocalisation bands shown for context.</p>
  <div class="chart-container" data-aos="fade-up">
    <h3 id="acoustic-title"></h3>
    <p class="chart-caption" id="acoustic-caption"></p>
    <div id="acoustic" class="chart-canvas"></div>
    <span class="source-tag" id="acoustic-source"></span>
  </div>
</section>

<!-- ====================== BUILD PATH STAIRCASE ====================== -->
<section>
  <h2 data-aos="fade-up">The build path</h2>
  <p class="section-lead" data-aos="fade-up">From a hobbyist benchtop to a class-society pilot. Bar heights are log-scaled spend; hover for the milestone scale.</p>
  <div class="chart-container" data-aos="fade-up">
    <div class="staircase" id="staircase"></div>
    <div class="staircase-axis" id="staircase-axis"></div>
    <p class="chart-caption" style="margin-top: 18px;">Order-of-magnitude planning estimates only. Each milestone embeds a research work-package listed in WP &sect;6.</p>
  </div>
</section>

<!-- ====================== CAVEAT ====================== -->
<section>
  <h2 data-aos="fade-up">The honest caveat</h2>
  <div class="caveat" id="caveat" data-aos="fade-up"></div>
</section>

<!-- ====================== FOOTER ====================== -->
<footer>
  <p><strong>RIMT - Resonant Ionic Momentum Transfer</strong> &middot; Project Leviathan</p>
  <p>Released by <span id="footer-author"></span> under <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">CC BY-SA 4.0</a></p>
  <p class="links">
    <a id="link-doi" href="" target="_blank">DOI (Zenodo)</a> &middot;
    <a id="link-github" href="" target="_blank">GitHub</a> &middot;
    <a id="link-whitepaper" href="">Whitepaper</a> &middot;
    <a id="link-comparison" href="">Detailed comparison</a> &middot;
    <a id="link-simulation" href="">Simulation</a>
  </p>
</footer>

<!-- ====================== MODAL ====================== -->
<div class="modal" id="modal" role="dialog" aria-modal="true">
  <div class="modal-content">
    <button class="modal-close" onclick="closeModal()" aria-label="Close">&times;</button>
    <h3 class="modal-title" id="modal-title"></h3>
    <p class="modal-detail" id="modal-detail"></p>
    <p class="modal-source" id="modal-source"></p>
  </div>
</div>

<!-- ====================== SCRIPTS ====================== -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>

<script>
"use strict";

// Canonical data injected at build time by build_infographic.py
const DATA = __INFOGRAPHIC_DATA_JSON__;

// ==================== Section: Hero ====================
document.getElementById("hero-headline").textContent = DATA.doc_meta.headline;
document.getElementById("hero-subtitle").textContent = DATA.doc_meta.subtitle;
document.getElementById("hero-licence-badge").textContent = DATA.doc_meta.license;
document.getElementById("footer-author").textContent = DATA.doc_meta.author;
document.getElementById("link-doi").href = DATA.links.doi;
document.getElementById("link-github").href = DATA.links.github;
document.getElementById("link-whitepaper").href = DATA.links.whitepaper;
document.getElementById("link-comparison").href = DATA.links.comparison;
document.getElementById("link-simulation").href = DATA.links.simulation;

// Hero entrance animation (GSAP)
gsap.from("#hero-headline", { y: 60, opacity: 0, duration: 1.2, ease: "power3.out" });
gsap.from("#hero-subtitle", { y: 30, opacity: 0, duration: 1.0, delay: 0.35, ease: "power3.out" });
gsap.from(".badge-row .badge", { y: 20, opacity: 0, duration: 0.8, delay: 0.8, stagger: 0.12, ease: "power2.out" });
gsap.from(".scroll-cue", { opacity: 0, duration: 1.5, delay: 1.4 });

// ==================== Section: Hero numbers ====================
const heroContainer = document.getElementById("hero-numbers");
DATA.hero_numbers.forEach((h, i) => {
  const tile = document.createElement("div");
  tile.className = "hero-tile";
  tile.setAttribute("data-aos", "zoom-in");
  tile.setAttribute("data-aos-delay", String(i * 90));

  const prefix = h.unit_prefix || "";
  const suffix = h.unit_suffix || "";
  const valueSpan = h.display_override
    ? `<span class="value">${h.display_override}</span>`
    : `<span class="value" data-target="${h.value}" data-from="${h.counter_from || 0}">${h.counter_from || 0}</span>`;

  tile.innerHTML = `
    <div class="value-row">${prefix ? `<span class="unit">${prefix}</span>` : ""}${valueSpan}${suffix ? `<span class="unit">${suffix}</span>` : ""}</div>
    <div class="label">${h.label}</div>
    <div class="source">${h.source}</div>
  `;
  heroContainer.appendChild(tile);
});

// Counter animation triggered on viewport entry
function animateCounter(el) {
  const target = parseFloat(el.dataset.target);
  const from = parseFloat(el.dataset.from || "0");
  const duration = 1600;
  const isFloat = !Number.isInteger(target);
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    const val = from + (target - from) * eased;
    el.textContent = isFloat ? val.toFixed(1) : Math.round(val);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.dataset.counted) {
      entry.target.dataset.counted = "1";
      animateCounter(entry.target);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll(".hero-tile .value[data-target]").forEach(el => counterObserver.observe(el));

// ==================== Section: Before / After ====================
const baContainer = document.getElementById("before-after");
DATA.before_after.forEach((row, i) => {
  const div = document.createElement("div");
  div.className = "ba-row";
  div.setAttribute("data-aos", "fade-up");
  div.setAttribute("data-aos-delay", String(i * 80));
  div.innerHTML = `
    <div class="ba-card conventional">${row.conventional}</div>
    <div class="ba-aspect">${row.aspect}</div>
    <div class="ba-card rimt">${row.rimt}</div>
  `;
  baContainer.appendChild(div);
});

// ==================== Section: Where it shines (clickable cards) ====================
const appContainer = document.getElementById("app-grid");
DATA.where_it_shines.forEach((app, i) => {
  const card = document.createElement("div");
  card.className = "app-card";
  card.setAttribute("data-aos", "zoom-in");
  card.setAttribute("data-aos-delay", String(i * 70));
  card.setAttribute("role", "button");
  card.setAttribute("tabindex", "0");
  card.innerHTML = `
    <h3>${app.title}</h3>
    <p class="summary">${app.summary}</p>
    <span class="more">Read more &rarr;</span>
  `;
  card.addEventListener("click", () => openModal(app.title, app.detail, app.source));
  card.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openModal(app.title, app.detail, app.source);
    }
  });
  appContainer.appendChild(card);
});

// ==================== Modal ====================
function openModal(title, detail, source) {
  document.getElementById("modal-title").textContent = title;
  document.getElementById("modal-detail").textContent = detail;
  document.getElementById("modal-source").textContent = source ? "Source: " + source : "";
  document.getElementById("modal").classList.add("active");
}
function closeModal() {
  document.getElementById("modal").classList.remove("active");
}
document.getElementById("modal").addEventListener("click", e => {
  if (e.target.id === "modal") closeModal();
});
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
});

// ==================== Section: Build-path staircase ====================
const stairContainer = document.getElementById("staircase");
const stairAxis = document.getElementById("staircase-axis");
const spends = DATA.build_path.map(b => b.spend_usd_m);
const minLog = Math.log10(Math.min(...spends));
const maxLog = Math.log10(Math.max(...spends));
const logRange = maxLog - minLog || 1;

DATA.build_path.forEach((step, i) => {
  const div = document.createElement("div");
  div.className = "step";
  div.setAttribute("data-aos", "fade-up");
  div.setAttribute("data-aos-delay", String(i * 90));
  const norm = (Math.log10(step.spend_usd_m) - minLog) / logRange;
  const heightPct = Math.max(norm * 100, 18);
  div.style.height = `${heightPct}%`;
  const spendStr = step.spend_usd_m < 1
    ? `$${step.spend_usd_m * 1000} k`
    : `$${step.spend_usd_m} M`;
  div.innerHTML = `
    <div class="year">Year ${step.year}</div>
    <div class="label">${step.milestone}</div>
    <div class="spend">${spendStr} cum.</div>
  `;
  div.title = step.scale;
  stairContainer.appendChild(div);

  const axisCell = document.createElement("div");
  axisCell.style.flex = "1";
  axisCell.style.textAlign = "center";
  axisCell.textContent = `Y${step.year}`;
  stairAxis.appendChild(axisCell);
});

// ==================== Section: Caveat ====================
document.getElementById("caveat").textContent = DATA.caveat;

// ==================== ECharts: common theming helpers ====================
const ECHARTS_TEXT = "#e7eef5";
const ECHARTS_MUTED = "#90a4ae";
const ECHARTS_GRID = "rgba(255, 255, 255, 0.06)";
const CATEGORY_COLOURS = {
  hobby:        "#ffb74d",
  recreational: "#ba68c8",
  conservation: "#4dd0e1",
  commercial:   "#81c784",
  defence:      "#ef5350"
};

function commonOptions() {
  return {
    backgroundColor: "transparent",
    textStyle: { color: ECHARTS_TEXT, fontFamily: "Inter, sans-serif" },
    legend: { textStyle: { color: ECHARTS_TEXT }, top: 10 },
    grid: { left: 70, right: 30, top: 60, bottom: 60, containLabel: true }
  };
}

// ==================== Chart: Application quadrant ====================
const qFig = DATA.figures.application_quadrant;
document.getElementById("quadrant-title").textContent = qFig.title;
document.getElementById("quadrant-caption").textContent = qFig.caption;
document.getElementById("quadrant-source").textContent = "Source: " + qFig.source;

const quadrantChart = echarts.init(document.getElementById("quadrant"), null, { renderer: "canvas" });
const quadrantSeriesData = qFig.points.map(p => ({
  value: [p.x, p.y],
  name: p.name,
  itemStyle: { color: CATEGORY_COLOURS[p.category] || "#ffffff" }
}));
quadrantChart.setOption({
  ...commonOptions(),
  tooltip: {
    trigger: "item",
    backgroundColor: "rgba(16, 40, 65, 0.95)",
    borderColor: "#4dd0e1",
    textStyle: { color: "#ffffff" },
    formatter: (p) => `<strong>${p.data.name}</strong><br/>Value to customer: ${p.data.value[0]}/10<br/>Customer risk tolerance: ${p.data.value[1]}/10`
  },
  xAxis: {
    name: qFig.axis_x_label,
    nameLocation: "middle",
    nameGap: 36,
    nameTextStyle: { color: ECHARTS_TEXT, fontSize: 12 },
    min: 0, max: 10.5,
    axisLine: { lineStyle: { color: ECHARTS_MUTED } },
    axisLabel: { color: ECHARTS_MUTED },
    splitLine: { lineStyle: { color: ECHARTS_GRID } }
  },
  yAxis: {
    name: qFig.axis_y_label,
    nameLocation: "middle",
    nameGap: 50,
    nameTextStyle: { color: ECHARTS_TEXT, fontSize: 12 },
    min: 0, max: 10.5,
    axisLine: { lineStyle: { color: ECHARTS_MUTED } },
    axisLabel: { color: ECHARTS_MUTED },
    splitLine: { lineStyle: { color: ECHARTS_GRID } }
  },
  series: [{
    type: "scatter",
    symbolSize: 18,
    data: quadrantSeriesData,
    label: {
      show: true,
      position: "right",
      color: "#e7eef5",
      fontSize: 11,
      formatter: (p) => p.data.name
    },
    markArea: {
      silent: true,
      itemStyle: { color: "rgba(255, 183, 77, 0.10)", borderColor: "rgba(255, 183, 77, 0.4)", borderWidth: 1 },
      data: [[{ name: "Natural early adopters", xAxis: 6, yAxis: 5 }, { xAxis: 10.5, yAxis: 10.5 }]],
      label: { show: true, position: "insideTopRight", color: "#ffb74d", fontSize: 11, fontWeight: 600 }
    }
  }]
});

// ==================== Chart: Energy chain (custom bar cascade) ====================
const eFig = DATA.figures.energy_chain;
document.getElementById("energy-title").textContent = eFig.title;
document.getElementById("energy-caption").textContent = eFig.caption;
document.getElementById("energy-source").textContent = "Source: " + eFig.source;

const energyChart = echarts.init(document.getElementById("energy"), null, { renderer: "canvas" });

// Each stack -> a series of stages on a horizontal bar. We render each stage
// as a segment of decreasing width with the retained-percentage label inside.
function buildStackSeries(stages, baseColor, lossColor) {
  const series = [];
  for (let i = 0; i < stages.length; i++) {
    series.push({
      name: stages[i].label,
      type: "bar",
      stack: "noop_" + i,  // each stage is its own stack (single bar)
      data: [stages[i].retained],
      itemStyle: { color: i === stages.length - 1 ? baseColor : "rgba(77, 208, 225, 0.6)", borderRadius: 4 },
      label: {
        show: true,
        formatter: (p) => `${p.value}%\n${stages[i].label}`,
        position: "insideRight",
        color: "#ffffff",
        fontSize: 11,
        lineHeight: 14
      },
      barWidth: "70%"
    });
  }
  return series;
}

// Compromise visual: one horizontal bar per stack, segmented by stage retained values.
// Use overlapping bars (no stack) so each later stage masks the earlier-stage bar visually.
energyChart.setOption({
  ...commonOptions(),
  tooltip: {
    trigger: "axis",
    axisPointer: { type: "shadow" },
    backgroundColor: "rgba(16, 40, 65, 0.95)",
    borderColor: "#4dd0e1",
    textStyle: { color: "#ffffff" },
    formatter: (params) => {
      let lines = ["<strong>" + params[0].axisValue + "</strong>"];
      params.forEach(p => { if (p.value > 0) lines.push(`${p.marker} ${p.seriesName}: ${p.value}%`); });
      return lines.join("<br/>");
    }
  },
  legend: { textStyle: { color: ECHARTS_TEXT }, top: 8, type: "scroll" },
  grid: { left: 130, right: 50, top: 60, bottom: 50 },
  xAxis: {
    type: "value", max: 100,
    axisLabel: { color: ECHARTS_MUTED, formatter: "{value}%" },
    splitLine: { lineStyle: { color: ECHARTS_GRID } }
  },
  yAxis: {
    type: "category",
    data: ["RIMT (modelled)", "Conventional"],
    axisLabel: { color: ECHARTS_TEXT, fontWeight: 600, fontSize: 13 },
    axisLine: { lineStyle: { color: ECHARTS_MUTED } }
  },
  series: (function() {
    // Build series so that each "stage retained" overlays as a bar on the row.
    // We use one series per stage; the largest renders behind, smaller bars in front.
    const stages = Math.max(eFig.conventional.stages.length, eFig.rimt.stages.length);
    const series = [];
    const palette = ["#ef5350", "#ff7043", "#ffa726", "#ffb74d", "#4dd0e1"];
    for (let i = 0; i < stages; i++) {
      const conv = eFig.conventional.stages[i];
      const rimt = eFig.rimt.stages[i];
      // The series value array maps to ['RIMT (modelled)', 'Conventional'] = [yIdx 0, yIdx 1].
      series.push({
        name: conv && rimt ? conv.label.split(" (")[0] : (conv ? conv.label : rimt.label),
        type: "bar",
        data: [rimt ? rimt.retained : 0, conv ? conv.retained : 0],
        itemStyle: { color: palette[i] || palette[palette.length - 1], borderRadius: 3 },
        label: {
          show: true,
          position: "insideRight",
          color: "#ffffff",
          fontSize: 11,
          formatter: (p) => p.value + "%"
        },
        barGap: "-100%",  // overlay rather than stack
        barCategoryGap: "40%"
      });
    }
    return series;
  })()
});

// ==================== Chart: Scorecard radar ====================
const rFig = DATA.figures.scorecard_radar;
document.getElementById("radar-title").textContent = rFig.title;
document.getElementById("radar-caption").textContent = rFig.caption;
document.getElementById("radar-source").textContent = "Source: " + rFig.source;

const radarChart = echarts.init(document.getElementById("radar"), null, { renderer: "canvas" });
radarChart.setOption({
  ...commonOptions(),
  tooltip: { trigger: "item" },
  legend: { data: ["Conventional", "RIMT (modelled)"], textStyle: { color: ECHARTS_TEXT }, top: 8 },
  radar: {
    indicator: rFig.axes.map(a => ({ name: a.name, max: 5 })),
    shape: "polygon",
    radius: "68%",
    axisName: { color: ECHARTS_TEXT, fontSize: 10 },
    splitLine: { lineStyle: { color: "rgba(255,255,255,0.08)" } },
    splitArea: { areaStyle: { color: ["rgba(255,255,255,0.015)", "rgba(255,255,255,0.04)"] } },
    axisLine: { lineStyle: { color: "rgba(255,255,255,0.18)" } }
  },
  series: [{
    type: "radar",
    data: [
      {
        value: rFig.axes.map(a => a.conventional),
        name: "Conventional",
        symbol: "circle", symbolSize: 5,
        lineStyle: { color: "#b0bec5", width: 2 },
        itemStyle: { color: "#b0bec5" },
        areaStyle: { color: "rgba(176, 190, 197, 0.22)" }
      },
      {
        value: rFig.axes.map(a => a.rimt),
        name: "RIMT (modelled)",
        symbol: "circle", symbolSize: 5,
        lineStyle: { color: "#4dd0e1", width: 2 },
        itemStyle: { color: "#4dd0e1" },
        areaStyle: { color: "rgba(77, 208, 225, 0.32)" }
      }
    ]
  }]
});

// ==================== Chart: CO2 sensitivity ====================
const cFig = DATA.figures.co2_sensitivity;
document.getElementById("co2-title").textContent = cFig.title;
document.getElementById("co2-caption").textContent = cFig.caption;
document.getElementById("co2-source").textContent = "Source: " + cFig.source;

const rimtDisplaced = cFig.years.map((y, i) => +(cFig.baseline_gt_co2[i] * cFig.rimt_share_pct[i] / 100).toFixed(3));
const co2Chart = echarts.init(document.getElementById("co2"), null, { renderer: "canvas" });
co2Chart.setOption({
  ...commonOptions(),
  tooltip: { trigger: "axis", backgroundColor: "rgba(16, 40, 65, 0.95)", borderColor: "#4dd0e1", textStyle: { color: "#ffffff" } },
  legend: { data: ["Baseline (no action)", "IMO target trajectory", "Avoided by RIMT-share"], textStyle: { color: ECHARTS_TEXT }, top: 8 },
  xAxis: {
    type: "category", data: cFig.years,
    axisLabel: { color: ECHARTS_MUTED },
    axisLine: { lineStyle: { color: ECHARTS_MUTED } }
  },
  yAxis: {
    type: "value",
    name: "Gt CO2 / yr",
    nameTextStyle: { color: ECHARTS_TEXT },
    axisLabel: { color: ECHARTS_MUTED },
    splitLine: { lineStyle: { color: ECHARTS_GRID } }
  },
  series: [
    {
      name: "Baseline (no action)", type: "line", smooth: true,
      data: cFig.baseline_gt_co2,
      lineStyle: { color: "#ef5350", type: "dashed", width: 2 },
      itemStyle: { color: "#ef5350" }
    },
    {
      name: "IMO target trajectory", type: "line", smooth: true,
      data: cFig.imo_target_gt_co2,
      lineStyle: { color: "#ffb74d", width: 2 },
      itemStyle: { color: "#ffb74d" },
      areaStyle: { color: "rgba(255, 183, 77, 0.12)" }
    },
    {
      name: "Avoided by RIMT-share", type: "line", smooth: true,
      data: rimtDisplaced,
      lineStyle: { color: "#4dd0e1", width: 3 },
      itemStyle: { color: "#4dd0e1" },
      areaStyle: { color: "rgba(77, 208, 225, 0.25)" }
    }
  ]
});

// ==================== Chart: Acoustic spectrum ====================
const aFig = DATA.figures.acoustic_spectrum;
document.getElementById("acoustic-title").textContent = aFig.title;
document.getElementById("acoustic-caption").textContent = aFig.caption;
document.getElementById("acoustic-source").textContent = "Source: " + aFig.source;

const acousticChart = echarts.init(document.getElementById("acoustic"), null, { renderer: "canvas" });
const whaleColours = ["rgba(186, 104, 200, 0.18)", "rgba(77, 208, 225, 0.16)", "rgba(255, 183, 77, 0.18)", "rgba(129, 199, 132, 0.18)"];
const markAreaData = aFig.whale_bands.map((band, i) => [
  { name: band.name, xAxis: band.min_hz, itemStyle: { color: whaleColours[i % whaleColours.length] } },
  { xAxis: band.max_hz }
]);

acousticChart.setOption({
  ...commonOptions(),
  tooltip: {
    trigger: "axis",
    backgroundColor: "rgba(16, 40, 65, 0.95)",
    borderColor: "#4dd0e1",
    textStyle: { color: "#ffffff" },
    formatter: (params) => {
      const lines = [`<strong>${params[0].axisValueLabel} Hz</strong>`];
      params.forEach(p => lines.push(`${p.marker} ${p.seriesName}: ${p.value[1]} dB`));
      return lines.join("<br/>");
    }
  },
  legend: { data: ["Container ship", "Electric small vessel", "RIMT (projected)"], textStyle: { color: ECHARTS_TEXT }, top: 8 },
  xAxis: {
    type: "log",
    name: "Frequency (Hz)",
    nameLocation: "middle", nameGap: 36,
    nameTextStyle: { color: ECHARTS_TEXT },
    axisLabel: { color: ECHARTS_MUTED, formatter: (v) => v >= 1000 ? (v / 1000) + "k" : v },
    splitLine: { lineStyle: { color: ECHARTS_GRID } }
  },
  yAxis: {
    type: "value",
    name: "dB re 1 uPa @ 1 m",
    nameTextStyle: { color: ECHARTS_TEXT },
    min: 60, max: 200,
    axisLabel: { color: ECHARTS_MUTED },
    splitLine: { lineStyle: { color: ECHARTS_GRID } }
  },
  series: [
    {
      name: "Container ship", type: "line", smooth: true,
      data: aFig.freq_hz.map((f, i) => [f, aFig.container_ship_db[i]]),
      lineStyle: { color: "#ef5350", width: 2 }, itemStyle: { color: "#ef5350" }
    },
    {
      name: "Electric small vessel", type: "line", smooth: true,
      data: aFig.freq_hz.map((f, i) => [f, aFig.electric_small_vessel_db[i]]),
      lineStyle: { color: "#b0bec5", width: 2 }, itemStyle: { color: "#b0bec5" }
    },
    {
      name: "RIMT (projected)", type: "line", smooth: true,
      data: aFig.freq_hz.map((f, i) => [f, aFig.rimt_projected_db[i]]),
      lineStyle: { color: "#4dd0e1", width: 3 }, itemStyle: { color: "#4dd0e1" },
      markArea: {
        silent: true,
        label: { show: true, position: "insideTop", color: "rgba(255,255,255,0.6)", fontSize: 10 },
        data: markAreaData
      }
    }
  ]
});

// ==================== Resize handling ====================
window.addEventListener("resize", () => {
  [quadrantChart, energyChart, radarChart, co2Chart, acousticChart].forEach(c => c.resize());
});

// ==================== AOS init (after DOM populated) ====================
AOS.init({ duration: 800, once: true, offset: 70, easing: "ease-out-cubic" });

</script>

</body>
</html>
"""


if __name__ == "__main__":
    main()
