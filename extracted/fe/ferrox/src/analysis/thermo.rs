//! Finite-temperature gas-phase thermodynamics for convex hull analysis.
//!
//! Extends the 0 K convex hull with temperature- and pressure-dependent gas
//! chemical potentials using NIST-JANAF Shomate equation fits. Capabilities:
//!
//! - Gas-phase Gibbs free energies G(T,P) for common atmospheric gases
//! - Formation energy corrections for open systems in gaseous atmospheres
//! - Temperature-dependent phase stability (e_above_hull at finite T)

use crate::analysis::convex_hull::{ConvexHullEntry, calculate_e_above_hull};
use crate::element::Element;
use crate::error::{FerroxError, Result};
use std::collections::HashMap;

// === Physical Constants ===

/// Boltzmann constant in eV/K.
const K_BOLTZMANN_EV: f64 = 8.617_333_262e-5;

/// Conversion factor from kJ/mol to eV per molecule (1 eV = 96.485 kJ/mol).
const KJ_PER_MOL_TO_EV: f64 = 1.0 / 96.485_332_12;

/// IUPAC standard reference pressure in bar.
const P_REF_BAR: f64 = 1.0;

/// Conversion factor from atm to bar.
const ATM_TO_BAR: f64 = 1.01325;

// === Gas Species ===

/// Supported gas-phase species for thermodynamic calculations.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum GasSpecies {
    /// Molecular oxygen.
    O2,
    /// Molecular nitrogen.
    N2,
    /// Molecular hydrogen.
    H2,
    /// Water vapor.
    H2O,
    /// Carbon dioxide.
    CO2,
    /// Molecular fluorine.
    F2,
    /// Molecular chlorine.
    Cl2,
    /// Sulfur dioxide.
    SO2,
    /// Ammonia.
    NH3,
}

impl GasSpecies {
    /// Number of atoms per molecule.
    pub fn num_atoms(&self) -> u8 {
        match self {
            Self::O2 | Self::N2 | Self::H2 | Self::F2 | Self::Cl2 => 2,
            Self::H2O | Self::CO2 | Self::SO2 => 3,
            Self::NH3 => 4,
        }
    }

    /// Standard formation enthalpy ΔH_f at 298.15 K in kJ/mol.
    pub fn formation_enthalpy_kj_per_mol(&self) -> f64 {
        match self {
            Self::O2 | Self::N2 | Self::H2 | Self::F2 | Self::Cl2 => 0.0,
            Self::H2O => -241.8264,
            Self::CO2 => -393.5224,
            Self::SO2 => -296.8100,
            Self::NH3 => -45.89806,
        }
    }

    /// Element-stoichiometry pairs: which elements and how many per molecule.
    pub fn element_stoichiometry(&self) -> &'static [(Element, u8)] {
        match self {
            Self::O2 => &[(Element::O, 2)],
            Self::N2 => &[(Element::N, 2)],
            Self::H2 => &[(Element::H, 2)],
            Self::F2 => &[(Element::F, 2)],
            Self::Cl2 => &[(Element::Cl, 2)],
            Self::H2O => &[(Element::H, 2), (Element::O, 1)],
            Self::CO2 => &[(Element::C, 1), (Element::O, 2)],
            Self::SO2 => &[(Element::S, 1), (Element::O, 2)],
            Self::NH3 => &[(Element::N, 1), (Element::H, 3)],
        }
    }
}

// === Shomate Equation ===

/// NIST-JANAF Shomate equation coefficients for a temperature range.
///
/// Cp° = A + B·t + C·t² + D·t³ + E/t²
/// H°−H°298 = A·t + B·t²/2 + C·t³/3 + D·t⁴/4 − E/t + F − H  (kJ/mol)
/// S° = A·ln(t) + B·t + C·t²/2 + D·t³/3 − E/(2·t²) + G  (J/(mol·K))
///
/// where t = T(K) / 1000.
#[derive(Debug, Clone, Copy)]
struct ShomateRange {
    t_min: f64,
    t_max: f64,
    a: f64,
    b: f64,
    c: f64,
    d: f64,
    e: f64,
    f: f64,
    g: f64,
    h: f64,
}

// === NIST-JANAF Shomate Coefficient Data ===
// Source: NIST Chemistry WebBook (https://webbook.nist.gov)

#[rustfmt::skip]
static O2_SHOMATE: [ShomateRange; 3] = [
    ShomateRange { t_min: 100.0, t_max: 700.0,
        a: 31.32234, b: -20.23531, c: 57.86644, d: -36.50624, e: -0.007374, f: -8.903471, g: 246.7945, h: 0.0 },
    ShomateRange { t_min: 700.0, t_max: 2000.0,
        a: 30.03235, b: 8.772972, c: -3.988133, d: 0.788313, e: -0.741599, f: -11.32468, g: 236.1663, h: 0.0 },
    ShomateRange { t_min: 2000.0, t_max: 6000.0,
        a: 20.91111, b: 10.72071, c: -2.020498, d: 0.146449, e: 9.245722, f: 5.337651, g: 237.6185, h: 0.0 },
];

#[rustfmt::skip]
static N2_SHOMATE: [ShomateRange; 3] = [
    ShomateRange { t_min: 100.0, t_max: 500.0,
        a: 28.98641, b: 1.853978, c: -9.647459, d: 16.63537, e: 0.000117, f: -8.671914, g: 226.4168, h: 0.0 },
    ShomateRange { t_min: 500.0, t_max: 2000.0,
        a: 19.50583, b: 19.88705, c: -8.598535, d: 1.369784, e: 0.527601, f: -4.935202, g: 212.3900, h: 0.0 },
    ShomateRange { t_min: 2000.0, t_max: 6000.0,
        a: 35.51872, b: 1.128728, c: -0.196103, d: 0.014662, e: -4.553760, f: -18.97091, g: 224.9810, h: 0.0 },
];

#[rustfmt::skip]
static H2_SHOMATE: [ShomateRange; 3] = [
    ShomateRange { t_min: 298.0, t_max: 1000.0,
        a: 33.066178, b: -11.363417, c: 11.432816, d: -2.772874, e: -0.158558, f: -9.980797, g: 172.707974, h: 0.0 },
    ShomateRange { t_min: 1000.0, t_max: 2500.0,
        a: 18.563083, b: 12.257357, c: -2.859786, d: 0.268238, e: 1.977990, f: -1.147438, g: 156.288133, h: 0.0 },
    ShomateRange { t_min: 2500.0, t_max: 6000.0,
        a: 43.413560, b: -4.293079, c: 1.272428, d: -0.096876, e: -20.533862, f: -38.515158, g: 162.081354, h: 0.0 },
];

#[rustfmt::skip]
// Gas-phase only; liquid H₂O below ~373 K means no gas Shomate data below 500 K.
// Temperatures below 500 K are clamped to the 500 K boundary.
static H2O_SHOMATE: [ShomateRange; 2] = [
    ShomateRange { t_min: 500.0, t_max: 1700.0,
        a: 30.09200, b: 6.832514, c: 6.793435, d: -2.534480, e: 0.082139, f: -250.8810, g: 223.3967, h: -241.8264 },
    ShomateRange { t_min: 1700.0, t_max: 6000.0,
        a: 41.96426, b: 8.622053, c: -1.499780, d: 0.098119, e: -11.15764, f: -272.1797, g: 219.7809, h: -241.8264 },
];

#[rustfmt::skip]
static CO2_SHOMATE: [ShomateRange; 2] = [
    ShomateRange { t_min: 298.0, t_max: 1200.0,
        a: 24.99735, b: 55.18696, c: -33.69137, d: 7.948387, e: -0.136638, f: -403.6075, g: 228.2431, h: -393.5224 },
    ShomateRange { t_min: 1200.0, t_max: 6000.0,
        a: 58.16639, b: 2.720074, c: -0.492289, d: 0.038844, e: -6.447293, f: -425.9186, g: 263.6125, h: -393.5224 },
];

#[rustfmt::skip]
static F2_SHOMATE: [ShomateRange; 1] = [
    ShomateRange { t_min: 298.0, t_max: 6000.0,
        a: 31.30420, b: 8.745340, c: -3.177980, d: 0.573712, e: -0.196576, f: -10.41308, g: 237.6790, h: 0.0 },
];

#[rustfmt::skip]
static CL2_SHOMATE: [ShomateRange; 2] = [
    ShomateRange { t_min: 298.0, t_max: 1000.0,
        a: 33.05060, b: 12.22940, c: -12.06510, d: 4.385330, e: -0.159494, f: -10.83480, g: 259.0290, h: 0.0 },
    ShomateRange { t_min: 1000.0, t_max: 3000.0,
        a: 42.67730, b: -5.009540, c: 1.904621, d: -0.165641, e: -2.098480, f: -18.27120, g: 266.0550, h: 0.0 },
];

#[rustfmt::skip]
static SO2_SHOMATE: [ShomateRange; 2] = [
    ShomateRange { t_min: 298.0, t_max: 1200.0,
        a: 21.43049, b: 74.35094, c: -57.75217, d: 16.35534, e: 0.086731, f: -305.7688, g: 254.8872, h: -296.8100 },
    ShomateRange { t_min: 1200.0, t_max: 6000.0,
        a: 57.48188, b: 1.009328, c: -0.076630, d: 0.005174, e: -4.045401, f: -324.4140, g: 302.7798, h: -296.8100 },
];

#[rustfmt::skip]
static NH3_SHOMATE: [ShomateRange; 2] = [
    ShomateRange { t_min: 298.0, t_max: 1400.0,
        a: 19.99563, b: 49.77119, c: -15.37599, d: 1.921168, e: 0.189174, f: -53.30667, g: 203.8591, h: -45.89806 },
    ShomateRange { t_min: 1400.0, t_max: 6000.0,
        a: 52.02427, b: 18.48801, c: -3.765128, d: 0.248541, e: -12.45799, f: -85.53895, g: 223.8022, h: -45.89806 },
];

/// Look up Shomate coefficient ranges for a gas species.
fn shomate_data(species: GasSpecies) -> &'static [ShomateRange] {
    match species {
        GasSpecies::O2 => &O2_SHOMATE,
        GasSpecies::N2 => &N2_SHOMATE,
        GasSpecies::H2 => &H2_SHOMATE,
        GasSpecies::H2O => &H2O_SHOMATE,
        GasSpecies::CO2 => &CO2_SHOMATE,
        GasSpecies::F2 => &F2_SHOMATE,
        GasSpecies::Cl2 => &CL2_SHOMATE,
        GasSpecies::SO2 => &SO2_SHOMATE,
        GasSpecies::NH3 => &NH3_SHOMATE,
    }
}

/// Find the Shomate coefficient range for a given temperature, clamping to
/// the nearest range boundary if outside all tabulated ranges.
///
/// Returns (range, clamped_temperature) where clamped_temperature is within
/// [range.t_min, range.t_max].
fn find_shomate_range(species: GasSpecies, temperature_k: f64) -> (&'static ShomateRange, f64) {
    let ranges = shomate_data(species);
    for range in ranges {
        if temperature_k >= range.t_min && temperature_k <= range.t_max {
            return (range, temperature_k);
        }
    }
    // Clamp to nearest range boundary
    if temperature_k < ranges[0].t_min {
        return (&ranges[0], ranges[0].t_min);
    }
    let last = ranges.last().expect("shomate data is never empty");
    (last, last.t_max)
}

// === Core Thermodynamic Functions ===

/// Compute H(T) − H(298.15 K) in kJ/mol for a gas species using the Shomate equation.
///
/// This is the molar enthalpy increment from 298.15 K to temperature `temperature_k`.
pub fn gas_enthalpy(species: GasSpecies, temperature_k: f64) -> Result<f64> {
    if temperature_k <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!("Temperature must be positive, got {temperature_k} K"),
        });
    }
    let (range, clamped_t) = find_shomate_range(species, temperature_k);
    let tau = clamped_t / 1000.0;
    let tau2 = tau * tau;
    let tau3 = tau2 * tau;
    let tau4 = tau3 * tau;
    Ok(
        range.a * tau + range.b * tau2 / 2.0 + range.c * tau3 / 3.0 + range.d * tau4 / 4.0
            - range.e / tau
            + range.f
            - range.h,
    )
}

/// Compute standard molar entropy S°(T) in J/(mol·K) for a gas species
/// using the Shomate equation.
pub fn gas_entropy(species: GasSpecies, temperature_k: f64) -> Result<f64> {
    if temperature_k <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!("Temperature must be positive, got {temperature_k} K"),
        });
    }
    let (range, clamped_t) = find_shomate_range(species, temperature_k);
    let tau = clamped_t / 1000.0;
    let tau2 = tau * tau;
    let tau3 = tau2 * tau;
    Ok(
        range.a * tau.ln() + range.b * tau + range.c * tau2 / 2.0 + range.d * tau3 / 3.0
            - range.e / (2.0 * tau2)
            + range.g,
    )
}

/// Compute gas-phase chemical potential μ(T, P) in eV per molecule.
///
/// Uses the Shomate equation for the standard Gibbs energy:
///   μ°(T) = ΔH_f + [H(T) − H(298)] − T·S(T)
/// plus the ideal-gas pressure correction:
///   μ(T, P) = μ°(T) + k_B·T·ln(P/P°)
///
/// where P° = 1 bar (IUPAC standard) and the input pressure is in atm.
/// Non-positive or non-finite pressures silently fall back to P° = 1 bar.
pub fn gas_chemical_potential(
    species: GasSpecies,
    temperature_k: f64,
    pressure_atm: f64,
) -> Result<f64> {
    if temperature_k <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!("Temperature must be positive, got {temperature_k} K"),
        });
    }
    // Use the clamped temperature consistently: enthalpy, entropy, and the
    // T·S / k_B·T terms must all reference the same effective temperature
    // so out-of-range calls stay on the Shomate boundary.
    let (_, clamped_t) = find_shomate_range(species, temperature_k);
    let delta_h = gas_enthalpy(species, clamped_t)?;
    let entropy = gas_entropy(species, clamped_t)?;
    let h_f = species.formation_enthalpy_kj_per_mol();

    // G(T) = ΔH_f + ΔH(T) − T·S(T) in kJ/mol
    let gibbs_kj = h_f + delta_h - clamped_t * entropy / 1000.0;
    let mu_standard = gibbs_kj * KJ_PER_MOL_TO_EV;

    // Pressure correction: k_B·T·ln(P_bar / P_ref)
    let pressure_bar = if pressure_atm > 0.0 && pressure_atm.is_finite() {
        pressure_atm * ATM_TO_BAR
    } else {
        P_REF_BAR
    };
    let pressure_correction = K_BOLTZMANN_EV * clamped_t * (pressure_bar / P_REF_BAR).ln();

    Ok(mu_standard + pressure_correction)
}

// === Element-to-Gas Mapping ===

/// Default mapping from element to its standard-state gas reference molecule.
///
/// Elements not present in this mapping (most metals, noble gases) are treated
/// as solid references and receive no gas correction.
pub fn default_element_to_gas(element: Element) -> Option<GasSpecies> {
    // Only elements whose thermodynamic standard state is a diatomic gas molecule.
    // C (graphite) and S (solid S8) are excluded — their standard states are solid.
    match element {
        Element::O => Some(GasSpecies::O2),
        Element::N => Some(GasSpecies::N2),
        Element::H => Some(GasSpecies::H2),
        Element::F => Some(GasSpecies::F2),
        Element::Cl => Some(GasSpecies::Cl2),
        _ => None,
    }
}

/// Stoichiometry of an element within its gas species (None if absent).
fn element_stoichiometry_in_gas(species: GasSpecies, element: Element) -> Option<u8> {
    species
        .element_stoichiometry()
        .iter()
        .find(|(elem, _)| *elem == element)
        .map(|(_, stoich)| *stoich)
}

// === Formation Energy Corrections ===

/// Compute gas-phase correction to an entry's per-atom energy at finite (T, P).
///
/// For each gas-forming element in the entry's composition, computes the change
/// in chemical potential Δμ between the 0 K reference and the gas at (T, P):
///
///   Δμ_molecule = μ(gas, T, P) − ΔH_f(gas)
///   Δμ_per_element = Δμ_molecule / stoichiometry
///   correction_per_atom = Σ_elements (fraction × Δμ_per_element)
///
/// Returns the per-atom energy correction in eV/atom. This correction is
/// typically applied only to unary reference entries when recomputing the hull.
pub fn correct_formation_energy(
    entry: &ConvexHullEntry,
    temperature_k: f64,
    gas_pressures: &HashMap<GasSpecies, f64>,
) -> f64 {
    let atom_count = entry.composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return 0.0;
    }

    let elem_comp = entry.composition.element_composition();
    let mut correction = 0.0;

    for element in elem_comp.unique_elements() {
        let Some(gas) = default_element_to_gas(element) else {
            continue;
        };
        let pressure = gas_pressures.get(&gas).copied().unwrap_or(1.0);

        let mu_tp = match gas_chemical_potential(gas, temperature_k, pressure) {
            Ok(val) => val,
            Err(_) => continue,
        };
        // Reference chemical potential: formation enthalpy at 298 K
        let mu_ref = gas.formation_enthalpy_kj_per_mol() * KJ_PER_MOL_TO_EV;
        let delta_mu_molecule = mu_tp - mu_ref;

        let Some(stoich) = element_stoichiometry_in_gas(gas, element) else {
            continue;
        };
        let delta_mu_per_element = delta_mu_molecule / stoich as f64;

        let amount = elem_comp.get_element_total(element);
        correction += (amount / atom_count) * delta_mu_per_element;
    }

    correction
}

// === Temperature-Dependent Hull ===

/// Compute energy above hull at finite temperature with gas-phase corrections.
///
/// Adjusts unary (single-element) reference energies for gas-forming elements
/// based on their chemical potentials at (T, P), then recomputes the convex
/// hull. Non-unary entries keep their original DFT energies.
///
/// This implements the standard approach from computational thermodynamics:
/// replacing the 0 K elemental reference with the gas-phase chemical potential
/// μ(T, P) effectively shifts the formation energy landscape. Phases with higher
/// gas-element content become less stable as entropy increases with temperature.
pub fn calculate_e_above_hull_at_temperature(
    entries: &[ConvexHullEntry],
    temperature_k: f64,
    gas_pressures: &HashMap<GasSpecies, f64>,
) -> Result<Vec<f64>> {
    let corrected_entries: Vec<ConvexHullEntry> = entries
        .iter()
        .map(|entry| {
            if !entry.is_unary() {
                return Ok(entry.clone());
            }
            let correction = correct_formation_energy(entry, temperature_k, gas_pressures);
            if correction.abs() < 1e-15 {
                return Ok(entry.clone());
            }
            let epa = entry.corrected_energy_per_atom()?;
            let new_epa = epa + correction;
            let n_atoms = entry.composition.num_atoms();
            let mut corrected = entry.clone();
            corrected.energy = new_epa * n_atoms;
            corrected.energy_per_atom = Some(new_epa);
            corrected.e_form_per_atom = None;
            corrected.correction = None;
            Ok(corrected)
        })
        .collect::<Result<Vec<_>>>()?;

    calculate_e_above_hull(&corrected_entries, &corrected_entries)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_approx(actual: f64, expected: f64, tolerance: f64, label: &str) {
        assert!(
            (actual - expected).abs() < tolerance,
            "{label}: expected {expected} ± {tolerance}, got {actual}"
        );
    }

    // NIST-JANAF reference values for Shomate validation of each gas species.
    // Source: https://webbook.nist.gov/chemistry/
    // (species, temperature_k, expected_entropy, tolerance)
    const JANAF_ENTROPY_REFS: &[(GasSpecies, f64, f64, f64)] = &[
        (GasSpecies::O2, 298.0, 205.15, 0.1),
        (GasSpecies::N2, 298.0, 191.61, 0.2),
        (GasSpecies::H2, 298.0, 130.68, 0.2),
        (GasSpecies::H2O, 500.0, 206.5, 0.5), // gas-phase range starts at 500K
        (GasSpecies::CO2, 298.0, 213.79, 0.2),
        (GasSpecies::F2, 298.0, 202.79, 0.7), // single wide range, lower accuracy
        (GasSpecies::Cl2, 298.0, 223.08, 0.2),
        (GasSpecies::SO2, 298.0, 248.22, 0.3),
        (GasSpecies::NH3, 298.0, 192.77, 0.3),
    ];

    #[test]
    fn test_gas_entropy_matches_janaf() {
        for &(species, temp, expected, tol) in JANAF_ENTROPY_REFS {
            let entropy = gas_entropy(species, temp).unwrap();
            assert_approx(entropy, expected, tol, &format!("S°({species:?}, {temp}K)"));
        }
    }

    #[test]
    fn test_gas_enthalpy_matches_janaf() {
        // (species, temperature_k, expected_kJ_per_mol, tolerance)
        let cases: &[(GasSpecies, f64, f64, f64)] = &[
            (GasSpecies::O2, 298.0, 0.0, 0.01),
            (GasSpecies::O2, 1000.0, 22.703, 0.01),
            (GasSpecies::CO2, 1000.0, 33.40, 0.05),
        ];
        for &(species, temp, expected, tol) in cases {
            let enthalpy = gas_enthalpy(species, temp).unwrap();
            assert_approx(
                enthalpy,
                expected,
                tol,
                &format!("ΔH({species:?}, {temp}K)"),
            );
        }
    }

    #[test]
    fn test_gas_chemical_potential_o2() {
        let mu_298 = gas_chemical_potential(GasSpecies::O2, 298.0, 1.0).unwrap();
        assert_approx(mu_298, -0.633, 0.005, "μ(O2, 298K, 1atm)");

        let mu_1000 = gas_chemical_potential(GasSpecies::O2, 1000.0, 0.21).unwrap();
        assert_approx(mu_1000, -2.423, 0.01, "μ(O2, 1000K, 0.21atm)");
    }

    #[test]
    fn test_negative_pressure_falls_back_to_reference() {
        let mu_ref = gas_chemical_potential(GasSpecies::O2, 500.0, 1.0 / ATM_TO_BAR).unwrap();
        let mu_neg = gas_chemical_potential(GasSpecies::O2, 500.0, -1.0).unwrap();
        assert_approx(mu_neg, mu_ref, 0.001, "negative pressure fallback");
    }

    #[test]
    fn test_rejects_nonpositive_temperature() {
        assert!(gas_enthalpy(GasSpecies::O2, 0.0).is_err());
        assert!(gas_entropy(GasSpecies::H2, -100.0).is_err());
    }

    #[test]
    fn test_num_atoms_per_molecule() {
        let cases: &[(GasSpecies, u8)] = &[
            (GasSpecies::O2, 2),
            (GasSpecies::N2, 2),
            (GasSpecies::H2, 2),
            (GasSpecies::F2, 2),
            (GasSpecies::Cl2, 2),
            (GasSpecies::H2O, 3),
            (GasSpecies::CO2, 3),
            (GasSpecies::SO2, 3),
            (GasSpecies::NH3, 4),
        ];
        for &(species, expected) in cases {
            assert_eq!(species.num_atoms(), expected, "{species:?}");
        }
    }

    #[test]
    fn test_temperature_clamping() {
        // Below range: O2 starts at 100K, querying at 50K should match 100K
        let below = gas_entropy(GasSpecies::O2, 50.0).unwrap();
        let at_min = gas_entropy(GasSpecies::O2, 100.0).unwrap();
        assert_approx(below, at_min, 1e-10, "clamping below range");

        // Above range: all species end at 6000K, querying at 7000K should match 6000K
        let above = gas_entropy(GasSpecies::N2, 7000.0).unwrap();
        let at_max = gas_entropy(GasSpecies::N2, 6000.0).unwrap();
        assert_approx(above, at_max, 1e-10, "clamping above range");
    }

    #[test]
    fn test_default_element_to_gas_mapping() {
        assert_eq!(default_element_to_gas(Element::O), Some(GasSpecies::O2));
        assert_eq!(default_element_to_gas(Element::N), Some(GasSpecies::N2));
        assert_eq!(default_element_to_gas(Element::H), Some(GasSpecies::H2));
        assert_eq!(default_element_to_gas(Element::F), Some(GasSpecies::F2));
        assert_eq!(default_element_to_gas(Element::Cl), Some(GasSpecies::Cl2));
        // Solid standard states: no gas mapping
        assert_eq!(default_element_to_gas(Element::C), None);
        assert_eq!(default_element_to_gas(Element::S), None);
        assert_eq!(default_element_to_gas(Element::Fe), None);
        assert_eq!(default_element_to_gas(Element::Li), None);
    }
}
