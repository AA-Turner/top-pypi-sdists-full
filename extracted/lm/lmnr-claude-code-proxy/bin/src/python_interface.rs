use crate::interface::{DEFAULT_PORT, DEFAULT_TIMEOUT};

/// Run the proxy server in a background thread
#[pyo3::pyfunction]
#[pyo3(signature = (target_url, port=DEFAULT_PORT))]
pub fn run(target_url: String, port: u16) -> pyo3::prelude::PyResult<()> {
    crate::interface::run(target_url, port)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
}

/// Stop the proxy server on a specific port
/// Uses a default timeout of 4 seconds for graceful shutdown
#[pyo3::pyfunction]
#[pyo3(signature = (port=DEFAULT_PORT))]
#[deprecated(since = "0.1.12", note = "Use stop_with_timeout instead")]
pub fn stop(port: u16) -> pyo3::prelude::PyResult<()> {
    crate::interface::stop(port).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
}

/// Stop the proxy server on a specific port with a timeout
/// If the server doesn't stop within the timeout, it will be forcefully terminated
#[pyo3::pyfunction]
#[pyo3(signature = (port=DEFAULT_PORT, timeout_secs=DEFAULT_TIMEOUT))]
pub fn stop_with_timeout(port: u16, timeout_secs: u64) -> pyo3::prelude::PyResult<()> {
    crate::interface::stop_with_timeout(port, timeout_secs)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
}
