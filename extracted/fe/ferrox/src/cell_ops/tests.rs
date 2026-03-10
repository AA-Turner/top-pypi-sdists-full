use super::*;
use crate::lattice::Lattice;
use approx::assert_relative_eq;
use nalgebra::{Matrix3, Vector3};

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
        row_a[0], row_a[1], row_a[2], row_b[0], row_b[1], row_b[2], row_c[0], row_c[1], row_c[2],
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
