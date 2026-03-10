// === Harmonic Bonds ===

use super::common_helpers::{add_virial_stress, finalize_stress, init_potential_arrays};
use super::{PotentialResult, minimum_image};
use crate::error::{FerroxError, Result};
use nalgebra::{Matrix3, Vector3};

/// A harmonic bond between two atoms.
#[derive(Debug, Clone, Copy)]
pub struct HarmonicBond {
    /// First atom index
    pub i: usize,
    /// Second atom index
    pub j: usize,
    /// Spring constant in eV/Å²
    pub k: f64,
    /// Equilibrium distance in Å
    pub r0: f64,
}

impl HarmonicBond {
    /// Create a new harmonic bond.
    pub fn new(i: usize, j: usize, k: f64, r0: f64) -> Self {
        Self { i, j, k, r0 }
    }
}

/// Compute harmonic bond energy and forces.
///
/// V = 0.5 * k * (r - r0)^2
/// F = -k * (r - r0) * r_hat
///
/// # Errors
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if the cell matrix is singular (non-invertible).
/// - `FerroxError::InvalidStructure` if any bond index is out of bounds.
pub fn compute_harmonic_bonds(
    positions: &[Vector3<f64>],
    bonds: &[HarmonicBond],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    compute_stress: bool,
) -> Result<PotentialResult> {
    // Guard: PBC requires a cell matrix
    if cell.is_none() && pbc.iter().any(|&enabled| enabled) {
        return Err(FerroxError::PbcWithoutCell);
    }

    let n_atoms = positions.len();
    let mut energy = 0.0;
    let (mut forces, mut per_atom_energies, mut stress) =
        init_potential_arrays(n_atoms, compute_stress);

    let inv_cell = cell
        .map(|c| c.try_inverse().ok_or(FerroxError::SingularCell))
        .transpose()?;

    for (bond_idx, bond) in bonds.iter().enumerate() {
        let idx_i = bond.i;
        let idx_j = bond.j;

        // Validate bond indices are within bounds
        if idx_i >= n_atoms {
            return Err(FerroxError::InvalidStructure {
                index: bond_idx,
                reason: format!("bond atom index i={idx_i} out of bounds (n_atoms={n_atoms})"),
            });
        }
        if idx_j >= n_atoms {
            return Err(FerroxError::InvalidStructure {
                index: bond_idx,
                reason: format!("bond atom index j={idx_j} out of bounds (n_atoms={n_atoms})"),
            });
        }

        let rij = minimum_image(
            positions[idx_j] - positions[idx_i],
            cell,
            inv_cell.as_ref(),
            pbc,
        );

        let dist = rij.norm();
        if dist < 1e-10 {
            continue;
        }

        let spring_k = bond.k;
        let eq_dist = bond.r0;
        let delta_r = dist - eq_dist;

        // V = 0.5 * k * dr^2
        let pair_energy = 0.5 * spring_k * delta_r * delta_r;
        energy += pair_energy;
        per_atom_energies[idx_i] += 0.5 * pair_energy;
        per_atom_energies[idx_j] += 0.5 * pair_energy;

        // F = -k * dr * r_hat = -k * dr / r * rij
        let force_mag = -spring_k * delta_r / dist;
        let force_vec = force_mag * rij;

        forces[idx_i] -= force_vec;
        forces[idx_j] += force_vec;

        add_virial_stress(&mut stress, &rij, &force_vec);
    }

    finalize_stress(&mut stress, cell);

    Ok(PotentialResult {
        energy,
        forces,
        stress,
        per_atom_energies: Some(per_atom_energies),
    })
}
