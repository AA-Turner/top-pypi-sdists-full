use pyo3::{Python, prelude::*};
use pyo3_stub_gen::derive::gen_stub_pyfunction;
use statsig_rust::statsig_global::StatsigGlobal;
use std::cell::Cell;
use std::sync::atomic::{AtomicBool, Ordering};

lazy_static::lazy_static! {
    static ref PYTHON_RUNNING: AtomicBool = AtomicBool::new(true);
}

#[gen_stub_pyfunction(module = "statsig_python_core")]
#[pyfunction]
pub fn notify_python_shutdown() {
    PYTHON_RUNNING.store(false, Ordering::SeqCst);
}

#[gen_stub_pyfunction(module = "statsig_python_core")]
#[pyfunction]
pub fn notify_python_fork(py: Python<'_>) {
    // Reset drops the shared Tokio runtime and may wait for workers that are
    // finishing Python callbacks. Let those workers acquire the GIL before
    // the fork proceeds.
    py.detach(StatsigGlobal::reset);
}

thread_local! {
    static IN_DETACHED_GATE_CHECK: Cell<bool> = const { Cell::new(false) };
}

struct GateCheckScope(bool);

impl GateCheckScope {
    fn enter(detached: bool) -> Self {
        Self(IN_DETACHED_GATE_CHECK.replace(detached))
    }
}

impl Drop for GateCheckScope {
    fn drop(&mut self) {
        IN_DETACHED_GATE_CHECK.set(self.0);
    }
}

pub struct SafeGil;

impl SafeGil {
    pub fn detach_for_gate_check(
        py: Python<'_>,
        remote_id_lists: bool,
        check: impl Send + FnOnce() -> bool,
    ) -> bool {
        if !remote_id_lists {
            return py.detach(check);
        }
        py.detach(|| {
            let _scope = GateCheckScope::enter(true);
            check()
        })
    }

    pub fn wait_for_membership(wait: &mut (dyn FnMut() + Send)) {
        if IN_DETACHED_GATE_CHECK.get() {
            wait();
            return;
        }
        Self::run(|py| match py {
            Some(py) => py.detach(wait),
            None => wait(),
        });
    }

    pub fn run<F, R>(f: F) -> R
    where
        F: for<'py> FnOnce(Option<Python<'py>>) -> R,
    {
        if !PYTHON_RUNNING.load(Ordering::SeqCst) {
            log_gil_unavailable();

            return f(None);
        }

        // A Python callback can start a new evaluation on this same thread.
        let _scope = IN_DETACHED_GATE_CHECK
            .get()
            .then(|| GateCheckScope::enter(false));
        Python::attach(move |py| f(Some(py)))
    }
}

fn log_gil_unavailable() {
    // we do not use the logging framework here as it may recursively try access the GIL
    eprintln!("StatsigSafeGil: GIL Unavailable. Python interpreter is shutting down");
}
