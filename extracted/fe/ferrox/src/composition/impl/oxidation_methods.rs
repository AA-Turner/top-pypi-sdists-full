use crate::composition::{AMOUNT_TOLERANCE, Composition, gcd_float};
use crate::element::Element;
use crate::species::Species;
use indexmap::IndexMap;
use std::collections::HashMap;

impl Composition {
    // =========================================================================
    // Oxidation State Methods
    // =========================================================================

    /// Guess charge-balanced oxidation state assignments for this composition.
    ///
    /// Returns possible oxidation state assignments sorted by ICSD probability.
    /// The first result is the most likely assignment.
    ///
    /// # Arguments
    ///
    /// * `target_charge` - Desired total charge (default 0 for charge balance)
    /// * `oxi_states_override` - Override oxidation states for specific elements
    /// * `use_all_oxi_states` - If true, consider all known oxidation states (not just common/ICSD)
    /// * `max_sites` - Maximum number of sites to enumerate (None = no limit)
    ///
    /// # Returns
    ///
    /// Vector of `OxiStateGuess` with oxidation states and probability scores.
    ///
    /// # Example
    ///
    /// ```
    /// use ferrox::composition::Composition;
    ///
    /// let comp = Composition::from_formula("Fe2O3").unwrap();
    /// let guesses = comp.oxi_state_guesses(0, None, false, None);
    /// // Best guess should be Fe3+ and O2-
    /// ```
    pub fn oxi_state_guesses(
        &self,
        target_charge: i8,
        oxi_states_override: Option<&std::collections::HashMap<Element, Vec<i8>>>,
        use_all_oxi_states: bool,
        max_sites: Option<usize>,
    ) -> Vec<crate::analysis::oxidation::OxiStateGuess> {
        // Collect unique elements and their amounts
        let elem_comp = self.element_composition();
        let elements: Vec<Element> = elem_comp.species.keys().map(|sp| sp.element).collect();
        let amounts: Vec<f64> = elem_comp.species.values().copied().collect();

        crate::analysis::oxidation::oxi_state_guesses(
            &elements,
            &amounts,
            target_charge,
            oxi_states_override,
            use_all_oxi_states,
            max_sites,
        )
    }

    /// Return a new composition with oxidation states assigned from guessing.
    ///
    /// Uses `oxi_state_guesses()` to find the most likely oxidation state assignment,
    /// then returns a new composition with those oxidation states applied.
    ///
    /// # Arguments
    ///
    /// * `target_charge` - Desired total charge (default 0 for charge balance)
    /// * `oxi_states_override` - Override oxidation states for specific elements
    /// * `use_all_oxi_states` - If true, consider all known oxidation states
    /// * `max_sites` - Maximum number of sites to enumerate
    ///
    /// # Returns
    ///
    /// New composition with oxidation states, or `None` if no valid assignment found
    /// or if any oxidation state is a non-integer (mixed-valence that cannot be
    /// represented as a single integer oxidation state).
    ///
    /// # Example
    ///
    /// ```
    /// use ferrox::composition::Composition;
    ///
    /// let comp = Composition::from_formula("NaCl").unwrap();
    /// let charged = comp.add_charges_from_oxi_state_guesses(0, None, false, None);
    /// // charged will have Na+ and Cl-
    /// ```
    pub fn add_charges_from_oxi_state_guesses(
        &self,
        target_charge: i8,
        oxi_states_override: Option<&std::collections::HashMap<Element, Vec<i8>>>,
        use_all_oxi_states: bool,
        max_sites: Option<usize>,
    ) -> Option<Self> {
        let guesses = self.oxi_state_guesses(
            target_charge,
            oxi_states_override,
            use_all_oxi_states,
            max_sites,
        );

        let best = guesses.first()?;

        // Check that all oxidation states are close to integers
        // Mixed-valence averages (e.g., 2.67 for Fe3O4) cannot be represented as single i8
        for oxi in best.oxidation_states.values() {
            if (*oxi - oxi.round()).abs() > crate::analysis::oxidation::OXI_INT_TOLERANCE {
                // Non-integer oxidation state indicates mixed-valence; cannot represent
                return None;
            }
        }

        // Create new composition with oxidation states
        let mut new_species: IndexMap<Species, f64> = IndexMap::new();

        for (sp, amt) in &self.species {
            // Look up the oxidation state for this element
            let oxi = best.oxidation_states.get(sp.element.symbol())?;
            let rounded = oxi.round();
            if !rounded.is_finite() || rounded < f64::from(i8::MIN) || rounded > f64::from(i8::MAX)
            {
                return None;
            }
            let oxi_state = rounded as i8;
            let new_sp = Species::new(sp.element, Some(oxi_state));
            *new_species.entry(new_sp).or_insert(0.0) += amt;
        }

        Some(Self {
            species: new_species,
            allow_negative: self.allow_negative,
        })
    }

    /// Remove oxidation states from all species in this composition.
    ///
    /// Returns a new composition where all species are neutral (no oxidation state).
    ///
    /// # Example
    ///
    /// ```
    /// use ferrox::composition::Composition;
    /// use ferrox::element::Element;
    /// use ferrox::species::Species;
    ///
    /// let fe3 = Species::new(Element::Fe, Some(3));
    /// let o2 = Species::new(Element::O, Some(-2));
    /// let comp = Composition::new([(fe3, 2.0), (o2, 3.0)]);
    /// let neutral = comp.remove_charges();
    /// // neutral composition has neutral Fe and O
    /// ```
    pub fn remove_charges(&self) -> Self {
        let mut new_species: IndexMap<Species, f64> = IndexMap::new();
        for (sp, &amt) in &self.species {
            *new_species
                .entry(Species::neutral(sp.element))
                .or_insert(0.0) += amt;
        }
        Self {
            species: new_species,
            allow_negative: self.allow_negative,
        }
    }

    /// Get the total charge of this composition based on oxidation states.
    ///
    /// Returns `None` if any species lacks an oxidation state, or if the total
    /// charge is not close to an integer (e.g., fractional compositions).
    ///
    /// # Example
    ///
    /// ```
    /// use ferrox::composition::Composition;
    /// use ferrox::element::Element;
    /// use ferrox::species::Species;
    ///
    /// let na = Species::new(Element::Na, Some(1));
    /// let cl = Species::new(Element::Cl, Some(-1));
    /// let comp = Composition::new([(na, 1.0), (cl, 1.0)]);
    /// assert_eq!(comp.charge(), Some(0));
    /// ```
    pub fn charge(&self) -> Option<i32> {
        // Epsilon for floating-point comparison. 1e-6 handles rounding errors from
        // f64 arithmetic while rejecting genuinely fractional charges (e.g., 0.5).
        const CHARGE_EPSILON: f64 = 1e-6;

        let mut total = 0.0_f64;
        for (sp, &amt) in &self.species {
            let oxi = sp.oxidation_state?;
            total += oxi as f64 * amt;
        }

        // Check if total is close to an integer
        let rounded = total.round();
        if (total - rounded).abs() > CHARGE_EPSILON {
            // Non-integer charge (e.g., fractional composition)
            return None;
        }

        Some(rounded as i32)
    }

    /// Check if this composition is charge balanced.
    ///
    /// Returns `true` if the total charge is zero, `false` otherwise.
    /// Returns `None` if any species lacks an oxidation state.
    pub fn is_charge_balanced(&self) -> Option<bool> {
        self.charge().map(|c| c == 0)
    }

    /// Number of reduced-formula units per cell (Z). Returns None if non-integer.
    pub fn num_formula_units(&self) -> Option<i32> {
        let factor = self.get_reduced_factor();
        let rounded = factor.round();
        if (factor - rounded).abs() < 1e-6 && rounded > 0.0 && rounded <= i32::MAX as f64 {
            Some(rounded as i32)
        } else {
            None
        }
    }

    /// Mean atomic mass in amu: sum(mass_i * amount_i) / sum(amount_i).
    pub fn mean_atomic_mass(&self) -> f64 {
        let total_atoms = self.num_atoms();
        if total_atoms < 1e-12 {
            return 0.0;
        }
        self.weight() / total_atoms
    }

    /// Mean atomic number: sum(Z_i * amount_i) / sum(amount_i).
    pub fn mean_atomic_number(&self) -> f64 {
        let total_atoms = self.num_atoms();
        if total_atoms < 1e-12 {
            return 0.0;
        }
        self.species
            .iter()
            .map(|(sp, amt)| sp.element.atomic_number() as f64 * amt.abs())
            .sum::<f64>()
            / total_atoms
    }

    /// Molar mass of the reduced formula unit in g/mol.
    pub fn molar_mass_reduced(&self) -> Option<f64> {
        let factor = self.get_reduced_factor();
        if factor < 1e-12 {
            return None;
        }
        Some(self.weight() / factor)
    }

    /// Atomic fractions as a map: {element_symbol: fraction}.
    /// Preserves sign of amounts for composition arithmetic (e.g. deltas).
    pub fn atomic_fractions_map(&self) -> HashMap<String, f64> {
        let total = self.num_atoms();
        if total < 1e-12 {
            return HashMap::new();
        }
        let elem_comp = self.element_composition();
        elem_comp
            .species
            .iter()
            .map(|(sp, amt)| (sp.element.symbol().to_string(), *amt / total))
            .collect()
    }

    /// Unit cell composition as a map: {element_symbol: amount}.
    pub fn composition_unit_cell_map(&self) -> HashMap<String, f64> {
        let elem_comp = self.element_composition();
        elem_comp
            .species
            .iter()
            .map(|(sp, amt)| (sp.element.symbol().to_string(), *amt))
            .collect()
    }

    /// Reduced composition as a map with integer amounts.
    /// Returns None if amounts don't reduce to clean integers.
    pub fn composition_reduced_map(&self) -> Option<HashMap<String, i32>> {
        let elem_comp = self.element_composition();
        let gcd = elem_comp.gcd_of_amounts();
        if gcd < 1e-12 {
            return None;
        }
        let mut result = HashMap::new();
        for (sp, amt) in &elem_comp.species {
            let reduced = amt / gcd;
            let rounded = reduced.round();
            if (reduced - rounded).abs() > 1e-6
                || rounded < i32::MIN as f64
                || rounded > i32::MAX as f64
            {
                return None;
            }
            result.insert(sp.element.symbol().to_string(), rounded as i32);
        }
        Some(result)
    }

    /// Electronegativity difference threshold for ANX categorization.
    /// Elements within this difference from the min/max EN are grouped together.
    const EN_CATEGORY_THRESHOLD: f64 = 0.1;

    /// ICSD-style ANX formula. Returns None for ambiguous cases.
    ///
    /// Classification: if oxidation states present, cations=A, neutral=N, anions=X.
    /// Otherwise uses electronegativity: least electronegative=A, most=X.
    pub fn anx_formula(&self) -> Option<String> {
        let elem_comp = self.element_composition();
        if elem_comp.is_empty() {
            return None;
        }

        let has_oxi = self.species.keys().any(|sp| sp.oxidation_state.is_some());

        let mut categories: Vec<(char, f64)> = Vec::new();

        if has_oxi {
            // Categorize by oxidation state using raw amounts (not element-level GCD,
            // since self.species may have multiple entries per element with different
            // oxidation states). The final GCD reduction happens on category totals below.
            // Species with no oxidation state (None) or zero are classified as neutral 'N'.
            // This is intentional: when *some* species have oxidation states, those without
            // are assumed neutral rather than ambiguous.
            for (sp, amt) in &self.species {
                let cat = match sp.oxidation_state {
                    Some(oxi) if oxi > 0 => 'A',
                    Some(oxi) if oxi < 0 => 'X',
                    _ => 'N',
                };
                categories.push((cat, *amt));
            }
        } else {
            let gcd = elem_comp.gcd_of_amounts();
            if gcd < 1e-12 {
                return None;
            }
            // Pair each element with (EN, reduced_amount) for sorting and classification.
            // Return None if any element lacks electronegativity data (e.g. noble gases).
            let mut elems: Vec<(f64, f64)> = Vec::new();
            for (sp, amt) in &elem_comp.species {
                let en = sp.element.electronegativity()?;
                elems.push((en, amt / gcd));
            }

            if elems.len() < 2 {
                return None;
            }

            elems.sort_by(|left, right| {
                left.0
                    .partial_cmp(&right.0)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });

            let max_en = elems.last().unwrap().0;
            let min_en = elems.first().unwrap().0;
            if (max_en - min_en).abs() < Self::EN_CATEGORY_THRESHOLD {
                return None;
            }

            for &(en, amt) in &elems {
                let cat = if (en - max_en).abs() < Self::EN_CATEGORY_THRESHOLD {
                    'X'
                } else if (en - min_en).abs() < Self::EN_CATEGORY_THRESHOLD {
                    'A'
                } else {
                    'N'
                };
                categories.push((cat, amt));
            }
        }

        // Accumulate totals per category: [A, N, X]
        let mut totals = [0.0_f64; 3];
        for (cat, amt) in &categories {
            match cat {
                'A' => totals[0] += amt,
                'N' => totals[1] += amt,
                'X' => totals[2] += amt,
                _ => {}
            }
        }

        let positive: Vec<f64> = totals.iter().copied().filter(|val| *val > 0.0).collect();
        if positive.is_empty() {
            return None;
        }

        let cat_gcd = positive.iter().copied().reduce(gcd_float).unwrap_or(1.0);
        if cat_gcd < AMOUNT_TOLERANCE {
            return None;
        }

        let mut parts = Vec::new();
        for (total, label) in totals.iter().zip(["A", "N", "X"]) {
            if *total > 0.0 {
                let reduced = total / cat_gcd;
                let count = reduced.round() as i32;
                if count < 1 || (reduced - count as f64).abs() > 0.01 {
                    return None;
                }
                if count == 1 {
                    parts.push(label.to_string());
                } else {
                    parts.push(format!("{label}{count}"));
                }
            }
        }

        Some(parts.concat())
    }
}
