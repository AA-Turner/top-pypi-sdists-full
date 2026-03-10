//! Surface analysis module for crystallographic surfaces.
//!
//! This module provides functionality for:
//! - Miller index manipulation and enumeration
//! - Surface termination analysis
//! - Adsorption site finding
//! - Surface energy calculations
//! - Wulff construction for equilibrium crystal shapes

/// Default cutoff distance for neighbor analysis in adsorption site finding (Å).
pub const DEFAULT_NEIGHBOR_CUTOFF: f64 = 4.0;

/// Default tolerance for identifying surface atoms (Å).
pub const DEFAULT_SURFACE_TOLERANCE: f64 = 0.1;

mod adsorption_finding;
mod adsorption_types;
mod analysis;
mod miller;
mod slab_extension;
mod termination;
mod wulff;

pub use adsorption_finding::find_adsorption_sites;
pub use adsorption_types::{AdsorptionSite, AdsorptionSiteType};
pub use analysis::{SurfaceEnergy, calculate_surface_energy, get_surface_atoms, surface_area};
pub use miller::{MillerIndex, enumerate_miller_indices};
pub use slab_extension::{SlabConfigExt, enumerate_terminations};
pub use termination::SurfaceTermination;
pub use wulff::{WulffFacet, WulffShape, compute_wulff_shape, d_spacing, miller_to_normal};

#[cfg(test)]
mod tests;
