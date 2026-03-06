//! Enhanced periodic boundary condition and cell operations.
//!
//! This module provides advanced cell manipulation functions including:
//! - Minimum image distance calculations for any cell geometry
//! - Niggli and Delaunay cell reduction algorithms
//! - Supercell generation strategies
//! - Lattice equivalence checking

use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::pbc::wrap_frac_coord;
use nalgebra::{Matrix3, Vector3};

// === Constants ===

/// Tolerance for detecting degenerate lattices (nearly zero perpendicular distance).
const DEGENERATE_LATTICE_TOLERANCE: f64 = 1e-10;

// === Minimum Image Distance Functions ===

/// Compute the minimum image distance between two positions.
///
/// This handles all cell geometries including highly skewed cells by checking
/// all 27 periodic images when necessary.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `pos1` - First position in fractional coordinates
/// * `pos2` - Second position in fractional coordinates
/// * `pbc` - Periodic boundary conditions along each axis
///
/// # Returns
///
/// The minimum distance between the two positions under PBC.
pub fn minimum_image_distance(
    lattice: &Lattice,
    pos1: &Vector3<f64>,
    pos2: &Vector3<f64>,
    pbc: [bool; 3],
) -> f64 {
    let delta_frac = pos2 - pos1;
    let delta_cart = minimum_image_vector(lattice, &delta_frac, pbc);
    delta_cart.norm()
}

/// Compute the minimum image displacement vector.
///
/// Finds the shortest Cartesian vector connecting two positions under PBC.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `delta` - Displacement in fractional coordinates
/// * `pbc` - Periodic boundary conditions along each axis
///
/// # Returns
///
/// The minimum image displacement vector in Cartesian coordinates.
pub fn minimum_image_vector(
    lattice: &Lattice,
    delta: &Vector3<f64>,
    pbc: [bool; 3],
) -> Vector3<f64> {
    // Wrap delta to [-0.5, 0.5] for periodic dimensions
    let mut wrapped = *delta;
    for dim in 0..3 {
        if pbc[dim] {
            wrapped[dim] = wrap_to_half(wrapped[dim]);
        }
    }

    // For highly skewed cells, use brute force method
    if is_highly_skewed(lattice) {
        return minimum_image_brute_force(lattice, &wrapped, pbc);
    }

    // Convert to Cartesian
    lattice.get_cartesian_coord(&wrapped)
}

/// Check if a lattice is highly skewed (angles far from 90°).
///
/// Highly skewed cells require checking more periodic images to find
/// the true minimum image distance.
///
/// # Arguments
///
/// * `lattice` - The lattice to check
///
/// # Returns
///
/// `true` if any angle deviates from 90° by more than 30°.
pub fn is_highly_skewed(lattice: &Lattice) -> bool {
    let angles = lattice.angles();
    for angle in angles.iter() {
        if (angle - 90.0).abs() > 30.0 {
            return true;
        }
    }
    false
}

/// Brute force minimum image calculation for highly skewed cells.
///
/// Checks periodic images within a range determined by perpendicular distances.
/// For highly skewed/small-volume cells, images beyond ±1 may be closest.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `delta` - Displacement in fractional coordinates (already wrapped to [-0.5, 0.5])
/// * `pbc` - Periodic boundary conditions along each axis
///
/// # Returns
///
/// The minimum image displacement vector in Cartesian coordinates.
pub fn minimum_image_brute_force(
    lattice: &Lattice,
    delta: &Vector3<f64>,
    pbc: [bool; 3],
) -> Vector3<f64> {
    let mut best_dist_sq = f64::INFINITY;
    let mut best_vec = lattice.get_cartesian_coord(delta);

    // For skewed cells, determine search range based on perpendicular distances
    // A rough estimate: max distance we care about is ~half the cell diagonal
    let perp_dists = perpendicular_distances(lattice);
    let min_perp = perp_dists.min();

    // Search range: need to check images that could be closer than best_dist
    // Use ceil(max_lattice_length / min_perp_dist) with minimum of 1
    // Clamp to max 10 to avoid O(n³) explosion for pathologically skewed cells
    const MAX_SEARCH_RANGE: i32 = 10;
    let lattice_lengths = lattice.lengths();
    let max_length = lattice_lengths.max();
    let search_range = if min_perp > DEGENERATE_LATTICE_TOLERANCE {
        ((max_length / min_perp).ceil() as i32).clamp(1, MAX_SEARCH_RANGE)
    } else {
        3 // fallback for degenerate lattices
    };

    for shift_a in -search_range..=search_range {
        if !pbc[0] && shift_a != 0 {
            continue;
        }
        for shift_b in -search_range..=search_range {
            if !pbc[1] && shift_b != 0 {
                continue;
            }
            for shift_c in -search_range..=search_range {
                if !pbc[2] && shift_c != 0 {
                    continue;
                }
                let shifted = Vector3::new(
                    delta[0] + shift_a as f64,
                    delta[1] + shift_b as f64,
                    delta[2] + shift_c as f64,
                );
                let cart = lattice.get_cartesian_coord(&shifted);
                let dist_sq = cart.norm_squared();
                if dist_sq < best_dist_sq {
                    best_dist_sq = dist_sq;
                    best_vec = cart;
                }
            }
        }
    }

    best_vec
}

/// Wrap a fractional coordinate to the range [-0.5, 0.5).
///
/// Uses `coord - coord.round()` where Rust's `round()` rounds half away from zero:
/// - `wrap_to_half(0.5)` returns -0.5
/// - `wrap_to_half(-0.5)` returns 0.5
///
/// # Arguments
///
/// * `coord` - The fractional coordinate value
///
/// # Returns
///
/// The wrapped coordinate in [-0.5, 0.5).
#[inline]
pub fn wrap_to_half(coord: f64) -> f64 {
    coord - coord.round()
}

/// Wrap a fractional coordinate to the range [0, 1).
///
/// Delegates to [`crate::pbc::wrap_frac_coord`] which handles negative inputs
/// and floating-point edge cases correctly.
#[inline]
pub fn wrap_to_unit(coord: f64) -> f64 {
    wrap_frac_coord(coord)
}

/// Wrap all fractional positions to the unit cell [0, 1)^3.
///
/// # Arguments
///
/// * `positions` - Slice of fractional coordinate vectors
///
/// # Returns
///
/// New vector with all positions wrapped to [0, 1)^3.
pub fn wrap_positions_to_unit_cell(positions: &[Vector3<f64>]) -> Vec<Vector3<f64>> {
    positions
        .iter()
        .map(|pos| {
            Vector3::new(
                wrap_to_unit(pos[0]),
                wrap_to_unit(pos[1]),
                wrap_to_unit(pos[2]),
            )
        })
        .collect()
}

/// Check if a position is inside the unit cell.
///
/// # Arguments
///
/// * `position` - Position in fractional coordinates
/// * `tolerance` - Tolerance for boundary checks
///
/// # Returns
///
/// `true` if all components are in [-tolerance, 1 + tolerance).
pub fn is_inside_unit_cell(position: &Vector3<f64>, tolerance: f64) -> bool {
    position
        .iter()
        .all(|&coord| coord >= -tolerance && coord < 1.0 + tolerance)
}

/// Find the periodic image of a position closest to a reference point.
///
/// For non-orthogonal lattices, this searches nearby periodic images to find
/// the one with minimum Cartesian distance to the reference point.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice (used to compute Cartesian distances)
/// * `position` - Position to find image for (fractional coordinates)
/// * `reference` - Reference position (fractional coordinates)
/// * `pbc` - Periodic boundary conditions along each axis
///
/// # Returns
///
/// The periodic image of `position` closest to `reference` in fractional coordinates.
pub fn closest_image(
    lattice: &Lattice,
    position: &Vector3<f64>,
    reference: &Vector3<f64>,
    pbc: [bool; 3],
) -> Vector3<f64> {
    let delta = position - reference;

    // First, wrap to [-0.5, 0.5) as initial guess
    let wrapped_delta = Vector3::new(
        if pbc[0] {
            wrap_to_half(delta[0])
        } else {
            delta[0]
        },
        if pbc[1] {
            wrap_to_half(delta[1])
        } else {
            delta[1]
        },
        if pbc[2] {
            wrap_to_half(delta[2])
        } else {
            delta[2]
        },
    );

    // For orthogonal cells, the wrapped fractional delta gives the closest image.
    // For skewed cells, check neighboring images to find the true minimum.
    let matrix = lattice.matrix();
    let mut best_delta = wrapped_delta;
    let mut best_dist_sq = (matrix * wrapped_delta).norm_squared();

    // Check neighboring images (shifts of -1, 0, +1 along each periodic axis)
    let shifts: &[i32] = &[-1, 0, 1];
    for &shift_a in shifts {
        if !pbc[0] && shift_a != 0 {
            continue;
        }
        for &shift_b in shifts {
            if !pbc[1] && shift_b != 0 {
                continue;
            }
            for &shift_c in shifts {
                if !pbc[2] && shift_c != 0 {
                    continue;
                }
                if shift_a == 0 && shift_b == 0 && shift_c == 0 {
                    continue; // Already checked wrapped_delta
                }

                let candidate_delta = Vector3::new(
                    wrapped_delta[0] + shift_a as f64,
                    wrapped_delta[1] + shift_b as f64,
                    wrapped_delta[2] + shift_c as f64,
                );
                let cart_delta = matrix * candidate_delta;
                let dist_sq = cart_delta.norm_squared();

                if dist_sq < best_dist_sq {
                    best_dist_sq = dist_sq;
                    best_delta = candidate_delta;
                }
            }
        }
    }

    reference + best_delta
}

// === Niggli Reduction ===

/// Niggli form type for classification.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NiggliForm {
    /// Type I: All off-diagonal products have the same sign (all positive or all negative)
    TypeI,
    /// Type II: Off-diagonal products have mixed signs or zeros
    TypeII,
}

/// Result of Niggli reduction.
#[derive(Debug, Clone)]
pub struct NiggliCell {
    /// The Niggli-reduced lattice matrix (rows are lattice vectors)
    pub matrix: Matrix3<f64>,
    /// The transformation matrix from original to Niggli basis
    pub transformation: Matrix3<f64>,
    /// The Niggli form type
    pub form: NiggliForm,
}

/// Niggli-reduced G6 representation: the 6 unique components of the metric tensor
/// of the Niggli-reduced lattice. Used as a canonical lattice key for identity/dedup.
#[derive(Debug, Clone)]
pub struct NiggliG6 {
    /// a·a (squared length of first basis vector)
    pub a2: f64,
    /// b·b (squared length of second basis vector)
    pub b2: f64,
    /// c·c (squared length of third basis vector)
    pub c2: f64,
    /// 2(b·c) (twice the dot product of second and third vectors)
    pub bc_2: f64,
    /// 2(a·c) (twice the dot product of first and third vectors)
    pub ac_2: f64,
    /// 2(a·b) (twice the dot product of first and second vectors)
    pub ab_2: f64,
}

impl NiggliG6 {
    /// Extract G6 components from a Niggli-reduced cell matrix.
    /// Rows of the matrix are the lattice basis vectors a, b, c.
    pub fn from_niggli_cell(cell: &NiggliCell) -> Self {
        let [av, bv, cv] = [0, 1, 2].map(|idx| cell.matrix.row(idx).transpose());
        Self {
            a2: av.dot(&av),
            b2: bv.dot(&bv),
            c2: cv.dot(&cv),
            bc_2: 2.0 * bv.dot(&cv),
            ac_2: 2.0 * av.dot(&cv),
            ab_2: 2.0 * av.dot(&bv),
        }
    }

    /// Return as a 6-element array [a², b², c², 2bc, 2ac, 2ab].
    pub fn as_array(&self) -> [f64; 6] {
        [self.a2, self.b2, self.c2, self.bc_2, self.ac_2, self.ab_2]
    }
}

/// Compute the Niggli G6 representation for a lattice.
pub fn niggli_g6(lattice: &Lattice, tolerance: f64) -> Result<NiggliG6> {
    let cell = niggli_reduce(lattice, tolerance)?;
    Ok(NiggliG6::from_niggli_cell(&cell))
}

/// Compute the Niggli-reduced cell of a lattice.
///
/// The Niggli reduction produces a unique reduced cell with:
/// - a ≤ b ≤ c (ordered by length)
/// - Specific conditions on angles depending on form type
///
/// # Arguments
///
/// * `lattice` - The lattice to reduce
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// The Niggli cell information including the reduced matrix and transformation.
///
/// # Errors
///
/// Returns an error if the reduction fails to converge.
pub fn niggli_reduce(lattice: &Lattice, tolerance: f64) -> Result<NiggliCell> {
    let niggli_lattice = lattice.get_niggli_reduced(tolerance)?;
    let niggli_matrix = *niggli_lattice.matrix();

    // Find transformation matrix
    let transformation = find_transformation_matrix(lattice.matrix(), &niggli_matrix);

    // Determine form type
    let metric = niggli_matrix * niggli_matrix.transpose();
    let ksi = 2.0 * metric[(1, 2)];
    let eta = 2.0 * metric[(0, 2)];
    let zeta = 2.0 * metric[(0, 1)];

    let form = if ksi * eta * zeta > 0.0 {
        NiggliForm::TypeI
    } else {
        NiggliForm::TypeII
    };

    Ok(NiggliCell {
        matrix: niggli_matrix,
        transformation,
        form,
    })
}

/// Check if a lattice is already Niggli-reduced.
///
/// # Arguments
///
/// * `lattice` - The lattice to check
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// `true` if the lattice satisfies Niggli conditions.
pub fn is_niggli_reduced(lattice: &Lattice, tolerance: f64) -> bool {
    let lengths = lattice.lengths();
    let matrix = lattice.matrix();
    let metric = matrix * matrix.transpose();

    // Check a ≤ b ≤ c
    if lengths[0] > lengths[1] + tolerance || lengths[1] > lengths[2] + tolerance {
        return false;
    }

    // Get metric tensor components
    let a_sq = metric[(0, 0)];
    let b_sq = metric[(1, 1)];
    let ksi = 2.0 * metric[(1, 2)];
    let eta = 2.0 * metric[(0, 2)];
    let zeta = 2.0 * metric[(0, 1)];

    // Check Type I or Type II conditions
    // Use absolute volume to handle left-handed lattices correctly
    let eps = tolerance * lattice.volume().abs().powf(1.0 / 3.0);

    if ksi * eta * zeta > 0.0 {
        // Type I: all off-diagonal products positive or all negative
        // Check |ξ| ≤ B, |η| ≤ A, |ζ| ≤ A
        ksi.abs() <= b_sq + eps && eta.abs() <= a_sq + eps && zeta.abs() <= a_sq + eps
    } else {
        // Type II: mixed signs or zeros
        // Additional checks for Type II
        let sum = ksi.abs() + eta.abs() + zeta.abs();
        sum <= (a_sq + b_sq) + eps
            && ksi.abs() <= b_sq + eps
            && eta.abs() <= a_sq + eps
            && zeta.abs() <= a_sq + eps
    }
}

// === Delaunay Reduction ===

/// Result of Delaunay reduction.
#[derive(Debug, Clone)]
pub struct DelaunayCell {
    /// The Delaunay-reduced lattice matrix
    pub matrix: Matrix3<f64>,
    /// The transformation matrix from original to Delaunay basis
    pub transformation: Matrix3<f64>,
}

/// Selling-reduced S6 representation: the 6 inner products of the 4 vectors
/// (a, b, c, d=-(a+b+c)) in a Delaunay-reduced basis. Canonicalized by selecting
/// the lexicographically smallest S6 over the 24 permutations of (a, b, c, d).
#[derive(Debug, Clone)]
pub struct SellingS6 {
    /// b·c
    pub bc: f64,
    /// a·c
    pub ac: f64,
    /// a·b
    pub ab: f64,
    /// a·d where d = -(a+b+c)
    pub ad: f64,
    /// b·d where d = -(a+b+c)
    pub bd: f64,
    /// c·d where d = -(a+b+c)
    pub cd: f64,
}

impl SellingS6 {
    /// Return as a 6-element array [bc, ac, ab, ad, bd, cd].
    pub fn as_array(&self) -> [f64; 6] {
        [self.bc, self.ac, self.ab, self.ad, self.bd, self.cd]
    }

    /// Compute the canonicalized S6 by selecting the lexicographically smallest
    /// S6 over all 24 permutations of (a, b, c, d).
    pub fn canonicalize(cell: &DelaunayCell) -> Result<Self> {
        let [av, bv, cv] = [0, 1, 2].map(|idx| cell.matrix.row(idx).transpose());
        let vecs: [Vector3<f64>; 4] = [av, bv, cv, -(av + bv + cv)];

        const PERMS: [[usize; 4]; 24] = [
            [0, 1, 2, 3],
            [0, 1, 3, 2],
            [0, 2, 1, 3],
            [0, 2, 3, 1],
            [0, 3, 1, 2],
            [0, 3, 2, 1],
            [1, 0, 2, 3],
            [1, 0, 3, 2],
            [1, 2, 0, 3],
            [1, 2, 3, 0],
            [1, 3, 0, 2],
            [1, 3, 2, 0],
            [2, 0, 1, 3],
            [2, 0, 3, 1],
            [2, 1, 0, 3],
            [2, 1, 3, 0],
            [2, 3, 0, 1],
            [2, 3, 1, 0],
            [3, 0, 1, 2],
            [3, 0, 2, 1],
            [3, 1, 0, 2],
            [3, 1, 2, 0],
            [3, 2, 0, 1],
            [3, 2, 1, 0],
        ];

        PERMS
            .iter()
            .map(|perm| {
                let [va, vb, vc, vd] = perm.map(|idx| vecs[idx]);
                Self {
                    bc: vb.dot(&vc),
                    ac: va.dot(&vc),
                    ab: va.dot(&vb),
                    ad: va.dot(&vd),
                    bd: vb.dot(&vd),
                    cd: vc.dot(&vd),
                }
            })
            .min_by(|left, right| {
                left.as_array()
                    .partial_cmp(&right.as_array())
                    .unwrap_or(std::cmp::Ordering::Equal)
            })
            .ok_or_else(|| FerroxError::InvalidLattice {
                reason: "Failed to canonicalize S6 (empty permutations)".to_string(),
            })
    }
}

/// Compute the canonicalized Selling S6 representation for a lattice.
pub fn selling_s6(lattice: &Lattice, tolerance: f64) -> Result<SellingS6> {
    let cell = delaunay_reduce(lattice, tolerance)?;
    SellingS6::canonicalize(&cell)
}

/// Compute the Delaunay-reduced cell of a lattice.
///
/// The Delaunay reduction produces a cell where all pairwise scalar products
/// of lattice vectors are non-positive (all angles ≥ 90°).
///
/// # Arguments
///
/// * `lattice` - The lattice to reduce
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// The Delaunay cell information including the reduced matrix and transformation.
///
/// # Errors
///
/// Returns an error if the reduction fails to converge.
pub fn delaunay_reduce(lattice: &Lattice, tolerance: f64) -> Result<DelaunayCell> {
    // Start with LLL-reduced lattice for numerical stability
    let mut matrix = lattice.lll_matrix();
    let mut total_transform = lattice.lll_mapping();

    // Use absolute volume to handle left-handed lattices correctly
    let eps = tolerance * lattice.volume().abs().powf(1.0 / 3.0);
    const MAX_ITER: usize = 100;

    for _ in 0..MAX_ITER {
        let mut changed = false;

        // Check and fix each pair of vectors
        for idx in 0..3 {
            for jdx in (idx + 1)..3 {
                let vec_i = matrix.row(idx).transpose();
                let vec_j = matrix.row(jdx).transpose();
                let dot = vec_i.dot(&vec_j);

                if dot > eps {
                    // Reduce: replace longer vector with v_long - v_short
                    let norm_i = vec_i.norm_squared();
                    let norm_j = vec_j.norm_squared();

                    let transform = if norm_i > norm_j {
                        // Replace v_i with v_i - v_j
                        let new_row = vec_i - vec_j;
                        matrix.set_row(idx, &new_row.transpose());
                        create_shear_transform(idx, jdx, -1)
                    } else {
                        // Replace v_j with v_j - v_i
                        let new_row = vec_j - vec_i;
                        matrix.set_row(jdx, &new_row.transpose());
                        create_shear_transform(jdx, idx, -1)
                    };
                    total_transform = transform * total_transform;
                    changed = true;
                }
            }
        }

        if !changed {
            return Ok(DelaunayCell {
                matrix,
                transformation: total_transform,
            });
        }
    }

    Err(FerroxError::ReductionNotConverged {
        iterations: MAX_ITER,
    })
}

// === Supercell Generation ===

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

// === Lattice Equivalence ===

/// Check if two lattices are equivalent within tolerances.
///
/// Two lattices are equivalent if one can be transformed to the other by
/// an integer transformation matrix with determinant ±1.
///
/// # Arguments
///
/// * `lattice1` - First lattice
/// * `lattice2` - Second lattice
/// * `length_tol` - Fractional tolerance for lattice vector lengths
/// * `angle_tol` - Tolerance for angles in degrees
///
/// # Returns
///
/// `true` if the lattices are equivalent.
pub fn lattices_equivalent(
    lattice1: &Lattice,
    lattice2: &Lattice,
    length_tol: f64,
    angle_tol: f64,
) -> bool {
    lattice1
        .find_mapping(lattice2, length_tol, angle_tol, true)
        .is_some()
}

/// Check if one lattice is a supercell of another.
///
/// Returns the transformation matrix if supercell is a supercell of primitive.
///
/// # Arguments
///
/// * `primitive` - The primitive cell lattice
/// * `supercell` - The potential supercell lattice
/// * `tolerance` - Numerical tolerance for comparisons
///
/// # Returns
///
/// `Some(matrix)` with the integer transformation matrix if supercell is indeed
/// a supercell, `None` otherwise.
pub fn is_supercell(
    primitive: &Lattice,
    supercell: &Lattice,
    tolerance: f64,
) -> Option<[[i32; 3]; 3]> {
    // The volume ratio should be close to a positive integer.
    // Use absolute value to allow opposite-handed (mirrored) supercells.
    let vol_ratio = supercell.volume() / primitive.volume();
    let vol_ratio_abs = vol_ratio.abs();
    let vol_int = vol_ratio_abs.round() as i32;

    if (vol_ratio_abs - vol_int as f64).abs() > tolerance {
        return None;
    }

    if vol_int <= 0 {
        return None;
    }

    // Find transformation: supercell_matrix = transform * primitive_matrix
    // So transform = supercell_matrix * primitive_matrix^(-1)
    let prim_inv = primitive.inv_matrix();
    let transform_f64 = supercell.matrix() * prim_inv;

    // Check if transformation is integer
    let mut transform = [[0i32; 3]; 3];
    for row in 0..3 {
        for col in 0..3 {
            let val = transform_f64[(row, col)];
            let rounded = val.round();
            if (val - rounded).abs() > tolerance {
                return None;
            }
            transform[row][col] = rounded as i32;
        }
    }

    // Verify determinant matches volume ratio
    let det = matrix_det_i32(&transform);
    if det.abs() != vol_int as i64 {
        return None;
    }

    Some(transform)
}

// === Helper Functions ===

/// Find the transformation matrix between two lattice matrices.
fn find_transformation_matrix(original: &Matrix3<f64>, transformed: &Matrix3<f64>) -> Matrix3<f64> {
    // transformed = transform * original
    // So transform = transformed * original^(-1)
    if let Some(inv) = original.try_inverse() {
        transformed * inv
    } else {
        Matrix3::identity()
    }
}

/// Create a shear transformation matrix.
fn create_shear_transform(target_row: usize, source_row: usize, factor: i32) -> Matrix3<f64> {
    let mut transform = Matrix3::<f64>::identity();
    transform[(target_row, source_row)] = factor as f64;
    transform
}

/// Compute determinant of a 3x3 integer matrix.
/// Uses i64 arithmetic to avoid overflow for large transformation matrices.
fn matrix_det_i32(matrix: &[[i32; 3]; 3]) -> i64 {
    let m00 = matrix[0][0] as i64;
    let m01 = matrix[0][1] as i64;
    let m02 = matrix[0][2] as i64;
    let m10 = matrix[1][0] as i64;
    let m11 = matrix[1][1] as i64;
    let m12 = matrix[1][2] as i64;
    let m20 = matrix[2][0] as i64;
    let m21 = matrix[2][1] as i64;
    let m22 = matrix[2][2] as i64;

    m00 * (m11 * m22 - m12 * m21) - m01 * (m10 * m22 - m12 * m20) + m02 * (m10 * m21 - m11 * m20)
}

#[cfg(test)]
mod tests {
    use super::*;
    use approx::assert_relative_eq;

    #[test]
    fn test_wrap_to_half() {
        assert_relative_eq!(wrap_to_half(0.3), 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_half(0.7), -0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_half(-0.3), -0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_half(-0.7), 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_half(1.3), 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_half(-1.3), -0.3, epsilon = 1e-10);
    }

    #[test]
    fn test_wrap_to_unit() {
        assert_relative_eq!(wrap_to_unit(0.3), 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_unit(1.3), 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_unit(-0.3), 0.7, epsilon = 1e-10);
        assert_relative_eq!(wrap_to_unit(-1.3), 0.7, epsilon = 1e-10);
    }

    #[test]
    fn test_is_inside_unit_cell() {
        let inside = Vector3::new(0.5, 0.5, 0.5);
        let outside_high = Vector3::new(0.5, 0.5, 1.5);
        let outside_low = Vector3::new(-0.5, 0.5, 0.5);
        let on_boundary = Vector3::new(0.0, 0.0, 0.0);

        assert!(is_inside_unit_cell(&inside, 1e-10));
        assert!(!is_inside_unit_cell(&outside_high, 1e-10));
        assert!(!is_inside_unit_cell(&outside_low, 1e-10));
        assert!(is_inside_unit_cell(&on_boundary, 1e-10));
    }

    #[test]
    fn test_perpendicular_distances_cubic() {
        let lattice = Lattice::cubic(4.0);
        let perp = perpendicular_distances(&lattice);

        // For cubic lattice, perpendicular distances equal lattice parameter
        assert_relative_eq!(perp[0], 4.0, epsilon = 1e-10);
        assert_relative_eq!(perp[1], 4.0, epsilon = 1e-10);
        assert_relative_eq!(perp[2], 4.0, epsilon = 1e-10);
    }

    #[test]
    fn test_perpendicular_distances_orthorhombic() {
        let lattice = Lattice::orthorhombic(3.0, 4.0, 5.0);
        let perp = perpendicular_distances(&lattice);

        // For orthorhombic, perpendicular distances equal lattice parameters
        assert_relative_eq!(perp[0], 3.0, epsilon = 1e-10);
        assert_relative_eq!(perp[1], 4.0, epsilon = 1e-10);
        assert_relative_eq!(perp[2], 5.0, epsilon = 1e-10);
    }

    #[test]
    fn test_minimum_image_distance_cubic() {
        let lattice = Lattice::cubic(4.0);
        let pbc = [true, true, true];

        // Same point
        let pos1 = Vector3::new(0.0, 0.0, 0.0);
        let dist = minimum_image_distance(&lattice, &pos1, &pos1, pbc);
        assert_relative_eq!(dist, 0.0, epsilon = 1e-10);

        // Points across boundary
        let pos2 = Vector3::new(0.1, 0.0, 0.0);
        let pos3 = Vector3::new(0.9, 0.0, 0.0);
        let dist = minimum_image_distance(&lattice, &pos2, &pos3, pbc);
        // Should be 0.2 * 4.0 = 0.8 (not 0.8 * 4.0 = 3.2)
        assert_relative_eq!(dist, 0.8, epsilon = 1e-10);
    }

    #[test]
    fn test_is_highly_skewed() {
        let cubic = Lattice::cubic(4.0);
        assert!(!is_highly_skewed(&cubic));

        // Triclinic with moderate angles (all within 30° of 90°)
        let triclinic = Lattice::from_parameters(4.0, 5.0, 6.0, 70.0, 80.0, 100.0);
        assert!(!is_highly_skewed(&triclinic));

        // Very skewed cell (angles more than 30° from 90°)
        let skewed = Lattice::from_parameters(4.0, 4.0, 4.0, 45.0, 45.0, 45.0);
        assert!(is_highly_skewed(&skewed));
    }

    #[test]
    fn test_find_supercell_for_target_atoms() {
        let lattice = Lattice::cubic(4.0);
        let n_atoms = 2;

        // Target 16 atoms = 2 * 8, so 2×2×2 supercell
        let matrix = find_supercell_for_target_atoms(&lattice, n_atoms, 16);
        let det = matrix[0][0] * matrix[1][1] * matrix[2][2]; // Diagonal matrix
        assert_eq!(det * n_atoms as i32, 16);
    }

    #[test]
    fn test_find_supercell_for_min_length() {
        let lattice = Lattice::cubic(4.0);

        // Need minimum 10 Å
        let matrix = find_supercell_for_min_length(&lattice, 10.0);
        // 4.0 * 3 = 12 Å ≥ 10 Å
        assert_eq!(matrix[0][0], 3);
        assert_eq!(matrix[1][1], 3);
        assert_eq!(matrix[2][2], 3);
    }

    #[test]
    fn test_niggli_reduction_cubic() {
        let lattice = Lattice::cubic(4.0);
        let niggli = niggli_reduce(&lattice, 1e-5).unwrap();

        // Cubic lattice is already Niggli-reduced
        let lengths = Lattice::new(niggli.matrix).lengths();
        assert_relative_eq!(lengths[0], 4.0, epsilon = 1e-5);
        assert_relative_eq!(lengths[1], 4.0, epsilon = 1e-5);
        assert_relative_eq!(lengths[2], 4.0, epsilon = 1e-5);
    }

    #[test]
    fn test_niggli_reduction_preserves_volume() {
        let lattice = Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0);
        let niggli = niggli_reduce(&lattice, 1e-5).unwrap();
        let niggli_lattice = Lattice::new(niggli.matrix);

        assert_relative_eq!(
            niggli_lattice.volume().abs(),
            lattice.volume().abs(),
            epsilon = 1e-3
        );
    }

    #[test]
    fn test_niggli_ordered_lengths() {
        let lattice = Lattice::from_parameters(5.0, 3.0, 4.0, 80.0, 90.0, 100.0);
        let niggli = niggli_reduce(&lattice, 1e-5).unwrap();
        let lengths = Lattice::new(niggli.matrix).lengths();

        // Niggli should give a ≤ b ≤ c
        assert!(lengths[0] <= lengths[1] + 1e-5);
        assert!(lengths[1] <= lengths[2] + 1e-5);
    }

    #[test]
    fn test_is_supercell() {
        let primitive = Lattice::cubic(4.0);
        let supercell = Lattice::new(Matrix3::from_diagonal(&Vector3::new(8.0, 8.0, 8.0)));

        let result = is_supercell(&primitive, &supercell, 1e-5);
        assert!(result.is_some());

        let transform = result.unwrap();
        assert_eq!(transform[0][0], 2);
        assert_eq!(transform[1][1], 2);
        assert_eq!(transform[2][2], 2);
    }

    #[test]
    fn test_lattices_equivalent_identity() {
        let lattice = Lattice::cubic(4.0);
        assert!(lattices_equivalent(&lattice, &lattice, 0.2, 5.0));
    }

    #[test]
    fn test_lattices_equivalent_permutation() {
        let lat1 = Lattice::cubic(4.0);
        // Same lattice with permuted axes
        let lat2 = Lattice::new(Matrix3::new(0.0, 4.0, 0.0, 0.0, 0.0, 4.0, 4.0, 0.0, 0.0));

        assert!(lattices_equivalent(&lat1, &lat2, 0.2, 5.0));
    }

    #[test]
    fn test_wrap_positions_to_unit_cell() {
        let positions = vec![Vector3::new(-0.5, 1.5, 2.3), Vector3::new(0.3, 0.7, -0.2)];

        let wrapped = wrap_positions_to_unit_cell(&positions);

        assert_relative_eq!(wrapped[0][0], 0.5, epsilon = 1e-10);
        assert_relative_eq!(wrapped[0][1], 0.5, epsilon = 1e-10);
        assert_relative_eq!(wrapped[0][2], 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrapped[1][0], 0.3, epsilon = 1e-10);
        assert_relative_eq!(wrapped[1][1], 0.7, epsilon = 1e-10);
        assert_relative_eq!(wrapped[1][2], 0.8, epsilon = 1e-10);
    }

    #[test]
    fn test_closest_image() {
        let lattice = Lattice::cubic(4.0);
        let pbc = [true, true, true];

        let position = Vector3::new(0.9, 0.0, 0.0);
        let reference = Vector3::new(0.1, 0.0, 0.0);

        let closest = closest_image(&lattice, &position, &reference, pbc);

        // Position 0.9 should map to -0.1 relative to reference 0.1
        // So closest should be 0.1 + (-0.2) = -0.1
        assert_relative_eq!(closest[0], -0.1, epsilon = 1e-10);
    }

    #[test]
    fn test_closest_image_skewed_cell() {
        // Highly skewed cell where fractional wrapping alone fails
        // a = [10, 0, 0], b = [9, 1, 0], c = [0, 0, 10]
        // The b-vector is almost parallel to a, creating a very skewed cell
        let matrix = Matrix3::new(10.0, 0.0, 0.0, 9.0, 1.0, 0.0, 0.0, 0.0, 10.0);
        let lattice = Lattice::new(matrix);
        let pbc = [true, true, true];

        // Position at (0.1, 0.6, 0) and reference at (0.1, 0.1, 0)
        // Fractional delta in b is 0.5, so naive wrapping keeps it at 0.5
        // But the image at (0.1, -0.4, 0) = original + (-1 in b) might be closer in Cartesian space
        let position = Vector3::new(0.1, 0.6, 0.0);
        let reference = Vector3::new(0.1, 0.1, 0.0);

        let closest = closest_image(&lattice, &position, &reference, pbc);

        // Compute Cartesian distances to verify we got the closest
        let delta_to_closest = closest - reference;
        let cart_closest = matrix * delta_to_closest;
        let dist_closest = cart_closest.norm();

        // The naive wrapped position would be at (0.1, 0.6, 0) -> delta = (0, 0.5, 0)
        let naive_delta = Vector3::new(0.0, 0.5, 0.0);
        let cart_naive = matrix * naive_delta;
        let dist_naive = cart_naive.norm();

        // Our implementation should find a distance <= naive distance
        assert!(
            dist_closest <= dist_naive + 1e-10,
            "closest_image should find shorter or equal distance: {} vs {}",
            dist_closest,
            dist_naive
        );

        // For this specific skewed cell, verify we found a better image
        // The image with shift_b = -1 gives delta = (0, -0.5, 0)
        // Cart: matrix * (0, -0.5, 0) = (-4.5, -0.5, 0), dist = sqrt(20.5) ≈ 4.53
        // Naive: matrix * (0, 0.5, 0) = (4.5, 0.5, 0), dist = sqrt(20.5) ≈ 4.53
        // Both have same distance in this symmetric case, so either is valid
        assert!(dist_closest <= dist_naive + 1e-10);
    }

    #[test]
    fn test_niggli_g6_cubic() {
        let lattice = Lattice::cubic(3.0);
        let g6 = super::niggli_g6(&lattice, 1e-5).unwrap();
        let arr = g6.as_array();
        let a_sq = 9.0;
        assert!((arr[0] - a_sq).abs() < 1e-8, "a² = {}", arr[0]);
        assert!((arr[1] - a_sq).abs() < 1e-8, "b² = {}", arr[1]);
        assert!((arr[2] - a_sq).abs() < 1e-8, "c² = {}", arr[2]);
        for (idx, val) in arr[3..].iter().enumerate() {
            assert!(val.abs() < 1e-8, "off-diagonal G6[{}] = {val}", idx + 3);
        }
    }

    #[test]
    fn test_selling_s6_cubic() {
        let lattice = Lattice::cubic(3.0);
        let s6 = super::selling_s6(&lattice, 1e-5).unwrap();
        let arr = s6.as_array();
        for (idx, val) in arr.iter().enumerate() {
            assert!(*val <= 1e-8, "S6[{idx}] = {val} should be non-positive");
        }
    }

    #[test]
    fn test_selling_s6_canonical_invariance() {
        // Asymmetric (triclinic-like) lattice: a=3, b=4, c=5, different angles
        let row_a = [3.0, 0.0, 0.0];
        let row_b = [1.0, 4.0, 0.0];
        let row_c = [0.5, 0.5, 5.0];
        let reference = Lattice::new(Matrix3::new(
            row_a[0], row_a[1], row_a[2], row_b[0], row_b[1], row_b[2], row_c[0], row_c[1],
            row_c[2],
        ));
        let s6_ref = super::selling_s6(&reference, 1e-5).unwrap().as_array();

        // Test multiple basis permutations: (b,c,a), (c,a,b), (c,b,a)
        let permuted_rows = [
            (row_b, row_c, row_a),
            (row_c, row_a, row_b),
            (row_c, row_b, row_a),
        ];
        for (perm_idx, (ra, rb, rc)) in permuted_rows.iter().enumerate() {
            let perm_lattice = Lattice::new(Matrix3::new(
                ra[0], ra[1], ra[2], rb[0], rb[1], rb[2], rc[0], rc[1], rc[2],
            ));
            let s6_perm = super::selling_s6(&perm_lattice, 1e-5).unwrap().as_array();
            for idx in 0..6 {
                assert!(
                    (s6_ref[idx] - s6_perm[idx]).abs() < 1e-6,
                    "permutation {perm_idx}: S6 should be invariant: {s6_ref:?} vs {s6_perm:?}"
                );
            }
        }
    }

    #[test]
    fn test_closest_image_asymmetric_skewed() {
        // More asymmetric skewed cell to ensure we pick the correct image
        // a = [4, 0, 0], b = [3, 1, 0], c = [0, 0, 4]
        let matrix = Matrix3::new(4.0, 0.0, 0.0, 3.0, 1.0, 0.0, 0.0, 0.0, 4.0);
        let lattice = Lattice::new(matrix);
        let pbc = [true, true, true];

        // Position (0, 0.4, 0), reference (0, 0, 0)
        // Naive: delta = (0, 0.4, 0) -> cart = (1.2, 0.4, 0), dist = sqrt(1.6) ≈ 1.26
        // With shift_b = -1: delta = (0, -0.6, 0) -> cart = (-1.8, -0.6, 0), dist = sqrt(3.6) ≈ 1.90
        // So naive is actually closer here
        let position = Vector3::new(0.0, 0.4, 0.0);
        let reference = Vector3::new(0.0, 0.0, 0.0);

        let closest = closest_image(&lattice, &position, &reference, pbc);
        let delta = closest - reference;

        // Should keep the 0.4 delta since it's closer
        assert_relative_eq!(delta[1], 0.4, epsilon = 1e-10);

        // Now test a case where shift is needed
        // Position (0, 0.8, 0), reference (0, 0, 0)
        // Naive wrapped: delta = (0, -0.2, 0) -> cart = (-0.6, -0.2, 0), dist = sqrt(0.4) ≈ 0.63
        let position2 = Vector3::new(0.0, 0.8, 0.0);
        let closest2 = closest_image(&lattice, &position2, &reference, pbc);
        let delta2 = closest2 - reference;

        // The wrapped delta should be -0.2 (or 0.8 - 1 = -0.2)
        assert_relative_eq!(delta2[1], -0.2, epsilon = 1e-10);
    }
}
