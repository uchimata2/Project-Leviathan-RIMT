# Project Leviathan — Solid-State Ionic Hull (SSIH)
### Resonant Ionic Momentum Transfer (RIMT): A Proposed Solid-State Marine Propulsion Architecture

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20361267.svg)](https://doi.org/10.5281/zenodo.20361267)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## What is RIMT?

RIMT proposes converting the entire wetted hull surface of a marine vessel into a distributed solid-state engine by manipulating the **Electrical Double Layer (EDL)** of seawater. A MHz-frequency asymmetric traveling-wave potential, applied via a sub-surface interdigitated electrode lattice and driven by GaN wide-bandgap power electronics, "ratchets" Na⁺/Cl⁻ ions along the hull. The viscous coupling of those ions to the surrounding water bulk generates forward thrust; the same boundary-layer manipulation is *hypothesised* to attenuate skin-friction drag, although the magnitude of that drag-reduction co-benefit is not quantified in this disclosure and is flagged in §6 as a key experimental question.

Operating in the **Faradaic-suppression band** (~2–5 MHz) inhibits electrolytic water splitting without magnetic infrastructure, distinguishing RIMT from both classical electro-osmotic thrusters and magnetohydrodynamic (MHD) drives.

**First-order computational models show:**

| Configuration | Dielectric | Drive | Slip (m/s) | Efficiency |
|---|---|---|---|---|
| Un-tuned baseline (Model 2) | Al₂O₃, 1 µm PECVD | 200 V fixed | 1.0 | **η ≈ 3%** (ohmic-loss dominated) |
| Optimised (Model 3) | Ta₂O₅, 500 nm ALD | 5.3 V tuned | 0.2 | **η ≈ 83%** (above the ~70–72% propeller ceiling) |

*Both numbers are first-order upper bounds under the §3.3 asymmetric sawtooth waveform; experimental validation is pending. The 3% baseline illustrates that fixed-voltage drive on a thick low-k dielectric is non-viable — adaptive voltage control is essential. No laboratory prototype has been built. See [Limitations](whitepaper/RIMT-whitepaper.md#6-limitations-and-future-work).*

---

## Repository Contents

```
Project-Leviathan-RIMT/
├── README.md                              This file
├── whitepaper/
│   ├── RIMT-whitepaper.md                 Full technical disclosure (Markdown)
│   ├── RIMT-whitepaper.html               Print-ready HTML (MathJax)
│   ├── RIMT-whitepaper.pdf                PDF export for citation and archival
│   └── export_html.py                     Markdown → HTML converter (all docs)
├── comparison/
│   ├── RIMT-vs-conventional-comparison.md Companion: 15-table side-by-side
│   │                                      comparison vs. conventional marine
│   │                                      propulsion, with application landscape
│   │                                      and quantitative scorecard
│   ├── RIMT-infographic-data.md           Structured data spec + canonical
│   │                                      `json` block (single source of truth
│   │                                      for the interactive page below)
│   ├── RIMT-infographic.html              **Interactive infographic** (ECharts
│   │                                      + GSAP + AOS, self-contained) — open
│   │                                      in a browser; sponsor / decision-maker
│   │                                      facing
│   └── build_infographic.py               Converter: reads the `json` block
│                                          from RIMT-infographic-data.md →
│                                          renders RIMT-infographic.html
└── simulations/
    ├── rimt_simulation.py                 Three first-order analytical models
    ├── test_rimt_simulation.py            Unit test suite (42 tests)
    └── requirements.txt                   Python dependencies
```

---

## Running the Simulations

Requires Python ≥ 3.9 and NumPy.

```bash
pip install -r simulations/requirements.txt
python simulations/rimt_simulation.py
```

Expected output (reference scenario: 10 m vessel, 30 m² hull, 20 knots):

```
Model 2 — Baseline:   η =  3.0%   V_drive = 200.0 V
Model 3 — Optimised:  η = 83.0%   V_drive =   5.31 V
```

Run the test suite to verify correctness:

```bash
cd simulations
pytest test_rimt_simulation.py -v
```

All 42 tests should pass.

---

## Key Physics

| Quantity | Value | Significance |
|---|---|---|
| Debye length in seawater | κ⁻¹ ≈ 0.39 nm | EDL thickness at 0.6 M NaCl, 20°C |
| Operating frequency | 2–5 MHz | Faradaic-suppression band, below dielectric heating onset |
| Sawtooth waveform | t_r = 100 ns / t_f = 400 ns | 1:4 rise:fall asymmetry, period = 500 ns ⇒ f_c = 2 MHz |
| Péclet number | Pe ≈ 65 (ionic) | Electric-field ion transport dominates Brownian diffusion |
| Wave propagation speed | v_w = 60 m/s (≈ 117 knots) | >> any vessel speed at f_c = 2 MHz, λ = 30 µm |
| Electrode geometry | w = 10 µm, g = 5 µm, λ = 30 µm | Finger width, inter-electrode gap, wavelength = 2(w+g) |
| Dielectric (optimised) | Ta₂O₅, 500 nm ALD | εr ≈ 20–25, pinhole-free |

---

## Novelty

Prior work on traveling-wave electro-osmosis (TWEO) is confined to microfluidic devices. Electro-osmotic thrusters for underwater vehicles have been demonstrated using DC-driven capillary arrays as point-source thrusters. RIMT is the first proposed system to apply MHz-frequency asymmetric traveling-wave potentials to a macroscopic hull-surface electrode array as a primary distributed propulsion mechanism.

See [Section 2 — Related Work](whitepaper/RIMT-whitepaper.md#2-related-work) for a full prior-art analysis with references.

---

## How to Cite

If you build on, extend, or refer to this work, please cite:

> Szabó, G. (2026). *Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer (RIMT)* [Technical Disclosure]. Zenodo. https://doi.org/10.5281/zenodo.20361267

BibTeX:
```bibtex
@techreport{szabo2026rimt,
  author      = {Szabó, Gábor},
  title       = {Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer ({RIMT})},
  year        = {2026},
  institution = {Zenodo},
  type        = {Technical Disclosure},
  doi         = {10.5281/zenodo.20361267},
  url         = {https://doi.org/10.5281/zenodo.20361267}
}
```

*The DOI above is the **concept DOI** — it always resolves to the latest version on Zenodo.*

---

## Author

**Gábor Szabó** (sole author, concept originator)

*AI research assistance acknowledged in the whitepaper Acknowledgments: Google Gemini, Claude (Anthropic). Per standard academic authorship norms, AI tools are not listed as authors.*

---

## License

This work is released under the **Creative Commons Attribution-ShareAlike 4.0 International License** ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).

You are free to share and adapt this material for any purpose, provided you give appropriate credit and distribute any derivatives under the same license.

---

## Defensive Publication Notice

This repository constitutes a **defensive publication**. All material herein is placed in the public domain as prior art under CC BY-SA 4.0, effective from the date of the Zenodo DOI assignment. Any patent application filed after that date that covers the RIMT/SSIH architecture as described in the whitepaper is anticipated by this prior art.
