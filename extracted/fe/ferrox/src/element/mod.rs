//! Chemical element definitions.
//!
//! This module provides the `Element` enum representing all 118 chemical elements,
//! along with associated data like atomic numbers, symbols, and electronegativities.
//!
//! Extended element data (oxidation states, ionic radii, Shannon radii) is loaded
//! from a gzipped JSON file at compile time and decompressed once on first access.

use flate2::read::GzDecoder;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::io::Read;
use std::sync::OnceLock;

mod element_enum;
mod normalization;

mod r#impl;

pub use element_enum::Element;
pub use normalization::{NormalizedSymbol, normalize_symbol};

// === Extended Element Data (loaded from gzipped JSON) ===

/// Compile-time embedded gzipped JSON data (single source of truth shared with TypeScript).
const ELEMENT_DATA_GZ: &[u8] = include_bytes!("../data/element_data.json.gz");

/// Decompressed JSON string (lazily initialized on first access).
static ELEMENT_DATA_JSON: OnceLock<String> = OnceLock::new();

fn get_element_data_json() -> &'static str {
    ELEMENT_DATA_JSON.get_or_init(|| {
        let mut decoder = GzDecoder::new(ELEMENT_DATA_GZ);
        let mut json = String::new();
        decoder
            .read_to_string(&mut json)
            .expect("Failed to decompress element data");
        json
    })
}

/// Shannon radius pair: crystal and ionic radii in Angstroms.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ShannonRadiusPair {
    /// Crystal radius in Angstroms.
    pub crystal_radius: f64,
    /// Ionic radius in Angstroms.
    pub ionic_radius: f64,
}

/// Shannon radii: coordination -> spin -> radii.
pub type ShannonCoordination = HashMap<String, HashMap<String, ShannonRadiusPair>>;

/// Shannon radii for all oxidation states: oxidation_state -> coordination -> spin -> radii.
pub type ShannonRadii = HashMap<String, ShannonCoordination>;

/// Element data from JSON (for deserialization).
#[derive(Debug, Deserialize)]
pub(crate) struct ElementData {
    name: String,
    atomic_radius: Option<f64>,
    covalent_radius: Option<f64>,
    oxidation_states: Option<Vec<i8>>,
    common_oxidation_states: Option<Vec<i8>>,
    icsd_oxidation_states: Option<Vec<i8>>,
    ionic_radii: Option<HashMap<String, f64>>,
    shannon_radii: Option<ShannonRadii>,
    // Physical properties
    melting_point: Option<f64>,
    boiling_point: Option<f64>,
    density: Option<f64>,
    electron_affinity: Option<f64>,
    ionization_energies: Option<Vec<f64>>,
    first_ionization: Option<f64>,
    molar_heat: Option<f64>,
    specific_heat: Option<f64>,
    // Electron configuration
    n_valence: Option<u8>,
    electron_configuration: Option<String>,
    electron_configuration_semantic: Option<String>,
}

static ELEMENT_DATA: OnceLock<Vec<ElementData>> = OnceLock::new();

pub(crate) fn get_element_data(z: u8) -> Option<&'static ElementData> {
    if !(1..=118).contains(&z) {
        return None;
    }
    let data = ELEMENT_DATA.get_or_init(|| {
        serde_json::from_str(get_element_data_json()).expect("Failed to parse element data JSON")
    });
    data.get((z - 1) as usize)
}

/// Periodic table block (s, p, d, f).
///
/// Note: Helium (He) is placed in group 18 with noble gases for chemical property
/// reasons, so it returns `Block::P` despite having a 1s² electron configuration.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Block {
    /// s-block (groups 1-2, except He)
    S,
    /// p-block (groups 13-18, including He)
    P,
    /// d-block (groups 3-12)
    D,
    /// f-block (lanthanoids and actinoids, except Lu and Lr)
    F,
}

impl Block {
    /// Get the block as a stable string representation.
    pub fn as_str(&self) -> &'static str {
        match self {
            Block::S => "S",
            Block::P => "P",
            Block::D => "D",
            Block::F => "F",
        }
    }
}

impl std::fmt::Display for Block {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

impl std::fmt::Display for Element {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.symbol())
    }
}

#[cfg(test)]
mod tests;
