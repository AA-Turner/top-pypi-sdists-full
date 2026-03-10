use super::*;
use crate::element::Element;
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::Vector3;
use std::collections::HashMap;
use std::path::Path;
use tempfile::{NamedTempFile, TempDir};

// Helper to count elements in a structure (counts dominant species per site)
fn count_element(structure: &Structure, elem: Element) -> usize {
    structure
        .species()
        .iter()
        .filter(|sp| sp.element == elem)
        .count()
}

#[test]
fn test_parse_simple_structure() {
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [
            {"species": [{"element": "Fe"}], "abc": [0,0,0]},
            {"species": [{"element": "Fe"}], "abc": [0.5,0.5,0.5]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 2);
    assert_eq!(s.species()[0].element, Element::Fe);
    assert_eq!(s.species()[1].element, Element::Fe);
    assert!((s.lattice.volume() - 64.0).abs() < 1e-10);
}

#[test]
fn test_parse_with_oxidation_states() {
    let json = r#"{
        "lattice": {"matrix": [[5.64,0,0],[0,5.64,0],[0,0,5.64]]},
        "sites": [
            {"species": [{"element": "Na", "oxidation_state": 1}], "abc": [0,0,0]},
            {"species": [{"element": "Cl", "oxidation_state": -1}], "abc": [0.5,0.5,0.5]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.species()[0].oxidation_state, Some(1));
    assert_eq!(s.species()[1].oxidation_state, Some(-1));
}

#[test]
fn test_parse_oxidation_states_as_floats() {
    // Pymatgen serializes oxidation states as floats (e.g., 3.0 instead of 3)
    let json = r#"{
        "lattice": {"matrix": [[5.0,0,0],[0,5.0,0],[0,0,5.0]]},
        "sites": [
            {"species": [{"element": "Bi", "oxidation_state": 3.0}], "abc": [0,0,0]},
            {"species": [{"element": "Zr", "oxidation_state": 4.0}], "abc": [0.5,0.5,0.5]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.species()[0].oxidation_state, Some(3));
    assert_eq!(s.species()[1].oxidation_state, Some(4));
}

#[test]
fn test_parse_oxidation_states_null() {
    // Test that null oxidation_state is handled correctly
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [
            {"species": [{"element": "Fe", "oxidation_state": null}], "abc": [0,0,0]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.species()[0].oxidation_state, None);
}

#[test]
fn test_parse_full_pymatgen_format() {
    // Test with all optional fields present
    let json = r#"{
        "@module": "pymatgen.core.structure",
        "@class": "Structure",
        "charge": 0,
        "lattice": {
            "matrix": [[3.84, 0, 0], [0, 3.84, 0], [0, 0, 3.84]],
            "pbc": [true, true, true]
        },
        "sites": [
            {"species": [{"element": "Cu", "occu": 1.0}], "abc": [0, 0, 0], "properties": {}}
        ],
        "properties": {}
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 1);
    assert_eq!(s.species()[0].element, Element::Cu);
}

#[test]
fn test_parse_unknown_element_becomes_dummy() {
    // Unknown elements are now mapped to Dummy with original_symbol in properties
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [{"element": "Zzz"}], "abc": [0,0,0]}]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 1);
    assert_eq!(s.species()[0].element, Element::Dummy);

    // The original symbol should be stored in site properties
    let props = &s.site_occupancies[0].properties;
    assert_eq!(
        props.get("original_symbol").and_then(|v| v.as_str()),
        Some("Zzz")
    );
}

#[test]
fn test_parse_empty_symbol_fails() {
    // Empty symbol should fail
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [{"element": ""}], "abc": [0,0,0]}]
    }"#;

    let result = parse_structure_json(json);
    assert!(result.is_err());
}

#[test]
fn test_parse_pseudo_elements() {
    // Dummy atoms are now valid
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [
            {"species": [{"element": "X"}], "abc": [0,0,0]},
            {"species": [{"element": "D"}], "abc": [0.5,0,0]},
            {"species": [{"element": "T"}], "abc": [0,0.5,0]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 3);
    assert_eq!(s.species()[0].element, Element::Dummy);
    assert_eq!(s.species()[1].element, Element::D);
    assert_eq!(s.species()[2].element, Element::T);
}

#[test]
fn test_parse_oxidation_state_from_symbol() {
    // Oxidation state extracted from symbol (e.g., Fe2+)
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [{"element": "Fe2+"}], "abc": [0,0,0]}]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.species()[0].element, Element::Fe);
    assert_eq!(s.species()[0].oxidation_state, Some(2));
}

#[test]
fn test_parse_oxidation_state_conflict_error() {
    // Conflicting oxidation state: symbol says 2+, JSON says 3
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [{"element": "Fe2+", "oxidation_state": 3}], "abc": [0,0,0]}]
    }"#;

    let result = parse_structure_json(json);
    assert!(result.is_err());
    let err = result.unwrap_err().to_string();
    assert!(err.contains("Conflicting oxidation states"));
}

#[test]
fn test_parse_oxidation_state_match_ok() {
    // Same oxidation state in symbol and JSON is fine
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [{"element": "Fe2+", "oxidation_state": 2}], "abc": [0,0,0]}]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.species()[0].oxidation_state, Some(2));
}

#[test]
fn test_parse_site_properties() {
    // Site properties should be preserved
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{
            "species": [{"element": "Fe"}],
            "abc": [0,0,0],
            "label": "Fe1_oct",
            "properties": {"magmom": 2.5, "selective_dynamics": [true, true, false]}
        }]
    }"#;

    let s = parse_structure_json(json).unwrap();
    let props = s.site_properties(0);

    // Check label is in properties
    assert_eq!(props.get("label").and_then(|v| v.as_str()), Some("Fe1_oct"));

    // Check magmom
    assert_eq!(props.get("magmom").and_then(|v| v.as_f64()), Some(2.5));

    // Check selective_dynamics
    let sd = props.get("selective_dynamics").and_then(|v| v.as_array());
    assert!(sd.is_some());
}

#[test]
fn test_parse_potcar_suffix() {
    // POTCAR suffix should be extracted to metadata
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [{"element": "Ca_pv"}], "abc": [0,0,0]}]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.species()[0].element, Element::Ca);

    // Check potcar_suffix in site properties
    let props = s.site_properties(0);
    assert_eq!(
        props.get("potcar_suffix").and_then(|v| v.as_str()),
        Some("_pv")
    );
}

#[test]
fn test_parse_multi_species_no_metadata_overwrite() {
    // Multi-species sites should NOT merge per-species metadata to avoid overwrites
    // E.g., a disordered site with Fe_pv and Ni_sv should not lose one's suffix
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [
            {"element": "Fe_pv", "occu": 0.5},
            {"element": "Ni_sv", "occu": 0.5}
        ], "abc": [0,0,0]}]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 1);

    // Both species should be present
    let site_occ = &s.site_occupancies[0];
    assert_eq!(site_occ.species.len(), 2);

    // Metadata should NOT be merged (would cause overwrite conflicts)
    let props = s.site_properties(0);
    assert!(
        props.get("potcar_suffix").is_none(),
        "Multi-species metadata should not be merged to avoid overwrites"
    );
}

#[test]
fn test_structure_charge() {
    // Helper to build minimal structure JSON with optional charge
    let make_json = |charge: Option<f64>| {
        let base = r#"{"lattice":{"matrix":[[4,0,0],[0,4,0],[0,0,4]]},"sites":[{"species":[{"element":"Na"}],"abc":[0,0,0]}]"#;
        charge.map_or(format!("{base}}}"), |c| format!("{base},\"charge\":{c}}}"))
    };

    // Parse: positive, negative, missing charge
    for (input, expected) in [(Some(1.0), 1.0), (Some(-1.5), -1.5), (None, 0.0)] {
        let s = parse_structure_json(&make_json(input)).unwrap();
        assert!((s.charge - expected).abs() < 1e-10, "input={input:?}");
        assert!(
            !s.properties.contains_key("charge"),
            "charge not in properties"
        );
    }

    // Roundtrip: charge survives serialize -> parse
    let s = Structure::try_new_full(
        Lattice::cubic(4.0),
        vec![SiteOccupancy::ordered(Species::neutral(Element::Li))],
        vec![Vector3::new(0.0, 0.0, 0.0)],
        [true, true, true],
        2.5,
        HashMap::new(),
    )
    .unwrap();
    let parsed = parse_structure_json(&structure_to_pymatgen_json(&s)).unwrap();
    assert!((parsed.charge - 2.5).abs() < 1e-10);
}

#[test]
fn test_site_properties_serialization() {
    // Site properties should round-trip through serialization
    let lattice = Lattice::cubic(4.0);
    let species = Species::neutral(Element::Fe);
    let coords = vec![Vector3::new(0.0, 0.0, 0.0)];

    let mut props = HashMap::new();
    props.insert("magmom".to_string(), serde_json::json!(2.5));
    props.insert("label".to_string(), serde_json::json!("Fe1"));

    let site_occ = crate::species::SiteOccupancy::with_properties(vec![(species, 1.0)], props);

    let s1 = Structure::try_new_from_occupancies(lattice, vec![site_occ], coords).unwrap();

    // Serialize and parse back
    let json = structure_to_pymatgen_json(&s1);
    let s2 = parse_structure_json(&json).unwrap();

    // Check properties are preserved
    let props2 = s2.site_properties(0);
    assert_eq!(props2.get("magmom").and_then(|v| v.as_f64()), Some(2.5));
    assert_eq!(props2.get("label").and_then(|v| v.as_str()), Some("Fe1"));
}

#[test]
fn test_parse_empty_species() {
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [{"species": [], "abc": [0,0,0]}]
    }"#;

    let result = parse_structure_json(json);
    assert!(result.is_err());
    let err = result.unwrap_err();
    assert!(err.to_string().contains("no species"));
}

#[test]
fn test_parse_invalid_json() {
    let json = "not valid json";
    let result = parse_structure_json(json);
    assert!(result.is_err());
}

#[test]
fn test_structure_to_json_roundtrip() {
    let lattice = Lattice::cubic(5.64);
    let species = vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)];
    let coords = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    let s1 = Structure::new(lattice, species, coords);

    let json = structure_to_pymatgen_json(&s1);
    let s2 = parse_structure_json(&json).unwrap();

    assert_eq!(s1.num_sites(), s2.num_sites());
    assert_eq!(s1.species()[0].element, s2.species()[0].element);
    assert_eq!(s1.species()[1].element, s2.species()[1].element);
    assert!((s1.lattice.volume() - s2.lattice.volume()).abs() < 1e-10);
    assert_eq!(s1.lattice.pbc, s2.lattice.pbc);
}

#[test]
fn test_structure_to_json_preserves_pbc() {
    // Test non-standard PBC (e.g., slab with vacuum in z-direction)
    let mut lattice = Lattice::cubic(10.0);
    lattice.pbc = [true, true, false]; // Non-periodic in z
    let species = vec![Species::neutral(Element::Si)];
    let coords = vec![Vector3::new(0.5, 0.5, 0.5)];
    let s1 = Structure::new(lattice, species, coords);

    let json = structure_to_pymatgen_json(&s1);
    assert!(
        json.contains(r#""pbc":[true,true,false]"#),
        "JSON should contain pbc: {json}"
    );

    let s2 = parse_structure_json(&json).unwrap();
    assert_eq!(
        s2.lattice.pbc,
        [true, true, false],
        "PBC should be preserved in roundtrip"
    );
}

#[test]
fn test_structure_to_json_preserves_properties() {
    // Test that properties survive JSON round-trip
    let json_with_props = r#"{
        "lattice": {"matrix": [[5.0,0,0],[0,5.0,0],[0,0,5.0]]},
        "sites": [{"species": [{"element": "Fe"}], "abc": [0.0, 0.0, 0.0]}],
        "properties": {"energy": -3.5, "source": "dft", "tags": ["test", "example"]}
    }"#;

    let s1 = parse_structure_json(json_with_props).unwrap();
    assert_eq!(s1.properties.len(), 3);
    assert_eq!(s1.properties["energy"], serde_json::json!(-3.5));
    assert_eq!(s1.properties["source"], serde_json::json!("dft"));

    // Round-trip through JSON
    let json_out = structure_to_pymatgen_json(&s1);
    let s2 = parse_structure_json(&json_out).unwrap();

    assert_eq!(s2.properties.len(), 3);
    assert_eq!(s2.properties["energy"], serde_json::json!(-3.5));
    assert_eq!(s2.properties["source"], serde_json::json!("dft"));
    assert_eq!(
        s2.properties["tags"],
        serde_json::json!(["test", "example"])
    );
}

#[test]
fn test_parse_rocksalt() {
    // Full NaCl structure
    let json = r#"{
        "lattice": {"matrix": [[5.64,0,0],[0,5.64,0],[0,0,5.64]]},
        "sites": [
            {"species": [{"element": "Na"}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Na"}], "abc": [0.5, 0.5, 0.0]},
            {"species": [{"element": "Na"}], "abc": [0.5, 0.0, 0.5]},
            {"species": [{"element": "Na"}], "abc": [0.0, 0.5, 0.5]},
            {"species": [{"element": "Cl"}], "abc": [0.5, 0.0, 0.0]},
            {"species": [{"element": "Cl"}], "abc": [0.0, 0.5, 0.0]},
            {"species": [{"element": "Cl"}], "abc": [0.0, 0.0, 0.5]},
            {"species": [{"element": "Cl"}], "abc": [0.5, 0.5, 0.5]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 8);

    // Check composition
    let comp = s.composition();
    assert_eq!(comp.reduced_formula(), "NaCl");
}

#[test]
fn test_parse_oxidation_state_overflow_i8() {
    // Oxidation states outside i8 range should error (after successful parsing)
    for oxi in [200, -200] {
        let json = format!(
            r#"{{"lattice": {{"matrix": [[4,0,0],[0,4,0],[0,0,4]]}},
                "sites": [{{"species": [{{"element": "Fe", "oxidation_state": {oxi}}}], "abc": [0,0,0]}}]}}"#
        );
        let result = parse_structure_json(&json);
        assert!(result.is_err(), "oxi={oxi} should error");
        assert!(result.unwrap_err().to_string().contains("out of range"));
    }
}

#[test]
fn test_parse_oxidation_state_overflow_i32() {
    // Float values that would overflow i32 should error during deserialization
    for oxi in ["3e10", "-3e10"] {
        let json = format!(
            r#"{{"lattice": {{"matrix": [[4,0,0],[0,4,0],[0,0,4]]}},
                "sites": [{{"species": [{{"element": "Fe", "oxidation_state": {oxi}}}], "abc": [0,0,0]}}]}}"#
        );
        let result = parse_structure_json(&json);
        assert!(result.is_err(), "oxi={oxi} should error");
        assert!(
            result.unwrap_err().to_string().contains("overflow"),
            "Error for oxi={oxi} should mention overflow"
        );
    }
}

#[test]
fn test_parse_disordered_site() {
    // Multiple species per site (disordered)
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [
            {"species": [
                {"element": "Fe", "occu": 0.5},
                {"element": "Co", "occu": 0.5}
            ], "abc": [0,0,0]}
        ]
    }"#;

    // Should parse successfully with all species preserved
    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 1);
    assert!(!s.is_ordered());

    // Check all species are present
    let site_occ = &s.site_occupancies[0];
    assert_eq!(site_occ.species.len(), 2);
    assert!((site_occ.total_occupancy() - 1.0).abs() < 1e-10);

    // Verify both Fe and Co are present
    let elements: Vec<_> = site_occ.species.iter().map(|(sp, _)| sp.element).collect();
    assert!(elements.contains(&Element::Fe));
    assert!(elements.contains(&Element::Co));
}

#[test]
fn test_parse_invalid_occupancy_rejected() {
    // Test various invalid occupancy values
    for (occu, desc) in [(-0.5, "negative"), (0.0, "zero"), (1.5, "> 1.0")] {
        let json = format!(
            r#"{{"lattice":{{"matrix":[[4,0,0],[0,4,0],[0,0,4]]}},"sites":[{{"species":[{{"element":"Fe","occu":{occu}}}],"abc":[0,0,0]}}]}}"#
        );
        let result = parse_structure_json(&json);
        assert!(result.is_err(), "{desc} occupancy should be rejected");
        let err = result.unwrap_err().to_string();
        assert!(
            err.contains("invalid occupancy"),
            "{desc} occupancy error should mention 'invalid occupancy': {err}"
        );
    }
}

#[test]
fn test_parse_overflow_occupancy_rejected() {
    // 1e309 overflows f64 to infinity - JSON parser catches this as "out of range"
    let json = r#"{"lattice":{"matrix":[[4,0,0],[0,4,0],[0,0,4]]},"sites":[{"species":[{"element":"Fe","occu":1e309}],"abc":[0,0,0]}]}"#;
    let result = parse_structure_json(json);
    assert!(result.is_err(), "Overflow occupancy should be rejected");
}

#[test]
fn test_parse_xyz_coords() {
    // Test parsing with xyz (Cartesian) coordinates
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [
            {"species": [{"element": "Fe"}], "xyz": [2, 2, 2], "abc": [0.5, 0.5, 0.5]}
        ]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 1);
    // Check fractional coords are used
    assert!((s.frac_coords[0][0] - 0.5).abs() < 1e-10);
}

#[test]
fn test_parse_minimal_lattice() {
    // Lattice with only matrix (no pbc field)
    let json = r#"{
        "lattice": {"matrix": [[3,0,0],[0,3,0],[0,0,3]]},
        "sites": [{"species": [{"element": "Cu"}], "abc": [0,0,0]}]
    }"#;

    let s = parse_structure_json(json).unwrap();
    assert_eq!(s.num_sites(), 1);
    assert!((s.lattice.volume() - 27.0).abs() < 1e-10);
}

// === POSCAR Parser Tests ===

#[test]
fn test_parse_poscar_cubic_diamond() {
    let poscar = r#"cubic diamond
  3.7
0.5 0.5 0.0
0.0 0.5 0.5
0.5 0.0 0.5
   C
   2
Direct
  0.0 0.0 0.0
  0.25 0.25 0.25
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 2);
    assert_eq!(s.species()[0].element, Element::C);
    assert_eq!(s.species()[1].element, Element::C);

    // Check fractional coordinates
    assert!((s.frac_coords[0].x - 0.0).abs() < 1e-10);
    assert!((s.frac_coords[1].x - 0.25).abs() < 1e-10);
}

#[test]
fn test_parse_poscar_nacl() {
    let poscar = r#"NaCl
   5.64
 1.0  0.0  0.0
 0.0  1.0  0.0
 0.0  0.0  1.0
   Na Cl
   1 1
Direct
   0.0  0.0  0.0
   0.5  0.5  0.5
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 2);
    assert_eq!(s.species()[0].element, Element::Na);
    assert_eq!(s.species()[1].element, Element::Cl);

    // Check volume (5.64^3)
    assert!((s.lattice.volume() - 5.64f64.powi(3)).abs() < 1e-6);
}

#[test]
fn test_parse_poscar_cartesian() {
    // POSCAR with Cartesian coordinates
    // Note: In POSCAR, Cartesian coords are already scaled by the lattice constant
    // So (1.435, 1.435, 1.435) with scale 2.87 gives actual coords (4.12, 4.12, 4.12)
    // which maps to fractional (0.5, 0.5, 0.5) with a=2.87*2=5.74
    let poscar = r#"Fe BCC
   2.87
 1.0  0.0  0.0
 0.0  1.0  0.0
 0.0  0.0  1.0
   Fe
   2
Cartesian
   0.0     0.0     0.0
   0.5     0.5     0.5
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 2);
    assert_eq!(s.species()[0].element, Element::Fe);

    // First atom at origin
    assert!((s.frac_coords[0].x - 0.0).abs() < 1e-10);

    // Second atom should be at (0.5, 0.5, 0.5) in fractional
    // Cartesian (0.5, 0.5, 0.5) * scale 2.87 = (1.435, 1.435, 1.435) in Å
    // Divide by lattice length 2.87 = (0.5, 0.5, 0.5) in fractional
    assert!((s.frac_coords[1].x - 0.5).abs() < 1e-6);
    assert!((s.frac_coords[1].y - 0.5).abs() < 1e-6);
    assert!((s.frac_coords[1].z - 0.5).abs() < 1e-6);
}

#[test]
fn test_parse_poscar_vasp4_error() {
    // VASP 4 format without element symbols should error
    let poscar = r#"Si
   5.43
 0.5 0.5 0.0
 0.0 0.5 0.5
 0.5 0.0 0.5
   2
Direct
   0.0 0.0 0.0
   0.25 0.25 0.25
"#;
    let result = parse_poscar_str(poscar);
    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("VASP 4 format"));
}

#[test]
fn test_parse_poscar_negative_scale_factor() {
    // Negative scale factor means volume = |scale|
    let poscar = r#"Test with volume scaling
  -27.0
3.0 0.0 0.0
0.0 3.0 0.0
0.0 0.0 3.0
   H
   1
Direct
  0.0 0.0 0.0
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 1);
    // Volume should be 27.0 (scale factor applied)
    assert!((s.lattice.volume() - 27.0).abs() < 1e-3);
}

#[test]
fn test_parse_poscar_multiple_elements() {
    // BaTiO3 tetragonal structure
    let poscar = r#"Ba1 Ti1 O3
1.0
4.001368 0.000000 0.000000
0.000000 4.001368 0.000000
0.000000 0.000000 4.215744
Ba Ti O
1 1 3
direct
0.000000 0.000000 0.020273
0.500000 0.500000 0.538852
0.000000 0.500000 0.492022
0.500000 0.000000 0.492022
0.500000 0.500000 0.970829
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 5);
    assert_eq!(s.species()[0].element, Element::Ba);
    assert_eq!(s.species()[1].element, Element::Ti);
    assert_eq!(s.species()[2].element, Element::O);
    assert_eq!(s.species()[3].element, Element::O);
    assert_eq!(s.species()[4].element, Element::O);

    // Check lattice parameters (a, b, c)
    let lengths = s.lattice.lengths();
    assert!((lengths.x - 4.001368).abs() < 1e-5);
    assert!((lengths.z - 4.215744).abs() < 1e-5);
}

#[test]
fn test_parse_poscar_rocksalt_full() {
    // Full NaCl structure (8 atoms)
    let poscar = r#"Na Cl
   1.00000000000000
 5.6903014761756712    0.0000000000000000    0.0000000000000000
 0.0000000000000000    5.6903014761756712    0.0000000000000000
 0.0000000000000000    0.0000000000000000    5.6903014761756712
  Na  Cl
   4   4
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.0000000000000000  0.5000000000000000  0.5000000000000000
  0.5000000000000000  0.0000000000000000  0.5000000000000000
  0.5000000000000000  0.5000000000000000  0.0000000000000000
  0.5000000000000000  0.5000000000000000  0.5000000000000000
  0.5000000000000000  0.0000000000000000  0.0000000000000000
  0.0000000000000000  0.5000000000000000  0.0000000000000000
  0.0000000000000000  0.0000000000000000  0.5000000000000000
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 8);

    // Count elements
    assert_eq!(count_element(&s, Element::Na), 4);
    assert_eq!(count_element(&s, Element::Cl), 4);

    // Check lattice constant (a = first length)
    let lengths = s.lattice.lengths();
    assert!((lengths.x - 5.6903014762).abs() < 1e-6);
}

#[test]
fn test_parse_poscar_selective_dynamics() {
    // Selective dynamics (should be parsed but flags ignored)
    let poscar = r#"Silicon slab with selective dynamics
1.0
   5.4689999999999999    0.0000000000000000    0.0000000000000000
   0.0000000000000000    5.4689999999999999    0.0000000000000000
   0.0000000000000000    0.0000000000000000   20.0000000000000000
Si
8
Selective dynamics
Direct
0.000 0.000 0.100 F F F
0.500 0.000 0.100 F F F
0.000 0.500 0.100 F F F
0.500 0.500 0.100 F F F
0.250 0.250 0.150 T T T
0.750 0.250 0.150 T T T
0.250 0.750 0.150 T T T
0.750 0.750 0.150 T T T
"#;
    let s = parse_poscar_str(poscar).unwrap();
    assert_eq!(s.num_sites(), 8);
    assert_eq!(s.species()[0].element, Element::Si);

    // Check some coordinates
    assert!((s.frac_coords[0].x - 0.0).abs() < 1e-10);
    assert!((s.frac_coords[0].z - 0.1).abs() < 1e-10);
    assert!((s.frac_coords[4].x - 0.25).abs() < 1e-10);
}

// === extXYZ Parser Tests ===

#[test]
fn test_parse_extxyz_quartz() {
    // Quartz structure in extXYZ format
    let extxyz = r#"6
Lattice="4.916 0.0 0.0 -2.458 4.257 0.0 0.0 0.0 5.405" Properties=species:S:1:pos:R:3
Si 1.229 0.0 0.0
Si -1.229 2.128 2.703
O 2.679 0.0 1.624
O -2.679 2.128 4.327
O 0.0 1.578 3.781
O 0.0 -1.578 1.081
"#;
    // Write to temp file and parse
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_quartz.xyz");
    std::fs::write(&temp_path, extxyz).unwrap();

    let s = parse_extxyz(&temp_path).unwrap();
    std::fs::remove_file(&temp_path).ok();

    assert_eq!(s.num_sites(), 6);

    // Count elements
    assert_eq!(count_element(&s, Element::Si), 2);
    assert_eq!(count_element(&s, Element::O), 4);

    // Check lattice (a, b, c)
    let lengths = s.lattice.lengths();
    assert!((lengths.x - 4.916).abs() < 0.01);
    assert!((lengths.z - 5.405).abs() < 0.01);

    // Verify fractional coordinates are sensible (within reasonable bounds)
    // First Si at Cartesian (1.229, 0, 0) should have fractional x ≈ 0.25
    assert!(
        s.frac_coords[0].x > 0.1 && s.frac_coords[0].x < 0.5,
        "First Si x-coord should be ~0.25, got {}",
        s.frac_coords[0].x
    );
    // All fractional coordinates should be finite
    for (idx, coord) in s.frac_coords.iter().enumerate() {
        assert!(coord.x.is_finite(), "Site {idx} x not finite");
        assert!(coord.y.is_finite(), "Site {idx} y not finite");
        assert!(coord.z.is_finite(), "Site {idx} z not finite");
    }
}

#[test]
fn test_parse_extxyz_with_energy() {
    // extXYZ with energy property
    let extxyz = r#"2
Lattice="5.0 0.0 0.0 0.0 5.0 0.0 0.0 0.0 5.0" energy=-10.5
H 0.0 0.0 0.0
O 2.5 2.5 2.5
"#;
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_with_energy.xyz");
    std::fs::write(&temp_path, extxyz).unwrap();

    let s = parse_extxyz(&temp_path).unwrap();
    std::fs::remove_file(&temp_path).ok();

    assert_eq!(s.num_sites(), 2);
    // Check energy is preserved in properties
    assert!(s.properties.contains_key("energy"));
    assert_eq!(s.properties["energy"], serde_json::json!(-10.5));
}

#[test]
fn test_parse_extxyz_with_pbc() {
    // extXYZ with PBC specification
    let extxyz = r#"1
Lattice="4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0" pbc="T T F"
C 2.0 2.0 2.0
"#;
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_with_pbc.xyz");
    std::fs::write(&temp_path, extxyz).unwrap();

    let s = parse_extxyz(&temp_path).unwrap();
    std::fs::remove_file(&temp_path).ok();

    assert_eq!(s.num_sites(), 1);
    assert_eq!(s.lattice.pbc, [true, true, false]);
}

#[test]
fn test_parse_extxyz_missing_lattice_error() {
    // Plain XYZ without lattice should error for crystal structure
    let xyz = r#"2
Cyclohexane (no lattice)
C 0.0 0.0 0.0
H 1.0 0.0 0.0
"#;
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_no_lattice.xyz");
    std::fs::write(&temp_path, xyz).unwrap();

    let result = parse_extxyz(&temp_path);
    std::fs::remove_file(&temp_path).ok();

    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("lattice"));
}

#[test]
fn test_parse_extxyz_trajectory() {
    // Multi-frame trajectory
    let extxyz = r#"2
Lattice="4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0" energy=-5.0
H 0.0 0.0 0.0
H 2.0 2.0 2.0
2
Lattice="4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0" energy=-5.5
H 0.1 0.1 0.1
H 2.1 2.1 2.1
"#;
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_trajectory.xyz");
    std::fs::write(&temp_path, extxyz).unwrap();

    let frames = parse_extxyz_trajectory(&temp_path).unwrap();
    std::fs::remove_file(&temp_path).ok();

    assert_eq!(frames.len(), 2);

    // Check first frame
    let s1 = frames[0].as_ref().unwrap();
    assert_eq!(s1.num_sites(), 2);
    assert_eq!(s1.properties["energy"], serde_json::json!(-5.0));

    // Check second frame
    let s2 = frames[1].as_ref().unwrap();
    assert_eq!(s2.num_sites(), 2);
    assert_eq!(s2.properties["energy"], serde_json::json!(-5.5));
}

#[test]
fn test_parse_extxyz_cubic_lattice() {
    // Simple cubic lattice with single atom
    let extxyz = r#"1
Lattice="3.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 3.0"
Fe 1.5 1.5 1.5
"#;
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_cubic.xyz");
    std::fs::write(&temp_path, extxyz).unwrap();

    let s = parse_extxyz(&temp_path).unwrap();
    std::fs::remove_file(&temp_path).ok();

    assert_eq!(s.num_sites(), 1);
    assert_eq!(s.species()[0].element, Element::Fe);

    // Check fractional coords (1.5 / 3.0 = 0.5)
    assert!((s.frac_coords[0].x - 0.5).abs() < 1e-10);
    assert!((s.frac_coords[0].y - 0.5).abs() < 1e-10);
    assert!((s.frac_coords[0].z - 0.5).abs() < 1e-10);
}

#[test]
fn test_parse_extxyz_hexagonal_lattice() {
    // Hexagonal lattice (non-orthogonal)
    let a = 3.0;
    let c = 5.0;
    let extxyz = format!(
        r#"1
Lattice="{a} 0.0 0.0 {} {} 0.0 0.0 0.0 {c}"
Mg 0.0 0.0 0.0
"#,
        -a / 2.0,
        a * (3.0_f64).sqrt() / 2.0
    );
    let temp_dir = std::env::temp_dir();
    let temp_path = temp_dir.join("test_hex.xyz");
    std::fs::write(&temp_path, &extxyz).unwrap();

    let s = parse_extxyz(&temp_path).unwrap();
    std::fs::remove_file(&temp_path).ok();

    assert_eq!(s.num_sites(), 1);
    // Atom at origin should have fractional coords (0, 0, 0)
    assert!((s.frac_coords[0].x - 0.0).abs() < 1e-10);
    assert!((s.frac_coords[0].y - 0.0).abs() < 1e-10);
    assert!((s.frac_coords[0].z - 0.0).abs() < 1e-10);
}

// === Format Detection Tests ===

#[test]
fn test_format_detection() {
    // Consolidated format detection test covering all cases:
    // - basic extensions, case-insensitive, POSCAR variants, and unknown
    let cases: &[(&str, Option<StructureFormat>)] = &[
        // Basic extensions
        ("structure.json", Some(StructureFormat::PymatgenJson)),
        ("structure.cif", Some(StructureFormat::Cif)),
        ("trajectory.xyz", Some(StructureFormat::ExtXyz)),
        ("structure.extxyz", Some(StructureFormat::ExtXyz)),
        ("structure.vasp", Some(StructureFormat::Poscar)),
        // Case-insensitive
        ("structure.JSON", Some(StructureFormat::PymatgenJson)),
        ("structure.CIF", Some(StructureFormat::Cif)),
        ("structure.XYZ", Some(StructureFormat::ExtXyz)),
        // POSCAR variants
        ("POSCAR", Some(StructureFormat::Poscar)),
        ("POSCAR.vasp", Some(StructureFormat::Poscar)),
        ("CONTCAR", Some(StructureFormat::Poscar)),
        ("CONTCAR.relax", Some(StructureFormat::Poscar)),
        // LAMMPS
        ("dump.lammpstrj", Some(StructureFormat::LammpsDump)),
        ("traj.lammpstrj.gz", Some(StructureFormat::LammpsDump)),
        ("output.lmp", Some(StructureFormat::LammpsDump)),
        ("output.lmp.gz", Some(StructureFormat::LammpsDump)),
        ("md.dump", Some(StructureFormat::LammpsDump)),
        ("md.dump.gz", Some(StructureFormat::LammpsDump)),
        // Unknown
        ("unknown.txt", None),
    ];
    for (path, expected) in cases {
        assert_eq!(
            StructureFormat::from_path(Path::new(path)),
            *expected,
            "Format detection failed for '{path}'"
        );
    }
}

// === parse_structure() auto-detection tests ===

#[test]
fn test_parse_structure_detects_json() {
    let temp_dir = std::env::temp_dir();
    let path = temp_dir.join("test_struct_detect.json");
    std::fs::write(
        &path,
        r#"{"lattice":{"matrix":[[4,0,0],[0,4,0],[0,0,4]]},"sites":[{"species":[{"element":"Fe"}],"abc":[0,0,0]}]}"#,
    )
    .unwrap();

    let s = parse_structure(&path).unwrap();
    std::fs::remove_file(&path).ok();

    assert_eq!(s.num_sites(), 1);
    assert_eq!(s.species()[0].element, Element::Fe);
}

#[test]
fn test_parse_structure_unknown_extension_error() {
    let path = Path::new("structure.unknown");
    let result = parse_structure(path);
    assert!(result.is_err(), "Unknown extension should return error");
    let err = result.unwrap_err();
    assert!(
        err.to_string().contains("Unknown"),
        "Error should mention unknown format: {err}"
    );
}

// === parse_structures_glob() tests ===

#[test]
fn test_parse_structures_glob_basic() {
    let temp_dir = TempDir::new().unwrap();

    // Create two JSON files
    let json = r#"{"lattice":{"matrix":[[4,0,0],[0,4,0],[0,0,4]]},"sites":[{"species":[{"element":"Cu"}],"abc":[0,0,0]}]}"#;
    std::fs::write(temp_dir.path().join("struct1.json"), json).unwrap();
    std::fs::write(temp_dir.path().join("struct2.json"), json).unwrap();

    let pattern = temp_dir.path().join("*.json").to_string_lossy().to_string();
    let results = parse_structures_glob(&pattern).unwrap();

    assert_eq!(results.len(), 2, "Should find 2 JSON files");
    // TempDir automatically cleans up on drop
}

#[test]
fn test_parse_structures_glob_no_matches() {
    let pattern = "/nonexistent/path/*.json";
    let results = parse_structures_glob(pattern).unwrap();
    assert!(results.is_empty(), "No matches should return empty vec");
}

#[test]
fn test_parse_structures_glob_invalid_pattern() {
    let pattern = "[invalid";
    let result = parse_structures_glob(pattern);
    assert!(result.is_err(), "Invalid glob pattern should return error");
}

// === Pymatgen Edge Case Tests (ported from pymatgen test suite) ===

#[test]
fn test_poscar_edge_cases() {
    // Fluorine element (not confused with False)
    let f_poscar = "F test\n1.0\n4.0 0.0 0.0\n0.0 4.0 0.0\n0.0 0.0 4.0\nF\n2\nDirect\n0.0 0.0 0.0\n0.5 0.5 0.5\n";
    let s = parse_poscar_str(f_poscar).unwrap();
    assert_eq!(s.num_sites(), 2);
    assert!(s.species().iter().all(|sp| sp.element == Element::F));

    // Selective dynamics with F element (T/F flags shouldn't affect element)
    let sd_poscar = "F slab\n1.0\n4.0 0.0 0.0\n0.0 4.0 0.0\n0.0 0.0 10.0\nF\n2\nSelective dynamics\nDirect\n0.0 0.0 0.1 F F F\n0.5 0.5 0.1 T T T\n";
    let s2 = parse_poscar_str(sd_poscar).unwrap();
    assert!(s2.species().iter().all(|sp| sp.element == Element::F));

    // Scale factor 1.1 scales lattice
    let scaled =
        "Scaled\n1.1\n4.0 0.0 0.0\n0.0 4.0 0.0\n0.0 0.0 4.0\nFe\n1\nCartesian\n2.0 2.0 2.0\n";
    assert!((parse_poscar_str(scaled).unwrap().lattice.lengths().x - 4.4).abs() < 1e-6);

    // Negative lattice vectors
    let neg = "Neg\n1.0\n-4.0 0.0 0.0\n0.0 4.0 0.0\n2.0 2.0 4.0\nFe\n1\nDirect\n0.0 0.0 0.0\n";
    assert!(parse_poscar_str(neg).unwrap().lattice.volume().abs() > 0.0);

    // Large structure (27 atoms)
    let mut large =
        String::from("Large\n1.0\n10.0 0.0 0.0\n0.0 10.0 0.0\n0.0 0.0 10.0\nFe\n27\nDirect\n");
    for i in 0..27 {
        large.push_str(&format!("{:.1} 0.0 0.0\n", i as f64 / 27.0));
    }
    assert_eq!(parse_poscar_str(&large).unwrap().num_sites(), 27);
}

#[test]
fn test_extxyz_edge_cases() {
    use std::io::Write;

    // With forces column - verify parsing succeeds with extra per-atom columns
    // Note: per-atom properties (forces) are parsed by extxyz crate but not
    // currently extracted to site_properties; only structure is verified
    let forces = "2\nLattice=\"4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0\" Properties=species:S:1:pos:R:3:forces:R:3\nFe 0.0 0.0 0.0 0.1 0.2 0.3\nFe 2.0 2.0 2.0 -0.1 -0.2 -0.3\n";
    let mut p1 = NamedTempFile::with_suffix(".xyz").unwrap();
    p1.write_all(forces.as_bytes()).unwrap();
    let s_forces = parse_extxyz(p1.path()).unwrap();
    assert_eq!(s_forces.num_sites(), 2);
    assert_eq!(s_forces.species()[0].element, Element::Fe);

    // With energy property - verify global property is extracted
    let energy = "2\nLattice=\"4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0\" energy=-5.5\nH 0.0 0.0 0.0\nH 2.0 2.0 2.0\n";
    let mut p2 = NamedTempFile::with_suffix(".xyz").unwrap();
    p2.write_all(energy.as_bytes()).unwrap();
    let s_energy = parse_extxyz(p2.path()).unwrap();
    assert!(s_energy.properties.contains_key("energy"));
    assert_eq!(
        s_energy.properties.get("energy").unwrap().as_f64(),
        Some(-5.5)
    );
    // NamedTempFile automatically cleans up on drop
}

#[test]
fn test_json_edge_cases() {
    // Oxidation states - verify the oxidation state is parsed
    let oxi = r#"{"lattice":{"matrix":[[4,0,0],[0,4,0],[0,0,4]]},"sites":[{"species":[{"element":"Fe","oxidation_state":2,"occu":1.0}],"abc":[0,0,0]}]}"#;
    let s_oxi = parse_structure_json(oxi).unwrap();
    assert_eq!(s_oxi.num_sites(), 1);
    assert_eq!(s_oxi.species()[0].oxidation_state, Some(2));

    // Disordered site - verify it's recognized as disordered
    let dis = r#"{"lattice":{"matrix":[[4,0,0],[0,4,0],[0,0,4]]},"sites":[{"species":[{"element":"Fe","occu":0.5},{"element":"Mn","occu":0.5}],"abc":[0,0,0]}]}"#;
    let s_dis = parse_structure_json(dis).unwrap();
    assert_eq!(s_dis.num_sites(), 1);
    assert!(!s_dis.is_ordered());
}

// === Structure Writer Tests ===

#[test]
fn test_structure_to_poscar_roundtrip() {
    // NaCl structure - tests format and coordinate roundtrip
    let lattice = Lattice::cubic(5.64);
    let species = vec![
        Species::neutral(Element::Na),
        Species::neutral(Element::Na),
        Species::neutral(Element::Cl),
        Species::neutral(Element::Cl),
    ];
    let coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.0, 0.5, 0.5),
    ];
    let s1 = Structure::new(lattice, species, coords);

    let poscar = structure_to_poscar(&s1, Some("NaCl test"));

    // Verify format
    assert!(poscar.starts_with("NaCl test\n"));
    assert!(poscar.contains("Direct\n"));

    // Roundtrip and compare
    let s2 = parse_poscar_str(&poscar).unwrap();
    assert_eq!(s1.num_sites(), s2.num_sites());
    assert!((s1.lattice.volume() - s2.lattice.volume()).abs() < 1e-6);
    assert_eq!(
        count_element(&s1, Element::Na),
        count_element(&s2, Element::Na)
    );

    // Verify coordinates (POSCAR groups by element, so match by position)
    let (cart1, cart2) = (s1.cart_coords(), s2.cart_coords());
    for c1 in &cart1 {
        assert!(
            cart2.iter().any(|c2| (c1 - c2).norm() < 1e-6),
            "Coordinate {:?} not found",
            c1
        );
    }
}

#[test]
fn test_structure_to_poscar_multi_element() {
    // BaTiO3 - tests element grouping with 3 species
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::Ba),
            Species::neutral(Element::Ti),
            Species::neutral(Element::O),
            Species::neutral(Element::O),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.5, 0.5, 0.0),
            Vector3::new(0.5, 0.0, 0.5),
            Vector3::new(0.0, 0.5, 0.5),
        ],
    );

    let poscar = structure_to_poscar(&s, None);
    let s2 = parse_poscar_str(&poscar).unwrap();

    assert_eq!(s2.num_sites(), 5);
    assert_eq!(count_element(&s2, Element::Ba), 1);
    assert_eq!(count_element(&s2, Element::Ti), 1);
    assert_eq!(count_element(&s2, Element::O), 3);
}

#[test]
fn test_structure_to_extxyz_roundtrip() {
    use std::io::Write;
    // Non-cubic lattice catches vector ordering bugs
    let s1 = Structure::new(
        Lattice::from_parameters(3.0, 4.0, 5.0, 90.0, 90.0, 90.0),
        vec![Species::neutral(Element::H), Species::neutral(Element::O)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let xyz = structure_to_extxyz(&s1, None);

    // Verify format
    let lines: Vec<&str> = xyz.lines().collect();
    assert_eq!(lines[0], "2");
    assert!(lines[1].contains("Lattice="));
    assert!(lines[1].contains("pbc="));

    // Roundtrip via temp file
    let mut temp_file = NamedTempFile::with_suffix(".xyz").unwrap();
    temp_file.write_all(xyz.as_bytes()).unwrap();
    let s2 = parse_extxyz(temp_file.path()).unwrap();

    // Compare lattice (catches ordering bugs)
    let (len1, len2) = (s1.lattice.lengths(), s2.lattice.lengths());
    assert!((len1.x - len2.x).abs() < 1e-6, "a mismatch");
    assert!((len1.y - len2.y).abs() < 1e-6, "b mismatch");
    assert!((len1.z - len2.z).abs() < 1e-6, "c mismatch");

    // Compare species and coords
    assert_eq!(s1.species()[0].element, s2.species()[0].element);
    assert_eq!(s1.species()[1].element, s2.species()[1].element);
    let (cart1, cart2) = (s1.cart_coords(), s2.cart_coords());
    for idx in 0..2 {
        assert!((cart1[idx] - cart2[idx]).norm() < 1e-6);
    }
}

#[test]
fn test_write_structure_auto_format() {
    let temp_dir = TempDir::new().unwrap();
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Cu)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );

    // Test that each format writes non-empty content and can be read back
    for filename in ["test.json", "POSCAR", "test.xyz", "test.cif"] {
        let path = temp_dir.path().join(filename);
        write_structure(&s, &path).unwrap();
        let content = std::fs::read_to_string(&path).unwrap();
        assert!(
            !content.is_empty(),
            "{} should produce non-empty output",
            filename
        );
        // Verify roundtrip: read back and check structure properties
        let read_back = parse_structure(&path).unwrap();
        assert_eq!(
            read_back.num_sites(),
            s.num_sites(),
            "{} roundtrip should preserve atom count",
            filename
        );
    }
}

#[test]
fn test_structure_to_extxyz_escapes_strings() {
    let s = Structure::new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );

    // Test with problematic string values
    let mut props = HashMap::new();
    props.insert("with_quote".to_string(), serde_json::json!("foo\"bar"));
    props.insert(
        "with_newline".to_string(),
        serde_json::json!("line1\nline2"),
    );
    props.insert(
        "with_backslash".to_string(),
        serde_json::json!("path\\to\\file"),
    );

    let xyz = structure_to_extxyz(&s, Some(&props));
    let lines: Vec<&str> = xyz.lines().collect();

    // Output should be exactly 3 lines (count, comment, atom)
    assert_eq!(lines.len(), 3, "Newlines in properties should be escaped");

    // Check escaped values are in comment line
    assert!(
        lines[1].contains(r#"with_quote="foo\"bar""#),
        "Quotes should be escaped"
    );
    assert!(
        lines[1].contains(r#"with_newline="line1\nline2""#),
        "Newlines should be escaped"
    );
    assert!(
        lines[1].contains(r#"with_backslash="path\\to\\file""#),
        "Backslashes should be escaped"
    );
}

// === Fixture-based Roundtrip Tests (matches TypeScript coverage) ===

#[test]
fn test_roundtrip_poscar_batio3_fixture() {
    // Parse BaTiO3 fixture, export, reparse - verifies real-world POSCAR handling
    let fixture = include_str!("../../tests/fixtures/structures/BaTiO3-tetragonal.poscar");
    let s1 = parse_poscar_str(fixture).unwrap();
    let exported = structure_to_poscar(&s1, None);
    let s2 = parse_poscar_str(&exported).unwrap();

    assert_eq!(s1.num_sites(), s2.num_sites());
    assert!((s1.lattice.volume() - s2.lattice.volume()).abs() < 1e-3);
    // Verify all coordinates roundtrip
    let (cart1, cart2) = (s1.cart_coords(), s2.cart_coords());
    for c1 in &cart1 {
        assert!(cart2.iter().any(|c2| (c1 - c2).norm() < 1e-4));
    }
}

#[test]
fn test_roundtrip_cif_tio2_fixture() {
    // Parse TiO2 CIF fixture, export, reparse
    let fixture = include_str!("../../tests/fixtures/structures/TiO2.cif");
    let s1 = crate::io::cif::parse_cif_str(fixture, std::path::Path::new("TiO2.cif")).unwrap();
    let exported = crate::io::cif::structure_to_cif(&s1, None);
    let s2 =
        crate::io::cif::parse_cif_str(&exported, std::path::Path::new("exported.cif")).unwrap();

    assert_eq!(s1.num_sites(), s2.num_sites());
    let (len1, len2) = (s1.lattice.lengths(), s2.lattice.lengths());
    assert!((len1.x - len2.x).abs() < 1e-4);
    assert!((len1.y - len2.y).abs() < 1e-4);
    assert!((len1.z - len2.z).abs() < 1e-4);
}

#[test]
fn test_parse_cif_li10gep2s12_symmetry_expansion() {
    // Li10GeP2S12: P42/nmc (space group 137) with 16 symmetry ops, 9 unique sites
    let fixture = include_str!("../../tests/fixtures/structures/Li10GeP2S12.cif");
    let structure =
        crate::io::cif::parse_cif_str(fixture, std::path::Path::new("Li10GeP2S12.cif")).unwrap();

    // After symmetry expansion: 62 sites (Ge1 and P1 share a position but are separate entries)
    // Element counts match pymatgen: Ge=4, Li=28, P=6, S=24
    assert_eq!(structure.num_sites(), 62);
    assert_eq!(count_element(&structure, Element::Li), 28);
    assert_eq!(count_element(&structure, Element::Ge), 4);
    assert_eq!(count_element(&structure, Element::P), 6);
    assert_eq!(count_element(&structure, Element::S), 24);
}

#[test]
fn test_parse_cif_mof_irmof1_symmetry_expansion() {
    // IRMOF-1: Fm-3m (space group 225) with 192 symmetry ops, 7 unique sites
    let fixture = include_str!("../../tests/fixtures/structures/mof-issue-127.cif");
    let structure =
        crate::io::cif::parse_cif_str(fixture, std::path::Path::new("mof-issue-127.cif")).unwrap();

    // Same as pymatgen: 424 sites (C=192, H=96, O=104, Zn=32)
    assert_eq!(structure.num_sites(), 424);
    assert_eq!(count_element(&structure, Element::Zn), 32);
    assert_eq!(count_element(&structure, Element::O), 104);
    assert_eq!(count_element(&structure, Element::C), 192);
    assert_eq!(count_element(&structure, Element::H), 96);
}

#[test]
fn test_parse_cif_p24ru4_aniso_loop_skipping() {
    // P24Ru4H252C296S24N16: C 1 2/c 1 (space group 15) with 8 symmetry ops, 63 unique sites
    // Also has _atom_site_aniso_* loop that must be skipped to find real coordinates
    let fixture = include_str!("../../tests/fixtures/structures/P24Ru4H252C296S24N16.cif");
    let structure =
        crate::io::cif::parse_cif_str(fixture, std::path::Path::new("P24Ru4H252C296S24N16.cif"))
            .unwrap();

    // Same as pymatgen: 616 sites (C=296, H=252, N=16, P=24, Ru=4, S=24)
    assert_eq!(structure.num_sites(), 616);
    assert_eq!(count_element(&structure, Element::C), 296);
    assert_eq!(count_element(&structure, Element::H), 252);
    assert_eq!(count_element(&structure, Element::Ru), 4);
}

#[test]
fn test_parse_cif_pf_sd_multi_data_blocks() {
    // PF-sd-1601634: CIF with multiple data_ blocks where later blocks have '?' placeholders
    let fixture = include_str!("../../tests/fixtures/structures/PF-sd-1601634.cif");
    let structure =
        crate::io::cif::parse_cif_str(fixture, std::path::Path::new("PF-sd-1601634.cif")).unwrap();

    // First data block has 10 sites with mixed _atom_site and _sm_ headers
    assert_eq!(structure.num_sites(), 10);
    assert_eq!(count_element(&structure, Element::As), 1);
    assert_eq!(count_element(&structure, Element::Pb), 2);
}

#[test]
fn test_roundtrip_extxyz_quartz_fixture() {
    use std::io::Write;
    // Parse quartz extXYZ fixture, export, reparse
    let fixture = include_str!("../../tests/fixtures/structures/quartz.extxyz");
    let mut temp = NamedTempFile::with_suffix(".xyz").unwrap();
    temp.write_all(fixture.as_bytes()).unwrap();
    let s1 = parse_extxyz(temp.path()).unwrap();

    let exported = structure_to_extxyz(&s1, None);
    let mut temp2 = NamedTempFile::with_suffix(".xyz").unwrap();
    temp2.write_all(exported.as_bytes()).unwrap();
    let s2 = parse_extxyz(temp2.path()).unwrap();

    assert_eq!(s1.num_sites(), s2.num_sites());
    let (len1, len2) = (s1.lattice.lengths(), s2.lattice.lengths());
    assert!((len1.x - len2.x).abs() < 1e-4);
    assert!((len1.y - len2.y).abs() < 1e-4);
    assert!((len1.z - len2.z).abs() < 1e-4);
}

#[test]
fn test_roundtrip_json_mp1_fixture() {
    // Parse mp-1 JSON fixture, export, reparse
    let fixture = include_str!("../../tests/fixtures/structures/mp-1.json");
    let s1 = parse_structure_json(fixture).unwrap();
    let exported = structure_to_pymatgen_json(&s1);
    let s2 = parse_structure_json(&exported).unwrap();

    assert_eq!(s1.num_sites(), s2.num_sites());
    assert!((s1.lattice.volume() - s2.lattice.volume()).abs() < 1e-6);
}

// === Triclinic/Non-orthogonal Lattice Tests ===

#[test]
fn test_poscar_triclinic_lattice() {
    // Triclinic lattice with all angles non-90
    let s1 = Structure::new(
        Lattice::from_parameters(3.0, 4.0, 5.0, 80.0, 85.0, 95.0),
        vec![Species::neutral(Element::C)],
        vec![Vector3::new(0.25, 0.5, 0.75)],
    );
    let poscar = structure_to_poscar(&s1, None);
    let s2 = parse_poscar_str(&poscar).unwrap();

    // Verify angles preserved
    let (a1, a2) = (s1.lattice.angles(), s2.lattice.angles());
    assert!((a1.x - a2.x).abs() < 1e-4, "alpha mismatch");
    assert!((a1.y - a2.y).abs() < 1e-4, "beta mismatch");
    assert!((a1.z - a2.z).abs() < 1e-4, "gamma mismatch");
}

#[test]
fn test_cif_triclinic_lattice() {
    let s1 = Structure::try_new(
        Lattice::from_parameters(3.0, 4.0, 5.0, 70.0, 80.0, 100.0),
        vec![Species::neutral(Element::Si)],
        vec![Vector3::new(0.1, 0.2, 0.3)],
    )
    .unwrap();
    let cif = crate::io::cif::structure_to_cif(&s1, None);
    let s2 = crate::io::cif::parse_cif_str(&cif, std::path::Path::new("tri.cif")).unwrap();

    let (a1, a2) = (s1.lattice.angles(), s2.lattice.angles());
    assert!((a1.x - a2.x).abs() < 1e-4);
    assert!((a1.y - a2.y).abs() < 1e-4);
    assert!((a1.z - a2.z).abs() < 1e-4);
}

// === High Precision Tests ===

#[test]
fn test_poscar_high_precision_coords() {
    let s1 = Structure::new(
        Lattice::cubic(10.0),
        vec![Species::neutral(Element::H)],
        vec![Vector3::new(0.123456789, 0.987654321, 0.555555555)],
    );
    let poscar = structure_to_poscar(&s1, None);

    // Verify high precision is preserved in roundtrip (16 decimal format)
    let s2 = parse_poscar_str(&poscar).unwrap();
    let (f1, f2) = (&s1.frac_coords[0], &s2.frac_coords[0]);
    assert!((f1.x - f2.x).abs() < 1e-10, "x precision loss");
    assert!((f1.y - f2.y).abs() < 1e-10, "y precision loss");
    assert!((f1.z - f2.z).abs() < 1e-10, "z precision loss");
}

// === Disordered Site Handling (CIF preserves occupancy) ===

#[test]
fn test_cif_disordered_site_roundtrip() {
    use crate::species::SiteOccupancy;
    // Create structure with disordered site
    let lattice = Lattice::cubic(4.0);
    let disordered = SiteOccupancy::new(vec![
        (Species::neutral(Element::Fe), 0.6),
        (Species::neutral(Element::Co), 0.4),
    ]);
    let s1 = Structure::try_new_from_occupancies(
        lattice,
        vec![disordered],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
    .unwrap();

    let cif = crate::io::cif::structure_to_cif(&s1, None);

    // Verify both species and occupancies appear
    assert!(cif.contains("Fe"));
    assert!(cif.contains("Co"));
    assert!(cif.contains("0.600000") || cif.contains("0.6"));
    assert!(cif.contains("0.400000") || cif.contains("0.4"));
}

// === CIF Data Block Name Sanitization ===

#[test]
fn test_cif_data_name_sanitization() {
    let s = Structure::try_new(
        Lattice::cubic(4.0),
        vec![Species::neutral(Element::H)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    )
    .unwrap();

    // Spaces and hyphens should be replaced with underscores
    let cif = crate::io::cif::structure_to_cif(&s, Some("test-structure name"));
    assert!(cif.starts_with("data_test_structure_name\n"));

    // Formula used when no name provided
    let cif2 = crate::io::cif::structure_to_cif(&s, None);
    assert!(cif2.starts_with("data_H\n"));
}

// === Large Structure Handling ===

#[test]
fn test_large_structure_export() {
    // Create 500-site structure (TypeScript tests 1000, but smaller for speed)
    let lattice = Lattice::cubic(20.0);
    let species: Vec<Species> = (0..500).map(|_| Species::neutral(Element::H)).collect();
    let coords: Vec<Vector3<f64>> = (0..500)
        .map(|idx| {
            Vector3::new(
                (idx % 10) as f64 / 10.0,
                ((idx / 10) % 10) as f64 / 10.0,
                (idx / 100) as f64 / 5.0,
            )
        })
        .collect();
    let s = Structure::new(lattice, species, coords);

    // All formats should handle large structures without panicking
    let poscar = structure_to_poscar(&s, None);
    let xyz = structure_to_extxyz(&s, None);
    let cif = crate::io::cif::structure_to_cif(&s, None);
    let json = structure_to_pymatgen_json(&s);

    // Verify all 500 sites are exported
    let s2 = parse_poscar_str(&poscar).unwrap();
    assert_eq!(s2.num_sites(), 500);

    let xyz_lines: Vec<&str> = xyz.lines().collect();
    assert_eq!(xyz_lines[0], "500"); // First line is atom count

    assert!(cif.matches("H").count() >= 500);
    assert!(json.contains("\"sites\""));
}

// === POSCAR Default Comment (formula) ===

#[test]
fn test_poscar_default_comment_uses_formula() {
    let s = Structure::new(
        Lattice::cubic(5.0),
        vec![
            Species::neutral(Element::Li),
            Species::neutral(Element::Fe),
            Species::neutral(Element::P),
            Species::neutral(Element::O),
        ],
        vec![
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.25, 0.25, 0.25),
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.75, 0.75, 0.75),
        ],
    );
    let poscar = structure_to_poscar(&s, None);

    // First line should be the reduced formula
    let first_line = poscar.lines().next().unwrap();
    assert!(
        first_line.contains("Li") && first_line.contains("Fe"),
        "Default comment should contain formula elements"
    );
}

// === extXYZ Properties Preservation ===

#[test]
fn test_extxyz_preserves_properties() {
    use std::io::Write;
    let mut s = Structure::new(
        Lattice::cubic(5.0),
        vec![Species::neutral(Element::Fe)],
        vec![Vector3::new(0.0, 0.0, 0.0)],
    );
    s.properties
        .insert("energy".to_string(), serde_json::json!(-5.5));
    s.properties
        .insert("config_type".to_string(), serde_json::json!("relaxed"));

    let xyz = structure_to_extxyz(&s, None);

    // Properties should appear in comment line
    assert!(xyz.contains("energy=-5.5") || xyz.contains("energy="));
    assert!(xyz.contains("config_type=\"relaxed\""));

    // Roundtrip preserves properties
    let mut temp = NamedTempFile::with_suffix(".xyz").unwrap();
    temp.write_all(xyz.as_bytes()).unwrap();
    let s2 = parse_extxyz(temp.path()).unwrap();
    assert_eq!(s2.properties.get("energy"), Some(&serde_json::json!(-5.5)));
}

#[test]
fn test_extxyz_preserves_charge() {
    use std::io::Write;
    // Create extXYZ with charge in info
    let xyz = r#"1
Lattice="5.0 0.0 0.0 0.0 5.0 0.0 0.0 0.0 5.0" charge=1.0 Properties=species:S:1:pos:R:3
Li 0.0 0.0 0.0
"#;
    let mut temp = NamedTempFile::with_suffix(".xyz").unwrap();
    temp.write_all(xyz.as_bytes()).unwrap();
    let s = parse_extxyz(temp.path()).unwrap();

    // Charge should be extracted from info, not stored in properties
    assert!((s.charge - 1.0).abs() < 1e-10, "charge should be 1.0");
    assert!(
        !s.properties.contains_key("charge"),
        "charge should not be in properties"
    );
}

// === Molecule IO Tests ===

fn water_molecule() -> Structure {
    let species = vec![
        Species::neutral(Element::O),
        Species::neutral(Element::H),
        Species::neutral(Element::H),
    ];
    let coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.96, 0.0, 0.0),
        Vector3::new(-0.24, 0.93, 0.0),
    ];
    Structure::try_new_molecule(species, coords, 0.0, std::collections::HashMap::new()).unwrap()
}

#[test]
fn test_parse_molecule_json() {
    // Water molecule
    let json = r#"{
        "sites": [
            {"species": [{"element": "O"}], "xyz": [0, 0, 0]},
            {"species": [{"element": "H"}], "xyz": [0.96, 0, 0]},
            {"species": [{"element": "H"}], "xyz": [-0.24, 0.93, 0]}
        ],
        "charge": 0
    }"#;
    let mol = parse_molecule_json(json).unwrap();
    assert_eq!(mol.num_sites(), 3);
    assert_eq!(mol.composition().reduced_formula(), "H2O");
    let cart = mol.cart_coords();
    assert!((cart[1].x - 0.96).abs() < 1e-10);
    // Charged ion
    let ion_json =
        r#"{"sites": [{"species": [{"element": "Na"}], "xyz": [0, 0, 0]}], "charge": 1.0}"#;
    let ion = parse_molecule_json(ion_json).unwrap();
    assert!((ion.charge - 1.0).abs() < 1e-10);
}

#[test]
fn test_parse_molecule_json_with_oxidation_states() {
    let json = r#"{
        "sites": [
            {"species": [{"element": "Na", "oxidation_state": 1}], "xyz": [0, 0, 0]},
            {"species": [{"element": "Cl", "oxidation_state": -1}], "xyz": [2.0, 0, 0]}
        ],
        "charge": 0
    }"#;

    let mol = parse_molecule_json(json).unwrap();
    assert_eq!(mol.species()[0].oxidation_state, Some(1));
    assert_eq!(mol.species()[1].oxidation_state, Some(-1));
}

#[test]
fn test_molecule_to_pymatgen_json_roundtrip() {
    let mol1 = water_molecule();
    let json = molecule_to_pymatgen_json(&mol1);
    let mol2 = parse_molecule_json(&json).unwrap();

    assert_eq!(mol1.num_sites(), mol2.num_sites());
    assert_eq!(
        mol1.composition().reduced_formula(),
        mol2.composition().reduced_formula()
    );

    // Check coordinates roundtrip
    let cart1 = mol1.cart_coords();
    let cart2 = mol2.cart_coords();
    for idx in 0..mol1.num_sites() {
        assert!((cart1[idx] - cart2[idx]).norm() < 1e-6);
    }
}

#[test]
fn test_molecule_to_xyz() {
    let mol = water_molecule();
    // Default comment (formula)
    let xyz = molecule_to_xyz(&mol, None);
    let lines: Vec<&str> = xyz.lines().collect();
    assert_eq!(lines[0], "3");
    assert_eq!(lines[1], "H2O");
    // Custom comment
    let xyz2 = molecule_to_xyz(&mol, Some("Water"));
    assert!(xyz2.lines().nth(1).unwrap() == "Water");
    // Round-trip preserves coordinates
    let reparsed = parse_xyz_str(&xyz).unwrap();
    let cart_orig = mol.cart_coords();
    let cart_reparsed = reparsed.cart_coords();
    for idx in 0..mol.num_sites() {
        assert!((cart_orig[idx] - cart_reparsed[idx]).norm() < 1e-10);
    }
}

#[test]
fn test_parse_xyz_str() {
    let xyz = "3\nWater\nO 0.0 0.0 0.0\nH 0.96 0.0 0.0\nH -0.24 0.93 0.0\n";
    let mol = parse_xyz_str(xyz).unwrap();

    assert_eq!(mol.num_sites(), 3);
    assert_eq!(mol.species()[0].element, Element::O);
    assert_eq!(mol.composition().reduced_formula(), "H2O");
}

#[test]
fn test_xyz_roundtrip() {
    use std::io::Write;

    let mol1 = water_molecule();
    let xyz = molecule_to_xyz(&mol1, None);

    // Write to temp file and parse back
    let mut temp = NamedTempFile::with_suffix(".xyz").unwrap();
    temp.write_all(xyz.as_bytes()).unwrap();
    let mol2 = parse_xyz(temp.path()).unwrap();

    assert_eq!(mol1.num_sites(), mol2.num_sites());
    let cart1 = mol1.cart_coords();
    let cart2 = mol2.cart_coords();
    for idx in 0..mol1.num_sites() {
        assert!((cart1[idx] - cart2[idx]).norm() < 1e-6);
    }
}

#[test]
fn test_molecule_to_extxyz() {
    let mut mol = water_molecule();
    mol.properties
        .insert("energy".to_string(), serde_json::json!(-10.5));
    mol.charge = -1.0;

    let xyz = molecule_to_extxyz(&mol, None);

    let lines: Vec<&str> = xyz.lines().collect();
    assert_eq!(lines[0], "3");
    assert!(lines[1].contains("pbc=\"F F F\""));
    assert!(lines[1].contains("charge=-1"));
    assert!(lines[1].contains("energy=-10.5"));
}

#[test]
#[allow(deprecated)]
fn test_parse_xyz_flexible_with_lattice() {
    use std::io::Write;

    // extXYZ with lattice should return Structure
    let extxyz = r#"1
Lattice="4.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 4.0"
Fe 2.0 2.0 2.0
"#;
    let mut temp = NamedTempFile::with_suffix(".xyz").unwrap();
    temp.write_all(extxyz.as_bytes()).unwrap();

    match parse_xyz_flexible(temp.path()).unwrap() {
        StructureOrMolecule::Structure(s) => {
            assert_eq!(s.num_sites(), 1);
            assert_eq!(s.species()[0].element, Element::Fe);
        }
        StructureOrMolecule::Molecule(_) => {
            panic!("Expected Structure, got Molecule");
        }
    }
}

#[test]
#[allow(deprecated)]
fn test_parse_xyz_flexible_without_lattice() {
    use std::io::Write;

    // XYZ without lattice should return Molecule
    let xyz = "3\nWater\nO 0.0 0.0 0.0\nH 0.96 0.0 0.0\nH -0.24 0.93 0.0\n";
    let mut temp = NamedTempFile::with_suffix(".xyz").unwrap();
    temp.write_all(xyz.as_bytes()).unwrap();

    match parse_xyz_flexible(temp.path()).unwrap() {
        StructureOrMolecule::Molecule(m) => {
            assert_eq!(m.num_sites(), 3);
            assert_eq!(m.composition().reduced_formula(), "H2O");
        }
        StructureOrMolecule::Structure(_) => {
            panic!("Expected Molecule, got Structure");
        }
    }
}

#[test]
fn test_write_xyz() {
    let mol = water_molecule();
    let temp_dir = TempDir::new().unwrap();
    let path = temp_dir.path().join("water.xyz");

    write_xyz(&mol, &path, Some("Test water")).unwrap();

    let content = std::fs::read_to_string(&path).unwrap();
    assert!(content.starts_with("3\n"));
    assert!(content.contains("Test water"));
}

#[test]
fn test_parse_molecule_json_empty_species_error() {
    let json = r#"{
        "sites": [{"species": [], "xyz": [0, 0, 0]}],
        "charge": 0
    }"#;

    let result = parse_molecule_json(json);
    assert!(result.is_err());
}

#[test]
fn test_parse_molecule_json_abc_only_error() {
    // Molecules require xyz (Cartesian) coords - abc (fractional) coords are invalid
    let json = r#"{
        "sites": [{"species": [{"element": "H"}], "abc": [0.5, 0.5, 0.5]}],
        "charge": 0
    }"#;
    let result = parse_molecule_json(json);
    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("xyz"));
}

#[test]
fn test_parse_molecule_json_with_properties() {
    let json = r#"{
        "sites": [{"species": [{"element": "C"}], "xyz": [0, 0, 0]}],
        "charge": 0,
        "properties": {"source": "test", "computed": true}
    }"#;

    let mol = parse_molecule_json(json).unwrap();
    assert_eq!(
        mol.properties.get("source"),
        Some(&serde_json::json!("test"))
    );
    assert_eq!(
        mol.properties.get("computed"),
        Some(&serde_json::json!(true))
    );
}

#[test]
fn test_molecule_json_with_labels() {
    let json = r#"{
        "sites": [
            {"species": [{"element": "C"}], "xyz": [0, 0, 0], "label": "C1"},
            {"species": [{"element": "H"}], "xyz": [1, 0, 0], "label": "H1"}
        ],
        "charge": 0
    }"#;

    let mol = parse_molecule_json(json).unwrap();

    // Check labels are preserved in site properties
    assert_eq!(
        mol.site_occupancies[0]
            .properties
            .get("label")
            .and_then(|v| v.as_str()),
        Some("C1")
    );
    assert_eq!(
        mol.site_occupancies[1]
            .properties
            .get("label")
            .and_then(|v| v.as_str()),
        Some("H1")
    );

    // Roundtrip should preserve labels
    let json_out = molecule_to_pymatgen_json(&mol);
    assert!(json_out.contains("C1"));
    assert!(json_out.contains("H1"));
}

// === ASE Atoms Dict Conversion Tests ===

#[test]
#[allow(deprecated)]
fn test_parse_ase_atoms_structure() {
    let json = r#"{
        "symbols": ["Fe", "Fe"],
        "positions": [[0, 0, 0], [1.435, 1.435, 1.435]],
        "cell": [[2.87, 0, 0], [0, 2.87, 0], [0, 0, 2.87]],
        "pbc": [true, true, true]
    }"#;

    match parse_ase_atoms_json(json).unwrap() {
        StructureOrMolecule::Structure(s) => {
            assert_eq!(s.num_sites(), 2);
            assert_eq!(s.species()[0].element, Element::Fe);
            assert!((s.lattice.volume() - 2.87_f64.powi(3)).abs() < 1e-6);
            // Verify pbc is correctly set on Structure
            assert_eq!(s.pbc, [true, true, true]);
            assert!(s.is_periodic());
            assert!(!s.is_molecule());
        }
        StructureOrMolecule::Molecule(_) => {
            panic!("Expected Structure, got Molecule");
        }
    }
}

#[test]
#[allow(deprecated)]
fn test_parse_ase_atoms_partial_pbc() {
    // 2D material with pbc only in x and y directions
    let json = r#"{
        "symbols": ["C", "C"],
        "positions": [[0, 0, 0], [1.23, 0.71, 0]],
        "cell": [[2.46, 0, 0], [1.23, 2.13, 0], [0, 0, 20]],
        "pbc": [true, true, false]
    }"#;

    match parse_ase_atoms_json(json).unwrap() {
        StructureOrMolecule::Structure(s) => {
            assert_eq!(s.num_sites(), 2);
            // Verify pbc is correctly propagated to Structure
            assert_eq!(s.pbc, [true, true, false]);
            assert_eq!(s.lattice.pbc, [true, true, false]);
            // is_periodic should be true (any pbc dimension)
            assert!(s.is_periodic());
            assert!(!s.is_molecule());
        }
        StructureOrMolecule::Molecule(_) => {
            panic!("Expected Structure with partial pbc, got Molecule");
        }
    }
}

#[test]
#[allow(deprecated)]
fn test_parse_ase_atoms_molecule() {
    let json = r#"{
        "symbols": ["O", "H", "H"],
        "positions": [[0, 0, 0], [0.96, 0, 0], [-0.24, 0.93, 0]],
        "pbc": [false, false, false],
        "info": {"charge": 0, "energy": -10.5}
    }"#;

    match parse_ase_atoms_json(json).unwrap() {
        StructureOrMolecule::Molecule(m) => {
            assert_eq!(m.num_sites(), 3);
            assert_eq!(m.composition().reduced_formula(), "H2O");
            assert_eq!(m.properties.get("energy"), Some(&serde_json::json!(-10.5)));
        }
        StructureOrMolecule::Structure(_) => {
            panic!("Expected Molecule, got Structure");
        }
    }
}

#[test]
#[allow(deprecated)]
fn test_parse_ase_atoms_molecule_no_cell() {
    // ASE molecules often have null cell
    let json = r#"{
        "symbols": ["C", "H", "H", "H", "H"],
        "positions": [[0, 0, 0], [1.09, 0, 0], [-0.36, 1.03, 0], [-0.36, -0.51, 0.89], [-0.36, -0.51, -0.89]]
    }"#;

    match parse_ase_atoms_json(json).unwrap() {
        StructureOrMolecule::Molecule(m) => {
            assert_eq!(m.num_sites(), 5);
            // Composition should have 1 C and 4 H regardless of formula ordering
            let comp = m.composition();
            assert!((comp.get_element_total(Element::C) - 1.0).abs() < 1e-10);
            assert!((comp.get_element_total(Element::H) - 4.0).abs() < 1e-10);
        }
        StructureOrMolecule::Structure(_) => {
            panic!("Expected Molecule, got Structure");
        }
    }
}

#[test]
fn test_structure_to_ase_atoms_dict() {
    let lattice = Lattice::cubic(4.0);
    let s = Structure::new(
        lattice,
        vec![Species::neutral(Element::Cu), Species::neutral(Element::Cu)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let ase_dict = structure_to_ase_atoms_dict(&s);

    assert_eq!(
        ase_dict["symbols"].as_array().unwrap(),
        &vec![serde_json::json!("Cu"), serde_json::json!("Cu")]
    );
    assert!(ase_dict["cell"].is_array());
    assert_eq!(ase_dict["pbc"], serde_json::json!([true, true, true]));
}

#[test]
fn test_structure_to_ase_atoms_dict_with_charge() {
    // Charged structure should include charge in info dict
    let lattice = Lattice::cubic(4.0);
    let s = Structure::try_new_full(
        lattice,
        vec![
            SiteOccupancy::ordered(Species::neutral(Element::Li)),
            SiteOccupancy::ordered(Species::neutral(Element::Li)),
        ],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
        [true, true, true],
        1.0, // positive charge
        HashMap::new(),
    )
    .unwrap();

    let ase_dict = structure_to_ase_atoms_dict(&s);

    // Charge should be in info dict
    assert_eq!(ase_dict["info"]["charge"], serde_json::json!(1.0));
}

#[test]
fn test_structure_to_ase_atoms_dict_zero_charge() {
    // Zero charge should NOT be in info dict
    let lattice = Lattice::cubic(4.0);
    let s = Structure::new(
        lattice,
        vec![Species::neutral(Element::Cu), Species::neutral(Element::Cu)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let ase_dict = structure_to_ase_atoms_dict(&s);

    // info dict should not have charge key when charge is zero
    assert!(!ase_dict["info"].as_object().unwrap().contains_key("charge"));
}

#[test]
fn test_molecule_to_ase_atoms_dict() {
    let mol = water_molecule();
    let ase_dict = molecule_to_ase_atoms_dict(&mol);

    assert_eq!(
        ase_dict["symbols"].as_array().unwrap(),
        &vec![
            serde_json::json!("O"),
            serde_json::json!("H"),
            serde_json::json!("H")
        ]
    );
    assert!(ase_dict["cell"].is_null());
    assert_eq!(ase_dict["pbc"], serde_json::json!([false, false, false]));
}

#[test]
#[allow(deprecated)]
fn test_ase_atoms_roundtrip_structure() {
    let s1 = Structure::new(
        Lattice::cubic(5.64),
        vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
        vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
    );

    let ase_dict = structure_to_ase_atoms_dict(&s1);
    let json = serde_json::to_string(&ase_dict).unwrap();

    match parse_ase_atoms_json(&json).unwrap() {
        StructureOrMolecule::Structure(s2) => {
            assert_eq!(s1.num_sites(), s2.num_sites());
            assert!((s1.lattice.volume() - s2.lattice.volume()).abs() < 1e-6);
            // Check positions (Cartesian)
            let (cart1, cart2) = (s1.cart_coords(), s2.cart_coords());
            for idx in 0..s1.num_sites() {
                assert!((cart1[idx] - cart2[idx]).norm() < 1e-6);
            }
        }
        StructureOrMolecule::Molecule(_) => {
            panic!("Expected Structure, got Molecule");
        }
    }
}

#[test]
#[allow(deprecated)]
fn test_ase_atoms_roundtrip_molecule() {
    let m1 = water_molecule();

    let ase_dict = molecule_to_ase_atoms_dict(&m1);
    let json = serde_json::to_string(&ase_dict).unwrap();

    match parse_ase_atoms_json(&json).unwrap() {
        StructureOrMolecule::Molecule(m2) => {
            assert_eq!(m1.num_sites(), m2.num_sites());
            let cart1 = m1.cart_coords();
            let cart2 = m2.cart_coords();
            for idx in 0..m1.num_sites() {
                assert!((cart1[idx] - cart2[idx]).norm() < 1e-6);
            }
        }
        StructureOrMolecule::Structure(_) => {
            panic!("Expected Molecule, got Structure");
        }
    }
}

#[test]
fn test_batch_structures_to_ase_dicts() {
    let structures = vec![
        Structure::new(
            Lattice::cubic(4.0),
            vec![Species::neutral(Element::Fe)],
            vec![Vector3::zeros()],
        ),
        Structure::new(
            Lattice::cubic(5.0),
            vec![Species::neutral(Element::Cu)],
            vec![Vector3::zeros()],
        ),
    ];

    let dicts = structures_to_ase_atoms_dicts(&structures);
    assert_eq!(dicts.len(), 2);
    assert_eq!(dicts[0]["symbols"], serde_json::json!(["Fe"]));
    assert_eq!(dicts[1]["symbols"], serde_json::json!(["Cu"]));
}

#[test]
fn test_ase_to_pymatgen_conversion() {
    // Structure
    let ase_struct = r#"{
        "symbols": ["Si", "Si"],
        "positions": [[0, 0, 0], [1.36, 1.36, 1.36]],
        "cell": [[2.72, 2.72, 0], [2.72, 0, 2.72], [0, 2.72, 2.72]],
        "pbc": [true, true, true]
    }"#;

    let pymatgen_json = ase_atoms_to_pymatgen_json(ase_struct).unwrap();
    assert!(pymatgen_json.contains("\"@class\":\"Structure\""));
    assert!(pymatgen_json.contains("\"lattice\""));

    // Molecule
    let ase_mol = r#"{
        "symbols": ["H", "H"],
        "positions": [[0, 0, 0], [0.74, 0, 0]],
        "pbc": [false, false, false]
    }"#;

    let pymatgen_json = ase_atoms_to_pymatgen_json(ase_mol).unwrap();
    assert!(pymatgen_json.contains("\"@class\":\"Molecule\""));
}

#[test]
#[allow(deprecated)]
fn test_ase_atoms_with_info() {
    let json = r#"{
        "symbols": ["Fe"],
        "positions": [[0, 0, 0]],
        "cell": [[2.87, 0, 0], [0, 2.87, 0], [0, 0, 2.87]],
        "pbc": [true, true, true],
        "info": {"energy": -5.5, "forces": [[0.1, 0.2, 0.3]], "config_type": "relaxed"}
    }"#;

    match parse_ase_atoms_json(json).unwrap() {
        StructureOrMolecule::Structure(s) => {
            assert_eq!(s.properties.get("energy"), Some(&serde_json::json!(-5.5)));
            assert_eq!(
                s.properties.get("config_type"),
                Some(&serde_json::json!("relaxed"))
            );
        }
        StructureOrMolecule::Molecule(_) => {
            panic!("Expected Structure, got Molecule");
        }
    }
}

#[test]
fn test_ase_atoms_length_mismatch_error() {
    let json = r#"{
        "symbols": ["Fe", "O"],
        "positions": [[0, 0, 0]]
    }"#;

    let result = parse_ase_atoms_json(json);
    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("same length"));
}

// --- Tests for expanded disorder merging (co-located sites) ---

#[test]
fn test_merge_colocated_sites_basic() {
    // Two different elements at the exact same fractional coordinates
    // with partial occupancies. Should be merged into one site.
    let json = r#"{
        "lattice": {"matrix": [[5,0,0],[0,5,0],[0,0,5]]},
        "sites": [
            {"species": [{"element": "K", "occu": 0.3}], "abc": [0,0,0]},
            {"species": [{"element": "Ba", "occu": 0.7}], "abc": [0,0,0]},
            {"species": [{"element": "Fe"}], "abc": [0.5,0.5,0.5]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    // K and Ba at [0,0,0] should be merged into 1 site, Fe stays separate
    assert_eq!(
        structure.num_sites(),
        2,
        "co-located K+Ba should merge into 1 site"
    );
    // The merged site should have Ba as dominant (0.7 > 0.3)
    assert_eq!(
        structure.site_occupancies[0].dominant_species().element,
        Element::Ba
    );
    // It should contain both species
    assert_eq!(structure.site_occupancies[0].species.len(), 2);
    // Total occupancy at merged site
    let total_occ = structure.site_occupancies[0].total_occupancy();
    assert!(
        (total_occ - 1.0).abs() < 1e-10,
        "occupancies should sum to 1.0"
    );
    // Fe site should be ordered
    assert!(structure.site_occupancies[1].is_ordered());
    assert_eq!(
        structure.site_occupancies[1].dominant_species().element,
        Element::Fe
    );
}

#[test]
fn test_merge_colocated_four_species_per_site() {
    // Reproduces the exact data format from SourceDocsUnique that caused
    // NaN forces: 4 elements (K, Ba, Gd, Eu) each at the same 4 positions
    // with partial occupancies, totaling 24 sites that should merge to 12.
    let json = r#"{
        "lattice": {"matrix": [[6.156,0,3.77e-16],[-3.77e-16,6.156,3.77e-16],[0,0,6.156]]},
        "sites": [
            {"species": [{"element": "K",  "occu": 0.06}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "K",  "occu": 0.06}], "abc": [0.5, 0.5, 0.0]},
            {"species": [{"element": "K",  "occu": 0.06}], "abc": [0.5, 0.0, 0.5]},
            {"species": [{"element": "K",  "occu": 0.06}], "abc": [0.0, 0.5, 0.5]},
            {"species": [{"element": "Ba", "occu": 0.88}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Ba", "occu": 0.88}], "abc": [0.5, 0.5, 0.0]},
            {"species": [{"element": "Ba", "occu": 0.88}], "abc": [0.5, 0.0, 0.5]},
            {"species": [{"element": "Ba", "occu": 0.88}], "abc": [0.0, 0.5, 0.5]},
            {"species": [{"element": "Gd", "occu": 0.05}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Gd", "occu": 0.05}], "abc": [0.5, 0.5, 0.0]},
            {"species": [{"element": "Gd", "occu": 0.05}], "abc": [0.5, 0.0, 0.5]},
            {"species": [{"element": "Gd", "occu": 0.05}], "abc": [0.0, 0.5, 0.5]},
            {"species": [{"element": "F"}], "abc": [0.25, 0.25, 0.25]},
            {"species": [{"element": "F"}], "abc": [0.75, 0.75, 0.25]},
            {"species": [{"element": "F"}], "abc": [0.75, 0.25, 0.75]},
            {"species": [{"element": "F"}], "abc": [0.25, 0.75, 0.75]},
            {"species": [{"element": "F"}], "abc": [0.75, 0.75, 0.75]},
            {"species": [{"element": "F"}], "abc": [0.25, 0.25, 0.75]},
            {"species": [{"element": "F"}], "abc": [0.25, 0.75, 0.25]},
            {"species": [{"element": "F"}], "abc": [0.75, 0.25, 0.25]},
            {"species": [{"element": "Eu", "occu": 0.01}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Eu", "occu": 0.01}], "abc": [0.5, 0.5, 0.0]},
            {"species": [{"element": "Eu", "occu": 0.01}], "abc": [0.5, 0.0, 0.5]},
            {"species": [{"element": "Eu", "occu": 0.01}], "abc": [0.0, 0.5, 0.5]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    // 4 positions with 4 species each = 16 expanded -> 4 merged + 8 F = 12 sites
    assert_eq!(
        structure.num_sites(),
        12,
        "24 expanded sites should merge to 12 (4 disordered + 8 ordered F)"
    );

    // Check the merged disordered sites have 4 species each
    let disordered_sites: Vec<_> = structure
        .site_occupancies
        .iter()
        .filter(|so| !so.is_ordered())
        .collect();
    assert_eq!(disordered_sites.len(), 4, "should have 4 disordered sites");
    for site in &disordered_sites {
        assert_eq!(
            site.species.len(),
            4,
            "each disordered site should have 4 species"
        );
        // Ba should be dominant (0.88)
        assert_eq!(site.dominant_species().element, Element::Ba);
        // Total occupancy should be 0.06 + 0.88 + 0.05 + 0.01 = 1.0
        let total = site.total_occupancy();
        assert!(
            (total - 1.0).abs() < 1e-10,
            "occupancies should sum to 1.0, got {total}"
        );
    }

    // Check F sites are ordered and unchanged
    let ordered_sites: Vec<_> = structure
        .site_occupancies
        .iter()
        .filter(|so| so.is_ordered())
        .collect();
    assert_eq!(ordered_sites.len(), 8, "should have 8 ordered F sites");
    for site in &ordered_sites {
        assert_eq!(site.dominant_species().element, Element::F);
    }
}

#[test]
fn test_merge_colocated_preserves_cartesian_coords() {
    // After merging, the Cartesian coordinates should not have overlapping
    // atoms (the original bug: overlapping atoms caused NaN in NequIP).
    let json = r#"{
        "lattice": {"matrix": [[5,0,0],[0,5,0],[0,0,5]]},
        "sites": [
            {"species": [{"element": "Fe", "occu": 0.6}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Co", "occu": 0.4}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "O"}],  "abc": [0.5, 0.5, 0.5]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    assert_eq!(structure.num_sites(), 2);

    // Verify no overlapping Cartesian coordinates
    let coords = structure.cart_coords();
    let dist = (coords[0] - coords[1]).norm();
    assert!(
        dist > 1.0,
        "merged sites should not overlap, got dist={dist}"
    );
}

#[test]
fn test_merge_colocated_no_merge_for_ordered() {
    // Fully ordered structure (no partial occupancy, no duplicate coords)
    // should be unchanged.
    let json = r#"{
        "lattice": {"matrix": [[4,0,0],[0,4,0],[0,0,4]]},
        "sites": [
            {"species": [{"element": "Na"}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Cl"}], "abc": [0.5, 0.5, 0.5]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    assert_eq!(structure.num_sites(), 2);
    assert!(structure.site_occupancies[0].is_ordered());
    assert!(structure.site_occupancies[1].is_ordered());
}

#[test]
fn test_merge_colocated_same_element_sums_occupancy() {
    // Same element at same position should sum occupancies.
    let json = r#"{
        "lattice": {"matrix": [[5,0,0],[0,5,0],[0,0,5]]},
        "sites": [
            {"species": [{"element": "Fe", "occu": 0.5}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Fe", "occu": 0.5}], "abc": [0.0, 0.0, 0.0]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    assert_eq!(
        structure.num_sites(),
        1,
        "same element at same position should merge"
    );
    // Occupancy should be summed
    assert_eq!(structure.site_occupancies[0].species.len(), 1);
    let (sp, occ) = &structure.site_occupancies[0].species[0];
    assert_eq!(sp.element, Element::Fe);
    assert!((occ - 1.0).abs() < 1e-10, "occupancies should sum to 1.0");
}

#[test]
fn test_merge_colocated_torch_sim_state_no_overlap() {
    // End-to-end test: ensure the TorchSimState from a merged structure
    // has no overlapping atoms (the actual failure mode).
    let json = r#"{
        "lattice": {"matrix": [[6,0,0],[0,6,0],[0,0,6]]},
        "sites": [
            {"species": [{"element": "K",  "occu": 0.1}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "Ba", "occu": 0.9}], "abc": [0.0, 0.0, 0.0]},
            {"species": [{"element": "F"}],  "abc": [0.25, 0.25, 0.25]},
            {"species": [{"element": "F"}],  "abc": [0.75, 0.75, 0.75]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    assert_eq!(structure.num_sites(), 3, "K+Ba merge into 1 + 2 F = 3");

    let state = structure_to_torch_sim_state(&structure);
    assert_eq!(
        state.positions.len(),
        3,
        "TorchSimState should have 3 atoms"
    );

    // Check no positions overlap
    for atom_idx in 0..state.positions.len() {
        for other_idx in (atom_idx + 1)..state.positions.len() {
            let pos_a = state.positions[atom_idx];
            let pos_b = state.positions[other_idx];
            let dist = ((pos_a[0] - pos_b[0]).powi(2)
                + (pos_a[1] - pos_b[1]).powi(2)
                + (pos_a[2] - pos_b[2]).powi(2))
            .sqrt();
            assert!(
                dist > 0.1,
                "atoms {atom_idx} and {other_idx} overlap at dist={dist}"
            );
        }
    }

    // Dominant species (Ba, 0.9) should be used for atomic number
    assert_eq!(
        state.atomic_numbers[0], 56,
        "Ba should be dominant at merged site"
    );
}

#[test]
fn test_merge_disabled_with_zero_tolerance() {
    // When merge_tol=0.0, no merging should occur even for identical coords.
    let json = r#"{
        "lattice": {"matrix": [[5,0,0],[0,5,0],[0,0,5]]},
        "sites": [
            {"species": [{"element": "K",  "occu": 0.3}], "abc": [0,0,0]},
            {"species": [{"element": "Ba", "occu": 0.7}], "abc": [0,0,0]}
        ]
    }"#;

    let structure = parse_structure_json_with_merge_tol(json, 0.0).unwrap();
    assert_eq!(
        structure.num_sites(),
        2,
        "merge_tol=0 should keep all sites separate"
    );
}

#[test]
fn test_merge_colocated_near_zero_coords() {
    // Test with coordinates very close to zero (like 6.16e-33) that
    // appeared in real MongoDB data.
    let json = r#"{
        "lattice": {"matrix": [[5,0,0],[0,5,0],[0,0,5]]},
        "sites": [
            {"species": [{"element": "K",  "occu": 0.06}], "abc": [6.16e-33, 0.5, 0.5]},
            {"species": [{"element": "Ba", "occu": 0.88}], "abc": [6.16e-33, 0.5, 0.5]},
            {"species": [{"element": "Gd", "occu": 0.05}], "abc": [6.16e-33, 0.5, 0.5]},
            {"species": [{"element": "Eu", "occu": 0.01}], "abc": [6.16e-33, 0.5, 0.5]},
            {"species": [{"element": "F"}],  "abc": [0.25, 0.25, 0.25]}
        ]
    }"#;

    let structure = parse_structure_json(json).unwrap();
    assert_eq!(
        structure.num_sites(),
        2,
        "4 co-located sites + 1 F = 2 sites"
    );
    assert_eq!(
        structure.site_occupancies[0].species.len(),
        4,
        "merged site should have K, Ba, Gd, Eu"
    );
    assert_eq!(
        structure.site_occupancies[0].dominant_species().element,
        Element::Ba,
        "Ba (0.88) should be dominant"
    );
}
