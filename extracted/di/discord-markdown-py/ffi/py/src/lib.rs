#![allow(
	unsafe_op_in_unsafe_fn,
	clippy::useless_conversion,
	reason = "pyo3 does this in its macro and we can't fix that"
)]

use std::sync::{
	Arc,
	atomic::{AtomicBool, Ordering},
};

use ::discord_markdown::rule::RuleSet;
use pyo3::{
	Bound, PyAny, PyResult, Python,
	exceptions::PyException,
	pyclass, pyfunction, pymethods, pymodule,
	types::{PyModule, PyModuleMethods},
	wrap_pyfunction,
};
use pythonize::{depythonize, pythonize};

#[pyclass]
struct CancelToken(Arc<AtomicBool>);

#[pymethods]
impl CancelToken {
	#[new]
	fn new() -> Self {
		Self(Arc::new(AtomicBool::new(false)))
	}

	fn cancel(&self) {
		self.0.store(true, Ordering::Relaxed);
	}

	#[getter]
	fn cancelled(&self) -> bool {
		self.0.load(Ordering::Relaxed)
	}
}

#[pyfunction]
#[pyo3(signature = (data, *, allowed_rules=None, cancel_token=None))]
fn parse<'py>(
	py: Python<'py>,
	data: &str,
	allowed_rules: Option<&Bound<'py, PyAny>>,
	cancel_token: Option<&CancelToken>,
) -> PyResult<Bound<'py, PyAny>> {
	// TODO: use classes instead of serde
	let allowed_rules = allowed_rules
		.map(depythonize::<RuleSet>)
		.transpose()?
		.unwrap_or_default();
	let cancelled = cancel_token.map_or_else(
		|| Arc::new(AtomicBool::new(false)),
		|token| Arc::clone(&token.0),
	);
	let data = data.to_owned();

	let result = py
		.allow_threads(|| {
			::discord_markdown::parse::<(), nom::error::Error<_>>(
				data.as_str(),
				::discord_markdown::Options {
					allowed_rules,
					cancelled,
				},
			)
		})
		.map_err(|err| PyException::new_err(err.to_string()))?;

	Ok(pythonize(py, &result)?)
}

#[pymodule]
fn discord_markdown(m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_function(wrap_pyfunction!(parse, m)?)?;
	m.add_class::<CancelToken>()?;
	Ok(())
}
