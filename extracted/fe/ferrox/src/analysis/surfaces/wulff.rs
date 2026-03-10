// === Wulff Construction ===

use super::MillerIndex;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use nalgebra::Vector3;
use serde::{Deserialize, Serialize};
use std::f64::consts::PI;

/// A facet on a Wulff shape (equilibrium crystal shape).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WulffFacet {
    /// Miller index of this facet
    pub miller_index: MillerIndex,
    /// Surface energy of this facet (J/m²)
    pub surface_energy: f64,
    /// Normal vector to the facet (unit vector)
    pub normal: Vector3<f64>,
    /// Distance from center to facet (proportional to surface energy)
    pub distance_from_center: f64,
    /// Fractional area of total surface (approximate).
    /// Note: This is a simplified calculation based on solid angle coverage.
    /// In a true Wulff construction, high-energy facets may be cut off entirely
    /// by lower-energy facets and should have zero area.
    pub area_fraction: f64,
}

impl WulffFacet {
    /// Create a new Wulff facet.
    pub fn new(
        miller_index: MillerIndex,
        surface_energy: f64,
        normal: Vector3<f64>,
        distance_from_center: f64,
        area_fraction: f64,
    ) -> Self {
        Self {
            miller_index,
            surface_energy,
            normal,
            distance_from_center,
            area_fraction,
        }
    }
}

/// Result of Wulff construction - the equilibrium crystal shape.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WulffShape {
    /// Facets making up the crystal shape
    pub facets: Vec<WulffFacet>,
    /// Vertices of the Wulff polyhedron
    pub vertices: Vec<Vector3<f64>>,
    /// Total surface area (relative units)
    pub total_surface_area: f64,
    /// Volume enclosed (relative units)
    pub volume: f64,
    /// Sphericity (1.0 = perfect sphere)
    pub sphericity: f64,
}

impl WulffShape {
    /// Create a new Wulff shape.
    pub fn new(
        facets: Vec<WulffFacet>,
        vertices: Vec<Vector3<f64>>,
        total_surface_area: f64,
        volume: f64,
    ) -> Self {
        // Sphericity = (π^(1/3) * (6V)^(2/3)) / A
        // For a sphere, sphericity = 1
        let sphericity = if total_surface_area > 0.0 && volume > 0.0 {
            PI.powf(1.0 / 3.0) * (6.0 * volume).powf(2.0 / 3.0) / total_surface_area
        } else {
            0.0
        };

        Self {
            facets,
            vertices,
            total_surface_area,
            volume,
            sphericity,
        }
    }
}

/// Convert Miller index to surface normal vector in Cartesian coordinates.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `hkl` - Miller index as [h, k, l]
///
/// # Returns
///
/// Unit normal vector in Cartesian coordinates.
///
/// # Note
///
/// Returns `[0, 0, 1]` for degenerate cases (e.g., singular lattice or
/// reciprocal vector with near-zero norm). Callers should validate that
/// the input lattice is non-singular.
pub fn miller_to_normal(lattice: &Lattice, hkl: [i32; 3]) -> Vector3<f64> {
    let inv_t = lattice.inv_matrix().transpose();
    let hkl_vec = Vector3::new(hkl[0] as f64, hkl[1] as f64, hkl[2] as f64);
    let normal = inv_t * hkl_vec;
    let norm = normal.norm();
    if norm > 1e-10 {
        normal / norm
    } else {
        Vector3::new(0.0, 0.0, 1.0)
    }
}

/// Calculate the d-spacing for a Miller plane.
///
/// The d-spacing is the perpendicular distance between parallel planes
/// in the crystal lattice.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `hkl` - Miller index as [h, k, l]
///
/// # Returns
///
/// d-spacing in Ångströms.
///
/// # Errors
///
/// Returns an error if hkl is [0, 0, 0].
pub fn d_spacing(lattice: &Lattice, hkl: [i32; 3]) -> Result<f64> {
    if hkl == [0, 0, 0] {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: "Miller indices cannot all be zero".to_string(),
        });
    }

    // d = 1 / |G| where G = h*b1 + k*b2 + l*b3 (reciprocal lattice vector without 2π)
    let inv_t = lattice.inv_matrix().transpose();
    let hkl_vec = Vector3::new(hkl[0] as f64, hkl[1] as f64, hkl[2] as f64);
    let g_vec = inv_t * hkl_vec;
    Ok(1.0 / g_vec.norm())
}

/// Compute the Wulff shape (equilibrium crystal shape) from surface energies.
///
/// The Wulff construction determines the equilibrium shape of a crystal
/// by minimizing total surface energy at fixed volume.
///
/// **Note**: This is a simplified implementation that:
/// - Does not compute actual polyhedron vertices (returns empty `vertices`)
/// - Uses spherical approximation for volume/area estimates
/// - Area fractions are approximate based on solid angle coverage
///
/// For precise Wulff geometry, consider using a dedicated convex hull library.
///
/// # Arguments
///
/// * `lattice` - The crystal lattice
/// * `surface_energies` - Vector of (Miller index, surface energy) pairs
///
/// # Returns
///
/// A WulffShape describing the equilibrium crystal.
pub fn compute_wulff_shape(
    lattice: &Lattice,
    surface_energies: &[(MillerIndex, f64)],
) -> Result<WulffShape> {
    if surface_energies.is_empty() {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: "Need at least one surface energy".to_string(),
        });
    }

    // Create facets from surface energies
    let mut facets: Vec<WulffFacet> = Vec::new();

    // Find minimum surface energy for normalization
    let min_energy = surface_energies
        .iter()
        .map(|(_, energy)| *energy)
        .filter(|e| e.is_finite() && *e > 0.0)
        .fold(f64::INFINITY, f64::min);

    if !min_energy.is_finite() || min_energy <= 0.0 {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: "All surface energies must be positive".to_string(),
        });
    }

    for (miller, energy) in surface_energies {
        if !energy.is_finite() || *energy <= 0.0 {
            continue;
        }

        let normal = miller_to_normal(lattice, miller.to_array());
        let distance = energy / min_energy; // Normalized distance

        // Add facet for this Miller index
        facets.push(WulffFacet::new(*miller, *energy, normal, distance, 0.0));

        // Also add the opposite facet (negative Miller index)
        let neg_miller = MillerIndex::new(-miller.h, -miller.k, -miller.l);
        let neg_normal = -normal;
        facets.push(WulffFacet::new(
            neg_miller, *energy, neg_normal, distance, 0.0,
        ));
    }

    // Simplified Wulff construction - compute approximate area fractions
    // based on solid angle coverage
    let total_solid_angle: f64 = facets
        .iter()
        .map(|f| 1.0 / f.distance_from_center.powi(2))
        .sum();

    for facet in &mut facets {
        facet.area_fraction = (1.0 / facet.distance_from_center.powi(2)) / total_solid_angle;
    }

    // Compute approximate volume and surface area (simplified)
    // For a Wulff polyhedron, these depend on the geometry
    let _total_area: f64 = facets.iter().map(|f| f.area_fraction).sum();
    let avg_distance: f64 = facets
        .iter()
        .map(|f| f.distance_from_center * f.area_fraction)
        .sum();
    let volume = (4.0 / 3.0) * PI * avg_distance.powi(3);
    let area = 4.0 * PI * avg_distance.powi(2);

    Ok(WulffShape::new(facets, vec![], area, volume))
}
