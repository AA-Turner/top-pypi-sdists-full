use crate::internal::asyncio::get_running_loop;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::PyDict;
use pyo3::{PyTraverseError, PyVisit, intern};

pub struct TaskLocal {
    event_loop: Option<Py<PyAny>>,
    context: Option<Py<PyAny>>,
}
impl TaskLocal {
    pub fn current(py: Python) -> PyResult<Self> {
        static ONCE_CTX_VARS: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

        Ok(TaskLocal {
            event_loop: Some(get_running_loop(py)?.unbind()),
            context: Some(
                ONCE_CTX_VARS
                    .import(py, "contextvars", "copy_context")?
                    .call0()?
                    .unbind(),
            ),
        })
    }

    pub fn event_loop(&self) -> PyResult<&Py<PyAny>> {
        self.event_loop
            .as_ref()
            .ok_or_else(|| PyRuntimeError::new_err("Expected event_loop"))
    }

    pub fn clone_ref(&self, py: Python) -> PyResult<Self> {
        Ok(TaskLocal {
            event_loop: Some(
                self.event_loop
                    .as_ref()
                    .ok_or_else(|| PyRuntimeError::new_err("Expected event_loop"))?
                    .clone_ref(py),
            ),
            context: Some(
                self.context
                    .as_ref()
                    .ok_or_else(|| PyRuntimeError::new_err("Expected context"))?
                    .clone_ref(py),
            ),
        })
    }

    pub fn event_loop_call_soon(&self, callable: &Bound<PyAny>) -> PyResult<()> {
        let py = callable.py();
        let event_loop = self.event_loop()?;
        let kwargs = PyDict::new(py);
        kwargs.set_item(intern!(py, "context"), &self.context)?;
        event_loop.call_method(py, intern!(py, "call_soon_threadsafe"), (callable,), Some(&kwargs))?;
        Ok(())
    }

    // :NOCOV_START
    pub fn __traverse__(&self, visit: &PyVisit<'_>) -> Result<(), PyTraverseError> {
        visit.call(&self.event_loop)?;
        visit.call(&self.context)?;
        Ok(())
    }

    pub fn __clear__(&mut self) {
        self.event_loop = None;
        self.context = None;
    } // :NOCOV_END
}

pub struct OnceTaskLocal(PyOnceLock<TaskLocal>);
impl Default for OnceTaskLocal {
    // :NOCOV_START
    fn default() -> Self {
        Self::new()
    } // :NOCOV_END
}

impl OnceTaskLocal {
    pub const fn new() -> Self {
        OnceTaskLocal(PyOnceLock::new())
    }

    pub fn get_or_current(&self, py: Python) -> PyResult<TaskLocal> {
        self.0.get_or_try_init(py, || TaskLocal::current(py))?.clone_ref(py)
    }

    pub fn clone_ref(&self, py: Python) -> PyResult<Self> {
        let slf = Self::new();
        if let Some(task_local) = self.0.get(py) {
            slf.0
                .set(py, task_local.clone_ref(py)?)
                .map_err(|_| PyRuntimeError::new_err("Expected unset PyOnceLock"))?;
        }
        Ok(slf)
    }
}
