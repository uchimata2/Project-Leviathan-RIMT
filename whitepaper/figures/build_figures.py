#!/usr/bin/env python3
"""
build_figures.py -- Generate the three RIMT whitepaper SVG figures and embed
them inline in RIMT-whitepaper.md and RIMT-vs-conventional-comparison.md.

Figures:
    Figure 1 -- IDE electrode cross-section  (w, g, d, lambda labelled)
    Figure 2 -- Asymmetric sawtooth waveform (t_r, t_f marked)
    Figure 3 -- Energy conversion chain      (conventional vs. RIMT)

Usage:
    python github-repo/whitepaper/figures/build_figures.py

Outputs:
    github-repo/whitepaper/figures/fig-1.svg
    github-repo/whitepaper/figures/fig-2.svg
    github-repo/whitepaper/figures/fig-3.svg
    github-repo/whitepaper/RIMT-whitepaper.md           (inline SVG blocks updated)
    github-repo/comparison/RIMT-vs-conventional-comparison.md  (Figure 1 block updated)

The MD update locates HTML comment markers
    <!-- FIGURE_N_START --> ... <!-- FIGURE_N_END -->
and replaces the content between them with the current figure HTML.
Re-running is idempotent once the markers are in place.
"""

import re
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent          # whitepaper/figures/
WP_DIR   = THIS_DIR.parent                          # whitepaper/
REPO_DIR = WP_DIR.parent                            # github-repo/
COMP_DIR = REPO_DIR / "comparison"

WP_MD   = WP_DIR / "RIMT-whitepaper.md"
COMP_MD = COMP_DIR / "RIMT-vs-conventional-comparison.md"


# ---------------------------------------------------------------------------
# Figure 1 -- IDE cross-section schematic
# ---------------------------------------------------------------------------
def _fig1_svg() -> str:
    """Schematic cross-section of the IDE layer stack."""
    return """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 290"
     style="display:block;max-width:100%;margin:0.5em auto;font-family:'Times New Roman',serif">
  <defs>
    <marker id="f1r" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L7,2.5 L0,5 Z" fill="#333"/>
    </marker>
    <marker id="f1l" markerWidth="7" markerHeight="5" refX="0" refY="2.5" orient="auto">
      <path d="M7,0 L0,2.5 L7,5 Z" fill="#333"/>
    </marker>
  </defs>

  <!-- background -->
  <rect width="540" height="290" fill="white"/>

  <!-- Seawater + EDL -->
  <rect x="15" y="14" width="460" height="96" fill="#d6eaf8" stroke="#5dade2" stroke-width="1"/>
  <text x="245" y="50" text-anchor="middle" font-size="13" fill="#1a5276">Seawater + Electrical Double Layer (EDL)</text>
  <line x1="50" y1="80" x2="300" y2="80" stroke="#c0392b" stroke-width="2" marker-end="url(#f1r)"/>
  <text x="175" y="74" text-anchor="middle" font-size="11" fill="#c0392b">travelling wave</text>

  <!-- Dielectric (Ta2O5) -->
  <rect x="15" y="110" width="460" height="20" fill="#a9cce3" stroke="#2e86c1" stroke-width="1"/>
  <text x="245" y="124" text-anchor="middle" font-size="11" fill="#1b4f72">Ta&#x2082;O&#x2085; dielectric &#xb7; ALD &#xb7; 500 nm</text>

  <!-- IDE electrode fingers: schematic w=90 px, g=46 px -->
  <!-- finger 1 phase + -->
  <rect x="15"  y="130" width="90" height="42" fill="#f9e547" stroke="#9a7d0a" stroke-width="1.5"/>
  <text x="60"  y="158" text-anchor="middle" font-size="18" fill="#922b21">+</text>
  <!-- finger 2 phase - -->
  <rect x="151" y="130" width="90" height="42" fill="#f9e547" stroke="#9a7d0a" stroke-width="1.5"/>
  <text x="196" y="158" text-anchor="middle" font-size="18" fill="#1a5276">&#x2212;</text>
  <!-- finger 3 phase + -->
  <rect x="287" y="130" width="90" height="42" fill="#f9e547" stroke="#9a7d0a" stroke-width="1.5"/>
  <text x="332" y="158" text-anchor="middle" font-size="18" fill="#922b21">+</text>
  <!-- finger 4 phase - (partial) -->
  <rect x="423" y="130" width="52" height="42" fill="#f9e547" stroke="#9a7d0a" stroke-width="1.5"/>
  <text x="449" y="158" text-anchor="middle" font-size="18" fill="#1a5276">&#x2212;</text>

  <!-- Hull substrate -->
  <rect x="15" y="172" width="460" height="76" fill="#b0bec5" stroke="#78909c" stroke-width="1.5"/>
  <text x="245" y="216" text-anchor="middle" font-size="13" font-weight="bold" fill="#263238">Hull substrate</text>

  <!-- Dimension: w (finger 1 width 90 px) -->
  <line x1="15" y1="125" x2="105" y2="125" stroke="#333" stroke-width="1"
        marker-start="url(#f1l)" marker-end="url(#f1r)"/>
  <text x="60" y="119" text-anchor="middle" font-size="12" font-style="italic">w</text>

  <!-- Dimension: g (gap 46 px) -->
  <line x1="105" y1="125" x2="151" y2="125" stroke="#333" stroke-width="1"
        marker-start="url(#f1l)" marker-end="url(#f1r)"/>
  <text x="128" y="119" text-anchor="middle" font-size="12" font-style="italic">g</text>

  <!-- Dimension: lambda = 2(w+g), from finger1 left to finger3 left (272 px) -->
  <line x1="15" y1="258" x2="287" y2="258" stroke="#333" stroke-width="1"
        marker-start="url(#f1l)" marker-end="url(#f1r)"/>
  <line x1="15"  y1="253" x2="15"  y2="263" stroke="#333" stroke-width="1"/>
  <line x1="287" y1="253" x2="287" y2="263" stroke="#333" stroke-width="1"/>
  <text x="151" y="275" text-anchor="middle" font-size="12" font-style="italic">
    &#x3bb; = 2(w + g)
  </text>

  <!-- Dimension: d (dielectric thickness), right-side leader -->
  <line x1="485" y1="110" x2="485" y2="130" stroke="#333" stroke-width="1"
        marker-start="url(#f1l)" marker-end="url(#f1r)"/>
  <text x="491" y="123" font-size="12" font-style="italic" fill="#1b4f72">d</text>

  <!-- Parameter value box (right margin) -->
  <text x="498" y="137" font-size="11" fill="#444">w = 10 &#xb5;m</text>
  <text x="498" y="151" font-size="11" fill="#444">g = 5 &#xb5;m</text>
  <text x="498" y="165" font-size="11" fill="#444">d = 500 nm</text>
  <text x="498" y="179" font-size="11" fill="#444">&#x3bb; = 30 &#xb5;m</text>

  <!-- Not-to-scale note -->
  <text x="15" y="284" font-size="10" fill="#888" font-style="italic">Schematic cross-section &#x2014; not to scale.</text>
</svg>"""


# ---------------------------------------------------------------------------
# Figure 2 -- Asymmetric sawtooth waveform
# ---------------------------------------------------------------------------
def _fig2_svg() -> str:
    """
    Two full cycles of the asymmetric sawtooth at f_c = 2 MHz.
    t_r = 100 ns (fast rise), t_f = 400 ns (slow fall), T = 500 ns.

    Plot area x in [70, 510], y in [30, 185].
    Scale: 440 px / 1000 ns = 0.44 px/ns.
    Cycle 1: t=0..500  -> x=70..290
    Cycle 2: t=500..1000 -> x=290..510
    t_r=100ns -> dx=44px; t_f=400ns -> dx=176px; T=500ns -> dx=220px
    """
    return """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 260"
     style="display:block;max-width:100%;margin:0.5em auto;font-family:'Times New Roman',serif">
  <defs>
    <marker id="f2r" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L7,2.5 L0,5 Z" fill="#333"/>
    </marker>
    <marker id="f2l" markerWidth="7" markerHeight="5" refX="0" refY="2.5" orient="auto">
      <path d="M7,0 L0,2.5 L7,5 Z" fill="#333"/>
    </marker>
    <marker id="f2rc" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L7,2.5 L0,5 Z" fill="#922b21"/>
    </marker>
    <marker id="f2lc" markerWidth="7" markerHeight="5" refX="0" refY="2.5" orient="auto">
      <path d="M7,0 L0,2.5 L7,5 Z" fill="#922b21"/>
    </marker>
    <marker id="f2rb" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L7,2.5 L0,5 Z" fill="#1a5276"/>
    </marker>
    <marker id="f2lb" markerWidth="7" markerHeight="5" refX="0" refY="2.5" orient="auto">
      <path d="M7,0 L0,2.5 L7,5 Z" fill="#1a5276"/>
    </marker>
  </defs>

  <rect width="560" height="260" fill="white"/>

  <!-- Axes -->
  <line x1="65" y1="185" x2="520" y2="185" stroke="#333" stroke-width="1.5" marker-end="url(#f2r)"/>
  <line x1="70" y1="190" x2="70" y2="22"  stroke="#333" stroke-width="1.5" marker-end="url(#f2r)"/>

  <!-- Axis labels -->
  <text x="527" y="189" font-size="13" fill="#333" font-style="italic">t</text>
  <text x="44"  y="35"  font-size="13" fill="#333" font-style="italic">V</text>
  <text x="70"  y="200" text-anchor="middle" font-size="10" fill="#555">0</text>

  <!-- V_drive dashed reference line -->
  <line x1="62" y1="35" x2="516" y2="35" stroke="#ccc" stroke-width="1" stroke-dasharray="5,4"/>
  <text x="57" y="38" text-anchor="end" font-size="11" font-style="italic" fill="#1a5276">V</text>

  <!-- Light grid lines at 100, 200, ..., 900 ns -->
  <!-- x = 70 + ns*0.44  -->
  <line x1="114" y1="30" x2="114" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="158" y1="30" x2="158" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="202" y1="30" x2="202" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="246" y1="30" x2="246" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="290" y1="30" x2="290" y2="185" stroke="#e0e0e0" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="334" y1="30" x2="334" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="378" y1="30" x2="378" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="422" y1="30" x2="422" y2="185" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="466" y1="30" x2="466" y2="185" stroke="#f0f0f0" stroke-width="1"/>

  <!-- Shaded grab/release regions (cycle 1 only for clarity) -->
  <polygon points="70,185 114,35 114,185"  fill="#fadbd8" fill-opacity="0.6"/>
  <polygon points="114,35 290,185 114,185" fill="#d6eaf8" fill-opacity="0.4"/>

  <!-- Waveform (2 full cycles) -->
  <!-- vertices: (70,185) (114,35) (290,185) (334,35) (510,185) -->
  <polyline points="70,185 114,35 290,185 334,35 510,185"
            fill="none" stroke="#2471a3" stroke-width="2.5" stroke-linejoin="miter"/>

  <!-- "grab" / "release" region labels -->
  <text x="92"  y="125" text-anchor="middle" font-size="11" fill="#922b21" font-style="italic">grab</text>
  <text x="202" y="125" text-anchor="middle" font-size="11" fill="#1a5276" font-style="italic">release</text>

  <!-- === Dimension annotations (cycle 1) === -->

  <!-- t_r: x=70..114 at y=207 -->
  <line x1="70" y1="207" x2="114" y2="207" stroke="#922b21" stroke-width="1"
        marker-start="url(#f2lc)" marker-end="url(#f2rc)"/>
  <text x="92" y="222" text-anchor="middle" font-size="12" fill="#922b21">
    <tspan font-style="italic">t</tspan><tspan baseline-shift="sub" font-size="9">r</tspan><tspan> = 100 ns</tspan>
  </text>

  <!-- t_f: x=114..290 at y=207 -->
  <line x1="114" y1="207" x2="290" y2="207" stroke="#1a5276" stroke-width="1"
        marker-start="url(#f2lb)" marker-end="url(#f2rb)"/>
  <text x="202" y="222" text-anchor="middle" font-size="12" fill="#1a5276">
    <tspan font-style="italic">t</tspan><tspan baseline-shift="sub" font-size="9">f</tspan><tspan> = 400 ns</tspan>
  </text>

  <!-- T: x=70..290 at y=234 -->
  <line x1="70"  y1="234" x2="290" y2="234" stroke="#555" stroke-width="1"
        marker-start="url(#f2l)" marker-end="url(#f2r)"/>
  <line x1="70"  y1="229" x2="70"  y2="239" stroke="#555" stroke-width="1"/>
  <line x1="290" y1="229" x2="290" y2="239" stroke="#555" stroke-width="1"/>
  <text x="180" y="250" text-anchor="middle" font-size="12" fill="#555">
    <tspan font-style="italic">T</tspan><tspan> = 500 ns  (</tspan><tspan font-style="italic">f</tspan><tspan baseline-shift="sub" font-size="9">c</tspan><tspan> = 2 MHz)</tspan>
  </text>

  <!-- x-axis labels -->
  <text x="290" y="199" text-anchor="middle" font-size="10" fill="#777">500 ns</text>
  <text x="510" y="199" text-anchor="middle" font-size="10" fill="#777">1000 ns</text>
</svg>"""


# ---------------------------------------------------------------------------
# Figure 3 -- Energy conversion chain (conventional vs. RIMT)
# ---------------------------------------------------------------------------
def _fig3_svg() -> str:
    """
    Side-by-side horizontal bar chart.
    Conventional: 100 -> 50 -> 47.5 -> 33
    RIMT (full chain): 100 -> 99 -> 96 -> 83
    Bar widths proportional to retained %, max width = 230 px (at 100%).
    """
    # Conventional bar widths (230 * pct/100):
    #   100 -> 230,  50 -> 115,  47.5 -> 109,  33 -> 75.9
    # RIMT bar widths (cumulative full chain):
    #   100 -> 230,  99 -> 228,  96 -> 221,  80 -> 184
    # Final 80% = full chain (0.99 * 0.97 * 0.83 ~ 80%); tile-only η = 83% per WP §4.4.
    return """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 310"
     style="display:block;max-width:100%;margin:0.5em auto;font-family:'Times New Roman',serif">
  <defs>
    <marker id="f3d" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L7,2.5 L0,5 Z" fill="#555"/>
    </marker>
  </defs>

  <rect width="640" height="310" fill="white"/>

  <!-- Divider -->
  <line x1="318" y1="8" x2="318" y2="295" stroke="#ddd" stroke-width="1"/>

  <!-- Column headers -->
  <text x="157" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#111">Conventional propulsion</text>
  <text x="476" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#111">RIMT (modelled)</text>

  <!-- ========== Conventional chain (left column, x origin = 15) ========== -->

  <!-- Stage 1: 100%, w=230 -->
  <rect x="15" y="28" width="230" height="34" fill="#27ae60" stroke="#1e8449" stroke-width="1"/>
  <text x="130" y="50" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Fuel chemical energy &#x2013; 100%</text>

  <!-- Loss label + arrow -->
  <text x="250" y="68" font-size="11" fill="#c0392b">&#x2212;50 % combustion</text>
  <line x1="127" y1="62" x2="127" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#f3d)"/>

  <!-- Stage 2: 50%, w=115 -->
  <rect x="15" y="74" width="115" height="34" fill="#f39c12" stroke="#d68910" stroke-width="1"/>
  <text x="72" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">50%</text>

  <!-- Loss label + arrow -->
  <text x="134" y="113" font-size="11" fill="#c0392b">&#x2212;2.5 % shaft</text>
  <line x1="72" y1="108" x2="72" y2="118" stroke="#555" stroke-width="1.5" marker-end="url(#f3d)"/>

  <!-- Stage 3: 47.5%, w=109 -->
  <rect x="15" y="120" width="109" height="34" fill="#e67e22" stroke="#d35400" stroke-width="1"/>
  <text x="69" y="142" text-anchor="middle" font-size="12" fill="white" font-weight="bold">47.5%</text>

  <!-- Loss label + arrow -->
  <text x="128" y="159" font-size="11" fill="#c0392b">&#x2212;14 % propeller</text>
  <line x1="69" y1="154" x2="69" y2="164" stroke="#555" stroke-width="1.5" marker-end="url(#f3d)"/>

  <!-- Stage 4: 33%, w=76 -->
  <rect x="15" y="166" width="76" height="34" fill="#e74c3c" stroke="#cb4335" stroke-width="1"/>
  <text x="53" y="188" text-anchor="middle" font-size="12" fill="white" font-weight="bold">&#x2248;33%</text>
  <text x="96" y="188" font-size="11" fill="#555">useful thrust</text>

  <!-- ========== RIMT chain (right column, x origin = 330) ========== -->

  <!-- Stage 1: 100%, w=230 -->
  <rect x="330" y="28" width="230" height="34" fill="#2980b9" stroke="#1f618d" stroke-width="1"/>
  <text x="445" y="50" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Battery electric &#x2013; 100%</text>

  <!-- Loss label + arrow -->
  <text x="563" y="68" font-size="11" fill="#1a5276">&#x2212;1 % DC bus</text>
  <line x1="445" y1="62" x2="445" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#f3d)"/>

  <!-- Stage 2: 99%, w=228 -->
  <rect x="330" y="74" width="228" height="34" fill="#2471a3" stroke="#1f618d" stroke-width="1"/>
  <text x="444" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">99%</text>

  <!-- Loss label + arrow -->
  <text x="561" y="113" font-size="11" fill="#1a5276">&#x2212;3 % GaN PEM</text>
  <line x1="444" y1="108" x2="444" y2="118" stroke="#555" stroke-width="1.5" marker-end="url(#f3d)"/>

  <!-- Stage 3: 96%, w=221 -->
  <rect x="330" y="120" width="221" height="34" fill="#1a6ea0" stroke="#154360" stroke-width="1"/>
  <text x="440" y="142" text-anchor="middle" font-size="12" fill="white" font-weight="bold">96%</text>

  <!-- Loss label + arrow -->
  <text x="554" y="159" font-size="11" fill="#1a5276">&#x2212;16 % tile losses</text>
  <line x1="440" y1="154" x2="440" y2="164" stroke="#555" stroke-width="1.5" marker-end="url(#f3d)"/>

  <!-- Stage 4: 80% full chain (tile eta = 83%); w=184 -->
  <rect x="330" y="166" width="184" height="34" fill="#27ae60" stroke="#1e8449" stroke-width="1"/>
  <text x="422" y="188" text-anchor="middle" font-size="12" fill="white" font-weight="bold">&#x2248;80%</text>
  <text x="518" y="188" font-size="11" fill="#555">useful thrust&#x2020;</text>

  <!-- Comparison dashed link -->
  <line x1="91" y1="194" x2="330" y2="194" stroke="#bbb" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="319" y="218" text-anchor="end" font-size="11" fill="#555" font-style="italic">83% vs 33%</text>

  <!-- Stage labels (right of conventional, left of RIMT) -->
  <text x="155" y="42"  font-size="10" fill="#888">fuel input</text>
  <text x="155" y="88"  font-size="10" fill="#888">after combustion</text>
  <text x="155" y="134" font-size="10" fill="#888">after shaft</text>
  <text x="155" y="180" font-size="10" fill="#888">propeller thrust</text>

  <!-- Footnote + source note -->
  <text x="320" y="243" text-anchor="middle" font-size="10" fill="#888" font-style="italic">&#x2020; Full chain = 0.99 &#xd7; 0.97 &#xd7; tile &#x3b7; (83 %) &#x2248; 80 %. WP &#xa7;4.4 headline 83 % is tile-boundary (&#xa7;4.3 definition).</text>
  <text x="320" y="257" text-anchor="middle" font-size="10" fill="#888" font-style="italic">Conventional: Comparison doc &#xa7;1&#x2013;2. RIMT: WP &#xa7;4.4 (Model 3, &#x3b1; = 0.005). Numbers rounded.</text>
</svg>"""


# ---------------------------------------------------------------------------
# Figure 5 -- η-vs-σ_seawater sensitivity curve (log-scale x-axis, WP §5.2)
# ---------------------------------------------------------------------------
def _fig5_svg() -> str:
    """η-vs-σ_seawater sensitivity curve; calls tuned_performance in a loop."""
    import math
    import sys as _sys

    _sdir = str(REPO_DIR / "simulations")
    if _sdir not in _sys.path:
        _sys.path.insert(0, _sdir)
    from rimt_simulation import tuned_performance  # noqa: PLC0415

    # 40 log-spaced σ values 0.05 → 5 S/m  (covers freshwater → open ocean)
    sigma_min, sigma_max = 0.05, 5.0
    _n = 40
    sigmas = [sigma_min * (sigma_max / sigma_min) ** (i / (_n - 1)) for i in range(_n)]
    etas   = [
        tuned_performance(
            vessel_speed_m_s=10.0, hull_area_m2=1.0,
            thrust_density_N_m2=50.0, sigma_seawater=s,
        ).efficiency * 100
        for s in sigmas
    ]

    # Plot-area bounds (x: log-scale; y: linear %-scale, y-inverted)
    X0, X1, YB, YT = 70.0, 510.0, 215.0, 22.0
    log_min = math.log10(sigma_min)                     # ≈ −1.301
    log_rng = math.log10(sigma_max) - log_min           # 2.0

    def _x(s: float) -> float:
        return X0 + (math.log10(s) - log_min) / log_rng * (X1 - X0)

    def _y(e: float) -> float:
        return YB + e / 100.0 * (YT - YB)   # YT < YB → negative slope

    # Curve polyline data (40 pts, log-spaced)
    pts = " ".join(f"{_x(s):.1f},{_y(e):.1f}" for s, e in zip(sigmas, etas))

    # Named tick positions
    tx = {sv: _x(sv) for sv in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0)}
    ty = {ev: _y(ev) for ev in (20, 40, 60, 80)}

    # Shaded-region bounds
    x_fw  = _x(0.1)           # freshwater region right edge (σ = 0.1 S/m)
    fw_w  = x_fw - X0
    x_oo  = _x(3.5)           # open-ocean region left edge  (σ = 3.5 S/m)
    oo_w  = X1 - x_oo

    # Design point (§3.5 reference: σ = 4.8 S/m → η ≈ 83 %)
    xdp   = _x(4.8)
    ydp   = _y(83)
    y83   = _y(83)

    # Region label x-centres
    fw_cx = (X0 + x_fw) / 2
    oo_cx = (x_oo + X1) / 2

    return f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 265"
     style="display:block;max-width:100%;margin:0.5em auto;font-family:'Times New Roman',serif">

  <defs>
    <marker id="f5rx" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L7,2.5 L0,5 Z" fill="#333"/>
    </marker>
    <marker id="f5ux" markerWidth="5" markerHeight="7" refX="2.5" refY="7" orient="auto">
      <path d="M0,0 L2.5,7 L5,0 Z" fill="#333" transform="rotate(180,2.5,3.5)"/>
    </marker>
  </defs>

  <rect width="560" height="265" fill="white"/>

  <!-- Freshwater shading (σ < 0.1 S/m) -->
  <rect x="{X0:.1f}" y="{YT:.1f}" width="{fw_w:.1f}" height="{YB - YT:.1f}"
        fill="#fef9e7" fill-opacity="0.75"/>

  <!-- Open-ocean shading (σ > 3.5 S/m) -->
  <rect x="{x_oo:.1f}" y="{YT:.1f}" width="{oo_w:.1f}" height="{YB - YT:.1f}"
        fill="#d6eaf8" fill-opacity="0.55"/>

  <!-- Horizontal grid lines (20 / 40 / 60 / 80 %) -->
  <line x1="{X0:.1f}" y1="{ty[80]:.1f}" x2="{X1:.1f}" y2="{ty[80]:.1f}" stroke="#ebebeb" stroke-width="1"/>
  <line x1="{X0:.1f}" y1="{ty[60]:.1f}" x2="{X1:.1f}" y2="{ty[60]:.1f}" stroke="#ebebeb" stroke-width="1"/>
  <line x1="{X0:.1f}" y1="{ty[40]:.1f}" x2="{X1:.1f}" y2="{ty[40]:.1f}" stroke="#ebebeb" stroke-width="1"/>
  <line x1="{X0:.1f}" y1="{ty[20]:.1f}" x2="{X1:.1f}" y2="{ty[20]:.1f}" stroke="#ebebeb" stroke-width="1"/>

  <!-- Vertical grid lines at σ ticks -->
  <line x1="{tx[0.1]:.1f}"  y1="{YT:.1f}" x2="{tx[0.1]:.1f}"  y2="{YB:.1f}" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="{tx[0.2]:.1f}"  y1="{YT:.1f}" x2="{tx[0.2]:.1f}"  y2="{YB:.1f}" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="{tx[0.5]:.1f}"  y1="{YT:.1f}" x2="{tx[0.5]:.1f}"  y2="{YB:.1f}" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="{tx[1.0]:.1f}"  y1="{YT:.1f}" x2="{tx[1.0]:.1f}"  y2="{YB:.1f}" stroke="#f0f0f0" stroke-width="1"/>
  <line x1="{tx[2.0]:.1f}"  y1="{YT:.1f}" x2="{tx[2.0]:.1f}"  y2="{YB:.1f}" stroke="#f0f0f0" stroke-width="1"/>

  <!-- η = 83 % dashed reference line -->
  <line x1="{X0:.1f}" y1="{y83:.1f}" x2="{X1:.1f}" y2="{y83:.1f}"
        stroke="#ccc" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="{X1 + 3:.1f}" y="{y83 + 3.5:.1f}" font-size="9" fill="#aaa">83%</text>

  <!-- Axes -->
  <line x1="{X0:.1f}" y1="{YB:.1f}" x2="{X1 + 5:.1f}" y2="{YB:.1f}"
        stroke="#333" stroke-width="1.5" marker-end="url(#f5rx)"/>
  <line x1="{X0:.1f}" y1="{YB:.1f}" x2="{X0:.1f}" y2="{YT - 5:.1f}"
        stroke="#333" stroke-width="1.5" marker-end="url(#f5ux)"/>

  <!-- η curve -->
  <polyline points="{pts}"
            fill="none" stroke="#2471a3" stroke-width="2.5" stroke-linejoin="round"/>

  <!-- Design-point circle (σ = 4.8 S/m, η ≈ 83 %) -->
  <circle cx="{xdp:.1f}" cy="{ydp:.1f}" r="4" fill="#e74c3c" stroke="white" stroke-width="1.2"/>

  <!-- Y-axis tick marks and labels -->
  <line x1="{X0:.1f}" y1="{ty[80]:.1f}" x2="{X0 - 6:.1f}" y2="{ty[80]:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{X0:.1f}" y1="{ty[60]:.1f}" x2="{X0 - 6:.1f}" y2="{ty[60]:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{X0:.1f}" y1="{ty[40]:.1f}" x2="{X0 - 6:.1f}" y2="{ty[40]:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{X0:.1f}" y1="{ty[20]:.1f}" x2="{X0 - 6:.1f}" y2="{ty[20]:.1f}" stroke="#555" stroke-width="1"/>
  <text x="{X0 - 8:.1f}" y="{ty[80] + 3.5:.1f}" text-anchor="end" font-size="10" fill="#555">80</text>
  <text x="{X0 - 8:.1f}" y="{ty[60] + 3.5:.1f}" text-anchor="end" font-size="10" fill="#555">60</text>
  <text x="{X0 - 8:.1f}" y="{ty[40] + 3.5:.1f}" text-anchor="end" font-size="10" fill="#555">40</text>
  <text x="{X0 - 8:.1f}" y="{ty[20] + 3.5:.1f}" text-anchor="end" font-size="10" fill="#555">20</text>
  <text x="{X0 - 8:.1f}" y="{YT + 3.5:.1f}"     text-anchor="end" font-size="10" fill="#555">100</text>

  <!-- Y-axis label -->
  <text x="46" y="17" text-anchor="end" font-size="12" fill="#333" font-style="italic">&#x3b7; [%]</text>

  <!-- X-axis tick marks and labels -->
  <line x1="{tx[0.05]:.1f}" y1="{YB:.1f}" x2="{tx[0.05]:.1f}" y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{tx[0.1]:.1f}"  y1="{YB:.1f}" x2="{tx[0.1]:.1f}"  y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{tx[0.2]:.1f}"  y1="{YB:.1f}" x2="{tx[0.2]:.1f}"  y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{tx[0.5]:.1f}"  y1="{YB:.1f}" x2="{tx[0.5]:.1f}"  y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{tx[1.0]:.1f}"  y1="{YB:.1f}" x2="{tx[1.0]:.1f}"  y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{tx[2.0]:.1f}"  y1="{YB:.1f}" x2="{tx[2.0]:.1f}"  y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <line x1="{tx[5.0]:.1f}"  y1="{YB:.1f}" x2="{tx[5.0]:.1f}"  y2="{YB + 6:.1f}" stroke="#555" stroke-width="1"/>
  <text x="{tx[0.05]:.1f}" y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">0.05</text>
  <text x="{tx[0.1]:.1f}"  y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">0.1</text>
  <text x="{tx[0.2]:.1f}"  y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">0.2</text>
  <text x="{tx[0.5]:.1f}"  y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">0.5</text>
  <text x="{tx[1.0]:.1f}"  y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">1</text>
  <text x="{tx[2.0]:.1f}"  y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">2</text>
  <text x="{tx[5.0]:.1f}"  y="{YB + 17:.1f}" text-anchor="middle" font-size="9.5" fill="#555">5</text>

  <!-- X-axis label -->
  <text x="{(X0 + X1) / 2:.1f}" y="{YB + 33:.1f}" text-anchor="middle" font-size="11" fill="#333"><tspan font-style="italic">&#x3c3;</tspan><tspan font-size="8" dy="2">sw</tspan><tspan dy="-2"> [S m&#x207b;&#xb9;] (log scale)</tspan></text>

  <!-- Region labels -->
  <text x="{fw_cx:.1f}" y="36" text-anchor="middle" font-size="9" fill="#9a7d0a">freshwater</text>
  <text x="{oo_cx:.1f}" y="36" text-anchor="middle" font-size="9" fill="#1a5276">ocean</text>

  <!-- Design-point annotation -->
  <text x="{xdp - 7:.1f}" y="{ydp - 8:.1f}" text-anchor="end" font-size="9" fill="#c0392b">&#x3c3; = 4.8&#xa0;S/m</text>
</svg>"""


# ---------------------------------------------------------------------------
# Wrap each SVG in a <figure> block with a numbered caption
# ---------------------------------------------------------------------------
def _wrap_figure(n: int, svg: str, caption: str) -> str:
    return (
        f'<figure style="margin:1.2em 0;text-align:center">\n'
        f'{svg}\n'
        f'<figcaption style="font-size:10pt;color:#444;margin-top:4pt;text-align:left">'
        f'<strong>Figure {n}.</strong> {caption}</figcaption>\n'
        f'</figure>'
    )


FIGURES = {
    1: _wrap_figure(
        1,
        _fig1_svg(),
        (
            "Schematic cross-section of the IDE layer stack (not to scale). "
            "Electrode finger width <em>w</em> = 10 &mu;m; "
            "inter-electrode gap <em>g</em> = 5 &mu;m; "
            "spatial wavelength &lambda; = 2(<em>w</em>&nbsp;+&nbsp;<em>g</em>) = 30 &mu;m; "
            "Ta&#x2082;O&#x2085; dielectric thickness <em>d</em> = 500 nm (ALD). "
            "Alternating +/&minus; polarity on adjacent fingers produces the lateral potential "
            "gradient; the traveling wave (red arrow) advances in the direction of net ion transport."
        ),
    ),
    2: _wrap_figure(
        2,
        _fig2_svg(),
        (
            "Asymmetric sawtooth carrier waveform at "
            "<em>f</em><sub>c</sub> = 2 MHz (<em>T</em> = 500 ns). "
            "Fast-rise &ldquo;grab&rdquo; phase "
            "<em>t</em><sub>r</sub> = 100 ns (shaded red, 20% of period); "
            "slow-fall &ldquo;release&rdquo; phase "
            "<em>t</em><sub>f</sub> = 400 ns (shaded blue, 80% of period). "
            "The 1&thinsp;:&thinsp;4 rise&thinsp;:&thinsp;fall ratio creates the net "
            "unidirectional momentum bias. Two complete cycles shown."
        ),
    ),
    3: _wrap_figure(
        3,
        _fig3_svg(),
        (
            "Energy conversion chain: conventional diesel-mechanical propulsion (left) "
            "vs. RIMT battery-electric propulsion (right). "
            "Bar width is proportional to the cumulative retained fraction of the input energy. "
            "Conventional: fuel chemical energy &rarr; combustion (&times;50%) "
            "&rarr; transmission + shaft (&times;95%) "
            "&rarr; propeller open-water (&times;70%) &rarr; &approx;33% useful thrust. "
            "RIMT: battery electric &rarr; DC bus (&times;99%) "
            "&rarr; GaN PEM (&times;97%) "
            "&rarr; tile EDL (tile-boundary &eta; = 83%, WP &sect;4.4) "
            "&rarr; &approx;80% full-chain useful thrust (0.99&times;0.97&times;0.83). "
            "The WP &sect;4.4 headline &eta;&nbsp;&asymp;&nbsp;83% is the tile-boundary efficiency "
            "(electrical input to tile &rarr; useful thrust; DC bus and GaN PEM losses not included "
            "&mdash; see WP &sect;4.3 for boundary definition). Numbers rounded."
        ),
    ),
    5: _wrap_figure(
        5,
        _fig5_svg(),
        (
            "Modelled conversion efficiency &eta; (Model 3, &alpha; = 0.005, "
            "<em>f</em><sub>c</sub> = 2&thinsp;MHz, "
            "<em>v</em><sub>slip</sub> = 0.2&thinsp;m&thinsp;s<sup>&minus;1</sup>) "
            "vs. seawater conductivity &sigma;<sub>sw</sub>, spanning freshwater to open ocean "
            "(&sigma;&thinsp;&isin;&thinsp;[0.05,&thinsp;5]&thinsp;S&thinsp;m<sup>&minus;1</sup>). "
            "Ohmic heating (&prop;&thinsp;&sigma;<sup>&minus;1</sup>) dominates the power budget at "
            "low conductivity; efficiency falls from 84&thinsp;% at open-ocean salinity "
            "(&sigma;&thinsp;&asymp;&thinsp;5&thinsp;S&thinsp;m<sup>&minus;1</sup>, right shading) "
            "to &asymp;5&thinsp;% in freshwater "
            "(&sigma;&thinsp;=&thinsp;0.05&thinsp;S&thinsp;m<sup>&minus;1</sup>, left shading). "
            "A thinner dielectric (e.g., 100&thinsp;nm HfO<sub>2</sub>, &sect;5.2) raises EDL "
            "surface charge density and reduces the minimum <em>V</em><sub>drive</sub>, "
            "partially compensating but not eliminating the &sigma;<sup>&minus;1</sup> "
            "ohmic penalty. Red dot: &sect;3.5 design point "
            "(&sigma; = 4.8&thinsp;S&thinsp;m<sup>&minus;1</sup>)."
        ),
    ),
}


# ---------------------------------------------------------------------------
# MD update: replace content between <!-- FIGURE_N_START/END --> markers
# ---------------------------------------------------------------------------
def update_md(path: Path, n: int, content: str) -> bool:
    """Replace the block between FIGURE_N_START and FIGURE_N_END markers."""
    start_tag = f"<!-- FIGURE_{n}_START -->"
    end_tag   = f"<!-- FIGURE_{n}_END -->"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(start_tag) + r".*?" + re.escape(end_tag),
        re.DOTALL,
    )
    replacement = f"{start_tag}\n{content}\n{end_tag}"
    new_text, count = pattern.subn(replacement, text)
    if count == 0:
        print(f"  [WARN] Markers for Figure {n} not found in {path.name}")
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> int:
    errors = 0

    # 1. Write standalone SVG files
    for n, content in FIGURES.items():
        # Extract just the SVG part (strip <figure> wrapper)
        m = re.search(r"(<svg\b.*?</svg>)", content, re.DOTALL)
        if m:
            svg_path = THIS_DIR / f"fig-{n}.svg"
            svg_path.write_text(m.group(1) + "\n", encoding="utf-8")
            print(f"Written: {svg_path}")

    # 2. Update RIMT-whitepaper.md (Figures 1, 2, 3, 5)
    for n in (1, 2, 3, 5):
        ok = update_md(WP_MD, n, FIGURES[n])
        if ok:
            print(f"Updated: {WP_MD.name} Figure {n}")
        else:
            errors += 1

    # 3. Update comparison doc (Figure 1 = energy chain, reuses Figure 3 content)
    ok = update_md(COMP_MD, 1, FIGURES[3])
    if ok:
        print(f"Updated: {COMP_MD.name} Figure 1 (energy chain)")
    else:
        errors += 1

    if errors:
        print(f"\n  {errors} marker(s) not found -- check MD files for comment markers.")
        return 1
    print("\nAll figures generated and embedded successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
