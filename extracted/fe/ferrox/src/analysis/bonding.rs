//! Bond detection and bonding analysis for crystal structures.
//!
//! This module provides methods to detect chemical bonds between atoms in
//! crystal structures using covalent radii or fixed distance cutoffs.
//!
//! # Bonding Strategies
//!
//! - **CovalentRadius**: Two atoms are bonded if their distance is less than
//!   `scale * (r1 + r2)` where r1, r2 are covalent radii. This is the standard
//!   approach used by pymatgen and ASE (typical scale: 1.1).
//! - **MaxDistance**: Simple fixed cutoff — atoms within the given distance are bonded.
//!
//! # Examples
//!
//! ```rust,ignore
//! use ferrox::structure::Structure;
//! use ferrox::analysis::bonding::{find_bonds, BondingStrategy};
//!
//! let structure = Structure::from_json(json_str)?;
//!
//! // Default: covalent radius with scale=1.1
//! let bonds = find_bonds(&structure, &BondingStrategy::default());
//!
//! // Custom scale factor
//! let bonds = find_bonds(&structure, &BondingStrategy::CovalentRadius { scale: 1.2 });
//!
//! // Fixed cutoff
//! let bonds = find_bonds(&structure, &BondingStrategy::MaxDistance { cutoff: 3.0 });
//! ```

use crate::neighbors::{NeighborList, NeighborListConfig, build_neighbor_list};
use crate::structure::Structure;

/// A chemical bond between two sites in a structure.
#[derive(Debug, Clone, PartialEq)]
pub struct Bond {
    /// Index of the first site.
    pub site_idx_1: usize,
    /// Index of the second site.
    pub site_idx_2: usize,
    /// Distance between the two sites in Angstroms.
    pub distance: f64,
    /// Periodic image offset [da, db, dc] in lattice vector units.
    pub image: [i32; 3],
}

/// Strategy for determining which atom pairs are bonded.
#[derive(Debug, Clone, PartialEq)]
pub enum BondingStrategy {
    /// Covalent radius method: atoms are bonded if distance < scale * (r1 + r2).
    /// The default scale of 1.1 provides a 10% tolerance above the sum of
    /// covalent radii, matching the pymatgen/ASE convention.
    CovalentRadius {
        /// Multiplicative scale factor applied to the sum of covalent radii.
        scale: f64,
    },
    /// Fixed maximum distance cutoff: all pairs within this distance are bonded.
    MaxDistance {
        /// Maximum bond distance in Angstroms.
        cutoff: f64,
    },
}

impl Default for BondingStrategy {
    /// Default strategy: covalent radius with scale = 1.1.
    fn default() -> Self {
        Self::CovalentRadius { scale: 1.1 }
    }
}

/// Find all bonds in a structure using the given bonding strategy.
///
/// Returns a list of bonds sorted by (site_idx_1, site_idx_2, distance).
/// Each bond appears once per direction (A->B and B->A are separate entries),
/// matching the neighbor list convention.
pub fn find_bonds(structure: &Structure, strategy: &BondingStrategy) -> Vec<Bond> {
    let Some(nl) = build_bond_neighbor_list(structure, strategy) else {
        return vec![];
    };

    let mut bonds = Vec::with_capacity(nl.len());
    for idx in 0..nl.len() {
        let center = nl.center_indices[idx];
        let neighbor = nl.neighbor_indices[idx];
        let dist = nl.distances[idx];

        if is_bonded(structure, center, neighbor, dist, strategy) {
            bonds.push(Bond {
                site_idx_1: center,
                site_idx_2: neighbor,
                distance: dist,
                image: nl.images[idx],
            });
        }
    }

    bonds.sort_by(|a, b| {
        a.site_idx_1
            .cmp(&b.site_idx_1)
            .then(a.site_idx_2.cmp(&b.site_idx_2))
            .then(a.distance.total_cmp(&b.distance))
    });

    bonds
}

/// Get all bonds for a specific site in the structure.
///
/// Returns bonds sorted by distance (nearest first).
///
/// # Panics
///
/// Panics if `site_idx` is out of bounds.
pub fn get_bonded_neighbors(
    structure: &Structure,
    site_idx: usize,
    strategy: &BondingStrategy,
) -> Vec<Bond> {
    assert!(
        site_idx < structure.num_sites(),
        "site_idx {site_idx} out of bounds (num_sites={})",
        structure.num_sites()
    );

    let Some(nl) = build_bond_neighbor_list(structure, strategy) else {
        return vec![];
    };

    let mut site_bonds = Vec::new();
    for idx in 0..nl.len() {
        if nl.center_indices[idx] != site_idx {
            continue;
        }
        let neighbor = nl.neighbor_indices[idx];
        let dist = nl.distances[idx];
        if is_bonded(structure, site_idx, neighbor, dist, strategy) {
            site_bonds.push(Bond {
                site_idx_1: site_idx,
                site_idx_2: neighbor,
                distance: dist,
                image: nl.images[idx],
            });
        }
    }

    site_bonds.sort_by(|a, b| a.distance.total_cmp(&b.distance));
    site_bonds
}

/// Build a neighbor list with the appropriate cutoff for a bonding strategy.
/// Returns `None` for structures with fewer than 2 sites or zero cutoff.
fn build_bond_neighbor_list(
    structure: &Structure,
    strategy: &BondingStrategy,
) -> Option<NeighborList> {
    if structure.num_sites() < 2 {
        return None;
    }
    let cutoff = match strategy {
        BondingStrategy::CovalentRadius { scale } => {
            let max_radius = structure
                .site_occupancies
                .iter()
                .filter_map(|occ| occ.dominant_species().element.covalent_radius())
                .fold(0.0_f64, f64::max);
            scale * 2.0 * max_radius
        }
        BondingStrategy::MaxDistance { cutoff } => *cutoff,
    };
    if cutoff <= 0.0 {
        return None;
    }
    let config = NeighborListConfig {
        cutoff,
        self_interaction: false,
        numerical_tol: 1e-8,
        ..Default::default()
    };
    Some(build_neighbor_list(structure, &config))
}

/// Check whether two sites are bonded under the given strategy.
fn is_bonded(
    structure: &Structure,
    center: usize,
    neighbor: usize,
    distance: f64,
    strategy: &BondingStrategy,
) -> bool {
    match strategy {
        BondingStrategy::CovalentRadius { scale } => {
            let elem_1 = structure.site_occupancies[center]
                .dominant_species()
                .element;
            let elem_2 = structure.site_occupancies[neighbor]
                .dominant_species()
                .element;

            let (r_1, r_2) = match (elem_1.covalent_radius(), elem_2.covalent_radius()) {
                (Some(r1), Some(r2)) => (r1, r2),
                _ => return false,
            };

            distance <= scale * (r_1 + r_2)
        }
        BondingStrategy::MaxDistance { cutoff } => distance <= *cutoff,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::element::Element;
    use crate::lattice::Lattice;
    use crate::species::Species;
    use nalgebra::Vector3;

    /// NaCl rocksalt: 4 Na + 4 Cl in conventional cell, a = 5.64 Å.
    fn make_nacl() -> Structure {
        let lattice = Lattice::cubic(5.64);
        let species = [
            vec![Species::neutral(Element::Na); 4],
            vec![Species::neutral(Element::Cl); 4],
        ]
        .concat();
        let frac_coords = vec![
            // Na sites (FCC sublattice)
            Vector3::new(0.0, 0.0, 0.0),
            Vector3::new(0.5, 0.5, 0.0),
            Vector3::new(0.5, 0.0, 0.5),
            Vector3::new(0.0, 0.5, 0.5),
            // Cl sites (shifted FCC sublattice)
            Vector3::new(0.5, 0.0, 0.0),
            Vector3::new(0.0, 0.5, 0.0),
            Vector3::new(0.0, 0.0, 0.5),
            Vector3::new(0.5, 0.5, 0.5),
        ];
        Structure::new(lattice, species, frac_coords)
    }

    /// Si diamond: 8 atoms in conventional cell, a = 5.431 Å.
    fn make_diamond_si() -> Structure {
        let a = 5.431;
        let lattice = Lattice::cubic(a);
        let species = vec![Species::neutral(Element::Si); 8];
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
        Structure::new(lattice, species, frac_coords)
    }

    /// Water molecule (non-periodic) in a bounding-box lattice.
    fn make_water_molecule() -> Structure {
        let mut lattice = Lattice::cubic(10.0);
        lattice.pbc = [false, false, false];
        let species = vec![
            Species::neutral(Element::O),
            Species::neutral(Element::H),
            Species::neutral(Element::H),
        ];
        // O at origin, two H atoms at ~0.96 Å with 104.5° angle
        let frac_coords = vec![
            Vector3::new(0.5, 0.5, 0.5),
            Vector3::new(0.5 + 0.096, 0.5, 0.5),
            Vector3::new(0.5 - 0.0245, 0.5 + 0.093, 0.5),
        ];
        Structure::new(lattice, species, frac_coords)
    }

    #[test]
    fn test_nacl_bonds_default() {
        // NaCl: each atom has CN=6 with nearest-neighbor distance a/2 = 2.82 Å.
        let nacl = make_nacl();
        let bonds = find_bonds(&nacl, &BondingStrategy::default());

        // Count bonds per site
        let mut counts = vec![0usize; nacl.num_sites()];
        for bond in &bonds {
            counts[bond.site_idx_1] += 1;
        }

        // Each Na bonded to 6 Cl and each Cl bonded to 6 Na
        for (idx, &count) in counts.iter().enumerate() {
            assert_eq!(count, 6, "Site {idx} has {count} bonds, expected 6");
        }

        // Check that Na sites bond only to Cl and vice versa
        for bond in &bonds {
            let elem_1 = nacl.site_occupancies[bond.site_idx_1]
                .dominant_species()
                .element;
            let elem_2 = nacl.site_occupancies[bond.site_idx_2]
                .dominant_species()
                .element;
            assert_ne!(
                elem_1, elem_2,
                "NaCl bonds should be between Na and Cl, got {elem_1}-{elem_2}"
            );
        }

        // Check bond distances (~2.82 Å = 5.64/2)
        let expected_dist = 5.64 / 2.0;
        for bond in &bonds {
            assert!(
                (bond.distance - expected_dist).abs() < 0.1,
                "Bond distance {} should be ~{expected_dist}",
                bond.distance
            );
        }
    }

    #[test]
    fn test_diamond_si_bonds() {
        // Diamond Si: each Si has CN=4 (tetrahedral), nn distance = a*sqrt(3)/4 ≈ 2.35 Å.
        let si = make_diamond_si();
        let bonds = find_bonds(&si, &BondingStrategy::default());

        let mut counts = vec![0usize; si.num_sites()];
        for bond in &bonds {
            counts[bond.site_idx_1] += 1;
        }

        for (idx, &count) in counts.iter().enumerate() {
            assert_eq!(
                count, 4,
                "Si site {idx} has {count} bonds, expected 4 (tetrahedral)"
            );
        }

        let expected_dist = 5.431 * 3.0_f64.sqrt() / 4.0;
        for bond in &bonds {
            assert!(
                (bond.distance - expected_dist).abs() < 0.05,
                "Si-Si distance {} should be ~{expected_dist}",
                bond.distance
            );
        }
    }

    #[test]
    fn test_water_molecule_non_periodic() {
        // Water molecule: O bonded to 2 H, each H bonded to 1 O, no PBC.
        let water = make_water_molecule();
        let bonds = find_bonds(&water, &BondingStrategy::CovalentRadius { scale: 1.3 });

        // O-H bonds only (H-H too far for bonding)
        assert_eq!(
            bonds.len(),
            4,
            "Expected 4 bond entries (2 O-H pairs × 2 directions)"
        );

        let mut o_bond_count = 0;
        let mut h_bond_count = 0;
        for bond in &bonds {
            let elem = water.site_occupancies[bond.site_idx_1]
                .dominant_species()
                .element;
            if elem == Element::O {
                o_bond_count += 1;
            } else {
                h_bond_count += 1;
            }
        }
        assert_eq!(o_bond_count, 2, "O should have 2 bonds");
        assert_eq!(h_bond_count, 2, "Each H should have 1 bond (2 total)");

        // All image offsets should be [0,0,0] (no periodicity)
        for bond in &bonds {
            assert_eq!(bond.image, [0, 0, 0], "Non-periodic: images must be zero");
        }
    }

    #[test]
    fn test_max_distance_strategy() {
        // MaxDistance strategy with custom cutoff on NaCl.
        let nacl = make_nacl();

        // Cutoff below nearest-neighbor distance: no bonds
        let bonds = find_bonds(&nacl, &BondingStrategy::MaxDistance { cutoff: 2.0 });
        assert!(bonds.is_empty(), "Cutoff too small should find no bonds");

        // Cutoff just above nn distance (~2.82 Å): only first shell
        let bonds = find_bonds(&nacl, &BondingStrategy::MaxDistance { cutoff: 3.0 });
        let mut counts = vec![0usize; nacl.num_sites()];
        for bond in &bonds {
            counts[bond.site_idx_1] += 1;
        }
        for &count in &counts {
            assert_eq!(count, 6, "NaCl first shell: 6 neighbors");
        }
    }

    #[test]
    fn test_get_bonded_neighbors_single_site() {
        // Query bonds for a single Na site in NaCl.
        let nacl = make_nacl();
        let bonds = get_bonded_neighbors(&nacl, 0, &BondingStrategy::default());

        assert_eq!(bonds.len(), 6, "Na site 0 should have 6 bonded neighbors");

        // All bonds should originate from site 0
        assert!(bonds.iter().all(|b| b.site_idx_1 == 0));

        // Sorted by distance
        let distances: Vec<f64> = bonds.iter().map(|b| b.distance).collect();
        assert!(distances.windows(2).all(|w| w[0] <= w[1]));
    }

    #[test]
    fn test_covalent_radius_scale_sensitivity() {
        // Varying the scale factor changes the number of detected bonds.
        let si = make_diamond_si();

        // Very tight scale: might miss some bonds
        let bonds_tight = find_bonds(&si, &BondingStrategy::CovalentRadius { scale: 0.8 });

        // Default scale
        let bonds_default = find_bonds(&si, &BondingStrategy::default());

        // Loose scale: should find at least as many as default
        let bonds_loose = find_bonds(&si, &BondingStrategy::CovalentRadius { scale: 1.5 });

        assert!(
            bonds_tight.len() <= bonds_default.len(),
            "Tighter scale should find <= bonds"
        );
        assert!(
            bonds_default.len() <= bonds_loose.len(),
            "Looser scale should find >= bonds"
        );
    }

    #[test]
    fn test_empty_structure() {
        // Empty structure returns no bonds.
        let empty = Structure::new(Lattice::cubic(5.0), vec![], vec![]);
        let bonds = find_bonds(&empty, &BondingStrategy::default());
        assert!(bonds.is_empty());
    }

    #[test]
    fn test_single_atom() {
        // Single-atom structure returns no bonds.
        let single = Structure::new(
            Lattice::cubic(5.0),
            vec![Species::neutral(Element::Cu)],
            vec![Vector3::new(0.0, 0.0, 0.0)],
        );
        let bonds = find_bonds(&single, &BondingStrategy::default());
        assert!(bonds.is_empty());
    }

    #[test]
    #[should_panic(expected = "out of bounds")]
    fn test_bonded_neighbors_out_of_bounds() {
        let nacl = make_nacl();
        get_bonded_neighbors(&nacl, 100, &BondingStrategy::default());
    }

    #[test]
    fn test_bond_struct_fields() {
        // Verify Bond fields are populated correctly.
        let nacl = make_nacl();
        let bonds = find_bonds(&nacl, &BondingStrategy::default());

        for bond in &bonds {
            assert!(bond.site_idx_1 < nacl.num_sites());
            assert!(bond.site_idx_2 < nacl.num_sites());
            assert!(bond.distance > 0.0);
        }
    }

    #[test]
    fn test_zero_scale_returns_no_bonds() {
        let nacl = make_nacl();
        let bonds = find_bonds(&nacl, &BondingStrategy::CovalentRadius { scale: 0.0 });
        assert!(bonds.is_empty(), "Zero scale should find no bonds");
    }

    #[test]
    fn test_default_strategy() {
        // Default is CovalentRadius with scale 1.1.
        assert_eq!(
            BondingStrategy::default(),
            BondingStrategy::CovalentRadius { scale: 1.1 }
        );
    }
}
