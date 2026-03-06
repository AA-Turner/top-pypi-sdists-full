//! Convex-hull Python bindings.

use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pyfunction;
use std::collections::HashSet;

use crate::composition::Composition;
use crate::convex_hull::{ConvexHullEntry, calculate_e_above_hull as calculate_e_above_hull_rs};

fn parse_optional_f64(
    label: &str,
    entry_idx: usize,
    entry: &Bound<'_, PyDict>,
    field_name: &str,
) -> PyResult<Option<f64>> {
    match entry.get_item(field_name)? {
        Some(value) => {
            let value = value.extract::<f64>().map_err(|_| {
                PyValueError::new_err(format!("{label}[{entry_idx}].{field_name} must be numeric"))
            })?;
            if !value.is_finite() {
                return Err(PyValueError::new_err(format!(
                    "{label}[{entry_idx}].{field_name} must be finite"
                )));
            }
            Ok(Some(value))
        }
        None => Ok(None),
    }
}

fn parse_optional_string(
    label: &str,
    entry_idx: usize,
    entry: &Bound<'_, PyDict>,
    field_name: &str,
) -> PyResult<Option<String>> {
    match entry.get_item(field_name)? {
        Some(value) => value.extract::<String>().map(Some).map_err(|_| {
            PyValueError::new_err(format!(
                "{label}[{entry_idx}].{field_name} must be a string"
            ))
        }),
        None => Ok(None),
    }
}

fn parse_composition_from_py(
    label: &str,
    entry_idx: usize,
    composition_obj: &Bound<'_, PyAny>,
) -> PyResult<Composition> {
    if let Ok(formula) = composition_obj.extract::<String>() {
        return Composition::from_formula(&formula).map_err(|err| {
            PyValueError::new_err(format!(
                "{label}[{entry_idx}].composition formula parse failed: {err}"
            ))
        });
    }

    let comp_dict = composition_obj.cast::<PyDict>().map_err(|_| {
        PyValueError::new_err(format!(
            "{label}[{entry_idx}].composition must be a formula string or dict[str, float]"
        ))
    })?;

    let mut element_amounts = Vec::with_capacity(comp_dict.len());
    for (element_obj, amount_obj) in comp_dict.iter() {
        let element_symbol = element_obj.extract::<String>().map_err(|_| {
            PyValueError::new_err(format!(
                "{label}[{entry_idx}].composition keys must be element symbols"
            ))
        })?;
        let amount_value = amount_obj.extract::<f64>().map_err(|_| {
            PyValueError::new_err(format!(
                "{label}[{entry_idx}].composition[{element_symbol}] must be numeric"
            ))
        })?;
        if !amount_value.is_finite() || amount_value <= 0.0 {
            return Err(PyValueError::new_err(format!(
                "{label}[{entry_idx}].composition[{element_symbol}] must be finite and positive"
            )));
        }
        let element = crate::element::Element::from_symbol(&element_symbol).ok_or_else(|| {
            PyValueError::new_err(format!(
                "{label}[{entry_idx}].composition has unknown element symbol: {element_symbol}"
            ))
        })?;
        element_amounts.push((element, amount_value));
    }
    Ok(Composition::from_elements(element_amounts))
}

fn parse_hull_entry(
    label: &str,
    entry_idx: usize,
    entry: &Bound<'_, PyDict>,
) -> PyResult<ConvexHullEntry> {
    let composition_obj = entry.get_item("composition")?.ok_or_else(|| {
        PyValueError::new_err(format!("{label}[{entry_idx}] missing 'composition'"))
    })?;
    let composition = parse_composition_from_py(label, entry_idx, &composition_obj)?;

    let atom_count = composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(PyValueError::new_err(format!(
            "{label}[{entry_idx}] has invalid atom count: {atom_count}"
        )));
    }

    let energy_total = parse_optional_f64(label, entry_idx, entry, "energy")?;
    let energy_per_atom = parse_optional_f64(label, entry_idx, entry, "energy_per_atom")?;
    let e_form_per_atom = parse_optional_f64(label, entry_idx, entry, "e_form_per_atom")?;
    let correction = parse_optional_f64(label, entry_idx, entry, "correction")?;

    if let (Some(total_energy), Some(per_atom_energy)) = (energy_total, energy_per_atom)
        && ((total_energy / atom_count) - per_atom_energy).abs() > 1e-8
    {
        return Err(PyValueError::new_err(format!(
            "{label}[{entry_idx}] has inconsistent 'energy' and 'energy_per_atom'"
        )));
    }

    let energy = if let Some(total_energy) = energy_total {
        total_energy
    } else if let Some(per_atom_energy) = energy_per_atom {
        per_atom_energy * atom_count
    } else if e_form_per_atom.is_some() {
        f64::NAN
    } else {
        return Err(PyValueError::new_err(format!(
            "{label}[{entry_idx}] requires one of: energy, energy_per_atom, e_form_per_atom"
        )));
    };

    let entry_id = parse_optional_string(label, entry_idx, entry, "entry_id")?;
    Ok(ConvexHullEntry {
        entry_id,
        composition,
        energy,
        energy_per_atom,
        e_form_per_atom,
        correction,
    })
}

fn parse_hull_entries(
    entries: &[Bound<'_, PyDict>],
    label: &str,
) -> PyResult<Vec<ConvexHullEntry>> {
    entries
        .iter()
        .enumerate()
        .map(|(entry_idx, entry)| parse_hull_entry(label, entry_idx, entry))
        .collect()
}

fn parse_query_and_refs(
    entries: Vec<Bound<'_, PyDict>>,
    reference_entries: Option<Vec<Bound<'_, PyDict>>>,
) -> PyResult<(Vec<ConvexHullEntry>, Vec<ConvexHullEntry>)> {
    let query_entries = parse_hull_entries(&entries, "entries")?;
    let reference_entries = if let Some(reference_entries) = reference_entries {
        parse_hull_entries(&reference_entries, "reference_entries")?
    } else {
        query_entries.clone()
    };
    Ok((query_entries, reference_entries))
}

/// Calculate energy above hull for entries.
///
/// Returns a list of the same length and order as `entries`, where
/// result[i] is the energy above hull (in eV/atom) for entries[i].
///
/// If `reference_entries` is omitted, `entries` are used as both query and
/// reference set.
#[gen_stub_pyfunction(module = "ferrox._ferrox.convex_hull")]
#[pyfunction]
#[pyo3(signature = (entries, reference_entries = None))]
fn calculate_e_above_hull(
    entries: Vec<Bound<'_, PyDict>>,
    reference_entries: Option<Vec<Bound<'_, PyDict>>>,
) -> PyResult<Vec<f64>> {
    let (query_entries, ref_entries) = parse_query_and_refs(entries, reference_entries)?;
    calculate_e_above_hull_rs(&query_entries, &ref_entries)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Calculate energy above hull and return an id->value mapping.
///
/// Entry ids default to reduced formulas if `entry_id` is absent.
#[gen_stub_pyfunction(module = "ferrox._ferrox.convex_hull")]
#[pyfunction]
#[pyo3(signature = (entries, reference_entries = None))]
fn calculate_e_above_hull_map(
    py: Python<'_>,
    entries: Vec<Bound<'_, PyDict>>,
    reference_entries: Option<Vec<Bound<'_, PyDict>>>,
) -> PyResult<Py<PyDict>> {
    let (query_entries, ref_entries) = parse_query_and_refs(entries, reference_entries)?;
    let mut seen_ids: HashSet<String> = HashSet::with_capacity(query_entries.len());
    for entry in &query_entries {
        let entry_key = entry.id_or_formula();
        if !seen_ids.insert(entry_key.clone()) {
            return Err(PyValueError::new_err(format!(
                "Duplicate entry id in query entries: {entry_key}"
            )));
        }
    }

    let distances = calculate_e_above_hull_rs(&query_entries, &ref_entries)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    let query_count = query_entries.len();
    let distance_count = distances.len();
    if distance_count != query_count {
        return Err(PyRuntimeError::new_err(format!(
            "Length mismatch in calculate_e_above_hull_map: query_entries has {} entries but calculate_e_above_hull returned {} distances",
            query_count, distance_count
        )));
    }

    let result = PyDict::new(py);
    for (entry, distance) in query_entries.iter().zip(distances) {
        let entry_key = entry.id_or_formula();
        result.set_item(entry_key, distance)?;
    }
    Ok(result.unbind())
}

/// Register convex_hull functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(calculate_e_above_hull, module)?)?;
    module.add_function(wrap_pyfunction!(calculate_e_above_hull_map, module)?)?;
    Ok(())
}
