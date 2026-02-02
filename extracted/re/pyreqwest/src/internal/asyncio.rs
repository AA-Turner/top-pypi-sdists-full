use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::{Bound, Py, PyAny, PyResult, Python, intern};

pub fn get_running_loop(py: Python) -> PyResult<Bound<PyAny>> {
    static GET_EV_LOOP: PyOnceLock<Py<PyAny>> = PyOnceLock::new();
    GET_EV_LOOP.import(py, "asyncio", "get_running_loop")?.call0()
}

pub fn is_async_callable(obj: &Bound<PyAny>) -> PyResult<bool> {
    if iscoroutinefunction(obj)? {
        return Ok(true);
    }
    if obj.hasattr(intern!(obj.py(), "__call__"))? {
        return iscoroutinefunction(&obj.getattr(intern!(obj.py(), "__call__"))?);
    }
    Ok(false) // :NOCOV
}

fn iscoroutinefunction(obj: &Bound<PyAny>) -> PyResult<bool> {
    static IS_CORO_FUNC: PyOnceLock<Py<PyAny>> = PyOnceLock::new();
    if !obj.is_callable() {
        return Err(PyValueError::new_err("Expected a callable"));
    }
    IS_CORO_FUNC
        .import(obj.py(), "inspect", "iscoroutinefunction")?
        .call1((obj,))?
        .extract()
}
