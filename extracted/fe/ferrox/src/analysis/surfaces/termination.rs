// === Surface Termination ===

use super::MillerIndex;
use crate::species::Species;
use crate::structure::Structure;
use serde::{Deserialize, Serialize};

/// A surface termination representing a specific way to cut a crystal surface.
///
/// Different terminations expose different atomic arrangements at the surface,
/// which affects surface properties like energy, polarity, and reactivity.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SurfaceTermination {
    /// Miller index defining the surface orientation
    pub miller_index: MillerIndex,
    /// Shift along the surface normal (fractional coordinates)
    pub shift: f64,
    /// Species present at the surface
    pub surface_species: Vec<Species>,
    /// Surface atomic density (atoms per Å²)
    pub surface_density: f64,
    /// Whether the surface is polar (has net dipole)
    pub is_polar: bool,
    /// The slab structure for this termination
    pub slab: Structure,
}

impl SurfaceTermination {
    /// Create a new surface termination.
    pub fn new(
        miller_index: MillerIndex,
        shift: f64,
        surface_species: Vec<Species>,
        surface_density: f64,
        is_polar: bool,
        slab: Structure,
    ) -> Self {
        Self {
            miller_index,
            shift,
            surface_species,
            surface_density,
            is_polar,
            slab,
        }
    }
}
