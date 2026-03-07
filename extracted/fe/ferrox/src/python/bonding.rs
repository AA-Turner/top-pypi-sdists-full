//! Bond detection Python bindings.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pyfunction;

use crate::analysis::bonding::{self, Bond, BondingStrategy};

use super::helpers::{StructureJson, check_site_idx, parse_struct};

/// Convert a Bond to a Python dict.
fn bond_to_pydict(py: Python<'_>, bond: &Bond) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);
    dict.set_item("site_idx_1", bond.site_idx_1)?;
    dict.set_item("site_idx_2", bond.site_idx_2)?;
    dict.set_item("distance", bond.distance)?;
    dict.set_item("image", bond.image)?;
    Ok(dict.unbind())
}

/// Parse a bonding strategy from the Python-facing string + optional parameters.
fn parse_strategy(strategy: &str, scale: f64, cutoff: f64) -> PyResult<BondingStrategy> {
    match strategy {
        "covalent_radius" => {
            if !scale.is_finite() || scale <= 0.0 {
                return Err(PyValueError::new_err(format!(
                    "scale must be positive and finite, got {scale}"
                )));
            }
            Ok(BondingStrategy::CovalentRadius { scale })
        }
        "max_distance" => {
            if !cutoff.is_finite() || cutoff <= 0.0 {
                return Err(PyValueError::new_err(format!(
                    "cutoff must be positive and finite, got {cutoff}"
                )));
            }
            Ok(BondingStrategy::MaxDistance { cutoff })
        }
        other => Err(PyValueError::new_err(format!(
            "Unknown bonding strategy '{other}'. Use 'covalent_radius' or 'max_distance'."
        ))),
    }
}

/// Find all bonds in a structure.
///
/// Args:
///     structure: Structure as JSON string or dict.
///     strategy: Bonding strategy name — "covalent_radius" (default) or "max_distance".
///     scale: Scale factor for covalent radius strategy (default: 1.1).
///     cutoff: Distance cutoff in Å for max_distance strategy (default: 3.0).
///
/// Returns:
///     List of bond dicts with keys: site_idx_1, site_idx_2, distance, image.
#[gen_stub_pyfunction(module = "ferrox._ferrox.bonding")]
#[pyfunction]
#[pyo3(signature = (structure, strategy = "covalent_radius", scale = 1.1, cutoff = 3.0))]
fn find_bonds(
    py: Python<'_>,
    structure: StructureJson,
    strategy: &str,
    scale: f64,
    cutoff: f64,
) -> PyResult<Vec<Py<PyDict>>> {
    let struc = parse_struct(&structure)?;
    let bond_strategy = parse_strategy(strategy, scale, cutoff)?;
    let bonds = bonding::find_bonds(&struc, &bond_strategy);

    bonds.iter().map(|bond| bond_to_pydict(py, bond)).collect()
}

/// Get bonds for a single site.
///
/// Args:
///     structure: Structure as JSON string or dict.
///     site_idx: Index of the site to query.
///     strategy: Bonding strategy name — "covalent_radius" (default) or "max_distance".
///     scale: Scale factor for covalent radius strategy (default: 1.1).
///     cutoff: Distance cutoff in Å for max_distance strategy (default: 3.0).
///
/// Returns:
///     List of bond dicts with keys: site_idx_1, site_idx_2, distance, image.
#[gen_stub_pyfunction(module = "ferrox._ferrox.bonding")]
#[pyfunction]
#[pyo3(signature = (structure, site_idx, strategy = "covalent_radius", scale = 1.1, cutoff = 3.0))]
fn get_bonded_neighbors(
    py: Python<'_>,
    structure: StructureJson,
    site_idx: usize,
    strategy: &str,
    scale: f64,
    cutoff: f64,
) -> PyResult<Vec<Py<PyDict>>> {
    let struc = parse_struct(&structure)?;
    check_site_idx(site_idx, struc.num_sites())?;
    let bond_strategy = parse_strategy(strategy, scale, cutoff)?;
    let bonds = bonding::get_bonded_neighbors(&struc, site_idx, &bond_strategy);

    bonds.iter().map(|bond| bond_to_pydict(py, bond)).collect()
}

/// Register bonding functions on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(find_bonds, module)?)?;
    module.add_function(wrap_pyfunction!(get_bonded_neighbors, module)?)?;
    Ok(())
}
