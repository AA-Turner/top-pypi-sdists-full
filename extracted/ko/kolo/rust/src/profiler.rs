use hashbrown::HashMap;
use pyo3::ffi;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::GILProtected;
use pyo3::types::PyBytes;
use pyo3::types::PyDict;
use pyo3::types::PyFrame;
use std::borrow::Cow;
use std::cell::RefCell;
use std::os::raw::c_int;
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
use super::utils;
use super::utils::{Event, SerializedFrame};

#[pyclass(module = "kolo._kolo")]
/// This struct holds data during profiling.
///
/// Several attributes are protected by `GILProtected` or `ThreadLocal` to support multi-threading.
/// Attributes guarded with `GILProtected` can only be mutated when we hold the GIL.
/// Attributes guarded with `ThreadLocal` store data that is only relevant to the current thread.
pub struct KoloProfiler {
    /// The location of the Kolo database on disk.
    db_path: String,
    /// Whether a trace should be saved every time a Python test exits.
    one_trace_per_test: bool,
    /// An identifier for the current trace. Can change if `one_trace_per_test` is `true`.
    trace_id: GILProtected<RefCell<String>>,
    trace_name: Option<String>,
    frames_by_thread: GILProtected<RefCell<HashMap<String, Vec<SerializedFrame>>>>,
    threads: GILProtected<RefCell<HashMap<String, PyObject>>>,
    /// A list of `Finder`s to check a filepath fragment for inclusion in the trace.
    include_frames: filters::Finders,
    /// A list of `Finder`s to check a filepath fragment for exclusion from the trace.
    ignore_frames: filters::Finders,
    /// A dictionary mapping `co_name` to a list of associated `PluginProcessor` instances.
    default_include_frames: GILProtected<RefCell<HashMap<String, Vec<PluginProcessor>>>>,
    /// A list of `PyFrame` objects (as the opaque `PyObject` type) and their associated `frame_id`.
    call_frames: ThreadLocal<RefCell<utils::CallFrames>>,
    /// The time tracing started.
    timestamp: f64,
    /// A dictionary mapping the Python `id` of a frame to the Kolo `frame_id`.
    _frame_ids: ThreadLocal<RefCell<utils::FrameIds>>,
    /// The thread_id of the thread where KoloProfiler was activated
    current_thread_id: String,
    /// A tag for where the profiler was created. e.g. `kolo.enable` or
    /// `kolo.middleware.KoloMiddleware`.
    source: String,
    /// A timeout for saving the trace to sqlite.
    timeout: usize,
    /// Whether to use the lightweight repr format when serializing frame data.
    lightweight_repr: bool,
    /// Omit return locals
    omit_return_locals: bool,

    config: config::Config,
}

#[pymethods]
impl KoloProfiler {
    /// This is called from Python code to trigger saving the trace. Used by
    /// `KoloProfiler.save`.
    fn save(&self) -> Result<(), PyErr> {
        Python::with_gil(|py| self.save_in_db(py))
    }

    /// This is called from Python code to build the trace. Used by
    /// `KoloProfiler.upload_trace_in_thread`.
    fn build_trace(&self) -> Result<Py<PyBytes>, PyErr> {
        Python::with_gil(|py| self.build_trace_inner(py))
    }

    /// Register the profiler on the current thread. Called by `threading.setprofile`. See
    /// `register_profiler` in `lib.rs`.
    fn register_threading_profiler(
        slf: PyRef<'_, Self>,
        _frame: PyObject,
        _event: PyObject,
        _arg: PyObject,
    ) -> Result<(), PyErr> {
        // Safety:
        //
        // PyEval_SetProfile takes two arguments:
        //  * trace_func: Option<Py_tracefunc>
        //  * arg1:       *mut PyObject
        //
        // `profile_callback` matches the signature of a `Py_tracefunc`, so we only
        // need to wrap it in `Some`.
        // `slf.into_ptr()` is a pointer to our Rust profiler instance as a Python
        // object.
        //
        // We must also hold the GIL, which we do because we're called from python.
        //
        // https://docs.rs/pyo3-ffi/latest/pyo3_ffi/fn.PyEval_SetProfile.html
        // https://docs.python.org/3/c-api/init.html#c.PyEval_SetProfile
        unsafe {
            ffi::PyEval_SetProfile(Some(profile_callback), slf.into_ptr());
        }
        Ok(())
    }
}

impl KoloProfiler {
    /// Create a new `KoloProfiler` instance from the Python `KoloProfiler` class.
    ///
    /// Converts the Python objects into their corresponding Rust types.
    pub fn new_from_python(py: Python, py_profiler: &Bound<'_, PyAny>) -> Result<Self, PyErr> {
        let config_dict = py_profiler.getattr(intern!(py, "config"))?;
        let config_dict = config_dict.downcast::<PyDict>()?;

        // TODO: Let's refactor this to use Config instead of config_dict eventually.

        let config = config::Config::new(config_dict)?;
        let filters = config_dict
            .get_item("filters")
            .expect("config.get(\"filters\") should not raise.");

        Ok(Self {
            db_path: py_profiler
                .getattr(intern!(py, "db_path"))?
                .str()?
                .extract()?,
            one_trace_per_test: py_profiler
                .getattr(intern!(py, "one_trace_per_test"))?
                .extract()?,
            trace_id: GILProtected::new(
                py_profiler
                    .getattr(intern!(py, "trace_id"))?
                    .extract::<String>()?
                    .into(),
            ),
            trace_name: py_profiler
                .getattr(intern!(py, "trace_name"))?
                .extract::<Option<String>>()?,
            source: py_profiler
                .getattr(intern!(py, "source"))?
                .extract::<String>()?,
            frames_by_thread: GILProtected::new(HashMap::new().into()),
            threads: GILProtected::new(HashMap::new().into()),
            include_frames: filters::load_filters(&filters, "include_frames")?,
            ignore_frames: filters::load_filters(&filters, "ignore_frames")?,
            default_include_frames: GILProtected::new(load_plugins(py, config_dict)?.into()),
            call_frames: ThreadLocal::new(),
            timestamp: utils::timestamp(),
            _frame_ids: ThreadLocal::new(),
            current_thread_id: utils::get_current_thread_id(py).unwrap(),
            timeout: config.get_or(py, "sqlite_busy_timeout", 60)?,
            lightweight_repr: config.get_or(py, "lightweight_repr", false)?,
            omit_return_locals: config.get_or(py, "omit_return_locals", false)?,
            config,
        })
    }

    /// Extract test name or HTTP request/response information from frames to set the trace name.
    fn _set_trace_name(&self, frames_by_thread: &HashMap<String, Vec<SerializedFrame>>) -> Option<String> {
        utils::extract_test_trace_name(frames_by_thread, &self.current_thread_id)
            .or_else(|| utils::extract_http_trace_name(frames_by_thread, &self.current_thread_id))
    }

    /// Build the trace as msgpack ready to save to sqlite or upload to the dashboard.
    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let frames_by_thread = self.frames_by_thread.get(py).take();
        let threads = self.threads.get(py).take();
        let trace_id = self.trace_id.get(py).borrow().clone();
        
        // Extract trace name if one wasn't explicitly set
        let trace_name = if self.trace_name.is_none() {
            self._set_trace_name(&frames_by_thread)
        } else {
            self.trace_name.clone()
        };

        utils::build_trace(
            py,
            frames_by_thread,
            threads,
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            self.timestamp,
            &self.config,
        )
    }

    /// Save the trace to sqlite.
    ///
    /// We delegate to the Python implementation because the time here is mostly spent in IO with
    /// the filesystem, so there's unlikely to be much of a performance win to justify a Rust
    /// implementation.
    fn save_in_db(&self, py: Python) -> Result<(), PyErr> {
        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("timeout", self.timeout).unwrap();

        let data = self.build_trace_inner(py)?;
        kwargs.set_item("msgpack", data).unwrap();

        let trace_id = self.trace_id.get(py).borrow().clone();
        let db = PyModule::import_bound(py, "kolo.db")?;
        let save = db.getattr(intern!(py, "save_trace_in_sqlite"))?;
        save.call((&self.db_path, &trace_id), Some(&kwargs))?;
        Ok(())
    }

    /// Create a trace frame in msgpack format from a profiling event.
    ///
    /// Analogous to the `KoloProfiler.process_frame` method in Python.
    fn process_frame(
        &self,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        arg: PyObject,
        name: &str,
        frame_types: &mut Vec<String>,
        frames: &mut Vec<SerializedFrame>,
    ) -> Result<(), PyErr> {
        let py = pyframe.py();
        let pyframe_id = pyframe.as_ptr() as usize;

        let frame_id = self
            ._frame_ids
            .get_or_default()
            .borrow_mut()
            .get_or_set(event, pyframe_id);
        let user_code_call_site = self
            .call_frames
            .get_or_default()
            .borrow_mut()
            .get_user_code_call_site(pyframe, event, &frame_id)?;

        // Gather frame data and convert to Rust types
        let arg = arg.downcast_bound::<PyAny>(py)?;

        let mut buf: Vec<u8> = vec![];
        utils::write_frame(
            &mut buf,
            pyframe,
            user_code_call_site,
            utils::Arg::Argument(arg),
            event,
            name,
            &frame_id,
            self.lightweight_repr,
            self.omit_return_locals,
        )?;

        frames.push(buf);
        frame_types.push("frame".to_string());
        self.push_frames(py, event, frame_types, frames)
    }

    fn push_frames(
        &self,
        py: Python,
        event: Event,
        frame_types: &mut [String],
        frames: &mut Vec<SerializedFrame>,
    ) -> Result<(), PyErr> {
        // Optimise the common case of no frames to push.
        if frame_types.is_empty() {
            return Ok(());
        }

        // Reverse the order of return frames so call and return frames can be paired up properly.
        if event == Event::Return {
            frames.reverse();
            frame_types.reverse();
        }
    
        let threading = PyModule::import_bound(py, "threading")?;
        let current_thread = threading.call_method0("current_thread")?;
        let thread_id = utils::get_thread_id(current_thread.as_ref(), py)?;
        
        self.threads.get(py).borrow_mut().insert(thread_id.clone(), current_thread.unbind());

        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                match frame_type.as_str() {
                    "start_test" => {
                        frames.drain(..index);
                        self.start_test(py)
                    }
                    "end_test" => {
                        let mut before: Vec<SerializedFrame> = frames.drain(..index + 1).collect();
                        self.push_frame_data(py, thread_id.clone(), &mut before);
                        self.save_in_db(py)?;
                    }
                    _ => {}
                }
            }
        }
        self.push_frame_data(py, thread_id, frames);
        Ok(())
    }

    fn push_frame_data(
        &self,
        py: Python,
        thread_id: String,
        frames: &mut Vec<SerializedFrame>,
    ) {
        self.frames_by_thread
            .get(py)
            .borrow_mut()
            .entry(thread_id)
            .or_default()
            .append(frames);
    }

    /// Start a new trace because a new test has started.
    fn start_test(&self, py: Python) {
        // Set a new `self.trace_id`.
        let trace_id = utils::trace_id();
        let mut self_trace_id = self.trace_id.get(py).borrow_mut();
        *self_trace_id = trace_id;

        // Clear frames by thread
        let mut frames = self.frames_by_thread.get(py).borrow_mut();
        *frames = HashMap::new();
    }

    /// Check if we should exclude the current frame from the trace using Kolo's builtin filters.
    fn process_default_ignore_frames(
        &self,
        pyframe: &Bound<'_, PyFrame>,
        co_filename: &str,
    ) -> bool {
        filters::library_filter(co_filename)
            | filters::frozen_filter(co_filename)
            | filters::kolo_filter(co_filename)
            | filters::exec_filter(co_filename)
            | filters::pytest_generated_filter(co_filename)
            | filters::attrs_filter(co_filename, pyframe)
    }

    /// Check if we should include the current frame in the trace.
    fn include_frame(&self, pyframe: &Bound<'_, PyFrame>, filename: &str) -> bool {
        self.include_frames.check(filename) | !self.ignore_frame(pyframe, filename)
    }

    /// Check if we should exclude the current frame from the trace.
    fn ignore_frame(&self, pyframe: &Bound<'_, PyFrame>, filename: &str) -> bool {
        self.process_default_ignore_frames(pyframe, filename) | self.ignore_frames.check(filename)
    }

    /// Run a frame processor (from `default_include_frames`) to build a Kolo frame.
    ///
    /// Analogous to the `default_include_frames` handling in `KoloProfiler.__call__`.
    fn run_frame_processor(
        &self,
        py: Python,
        processor: &PluginProcessor,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        arg: &PyObject,
        filename: &str,
    ) -> Result<Option<(String, SerializedFrame)>, PyErr> {
        if !processor.matches_frame(py, pyframe, event, arg, filename)? {
            return Ok(None);
        }
        let call_frames = self.call_frames.get_or_default().borrow().get_bound(py);
        processor.process(py, pyframe, event, arg, call_frames, self.lightweight_repr)
    }

    /// Run the Kolo profiling logic.
    ///
    /// Analagous to `KoloProfiler.__call__`.
    fn profile(&self, frame: &PyObject, arg: PyObject, event: Event, py: Python) {
        let pyframe = frame.bind(py);
        let pyframe = pyframe
            .downcast::<PyFrame>()
            .expect("Python gives us a PyFrame");
        let f_code = pyframe
            .getattr(intern!(py, "f_code"))
            .expect("A frame always has an `f_code`");
        let co_filename = f_code
            .getattr(intern!(py, "co_filename"))
            .expect("`f_code` always has `co_filename`");
        let co_name = f_code
            .getattr(intern!(py, "co_name"))
            .expect("`f_code` always has `co_name`");
        let filename = co_filename
            .extract::<Cow<str>>()
            .expect("`co_filename` is always a string");
        let name = co_name
            .extract::<Cow<str>>()
            .expect("`co_name` is always a string");

        let mut frames = vec![];
        let mut frame_types = vec![];
        let default_include_frames = self.default_include_frames.get(py).borrow();
        if let Some(processors) = default_include_frames.get(&name.to_string()) {
            for processor in processors.iter() {
                match self.run_frame_processor(py, processor, pyframe, event, &arg, &filename) {
                    Ok(Some((frame_type, data))) => {
                        frames.push(data);
                        frame_types.push(frame_type);
                    }
                    Ok(None) => {}
                    Err(err) => self.log_error(py, err, pyframe, event, &co_filename, &co_name),
                }
            }
        };

        let result = match self.include_frame(pyframe, &filename) {
            true => self.process_frame(pyframe, event, arg, &name, &mut frame_types, &mut frames),
            false => self.push_frames(py, event, &mut frame_types, &mut frames),
        };
        if let Err(err) = result {
            self.log_error(py, err, pyframe, event, &co_filename, &co_name);
        }
    }

    /// Log an unexpected error using Python's logging.
    fn log_error(
        &self,
        py: Python,
        err: PyErr,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        co_filename: &Bound<'_, PyAny>,
        co_name: &Bound<'_, PyAny>,
    ) {
        let logging = PyModule::import_bound(py, "logging").unwrap();
        let logger = logging.call_method1("getLogger", ("kolo",)).unwrap();
        let locals = pyframe.getattr(intern!(py, "f_locals")).unwrap();

        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("exc_info", err).unwrap();

        let event: &str = event.into();
        logger
            .call_method(
                "warning",
                (
                    PYTHON_EXCEPTION_WARNING,
                    co_filename,
                    co_name,
                    event,
                    locals,
                ),
                Some(&kwargs),
            )
            .unwrap();
    }
}

const PYTHON_EXCEPTION_WARNING: &str = "Unexpected exception in Rust.
    co_filename: %s
    co_name: %s
    event: %s
    frame locals: %s
";

// Safety:
//
// We match the type signature of `Py_tracefunc`.
//
// https://docs.rs/pyo3-ffi/latest/pyo3_ffi/type.Py_tracefunc.html
/// The low-level callback function that `PyEval_SetProfile` calls into for each event.
///
/// We convert the raw ffi types into nicely behaved safe PyO3 types and then delegate to
/// `KoloProfiler.process` for the main work.
pub extern "C" fn profile_callback(
    _obj: *mut ffi::PyObject,
    _frame: *mut ffi::PyFrameObject,
    what: c_int,
    _arg: *mut ffi::PyObject,
) -> c_int {
    // Exit early if we're not handling a Python `call` or `return` event.
    let event = match what {
        ffi::PyTrace_CALL => Event::Call,
        ffi::PyTrace_RETURN => Event::Return,
        _ => return 0,
    };
    let _frame = _frame as *mut ffi::PyObject;
    Python::with_gil(|py| {
        // Safety:
        //
        // `from_borrowed_ptr_or_err` must be called in an unsafe block.
        //
        // `_obj` is a reference to our `KoloProfiler` wrapped up in a Python object, so
        // we can safely convert it from an `ffi::PyObject` to a `PyObject`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_err
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let obj = match unsafe { PyObject::from_borrowed_ptr_or_err(py, _obj) } {
            Ok(obj) => obj,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };
        let profiler = match obj.extract::<PyRef<KoloProfiler>>(py) {
            Ok(profiler) => profiler,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };

        // Safety:
        //
        // `from_borrowed_ptr_or_err` must be called in an unsafe block.
        //
        // `_frame` is an `ffi::PyFrameObject` which can be converted safely
        // to a `PyObject`. We can later convert it into a `pyo3::types::PyFrame`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_err
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let frame = match unsafe { PyObject::from_borrowed_ptr_or_err(py, _frame) } {
            Ok(frame) => frame,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };

        // Safety:
        //
        // `from_borrowed_ptr_or_opt` must be called in an unsafe block.
        //
        // `_arg` is either a `Py_None` (PyTrace_CALL) or any PyObject (PyTrace_RETURN) or
        // NULL (PyTrace_RETURN). The first two can be unwrapped as a PyObject. `NULL` we
        // convert to a `py.None()`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Py.html#method.from_borrowed_ptr_or_opt
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let arg = match unsafe { PyObject::from_borrowed_ptr_or_opt(py, _arg) } {
            Some(arg) => arg,
            // TODO: Perhaps better exception handling here?
            None => py.None(),
        };

        profiler.profile(&frame, arg, event, py);
        0
    })
}
