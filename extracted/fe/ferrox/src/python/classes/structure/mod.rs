//! PyStructure: OOP wrapper for Structure with MoyoDataset caching.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pyclass;

use moyo::MoyoDataset;

use crate::analysis::magnetism::MagneticAnalysis;

/// Set multiple dict keys to None.
pub(super) fn set_none_keys(dict: &Bound<'_, PyDict>, keys: &[&str]) -> PyResult<()> {
    let none = dict.py().None();
    for key in keys {
        dict.set_item(*key, &none)?;
    }
    Ok(())
}

/// Build a histogram of Wyckoff letter occurrences.
pub(super) fn wyckoff_histogram(wyckoffs: &[char]) -> HashMap<String, usize> {
    let mut hist = HashMap::new();
    for wyk in wyckoffs {
        *hist.entry(wyk.to_string()).or_default() += 1;
    }
    hist
}

/// Write MagneticAnalysis fields into a PyDict.
pub(super) fn write_mag_analysis(dict: &Bound<'_, PyDict>, mag: &MagneticAnalysis) -> PyResult<()> {
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
    pub(crate) inner: crate::structure::Structure,
    cached_dataset: Mutex<Option<(f64, Arc<MoyoDataset>)>>,
}

/// Convert any FerroxError to PyValueError.
pub(super) fn ferrox_err(err: impl std::fmt::Display) -> PyErr {
    PyValueError::new_err(err.to_string())
}

/// Accept either [a, b, c] diagonal scaling or a 3x3 transformation matrix.
pub(super) enum SupercellInput {
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

mod internal_helpers_impl;
mod pymethods_basic;
mod pymethods_ops;
mod pymethods_symmetry;
