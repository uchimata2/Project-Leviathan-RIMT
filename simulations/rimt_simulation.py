#!/usr/bin/env python3
"""
rimt_simulation.py — Resonant Ionic Momentum Transfer: First-Order Models
==========================================================================

Project Leviathan — Solid-State Ionic Hull (SSIH)

Author  : Gábor Szabó
Date    : May 2026
License : CC BY-SA 4.0  <https://creativecommons.org/licenses/by-sa/4.0/>

Three analytical models of increasing sophistication, corresponding to the
mathematical derivations in the SSIH whitepaper (Section 4):

  Model 1 — Debye Layer Fundamentals
      Establishes the physical basis: Debye screening length, surface charge
      density, and upper-bound thrust density / electro-osmotic velocity using
      the linearised Poisson–Boltzmann model and the Smoluchowski equation.
      Uses a 1 MV/m pulsed tangential field — an upper bound, not a sustained
      operating point.

  Model 2 — Parametric RIMT Performance  (baseline / untuned design)
      Evaluates a specific set of hardware parameters (1 µm alumina coating,
      200 V fixed peak, 2 MHz, 1.0 m/s wave-fluid slip).  Shows that fixed
      high-voltage drive on a thick low-k dielectric is dominated by
      displacement-current ohmic loss → η ≈ 3 %.  Illustrates that adaptive
      voltage control is essential, not optional.

  Model 3 — Tuned RIMT Performance  (optimised design — Ta₂O₅ 500 nm)
      Inverts the thrust equation: given a required thrust density, solves
      analytically for the minimum drive voltage.  With a 500 nm Ta₂O₅
      dielectric, a synchronised wave (0.2 m/s slip), and the §3.3 sawtooth
      form factor in the ohmic loss term, efficiency reaches η ≈ 83 %.

Usage
-----
    python rimt_simulation.py

Dependencies
------------
    Python ≥ 3.9
    numpy  ≥ 1.21  (pip install numpy)
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

# Ensure Unicode output works on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Physical constants  (CODATA 2018 exact values where applicable)
# ---------------------------------------------------------------------------

BOLTZMANN        : float = 1.380_649e-23     # J K⁻¹
ELEM_CHARGE      : float = 1.602_176_634e-19 # C
AVOGADRO         : float = 6.022_140_76e23   # mol⁻¹
EPSILON_0        : float = 8.854_187_817e-12 # F m⁻¹  vacuum permittivity

# Seawater physical properties at ~20 °C, 35 ppt salinity
EPSILON_R_WATER  : float = 80.0    # relative permittivity of liquid water
VISCOSITY_WATER  : float = 1.08e-3 # Pa s  dynamic viscosity of seawater (35 PSU, 20 °C)
SIGMA_SEAWATER   : float = 4.8     # S m⁻¹ electrical conductivity (3.5 % NaCl)
MOLARITY_NaCl    : float = 0.6     # mol L⁻¹  ≈ 35 ppt NaCl

# Sawtooth waveform parameters (WP §3.3 — asymmetric 1:4 rise:fall ratio)
# RMS form factor K for a sawtooth driven across a capacitive dielectric:
#   i(t) = C dV/dt  →  rectangular current (+C V_pk / t_r during rise,
#                                          −C V_pk / t_f during fall)
#   i_rms² T = (C V_pk)² (1/t_r + 1/t_f)
#   i_rms    = sigma_surf · sqrt( (1/t_r + 1/t_f) / T )
# With r = t_r / T:
#   K = sqrt( 1/r + 1/(1-r) )    so that  i_rms = K · sigma_surf · f
# For r = 0.2 (100 ns rise / 400 ns fall at 2 MHz):  K = 2.5
SAWTOOTH_RISE_FRAC   : float = 0.2  # t_r / T, fixed by WP §3.3 (100 / 500 ns)
SAWTOOTH_FORM_FACTOR : float = math.sqrt(
    1.0 / SAWTOOTH_RISE_FRAC + 1.0 / (1.0 - SAWTOOTH_RISE_FRAC)
)  # = 2.5 for r = 0.2


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------

@dataclass
class DebyeLayerResult:
    """Output of the Debye layer fundamentals analysis (Model 1)."""
    debye_length_nm   : float  # λ_D  Debye screening length [nm]
    surface_charge    : float  # σ    EDL surface charge density [C m⁻²]
    thrust_density    : float  # F/A  Coulomb body force per unit area [N m⁻²]
    eo_velocity       : float  # u_eo Smoluchowski electro-osmotic velocity [m s⁻¹]
    fluid_power       : float  # P/A  upper-bound fluid power density [W m⁻²]


@dataclass
class PerformanceResult:
    """Output of a RIMT propulsive performance model (Models 2 & 3)."""
    label             : str
    drive_voltage_V   : float  # peak drive voltage [V]
    thrust_density    : float  # F/A  [N m⁻²]
    ohmic_loss_W_m2   : float  # resistive heating loss [W m⁻²]
    viscous_loss_W_m2 : float  # slip-induced viscous dissipation [W m⁻²]
    useful_power_W    : float  # P_useful = thrust_total × v_ship [W]
    total_power_W     : float  # P_total  = useful + all losses [W]
    efficiency        : float  # η = P_useful / P_total  [0–1]


# ---------------------------------------------------------------------------
# Model 1 — Debye Layer Fundamentals
# ---------------------------------------------------------------------------

def analyse_debye_layer(
    temperature_K      : float = 293.0,
    zeta_potential_V   : float = -0.030,
    tangential_field   : float = 1.0e6,
) -> DebyeLayerResult:
    """
    Compute fundamental electro-kinetic properties of the seawater/hull interface.

    This is a theoretical upper-bound analysis.  The 1 MV/m tangential field
    is the pulsed peak achievable during the fast-rise edge of the sawtooth
    waveform; it equals V_peak / g for the §3 design point (5.3 V / 5 µm).
    It is not a sustained steady-state field.

    Parameters
    ----------
    temperature_K     : Absolute temperature [K].  Default 293 K (20 °C).
    zeta_potential_V  : Zeta potential at dielectric/electrolyte interface [V].
                        Default −30 mV (Ta₂O₅ / seawater near pH 8, literature
                        value).  The Smoluchowski / Gouy-Chapman expressions
                        below use |ζ| — the sign sets only the direction of
                        u_eo (set by E_t orientation).
    tangential_field  : Mean tangential electric field [V m⁻¹].

    Returns
    -------
    DebyeLayerResult

    Physics
    -------
    Debye screening length (linearised Poisson–Boltzmann):
        λ_D = sqrt( ε₀ ε_r k_B T / (2 n₀ e²) )

    Surface charge density (Gouy–Chapman model):
        σ = ε₀ ε_r ζ / λ_D

    Thrust density (Coulomb body force on EDL):
        F/A = σ · E_t

    Smoluchowski electro-osmotic velocity:
        u_eo = ε₀ ε_r ζ E_t / η
    """
    eps = EPSILON_0 * EPSILON_R_WATER

    # Ion number density [m⁻³]  (Na⁺ = Cl⁻ for monovalent NaCl)
    n_ions = MOLARITY_NaCl * 1_000 * AVOGADRO   # mol L⁻¹ → mol m⁻³ → ions m⁻³

    # Debye screening length [m]
    lambda_D = math.sqrt(
        (eps * BOLTZMANN * temperature_K)
        / (2.0 * n_ions * ELEM_CHARGE ** 2)
    )

    # Surface charge density magnitude [C m⁻²]  — sign drops out for force / power
    sigma = abs(eps * zeta_potential_V) / lambda_D

    # Coulomb body force per unit area [N m⁻²]  (magnitude — direction set by E_t)
    thrust_density = sigma * tangential_field

    # Smoluchowski EO velocity magnitude [m s⁻¹]
    u_eo = (eps * abs(zeta_potential_V) * tangential_field) / VISCOSITY_WATER

    # Upper-bound fluid power density [W m⁻²]  (F/A × u_eo, no loss accounted)
    fluid_power = thrust_density * u_eo

    return DebyeLayerResult(
        debye_length_nm = lambda_D * 1e9,
        surface_charge  = sigma,
        thrust_density  = thrust_density,
        eo_velocity     = u_eo,
        fluid_power     = fluid_power,
    )


# ---------------------------------------------------------------------------
# Model 2 — Parametric RIMT Performance  (baseline / untuned)
# ---------------------------------------------------------------------------

def parametric_performance(
    vessel_speed_m_s   : float,
    thrust_required_N  : float,
    hull_area_m2       : float,
    coating_thickness_m: float = 1.0e-6,   # Al₂O₃ baseline (2× thicker than Model 3)
    dielectric_er      : float = 10.0,     # Al₂O₃ (≈ half of Ta₂O₅ in Model 3)
    drive_voltage_V    : float = 200.0,    # fixed high-V baseline — V²-scaled ohmic loss is the headline failure mode
    drive_freq_Hz      : float = 2.0e6,    # §3.3 carrier
    slip_velocity_m_s  : float = 1.0,      # poorly synchronised wave (5× higher slip than Model 3)
    electrode_gap_m    : float = 10.0e-6,  # 2× looser pitch than Model 3 (longer ohmic conduction path)
    coupling_alpha     : float = 0.01,     # C_dl / (C_dl + C_diel) — see WP §4.1 derivation
    sigma_seawater     : float = SIGMA_SEAWATER,  # override for freshwater / brackish testing
) -> PerformanceResult:
    """
    Evaluate RIMT performance for an explicit hardware configuration.

    This model calculates available thrust and both loss channels (ohmic and
    viscous) for the supplied parameters, then derives propulsive efficiency.
    Default values represent a baseline, untuned design; they are intentionally
    sub-optimal to illustrate the importance of material and frequency selection.

    Parameters
    ----------
    vessel_speed_m_s    : Target vessel speed [m s⁻¹].
    thrust_required_N   : Total hull thrust needed to maintain vessel speed [N].
    hull_area_m2        : Active (wetted) hull area [m²].
    coating_thickness_m : Dielectric coating thickness [m].  Default 1 µm.
    dielectric_er       : Relative permittivity of coating.  Default 10 (alumina).
    drive_voltage_V     : Peak sawtooth waveform voltage [V].  Default 200 V.
    drive_freq_Hz       : Drive frequency [Hz].  Default 2 MHz (matches the
                          §3.3 sawtooth period of 500 ns).
    slip_velocity_m_s   : Absolute wave–fluid velocity slip [m s⁻¹].
                          Default 1.0 m/s — poorly synchronised wave.  Note:
                          this is the wave-to-fluid differential at the EDL,
                          not a fraction of vessel speed.
    electrode_gap_m     : Inter-electrode gap g [m] (seawater-conduction length
                          between adjacent fingers — WP §3.1 / §4.2).
                          Default 10 µm.
    coupling_alpha      : Fraction of coating field penetrating the Debye layer.
                          Default 0.01 — derived from the capacitive voltage
                          division between the dielectric (C_diel) and the EDL
                          (C_dl) in series: α ≈ C_dl / (C_dl + C_diel).

    Returns
    -------
    PerformanceResult

    Physics
    -------
    Capacitively induced surface charge:
        σ_surf = ε₀ ε_r V_peak / d

    Penetrating tangential field (Debye-screened):
        E_water = α · V_peak / d

    Time-averaged thrust density (sawtooth cycle):
        F/A = 0.5 · σ_surf · E_water

    Ohmic heating (displacement current to/from the dielectric capacitance):
        i(t) = C · dV/dt   for the §3.3 asymmetric sawtooth (rise:fall = 1:4)
        J_rms = K · σ_surf · f          with K = SAWTOOTH_FORM_FACTOR = 2.5
        P_ohm = J_rms² · pitch / σ_seawater

    Viscous slip dissipation:
        P_visc = (F/A)_required · v_slip

    Total power and efficiency:
        P_total  = P_useful + (P_ohm + P_visc) · A
        η        = P_useful / P_total
    """
    # ---- Input validation --------------------------------------------------
    if coating_thickness_m <= 0:
        raise ValueError("coating_thickness_m must be > 0")
    if dielectric_er <= 0:
        raise ValueError("dielectric_er must be > 0")
    if hull_area_m2 <= 0:
        raise ValueError("hull_area_m2 must be > 0")
    if drive_freq_Hz < 0:
        raise ValueError("drive_freq_Hz must be >= 0")
    if sigma_seawater <= 0:
        raise ValueError("sigma_seawater must be > 0")

    eps_coating = EPSILON_0 * dielectric_er

    # Capacitively induced surface charge density [C m⁻²]
    sigma_surf = eps_coating * drive_voltage_V / coating_thickness_m

    # Tangential field reaching the bulk electrolyte [V m⁻¹] — screened by EDL
    e_water = coupling_alpha * (drive_voltage_V / coating_thickness_m)

    # Available thrust density [N m⁻²]  (factor ½ for sawtooth time-average)
    thrust_density = 0.5 * sigma_surf * e_water

    # Required thrust density [N m⁻²]  (actual operating point)
    thrust_density_required = thrust_required_N / hull_area_m2

    # Ohmic heating loss per unit area [W m⁻²]
    # Displacement current through the dielectric capacitor; sawtooth form factor
    # applies for the §3.3 1:4 asymmetric waveform.  See SAWTOOTH_FORM_FACTOR.
    # Conduction-length factor is the inter-electrode gap g (WP §4.2).
    j_rms = SAWTOOTH_FORM_FACTOR * sigma_surf * drive_freq_Hz
    p_ohmic = (j_rms ** 2 * electrode_gap_m) / sigma_seawater

    # Viscous slip loss per unit area [W m⁻²]
    # Uses the *required* thrust density, not the available one.
    # v_slip is the absolute wave–fluid velocity differential at the EDL,
    # independent of vessel speed.
    p_viscous = thrust_density_required * slip_velocity_m_s

    # Power budget
    useful_power = thrust_required_N * vessel_speed_m_s
    loss_power   = (p_ohmic + p_viscous) * hull_area_m2
    total_power  = useful_power + loss_power

    return PerformanceResult(
        label           = "Model 2 — Baseline (alumina 1 µm, 200 V, 2 MHz, 1.0 m/s slip)",
        drive_voltage_V = drive_voltage_V,
        thrust_density  = thrust_density,
        ohmic_loss_W_m2 = p_ohmic,
        viscous_loss_W_m2 = p_viscous,
        useful_power_W  = useful_power,
        total_power_W   = total_power,
        efficiency      = useful_power / total_power,
    )


# ---------------------------------------------------------------------------
# Model 3 — Tuned RIMT Performance  (Ta₂O₅ 500 nm — optimised)
# ---------------------------------------------------------------------------

def tuned_performance(
    vessel_speed_m_s         : float,
    hull_area_m2             : float,
    thrust_density_N_m2      : float,
    coating_thickness_m      : float = 0.5e-6,   # Ta₂O₅ ALD (2× thinner than Model 2 baseline)
    dielectric_er            : float = 20.0,     # Ta₂O₅ (≈ 2× higher k than Model 2's Al₂O₃)
    drive_freq_Hz            : float = 2.0e6,    # §3.3 carrier
    slip_velocity_m_s        : float = 0.2,      # synchronised wave — small residual slip
    electrode_gap_m          : float = 5.0e-6,   # 2× tighter pitch than Model 2 (shorter ohmic path)
    coupling_alpha           : float = 0.005,    # C_dl / (C_dl + C_diel) — see WP §4.1; smaller than Model 2 because thinner / higher-k dielectric stores more of V on its own capacitance
    sigma_seawater           : float = SIGMA_SEAWATER,  # override for freshwater / brackish testing
) -> PerformanceResult:
    """
    Compute the minimum drive voltage and achievable efficiency for an optimised
    RIMT configuration.

    Unlike Model 2, this model is design-driven: the required thrust density is
    the input, and the drive voltage is solved analytically.  Default parameters
    represent the Ta₂O₅ 500 nm ALD design described in the SSIH whitepaper.

    Parameters
    ----------
    vessel_speed_m_s       : Target vessel speed [m s⁻¹].
    hull_area_m2           : Active hull area [m²].
    thrust_density_N_m2    : Required thrust per unit area [N m⁻²].
                             Typical 10 m boat at 20 knots: ~50 N m⁻².
    coating_thickness_m    : Dielectric thickness [m].  Default 500 nm (Ta₂O₅ ALD).
    dielectric_er          : Relative permittivity.  Default 20 (Ta₂O₅ ≈ 20–25).
    drive_freq_Hz          : Drive frequency [Hz].  Default 2 MHz.
    slip_velocity_m_s      : Absolute wave–fluid velocity slip [m s⁻¹].
                             Default 0.2 m/s — synchronised wave, small residual.
    electrode_gap_m        : Inter-electrode gap g [m].  Default 5 µm.
    coupling_alpha         : Debye-screening penetration factor.  Default 0.005
                             (capacitive division between thin Ta₂O₅ and the
                             diffuse EDL — smaller than alumina case because
                             the thinner / higher-k dielectric stores more of
                             the applied voltage on its own capacitance).

    Returns
    -------
    PerformanceResult

    Physics — voltage inversion
    ---------------------------
    From  F/A = (ε₀ ε_r α / 2d²) · V²  →  V = sqrt( F/A · 2d² / (ε₀ ε_r α) )
    """
    # ---- Input validation --------------------------------------------------
    if coating_thickness_m <= 0:
        raise ValueError("coating_thickness_m must be > 0")
    if dielectric_er <= 0:
        raise ValueError("dielectric_er must be > 0")
    if hull_area_m2 <= 0:
        raise ValueError("hull_area_m2 must be > 0")
    if thrust_density_N_m2 < 0:
        raise ValueError("thrust_density_N_m2 must be >= 0")
    if drive_freq_Hz < 0:
        raise ValueError("drive_freq_Hz must be >= 0")
    if coupling_alpha <= 0:
        raise ValueError("coupling_alpha must be > 0")
    if sigma_seawater <= 0:
        raise ValueError("sigma_seawater must be > 0")

    eps_coating = EPSILON_0 * dielectric_er

    # Invert the thrust equation to find the required drive voltage [V]
    thrust_coeff = (0.5 * eps_coating * coupling_alpha) / (coating_thickness_m ** 2)
    drive_voltage = math.sqrt(thrust_density_N_m2 / thrust_coeff)

    # Surface charge density at the solved voltage [C m⁻²]
    sigma_surf = eps_coating * drive_voltage / coating_thickness_m

    # Ohmic heating loss [W m⁻²]
    # Displacement current with §3.3 sawtooth form factor (see module-level note).
    j_rms  = SAWTOOTH_FORM_FACTOR * sigma_surf * drive_freq_Hz
    p_ohmic = (j_rms ** 2 * electrode_gap_m) / sigma_seawater

    # Viscous slip loss [W m⁻²]  — absolute wave-fluid velocity differential
    p_viscous = thrust_density_N_m2 * slip_velocity_m_s

    # Power budget per unit area [W m⁻²]
    useful_per_m2 = thrust_density_N_m2 * vessel_speed_m_s
    total_per_m2  = useful_per_m2 + p_ohmic + p_viscous

    efficiency = useful_per_m2 / total_per_m2

    return PerformanceResult(
        label             = "Model 3 — Optimised (Ta₂O₅ 500 nm, 2 MHz, 0.2 m/s slip)",
        drive_voltage_V   = drive_voltage,
        thrust_density    = thrust_density_N_m2,
        ohmic_loss_W_m2   = p_ohmic,
        viscous_loss_W_m2 = p_viscous,
        useful_power_W    = useful_per_m2 * hull_area_m2,
        total_power_W     = total_per_m2  * hull_area_m2,
        efficiency        = efficiency,
    )


# ---------------------------------------------------------------------------
# Formatted output helpers
# ---------------------------------------------------------------------------

def _print_section(title: str) -> None:
    width = 62
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def _print_debye(r: DebyeLayerResult) -> None:
    print(f"  Debye length         λ_D = {r.debye_length_nm:.4f} nm")
    print(f"  Surface charge         σ = {r.surface_charge:.4f} C m⁻²")
    print(f"  Thrust density       F/A = {r.thrust_density:,.1f} N m⁻²")
    print(f"  EO velocity         u_eo = {r.eo_velocity*1000:.2f} mm s⁻¹")
    print(f"  Fluid power density  P/A = {r.fluid_power/1000:,.1f} kW m⁻²")


def _print_perf(r: PerformanceResult) -> None:
    print(f"  {r.label}")
    print(f"  Drive voltage          V = {r.drive_voltage_V:.2f} V")
    print(f"  Thrust density       F/A = {r.thrust_density:.1f} N m⁻²")
    print(f"  Ohmic loss         P_ohm = {r.ohmic_loss_W_m2:.2f} W m⁻²")
    print(f"  Viscous slip loss  P_vis = {r.viscous_loss_W_m2:.2f} W m⁻²")
    print(f"  Useful power      P_use  = {r.useful_power_W/1000:.2f} kW")
    print(f"  Total power       P_tot  = {r.total_power_W/1000:.2f} kW")
    print(f"  Propulsive efficiency  η = {r.efficiency*100:.1f} %")


# ---------------------------------------------------------------------------
# Main — reference scenario: 10 m boat, 30 m² hull, 10 m/s (≈ 20 knots)
# ---------------------------------------------------------------------------

def main() -> None:
    VESSEL_SPEED   = 10.0   # m/s  (~20 knots)
    HULL_AREA      = 30.0   # m²
    THRUST_TOTAL   = 1_500  # N    (to sustain cruise speed)
    THRUST_PER_M2  = THRUST_TOTAL / HULL_AREA  # = 50 N m⁻²

    print()
    print("  RIMT Simulation Suite — Project Leviathan")
    print(f"  Scenario: {HULL_AREA} m² hull, {VESSEL_SPEED} m/s, {THRUST_TOTAL} N required")

    # --- Model 1 ---
    _print_section("Model 1 — Debye Layer Fundamentals (upper-bound analysis)")
    r1 = analyse_debye_layer()
    _print_debye(r1)
    print()
    print("  NOTE: 1 MV/m is the pulsed peak field on the fast-rise edge of")
    print("  the sawtooth (≈ V_peak / electrode_gap), not a continuous level.")
    print(f"  Required for scenario:  {THRUST_PER_M2:.0f} N m⁻²  (factor {r1.thrust_density/THRUST_PER_M2:,.0f}× headroom)")

    # --- Model 2 ---
    _print_section("Model 2 — Baseline Design (untuned parameters)")
    r2 = parametric_performance(
        vessel_speed_m_s  = VESSEL_SPEED,
        thrust_required_N = THRUST_TOTAL,
        hull_area_m2      = HULL_AREA,
    )
    _print_perf(r2)
    print()
    print("  Dominant loss: displacement-current ohmic heating from the high")
    print("  fixed drive voltage on a thick low-k dielectric.  Illustrates why")
    print("  adaptive voltage control + thin high-k dielectric are required.")

    # --- Model 3 ---
    _print_section("Model 3 — Optimised Design (Ta₂O₅ 500 nm, synchronised wave)")
    r3 = tuned_performance(
        vessel_speed_m_s    = VESSEL_SPEED,
        hull_area_m2        = HULL_AREA,
        thrust_density_N_m2 = THRUST_PER_M2,
    )
    _print_perf(r3)

    # --- Comparison ---
    _print_section("Comparison Summary")
    print(f"  {'Design':<40}  {'η':>6}  {'V_drive':>9}")
    print(f"  {'-'*40}  {'-'*6}  {'-'*9}")
    print(f"  {'Baseline (Model 2)':<40}  {r2.efficiency*100:>5.1f}%  {r2.drive_voltage_V:>8.1f}V")
    print(f"  {'Optimised — Ta₂O₅ 500 nm (Model 3)':<40}  {r3.efficiency*100:>5.1f}%  {r3.drive_voltage_V:>8.2f}V")
    print()
    print("  Efficiency gain from material + synchronisation optimisation:")
    delta = (r3.efficiency - r2.efficiency) * 100
    print(f"  Δη = {delta:+.1f} percentage points")
    print()


if __name__ == "__main__":
    main()
