# Conventional Marine Propulsion vs. Resonant Ionic Momentum Transfer (RIMT)
## A Side-by-Side Comparative Analysis

**Companion document to:** *Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer (RIMT) — Technical Disclosure & Whitepaper*<br>
**Author:** Gábor Szabó<br>
**Date:** 2026-05-25<br>
**Version:** 1.1<br>
**License:** CC BY-SA 4.0 International

---

## Reader's note

This document compares an **established, empirically characterised technology** (conventional internal-combustion and electric marine propulsion) against a **proposed, theoretically analysed concept** (RIMT). The asymmetry is intentional and unavoidable: conventional propulsion has more than 150 years of operating data, classification-society rule sets, and component supply chains. RIMT exists as first-order analytical models and an open technical disclosure, with no laboratory prototype yet. All RIMT figures should be read as *design-target or first-order upper bound* rather than measured performance. The whitepaper's §6 ("Limitations and Future Work") enumerates what remains experimentally open.

The aim is not to declare a winner. It is to give a reader who already understands conventional marine propulsion a structured framework for evaluating where RIMT could win, where it must close gaps, and where conventional engineering retains decisive advantages.

Throughout, references in `[brackets]` point to the bibliography at the end. References to the whitepaper use the form `WP §X.Y`.

---

## Executive Summary

Conventional marine propulsion — overwhelmingly diesel-mechanical, with growing electric and hybrid variants — is a mature, regulated, and commoditised industry. A modern slow-speed two-stroke marine diesel reaches ~50 % brake thermal efficiency [13]; its open-water propeller adds another 55–70 % conversion to thrust [4]; hull resistance, drivetrain losses, and biofouling drop the wake-to-water number further. End-to-end fuel-energy-to-useful-thrust efficiency for a clean, well-trimmed merchant ship sits in the 25–35 % band, and biofouling alone is documented to cost the global industry on the order of $30 billion annually in extra fuel [10]. Underwater noise and CO₂ emissions are under increasing regulatory pressure: the IMO's 2023 Revised GHG Strategy targets net-zero shipping by or around 2050, with binding interim cuts in 2030 and 2040 [1, 3]; underwater radiated noise guidelines exit their Experience Building Phase at MEPC 85 in 2026, with mandatory measures on the table [5, 6].

RIMT proposes an entirely different mechanism: a MHz-frequency asymmetric traveling-wave potential applied across a hull-embedded micro-electrode lattice manipulates the Electrical Double Layer (EDL) of seawater, converting the entire wetted hull into a distributed solid-state actuator with no moving parts (WP §1.3, §3). First-order modelling places the optimised configuration at tile-boundary η ≈ 83 % (first-order upper bound; WP §4.4; DC bus and GaN PEM losses not included; full chain ≈ 80 %) versus a non-viable fixed-voltage baseline at η ≈ 3 %, and identifies adaptive voltage control as the dominant lever. If — and it remains a substantial *if* — laboratory validation reproduces even the lower half of this range under realistic seawater, fouling, and turbulence conditions, RIMT could in principle address several of the regulatory and ecological pressures facing conventional propulsion: it has no combustion, no propeller, no acoustic signature from rotating machinery, and no minimum draft.

The structured comparison below covers 15 categories. RIMT's strengths cluster around environmental, regulatory, mechanical-simplicity, and safety axes; its weaknesses are concentrated in three areas: (i) technology readiness (TRL 2 vs. TRL 9 — first-order theory vs. fielded systems), (ii) production maturity (sub-15 µm flexible-substrate lithography and large-area ALD are emerging industrial processes, not catalogue marine-supply items), and (iii) operational envelope at low salinity (freshwater performance is reduced by the same physics that makes the system work in seawater). The document closes with a quantitative scorecard, a "where RIMT could win" narrative, and a "where conventional wins" narrative.

---

## Comparison Tables

### 1. Operating principle and physics

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Energy conversion chain | Chemical (fuel) → thermal (combustion) → mechanical (crankshaft) → rotational (shaft) → hydrodynamic (propeller) → thrust. Each stage is loss-bearing. | Electrical (DC bus) → high-frequency AC (GaN PEM) → tangential electric field across EDL → directed ion drift → viscous coupling to bulk water → thrust (WP §3.3, §4). |
| Thrust generation mechanism | Point-source: a rotating screw accelerates a column of water aft, generating Newtonian reaction force. Local cavitation and tip vortices set the practical ceiling. | Distributed: every cm² of hull surface acts as a momentum source. No vortex shedding, no cavitation, no minimum local flow velocity required (WP §1.3, §7). Cooling design must accommodate stationary-vessel operation, since the only thermal sink for the GaN PEMs at zero vessel speed is conductive heat flow to still water through the hull. |
| Working-fluid interaction | The fluid is accelerated in bulk through a discrete actuator (propeller, waterjet). | The fluid's existing ion population is "ratcheted" along the hull within the Debye layer; bulk water moves via viscous coupling from the ion sheath outward (WP §1.3, §4.1). |
| Frequency / time-scale | Shaft RPM ranges from ~100 rpm (large two-stroke) to ~6 000 rpm (high-speed outboard). | Carrier frequency 2–5 MHz; full traveling-wave period 500 ns; rise:fall asymmetry 1:4 (WP §3.3). |
| Underlying physical theory | Froude–Rankine momentum theory of propellers; Bernoulli/energy balance; cavitation criteria; viscous boundary-layer theory. | Smoluchowski electro-osmotic flow; Debye–Hückel EDL theory; induced-charge traveling-wave electro-osmosis (IC-TWEO) [WP refs 1, 3, 4, 5]. |
| Theoretical efficiency ceiling | Propeller open-water efficiency limited to ~70–77 % under ideal load; the same hull has 25–35 % well-to-wake when fuel-to-shaft losses are included [4, 13]. | First-order upper bound tile-boundary η ≈ 83 % (electrical input to tile → useful thrust; DC bus and GaN PEM losses not included — see WP §4.3 boundary definition) for the optimised configuration at the assumed phenomenological coupling factor α = 0.005 (WP §4.4, §4.4.1 sensitivity table); full battery-to-thrust chain ≈ 80 %; realised efficiency requires experimental confirmation of α on the proposed Ta₂O₅ stack. |

### 2. Performance

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Propulsive efficiency (wake-to-water, hull-clean) | ~55–77 % open-water propeller efficiency; ~70–72 % practical ceiling on optimised commercial vessels (Carlton 2018; [4]). | Modelled tile-boundary η ≈ 83 % at the assumed coupling α = 0.005 (WP §4.4, Model 3, tuned; DC bus and GaN PEM losses not included — see WP §4.3 boundary definition); WP §4.4.1 reports the sensitivity band η ≈ 52–96 % across the literature-plausible range α ∈ [0.001, 0.05]. Baseline (Model 2, fixed 200 V, 1 µm Al₂O₃) is η ≈ 3 % — demonstrates that adaptive voltage matching is essential. |
| Total wall-plug or fuel-to-thrust efficiency | Two-stroke diesel: ~50 % brake thermal × ~70 % propeller × ~95 % transmission ≈ 33 % at design load [4, 13]. Four-stroke and high-speed engines fall to 25 % or below. | Modelled tile-boundary η ≈ 83 % (WP §4.4 Model 3; EDL electrical input to tile → useful thrust; DC bus and GaN PEM losses not included); full battery-to-thrust chain ≈ 0.99 × 0.97 × 0.83 ≈ 80 %; on a battery-electric vessel the upstream charging chain (~92 % grid → ~95 % battery round-trip) reduces well-to-wake by a further ~10 %. |
| Thrust density | ~10⁴–10⁵ N/m² at the propeller disk, integrated over a fraction of a percent of hull area. | Design target 50 N/m² distributed across the full wetted hull (WP §4.4); for a 30 m² hull this gives 1 500 N total thrust at the §4.4 design point. |
| Top speed | Routine 12–25 knots commercial; planing recreational craft 30–60 knots; high-performance jets >60 knots. | The wave-pattern propagation speed v_w = 60 m/s ≈ 117 knots (WP §3.3) substantially exceeds any conceivable vessel speed, so the actuator is not the speed-limiting element. Vessel top speed is set by hull-form drag and onboard electrical power, not the RIMT mechanism. (v_w is a wave kinematic, not a vessel-speed claim.) |
| Low-speed maneuverability | Propellers below ~30 % design RPM lose efficiency steeply (down to ~40 %); rudders need flow to be effective; bow thrusters are added complexity. | Thrust direction is electronically reversible by inverting the electrode phase sequence; differential tile activation provides yaw/sway authority without rudders or thrusters (WP §3.3). |
| Acceleration / response time | Throttle-up-to-thrust latency seconds to tens of seconds (engine speed-up, shaft inertia, prop wash establishment). | Electronic; full thrust reversal within carrier-frequency time scales (microseconds), constrained in practice by DC bus dynamics and crew safety (WP §3.3, §3.4). |
| Reversibility | Reverse gear or controllable-pitch propeller; mechanical complexity scales with ship size. | Phase-sequence inversion; no mechanical reverse gear. |
| Sensitivity to fouled hull | Severe: documented up to 40 % fuel penalty (industry-wide ~$30B/yr) and up to 55 % emissions increase [10]. | Fouling layer attenuates EDL coupling (acts as added dielectric thickness, WP §5.1); MHz-range AC field is hypothesised to suppress early-stage protein adsorption and bacterial adhesion, but this requires experimental validation. |

### 3. Economics

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| CAPEX, mid-range 20 m vessel | Engine alone $20k–$120k+ per unit, plus shaft, prop, gearbox, controls; installed package typically $50k–$120k [2]. | No verified BOM yet; whitepaper plausibility estimate $\mathcal{O}(10^5)$ USD at volume maturity (WP §6) is contingent on (i) sub-15 µm flexible-substrate lithography and (ii) large-area ALD reaching catalogue-marine readiness. First-of-kind prototype installations would be substantially higher. |
| CAPEX scaling | Roughly linear with shaft power; gearbox and shaft costs scale faster than engine cost above 10 MW. | Roughly linear with wetted hull area, since the SSIH is a tiled architecture (WP §3.4). 30 cm × 30 cm tiles allow per-unit cost learning curves familiar from flexible electronics. |
| OPEX (annual energy) | Marine diesel fuel cost dominates; biofouling adds up to 40 % overhead. Mid-range 20 m yacht at a representative 200 hrs/yr usage (typical for owner-operated mid-latitude recreational yachts; ranges from ~100 hrs/yr in cold-climate seasonal use to ~300 hrs/yr in chartered or year-round operation): typical $7k–$15k fuel + $5k–$15k servicing (rough order of magnitude; varies widely with cruise speed and bunker price). | Electrical energy at modelled tile-boundary η ≈ 83 % (full chain ≈ 80 %; WP §4.3 boundary); battery-electric or hybrid energy source. Annual energy cost depends on local electricity tariff and usage profile; at $0.20/kWh and the same 200 hrs/yr usage, on the order of $1k–$4k for the same hull. The OPEX gap widens with carbon pricing and bunker-fuel surcharges. |
| Maintenance cost | Routine oil changes, impeller/cooling-pump service, injector/turbo overhaul, prop polish, shaft seal, dry-dock antifouling repaint every 1–3 years. | No moving parts; per-tile replacement on failure (WP §3.4); no antifouling repaint cycle if the AC-EF antifouling effect is realised — otherwise comparable to a coated steel hull. |
| Lifetime / replacement interval | Heavy commercial diesel: 25 000–40 000 hrs to major overhaul; recreational gasoline outboard: 2 000–3 000 hrs. | Unknown; bounded by Ta₂O₅ dielectric lifetime under continuous electrochemical cycling — explicitly identified in WP §6 as an open experimental question. |
| Total cost of ownership sensitivity | Highly sensitive to bunker fuel price, carbon-pricing legislation, biofouling growth rate. | Sensitive to electricity price, dielectric MTBF, and tile failure rate. Insensitive to fuel-price shocks. |
| Residual / resale value | Well-established second-hand market; auction houses, surveyor protocols, blue-book pricing. | None; novel asset class with no resale market and no surveyor practice. |

### 4. Manufacturing

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Primary fabrication methods | Cast-iron block, forged crankshaft, machined cylinder heads, propeller casting + balancing. Heavy industrial supply chain. | Photolithographic patterning of interdigitated electrodes on flexible substrate; ALD deposition of 500 nm Ta₂O₅; surface-mount GaN PEM assembly (WP §3.1–3.4, §6). |
| Critical materials / supply chain | Steel, cast iron, copper windings (for hybrid), nickel/chromium alloys, lubricants, marine diesel. | Gold or platinum-plated copper electrodes, Ta₂O₅ ALD precursors, GaN power devices, flexible substrate. None individually exotic, but the integrated combination is not yet a catalogue marine product. |
| Production scalability | Mature; global capacity ~$36 B/yr market in 2025 [9]. Wärtsilä, MAN ES, Cummins, Rolls-Royce, Caterpillar dominate; top 5 = 40.5 % share. | Currently limited by (a) sub-15 µm flexible-substrate lithography roll-to-roll capacity and (b) large-area ALD throughput — both in active industrial development (WP §6). |
| Lead time | New-build commercial main engine 12–24 months; recreational and small-craft engines days to weeks from inventory. | First-of-kind prototype tiles: months to a year; production tiles at scale: unknown, optimistically 6–12 months with mature roll-to-roll flexible electronics fab. |
| Geographic distribution | Engines: Europe (MAN, Wärtsilä), Japan (Yanmar, Mitsubishi), Korea (Hyundai HHI), USA (Caterpillar, Cummins), China. Highly globalised. | If realised, would inherit semiconductor and flexible-electronics geography (East Asia, Western Europe, USA). |
| Maturity of tooling | TRL 9, IS0-9001 certified, in volume production for decades. | TRL 2 (concept validated by analysis only); the constituent processes (lithography, ALD, GaN) are TRL 9, but their integration into a hull-area tile is unvalidated. |

### 5. Complexity

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Number of moving parts | Hundreds to thousands per drivetrain (pistons, valves, rings, bearings, gears, shafts, cooling pumps, fuel pumps, injectors, governor, prop blades, shaft seals). | Zero in the propulsion path (the vessel as a whole still has the usual non-propulsion mechanical systems — bilge pumps, steering linkages, hatches, HVAC fans). Cooling fans on GaN PEMs are the only rotating elements within the propulsion chain, and they can be replaced by solid-state Peltier cooling if needed. |
| Distinct subsystems | Engine, fuel system, lubrication, cooling, exhaust, gearbox, shaft, propeller, control. | Active tile array, DC bus distribution, central propulsion management controller, salinity sensor network. |
| Control system | Modern ECMs are sophisticated but the underlying actuator (combustion) is fundamentally analog. | Inherently digital: every tile is an addressable element of a phased array. State-of-the-art digital propulsion. |
| Software / firmware | Engine control units: tens to hundreds of thousands of LOC, mostly safety-critical real-time. | PEM firmware (per-tile): waveform synthesis, fault detection, impedance sensing. Central controller: thrust allocation, salinity adaptation, fault re-routing. Software footprint substantial but conventionally architected (motor-drive parallels). |
| Integration with hull design | Bolt-in (engine on bedplate, prop on shaft); requires through-hull penetrations for shaft seal and exhaust. | Surface-applied during hull construction or refit; no through-hull penetrations required for the propulsion mechanism itself; tile electrical wiring routed inboard from the hull-internal face. |
| Failure modes | Long known list with empirical MTBF and inspection protocols. | Per-tile: dielectric breach, electrode delamination, GaN switch fault, communication-bus fault. New territory but follows established power-electronics fault models. |

### 6. Environmental impact

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Direct CO₂ emissions | International shipping ≈ 3 % of global CO₂; IMO target net-zero by ~2050, with at-least-20 % cut (striving 30 %) by 2030 and 70–80 % by 2040 vs. 2008 [1, 3]. | Zero direct CO₂ in operation; upstream emissions reflect electricity-grid carbon intensity plus embodied carbon in tile manufacturing (semiconductor, ALD, electrode-metal supply chains). On a fully renewable grid, *operational* propulsion CO₂ is zero; *life-cycle* CO₂ requires a separate LCA study. |
| Other GHGs | NOₓ, methane slip (LNG engines), N₂O. IMO Tier III enforced in ECA zones. | None directly. |
| Criteria pollutants | SOₓ, NOₓ, particulate matter (PM), CO. MARPOL Annex VI sulfur cap 0.5 % global, 0.1 % in ECAs. | None. |
| Oil / fuel spill risk | Significant: hull breach, engine-room leaks, bunkering accidents. Decades of regulation (OPA-90, MARPOL Annex I). | None; no liquid hydrocarbon onboard for the propulsion system. Battery thermal runaway is the analogous risk and is a separate hazard from the propulsion mechanism. |
| Underwater noise | Container ship monopole source level ~180 dB re 1 µPa @ 1 m (with peak measurements in the 180–188 dB range across the cited studies), predominantly below 40 Hz from prop cavitation + machinery vibration [7, 8]. IMO Experience Building Phase ends MEPC 85 in 2026; mandatory measures on the table after that [5, 6]. | The two dominant acoustic sources of a conventional vessel — propeller cavitation and rotating-machinery vibration — are absent by construction. The 2 MHz drive carrier is electrical, not acoustic; in seawater (σ ≈ 5 S/m) the EM skin depth at 2 MHz is ~16 cm, so the field does not propagate beyond the immediate hull boundary. The dominant emitted signature reduces to residual hull-flow noise of the displacement hull itself. |
| Cetacean and fish strike | Direct propeller and hull strike contribute tens to hundreds of documented large-cetacean mortalities annually in shipping lanes globally (IWC ship-strike database; regional NOAA right-whale records). Small recreational propeller strikes injure swimmers and pinnipeds. | No external rotating element; no propeller-strike mechanism. Strike risk reduces to the hull's own impact profile. |
| Biofouling and antifouling paint | Industry pays ~$30B/yr extra fuel from biofouling; antifouling paints (copper, biocides) themselves are pollutants and increasingly restricted. | The MHz field is hypothesised to suppress early-stage organic adhesion (WP §5.1); if validated this eliminates copper-biocide paint runoff. Validation required. |
| Ballast water cross-contamination | Major invasive-species vector; BWM Convention 2017 mandates treatment. | Unchanged — ballast is a separate system. |
| End-of-life disposal | Engines and exhaust components contain hazardous metals; oil residues; complex recycling. | Tiles contain noble-metal electrodes (recoverable), Ta₂O₅ (inert), GaN (recoverable), copper wiring. Solid-state assembly is conceptually cleaner to disassemble; needs an actual recycling pathway designed. |

### 7. Logistics

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Energy supply | Marine diesel oil (MDO), heavy fuel oil (HFO), increasingly LNG and methanol; emerging ammonia. | Electricity (shore charge, on-board battery, on-board generator). |
| Refuelling / recharging time | Diesel bunkering: hours for a yacht, hours-to-days for a container ship. | High-power DC shore charge timelines familiar from automotive EVs scaled up; minutes-to-hours depending on battery size and charger rating. Battery-pack swap is an architectural option. |
| Port infrastructure | Bunkering barges, fuel terminals, storage tanks; established globally. | High-power shore-power connections; megawatt-class shore-side charging is being rolled out independently of RIMT for battery-electric ferries; RIMT inherits that infrastructure. |
| Range per fill / charge | Crude carriers: 20 000 + nautical miles on one fill; recreational diesel yacht: 500–2 000 nm; gasoline outboards: 50–200 nm. | Determined by on-board battery capacity (or hybrid genset); not a function of the actuator. Energy-density gap between liquid hydrocarbons (~12 kWh/kg) and Li-ion (~0.25 kWh/kg) is the binding constraint for ocean-crossing applications. |
| Storage / handling | Hazardous liquid; vapour-recovery, spill containment, fire suppression required. | Battery: thermal-runaway containment is the analog; established but separate from propulsion. |
| Bunkering complexity | Significant: paperwork (BDN), quality testing, sampling, sludge disposal. | None for shore charge; standard high-power DC connector. |

### 8. Usability and ergonomics

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Bridge / cockpit experience | Engine noise, vibration, exhaust smell. Modern installations mitigate but do not eliminate. | Silent at the bridge; no engine-room vibration; no exhaust. Total acoustic signature dominated by sea-state. |
| Operator learning curve | Years to professional proficiency (engineer ratings, certificates); recreational courses 20–40 hrs for basic. | Throttle-and-direction interface unchanged from operator standpoint; deeper diagnostics require power-electronics knowledge rather than IC-engine knowledge. |
| Throttle response | Lagging (engine spool-up, shaft inertia, prop wash). | Effectively instantaneous (electronic). |
| Idle behaviour | Engine must run at idle RPM, consuming fuel and emitting exhaust. | Standby = zero current; no idle waste. |
| Special skills | Certificate of Competency (Engineer) for >750 kW; STCW endorsements for various engine types. | Power-electronics qualification analogous to electric-vehicle high-voltage certification. Lower entry barrier than the diesel engineer pathway, in principle. |
| Crew comfort below decks | Engine-room heat and noise; the engine room is generally the noisiest, hottest compartment. | No engine room. Hull-electronics compartments are dry, ambient-temperature, silent. |

### 9. Safety

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Fire / explosion | Diesel: relatively safe (high flash point); gasoline outboards and LNG: significant hazard. Engine-room fires are leading cause of vessel loss. | No fuel; battery thermal runaway is the analog and is addressed at the battery, not at the propulsion actuator. The hull-surface electrodes themselves carry low absolute power per tile. |
| Toxic exhaust | CO, NO₂, SOₓ, PM — chronic and acute health hazards in enclosed engine rooms. | None. |
| Propeller strike | Recreational: hundreds of injuries annually in busy waterways; commercial: documented cetacean fatalities. | Eliminated. No external rotating component. |
| Electrical / HV hazard | Limited to instrumentation and modern hybrid drives. | Each tile is electrically energised; the §3 design uses ≤ 5.3 V drive in the optimised configuration (WP §4.4) but transient and dielectric-breach conditions need careful per-tile isolation. GaN PEMs operate at higher local rail voltages. Fault response time "few µs" (WP §3.4, §5.3) is engineered to be faster than a person can contact a breach. |
| Fault tolerance | Single-engine vessels: zero redundancy; twin-engine: ~50 %. | Designed for ~15 % tile attrition while maintaining cruising speed via central-controller redistribution (WP §3.4); target spec, requires experimental validation. |
| Failure-to-safe | Engine seize-up or out-of-fuel = loss of propulsion + steerage. | Total-power-loss = passive coasting + drift; no runaway thrust mode (the field decays within one carrier cycle on power loss). |
| EMI / RF safety | Negligible; mechanical system. | MHz tangential fields are confined within the EDL by the dielectric and are not radiating antennas; EM skin depth in seawater bounds external radiation (δ ≈ 16 cm at 2 MHz). The binding constraint is in-hull coupling to the vessel's own GMDSS DSC receiver (2.187 5 MHz) and maritime mobile HF band (4–5 MHz); three mitigation paths are available (shielding, antenna placement, carrier-frequency selection). Quantitative EMI measurements at hull scale are an explicit open question. See WP §5.4. |

### 10. Maintenance

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Routine service interval | 200–500 engine hours for oil/filter; 5 000–10 000 hrs for top-end overhaul; 25 000–40 000 hrs for major rebuild. | No oil, no combustion; routine maintenance = electrical diagnostic sweep and tile health audit (target interval: yearly during scheduled hull inspection). |
| Dry-docking | Required for shaft work, prop polish, antifouling repaint, hull survey; typically 1–3 years interval. | Tile replacement is in principle in-water if the affected area is accessible; deep-hull tile replacement still requires dry-docking. Antifouling paint cycle eliminated if AC-EF antifouling effect is validated. |
| Wearing parts | Many: rings, bearings, valves, injectors, impellers, seals, prop blades. | Bonded ceramic dielectric and bonded electrode lattice; no sliding contacts. GaN devices have very long electrical lifetime under design conditions. |
| MTBF | Well-characterised; insurance actuarial tables exist for each engine class. | Unknown; the Ta₂O₅ dielectric MTBF under marine cycling is identified in WP §6 as an open question. |
| Field-repairability | Established global service network; certified marine engineers in every major port. | Tile-swap is a low-skill operation in principle (mechanical de-bond, electrical disconnect, re-bond); diagnostic skill required is power-electronics rather than IC-engine. Service network does not yet exist. |
| Spare-parts logistics | Mature; OEM catalogues; aftermarket parts; long-tail availability for legacy engines. | None; would need to be built from scratch alongside production. |
| Operator-performable maintenance | Daily checks (oil, coolant, exhaust); operator-replaceable filters; weekly visual inspection. | Daily diagnostic sweep is software-only; physical tile inspection per scheduled interval. |

### 11. Regulatory and certification

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Emissions framework | MARPOL Annex VI; IMO Tier I/II/III NOₓ; sulfur cap; CII / EEDI / EEXI / SEEMP regulatory machinery. IMO Net-Zero Framework expected to be adopted around the April 2026 MEPC session [1]. | Out of scope — no combustion emissions. CO₂ accounting deferred to electricity grid intensity (Scope 2 under standard GHG accounting). |
| Underwater noise | Voluntary IMO guidelines under Experience Building Phase to 2026; mandatory measures possible after [5, 6]. | Likely below any mandatory threshold once hull-flow noise is the only emitted signature. Could become a regulatory selling point. |
| Class society rules | DNV, ABS, LR, BV, CCS, KR, NK, RINA: well-developed rule sets for engines, propellers, shafts, exhausts. | No existing rule set. Type approval would require novel high-voltage and EMI rules; class societies have parallels (e.g., shore-power, hybrid-electric rule sets) that would inform new rules. |
| Type approval | Established and routine. | Would require a multi-year program with at least one classification society; this is identified as out-of-scope for the present disclosure. |
| ECA compliance | Engineering challenge for many existing vessels (scrubbers, low-sulfur fuel, dual-fuel conversion). | Inherent compliance — zero direct emissions. |
| Decarbonisation pathway | Multiple competing pathways: LNG bridge fuel, methanol, ammonia, biofuels, hydrogen, battery-electric, wind assist. None individually solves the 2050 target [1, 3]. | If validated, a single technology pathway covering propulsion. Does not address auxiliary loads (lighting, HVAC, cargo handling) which require separate electrification. |
| Regulatory novelty risk | Low; incremental tightening within familiar framework. | High; new technology classes typically take 5–15 years to settle into class-society rules and insurance practice. |

### 12. Operational envelope

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Minimum draft | Bounded by propeller diameter and immersion; shallow-water operation forces small props with reduced efficiency, water jets, or surface-piercing drives. | Zero hydrodynamic minimum: thrust is generated at the hull skin. Practical minimum draft is set by hull buoyancy alone. |
| Debris / floating-object tolerance | Lines, weeds, plastic bags routinely foul propellers; sub-surface debris can damage blades and shafts. | No external moving element to foul; deep cuts that breach the dielectric trigger local tile fault and isolation (WP §5.3). |
| Ice operation | Ice-class propellers are reinforced and de-rated; ice impact damages blades; specialised hull designs (icebreaker hulls) required. | Ice abrasion against the dielectric is an unresolved question (WP §5.3). Active Tile architecture permits localised replacement of ice-damaged sections without dry-docking the whole vessel, in principle. |
| Salinity range | Diesel and gasoline indifferent to salinity. | EDL coupling depends on ion concentration: best in seawater (~5 S/m), reduced in brackish (0.5–2 S/m), poor in freshwater (<0.1 S/m). Adaptive drive voltage partially compensates (WP §5.2). |
| Sea-state limits | Engine performance unaffected; hull and crew limit. | Tile-level robustness to wave slap and slamming loads is an open question (WP §6); the bonded ceramic layer is mechanically stiff and brittle, so slamming-load qualification is required. |
| Cold/hot start | Diesel cold-start in arctic conditions is non-trivial; pre-heaters needed. | Solid-state, no cold-start issues; electronics are temperature-derated like any wide-bandgap power system. |

### 13. Scalability across vessel classes

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Smallest practical vessel (jet ski, dinghy) | Mature: 2-stroke outboards, electric outboards, jet drives. | A single 30 cm × 30 cm tile delivers ~5 N of thrust at design density; thirty tiles ≈ 150 N — adequate for a one-person craft. Scaling to jet-ski speeds (40+ knots) requires increased thrust density, an open question. |
| Mid-range (10–20 m yacht, small ferry) | Conventional 10–20 m yachts use 50–200 hp diesel inboards or 60–300 hp outboards; small ferries use 200–800 kW diesel-electric drives. Well-served by existing OEMs across all sub-segments. | The whitepaper's reference design point (30 m² hull, 1 500 N at 10 m/s; WP §4.4). |
| Large commercial (100 m+ container, tanker) | Slow-speed two-stroke diesel; the most efficient configuration available today. | Hundreds to thousands of tiles; tile count scales with wetted area. Aggregated power draw at sea is non-trivial — requires battery/genset/nuclear sizing well beyond present marine-electric norms. |
| Mega-vessel (300 m+) | Routine; 80 MW main engines common; up to ~110 MW (Triple-E class). | Theoretically scalable; at scale the limiting factor becomes onboard electricity generation, not the actuator. |
| Naval / military | Sophisticated diesel-electric or nuclear-electric drives with quieting measures. | Acoustic-signature elimination is a significant theoretical advantage for stealth applications. Identified as natural high-value early adopter sector if classification can be obtained. |
| Underwater (UUV, submarine) | Battery-electric with screw or pump-jet; the closest prior art (Hansen et al. 2020 [WP ref 2]) is an electro-osmotic capillary thruster for a 5 kg UUV. | Natural fit: hull-distributed silent propulsion is exactly what UUV designers want. Possibly the lowest-risk first application. |

### 14. Market position and adoption

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| Installed base | Effectively the entire global merchant fleet (~100 000 vessels) and recreational fleet (~30 M boats worldwide). | Zero. |
| Annual new-build volume | $36 B/yr marine engine market in 2025 [9]; diesel = 66 % share; top 5 OEMs (Wärtsilä, Volvo Penta, Cummins, Rolls-Royce, Caterpillar) hold 40.5 %. | None until prototype is built. |
| Brand and OEM ecosystem | Long-established brand value, service networks, financing channels. | None; the comparative play is open-source / academic / start-up. |
| Customer perception | Familiar, trusted, well-understood failure modes. | Untested; risk-averse customers will wait for proven installations. |
| Novelty / first-mover advantage | None remaining; the technology is commoditised. | Substantial; the prior-art disclosure under CC BY-SA 4.0 establishes Szabó as the originator and prevents proprietary patent capture (WP §7). |
| Adoption barriers | Carbon regulation, fuel price, IMO 2030/2040/2050 targets. | Lab validation; class-society type approval; OEM partnerships; insurance availability; service network bootstrap. |
| Insurance availability | Routine; well-established actuarial basis. | Would need to be negotiated case-by-case for first installations. |

### 15. Technology readiness and maturity

| Sub-aspect | Conventional propulsion | RIMT |
|---|---|---|
| TRL (NASA scale) | 9 (fielded systems). | Between TRL 2 (concept formulated) and TRL 3 (analytical proof-of-concept) — the first-order computational models and 52-unit-test simulation suite arguably push the project toward TRL 3, but no physical experiment has been performed (WP §6). The project is reported as TRL 2 for conservative accounting. |
| Operating history | 150 + years for steam/diesel; 60 + years for modern slow-speed two-stroke. | None as a fielded system; component technologies (GaN power electronics, ALD Ta₂O₅, IDE electrokinetics) individually mature. |
| Open vs. proprietary | OEMs hold thousands of patents on engine internals; basic configurations are off-patent. | Defensive publication under CC BY-SA 4.0; the design space is being deliberately kept open. |
| Patent landscape | Dense at the component level; clear at the architectural level. | Prior-art disclosure deliberately blocks proprietary capture (WP §7); first-mover patent risk is reduced by this strategy. |
| Standardisation | ISO, IMO, class-society standards exist for every component and operating condition. | None. Would need to be developed in parallel with first installations. |
| Research community | Marine engineering departments worldwide; ~10⁴ active researchers; established conferences (CIMAC, SNAME, INEC). | Microfluidics electrokinetics community (WP §2): hundreds of active researchers, but no one currently working on marine-scale TWEO. Whitepaper is intended to draw that community in. |

---

## Quantitative scorecard

A normalised one-page view of the comparison. The rubric is qualitative and is intentionally honest about RIMT's "design target" status: a "+" or "++" in the RIMT column means *if the first-order model is reproduced in hardware*, not *measured today*.

**Rubric legend** (ASCII equivalents in parentheses to avoid en/em-dash confusion):

| Mark | ASCII | Meaning |
|:---:|:---:|---|
| `++` | `++` | Strong advantage |
| `+`  | `+`  | Advantage |
| `0`  | `0`  | Neutral |
| `–`  | `-`  | Disadvantage |
| `– –` | `--` | Strong disadvantage |
| `?` | `?` | Unresolved / unknown |

| Category | Conventional | RIMT (modelled) | Decisive factor |
|---|:---:|:---:|---|
| 1. Operating principle / physics novelty | 0 | ++ | RIMT is a new propulsive mechanism at this scale |
| 2. Performance — efficiency | + | ++ | 70–72 % ceiling vs. 83 % tile-boundary modelled upper bound (full chain ≈ 80 %) |
| 3. Economics — OPEX | – | + | Fuel cost vs. electricity at modelled efficiency |
| 3. Economics — CAPEX | + | – | Mature supply chain vs. nascent flexible-electronics fab |
| 4. Manufacturing maturity | ++ | – | Decades of tooling vs. emerging process |
| 5. Complexity (mechanical) | – | ++ | Thousands of moving parts vs. zero |
| 5. Complexity (software) | 0 | – | Conventional ECMs vs. distributed phased-array control |
| 6. Environment — emissions | – – | ++ | Conventional has CO₂, NOₓ, SOₓ, PM, noise, oil spill, biocide; RIMT has none directly |
| 7. Logistics — fuel | – | + | Bunker logistics vs. shore charge |
| 7. Logistics — range | ++ | – | Hydrocarbon energy density vs. battery |
| 8. Usability | 0 | + | Silent, instant-response, zero idle |
| 9. Safety — fire / strike | – | ++ | Fuel & propeller hazards eliminated |
| 9. Safety — electrical | + | 0 | Existing HV systems vs. novel EMI/HV regime |
| 10. Maintenance | – | + | Service-intensive vs. solid-state (if dielectric MTBF holds) |
| 11. Regulatory | – | + | Tightening emissions regime favours RIMT |
| 12. Operational envelope — shallow water | 0 | ++ | Zero draft requirement |
| 12. Operational envelope — freshwater | + | – | RIMT degrades at low ionic concentration |
| 12. Operational envelope — ice | + | ? | Ice abrasion on dielectric unresolved |
| 13. Scalability | + | + | Both scale, by different mechanisms |
| 14. Market position | ++ | – | Installed base 100 % vs. 0 % |
| 15. TRL | ++ | – – | TRL 9 vs. TRL 2 |

**Net read:** RIMT's modelled profile is strongest exactly where conventional propulsion is most pressured — environmental, regulatory, maintenance, safety. RIMT's weakest cells are exactly where conventional is strongest — TRL, supply chain, installed base. This is the classical innovator's-dilemma profile, in which the incumbent has every present advantage and the challenger has every future-trend advantage.

---

## Where RIMT could win

A reader who has worked through the tables above can predict the conclusions, but they bear stating explicitly.

**Regulatory tailwind.** The IMO's Revised GHG Strategy [1, 3] requires steep emissions cuts by 2030, 2040, and 2050 against a 2008 baseline. Underwater radiated noise enters its mandatory-or-not decision window at MEPC 85 in 2026 [5, 6]. Antifouling-paint biocides are under increasing restriction in coastal states. Each of these regulatory vectors targets a problem that RIMT, by construction, would not produce in the first place rather than mitigate by addition. Conventional propulsion has to add scrubbers, switch fuels, slow down, repaint, and add quieting jackets — and still falls short of 2050. RIMT, if validated, does not add to the conventional propulsor — it replaces it, and the consequent elimination is concurrent across emissions, noise, biocide runoff, and propeller strikes rather than sequential mitigation through retrofits.

**Maintenance economics for high-utilisation vessels.** A vessel that operates 4 000 + hours per year currently sees most of its TCO go to fuel and engine maintenance. The "no moving parts" claim of RIMT is unusually robust because the active element is a phased array of static electrodes coated by a ceramic dielectric and driven by surface-mount semiconductors — the components with the lowest known wear rates in any electromechanical category. If the Ta₂O₅ dielectric durability proves out, the operating-cost picture would differ structurally from any internal-combustion option.

**Naval and UUV applications.** Acoustic-signature reduction is among the most persistent challenges in naval submarine propulsion; conventional answers (pump-jets, raft-mounted machinery, acoustic-tile cladding) mitigate rather than eliminate the source. The closest prior art (Hansen et al. 2020 [WP ref 2]) already demonstrated electro-osmotic vehicle propulsion at UUV scale. RIMT's hull-distributed architecture is a natural fit for stealth applications, and these applications are willing to pay technology-development premiums that civilian vessels are not. A funded UUV demonstrator may be the fastest practical route to a hardware validation of RIMT.

**Shallow-water and zero-draft operation.** No propulsor; no minimum draft. River boats, marsh boats, rescue craft in flood conditions, and shore-attack landing craft all currently sacrifice efficiency to shallow-water capability. RIMT's distributed-skin actuator is geometrically indifferent to local water depth.

---

## Application landscape — where RIMT's profile fits naturally

The "Where RIMT could win" narrative above sketches the general shape of RIMT's strategic positioning. This section catalogues specific application classes, organised by sector. Each entry pairs an established market category with the RIMT property that creates the fit, and tags an indicative plausibility horizon: **Near-term** (≤ 5 years from a successful first lab validation), **Mid-term** (5–15 years), **Long-term** (≥ 15 years). All horizons are conditional on a first lab prototype being built and the η ≈ 83 % figure being reproduced within an order of magnitude; if validation fails, all horizons collapse.

The list is deliberately broad. The intent is not to claim that RIMT will be the optimal answer for every entry — most will be revisited (and many discarded) as real performance data arrives. Naming the candidates explicitly is the first step toward separating realistic early-market opportunities from wishful long-shots.

### Defence and security

Acoustic-signature reduction is among the most valuable properties RIMT offers in this sector. Cetacean-acoustic detection of submarines is the historic adversary of submarine stealth; conventional answers are pump-jets, raft-mounted machinery, and acoustic-tile cladding, all of which mitigate rather than eliminate. RIMT removes the dominant source.

| Application | Why RIMT fits | Plausibility |
|---|---|---|
| Strategic and attack submarines | Removes propeller/pump-jet acoustic source; hull becomes the propulsor | Long-term (national-programme scale, decades of qualification) |
| Unmanned underwater vehicles (UUVs/AUVs) | Silent; no rotating elements to entangle in nets or seabed debris; distributed thrust gives fine attitude control; lowest-stakes first-mover venue (small craft, accepted risk envelope) | **Near-term** — most plausible first hardware validation |
| Special-forces clandestine insertion craft | Silent surface and sub-surface operation; no exhaust signature for IR/visual detection | Mid-term (defence-funded prototype) |
| Mine countermeasure drones | Non-magnetic, non-acoustic; minimises triggering of mine fusing | Mid-term |
| Surface combatant signature management | Reduces own-ship noise that degrades own sonar; removes wake-cavitation signature | Long-term (full-class redesign) |

### Marine science, conservation, and wildlife-sensitive operation

Conventional propellers strike, deafen, and disturb marine fauna. Where the mission *is* to observe, count, study, or protect that fauna, the propulsor itself becomes a contaminant of the measurement.

| Application | Why RIMT fits | Plausibility |
|---|---|---|
| Marine-reserve patrol and ranger vessels | No propeller strike on manatees, turtles, sea lions, dugongs; near-silent operation | Near-term (small craft, regional pilots) |
| Whale-watching tour boats | Acoustic stealth removes the operator's own contribution to the disturbance that regulations are tightening to limit | Near-term |
| Cetacean and pinniped research vessels | Removes the dominant source of self-induced acoustic interference in passive-sonar studies | Near-term |
| Coral-reef and seagrass survey craft | Zero-draft capability; no prop-wash sediment plume; no propeller damage to shallow benthic habitat | Near-term |
| Polar research vessels (in open water) | Low underwater radiated noise reduces displacement of monitored marine mammals; no exhaust contamination of clean-air samples | Mid-term (ice-abrasion qualification gates broader use) |
| Fisheries-stock survey ships | Silent operation does not herd or scatter the fish populations being acoustically counted | Mid-term |

### Commercial and industrial niches

These are the segments where high utilisation, regulatory pressure, or geographic constraints make conventional propulsion structurally awkward.

| Application | Why RIMT fits | Plausibility |
|---|---|---|
| Inland-waterway and canal boats | Shallow draft; zero emissions in urban-canal contexts where diesel is increasingly restricted; low noise for residential waterways | Near-term (small fleets, regional regulation) |
| Harbour tugs and pilot boats | High duty cycle amortises CAPEX premium; ports already pushing for shore-power and zero local emissions | Mid-term |
| Short-haul passenger ferries (urban) | Frequent docking favours instant-response electronic thrust; cities tightening port-side emissions and noise rules | Mid-term |
| Cruise-ship port-side manoeuvring | Many cruise lines already required to use battery-electric in port — RIMT replaces the bow and stern thrusters that are the noisiest in-port emitter | Long-term (large-vessel certification) |
| Aquaculture cage-tending workboats | Low-disturbance operation around farmed-fish pens reduces stress-induced mortality | Mid-term |
| Sonar-survey and seismic-research vessels | Removes the largest in-band noise source competing with the survey signal | Mid-term |
| Search-and-rescue craft | Quiet hull lets crew hear survivors; no propeller hazard around floating casualties; instant thrust response in surf-zone work | Mid-term |

### Recreational and luxury

The recreational segment is the largest installed base of marine propulsors by unit count. Most of the comfort, safety, and environmental advantages of RIMT are felt most acutely here, where the operator and passengers are within metres of the propulsor.

| Application | Why RIMT fits | Plausibility |
|---|---|---|
| Luxury yacht primary or auxiliary propulsion | Silent cruising; no exhaust on aft deck; no shaft vibration on hull-mounted sleeping cabins | Mid-term |
| Sailing-yacht auxiliary "engine" replacement | Replaces a 20–60 kW diesel auxiliary that runs few hours/year but takes up engine-room volume, requires fuel tankage, and breaks the sail-only ethic | Near-term (low-power demonstrator) |
| Inflatable boats and tenders | No propeller hazard around swimmers boarding from the water; no fuel onboard an inflatable craft | Near-term |
| Pontoon and party boats | Pontoon hulls operate on lakes where noise ordinances bite; no shore-side fuel handling | Near-term |
| Pool, lagoon, and resort taxi craft | No fumes in enclosed waters; no propeller hazard around swimmers | Near-term |

### Hobby, education, and toys

The smallest end of the size range is also the lowest stakes for a TRL-2 technology. Failure modes are inconvenient, not catastrophic. The educational appeal of a visible electrokinetic effect is intrinsic.

| Application | Why RIMT fits | Plausibility |
|---|---|---|
| Radio-controlled boats and submarines | No propeller-blade injury risk to children; no fuel; silent operation lets onlookers hear what is happening | **Near-term** — possibly the easiest standalone consumer demonstration of the principle |
| STEM education kits | A hands-on demonstration of electrokinetics is currently a microfluidics-lab exercise; a tabletop "ionic boat" makes the principle visible | Near-term |
| Aquarium current generators | Replace impeller pumps with a hull-skin actuator; silent, no rotating element for fish to be sucked into | Near-term (very small product, very small unit price) |
| Pool-cleaning robot propulsion | No propeller, no impeller, no entangled hair, no minimum-draft constraint | Mid-term |

### Adjacent and unconventional uses

| Application | Why RIMT fits | Plausibility |
|---|---|---|
| Offshore wind / oil-platform inspection ROVs | Quiet operation around acoustic instrumentation; no cable-entanglement risk | Near-term |
| Subsea cable and pipeline survey vehicles | Distributed thrust gives precision stationkeeping above the line being surveyed; no cavitation noise in hydrophone-array data | Mid-term |
| Underwater archaeology vehicles | No prop-wash to disturb sediment overlying artefacts | Near-term |
| Hospital and disaster-relief ships | Silent harbour operations where moored alongside disaster zones reduce patient-area noise | Long-term |
| Buoy and platform stationkeeping | Counters tidal current to hold position without rotating thrusters | Mid-term |
| Hydrofoil and surface-effect craft | Hull-skin thrust source is geometrically compatible with the small wetted surface of foiling vessels; removes the strut-mounted propulsor that currently couples noise back into the hull | Long-term |
| Antarctic / Arctic icebreaker auxiliary thrust | Where ice-induced propeller damage is a primary maintenance cost, an additive hull-skin source reduces dependence on the main screw | Long-term (ice qualification required) |

### How to read this list

A reader looking for the **lowest-risk early validation** should focus on **Near-term** entries at the smallest physical scale and the most permissive failure envelope — UUVs, sailing-yacht auxiliaries, RC craft, and pool/aquaculture circulation. A reader looking for the **largest-value early win** should focus on naval UUVs, harbour tugs, and short-haul urban ferries, where regulatory pressure and high utilisation co-locate. The mega-vessel and submarine segments are real but their certification timelines are measured in decades.

---

## Where conventional propulsion retains the advantage

**Energy density.** A modern diesel main engine plus its bunker tanks delivers a ship-energy density that no battery + electric propulsor presently approaches by an order of magnitude or more. Ocean-crossing range will require either hybrid auxiliary genset, nuclear power, or a regulatory and commercial revolution in shore-charging infrastructure that is independent of RIMT and required by every electric-propulsion architecture.

**Cold, hard, validated economics.** The CAPEX, OPEX, MTBF, residual value, insurance premium, and surveyor-acceptance picture for a marine diesel engine is fully known to four-digit accuracy and underpins ship finance. None of this exists for RIMT and bringing it into existence is the work of years and tens to hundreds of millions of dollars of capital.

**Component supply chain depth.** A diesel-powered yacht's engine room can be serviced in every major port on Earth, with spares available next-day for any common configuration. A first-generation RIMT vessel needs every replacement tile, every diagnostic console, and every certified service technician to be invented and trained alongside the vessel itself.

**Operational envelope edge cases.** Ice abrasion, slamming-load qualification, freshwater salinity adaptation, and resistance to deliberate mechanical attack (military environment, debris-rich harbours) are all unresolved engineering questions for RIMT (WP §5, §6). Conventional propulsion has decades of empirical answers in each of these domains.

**Regulatory inertia.** Even if RIMT were qualified by a classification society tomorrow, the regulatory acceptance pathway through IMO, flag-state administrations, insurance underwriters, and port authorities is multi-year. Conventional propulsion is the legal default.

---

## Caveats and reading instructions

This is a *strategic* comparison rather than an *engineering* comparison. Many sub-aspects above hide further technical depth. In particular, every RIMT cell that quotes a number (tile-boundary η = 83 % / full-chain ≈ 80 %, Pe ≈ 65, 50 N/m², 5.3 V, 60 m/s wave speed) comes from a first-order analytical model implemented and unit-tested in the companion repository (`simulations/rimt_simulation.py`, 52 tests passing). They are *upper bounds* under stated idealisations; the whitepaper §6 enumerates the experimental work needed to set realistic lower bounds.

Conventional-propulsion figures are drawn from textbook, regulatory, and trade-press sources cited in the bibliography. Where ranges are given (e.g., "55–77 % open-water propeller efficiency"), the spread reflects real differences across vessel class and operating point rather than measurement uncertainty.

The quantitative scorecard's `+`/`++`/`–`/`– –` marks are deliberately qualitative. A reader who wants a single numerical decision criterion should compute their own weighted sum using the weights that reflect their own application: a small-vessel recreational user weights `9. Safety — fire/strike` and `12. shallow water` highly; a container-shipping firm weights `7. range` and `15. TRL` highly; a navy weights `6. noise` and `9. safety` highly. The scorecard's purpose is to expose the trade-off structure, not to declare a winner.

---

## References

*The references below cover only the conventional-propulsion side of the comparison. All `WP refs [n]` cross-references in the table body are inherited from the whitepaper bibliography ([`whitepaper/RIMT-whitepaper.md`](../whitepaper/RIMT-whitepaper.md), refs 1–7 and the cited textbooks block); please consult the whitepaper directly for the full citation entries.*

1. Global Maritime Forum. *A guide to the IMO's Net-Zero Framework*. https://globalmaritimeforum.org/news/a-guide-to-the-imos-net-zero-framework/
2. Depco Power Systems. *Marine Diesel Engine Costs: New, Used & Rebuilt Guide*. https://www.depco.com/faq/how-much-does-a-marine-diesel-engine-cost/
3. International Council on Clean Transportation (ICCT). *IMO's newly revised GHG strategy: What it means for shipping and the Paris Agreement*. https://theicct.org/marine-imo-updated-ghg-strategy-jul23/
4. Maritime Executive. *OP-ED: Marine Propulsive Efficiency in Speed Restricted Waterways*. https://maritime-executive.com/features/op-ed-marine-propulsive-efficiency-in-speed-restricted-waterways
5. IMO. *Ship noise — IMO Hot Topics*. https://www.imo.org/en/mediacentre/hottopics/pages/noise.aspx
6. BIMCO. *Ships must cut underwater noise or face mandatory regulation*. https://www.bimco.org/news-insights/bimco-news/2024/20240207-imo-sdc-10-underwater-radiated-noise/
7. Nature Scientific Reports. *Relationship between container ship underwater noise levels and ship design, operational and oceanographic conditions*. https://www.nature.com/articles/srep01760
8. *Deep-water measurements of container ship radiated noise signatures and directionality*. Journal of the Acoustical Society of America, 142(3), 1563 (2017). https://pubmed.ncbi.nlm.nih.gov/28964105/
9. GMInsights. *Marine Engines Market Size, Share, Industry Report 2026–2035*. https://www.gminsights.com/industry-analysis/marine-engines-market
10. Qlayers. *The Hidden Cost of Efficiency: Biofouling in Maritime Shipping*. https://www.qlayers.com/the-hidden-cost-of-efficiency-biofouling-in-maritime-shipping/
11. Carlton, J. S. (2018). *Marine Propellers and Propulsion* (4th ed.). Butterworth-Heinemann. (Cited via the whitepaper for propeller theory and the 70–72 % practical efficiency ceiling.)
12. ScienceDirect topic. *Propeller Efficiency*. https://www.sciencedirect.com/topics/engineering/propeller-efficiency
13. MAN Energy Solutions. *Efficiency of MAN B&W two-stroke engines* (stationary applications). https://www.man-es.com/docs/default-source/document-sync-archive/efficiency-of-man-b-w-two-stroke-engines-eng.pdf
14. International Whaling Commission. *Anthropogenic sound*. https://iwc.int/management-and-conservation/environment/anthropogenic-sound
15. RIMT Whitepaper — *Solid-State Marine Propulsion via Resonant Ionic Momentum Transfer (RIMT)*, Szabó (2026). Same Zenodo deposit / [`whitepaper/RIMT-whitepaper.md`](../whitepaper/RIMT-whitepaper.md). All "WP §" cross-references in this document refer to that file.

---

*Companion document to the RIMT Technical Disclosure, published under CC BY-SA 4.0 · Project Leviathan · DOI: [10.5281/zenodo.20361267](https://doi.org/10.5281/zenodo.20361267) (concept, always-latest)*

---

## Appendix A — Sources of asymmetry

For full transparency about where the comparison has unavoidable epistemic asymmetry:

- **Conventional column** — numbers are drawn from publicly available textbook, industry-report, and trade-press sources cited in the bibliography. Where ranges are given, they reflect the spread across vessel classes and operating points in the original sources, not measurement uncertainty.
- **RIMT column** — every quantitative claim traces back to the whitepaper ([`whitepaper/RIMT-whitepaper.md`](../whitepaper/RIMT-whitepaper.md)) or its companion simulation ([`simulations/rimt_simulation.py`](../simulations/rimt_simulation.py), 52 unit tests passing). These are *first-order analytical upper bounds under stated idealisations*, not measurements. The whitepaper §6 (Limitations and Future Work) is the canonical list of what remains experimentally open.

Readers comparing a row across both columns are therefore comparing *measured empirical practice* against *modelled design target*. Where a row's RIMT cell uses a word like "designed," "modelled," "target," or "if validated," the asymmetry is explicit. Where it does not, the asymmetry remains and should be understood from this appendix.

---

## Appendix B — Figures and visualisation specifications

Figure 1 (energy conversion chain) is rendered below. Figures 2–6 retain their full specifications for reference; static rendered versions are deferred to v1.2 (the interactive infographic at `RIMT-infographic.html` already provides interactive versions of Figures 3–5).

### Figure 1 — Energy conversion chain, side-by-side (Sankey or block diagram)

**Purpose.** Show the same input (1 unit of primary energy) flowing through the two propulsion stacks, with each loss stage labelled.

**Conventional stack (top row):**

Fuel chemical energy (100 %) → combustion (≈ 50 % retained, 50 % heat loss) → transmission + shaft (≈ 95 %) → propeller open-water (≈ 70 %) → hull-clean useful thrust ≈ 33 %. Stage values from Section 1 and Section 2 of this document and WP §4.

**RIMT stack (bottom row):**

Battery electric energy (100 %) → DC bus (≈ 99 %) → GaN PEM AC synthesis (≈ 97 %) → EDL traveling-wave coupling + ohmic loss + viscous coupling (tile-boundary η = 83 % — WP §4.4 headline; see §4.3 for boundary definition) → useful thrust ≈ 80 % full chain (0.99 × 0.97 × 0.83). Numbers from the optimised reference point in WP §4.4.

**Visual notes.** Use proportional band widths if drawn as Sankey; identical input width for both stacks so the difference in retained thrust is visually obvious. Loss bands in muted red; retained band in cool blue.

<!-- FIGURE_1_START -->
<figure style="margin:1.2em 0;text-align:center">
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
</svg>
<figcaption style="font-size:10pt;color:#444;margin-top:4pt;text-align:left"><strong>Figure 3.</strong> Energy conversion chain: conventional diesel-mechanical propulsion (left) vs. RIMT battery-electric propulsion (right). Bar width is proportional to the cumulative retained fraction of the input energy. Conventional: fuel chemical energy &rarr; combustion (&times;50%) &rarr; transmission + shaft (&times;95%) &rarr; propeller open-water (&times;70%) &rarr; &approx;33% useful thrust. RIMT: battery electric &rarr; DC bus (&times;99%) &rarr; GaN PEM (&times;97%) &rarr; tile EDL (tile-boundary &eta; = 83%, WP &sect;4.4) &rarr; &approx;80% full-chain useful thrust (0.99&times;0.97&times;0.83). The WP &sect;4.4 headline &eta;&nbsp;&asymp;&nbsp;83% is the tile-boundary efficiency (electrical input to tile &rarr; useful thrust; DC bus and GaN PEM losses not included &mdash; see WP &sect;4.3 for boundary definition). Numbers rounded.</figcaption>
</figure>
<!-- FIGURE_1_END -->

### Figure 2 — Quantitative scorecard as a radar chart

**Purpose.** A single image that conveys the trade-off structure of the 20-row scorecard at a glance.

**Axes (20):** the 20 rows of the Quantitative Scorecard, in the order printed.

**Mapping `+`/`++`/`–`/`– –` to numeric axis values:** `– –` = 1, `–` = 2, `0` = 3, `+` = 4, `++` = 5. For the "TRL" axis (RIMT = `– –`), keep the asymmetry visible — do not normalise it away.

**Two overlaid polygons:** Conventional in one colour, RIMT (modelled) in another, both translucent. Add a small caption restating the "modelled, not measured" caveat.

*Rendered figure deferred to v1.2. The specification above documents the intended content.*

### Figure 3 — Application landscape quadrant

**Purpose.** Position each application from the Application Landscape section on a 2-D plane.

**Axes.**
- X-axis: *Value of RIMT's unique properties* (acoustic stealth + zero-draft + zero-emission) on a 0–10 scale.
- Y-axis: *Risk tolerance of the typical early customer in this segment* on a 0–10 scale (consumer toys ≈ 10; naval surface combatant ≈ 1).

**Each application = a labelled dot.** Suggested coordinates:

| Application | X (value) | Y (risk tolerance) |
|---|:---:|:---:|
| RC boat | 4 | 10 |
| Pool cleaner | 5 | 9 |
| Aquarium pump | 4 | 9 |
| STEM education kit | 3 | 9 |
| Sailing-yacht auxiliary | 6 | 8 |
| Marine-reserve ranger boat | 8 | 7 |
| Whale-watching tour boat | 9 | 6 |
| Inland canal boat | 7 | 6 |
| Small naval UUV | 10 | 5 |
| Cetacean research vessel | 9 | 4 |
| Harbour tug | 7 | 3 |
| Urban passenger ferry | 8 | 3 |
| Container ship | 4 | 1 |
| Attack submarine | 10 | 1 |

**Visual notes.** The "sweet spot" — upper-right — is where RIMT is both highly valuable to the customer *and* the customer is most willing to accept technology risk. This is where the dots cluster from the hobby/toys/recreation, marine-science, and small-craft niches. Label that region "natural early adopters."

*Rendered figure deferred to v1.2. An interactive version is available in the companion infographic (`RIMT-infographic.html`).*

### Figure 4 — CO₂ reduction sensitivity to fleet adoption

**Purpose.** Quantify the upside of RIMT for shipping-decarbonisation policy makers.

**Anchor numbers (from the IMO baseline cited in [1, 3]):**
- 2008 international-shipping CO₂ baseline: ≈ 1.05 Gt CO₂/yr
- 2050 IMO net-zero target: 0 Gt by ≈ 2050; interim 70–80 % cut by 2040
- 2024 actual: ≈ 1.05–1.1 Gt CO₂/yr (essentially flat against baseline)

**Plot a stacked-area chart over the years 2025–2050 showing:**
- Baseline (no action): flat at 1.05 Gt
- IMO target curve: declining from 1.05 Gt to 0
- Hypothetical RIMT adoption curve: 0 % of fleet by 2030, 5 % by 2035, 20 % by 2040, 50 % by 2050 (illustrative — not a forecast)
- CO₂ avoided = baseline minus RIMT-share-displaced — shade the avoided area

**Caveat to put in the caption:** the RIMT share assumes RIMT propulsion is paired with renewable grid electricity. Adoption percentages are illustrative for sensitivity analysis only, not a forecast.

*Rendered figure deferred to v1.2. An interactive version is available in the companion infographic (`RIMT-infographic.html`).*

### Figure 5 — TRL pathway and indicative cost-to-validate

**Purpose.** Help a potential R&D sponsor see the rough scale of what is being asked for.

**X-axis:** years from t = 0 (= first funded prototype).

**Y-axis:** cumulative R&D investment, USD millions, log scale.

**Milestones to plot:**

| Year | Milestone | Cumulative spend (illustrative) |
|---|---|---|
| 0 | Bench-top ionic-plate prototype | $0.05 M |
| 1 | Torsion-balance thrust measurement; first η, drag, fouling numbers | $0.2 M |
| 2 | 1 m² tile demonstration, indoor saltwater tank | $1 M |
| 3 | Sub-scale vessel demonstrator (≈ 3 m, ≈ 1 m²) | $5 M |
| 5 | First in-water vessel demonstrator (≈ 10 m, ≈ 30 m²) | $20 M |
| 8 | First class-society pilot (small commercial craft, single-tile-array hull) | $80 M |

**Caveat in caption:** numbers are order-of-magnitude planning estimates, not commitments. The whitepaper §6 lists the experimental work each milestone embeds.

*Rendered figure deferred to v1.2. An interactive version is available in the companion infographic (`RIMT-infographic.html`).*

### Figure 6 (optional) — Acoustic signature comparison

**Purpose.** Make the underwater-noise advantage concrete to a non-engineer reader.

**X-axis:** frequency, 10 Hz to 100 kHz, log scale.

**Y-axis:** sound pressure level, dB re 1 µPa @ 1 m.

**Curves:**
- Container-ship monopole source spectrum: ≈ 180 dB at 10–40 Hz, declining to ≈ 130 dB above 1 kHz (after [7, 8]).
- A clean, electric-propulsion small vessel for reference: ≈ 130 dB at 10 Hz, ≈ 110 dB above 1 kHz.
- RIMT projected: hull-flow noise of the displacement hull alone, ≈ 110 dB at 10 Hz, ≈ 90 dB above 1 kHz (projected from the source-elimination argument in Section 6).

**Shaded overlay:** cetacean vocalisation bands (blue whale 10–40 Hz; humpback 30 Hz–8 kHz; killer whale 0.5–40 kHz; sperm-whale clicks 5–25 kHz).

**Caveat in caption:** the RIMT curve is a projection from the source-elimination argument, not a measurement.

*Rendered figure deferred to v1.2. The specification above documents the intended content.*

### Render-priority notes

For "publication-grade" feel, the highest-leverage figures are 1, 2, and 4. For a sponsor / decision-maker pitch deck, Figures 3 and 5 are the most useful (and form the basis of the separately-shipped infographic data package, `RIMT-infographic-data.md`). Figure 6 is the "killer chart" for environmental-stakeholder audiences.

