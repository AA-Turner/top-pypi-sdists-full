use crate::error::{FerroxError, Result};
use crate::species::SiteOccupancy;
use nalgebra::Vector3;

use super::Structure;
use super::ordering_and_enumeration::{interpolate_lattices_linear, wrap_frac_diff};

impl Structure {
    // === Coordination Analysis ===

    /// Get coordination numbers for all sites using a distance cutoff.
    ///
    /// Counts the number of neighbors within the specified cutoff distance for each site.
    /// Uses periodic boundary conditions.
    ///
    /// # Arguments
    ///
    /// * `cutoff` - Maximum distance (in Angstroms) to consider a site as a neighbor
    ///
    /// # Returns
    ///
    /// A vector of coordination numbers, one for each site in the structure.
    pub fn get_coordination_numbers(&self, cutoff: f64) -> Vec<usize> {
        crate::analysis::coordination::get_coordination_numbers(self, cutoff)
    }

    /// Get coordination number for a single site using a distance cutoff.
    ///
    /// # Arguments
    ///
    /// * `site_idx` - Index of the site to analyze
    /// * `cutoff` - Maximum distance (in Angstroms) to consider a site as a neighbor
    ///
    /// # Returns
    ///
    /// The coordination number for the specified site.
    ///
    /// # Panics
    ///
    /// Panics if `site_idx` is out of bounds.
    pub fn get_coordination_number(&self, site_idx: usize, cutoff: f64) -> usize {
        crate::analysis::coordination::get_coordination_number(self, site_idx, cutoff)
    }

    /// Get the local environment (detailed neighbor information) for a site.
    ///
    /// Returns detailed information about each neighbor including species, distance,
    /// and periodic image offset.
    ///
    /// # Arguments
    ///
    /// * `site_idx` - Index of the site to analyze
    /// * `cutoff` - Maximum distance (in Angstroms) to consider a site as a neighbor
    ///
    /// # Returns
    ///
    /// A vector of `LocalEnvNeighbor` structs describing each neighbor.
    ///
    /// # Panics
    ///
    /// Panics if `site_idx` is out of bounds.
    pub fn get_local_environment(
        &self,
        site_idx: usize,
        cutoff: f64,
    ) -> Vec<crate::analysis::coordination::LocalEnvNeighbor> {
        crate::analysis::coordination::get_local_environment(self, site_idx, cutoff)
    }

    /// Get Voronoi-weighted coordination number for a single site.
    ///
    /// Uses Voronoi tessellation to determine neighbors based on solid angle.
    ///
    /// **Note**: Results are only geometrically correct for orthogonal lattices
    /// (cubic/tetragonal/orthorhombic). Use cutoff-based methods for non-orthogonal cells.
    ///
    /// # Arguments
    ///
    /// * `site_idx` - Index of the site to analyze
    /// * `config` - Optional configuration (min_solid_angle threshold)
    ///
    /// # Returns
    ///
    /// The effective coordination number (can be fractional).
    ///
    /// # Panics
    ///
    /// Panics if `site_idx` is out of bounds.
    #[cfg(not(target_arch = "wasm32"))]
    pub fn get_cn_voronoi(
        &self,
        site_idx: usize,
        config: Option<&crate::analysis::coordination::VoronoiConfig>,
    ) -> f64 {
        crate::analysis::coordination::get_cn_voronoi(self, site_idx, config)
    }

    /// Get Voronoi-weighted coordination numbers for all sites.
    ///
    /// Uses Voronoi tessellation to determine neighbors based on solid angle.
    ///
    /// **Note**: Results are only geometrically correct for orthogonal lattices
    /// (cubic/tetragonal/orthorhombic). Use cutoff-based methods for non-orthogonal cells.
    ///
    /// # Arguments
    ///
    /// * `config` - Optional configuration (min_solid_angle threshold)
    ///
    /// # Returns
    ///
    /// A vector of effective coordination numbers, one for each site.
    #[cfg(not(target_arch = "wasm32"))]
    pub fn get_cn_voronoi_all(
        &self,
        config: Option<&crate::analysis::coordination::VoronoiConfig>,
    ) -> Vec<f64> {
        crate::analysis::coordination::get_cn_voronoi_all(self, config)
    }

    /// Get Voronoi neighbors with their solid angle fractions for a site.
    ///
    /// Returns neighbors sorted by solid angle (largest first).
    ///
    /// **Note**: Results are only geometrically correct for orthogonal lattices
    /// (cubic/tetragonal/orthorhombic). Use cutoff-based methods for non-orthogonal cells.
    ///
    /// # Arguments
    ///
    /// * `site_idx` - Index of the site to analyze
    /// * `config` - Optional configuration (min_solid_angle threshold)
    ///
    /// # Returns
    ///
    /// A vector of tuples `(neighbor_idx, solid_angle_fraction)`.
    #[cfg(not(target_arch = "wasm32"))]
    pub fn get_voronoi_neighbors(
        &self,
        site_idx: usize,
        config: Option<&crate::analysis::coordination::VoronoiConfig>,
    ) -> Vec<(usize, f64)> {
        crate::analysis::coordination::get_voronoi_neighbors(self, site_idx, config)
    }

    // === Structure Interpolation (NEB) ===

    /// Interpolate between this structure and end_structure for NEB calculations.
    ///
    /// Generates `n_images + 1` structures including the start and end structures.
    /// Intermediate structures have linearly interpolated coordinates.
    ///
    /// # Arguments
    ///
    /// * `end` - The end structure (must have same number of sites and species order)
    /// * `n_images` - Number of intermediate images (n_images=0 returns just start)
    /// * `interpolate_lattices` - If true, also interpolate lattice parameters linearly
    /// * `use_pbc` - If true, use minimum image convention for coordinate interpolation
    ///
    /// # Returns
    ///
    /// `Ok(Vec<Structure>)` with n_images + 1 structures, or `Err` if structures are incompatible.
    ///
    /// # Example
    ///
    /// ```ignore
    /// let images = start.interpolate(&end, 5, false, true)?;
    /// assert_eq!(images.len(), 6); // start + 5 intermediates + end overlap
    /// ```
    pub fn interpolate(
        &self,
        end: &Structure,
        n_images: usize,
        interpolate_lattices: bool,
        use_pbc: bool,
    ) -> Result<Vec<Structure>> {
        // Validate compatibility: same number of sites
        if self.num_sites() != end.num_sites() {
            return Err(FerroxError::MatchingError {
                reason: format!(
                    "Cannot interpolate structures with different number of sites: {} vs {}",
                    self.num_sites(),
                    end.num_sites()
                ),
            });
        }

        // Check species match at each site (using dominant species for disordered sites)
        for (idx, (so1, so2)) in self
            .site_occupancies
            .iter()
            .zip(&end.site_occupancies)
            .enumerate()
        {
            if so1.dominant_species().element != so2.dominant_species().element {
                return Err(FerroxError::MatchingError {
                    reason: format!(
                        "Species mismatch at site {}: {:?} vs {:?}",
                        idx,
                        so1.dominant_species().element,
                        so2.dominant_species().element
                    ),
                });
            }
        }

        // Check periodicity matches
        if self.pbc != end.pbc {
            return Err(FerroxError::MatchingError {
                reason: format!(
                    "Cannot interpolate structures with different periodicity: {:?} vs {:?}",
                    self.pbc, end.pbc
                ),
            });
        }

        // Check charge matches
        if (self.charge - end.charge).abs() > 1e-10 {
            return Err(FerroxError::MatchingError {
                reason: format!(
                    "Cannot interpolate structures with different charges: {} vs {}",
                    self.charge, end.charge
                ),
            });
        }

        // Edge case: n_images=0 returns just the start structure
        if n_images == 0 {
            return Ok(vec![self.clone()]);
        }

        let mut images = Vec::with_capacity(n_images + 1);

        for img_idx in 0..=n_images {
            let x = img_idx as f64 / n_images as f64;

            // Interpolate fractional coordinates
            let new_frac_coords: Vec<Vector3<f64>> = self
                .frac_coords
                .iter()
                .zip(&end.frac_coords)
                .map(|(fc_start, fc_end)| {
                    let diff = fc_end - fc_start;
                    let diff = if use_pbc { wrap_frac_diff(diff) } else { diff };
                    fc_start + x * diff
                })
                .collect();

            // Optionally interpolate lattice
            let new_lattice = if interpolate_lattices {
                interpolate_lattices_linear(&self.lattice, &end.lattice, x)
            } else {
                self.lattice.clone()
            };

            images.push(Structure::try_new_full(
                new_lattice,
                self.site_occupancies.clone(),
                new_frac_coords,
                self.pbc,
                self.charge,
                self.properties.clone(),
            )?);
        }

        Ok(images)
    }

    // === Structure Matching Convenience Methods ===

    /// Check if this structure matches another using default matcher settings.
    ///
    /// # Arguments
    ///
    /// * `other` - The structure to compare against
    /// * `anonymous` - If true, allows any species permutation (prototype matching)
    ///
    /// # Returns
    ///
    /// `true` if structures match, `false` otherwise.
    ///
    /// # Example
    ///
    /// ```ignore
    /// let nacl = make_nacl();
    /// let mgo = make_mgo();
    ///
    /// // Exact match (same species)
    /// assert!(nacl.matches(&nacl, false));
    ///
    /// // Anonymous match (same prototype, different species)
    /// assert!(nacl.matches(&mgo, true));
    /// ```
    pub fn matches(&self, other: &Structure, anonymous: bool) -> bool {
        let matcher = crate::analysis::structure_matcher::StructureMatcher::new();
        self.matches_with(other, &matcher, anonymous)
    }

    /// Check if structures match using custom matcher settings.
    ///
    /// # Arguments
    ///
    /// * `other` - The structure to compare against
    /// * `matcher` - Custom `StructureMatcher` with tolerance settings
    /// * `anonymous` - If true, allows any species permutation
    ///
    /// # Returns
    ///
    /// `true` if structures match according to the matcher settings.
    pub fn matches_with(
        &self,
        other: &Structure,
        matcher: &crate::analysis::structure_matcher::StructureMatcher,
        anonymous: bool,
    ) -> bool {
        if anonymous {
            matcher.fit_anonymous(self, other, None)
        } else {
            matcher.fit(self, other)
        }
    }

    // === Structure Sorting ===

    /// Sort sites in place by atomic number (ascending by default).
    ///
    /// Sites with disordered occupancies are sorted by their dominant species
    /// (highest occupancy).
    ///
    /// # Arguments
    ///
    /// * `reverse` - If true, sort in descending order (heaviest first)
    ///
    /// # Returns
    ///
    /// Mutable reference to self for method chaining.
    pub fn sort(&mut self, reverse: bool) -> &mut Self {
        self.sort_by_key(|so| so.dominant_species().element.atomic_number(), reverse)
    }

    /// Sort sites in place by electronegativity (ascending by default).
    ///
    /// Sites with undefined electronegativity (noble gases) are placed last.
    /// Uses dominant species for disordered sites.
    ///
    /// # Arguments
    ///
    /// * `reverse` - If true, sort in descending order (most electronegative first)
    pub fn sort_by_electronegativity(&mut self, reverse: bool) -> &mut Self {
        let mut indices: Vec<usize> = (0..self.num_sites()).collect();
        indices.sort_by(|&a_idx, &b_idx| {
            let en_a = self.site_occupancies[a_idx]
                .dominant_species()
                .element
                .electronegativity();
            let en_b = self.site_occupancies[b_idx]
                .dominant_species()
                .element
                .electronegativity();
            match (en_a, en_b) {
                (Some(a), Some(b)) => a.partial_cmp(&b).unwrap_or(std::cmp::Ordering::Equal),
                (Some(_), None) => std::cmp::Ordering::Less, // Defined before undefined
                (None, Some(_)) => std::cmp::Ordering::Greater,
                (None, None) => std::cmp::Ordering::Equal,
            }
        });

        if reverse {
            indices.reverse();
        }

        self.apply_site_permutation(&indices)
    }

    /// Sort sites in place by a custom key function.
    ///
    /// # Arguments
    ///
    /// * `key` - Function that extracts a sortable key from each SiteOccupancy
    /// * `reverse` - If true, sort in descending order
    pub fn sort_by_key<K, F>(&mut self, key: F, reverse: bool) -> &mut Self
    where
        F: Fn(&SiteOccupancy) -> K,
        K: Ord,
    {
        let mut indices: Vec<usize> = (0..self.num_sites()).collect();
        indices.sort_by_key(|&idx| key(&self.site_occupancies[idx]));

        if reverse {
            indices.reverse();
        }

        self.apply_site_permutation(&indices)
    }

    /// Apply a permutation to reorder sites.
    #[inline]
    fn apply_site_permutation(&mut self, indices: &[usize]) -> &mut Self {
        let new_site_occupancies: Vec<SiteOccupancy> = indices
            .iter()
            .map(|&idx| self.site_occupancies[idx].clone())
            .collect();
        let new_frac_coords: Vec<Vector3<f64>> =
            indices.iter().map(|&idx| self.frac_coords[idx]).collect();

        self.site_occupancies = new_site_occupancies;
        self.frac_coords = new_frac_coords;
        self
    }

    /// Get a sorted copy of the structure by atomic number.
    pub fn get_sorted_structure(&self, reverse: bool) -> Self {
        let mut copy = self.clone();
        copy.sort(reverse);
        copy
    }

    /// Get a copy sorted by electronegativity.
    pub fn get_sorted_by_electronegativity(&self, reverse: bool) -> Self {
        let mut copy = self.clone();
        copy.sort_by_electronegativity(reverse);
        copy
    }
}
