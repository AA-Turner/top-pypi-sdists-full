//! Crystallographic lattice operations.
//!
//! This module provides the [`Lattice`] struct for representing 3D periodic lattices,
//! along with constructors for standard cell types, geometric queries, coordinate
//! transforms, and lattice reductions (Niggli, LLL).
//!
//! ```
//! use ferrox::lattice::Lattice;
//!
//! let lattice = Lattice::cubic(4.0);
//! assert!((lattice.volume() - 64.0).abs() < 1e-10);
//! assert!(lattice.lengths().iter().all(|len| (len - 4.0).abs() < 1e-10));
//! ```

use nalgebra::Matrix3;
use serde::{Deserialize, Serialize};

/// A crystallographic lattice defined by a 3x3 matrix.
///
/// The lattice matrix has lattice vectors as rows:
/// ```text
/// | a1x  a1y  a1z |
/// | a2x  a2y  a2z |
/// | a3x  a3y  a3z |
/// ```
///
/// # Examples
///
/// ```
/// use ferrox::lattice::Lattice;
///
/// // Create a cubic lattice with a = 4.0 Å
/// let lattice = Lattice::cubic(4.0);
/// assert!((lattice.volume() - 64.0).abs() < 1e-10);
/// ```
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Lattice {
    /// The 3x3 lattice matrix (rows are lattice vectors).
    matrix: Matrix3<f64>,
    /// Periodic boundary conditions along each axis.
    pub pbc: [bool; 3],
}

#[path = "impl/core_impl.rs"]
mod core_impl;

#[path = "impl/reductions_impl.rs"]
mod reductions_impl;

#[path = "impl/mappings_impl.rs"]
mod mappings_impl;

#[cfg(test)]
mod tests;
