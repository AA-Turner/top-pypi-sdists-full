//! Chemical potential diagram Python bindings.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3_stub_gen::derive::gen_stub_pyfunction;

use crate::analysis::chempot::{
    compute_chempot_diagram as compute_chempot_diagram_rs, dedup_vertices,
    get_chempot_limits as get_chempot_limits_rs,
};
use crate::analysis::convex_hull::ConvexHullEntry;
use crate::composition::Composition;

/// Parse a `ConvexHullEntry` from a Python dict with keys:
/// `composition` (str or dict), `energy_per_atom` (float), and optional
/// `entry_id` (str), `energy` (float), `e_form_per_atom` (float), `correction` (float).
fn parse_chempot_entry(entry_idx: usize, entry: &Bound<'_, PyDict>) -> PyResult<ConvexHullEntry> {
    let composition_obj = entry.get_item("composition")?.ok_or_else(|| {
        PyValueError::new_err(format!("entries[{entry_idx}] missing 'composition'"))
    })?;

    let composition = if let Ok(formula) = composition_obj.extract::<String>() {
        Composition::from_formula(&formula).map_err(|err| {
            PyValueError::new_err(format!(
                "entries[{entry_idx}].composition formula parse failed: {err}"
            ))
        })?
    } else {
        let comp_dict = composition_obj.cast::<PyDict>().map_err(|_| {
            PyValueError::new_err(format!(
                "entries[{entry_idx}].composition must be a formula string or dict[str, float]"
            ))
        })?;
        let mut element_amounts = Vec::with_capacity(comp_dict.len());
        for (element_obj, amount_obj) in comp_dict.iter() {
            let symbol = element_obj.extract::<String>().map_err(|_| {
                PyValueError::new_err(format!(
                    "entries[{entry_idx}].composition keys must be element symbols"
                ))
            })?;
            let amount = amount_obj.extract::<f64>().map_err(|_| {
                PyValueError::new_err(format!(
                    "entries[{entry_idx}].composition[{symbol}] must be numeric"
                ))
            })?;
            if !amount.is_finite() || amount <= 0.0 {
                return Err(PyValueError::new_err(format!(
                    "entries[{entry_idx}].composition[{symbol}] must be finite and positive"
                )));
            }
            let element = crate::element::Element::from_symbol(&symbol).ok_or_else(|| {
                PyValueError::new_err(format!(
                    "entries[{entry_idx}].composition has unknown element: {symbol}"
                ))
            })?;
            element_amounts.push((element, amount));
        }
        Composition::from_elements(element_amounts)
    };

    let atom_count = composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(PyValueError::new_err(format!(
            "entries[{entry_idx}] has invalid atom count: {atom_count}"
        )));
    }

    let energy_total: Option<f64> = entry
        .get_item("energy")?
        .map(|val| val.extract::<f64>())
        .transpose()
        .map_err(|_| {
            PyValueError::new_err(format!("entries[{entry_idx}].energy must be numeric"))
        })?;

    let energy_per_atom: Option<f64> = entry
        .get_item("energy_per_atom")?
        .map(|val| val.extract::<f64>())
        .transpose()
        .map_err(|_| {
            PyValueError::new_err(format!(
                "entries[{entry_idx}].energy_per_atom must be numeric"
            ))
        })?;

    let e_form_per_atom: Option<f64> = entry
        .get_item("e_form_per_atom")?
        .map(|val| val.extract::<f64>())
        .transpose()
        .map_err(|_| {
            PyValueError::new_err(format!(
                "entries[{entry_idx}].e_form_per_atom must be numeric"
            ))
        })?;

    let correction: Option<f64> = entry
        .get_item("correction")?
        .map(|val| val.extract::<f64>())
        .transpose()
        .map_err(|_| {
            PyValueError::new_err(format!("entries[{entry_idx}].correction must be numeric"))
        })?;

    let energy = if let Some(total) = energy_total {
        total
    } else if let Some(per_atom) = energy_per_atom {
        per_atom * atom_count
    } else {
        return Err(PyValueError::new_err(format!(
            "entries[{entry_idx}] requires 'energy' or 'energy_per_atom'"
        )));
    };

    let entry_id: Option<String> = entry
        .get_item("entry_id")?
        .map(|val| val.extract::<String>())
        .transpose()
        .map_err(|_| {
            PyValueError::new_err(format!("entries[{entry_idx}].entry_id must be a string"))
        })?;

    Ok(ConvexHullEntry {
        entry_id,
        composition,
        energy,
        energy_per_atom,
        e_form_per_atom,
        correction,
    })
}

/// Compute a chemical potential diagram from phase entries.
///
/// Args:
///     entries: List of dicts with keys ``composition`` (str or dict[str, float]),
///         ``energy_per_atom`` or ``energy`` (float), and optionally
///         ``e_form_per_atom``, ``entry_id``, ``correction``.
///
/// Returns:
///     Dict with keys:
///     - ``elements``: list of element symbols (axis order)
///     - ``regions``: list of dicts with ``phase_name``, ``vertices``, ``e_form_per_atom``
///     - ``el_refs``: dict mapping element symbol to reference energy per atom
#[gen_stub_pyfunction(module = "ferrox._ferrox.chempot")]
#[pyfunction]
fn compute_chempot_diagram(
    py: Python<'_>,
    entries: Vec<Bound<'_, PyDict>>,
) -> PyResult<Py<PyDict>> {
    let hull_entries: Vec<ConvexHullEntry> = entries
        .iter()
        .enumerate()
        .map(|(idx, entry)| parse_chempot_entry(idx, entry))
        .collect::<PyResult<Vec<_>>>()?;

    let diagram = compute_chempot_diagram_rs(&hull_entries)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;

    let result = PyDict::new(py);

    let elements_list = PyList::new(py, diagram.elements.iter().map(|el| el.symbol()))
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    result.set_item("elements", elements_list)?;

    let regions_list: Vec<Py<PyDict>> = diagram
        .regions
        .iter()
        .map(|region| {
            let region_dict = PyDict::new(py);
            region_dict.set_item("phase_name", &region.phase_name)?;

            let unique_verts = dedup_vertices(&region.vertices, 1e-8);
            region_dict.set_item("vertices", &unique_verts)?;
            region_dict.set_item("e_form_per_atom", region.e_form_per_atom)?;
            Ok(region_dict.unbind())
        })
        .collect::<PyResult<Vec<_>>>()?;
    result.set_item("regions", regions_list)?;

    let el_refs_dict = PyDict::new(py);
    for (element, energy) in &diagram.el_refs {
        el_refs_dict.set_item(element.symbol(), energy)?;
    }
    result.set_item("el_refs", el_refs_dict)?;

    Ok(result.unbind())
}

/// Get per-element chemical potential bounds for a phase.
///
/// Args:
///     entries: List of entry dicts (same format as ``compute_chempot_diagram``).
///     phase: Phase name (reduced formula) to query.
///
/// Returns:
///     List of ``[min, max]`` pairs for each element axis, or ``None`` if
///     the phase has no stability region.
#[gen_stub_pyfunction(module = "ferrox._ferrox.chempot")]
#[pyfunction]
fn get_chempot_limits(
    entries: Vec<Bound<'_, PyDict>>,
    phase: &str,
) -> PyResult<Option<Vec<(f64, f64)>>> {
    let hull_entries: Vec<ConvexHullEntry> = entries
        .iter()
        .enumerate()
        .map(|(idx, entry)| parse_chempot_entry(idx, entry))
        .collect::<PyResult<Vec<_>>>()?;

    let diagram = compute_chempot_diagram_rs(&hull_entries)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;

    Ok(get_chempot_limits_rs(&diagram, phase))
}

/// Register chempot functions on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(compute_chempot_diagram, module)?)?;
    module.add_function(wrap_pyfunction!(get_chempot_limits, module)?)?;
    Ok(())
}
