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
    ├── test_rimt_simulation.py            Unit test suite (45 tests)
    └── requirements.txt                   Python dependencies
```

---

## Running the Simulations

Requires Python ≥ 3.9 and NumPy.

```bash
pip install -r simulations/requirements.txt
python simulations/rimt_simulation.py
```

Expected output (reference scenario: 10 m vessel, 30 m² hull, 10 m/s ≈ 19.4 knots). The transcript below is abridged; the live script prints longer labels and additional intermediate quantities (Debye length, surface charge density, wave-fluid slip, etc.):

```
Baseline (Model 2)              η =  3.0%   V_drive = 200.0 V
Optimised — Ta₂O₅ 500 nm (Model 3)  η = 83.0%   V_drive =   5.31 V
```

Run the test suite to verify correctness:

```bash
cd simulations
pytest test_rimt_simulation.py -v
```

All 45 tests should pass.

### Reproducibility

The simulation results above were obtained with the following toolchain (also encoded as `simulations/requirements.txt`):

- **Python** 3.12 (≥ 3.9 supported)
- **NumPy** ≥ 1.21 (any current 1.x or 2.x release)
- **pytest** ≥ 7 (for running the unit tests)
- **Operating system** Windows 11 (also tested transparently on Linux via CI-free containers)
- **Expected runtime** Under 1 second for the full `main()` run; under 1 second for the full 45-test pytest pass
- **Expected exact test count** 45 passed, 0 failed, 0 skipped

Headline numerical results (η = 3.0 % / 83.0 %, V_drive = 200.0 V / 5.31 V, Pe ≈ 65, v_w = 60 m/s) are deterministic — no random seeds are used in the model — and reproduce exactly bit-for-bit across the supported toolchain.

---

## Key Physics

| Quantity | Value | Significance |
|---|---|---|
| Debye length in seawater | κ⁻¹ ≈ 0.39 nm | EDL thickness at 0.6 M NaCl, 20°C |
| Operating frequency | 2–5 MHz | Faradaic-suppression band, below dielectric heating onset |
| Sawtooth waveform | t_r = 100 ns / t_f = 400 ns | 1:4 rise:fall asymmetry, period = 500 ns ⇒ f_c = 2 MHz |
| Sawtooth form factor | K = 2.5 | RMS shape factor at r = 0.2, used in j_rms = K·σ_surf·f |
| Péclet number | Pe ≈ 65 (ionic) | Electric-field ion transport dominates Brownian diffusion |
| Wave propagation speed | v_w = 60 m/s (≈ 117 knots) | Wave-pattern kinematic, not vessel speed; >> any vessel speed at f_c = 2 MHz, λ = 30 µm |
| Electrode geometry | w = 10 µm, g = 5 µm, λ = 30 µm | Finger width, inter-electrode gap, wavelength = 2(w+g) |
| Dielectric (optimised) | Ta₂O₅, 500 nm ALD | εr ≈ 20–25, pinhole-free |
| EDL coupling factor | α = 0.005 (Ta₂O₅) / 0.01 (Al₂O₃) | First-order coupling assumption between drive voltage and tangential EDL field |
| Wave–fluid slip | v_slip = 0.2 m/s (tuned) / 1.0 m/s (baseline) | Sets the viscous-loss component of efficiency |
| **Headline efficiency** | **η ≈ 83 % (tuned) / 3 % (baseline)** | First-order upper bounds; experimental validation pending |

---

## Novelty

Prior work on traveling-wave electro-osmosis (TWEO) is confined to microfluidic devices. Electro-osmotic thrusters for underwater vehicles have been demonstrated using DC-driven capillary arrays as point-source thrusters. RIMT is the first proposed system to apply MHz-frequency asymmetric traveling-wave potentials to a macroscopic hull-surface electrode array as a primary distributed propulsion mechanism.

See [Section 2 — Related Work](whitepaper/RIMT-whitepaper.md#2-related-work) for a full prior-art analysis with references.

---

## How to Cite

If you build on, extend, or refer to this work, please cite:

> Szabó, G. (2026). *Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer (RIMT)* [Technical Disclosure]. Zenodo. https://doi.org/10.5281/zenodo.20361267

BibTeX (using `@misc` per the convention for Zenodo deposits; an equivalent `@techreport` form is fine too if your bibliography style prefers it):
```bibtex
@misc{szabo2026rimt,
  author       = {Szabó, Gábor},
  title        = {Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer ({RIMT}):
                  Technical Disclosure \& Whitepaper},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.20361267},
  url          = {https://doi.org/10.5281/zenodo.20361267},
  note         = {Concept DOI; resolves to the latest version. CC BY-SA 4.0.}
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

This repository constitutes a **defensive publication**. All material herein is placed in the public domain as prior art under CC BY-SA 4.0, effective from the date of the Zenodo DOI assignment. Any patent application filed after that date that claims subject matter described in the whitepaper *may be anticipated* by this prior art. The defensive-publication mechanism depends on a patent examiner's diligence in locating and citing the prior art; final patentability determinations rest with individual patent offices and courts in each relevant jurisdiction. This notice records the author's intent that the design space be kept open; it is not a unilateral declaration of unpatentability.
