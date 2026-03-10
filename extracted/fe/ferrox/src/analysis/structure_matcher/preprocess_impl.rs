use super::{AnonymousClassMapping, ComparatorType, MAX_SUPPORTED_ATOMIC_NUMBER, StructureMatcher};
use crate::element::Element;
use crate::error::OnError;
use crate::lattice::Lattice;
use crate::pbc::wrap_frac_coords_pbc;
use crate::species::Species;
use crate::structure::Structure;
use nalgebra::Matrix3;
use std::collections::{HashMap, HashSet};

impl StructureMatcher {
    /// Create a new `StructureMatcher` with default settings.
    pub fn new() -> Self {
        Self::default()
    }

    /// Builder method to set lattice length tolerance.
    pub fn with_latt_len_tol(mut self, latt_len_tol: f64) -> Self {
        self.latt_len_tol = latt_len_tol;
        self
    }

    /// Builder method to set site position tolerance.
    pub fn with_site_pos_tol(mut self, site_pos_tol: f64) -> Self {
        self.site_pos_tol = site_pos_tol;
        self
    }

    /// Builder method to set angle tolerance.
    pub fn with_angle_tol(mut self, angle_tol: f64) -> Self {
        self.angle_tol = angle_tol;
        self
    }

    /// Builder method to set primitive cell reduction.
    pub fn with_primitive_cell(mut self, primitive_cell: bool) -> Self {
        self.primitive_cell = primitive_cell;
        self
    }

    /// Builder method to set volume scaling.
    pub fn with_scale(mut self, scale: bool) -> Self {
        self.scale = scale;
        self
    }

    /// Builder method to set supercell matching.
    pub fn with_attempt_supercell(mut self, attempt_supercell: bool) -> Self {
        self.attempt_supercell = attempt_supercell;
        self
    }

    /// Builder method to set the comparator type.
    pub fn with_comparator(mut self, comparator_type: ComparatorType) -> Self {
        self.comparator_type = comparator_type;
        self
    }

    /// Builder method to set error handling.
    pub fn with_on_error(mut self, on_error: OnError) -> Self {
        self.on_error = on_error;
        self
    }

    /// Build a predefined element-to-class mapping.
    pub fn predefined_class_mapping(
        mapping_kind: AnonymousClassMapping,
    ) -> HashMap<Element, String> {
        let mut class_mapping = HashMap::new();
        for atomic_number in 1..=MAX_SUPPORTED_ATOMIC_NUMBER {
            if let Some(element) = Element::from_atomic_number(atomic_number)
                && let Some(class_label) = mapping_kind.class_for_element(element)
            {
                class_mapping.insert(element, class_label.to_string());
            }
        }
        class_mapping
    }

    /// Return elements present in the inputs that are not covered by a predefined mapping.
    pub fn missing_predefined_mapping_elements(
        struct1: &Structure,
        struct2: &Structure,
        mapping_kind: AnonymousClassMapping,
    ) -> Vec<Element> {
        let mut missing_elements = HashSet::new();
        for structure in [struct1, struct2] {
            for species in structure.species() {
                if mapping_kind.class_for_element(species.element).is_none() {
                    missing_elements.insert(species.element);
                }
            }
        }
        let mut sorted_missing: Vec<_> = missing_elements.into_iter().collect();
        sorted_missing.sort_unstable();
        sorted_missing
    }

    /// Check if two species are equal according to the comparator.
    pub(super) fn species_equal(&self, sp1: &Species, sp2: &Species) -> bool {
        match self.comparator_type {
            ComparatorType::Species => sp1 == sp2,
            ComparatorType::Element => sp1.element == sp2.element,
        }
    }

    /// Get composition hash for prefiltering, aligned with comparator semantics.
    ///
    /// For `ComparatorType::Element`, oxidation states are ignored.
    /// For `ComparatorType::Species`, full species information is used.
    pub fn composition_hash(&self, structure: &Structure) -> u64 {
        match self.comparator_type {
            ComparatorType::Element => structure.composition().formula_hash(),
            ComparatorType::Species => structure.species_composition().species_hash(),
        }
    }

    pub(super) fn compositions_equal(&self, struct1: &Structure, struct2: &Structure) -> bool {
        match self.comparator_type {
            ComparatorType::Element => {
                struct1.composition().reduced_composition()
                    == struct2.composition().reduced_composition()
            }
            ComparatorType::Species => {
                struct1.species_composition().reduced_composition()
                    == struct2.species_composition().reduced_composition()
            }
        }
    }

    /// Get reduced structure (Niggli reduced, optionally primitive).
    ///
    /// Matches pymatgen's `_get_reduced_structure` behavior:
    /// 1. Niggli reduction on the lattice
    /// 2. If `primitive_cell` is true, reduce to primitive cell via symmetry analysis
    ///
    /// Properties from the original structure are preserved.
    pub(super) fn has_oxidation_states(structure: &Structure) -> bool {
        structure.site_occupancies.iter().any(|site_occ| {
            site_occ
                .species
                .iter()
                .any(|(species, _)| species.oxidation_state.is_some())
        })
    }

    pub(super) fn should_skip_primitive_reduction(&self, structure: &Structure) -> bool {
        self.comparator_type == ComparatorType::Species && Self::has_oxidation_states(structure)
    }

    pub(super) fn niggli_reduce_structure(structure: &Structure) -> Structure {
        let mut reduced_structure = structure.clone();
        // Do Niggli reduction on the lattice
        if let Ok(niggli_lattice) = reduced_structure.lattice.get_niggli_reduced(1e-5) {
            // Transform coordinates to new lattice
            let original_cart_coords = reduced_structure.cart_coords();
            let original_pbc = reduced_structure.lattice.pbc;
            reduced_structure.lattice = niggli_lattice;
            reduced_structure.lattice.pbc = original_pbc;
            reduced_structure.frac_coords = reduced_structure
                .lattice
                .get_fractional_coords(&original_cart_coords);
            // Wrap to [0, 1)
            for frac_coord in &mut reduced_structure.frac_coords {
                *frac_coord = wrap_frac_coords_pbc(frac_coord, reduced_structure.lattice.pbc);
            }
        }
        reduced_structure
    }

    pub(super) fn try_get_reduced_structure(
        &self,
        structure: &Structure,
    ) -> crate::error::Result<Structure> {
        let mut result = Self::niggli_reduce_structure(structure);

        // Reduce to primitive cell if requested (skip empty structures)
        if self.primitive_cell
            && result.num_sites() > 0
            && !self.should_skip_primitive_reduction(&result)
        {
            let original_pbc = result.lattice.pbc;
            let mut prim = result.get_primitive(1e-4)?;
            // Preserve properties from original structure
            prim.properties = result.properties.clone();
            prim.lattice.pbc = original_pbc;
            result = prim;
        }

        Ok(result)
    }

    pub(super) fn get_reduced_structure_with_on_error(
        &self,
        structure: &Structure,
        operation_name: &str,
    ) -> Structure {
        match self.try_get_reduced_structure(structure) {
            Ok(reduced_structure) => reduced_structure,
            Err(error) => {
                if self.on_error.should_fail() {
                    panic!(
                        "StructureMatcher::{operation_name} failed to reduce structure: {error}"
                    );
                }
                tracing::warn!(
                    operation_name,
                    error = %error,
                    "StructureMatcher skipping primitive reduction after error"
                );
                Self::niggli_reduce_structure(structure)
            }
        }
    }

    pub(super) fn has_integer_supercell_ratio(site_count_a: usize, site_count_b: usize) -> bool {
        site_count_a > 0
            && site_count_b > 0
            && (site_count_a.is_multiple_of(site_count_b)
                || site_count_b.is_multiple_of(site_count_a))
    }

    pub(crate) fn reduce_structure_for_batch(
        &self,
        structure: &Structure,
    ) -> crate::error::Result<Structure> {
        self.try_get_reduced_structure(structure)
    }

    /// Preprocess structures for matching (reduces then prepares pair).
    ///
    /// Returns (struct1, struct2, supercell_factor, s1_supercell)
    pub(super) fn preprocess(
        &self,
        struct1: &Structure,
        struct2: &Structure,
    ) -> (Structure, Structure, usize, bool) {
        let s1 = self.get_reduced_structure_with_on_error(struct1, "preprocess");
        let s2 = self.get_reduced_structure_with_on_error(struct2, "preprocess");
        self.preprocess_pair(s1, s2)
    }

    /// Prepare already-reduced structures for matching.
    ///
    /// Computes supercell factor and scales volumes. Use when structures have
    /// already been reduced via `reduce_structure`.
    ///
    /// Returns (struct1, struct2, supercell_factor, s1_supercell)
    pub(super) fn preprocess_pair(
        &self,
        mut s1: Structure,
        mut s2: Structure,
    ) -> (Structure, Structure, usize, bool) {
        let (supercell_factor, s1_supercell) = if self.attempt_supercell {
            // Guard against division by zero
            if s1.num_sites() == 0 || s2.num_sites() == 0 {
                (1, true)
            } else if s2.num_sites() >= s1.num_sites() {
                if s2.num_sites().is_multiple_of(s1.num_sites()) {
                    (s2.num_sites() / s1.num_sites(), true)
                } else {
                    (1, true)
                }
            } else if s1.num_sites().is_multiple_of(s2.num_sites()) {
                (s1.num_sites() / s2.num_sites(), false)
            } else {
                (1, true)
            }
        } else {
            (1, true)
        };

        let mult = if s1_supercell {
            supercell_factor as f64
        } else {
            1.0 / supercell_factor as f64
        };

        // Scale lattices to same volume (skip if empty or degenerate to avoid division by zero)
        let v1 = s1.lattice.volume();
        let v2 = s2.lattice.volume();
        if self.scale && v1 > f64::EPSILON && v2 > f64::EPSILON {
            // PBC consistency check - prevents silent drift when scaling overwrites pbc
            debug_assert_eq!(
                s1.lattice.pbc, s2.lattice.pbc,
                "PBC mismatch in preprocess_pair"
            );
            let pbc = s1.lattice.pbc;
            let ratio = (v2 / (v1 * mult)).powf(1.0 / 6.0);
            s1.lattice = Lattice::new(*s1.lattice.matrix() * ratio);
            s1.lattice.pbc = pbc;
            s2.lattice = Lattice::new(*s2.lattice.matrix() / ratio);
            s2.lattice.pbc = pbc;
        }

        (s1, s2, supercell_factor, s1_supercell)
    }

    /// Create a mask for species matching.
    ///
    /// mask[i][j] = true means s2[i] cannot match s1[j]
    pub(super) fn get_mask(&self, struct1: &Structure, struct2: &Structure) -> Vec<Vec<bool>> {
        let n1 = struct1.num_sites();
        let n2 = struct2.num_sites();
        let mut mask = vec![vec![false; n1]; n2];

        let species1 = struct1.species();
        let species2 = struct2.species();
        for (idx2, sp2) in species2.iter().enumerate() {
            for (idx1, sp1) in species1.iter().enumerate() {
                mask[idx2][idx1] = !self.species_equal(sp1, sp2);
            }
        }

        mask
    }

    /// Find translation indices for matching.
    pub(super) fn get_translation_indices(&self, mask: &[Vec<bool>]) -> (Vec<usize>, usize) {
        if mask.is_empty() {
            return (vec![], 0);
        }

        // Find the row with the most masked (incompatible) entries
        // Note: mask is guaranteed non-empty (checked at line 230), so unwrap is safe
        let (best_row, _) = mask
            .iter()
            .enumerate()
            .max_by_key(|(_, row)| row.iter().filter(|&&x| x).count())
            .unwrap();

        // Find unmasked indices in struct1 for this row
        let s1_inds: Vec<usize> = mask[best_row]
            .iter()
            .enumerate()
            .filter(|&(_, &masked)| !masked)
            .map(|(idx, _)| idx)
            .collect();

        (s1_inds, best_row)
    }

    /// Get lattice mappings for matching.
    pub(super) fn get_lattices(
        &self,
        target_lattice: &Lattice,
        source: &Structure,
        supercell_size: usize,
    ) -> Vec<(Lattice, Matrix3<i32>)> {
        source
            .lattice
            .find_all_mappings_with_determinant(
                target_lattice,
                self.latt_len_tol,
                self.angle_tol,
                true,
                supercell_size,
            )
            .into_iter()
            .map(|(latt, _, scale_m)| (latt, scale_m))
            .collect()
    }

    pub(super) fn sorted_lattice_candidates(
        &self,
        target_lattice: &Lattice,
        source: &Structure,
        supercell_size: usize,
    ) -> Vec<(Lattice, Matrix3<i32>)> {
        let mut lattice_candidates = self.get_lattices(target_lattice, source, supercell_size);
        lattice_candidates.sort_by(|(lattice_a, _), (lattice_b, _)| {
            let score_a = Self::lattice_similarity_score(lattice_a, target_lattice);
            let score_b = Self::lattice_similarity_score(lattice_b, target_lattice);
            score_a.total_cmp(&score_b)
        });
        lattice_candidates
    }

    pub(super) fn lattice_similarity_score(
        candidate_lattice: &Lattice,
        target_lattice: &Lattice,
    ) -> f64 {
        let candidate_lengths = candidate_lattice.lengths();
        let target_lengths = target_lattice.lengths();
        let candidate_angles = candidate_lattice.angles();
        let target_angles = target_lattice.angles();

        let mut score = 0.0;
        for axis_idx in 0..3 {
            let length_norm = target_lengths[axis_idx].abs().max(f64::EPSILON);
            score += (candidate_lengths[axis_idx] - target_lengths[axis_idx]).abs() / length_norm;
            score += (candidate_angles[axis_idx] - target_angles[axis_idx]).abs() / 180.0;
        }
        score
    }

    /// Compute average lattice from two lattices.
    pub(super) fn average_lattice(l1: &Lattice, l2: &Lattice) -> Lattice {
        let params1 = l1.lengths();
        let params2 = l2.lengths();
        let angles1 = l1.angles();
        let angles2 = l2.angles();

        let mut avg_lattice = Lattice::from_parameters(
            (params1[0] + params2[0]) / 2.0,
            (params1[1] + params2[1]) / 2.0,
            (params1[2] + params2[2]) / 2.0,
            (angles1[0] + angles2[0]) / 2.0,
            (angles1[1] + angles2[1]) / 2.0,
            (angles1[2] + angles2[2]) / 2.0,
        );
        debug_assert_eq!(l1.pbc, l2.pbc, "PBC mismatch in average_lattice");
        avg_lattice.pbc = l1.pbc;
        avg_lattice
    }
}
