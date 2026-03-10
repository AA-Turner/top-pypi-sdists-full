use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pymethods;

use crate::cell_ops;
use crate::io::structure_to_pymatgen_json;
use crate::python::helpers::{SpacegroupInput, StructureJson, parse_struct, structure_to_pydict};

use super::{PyStructure, ferrox_err};

#[gen_stub_pymethods]
#[pymethods]
impl PyStructure {
    /// Create a new Structure from a JSON string or dict.
    #[new]
    fn new(structure: StructureJson) -> PyResult<Self> {
        Ok(Self::wrap(parse_struct(&structure)?))
    }

    /// Convert to a pymatgen-compatible dict.
    fn as_dict(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        Ok(structure_to_pydict(py, &self.inner)?.unbind())
    }

    /// Convert to a JSON string.
    fn to_json(&self) -> String {
        structure_to_pymatgen_json(&self.inner)
    }

    /// Construct from a pymatgen-compatible dict (alias for `Structure(dict)`).
    #[staticmethod]
    fn from_dict(structure: StructureJson) -> PyResult<Self> {
        Self::new(structure)
    }

    /// Create a copy of this structure.
    fn copy(&self) -> Self {
        Self::wrap(self.inner.clone())
    }

    // === Python dunder methods ===

    /// Readable summary matching pymatgen's `str(Structure)` format.
    fn __str__(&self) -> String {
        let comp = self.inner.composition();
        let lengths = self.inner.lattice.lengths();
        let angles = self.inner.lattice.angles();

        let mut out = format!(
            "Full Formula ({})\nReduced Formula: {}\n\
         abc   : {:>10.6} {:>10.6} {:>10.6}\n\
         angles: {:>10.6} {:>10.6} {:>10.6}\n\
         pbc   :       True       True       True\n\
         Sites ({})\n",
            comp.formula(),
            comp.reduced_formula(),
            lengths.x,
            lengths.y,
            lengths.z,
            angles.x,
            angles.y,
            angles.z,
            self.inner.num_sites(),
        );

        out.push_str("  #  SP        a      b      c\n");
        out.push_str("---  ------  -----  -----  -----\n");
        let species = self.inner.species_strings();
        for (idx, (sp, coord)) in species.iter().zip(&self.inner.frac_coords).enumerate() {
            out.push_str(&format!(
                "{:>3}  {:<6}  {:>5.3}  {:>5.3}  {:>5.3}\n",
                idx, sp, coord.x, coord.y, coord.z
            ));
        }
        out.pop(); // trailing newline
        out
    }

    fn __repr__(&self) -> String {
        let comp = self.inner.composition();
        format!(
            "Structure({}, {} sites, V={:.2} A^3)",
            comp.reduced_formula(),
            self.inner.num_sites(),
            self.inner.volume()
        )
    }

    fn __len__(&self) -> usize {
        self.inner.num_sites()
    }

    /// Structural equality using the built-in structure matcher.
    fn __eq__(&self, other: &Self) -> bool {
        self.inner.matches(&other.inner, false)
    }

    /// Access a site by index. Returns a dict with species, abc, and xyz.
    fn __getitem__(&self, py: Python<'_>, idx: isize) -> PyResult<Py<PyDict>> {
        let n_sites = self.inner.num_sites() as isize;
        let resolved = if idx < 0 { n_sites + idx } else { idx };
        if resolved < 0 || resolved >= n_sites {
            return Err(pyo3::exceptions::PyIndexError::new_err(format!(
                "site index {idx} out of range for structure with {n_sites} sites"
            )));
        }
        let site_idx = resolved as usize;
        let species = &self.inner.species_strings()[site_idx];
        let frac = &self.inner.frac_coords[site_idx];
        let cart = self.inner.cart_coords();
        let cart_coord = &cart[site_idx];

        let dict = PyDict::new(py);
        dict.set_item("species_string", species)?;
        dict.set_item("abc", [frac.x, frac.y, frac.z])?;
        dict.set_item("xyz", [cart_coord.x, cart_coord.y, cart_coord.z])?;
        Ok(dict.unbind())
    }

    // === Properties matching pymatgen conventions ===

    /// Unit cell formula (e.g. "Na4 Cl4").
    #[getter]
    fn formula(&self) -> String {
        self.inner.composition().formula()
    }

    /// Fractional coordinates of all sites as list of [a, b, c].
    #[getter]
    fn frac_coords(&self) -> Vec<[f64; 3]> {
        self.inner
            .frac_coords
            .iter()
            .map(|coord| [coord.x, coord.y, coord.z])
            .collect()
    }

    /// Lattice parameter a in Angstrom.
    #[getter]
    fn a(&self) -> f64 {
        self.inner.lattice.lengths().x
    }

    /// Lattice parameter b in Angstrom.
    #[getter]
    fn b(&self) -> f64 {
        self.inner.lattice.lengths().y
    }

    /// Lattice parameter c in Angstrom.
    #[getter]
    fn c(&self) -> f64 {
        self.inner.lattice.lengths().z
    }

    /// Lattice angle alpha in degrees.
    #[getter]
    fn alpha(&self) -> f64 {
        self.inner.lattice.angles().x
    }

    /// Lattice angle beta in degrees.
    #[getter]
    fn beta(&self) -> f64 {
        self.inner.lattice.angles().y
    }

    /// Lattice angle gamma in degrees.
    #[getter]
    fn gamma(&self) -> f64 {
        self.inner.lattice.angles().z
    }

    /// Create a structure from a named prototype (e.g. "fcc", "rocksalt", "perovskite").
    ///
    /// Supported prototypes: sc, fcc, bcc, hcp, diamond, rocksalt, perovskite,
    /// cscl, fluorite, antifluorite, zincblende, wurtzite.
    ///
    /// Args:
    ///     prototype: Name of the prototype structure
    ///     species: Element symbols for each symmetrically distinct site
    ///     a: Lattice parameter a (required for all prototypes)
    ///     b: Lattice parameter b (optional)
    ///     c: Lattice parameter c (required for hcp, wurtzite)
    #[staticmethod]
    #[pyo3(signature = (prototype, species, a, b = None, c = None))]
    fn from_prototype(
        prototype: &str,
        species: Vec<String>,
        a: f64,
        b: Option<f64>,
        c: Option<f64>,
    ) -> PyResult<Self> {
        let site_occs =
            crate::species::SiteOccupancy::parse_symbols(&species).map_err(ferrox_err)?;
        let inner = crate::structure::Structure::from_prototype(prototype, site_occs, a, b, c)
            .map_err(ferrox_err)?;
        Ok(Self::wrap(inner))
    }

    /// Create a structure from a space group, lattice, and asymmetric unit.
    ///
    /// Args:
    ///     sg: Space group as ITA number (1-230) or Hermann-Mauguin symbol (e.g. "Fm-3m")
    ///     lattice: 3x3 lattice matrix or [[a, b, c, alpha, beta, gamma]]
    ///     species: Element symbols for each symmetrically distinct site
    ///     coords: Fractional coordinates of each distinct site (Nx3 list)
    ///     tol: Tolerance for deduplicating equivalent sites (default: 1e-5)
    #[staticmethod]
    #[pyo3(signature = (sg, lattice, species, coords, tol = None))]
    fn from_spacegroup(
        sg: SpacegroupInput,
        lattice: Vec<Vec<f64>>,
        species: Vec<String>,
        coords: Vec<[f64; 3]>,
        tol: Option<f64>,
    ) -> PyResult<Self> {
        let lat = crate::python::structure::parse_lattice_input(&lattice)?;
        let site_occs =
            crate::species::SiteOccupancy::parse_symbols(&species).map_err(ferrox_err)?;
        let frac_coords: Vec<nalgebra::Vector3<f64>> = coords
            .iter()
            .map(|coord| nalgebra::Vector3::new(coord[0], coord[1], coord[2]))
            .collect();
        let inner =
            crate::structure::Structure::from_spacegroup(&sg.0, lat, site_occs, frac_coords, tol)
                .map_err(ferrox_err)?;
        Ok(Self::wrap(inner))
    }

    // === Core properties ===

    /// Number of atomic sites in the structure.
    #[getter]
    fn num_sites(&self) -> usize {
        self.inner.num_sites()
    }

    /// Whether all sites are ordered (single species per site).
    #[getter]
    fn is_ordered(&self) -> bool {
        self.inner.is_ordered()
    }

    /// Volume of the unit cell in ų.
    #[getter]
    fn volume(&self) -> f64 {
        self.inner.volume()
    }

    /// Mass density in g/cm³. Returns None for non-periodic structures.
    #[getter]
    fn density(&self) -> Option<f64> {
        self.inner.density()
    }

    // === Disorder analysis ===

    /// True if any site contains more than one species.
    #[getter]
    fn has_substitutional_disorder(&self) -> bool {
        self.inner.has_substitutional_disorder()
    }

    /// True if any site has total occupancy < 1 - tol.
    #[pyo3(signature = (tol = 1e-3))]
    fn has_vacancy_disorder(&self, tol: f64) -> bool {
        self.inner.has_vacancy_disorder(tol)
    }

    /// Maximum number of distinct species on any single site.
    #[getter]
    fn max_species_per_site(&self) -> usize {
        self.inner.max_species_per_site()
    }

    /// Minimum total occupancy across all sites.
    #[getter]
    fn min_total_occupancy_per_site(&self) -> f64 {
        self.inner.min_total_occupancy_per_site()
    }

    /// Number of disordered sites (multiple species or partial occupancy).
    #[pyo3(signature = (tol = 1e-3))]
    fn num_disordered_sites(&self, tol: f64) -> usize {
        self.inner.num_disordered_sites(tol)
    }

    /// Whether any species has an explicit oxidation state.
    #[getter]
    fn has_oxidation_states(&self) -> bool {
        self.inner.has_oxidation_states()
    }

    // === Composition ===

    /// Number of reduced-formula units per cell (Z). None if non-integer.
    #[getter]
    fn num_formula_units(&self) -> Option<i32> {
        self.inner.composition().num_formula_units()
    }

    /// Mean atomic mass in amu.
    #[getter]
    fn mean_atomic_mass(&self) -> f64 {
        self.inner.composition().mean_atomic_mass()
    }

    /// Mean atomic number.
    #[getter]
    fn mean_atomic_number(&self) -> f64 {
        self.inner.composition().mean_atomic_number()
    }

    /// Molar mass of the reduced formula unit (g/mol).
    #[getter]
    fn molar_mass_reduced(&self) -> Option<f64> {
        self.inner.composition().molar_mass_reduced()
    }

    /// Total molar mass of the unit cell (g/mol).
    #[getter]
    fn molar_mass_unit_cell(&self) -> f64 {
        self.inner.composition().weight()
    }

    /// Reduced formula string.
    #[getter]
    fn reduced_formula(&self) -> String {
        self.inner.composition().reduced_formula()
    }

    /// Anonymous formula (e.g. "A2B3").
    #[getter]
    fn anonymized_formula(&self) -> String {
        self.inner.composition().anonymous_formula()
    }

    /// Chemical system (e.g. "Fe-O").
    #[getter]
    fn chemical_system(&self) -> String {
        self.inner.composition().chemical_system()
    }

    /// Number of unique elements.
    #[getter]
    fn num_elements(&self) -> usize {
        self.inner.composition().num_elements()
    }

    /// Sorted unique element symbols.
    #[getter]
    fn elements(&self) -> Vec<String> {
        let mut elems: Vec<String> = self
            .inner
            .composition()
            .unique_elements()
            .iter()
            .map(|elem| elem.symbol().to_string())
            .collect();
        elems.sort_unstable();
        elems
    }

    /// ICSD-style ANX formula. None for ambiguous cases.
    /// Uses species_composition() to preserve oxidation states for classification.
    #[getter]
    fn anx_formula(&self) -> Option<String> {
        self.inner.species_composition().anx_formula()
    }

    // === Lattice ===

    /// Atomic density in sites/ų.
    #[getter]
    fn atomic_density(&self) -> Option<f64> {
        self.inner.atomic_density()
    }

    /// Volume per atomic site in ų.
    #[getter]
    fn volume_per_site(&self) -> Option<f64> {
        self.inner.volume_per_site()
    }

    // === Niggli G6 ===

    /// Niggli G6 representation [a², b², c², 2bc, 2ac, 2ab].
    #[pyo3(signature = (tol = 1e-5))]
    fn get_niggli_g6(&self, tol: f64) -> PyResult<[f64; 6]> {
        cell_ops::niggli_g6(&self.inner.lattice, tol)
            .map(|g6| g6.as_array())
            .map_err(ferrox_err)
    }

    /// Selling S6 representation [bc, ac, ab, ad, bd, cd] (canonicalized).
    #[pyo3(signature = (tol = 1e-5))]
    fn get_selling_s6(&self, tol: f64) -> PyResult<[f64; 6]> {
        cell_ops::selling_s6(&self.inner.lattice, tol)
            .map(|s6| s6.as_array())
            .map_err(ferrox_err)
    }
}
