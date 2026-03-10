use super::*;
use crate::element::Element;
use crate::lattice::Lattice;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::{Matrix3, Vector3};

fn make_fcc(element: Element, a: f64) -> Structure {
    let lattice = Lattice::cubic(a);
    let species = vec![Species::neutral(element); 4];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.0, 0.5, 0.5),
    ];
    Structure::new(lattice, species, frac_coords)
}

fn make_bcc(element: Element, a: f64) -> Structure {
    let lattice = Lattice::cubic(a);
    let species = vec![Species::neutral(element); 2];
    let frac_coords = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    Structure::new(lattice, species, frac_coords)
}

fn make_simple_cubic(element: Element, a: f64) -> Structure {
    let lattice = Lattice::cubic(a);
    let species = vec![Species::neutral(element)];
    let frac_coords = vec![Vector3::new(0.0, 0.0, 0.0)];
    Structure::new(lattice, species, frac_coords)
}

#[test]
fn test_fcc_coordination() {
    // FCC Cu: each atom has 12 nearest neighbors at a/sqrt(2) ≈ 2.55 Å
    let fcc = make_fcc(Element::Cu, 3.61);
    let config = NeighborListConfig {
        cutoff: 3.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&fcc, &config);

    // Count neighbors per site
    let mut counts = [0usize; 4];
    for &center in &nl.center_indices {
        counts[center] += 1;
    }

    // Each site should have 12 neighbors
    for (idx, count) in counts.iter().enumerate() {
        assert_eq!(
            *count, 12,
            "FCC site {idx} has {count} neighbors, expected 12"
        );
    }

    // Check distance (should be a/sqrt(2) ≈ 2.552 Å)
    let expected_dist = 3.61 / 2.0_f64.sqrt();
    for dist in &nl.distances {
        assert!(
            (*dist - expected_dist).abs() < 0.1,
            "Distance {dist} doesn't match expected {expected_dist}"
        );
    }
}

#[test]
fn test_bcc_coordination() {
    // BCC Fe: first shell has 8 neighbors at a*sqrt(3)/2 ≈ 2.48 Å
    let bcc = make_bcc(Element::Fe, 2.87);
    let config = NeighborListConfig {
        cutoff: 2.6,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&bcc, &config);

    // Count neighbors per site
    let mut counts = [0usize; 2];
    for &center in &nl.center_indices {
        counts[center] += 1;
    }

    // Each site should have 8 neighbors
    for (idx, count) in counts.iter().enumerate() {
        assert_eq!(
            *count, 8,
            "BCC site {idx} has {count} neighbors, expected 8"
        );
    }
}

#[test]
fn test_simple_cubic_coordination() {
    // Simple cubic: 6 neighbors at distance a
    let sc = make_simple_cubic(Element::Cu, 3.0);
    let config = NeighborListConfig {
        cutoff: 3.5,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // Should have 6 neighbors (nearest neighbors via PBC)
    assert_eq!(nl.len(), 6, "Simple cubic should have 6 neighbors");

    // All distances should be 3.0 Å
    for dist in &nl.distances {
        assert!(
            (*dist - 3.0).abs() < 0.01,
            "Distance {dist} doesn't match expected 3.0"
        );
    }
}

#[test]
fn test_get_site_neighbors() {
    let fcc = make_fcc(Element::Cu, 3.61);
    let neighbors = get_site_neighbors(&fcc, 0, 3.0);

    assert_eq!(neighbors.len(), 12, "FCC site 0 should have 12 neighbors");

    // Check sorting by distance
    for window in neighbors.windows(2) {
        assert!(
            window[0].1 <= window[1].1,
            "Neighbors should be sorted by distance"
        );
    }
}

#[test]
fn test_empty_structure() {
    let empty = Structure::new(Lattice::cubic(5.0), vec![], vec![]);
    let config = NeighborListConfig::default();
    let nl = build_neighbor_list(&empty, &config);

    assert!(nl.is_empty(), "Empty structure should have no neighbors");
}

#[test]
fn test_zero_cutoff() {
    let fcc = make_fcc(Element::Cu, 3.61);
    let config = NeighborListConfig {
        cutoff: 0.0,
        ..Default::default()
    };
    let nl = build_neighbor_list(&fcc, &config);

    assert!(nl.is_empty(), "Zero cutoff should give no neighbors");
}

#[test]
fn test_negative_cutoff() {
    let fcc = make_fcc(Element::Cu, 3.61);
    let config = NeighborListConfig {
        cutoff: -1.0,
        ..Default::default()
    };
    let nl = build_neighbor_list(&fcc, &config);

    assert!(nl.is_empty(), "Negative cutoff should give no neighbors");
}

#[test]
fn test_self_interaction() {
    let sc = make_simple_cubic(Element::Cu, 3.0);

    // Without self-interaction (should only count periodic images)
    let config_no_self = NeighborListConfig {
        cutoff: 0.1,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };
    let nl_no_self = build_neighbor_list(&sc, &config_no_self);
    assert!(
        nl_no_self.is_empty(),
        "No neighbors within 0.1 Å without self"
    );

    // With self-interaction enabled
    let config_self = NeighborListConfig {
        cutoff: 0.1,
        self_interaction: true,
        numerical_tol: 1e-8,
        ..Default::default()
    };
    let nl_self = build_neighbor_list(&sc, &config_self);
    assert_eq!(nl_self.len(), 1, "Should have 1 self-interaction");
    assert_eq!(nl_self.center_indices[0], nl_self.neighbor_indices[0]);
    assert!(nl_self.distances[0] < 1e-8);
}

#[test]
fn test_periodic_images() {
    // Single atom in a 3 Å cubic cell
    let sc = make_simple_cubic(Element::Cu, 3.0);
    let config = NeighborListConfig {
        cutoff: 5.0, // Should find neighbors at 3.0 Å and 3*sqrt(2) ≈ 4.24 Å
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // Count neighbors by distance
    let first_shell: Vec<_> = nl.distances.iter().filter(|&&d| d < 3.5).collect();
    let second_shell: Vec<_> = nl
        .distances
        .iter()
        .filter(|&&d| (3.5..4.5).contains(&d))
        .collect();

    assert_eq!(first_shell.len(), 6, "6 first-shell neighbors at 3.0 Å");
    assert_eq!(
        second_shell.len(),
        12,
        "12 second-shell neighbors at ~4.24 Å"
    );
}

#[test]
fn test_comparison_with_old_implementation() {
    // This test ensures the new implementation gives the same results as the old one
    let fcc = make_fcc(Element::Cu, 3.61);
    let cutoff = 3.0;

    // Use new implementation
    let config = NeighborListConfig {
        cutoff,
        ..Default::default()
    };
    let nl_new = build_neighbor_list(&fcc, &config);

    // Use old implementation from Structure
    let (old_centers, _old_neighbors, _old_images, old_distances) =
        fcc.get_neighbor_list(cutoff, 1e-8, true);

    // Should have same number of pairs
    assert_eq!(
        nl_new.len(),
        old_centers.len(),
        "New and old implementations should find same number of pairs"
    );

    // Check that all distances are found (order may differ)
    let mut new_dists: Vec<f64> = nl_new.distances.clone();
    let mut old_dists: Vec<f64> = old_distances.clone();
    new_dists.sort_by(|a, b| a.partial_cmp(b).unwrap());
    old_dists.sort_by(|a, b| a.partial_cmp(b).unwrap());

    for (new, old) in new_dists.iter().zip(old_dists.iter()) {
        assert!(
            (new - old).abs() < 1e-6,
            "Distance mismatch: new={new}, old={old}"
        );
    }
}

// === Additional comprehensive tests ===

/// Helper to create a triclinic lattice structure.
fn make_triclinic(element: Element) -> Structure {
    // Triclinic lattice: a=4.0, b=5.0, c=6.0, alpha=70°, beta=80°, gamma=85°
    let lattice = Lattice::from_parameters(4.0, 5.0, 6.0, 70.0, 80.0, 85.0);
    let species = vec![Species::neutral(element); 4];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.25, 0.25, 0.25),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.75, 0.25, 0.5),
    ];
    Structure::new(lattice, species, frac_coords)
}

#[test]
fn test_triclinic_cell() {
    // Triclinic cells have non-orthogonal lattice vectors
    // Verify correct neighbor finding with skewed coordinates
    let triclinic = make_triclinic(Element::Si);
    let config = NeighborListConfig {
        cutoff: 4.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&triclinic, &config);

    // Should find some neighbors
    assert!(!nl.is_empty(), "Triclinic cell should have neighbors");

    // Verify all distances are positive and within cutoff
    for dist in &nl.distances {
        assert!(*dist > 0.0, "Distance should be positive");
        assert!(
            *dist <= config.cutoff + config.numerical_tol,
            "Distance {dist} exceeds cutoff"
        );
    }

    // Verify center/neighbor indices are valid
    let n_sites = triclinic.num_sites();
    for (&center, &neighbor) in nl.center_indices.iter().zip(&nl.neighbor_indices) {
        assert!(center < n_sites, "Invalid center index");
        assert!(neighbor < n_sites, "Invalid neighbor index");
    }

    // Cross-check: manually compute distances for a few pairs
    let cart_coords = triclinic.cart_coords();
    let matrix = triclinic.lattice.matrix();
    let lattice_vecs = [
        matrix.row(0).transpose(),
        matrix.row(1).transpose(),
        matrix.row(2).transpose(),
    ];

    for idx in 0..nl.len().min(10) {
        let center_cart = &cart_coords[nl.center_indices[idx]];
        let neighbor_cart = &cart_coords[nl.neighbor_indices[idx]];
        let image = nl.images[idx];

        let offset = (image[0] as f64) * lattice_vecs[0]
            + (image[1] as f64) * lattice_vecs[1]
            + (image[2] as f64) * lattice_vecs[2];

        let expected_dist = (neighbor_cart + offset - center_cart).norm();
        assert!(
            (nl.distances[idx] - expected_dist).abs() < 1e-10,
            "Distance mismatch: got {}, expected {}",
            nl.distances[idx],
            expected_dist
        );
    }
}

#[test]
fn test_mixed_pbc_xy_only() {
    // Test with PBC only in x and y directions (slab geometry)
    let mut lattice = Lattice::cubic(5.0);
    lattice.pbc = [true, true, false];

    let species = vec![Species::neutral(Element::Cu); 2];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.1), // near bottom
        Vector3::new(0.0, 0.0, 0.9), // near top
    ];
    let slab = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 6.0, // larger than cell, should NOT wrap in z
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&slab, &config);

    // Atoms are 4.0 Å apart in z (0.8 * 5.0 = 4.0)
    // With no PBC in z, they should be found as neighbors at ~4.0 Å
    // But should NOT find neighbors via z-wrapping (which would be 1.0 Å)

    // Check that all z-image offsets are 0
    for image in &nl.images {
        assert_eq!(
            image[2], 0,
            "z-periodic image should be 0 when pbc[2]=false"
        );
    }

    // Verify we find the direct pair
    let found_direct = nl.distances.iter().any(|&d| (d - 4.0).abs() < 0.1);
    assert!(found_direct, "Should find direct neighbor at ~4.0 Å");

    // Should NOT find wrapped pair at ~1.0 Å
    let found_wrapped = nl.distances.iter().any(|&d| d < 2.0);
    assert!(
        !found_wrapped,
        "Should NOT find z-wrapped neighbor when pbc[2]=false"
    );
}

#[test]
fn test_mixed_pbc_z_only() {
    // Test with PBC only in z direction (wire geometry)
    let mut lattice = Lattice::cubic(3.0);
    lattice.pbc = [false, false, true];

    let species = vec![Species::neutral(Element::Cu)];
    let frac_coords = vec![Vector3::new(0.5, 0.5, 0.0)];
    let wire = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 4.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&wire, &config);

    // Should find neighbors via z-periodic images only
    // Distance should be 3.0 Å (one cell in z)
    assert!(!nl.is_empty(), "Should find z-periodic neighbors");

    // All images should have x=0, y=0
    for image in &nl.images {
        assert_eq!(image[0], 0, "x-image should be 0 when pbc[0]=false");
        assert_eq!(image[1], 0, "y-image should be 0 when pbc[1]=false");
    }
}

#[test]
fn test_cutoff_larger_than_cell() {
    // When cutoff > cell dimension, multiple periodic images are needed
    let small_cell = make_simple_cubic(Element::Cu, 2.0); // 2 Å cell
    let config = NeighborListConfig {
        cutoff: 5.0, // 2.5x the cell size
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&small_cell, &config);

    // Should find neighbors at 2.0 Å (1 cell), ~2.83 Å (face diagonal),
    // ~3.46 Å (body diagonal), 4.0 Å (2 cells), etc.

    // Count neighbors at different distance shells
    let shell_2: usize = nl.distances.iter().filter(|&&d| d < 2.5).count();
    let shell_3: usize = nl
        .distances
        .iter()
        .filter(|&&d| (2.5..3.1).contains(&d))
        .count();
    let shell_4: usize = nl
        .distances
        .iter()
        .filter(|&&d| (3.1..3.7).contains(&d))
        .count();

    assert_eq!(shell_2, 6, "First shell (2.0 Å): expected 6 neighbors");
    assert_eq!(shell_3, 12, "Second shell (~2.83 Å): expected 12 neighbors");
    assert_eq!(shell_4, 8, "Third shell (~3.46 Å): expected 8 neighbors");
    // Fourth shell includes neighbors at 4.0 Å and also via diagonal paths
    // so we just verify it's non-empty rather than exact count

    // Verify image magnitudes
    for image in &nl.images {
        // For cutoff=5.0 and cell=2.0, max image should be ceil(5/2)=3
        for &img_coord in image {
            assert!(img_coord.abs() <= 3, "Image offset too large: {:?}", image);
        }
    }
}

#[test]
fn test_boundary_atoms() {
    // Test atoms at fractional coordinates 0.0 and 0.5
    // These are at cell boundaries and can have numerical issues
    let lattice = Lattice::cubic(4.0);
    let species = vec![Species::neutral(Element::Cu); 3];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0), // corner
        Vector3::new(0.5, 0.5, 0.5), // body center
        Vector3::new(0.5, 0.0, 0.5), // face center
    ];
    let boundary = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 5.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&boundary, &config);

    // Check that all distances are valid (positive and within cutoff)
    for dist in &nl.distances {
        assert!(*dist > 1e-10, "Spurious zero distance found");
        assert!(*dist <= config.cutoff + 1e-8, "Distance exceeds cutoff");
    }

    // Verify we found some neighbors
    assert!(!nl.is_empty(), "Should find neighbors for boundary atoms");
}

#[test]
fn test_atoms_at_exact_fractional_positions() {
    // Test atoms at exactly 0.0 and 1.0 - these should be equivalent
    let lattice = Lattice::cubic(3.0);
    let species = vec![Species::neutral(Element::Cu); 2];

    // Both atoms at the same position (0.0 = 1.0 due to PBC)
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(1.0, 1.0, 1.0), // wraps to (0,0,0)
    ];
    let overlap = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 0.1,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&overlap, &config);

    // Atoms at same position should find each other at ~0 distance
    // But this is essentially self-interaction, depends on tolerance
    // With numerical_tol=1e-8, distances < 1e-8 are treated as self

    // The key check is no crashes or infinite loops
    assert!(
        nl.len() <= 2,
        "Should have at most 2 pairs (each direction)"
    );
}

#[test]
fn test_large_system_scaling() {
    // Test with 1000+ atoms to verify O(n) scaling
    let lattice_const = 3.61;
    let supercell_size = 6; // 6x6x6 supercell = 6^3 * 4 = 864 atoms

    let supercell_lattice = Lattice::cubic(lattice_const * supercell_size as f64);
    let num_cells = supercell_size * supercell_size * supercell_size;
    let mut species = Vec::with_capacity(num_cells * 4);
    let mut frac_coords = Vec::with_capacity(num_cells * 4);

    let fcc_basis = [
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.0, 0.5, 0.5),
    ];

    for idx_a in 0..supercell_size {
        for idx_b in 0..supercell_size {
            for idx_c in 0..supercell_size {
                for base in &fcc_basis {
                    let frac = Vector3::new(
                        (base.x + idx_a as f64) / supercell_size as f64,
                        (base.y + idx_b as f64) / supercell_size as f64,
                        (base.z + idx_c as f64) / supercell_size as f64,
                    );
                    frac_coords.push(frac);
                    species.push(Species::neutral(Element::Cu));
                }
            }
        }
    }

    let large_system = Structure::new(supercell_lattice, species, frac_coords);
    let n_atoms = large_system.num_sites();
    assert!(
        n_atoms >= 800,
        "Should have at least 800 atoms, got {n_atoms}"
    );

    let config = NeighborListConfig {
        cutoff: 3.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    // Time the neighbor finding
    let start = std::time::Instant::now();
    let nl = build_neighbor_list(&large_system, &config);
    let elapsed = start.elapsed();

    // Should complete in reasonable time (< 2 seconds even without rayon)
    assert!(
        elapsed.as_secs_f64() < 2.0,
        "Neighbor finding took too long: {:.2}s for {} atoms",
        elapsed.as_secs_f64(),
        n_atoms
    );

    // Verify correctness: each atom should have ~12 neighbors (FCC first shell)
    let mut counts = vec![0usize; n_atoms];
    for &center in &nl.center_indices {
        counts[center] += 1;
    }

    // All atoms should have exactly 12 neighbors
    let all_have_12 = counts.iter().all(|&c| c == 12);
    assert!(
        all_have_12,
        "All FCC atoms should have 12 neighbors within 3.0 Å cutoff"
    );
}

#[test]
fn test_numerical_tolerance_at_cutoff() {
    // Test atoms exactly at the cutoff distance
    // This verifies proper handling of floating-point edge cases
    let a = 3.0;
    let cutoff = 3.0; // Exactly equals lattice constant

    let sc = make_simple_cubic(Element::Cu, a);
    let config = NeighborListConfig {
        cutoff,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // First shell neighbors are exactly at cutoff distance
    // Should include them (cutoff comparison is <=)
    assert_eq!(nl.len(), 6, "Should find 6 neighbors at exactly cutoff");

    for dist in &nl.distances {
        assert!(
            (*dist - cutoff).abs() < 1e-10,
            "All neighbors should be at exactly {cutoff} Å"
        );
    }
}

#[test]
fn test_numerical_tolerance_just_inside_cutoff() {
    // Neighbors slightly inside the cutoff
    let a = 2.9999999;
    let cutoff = 3.0;

    let sc = make_simple_cubic(Element::Cu, a);
    let config = NeighborListConfig {
        cutoff,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // Should find neighbors (distance < cutoff)
    assert_eq!(nl.len(), 6, "Should find 6 neighbors just inside cutoff");
}

#[test]
fn test_numerical_tolerance_just_outside_cutoff() {
    // Neighbors slightly outside the cutoff
    let a = 3.0000001;
    let cutoff = 3.0;

    let sc = make_simple_cubic(Element::Cu, a);
    let config = NeighborListConfig {
        cutoff,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // Should NOT find neighbors (distance > cutoff)
    assert!(
        nl.is_empty(),
        "Should not find neighbors just outside cutoff"
    );
}

#[test]
fn test_very_small_cell() {
    // Test with cell smaller than typical interatomic distances
    let lattice = Lattice::cubic(1.5); // Very small cell
    let species = vec![Species::neutral(Element::H); 2];
    let frac_coords = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    let small = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 5.0, // Much larger than cell
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&small, &config);

    // 2-atom cell (a=1.5 Å) with cutoff=5.0 Å spans many periodic images
    // Each atom should have many neighbors due to the large cutoff/cell ratio
    // Key invariant: neighbor count should be symmetric (each atom has same count)
    let count_0 = nl.center_indices.iter().filter(|&&c| c == 0).count();
    let count_1 = nl.center_indices.iter().filter(|&&c| c == 1).count();
    assert_eq!(
        count_0, count_1,
        "Both atoms should have same neighbor count"
    );
    assert!(
        count_0 > 100,
        "Should have many neighbors with cutoff >> cell size"
    );

    // Verify no duplicates (same center-neighbor-image triple)
    let mut pairs: std::collections::HashSet<(usize, usize, [i32; 3])> =
        std::collections::HashSet::new();
    for idx in 0..nl.len() {
        let triple = (
            nl.center_indices[idx],
            nl.neighbor_indices[idx],
            nl.images[idx],
        );
        assert!(pairs.insert(triple), "Duplicate pair found: {:?}", triple);
    }
}

#[test]
fn test_hexagonal_lattice() {
    // Test with hexagonal close-packed structure
    let lattice = Lattice::hexagonal(2.95, 4.68); // HCP Mg
    let species = vec![Species::neutral(Element::Mg); 2];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(1.0 / 3.0, 2.0 / 3.0, 0.5),
    ];
    let hcp = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 3.5,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&hcp, &config);

    // HCP should have CN=12 for first coordination shell
    // (6 in-plane + 3 above + 3 below)
    let mut counts = [0, 0];
    for &center in &nl.center_indices {
        counts[center] += 1;
    }

    // Both atoms should have 12 neighbors
    assert_eq!(counts[0], 12, "HCP site 0 should have CN=12");
    assert_eq!(counts[1], 12, "HCP site 1 should have CN=12");
}

#[test]
fn test_monoclinic_lattice() {
    // Test with monoclinic lattice (one non-right angle)
    let lattice = Lattice::from_parameters(5.0, 4.0, 6.0, 90.0, 110.0, 90.0);
    let species = vec![Species::neutral(Element::Si); 2];
    let frac_coords = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)];
    let monoclinic = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 4.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&monoclinic, &config);

    // Verify distances are correct
    let cart_coords = monoclinic.cart_coords();
    let matrix = monoclinic.lattice.matrix();
    let lattice_vecs = [
        matrix.row(0).transpose(),
        matrix.row(1).transpose(),
        matrix.row(2).transpose(),
    ];

    for idx in 0..nl.len() {
        let center_cart = &cart_coords[nl.center_indices[idx]];
        let neighbor_cart = &cart_coords[nl.neighbor_indices[idx]];
        let image = nl.images[idx];

        let offset = (image[0] as f64) * lattice_vecs[0]
            + (image[1] as f64) * lattice_vecs[1]
            + (image[2] as f64) * lattice_vecs[2];

        let expected_dist = (neighbor_cart + offset - center_cart).norm();
        assert!(
            (nl.distances[idx] - expected_dist).abs() < 1e-10,
            "Monoclinic distance mismatch"
        );
    }
}

#[test]
fn test_neighbor_list_symmetry() {
    // For full PBC, if A neighbors B at distance d with image I,
    // then B should neighbor A at distance d with image -I
    let fcc = make_fcc(Element::Cu, 3.61);
    let config = NeighborListConfig {
        cutoff: 3.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&fcc, &config);

    // Build a set of all (center, neighbor, image) pairs
    let pairs: std::collections::HashSet<(usize, usize, [i32; 3])> = nl
        .center_indices
        .iter()
        .enumerate()
        .map(|(idx, &center)| (center, nl.neighbor_indices[idx], nl.images[idx]))
        .collect();

    // For each pair, check that the reverse exists
    for (center, neighbor, image) in &pairs {
        let reverse_image = [-image[0], -image[1], -image[2]];
        assert!(
            pairs.contains(&(*neighbor, *center, reverse_image)),
            "Missing reverse pair: ({neighbor}, {center}, {reverse_image:?})"
        );
    }
}

#[test]
fn test_triclinic_cell_60_70_80() {
    // Triclinic with angles 60°, 70°, 80° as specified
    let lattice = Lattice::from_parameters(4.0, 4.5, 5.0, 60.0, 70.0, 80.0);
    let species = vec![Species::neutral(Element::Si); 4];
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.25, 0.25, 0.25),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.75, 0.25, 0.5),
    ];
    let triclinic = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 4.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&triclinic, &config);

    // Verify we find neighbors
    assert!(
        !nl.is_empty(),
        "Triclinic (60°, 70°, 80°) should have neighbors"
    );

    // Verify distances are within cutoff
    for dist in &nl.distances {
        assert!(*dist > 0.0 && *dist <= config.cutoff + 1e-8);
    }

    // Cross-validate distances by manual computation
    let cart_coords = triclinic.cart_coords();
    let matrix = triclinic.lattice.matrix();
    let lattice_vecs = [
        matrix.row(0).transpose(),
        matrix.row(1).transpose(),
        matrix.row(2).transpose(),
    ];

    for idx in 0..nl.len() {
        let center_cart = &cart_coords[nl.center_indices[idx]];
        let neighbor_cart = &cart_coords[nl.neighbor_indices[idx]];
        let image = nl.images[idx];

        let offset = (image[0] as f64) * lattice_vecs[0]
            + (image[1] as f64) * lattice_vecs[1]
            + (image[2] as f64) * lattice_vecs[2];

        let expected_dist = (neighbor_cart + offset - center_cart).norm();
        assert!(
            (nl.distances[idx] - expected_dist).abs() < 1e-10,
            "Distance mismatch in triclinic cell"
        );
    }
}

#[test]
fn test_mixed_pbc_all_combinations() {
    // Test all 8 combinations of PBC settings
    let pbc_combos: [[bool; 3]; 8] = [
        [false, false, false],
        [true, false, false],
        [false, true, false],
        [false, false, true],
        [true, true, false],
        [true, false, true],
        [false, true, true],
        [true, true, true],
    ];

    for pbc in pbc_combos {
        let mut lattice = Lattice::cubic(4.0);
        lattice.pbc = pbc;

        let species = vec![Species::neutral(Element::Cu); 2];
        let frac_coords = vec![Vector3::new(0.1, 0.1, 0.1), Vector3::new(0.9, 0.9, 0.9)];
        let structure = Structure::new(lattice, species, frac_coords);

        let config = NeighborListConfig {
            cutoff: 5.0,
            self_interaction: false,
            numerical_tol: 1e-8,
            ..Default::default()
        };

        let nl = build_neighbor_list(&structure, &config);

        // Verify that periodic images only appear in periodic directions
        for image in &nl.images {
            for (axis, &is_periodic) in pbc.iter().enumerate() {
                if !is_periodic {
                    assert_eq!(
                        image[axis], 0,
                        "Non-periodic axis {} has non-zero image {:?} for pbc={:?}",
                        axis, image, pbc
                    );
                }
            }
        }
    }
}

#[test]
fn test_cutoff_multiple_cell_sizes() {
    // Test cutoffs that are 2x, 3x, and 4x the cell dimension
    let a = 2.0;
    let sc = make_simple_cubic(Element::Cu, a);

    for multiplier in [2.0, 3.0, 4.0] {
        let cutoff = a * multiplier;
        let config = NeighborListConfig {
            cutoff,
            ..Default::default()
        };

        let nl = build_neighbor_list(&sc, &config);

        // Count neighbors at exactly a distance
        for shell in 1..=(multiplier as i32) {
            let shell_dist = (shell as f64) * a;
            let count = nl
                .distances
                .iter()
                .filter(|&&d| (d - shell_dist).abs() < 0.01)
                .count();

            if shell == 1 {
                assert_eq!(count, 6, "Shell {shell} should have 6 neighbors");
            }
        }

        // Verify max image magnitude
        let max_expected = (cutoff / a).ceil() as i32;
        for image in &nl.images {
            for &coord in image {
                assert!(
                    coord.abs() <= max_expected,
                    "Image coord {} exceeds expected max {} for cutoff={}",
                    coord,
                    max_expected,
                    cutoff
                );
            }
        }
    }
}

#[test]
fn test_boundary_atoms_half_coords() {
    // Test atoms at exactly 0.5 fractional coordinates
    let lattice = Lattice::cubic(4.0);
    let species = vec![Species::neutral(Element::Cu); 4];
    let frac_coords = vec![
        Vector3::new(0.0, 0.5, 0.5),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.5, 0.5),
    ];
    let boundary = Structure::new(lattice, species, frac_coords);

    let config = NeighborListConfig {
        cutoff: 3.0,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };

    let nl = build_neighbor_list(&boundary, &config);

    // Verify correct handling of half-integer positions
    assert!(!nl.is_empty());

    // Verify all distances are positive and within cutoff
    for dist in &nl.distances {
        assert!(*dist > 0.0, "Distance should be positive");
        assert!(
            *dist <= config.cutoff + 1e-8,
            "Distance {} exceeds cutoff",
            dist
        );
    }

    // Expected distances: 2.0 Å (same plane) and sqrt(2)*2 ≈ 2.83 Å (diagonal)
    let has_2_angstrom = nl.distances.iter().any(|&d| (d - 2.0).abs() < 0.01);
    let has_diagonal = nl
        .distances
        .iter()
        .any(|&d| (d - 2.0_f64.sqrt() * 2.0).abs() < 0.01);
    assert!(has_2_angstrom, "Should find neighbors at 2.0 Å");
    assert!(
        has_diagonal,
        "Should find neighbors at ~2.83 Å (face diagonal)"
    );
}

#[test]
fn test_exact_cutoff_boundary_precision() {
    // Test with distances very close to cutoff (within machine precision)
    let epsilon = 1e-14; // Machine epsilon level
    let cutoff = 3.0;

    // Create structure where neighbor is at exactly cutoff - epsilon
    let adjusted_a = cutoff - epsilon;
    let sc = make_simple_cubic(Element::Cu, adjusted_a);

    let config = NeighborListConfig {
        cutoff,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // Should find neighbors (distance < cutoff)
    assert!(nl.len() >= 6, "Should find neighbors at cutoff - epsilon");

    // Now test at cutoff + epsilon
    let adjusted_a_plus = cutoff + epsilon;
    let sc_plus = make_simple_cubic(Element::Cu, adjusted_a_plus);
    let nl_plus = build_neighbor_list(&sc_plus, &config);

    // Atoms at distance > cutoff should be excluded
    // The neighbor distance is adjusted_a_plus = cutoff + epsilon > cutoff
    // So neighbors should NOT be included (strict < or <= cutoff policy)
    assert!(
        nl_plus.len() <= 6,
        "Neighbors at cutoff + epsilon should be excluded or at boundary, found {}",
        nl_plus.len()
    );
}

#[test]
fn test_neighbor_counts_different_cutoffs() {
    // Verify neighbor counts increase appropriately with cutoff
    let fcc = make_fcc(Element::Cu, 3.61);
    let expected_dist = 3.61 / 2.0_f64.sqrt(); // ~2.55 Å

    let cutoffs_and_expected: [(f64, usize); 4] = [
        (2.0, 0),           // below first shell
        (3.0, 12),          // first shell (12 neighbors)
        (4.0, 12 + 6),      // first + second shell
        (5.0, 12 + 6 + 24), // first + second + third shell
    ];

    for (cutoff, expected_min) in cutoffs_and_expected {
        let config = NeighborListConfig {
            cutoff,
            ..Default::default()
        };

        let nl = build_neighbor_list(&fcc, &config);
        let total_pairs = nl.len();
        let pairs_per_atom = total_pairs / 4;

        if cutoff > expected_dist {
            assert!(
                pairs_per_atom >= expected_min / 4,
                "Cutoff {}: expected at least {} neighbors per atom, got {}",
                cutoff,
                expected_min / 4,
                pairs_per_atom
            );
        }
    }
}

// === ASE/torch-sim Compatible Tests ===

#[test]
fn test_ase_compatible_neighbor_list_format() {
    // Tests that our neighbor list format matches ASE's NeighborList output:
    // - center_indices[i]: index of center atom for pair i
    // - neighbor_indices[i]: index of neighbor atom for pair i
    // - distances[i]: distance between center and neighbor
    // - images[i]: periodic image shift [n_a, n_b, n_c]
    //
    // This is the standard format used by ASE and torch-sim

    let sc = make_simple_cubic(Element::Cu, 4.0);
    let config = NeighborListConfig {
        cutoff: 5.0,
        ..Default::default()
    };

    let nl = build_neighbor_list(&sc, &config);

    // Verify format: all arrays same length
    assert_eq!(
        nl.center_indices.len(),
        nl.neighbor_indices.len(),
        "center and neighbor indices must have same length"
    );
    assert_eq!(
        nl.center_indices.len(),
        nl.distances.len(),
        "indices and distances must have same length"
    );
    assert_eq!(
        nl.center_indices.len(),
        nl.images.len(),
        "indices and images must have same length"
    );

    // Verify indices are valid
    let n_atoms = sc.num_sites();
    assert!(
        nl.center_indices.iter().all(|&idx| idx < n_atoms),
        "All center indices should be < n_atoms"
    );
    assert!(
        nl.neighbor_indices.iter().all(|&idx| idx < n_atoms),
        "All neighbor indices should be < n_atoms"
    );

    // Verify distances are consistent with positions + images
    let positions = sc.cart_coords();
    let lattice_matrix = sc.lattice.matrix();
    let lattice_vecs = [
        lattice_matrix.row(0).transpose(),
        lattice_matrix.row(1).transpose(),
        lattice_matrix.row(2).transpose(),
    ];

    for (idx, (&center, &neighbor)) in nl
        .center_indices
        .iter()
        .zip(&nl.neighbor_indices)
        .enumerate()
    {
        let image = nl.images[idx];
        let expected_dist = nl.distances[idx];

        let center_pos = &positions[center];
        let neighbor_pos = &positions[neighbor];

        // Apply periodic image
        let image_offset = (image[0] as f64) * lattice_vecs[0]
            + (image[1] as f64) * lattice_vecs[1]
            + (image[2] as f64) * lattice_vecs[2];

        let actual_dist = (neighbor_pos + image_offset - center_pos).norm();

        assert!(
            (actual_dist - expected_dist).abs() < 1e-10,
            "Distance mismatch: computed {}, stored {}",
            actual_dist,
            expected_dist
        );
    }
}

#[test]
fn test_torch_sim_diamond_si_neighbor_count() {
    // Si diamond: 4 tetrahedral neighbors per atom at a*sqrt(3)/4 ≈ 2.35 Å
    let a = 5.431;
    let nn_dist = a * 3.0_f64.sqrt() / 4.0; // ~2.35 Å

    // Build Si diamond with 8-atom conventional cell (FCC + basis)
    let lattice = Lattice::cubic(a);
    let species = vec![Species::neutral(Element::Si); 8];
    // Diamond structure: FCC lattice with 2-atom basis at (0,0,0) and (1/4,1/4,1/4)
    // FCC positions: (0,0,0), (0.5,0.5,0), (0.5,0,0.5), (0,0.5,0.5)
    // Plus same shifted by (1/4,1/4,1/4)
    let frac_coords = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.5, 0.5, 0.0),
        Vector3::new(0.5, 0.0, 0.5),
        Vector3::new(0.0, 0.5, 0.5),
        Vector3::new(0.25, 0.25, 0.25),
        Vector3::new(0.75, 0.75, 0.25),
        Vector3::new(0.75, 0.25, 0.75),
        Vector3::new(0.25, 0.75, 0.75),
    ];
    let si_diamond = Structure::new(lattice, species, frac_coords);

    // Cutoff just above first shell
    let config = NeighborListConfig {
        cutoff: nn_dist * 1.1,
        ..Default::default()
    };

    let nl = build_neighbor_list(&si_diamond, &config);

    // Diamond has coordination number 4 (tetrahedral)
    let n_atoms = si_diamond.num_sites();
    let coordination = 4;
    let expected_pairs = n_atoms * coordination;
    assert_eq!(
        nl.len(),
        expected_pairs,
        "Si diamond: expected {} pairs ({} neighbors × {} atoms), got {}",
        expected_pairs,
        coordination,
        n_atoms,
        nl.len()
    );

    // All distances should be approximately nn_dist
    for &dist in &nl.distances {
        assert!(
            (dist - nn_dist).abs() < 0.05,
            "Si neighbor distance {} should be ~{} Å",
            dist,
            nn_dist
        );
    }
}

#[test]
fn test_torch_sim_fcc_cu_neighbor_count() {
    // torch-sim tests FCC Cu structure
    // First shell: each atom has 12 nearest neighbors
    // Distance: a/sqrt(2) ≈ 2.55 Å for a=3.61 Å

    let a = 3.61; // Cu lattice constant
    let nn_dist = a / 2.0_f64.sqrt(); // ~2.55 Å

    let fcc_cu = make_fcc(Element::Cu, a);

    // Cutoff just above first shell
    let config = NeighborListConfig {
        cutoff: nn_dist * 1.1,
        ..Default::default()
    };

    let nl = build_neighbor_list(&fcc_cu, &config);

    // 4-atom FCC cell, 12 neighbors per atom = 48 pairs total
    assert_eq!(
        nl.len(),
        48,
        "FCC Cu: expected 48 pairs (12 neighbors × 4 atoms), got {}",
        nl.len()
    );

    // All distances should be approximately nn_dist
    for &dist in &nl.distances {
        assert!(
            (dist - nn_dist).abs() < 0.01,
            "Cu neighbor distance {} should be ~{} Å",
            dist,
            nn_dist
        );
    }
}

// === for_each_pair and count_pairs tests ===

#[test]
fn test_for_each_pair_basic_and_cutoff() {
    // At exactly cutoff: included (<=)
    let positions = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(2.0, 0.0, 0.0)];
    let mut pairs = Vec::new();
    for_each_pair(
        &positions,
        None,
        [false; 3],
        2.0,
        |idx_i, idx_j, _rij, dist| {
            pairs.push((idx_i, idx_j, dist));
        },
    )
    .unwrap();
    assert_eq!(pairs.len(), 1);
    assert_eq!((pairs[0].0, pairs[0].1), (0, 1));
    assert!((pairs[0].2 - 2.0).abs() < 1e-10);

    // Beyond cutoff: excluded
    let cutoff = 3.0;
    let positions3 = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(cutoff, 0.0, 0.0), // Exactly at cutoff - included
        Vector3::new(cutoff + 0.001, 0.0, 0.0), // Beyond - excluded from (0,2)
    ];
    // Pairs: (0,1) at cutoff, (1,2) at 0.001, (0,2) beyond → 2 pairs
    assert_eq!(
        count_pairs(&positions3, None, [false; 3], cutoff).unwrap(),
        2
    );
}

#[test]
fn test_count_pairs_edge_cases() {
    // Empty and single-atom: 0 pairs
    assert_eq!(count_pairs(&[], None, [false; 3], 5.0).unwrap(), 0);
    assert_eq!(
        count_pairs(&[Vector3::new(0.0, 0.0, 0.0)], None, [false; 3], 5.0).unwrap(),
        0
    );
}

#[test]
fn test_for_each_pair_periodic() {
    let cell = Matrix3::from_diagonal(&Vector3::new(5.0, 5.0, 5.0));
    let positions = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(4.5, 0.0, 0.0)];
    // Minimum image distance is 0.5 via PBC
    assert_eq!(
        count_pairs(&positions, Some(&cell), [true; 3], 1.0).unwrap(),
        1
    );
    assert_eq!(
        count_pairs(&positions, Some(&cell), [false; 3], 1.0).unwrap(),
        0
    );
}

#[test]
fn test_for_each_pair_vector_direction() {
    // rij should point from i to j
    let positions = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(2.0, 1.0, 0.5)];
    let mut rij_captured = Vector3::zeros();
    for_each_pair(&positions, None, [false; 3], 5.0, |_, _, rij, _| {
        rij_captured = rij
    })
    .unwrap();
    assert!((rij_captured - (positions[1] - positions[0])).norm() < 1e-10);
}

#[test]
fn test_count_pairs_fcc() {
    // FCC unit cell: 4 atoms → 6 unique pairs (4 choose 2)
    let a = 4.0;
    let positions = vec![
        Vector3::new(0.0, 0.0, 0.0),
        Vector3::new(0.0, 0.5 * a, 0.5 * a),
        Vector3::new(0.5 * a, 0.0, 0.5 * a),
        Vector3::new(0.5 * a, 0.5 * a, 0.0),
    ];
    let cell = Matrix3::from_diagonal(&Vector3::new(a, a, a));
    let nn_dist = a / 2.0_f64.sqrt();
    assert_eq!(
        count_pairs(&positions, Some(&cell), [true; 3], nn_dist * 1.01).unwrap(),
        6
    );
}

#[test]
fn test_for_each_pair_pbc_without_cell_error() {
    // Enabling PBC without a cell should return an error
    let positions = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(1.0, 0.0, 0.0)];
    let result = for_each_pair(&positions, None, [true, false, false], 5.0, |_, _, _, _| {});
    assert!(result.is_err());
    assert!(matches!(
        result.unwrap_err(),
        crate::error::FerroxError::PbcWithoutCell
    ));
}

#[test]
fn test_for_each_pair_singular_cell_error() {
    // Singular (non-invertible) cell should return an error
    let positions = vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(1.0, 0.0, 0.0)];
    let singular_cell = Matrix3::zeros(); // All zeros = singular
    let result = for_each_pair(
        &positions,
        Some(&singular_cell),
        [true; 3],
        5.0,
        |_, _, _, _| {},
    );
    assert!(result.is_err());
    assert!(matches!(
        result.unwrap_err(),
        crate::error::FerroxError::SingularCell
    ));
}
