use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3_stub_gen::derive::gen_stub_pymethods;

use nalgebra::{Matrix3, Vector3};

use crate::distortions;
use crate::python::helpers::{
    mat3_to_array, parse_element, parse_reduction_algo, props_to_pydict, py_to_json_value,
};
use crate::structure::{
    ReductionAlgo, SymmOp, geometric_crystal_class_from_hall, laue_group_from_point_group,
    point_group_symbol, spacegroup_to_crystal_system,
};

use super::super::composition::PyComposition;
use super::super::lattice::PyLattice;
use super::{PyStructure, SupercellInput, ferrox_err};

#[gen_stub_pymethods]
#[pymethods]
impl PyStructure {
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
