use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Build a reverse mapping from alias -> field_name given a forward mapping
/// of field_name -> alias. If a field has no alias (alias == field_name),
/// it still gets an identity entry.
///
/// This is called once per model class and cached.
#[pyfunction]
pub fn build_reverse_alias_map<'py>(
    py: Python<'py>,
    field_alias_map: &Bound<'py, PyDict>,
) -> PyResult<Bound<'py, PyDict>> {
    let result = PyDict::new(py);
    for (key, value) in field_alias_map.iter() {
        let field_name: String = key.extract()?;
        let alias: String = value.extract()?;
        // Map alias -> field_name
        result.set_item(&alias, &field_name)?;
        // Also keep field_name -> field_name for identity lookups
        if alias != field_name {
            result.set_item(&field_name, &field_name)?;
        }
    }
    Ok(result)
}
