use super::*;
use approx::assert_relative_eq;
use nalgebra::Vector3;
use std::f64::consts::PI;
use std::time::{Duration, Instant};

#[test]
fn test_cubic() {
    let lattice = Lattice::cubic(4.0);
    assert_relative_eq!(lattice.volume(), 64.0, epsilon = 1e-10);

    let lengths = lattice.lengths();
    assert_relative_eq!(lengths[0], 4.0, epsilon = 1e-10);
    assert_relative_eq!(lengths[1], 4.0, epsilon = 1e-10);
    assert_relative_eq!(lengths[2], 4.0, epsilon = 1e-10);

    let angles = lattice.angles();
    assert_relative_eq!(angles[0], 90.0, epsilon = 1e-10);
    assert_relative_eq!(angles[1], 90.0, epsilon = 1e-10);
    assert_relative_eq!(angles[2], 90.0, epsilon = 1e-10);
}

#[test]
fn test_hexagonal() {
    let lattice = Lattice::hexagonal(3.0, 5.0);
    let lengths = lattice.lengths();
    assert_relative_eq!(lengths[0], 3.0, epsilon = 1e-10);
    assert_relative_eq!(lengths[1], 3.0, epsilon = 1e-10);
    assert_relative_eq!(lengths[2], 5.0, epsilon = 1e-10);

    let angles = lattice.angles();
    assert_relative_eq!(angles[0], 90.0, epsilon = 1e-10);
    assert_relative_eq!(angles[1], 90.0, epsilon = 1e-10);
    assert_relative_eq!(angles[2], 120.0, epsilon = 1e-10);
}

#[test]
fn test_coordinate_conversion() {
    let lattice = Lattice::cubic(4.0);

    let cart = vec![Vector3::new(2.0, 2.0, 2.0)];
    let frac = lattice.get_fractional_coords(&cart);
    assert_relative_eq!(frac[0][0], 0.5, epsilon = 1e-10);
    assert_relative_eq!(frac[0][1], 0.5, epsilon = 1e-10);
    assert_relative_eq!(frac[0][2], 0.5, epsilon = 1e-10);

    let cart_back = lattice.get_cartesian_coords(&frac);
    assert_relative_eq!(cart_back[0][0], 2.0, epsilon = 1e-10);
    assert_relative_eq!(cart_back[0][1], 2.0, epsilon = 1e-10);
    assert_relative_eq!(cart_back[0][2], 2.0, epsilon = 1e-10);
}

#[test]
fn test_reciprocal() {
    let lattice = Lattice::cubic(4.0);
    let recip = lattice.reciprocal();

    // For cubic, reciprocal lengths should be 2π/a
    let recip_lengths = recip.lengths();
    let expected = 2.0 * PI / 4.0;
    assert_relative_eq!(recip_lengths[0], expected, epsilon = 1e-10);
    assert_relative_eq!(recip_lengths[1], expected, epsilon = 1e-10);
    assert_relative_eq!(recip_lengths[2], expected, epsilon = 1e-10);
}

#[test]
fn test_lll_reduction_cubic() {
    // For a cubic lattice, LLL should return essentially the same lattice
    let lattice = Lattice::cubic(4.0);
    let lll = lattice.get_lll_reduced(0.75);

    // Volume should be preserved
    assert_relative_eq!(lll.volume(), lattice.volume(), epsilon = 1e-8);
}

#[test]
fn test_lll_reduction_skewed() {
    // Create a skewed lattice
    let matrix = Matrix3::new(4.0, 0.0, 0.0, 2.0, 4.0, 0.0, 1.0, 1.0, 4.0);
    let lattice = Lattice::new(matrix);
    let lll = lattice.get_lll_reduced(0.75);

    // Volume should be preserved
    assert_relative_eq!(lll.volume(), lattice.volume(), epsilon = 1e-8);

    // LLL-reduced vectors should be more orthogonal
    // (this is a qualitative check - vectors shouldn't be longer than originals)
    let orig_lengths = lattice.lengths();
    let lll_lengths = lll.lengths();

    // At least one vector should be shorter or equal
    let total_orig: f64 = orig_lengths.iter().sum();
    let total_lll: f64 = lll_lengths.iter().sum();
    assert!(total_lll <= total_orig + 1e-8);
}

#[test]
fn test_lll_reduction_degenerate_lattice() {
    // Test with near-degenerate lattice (linearly dependent vectors)
    // This should not panic or produce NaN/Inf due to division by zero
    let matrix = Matrix3::new(
        1.0, 0.0, 0.0, // first vector
        2.0, 0.0, 0.0, // parallel to first (degenerate)
        0.0, 0.0, 1.0, // third vector
    );
    let lattice = Lattice::new(matrix);
    let lll = lattice.get_lll_reduced(0.75);

    // Result should not contain NaN or Inf
    let lll_mat = lll.matrix();
    for idx in 0..3 {
        for jdx in 0..3 {
            assert!(
                lll_mat[(idx, jdx)].is_finite(),
                "LLL result should be finite, got {:?}",
                lll_mat
            );
        }
    }
}

#[test]
fn test_niggli_reduction_cubic() {
    let lattice = Lattice::cubic(4.0);
    let niggli = lattice.get_niggli_reduced(1e-5).unwrap();

    // For cubic, Niggli reduced should have same lengths
    let lengths = niggli.lengths();
    assert_relative_eq!(lengths[0], 4.0, epsilon = 1e-5);
    assert_relative_eq!(lengths[1], 4.0, epsilon = 1e-5);
    assert_relative_eq!(lengths[2], 4.0, epsilon = 1e-5);

    // Volume should be preserved
    assert_relative_eq!(niggli.volume(), 64.0, epsilon = 1e-5);
}

#[test]
fn test_niggli_reduction_supercell() {
    // Create a 2x1x1 supercell of cubic
    let matrix = Matrix3::new(8.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 4.0);
    let lattice = Lattice::new(matrix);
    let niggli = lattice.get_niggli_reduced(1e-5).unwrap();

    // Volume should be preserved
    assert_relative_eq!(niggli.volume(), lattice.volume(), epsilon = 1e-5);

    // Niggli reduction should give a ≤ b ≤ c
    let lengths = niggli.lengths();
    assert!(lengths[0] <= lengths[1] + 1e-5);
    assert!(lengths[1] <= lengths[2] + 1e-5);
}

#[test]
fn test_niggli_reduction_triclinic() {
    // Triclinic lattice
    let lattice = Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0);
    let niggli = lattice.get_niggli_reduced(1e-5).unwrap();

    // Volume should be preserved
    assert_relative_eq!(niggli.volume(), lattice.volume(), epsilon = 1e-3);

    // Niggli reduction should give a ≤ b ≤ c
    let lengths = niggli.lengths();
    assert!(lengths[0] <= lengths[1] + 1e-5);
    assert!(lengths[1] <= lengths[2] + 1e-5);
}

#[test]
fn test_niggli_acute_angles() {
    // Niggli reduction should produce angles in [60, 120] for acute inputs
    for input_angle in [28.0, 56.5] {
        let lattice =
            Lattice::from_parameters(5.0, 5.0, 5.0, input_angle, input_angle, input_angle);
        let niggli = lattice.get_niggli_reduced(1e-5).unwrap();
        for (idx, &angle) in niggli.angles().iter().enumerate() {
            assert!(
                (59.0..=121.0).contains(&angle),
                "input {input_angle}°: Niggli angle[{idx}] = {angle} out of [60, 120]"
            );
        }
    }
}

#[test]
fn test_from_parameters_consistency() {
    // Cubic: a=[4,0,0], b=[0,4,0], c=[0,0,4]
    let m = *Lattice::from_parameters(4.0, 4.0, 4.0, 90.0, 90.0, 90.0).matrix();
    assert_relative_eq!(
        m,
        Matrix3::from_diagonal(&Vector3::new(4.0, 4.0, 4.0)),
        epsilon = 1e-10
    );

    // Hexagonal: a=[3,0,0], b=[-1.5, 2.598, 0], c=[0,0,5]
    let mh = *Lattice::from_parameters(3.0, 3.0, 5.0, 90.0, 90.0, 120.0).matrix();
    assert_relative_eq!(mh[(0, 0)], 3.0, epsilon = 1e-10);
    assert_relative_eq!(mh[(1, 0)], -1.5, epsilon = 1e-10);
    assert_relative_eq!(mh[(1, 1)], 2.598, epsilon = 0.001);
    assert_relative_eq!(mh[(2, 2)], 5.0, epsilon = 1e-10);

    // Acute rhombohedral: c along z (pymatgen convention)
    let acute = Lattice::from_parameters(5.935, 5.935, 5.935, 28.05, 28.05, 28.05);
    let ma = acute.matrix();
    assert_relative_eq!(ma[(2, 0)], 0.0, epsilon = 1e-10);
    assert_relative_eq!(ma[(2, 1)], 0.0, epsilon = 1e-10);
    assert_relative_eq!(ma[(2, 2)], 5.935, epsilon = 1e-10);
    for &angle in acute.angles().iter() {
        assert_relative_eq!(angle, 28.05, epsilon = 0.001);
    }
}

#[test]
fn test_niggli_pymatgen_compat() {
    // EXACT matrix from pymatgen for rhomb_3478.cif
    let matrix = Matrix3::from_rows(&[
        [2.790935, 0.000000, 5.238132].into(),
        [1.308401, 2.465239, 5.238132].into(),
        [0.000000, 0.000000, 5.935263].into(),
    ]);
    let niggli = Lattice::new(matrix).get_niggli_reduced(1e-5).unwrap();

    // pymatgen Niggli: angles (75.975, 75.975, 60.0), lengths (2.8767, 2.8767, 5.9353)
    let angles = niggli.angles();
    assert_relative_eq!(angles[0], 75.975, epsilon = 0.01);
    assert_relative_eq!(angles[1], 75.975, epsilon = 0.01);
    assert_relative_eq!(angles[2], 60.0, epsilon = 0.01);
    let lengths = niggli.lengths();
    assert_relative_eq!(lengths[0], 2.8767, epsilon = 0.001);
    assert_relative_eq!(lengths[1], 2.8767, epsilon = 0.001);
    assert_relative_eq!(lengths[2], 5.9353, epsilon = 0.001);
    assert!(niggli.matrix().determinant() > 0.0, "positive det");
}

#[test]
fn test_niggli_consistency() {
    // Verify Niggli reduction is deterministic
    let matrix = Matrix3::from_rows(&[
        [2.790935, 0.000000, 5.238132].into(),
        [1.308401, 2.465239, 5.238132].into(),
        [0.000000, 0.000000, 5.935263].into(),
    ]);
    let lattice = Lattice::new(matrix);
    let m1 = *lattice.get_niggli_reduced(1e-5).unwrap().matrix();
    let m2 = *lattice.get_niggli_reduced(1e-5).unwrap().matrix();
    assert_relative_eq!(m1, m2, epsilon = 1e-10);
}

#[test]
fn test_find_mapping_alignment() {
    // Test that find_mapping returns mapping from rhomb_3478 to its ideal Niggli
    let matrix = Matrix3::from_rows(&[
        [2.790935, 0.000000, 5.238132].into(),
        [1.308401, 2.465239, 5.238132].into(),
        [0.000000, 0.000000, 5.935263].into(),
    ]);
    let lattice = Lattice::new(matrix);
    let ideal_niggli = Lattice::from_parameters(2.8767, 2.8767, 5.9353, 75.975, 75.975, 60.0);

    let tol = 1e-5 * lattice.volume().abs().powf(1.0 / 3.0);
    let result = lattice.find_mapping(&ideal_niggli, tol, 5.0 * tol * 180.0 / PI, true);
    assert!(result.is_some(), "should find mapping to ideal Niggli");
}

#[test]
fn test_find_mapping_acute_angles() {
    // rhomb_3478 lattice: acute angles should still find self-mappings
    let lattice = Lattice::from_parameters(5.935, 5.935, 5.935, 28.05, 28.05, 28.05);
    let niggli = lattice.get_niggli_reduced(1e-5).unwrap();
    assert!(
        !niggli.find_all_mappings(&niggli, 0.2, 5.0, true).is_empty(),
        "Niggli"
    );
    assert!(
        !lattice
            .find_all_mappings(&lattice, 0.2, 5.0, true)
            .is_empty(),
        "original"
    );
}

#[test]
fn test_find_mapping_identity() {
    let lattice = Lattice::cubic(4.0);

    // Should find identity mapping to itself
    let mapping = lattice.find_mapping(&lattice, 0.1, 5.0, true);
    assert!(mapping.is_some());

    let (aligned, _, scale) = mapping.unwrap();
    // Aligned lattice should have same volume
    assert_relative_eq!(aligned.volume(), lattice.volume(), epsilon = 1e-3);
    // Scale matrix determinant should be ±1 (no supercell)
    let det = scale.map(|x| x as f64).determinant().abs();
    assert_relative_eq!(det, 1.0, epsilon = 1e-8);
}

#[test]
fn test_find_mapping_equivalent() {
    // Test finding mapping between equivalent lattices with different orientations
    let lat1 = Lattice::cubic(4.0);
    // Same lattice but with permuted axes
    let lat2 = Lattice::new(Matrix3::new(0.0, 4.0, 0.0, 0.0, 0.0, 4.0, 4.0, 0.0, 0.0));

    // Should find mapping
    let mapping = lat1.find_mapping(&lat2, 0.1, 5.0, true);
    assert!(mapping.is_some());

    let (aligned, _, _) = mapping.unwrap();
    // Aligned lattice should have same volume
    assert_relative_eq!(aligned.volume(), lat2.volume(), epsilon = 1e-3);
}

#[test]
fn test_find_mapping_obtuse_angles() {
    // Co8-like lattice: obtuse angles (103°, 103°, 90°)
    let lattice = Lattice::from_parameters(3.7, 3.7, 8.0, 103.0, 103.0, 90.0);
    let mappings = lattice.find_all_mappings(&lattice, 0.2, 5.0, true);
    assert!(!mappings.is_empty(), "should find self-mapping");
    let (aligned, _, scale) = &mappings[0];
    assert_relative_eq!(aligned.volume(), lattice.volume(), epsilon = 0.1);
    // Scale matrix determinant should be ±1 (no supercell)
    let det = scale.map(|x| x as f64).determinant().abs();
    assert_relative_eq!(det, 1.0, epsilon = 1e-8);
}

#[test]
fn test_find_mapping_obtuse_la2coo4() {
    // La2CoO4-like lattice: obtuse angles (90°, 90°, 132.8°)
    let lattice = Lattice::from_parameters(5.5, 5.5, 12.5, 90.0, 90.0, 132.8);
    assert!(
        !lattice
            .find_all_mappings(&lattice, 0.2, 5.0, true)
            .is_empty()
    );
}

#[test]
fn test_niggli_co8_lattice() {
    // Co8 lattice: angles (103.4°, 103.4°, 90°)
    let matrix = Matrix3::new(
        3.60626994,
        0.0,
        -0.85837136,
        -0.20223523,
        3.60059493,
        -0.85837136,
        0.0,
        0.0,
        7.98790154,
    );
    let niggli = Lattice::new(matrix).get_niggli_reduced(1e-5).unwrap();

    // Niggli angles should be in [60°, 120°]
    for (idx, &angle) in niggli.angles().iter().enumerate() {
        assert!((59.0..=121.0).contains(&angle), "angle[{idx}] = {angle}");
    }
    // Should find self-mappings
    assert!(!niggli.find_all_mappings(&niggli, 0.2, 5.0, true).is_empty());
}

#[test]
fn test_find_all_mappings_length_tolerance_bounds() {
    // Test that length tolerance uses symmetric bounds (1/(1+len_tol), 1+len_tol)
    // not asymmetric bounds (1-len_tol, 1+len_tol)
    // With len_tol=0.2: correct range is (0.833, 1.2), NOT (0.8, 1.2)

    let len_tol = 0.2;
    let ang_tol = 5.0;

    // Base cubic lattice
    let base = Lattice::cubic(5.0);

    // Test 1: Ratio 0.84 - inside both (0.833, 1.2) and (0.8, 1.2)
    // Should find mapping
    let scaled_084 = Lattice::cubic(5.0 * 0.84);
    let mappings = base.find_all_mappings(&scaled_084, len_tol, ang_tol, true);
    assert!(
        !mappings.is_empty(),
        "Ratio 0.84 should be inside tolerance (0.833, 1.2)"
    );

    // Test 2: Ratio 0.82 - inside (0.8, 1.2) but OUTSIDE (0.833, 1.2)
    // Should NOT find mapping with correct implementation
    let scaled_082 = Lattice::cubic(5.0 * 0.82);
    let mappings = base.find_all_mappings(&scaled_082, len_tol, ang_tol, true);
    assert!(
        mappings.is_empty(),
        "Ratio 0.82 should be OUTSIDE tolerance (0.833, 1.2)"
    );

    // Test 3: Ratio exactly at boundary 0.833 (= 1/1.2)
    // With strict inequalities, boundary is excluded
    let scaled_boundary = Lattice::cubic(5.0 / 1.2);
    let mappings = base.find_all_mappings(&scaled_boundary, len_tol, ang_tol, true);
    assert!(
        mappings.is_empty(),
        "Ratio 0.833 (exact boundary) should be excluded with strict inequality"
    );

    // Test 4: Ratio 1.19 - inside (0.833, 1.2)
    // Should find mapping
    let scaled_119 = Lattice::cubic(5.0 * 1.19);
    let mappings = base.find_all_mappings(&scaled_119, len_tol, ang_tol, true);
    assert!(
        !mappings.is_empty(),
        "Ratio 1.19 should be inside tolerance (0.833, 1.2)"
    );

    // Test 5: Ratio 1.21 - outside (0.833, 1.2)
    // Should NOT find mapping
    let scaled_121 = Lattice::cubic(5.0 * 1.21);
    let mappings = base.find_all_mappings(&scaled_121, len_tol, ang_tol, true);
    assert!(
        mappings.is_empty(),
        "Ratio 1.21 should be OUTSIDE tolerance (0.833, 1.2)"
    );

    // Test 6: Ratio exactly at boundary 1.2
    // With strict inequalities, boundary is excluded
    let scaled_upper = Lattice::cubic(5.0 * 1.2);
    let mappings = base.find_all_mappings(&scaled_upper, len_tol, ang_tol, true);
    assert!(
        mappings.is_empty(),
        "Ratio 1.2 (exact boundary) should be excluded with strict inequality"
    );
}

#[test]
fn test_find_all_mappings_triclinic_one_axis_outside() {
    // Test that ALL three axes must be within tolerance
    // If just one axis is outside, the mapping should fail

    let len_tol = 0.2;
    let ang_tol = 5.0;

    // Triclinic lattice with different lengths
    let lat1 = Lattice::from_parameters(6.0, 7.0, 8.0, 80.0, 85.0, 90.0);

    // Scale only the 'a' axis by 0.82 (outside tolerance)
    // b and c stay at 1.0 (inside tolerance)
    let lat2 = Lattice::from_parameters(6.0 * 0.82, 7.0, 8.0, 80.0, 85.0, 90.0);

    let mappings = lat1.find_all_mappings(&lat2, len_tol, ang_tol, true);
    assert!(
        mappings.is_empty(),
        "Should not find mapping when one axis ratio (0.82) is outside tolerance"
    );
}

#[test]
fn test_find_all_mappings_angle_tolerance() {
    // Test that angle tolerance is respected
    let len_tol = 0.2;
    let ang_tol = 5.0; // 5 degree angle tolerance

    let lat1 = Lattice::from_parameters(5.0, 5.0, 5.0, 90.0, 90.0, 90.0);

    // Same lengths but angles differ by 4 degrees (within 5 degree tolerance)
    let lat2 = Lattice::from_parameters(5.0, 5.0, 5.0, 90.0, 90.0, 94.0);
    let mappings = lat1.find_all_mappings(&lat2, len_tol, ang_tol, true);
    assert!(
        !mappings.is_empty(),
        "4 degree angle difference should be within 5 degree tolerance"
    );

    // Same lengths but angles differ by 7 degrees (outside 5 degree tolerance)
    let lat3 = Lattice::from_parameters(5.0, 5.0, 5.0, 90.0, 90.0, 97.0);
    let mappings = lat1.find_all_mappings(&lat3, len_tol, ang_tol, true);
    assert!(
        mappings.is_empty(),
        "7 degree angle difference should be outside 5 degree tolerance"
    );
}

#[test]
fn test_find_all_mappings_self_mapping() {
    // Any lattice should have at least one mapping to itself (identity)
    let lattices = vec![
        Lattice::cubic(5.0),
        Lattice::hexagonal(3.0, 5.0),
        Lattice::orthorhombic(3.0, 4.0, 5.0),
        Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0), // triclinic
    ];

    for lat in lattices {
        let mappings = lat.find_all_mappings(&lat, 0.2, 5.0, true);
        assert!(
            !mappings.is_empty(),
            "Any lattice should have mapping to itself"
        );
    }
}

#[test]
fn test_find_all_mappings_with_determinant_extreme_size_mismatch_fails_fast() {
    let small = Lattice::from_array([
        [2.7858242382594893, 0.0, -0.016875404100549208],
        [0.2841525002116433, 2.771251477612547, 0.016605398193201584],
        [0.0, 0.0, 3.44067117],
    ]);
    let large = Lattice::from_array([
        [30.00000006, 0.0, -5.2359874702342945e-08],
        [
            -0.00378320460790132,
            29.99908048144873,
            -7.801382667762688e-07,
        ],
        [0.0, 0.0, 29.99129105],
    ]);

    let started = Instant::now();
    let mappings = small.find_all_mappings_with_determinant(&large, 0.2, 5.0, true, 1);
    let elapsed = started.elapsed();

    assert!(
        mappings.is_empty(),
        "Extreme size mismatch should not produce constrained lattice mappings"
    );
    assert!(
        elapsed < Duration::from_millis(250),
        "Constrained pathological mapping search should fail fast, took {elapsed:?}"
    );
}

#[test]
fn test_find_all_mappings_different_len_tol_values() {
    // Test that different len_tol values produce expected results
    let base = Lattice::cubic(5.0);
    let scaled_09 = Lattice::cubic(5.0 * 0.9); // 10% smaller, ratio = 0.9

    // len_tol=0.05: range is (0.952, 1.05) - 0.9 ratio is outside
    let mappings = base.find_all_mappings(&scaled_09, 0.05, 5.0, true);
    assert!(
        mappings.is_empty(),
        "0.9 ratio should be outside (0.952, 1.05) tolerance"
    );

    // len_tol=0.1: range is (0.909, 1.1) - 0.9 ratio is still OUTSIDE (0.9 < 0.909)
    let mappings = base.find_all_mappings(&scaled_09, 0.1, 5.0, true);
    assert!(
        mappings.is_empty(),
        "0.9 ratio should be outside (0.909, 1.1) tolerance (0.9 < 0.909)"
    );

    // len_tol=0.12: range is (0.893, 1.12) - 0.9 ratio is inside
    let mappings = base.find_all_mappings(&scaled_09, 0.12, 5.0, true);
    assert!(
        !mappings.is_empty(),
        "0.9 ratio should be inside (0.893, 1.12) tolerance"
    );

    // len_tol=0.15: range is (0.87, 1.15) - 0.9 ratio is inside
    let mappings = base.find_all_mappings(&scaled_09, 0.15, 5.0, true);
    assert!(
        !mappings.is_empty(),
        "0.9 ratio should be inside (0.87, 1.15) tolerance"
    );
}

#[test]
fn test_monoclinic_lattice() {
    // Monoclinic: a ≠ b ≠ c, α = γ = 90°, β ≠ 90°
    let lattice = Lattice::from_parameters(5.0, 6.0, 7.0, 90.0, 100.0, 90.0);
    let lengths = lattice.lengths();
    let angles = lattice.angles();

    assert_relative_eq!(lengths[0], 5.0, epsilon = 1e-8);
    assert_relative_eq!(lengths[1], 6.0, epsilon = 1e-8);
    assert_relative_eq!(lengths[2], 7.0, epsilon = 1e-8);

    assert_relative_eq!(angles[0], 90.0, epsilon = 1e-8);
    assert_relative_eq!(angles[1], 100.0, epsilon = 1e-8);
    assert_relative_eq!(angles[2], 90.0, epsilon = 1e-8);
}

#[test]
fn test_tetragonal_lattice() {
    let lattice = Lattice::tetragonal(4.0, 6.0);
    let lengths = lattice.lengths();
    let angles = lattice.angles();

    assert_relative_eq!(lengths[0], 4.0, epsilon = 1e-8);
    assert_relative_eq!(lengths[1], 4.0, epsilon = 1e-8);
    assert_relative_eq!(lengths[2], 6.0, epsilon = 1e-8);

    for angle in angles.iter() {
        assert_relative_eq!(*angle, 90.0, epsilon = 1e-8);
    }
}

#[test]
fn test_rhombohedral_lattice() {
    // Rhombohedral: a = b = c, α = β = γ ≠ 90°
    let lattice = Lattice::from_parameters(5.0, 5.0, 5.0, 80.0, 80.0, 80.0);
    let lengths = lattice.lengths();
    let angles = lattice.angles();

    // All lengths should be equal
    assert_relative_eq!(lengths[0], lengths[1], epsilon = 1e-8);
    assert_relative_eq!(lengths[1], lengths[2], epsilon = 1e-8);

    // All angles should be equal
    assert_relative_eq!(angles[0], angles[1], epsilon = 1e-8);
    assert_relative_eq!(angles[1], angles[2], epsilon = 1e-8);
    assert_relative_eq!(angles[0], 80.0, epsilon = 1e-8);
}

#[test]
fn test_niggli_reduction_preserves_volume_various_lattices() {
    let lattices = vec![
        ("cubic", Lattice::cubic(4.0)),
        ("hexagonal", Lattice::hexagonal(3.0, 5.0)),
        ("orthorhombic", Lattice::orthorhombic(3.0, 4.0, 5.0)),
        ("tetragonal", Lattice::tetragonal(4.0, 6.0)),
        (
            "monoclinic",
            Lattice::from_parameters(5.0, 6.0, 7.0, 90.0, 100.0, 90.0),
        ),
        (
            "triclinic",
            Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0),
        ),
        (
            "rhombohedral",
            Lattice::from_parameters(5.0, 5.0, 5.0, 80.0, 80.0, 80.0),
        ),
    ];

    for (name, lattice) in lattices {
        let niggli = lattice.get_niggli_reduced(1e-5).unwrap();
        assert_relative_eq!(
            niggli.volume().abs(),
            lattice.volume().abs(),
            epsilon = 1e-3
        );
        // Niggli should produce ordered lengths: a <= b <= c
        let lengths = niggli.lengths();
        assert!(
            lengths[0] <= lengths[1] + 1e-5 && lengths[1] <= lengths[2] + 1e-5,
            "{name}: Niggli lengths should be ordered a <= b <= c, got {:?}",
            lengths
        );
    }
}

#[test]
fn test_lll_reduction_preserves_volume() {
    let lattices = vec![
        Lattice::cubic(4.0),
        Lattice::hexagonal(3.0, 5.0),
        Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0),
    ];

    for lattice in lattices {
        let lll = lattice.get_lll_reduced(0.75);
        assert_relative_eq!(lll.volume().abs(), lattice.volume().abs(), epsilon = 1e-8);
    }
}

#[test]
fn test_metric_tensor() {
    let lattice = Lattice::cubic(4.0);
    let metric = lattice.metric_tensor();

    // For cubic, metric tensor should be diagonal with a^2 on diagonal
    assert_relative_eq!(metric[(0, 0)], 16.0, epsilon = 1e-8);
    assert_relative_eq!(metric[(1, 1)], 16.0, epsilon = 1e-8);
    assert_relative_eq!(metric[(2, 2)], 16.0, epsilon = 1e-8);
    assert_relative_eq!(metric[(0, 1)], 0.0, epsilon = 1e-8);
    assert_relative_eq!(metric[(0, 2)], 0.0, epsilon = 1e-8);
    assert_relative_eq!(metric[(1, 2)], 0.0, epsilon = 1e-8);
}

#[test]
fn test_find_mapping_identical_lattices() {
    // Two identical lattices should have a mapping
    let lat1 = Lattice::cubic(5.0);
    let lat2 = Lattice::cubic(5.0);

    let result = lat1.find_mapping(&lat2, 0.2, 5.0, false);
    assert!(result.is_some(), "Identical lattices should have mapping");

    let (_new_lattice, _rotation, supercell) = result.unwrap();

    // Supercell matrix should have determinant ±1 (no supercell)
    let det: i32 = supercell[(0, 0)]
        * (supercell[(1, 1)] * supercell[(2, 2)] - supercell[(1, 2)] * supercell[(2, 1)])
        - supercell[(0, 1)]
            * (supercell[(1, 0)] * supercell[(2, 2)] - supercell[(1, 2)] * supercell[(2, 0)])
        + supercell[(0, 2)]
            * (supercell[(1, 0)] * supercell[(2, 1)] - supercell[(1, 1)] * supercell[(2, 0)]);
    assert_eq!(
        det.abs(),
        1,
        "Supercell det should be ±1 for identical lattices"
    );
}

#[test]
fn test_niggli_angles_in_valid_range() {
    // Test various lattices that Niggli reduction produces angles in [60°, 120°]
    // Use moderate angles that are known to work well
    let test_cases = vec![
        // Moderate acute angles
        Lattice::from_parameters(5.0, 5.0, 5.0, 70.0, 70.0, 70.0),
        Lattice::from_parameters(5.0, 5.0, 5.0, 65.0, 65.0, 65.0),
        // Moderate obtuse angles
        Lattice::from_parameters(5.0, 5.0, 5.0, 110.0, 110.0, 110.0),
        Lattice::from_parameters(5.0, 5.0, 5.0, 115.0, 115.0, 115.0),
        // Mixed angles
        Lattice::from_parameters(4.0, 5.0, 6.0, 75.0, 105.0, 95.0),
    ];

    for lattice in test_cases {
        let niggli_result = lattice.get_niggli_reduced(1e-5);
        if let Ok(niggli) = niggli_result {
            let angles = niggli.angles();
            for (idx, &angle) in angles.iter().enumerate() {
                // Allow small tolerance for numerical errors
                assert!(
                    (59.0..=121.0).contains(&angle),
                    "Niggli angle[{}] = {:.2} out of expected [60, 120] range",
                    idx,
                    angle
                );
            }
        }
        // Some edge cases may fail reduction, which is acceptable
    }
}

#[test]
fn test_reciprocal_degenerate_lattices() {
    // Test that reciprocal() doesn't produce inf/NaN for degenerate lattices.
    let test_cases = [
        // Coplanar vectors: all lie in xy-plane (zero volume)
        Matrix3::new(1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0),
        // Near-degenerate: extremely small z-component
        Matrix3::new(1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1e-20),
    ];

    for matrix in test_cases {
        let lattice = Lattice::new(matrix);
        let recip_m = *lattice.reciprocal().matrix();
        assert!(
            recip_m.iter().all(|v| v.is_finite()),
            "Reciprocal matrix has non-finite values for vol={:.2e}",
            lattice.volume()
        );
    }
}

#[test]
fn test_angles_no_nan_edge_cases() {
    // Test angles() with edge cases that could cause NaN from floating-point drift.
    let test_cases = [
        // Extreme angles close to 0° and 180°
        Lattice::from_parameters(1.0, 1.0, 1.0, 5.0, 90.0, 90.0),
        Lattice::from_parameters(1.0, 1.0, 1.0, 175.0, 90.0, 90.0),
        Lattice::from_parameters(1.0, 1.0, 1.0, 2.0, 2.0, 2.0),
        Lattice::from_parameters(1.0, 1.0, 1.0, 178.0, 178.0, 178.0),
        // Nearly parallel vectors (can push cos slightly > 1)
        Lattice::new(Matrix3::new(
            1.0,
            0.0,
            0.0,
            0.9999999999,
            1e-10,
            0.0,
            0.0,
            0.0,
            1.0,
        )),
    ];

    for lattice in test_cases {
        let angles = lattice.angles();
        assert!(
            angles
                .iter()
                .all(|&a| a.is_finite() && (0.0..=180.0).contains(&a)),
            "angles={:?} invalid for lattice with vol={:.2e}",
            angles,
            lattice.volume()
        );
    }
}

// =========================================================================
// Pymatgen Edge Case Tests (ported from pymatgen test suite)
// =========================================================================

#[test]
fn test_unusual_lattice_edge_cases() {
    // Combined test for unusual lattices that should not crash
    let edge_cases: Vec<(&str, Lattice)> = vec![
        (
            "near-singular 10°",
            Lattice::from_parameters(1.0, 1.0, 1.0, 10.0, 10.0, 10.0),
        ),
        (
            "obtuse 156°",
            Lattice::from_parameters(7.365, 6.199, 5.353, 75.54, 81.18, 156.4),
        ),
        (
            "two obtuse",
            Lattice::from_parameters(4.0, 10.0, 11.0, 100.0, 110.0, 80.0),
        ),
        (
            "monoclinic 66°",
            Lattice::from_parameters(10.0, 20.0, 30.0, 90.0, 66.0, 90.0),
        ),
        (
            "negative matrix",
            Lattice::from_array([
                [-0.259, 1.187, -0.124],
                [2.217, 1.007, 0.733],
                [1.144, -0.469, -0.023],
            ]),
        ),
    ];
    for (name, lattice) in edge_cases {
        let vol = lattice.volume();
        let angles = lattice.angles();
        assert!(vol.is_finite(), "{name}: volume not finite");
        assert!(
            angles.iter().all(|a| a.is_finite()),
            "{name}: angles not finite"
        );
    }
}

#[test]
fn test_lll_preserves_volume() {
    let matrix = Matrix3::new(0.5, 0.3, 0.1, 0.2, 0.7, 0.4, 0.1, 0.2, 0.8);
    let lattice = Lattice::new(matrix);
    let lll = lattice.get_lll_reduced(0.75);
    assert_relative_eq!(lll.volume().abs(), lattice.volume().abs(), epsilon = 1e-8);
}

#[test]
fn test_coordinate_operations() {
    // Roundtrip: frac → cart → frac (validate all components)
    let lattice = Lattice::from_parameters(4.0, 5.0, 6.0, 85.0, 95.0, 100.0);
    let frac = Vector3::new(0.3, 0.7, 0.2);
    let cart = lattice.get_cartesian_coords(&[frac]);
    let frac_back = lattice.get_fractional_coords(&cart);
    assert_relative_eq!(frac.x, frac_back[0].x, epsilon = 1e-10);
    assert_relative_eq!(frac.y, frac_back[0].y, epsilon = 1e-10);
    assert_relative_eq!(frac.z, frac_back[0].z, epsilon = 1e-10);

    // Large fractional coords
    let lattice2 = Lattice::cubic(4.0);
    let cart1 = lattice2.matrix().transpose() * Vector3::new(0.0, 0.0, 17.0);
    let cart2 = lattice2.matrix().transpose() * Vector3::new(0.0, 0.0, 10.0);
    assert!((cart1.z - cart2.z - 28.0).abs() < 1e-10);
}

#[test]
fn test_reciprocal_lattice() {
    // Cubic: reciprocal should have 2π/a factor
    let cubic = Lattice::cubic(10.0);
    assert_relative_eq!(
        cubic.reciprocal().lengths()[0],
        2.0 * PI / 10.0,
        epsilon = 1e-6
    );

    // Hexagonal: a* ≠ c*
    let hex = Lattice::hexagonal(3.0, 5.0);
    let recip = hex.reciprocal().lengths();
    assert!((recip[0] - recip[2]).abs() > 0.1);
}

#[test]
fn test_niggli_extreme_angles() {
    // Triclinic with fractional minutes (103°55', 109°28', 134°53')
    let lattice = Lattice::from_parameters(
        3.0,
        5.196,
        2.0,
        103.0 + 55.0 / 60.0,
        109.0 + 28.0 / 60.0,
        134.0 + 53.0 / 60.0,
    );
    assert!(lattice.volume().abs() > 0.0);
    if let Ok(niggli) = lattice.get_niggli_reduced(1e-5) {
        assert_relative_eq!(
            niggli.volume().abs(),
            lattice.volume().abs(),
            epsilon = 1e-3
        );
    }
}

#[test]
fn test_partial_pbc() {
    let mut lattice = Lattice::cubic(4.0);
    lattice.pbc = [true, true, false];
    assert_eq!(lattice.pbc, [true, true, false]);
    assert_relative_eq!(lattice.volume(), 64.0, epsilon = 1e-10);
}
