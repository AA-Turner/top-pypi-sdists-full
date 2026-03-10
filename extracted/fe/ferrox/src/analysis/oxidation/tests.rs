// === Tests ===

use super::composition_guess::combinations_with_replacement;
use super::defect_guess::{format_oxi_state, get_element_oxi_probs};
use super::*;
use crate::defects::DefectType;
use crate::element::Element;

#[test]
fn test_data_loading() {
    let oxi_prob = get_icsd_oxi_prob();
    assert!(!oxi_prob.is_empty() && oxi_prob.contains_key("Fe:3") && oxi_prob.contains_key("O:-2"));
    let bv_stats = get_icsd_bv_stats();
    assert!(!bv_stats.is_empty() && bv_stats.contains_key("Fe:3"));
    let bv_params = get_bv_params();
    assert!(!bv_params.is_empty() && bv_params.contains_key("Fe") && bv_params.contains_key("O"));
}

#[test]
fn test_species_key() {
    for (elem, oxi, expected) in [
        (Element::Fe, 3, "Fe:3"),
        (Element::O, -2, "O:-2"),
        (Element::Na, 1, "Na:1"),
    ] {
        assert_eq!(species_key(elem, oxi), expected);
    }
}

#[test]
fn test_is_electronegative() {
    assert!(
        [Element::O, Element::F, Element::Cl]
            .iter()
            .all(|&e| is_electronegative(e))
    );
    assert!(
        [Element::Na, Element::Fe, Element::Ca]
            .iter()
            .all(|&e| !is_electronegative(e))
    );
}

#[test]
fn test_calculate_bond_valence() {
    assert!(calculate_bond_valence(Element::Fe, Element::O, 2.0, 1.0) > 0.0); // Fe-O positive
    assert_eq!(
        calculate_bond_valence(Element::Fe, Element::Fe, 2.5, 1.0),
        0.0
    ); // same elem
    assert_eq!(
        calculate_bond_valence(Element::Na, Element::K, 3.0, 1.0),
        0.0
    ); // non-electroneg
}

#[test]
fn test_calculate_bv_sum() {
    // Fe with 6 O neighbors at 2.0 Å (octahedral) should give BVS ~3
    let neighbors = vec![
        BvNeighbor {
            element: Element::O,
            distance: 2.0,
            occupancy: 1.0
        };
        6
    ];
    let bvs = calculate_bv_sum(Element::Fe, &neighbors, 1.0);
    assert!((2.0..4.0).contains(&bvs), "Fe BVS={bvs}");
}

#[test]
fn test_get_oxi_probability() {
    assert!(get_oxi_probability(Element::Fe, 3).unwrap() > 0);
    assert!(get_oxi_probability(Element::O, -2).unwrap() > 10000);
    assert!(get_oxi_probability(Element::Fe, 10).is_none());
}

// Helper to verify oxidation state guesses
fn check_oxi_guess(name: &str, elements: &[Element], amounts: &[f64], expected: &[(&str, f64)]) {
    let guesses = oxi_state_guesses(elements, amounts, 0, None, false, None);
    assert!(!guesses.is_empty(), "{name}: should find solution");
    let best = &guesses[0];
    for (elem, oxi) in expected {
        let actual = *best.oxidation_states.get(*elem).unwrap();
        assert!(
            (actual - oxi).abs() < 0.01,
            "{name}: {elem} should be {oxi:+}, got {actual:+}"
        );
    }
}

#[test]
fn test_oxi_state_guesses_common_compounds() {
    check_oxi_guess(
        "NaCl",
        &[Element::Na, Element::Cl],
        &[1.0, 1.0],
        &[("Na", 1.0), ("Cl", -1.0)],
    );
    check_oxi_guess(
        "Fe2O3",
        &[Element::Fe, Element::O],
        &[2.0, 3.0],
        &[("Fe", 3.0), ("O", -2.0)],
    );
    check_oxi_guess("Fe (single)", &[Element::Fe], &[2.0], &[("Fe", 0.0)]);
}

#[test]
fn test_oxi_state_guesses_ternary() {
    // LiFePO4: Li+, Fe2+, P5+, O2-
    let guesses = oxi_state_guesses(
        &[Element::Li, Element::Fe, Element::P, Element::O],
        &[1.0, 1.0, 1.0, 4.0],
        0,
        None,
        false,
        None,
    );
    assert!(!guesses.is_empty());
    // Verify sorted by decreasing probability
    assert!(
        guesses
            .windows(2)
            .all(|w| w[0].probability >= w[1].probability)
    );
    check_oxi_guess(
        "LiFePO4",
        &[Element::Li, Element::Fe, Element::P, Element::O],
        &[1.0, 1.0, 1.0, 4.0],
        &[("Li", 1.0), ("P", 5.0), ("O", -2.0)],
    );
}

#[test]
fn test_combinations_with_replacement() {
    // C(2+2-1, 2) = C(3,2) = 3 non-decreasing combinations: [1,1], [1,2], [2,2]
    let combos = combinations_with_replacement(&[1, 2], 2);
    assert_eq!(combos.len(), 3);
    assert!(combos.iter().all(|c| c.windows(2).all(|w| w[0] <= w[1]))); // non-decreasing
    assert!(combinations_with_replacement(&[], 3).is_empty());
    assert_eq!(
        combinations_with_replacement(&[1, 2, 3], 0),
        vec![Vec::<i8>::new()]
    );
    // C(3+3-1, 3) = C(5,3) = 10
    assert_eq!(combinations_with_replacement(&[1, 2, 3], 3).len(), 10);
    // Guard against blow-ups: C(10+10-1, 10) = C(19,10) = 92378, under limit
    assert!(!combinations_with_replacement(&(0..10).collect::<Vec<i8>>(), 10).is_empty());
    // But C(2+100-1, 100) = C(101,2) = 5050 is fine, check large count doesn't overflow
    assert_eq!(combinations_with_replacement(&[1, 2], 100).len(), 101); // C(101,1) = 101
}

#[test]
fn test_get_candidate_oxi_states() {
    let fe = get_candidate_oxi_states(Element::Fe, false);
    assert!(fe.contains(&2) && fe.contains(&3));
    assert!(get_candidate_oxi_states(Element::O, false).contains(&-2));
}

// === Defect Charge State Guessing Tests ===

#[test]
fn test_format_oxi_state() {
    assert_eq!(format_oxi_state(2), "^{2+}");
    assert_eq!(format_oxi_state(-2), "^{2-}");
    assert_eq!(format_oxi_state(1), "^{+}");
    assert_eq!(format_oxi_state(-1), "^{-}");
    assert_eq!(format_oxi_state(0), "");
}

#[test]
fn test_get_element_oxi_probs() {
    // Oxygen should have -2 as most common
    let o_probs = get_element_oxi_probs("O");
    assert!(!o_probs.is_empty());
    assert_eq!(o_probs[0].0, -2, "O should have -2 as most common");

    // Iron should have multiple oxidation states
    let fe_probs = get_element_oxi_probs("Fe");
    assert!(!fe_probs.is_empty());
    assert!(
        fe_probs.iter().any(|(oxi, _)| *oxi == 3),
        "Fe should have +3"
    );
    assert!(
        fe_probs.iter().any(|(oxi, _)| *oxi == 2),
        "Fe should have +2"
    );

    // Unknown element should return empty
    let unknown = get_element_oxi_probs("Xx");
    assert!(unknown.is_empty());
}

#[test]
fn test_vacancy_charge_states() {
    // Oxygen vacancy: O^{2-} removed => charge = +2 most likely
    let charges = guess_defect_charge_states(DefectType::Vacancy, Some("O"), None, None, 4);
    assert!(!charges.is_empty());
    assert_eq!(charges[0].charge, 2, "O vacancy should be +2");
    assert!(
        charges[0].probability > 0.5,
        "O vacancy +2 should be dominant"
    );

    // Sodium vacancy: Na^{+} removed => charge = -1 most likely
    let na_charges = guess_defect_charge_states(DefectType::Vacancy, Some("Na"), None, None, 4);
    assert!(!na_charges.is_empty());
    assert_eq!(na_charges[0].charge, -1, "Na vacancy should be -1");
}

#[test]
fn test_interstitial_charge_states() {
    // Lithium interstitial: Li^{+} added => charge = +1 most likely
    let charges = guess_defect_charge_states(DefectType::Interstitial, None, Some("Li"), None, 4);
    assert!(!charges.is_empty());
    assert_eq!(charges[0].charge, 1, "Li interstitial should be +1");

    // Oxygen interstitial: O^{2-} added => charge = -2 most likely
    let o_charges = guess_defect_charge_states(DefectType::Interstitial, None, Some("O"), None, 4);
    assert!(!o_charges.is_empty());
    assert_eq!(o_charges[0].charge, -2, "O interstitial should be -2");
}

#[test]
fn test_substitution_charge_states() {
    // Al^{3+} on Si^{4+} site => charge = -1
    let charges =
        guess_defect_charge_states(DefectType::Substitution, None, Some("Al"), Some("Si"), 4);
    assert!(!charges.is_empty());
    // Al is typically 3+, Si is typically 4+, so charge should be -1
    assert!(
        charges.iter().any(|guess| guess.charge == -1),
        "Al on Si should have -1 as possibility"
    );

    // P^{5+} on Si^{4+} site => charge = +1
    let p_charges =
        guess_defect_charge_states(DefectType::Substitution, None, Some("P"), Some("Si"), 4);
    assert!(!p_charges.is_empty());
    assert!(
        p_charges.iter().any(|guess| guess.charge == 1),
        "P on Si should have +1 as possibility"
    );
}

#[test]
fn test_antisite_charge_states() {
    // Na-Cl antisite: should have various charge states
    let charges = guess_defect_charge_states(DefectType::Antisite, Some("Na"), Some("Cl"), None, 4);
    assert!(!charges.is_empty());
    // Na is +1, Cl is -1, so antisite charge = (+1) - (-1) = +2 or vice versa
    assert!(
        charges.iter().any(|guess| guess.charge.abs() <= 2),
        "Na-Cl antisite should have reasonable charges"
    );
}

#[test]
fn test_charge_state_probabilities_normalized() {
    let charges = guess_defect_charge_states(DefectType::Vacancy, Some("Fe"), None, None, 4);
    assert!(!charges.is_empty());
    let total: f64 = charges.iter().map(|guess| guess.probability).sum();
    assert!(
        (total - 1.0).abs() < 0.01,
        "Probabilities should sum to 1, got {total}"
    );
}

#[test]
fn test_charge_state_sorted_by_probability() {
    let charges = guess_defect_charge_states(DefectType::Vacancy, Some("O"), None, None, 4);
    assert!(charges.len() >= 2);
    for window in charges.windows(2) {
        assert!(
            window[0].probability >= window[1].probability,
            "Charges should be sorted by decreasing probability"
        );
    }
}

#[test]
fn test_max_charge_filtering() {
    // With max_charge = 1, should not see +2 charges for O vacancy
    let charges = guess_defect_charge_states(DefectType::Vacancy, Some("O"), None, None, 1);
    assert!(
        charges.iter().all(|guess| guess.charge.abs() <= 1),
        "All charges should be within max_charge"
    );
}

#[test]
fn test_missing_species_returns_empty() {
    let charges = guess_defect_charge_states(DefectType::Vacancy, None, None, None, 4);
    assert!(charges.is_empty(), "Missing species should return empty");

    let int_charges = guess_defect_charge_states(DefectType::Interstitial, None, None, None, 4);
    assert!(
        int_charges.is_empty(),
        "Missing species should return empty"
    );
}

#[test]
fn test_batch_charge_state_guessing() {
    let defects = vec![
        (DefectType::Vacancy, Some("O"), None, None),
        (DefectType::Interstitial, None, Some("Li"), None),
        (DefectType::Substitution, None, Some("Al"), Some("Si")),
    ];
    let results = guess_defect_charge_states_batch(&defects, 4);
    assert_eq!(results.len(), 3);
    assert!(!results[0].is_empty()); // O vacancy
    assert!(!results[1].is_empty()); // Li interstitial
    assert!(!results[2].is_empty()); // Al on Si
}
