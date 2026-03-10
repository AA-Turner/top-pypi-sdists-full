// === Data Structures ===

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Bond valence parameters for an element (O'Keeffe & Brese 1991).
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct BvParams {
    /// Bond valence radius parameter
    pub r: f64,
    /// Electronegativity-related parameter
    pub c: f64,
}

/// BVS statistics from ICSD data.
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct BvStats {
    /// Mean BVS value
    pub mean: f64,
    /// Standard deviation
    pub std: f64,
    /// Number of data points
    pub n: u32,
}

/// Result of oxidation state guessing.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OxiStateGuess {
    /// Oxidation states per element (average if multiple sites)
    pub oxidation_states: HashMap<String, f64>,
    /// Probability score (higher is more likely)
    pub probability: f64,
}
