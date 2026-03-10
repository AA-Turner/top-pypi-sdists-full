use crate::cell_ops::perpendicular_distances;
use crate::error::{FerroxError, Result};
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};

// === Supercell for Defect Calculations ===

/// Configuration for finding optimal defect supercells.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DefectSupercellConfig {
    /// Minimum distance between periodic images of the defect (Angstrom).
    pub min_distance: f64,
    /// Maximum number of atoms allowed in the supercell.
    pub max_atoms: usize,
    /// Preference for cubic supercells (0.0 = none, 1.0 = strong).
    pub cubic_preference: f64,
}

impl Default for DefectSupercellConfig {
    fn default() -> Self {
        Self {
            min_distance: 10.0,
            max_atoms: 200,
            cubic_preference: 0.5,
        }
    }
}

/// Find an optimal supercell matrix for dilute defect calculations.
///
/// This function finds a supercell transformation matrix that:
/// 1. Ensures periodic images of the defect are at least `min_distance` apart.
/// 2. Keeps the total number of atoms below `max_atoms`.
/// 3. Optionally prefers more cubic supercells.
///
/// # Arguments
///
/// * `structure` - The structure to create a supercell for.
/// * `config` - Configuration specifying constraints.
///
/// # Returns
///
/// A 3x3 integer transformation matrix for creating the supercell.
pub fn find_defect_supercell(
    structure: &Structure,
    config: &DefectSupercellConfig,
) -> Result<[[i32; 3]; 3]> {
    let lattice = &structure.lattice;
    let lengths = lattice.lengths();
    let num_sites = structure.num_sites();

    if num_sites == 0 {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: "Cannot create supercell for empty structure".to_string(),
        });
    }

    // Calculate perpendicular distances (heights of the parallelepiped)
    let perp_dists = perpendicular_distances(lattice);

    // Check for degenerate lattice (zero perpendicular distance in any direction)
    if perp_dists.x <= 0.0 || perp_dists.y <= 0.0 || perp_dists.z <= 0.0 {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: format!(
                "Degenerate lattice with zero perpendicular distance: {:?}",
                perp_dists
            ),
        });
    }

    // Minimum scaling factors needed for each direction
    // Safe division since we verified perp_dists are positive
    let min_scale_a = (config.min_distance / perp_dists.x).ceil().max(1.0) as i32;
    let min_scale_b = (config.min_distance / perp_dists.y).ceil().max(1.0) as i32;
    let min_scale_c = (config.min_distance / perp_dists.z).ceil().max(1.0) as i32;

    // Start with minimum diagonal supercell
    let mut best_matrix = [
        [min_scale_a, 0, 0],
        [0, min_scale_b, 0],
        [0, 0, min_scale_c],
    ];
    let mut best_score = f64::MAX;

    // Search for better supercell matrices
    let max_scale = ((config.max_atoms as f64 / num_sites as f64).cbrt().ceil() as i32 + 1)
        .max(min_scale_a.max(min_scale_b).max(min_scale_c));

    for scale_a in min_scale_a..=max_scale {
        for scale_b in min_scale_b..=max_scale {
            for scale_c in min_scale_c..=max_scale {
                let matrix = [[scale_a, 0, 0], [0, scale_b, 0], [0, 0, scale_c]];

                // Check atom count
                let det = scale_a * scale_b * scale_c;
                let n_atoms = num_sites * det.unsigned_abs() as usize;
                if n_atoms > config.max_atoms {
                    continue;
                }

                // Check perpendicular distances in supercell
                let super_lengths = Vector3::new(
                    lengths.x * scale_a as f64,
                    lengths.y * scale_b as f64,
                    lengths.z * scale_c as f64,
                );
                let super_perp = Vector3::new(
                    perp_dists.x * scale_a as f64,
                    perp_dists.y * scale_b as f64,
                    perp_dists.z * scale_c as f64,
                );

                if super_perp.min() < config.min_distance {
                    continue;
                }

                // Score: prefer smaller cells with good cubicity
                let size_score = n_atoms as f64;
                let cubicity_score = if config.cubic_preference > 0.0 {
                    let avg_len = (super_lengths.x + super_lengths.y + super_lengths.z) / 3.0;
                    let deviation = ((super_lengths.x - avg_len).powi(2)
                        + (super_lengths.y - avg_len).powi(2)
                        + (super_lengths.z - avg_len).powi(2))
                        / 3.0;
                    deviation.sqrt() * config.cubic_preference
                } else {
                    0.0
                };

                let score = size_score + cubicity_score;

                if score < best_score {
                    best_score = score;
                    best_matrix = matrix;
                }
            }
        }
    }

    Ok(best_matrix)
}
