#!/usr/bin/env python3
"""
test_rimt_simulation.py — Unit tests for RIMT simulation models
================================================================

Run with:
    python -m pytest test_rimt_simulation.py -v
    # or:
    python test_rimt_simulation.py
"""

import io
import math
import unittest
from contextlib import redirect_stdout

from rimt_simulation import (
    analyse_debye_layer,
    parametric_performance,
    tuned_performance,
    sensitivity_sweep,
    main,
    DebyeLayerResult,
    PerformanceResult,
    SensitivityPoint,
    EPSILON_0,
    EPSILON_R_WATER,
    VISCOSITY_WATER,
    ELEM_CHARGE,
    BOLTZMANN,
    AVOGADRO,
    MOLARITY_NaCl,
    SAWTOOTH_RISE_FRAC,
    SAWTOOTH_FORM_FACTOR,
)


# ---------------------------------------------------------------------------
# Shared test scenario (10 m boat, 30 m² hull, 20 knots)
# ---------------------------------------------------------------------------

VESSEL_SPEED  = 10.0   # m/s
HULL_AREA     = 30.0   # m²
THRUST_TOTAL  = 1_500  # N
THRUST_PER_M2 = THRUST_TOTAL / HULL_AREA   # 50 N m⁻²


# ---------------------------------------------------------------------------
# Model 1 — Debye Layer
# ---------------------------------------------------------------------------

class TestDebyeLayer(unittest.TestCase):

    def setUp(self):
        self.r = analyse_debye_layer()

    def test_return_type(self):
        self.assertIsInstance(self.r, DebyeLayerResult)

    def test_debye_length_order_of_magnitude(self):
        """λ_D in 0.6 M NaCl is ~0.39–0.40 nm (well-established textbook value)."""
        self.assertAlmostEqual(self.r.debye_length_nm, 0.393, delta=0.01)

    def test_surface_charge_positive(self):
        """Magnitude of EDL surface charge density is always positive."""
        self.assertGreater(self.r.surface_charge, 0)

    def test_thrust_density_positive(self):
        self.assertGreater(self.r.thrust_density, 0)

    def test_thrust_density_far_exceeds_requirement(self):
        """At 1 MV/m the available thrust density is orders of magnitude above the
        ~50 N m⁻² needed for propulsion — confirms large physical headroom."""
        self.assertGreater(self.r.thrust_density, THRUST_PER_M2 * 100)

    def test_eo_velocity_smoluchowski(self):
        """
        Verify Smoluchowski formula manually against default ζ = -30 mV
        and seawater viscosity 1.08e-3 Pa·s:
            u = ε₀ ε_r |ζ| E / μ
        """
        eps = EPSILON_0 * EPSILON_R_WATER
        expected = (eps * abs(-0.030) * 1e6) / VISCOSITY_WATER
        self.assertAlmostEqual(self.r.eo_velocity, expected, places=6)

    def test_eo_velocity_range(self):
        """At |ζ| = 30 mV and 1 MV/m field, EO velocity is ~19.7 mm/s."""
        self.assertAlmostEqual(self.r.eo_velocity * 1000, 19.7, delta=0.5)

    def test_zeta_default_matches_whitepaper(self):
        """Default ζ is the literature value for Ta₂O₅/seawater (≈ -30 mV)."""
        r = analyse_debye_layer()
        # We can't read ζ directly; verify via the EO velocity proportionality
        r_double = analyse_debye_layer(zeta_potential_V=-0.060)
        self.assertAlmostEqual(r_double.eo_velocity / r.eo_velocity, 2.0, places=5)

    def test_zeta_sign_invariant(self):
        """Surface charge magnitude and u_eo magnitude must not depend on ζ sign."""
        r_neg = analyse_debye_layer(zeta_potential_V=-0.030)
        r_pos = analyse_debye_layer(zeta_potential_V=+0.030)
        self.assertAlmostEqual(r_neg.surface_charge, r_pos.surface_charge, places=12)
        self.assertAlmostEqual(r_neg.eo_velocity,    r_pos.eo_velocity,    places=12)

    def test_fluid_power_equals_thrust_times_velocity(self):
        """Fluid power P/A should equal thrust density × EO velocity."""
        expected = self.r.thrust_density * self.r.eo_velocity
        self.assertAlmostEqual(self.r.fluid_power, expected, places=3)

    def test_custom_temperature(self):
        """Higher temperature → longer Debye length (more thermal disorder)."""
        r_cold = analyse_debye_layer(temperature_K=273.0)
        r_warm = analyse_debye_layer(temperature_K=303.0)
        self.assertLess(r_cold.debye_length_nm, r_warm.debye_length_nm)

    def test_custom_zeta_scales_thrust(self):
        """Doubling |ζ| should double both surface charge and thrust."""
        r1 = analyse_debye_layer(zeta_potential_V=-0.025)
        r2 = analyse_debye_layer(zeta_potential_V=-0.050)
        self.assertAlmostEqual(r2.surface_charge / r1.surface_charge, 2.0, places=5)
        self.assertAlmostEqual(r2.thrust_density  / r1.thrust_density,  2.0, places=5)


# ---------------------------------------------------------------------------
# Model 2 — Parametric Performance
# ---------------------------------------------------------------------------

class TestParametricPerformance(unittest.TestCase):

    def setUp(self):
        self.r = parametric_performance(
            vessel_speed_m_s  = VESSEL_SPEED,
            thrust_required_N = THRUST_TOTAL,
            hull_area_m2      = HULL_AREA,
        )

    def test_return_type(self):
        self.assertIsInstance(self.r, PerformanceResult)

    def test_efficiency_physical_range(self):
        """Efficiency must be strictly between 0 and 1."""
        self.assertGreater(self.r.efficiency, 0.0)
        self.assertLess(self.r.efficiency,    1.0)

    def test_total_power_exceeds_useful(self):
        """Total power = useful + losses; must always exceed useful alone."""
        self.assertGreater(self.r.total_power_W, self.r.useful_power_W)

    def test_useful_power_correct(self):
        """Useful power = thrust × speed = 1500 N × 10 m/s = 15 000 W."""
        self.assertAlmostEqual(self.r.useful_power_W, 15_000.0, places=1)

    def test_losses_positive(self):
        self.assertGreater(self.r.ohmic_loss_W_m2,   0.0)
        self.assertGreater(self.r.viscous_loss_W_m2,  0.0)

    def test_efficiency_below_optimised(self):
        """Untuned design must achieve lower efficiency than the optimised Model 3."""
        r3 = tuned_performance(
            vessel_speed_m_s    = VESSEL_SPEED,
            hull_area_m2        = HULL_AREA,
            thrust_density_N_m2 = THRUST_PER_M2,
        )
        self.assertLess(self.r.efficiency, r3.efficiency)

    def test_higher_slip_lowers_efficiency(self):
        """Increasing absolute wave–fluid slip should reduce propulsive efficiency."""
        r_low  = parametric_performance(VESSEL_SPEED, THRUST_TOTAL, HULL_AREA, slip_velocity_m_s=0.5)
        r_high = parametric_performance(VESSEL_SPEED, THRUST_TOTAL, HULL_AREA, slip_velocity_m_s=2.0)
        self.assertGreater(r_low.efficiency, r_high.efficiency)

    def test_power_balance(self):
        """P_total must equal P_useful + (P_ohmic + P_viscous) × hull_area."""
        expected = (
            self.r.useful_power_W
            + (self.r.ohmic_loss_W_m2 + self.r.viscous_loss_W_m2) * HULL_AREA
        )
        self.assertAlmostEqual(self.r.total_power_W, expected, places=2)


# ---------------------------------------------------------------------------
# Model 3 — Tuned Performance
# ---------------------------------------------------------------------------

class TestTunedPerformance(unittest.TestCase):

    def setUp(self):
        self.r = tuned_performance(
            vessel_speed_m_s    = VESSEL_SPEED,
            hull_area_m2        = HULL_AREA,
            thrust_density_N_m2 = THRUST_PER_M2,
        )

    def test_return_type(self):
        self.assertIsInstance(self.r, PerformanceResult)

    def test_efficiency_matches_whitepaper(self):
        """Whitepaper Section 4.4 reports η ≈ 83 % for this configuration
        (post-Phase-6 correction: sawtooth form factor, seawater viscosity,
        literature ζ, absolute wave-fluid slip)."""
        self.assertAlmostEqual(self.r.efficiency, 0.83, delta=0.01)

    def test_efficiency_above_propeller_ceiling(self):
        """Optimised design must exceed the practical propeller ceiling (~72 %)."""
        self.assertGreater(self.r.efficiency, 0.72)

    def test_drive_voltage_low(self):
        """
        Whitepaper reports ~5.3 V drive voltage; must be in a physically
        plausible range (1–20 V at 500 nm Ta₂O₅).
        """
        self.assertGreater(self.r.drive_voltage_V, 1.0)
        self.assertLess(   self.r.drive_voltage_V, 20.0)

    def test_drive_voltage_matches_whitepaper(self):
        """Whitepaper reports V_req ≈ 5.31 V."""
        self.assertAlmostEqual(self.r.drive_voltage_V, 5.31, delta=0.05)

    def test_ohmic_loss_bounded(self):
        """Ohmic heating under the §3.3 sawtooth form factor is the dominant
        loss in the optimised design (~92 W/m² ≈ 18 % of useful per-area
        power).  Must stay below useful power per unit area."""
        useful_per_m2 = THRUST_PER_M2 * VESSEL_SPEED  # 500 W m⁻²
        self.assertLess(self.r.ohmic_loss_W_m2, useful_per_m2)

    def test_total_power_exceeds_useful(self):
        self.assertGreater(self.r.total_power_W, self.r.useful_power_W)

    def test_power_balance(self):
        """η = P_useful / P_total must hold."""
        eta_check = self.r.useful_power_W / self.r.total_power_W
        self.assertAlmostEqual(self.r.efficiency, eta_check, places=6)

    def test_thinner_coating_lowers_voltage(self):
        """Thinner dielectric → stronger capacitive coupling → lower required voltage."""
        r_thick = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, coating_thickness_m=1.0e-6)
        r_thin  = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, coating_thickness_m=0.5e-6)
        self.assertGreater(r_thick.drive_voltage_V, r_thin.drive_voltage_V)

    def test_higher_er_lowers_voltage(self):
        """Higher-k dielectric → more surface charge per volt → lower voltage needed."""
        r_low_k  = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, dielectric_er=10.0)
        r_high_k = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, dielectric_er=20.0)
        self.assertGreater(r_low_k.drive_voltage_V, r_high_k.drive_voltage_V)

    def test_thrust_density_preserved(self):
        """Model 3 must deliver exactly the requested thrust density."""
        self.assertAlmostEqual(self.r.thrust_density, THRUST_PER_M2, places=6)


# ---------------------------------------------------------------------------
# Cross-model sanity
# ---------------------------------------------------------------------------

class TestCrossModel(unittest.TestCase):

    def test_model3_efficiency_always_beats_model2_at_same_scenario(self):
        """Optimised parameters must outperform untuned ones under identical load."""
        r2 = parametric_performance(VESSEL_SPEED, THRUST_TOTAL, HULL_AREA)
        r3 = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2)
        self.assertGreater(r3.efficiency, r2.efficiency)

    def test_model1_debye_length_consistent_with_model3_voltage(self):
        """
        Model 1 Debye length should be sub-nanometre for seawater;
        Model 3 must still achieve thrust efficiency exceeding the propeller
        ceiling at 500 nm coating — confirming that the dielectric fully
        spans the Debye layer.
        """
        r1 = analyse_debye_layer()
        r3 = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2)
        coating_nm = 500.0
        self.assertGreater(coating_nm, r1.debye_length_nm)   # coating >> λ_D
        self.assertGreater(r3.efficiency, 0.72)              # exceeds propeller ceiling


# ---------------------------------------------------------------------------
# Sawtooth form factor (regression guard for Phase-6 fix #1)
# ---------------------------------------------------------------------------

class TestSawtoothFormFactor(unittest.TestCase):

    def test_form_factor_value_for_1_to_4_ratio(self):
        """For r = 0.2 (100 ns rise / 400 ns fall), K = sqrt(5 + 1.25) = 2.5."""
        self.assertAlmostEqual(SAWTOOTH_RISE_FRAC, 0.2, places=6)
        self.assertAlmostEqual(SAWTOOTH_FORM_FACTOR, 2.5, places=6)

    def test_form_factor_used_in_ohmic_loss(self):
        """
        Regression guard for the Phase-6 #1 fix: the ohmic-loss formula must
        use the sawtooth form factor (K · σ_surf · f), not σ_surf · f / √2.
        Re-derives p_ohmic from Model 3 inputs and compares to the result.
        """
        r3 = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2)
        eps_coat = EPSILON_0 * 20.0  # Ta₂O₅
        sigma_surf = eps_coat * r3.drive_voltage_V / 0.5e-6
        j_rms_expected = SAWTOOTH_FORM_FACTOR * sigma_surf * 2.0e6
        p_ohm_expected = j_rms_expected ** 2 * 5.0e-6 / 4.8
        self.assertAlmostEqual(r3.ohmic_loss_W_m2, p_ohm_expected, delta=0.5)


# ---------------------------------------------------------------------------
# Input validation (regression guard for Phase-7 F-F7 fix)
# ---------------------------------------------------------------------------

class TestInputValidation(unittest.TestCase):

    def test_model2_rejects_nonpositive_coating(self):
        with self.assertRaises(ValueError):
            parametric_performance(VESSEL_SPEED, THRUST_TOTAL, HULL_AREA, coating_thickness_m=0.0)

    def test_model2_rejects_nonpositive_er(self):
        with self.assertRaises(ValueError):
            parametric_performance(VESSEL_SPEED, THRUST_TOTAL, HULL_AREA, dielectric_er=0.0)

    def test_model3_rejects_nonpositive_coating(self):
        with self.assertRaises(ValueError):
            tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, coating_thickness_m=-1e-6)

    def test_model3_rejects_nonpositive_alpha(self):
        with self.assertRaises(ValueError):
            tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, coupling_alpha=0.0)

    def test_model3_rejects_nonpositive_sigma_seawater(self):
        with self.assertRaises(ValueError):
            tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, sigma_seawater=0.0)


# ---------------------------------------------------------------------------
# Salinity edge case: lower σ_seawater → higher ohmic loss → lower η
# (Phase-7 F-F7 fix: SIGMA_SEAWATER is now a parameter override.)
# ---------------------------------------------------------------------------

class TestSalinityOverride(unittest.TestCase):

    def test_lower_conductivity_lowers_efficiency(self):
        """Brackish (σ ≈ 0.5 S/m) must yield lower η than open ocean (σ ≈ 5 S/m)."""
        r_ocean    = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, sigma_seawater=4.8)
        r_brackish = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, sigma_seawater=0.5)
        self.assertGreater(r_ocean.efficiency, r_brackish.efficiency)

    def test_lower_conductivity_raises_ohmic_loss(self):
        r_ocean    = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, sigma_seawater=4.8)
        r_brackish = tuned_performance(VESSEL_SPEED, HULL_AREA, THRUST_PER_M2, sigma_seawater=0.5)
        self.assertGreater(r_brackish.ohmic_loss_W_m2, r_ocean.ohmic_loss_W_m2)


# ---------------------------------------------------------------------------
# Main entrypoint smoke test (regression guard for README "Expected output")
# ---------------------------------------------------------------------------

class TestMainSmoke(unittest.TestCase):
    """Capture main() stdout and assert the headline numbers / labels render.

    If main()'s format strings drift from the values asserted in the README
    "Expected output" block, this test fires immediately. Cheap regression
    guard for the cross-doc invariants in [[project-rimt-data-sync-registry]].
    """

    def setUp(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main()
        self.out = buf.getvalue()

    def test_headline_efficiencies_present(self):
        self.assertIn("3.0 %", self.out)
        self.assertIn("83.0 %", self.out)

    def test_drive_voltages_present(self):
        self.assertIn("200.00 V", self.out)
        self.assertIn("5.31 V", self.out)

    def test_model_labels_present(self):
        self.assertIn("Baseline (Model 2)", self.out)
        self.assertIn("Optimised", self.out)


# ---------------------------------------------------------------------------
# Sensitivity sweep — WP §4.4.2
# ---------------------------------------------------------------------------

class TestSensitivitySweep(unittest.TestCase):
    """Validate sensitivity_sweep output structure and monotone behaviour."""

    def setUp(self):
        self.sweep = sensitivity_sweep(
            vessel_speed_m_s    = VESSEL_SPEED,
            thrust_density_N_m2 = THRUST_PER_M2,
        )

    def test_returns_all_four_axes(self):
        """Result dict must contain exactly the four documented axes."""
        self.assertEqual(set(self.sweep.keys()), {"alpha", "v_slip", "sigma", "f_c"})

    def test_each_point_is_sensitivity_point(self):
        """Every element in every axis must be a SensitivityPoint."""
        for pts in self.sweep.values():
            for pt in pts:
                self.assertIsInstance(pt, SensitivityPoint)
                self.assertIsInstance(pt.result, PerformanceResult)

    def test_reference_point_reproduces_headline(self):
        """α = 0.005, v_slip = 0.2, σ = 5.0, f_c = 2 MHz → η ≈ 83 % (±2 %)."""
        alpha_pts = self.sweep["alpha"]
        ref = next(p for p in alpha_pts if abs(p.param_value - 0.005) < 1e-9)
        self.assertAlmostEqual(ref.result.efficiency, 0.83, delta=0.02)

    def test_alpha_axis_monotone_increasing(self):
        """η must increase strictly as α increases (higher coupling → less ohmic loss)."""
        etas = [p.result.efficiency for p in self.sweep["alpha"]]
        self.assertTrue(all(etas[i] < etas[i+1] for i in range(len(etas)-1)))

    def test_v_slip_axis_monotone_decreasing(self):
        """η must decrease as v_slip increases (more viscous dissipation)."""
        etas = [p.result.efficiency for p in self.sweep["v_slip"]]
        self.assertTrue(all(etas[i] > etas[i+1] for i in range(len(etas)-1)))

    def test_sigma_axis_monotone_increasing(self):
        """η must increase with σ_seawater (higher conductivity → lower ohmic loss)."""
        etas = [p.result.efficiency for p in self.sweep["sigma"]]
        self.assertTrue(all(etas[i] < etas[i+1] for i in range(len(etas)-1)))

    def test_fc_axis_monotone_decreasing(self):
        """η must fall sharply as f_c rises (ohmic loss scales as f²)."""
        etas = [p.result.efficiency for p in self.sweep["f_c"]]
        self.assertTrue(all(etas[i] > etas[i+1] for i in range(len(etas)-1)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
