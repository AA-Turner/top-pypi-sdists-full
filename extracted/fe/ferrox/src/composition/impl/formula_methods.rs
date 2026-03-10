use crate::composition::{AMOUNT_TOLERANCE, Composition, format_amount, gcd_float, hill_sort_key};
use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::species::Species;
use indexmap::IndexMap;
use std::collections::HashSet;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

impl Composition {
    // =========================================================================
    // Formula Representations
    // =========================================================================

    /// Get species sorted by electronegativity (most electropositive first).
    fn sorted_by_electronegativity(&self) -> Vec<(&Species, &f64)> {
        let mut sorted: Vec<_> = self.species.iter().collect();
        sorted.sort_by(|(a, _), (b, _)| {
            let en_a = a.electronegativity().unwrap_or(f64::MAX);
            let en_b = b.electronegativity().unwrap_or(f64::MAX);
            en_a.partial_cmp(&en_b)
                .unwrap_or(std::cmp::Ordering::Equal)
                .then_with(|| a.element.symbol().cmp(b.element.symbol()))
        });
        sorted
    }

    /// Get a formula string with elements sorted by electronegativity.
    ///
    /// Most electropositive elements come first (e.g., "Li4 Fe4 P4 O16").
    ///
    /// Note: Oxidation states are ignored. Species are collapsed to element
    /// symbols only. Use `iter()` to access full Species information.
    pub fn formula(&self) -> String {
        if self.is_empty() {
            return String::new();
        }
        // Aggregate by element (collapse oxidation states), then sort
        self.element_composition()
            .sorted_by_electronegativity()
            .iter()
            .map(|(sp, amt)| format_amount(sp.element.symbol(), **amt))
            .collect::<Vec<_>>()
            .join(" ")
    }

    /// Get the reduced formula string.
    ///
    /// Amounts are divided by their GCD, producing minimal integer ratios.
    ///
    /// Note: Oxidation states are ignored. Species are collapsed to element
    /// symbols only. Two compositions with identical elements but different
    /// oxidation states (e.g., Fe²⁺O vs Fe³⁺O) produce identical formulas.
    pub fn reduced_formula(&self) -> String {
        if self.is_empty() {
            return String::new();
        }
        // Aggregate by element (collapse oxidation states)
        let elem_comp = self.element_composition();
        let gcd = elem_comp.gcd_of_amounts();
        if gcd < AMOUNT_TOLERANCE {
            return self.formula().replace(' ', "");
        }

        elem_comp
            .sorted_by_electronegativity()
            .iter()
            .map(|(sp, amt)| format_amount(sp.element.symbol(), **amt / gcd))
            .collect::<Vec<_>>()
            .join("")
    }

    /// Get the anonymous formula with elements replaced by A, B, C, etc.
    ///
    /// Elements are sorted by electronegativity (same order as reduced_formula),
    /// then replaced with sequential letters. Useful for structure matching.
    ///
    /// # Example
    /// ```
    /// use ferrox::composition::Composition;
    /// let comp = Composition::from_formula("Fe2O3").unwrap();
    /// assert_eq!(comp.anonymous_formula(), "A2B3");
    /// ```
    pub fn anonymous_formula(&self) -> String {
        if self.is_empty() {
            return String::new();
        }
        let elem_comp = self.element_composition();
        let gcd = elem_comp.gcd_of_amounts();
        if gcd < AMOUNT_TOLERANCE {
            return String::new();
        }

        elem_comp
            .sorted_by_electronegativity()
            .iter()
            .enumerate()
            .map(|(idx, (_, amt))| {
                let letter = (b'A' + idx as u8) as char;
                format_amount(&letter.to_string(), **amt / gcd)
            })
            .collect::<Vec<_>>()
            .join("")
    }

    /// Get the Hill formula.
    ///
    /// Carbon first, then hydrogen, then remaining elements alphabetically.
    /// When there's no carbon, all elements are alphabetically sorted.
    pub fn hill_formula(&self) -> String {
        if self.is_empty() {
            return String::new();
        }

        // Get element composition (collapse oxidation states)
        let elem_comp = self.element_composition();
        let mut entries: Vec<(&str, f64)> = elem_comp
            .species
            .iter()
            .map(|(sp, amt)| (sp.element.symbol(), *amt))
            .collect();

        // Hill order: C first (if present), then H, then alphabetical
        let has_carbon = entries.iter().any(|(sym, _)| *sym == "C");
        entries.sort_by(|(a, _), (b, _)| {
            hill_sort_key(a, has_carbon).cmp(&hill_sort_key(b, has_carbon))
        });

        entries
            .iter()
            .map(|(sym, amt)| format_amount(sym, *amt))
            .collect::<Vec<_>>()
            .join(" ")
    }

    /// Get the alphabetical formula.
    ///
    /// Elements sorted alphabetically.
    pub fn alphabetical_formula(&self) -> String {
        let formula = self.formula();
        let mut parts: Vec<_> = formula.split_whitespace().collect();
        parts.sort();
        parts.join(" ")
    }

    // =========================================================================
    // Reduction Methods
    // =========================================================================

    /// Get the reduced composition (amounts divided by GCD).
    pub fn reduced_composition(&self) -> Self {
        let factor = self.get_reduced_factor();
        if factor < AMOUNT_TOLERANCE {
            return self.clone();
        }
        self.clone() / factor
    }

    /// Get the reduction factor (GCD of amounts).
    pub fn get_reduced_factor(&self) -> f64 {
        self.gcd_of_amounts()
    }

    /// Compute GCD of all amounts.
    pub(crate) fn gcd_of_amounts(&self) -> f64 {
        if self.species.is_empty() {
            return 0.0;
        }

        let amounts: Vec<f64> = self.species.values().copied().collect();
        let mut result = amounts[0].abs();

        for &amt in &amounts[1..] {
            result = gcd_float(result, amt.abs());
            if result < AMOUNT_TOLERANCE {
                return 1.0; // Fallback
            }
        }

        result
    }

    /// Get the element composition (collapse oxidation states).
    ///
    /// Species with the same element are merged. Near-zero amounts are filtered out.
    pub fn element_composition(&self) -> Self {
        let mut elem_amounts: IndexMap<Species, f64> = IndexMap::new();
        for (sp, amt) in &self.species {
            let neutral = Species::neutral(sp.element);
            *elem_amounts.entry(neutral).or_insert(0.0) += amt;
        }
        // Filter out near-zero amounts (can occur when oxidation states cancel)
        elem_amounts.retain(|_, amt| amt.abs() >= AMOUNT_TOLERANCE);
        Self {
            species: elem_amounts,
            allow_negative: self.allow_negative,
        }
    }

    // =========================================================================
    // Comparison Methods
    // =========================================================================

    /// Check if two compositions are approximately equal.
    ///
    /// Uses both relative and absolute tolerances.
    pub fn almost_equals(&self, other: &Self, rel_tol: f64, abs_tol: f64) -> bool {
        let all_species: HashSet<_> = self.species.keys().chain(other.species.keys()).collect();

        for sp in all_species {
            let a = self.get(*sp);
            let b = other.get(*sp);
            let tol = abs_tol + rel_tol * (a.abs() + b.abs()) / 2.0;
            if (a - b).abs() > tol {
                return false;
            }
        }
        true
    }

    // =========================================================================
    // Element Remapping
    // =========================================================================

    /// Create new composition with elements remapped according to mapping.
    ///
    /// Elements not in the mapping are preserved as-is.
    /// If multiple elements map to the same target, their amounts are summed.
    pub fn remap_elements(&self, mapping: &std::collections::HashMap<Element, Element>) -> Self {
        let mut remapped: IndexMap<Species, f64> = IndexMap::new();
        for (sp, &amt) in &self.species {
            let new_elem = mapping.get(&sp.element).copied().unwrap_or(sp.element);
            let new_sp = Species::new(new_elem, sp.oxidation_state);
            *remapped.entry(new_sp).or_insert(0.0) += amt;
        }
        Self {
            species: remapped,
            allow_negative: self.allow_negative,
        }
    }

    // =========================================================================
    // Checked Arithmetic
    // =========================================================================

    /// Subtract with error checking for negative amounts.
    ///
    /// Returns an error if the result would have negative amounts and
    /// self.allow_negative is false. The result inherits the caller's
    /// allow_negative policy, not the RHS's.
    pub fn sub_checked(&self, other: &Self) -> Result<Self> {
        let mut result = self.clone() - other.clone();
        // Enforce caller's policy, not the merged policy from the - operator
        result.allow_negative = self.allow_negative;
        if !result.is_valid() {
            return Err(FerroxError::CompositionError {
                reason: "Subtraction resulted in negative amounts".into(),
            });
        }
        Ok(result)
    }

    /// Get a hash of the reduced formula (element-only, ignores oxidation states).
    ///
    /// This is useful for grouping compositions by stoichiometry regardless of
    /// oxidation states. Note: This is different from the `Hash` trait which
    /// includes full Species information including oxidation states.
    ///
    /// Two compositions with Fe2O3 stoichiometry will have the same formula_hash
    /// even if one has Fe²⁺/Fe³⁺ and the other has neutral Fe.
    pub fn formula_hash(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.reduced_formula().hash(&mut hasher);
        hasher.finish()
    }

    /// Get a hash that includes full Species information (with oxidation states).
    ///
    /// Unlike `formula_hash()` which ignores oxidation states, this method
    /// produces different hashes for compositions with the same elements but
    /// different oxidation states (e.g., Fe²⁺O vs Fe³⁺O).
    pub fn species_hash(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        // Use the Hash trait implementation which includes oxidation states
        self.reduced_composition().hash(&mut hasher);
        hasher.finish()
    }
}
