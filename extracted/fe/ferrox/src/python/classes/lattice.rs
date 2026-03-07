//! PyLattice: OOP wrapper for Lattice.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

use crate::lattice::Lattice;
use crate::python::helpers::mat3_to_array;

/// A crystallographic lattice with matrix operations and reduction.
///
/// Examples:
///     >>> lat = Lattice([[5.0, 0, 0], [0, 5.0, 0], [0, 0, 5.0]])
///     >>> lat.volume
///     125.0
///     >>> lat.a
///     5.0
///     >>> lat = Lattice.from_parameters(5.0, 5.0, 5.0, 90.0, 90.0, 90.0)
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.lattice", name = "Lattice")]
pub struct PyLattice {
    inner: Lattice,
}

fn coords_to_vec3(coords: Vec<[f64; 3]>) -> Vec<nalgebra::Vector3<f64>> {
    coords
        .into_iter()
        .map(|coord| nalgebra::Vector3::new(coord[0], coord[1], coord[2]))
        .collect()
}

fn vec3_to_coords(coords: Vec<nalgebra::Vector3<f64>>) -> Vec<[f64; 3]> {
    coords
        .into_iter()
        .map(|coord| [coord.x, coord.y, coord.z])
        .collect()
}

impl PyLattice {
    /// Construct from an existing Rust Lattice (for internal use by Structure, etc.).
    pub fn from_inner(inner: Lattice) -> Self {
        Self { inner }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyLattice {
    /// Create a Lattice from a 3x3 matrix (rows = lattice vectors).
    #[new]
    fn new(matrix: [[f64; 3]; 3]) -> Self {
        Self::from_inner(Lattice::from_array(matrix))
    }

    /// Create a Lattice from lattice parameters (a, b, c, alpha, beta, gamma).
    #[staticmethod]
    fn from_parameters(a: f64, b: f64, c: f64, alpha: f64, beta: f64, gamma: f64) -> Self {
        Self::from_inner(Lattice::from_parameters(a, b, c, alpha, beta, gamma))
    }

    /// Create a cubic lattice.
    #[staticmethod]
    fn cubic(a: f64) -> Self {
        Self::from_inner(Lattice::cubic(a))
    }

    /// Create a tetragonal lattice.
    #[staticmethod]
    fn tetragonal(a: f64, c: f64) -> Self {
        Self::from_inner(Lattice::tetragonal(a, c))
    }

    /// Create an orthorhombic lattice.
    #[staticmethod]
    fn orthorhombic(a: f64, b: f64, c: f64) -> Self {
        Self::from_inner(Lattice::orthorhombic(a, b, c))
    }

    /// Create a hexagonal lattice.
    #[staticmethod]
    fn hexagonal(a: f64, c: f64) -> Self {
        Self::from_inner(Lattice::hexagonal(a, c))
    }

    // === Properties ===

    /// 3x3 lattice matrix (rows = lattice vectors).
    #[getter]
    fn matrix(&self) -> [[f64; 3]; 3] {
        mat3_to_array(self.inner.matrix())
    }

    /// Unit cell volume in ų.
    #[getter]
    fn volume(&self) -> f64 {
        self.inner.volume()
    }

    /// Lattice parameter a in Angstrom.
    #[getter]
    fn a(&self) -> f64 {
        self.inner.lengths().x
    }

    /// Lattice parameter b in Angstrom.
    #[getter]
    fn b(&self) -> f64 {
        self.inner.lengths().y
    }

    /// Lattice parameter c in Angstrom.
    #[getter]
    fn c(&self) -> f64 {
        self.inner.lengths().z
    }

    /// Lattice angle alpha in degrees.
    #[getter]
    fn alpha(&self) -> f64 {
        self.inner.angles().x
    }

    /// Lattice angle beta in degrees.
    #[getter]
    fn beta(&self) -> f64 {
        self.inner.angles().y
    }

    /// Lattice angle gamma in degrees.
    #[getter]
    fn gamma(&self) -> f64 {
        self.inner.angles().z
    }

    /// Lattice lengths [a, b, c] in Angstrom.
    #[getter]
    fn lengths(&self) -> [f64; 3] {
        let lengths = self.inner.lengths();
        [lengths.x, lengths.y, lengths.z]
    }

    /// Lattice angles [alpha, beta, gamma] in degrees.
    #[getter]
    fn angles(&self) -> [f64; 3] {
        let angles = self.inner.angles();
        [angles.x, angles.y, angles.z]
    }

    /// Periodic boundary conditions [x, y, z].
    #[getter]
    fn pbc(&self) -> [bool; 3] {
        self.inner.pbc
    }

    /// Whether the lattice is orthogonal (all angles ≈ 90°).
    #[getter]
    fn is_orthogonal(&self) -> bool {
        let angles = self.inner.angles();
        const TOL: f64 = 0.01;
        (angles.x - 90.0).abs() < TOL
            && (angles.y - 90.0).abs() < TOL
            && (angles.z - 90.0).abs() < TOL
    }

    /// Lattice parameters as (a, b, c, alpha, beta, gamma) tuple.
    #[getter]
    fn parameters(&self) -> (f64, f64, f64, f64, f64, f64) {
        let lengths = self.inner.lengths();
        let angles = self.inner.angles();
        (
            lengths.x, lengths.y, lengths.z, angles.x, angles.y, angles.z,
        )
    }

    /// Lattice vector lengths [a, b, c] (alias for lengths, pymatgen compat).
    #[getter]
    fn abc(&self) -> [f64; 3] {
        let lengths = self.inner.lengths();
        [lengths.x, lengths.y, lengths.z]
    }

    // === Matrix operations ===

    /// Inverse of the lattice matrix.
    #[getter]
    fn inv_matrix(&self) -> [[f64; 3]; 3] {
        mat3_to_array(&self.inner.inv_matrix())
    }

    /// Metric tensor (G = M^T * M).
    #[getter]
    fn metric_tensor(&self) -> [[f64; 3]; 3] {
        mat3_to_array(&self.inner.metric_tensor())
    }

    /// Reciprocal lattice.
    #[getter]
    fn reciprocal(&self) -> PyLattice {
        Self::from_inner(self.inner.reciprocal_lattice())
    }

    // === Coordinate transformations ===

    /// Convert Cartesian coordinates to fractional.
    fn get_fractional_coords(&self, cart_coords: Vec<[f64; 3]>) -> Vec<[f64; 3]> {
        vec3_to_coords(
            self.inner
                .get_fractional_coords(&coords_to_vec3(cart_coords)),
        )
    }

    /// Convert fractional coordinates to Cartesian.
    fn get_cartesian_coords(&self, frac_coords: Vec<[f64; 3]>) -> Vec<[f64; 3]> {
        vec3_to_coords(
            self.inner
                .get_cartesian_coords(&coords_to_vec3(frac_coords)),
        )
    }

    // === Lattice reduction ===

    /// LLL-reduced lattice.
    #[pyo3(signature = (delta = 0.75))]
    fn get_lll_reduced_lattice(&self, delta: f64) -> PyResult<Self> {
        if !delta.is_finite() || delta <= 0.25 || delta > 1.0 {
            return Err(PyValueError::new_err(
                "delta must be in range (0.25, 1.0] for LLL reduction",
            ));
        }
        Ok(Self::from_inner(self.inner.get_lll_reduced(delta)))
    }

    /// LLL reduction mapping matrix.
    #[getter]
    fn lll_mapping(&self) -> [[f64; 3]; 3] {
        mat3_to_array(&self.inner.lll_mapping())
    }

    /// Niggli-reduced lattice.
    #[pyo3(signature = (tol = 1e-5))]
    fn get_niggli_reduced_lattice(&self, tol: f64) -> PyResult<Self> {
        let reduced = self
            .inner
            .get_niggli_reduced(tol)
            .map_err(|err| PyValueError::new_err(err.to_string()))?;
        Ok(Self::from_inner(reduced))
    }

    /// Create a copy of this lattice.
    fn copy(&self) -> Self {
        Self::from_inner(self.inner.clone())
    }

    // === Dunder methods ===

    fn __str__(&self) -> String {
        let lengths = self.inner.lengths();
        let angles = self.inner.angles();
        format!(
            "Lattice\n    abc : {:>10.6} {:>10.6} {:>10.6}\n angles : {:>10.6} {:>10.6} {:>10.6}\n volume : {:>10.6}",
            lengths.x,
            lengths.y,
            lengths.z,
            angles.x,
            angles.y,
            angles.z,
            self.inner.volume()
        )
    }

    fn __repr__(&self) -> String {
        let lengths = self.inner.lengths();
        let angles = self.inner.angles();
        format!(
            "Lattice(a={:.4}, b={:.4}, c={:.4}, alpha={:.2}, beta={:.2}, gamma={:.2})",
            lengths.x, lengths.y, lengths.z, angles.x, angles.y, angles.z
        )
    }

    fn __eq__(&self, other: &Self) -> bool {
        let tol = 1e-8;
        let self_mat = self.inner.matrix();
        let other_mat = other.inner.matrix();
        (0..3)
            .all(|row| (0..3).all(|col| (self_mat[(row, col)] - other_mat[(row, col)]).abs() < tol))
    }
}
