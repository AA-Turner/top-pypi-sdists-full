//! Python bindings for JSON Tools RS
//!
//! This module provides Python bindings for the unified JSONTools API
//! using PyO3. It exposes the complete JSONTools builder pattern API to Python
//! with support for both flattening and unflattening operations, collision handling,
//! and all advanced features.

#[cfg(feature = "python")]
use pyo3::exceptions::{PyRuntimeError, PyValueError};
#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use pyo3::sync::PyOnceLock;
#[cfg(feature = "python")]
use pyo3::types::{PyBytes, PyDict, PyList, PyModule, PyString};

#[cfg(feature = "python")]
use std::mem;
#[cfg(feature = "python")]
use std::sync::Mutex;

#[cfg(feature = "python")]
use indexmap::{IndexMap, IndexSet};

#[cfg(feature = "python")]
use arrow_array::{
    Array, ArrayRef, LargeStringArray, ListArray, RecordBatch, StringArray, StringViewArray,
};
#[cfg(feature = "python")]
use arrow_buffer::OffsetBuffer;
#[cfg(feature = "python")]
use arrow_schema::{DataType, Field, Schema};
#[cfg(feature = "python")]
use compact_str::CompactString;
#[cfg(feature = "python")]
use pyo3_arrow::{PyChunkedArray, PyTable};
#[cfg(feature = "python")]
use std::sync::Arc;

#[cfg(feature = "python")]
use crate::arrow_columnar::{raw_scalar_kind, ColumnBuilder, ColumnPlan, KindFlags, ListCell};
#[cfg(feature = "python")]
use crate::config::{ProcessingConfig, TypeConversionMode};
#[cfg(feature = "python")]
use crate::convert::convert_string_for_mode;
#[cfg(feature = "python")]
use crate::flatten::{escape_json_string, unescape_json_string, write_json_escaped_key};
#[cfg(feature = "python")]
use crate::transform::{apply_replacement_patterns, matches_any_pattern};
use crate::{JSONTools, JsonOutput};

#[cfg(feature = "python")]
pyo3::create_exception!(
    json_tools_rs,
    JsonToolsError,
    pyo3::exceptions::PyException,
    "Python exception for JSON Tools operations"
);

/// Lock the inner config mutex, converting poison errors to Python exceptions.
#[cfg(feature = "python")]
#[inline]
fn lock_config(mutex: &Mutex<JSONTools>) -> PyResult<std::sync::MutexGuard<'_, JSONTools>> {
    mutex
        .lock()
        .map_err(|e| PyRuntimeError::new_err(format!("internal config lock poisoned: {e}")))
}

/// JSON (de)serialization callables, resolved once per process and cached:
/// `orjson` (a hard dependency -- see `pyproject.toml`; 5-10x faster than
/// stdlib for the dict<->str conversion this module performs on every
/// dict-shaped call) with the stdlib `json` module kept alongside as a
/// per-call fallback for the inputs orjson can't handle (integers beyond
/// 64-bit range, arbitrary type subclasses, ...) -- retrying with stdlib on
/// an orjson error preserves stdlib's behavior and error surfaces for exactly
/// those inputs instead of changing them.
#[cfg(feature = "python")]
struct JsonCallables {
    /// `orjson.dumps`.
    dumps: Py<PyAny>,
    /// Kwargs for the dumps call: `{"option": orjson.OPT_NON_STR_KEYS}`, so
    /// int/float/bool/None dict keys are coerced to strings exactly like
    /// stdlib `json.dumps` does by default.
    dumps_kwargs: Py<PyDict>,
    /// stdlib `json.dumps` -- fallback when orjson rejects an input.
    stdlib_dumps: Py<PyAny>,
    /// `orjson.loads`.
    loads: Py<PyAny>,
    /// stdlib `json.loads` -- fallback: orjson rejects some JSON stdlib
    /// accepts (integers beyond 64-bit range).
    stdlib_loads: Py<PyAny>,
}

#[cfg(feature = "python")]
static JSON_CALLABLES: PyOnceLock<JsonCallables> = PyOnceLock::new();

/// Resolve (once) and return the cached JSON callables. Caching the bound
/// callables saves the per-call `sys.modules` lookup + `getattr` +
/// bound-method allocation that `py.import("json")?.call_method1(...)` costs.
#[cfg(feature = "python")]
fn json_callables(py: Python<'_>) -> PyResult<&'static JsonCallables> {
    JSON_CALLABLES.get_or_try_init(py, || {
        let json_mod = py.import("json")?;
        let stdlib_dumps = json_mod.getattr("dumps")?.unbind();
        let stdlib_loads = json_mod.getattr("loads")?.unbind();
        let orjson = py.import("orjson")?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("option", orjson.getattr("OPT_NON_STR_KEYS")?)?;
        Ok(JsonCallables {
            dumps: orjson.getattr("dumps")?.unbind(),
            dumps_kwargs: kwargs.unbind(),
            stdlib_dumps,
            loads: orjson.getattr("loads")?.unbind(),
            stdlib_loads,
        })
    })
}

/// Serialize a Python object to a JSON string using `orjson`, falling back to
/// Python's own (C-accelerated) `json` module for inputs orjson rejects --
/// never a Rust-side serde traversal.
///
/// Benchmarked against the previous `depythonize` + `sonic-rs` serialize
/// approach: for flat dicts the old approach was marginally faster (~25%),
/// but for the nested data this library's `.flatten()`/`.unflatten()` exist to
/// handle -- and for `list[dict]`/DataFrame batches, which are the realistic
/// call shape -- `depythonize` was 5-30% slower for a single nested dict, and
/// 2-3x slower for DataFrame rows, than just letting CPython's own hand-tuned
/// C `json` module do the conversion. orjson beats stdlib by a further 5-10x
/// on the same call shape.
#[cfg(feature = "python")]
#[inline]
fn py_dumps(py: Python<'_>, obj: &Bound<'_, PyAny>) -> PyResult<String> {
    let callables = json_callables(py)?;
    let result = match callables
        .dumps
        .bind(py)
        .call((obj,), Some(callables.dumps_kwargs.bind(py)))
    {
        Ok(out) => out,
        // orjson rejects inputs stdlib handles (ints beyond 64-bit, exotic
        // subclasses, ...) -- retry with stdlib so those inputs keep working
        // exactly as before, including stdlib's error messages when the
        // input is genuinely unserializable.
        Err(_) => callables.stdlib_dumps.bind(py).call1((obj,))?,
    };
    // orjson returns `bytes`; stdlib returns `str`.
    if let Ok(bytes) = result.cast::<PyBytes>() {
        std::str::from_utf8(bytes.as_bytes())
            .map(str::to_owned)
            .map_err(|e| {
                PyValueError::new_err(format!("JSON serializer produced non-UTF-8 output: {e}"))
            })
    } else {
        result.extract::<String>()
    }
}

/// True if `s` contains a run of >= 19 consecutive ASCII digits -- the only
/// way an integer literal outside 64-bit range can appear (i64::MAX has 19
/// digits). Used to guard orjson's `loads`, which silently parses such
/// integers as lossy floats where stdlib preserves them exactly (Python ints
/// are arbitrary-precision). Deliberately conservative: long digit runs
/// inside strings or float literals also match and just take the stdlib path.
///
/// Samples every 19th byte instead of scanning all of them: any 19-digit run
/// must contain a sampled position (consecutive samples are <= 19 apart), and
/// a sampled digit expands to its full run to measure the real length, with
/// the next sample resuming past the run's known non-digit end.
#[cfg(feature = "python")]
#[inline]
fn may_contain_big_int(s: &[u8]) -> bool {
    const RUN: usize = 19;
    let n = s.len();
    let mut i = 0;
    while i < n {
        if s[i].is_ascii_digit() {
            let mut start = i;
            while start > 0 && s[start - 1].is_ascii_digit() {
                start -= 1;
            }
            let mut end = i + 1;
            while end < n && s[end].is_ascii_digit() {
                end += 1;
            }
            if end - start >= RUN {
                return true;
            }
            // `end` is a known non-digit (or out of bounds), so the next run
            // starts at end+1 at the earliest and sampling end+RUN leaves at
            // most RUN-1 unsampled positions before it -- too short to hide
            // a qualifying run.
            i = end + RUN;
        } else {
            i += RUN;
        }
    }
    false
}

/// Deserialize a JSON string into a Python object using `orjson`, falling
/// back to Python's own `json` module for inputs orjson rejects. See
/// `py_dumps` for the rationale -- this is the output-side half of the same
/// design.
///
/// Documents that may contain integers beyond 64-bit range always take the
/// stdlib path: orjson parses those as lossy floats with no error to hook a
/// fallback on, and this library guarantees integer precision end-to-end.
#[cfg(feature = "python")]
#[inline]
fn py_loads<'py>(py: Python<'py>, json_str: &str) -> PyResult<Bound<'py, PyAny>> {
    let callables = json_callables(py)?;
    if !may_contain_big_int(json_str.as_bytes()) {
        // On an unexpected orjson failure over our own valid output, fall
        // through to stdlib so its behavior/error surface is what the caller
        // sees, exactly as before the accelerator existed.
        if let Ok(obj) = callables.loads.bind(py).call1((json_str,)) {
            return Ok(obj);
        }
    }
    callables.stdlib_loads.bind(py).call1((json_str,))
}

// =============================================================================
// DataFrame and Series Support Types
// =============================================================================

/// Type of DataFrame library detected via duck-typing.
///
/// Detection uses `type(obj).__module__` and `type(obj).__name__` to identify
/// the DataFrame variant without importing the library, falling back to
/// checking for `to_dict()` or `to_json()` methods for generic compatibility.
#[cfg(feature = "python")]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DataFrameType {
    /// pandas.DataFrame — uses `to_dict("records")` for row extraction
    Pandas,
    /// polars.DataFrame — uses `to_dicts()` for row extraction
    Polars,
    /// pyarrow.Table — uses `to_pydict()` for columnar extraction
    PyArrow,
    /// pyspark.sql.DataFrame — uses `toJSON().collect()` for distributed extraction
    PySpark,
    /// Any object with `to_dict()` or `to_json()` methods
    Generic,
}

/// Type of Series library detected via duck-typing.
///
/// Similar to `DataFrameType`, uses module/name introspection to identify
/// the Series variant, falling back to `to_list()` / `tolist()` for generics.
#[cfg(feature = "python")]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SeriesType {
    /// pandas.Series — uses `tolist()` for value extraction
    Pandas,
    /// polars.Series — uses `to_list()` for value extraction
    Polars,
    /// pyarrow.Array or pyarrow.ChunkedArray — uses `to_pylist()`
    PyArrow,
    /// pyspark.sql.Column (rare) — uses `collect()` for distributed extraction
    PySpark,
    /// Any object with `to_list()` or `tolist()` methods
    Generic,
}

/// Unified data structure type for detection.
///
/// Wraps either a DataFrame or Series detection result so the processing
/// pipeline can handle both types uniformly before dispatching to
/// type-specific extraction logic.
#[cfg(feature = "python")]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DataStructureType {
    /// A DataFrame-like object (tabular rows/columns)
    DataFrame(DataFrameType),
    /// A Series-like object (single column/array of values)
    Series(SeriesType),
}

/// Target DataFrame library for `PyJSONTools::execute`'s `normalise=True` path.
///
/// Distinct from `DataFrameType`/`SeriesType` above (which describe *detected*
/// input): this describes the *requested or resolved output* -- every processed
/// row becomes one row of the resulting table regardless of what shape the input
/// was (a bare `dict` produces a 1-row table just like a `DataFrame` produces an
/// N-row one). `Generic` has no equivalent here -- there's no single library to
/// reconstruct against for a duck-typed "has to_dict()" object.
#[cfg(feature = "python")]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum NormaliseTarget {
    Pandas,
    Polars,
    PyArrow,
    PySpark,
}

#[cfg(feature = "python")]
impl NormaliseTarget {
    /// Parse a user-supplied `target=` string. Errors list the valid values
    /// rather than falling back silently -- an explicit target is a promise to
    /// the caller that exactly this backend will be used.
    fn parse(s: &str) -> PyResult<Self> {
        match s {
            "pandas" => Ok(Self::Pandas),
            "polars" => Ok(Self::Polars),
            "pyarrow" => Ok(Self::PyArrow),
            "pyspark" => Ok(Self::PySpark),
            other => Err(JsonToolsError::new_err(format!(
                "Unknown normalise target {other:?}; expected one of \"pandas\", \"polars\", \"pyarrow\", \"pyspark\""
            ))),
        }
    }

    /// Also the pip/import name for all four -- reused for both.
    fn name(self) -> &'static str {
        match self {
            Self::Pandas => "pandas",
            Self::Polars => "polars",
            Self::PyArrow => "pyarrow",
            Self::PySpark => "pyspark",
        }
    }

    fn from_dataframe_type(t: DataFrameType) -> Option<Self> {
        match t {
            DataFrameType::Pandas => Some(Self::Pandas),
            DataFrameType::Polars => Some(Self::Polars),
            DataFrameType::PyArrow => Some(Self::PyArrow),
            DataFrameType::PySpark => Some(Self::PySpark),
            DataFrameType::Generic => None,
        }
    }

    fn from_series_type(t: SeriesType) -> Option<Self> {
        match t {
            SeriesType::Pandas => Some(Self::Pandas),
            SeriesType::Polars => Some(Self::Polars),
            SeriesType::PyArrow => Some(Self::PyArrow),
            SeriesType::PySpark => Some(Self::PySpark),
            SeriesType::Generic => None,
        }
    }
}

/// Python wrapper for JsonOutput enum
#[cfg(feature = "python")]
#[pyclass(name = "JsonOutput", module = "json_tools_rs", frozen, from_py_object)]
#[derive(Debug, Clone)]
pub struct PyJsonOutput {
    inner: JsonOutput,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyJsonOutput {
    /// Check if this is a single result
    #[getter]
    fn is_single(&self) -> bool {
        matches!(self.inner, JsonOutput::Single(_))
    }

    /// Check if this is a multiple result
    #[getter]
    fn is_multiple(&self) -> bool {
        matches!(self.inner, JsonOutput::Multiple(_))
    }

    /// Get the single result (raises ValueError if multiple)
    ///
    /// Builds the Python string directly from the borrowed Rust value --
    /// avoids cloning the (potentially large) result string on the Rust side
    /// before PyO3's own unavoidable Rust->Python string copy at the FFI
    /// boundary, matching `to_python()`'s existing zero-extra-copy pattern
    /// (this method's own doc comment above already promises avoiding a
    /// clone; the accessor should keep that promise too).
    fn get_single(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        match &self.inner {
            JsonOutput::Single(result) => Ok(result.into_pyobject(py)?.into_any().unbind()),
            JsonOutput::Multiple(_) => Err(PyValueError::new_err(
                "Result contains multiple JSON strings, use get_multiple() instead",
            )),
        }
    }

    /// Get the multiple results (raises ValueError if single)
    ///
    /// See `get_single`'s doc comment -- same avoided-clone reasoning,
    /// more consequential here since it's a `Vec<String>` (every result
    /// string in the batch) rather than one string.
    fn get_multiple(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        match &self.inner {
            JsonOutput::Single(_) => Err(PyValueError::new_err(
                "Result contains single JSON string, use get_single() instead",
            )),
            JsonOutput::Multiple(results) => Ok(results.into_pyobject(py)?.into_any().unbind()),
        }
    }

    /// Get the result as a Python object (string for single, list for multiple)
    fn to_python(&self, py: Python) -> PyResult<Py<PyAny>> {
        match &self.inner {
            JsonOutput::Single(result) => Ok(result.into_pyobject(py)?.into_any().unbind()),
            JsonOutput::Multiple(results) => Ok(results.into_pyobject(py)?.into_any().unbind()),
        }
    }

    fn __repr__(&self) -> String {
        match &self.inner {
            JsonOutput::Single(result) => format!("JsonOutput.Single('{}')", result),
            JsonOutput::Multiple(results) => format!("JsonOutput.Multiple({:?})", results),
        }
    }

    fn __str__(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        match &self.inner {
            JsonOutput::Single(result) => Ok(result.into_pyobject(py)?.into_any().unbind()),
            JsonOutput::Multiple(results) => Ok(format!("{:?}", results)
                .into_pyobject(py)?
                .into_any()
                .unbind()),
        }
    }
}

#[cfg(feature = "python")]
impl From<JsonOutput> for PyJsonOutput {
    fn from(output: JsonOutput) -> Self {
        PyJsonOutput { inner: output }
    }
}

#[cfg(feature = "python")]
impl PyJsonOutput {
    /// Helper method to create PyJsonOutput from Rust JsonOutput
    pub fn from_rust_output(output: JsonOutput) -> Self {
        PyJsonOutput { inner: output }
    }
}

/// Python JSONTools class - the unified API for JSON manipulation
///
/// This is the single entry point for all JSON operations in Python, providing both
/// flattening and unflattening capabilities with advanced features like collision handling,
/// filtering, and comprehensive transformations. It mirrors the Rust JSONTools API exactly.
///
/// # Performance Optimization
/// Uses Mutex for interior mutability to avoid cloning the entire JSONTools struct
/// on every builder method call. This provides 30-50% performance improvement over
/// the previous clone-based approach while maintaining thread safety for Python's GIL.
///
/// # Input/Output Type Mapping
/// - str input → str output (JSON string)
/// - dict input → dict output (Python dictionary)
/// - list[str] input → list[str] output (list of JSON strings)
/// - list[dict] input → list[dict] output (list of Python dictionaries)
/// - Mixed list preserves original types in output
///
/// # Examples
///
/// ```python
/// import json_tools_rs
///
/// # Basic flattening
/// result = json_tools_rs.JSONTools().flatten().execute('{"a": {"b": 1}}')
/// print(result)  # '{"a.b": 1}' (string)
///
/// # Basic unflattening
/// result = json_tools_rs.JSONTools().unflatten().execute('{"a.b": 1}')
/// print(result)  # '{"a": {"b": 1}}' (string)
///
/// # Advanced configuration with collision handling
/// tools = (json_tools_rs.JSONTools()
///     .flatten()
///     .separator("::")
///     .remove_empty_strings(True)
///     .remove_nulls(True)
///     .lowercase_keys(True)
///     .key_replacement("(User|Admin|Guest)_", "")
///     .handle_key_collision(True))
///
/// result = tools.execute({"User_name": "John", "Admin_name": "", "Guest_name": "Bob"})
/// print(result)  # {"name": ["John", "Bob"]} (dict, empty string filtered out)
///
///
/// # Batch processing with type preservation
/// str_list = ['{"a": 1}', '{"b": 2}']
/// results = json_tools_rs.JSONTools().flatten().execute(str_list)
/// print(results)  # ['{"a": 1}', '{"b": 2}'] (list of strings)
/// ```
#[cfg(feature = "python")]
#[pyclass(name = "JSONTools", module = "json_tools_rs")]
pub struct PyJSONTools {
    // Use Mutex for interior mutability - allows mutation through shared reference
    // This eliminates the need to clone JSONTools on every builder method call
    // Mutex is required for thread safety (PyO3 requires Sync)
    inner: Mutex<JSONTools>,
}

#[cfg(feature = "python")]
impl Default for PyJSONTools {
    fn default() -> Self {
        Self::new()
    }
}

// =============================================================================
// DataFrame and Series Detection Functions
// =============================================================================

/// Detect if the input is a DataFrame or Series
#[cfg(feature = "python")]
fn detect_data_structure(obj: &Bound<'_, PyAny>) -> PyResult<Option<DataStructureType>> {
    // Try DataFrame detection first
    if let Some(df_type) = detect_dataframe_type(obj)? {
        return Ok(Some(DataStructureType::DataFrame(df_type)));
    }

    // Try Series detection
    if let Some(series_type) = detect_series_type(obj)? {
        return Ok(Some(DataStructureType::Series(series_type)));
    }

    // Neither DataFrame nor Series
    Ok(None)
}

/// Detect DataFrame type using duck typing (no imports)
#[cfg(feature = "python")]
fn detect_dataframe_type(obj: &Bound<'_, PyAny>) -> PyResult<Option<DataFrameType>> {
    // Get module and class name for specific detection
    let module = obj
        .getattr("__class__")?
        .getattr("__module__")?
        .extract::<String>()
        .unwrap_or_default();

    let class_name = obj
        .getattr("__class__")?
        .getattr("__name__")?
        .extract::<String>()
        .unwrap_or_default();

    // Check for PyArrow Table (class name is "Table", not "DataFrame")
    if module.starts_with("pyarrow") && class_name == "Table" {
        return Ok(Some(DataFrameType::PyArrow));
    }

    // Check for DataFrame-like methods
    let has_to_dict = obj.hasattr("to_dict")?;
    let has_columns = obj.hasattr("columns")?;

    if !has_to_dict && !has_columns {
        return Ok(None); // Not a DataFrame
    }

    // Check if it's actually a DataFrame class
    if class_name != "DataFrame" {
        return Ok(None);
    }

    // Detect specific library
    if module.starts_with("pandas") {
        Ok(Some(DataFrameType::Pandas))
    } else if module.starts_with("polars") {
        Ok(Some(DataFrameType::Polars))
    } else if module.contains("pyspark.sql") {
        Ok(Some(DataFrameType::PySpark))
    } else if has_to_dict || obj.hasattr("to_json")? {
        // Generic DataFrame-like object
        Ok(Some(DataFrameType::Generic))
    } else {
        Ok(None)
    }
}

/// Detect Series type using duck typing (no imports)
#[cfg(feature = "python")]
fn detect_series_type(obj: &Bound<'_, PyAny>) -> PyResult<Option<SeriesType>> {
    // Get module and class name for specific detection
    let module = obj
        .getattr("__class__")?
        .getattr("__module__")?
        .extract::<String>()
        .unwrap_or_default();

    let class_name = obj
        .getattr("__class__")?
        .getattr("__name__")?
        .extract::<String>()
        .unwrap_or_default();

    // Check for PyArrow Array/ChunkedArray (various class names: Array, ChunkedArray, Int64Array, etc.)
    if module.starts_with("pyarrow")
        && (class_name.contains("Array") || obj.hasattr("to_pylist")?)
    {
        return Ok(Some(SeriesType::PyArrow));
    }

    // Check for Series-like methods
    let has_to_list = obj.hasattr("to_list")? || obj.hasattr("tolist")?;
    let has_dtype = obj.hasattr("dtype")?;

    if !has_to_list && !has_dtype {
        return Ok(None); // Not a Series
    }

    // Check if it's actually a Series class
    if class_name != "Series" {
        return Ok(None);
    }

    // Detect specific library
    if module.starts_with("pandas") {
        Ok(Some(SeriesType::Pandas))
    } else if module.starts_with("polars") {
        Ok(Some(SeriesType::Polars))
    } else if module.contains("pyspark") {
        Ok(Some(SeriesType::PySpark))
    } else if has_to_list {
        // Generic Series-like object
        Ok(Some(SeriesType::Generic))
    } else {
        Ok(None)
    }
}

// =============================================================================
// DataFrame Conversion Functions
// =============================================================================

/// Split newline-delimited JSON (JSONL/NDJSON) text into individual record
/// strings, filtering blank lines. Handles both a trailing newline after the
/// last record and an entirely empty/all-whitespace result for a zero-row
/// DataFrame (pandas gives `"\n"`, polars gives `""` for an empty frame --
/// both correctly yield an empty `Vec` here).
#[cfg(feature = "python")]
fn split_ndjson(text: &str) -> Vec<String> {
    text.lines()
        .filter(|line| !line.trim().is_empty())
        .map(str::to_string)
        .collect()
}

/// Convert a DataFrame to per-row JSON strings.
///
/// Prefers each library's own native JSON export (pandas `to_json`, polars
/// `write_ndjson`) over `to_dict()`/`to_dicts()` + per-row Python<->Rust
/// conversion: benchmarked at ~2-3x faster for realistic row counts, because
/// `to_dict`/`to_dicts` already pay to construct a full Python object graph
/// (one dict per row, each field touched via the DataFrame library's own
/// Python-level iteration) before any conversion to JSON even starts, while
/// the native JSON writers go straight from the DataFrame's internal
/// columnar storage to bytes. PyArrow has no native JSON writer of its own,
/// but bridges through pandas's when pandas is importable (measured ~2x
/// faster than `to_pylist()` + per-item conversion for a realistic table --
/// the same insight already applied to the PySpark arm below, which bridges
/// through pandas for the identical reason) -- see the `PyArrow` arm's own
/// comment for why that bridge must use `types_mapper=pd.ArrowDtype`, not
/// plain `to_pandas()`. Falls back to `to_pylist()` + per-item conversion
/// when pandas isn't installed (still faster than the old `depythonize`-
/// based path -- see `py_dumps`'s doc comment for why).
#[cfg(feature = "python")]
fn dataframe_to_json_strings(
    df: &Bound<'_, PyAny>,
    df_type: DataFrameType,
) -> PyResult<Vec<String>> {
    let py = df.py();

    match df_type {
        DataFrameType::Pandas => {
            let kwargs = pyo3::types::PyDict::new(py);
            kwargs.set_item("orient", "records")?;
            kwargs.set_item("lines", true)?;
            let text: String = df.call_method("to_json", (), Some(&kwargs))?.extract()?;
            Ok(split_ndjson(&text))
        }

        DataFrameType::Polars => {
            let text: String = df.call_method0("write_ndjson")?.extract()?;
            Ok(split_ndjson(&text))
        }

        DataFrameType::PyArrow => {
            if let Ok(pandas) = cached_import(py, &PANDAS_MODULE, "pandas") {
                // `types_mapper=pd.ArrowDtype` is not optional polish here: plain
                // `to_pandas()` (no types_mapper) silently corrupts an integer
                // column that contains any null into float64 (pandas' legacy
                // dtype has no integer null sentinel), e.g. `[1, 2, None, 4]`
                // becoming `[1.0, 2.0, None, 4.0]` -- confirmed by direct
                // comparison against the pre-bridge to_pylist()-based output,
                // not hypothetical. `ArrowDtype` keeps the column
                // Arrow-native (real nullable ints), sidestepping the
                // coercion entirely, and measured no slower (in fact
                // marginally faster) than the plain bridge. Requires pandas
                // >=1.5 (2022) for `pd.ArrowDtype`; older pandas raises
                // AttributeError here and falls through to the plain bridge,
                // then to `to_pylist()` if that fails too.
                if let Ok(arrow_dtype) = pandas.getattr("ArrowDtype") {
                    let kwargs = pyo3::types::PyDict::new(py);
                    kwargs.set_item("types_mapper", arrow_dtype)?;
                    if let Ok(pandas_df) = df.call_method("to_pandas", (), Some(&kwargs)) {
                        return dataframe_to_json_strings(&pandas_df, DataFrameType::Pandas);
                    }
                }
                if let Ok(pandas_df) = df.call_method0("to_pandas") {
                    return dataframe_to_json_strings(&pandas_df, DataFrameType::Pandas);
                }
            }
            let records = df.call_method0("to_pylist")?;
            let list = records.cast::<pyo3::types::PyList>()?;
            pylist_to_json_strings(py, list)
        }

        DataFrameType::PySpark => {
            // No native line-delimited JSON writer reachable without a SparkSession
            // round-trip; convert to pandas first and reuse its native path.
            let pandas_df = df.call_method0("toPandas")?;
            dataframe_to_json_strings(&pandas_df, DataFrameType::Pandas)
        }

        DataFrameType::Generic => {
            // Prefer a pandas-style to_json(orient='records', lines=True) if the
            // object actually accepts that signature; fall back to to_dict() +
            // per-row conversion for anything that doesn't.
            if df.hasattr("to_json")? {
                let kwargs = pyo3::types::PyDict::new(py);
                kwargs.set_item("orient", "records")?;
                kwargs.set_item("lines", true)?;
                if let Ok(result) = df.call_method("to_json", (), Some(&kwargs)) {
                    if let Ok(text) = result.extract::<String>() {
                        return Ok(split_ndjson(&text));
                    }
                }
            }
            if df.hasattr("to_dict")? {
                let kwargs = pyo3::types::PyDict::new(py);
                kwargs.set_item("orient", "records")?;
                let records = df.call_method("to_dict", (), Some(&kwargs))?;
                let list = records.cast::<pyo3::types::PyList>()?;
                pylist_to_json_strings(py, list)
            } else {
                Err(JsonToolsError::new_err(
                    "Generic DataFrame must have to_dict() method",
                ))
            }
        }
    }
}

/// Rows sampled to decide whether a column holds JSON-string values worth
/// auto-expanding -- bounded regardless of DataFrame size, so detection stays
/// cheap. A column that's null (or otherwise never a string) in every sampled
/// row won't be detected -- a safe fallback (stays a plain column, not a
/// crash), not a guarantee of detecting every genuinely-JSON column.
#[cfg(feature = "python")]
const JSON_COLUMN_DETECTION_SAMPLE_SIZE: usize = 20;

/// Detect top-level keys, across a sample of row-JSON strings, that hold a JSON
/// *string* value which itself parses as a JSON object or array -- not any
/// scalar, since a string that happens to parse as a bare number/bool/null
/// isn't a column-expansion candidate. Array is included deliberately: a
/// JSON-string-encoded array should expand into indexed sub-columns the same
/// way an already-list-typed cell does today. A key must parse successfully in
/// *every* sampled row where it appears as a string -- conservative: any
/// failure in the sample disqualifies the whole column from auto-expansion, no
/// partial/mixed result.
#[cfg(feature = "python")]
fn detect_json_string_columns(rows: &[String]) -> Vec<String> {
    let sample_size = rows.len().min(JSON_COLUMN_DETECTION_SAMPLE_SIZE);
    let mut seen: IndexMap<String, usize> = IndexMap::new();
    let mut parsed_ok: IndexMap<String, usize> = IndexMap::new();

    // RawValue-based, same reasoning as `splice_row`: this sample is bounded to
    // (at most) 20 rows regardless of DataFrame size, but a large embedded
    // payload (thousands of keys, github.com/amaye15/JSON-Tools-rs/issues/31)
    // makes even 20 full `Value`-tree parses genuinely slow -- measured ~130ms
    // of a ~650ms total for a 100-row/4,000-key case before this change, nearly
    // a fifth of the whole call for a step that's supposed to be the cheap part.
    for row in &rows[..sample_size] {
        let Ok(fields) =
            serde_json::from_str::<IndexMap<String, &serde_json::value::RawValue>>(row)
        else {
            continue;
        };
        for (key, raw) in &fields {
            let text = raw.get();
            if !text.starts_with('"') {
                continue;
            }
            let Ok(inner) = serde_json::from_str::<String>(text) else {
                continue;
            };
            *seen.entry(key.clone()).or_insert(0) += 1;
            let is_object_or_array = serde_json::from_str::<&serde_json::value::RawValue>(&inner)
                .is_ok()
                && matches!(inner.as_bytes().first(), Some(b'{') | Some(b'['));
            if is_object_or_array {
                *parsed_ok.entry(key.clone()).or_insert(0) += 1;
            }
        }
    }

    seen.into_iter()
        .filter(|(key, count)| parsed_ok.get(key).copied().unwrap_or(0) == *count)
        .map(|(key, _)| key)
        .collect()
}

/// Splice `target_keys`' string values into parsed nested JSON within a single
/// row. Returns `None` if the row doesn't parse as a JSON object at all, or if
/// none of `target_keys` actually needed splicing in this row -- both cases
/// left unchanged by the caller (cheaper than a no-op reserialize). Increments
/// `failure_counts[key]` for any target key present as a string in this row
/// whose value fails to re-parse as an object/array here (the sample that
/// drove detection can still be wrong for a specific later row).
///
/// Deliberately avoids building a full `serde_json::Value` tree for the target
/// field's content (github.com/amaye15/JSON-Tools-rs/issues/31): an earlier
/// version of this function parsed the target string into a full `Value` tree
/// and reserialized the whole row, both O(field count) in the target content --
/// expensive and wasteful for a large embedded payload (e.g. a JSON-string
/// column expanding into thousands of columns), since the core flatten engine
/// parses the same content again moments later regardless. `RawValue` captures
/// each field's exact source byte span without recursing into it, so both the
/// outer row and the target field's validity check stay cheap regardless of
/// how large the target content is; reconstruction copies every OTHER field's
/// bytes verbatim (no reserialization -- also strictly safer than the old
/// approach, e.g. no risk of a `Number` being reformatted through a parse/
/// format round-trip). Benchmarked: ~13x faster on a 200-row/500-key case.
#[cfg(feature = "python")]
fn splice_row(
    row: &str,
    target_keys: &[String],
    failure_counts: &mut IndexMap<String, usize>,
) -> Option<String> {
    let fields = parse_object_fields_indexed(row)?;

    // Pass 1: decide which target keys actually need splicing, without yet
    // committing to a reconstruction -- preserves the fast path for a row
    // where the target column is null/absent (returns None: the caller reuses
    // the original row string byte-for-byte, zero allocation here).
    let mut substitutions: IndexMap<&str, String> = IndexMap::new();
    let mut changed = false;
    for key in target_keys {
        let Some(raw) = fields.get(key.as_str()) else {
            continue;
        };
        let text = raw.get();
        if !text.starts_with('"') {
            continue; // not a string-typed field (null/number/object/array/bool)
        }
        let Ok(inner) = serde_json::from_str::<String>(text) else {
            continue;
        };
        // Validate-then-classify, in that order: a successful RawValue parse is
        // what guarantees the first byte is one of JSON's single-ASCII-byte
        // leading tokens, safe to inspect directly only after validation.
        match serde_json::from_str::<&serde_json::value::RawValue>(&inner) {
            Ok(_) if matches!(inner.as_bytes().first(), Some(b'{') | Some(b'[')) => {
                substitutions.insert(key.as_str(), inner);
                changed = true;
            }
            _ => {
                // Matches the previous implementation exactly: a valid-but-
                // scalar value and a genuinely invalid one both count as a
                // "failure" for this column (neither is splice-worthy).
                *failure_counts.entry(key.clone()).or_insert(0) += 1;
            }
        }
    }
    if !changed {
        return None;
    }

    // Pass 2: reconstruct the row, splicing `substitutions` for detected keys
    // and copying every other field's exact source bytes verbatim. Key
    // escaping reuses `write_json_escaped_key` (flatten.rs) instead of
    // `serde_json::to_string(key)` -- the latter allocates a fresh
    // `Vec::with_capacity(128)` per key (via serde_json's `Serializer`/
    // `Formatter`/`io::Write` machinery) just to produce a quoted string
    // literal, for every field of every row this function touches.
    // `write_json_escaped_key` writes straight into `out` with zero
    // allocation on the common no-escaping-needed path -- the same function
    // already proven in this exact role at flatten.rs:1469/unflatten.rs:1059.
    let mut out = String::with_capacity(row.len() + 64);
    out.push('{');
    for (i, (key, raw)) in fields.iter().enumerate() {
        if i > 0 {
            out.push(',');
        }
        out.push('"');
        write_json_escaped_key(&mut out, key);
        out.push_str("\":");
        match substitutions.get(key.as_ref()) {
            Some(inner) => out.push_str(inner),
            None => out.push_str(raw.get()),
        }
    }
    out.push('}');
    Some(out)
}

/// Apply `detect_json_string_columns`, then splice each detected key's per-row
/// string value into genuine nested JSON across all rows -- so `flatten()`
/// expands it exactly the same way an already-dict/struct-typed column does
/// today, with no Python-level parse or dict-object-graph construction (the
/// overhead github.com/amaye15/JSON-Tools-rs/issues/30 reports paying via a
/// manual `orjson.loads()` workaround). A row that fails to re-parse despite
/// its column being detected keeps its original string value for that row only
/// (best-effort, not a hard error -- this is heuristic auto-detection, not a
/// guarantee); if any row failed for a given column, emits one aggregated
/// Python warning per column naming the failure count, so this stays loud
/// instead of silently producing a column that's structurally different for
/// just that one row. Rows with none of the detected columns present pass
/// through completely unchanged (zero parse/reserialize cost) -- the common
/// case for a DataFrame with no JSON-string columns at all.
#[cfg(feature = "python")]
fn expand_json_string_columns(py: Python<'_>, rows: Vec<String>) -> PyResult<Vec<String>> {
    let target_keys = detect_json_string_columns(&rows);
    if target_keys.is_empty() {
        return Ok(rows);
    }

    let mut failure_counts: IndexMap<String, usize> = IndexMap::new();
    let mut out = Vec::with_capacity(rows.len());
    for row in rows {
        let spliced = splice_row(&row, &target_keys, &mut failure_counts);
        out.push(spliced.unwrap_or(row));
    }

    if !failure_counts.is_empty() {
        let warnings = py.import("warnings")?;
        for (key, count) in &failure_counts {
            warnings.call_method1(
                "warn",
                (format!(
                    "JSON-string column expansion: {count} row(s) in column \"{key}\" looked \
                     like JSON in a sample but failed to parse and were left as their \
                     original string value",
                ),),
            )?;
        }
    }

    Ok(out)
}

/// Column names, in schema order, for a Polars `DataFrame` or PyArrow `Table`/
/// `RecordBatch`. Only called for those two types -- see
/// `detect_and_extract_json_columns_zerocopy`'s doc comment for why they're
/// singled out.
#[cfg(feature = "python")]
fn dataframe_column_names(df: &Bound<'_, PyAny>, df_type: DataFrameType) -> PyResult<Vec<String>> {
    match df_type {
        DataFrameType::Polars => df.getattr("columns")?.extract(),
        DataFrameType::PyArrow => df.getattr("column_names")?.extract(),
        _ => unreachable!("only called for Polars/PyArrow -- see caller"),
    }
}

/// Get a single column as a Python object (a polars `Series` or PyArrow
/// `ChunkedArray`) -- both implement the Arrow PyCapsule interface, so
/// `.extract::<PyChunkedArray>()` on the result converts it zero-copy.
#[cfg(feature = "python")]
fn dataframe_get_column<'py>(
    df: &Bound<'py, PyAny>,
    df_type: DataFrameType,
    name: &str,
) -> PyResult<Bound<'py, PyAny>> {
    match df_type {
        DataFrameType::Polars => df.get_item(name),
        DataFrameType::PyArrow => df.call_method1("column", (name,)),
        _ => unreachable!("only called for Polars/PyArrow -- see caller"),
    }
}

/// Drop the given columns from a Polars `DataFrame` or PyArrow `Table`,
/// returning a new (lighter) object -- used to keep the native-writer call in
/// `dataframe_to_json_strings` cheap by excluding columns already extracted
/// via zero-copy (see `detect_and_extract_json_columns_zerocopy`'s doc
/// comment: escaping a large embedded JSON blob is the dominant cost of that
/// writer call, confirmed empirically -- dropping the column first, not just
/// ignoring its output, is what actually avoids paying for it).
#[cfg(feature = "python")]
fn dataframe_drop_columns<'py>(
    df: &Bound<'py, PyAny>,
    df_type: DataFrameType,
    cols: &[String],
) -> PyResult<Bound<'py, PyAny>> {
    match df_type {
        DataFrameType::Polars => df.call_method1("drop", (cols.to_vec(),)),
        DataFrameType::PyArrow => df.call_method1("drop_columns", (cols.to_vec(),)),
        _ => unreachable!("only called for Polars/PyArrow -- see caller"),
    }
}

/// Extract every value of an Arrow-backed string column via the Arrow
/// PyCapsule interface (zero-copy: no serialization, no Python-level
/// per-cell iteration) -- `None` per cell for a null, `Some(text)` otherwise.
/// Returns `Ok(None)` (not an error) if `col` isn't string-typed -- callers
/// use this to skip non-string columns, which can never hold embedded JSON
/// text (a dict/struct-typed column is already handled directly by the
/// flatten engine; a numeric/bool/nested-list column can't hold JSON text at
/// all).
/// `CompactString` rather than `String` per cell: short JSON-string-column
/// values (short embedded objects, short scalars) stay on the stack instead
/// of heap-allocating, same tradeoff as this crate's other short-string
/// hot paths (`CompactKeyBuilder`/`ValueRef::Owned`). Values long enough to
/// exceed the 24-byte inline cap (larger embedded JSON blobs, the case this
/// whole zero-copy path exists for) still heap-allocate exactly as before --
/// this only removes the allocation for the shorter cells in a column, not
/// all of them.
#[cfg(feature = "python")]
fn extract_arrow_string_values(
    col: &Bound<'_, PyAny>,
) -> PyResult<Option<Vec<Option<CompactString>>>> {
    let Ok(chunked) = col.extract::<PyChunkedArray>() else {
        return Ok(None);
    };
    Ok(extract_arrow_string_values_from_chunked(&chunked))
}

/// Pure-Rust half of [`extract_arrow_string_values`] -- everything after the
/// one `Bound`-touching `.extract::<PyChunkedArray>()` call. Split out so
/// callers that already hold a `PyChunkedArray` (no need to re-fetch/re-
/// extract the column) can call this directly, and so the work can run
/// inside a `py.detach()` block (this function never touches `py`).
#[cfg(feature = "python")]
fn extract_arrow_string_values_from_chunked(
    chunked: &PyChunkedArray,
) -> Option<Vec<Option<CompactString>>> {
    let mut out = Vec::new();
    for chunk in chunked.chunks() {
        if let Some(arr) = chunk.as_any().downcast_ref::<StringArray>() {
            for i in 0..arr.len() {
                out.push(arr.is_valid(i).then(|| CompactString::from(arr.value(i))));
            }
        } else if let Some(arr) = chunk.as_any().downcast_ref::<LargeStringArray>() {
            for i in 0..arr.len() {
                out.push(arr.is_valid(i).then(|| CompactString::from(arr.value(i))));
            }
        } else {
            // Not a string array (int/float/bool/struct/...).
            let arr = chunk.as_any().downcast_ref::<StringViewArray>()?;
            for i in 0..arr.len() {
                out.push(arr.is_valid(i).then(|| CompactString::from(arr.value(i))));
            }
        }
    }
    Some(out)
}

/// Check whether a leaf value's text is itself a JSON object or array --
/// shared detection rule between the text-based detector (`detect_json_
/// string_columns`) and this zero-copy one, so "does this column hold
/// embedded JSON" means the exact same thing regardless of which path found
/// it.
#[cfg(feature = "python")]
fn is_json_object_or_array_text(text: &str) -> bool {
    serde_json::from_str::<&serde_json::value::RawValue>(text).is_ok()
        && matches!(text.as_bytes().first(), Some(b'{') | Some(b'['))
}

/// Arrow-native twin of `detect_json_string_columns` + the column-extraction
/// half of `splice_row`, for Polars `DataFrame`/PyArrow `Table` input
/// specifically. Those two libraries expose their string columns through the
/// Arrow PyCapsule interface, so a column already holding embedded JSON text
/// (github.com/amaye15/JSON-Tools-rs/issues/30) can be read directly via
/// `pyo3-arrow` instead of round-tripping through the DataFrame's own native
/// JSON writer -- which would first *escape* that text into a quoted string
/// value (`dataframe_to_json_strings`), only for `splice_row` to immediately
/// *unescape* it back out. Measured directly (interleaved, isolated probe,
/// 2026-07-30): reading the column zero-copy is ~8.7x (polars)/~28x
/// (pyarrow) faster than that round trip for a realistic embedded payload,
/// and confirmed separately that the escaping step -- not fixed per-row
/// overhead -- is what dominates the native writer's cost (dropping the
/// column before calling it cut that call's own time ~44x).
///
/// Returns `None` for any other `DataFrameType` (pandas isn't Arrow-backed
/// by default; PySpark bridges through pandas already; this optimization
/// doesn't apply there). Returns `Some` with an empty target-column list
/// when the type *is* Polars/PyArrow but sampling found no embedded-JSON
/// columns -- callers should still fall back to the plain
/// `dataframe_to_json_strings` path in that case, since there's nothing to
/// splice.
#[cfg(feature = "python")]
#[allow(clippy::type_complexity)]
fn detect_and_extract_json_columns_zerocopy(
    df: &Bound<'_, PyAny>,
    df_type: DataFrameType,
) -> PyResult<
    Option<(
        Vec<String>,
        IndexMap<String, Vec<Option<CompactString>>>,
        Vec<String>,
    )>,
> {
    if !matches!(df_type, DataFrameType::Polars | DataFrameType::PyArrow) {
        return Ok(None);
    }

    let column_order = dataframe_column_names(df, df_type)?;
    let mut target_cols = Vec::new();
    let mut target_values: IndexMap<String, Vec<Option<CompactString>>> = IndexMap::new();

    for name in &column_order {
        let col = dataframe_get_column(df, df_type, name)?;
        let Some(values) = extract_arrow_string_values(&col)? else {
            continue; // not a string column at all -- can't hold embedded JSON
        };

        let sample_size = values.len().min(JSON_COLUMN_DETECTION_SAMPLE_SIZE);
        let mut sampled_any = false;
        let mut all_sampled_are_json = true;
        for value in values.iter().take(sample_size).flatten() {
            sampled_any = true;
            if !is_json_object_or_array_text(value) {
                all_sampled_are_json = false;
                break;
            }
        }

        if sampled_any && all_sampled_are_json {
            target_cols.push(name.clone());
            target_values.insert(name.clone(), values);
        }
    }

    Ok(Some((target_cols, target_values, column_order)))
}

/// Rebuild each row's JSON object from two sources: `base_rows` (the native-
/// writer output for every column *except* `target_cols`, already valid
/// JSON text per row) and `target_values` (the zero-copy-extracted raw text
/// for `target_cols`, one `Vec` per column, indexed by row). Iterates
/// `column_order` -- the DataFrame's *original* schema order, captured
/// before any columns were dropped -- so the spliced-in columns land back in
/// their original position rather than at the end, matching what the text-
/// based `splice_row` path already guarantees (the "not alphabetized"
/// column-order tests from issue #31 apply here too). A target value that
/// isn't itself valid JSON object/array text (rare -- the column passed
/// sampling but this particular row didn't) falls back to a plain escaped
/// string literal via the same `write_json_escaped_key` used for keys, and
/// counts toward the same aggregated warning `expand_json_string_columns`
/// already emits for this case.
#[cfg(feature = "python")]
fn splice_zerocopy_columns(
    py: Python<'_>,
    base_rows: Vec<String>,
    column_order: &[String],
    target_cols: &[String],
    target_values: &IndexMap<String, Vec<Option<CompactString>>>,
) -> PyResult<Vec<String>> {
    let target_set: IndexSet<&str> = target_cols.iter().map(String::as_str).collect();
    let mut failure_counts: IndexMap<String, usize> = IndexMap::new();
    let mut out = Vec::with_capacity(base_rows.len());

    for (row_idx, base_row) in base_rows.iter().enumerate() {
        let base_fields = parse_object_fields_indexed(base_row).ok_or_else(|| {
            JsonToolsError::new_err(format!("Failed to parse intermediate row {row_idx}"))
        })?;

        let mut row_out = String::with_capacity(base_row.len() + 64);
        row_out.push('{');
        let mut first = true;
        for key in column_order {
            if !first {
                row_out.push(',');
            }
            first = false;
            row_out.push('"');
            write_json_escaped_key(&mut row_out, key);
            row_out.push_str("\":");

            if target_set.contains(key.as_str()) {
                match target_values.get(key).and_then(|col| col.get(row_idx)) {
                    Some(Some(text)) if is_json_object_or_array_text(text) => {
                        row_out.push_str(text);
                    }
                    Some(Some(text)) => {
                        row_out.push('"');
                        write_json_escaped_key(&mut row_out, text);
                        row_out.push('"');
                        *failure_counts.entry(key.clone()).or_insert(0) += 1;
                    }
                    _ => row_out.push_str("null"),
                }
            } else if let Some(raw) = base_fields.get(key.as_str()) {
                row_out.push_str(raw.get());
            } else {
                row_out.push_str("null");
            }
        }
        row_out.push('}');
        out.push(row_out);
    }

    if !failure_counts.is_empty() {
        let warnings = py.import("warnings")?;
        for (key, count) in &failure_counts {
            warnings.call_method1(
                "warn",
                (format!(
                    "JSON-string column expansion: {count} row(s) in column \"{key}\" looked \
                     like JSON in a sample but failed to parse and were left as their \
                     original string value",
                ),),
            )?;
        }
    }

    Ok(out)
}

/// Un-nest every top-level *object*-valued field into top-level siblings,
/// dropping the field's own key -- so a DataFrame column holding a nested
/// object (whether a native dict/struct-typed column, serialized as-is by the
/// DataFrame library's own writer, or a JSON-*string* column already decoded
/// into real JSON by `splice_row`/`splice_zerocopy_columns` above) expands
/// into bare inner-key columns instead of columns prefixed by the source
/// column's own name (github.com/amaye15/JSON-Tools-rs/issues -- "don't keep
/// the original column name" report, 2026-07-31). Every top-level key in a
/// DataFrame row *is* a column name by construction (a DataFrame row has
/// exactly one JSON level per column), so this never risks mistaking a
/// document's own meaningful nesting for a column boundary -- that
/// distinction only exists for genuinely top-level fields, which is exactly
/// what this function -- and only this function -- looks at. Applied once,
/// non-recursively: nesting *within* a column's own content (e.g. a column
/// whose value is `{"a": {"b": 1}}`) still flattens normally from "a"
/// onward -- only the column-name level itself is suppressed.
///
/// Array-valued fields are left nested under their original key (unchanged):
/// an index-based prefix like `col.0` is still meaningful, whereas a bare
/// `0`/`1`/... column name would not be, and risks collision across every
/// array-valued column in the DataFrame.
///
/// Un-nesting two different columns whose contents share a field name (or a
/// field name that collides with an existing top-level column) can produce
/// genuine duplicate keys in the reconstructed row text -- deliberately left
/// unresolved here. This function only ever copies bytes; the core flatten
/// pass immediately following it already has its own, user-configurable
/// collision handling (`handle_key_collision`) for exactly this situation,
/// and reusing it (rather than inventing a second policy here) is the
/// explicit, confirmed choice for this feature.
///
/// Parse a JSON object's top-level fields, preferring zero-copy borrowed
/// keys -- called once per row (and again per unnested column) on every
/// flatten-mode DataFrame row, so an owned `String` per key was a real,
/// measured cost (~1.4us/call end to end, ~24% of a realistic `execute(df)`
/// call -- most of it this exact allocation). DataFrame column names /
/// nested object keys essentially never contain characters needing JSON
/// escaping, so the borrowed-key parse succeeds in the overwhelmingly
/// common case; falls back to owned keys only when a key genuinely needs
/// unescaping -- always correct, never silently treats a row as having
/// nothing to unnest just because one key happened to need escaping.
#[cfg(feature = "python")]
fn parse_object_fields(
    text: &str,
) -> Option<Vec<(std::borrow::Cow<'_, str>, &serde_json::value::RawValue)>> {
    if let Ok(fields) = serde_json::from_str::<IndexMap<&str, &serde_json::value::RawValue>>(text) {
        return Some(
            fields
                .into_iter()
                .map(|(k, v)| (std::borrow::Cow::Borrowed(k), v))
                .collect(),
        );
    }
    let fields: IndexMap<String, &serde_json::value::RawValue> = serde_json::from_str(text).ok()?;
    Some(
        fields
            .into_iter()
            .map(|(k, v)| (std::borrow::Cow::Owned(k), v))
            .collect(),
    )
}

/// Same borrowed-key-preferring parse as [`parse_object_fields`], but into an
/// `IndexMap` instead of a `Vec` -- for callers (like `splice_row`) that need
/// indexed/hashed key lookups, not just iteration, so a `Vec`'s O(n) lookup
/// isn't an acceptable trade for large-column-count rows (e.g. issue #31's
/// 4,042-column case).
#[cfg(feature = "python")]
fn parse_object_fields_indexed(
    text: &str,
) -> Option<IndexMap<std::borrow::Cow<'_, str>, &serde_json::value::RawValue>> {
    if let Ok(fields) = serde_json::from_str::<IndexMap<&str, &serde_json::value::RawValue>>(text) {
        return Some(
            fields
                .into_iter()
                .map(|(k, v)| (std::borrow::Cow::Borrowed(k), v))
                .collect(),
        );
    }
    let fields: IndexMap<String, &serde_json::value::RawValue> = serde_json::from_str(text).ok()?;
    Some(
        fields
            .into_iter()
            .map(|(k, v)| (std::borrow::Cow::Owned(k), v))
            .collect(),
    )
}

/// Returns `None` (row unchanged, zero-copy) when no top-level field is
/// object-valued -- the common case for a DataFrame with no embedded/struct
/// columns at all.
#[cfg(feature = "python")]
fn unnest_object_valued_columns(row: &str) -> Option<String> {
    let fields = parse_object_fields(row)?;

    if !fields
        .iter()
        .any(|(_, raw)| raw.get().as_bytes().first() == Some(&b'{'))
    {
        return None;
    }

    let mut out = String::with_capacity(row.len() + 64);
    out.push('{');
    let mut first = true;
    for (key, raw) in &fields {
        let text = raw.get();
        if text.as_bytes().first() == Some(&b'{') {
            // RawValue already guarantees `text` is well-formed JSON, so a
            // leading `{` guarantees `parse_object_fields` succeeds --
            // structurally impossible to fail here (its own owned-key
            // fallback always succeeds for well-formed JSON).
            if let Some(inner_fields) = parse_object_fields(text) {
                for (inner_key, inner_raw) in &inner_fields {
                    if !first {
                        out.push(',');
                    }
                    first = false;
                    out.push('"');
                    write_json_escaped_key(&mut out, inner_key);
                    out.push_str("\":");
                    out.push_str(inner_raw.get());
                }
            }
        } else {
            if !first {
                out.push(',');
            }
            first = false;
            out.push('"');
            write_json_escaped_key(&mut out, key);
            out.push_str("\":");
            out.push_str(text);
        }
    }
    out.push('}');
    Some(out)
}

/// Convert a Python list of dicts to per-item JSON strings via Python's own
/// `json` module (see `py_dumps`'s doc comment).
#[cfg(feature = "python")]
fn pylist_to_json_strings(
    py: Python<'_>,
    list: &Bound<'_, pyo3::types::PyList>,
) -> PyResult<Vec<String>> {
    let mut strings = Vec::with_capacity(list.len());
    for item in list.iter() {
        let json_str = py_dumps(py, &item)
            .map_err(|e| JsonToolsError::new_err(format!("Failed to convert record: {}", e)))?;
        strings.push(json_str);
    }
    Ok(strings)
}

// =============================================================================
// Series Conversion Functions
// =============================================================================

/// Convert Series to Python list
#[cfg(feature = "python")]
fn series_to_list<'py>(
    series: &Bound<'py, PyAny>,
    series_type: SeriesType,
) -> PyResult<Bound<'py, pyo3::types::PyList>> {
    match series_type {
        SeriesType::Pandas => {
            // Try to_list() first, fallback to tolist()
            if series.hasattr("to_list")? {
                let list = series.call_method0("to_list")?;
                Ok(list.cast::<pyo3::types::PyList>()?.clone())
            } else {
                let list = series.call_method0("tolist")?;
                Ok(list.cast::<pyo3::types::PyList>()?.clone())
            }
        }

        SeriesType::Polars => {
            // Polars uses to_list()
            let list = series.call_method0("to_list")?;
            Ok(list.cast::<pyo3::types::PyList>()?.clone())
        }

        SeriesType::PyArrow => {
            // PyArrow Arrays use to_pylist()
            let list = series.call_method0("to_pylist")?;
            Ok(list.cast::<pyo3::types::PyList>()?.clone())
        }

        SeriesType::PySpark => {
            // PySpark doesn't have Series, but if it exists, convert via pandas
            let pandas_series = series.call_method0("toPandas")?;
            let list = pandas_series.call_method0("tolist")?;
            Ok(list.cast::<pyo3::types::PyList>()?.clone())
        }

        SeriesType::Generic => {
            // Try to_list() first, fallback to tolist()
            if series.hasattr("to_list")? {
                let list = series.call_method0("to_list")?;
                Ok(list.cast::<pyo3::types::PyList>()?.clone())
            } else if series.hasattr("tolist")? {
                let list = series.call_method0("tolist")?;
                Ok(list.cast::<pyo3::types::PyList>()?.clone())
            } else {
                Err(JsonToolsError::new_err(
                    "Generic Series must have to_list() or tolist() method",
                ))
            }
        }
    }
}

/// Helper macro to reduce boilerplate in PyJSONTools builder methods.
/// Each builder method follows the same pattern: lock the mutex, take the inner
/// JSONTools, apply a builder method, store the result back, and return `slf`.
#[cfg(feature = "python")]
macro_rules! py_builder_method {
    ($slf:expr, $tools:ident, $body:expr) => {{
        let mut guard = lock_config(&$slf.inner)?;
        let $tools = mem::take(&mut *guard);
        *guard = $body;
        drop(guard);
        Ok($slf)
    }};
}

#[cfg(feature = "python")]
#[pymethods]
impl PyJSONTools {
    /// Create a new JSONTools instance with default settings.
    ///
    /// Returns a new builder that can be configured with flatten(), unflatten(),
    /// or normal() mode, optional transformations, and then executed.
    ///
    /// Example:
    ///     >>> tools = JSONTools()
    ///     >>> result = tools.flatten().execute({"user": {"name": "John"}})
    #[new]
    #[pyo3(text_signature = "()")]
    pub fn new() -> Self {
        Self {
            inner: Mutex::new(JSONTools::new()),
        }
    }

    /// Set operation mode to flatten nested JSON into dot-separated keys.
    ///
    /// Example:
    ///     >>> result = JSONTools().flatten().execute({"a": {"b": 1}})
    ///     >>> result == {"a.b": 1}
    #[pyo3(text_signature = "($self)")]
    #[inline]
    pub fn flatten(slf: PyRef<'_, Self>) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.flatten())
    }

    /// Set operation mode to unflatten dot-separated keys back into nested JSON.
    ///
    /// Example:
    ///     >>> result = JSONTools().unflatten().execute({"a.b": 1})
    ///     >>> result == {"a": {"b": 1}}
    #[pyo3(text_signature = "($self)")]
    #[inline]
    pub fn unflatten(slf: PyRef<'_, Self>) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.unflatten())
    }

    /// Set operation mode to normal (apply transformations without flatten/unflatten).
    ///
    /// In normal mode, key/value replacements, filtering, and type conversion
    /// are applied recursively without changing the nesting structure.
    #[pyo3(text_signature = "($self)")]
    #[inline]
    pub fn normal(slf: PyRef<'_, Self>) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.normal())
    }

    /// Set the separator for nested keys (default: ".").
    ///
    /// Args:
    ///     separator: Non-empty string to use between nested key segments.
    ///
    /// Raises:
    ///     ValueError: If separator is empty.
    #[pyo3(text_signature = "($self, separator)")]
    #[inline]
    pub fn separator(slf: PyRef<'_, Self>, separator: String) -> PyResult<PyRef<'_, Self>> {
        if separator.is_empty() {
            return Err(PyValueError::new_err("Separator cannot be empty"));
        }
        py_builder_method!(slf, tools, tools.separator(separator))
    }

    /// Enable or disable lowercase key conversion.
    ///
    /// Args:
    ///     value: True to convert all keys to lowercase.
    #[pyo3(text_signature = "($self, value)")]
    #[inline]
    pub fn lowercase_keys(slf: PyRef<'_, Self>, value: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.lowercase_keys(value))
    }

    /// Enable or disable removal of keys with empty string values.
    ///
    /// Args:
    ///     value: True to remove keys whose values are empty strings ("").
    #[pyo3(text_signature = "($self, value)")]
    #[inline]
    pub fn remove_empty_strings(slf: PyRef<'_, Self>, value: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.remove_empty_strings(value))
    }

    /// Enable or disable removal of keys with null values.
    ///
    /// Args:
    ///     value: True to remove keys whose values are null/None.
    #[pyo3(text_signature = "($self, value)")]
    #[inline]
    pub fn remove_nulls(slf: PyRef<'_, Self>, value: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.remove_nulls(value))
    }

    /// Enable or disable removal of keys with empty object values ({}).
    ///
    /// Args:
    ///     value: True to remove keys whose values are empty objects.
    #[pyo3(text_signature = "($self, value)")]
    #[inline]
    pub fn remove_empty_objects(slf: PyRef<'_, Self>, value: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.remove_empty_objects(value))
    }

    /// Enable or disable removal of keys with empty array values ([]).
    ///
    /// Args:
    ///     value: True to remove keys whose values are empty arrays.
    #[pyo3(text_signature = "($self, value)")]
    #[inline]
    pub fn remove_empty_arrays(slf: PyRef<'_, Self>, value: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.remove_empty_arrays(value))
    }

    /// Add a key replacement pattern (regex or literal fallback).
    ///
    /// Args:
    ///     find: Regex pattern to match against keys. Falls back to literal
    ///         string replacement if regex compilation fails.
    ///     replace: Replacement string.
    #[pyo3(text_signature = "($self, find, replace)")]
    #[inline]
    pub fn key_replacement(
        slf: PyRef<'_, Self>,
        find: String,
        replace: String,
    ) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.key_replacement(find, replace))
    }

    /// Add a value replacement pattern (regex or literal fallback).
    ///
    /// Args:
    ///     find: Regex pattern to match against values. Falls back to literal
    ///         string replacement if regex compilation fails.
    ///     replace: Replacement string.
    #[pyo3(text_signature = "($self, find, replace)")]
    #[inline]
    pub fn value_replacement(
        slf: PyRef<'_, Self>,
        find: String,
        replace: String,
    ) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.value_replacement(find, replace))
    }

    /// Exclude any key (and its entire value/subtree) whose name contains `pattern`.
    ///
    /// Literal substring match by default; wrap in `r'...'` for regex, matching
    /// key_replacement's convention. Additive -- call once per keyword to exclude
    /// multiple. Matching a container key drops its entire subtree.
    ///
    /// Args:
    ///     pattern: Substring (or r'...'-wrapped regex) to match against key names.
    #[pyo3(text_signature = "($self, pattern)")]
    #[inline]
    pub fn exclude_key(slf: PyRef<'_, Self>, pattern: String) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.exclude_key(pattern))
    }

    /// Drop a key-value pair whose value contains `pattern`.
    ///
    /// Literal substring match by default; wrap in `r'...'` for regex, matching
    /// exclude_key's convention. Additive -- call once per pattern to exclude
    /// multiple. Only applies to scalar leaf values (strings/numbers/booleans/null).
    ///
    /// Args:
    ///     pattern: Substring (or r'...'-wrapped regex) to match against values.
    #[pyo3(text_signature = "($self, pattern)")]
    #[inline]
    pub fn exclude_value(slf: PyRef<'_, Self>, pattern: String) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.exclude_value(pattern))
    }

    /// Enable collision handling by collecting duplicate keys into arrays.
    ///
    /// When key transformations produce duplicate keys, values are collected
    /// into arrays (e.g., "name": ["John", "Jane"]).
    ///
    /// Args:
    ///     value: True to enable collision handling.
    #[pyo3(text_signature = "($self, value)")]
    #[inline]
    pub fn handle_key_collision(slf: PyRef<'_, Self>, value: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.handle_key_collision(value))
    }

    /// Flattened key names that must always render as a JSON array, even
    /// when only one value is present in a given document.
    ///
    /// Without this, a key's scalar-vs-array shape depends on whether a
    /// collision actually happened *in that specific document*: a key that
    /// collides in some rows of a batch/DataFrame (e.g. because of
    /// key_replacement()) but not others ends up a str in some results and
    /// a list in others -- an inconsistent shape that's awkward for any
    /// downstream consumer expecting a stable schema, including building a
    /// DataFrame column from the results, or normalise()'s own column
    /// typing (a column that's consistently List<T> needs every row's
    /// value to already be array-shaped -- this is exactly how to get
    /// that). Naming a key here guarantees every document that has that
    /// key emits it as an array, regardless of handle_key_collision().
    ///
    /// Matched against the *final* flattened key name (after
    /// separator-joining and any key transforms) -- the same name
    /// handle_key_collision() resolves collisions on. Works for all
    /// operations (flatten, unflatten, normal) and for normalise()/
    /// DataFrame input, since those are built on top of flatten().
    ///
    /// Args:
    ///     keys: Iterable of flattened key names that must always be arrays.
    #[pyo3(text_signature = "($self, keys)")]
    #[inline]
    pub fn always_array_keys(slf: PyRef<'_, Self>, keys: Vec<String>) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.always_array_keys(keys))
    }

    /// Enable automatic type conversion from strings to numbers and booleans
    ///
    /// When enabled, the library will attempt to convert string values:
    /// - Numbers: "123" → 123, "1,234.56" → 1234.56, "$99.99" → 99.99
    /// - Booleans: "true"/"TRUE"/"True" → true, "false"/"FALSE"/"False" → false
    ///
    /// If conversion fails, the original string value is kept.
    ///
    /// # Arguments
    /// * `enable` - Whether to enable automatic type conversion
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// result = jt.JSONTools().flatten().auto_convert_types(True).execute({"id": "123", "active": "true"})
    /// print(result)  # {'id': 123, 'active': True}
    /// ```
    ///
    #[pyo3(text_signature = "($self, enable)")]
    #[inline]
    pub fn auto_convert_types(slf: PyRef<'_, Self>, enable: bool) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.auto_convert_types(enable))
    }

    /// Enable or disable date/datetime string conversion independently of the other
    /// type-conversion categories (nulls, booleans, numbers).
    ///
    /// # Arguments
    /// * `enable` - Whether to enable date/datetime conversion
    /// * `normalize_to_utc` - If set, configure whether recognized dates/datetimes
    ///   are normalized to UTC (default: True). When False, a recognized date is
    ///   left unchanged but is still protected from being misread as a number.
    /// * `assume_utc_for_naive` - If set, configure whether timezone-less datetimes
    ///   (e.g. "2024-01-15T10:30:00") are assumed to be UTC and get a `Z` appended
    ///   (default: True). When False, naive datetimes are left unchanged.
    ///
    /// A second call without `normalize_to_utc`/`assume_utc_for_naive` preserves
    /// whatever those were set to by a previous call -- only `enable` is always
    /// applied.
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// tools = jt.JSONTools().flatten().convert_dates(True, assume_utc_for_naive=False)
    /// ```
    #[pyo3(signature = (enable, normalize_to_utc=None, assume_utc_for_naive=None))]
    #[pyo3(text_signature = "($self, enable, normalize_to_utc=None, assume_utc_for_naive=None)")]
    pub fn convert_dates(
        slf: PyRef<'_, Self>,
        enable: bool,
        normalize_to_utc: Option<bool>,
        assume_utc_for_naive: Option<bool>,
    ) -> PyResult<PyRef<'_, Self>> {
        let mut guard = lock_config(&slf.inner)?;
        let tools = mem::take(&mut *guard);
        let mut cfg = tools.date_conversion().clone();
        cfg.enabled = enable;
        if let Some(v) = normalize_to_utc {
            cfg.normalize_to_utc = v;
        }
        if let Some(v) = assume_utc_for_naive {
            cfg.assume_utc_for_naive = v;
        }
        *guard = tools.convert_dates_config(cfg);
        drop(guard);
        Ok(slf)
    }

    /// Enable or disable null-string conversion independently of the other
    /// type-conversion categories (dates, booleans, numbers).
    ///
    /// # Arguments
    /// * `enable` - Whether to enable null-string conversion
    /// * `extra_tokens` - If set, a list of additional strings to recognize as null,
    ///   beyond the built-in list ("null", "NULL", "nil", "none", "N/A", "NA", etc.).
    ///   Additive only -- replaces any previously-set extra token list, but never
    ///   narrows the built-in list. Matched exactly (case-sensitive).
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// tools = jt.JSONTools().flatten().convert_nulls(True, extra_tokens=["missing"])
    /// ```
    #[pyo3(signature = (enable, extra_tokens=None))]
    #[pyo3(text_signature = "($self, enable, extra_tokens=None)")]
    pub fn convert_nulls(
        slf: PyRef<'_, Self>,
        enable: bool,
        extra_tokens: Option<Vec<String>>,
    ) -> PyResult<PyRef<'_, Self>> {
        let mut guard = lock_config(&slf.inner)?;
        let tools = mem::take(&mut *guard);
        let mut cfg = tools.null_conversion().clone();
        cfg.enabled = enable;
        if let Some(tokens) = extra_tokens {
            cfg.extra_tokens = tokens.into();
        }
        *guard = tools.convert_nulls_config(cfg);
        drop(guard);
        Ok(slf)
    }

    /// Enable or disable boolean-string conversion independently of the other
    /// type-conversion categories (dates, nulls, numbers).
    ///
    /// # Arguments
    /// * `enable` - Whether to enable boolean-string conversion
    /// * `extra_true_tokens` - If set, additional strings recognized as `true`,
    ///   beyond the built-in list ("true", "yes", "on", "y", etc.). Replaces any
    ///   previously-set list.
    /// * `extra_false_tokens` - If set, additional strings recognized as `false`,
    ///   beyond the built-in list ("false", "no", "off", "n", etc.). Replaces any
    ///   previously-set list.
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// tools = jt.JSONTools().flatten().convert_booleans(
    ///     True, extra_true_tokens=["si"], extra_false_tokens=["nope"]
    /// )
    /// ```
    #[pyo3(signature = (enable, extra_true_tokens=None, extra_false_tokens=None))]
    #[pyo3(text_signature = "($self, enable, extra_true_tokens=None, extra_false_tokens=None)")]
    pub fn convert_booleans(
        slf: PyRef<'_, Self>,
        enable: bool,
        extra_true_tokens: Option<Vec<String>>,
        extra_false_tokens: Option<Vec<String>>,
    ) -> PyResult<PyRef<'_, Self>> {
        let mut guard = lock_config(&slf.inner)?;
        let tools = mem::take(&mut *guard);
        let mut cfg = tools.boolean_conversion().clone();
        cfg.enabled = enable;
        if let Some(tokens) = extra_true_tokens {
            cfg.extra_true_tokens = tokens.into();
        }
        if let Some(tokens) = extra_false_tokens {
            cfg.extra_false_tokens = tokens.into();
        }
        *guard = tools.convert_booleans_config(cfg);
        drop(guard);
        Ok(slf)
    }

    /// Enable or disable numeric-string conversion independently of the other
    /// type-conversion categories (dates, nulls, booleans).
    ///
    /// Plain integers/decimals, scientific notation, and thousands-separator
    /// cleanup are always applied when `enable` is True; the remaining sub-formats
    /// can each be disabled independently.
    ///
    /// # Arguments
    /// * `enable` - Whether to enable numeric-string conversion
    /// * `currency` - If set, configure currency symbol/code/credit-debit-suffix
    ///   stripping (default: True)
    /// * `percent` - If set, configure `%`/permille/per-ten-thousand suffix parsing
    ///   (default: True)
    /// * `basis_points` - If set, configure text basis-point suffix parsing, e.g.
    ///   "25bps" (default: True)
    /// * `suffixes` - If set, configure K/M/B/T magnitude suffix parsing (default: True)
    /// * `fractions` - If set, configure fraction parsing, e.g. "1/2" (default: True)
    /// * `radix` - If set, configure hex/binary/octal literal parsing (default: True)
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// tools = jt.JSONTools().flatten().convert_numbers(True, currency=False)
    /// ```
    #[pyo3(signature = (
        enable,
        currency=None,
        percent=None,
        basis_points=None,
        suffixes=None,
        fractions=None,
        radix=None
    ))]
    #[pyo3(
        text_signature = "($self, enable, currency=None, percent=None, basis_points=None, suffixes=None, fractions=None, radix=None)"
    )]
    #[allow(clippy::too_many_arguments)]
    pub fn convert_numbers(
        slf: PyRef<'_, Self>,
        enable: bool,
        currency: Option<bool>,
        percent: Option<bool>,
        basis_points: Option<bool>,
        suffixes: Option<bool>,
        fractions: Option<bool>,
        radix: Option<bool>,
    ) -> PyResult<PyRef<'_, Self>> {
        let mut guard = lock_config(&slf.inner)?;
        let tools = mem::take(&mut *guard);
        let mut cfg = tools.number_conversion().clone();
        cfg.enabled = enable;
        if let Some(v) = currency {
            cfg.currency = v;
        }
        if let Some(v) = percent {
            cfg.percent = v;
        }
        if let Some(v) = basis_points {
            cfg.basis_points = v;
        }
        if let Some(v) = suffixes {
            cfg.suffixes = v;
        }
        if let Some(v) = fractions {
            cfg.fractions = v;
        }
        if let Some(v) = radix {
            cfg.radix = v;
        }
        *guard = tools.convert_numbers_config(cfg);
        drop(guard);
        Ok(slf)
    }

    /// Set the minimum batch size for parallel processing
    ///
    /// When processing multiple JSON documents, this threshold determines when to use
    /// parallel processing. Batches smaller than this threshold will be processed sequentially
    /// to avoid the overhead of thread spawning.
    ///
    /// Default: 10 items (can be overridden with JSON_TOOLS_PARALLEL_THRESHOLD environment variable)
    ///
    /// # Arguments
    /// * `threshold` - Minimum number of items in a batch to trigger parallel processing
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// # Only use parallelism for batches of 50+ items
    /// tools = jt.JSONTools().flatten().parallel_threshold(50)
    /// results = tools.execute([...])  # Large batch will use parallel processing
    /// ```
    ///
    #[pyo3(text_signature = "($self, threshold)")]
    #[inline]
    pub fn parallel_threshold(slf: PyRef<'_, Self>, threshold: usize) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.parallel_threshold(threshold))
    }

    /// Configure the number of threads for parallel processing
    ///
    /// By default, the number of logical CPUs is used. This method allows you to override
    /// that behavior for specific workloads or resource constraints.
    ///
    /// # Arguments
    /// * `num_threads` - Number of threads to use (None = use system default)
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// # Limit to 4 threads for resource-constrained environments
    /// tools = jt.JSONTools().flatten().num_threads(4)
    /// # Or use None to auto-detect (default)
    /// tools = jt.JSONTools().flatten().num_threads(None)
    /// ```
    ///
    #[pyo3(text_signature = "($self, num_threads)")]
    #[inline]
    pub fn num_threads(
        slf: PyRef<'_, Self>,
        num_threads: Option<usize>,
    ) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.num_threads(num_threads))
    }

    /// Configure the threshold for nested parallel processing within individual JSON documents
    ///
    /// When flattening or unflattening a single large JSON document, this threshold determines
    /// when to parallelize the processing of objects and arrays. Only objects/arrays with more
    /// than this many keys/items will be processed in parallel.
    ///
    /// Default: 100 (can be overridden with JSON_TOOLS_NESTED_PARALLEL_THRESHOLD environment variable)
    ///
    /// # Arguments
    /// * `threshold` - Minimum number of keys/items to trigger nested parallelism
    ///
    /// # Returns
    /// Self for method chaining
    ///
    /// # Example
    /// ```python
    /// import json_tools_rs as jt
    /// # Only parallelize objects/arrays with 200+ items
    /// tools = jt.JSONTools().flatten().nested_parallel_threshold(200)
    /// result = tools.execute(large_json)  # Large nested structures will use parallel processing
    /// ```
    ///
    #[pyo3(text_signature = "($self, threshold)")]
    #[inline]
    pub fn nested_parallel_threshold(
        slf: PyRef<'_, Self>,
        threshold: usize,
    ) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.nested_parallel_threshold(threshold))
    }

    /// Set the maximum array index allowed during unflattening (DoS protection)
    ///
    /// Prevents malicious flattened keys like "items.999999999" from causing
    /// excessive memory allocation. Keys with array indices exceeding this
    /// limit will produce an error during unflattening.
    ///
    /// Default: 100,000
    #[pyo3(text_signature = "($self, max)")]
    #[inline]
    pub fn max_array_index(slf: PyRef<'_, Self>, max: usize) -> PyResult<PyRef<'_, Self>> {
        py_builder_method!(slf, tools, tools.max_array_index(max))
    }

    /// Execute the configured JSON operation
    ///
    /// This method executes the configured operation (flatten or unflatten) with all
    /// the specified transformations, collision handling, and filtering options.
    ///
    /// # Arguments
    /// * `json_input` - JSON input as:
    ///   - str: JSON string
    ///   - dict: Python dictionary (will be serialized to JSON)
    ///   - list[str]: List of JSON strings
    ///   - list[dict]: List of Python dictionaries (will be serialized to JSON)
    ///
    /// # Returns
    /// * str input → str output (processed JSON string)
    /// * dict input → dict output (processed Python dictionary)
    /// * list[str] input → list[str] output (list of processed JSON strings)
    /// * list[dict] input → list[dict] output (list of processed Python dictionaries)
    /// * When `normalise=True`: always a wide DataFrame (one column per flattened
    ///   key), regardless of input shape -- see `execute_normalise` for details.
    ///
    /// # Performance
    /// Uses interior mutability to avoid cloning JSONTools - only clones for execute() call
    #[pyo3(signature = (json_input, normalise=false, target=None))]
    #[pyo3(text_signature = "($self, json_input, normalise=False, target=None)")]
    pub fn execute(
        &self,
        json_input: &Bound<'_, PyAny>,
        normalise: bool,
        target: Option<String>,
    ) -> PyResult<Py<PyAny>> {
        let py = json_input.py();

        if normalise {
            return self.execute_normalise(json_input, target);
        }
        if target.is_some() {
            return Err(JsonToolsError::new_err(
                "target is only valid when normalise=True",
            ));
        }

        // An exactly-typed str/dict/list can never be a DataFrame/Series, so
        // skip the duck-typing detection (several getattr/hasattr chains) for
        // the common input shapes -- it's pure per-call overhead there.
        // Subclasses and everything else still take the full detection path.
        let is_exact_common_type = json_input.is_exact_instance_of::<PyString>()
            || json_input.is_exact_instance_of::<PyDict>()
            || json_input.is_exact_instance_of::<PyList>();

        // Check for DataFrame or Series first (before other type checks)
        if !is_exact_common_type {
            match detect_data_structure(json_input)? {
                Some(DataStructureType::DataFrame(df_type)) => {
                    return self.execute_dataframe(json_input, df_type);
                }
                Some(DataStructureType::Series(series_type)) => {
                    return self.execute_series(json_input, series_type);
                }
                None => {
                    // Fall through to existing type checks
                }
            }
        }

        // Fast path: single JSON string → return JSON string
        if let Ok(json_str) = json_input.extract::<String>() {
            // TIER 6→3 OPTIMIZATION: Take ownership instead of cloning
            // Saves 1K-10K cycles by avoiding deep clone of entire JSONTools config
            let result = py
                .detach(|| {
                    let mut guard = lock_config(&self.inner)?;
                    let tools = mem::take(&mut *guard);
                    let result = tools.execute(json_str.as_str());
                    *guard = tools;
                    result
                })
                .map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to process JSON string: {}", e))
                })?;

            match result {
                JsonOutput::Single(processed) => {
                    Ok(processed.into_pyobject(py)?.into_any().unbind())
                }
                JsonOutput::Multiple(_) => Err(PyValueError::new_err(
                    "Unexpected multiple results for single JSON input",
                )),
            }
        } else if json_input.is_instance_of::<pyo3::types::PyDict>() {
            // Serialize via Python's own `json` module -- see `py_dumps`'s doc comment
            // for why this beats the generic serde-based `depythonize` for the nested
            // data this library's flatten/unflatten exist to handle.
            let json_str = py_dumps(py, json_input).map_err(|e| {
                JsonToolsError::new_err(format!("Failed to convert Python dict: {}", e))
            })?;

            // Process with Rust tools (release GIL)
            let result = py
                .detach(|| {
                    let mut guard = lock_config(&self.inner)?;
                    let tools = mem::take(&mut *guard);
                    let result = tools.execute(json_str.as_str());
                    *guard = tools;
                    result
                })
                .map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to process Python dict: {}", e))
                })?;

            match result {
                JsonOutput::Single(processed) => {
                    let python_dict = py_loads(py, &processed).map_err(|e| {
                        JsonToolsError::new_err(format!("Failed to convert to Python: {}", e))
                    })?;
                    Ok(python_dict.unbind())
                }
                JsonOutput::Multiple(_) => Err(PyValueError::new_err(
                    "Unexpected multiple results for single dict input",
                )),
            }
        } else if json_input.is_instance_of::<pyo3::types::PyList>() {
            // Handle list input - batch processing of JSON strings and/or dicts
            let list = json_input.cast::<pyo3::types::PyList>()?;

            if list.is_empty() {
                return Ok(Vec::<String>::new().into_pyobject(py)?.into_any().unbind());
            }

            let mut json_strings: Vec<String> = Vec::with_capacity(list.len());
            let mut is_str_flags: Vec<bool> = Vec::with_capacity(list.len());
            let mut has_other_types = false;

            for item in list.iter() {
                if let Ok(json_str) = item.extract::<String>() {
                    json_strings.push(json_str);
                    is_str_flags.push(true);
                } else if item.is_instance_of::<pyo3::types::PyDict>() {
                    let json_str = py_dumps(py, &item).map_err(|e| {
                        JsonToolsError::new_err(format!("Failed to convert dict in list: {}", e))
                    })?;
                    json_strings.push(json_str);
                    is_str_flags.push(false);
                } else {
                    has_other_types = true;
                    break;
                }
            }

            if has_other_types {
                return Err(PyValueError::new_err(
                    "List items must be either JSON strings or Python dictionaries",
                ));
            }

            // TIER 6→3 OPTIMIZATION: Take ownership instead of cloning
            let result = py
                .detach(|| {
                    let mut guard = lock_config(&self.inner)?;
                    let tools = mem::take(&mut *guard);
                    let result = tools.execute(json_strings);
                    *guard = tools;
                    result
                })
                .map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to process JSON list: {}", e))
                })?;

            match result {
                JsonOutput::Single(_) => Err(PyValueError::new_err(
                    "Unexpected single result for multiple input",
                )),
                JsonOutput::Multiple(processed_list) => {
                    // Determine output shape and transform accordingly
                    let all_strings = is_str_flags.iter().all(|&b| b);
                    let all_dicts = is_str_flags.iter().all(|&b| !b);

                    if all_strings {
                        Ok(processed_list.into_pyobject(py)?.into_any().unbind())
                    } else if all_dicts {
                        let mut dict_results: Vec<Py<PyAny>> =
                            Vec::with_capacity(processed_list.len());
                        for processed_json in processed_list {
                            let python_dict = py_loads(py, &processed_json).map_err(|e| {
                                JsonToolsError::new_err(format!(
                                    "Failed to convert to Python dict: {}",
                                    e
                                ))
                            })?;
                            dict_results.push(python_dict.unbind());
                        }
                        Ok(dict_results.into_pyobject(py)?.into_any().unbind())
                    } else {
                        let mut mixed_results: Vec<Py<PyAny>> =
                            Vec::with_capacity(processed_list.len());
                        for (processed_json, is_str) in processed_list.into_iter().zip(is_str_flags)
                        {
                            if is_str {
                                mixed_results
                                    .push(processed_json.into_pyobject(py)?.into_any().unbind());
                            } else {
                                let python_dict = py_loads(py, &processed_json).map_err(|e| {
                                    JsonToolsError::new_err(format!(
                                        "Failed to convert to Python dict: {}",
                                        e
                                    ))
                                })?;
                                mixed_results.push(python_dict.unbind());
                            }
                        }
                        Ok(mixed_results.into_pyobject(py)?.into_any().unbind())
                    }
                }
            }
        } else {
            Err(PyValueError::new_err(
                "json_input must be a JSON string, Python dict, list of JSON strings, or list of Python dicts",
            ))
        }
    }

    /// Execute the configured operation and return a JsonOutput object
    ///
    /// This method returns the full JsonOutput object for advanced use cases
    /// where you need to check the result type or handle both single and multiple
    /// results in a unified way.
    ///
    /// # Arguments
    /// * `json_input` - JSON input as:
    ///   - str: JSON string
    ///   - dict: Python dictionary (will be serialized to JSON)
    ///   - list[str]: List of JSON strings
    ///   - list[dict]: List of Python dictionaries (will be serialized to JSON)
    ///
    /// # Returns
    /// * `PyJsonOutput` - JsonOutput object with is_single/is_multiple methods
    ///
    /// # Performance
    /// Uses interior mutability to avoid cloning JSONTools - only clones for execute() call
    #[pyo3(text_signature = "($self, json_input)")]
    pub fn execute_to_output(&self, json_input: &Bound<'_, PyAny>) -> PyResult<PyJsonOutput> {
        let py = json_input.py();

        // Note: DataFrames/Series are not supported in execute_to_output()
        // Use execute() instead for DataFrame/Series support

        // Single JSON string
        if let Ok(json_str) = json_input.extract::<String>() {
            // TIER 6→3: Take ownership instead of cloning (10K-50K cycles saved)
            let result = py
                .detach(|| {
                    let mut guard = lock_config(&self.inner)?;
                    let tools = mem::take(&mut *guard);
                    let result = tools.execute(json_str.as_str());
                    *guard = tools;
                    result
                })
                .map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to process JSON string: {}", e))
                })?;
            return Ok(PyJsonOutput::from_rust_output(result));
        }

        // Single Python dictionary - serialize via Python's own `json` module (see
        // `py_dumps`'s doc comment)
        if json_input.is_instance_of::<pyo3::types::PyDict>() {
            let json_str = py_dumps(py, json_input).map_err(|e| {
                JsonToolsError::new_err(format!("Failed to convert Python dict: {}", e))
            })?;

            let result = py
                .detach(|| {
                    let mut guard = lock_config(&self.inner)?;
                    let tools = mem::take(&mut *guard);
                    let result = tools.execute(json_str.as_str());
                    *guard = tools;
                    result
                })
                .map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to process Python dict: {}", e))
                })?;
            return Ok(PyJsonOutput::from_rust_output(result));
        }

        // List input - batch processing or single JSON array
        if json_input.is_instance_of::<pyo3::types::PyList>() {
            let list = json_input.cast::<pyo3::types::PyList>()?;

            if list.is_empty() {
                return Ok(PyJsonOutput::from_rust_output(JsonOutput::Multiple(vec![])));
            }

            let mut json_strings: Vec<String> = Vec::with_capacity(list.len());

            for item in list.iter() {
                if let Ok(json_str) = item.extract::<String>() {
                    json_strings.push(json_str);
                } else if item.is_instance_of::<pyo3::types::PyDict>() {
                    let json_str = py_dumps(py, &item).map_err(|e| {
                        JsonToolsError::new_err(format!("Failed to convert dict in list: {}", e))
                    })?;
                    json_strings.push(json_str);
                } else {
                    return Err(PyValueError::new_err(
                        "List items must be either JSON strings or Python dictionaries",
                    ));
                }
            }

            // Process the list of JSON strings directly
            // TIER 6→3: Take ownership instead of cloning (10K-50K cycles saved)
            let result = py
                .detach(|| {
                    let mut guard = lock_config(&self.inner)?;
                    let tools = mem::take(&mut *guard);
                    let result = tools.execute(json_strings);
                    *guard = tools;
                    result
                })
                .map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to process JSON list: {}", e))
                })?;
            return Ok(PyJsonOutput::from_rust_output(result));
        }

        Err(PyValueError::new_err(
            "json_input must be a JSON string, Python dict, DataFrame, Series, list of JSON strings, or list of Python dicts",
        ))
    }

    /// Serialize this instance's configuration to a JSON string, from which an
    /// equivalent, independent instance can be rebuilt via
    /// `JSONTools.from_config_json(...)`.
    ///
    /// This is the mechanism behind pickle support (`__reduce__`, below) --
    /// useful directly too for shipping a configured `JSONTools` across any
    /// other process boundary that can't pickle a native extension object,
    /// e.g. a PySpark `mapInPandas` partition function, which should close
    /// over this string (not `self`) and call `from_config_json` fresh inside
    /// each partition.
    #[pyo3(text_signature = "($self)")]
    pub fn to_config_json(&self) -> PyResult<String> {
        let guard = lock_config(&self.inner)?;
        Ok(guard.to_config_json())
    }

    /// Reconstruct a `JSONTools` instance from a JSON string previously
    /// produced by `to_config_json()`. See that method's doc for why this
    /// pair exists.
    #[staticmethod]
    #[pyo3(text_signature = "(config_json)")]
    pub fn from_config_json(config_json: &str) -> PyResult<Self> {
        let tools = crate::config_json::build_tools(config_json)
            .map_err(|e| JsonToolsError::new_err(format!("Invalid configuration: {e}")))?;
        Ok(Self {
            inner: Mutex::new(tools),
        })
    }

    /// Pickle support (`pickle.dumps`/`pickle.loads`, and by extension
    /// cloudpickle-based closure capture, e.g. inside a PySpark UDF or
    /// `mapInPandas` function) -- see github.com/amaye15/JSON-Tools-rs/issues/29.
    ///
    /// A `PyJSONTools` wraps a native Rust object with no Python `__dict__`,
    /// so the standard `__reduce__` protocol is used instead of `__getstate__`/
    /// `__setstate__`: returns `(from_config_json, (config_json_string,))`.
    /// Unpickling calls `JSONTools.from_config_json(config_json_string)`,
    /// which reconstructs an independent, equivalently-configured instance --
    /// `from_config_json` is a `#[staticmethod]` on a module-registered class,
    /// so pickle can serialize the callable itself by reference
    /// (`json_tools_rs.JSONTools.from_config_json`), the same way it already
    /// handles any other class/static method reference.
    pub fn __reduce__<'py>(slf: &Bound<'py, Self>) -> PyResult<(Bound<'py, PyAny>, (String,))> {
        let config_json = slf.borrow().to_config_json()?;
        let ctor = slf.get_type().getattr("from_config_json")?;
        Ok((ctor, (config_json,)))
    }
}

// =============================================================================
// DataFrame Reconstruction Functions
// =============================================================================

/// Reconstruct DataFrame from list of dicts (with fallback to list)
#[cfg(feature = "python")]
fn reconstruct_dataframe(
    py: Python,
    df_type: DataFrameType,
    processed_dicts: Vec<Py<PyAny>>,
) -> PyResult<Py<PyAny>> {
    match df_type {
        DataFrameType::Pandas => reconstruct_pandas_df(py, processed_dicts),
        DataFrameType::Polars => reconstruct_polars_df(py, processed_dicts),
        DataFrameType::PyArrow => reconstruct_pyarrow_table(py, processed_dicts),
        DataFrameType::PySpark => {
            // PySpark reconstruction would need SparkSession - fallback to list for now
            Ok(processed_dicts.into_pyobject(py)?.into_any().unbind())
        }
        DataFrameType::Generic => {
            // Generic - just return list of dicts
            Ok(processed_dicts.into_pyobject(py)?.into_any().unbind())
        }
    }
}

/// Reconstruct pandas DataFrame
#[cfg(feature = "python")]
fn reconstruct_pandas_df(py: Python, records: Vec<Py<PyAny>>) -> PyResult<Py<PyAny>> {
    // Convert to Python list once — O(1) refcount clone instead of O(N) item clones
    let py_list = records.into_pyobject(py)?.into_any().unbind();

    match cached_import(py, &PANDAS_MODULE, "pandas") {
        Ok(pandas) => match pandas.call_method1("DataFrame", (py_list.clone_ref(py),)) {
            Ok(df) => Ok(df.unbind()),
            Err(_) => Ok(py_list),
        },
        Err(_) => Ok(py_list),
    }
}

/// Reconstruct polars DataFrame
#[cfg(feature = "python")]
fn reconstruct_polars_df(py: Python, records: Vec<Py<PyAny>>) -> PyResult<Py<PyAny>> {
    // Convert to Python list once — O(1) refcount clone instead of O(N) item clones
    let py_list = records.into_pyobject(py)?.into_any().unbind();

    match cached_import(py, &POLARS_MODULE, "polars") {
        Ok(polars) => match polars.call_method1("DataFrame", (py_list.clone_ref(py),)) {
            Ok(df) => Ok(df.unbind()),
            Err(_) => Ok(py_list),
        },
        Err(_) => Ok(py_list),
    }
}

/// Reconstruct PyArrow Table
#[cfg(feature = "python")]
fn reconstruct_pyarrow_table(py: Python, records: Vec<Py<PyAny>>) -> PyResult<Py<PyAny>> {
    // Convert to Python list once — O(1) refcount clone instead of O(N) item clones
    let py_list = records.into_pyobject(py)?.into_any().unbind();

    match cached_import(py, &PYARROW_MODULE, "pyarrow") {
        Ok(pyarrow) => {
            let table_class = pyarrow.getattr("Table")?;
            match table_class.call_method1("from_pylist", (py_list.clone_ref(py),)) {
                Ok(table) => Ok(table.unbind()),
                Err(_) => Ok(py_list),
            }
        }
        Err(_) => Ok(py_list),
    }
}

// =============================================================================
// Series Reconstruction Functions
// =============================================================================

/// Reconstruct Series from list (with fallback to list)
#[cfg(feature = "python")]
fn reconstruct_series(
    py: Python,
    series_type: SeriesType,
    processed_items: Vec<Py<PyAny>>,
) -> PyResult<Py<PyAny>> {
    match series_type {
        SeriesType::Pandas => reconstruct_pandas_series(py, processed_items),
        SeriesType::Polars => reconstruct_polars_series(py, processed_items),
        SeriesType::PyArrow => reconstruct_pyarrow_array(py, processed_items),
        SeriesType::PySpark => {
            // PySpark doesn't have Series - fallback to list
            Ok(processed_items.into_pyobject(py)?.into_any().unbind())
        }
        SeriesType::Generic => {
            // Generic - just return list
            Ok(processed_items.into_pyobject(py)?.into_any().unbind())
        }
    }
}

/// Reconstruct pandas Series
#[cfg(feature = "python")]
fn reconstruct_pandas_series(py: Python, items: Vec<Py<PyAny>>) -> PyResult<Py<PyAny>> {
    // Convert to Python list once — O(1) refcount clone instead of O(N) item clones
    let py_list = items.into_pyobject(py)?.into_any().unbind();

    match cached_import(py, &PANDAS_MODULE, "pandas") {
        Ok(pandas) => match pandas.call_method1("Series", (py_list.clone_ref(py),)) {
            Ok(series) => Ok(series.unbind()),
            Err(_) => Ok(py_list),
        },
        Err(_) => Ok(py_list),
    }
}

/// Reconstruct polars Series
#[cfg(feature = "python")]
fn reconstruct_polars_series(py: Python, items: Vec<Py<PyAny>>) -> PyResult<Py<PyAny>> {
    // Convert to Python list once — O(1) refcount clone instead of O(N) item clones
    let py_list = items.into_pyobject(py)?.into_any().unbind();

    match cached_import(py, &POLARS_MODULE, "polars") {
        Ok(polars) => match polars.call_method1("Series", (py_list.clone_ref(py),)) {
            Ok(series) => Ok(series.unbind()),
            Err(_) => Ok(py_list),
        },
        Err(_) => Ok(py_list),
    }
}

/// Reconstruct PyArrow Array
#[cfg(feature = "python")]
fn reconstruct_pyarrow_array(py: Python, items: Vec<Py<PyAny>>) -> PyResult<Py<PyAny>> {
    // Convert to Python list once — O(1) refcount clone instead of O(N) item clones
    let py_list = items.into_pyobject(py)?.into_any().unbind();

    match cached_import(py, &PYARROW_MODULE, "pyarrow") {
        Ok(pyarrow) => match pyarrow.call_method1("array", (py_list.clone_ref(py),)) {
            Ok(array) => Ok(array.unbind()),
            Err(_) => Ok(py_list),
        },
        Err(_) => Ok(py_list),
    }
}

// =============================================================================
// Normalise: Wide DataFrame Reconstruction (execute(..., normalise=True))
// =============================================================================
//
// Unlike the lenient `reconstruct_pandas_df`/`reconstruct_polars_df`/
// `reconstruct_pyarrow_table` above (used by plain `execute(df)`, which silently
// falls back to a list of dicts if the target library isn't installed), everything
// in this section is strict: `normalise=True` is an explicit request for a real
// DataFrame, so a missing library or an un-normaliseable row is a clear
// `JsonToolsError`, never a silent fallback.

/// Convert a Python list whose items are each either a JSON string or a Python
/// dict into per-item JSON strings. The same mixed-item handling `execute()`'s
/// list branch and `execute_series` already do inline, factored out here since
/// `extract_normalise_json_strings` needs it for both list input and
/// Series-derived lists.
#[cfg(feature = "python")]
fn mixed_pylist_to_json_strings(py: Python<'_>, list: &Bound<'_, PyList>) -> PyResult<Vec<String>> {
    let mut json_strings = Vec::with_capacity(list.len());
    for item in list.iter() {
        if let Ok(json_str) = item.extract::<String>() {
            json_strings.push(json_str);
        } else if item.is_instance_of::<PyDict>() {
            let json_str = py_dumps(py, &item)
                .map_err(|e| JsonToolsError::new_err(format!("Failed to convert item: {e}")))?;
            json_strings.push(json_str);
        } else {
            return Err(PyValueError::new_err(
                "List/Series items must be either JSON strings or Python dictionaries",
            ));
        }
    }
    Ok(json_strings)
}

/// Coerce any shape `execute()` accepts into a uniform `Vec<String>` of JSON rows
/// for `normalise=True` -- a bare `str`/`dict` becomes a single-row `Vec`, matching
/// how plain `execute()` treats those as one opaque unit. Also returns the
/// detected input structure (when the input was itself a live DataFrame/Series),
/// used by `resolve_normalise_target` to default the output to the input's own
/// backend.
#[cfg(feature = "python")]
fn extract_normalise_json_strings(
    json_input: &Bound<'_, PyAny>,
) -> PyResult<(Vec<String>, Option<DataStructureType>)> {
    let py = json_input.py();

    if let Some(structure) = detect_data_structure(json_input)? {
        let json_strings = match structure {
            DataStructureType::DataFrame(df_type) => {
                let rows = dataframe_to_json_strings(json_input, df_type)?;
                // Unconditional here (no is_flatten_mode() check needed): the only
                // caller, execute_normalise, already hard-requires flatten mode
                // before reaching this function at all -- see its doc comment.
                let rows = expand_json_string_columns(py, rows)?;
                // See `unnest_object_valued_columns`'s doc comment -- same
                // column-name-prefix removal `execute_dataframe` applies,
                // needed here too since normalise=True has its own separate
                // DataFrame-to-json_strings path rather than sharing that one.
                rows.into_iter()
                    .map(|row| unnest_object_valued_columns(&row).unwrap_or(row))
                    .collect()
            }
            DataStructureType::Series(series_type) => {
                let list = series_to_list(json_input, series_type)?;
                mixed_pylist_to_json_strings(py, &list)?
            }
        };
        return Ok((json_strings, Some(structure)));
    }

    if let Ok(json_str) = json_input.extract::<String>() {
        return Ok((vec![json_str], None));
    }

    if json_input.is_instance_of::<PyDict>() {
        let json_str = py_dumps(py, json_input)
            .map_err(|e| JsonToolsError::new_err(format!("Failed to convert Python dict: {e}")))?;
        return Ok((vec![json_str], None));
    }

    if json_input.is_instance_of::<PyList>() {
        let list = json_input.cast::<PyList>()?;
        let json_strings = mixed_pylist_to_json_strings(py, list)?;
        return Ok((json_strings, None));
    }

    Err(PyValueError::new_err(
        "json_input must be a JSON string, Python dict, list of JSON strings/dicts, DataFrame, or Series",
    ))
}

#[cfg(feature = "python")]
static PANDAS_MODULE: PyOnceLock<Py<PyModule>> = PyOnceLock::new();
#[cfg(feature = "python")]
static POLARS_MODULE: PyOnceLock<Py<PyModule>> = PyOnceLock::new();
#[cfg(feature = "python")]
static PYARROW_MODULE: PyOnceLock<Py<PyModule>> = PyOnceLock::new();
#[cfg(feature = "python")]
static PYSPARK_MODULE: PyOnceLock<Py<PyModule>> = PyOnceLock::new();
#[cfg(feature = "python")]
static PYSPARK_SQL_MODULE: PyOnceLock<Py<PyModule>> = PyOnceLock::new();
#[cfg(feature = "python")]
static PYSPARK_TYPES_MODULE: PyOnceLock<Py<PyModule>> = PyOnceLock::new();

/// Import-and-cache a top-level module the first time it's needed. Mirrors
/// `json_callables`'s existing `PyOnceLock` idiom (see its doc comment)
/// applied to modules instead of callables: every `normalise=True`/PySpark-
/// `execute()` call previously paid a fresh `sys.modules` lookup +
/// module-object materialization on each of `resolve_normalise_target`'s
/// auto-detect probe, `require_importable`, and every `reconstruct_*_
/// normalise` function -- up to 4 redundant imports of the *same* module
/// (e.g. `reconstruct_pyspark_normalise` importing `pandas` just to check
/// it's installed, then calling `reconstruct_pandas_normalise`, which
/// imports `pandas` again) on a single call.
#[cfg(feature = "python")]
fn cached_import<'py>(
    py: Python<'py>,
    cell: &'static PyOnceLock<Py<PyModule>>,
    name: &str,
) -> PyResult<Bound<'py, PyModule>> {
    let module = cell.get_or_try_init(py, || py.import(name).map(|m| m.unbind()))?;
    Ok(module.bind(py).clone())
}

/// Resolve the effective `NormaliseTarget`: an explicit `target=` wins outright;
/// otherwise an input that was itself a live DataFrame/Series of a known backend
/// keeps that backend; otherwise try pandas -> polars -> pyarrow, first installed
/// wins. `pyspark` is deliberately excluded from this last bare-JSON-input
/// fallback -- creating a SparkSession-dependent result as a silent default for a
/// plain string/dict input would be surprising, so pyspark is only reachable via
/// an explicit `target="pyspark"` or when the input itself was already a
/// live PySpark object.
#[cfg(feature = "python")]
fn resolve_normalise_target(
    py: Python<'_>,
    detected: Option<DataStructureType>,
    requested: Option<NormaliseTarget>,
) -> PyResult<NormaliseTarget> {
    if let Some(target) = requested {
        return Ok(target);
    }

    let from_input = match detected {
        Some(DataStructureType::DataFrame(t)) => NormaliseTarget::from_dataframe_type(t),
        Some(DataStructureType::Series(t)) => NormaliseTarget::from_series_type(t),
        None => None,
    };
    if let Some(target) = from_input {
        return Ok(target);
    }

    for candidate in [
        NormaliseTarget::Pandas,
        NormaliseTarget::Polars,
        NormaliseTarget::PyArrow,
    ] {
        let cell = match candidate {
            NormaliseTarget::Pandas => &PANDAS_MODULE,
            NormaliseTarget::Polars => &POLARS_MODULE,
            NormaliseTarget::PyArrow => &PYARROW_MODULE,
            NormaliseTarget::PySpark => unreachable!("PySpark excluded from this candidate list"),
        };
        if cached_import(py, cell, candidate.name()).is_ok() {
            return Ok(candidate);
        }
    }

    Err(JsonToolsError::new_err(
        "normalise=True could not auto-detect a target DataFrame library: none of pandas, \
         polars, pyarrow are installed. Pass target=\"pandas\"|\"polars\"|\"pyarrow\"|\"pyspark\" \
         explicitly, or install one of these libraries.",
    ))
}

/// Strict presence check for `normalise=True`'s target library -- see this
/// section's header comment for why this doesn't fall back silently like the
/// lenient `reconstruct_*_df` helpers do.
#[cfg(feature = "python")]
fn require_importable<'py>(
    py: Python<'py>,
    target: NormaliseTarget,
) -> PyResult<Bound<'py, PyModule>> {
    require_pyarrow_for_normalise(py, target.name())?;
    let cell = match target {
        NormaliseTarget::Pandas => &PANDAS_MODULE,
        NormaliseTarget::Polars => &POLARS_MODULE,
        NormaliseTarget::PyArrow => &PYARROW_MODULE,
        NormaliseTarget::PySpark => &PYSPARK_MODULE,
    };
    cached_import(py, cell, target.name()).map_err(|_| {
        JsonToolsError::new_err(format!(
            "normalise(target=\"{}\") requires the '{}' package to be installed",
            target.name(),
            target.name()
        ))
    })
}

/// `normalise=True`'s reconstruction is Arrow-native (github.com/amaye15/
/// JSON-Tools-rs/issues/35): pandas and pyspark are derived from a genuine
/// `pyarrow.Table` (`build_normalise_table`), so pyarrow itself is now
/// required for those two targets, not just `target="pyarrow"` -- verified
/// directly that there is no pyarrow-free way to get genuinely Arrow-built
/// data into a pandas DataFrame (every route tried needs pyarrow internally,
/// even via a polars intermediary); pyspark inherits the same requirement
/// since its own reconstruction bridges through pandas. `target="pyarrow"`
/// itself is exempted from calling this separately -- `require_importable`'s
/// own subsequent pyarrow-specific check already covers it with a
/// pyarrow-specific message, calling this too would just duplicate it.
/// `target="polars"` is also exempted: verified directly (in a pyarrow-free
/// environment) that `pl.from_arrow` accepts the raw pyo3-arrow
/// capsule-protocol object without pyarrow at all, so `build_normalise_table`
/// skips the pyarrow-materialization step entirely for that target --
/// preserving the same zero-pyarrow-dependency guarantee `target="polars"`
/// already had before this round.
#[cfg(feature = "python")]
fn require_pyarrow_for_normalise(py: Python<'_>, target_name: &str) -> PyResult<()> {
    if target_name == "pyarrow" || target_name == "polars" {
        return Ok(());
    }
    cached_import(py, &PYARROW_MODULE, "pyarrow").map_err(|_| {
        JsonToolsError::new_err(format!(
            "normalise(target=\"{target_name}\") requires the 'pyarrow' package to be \
             installed -- normalise's reconstruction builds a real Arrow table \
             internally, then derives {target_name} from it, regardless of which \
             target was requested"
        ))
    })?;
    Ok(())
}

/// Auto-discover the active PySpark session for `target="pyspark"` (and plain
/// `execute()` on a PySpark DataFrame, which reuses this same reconstruction
/// mechanism). No `spark=` parameter is offered -- the caller is expected to
/// already be inside a Spark driver/notebook with a session created
/// (`SparkSession.builder.getOrCreate()`).
#[cfg(feature = "python")]
fn require_active_spark_session(py: Python<'_>) -> PyResult<Bound<'_, PyAny>> {
    // See `require_pyarrow_for_normalise`'s doc comment -- PySpark
    // reconstruction bridges through pandas, which itself requires pyarrow
    // under this engine, so check it explicitly with a clear message here
    // too (this call site doesn't go through `require_importable`).
    require_pyarrow_for_normalise(py, "pyspark")?;
    let pyspark_sql = cached_import(py, &PYSPARK_SQL_MODULE, "pyspark.sql").map_err(|_| {
        JsonToolsError::new_err(
            "normalise(target=\"pyspark\") requires the 'pyspark' package to be installed",
        )
    })?;
    let session_cls = pyspark_sql.getattr("SparkSession")?;
    let active = session_cls.call_method0("getActiveSession")?;
    if active.is_none() {
        return Err(JsonToolsError::new_err(
            "normalise(target=\"pyspark\") requires an active SparkSession \
             (SparkSession.getActiveSession() returned None); create one first, \
             e.g. SparkSession.builder.getOrCreate()",
        ));
    }
    Ok(active)
}

// =============================================================================
// Arrow-native normalise() reconstruction (github.com/amaye15/JSON-Tools-rs/
// issues/35 -- "native Arrow output" / real column typing, 2026-07-31)
// =============================================================================
//
// Replaces the previous `union_and_columnarize` + four `reconstruct_*_
// normalise` functions' `Bound<PyAny>`-boxing approach with a single pass
// that builds a real Arrow `RecordBatch` directly from `RawValue`-parsed
// rows -- never boxing a scalar value into a Python object -- then derives
// every requested target from that ONE canonical table via the cheapest
// conversion path verified for each target (measured directly, see
// CHANGELOG.md's v0.9.20 entry for the numbers this design is based on):
//   - pyarrow: `PyTable::into_pyarrow(py)` -- genuinely zero-copy.
//   - pandas: `.to_pandas(types_mapper=pd.ArrowDtype)` -- genuinely
//     zero-copy, but changes the output dtype from plain numpy dtypes to
//     Arrow-backed ones (e.g. `int64` -> `int64[pyarrow]`) -- an intentional,
//     confirmed choice, not an oversight.
//   - polars: `pl.from_arrow(table, rechunk=False)` -- near-zero-copy
//     (verified: far cheaper than a real copy, but not a pure O(1) view).
//   - pyspark: `.to_pandas()` (plain, NOT ArrowDtype -- see
//     `reconstruct_pyspark_normalise`'s doc comment for why) feeding the
//     existing, unchanged `SparkSession.createDataFrame(df, schema)` bridge.
//     Not zero-copy -- architecturally impossible across the JVM process
//     boundary -- but still avoids all per-value PyObject boxing.
//
// List-valued columns (a genuinely list-valued JSON leaf, or
// `handle_key_collision(True)`'s collision arrays) build as real Arrow
// `List<T>` columns, not stringified -- verified directly (an isolated
// scratch-crate probe) that pyarrow/polars/pandas all consume `List<T>`
// correctly. A column that's genuinely mixed-scalar-kind across rows with no
// list involved still stringifies: Arrow's `Union` type, the only real
// alternative, was tested directly and rejected outright by both polars
// (`ComputeError: cannot create series from Union(...)`) and pandas
// (`NotImplementedError`/`ArrowNotImplementedError`) -- a confirmed dead end
// for this ecosystem, not a laziness shortcut.

/// Parse each processed (flattened) JSON string into `RawValue`-backed rows,
/// union every row's keys in first-seen order, decide each column's real
/// Arrow type, and build the corresponding `RecordBatch` -- all without ever
/// boxing a scalar value into a Python object. Returns the built table and
/// the Rust-native `Schema` it was built from (so `reconstruct_pyspark_
/// normalise` can derive its PySpark schema directly from known Arrow
/// `DataType`s instead of re-parsing a string type representation back out
/// of Python).
///
/// `via_pyarrow` controls how the table crosses into Python: `true` calls
/// `PyTable::into_pyarrow` to materialize a genuine `pyarrow.Table`
/// (verified zero-copy) -- required for pandas/pyspark, which have no
/// pyarrow-free route to real Arrow-built data (verified directly: every
/// path tried, including via a polars intermediary, needs pyarrow
/// internally). `false` returns the raw pyo3-arrow capsule-protocol object
/// via `into_pyobject` instead -- polars' own `from_arrow` accepts this
/// directly (verified directly, in a pyarrow-free environment), so `target=
/// "polars"` keeps working exactly as before this round: no new pyarrow
/// dependency.
///
/// `dates_enabled` (the caller's own `.convert_dates()`/`.auto_convert_types()`
/// setting -- see `raw_scalar_kind`'s doc comment) gates whether a
/// date/datetime-shaped string column resolves to a real `Date32`/
/// `TimestampUtcMicros` Arrow column instead of `Utf8`. Only applied to
/// top-level scalar columns, never to list-column elements (`ColumnPlan`'s
/// doc comment) -- list elements always pass `false` regardless.
#[cfg(feature = "python")]
fn build_normalise_table<'py>(
    py: Python<'py>,
    processed: &[String],
    via_pyarrow: bool,
    dates_enabled: bool,
) -> PyResult<(Bound<'py, PyAny>, Arc<Schema>)> {
    let n_rows = processed.len();
    let mut rows: Vec<IndexMap<std::borrow::Cow<'_, str>, &serde_json::value::RawValue>> =
        Vec::with_capacity(n_rows);
    let mut key_order: IndexSet<String> = IndexSet::new();

    for (idx, json_str) in processed.iter().enumerate() {
        // Zero-copy borrowed-key parse first (correct whenever no key needs
        // JSON-unescaping, the overwhelmingly common case for flattened
        // dotted-path keys); falls back to owned keys, with the original
        // detailed parse error, only when that fails. Real-world `normalise`
        // input is typically many rows sharing (almost) the same column set
        // (the whole point of a wide DataFrame), so `key_order` -- unlike
        // each row's own field map -- still needs owned `String`s, but only
        // the *first* row to introduce a given key should pay for one: the
        // `contains` check below skips the allocation entirely for every
        // row that repeats an already-seen key, rather than unconditionally
        // cloning (and immediately discarding) a fresh String per key on
        // every single row -- a real, measured cost at issue #31's own
        // scale (754 rows x 4,042 columns is ~3M wasted clones otherwise).
        let fields: IndexMap<std::borrow::Cow<'_, str>, &serde_json::value::RawValue> =
            if let Ok(fields) =
                serde_json::from_str::<IndexMap<&str, &serde_json::value::RawValue>>(json_str)
            {
                fields
                    .into_iter()
                    .map(|(k, v)| (std::borrow::Cow::Borrowed(k), v))
                    .collect()
            } else {
                let owned: IndexMap<String, &serde_json::value::RawValue> =
                    serde_json::from_str(json_str).map_err(|e| {
                        JsonToolsError::new_err(format!(
                            "normalise=True requires every flattened row to be a JSON object; \
                             row {idx} failed to parse as one: {e}"
                        ))
                    })?;
                owned
                    .into_iter()
                    .map(|(k, v)| (std::borrow::Cow::Owned(k), v))
                    .collect()
            };
        for key in fields.keys() {
            if !key_order.contains(key.as_ref()) {
                key_order.insert(key.to_string());
            }
        }
        rows.push(fields);
    }

    let n_keys = key_order.len();

    if n_keys == 0 {
        // No columns at all (zero rows, or every row was `{}`) -- a genuinely
        // empty table. Arrow's own RecordBatch can't represent "N rows, 0
        // columns" (row count is derived from column lengths), the same
        // degenerate case the old PySpark-specific code special-cased.
        let schema = Arc::new(Schema::empty());
        let batch = RecordBatch::new_empty(schema.clone());
        let table = PyTable::try_new(vec![batch], schema.clone())
            .map_err(|e| JsonToolsError::new_err(format!("Failed to build empty table: {e}")))?;
        return Ok((table_to_python(table, py, via_pyarrow)?, schema));
    }

    // Pass 1a: scatter each row's own entries into pre-sized per-column slots
    // (same single-native-iteration-per-row idiom `union_and_columnarize`
    // established -- O(total fields present), not O(n_rows * n_keys)), and
    // detect which columns are ever list-valued.
    let mut column_slots: Vec<Vec<Option<&serde_json::value::RawValue>>> =
        (0..n_keys).map(|_| vec![None; n_rows]).collect();
    let mut any_list_per_col: Vec<bool> = vec![false; n_keys];

    for (row_idx, row) in rows.iter().enumerate() {
        for (key, raw) in row {
            let Some(col_idx) = key_order.get_index_of(key.as_ref()) else {
                continue; // unreachable: key_order was built from these same rows above
            };
            if raw.get().as_bytes().first() == Some(&b'[') {
                any_list_per_col[col_idx] = true;
            }
            column_slots[col_idx][row_idx] = Some(*raw);
        }
    }

    // Pass 1b+2, per column: aggregate kind flags (scalar interpretation, or
    // -- for a list-valued column -- element kind across every list cell's
    // elements plus every to-be-wrapped scalar cell's own kind, matching
    // `union_and_columnarize`'s wrap-then-classify order), decide this
    // column's `ColumnPlan`, then build its real Arrow array. A list
    // column's cells are parsed exactly once each (cached as `ListCell` --
    // see its doc comment) and reused for the build step below instead of
    // re-parsing the same JSON array text a second time; a scalar column's
    // classification is cheap enough (no parse/allocation, just a byte-shape
    // check) that a second pass over its own already-borrowed `&RawValue`
    // cells costs nothing extra worth caching for.
    let mut fields: Vec<Field> = Vec::with_capacity(n_keys);
    let mut arrays: Vec<ArrayRef> = Vec::with_capacity(n_keys);
    for (col_idx, key) in key_order.iter().enumerate() {
        if any_list_per_col[col_idx] {
            let mut flags = KindFlags::default();
            let mut cached: Vec<ListCell<'_>> = Vec::with_capacity(n_rows);
            for cell in &column_slots[col_idx] {
                let parsed = match cell {
                    None => ListCell::Absent,
                    Some(raw) => {
                        let text = raw.get();
                        // Date detection never applies to list elements (see
                        // ColumnPlan's doc comment) -- always `false` here
                        // regardless of the caller's own setting.
                        match text.as_bytes().first() {
                            Some(b'n') => ListCell::Null,
                            Some(b'[') => {
                                let elems: Vec<&serde_json::value::RawValue> =
                                    serde_json::from_str(text).unwrap_or_default();
                                for elem in &elems {
                                    if let Some(k) = raw_scalar_kind(elem.get(), false) {
                                        flags.merge(k);
                                    }
                                }
                                ListCell::Elems(elems)
                            }
                            _ => {
                                if let Some(k) = raw_scalar_kind(text, false) {
                                    flags.merge(k);
                                }
                                ListCell::Scalar(text)
                            }
                        }
                    }
                };
                cached.push(parsed);
            }
            let mut builder = ColumnBuilder::new(ColumnPlan::List(flags.resolve()), n_rows);
            fields.push(builder.arrow_field(key));
            for cell in &cached {
                builder.append_list_cell(cell);
            }
            arrays.push(builder.finish());
        } else {
            let mut flags = KindFlags::default();
            for cell in &column_slots[col_idx] {
                let Some(raw) = cell else { continue };
                if let Some(k) = raw_scalar_kind(raw.get(), dates_enabled) {
                    flags.merge(k);
                }
            }
            let mut builder = ColumnBuilder::new(ColumnPlan::Scalar(flags.resolve()), n_rows);
            fields.push(builder.arrow_field(key));
            for cell in &column_slots[col_idx] {
                builder.append_row(cell.map(serde_json::value::RawValue::get));
            }
            arrays.push(builder.finish());
        }
    }

    let schema = Arc::new(Schema::new(fields));
    let batch = RecordBatch::try_new(schema.clone(), arrays)
        .map_err(|e| JsonToolsError::new_err(format!("Failed to build record batch: {e}")))?;
    let table = PyTable::try_new(vec![batch], schema.clone())
        .map_err(|e| JsonToolsError::new_err(format!("Failed to build Arrow table: {e}")))?;
    Ok((table_to_python(table, py, via_pyarrow)?, schema))
}

/// Cross a built `PyTable` into Python. See `build_normalise_table`'s
/// `via_pyarrow` doc comment for what each mode requires/supports.
#[cfg(feature = "python")]
fn table_to_python(
    table: PyTable,
    py: Python<'_>,
    via_pyarrow: bool,
) -> PyResult<Bound<'_, PyAny>> {
    if via_pyarrow {
        table.into_pyarrow(py)
    } else {
        Ok(table.into_pyobject(py)?.into_any())
    }
}

/// Reconstruct a pandas DataFrame from the canonical Arrow table, via
/// `to_pandas(types_mapper=pd.ArrowDtype)` -- genuinely zero-copy (verified:
/// flat ~0.3ms regardless of row count, vs. linear-scaling ~700ms+ at 5M rows
/// for plain numpy dtypes). This is an intentional, user-confirmed breaking
/// dtype change from the old `union_and_columnarize`-based output (`int64`
/// becomes `int64[pyarrow]` etc.) -- see CHANGELOG.md's v0.9.20 entry.
#[cfg(feature = "python")]
fn reconstruct_pandas_normalise(py: Python<'_>, table: &Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
    let pandas = cached_import(py, &PANDAS_MODULE, "pandas")?;
    let arrow_dtype = pandas.getattr("ArrowDtype")?;
    let kwargs = PyDict::new(py);
    kwargs.set_item("types_mapper", arrow_dtype)?;
    let df = table.call_method("to_pandas", (), Some(&kwargs))?;
    Ok(df.unbind())
}

/// Reconstruct a polars DataFrame from the canonical Arrow table, via
/// `pl.from_arrow(table, rechunk=False)` -- near-zero-copy (verified: far
/// cheaper than a real copy, though not a pure O(1) view like the pandas
/// ArrowDtype path above -- `rechunk=False` avoids paying for a forced
/// contiguous-memory pass this engine's single-`RecordBatch` output never
/// needs anyway).
#[cfg(feature = "python")]
fn reconstruct_polars_normalise(py: Python<'_>, table: &Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
    let polars = cached_import(py, &POLARS_MODULE, "polars")?;
    let kwargs = PyDict::new(py);
    kwargs.set_item("rechunk", false)?;
    let df = polars.call_method("from_arrow", (table,), Some(&kwargs))?;
    Ok(df.unbind())
}

/// Map an Arrow `DataType` to its PySpark SQL type. Only the shapes this
/// engine's own `ColumnBuilder` ever produces are handled (Boolean/Int64/
/// Float64/Date32/Timestamp/Utf8, and List of one of those) -- exhaustive
/// for this module's own output, not a general Arrow-to-Spark mapper.
#[cfg(feature = "python")]
fn arrow_type_to_spark<'py>(
    types_mod: &Bound<'py, PyModule>,
    dt: &DataType,
) -> PyResult<Bound<'py, PyAny>> {
    match dt {
        DataType::Boolean => types_mod.getattr("BooleanType")?.call0(),
        DataType::Int64 => types_mod.getattr("LongType")?.call0(),
        DataType::Float64 => types_mod.getattr("DoubleType")?.call0(),
        DataType::Date32 => types_mod.getattr("DateType")?.call0(),
        DataType::Timestamp(_, _) => types_mod.getattr("TimestampType")?.call0(),
        DataType::Utf8 => types_mod.getattr("StringType")?.call0(),
        DataType::List(inner) => {
            let elem_type = arrow_type_to_spark(types_mod, inner.data_type())?;
            types_mod.getattr("ArrayType")?.call1((elem_type,))
        }
        other => Err(JsonToolsError::new_err(format!(
            "Unsupported Arrow type for PySpark schema derivation: {other:?}"
        ))),
    }
}

/// Reconstruct a real PySpark DataFrame from the canonical Arrow table, via
/// Spark's own Arrow-optimized `SparkSession.createDataFrame(pandas.DataFrame,
/// schema)` bridge (Arrow conversion on by default since Spark 3.0 via
/// `spark.sql.execution.arrow.pyspark.enabled`) -- the idiomatic, "native" way
/// to get driver-side tabular data into a real distributed DataFrame. This
/// mechanism itself is unchanged from before this round's rewrite; only its
/// input changed, from `NormaliseColumns`' boxed-object columns to a plain
/// pandas DataFrame derived from this module's own Arrow table.
///
/// The pandas bridge here deliberately uses **plain** `to_pandas()`, not
/// `types_mapper=pd.ArrowDtype` (unlike `reconstruct_pandas_normalise`
/// above): this exact bridge already has a documented history of silent
/// corruption from pandas nullable-extension dtypes on Spark's *non*-Arrow
/// fallback path (taken automatically when pyarrow isn't installed) -- an
/// earlier version of this function used pandas's nullable `"string"` dtype
/// for an all-null column and it serialized as the *literal string* `"<NA>"`
/// instead of a real null on that fallback path. `ArrowDtype` is exactly this
/// same category of nullable extension dtype, so it inherits that same risk
/// until proven otherwise; plain Python `None`-backed columns were verified
/// correct on both the Arrow and non-Arrow paths, so that's what's used here.
/// The explicit schema (derived directly from this table's own Arrow schema,
/// not re-inferred) is what actually made that earlier all-null-column
/// corruption bug (`StructType([])` from schema inference) go away in the
/// first place, and remains required for the same reason.
///
/// Used by both `execute_normalise` (`target="pyspark"`) and, since
/// github.com/amaye15/JSON-Tools-rs/issues/31, plain `execute_dataframe` for
/// PySpark input.
#[cfg(feature = "python")]
fn reconstruct_pyspark_normalise(
    py: Python<'_>,
    spark: &Bound<'_, PyAny>,
    table: &Bound<'_, PyAny>,
    schema: &Schema,
) -> PyResult<Py<PyAny>> {
    let types_mod = cached_import(py, &PYSPARK_TYPES_MODULE, "pyspark.sql.types")?;

    if schema.fields().is_empty() {
        let empty_schema = types_mod.getattr("StructType")?.call0()?;
        let empty_rows: Vec<Py<PyAny>> = Vec::new();
        let df = spark.call_method1("createDataFrame", (empty_rows, empty_schema))?;
        return Ok(df.unbind());
    }

    cached_import(py, &PANDAS_MODULE, "pandas").map_err(|_| {
        JsonToolsError::new_err(
            "Reconstructing a PySpark DataFrame (via execute() or \
             normalise(target=\"pyspark\")) requires pandas to be installed -- it's \
             used internally to build the DataFrame handed to Spark's \
             Arrow-optimized createDataFrame() bridge",
        )
    })?;

    let struct_field_cls = types_mod.getattr("StructField")?;
    let mut spark_fields: Vec<Bound<'_, PyAny>> = Vec::with_capacity(schema.fields().len());
    for field in schema.fields() {
        let field_type = arrow_type_to_spark(&types_mod, field.data_type())?;
        spark_fields.push(struct_field_cls.call1((field.name(), field_type, true))?);
    }
    let spark_schema = types_mod.getattr("StructType")?.call1((spark_fields,))?;

    let pandas_df = table.call_method0("to_pandas")?;
    let df = spark.call_method1("createDataFrame", (pandas_df, spark_schema))?;
    Ok(df.unbind())
}

// =============================================================================
// Flat-DataFrame fast path for plain `.flatten().execute(df)`
// =============================================================================
//
// `execute_dataframe` below always round-trips the whole DataFrame through
// JSON text: serialize every row (`dataframe_to_json_strings`), parse+flatten
// each row in Rust, deserialize the output JSON back into Python dicts
// (`py_loads`), reconstruct a DataFrame from those dicts. Measured directly
// (interleaved A/B): for a DataFrame with no nested/struct columns, that
// round trip costs ~90-99ms for 20K rows x 20 cols, of which pandas' own
// `to_json()` is ~36ms, this crate's own flatten logic (isolated) is only
// ~6.5ms, and deserialize+reconstruct is ~18-60ms -- the JSON-text round trip
// itself is the cost, paid even when there's nothing nested to flatten (a
// common case: generic pipelines that call `.flatten()` defensively, or use
// it purely for its key-transform/type-conversion features on already-
// tabular data).
//
// This fast path reads column values directly, applies the exact same
// per-cell value-transform logic (`convert_string_for_mode`/
// `apply_replacement_patterns`, unchanged) directly in Rust, and writes
// results back into columns/renames columns natively -- never touching
// `to_json`/`py_loads`/`DataFrame(list_of_dicts)`. Scope: plain
// `.flatten().execute(df)` only (not `normalise=True`, which already has its
// own, separately-optimized Arrow-native path via `build_normalise_table`).
// Eligibility is a whole-DataFrame decision: any disqualifying column, mode,
// or config interaction falls through to the existing pipeline unchanged --
// this is strictly an optimization, never a second code path with its own
// behavior to keep in sync by hand for the cases it doesn't handle.

/// One output column's fast-path plan, in final (post-rename) output order.
#[cfg(feature = "python")]
enum FastPathColumn {
    /// Reuse the source column's existing Arrow array unchanged (a
    /// non-string dtype -- nothing for `auto_convert_types` to do, native
    /// nulls stay native).
    PassThrough { source_col: usize },
    /// Same as `PassThrough`, but the column's name is in `always_array_keys`
    /// -- wrap every cell (including null ones) as a 1-element list, per
    /// `flatten.rs`'s own confirmed semantics (a null cell becomes `[null]`,
    /// not a null list).
    PassThroughWrapped { source_col: usize },
    /// A string column: run the full value-transform pipeline per cell, then
    /// resolve the column's final type from the accumulated per-cell kinds
    /// (bool > numeric > string priority; mixed -> stringify).
    StringTransform { source_col: usize, wrap: bool },
}

/// A fully-resolved plan for the fast path: eligibility already confirmed,
/// nothing left to do but execute it. `output_columns` pairs each final
/// output name with its `FastPathColumn` plan (indexing back into the
/// caller's own `chunked_arrays`/`string_values`, keyed by *source* column
/// position), already in final output order (first-seen order of each
/// unique post-rename name, matching `flatten.rs`'s own collision-resolution
/// ordering).
#[cfg(feature = "python")]
struct FastPathPlan {
    output_columns: Vec<(String, FastPathColumn)>,
}

/// Classify a Polars/PyArrow column's Arrow `DataType` for fast-path
/// eligibility. `None` means disqualifying (nested/nullable-complex type) --
/// the whole DataFrame falls back, not just this column (see module doc
/// comment).
#[cfg(feature = "python")]
enum ArrowColKind {
    NonString,
    String,
}

#[cfg(feature = "python")]
fn classify_arrow_dtype(dt: &DataType) -> Option<ArrowColKind> {
    match dt {
        DataType::Struct(_)
        | DataType::List(_)
        | DataType::LargeList(_)
        | DataType::ListView(_)
        | DataType::LargeListView(_)
        | DataType::FixedSizeList(_, _)
        | DataType::Map(_, _)
        | DataType::Union(_, _)
        | DataType::Dictionary(_, _)
        | DataType::RunEndEncoded(_, _) => None,
        DataType::Utf8 | DataType::LargeUtf8 | DataType::Utf8View => Some(ArrowColKind::String),
        _ => Some(ArrowColKind::NonString),
    }
}

/// Check whether `df` (Polars/PyArrow only -- schema-level dtype access is
/// what makes this cheap, see module doc comment) qualifies for the fast
/// path under `config`, and if so, build its execution plan. Returns
/// `Ok(None)` for any disqualifying reason (never an error) -- the caller
/// falls through to the existing pipeline unchanged.
#[cfg(feature = "python")]
#[allow(clippy::type_complexity)]
fn check_arrow_fastpath_eligibility(
    df: &Bound<'_, PyAny>,
    df_type: DataFrameType,
    config: &ProcessingConfig,
) -> PyResult<
    Option<(
        FastPathPlan,
        Vec<PyChunkedArray>,
        Vec<Option<Vec<Option<CompactString>>>>,
    )>,
> {
    if !matches!(df_type, DataFrameType::Polars | DataFrameType::PyArrow) {
        return Ok(None);
    }

    // `remove_nulls`/`value_exclusions` also apply to a genuine (non-string)
    // scalar leaf, not just a string token -- confirmed directly against
    // `flatten.rs`'s `emit_scalar_value` (`remove_nulls && trimmed == b"null"`
    // and a `value_exclusions` check, both operating on the raw scalar text,
    // independent of `emit_string_value_shared`'s own string-specific
    // handling). A "pass through the source array unchanged" non-string
    // column can't honor either without per-cell text formatting + the same
    // "drop the whole column if every cell ends up filtered" handling the
    // string path needs -- real, buildable, but not done for v1. Disqualify
    // the whole DataFrame whenever either is configured, regardless of which
    // columns are actually affected -- correctness over coverage.
    if config.filtering.remove_nulls || config.replacements.has_value_exclusions() {
        return Ok(None);
    }

    let column_names = dataframe_column_names(df, df_type)?;
    if column_names.is_empty() {
        return Ok(None);
    }

    // A genuinely empty (0-row) DataFrame reconstructs, via the old
    // list-of-dicts path, to a table with *zero columns* (nothing to infer a
    // schema from an empty list) -- not "every source column, 0 rows".
    // Simplest correct behavior: treat 0 rows as disqualifying too, same as
    // 0 columns above, rather than replicate that degenerate case here.
    let first_col = dataframe_get_column(df, df_type, &column_names[0])?;
    if let Ok(chunked) = first_col.extract::<PyChunkedArray>() {
        if chunked.chunks().iter().map(|c| c.len()).sum::<usize>() == 0 {
            return Ok(None);
        }
    }

    let mut chunked_arrays: Vec<PyChunkedArray> = Vec::with_capacity(column_names.len());
    let mut kinds: Vec<ArrowColKind> = Vec::with_capacity(column_names.len());
    for name in &column_names {
        let col = dataframe_get_column(df, df_type, name)?;
        let Ok(chunked) = col.extract::<PyChunkedArray>() else {
            return Ok(None);
        };
        let Some(kind) = classify_arrow_dtype(chunked.data_type()) else {
            return Ok(None);
        };
        kinds.push(kind);
        chunked_arrays.push(chunked);
    }

    // String columns: confirm none secretly hold embedded JSON object/array
    // text (the same disqualifying condition `detect_and_extract_json_
    // columns_zerocopy` already treats as "needs real parsing, not a plain
    // string"), sampling at most `JSON_COLUMN_DETECTION_SAMPLE_SIZE` non-null
    // values per column via the same zero-copy extraction the value pipeline
    // will need anyway if this column turns out eligible.
    // Pure-Rust from here: `chunked_arrays` is already fully extracted
    // (above), so string-value extraction + the JSON-text sample check never
    // touch a `Bound<'py, PyAny>` -- release the GIL for it. This loop is
    // O(rows) (unlike the JSON-text sample check inside it, which is bounded
    // by `JSON_COLUMN_DETECTION_SAMPLE_SIZE`), so it's worth detaching for.
    let py = df.py();
    let string_values: Option<Vec<Option<Vec<Option<CompactString>>>>> = py.detach(|| {
        let mut string_values: Vec<Option<Vec<Option<CompactString>>>> =
            vec![None; column_names.len()];
        for (i, kind) in kinds.iter().enumerate() {
            if !matches!(kind, ArrowColKind::String) {
                continue;
            }
            let Some(values) = extract_arrow_string_values_from_chunked(&chunked_arrays[i]) else {
                return None; // schema said string, extraction disagreed -- bail safely
            };
            let sampled_json = values
                .iter()
                .flatten()
                .take(JSON_COLUMN_DETECTION_SAMPLE_SIZE)
                .any(|v| is_json_object_or_array_text(v));
            if sampled_json {
                return None;
            }
            string_values[i] = Some(values);
        }
        Some(string_values)
    });
    let Some(string_values) = string_values else {
        return Ok(None);
    };

    // Column-name planning: exclusions, then rename, preserving first-seen
    // order of each final unique name (matches `flatten.rs`'s own
    // collision-resolution ordering).
    let has_key_exclusions = config.replacements.has_key_exclusions();
    let mut final_name_first_seen: IndexMap<String, usize> = IndexMap::new(); // final name -> output slot
    let mut groups: Vec<Vec<usize>> = Vec::new(); // output slot -> source column indices, in order added
    for (i, name) in column_names.iter().enumerate() {
        if has_key_exclusions && matches_any_pattern(name, &config.replacements.key_exclusions) {
            continue;
        }
        let mut final_name = name.clone();
        if let Some(replaced) =
            apply_replacement_patterns(name, &config.replacements.key_replacements)
        {
            final_name = replaced;
        }
        if config.lowercase_keys {
            final_name = final_name.to_lowercase();
        }
        match final_name_first_seen.get(&final_name) {
            Some(&slot) => groups[slot].push(i),
            None => {
                let slot = groups.len();
                final_name_first_seen.insert(final_name, slot);
                groups.push(vec![i]);
            }
        }
    }

    if groups.is_empty() {
        return Ok(None); // every column excluded -- degenerate, let the existing path handle it
    }

    let has_collision_handling = config.collision.has_collision_handling();
    let has_always_array_keys = config.collision.has_always_array_keys();
    let mut output_columns = Vec::with_capacity(groups.len());
    for (final_name, _) in &final_name_first_seen {
        let slot = final_name_first_seen[final_name];
        let sources = &groups[slot];
        let force_array = has_always_array_keys
            && config
                .collision
                .always_array_keys
                .iter()
                .any(|k| k == final_name);

        if sources.len() > 1 {
            // A genuine rename-induced collision (input columns are unique by
            // construction). Real handling needs an array-typed column
            // zipping every source -- fall back to the full pipeline for v1
            // (see plan: rare trigger, only fires when a rename config
            // specifically collapses two distinct source names).
            if has_collision_handling || force_array {
                return Ok(None);
            }
            // No collision handling, not an always-array key: last-column-
            // wins, matching `flatten.rs`'s own resolved semantics exactly.
            let source_col = *sources.last().expect("sources non-empty");
            output_columns.push((
                final_name.clone(),
                plan_for_column(source_col, force_array, &kinds[source_col]),
            ));
        } else {
            let source_col = sources[0];
            output_columns.push((
                final_name.clone(),
                plan_for_column(source_col, force_array, &kinds[source_col]),
            ));
        }
    }

    Ok(Some((
        FastPathPlan { output_columns },
        chunked_arrays,
        string_values,
    )))
}

#[cfg(feature = "python")]
fn plan_for_column(source_col: usize, force_array: bool, kind: &ArrowColKind) -> FastPathColumn {
    match (kind, force_array) {
        (ArrowColKind::String, wrap) => FastPathColumn::StringTransform { source_col, wrap },
        (ArrowColKind::NonString, false) => FastPathColumn::PassThrough { source_col },
        (ArrowColKind::NonString, true) => FastPathColumn::PassThroughWrapped { source_col },
    }
}

/// Apply `value_replacements -> auto_convert_types -> remove_nulls ->
/// value_exclusions -> remove_empty_strings` to one string cell, in the
/// exact order `transform.rs`'s `emit_string_value_shared` uses (verified
/// directly against that function, not re-derived from memory). Returns
/// `None` for a filtered (should become null) cell, `Some(text)` where
/// `text` is JSON-fragment text (quoted+escaped for a plain string, a bare
/// token for a converted number/bool/date) ready for
/// `raw_scalar_kind`/`ColumnBuilder::append_row`.
#[cfg(feature = "python")]
fn transform_string_cell(raw: &str, config: &ProcessingConfig) -> Option<CompactString> {
    let has_replacements = config.replacements.has_value_replacements();
    let type_conversion_mode = config.type_conversion_mode;
    let auto_convert = type_conversion_mode != TypeConversionMode::Disabled;
    let has_value_exclusions = config.replacements.has_value_exclusions();

    if has_replacements {
        if let Some(replaced) =
            apply_replacement_patterns(raw, &config.replacements.value_replacements)
        {
            if config.filtering.remove_empty_strings && replaced.is_empty() {
                return None;
            }
            if auto_convert {
                if let Some(converted) = convert_string_for_mode(
                    &replaced,
                    type_conversion_mode,
                    &config.type_conversion,
                ) {
                    if config.filtering.remove_nulls && converted == "null" {
                        return None;
                    }
                    if has_value_exclusions
                        && matches_any_pattern(&converted, &config.replacements.value_exclusions)
                    {
                        return None;
                    }
                    return Some(CompactString::from(converted));
                }
            }
            if has_value_exclusions
                && matches_any_pattern(&replaced, &config.replacements.value_exclusions)
            {
                return None;
            }
            return Some(quote_json_fragment(&replaced));
        }
    }

    if auto_convert {
        if let Some(converted) =
            convert_string_for_mode(raw, type_conversion_mode, &config.type_conversion)
        {
            if config.filtering.remove_nulls && converted == "null" {
                return None;
            }
            if has_value_exclusions
                && matches_any_pattern(&converted, &config.replacements.value_exclusions)
            {
                return None;
            }
            return Some(CompactString::from(converted));
        }
    }

    if has_value_exclusions && matches_any_pattern(raw, &config.replacements.value_exclusions) {
        return None;
    }
    Some(quote_json_fragment(raw))
}

/// Build the JSON-fragment text (quoted, escaped) for a plain string value --
/// the shape `raw_scalar_kind`/`ColumnBuilder::append_row` expect for a
/// `Utf8`-kind cell.
#[cfg(feature = "python")]
fn quote_json_fragment(s: &str) -> CompactString {
    let escaped = escape_json_string(s);
    let mut buf = CompactString::with_capacity(escaped.len() + 2);
    buf.push('"');
    buf.push_str(&escaped);
    buf.push('"');
    buf
}

/// Wrap `array` as a 1-element-per-row `ListArray` -- every row gets a
/// present (never null) single-element list, whose one element carries
/// `array`'s own value/null for that row unchanged. Matches `flatten.rs`'s
/// confirmed `always_array_keys` semantics: a null cell wraps to `[null]`,
/// not to a null list (verified directly against `resolve_and_write`'s
/// `force_array` branch, which wraps whatever `write_value_ref` would have
/// written unwrapped -- including a literal `null` -- rather than omitting
/// the value).
#[cfg(feature = "python")]
fn wrap_as_single_element_list(array: ArrayRef, item_name: &str) -> ArrayRef {
    let len = array.len();
    let offsets = OffsetBuffer::new((0..=len as i32).collect::<Vec<i32>>().into());
    let field = Arc::new(Field::new(item_name, array.data_type().clone(), true));
    Arc::new(ListArray::new(field, offsets, array, None))
}

/// Concatenate a `PyChunkedArray`'s chunks into one contiguous `ArrayRef`
/// (a `RecordBatch` needs one array per column; a source `ChunkedArray` may
/// have several chunks, common after `pa.concat_tables`/certain polars
/// operations).
#[cfg(feature = "python")]
fn concat_chunks(chunked: &PyChunkedArray) -> PyResult<ArrayRef> {
    let chunks = chunked.chunks();
    match chunks.len() {
        0 => Ok(arrow_array::new_empty_array(chunked.data_type())),
        1 => Ok(chunks[0].clone()),
        _ => {
            let refs: Vec<&dyn Array> = chunks.iter().map(|c| c.as_ref()).collect();
            arrow_select::concat::concat(&refs).map_err(|e| {
                JsonToolsError::new_err(format!("Failed to concatenate column chunks: {e}"))
            })
        }
    }
}

/// Execute an already-eligible fast-path plan against Polars/PyArrow input,
/// building the output natively via the same Arrow builders `normalise()`'s
/// engine uses (`arrow_columnar`), then deriving the output DataFrame type
/// the same way `execute_normalise` derives its `target=` (output type
/// always matches `df_type` here -- this path has no `target=` of its own).
/// `string_values` is indexed by *source* column (matching `chunked_arrays`),
/// already extracted by `check_arrow_fastpath_eligibility` -- never
/// re-extracted here.
#[cfg(feature = "python")]
fn execute_arrow_fastpath(
    py: Python<'_>,
    df_type: DataFrameType,
    plan: FastPathPlan,
    chunked_arrays: Vec<PyChunkedArray>,
    string_values: Vec<Option<Vec<Option<CompactString>>>>,
    config: &ProcessingConfig,
) -> PyResult<Py<PyAny>> {
    let dates_enabled = config.type_conversion.dates.enabled;

    // The entire per-column build (extraction, per-cell transform, and Arrow
    // array construction) is pure Rust / arrow-rs -- it never touches a
    // `Bound<'py, PyAny>` or takes a `py` parameter (`concat_chunks` only
    // calls `.chunks()`/`.data_type()`; `ColumnBuilder`/`wrap_as_single_
    // element_list` are pure arrow-rs; `transform_string_cell` is pure
    // Rust). For a large DataFrame this can be tens of milliseconds of
    // computation, so release the GIL for it -- otherwise every other
    // Python thread in the process (a multi-threaded web server, a
    // ThreadPoolExecutor) stalls for no reason, matching every other
    // execution path in this file (see their own `py.detach()` calls).
    // `PyChunkedArray` is `Send` (it's a `#[pyclass(frozen)]` wrapping
    // `Vec<ArrayRef>`/`FieldRef`, both `Send + Sync` via arrow-rs; pyo3's
    // `#[pyclass]` macro requires `Send` to compile unless marked
    // `unsendable`, which it isn't).
    let (fields, arrays): (Vec<Field>, Vec<ArrayRef>) = py.detach(move || {
        let mut fields: Vec<Field> = Vec::with_capacity(plan.output_columns.len());
        let mut arrays: Vec<ArrayRef> = Vec::with_capacity(plan.output_columns.len());

        for (name, col_plan) in &plan.output_columns {
            match col_plan {
                FastPathColumn::PassThrough { source_col } => {
                    let arr = concat_chunks(&chunked_arrays[*source_col])?;
                    fields.push(Field::new(name, arr.data_type().clone(), true));
                    arrays.push(arr);
                }
                FastPathColumn::PassThroughWrapped { source_col } => {
                    let arr = concat_chunks(&chunked_arrays[*source_col])?;
                    let wrapped = wrap_as_single_element_list(arr, "item");
                    fields.push(Field::new(name, wrapped.data_type().clone(), true));
                    arrays.push(wrapped);
                }
                FastPathColumn::StringTransform { source_col, wrap } => {
                    let values = string_values[*source_col]
                        .as_ref()
                        .expect("string column always has extracted values by this point");

                    // Pass 1: transform every cell, accumulate this column's
                    // resolved kind (same bool > numeric > string priority as
                    // `build_normalise_table`), and track whether this key would
                    // ever actually appear in the old (JSON-text) path's output.
                    // A genuine source null keeps the key present (value null) --
                    // `remove_nulls`/`value_exclusions` are excluded from fast-
                    // path eligibility entirely (see eligibility check), so the
                    // only way a cell's key is *omitted* here is
                    // `remove_empty_strings` filtering a replaced value to "" (the
                    // one remaining early-return in `transform_string_cell`).
                    // If EVERY row omits the key this way, the old path never
                    // creates this column at all -- drop it here too, rather
                    // than emit an always-null column the old path never would.
                    let mut transformed: Vec<Option<CompactString>> =
                        Vec::with_capacity(values.len());
                    let mut flags = KindFlags::default();
                    let mut any_key_present = false;
                    for cell in values {
                        match cell {
                            None => {
                                any_key_present = true; // genuine null: key stays present
                                transformed.push(None);
                            }
                            Some(raw) => {
                                let out = transform_string_cell(raw, config);
                                if let Some(text) = &out {
                                    any_key_present = true;
                                    if let Some(k) = raw_scalar_kind(text, dates_enabled) {
                                        flags.merge(k);
                                    }
                                }
                                transformed.push(out);
                            }
                        }
                    }

                    if !any_key_present {
                        continue; // this key never appears in any row -- no column at all
                    }

                    let scalar_kind = flags.resolve();

                    // Pass 2: build the typed array from the transformed text.
                    let mut builder =
                        ColumnBuilder::new(ColumnPlan::Scalar(scalar_kind), transformed.len());
                    for cell in &transformed {
                        builder.append_row(cell.as_deref());
                    }
                    let arr = builder.finish();

                    if *wrap {
                        let wrapped = wrap_as_single_element_list(arr, "item");
                        fields.push(Field::new(name, wrapped.data_type().clone(), true));
                        arrays.push(wrapped);
                    } else {
                        fields.push(Field::new(name, arr.data_type().clone(), true));
                        arrays.push(arr);
                    }
                }
            }
        }

        Ok::<_, PyErr>((fields, arrays))
    })?;

    let schema = Arc::new(Schema::new(fields));
    let batch = RecordBatch::try_new(schema.clone(), arrays).map_err(|e| {
        JsonToolsError::new_err(format!("Failed to build fast-path record batch: {e}"))
    })?;
    let table = PyTable::try_new(vec![batch], schema).map_err(|e| {
        JsonToolsError::new_err(format!("Failed to build fast-path Arrow table: {e}"))
    })?;

    // Polars accepts the raw pyo3-arrow capsule object directly via
    // `pl.from_arrow` (verified in `build_normalise_table`'s own doc
    // comment) -- no need to materialize a genuine `pyarrow.Table` first.
    // PyArrow needs the genuine table itself, since that *is* the output.
    match df_type {
        DataFrameType::PyArrow => table.into_pyarrow(py).map(|b| b.unbind()),
        DataFrameType::Polars => {
            let raw = table.into_pyobject(py)?.into_any();
            reconstruct_polars_normalise(py, &raw)
        }
        _ => unreachable!("only called for Polars/PyArrow -- see caller"),
    }
}

// =============================================================================
// Flat-DataFrame fast path: pandas
// =============================================================================
//
// Pandas has no schema-level dtype-check-without-sampling equivalent to
// Arrow's (an `object`-dtype column can hold literally any Python type per
// cell), and no zero-copy column access -- `series_to_list`'s existing
// `.to_list()`/`.tolist()` pattern is the only extraction mechanism (boxes
// every value into a `PyObject`, same as it always has). More importantly,
// pandas' own `pd.DataFrame(list_of_dicts)` reconstruction (the *old* path)
// does NOT unify a mixed-type column to one type the way Arrow forces --
// confirmed directly: `pd.DataFrame([{"v":42},{"v":"abc"}])` keeps `42` as a
// real Python `int` and `"abc"` as a real `str` in the same `object`-dtype
// column, no stringification. So unlike the polars/pyarrow path above
// (which reuses `arrow_columnar`'s column-wide type-unification), pandas
// cells are converted *independently* -- each transformed value becomes its
// own native Python object (int/float/bool/str/None), matching exactly what
// `py_loads` on that same JSON fragment would produce.

/// Classify a pandas column's `dtype` string (`str(series.dtype)`) for
/// fast-path eligibility. `None` means disqualifying (datetime64/
/// Categorical/Timedelta/other extension dtypes -- see the module-level
/// "pandas re-encoding caveat": today's output for those comes from
/// pandas' own JSON encoder, e.g. epoch-millisecond ints for datetimes by
/// default, not the raw Python object, so a naive pass-through would
/// silently change output for them).
#[cfg(feature = "python")]
enum PandasColKind {
    NonString,
    String,
}

#[cfg(feature = "python")]
fn classify_pandas_dtype(dtype_str: &str) -> Option<PandasColKind> {
    match dtype_str {
        "int8" | "int16" | "int32" | "int64" | "uint8" | "uint16" | "uint32" | "uint64"
        | "Int8" | "Int16" | "Int32" | "Int64" | "UInt8" | "UInt16" | "UInt32" | "UInt64"
        | "float32" | "float64" | "Float32" | "Float64" | "bool" | "boolean" => {
            Some(PandasColKind::NonString)
        }
        "object" => Some(PandasColKind::String),
        _ => None,
    }
}

/// Extract an `object`-dtype pandas column's values as `Option<String>` per
/// cell -- `Ok(None)` (not an error) if any cell is neither `None`/`NaN` nor
/// a `str`, since that means this column genuinely holds mixed Python
/// objects (dicts, lists, numbers already mixed into an object column,
/// ...), not the plain-string-with-nulls shape this fast path handles.
#[cfg(feature = "python")]
fn extract_pandas_object_column(col: &Bound<'_, PyAny>) -> PyResult<Option<Vec<Option<String>>>> {
    let list = col.call_method0("tolist")?;
    let list = list.cast::<PyList>()?;
    let mut out = Vec::with_capacity(list.len());
    for item in list.iter() {
        if item.is_none() {
            out.push(None);
            continue;
        }
        if let Ok(s) = item.extract::<String>() {
            out.push(Some(s));
            continue;
        }
        // pandas represents a missing value in an object column as float
        // NaN as often as it does None -- both mean "null" here.
        if let Ok(f) = item.extract::<f64>() {
            if f.is_nan() {
                out.push(None);
                continue;
            }
        }
        return Ok(None); // some other Python type -- not eligible
    }
    Ok(Some(out))
}

/// Convert one JSON-fragment-text value (`transform_string_cell`'s output
/// shape: `null`/`true`/`false`/a bare number/a quoted-escaped string) into
/// its native Python equivalent -- exactly what `py_loads` on that same
/// fragment would produce, since that's the object pandas' own
/// `pd.DataFrame(list_of_dicts)` reconstruction would have ended up holding
/// for this cell in the old path.
#[cfg(feature = "python")]
fn json_fragment_to_pyobject(py: Python<'_>, text: &str) -> PyResult<Py<PyAny>> {
    match text.as_bytes().first() {
        Some(b'"') => {
            let inner = &text[1..text.len() - 1];
            let unescaped = unescape_json_string(inner);
            Ok(unescaped.into_pyobject(py)?.into_any().unbind())
        }
        Some(b't') => Ok(true.into_pyobject(py)?.to_owned().into_any().unbind()),
        Some(b'f') => Ok(false.into_pyobject(py)?.to_owned().into_any().unbind()),
        _ => {
            let is_float_syntax = text.bytes().any(|b| matches!(b, b'.' | b'e' | b'E'));
            if !is_float_syntax {
                if let Ok(i) = text.parse::<i64>() {
                    return Ok(i.into_pyobject(py)?.into_any().unbind());
                }
            }
            let f: f64 = text.parse().map_err(|_| {
                JsonToolsError::new_err(format!("Fast path produced invalid number text: {text}"))
            })?;
            Ok(f.into_pyobject(py)?.into_any().unbind())
        }
    }
}

/// One output column's pandas fast-path plan -- simpler than the Arrow
/// version's `FastPathColumn` since there's no column-wide type to resolve
/// (see module doc comment): a `PassThrough` column is reused as the exact
/// same `Series` object (renamed), and a `StringTransform` column becomes a
/// plain Python list of independently-typed values.
#[cfg(feature = "python")]
enum PandasFastPathColumn {
    PassThrough { source_col: usize },
    PassThroughWrapped { source_col: usize },
    StringTransform { source_col: usize, wrap: bool },
}

#[cfg(feature = "python")]
struct PandasFastPathPlan {
    output_columns: Vec<(String, PandasFastPathColumn)>,
}

/// Check whether `df` (pandas only) qualifies for the fast path under
/// `config`, mirroring `check_arrow_fastpath_eligibility`'s structure and
/// disqualification rules (see its doc comment for the shared reasoning:
/// whole-DataFrame decision, `remove_nulls`/`value_exclusions` excluded
/// entirely, rename-collision handling, `always_array_keys`). Returns
/// `Ok(None)` for any disqualifying reason -- the caller falls through to
/// the existing pipeline unchanged.
#[cfg(feature = "python")]
#[allow(clippy::type_complexity)]
fn check_pandas_fastpath_eligibility<'py>(
    df: &Bound<'py, PyAny>,
    config: &ProcessingConfig,
) -> PyResult<
    Option<(
        PandasFastPathPlan,
        Vec<Bound<'py, PyAny>>,
        Vec<Option<Vec<Option<String>>>>,
    )>,
> {
    if config.filtering.remove_nulls || config.replacements.has_value_exclusions() {
        return Ok(None);
    }

    let column_names: Vec<String> = df.getattr("columns")?.call_method0("tolist")?.extract()?;
    if column_names.is_empty() {
        return Ok(None);
    }
    let n_rows: usize = df.call_method0("__len__")?.extract()?;
    if n_rows == 0 {
        return Ok(None); // matches the Arrow path's same degenerate-case reasoning
    }

    let mut columns: Vec<Bound<'_, PyAny>> = Vec::with_capacity(column_names.len());
    let mut kinds: Vec<PandasColKind> = Vec::with_capacity(column_names.len());
    for name in &column_names {
        let col = df.get_item(name)?;
        let dtype_str: String = col.getattr("dtype")?.str()?.extract()?;
        let Some(kind) = classify_pandas_dtype(&dtype_str) else {
            return Ok(None);
        };
        kinds.push(kind);
        columns.push(col);
    }

    let mut string_values: Vec<Option<Vec<Option<String>>>> = vec![None; column_names.len()];
    for (i, kind) in kinds.iter().enumerate() {
        if !matches!(kind, PandasColKind::String) {
            continue;
        }
        let Some(values) = extract_pandas_object_column(&columns[i])? else {
            return Ok(None);
        };
        let sampled_json = values
            .iter()
            .flatten()
            .take(JSON_COLUMN_DETECTION_SAMPLE_SIZE)
            .any(|v| is_json_object_or_array_text(v));
        if sampled_json {
            return Ok(None);
        }
        string_values[i] = Some(values);
    }

    let has_key_exclusions = config.replacements.has_key_exclusions();
    let mut final_name_first_seen: IndexMap<String, usize> = IndexMap::new();
    let mut groups: Vec<Vec<usize>> = Vec::new();
    for (i, name) in column_names.iter().enumerate() {
        if has_key_exclusions && matches_any_pattern(name, &config.replacements.key_exclusions) {
            continue;
        }
        let mut final_name = name.clone();
        if let Some(replaced) =
            apply_replacement_patterns(name, &config.replacements.key_replacements)
        {
            final_name = replaced;
        }
        if config.lowercase_keys {
            final_name = final_name.to_lowercase();
        }
        match final_name_first_seen.get(&final_name) {
            Some(&slot) => groups[slot].push(i),
            None => {
                let slot = groups.len();
                final_name_first_seen.insert(final_name, slot);
                groups.push(vec![i]);
            }
        }
    }

    if groups.is_empty() {
        return Ok(None);
    }

    let has_collision_handling = config.collision.has_collision_handling();
    let has_always_array_keys = config.collision.has_always_array_keys();
    let mut output_columns = Vec::with_capacity(groups.len());
    for (final_name, &slot) in &final_name_first_seen {
        let sources = &groups[slot];
        let force_array = has_always_array_keys
            && config
                .collision
                .always_array_keys
                .iter()
                .any(|k| k == final_name);

        if sources.len() > 1 {
            if has_collision_handling || force_array {
                return Ok(None);
            }
            let source_col = *sources.last().expect("sources non-empty");
            output_columns.push((
                final_name.clone(),
                pandas_plan_for_column(source_col, force_array, &kinds[source_col]),
            ));
        } else {
            let source_col = sources[0];
            output_columns.push((
                final_name.clone(),
                pandas_plan_for_column(source_col, force_array, &kinds[source_col]),
            ));
        }
    }

    Ok(Some((
        PandasFastPathPlan { output_columns },
        columns,
        string_values,
    )))
}

#[cfg(feature = "python")]
fn pandas_plan_for_column(
    source_col: usize,
    force_array: bool,
    kind: &PandasColKind,
) -> PandasFastPathColumn {
    match (kind, force_array) {
        (PandasColKind::String, wrap) => PandasFastPathColumn::StringTransform { source_col, wrap },
        (PandasColKind::NonString, false) => PandasFastPathColumn::PassThrough { source_col },
        (PandasColKind::NonString, true) => PandasFastPathColumn::PassThroughWrapped { source_col },
    }
}

/// One pandas `StringTransform` cell's Pass-1 outcome. A cell can become
/// "empty" for two *different* reasons that the old (slow, JSON-text) path
/// reconstructs differently, and this distinguishes them rather than
/// collapsing both to a bare `None`: a genuine source null keeps the row's
/// dict key present with value `null`, which `pd.DataFrame(list_of_dicts)`
/// keeps as a real Python `None`; `remove_empty_strings` filtering a
/// replaced value to `""` instead makes the old path *omit the key from
/// that row's dict entirely*, and pandas fills a key missing from only some
/// rows with `NaN` (a `float`), not `None` -- confirmed directly against the
/// slow path (forced via a disqualifying column) rather than assumed.
#[cfg(feature = "python")]
enum PandasStringCell {
    Value(CompactString),
    Null,
    Omitted,
}

/// Pure-Rust Pass 1 for one pandas `StringTransform` column (see
/// [`execute_pandas_fastpath`]'s own doc comment for why this is split out).
#[cfg(feature = "python")]
fn transform_pandas_string_column(
    values: &[Option<String>],
    config: &ProcessingConfig,
) -> (Vec<PandasStringCell>, bool) {
    let mut transformed = Vec::with_capacity(values.len());
    let mut any_key_present = false;
    for cell in values {
        match cell {
            None => {
                any_key_present = true; // genuine null: key stays present
                transformed.push(PandasStringCell::Null);
            }
            Some(raw) => match transform_string_cell(raw, config) {
                None => transformed.push(PandasStringCell::Omitted),
                Some(text) => {
                    any_key_present = true;
                    transformed.push(PandasStringCell::Value(text));
                }
            },
        }
    }
    (transformed, any_key_present)
}

/// Execute an already-eligible pandas fast-path plan. `columns`/
/// `string_values` are indexed by *source* column position, already
/// extracted by `check_pandas_fastpath_eligibility` -- never re-extracted
/// here.
#[cfg(feature = "python")]
fn execute_pandas_fastpath(
    py: Python<'_>,
    plan: PandasFastPathPlan,
    columns: Vec<Bound<'_, PyAny>>,
    string_values: Vec<Option<Vec<Option<String>>>>,
    config: &ProcessingConfig,
) -> PyResult<Py<PyAny>> {
    // Pass 0: transform every StringTransform column's cells in one GIL
    // release -- pure Rust (`transform_string_cell`), never touches a
    // `Bound<PyAny>`. One `py.detach()` call for the whole function (not one
    // per column) avoids repeated release/reacquire round trips.
    // `PassThrough`/`PassThroughWrapped` inherently touch `Bound<'_, PyAny>`
    // (confirmed `Bound<'py, T>: !Send` -- it wraps a `Python<'py>` token,
    // which carries pyo3's explicit stable-Rust `!Send` marker) and so stay
    // GIL-held in the loop below, unchanged from before this split.
    let precomputed: Vec<Option<(Vec<PandasStringCell>, bool)>> = py.detach(|| {
        plan.output_columns
            .iter()
            .map(|(_, col_plan)| match col_plan {
                PandasFastPathColumn::StringTransform { source_col, .. } => {
                    let values = string_values[*source_col]
                        .as_ref()
                        .expect("string column always has extracted values by this point");
                    Some(transform_pandas_string_column(values, config))
                }
                _ => None,
            })
            .collect()
    });

    let out_dict = PyDict::new(py);

    for ((name, col_plan), precomputed) in plan.output_columns.iter().zip(&precomputed) {
        match col_plan {
            PandasFastPathColumn::PassThrough { source_col } => {
                // Reuse the exact same Series object -- no extraction, no
                // reconstruction, nulls/dtype preserved perfectly by
                // construction (nothing round-trips through JSON at all).
                out_dict.set_item(name, &columns[*source_col])?;
            }
            PandasFastPathColumn::PassThroughWrapped { source_col } => {
                let values = columns[*source_col].call_method0("tolist")?;
                let values = values.cast::<PyList>()?;
                let wrapped = PyList::empty(py);
                for v in values.iter() {
                    let one = PyList::new(py, [v])?;
                    wrapped.append(one)?;
                }
                out_dict.set_item(name, wrapped)?;
            }
            PandasFastPathColumn::StringTransform { wrap, .. } => {
                // Same "does this key ever actually appear" semantics as the
                // Arrow path (see its own doc comment for the full
                // reasoning) -- fully resolved by Pass 0 above.
                let (transformed, any_key_present) = precomputed
                    .as_ref()
                    .expect("StringTransform column always has a precomputed Pass-0 result");

                if !*any_key_present {
                    continue;
                }

                let out_list = PyList::empty(py);
                for cell in transformed {
                    let converted = match cell {
                        // Genuine source null: old path keeps the key
                        // present with a real `None`.
                        PandasStringCell::Null => py.None(),
                        // `remove_empty_strings` filtered this cell: old
                        // path omits the key from that row's dict entirely,
                        // and pandas fills a key missing from only some
                        // rows with `NaN` (a float), not `None`.
                        PandasStringCell::Omitted => {
                            f64::NAN.into_pyobject(py)?.into_any().unbind()
                        }
                        PandasStringCell::Value(text) => json_fragment_to_pyobject(py, text)?,
                    };
                    if *wrap {
                        let one = PyList::new(py, [converted])?;
                        out_list.append(one)?;
                    } else {
                        out_list.append(converted)?;
                    }
                }
                // Build an explicit dtype=object Series rather than handing
                // pandas a raw list: `pd.DataFrame(dict_of_lists)`'s own type
                // inference for a column mixing None/NaN/str was observed to
                // differ across pandas/numpy versions (a column with both a
                // genuine None and a float NaN got its None silently
                // coerced to NaN on some CI legs, not reproducible locally).
                // `dtype=object` is pandas' documented no-inference
                // construction path -- every element stays the exact Python
                // object it already is, no coercion possible.
                let pandas = cached_import(py, &PANDAS_MODULE, "pandas")?;
                let dtype_kwargs = PyDict::new(py);
                dtype_kwargs.set_item("dtype", "object")?;
                let series = pandas.call_method("Series", (out_list,), Some(&dtype_kwargs))?;
                out_dict.set_item(name, series)?;
            }
        }
    }

    let pandas = cached_import(py, &PANDAS_MODULE, "pandas")?;
    let df = pandas.call_method1("DataFrame", (out_dict,))?;
    Ok(df.unbind())
}

// =============================================================================
// PyJSONTools Helper Methods (DataFrame and Series Processing)
// =============================================================================

#[cfg(feature = "python")]
impl PyJSONTools {
    /// Process DataFrame through existing pipeline
    fn execute_dataframe(
        &self,
        df: &Bound<'_, PyAny>,
        df_type: DataFrameType,
    ) -> PyResult<Py<PyAny>> {
        let py = df.py();
        let is_flatten_mode = lock_config(&self.inner)?.is_flatten_mode();

        // Flat-DataFrame fast path (see its own module doc comment above):
        // pandas/Polars/PyArrow, `.flatten()` only. Eligibility is a
        // whole-DataFrame decision that never errors -- `Ok(None)` for any
        // disqualifying reason falls straight through to the existing,
        // unmodified pipeline below exactly as if this check didn't exist.
        if is_flatten_mode {
            match df_type {
                DataFrameType::Polars | DataFrameType::PyArrow => {
                    let config = ProcessingConfig::from_json_tools(&*lock_config(&self.inner)?);
                    if let Some((plan, chunked_arrays, string_values)) =
                        check_arrow_fastpath_eligibility(df, df_type, &config)?
                    {
                        return execute_arrow_fastpath(
                            py,
                            df_type,
                            plan,
                            chunked_arrays,
                            string_values,
                            &config,
                        );
                    }
                }
                DataFrameType::Pandas => {
                    let config = ProcessingConfig::from_json_tools(&*lock_config(&self.inner)?);
                    if let Some((plan, columns, string_values)) =
                        check_pandas_fastpath_eligibility(df, &config)?
                    {
                        return execute_pandas_fastpath(py, plan, columns, string_values, &config);
                    }
                }
                _ => {}
            }
        }

        // Step 1: Convert DataFrame directly to per-row JSON strings (native
        // to_json/write_ndjson where available -- see `dataframe_to_json_strings`'s
        // doc comment), then in flatten mode only, auto-expand any column
        // holding JSON *strings* (not already dicts/structs) the same way a
        // dict-typed column already expands (github.com/amaye15/
        // JSON-Tools-rs/issues/30), and finally un-nest every object-valued
        // top-level field (from either source) so its own keys become bare
        // columns instead of being prefixed by the source column's name (see
        // `unnest_object_valued_columns`'s doc comment). `.normal()`/
        // `.unflatten()` DataFrame processing is intentionally untouched by
        // any of this.
        //
        // For Polars/PyArrow input, `detect_and_extract_json_columns_zerocopy`
        // finds embedded-JSON-string columns directly via Arrow zero-copy
        // access and, if it finds any, takes a different route: those columns
        // are dropped before the native writer runs (avoiding the writer
        // having to escape their -- often large -- content at all) and
        // spliced back in from the zero-copy values afterward. See that
        // function's doc comment for the measured win and why this is
        // scoped to just those two DataFrame types.
        let json_strings = if is_flatten_mode {
            let rows = match detect_and_extract_json_columns_zerocopy(df, df_type)? {
                Some((target_cols, target_values, column_order)) if !target_cols.is_empty() => {
                    let df_reduced = dataframe_drop_columns(df, df_type, &target_cols)?;
                    let base_rows = dataframe_to_json_strings(&df_reduced, df_type)?;
                    splice_zerocopy_columns(
                        py,
                        base_rows,
                        &column_order,
                        &target_cols,
                        &target_values,
                    )?
                }
                Some(_) => {
                    // Polars/PyArrow input, but sampling found no embedded-JSON
                    // columns -- nothing to splice, use the plain path.
                    dataframe_to_json_strings(df, df_type)?
                }
                None => {
                    // pandas/PySpark/generic: not Arrow-backed by default, use
                    // the existing text-based detect-then-splice path.
                    let rows = dataframe_to_json_strings(df, df_type)?;
                    expand_json_string_columns(py, rows)?
                }
            };
            rows.into_iter()
                .map(|row| unnest_object_valued_columns(&row).unwrap_or(row))
                .collect()
        } else {
            dataframe_to_json_strings(df, df_type)?
        };

        // Step 2: Process through existing pipeline (releases GIL)
        let result = py
            .detach(|| {
                let mut guard = lock_config(&self.inner)?;
                let tools = mem::take(&mut *guard);
                let result = tools.execute(json_strings); // Batch processing
                *guard = tools;
                result
            })
            .map_err(|e| JsonToolsError::new_err(format!("Failed to process DataFrame: {}", e)))?;

        // Step 3: Reconstruct DataFrame from results
        match result {
            JsonOutput::Multiple(processed_list) => match df_type {
                // PySpark gets a genuine, schema-driven Spark DataFrame back --
                // reuses the exact machinery built for normalise(target="pyspark")
                // (github.com/amaye15/JSON-Tools-rs/issues/31) instead of the old
                // dict-list-then-fallback-to-list behavior.
                DataFrameType::PySpark => {
                    let spark = require_active_spark_session(py)?;
                    let dates_enabled = lock_config(&self.inner)?.date_conversion().enabled;
                    let (table, schema) =
                        build_normalise_table(py, &processed_list, true, dates_enabled)?;
                    reconstruct_pyspark_normalise(py, &spark, &table, &schema)
                }
                _ => {
                    // Convert JSON strings back to Python dicts
                    let mut processed_dicts: Vec<Py<PyAny>> =
                        Vec::with_capacity(processed_list.len());
                    for json_str in processed_list {
                        let py_dict = py_loads(py, &json_str).map_err(|e| {
                            JsonToolsError::new_err(format!("Failed to convert to Python: {}", e))
                        })?;
                        processed_dicts.push(py_dict.unbind());
                    }

                    // Reconstruct DataFrame (with fallback to list)
                    reconstruct_dataframe(py, df_type, processed_dicts)
                }
            },
            JsonOutput::Single(_) => Err(PyValueError::new_err(
                "Unexpected single result for DataFrame input",
            )),
        }
    }

    /// Process Series through existing list pipeline (REUSE existing code!)
    fn execute_series(
        &self,
        series: &Bound<'_, PyAny>,
        series_type: SeriesType,
    ) -> PyResult<Py<PyAny>> {
        let py = series.py();

        // Step 1: Convert Series to Python list
        let list = series_to_list(series, series_type)?;

        // Step 2: Process using EXISTING list handling code (copy from execute() method)
        let mut json_strings: Vec<String> = Vec::with_capacity(list.len());
        let mut is_str_flags: Vec<bool> = Vec::with_capacity(list.len());
        let mut has_other_types = false;

        for item in list.iter() {
            if let Ok(json_str) = item.extract::<String>() {
                json_strings.push(json_str);
                is_str_flags.push(true);
            } else if item.is_instance_of::<pyo3::types::PyDict>() {
                let json_str = py_dumps(py, &item).map_err(|e| {
                    JsonToolsError::new_err(format!("Failed to convert dict in series: {}", e))
                })?;
                json_strings.push(json_str);
                is_str_flags.push(false);
            } else {
                has_other_types = true;
                break;
            }
        }

        if has_other_types {
            return Err(PyValueError::new_err(
                "Series items must be either JSON strings or Python dictionaries",
            ));
        }

        // Step 3: Process through existing pipeline (releases GIL)
        let result = py
            .detach(|| {
                let mut guard = lock_config(&self.inner)?;
                let tools = mem::take(&mut *guard);
                let result = tools.execute(json_strings);
                *guard = tools;
                result
            })
            .map_err(|e| JsonToolsError::new_err(format!("Failed to process Series: {}", e)))?;

        // Step 4: Reconstruct Series from results
        match result {
            JsonOutput::Multiple(processed_list) => {
                // Type preservation: convert back to appropriate format
                let all_strings = is_str_flags.iter().all(|&b| b);
                let all_dicts = is_str_flags.iter().all(|&b| !b);

                let processed_items: Vec<Py<PyAny>> = if all_strings {
                    // All strings - convert to list of strings
                    processed_list
                        .into_iter()
                        .map(|s| {
                            s.into_pyobject(py)
                                .map(|o| o.into_any().unbind())
                                .map_err(|e| {
                                    JsonToolsError::new_err(format!(
                                        "Failed to convert string to Python object: {}",
                                        e
                                    ))
                                })
                        })
                        .collect::<PyResult<Vec<_>>>()?
                } else if all_dicts {
                    // All dicts - convert to list of dicts
                    let mut dict_results = Vec::with_capacity(processed_list.len());
                    for processed_json in processed_list {
                        let python_dict = py_loads(py, &processed_json).map_err(|e| {
                            JsonToolsError::new_err(format!(
                                "Failed to convert to Python dict: {}",
                                e
                            ))
                        })?;
                        dict_results.push(python_dict.unbind());
                    }
                    dict_results
                } else {
                    // Mixed results - convert each based on type
                    let mut mixed_results = Vec::with_capacity(processed_list.len());
                    for (processed_json, is_str) in processed_list.into_iter().zip(is_str_flags) {
                        if is_str {
                            mixed_results
                                .push(processed_json.into_pyobject(py)?.into_any().unbind());
                        } else {
                            let python_dict = py_loads(py, &processed_json).map_err(|e| {
                                JsonToolsError::new_err(format!(
                                    "Failed to convert to Python: {}",
                                    e
                                ))
                            })?;
                            mixed_results.push(python_dict.unbind());
                        }
                    }
                    mixed_results
                };

                // Reconstruct Series (with fallback to list)
                reconstruct_series(py, series_type, processed_items)
            }
            JsonOutput::Single(_) => Err(PyValueError::new_err(
                "Unexpected single result for Series input",
            )),
        }
    }

    /// Backing implementation for `execute(json_input, normalise=True, target=...)`.
    /// See the "Normalise" section above for the shared helpers this wires
    /// together.
    fn execute_normalise(
        &self,
        json_input: &Bound<'_, PyAny>,
        target: Option<String>,
    ) -> PyResult<Py<PyAny>> {
        let py = json_input.py();

        if !lock_config(&self.inner)?.is_flatten_mode() {
            return Err(JsonToolsError::new_err(
                "normalise=True requires .flatten() mode -- unflattened/nested JSON \
                 can't produce clean scalar columns for a wide DataFrame",
            ));
        }

        let requested_target = target.as_deref().map(NormaliseTarget::parse).transpose()?;

        let (json_strings, detected) = extract_normalise_json_strings(json_input)?;
        let resolved_target = resolve_normalise_target(py, detected, requested_target)?;

        // For pyspark, resolve the active session up front (before doing any
        // processing work) so a missing session fails fast with a clear error.
        let spark_session = if resolved_target == NormaliseTarget::PySpark {
            Some(require_active_spark_session(py)?)
        } else {
            require_importable(py, resolved_target)?;
            None
        };

        // Process through the Rust engine (releases GIL) -- same mem::take/restore
        // idiom `execute_dataframe`/`execute_series` above use to avoid cloning.
        let result = py
            .detach(|| {
                let mut guard = lock_config(&self.inner)?;
                let tools = mem::take(&mut *guard);
                let result = tools.execute(json_strings);
                *guard = tools;
                result
            })
            .map_err(|e| JsonToolsError::new_err(format!("Failed to process JSON: {}", e)))?;

        let processed_list = match result {
            JsonOutput::Multiple(processed_list) => processed_list,
            JsonOutput::Single(single) => vec![single],
        };

        // Only `target="polars"` can skip pyarrow entirely (verified directly
        // -- see `build_normalise_table`'s `via_pyarrow` doc comment); every
        // other target needs a genuine `pyarrow.Table` regardless.
        let via_pyarrow = resolved_target != NormaliseTarget::Polars;
        let dates_enabled = lock_config(&self.inner)?.date_conversion().enabled;
        let (table, schema) =
            build_normalise_table(py, &processed_list, via_pyarrow, dates_enabled)?;

        match resolved_target {
            // `build_normalise_table` already produced the canonical pyarrow.Table
            // -- nothing further to derive.
            NormaliseTarget::PyArrow => Ok(table.unbind()),
            NormaliseTarget::Pandas => reconstruct_pandas_normalise(py, &table),
            NormaliseTarget::Polars => reconstruct_polars_normalise(py, &table),
            NormaliseTarget::PySpark => {
                let spark = spark_session.expect("resolved to PySpark target above");
                reconstruct_pyspark_normalise(py, &spark, &table, &schema)
            }
        }
    }
}

/// Python module definition
#[cfg(feature = "python")]
#[pymodule]
fn json_tools_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add the unified JSONTools class
    m.add_class::<PyJSONTools>()?;

    // Add the JsonOutput class for results
    m.add_class::<PyJsonOutput>()?;

    // Add the custom exception
    m.add("JsonToolsError", m.py().get_type::<JsonToolsError>())?;

    // Add module metadata
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__author__", "JSON Tools RS Contributors")?;
    m.add(
        "__description__",
        "Python bindings for JSON Tools RS - Unified JSON manipulation library with advanced collision handling and filtering",
    )?;

    Ok(())
}

#[cfg(all(test, feature = "python"))]
mod marshal_tests {
    use super::may_contain_big_int;

    /// Straightforward reference implementation: full scan for a digit run
    /// of >= 19. The sampled version must agree with this everywhere.
    fn naive(s: &[u8]) -> bool {
        let mut run = 0usize;
        for &b in s {
            if b.is_ascii_digit() {
                run += 1;
                if run >= 19 {
                    return true;
                }
            } else {
                run = 0;
            }
        }
        false
    }

    #[test]
    fn big_int_guard_edges() {
        assert!(!may_contain_big_int(b""));
        assert!(!may_contain_big_int(b"{}"));
        // 18 digits: largest run that must NOT trigger
        assert!(!may_contain_big_int(b"123456789012345678"));
        // 19 digits: must trigger, at string start, middle, and end
        assert!(may_contain_big_int(b"1234567890123456789"));
        assert!(may_contain_big_int(b"{\"big\": 1234567890123456789}"));
        assert!(may_contain_big_int(
            b"xxxxxxxxxxxxxxxxxxxxx1234567890123456789"
        ));
        // i64::MAX itself (19 digits) is conservatively flagged -- fine
        assert!(may_contain_big_int(b"9223372036854775807"));
        // runs split by separators never combine
        assert!(!may_contain_big_int(b"123456789.123456789e12"));
        // long digit runs inside strings count too (conservative by design)
        assert!(may_contain_big_int(b"{\"id\": \"12345678901234567890\"}"));
    }

    #[test]
    fn big_int_guard_matches_naive_scan() {
        // Deterministic xorshift; digit-heavy alphabet so long runs actually
        // occur, exercising run expansion straddling sample points.
        let mut state = 0x9e3779b97f4a7c15u64;
        let mut next = move || {
            state ^= state << 13;
            state ^= state >> 7;
            state ^= state << 17;
            state
        };
        for len in [0usize, 1, 17, 18, 19, 20, 37, 38, 57, 200, 1000] {
            for _ in 0..500 {
                let bytes: Vec<u8> = (0..len)
                    .map(|_| match next() % 4 {
                        0 => b'a',
                        1 => b',',
                        _ => b'0' + (next() % 10) as u8,
                    })
                    .collect();
                assert_eq!(
                    may_contain_big_int(&bytes),
                    naive(&bytes),
                    "mismatch on {:?}",
                    String::from_utf8_lossy(&bytes)
                );
            }
        }
    }
}

#[cfg(all(test, feature = "python"))]
mod arrow_normalise_tests {
    use crate::arrow_columnar::{raw_scalar_kind, stringify_raw, KindFlags, ScalarKind};
    use arrow_array::builder::{Float64Builder, Int64Builder, ListBuilder, StringBuilder};
    use arrow_array::{Array, BooleanArray, Float64Array, Int64Array, StringArray};

    // -------------------------------------------------------------------
    // raw_scalar_kind / KindFlags::resolve -- pure classification logic,
    // no Python interpreter needed (this crate's `pyo3` dependency uses the
    // "extension-module" feature, which disables auto-initialization, so
    // `cargo test --features python` has no embedded interpreter to run
    // Python-calling code against -- consistent with `marshal_tests` above
    // only testing the Python-free `may_contain_big_int`).
    // -------------------------------------------------------------------

    #[test]
    fn raw_scalar_kind_classifies_every_shape() {
        assert!(raw_scalar_kind("null", false).is_none());
        assert!(raw_scalar_kind("true", false).unwrap().bool_);
        assert!(raw_scalar_kind("false", false).unwrap().bool_);
        assert!(raw_scalar_kind("\"hi\"", false).unwrap().str_);
        assert!(raw_scalar_kind("123", false).unwrap().int_);
        assert!(raw_scalar_kind("-42", false).unwrap().int_);
        assert!(raw_scalar_kind("1.5", false).unwrap().float_);
        assert!(raw_scalar_kind("1e10", false).unwrap().float_);
        assert!(raw_scalar_kind("1E10", false).unwrap().float_);
        // Integer too large for i64 -- downgrades to float, not an error.
        assert!(
            raw_scalar_kind("99999999999999999999", false)
                .unwrap()
                .float_
        );
        // i64::MAX itself still fits.
        assert!(raw_scalar_kind("9223372036854775807", false).unwrap().int_);
        // A literal empty object (remove_empty_objects=False) -- str_,
        // stringified to its own "{}" text, not a number-parse panic.
        assert!(raw_scalar_kind("{}", false).unwrap().str_);
    }

    #[test]
    fn raw_scalar_kind_dates_gated_on_dates_enabled() {
        // dates_enabled=false: a date-shaped string is just an ordinary string,
        // never independently pattern-matched -- the whole point of gating this
        // on the caller's own opt-in convert_dates()/auto_convert_types().
        assert!(raw_scalar_kind("\"2024-01-15\"", false).unwrap().str_);
        assert!(
            raw_scalar_kind("\"2024-01-15T10:30:00Z\"", false)
                .unwrap()
                .str_
        );

        // dates_enabled=true: recognized as date/datetime.
        assert!(raw_scalar_kind("\"2024-01-15\"", true).unwrap().date_);
        assert!(
            raw_scalar_kind("\"2024-01-15T10:30:00Z\"", true)
                .unwrap()
                .datetime_
        );
        assert!(
            raw_scalar_kind("\"2024-01-15T10:30:00+05:00\"", true)
                .unwrap()
                .datetime_
        );
        // An ordinary string that merely starts with digits stays a string --
        // a real chrono parse, not a shape heuristic that could false-positive.
        assert!(
            raw_scalar_kind("\"2024-01-15-extra-text\"", true)
                .unwrap()
                .str_
        );
        assert!(raw_scalar_kind("\"not a date\"", true).unwrap().str_);
        assert!(raw_scalar_kind("\"hi\"", true).unwrap().str_);
    }

    #[test]
    fn kind_flags_resolve_priority() {
        let bool_only = KindFlags {
            bool_: true,
            ..Default::default()
        };
        assert_eq!(bool_only.resolve(), ScalarKind::Bool);

        let int_only = KindFlags {
            int_: true,
            ..Default::default()
        };
        assert_eq!(int_only.resolve(), ScalarKind::Int64);

        let float_only = KindFlags {
            float_: true,
            ..Default::default()
        };
        assert_eq!(float_only.resolve(), ScalarKind::Float64);

        // int + float mix -> promotes to Float64, not a "mixed kind" stringify.
        let int_float = KindFlags {
            int_: true,
            float_: true,
            ..Default::default()
        };
        assert_eq!(int_float.resolve(), ScalarKind::Float64);

        let str_only = KindFlags {
            str_: true,
            ..Default::default()
        };
        assert_eq!(str_only.resolve(), ScalarKind::Utf8);

        // Nothing seen at all (all-null column) -> Utf8 default.
        assert_eq!(KindFlags::default().resolve(), ScalarKind::Utf8);

        // Any real mix beyond int/float alone -> stringify fallback.
        let bool_numeric = KindFlags {
            bool_: true,
            int_: true,
            ..Default::default()
        };
        assert_eq!(bool_numeric.resolve(), ScalarKind::Utf8);

        let bool_str = KindFlags {
            bool_: true,
            str_: true,
            ..Default::default()
        };
        assert_eq!(bool_str.resolve(), ScalarKind::Utf8);

        let numeric_str = KindFlags {
            int_: true,
            str_: true,
            ..Default::default()
        };
        assert_eq!(numeric_str.resolve(), ScalarKind::Utf8);

        let date_only = KindFlags {
            date_: true,
            ..Default::default()
        };
        assert_eq!(date_only.resolve(), ScalarKind::Date32);

        let datetime_only = KindFlags {
            datetime_: true,
            ..Default::default()
        };
        assert_eq!(datetime_only.resolve(), ScalarKind::TimestampUtcMicros);

        // date + datetime mix -> promotes to TimestampUtcMicros (a bare date
        // becomes midnight UTC), the same "promote the narrower kind" pattern
        // int->float already uses -- not a stringify fallback.
        let date_datetime = KindFlags {
            date_: true,
            datetime_: true,
            ..Default::default()
        };
        assert_eq!(date_datetime.resolve(), ScalarKind::TimestampUtcMicros);

        // temporal mixed with any other real kind -> stringify fallback, same
        // as any other kind mixing.
        let date_str = KindFlags {
            date_: true,
            str_: true,
            ..Default::default()
        };
        assert_eq!(date_str.resolve(), ScalarKind::Utf8);

        let date_numeric = KindFlags {
            date_: true,
            int_: true,
            ..Default::default()
        };
        assert_eq!(date_numeric.resolve(), ScalarKind::Utf8);

        let date_bool = KindFlags {
            date_: true,
            bool_: true,
            ..Default::default()
        };
        assert_eq!(date_bool.resolve(), ScalarKind::Utf8);
    }

    #[test]
    fn kind_flags_merge_is_union() {
        let mut flags = KindFlags::default();
        flags.merge(KindFlags {
            int_: true,
            ..Default::default()
        });
        flags.merge(KindFlags {
            float_: true,
            ..Default::default()
        });
        assert!(flags.int_ && flags.float_ && !flags.bool_ && !flags.str_);
    }

    // -------------------------------------------------------------------
    // stringify_raw -- the mixed-kind fallback's Python str()-equivalent
    // conversion.
    // -------------------------------------------------------------------

    #[test]
    fn stringify_raw_matches_python_str_semantics() {
        assert_eq!(stringify_raw("\"hello\""), "hello");
        assert_eq!(stringify_raw("\"with \\\"quotes\\\"\""), "with \"quotes\"");
        assert_eq!(stringify_raw("true"), "True");
        assert_eq!(stringify_raw("false"), "False");
        assert_eq!(stringify_raw("123"), "123");
        assert_eq!(stringify_raw("1.5"), "1.5");
    }

    // -------------------------------------------------------------------
    // ColumnBuilder / append_list_row -- these build real `arrow_array`
    // types directly and never touch a Python object, so they're testable
    // without a live interpreter too.
    // -------------------------------------------------------------------

    #[test]
    fn scalar_int_column_builds_correctly_with_nulls() {
        let mut b = Int64Builder::new();
        b.append_value(1);
        b.append_null();
        b.append_value(3);
        let arr: Int64Array = b.finish();
        assert_eq!(arr.len(), 3);
        assert_eq!(arr.value(0), 1);
        assert!(arr.is_null(1));
        assert_eq!(arr.value(2), 3);
    }

    #[test]
    fn scalar_bool_column_builds_correctly() {
        use arrow_array::builder::BooleanBuilder;
        let mut b = BooleanBuilder::new();
        b.append_value(true);
        b.append_value(false);
        b.append_null();
        let arr: BooleanArray = b.finish();
        assert_eq!(arr.len(), 3);
        assert!(arr.value(0));
        assert!(!arr.value(1));
        assert!(arr.is_null(2));
    }

    #[test]
    fn scalar_float_column_promotes_int_and_float_uniformly() {
        // Mirrors what ColumnBuilder::Float64's append_row does for a
        // column resolved to Float64 (int/float mix): every value, whether
        // its source text was int- or float-formatted, parses as f64.
        let mut b = Float64Builder::new();
        for text in ["5", "5.5", "-3"] {
            b.append_value(text.parse::<f64>().unwrap());
        }
        let arr: Float64Array = b.finish();
        assert_eq!(arr.values(), &[5.0, 5.5, -3.0]);
    }

    #[test]
    fn homogeneous_string_list_builds_correctly() {
        let mut b = ListBuilder::new(StringBuilder::new());
        b.values().append_value("a");
        b.values().append_value("b");
        b.append(true); // ["a", "b"]
        b.append(true); // [] (empty but present)
        b.append(false); // null
        b.values().append_value("z");
        b.append(true); // ["z"]
        let arr = b.finish();

        assert_eq!(arr.len(), 4);
        assert!(!arr.is_null(0));
        assert_eq!(arr.value(0).len(), 2);
        assert!(!arr.is_null(1));
        assert_eq!(arr.value(1).len(), 0); // empty, not null
        assert!(arr.is_null(2));
        assert_eq!(arr.value(3).len(), 1);

        let first_cell = arr.value(0);
        let inner: &StringArray = first_cell.as_any().downcast_ref().unwrap();
        assert_eq!(inner.value(0), "a");
        assert_eq!(inner.value(1), "b");
    }

    #[test]
    fn scalar_cell_wraps_into_single_element_list() {
        // Mirrors handle_key_collision(True): a row where no collision
        // occurred contributes a scalar value that must wrap into a
        // single-element list to keep the column uniformly List<T>.
        let mut b = ListBuilder::new(StringBuilder::new());
        // Simulates append_list_row's "_ => wrap scalar" branch.
        b.values().append_value("solo");
        b.append(true);
        let arr = b.finish();
        assert_eq!(arr.len(), 1);
        let first_cell = arr.value(0);
        let inner: &StringArray = first_cell.as_any().downcast_ref().unwrap();
        assert_eq!(inner.len(), 1);
        assert_eq!(inner.value(0), "solo");
    }
}
