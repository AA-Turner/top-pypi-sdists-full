pub use chalk_ast as ast;
pub use chalk_ast::*;
pub use chalk_ignore as ignore;
pub use chalk_project as project;
pub use chalk_proto as proto;
pub use chalk_utils::{duration, namespace};

// ---------------------------------------------------------------------------
// PyO3 Python bindings (gated behind "python" feature)
// ---------------------------------------------------------------------------

#[cfg(feature = "python")]
use std::collections::HashMap;
#[cfg(feature = "python")]
use std::sync::Arc;

#[cfg(feature = "python")]
use pyo3::exceptions::{PyIOError, PyValueError};
#[cfg(feature = "python")]
use pyo3::prelude::*;

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
    m.add_function(wrap_pyfunction!(to_snake_case, m)?)?;
    m.add_function(wrap_pyfunction!(build_namespaced_name, m)?)?;
    Ok(())
}
