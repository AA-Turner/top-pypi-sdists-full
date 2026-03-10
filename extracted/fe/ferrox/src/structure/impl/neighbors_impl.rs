use nalgebra::Vector3;

use super::Structure;

impl Structure {
    // === Neighbor Finding Methods ===

    /// Get neighbor list as arrays: (center_indices, neighbor_indices, offset_vectors, distances).
    ///
    /// Finds all atom pairs within cutoff radius using periodic boundary conditions.
    ///
    /// # Arguments
    ///
    /// * `cutoff` - Cutoff radius in Angstroms
    /// * `numerical_tol` - Tolerance for distance comparisons (typically 1e-8)
    /// * `exclude_self` - If true, exclude self-pairs (distance ~0)
    ///
    /// # Returns
    ///
    /// Tuple of (center_indices, neighbor_indices, image_offsets, distances)
    ///
    /// # Performance
    ///
    /// Uses the shared NeighborList implementation (cell-list for larger systems,
    /// brute-force fallback based on `NeighborListConfig::cell_list_threshold`).
    pub fn get_neighbor_list(
        &self,
        cutoff: f64,
        numerical_tol: f64,
        exclude_self: bool,
    ) -> (Vec<usize>, Vec<usize>, Vec<[i32; 3]>, Vec<f64>) {
        use crate::neighbors::{NeighborListConfig, build_neighbor_list};

        // Validate inputs to avoid silent NaN/inf behavior
        assert!(
            cutoff.is_finite(),
            "get_neighbor_list: cutoff must be finite, got {cutoff}"
        );
        assert!(
            numerical_tol.is_finite() && numerical_tol >= 0.0,
            "get_neighbor_list: numerical_tol must be finite and >= 0, got {numerical_tol}"
        );

        if self.num_sites() == 0 || cutoff <= 0.0 {
            return (vec![], vec![], vec![], vec![]);
        }

        let config = NeighborListConfig {
            cutoff,
            self_interaction: !exclude_self,
            numerical_tol,
            ..Default::default()
        };

        let nl = build_neighbor_list(self, &config);

        (
            nl.center_indices,
            nl.neighbor_indices,
            nl.images,
            nl.distances,
        )
    }

    /// Get all neighbors for each site within cutoff radius.
    pub fn get_all_neighbors(&self, cutoff: f64) -> Vec<Vec<(usize, f64, [i32; 3])>> {
        let num_sites = self.num_sites();
        let mut result = vec![Vec::new(); num_sites];

        let (centers, neighbors, images, dists) = self.get_neighbor_list(cutoff, 1e-8, true);

        for (kdx, &center) in centers.iter().enumerate() {
            result[center].push((neighbors[kdx], dists[kdx], images[kdx]));
        }

        result
    }

    /// Get the distance between sites `i` and `j` using minimum image convention.
    ///
    /// # Panics
    ///
    /// Panics if `i` or `j` is out of bounds.
    #[inline]
    pub fn get_distance(&self, i: usize, j: usize) -> f64 {
        self.get_distance_and_image(i, j).0
    }

    /// Get distance and periodic image between sites `i` and `j`.
    ///
    /// Returns `(distance, image)` where `image` is the lattice translation `[da, db, dc]`
    /// that gives the shortest distance. For example, `[1, 0, 0]` means the shortest
    /// path goes through the +a periodic boundary.
    ///
    /// # Panics
    ///
    /// Panics if `i` or `j` is out of bounds.
    pub fn get_distance_and_image(&self, i: usize, j: usize) -> (f64, [i32; 3]) {
        assert!(
            i < self.num_sites(),
            "Index i={} out of bounds (num_sites={})",
            i,
            self.num_sites()
        );
        assert!(
            j < self.num_sites(),
            "Index j={} out of bounds (num_sites={})",
            j,
            self.num_sites()
        );

        let fcoords_i = vec![self.frac_coords[i]];
        let fcoords_j = vec![self.frac_coords[j]];
        let (_, d2, images) =
            crate::pbc::pbc_shortest_vectors(&self.lattice, &fcoords_i, &fcoords_j, None, None);
        (d2[0][0].sqrt(), images[0][0])
    }

    /// Get distance to a specific periodic image of site `j`.
    ///
    /// `jimage` specifies the lattice translation, e.g., `[1, 0, 0]` means the image
    /// of site `j` shifted by +a lattice vector. Coordinates are wrapped to [0, 1)
    /// only along periodic axes, consistent with `pbc_shortest_vectors`.
    ///
    /// # Panics
    ///
    /// Panics if `i` or `j` is out of bounds.
    pub fn get_distance_with_image(&self, i: usize, j: usize, jimage: [i32; 3]) -> f64 {
        assert!(
            i < self.num_sites(),
            "Index i={} out of bounds (num_sites={})",
            i,
            self.num_sites()
        );
        assert!(
            j < self.num_sites(),
            "Index j={} out of bounds (num_sites={})",
            j,
            self.num_sites()
        );

        // Wrap coordinates only along periodic axes for consistency with pbc_shortest_vectors
        let pbc = self.lattice.pbc;
        let frac_i = crate::pbc::wrap_frac_coords_pbc(&self.frac_coords[i], pbc);
        let frac_j = crate::pbc::wrap_frac_coords_pbc(&self.frac_coords[j], pbc);

        let cart_i = self.lattice.get_cartesian_coords(&[frac_i])[0];
        let frac_j_shifted = frac_j + Vector3::from(jimage.map(|val| val as f64));
        let cart_j = self.lattice.get_cartesian_coords(&[frac_j_shifted])[0];
        (cart_j - cart_i).norm()
    }

    /// Get the full distance matrix between all sites under PBC.
    pub fn distance_matrix(&self) -> Vec<Vec<f64>> {
        let num_sites = self.num_sites();
        if num_sites == 0 {
            return vec![];
        }

        let (_, d2, _) = crate::pbc::pbc_shortest_vectors(
            &self.lattice,
            &self.frac_coords,
            &self.frac_coords,
            None,
            None,
        );

        d2.into_iter()
            .map(|row| row.into_iter().map(|dist_sq| dist_sq.sqrt()).collect())
            .collect()
    }

    /// Get Cartesian distance from a site to an arbitrary point.
    ///
    /// This is a simple Euclidean distance, not using periodic boundary conditions.
    /// For PBC-aware distances between sites, use `get_distance()`.
    ///
    /// # Arguments
    ///
    /// * `idx` - Site index
    /// * `point` - Cartesian coordinates of the point
    ///
    /// # Panics
    ///
    /// Panics if `idx` is out of bounds.
    pub fn distance_from_point(&self, idx: usize, point: Vector3<f64>) -> f64 {
        assert!(
            idx < self.num_sites(),
            "Site index {} out of bounds (num_sites={})",
            idx,
            self.num_sites()
        );
        let cart = self.lattice.get_cartesian_coords(&[self.frac_coords[idx]])[0];
        (cart - point).norm()
    }

    /// Check if sites `i` and `j` are periodic images of each other.
    ///
    /// Two sites are periodic images if they have the same species (using dominant
    /// species for disordered sites) and their fractional coordinates differ by
    /// integers within the specified tolerance.
    ///
    /// # Arguments
    ///
    /// * `i` - First site index
    /// * `j` - Second site index
    /// * `tolerance` - Tolerance for coordinate comparison (typically 1e-8)
    ///
    /// # Panics
    ///
    /// Panics if `i` or `j` is out of bounds.
    pub fn is_periodic_image(&self, i: usize, j: usize, tolerance: f64) -> bool {
        assert!(
            i < self.num_sites(),
            "Index i={} out of bounds (num_sites={})",
            i,
            self.num_sites()
        );
        assert!(
            j < self.num_sites(),
            "Index j={} out of bounds (num_sites={})",
            j,
            self.num_sites()
        );

        // Check species match (using dominant species for disordered sites)
        if self.site_occupancies[i].dominant_species()
            != self.site_occupancies[j].dominant_species()
        {
            return false;
        }

        // Check coordinates differ by integers within tolerance
        let diff = self.frac_coords[i] - self.frac_coords[j];
        for kdx in 0..3 {
            if (diff[kdx] - diff[kdx].round()).abs() > tolerance {
                return false;
            }
        }
        true
    }
}
