use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use std::collections::BTreeMap;

/// Translates a list of related strings into a nested dictionary.
#[pyfunction]
pub fn group_related_list(py: Python<'_>, list_: Vec<String>) -> PyResult<PyObject> {
    group_related_inner(py, &list_)
}

fn group_related_inner(py: Python<'_>, list_: &[String]) -> PyResult<PyObject> {
    let mut groups: BTreeMap<String, Vec<String>> = BTreeMap::new();

    let mut sorted_list: Vec<&String> = list_.iter().collect();
    sorted_list.sort_by(|a, b| {
        let a_first = a.split("__").next().unwrap_or("");
        let b_first = b.split("__").next().unwrap_or("");
        a_first.cmp(b_first)
    });

    for item in &sorted_list {
        let parts: Vec<&str> = item.splitn(2, "__").collect();
        let key = parts[0].to_string();
        let rest = if parts.len() > 1 {
            Some(parts[1].to_string())
        } else {
            None
        };

        let entry = groups.entry(key).or_default();
        if let Some(r) = rest {
            entry.push(r);
        }
    }

    let mut result_items: Vec<(String, PyObject)> = Vec::new();

    for (key, mut children) in groups {
        children.sort();

        let has_nested = children.iter().any(|x| x.contains("__"));

        if has_nested {
            let nested = group_related_inner(py, &children)?;
            result_items.push((key, nested));
        } else {
            let py_list = PyList::new(py, &children)?;
            result_items.push((key, py_list.unbind().into()));
        }
    }

    // Sort by length of values, then by key
    result_items.sort_by(|a, b| {
        let a_len = a.1.bind(py).len().unwrap_or(0);
        let b_len = b.1.bind(py).len().unwrap_or(0);
        a_len.cmp(&b_len).then_with(|| a.0.cmp(&b.0))
    });

    let dict = PyDict::new(py);
    for (key, value) in &result_items {
        dict.set_item(key, value)?;
    }

    Ok(dict.unbind().into())
}
