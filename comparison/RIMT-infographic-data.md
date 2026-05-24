# RIMT Infographic Data Package

**Purpose.** This file is a structured data feed for visualisation tools (Napkin, Canva, Adobe Express, Visme, an LLM with image generation, etc.). It contains the headline pitch, hero numbers, before/after panels, application matrix, build path, and call-to-action that would form a single-page infographic aimed at **decision makers, manufacturers, and potential R&D sponsors** — not a consumer-marketing piece.

**Companion to:**
- Full whitepaper: [`whitepaper/RIMT-whitepaper.md`](../whitepaper/RIMT-whitepaper.md)
- Detailed comparison: [`comparison/RIMT-vs-conventional-comparison.md`](RIMT-vs-conventional-comparison.md)

**Author / originator:** Gábor Szabó<br>
**Licence:** CC BY-SA 4.0 — use freely, share back any derivatives.

---

## 1. Headline pitch (one sentence)

> A solid-state marine engine that turns the entire wetted hull into a silent, distributed propulsor — no spinning propeller, no combustion, no fuel onboard.

**Sub-line (one line):** First-order analytical concept, TRL 2; published as a defensive disclosure to keep the technology open for any builder to validate.

## 2. Hero numbers (five tiles)

Use as five large numerical tiles in a horizontal strip at the top of the infographic.

| Number | Label | Source |
|---|---|---|
| **83 %** | First-order modelled wall-plug efficiency (electrical input to useful thrust) | RIMT whitepaper §4.4 (Model 3, optimised) |
| **0** | Moving parts in the propulsion path | RIMT design (whitepaper §3) |
| **$30 B / yr** | Annual cost of propeller biofouling to global shipping today — would be largely eliminated if RIMT's antifouling co-benefit holds | Comparison ref [10] |
| **~ 3 %** | Share of global CO₂ from international shipping today, with IMO target of net-zero by ≈ 2050 | Comparison refs [1, 3] |
| **2026** | Year MEPC 85 decides whether IMO underwater-noise rules become mandatory | Comparison refs [5, 6] |

## 3. Before / After (four-panel comparison)

Render as four side-by-side icon pairs (conventional ← → RIMT).

| Aspect | Conventional today | RIMT if validated |
|---|---|---|
| **Direct emissions** | CO₂, NOₓ, SOₓ, PM, oil-spill risk | Zero direct |
| **Underwater noise** | 180+ dB monopole source, dominated by propeller cavitation | Hull-flow noise of the displacement hull alone |
| **Moving parts** | Hundreds to thousands per drivetrain | Zero in the propulsion path |
| **Propeller strikes on marine life** | Tens to hundreds of large cetaceans killed annually in shipping lanes; recreational injuries to swimmers and pinnipeds | Eliminated — no external rotating element |

## 4. Where it shines (five application tiles)

Five cards, each one hero application drawn from the broader Application Landscape in the comparison document.

1. **Stealth UUVs (defence).** Silent, low-signature, no cavitation. The likely first hardware validation venue — small craft, accepted risk envelope, customer willing to pay technology-development premiums.
2. **Whale-watching and cetacean research.** Removes the operator's own contribution to the disturbance regulations are tightening to limit.
3. **Inland-waterway and canal boats.** Zero emissions and low noise in urban-canal contexts where diesel is increasingly restricted.
4. **Harbour tugs and pilot boats.** High duty cycle amortises CAPEX premium fastest; ports already mandating shore-power and zero local emissions.
5. **RC boats and educational kits.** Lowest-stakes first consumer demonstration of the principle; visible electrokinetic effect makes a strong STEM teaching tool.

*(Full application landscape with six sectors and ~30 entries lives in the comparison document.)*

## 5. Build path (call-to-action panel)

A small staircase chart of milestones, illustrating that early validation is **cheap on the scale of marine R&D**.

| Milestone | Indicative scale | Indicative cumulative spend |
|---|---|---|
| Bench-top ionic plate (10 × 10 cm tile) | University / hobbyist lab | $50 k |
| Torsion-balance thrust measurement; first η, drag, fouling data | 1-person team × 6 months | $0.2 M |
| 1 m² tile in a saltwater tank | Small applied-research project | $1 M |
| 3 m sub-scale vessel demonstrator | Research consortium | $5 M |
| 10 m in-water vessel demonstrator | Industry / national programme | $20 M |

All figures are order-of-magnitude planning estimates, not committed costs. Detail in the comparison document's Figure 5 specification.

## 6. The honest caveat (one paragraph, bottom)

> RIMT is a **first-order analytical concept at TRL 2**. No laboratory prototype has been built. The figures shown are *modelled upper bounds under stated idealisations* — not measurements. Realistic performance must be set by experiment. The work is published under **CC BY-SA 4.0** as a defensive disclosure: any individual, university, company, or research consortium is free to build, modify, and benefit from the technology, with the only obligation being attribution and same-licence sharing of derivative work.

## 7. Where to find more

- **DOI (concept, always-latest):** [`10.5281/zenodo.20361267`](https://doi.org/10.5281/zenodo.20361267)
- **GitHub repository:** [uchimata2/Project-Leviathan-RIMT](https://github.com/uchimata2/Project-Leviathan-RIMT)
- **Whitepaper:** [`whitepaper/RIMT-whitepaper.md`](../whitepaper/RIMT-whitepaper.md)
- **Detailed comparison:** [`comparison/RIMT-vs-conventional-comparison.md`](RIMT-vs-conventional-comparison.md)
- **Open-source simulation (42 unit tests passing):** [`simulations/rimt_simulation.py`](../simulations/rimt_simulation.py)

---

## 8. Suggested layout for the rendering tool

A single A3 (or 2× US-letter) portrait page. Top to bottom:

| Band | Height | Content |
|---|:---:|---|
| Header | 10 % | Title: "RIMT — A Silent Solid-State Marine Engine." Sub-title: the one-sentence headline pitch (Section 1). |
| Hero numbers | 15 % | Five large numerical tiles from Section 2 in a horizontal strip. |
| Before / After | 20 % | Four pairs of side-by-side icons + short labels from Section 3. |
| Where it shines | 25 % | Five vertical cards from Section 4, each with a small representative icon. |
| Build path | 15 % | Horizontal staircase / timeline of the milestones in Section 5. |
| Caveat band | 5 % | The paragraph from Section 6 in muted but clearly legible type. |
| Footer | 10 % | DOI badge, GitHub link, CC BY-SA 4.0 badge, attribution to Gábor Szabó. |

### Visual style direction

- **Palette.** Deep navy backgrounds; lighter teal for RIMT "modelled" data; light grey for conventional "today" data; a single warm accent (amber) for hero numbers and the call-to-action panel. The point is decision-maker clarity, not boat-show flash.
- **Typography.** Sans-serif (Inter, IBM Plex Sans, or similar) for numerical tiles; serif optional for the headline pitch and caveat paragraph for readability.
- **Iconography.** Geometric, flat, monochrome within each panel; avoid skeuomorphic boat/propeller clip-art.
- **Tone.** Factual throughout. The cumulative effect should be: *"this would be worth a bench-test grant,"* not *"buy this now."* Resist marketing-language temptation; the numbers do the work.

---

## 9. Optional supporting visuals (if a multi-page deck rather than a single sheet)

If the audience wants a 3–4 page slide deck instead of a one-sheet, include also:

1. **Side-by-side energy-conversion chain** (Figure 1 from the comparison document's Appendix B).
2. **20-axis radar chart of the scorecard** (Figure 2 from the comparison document's Appendix B).
3. **CO₂ reduction sensitivity chart** (Figure 4 from the comparison document's Appendix B).
4. **Underwater acoustic-signature comparison curve** (Figure 6 from the comparison document's Appendix B).

These are the highest-value supporting graphics if more than one page is on the table.

---

## 10. Canonical machine-readable data (for `build_infographic.py`)

The fenced `json` block below is the **single source of truth** consumed by `build_infographic.py` to render the interactive HTML at `RIMT-infographic.html`. Prose sections 1–9 above are for human readers; the JSON block is for the renderer.

Every numerical claim carries a `source` field pointing at its canonical location (whitepaper section, comparison-document section, or external reference number). If a source value in the WP or the comparison document changes, the corresponding field here must be updated in lockstep — see the `project-rimt-data-sync-registry` memory for the full cross-document data invariant list.

```json
{
  "schema_version": "1.0",
  "doc_meta": {
    "title": "RIMT — A Silent Solid-State Marine Engine",
    "headline": "A solid-state marine engine that turns the entire wetted hull into a silent, distributed propulsor — no spinning propeller, no combustion, no fuel onboard.",
    "subtitle": "First-order analytical concept, TRL 2. Published as a defensive disclosure under CC BY-SA 4.0 so any builder can validate it.",
    "author": "Gábor Szabó",
    "license": "CC BY-SA 4.0 International",
    "doi_placeholder": "10.5281/zenodo.20361267",
    "source": "WP §1, Comparison Executive Summary"
  },
  "hero_numbers": [
    {
      "value": 83,
      "counter_from": 0,
      "unit_suffix": " %",
      "label": "First-order modelled wall-plug efficiency (electrical input to useful thrust)",
      "source": "WP §4.4 (Model 3, optimised)"
    },
    {
      "value": 0,
      "counter_from": 0,
      "unit_suffix": "",
      "label": "Moving parts in the propulsion path",
      "source": "WP §3"
    },
    {
      "value": 30,
      "counter_from": 0,
      "unit_prefix": "$",
      "unit_suffix": "B / yr",
      "label": "Annual biofouling cost to global shipping today — eliminated if RIMT's antifouling co-benefit holds",
      "source": "Comparison ref [10]"
    },
    {
      "value": 3,
      "display_override": "~3",
      "unit_suffix": " %",
      "label": "Share of global CO₂ from international shipping today (IMO target: net-zero by ≈ 2050)",
      "source": "Comparison refs [1, 3]"
    },
    {
      "value": 2026,
      "counter_from": 2020,
      "unit_suffix": "",
      "label": "Year MEPC 85 decides whether IMO underwater-noise rules become mandatory",
      "source": "Comparison refs [5, 6]"
    }
  ],
  "before_after": [
    {
      "aspect": "Direct emissions",
      "conventional": "CO₂, NOₓ, SOₓ, PM, oil-spill risk",
      "rimt": "Zero direct",
      "source": "Comparison §6"
    },
    {
      "aspect": "Underwater noise",
      "conventional": "180+ dB monopole source, dominated by propeller cavitation",
      "rimt": "Hull-flow noise of the displacement hull alone",
      "source": "Comparison §6 + refs [7, 8]"
    },
    {
      "aspect": "Moving parts",
      "conventional": "Hundreds to thousands per drivetrain",
      "rimt": "Zero in the propulsion path",
      "source": "Comparison §5"
    },
    {
      "aspect": "Strikes on marine life",
      "conventional": "Tens to hundreds of large cetaceans killed annually in shipping lanes; recreational injuries to swimmers and pinnipeds",
      "rimt": "Eliminated — no external rotating element",
      "source": "Comparison §6"
    }
  ],
  "where_it_shines": [
    {
      "title": "Stealth UUVs (defence)",
      "summary": "Silent, low-signature, no cavitation.",
      "detail": "Small craft, accepted risk envelope, customer willing to pay technology-development premiums. The likely first hardware validation venue — closest prior art (Hansen et al. 2020) already demonstrated electro-osmotic vehicle propulsion at UUV scale.",
      "source": "Comparison §13 + Application Landscape §Defence"
    },
    {
      "title": "Whale-watching and cetacean research",
      "summary": "Removes the operator's contribution to disturbance.",
      "detail": "Acoustic stealth removes the operator's own contribution to the disturbance regulations are tightening to limit. For research vessels, also removes the dominant source of self-induced acoustic interference in passive-sonar studies.",
      "source": "Application Landscape §Marine science"
    },
    {
      "title": "Inland-waterway and canal boats",
      "summary": "Zero emissions and low noise in urban canals.",
      "detail": "Diesel is increasingly restricted in urban-canal contexts where the boat moves slowly through residential areas. Shallow draft is a structural advantage on inland waterways. Small fleets, regional regulation — a plausible near-term entry market.",
      "source": "Application Landscape §Commercial"
    },
    {
      "title": "Harbour tugs and pilot boats",
      "summary": "High duty cycle amortises CAPEX premium fastest.",
      "detail": "Ports already mandating shore-power and zero local emissions; high utilisation (4 000 + hours/year) means the OPEX advantage compounds quickly. The structural advantage of the no-moving-parts maintenance profile is felt most strongly here.",
      "source": "Application Landscape §Commercial + Where RIMT could win"
    },
    {
      "title": "RC boats and educational kits",
      "summary": "Lowest-stakes consumer demonstration.",
      "detail": "No propeller-blade injury risk to children, no fuel, silent operation. The educational appeal of a visible electrokinetic effect is intrinsic — currently a microfluidics-lab exercise, a tabletop ionic boat makes it tangible.",
      "source": "Application Landscape §Hobby"
    }
  ],
  "build_path": [
    {"year": 0, "milestone": "Bench-top ionic plate (10 × 10 cm tile)", "scale": "University / hobbyist lab", "spend_usd_m": 0.05},
    {"year": 1, "milestone": "Torsion-balance thrust measurement; first η, drag, fouling data", "scale": "1-person team × 6 months", "spend_usd_m": 0.2},
    {"year": 2, "milestone": "1 m² tile in a saltwater tank", "scale": "Small applied-research project", "spend_usd_m": 1},
    {"year": 3, "milestone": "Sub-scale vessel demonstrator (~ 3 m)", "scale": "Research consortium", "spend_usd_m": 5},
    {"year": 5, "milestone": "In-water vessel demonstrator (~ 10 m)", "scale": "Industry / national programme", "spend_usd_m": 20},
    {"year": 8, "milestone": "Class-society pilot (small commercial craft)", "scale": "National programme / consortium", "spend_usd_m": 80}
  ],
  "caveat": "RIMT is a first-order analytical concept at TRL 2. No laboratory prototype has been built. The figures shown are modelled upper bounds under stated idealisations — not measurements. Realistic performance must be set by experiment. Published under CC BY-SA 4.0 as a defensive disclosure: any individual, university, company, or research consortium is free to build, modify, and benefit from the technology, with the only obligation being attribution and same-licence sharing of derivative work.",
  "figures": {
    "energy_chain": {
      "title": "Energy conversion chain: conventional vs. RIMT",
      "caption": "Same input (1 unit of primary energy) tracked through each stack. Each stage shows the percentage retained after losses; the final value is useful thrust delivered.",
      "conventional": {
        "stages": [
          {"label": "Fuel chemical energy", "retained": 100},
          {"label": "Combustion (~50 % heat loss)", "retained": 50},
          {"label": "Transmission + shaft (~95 %)", "retained": 47.5},
          {"label": "Propeller open-water (~70 %)", "retained": 33}
        ]
      },
      "rimt": {
        "stages": [
          {"label": "Battery electric energy", "retained": 100},
          {"label": "DC bus (~99 %)", "retained": 99},
          {"label": "GaN PEM AC synthesis (~97 %)", "retained": 96},
          {"label": "EDL coupling + ohmic + viscous", "retained": 83}
        ]
      },
      "source": "WP §4.4, Comparison §1 + §2, Comparison Appendix B Figure 1"
    },
    "scorecard_radar": {
      "title": "Quantitative scorecard — RIMT (modelled) vs. conventional",
      "caption": "20 axes scored on the qualitative −−/−/0/+/++ rubric (1–5). RIMT scores reflect modelled design targets, not measurements.",
      "axes": [
        {"name": "Physics novelty", "conventional": 3, "rimt": 5},
        {"name": "Efficiency", "conventional": 4, "rimt": 5},
        {"name": "OPEX", "conventional": 2, "rimt": 4},
        {"name": "CAPEX", "conventional": 4, "rimt": 2},
        {"name": "Mfg maturity", "conventional": 5, "rimt": 2},
        {"name": "Mech. complexity", "conventional": 2, "rimt": 5},
        {"name": "SW complexity", "conventional": 3, "rimt": 2},
        {"name": "Emissions", "conventional": 1, "rimt": 5},
        {"name": "Logistics: fuel", "conventional": 2, "rimt": 4},
        {"name": "Logistics: range", "conventional": 5, "rimt": 2},
        {"name": "Usability", "conventional": 3, "rimt": 4},
        {"name": "Safety: fire/strike", "conventional": 2, "rimt": 5},
        {"name": "Safety: electrical", "conventional": 4, "rimt": 3},
        {"name": "Maintenance", "conventional": 2, "rimt": 4},
        {"name": "Regulatory", "conventional": 2, "rimt": 4},
        {"name": "Shallow water", "conventional": 3, "rimt": 5},
        {"name": "Freshwater", "conventional": 4, "rimt": 2},
        {"name": "Scalability", "conventional": 4, "rimt": 4},
        {"name": "Market position", "conventional": 5, "rimt": 2},
        {"name": "TRL", "conventional": 5, "rimt": 1}
      ],
      "source": "Comparison Quantitative Scorecard"
    },
    "application_quadrant": {
      "title": "Application landscape — natural early adopters",
      "caption": "Upper-right cluster = high RIMT value × high customer risk tolerance. Lower-left = harder near-term targets.",
      "axis_x_label": "Value of RIMT's unique properties (acoustic stealth + zero-draft + zero-emission)",
      "axis_y_label": "Risk tolerance of typical early customer",
      "points": [
        {"name": "RC boat", "x": 4, "y": 10, "category": "hobby"},
        {"name": "Pool cleaner", "x": 5, "y": 9, "category": "hobby"},
        {"name": "Aquarium pump", "x": 4, "y": 9, "category": "hobby"},
        {"name": "STEM education kit", "x": 3, "y": 9, "category": "hobby"},
        {"name": "Sailing-yacht auxiliary", "x": 6, "y": 8, "category": "recreational"},
        {"name": "Marine-reserve ranger boat", "x": 8, "y": 7, "category": "conservation"},
        {"name": "Whale-watching tour boat", "x": 9, "y": 6, "category": "conservation"},
        {"name": "Inland canal boat", "x": 7, "y": 6, "category": "commercial"},
        {"name": "Small naval UUV", "x": 10, "y": 5, "category": "defence"},
        {"name": "Cetacean research vessel", "x": 9, "y": 4, "category": "conservation"},
        {"name": "Harbour tug", "x": 7, "y": 3, "category": "commercial"},
        {"name": "Urban passenger ferry", "x": 8, "y": 3, "category": "commercial"},
        {"name": "Container ship", "x": 4, "y": 1, "category": "commercial"},
        {"name": "Attack submarine", "x": 10, "y": 1, "category": "defence"}
      ],
      "source": "Comparison Appendix B Figure 3"
    },
    "co2_sensitivity": {
      "title": "Shipping CO₂ — adoption sensitivity (illustrative)",
      "caption": "Hypothetical RIMT-fleet adoption against the IMO net-zero trajectory. Adoption percentages are sensitivity-analysis stand-ins, not forecasts. RIMT share assumes pairing with renewable grid electricity.",
      "years": [2025, 2030, 2035, 2040, 2045, 2050],
      "baseline_gt_co2": [1.05, 1.05, 1.05, 1.05, 1.05, 1.05],
      "imo_target_gt_co2": [1.05, 0.84, 0.55, 0.25, 0.10, 0],
      "rimt_share_pct": [0, 0, 5, 20, 35, 50],
      "source": "Comparison refs [1, 3] + Comparison Appendix B Figure 4"
    },
    "trl_pathway": {
      "title": "TRL pathway — cost to validate",
      "caption": "Order-of-magnitude planning estimates. Each milestone embeds an experimental work package listed in WP §6.",
      "milestones": [
        {"year": 0, "milestone": "Bench-top ionic plate", "spend_usd_m": 0.05},
        {"year": 1, "milestone": "Torsion-balance thrust", "spend_usd_m": 0.2},
        {"year": 2, "milestone": "1 m² tile, tank", "spend_usd_m": 1},
        {"year": 3, "milestone": "3 m demonstrator", "spend_usd_m": 5},
        {"year": 5, "milestone": "10 m demonstrator", "spend_usd_m": 20},
        {"year": 8, "milestone": "Class-society pilot", "spend_usd_m": 80}
      ],
      "source": "Comparison Appendix B Figure 5"
    },
    "acoustic_spectrum": {
      "title": "Underwater acoustic signature comparison",
      "caption": "Projected RIMT spectrum is derived from the source-elimination argument, not measurement. Container-ship curve is after [7, 8]. Whale-vocalisation bands shown for context.",
      "freq_hz": [10, 31, 100, 316, 1000, 3162, 10000, 31623, 100000],
      "container_ship_db": [180, 178, 170, 155, 140, 135, 132, 130, 130],
      "electric_small_vessel_db": [130, 128, 125, 120, 115, 112, 110, 108, 108],
      "rimt_projected_db": [110, 108, 105, 100, 95, 92, 90, 88, 88],
      "whale_bands": [
        {"name": "Blue whale", "min_hz": 10, "max_hz": 40},
        {"name": "Humpback", "min_hz": 30, "max_hz": 8000},
        {"name": "Killer whale", "min_hz": 500, "max_hz": 40000},
        {"name": "Sperm whale clicks", "min_hz": 5000, "max_hz": 25000}
      ],
      "source": "Comparison refs [7, 8] + Comparison Appendix B Figure 6"
    }
  },
  "links": {
    "whitepaper": "../whitepaper/RIMT-whitepaper.html",
    "comparison": "RIMT-vs-conventional-comparison.html",
    "simulation": "../simulations/rimt_simulation.py",
    "github": "https://github.com/uchimata2/Project-Leviathan-RIMT",
    "doi": "https://doi.org/10.5281/zenodo.20361267"
  }
}
```

---

*Generated as supporting material for the RIMT Technical Disclosure, CC BY-SA 4.0 · Project Leviathan · DOI: [10.5281/zenodo.20361267](https://doi.org/10.5281/zenodo.20361267) (concept, always-latest)*
