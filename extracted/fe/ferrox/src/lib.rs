//! # ferrox
//!
//! High-performance base layer for computational materials science.
//!
//! This crate provides fast implementations of common materials science operations
//! including I/O, structure matching, symmetry analysis, molecular dynamics, surface
//! science, defect engineering, and trajectory analysis.
//!
//! ## Features
//!
//! - **Structure I/O**: Parse CIF, POSCAR, extXYZ, LAMMPS, and more
//! - **Structure Matching**: Fast deduplication and grouping with parallel processing
//! - **Symmetry Analysis**: Space groups, Wyckoff positions, primitive/conventional cells
//! - **Molecular Dynamics**: NVE/NVT integrators, thermostats, classical potentials
//! - **Surface Science**: Slab generation, Miller indices, adsorption sites
//! - **Defect Engineering**: Vacancies, substitutions, interstitials, Voronoi sites
//! - **Trajectory Analysis**: RDF, MSD, diffusion coefficients, order parameters
//! - **Python bindings**: Optional PyO3 bindings, compatible with pymatgen dictionaries
//! - **WASM bindings**: Optional wasm-bindgen bindings for browser use
//!
//! ## Example
//!
//! ```rust,ignore
//! use ferrox::structure::Structure;
//! use ferrox::structure_matcher::StructureMatcher;
//!
//! let matcher = StructureMatcher::new()
//!     .with_latt_len_tol(0.2)
//!     .with_site_pos_tol(0.3)
//!     .with_angle_tol(5.0);
//!
//! let is_match = matcher.fit(&struct1, &struct2);
//! ```

#![warn(missing_docs)]
#![warn(clippy::all)]

pub mod error;

// Core types
pub mod composition;
pub mod element;
pub mod lattice;
pub mod species;
pub mod structure;

// Foundational utilities
pub mod algorithms;
pub mod cell_ops;
pub mod neighbors;
pub mod pbc;

// Structure generation
pub mod defects;
pub mod distortions;

// Transformations (internal - public API is via Structure methods)
pub(crate) mod transformations;

// Domain clusters
pub mod analysis;
pub mod io;
pub mod simulation;

// Re-exports for convenience
pub use algorithms::EnumConfig;
pub use transformations::{OrderDisorderedConfig, PartialRemoveConfig};

// Re-exports for convenience
pub use error::{FerroxError, OnError, Result};

// Python bindings (optional, also enabled for stub generation via `stub-gen -> python`).
#[cfg(feature = "python")]
pub mod python;

#[cfg(feature = "python")]
use pyo3::prelude::*;

// WASM bindings (optional)
#[cfg(feature = "wasm")]
pub mod wasm;

#[cfg(feature = "wasm")]
pub use wasm::types as wasm_types;

/// Python module entry point using declarative submodules.
/// Each submodule is a real Python module registered in sys.modules.
#[cfg(feature = "python")]
#[pymodule]
mod _ferrox {
    use pyo3::prelude::*;

    #[pymodule_export]
    use crate::python::element::Element;

    // Keep in sync with submodules.rs define_submodule! calls and stub_gen.rs submodules array
    #[pymodule_export]
    use crate::python::submodules::bonding;
    #[pymodule_export]
    use crate::python::submodules::cell;
    #[pymodule_export]
    use crate::python::submodules::chempot;
    #[pymodule_export]
    use crate::python::submodules::composition;
    #[pymodule_export]
    use crate::python::submodules::convex_hull;
    #[pymodule_export]
    use crate::python::submodules::coordination;
    #[pymodule_export]
    use crate::python::submodules::defects;
    #[pymodule_export]
    use crate::python::submodules::elastic;
    #[pymodule_export]
    use crate::python::submodules::io;
    #[pymodule_export]
    use crate::python::submodules::lattice;
    #[pymodule_export]
    use crate::python::submodules::md;
    #[pymodule_export]
    use crate::python::submodules::mp;
    #[pymodule_export]
    use crate::python::submodules::neighbors;
    #[pymodule_export]
    use crate::python::submodules::optimizers;
    #[pymodule_export]
    use crate::python::submodules::order_params;
    #[pymodule_export]
    use crate::python::submodules::oxidation;
    #[pymodule_export]
    use crate::python::submodules::potentials;
    #[pymodule_export]
    use crate::python::submodules::properties;
    #[pymodule_export]
    use crate::python::submodules::rdf;
    #[pymodule_export]
    use crate::python::submodules::species;
    #[pymodule_export]
    use crate::python::submodules::structure;
    #[pymodule_export]
    use crate::python::submodules::surfaces;
    #[pymodule_export]
    use crate::python::submodules::symmetry;
    #[pymodule_export]
    use crate::python::submodules::trajectory;
    #[pymodule_export]
    use crate::python::submodules::vasp;
    #[pymodule_export]
    use crate::python::submodules::xrd;

    #[pymodule_init]
    fn init(module: &Bound<'_, PyModule>) -> PyResult<()> {
        module.add("__version__", env!("CARGO_PKG_VERSION"))?;
        crate::python::element::register(module)?;
        Ok(())
    }
}
