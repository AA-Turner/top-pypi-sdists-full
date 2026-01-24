//! Python visitor bridge implementations.
//!
//! This module provides the bridge between Python visitor objects and the Rust HtmlVisitor trait.

use super::types::{context_to_dict, result_from_dict};
use html_to_markdown_rs::visitor::{HtmlVisitor, NodeContext, VisitResult};
use pyo3::prelude::*;
use pyo3::types::PyAny;

#[cfg(feature = "async-visitor")]
use crate::PYTHON_TASK_LOCALS;

/// PyO3 wrapper around a Python visitor object.
///
/// This struct bridges Python callbacks to the Rust HtmlVisitor trait.
/// It holds a reference to a Python object and calls its methods dynamically.
#[derive(Debug)]
pub struct PyVisitorBridge {
    pub visitor: Py<PyAny>,
}

impl PyVisitorBridge {
    /// Create a new bridge wrapping a Python visitor object.
    pub const fn new(visitor: Py<PyAny>) -> Self {
        Self { visitor }
    }

    /// Call a Python visitor method and convert the result.
    fn call_visitor_method(
        &self,
        py: Python<'_>,
        method_name: &str,
        args: &[Bound<'_, PyAny>],
    ) -> PyResult<VisitResult> {
        let visitor_bound = self.visitor.bind(py);
        let method = match visitor_bound.getattr(method_name) {
            Ok(m) => m,
            Err(_) => {
                return Ok(VisitResult::Continue);
            }
        };

        let args_tuple = pyo3::types::PyTuple::new(py, args)?;

        let result = method.call(args_tuple, None)?;

        if result.is_none() {
            return Ok(VisitResult::Continue);
        }

        #[cfg(feature = "async-visitor")]
        if result.hasattr("__await__")? {
            let locals = PYTHON_TASK_LOCALS
                .get()
                .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("Async visitor event loop not initialized"))?;

            let fut = pyo3_async_runtimes::into_future_with_locals(locals, result)?;
            let py_result: Py<PyAny> = py.detach(|| pyo3_async_runtimes::tokio::get_runtime().block_on(fut))?;
            let result_dict: Bound<'_, pyo3::types::PyDict> = py_result.bind(py).extract()?;
            return result_from_dict(&result_dict);
        }

        let result_dict: Bound<'_, pyo3::types::PyDict> = result.extract()?;

        result_from_dict(&result_dict)
    }
}

// Macro to implement simple visitor methods that just pass context
macro_rules! impl_visit_ctx_only {
    ($self:ident, $ctx:ident, $method:literal) => {{
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, $ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone()];
            $self
                .call_visitor_method(py, $method, &args)
                .unwrap_or(VisitResult::Continue)
        })
    }};
}

// Macro to implement visitor methods with context and one text arg
macro_rules! impl_visit_ctx_text {
    ($self:ident, $ctx:ident, $method:literal, $text:ident) => {{
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, $ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let text_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, $text).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), text_py];
            $self
                .call_visitor_method(py, $method, &args)
                .unwrap_or(VisitResult::Continue)
        })
    }};
}

// Macro to implement visitor methods with context and optional src
macro_rules! impl_visit_ctx_opt_src {
    ($self:ident, $ctx:ident, $method:literal, $src:ident) => {{
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, $ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let src_py: Bound<'_, PyAny> = match $src {
                Some(s) => pyo3::types::PyString::new(py, s).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), src_py];
            $self
                .call_visitor_method(py, $method, &args)
                .unwrap_or(VisitResult::Continue)
        })
    }};
}

impl HtmlVisitor for PyVisitorBridge {
    fn visit_element_start(&mut self, ctx: &NodeContext) -> VisitResult {
        impl_visit_ctx_only!(self, ctx, "visit_element_start")
    }

    fn visit_element_end(&mut self, ctx: &NodeContext, output: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_element_end", output)
    }

    fn visit_text(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_text", text)
    }

    fn visit_link(&mut self, ctx: &NodeContext, href: &str, text: &str, title: Option<&str>) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let href_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, href).as_any().clone();
            let text_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, text).as_any().clone();
            let title_py: Bound<'_, PyAny> = match title {
                Some(t) => pyo3::types::PyString::new(py, t).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), href_py, text_py, title_py];
            self.call_visitor_method(py, "visit_link", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_image(&mut self, ctx: &NodeContext, src: &str, alt: &str, title: Option<&str>) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let src_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, src).as_any().clone();
            let alt_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, alt).as_any().clone();
            let title_py: Bound<'_, PyAny> = match title {
                Some(t) => pyo3::types::PyString::new(py, t).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), src_py, alt_py, title_py];
            self.call_visitor_method(py, "visit_image", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_heading(&mut self, ctx: &NodeContext, level: u32, text: &str, id: Option<&str>) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let level_py: Bound<'_, PyAny> = pyo3::types::PyInt::new(py, level).as_any().clone();
            let text_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, text).as_any().clone();
            let id_py: Bound<'_, PyAny> = match id {
                Some(i) => pyo3::types::PyString::new(py, i).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), level_py, text_py, id_py];
            self.call_visitor_method(py, "visit_heading", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_code_block(&mut self, ctx: &NodeContext, lang: Option<&str>, code: &str) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let lang_py: Bound<'_, PyAny> = match lang {
                Some(l) => pyo3::types::PyString::new(py, l).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let code_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, code).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), lang_py, code_py];
            self.call_visitor_method(py, "visit_code_block", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_code_inline(&mut self, ctx: &NodeContext, code: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_code_inline", code)
    }

    fn visit_list_item(&mut self, ctx: &NodeContext, ordered: bool, marker: &str, text: &str) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let ordered_py: Bound<'_, PyAny> = pyo3::types::PyBool::new(py, ordered).as_any().clone();
            let marker_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, marker).as_any().clone();
            let text_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, text).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), ordered_py, marker_py, text_py];
            self.call_visitor_method(py, "visit_list_item", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_list_start(&mut self, ctx: &NodeContext, ordered: bool) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let ordered_py: Bound<'_, PyAny> = pyo3::types::PyBool::new(py, ordered).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), ordered_py];
            self.call_visitor_method(py, "visit_list_start", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_list_end(&mut self, ctx: &NodeContext, ordered: bool, output: &str) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let ordered_py: Bound<'_, PyAny> = pyo3::types::PyBool::new(py, ordered).as_any().clone();
            let output_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, output).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), ordered_py, output_py];
            self.call_visitor_method(py, "visit_list_end", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_table_start(&mut self, ctx: &NodeContext) -> VisitResult {
        impl_visit_ctx_only!(self, ctx, "visit_table_start")
    }

    fn visit_table_row(&mut self, ctx: &NodeContext, cells: &[String], is_header: bool) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let cells_py: Bound<'_, PyAny> = match pyo3::types::PyList::new(py, cells) {
                Ok(list) => list.as_any().clone(),
                Err(_) => return VisitResult::Continue,
            };
            let is_header_py: Bound<'_, PyAny> = pyo3::types::PyBool::new(py, is_header).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), cells_py, is_header_py];
            self.call_visitor_method(py, "visit_table_row", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_table_end(&mut self, ctx: &NodeContext, output: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_table_end", output)
    }

    fn visit_blockquote(&mut self, ctx: &NodeContext, content: &str, depth: usize) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let content_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, content).as_any().clone();
            let depth_py: Bound<'_, PyAny> = pyo3::types::PyInt::new(py, depth).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), content_py, depth_py];
            self.call_visitor_method(py, "visit_blockquote", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_strong(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_strong", text)
    }

    fn visit_emphasis(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_emphasis", text)
    }

    fn visit_strikethrough(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_strikethrough", text)
    }

    fn visit_underline(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_underline", text)
    }

    fn visit_subscript(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_subscript", text)
    }

    fn visit_superscript(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_superscript", text)
    }

    fn visit_mark(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_mark", text)
    }

    fn visit_line_break(&mut self, ctx: &NodeContext) -> VisitResult {
        impl_visit_ctx_only!(self, ctx, "visit_line_break")
    }

    fn visit_horizontal_rule(&mut self, ctx: &NodeContext) -> VisitResult {
        impl_visit_ctx_only!(self, ctx, "visit_horizontal_rule")
    }

    fn visit_custom_element(&mut self, ctx: &NodeContext, tag_name: &str, html: &str) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let tag_name_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, tag_name).as_any().clone();
            let html_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, html).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), tag_name_py, html_py];
            self.call_visitor_method(py, "visit_custom_element", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_definition_list_start(&mut self, ctx: &NodeContext) -> VisitResult {
        impl_visit_ctx_only!(self, ctx, "visit_definition_list_start")
    }

    fn visit_definition_term(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_definition_term", text)
    }

    fn visit_definition_description(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_definition_description", text)
    }

    fn visit_definition_list_end(&mut self, ctx: &NodeContext, output: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_definition_list_end", output)
    }

    fn visit_form(&mut self, ctx: &NodeContext, action: Option<&str>, method: Option<&str>) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let action_py: Bound<'_, PyAny> = match action {
                Some(a) => pyo3::types::PyString::new(py, a).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let method_py: Bound<'_, PyAny> = match method {
                Some(m) => pyo3::types::PyString::new(py, m).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), action_py, method_py];
            self.call_visitor_method(py, "visit_form", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_input(
        &mut self,
        ctx: &NodeContext,
        input_type: &str,
        name: Option<&str>,
        value: Option<&str>,
    ) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let input_type_py: Bound<'_, PyAny> = pyo3::types::PyString::new(py, input_type).as_any().clone();
            let name_py: Bound<'_, PyAny> = match name {
                Some(n) => pyo3::types::PyString::new(py, n).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let value_py: Bound<'_, PyAny> = match value {
                Some(v) => pyo3::types::PyString::new(py, v).as_any().clone(),
                None => py.None().bind(py).clone(),
            };
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), input_type_py, name_py, value_py];
            self.call_visitor_method(py, "visit_input", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_button(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_button", text)
    }

    fn visit_audio(&mut self, ctx: &NodeContext, src: Option<&str>) -> VisitResult {
        impl_visit_ctx_opt_src!(self, ctx, "visit_audio", src)
    }

    fn visit_video(&mut self, ctx: &NodeContext, src: Option<&str>) -> VisitResult {
        impl_visit_ctx_opt_src!(self, ctx, "visit_video", src)
    }

    fn visit_iframe(&mut self, ctx: &NodeContext, src: Option<&str>) -> VisitResult {
        impl_visit_ctx_opt_src!(self, ctx, "visit_iframe", src)
    }

    fn visit_details(&mut self, ctx: &NodeContext, open: bool) -> VisitResult {
        Python::attach(|py| {
            let ctx_dict = match context_to_dict(py, ctx) {
                Ok(d) => d,
                Err(_) => return VisitResult::Continue,
            };
            let open_py: Bound<'_, PyAny> = pyo3::types::PyBool::new(py, open).as_any().clone();
            let args: Vec<Bound<'_, PyAny>> = vec![ctx_dict.as_any().clone(), open_py];
            self.call_visitor_method(py, "visit_details", &args)
                .unwrap_or(VisitResult::Continue)
        })
    }

    fn visit_summary(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_summary", text)
    }

    fn visit_figure_start(&mut self, ctx: &NodeContext) -> VisitResult {
        impl_visit_ctx_only!(self, ctx, "visit_figure_start")
    }

    fn visit_figcaption(&mut self, ctx: &NodeContext, text: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_figcaption", text)
    }

    fn visit_figure_end(&mut self, ctx: &NodeContext, output: &str) -> VisitResult {
        impl_visit_ctx_text!(self, ctx, "visit_figure_end", output)
    }
}
