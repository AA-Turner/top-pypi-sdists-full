#![allow(clippy::all, clippy::pedantic, clippy::nursery, missing_docs)]

// Module declarations for modular organization
pub mod handles;
pub mod helpers;
pub mod options;
pub mod types;

#[cfg(feature = "visitor")]
pub mod visitor;

pub mod conversion;

// Re-exports from modules for public API
pub use handles::ConversionOptionsHandle;
pub use options::{ConversionOptions, PreprocessingOptions};

#[cfg(feature = "inline-images")]
pub use types::InlineImageConfig;

#[cfg(feature = "inline-images")]
use conversion::{convert_with_inline_images, convert_with_inline_images_handle, convert_with_inline_images_json};

#[cfg(feature = "metadata")]
pub use types::MetadataConfig;

#[cfg(feature = "metadata")]
use conversion::{convert_with_metadata, convert_with_metadata_handle, convert_with_metadata_json};

use html_to_markdown_bindings_common::parse_conversion_options;
mod profiling;
use helpers::{run_with_guard_and_profile, to_py_err};
#[cfg(feature = "visitor")]
use html_to_markdown_rs::visitor::HtmlVisitor;
#[cfg(feature = "async-visitor")]
use once_cell::sync::OnceCell;
use pyo3::prelude::*;
#[cfg(feature = "async-visitor")]
use pyo3_async_runtimes::TaskLocals;
#[cfg(feature = "visitor")]
use std::cell::RefCell;
use std::path::PathBuf;
#[cfg(feature = "visitor")]
use std::rc::Rc;

#[cfg(feature = "async-visitor")]
pub static PYTHON_TASK_LOCALS: OnceCell<TaskLocals> = OnceCell::new();

#[cfg(feature = "async-visitor")]
fn init_python_event_loop(_py: Python) -> PyResult<()> {
    if PYTHON_TASK_LOCALS.get().is_some() {
        return Ok(());
    }

    let (tx, rx) = std::sync::mpsc::channel::<PyResult<TaskLocals>>();

    std::thread::spawn(move || {
        let result = Python::attach(|py| -> PyResult<()> {
            let asyncio = py.import("asyncio")?;
            let event_loop = asyncio.call_method0("new_event_loop")?;
            asyncio.call_method1("set_event_loop", (event_loop.clone(),))?;

            let locals = TaskLocals::new(event_loop.clone()).copy_context(py)?;
            let _ = tx.send(Ok(locals));

            event_loop.call_method0("run_forever")?;
            Ok(())
        });

        if let Err(err) = result {
            let _ = tx.send(Err(err));
        }
    });

    let task_locals = rx
        .recv()
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Failed to init async event loop"))??;

    PYTHON_TASK_LOCALS
        .set(task_locals)
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Python async context already initialized"))?;

    Ok(())
}

#[pyfunction]
fn start_profiling(output_path: &str, frequency: Option<i32>) -> PyResult<()> {
    let path = PathBuf::from(output_path);
    let freq = frequency.unwrap_or(1000);
    profiling::start(path, freq).map_err(to_py_err)?;
    Ok(())
}

#[pyfunction]
fn stop_profiling() -> PyResult<()> {
    profiling::stop().map_err(to_py_err)?;
    Ok(())
}

/// Convert HTML to Markdown.
///
/// Args:
///     html: HTML string to convert
///     options: Optional conversion configuration
///     visitor: Optional visitor for custom conversion logic (requires visitor feature)
///
/// Returns:
///     Markdown string
///
/// Raises:
///     ValueError: Invalid HTML or configuration
///
/// Example:
///     ```ignore
///     from html_to_markdown import convert, ConversionOptions
///
///     html = "<h1>Hello</h1><p>World</p>"
///     markdown = convert(html)
///
///     # With options
///     options = ConversionOptions(heading_style="atx")
///     markdown = convert(html, options)
///
///     # With visitor (visitor feature required)
///     class CustomVisitor:
///         def visit_text(self, ctx, text):
///            return {"type": "continue"}
///     markdown = convert(html, visitor=CustomVisitor())
///     ```
#[pyfunction]
#[cfg(feature = "visitor")]
#[pyo3(signature = (html, options=None, visitor=None))]
fn convert(
    py: Python<'_>,
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<String> {
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());

    let Some(visitor_py) = visitor else {
        return py
            .detach(move || run_with_guard_and_profile(|| html_to_markdown_rs::convert(&html, rust_options.clone())))
            .map_err(to_py_err);
    };

    let bridge = visitor::PyVisitorBridge::new(visitor_py);
    let visitor_handle = std::sync::Arc::new(std::sync::Mutex::new(bridge));

    py.detach(move || {
        run_with_guard_and_profile(|| {
            let rc_visitor: Rc<RefCell<dyn HtmlVisitor>> = {
                Python::attach(|py| {
                    let guard = visitor_handle.lock().unwrap();
                    let bridge_copy = visitor::PyVisitorBridge::new(guard.visitor.clone_ref(py));
                    Rc::new(RefCell::new(bridge_copy)) as Rc<RefCell<dyn HtmlVisitor>>
                })
            };
            html_to_markdown_rs::convert_with_visitor(&html, rust_options.clone(), Some(rc_visitor))
        })
    })
    .map_err(to_py_err)
}

#[pyfunction]
#[cfg(not(feature = "visitor"))]
#[pyo3(signature = (html, options=None, visitor=None))]
fn convert(
    py: Python<'_>,
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<String> {
    if visitor.is_some() {
        return Err(PyErr::new::<pyo3::exceptions::PyNotImplementedError, _>(
            "Visitor support requires the 'visitor' feature to be enabled",
        ));
    }
    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());
    py.detach(move || run_with_guard_and_profile(|| html_to_markdown_rs::convert(&html, rust_options.clone())))
        .map_err(to_py_err)
}

#[pyfunction]
#[pyo3(signature = (html, options_json=None))]
fn convert_json(py: Python<'_>, html: &str, options_json: Option<&str>) -> PyResult<String> {
    let html = html.to_owned();
    let rust_options = parse_conversion_options(options_json).map_err(to_py_err)?;
    py.detach(move || run_with_guard_and_profile(|| html_to_markdown_rs::convert(&html, rust_options.clone())))
        .map_err(to_py_err)
}

#[pyfunction]
#[pyo3(signature = (html, handle))]
fn convert_with_options_handle(py: Python<'_>, html: &str, handle: &ConversionOptionsHandle) -> PyResult<String> {
    let html = html.to_owned();
    let rust_options = handle.inner.clone();
    py.detach(move || run_with_guard_and_profile(|| html_to_markdown_rs::convert(&html, Some(rust_options.clone()))))
        .map_err(to_py_err)
}

#[pyfunction]
#[pyo3(signature = (options=None))]
fn create_options_handle(options: Option<ConversionOptions>) -> ConversionOptionsHandle {
    ConversionOptionsHandle::new_with_options(options)
}

#[pyfunction]
#[pyo3(signature = (options_json=None))]
fn create_options_handle_json(options_json: Option<&str>) -> PyResult<ConversionOptionsHandle> {
    let rust_options = parse_conversion_options(options_json)
        .map_err(to_py_err)?
        .unwrap_or_default();
    Ok(ConversionOptionsHandle::new_with_rust(rust_options))
}

/// Convert HTML to Markdown with a custom visitor.
///
/// Deprecated: Use convert() with the visitor parameter instead. All convert functions now accept optional visitors.
///
/// Example:
///     ```ignore
///     from html_to_markdown import convert
///     import warnings
///
///     class MyVisitor:
///         def visit_text(self, ctx, text):
///             return {"type": "continue"}
///
///     # Old way (deprecated):
///     # markdown = convert_with_visitor(html, visitor=MyVisitor())
///
///     # New way (recommended):
///     markdown = convert(html, visitor=MyVisitor())
///     ```
#[cfg(feature = "visitor")]
#[pyfunction]
#[pyo3(signature = (html, options=None, visitor=None))]
fn convert_with_visitor(
    py: Python<'_>,
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<String> {
    // NOTE: convert_with_visitor() is deprecated in favor of convert() with visitor parameter.
    // All convert functions now accept optional visitors. Example: convert(html, visitor=my_visitor)

    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());

    let Some(visitor_py) = visitor else {
        return py
            .detach(move || run_with_guard_and_profile(|| html_to_markdown_rs::convert(&html, rust_options.clone())))
            .map_err(to_py_err);
    };

    let bridge = visitor::PyVisitorBridge::new(visitor_py);
    let visitor_handle = std::sync::Arc::new(std::sync::Mutex::new(bridge));

    py.detach(move || {
        run_with_guard_and_profile(|| {
            let rc_visitor: Rc<RefCell<dyn HtmlVisitor>> = {
                Python::attach(|py| {
                    let guard = visitor_handle.lock().unwrap();
                    let bridge_copy = visitor::PyVisitorBridge::new(guard.visitor.clone_ref(py));
                    Rc::new(RefCell::new(bridge_copy)) as Rc<RefCell<dyn HtmlVisitor>>
                })
            };
            html_to_markdown_rs::convert_with_visitor(&html, rust_options.clone(), Some(rc_visitor))
        })
    })
    .map_err(to_py_err)
}

/// Convert HTML to Markdown with a custom visitor (async-compatible version).
///
/// This function provides async-compatible support for visitor methods using pyo3-async-runtimes
/// with proper event loop management. Supports both synchronous and asynchronous visitor methods.
///
/// The visitor object should define callback methods that return dictionaries:
/// - `def visit_text(ctx, text)`: Called for text nodes (can be async)
/// - `def visit_link(ctx, href, text, title)`: Called for links (can be async)
/// - And many others...
///
/// Each method should return a dict (or coroutine) with a 'type' key:
/// - `{"type": "continue"}` - Continue with default conversion
/// - `{"type": "skip"}` - Skip this element
/// - `{"type": "preserve_html"}` - Preserve original HTML
/// - `{"type": "custom", "output": "markdown"}` - Custom markdown output
/// - `{"type": "error", "message": "error"}` - Stop with error
///
/// Example:
///     ```ignore
///     from html_to_markdown import convert_with_async_visitor
///     import asyncio
///
///     class MyAsyncVisitor:
///         async def visit_text(self, ctx, text):
///             # Can perform async operations here
///             result = await some_async_operation()
///             return {"type": "continue"}
///
///     html = "<h1>Hello</h1><p>World</p>"
///     markdown = await convert_with_async_visitor(html, visitor=MyAsyncVisitor())
///     ```
#[cfg(feature = "async-visitor")]
#[pyfunction]
#[pyo3(signature = (html, options=None, visitor=None))]
fn convert_with_async_visitor(
    py: Python<'_>,
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<String> {
    init_python_event_loop(py)?;

    let html = html.to_owned();
    let rust_options = options.map(|opts| opts.to_rust());

    let Some(visitor_py) = visitor else {
        return py
            .detach(move || run_with_guard_and_profile(|| html_to_markdown_rs::convert(&html, rust_options.clone())))
            .map_err(to_py_err);
    };

    let visitor_handle = std::sync::Arc::new(std::sync::Mutex::new(visitor_py));

    py.detach(move || {
        run_with_guard_and_profile(|| {
            let rc_visitor: Rc<RefCell<dyn HtmlVisitor>> = {
                Python::attach(|py| {
                    let guard = visitor_handle.lock().unwrap();
                    let bridge_copy = visitor::PyAsyncVisitorBridge::new(guard.clone_ref(py));
                    Rc::new(RefCell::new(bridge_copy)) as Rc<RefCell<dyn HtmlVisitor>>
                })
            };
            html_to_markdown_rs::convert_with_visitor(&html, rust_options.clone(), Some(rc_visitor))
        })
    })
    .map_err(to_py_err)
}

/// Fallback for when async-visitor feature is not enabled
#[cfg(all(feature = "visitor", not(feature = "async-visitor")))]
#[pyfunction]
#[pyo3(signature = (html, options=None, visitor=None))]
fn convert_with_async_visitor(
    py: Python<'_>,
    html: &str,
    options: Option<ConversionOptions>,
    visitor: Option<Py<PyAny>>,
) -> PyResult<String> {
    convert_with_visitor(py, html, options, visitor)
}

/// Python bindings for html-to-markdown
#[pymodule]
fn _html_to_markdown(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert, m)?)?;
    m.add_function(wrap_pyfunction!(convert_json, m)?)?;
    m.add_function(wrap_pyfunction!(convert_with_options_handle, m)?)?;
    m.add_function(wrap_pyfunction!(create_options_handle, m)?)?;
    m.add_function(wrap_pyfunction!(create_options_handle_json, m)?)?;
    m.add_class::<ConversionOptions>()?;
    m.add_class::<PreprocessingOptions>()?;
    m.add_class::<ConversionOptionsHandle>()?;
    #[cfg(feature = "inline-images")]
    {
        m.add_function(wrap_pyfunction!(convert_with_inline_images, m)?)?;
        m.add_function(wrap_pyfunction!(convert_with_inline_images_json, m)?)?;
        m.add_function(wrap_pyfunction!(convert_with_inline_images_handle, m)?)?;
        m.add_class::<InlineImageConfig>()?;
    }
    #[cfg(feature = "metadata")]
    {
        m.add_function(wrap_pyfunction!(convert_with_metadata, m)?)?;
        m.add_function(wrap_pyfunction!(convert_with_metadata_json, m)?)?;
        m.add_function(wrap_pyfunction!(convert_with_metadata_handle, m)?)?;
        m.add_class::<MetadataConfig>()?;
    }
    #[cfg(feature = "visitor")]
    {
        m.add_function(wrap_pyfunction!(convert_with_visitor, m)?)?;
        m.add_function(wrap_pyfunction!(convert_with_async_visitor, m)?)?;
    }
    m.add_function(wrap_pyfunction!(start_profiling, m)?)?;
    m.add_function(wrap_pyfunction!(stop_profiling, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_convert_returns_markdown() {
        Python::initialize();
        Python::attach(|py| -> PyResult<()> {
            let html = "<h1>Hello</h1>";
            let result = convert(py, html, None, None)?;
            assert!(result.contains("Hello"));
            Ok(())
        })
        .expect("conversion succeeds");
    }

    #[test]
    fn test_conversion_options_defaults() {
        let opts = ConversionOptions::new(
            "underlined".to_string(),
            "spaces".to_string(),
            4,
            "*+-".to_string(),
            '*',
            false,
            false,
            false,
            false,
            "".to_string(),
            true,
            false,
            false,
            true,
            "double-equal".to_string(),
            true,
            "normalized".to_string(),
            false,
            false,
            80,
            false,
            "".to_string(),
            "".to_string(),
            "spaces".to_string(),
            "indented".to_string(),
            Vec::new(),
            None,
            false,
            Vec::new(),
            Vec::new(),
            "utf-8".to_string(),
            false,
            "markdown".to_string(),
        );
        let rust_opts = opts.to_rust();
        assert_eq!(rust_opts.list_indent_width, 4);
        assert_eq!(rust_opts.wrap_width, 80);
    }

    #[test]
    fn test_preprocessing_options_conversion() {
        let preprocessing = PreprocessingOptions::new(true, "aggressive".to_string(), true, false);
        let rust_preprocessing = preprocessing.to_rust();
        assert!(rust_preprocessing.enabled);
        assert!(matches!(
            rust_preprocessing.preset,
            html_to_markdown_rs::PreprocessingPreset::Aggressive
        ));
        assert!(rust_preprocessing.remove_navigation);
        assert!(!rust_preprocessing.remove_forms);
    }
}
