use crate::lattice::Lattice;

use super::helpers::matrix_det_i32;

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
