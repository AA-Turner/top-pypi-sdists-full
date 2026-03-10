// === Common Helpers ===

use super::common_types::PotentialResult;
use crate::error::{FerroxError, Result};
use nalgebra::{Matrix3, Vector3};

/// Apply minimum image convention to a displacement vector.
#[inline]
pub fn minimum_image(
    rij: Vector3<f64>,
    cell: Option<&Matrix3<f64>>,
    inv_cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
) -> Vector3<f64> {
    if let (Some(cell_mat), Some(inv)) = (cell, inv_cell) {
        let frac = inv * rij;
        let wrapped = Vector3::new(
            if pbc[0] {
                frac.x - frac.x.round()
            } else {
                frac.x
            },
            if pbc[1] {
                frac.y - frac.y.round()
            } else {
                frac.y
            },
            if pbc[2] {
                frac.z - frac.z.round()
            } else {
                frac.z
            },
        );
        cell_mat * wrapped
    } else {
        rij
    }
}

/// Initialize arrays for potential calculation.
#[inline]
pub(super) fn init_potential_arrays(
    n_atoms: usize,
    compute_stress: bool,
) -> (Vec<Vector3<f64>>, Vec<f64>, Option<Matrix3<f64>>) {
    (
        vec![Vector3::zeros(); n_atoms],
        vec![0.0; n_atoms],
        if compute_stress {
            Some(Matrix3::zeros())
        } else {
            None
        },
    )
}

/// Finalize stress tensor by dividing by volume.
/// If no cell is provided, stress is set to None (can't compute without volume).
#[inline]
pub(super) fn finalize_stress(stress: &mut Option<Matrix3<f64>>, cell: Option<&Matrix3<f64>>) {
    if let Some(s) = stress {
        if let Some(cell_mat) = cell {
            let volume = cell_mat.determinant().abs();
            if volume > 1e-10 {
                *s /= volume;
            }
        } else {
            // No cell means no volume - can't compute proper stress tensor
            *stress = None;
        }
    }
}

/// Add virial contribution to stress tensor: -r_ij ⊗ f_ij
#[inline]
pub(super) fn add_virial_stress(
    stress: &mut Option<Matrix3<f64>>,
    rij: &Vector3<f64>,
    force_vec: &Vector3<f64>,
) {
    if let Some(s) = stress {
        for alpha in 0..3 {
            for beta in 0..3 {
                s[(alpha, beta)] -= rij[alpha] * force_vec[beta];
            }
        }
    }
}

/// Result of a single pair interaction calculation.
pub struct PairInteraction {
    /// Pair energy contribution
    pub energy: f64,
    /// Force magnitude times distance (force_vec = force_mag_r * rij / dist²)
    pub force_mag_r: f64,
}

/// Generic pair potential computation using a closure for the interaction.
///
/// This is the DRY core that all pair potentials can use.
///
/// # Arguments
/// * `positions` - Atomic positions
/// * `atomic_numbers` - Optional element numbers for per-pair parameters
/// * `cell` - Optional cell matrix
/// * `pbc` - Periodic boundary conditions
/// * `cutoff` - Cutoff distance
/// * `compute_stress` - Whether to compute stress tensor
/// * `interaction` - Closure (z_i, z_j, dist, dist_sq) -> Option<PairInteraction>
///
/// # Errors
/// - `FerroxError::InvalidStructure` if `atomic_numbers` length doesn't match `positions` length.
/// - `FerroxError::PbcWithoutCell` if PBC is enabled but no cell matrix is provided.
/// - `FerroxError::SingularCell` if `cell` is provided but not invertible.
pub fn compute_pair_potential_generic<F>(
    positions: &[Vector3<f64>],
    atomic_numbers: Option<&[u8]>,
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    cutoff: f64,
    compute_stress: bool,
    mut interaction: F,
) -> Result<PotentialResult>
where
    F: FnMut(u8, u8, f64, f64) -> Option<PairInteraction>,
{
    // Guard: PBC requires a cell matrix
    if cell.is_none() && pbc.iter().any(|&enabled| enabled) {
        return Err(FerroxError::PbcWithoutCell);
    }

    let n_atoms = positions.len();

    // Validate atomic_numbers length if provided
    if let Some(z) = atomic_numbers
        && z.len() != n_atoms
    {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: format!(
                "atomic_numbers length ({}) must match positions length ({})",
                z.len(),
                n_atoms
            ),
        });
    }

    let mut energy = 0.0;
    let (mut forces, mut per_atom_energies, mut stress) =
        init_potential_arrays(n_atoms, compute_stress);

    let inv_cell = cell
        .map(|c| c.try_inverse().ok_or(FerroxError::SingularCell))
        .transpose()?;
    let cutoff_sq = cutoff * cutoff;

    for idx_i in 0..n_atoms {
        let z_i = atomic_numbers.map_or(0, |z| z[idx_i]);
        for idx_j in (idx_i + 1)..n_atoms {
            let z_j = atomic_numbers.map_or(0, |z| z[idx_j]);

            let rij = minimum_image(
                positions[idx_j] - positions[idx_i],
                cell,
                inv_cell.as_ref(),
                pbc,
            );

            let dist_sq = rij.norm_squared();
            if dist_sq > cutoff_sq {
                continue;
            }

            let dist = dist_sq.sqrt();
            if dist < 1e-10 {
                continue;
            }

            if let Some(pair) = interaction(z_i, z_j, dist, dist_sq) {
                energy += pair.energy;
                per_atom_energies[idx_i] += 0.5 * pair.energy;
                per_atom_energies[idx_j] += 0.5 * pair.energy;

                // force_vec = force_mag_r * rij / dist² (since rij has magnitude dist)
                let force_vec = (pair.force_mag_r / dist_sq) * rij;

                forces[idx_i] -= force_vec;
                forces[idx_j] += force_vec;

                add_virial_stress(&mut stress, &rij, &force_vec);
            }
        }
    }

    finalize_stress(&mut stress, cell);

    Ok(PotentialResult {
        energy,
        forces,
        stress,
        per_atom_energies: Some(per_atom_energies),
    })
}
