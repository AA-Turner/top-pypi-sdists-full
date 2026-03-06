//! Elastic tensor calculations.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3_stub_gen::derive::gen_stub_pyfunction;

use crate::elastic;

use super::helpers::{array_to_mat3, mat3_to_array};

/// Generate strain matrices for elastic constant calculation.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
#[pyo3(signature = (magnitude = 0.01, shear = true))]
fn generate_strains(magnitude: f64, shear: bool) -> Vec<[[f64; 3]; 3]> {
    elastic::generate_strains(magnitude, shear)
        .into_iter()
        .map(|m| mat3_to_array(&m))
        .collect()
}

/// Apply a strain to a cell matrix.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn apply_strain(cell: [[f64; 3]; 3], strain: [[f64; 3]; 3]) -> [[f64; 3]; 3] {
    mat3_to_array(&elastic::apply_strain(
        &array_to_mat3(cell),
        &array_to_mat3(strain),
    ))
}

/// Convert stress tensor to Voigt notation.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn stress_to_voigt(stress: [[f64; 3]; 3]) -> [f64; 6] {
    elastic::stress_to_voigt(&array_to_mat3(stress))
}

/// Convert strain tensor to Voigt notation.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn strain_to_voigt(strain: [[f64; 3]; 3]) -> [f64; 6] {
    elastic::strain_to_voigt(&array_to_mat3(strain))
}

/// Calculate the elastic tensor from strains and stresses.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn tensor_from_stresses(
    strains: Vec<[[f64; 3]; 3]>,
    stresses: Vec<[[f64; 3]; 3]>,
) -> PyResult<[[f64; 6]; 6]> {
    if strains.len() != stresses.len() {
        return Err(PyValueError::new_err(
            "strains and stresses must have same length",
        ));
    }
    if strains.len() < 6 {
        return Err(PyValueError::new_err("Need at least 6 strain/stress pairs"));
    }
    let strain_mats: Vec<_> = strains.iter().map(|&s| array_to_mat3(s)).collect();
    let stress_mats: Vec<_> = stresses.iter().map(|&s| array_to_mat3(s)).collect();
    let (tensor, _) = elastic::try_elastic_tensor_from_stresses(&strain_mats, &stress_mats);
    Ok(tensor)
}

/// Calculate the bulk modulus from elastic tensor.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn bulk_modulus(tensor: [[f64; 6]; 6]) -> f64 {
    elastic::bulk_modulus(&tensor)
}

/// Calculate the shear modulus from elastic tensor.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn shear_modulus(tensor: [[f64; 6]; 6]) -> f64 {
    elastic::shear_modulus(&tensor)
}

/// Calculate Young's modulus from bulk and shear moduli.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn youngs_modulus(bulk: f64, shear: f64) -> f64 {
    elastic::youngs_modulus(bulk, shear)
}

/// Calculate Poisson's ratio from bulk and shear moduli.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn poisson_ratio(bulk: f64, shear: f64) -> f64 {
    elastic::poisson_ratio(bulk, shear)
}

/// Check if an elastic tensor indicates mechanical stability.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn is_stable(tensor: [[f64; 6]; 6]) -> bool {
    elastic::is_mechanically_stable(&tensor)
}

/// Calculate the Zener anisotropy ratio.
#[gen_stub_pyfunction(module = "ferrox._ferrox.elastic")]
#[pyfunction]
fn zener_ratio(c11: f64, c12: f64, c44: f64) -> f64 {
    elastic::zener_ratio(c11, c12, c44)
}

/// Register elastic functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(generate_strains, module)?)?;
    module.add_function(wrap_pyfunction!(apply_strain, module)?)?;
    module.add_function(wrap_pyfunction!(stress_to_voigt, module)?)?;
    module.add_function(wrap_pyfunction!(strain_to_voigt, module)?)?;
    module.add_function(wrap_pyfunction!(tensor_from_stresses, module)?)?;
    module.add_function(wrap_pyfunction!(bulk_modulus, module)?)?;
    module.add_function(wrap_pyfunction!(shear_modulus, module)?)?;
    module.add_function(wrap_pyfunction!(youngs_modulus, module)?)?;
    module.add_function(wrap_pyfunction!(poisson_ratio, module)?)?;
    module.add_function(wrap_pyfunction!(is_stable, module)?)?;
    module.add_function(wrap_pyfunction!(zener_ratio, module)?)?;
    Ok(())
}
