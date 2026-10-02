#![allow(
	unexpected_cfgs,
	unsafe_op_in_unsafe_fn,
	clippy::useless_conversion,
	reason = "pyo3 does this in its macro and we can't fix that"
)]

use ::discord_markdown::{DEFAULT_FUEL, error::Error, node::SpannedNodes, rule::RuleSet};
use pyo3::{
	Bound, PyAny, PyResult, Python, create_exception,
	exceptions::PyException,
	pyfunction, pymodule,
	types::{PyModule, PyModuleMethods},
	wrap_pyfunction,
};
use pythonize::{depythonize, pythonize};

/// Parse markdown content into an AST.
///
/// `fuel` bounds how much work the parse may do before giving up and raising, and defaults to
/// `DEFAULT_FUEL`. See the `fuel` field of the Rust `Options` struct for how to choose a value:
/// the short version is that ordinary content needs a tiny fraction of the default, and lowering
/// it tightens the worst case for adversarial content at the risk of rejecting real content.
#[pyfunction]
#[pyo3(signature = (data, *, allowed_rules=None, fuel=DEFAULT_FUEL))]
fn parse<'py>(
	py: Python<'py>,
	data: &str,
	allowed_rules: Option<&Bound<'py, PyAny>>,
	fuel: u32,
) -> PyResult<Bound<'py, PyAny>> {
	create_exception!(py.module, OutOfFuelException, PyException);

	// TODO: use classes instead of serde
	let allowed_rules = allowed_rules
		.map(depythonize::<RuleSet>)
		.transpose()?
		.unwrap_or_default();
	let data = data.to_owned();

	let result = py
		.allow_threads(|| {
			::discord_markdown::parse::<(), Error<'_>>(
				data.as_str(),
				::discord_markdown::Options {
					allowed_rules,
					fuel,
				},
			)
		})
		.map_err(|err| {
			let msg = err.to_string();

			match err {
				Error::OutOfFuel => OutOfFuelException::new_err(msg),
				Error::Parse(_) => PyException::new_err(msg),
			}
		})?;

	Ok(pythonize(py, &result)?)
}

/// Turn an AST back into markdown.
///
/// Takes the value `parse` returned. The AST cannot reconstruct everything exactly: text is not
/// re-escaped, italics always come back as `_`, and unordered lists always as `* `.
#[pyfunction]
fn unparse(py: Python<'_>, nodes: &Bound<'_, PyAny>) -> PyResult<String> {
	let nodes = depythonize::<SpannedNodes<'static, ()>>(nodes)?;

	Ok(py.allow_threads(|| ::discord_markdown::unparse(&nodes)))
}

#[pymodule]
fn discord_markdown(m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_function(wrap_pyfunction!(parse, m)?)?;
	m.add_function(wrap_pyfunction!(unparse, m)?)?;
	m.add("DEFAULT_FUEL", DEFAULT_FUEL)?;
	Ok(())
}
