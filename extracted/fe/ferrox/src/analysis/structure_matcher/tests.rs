use super::*;
use crate::element::Element;
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::{Matrix3, Vector3};
use std::collections::HashMap;

// Helper: single atom at origin in cubic cell
fn make_simple_cubic(element: Element, a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![Species::neutral(element)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
}

// Helper: two atoms in BCC-like positions
fn make_bcc(element: Element, a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![Species::neutral(element), Species::neutral(element)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    )
}

fn make_nacl() -> Structure {
    Structure::new(
        Lattice::cubic(5.64),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    )
}

fn make_nacl_shifted() -> Structure {
    Structure::new(
        Lattice::cubic(5.64),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![Vector3::new(0.01, 0.0, 0.0), Vector3::new(0.51, 0.5, 0.5)],
    )
}

fn make_degenerate_lattice_structure(element: Element) -> Structure {
    let degenerate_lattice =
        Lattice::new(Matrix3::new(1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0));
    Structure::new(
        degenerate_lattice,
        vec![Species::neutral(element)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
}

#[test]
fn test_builder() {
    let matcher = StructureMatcher::new()
        .with_latt_len_tol(0.1)
        .with_site_pos_tol(0.2)
        .with_angle_tol(3.0);

    assert!((matcher.latt_len_tol - 0.1).abs() < 1e-10);
    assert!((matcher.site_pos_tol - 0.2).abs() < 1e-10);
    assert!((matcher.angle_tol - 3.0).abs() < 1e-10);
}

#[test]
fn test_fit_identical() {
    let s = make_nacl();
    let matcher = StructureMatcher::new();
    assert!(matcher.fit(&s, &s));
}

#[test]
fn test_fit_shifted() {
    let s1 = make_nacl();
    let s2 = make_nacl_shifted();
    let matcher = StructureMatcher::new();
    // Should match within default tolerance
    assert!(matcher.fit(&s1, &s2));
}

#[test]
fn test_fit_different_composition() {
    let s1 = make_nacl();
    // KCl instead of NaCl
    let lattice = Lattice::cubic(5.64);
    let species = vec![Species::neutral(Element::K), Species::neutral(Element::Cl)];
    let frac_coords = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    let s2 = Structure::new(lattice, species, frac_coords);

    let matcher = StructureMatcher::new();
    // Different composition should not match
    assert!(!matcher.fit(&s1, &s2));
}

#[test]
fn test_get_rms_dist() {
    let s1 = make_nacl();
    let s2 = make_nacl_shifted();
    let matcher = StructureMatcher::new();

    let result = matcher.get_rms_dist(&s1, &s2);
    assert!(result.is_some());

    let (rms, max_dist) = result.unwrap();
    // RMS should be small for slightly shifted structure
    assert!(rms < 0.1, "RMS {rms} too large");
    assert!(max_dist < 0.2, "max_dist {max_dist} too large");
}

#[test]
fn test_fit_different_sites() {
    // Different number of sites
    let lattice = Lattice::cubic(5.64);
    let s1 = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Na)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let s2 = Structure::new(
        lattice,
        vec![Species::neutral(Element::Na), Species::neutral(Element::Na)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let matcher = StructureMatcher::new();
    // Different number of sites should not match (without supercell)
    assert!(!matcher.fit(&s1, &s2));
}

#[test]
fn test_fit_with_scale_true() {
    // Structures with same shape but different volumes should match with scale=true
    let s1 = make_simple_cubic(Element::Fe, 4.0);
    let s2 = make_simple_cubic(Element::Fe, 6.0); // 50% larger

    let matcher = StructureMatcher::new().with_scale(true);
    assert!(
        matcher.fit(&s1, &s2),
        "Same structure at different scales should match"
    );
}

#[test]
fn test_fit_with_scale_false() {
    // With scale=false and tight len_tol, very different volumes should not match
    let s1 = make_simple_cubic(Element::Fe, 4.0);
    let s2 = make_simple_cubic(Element::Fe, 6.0); // 50% larger, ratio=1.5 well outside len_tol=0.2

    let matcher = StructureMatcher::new().with_scale(false);
    assert!(
        !matcher.fit(&s1, &s2),
        "Very different volumes should not match with scale=false"
    );
}

// Helper: single atom at origin with custom lattice
fn make_single_site(lattice: Lattice, element: Element) -> Structure {
    Structure::new(
        lattice,
        vec![Species::neutral(element)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
}

// Helper: FCC conventional cell (4 atoms)
fn make_fcc_conventional(element: Element, a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![
            Species::neutral(element),
            Species::neutral(element),
            Species::neutral(element),
            Species::neutral(element),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.0),
            Vector3::new(0.5, 0.0, 0.5),
            Vector3::new(0.0, 0.5, 0.5),
        ],
    )
}

#[test]
fn test_fit_angle_tolerance() {
    let s1 = make_single_site(
        Lattice::from_parameters(5.0, 5.0, 5.0, 90.0, 90.0, 90.0),
        Element::Si,
    );
    let matcher = StructureMatcher::new().with_angle_tol(5.0);
    // (gamma, should_match)
    for (gamma, should_match) in [(93.0, true), (110.0, false)] {
        let s2 = make_single_site(
            Lattice::from_parameters(5.0, 5.0, 5.0, 90.0, 90.0, gamma),
            Element::Si,
        );
        assert_eq!(matcher.fit(&s1, &s2), should_match, "gamma={gamma}");
    }
}

#[test]
fn test_fit_site_tolerance_strict() {
    // Use multi-atom structure where relative positions matter
    // Disable primitive_cell since BCC (2 atoms) reduces to primitive (1 atom),
    // which would make the displaced structure also 1 atom and they'd trivially match
    let s1 = make_bcc(Element::Fe, 5.0);
    // Displace second atom significantly (relative to first)
    let s2 = Structure::new(
        Lattice::cubic(5.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.8)], // z displaced by 0.3
    );

    let matcher_strict = StructureMatcher::new()
        .with_site_pos_tol(0.01)
        .with_primitive_cell(false);
    assert!(
        !matcher_strict.fit(&s1, &s2),
        "Large relative displacement should fail with strict site_pos_tol"
    );

    let matcher_lenient = StructureMatcher::new()
        .with_site_pos_tol(0.5)
        .with_primitive_cell(false);
    assert!(
        matcher_lenient.fit(&s1, &s2),
        "Large relative displacement should pass with lenient site_pos_tol"
    );
}

#[test]
fn test_get_rms_dist_no_match() {
    // Completely different structures
    let s1 = make_simple_cubic(Element::Na, 5.0);
    let s2 = make_simple_cubic(Element::Cl, 5.0); // Different element

    let matcher = StructureMatcher::new();
    let result = matcher.get_rms_dist(&s1, &s2);
    assert!(
        result.is_none(),
        "Different compositions should return None for RMS"
    );
}

#[test]
fn test_matcher_builder_chain() {
    let matcher = StructureMatcher::new()
        .with_latt_len_tol(0.1)
        .with_site_pos_tol(0.2)
        .with_angle_tol(3.0)
        .with_scale(true)
        .with_attempt_supercell(false)
        .with_comparator(ComparatorType::Element);

    assert!((matcher.latt_len_tol - 0.1).abs() < 1e-10);
    assert!((matcher.site_pos_tol - 0.2).abs() < 1e-10);
    assert!((matcher.angle_tol - 3.0).abs() < 1e-10);
    assert!(matcher.scale);
    assert!(!matcher.attempt_supercell);
}

#[test]
fn test_group_edge_cases() {
    let matcher = StructureMatcher::new();
    // Empty input
    assert!(matcher.group(&[]).unwrap().is_empty());
    // Single structure
    let s = make_simple_cubic(Element::Fe, 5.0);
    let groups = matcher.group(&[s]).unwrap();
    assert_eq!(groups.len(), 1);
    assert_eq!(groups[&0], vec![0]);
}

#[test]
fn test_group_identical_structures() {
    let s = make_simple_cubic(Element::Fe, 5.0);
    let structures = vec![s.clone(), s.clone(), s.clone()];
    let matcher = StructureMatcher::new();
    let groups = matcher.group(&structures).unwrap();

    // All three should be in one group
    assert_eq!(groups.len(), 1);
    assert_eq!(groups[&0].len(), 3);
}

#[test]
fn test_group_different_compositions() {
    let structures = vec![
        make_simple_cubic(Element::Fe, 5.0),
        make_simple_cubic(Element::Cu, 5.0),
        make_simple_cubic(Element::Ni, 5.0),
    ];

    let matcher = StructureMatcher::new();
    let groups = matcher.group(&structures).unwrap();

    // Each should be its own group
    assert_eq!(
        groups.len(),
        3,
        "Different compositions should be in different groups"
    );
}

#[test]
fn test_deduplicate_preserves_order() {
    let s1 = make_simple_cubic(Element::Fe, 5.0);
    let s2 = make_simple_cubic(Element::Cu, 5.0);

    // s1, s2, s1_copy, s2_copy
    let structures = vec![s1.clone(), s2.clone(), s1.clone(), s2.clone()];
    let matcher = StructureMatcher::new();
    let mapping = matcher.deduplicate(&structures).unwrap().parents;

    // Index 0 -> 0 (first Fe)
    // Index 1 -> 1 (first Cu)
    // Index 2 -> 0 (maps to first Fe)
    // Index 3 -> 1 (maps to first Cu)
    assert_eq!(mapping[0], 0);
    assert_eq!(mapping[1], 1);
    assert_eq!(mapping[2], 0);
    assert_eq!(mapping[3], 1);
}

#[test]
fn test_fit_triclinic_structures() {
    let lattice = Lattice::from_parameters(3.0, 4.0, 5.0, 75.0, 85.0, 95.0);
    let s1 = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Ca), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let s2 = s1.clone();

    let matcher = StructureMatcher::new();
    assert!(
        matcher.fit(&s1, &s2),
        "Identical triclinic structures should match"
    );
}

#[test]
fn test_fit_hexagonal_structures() {
    let lattice = Lattice::hexagonal(3.0, 5.0);
    let s1 = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Ti), Species::neutral(Element::Ti)],
        vec![
            Vector3::new(1.0 / 3.0, 2.0 / 3.0, 0.25),
            Vector3::new(2.0 / 3.0, 1.0 / 3.0, 0.75),
        ],
    );
    let s2 = s1.clone();

    let matcher = StructureMatcher::new();
    assert!(
        matcher.fit(&s1, &s2),
        "Identical hexagonal structures should match"
    );
}

#[test]
fn test_fit_anonymous_identical() {
    let s = make_nacl();
    let matcher = StructureMatcher::new();
    assert!(matcher.fit_anonymous(&s, &s, None));
}

#[test]
fn test_fit_anonymous_swapped_species() {
    // NaCl with swapped species order should match
    let nacl = make_nacl();
    let clna = Structure::new(
        Lattice::cubic(5.64),
        vec![Species::neutral(Element::Cl), Species::neutral(Element::Na)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert!(StructureMatcher::new().fit_anonymous(&nacl, &clna, None));
}

#[test]
fn test_fit_anonymous_same_prototype() {
    // NaCl and MgO have the same rocksalt prototype
    let nacl = make_nacl();
    let mgo = Structure::new(
        Lattice::cubic(4.21),
        vec![Species::neutral(Element::Mg), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert!(StructureMatcher::new().fit_anonymous(&nacl, &mgo, None));
}

#[test]
fn test_fit_anonymous_different_stoichiometry() {
    // AB vs A2B3 stoichiometry should not match
    let nacl = make_nacl();
    let a2b3 = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::Fe),
            Species::neutral(Element::Fe),
            Species::neutral(Element::O),
            Species::neutral(Element::O),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.25, 0.25, 0.25),
            Vector3::new(0.75, 0.75, 0.75),
            Vector3::new(0.25, 0.75, 0.25),
        ],
    );
    assert!(!StructureMatcher::new().fit_anonymous(&nacl, &a2b3, None));
}

#[test]
fn test_fit_anonymous_single_element() {
    let fe = make_simple_cubic(Element::Fe, 4.0);
    let cu = make_simple_cubic(Element::Cu, 4.0);
    let matcher = StructureMatcher::new();
    assert!(matcher.fit_anonymous(&fe, &cu, None));
}

#[test]
fn test_fit_anonymous_different_num_elements() {
    let nacl = make_nacl();
    let fe = make_simple_cubic(Element::Fe, 4.0);
    let matcher = StructureMatcher::new();
    assert!(!matcher.fit_anonymous(&nacl, &fe, None));
}

#[test]
fn test_empty_structures() {
    let lattice = Lattice::cubic(4.0);
    let s1 = Structure::new(lattice.clone(), vec![], vec![]);
    let s2 = Structure::new(lattice, vec![], vec![]);

    let matcher = StructureMatcher::new();
    // Empty structures don't match (early exit when n_sites == 0)
    assert!(!matcher.fit(&s1, &s2));
}

#[test]
fn test_single_site_structure() {
    let s1 = make_simple_cubic(Element::Cu, 4.0);
    let s2 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::new(0.01, 0.01, 0.01)], // slightly shifted
    );

    let matcher = StructureMatcher::new();
    assert!(matcher.fit(&s1, &s2));
}

#[test]
fn test_fit_with_primitive_cell_option() {
    // Two conventional FCC cells at slightly different scales
    let fcc_conv1 = make_fcc_conventional(Element::Cu, 3.6);
    let fcc_conv2 = make_fcc_conventional(Element::Cu, 3.65); // 1.4% larger

    // Without primitive_cell, both have 4 atoms so they can match (with scale=true)
    let matcher_no_prim = StructureMatcher::new().with_primitive_cell(false);
    assert!(
        matcher_no_prim.fit(&fcc_conv1, &fcc_conv2),
        "Same FCC at different scales should match with scale=true"
    );

    // With primitive_cell=true (default), reduction happens first then matching
    let matcher_with_prim = StructureMatcher::new().with_primitive_cell(true);
    assert!(
        matcher_with_prim.fit(&fcc_conv1, &fcc_conv2),
        "Same FCC at different scales should match with primitive_cell=true"
    );

    // Verify that primitive_cell=true reduces site count
    // (implicitly tested by the get_primitive tests in structure.rs)

    // Same structure should always match
    assert!(
        matcher_no_prim.fit(&fcc_conv1, &fcc_conv1),
        "Same structure should match"
    );
}

#[test]
fn test_primitive_cell_reduces_conventional_to_primitive() {
    // Create FCC conventional (4 atoms) and get its moyo-produced primitive (1 atom)
    let fcc_conv = make_fcc_conventional(Element::Cu, 3.6);
    let fcc_prim = fcc_conv.get_primitive(1e-4).unwrap();

    assert_eq!(fcc_conv.num_sites(), 4);
    assert_eq!(fcc_prim.num_sites(), 1);

    // Without primitive_cell, different site counts means no match
    let matcher_no_prim = StructureMatcher::new().with_primitive_cell(false);
    assert!(
        !matcher_no_prim.fit(&fcc_conv, &fcc_prim),
        "4 sites vs 1 site should not match without primitive_cell"
    );

    // With primitive_cell=true, conventional reduces to primitive and should match
    let matcher_with_prim = StructureMatcher::new().with_primitive_cell(true);
    assert!(
        matcher_with_prim.fit(&fcc_conv, &fcc_prim),
        "FCC conventional and its primitive should match with primitive_cell=true"
    );
}

#[test]
fn test_on_error_behavior() {
    // Test that on_error setting is stored correctly
    let matcher_fail = StructureMatcher::new().with_on_error(crate::error::OnError::Fail);
    assert!(matcher_fail.on_error.should_fail());

    let matcher_skip = StructureMatcher::new().with_on_error(crate::error::OnError::Skip);
    assert!(!matcher_skip.on_error.should_fail());
}

#[test]
#[should_panic(expected = "StructureMatcher::fit failed to reduce structure")]
fn test_on_error_fail_panics_in_fit() {
    let invalid_structure = make_degenerate_lattice_structure(Element::Fe);
    let matcher = StructureMatcher::new()
        .with_primitive_cell(true)
        .with_on_error(crate::error::OnError::Fail);
    let _ = matcher.fit(&invalid_structure, &invalid_structure);
}

#[test]
fn test_on_error_skip_does_not_panic_in_fit() {
    let invalid_structure = make_degenerate_lattice_structure(Element::Fe);
    let matcher = StructureMatcher::new()
        .with_primitive_cell(true)
        .with_on_error(crate::error::OnError::Skip);
    let result = std::panic::catch_unwind(|| matcher.fit(&invalid_structure, &invalid_structure));
    assert!(result.is_ok());
}

#[test]
fn test_comparator_type_element() {
    // Test that element comparator ignores oxidation states
    // Use primitive_cell=false to preserve oxidation states (moyo strips them)
    let s1 = Structure::new(
        Lattice::cubic(5.64),
        vec![
            Species::new(Element::Fe, Some(2)),
            Species::new(Element::O, Some(-2)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let s2 = Structure::new(
        Lattice::cubic(5.64),
        vec![
            Species::new(Element::Fe, Some(3)), // different oxidation state
            Species::new(Element::O, Some(-2)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    // Species comparator should NOT match (different oxidation states)
    // Use primitive_cell=false since moyo's primitive reduction loses oxidation states
    let matcher_species = StructureMatcher::new()
        .with_comparator(ComparatorType::Species)
        .with_primitive_cell(false);
    assert!(!matcher_species.fit(&s1, &s2));

    // Element comparator should match (same elements)
    let matcher_element = StructureMatcher::new()
        .with_comparator(ComparatorType::Element)
        .with_primitive_cell(false);
    assert!(matcher_element.fit(&s1, &s2));
}

#[test]
fn test_large_perturbation_no_match() {
    let s1 = make_nacl();
    let s2 = Structure::new(
        Lattice::cubic(5.64),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![
            Vector3::new(0.3, 0.3, 0.3), // large shift
            Vector3::new(0.5, 0.5, 0.5),
        ],
    );

    let matcher = StructureMatcher::new().with_site_pos_tol(0.1);
    assert!(
        !matcher.fit(&s1, &s2),
        "Large perturbation should not match"
    );
}

// =========================================================================
// Degenerate lattice tests
// =========================================================================

#[test]
fn test_fit_degenerate_lattice_zero_volume() {
    // Coplanar vectors - zero volume (degenerate)
    let lattice = Lattice::new(Matrix3::new(
        1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, // third vector in same plane
    ));
    let s = Structure::new(
        lattice,
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::zeros()],
    );
    let matcher = StructureMatcher::new();

    // Should return false gracefully (not panic) for degenerate lattice
    assert!(
        !matcher.fit(&s, &s),
        "Degenerate lattice (zero volume) should return false"
    );
}

#[test]
fn test_fit_near_degenerate_lattice() {
    // Very flat lattice (small c parameter)
    let lattice = Lattice::from_parameters(5.0, 5.0, 0.1, 90.0, 90.0, 90.0);
    let s = Structure::new(
        lattice,
        vec![Species::neutral(Element::C)],
        vec![Vector3::zeros()],
    );
    let matcher = StructureMatcher::new().with_primitive_cell(false);

    // Near-degenerate but non-singular lattice should still self-match deterministically.
    assert!(
        matcher.fit(&s, &s),
        "Near-degenerate lattice should match itself"
    );
}

// =========================================================================
// fit_preprocessed() direct tests
// =========================================================================

#[test]
fn test_fit_preprocessed_skips_reduction() {
    let s1 = make_fcc_conventional(Element::Cu, 3.6);
    let s2 = make_fcc_conventional(Element::Cu, 3.65);
    let matcher = StructureMatcher::new();

    // Manually reduce
    let r1 = matcher.reduce_structure(&s1);
    let r2 = matcher.reduce_structure(&s2);

    // fit_preprocessed should work on already-reduced structures
    assert!(
        matcher.fit_preprocessed(&r1, &r2),
        "Preprocessed FCC structures should match"
    );
}

#[test]
fn test_reduce_structure_produces_niggli_cell() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let matcher = StructureMatcher::new();
    let reduced = matcher.reduce_structure(&fcc);

    // Reduced cell should have fewer or equal sites (FCC -> primitive)
    assert!(
        reduced.num_sites() <= fcc.num_sites(),
        "Reduced structure should have <= sites"
    );
    // Volume should be preserved or reduced by integer factor
    let vol_ratio = fcc.lattice.volume() / reduced.lattice.volume();
    assert!(
        (vol_ratio.round() - vol_ratio).abs() < 0.01,
        "Volume ratio should be close to integer: {vol_ratio}"
    );
}

#[test]
fn test_reduce_structure_idempotent() {
    let s = make_bcc(Element::Fe, 2.87);
    let matcher = StructureMatcher::new();
    let r1 = matcher.reduce_structure(&s);
    let r2 = matcher.reduce_structure(&r1);

    // Reducing twice should give same result
    assert_eq!(
        r1.num_sites(),
        r2.num_sites(),
        "Reducing twice should preserve site count"
    );
    assert!(
        (r1.lattice.volume() - r2.lattice.volume()).abs() < 1e-6,
        "Reducing twice should preserve volume"
    );
}

// =========================================================================
// Extreme tolerance tests
// =========================================================================

#[test]
fn test_fit_very_small_site_tolerance_strict() {
    // Use multi-atom structure (BCC) so relative positions matter
    let s1 = make_bcc(Element::Fe, 4.0);
    // Create perturbed structure with significant relative shift
    let s2 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.7)], // shifted from 0.5
    );
    let matcher = StructureMatcher::new()
        .with_site_pos_tol(0.01)
        .with_primitive_cell(false); // keep multi-atom structure

    // Small tolerance should reject significant perturbation
    assert!(
        !matcher.fit(&s1, &s2),
        "Small tolerance should reject perturbation"
    );
    // Identical should still match
    assert!(
        matcher.fit(&s1, &s1),
        "Identical structures should match with small tolerance"
    );
}

#[test]
fn test_fit_very_large_tolerance_permissive() {
    let s1 = make_simple_cubic(Element::Fe, 4.0);
    let s2 = make_simple_cubic(Element::Fe, 6.0); // 50% larger

    let matcher = StructureMatcher::new()
        .with_site_pos_tol(1.0)
        .with_latt_len_tol(0.5)
        .with_scale(false); // Don't scale volumes

    // Very large tolerance might match very different structures - tests boundary behavior
    let _ = matcher.fit(&s1, &s2);
}

#[test]
fn test_fit_zero_angle_tolerance() {
    let s1 = make_simple_cubic(Element::Fe, 4.0);
    let s2 = Structure::new(
        Lattice::from_parameters(4.0, 4.0, 4.0, 90.0, 90.0, 91.0), // 1° off
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::zeros()],
    );
    let matcher = StructureMatcher::new().with_angle_tol(0.0);

    // Zero angle tolerance should reject 1° deviation
    assert!(
        !matcher.fit(&s1, &s2),
        "Zero angle tolerance should reject 1° deviation"
    );
}

// =========================================================================
// fit_anonymous() edge cases
// =========================================================================

#[test]
fn test_fit_anonymous_many_elements_stress() {
    // 7 elements = 5040 permutations (moderate stress test)
    let lattice = Lattice::cubic(14.0);
    let elements = [
        Element::Li,
        Element::Na,
        Element::K,
        Element::Rb,
        Element::Cs,
        Element::Fr,
        Element::Be,
    ];
    let species: Vec<_> = elements.iter().map(|&e| Species::neutral(e)).collect();
    let coords: Vec<_> = (0..7)
        .map(|i| Vector3::new(i as f64 * 0.14, 0.0, 0.0))
        .collect();
    let s1 = Structure::new(lattice.clone(), species.clone(), coords.clone());

    // Same structure with elements reversed (permuted)
    let species2: Vec<_> = elements
        .iter()
        .rev()
        .map(|&e| Species::neutral(e))
        .collect();
    let s2 = Structure::new(lattice, species2, coords);

    let matcher = StructureMatcher::new().with_primitive_cell(false);
    // Should find a matching permutation within reasonable time
    assert!(
        matcher.fit_anonymous(&s1, &s2, None),
        "fit_anonymous should handle 7 elements (5040 permutations)"
    );
}

#[test]
fn test_fit_anonymous_works_with_any_comparator() {
    // fit_anonymous should work regardless of matcher's comparator_type setting
    let s = make_simple_cubic(Element::Fe, 4.0);

    // Works with default Species comparator
    let matcher_species = StructureMatcher::new();
    assert!(matcher_species.fit_anonymous(&s, &s, None));

    // Works with Element comparator too
    let matcher_element = StructureMatcher::new().with_comparator(ComparatorType::Element);
    assert!(matcher_element.fit_anonymous(&s, &s, None));
}

#[test]
fn test_fit_anonymous_ignores_oxidation_states() {
    // fit_anonymous should ignore oxidation states and match based on elements only
    // Use primitive_cell=false to preserve oxidation states through processing
    let s1 = Structure::new(
        Lattice::cubic(5.64),
        vec![
            Species::new(Element::Na, Some(1)),
            Species::new(Element::Cl, Some(-1)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let s2 = Structure::new(
        Lattice::cubic(5.64),
        vec![
            Species::new(Element::Mg, Some(2)), // Different oxidation state
            Species::new(Element::O, Some(-2)), // Different oxidation state
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    // Should match anonymously (same rocksalt prototype)
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(
        matcher.fit_anonymous(&s1, &s2, None),
        "fit_anonymous should ignore oxidation states and match NaCl with MgO"
    );
}

#[test]
fn test_fit_anonymous_predefined_metal_nonmetal() {
    let nacl = make_nacl();
    let mgo = Structure::new(
        Lattice::cubic(4.21),
        vec![Species::neutral(Element::Mg), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(matcher.fit_anonymous(
        &nacl,
        &mgo,
        Some(AnonymousMatchMode::Predefined(
            AnonymousClassMapping::MetalNonMetal,
        ))
    ));
}

#[test]
fn test_fit_anonymous_mapped_custom_classes() {
    let first_structure = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::Ca),
            Species::neutral(Element::Al),
            Species::neutral(Element::Cl),
            Species::neutral(Element::Cl),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.25, 0.25, 0.25),
            Vector3::new(0.75, 0.75, 0.75),
        ],
    );
    let second_structure = Structure::new(
        Lattice::cubic(5.2),
        vec![
            Species::neutral(Element::Li),
            Species::neutral(Element::Li),
            Species::neutral(Element::Br),
            Species::neutral(Element::Br),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.25, 0.25, 0.25),
            Vector3::new(0.75, 0.75, 0.75),
        ],
    );

    let class_mapping = HashMap::from([
        (Element::Ca, "C".to_string()),
        (Element::Al, "C".to_string()),
        (Element::Cl, "X".to_string()),
        (Element::Li, "C".to_string()),
        (Element::Br, "X".to_string()),
    ]);
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(
        !matcher.fit_anonymous(&first_structure, &second_structure, None),
        "Element-permutation mode should fail for 3 elements vs 2 elements",
    );
    assert!(matcher.fit_anonymous(
        &first_structure,
        &second_structure,
        Some(AnonymousMatchMode::Custom(&class_mapping)),
    ));
}

#[test]
fn test_fit_anonymous_mapped_fails_when_element_unmapped() {
    let class_mapping = HashMap::from([(Element::Na, "C".to_string())]);
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(!matcher.fit_anonymous(
        &make_nacl(),
        &make_nacl(),
        Some(AnonymousMatchMode::Custom(&class_mapping)),
    ));
}

#[test]
fn test_get_structure_distance_anonymous_mapped_returns_none_for_unmapped() {
    let class_mapping = HashMap::from([(Element::Na, "C".to_string())]);
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(
        matcher
            .get_structure_distance_anonymous_mapped(&make_nacl(), &make_nacl(), &class_mapping)
            .is_none()
    );
}

#[test]
fn test_fit_anonymous_explicit_element_permutation_mode_matches_default() {
    let nacl = make_nacl();
    let mgo = Structure::new(
        Lattice::cubic(4.21),
        vec![Species::neutral(Element::Mg), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    let default_result = matcher.fit_anonymous(&nacl, &mgo, None);
    let explicit_mode_result =
        matcher.fit_anonymous(&nacl, &mgo, Some(AnonymousMatchMode::ElementPermutation));
    assert_eq!(default_result, explicit_mode_result);
    assert!(default_result);
}

#[test]
fn test_anonymous_class_mapping_from_name_aliases() {
    assert_eq!(
        AnonymousClassMapping::from_name("ACX"),
        Some(AnonymousClassMapping::Acx)
    );
    assert_eq!(
        AnonymousClassMapping::from_name("cea"),
        Some(AnonymousClassMapping::Cea)
    );
    assert_eq!(
        AnonymousClassMapping::from_name("metal/non-metal"),
        Some(AnonymousClassMapping::MetalNonMetal)
    );
    assert_eq!(
        AnonymousClassMapping::from_name("metal_nonmetal"),
        Some(AnonymousClassMapping::MetalNonMetal)
    );
    assert_eq!(
        AnonymousClassMapping::from_name("metal_non_metal"),
        Some(AnonymousClassMapping::MetalNonMetal)
    );
    assert_eq!(AnonymousClassMapping::from_name("unknown"), None);
}

#[test]
fn test_fit_anonymous_predefined_acx_fails_for_uncovered_elements() {
    let fe = make_simple_cubic(Element::Fe, 4.0);
    let cu = make_simple_cubic(Element::Cu, 4.0);
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(!matcher.fit_anonymous(
        &fe,
        &cu,
        Some(AnonymousMatchMode::Predefined(AnonymousClassMapping::Acx)),
    ));
}

#[test]
fn test_fit_anonymous_predefined_metal_nonmetal_covers_isotopes() {
    let h2o = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::H),
            Species::neutral(Element::H),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.25, 0.25, 0.25),
        ],
    );
    let d2o = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::D),
            Species::neutral(Element::D),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.25, 0.25, 0.25),
        ],
    );
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    assert!(matcher.fit_anonymous(
        &h2o,
        &d2o,
        Some(AnonymousMatchMode::Predefined(
            AnonymousClassMapping::MetalNonMetal,
        )),
    ));
}

// =========================================================================
// Pymatgen Edge Case Tests (ported from pymatgen test suite)
// =========================================================================

#[test]
fn test_matching_edge_cases() {
    let matcher = StructureMatcher::new().with_primitive_cell(false);

    // Out-of-cell sites: 0.98 ≈ -0.02 (wrapped)
    let s1 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.98, 0.0, 0.0)],
    );
    let s2 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(-0.02, 0.0, 0.0)],
    );
    assert!(matcher.fit(&s1, &s2), "Wrapped coords should match");

    // Site shuffling: order shouldn't matter
    let s3 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::O)],
        vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
    );
    let s4 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::O), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.5, 0.5, 0.5), Vector3::zeros()],
    );
    assert!(matcher.fit(&s3, &s4), "Site order shouldn't matter");

    // Large translation should fail
    let s5 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
    );
    let s6 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::zeros(), Vector3::new(0.9, 0.9, 0.7)],
    );
    assert!(
        !matcher.with_site_pos_tol(0.3).fit(&s5, &s6),
        "Large shift should fail"
    );
}

#[test]
fn test_scaling_and_comparators() {
    // scale=false is more restrictive
    let s1 = make_simple_cubic(Element::Fe, 4.0);
    let s2 = make_simple_cubic(Element::Fe, 4.5);
    let fit_scale = StructureMatcher::new().fit(&s1, &s2);
    let fit_no_scale = StructureMatcher::new().with_scale(false).fit(&s1, &s2);
    assert!(!fit_no_scale || fit_scale, "no_scale more restrictive");

    // Element comparator ignores oxidation states
    let s3 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::new(Element::Fe, Some(2))],
        vec![Vector3::zeros()],
    );
    let s4 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::new(Element::Fe, Some(3))],
        vec![Vector3::zeros()],
    );
    let m_species = StructureMatcher::new().with_primitive_cell(false);
    let m_elem = m_species.clone().with_comparator(ComparatorType::Element);
    assert!(
        !m_species.fit(&s3, &s4),
        "Species comparator rejects diff oxi"
    );
    assert!(m_elem.fit(&s3, &s4), "Element comparator accepts same elem");
}

#[test]
fn test_supercell_matching() {
    let s1 = make_simple_cubic(Element::Fe, 4.0);
    let coords: Vec<_> = (0..8)
        .map(|i| {
            Vector3::new(
                (i & 1) as f64 * 0.5,
                ((i >> 1) & 1) as f64 * 0.5,
                ((i >> 2) & 1) as f64 * 0.5,
            )
        })
        .collect();
    let s2 = Structure::new(
        Lattice::cubic(8.0),
        vec![Species::neutral(Element::Fe); 8],
        coords,
    );

    assert!(
        !StructureMatcher::new()
            .with_primitive_cell(false)
            .fit(&s1, &s2)
    );
    assert!(
        StructureMatcher::new()
            .with_primitive_cell(true)
            .fit(&s1, &s2)
    );
}

#[test]
fn test_attempt_supercell_matches_in_core_paths() {
    let primitive = make_simple_cubic(Element::Fe, 4.0);
    let supercell_coords: Vec<_> = (0..8)
        .map(|idx| {
            Vector3::new(
                (idx & 1) as f64 * 0.5,
                ((idx >> 1) & 1) as f64 * 0.5,
                ((idx >> 2) & 1) as f64 * 0.5,
            )
        })
        .collect();
    let supercell = Structure::new(
        Lattice::cubic(8.0),
        vec![Species::neutral(Element::Fe); 8],
        supercell_coords,
    );

    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_attempt_supercell(true);

    assert!(
        matcher.fit(&primitive, &supercell),
        "attempt_supercell should match primitive and supercell in fit() path"
    );

    let reduced_primitive = matcher.reduce_structure(&primitive);
    let reduced_supercell = matcher.reduce_structure(&supercell);
    assert!(
        matcher.fit_preprocessed(&reduced_primitive, &reduced_supercell),
        "attempt_supercell should match primitive and supercell in fit_preprocessed() path"
    );
}

#[test]
fn test_attempt_supercell_matches_nondiagonal_supercell() {
    let primitive = make_simple_cubic(Element::Fe, 4.0);
    let nondiagonal_supercell = primitive
        .make_supercell([[2, 1, 0], [0, 2, 0], [0, 0, 1]])
        .unwrap();
    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_attempt_supercell(true);

    assert!(
        matcher.fit(&primitive, &nondiagonal_supercell),
        "attempt_supercell should match non-diagonal supercells"
    );
}

#[test]
fn test_attempt_supercell_matches_factor_above_ten() {
    let primitive = make_simple_cubic(Element::Fe, 4.0);
    let larger_supercell = primitive.make_supercell_diag([11, 1, 1]);
    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_attempt_supercell(true);

    assert!(
        matcher.fit(&primitive, &larger_supercell),
        "attempt_supercell should match valid supercells even when factor > 10"
    );
}

#[test]
fn test_attempt_supercell_is_symmetric_for_large_factor() {
    let primitive = make_simple_cubic(Element::Fe, 4.0);
    let larger_supercell = primitive.make_supercell_diag([11, 1, 1]);
    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_attempt_supercell(true);

    assert!(matcher.fit(&primitive, &larger_supercell));
    assert!(matcher.fit(&larger_supercell, &primitive));
}

#[test]
fn test_attempt_supercell_rejects_non_integer_site_ratio() {
    let two_site_structure = make_bcc(Element::Fe, 2.87);
    let three_site_structure = Structure::new(
        Lattice::cubic(4.0),
        vec![
            Species::neutral(Element::Fe),
            Species::neutral(Element::Fe),
            Species::neutral(Element::Fe),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.0),
            Vector3::new(0.5, 0.0, 0.5),
        ],
    );
    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_attempt_supercell(true);

    assert!(!matcher.fit(&two_site_structure, &three_site_structure));
}

#[test]
fn test_fit_preprocessed_rejects_non_integer_site_ratio() {
    let two_site_structure = make_bcc(Element::Fe, 2.87);
    let three_site_structure = Structure::new(
        Lattice::cubic(4.0),
        vec![
            Species::neutral(Element::Fe),
            Species::neutral(Element::Fe),
            Species::neutral(Element::Fe),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.0),
            Vector3::new(0.5, 0.0, 0.5),
        ],
    );
    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_attempt_supercell(true);
    let reduced_two_site = matcher.reduce_structure(&two_site_structure);
    let reduced_three_site = matcher.reduce_structure(&three_site_structure);

    assert!(!matcher.fit_preprocessed(&reduced_two_site, &reduced_three_site));
}

#[test]
fn test_rms_distance() {
    let s = make_simple_cubic(Element::Fe, 4.0);
    let matcher = StructureMatcher::new().with_primitive_cell(false);
    // Identical → RMS ≈ 0
    if let Some((rms, _)) = matcher.get_rms_dist(&s, &s) {
        assert!(rms < 1e-10);
    }
    // Small perturbation → small RMS
    let s2 = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.01, 0.0, 0.0)],
    );
    if let Some((rms, _)) = matcher.with_site_pos_tol(0.5).get_rms_dist(&s, &s2) {
        assert!(rms < 0.1);
    }
}

#[test]
fn test_composition_hash_respects_comparator_type() {
    // Create two structures: same elements, different oxidation states
    let fe2 = Species::new(Element::Fe, Some(2));
    let fe3 = Species::new(Element::Fe, Some(3));
    let o2 = Species::new(Element::O, Some(-2));

    // FeO with Fe2+
    let s1 = Structure::new(
        Lattice::cubic(4.0),
        vec![fe2, o2],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    // FeO with Fe3+
    let s2 = Structure::new(
        Lattice::cubic(4.0),
        vec![fe3, o2],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    // Element comparator: same hash (oxidation states ignored)
    let elem_matcher = StructureMatcher::new().with_comparator(ComparatorType::Element);
    assert_eq!(
        elem_matcher.composition_hash(&s1),
        elem_matcher.composition_hash(&s2),
        "Element comparator should give same hash for same elements"
    );

    // Species comparator: different hash (oxidation states matter)
    let species_matcher = StructureMatcher::new().with_comparator(ComparatorType::Species);
    assert_ne!(
        species_matcher.composition_hash(&s1),
        species_matcher.composition_hash(&s2),
        "Species comparator should give different hash for different oxidation states"
    );
}

// =========================================================================
// get_structure_distance() tests
// =========================================================================

#[test]
fn test_structure_distance_basic_properties() {
    // Tests: identical=0, symmetry, ranking (identical < shifted)
    // Disable primitive_cell since moyo standardizes NaCl to canonical Wyckoff
    // positions, erasing the rigid-body shift and producing distance=0
    let s1 = make_nacl();
    let s2 = make_nacl_shifted();
    let matcher = StructureMatcher::new().with_primitive_cell(false);

    let d_self = matcher.get_structure_distance(&s1, &s1);
    let d12 = matcher.get_structure_distance(&s1, &s2);
    let d21 = matcher.get_structure_distance(&s2, &s1);

    assert!(d_self < 1e-10, "d(s,s) should be ~0, got {d_self}");
    assert!(
        (d12 - d21).abs() < 1e-10,
        "Should be symmetric: {d12} vs {d21}"
    );
    assert!(
        d_self < d12,
        "Identical ({d_self}) should be < shifted ({d12})"
    );
    assert!(
        d12 < 1.0,
        "Similar structures should have small distance: {d12}"
    );
}

#[test]
fn test_structure_distance_composition() {
    // Different compositions should return finite distance, larger than same composition
    let nacl = make_nacl();
    let fe = make_simple_cubic(Element::Fe, 4.0);
    let cuo = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Cu), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    // NaBr with SAME geometry as NaCl (tests composition_weight in isolation)
    let nabr_same_geom = Structure::new(
        Lattice::cubic(5.64), // Same as NaCl
        vec![Species::neutral(Element::Na), Species::neutral(Element::Br)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let matcher = StructureMatcher::new();

    let d_same = matcher.get_structure_distance(&nacl, &nacl);
    let d_disjoint = matcher.get_structure_distance(&nacl, &cuo);
    let d_partial = matcher.get_structure_distance(&nacl, &nabr_same_geom);
    let d_no_overlap = matcher.get_structure_distance(&nacl, &fe);

    assert!(d_disjoint.is_finite() && d_disjoint > d_same);
    assert!(d_no_overlap.is_finite() && d_no_overlap > 0.0);
    // Same geometry but partial overlap: composition_distance = 1 - 1/3 ≈ 0.667
    // With COMPOSITION_WEIGHT = 5.0, expected contribution ≈ 3.33
    // Geometric distance is small but non-zero (~2.2) due to normalization
    assert!(
        d_partial > 3.0,
        "Same geometry + partial overlap should have composition penalty: {d_partial}"
    );
    // Partial should be less than disjoint (DISJOINT_COMPOSITION_DISTANCE = 1e9)
    assert!(
        d_partial < d_disjoint,
        "Partial ({d_partial}) < disjoint ({d_disjoint})"
    );
}

#[test]
fn test_structure_distance_empty() {
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    let non_empty = make_simple_cubic(Element::Fe, 4.0);
    let matcher = StructureMatcher::new();

    assert!(matcher.get_structure_distance(&empty, &empty) < 1e-10);
    let d = matcher.get_structure_distance(&empty, &non_empty);
    assert!((d - EMPTY_STRUCTURE_DISTANCE).abs() < 1e-10, "Got {d}");
}

#[test]
fn test_structure_distance_on_error_fail_returns_finite_for_degenerate_structures() {
    let degenerate = make_degenerate_lattice_structure(Element::Fe);
    let matcher_fail = StructureMatcher::new()
        .with_primitive_cell(true)
        .with_on_error(crate::error::OnError::Fail);
    let matcher_skip = StructureMatcher::new()
        .with_primitive_cell(true)
        .with_on_error(crate::error::OnError::Skip);

    let result =
        std::panic::catch_unwind(|| matcher_fail.get_structure_distance(&degenerate, &degenerate));
    assert!(
        result.is_ok(),
        "get_structure_distance should not panic even when on_error=Fail"
    );
    let distance = result.unwrap();
    let distance_skip = matcher_skip.get_structure_distance(&degenerate, &degenerate);
    assert!(
        distance.is_finite(),
        "distance should be finite, got {distance}"
    );
    assert!(
        (distance - distance_skip).abs() < 1e-10,
        "on_error policy should not affect get_structure_distance: fail={distance}, skip={distance_skip}"
    );
}

#[test]
fn test_structure_distance_pbc_wrapping() {
    // Atom at (0.95,0.95,0.95) should be CLOSER to origin than (0.3,0.3,0.3) via PBC
    let lattice = Lattice::cubic(4.0);
    let at_origin = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let near_corner = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.95, 0.95, 0.95)],
    );
    let at_030 = Structure::new(
        lattice,
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.3, 0.3, 0.3)],
    );
    let matcher = StructureMatcher::new();

    let d_corner = matcher.get_structure_distance(&at_origin, &near_corner);
    let d_030 = matcher.get_structure_distance(&at_origin, &at_030);

    assert!(
        d_corner < d_030,
        "PBC failed: {d_corner} should be < {d_030}"
    );
}

#[test]
fn test_structure_distance_hexagonal_pbc() {
    // Non-orthogonal lattice (hexagonal, gamma=120°) - PBC must work correctly
    let a = 3.0;
    let hex = Matrix3::new(
        a,
        0.0,
        0.0,
        -a / 2.0,
        a * 3.0_f64.sqrt() / 2.0,
        0.0,
        0.0,
        0.0,
        5.0,
    );
    let species = vec![Species::neutral(Element::Mg), Species::neutral(Element::O)];
    let o_pos = Vector3::new(0.333, 0.667, 0.5);

    let hex_origin = Structure::new(
        Lattice::new(hex),
        species.clone(),
        vec![Vector3::new(0.0, 0.0, 0.0), o_pos],
    );
    let hex_boundary = Structure::new(
        Lattice::new(hex),
        species,
        vec![Vector3::new(0.95, 0.0, 0.0), o_pos], // Near periodic boundary
    );
    let matcher = StructureMatcher::new();

    // Identical should be 0
    assert!(matcher.get_structure_distance(&hex_origin, &hex_origin) < 1e-10);

    // Boundary atom should wrap to be close (fractional 0.95 wraps to -0.05)
    let d = matcher.get_structure_distance(&hex_origin, &hex_boundary);
    assert!(d < 1.0, "Hexagonal PBC failed: {d} should be < 1.0");

    // Symmetry must hold
    let d_rev = matcher.get_structure_distance(&hex_boundary, &hex_origin);
    assert!((d - d_rev).abs() < 1e-10, "Asymmetric: {d} vs {d_rev}");
}

#[test]
fn test_structure_distance_symmetry_various_cases() {
    // Tests d(A,B) = d(B,A) across: equal sizes, unequal sizes, different lattice shapes
    let matcher = StructureMatcher::new();

    // Case 1: Different lattice shapes (cubic vs tetragonal)
    let cubic = make_simple_cubic(Element::Fe, 4.0);
    let tetragonal = Structure::new(
        Lattice::new(Matrix3::new(4.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 6.0)),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );

    // Case 2: Unequal sizes (1 vs 3 sites, same lattice)
    let large = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe); 3],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.0, 0.0),
            Vector3::new(0.0, 0.5, 0.0),
        ],
    );

    // Case 3: Different lattices + unequal sizes (most rigorous)
    let hex_large = Structure::new(
        Lattice::new(Matrix3::new(4.0, 0.0, 0.0, -2.0, 3.464, 0.0, 0.0, 0.0, 6.0)),
        vec![Species::neutral(Element::Fe); 2],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.333, 0.667, 0.5)],
    );

    for (name, s1, s2) in [
        ("cubic-tetragonal", &cubic, &tetragonal),
        ("equal-unequal", &cubic, &large),
        ("cubic-hexagonal", &cubic, &hex_large),
    ] {
        let d12 = matcher.get_structure_distance(s1, s2);
        let d21 = matcher.get_structure_distance(s2, s1);
        assert!(d12.is_finite() && d12 >= 0.0, "{name}: non-negative");
        assert!((d12 - d21).abs() < 1e-10, "{name}: {d12} != {d21}");
    }
}

#[test]
fn test_structure_distance_different_lattices_same_frac_coords() {
    // Regression test: structures with identical fractional coordinates but different
    // lattice shapes should NOT have zero geometric distance.
    // Before the fix, subtracting fractional coords directly gave zero distance
    // because frac_diff = (0,0,0) - (0,0,0) = (0,0,0) regardless of lattice shape.
    let matcher = StructureMatcher::new();

    // Same fractional coords (0,0,0) but different lattices
    let cubic = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let tetragonal = Structure::new(
        Lattice::new(Matrix3::new(4.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 8.0)), // c = 2a
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );

    // Both have atom at origin -> same Cartesian position -> distance should be ~0
    let d_origin = matcher.get_structure_distance(&cubic, &tetragonal);
    assert!(
        d_origin < 0.1,
        "Origin atoms should have small distance: {d_origin}"
    );

    // Now test with atom at (0.5, 0.5, 0.5) in each
    // Cubic: Cartesian = (2, 2, 2)
    // Tetragonal: Cartesian = (2, 2, 4) - different!
    let cubic_center = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.5, 0.5, 0.5)],
    );
    let tetragonal_center = Structure::new(
        Lattice::new(Matrix3::new(4.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 8.0)),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.5, 0.5, 0.5)],
    );

    let d_center = matcher.get_structure_distance(&cubic_center, &tetragonal_center);
    // Cartesian diff = (0, 0, 2) Å between the two center positions.
    // After PBC wrapping and normalization, expect meaningful non-zero distance.
    // Before the fix, subtracting frac coords directly gave ~0 distance.
    assert!(
        d_center > 0.1,
        "Same frac coords in different lattices should have non-zero distance: {d_center}"
    );

    // Verify symmetry holds
    let d_center_rev = matcher.get_structure_distance(&tetragonal_center, &cubic_center);
    assert!(
        (d_center - d_center_rev).abs() < 1e-10,
        "Distance should be symmetric: {d_center} vs {d_center_rev}"
    );
}

// =========================================================================
// pymatgen-compatible Oxidation State Tests
// =========================================================================

#[test]
fn test_oxi_state_matching_pymatgen_compatible() {
    // Matches pymatgen test_oxi: same structure with different oxidation states
    // Species comparator should NOT match, Element comparator SHOULD match

    // Li2O antifluorite: Li at (1/4, 1/4, 1/4) etc., O at (0,0,0)
    let lattice = Lattice::cubic(4.619);
    let coords = vec![
        Vector3::new(0.25, 0.25, 0.25),
        Vector3::new(0.75, 0.75, 0.75),
        Vector3::new(0.0, 0.0, 0.0),
    ];

    let li2o_neutral = Structure::new(
        lattice.clone(),
        vec![
            Species::neutral(Element::Li),
            Species::neutral(Element::Li),
            Species::neutral(Element::O),
        ],
        coords.clone(),
    );
    let li2o_charged = Structure::new(
        lattice,
        vec![
            Species::new(Element::Li, Some(1)),
            Species::new(Element::Li, Some(1)),
            Species::new(Element::O, Some(-2)),
        ],
        coords,
    );

    // Species comparator: should NOT match (different oxidation states)
    let species_matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_comparator(ComparatorType::Species);
    assert!(
        !species_matcher.fit(&li2o_neutral, &li2o_charged),
        "Species comparator should reject different oxidation states"
    );

    // Element comparator: SHOULD match (same elements, ignores oxidation states)
    let element_matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_comparator(ComparatorType::Element);
    assert!(
        element_matcher.fit(&li2o_neutral, &li2o_charged),
        "Element comparator should match same elements regardless of oxidation state"
    );
}

#[test]
fn test_primitive_cell_supercell_matching_pymatgen() {
    // Matches pymatgen test_primitive: primitive cell should match its supercell
    let primitive = make_simple_cubic(Element::Fe, 4.0);

    // Create a 2x2x2 supercell using itertools-style iteration
    let (supercell_species, supercell_coords): (Vec<_>, Vec<_>) = (0..8)
        .map(|idx| {
            let (idx_x, idx_y, idx_z) = (idx / 4, (idx / 2) % 2, idx % 2);
            (
                Species::neutral(Element::Fe),
                Vector3::new(idx_x as f64 * 0.5, idx_y as f64 * 0.5, idx_z as f64 * 0.5),
            )
        })
        .unzip();
    let supercell = Structure::new(Lattice::cubic(8.0), supercell_species, supercell_coords);

    // Without primitive cell reduction, they shouldn't match
    let no_prim = StructureMatcher::new().with_primitive_cell(false);
    assert!(
        !no_prim.fit(&primitive, &supercell),
        "Without primitive_cell, different sizes shouldn't match directly"
    );

    // With primitive cell reduction, they should match
    let with_prim = StructureMatcher::new().with_primitive_cell(true);
    assert!(
        with_prim.fit(&primitive, &supercell),
        "With primitive_cell, supercell should reduce to match primitive"
    );
}

#[test]
fn test_species_comparator_default_primitive_cell_keeps_oxidation_semantics() {
    let lattice = Lattice::cubic(4.0);
    let s_fe2 = Structure::new(
        lattice.clone(),
        vec![Species::new(Element::Fe, Some(2))],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let s_fe3 = Structure::new(
        lattice,
        vec![Species::new(Element::Fe, Some(3))],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );

    let matcher = StructureMatcher::new().with_comparator(ComparatorType::Species);
    assert!(
        !matcher.fit(&s_fe2, &s_fe3),
        "Species comparator must reject different oxidation states even with primitive_cell=true"
    );
}

#[test]
fn test_non_periodic_matching_does_not_wrap_coordinates() {
    let mut non_periodic_lattice = Lattice::cubic(4.0);
    non_periodic_lattice.pbc = [false, false, false];

    let site_origin = Structure::new(
        non_periodic_lattice.clone(),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let site_shifted = Structure::new(
        non_periodic_lattice,
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(1.0, 0.0, 0.0)],
    );
    assert!((site_origin.frac_coords[0].x - 0.0).abs() < 1e-12);
    assert!((site_shifted.frac_coords[0].x - 1.0).abs() < 1e-12);

    let matcher = StructureMatcher::new()
        .with_primitive_cell(false)
        .with_site_pos_tol(1e-3);
    assert!(
        !matcher.fit(&site_origin, &site_shifted),
        "Non-periodic matching should not wrap coordinates across unit boundaries"
    );
}

#[test]
fn test_primitive_reduction_preserves_non_periodic_pbc() {
    let mut non_periodic_lattice = Lattice::cubic(4.0);
    non_periodic_lattice.pbc = [false, false, false];

    let site_origin = Structure::new(
        non_periodic_lattice.clone(),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let site_shifted = Structure::new(
        non_periodic_lattice,
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(1.0, 0.0, 0.0)],
    );

    let matcher = StructureMatcher::new()
        .with_primitive_cell(true)
        .with_site_pos_tol(1e-3);
    let reduced_origin = matcher.reduce_structure(&site_origin);
    assert_eq!(reduced_origin.lattice.pbc, [false, false, false]);
    assert!(
        !matcher.fit(&site_origin, &site_shifted),
        "primitive reduction must preserve non-periodic PBC semantics"
    );
}

/// Single-atom structure at given fractional position.
fn atom_at(latt: Lattice, elem: Element, frac: Vector3<f64>) -> Structure {
    Structure::new(latt, vec![Species::neutral(elem)], vec![frac])
}

#[test]
fn test_structure_distance_respects_non_periodic_pbc() {
    // Frac coords 0.0 and 0.9 in 10 Å cell: periodic wraps (1 Å), non-periodic doesn't (9 Å)
    let periodic_latt = Lattice::cubic(10.0);
    let mut non_periodic_latt = Lattice::cubic(10.0);
    non_periodic_latt.pbc = [false, false, false];
    let origin = Vector3::new(0.0, 0.0, 0.0);
    let shifted = Vector3::new(0.9, 0.0, 0.0);

    let matcher = StructureMatcher::new().with_primitive_cell(false);
    let dist_periodic = matcher.get_structure_distance(
        &atom_at(periodic_latt.clone(), Element::Fe, origin),
        &atom_at(periodic_latt, Element::Fe, shifted),
    );
    let dist_non_periodic = matcher.get_structure_distance(
        &atom_at(non_periodic_latt.clone(), Element::Fe, origin),
        &atom_at(non_periodic_latt, Element::Fe, shifted),
    );

    assert!(
        dist_non_periodic > dist_periodic * 3.0,
        "Non-periodic distance ({dist_non_periodic:.4}) should be much larger than \
         periodic distance ({dist_periodic:.4}) — wrapping must be disabled for pbc=false"
    );
}

#[test]
fn test_structure_distance_mixed_pbc_per_axis() {
    // Periodic in x only: x-shift wraps (small), y-shift doesn't (large)
    let mut latt = Lattice::cubic(10.0);
    latt.pbc = [true, false, false];
    let origin = Vector3::new(0.0, 0.0, 0.0);

    let matcher = StructureMatcher::new().with_primitive_cell(false);
    let base = atom_at(latt.clone(), Element::Cu, origin);
    let dist_x = matcher.get_structure_distance(
        &base,
        &atom_at(latt.clone(), Element::Cu, Vector3::new(0.9, 0.0, 0.0)),
    );
    let dist_y = matcher.get_structure_distance(
        &base,
        &atom_at(latt, Element::Cu, Vector3::new(0.0, 0.9, 0.0)),
    );

    assert!(
        dist_y > dist_x * 3.0,
        "Non-periodic y distance ({dist_y:.4}) should be much larger than \
         periodic x distance ({dist_x:.4})"
    );
}

#[test]
fn test_structure_distance_asymmetric_pbc_is_order_independent() {
    // s1 is periodic, s2 is non-periodic. The distance must be the same
    // regardless of argument order so the source/target swap uses the
    // correct structure's PBC for wrapping.
    let mut periodic_latt = Lattice::cubic(10.0);
    periodic_latt.pbc = [true, true, true];
    let mut non_periodic_latt = Lattice::cubic(10.0);
    non_periodic_latt.pbc = [false, false, false];

    let shifted = Vector3::new(0.9, 0.0, 0.0);
    let origin = Vector3::new(0.0, 0.0, 0.0);

    let pbc_struct = Structure::new(
        periodic_latt,
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![origin, shifted],
    );
    let nopbc_struct = Structure::new(
        non_periodic_latt,
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![origin, shifted],
    );

    let matcher = StructureMatcher::new().with_primitive_cell(false);
    let dist_ab = matcher.get_structure_distance(&pbc_struct, &nopbc_struct);
    let dist_ba = matcher.get_structure_distance(&nopbc_struct, &pbc_struct);

    assert!(
        (dist_ab - dist_ba).abs() < 1e-10,
        "Distance must be order-independent: d(A,B)={dist_ab:.6} vs d(B,A)={dist_ba:.6}"
    );
}

#[test]
fn test_anonymous_matching_different_stoichiometry() {
    // Anonymous matching should fail for different stoichiometries
    let matcher = StructureMatcher::new().with_primitive_cell(false);

    // AB structure (FeO-like)
    let ab = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    // A2B structure (Cu2S-like)
    let a2b = Structure::new(
        Lattice::cubic(4.0),
        vec![
            Species::neutral(Element::Cu),
            Species::neutral(Element::Cu),
            Species::neutral(Element::S),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
        ],
    );

    // AB2 structure (TiO2-like)
    let ab2 = Structure::new(
        Lattice::cubic(4.0),
        vec![
            Species::neutral(Element::Ti),
            Species::neutral(Element::O),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.25, 0.25, 0.0),
            Vector3::new(0.75, 0.75, 0.0),
        ],
    );

    // ABC structure (ternary)
    let abc = Structure::new(
        Lattice::cubic(4.0),
        vec![
            Species::neutral(Element::Li),
            Species::neutral(Element::Mn),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.25, 0.25, 0.25),
        ],
    );

    // Test all pairwise combinations of different stoichiometries
    let cases = [
        (&ab, &a2b, "AB vs A2B"),
        (&ab, &ab2, "AB vs AB2"),
        (&a2b, &ab2, "A2B vs AB2"),
        (&ab, &abc, "AB vs ABC"),
        (&a2b, &abc, "A2B vs ABC"),
    ];

    for (struct1, struct2, label) in cases {
        assert!(
            !matcher.fit_anonymous(struct1, struct2, None),
            "{label} should not match anonymously"
        );
    }
}
