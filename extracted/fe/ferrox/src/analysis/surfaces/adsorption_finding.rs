// === Adsorption Site Finding ===

use super::{
    AdsorptionSite, AdsorptionSiteType, DEFAULT_NEIGHBOR_CUTOFF, DEFAULT_SURFACE_TOLERANCE,
    get_surface_atoms,
};
use crate::error::{Result, check_non_negative};
use crate::structure::Structure;
use nalgebra::Vector3;
use std::collections::HashSet;

/// Find adsorption sites on a surface.
///
/// Identifies atop, bridge, and hollow sites on the surface of a slab.
///
/// # Arguments
///
/// * `slab` - The slab structure
/// * `height` - Height above surface for placing adsorbates (Å). Must be non-negative and finite.
/// * `site_types` - Optional filter for site types (None = all types)
/// * `neighbor_cutoff` - Optional cutoff for neighbor analysis (default: 4.0 Å).
///   May need adjustment for structures with longer bonds (e.g., some oxides)
///   or shorter bonds in close-packed structures.
/// * `surface_tolerance` - Optional tolerance for identifying surface atoms (default: 0.1 Å).
///
/// # Returns
///
/// `Result<Vec<AdsorptionSite>>` - Vector of adsorption sites found on the surface.
///
/// # Errors
///
/// Returns `FerroxError` if `height` is negative or non-finite.
pub fn find_adsorption_sites(
    slab: &Structure,
    height: f64,
    site_types: Option<&[AdsorptionSiteType]>,
    neighbor_cutoff: Option<f64>,
    surface_tolerance: Option<f64>,
) -> Result<Vec<AdsorptionSite>> {
    check_non_negative(height, "height")?;

    let mut sites = Vec::new();

    // Get surface atoms with specified tolerance
    let tolerance = surface_tolerance.unwrap_or(DEFAULT_SURFACE_TOLERANCE);
    let surface_indices = get_surface_atoms(slab, tolerance);

    if surface_indices.is_empty() {
        return Ok(sites);
    }

    // Get Cartesian positions of surface atoms
    let cart_coords = slab.cart_coords();
    let surface_cart: Vec<Vector3<f64>> = surface_indices
        .iter()
        .map(|&idx| cart_coords[idx])
        .collect();

    // Get average z-coordinate of surface atoms
    let avg_z: f64 =
        surface_cart.iter().map(|coord| coord.z).sum::<f64>() / surface_cart.len() as f64;

    // Height for placing sites above surface
    let site_z = avg_z + height;

    // Check if we should include each site type
    let include_atop = site_types
        .map(|types| types.contains(&AdsorptionSiteType::Atop))
        .unwrap_or(true);
    let include_bridge = site_types
        .map(|types| types.contains(&AdsorptionSiteType::Bridge))
        .unwrap_or(true);
    let include_hollow3 = site_types
        .map(|types| types.contains(&AdsorptionSiteType::Hollow3))
        .unwrap_or(true);
    let include_hollow4 = site_types
        .map(|types| types.contains(&AdsorptionSiteType::Hollow4))
        .unwrap_or(true);

    // Atop sites: directly above each surface atom
    if include_atop {
        for (local_idx, &global_idx) in surface_indices.iter().enumerate() {
            let cart = surface_cart[local_idx];
            let cart_pos = Vector3::new(cart.x, cart.y, site_z);
            let frac_pos = slab.lattice.get_fractional_coord(&cart_pos);

            sites.push(AdsorptionSite::new(
                AdsorptionSiteType::Atop,
                frac_pos,
                cart_pos,
                height,
                vec![global_idx],
                1,
            ));
        }
    }

    // Bridge and hollow sites require neighbor analysis
    if include_bridge || include_hollow3 || include_hollow4 {
        // Build neighbor list for surface atoms
        let cutoff = neighbor_cutoff.unwrap_or(DEFAULT_NEIGHBOR_CUTOFF);
        let (center_idx, neighbor_idx, images, distances) =
            slab.get_neighbor_list(cutoff, 1e-8, true);

        // Build adjacency set for O(1) neighbor lookups
        // Store edges as (min, max) pairs with image offset for the larger index
        let surface_set: HashSet<usize> = surface_indices.iter().copied().collect();
        // Store edges with image info: key=(min_idx, max_idx), value=image_offset for max_idx relative to min_idx
        let mut edges_with_images: std::collections::HashMap<(usize, usize), [i32; 3]> =
            std::collections::HashMap::new();
        for (((&ci, &ni), &image), &dist) in center_idx
            .iter()
            .zip(neighbor_idx.iter())
            .zip(images.iter())
            .zip(distances.iter())
        {
            if dist < cutoff && surface_set.contains(&ci) && surface_set.contains(&ni) {
                let (edge, stored_image) = if ci < ni {
                    ((ci, ni), image)
                } else {
                    ((ni, ci), [-image[0], -image[1], -image[2]])
                };
                edges_with_images.entry(edge).or_insert(stored_image);
            }
        }
        let edges: HashSet<(usize, usize)> = edges_with_images.keys().copied().collect();

        // Helper to check if two atoms are neighbors using the prebuilt set
        let are_neighbors = |a: usize, b: usize| -> bool {
            let edge = if a < b { (a, b) } else { (b, a) };
            edges.contains(&edge)
        };

        // Build adjacency list for efficient neighbor iteration
        let mut adjacency: std::collections::HashMap<usize, Vec<usize>> =
            std::collections::HashMap::new();
        for &(a, b) in &edges {
            adjacency.entry(a).or_default().push(b);
            adjacency.entry(b).or_default().push(a);
        }

        // Map from global index to local index for position lookup
        let global_to_local: std::collections::HashMap<usize, usize> = surface_indices
            .iter()
            .enumerate()
            .map(|(local, &global)| (global, local))
            .collect();

        // Helper to get image-shifted Cartesian position
        let get_shifted_cart = |global_idx: usize, image: [i32; 3]| -> Vector3<f64> {
            let idx = global_to_local[&global_idx];
            let base_cart = surface_cart[idx];
            let shift = slab.lattice.get_cartesian_coord(&Vector3::new(
                image[0] as f64,
                image[1] as f64,
                image[2] as f64,
            ));
            base_cart + shift
        };

        // Bridge sites: at midpoint of each edge (accounting for periodic images)
        if include_bridge {
            for (&(global_i, global_j), &image_j) in &edges_with_images {
                let idx_i = global_to_local[&global_i];
                let cart_i = surface_cart[idx_i];
                // global_j is at image_j relative to global_i
                let cart_j = get_shifted_cart(global_j, image_j);
                let midpoint = (cart_i + cart_j) / 2.0;
                let cart_pos = Vector3::new(midpoint.x, midpoint.y, site_z);
                let frac_pos = slab.lattice.get_fractional_coord(&cart_pos);

                sites.push(AdsorptionSite::new(
                    AdsorptionSiteType::Bridge,
                    frac_pos,
                    cart_pos,
                    height,
                    vec![global_i, global_j],
                    1,
                ));
            }
        }

        // Helper to get image offset from a to b (b's image relative to a)
        let get_image = |a: usize, b: usize| -> [i32; 3] {
            if a < b {
                edges_with_images.get(&(a, b)).copied().unwrap_or([0, 0, 0])
            } else {
                let img = edges_with_images.get(&(b, a)).copied().unwrap_or([0, 0, 0]);
                [-img[0], -img[1], -img[2]]
            }
        };

        // Hollow sites require finding triangular or square arrangements
        if include_hollow3 || include_hollow4 {
            // Find triangles: for each edge (i,j), find common neighbors k
            if include_hollow3 {
                let mut found_triangles: HashSet<(usize, usize, usize)> = HashSet::new();
                for &(global_i, global_j) in &edges {
                    if let (Some(neighbors_i), Some(neighbors_j)) =
                        (adjacency.get(&global_i), adjacency.get(&global_j))
                    {
                        // Find common neighbors
                        let set_i: HashSet<usize> = neighbors_i.iter().copied().collect();
                        for &global_k in neighbors_j {
                            if global_k > global_j && set_i.contains(&global_k) {
                                // Found triangle i-j-k, normalize order to avoid duplicates
                                let mut tri = [global_i, global_j, global_k];
                                tri.sort();
                                if found_triangles.insert((tri[0], tri[1], tri[2])) {
                                    // Compute centroid using image-shifted coordinates
                                    // Use global_i as reference (image = [0,0,0])
                                    let idx_i = global_to_local[&global_i];
                                    let cart_i = surface_cart[idx_i];
                                    let image_j = get_image(global_i, global_j);
                                    let cart_j = get_shifted_cart(global_j, image_j);
                                    let image_k = get_image(global_i, global_k);
                                    let cart_k = get_shifted_cart(global_k, image_k);

                                    let centroid = (cart_i + cart_j + cart_k) / 3.0;
                                    let cart_pos = Vector3::new(centroid.x, centroid.y, site_z);
                                    let frac_pos = slab.lattice.get_fractional_coord(&cart_pos);

                                    sites.push(AdsorptionSite::new(
                                        AdsorptionSiteType::Hollow3,
                                        frac_pos,
                                        cart_pos,
                                        height,
                                        vec![global_i, global_j, global_k],
                                        1,
                                    ));
                                }
                            }
                        }
                    }
                }
            }

            // Hollow4: find quadrilaterals by looking for cycles of 4
            if include_hollow4 && surface_indices.len() >= 4 {
                let mut found_quads: HashSet<(usize, usize, usize, usize)> = HashSet::new();
                // For each edge (i,j), look for two other atoms k,l such that
                // i-k, k-l, l-j are all edges (forming i-j-l-k cycle)
                for &(global_i, global_j) in &edges {
                    if let (Some(neighbors_i), Some(neighbors_j)) =
                        (adjacency.get(&global_i), adjacency.get(&global_j))
                    {
                        // For each neighbor k of i (k != j)
                        for &global_k in neighbors_i {
                            if global_k == global_j {
                                continue;
                            }
                            // For each neighbor l of j (l != i, l != k)
                            for &global_l in neighbors_j {
                                if global_l == global_i || global_l == global_k {
                                    continue;
                                }
                                // Check if k-l is an edge
                                if are_neighbors(global_k, global_l) {
                                    // Found quadrilateral i-k-l-j
                                    let mut quad = [global_i, global_j, global_k, global_l];
                                    quad.sort();
                                    if found_quads.insert((quad[0], quad[1], quad[2], quad[3])) {
                                        // Compute centroid using image-shifted coordinates
                                        // Use global_i as reference (image = [0,0,0])
                                        // For diagonal neighbors (l), compute image by chaining
                                        // through the neighbor path: i->j->l
                                        let idx_i = global_to_local[&global_i];
                                        let cart_i = surface_cart[idx_i];
                                        let image_j = get_image(global_i, global_j);
                                        let cart_j = get_shifted_cart(global_j, image_j);
                                        let image_k = get_image(global_i, global_k);
                                        let cart_k = get_shifted_cart(global_k, image_k);
                                        // l is a neighbor of j, not necessarily of i, so compose images
                                        let image_j_to_l = get_image(global_j, global_l);
                                        let image_l = [
                                            image_j[0] + image_j_to_l[0],
                                            image_j[1] + image_j_to_l[1],
                                            image_j[2] + image_j_to_l[2],
                                        ];
                                        let cart_l = get_shifted_cart(global_l, image_l);

                                        let centroid = (cart_i + cart_j + cart_k + cart_l) / 4.0;
                                        let cart_pos = Vector3::new(centroid.x, centroid.y, site_z);
                                        let frac_pos = slab.lattice.get_fractional_coord(&cart_pos);

                                        sites.push(AdsorptionSite::new(
                                            AdsorptionSiteType::Hollow4,
                                            frac_pos,
                                            cart_pos,
                                            height,
                                            vec![global_i, global_j, global_k, global_l],
                                            1,
                                        ));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Ok(sites)
}
