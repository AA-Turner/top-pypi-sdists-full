#[cfg(not(PyPy))]
#[path = ""]
mod _kolo {
    use pyo3::exceptions::PyTypeError;
    use pyo3::ffi;
    use pyo3::intern;
    use pyo3::prelude::*;
    #[cfg(Py_GIL_DISABLED)]
    use pyo3::types::PyList;
    use pyo3::types::PyTuple;
    use pyo3::types::{PyBytes, PyDict};
    use std::os::raw::c_int;
    use std::ptr;

    mod config;
    mod filters;
    mod idle_monitor;
    mod monitoring;
    mod plugins;
    mod profiler;
    mod thread_hooks;
    mod trace_container;
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
    fn register_profiler(profiler: Py<PyAny>) -> Result<(), PyErr> {
        Python::attach(|py| {
            let py_profiler = profiler.bind(py);
            if !py_profiler.is_callable() {
                return Err(PyTypeError::new_err("profiler object is not callable"));
            }

            let rust_profiler = profiler::KoloProfiler::new_from_python(py, py_profiler)?;

            // Convert the Rust struct into a Python object the Python interpreter can handle.
            let py_rust_profiler = Bound::new(py, rust_profiler)?.into_any().unbind();

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
                let threading = PyModule::import(py, "threading")?;
                let args =
                    PyTuple::new(
                        py,
                        [py_rust_profiler_2
                            .getattr(py, intern!(py, "register_threading_profiler"))?],
                    )?;
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

    #[pyfunction]
    #[pyo3(signature = (value, lightweight_repr=false))]
    /// Encode `value` with the native serializer used for traced frames.
    /// Exposed so tests can compare it with `kolo.serialize.dump_msgpack`.
    fn _native_dump_msgpack<'py>(
        value: &Bound<'py, PyAny>,
        lightweight_repr: bool,
    ) -> Result<Bound<'py, PyBytes>, PyErr> {
        let py = value.py();
        let encoded = utils::Serializer::new(py)?.dump_msgpack(py, value, lightweight_repr)?;
        Ok(PyBytes::new(py, &encoded))
    }

    #[pyfunction]
    /// Exact lists and dicts reachable from `value` through exact lists and
    /// dict values, counting repeats, stopping at `limit`. Runs no Python
    /// code. `kolo.serialize` uses it to skip replaying the shared-reference
    /// rule for values too small to start tracking, once per Python-backend
    /// frame, so it walks borrowed pointers without touching refcounts.
    fn _count_plain_containers(value: &Bound<'_, PyAny>, limit: usize) -> usize {
        #[cfg(not(Py_GIL_DISABLED))]
        // Safety: the GIL is held and nothing here runs Python code, so no
        // container reachable from `value` can change or be freed meanwhile.
        unsafe {
            count_plain_containers_borrowed(value.as_ptr(), limit)
        }
        #[cfg(Py_GIL_DISABLED)]
        {
            fn is_plain(item: &Bound<'_, PyAny>) -> bool {
                item.is_exact_instance_of::<PyList>() || item.is_exact_instance_of::<PyDict>()
            }
            let mut pending = vec![value.clone()];
            let mut count: usize = 0;
            // Every pending container counts once popped: stop as soon as
            // they reach the limit, so a wide or cyclic high-fanout value
            // never grows the queue past it.
            while let Some(container) = pending.pop() {
                if let Ok(list) = container.cast_exact::<PyList>() {
                    count += 1;
                    for item in list.iter() {
                        if is_plain(&item) {
                            pending.push(item);
                            if count.saturating_add(pending.len()) >= limit {
                                return limit.max(count);
                            }
                        }
                    }
                } else if let Ok(dict) = container.cast_exact::<PyDict>() {
                    count += 1;
                    for (_, item) in dict.iter() {
                        if is_plain(&item) {
                            pending.push(item);
                            if count.saturating_add(pending.len()) >= limit {
                                return limit.max(count);
                            }
                        }
                    }
                }
                if count.saturating_add(pending.len()) >= limit {
                    return limit.max(count);
                }
            }
            count
        }
    }

    /// `_count_plain_containers` over borrowed pointers.
    ///
    /// # Safety
    /// `root` is a live object, the GIL is held, and no Python code may run
    /// while this walks.
    #[cfg(not(Py_GIL_DISABLED))]
    unsafe fn count_plain_containers_borrowed(root: *mut ffi::PyObject, limit: usize) -> usize {
        let list_type = ptr::addr_of_mut!(ffi::PyList_Type);
        let dict_type = ptr::addr_of_mut!(ffi::PyDict_Type);
        let is_plain = |object: *mut ffi::PyObject| {
            let object_type = ffi::Py_TYPE(object);
            object_type == list_type || object_type == dict_type
        };
        if !is_plain(root) {
            return 0;
        }
        // Frames rarely hold more than a few nested containers at once, so
        // the pending stack only allocates past this.
        const INLINE: usize = 32;
        struct Pending {
            inline: [*mut ffi::PyObject; INLINE],
            inline_len: usize,
            spill: Vec<*mut ffi::PyObject>,
        }
        impl Pending {
            fn push(&mut self, object: *mut ffi::PyObject) {
                if self.inline_len < INLINE {
                    self.inline[self.inline_len] = object;
                    self.inline_len += 1;
                } else {
                    self.spill.push(object);
                }
            }
            fn len(&self) -> usize {
                self.inline_len + self.spill.len()
            }
            fn pop(&mut self) -> Option<*mut ffi::PyObject> {
                if let Some(object) = self.spill.pop() {
                    return Some(object);
                }
                if self.inline_len == 0 {
                    return None;
                }
                self.inline_len -= 1;
                Some(self.inline[self.inline_len])
            }
        }
        let mut pending = Pending {
            inline: [ptr::null_mut(); INLINE],
            inline_len: 0,
            spill: Vec::new(),
        };
        pending.push(root);
        let mut count = 0;
        while let Some(container) = pending.pop() {
            count += 1;
            if count >= limit {
                break;
            }
            // Every pending container counts once popped: stop as soon as
            // they reach the limit, so a cyclic high-fanout value cannot
            // grow the queue.
            if ffi::Py_TYPE(container) == list_type {
                for index in 0..ffi::PyList_GET_SIZE(container) {
                    let item = ffi::PyList_GET_ITEM(container, index);
                    if is_plain(item) {
                        if count + pending.len() + 1 >= limit {
                            return limit;
                        }
                        pending.push(item);
                    }
                }
            } else {
                let mut position = 0;
                let mut key = ptr::null_mut();
                let mut item = ptr::null_mut();
                while ffi::PyDict_Next(container, &mut position, &mut key, &mut item) != 0 {
                    if is_plain(item) {
                        if count + pending.len() + 1 >= limit {
                            return limit;
                        }
                        pending.push(item);
                    }
                }
            }
        }
        count
    }

    #[pyfunction]
    #[pyo3(signature = (enabled=None, verify=None, stats=None))]
    /// Override `KOLO_REPR_REUSE`, `KOLO_REPR_REUSE_VERIFY` and
    /// `KOLO_REPR_REUSE_STATS` for cross-event repr reuse. Reuse disabled by
    /// `KOLO_REPR_REUSE=0` when `kolo._kolo` was imported cannot be enabled
    /// here (its startup checks only run during that import).
    fn _repr_reuse_configure(enabled: Option<bool>, verify: Option<bool>, stats: Option<bool>) {
        utils::repr_reuse_configure(enabled, verify, stats)
    }

    #[pyfunction]
    #[pyo3(signature = (reset=false))]
    /// Counters of cross-event repr reuse (timings need `stats=True`).
    fn _repr_reuse_stats(py: Python<'_>, reset: bool) -> PyResult<Bound<'_, PyDict>> {
        utils::repr_reuse_stats(py, reset)
    }

    #[pyfunction]
    /// Whether this thread is inside a native encode (see the Django query
    /// guard in `kolo.serialize`).
    fn _native_encode_in_progress() -> bool {
        utils::native_encode_in_progress()
    }

    #[pyfunction]
    fn writer_circuit_open() -> bool {
        trace_container::writer_circuit_open()
    }

    /// Mark (or unmark) the calling thread as one of Kolo's own background
    /// workers, returning the previous value. The mark is per OS thread and
    /// dies with it.
    ///
    /// `sys.monitoring` is interpreter-global, so a save/emit/upload worker
    /// left over from one trace keeps running while the next trace records.
    /// Marked threads are never recorded by any Kolo monitor or profiler: the
    /// mark lives in the per-thread hook state every callback already reads
    /// first, so excluding workers costs nothing extra.
    #[pyfunction]
    fn set_current_thread_kolo_worker(value: bool) -> bool {
        thread_hooks::set(thread_hooks::WORKER, value)
    }

    /// Forget the calling thread's worker mark and suspension. Only for the
    /// one thread of a forked child: whatever it was in the parent, it is now
    /// the child's main thread, which Kolo must be able to trace.
    /// Returns whether the thread was marked as a worker.
    #[pyfunction]
    fn _reset_thread_hooks_after_fork() -> bool {
        thread_hooks::set(thread_hooks::SUSPENDED, false);
        thread_hooks::set(thread_hooks::WORKER, false)
    }

    /// The calling thread's hook state byte (see `thread_hooks`), so tests
    /// can check that no mark or suspension leaks onto a thread.
    #[pyfunction]
    fn _current_thread_hook_state() -> u8 {
        thread_hooks::get()
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
        // `unsafe` block in `Python::attach`.
        //
        // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
        // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
        Python::attach(|_py| unsafe {
            ffi::PyEval_SetProfile(Some(noop_profile), ptr::null_mut());
        })
    }

    // PyO3 0.28 flipped the default to gil_used = false. Keep the GIL-requiring
    // declaration we had before: value serialization iterates user containers
    // without a critical section, so concurrent mutation on a free-threaded
    // build can panic mid-capture.
    #[pymodule(gil_used = true)]
    mod _kolo {
        #[pymodule_export]
        use super::idle_monitor::{kolo_tool_is_idle, take_idle_monitor, IdleMonitor};
        #[pymodule_export]
        use super::monitoring::KoloMonitor;
        #[pymodule_export]
        use super::{
            _count_plain_containers, _current_thread_hook_state, _native_dump_msgpack,
            _native_encode_in_progress, _repr_reuse_configure, _repr_reuse_stats,
            _reset_thread_hooks_after_fork, register_monitor, register_noop_profiler,
            register_profiler, set_current_thread_kolo_worker, writer_circuit_open,
        };

        #[pymodule_init]
        fn init(module: &pyo3::Bound<'_, pyo3::types::PyModule>) -> pyo3::PyResult<()> {
            super::utils::repr_reuse_preload(module.py())
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use pyo3::types::PyType;

        #[test]
        fn test_register_profiler_uncallable() {
            Python::initialize();

            Python::attach(|py| {
                let invalid: Py<PyAny> = PyTuple::empty(py).into();
                let pyerr = register_profiler(invalid).unwrap_err();

                assert!(pyerr.get_type(py).is(&PyType::new::<PyTypeError>(py)));
                assert_eq!(
                    pyerr.value(py).to_string(),
                    "profiler object is not callable"
                );
            });
        }
    }
}
