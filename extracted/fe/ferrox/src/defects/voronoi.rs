use super::{InterstitialSiteType, classify_interstitial_site};
use crate::pbc::wrap_frac_coords_pbc;
#[cfg(not(target_arch = "wasm32"))]
use crate::pbc::{count_atoms_at_distance, min_distance_to_atoms};
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};

// === Voronoi-Based Interstitial Site Finding ===

/// Enhanced interstitial site information from Voronoi analysis.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VoronoiInterstitial {
    /// Position in fractional coordinates.
    pub frac_coords: Vector3<f64>,
    /// Position in Cartesian coordinates.
    pub cart_coords: Vector3<f64>,
    /// Distance to the nearest atom.
    pub min_distance: f64,
    /// Number of nearest neighbors (vertices of Voronoi cell).
    pub coordination: usize,
    /// Classification of the site geometry.
    pub site_type: InterstitialSiteType,
    /// Wyckoff label if symmetry analysis was performed.
    pub wyckoff_label: Option<String>,
    /// Number of symmetry-equivalent sites.
    pub multiplicity: usize,
}

// Voronoi implementation is not available for wasm32 due to meshless_voronoi dependency
#[cfg(not(target_arch = "wasm32"))]
use glam::DVec3;
#[cfg(not(target_arch = "wasm32"))]
use meshless_voronoi::{Dimensionality, VoronoiIntegrator};

/// Find interstitial sites using Voronoi tessellation.
///
/// This method identifies potential interstitial positions as vertices
/// of the Voronoi tessellation of the atomic positions. Sites are filtered
/// by minimum distance and optionally reduced by symmetry.
///
/// # Arguments
///
/// * `structure` - The structure to analyze
/// * `min_dist` - Minimum distance to nearest atom (default: 0.5 Å if None)
/// * `symprec` - Symmetry precision for equivalent site detection
///
/// # Returns
///
/// Vector of `VoronoiInterstitial` sites, sorted by decreasing min_distance.
///
/// # Note
///
/// For non-orthogonal lattices, accuracy may be reduced due to the rectangular
/// bounding box used by the Voronoi algorithm.
///
/// On wasm32 targets, this function returns an empty vector since meshless_voronoi
/// is not available.
#[cfg(not(target_arch = "wasm32"))]
pub fn find_voronoi_interstitials(
    structure: &Structure,
    min_dist: Option<f64>,
    symprec: f64,
) -> Vec<VoronoiInterstitial> {
    // Handle empty structure
    if structure.num_sites() == 0 {
        return Vec::new();
    }

    let lattice = &structure.lattice;
    let num_sites = structure.num_sites();

    // Default minimum distance
    let min_distance_threshold = min_dist.unwrap_or(0.5);

    // Build 3x3x3 supercell positions to handle PBC correctly
    // The Voronoi algorithm uses a rectangular box, so we need to ensure
    // periodic images are included
    let mut supercell_positions: Vec<DVec3> = Vec::with_capacity(num_sites * 27);
    let mut original_cart_coords: Vec<Vector3<f64>> = Vec::with_capacity(num_sites);

    for frac in &structure.frac_coords {
        let cart = lattice.get_cartesian_coord(frac);
        original_cart_coords.push(cart);

        // Add 3x3x3 periodic images
        for img_a in -1..=1_i32 {
            for img_b in -1..=1_i32 {
                for img_c in -1..=1_i32 {
                    let shift = lattice.get_cartesian_coord(&Vector3::new(
                        img_a as f64,
                        img_b as f64,
                        img_c as f64,
                    ));
                    let pos = cart + shift;
                    supercell_positions.push(DVec3::new(pos.x, pos.y, pos.z));
                }
            }
        }
    }

    // Compute bounding box for the supercell
    let matrix = lattice.matrix();
    let lattice_vectors: [Vector3<f64>; 3] = [
        matrix.row(0).transpose(),
        matrix.row(1).transpose(),
        matrix.row(2).transpose(),
    ];

    // Compute min/max extent of the 3x3x3 supercell
    let (anchor, width) = compute_supercell_bounds(&lattice_vectors);

    // Build Voronoi tessellation using VoronoiIntegrator to get vertices
    let voronoi_integrator = VoronoiIntegrator::build(
        &supercell_positions,
        None, // no mask - compute all cells
        anchor,
        width,
        Dimensionality::ThreeD,
        false, // not periodic - we handle PBC via supercell
    );

    // Convert to get face/vertex information
    let voronoi_with_faces = voronoi_integrator.with_faces();

    // Collect all unique vertices
    let mut unique_vertices: Vec<Vector3<f64>> = Vec::new();

    for cell in voronoi_with_faces.cells_iter() {
        for vertex in &cell.vertices {
            let pos = Vector3::new(vertex.loc.x, vertex.loc.y, vertex.loc.z);

            // Check if this vertex is inside or near the central unit cell
            let frac = lattice.get_fractional_coord(&pos);
            if !is_near_unit_cell(&frac, 0.1) {
                continue;
            }

            // Check if vertex is unique (not already in list)
            let is_duplicate = unique_vertices.iter().any(|existing| {
                // Use shared min_distance_to_atoms with single-element slice for separation check
                let sep = min_distance_to_atoms(&pos, &[*existing], lattice.matrix(), lattice.pbc);
                sep < symprec
            });

            if !is_duplicate {
                unique_vertices.push(pos);
            }
        }
    }

    // Process each unique vertex to create interstitial sites
    let mut interstitials: Vec<VoronoiInterstitial> = Vec::new();
    let pbc = lattice.pbc;
    let matrix = lattice.matrix();

    for cart_pos in unique_vertices {
        // Calculate minimum distance to any atom
        let min_atom_dist = min_distance_to_atoms(&cart_pos, &original_cart_coords, matrix, pbc);

        // Filter by minimum distance threshold
        if min_atom_dist < min_distance_threshold {
            continue;
        }

        // Map to unit cell [0, 1) only along periodic axes
        let frac = lattice.get_fractional_coord(&cart_pos);
        let wrapped_frac = wrap_frac_coords_pbc(&frac, pbc);
        let wrapped_cart = lattice.get_cartesian_coord(&wrapped_frac);

        // Check if this wrapped position is a duplicate
        let existing_carts: Vec<Vector3<f64>> =
            interstitials.iter().map(|i| i.cart_coords).collect();
        let sep_to_existing = min_distance_to_atoms(&wrapped_cart, &existing_carts, matrix, pbc);
        if sep_to_existing < symprec {
            continue;
        }

        // Count coordination (atoms at approximately the same distance)
        let coordination = count_atoms_at_distance(
            &wrapped_cart,
            &original_cart_coords,
            matrix,
            pbc,
            min_atom_dist,
            0.3,
        );

        // Classify site type
        let site_type = classify_interstitial_site(coordination);

        interstitials.push(VoronoiInterstitial {
            frac_coords: wrapped_frac,
            cart_coords: wrapped_cart,
            min_distance: min_atom_dist,
            coordination,
            site_type,
            wyckoff_label: None, // To be filled by symmetry analysis
            multiplicity: 1,     // To be updated by symmetry reduction
        });
    }

    // Sort by min_distance (largest first - most spacious sites)
    interstitials.sort_by(|site_a, site_b| {
        site_b
            .min_distance
            .partial_cmp(&site_a.min_distance)
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    interstitials
}

/// Compute bounding box for a 3x3x3 supercell.
#[cfg(not(target_arch = "wasm32"))]
fn compute_supercell_bounds(lattice_vectors: &[Vector3<f64>; 3]) -> (DVec3, DVec3) {
    let mut min_corner = Vector3::new(f64::MAX, f64::MAX, f64::MAX);
    let mut max_corner = Vector3::new(f64::MIN, f64::MIN, f64::MIN);

    // Check all 8 corners of the 3x3x3 supercell (from -1 to 2 in each direction)
    for corner_a in [-1, 2] {
        for corner_b in [-1, 2] {
            for corner_c in [-1, 2] {
                let corner = lattice_vectors[0] * corner_a as f64
                    + lattice_vectors[1] * corner_b as f64
                    + lattice_vectors[2] * corner_c as f64;
                min_corner.x = min_corner.x.min(corner.x);
                min_corner.y = min_corner.y.min(corner.y);
                min_corner.z = min_corner.z.min(corner.z);
                max_corner.x = max_corner.x.max(corner.x);
                max_corner.y = max_corner.y.max(corner.y);
                max_corner.z = max_corner.z.max(corner.z);
            }
        }
    }

    // Add small padding to avoid edge effects
    let padding = 0.1;
    let anchor = DVec3::new(
        min_corner.x - padding,
        min_corner.y - padding,
        min_corner.z - padding,
    );
    let width = DVec3::new(
        max_corner.x - min_corner.x + 2.0 * padding,
        max_corner.y - min_corner.y + 2.0 * padding,
        max_corner.z - min_corner.z + 2.0 * padding,
    );

    (anchor, width)
}

/// Check if fractional coordinates are near the unit cell [0, 1).
#[cfg(not(target_arch = "wasm32"))]
fn is_near_unit_cell(frac: &Vector3<f64>, tolerance: f64) -> bool {
    let lower = -tolerance;
    let upper = 1.0 + tolerance;
    frac.x >= lower
        && frac.x < upper
        && frac.y >= lower
        && frac.y < upper
        && frac.z >= lower
        && frac.z < upper
}

/// Wasm32 fallback: returns empty vector since meshless_voronoi is not available.
#[cfg(target_arch = "wasm32")]
pub fn find_voronoi_interstitials(
    _structure: &Structure,
    _min_dist: Option<f64>,
    _symprec: f64,
) -> Vec<VoronoiInterstitial> {
    Vec::new()
}
