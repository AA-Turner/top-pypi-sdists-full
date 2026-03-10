// === Simple Pair Iterator for Potentials ===

use nalgebra::{Matrix3, Vector3};

/// Iterate over all unique pairs within cutoff distance.
///
/// This is a simpler interface for use with potential calculations
/// that don't need the full Structure object.
///
/// # Arguments
/// * `positions` - Cartesian positions in Angstrom
/// * `cell` - Optional 3x3 cell matrix (rows are lattice vectors)
/// * `pbc` - Periodic boundary conditions [x, y, z]
/// * `cutoff` - Cutoff distance in Angstrom
/// * `callback` - Called for each pair with (i, j, r_ij, distance)
///
/// # Minimum Image Convention
/// Uses minimum image convention: only considers the nearest periodic image
/// of each atom pair. For correct behavior, the cutoff should be less than
/// half the smallest cell dimension. Larger cutoffs may miss some pairs.
///
/// # Example
/// ```rust,ignore
/// for_each_pair(&positions, Some(&cell), [true; 3], 5.0, |i, j, r_ij, dist| {
///     // Compute pair interaction
/// });
/// ```
/// # Errors
/// Returns `FerroxError::PbcWithoutCell` if any PBC direction is enabled but cell is None.
/// Returns `FerroxError::SingularCell` if the cell matrix is non-invertible.
pub fn for_each_pair<F>(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    cutoff: f64,
    mut callback: F,
) -> crate::error::Result<()>
where
    F: FnMut(usize, usize, Vector3<f64>, f64),
{
    use crate::error::FerroxError;
    use crate::simulation::potentials::minimum_image;

    // Guard: PBC requires a cell matrix
    if cell.is_none() && pbc.iter().any(|&enabled| enabled) {
        return Err(FerroxError::PbcWithoutCell);
    }

    let n_atoms = positions.len();
    let cutoff_sq = cutoff * cutoff;
    let inv_cell = cell
        .map(|mat| mat.try_inverse().ok_or(FerroxError::SingularCell))
        .transpose()?;

    // O(N²) iteration - for O(N) use build_neighbor_list() with CellList
    for idx_i in 0..n_atoms {
        for idx_j in (idx_i + 1)..n_atoms {
            let rij = minimum_image(
                positions[idx_j] - positions[idx_i],
                cell,
                inv_cell.as_ref(),
                pbc,
            );

            let dist_sq = rij.norm_squared();
            if dist_sq <= cutoff_sq {
                callback(idx_i, idx_j, rij, dist_sq.sqrt());
            }
        }
    }

    Ok(())
}

/// Count pairs within cutoff distance.
///
/// Useful for estimating memory requirements.
///
/// # Errors
/// Returns `FerroxError::PbcWithoutCell` if any PBC direction is enabled but cell is None.
/// Returns `FerroxError::SingularCell` if the cell matrix is non-invertible.
pub fn count_pairs(
    positions: &[Vector3<f64>],
    cell: Option<&Matrix3<f64>>,
    pbc: [bool; 3],
    cutoff: f64,
) -> crate::error::Result<usize> {
    let mut count = 0;
    for_each_pair(positions, cell, pbc, cutoff, |_, _, _, _| {
        count += 1;
    })?;
    Ok(count)
}
