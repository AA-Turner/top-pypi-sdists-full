//! Python bindings for the `jsonata` Rust port (PyO3).
//!
//! ```python
//! import jsonata
//! expr = jsonata.Jsonata("foo.bar")
//! expr.evaluate({"foo": {"bar": 42}})   # -> 42
//! ```

use std::rc::Rc;

use jsonata_core::frame::Frame;
use jsonata_core::value::{ArrayFlags, JValue, Object};
use jsonata_core::{JError, Jsonata as CoreJsonata};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString, PyTuple};

// ---------------------------------------------------------------------------
// Python <-> JValue conversion
// ---------------------------------------------------------------------------

/// Convert a Python object into a JSONata value. `None` maps to JSON null.
fn py_to_jvalue(obj: &Bound<'_, PyAny>) -> PyResult<JValue> {
    if obj.is_none() {
        return Ok(JValue::Null);
    }
    // bool must be checked before int (bool is a subclass of int in Python)
    if let Ok(b) = obj.cast::<PyBool>() {
        return Ok(JValue::Bool(b.is_true()));
    }
    if obj.cast::<PyInt>().is_ok() {
        let v: i64 = obj.extract()?;
        return Ok(JValue::Number(v as f64));
    }
    if obj.cast::<PyFloat>().is_ok() {
        let v: f64 = obj.extract()?;
        return Ok(JValue::Number(v));
    }
    if obj.cast::<PyString>().is_ok() {
        // `extract::<String>()` works under the limited (abi3) API, unlike
        // `PyString::to_str` which needs PyUnicode_AsUTF8AndSize (>=3.10).
        let s: String = obj.extract()?;
        return Ok(JValue::string(s));
    }
    if let Ok(d) = obj.cast::<PyDict>() {
        let mut obj_map = Object::new();
        for (k, v) in d.iter() {
            let key: String = k
                .extract()
                .map_err(|_| PyValueError::new_err("JSONata object keys must be strings"))?;
            obj_map.insert(key, py_to_jvalue(&v)?);
        }
        return Ok(JValue::object(obj_map));
    }
    if let Ok(list) = obj.cast::<PyList>() {
        let mut items = Vec::with_capacity(list.len());
        for item in list.iter() {
            items.push(py_to_jvalue(&item)?);
        }
        return Ok(JValue::array(items, ArrayFlags::default()));
    }
    if let Ok(t) = obj.cast::<PyTuple>() {
        let mut items = Vec::with_capacity(t.len());
        for item in t.iter() {
            items.push(py_to_jvalue(&item)?);
        }
        return Ok(JValue::array(items, ArrayFlags::default()));
    }
    Err(PyValueError::new_err(format!(
        "Unsupported Python type for JSONata input: {}",
        obj.get_type().name()?
    )))
}

/// Convert a JSONata value back into a Python object. A JSON `null` always maps
/// to Python `None`; functions map to `None`. `undefined` (a no-match / absent
/// value) maps to `None` too, unless `preserve_undefined` is set — then it maps
/// to the `jsonata.UNDEFINED` sentinel so callers can tell it apart from a real
/// JSON `null`. `preserve_undefined` is driven by `set_output_convert_nulls`.
fn jvalue_to_py(py: Python<'_>, v: &JValue, preserve_undefined: bool) -> PyResult<Py<PyAny>> {
    Ok(match v {
        JValue::Undefined => {
            if preserve_undefined {
                undefined_singleton(py)?.into_any()
            } else {
                py.None()
            }
        }
        JValue::Null => py.None(),
        JValue::Bool(b) => b.into_pyobject(py)?.to_owned().unbind().into_any(),
        JValue::Number(n) => {
            if JValue::number_is_integral(*n) {
                (*n as i64).into_pyobject(py)?.into_any().unbind()
            } else {
                (*n).into_pyobject(py)?.into_any().unbind()
            }
        }
        JValue::String(s) => s.as_ref().into_pyobject(py)?.into_any().unbind(),
        JValue::Array(a, _) => {
            let list = PyList::empty(py);
            for item in a.iter() {
                list.append(jvalue_to_py(py, item, preserve_undefined)?)?;
            }
            list.into_any().unbind()
        }
        JValue::Object(o) => {
            let dict = PyDict::new(py);
            for (k, val) in o.iter() {
                dict.set_item(k, jvalue_to_py(py, val, preserve_undefined)?)?;
            }
            dict.into_any().unbind()
        }
        JValue::Lambda(_) | JValue::Native(_) | JValue::Partial(_) => py.None(),
        JValue::Regex(r) => r.pattern.as_str().into_pyobject(py)?.into_any().unbind(),
    })
}

/// Sentinel for a JSONata `undefined` (no-match / absent) result, returned in
/// place of `None` when null-conversion is disabled via
/// `set_output_convert_nulls(False)`. This lets callers distinguish a real JSON
/// `null` (Python `None`) from "the expression matched nothing".
#[pyclass(frozen, name = "UndefinedType", module = "jsonata")]
struct UndefinedType;

#[pymethods]
impl UndefinedType {
    fn __repr__(&self) -> &'static str {
        "jsonata.UNDEFINED"
    }
    fn __bool__(&self) -> bool {
        false
    }
}

/// The process-wide `jsonata.UNDEFINED` singleton.
static UNDEFINED: PyOnceLock<Py<UndefinedType>> = PyOnceLock::new();

fn undefined_singleton(py: Python<'_>) -> PyResult<Py<UndefinedType>> {
    UNDEFINED
        .get_or_try_init(py, || Py::new(py, UndefinedType))
        .map(|p| p.clone_ref(py))
}

/// Run `f`, converting a Rust panic into a catchable [`JsonataError`].
///
/// Without this, a panic crossing the PyO3 boundary is raised as
/// `pyo3.PanicException`, which deliberately inherits from `BaseException`
/// (like `KeyboardInterrupt`) — an `except Exception:` handler will NOT catch
/// it, so a single panicking evaluation can take down an application's event
/// loop. Panics are still bugs (please report them), but they should be
/// *catchable* bugs at the Python level.
///
/// This cannot help with non-unwinding failures (stack-overflow or OOM
/// aborts); the core's parse/eval depth caps exist to keep those out of
/// reach on default stacks.
fn catch_panic<T>(f: impl FnOnce() -> PyResult<T>) -> PyResult<T> {
    match std::panic::catch_unwind(std::panic::AssertUnwindSafe(f)) {
        Ok(r) => r,
        Err(payload) => {
            let msg = payload
                .downcast_ref::<&str>()
                .map(|s| s.to_string())
                .or_else(|| payload.downcast_ref::<String>().cloned())
                .unwrap_or_else(|| "unknown panic payload".to_string());
            let location = LAST_PANIC_LOCATION.with(|c| c.borrow_mut().take());
            let py_err = JsonataInternalError::new_err(format!(
                "internal error (Rust panic) during JSONata processing: {msg}"
            ));
            Python::attach(|py| {
                let val = py_err.value(py).as_any();
                // A stable, greppable code so upstream telemetry can bucket
                // these (regular JsonataErrors carry S/T/D/U catalog codes).
                let _ = val.setattr("code", "PANIC");
                let _ = val.setattr("position", -1);
                let _ = val.setattr("panic_location", location);
            });
            Err(py_err)
        }
    }
}

thread_local! {
    /// `file:line:col` of the most recent panic on this thread, recorded by
    /// the chained panic hook below (the unwind payload itself carries only
    /// the message, not the location).
    static LAST_PANIC_LOCATION: std::cell::RefCell<Option<String>> =
        const { std::cell::RefCell::new(None) };
}

/// Install (once, at module import) a panic hook that records the panic
/// location to a thread-local and then delegates to the previous hook, so
/// default stderr reporting and any host-installed hook keep working.
fn install_panic_recorder() {
    static ONCE: std::sync::Once = std::sync::Once::new();
    ONCE.call_once(|| {
        let prev = std::panic::take_hook();
        std::panic::set_hook(Box::new(move |info| {
            let loc = info
                .location()
                .map(|l| format!("{}:{}:{}", l.file(), l.line(), l.column()));
            LAST_PANIC_LOCATION.with(|c| *c.borrow_mut() = loc);
            prev(info);
        }));
    });
}

fn to_pyerr(e: JError) -> PyErr {
    let py_err = JsonataError::new_err(e.message());
    Python::attach(|py| {
        let val = py_err.value(py).as_any();
        let _ = val.setattr("code", e.error.clone());
        let _ = val.setattr("position", e.location);
    });
    py_err
}

// ---------------------------------------------------------------------------
// Python classes
// ---------------------------------------------------------------------------

pyo3::create_exception!(
    jsonata,
    JsonataError,
    pyo3::exceptions::PyException,
    "Raised for any JSONata compile-time or evaluation error.\n\n\
     Instances raised by this library carry `code` (the JSONata catalog error\n\
     code, e.g. \"S0201\") and `position` (a character offset into the\n\
     expression) attributes."
);
pyo3::create_exception!(
    jsonata,
    JsonataInternalError,
    JsonataError,
    "An internal error (Rust panic) occurred during JSONata processing.\n\n\
     These indicate a bug in the jsonata engine, not in the expression or the\n\
     input data — please report them. Attributes for telemetry: `code` is\n\
     always the string \"PANIC\", `panic_location` is the Rust `file:line:col`\n\
     that panicked (or None), and the message carries the panic payload.\n\n\
     Subclasses JsonataError, so existing handlers keep catching it."
);

/// A compiled JSONata expression.
#[pyclass(unsendable)]
struct Jsonata {
    inner: CoreJsonata,
    /// Optional `(timeout_ms, max_recursion_depth)` guard applied to every
    /// `evaluate` call. Set via `set_runtime_bounds`.
    runtime_bounds: Option<(i64, i32)>,
    /// Mirror of the core's `output_convert_nulls` flag so `evaluate` knows
    /// whether to surface `undefined` distinctly from JSON `null`.
    convert_nulls: bool,
}

#[pymethods]
impl Jsonata {
    /// Compile a JSONata expression. Raises `JsonataError` on a syntax error.
    #[new]
    fn new(expr: &str) -> PyResult<Self> {
        let inner = catch_panic(|| CoreJsonata::new(expr).map_err(to_pyerr))?;
        Ok(Jsonata {
            inner,
            runtime_bounds: None,
            convert_nulls: true,
        })
    }

    /// Evaluate the expression against `data`, with optional variable
    /// `bindings` (a dict mapping `$name` (without the `$`) to a value).
    #[pyo3(signature = (data=None, bindings=None))]
    fn evaluate(
        &self,
        py: Python<'_>,
        data: Option<Bound<'_, PyAny>>,
        bindings: Option<Bound<'_, PyDict>>,
    ) -> PyResult<Py<PyAny>> {
        let input = match data {
            Some(d) => catch_panic(|| py_to_jvalue(&d))?,
            None => JValue::Undefined,
        };
        // Build a bindings/bounds carrier frame if we have anything to carry.
        // The core reads runtime bounds off the frame passed to `evaluate`.
        let frame = if bindings.is_some() || self.runtime_bounds.is_some() {
            let f = Frame::new(None);
            {
                let mut fb = f.borrow_mut();
                if let Some(b) = bindings {
                    for (k, v) in b.iter() {
                        let key: String = k.extract()?;
                        fb.bind(&key, py_to_jvalue(&v)?);
                    }
                }
                if let Some((timeout_ms, max_depth)) = self.runtime_bounds {
                    fb.set_runtime_bounds(timeout_ms, max_depth);
                }
            }
            Some(f)
        } else {
            None
        };
        catch_panic(|| {
            let result = self.inner.evaluate(input, frame).map_err(to_pyerr)?;
            jvalue_to_py(py, &result, !self.convert_nulls)
        })
    }

    /// Set an evaluation timeout (milliseconds) and a maximum recursion depth,
    /// guarding against runaway/non-terminating expressions. Applies to every
    /// subsequent `evaluate` call (mirrors Java `Frame.setRuntimeBounds`).
    fn set_runtime_bounds(&mut self, timeout_ms: i64, max_recursion_depth: i32) {
        self.runtime_bounds = Some((timeout_ms, max_recursion_depth));
    }

    /// Control how JSON `null` and `undefined` (no-match) results are surfaced.
    /// When `True` (the default) both collapse to Python `None`. When `False`,
    /// a JSON `null` stays `None` while `undefined` becomes the
    /// `jsonata.UNDEFINED` sentinel, so the two can be told apart.
    fn set_output_convert_nulls(&mut self, convert: bool) {
        self.convert_nulls = convert;
        self.inner.set_output_convert_nulls(convert);
    }

    /// Assign a value to a variable available to the expression.
    fn assign(&mut self, name: &str, value: Bound<'_, PyAny>) -> PyResult<()> {
        catch_panic(|| {
            self.inner.assign(name, py_to_jvalue(&value)?);
            Ok(())
        })
    }

    /// Register a custom function callable from the expression as `$name(...)`.
    /// `func` is a Python callable; arguments and the return value are converted
    /// to/from JSONata values automatically.
    #[pyo3(signature = (name, func, signature=None))]
    fn register_function(
        &mut self,
        name: &str,
        func: Py<PyAny>,
        signature: Option<&str>,
    ) -> PyResult<()> {
        let closure = move |args: &[JValue]| -> Result<JValue, JError> {
            Python::attach(|py| {
                let mut py_args: Vec<Py<PyAny>> = Vec::with_capacity(args.len());
                for a in args {
                    // Custom-function args always use plain `None` for absent
                    // values (never the UNDEFINED sentinel).
                    py_args.push(jvalue_to_py(py, a, false).map_err(pyerr_to_jerr)?);
                }
                let tuple = PyTuple::new(py, py_args).map_err(pyerr_to_jerr)?;
                let res = func.call1(py, tuple).map_err(pyerr_to_jerr)?;
                py_to_jvalue(res.bind(py)).map_err(pyerr_to_jerr)
            })
        };
        self.inner
            .register_function(name, signature, Rc::new(closure));
        Ok(())
    }
}

fn pyerr_to_jerr(e: PyErr) -> JError {
    // Surface the Python error message; the harness only needs an error to be
    // raised. (Mirrors how jsonata-java wraps a thrown function error.)
    let mut je = JError::new("D3137");
    je.current = Some(JValue::string(e.to_string()));
    je
}

/// Convenience: parse + evaluate in one call.
#[pyfunction]
#[pyo3(signature = (expr, data=None, bindings=None))]
fn evaluate(
    py: Python<'_>,
    expr: &str,
    data: Option<Bound<'_, PyAny>>,
    bindings: Option<Bound<'_, PyDict>>,
) -> PyResult<Py<PyAny>> {
    let j = Jsonata::new(expr)?;
    j.evaluate(py, data, bindings)
}

#[pymodule]
fn jsonata(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Jsonata>()?;
    m.add_class::<UndefinedType>()?;
    m.add_function(wrap_pyfunction!(evaluate, m)?)?;
    m.add("JsonataError", m.py().get_type::<JsonataError>())?;
    m.add(
        "JsonataInternalError",
        m.py().get_type::<JsonataInternalError>(),
    )?;
    install_panic_recorder();
    m.add("UNDEFINED", undefined_singleton(m.py())?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
