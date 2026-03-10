use super::{CellList, NeighborList, NeighborListConfig, wrap_frac_coords};
use crate::lattice::Lattice;
use crate::structure::Structure;
use nalgebra::Vector3;

#[cfg(feature = "rayon")]
use rayon::prelude::*;

/// Build a neighbor list using the cell-list algorithm.
///
/// This is the main entry point for neighbor finding. For systems with more than
/// ~100 atoms, this is significantly faster than brute-force O(n²) approaches.
///
/// # Arguments
///
/// * `structure` - The crystal structure to analyze
/// * `config` - Configuration for neighbor list computation
///
/// # Returns
///
/// A `NeighborList` containing all atom pairs within the cutoff distance.
pub fn build_neighbor_list(structure: &Structure, config: &NeighborListConfig) -> NeighborList {
    let n_atoms = structure.num_sites();
    let cutoff = config.cutoff;

    // Handle edge cases
    if n_atoms == 0 || cutoff <= 0.0 {
        return NeighborList::new();
    }

    let lattice = &structure.lattice;
    let pbc = lattice.pbc;
    let frac_coords = &structure.frac_coords;

    // Get Cartesian coordinates and lattice vectors
    let cart_coords = structure.cart_coords();
    let matrix = lattice.matrix();
    let lattice_vecs = [
        matrix.row(0).transpose(),
        matrix.row(1).transpose(),
        matrix.row(2).transpose(),
    ];

    // Compute the search range for periodic images
    // For each axis, determine how many periodic images we need to consider
    let volume = lattice.volume();
    let max_images: [i32; 3] = std::array::from_fn(|idx| {
        if !pbc[idx] {
            0
        } else {
            let cross = lattice_vecs[(idx + 1) % 3].cross(&lattice_vecs[(idx + 2) % 3]);
            let height = volume / cross.norm();
            (cutoff / height).ceil() as i32
        }
    });

    // For small systems or when we need many periodic images, fall back to brute-force
    // The cell-list approach has overhead that isn't worth it for small systems
    let use_cell_list = n_atoms > config.cell_list_threshold
        && max_images.iter().all(|&m| m <= 1)
        && pbc.iter().all(|&p| p);

    if use_cell_list {
        build_neighbor_list_celllist(frac_coords, &cart_coords, lattice, &lattice_vecs, config)
    } else {
        build_neighbor_list_bruteforce(&cart_coords, &lattice_vecs, pbc, &max_images, config)
    }
}

/// Build neighbor list using cell-list algorithm (O(n) for large systems).
fn build_neighbor_list_celllist(
    frac_coords: &[Vector3<f64>],
    cart_coords: &[Vector3<f64>],
    lattice: &Lattice,
    lattice_vecs: &[Vector3<f64>; 3],
    config: &NeighborListConfig,
) -> NeighborList {
    let cutoff = config.cutoff;
    let cutoff_sq = cutoff * cutoff;
    let pbc = lattice.pbc;
    let n_atoms = frac_coords.len();

    // Build cell list
    let cell_list = CellList::build(frac_coords, lattice, cutoff);

    // Estimate capacity (12 neighbors per atom is typical for close-packed structures)
    let estimated_pairs = n_atoms * 12;

    #[cfg(feature = "rayon")]
    let result = {
        // Parallel processing: each atom computes its neighbors independently
        let per_atom_results: Vec<NeighborList> = (0..n_atoms)
            .into_par_iter()
            .map(|center_idx| {
                let mut local_nl = NeighborList::with_capacity(20);
                let center_cart = &cart_coords[center_idx];
                let center_frac = &frac_coords[center_idx];
                let wrapped_center = wrap_frac_coords(center_frac);

                // Find which bin this atom is in
                let bx = ((wrapped_center.x / cell_list.bin_size_frac[0]).floor() as usize)
                    .min(cell_list.n_bins[0] - 1);
                let by = ((wrapped_center.y / cell_list.bin_size_frac[1]).floor() as usize)
                    .min(cell_list.n_bins[1] - 1);
                let bz = ((wrapped_center.z / cell_list.bin_size_frac[2]).floor() as usize)
                    .min(cell_list.n_bins[2] - 1);
                let center_bin = cell_list.bin_index(bx, by, bz);

                // Check all neighboring bins
                for (neighbor_bin, base_image) in cell_list.neighbor_bins(center_bin, pbc) {
                    for &neighbor_idx in &cell_list.bins[neighbor_bin] {
                        // Compute distance with periodic image
                        let offset = (base_image[0] as f64) * lattice_vecs[0]
                            + (base_image[1] as f64) * lattice_vecs[1]
                            + (base_image[2] as f64) * lattice_vecs[2];

                        let neighbor_cart = cart_coords[neighbor_idx] + offset;
                        let diff = neighbor_cart - center_cart;
                        let dist_sq = diff.norm_squared();

                        if dist_sq <= cutoff_sq {
                            // Check self-interaction
                            let is_self = center_idx == neighbor_idx
                                && base_image == [0, 0, 0]
                                && dist_sq < config.numerical_tol * config.numerical_tol;

                            if !is_self || config.self_interaction {
                                local_nl.push(center_idx, neighbor_idx, dist_sq.sqrt(), base_image);
                            }
                        }
                    }
                }

                local_nl
            })
            .collect();

        // Merge all per-atom results
        let mut result = NeighborList::with_capacity(estimated_pairs);
        for nl in per_atom_results {
            result.extend(nl);
        }
        result
    };

    #[cfg(not(feature = "rayon"))]
    let result = {
        let mut result = NeighborList::with_capacity(estimated_pairs);

        for center_idx in 0..n_atoms {
            let center_cart = &cart_coords[center_idx];
            let center_frac = &frac_coords[center_idx];
            let wrapped_center = wrap_frac_coords(center_frac);

            // Find which bin this atom is in
            let bx = ((wrapped_center.x / cell_list.bin_size_frac[0]).floor() as usize)
                .min(cell_list.n_bins[0] - 1);
            let by = ((wrapped_center.y / cell_list.bin_size_frac[1]).floor() as usize)
                .min(cell_list.n_bins[1] - 1);
            let bz = ((wrapped_center.z / cell_list.bin_size_frac[2]).floor() as usize)
                .min(cell_list.n_bins[2] - 1);
            let center_bin = cell_list.bin_index(bx, by, bz);

            // Check all neighboring bins
            for (neighbor_bin, base_image) in cell_list.neighbor_bins(center_bin, pbc) {
                for &neighbor_idx in &cell_list.bins[neighbor_bin] {
                    // Compute distance with periodic image
                    let offset = (base_image[0] as f64) * lattice_vecs[0]
                        + (base_image[1] as f64) * lattice_vecs[1]
                        + (base_image[2] as f64) * lattice_vecs[2];

                    let neighbor_cart = cart_coords[neighbor_idx] + offset;
                    let diff = neighbor_cart - center_cart;
                    let dist_sq = diff.norm_squared();

                    if dist_sq <= cutoff_sq {
                        // Check self-interaction
                        let is_self = center_idx == neighbor_idx
                            && base_image == [0, 0, 0]
                            && dist_sq < config.numerical_tol * config.numerical_tol;

                        if !is_self || config.self_interaction {
                            result.push(center_idx, neighbor_idx, dist_sq.sqrt(), base_image);
                        }
                    }
                }
            }
        }

        result
    };

    result
}

/// Build neighbor list using brute-force O(n²) algorithm.
///
/// Used for small systems or when many periodic images are needed.
fn build_neighbor_list_bruteforce(
    cart_coords: &[Vector3<f64>],
    lattice_vecs: &[Vector3<f64>; 3],
    pbc: [bool; 3],
    max_images: &[i32; 3],
    config: &NeighborListConfig,
) -> NeighborList {
    let n_atoms = cart_coords.len();
    let cutoff = config.cutoff;
    let cutoff_sq = cutoff * cutoff;
    let tol_sq = config.numerical_tol * config.numerical_tol;

    // Estimate capacity
    let estimated_pairs = n_atoms * 12;
    let mut result = NeighborList::with_capacity(estimated_pairs);

    // Image ranges (only check non-negative for non-periodic)
    let x_range: Vec<i32> = if pbc[0] {
        (-max_images[0]..=max_images[0]).collect()
    } else {
        vec![0]
    };
    let y_range: Vec<i32> = if pbc[1] {
        (-max_images[1]..=max_images[1]).collect()
    } else {
        vec![0]
    };
    let z_range: Vec<i32> = if pbc[2] {
        (-max_images[2]..=max_images[2]).collect()
    } else {
        vec![0]
    };

    for (center_idx, center_cart) in cart_coords.iter().enumerate() {
        for (neighbor_idx, neighbor_cart) in cart_coords.iter().enumerate() {
            for &dx in &x_range {
                for &dy in &y_range {
                    for &dz in &z_range {
                        let offset = (dx as f64) * lattice_vecs[0]
                            + (dy as f64) * lattice_vecs[1]
                            + (dz as f64) * lattice_vecs[2];

                        let diff = neighbor_cart + offset - center_cart;
                        let dist_sq = diff.norm_squared();

                        if dist_sq <= cutoff_sq {
                            // Check self-interaction
                            let is_self = center_idx == neighbor_idx
                                && dx == 0
                                && dy == 0
                                && dz == 0
                                && dist_sq < tol_sq;

                            if !is_self || config.self_interaction {
                                result.push(center_idx, neighbor_idx, dist_sq.sqrt(), [dx, dy, dz]);
                            }
                        }
                    }
                }
            }
        }
    }

    result
}

/// Get neighbors for a single site.
///
/// This is a convenience function that returns only neighbors for one site.
///
/// # Arguments
///
/// * `structure` - The crystal structure
/// * `site_idx` - Index of the site to find neighbors for
/// * `cutoff` - Maximum distance in Angstroms
///
/// # Returns
///
/// A vector of `(neighbor_idx, distance, image)` tuples, sorted by distance.
pub fn get_site_neighbors(
    structure: &Structure,
    site_idx: usize,
    cutoff: f64,
) -> Vec<(usize, f64, [i32; 3])> {
    assert!(
        site_idx < structure.num_sites(),
        "site_idx {} out of bounds (num_sites={})",
        site_idx,
        structure.num_sites()
    );

    let config = NeighborListConfig {
        cutoff,
        ..Default::default()
    };

    let nl = build_neighbor_list(structure, &config);

    // Filter to only include neighbors of the specified site
    let mut neighbors: Vec<_> = nl
        .center_indices
        .iter()
        .enumerate()
        .filter(|&(_, c)| *c == site_idx)
        .map(|(idx, _)| (nl.neighbor_indices[idx], nl.distances[idx], nl.images[idx]))
        .collect();

    // Sort by distance
    neighbors.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));

    neighbors
}
