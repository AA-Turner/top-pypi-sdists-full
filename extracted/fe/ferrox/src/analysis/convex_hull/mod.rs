//! Convex hull construction and 0 K energetics.
//!
//! This module implements a generalized N-dimensional lower convex hull and
//! energy-above-hull (`e_above_hull`) calculations inspired by matterviz and
//! pymatgen convex-hull logic.

mod energetics;
mod interpolation;
mod linalg;
mod quickhull;

pub use energetics::{
    build_lower_hull, calculate_e_above_hull, compute_e_form_per_atom,
    find_lowest_energy_unary_refs,
};
pub use interpolation::compute_e_above_hull_nd;
pub use quickhull::{compute_lower_hull_nd, compute_quickhull_nd};

use crate::composition::Composition;
use crate::element::Element;
use crate::error::{FerroxError, Result};
use std::collections::HashSet;

/// Numerical tolerance used throughout hull calculations.
const HULL_EPSILON: f64 = 1e-9;
/// Slightly relaxed tolerance for barycentric membership checks.
const BARYCENTRIC_TOL: f64 = HULL_EPSILON * 1.001;

/// Input entry for convex-hull calculations.
#[derive(Debug, Clone)]
pub struct ConvexHullEntry {
    /// Optional external identifier (e.g. mp-id).
    pub entry_id: Option<String>,
    /// Composition of the phase.
    pub composition: Composition,
    /// Total energy (eV) of the entry.
    pub energy: f64,
    /// Optional precomputed per-atom energy (eV/atom).
    pub energy_per_atom: Option<f64>,
    /// Optional precomputed formation energy (eV/atom).
    pub e_form_per_atom: Option<f64>,
    /// Optional total-energy correction (eV).
    pub correction: Option<f64>,
}

impl ConvexHullEntry {
    /// Construct a new entry from composition and total energy.
    pub fn new(composition: Composition, energy: f64) -> Self {
        Self {
            entry_id: None,
            composition,
            energy,
            energy_per_atom: None,
            e_form_per_atom: None,
            correction: None,
        }
    }

    /// Build a stable key for this entry.
    pub fn id_or_formula(&self) -> String {
        self.entry_id
            .clone()
            .unwrap_or_else(|| self.composition.reduced_formula())
    }

    /// Return true if this entry is unary.
    pub fn is_unary(&self) -> bool {
        self.composition.element_composition().num_elements() == 1
    }

    /// Return this entry's corrected energy per atom.
    pub fn corrected_energy_per_atom(&self) -> Result<f64> {
        let atom_count = self.composition.num_atoms();
        if !atom_count.is_finite() || atom_count <= 0.0 {
            return Err(FerroxError::CompositionError {
                reason: format!(
                    "Entry {} has non-positive atom count ({atom_count})",
                    self.id_or_formula()
                ),
            });
        }

        let value = if let Some(correction_total) = self.correction {
            let total_energy = if let Some(energy_per_atom) = self.energy_per_atom {
                energy_per_atom * atom_count
            } else {
                self.energy
            };
            (total_energy + correction_total) / atom_count
        } else if let Some(energy_per_atom) = self.energy_per_atom {
            energy_per_atom
        } else {
            self.energy / atom_count
        };

        if !value.is_finite() {
            return Err(FerroxError::CompositionError {
                reason: format!("Entry {} has non-finite energy", self.id_or_formula()),
            });
        }
        Ok(value)
    }
}

/// Hyperplane in N dimensions: `normal · x + offset = 0`.
#[derive(Debug, Clone)]
pub struct HyperplaneND {
    /// Unit normal vector.
    pub normal: Vec<f64>,
    /// Plane offset.
    pub offset: f64,
}

/// Facet on an N-dimensional convex hull.
#[derive(Debug, Clone)]
pub struct SimplexFaceND {
    /// Point indices defining this facet.
    pub vertex_indices: Vec<usize>,
    /// Facet hyperplane.
    pub plane: HyperplaneND,
    /// Facet centroid.
    pub centroid: Vec<f64>,
    /// Point indices known to lie outside this facet.
    pub outside_points: HashSet<usize>,
}

/// Lower hull model built from reference entries.
#[derive(Debug, Clone)]
pub struct LowerHullND {
    /// Element ordering used for barycentric-like coordinates.
    pub element_order: Vec<Element>,
    /// Points used to construct the hull.
    pub reference_points: Vec<Vec<f64>>,
    /// Lower hull facets (downward in energy dimension).
    pub lower_facets: Vec<SimplexFaceND>,
}

#[cfg(test)]
mod tests;
