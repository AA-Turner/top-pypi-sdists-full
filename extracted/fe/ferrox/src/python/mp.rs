//! Python bindings for Materials Project data access (API + S3).

use std::collections::HashSet;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString};
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use serde_json::Value;

use crate::mp::{MPOpenData, MPRester, MpError, SearchFilter};

// === serde_json::Value <-> Py<PyAny> conversion ===

fn json_value_to_py(py: Python<'_>, val: &Value) -> Py<PyAny> {
    match val {
        Value::Null => py.None(),
        Value::Bool(b) => b.into_pyobject(py).unwrap().to_owned().into_any().unbind(),
        Value::Number(n) => {
            if let Some(idx) = n.as_i64() {
                idx.into_pyobject(py).unwrap().into_any().unbind()
            } else if let Some(fval) = n.as_f64() {
                fval.into_pyobject(py).unwrap().into_any().unbind()
            } else {
                py.None()
            }
        }
        Value::String(s) => s.into_pyobject(py).unwrap().into_any().unbind(),
        Value::Array(arr) => {
            let items: Vec<Py<PyAny>> = arr.iter().map(|v| json_value_to_py(py, v)).collect();
            PyList::new(py, &items).unwrap().into_any().unbind()
        }
        Value::Object(map) => {
            let dict = PyDict::new(py);
            for (key, val) in map {
                dict.set_item(key, json_value_to_py(py, val)).unwrap();
            }
            dict.into_any().unbind()
        }
    }
}

fn py_to_json_value(obj: &Bound<'_, PyAny>) -> PyResult<Value> {
    if obj.is_none() {
        return Ok(Value::Null);
    }
    if let Ok(b) = obj.cast::<PyBool>() {
        return Ok(Value::Bool(b.is_true()));
    }
    if let Ok(i) = obj.cast::<PyInt>() {
        let val: i64 = i.extract()?;
        return Ok(Value::Number(val.into()));
    }
    if let Ok(f) = obj.cast::<PyFloat>() {
        let val: f64 = f.extract()?;
        return Ok(serde_json::Number::from_f64(val).map_or(Value::Null, Value::Number));
    }
    if let Ok(s) = obj.cast::<PyString>() {
        return Ok(Value::String(s.to_string()));
    }
    if let Ok(lst) = obj.cast::<PyList>() {
        let items: PyResult<Vec<Value>> = lst.iter().map(|item| py_to_json_value(&item)).collect();
        return Ok(Value::Array(items?));
    }
    if let Ok(d) = obj.cast::<PyDict>() {
        let mut map = serde_json::Map::new();
        for (key, val) in d.iter() {
            let key_str: String = key.extract()?;
            map.insert(key_str, py_to_json_value(&val)?);
        }
        return Ok(Value::Object(map));
    }
    Err(PyValueError::new_err(format!(
        "Cannot convert Python {type_name} to JSON value",
        type_name = obj.get_type().name()?
    )))
}

// === Error conversion ===

pyo3::create_exception!(
    ferrox._ferrox.mp,
    MPClientError,
    pyo3::exceptions::PyRuntimeError,
    "Base error for all Materials Project operations."
);
pyo3::create_exception!(
    ferrox._ferrox.mp,
    MPHTTPError,
    MPClientError,
    "HTTP-level error from Materials Project API."
);
pyo3::create_exception!(
    ferrox._ferrox.mp,
    MPDecodeError,
    MPClientError,
    "Response parsing error (XML or JSON)."
);

fn mp_error_to_py(err: MpError) -> PyErr {
    match &err {
        MpError::Http { .. } => MPHTTPError::new_err(err.to_string()),
        MpError::Xml(_) => MPDecodeError::new_err(err.to_string()),
        _ => MPClientError::new_err(err.to_string()),
    }
}

// === PyO3 classes ===

/// Materials Project REST API client with parallel paginated search.
///
/// Uses Rust HTTP (ureq) with connection pooling and rayon for parallel
/// page fetches.  Typically 5-8x faster than sequential Python urllib.
///
/// ```python
/// mpr = MPRester("your_api_key")
/// docs = mpr.search(
///     "materials/summary",
///     fields=["material_id", "formula_pretty"],
///     chemsys="Li-Fe-O",
///     limit=100,
/// )
/// ```
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.mp", name = "MPRester")]
pub struct PyMPRester {
    inner: MPRester,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyMPRester {
    /// Create a new API client.
    ///
    /// Args:
    ///     api_key: Materials Project API key.
    ///     base_url: API base URL (default: ``https://api.materialsproject.org``).
    ///     timeout_seconds: Per-request timeout.
    #[new]
    #[pyo3(signature = (api_key, *, base_url=None, timeout_seconds=30))]
    fn new(api_key: String, base_url: Option<String>, timeout_seconds: u64) -> PyResult<Self> {
        if api_key.is_empty() {
            return Err(PyValueError::new_err("api_key must be a non-empty string"));
        }
        Ok(Self {
            inner: MPRester::new(api_key, base_url, timeout_seconds),
        })
    }

    fn __repr__(&self) -> String {
        "MPRester(api_key='...')".to_owned()
    }

    /// Fetch a single document by ID.
    ///
    /// Args:
    ///     path: Endpoint path, e.g. ``"materials/summary"``.
    ///     doc_id: Document identifier, e.g. ``"mp-149"``.
    fn get_by_id(&self, py: Python<'_>, path: &str, doc_id: &str) -> PyResult<Py<PyAny>> {
        let result = py.detach(|| self.inner.get_by_id(path, doc_id).map_err(mp_error_to_py))?;
        Ok(json_value_to_py(py, &result))
    }

    /// Search with parallel paginated fetching.
    ///
    /// Fetches the first page to discover total count, then fires remaining
    /// pages in parallel via Rust threads for maximum throughput.
    ///
    /// Args:
    ///     path: Endpoint path, e.g. ``"materials/summary"``.
    ///     fields: Field(s) to include in returned documents.
    ///     limit: Maximum total documents to return.
    ///     chunk_size: Documents per API page (default 1000).
    ///     **query: Arbitrary query parameters (chemsys, elements, etc.).
    #[pyo3(signature = (path, *, fields=None, limit=None, chunk_size=1000, **query))]
    fn search(
        &self,
        py: Python<'_>,
        path: &str,
        fields: Option<Vec<String>>,
        limit: Option<usize>,
        chunk_size: usize,
        query: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<Py<PyAny>> {
        let mut params: Vec<(String, String)> = Vec::new();

        if let Some(ref field_list) = fields {
            params.push(("_fields".into(), field_list.join(",")));
        }

        if let Some(kwargs) = query {
            for (key, val) in kwargs.iter() {
                let key_str: String = key.extract()?;
                let val_str = py_value_to_query_string(&val)?;
                params.push((key_str, val_str));
            }
        }

        let endpoint = if path.starts_with('/') {
            path.to_owned()
        } else {
            format!("/{path}")
        };

        let results = py.detach(|| {
            self.inner
                .search(&endpoint, &params, limit, chunk_size)
                .map_err(mp_error_to_py)
        })?;

        let py_list: Vec<Py<PyAny>> = results
            .iter()
            .map(|doc| json_value_to_py(py, doc))
            .collect();
        Ok(PyList::new(py, &py_list)?.into_any().unbind())
    }
}

/// Convert a Python query parameter value to a string for URL encoding.
fn py_value_to_query_string(obj: &Bound<'_, PyAny>) -> PyResult<String> {
    if let Ok(b) = obj.cast::<PyBool>() {
        return Ok(if b.is_true() { "true" } else { "false" }.into());
    }
    if let Ok(lst) = obj.cast::<PyList>() {
        let items: PyResult<Vec<String>> = lst
            .iter()
            .map(|item| item.str().map(|s| s.to_string()))
            .collect();
        return Ok(items?.join(","));
    }
    Ok(obj.str()?.to_string())
}

/// Direct access to Materials Project data on AWS Open Data S3 buckets.
///
/// No API key required.  Downloads gzip-compressed JSONL collection data
/// directly from ``s3://materialsproject-build`` and applies filters
/// client-side.  Multiple files are fetched in parallel via Rust threads.
///
/// ```python
/// mp = MPOpenData()
/// docs = mp.search(
///     "summary",
///     chemsys="Li-Fe-O",
///     fields=["material_id", "formula_pretty"],
/// )
/// ```
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.mp", name = "MPOpenData")]
pub struct PyMPOpenData {
    inner: MPOpenData,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyMPOpenData {
    /// Create a new open-data client.
    ///
    /// Args:
    ///     version: Database version string (e.g. ``'2024-11-14'``).
    ///         ``None`` auto-detects the latest available version.
    ///     timeout_seconds: Per-request timeout for S3 downloads.
    #[new]
    #[pyo3(signature = (version=None, timeout_seconds=120))]
    fn new(version: Option<String>, timeout_seconds: u64) -> Self {
        Self {
            inner: MPOpenData::new(version, timeout_seconds, "ferrox-mp-opendata".into()),
        }
    }

    /// Return string representation with version info.
    fn __repr__(&mut self) -> String {
        let ver = self
            .inner
            .version()
            .map(|v| v.to_owned())
            .unwrap_or_else(|_| "unknown".into());
        format!("MPOpenData(version='{ver}')")
    }

    /// Resolved database version (auto-detects latest if not set).
    #[getter]
    fn version(&mut self) -> PyResult<String> {
        self.inner
            .version()
            .map(|s| s.to_owned())
            .map_err(mp_error_to_py)
    }

    /// List available database versions (e.g. ``['2022-10-28', '2024-11-14']``).
    fn list_versions(&self) -> PyResult<Vec<String>> {
        self.inner.list_versions().map_err(mp_error_to_py)
    }

    /// List available collection names for a database version.
    ///
    /// Args:
    ///     version: Override the instance version for this call.
    #[pyo3(signature = (version=None))]
    fn list_collections(&mut self, version: Option<&str>) -> PyResult<Vec<String>> {
        self.inner.list_collections(version).map_err(mp_error_to_py)
    }

    /// Download and filter collection data from S3.
    ///
    /// Fetches gzipped JSONL files from the ``materialsproject-build``
    /// bucket and applies all filters client-side in Rust.
    ///
    /// Args:
    ///     collection: Collection name (e.g. ``'summary'``, ``'thermo'``).
    ///     fields: Field(s) to include in returned documents.
    ///     chemsys: Chemical system filter, e.g. ``'Li-Fe-O'``.
    ///     elements: Required elements — materials must contain *all*.
    ///     exclude_elements: Excluded elements — materials must contain *none*.
    ///     material_ids: Filter to specific material IDs.
    ///     formula: Exact match on ``formula_pretty``.
    ///     energy_above_hull_max: Upper bound on ``energy_above_hull`` (eV/atom).
    ///     band_gap_min: Lower bound on ``band_gap`` (eV).
    ///     band_gap_max: Upper bound on ``band_gap`` (eV).
    ///     nsites_min: Minimum number of sites.
    ///     nsites_max: Maximum number of sites.
    ///     filter_fn: Arbitrary callable applied to each document dict (Python-side post-filter).
    ///     limit: Maximum number of documents to return.
    ///     **match_kwargs: Generic exact-match filters on any document field,
    ///         e.g. ``is_stable=True``, ``crystal_system="cubic"``.
    ///
    /// Returns:
    ///     List of matching document dicts.
    #[pyo3(signature = (
        collection,
        *,
        fields=None,
        chemsys=None,
        elements=None,
        exclude_elements=None,
        material_ids=None,
        formula=None,
        energy_above_hull_max=None,
        band_gap_min=None,
        band_gap_max=None,
        nsites_min=None,
        nsites_max=None,
        filter_fn=None,
        limit=None,
        **match_kwargs,
    ))]
    #[allow(clippy::too_many_arguments)]
    fn search(
        &mut self,
        py: Python<'_>,
        collection: &str,
        fields: Option<Vec<String>>,
        chemsys: Option<&str>,
        elements: Option<Vec<String>>,
        exclude_elements: Option<Vec<String>>,
        material_ids: Option<Vec<String>>,
        formula: Option<String>,
        energy_above_hull_max: Option<f64>,
        band_gap_min: Option<f64>,
        band_gap_max: Option<f64>,
        nsites_min: Option<u64>,
        nsites_max: Option<u64>,
        filter_fn: Option<Py<PyAny>>,
        limit: Option<usize>,
        match_kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<Py<PyAny>> {
        let mut match_fields = Vec::new();
        if let Some(kwargs) = match_kwargs {
            for (key, val) in kwargs.iter() {
                let key_str: String = key.extract()?;
                let json_val = py_to_json_value(&val)?;
                match_fields.push((key_str, json_val));
            }
        }

        let filter = SearchFilter {
            chemsys: chemsys.map(SearchFilter::parse_chemsys),
            elements: elements.map(|v| v.into_iter().collect()),
            exclude_elements: exclude_elements.map(|v| v.into_iter().collect()),
            material_ids: material_ids.map(|v| v.into_iter().collect()),
            formula,
            energy_above_hull_max,
            band_gap_min,
            band_gap_max,
            nsites_min,
            nsites_max,
            match_fields,
        };

        let field_set: Option<HashSet<String>> = fields.map(|v| v.into_iter().collect());

        // When filter_fn is set, fetch without limit so the Python callback
        // sees all Rust-filtered docs before we truncate.
        let rust_limit = if filter_fn.is_some() { None } else { limit };

        let results = py.detach(|| {
            self.inner
                .search(collection, &filter, field_set.as_ref(), rust_limit)
                .map_err(mp_error_to_py)
        })?;

        let py_dicts: Vec<Py<PyAny>> = if let Some(ref func) = filter_fn {
            let mut filtered = Vec::new();
            for doc in &results {
                if let Some(cap) = limit {
                    if filtered.len() >= cap {
                        break;
                    }
                }
                let py_dict = json_value_to_py(py, doc);
                let keep: bool = func.call1(py, (&py_dict,))?.extract(py)?;
                if keep {
                    filtered.push(py_dict);
                }
            }
            filtered
        } else {
            results
                .iter()
                .map(|doc| json_value_to_py(py, doc))
                .collect()
        };

        Ok(PyList::new(py, &py_dicts)?.into_any().unbind())
    }

    // --- Parsed bucket (per-material files) ---

    /// List data categories in the parsed bucket.
    ///
    /// Returns category names like ``['bandstructures', 'chgcars', 'dos', ...]``.
    fn list_parsed_categories(&self) -> PyResult<Vec<String>> {
        self.inner.list_parsed_categories().map_err(mp_error_to_py)
    }

    /// Download a single parsed document by material ID.
    ///
    /// Files are stored as ``{category}/{material_id}.json.gz`` in the
    /// ``materialsproject-parsed`` S3 bucket. No API key required.
    ///
    /// Args:
    ///     category: Data category (e.g. ``'chgcars'``, ``'dos'``,
    ///         ``'bandstructures'``).
    ///     material_id: Material identifier (e.g. ``'mp-149'``).
    ///
    /// ```python
    /// mp = MPOpenData()
    /// chgcar = mp.get_parsed("chgcars", "mp-149")
    /// ```
    fn get_parsed(&self, py: Python<'_>, category: &str, material_id: &str) -> PyResult<Py<PyAny>> {
        let result = py.detach(|| {
            self.inner
                .get_parsed(category, material_id)
                .map_err(mp_error_to_py)
        })?;
        Ok(json_value_to_py(py, &result))
    }

    /// Download multiple parsed documents in parallel.
    ///
    /// Returns a list of ``(material_id, doc)`` tuples. Failed downloads
    /// are silently skipped. Shows a tqdm progress bar if tqdm is installed.
    ///
    /// Args:
    ///     category: Data category (e.g. ``'chgcars'``, ``'dos'``).
    ///     material_ids: List of material identifiers.
    ///     show_progress: Whether to show a progress bar (default ``True``).
    ///
    /// ```python
    /// mp = MPOpenData()
    /// results = mp.get_parsed_batch("dos", ["mp-149", "mp-13"])
    /// ```
    #[pyo3(signature = (category, material_ids, *, show_progress=true))]
    fn get_parsed_batch(
        &self,
        py: Python<'_>,
        category: &str,
        material_ids: Vec<String>,
        show_progress: bool,
    ) -> PyResult<Py<PyAny>> {
        let total = material_ids.len();
        let progress = std::sync::Arc::new(std::sync::atomic::AtomicUsize::new(0));

        // Try to create a tqdm progress bar
        let pbar: Option<Py<PyAny>> = if show_progress && total > 1 {
            py.import("tqdm.auto")
                .or_else(|_| py.import("tqdm"))
                .ok()
                .and_then(|tqdm_mod| {
                    tqdm_mod
                        .getattr("tqdm")
                        .ok()?
                        .call1((total,))
                        .ok()
                        .map(|obj| {
                            let _ = obj.setattr("unit", "file");
                            let _ = obj.setattr("desc", format!("Downloading {category}"));
                            obj.unbind()
                        })
                })
        } else {
            None
        };

        // Spawn a polling thread that updates tqdm from the AtomicUsize counter.
        // The polling thread acquires the GIL briefly each tick.
        let done_flag = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));

        let poll_handle: Option<std::thread::JoinHandle<()>> = if let Some(ref pbar_ref) = pbar {
            let progress_clone = progress.clone();
            let done_clone = done_flag.clone();
            let pbar_clone: Py<PyAny> = pbar_ref.clone_ref(py);
            Some(std::thread::spawn(move || {
                let mut last_seen = 0usize;
                loop {
                    std::thread::sleep(std::time::Duration::from_millis(100));
                    let current = progress_clone.load(std::sync::atomic::Ordering::Relaxed);
                    if current > last_seen {
                        let delta = current - last_seen;
                        last_seen = current;
                        Python::attach(|py_inner| {
                            let _ = pbar_clone.call_method1(py_inner, "update", (delta,));
                        });
                    }
                    if done_clone.load(std::sync::atomic::Ordering::Relaxed) {
                        // Final flush
                        let final_count = progress_clone.load(std::sync::atomic::Ordering::Relaxed);
                        if final_count > last_seen {
                            let delta = final_count - last_seen;
                            Python::attach(|py_inner| {
                                let _ = pbar_clone.call_method1(py_inner, "update", (delta,));
                            });
                        }
                        break;
                    }
                }
            }))
        } else {
            None
        };

        // Run the parallel downloads AND wait for polling thread, all with GIL released
        let results = py.detach(|| {
            let result = self
                .inner
                .get_parsed_batch(category, &material_ids, Some(&progress))
                .map_err(mp_error_to_py);
            done_flag.store(true, std::sync::atomic::Ordering::Relaxed);
            if let Some(handle) = poll_handle {
                let _ = handle.join();
            }
            result
        })?;

        // Close the progress bar
        if let Some(ref pbar_obj) = pbar {
            let _ = pbar_obj.call_method0(py, "close");
        }

        let py_tuples: Vec<Py<PyAny>> = results
            .iter()
            .map(|(mid, doc)| {
                let py_mid = mid.into_pyobject(py).unwrap().into_any().unbind();
                let py_doc = json_value_to_py(py, doc);
                let tuple = pyo3::types::PyTuple::new(py, &[py_mid, py_doc]).unwrap();
                tuple.into_any().unbind()
            })
            .collect();
        Ok(PyList::new(py, &py_tuples)?.into_any().unbind())
    }
}

/// Register mp functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add("MPClientError", module.py().get_type::<MPClientError>())?;
    module.add("MPHTTPError", module.py().get_type::<MPHTTPError>())?;
    module.add("MPDecodeError", module.py().get_type::<MPDecodeError>())?;
    module.add_class::<PyMPRester>()?;
    module.add_class::<PyMPOpenData>()?;
    Ok(())
}
