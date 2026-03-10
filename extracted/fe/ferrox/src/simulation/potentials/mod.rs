//! Classical interatomic potentials.
//!
//! This module provides native Rust implementations of classical force fields
//! for use in molecular dynamics and geometry optimization.
//!
//! Features:
//! - Per-element-pair parameters via `PairPotential<P>`
//! - Optional virial stress tensor calculation
//! - Lennard-Jones, Morse, Soft Sphere, and Harmonic potentials

mod common_helpers;
mod common_types;
mod harmonic;
mod lennard_jones;
mod morse;
mod soft_sphere;

pub use common_helpers::{PairInteraction, compute_pair_potential_generic, minimum_image};
pub use common_types::{PairPotential, PotentialResult};
pub use harmonic::{HarmonicBond, compute_harmonic_bonds};
pub use lennard_jones::{
    LJParams, LennardJonesParams, LennardJonesResult, compute_lennard_jones,
    compute_lennard_jones_forces, compute_lj_full, compute_lj_pair,
};
pub use morse::{MorseParams, compute_morse, compute_morse_simple};
pub use soft_sphere::{SoftSphereParams, compute_soft_sphere, compute_soft_sphere_simple};

#[cfg(test)]
mod tests;
