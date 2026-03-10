//! Enhanced periodic boundary condition and cell operations.
//!
//! This module provides advanced cell manipulation functions including:
//! - Minimum image distance calculations for any cell geometry
//! - Niggli and Delaunay cell reduction algorithms
//! - Supercell generation strategies
//! - Lattice equivalence checking

mod delaunay;
mod equivalence;
mod helpers;
mod minimum_image;
mod niggli;
mod supercell;

pub use delaunay::{DelaunayCell, SellingS6, delaunay_reduce, selling_s6};
pub use equivalence::{is_supercell, lattices_equivalent};
pub use minimum_image::{
    closest_image, is_highly_skewed, is_inside_unit_cell, minimum_image_brute_force,
    minimum_image_distance, minimum_image_vector, wrap_positions_to_unit_cell, wrap_to_half,
    wrap_to_unit,
};
pub use niggli::{NiggliCell, NiggliForm, NiggliG6, is_niggli_reduced, niggli_g6, niggli_reduce};
pub use supercell::{
    SupercellStrategy, find_supercell_for_min_image_dist, find_supercell_for_min_length,
    find_supercell_for_target_atoms, find_supercell_matrix, perpendicular_distances,
};

/// Tolerance for detecting degenerate lattices (nearly zero perpendicular distance).
const DEGENERATE_LATTICE_TOLERANCE: f64 = 1e-10;

#[cfg(test)]
mod tests;
