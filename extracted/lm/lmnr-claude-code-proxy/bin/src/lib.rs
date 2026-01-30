mod anthropic;
mod interface;
mod proto;
mod proxy;
#[cfg(feature = "python")]
mod python_interface;
mod server;
mod spans;
mod state;
#[cfg(feature = "typescript")]
pub mod ts_interface;

#[cfg(feature = "python")]
use pyo3::prelude::PyModuleMethods;

#[cfg(feature = "python")]
use python_interface::{run, stop, stop_with_timeout};

/// Python module definition
#[cfg(feature = "python")]
#[pyo3::prelude::pymodule(name = "lmnr_claude_code_proxy")]
fn lmnr_claude_code_proxy(
    m: &pyo3::Bound<'_, pyo3::prelude::PyModule>,
) -> pyo3::prelude::PyResult<()> {
    m.add_function(pyo3::wrap_pyfunction!(run, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(stop, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(stop_with_timeout, m)?)?;
    Ok(())
}

/// TypeScript/NAPI module definition
/// NAPI-RS will automatically use the functions marked with #[napi] from ts_interface
#[cfg(feature = "typescript")]
pub use ts_interface::*;
