use crate::lattice::Lattice;
use crate::pbc::wrap_frac_coord;
use nalgebra::Vector3;

use super::DEGENERATE_LATTICE_TOLERANCE;
use super::supercell::perpendicular_distances;

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
