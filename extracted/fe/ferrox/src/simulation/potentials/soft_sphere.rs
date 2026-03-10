// === Soft Sphere Potential ===

use super::{PairInteraction, PairPotential, PotentialResult, compute_pair_potential_generic};
use crate::error::Result;
use nalgebra::{Matrix3, Vector3};

/// Soft Sphere pair parameters: V(r) = epsilon * (sigma/r)^alpha
#[derive(Debug, Clone, Copy)]
pub struct SoftSphereParams {
    /// Length scale in Angstrom
    pub sigma: f64,
    /// Energy scale in eV
    pub epsilon: f64,
    /// Exponent (12 = hard, 2 = soft)
    pub alpha: f64,
}

impl Default for SoftSphereParams {
    fn default() -> Self {
        Self {
            sigma: 1.0,
            epsilon: 1.0,
            alpha: 12.0,
        }
    }
}

impl SoftSphereParams {
    /// Create new Soft Sphere parameters.
    pub fn new(sigma: f64, epsilon: f64, alpha: f64) -> Self {
        Self {
            sigma,
            epsilon,
            alpha,
        }
    }
}

/// Compute Soft Sphere potential energy and forces.
/// V(r) = epsilon * (sigma/r)^alpha
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_soft_sphere(
    positions: &[Vector3<f64>],
    atomic_numbers: &[u8],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    potential: &PairPotential<SoftSphereParams>,
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
            let energy = params.epsilon * (params.sigma / dist).powf(params.alpha);
            // dV/dr = -alpha*V/r, force_mag_r = alpha*V (since force_vec = force_mag_r/dist² * rij)
            let force_mag_r = params.alpha * energy;
            Some(PairInteraction {
                energy,
                force_mag_r,
            })
        },
    )
}

/// Simple Soft Sphere computation without per-pair parameters.
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
#[allow(clippy::too_many_arguments)]
pub fn compute_soft_sphere_simple(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    sigma: f64,
    epsilon: f64,
    alpha: f64,
    cutoff: f64,
    compute_stress: bool,
) -> Result<PotentialResult> {
    let dummy_z = vec![0u8; positions.len()];
    let potential = PairPotential::new(SoftSphereParams::new(sigma, epsilon, alpha), cutoff);
    compute_soft_sphere(positions, &dummy_z, cell, pbc, &potential, compute_stress)
}
