use pyo3::{exceptions::PyRuntimeError, intern, prelude::*, types::PyDict};

#[pyclass(name = "ServerInformation", module = "notify_rs")]
#[derive(Debug)]
/// Return value of :func:`~.get_server_information()`.
pub struct PyServerInformation {
	#[pyo3(get, set)]
	/// The product name of the server.
	pub name: String,

	#[pyo3(get, set)]
	/// The vendor name.
	pub vendor: String,

	#[pyo3(get, set)]
	/// The server's version string.
	pub version: String,

	#[pyo3(get, set)]
	/// The specification version the server is compliant with.
	pub spec_version: String,
}

#[pymethods]
impl PyServerInformation {
	#[classattr]
	pub fn __annotations__(py: Python<'_>) -> PyResult<Py<PyAny>> {
		let builtins = PyModule::import(py, "builtins")?;
		let t = builtins.getattr(intern!(py, "int"))?;
		let dict = PyDict::new(py);
		dict.set_item("name", &t)?;
		dict.set_item("vendor", &t)?;
		dict.set_item("version", &t)?;
		dict.set_item("spec_version", &t)?;
		Ok(dict.into())
	}
}

#[cfg(all(unix, not(target_os = "macos")))]
use notify_rust::get_server_information;

#[cfg(all(unix, not(target_os = "macos")))]
#[pyfunction(name = "get_server_information")]
/// Returns a struct containing ServerInformation.
///
/// This struct contains name, vendor, version and spec_version of the notification server running.
pub fn get_server_information_py() -> PyResult<PyServerInformation> {
	let server_information = get_server_information();
	match server_information {
		Ok(info) => Ok(PyServerInformation {
			name: info.name,
			vendor: info.vendor,
			version: info.version,
			spec_version: info.spec_version,
		}),
		Err(e) => Err(PyRuntimeError::new_err(e.to_string())),
	}
}

#[cfg(not(all(unix, not(target_os = "macos"))))]
use pyo3::exceptions::PyNotImplementedError;

#[cfg(not(all(unix, not(target_os = "macos"))))]
#[pyfunction(name = "get_server_information")]
/// Returns a struct containing ServerInformation.
///
/// This struct contains name, vendor, version and spec_version of the notification server running.
pub fn get_server_information_py() -> PyResult<PyServerInformation> {
	Err(PyNotImplementedError::new_err(
		"Not supported on this platform.",
	))
}
