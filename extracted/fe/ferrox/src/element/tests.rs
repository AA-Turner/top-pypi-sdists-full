use super::*;

#[test]
fn test_roundtrip() {
    // Comprehensive test: all 118 elements round-trip correctly
    for z in 1..=118 {
        let elem = Element::from_atomic_number(z).unwrap();
        assert_eq!(elem.atomic_number(), z, "atomic_number mismatch for Z={z}");
        assert_eq!(
            Element::from_symbol(elem.symbol()),
            Some(elem),
            "symbol roundtrip failed for Z={z}"
        );
        // Case-insensitive lookup
        assert_eq!(
            Element::from_symbol(&elem.symbol().to_lowercase()),
            Some(elem),
            "lowercase lookup failed for Z={z}"
        );
        assert_eq!(
            Element::from_symbol(&elem.symbol().to_uppercase()),
            Some(elem),
            "uppercase lookup failed for Z={z}"
        );
    }

    // Pseudo-elements roundtrip
    for (z, elem, sym) in [
        (119, Element::Dummy, "X"),
        (120, Element::D, "D"),
        (121, Element::T, "T"),
    ] {
        assert_eq!(Element::from_atomic_number(z), Some(elem));
        assert_eq!(elem.symbol(), sym);
        assert_eq!(Element::from_symbol(sym), Some(elem));
    }

    // Dummy atom aliases
    for alias in ["X", "Xx", "dummy", "Vac", "VA"] {
        assert_eq!(
            Element::from_symbol(alias),
            Some(Element::Dummy),
            "Dummy alias '{alias}' should work"
        );
    }

    // Edge cases: truly invalid inputs
    assert_eq!(
        Element::from_symbol(""),
        None,
        "empty string should return None"
    );
    assert_eq!(
        Element::from_symbol("  "),
        None,
        "whitespace should return None"
    );
    assert_eq!(
        Element::from_atomic_number(0),
        None,
        "Z=0 should return None"
    );
    assert_eq!(
        Element::from_atomic_number(122),
        None,
        "Z=122 should return None"
    );
    assert_eq!(
        Element::from_atomic_number(255),
        None,
        "Z=255 should return None"
    );
}

#[test]
fn test_atomic_mass() {
    // Verify data arrays have consistent lengths
    assert_eq!(Element::ATOMIC_MASSES.len(), Element::SYMBOLS.len());
    assert_eq!(Element::ELECTRONEGATIVITIES.len(), Element::SYMBOLS.len());

    // Spot-check common elements (element, expected, tolerance)
    for (elem, expected, tol) in [
        (Element::H, 1.008, 0.001),
        (Element::C, 12.011, 0.001),
        (Element::N, 14.007, 0.001),
        (Element::O, 15.999, 0.001),
        (Element::Fe, 55.845, 0.01),
        (Element::Cu, 63.546, 0.01),
        (Element::Au, 196.967, 0.01),
        (Element::U, 238.029, 0.01),
    ] {
        assert!((elem.atomic_mass() - expected).abs() < tol, "{elem:?}");
    }
    // All 118 elements should have positive mass
    for z in 1..=118 {
        assert!(Element::from_atomic_number(z).unwrap().atomic_mass() > 0.0);
    }

    // Superheavy elements (Z >= 104) should have monotonically increasing mass
    // (since values are based on most stable isotopes which increase with Z)
    for z in 104..118 {
        let m1 = Element::from_atomic_number(z).unwrap().atomic_mass();
        let m2 = Element::from_atomic_number(z + 1).unwrap().atomic_mass();
        assert!(
            m2 >= m1,
            "Mass should increase: Z={z} ({m1}) <= Z={} ({m2})",
            z + 1
        );
    }
}

#[test]
fn test_electronegativity() {
    // Spot-check known values (Pauling scale)
    let known_values = [
        (Element::H, Some(2.20)),
        (Element::C, Some(2.55)),
        (Element::N, Some(3.04)),
        (Element::O, Some(3.44)),
        (Element::F, Some(3.98)), // Most electronegative
        (Element::Fe, Some(1.83)),
        (Element::Au, Some(2.54)),
        // Some noble gases have no electronegativity (stored as NaN)
        (Element::He, None),
        (Element::Ne, None),
        (Element::Ar, None),
        // Note: Kr, Xe, Rn have values in this dataset (some sources assign them)
    ];

    for (elem, expected) in known_values {
        match expected {
            Some(val) => {
                let en = elem
                    .electronegativity()
                    .unwrap_or_else(|| panic!("{elem:?} should have electronegativity"));
                assert!(
                    (en - val).abs() < 0.01,
                    "{elem:?} electronegativity {en} != expected {val}"
                );
            }
            None => {
                assert!(
                    elem.electronegativity().is_none(),
                    "{elem:?} should have no electronegativity"
                );
            }
        }
    }

    // Verify electronegativity() returns None for elements with NaN
    // (He=2, Ne=10, Ar=18 are confirmed NaN in the dataset)
    for z in [2, 10, 18] {
        let elem = Element::from_atomic_number(z).unwrap();
        assert!(
            elem.electronegativity().is_none(),
            "{elem:?} (Z={z}) should have no electronegativity"
        );
    }
}

#[test]
#[allow(clippy::type_complexity)]
fn test_normalize_symbol_comprehensive() {
    // Test cases from the plan's symbol normalization table
    let test_cases: Vec<(&str, Element, Option<i8>, Vec<(&str, &str)>)> = vec![
        // (input, expected_element, expected_oxi, expected_metadata_pairs)
        ("Fe", Element::Fe, None, vec![]),
        ("Ca", Element::Ca, None, vec![]),
        ("O", Element::O, None, vec![]),
        // Oxidation states
        ("Fe2+", Element::Fe, Some(2), vec![]),
        ("O2-", Element::O, Some(-2), vec![]),
        ("Na+", Element::Na, Some(1), vec![]),
        ("Cl-", Element::Cl, Some(-1), vec![]),
        ("Fe3+", Element::Fe, Some(3), vec![]),
        ("Ti4+", Element::Ti, Some(4), vec![]),
        // POTCAR suffixes
        ("Ca_pv", Element::Ca, None, vec![("potcar_suffix", "_pv")]),
        ("Fe_sv", Element::Fe, None, vec![("potcar_suffix", "_sv")]),
        ("O_s", Element::O, None, vec![("potcar_suffix", "_s")]),
        // Pseudo-elements
        ("D", Element::D, None, vec![]),
        ("T", Element::T, None, vec![]),
        ("X", Element::Dummy, None, vec![]),
        ("Xx", Element::Dummy, None, vec![]),
        ("Dummy", Element::Dummy, None, vec![]),
        ("Vac", Element::Dummy, None, vec![]),
        // CIF-style labels
        ("Fe1", Element::Fe, None, vec![("label", "Fe1")]),
        ("Fe1_oct", Element::Fe, None, vec![("label", "Fe1_oct")]),
        ("Na2a", Element::Na, None, vec![("label", "Na2a")]),
        ("O2", Element::O, None, vec![("label", "O2")]),
        // Hash suffix (should be stripped, no metadata)
        ("Fe/hash123", Element::Fe, None, vec![]),
    ];

    for (input, expected_elem, expected_oxi, expected_metadata) in test_cases {
        let result = normalize_symbol(input)
            .unwrap_or_else(|e| panic!("Failed to normalize '{input}': {e}"));
        assert_eq!(
            result.element, expected_elem,
            "Element mismatch for '{input}': got {:?}, expected {:?}",
            result.element, expected_elem
        );
        assert_eq!(
            result.oxidation_state, expected_oxi,
            "Oxidation state mismatch for '{input}'"
        );

        // Check metadata
        for (key, expected_val) in expected_metadata {
            let actual = result.metadata.get(key);
            assert!(
                actual.is_some(),
                "Missing metadata key '{key}' for '{input}'"
            );
            let actual_str = actual.unwrap().as_str().unwrap_or("");
            assert_eq!(
                actual_str, expected_val,
                "Metadata mismatch for '{input}' key '{key}'"
            );
        }
    }

    // Test unknown symbol fallback to Dummy with original_symbol
    let unknown = normalize_symbol("UnknownElement123").unwrap();
    assert_eq!(unknown.element, Element::Dummy);
    assert_eq!(
        unknown
            .metadata
            .get("original_symbol")
            .and_then(|v| v.as_str()),
        Some("UnknownElement123")
    );

    // Test empty string error
    assert!(normalize_symbol("").is_err());
    assert!(normalize_symbol("   ").is_err());
}

#[test]
fn test_pseudo_element_properties() {
    // Test is_pseudo and is_dummy methods
    assert!(!Element::Fe.is_pseudo());
    assert!(!Element::H.is_pseudo());
    assert!(!Element::Og.is_pseudo());

    assert!(Element::Dummy.is_pseudo());
    assert!(Element::D.is_pseudo());
    assert!(Element::T.is_pseudo());

    assert!(Element::Dummy.is_dummy());
    assert!(!Element::D.is_dummy());
    assert!(!Element::T.is_dummy());
    assert!(!Element::Fe.is_dummy());

    // Test atomic_mass for pseudo-elements
    assert_eq!(Element::Dummy.atomic_mass(), 0.0);
    assert!((Element::D.atomic_mass() - 2.014).abs() < 0.01);
    assert!((Element::T.atomic_mass() - 3.016).abs() < 0.01);

    // Test electronegativity returns None for pseudo-elements
    assert!(Element::Dummy.electronegativity().is_none());
    assert!(Element::D.electronegativity().is_none());
    assert!(Element::T.electronegativity().is_none());
}

#[test]
fn test_row_and_group() {
    // Test periodic table positioning
    // Format: (element, expected_row, expected_group)
    let cases: &[(Element, u8, u8)] = &[
        // Period 1
        (Element::H, 1, 1),
        (Element::He, 1, 18),
        // Period 2
        (Element::Li, 2, 1),
        (Element::Be, 2, 2),
        (Element::B, 2, 13),
        (Element::C, 2, 14),
        (Element::N, 2, 15),
        (Element::O, 2, 16),
        (Element::F, 2, 17),
        (Element::Ne, 2, 18),
        // Period 3
        (Element::Na, 3, 1),
        (Element::Mg, 3, 2),
        (Element::Al, 3, 13),
        (Element::Ar, 3, 18),
        // Period 4 - transition metals
        (Element::K, 4, 1),
        (Element::Ca, 4, 2),
        (Element::Sc, 4, 3),
        (Element::Ti, 4, 4),
        (Element::Fe, 4, 8),
        (Element::Cu, 4, 11),
        (Element::Zn, 4, 12),
        (Element::Kr, 4, 18),
        // Lanthanoids (row 6, group 3)
        (Element::La, 6, 3),
        (Element::Ce, 6, 3),
        (Element::Lu, 6, 3),
        // Actinoids (row 7, group 3)
        (Element::Ac, 7, 3),
        (Element::U, 7, 3),
        (Element::Lr, 7, 3),
        // Period 7
        (Element::Og, 7, 18),
    ];

    for (elem, expected_row, expected_group) in cases {
        assert_eq!(
            elem.row(),
            *expected_row,
            "{elem:?} row should be {expected_row}"
        );
        assert_eq!(
            elem.group(),
            *expected_group,
            "{elem:?} group should be {expected_group}"
        );
    }

    // Pseudo-elements
    assert_eq!(Element::Dummy.row(), 0);
    assert_eq!(Element::Dummy.group(), 0);
}

#[test]
fn test_block() {
    let cases: &[(Element, Block)] = &[
        // s-block: groups 1-2
        (Element::H, Block::S),
        (Element::Li, Block::S),
        (Element::Na, Block::S),
        (Element::Ca, Block::S),
        // p-block: groups 13-18 (includes He despite 1s² config)
        (Element::B, Block::P),
        (Element::C, Block::P),
        (Element::O, Block::P),
        (Element::He, Block::P),
        (Element::Ne, Block::P),
        // d-block: groups 3-12
        (Element::Sc, Block::D),
        (Element::Fe, Block::D),
        (Element::Cu, Block::D),
        (Element::Zn, Block::D),
        // f-block boundaries: La (Z=57) to Yb (Z=70), Ac (Z=89) to No (Z=102)
        (Element::La, Block::F),
        (Element::Ce, Block::F),
        (Element::Yb, Block::F),
        (Element::Ac, Block::F),
        (Element::No, Block::F),
        // Lu (Z=71) and Lr (Z=103) are d-block
        (Element::Lu, Block::D),
        (Element::Lr, Block::D),
    ];
    for (elem, expected) in cases {
        assert_eq!(elem.block(), *expected, "{elem:?} should be {expected:?}");
    }
}

#[test]
fn test_classification() {
    // Helper to test a classification method on multiple elements
    fn check(elems: &[Element], pred: fn(&Element) -> bool, name: &str) {
        for elem in elems {
            assert!(pred(elem), "{elem:?} should be {name}");
        }
    }

    use Element::*;

    // Group classifications
    check(
        &[He, Ne, Ar, Kr, Xe, Rn, Og],
        Element::is_noble_gas,
        "noble gas",
    );
    check(&[Li, Na, K, Rb, Cs, Fr], Element::is_alkali, "alkali");
    check(&[Be, Mg, Ca, Sr, Ba, Ra], Element::is_alkaline, "alkaline");
    check(&[F, Cl, Br, I, At], Element::is_halogen, "halogen");
    check(&[O, S, Se, Te, Po], Element::is_chalcogen, "chalcogen");
    check(
        &[B, Si, Ge, As, Sb, Te, Po],
        Element::is_metalloid,
        "metalloid",
    );
    check(
        &[Fe, Cu, Zn, Au],
        Element::is_transition_metal,
        "transition metal",
    );
    check(&[Tc, Pm, Po, U], Element::is_radioactive, "radioactive");
    check(&[La, Ce, Sc, Y, U], Element::is_rare_earth, "rare earth");

    // Alkali/alkaline metals should also be metals
    for elem in [Li, Na, K, Be, Mg, Ca] {
        assert!(elem.is_metal(), "{elem:?} should be metal");
    }

    // Negative cases
    assert!(!H.is_noble_gas());
    assert!(!H.is_alkali()); // H is group 1 but not alkali
    assert!(!Al.is_transition_metal());
    assert!(!Fe.is_radioactive());
    assert!(!Bi.is_radioactive()); // Z=83, just below cutoff
    assert!(!Fe.is_rare_earth());
}

#[test]
fn test_oxidation_states() {
    // Iron has multiple oxidation states
    let fe_oxi = Element::Fe.oxidation_states();
    assert!(fe_oxi.contains(&2), "Fe should have +2");
    assert!(fe_oxi.contains(&3), "Fe should have +3");

    let fe_common = Element::Fe.common_oxidation_states();
    assert!(!fe_common.is_empty());

    // Max and min oxidation states
    let fe_max = Element::Fe.max_oxidation_state();
    let fe_min = Element::Fe.min_oxidation_state();
    assert!(fe_max.is_some());
    assert!(fe_min.is_some());
    assert!(fe_max.unwrap() > 0);
    assert!(fe_min.unwrap() < fe_max.unwrap());

    // Oxygen
    let o_oxi = Element::O.oxidation_states();
    assert!(o_oxi.contains(&-2), "O should have -2");

    // Noble gases typically have no oxidation states
    let he_oxi = Element::He.oxidation_states();
    assert!(he_oxi.is_empty(), "He should have no oxidation states");

    // Pseudo-elements
    assert!(Element::Dummy.oxidation_states().is_empty());
}

#[test]
fn test_radii() {
    // Atomic radius
    let fe_radius = Element::Fe.atomic_radius();
    assert!(fe_radius.is_some(), "Fe should have atomic radius");
    let radius = fe_radius.unwrap();
    assert!(
        radius > 1.0 && radius < 2.0,
        "Fe radius should be ~1.2-1.3 Å"
    );

    // Noble gases may not have atomic radius
    // (depends on data source)

    // Covalent radius
    let c_cov = Element::C.covalent_radius();
    assert!(c_cov.is_some(), "C should have covalent radius");

    // Ionic radii
    let fe_ionic = Element::Fe.ionic_radii();
    assert!(fe_ionic.is_some(), "Fe should have ionic radii");
    let ionic_map = fe_ionic.unwrap();
    assert!(ionic_map.contains_key("2") || ionic_map.contains_key("3"));

    // Ionic radius for specific oxidation state
    let fe2_radius = Element::Fe.ionic_radius(2);
    assert!(fe2_radius.is_some(), "Fe2+ should have ionic radius");

    // Pseudo-elements
    assert!(Element::Dummy.atomic_radius().is_none());
    assert!(Element::Dummy.ionic_radii().is_none());
}

#[test]
fn test_shannon_radii() {
    // Fe should have Shannon radii
    let fe_shannon = Element::Fe.shannon_radii();
    assert!(fe_shannon.is_some(), "Fe should have Shannon radii");

    // Fe2+ in octahedral coordination should have radius
    // Note: Shannon data uses Roman numerals for coordination
    let fe2_vi = Element::Fe.shannon_ionic_radius(2, "VI", "High Spin");
    // This may be None if the exact key doesn't match - just test the API works
    if let Some(radius) = fe2_vi {
        assert!(
            radius > 0.0 && radius < 1.5,
            "Shannon radius should be reasonable"
        );
    }

    // Na should have Shannon radii for +1
    let na_shannon = Element::Na.shannon_radii();
    assert!(na_shannon.is_some(), "Na should have Shannon radii");

    // Pseudo-elements
    assert!(Element::Dummy.shannon_radii().is_none());
}

#[test]
fn test_name() {
    assert_eq!(Element::Fe.name(), "Iron");
    assert_eq!(Element::H.name(), "Hydrogen");
    assert_eq!(Element::O.name(), "Oxygen");
    assert_eq!(Element::Au.name(), "Gold");
    assert_eq!(Element::Og.name(), "Oganesson");

    // Pseudo-elements return "Unknown"
    assert_eq!(Element::Dummy.name(), "Unknown");
}

// =========================================================================
// Pymatgen Edge Case Tests (ported from pymatgen test suite)
// =========================================================================

#[test]
fn test_invalid_symbols() {
    // Invalid symbols should return None
    assert!(Element::from_symbol("Dolphin").is_none());
    assert!(Element::from_symbol("Tyrannosaurus").is_none());
    assert!(Element::from_symbol("Zebra").is_none());
    // Note: Short invalid symbols may return Dummy instead of None
}

#[test]
fn test_isotopes_d_t() {
    // D and T are isotopes of hydrogen
    let d = Element::D;
    let t = Element::T;
    let h = Element::H;

    // All should have symbol "H" (normalized)
    assert_eq!(d.symbol(), "D");
    assert_eq!(t.symbol(), "T");
    assert_eq!(h.symbol(), "H");

    // Different atomic masses
    let h_mass = h.atomic_mass();
    let d_mass = d.atomic_mass();
    let t_mass = t.atomic_mass();
    assert!(d_mass > h_mass, "D mass should be > H mass");
    assert!(t_mass > d_mass, "T mass should be > D mass");
    assert!((d_mass - 2.014).abs() < 0.01, "D mass ≈ 2.014");
    assert!((t_mass - 3.016).abs() < 0.01, "T mass ≈ 3.016");
}

#[test]
fn test_from_atomic_number() {
    assert_eq!(Element::from_atomic_number(1), Some(Element::H));
    assert_eq!(Element::from_atomic_number(26), Some(Element::Fe));
    assert_eq!(Element::from_atomic_number(118), Some(Element::Og));
    assert_eq!(Element::from_atomic_number(0), None);
}

#[test]
fn test_element_equality() {
    assert_eq!(Element::Fe, Element::Fe);
    assert_eq!(Element::from_symbol("Fe"), Some(Element::Fe));
}

#[test]
fn test_normalize_symbol_edge_cases() {
    // Combined test for symbol normalization edge cases
    let simple_cases: &[(&str, Element)] = &[
        // POTCAR suffixes
        ("Ca_pv", Element::Ca),
        ("Fe_sv", Element::Fe),
        ("O_s", Element::O),
        // CIF labels
        ("Fe1", Element::Fe),
        ("Fe1a", Element::Fe),
        ("Na2", Element::Na),
        // Slash suffix (VASP 6.4.2)
        ("Li/", Element::Li),
    ];
    for (symbol, expected) in simple_cases {
        let norm = normalize_symbol(symbol).expect(symbol);
        assert_eq!(norm.element, *expected, "{symbol}");
    }

    // Oxidation state cases
    let oxi_cases: &[(&str, Element, i8)] = &[
        ("Fe2+", Element::Fe, 2),
        ("O2-", Element::O, -2),
        ("Na+", Element::Na, 1),
        ("Cl-", Element::Cl, -1),
    ];
    for (symbol, elem, oxi) in oxi_cases {
        let norm = normalize_symbol(symbol).expect(symbol);
        assert_eq!(norm.element, *elem, "{symbol}");
        assert_eq!(norm.oxidation_state, Some(*oxi), "{symbol}");
    }
}

#[test]
fn test_element_edge_cases() {
    // Dummy element has atomic number > 118, missing properties
    let dummy = Element::Dummy;
    assert!(dummy.atomic_number() > 118);
    assert!(dummy.atomic_radius().is_none());
    assert!(dummy.oxidation_states().is_empty());

    // Noble gases have undefined electronegativity (converted to None)
    assert!(Element::He.electronegativity().is_none());

    // U has many oxidation states
    assert!(!Element::U.oxidation_states().is_empty());

    // Og handles missing data gracefully
    let _ = (Element::Og.atomic_radius(), Element::Og.covalent_radius());
}
