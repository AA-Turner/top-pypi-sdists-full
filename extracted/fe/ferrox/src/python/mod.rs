//! Python bindings for ferrox.
//!
//! This module provides PyO3 bindings organized into submodules:
//! - `ferrox.cell` - Cell reduction and transformations
//! - `ferrox.composition` - Formula parsing and composition analysis
//! - `ferrox.convex_hull` - Convex hull and energy-above-hull
//! - `ferrox.coordination` - Coordination number analysis
//! - `ferrox.defects` - Point defect generation
//! - `ferrox.elastic` - Elastic tensor calculations
//! - `ferrox.io` - File I/O and format conversion
//! - `ferrox.lattice` - Lattice operations
//! - `ferrox.md` - Molecular dynamics integrators
//! - `ferrox.mp` - Materials Project integration
//! - `ferrox.neighbors` - Distance and neighbor calculations
//! - `ferrox.optimizers` - Geometry optimizers (FIRE, CellFIRE)
//! - `ferrox.order_params` - Order parameters (Steinhardt Q)
//! - `ferrox.oxidation` - Oxidation state analysis
//! - `ferrox.potentials` - Classical interatomic potentials
//! - `ferrox.properties` - Physical property calculations
//! - `ferrox.rdf` - Radial distribution functions
//! - `ferrox.species` - Chemical species with oxidation states
//! - `ferrox.structure` - Structure manipulation and matching
//! - `ferrox.surfaces` - Surface and slab operations
//! - `ferrox.symmetry` - Space group and symmetry operations
//! - `ferrox.trajectory` - Trajectory analysis
//! - `ferrox.vasp` - VASP file I/O (CHGCAR parsing, Fourier extraction)
//! - `ferrox.xrd` - X-ray diffraction

// PyO3 proc macros generate code that triggers false positive clippy warnings
#![allow(clippy::useless_conversion)]

// Define stub info gatherer for pyo3-stub-gen
pyo3_stub_gen::define_stub_info_gatherer!(stub_info);

// Shared helpers
pub mod helpers;

// OOP classes
pub mod classes;

// Submodules
pub mod bonding;
pub mod cell;
pub mod chempot;
pub mod composition;
pub mod convex_hull;
pub mod coordination;
pub mod defects;
pub mod elastic;
pub mod element;
pub mod io;
pub mod lattice;
pub mod md;
pub mod mp;
pub mod neighbors;
pub mod optimizers;
pub mod order_params;
pub mod oxidation;
pub mod potentials;
pub mod properties;
pub mod rdf;
pub mod species;
pub mod structure;
pub mod surfaces;
pub mod symmetry;
pub mod trajectory;
pub mod vasp;
pub mod xrd;

// Declarative submodule definitions (each is a standalone #[pymodule])
pub mod submodules;
