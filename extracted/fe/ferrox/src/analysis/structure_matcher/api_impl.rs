use super::{
    AnonymousClassMapping, AnonymousMatchMode, COMPOSITION_WEIGHT, ComparatorType,
    DISJOINT_COMPOSITION_DISTANCE, EMPTY_STRUCTURE_DISTANCE, MAX_SUPPORTED_ATOMIC_NUMBER,
    MIN_LATTICE_VOLUME, StructureMatcher, UNMATCHED_SOURCE_PENALTY, UNMATCHED_TARGET_PENALTY,
};
use crate::element::Element;
use crate::lattice::Lattice;
use crate::structure::Structure;
use itertools::Itertools;
use nalgebra::Vector3;
use std::collections::{HashMap, HashSet};

impl StructureMatcher {
    /// Check if two structures match.
    ///
    /// Returns `true` when the structures are equivalent within configured tolerances.
    pub fn fit(&self, struct1: &Structure, struct2: &Structure) -> bool {
        // Reduce structures then delegate to fit_preprocessed
        self.fit_preprocessed(
            &self.get_reduced_structure_with_on_error(struct1, "fit"),
            &self.get_reduced_structure_with_on_error(struct2, "fit"),
        )
    }

    /// Get the RMS distance between two structures.
    ///
    /// # Returns
    ///
    /// `Some((rms, max_dist))` if structures match, `None` otherwise.
    pub fn get_rms_dist(&self, struct1: &Structure, struct2: &Structure) -> Option<(f64, f64)> {
        if struct1.lattice.pbc != struct2.lattice.pbc {
            return None;
        }
        let (s1, s2, supercell_factor, s1_supercell) = self.preprocess(struct1, struct2);
        self.match_internal(&s1, &s2, supercell_factor, s1_supercell, false, true)
            .map(|(rms, distances, _)| {
                let max_dist = distances.iter().cloned().fold(0.0, f64::max);
                (rms, max_dist)
            })
    }

    /// Compute a universal distance between any two crystal structures.
    ///
    /// Unlike `get_rms_dist` which may return `None` for incompatible structures,
    /// this method always returns a finite distance value, making it suitable for
    /// consistent ranking of structures by similarity.
    ///
    /// # Properties
    ///
    /// - d(x, y) ≥ 0 (non-negative)
    /// - d(x, x) = 0 (identity)
    /// - d(x, y) = d(y, x) (symmetric)
    /// - Always finite (empty vs non-empty returns `EMPTY_STRUCTURE_DISTANCE`)
    ///
    /// Note: Triangle inequality is not guaranteed due to greedy matching.
    ///
    /// # Algorithm
    ///
    /// The distance is a weighted sum of:
    /// 1. **Geometric distance**: RMS of greedy-matched site positions (both structures
    ///    normalized to unit total volume for consistent comparison)
    /// 2. **Composition distance**: Jaccard distance on element sets
    ///
    /// # Returns
    ///
    /// Finite distance in [0, 1e9]. Identical structures return 0.0.
    pub fn get_structure_distance(&self, struct1: &Structure, struct2: &Structure) -> f64 {
        let n1 = struct1.num_sites();
        let n2 = struct2.num_sites();

        // Handle edge cases - always return finite values
        if n1 == 0 && n2 == 0 {
            return 0.0;
        }
        if n1 == 0 || n2 == 0 {
            return EMPTY_STRUCTURE_DISTANCE;
        }

        // Composition distance (Jaccard distance on element sets)
        let elements1: HashSet<_> = struct1.species().iter().map(|s| s.element).collect();
        let elements2: HashSet<_> = struct2.species().iter().map(|s| s.element).collect();

        let intersection = elements1.intersection(&elements2).count();
        if intersection == 0 {
            return DISJOINT_COMPOSITION_DISTANCE;
        }

        let union = elements1.union(&elements2).count();
        let composition_distance = 1.0 - (intersection as f64 / union as f64);

        // Use non-panicking reduction fallback here so this method always returns
        // a finite distance, independent of the on_error policy.
        let s1_reduced = self
            .try_get_reduced_structure(struct1)
            .unwrap_or_else(|_| Self::niggli_reduce_structure(struct1));
        let s2_reduced = self
            .try_get_reduced_structure(struct2)
            .unwrap_or_else(|_| Self::niggli_reduce_structure(struct2));
        let n1_reduced = s1_reduced.num_sites();
        let n2_reduced = s2_reduced.num_sites();

        // Symmetrize geometric distance when REDUCED sizes are equal (greedy matching is order-dependent)
        // Must use reduced sizes since compute_geometric_distance operates on reduced structures
        let geometric_distance = if n1_reduced == n2_reduced {
            let d1 = self.compute_geometric_distance_inner(&s1_reduced, &s2_reduced);
            let d2 = self.compute_geometric_distance_inner(&s2_reduced, &s1_reduced);
            (d1 + d2) / 2.0
        } else {
            self.compute_geometric_distance_inner(&s1_reduced, &s2_reduced)
        };
        geometric_distance + COMPOSITION_WEIGHT * composition_distance
    }

    /// Compute geometric distance between two already-reduced structures.
    ///
    /// Normalizes both structures to unit total volume (1 Å³), converts each to Cartesian
    /// in this common frame, then computes RMS distance via greedy element-constrained matching.
    ///
    /// Note: Expects pre-reduced structures (call get_reduced_structure first).
    fn compute_geometric_distance_inner(&self, s1: &Structure, s2: &Structure) -> f64 {
        let n1 = s1.num_sites();
        let n2 = s2.num_sites();

        if n1 == 0 || n2 == 0 {
            return EMPTY_STRUCTURE_DISTANCE;
        }

        // Guard against zero/degenerate volumes to avoid inf/NaN in normalization
        let vol1 = s1.lattice.volume();
        let vol2 = s2.lattice.volume();
        if vol1 <= MIN_LATTICE_VOLUME || vol2 <= MIN_LATTICE_VOLUME {
            return EMPTY_STRUCTURE_DISTANCE; // Degenerate lattice treated as incomparable
        }

        // Normalize BOTH lattices to unit total volume (1 Å³). This ensures distances
        // are comparable regardless of the original cell sizes.
        let scale1 = (1.0 / vol1).powf(1.0 / 3.0);
        let scale2 = (1.0 / vol2).powf(1.0 / 3.0);
        let mut lattice1 = Lattice::new(*s1.lattice.matrix() * scale1);
        let mut lattice2 = Lattice::new(*s2.lattice.matrix() * scale2);
        lattice1.pbc = s1.lattice.pbc;
        lattice2.pbc = s2.lattice.pbc;

        let frac1 = &s1.frac_coords;
        let frac2 = &s2.frac_coords;

        let elem1: Vec<_> = s1.species().iter().map(|s| s.element).collect();
        let elem2: Vec<_> = s2.species().iter().map(|s| s.element).collect();

        // Use smaller as source, larger as target (for consistent matching direction)
        let (
            source_frac,
            target_frac,
            source_elem,
            target_elem,
            source_latt,
            target_latt,
            n_source,
            n_target,
        ) = if n1 <= n2 {
            (frac1, frac2, &elem1, &elem2, &lattice1, &lattice2, n1, n2)
        } else {
            (frac2, frac1, &elem2, &elem1, &lattice2, &lattice1, n2, n1)
        };

        // Greedy matching: for each source site, find nearest compatible target site
        let mut total_sq_dist = 0.0;
        let mut used_target = vec![false; n_target];

        for (src_idx, src_frac) in source_frac.iter().enumerate() {
            let src_elem = source_elem[src_idx];
            let mut best_dist = f64::INFINITY;
            let mut best_target = None;

            for (tgt_idx, tgt_frac) in target_frac.iter().enumerate() {
                if used_target[tgt_idx] || target_elem[tgt_idx] != src_elem {
                    continue;
                }

                // Minimum image distance handling different lattices:
                // 1. Convert each site to Cartesian using its OWN lattice
                // 2. Compute Cartesian difference
                // 3. Convert to fractional (using source_latt) for PBC wrapping
                // 4. Wrap to [-0.5, 0.5] and convert back to Cartesian
                let src_cart = source_latt.get_cartesian_coords(&[*src_frac])[0];
                let tgt_cart = target_latt.get_cartesian_coords(&[*tgt_frac])[0];
                let cart_diff = tgt_cart - src_cart;

                // Convert to fractional for minimum-image wrapping (source lattice
                // as reference). Only wrap along periodic axes.
                let frac_diff = source_latt.get_fractional_coords(&[cart_diff])[0];
                let pbc = source_latt.pbc;
                let wrap = |val: f64, periodic: bool| {
                    if periodic { val - val.round() } else { val }
                };
                let wrapped_frac = Vector3::new(
                    wrap(frac_diff.x, pbc[0]),
                    wrap(frac_diff.y, pbc[1]),
                    wrap(frac_diff.z, pbc[2]),
                );
                let wrapped_cart_diff = source_latt.get_cartesian_coords(&[wrapped_frac])[0];
                let dist = wrapped_cart_diff.norm();

                if dist < best_dist {
                    best_dist = dist;
                    best_target = Some(tgt_idx);
                }
            }

            if let Some(tgt_idx) = best_target {
                used_target[tgt_idx] = true;
                total_sq_dist += best_dist * best_dist;
            } else {
                total_sq_dist += UNMATCHED_SOURCE_PENALTY;
            }
        }

        let matched = used_target.iter().filter(|&&u| u).count();
        let unmatched_targets = n_target - matched;
        total_sq_dist += unmatched_targets as f64 * UNMATCHED_TARGET_PENALTY;

        let total_sites = n_source + unmatched_targets;
        (total_sq_dist / total_sites as f64).sqrt()
    }

    /// Check if two structures match under any species permutation.
    ///
    /// This is useful for comparing structures where the identity of species
    /// is not important, only the arrangement. For example, NaCl and MgO both
    /// have the rocksalt structure, so `fit_anonymous` would return true.
    ///
    /// # Algorithm (matches pymatgen's fit_anonymous)
    ///
    /// 1. Get unique elements from both structures in order of first appearance
    /// 2. If different number of unique elements, return false
    /// 3. For each permutation of struct2's elements:
    ///    - Create mapping: struct1.elements[i] -> permuted_elements[i]
    ///    - Compute mapped composition from struct1
    ///    - If mapped composition hash != struct2 composition hash, skip (fast pruning)
    ///    - Otherwise, remap struct1's species and call fit()
    /// 4. Return true on first match
    ///
    /// # Note
    ///
    /// This method always uses element-only matching (ignores oxidation states),
    /// regardless of the matcher's `comparator_type` setting. This matches pymatgen's
    /// behavior where anonymous matching only considers elemental identity.
    pub fn fit_anonymous(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        match_mode: Option<AnonymousMatchMode<'_>>,
    ) -> bool {
        match match_mode.unwrap_or(AnonymousMatchMode::ElementPermutation) {
            AnonymousMatchMode::ElementPermutation => {
                self.fit_anonymous_by_element_permutation(struct1, struct2)
            }
            AnonymousMatchMode::Predefined(mapping_kind) => {
                if !Self::missing_predefined_mapping_elements(struct1, struct2, mapping_kind)
                    .is_empty()
                {
                    return false;
                }
                let class_mapping = Self::predefined_class_mapping(mapping_kind);
                self.fit_anonymous_with_class_mapping(struct1, struct2, &class_mapping)
            }
            AnonymousMatchMode::Custom(class_mapping) => {
                self.fit_anonymous_with_class_mapping(struct1, struct2, class_mapping)
            }
        }
    }

    fn fit_anonymous_by_element_permutation(
        &self,
        struct1: &Structure,
        struct2: &Structure,
    ) -> bool {
        // Get unique elements in order of first appearance
        let elements1 = struct1.unique_elements();
        let elements2 = struct2.unique_elements();

        // Different number of unique elements -> no match possible
        if elements1.len() != elements2.len() {
            return false;
        }

        // Handle empty structures
        if elements1.is_empty() {
            return false;
        }

        // Get compositions for fast pruning (compute once, outside loop)
        // Use element_composition() since fit_anonymous ignores oxidation states
        let comp1 = struct1.composition();
        let comp2 = struct2.composition();
        let comp2_hash = comp2.element_composition().formula_hash();

        // Create element-only matcher once (used for all permutations)
        let element_matcher = Self {
            comparator_type: ComparatorType::Element,
            ..self.clone()
        };

        // Try all permutations of elements2
        for perm in elements2.iter().permutations(elements2.len()) {
            // Create mapping: elements1[i] -> perm[i]
            let mapping: HashMap<Element, Element> = elements1
                .iter()
                .zip(perm.iter())
                .map(|(&e1, &&e2)| (e1, e2))
                .collect();

            // Fast composition hash check before expensive structure matching
            let mapped_comp = comp1.remap_elements(&mapping);
            if mapped_comp.element_composition().formula_hash() != comp2_hash {
                continue;
            }

            // Composition matches - do full structure comparison
            let remapped_struct1 = struct1.remap_species(&mapping);
            if element_matcher.fit(&remapped_struct1, struct2) {
                return true;
            }
        }

        false
    }

    fn fit_anonymous_with_class_mapping(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        class_mapping: &HashMap<Element, String>,
    ) -> bool {
        let Some((mapped_struct1, mapped_struct2)) =
            self.remap_structures_for_class_matching(struct1, struct2, class_mapping)
        else {
            return false;
        };
        let element_matcher = Self {
            comparator_type: ComparatorType::Element,
            ..self.clone()
        };
        element_matcher.fit(&mapped_struct1, &mapped_struct2)
    }

    /// Compute structure distance after applying class-based anonymous mapping.
    ///
    /// Returns `None` if any element in either structure is not present in
    /// `class_mapping`.
    pub fn get_structure_distance_anonymous_mapped(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        class_mapping: &HashMap<Element, String>,
    ) -> Option<f64> {
        let (mapped_struct1, mapped_struct2) =
            self.remap_structures_for_class_matching(struct1, struct2, class_mapping)?;
        let element_matcher = Self {
            comparator_type: ComparatorType::Element,
            ..self.clone()
        };
        Some(element_matcher.get_structure_distance(&mapped_struct1, &mapped_struct2))
    }

    /// Compute structure distance after applying a predefined class-based mapping.
    pub fn get_structure_distance_anonymous_predefined(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        mapping_kind: AnonymousClassMapping,
    ) -> Option<f64> {
        let class_mapping = Self::predefined_class_mapping(mapping_kind);
        self.get_structure_distance_anonymous_mapped(struct1, struct2, &class_mapping)
    }

    fn remap_structures_for_class_matching(
        &self,
        struct1: &Structure,
        struct2: &Structure,
        class_mapping: &HashMap<Element, String>,
    ) -> Option<(Structure, Structure)> {
        let mut class_labels = HashSet::new();
        let mut unique_elements = HashSet::new();
        for structure in [struct1, struct2] {
            for species in structure.species() {
                let element = species.element;
                unique_elements.insert(element);
                let class_label = class_mapping.get(&element)?;
                class_labels.insert(class_label.clone());
            }
        }

        if class_labels.len() > usize::from(MAX_SUPPORTED_ATOMIC_NUMBER) {
            return None;
        }

        let mut sorted_class_labels: Vec<_> = class_labels.into_iter().collect();
        sorted_class_labels.sort_unstable();

        let mut placeholder_by_class = HashMap::new();
        for (class_idx, class_label) in sorted_class_labels.into_iter().enumerate() {
            let placeholder = Element::from_atomic_number((class_idx + 1) as u8)?;
            placeholder_by_class.insert(class_label, placeholder);
        }

        let mut element_remap = HashMap::new();
        for element in unique_elements {
            let class_label = class_mapping.get(&element)?;
            let placeholder_element = *placeholder_by_class.get(class_label)?;
            element_remap.insert(element, placeholder_element);
        }

        let mapped_struct1 = struct1.remap_species(&element_remap);
        let mapped_struct2 = struct2.remap_species(&element_remap);
        Some((mapped_struct1, mapped_struct2))
    }

    /// Check if two already-reduced structures match.
    ///
    /// This is an optimization for batch operations where structures have already
    /// been preprocessed with `reduce_structure`. Skips redundant Niggli reduction
    /// and primitive cell reduction.
    ///
    /// # Arguments
    ///
    /// * `reduced1` - First structure (already Niggli reduced + primitive cell if enabled)
    /// * `reduced2` - Second structure (already preprocessed)
    ///
    /// # Note
    ///
    /// Use this when you've already called `reduce_structure` on both inputs.
    /// For general use, prefer `fit` which handles preprocessing automatically.
    pub fn fit_preprocessed(&self, reduced1: &Structure, reduced2: &Structure) -> bool {
        if reduced1.lattice.pbc != reduced2.lattice.pbc {
            return false;
        }

        // Use preprocess_pair to handle supercell factor and volume scaling
        let (s1, s2, supercell_factor, s1_supercell) =
            self.preprocess_pair(reduced1.clone(), reduced2.clone());

        // Composition check
        if self.composition_hash(&s1) != self.composition_hash(&s2) {
            return false;
        }
        if !self.compositions_equal(&s1, &s2) {
            return false;
        }

        // Site count check (without supercell)
        if !self.attempt_supercell && s1.num_sites() != s2.num_sites() {
            return false;
        }
        if self.attempt_supercell
            && s1.num_sites() != s2.num_sites()
            && !Self::has_integer_supercell_ratio(s1.num_sites(), s2.num_sites())
        {
            return false;
        }

        if self
            .match_internal(&s1, &s2, supercell_factor, s1_supercell, true, false)
            .is_some_and(|(val, _, _)| val <= self.site_pos_tol)
        {
            return true;
        }

        self.attempt_supercell
            && s1.num_sites() != s2.num_sites()
            && self.match_with_explicit_supercell(&s1, &s2)
    }

    /// Apply Niggli reduction and optionally primitive cell reduction.
    ///
    /// Use this to preprocess structures before calling `fit_preprocessed`.
    pub fn reduce_structure(&self, structure: &Structure) -> Structure {
        self.get_reduced_structure_with_on_error(structure, "reduce_structure")
    }
}
