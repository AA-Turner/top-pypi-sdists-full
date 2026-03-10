use crate::algorithms::EnumConfig;
use crate::error::Result;
use crate::lattice::Lattice;
use crate::transformations::{OrderDisorderedConfig, PartialRemoveConfig};
use nalgebra::Vector3;

use super::Structure;

// === Ordering and Enumeration Methods ===

impl Structure {
    /// Scale structure so fractional occupancies become integral site counts.
    ///
    /// Creates the smallest supercell where fractional occupancies can be represented
    /// as whole numbers of fully-occupied sites. After transformation, all sites have
    /// occupancy 1.0, ready for use with `order_disordered`.
    ///
    /// # Arguments
    ///
    /// * `max_denominator` - Maximum denominator when rationalizing occupancies
    /// * `tolerance` - Tolerance for matching occupancies to fractions
    ///
    /// # Returns
    ///
    /// A new structure with discretized occupancies.
    ///
    /// # Example
    ///
    /// ```ignore
    /// // Structure with 1 site at 0.75 Li, 0.25 vacancy
    /// let discretized = structure.discretize_occupancies(10, 0.01)?;
    /// // Now has 4x supercell with 4 sites, each at 1.0 occupancy
    /// ```
    pub fn discretize_occupancies(&self, max_denominator: u32, tolerance: f64) -> Result<Self> {
        use crate::transformations::{DiscretizeOccupanciesTransform, Transform};
        let transform = DiscretizeOccupanciesTransform::new(max_denominator, tolerance);
        transform.applied(self)
    }

    /// Enumerate all orderings of a disordered structure.
    ///
    /// Takes a structure with disordered sites (multiple species per site) and
    /// enumerates all possible ordered configurations. Structures are optionally
    /// ranked by Ewald energy.
    ///
    /// # Arguments
    ///
    /// * `config` - Configuration options for ordering
    ///
    /// # Returns
    ///
    /// A vector of ordered structures, optionally sorted by energy.
    ///
    /// # Example
    ///
    /// ```ignore
    /// let config = OrderDisorderedConfig {
    ///     max_structures: Some(100),
    ///     sort_by_energy: true,
    ///     ..Default::default()
    /// };
    /// let orderings = disordered.order_disordered(config)?;
    /// for s in orderings {
    ///     println!("Energy: {:?}", s.properties.get("ewald_energy"));
    /// }
    /// ```
    pub fn order_disordered(&self, config: OrderDisorderedConfig) -> Result<Vec<Self>> {
        use crate::transformations::{OrderDisorderedTransform, TransformMany};
        let transform = OrderDisorderedTransform::new(config);
        transform.apply_all(self)
    }

    /// Enumerate all ways to partially remove a species.
    ///
    /// Removes a fraction of a specific species and enumerates all possible
    /// removal patterns, ranked by Ewald energy.
    ///
    /// # Arguments
    ///
    /// * `config` - Configuration specifying species, fraction, and options
    ///
    /// # Returns
    ///
    /// A vector of structures with partial removals, sorted by energy.
    ///
    /// # Example
    ///
    /// ```ignore
    /// let config = PartialRemoveConfig::new(Species::new(Element::Li, Some(1)), 0.5);
    /// let removed = lio2.partial_remove(config)?;
    /// // Each structure has half the Li atoms removed
    /// ```
    pub fn partial_remove(&self, config: PartialRemoveConfig) -> Result<Vec<Self>> {
        use crate::transformations::{PartialRemoveTransform, TransformMany};
        let transform = PartialRemoveTransform::new(config);
        transform.apply_all(self)
    }

    /// Generate all derivative structures (supercells) in size range.
    ///
    /// Enumerates derivative structures from the parent lattice using HNF/SNF
    /// algorithms. This is useful for systematic exploration of supercells
    /// and ordered configurations.
    ///
    /// # Arguments
    ///
    /// * `min_size` - Minimum supercell size (number of formula units)
    /// * `max_size` - Maximum supercell size (number of formula units)
    ///
    /// # Returns
    ///
    /// A vector of derivative structures.
    ///
    /// # Example
    ///
    /// ```ignore
    /// // Generate all supercells with 1-4 formula units
    /// let derivatives = parent.enumerate_derivatives(1, 4)?;
    /// for d in derivatives {
    ///     println!("Volume ratio: {}", d.volume() / parent.volume());
    /// }
    /// ```
    pub fn enumerate_derivatives(&self, min_size: usize, max_size: usize) -> Result<Vec<Self>> {
        use crate::algorithms::EnumerateDerivativesTransform;
        use crate::transformations::TransformMany;
        let config = EnumConfig {
            min_size,
            max_size,
            ..Default::default()
        };
        let transform = EnumerateDerivativesTransform::new(config);
        transform.apply_all(self)
    }
}

// === Random Vector Generation for Perturbation ===

/// Generate a random vector with magnitude uniformly distributed in [min_dist, max_dist].
///
/// Direction is uniformly distributed on the unit sphere using rejection sampling.
pub(super) fn get_random_vector(
    rng: &mut dyn rand::RngCore,
    min_dist: f64,
    max_dist: f64,
) -> Vector3<f64> {
    use rand::Rng;

    loop {
        // Generate point in cube [-1, 1]^3
        let x: f64 = rng.gen_range(-1.0..1.0);
        let y: f64 = rng.gen_range(-1.0..1.0);
        let z: f64 = rng.gen_range(-1.0..1.0);
        let norm_sq = x * x + y * y + z * z;

        // Rejection sampling: accept if inside unit sphere and not at origin
        if norm_sq > 0.01 && norm_sq <= 1.0 {
            let norm = norm_sq.sqrt();
            let magnitude = rng.gen_range(min_dist..=max_dist);
            return Vector3::new(x, y, z) / norm * magnitude;
        }
    }
}

/// Wrap fractional coordinate difference to [-0.5, 0.5) for minimum image convention.
#[inline]
pub(super) fn wrap_frac_diff(diff: Vector3<f64>) -> Vector3<f64> {
    Vector3::new(
        diff[0] - diff[0].round(),
        diff[1] - diff[1].round(),
        diff[2] - diff[2].round(),
    )
}

/// Linear interpolation of lattice parameters (lengths and angles).
///
/// Creates a new lattice with linearly interpolated a, b, c lengths and
/// alpha, beta, gamma angles between the start and end lattices.
pub(super) fn interpolate_lattices_linear(start: &Lattice, end: &Lattice, x: f64) -> Lattice {
    let start_lengths = start.lengths();
    let start_angles = start.angles();
    let end_lengths = end.lengths();
    let end_angles = end.angles();

    let new_lengths = start_lengths + x * (end_lengths - start_lengths);
    let new_angles = start_angles + x * (end_angles - start_angles);

    Lattice::from_parameters(
        new_lengths[0],
        new_lengths[1],
        new_lengths[2],
        new_angles[0],
        new_angles[1],
        new_angles[2],
    )
}

// === Transformation Methods ===
