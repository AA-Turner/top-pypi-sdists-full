mod index;
mod storage;
mod metrics;
mod errors;
mod concurrency;

use pyo3::prelude::*;
use index::AnnIndex;
use metrics::Distance;
use concurrency::ThreadSafeAnnIndex;

/// The Python module declaration.
#[pymodule]
fn rust_annie(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<AnnIndex>()?;
    m.add_class::<Distance>()?;
    m.add_class::<ThreadSafeAnnIndex>()?;
    Ok(())
}
