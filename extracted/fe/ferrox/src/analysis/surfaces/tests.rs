use super::*;
use crate::element::Element;
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use approx::assert_abs_diff_eq;
use nalgebra::Vector3;

const TOL: f64 = 1e-6;

// === Helper Functions ===

/// Build a simple slab-like structure: atoms stacked along z with vacuum gap.
fn make_slab_like(lattice_param: f64, n_layers: usize, vacuum: f64) -> Structure {
    let c_total = (n_layers as f64) * lattice_param + vacuum;
    let lattice = Lattice::orthorhombic(lattice_param, lattice_param, c_total);
    let frac_coords: Vec<_> = (0..n_layers)
        .map(|idx| Vector3::new(0.0, 0.0, (idx as f64 * lattice_param) / c_total))
        .collect();
    Structure::new(
        lattice,
        vec![Species::neutral(Element::Cu); n_layers],
        frac_coords,
    )
}

/// Build an FCC conventional cell for slab generation tests.
fn make_fcc(lattice_param: f64, element: Element) -> Structure {
    let lattice = Lattice::cubic(lattice_param);
    let species = vec![Species::neutral(element); 4];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.0, 0.5, 0.5),
    ];
    Structure::new(lattice, species, frac_coords)
}

// === MillerIndex Tests ===

#[test]
/// GCD reduction: common factor, zero, negative, and already-coprime cases.
fn test_miller_index_reduced() {
    let cases: &[([i32; 3], [i32; 3])] = &[
        ([2, 4, 6], [1, 2, 3]),
        ([0, 0, 0], [0, 0, 0]),
        ([-2, -4, -2], [-1, -2, -1]),
        ([3, 5, 7], [3, 5, 7]),
        // GCD(h,k)=2 but GCD(h,k,l)=1 — requires all three indices in GCD
        ([2, 4, 3], [2, 4, 3]),
    ];
    for &(input, expected) in cases {
        let reduced = MillerIndex::from(input).reduced();
        assert_eq!(
            reduced,
            MillerIndex::from(expected),
            "reduced({input:?}) = {reduced:?}"
        );
    }
}

#[test]
/// Verify is_zero, norm_l1, Display, and array round-trip conversions.
fn test_miller_index_properties_and_conversions() {
    let miller = MillerIndex::new(1, -2, 3);

    assert!(!miller.is_zero());
    assert!(MillerIndex::new(0, 0, 0).is_zero());

    assert_eq!(miller.norm_l1(), 6); // |1| + |-2| + |3|

    assert_eq!(format!("{miller}"), "(1, -2, 3)");

    // Round-trip through array
    let arr: [i32; 3] = miller.into();
    assert_eq!(arr, [1, -2, 3]);
    let back: MillerIndex = arr.into();
    assert_eq!(back, miller);
}

// === Enumeration Tests ===

#[test]
/// Enumeration with max_index=1 should produce exactly 13 unique planes after
/// sign normalization and GCD reduction, excluding (0,0,0).
fn test_enumerate_miller_max_1() {
    let indices = enumerate_miller_indices(1);
    assert_eq!(indices.len(), 13);
    assert!(!indices.contains(&MillerIndex::new(0, 0, 0)));
    for expected in [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]] {
        assert!(
            indices.contains(&MillerIndex::from(expected)),
            "missing {expected:?}"
        );
    }
}

#[test]
/// Results should be sorted by L1 norm (ascending).
fn test_enumerate_miller_sorted_by_l1_norm() {
    let indices = enumerate_miller_indices(3);
    for window in indices.windows(2) {
        assert!(
            window[0].norm_l1() <= window[1].norm_l1(),
            "Expected {:?} (L1={}) <= {:?} (L1={})",
            window[0],
            window[0].norm_l1(),
            window[1],
            window[1].norm_l1(),
        );
    }
}

#[test]
/// Higher max_index produces strictly more planes.
fn test_enumerate_miller_monotonic_count() {
    let count_1 = enumerate_miller_indices(1).len();
    let count_2 = enumerate_miller_indices(2).len();
    let count_3 = enumerate_miller_indices(3).len();
    assert!(
        count_1 < count_2,
        "max=1 ({count_1}) should be < max=2 ({count_2})"
    );
    assert!(
        count_2 < count_3,
        "max=2 ({count_2}) should be < max=3 ({count_3})"
    );
}

// === D-Spacing Tests ===

#[test]
fn test_d_spacing_cubic() {
    let lattice = Lattice::cubic(4.0);
    let d_100 = d_spacing(&lattice, [1, 0, 0]).unwrap();
    // For cubic: d_hkl = a / sqrt(h² + k² + l²)
    assert_abs_diff_eq!(d_100, 4.0, epsilon = 0.01); // d_100 = 4.0 / sqrt(1)

    let d_110 = d_spacing(&lattice, [1, 1, 0]).unwrap();
    assert_abs_diff_eq!(d_110, 4.0 / 2.0_f64.sqrt(), epsilon = 0.01); // d_110 ≈ 2.83

    let d_111 = d_spacing(&lattice, [1, 1, 1]).unwrap();
    assert_abs_diff_eq!(d_111, 4.0 / 3.0_f64.sqrt(), epsilon = 0.01); // d_111 ≈ 2.31
}

#[test]
fn test_d_spacing_zero_error() {
    let lattice = Lattice::cubic(4.0);
    let result = d_spacing(&lattice, [0, 0, 0]);
    assert!(result.is_err());
}

#[test]
/// For tetragonal lattice (a=a, c≠a): d_001 = c, d_100 = a.
fn test_d_spacing_tetragonal() {
    let lattice = Lattice::tetragonal(3.0, 5.0);
    let d_001 = d_spacing(&lattice, [0, 0, 1]).unwrap();
    assert_abs_diff_eq!(d_001, 5.0, epsilon = 0.01);

    let d_100 = d_spacing(&lattice, [1, 0, 0]).unwrap();
    assert_abs_diff_eq!(d_100, 3.0, epsilon = 0.01);

    // Tetragonal a=b, so d_010 = d_100
    let d_010 = d_spacing(&lattice, [0, 1, 0]).unwrap();
    assert_abs_diff_eq!(d_010, d_100, epsilon = TOL);
}

#[test]
/// For orthorhombic lattice: d_hkl = 1/sqrt((h/a)² + (k/b)² + (l/c)²).
fn test_d_spacing_orthorhombic() {
    let (param_a, param_b, param_c) = (3.0, 4.0, 5.0);
    let lattice = Lattice::orthorhombic(param_a, param_b, param_c);

    let d_100 = d_spacing(&lattice, [1, 0, 0]).unwrap();
    assert_abs_diff_eq!(d_100, param_a, epsilon = 0.01);

    let d_010 = d_spacing(&lattice, [0, 1, 0]).unwrap();
    assert_abs_diff_eq!(d_010, param_b, epsilon = 0.01);

    let d_001 = d_spacing(&lattice, [0, 0, 1]).unwrap();
    assert_abs_diff_eq!(d_001, param_c, epsilon = 0.01);

    // d_111 = 1/sqrt(1/9 + 1/16 + 1/25)
    let expected = 1.0 / (1.0 / 9.0 + 1.0 / 16.0 + 1.0 / 25.0_f64).sqrt();
    let d_111 = d_spacing(&lattice, [1, 1, 1]).unwrap();
    assert_abs_diff_eq!(d_111, expected, epsilon = 0.01);
}

#[test]
/// d-spacing should scale linearly with lattice parameter.
fn test_d_spacing_scales_with_lattice_param() {
    let lattice_small = Lattice::cubic(2.0);
    let lattice_large = Lattice::cubic(6.0);

    let d_small = d_spacing(&lattice_small, [1, 1, 0]).unwrap();
    let d_large = d_spacing(&lattice_large, [1, 1, 0]).unwrap();
    assert_abs_diff_eq!(d_large / d_small, 3.0, epsilon = TOL);
}

// === Miller-to-Normal Tests ===

#[test]
/// For cubic, normals align with Miller direction: (100)→x, (001)→z, (110)→[1,1,0]/√2.
fn test_miller_to_normal_cubic() {
    let lattice = Lattice::cubic(4.0);

    let normal_100 = miller_to_normal(&lattice, [1, 0, 0]);
    assert_abs_diff_eq!(normal_100.norm(), 1.0, epsilon = TOL);
    assert!(normal_100.x.abs() > 0.99);

    let normal_001 = miller_to_normal(&lattice, [0, 0, 1]);
    assert_abs_diff_eq!(normal_001.norm(), 1.0, epsilon = TOL);
    assert!(normal_001.z.abs() > 0.99);

    let normal_110 = miller_to_normal(&lattice, [1, 1, 0]);
    assert_abs_diff_eq!(normal_110.norm(), 1.0, epsilon = TOL);
    let expected_110 = Vector3::new(1.0, 1.0, 0.0).normalize();
    assert!((normal_110 - expected_110).norm() < 0.01);
}

#[test]
/// For tetragonal, (001) and (100) normals should still be along z and x.
fn test_miller_to_normal_tetragonal() {
    let lattice = Lattice::tetragonal(3.0, 5.0);

    let normal_001 = miller_to_normal(&lattice, [0, 0, 1]);
    assert_abs_diff_eq!(normal_001.norm(), 1.0, epsilon = TOL);
    assert!(normal_001.z.abs() > 0.99, "(001) normal should be along z");

    let normal_100 = miller_to_normal(&lattice, [1, 0, 0]);
    assert_abs_diff_eq!(normal_100.norm(), 1.0, epsilon = TOL);
    assert!(normal_100.x.abs() > 0.99, "(100) normal should be along x");
}

#[test]
/// Normal vectors for (hkl) and (-h,-k,-l) should be antiparallel.
fn test_miller_to_normal_antiparallel() {
    let lattice = Lattice::cubic(4.0);
    let normal_pos = miller_to_normal(&lattice, [1, 2, 3]);
    let normal_neg = miller_to_normal(&lattice, [-1, -2, -3]);
    let dot = normal_pos.dot(&normal_neg);
    assert_abs_diff_eq!(dot, -1.0, epsilon = TOL);
}

// === Surface Energy Tests ===

#[test]
/// γ = (E_slab - n*E_bulk) / (2A): normal case, zero-area (NaN), and zero-difference.
fn test_surface_energy_calculation() {
    // E_surf = (-100 - 8*(-10)) / (2*10) = -1.0
    assert_abs_diff_eq!(
        calculate_surface_energy(-100.0, -10.0, 8, 10.0),
        -1.0,
        epsilon = 0.001
    );
    // Zero area → NaN
    assert!(calculate_surface_energy(-100.0, -10.0, 8, 0.0).is_nan());
    // Slab equals bulk → zero
    assert_abs_diff_eq!(
        calculate_surface_energy(-80.0, -10.0, 8, 25.0),
        0.0,
        epsilon = TOL
    );
}

#[test]
/// SurfaceEnergy::new should correctly convert eV/Å² to J/m².
fn test_surface_energy_unit_conversion() {
    let se = SurfaceEnergy::new(MillerIndex::new(1, 0, 0), 1.0, 50.0);
    // 1 eV/Å² = 16.02176634 J/m²
    assert_abs_diff_eq!(se.energy_j_per_m2, 16.02176634, epsilon = 1e-5);
    assert_eq!(se.surface_area, 50.0);
    assert_eq!(se.miller_index, MillerIndex::new(1, 0, 0));
}

// === Surface Area Tests ===

#[test]
/// Surface area of an orthorhombic slab should equal a*b.
fn test_surface_area_orthorhombic() {
    let param_a = 3.0;
    let slab = make_slab_like(param_a, 3, 10.0);
    // The helper uses orthorhombic(a, a, c_total), so area = a*a
    let area = surface_area(&slab);
    assert_abs_diff_eq!(area, param_a * param_a, epsilon = TOL);
}

// === Surface Atoms Tests ===

#[test]
/// Tight tolerance finds only the topmost atom; wider tolerance captures more; empty → empty.
fn test_get_surface_atoms() {
    let slab = make_slab_like(2.0, 5, 10.0);

    // Tight tolerance: only the topmost atom (idx=4, frac z ≈ 0.4)
    let surface = get_surface_atoms(&slab, 0.05);
    assert_eq!(surface, [4]);

    // Wider tolerance captures more layers
    assert!(get_surface_atoms(&slab, 0.5).len() > surface.len());

    // Empty structure → no surface atoms
    let empty = Structure::new(Lattice::cubic(4.0), vec![], vec![]);
    assert!(get_surface_atoms(&empty, 0.1).is_empty());
}

// === Adsorption Site Type Tests ===

#[test]
/// parse → as_str round-trip, Display, case-insensitivity, aliases, and invalid input.
fn test_adsorption_site_type_parsing() {
    let variants = [
        AdsorptionSiteType::Atop,
        AdsorptionSiteType::Bridge,
        AdsorptionSiteType::Hollow3,
        AdsorptionSiteType::Hollow4,
        AdsorptionSiteType::Other,
    ];
    for variant in &variants {
        let name = variant.as_str();
        assert_eq!(
            AdsorptionSiteType::parse(name),
            Some(*variant),
            "round-trip failed for {name}"
        );
        assert_eq!(format!("{variant}"), name, "Display mismatch for {name}");
    }
    // Case-insensitive, aliases, and invalid input
    for (input, expected) in [
        ("ATOP", Some(AdsorptionSiteType::Atop)),
        ("Bridge", Some(AdsorptionSiteType::Bridge)),
        ("fcc", Some(AdsorptionSiteType::Hollow3)),
        ("HCP", Some(AdsorptionSiteType::Hollow3)),
        ("invalid", None),
    ] {
        assert_eq!(
            AdsorptionSiteType::parse(input),
            expected,
            "parse({input:?})"
        );
    }
}

// === Wulff Construction Tests ===

#[test]
/// Sphericity in (0,1] for valid shapes, 0 when volume or area is zero.
fn test_wulff_shape_sphericity() {
    let shape = WulffShape::new(vec![], vec![], 100.0, 50.0);
    assert!(shape.sphericity > 0.0 && shape.sphericity <= 1.0);

    assert_eq!(WulffShape::new(vec![], vec![], 100.0, 0.0).sphericity, 0.0);
    assert_eq!(WulffShape::new(vec![], vec![], 0.0, 50.0).sphericity, 0.0);
}

#[test]
/// Wulff shape with equal surface energies on all cubic facets should have
/// equal area fractions for symmetry-equivalent facets.
fn test_wulff_shape_cubic_equal_energies() {
    let lattice = Lattice::cubic(4.0);
    let energies = vec![
        (MillerIndex::new(1, 0, 0), 1.0),
        (MillerIndex::new(0, 1, 0), 1.0),
        (MillerIndex::new(0, 0, 1), 1.0),
    ];
    let shape = compute_wulff_shape(&lattice, &energies).unwrap();

    // 3 input facets × 2 (positive + negative) = 6 facets
    assert_eq!(shape.facets.len(), 6);

    // All facets should be equidistant and have equal area fraction (cube symmetry)
    let first_dist = shape.facets[0].distance_from_center;
    for facet in &shape.facets {
        assert_abs_diff_eq!(facet.distance_from_center, first_dist, epsilon = TOL);
        assert_abs_diff_eq!(facet.area_fraction, 1.0 / 6.0, epsilon = TOL);
    }
}

#[test]
/// Lower-energy facets should be closer to center (smaller distance_from_center).
fn test_wulff_shape_lower_energy_closer() {
    let lattice = Lattice::cubic(4.0);
    let energies = vec![
        (MillerIndex::new(1, 0, 0), 1.0),
        (MillerIndex::new(1, 1, 1), 3.0),
    ];
    let shape = compute_wulff_shape(&lattice, &energies).unwrap();

    let max_dist_100 = shape
        .facets
        .iter()
        .filter(|f| f.surface_energy == 1.0)
        .map(|f| f.distance_from_center)
        .fold(f64::NEG_INFINITY, f64::max);
    let min_dist_111 = shape
        .facets
        .iter()
        .filter(|f| f.surface_energy == 3.0)
        .map(|f| f.distance_from_center)
        .fold(f64::INFINITY, f64::min);

    assert!(
        max_dist_100 < min_dist_111,
        "all (100) facets should be closer than any (111)"
    );
}

#[test]
/// Empty input and non-positive energies should both be rejected.
fn test_wulff_shape_invalid_input_errors() {
    let lattice = Lattice::cubic(4.0);
    assert!(compute_wulff_shape(&lattice, &[]).is_err());
    let bad_energies = [
        (MillerIndex::new(1, 0, 0), -1.0),
        (MillerIndex::new(0, 1, 0), 0.0),
    ];
    assert!(compute_wulff_shape(&lattice, &bad_energies).is_err());
}

// === SlabConfigExt Tests ===

#[test]
/// Builder methods should set fields correctly.
fn test_slab_config_ext_builder() {
    let config = SlabConfigExt::new(MillerIndex::new(1, 1, 0))
        .with_min_slab_size(15.0)
        .with_min_vacuum(12.0)
        .with_center_slab(false)
        .with_in_unit_planes(true)
        .with_primitive(true);

    assert_eq!(config.miller_index, MillerIndex::new(1, 1, 0));
    assert_eq!(config.min_slab_size, 15.0);
    assert_eq!(config.min_vacuum, 12.0);
    assert!(!config.center_slab);
    assert!(config.in_unit_planes);
    assert!(config.primitive);
}

#[test]
/// to_slab_config should correctly propagate all fields.
fn test_slab_config_ext_to_slab_config() {
    let ext = SlabConfigExt::new(MillerIndex::new(1, 1, 1))
        .with_min_slab_size(20.0)
        .with_min_vacuum(15.0)
        .with_center_slab(false);

    let basic = ext.to_slab_config(0.01);
    assert_eq!(basic.miller_index, [1, 1, 1]);
    assert_eq!(basic.min_slab_size, 20.0);
    assert_eq!(basic.min_vacuum_size, 15.0);
    assert!(!basic.center_slab);
    assert_eq!(basic.symprec, 0.01);
}

// === Slab Generation Integration Tests ===

const CU_LATTICE_PARAM: f64 = 3.615;

fn make_cu_100_slab_config(min_vacuum: f64) -> crate::structure::SlabConfig {
    crate::structure::SlabConfig {
        miller_index: [1, 0, 0],
        min_slab_size: 8.0,
        min_vacuum_size: min_vacuum,
        center_slab: true,
        in_unit_planes: false,
        primitive: false,
        symprec: 0.1,
        termination_index: Some(0),
    }
}

#[test]
/// FCC Cu (100) slab should have expected surface area ≈ a².
fn test_fcc_100_slab_surface_area() {
    let cu_fcc = make_fcc(CU_LATTICE_PARAM, Element::Cu);
    let slabs = cu_fcc
        .generate_slabs(&make_cu_100_slab_config(10.0))
        .unwrap();
    assert!(!slabs.is_empty(), "should generate at least one slab");

    let area = surface_area(&slabs[0]);
    assert!(
        area > 1.0,
        "surface area should be positive and non-trivial, got {area}"
    );
    assert!(
        area < CU_LATTICE_PARAM * CU_LATTICE_PARAM * 4.0,
        "surface area should be bounded, got {area}"
    );
}

#[test]
/// Adsorption site finding on a generated FCC slab should find atop sites.
fn test_find_adsorption_sites_atop_on_fcc_slab() {
    let cu_fcc = make_fcc(CU_LATTICE_PARAM, Element::Cu);
    let slabs = cu_fcc
        .generate_slabs(&make_cu_100_slab_config(12.0))
        .unwrap();
    assert!(!slabs.is_empty());
    let slab = &slabs[0];

    let sites =
        find_adsorption_sites(slab, 2.0, Some(&[AdsorptionSiteType::Atop]), None, None).unwrap();

    // Every atop site should have exactly 1 coordinating atom
    for site in &sites {
        assert_eq!(site.site_type, AdsorptionSiteType::Atop);
        assert_eq!(site.coordinating_atoms.len(), 1);
        assert_abs_diff_eq!(site.height, 2.0, epsilon = TOL);
    }

    // Should find at least one atop site (one per surface atom)
    let n_surface = get_surface_atoms(slab, DEFAULT_SURFACE_TOLERANCE).len();
    assert_eq!(
        sites.len(),
        n_surface,
        "should find one atop site per surface atom"
    );
}

#[test]
/// Negative height should return an error.
fn test_find_adsorption_sites_negative_height_error() {
    let slab = make_slab_like(3.0, 3, 10.0);
    let result = find_adsorption_sites(&slab, -1.0, None, None, None);
    assert!(result.is_err());
}
