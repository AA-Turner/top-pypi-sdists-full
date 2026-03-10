use crate::impl_display_via_as_str;
use serde::{Deserialize, Serialize};

// === Interstitial Site Finding ===

/// Classification of interstitial site geometry.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum InterstitialSiteType {
    /// Trigonal site (3 neighbors).
    Trigonal,
    /// Tetrahedral site (4 neighbors).
    Tetrahedral,
    /// Square pyramidal site (5 neighbors).
    SquarePyramidal,
    /// Octahedral site (6 neighbors).
    Octahedral,
    /// Cubic site (8 neighbors).
    Cubic,
    /// Cuboctahedral site (12 neighbors).
    Cuboctahedral,
    /// Other coordination environment.
    Other,
}

impl InterstitialSiteType {
    /// Convert to string representation.
    pub fn as_str(&self) -> &'static str {
        match self {
            InterstitialSiteType::Trigonal => "trigonal",
            InterstitialSiteType::Tetrahedral => "tetrahedral",
            InterstitialSiteType::SquarePyramidal => "square_pyramidal",
            InterstitialSiteType::Octahedral => "octahedral",
            InterstitialSiteType::Cubic => "cubic",
            InterstitialSiteType::Cuboctahedral => "cuboctahedral",
            InterstitialSiteType::Other => "other",
        }
    }
}

impl_display_via_as_str!(InterstitialSiteType);

/// Classify an interstitial site based on its coordination number.
///
/// # Arguments
///
/// * `coordination` - The coordination number of the site.
///
/// # Returns
///
/// The classified site type.
pub fn classify_interstitial_site(coordination: usize) -> InterstitialSiteType {
    match coordination {
        3 => InterstitialSiteType::Trigonal,
        4 => InterstitialSiteType::Tetrahedral,
        5 => InterstitialSiteType::SquarePyramidal,
        6 => InterstitialSiteType::Octahedral,
        8 => InterstitialSiteType::Cubic,
        12 => InterstitialSiteType::Cuboctahedral,
        _ => InterstitialSiteType::Other,
    }
}
