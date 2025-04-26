#[cfg(not(PyPy))]
#[path = ""]
mod _kolo {
    use pyo3::exceptions::PyTypeError;
    use pyo3::ffi;
    use pyo3::intern;
    use pyo3::prelude::*;
    use pyo3::types::PyDict;
    use pyo3::types::PyTuple;
    use std::os::raw::c_int;
    use std::ptr;

    mod config;
    mod filters;
    mod monitoring;
    mod plugins;
    mod profiler;
    mod utils;

    #[pyfunction]
    /// register_profiler is called from Python to configure profiling to use the Rust
    /// implementation
    ///
    /// The `profiler` argument is an instance of the `KoloProfiler` class implemented in
    /// `src/kolo/profiler.py`. We pass this to the `KoloProfiler::new_from_python` method to
    /// create an instance of the Rust profiler.
    ///
    /// The `KoloProfiler` struct is registered with Python via `PyEval_SetProfile`. If
    /// `use_threading` is `true` we also use `threading.setprofile` with the
    /// `KoloProfiler::register_threading_profiler` callback to register on all threads.
    fn register_profiler(profiler: PyObject) -> Result<(), PyErr> {
        Python::with_gil(|py| {
            let py_profiler = profiler.bind(py);
            if !py_profiler.is_callable() {
                return Err(PyTypeError::new_err("profiler object is not callable"));
            }

            let rust_profiler = profiler::KoloProfiler::new_from_python(py, py_profiler)?;

            // Convert the Rust struct into a Python object the Python interpreter can handle.
            let py_rust_profiler = rust_profiler.into_py(py);

            // Increment the reference count of our profiler as a Python object so we can pass it
            // to both `PyEval_SetProfile` and `threading.setprofile`.
            let py_rust_profiler_2 = py_rust_profiler.bind(py).clone().unbind();

            // Store the Rust profiler on the Python profiler, so methods on the Python profiler
            // can delegate to the Rust profiler. See `Enabled.__exit__` and
            // `KoloProfiler.save()`. This is perhaps a bit convoluted - we could
            // instead change so the Rust profiler is stored directly on `Enabled`.
            py_profiler.setattr("rust_profiler", &py_rust_profiler)?;

            // Safety:
            //
            // PyEval_SetProfile takes two arguments:
            //  * trace_func: Option<Py_tracefunc>
            //  * arg1:       *mut PyObject
            //
            // `profile_callback` matches the signature of a `Py_tracefunc`, so we only
            // need to wrap it in `Some`.
            // `py_rust_profiler.into_ptr()` is a pointer to our Rust profiler
            // instance as a Python object.
            //
            // We must also hold the GIL, which we explicitly do above.
            //
            // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
            // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
            unsafe {
                ffi::PyEval_SetProfile(
                    Some(profiler::profile_callback),
                    py_rust_profiler.into_ptr(),
                );
            }
            let config = py_profiler.getattr(intern!(py, "config"))?;
            let use_threading = match config.get_item("threading") {
                Ok(threading) => threading.extract::<bool>().unwrap_or(false),
                Err(_) => false,
            };
            if use_threading {
                let threading = PyModule::import_bound(py, "threading")?;
                let args =
                    PyTuple::new_bound(
                        py,
                        [py_rust_profiler_2
                            .getattr(py, intern!(py, "register_threading_profiler"))?],
                    );
                threading.call_method1("setprofile", args)?;
            }

            Ok(())
        })
    }

    #[pyfunction]
    #[pyo3(signature = (db_path, config, source, one_trace_per_test, name=None))]
    fn register_monitor(
        db_path: String,
        config: &Bound<'_, PyDict>,
        source: String,
        one_trace_per_test: bool,
        name: Option<String>,
    ) -> Result<monitoring::KoloMonitor, PyErr> {
        monitoring::KoloMonitor::new(db_path, config, source, one_trace_per_test, name)
    }

    // Safety:
    //
    // We match the type signature of `Py_tracefunc`.
    //
    // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/type.Py_tracefunc.html
    extern "C" fn noop_profile(
        _obj: *mut ffi::PyObject,
        _frame: *mut ffi::PyFrameObject,
        _what: c_int,
        _arg: *mut ffi::PyObject,
    ) -> c_int {
        0
    }

    #[pyfunction]
    /// Register a minimal profiler for comparison purposes in benchmarking
    fn register_noop_profiler() {
        // Safety:
        //
        // PyEval_SetProfile takes two arguments:
        //  * trace_func: Option<Py_tracefunc>
        //  * arg1:       *mut PyObject
        //
        // `noop_profile` matches the signature of a `Py_tracefunc`, so
        // we only need to wrap it in `Some`.
        // `arg1` can accept a NULL pointer, so that's what we pass.
        //
        // PyEval_SetProfile also requires we hold the GIL, so we wrap the
        // `unsafe` block in `Python::with_gil`.
        //
        // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
        // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
        Python::with_gil(|_py| unsafe {
            ffi::PyEval_SetProfile(Some(noop_profile), ptr::null_mut());
        })
    }

    #[pymodule]
    mod _kolo {
        #[pymodule_export]
        use super::{register_monitor, register_noop_profiler, register_profiler};
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use pyo3::types::PyType;

        #[test]
        fn test_register_profiler_uncallable() {
            pyo3::prepare_freethreaded_python();

            Python::with_gil(|py| {
                let invalid: PyObject = PyTuple::empty_bound(py).into();
                let pyerr = register_profiler(invalid).unwrap_err();

                assert!(pyerr
                    .get_type_bound(py)
                    .is(&PyType::new_bound::<PyTypeError>(py)));
                assert_eq!(
                    pyerr.value_bound(py).to_string(),
                    "profiler object is not callable"
                );
            });
        }
    }
}
