//! Read-only scientific analysis on crystal structures.
//!
//! Each submodule operates on [`Structure`](crate::structure::Structure) without modifying it.

pub mod batch; // batch processing for structure matching
pub mod bonding; // bond-order and connectivity analysis
pub mod brillouin; // Brillouin zone and k-path generation
pub mod chempot; // chemical potential diagram computation
pub mod convex_hull; // thermodynamic stability (convex hull construction)
pub mod coordination; // coordination number and environment analysis
pub mod elastic; // elastic tensor and mechanical properties
pub mod magnetism; // magnetic ordering analysis
pub mod order_params; // bond orientational order parameters (Steinhardt)
pub mod oxidation; // oxidation state assignment
pub mod prototype; // AFLOW prototype structure labeling
pub mod rdf; // radial distribution functions
pub mod structure_matcher; // structure comparison and deduplication
pub mod surfaces; // surface energy and slab analysis
pub mod thermo; // finite-temperature gas-phase thermodynamics
pub mod trajectory; // molecular dynamics trajectory analysis
pub mod xrd; // X-ray diffraction pattern simulation
