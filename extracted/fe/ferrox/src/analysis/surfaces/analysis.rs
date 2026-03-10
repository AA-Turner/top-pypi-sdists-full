// === Surface Analysis Functions ===

use super::MillerIndex;
use crate::structure::Structure;
use serde::{Deserialize, Serialize};

/// Get indices of surface atoms in a slab structure.
///
/// Surface atoms are identified as those with z-coordinates (in fractional)
/// above a certain threshold, based on the vacuum region.
///
/// # Arguments
///
/// * `slab` - The slab structure
/// * `tolerance` - Tolerance for identifying surface layers in **fractional coordinates**.
///   For example, 0.1 means atoms within 10% of the c-axis length from the top
///   are considered surface atoms. Typical values: 0.05-0.15 depending on slab thickness.
///
/// # Returns
///
/// Indices of atoms at the top surface.
pub fn get_surface_atoms(slab: &Structure, tolerance: f64) -> Vec<usize> {
    if slab.num_sites() == 0 {
        return vec![];
    }

    // Find the maximum z-coordinate
    let max_z = slab
        .frac_coords
        .iter()
        .map(|coord| coord.z)
        .fold(f64::NEG_INFINITY, f64::max);

    // Find atoms within tolerance of the maximum z
    slab.frac_coords
        .iter()
        .enumerate()
        .filter(|(_, coord)| (coord.z - max_z).abs() < tolerance)
        .map(|(idx, _)| idx)
        .collect()
}

/// Calculate the surface area of a slab.
///
/// The surface area is calculated as the cross product of the a and b
/// lattice vectors, giving the area of the periodic unit cell surface.
///
/// # Arguments
///
/// * `slab` - The slab structure
///
/// # Returns
///
/// Surface area in Å².
pub fn surface_area(slab: &Structure) -> f64 {
    let matrix = slab.lattice.matrix();
    let a_vec = matrix.row(0).transpose();
    let b_vec = matrix.row(1).transpose();
    a_vec.cross(&b_vec).norm()
}

/// Calculate surface energy from DFT energies.
///
/// Uses the standard formula:
/// γ = (E_slab - n * E_bulk) / (2 * A)
///
/// where the factor of 2 accounts for the two surfaces of the slab.
///
/// # Arguments
///
/// * `slab_energy` - Total energy of the slab (eV)
/// * `bulk_energy_per_atom` - Energy per atom in the bulk (eV)
/// * `n_atoms` - Number of atoms in the slab
/// * `area` - Surface area (Å²)
///
/// # Returns
///
/// Surface energy in eV/Å².
pub fn calculate_surface_energy(
    slab_energy: f64,
    bulk_energy_per_atom: f64,
    n_atoms: usize,
    area: f64,
) -> f64 {
    if area <= 0.0 {
        return f64::NAN;
    }
    (slab_energy - (n_atoms as f64) * bulk_energy_per_atom) / (2.0 * area)
}

/// Result of a surface energy calculation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SurfaceEnergy {
    /// Miller index of the surface
    pub miller_index: MillerIndex,
    /// Surface energy in eV/Å²
    pub energy_ev_per_a2: f64,
    /// Surface energy in J/m²
    pub energy_j_per_m2: f64,
    /// Surface area used in calculation (Å²)
    pub surface_area: f64,
}

impl SurfaceEnergy {
    /// Create a new surface energy result.
    ///
    /// Automatically converts from eV/Å² to J/m².
    pub fn new(miller_index: MillerIndex, energy_ev_per_a2: f64, surface_area: f64) -> Self {
        // Conversion factor: 1 eV/Å² = 16.02176634 J/m²
        const EV_A2_TO_J_M2: f64 = 16.02176634;
        Self {
            miller_index,
            energy_ev_per_a2,
            energy_j_per_m2: energy_ev_per_a2 * EV_A2_TO_J_M2,
            surface_area,
        }
    }
}
