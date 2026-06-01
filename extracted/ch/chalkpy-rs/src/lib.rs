pub use chalk_ast as ast;
pub use chalk_ast::*;
pub use chalk_ignore as ignore;
pub use chalk_project as project;
pub use chalk_proto as proto;
pub use chalk_utils::{duration, isodate, namespace};

// ---------------------------------------------------------------------------
// PyO3 Python bindings (gated behind "python" feature)
// ---------------------------------------------------------------------------

#[cfg(feature = "python")]
use std::collections::HashMap;
#[cfg(feature = "python")]
use std::sync::Arc;

#[cfg(feature = "python")]
use pyo3::exceptions::{PyIOError, PyOverflowError, PyTypeError, PyValueError};
#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use pyo3::types::{
    PyAny, PyDate, PyDateAccess, PyDateTime, PyDelta, PyDeltaAccess, PyModule, PyTime, PyTzInfo,
};

#[cfg(feature = "python")]
type PyRangeTuple = (u32, u32, u32, u32);

#[cfg(feature = "python")]
fn location_to_range_tuple(location: lsp_types::Location) -> PyRangeTuple {
    (
        location.range.start.line,
        location.range.start.character,
        location.range.end.line,
        location.range.end.character,
    )
}

#[cfg(feature = "python")]
fn import_alias_map_to_python(
    imports: &chalk_ast::ImportAliasMap,
) -> HashMap<String, HashMap<String, Vec<String>>> {
    imports
        .iter()
        .map(|(module, symbols)| {
            let symbols = symbols
                .iter()
                .map(|(symbol, aliases)| {
                    let mut aliases: Vec<String> = aliases.iter().cloned().collect();
                    aliases.sort();
                    (symbol.clone(), aliases)
                })
                .collect();
            (module.clone(), symbols)
        })
        .collect()
}

#[cfg(feature = "python")]
fn kwarg_location_map_to_python(
    kwargs: &chalk_ast::KwargLocationMap,
) -> HashMap<String, PyRangeTuple> {
    kwargs
        .iter()
        .map(|(name, location)| (name.clone(), location_to_range_tuple(location.clone())))
        .collect()
}

#[cfg(feature = "python")]
fn nested_kwarg_location_map_to_python(
    kwargs: &HashMap<String, chalk_ast::KwargLocationMap>,
) -> HashMap<String, HashMap<String, PyRangeTuple>> {
    kwargs
        .iter()
        .map(|(name, nested)| (name.clone(), kwarg_location_map_to_python(nested)))
        .collect()
}

#[cfg(feature = "python")]
#[pyclass(name = "StdAstFileSystem", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyStdAstFileSystem {
    inner: Arc<chalk_ast::StdAstFileSystem>,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyStdAstFileSystem {
    #[new]
    #[pyo3(signature = (files))]
    fn new(files: Vec<String>) -> PyResult<Self> {
        Ok(Self {
            inner: Arc::new(chalk_ast::StdAstFileSystem::new(files)),
        })
    }

    fn read_to_string(&self, py: Python, path: &str) -> PyResult<String> {
        py.detach(|| self.inner.read_to_string(path))
            .map_err(|err| PyIOError::new_err(err.to_string()))
    }

    fn all_files(&self, py: Python) -> PyResult<Vec<String>> {
        py.detach(|| self.inner.all_files())
            .map_err(|err| PyIOError::new_err(err.to_string()))
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "AstFileParserCache", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyAstFileParserCache {
    inner: chalk_ast::AstFileParserCache,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyAstFileParserCache {
    #[new]
    #[pyo3(signature = (files, project_root, filesystem=None))]
    fn new(
        py: Python,
        files: Vec<String>,
        project_root: String,
        filesystem: Option<Py<PyStdAstFileSystem>>,
    ) -> PyResult<Self> {
        let project_root = std::path::PathBuf::from(project_root);
        let inner = match filesystem {
            Some(filesystem) => {
                let filesystem = filesystem.borrow(py);
                let fs: Arc<dyn chalk_ast::AstFileSystem> = filesystem.inner.clone();
                chalk_ast::AstFileParserCache::with_filesystem(project_root, fs)
            }
            None => chalk_ast::AstFileParserCache::new(project_root, files),
        };
        Ok(Self { inner })
    }

    fn all_files(&self, py: Python) -> PyResult<Vec<String>> {
        py.detach(|| self.inner.all_files())
            .map_err(|err| PyIOError::new_err(err.to_string()))
    }

    fn get_parsed_file(
        &self,
        py: Python,
        path: &str,
    ) -> PyResult<(
        String,
        String,
        HashMap<String, HashMap<String, Vec<String>>>,
    )> {
        let parsed = py
            .detach(|| self.inner.get_parsed_file(path))
            .map_err(PyValueError::new_err)?;
        Ok((
            parsed.path.clone(),
            parsed.source.clone(),
            import_alias_map_to_python(&parsed.imports),
        ))
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "FeatureFieldAST", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyFeatureFieldAST {
    inner: chalk_ast::FeatureFieldAST,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyFeatureFieldAST {
    #[getter]
    fn field_name(&self) -> String {
        self.inner.field_name.clone()
    }

    #[getter]
    fn field_name_location(&self) -> PyRangeTuple {
        location_to_range_tuple(self.inner.field_name_location.clone())
    }

    #[getter]
    fn comment(&self) -> Option<String> {
        self.inner.comment.clone()
    }

    #[getter]
    fn description(&self) -> Option<String> {
        self.inner.description.clone()
    }

    #[getter]
    fn owner(&self) -> Option<String> {
        self.inner.owner.clone()
    }

    #[getter]
    fn tags(&self) -> Vec<String> {
        self.inner.tags.clone()
    }

    #[getter]
    fn annotation(&self) -> Option<PyRangeTuple> {
        self.inner.annotation.clone().map(location_to_range_tuple)
    }

    #[getter]
    fn feature_call(&self) -> Option<PyRangeTuple> {
        self.inner.feature_call.clone().map(location_to_range_tuple)
    }

    #[getter]
    fn kwarg_names(&self) -> HashMap<String, PyRangeTuple> {
        kwarg_location_map_to_python(&self.inner.kwarg_names)
    }

    #[getter]
    fn kwargs(&self) -> HashMap<String, PyRangeTuple> {
        kwarg_location_map_to_python(&self.inner.kwargs)
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "FeatureClassAST", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyFeatureClassAST {
    inner: chalk_ast::FeatureClassAST,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyFeatureClassAST {
    #[getter]
    fn module(&self) -> String {
        self.inner.module.clone()
    }

    #[getter]
    fn namespace(&self) -> String {
        self.inner.namespace.clone()
    }

    #[getter]
    fn class_name(&self) -> String {
        self.inner.class_name.clone()
    }

    #[getter]
    fn source(&self) -> String {
        self.inner.source.clone()
    }

    #[getter]
    fn class_name_location(&self) -> PyRangeTuple {
        location_to_range_tuple(self.inner.class_name_location.clone())
    }

    #[getter]
    fn class_definition_location(&self) -> PyRangeTuple {
        location_to_range_tuple(self.inner.class_definition_location.clone())
    }

    #[getter]
    fn decorator_location(&self) -> PyRangeTuple {
        location_to_range_tuple(self.inner.decorator_location.clone())
    }

    #[getter]
    fn kwarg_names(&self) -> HashMap<String, PyRangeTuple> {
        kwarg_location_map_to_python(&self.inner.kwarg_names)
    }

    #[getter]
    fn kwargs(&self) -> HashMap<String, PyRangeTuple> {
        kwarg_location_map_to_python(&self.inner.kwargs)
    }

    #[getter]
    fn fields(&self) -> HashMap<String, PyFeatureFieldAST> {
        self.inner
            .fields
            .iter()
            .map(|(name, field)| {
                (
                    name.clone(),
                    PyFeatureFieldAST {
                        inner: field.clone(),
                    },
                )
            })
            .collect()
    }

    #[getter]
    fn annotations(&self) -> Vec<PyFeatureFieldAST> {
        self.inner
            .annotations
            .iter()
            .cloned()
            .map(|field| PyFeatureFieldAST { inner: field })
            .collect()
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "FunctionArgAST", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyFunctionArgAST {
    inner: chalk_ast::FunctionArgAST,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyFunctionArgAST {
    #[getter]
    fn arg_name(&self) -> String {
        self.inner.arg_name.clone()
    }

    #[getter]
    fn arg_location(&self) -> PyRangeTuple {
        location_to_range_tuple(self.inner.arg_location.clone())
    }

    #[getter]
    fn annotation(&self) -> Option<PyRangeTuple> {
        self.inner.annotation.clone().map(location_to_range_tuple)
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "ResolverAST", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyResolverAST {
    inner: chalk_ast::ResolverAST,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyResolverAST {
    #[getter]
    fn module(&self) -> String {
        self.inner.module.clone()
    }

    #[getter]
    fn resolver_name(&self) -> String {
        self.inner.resolver_name.clone()
    }

    #[getter]
    fn resolver_name_location(&self) -> PyRangeTuple {
        location_to_range_tuple(self.inner.resolver_name_location.clone())
    }

    #[getter]
    fn decorator_location(&self) -> Option<PyRangeTuple> {
        self.inner
            .decorator_location
            .clone()
            .map(location_to_range_tuple)
    }

    #[getter]
    fn kwarg_names(&self) -> HashMap<String, PyRangeTuple> {
        kwarg_location_map_to_python(&self.inner.kwarg_names)
    }

    #[getter]
    fn kwargs(&self) -> HashMap<String, PyRangeTuple> {
        kwarg_location_map_to_python(&self.inner.kwargs)
    }

    #[getter]
    fn kwarg_dict_key_names(&self) -> HashMap<String, HashMap<String, PyRangeTuple>> {
        nested_kwarg_location_map_to_python(&self.inner.kwarg_dict_key_names)
    }

    #[getter]
    fn kwarg_dict_values(&self) -> HashMap<String, HashMap<String, PyRangeTuple>> {
        nested_kwarg_location_map_to_python(&self.inner.kwarg_dict_values)
    }

    #[getter]
    fn args_in_order(&self) -> Vec<String> {
        self.inner.args_in_order.clone()
    }

    #[getter]
    fn args(&self) -> HashMap<String, PyFunctionArgAST> {
        self.inner
            .args
            .iter()
            .map(|(name, arg)| (name.clone(), PyFunctionArgAST { inner: arg.clone() }))
            .collect()
    }

    #[getter]
    fn return_annotation(&self) -> Option<PyRangeTuple> {
        self.inner
            .return_annotation
            .clone()
            .map(location_to_range_tuple)
    }

    #[getter]
    fn missing_return_annotation(&self) -> Option<PyRangeTuple> {
        self.inner
            .missing_return_annotation
            .clone()
            .map(location_to_range_tuple)
    }

    #[getter]
    fn return_statements(&self) -> Vec<PyRangeTuple> {
        self.inner
            .return_statements
            .iter()
            .cloned()
            .map(location_to_range_tuple)
            .collect()
    }

    #[getter]
    fn body(&self) -> Option<PyRangeTuple> {
        self.inner.body.clone().map(location_to_range_tuple)
    }

    #[getter]
    fn return_arg(&self) -> Option<PyRangeTuple> {
        self.inner.return_arg.clone().map(location_to_range_tuple)
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "AstProjectIndex", skip_from_py_object)]
#[derive(Clone, Debug)]
struct PyAstProjectIndex {
    inner: chalk_ast::AstProjectIndex,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyAstProjectIndex {
    #[new]
    #[pyo3(signature = (files, project_root, filesystem=None))]
    fn new(
        py: Python,
        files: Vec<String>,
        project_root: String,
        filesystem: Option<Py<PyStdAstFileSystem>>,
    ) -> PyResult<Self> {
        let project_root = std::path::PathBuf::from(project_root);
        let fs = filesystem.map(|filesystem| {
            let filesystem = filesystem.borrow(py);
            let fs: Arc<dyn chalk_ast::AstFileSystem> = filesystem.inner.clone();
            fs
        });
        let inner = py
            .detach(move || match fs {
                Some(fs) => {
                    chalk_ast::AstProjectIndex::with_filesystem(project_root.clone(), files, fs)
                }
                None => chalk_ast::AstProjectIndex::new(project_root, files),
            })
            .map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    fn feature_class_ast(&self, module: &str, class_name: &str) -> Option<PyFeatureClassAST> {
        self.inner
            .feature_class_ast(module, class_name)
            .map(|ast| PyFeatureClassAST { inner: ast })
    }

    fn feature_class_ast_in_file(
        &self,
        file_path: &str,
        class_name: &str,
    ) -> Option<PyFeatureClassAST> {
        self.inner
            .feature_class_ast_in_file(file_path, class_name)
            .map(|ast| PyFeatureClassAST { inner: ast })
    }

    fn resolver_ast(&self, module: &str, resolver_name: &str) -> Option<PyResolverAST> {
        self.inner
            .resolver_ast(module, resolver_name)
            .map(|ast| PyResolverAST { inner: ast })
    }

    fn resolver_ast_in_file(&self, file_path: &str, resolver_name: &str) -> Option<PyResolverAST> {
        self.inner
            .resolver_ast_in_file(file_path, resolver_name)
            .map(|ast| PyResolverAST { inner: ast })
    }

    fn function_ast(&self, module: &str, function_name: &str) -> Option<PyResolverAST> {
        self.inner
            .function_ast(module, function_name)
            .map(|ast| PyResolverAST { inner: ast })
    }

    fn function_ast_in_file(&self, file_path: &str, function_name: &str) -> Option<PyResolverAST> {
        self.inner
            .function_ast_in_file(file_path, function_name)
            .map(|ast| PyResolverAST { inner: ast })
    }

    fn nonblocking_start_index(&self) {
        self.inner.nonblocking_start_index();
    }
}

#[cfg(feature = "python")]
#[pyfunction]
fn parse_duration_ms(py: Python, s: &str) -> PyResult<i64> {
    py.detach(|| duration::parse_duration_ms(s))
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))
}

#[cfg(feature = "python")]
#[pyfunction]
fn parse_duration_s(py: Python, s: &str) -> PyResult<i64> {
    py.detach(|| duration::parse_duration_s(s))
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))
}

#[cfg(feature = "python")]
#[pyfunction]
fn seconds_to_duration_string(py: Python, total_seconds: f64) -> String {
    py.detach(|| duration::seconds_to_duration_string(total_seconds))
}

#[cfg(feature = "python")]
fn iso_timezone_to_python<'py>(
    py: Python<'py>,
    timezone: Option<isodate::IsoTimezone>,
) -> PyResult<Option<Bound<'py, PyTzInfo>>> {
    match timezone {
        None => Ok(None),
        Some(isodate::IsoTimezone::Utc) => Ok(Some(PyTzInfo::utc(py)?.to_owned())),
        Some(isodate::IsoTimezone::Fixed { name, seconds }) => {
            let offset = PyDelta::new(py, 0, seconds, 0, true)?;
            let datetime = PyModule::import(py, "datetime")?;
            Ok(Some(
                datetime
                    .getattr("timezone")?
                    .call1((offset, name))?
                    .cast_into::<PyTzInfo>()?,
            ))
        }
    }
}

#[cfg(feature = "python")]
fn datetime_timezone_to_python<'py>(
    py: Python<'py>,
    timezone: Option<isodate::IsoTimezone>,
) -> PyResult<Option<Bound<'py, PyTzInfo>>> {
    match timezone {
        None => Ok(None),
        Some(isodate::IsoTimezone::Utc) | Some(isodate::IsoTimezone::Fixed { seconds: 0, .. }) => {
            Ok(Some(PyTzInfo::utc(py)?.to_owned()))
        }
        Some(isodate::IsoTimezone::Fixed { seconds, .. }) => {
            let offset = PyDelta::new(py, 0, seconds, 0, true)?;
            Ok(Some(PyTzInfo::fixed_offset(py, offset)?))
        }
    }
}

#[cfg(feature = "python")]
#[pyfunction]
fn parse_iso_date<'py>(py: Python<'py>, s: &str) -> PyResult<Bound<'py, PyDate>> {
    let parsed = py
        .detach(|| isodate::parse_date(s))
        .map_err(PyValueError::new_err)?;
    PyDate::new(py, parsed.year, parsed.month, parsed.day)
}

#[cfg(feature = "python")]
#[pyfunction]
fn parse_iso_time<'py>(py: Python<'py>, s: &str) -> PyResult<Bound<'py, PyTime>> {
    let parsed = py
        .detach(|| isodate::parse_time(s))
        .map_err(PyValueError::new_err)?;
    let timezone = iso_timezone_to_python(py, parsed.timezone)?;
    PyTime::new(
        py,
        parsed.hour,
        parsed.minute,
        parsed.second,
        parsed.microsecond,
        timezone.as_ref(),
    )
}

#[cfg(feature = "python")]
#[pyfunction]
fn parse_datetime<'py>(py: Python<'py>, s: &str) -> PyResult<Bound<'py, PyDateTime>> {
    let today = py
        .import("datetime")?
        .getattr("date")?
        .call_method0("today")?
        .cast_into::<PyDate>()?;
    let default_date = isodate::IsoDate {
        year: today.get_year(),
        month: today.get_month(),
        day: today.get_day(),
    };
    let parsed = py
        .detach(|| isodate::parse_datetime_with_default_date(s, Some(default_date)))
        .map_err(PyValueError::new_err)?;
    let timezone = datetime_timezone_to_python(py, parsed.time.timezone)?;
    PyDateTime::new(
        py,
        parsed.date.year,
        parsed.date.month,
        parsed.date.day,
        parsed.time.hour,
        parsed.time.minute,
        parsed.time.second,
        parsed.time.microsecond,
        timezone.as_ref(),
    )
}

#[cfg(feature = "python")]
#[pyfunction]
fn parse_iso_duration<'py>(py: Python<'py>, s: &str) -> PyResult<Bound<'py, PyDelta>> {
    let parsed = py
        .detach(|| isodate::parse_duration(s))
        .map_err(PyValueError::new_err)?;
    let isodate::IsoDuration::Timedelta { total_microseconds } = parsed else {
        return Err(PyTypeError::new_err(format!(
            "ISO 8601 duration '{s}' contains year/month components that cannot be represented as a fixed timedelta"
        )));
    };
    let (days, seconds, microseconds) =
        isodate::split_timedelta(total_microseconds).map_err(PyOverflowError::new_err)?;
    PyDelta::new(py, days, seconds, microseconds, false)
}

#[cfg(feature = "python")]
#[pyfunction]
fn duration_isoformat(py: Python, tduration: &Bound<'_, PyAny>) -> PyResult<String> {
    let delta = tduration
        .cast::<PyDelta>()
        .map_err(|_| PyTypeError::new_err("duration_isoformat expects a datetime.timedelta"))?;
    let days = delta.get_days();
    let seconds = delta.get_seconds();
    let microseconds = delta.get_microseconds();
    Ok(py.detach(|| isodate::duration_isoformat(days, seconds, microseconds)))
}

#[cfg(feature = "python")]
#[pyfunction]
fn timezone_from_name<'py>(py: Python<'py>, name: &str) -> PyResult<Option<Bound<'py, PyTzInfo>>> {
    if name.is_empty() {
        return Ok(None);
    }
    let zone_info = PyModule::import(py, "zoneinfo")?.getattr("ZoneInfo")?;
    match zone_info.call1((name,)) {
        Ok(tz) => Ok(Some(tz.cast_into::<PyTzInfo>()?)),
        Err(_) => Ok(None),
    }
}

#[cfg(feature = "python")]
#[pyfunction]
fn to_snake_case(py: Python, name: &str) -> String {
    py.detach(|| chalk_utils::to_snake_case(name))
}

#[cfg(feature = "python")]
#[pyfunction]
#[pyo3(signature = (namespace=None, name=None))]
fn build_namespaced_name(py: Python, namespace: Option<&str>, name: Option<&str>) -> String {
    py.detach(|| chalk_utils::build_namespaced_name(namespace, name))
}

#[cfg(feature = "python")]
#[pymodule]
fn chalk_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyStdAstFileSystem>()?;
    m.add_class::<PyAstFileParserCache>()?;
    m.add_class::<PyFeatureFieldAST>()?;
    m.add_class::<PyFeatureClassAST>()?;
    m.add_class::<PyFunctionArgAST>()?;
    m.add_class::<PyResolverAST>()?;
    m.add_class::<PyAstProjectIndex>()?;
    m.add_function(wrap_pyfunction!(parse_duration_ms, m)?)?;
    m.add_function(wrap_pyfunction!(parse_duration_s, m)?)?;
    m.add_function(wrap_pyfunction!(seconds_to_duration_string, m)?)?;
    m.add_function(wrap_pyfunction!(parse_iso_date, m)?)?;
    m.add_function(wrap_pyfunction!(parse_iso_time, m)?)?;
    m.add_function(wrap_pyfunction!(parse_datetime, m)?)?;
    m.add_function(wrap_pyfunction!(parse_iso_duration, m)?)?;
    m.add_function(wrap_pyfunction!(duration_isoformat, m)?)?;
    m.add_function(wrap_pyfunction!(timezone_from_name, m)?)?;
    m.add_function(wrap_pyfunction!(to_snake_case, m)?)?;
    m.add_function(wrap_pyfunction!(build_namespaced_name, m)?)?;
    Ok(())
}
