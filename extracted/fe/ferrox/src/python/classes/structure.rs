//! PyStructure: OOP wrapper for Structure with MoyoDataset caching.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

use moyo::MoyoDataset;
use nalgebra::{Matrix3, Vector3};

use crate::cell_ops;
use crate::distortions;
use crate::io::structure_to_pymatgen_json;
use crate::structure::{
    ReductionAlgo, SymmOp, geometric_crystal_class_from_hall, laue_group_from_point_group,
    point_group_symbol, spacegroup_to_crystal_system, spacegroup_type_from_number,
};

use crate::analysis::magnetism::MagneticAnalysis;
use crate::python::helpers::{
    SpacegroupInput, StructureJson, mat3_to_array, parse_element, parse_reduction_algo,
    parse_struct, props_to_pydict, py_to_json_value, structure_to_pydict,
};

use super::composition::PyComposition;
use super::lattice::PyLattice;

/// Set multiple dict keys to None.
fn set_none_keys(dict: &Bound<'_, PyDict>, keys: &[&str]) -> PyResult<()> {
    let none = dict.py().None();
    for key in keys {
        dict.set_item(*key, &none)?;
    }
    Ok(())
}

/// Build a histogram of Wyckoff letter occurrences.
fn wyckoff_histogram(wyckoffs: &[char]) -> HashMap<String, usize> {
    let mut hist = HashMap::new();
    for wyk in wyckoffs {
        *hist.entry(wyk.to_string()).or_default() += 1;
    }
    hist
}

/// Write MagneticAnalysis fields into a PyDict.
fn write_mag_analysis(dict: &Bound<'_, PyDict>, mag: &MagneticAnalysis) -> PyResult<()> {
    dict.set_item("has_magmoms", mag.has_magmoms)?;
    dict.set_item("is_magnetic", mag.is_magnetic)?;
    dict.set_item("magnetic_ordering", mag.ordering.map(|ord| ord.as_str()))?;
    dict.set_item("magmoms", &mag.magmoms)?;
    dict.set_item("total_magmom", mag.total_magmom)?;
    dict.set_item("max_abs_magmom", mag.max_abs_magmom)?;
    dict.set_item("num_magnetic_sites", mag.num_magnetic_sites)?;
    dict.set_item("num_unique_magnetic_sites", mag.num_unique_magnetic_sites)?;
    dict.set_item("types_of_magnetic_species", &mag.types_of_magnetic_species)?;
    dict.set_item("total_magnetization", mag.total_magnetization)?;
    dict.set_item(
        "total_magnetization_normalized_vol",
        mag.total_magnetization_normalized_vol,
    )?;
    dict.set_item(
        "total_magnetization_normalized_formula_units",
        mag.total_magnetization_normalized_formula_units,
    )?;
    Ok(())
}

/// A Structure with cached symmetry analysis for efficient property access.
///
/// Parses the structure JSON once on construction, and caches the MoyoDataset
/// (keyed by symprec) so that repeated symmetry queries are fast.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.structure", name = "Structure")]
pub struct PyStructure {
    inner: crate::structure::Structure,
    cached_dataset: Mutex<Option<(f64, Arc<MoyoDataset>)>>,
}

/// Convert any FerroxError to PyValueError.
fn ferrox_err(err: impl std::fmt::Display) -> PyErr {
    PyValueError::new_err(err.to_string())
}

/// Accept either [a, b, c] diagonal scaling or a 3x3 transformation matrix.
enum SupercellInput {
    Diag([i32; 3]),
    Matrix([[i32; 3]; 3]),
}

impl pyo3_stub_gen::PyStubType for SupercellInput {
    fn type_input() -> pyo3_stub_gen::TypeInfo {
        pyo3_stub_gen::TypeInfo::builtin("Sequence[int] | Sequence[Sequence[int]]")
    }
    fn type_output() -> pyo3_stub_gen::TypeInfo {
        Self::type_input()
    }
}

impl<'a, 'py> pyo3::FromPyObject<'a, 'py> for SupercellInput {
    type Error = PyErr;

    fn extract(ob: pyo3::Borrowed<'a, 'py, pyo3::PyAny>) -> PyResult<Self> {
        if let Ok(diag) = ob.extract::<[i32; 3]>() {
            return Ok(Self::Diag(diag));
        }
        if let Ok(matrix) = ob.extract::<[[i32; 3]; 3]>() {
            return Ok(Self::Matrix(matrix));
        }
        Err(PyValueError::new_err(
            "scaling must be [a, b, c] (diagonal) or [[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]] (3x3 matrix)",
        ))
    }
}

// === Internal helpers (not exposed to Python) ===

impl PyStructure {
    /// Wrap a Rust Structure into a PyStructure (fresh symmetry cache).
    fn wrap(inner: crate::structure::Structure) -> Self {
        Self {
            inner,
            cached_dataset: Mutex::new(None),
        }
    }

    fn wrap_many(structures: Vec<crate::structure::Structure>) -> Vec<Self> {
        structures.into_iter().map(Self::wrap).collect()
    }

    fn parse_neutral_species_list(
        species_symbols: &[String],
    ) -> PyResult<Vec<crate::species::Species>> {
        species_symbols
            .iter()
            .map(|symbol| Ok(crate::species::Species::neutral(parse_element(symbol)?)))
            .collect()
    }

    /// Get or compute the cached symmetry dataset (cheap Arc clone on hit).
    fn _dataset(&self, symprec: f64) -> PyResult<Arc<MoyoDataset>> {
        let mut cache = self.cached_dataset.lock().map_err(ferrox_err)?;
        if let Some((cached_prec, ref ds)) = *cache
            && (cached_prec - symprec).abs() < 1e-12
        {
            return Ok(Arc::clone(ds));
        }
        let ds = Arc::new(
            self.inner
                .get_symmetry_dataset(symprec)
                .map_err(ferrox_err)?,
        );
        *cache = Some((symprec, Arc::clone(&ds)));
        Ok(ds)
    }

    /// Look up SpacegroupTypeInfo from the cached dataset.
    fn _spg_type_info(&self, symprec: f64) -> PyResult<crate::structure::SpacegroupTypeInfo> {
        let ds = self._dataset(symprec)?;
        spacegroup_type_from_number(ds.number).map_err(ferrox_err)
    }
}

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

    // === Symmetry (using cached dataset) ===

    /// Space group number (1-230).
    #[pyo3(signature = (symprec = 0.01))]
    fn get_spacegroup_number(&self, symprec: f64) -> PyResult<i32> {
        Ok(self._dataset(symprec)?.number)
    }

    /// Hermann-Mauguin short symbol.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_spacegroup_symbol(&self, symprec: f64) -> PyResult<String> {
        Ok(self._dataset(symprec)?.hm_symbol.clone())
    }

    /// Hall number (1-530).
    #[pyo3(signature = (symprec = 0.01))]
    fn get_hall_number(&self, symprec: f64) -> PyResult<i32> {
        Ok(self._dataset(symprec)?.hall_number)
    }

    /// Crystal system string.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_crystal_system(&self, symprec: f64) -> PyResult<String> {
        let ds = self._dataset(symprec)?;
        Ok(spacegroup_to_crystal_system(ds.number).to_string())
    }

    /// Pearson symbol (e.g. "cF8").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_pearson_symbol(&self, symprec: f64) -> PyResult<String> {
        Ok(self._dataset(symprec)?.pearson_symbol.clone())
    }

    /// Bravais class (e.g. "cF", "tI", "oP").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_bravais_class(&self, symprec: f64) -> PyResult<String> {
        Ok(self._spg_type_info(symprec)?.bravais_class.to_string())
    }

    /// Lattice system (e.g. "cubic", "hexagonal").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_lattice_system(&self, symprec: f64) -> PyResult<String> {
        Ok(self._spg_type_info(symprec)?.lattice_system.to_string())
    }

    /// Crystal family (e.g. "cubic", "hexagonal").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_crystal_family(&self, symprec: f64) -> PyResult<String> {
        Ok(self._spg_type_info(symprec)?.crystal_family.to_string())
    }

    /// Whether centrosymmetric.
    #[pyo3(signature = (symprec = 0.01))]
    fn is_centrosymmetric(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_centrosymmetric)
    }

    /// Whether polar.
    #[pyo3(signature = (symprec = 0.01))]
    fn is_polar(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_polar)
    }

    /// Whether chiral (Sohncke group).
    #[pyo3(signature = (symprec = 0.01))]
    fn is_chiral(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_chiral)
    }

    /// Whether piezoelectricity is symmetry-allowed.
    /// Non-centrosymmetric except point group 432 (O), whose high symmetry
    /// forces all piezoelectric tensor coefficients to zero.
    #[pyo3(signature = (symprec = 0.01))]
    fn is_piezoelectric_allowed(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_piezoelectric_allowed)
    }

    /// Whether SHG is symmetry-allowed (non-centrosymmetric).
    #[pyo3(signature = (symprec = 0.01))]
    fn is_shg_allowed(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_shg_allowed)
    }

    /// Number of symmetry operations.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_num_symmetry_operations(&self, symprec: f64) -> PyResult<usize> {
        Ok(self._dataset(symprec)?.operations.len())
    }

    /// Number of symmetry-unique sites.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_num_unique_sites(&self, symprec: f64) -> PyResult<usize> {
        let ds = self._dataset(symprec)?;
        Ok(ds.orbits.iter().collect::<HashSet<_>>().len())
    }

    /// Wyckoff letters for each site.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_wyckoff_letters(&self, symprec: f64) -> PyResult<Vec<String>> {
        let ds = self._dataset(symprec)?;
        Ok(ds.wyckoffs.iter().map(|ch| ch.to_string()).collect())
    }

    /// Wyckoff histogram: {letter: count}.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_wyckoff_histogram(&self, py: Python<'_>, symprec: f64) -> PyResult<Py<PyDict>> {
        let ds = self._dataset(symprec)?;
        Ok(wyckoff_histogram(&ds.wyckoffs).into_pyobject(py)?.unbind())
    }

    /// Site symmetry symbols.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_site_symmetry_symbols(&self, symprec: f64) -> PyResult<Vec<String>> {
        let ds = self._dataset(symprec)?;
        Ok(ds.site_symmetry_symbols.clone())
    }

    // === Magnetism ===

    /// Magnetic analysis results as a dict.
    #[pyo3(signature = (threshold = 0.05, symprec = 0.01))]
    fn get_magnetic_analysis(
        &self,
        py: Python<'_>,
        threshold: f64,
        symprec: f64,
    ) -> PyResult<Py<PyDict>> {
        let dataset = self._dataset(symprec).ok();
        let analysis = self
            .inner
            .magnetic_analysis(threshold, dataset.as_ref().map(|ds| &ds.orbits[..]));
        let dict = PyDict::new(py);
        write_mag_analysis(&dict, &analysis)?;
        Ok(dict.unbind())
    }

    // === Batch metadata ===

    /// Get all structure metadata as a comprehensive dict.
    ///
    /// Computes the symmetry dataset once and extracts all fields in a single pass.
    #[pyo3(signature = (symprec = 0.01, reduce_tol = 1e-5, mag_threshold = 0.05, disorder_tol = 1e-3))]
    fn get_all_metadata(
        &self,
        py: Python<'_>,
        symprec: f64,
        reduce_tol: f64,
        mag_threshold: f64,
        disorder_tol: f64,
    ) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        let comp = self.inner.composition();
        let species_comp = self.inner.species_composition();

        // Core
        dict.set_item("is_ordered", self.inner.is_ordered())?;
        dict.set_item("num_sites", self.inner.num_sites())?;
        dict.set_item("num_formula_units", comp.num_formula_units())?;

        // Composition
        dict.set_item("reduced_formula", comp.reduced_formula())?;
        dict.set_item("anonymized_formula", comp.anonymous_formula())?;
        dict.set_item("formula_unit_cell", comp.formula())?;
        dict.set_item("chemical_system", comp.chemical_system())?;
        dict.set_item("num_elements", comp.num_elements())?;
        dict.set_item("mean_atomic_mass", comp.mean_atomic_mass())?;
        dict.set_item("mean_atomic_number", comp.mean_atomic_number())?;
        dict.set_item("molar_mass_reduced", comp.molar_mass_reduced())?;
        dict.set_item("molar_mass_unit_cell", comp.weight())?;
        dict.set_item("anx_formula", species_comp.anx_formula())?;

        // Elements
        let mut elems: Vec<String> = comp
            .unique_elements()
            .iter()
            .map(|elem| elem.symbol().to_string())
            .collect();
        elems.sort_unstable();
        dict.set_item("elements", elems)?;

        // Composition maps
        dict.set_item("atomic_fractions", comp.atomic_fractions_map())?;
        dict.set_item("composition_unit_cell", comp.composition_unit_cell_map())?;
        dict.set_item("composition_reduced", comp.composition_reduced_map())?;

        // Disorder
        dict.set_item(
            "has_substitutional_disorder",
            self.inner.has_substitutional_disorder(),
        )?;
        dict.set_item(
            "has_vacancy_disorder",
            self.inner.has_vacancy_disorder(disorder_tol),
        )?;
        dict.set_item("max_species_per_site", self.inner.max_species_per_site())?;
        dict.set_item(
            "min_total_occupancy_per_site",
            self.inner.min_total_occupancy_per_site(),
        )?;
        dict.set_item(
            "num_disordered_sites",
            self.inner.num_disordered_sites(disorder_tol),
        )?;

        // Oxidation (reuse species_comp from above)
        let has_oxi = self.inner.has_oxidation_states();
        dict.set_item("has_oxidation_states", has_oxi)?;
        if has_oxi {
            dict.set_item("composition_charge", species_comp.charge())?;
            dict.set_item("is_charge_neutral", species_comp.is_charge_balanced())?;
        } else {
            dict.set_item("composition_charge", py.None())?;
            dict.set_item("is_charge_neutral", py.None())?;
        }

        // Lattice
        let lengths = self.inner.lattice.lengths();
        let angles = self.inner.lattice.angles();
        dict.set_item("volume", self.inner.volume())?;
        dict.set_item("density", self.inner.density())?;
        dict.set_item("atomic_density", self.inner.atomic_density())?;
        dict.set_item("volume_per_site", self.inner.volume_per_site())?;
        dict.set_item("lattice_a", lengths.x)?;
        dict.set_item("lattice_b", lengths.y)?;
        dict.set_item("lattice_c", lengths.z)?;
        dict.set_item("lattice_alpha", angles.x)?;
        dict.set_item("lattice_beta", angles.y)?;
        dict.set_item("lattice_gamma", angles.z)?;

        dict.set_item("lattice_matrix", mat3_to_array(self.inner.lattice.matrix()))?;

        // Niggli G6
        let g6_keys = [
            "niggli_g6_a2",
            "niggli_g6_b2",
            "niggli_g6_c2",
            "niggli_g6_2bc",
            "niggli_g6_2ac",
            "niggli_g6_2ab",
        ];
        match cell_ops::niggli_g6(&self.inner.lattice, reduce_tol) {
            Ok(g6) => {
                for (key, val) in g6_keys.iter().zip(g6.as_array()) {
                    dict.set_item(*key, val)?;
                }
            }
            Err(_) => set_none_keys(&dict, &g6_keys)?,
        }

        // Selling S6
        let s6_keys = [
            "selling_s6_bc",
            "selling_s6_ac",
            "selling_s6_ab",
            "selling_s6_ad",
            "selling_s6_bd",
            "selling_s6_cd",
        ];
        match cell_ops::selling_s6(&self.inner.lattice, reduce_tol) {
            Ok(s6) => {
                for (key, val) in s6_keys.iter().zip(s6.as_array()) {
                    dict.set_item(*key, val)?;
                }
            }
            Err(_) => set_none_keys(&dict, &s6_keys)?,
        }

        // Symmetry (single dataset computation, reuse for magnetism + prototype).
        // SYM_KEYS enumerates every key this block writes so the fallback path
        // can set them all to None in one call.
        const SYM_KEYS: &[&str] = &[
            "spacegroup_number",
            "spacegroup_hm_short",
            "hall_number",
            "pearson_symbol",
            "crystal_system",
            "num_symmetry_operations",
            "wyckoffs",
            "site_symmetry_symbols",
            "num_unique_sites",
            "wyckoff_histogram",
            "point_group",
            "laue_group",
            "is_centrosymmetric",
            "is_polar",
            "is_chiral",
            "is_piezoelectric_allowed",
            "is_shg_allowed",
            "hall_symbol",
            "arithmetic_crystal_class_number",
            "arithmetic_crystal_class_symbol",
            "bravais_class",
            "lattice_system",
            "crystal_family",
            "std_linear",
            "std_origin_shift",
            "std_rotation_matrix",
            "mapping_std_prim",
        ];
        let dataset = self._dataset(symprec).ok();
        if let Some(ref ds) = dataset {
            dict.set_item("spacegroup_number", ds.number)?;
            dict.set_item("spacegroup_hm_short", &ds.hm_symbol)?;
            dict.set_item("hall_number", ds.hall_number)?;
            dict.set_item("pearson_symbol", &ds.pearson_symbol)?;
            dict.set_item("crystal_system", spacegroup_to_crystal_system(ds.number))?;
            dict.set_item("num_symmetry_operations", ds.operations.len())?;

            // Wyckoff
            let wyckoff_strs: Vec<String> = ds.wyckoffs.iter().map(|ch| ch.to_string()).collect();
            dict.set_item("wyckoffs", &wyckoff_strs)?;
            dict.set_item("site_symmetry_symbols", &ds.site_symmetry_symbols)?;

            let unique_sites = ds.orbits.iter().collect::<HashSet<_>>().len();
            dict.set_item("num_unique_sites", unique_sites)?;

            // Wyckoff histogram
            dict.set_item("wyckoff_histogram", wyckoff_histogram(&ds.wyckoffs))?;

            // Point group + SpacegroupTypeInfo
            if let Ok(info) = spacegroup_type_from_number(ds.number) {
                dict.set_item("point_group", info.point_group)?;
                dict.set_item("laue_group", info.laue_group)?;
                dict.set_item("is_centrosymmetric", info.is_centrosymmetric)?;
                dict.set_item("is_polar", info.is_polar)?;
                dict.set_item("is_chiral", info.is_chiral)?;
                dict.set_item("is_piezoelectric_allowed", info.is_piezoelectric_allowed)?;
                dict.set_item("is_shg_allowed", info.is_shg_allowed)?;
                dict.set_item("hall_symbol", info.hall_symbol)?;
                dict.set_item(
                    "arithmetic_crystal_class_number",
                    info.arithmetic_crystal_class_number,
                )?;
                dict.set_item(
                    "arithmetic_crystal_class_symbol",
                    info.arithmetic_crystal_class_symbol,
                )?;
                dict.set_item("bravais_class", info.bravais_class)?;
                dict.set_item("lattice_system", info.lattice_system)?;
                dict.set_item("crystal_family", info.crystal_family)?;
            }

            // Transformation matrices
            dict.set_item("std_linear", mat3_to_array(&ds.std_linear))?;
            let shift = &ds.std_origin_shift;
            dict.set_item("std_origin_shift", [shift.x, shift.y, shift.z])?;
            dict.set_item(
                "std_rotation_matrix",
                mat3_to_array(&ds.std_rotation_matrix),
            )?;
            dict.set_item("mapping_std_prim", &ds.mapping_std_prim)?;
        } else {
            set_none_keys(&dict, SYM_KEYS)?;
        }

        // Magnetism (reuse orbits from symmetry dataset above)
        let orbits = dataset.as_ref().map(|ds| &ds.orbits[..]);
        let mag = self.inner.magnetic_analysis(mag_threshold, orbits);
        write_mag_analysis(&dict, &mag)?;

        // Prototype label (reuse dataset to avoid recomputing symmetry)
        const PROTO_KEYS: &[&str] = &[
            "protostructure_label",
            "prototype_method",
            "prototype_symprec",
        ];
        let pre_proto_count = dict.len();
        if let Some(label) = dataset
            .as_ref()
            .and_then(|ds| self.inner.protostructure_label_from_dataset(ds).ok())
        {
            dict.set_item("protostructure_label", &label)?;
            dict.set_item("prototype_method", "moyo")?;
            dict.set_item("prototype_symprec", symprec)?;
        } else {
            set_none_keys(&dict, PROTO_KEYS)?;
        }
        debug_assert_eq!(
            dict.len() - pre_proto_count,
            PROTO_KEYS.len(),
            "PROTO_KEYS has {} entries but {} keys were written",
            PROTO_KEYS.len(),
            dict.len() - pre_proto_count,
        );

        Ok(dict.unbind())
    }

    // === Prototype labels ===

    /// Get AFLOW-style protostructure label.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_protostructure_label(&self, symprec: f64) -> PyResult<String> {
        self.inner
            .get_protostructure_label(symprec)
            .map_err(ferrox_err)
    }

    /// Point group symbol (e.g. "m-3m", "4/mmm").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_point_group(&self, symprec: f64) -> PyResult<&'static str> {
        let ds = self._dataset(symprec)?;
        let gcc = geometric_crystal_class_from_hall(ds.hall_number).map_err(ferrox_err)?;
        Ok(point_group_symbol(gcc))
    }

    // === Structure operations ===

    /// Create a supercell.
    ///
    /// Args:
    ///     scaling: Either [a, b, c] diagonal factors or a 3x3 transformation matrix.
    fn make_supercell(&self, scaling: SupercellInput) -> PyResult<Self> {
        match scaling {
            SupercellInput::Diag(ns) => {
                if ns.iter().any(|&n| n <= 0) {
                    return Err(PyValueError::new_err(format!(
                        "supercell scaling factors must all be positive, got {ns:?}"
                    )));
                }
                Ok(Self::wrap(self.inner.make_supercell_diag(ns)))
            }
            SupercellInput::Matrix(matrix) => Ok(Self::wrap(
                self.inner.make_supercell(matrix).map_err(ferrox_err)?,
            )),
        }
    }

    /// Cartesian coordinates of all sites as list of [x, y, z].
    #[getter]
    fn cart_coords(&self) -> Vec<[f64; 3]> {
        self.inner
            .cart_coords()
            .iter()
            .map(|coord| [coord.x, coord.y, coord.z])
            .collect()
    }

    /// Species string for each site (e.g. ["Na", "Cl"]).
    #[getter]
    fn species_strings(&self) -> Vec<String> {
        self.inner.species_strings()
    }

    /// Distance between two sites.
    ///
    /// Uses minimum image convention by default. Pass `image` to specify
    /// a particular periodic image offset.
    #[pyo3(signature = (site_idx_a, site_idx_b, image = None))]
    fn get_distance(
        &self,
        site_idx_a: usize,
        site_idx_b: usize,
        image: Option<[i32; 3]>,
    ) -> PyResult<f64> {
        let n_sites = self.inner.num_sites();
        if site_idx_a >= n_sites || site_idx_b >= n_sites {
            return Err(pyo3::exceptions::PyIndexError::new_err(format!(
                "site index out of range: got ({site_idx_a}, {site_idx_b}) \
                 for structure with {n_sites} sites"
            )));
        }
        Ok(match image {
            Some(jimage) => self
                .inner
                .get_distance_with_image(site_idx_a, site_idx_b, jimage),
            None => self.inner.get_distance(site_idx_a, site_idx_b),
        })
    }

    /// N×N distance matrix (minimum image convention).
    #[getter]
    fn distance_matrix(&self) -> Vec<Vec<f64>> {
        self.inner.distance_matrix()
    }

    /// Atomic numbers for each site.
    #[getter]
    fn atomic_numbers(&self) -> Vec<u8> {
        self.inner
            .site_occupancies
            .iter()
            .map(|occ| occ.dominant_species().element.atomic_number())
            .collect()
    }

    /// Periodic boundary conditions [x, y, z].
    #[getter]
    fn pbc(&self) -> [bool; 3] {
        self.inner.lattice.pbc
    }

    /// All site properties as list of dicts (one per site).
    #[getter]
    fn site_properties(&self, py: Python<'_>) -> PyResult<Py<PyList>> {
        let result: Vec<_> = (0..self.inner.num_sites())
            .map(|idx| props_to_pydict(py, self.inner.site_properties(idx)))
            .collect::<PyResult<_>>()?;
        Ok(PyList::new(py, result)?.unbind())
    }

    // === Distortions ===

    /// Distort bonds around a center site by specified factors.
    /// Returns one Structure per factor.
    #[pyo3(signature = (center_site_idx, distortion_factors, num_neighbors = None, cutoff = 5.0))]
    fn distort_bonds(
        &self,
        center_site_idx: usize,
        distortion_factors: Vec<f64>,
        num_neighbors: Option<usize>,
        cutoff: f64,
    ) -> PyResult<Vec<Self>> {
        let results = distortions::distort_bonds(
            &self.inner,
            center_site_idx,
            &distortion_factors,
            num_neighbors,
            cutoff,
        )
        .map_err(ferrox_err)?;

        Ok(results
            .into_iter()
            .map(|result| Self::wrap(result.structure))
            .collect())
    }

    /// Create a dimer by moving two atoms closer together.
    fn create_dimer(
        &self,
        site_a_idx: usize,
        site_b_idx: usize,
        target_distance: f64,
    ) -> PyResult<Self> {
        let result =
            distortions::create_dimer(&self.inner, site_a_idx, site_b_idx, target_distance)
                .map_err(ferrox_err)?;
        Ok(Self::wrap(result.structure))
    }

    /// Apply Monte Carlo rattling to all atoms.
    #[pyo3(signature = (stdev, seed, min_distance = 0.5, max_attempts = 100))]
    fn rattle(
        &self,
        stdev: f64,
        seed: u64,
        min_distance: f64,
        max_attempts: usize,
    ) -> PyResult<Self> {
        if max_attempts == 0 {
            return Err(PyValueError::new_err("max_attempts must be greater than 0"));
        }
        let result =
            distortions::rattle_structure(&self.inner, stdev, seed, min_distance, max_attempts)
                .map_err(ferrox_err)?;
        Ok(Self::wrap(result.structure))
    }

    /// Apply local rattling with distance-dependent amplitude decay.
    fn local_rattle(
        &self,
        center_site_idx: usize,
        max_amplitude: f64,
        decay_radius: f64,
        seed: u64,
    ) -> PyResult<Self> {
        let result = distortions::local_rattle(
            &self.inner,
            center_site_idx,
            max_amplitude,
            decay_radius,
            seed,
        )
        .map_err(ferrox_err)?;
        Ok(Self::wrap(result.structure))
    }

    // === OOP accessors for Lattice and Composition ===

    /// Get the lattice as a Lattice object.
    #[getter]
    fn lattice(&self) -> PyLattice {
        PyLattice::from_inner(self.inner.lattice.clone())
    }

    /// Composition object for this structure.
    #[getter]
    fn composition(&self) -> PyComposition {
        PyComposition::from_inner(self.inner.composition())
    }

    /// Total mass in atomic mass units (amu).
    #[getter]
    fn total_mass(&self) -> f64 {
        self.inner.total_mass()
    }

    // === Structure manipulation (migrated from ferrox.structure module) ===

    /// Get a reduced cell structure.
    ///
    /// Args:
    ///     algorithm: "niggli" or "lll"
    ///     niggli_tol: Tolerance for Niggli reduction (default 1e-5)
    ///     lll_delta: Delta parameter for LLL reduction (default 0.75)
    #[pyo3(signature = (algorithm = "niggli", niggli_tol = 1e-5, lll_delta = 0.75))]
    fn get_reduced_structure(
        &self,
        algorithm: &str,
        niggli_tol: f64,
        lll_delta: f64,
    ) -> PyResult<Self> {
        let algo = parse_reduction_algo(algorithm)?;
        match algo {
            ReductionAlgo::Niggli if !niggli_tol.is_finite() || niggli_tol <= 0.0 => {
                return Err(PyValueError::new_err(
                    "niggli_tol must be finite and positive",
                ));
            }
            ReductionAlgo::LLL
                if !lll_delta.is_finite() || lll_delta <= 0.25 || lll_delta > 1.0 =>
            {
                return Err(PyValueError::new_err(
                    "lll_delta must be finite and in range (0.25, 1.0]",
                ));
            }
            _ => {}
        }
        let reduced = self
            .inner
            .get_reduced_structure_with_params(algo, niggli_tol, lll_delta)
            .map_err(ferrox_err)?;
        Ok(Self::wrap(reduced))
    }

    /// Wrap all sites into the unit cell [0, 1).
    fn wrap_to_unit_cell(&self) -> Self {
        let mut inner = self.inner.clone();
        inner.wrap_to_unit_cell();
        Self::wrap(inner)
    }

    /// Interpolate between this structure and another.
    #[pyo3(signature = (other, n_images, interpolate_lattices = false, use_pbc = true))]
    fn interpolate(
        &self,
        other: &Self,
        n_images: usize,
        interpolate_lattices: bool,
        use_pbc: bool,
    ) -> PyResult<Vec<Self>> {
        if n_images == 0 {
            return Err(PyValueError::new_err(
                "n_images must be at least 1 to generate interpolated structures",
            ));
        }
        let images = self
            .inner
            .interpolate(&other.inner, n_images, interpolate_lattices, use_pbc)
            .map_err(ferrox_err)?;
        Ok(Self::wrap_many(images))
    }

    /// Get structure with sites sorted.
    ///
    /// Args:
    ///     by: Sort key — "species" (default) or "electronegativity"
    ///     reverse: Reverse sort order (default False)
    #[pyo3(signature = (by = "species", reverse = false))]
    fn sort(&self, by: &str, reverse: bool) -> PyResult<Self> {
        match by {
            "species" => Ok(Self::wrap(self.inner.get_sorted_structure(reverse))),
            "electronegativity" => Ok(Self::wrap(
                self.inner.get_sorted_by_electronegativity(reverse),
            )),
            _ => Err(PyValueError::new_err(format!(
                "sort by must be 'species' or 'electronegativity', got '{by}'"
            ))),
        }
    }

    /// Substitute one species with another.
    fn substitute_species(&self, old_species: &str, new_species: &str) -> PyResult<Self> {
        let old_elem = parse_element(old_species)?;
        let new_elem = parse_element(new_species)?;
        let result = self
            .inner
            .substitute(
                crate::species::Species::neutral(old_elem),
                crate::species::Species::neutral(new_elem),
            )
            .map_err(ferrox_err)?;
        Ok(Self::wrap(result))
    }

    /// Remove all sites of specified species.
    fn remove_species(&self, species_list: Vec<String>) -> PyResult<Self> {
        let species = Self::parse_neutral_species_list(&species_list)?;
        let result = self.inner.remove_species(&species).map_err(ferrox_err)?;
        Ok(Self::wrap(result))
    }

    /// Remove sites at specified indices.
    fn remove_sites(&self, indices: Vec<usize>) -> PyResult<Self> {
        let result = self
            .inner
            .remove_sites(&indices)
            .map_err(|err| pyo3::exceptions::PyIndexError::new_err(err.to_string()))?;
        Ok(Self::wrap(result))
    }

    /// Apply a deformation gradient to the structure.
    fn deform(&self, gradient: [[f64; 3]; 3]) -> PyResult<Self> {
        if gradient.iter().flatten().any(|v| !v.is_finite()) {
            return Err(PyValueError::new_err("gradient must be finite"));
        }
        let grad_matrix = Matrix3::from_row_slice(&gradient.concat());
        let result = self.inner.deform(grad_matrix).map_err(ferrox_err)?;
        Ok(Self::wrap(result))
    }

    /// Compute Ewald energy for a structure with oxidation states.
    #[pyo3(signature = (eta = None, real_cutoff = None, accuracy = None))]
    fn ewald_energy(
        &self,
        eta: Option<f64>,
        real_cutoff: Option<f64>,
        accuracy: Option<f64>,
    ) -> PyResult<f64> {
        if let Some(acc) = accuracy.filter(|&a| a <= 0.0 || !a.is_finite()) {
            return Err(PyValueError::new_err(format!(
                "accuracy must be positive and finite, got {acc}"
            )));
        }
        if let Some(rc) = real_cutoff.filter(|&r| r <= 0.0 || !r.is_finite()) {
            return Err(PyValueError::new_err(format!(
                "real_cutoff must be positive and finite, got {rc}"
            )));
        }
        let mut ewald = crate::algorithms::ewald::Ewald::new();
        if let Some(eta_val) = eta {
            if eta_val <= 0.0 || !eta_val.is_finite() {
                return Err(PyValueError::new_err("eta must be positive and finite"));
            }
            ewald = ewald.with_eta(eta_val);
        }
        if let Some(rc) = real_cutoff {
            ewald = ewald.with_real_cutoff(rc);
        }
        if let Some(acc) = accuracy {
            ewald = ewald.with_accuracy(acc);
        }
        ewald.energy(&self.inner).map_err(ferrox_err)
    }

    /// Generate ordered structures from a disordered structure.
    #[pyo3(signature = (max_structures = 100))]
    fn order_disordered(&self, max_structures: usize) -> PyResult<Vec<Self>> {
        let config = crate::transformations::OrderDisorderedConfig {
            max_structures: Some(max_structures),
            ..Default::default()
        };
        let results = self.inner.order_disordered(config).map_err(ferrox_err)?;
        Ok(Self::wrap_many(results))
    }

    /// Enumerate derivative structures within a size range.
    #[pyo3(signature = (min_size = 1, max_size = 4))]
    fn enumerate_derivatives(&self, min_size: usize, max_size: usize) -> PyResult<Vec<Self>> {
        if min_size > max_size {
            return Err(PyValueError::new_err("min_size must be <= max_size"));
        }
        let results = self
            .inner
            .enumerate_derivatives(min_size, max_size)
            .map_err(ferrox_err)?;
        Ok(Self::wrap_many(results))
    }

    /// Translate selected sites by a vector.
    #[pyo3(signature = (indices, vector, fractional = true))]
    fn translate_sites(
        &self,
        indices: Vec<usize>,
        vector: [f64; 3],
        fractional: bool,
    ) -> PyResult<Self> {
        if vector.iter().any(|v| !v.is_finite()) {
            return Err(PyValueError::new_err("vector must be finite"));
        }
        let mut inner = self.inner.clone();
        let num_sites = inner.num_sites();
        if let Some(&idx) = indices.iter().find(|&&idx| idx >= num_sites) {
            return Err(pyo3::exceptions::PyIndexError::new_err(format!(
                "Site index {idx} out of bounds (num_sites={num_sites})"
            )));
        }
        inner.translate_sites(&indices, Vector3::from(vector), fractional);
        Ok(Self::wrap(inner))
    }

    /// Perturb all sites by random vectors.
    #[pyo3(signature = (distance, min_distance = None, seed = None))]
    fn perturb(
        &self,
        distance: f64,
        min_distance: Option<f64>,
        seed: Option<u64>,
    ) -> PyResult<Self> {
        if !distance.is_finite() || distance < 0.0 {
            return Err(PyValueError::new_err(
                "distance must be finite and non-negative",
            ));
        }
        if let Some(min_dist) = min_distance {
            if !min_dist.is_finite() || min_dist < 0.0 {
                return Err(PyValueError::new_err(
                    "min_distance must be finite and non-negative",
                ));
            }
            if min_dist > distance {
                return Err(PyValueError::new_err("min_distance must be <= distance"));
            }
        }
        let mut inner = self.inner.clone();
        inner.perturb(distance, min_distance, seed);
        Ok(Self::wrap(inner))
    }

    /// Labels for all sites.
    #[getter]
    fn site_labels(&self) -> Vec<String> {
        self.inner.site_labels()
    }

    /// Set a site property.
    fn set_site_property(
        &self,
        idx: usize,
        key: &str,
        value: Bound<'_, pyo3::PyAny>,
    ) -> PyResult<Self> {
        let mut inner = self.inner.clone();
        if idx >= inner.num_sites() {
            return Err(pyo3::exceptions::PyIndexError::new_err(format!(
                "Site index {idx} out of bounds for structure with {} sites",
                inner.num_sites()
            )));
        }
        let json_val = py_to_json_value(&value)?;
        inner.set_site_property(idx, key, json_val);
        Ok(Self::wrap(inner))
    }

    /// Whether this structure matches another using StructureMatcher.
    #[pyo3(signature = (other, anonymous = false))]
    fn matches(&self, other: &Self, anonymous: bool) -> bool {
        self.inner.matches(&other.inner, anonymous)
    }

    // === Symmetry operations (migrated from ferrox.symmetry module) ===

    /// Get symmetry operations as list of {rotation, translation} dicts.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_symmetry_operations(&self, py: Python<'_>, symprec: f64) -> PyResult<Vec<Py<PyDict>>> {
        let ops = self
            .inner
            .get_symmetry_operations(symprec)
            .map_err(ferrox_err)?;
        ops.iter()
            .map(|(rot, trans)| {
                let dict = PyDict::new(py);
                dict.set_item("rotation", rot.to_vec())?;
                dict.set_item("translation", trans.to_vec())?;
                Ok(dict.unbind())
            })
            .collect()
    }

    /// Get equivalent site indices (orbit mapping).
    #[pyo3(signature = (symprec = 0.01))]
    fn get_equivalent_sites(&self, symprec: f64) -> PyResult<Vec<usize>> {
        self.inner.get_equivalent_sites(symprec).map_err(ferrox_err)
    }

    /// Get the primitive cell.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_primitive(&self, symprec: f64) -> PyResult<Self> {
        let primitive = self.inner.get_primitive(symprec).map_err(ferrox_err)?;
        Ok(Self::wrap(primitive))
    }

    /// Get the conventional cell.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_conventional(&self, symprec: f64) -> PyResult<Self> {
        let conventional = self
            .inner
            .get_conventional_structure(symprec)
            .map_err(ferrox_err)?;
        Ok(Self::wrap(conventional))
    }

    /// Get the ITA-standardized structure. Returns (structure, transformation_matrix).
    #[pyo3(signature = (symprec = 0.01, primitive = false))]
    fn get_standardized(
        &self,
        py: Python<'_>,
        symprec: f64,
        primitive: bool,
    ) -> PyResult<Py<PyDict>> {
        let (std_struc, transformation) = self
            .inner
            .get_standardized_structure(symprec, primitive)
            .map_err(ferrox_err)?;
        let dict = PyDict::new(py);
        let py_struct = Self::wrap(std_struc);
        dict.set_item("structure", py_struct.into_pyobject(py)?)?;
        dict.set_item("transformation", mat3_to_array(&transformation))?;
        Ok(dict.unbind())
    }

    /// Symmetrize by averaging equivalent atomic positions.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_symmetrized(&self, symprec: f64) -> PyResult<Self> {
        let symmetrized = self
            .inner
            .get_symmetrized_structure(symprec)
            .map_err(ferrox_err)?;
        Ok(Self::wrap(symmetrized))
    }

    /// Get all site indices symmetry-equivalent to the given site.
    #[pyo3(signature = (site_idx, symprec = 0.01))]
    fn get_symmetry_equivalent_sites(&self, site_idx: usize, symprec: f64) -> PyResult<Vec<usize>> {
        self.inner
            .get_symmetry_equivalent_sites(site_idx, symprec)
            .map_err(ferrox_err)
    }

    /// Get the full symmetry dataset as a dict.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_symmetry_dataset(&self, py: Python<'_>, symprec: f64) -> PyResult<Py<PyDict>> {
        let dataset = self._dataset(symprec)?;
        let dict = PyDict::new(py);
        dict.set_item("spacegroup_number", dataset.number)?;
        dict.set_item("spacegroup_symbol", &dataset.hm_symbol)?;
        dict.set_item("hall_number", dataset.hall_number)?;
        dict.set_item("pearson_symbol", &dataset.pearson_symbol)?;
        dict.set_item("num_operations", dataset.operations.len())?;
        dict.set_item(
            "crystal_system",
            spacegroup_to_crystal_system(dataset.number),
        )?;

        let gcc = geometric_crystal_class_from_hall(dataset.hall_number).map_err(ferrox_err)?;
        dict.set_item("point_group", point_group_symbol(gcc))?;
        dict.set_item("laue_group", laue_group_from_point_group(gcc))?;

        let wyckoff_strs: Vec<String> = dataset.wyckoffs.iter().map(|c| c.to_string()).collect();
        dict.set_item("wyckoff_letters", wyckoff_strs)?;
        dict.set_item("equivalent_sites", &dataset.orbits)?;
        dict.set_item("site_symmetry_symbols", &dataset.site_symmetry_symbols)?;

        dict.set_item("std_linear", mat3_to_array(&dataset.std_linear))?;
        let shift = &dataset.std_origin_shift;
        dict.set_item("std_origin_shift", [shift.x, shift.y, shift.z])?;
        dict.set_item(
            "std_rotation_matrix",
            mat3_to_array(&dataset.std_rotation_matrix),
        )?;
        dict.set_item("mapping_std_prim", &dataset.mapping_std_prim)?;

        Ok(dict.unbind())
    }

    /// Laue group symbol (e.g. "m-3m").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_laue_group(&self, symprec: f64) -> PyResult<&'static str> {
        let ds = self._dataset(symprec)?;
        let gcc = geometric_crystal_class_from_hall(ds.hall_number).map_err(ferrox_err)?;
        Ok(laue_group_from_point_group(gcc))
    }

    /// Apply a symmetry operation (rotation + translation) to the structure.
    #[pyo3(signature = (rotation, translation, fractional = true))]
    fn apply_operation(
        &self,
        rotation: [[f64; 3]; 3],
        translation: [f64; 3],
        fractional: bool,
    ) -> Self {
        let mut inner = self.inner.clone();
        let rot = Matrix3::from_row_slice(&rotation.concat());
        let op = SymmOp::new(rot, Vector3::from(translation));
        inner.apply_operation(&op, fractional);
        Self::wrap(inner)
    }

    /// Apply inversion through the origin.
    #[pyo3(signature = (fractional = true))]
    fn apply_inversion(&self, fractional: bool) -> Self {
        let mut inner = self.inner.clone();
        inner.apply_operation(&SymmOp::inversion(), fractional);
        Self::wrap(inner)
    }

    /// Apply a translation to all sites.
    #[pyo3(signature = (translation, fractional = true))]
    fn apply_translation(&self, translation: [f64; 3], fractional: bool) -> Self {
        let mut inner = self.inner.clone();
        inner.apply_operation(&SymmOp::translation(Vector3::from(translation)), fractional);
        Self::wrap(inner)
    }
}
