mod alias_utils;
mod group_related;
mod hash_item;
mod merge_instances;
mod merge_items;
mod parsers;
mod translate_list;
mod unique_list;

use pyo3::prelude::*;

/// Rust-accelerated utility functions for ormar ORM.
#[pymodule]
fn ormar_rust_utils(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parsers::encode_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(parsers::decode_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(parsers::encode_json, m)?)?;
    m.add_function(wrap_pyfunction!(hash_item::hash_item, m)?)?;
    m.add_function(wrap_pyfunction!(translate_list::translate_list_to_dict, m)?)?;
    m.add_function(wrap_pyfunction!(group_related::group_related_list, m)?)?;
    m.add_class::<unique_list::UniqueList>()?;
    m.add_function(wrap_pyfunction!(merge_instances::group_by_pk, m)?)?;
    m.add_function(wrap_pyfunction!(merge_items::plan_merge_items_lists, m)?)?;
    m.add_function(wrap_pyfunction!(alias_utils::build_reverse_alias_map, m)?)?;
    Ok(())
}
