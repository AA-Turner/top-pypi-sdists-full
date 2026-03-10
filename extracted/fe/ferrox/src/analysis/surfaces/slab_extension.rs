// === Slab Config Extension ===

use super::{
    DEFAULT_SURFACE_TOLERANCE, MillerIndex, SurfaceTermination, get_surface_atoms, surface_area,
};
use crate::error::Result;
use crate::species::Species;
use crate::structure::Structure;
use std::collections::HashSet;

/// Extended configuration for slab generation with additional surface analysis options.
///
/// This extends the basic SlabConfig from structure.rs with additional
/// parameters for surface termination enumeration.
#[derive(Debug, Clone)]
pub struct SlabConfigExt {
    /// Basic slab configuration
    pub miller_index: MillerIndex,
    /// Minimum slab thickness in Angstroms
    pub min_slab_size: f64,
    /// Minimum vacuum thickness in Angstroms
    pub min_vacuum: f64,
    /// Center the slab in the vacuum
    pub center_slab: bool,
    /// Interpret min_slab_size as number of unit planes
    pub in_unit_planes: bool,
    /// Reduce to primitive surface cell
    pub primitive: bool,
    /// Maximum search range for surface normal basis vectors
    pub max_normal_search: i32,
    /// Symmetrize the slab
    pub symmetrize: bool,
}

impl Default for SlabConfigExt {
    fn default() -> Self {
        Self {
            miller_index: MillerIndex::new(1, 0, 0),
            min_slab_size: 10.0,
            min_vacuum: 10.0,
            center_slab: true,
            in_unit_planes: false,
            primitive: false,
            max_normal_search: 5,
            symmetrize: false,
        }
    }
}

impl SlabConfigExt {
    /// Create a new config with the given Miller index.
    pub fn new(miller_index: MillerIndex) -> Self {
        Self {
            miller_index,
            ..Default::default()
        }
    }

    /// Set the minimum slab size.
    #[must_use]
    pub fn with_min_slab_size(mut self, size: f64) -> Self {
        self.min_slab_size = size;
        self
    }

    /// Set the minimum vacuum size.
    #[must_use]
    pub fn with_min_vacuum(mut self, vacuum: f64) -> Self {
        self.min_vacuum = vacuum;
        self
    }

    /// Set whether to center the slab.
    #[must_use]
    pub fn with_center_slab(mut self, center: bool) -> Self {
        self.center_slab = center;
        self
    }

    /// Set whether min_slab_size is in unit planes.
    #[must_use]
    pub fn with_in_unit_planes(mut self, in_planes: bool) -> Self {
        self.in_unit_planes = in_planes;
        self
    }

    /// Set whether to reduce to primitive cell.
    #[must_use]
    pub fn with_primitive(mut self, primitive: bool) -> Self {
        self.primitive = primitive;
        self
    }

    /// Convert to the basic SlabConfig used by Structure::generate_slabs
    pub fn to_slab_config(&self, symprec: f64) -> crate::structure::SlabConfig {
        crate::structure::SlabConfig {
            miller_index: self.miller_index.to_array(),
            min_slab_size: self.min_slab_size,
            min_vacuum_size: self.min_vacuum,
            center_slab: self.center_slab,
            in_unit_planes: self.in_unit_planes,
            primitive: self.primitive,
            symprec,
            termination_index: None,
        }
    }
}

/// Enumerate all unique terminations for a given Miller index.
///
/// This uses the structure's generate_slabs method to find all unique
/// surface terminations and wraps them in SurfaceTermination structs
/// with additional metadata.
///
/// # Arguments
///
/// * `structure` - The bulk structure
/// * `miller_index` - The surface orientation
/// * `config` - Configuration for slab generation
/// * `symprec` - Symmetry precision for identifying unique terminations
///
/// # Returns
///
/// Vector of unique surface terminations.
pub fn enumerate_terminations(
    structure: &Structure,
    miller_index: MillerIndex,
    config: &SlabConfigExt,
    symprec: f64,
) -> Result<Vec<SurfaceTermination>> {
    // Use the existing SlabConfig infrastructure
    let slab_config = crate::structure::SlabConfig {
        miller_index: miller_index.to_array(),
        min_slab_size: config.min_slab_size,
        min_vacuum_size: config.min_vacuum,
        center_slab: config.center_slab,
        in_unit_planes: config.in_unit_planes,
        primitive: config.primitive,
        symprec,
        termination_index: None,
    };

    let slabs = structure.generate_slabs(&slab_config)?;

    let mut terminations = Vec::new();
    for (idx, slab) in slabs.into_iter().enumerate() {
        // Calculate surface properties
        let area = surface_area(&slab);
        let surface_atoms = get_surface_atoms(&slab, DEFAULT_SURFACE_TOLERANCE);
        let surface_species: Vec<Species> = surface_atoms
            .iter()
            .filter_map(|&site_idx| slab.site_occupancies.get(site_idx))
            .map(|occ| *occ.dominant_species())
            .collect();

        let density = if area > 0.0 {
            surface_atoms.len() as f64 / area
        } else {
            0.0
        };

        // Calculate is_polar by comparing top vs bottom surface compositions
        let is_polar = {
            // Get top surface species (already computed as surface_species)
            let top_species: HashSet<Species> = surface_species.iter().cloned().collect();

            // Get bottom surface species (atoms near minimum z)
            let min_z = slab
                .frac_coords
                .iter()
                .map(|coord| coord.z)
                .fold(f64::INFINITY, f64::min);
            let bottom_atoms: Vec<usize> = slab
                .frac_coords
                .iter()
                .enumerate()
                .filter(|(_, coord)| (coord.z - min_z).abs() < DEFAULT_SURFACE_TOLERANCE)
                .map(|(site_idx, _)| site_idx)
                .collect();
            let bottom_species: HashSet<Species> = bottom_atoms
                .iter()
                .filter_map(|&site_idx| slab.site_occupancies.get(site_idx))
                .map(|occ| *occ.dominant_species())
                .collect();

            // Polar if top and bottom have different species compositions
            !top_species.is_empty() && !bottom_species.is_empty() && top_species != bottom_species
        };

        // Note: The shift value is a placeholder index (0.0, 0.1, 0.2, ...) rather than
        // an actual fractional coordinate along the surface normal. This provides a
        // unique identifier for each termination but doesn't represent the true
        // crystallographic shift. Use the slab structure directly for accurate geometry.
        terminations.push(SurfaceTermination::new(
            miller_index,
            idx as f64 * 0.1, // Termination index (not a true fractional shift)
            surface_species,
            density,
            is_polar,
            slab,
        ));
    }

    Ok(terminations)
}
