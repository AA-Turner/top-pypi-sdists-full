#[cfg(feature = "visitor")]
use html_to_markdown_rs::visitor::VisitResult;
use pyo3::prelude::*;
use pyo3::types::PyDict;

#[cfg(feature = "visitor")]
/// Convert a Python dictionary result to a VisitResult enum.
pub fn result_from_dict(result_dict: &Bound<'_, PyDict>) -> PyResult<VisitResult> {
    let result_type: String = result_dict
        .get_item("type")?
        .ok_or_else(|| pyo3::exceptions::PyTypeError::new_err("Visitor result dict must have 'type' key"))?
        .extract()?;

    match result_type.as_str() {
        "continue" => Ok(VisitResult::Continue),
        "skip" => Ok(VisitResult::Skip),
        "preserve_html" => Ok(VisitResult::PreserveHtml),
        "custom" => {
            let output: String = result_dict
                .get_item("output")?
                .ok_or_else(|| {
                    pyo3::exceptions::PyTypeError::new_err("Visitor 'custom' result must have 'output' key")
                })?
                .extract()?;
            Ok(VisitResult::Custom(output))
        }
        "error" => {
            let message: String = result_dict
                .get_item("message")?
                .ok_or_else(|| {
                    pyo3::exceptions::PyTypeError::new_err("Visitor 'error' result must have 'message' key")
                })?
                .extract()?;
            Ok(VisitResult::Error(message))
        }
        unknown => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown visitor result type: {}",
            unknown
        ))),
    }
}

#[cfg(feature = "visitor")]
/// Convert NodeContext to a Python dictionary.
pub fn context_to_dict<'a>(
    py: Python<'a>,
    ctx: &html_to_markdown_rs::visitor::NodeContext,
) -> PyResult<Bound<'a, PyDict>> {
    let dict = PyDict::new(py);

    let node_type_str = format!("{:?}", ctx.node_type).to_lowercase();
    dict.set_item("node_type", node_type_str)?;

    dict.set_item("tag_name", &ctx.tag_name)?;

    let attrs_dict = PyDict::new(py);
    for (k, v) in &ctx.attributes {
        attrs_dict.set_item(k, v)?;
    }
    dict.set_item("attributes", attrs_dict)?;

    dict.set_item("depth", ctx.depth)?;

    dict.set_item("index_in_parent", ctx.index_in_parent)?;

    match &ctx.parent_tag {
        Some(tag) => dict.set_item("parent_tag", tag)?,
        None => dict.set_item("parent_tag", py.None())?,
    }

    dict.set_item("is_inline", ctx.is_inline)?;

    Ok(dict)
}
