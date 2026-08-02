use pyo3::prelude::*;
use std::collections::HashMap;

/// Creates a merge plan for two lists of items identified by PK hashes.
///
/// Returns Vec<(current_idx, Option<other_idx>)> where:
/// - current_idx is the index in current_pks
/// - other_idx is Some(index) in other_pks if a matching PK was found, None otherwise
///
/// This replaces Python's O(n^2) linear scan with O(n) hash lookups.
///
/// Parameters:
/// - current_pks: list of PK values from the current field list
/// - other_pks: list of PK values from the other list
#[pyfunction]
pub fn plan_merge_items_lists(
    py: Python<'_>,
    current_pks: Vec<PyObject>,
    other_pks: Vec<PyObject>,
) -> PyResult<Vec<(usize, Option<usize>)>> {
    // Build hash map from other_pks: hash -> index
    let mut other_map: HashMap<u64, usize> = HashMap::with_capacity(other_pks.len());
    for (idx, pk) in other_pks.iter().enumerate() {
        let hash = pk.bind(py).hash()? as u64;
        other_map.entry(hash).or_insert(idx);
    }

    let mut plan = Vec::with_capacity(current_pks.len());
    for (idx, pk) in current_pks.iter().enumerate() {
        let hash = pk.bind(py).hash()? as u64;
        let other_idx = other_map.get(&hash).copied();
        plan.push((idx, other_idx));
    }

    Ok(plan)
}
