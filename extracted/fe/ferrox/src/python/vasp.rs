//! Python bindings for VASP file format support (CHGCAR parsing, Fourier extraction).

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3_stub_gen::derive::gen_stub_pyfunction;
use std::path::Path;

use super::helpers::structure_to_pydict;
use crate::io::vasp::chgcar;

/// Convert a FourierResult to a Python dict with all keys.
fn fourier_result_to_pydict<'py>(
    py: Python<'py>,
    result: chgcar::FourierResult,
) -> PyResult<Bound<'py, PyDict>> {
    let dict = PyDict::new(py);
    dict.set_item("hkl_range", result.hkl_range.to_vec())?;
    dict.set_item("g_max", result.g_max)?;
    dict.set_item("lattice", result.lattice.to_vec())?;
    dict.set_item("recip_lattice", result.recip_lattice.to_vec())?;
    dict.set_item("grid_shape", result.grid_shape.to_vec())?;
    dict.set_item("g_nyquist", result.g_nyquist)?;
    dict.set_item("is_spin_polarized", result.is_spin_polarized)?;
    dict.set_item("total_electrons", result.total_electrons)?;
    dict.set_item("total_magnetization", result.total_magnetization)?;
    dict.set_item("coeff_shape", result.coeff_shape.to_vec())?;
    dict.set_item("n_coeffs_inside_sphere", result.n_coeffs_inside_sphere)?;
    dict.set_item("volume", result.volume)?;
    dict.set_item("rho_real", result.rho_real)?;
    dict.set_item("rho_imag", result.rho_imag)?;
    if let Some(down_real) = result.rho_down_real {
        dict.set_item("rho_down_real", down_real)?;
    }
    if let Some(down_imag) = result.rho_down_imag {
        dict.set_item("rho_down_imag", down_imag)?;
    }
    Ok(dict)
}

/// Parse a VASP CHGCAR file and return structure dict + volumetric grid data.
///
/// Returns a dict with keys:
///   - "structure": pymatgen-style structure dict
///   - "grid_shape": [NGX, NGY, NGZ]
///   - "total": flat list of charge density * volume values (C-ordered)
///   - "diff": flat list of spin-difference values (None if non-spin-polarized)
///   - "is_spin_polarized": bool
#[gen_stub_pyfunction(module = "ferrox._ferrox.vasp")]
#[pyfunction]
fn parse_chgcar(py: Python<'_>, path: &str) -> PyResult<Py<PyDict>> {
    let data = chgcar::parse_chgcar(Path::new(path))
        .map_err(|err| pyo3::exceptions::PyValueError::new_err(format!("{err}")))?;

    let result = PyDict::new(py);
    result.set_item("structure", structure_to_pydict(py, &data.structure)?)?;
    result.set_item("grid_shape", data.grid_shape.to_vec())?;
    result.set_item("is_spin_polarized", data.diff.is_some())?;
    match data.diff {
        Some(diff) => result.set_item("diff", diff)?,
        None => result.set_item("diff", py.None())?,
    }
    result.set_item("total", data.total)?;

    Ok(result.unbind())
}

/// Extract low-frequency Fourier coefficients from a VASP CHGCAR file.
///
/// Parses the CHGCAR, performs 3D FFT, and extracts all G-vectors within
/// |G| < g_max. Returns a dict with Fourier coefficients and metadata.
///
/// Args:
///     path: Path to CHGCAR file (plain or gzipped).
///     g_max: Maximum |G| cutoff in Angstrom^-1. Default: `DEFAULT_G_MAX` (8.0).
///
/// Returns:
///     Dict with keys: hkl_range, g_max, lattice, recip_lattice, grid_shape,
///     g_nyquist, is_spin_polarized, total_electrons, total_magnetization,
///     coeff_shape, n_coeffs_inside_sphere, volume,
///     rho_real, rho_imag (and rho_down_real/imag if spin-polarized).
#[gen_stub_pyfunction(module = "ferrox._ferrox.vasp")]
#[pyfunction]
#[pyo3(signature = (path, g_max=None))]
fn extract_fourier_from_chgcar(
    py: Python<'_>,
    path: &str,
    g_max: Option<f64>,
) -> PyResult<Py<PyDict>> {
    let g_max = g_max.unwrap_or(chgcar::DEFAULT_G_MAX);
    let data = chgcar::parse_chgcar(Path::new(path))
        .map_err(|err| pyo3::exceptions::PyValueError::new_err(format!("{err}")))?;
    let result = chgcar::extract_fourier_modes(&data, g_max)
        .map_err(|err| pyo3::exceptions::PyValueError::new_err(format!("{err}")))?;
    Ok(fourier_result_to_pydict(py, result)?.unbind())
}

/// Process multiple CHGCAR files in parallel and extract Fourier coefficients.
///
/// Uses rayon for file-level parallelism. Returns a list of result dicts
/// (same format as extract_fourier_from_chgcar) or error strings.
#[gen_stub_pyfunction(module = "ferrox._ferrox.vasp")]
#[pyfunction]
#[pyo3(signature = (paths, g_max=None))]
fn batch_extract_fourier(
    py: Python<'_>,
    paths: Vec<String>,
    g_max: Option<f64>,
) -> PyResult<Py<PyList>> {
    let g_max = g_max.unwrap_or(chgcar::DEFAULT_G_MAX);
    let (results, _elapsed) = py
        .detach(|| {
            let path_refs: Vec<&Path> = paths.iter().map(|p| Path::new(p.as_str())).collect();
            chgcar::process_batch(&path_refs, g_max)
        })
        .map_err(|err| pyo3::exceptions::PyValueError::new_err(format!("{err}")))?;

    let out = PyList::empty(py);
    for (idx, res) in results.into_iter().enumerate() {
        match res {
            Ok(result) => out.append(fourier_result_to_pydict(py, result)?)?,
            Err(err) => {
                let dict = PyDict::new(py);
                dict.set_item("error", err.to_string())?;
                dict.set_item("path", &paths[idx])?;
                out.append(dict)?;
            }
        }
    }

    Ok(out.unbind())
}

/// Register vasp functions on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_chgcar, module)?)?;
    module.add_function(wrap_pyfunction!(extract_fourier_from_chgcar, module)?)?;
    module.add_function(wrap_pyfunction!(batch_extract_fourier, module)?)?;
    Ok(())
}
