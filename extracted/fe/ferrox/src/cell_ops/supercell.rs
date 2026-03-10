use crate::lattice::Lattice;
use nalgebra::Vector3;

use super::DEGENERATE_LATTICE_TOLERANCE;

/// Strategy for finding optimal supercell matrices.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SupercellStrategy {
    /// Simple cubic expansion (n × n × n)
    Cubic(i32),
    /// Diagonal expansion (na × nb × nc)
    Diagonal([i32; 3]),
    /// General 3×3 transformation matrix
    General([[i32; 3]; 3]),
    /// Target a specific number of atoms
    TargetAtoms(usize),
    /// Ensure minimum cell length along all axes
    MinLength(f64),
    /// Ensure minimum image distance between periodic images
    MinImageDistance(f64),
}

/// Find an optimal supercell matrix for a given strategy.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `n_atoms` - Number of atoms in the primitive cell
/// * `strategy` - The supercell strategy to use
///
/// # Returns
///
/// A 3×3 integer transformation matrix for the supercell.
pub fn find_supercell_matrix(
    lattice: &Lattice,
    n_atoms: usize,
    strategy: SupercellStrategy,
) -> [[i32; 3]; 3] {
    match strategy {
        SupercellStrategy::Cubic(n_val) => [[n_val, 0, 0], [0, n_val, 0], [0, 0, n_val]],
        SupercellStrategy::Diagonal(diag) => [[diag[0], 0, 0], [0, diag[1], 0], [0, 0, diag[2]]],
        SupercellStrategy::General(matrix) => matrix,
        SupercellStrategy::TargetAtoms(target) => {
            find_supercell_for_target_atoms(lattice, n_atoms, target)
        }
        SupercellStrategy::MinLength(min_len) => find_supercell_for_min_length(lattice, min_len),
        SupercellStrategy::MinImageDistance(min_dist) => {
            find_supercell_for_min_image_dist(lattice, min_dist)
        }
    }
}

/// Find a near-cubic supercell that approaches a target atom count.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `n_atoms` - Number of atoms in the primitive cell
/// * `target_atoms` - Target number of atoms
///
/// # Returns
///
/// A 3×3 diagonal integer transformation matrix.
pub fn find_supercell_for_target_atoms(
    lattice: &Lattice,
    n_atoms: usize,
    target_atoms: usize,
) -> [[i32; 3]; 3] {
    if n_atoms == 0 || target_atoms == 0 {
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    }

    let target_factor = (target_atoms as f64 / n_atoms as f64).max(1.0);
    let lengths = lattice.lengths();

    // Find multipliers that give approximately cubic supercell and target atom count
    let mut best_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    let mut best_diff = usize::MAX;

    // Search for optimal diagonal expansion
    let max_mult = (target_factor.powf(1.0 / 3.0) * 3.0).ceil() as i32;

    for mult_a in 1..=max_mult {
        for mult_b in 1..=max_mult {
            for mult_c in 1..=max_mult {
                let total = (mult_a * mult_b * mult_c) as usize * n_atoms;
                let diff = total.abs_diff(target_atoms);

                if diff < best_diff {
                    // Check if this is reasonably cubic
                    let effective_lengths = Vector3::new(
                        lengths[0] * mult_a as f64,
                        lengths[1] * mult_b as f64,
                        lengths[2] * mult_c as f64,
                    );
                    let max_eff = effective_lengths.max();
                    let min_eff = effective_lengths.min();

                    // Allow up to 50% deviation from cubic
                    if max_eff / min_eff <= 1.5 || diff == 0 {
                        best_diff = diff;
                        best_matrix = [[mult_a, 0, 0], [0, mult_b, 0], [0, 0, mult_c]];
                    }
                }

                if best_diff == 0 {
                    break;
                }
            }
        }
    }

    best_matrix
}

/// Find a supercell where all cell lengths exceed a minimum value.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `min_length` - Minimum required cell length in Ångströms (must be positive)
///
/// # Returns
///
/// A 3×3 diagonal integer transformation matrix.
pub fn find_supercell_for_min_length(lattice: &Lattice, min_length: f64) -> [[i32; 3]; 3] {
    // Handle invalid input gracefully
    if min_length <= 0.0 || !min_length.is_finite() {
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    }

    let lengths = lattice.lengths();
    let mult_a = (min_length / lengths[0]).ceil() as i32;
    let mult_b = (min_length / lengths[1]).ceil() as i32;
    let mult_c = (min_length / lengths[2]).ceil() as i32;

    [
        [mult_a.max(1), 0, 0],
        [0, mult_b.max(1), 0],
        [0, 0, mult_c.max(1)],
    ]
}

/// Find a supercell with minimum image distance at least the specified value.
///
/// The perpendicular distances (heights of the parallelepiped) determine the
/// minimum image distance, not the lattice vector lengths.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `min_dist` - Minimum required image distance in Ångströms (must be positive)
///
/// # Returns
///
/// A 3×3 diagonal integer transformation matrix.
pub fn find_supercell_for_min_image_dist(lattice: &Lattice, min_dist: f64) -> [[i32; 3]; 3] {
    // Handle invalid input gracefully
    if min_dist <= 0.0 || !min_dist.is_finite() {
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    }

    let perp_dists = perpendicular_distances(lattice);

    // Protect against zero perpendicular distances (degenerate lattice)
    let mult_a = if perp_dists[0] > DEGENERATE_LATTICE_TOLERANCE {
        (min_dist / perp_dists[0]).ceil() as i32
    } else {
        1
    };
    let mult_b = if perp_dists[1] > DEGENERATE_LATTICE_TOLERANCE {
        (min_dist / perp_dists[1]).ceil() as i32
    } else {
        1
    };
    let mult_c = if perp_dists[2] > DEGENERATE_LATTICE_TOLERANCE {
        (min_dist / perp_dists[2]).ceil() as i32
    } else {
        1
    };

    [
        [mult_a.max(1), 0, 0],
        [0, mult_b.max(1), 0],
        [0, 0, mult_c.max(1)],
    ]
}

/// Compute the perpendicular distances (heights) of the lattice parallelepiped.
///
/// The perpendicular distance for axis i is V / |a_j × a_k| where j, k are
/// the other two axes. This is the minimum distance between parallel planes
/// of the lattice.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
///
/// # Returns
///
/// Vector of perpendicular distances [d_a, d_b, d_c]. Returns 0.0 for any
/// axis where the perpendicular distance cannot be computed (degenerate lattice).
pub fn perpendicular_distances(lattice: &Lattice) -> Vector3<f64> {
    let matrix = lattice.matrix();
    let vec_a = matrix.row(0).transpose();
    let vec_b = matrix.row(1).transpose();
    let vec_c = matrix.row(2).transpose();

    let volume = lattice.volume().abs();

    // d_a = V / |b × c|, d_b = V / |c × a|, d_c = V / |a × b|
    let cross_bc = vec_b.cross(&vec_c).norm();
    let cross_ca = vec_c.cross(&vec_a).norm();
    let cross_ab = vec_a.cross(&vec_b).norm();

    // Use a small epsilon to avoid division by near-zero values
    const EPS: f64 = 1e-10;

    Vector3::new(
        if cross_bc > EPS {
            volume / cross_bc
        } else {
            0.0
        },
        if cross_ca > EPS {
            volume / cross_ca
        } else {
            0.0
        },
        if cross_ab > EPS {
            volume / cross_ab
        } else {
            0.0
        },
    )
}
