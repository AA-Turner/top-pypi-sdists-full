use pyo3::{exceptions::PyRuntimeError, prelude::*};

#[cfg(all(unix, not(target_os = "macos")))]
use notify_rust::get_capabilities;

#[cfg(all(unix, not(target_os = "macos")))]
#[pyfunction(name = "get_capabilities")]
/// Get list of all capabilities of the running notification server.
pub fn get_capabilities_py() -> PyResult<Vec<String>> {
	let capabilities = get_capabilities();
	match capabilities {
		Ok(caps) => Ok(caps),
		Err(e) => Err(PyRuntimeError::new_err(e.to_string())),
	}
}

#[cfg(not(all(unix, not(target_os = "macos"))))]
use pyo3::exceptions::PyNotImplementedError;

#[cfg(not(all(unix, not(target_os = "macos"))))]
#[pyfunction(name = "get_capabilities")]
/// Returns a struct containing ServerInformation.
///
/// This struct contains name, vendor, version and spec_version of the notification server running.
pub fn get_capabilities_py() -> PyResult<Vec<String>> {
	Err(PyNotImplementedError::new_err(
		"Not supported on this platform.",
	))
}
