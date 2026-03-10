use super::*;
use crate::element::Element;
use crate::species::Species;
use std::collections::HashMap;

// =========================================================================
// Basic Construction Tests
// =========================================================================

#[test]
fn test_composition_from_elements() {
    let comp = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);

    assert_eq!(comp.get(Element::Fe), 2.0);
    assert_eq!(comp.get(Element::O), 3.0);
    assert_eq!(comp.get(Element::H), 0.0); // missing element returns 0
    assert!((comp.num_atoms() - 5.0).abs() < AMOUNT_TOLERANCE);
    assert_eq!(comp.num_elements(), 2);
}

#[test]
fn test_composition_from_species() {
    let fe2 = Species::new(Element::Fe, Some(2));
    let fe3 = Species::new(Element::Fe, Some(3));
    let o2 = Species::new(Element::O, Some(-2));

    let comp = Composition::new([(fe2, 2.0), (fe3, 1.0), (o2, 4.0)]);

    assert_eq!(comp.get(fe2), 2.0);
    assert_eq!(comp.get(fe3), 1.0);
    assert_eq!(comp.get_element_total(Element::Fe), 3.0);
    assert_eq!(comp.num_species(), 3);
    assert_eq!(comp.num_elements(), 2); // Fe and O
}

#[test]
fn test_constructor_filters_zero_and_negative_amounts() {
    // new() filters zero, negative, and near-zero amounts (allow_negative=false)
    let fe = Species::neutral(Element::Fe);
    let comp = Composition::new([
        (fe, 2.0),                              // positive: kept
        (Species::neutral(Element::O), 0.0),    // zero: filtered
        (Species::neutral(Element::Na), -1.0),  // negative: filtered
        (Species::neutral(Element::Cl), 1e-12), // near-zero: filtered
    ]);
    assert_eq!(comp.num_species(), 1);
    assert_eq!(comp.get(fe), 2.0);
    assert!(comp.is_valid());

    // from_elements() delegates to new(), same behavior
    let comp2 = Composition::from_elements([(Element::Fe, 2.0), (Element::O, -3.0)]);
    assert_eq!(comp2.num_elements(), 1);
}

// =========================================================================
// Formula Parsing Tests
// =========================================================================

#[test]
fn test_from_formula() {
    // Simple formulas: (formula, expected_atoms, chemical_system)
    let simple_cases = [
        ("Fe2O3", 5.0, "Fe-O"),
        ("NaCl", 2.0, "Cl-Na"),
        ("H2O", 3.0, "H-O"),
        ("LiFePO4", 7.0, "Fe-Li-O-P"),
        ("Cu", 1.0, "Cu"),          // single element
        ("  Fe2O3  ", 5.0, "Fe-O"), // whitespace trimmed
        ("H1000", 1000.0, "H"),     // large multiplier
    ];
    for (formula, expected_atoms, expected_system) in simple_cases {
        let comp = Composition::from_formula(formula).unwrap();
        assert!(
            (comp.num_atoms() - expected_atoms).abs() < AMOUNT_TOLERANCE,
            "{formula}: expected {expected_atoms} atoms, got {}",
            comp.num_atoms()
        );
        assert_eq!(comp.chemical_system(), expected_system, "{formula}");
    }

    // Parentheses/brackets: (formula, element_amounts)
    let paren_cases: &[(&str, &[(Element, f64)])] = &[
        (
            "Ca3(PO4)2",
            &[(Element::Ca, 3.0), (Element::P, 2.0), (Element::O, 8.0)],
        ),
        (
            "Mg(OH)2",
            &[(Element::Mg, 1.0), (Element::O, 2.0), (Element::H, 2.0)],
        ),
        (
            "Al2(SO4)3",
            &[(Element::Al, 2.0), (Element::S, 3.0), (Element::O, 12.0)],
        ),
        (
            "[Cu(NH3)4]SO4",
            &[
                (Element::Cu, 1.0),
                (Element::N, 4.0),
                (Element::H, 12.0),
                (Element::S, 1.0),
                (Element::O, 4.0),
            ],
        ),
    ];
    for (formula, expected) in paren_cases {
        let comp = Composition::from_formula(formula).unwrap();
        for (elem, amt) in *expected {
            assert_eq!(comp.get(*elem), *amt, "{formula}: {elem:?}");
        }
    }

    // Error cases
    assert!(Composition::from_formula("").is_err(), "empty formula");
    assert!(
        Composition::from_formula("XxYy2").is_err(),
        "unknown element"
    );
    assert!(
        Composition::from_formula("(OH).").is_err(),
        "invalid multiplier '.'"
    );
    // Note: "(PO4)abc" parses as PO4 - trailing lowercase is silently ignored.
    // This matches pymatgen behavior where regex-based parsing skips non-matching text.
}

// =========================================================================
// Reduced Formula Tests
// =========================================================================

#[test]
fn test_reduced_formula() {
    // (elements, expected_reduced_formula)
    let cases: &[(&[(Element, f64)], &str)] = &[
        (&[(Element::Fe, 2.0), (Element::O, 3.0)], "Fe2O3"),
        (&[(Element::Na, 1.0), (Element::Cl, 1.0)], "NaCl"),
        (&[(Element::H, 2.0), (Element::O, 1.0)], "H2O"),
        (&[(Element::H, 4.0), (Element::O, 2.0)], "H2O"), // reduction
        (&[(Element::Fe, 4.0), (Element::O, 6.0)], "Fe2O3"), // reduction
        (&[(Element::Cu, 1.0)], "Cu"),                    // single
        (&[(Element::Cu, 4.0)], "Cu"),                    // single, any amount
        (&[(Element::Fe, 0.5), (Element::O, 0.75)], "Fe2O3"), // fractional
    ];
    for (elements, expected) in cases {
        let comp = Composition::from_elements(elements.iter().copied());
        assert_eq!(comp.reduced_formula(), *expected, "{:?}", elements);
    }
}

// =========================================================================
// Weight and Fraction Tests
// =========================================================================

#[test]
fn test_weight() {
    let comp = Composition::from_elements([(Element::H, 2.0), (Element::O, 1.0)]);
    // H2O: 2*1.008 + 1*15.999 ≈ 18.015
    let weight = comp.weight();
    assert!((weight - 18.015).abs() < 0.1, "H2O weight: {weight}");
}

#[test]
fn test_atomic_fraction() {
    let comp = Composition::from_elements([(Element::H, 2.0), (Element::O, 1.0)]);
    let h_frac = comp.get_atomic_fraction(Element::H);
    let o_frac = comp.get_atomic_fraction(Element::O);

    assert!((h_frac - 2.0 / 3.0).abs() < AMOUNT_TOLERANCE);
    assert!((o_frac - 1.0 / 3.0).abs() < AMOUNT_TOLERANCE);
}

#[test]
fn test_wt_fraction() {
    let comp = Composition::from_elements([(Element::H, 2.0), (Element::O, 1.0)]);
    let o_wt_frac = comp.get_wt_fraction(Element::O);
    // O contributes ~88.8% of H2O by mass
    assert!(
        (o_wt_frac - 0.888).abs() < 0.01,
        "O wt fraction: {o_wt_frac}"
    );
}

#[test]
fn test_fractional_composition() {
    let comp = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
    let frac = comp.fractional_composition();

    assert!((frac.num_atoms() - 1.0).abs() < AMOUNT_TOLERANCE);
    assert!((frac.get(Element::Fe) - 0.4).abs() < AMOUNT_TOLERANCE);
    assert!((frac.get(Element::O) - 0.6).abs() < AMOUNT_TOLERANCE);
}

// =========================================================================
// Arithmetic Tests
// =========================================================================

#[test]
fn test_arithmetic_operations() {
    let fe2o3 = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
    let feo = Composition::from_elements([(Element::Fe, 1.0), (Element::O, 1.0)]);
    let h2o = Composition::from_elements([(Element::H, 2.0), (Element::O, 1.0)]);

    // Add
    let sum = fe2o3.clone() + feo.clone();
    assert_eq!(sum.get(Element::Fe), 3.0);
    assert_eq!(sum.get(Element::O), 4.0);
    assert_eq!(sum.reduced_formula(), "Fe3O4");

    // Sub
    let diff = sum.clone() - feo;
    assert_eq!(diff.get(Element::Fe), 2.0);
    assert_eq!(diff.get(Element::O), 3.0);

    // Mul (both directions)
    let scaled = h2o.clone() * 3.0;
    assert_eq!(scaled.get(Element::H), 6.0);
    let scaled_rev = 3.0 * h2o;
    assert_eq!(scaled_rev.get(Element::H), 6.0);

    // Div
    let halved = sum / 2.0;
    assert_eq!(halved.get(Element::Fe), 1.5);
}

#[test]
fn test_subtraction_negative_handling() {
    let small = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
    let large = Composition::from_elements([(Element::Fe, 4.0), (Element::O, 6.0)]);
    let feo = Composition::from_elements([(Element::Fe, 1.0), (Element::O, 1.0)]);

    // Subtraction producing negatives: invalid unless allow_negative=true
    assert!(!(small.clone() - large.clone()).is_valid());
    assert!((small.clone().with_allow_negative(true) - large.clone()).is_valid());

    // sub_checked: error on negatives, ok otherwise
    assert!(small.sub_checked(&large).is_err());
    assert!(small.sub_checked(&feo).is_ok());

    // sub_checked enforces caller's policy (not RHS's) and result inherits it
    assert!(
        small
            .sub_checked(&large.clone().with_allow_negative(true))
            .is_err()
    );
    assert!(!small.sub_checked(&feo).unwrap().allow_negative);
}

#[test]
#[should_panic(expected = "Cannot divide Composition by zero")]
fn test_div_by_zero_panics() {
    let comp = Composition::from_elements([(Element::Fe, 2.0)]);
    let _ = comp / 0.0;
}

// =========================================================================
// Formula Variant Tests
// =========================================================================

#[test]
fn test_formula_variants() {
    // Hill formula: C first, H second (if C present), then alphabetical
    let hill_cases: &[(&[(Element, f64)], &str)] = &[
        (
            &[(Element::C, 6.0), (Element::H, 12.0), (Element::O, 6.0)],
            "C6 H12 O6",
        ), // glucose
        (
            &[(Element::C, 1.0), (Element::H, 1.0), (Element::F, 3.0)],
            "C H F3",
        ), // H before F (C present)
        (&[(Element::H, 1.0), (Element::F, 1.0)], "F H"), // F before H (no C)
        (
            &[(Element::O, 1.0), (Element::H, 2.0), (Element::N, 1.0)],
            "H2 N O",
        ), // no C, alphabetical
    ];
    for (elements, expected) in hill_cases {
        let comp = Composition::from_elements(elements.iter().copied());
        assert_eq!(comp.hill_formula(), *expected, "{:?}", elements);
    }

    // Alphabetical formula: purely alphabetical by symbol
    let comp = Composition::from_formula("LiFePO4").unwrap();
    assert_eq!(comp.alphabetical_formula(), "Fe Li O4 P");
}

// =========================================================================
// Comparison Tests
// =========================================================================

#[test]
fn test_equality_and_comparison() {
    let fe2o3 = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
    let fe4o6 = Composition::from_elements([(Element::Fe, 4.0), (Element::O, 6.0)]);
    let fe2o3_copy = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);

    // PartialEq compares exact species and amounts (scaling matters)
    assert_eq!(fe2o3, fe2o3_copy, "same species and amounts");
    assert_ne!(
        fe2o3, fe4o6,
        "different amounts, even if same reduced formula"
    );

    // formula_hash ignores scaling (groups by stoichiometry)
    assert_eq!(fe2o3.formula_hash(), fe4o6.formula_hash());

    // Oxidation states matter for equality
    let fe2_species = Species::new(Element::Fe, Some(2));
    let fe3_species = Species::new(Element::Fe, Some(3));
    let o2_species = Species::new(Element::O, Some(-2));

    let feo_with_fe2 = Composition::new([(fe2_species, 1.0), (o2_species, 1.0)]);
    let feo_with_fe3 = Composition::new([(fe3_species, 1.0), (o2_species, 1.0)]);
    assert_ne!(feo_with_fe2, feo_with_fe3, "different oxidation states");
    // But formula_hash ignores oxidation states
    assert_eq!(feo_with_fe2.formula_hash(), feo_with_fe3.formula_hash());

    // Mixed oxidation states: formulas aggregate by element
    let mixed = Composition::new([(fe2_species, 1.0), (fe3_species, 2.0), (o2_species, 4.0)]);
    assert_eq!(mixed.formula(), "Fe3 O4", "Fe²⁺ + 2×Fe³⁺ = Fe3");
    assert_eq!(mixed.reduced_formula(), "Fe3O4");
    // Same formula_hash as neutral Fe3O4
    let neutral_fe3o4 = Composition::from_elements([(Element::Fe, 3.0), (Element::O, 4.0)]);
    assert_eq!(mixed.formula_hash(), neutral_fe3o4.formula_hash());

    // almost_equals with tolerances
    let comp_approx = Composition::from_elements([(Element::Fe, 2.001), (Element::O, 2.999)]);
    assert!(fe2o3.almost_equals(&comp_approx, 0.01, 0.01));
    assert!(!fe2o3.almost_equals(&comp_approx, 0.0001, 0.0001));
}

// =========================================================================
// Property Tests
// =========================================================================

#[test]
fn test_element_properties() {
    let fe = Composition::from_elements([(Element::Fe, 1.0)]);
    let fe2o3 = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
    let h2o = Composition::from_elements([(Element::H, 2.0), (Element::O, 1.0)]);
    let nacl = Composition::from_elements([(Element::Na, 1.0), (Element::Cl, 1.0)]);

    // is_element
    assert!(fe.is_element());
    assert!(!fe2o3.is_element());

    // average_electroneg: Na(0.93) + Cl(3.16) / 2 ≈ 2.045
    let avg_en = nacl.average_electroneg().unwrap();
    assert!((avg_en - 2.045).abs() < 0.1, "NaCl avg EN: {avg_en}");

    // total_electrons: H(Z=1)*2 + O(Z=8)*1 = 10
    assert!((h2o.total_electrons() - 10.0).abs() < AMOUNT_TOLERANCE);
}

#[test]
fn test_remap_elements() {
    let nacl = Composition::from_elements([(Element::Na, 1.0), (Element::Cl, 1.0)]);
    let mapping = HashMap::from([(Element::Na, Element::K)]);
    let remapped = nacl.remap_elements(&mapping);

    assert_eq!(remapped.get(Element::K), 1.0);
    assert_eq!(remapped.get(Element::Cl), 1.0);
    assert_eq!(remapped.get(Element::Na), 0.0);
}

// =========================================================================
// Pymatgen Edge Case Tests (ported from pymatgen test suite)
// =========================================================================

#[test]
fn test_formula_parsing_edge_cases() {
    // Various formula edge cases in one test
    let cases: &[(&str, &[(Element, f64)])] = &[
        ("NaN", &[(Element::Na, 1.0), (Element::N, 1.0)]), // not float NaN
        (
            "Y3N@C80",
            &[(Element::Y, 3.0), (Element::N, 1.0), (Element::C, 80.0)],
        ), // metallofullerene
        ("{Fe2O3}2", &[(Element::Fe, 4.0), (Element::O, 6.0)]), // curly brackets
        // gh-3559: deeply nested formula
        (
            "Li3Fe2((PO4)3(CO3)5)2",
            &[
                (Element::Li, 3.0),
                (Element::Fe, 2.0),
                (Element::P, 6.0),
                (Element::C, 10.0),
                (Element::O, 54.0),
            ],
        ),
    ];
    for (formula, expected) in cases {
        let comp = Composition::from_formula(formula).expect(formula);
        for (elem, amt) in *expected {
            assert_eq!(comp.get(*elem), *amt, "{formula}: {elem:?}");
        }
    }

    // Square brackets with nested parentheses
    let comp = Composition::from_formula("[Cu(NH3)4]SO4").unwrap();
    assert_eq!(comp.get(Element::Cu), 1.0);
    assert_eq!(comp.get(Element::H), 12.0);

    // Fractional subscripts
    let frac = Composition::from_formula("Li1.5Si0.5").unwrap();
    assert!((frac.get(Element::Li) - 1.5).abs() < AMOUNT_TOLERANCE);

    // Invalid inputs should error
    for invalid in ["", "   ", "6123"] {
        assert!(Composition::from_formula(invalid).is_err(), "{invalid}");
    }
}

#[test]
fn test_reduced_formula_and_hash() {
    // Single element reduces to symbol
    assert_eq!(
        Composition::from_elements([(Element::O, 4.0)]).reduced_formula(),
        "O"
    );
    // Fe4O6 → Fe2O3
    assert_eq!(
        Composition::from_elements([(Element::Fe, 4.0), (Element::O, 6.0)]).reduced_formula(),
        "Fe2O3"
    );
    // Equal reduced formulas have equal hashes
    let comp1 = Composition::from_elements([(Element::Fe, 2.0), (Element::O, 3.0)]);
    let comp2 = Composition::from_elements([(Element::Fe, 4.0), (Element::O, 6.0)]);
    assert_eq!(comp1.formula_hash(), comp2.formula_hash());
    // Small fractions don't crash
    let frac = Composition::from_elements([(Element::Li, 1.0 / 6.0), (Element::B, 1.0)]);
    assert!(frac.num_atoms() > 0.0);
}

#[test]
fn test_composition_accessors() {
    // Missing element returns 0
    let comp = Composition::from_formula("NaCl").unwrap();
    assert_eq!(comp.get_atomic_fraction(Element::S), 0.0);
    assert_eq!(comp.get_wt_fraction(Element::S), 0.0);

    // Empty composition
    let empty = Composition::from_elements([]);
    assert!(empty.is_empty());
    assert_eq!(empty.formula(), "");
    assert!(empty.average_electroneg().is_none());
}

#[test]
fn test_hill_formula_ordering() {
    // Hill: C first, H second when C present, then alphabetical
    let comp = Composition::from_elements([
        (Element::Ga, 8.0),
        (Element::H, 102.0),
        (Element::C, 32.0),
        (Element::O, 3.0),
    ]);
    let hill = comp.hill_formula();
    assert!(hill.starts_with("C"), "Hill should start with C: {}", hill);
    let parts: Vec<&str> = hill.split_whitespace().collect();
    assert_eq!(parts[0], "C32");
    assert_eq!(parts[1], "H102");
}

// =========================================================================
// Oxidation State Tests
// =========================================================================

fn check_oxi(formula: &str, expected: &[(&str, f64)]) {
    let guesses = Composition::from_formula(formula)
        .unwrap()
        .oxi_state_guesses(0, None, false, None);
    assert!(!guesses.is_empty(), "{formula}");
    let best = &guesses[0];
    for (elem, oxi) in expected {
        let actual = *best.oxidation_states.get(*elem).unwrap();
        assert!(
            (actual - oxi).abs() < 0.01,
            "{formula}: {elem}={actual}, expected {oxi}"
        );
    }
}

#[test]
fn test_oxi_state_guesses() {
    check_oxi("NaCl", &[("Na", 1.0), ("Cl", -1.0)]);
    check_oxi("Fe2O3", &[("Fe", 3.0), ("O", -2.0)]);
}

#[test]
fn test_add_charges_from_oxi_state_guesses() {
    let charged = Composition::from_formula("NaCl")
        .unwrap()
        .add_charges_from_oxi_state_guesses(0, None, false, None)
        .unwrap();
    assert_eq!(charged.get(Species::new(Element::Na, Some(1))), 1.0);
    assert_eq!(charged.get(Species::new(Element::Cl, Some(-1))), 1.0);
}

#[test]
fn test_remove_charges() {
    let na = Species::new(Element::Na, Some(1));
    let cl = Species::new(Element::Cl, Some(-1));
    let neutral = Composition::new([(na, 1.0), (cl, 1.0)]).remove_charges();
    assert_eq!(neutral.get(Species::neutral(Element::Na)), 1.0);
    assert_eq!(neutral.get(Species::neutral(Element::Cl)), 1.0);
    assert_eq!(neutral.get(na), 0.0); // charged species gone
}

#[test]
fn test_charge_and_balance() {
    let na = Species::new(Element::Na, Some(1));
    let cl = Species::new(Element::Cl, Some(-1));
    let o = Species::new(Element::O, Some(-2));

    // No oxi states -> None
    assert!(
        Composition::from_formula("NaCl")
            .unwrap()
            .charge()
            .is_none()
    );
    // Balanced: Na+ + Cl- = 0
    assert_eq!(Composition::new([(na, 1.0), (cl, 1.0)]).charge(), Some(0));
    assert_eq!(
        Composition::new([(na, 1.0), (cl, 1.0)]).is_charge_balanced(),
        Some(true)
    );
    // Unbalanced: 2Na+ + Cl- = +1
    assert_eq!(Composition::new([(na, 2.0), (cl, 1.0)]).charge(), Some(1));
    // Na2O is balanced, NaO is not
    assert_eq!(
        Composition::new([(na, 2.0), (o, 1.0)]).is_charge_balanced(),
        Some(true)
    );
    assert_eq!(
        Composition::new([(na, 1.0), (o, 1.0)]).is_charge_balanced(),
        Some(false)
    );
}

// =========================================================================
// ANX Formula Tests
// =========================================================================

#[test]
fn test_anx_formula_oxi_path() {
    // Table of (species_with_amounts, expected_anx) via oxidation-state classification
    let na1 = Species::new(Element::Na, Some(1));
    let cl1 = Species::new(Element::Cl, Some(-1));
    let fe2 = Species::new(Element::Fe, Some(2));
    let fe3 = Species::new(Element::Fe, Some(3));
    let fe0 = Species::new(Element::Fe, Some(0));
    let o2 = Species::new(Element::O, Some(-2));

    #[allow(clippy::type_complexity)]
    let cases: Vec<(Vec<(Species, f64)>, Option<&str>)> = vec![
        (vec![(na1, 1.0), (cl1, 1.0)], Some("AX")),  // NaCl → AX
        (vec![(fe3, 2.0), (o2, 3.0)], Some("A2X3")), // Fe₂O₃ → A2X3
        (vec![(fe0, 1.0), (o2, 1.0)], Some("NX")),   // neutral Fe + O²⁻ → NX
        (vec![(fe2, 0.5), (o2, 0.5)], Some("AX")),   // partial occ, GCD=0.5
        (vec![(fe2, 0.4), (o2, 0.6)], Some("A2X3")), // partial occ, GCD=0.2
        (vec![(fe2, 0.5), (o2, 1.0)], Some("AX2")),  // fractional ratio → AX2
        (vec![(na1, 2.0), (cl1, 2.0)], Some("AX")),  // GCD reduction: 2:2 → 1:1
        (vec![(fe2, 1.0), (o2, std::f64::consts::SQRT_2)], None), // irrational ratio
    ];
    for (species_amts, expected) in &cases {
        let comp = Composition::new(species_amts.clone());
        assert_eq!(
            comp.anx_formula(),
            expected.map(ToString::to_string),
            "species: {species_amts:?}"
        );
    }
}

#[test]
fn test_anx_formula_en_path() {
    // Table of (formula_or_elements, expected_anx) via electronegativity classification
    let cases: Vec<(&str, Option<&str>)> = vec![
        ("NaCl", Some("AX")),   // binary, Na<Cl in EN
        ("Na2Cl2", Some("AX")), // GCD reduction via EN path
        ("Fe", None),           // single element → no EN classification
        ("FeCo", None),         // similar EN → None
    ];
    for (formula, expected) in &cases {
        assert_eq!(
            Composition::from_formula(formula).unwrap().anx_formula(),
            expected.map(ToString::to_string),
            "formula: {formula}"
        );
    }
    // Empty composition
    assert_eq!(Composition::from_elements([]).anx_formula(), None);
    // Noble gases (no EN data)
    assert_eq!(
        Composition::from_elements([(Element::He, 1.0), (Element::Ne, 1.0)]).anx_formula(),
        None
    );
    // Mixed: one element with EN, one without → None (not biased by 0.0 fallback)
    assert_eq!(
        Composition::from_elements([(Element::He, 1.0), (Element::Na, 1.0)]).anx_formula(),
        None
    );
}

#[test]
fn test_anx_formula_en_ternary() {
    // LiFePO4: Li=A (lowest EN), O=X (highest EN), Fe/P=N
    let anx = Composition::from_formula("LiFePO4")
        .unwrap()
        .anx_formula()
        .expect("LiFePO4 should produce an ANX label");
    assert!(anx.contains('A'), "should have A category: {anx}");
    assert!(anx.contains('X'), "should have X category: {anx}");
}

#[test]
fn test_anx_formula_tolerance_boundary() {
    // Clean integer ratios always produce ANX labels
    assert_eq!(
        Composition::from_formula("Fe2O3").unwrap().anx_formula(),
        Some("A2X3".to_string()),
    );
    // Irrational ratios like sqrt(2):1 can't round to integers, yielding None
    let irrational =
        Composition::from_elements([(Element::Fe, std::f64::consts::SQRT_2), (Element::O, 1.0)]);
    assert_eq!(irrational.anx_formula(), None);
}

#[test]
fn test_gcd_float() {
    let cases: &[(f64, f64, f64)] = &[
        (6.0, 4.0, 2.0),
        (0.5, 1.0, 0.5),
        (0.2, 0.6, 0.2),
        (0.0, 3.0, 3.0), // gcd(0, x) = x
        (5.0, 0.0, 5.0), // gcd(x, 0) = x
        (7.0, 7.0, 7.0), // identical
        (0.3, 0.3, 0.3),
    ];
    for &(left, right, expected) in cases {
        let result = super::gcd_float(left, right);
        assert!(
            (result - expected).abs() < 1e-8,
            "gcd_float({left}, {right}) = {result}, expected {expected}",
        );
    }
    // Irrational pair converges to near-zero (no rational GCD)
    assert!(super::gcd_float(std::f64::consts::SQRT_2, 1.0) < 1e-6);
}

#[test]
fn test_gcd_i64() {
    let cases: &[(i64, i64, i64)] = &[
        (12, 8, 4),
        (7, 13, 1), // coprime
        (-6, 4, 2), // negative handled
        (0, 5, 5),
    ];
    for &(left, right, expected) in cases {
        assert_eq!(
            super::gcd_i64(left, right),
            expected,
            "gcd_i64({left}, {right})"
        );
    }
}
