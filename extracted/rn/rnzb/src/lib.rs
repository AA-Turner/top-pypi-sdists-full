mod exception;
mod file;
mod meta;
mod nzb;
mod repr;
mod segment;
mod tuple;

use crate::exception::InvalidNzbError;
use crate::file::File;
use crate::meta::Meta;
use crate::nzb::Nzb;
use crate::segment::Segment;
use pyo3::prelude::*;

#[pymodule(gil_used = false)]
fn rnzb(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Nzb>()?;
    m.add_class::<Meta>()?;
    m.add_class::<File>()?;
    m.add_class::<Segment>()?;
    m.add("InvalidNzbError", py.get_type::<InvalidNzbError>())?;
    m.add(
        "__all__",
        ("File", "InvalidNzbError", "Meta", "Nzb", "Segment"),
    )?;
    Ok(())
}
