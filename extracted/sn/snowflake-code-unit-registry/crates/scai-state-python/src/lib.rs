//! Python bindings for SCAI state management
//!
//! This crate provides Python bindings using the generated Rust types
//! from the JSON schema. Data crosses the FFI boundary as native Python
//! objects (dicts/lists) using the `pythonize` crate for direct
//! serde ↔ Python conversion – no JSON string intermediary.

use pyo3::create_exception;
use pyo3::prelude::*;
use pythonize::{depythonize, pythonize};
use scai_log::ScaiLogger as CoreScaiLogger;
use scai_state_core::{
    ChecksumMode, CodeUnit, CodeUnitRegistry as RustRegistry, FindOptions, WriteOptions,
};
use serde::Deserialize;
use std::collections::HashMap;

// Custom exception with error_code attribute
create_exception!(scai_state, ScaiError, pyo3::exceptions::PyException);

/// Convert a core error into a Python ScaiError with error_code and info.
fn to_py_error(py: Python<'_>, e: scai_state_core::Error) -> PyErr {
    let info = e.info();
    let code = info.code;
    let message = info.message.clone();
    let err = PyErr::new::<ScaiError, _>(message);
    let _ = err.value(py).setattr("error_code", code);
    if let Ok(info_dict) = pythonize(py, &info) {
        let _ = err.value(py).setattr("info", info_dict);
    }
    err
}

/// Parse a checksum_mode string into a core `ChecksumMode`.
/// Maps binding-layer parse errors to PyValueError so callers get a clear message.
fn parse_checksum(py: Python<'_>, s: &str) -> PyResult<ChecksumMode> {
    s.parse::<ChecksumMode>().map_err(|e| to_py_error(py, e))
}

/// Intermediate struct for deserializing Python-side `WriteOptions`.
#[derive(Debug, Default, serde::Deserialize)]
#[serde(default)]
struct PyWriteOptions {
    checksum_mode: Option<String>,
}

fn parse_write_options(
    py: Python<'_>,
    opts: Option<&Bound<'_, PyAny>>,
) -> PyResult<Option<WriteOptions>> {
    let obj = match opts {
        None => return Ok(None),
        Some(o) => o,
    };
    let input: PyWriteOptions = depythonize(obj)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
    match input.checksum_mode {
        None => Ok(None),
        Some(s) => {
            let mode = parse_checksum(py, &s)?;
            Ok(Some(WriteOptions {
                checksum_mode: mode,
            }))
        }
    }
}

/// Python-side payload for `find_all` options.
#[derive(Debug, Default, Deserialize)]
#[serde(default)]
struct PyFindOptions {
    filter: Option<String>,
    fields: Option<Vec<String>>,
    include_dependencies: bool,
    bindings: Option<HashMap<String, String>>,
    /// Path to a `database-bindings.yml`. The read resolves it and returns bound
    /// units, so the caller passes a path rather than parsing the YAML and
    /// building the token map itself. Mutually exclusive with `bindings`.
    bindings_path: Option<String>,
}

/// Python wrapper for CodeUnitRegistry
#[pyclass]
pub struct CodeUnitRegistry {
    inner: RustRegistry,
}

#[pymethods]
impl CodeUnitRegistry {
    /// Initialize a new registry at the given path
    #[staticmethod]
    fn exists(path: &str) -> bool {
        RustRegistry::exists(path)
    }

    #[staticmethod]
    fn init(py: Python<'_>, path: &str) -> PyResult<Self> {
        let inner = RustRegistry::init(path).map_err(|e| to_py_error(py, e))?;
        Ok(Self { inner })
    }

    /// Open an existing registry at the given path
    #[staticmethod]
    fn open(py: Python<'_>, path: &str) -> PyResult<Self> {
        let inner = RustRegistry::open(path).map_err(|e| to_py_error(py, e))?;
        Ok(Self { inner })
    }

    // ── Create ───────────────────────────────────────────────────────────

    /// Create a new code unit on disk. Returns the ID.
    #[pyo3(signature = (code_unit, options=None))]
    fn create(
        &self,
        py: Python<'_>,
        code_unit: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<String> {
        let mut cu: CodeUnit = depythonize(&code_unit)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let opts = parse_write_options(py, options.as_ref())?;
        self.inner
            .create(&mut cu, opts.as_ref())
            .map_err(|e| to_py_error(py, e))
    }

    /// Batch create multiple code units efficiently.
    /// Returns a dict: {"succeeded": [id, ...], "failed": [{"id": ..., "error": {...}}, ...], "sideEffectIds": [...]}
    #[pyo3(signature = (batch, options=None))]
    fn create_batch(
        &self,
        py: Python<'_>,
        batch: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<Py<PyAny>> {
        let mut batch: Vec<CodeUnit> = depythonize(&batch)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let opts = parse_write_options(py, options.as_ref())?;
        let result = self
            .inner
            .create_batch(&mut batch, opts.as_ref())
            .map_err(|e| to_py_error(py, e))?;
        batch_result_to_py(py, &result)
    }

    // ── Load / List ──────────────────────────────────────────────────────

    /// Load a code unit by ID. Returns CodeUnit as a Python dict.
    /// Get a code unit by ID. Returns a Python dict.
    #[pyo3(name = "get_by_id", signature = (id, include=None))]
    fn get_by_id(
        &self,
        py: Python<'_>,
        id: &str,
        include: Option<Vec<String>>,
    ) -> PyResult<Py<PyAny>> {
        let include_refs: Option<Vec<&str>> = include
            .as_ref()
            .map(|v| v.iter().map(|s| s.as_str()).collect());
        let doc = self
            .inner
            .get_by_id(id, include_refs.as_deref())
            .map_err(|e| to_py_error(py, e))?;
        pythonize(py, &doc)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    /// Find all code units using a single options object.
    /// Returns a Python list of dicts.
    #[pyo3(name = "find_all", signature = (options=None))]
    fn find_all(&self, py: Python<'_>, options: Option<Bound<'_, PyAny>>) -> PyResult<Py<PyAny>> {
        let options = match options {
            Some(options) => depythonize::<PyFindOptions>(&options)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?,
            None => PyFindOptions::default(),
        };

        let include_refs: Option<Vec<&str>> = options
            .fields
            .as_ref()
            .map(|v| v.iter().map(|s| s.as_str()).collect());
        // `Option<String>` -> `Option<&Path>` needs an owned intermediate that outlives
        // the `FindOptions`, same shape as the fields projection above.
        let bindings_path_ref: Option<std::path::PathBuf> =
            options.bindings_path.as_ref().map(std::path::PathBuf::from);
        let docs = self
            .inner
            .find_all(FindOptions {
                filter: options.filter.as_deref(),
                fields: include_refs.as_deref(),
                include_dependencies: options.include_dependencies,
                bindings: options.bindings.as_ref(),
                bindings_path: bindings_path_ref.as_deref(),
            })
            .map_err(|e| to_py_error(py, e))?;
        pythonize(py, &docs)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    /// Find code units matching all fields present in a partial code unit object.
    /// Returns a Python list of dicts.
    #[pyo3(name = "find_by_object", signature = (partial, include=None))]
    fn find_by_object(
        &self,
        py: Python<'_>,
        partial: Bound<'_, PyAny>,
        include: Option<Vec<String>>,
    ) -> PyResult<Py<PyAny>> {
        let partial_value: serde_json::Value = depythonize(&partial)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let include_refs: Option<Vec<&str>> = include
            .as_ref()
            .map(|v| v.iter().map(|s| s.as_str()).collect());
        let docs = self
            .inner
            .find_by_object(&partial_value, include_refs.as_deref())
            .map_err(|e| to_py_error(py, e))?;
        pythonize(py, &docs)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    // ── Update (PATCH) ───────────────────────────────────────────────────

    /// Update specific fields in a code unit by dot-notation paths.
    #[pyo3(signature = (id, updates, options=None))]
    fn update(
        &self,
        py: Python<'_>,
        id: &str,
        updates: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<()> {
        let updates_map: serde_json::Map<String, serde_json::Value> = depythonize(&updates)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let updates_vec: Vec<(&str, serde_json::Value)> = updates_map
            .iter()
            .map(|(k, v)| (k.as_str(), v.clone()))
            .collect();
        let opts = parse_write_options(py, options.as_ref())?;
        self.inner
            .update(id, &updates_vec, opts.as_ref())
            .map_err(|e| to_py_error(py, e))
    }

    /// Update all code units matching a filter with the same updates.
    #[pyo3(signature = (filter, updates, options=None))]
    fn update_where(
        &self,
        py: Python<'_>,
        filter: &str,
        updates: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<Py<PyAny>> {
        let updates_map: serde_json::Map<String, serde_json::Value> = depythonize(&updates)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let updates_vec: Vec<(&str, serde_json::Value)> = updates_map
            .iter()
            .map(|(k, v)| (k.as_str(), v.clone()))
            .collect();
        let opts = parse_write_options(py, options.as_ref())?;
        let result = self
            .inner
            .update_where(filter, &updates_vec, opts.as_ref())
            .map_err(|e| to_py_error(py, e))?;
        batch_result_to_py(py, &result)
    }

    /// Batch update multiple code units efficiently.
    #[pyo3(signature = (batch, options=None))]
    fn update_batch(
        &self,
        py: Python<'_>,
        batch: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<Py<PyAny>> {
        let batch_raw: Vec<(String, serde_json::Map<String, serde_json::Value>)> =
            depythonize(&batch)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let batch_vec: Vec<(&str, Vec<(&str, serde_json::Value)>)> = batch_raw
            .iter()
            .map(|(id, updates_map)| {
                let updates: Vec<(&str, serde_json::Value)> = updates_map
                    .iter()
                    .map(|(k, v)| (k.as_str(), v.clone()))
                    .collect();
                (id.as_str(), updates)
            })
            .collect();
        let opts = parse_write_options(py, options.as_ref())?;
        let result = self
            .inner
            .update_batch(&batch_vec, opts.as_ref())
            .map_err(|e| to_py_error(py, e))?;
        batch_result_to_py(py, &result)
    }

    // ── Upsert (merge) ──────────────────────────────────────────────────

    /// Create-or-merge a single code unit. Returns the ID.
    #[pyo3(signature = (code_unit, options=None))]
    fn upsert(
        &self,
        py: Python<'_>,
        code_unit: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<String> {
        let mut cu: CodeUnit = depythonize(&code_unit)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let opts = parse_write_options(py, options.as_ref())?;
        self.inner
            .upsert(&mut cu, opts.as_ref())
            .map_err(|e| to_py_error(py, e))
    }

    /// Batch upsert multiple code units.
    #[pyo3(signature = (batch, options=None))]
    fn upsert_batch(
        &self,
        py: Python<'_>,
        batch: Bound<'_, PyAny>,
        options: Option<Bound<'_, PyAny>>,
    ) -> PyResult<Py<PyAny>> {
        let mut batch: Vec<CodeUnit> = depythonize(&batch)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        let opts = parse_write_options(py, options.as_ref())?;
        let result = self
            .inner
            .upsert_batch(&mut batch, opts.as_ref())
            .map_err(|e| to_py_error(py, e))?;
        batch_result_to_py(py, &result)
    }

    /// Recompute checksums for selected file entries on an existing code unit.
    /// `checksum_mode`: "none" | "source" | "converted" | "snapshot" | "all"
    fn update_checksum(&self, py: Python<'_>, id: &str, checksum_mode: &str) -> PyResult<()> {
        let mode = parse_checksum(py, checksum_mode)?;
        self.inner
            .update_checksum(id, mode)
            .map_err(|e| to_py_error(py, e))
    }

    /// Validate checksums for an existing code unit.
    fn validate_checksum(
        &self,
        py: Python<'_>,
        id: &str,
        checksum_mode: &str,
    ) -> PyResult<Py<PyAny>> {
        let checksum = parse_checksum(py, checksum_mode)?;
        let report = self
            .inner
            .validate_checksum(id, checksum)
            .map_err(|e| to_py_error(py, e))?;
        pythonize(py, &report)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    // ── Validation ────────────────────────────────────────────────────────

    /// Validate all code units in the registry.
    #[pyo3(signature = (checksum_mode="all"))]
    fn validate(&self, py: Python<'_>, checksum_mode: &str) -> PyResult<Py<PyAny>> {
        let mode = parse_checksum(py, checksum_mode)?;
        let report = self.inner.validate(mode).map_err(|e| to_py_error(py, e))?;
        pythonize(py, &report)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    /// Validate a single code unit by ID.
    #[pyo3(signature = (id, checksum_mode="all"))]
    fn validate_unit(&self, py: Python<'_>, id: &str, checksum_mode: &str) -> PyResult<Py<PyAny>> {
        let mode = parse_checksum(py, checksum_mode)?;
        let report = self
            .inner
            .validate_unit(id, mode)
            .map_err(|e| to_py_error(py, e))?;
        pythonize(py, &report)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    // ── Change detection ─────────────────────────────────────────────────

    /// Detect source-code changes (modified, removed, untracked files).
    #[pyo3(signature = (checksum_mode="all", filter=None))]
    fn find_sql_file_changes(
        &self,
        py: Python<'_>,
        checksum_mode: &str,
        filter: Option<&str>,
    ) -> PyResult<Py<PyAny>> {
        let mode = parse_checksum(py, checksum_mode)?;
        let changes = self
            .inner
            .find_sql_file_changes(mode, filter)
            .map_err(|e| to_py_error(py, e))?;
        pythonize(py, &changes)
            .map(|b| b.unbind())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    // ── Delete ───────────────────────────────────────────────────────────

    /// Delete a code unit by ID.
    fn delete(&self, py: Python<'_>, id: &str) -> PyResult<()> {
        self.inner.delete(id).map_err(|e| to_py_error(py, e))
    }

    // ── Refresh ─────────────────────────────────────────────────────────

    /// Recompute dependency-derived fields across the entire registry.
    /// Uses strict cycle detection: raises ScaiError with error_code 1014 on cycles.
    fn refresh_dependencies(&self, py: Python<'_>) -> PyResult<()> {
        self.inner
            .refresh_dependencies()
            .map_err(|e| to_py_error(py, e))
    }

    // ── Migration ─────────────────────────────────────────────────────

    /// Migrate all registry documents to the current schema version.
    ///
    /// Best-effort: per-file failures are returned in `BatchResult.failed`.
    /// Raises only on batch-level failures; partial progress may have occurred.
    fn migrate_schema_all(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        let result = self
            .inner
            .migrate_schema_all()
            .map_err(|e| to_py_error(py, e))?;
        batch_result_to_py(py, &result)
    }
}

/// Generate a new code unit ID (32-character UUID v4).
#[pyfunction]
fn generate_id() -> String {
    scai_state_core::generate_id()
}

/// Hash a file with xxHash3-128 and return the 32-character lowercase hex digest.
///
/// The path must be absolute. File-not-found raises ScaiError (code 1023, FileIoError).
#[pyfunction]
fn compute_file_checksum(py: Python<'_>, path: &str) -> PyResult<String> {
    scai_state_core::compute_file_checksum(path).map_err(|e| to_py_error(py, e))
}

/// Returns a list of [name, code] pairs for every error variant.
///
/// Used by the Python contract test to verify the `ErrorCode` IntEnum
/// stays in sync with the Rust `Error` enum.
#[pyfunction]
fn list_error_codes(py: Python<'_>) -> PyResult<Py<PyAny>> {
    let codes = scai_state_core::Error::all_codes();
    let pairs: Vec<(String, i32)> = codes
        .into_iter()
        .map(|(name, code)| (name.to_string(), code))
        .collect();
    pythonize(py, &pairs)
        .map(|b| b.unbind())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

/// Return the current schema version supported by this library.
#[pyfunction]
fn current_schema_version() -> i32 {
    scai_state_core::CURRENT_SCHEMA_VERSION as i32
}

/// Return the auto-generated query reference for CodeUnit fields.
///
/// Lists every queryable field path, type, allowed values, and supported
/// SQL WHERE operators. Useful for LLM/agent tool descriptions.
#[pyfunction]
fn query_reference() -> String {
    scai_state_core::QUERY_REFERENCE.to_string()
}

/// Diff a script's declared `scriptBindings[].name` set against a caller-supplied
/// `name → value` map.
///
/// Returns a dict ``{"missing": [...], "extra": [...], "empty": [...]}`` (sorted).
/// Raises ``ScaiError`` only when the script's ``kind`` is not ``"script"``.
#[pyfunction]
fn validate_bindings(
    py: Python<'_>,
    script: Bound<'_, PyAny>,
    provided: HashMap<String, String>,
) -> PyResult<Py<PyAny>> {
    let cu: CodeUnit = depythonize(&script)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
    let diff =
        scai_state_core::validate_bindings(&cu, &provided).map_err(|e| to_py_error(py, e))?;
    pythonize(py, &diff)
        .map(|b| b.unbind())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

/// Parse a SnowConvert ``database-bindings.yml`` into the token maps
/// :attr:`FindOptions.bindings` consumes.
///
/// ``yaml`` is the file *contents*. Returns a dict
/// ``{"source": {...}, "snow": {...}, "source_tokens": {...}, "snow_tokens": {...}}``:
/// the two raw ``name -> database`` maps as written, plus the wrapped literal-token
/// maps ready to hand to a read (``${NAME}`` for source, ``<%NAME%>`` for snow).
///
/// Pass ``source_wrappers`` when the conversion used a non-default source wrapper;
/// each entry is a format string containing ``{name}`` (e.g. ``"@{name}@"``). Every
/// form becomes its own key, so a name written in more than one spelling resolves
/// whichever appears. The snow side is always ``<%NAME%>`` -- Snow CLI templating is
/// invariant.
///
/// Raises ``ScaiError`` when the document is not valid or carries an unknown section.
///
/// .. warning::
///    A bound read also rewrites ``target.name`` and ``target.canonical_name``. If
///    you derive a stable identity from those -- a baseline key, a stage path, an
///    on-disk layout -- read **without** bindings for that call, or the identity
///    silently changes and previously stored artifacts stop matching.
#[pyfunction]
#[pyo3(signature = (yaml, source_wrappers = None))]
fn parse_database_bindings(
    py: Python<'_>,
    yaml: &str,
    source_wrappers: Option<Vec<String>>,
) -> PyResult<Py<PyAny>> {
    use std::collections::HashMap as Map;

    let parsed = scai_state_core::parse_database_bindings(yaml).map_err(|e| to_py_error(py, e))?;

    // Format-string wrappers keep the Python surface data-only: a callable would not
    // survive the boundary, and the core's fn-pointer type cannot be built from one.
    // Expansion is delegated to the core so the case spellings apply here too --
    // doing it inline is what previously made this path skip them.
    let source_tokens: Map<String, String> = match source_wrappers {
        None => parsed.source_token_map_default(),
        Some(forms) => parsed
            .source_token_map_from_formats(&forms)
            .map_err(PyErr::new::<pyo3::exceptions::PyValueError, _>)?,
    };

    let payload = serde_json::json!({
        "source": parsed.source,
        "snow": parsed.snow,
        "source_tokens": source_tokens,
        "snow_tokens": parsed.snow_token_map(),
    });
    pythonize(py, &payload)
        .map(|b| b.unbind())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

/// Diff a script's declared `scriptMetadata.IO[]` against the file references a
/// test case supplies.
///
/// ``provided`` is a list of dicts
/// ``{"direction": "read"|"write", "path": {"kind": "binding"|"literal", "name"?: ..., "value"?: ...}}``.
/// Returns a dict ``{"missing": [...], "extra": [...], "direction_mismatch": [...]}`` (sorted).
/// Raises ``ScaiError`` only when the script's ``kind`` is not ``"script"``.
#[pyfunction]
fn validate_script_io(
    py: Python<'_>,
    script: Bound<'_, PyAny>,
    provided: Bound<'_, PyAny>,
) -> PyResult<Py<PyAny>> {
    let cu: CodeUnit = depythonize(&script)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
    let provided: Vec<scai_state_core::ProvidedIo> = depythonize(&provided)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
    let diff =
        scai_state_core::validate_script_io(&cu, &provided).map_err(|e| to_py_error(py, e))?;
    pythonize(py, &diff)
        .map(|b| b.unbind())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

// ── Logging ─────────────────────────────────────────────────────────────

fn parse_log_level(py: Python<'_>, s: &str) -> PyResult<scai_log::LogLevel> {
    s.parse::<scai_log::LogLevel>()
        .map_err(|e| to_py_error(py, e.into()))
}

/// Python wrapper for the unified SCAI logger.
#[pyclass]
pub struct ScaiLogger {
    inner: CoreScaiLogger,
}

#[pymethods]
impl ScaiLogger {
    /// Initialize the logger.
    ///
    /// Log path: ``~/.snowflake/scai/logs/scai{YYYYMMDD}.log``
    ///
    /// Args:
    ///     process: Process identity string (e.g. ``"CLI"``, ``"DET_ENGINE"``).
    ///     project_id: Optional project ID to include in log entries.
    #[staticmethod]
    #[pyo3(signature = (process, project_id=None, session_id=None))]
    fn init(
        py: Python<'_>,
        process: &str,
        project_id: Option<&str>,
        session_id: Option<&str>,
    ) -> PyResult<Self> {
        let inner = match project_id {
            Some(pr) => CoreScaiLogger::init_with_project_id(process, pr),
            None => CoreScaiLogger::init(process),
        }
        .map_err(|e| to_py_error(py, e.into()))?;
        let inner = match session_id {
            Some(sn) => inner.with_session_id(sn),
            None => inner,
        };
        Ok(Self { inner })
    }

    /// Test-only: initialize with an explicit log directory.
    /// Not re-exported by the public ``snowflake_code_unit_registry`` wrapper.
    #[staticmethod]
    #[pyo3(signature = (process, log_dir, project_id=None, session_id=None))]
    fn init_in_dir(
        py: Python<'_>,
        process: &str,
        log_dir: &str,
        project_id: Option<&str>,
        session_id: Option<&str>,
    ) -> PyResult<Self> {
        let inner = match project_id {
            Some(pr) => CoreScaiLogger::init_in_dir_with_project_id(
                process,
                pr,
                std::path::PathBuf::from(log_dir),
            ),
            None => CoreScaiLogger::init_in_dir(process, std::path::PathBuf::from(log_dir)),
        }
        .map_err(|e| to_py_error(py, e.into()))?;
        let inner = match session_id {
            Some(sn) => inner.with_session_id(sn),
            None => inner,
        };
        Ok(Self { inner })
    }

    fn is_enabled(&self, py: Python<'_>, level: &str) -> PyResult<bool> {
        let lvl = parse_log_level(py, level)?;
        Ok(self.inner.is_enabled(lvl))
    }

    fn debug(&self, message: &str) {
        self.inner.debug(message);
    }

    fn info(&self, message: &str) {
        self.inner.info(message);
    }

    fn warn(&self, message: &str) {
        self.inner.warn(message);
    }

    fn error(&self, message: &str) {
        self.inner.error(message);
    }

    /// Log with optional structured context (dict serialized as JSON).
    #[pyo3(signature = (level, message, context=None))]
    fn log(
        &self,
        py: Python<'_>,
        level: &str,
        message: &str,
        context: Option<Bound<'_, pyo3::types::PyDict>>,
    ) -> PyResult<()> {
        let level = parse_log_level(py, level)?;
        let ctx_json = match context {
            Some(ref dict) => {
                let val: serde_json::Value = depythonize(dict)
                    .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
                Some(serde_json::to_string(&val).unwrap_or_default())
            }
            None => None,
        };
        self.inner.log(level, message, ctx_json.as_deref());
        Ok(())
    }

    /// Returns the path of the current log file.
    fn log_path(&self) -> String {
        self.inner.log_path().display().to_string()
    }
}

/// Convert a BatchResult into a Python dict.
fn batch_result_to_py(
    py: Python<'_>,
    result: &scai_state_core::BatchResult,
) -> PyResult<Py<PyAny>> {
    pythonize(py, result)
        .map(|b| b.unbind())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

/// Python module definition
#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CodeUnitRegistry>()?;
    m.add_class::<ScaiLogger>()?;
    m.add_function(wrap_pyfunction!(generate_id, m)?)?;
    m.add_function(wrap_pyfunction!(compute_file_checksum, m)?)?;
    m.add_function(wrap_pyfunction!(list_error_codes, m)?)?;
    m.add_function(wrap_pyfunction!(query_reference, m)?)?;
    m.add_function(wrap_pyfunction!(validate_bindings, m)?)?;
    m.add_function(wrap_pyfunction!(parse_database_bindings, m)?)?;
    m.add_function(wrap_pyfunction!(validate_script_io, m)?)?;
    m.add_function(wrap_pyfunction!(current_schema_version, m)?)?;
    m.add("ScaiError", m.py().get_type::<ScaiError>())?;
    Ok(())
}
