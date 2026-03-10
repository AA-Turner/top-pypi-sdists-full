use super::slab::{
    compute_d_spacing, get_slab_transformation, identify_layer_positions, reduce_miller_indices,
};
use super::symmetry_helpers::{
    build_conventional_operations, generate_orbit, point_group_is_centrosymmetric,
    point_group_is_piezoelectric, resolve_spacegroup, spacegroup_to_crystal_system,
    spacegroup_type_from_number, validate_lattice_compatibility,
};
use super::*;
use crate::element::Element;
use crate::species::Species;
use moyo::data::Centering;
use nalgebra::Matrix3;

/// Shorthand for creating an ordered single-element SiteOccupancy in tests.
fn occ(sym: &str) -> SiteOccupancy {
    SiteOccupancy::ordered(Species::neutral(Element::from_symbol(sym).unwrap()))
}

// === Test Structure Factories ===

// NaCl primitive cell (rocksalt, a=5.64Å)
fn make_nacl() -> Structure {
    make_rocksalt(Element::Na, Element::Cl, 5.64)
}

// FCC conventional cell (4 atoms)
fn make_fcc_conventional(element: Element, a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![Species::neutral(element); 4],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.0),
            Vector3::new(0.5, 0.0, 0.5),
            Vector3::new(0.0, 0.5, 0.5),
        ],
    )
}

// BCC conventional cell (2 atoms)
fn make_bcc(element: Element, a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![Species::neutral(element); 2],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    )
}

// Rocksalt structure (cation at origin, anion at body center)
fn make_rocksalt(cation: Element, anion: Element, a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![Species::neutral(cation), Species::neutral(anion)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    )
}

// Single Cu atom at fractional position in 4Å cubic cell
fn make_cu_at(x: f64, y: f64, z: f64) -> Structure {
    Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::new(x, y, z)],
    )
}

// Single Cu atom at origin in cubic cell with variable lattice constant
fn make_cu_cubic(a: f64) -> Structure {
    Structure::new(
        Lattice::cubic(a),
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::zeros()],
    )
}

#[test]
fn test_structure_constructors() {
    // new() and try_new() both work
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert_eq!(s.num_sites(), 2);
    assert_eq!(s.composition().reduced_formula(), "NaCl");

    let s2 = Structure::try_new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    )
    .unwrap();
    assert_eq!(s2.num_sites(), 2);
}

#[test]
fn test_structure_constructor_errors() {
    // Length mismatch
    let result = Structure::try_new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![Vector3::new(0.0, 0.0, 0.0)], // Only 1 coord for 2 species
    );
    assert!(result.is_err());

    // Empty SiteOccupancy
    let empty_occ = SiteOccupancy {
        species: vec![],
        properties: HashMap::new(),
    };
    let result = Structure::try_new_from_occupancies(
        Lattice::cubic(4.0),
        vec![empty_occ],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    assert!(result.is_err());
    assert!(
        result
            .unwrap_err()
            .to_string()
            .contains("at least one species")
    );

    // Non-finite charge should error
    for bad_charge in [f64::NAN, f64::INFINITY, f64::NEG_INFINITY] {
        let result = Structure::try_new_full(
            Lattice::cubic(4.0),
            vec![SiteOccupancy::ordered(Species::neutral(Element::Na))],
            vec![Vector3::new(0.0, 0.0, 0.0)],
            [true, true, true],
            bad_charge,
            HashMap::new(),
        );
        assert!(
            result.is_err(),
            "Non-finite charge {bad_charge} should error"
        );
        assert!(
            result
                .unwrap_err()
                .to_string()
                .contains("charge must be finite")
        );
    }
}

#[test]
fn test_to_moyo_cell() {
    let s = make_nacl();
    let cell = s.to_moyo_cell();
    assert_eq!(cell.num_atoms(), 2);
    assert_eq!(cell.numbers, vec![11, 17]);
}

#[test]
fn test_from_moyo_cell_roundtrip() {
    let s = make_nacl();
    let s2 = Structure::from_moyo_cell(&s.to_moyo_cell()).unwrap();
    assert_eq!(s2.num_sites(), s.num_sites());
    assert_eq!(s2.species()[0].element, Element::Na);
    assert_eq!(s2.species()[1].element, Element::Cl);
}

#[test]
fn test_get_primitive_fcc() {
    let fcc_conv = make_fcc_conventional(Element::Cu, 3.6);
    assert_eq!(fcc_conv.num_sites(), 4);
    let prim = fcc_conv.get_primitive(1e-4).unwrap();
    assert_eq!(prim.num_sites(), 1);
    assert_eq!(prim.species()[0].element, Element::Cu);
}

#[test]
fn test_get_spacegroup_number() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    assert_eq!(fcc.get_spacegroup_number(1e-4).unwrap(), 225);
}

#[test]
fn test_get_spacegroup_symbol() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    // moyo returns space-separated symbols
    assert_eq!(fcc.get_spacegroup_symbol(1e-4).unwrap(), "F m -3 m");
    let bcc = make_bcc(Element::Fe, 2.87);
    assert_eq!(bcc.get_spacegroup_symbol(1e-4).unwrap(), "I m -3 m");
    let nacl = make_nacl();
    assert_eq!(nacl.get_spacegroup_symbol(1e-4).unwrap(), "P m -3 m");
}

#[test]
fn test_get_hall_number() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    // FCC (Fm-3m) has Hall number 523
    let hall = fcc.get_hall_number(1e-4).unwrap();
    assert!(hall > 0 && hall <= 530);
}

#[test]
fn test_get_pearson_symbol() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    // FCC Cu conventional cell: face-centered cubic with 4 atoms
    assert_eq!(fcc.get_pearson_symbol(1e-4).unwrap(), "cF4");
    let bcc = make_bcc(Element::Fe, 2.87);
    // BCC Fe: body-centered cubic with 2 atoms
    assert_eq!(bcc.get_pearson_symbol(1e-4).unwrap(), "cI2");
}

#[test]
fn test_get_wyckoff_letters() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let wyckoffs = fcc.get_wyckoff_letters(1e-4).unwrap();
    assert_eq!(wyckoffs.len(), 4); // 4 atoms in conventional FCC cell
    // All should be same Wyckoff position for identical atoms
    let first = wyckoffs[0];
    assert!(wyckoffs.iter().all(|&w| w == first));
}

#[test]
fn test_get_wyckoff_sites() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let sites = fcc.get_wyckoff_sites(1e-4).unwrap();
    assert_eq!(sites.len(), 4); // 4 atoms in conventional FCC cell

    // All sites should have same Wyckoff label (equivalent positions)
    let first_label = &sites[0].label;
    assert!(sites.iter().all(|s| &s.label == first_label));

    // Multiplicity should be 4 for 4a Wyckoff position in Fm-3m
    assert_eq!(sites[0].multiplicity, 4);

    // All sites should have same site symmetry
    let first_symm = &sites[0].site_symmetry;
    assert!(sites.iter().all(|s| &s.site_symmetry == first_symm));

    // Test NaCl - should have two different Wyckoff positions
    let nacl = make_nacl();
    let nacl_sites = nacl.get_wyckoff_sites(1e-4).unwrap();
    assert_eq!(nacl_sites.len(), 2);
    // Na and Cl are at different Wyckoff positions
    assert_ne!(nacl_sites[0].label, nacl_sites[1].label);
}

#[test]
fn test_get_site_symmetry_symbols() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let symbols = fcc.get_site_symmetry_symbols(1e-4).unwrap();
    assert_eq!(symbols.len(), 4);
    // FCC atoms at high-symmetry positions should have same site symmetry
    let first = &symbols[0];
    assert!(symbols.iter().all(|s| s == first));
}

#[test]
fn test_get_symmetry_operations() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let ops = fcc.get_symmetry_operations(1e-4).unwrap();
    // Fm-3m has 192 operations in the conventional cell
    assert_eq!(
        ops.len(),
        192,
        "FCC Fm-3m should have 192 symmetry operations"
    );
    // Check that operations have valid structure
    for (rot, trans) in &ops {
        // Rotation determinant should be +/- 1
        let det = rot[0][0] * (rot[1][1] * rot[2][2] - rot[1][2] * rot[2][1])
            - rot[0][1] * (rot[1][0] * rot[2][2] - rot[1][2] * rot[2][0])
            + rot[0][2] * (rot[1][0] * rot[2][1] - rot[1][1] * rot[2][0]);
        assert!(det == 1 || det == -1);
        // Translation should be within the conventional [-0.5, 0.5] range
        // (with symmetric tolerance for floating-point rounding)
        for &t in trans {
            assert!((-0.5 - 1e-8..=0.5 + 1e-8).contains(&t));
        }
    }
}

#[test]
fn test_get_equivalent_sites() {
    // NaCl: 2 sites should be inequivalent (different elements)
    let nacl = make_nacl();
    let orbits = nacl.get_equivalent_sites(1e-4).unwrap();
    assert_eq!(orbits.len(), 2);
    // Each site should be its own representative since they're different elements
    assert_eq!(orbits[0], 0);
    assert_eq!(orbits[1], 1);

    // FCC: All 4 sites should be equivalent
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let orbits_fcc = fcc.get_equivalent_sites(1e-4).unwrap();
    assert_eq!(orbits_fcc.len(), 4);
    // All should map to the same representative
    let representative = orbits_fcc[0];
    assert!(orbits_fcc.iter().all(|&o| o == representative));
}

#[test]
fn test_get_crystal_system() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    assert_eq!(fcc.get_crystal_system(1e-4).unwrap(), "cubic");
    let bcc = make_bcc(Element::Fe, 2.87);
    assert_eq!(bcc.get_crystal_system(1e-4).unwrap(), "cubic");
    let nacl = make_nacl();
    assert_eq!(nacl.get_crystal_system(1e-4).unwrap(), "cubic");
}

#[test]
fn test_get_symmetry_dataset() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let dataset = fcc.get_symmetry_dataset(1e-4).unwrap();
    assert_eq!(dataset.number, 225);
    assert_eq!(dataset.hm_symbol, "F m -3 m");
    assert_eq!(dataset.wyckoffs.len(), 4);
    assert_eq!(dataset.orbits.len(), 4);
    assert!(!dataset.operations.is_empty());
}

#[test]
fn test_empty_structure_symmetry_error() {
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    let result = empty.get_symmetry_dataset(1e-4);
    assert!(result.is_err());
    let err = result.unwrap_err();
    assert!(err.to_string().contains("empty structure"));
}

#[test]
fn test_crystal_system_coverage() {
    // Test the spacegroup_to_crystal_system helper
    assert_eq!(spacegroup_to_crystal_system(1), "triclinic");
    assert_eq!(spacegroup_to_crystal_system(2), "triclinic");
    assert_eq!(spacegroup_to_crystal_system(3), "monoclinic");
    assert_eq!(spacegroup_to_crystal_system(15), "monoclinic");
    assert_eq!(spacegroup_to_crystal_system(16), "orthorhombic");
    assert_eq!(spacegroup_to_crystal_system(74), "orthorhombic");
    assert_eq!(spacegroup_to_crystal_system(75), "tetragonal");
    assert_eq!(spacegroup_to_crystal_system(142), "tetragonal");
    assert_eq!(spacegroup_to_crystal_system(143), "trigonal");
    assert_eq!(spacegroup_to_crystal_system(167), "trigonal");
    assert_eq!(spacegroup_to_crystal_system(168), "hexagonal");
    assert_eq!(spacegroup_to_crystal_system(194), "hexagonal");
    assert_eq!(spacegroup_to_crystal_system(195), "cubic");
    assert_eq!(spacegroup_to_crystal_system(230), "cubic");
    assert_eq!(spacegroup_to_crystal_system(0), "unknown");
    assert_eq!(spacegroup_to_crystal_system(231), "unknown");
}

#[test]
fn test_spacegroups() {
    assert_eq!(
        make_fcc_conventional(Element::Cu, 3.6)
            .get_spacegroup_number(1e-4)
            .unwrap(),
        225
    );
    assert_eq!(
        make_bcc(Element::Fe, 2.87)
            .get_spacegroup_number(1e-4)
            .unwrap(),
        229
    );
    assert_eq!(make_nacl().get_spacegroup_number(1e-4).unwrap(), 221);
}

#[test]
fn test_get_primitive() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    assert_eq!(fcc.get_primitive(1e-4).unwrap().num_sites(), 1);
    let bcc = make_bcc(Element::Fe, 2.87);
    assert_eq!(bcc.get_primitive(1e-4).unwrap().num_sites(), 1);
}

#[test]
fn test_moyo_roundtrip() {
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let restored = Structure::from_moyo_cell(&fcc.to_moyo_cell()).unwrap();
    assert_eq!(restored.num_sites(), fcc.num_sites());
    for (orig, new) in fcc.species().iter().zip(restored.species().iter()) {
        assert_eq!(orig.element, new.element);
    }
    let diff = (fcc.lattice.matrix() - restored.lattice.matrix()).norm();
    assert!(diff < 1e-10, "lattice matrix mismatch: norm diff = {diff}");
}

#[test]
fn test_moyo_roundtrip_hexagonal_lattice() {
    let hex = Structure::new(
        Lattice::hexagonal(5.0, 14.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let restored = Structure::from_moyo_cell(&hex.to_moyo_cell()).unwrap();
    let diff = (hex.lattice.matrix() - restored.lattice.matrix()).norm();
    assert!(diff < 1e-10, "lattice matrix mismatch: norm diff = {diff}");
}

#[test]
fn test_moyo_roundtrip_skewed_lattice_preserves_row_basis() {
    let skewed = Structure::new(
        Lattice::from_array([[3.1, 0.2, 0.1], [0.0, 4.2, 0.3], [0.0, 0.0, 5.3]]),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::O)],
        vec![
            Vector3::new(0.12, 0.23, 0.34),
            Vector3::new(0.61, 0.42, 0.83),
        ],
    );
    let moyo_cell = skewed.to_moyo_cell();

    // moyo stores the same basis vectors as columns internally.
    assert_eq!(moyo_cell.lattice.basis, skewed.lattice.matrix().transpose());

    let restored = Structure::from_moyo_cell(&moyo_cell).unwrap();
    let diff = (skewed.lattice.matrix() - restored.lattice.matrix()).norm();
    assert!(diff < 1e-10, "lattice matrix mismatch: norm diff = {diff}");
}

#[test]
fn test_conventional_cell_angles_r3c() {
    // Fe2O3 corundum (SG 167, R-3c): conventional cell must be hexagonal
    let hex_lattice = Lattice::hexagonal(5.0355, 13.7471);
    let struc = Structure::from_spacegroup(
        "167",
        hex_lattice,
        vec![occ("Fe"), occ("O")],
        vec![
            Vector3::new(0.0, 0.0, 0.3553),
            Vector3::new(0.3060, 0.0, 0.25),
        ],
        None,
    )
    .expect("Should create R-3c structure");

    let conv = struc.get_conventional_structure(1e-4).unwrap();
    let angles = conv.lattice.angles();
    for (&angle, (label, expected)) in
        angles
            .iter()
            .zip([("alpha", 90.0), ("beta", 90.0), ("gamma", 120.0)])
    {
        assert!(
            (angle - expected).abs() < 0.5,
            "{label} should be ~{expected}°, got {angle:.1}°",
        );
    }
    let lengths = conv.lattice.lengths();
    assert!(
        (lengths[0] - lengths[1]).abs() < 0.01,
        "a and b should be equal, got a={:.4}, b={:.4}",
        lengths[0],
        lengths[1]
    );
}

#[test]
fn test_oxidation_states() {
    let nacl = Structure::new(
        Lattice::cubic(5.64),
        vec![
            Species::new(Element::Na, Some(1)),
            Species::new(Element::Cl, Some(-1)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert_eq!(nacl.species()[0].oxidation_state, Some(1));
    assert_eq!(nacl.species()[1].oxidation_state, Some(-1));
}

#[test]
fn test_cart_coords() {
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Cu); 2],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let cart = s.cart_coords();
    assert_eq!(cart.len(), 2);
    assert!((cart[1][0] - 2.0).abs() < 1e-10);
}

#[test]
fn test_empty_structure() {
    let s = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    assert_eq!(s.num_sites(), 0);
    assert!(s.composition().is_empty());
}

#[test]
fn test_disordered_structure() {
    let site_occ = vec![
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ]),
        SiteOccupancy::ordered(Species::neutral(Element::O)),
    ];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(4.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert_eq!(s.num_sites(), 2);
    assert!(!s.is_ordered());
    assert!(!s.site_occupancies[0].is_ordered());
    assert!(s.site_occupancies[1].is_ordered());
}

#[test]
fn test_disordered_composition() {
    let site_occ = vec![
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ]),
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ]),
    ];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(4.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let comp = s.composition();
    assert!((comp.get(Element::Fe) - 1.0).abs() < 1e-10);
    assert!((comp.get(Element::Co) - 1.0).abs() < 1e-10);
    assert_eq!(comp.reduced_formula(), "FeCo");
}

#[test]
fn test_species_composition_preserves_oxidation_states() {
    let fe2 = Species::new(Element::Fe, Some(2));
    let fe3 = Species::new(Element::Fe, Some(3));
    let o2 = Species::new(Element::O, Some(-2));

    // Minimal structure: Fe2+, Fe3+, O2- (3 sites)
    let structure = Structure::new(
        Lattice::cubic(4.0),
        vec![fe2, fe3, o2],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
        ],
    );

    // composition() loses oxidation states
    let elem_comp = structure.composition();
    assert!((elem_comp.get(Element::Fe) - 2.0).abs() < 1e-10);

    // species_composition() preserves them
    let species_comp = structure.species_composition();
    assert!((species_comp.get(fe2) - 1.0).abs() < 1e-10);
    assert!((species_comp.get(fe3) - 1.0).abs() < 1e-10);

    // species_hash differs, formula_hash is the same
    assert_ne!(elem_comp.species_hash(), species_comp.species_hash());
    assert_eq!(elem_comp.formula_hash(), species_comp.formula_hash());
}

#[test]
fn test_ordered_structure_is_ordered() {
    assert!(make_nacl().is_ordered());
}

#[test]
fn test_species_accessor() {
    let site_occ = vec![
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.7),
            (Species::neutral(Element::Co), 0.3),
        ]),
        SiteOccupancy::ordered(Species::neutral(Element::O)),
    ];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(4.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert_eq!(s.species()[0].element, Element::Fe);
    assert_eq!(s.species()[1].element, Element::O);
}

#[test]
fn test_unique_elements_disordered() {
    let site_occ = vec![
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ]),
        SiteOccupancy::ordered(Species::neutral(Element::O)),
    ];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(4.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let elements = s.unique_elements();
    assert_eq!(elements.len(), 3);
    assert!(elements.contains(&Element::Fe));
    assert!(elements.contains(&Element::Co));
    assert!(elements.contains(&Element::O));
}

#[test]
fn test_unique_elements_non_consecutive_duplicates() {
    // Verify itertools::unique() removes ALL duplicates, not just consecutive ones.
    // Pattern: disordered site with Fe+Co followed by ordered Fe site.
    // Should produce [Fe, Co], not [Fe, Co, Fe].
    let site_occ = vec![
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ]),
        SiteOccupancy::ordered(Species::neutral(Element::Fe)), // Fe again, non-consecutive
    ];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(4.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let elements = s.unique_elements();
    // itertools::unique() correctly removes ALL duplicates (not just consecutive ones
    // like dedup() would). This is critical for fit_anonymous() to work correctly.
    assert_eq!(
        elements.len(),
        2,
        "unique_elements should dedupe non-consecutive duplicates, got: {elements:?}"
    );
    assert!(elements.contains(&Element::Fe));
    assert!(elements.contains(&Element::Co));
}

// === remap_species() tests ===

#[test]
fn test_remap_species_basic() {
    // NaCl -> KCl mapping
    let nacl = make_rocksalt(Element::Na, Element::Cl, 5.64);
    let mapping = HashMap::from([(Element::Na, Element::K)]);
    let remapped = nacl.remap_species(&mapping);

    assert_eq!(
        remapped.species()[0].element,
        Element::K,
        "Na should map to K"
    );
    assert_eq!(
        remapped.species()[1].element,
        Element::Cl,
        "Cl should be unchanged"
    );
    assert_eq!(
        remapped.num_sites(),
        nacl.num_sites(),
        "Site count should be preserved"
    );
}

#[test]
fn test_remap_species_preserves_oxidation_states() {
    // Species with oxidation states should preserve them
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::new(Element::Fe, Some(2)),
            Species::new(Element::O, Some(-2)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let mapping = HashMap::from([(Element::Fe, Element::Co)]);
    let remapped = s.remap_species(&mapping);

    assert_eq!(remapped.species()[0].element, Element::Co);
    assert_eq!(
        remapped.species()[0].oxidation_state,
        Some(2),
        "Oxidation state should be preserved"
    );
}

#[test]
fn test_remap_species_unmapped_elements_unchanged() {
    let s = make_rocksalt(Element::Na, Element::Cl, 5.64);
    let mapping = HashMap::from([(Element::Fe, Element::Co)]); // irrelevant mapping
    let remapped = s.remap_species(&mapping);

    assert_eq!(
        remapped.species()[0].element,
        Element::Na,
        "Na should be unchanged"
    );
    assert_eq!(
        remapped.species()[1].element,
        Element::Cl,
        "Cl should be unchanged"
    );
}

#[test]
fn test_remap_species_empty_structure() {
    let s = Structure::new(Lattice::cubic(5.0), vec![], vec![]);
    let mapping = HashMap::from([(Element::Na, Element::K)]);
    let remapped = s.remap_species(&mapping);
    assert_eq!(
        remapped.num_sites(),
        0,
        "Empty structure should remain empty"
    );
}

#[test]
fn test_remap_species_disordered_site() {
    // Disordered site with Fe(0.6) + Co(0.4), mapping both to Ni
    // Should produce single Ni(1.0) species
    let site_occ = vec![SiteOccupancy::new(vec![
        (Species::neutral(Element::Fe), 0.6),
        (Species::neutral(Element::Co), 0.4),
    ])];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(4.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let mapping = HashMap::from([(Element::Fe, Element::Ni), (Element::Co, Element::Ni)]);
    let remapped = s.remap_species(&mapping);

    // Should have single species with combined occupancy
    assert_eq!(remapped.site_occupancies[0].species.len(), 1);
    assert_eq!(remapped.species()[0].element, Element::Ni);
    assert!(
        (remapped.site_occupancies[0].total_occupancy() - 1.0).abs() < 1e-10,
        "Occupancies should sum to 1.0"
    );
}

// === Neighbor Finding Tests ===

#[test]
fn test_neighbor_list_edge_cases() {
    // Empty structure returns empty results
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    let (centers, neighbors, images, distances) = empty.get_neighbor_list(3.0, 1e-8, true);
    assert!(
        centers.is_empty() && neighbors.is_empty() && images.is_empty() && distances.is_empty()
    );

    // Zero cutoff returns empty results
    let nacl = make_nacl();
    let (centers, neighbors, images, distances) = nacl.get_neighbor_list(0.0, 1e-8, true);
    assert!(
        centers.is_empty() && neighbors.is_empty() && images.is_empty() && distances.is_empty()
    );
}

#[test]
fn test_neighbor_list_nacl() {
    // NaCl: Na at (0,0,0), Cl at (0.5,0.5,0.5)
    // Na-Cl distance = a * sqrt(3) / 2 = 5.64 * sqrt(3) / 2 ≈ 4.88 Å
    let nacl = make_nacl();
    let na_cl_dist = 5.64 * (3.0_f64).sqrt() / 2.0;

    // Find neighbors within 5 Å (should find the Cl neighbor)
    let (centers, neighbors, _images, distances) = nacl.get_neighbor_list(5.0, 1e-8, true);

    // Count neighbors of site 0 (Na)
    let na_neighbors: Vec<_> = centers
        .iter()
        .zip(&distances)
        .filter(|&(&c, _)| c == 0)
        .collect();

    assert!(
        !na_neighbors.is_empty(),
        "Na should have at least one neighbor within 5 Å"
    );

    // Check that the Cl neighbor is found at correct distance
    let cl_found = na_neighbors
        .iter()
        .any(|&(_, &d)| (d - na_cl_dist).abs() < 0.01);
    assert!(cl_found, "Should find Cl at distance {:.2} Å", na_cl_dist);

    // Verify neighbor is Cl (site 1)
    let cl_neighbor = centers
        .iter()
        .zip(&neighbors)
        .any(|(&c, &n)| c == 0 && n == 1);
    assert!(
        cl_neighbor,
        "Na (site 0) should have Cl (site 1) as neighbor"
    );
}

#[test]
fn test_neighbor_list_fcc_nearest_neighbors() {
    // FCC Cu: each atom has 12 nearest neighbors at distance a/sqrt(2)
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let nn_dist = 3.6 / (2.0_f64).sqrt(); // ≈ 2.55 Å

    // Find neighbors just beyond NN distance
    let (centers, _neighbors, _images, distances) =
        fcc.get_neighbor_list(nn_dist + 0.1, 1e-8, true);

    // Count unique (center, neighbor) pairs for site 0
    let site0_neighbors: Vec<_> = centers
        .iter()
        .zip(&distances)
        .filter(|&(&c, _)| c == 0)
        .collect();

    assert_eq!(
        site0_neighbors.len(),
        12,
        "FCC site 0 should have 12 nearest neighbors, got {}",
        site0_neighbors.len()
    );

    // All distances should be approximately nn_dist
    for &(_, &d) in &site0_neighbors {
        assert!(
            (d - nn_dist).abs() < 0.01,
            "NN distance should be {:.3}, got {:.3}",
            nn_dist,
            d
        );
    }
}

#[test]
fn test_neighbor_list_self_pairs() {
    let s = make_cu_at(0.0, 0.0, 0.0);

    // With exclude_self=true, should not find self at distance 0
    let (centers, neighbors, images, _) = s.get_neighbor_list(10.0, 1e-8, true);
    let self_same_image = centers
        .iter()
        .zip(&neighbors)
        .zip(&images)
        .any(|((&c, &n), &img)| c == n && img == [0, 0, 0]);
    assert!(!self_same_image, "Self in same image should be excluded");

    // With exclude_self=false, should find self at distance 0
    let (_, _, images, distances) = s.get_neighbor_list(0.1, 1e-8, false);
    let self_found = images
        .iter()
        .zip(&distances)
        .any(|(&img, &d)| img == [0, 0, 0] && d < 1e-8);
    assert!(self_found, "Self at distance 0 should be found");
}

#[test]
fn test_neighbor_list_periodic_images() {
    // Cutoff = 4.0 should find 6 neighbors (periodic images along each axis)
    let (centers, _, images, distances) =
        make_cu_at(0.0, 0.0, 0.0).get_neighbor_list(4.0, 1e-8, true);

    assert_eq!(centers.len(), 6, "Should find 6 periodic images");
    assert!(distances.iter().all(|&d| (d - 4.0).abs() < 1e-8));

    // Check all 6 face-adjacent images are found
    for exp in [
        [-1, 0, 0],
        [1, 0, 0],
        [0, -1, 0],
        [0, 1, 0],
        [0, 0, -1],
        [0, 0, 1],
    ] {
        assert!(images.contains(&exp), "Missing image {exp:?}");
    }
}

#[test]
fn test_get_all_neighbors() {
    let nacl = make_nacl();
    let neighbors = nacl.get_all_neighbors(5.0);

    assert_eq!(neighbors.len(), 2, "Should have 2 sites");
    assert!(!neighbors[0].is_empty(), "Na should have neighbors");
    assert!(!neighbors[1].is_empty(), "Cl should have neighbors");
}

#[test]
fn test_get_distance() {
    let nacl = make_nacl();

    // Self-distance is zero
    assert!(nacl.get_distance(0, 0) < 1e-10);
    assert!(nacl.get_distance(1, 1) < 1e-10);

    // Distance is symmetric
    let d01 = nacl.get_distance(0, 1);
    assert!((d01 - nacl.get_distance(1, 0)).abs() < 1e-10);

    // Na-Cl distance in rocksalt is a*sqrt(3)/2
    let expected = 5.64 * (3.0_f64).sqrt() / 2.0;
    assert!(
        (d01 - expected).abs() < 0.01,
        "Na-Cl distance: expected {expected:.3}, got {d01:.3}"
    );
}

#[test]
#[should_panic(expected = "out of bounds")]
fn test_get_distance_out_of_bounds() {
    let nacl = make_nacl();
    nacl.get_distance(0, 10); // Site 10 doesn't exist
}

#[test]
fn test_distance_matrix() {
    // Empty structure returns empty matrix
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    assert!(empty.distance_matrix().is_empty());

    // NaCl: dimensions, consistency with get_distance
    let nacl = make_nacl();
    let dm = nacl.distance_matrix();
    assert_eq!(dm.len(), 2);
    assert!(dm.iter().all(|row| row.len() == 2));
    for (idx, row) in dm.iter().enumerate() {
        for (jdx, &d) in row.iter().enumerate() {
            assert!((d - nacl.get_distance(idx, jdx)).abs() < 1e-10);
        }
    }

    // FCC: diagonal is zero, matrix is symmetric
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    let dm = fcc.distance_matrix();
    for (idx, row) in dm.iter().enumerate() {
        assert!(row[idx] < 1e-10, "Diagonal should be 0");
        for (jdx, &val) in row.iter().enumerate().skip(idx + 1) {
            assert!((val - dm[jdx][idx]).abs() < 1e-10, "Should be symmetric");
        }
    }
}

// === Comprehensive tests for pymatgen-parity features ===

#[test]
fn test_distance_and_image_cubic() {
    // sqrt(2.5^2 + 3.5^2 + 4.5^2) = 6.22494979899
    let expected_dist = 6.22494979899;

    // Direct path (no image shift)
    let s = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.25, 0.35, 0.45), Vector3::zeros()],
    );
    let (dist, img) = s.get_distance_and_image(0, 1);
    assert!((dist - expected_dist).abs() < 1e-6);
    assert_eq!(img, [0, 0, 0]);

    // Via periodic boundary (site at 1.0 wraps to 0.0)
    let s = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.25, 0.35, 0.45), Vector3::new(1.0, 1.0, 1.0)],
    );
    let (dist, img) = s.get_distance_and_image(0, 1);
    assert!((dist - expected_dist).abs() < 1e-6);
    assert!((dist - s.get_distance_with_image(0, 1, img)).abs() < 1e-10);
}

#[test]
fn test_distance_and_image_lattice_types() {
    // Same site: zero distance
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.5, 0.5, 0.5)],
    );
    let (dist, img) = s.get_distance_and_image(0, 0);
    assert!(dist < 1e-10);
    assert_eq!(img, [0, 0, 0]);

    // Multiple lattice types: verify get_distance_and_image matches get_distance
    let lattices = [
        Lattice::cubic(4.0),
        Lattice::hexagonal(3.0, 5.0),
        Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0), // Triclinic
        Lattice::from_parameters(3.0, 3.1, 10.0, 2.96, 2.0, 1.0),  // Highly skewed
    ];
    for lattice in lattices {
        let s = Structure::new(
            lattice,
            vec![Species::neutral(Element::Fe), Species::neutral(Element::Cu)],
            vec![Vector3::new(0.1, 0.2, 0.3), Vector3::new(0.7, 0.8, 0.9)],
        );
        let (dist, _) = s.get_distance_and_image(0, 1);
        assert!((dist - s.get_distance(0, 1)).abs() < 1e-10);
        assert!(dist > 0.0 && dist < 10.0);
    }
    // Image roundtrip consistency (cubic - simple case where LLL doesn't skew images)
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Cu)],
        vec![Vector3::new(0.1, 0.2, 0.3), Vector3::new(0.7, 0.8, 0.9)],
    );
    let (dist, img) = s.get_distance_and_image(0, 1);
    assert!((dist - s.get_distance_with_image(0, 1, img)).abs() < 1e-10);

    // Hexagonal: verify specific distance along c-axis
    let s = Structure::new(
        Lattice::hexagonal(3.0, 5.0),
        vec![Species::neutral(Element::Cu), Species::neutral(Element::Cu)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.0, 0.0, 0.5)],
    );
    let (dist, _) = s.get_distance_and_image(0, 1);
    assert!((dist - 2.5).abs() < 1e-10); // 0.5 * 5.0
}

#[test]
fn test_distance_with_image() {
    // Specific image distances in cubic lattice
    let s = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::zeros(), Vector3::new(0.5, 0.0, 0.0)],
    );
    assert!((s.get_distance_with_image(0, 1, [0, 0, 0]) - 5.0).abs() < 1e-10); // Direct
    assert!((s.get_distance_with_image(0, 1, [1, 0, 0]) - 15.0).abs() < 1e-10); // +a shift
    assert!((s.get_distance_with_image(0, 1, [-1, 0, 0]) - 5.0).abs() < 1e-10); // -a shift
    let diag_expected = (1.5_f64.powi(2) + 1.0 + 1.0).sqrt() * 10.0;
    assert!((s.get_distance_with_image(0, 1, [1, 1, 1]) - diag_expected).abs() < 1e-10);

    // Image returned by get_distance_and_image gives same distance
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Cu), Species::neutral(Element::Cu)],
        vec![Vector3::new(0.1, 0.0, 0.0), Vector3::new(0.9, 0.0, 0.0)],
    );
    let (dist, img) = s.get_distance_and_image(0, 1);
    assert!((dist - s.get_distance_with_image(0, 1, img)).abs() < 1e-10);

    // Coordinates outside [0,1) are wrapped correctly for periodic axes
    let s = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.25, 0.35, 0.45), Vector3::new(1.0, 1.0, 1.0)], // Wraps to (0,0,0)
    );
    let (dist, img) = s.get_distance_and_image(0, 1);
    assert!((dist - s.get_distance_with_image(0, 1, img)).abs() < 1e-10);

    // Non-periodic axes: coordinates outside [0,1) should NOT be wrapped
    let mut slab_lattice = Lattice::cubic(10.0);
    slab_lattice.pbc = [true, true, false]; // z is non-periodic (slab)
    let s = Structure::new(
        slab_lattice.clone(),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.1), Vector3::new(0.0, 0.0, 1.5)], // z=1.5 outside [0,1)
    );
    // With non-periodic z, z=1.5 should NOT wrap to 0.5
    // Distance should be (1.5 - 0.1) * 10 = 14, not (0.5 - 0.1) * 10 = 4
    let dist = s.get_distance_with_image(0, 1, [0, 0, 0]);
    assert!(
        (dist - 14.0).abs() < 1e-10,
        "Non-periodic axis should not wrap: expected 14.0, got {dist}"
    );

    // Negative coordinate on non-periodic axis should also NOT wrap
    let s = Structure::new(
        slab_lattice.clone(),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.5), Vector3::new(0.0, 0.0, -0.5)], // z=-0.5
    );
    // z=-0.5 should NOT wrap to 0.5, distance = |0.5 - (-0.5)| * 10 = 10
    let dist = s.get_distance_with_image(0, 1, [0, 0, 0]);
    assert!(
        (dist - 10.0).abs() < 1e-10,
        "Negative coord on non-periodic axis should not wrap: expected 10.0, got {dist}"
    );

    // Non-zero jimage on partial-PBC: only periodic axes should use the image shift
    let s = Structure::new(
        slab_lattice.clone(),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    // jimage [1, 0, 0] shifts site 1 by +a (periodic): x = 0.5 + 1 = 1.5
    // Distance in x: 1.5 * 10 = 15, y: 0.5 * 10 = 5, z: 0.5 * 10 = 5
    let dist_with_x_shift = s.get_distance_with_image(0, 1, [1, 0, 0]);
    let expected = (15.0_f64.powi(2) + 5.0_f64.powi(2) + 5.0_f64.powi(2)).sqrt();
    assert!(
        (dist_with_x_shift - expected).abs() < 1e-10,
        "jimage shift on periodic x axis: expected {expected}, got {dist_with_x_shift}"
    );

    // jimage [0, 0, 1] shifts site 1 by +c (non-periodic z): z = 0.5 + 1 = 1.5
    // Note: for non-periodic axes, the jimage shift still applies but coords don't wrap
    let dist_with_z_shift = s.get_distance_with_image(0, 1, [0, 0, 1]);
    let expected_z = (5.0_f64.powi(2) + 5.0_f64.powi(2) + 15.0_f64.powi(2)).sqrt();
    assert!(
        (dist_with_z_shift - expected_z).abs() < 1e-10,
        "jimage shift on non-periodic z axis: expected {expected_z}, got {dist_with_z_shift}"
    );
}

#[test]
fn test_is_periodic_image() {
    let lattice = Lattice::cubic(10.0);

    // Same position in different cells (differs by integers)
    let s = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![
            Vector3::new(0.25, 0.35, 0.45),
            Vector3::new(1.25, 2.35, 4.45),
        ],
    );
    assert!(s.is_periodic_image(0, 1, 1e-8));
    assert!(s.is_periodic_image(1, 0, 1e-8)); // Symmetric

    // Tolerance behavior: slight difference
    let s = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![
            Vector3::new(0.25, 0.35, 0.45),
            Vector3::new(1.25, 2.35, 4.46),
        ],
    );
    assert!(!s.is_periodic_image(0, 1, 1e-8)); // Tight: no
    assert!(s.is_periodic_image(0, 1, 0.02)); // Loose: yes

    // Different species -> NOT periodic images
    let s = Structure::new(
        lattice.clone(),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Co)],
        vec![
            Vector3::new(0.25, 0.35, 0.45),
            Vector3::new(1.25, 2.35, 4.45),
        ],
    );
    assert!(!s.is_periodic_image(0, 1, 1e-8));

    // Disordered sites with same dominant species
    let s = Structure::new_from_occupancies(
        lattice,
        vec![
            SiteOccupancy::new(vec![
                (Species::neutral(Element::Fe), 0.6),
                (Species::neutral(Element::Co), 0.4),
            ]),
            SiteOccupancy::new(vec![
                (Species::neutral(Element::Fe), 0.7),
                (Species::neutral(Element::Ni), 0.3),
            ]),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(1.0, 0.0, 0.0)],
    );
    assert!(s.is_periodic_image(0, 1, 1e-8)); // Same dominant species (Fe)

    // Self is own periodic image
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.5, 0.5, 0.5)],
    );
    assert!(s.is_periodic_image(0, 0, 1e-8));

    // Negative tolerance always fails (validated at Python layer, but document Rust behavior)
    assert!(!s.is_periodic_image(0, 0, -1.0));
}

#[test]
fn test_distance_from_point() {
    // Cubic: site at (2.5, 3.5, 4.5) Cartesian
    let s = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.25, 0.35, 0.45)],
    );
    // From origin: sqrt(2.5^2 + 3.5^2 + 4.5^2)
    assert!((s.distance_from_point(0, Vector3::zeros()) - 6.22494979899).abs() < 1e-6);
    // From (1, 1, 1): sqrt((2.5-1)^2 + (3.5-1)^2 + (4.5-1)^2)
    assert!(
        (s.distance_from_point(0, Vector3::new(1.0, 1.0, 1.0)) - 20.75_f64.sqrt()).abs() < 1e-10
    );

    // Same location -> zero distance
    let s = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.1, 0.1, 0.1)], // Cartesian: (1, 1, 1)
    );
    assert!(s.distance_from_point(0, Vector3::new(1.0, 1.0, 1.0)) < 1e-10);

    // Hexagonal: site along c-axis at z=2.5
    let s = Structure::new(
        Lattice::hexagonal(3.0, 5.0),
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::new(0.0, 0.0, 0.5)],
    );
    assert!((s.distance_from_point(0, Vector3::zeros()) - 2.5).abs() < 1e-10);
}

#[test]
fn test_site_labels() {
    let lattice = Lattice::cubic(4.0);

    // Defaults to species string (ordered and with oxidation)
    let s = Structure::new(
        lattice.clone(),
        vec![
            Species::neutral(Element::Fe),
            Species::new(Element::O, Some(-2)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert_eq!(s.site_label(0), "Fe");
    assert_eq!(s.site_label(1), "O2-");

    // Disordered site uses species_string (sorted by electronegativity: Fe < Co)
    let s = Structure::new_from_occupancies(
        lattice.clone(),
        vec![SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ])],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    assert_eq!(s.site_label(0), "Fe:0.5, Co:0.5");

    // Custom labels override defaults
    let mut s = Structure::new(
        lattice.clone(),
        vec![
            Species::neutral(Element::Fe),
            Species::neutral(Element::Co),
            Species::neutral(Element::Ni),
        ],
        vec![
            Vector3::zeros(),
            Vector3::new(0.25, 0.25, 0.25),
            Vector3::new(0.5, 0.5, 0.5),
        ],
    );
    assert_eq!(s.site_labels(), vec!["Fe", "Co", "Ni"]); // Defaults
    s.set_site_label(1, "custom");
    assert_eq!(s.site_labels(), vec!["Fe", "custom", "Ni"]); // Mixed

    // Method chaining and special characters
    let mut s = Structure::new(
        lattice,
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)],
        vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
    );
    s.set_site_label(0, "Fe_oct (site 1)")
        .set_site_label(1, "Fe_tet");
    assert_eq!(s.site_label(0), "Fe_oct (site 1)");
    assert_eq!(s.site_label(1), "Fe_tet");

    // Label persists in properties
    let props = s.site_properties(0);
    assert_eq!(
        props.get("label").unwrap().as_str().unwrap(),
        "Fe_oct (site 1)"
    );
}

#[test]
fn test_species_strings() {
    // Empty structure
    let s = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    assert!(s.species_strings().is_empty());

    // Large structure: all same species
    let n = 100;
    let s = Structure::new(
        Lattice::cubic(10.0),
        (0..n).map(|_| Species::neutral(Element::Cu)).collect(),
        (0..n)
            .map(|idx| {
                Vector3::new(
                    (idx % 10) as f64 / 10.0,
                    ((idx / 10) % 10) as f64 / 10.0,
                    (idx / 100) as f64 / 10.0,
                )
            })
            .collect(),
    );
    let strings = s.species_strings();
    assert_eq!(strings.len(), n);
    assert!(strings.iter().all(|s| s == "Cu"));
}

#[test]
fn test_pbc_image_indices() {
    let lattice = Lattice::cubic(4.0);

    // No wrap: nearby sites in same cell
    let c1 = vec![Vector3::new(0.2, 0.2, 0.2)];
    let c2 = vec![Vector3::new(0.3, 0.3, 0.3)];
    let (_, _, images) = crate::pbc::pbc_shortest_vectors(&lattice, &c1, &c2, None, None);
    assert_eq!(images[0][0], [0, 0, 0]);

    // Negative wrap: 0.1 to 0.9 wraps via -x
    let c1 = vec![Vector3::new(0.1, 0.0, 0.0)];
    let c2 = vec![Vector3::new(0.9, 0.0, 0.0)];
    let (_, d2, images) = crate::pbc::pbc_shortest_vectors(&lattice, &c1, &c2, None, None);
    assert!((d2[0][0].sqrt() - 0.8).abs() < 1e-8); // 0.2 * 4 = 0.8
    assert_eq!(images[0][0][0], -1);

    // Positive wrap: 0.9 to 0.1 wraps via +x
    let c1 = vec![Vector3::new(0.9, 0.0, 0.0)];
    let c2 = vec![Vector3::new(0.1, 0.0, 0.0)];
    let (_, _, images) = crate::pbc::pbc_shortest_vectors(&lattice, &c1, &c2, None, None);
    assert_eq!(images[0][0][0], 1);

    // Corner wrap: all three directions
    let c1 = vec![Vector3::new(0.05, 0.05, 0.05)];
    let c2 = vec![Vector3::new(0.95, 0.95, 0.95)];
    let (_, _, images) = crate::pbc::pbc_shortest_vectors(&lattice, &c1, &c2, None, None);
    assert_eq!(images[0][0], [-1, -1, -1]);

    // Multiple pairs: verify small images for nearby sites
    let c1 = vec![Vector3::new(0.1, 0.1, 0.1), Vector3::new(0.4, 0.4, 0.4)];
    let c2 = vec![Vector3::new(0.2, 0.2, 0.2), Vector3::new(0.3, 0.3, 0.3)];
    let (_, d2, images) = crate::pbc::pbc_shortest_vectors(&lattice, &c1, &c2, None, None);
    for idx in 0..2 {
        for jdx in 0..2 {
            assert!(d2[idx][jdx].sqrt() < 7.0);
            let img = images[idx][jdx];
            assert!(img[0].abs() <= 1 && img[1].abs() <= 1 && img[2].abs() <= 1);
        }
    }
}

#[test]
fn test_comprehensive_distance_verification() {
    // Comprehensive test: verify all distance methods agree
    let lattice = Lattice::cubic(5.0);
    let s = Structure::new(
        lattice,
        vec![Species::neutral(Element::Fe), Species::neutral(Element::Cu)],
        vec![Vector3::new(0.1, 0.2, 0.3), Vector3::new(0.8, 0.9, 0.7)],
    );

    // get_distance should equal sqrt of distance_matrix entry
    let d01 = s.get_distance(0, 1);
    let dm = s.distance_matrix();
    assert!((d01 - dm[0][1]).abs() < 1e-10);
    assert!((d01 - dm[1][0]).abs() < 1e-10); // Symmetric

    // get_distance_and_image should give same distance
    let (d_and_img, img) = s.get_distance_and_image(0, 1);
    assert!((d01 - d_and_img).abs() < 1e-10);

    // Using that image should give same distance
    let d_with_img = s.get_distance_with_image(0, 1, img);
    assert!((d01 - d_with_img).abs() < 1e-10);
}

#[test]
fn test_neighbor_list_bcc_nearest_neighbors() {
    // BCC: each atom has 8 nearest neighbors at distance a*sqrt(3)/2
    let bcc = make_bcc(Element::Fe, 2.87);
    let nn_dist = 2.87 * (3.0_f64).sqrt() / 2.0; // ≈ 2.48 Å

    let (centers, _neighbors, _images, distances) =
        bcc.get_neighbor_list(nn_dist + 0.1, 1e-8, true);

    // Count neighbors for site 0
    let site0_neighbors: Vec<_> = centers
        .iter()
        .zip(&distances)
        .filter(|&(&c, _)| c == 0)
        .collect();

    assert_eq!(
        site0_neighbors.len(),
        8,
        "BCC site 0 should have 8 nearest neighbors, got {}",
        site0_neighbors.len()
    );
}

#[test]
fn test_neighbor_list_hexagonal() {
    // Test with non-cubic lattice
    let lattice = Lattice::hexagonal(3.0, 5.0);
    let s = Structure::new(
        lattice,
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );

    // Find neighbors within lattice parameter distance
    let (centers, _neighbors, _images, distances) = s.get_neighbor_list(3.1, 1e-8, true);

    // Should find some neighbors
    assert!(
        !centers.is_empty(),
        "Should find neighbors in hexagonal lattice"
    );

    // All distances should be positive and <= cutoff
    for d in &distances {
        assert!(
            *d > 0.0 && *d <= 3.1,
            "Distance {} should be in (0, 3.1]",
            d
        );
    }
}

// === SymmOp and apply_operation tests ===

#[test]
fn test_symmop_constructors() {
    // Identity: I, [0,0,0]
    let op = SymmOp::identity();
    assert_eq!(op.rotation, Matrix3::identity());
    assert_eq!(op.translation, Vector3::zeros());

    // Inversion: -I, [0,0,0]
    let op = SymmOp::inversion();
    assert_eq!(op.rotation, -Matrix3::identity());
    assert_eq!(op.translation, Vector3::zeros());

    // Translation: I, [0.5,0.25,0]
    let v = Vector3::new(0.5, 0.25, 0.0);
    let op = SymmOp::translation(v);
    assert_eq!(op.rotation, Matrix3::identity());
    assert_eq!(op.translation, v);

    // Rotation_z(90°): (1,0,0) -> (0,1,0)
    use std::f64::consts::FRAC_PI_2;
    let op = SymmOp::rotation_z(FRAC_PI_2);
    let rotated = op.rotation * Vector3::new(1.0, 0.0, 0.0);
    assert!((rotated - Vector3::new(0.0, 1.0, 0.0)).norm() < 1e-10);
}

#[test]
fn test_apply_operation_fractional() {
    // Identity: coords unchanged
    let original = make_cu_at(0.25, 0.25, 0.25);
    let transformed = original.apply_operation_copy(&SymmOp::identity(), true);
    assert!((transformed.frac_coords[0] - original.frac_coords[0]).norm() < 1e-10);

    // Inversion: (0.25, 0.25, 0.25) -> (-0.25, -0.25, -0.25)
    let inverted = original.apply_operation_copy(&SymmOp::inversion(), true);
    assert!((inverted.frac_coords[0] - Vector3::new(-0.25, -0.25, -0.25)).norm() < 1e-10);

    // Translation: (0,0,0) + (0.5,0,0) = (0.5, 0, 0)
    let translated = make_cu_at(0.0, 0.0, 0.0)
        .apply_operation_copy(&SymmOp::translation(Vector3::new(0.5, 0.0, 0.0)), true);
    assert!((translated.frac_coords[0] - Vector3::new(0.5, 0.0, 0.0)).norm() < 1e-10);
}

#[test]
fn test_apply_operation_cartesian() {
    use std::f64::consts::FRAC_PI_2;
    // 90° rotation around z-axis: (0.25,0,0) frac -> (1,0,0) Å -> (0,1,0) Å -> (0,0.25,0) frac
    let rotated =
        make_cu_at(0.25, 0.0, 0.0).apply_operation_copy(&SymmOp::rotation_z(FRAC_PI_2), false);
    assert!((rotated.frac_coords[0] - Vector3::new(0.0, 0.25, 0.0)).norm() < 1e-10);
}

#[test]
fn test_apply_operation_in_place_and_chaining() {
    // In-place translation
    let mut s = make_cu_at(0.0, 0.0, 0.0);
    s.apply_operation(&SymmOp::translation(Vector3::new(0.5, 0.5, 0.5)), true);
    assert!((s.frac_coords[0] - Vector3::new(0.5, 0.5, 0.5)).norm() < 1e-10);

    // Chaining: translate then invert
    let mut s = make_cu_at(0.0, 0.0, 0.0);
    s.apply_operation(&SymmOp::translation(Vector3::new(0.25, 0.0, 0.0)), true)
        .apply_operation(&SymmOp::inversion(), true);
    assert!((s.frac_coords[0] - Vector3::new(-0.25, 0.0, 0.0)).norm() < 1e-10);
}

#[test]
fn test_apply_operation_preserves_sites() {
    let nacl = make_nacl();
    let transformed = nacl.apply_operation_copy(&SymmOp::inversion(), true);
    assert_eq!(transformed.num_sites(), nacl.num_sites());
    assert_eq!(transformed.species()[0].element, nacl.species()[0].element);
}

// === Physical Properties Tests (volume, total_mass, density) ===

#[test]
fn test_volume() {
    // Cubic cell: 4^3 = 64 Å³
    assert!((make_cu_at(0.0, 0.0, 0.0).volume() - 64.0).abs() < 1e-10);
    // Structure.volume() should delegate to Lattice.volume()
    let nacl = make_nacl();
    assert!((nacl.volume() - nacl.lattice.volume()).abs() < 1e-10);
}

#[test]
fn test_total_mass() {
    // NaCl: Na (22.99) + Cl (35.45) ≈ 58.44 u
    assert!((make_nacl().total_mass() - 58.44).abs() < 0.1);
    // FCC Cu: 4 atoms * 63.546 ≈ 254.18 u
    assert!((make_fcc_conventional(Element::Cu, 3.6).total_mass() - 254.18).abs() < 0.1);
}

#[test]
fn test_total_mass_disordered() {
    // 50% Fe (55.845) + 50% Co (58.933) = 57.389 u
    let s = Structure::new_from_occupancies(
        Lattice::cubic(2.87),
        vec![SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.5),
            (Species::neutral(Element::Co), 0.5),
        ])],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    assert!((s.total_mass() - 57.389).abs() < 0.01);
}

#[test]
fn test_density() {
    // FCC Cu: a=3.615Å, 4 atoms → ~8.94 g/cm³
    let fcc = make_fcc_conventional(Element::Cu, 3.615);
    assert!((fcc.density().unwrap() - 8.94).abs() < 0.1);
    // NaCl primitive: ~0.54 g/cm³
    let nacl = make_nacl();
    let nacl_density = nacl.density().unwrap();
    assert!(nacl_density > 0.5 && nacl_density < 0.6);
    // 1 Cu in 1 Å³ → ~105.5 g/cm³
    let tiny = make_cu_cubic(1.0);
    assert!((tiny.density().unwrap() - 105.5).abs() < 1.0);
}

// === Site Manipulation Tests (translate_sites, perturb) ===

#[test]
fn test_translate_sites() {
    // Single site, fractional coords
    let mut s = make_nacl();
    s.translate_sites(&[0], Vector3::new(0.1, 0.0, 0.0), true);
    assert!((s.frac_coords[0][0] - 0.1).abs() < 1e-10);
    assert!((s.frac_coords[1] - Vector3::new(0.5, 0.5, 0.5)).norm() < 1e-10); // unchanged

    // Multiple sites
    let mut s = make_nacl();
    s.translate_sites(&[0, 1], Vector3::new(0.1, 0.0, 0.0), true);
    assert!((s.frac_coords[0][0] - 0.1).abs() < 1e-10);
    assert!((s.frac_coords[1][0] - 0.6).abs() < 1e-10);

    // Cartesian coords: 2Å on 4Å lattice = 0.5 fractional
    let mut s = make_cu_at(0.0, 0.0, 0.0);
    s.translate_sites(&[0], Vector3::new(2.0, 0.0, 0.0), false);
    assert!((s.frac_coords[0][0] - 0.5).abs() < 1e-10);

    // Chaining
    let mut s = make_nacl();
    s.translate_sites(&[0], Vector3::new(0.1, 0.0, 0.0), true)
        .translate_sites(&[0], Vector3::new(0.0, 0.1, 0.0), true);
    assert!((s.frac_coords[0][0] - 0.1).abs() < 1e-10);
    assert!((s.frac_coords[0][1] - 0.1).abs() < 1e-10);
}

#[test]
#[should_panic(expected = "out of bounds")]
fn test_translate_sites_out_of_bounds() {
    make_nacl().translate_sites(&[10], Vector3::new(0.1, 0.0, 0.0), true);
}

#[test]
fn test_perturb_reproducibility() {
    // Same seed → same result
    let mut s1 = make_nacl();
    let mut s2 = make_nacl();
    s1.perturb(0.1, None, Some(42));
    s2.perturb(0.1, None, Some(42));
    for (fc1, fc2) in s1.frac_coords.iter().zip(&s2.frac_coords) {
        assert!((fc1 - fc2).norm() < 1e-10);
    }
    // Different seeds → different results
    let mut s3 = make_nacl();
    s3.perturb(0.1, None, Some(43));
    assert!(
        s1.frac_coords
            .iter()
            .zip(&s3.frac_coords)
            .any(|(a, b)| (a - b).norm() > 1e-10)
    );
}

#[test]
fn test_perturb_distance_range() {
    let orig = make_nacl();
    let mut perturbed = orig.clone();
    perturbed.perturb(0.5, Some(0.2), Some(123));
    for (orig_c, pert_c) in orig.cart_coords().iter().zip(&perturbed.cart_coords()) {
        let dist = (orig_c - pert_c).norm();
        assert!(
            (0.2 - 1e-6..=0.5 + 1e-6).contains(&dist),
            "dist {dist} out of [0.2, 0.5]"
        );
    }
}

#[test]
fn test_perturb_all_sites_moved() {
    let orig = make_nacl();
    let mut perturbed = orig.clone();
    perturbed.perturb(0.1, Some(0.05), Some(42));
    for (orig_fc, pert_fc) in orig.frac_coords.iter().zip(&perturbed.frac_coords) {
        assert!((orig_fc - pert_fc).norm() > 1e-10, "site should have moved");
    }
}

#[test]
fn test_perturb_zero_distance() {
    let orig = make_nacl();
    let mut perturbed = orig.clone();
    perturbed.perturb(0.0, None, Some(42));
    for (orig_fc, pert_fc) in orig.frac_coords.iter().zip(&perturbed.frac_coords) {
        assert!(
            (orig_fc - pert_fc).norm() < 1e-10,
            "zero perturb should not move sites"
        );
    }
}

#[test]
fn test_perturb_chaining() {
    let mut s = make_nacl();
    s.perturb(0.1, None, Some(42)).perturb(0.1, None, Some(43));
    assert_eq!(s.num_sites(), 2);
}

#[test]
#[should_panic(expected = "must be >=")]
fn test_perturb_invalid_range() {
    make_nacl().perturb(0.1, Some(0.5), None); // min > max
}

// === Sorting tests ===

#[test]
fn test_sort_by_atomic_number() {
    // Test sorting by Z: Fe(26), O(8), H(1) -> H, O, Fe
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::Fe),
            Species::neutral(Element::O),
            Species::neutral(Element::H),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.0, 0.0),
            Vector3::new(0.0, 0.5, 0.0),
        ],
    );

    // Ascending: H < O < Fe
    let asc = s.get_sorted_structure(false);
    assert_eq!(asc.species()[0].element, Element::H);
    assert_eq!(asc.species()[1].element, Element::O);
    assert_eq!(asc.species()[2].element, Element::Fe);

    // Descending: Fe > O > H
    let desc = s.get_sorted_structure(true);
    assert_eq!(desc.species()[0].element, Element::Fe);
    assert_eq!(desc.species()[2].element, Element::H);
}

#[test]
fn test_sort_by_electronegativity() {
    // Na (0.93) < Fe (1.83) < O (3.44)
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::O),
            Species::neutral(Element::Na),
            Species::neutral(Element::Fe),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.0, 0.0),
            Vector3::new(0.0, 0.5, 0.0),
        ],
    );

    let sorted = s.get_sorted_by_electronegativity(false);
    assert_eq!(sorted.species()[0].element, Element::Na);
    assert_eq!(sorted.species()[1].element, Element::Fe);
    assert_eq!(sorted.species()[2].element, Element::O);
}

#[test]
fn test_sort_in_place_preserves_coords() {
    // Coords should follow their species when sorted
    let mut s = Structure::new(
        Lattice::cubic(5.0),
        vec![Species::neutral(Element::Fe), Species::neutral(Element::H)],
        vec![Vector3::new(0.1, 0.2, 0.3), Vector3::new(0.4, 0.5, 0.6)],
    );
    s.sort(false); // H should come first

    assert_eq!(s.species()[0].element, Element::H);
    assert!((s.frac_coords[0] - Vector3::new(0.4, 0.5, 0.6)).norm() < 1e-10);
    assert_eq!(s.species()[1].element, Element::Fe);
    assert!((s.frac_coords[1] - Vector3::new(0.1, 0.2, 0.3)).norm() < 1e-10);
}

#[test]
fn test_sort_noble_gas_last() {
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::Ar), // No EN
            Species::neutral(Element::Na), // EN = 0.93
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let sorted = s.get_sorted_by_electronegativity(false);
    assert_eq!(sorted.species()[0].element, Element::Na);
    assert_eq!(sorted.species()[1].element, Element::Ar);
}

#[test]
fn test_sort_empty_structure() {
    let mut s = Structure::new(Lattice::cubic(5.0), vec![], vec![]);
    s.sort(false);
    assert_eq!(s.num_sites(), 0);
}

#[test]
fn test_sort_disordered_uses_dominant() {
    let site_occ = vec![
        SiteOccupancy::ordered(Species::neutral(Element::Cu)), // Z=29
        SiteOccupancy::new(vec![
            (Species::neutral(Element::Fe), 0.6), // Z=26, dominant
            (Species::neutral(Element::Co), 0.4), // Z=27
        ]),
    ];
    let s = Structure::new_from_occupancies(
        Lattice::cubic(5.0),
        site_occ,
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let sorted = s.get_sorted_structure(false);
    assert_eq!(sorted.species()[0].element, Element::Fe);
    assert_eq!(sorted.species()[1].element, Element::Cu);
}

// === Copy and sanitization tests ===

#[test]
fn test_copy() {
    // Without sanitize: exact clone
    let nacl = make_nacl();
    let copy = nacl.copy(false);
    assert_eq!(copy.num_sites(), nacl.num_sites());
    for (orig, copied) in nacl.frac_coords.iter().zip(&copy.frac_coords) {
        assert!((orig - copied).norm() < 1e-10);
    }

    // With sanitize: sorts by electronegativity (H < O)
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![Species::neutral(Element::O), Species::neutral(Element::H)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    let sanitized = s.copy(true);
    assert_eq!(sanitized.species()[0].element, Element::H);
    assert_eq!(sanitized.species()[1].element, Element::O);
}

#[test]
fn test_copy_with_properties() {
    let s = make_nacl();
    let props = HashMap::from([
        ("energy".to_string(), serde_json::json!(-5.5)),
        ("source".to_string(), serde_json::json!("test")),
    ]);

    let copy = s.copy_with_properties(props);

    assert_eq!(
        copy.properties.get("energy"),
        Some(&serde_json::json!(-5.5))
    );
    assert_eq!(
        copy.properties.get("source"),
        Some(&serde_json::json!("test"))
    );
}

#[test]
fn test_wrap_to_unit_cell() {
    // (1.5, -0.3, 2.7) -> (0.5, 0.7, 0.7)
    let mut s = make_cu_at(1.5, -0.3, 2.7);
    s.wrap_to_unit_cell();
    assert!((s.frac_coords[0] - Vector3::new(0.5, 0.7, 0.7)).norm() < 1e-10);

    // Already in [0,1) should be unchanged
    let mut s = make_cu_at(0.25, 0.5, 0.75);
    let orig = s.frac_coords[0];
    s.wrap_to_unit_cell();
    assert!((s.frac_coords[0] - orig).norm() < 1e-10);
}

#[test]
fn test_wrap_to_unit_cell_respects_pbc() {
    // Non-periodic structure (molecule) - coordinates should not be wrapped
    let mut molecule = Structure::try_new_full(
        Lattice::cubic(10.0),
        vec![SiteOccupancy::ordered(Species::neutral(Element::C))],
        vec![Vector3::new(1.5, -0.3, 2.7)], // outside [0,1)
        [false, false, false],              // molecule: no periodicity
        0.0,
        HashMap::new(),
    )
    .unwrap();
    molecule.wrap_to_unit_cell();
    // Coordinates should remain unchanged for non-periodic structure
    assert!(
        (molecule.frac_coords[0] - Vector3::new(1.5, -0.3, 2.7)).norm() < 1e-10,
        "Molecule coords should not be wrapped"
    );

    // Partial periodicity (slab: periodic in x,y but not z)
    let mut slab = Structure::try_new_full(
        Lattice::cubic(10.0),
        vec![SiteOccupancy::ordered(Species::neutral(Element::C))],
        vec![Vector3::new(1.5, -0.3, 2.7)],
        [true, true, false], // slab: periodic in xy, not z
        0.0,
        HashMap::new(),
    )
    .unwrap();
    slab.wrap_to_unit_cell();
    // x,y should be wrapped but z should remain unchanged
    assert!(
        (slab.frac_coords[0][0] - 0.5).abs() < 1e-10,
        "x should wrap to 0.5"
    );
    assert!(
        (slab.frac_coords[0][1] - 0.7).abs() < 1e-10,
        "y should wrap to 0.7"
    );
    assert!(
        (slab.frac_coords[0][2] - 2.7).abs() < 1e-10,
        "z should NOT wrap (not periodic)"
    );
}

#[test]
fn test_reduced_structure_errors_for_partial_pbc() {
    // Molecule (fully non-periodic) should error on lattice reduction
    let molecule = Structure::try_new_full(
        Lattice::cubic(10.0),
        vec![SiteOccupancy::ordered(Species::neutral(Element::C))],
        vec![Vector3::new(0.5, 0.5, 0.5)],
        [false, false, false], // molecule
        0.0,
        HashMap::new(),
    )
    .unwrap();

    let result = molecule.get_reduced_structure(ReductionAlgo::Niggli);
    assert!(result.is_err(), "Should error for molecule");
    let err_msg = result.unwrap_err().to_string();
    assert!(
        err_msg.contains("fully periodic"),
        "Error should mention fully periodic: {err_msg}"
    );

    // Slab (partial periodicity) should also error - reduction could mix axes
    let slab = Structure::try_new_full(
        Lattice::cubic(10.0),
        vec![SiteOccupancy::ordered(Species::neutral(Element::C))],
        vec![Vector3::new(0.5, 0.5, 0.5)],
        [true, true, false], // slab: periodic in xy, vacuum in z
        0.0,
        HashMap::new(),
    )
    .unwrap();

    let result_slab = slab.get_reduced_structure(ReductionAlgo::Niggli);
    assert!(result_slab.is_err(), "Should error for slab (partial PBC)");

    let result_slab_lll = slab.get_reduced_structure(ReductionAlgo::LLL);
    assert!(
        result_slab_lll.is_err(),
        "Should also error for LLL on slab"
    );

    // Wire (1D periodic) should also error
    let wire = Structure::try_new_full(
        Lattice::cubic(10.0),
        vec![SiteOccupancy::ordered(Species::neutral(Element::C))],
        vec![Vector3::new(0.5, 0.5, 0.5)],
        [true, false, false], // wire: periodic only in x
        0.0,
        HashMap::new(),
    )
    .unwrap();

    let result_wire = wire.get_reduced_structure(ReductionAlgo::Niggli);
    assert!(result_wire.is_err(), "Should error for wire (1D PBC)");
}

#[test]
fn test_sort_method_chaining() {
    let mut s = Structure::new(
        Lattice::cubic(5.0),
        vec![Species::neutral(Element::O), Species::neutral(Element::H)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    s.sort(false).wrap_to_unit_cell();

    assert_eq!(s.species()[0].element, Element::H);
    assert_eq!(s.species()[1].element, Element::O);
}

#[test]
fn test_get_reduced_structure() {
    // Test LLL on cubic NaCl
    let nacl = make_nacl();
    let lll = nacl.get_reduced_structure(ReductionAlgo::LLL).unwrap();
    assert!((lll.lattice.volume() - nacl.lattice.volume()).abs() < 1e-6);
    assert_eq!(lll.num_sites(), nacl.num_sites());

    // Test Niggli on skewed lattice
    let skewed = Structure::new(
        Lattice::new(Matrix3::new(4.0, 2.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 4.0)),
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::new(0.25, 0.25, 0.25)],
    );
    let niggli = skewed.get_reduced_structure(ReductionAlgo::Niggli).unwrap();
    assert!((niggli.lattice.volume() - skewed.lattice.volume()).abs() < 1e-6);
}

// === interpolate() tests ===

#[test]
fn test_interpolate_identical_structures() {
    let s = make_nacl();
    let images = s.interpolate(&s, 5, false, true).unwrap();
    assert_eq!(images.len(), 6);

    for img in &images {
        for (orig, interp) in s.frac_coords.iter().zip(&img.frac_coords) {
            assert!(
                (orig - interp).norm() < 1e-10,
                "Identical structure interpolation should produce same coords"
            );
        }
    }
}

#[test]
fn test_interpolate_linear_displacement() {
    let images = make_cu_at(0.0, 0.0, 0.0)
        .interpolate(&make_cu_at(0.5, 0.0, 0.0), 4, false, false)
        .unwrap();
    assert_eq!(images.len(), 5);
    for (idx, img) in images.iter().enumerate() {
        let expected = 0.5 * idx as f64 / 4.0;
        assert!(
            (img.frac_coords[0][0] - expected).abs() < 1e-10,
            "Image {idx}"
        );
    }
}

#[test]
fn test_interpolate_pbc() {
    // 0.9→0.1 crosses boundary with PBC, goes through 0.5 without
    let (start, end) = (make_cu_at(0.9, 0.0, 0.0), make_cu_at(0.1, 0.0, 0.0));
    let mid_pbc = start.interpolate(&end, 4, false, true).unwrap()[2].frac_coords[0][0];
    let mid_no_pbc = start.interpolate(&end, 4, false, false).unwrap()[2].frac_coords[0][0];
    assert!(
        !(0.2..=0.8).contains(&mid_pbc),
        "PBC: middle should be near boundary"
    );
    assert!(
        (mid_no_pbc - 0.5).abs() < 0.1,
        "No PBC: middle should be ~0.5"
    );

    // 0.3→0.8 (diff=0.5) - distinguishes round() from floor()
    let mid = make_cu_at(0.3, 0.0, 0.0)
        .interpolate(&make_cu_at(0.8, 0.0, 0.0), 4, false, true)
        .unwrap()[2]
        .frac_coords[0][0];
    assert!(
        !(0.15..=0.85).contains(&mid),
        "0.3→0.8 with PBC should cross boundary"
    );
}

#[test]
fn test_interpolate_errors() {
    let nacl = make_nacl();

    // Different site counts
    let cu_fcc = make_fcc_conventional(Element::Cu, 3.6);
    let err = nacl.interpolate(&cu_fcc, 5, false, true).unwrap_err();
    assert!(
        err.to_string().contains("different number"),
        "Expected site count error"
    );

    // Species mismatch (same site count, different elements)
    let kcl = make_rocksalt(Element::K, Element::Cl, 6.29);
    let err = nacl.interpolate(&kcl, 5, false, true).unwrap_err();
    assert!(
        err.to_string().contains("Species mismatch"),
        "Expected species error"
    );

    // Periodicity mismatch
    let mut mol = nacl.clone();
    mol.set_pbc([false, false, false]);
    let err = nacl.interpolate(&mol, 5, false, true).unwrap_err();
    assert!(
        err.to_string().contains("different periodicity"),
        "Expected pbc mismatch error"
    );

    // Charge mismatch
    let mut charged = nacl.clone();
    charged.charge = 1.0;
    let err = nacl.interpolate(&charged, 5, false, true).unwrap_err();
    assert!(
        err.to_string().contains("different charges"),
        "Expected charge mismatch error"
    );
}

#[test]
fn test_interpolate_lattice() {
    let images = make_cu_cubic(4.0)
        .interpolate(&make_cu_cubic(5.0), 4, true, false)
        .unwrap();

    // Check endpoints and middle
    let get_a = |idx: usize| images[idx].lattice.lengths()[0];
    assert!((get_a(0) - 4.0).abs() < 1e-6, "First should be 4.0");
    assert!((get_a(2) - 4.5).abs() < 1e-6, "Middle should be 4.5");
    assert!((get_a(4) - 5.0).abs() < 1e-6, "Last should be 5.0");

    // Verify monotonic increase
    for idx in 1..images.len() {
        assert!(get_a(idx) >= get_a(idx - 1), "Lattice should increase");
    }
}

#[test]
fn test_interpolate_edge_cases() {
    // n_images=0 returns just start structure
    let nacl = make_nacl();
    let images = nacl.interpolate(&nacl, 0, false, true).unwrap();
    assert_eq!(images.len(), 1);

    // Empty structures work
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    let images = empty.interpolate(&empty, 5, false, true).unwrap();
    assert_eq!(images.len(), 6);
    assert!(images.iter().all(|img| img.num_sites() == 0));
}

// === matches() and matches_with() tests ===

#[test]
fn test_matches() {
    let nacl = make_nacl();

    // Self-match (exact and anonymous)
    assert!(nacl.matches(&nacl, false), "Structure should match itself");
    assert!(nacl.matches(&nacl, true), "Anonymous self-match");

    // Different composition - no exact match
    let kcl = make_rocksalt(Element::K, Element::Cl, 6.29);
    assert!(
        !nacl.matches(&kcl, false),
        "Different compositions shouldn't match"
    );

    // Same prototype (rocksalt) - anonymous match
    let mgo = Structure::new(
        Lattice::cubic(4.21),
        vec![Species::neutral(Element::Mg), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );
    assert!(nacl.matches(&mgo, true), "NaCl/MgO same prototype");

    // BCC prototype: Fe vs W
    let fe_bcc = make_bcc(Element::Fe, 2.87);
    let w_bcc = make_bcc(Element::W, 3.16);
    assert!(!fe_bcc.matches(&w_bcc, false));
    assert!(fe_bcc.matches(&w_bcc, true), "BCC prototype match");

    // FCC prototype: Cu vs Al
    let cu_fcc = make_fcc_conventional(Element::Cu, 3.6);
    let al_fcc = make_fcc_conventional(Element::Al, 4.05);
    assert!(!cu_fcc.matches(&al_fcc, false));
    assert!(cu_fcc.matches(&al_fcc, true), "FCC prototype match");
}

// === Supercell Tests ===

#[test]
fn test_supercell_scaling() {
    // Test various scaling methods: matrix, diag, and operators
    let nacl = make_nacl(); // 2 sites
    let orig_vol = nacl.lattice.volume();

    // (description, supercell, expected_sites, volume_factor)
    let cases: [(&str, Structure, usize, f64); 5] = [
        (
            "2x2x2 matrix",
            nacl.make_supercell([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
                .unwrap(),
            16,
            8.0,
        ),
        ("diag [2,3,1]", nacl.make_supercell_diag([2, 3, 1]), 12, 6.0),
        ("* 2 operator", &nacl * 2, 16, 8.0),
        ("* [3,1,2] operator", &nacl * [3, 1, 2], 12, 6.0),
        (
            "sheared [[2,1,0],[0,1,0],[0,0,1]]",
            nacl.make_supercell([[2, 1, 0], [0, 1, 0], [0, 0, 1]])
                .unwrap(),
            4,
            2.0,
        ),
    ];

    for (desc, super_s, exp_sites, vol_factor) in cases {
        assert_eq!(super_s.num_sites(), exp_sites, "{desc}: wrong site count");
        assert!(
            (super_s.lattice.volume() - orig_vol * vol_factor).abs() < 1e-6,
            "{desc}: volume should scale by {vol_factor}"
        );
    }

    // Verify composition scales correctly (2x2x2)
    let super_nacl = &nacl * 2;
    assert_eq!(super_nacl.composition().get(Element::Na), 8.0);
    assert_eq!(super_nacl.composition().get(Element::Cl), 8.0);

    // FCC conventional: 4 atoms -> 2x2x2 = 32
    let fcc = make_fcc_conventional(Element::Cu, 3.6);
    assert_eq!(fcc.make_supercell_diag([2, 2, 2]).num_sites(), 32);

    // Verify coordinates are distinct (atoms distributed, not clustered at same positions)
    // For 16 sites in 2x2x2 supercell, all coords should be unique
    let fc = &super_nacl.frac_coords;
    let n_unique = fc
        .iter()
        .map(|c| format!("{:.6},{:.6},{:.6}", c[0], c[1], c[2]))
        .collect::<std::collections::HashSet<_>>()
        .len();
    assert_eq!(
        n_unique, 16,
        "2x2x2 supercell should have 16 unique positions, got {n_unique}"
    );
}

#[test]
fn test_supercell_monoclinic_lattice_vectors() {
    // Verify matrix multiplication order with non-cubic lattice
    let mono = Structure::new(
        Lattice::from_parameters(3.0, 4.0, 5.0, 90.0, 100.0, 90.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    let mono_super = mono
        .make_supercell([[2, 0, 0], [0, 1, 0], [0, 0, 1]])
        .unwrap();

    // 2x1x1: new a-vector should be 2x original
    let orig = mono.lattice.matrix().row(0);
    let new = mono_super.lattice.matrix().row(0);
    for idx in 0..3 {
        assert!(
            (new[idx] - 2.0 * orig[idx]).abs() < 1e-6,
            "a-vector[{idx}] mismatch"
        );
    }
}

#[test]
fn test_supercell_zero_det_error() {
    let result = make_nacl().make_supercell([[1, 0, 0], [1, 0, 0], [0, 0, 1]]);
    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("zero determinant"));
}

#[test]
fn test_supercell_negative_diagonal() {
    // Negative diagonal values create mirror transforms
    // The supercell should still have correct site count and volume
    let nacl = make_nacl();
    let orig_vol = nacl.lattice.volume();

    // Test negative scaling: -2 x 1 x 1 (mirror along a-axis, doubled)
    let super_neg = nacl
        .make_supercell([[-2, 0, 0], [0, 1, 0], [0, 0, 1]])
        .unwrap();
    assert_eq!(super_neg.num_sites(), 4, "Should have 4 sites");
    assert!(
        (super_neg.lattice.volume().abs() - orig_vol * 2.0).abs() < 1e-6,
        "Volume should double (may be negative for mirror)"
    );

    // Verify behavior matches general algorithm by comparing with non-diagonal
    // that produces same result: [[-2,0,0],[0,1,0],[0,0,1]] vs general path
    let super_gen = nacl
        .make_supercell([[-2, 0, 0], [0, 1, 0], [0, 0, 1]])
        .unwrap();
    assert_eq!(super_neg.num_sites(), super_gen.num_sites());
}

#[test]
fn test_supercell_preserves_site_properties() {
    // Create a structure with site properties
    let lattice = Lattice::cubic(4.0);
    let species = Species::neutral(Element::Fe);

    let mut props = HashMap::new();
    props.insert("magmom".to_string(), serde_json::json!(2.5));
    props.insert("label".to_string(), serde_json::json!("Fe1"));

    let site_occ = SiteOccupancy::with_properties(vec![(species, 1.0)], props);
    let s = Structure::try_new_from_occupancies(
        lattice,
        vec![site_occ],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
    .unwrap();

    // Make 2x2x2 supercell
    let super_cell = s.make_supercell_diag([2, 2, 2]);
    assert_eq!(super_cell.num_sites(), 8);

    // Each site should have the original properties plus orig_site_idx
    for idx in 0..8 {
        let props = super_cell.site_properties(idx);

        // Original properties preserved
        assert_eq!(props.get("magmom").and_then(|v| v.as_f64()), Some(2.5));
        assert_eq!(props.get("label").and_then(|v| v.as_str()), Some("Fe1"));

        // orig_site_idx should be 0 (only one original site)
        assert_eq!(
            props.get("orig_site_idx").and_then(|v| v.as_u64()),
            Some(0),
            "Site {idx} missing orig_site_idx"
        );
    }
}

#[test]
fn test_supercell_orig_site_idx_multiple_sites() {
    // Test with multiple original sites
    let nacl = make_nacl(); // 2 sites: Na at 0,0,0 and Cl at 0.5,0.5,0.5

    // Make 2x1x1 supercell
    let super_cell = nacl.make_supercell_diag([2, 1, 1]);
    assert_eq!(super_cell.num_sites(), 4);

    // Should have 2 sites from orig_site_idx 0 and 2 from orig_site_idx 1
    let orig_indices: Vec<u64> = (0..4)
        .map(|idx| {
            super_cell
                .site_properties(idx)
                .get("orig_site_idx")
                .and_then(|v| v.as_u64())
                .expect("Missing orig_site_idx")
        })
        .collect();

    assert_eq!(orig_indices.iter().filter(|&&x| x == 0).count(), 2);
    assert_eq!(orig_indices.iter().filter(|&&x| x == 1).count(), 2);
}

#[test]
fn test_supercell_nested_preserves_orig_site_idx() {
    // Test that nested supercells preserve the original site index
    let lattice = Lattice::cubic(4.0);
    let species = Species::neutral(Element::Fe);
    let site_occ = SiteOccupancy::ordered(species);
    let s = Structure::try_new_from_occupancies(
        lattice,
        vec![site_occ],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
    .unwrap();

    // First supercell: 2x1x1
    let super1 = s.make_supercell_diag([2, 1, 1]);
    assert_eq!(super1.num_sites(), 2);

    // All sites should have orig_site_idx = 0 (from original structure)
    for idx in 0..2 {
        assert_eq!(
            super1
                .site_properties(idx)
                .get("orig_site_idx")
                .and_then(|v| v.as_u64()),
            Some(0)
        );
    }

    // Second supercell of the first: 1x2x1
    let super2 = super1.make_supercell_diag([1, 2, 1]);
    assert_eq!(super2.num_sites(), 4);

    // All sites should STILL have orig_site_idx = 0 (preserved from first supercell)
    for idx in 0..4 {
        assert_eq!(
            super2
                .site_properties(idx)
                .get("orig_site_idx")
                .and_then(|v| v.as_u64()),
            Some(0),
            "Site {idx} should preserve original orig_site_idx"
        );
    }
}

#[test]
fn test_reduced_structure_wraps_coords() {
    let reduced = make_cu_at(1.5, -0.3, 0.8) // outside [0,1)
        .get_reduced_structure(ReductionAlgo::Niggli)
        .unwrap();
    for &c in reduced.frac_coords[0].iter() {
        assert!((0.0..1.0).contains(&c), "coord {c} not in [0,1)");
    }
}

// === Slab Generation Tests ===

#[test]
fn test_reduce_miller_indices() {
    let cases: [([i32; 3], [i32; 3]); 14] = [
        // Already reduced
        ([1, 0, 0], [1, 0, 0]),
        ([1, 1, 1], [1, 1, 1]),
        // Needs reduction
        ([2, 0, 0], [1, 0, 0]),
        ([2, 2, 2], [1, 1, 1]),
        ([4, 2, 6], [2, 1, 3]),
        ([6, 9, 12], [2, 3, 4]),
        // Negatives
        ([-2, 0, 0], [-1, 0, 0]),
        ([2, -4, 2], [1, -2, 1]),
        ([-3, -6, -9], [-1, -2, -3]),
        // Zeros
        ([0, 0, 0], [0, 0, 0]),
        ([0, 2, 0], [0, 1, 0]),
        ([0, 0, 4], [0, 0, 1]),
        // Mixed
        ([1, 2, 3], [1, 2, 3]),
        ([-1, 1, 0], [-1, 1, 0]),
    ];

    for (input, expected) in cases {
        assert_eq!(
            reduce_miller_indices(input),
            expected,
            "reduce({:?})",
            input
        );
    }
}

#[test]
fn test_slab_transformation_nonsingular() {
    let det3 = |m: [[i32; 3]; 3]| {
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    };

    let cubic = Lattice::cubic(4.0);
    for hkl in [
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [1, 1, 1],
        [2, 1, 0],
        [3, 1, 1],
    ] {
        assert!(
            det3(get_slab_transformation(&cubic, hkl)) != 0,
            "{:?} singular",
            hkl
        );
    }
}

#[test]
fn test_compute_d_spacing() {
    let a = 4.0;
    let cubic = Lattice::cubic(a);

    // d(hkl) = a / sqrt(h² + k² + l²)
    for (hkl, divisor) in [
        ([1, 0, 0], 1.0),
        ([1, 1, 0], 2.0_f64.sqrt()),
        ([1, 1, 1], 3.0_f64.sqrt()),
        ([2, 0, 0], 2.0),
        ([2, 1, 1], 6.0_f64.sqrt()),
    ] {
        let d = compute_d_spacing(&cubic, hkl);
        assert!((d - a / divisor).abs() < 1e-10, "d{:?}", hkl);
    }

    // Tetragonal: d(001)=c, d(100)=a
    let tetra = Lattice::tetragonal(4.0, 6.0);
    assert!((compute_d_spacing(&tetra, [0, 0, 1]) - 6.0).abs() < 1e-10);
    assert!((compute_d_spacing(&tetra, [1, 0, 0]) - 4.0).abs() < 1e-10);
}

#[test]
fn test_identify_layer_positions() {
    // Empty
    assert!(identify_layer_positions(&[], 0.01).is_empty());

    // Single layer
    let single = vec![Vector3::new(0.0, 0.0, 0.5), Vector3::new(0.5, 0.5, 0.5)];
    let layers = identify_layer_positions(&single, 0.01);
    assert_eq!(layers.len(), 1);
    assert!((layers[0] - 0.5).abs() < 1e-10);

    // Multiple layers
    let multi = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.0, 0.0, 0.33),
        Vector3::new(0.0, 0.0, 0.67),
    ];
    assert_eq!(identify_layer_positions(&multi, 0.05).len(), 3);

    // Tolerance sensitivity: [0.0, 0.02, 0.04]
    let chain = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.0, 0.0, 0.02),
        Vector3::new(0.0, 0.0, 0.04),
    ];
    assert_eq!(identify_layer_positions(&chain, 0.05).len(), 1); // large tol = 1 layer
    assert_eq!(identify_layer_positions(&chain, 0.01).len(), 3); // small tol = 3 layers
}

#[test]
fn test_slab_config() {
    // Default values
    let def = SlabConfig::default();
    assert_eq!(def.miller_index, [1, 0, 0]);
    assert_eq!(def.min_slab_size, 10.0);
    assert!(def.center_slab);

    // Builder
    let cfg = SlabConfig::new([1, 1, 0])
        .with_min_slab_size(15.0)
        .with_min_vacuum_size(20.0)
        .with_center_slab(false)
        .with_in_unit_planes(true)
        .with_symprec(0.001);

    assert_eq!(cfg.miller_index, [1, 1, 0]);
    assert_eq!(cfg.min_slab_size, 15.0);
    assert_eq!(cfg.min_vacuum_size, 20.0);
    assert!(!cfg.center_slab);
    assert!(cfg.in_unit_planes);
}

#[test]
fn test_make_slab_basic() {
    let cubic = make_cu_cubic(4.0);
    let slab = cubic
        .make_slab(
            &SlabConfig::new([1, 0, 0])
                .with_min_slab_size(8.0)
                .with_min_vacuum_size(10.0),
        )
        .unwrap();

    assert_eq!(slab.lattice.pbc, [true, true, false]);
    assert!(slab.num_sites() >= 2);
    assert_eq!(
        slab.properties["miller_index"],
        serde_json::json!([1, 0, 0])
    );
    assert_eq!(slab.properties["termination_index"], serde_json::json!(0));
}

#[test]
fn test_make_slab_various_surfaces() {
    let cubic = make_cu_cubic(4.0);

    for hkl in [[1, 0, 0], [1, 1, 0], [1, 1, 1], [2, 1, 0], [2, 1, 1]] {
        let slab = cubic
            .make_slab(
                &SlabConfig::new(hkl)
                    .with_min_slab_size(8.0)
                    .with_min_vacuum_size(10.0),
            )
            .unwrap_or_else(|_| panic!("{:?} failed", hkl));

        assert_eq!(slab.lattice.pbc, [true, true, false]);
        assert!(slab.num_sites() > 0);

        // All coords approximately in [0,1) (allowing small floating point tolerance)
        for fc in &slab.frac_coords {
            assert!(fc.x >= -1e-10 && fc.x < 1.0 + 1e-10, "x={}", fc.x);
            assert!(fc.y >= -1e-10 && fc.y < 1.0 + 1e-10, "y={}", fc.y);
            assert!(fc.z >= -1e-10 && fc.z < 1.0 + 1e-10, "z={}", fc.z);
        }
    }
}

#[test]
fn test_make_slab_in_unit_planes() {
    let cubic = make_cu_cubic(4.0);
    let slab = cubic
        .make_slab(
            &SlabConfig::new([1, 0, 0])
                .with_min_slab_size(3.0)
                .with_in_unit_planes(true)
                .with_min_vacuum_size(10.0),
        )
        .unwrap();

    // 3 planes * 4Å + 10Å vacuum ≈ 22Å
    let c = slab.lattice.lengths().z;
    assert!((c - 22.0).abs() < 1.0, "c={}", c);
}

#[test]
fn test_make_slab_centering() {
    let cubic = make_cu_cubic(4.0);
    let avg_z =
        |s: &Structure| s.frac_coords.iter().map(|c| c.z).sum::<f64>() / s.num_sites() as f64;

    let centered = cubic
        .make_slab(
            &SlabConfig::new([1, 0, 0])
                .with_min_slab_size(4.0)
                .with_min_vacuum_size(20.0)
                .with_center_slab(true),
        )
        .unwrap();
    let bottom = cubic
        .make_slab(
            &SlabConfig::new([1, 0, 0])
                .with_min_slab_size(4.0)
                .with_min_vacuum_size(20.0)
                .with_center_slab(false),
        )
        .unwrap();

    assert!(avg_z(&centered) > avg_z(&bottom));
    assert!(
        avg_z(&centered) > 0.3,
        "centered avg_z={}",
        avg_z(&centered)
    );
}

#[test]
fn test_make_slab_errors() {
    let cubic = make_cu_cubic(4.0);
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);

    // [0,0,0] rejected
    let err = cubic.make_slab(&SlabConfig::new([0, 0, 0])).unwrap_err();
    assert!(err.to_string().contains("zero"));

    // Negative vacuum rejected
    let err = cubic
        .make_slab(&SlabConfig::new([1, 0, 0]).with_min_vacuum_size(-5.0))
        .unwrap_err();
    assert!(err.to_string().contains("non-negative"));

    // NaN vacuum rejected
    let err = cubic
        .make_slab(&SlabConfig::new([1, 0, 0]).with_min_vacuum_size(f64::NAN))
        .unwrap_err();
    assert!(err.to_string().contains("finite"));

    // Empty structure rejected
    let err = empty.make_slab(&SlabConfig::new([1, 0, 0])).unwrap_err();
    assert!(err.to_string().contains("empty"));

    // Non-positive slab size rejected
    let err = cubic
        .make_slab(&SlabConfig::new([1, 0, 0]).with_min_slab_size(0.0))
        .unwrap_err();
    assert!(err.to_string().contains("positive"));

    // Invalid symprec rejected
    let err = cubic
        .make_slab(&SlabConfig::new([1, 0, 0]).with_symprec(0.0))
        .unwrap_err();
    assert!(err.to_string().contains("positive"));
}

#[test]
fn test_generate_slabs_terminations() {
    let nacl = make_nacl();
    let slabs = nacl
        .generate_slabs(
            &SlabConfig::new([1, 0, 0])
                .with_min_slab_size(10.0)
                .with_min_vacuum_size(10.0),
        )
        .unwrap();

    assert!(!slabs.is_empty());

    for (idx, slab) in slabs.iter().enumerate() {
        assert_eq!(slab.lattice.pbc, [true, true, false]);
        assert_eq!(
            slab.properties["termination_index"].as_u64().unwrap(),
            idx as u64
        );
    }
}

#[test]
fn test_piezoelectric_432_exception() {
    // Point group 432 (O) is non-centrosymmetric but forbids piezoelectricity
    use moyo::data::GeometricCrystalClass;
    assert!(
        !point_group_is_centrosymmetric(GeometricCrystalClass::O),
        "432 should be non-centrosymmetric"
    );
    assert!(
        !point_group_is_piezoelectric(GeometricCrystalClass::O),
        "432 should NOT allow piezoelectricity"
    );
    // Other non-centrosymmetric groups DO allow piezoelectricity
    assert!(point_group_is_piezoelectric(GeometricCrystalClass::C1));
    assert!(point_group_is_piezoelectric(GeometricCrystalClass::Td));
    // Centrosymmetric groups don't allow it either
    assert!(!point_group_is_piezoelectric(GeometricCrystalClass::Oh));
}

#[test]
fn test_spacegroup_type_lowercase_casing() {
    for (spg, expected_sys, expected_family) in [
        (1, "triclinic", "triclinic"),
        (15, "monoclinic", "monoclinic"),
        (62, "orthorhombic", "orthorhombic"),
        (136, "tetragonal", "tetragonal"),
        (167, "trigonal", "hexagonal"),
        (194, "hexagonal", "hexagonal"),
        (225, "cubic", "cubic"),
    ] {
        let info = spacegroup_type_from_number(spg).unwrap();
        assert_eq!(
            info.crystal_system, expected_sys,
            "spg {spg} crystal_system"
        );
        assert_eq!(
            info.crystal_family, expected_family,
            "spg {spg} crystal_family"
        );
        assert!(
            info.lattice_system.chars().all(|ch| ch.is_lowercase()),
            "spg {spg} lattice_system '{}' should be lowercase",
            info.lattice_system
        );
    }
}

#[test]
fn test_spacegroup_type_lazylocked_lookup() {
    for spg in 1..=230 {
        let info = spacegroup_type_from_number(spg);
        assert!(info.is_ok(), "spg {spg} should resolve");
    }
    assert!(spacegroup_type_from_number(0).is_err());
    assert!(spacegroup_type_from_number(231).is_err());
}

#[test]
fn test_disorder_properties_empty_structure() {
    let empty = Structure::new(Lattice::cubic(3.0), vec![], vec![]);
    assert_eq!(empty.max_species_per_site(), 0);
    assert!(!empty.has_substitutional_disorder());
    assert!(!empty.has_vacancy_disorder(1e-3));
    assert_eq!(empty.num_disordered_sites(1e-3), 0);
    // Empty structure: vacuously all sites are fully occupied
    assert_eq!(empty.min_total_occupancy_per_site(), 1.0);
}

// === from_spacegroup / from_prototype tests ===

#[test]
fn test_resolve_spacegroup_by_number() {
    // ITA number as string
    let hall = resolve_spacegroup("225").unwrap();
    assert!(hall > 0);
    // All valid space groups should resolve
    for sg_num in 1..=230 {
        assert!(
            resolve_spacegroup(&sg_num.to_string()).is_ok(),
            "Space group {sg_num} should resolve"
        );
    }
    // Out of range
    assert!(resolve_spacegroup("0").is_err());
    assert!(resolve_spacegroup("231").is_err());
    assert!(resolve_spacegroup("-1").is_err());
}

#[test]
fn test_resolve_spacegroup_by_hm_symbol() {
    // Standard short notation
    let hall_fm3m = resolve_spacegroup("Fm-3m").unwrap();
    let hall_225 = resolve_spacegroup("225").unwrap();
    assert_eq!(hall_fm3m, hall_225);

    // Various common symbols
    assert!(resolve_spacegroup("Pm-3m").is_ok());
    assert!(resolve_spacegroup("Im-3m").is_ok());
    assert!(resolve_spacegroup("P6_3/mmc").is_ok());
    assert!(resolve_spacegroup("Fd-3m").is_ok());
    assert!(resolve_spacegroup("F-43m").is_ok());

    // Case-insensitive matching
    let hall_lower = resolve_spacegroup("fm-3m").unwrap();
    assert_eq!(hall_lower, hall_fm3m);

    // Unknown symbol
    assert!(resolve_spacegroup("Xx-9z").is_err());
}

#[test]
fn test_from_spacegroup_known_structures() {
    let check = |label: &str, sg, lattice, syms: &[&str], coords, n_sites, formula: &str| {
        let species = syms.iter().map(|s| occ(s)).collect();
        let struc = Structure::from_spacegroup(sg, lattice, species, coords, None)
            .unwrap_or_else(|err| panic!("{label}: {err}"));
        assert_eq!(struc.num_sites(), n_sites, "{label}: wrong site count");
        assert_eq!(
            struc.composition().reduced_formula(),
            formula,
            "{label}: wrong formula"
        );
    };
    check(
        "NaCl",
        "225",
        Lattice::cubic(5.64),
        &["Na", "Cl"],
        vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
        8,
        "NaCl",
    );
    check(
        "Rutile",
        "136",
        Lattice::tetragonal(4.6, 2.95),
        &["Ti", "O"],
        vec![Vector3::zeros(), Vector3::new(0.3, 0.3, 0.0)],
        6,
        "TiO2",
    );
    check(
        "HCP Mg",
        "P6_3/mmc",
        Lattice::hexagonal(3.21, 5.21),
        &["Mg"],
        vec![Vector3::new(1.0 / 3.0, 2.0 / 3.0, 0.25)],
        2,
        "Mg",
    );
    check(
        "Perovskite",
        "221",
        Lattice::cubic(3.905),
        &["Sr", "Ti", "O"],
        vec![
            Vector3::zeros(),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.5, 0.5, 0.0),
        ],
        5,
        "SrTiO3",
    );
}

#[test]
fn test_from_spacegroup_lattice_incompatible() {
    let result = Structure::from_spacegroup(
        "225",
        Lattice::tetragonal(5.0, 7.0),
        vec![occ("Fe")],
        vec![Vector3::zeros()],
        None,
    );
    assert!(
        result.is_err(),
        "Cubic SG with tetragonal lattice should fail"
    );
}

#[test]
fn test_from_spacegroup_trigonal_r_centering_rejects_rhombohedral_lattice() {
    // R-3 (SG 148) resolves to a Hall symbol with R centering.
    // A primitive rhombohedral cell is incompatible with R centering translations.
    let rhomb_lattice = Lattice::from_parameters(5.0, 5.0, 5.0, 60.0, 60.0, 60.0);
    let result = Structure::from_spacegroup(
        "148",
        rhomb_lattice,
        vec![occ("Fe")],
        vec![Vector3::zeros()],
        None,
    );
    let err_msg = result.unwrap_err().to_string();
    assert!(
        err_msg.contains("R centering"),
        "Error should mention R centering incompatibility, got: {err_msg}"
    );
}

#[test]
fn test_from_spacegroup_trigonal_r_centering_accepts_hexagonal_lattice() {
    // R-3 (SG 148) with hexagonal conventional cell should work.
    // Al2O3 (corundum) uses R-3c (167), but R-3 (148) with a simple
    // site at the origin should produce 3 sites from R centering.
    let hex_lattice = Lattice::hexagonal(5.0, 14.0);
    let result = Structure::from_spacegroup(
        "148",
        hex_lattice,
        vec![occ("Fe")],
        vec![Vector3::zeros()],
        None,
    );
    let struc = result.expect("Hexagonal lattice should be accepted for R-3");
    // R centering triples the origin site: (0,0,0), (2/3,1/3,1/3), (1/3,2/3,2/3)
    assert_eq!(
        struc.num_sites(),
        3,
        "R centering should produce 3 sites from 1 orbit"
    );
    assert_eq!(struc.composition().reduced_formula(), "Fe");
}

#[test]
fn test_from_spacegroup_trigonal_p_centering_accepts_hexagonal_lattice() {
    // P3 (SG 143) has P centering — hexagonal lattice should work.
    let hex_lattice = Lattice::hexagonal(5.0, 8.0);
    let result = Structure::from_spacegroup(
        "143",
        hex_lattice,
        vec![occ("Fe")],
        vec![Vector3::new(0.1, 0.2, 0.3)],
        None,
    );
    let struc = result.expect("Hexagonal lattice should be accepted for P3");
    // P3 has 3 rotation ops × P centering (1 lattice point) = 3 sites
    assert_eq!(
        struc.num_sites(),
        3,
        "P3 should produce 3 sites from 3-fold rotation"
    );
}

#[test]
fn test_from_spacegroup_length_mismatch() {
    let result = Structure::from_spacegroup(
        "225",
        Lattice::cubic(5.0),
        vec![occ("Fe")],
        vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
        None,
    );
    assert!(result.is_err(), "Mismatched species/coords should fail");
}

#[test]
#[allow(clippy::type_complexity)]
fn test_from_prototype_all_types() {
    // (prototype, species symbols, a, c, expected_sites, expected_formula)
    let cases: &[(&str, &[&str], f64, Option<f64>, usize, &str)] = &[
        ("sc", &["Po"], 3.35, None, 1, "Po"),
        ("fcc", &["Cu"], 3.6, None, 4, "Cu"),
        ("bcc", &["Fe"], 2.87, None, 2, "Fe"),
        ("hcp", &["Mg"], 3.21, Some(5.21), 2, "Mg"),
        ("diamond", &["C"], 3.57, None, 8, "C"),
        ("rocksalt", &["Na", "Cl"], 5.64, None, 8, "NaCl"),
        ("perovskite", &["Sr", "Ti", "O"], 3.905, None, 5, "SrTiO3"),
        ("cscl", &["Cs", "Cl"], 4.12, None, 2, "CsCl"),
        ("fluorite", &["Ca", "F"], 5.46, None, 12, "CaF2"),
        ("antifluorite", &["Li", "O"], 4.61, None, 12, "Li2O"),
        ("zincblende", &["Zn", "S"], 5.41, None, 8, "ZnS"),
        ("wurtzite", &["Zn", "O"], 3.25, Some(5.21), 4, "ZnO"),
    ];
    for &(proto, syms, a, c_param, expected_sites, expected_formula) in cases {
        let species = syms.iter().map(|s| occ(s)).collect();
        let struc = Structure::from_prototype(proto, species, a, None, c_param)
            .unwrap_or_else(|err| panic!("{proto}: {err}"));
        assert_eq!(
            struc.num_sites(),
            expected_sites,
            "{proto}: wrong site count"
        );
        assert_eq!(
            struc.composition().reduced_formula(),
            expected_formula,
            "{proto}: wrong formula"
        );
    }
}

#[test]
fn test_from_prototype_case_insensitive() {
    let upper = Structure::from_prototype("FCC", vec![occ("Cu")], 3.6, None, None).unwrap();
    let lower = Structure::from_prototype("fcc", vec![occ("Cu")], 3.6, None, None).unwrap();
    assert_eq!(upper.num_sites(), lower.num_sites());
}

#[test]
fn test_from_prototype_wrong_species_count() {
    let result = Structure::from_prototype("rocksalt", vec![occ("Na")], 5.64, None, None);
    assert!(result.is_err(), "Wrong species count should fail");
}

#[test]
fn test_from_prototype_unknown() {
    let result = Structure::from_prototype("unknown_prototype", vec![occ("Fe")], 3.0, None, None);
    assert!(result.is_err(), "Unknown prototype should fail");
}

#[test]
fn test_from_prototype_missing_c_for_hcp() {
    assert!(Structure::from_prototype("hcp", vec![occ("Mg")], 3.21, None, None).is_err());
}

#[test]
fn test_validate_lattice_compatibility() {
    let rhomb60 = Lattice::from_parameters(5.0, 5.0, 5.0, 60.0, 60.0, 60.0);
    let rhomb120 = Lattice::from_parameters(5.0, 5.0, 5.0, 120.0, 120.0, 120.0);

    // (lattice, sg_number, centering, should_pass, label)
    let cases: Vec<(Lattice, i32, Centering, bool, &str)> = vec![
        // Cubic
        (Lattice::cubic(5.0), 225, Centering::F, true, "cubic ok"),
        (
            Lattice::tetragonal(5.0, 7.0),
            225,
            Centering::F,
            false,
            "tetragonal != cubic",
        ),
        // Hexagonal
        (
            Lattice::hexagonal(3.0, 5.0),
            194,
            Centering::P,
            true,
            "hexagonal ok",
        ),
        (
            Lattice::cubic(3.0),
            194,
            Centering::P,
            false,
            "cubic != hexagonal",
        ),
        // Tetragonal
        (
            Lattice::tetragonal(4.0, 6.0),
            136,
            Centering::P,
            true,
            "tetragonal ok",
        ),
        (
            Lattice::hexagonal(4.0, 6.0),
            136,
            Centering::P,
            false,
            "hexagonal != tetragonal",
        ),
        // Orthorhombic
        (
            Lattice::orthorhombic(3.0, 4.0, 5.0),
            62,
            Centering::P,
            true,
            "orthorhombic ok",
        ),
        // Monoclinic (each unique axis + failure case)
        (
            Lattice::from_parameters(3.0, 4.0, 5.0, 100.0, 90.0, 90.0),
            14,
            Centering::P,
            true,
            "mono axis-a",
        ),
        (
            Lattice::from_parameters(3.0, 4.0, 5.0, 90.0, 100.0, 90.0),
            14,
            Centering::P,
            true,
            "mono axis-b",
        ),
        (
            Lattice::from_parameters(3.0, 4.0, 5.0, 90.0, 90.0, 100.0),
            14,
            Centering::P,
            true,
            "mono axis-c",
        ),
        (
            Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 100.0, 90.0),
            14,
            Centering::P,
            false,
            "mono 2 non-right",
        ),
        // Trigonal + R centering: only hexagonal metric allowed
        (
            Lattice::hexagonal(3.0, 5.0),
            148,
            Centering::R,
            true,
            "trig R hex ok",
        ),
        (
            rhomb60.clone(),
            148,
            Centering::R,
            false,
            "trig R rhomb rejected",
        ),
        (
            Lattice::cubic(5.0),
            148,
            Centering::R,
            false,
            "trig R cubic rejected",
        ),
        // Trigonal + P centering: hex and rhomb accepted, 120 deg rejected
        (
            Lattice::hexagonal(3.0, 5.0),
            143,
            Centering::P,
            true,
            "trig P hex ok",
        ),
        (rhomb60, 143, Centering::P, true, "trig P rhomb ok"),
        (
            rhomb120,
            143,
            Centering::P,
            false,
            "trig P 120 deg rejected",
        ),
        // Triclinic: no constraints
        (
            Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 70.0),
            1,
            Centering::P,
            true,
            "triclinic ok",
        ),
    ];

    for (lattice, sg, centering, should_pass, label) in &cases {
        let result = validate_lattice_compatibility(lattice, *sg, *centering);
        assert_eq!(
            result.is_ok(),
            *should_pass,
            "{label}: expected {should_pass}, got {result:?}"
        );
    }
}

#[test]
fn test_generate_orbit_identity() {
    // Identity operation should produce exactly one site
    use moyo::base::Operation;
    let coord = Vector3::new(0.1, 0.2, 0.3);
    let ops = vec![Operation::identity()];
    let orbit = generate_orbit(&coord, &ops, 1e-5);
    assert_eq!(orbit.len(), 1);
    assert!((orbit[0] - coord).norm() < 1e-10);
}

#[test]
fn test_generate_orbit_deduplication() {
    // Applying the identity twice should still give one unique site
    use moyo::base::Operation;
    let coord = Vector3::new(0.25, 0.25, 0.25);
    let ops = vec![Operation::identity(), Operation::identity()];
    let orbit = generate_orbit(&coord, &ops, 1e-5);
    assert_eq!(orbit.len(), 1);
}

#[test]
fn test_build_conventional_operations() {
    use moyo::base::Operation;
    let ops = vec![Operation::identity()];

    // P centering: 1 lattice point → 1 op
    let p_points = vec![Vector3::new(0.0, 0.0, 0.0)];
    let full = build_conventional_operations(&ops, &p_points);
    assert_eq!(full.len(), 1);

    // I centering: 2 lattice points → 2 ops
    let i_points = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    let full_i = build_conventional_operations(&ops, &i_points);
    assert_eq!(full_i.len(), 2);
}

// === Tests ported from ASE/pymatgen coverage ===

#[test]
fn test_from_spacegroup_string_vs_int_equivalent() {
    let species = vec![occ("Na"), occ("Cl")];
    let coords = vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)];

    let by_symbol = Structure::from_spacegroup(
        "Fm-3m",
        Lattice::cubic(5.64),
        species.clone(),
        coords.clone(),
        None,
    )
    .unwrap();
    let by_number =
        Structure::from_spacegroup("225", Lattice::cubic(5.64), species, coords, None).unwrap();

    assert_eq!(by_symbol.num_sites(), by_number.num_sites());
    assert_eq!(
        by_symbol.composition().reduced_formula(),
        by_number.composition().reduced_formula()
    );
    for (pos_a, pos_b) in by_symbol.frac_coords.iter().zip(&by_number.frac_coords) {
        assert!((pos_a - pos_b).norm() < 1e-10);
    }
}

#[test]
fn test_from_spacegroup_diamond_exact_positions() {
    let diamond = Structure::from_spacegroup(
        "227",
        Lattice::cubic(3.57),
        vec![occ("C")],
        vec![Vector3::zeros()],
        None,
    )
    .unwrap();

    assert_eq!(diamond.num_sites(), 8);

    // Verify all 8 positions match ASE's reference (Fd-3m, 8a Wyckoff)
    let expected = [
        [0.0, 0.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.5, 0.5, 0.0],
        [0.5, 0.0, 0.5],
        [0.75, 0.25, 0.75],
        [0.25, 0.25, 0.25],
        [0.25, 0.75, 0.75],
        [0.75, 0.75, 0.25],
    ];
    for exp in &expected {
        let exp_vec = Vector3::new(exp[0], exp[1], exp[2]);
        let found = diamond.frac_coords.iter().any(|pos| {
            let mut diff = pos - exp_vec;
            diff -= diff.map(|elem| elem.round());
            diff.norm() < 1e-6
        });
        assert!(
            found,
            "Expected position ({}, {}, {}) not found in diamond",
            exp[0], exp[1], exp[2]
        );
    }
}

#[test]
fn test_from_spacegroup_additional_structures() {
    // CoSb3 skutterudite: Im-3 (204)
    let cosb3 = Structure::from_spacegroup(
        "204",
        Lattice::cubic(9.04),
        vec![occ("Co"), occ("Sb")],
        vec![
            Vector3::new(0.25, 0.25, 0.25),
            Vector3::new(0.0, 0.335, 0.158),
        ],
        None,
    )
    .unwrap();
    assert_eq!(cosb3.num_sites(), 32, "Skutterudite: 8 Co + 24 Sb");
    assert_eq!(cosb3.composition().reduced_formula(), "CoSb3");

    // I4/mmm (139) tetragonal
    let i4mmm = Structure::from_spacegroup(
        "139",
        Lattice::tetragonal(1.0, 1.0),
        vec![occ("H")],
        vec![Vector3::new(0.5, 0.25, 0.0)],
        None,
    )
    .unwrap();
    assert_eq!(i4mmm.num_sites(), 8);

    // Li2O antifluorite: Fm-3m (225)
    let li2o = Structure::from_spacegroup(
        "225",
        Lattice::cubic(3.0),
        vec![occ("Li"), occ("O")],
        vec![Vector3::new(0.25, 0.25, 0.25), Vector3::zeros()],
        None,
    )
    .unwrap();
    assert_eq!(li2o.num_sites(), 12);
    assert_eq!(li2o.composition().reduced_formula(), "Li2O");
}

#[test]
fn test_from_prototype_rocksalt_distinct_sublattices() {
    let nacl = Structure::from_prototype("rocksalt", vec![occ("Na"), occ("Cl")], 5.64, None, None)
        .unwrap();

    let na_pos: Vec<_> = nacl
        .frac_coords
        .iter()
        .zip(nacl.species())
        .filter(|(_, sp)| sp.element == Element::Na)
        .map(|(pos, _)| *pos)
        .collect();
    let cl_pos: Vec<_> = nacl
        .frac_coords
        .iter()
        .zip(nacl.species())
        .filter(|(_, sp)| sp.element == Element::Cl)
        .map(|(pos, _)| *pos)
        .collect();

    // No Na position should coincide with any Cl position
    for na in &na_pos {
        for cl in &cl_pos {
            let mut diff = na - cl;
            diff -= diff.map(|elem| elem.round());
            assert!(
                diff.norm() > 0.1,
                "Na at ({:.2},{:.2},{:.2}) overlaps Cl at ({:.2},{:.2},{:.2})",
                na.x,
                na.y,
                na.z,
                cl.x,
                cl.y,
                cl.z
            );
        }
    }

    // Distance from site 0 (Na at origin) to site 4 (Cl at 0.5,0.5,0.5) = body diagonal / 2
    // (The nearest Na-Cl distance in rocksalt is a/2, between different site pairs)
    let na_cl_dist = nacl.get_distance(0, 4);
    let expected = 5.64 * (3.0_f64).sqrt() / 2.0;
    assert!(
        (na_cl_dist - expected).abs() < 0.01,
        "Na-Cl distance: expected {expected:.3}, got {na_cl_dist:.3}"
    );
}

#[test]
fn test_from_prototype_cubic_lattices_are_orthogonal() {
    let cubic_protos: &[(&str, &[&str])] = &[
        ("sc", &["Fe"]),
        ("fcc", &["Fe"]),
        ("bcc", &["Fe"]),
        ("diamond", &["Fe"]),
        ("rocksalt", &["Fe", "O"]),
        ("perovskite", &["Fe", "O", "N"]),
        ("cscl", &["Fe", "O"]),
        ("fluorite", &["Fe", "O"]),
        ("antifluorite", &["Fe", "O"]),
        ("zincblende", &["Fe", "O"]),
    ];
    for &(proto, syms) in cubic_protos {
        let species = syms.iter().map(|s| occ(s)).collect();
        let struc = Structure::from_prototype(proto, species, 5.0, None, None).unwrap();
        for (idx, angle) in struc.lattice.angles().iter().enumerate() {
            assert!(
                (angle - 90.0).abs() < 0.01,
                "{proto}: angle[{idx}] = {angle}, expected 90°"
            );
        }
    }
}

#[test]
fn test_from_prototype_missing_c_for_wurtzite() {
    assert!(
        Structure::from_prototype("wurtzite", vec![occ("Zn"), occ("O")], 3.25, None, None).is_err()
    );
}

#[test]
fn test_from_prototype_rejects_invalid_lattice_params() {
    for bad_a in [-2.87, 0.0, f64::NAN, f64::INFINITY] {
        assert!(
            Structure::from_prototype("bcc", vec![occ("Fe")], bad_a, None, None).is_err(),
            "a={bad_a} should be rejected"
        );
    }
    for bad_c in [-5.21, 0.0] {
        assert!(
            Structure::from_prototype("hcp", vec![occ("Mg")], 3.21, None, Some(bad_c)).is_err(),
            "c={bad_c} should be rejected"
        );
    }
    // b is not used by any current prototype
    assert!(
        Structure::from_prototype("fcc", vec![occ("Cu")], 3.6, Some(5.0), None).is_err(),
        "b should be rejected for all prototypes"
    );
    // c is only used by hcp and wurtzite
    for cubic_proto in [
        "sc",
        "fcc",
        "bcc",
        "diamond",
        "rocksalt",
        "cscl",
        "fluorite",
        "antifluorite",
        "zincblende",
        "perovskite",
    ] {
        let species: Vec<_> = match cubic_proto {
            "rocksalt" | "cscl" | "fluorite" | "antifluorite" | "zincblende" => {
                vec![occ("Na"), occ("Cl")]
            }
            "perovskite" => vec![occ("Sr"), occ("Ti"), occ("O")],
            _ => vec![occ("Fe")],
        };
        assert!(
            Structure::from_prototype(cubic_proto, species, 5.0, None, Some(7.0)).is_err(),
            "c should be rejected for {cubic_proto}"
        );
    }
}

#[test]
fn test_from_spacegroup_invalid_tol() {
    for bad_tol in [0.0, -1e-5, f64::NAN] {
        let result = Structure::from_spacegroup(
            "225",
            Lattice::cubic(5.0),
            vec![occ("Fe")],
            vec![Vector3::zeros()],
            Some(bad_tol),
        );
        assert!(result.is_err(), "tol={bad_tol} should be rejected");
    }
}

#[test]
fn test_from_spacegroup_unknown_symbol() {
    assert!(resolve_spacegroup("Xx-9z").is_err());
    assert!(resolve_spacegroup("not-a-spacegroup").is_err());
}
