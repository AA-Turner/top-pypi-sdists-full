use nalgebra::{Matrix3, Vector3};
use std::collections::HashMap;

use super::Structure;
use super::ordering_and_enumeration::get_random_vector;

// === Symmetry Operations ===

/// A crystallographic symmetry operation: rotation + translation.
///
/// Transforms coordinates as: `new = rotation * old + translation`
///
/// In fractional coordinates:
///   `new_frac = rotation @ old_frac + translation`
///
/// In Cartesian coordinates:
///   `new_cart = rotation @ old_cart + translation`
#[derive(Debug, Clone)]
pub struct SymmOp {
    /// 3x3 rotation/rotation-reflection matrix.
    pub rotation: Matrix3<f64>,
    /// Translation vector.
    pub translation: Vector3<f64>,
}

impl SymmOp {
    /// Create a new symmetry operation from rotation matrix and translation vector.
    pub fn new(rotation: Matrix3<f64>, translation: Vector3<f64>) -> Self {
        Self {
            rotation,
            translation,
        }
    }

    /// Identity operation (no transformation).
    pub fn identity() -> Self {
        Self::new(Matrix3::identity(), Vector3::zeros())
    }

    /// Inversion through the origin.
    pub fn inversion() -> Self {
        Self::new(-Matrix3::identity(), Vector3::zeros())
    }

    /// Pure translation (no rotation).
    pub fn translation(vector: Vector3<f64>) -> Self {
        Self::new(Matrix3::identity(), vector)
    }

    /// Rotation around the z-axis by angle (in radians).
    pub fn rotation_z(angle: f64) -> Self {
        let c = angle.cos();
        let s = angle.sin();
        let rotation = Matrix3::new(c, -s, 0.0, s, c, 0.0, 0.0, 0.0, 1.0);
        Self::new(rotation, Vector3::zeros())
    }
}

// Additional Structure methods for symmetry operations
impl Structure {
    /// Apply a symmetry operation to all sites.
    ///
    /// # Arguments
    ///
    /// * `op` - The symmetry operation to apply
    /// * `fractional` - If true, operation is in fractional coordinates; otherwise Cartesian
    ///
    /// # Returns
    ///
    /// Mutable reference to self for method chaining.
    ///
    /// # Example
    ///
    /// ```ignore
    /// let mut s = make_nacl();
    /// // Inversion through origin
    /// s.apply_operation(&SymmOp::inversion(), true);
    /// ```
    pub fn apply_operation(&mut self, op: &SymmOp, fractional: bool) -> &mut Self {
        if fractional {
            // Apply in fractional coordinates directly
            for fc in &mut self.frac_coords {
                *fc = op.rotation * (*fc) + op.translation;
            }
        } else {
            // Convert to Cartesian, apply operation, convert back
            let cart_coords = self.lattice.get_cartesian_coords(&self.frac_coords);
            let new_cart: Vec<Vector3<f64>> = cart_coords
                .iter()
                .map(|c| op.rotation * c + op.translation)
                .collect();
            self.frac_coords = self.lattice.get_fractional_coords(&new_cart);
        }
        self
    }

    /// Apply a symmetry operation and return a new structure.
    ///
    /// This is a non-mutating version of `apply_operation` that returns
    /// a transformed copy while leaving the original unchanged.
    ///
    /// # Arguments
    ///
    /// * `op` - The symmetry operation to apply
    /// * `fractional` - If true, operation is in fractional coordinates; otherwise Cartesian
    pub fn apply_operation_copy(&self, op: &SymmOp, fractional: bool) -> Self {
        let mut copy = self.clone();
        copy.apply_operation(op, fractional);
        copy
    }

    // === Physical Properties ===

    /// Volume of the unit cell in Angstrom^3.
    #[inline]
    pub fn volume(&self) -> f64 {
        self.lattice.volume()
    }

    /// Total mass in atomic mass units (u), accounting for partial occupancies.
    pub fn total_mass(&self) -> f64 {
        self.site_occupancies
            .iter()
            .flat_map(|site_occ| site_occ.species.iter())
            .map(|(sp, occ)| sp.element.atomic_mass() * occ)
            .sum()
    }

    /// Density in g/cm^3, or `None` for non-fully-periodic or zero-volume structures.
    ///
    /// Returns `None` for:
    /// - Molecules (non-periodic systems)
    /// - Slabs/wires (partially periodic) - vacuum makes density misleading
    /// - Zero-volume structures
    ///
    /// Density is only meaningful for fully 3D-periodic bulk materials.
    pub fn density(&self) -> Option<f64> {
        // Density is only meaningful for fully periodic (3D) bulk materials
        // Slabs (2D) and wires (1D) have vacuum that makes density misleading
        if self.pbc != [true, true, true] {
            return None;
        }
        let volume = self.volume();
        if volume <= 0.0 {
            return None;
        }
        // 1 amu = 1.66053906660e-24 g
        // 1 Å = 1e-8 cm, so 1 Å³ = 1e-24 cm³
        // density = (mass_amu * 1.66054e-24 g) / (volume_ang3 * 1e-24 cm³)
        const AMU_TO_G_PER_CM3: f64 = 1.66053906660;
        Some(self.total_mass() * AMU_TO_G_PER_CM3 / volume)
    }

    // === Site Properties ===

    /// Get site properties for a specific site index.
    ///
    /// # Panics
    ///
    /// Panics if `idx` is out of bounds.
    pub fn site_properties(&self, idx: usize) -> &HashMap<String, serde_json::Value> {
        assert!(
            idx < self.num_sites(),
            "Site index {} out of bounds (num_sites={})",
            idx,
            self.num_sites()
        );
        &self.site_occupancies[idx].properties
    }

    /// Get mutable site properties for a specific site index.
    ///
    /// # Panics
    ///
    /// Panics if `idx` is out of bounds.
    pub fn site_properties_mut(&mut self, idx: usize) -> &mut HashMap<String, serde_json::Value> {
        assert!(
            idx < self.num_sites(),
            "Site index {} out of bounds (num_sites={})",
            idx,
            self.num_sites()
        );
        &mut self.site_occupancies[idx].properties
    }

    /// Set a site property.
    ///
    /// # Panics
    ///
    /// Panics if `idx` is out of bounds.
    pub fn set_site_property(
        &mut self,
        idx: usize,
        key: &str,
        value: serde_json::Value,
    ) -> &mut Self {
        assert!(
            idx < self.num_sites(),
            "Site index {} out of bounds (num_sites={})",
            idx,
            self.num_sites()
        );
        self.site_occupancies[idx]
            .properties
            .insert(key.to_string(), value);
        self
    }

    /// Get all site properties as a vector (parallel to frac_coords).
    pub fn all_site_properties(&self) -> Vec<&HashMap<String, serde_json::Value>> {
        self.site_occupancies
            .iter()
            .map(|so| &so.properties)
            .collect()
    }

    /// Get label for a specific site.
    ///
    /// Returns the explicit label if set in site properties, otherwise falls back
    /// to `species_string()` (e.g., "Fe" or "Fe:0.5, Co:0.5").
    ///
    /// # Panics
    ///
    /// Panics if `idx` is out of bounds.
    pub fn site_label(&self, idx: usize) -> String {
        assert!(
            idx < self.num_sites(),
            "Site index {} out of bounds (num_sites={})",
            idx,
            self.num_sites()
        );
        self.site_occupancies[idx]
            .properties
            .get("label")
            .and_then(|v| v.as_str())
            .map(String::from)
            .unwrap_or_else(|| self.site_occupancies[idx].species_string())
    }

    /// Set label for a specific site.
    ///
    /// The label is stored in the site's properties as `"label"`.
    /// Returns self for method chaining.
    ///
    /// # Panics
    ///
    /// Panics if `idx` is out of bounds.
    pub fn set_site_label(&mut self, idx: usize, label: &str) -> &mut Self {
        assert!(
            idx < self.num_sites(),
            "Site index {} out of bounds (num_sites={})",
            idx,
            self.num_sites()
        );
        self.site_occupancies[idx]
            .properties
            .insert("label".to_string(), serde_json::json!(label));
        self
    }

    /// Get labels for all sites.
    ///
    /// Returns a vector of labels, one per site. Sites without explicit labels
    /// return their `species_string()`.
    pub fn site_labels(&self) -> Vec<String> {
        (0..self.num_sites())
            .map(|idx| self.site_label(idx))
            .collect()
    }

    /// Normalize all species symbols in the structure.
    ///
    /// Since structures are already normalized during parsing (element symbols
    /// are converted to Element enum variants), this is a no-op. Provided for
    /// API symmetry with pymatgen.
    ///
    /// Returns mutable reference to self for method chaining.
    pub fn normalize(&mut self) -> &mut Self {
        // Already normalized - Element enum guarantees valid symbols
        self
    }

    // === Site Manipulation ===

    /// Translate specific sites by a vector.
    ///
    /// # Arguments
    /// * `indices` - Site indices to translate
    /// * `vector` - Translation vector
    /// * `frac_coords` - If true, vector is in fractional coords; otherwise Cartesian
    ///
    /// # Panics
    /// Panics if any index is out of bounds.
    pub fn translate_sites(
        &mut self,
        indices: &[usize],
        vector: Vector3<f64>,
        frac_coords: bool,
    ) -> &mut Self {
        let frac_vector = if frac_coords {
            vector
        } else {
            self.lattice.get_fractional_coords(&[vector])[0]
        };
        for &idx in indices {
            assert!(
                idx < self.frac_coords.len(),
                "Index {idx} out of bounds (num_sites = {})",
                self.num_sites()
            );
            self.frac_coords[idx] += frac_vector;
        }
        self
    }

    /// Perturb all sites by random vectors with magnitude up to `distance` Angstroms.
    ///
    /// # Arguments
    /// * `distance` - Maximum perturbation distance in Angstroms
    /// * `min_distance` - Minimum perturbation distance (default 0)
    /// * `seed` - Optional seed for reproducibility
    ///
    /// # Panics
    /// Panics if distance < min_distance.
    pub fn perturb(
        &mut self,
        distance: f64,
        min_distance: Option<f64>,
        seed: Option<u64>,
    ) -> &mut Self {
        use rand::SeedableRng;
        use rand::rngs::StdRng;

        let min_dist = min_distance.unwrap_or(0.0);
        assert!(
            distance >= min_dist,
            "distance ({distance}) must be >= min_distance ({min_dist})"
        );

        // Use seeded RNG for reproducibility, or thread RNG for randomness
        let mut seeded_rng;
        let mut thread_rng;
        let rng: &mut dyn rand::RngCore = match seed {
            Some(s) => {
                seeded_rng = StdRng::seed_from_u64(s);
                &mut seeded_rng
            }
            None => {
                thread_rng = rand::thread_rng();
                &mut thread_rng
            }
        };

        for idx in 0..self.num_sites() {
            let rand_vec = get_random_vector(rng, min_dist, distance);
            self.translate_sites(&[idx], rand_vec, false);
        }
        self
    }
}
