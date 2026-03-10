use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::species::{SiteOccupancy, Species};
use itertools::Itertools;
use std::collections::{BTreeMap, HashMap};

use super::Structure;

impl Structure {
    // === Bond Valence Sum Methods ===

    /// Compute bond valence sums for all sites using O'Keeffe & Brese formula.
    ///
    /// For disordered sites, calculates occupancy-weighted average BVS.
    ///
    /// # Arguments
    /// * `max_radius` - Cutoff radius for neighbor search (Å)
    /// * `scale_factor` - Distance scaling (1.015 for GGA, 1.0 for experimental)
    pub fn compute_all_bv_sums(&self, max_radius: f64, scale_factor: f64) -> Result<Vec<f64>> {
        let (center_indices, neighbor_indices, _, distances) =
            self.get_neighbor_list(max_radius, 1e-8, true);

        // Group neighbors by center site
        let mut site_neighbors: Vec<Vec<crate::analysis::oxidation::BvNeighbor>> =
            vec![Vec::new(); self.num_sites()];
        for (idx, &center_idx) in center_indices.iter().enumerate() {
            for (sp, occ) in &self.site_occupancies[neighbor_indices[idx]].species {
                site_neighbors[center_idx].push(crate::analysis::oxidation::BvNeighbor {
                    element: sp.element,
                    distance: distances[idx],
                    occupancy: *occ,
                });
            }
        }

        // Calculate occupancy-weighted BVS for each site
        Ok(site_neighbors
            .into_iter()
            .zip(&self.site_occupancies)
            .map(|(neighbors, site_occu)| {
                site_occu
                    .species
                    .iter()
                    .map(|(sp, occ)| {
                        crate::analysis::oxidation::calculate_bv_sum(
                            sp.element,
                            &neighbors,
                            scale_factor,
                        ) * occ
                    })
                    .sum()
            })
            .collect())
    }

    /// Guess oxidation states using BVS-based MAP estimation with symmetry.
    ///
    /// # Errors
    /// Returns an error if any site is disordered (multiple species), since
    /// BVS analysis requires a single element per site.
    pub fn guess_oxidation_states_bvs(
        &self,
        symprec: f64,
        max_radius: f64,
        scale_factor: f64,
    ) -> Result<Vec<i8>> {
        if self.num_sites() == 0 {
            return Ok(vec![]);
        }

        // Guard against disordered sites - BVS requires single element per site
        if let Some(idx) = self.site_occupancies.iter().position(|so| !so.is_ordered()) {
            return Err(FerroxError::InvalidStructure {
                index: idx,
                reason: "BVS-based oxidation state guessing requires ordered sites; \
                         use composition-based guessing for disordered structures"
                    .into(),
            });
        }

        let orbits = self.get_equivalent_sites(symprec)?;
        let bv_sums = self.compute_all_bv_sums(max_radius, scale_factor)?;

        // Find unique orbit representatives and their multiplicities
        let mut seen = std::collections::HashSet::new();
        let unique_sites: Vec<_> = orbits
            .iter()
            .enumerate()
            .filter(|&(_, &orbit)| seen.insert(orbit))
            .map(|(idx, _)| idx)
            .collect();

        let (site_probs, multiplicities): (Vec<_>, Vec<_>) = unique_sites
            .iter()
            .map(|&idx| {
                let elem = self.site_occupancies[idx].dominant_species().element;
                let probs =
                    crate::analysis::oxidation::get_oxi_state_probabilities(elem, bv_sums[idx]);
                let mult = orbits.iter().filter(|&&o| o == orbits[idx]).count();
                // Filter to top candidates (>1% of max prob), fallback to neutral
                let filtered = if probs.is_empty() {
                    vec![(0, 1.0)]
                } else {
                    let max_p = probs[0].1;
                    probs
                        .into_iter()
                        .filter(|(_, p)| *p > 0.01 * max_p)
                        .collect()
                };
                (filtered, mult)
            })
            .unzip();

        let assignment = crate::analysis::oxidation::find_charge_balanced_assignment(
            &site_probs,
            &multiplicities,
        )
        .ok_or_else(|| FerroxError::CompositionError {
            reason: "No charge-balanced oxidation state assignment found".into(),
        })?;

        // Expand to all sites via orbit mapping
        let mut result = vec![0i8; self.num_sites()];
        for (unique_idx, &site_idx) in unique_sites.iter().enumerate() {
            let orbit = orbits[site_idx];
            for (idx, &o) in orbits.iter().enumerate() {
                if o == orbit {
                    result[idx] = assignment[unique_idx];
                }
            }
        }
        Ok(result)
    }

    /// Add oxidation states by element symbol mapping.
    pub fn add_oxidation_state_by_element(
        &self,
        oxi_states: &std::collections::HashMap<String, i8>,
    ) -> Self {
        self.map_species(|sp| {
            let oxi = oxi_states
                .get(sp.element.symbol())
                .copied()
                .or(sp.oxidation_state);
            Species::new(sp.element, oxi)
        })
    }

    /// Add oxidation states by site index. Errors if any site is disordered.
    pub fn add_oxidation_state_by_site(&self, oxi_states: &[i8]) -> Result<Self> {
        if let Some(idx) = self.site_occupancies.iter().position(|so| !so.is_ordered()) {
            return Err(FerroxError::InvalidStructure {
                index: idx,
                reason: "add_oxidation_state_by_site requires ordered sites".into(),
            });
        }
        if oxi_states.len() != self.num_sites() {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "oxi_states length ({}) != num_sites ({})",
                    oxi_states.len(),
                    self.num_sites()
                ),
            });
        }
        Ok(self.map_species_by_site(|site_idx, sp| {
            Species::new(sp.element, Some(oxi_states[site_idx]))
        }))
    }

    /// Remove oxidation states from all sites.
    pub fn remove_oxidation_states(&self) -> Self {
        self.map_species(|sp| Species::neutral(sp.element))
    }

    // Helper: transform all species with a mapping function, preserving site properties
    fn map_species<F>(&self, f: F) -> Self
    where
        F: Fn(&Species) -> Species,
    {
        Self {
            lattice: self.lattice.clone(),
            site_occupancies: self
                .site_occupancies
                .iter()
                .map(|so| {
                    let new_species = so.species.iter().map(|(sp, occ)| (f(sp), *occ)).collect();
                    SiteOccupancy::with_properties(new_species, so.properties.clone())
                })
                .collect(),
            frac_coords: self.frac_coords.clone(),
            pbc: self.pbc,
            charge: self.charge,
            properties: self.properties.clone(),
        }
    }

    // Helper: transform species with site index context, preserving site properties
    fn map_species_by_site<F>(&self, f: F) -> Self
    where
        F: Fn(usize, &Species) -> Species,
    {
        Self {
            lattice: self.lattice.clone(),
            site_occupancies: self
                .site_occupancies
                .iter()
                .enumerate()
                .map(|(idx, so)| {
                    let new_species = so
                        .species
                        .iter()
                        .map(|(sp, occ)| (f(idx, sp), *occ))
                        .collect();
                    SiteOccupancy::with_properties(new_species, so.properties.clone())
                })
                .collect(),
            frac_coords: self.frac_coords.clone(),
            pbc: self.pbc,
            charge: self.charge,
            properties: self.properties.clone(),
        }
    }

    /// Get unique elements in this structure.
    pub fn unique_elements(&self) -> Vec<Element> {
        self.site_occupancies
            .iter()
            .flat_map(|so| so.species.iter().map(|(sp, _)| sp.element))
            .unique()
            .collect()
    }

    /// Create a copy with species elements remapped.
    ///
    /// If multiple species map to the same element, their occupancies are summed.
    pub fn remap_species(&self, mapping: &HashMap<Element, Element>) -> Self {
        let new_site_occupancies: Vec<SiteOccupancy> = self
            .site_occupancies
            .iter()
            .map(|so| {
                // Group by (new_element, oxidation_state) and sum occupancies
                // Use BTreeMap for deterministic ordering (important for dominant_species on ties)
                let mut grouped: BTreeMap<(Element, Option<i8>), f64> = BTreeMap::new();
                for (sp, occ) in &so.species {
                    let new_elem = mapping.get(&sp.element).copied().unwrap_or(sp.element);
                    let key = (new_elem, sp.oxidation_state);
                    *grouped.entry(key).or_insert(0.0) += occ;
                }
                let new_species: Vec<(Species, f64)> = grouped
                    .into_iter()
                    .map(|((elem, oxi), occ)| (Species::new(elem, oxi), occ))
                    .collect();
                SiteOccupancy::new(new_species)
            })
            .collect();
        Self {
            lattice: self.lattice.clone(),
            site_occupancies: new_site_occupancies,
            frac_coords: self.frac_coords.clone(),
            pbc: self.pbc,
            charge: self.charge,
            properties: self.properties.clone(),
        }
    }
}
