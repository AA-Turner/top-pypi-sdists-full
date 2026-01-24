use pyo3::prelude::*;
/// Wrapper around notify-rust to show desktop notifications
mod capabilities;
mod notification;
mod notification_handle;
mod server_information;
use crate::capabilities::get_capabilities_py;
use crate::notification::PyNotification;
use crate::notification_handle::PyNotificationHandle;
use crate::server_information::{PyServerInformation, get_server_information_py};

#[pymodule]
fn _notify_rs(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_class::<PyNotification>().unwrap();
	m.add_class::<PyNotificationHandle>().unwrap();
	m.add_class::<PyServerInformation>().unwrap();

	let get_server_information = wrap_pyfunction!(get_server_information_py, m)?;
	get_server_information.setattr("__module__", "notify_rs")?;
	m.add_function(get_server_information).unwrap();

	let get_capabilities = wrap_pyfunction!(get_capabilities_py, m)?;
	get_capabilities.setattr("__module__", "notify_rs")?;
	m.add_function(get_capabilities).unwrap();

	m.add("TIMEOUT_NEVER", -2).unwrap();
	m.add("TIMEOUT_DEFAULT", -1).unwrap();
	m.add("URGENCY_LOW", 0).unwrap();
	m.add("URGENCY_NORMAL", 1).unwrap();
	m.add("URGENCY_CRITICAL", 2).unwrap();

	Ok(())
}
