use super::*;
use crate::cell_ops::perpendicular_distances;
use crate::element::Element;
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::Vector3;

fn make_nacl() -> Structure {
    let lattice = Lattice::cubic(5.64);
    let species = vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)];
    let coords = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    Structure::new(lattice, species, coords)
}

fn make_fcc_cu() -> Structure {
    let lattice = Lattice::cubic(3.6);
    let species = vec![
        Species::neutral(Element::Cu),
        Species::neutral(Element::Cu),
        Species::neutral(Element::Cu),
        Species::neutral(Element::Cu),
    ];
    let coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.0, 0.5, 0.5),
    ];
    Structure::new(lattice, species, coords)
}

#[test]
fn test_create_vacancy() {
    let structure = make_nacl();
    assert_eq!(structure.num_sites(), 2);

    let defect = create_vacancy(&structure, 0).unwrap();
    assert_eq!(defect.structure.num_sites(), 1);
    assert_eq!(defect.defect.defect_type, DefectType::Vacancy);
    assert_eq!(defect.defect.original_species.unwrap().element, Element::Na);
}

#[test]
fn test_create_substitution() {
    let structure = make_nacl();
    let new_species = Species::neutral(Element::K);

    let defect = create_substitution(&structure, 0, new_species).unwrap();
    assert_eq!(defect.structure.num_sites(), 2);
    assert_eq!(defect.defect.defect_type, DefectType::Substitution);
    assert_eq!(defect.defect.species.unwrap().element, Element::K);
    assert_eq!(defect.defect.original_species.unwrap().element, Element::Na);

    // Verify the species was actually changed
    assert_eq!(
        defect.structure.site_occupancies[0]
            .dominant_species()
            .element,
        Element::K
    );
}

#[test]
fn test_create_antisite() {
    let structure = make_nacl();

    let swapped = create_antisite_pair(&structure, 0, 1).unwrap();
    assert_eq!(swapped.num_sites(), 2);

    // Na and Cl should be swapped
    assert_eq!(
        swapped.site_occupancies[0].dominant_species().element,
        Element::Cl
    );
    assert_eq!(
        swapped.site_occupancies[1].dominant_species().element,
        Element::Na
    );
}

#[test]
fn test_create_interstitial() {
    let structure = make_nacl();
    let species = Species::neutral(Element::Li);
    let position = Vector3::new(0.25, 0.25, 0.25);

    let defect = create_interstitial(&structure, position, species).unwrap();
    assert_eq!(defect.structure.num_sites(), 3);
    assert_eq!(defect.defect.defect_type, DefectType::Interstitial);
}

#[test]
fn test_classify_interstitial_site() {
    assert_eq!(
        classify_interstitial_site(3),
        InterstitialSiteType::Trigonal
    );
    assert_eq!(
        classify_interstitial_site(4),
        InterstitialSiteType::Tetrahedral
    );
    assert_eq!(
        classify_interstitial_site(5),
        InterstitialSiteType::SquarePyramidal
    );
    assert_eq!(
        classify_interstitial_site(6),
        InterstitialSiteType::Octahedral
    );
    assert_eq!(classify_interstitial_site(8), InterstitialSiteType::Cubic);
    assert_eq!(
        classify_interstitial_site(12),
        InterstitialSiteType::Cuboctahedral
    );
    assert_eq!(classify_interstitial_site(7), InterstitialSiteType::Other);
}

#[test]
fn test_find_defect_supercell() {
    let structure = make_nacl();
    let config = DefectSupercellConfig {
        min_distance: 10.0,
        max_atoms: 200,
        cubic_preference: 0.5,
    };

    let matrix = find_defect_supercell(&structure, &config).unwrap();

    // Should be at least 2x2x2 to satisfy min_distance for NaCl (a=5.64)
    let det = matrix[0][0] * matrix[1][1] * matrix[2][2];
    assert!(det >= 8);

    // Check perpendicular distances
    let super_lattice = Lattice::cubic(5.64 * matrix[0][0] as f64);
    let perp = perpendicular_distances(&super_lattice);
    assert!(perp.min() >= config.min_distance);
}

#[test]
fn test_vacancy_out_of_bounds() {
    let structure = make_nacl();
    let result = create_vacancy(&structure, 10);
    assert!(result.is_err());
}

#[test]
fn test_find_defect_supercell_degenerate_lattice() {
    // Create a degenerate lattice with one zero-length axis
    use nalgebra::Matrix3;
    let degenerate_matrix = Matrix3::new(5.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0);
    let lattice = Lattice::new(degenerate_matrix);
    let species = vec![Species::neutral(Element::Fe)];
    let coords = vec![Vector3::new(0.0, 0.0, 0.0)];
    let structure = Structure::new(lattice, species, coords);

    let config = DefectSupercellConfig {
        min_distance: 10.0,
        max_atoms: 100,
        cubic_preference: 0.0,
    };

    let result = find_defect_supercell(&structure, &config);
    assert!(result.is_err(), "Should fail for degenerate lattice");
}

#[test]
fn test_antisite_same_site_error() {
    let structure = make_nacl();
    let result = create_antisite_pair(&structure, 0, 0);
    assert!(result.is_err());
}

#[test]
fn test_find_voronoi_interstitials_empty_structure() {
    let lattice = Lattice::cubic(5.0);
    let structure = Structure::new(lattice, vec![], vec![]);
    let sites = find_voronoi_interstitials(&structure, None, 0.01);
    assert!(sites.is_empty());
}

#[test]
fn test_find_voronoi_interstitials_fcc() {
    let structure = make_fcc_cu();
    let sites = find_voronoi_interstitials(&structure, Some(0.5), 0.1);

    // FCC should have octahedral (at 0.5, 0.5, 0.5) and tetrahedral sites
    assert!(!sites.is_empty(), "FCC should have interstitial sites");

    // All sites should have positive min_distance
    for site in &sites {
        assert!(site.min_distance > 0.0);
        assert!(site.coordination > 0);
    }

    // Sites should be sorted by min_distance (descending)
    for idx in 1..sites.len() {
        assert!(
            sites[idx - 1].min_distance >= sites[idx].min_distance,
            "Sites should be sorted by min_distance descending"
        );
    }
}

#[test]
fn test_find_voronoi_interstitials_bcc() {
    // BCC structure (Fe)
    let lattice = Lattice::cubic(2.87);
    let species = vec![Species::neutral(Element::Fe), Species::neutral(Element::Fe)];
    let coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.5), // body center
    ];
    let structure = Structure::new(lattice, species, coords);

    let sites = find_voronoi_interstitials(&structure, Some(0.5), 0.1);

    // BCC should have octahedral sites at face centers and edge centers
    assert!(!sites.is_empty(), "BCC should have interstitial sites");

    for site in &sites {
        assert!(site.min_distance > 0.0);
        // All fractional coords should be in [0, 1)
        assert!(site.frac_coords.x >= 0.0 && site.frac_coords.x < 1.0);
        assert!(site.frac_coords.y >= 0.0 && site.frac_coords.y < 1.0);
        assert!(site.frac_coords.z >= 0.0 && site.frac_coords.z < 1.0);
    }
}

#[test]
fn test_voronoi_interstitial_site_type_classification() {
    let structure = make_fcc_cu();
    let sites = find_voronoi_interstitials(&structure, Some(0.3), 0.1);

    // Check that sites have valid classifications
    for site in &sites {
        match site.coordination {
            3 => assert_eq!(site.site_type, InterstitialSiteType::Trigonal),
            4 => assert_eq!(site.site_type, InterstitialSiteType::Tetrahedral),
            5 => assert_eq!(site.site_type, InterstitialSiteType::SquarePyramidal),
            6 => assert_eq!(site.site_type, InterstitialSiteType::Octahedral),
            8 => assert_eq!(site.site_type, InterstitialSiteType::Cubic),
            12 => assert_eq!(site.site_type, InterstitialSiteType::Cuboctahedral),
            _ => assert_eq!(site.site_type, InterstitialSiteType::Other),
        }
    }
}

// === Defect Naming Tests ===

#[test]
fn test_defect_name_vacancy() {
    let defect = PointDefect::vacancy(0, Vector3::zeros(), Species::neutral(Element::O));
    assert_eq!(defect.name(None, None), "v_O");
    assert_eq!(defect.name(Some("4a"), None), "v_O_4a");
    assert_eq!(defect.name(Some("8c"), None), "v_O_8c");
}

#[test]
fn test_defect_name_substitution() {
    let defect = PointDefect::substitution(
        0,
        Vector3::zeros(),
        Species::neutral(Element::Fe),
        Species::neutral(Element::Ni),
    );
    assert_eq!(defect.name(None, None), "Fe_on_Ni");
}

#[test]
fn test_defect_name_interstitial() {
    let defect = PointDefect::interstitial(
        Vector3::new(0.25, 0.25, 0.25),
        Species::neutral(Element::Li),
    );
    assert_eq!(defect.name(None, None), "Li_i");
    assert_eq!(defect.name(None, Some("oct")), "Li_i_oct");
    assert_eq!(defect.name(None, Some("tet")), "Li_i_tet");
}

#[test]
fn test_defect_name_antisite() {
    // Antisite: Fe on Ni site
    let defect = PointDefect {
        defect_type: DefectType::Antisite,
        site_idx: Some(0),
        position: Vector3::zeros(),
        species: Some(Species::neutral(Element::Fe)),
        original_species: Some(Species::neutral(Element::Ni)),
        charge: 0,
    };
    assert_eq!(defect.name(None, None), "Fe_Ni");
}

#[test]
fn test_generate_defect_name_function() {
    let defect = PointDefect::vacancy(0, Vector3::zeros(), Species::neutral(Element::Na));
    assert_eq!(generate_defect_name(&defect, None, None), "v_Na");
    assert_eq!(generate_defect_name(&defect, Some("2a"), None), "v_Na_2a");
}

// === DefectsGenerator Tests ===

#[test]
fn test_defects_generator_config_default() {
    let config = DefectsGeneratorConfig::default();
    assert!(config.include_vacancies);
    assert!(config.include_substitutions);
    assert!(config.include_interstitials);
    assert!(config.include_antisites);
    assert_eq!(config.supercell_min_dist, 10.0);
    assert_eq!(config.supercell_max_atoms, 200);
    assert_eq!(config.symprec, 0.01);
    assert_eq!(config.max_charge, 4);
}

#[test]
fn test_generate_all_defects_nacl() {
    let structure = make_nacl();
    let config = DefectsGeneratorConfig::default();

    let result = generate_all_defects(&structure, &config).unwrap();

    // Should have vacancies for Na and Cl
    assert_eq!(result.vacancies.len(), 2);

    // Should have antisites since there are 2 elements
    assert_eq!(result.antisites.len(), 2); // Na on Cl, Cl on Na

    // No extrinsic dopants, so no substitutions
    assert!(result.substitutions.is_empty());

    // Should have interstitials for both Na and Cl
    assert!(!result.interstitials.is_empty());

    // Total defects should be sum of all types
    assert_eq!(
        result.n_defects,
        result.vacancies.len()
            + result.substitutions.len()
            + result.interstitials.len()
            + result.antisites.len()
    );

    // Check vacancy naming
    let vacancy_names: Vec<&str> = result.vacancies.iter().map(|d| d.name.as_str()).collect();
    assert!(vacancy_names.iter().any(|n| n.starts_with("v_Na")));
    assert!(vacancy_names.iter().any(|n| n.starts_with("v_Cl")));
}

#[test]
fn test_generate_all_defects_with_extrinsic() {
    let structure = make_nacl();
    let config = DefectsGeneratorConfig {
        extrinsic: vec!["K".to_string(), "Br".to_string()],
        ..Default::default()
    };

    let result = generate_all_defects(&structure, &config).unwrap();

    // Should have substitutions: K_on_Na, K_on_Cl, Br_on_Na, Br_on_Cl
    assert_eq!(result.substitutions.len(), 4);

    // Check substitution naming
    let sub_names: Vec<&str> = result
        .substitutions
        .iter()
        .map(|d| d.name.as_str())
        .collect();
    assert!(sub_names.contains(&"K_on_Na"));
    assert!(sub_names.contains(&"K_on_Cl"));
    assert!(sub_names.contains(&"Br_on_Na"));
    assert!(sub_names.contains(&"Br_on_Cl"));
}

#[test]
fn test_generate_all_defects_vacancies_only() {
    let structure = make_nacl();
    let config = DefectsGeneratorConfig {
        include_vacancies: true,
        include_substitutions: false,
        include_interstitials: false,
        include_antisites: false,
        ..Default::default()
    };

    let result = generate_all_defects(&structure, &config).unwrap();

    assert_eq!(result.vacancies.len(), 2);
    assert!(result.substitutions.is_empty());
    assert!(result.interstitials.is_empty());
    assert!(result.antisites.is_empty());
}

#[test]
fn test_generate_all_defects_single_element() {
    let structure = make_fcc_cu();
    let config = DefectsGeneratorConfig::default();

    let result = generate_all_defects(&structure, &config).unwrap();

    // Should have 1 vacancy type (all Cu sites are equivalent)
    assert_eq!(result.vacancies.len(), 1);
    assert_eq!(result.vacancies[0].original_species, Some("Cu".to_string()));

    // No antisites for single element
    assert!(result.antisites.is_empty());

    // Should have interstitials for Cu
    assert!(!result.interstitials.is_empty());
}

#[test]
fn test_defect_entry_charge_states() {
    let structure = make_nacl();
    let config = DefectsGeneratorConfig {
        max_charge: 4,
        ..Default::default()
    };

    let result = generate_all_defects(&structure, &config).unwrap();

    // Check that vacancies have charge states
    for vacancy in &result.vacancies {
        assert!(!vacancy.charge_states.is_empty());
        // Cl vacancy should have +1 as likely charge (Cl is -1)
        if vacancy.original_species == Some("Cl".to_string()) {
            assert!(vacancy.charge_states.iter().any(|cs| cs.charge == 1));
        }
        // Na vacancy should have -1 as likely charge (Na is +1)
        if vacancy.original_species == Some("Na".to_string()) {
            assert!(vacancy.charge_states.iter().any(|cs| cs.charge == -1));
        }
    }
}

#[test]
fn test_defect_entry_has_coordinates() {
    let structure = make_nacl();
    let config = DefectsGeneratorConfig::default();

    let result = generate_all_defects(&structure, &config).unwrap();

    // All defects should have fractional coordinates (with tolerance for floating-point)
    let eps = 1e-10;
    for vacancy in &result.vacancies {
        assert!(vacancy.frac_coords.x >= -eps && vacancy.frac_coords.x <= 1.0 + eps);
        assert!(vacancy.frac_coords.y >= -eps && vacancy.frac_coords.y <= 1.0 + eps);
        assert!(vacancy.frac_coords.z >= -eps && vacancy.frac_coords.z <= 1.0 + eps);
    }

    for interstitial in &result.interstitials {
        assert!(interstitial.frac_coords.x >= -eps && interstitial.frac_coords.x <= 1.0 + eps);
        assert!(interstitial.frac_coords.y >= -eps && interstitial.frac_coords.y <= 1.0 + eps);
        assert!(interstitial.frac_coords.z >= -eps && interstitial.frac_coords.z <= 1.0 + eps);
    }
}

#[test]
fn test_defect_entry_supercell_matrix() {
    let structure = make_nacl();
    let config = DefectsGeneratorConfig {
        supercell_min_dist: 10.0,
        supercell_max_atoms: 200,
        ..Default::default()
    };

    let result = generate_all_defects(&structure, &config).unwrap();

    // Supercell matrix should satisfy min distance
    let det = result.supercell_matrix[0][0]
        * result.supercell_matrix[1][1]
        * result.supercell_matrix[2][2];
    assert!(det >= 8, "Supercell should be at least 2x2x2 for NaCl");
}
