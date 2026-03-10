use crate::composition::{AMOUNT_TOLERANCE, Composition, parse_formula_recursive};
use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::species::Species;
use indexmap::IndexMap;
use std::collections::HashSet;

impl Composition {
    // =========================================================================
    // Constructors
    // =========================================================================

    /// Create a new composition from species-amount pairs.
    ///
    /// Zero and negative amounts are filtered out (since allow_negative defaults to false).
    pub fn new(species: impl IntoIterator<Item = (Species, f64)>) -> Self {
        let species: IndexMap<Species, f64> = species
            .into_iter()
            .filter(|(_, amt)| *amt > AMOUNT_TOLERANCE)
            .collect();
        Self {
            species,
            allow_negative: false,
        }
    }

    /// Create a new composition from element-amount pairs (no oxidation states).
    ///
    /// This is a convenience constructor that converts Elements to neutral Species.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::composition::Composition;
    /// use ferrox::element::Element;
    ///
    /// let comp = Composition::from_elements([
    ///     (Element::Fe, 2.0),
    ///     (Element::O, 3.0),
    /// ]);
    /// assert_eq!(comp.reduced_formula(), "Fe2O3");
    /// assert_eq!(comp.num_atoms(), 5.0);
    /// ```
    pub fn from_elements(elements: impl IntoIterator<Item = (Element, f64)>) -> Self {
        Self::new(
            elements
                .into_iter()
                .map(|(el, amt)| (Species::neutral(el), amt)),
        )
    }

    /// Parse a composition from a formula string.
    ///
    /// Supports:
    /// - Simple formulas: "Fe2O3", "NaCl", "H2O"
    /// - Parentheses: "Ca3(PO4)2", "Mg(OH)2"
    /// - Brackets (converted to parentheses): "[Cu(NH3)4]SO4"
    /// - Metallofullerene syntax (@ stripped): "Y3N@C80"
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::composition::Composition;
    ///
    /// let comp = Composition::from_formula("LiFePO4").unwrap();
    /// assert_eq!(comp.num_atoms(), 7.0);
    ///
    /// let comp2 = Composition::from_formula("Ca3(PO4)2").unwrap();
    /// assert_eq!(comp2.num_atoms(), 13.0);  // 3 + 2 + 8
    /// ```
    pub fn from_formula(formula: &str) -> Result<Self> {
        let formula = formula.trim();
        if formula.is_empty() {
            return Err(FerroxError::ParseError {
                path: "formula".into(),
                reason: "Empty formula string".into(),
            });
        }

        // Preprocess: strip @, convert brackets to parentheses
        let formula = formula
            .replace('@', "")
            .replace('[', "(")
            .replace(']', ")")
            .replace('{', "(")
            .replace('}', ")");

        let species_amounts = parse_formula_recursive(&formula)?;
        Ok(Self::new(species_amounts))
    }

    /// Builder: set whether to allow negative amounts.
    pub fn with_allow_negative(mut self, allow: bool) -> Self {
        self.allow_negative = allow;
        self
    }

    // =========================================================================
    // Basic Accessors
    // =========================================================================

    /// Get the amount of a species in this composition.
    ///
    /// Returns 0.0 if the species is not present.
    pub fn get(&self, species: impl Into<Species>) -> f64 {
        let sp = species.into();
        self.species.get(&sp).copied().unwrap_or(0.0)
    }

    /// Get the total amount summed across all oxidation states of an element.
    ///
    /// For example, if composition has Fe2+ (2.0) and Fe3+ (1.0), this returns 3.0 for Fe.
    pub fn get_element_total(&self, element: Element) -> f64 {
        self.species
            .iter()
            .filter(|(sp, _)| sp.element == element)
            .map(|(_, amt)| amt)
            .sum()
    }

    /// Get the total number of atoms.
    pub fn num_atoms(&self) -> f64 {
        self.species.values().map(|v| v.abs()).sum()
    }

    /// Get the number of unique species.
    pub fn num_species(&self) -> usize {
        self.species.len()
    }

    /// Get the number of unique elements (ignoring oxidation states).
    pub fn num_elements(&self) -> usize {
        self.unique_elements().len()
    }

    /// Check if composition is empty.
    pub fn is_empty(&self) -> bool {
        self.species.is_empty()
    }

    /// Check if composition represents a single element.
    pub fn is_element(&self) -> bool {
        self.unique_elements().len() == 1
    }

    /// Check if composition is valid (no negative amounts unless allowed).
    pub fn is_valid(&self) -> bool {
        self.allow_negative || self.species.values().all(|&v| v >= -AMOUNT_TOLERANCE)
    }

    /// Get unique elements (ignoring oxidation states).
    pub fn unique_elements(&self) -> HashSet<Element> {
        self.species.keys().map(|sp| sp.element).collect()
    }

    /// Get all species as a vector.
    pub fn species_list(&self) -> Vec<Species> {
        self.species.keys().copied().collect()
    }

    /// Get all elements as a vector (may contain duplicates if multiple oxidation states).
    pub fn elements(&self) -> Vec<Element> {
        self.species.keys().map(|sp| sp.element).collect()
    }

    /// Iterate over (species, amount) pairs.
    pub fn iter(&self) -> impl Iterator<Item = (&Species, &f64)> {
        self.species.iter()
    }

    // =========================================================================
    // Chemical System
    // =========================================================================

    /// Get the chemical system string (e.g., "Fe-O" for Fe2O3).
    ///
    /// Elements are sorted alphabetically and joined by dashes.
    /// This format is commonly used as database keys.
    pub fn chemical_system(&self) -> String {
        let mut symbols: Vec<&str> = self.unique_elements().iter().map(|e| e.symbol()).collect();
        symbols.sort();
        symbols.join("-")
    }

    /// Get the set of element symbols in the composition.
    pub fn chemical_system_set(&self) -> HashSet<String> {
        self.unique_elements()
            .iter()
            .map(|e| e.symbol().to_string())
            .collect()
    }

    // =========================================================================
    // Weight and Fraction Calculations
    // =========================================================================

    /// Get the total molecular weight in atomic mass units.
    pub fn weight(&self) -> f64 {
        self.species
            .iter()
            .map(|(sp, amt)| sp.element.atomic_mass() * amt.abs())
            .sum()
    }

    /// Get the atomic fraction of a species.
    ///
    /// Returns the amount of the species divided by total atoms.
    pub fn get_atomic_fraction(&self, species: impl Into<Species>) -> f64 {
        let total = self.num_atoms();
        if total < AMOUNT_TOLERANCE {
            return 0.0;
        }
        self.get(species).abs() / total
    }

    /// Get the weight fraction of a species.
    ///
    /// Returns the mass contribution of the species divided by total weight.
    pub fn get_wt_fraction(&self, species: impl Into<Species>) -> f64 {
        let total_weight = self.weight();
        if total_weight < AMOUNT_TOLERANCE {
            return 0.0;
        }
        let sp = species.into();
        let el_mass = sp.element.atomic_mass() * self.get(sp).abs();
        el_mass / total_weight
    }

    /// Get the fractional composition (amounts normalized to sum to 1).
    pub fn fractional_composition(&self) -> Self {
        let total = self.num_atoms();
        if total < AMOUNT_TOLERANCE {
            return self.clone();
        }
        self.clone() / total
    }

    /// Get average electronegativity weighted by amount.
    ///
    /// Returns None if any species lacks electronegativity data.
    pub fn average_electroneg(&self) -> Option<f64> {
        if self.is_empty() {
            return None;
        }
        let mut total_en = 0.0;
        let mut total_atoms = 0.0;
        for (sp, amt) in &self.species {
            let en = sp.electronegativity()?; // Return None if any species lacks EN
            total_en += en * amt.abs();
            total_atoms += amt.abs();
        }
        if total_atoms < AMOUNT_TOLERANCE {
            return None;
        }
        Some(total_en / total_atoms)
    }

    /// Get total number of electrons in the composition.
    pub fn total_electrons(&self) -> f64 {
        self.species
            .iter()
            .map(|(sp, amt)| sp.element.atomic_number() as f64 * amt.abs())
            .sum()
    }
}
