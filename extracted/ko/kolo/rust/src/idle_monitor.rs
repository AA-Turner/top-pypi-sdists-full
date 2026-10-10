use bstr::Finder;
use hashbrown::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyCode, PyModule};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex, MutexGuard};

use super::filters;
use super::plugins::PluginProcessor;
use super::thread_hooks;
use super::utils;

/// How Kolo's sys.monitoring tool behaves between trace sessions.
///
/// Re-arming the tool for every session re-instruments every code object the
/// session runs, and again when it is disarmed, and forgets which locations
/// were disabled, so each session starts by refiring once at every excluded
/// location. Instead the tool stays armed, and outside a session its
/// callbacks disable every location that fires, so idle code stops paying
/// for monitoring after its first event.
///
/// A disabled location stays disabled for the next session. That is only
/// sound for locations the next session would itself disable: code its
/// filters statically exclude, with no plugin candidate for its filename.
/// Code a session may record (user code, mostly) is left enabled, because
/// callers often run a little of it around every session, e.g. the function
/// that enters and exits `kolo.enable()`. Only when such code keeps firing
/// between two sessions is it disabled too, which marks the filter dirty: the
/// next session then restarts events, as every session did before.
///
/// `idle_event` never releases the GIL: it calls no Python code, and its
/// mutex is never contended while the GIL is held. A session can therefore
/// start or end between any two idle callbacks, but never during one.
pub struct IdleFilter {
    include_frames: filters::Finders,
    ignore_frames: filters::Finders,
    processor_filenames: HashMap<String, Vec<Finder<'static>>>,
    disable: Py<PyAny>,
    dirty: AtomicBool,
    /// Events per recordable code object, keyed by address. Only recordable
    /// code is counted, and every outcome for a counted address (leave
    /// enabled, or disable and mark dirty) is sound for any code object, so a
    /// reused address is harmless and the code need not be kept alive.
    recordable_events: Mutex<HashMap<usize, u32>>,
    /// Set once an idle callback panicked, so it is reported only once.
    panicked: AtomicBool,
}

/// Events a recordable code object may fire between two sessions before its
/// locations are disabled and the next session has to restart events.
const RECORDABLE_EVENTS_BEFORE_DISABLE: u32 = 64;
/// Distinct recordable code objects tracked between two sessions. Beyond this
/// a new one is disabled straight away, marking the filter dirty.
const MAX_RECORDABLE_CODE_OBJECTS: usize = 4096;

const CALLBACK_EVENTS: [(&str, &str); 6] = [
    ("PY_START", "monitor_pystart"),
    ("PY_RETURN", "monitor_pyreturn"),
    ("PY_UNWIND", "monitor_pyunwind"),
    ("PY_RESUME", "monitor_pyresume"),
    ("PY_YIELD", "monitor_pyyield"),
    ("PY_THROW", "monitor_pythrow"),
];

/// Register `callbacks`' monitoring methods for Kolo's tool; events without
/// a method get no callback.
///
/// `register_callback` runs audit hooks, so other threads can run between
/// the six calls. Callers only switch between callbacks that are all idle,
/// which handle every event the same way.
pub fn register_callbacks(callbacks: &Bound<'_, PyAny>, tool_id: u8) -> PyResult<()> {
    let py = callbacks.py();
    let monitoring = PyModule::import(py, "sys")?.getattr("monitoring")?;
    let events = monitoring.getattr("events")?;
    let register = monitoring.getattr("register_callback")?;
    for (event, method) in CALLBACK_EVENTS {
        let callback = match callbacks.hasattr(method)? {
            true => callbacks.getattr(method)?,
            false => py.None().into_bound(py),
        };
        register.call1((tool_id, events.getattr(event)?, callback))?;
    }
    Ok(())
}

/// Release Kolo's tool the way a session without an armed tool is torn
/// down, carrying on past failures so that as much as possible is undone.
///
/// The ID is only freed once every callback is unregistered: before Python
/// 3.14 `free_tool_id` keeps callbacks, so the next owner of the ID would
/// inherit Kolo's. A tool left claimed blocks later sessions loudly instead.
pub fn release_tool(py: Python, tool_id: u8) {
    let Ok(monitoring) = PyModule::import(py, "sys").and_then(|sys| sys.getattr("monitoring"))
    else {
        return;
    };
    let _ = monitoring.call_method1("set_events", (tool_id, 0));
    let mut callbacks_removed = false;
    if let Ok(events) = monitoring.getattr("events") {
        callbacks_removed = true;
        for (event, _method) in CALLBACK_EVENTS {
            let removed = events.getattr(event).and_then(|event| {
                monitoring.call_method1("register_callback", (tool_id, event, py.None()))
            });
            callbacks_removed &= removed.is_ok();
        }
    }
    if callbacks_removed {
        let _ = monitoring.call_method1("free_tool_id", (tool_id,));
    }
    let _ = monitoring.call_method0("restart_events");
}

pub fn restart_events(py: Python) -> PyResult<()> {
    PyModule::import(py, "sys")?
        .getattr("monitoring")?
        .call_method0("restart_events")?;
    Ok(())
}

impl IdleFilter {
    pub fn new(
        include_frames: &filters::Finders,
        ignore_frames: &filters::Finders,
        processors: &HashMap<String, Vec<PluginProcessor>>,
        disable: Py<PyAny>,
    ) -> Self {
        IdleFilter {
            include_frames: include_frames.clone(),
            ignore_frames: ignore_frames.clone(),
            processor_filenames: processors
                .iter()
                .map(|(co_name, processors)| {
                    let finders = processors
                        .iter()
                        .map(|processor| processor.filename_finder().clone())
                        .collect();
                    (co_name.clone(), finders)
                })
                .collect(),
            disable,
            dirty: AtomicBool::new(false),
            recordable_events: Mutex::new(HashMap::new()),
            panicked: AtomicBool::new(false),
        }
    }

    /// Whether both filters make the same static decisions.
    pub fn same_filters(&self, other: &IdleFilter) -> bool {
        self.include_frames.same_fragments(&other.include_frames)
            && self.ignore_frames.same_fragments(&other.ignore_frames)
            && self.processor_filenames.len() == other.processor_filenames.len()
            && self.processor_filenames.iter().all(|(co_name, finders)| {
                other
                    .processor_filenames
                    .get(co_name)
                    .is_some_and(|others| {
                        finders.len() == others.len()
                            && finders
                                .iter()
                                .zip(others)
                                .all(|(finder, other)| finder.needle() == other.needle())
                    })
            })
    }

    /// Whether a location a session may need was disabled since the last
    /// call. Clears the flag.
    pub fn take_dirty(&self) -> bool {
        self.dirty.swap(false, Ordering::AcqRel)
    }

    /// Whether a session with these filters could record or plugin-process
    /// an event for this code object.
    pub(crate) fn session_may_record(&self, code: &Bound<'_, PyCode>) -> PyResult<bool> {
        let py = code.py();
        let filename = code
            .getattr(intern!(py, "co_filename"))?
            .extract::<String>()?;
        // Empty filenames are filtered by inspecting the caller (attrs).
        if filename.is_empty()
            || filters::include_frame(py, &filename, &self.include_frames, &self.ignore_frames)?
        {
            return Ok(true);
        }
        if self.processor_filenames.is_empty() {
            return Ok(false);
        }
        let name = code.getattr(intern!(py, "co_name"))?.extract::<String>()?;
        Ok(self.processor_filenames.get(&name).is_some_and(|finders| {
            finders
                .iter()
                .any(|finder| finder.find(filename.as_bytes()).is_some())
        }))
    }

    /// Handle a PY_START, PY_RETURN, PY_RESUME or PY_YIELD event.
    pub fn idle_event(&self, code: &Bound<'_, PyCode>) -> Py<PyAny> {
        self.guarded(code.py(), || self.unguarded_idle_event(code))
    }

    /// Run an idle callback without letting a Kolo panic escape into user
    /// code. Leaving the location enabled is always sound; marking the filter
    /// dirty makes the next session restart events as before.
    fn guarded(&self, py: Python, callback: impl FnOnce() -> Py<PyAny>) -> Py<PyAny> {
        match catch_unwind(AssertUnwindSafe(callback)) {
            Ok(result) => result,
            Err(payload) => {
                self.dirty.store(true, Ordering::Release);
                if !self.panicked.swap(true, Ordering::Relaxed) {
                    utils::report_panic(py, payload);
                }
                py.None()
            }
        }
    }

    /// The counts stay usable after a panic: each is only ever a hint.
    fn recordable_events(&self) -> MutexGuard<'_, HashMap<usize, u32>> {
        self.recordable_events
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner())
    }

    fn unguarded_idle_event(&self, code: &Bound<'_, PyCode>) -> Py<PyAny> {
        let py = code.py();
        // Kolo's own threads (and save sections) only disable what the
        // filters statically exclude: their activity says nothing about the
        // user code around a session, so it must not count towards disabling
        // recordable code and dirtying the filter.
        let hooks_off = thread_hooks::get() & thread_hooks::OFF != 0;
        let code_id = code.as_ptr() as usize;
        if let Some(events) = self.recordable_events().get_mut(&code_id) {
            if hooks_off {
                return py.None();
            }
            *events += 1;
            if *events <= RECORDABLE_EVENTS_BEFORE_DISABLE {
                return py.None();
            }
            return self.disable_recordable(py);
        }
        match self.session_may_record(code) {
            Ok(false) => self.disable.clone_ref(py),
            Ok(true) if hooks_off => py.None(),
            Ok(true) => {
                let mut recordable_events = self.recordable_events();
                if recordable_events.len() >= MAX_RECORDABLE_CODE_OBJECTS {
                    drop(recordable_events);
                    return self.disable_recordable(py);
                }
                recordable_events.insert(code_id, 1);
                py.None()
            }
            // Leaving the location enabled is always sound.
            Err(_) => py.None(),
        }
    }

    fn disable_recordable(&self, py: Python) -> Py<PyAny> {
        self.dirty.store(true, Ordering::Release);
        self.disable.clone_ref(py)
    }
}

/// The callbacks registered between sessions, sharing the ended session's
/// `IdleFilter` so the monitor itself can be dropped. PY_UNWIND and PY_THROW
/// cannot be disabled, so they get no callback: CPython then skips the call,
/// and unwinding stays almost free without changing the tool's events (which
/// would make every code object re-check its instrumentation).
#[pyclass(module = "kolo._kolo", frozen)]
pub struct IdleMonitor {
    filter: Arc<IdleFilter>,
}

impl IdleMonitor {
    pub fn new(filter: Arc<IdleFilter>) -> Self {
        IdleMonitor { filter }
    }

    pub fn filter(&self) -> &IdleFilter {
        &self.filter
    }
}

/// The idle callbacks while Kolo keeps its tool armed between sessions.
/// Only touched with the GIL held, so the lock is never contended.
static IDLE_MONITOR: Mutex<Option<Py<IdleMonitor>>> = Mutex::new(None);

pub fn set_idle_monitor(idle: Py<IdleMonitor>) {
    *IDLE_MONITOR.lock().expect("idle monitor mutex poisoned") = Some(idle);
}

/// Take over the armed tool's idle callbacks, if Kolo kept it armed.
#[pyfunction]
pub fn take_idle_monitor() -> Option<Py<IdleMonitor>> {
    IDLE_MONITOR
        .lock()
        .expect("idle monitor mutex poisoned")
        .take()
}

/// Whether Kolo holds its tool ID only to stay armed between sessions.
#[pyfunction]
pub fn kolo_tool_is_idle() -> bool {
    IDLE_MONITOR
        .lock()
        .expect("idle monitor mutex poisoned")
        .is_some()
}

#[pymethods]
impl IdleMonitor {
    fn monitor_pystart(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        self.filter.idle_event(code)
    }

    fn monitor_pyresume(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        self.filter.idle_event(code)
    }

    fn monitor_pyreturn(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        _retval: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        self.filter.idle_event(code)
    }

    fn monitor_pyyield(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        _retval: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        self.filter.idle_event(code)
    }
}

#[cfg(test)]
mod tests {
    use super::thread_hooks;
    use super::{IdleFilter, RECORDABLE_EVENTS_BEFORE_DISABLE};
    use crate::_kolo::filters::build_finders;
    use crate::_kolo::plugins::{load_plugin_data_for_test, PluginProcessor};
    use hashbrown::HashMap;
    use pyo3::prelude::*;
    use pyo3::types::{PyCode, PyCodeInput, PyDict, PyList};
    use std::ffi::CString;

    fn processors(py: Python, path_fragment: &str) -> HashMap<String, Vec<PluginProcessor>> {
        let plugin_data = PyDict::new(py);
        plugin_data.set_item("co_names", ["execute"]).unwrap();
        plugin_data
            .set_item("path_fragment", path_fragment)
            .unwrap();
        plugin_data.set_item("call_type", "query").unwrap();
        plugin_data.set_item("return_type", "query_end").unwrap();
        let plugins = PyList::new(py, [plugin_data]).unwrap();
        load_plugin_data_for_test(py, &plugins, &PyDict::new(py)).unwrap()
    }

    fn idle_filter(
        py: Python,
        include: &[&str],
        ignore: &[&str],
        plugins: &HashMap<String, Vec<PluginProcessor>>,
    ) -> IdleFilter {
        // Any distinct object stands in for sys.monitoring.DISABLE, which
        // older Pythons running these tests do not have.
        let disable = PyDict::new(py).into_any().unbind();
        IdleFilter::new(
            &build_finders(include.iter().map(|path| path.to_string()).collect()),
            &build_finders(ignore.iter().map(|path| path.to_string()).collect()),
            plugins,
            disable,
        )
    }

    fn function_code<'py>(py: Python<'py>, name: &str, filename: &str) -> Bound<'py, PyCode> {
        let source = CString::new(format!("def {name}():\n    pass\n")).unwrap();
        let filename = CString::new(filename).unwrap();
        let module = PyCode::compile(py, &source, &filename, PyCodeInput::File).unwrap();
        let constants = module.getattr("co_consts").unwrap();
        constants
            .get_item(0)
            .unwrap()
            .cast_into::<PyCode>()
            .unwrap()
    }

    #[test]
    fn excluded_code_is_disabled_without_dirtying_the_filter() {
        Python::initialize();
        Python::attach(|py| {
            let idle = idle_filter(py, &[], &[], &processors(py, "django/db/backends/"));
            let library = function_code(py, "helper", "/venv/lib/site-packages/lib.py");
            // A plugin candidate by name whose filename the plugin rejects.
            let other_execute = function_code(py, "execute", "/venv/site-packages/x.py");
            let ignored = function_code(py, "helper", "/srv/app/ignored/views.py");
            let idle = IdleFilter {
                ignore_frames: build_finders(vec!["app/ignored/".to_string()]),
                ..idle
            };

            for code in [&library, &other_execute, &ignored] {
                assert!(idle.idle_event(code).bind(py).is(idle.disable.bind(py)));
            }
            assert!(!idle.take_dirty());
        });
    }

    #[test]
    fn recordable_code_stays_enabled_until_it_keeps_firing() {
        Python::initialize();
        Python::attach(|py| {
            let idle = idle_filter(
                py,
                &["lib/python3/included.py"],
                &[],
                &processors(py, "django/db/backends/"),
            );
            let candidates = [
                function_code(py, "view", "/srv/app/views.py"),
                function_code(py, "helper", "/usr/lib/python3/included.py"),
                function_code(py, "execute", "/venv/site-packages/django/db/backends/u.py"),
                function_code(py, "generated", ""),
            ];
            for code in &candidates {
                for _ in 0..RECORDABLE_EVENTS_BEFORE_DISABLE {
                    assert!(idle.idle_event(code).bind(py).is_none());
                }
                assert!(!idle.take_dirty());
                assert!(idle.idle_event(code).bind(py).is(idle.disable.bind(py)));
                assert!(idle.take_dirty());
                assert!(!idle.take_dirty());
            }
        });
    }

    #[test]
    fn kolo_threads_never_dirty_the_idle_filter() {
        Python::initialize();
        Python::attach(|py| {
            let idle = idle_filter(py, &[], &[], &HashMap::new());
            let view = function_code(py, "view", "/srv/app/views.py");
            let library = function_code(py, "helper", "/venv/lib/site-packages/lib.py");
            for flag in [thread_hooks::WORKER, thread_hooks::SUSPENDED] {
                thread_hooks::set(flag, true);
                // Static exclusions still apply on Kolo's threads...
                assert!(idle.idle_event(&library).bind(py).is(idle.disable.bind(py)));
                // ...but their activity never counts towards disabling
                // recordable code.
                for _ in 0..=RECORDABLE_EVENTS_BEFORE_DISABLE {
                    assert!(idle.idle_event(&view).bind(py).is_none());
                }
                thread_hooks::set(flag, false);
                assert!(!idle.take_dirty());
            }
            // A traced thread's count starts from scratch.
            for _ in 0..RECORDABLE_EVENTS_BEFORE_DISABLE {
                assert!(idle.idle_event(&view).bind(py).is_none());
            }
            // Once counted, Kolo's threads still don't add to the count.
            thread_hooks::set(thread_hooks::WORKER, true);
            for _ in 0..RECORDABLE_EVENTS_BEFORE_DISABLE {
                assert!(idle.idle_event(&view).bind(py).is_none());
            }
            thread_hooks::set(thread_hooks::WORKER, false);
            assert!(!idle.take_dirty());
            assert!(idle.idle_event(&view).bind(py).is(idle.disable.bind(py)));
            assert!(idle.take_dirty());
        });
    }

    #[test]
    fn a_panicking_idle_callback_leaves_the_location_enabled() {
        Python::initialize();
        Python::attach(|py| {
            let idle = idle_filter(py, &[], &[], &HashMap::new());
            let view = function_code(py, "view", "/srv/app/views.py");

            // Panic while holding the counts' lock, as a real bug might.
            let result = idle.guarded(py, || {
                let _counts = idle.recordable_events();
                panic!("kolo bug")
            });

            assert!(result.bind(py).is_none());
            assert!(!pyo3::PyErr::occurred(py));
            // The next session restarts events.
            assert!(idle.take_dirty());
            // Later idle callbacks still work on the poisoned lock.
            assert!(idle.idle_event(&view).bind(py).is_none());
        });
    }

    #[test]
    fn same_filters_compares_every_static_filter() {
        Python::initialize();
        Python::attach(|py| {
            let django = processors(py, "django/db/backends/");
            let idle = idle_filter(py, &["app/"], &[], &django);

            assert!(idle.same_filters(&idle_filter(py, &["app/"], &[], &django)));
            assert!(!idle.same_filters(&idle_filter(py, &["app/", "lib/"], &[], &django)));
            assert!(!idle.same_filters(&idle_filter(py, &["other/"], &[], &django)));
            assert!(!idle.same_filters(&idle_filter(py, &["app/"], &["app/x"], &django)));
            assert!(!idle.same_filters(&idle_filter(
                py,
                &["app/"],
                &[],
                &processors(py, "sqlalchemy/")
            )));
            assert!(!idle.same_filters(&idle_filter(py, &["app/"], &[], &HashMap::new())));
        });
    }
}
