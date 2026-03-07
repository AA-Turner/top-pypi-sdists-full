//! PyComposition: OOP wrapper for Composition.

use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

use crate::composition::Composition;
use crate::python::helpers::{parse_comp, parse_element};

/// A chemical composition with formula parsing, reduction, and analysis.
///
/// Wraps the Rust Composition type to provide a Pythonic OOP interface
/// matching pymatgen conventions.
///
/// Examples:
///     >>> comp = Composition("Fe2O3")
///     >>> comp.reduced_formula
///     'Fe2O3'
///     >>> comp.num_atoms
///     5.0
///     >>> comp.weight
///     159.6882
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.composition", name = "Composition")]
pub struct PyComposition {
    inner: Composition,
}

impl PyComposition {
    /// Construct from an existing Rust Composition (for internal use by Structure, etc.).
    pub fn from_inner(inner: Composition) -> Self {
        Self { inner }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyComposition {
    /// Create a Composition from a formula string (e.g. "Fe2O3", "Na0.5Cl0.5").
    #[new]
    fn new(formula: &str) -> PyResult<Self> {
        Ok(Self::from_inner(parse_comp(formula)?))
    }

    // === Formula representations ===

    /// Unit cell formula (e.g. "Fe2 O3").
    #[getter]
    fn formula(&self) -> String {
        self.inner.formula()
    }

    /// Reduced formula (e.g. "Fe2O3").
    #[getter]
    fn reduced_formula(&self) -> String {
        self.inner.reduced_formula()
    }

    /// Anonymous formula (e.g. "A2B3").
    #[getter]
    fn anonymized_formula(&self) -> String {
        self.inner.anonymous_formula()
    }

    /// Hill formula (C and H first, then alphabetical).
    #[getter]
    fn hill_formula(&self) -> String {
        self.inner.hill_formula()
    }

    /// Alphabetical formula.
    #[getter]
    fn alphabetical_formula(&self) -> String {
        self.inner.alphabetical_formula()
    }

    /// Chemical system string (e.g. "Fe-O").
    #[getter]
    fn chemical_system(&self) -> String {
        self.inner.chemical_system()
    }

    /// ICSD-style ANX formula. None for ambiguous cases.
    #[getter]
    fn anx_formula(&self) -> Option<String> {
        self.inner.anx_formula()
    }

    // === Counts ===

    /// Total number of atoms.
    #[getter]
    fn num_atoms(&self) -> f64 {
        self.inner.num_atoms()
    }

    /// Number of unique elements.
    #[getter]
    fn num_elements(&self) -> usize {
        self.inner.num_elements()
    }

    /// Number of unique species (elements + oxidation states).
    #[getter]
    fn num_species(&self) -> usize {
        self.inner.num_species()
    }

    /// Number of reduced formula units per cell (Z).
    #[getter]
    fn num_formula_units(&self) -> Option<i32> {
        self.inner.num_formula_units()
    }

    /// Reduction factor (GCD of atom counts).
    #[getter]
    fn reduced_factor(&self) -> f64 {
        self.inner.get_reduced_factor()
    }

    // === Physical properties ===

    /// Total molecular weight in g/mol.
    #[getter]
    fn weight(&self) -> f64 {
        self.inner.weight()
    }

    /// Mean atomic mass in amu.
    #[getter]
    fn mean_atomic_mass(&self) -> f64 {
        self.inner.mean_atomic_mass()
    }

    /// Mean atomic number.
    #[getter]
    fn mean_atomic_number(&self) -> f64 {
        self.inner.mean_atomic_number()
    }

    /// Molar mass of the reduced formula unit (g/mol).
    #[getter]
    fn molar_mass_reduced(&self) -> Option<f64> {
        self.inner.molar_mass_reduced()
    }

    /// Average Pauling electronegativity.
    #[getter]
    fn average_electroneg(&self) -> Option<f64> {
        self.inner.average_electroneg()
    }

    /// Total number of electrons.
    #[getter]
    fn total_electrons(&self) -> f64 {
        self.inner.total_electrons()
    }

    // === Elements ===

    /// Sorted unique element symbols.
    #[getter]
    fn elements(&self) -> Vec<String> {
        let mut elems: Vec<String> = self
            .inner
            .unique_elements()
            .iter()
            .map(|elem| elem.symbol().to_string())
            .collect();
        elems.sort_unstable();
        elems
    }

    /// Whether this is a single-element composition.
    #[getter]
    fn is_element(&self) -> bool {
        self.inner.is_element()
    }

    /// Whether all amounts are non-negative.
    #[getter]
    fn valid(&self) -> bool {
        self.inner.is_valid()
    }

    // === Charge and oxidation ===

    /// Total charge. None if no oxidation states assigned.
    #[getter]
    fn charge(&self) -> Option<i32> {
        self.inner.charge()
    }

    /// Whether the composition is charge balanced.
    #[getter]
    fn is_charge_balanced(&self) -> Option<bool> {
        self.inner.is_charge_balanced()
    }

    // === Fraction methods ===

    /// Get atomic fraction of an element.
    fn get_atomic_fraction(&self, element: &str) -> PyResult<f64> {
        Ok(self
            .inner
            .get_atomic_fraction(crate::species::Species::neutral(parse_element(element)?)))
    }

    /// Get weight fraction of an element.
    fn get_wt_fraction(&self, element: &str) -> PyResult<f64> {
        Ok(self
            .inner
            .get_wt_fraction(crate::species::Species::neutral(parse_element(element)?)))
    }

    /// Atomic fractions as {element: fraction}.
    #[getter]
    fn atomic_fractions(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        Ok(self
            .inner
            .atomic_fractions_map()
            .into_pyobject(py)?
            .unbind())
    }

    /// Composition as {element: amount} dict.
    fn to_dict(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        Ok(self
            .inner
            .composition_unit_cell_map()
            .into_pyobject(py)?
            .unbind())
    }

    // === Derived compositions ===

    /// Reduced composition (lowest integer ratio).
    #[getter]
    fn reduced(&self) -> PyComposition {
        Self::from_inner(self.inner.reduced_composition())
    }

    /// Fractional composition (each amount divided by total, sums to 1).
    #[getter]
    fn fractional(&self) -> PyComposition {
        Self::from_inner(self.inner.fractional_composition())
    }

    /// Element-only composition (oxidation states stripped).
    #[getter]
    fn element_composition(&self) -> PyComposition {
        Self::from_inner(self.inner.element_composition())
    }

    /// Composition with charges removed.
    fn remove_charges(&self) -> Self {
        Self::from_inner(self.inner.remove_charges())
    }

    /// Remap elements (e.g. {"Fe": "Co"}).
    fn remap_elements(&self, mapping: HashMap<String, String>) -> PyResult<Self> {
        let mut elem_map = HashMap::new();
        for (from_sym, to_sym) in mapping {
            elem_map.insert(parse_element(&from_sym)?, parse_element(&to_sym)?);
        }
        Ok(Self::from_inner(self.inner.remap_elements(&elem_map)))
    }

    // === Comparison ===

    /// Whether two compositions are almost equal.
    #[pyo3(signature = (other, rel_tol = 1e-6, abs_tol = 1e-8))]
    fn almost_equals(&self, other: &Self, rel_tol: f64, abs_tol: f64) -> bool {
        self.inner.almost_equals(&other.inner, rel_tol, abs_tol)
    }

    /// Hash based on element composition (ignoring oxidation states).
    fn formula_hash(&self) -> u64 {
        self.inner.formula_hash()
    }

    /// Hash based on species (including oxidation states).
    fn species_hash(&self) -> u64 {
        self.inner.species_hash()
    }

    // === Dunder methods ===

    fn __str__(&self) -> String {
        self.inner.formula()
    }

    fn __repr__(&self) -> String {
        format!("Composition(\"{}\")", self.inner.reduced_formula())
    }

    /// Exact equality: same species and amounts at 1e-8 resolution
    /// (use almost_equals for custom tolerances).
    fn __eq__(&self, other: &Self) -> bool {
        self.inner == other.inner
    }

    fn __hash__(&self) -> u64 {
        use std::hash::{Hash, Hasher};
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        self.inner.hash(&mut hasher);
        hasher.finish()
    }

    fn __len__(&self) -> usize {
        self.inner.num_elements()
    }

    /// Combine two compositions.
    fn __add__(&self, other: &Self) -> Self {
        Self::from_inner(self.inner.clone() + other.inner.clone())
    }

    /// Subtract a composition.
    fn __sub__(&self, other: &Self) -> PyResult<Self> {
        self.inner
            .sub_checked(&other.inner)
            .map(Self::from_inner)
            .map_err(|err| PyValueError::new_err(err.to_string()))
    }

    /// Scale composition by a factor.
    fn __mul__(&self, factor: f64) -> PyResult<Self> {
        if !factor.is_finite() || factor < 0.0 {
            return Err(PyValueError::new_err(
                "Composition scale factor must be finite and non-negative",
            ));
        }
        Ok(Self::from_inner(self.inner.clone() * factor))
    }

    /// Divide composition by a factor.
    fn __truediv__(&self, factor: f64) -> PyResult<Self> {
        if !factor.is_finite() || factor < 0.0 {
            return Err(PyValueError::new_err(
                "Composition divisor must be finite and non-negative",
            ));
        }
        if factor < 1e-8 {
            return Err(PyValueError::new_err("Cannot divide composition by zero"));
        }
        Ok(Self::from_inner(self.inner.clone() / factor))
    }
}
