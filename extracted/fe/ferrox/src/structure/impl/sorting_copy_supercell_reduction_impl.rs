use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use nalgebra::{Matrix3, Vector3};
use std::collections::HashMap;

use super::supercell_helpers::lattice_points_in_supercell;
use super::{ReductionAlgo, Structure};

impl Structure {
    // === Copy and Sanitization ===

    /// Create a copy, optionally sanitized.
    ///
    /// Sanitization applies these steps in order:
    /// 1. LLL lattice reduction (produces nearly orthogonal basis)
    /// 2. Sort sites by electronegativity
    /// 3. Wrap fractional coordinates to [0, 1)
    ///
    /// # Arguments
    ///
    /// * `sanitize` - If true, apply sanitization steps
    pub fn copy(&self, sanitize: bool) -> Self {
        if !sanitize {
            return self.clone();
        }

        // 1. Get LLL-reduced structure (or clone if reduction fails)
        let mut result = self
            .get_reduced_structure(ReductionAlgo::LLL)
            .unwrap_or_else(|err| {
                tracing::warn!("LLL reduction failed during sanitization: {err}");
                self.clone()
            });

        // 2. Sort by electronegativity
        result.sort_by_electronegativity(false);

        // 3. Wrap coords to [0, 1)
        result.wrap_to_unit_cell();

        result
    }

    /// Create a copy with updated properties.
    ///
    /// Existing properties are preserved; new ones are added or overwritten.
    pub fn copy_with_properties(&self, properties: HashMap<String, serde_json::Value>) -> Self {
        let mut result = self.clone();
        result.properties.extend(properties);
        result
    }

    /// Wrap fractional coordinates to [0, 1) along periodic axes.
    ///
    /// Only coordinates along periodic dimensions (where `pbc[axis] == true`)
    /// are wrapped. Non-periodic axes retain their original values.
    ///
    /// # Returns
    ///
    /// Mutable reference to self for method chaining.
    pub fn wrap_to_unit_cell(&mut self) -> &mut Self {
        for fc in &mut self.frac_coords {
            *fc = crate::pbc::wrap_frac_coords_pbc(fc, self.pbc);
        }
        self
    }

    // === Supercell Methods ===

    /// Create a supercell from a 3x3 integer scaling matrix.
    ///
    /// The new lattice vectors are: new_lattice = scaling_matrix * old_lattice.
    /// Sites are replicated for all lattice points within the supercell.
    ///
    /// # Arguments
    ///
    /// * `scaling_matrix` - 3x3 integer matrix defining the supercell transformation
    ///
    /// # Returns
    ///
    /// `Ok(Structure)` with the supercell, or `Err` if the scaling matrix has zero determinant.
    pub fn make_supercell(&self, scaling_matrix: [[i32; 3]; 3]) -> Result<Self> {
        // Convert to nalgebra Matrix3<f64>
        let scale = Matrix3::new(
            scaling_matrix[0][0] as f64,
            scaling_matrix[0][1] as f64,
            scaling_matrix[0][2] as f64,
            scaling_matrix[1][0] as f64,
            scaling_matrix[1][1] as f64,
            scaling_matrix[1][2] as f64,
            scaling_matrix[2][0] as f64,
            scaling_matrix[2][1] as f64,
            scaling_matrix[2][2] as f64,
        );

        // Check determinant (should be a non-zero integer)
        let det = scale.determinant();
        if det.abs() < 0.5 {
            return Err(FerroxError::InvalidLattice {
                reason: "Supercell scaling matrix has zero determinant".to_string(),
            });
        }
        let n_cells = det.abs().round() as usize;

        // Compute new lattice matrix: new_matrix = scale * old_matrix
        let new_matrix = scale * self.lattice.matrix();
        let mut new_lattice = Lattice::new(new_matrix);
        new_lattice.pbc = self.lattice.pbc;

        // Compute inverse for transforming fractional coordinates
        let inv_scale = scale
            .try_inverse()
            .ok_or_else(|| FerroxError::InvalidLattice {
                reason: "Cannot invert scaling matrix".to_string(),
            })?;

        // Generate all lattice points in the supercell
        let lattice_points = lattice_points_in_supercell(&scaling_matrix);

        // Create new sites
        let mut new_site_occupancies = Vec::with_capacity(self.num_sites() * n_cells);
        let mut new_frac_coords = Vec::with_capacity(self.num_sites() * n_cells);

        for (orig_idx, (site_occ, frac)) in self
            .site_occupancies
            .iter()
            .zip(&self.frac_coords)
            .enumerate()
        {
            for lattice_pt in &lattice_points {
                // Shift by lattice point, then transform to new fractional coords
                let shifted = frac + lattice_pt;
                let new_frac = inv_scale * shifted;

                // Copy site occupancy with orig_site_idx for tracking
                // Only set if not already present (preserves chain for nested supercells)
                let mut new_site_occ = site_occ.clone();
                new_site_occ
                    .properties
                    .entry("orig_site_idx".to_string())
                    .or_insert_with(|| serde_json::json!(orig_idx));

                new_site_occupancies.push(new_site_occ);
                new_frac_coords.push(new_frac);
            }
        }

        Structure::try_new_full(
            new_lattice,
            new_site_occupancies,
            new_frac_coords,
            self.pbc,
            self.charge,
            self.properties.clone(),
        )
    }

    /// Create a diagonal supercell (nx x ny x nz).
    ///
    /// This is a convenience method for the common case of uniform scaling
    /// along each axis without shearing.
    ///
    /// # Panics
    ///
    /// Panics if any scaling factor is not positive.
    pub fn make_supercell_diag(&self, ns: [i32; 3]) -> Self {
        assert!(
            ns.iter().all(|&n| n > 0),
            "Supercell scaling factors must be positive, got {:?}",
            ns
        );
        self.make_supercell([[ns[0], 0, 0], [0, ns[1], 0], [0, 0, ns[2]]])
            .expect("Diagonal supercell matrix cannot have zero determinant")
    }

    // === Lattice Reduction Methods ===

    /// Get structure with reduced lattice.
    ///
    /// Atomic positions are preserved in Cartesian space; only the lattice
    /// basis changes. Fractional coordinates are wrapped to [0, 1).
    ///
    /// # Arguments
    ///
    /// * `algo` - Which reduction algorithm to use (Niggli or LLL)
    pub fn get_reduced_structure(&self, algo: ReductionAlgo) -> Result<Self> {
        self.get_reduced_structure_with_params(algo, 1e-5, 0.75)
    }

    /// Get reduced structure with custom parameters.
    ///
    /// # Arguments
    ///
    /// * `algo` - Reduction algorithm (Niggli or LLL)
    /// * `niggli_tol` - Tolerance for Niggli reduction (ignored if LLL)
    /// * `lll_delta` - Delta parameter for LLL reduction (ignored if Niggli)
    ///
    /// # Errors
    ///
    /// Returns an error if the structure is not fully periodic (pbc != [true, true, true]).
    /// Lattice reduction can mix axes and alter vacuum layers in slabs/wires, so it's
    /// only safe for fully 3D-periodic bulk structures.
    pub fn get_reduced_structure_with_params(
        &self,
        algo: ReductionAlgo,
        niggli_tol: f64,
        lll_delta: f64,
    ) -> Result<Self> {
        if self.pbc != [true, true, true] {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "Cannot reduce lattice unless structure is fully periodic (pbc must be [true, true, true])".to_string(),
            });
        }
        // Get reduced lattice
        let reduced_lattice = match algo {
            ReductionAlgo::Niggli => self.lattice.get_niggli_reduced(niggli_tol)?,
            ReductionAlgo::LLL => self.lattice.get_lll_reduced(lll_delta),
        };

        // Convert current fractional coords to Cartesian
        let cart_coords = self.lattice.get_cartesian_coords(&self.frac_coords);

        // Convert Cartesian to new fractional coords and wrap periodic axes to [0, 1)
        let new_frac_coords: Vec<Vector3<f64>> = reduced_lattice
            .get_fractional_coords(&cart_coords)
            .into_iter()
            .map(|fc| crate::pbc::wrap_frac_coords_pbc(&fc, self.pbc))
            .collect();

        Structure::try_new_full(
            reduced_lattice,
            self.site_occupancies.clone(),
            new_frac_coords,
            self.pbc,
            self.charge,
            self.properties.clone(),
        )
    }
}
