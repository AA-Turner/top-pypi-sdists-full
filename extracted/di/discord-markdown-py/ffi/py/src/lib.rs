#![allow(
	unexpected_cfgs,
	unsafe_op_in_unsafe_fn,
	clippy::useless_conversion,
	reason = "pyo3 does this in its macro and we can't fix that"
)]

use ::discord_markdown::{
	DEFAULT_FUEL, Options,
	error::Error,
	node::Blocks,
	syntax::{Syntax, SyntaxSet},
};
use pyo3::{
	Bound, PyAny, PyResult, Python, create_exception,
	exceptions::PyException,
	pyfunction, pymodule,
	types::{PyAnyMethods, PyModule, PyModuleMethods},
	wrap_pyfunction,
};
use pythonize::{depythonize, pythonize};

/// Parse markdown content into an AST.
///
/// `fuel` bounds how much work the parse may do before giving up and raising, and defaults to
/// `DEFAULT_FUEL`. See the `fuel` field of the Rust `Options` struct for how to choose a value:
/// the short version is that ordinary content needs a tiny fraction of the default, and lowering
/// it tightens the worst case for adversarial content at the risk of rejecting real content.
///
/// `flags` selects the syntax to parse, as members of the `Syntax` flag enum, and defaults to
/// `Syntax.ALL`, which `0` also means. Bits no syntax uses are ignored.
#[pyfunction]
#[pyo3(signature = (data, *, flags=Options::ALL_FLAGS, fuel=DEFAULT_FUEL))]
fn parse<'py>(py: Python<'py>, data: &str, flags: u32, fuel: u32) -> PyResult<Bound<'py, PyAny>> {
	create_exception!(py.module, OutOfFuelException, PyException);

	let data = data.to_owned();

	let result = py
		.allow_threads(|| {
			::discord_markdown::parse::<(), Error<'_>>(
				data.as_str(),
				Options::from_flags(flags, fuel),
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
	let nodes = depythonize::<Blocks<'static, ()>>(nodes)?;

	Ok(py.allow_threads(|| ::discord_markdown::unparse(&nodes)))
}

#[pymodule]
fn discord_markdown(m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_function(wrap_pyfunction!(parse, m)?)?;
	m.add_function(wrap_pyfunction!(unparse, m)?)?;
	m.add("DEFAULT_FUEL", DEFAULT_FUEL)?;
	m.add("Syntax", syntax_flag(m.py())?)?;
	Ok(())
}

/// The `Syntax` flag enum: a member per syntax, named by [`Syntax::flag_name`], plus `DEV_LINKS`,
/// the groups in [`Syntax::GROUPS`], and `ALL`.
fn syntax_flag(py: Python<'_>) -> PyResult<Bound<'_, PyAny>> {
	let members = SyntaxSet::all()
		.iter()
		.map(|syntax| (syntax.flag_name(), SyntaxSet::from(syntax).as_u32()))
		.chain([("DEV_LINKS".to_owned(), Options::DEV_LINKS)])
		.chain(Syntax::GROUPS.map(|(name, set)| (name.to_owned(), set.as_u32())))
		.chain([("ALL".to_owned(), Options::ALL_FLAGS)])
		.collect::<Vec<_>>();

	py.import_bound("enum")?
		.getattr("IntFlag")?
		.call1(("Syntax", members))
}
