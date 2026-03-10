// === Common Types ===

use nalgebra::{Matrix3, Vector3};
use std::collections::HashMap;

/// Generic pair parameter storage for element-specific interactions.
#[derive(Debug, Clone)]
pub struct PairPotential<P: Clone> {
    /// Element-pair specific parameters
    params: HashMap<(u8, u8), P>,
    /// Default parameters for pairs not explicitly set
    default: P,
    /// Cutoff distance in Angstrom
    pub cutoff: f64,
}

impl<P: Clone> PairPotential<P> {
    /// Create a new pair potential with default parameters.
    pub fn new(default: P, cutoff: f64) -> Self {
        Self {
            params: HashMap::new(),
            default,
            cutoff,
        }
    }

    /// Get parameters for a specific element pair.
    pub fn get(&self, z1: u8, z2: u8) -> &P {
        let key = if z1 <= z2 { (z1, z2) } else { (z2, z1) };
        self.params.get(&key).unwrap_or(&self.default)
    }

    /// Set parameters for a specific element pair.
    pub fn set(&mut self, z1: u8, z2: u8, params: P) {
        let key = if z1 <= z2 { (z1, z2) } else { (z2, z1) };
        self.params.insert(key, params);
    }
}

/// Result of potential energy/force calculation.
#[derive(Debug, Clone)]
pub struct PotentialResult {
    /// Total potential energy in eV
    pub energy: f64,
    /// Forces on each atom in eV/Angstrom (Nx3)
    pub forces: Vec<Vector3<f64>>,
    /// Virial stress tensor in eV/Å³ (optional, 3x3 symmetric)
    pub stress: Option<Matrix3<f64>>,
    /// Per-atom energies (optional)
    pub per_atom_energies: Option<Vec<f64>>,
}
