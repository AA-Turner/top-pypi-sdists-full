use notify_rust::{Timeout, Urgency};
use pyo3::{exceptions::PyValueError, prelude::*};

#[cfg(target_family = "unix")]
use notify_rust::NotificationHandle;

#[cfg(not(target_family = "unix"))]
#[pyclass(name = "NotificationHandle", module = "notify_rs")]
#[repr(transparent)]
#[derive(Debug)]
// A wrapper around a [`NotificationHandle`] that can be converted to and from python with `pyo3`.
/// A handle to a shown notification.
pub struct PyNotificationHandle();

#[cfg(target_family = "unix")]
#[pyclass(name = "NotificationHandle", module = "notify_rs")]
#[repr(transparent)]
#[derive(Debug)]
// A wrapper around a [`NotificationHandle`] that can be converted to and from python with `pyo3`.
/// A handle to a shown notification.
pub struct PyNotificationHandle(pub NotificationHandle);

#[cfg(target_family = "unix")]
impl From<PyNotificationHandle> for NotificationHandle {
	fn from(value: PyNotificationHandle) -> Self {
		value.0
	}
}

// impl PyNotificationHandle {
//     pub(crate) fn new(handle: NotificationHandle) -> Self {
//         PyNotificationHandle {0: handle}
//     }
// }

#[cfg(target_family = "unix")]
#[pymethods]
impl PyNotificationHandle {
	// #[new]
	// pub fn __init__() -> PyResult<Self> {
	//     Ok(PyNotificationHandle::new())
	// }

	// TODO: fn wait_for_action<F>(self, invocation_closure: F)
	// TODO: fn close<'a>(slf: PyRefMut<'a, Self>) {
	// 	slf.0.close();
	// }
	// TODO: fn on_close<A>(self, handler: impl CloseHandler<A>)
	#[cfg(target_os = "linux")]
	#[pyo3(signature = () -> "NotificationHandle")]
	fn update<'a>(mut slf: PyRefMut<'a, Self>) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.update();
		Ok(slf)
	}

	// TODO: macOS
	#[cfg(target_os = "linux")]
	#[pyo3(signature = () -> "int")]
	fn id(&self) -> PyResult<u32> {
		Ok(self.0.id())
	}

	/// Filled by default with executable name.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = () -> "str")]
	fn get_appname<'a>(slf: PyRefMut<'a, Self>) -> PyResult<String> {
		Ok(slf.0.appname.clone())
	}

	/// Single line to summarize the content.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = () -> "str")]
	fn get_summary<'a>(slf: PyRefMut<'a, Self>) -> PyResult<String> {
		Ok(slf.0.summary.clone())
	}

	/// Subtitle for macOS
	// #[getter]
	#[pyo3(signature = () -> "str | None")]
	fn get_subtitle<'a>(slf: PyRefMut<'a, Self>) -> PyResult<Option<String>> {
		Ok(slf.0.subtitle.clone())
	}

	/// Multiple lines possible, may support simple markup, check out get_capabilities() -> body-markup and body-hyperlinks.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = () -> "str")]
	fn get_body<'a>(slf: PyRefMut<'a, Self>) -> PyResult<String> {
		Ok(slf.0.body.clone())
	}

	/// Use a ``file://`` URI or a name in an icon theme.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = () -> "str")]
	fn get_icon<'a>(slf: PyRefMut<'a, Self>) -> PyResult<String> {
		Ok(slf.0.icon.clone())
	}

	/// Lifetime of the Notification in ms. Often not respected by server, sorry.
	///
	/// :rtype: :class:`int`
	///
	/// .. latex:clearpage::
	#[pyo3(signature = () -> "int")]
	fn get_timeout<'a>(slf: PyRefMut<'a, Self>) -> PyResult<i32> {
		match slf.0.timeout {
			Timeout::Never => Ok(-2),
			Timeout::Default => Ok(-1),
			_ => Ok(slf.0.timeout.into()),
		}
	}

	/// Overwrite the appname field.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = (appname: "str") -> "NotificationHandle")]
	fn appname<'a>(mut slf: PyRefMut<'a, Self>, appname: &str) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.appname(appname);
		Ok(slf)
	}

	/// Set the summary.
	///
	/// Often acts as title of the notification. For more elaborate content use the body field.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = (summary: "str") -> "NotificationHandle")]
	fn summary<'a>(mut slf: PyRefMut<'a, Self>, summary: &str) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.summary(summary);
		Ok(slf)
	}

	/// Set the subtitle.
	///
	/// This is only useful on macOS; It’s not part of the XDG specification.
	///
	/// :rtype: :class:`str`
	#[pyo3(signature = (subtitle: "str") -> "NotificationHandle")]
	fn subtitle<'a>(mut slf: PyRefMut<'a, Self>, subtitle: &str) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.subtitle(subtitle);
		Ok(slf)
	}

	#[cfg(not(target_os = "macos"))]
	// TODO: path param type
	/// Path to an image to use in the ``image_data`` hint.
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = (path: "str") -> "NotificationHandle")]
	fn image_path<'a>(
		mut slf: PyRefMut<'a, Self>,
		path: std::path::PathBuf,
	) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.image_path(path.to_str().unwrap());
		Ok(slf)
	}

	#[cfg(target_os = "macos")]
	// TODO: path param type
	/// Path to an image to use in the ``image_data`` hint.
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = (path: "str") -> "NotificationHandle")]
	fn image_path<'a>(
		mut slf: PyRefMut<'a, Self>,
		path: std::path::PathBuf,
	) -> PyResult<PyRefMut<'a, Self>> {
		Ok(slf)
	}

	#[pyo3(signature = (name: "str") -> "NotificationHandle")]
	fn sound_name<'a>(mut slf: PyRefMut<'a, Self>, name: &str) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.sound_name(name);
		Ok(slf)
	}

	/// Set the content of the body field.
	///
	/// Multiline textual content of the notification. Each line should be treated as a paragraph. Simple html markup should be supported, depending on the server implementation.
	///
	/// :param body: :class:`str`
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = (body: "str") -> "NotificationHandle")]
	fn body<'a>(mut slf: PyRefMut<'a, Self>, body: &str) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.body(body);
		Ok(slf)
	}

	/// Set the icon field.
	///
	/// You can use common icon names here; usually those in /usr/share/icons can all be used.
	/// You can also use an absolute path to a file.
	///
	/// .. note:: macOS does not have support manually setting the icon
	///
	/// :param icon: :class:`str`
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = (icon: "str") -> "NotificationHandle")]
	fn icon<'a>(
		mut slf: PyRefMut<'a, Self>,
		icon: std::path::PathBuf,
	) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.icon(icon.to_str().unwrap());
		Ok(slf)
	}

	/// Set the icon field automatically.
	///
	/// This looks at your binary’s name and uses it to set the icon.
	///
	/// .. note:: macOS does not have support manually setting the icon
	///
	/// :rtype: :class:`~.Notification`
	///
	/// .. latex:clearpage::
	#[pyo3(signature = () -> "NotificationHandle")]
	fn auto_icon<'a>(mut slf: PyRefMut<'a, Self>) -> PyResult<PyRefMut<'a, Self>> {
		slf.0.auto_icon();
		Ok(slf)
	}

	// TODO: fn hint<'a>(mut slf: PyRefMut<'a, Self>, hint: Hint) -> PyResult<PyRefMut<'a, Self>> {
	// 	self.0.hint(hint);
	// 	Ok(slf)
	// }

	/// Set the timeout.
	///
	/// :param body: :class:`int`
	///
	/// :rtype: :class:`~.Notification`
	///
	/// .. latex:clearpage::
	#[pyo3(signature = (timeout: "int") -> "NotificationHandle")]
	fn timeout<'a>(mut slf: PyRefMut<'a, Self>, timeout: i32) -> PyResult<PyRefMut<'a, Self>> {
		match timeout {
			-1 => slf.0.timeout(Timeout::Default),
			-2 => slf.0.timeout(Timeout::Never),
			_ => {
				if timeout >= 0 {
					slf.0.timeout(timeout)
				} else {
					return Err(PyValueError::new_err(format!(
						"Invalid timeout value {timeout}"
					)));
				}
			}
		};
		Ok(slf)
	}

	#[cfg(target_os = "linux")]
	/// Controls whether the notification is shown to the user while e.g. watching a video.
	///
	/// :param body: :class:`int`
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = (urgency: "int") -> "NotificationHandle")]
	fn urgency<'a>(mut slf: PyRefMut<'a, Self>, urgency: i32) -> PyResult<PyRefMut<'a, Self>> {
		match urgency {
			0 => slf.0.urgency(Urgency::Low),
			1 => slf.0.urgency(Urgency::Normal),
			2 => slf.0.urgency(Urgency::Critical),
			_ => {
				return Err(PyValueError::new_err(format!(
					"Invalid urgency value {urgency}"
				)));
			}
		};

		Ok(slf)
	}

	#[cfg(not(target_os = "linux"))]
	/// Controls whether the notification is shown to the user while e.g. watching a video.
	///
	/// :param body: :class:`int`
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = (urgency: "int") -> "NotificationHandle")]
	fn urgency<'a>(mut slf: PyRefMut<'a, Self>, urgency: i32) -> PyResult<PyRefMut<'a, Self>> {
		Ok(slf)
	}

	/// Finalizes a Notification.
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = () -> "NotificationHandle")]
	fn finalize(slf: PyRef<Self>) -> PyResult<PyRef<Self>> {
		slf.0.finalize();
		Ok(slf)
	}

	#[cfg(target_family = "unix")]
	/// Shows the notification.
	///
	/// On Windows this returns the :class:`~.Notification`;
	/// on Unix and other OSes it returns a :class:`~.NotificationHandle`, which can be used to modify the notification later.
	#[pyo3(signature = () -> "NotificationHandle")]
	fn show(slf: PyRef<Self>) -> PyResult<PyNotificationHandle> {
		match slf.0.show() {
			Err(error) => Err(PyValueError::new_err(error.to_string())),
			Ok(result) => Ok(PyNotificationHandle(result)),
		}
	}

	#[cfg(not(target_family = "unix"))]
	/// Shows the notification.
	///
	/// :rtype: :class:`~.Notification`
	#[pyo3(signature = () -> "Notification")]
	fn show<'a>(mut slf: PyRefMut<'a, Self>) -> PyResult<PyRef<Self>> {
		match slf.0.show() {
			Err(error) => Err(PyValueError::new_err(error.to_string())),
			Ok(_) => Ok(slf),
		}
	}
}
