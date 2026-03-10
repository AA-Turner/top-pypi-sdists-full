use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use nalgebra::{Matrix3, Vector3};
use std::collections::{HashMap, HashSet};

use super::Structure;

// === Transformation Methods ===

impl Structure {
    /// Rotate the structure around an arbitrary axis by a given angle.
    ///
    /// Uses Rodrigues' rotation formula. Both the lattice and atomic positions
    /// are rotated together, so fractional coordinates remain unchanged.
    ///
    /// # Arguments
    /// * `axis` - Rotation axis (will be normalized)
    /// * `angle` - Rotation angle in radians
    ///
    /// # Errors
    /// Returns an error if the rotation axis has zero length.
    ///
    /// # Example
    /// ```rust,ignore
    /// use nalgebra::Vector3;
    /// use std::f64::consts::FRAC_PI_2;
    ///
    /// let rotated = structure.rotate(Vector3::z(), FRAC_PI_2)?;
    /// ```
    pub fn rotate(&self, axis: Vector3<f64>, angle: f64) -> Result<Self> {
        // Normalize axis, error if zero-length
        let axis = axis
            .try_normalize(f64::EPSILON)
            .ok_or_else(|| FerroxError::TransformError {
                reason: "rotation axis has zero length".to_string(),
            })?;

        // Rodrigues' rotation formula
        let cos_a = angle.cos();
        let sin_a = angle.sin();
        let one_minus_cos = 1.0 - cos_a;
        let (ax, ay, az) = (axis.x, axis.y, axis.z);

        let rot = Matrix3::new(
            one_minus_cos * ax * ax + cos_a,
            one_minus_cos * ax * ay - sin_a * az,
            one_minus_cos * ax * az + sin_a * ay,
            one_minus_cos * ax * ay + sin_a * az,
            one_minus_cos * ay * ay + cos_a,
            one_minus_cos * ay * az - sin_a * ax,
            one_minus_cos * ax * az - sin_a * ay,
            one_minus_cos * ay * az + sin_a * ax,
            one_minus_cos * az * az + cos_a,
        );

        // Rotate lattice vectors: L_new = R * L_old
        let new_matrix = rot * self.lattice.matrix();
        let new_lattice = Lattice::from_matrix_with_pbc(new_matrix, self.lattice.pbc);

        // Fractional coordinates remain unchanged for rigid rotation
        let mut result = self.clone();
        result.lattice = new_lattice;
        Ok(result)
    }

    /// Substitute one species for another throughout the structure.
    ///
    /// All occurrences of `from` species are replaced with `to` species.
    ///
    /// # Arguments
    /// * `from` - The species to replace
    /// * `to` - The replacement species
    ///
    /// # Example
    /// ```rust,ignore
    /// use ferrox::species::Species;
    /// use ferrox::element::Element;
    ///
    /// let substituted = structure.substitute(
    ///     Species::neutral(Element::Fe),
    ///     Species::neutral(Element::Co),
    /// )?;
    /// ```
    pub fn substitute(&self, from: Species, to: Species) -> Result<Self> {
        let mut result = self.clone();
        for site_occ in &mut result.site_occupancies {
            for (species, _) in &mut site_occ.species {
                if *species == from {
                    *species = to;
                }
            }
        }
        Ok(result)
    }

    /// Substitute multiple species according to a mapping.
    ///
    /// Each species in the map's keys is replaced with the corresponding value.
    ///
    /// # Arguments
    /// * `map` - HashMap mapping old species to new species
    ///
    /// # Example
    /// ```rust,ignore
    /// use std::collections::HashMap;
    /// use ferrox::species::Species;
    /// use ferrox::element::Element;
    ///
    /// let mut map = HashMap::new();
    /// map.insert(Species::neutral(Element::Fe), Species::neutral(Element::Co));
    /// map.insert(Species::neutral(Element::Ni), Species::neutral(Element::Cu));
    /// let substituted = structure.substitute_map(map)?;
    /// ```
    pub fn substitute_map(&self, map: HashMap<Species, Species>) -> Result<Self> {
        let mut result = self.clone();
        for site_occ in &mut result.site_occupancies {
            for (species, _) in &mut site_occ.species {
                if let Some(replacement) = map.get(species) {
                    *species = *replacement;
                }
            }
        }
        Ok(result)
    }

    /// Remove all sites containing the specified species.
    ///
    /// Sites that have any of the specified species in their occupancy are removed.
    ///
    /// # Arguments
    /// * `species` - Slice of species to remove
    ///
    /// # Example
    /// ```rust,ignore
    /// use ferrox::species::Species;
    /// use ferrox::element::Element;
    ///
    /// let stripped = structure.remove_species(&[
    ///     Species::neutral(Element::Li),
    /// ])?;
    /// ```
    pub fn remove_species(&self, species: &[Species]) -> Result<Self> {
        let species_to_remove: HashSet<&Species> = species.iter().collect();

        // Find indices of sites to keep (those without any species to remove)
        let indices_to_keep: Vec<usize> = self
            .site_occupancies
            .iter()
            .enumerate()
            .filter(|(_, site_occ)| {
                !site_occ
                    .species
                    .iter()
                    .any(|(sp, _)| species_to_remove.contains(sp))
            })
            .map(|(idx, _)| idx)
            .collect();

        let mut result = self.clone();
        result.site_occupancies = indices_to_keep
            .iter()
            .map(|&idx| self.site_occupancies[idx].clone())
            .collect();
        result.frac_coords = indices_to_keep
            .iter()
            .map(|&idx| self.frac_coords[idx])
            .collect();

        Ok(result)
    }

    /// Apply a deformation gradient to the lattice.
    ///
    /// The deformation gradient F transforms the lattice as:
    /// `new_lattice = old_lattice * F` (row-vector convention)
    ///
    /// Fractional coordinates remain unchanged (they're relative to the lattice).
    ///
    /// # Arguments
    /// * `gradient` - 3x3 deformation gradient tensor
    ///
    /// # Example
    /// ```rust,ignore
    /// use nalgebra::Matrix3;
    ///
    /// // Apply 1% tensile strain along x
    /// let f = Matrix3::new(
    ///     1.01, 0.0, 0.0,
    ///     0.0, 1.0, 0.0,
    ///     0.0, 0.0, 1.0,
    /// );
    /// let deformed = structure.deform(f)?;
    /// ```
    pub fn deform(&self, gradient: Matrix3<f64>) -> Result<Self> {
        // Right-multiply: rows are lattice vectors (row-vector convention)
        let new_matrix = self.lattice.matrix() * gradient;
        let new_lattice = Lattice::from_matrix_with_pbc(new_matrix, self.lattice.pbc);

        let mut result = self.clone();
        result.lattice = new_lattice;
        Ok(result)
    }

    /// Randomly perturb atomic positions.
    ///
    /// Each site is translated by a random vector with magnitude uniformly
    /// distributed in [0, distance].
    ///
    /// # Arguments
    /// * `distance` - Maximum perturbation distance in Angstroms
    /// * `seed` - Optional seed for reproducibility
    ///
    /// # Example
    /// ```rust,ignore
    /// // Perturb all atoms by up to 0.1 Å with fixed seed
    /// let perturbed = structure.perturb_copy(0.1, Some(42))?;
    /// ```
    pub fn perturb_copy(&self, distance: f64, seed: Option<u64>) -> Result<Self> {
        let mut result = self.clone();
        result.perturb(distance, None, seed);
        Ok(result)
    }

    // -------------------------------------------------------------------------
    // Site-level transformations
    // -------------------------------------------------------------------------

    /// Insert new sites into the structure.
    ///
    /// Creates a new structure with additional sites at the specified coordinates.
    ///
    /// # Arguments
    ///
    /// * `species` - Species for each new site
    /// * `coords` - Coordinates of each new site
    /// * `fractional` - Whether coordinates are fractional (true) or Cartesian (false)
    ///
    /// # Errors
    ///
    /// Returns an error if the lengths of `species` and `coords` don't match.
    pub fn insert_sites(
        &self,
        species: &[Species],
        coords: &[Vector3<f64>],
        fractional: bool,
    ) -> Result<Self> {
        if species.len() != coords.len() {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "species and coords must have same length ({} vs {})",
                    species.len(),
                    coords.len()
                ),
            });
        }

        let mut result = self.clone();
        for (sp, coord) in species.iter().zip(coords.iter()) {
            let frac_coord = if fractional {
                *coord
            } else {
                result.lattice.get_fractional_coord(coord)
            };
            result.site_occupancies.push(SiteOccupancy::ordered(*sp));
            result.frac_coords.push(frac_coord);
        }
        Ok(result)
    }

    /// Remove sites by index.
    ///
    /// Creates a new structure with the specified sites removed.
    ///
    /// # Errors
    ///
    /// Returns an error if any index is out of bounds.
    pub fn remove_sites(&self, indices: &[usize]) -> Result<Self> {
        let n_sites = self.num_sites();
        for &idx in indices {
            if idx >= n_sites {
                return Err(FerroxError::InvalidStructure {
                    index: idx,
                    reason: format!("Site index {} out of bounds (num_sites={})", idx, n_sites),
                });
            }
        }

        let remove_set: HashSet<usize> = indices.iter().copied().collect();

        let (new_occupancies, new_coords): (Vec<_>, Vec<_>) = self
            .site_occupancies
            .iter()
            .zip(self.frac_coords.iter())
            .enumerate()
            .filter(|(idx, _)| !remove_set.contains(idx))
            .map(|(_, (occ, coord))| (occ.clone(), *coord))
            .unzip();

        let mut result = self.clone();
        result.site_occupancies = new_occupancies;
        result.frac_coords = new_coords;
        Ok(result)
    }

    /// Replace species at specific site indices.
    ///
    /// Creates a new structure with the species at the specified sites replaced.
    ///
    /// # Errors
    ///
    /// Returns an error if any index is out of bounds.
    pub fn replace_site_species(&self, replacements: &[(usize, Species)]) -> Result<Self> {
        let n_sites = self.num_sites();

        for &(idx, _) in replacements {
            if idx >= n_sites {
                return Err(FerroxError::InvalidStructure {
                    index: idx,
                    reason: format!("Site index {} out of bounds (num_sites={})", idx, n_sites),
                });
            }
        }

        let mut result = self.clone();
        for &(idx, species) in replacements {
            result.site_occupancies[idx] = SiteOccupancy::ordered(species);
        }
        Ok(result)
    }

    /// Translate specific sites by a vector, returning a new structure.
    ///
    /// Creates a new structure with the specified sites translated. Duplicate
    /// indices are deduplicated to avoid translating the same site multiple times.
    ///
    /// This is the Result-returning, copy-based version of `translate_sites`.
    ///
    /// # Errors
    ///
    /// Returns an error if any index is out of bounds.
    pub fn translate_sites_copy(
        &self,
        indices: &[usize],
        vector: Vector3<f64>,
        fractional: bool,
    ) -> Result<Self> {
        let n_sites = self.num_sites();

        // Deduplicate indices to avoid translating the same site multiple times
        let mut unique_indices: Vec<usize> = indices.to_vec();
        unique_indices.sort_unstable();
        unique_indices.dedup();

        // Validate indices
        for &idx in &unique_indices {
            if idx >= n_sites {
                return Err(FerroxError::InvalidStructure {
                    index: idx,
                    reason: format!("Site index {} out of bounds (num_sites={})", idx, n_sites),
                });
            }
        }

        // Convert to fractional if needed
        let frac_vector = if fractional {
            vector
        } else {
            self.lattice.get_fractional_coord(&vector)
        };

        let mut result = self.clone();
        for &idx in &unique_indices {
            result.frac_coords[idx] += frac_vector;
        }
        Ok(result)
    }

    /// Translate all sites by a vector.
    ///
    /// Creates a new structure with all sites translated by the given vector.
    pub fn translate_all(&self, vector: Vector3<f64>, fractional: bool) -> Result<Self> {
        let frac_vector = if fractional {
            vector
        } else {
            self.lattice.get_fractional_coord(&vector)
        };

        let mut result = self.clone();
        for fc in &mut result.frac_coords {
            *fc += frac_vector;
        }
        Ok(result)
    }

    /// Apply radial distortion around a center site.
    ///
    /// Displaces neighboring sites radially outward (positive displacement)
    /// or inward (negative displacement) from a center site. Useful for
    /// modeling defects and local relaxation effects.
    ///
    /// # Arguments
    ///
    /// * `center_idx` - Index of the center site
    /// * `displacement` - Radial displacement in Angstroms (positive = outward, negative = inward)
    /// * `cutoff` - Cutoff radius in Angstroms (None = only nearest neighbors)
    ///
    /// # Errors
    ///
    /// Returns an error if `center_idx` is out of bounds.
    pub fn radial_distort(
        &self,
        center_idx: usize,
        displacement: f64,
        cutoff: Option<f64>,
    ) -> Result<Self> {
        let n_sites = self.num_sites();

        if center_idx >= n_sites {
            return Err(FerroxError::InvalidStructure {
                index: center_idx,
                reason: format!(
                    "Center site index {} out of bounds (num_sites={})",
                    center_idx, n_sites
                ),
            });
        }

        let mut result = self.clone();

        // Get the center position in Cartesian coordinates
        let center_frac = result.frac_coords[center_idx];
        let center_cart = result.lattice.get_cartesian_coord(&center_frac);

        // Determine cutoff (if None, find nearest neighbor distance)
        let effective_cutoff = match cutoff {
            Some(r) => r,
            None => {
                // Find minimum non-zero distance to center
                let mut min_dist = f64::INFINITY;
                for idx in 0..n_sites {
                    if idx == center_idx {
                        continue;
                    }
                    let dist = result.get_distance(center_idx, idx);
                    if dist > 1e-8 && dist < min_dist {
                        min_dist = dist;
                    }
                }
                // Add small tolerance to include nearest neighbors
                min_dist + 0.1
            }
        };

        // Apply radial displacement to sites within cutoff
        for idx in 0..n_sites {
            if idx == center_idx {
                continue;
            }

            let fc = result.frac_coords[idx];
            let cart = result.lattice.get_cartesian_coord(&fc);
            let diff = cart - center_cart;
            let dist = diff.norm();

            if dist > 1e-8 && dist <= effective_cutoff {
                // Compute unit radial vector
                let radial_unit = diff / dist;
                // Apply displacement
                let new_cart = cart + radial_unit * displacement;
                result.frac_coords[idx] = result.lattice.get_fractional_coord(&new_cart);
            }
        }

        Ok(result)
    }
}
