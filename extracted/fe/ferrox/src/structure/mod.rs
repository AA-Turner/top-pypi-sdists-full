//! Crystal structure representation.
//!
//! This module provides the [`Structure`] type for representing periodic and
//! non-periodic atomic systems with a [`Lattice`], site occupancies, and
//! fractional coordinates.
//!
//! ```
//! use ferrox::structure::Structure;
//! use ferrox::lattice::Lattice;
//! use ferrox::species::Species;
//! use ferrox::element::Element;
//! use nalgebra::Vector3;
//!
//! let structure = Structure::new(
//!     Lattice::cubic(5.64),
//!     vec![Species::neutral(Element::Na), Species::neutral(Element::Cl)],
//!     vec![Vector3::new(0.0, 0.0, 0.0), Vector3::new(0.5, 0.5, 0.5)],
//! );
//! assert_eq!(structure.num_sites(), 2);
//! ```

use crate::lattice::Lattice;
use crate::species::SiteOccupancy;
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// A symmetry operation represented as a rotation matrix and translation vector.
/// The rotation is a 3x3 integer matrix (in fractional coordinates) and the
/// translation is a 3-element float array (in fractional coordinates).
pub type SymmetryOperation = ([[i32; 3]; 3], [f64; 3]);

/// Information about a Wyckoff position in a crystal structure.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WyckoffSite {
    /// Wyckoff label (e.g., "4a", "8c", "24d").
    pub label: String,
    /// Multiplicity of the site.
    pub multiplicity: usize,
    /// Point group symmetry at this site (e.g., "m..", "-1", "4mm").
    pub site_symmetry: String,
    /// Representative fractional coordinates.
    pub representative_coords: Vector3<f64>,
}

/// Lattice reduction algorithm choice.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReductionAlgo {
    /// Niggli reduction - produces unique reduced cell with a <= b <= c
    Niggli,
    /// LLL reduction - produces nearly orthogonal basis (faster, less unique)
    LLL,
}

/// A crystal structure with lattice, site occupancies, and coordinates.
///
/// Each site can have multiple species with partial occupancies (disordered sites).
/// For ordered sites, there is a single species with occupancy 1.0.
///
/// For non-periodic systems (molecules), use `set_pbc([false, false, false])`.
/// The lattice is still required but can be a dummy/bounding-box lattice.
///
/// **Important**: Always use `set_pbc()` to modify periodicity - this keeps
/// `Structure.pbc` and `Lattice.pbc` synchronized. Direct field assignment
/// may cause desync issues.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Structure {
    /// The crystal lattice.
    pub lattice: Lattice,
    /// Site occupancies (species + occupancy) at each site.
    pub site_occupancies: Vec<SiteOccupancy>,
    /// Fractional coordinates for each site.
    pub frac_coords: Vec<Vector3<f64>>,
    /// Periodic boundary conditions for each axis (default: all true).
    /// Use `set_pbc()` to modify - keeps lattice.pbc in sync.
    #[serde(default = "default_pbc")]
    pub pbc: [bool; 3],
    /// Total charge (relevant for molecules, default: 0.0).
    #[serde(default)]
    pub charge: f64,
    /// Optional properties (for caching).
    #[serde(default)]
    pub properties: HashMap<String, serde_json::Value>,
}

/// Default PBC is fully periodic.
fn default_pbc() -> [bool; 3] {
    [true, true, true]
}

// impl/ submodules (these all add `impl Structure { ... }` blocks)
#[path = "impl/bond_valence_and_species_impl.rs"]
mod bond_valence_and_species_impl;
#[path = "impl/constructors_and_basic_impl.rs"]
mod constructors_and_basic_impl;
#[path = "impl/coordination_interpolation_matching_impl.rs"]
mod coordination_interpolation_matching_impl;
#[path = "impl/neighbors_impl.rs"]
mod neighbors_impl;
#[path = "impl/sorting_copy_supercell_reduction_impl.rs"]
mod sorting_copy_supercell_reduction_impl;
#[path = "impl/symmetry_dataset_methods_impl.rs"]
mod symmetry_dataset_methods_impl;

mod ordering_and_enumeration;
mod slab;
mod supercell_helpers;
mod symmetry_helpers;
mod symmetry_ops;
mod transformations;

pub use slab::SlabConfig;
pub use symmetry_ops::SymmOp;

#[allow(unused_imports)]
pub(crate) use symmetry_helpers::{
    SpacegroupTypeInfo, geometric_crystal_class_from_hall, laue_group_from_point_group,
    mat3_to_array, moyo_ops_to_arrays, point_group_is_centrosymmetric, point_group_is_chiral,
    point_group_is_polar, point_group_symbol, spacegroup_to_crystal_system,
    spacegroup_type_from_number,
};

#[cfg(test)]
mod tests;
