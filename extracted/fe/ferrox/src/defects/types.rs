use crate::impl_display_via_as_str;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};

// === Defect Types ===

/// Type of point defect in a crystal structure.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DefectType {
    /// Vacancy: missing atom at a lattice site.
    Vacancy,
    /// Interstitial: extra atom at a non-lattice position.
    Interstitial,
    /// Substitution: atom of different species at a lattice site.
    Substitution,
    /// Antisite: two atoms swapped between their normal sites.
    Antisite,
}

impl DefectType {
    /// Convert defect type to string representation.
    pub fn as_str(&self) -> &'static str {
        match self {
            DefectType::Vacancy => "vacancy",
            DefectType::Interstitial => "interstitial",
            DefectType::Substitution => "substitution",
            DefectType::Antisite => "antisite",
        }
    }
}

impl_display_via_as_str!(DefectType);

/// A point defect in a crystal structure.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PointDefect {
    /// Type of defect.
    pub defect_type: DefectType,
    /// Index of the defect site (for vacancy/substitution) or -1 for interstitial.
    pub site_idx: Option<usize>,
    /// Position of the defect in fractional coordinates.
    pub position: Vector3<f64>,
    /// Species at the defect site (new species for substitution/interstitial).
    pub species: Option<Species>,
    /// Original species before defect formation (for vacancy/substitution).
    pub original_species: Option<Species>,
    /// Charge state of the defect.
    pub charge: i32,
}

impl PointDefect {
    /// Create a new vacancy defect.
    pub fn vacancy(site_idx: usize, position: Vector3<f64>, original_species: Species) -> Self {
        Self {
            defect_type: DefectType::Vacancy,
            site_idx: Some(site_idx),
            position,
            species: None,
            original_species: Some(original_species),
            charge: 0,
        }
    }

    /// Create a new substitution defect.
    pub fn substitution(
        site_idx: usize,
        position: Vector3<f64>,
        new_species: Species,
        original_species: Species,
    ) -> Self {
        Self {
            defect_type: DefectType::Substitution,
            site_idx: Some(site_idx),
            position,
            species: Some(new_species),
            original_species: Some(original_species),
            charge: 0,
        }
    }

    /// Create a new interstitial defect.
    pub fn interstitial(position: Vector3<f64>, species: Species) -> Self {
        Self {
            defect_type: DefectType::Interstitial,
            site_idx: None,
            position,
            species: Some(species),
            original_species: None,
            charge: 0,
        }
    }

    /// Set the charge state of the defect.
    pub fn with_charge(mut self, charge: i32) -> Self {
        self.charge = charge;
        self
    }

    /// Generate a doped-compatible name for this point defect.
    ///
    /// Naming conventions:
    /// - Vacancy: `v_{element}` or `v_{element}_{wyckoff}` (e.g., "v_O", "v_O_4a")
    /// - Substitution: `{new}_on_{original}` (e.g., "Fe_on_Ni")
    /// - Interstitial: `{element}_i` or `{element}_i_{site_type}` (e.g., "Li_i", "Li_i_oct")
    /// - Antisite: `{A}_{B}` swap notation (e.g., "Fe_Ni" for Fe on Ni site)
    ///
    /// # Arguments
    ///
    /// * `wyckoff` - Optional Wyckoff label for the defect site (e.g., "4a", "8c")
    /// * `site_type` - Optional site type for interstitials (e.g., "oct", "tet")
    ///
    /// # Returns
    ///
    /// A string name following doped naming conventions.
    pub fn name(&self, wyckoff: Option<&str>, site_type: Option<&str>) -> String {
        match self.defect_type {
            DefectType::Vacancy => {
                let element = self
                    .original_species
                    .as_ref()
                    .map(|sp| sp.element.symbol())
                    .unwrap_or("X");
                match wyckoff {
                    Some(wyk) => format!("v_{element}_{wyk}"),
                    None => format!("v_{element}"),
                }
            }
            DefectType::Substitution => {
                let new_elem = self
                    .species
                    .as_ref()
                    .map(|sp| sp.element.symbol())
                    .unwrap_or("X");
                let orig_elem = self
                    .original_species
                    .as_ref()
                    .map(|sp| sp.element.symbol())
                    .unwrap_or("X");
                format!("{new_elem}_on_{orig_elem}")
            }
            DefectType::Interstitial => {
                let element = self
                    .species
                    .as_ref()
                    .map(|sp| sp.element.symbol())
                    .unwrap_or("X");
                match site_type {
                    Some(st) => format!("{element}_i_{st}"),
                    None => format!("{element}_i"),
                }
            }
            DefectType::Antisite => {
                // For antisite, species is the new one, original_species is what was there
                let new_elem = self
                    .species
                    .as_ref()
                    .map(|sp| sp.element.symbol())
                    .unwrap_or("X");
                let orig_elem = self
                    .original_species
                    .as_ref()
                    .map(|sp| sp.element.symbol())
                    .unwrap_or("X");
                format!("{new_elem}_{orig_elem}")
            }
        }
    }
}

/// Generate a doped-compatible name for a point defect.
///
/// This is a convenience function that calls `PointDefect::name()`.
/// See that method for full documentation on naming conventions.
///
/// # Arguments
///
/// * `defect` - The point defect to name
/// * `wyckoff` - Optional Wyckoff label for the defect site
/// * `site_type` - Optional site type for interstitials (e.g., "oct", "tet")
///
/// # Returns
///
/// A string name following doped naming conventions.
pub fn generate_defect_name(
    defect: &PointDefect,
    wyckoff: Option<&str>,
    site_type: Option<&str>,
) -> String {
    defect.name(wyckoff, site_type)
}

/// Result of creating a defect structure.
#[derive(Debug, Clone)]
pub struct DefectStructure {
    /// The defective structure.
    pub structure: Structure,
    /// Information about the defect.
    pub defect: PointDefect,
}
