// === Morse Potential ===

use super::{PairInteraction, PairPotential, PotentialResult, compute_pair_potential_generic};
use crate::error::Result;
use nalgebra::{Matrix3, Vector3};

/// Morse pair parameters: V(r) = D * (1 - exp(-alpha*(r - r0)))^2 - D
#[derive(Debug, Clone, Copy)]
pub struct MorseParams {
    /// Well depth in eV
    pub d: f64,
    /// Width parameter in 1/Angstrom
    pub alpha: f64,
    /// Equilibrium distance in Angstrom
    pub r0: f64,
}

impl Default for MorseParams {
    fn default() -> Self {
        Self {
            d: 1.0,
            alpha: 1.0,
            r0: 1.0,
        }
    }
}

impl MorseParams {
    /// Create new Morse parameters.
    pub fn new(d: f64, alpha: f64, r0: f64) -> Self {
        Self { d, alpha, r0 }
    }
}

/// Compute Morse potential energy and forces.
/// V(r) = D * (1 - exp(-alpha*(r - r0)))^2 - D
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_morse(
    positions: &[Vector3<f64>],
    atomic_numbers: &[u8],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    potential: &PairPotential<MorseParams>,
    compute_stress: bool,
) -> Result<PotentialResult> {
    compute_pair_potential_generic(
        positions,
        Some(atomic_numbers),
        cell,
        pbc,
        potential.cutoff,
        compute_stress,
        |z_i, z_j, dist, _dist_sq| {
            let params = potential.get(z_i, z_j);
            let exp_term = (-params.alpha * (dist - params.r0)).exp();
            let one_minus_exp = 1.0 - exp_term;
            let energy = params.d * one_minus_exp * one_minus_exp - params.d;
            // dV/dr = 2*D*alpha*(1-exp)*exp, force_mag_r = -dV/dr * dist
            let dvdr = 2.0 * params.d * params.alpha * one_minus_exp * exp_term;
            let force_mag_r = -dvdr * dist;
            Some(PairInteraction {
                energy,
                force_mag_r,
            })
        },
    )
}

/// Simple Morse computation without per-pair parameters.
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
#[allow(clippy::too_many_arguments)]
pub fn compute_morse_simple(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    d: f64,
    alpha: f64,
    r0: f64,
    cutoff: f64,
    compute_stress: bool,
) -> Result<PotentialResult> {
    let dummy_z = vec![0u8; positions.len()];
    let potential = PairPotential::new(MorseParams::new(d, alpha, r0), cutoff);
    compute_morse(positions, &dummy_z, cell, pbc, &potential, compute_stress)
}
