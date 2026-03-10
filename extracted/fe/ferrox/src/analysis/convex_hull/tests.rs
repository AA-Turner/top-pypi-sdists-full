use super::energetics::sorted_elements_from_entries;
use super::*;
use approx::assert_abs_diff_eq;
use std::collections::{HashMap, HashSet};
use std::iter::zip;

fn make_entry(formula: &str, e_form_per_atom: f64, entry_id: &str) -> ConvexHullEntry {
    let composition = Composition::from_formula(formula).expect("formula should parse in tests");
    ConvexHullEntry {
        entry_id: Some(entry_id.to_string()),
        composition,
        energy: e_form_per_atom,
        energy_per_atom: Some(e_form_per_atom),
        e_form_per_atom: Some(e_form_per_atom),
        correction: None,
    }
}

fn make_entry_total_energy(formula: &str, total_energy: f64, entry_id: &str) -> ConvexHullEntry {
    let composition = Composition::from_formula(formula).expect("formula should parse in tests");
    ConvexHullEntry {
        entry_id: Some(entry_id.to_string()),
        composition,
        energy: total_energy,
        energy_per_atom: None,
        e_form_per_atom: None,
        correction: None,
    }
}

#[test]
fn test_corrected_energy_per_atom_variants() {
    let test_cases = [(None, -4.0), (Some(0.6), -3.8)];
    for (case_idx, (correction, expected_value)) in test_cases.into_iter().enumerate() {
        let mut entry = make_entry_total_energy("Li2O", -12.0, &format!("li2o_{case_idx}"));
        entry.correction = correction;
        let corrected_value = entry
            .corrected_energy_per_atom()
            .expect("corrected energy should compute");
        assert_abs_diff_eq!(corrected_value, expected_value, epsilon = 1e-12);
    }
}

fn assert_distances_approx_eq(
    actual_distances: &[f64],
    expected_distances: &[f64],
    tolerance: f64,
) {
    assert_eq!(actual_distances.len(), expected_distances.len());
    for (actual_distance, expected_distance) in zip(actual_distances, expected_distances) {
        assert_abs_diff_eq!(*actual_distance, *expected_distance, epsilon = tolerance);
    }
}

#[test]
fn test_find_lowest_energy_unary_refs_selects_lowest_polymorph() {
    let refs = vec![
        make_entry("Li", -0.1, "li_high"),
        make_entry("Li", -0.3, "li_low"),
        make_entry("O", -0.4, "o"),
        make_entry("LiO", -1.0, "lio"),
    ];
    let unary_refs = find_lowest_energy_unary_refs(&refs).expect("unary refs should build");
    assert_eq!(unary_refs.len(), 2);
    assert_abs_diff_eq!(unary_refs[&Element::Li], -0.3, epsilon = 1e-12);
    assert_abs_diff_eq!(unary_refs[&Element::O], -0.4, epsilon = 1e-12);
}

#[test]
fn test_compute_e_form_per_atom_with_missing_reference_errors() {
    let entry = make_entry_total_energy("LiO", -8.0, "lio");
    let refs = HashMap::from([(Element::Li, -1.0)]);
    let result = compute_e_form_per_atom(&entry, &refs);
    let error = result.expect_err("missing unary reference should fail");
    let FerroxError::CompositionError { reason } = error else {
        panic!("expected CompositionError");
    };
    assert!(reason.contains("Missing unary reference for element O"));
}

#[test]
fn test_compute_e_form_per_atom_prefers_precomputed_value() {
    let entry = make_entry("LiO", -123.0, "lio_precomputed");
    let refs = HashMap::from([(Element::Li, -1.0), (Element::O, -2.0)]);
    let value = compute_e_form_per_atom(&entry, &refs).expect("precomputed value should be used");
    assert_abs_diff_eq!(value, -123.0, epsilon = 1e-12);
}

#[test]
fn test_build_lower_hull_requires_non_empty_references() {
    let result = build_lower_hull(&[]);
    let error = result.expect_err("empty references should fail");
    let FerroxError::CompositionError { reason } = error else {
        panic!("expected CompositionError");
    };
    assert!(reason.contains("Reference entries cannot be empty"));
}

#[test]
fn test_build_lower_hull_requires_terminal_entries_for_elements() {
    let refs = vec![make_entry_total_energy("LiO", -8.0, "lio_only")];
    let result = build_lower_hull(&refs);
    let error = result.expect_err("missing unary references should fail");
    let FerroxError::CompositionError { reason } = error else {
        panic!("expected CompositionError");
    };
    assert!(reason.contains("Missing unary reference for element Li"));
}

#[test]
fn test_binary_e_above_hull() {
    let references = vec![
        make_entry("Li", 0.0, "li"),
        make_entry("O", 0.0, "o"),
        make_entry("LiO", -1.0, "lio"),
        make_entry("Li2O", -0.2, "li2o"),
    ];
    let queries = vec![make_entry("Li2O", -0.2, "li2o")];
    let distances =
        calculate_e_above_hull(&queries, &references).expect("binary hull should compute");
    assert_distances_approx_eq(&distances, &[0.466_666_666_7], 1e-6);
}

#[test]
fn test_unary_system_e_above_hull_is_non_negative_formation_energy() {
    let references = vec![make_entry("Fe", 0.0, "fe_ref")];
    let queries = vec![
        make_entry("Fe", 0.5, "fe_unstable"),
        make_entry("Fe", -0.5, "fe_lower"),
    ];
    let distances =
        calculate_e_above_hull(&queries, &references).expect("unary hull should compute");
    assert_distances_approx_eq(&distances, &[0.5, 0.0], 1e-12);
}

#[test]
fn test_unary_system_with_multiple_reference_entries_uses_reference_minimum() {
    let references = vec![
        make_entry("Fe", -0.5, "fe_ref_low"),
        make_entry("Fe", 0.0, "fe_ref_high"),
    ];
    let queries = vec![make_entry("Fe", 0.2, "fe_query")];
    let distances =
        calculate_e_above_hull(&queries, &references).expect("unary hull should compute");
    assert_distances_approx_eq(&distances, &[0.7], 1e-12);
}

#[test]
fn test_calculate_e_above_hull_errors_on_empty_refs() {
    let queries = vec![make_entry("Li", 0.0, "li")];
    let result = calculate_e_above_hull(&queries, &[]);
    let error = result.expect_err("empty references should fail");
    let FerroxError::CompositionError { reason } = error else {
        panic!("expected CompositionError");
    };
    assert!(reason.contains("Reference entries cannot be empty"));
}

#[test]
fn test_calculate_e_above_hull_errors_on_missing_element_in_reference_system() {
    let references = vec![
        make_entry("Li", 0.0, "li_ref"),
        make_entry("O", 0.0, "o_ref"),
    ];
    let queries = vec![make_entry_total_energy("LiF", -0.4, "lif")];
    let result = calculate_e_above_hull(&queries, &references);
    let error = result.expect_err("missing reference element should fail");
    let FerroxError::CompositionError { reason } = error else {
        panic!("expected CompositionError");
    };
    assert!(reason.contains("Missing unary reference for element F"));
}

#[test]
fn test_calculate_e_above_hull_returns_empty_for_empty_query_batch() {
    let references = vec![make_entry("Li", 0.0, "li"), make_entry("O", 0.0, "o")];
    let distances =
        calculate_e_above_hull(&[], &references).expect("empty query should return empty");
    assert!(distances.is_empty());
}

#[test]
fn test_batch_results_match_single_entry_calls() {
    let references = vec![
        make_entry("Li", 0.0, "li"),
        make_entry("O", 0.0, "o"),
        make_entry("LiO", -1.0, "lio"),
        make_entry("Li2O", -0.2, "li2o"),
    ];
    let queries = vec![
        make_entry("Li2O", -0.2, "q1"),
        make_entry("LiO", -1.0, "q2"),
        make_entry("LiO", -0.7, "q3"),
    ];
    let batch = calculate_e_above_hull(&queries, &references).expect("batch should compute");
    assert_eq!(batch.len(), queries.len());
    for (query, batch_value) in zip(&queries, &batch) {
        let single = calculate_e_above_hull(std::slice::from_ref(query), &references)
            .expect("single should compute");
        assert!((single[0] - batch_value).abs() < 1e-12);
    }
}

#[test]
fn test_ternary_same_composition_above_hull_positive_distance() {
    let references = vec![
        make_entry("Li", 0.0, "li"),
        make_entry("Na", 0.0, "na"),
        make_entry("K", 0.0, "k"),
        make_entry("LiNaK", -1.0, "linak_stable"),
    ];
    let queries = vec![
        make_entry("LiNaK", -0.8, "linak_unstable"),
        make_entry("LiNaK", -1.0, "linak_on_hull"),
    ];
    let distances = calculate_e_above_hull(&queries, &references).expect("ternary should compute");
    assert_distances_approx_eq(&distances, &[0.2, 0.0], 1e-12);
}

#[test]
fn test_quinary_general_nd_hull() {
    let references = vec![
        make_entry("Li", 0.0, "li"),
        make_entry("Na", 0.0, "na"),
        make_entry("K", 0.0, "k"),
        make_entry("Rb", 0.0, "rb"),
        make_entry("Cs", 0.0, "cs"),
        make_entry("LiNaKRbCs", -0.2, "mixed_stable"),
    ];
    let queries = vec![
        make_entry("LiNaKRbCs", -0.1, "mixed_unstable"),
        make_entry("Li", 0.0, "li_query"),
    ];
    let distances =
        calculate_e_above_hull(&queries, &references).expect("quinary hull should compute");
    assert_distances_approx_eq(&distances, &[0.1, 0.0], 1e-8);
}

#[test]
fn test_degenerate_hull_falls_back_to_non_negative_formation_energy() {
    let references = vec![
        make_entry("Li", 0.0, "li"),
        make_entry("Na", 0.0, "na"),
        make_entry("K", 0.0, "k"),
        make_entry("LiNaK", 0.0, "linak"),
    ];
    let queries = vec![
        make_entry("LiNaK", 0.2, "query_positive"),
        make_entry("LiNaK", -0.1, "query_negative"),
    ];
    let distances =
        calculate_e_above_hull(&queries, &references).expect("degenerate hull should compute");
    assert_distances_approx_eq(&distances, &[0.2, 0.0], 1e-12);
}

#[test]
fn test_compute_quickhull_nd_returns_empty_for_underdetermined_inputs() {
    let test_cases: Vec<Vec<Vec<f64>>> = vec![
        vec![],
        vec![vec![0.0, 0.0]],
        vec![vec![0.0, 0.0], vec![1.0, 0.0]],
        vec![
            vec![0.0, 0.0, 0.0],
            vec![1.0, 0.0, 0.0],
            vec![0.0, 1.0, 0.0],
        ],
    ];
    for points in test_cases {
        let facets = compute_quickhull_nd(&points).expect("quickhull should not error");
        assert!(facets.is_empty());
    }
}

#[test]
fn test_compute_quickhull_nd_5d_simplex_has_6_facets() {
    let points = vec![
        vec![0.0, 0.0, 0.0, 0.0, 0.0],
        vec![1.0, 0.0, 0.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0, 0.0, 0.0],
        vec![0.0, 0.0, 1.0, 0.0, 0.0],
        vec![0.0, 0.0, 0.0, 1.0, 0.0],
        vec![0.0, 0.0, 0.0, 0.0, 1.0],
    ];
    let facets = compute_quickhull_nd(&points).expect("quickhull should compute in 5D");
    assert_eq!(facets.len(), 6);
}

#[test]
fn test_compute_lower_hull_nd_filters_by_last_normal_component() {
    let face_up = SimplexFaceND {
        vertex_indices: vec![0, 1, 2],
        plane: HyperplaneND {
            normal: vec![0.0, 0.0, 1.0],
            offset: 0.0,
        },
        centroid: vec![0.0, 0.0, 0.0],
        outside_points: HashSet::new(),
    };
    let face_down = SimplexFaceND {
        vertex_indices: vec![0, 1, 2],
        plane: HyperplaneND {
            normal: vec![0.0, 0.0, -1.0],
            offset: 0.0,
        },
        centroid: vec![0.0, 0.0, 0.0],
        outside_points: HashSet::new(),
    };
    let lower = compute_lower_hull_nd(&[face_up, face_down.clone()]);
    assert_eq!(lower.len(), 1);
    assert_eq!(lower[0].vertex_indices, face_down.vertex_indices);
}

#[test]
fn test_compute_e_above_hull_nd_interpolates_simple_triangle() {
    let points = vec![
        vec![0.0, 0.0, 0.0],
        vec![1.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0],
    ];
    let lower_face = SimplexFaceND {
        vertex_indices: vec![0, 1, 2],
        plane: HyperplaneND {
            normal: vec![0.0, 0.0, -1.0],
            offset: 0.0,
        },
        centroid: vec![0.0, 0.0, 0.0],
        outside_points: HashSet::new(),
    };
    let query_points = vec![vec![0.25, 0.25, 0.0], vec![0.25, 0.25, 0.4]];
    let distances = compute_e_above_hull_nd(&query_points, &[lower_face], &points);
    assert_distances_approx_eq(&distances, &[0.0, 0.4], 1e-12);
}

#[test]
fn test_compute_e_above_hull_nd_returns_nan_outside_domain() {
    let points = vec![
        vec![0.0, 0.0, 0.0],
        vec![1.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0],
    ];
    let lower_face = SimplexFaceND {
        vertex_indices: vec![0, 1, 2],
        plane: HyperplaneND {
            normal: vec![0.0, 0.0, -1.0],
            offset: 0.0,
        },
        centroid: vec![0.0, 0.0, 0.0],
        outside_points: HashSet::new(),
    };
    let query_points = vec![vec![1.2, 1.2, 0.1]];
    let distances = compute_e_above_hull_nd(&query_points, &[lower_face], &points);
    assert!(distances[0].is_nan());
}

#[test]
fn test_compute_e_above_hull_nd_returns_nan_when_hull_is_empty() {
    let points = vec![
        vec![0.0, 0.0, 0.0],
        vec![1.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0],
    ];
    let distances = compute_e_above_hull_nd(&[vec![0.25, 0.25, 0.1]], &[], &points);
    assert!(distances[0].is_nan());
}

#[test]
fn test_compute_e_above_hull_nd_returns_nan_for_malformed_facets() {
    let points = vec![
        vec![0.0, 0.0, 0.0],
        vec![1.0, 0.0, 0.0],
        vec![0.0, 1.0, 0.0],
    ];
    let malformed_empty_face = SimplexFaceND {
        vertex_indices: vec![],
        plane: HyperplaneND {
            normal: vec![0.0, 0.0, -1.0],
            offset: 0.0,
        },
        centroid: vec![],
        outside_points: HashSet::new(),
    };
    let malformed_oob_face = SimplexFaceND {
        vertex_indices: vec![0, 1, 99],
        plane: HyperplaneND {
            normal: vec![0.0, 0.0, -1.0],
            offset: 0.0,
        },
        centroid: vec![0.0, 0.0, 0.0],
        outside_points: HashSet::new(),
    };
    let distances = compute_e_above_hull_nd(
        &[vec![0.25, 0.25, 0.1]],
        &[malformed_empty_face, malformed_oob_face],
        &points,
    );
    assert!(distances[0].is_nan());
}

#[test]
fn test_sorted_elements_from_entries_uses_atomic_number_ordering() {
    let refs = vec![
        make_entry("Na", 0.0, "na"),
        make_entry("Li", 0.0, "li"),
        make_entry("O", 0.0, "o"),
    ];
    let ordering = sorted_elements_from_entries(&refs);
    assert_eq!(ordering, vec![Element::Li, Element::O, Element::Na]);
}

#[test]
fn test_reference_and_query_with_same_entries_are_all_on_hull() {
    let references = vec![
        make_entry("Li", 0.0, "li"),
        make_entry("O", 0.0, "o"),
        make_entry("LiO", -1.0, "lio"),
    ];
    let mut queries = references.clone();
    queries.push(make_entry("LiO", -0.8, "lio_above"));
    let distances =
        calculate_e_above_hull(&queries, &references).expect("self-hull distances should compute");
    assert_distances_approx_eq(&distances, &[0.0, 0.0, 0.0, 0.2], 1e-12);
}

#[test]
fn test_precomputed_e_form_reference_set_is_used_without_synthetic_zero_corners() {
    let references = vec![
        make_entry("Li", 1.0, "li"),
        make_entry("O", 1.0, "o"),
        make_entry("LiO", 0.5, "lio"),
    ];
    let distances =
        calculate_e_above_hull(&references, &references).expect("self-hull should compute");
    assert_distances_approx_eq(&distances, &[0.0, 0.0, 0.0], 1e-12);
}
