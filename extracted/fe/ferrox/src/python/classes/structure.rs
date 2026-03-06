//! PyStructure: OOP wrapper for Structure with MoyoDataset caching.

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

use moyo::MoyoDataset;

use crate::cell_ops;
use crate::structure::{
    geometric_crystal_class_from_hall, spacegroup_to_crystal_system, spacegroup_type_from_number,
};

use crate::magnetism::MagneticAnalysis;
use crate::python::helpers::{StructureJson, mat3_to_array, parse_struct};

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

// === Internal helpers (not exposed to Python) ===

impl PyStructure {
    /// Get or compute the cached symmetry dataset (cheap Arc clone on hit).
    fn _dataset(&self, symprec: f64) -> PyResult<Arc<MoyoDataset>> {
        let mut cache = self
            .cached_dataset
            .lock()
            .map_err(|err| PyValueError::new_err(err.to_string()))?;
        if let Some((cached_prec, ref ds)) = *cache
            && (cached_prec - symprec).abs() < 1e-12
        {
            return Ok(Arc::clone(ds));
        }
        let ds = Arc::new(
            self.inner
                .get_symmetry_dataset(symprec)
                .map_err(|err| PyValueError::new_err(err.to_string()))?,
        );
        *cache = Some((symprec, Arc::clone(&ds)));
        Ok(ds)
    }

    /// Look up SpacegroupTypeInfo from the cached dataset.
    fn _spg_type_info(&self, symprec: f64) -> PyResult<crate::structure::SpacegroupTypeInfo> {
        let ds = self._dataset(symprec)?;
        spacegroup_type_from_number(ds.number).map_err(|err| PyValueError::new_err(err.to_string()))
    }

    /// Evaluate a predicate on the geometric crystal class.
    fn _gcc_predicate(
        &self,
        symprec: f64,
        predicate: fn(moyo::data::GeometricCrystalClass) -> bool,
    ) -> PyResult<bool> {
        let ds = self._dataset(symprec)?;
        let gcc = geometric_crystal_class_from_hall(ds.hall_number)
            .map_err(|err| PyValueError::new_err(err.to_string()))?;
        Ok(predicate(gcc))
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyStructure {
    /// Create a new Structure from a JSON string or dict.
    #[new]
    fn new(structure: StructureJson) -> PyResult<Self> {
        let inner = parse_struct(&structure)?;
        Ok(Self {
            inner,
            cached_dataset: Mutex::new(None),
        })
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

    /// Atomic fractions as {element: fraction}.
    fn get_atomic_fractions(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        Ok(self
            .inner
            .composition()
            .atomic_fractions_map()
            .into_pyobject(py)?
            .unbind())
    }

    /// Unit cell composition as {element: amount}.
    fn get_composition_unit_cell(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        Ok(self
            .inner
            .composition()
            .composition_unit_cell_map()
            .into_pyobject(py)?
            .unbind())
    }

    /// Reduced composition as {element: integer_amount}. None if non-integer reduction.
    fn get_composition_reduced(&self, py: Python<'_>) -> PyResult<Option<Py<PyDict>>> {
        self.inner
            .composition()
            .composition_reduced_map()
            .map(|map| Ok(map.into_pyobject(py)?.unbind()))
            .transpose()
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

    /// Lattice parameters [a, b, c] in Å.
    #[getter]
    fn lattice_params(&self) -> [f64; 3] {
        let lengths = self.inner.lattice.lengths();
        [lengths.x, lengths.y, lengths.z]
    }

    /// Lattice angles [alpha, beta, gamma] in degrees.
    #[getter]
    fn lattice_angles(&self) -> [f64; 3] {
        let angles = self.inner.lattice.angles();
        [angles.x, angles.y, angles.z]
    }

    /// 3x3 lattice matrix.
    #[getter]
    fn lattice_matrix(&self) -> [[f64; 3]; 3] {
        mat3_to_array(self.inner.lattice.matrix())
    }

    // === Niggli G6 ===

    /// Niggli G6 representation [a², b², c², 2bc, 2ac, 2ab].
    #[pyo3(signature = (tol = 1e-5))]
    fn get_niggli_g6(&self, tol: f64) -> PyResult<[f64; 6]> {
        cell_ops::niggli_g6(&self.inner.lattice, tol)
            .map(|g6| g6.as_array())
            .map_err(|err| PyValueError::new_err(err.to_string()))
    }

    /// Selling S6 representation [bc, ac, ab, ad, bd, cd] (canonicalized).
    #[pyo3(signature = (tol = 1e-5))]
    fn get_selling_s6(&self, tol: f64) -> PyResult<[f64; 6]> {
        cell_ops::selling_s6(&self.inner.lattice, tol)
            .map(|s6| s6.as_array())
            .map_err(|err| PyValueError::new_err(err.to_string()))
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
            .map_err(|err| PyValueError::new_err(err.to_string()))
    }
}
