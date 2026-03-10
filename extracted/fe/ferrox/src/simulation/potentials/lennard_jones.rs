// === Lennard-Jones Potential ===

use super::{PairInteraction, PairPotential, PotentialResult, compute_pair_potential_generic};
use crate::error::Result;
use nalgebra::{Matrix3, Vector3};

/// Lennard-Jones pair parameters for use with `PairPotential<LJParams>`.
///
/// For simple single-species LJ, use `LennardJonesParams` instead.
#[derive(Debug, Clone, Copy)]
pub struct LJParams {
    /// Distance parameter sigma in Angstrom
    pub sigma: f64,
    /// Energy parameter epsilon in eV
    pub epsilon: f64,
}

impl Default for LJParams {
    fn default() -> Self {
        Self {
            sigma: 3.4,      // Typical for Ar
            epsilon: 0.0103, // ~0.0103 eV for Ar
        }
    }
}

impl LJParams {
    /// Create new LJ parameters.
    pub fn new(sigma: f64, epsilon: f64) -> Self {
        Self { sigma, epsilon }
    }
}

/// Lennard-Jones potential parameters for simple single-species calculations.
///
/// For multi-species with per-element-pair parameters, use `PairPotential<LJParams>`.
#[derive(Debug, Clone, Copy)]
pub struct LennardJonesParams {
    /// Distance parameter sigma in Angstrom
    pub sigma: f64,
    /// Energy parameter epsilon in eV
    pub epsilon: f64,
    /// Cutoff distance in Angstrom (None = no cutoff)
    pub cutoff: Option<f64>,
}

impl Default for LennardJonesParams {
    fn default() -> Self {
        Self {
            sigma: 3.4,
            epsilon: 0.0103,
            cutoff: Some(10.0),
        }
    }
}

impl LennardJonesParams {
    /// Create new LJ parameters.
    pub fn new(sigma: f64, epsilon: f64, cutoff: Option<f64>) -> Self {
        Self {
            sigma,
            epsilon,
            cutoff,
        }
    }

    /// Create parameters for Argon.
    pub fn argon() -> Self {
        Self::default()
    }
}

/// Result of simple Lennard-Jones energy/force calculation (no stress tensor).
#[derive(Debug, Clone)]
pub struct LennardJonesResult {
    /// Total potential energy in eV
    pub energy: f64,
    /// Forces on each atom in eV/Angstrom
    pub forces: Vec<Vector3<f64>>,
    /// Per-atom energies
    pub per_atom_energies: Option<Vec<f64>>,
}

/// Compute Lennard-Jones energy and forces for a set of positions.
///
/// Uses minimum image convention for periodic systems.
///
/// # Arguments
/// * `positions` - Atomic positions in Angstrom (Nx3)
/// * `cell` - Optional 3x3 cell matrix (rows are lattice vectors)
/// * `pbc` - Periodic boundary conditions [x, y, z]
/// * `params` - LJ parameters
///
/// # Returns
/// Energy and forces
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_lennard_jones(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    params: &LennardJonesParams,
) -> Result<LennardJonesResult> {
    let result = compute_lj_full(positions, cell, pbc, params, false)?;
    Ok(LennardJonesResult {
        energy: result.energy,
        forces: result.forces,
        per_atom_energies: result.per_atom_energies,
    })
}

/// Compute LJ forces only.
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_lennard_jones_forces(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    params: &LennardJonesParams,
) -> Result<Vec<Vector3<f64>>> {
    Ok(compute_lennard_jones(positions, cell, pbc, params)?.forces)
}

/// Compute Lennard-Jones with optional stress tensor.
/// V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_lj_full(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    params: &LennardJonesParams,
    compute_stress: bool,
) -> Result<PotentialResult> {
    let sigma6 = params.sigma.powi(6);
    let sigma12 = sigma6 * sigma6;
    let epsilon = params.epsilon;
    let cutoff = params.cutoff.unwrap_or(f64::INFINITY);

    compute_pair_potential_generic(
        positions,
        None,
        cell,
        pbc,
        cutoff,
        compute_stress,
        |_, _, _dist, dist_sq| {
            let dist6_inv = 1.0 / (dist_sq * dist_sq * dist_sq);
            let dist12_inv = dist6_inv * dist6_inv;
            let energy = 4.0 * epsilon * (sigma12 * dist12_inv - sigma6 * dist6_inv);
            let force_mag_r = 24.0 * epsilon * (2.0 * sigma12 * dist12_inv - sigma6 * dist6_inv);
            Some(PairInteraction {
                energy,
                force_mag_r,
            })
        },
    )
}

/// Compute LJ with per-element-pair parameters.
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_lj_pair(
    positions: &[Vector3<f64>],
    atomic_numbers: &[u8],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    potential: &PairPotential<LJParams>,
    compute_stress: bool,
) -> Result<PotentialResult> {
    compute_pair_potential_generic(
        positions,
        Some(atomic_numbers),
        cell,
        pbc,
        potential.cutoff,
        compute_stress,
        |z_i, z_j, _dist, dist_sq| {
            let params = potential.get(z_i, z_j);
            let sigma6 = params.sigma.powi(6);
            let sigma12 = sigma6 * sigma6;
            let dist6_inv = 1.0 / (dist_sq * dist_sq * dist_sq);
            let dist12_inv = dist6_inv * dist6_inv;
            let energy = 4.0 * params.epsilon * (sigma12 * dist12_inv - sigma6 * dist6_inv);
            let force_mag_r =
                24.0 * params.epsilon * (2.0 * sigma12 * dist12_inv - sigma6 * dist6_inv);
            Some(PairInteraction {
                energy,
                force_mag_r,
            })
        },
    )
}
