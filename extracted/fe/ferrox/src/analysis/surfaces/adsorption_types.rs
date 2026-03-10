// === Adsorption Sites ===

use crate::impl_display_via_as_str;
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};

/// Type of adsorption site on a surface.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum AdsorptionSiteType {
    /// Atop site - directly above a surface atom
    Atop,
    /// Bridge site - between two surface atoms
    Bridge,
    /// Hollow site with 3-fold coordination
    Hollow3,
    /// Hollow site with 4-fold coordination
    Hollow4,
    /// Other site type
    Other,
}

impl AdsorptionSiteType {
    /// Parse from string representation.
    pub fn parse(type_str: &str) -> Option<Self> {
        match type_str.to_lowercase().as_str() {
            "atop" | "on_top" | "top" => Some(Self::Atop),
            "bridge" => Some(Self::Bridge),
            "hollow3" | "hollow_3" | "fcc" | "hcp" => Some(Self::Hollow3),
            "hollow4" | "hollow_4" | "hollow" => Some(Self::Hollow4),
            "other" => Some(Self::Other),
            _ => None,
        }
    }

    /// Get string representation.
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Atop => "atop",
            Self::Bridge => "bridge",
            Self::Hollow3 => "hollow3",
            Self::Hollow4 => "hollow4",
            Self::Other => "other",
        }
    }
}

impl_display_via_as_str!(AdsorptionSiteType);

/// An adsorption site on a surface.
///
/// Represents a location where adsorbates can bind to the surface.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AdsorptionSite {
    /// Type of adsorption site
    pub site_type: AdsorptionSiteType,
    /// Position in fractional coordinates
    pub position: Vector3<f64>,
    /// Position in Cartesian coordinates
    pub cart_position: Vector3<f64>,
    /// Height above the surface (Å)
    pub height: f64,
    /// Indices of surface atoms coordinating this site
    pub coordinating_atoms: Vec<usize>,
    /// Symmetry multiplicity of this site
    pub symmetry_multiplicity: usize,
}

impl AdsorptionSite {
    /// Create a new adsorption site.
    pub fn new(
        site_type: AdsorptionSiteType,
        position: Vector3<f64>,
        cart_position: Vector3<f64>,
        height: f64,
        coordinating_atoms: Vec<usize>,
        symmetry_multiplicity: usize,
    ) -> Self {
        Self {
            site_type,
            position,
            cart_position,
            height,
            coordinating_atoms,
            symmetry_multiplicity,
        }
    }
}
