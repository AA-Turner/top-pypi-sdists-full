use hashbrown::{HashMap, HashSet};
use pyo3::ffi;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
use pyo3::types::PyBytes;
use pyo3::types::PyDict;
use pyo3::types::PyFrame;
use std::borrow::Cow;
use std::cell::RefCell;
use std::os::raw::c_int;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Mutex;
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
use super::utils;
use super::utils::{Event, SerializedFrame, Serializer};

const TRACKING_PROBE_INTERVAL: usize = 1024;

#[path = "subtree_flush.rs"]
mod subtree_flush;
use subtree_flush::{resolve_flush_subtree_bytes, CandidateOwner, FlushCandidate, OpenSubtree};

#[derive(Default)]
struct FlushThreadState {
    cumulative_bytes: usize,
    armed: bool,
    generation: u64,
    probed_end_index: usize,
    next_probe_end_index: usize,
}

struct RestoreGuard<'a, 'py> {
    frames_by_thread: &'a Mutex<HashMap<String, Vec<SerializedFrame>>>,
    thread_id: String,
    start_index: usize,
    subtree_by_thread: Option<HashMap<String, Vec<SerializedFrame>>>,
    flushed_bytes: usize,
    py: Python<'py>,
}

impl<'a, 'py> RestoreGuard<'a, 'py> {
    fn new(
        frames_by_thread: &'a Mutex<HashMap<String, Vec<SerializedFrame>>>,
        thread_id: String,
        start_index: usize,
        drained_frames: Vec<SerializedFrame>,
        py: Python<'py>,
    ) -> Self {
        let flushed_bytes = drained_frames.iter().map(|frame| frame.len()).sum();
        let mut subtree_by_thread = HashMap::new();
        subtree_by_thread.insert(thread_id.clone(), drained_frames);
        Self {
            frames_by_thread,
            thread_id,
            start_index,
            subtree_by_thread: Some(subtree_by_thread),
            flushed_bytes,
            py,
        }
    }

    fn subtree_by_thread(&self) -> &HashMap<String, Vec<SerializedFrame>> {
        self.subtree_by_thread
            .as_ref()
            .expect("restore guard disarmed before subtree save completed")
    }

    fn flushed_bytes(&self) -> usize {
        self.flushed_bytes
    }

    fn disarm(&mut self) {
        self.subtree_by_thread = None;
    }
}

impl Drop for RestoreGuard<'_, '_> {
    fn drop(&mut self) {
        let Some(mut subtree_by_thread) = self.subtree_by_thread.take() else {
            return;
        };
        let Some(drained_frames) = subtree_by_thread.remove(&self.thread_id) else {
            return;
        };
        let Ok(mut frames_by_thread) = self.frames_by_thread.lock_py_attached(self.py) else {
            return;
        };
        let Some(frames) = frames_by_thread.get_mut(&self.thread_id) else {
            return;
        };
        frames.splice(self.start_index..self.start_index, drained_frames);
    }
}

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
    trace_id: Mutex<String>,
    explicit_trace_name: Option<String>,
    trace_name: Mutex<Option<String>>,
    frames_by_thread: Mutex<HashMap<String, Vec<SerializedFrame>>>,
    threads: Mutex<HashMap<String, Py<PyAny>>>,
    /// A list of `Finder`s to check a filepath fragment for inclusion in the trace.
    include_frames: filters::Finders,
    /// A list of `Finder`s to check a filepath fragment for exclusion from the trace.
    ignore_frames: filters::Finders,
    /// A dictionary mapping `co_name` to a list of associated `PluginProcessor` instances.
    default_include_frames: Mutex<HashMap<String, Vec<PluginProcessor>>>,
    /// A list of `PyFrame` objects (as the opaque `PyObject` type) and their associated `frame_id`.
    // NOTE: `thread_local::ThreadLocal<RefCell<...>>` entries persist for
    // threads that exit while tracing is active — they are only reclaimed
    // when the whole `KoloProfiler` is dropped. Bounded by the number of
    // distinct threads the process spawns, which is small in practice.
    // Decided won't-fix; see #2535 item 1.
    call_frames: ThreadLocal<RefCell<utils::CallFrames>>,
    /// The time tracing started.
    timestamp: f64,
    /// A dictionary mapping the Python `id` of a frame to the Kolo `frame_id`.
    _frame_ids: ThreadLocal<RefCell<utils::FrameIds>>,
    /// The thread_id of the thread where KoloProfiler was activated
    current_thread_id: String,
    current_thread_fn: Py<PyAny>,
    /// A tag for where the profiler was created. e.g. `kolo.enable` or
    /// `kolo.middleware.KoloMiddleware`.
    source: String,
    /// A timeout for saving the trace to sqlite.
    timeout: usize,
    /// Whether to use the lightweight repr format when serializing frame data.
    lightweight_repr: bool,
    serializer: Serializer,
    /// Omit return locals
    omit_return_locals: bool,
    #[pyo3(get)]
    /// Maximum buffered bytes before flushing a subtree. None means disabled.
    flush_subtree_bytes: Option<usize>,
    tracking_start_bytes: usize,
    flush_thread_state: ThreadLocal<RefCell<FlushThreadState>>,
    suspend_hooks: ThreadLocal<RefCell<bool>>,
    // Relaxed is enough here: the generation only invalidates per-thread TLS state,
    // and every other shared structure in the flush path is synchronized by Mutex.
    flush_generation: AtomicU64,
    flush_barrier: Mutex<()>,
    subtree_stack: Mutex<HashMap<String, Vec<OpenSubtree>>>,
    flush_in_progress: Mutex<HashSet<String>>,
    root_trace_id: Mutex<String>,

    config: config::Config,
}

#[pymethods]
impl KoloProfiler {
    /// This is called from Python code to trigger saving the trace. Used by
    /// `KoloProfiler.save`.
    fn save(&self) -> Result<(), PyErr> {
        Python::attach(|py| self.save_in_db(py))
    }

    /// This is called from Python code to build the trace. Used by
    /// `KoloProfiler.upload_trace_in_thread`.
    fn build_trace(&self) -> Result<Py<PyBytes>, PyErr> {
        Python::attach(|py| self.build_trace_inner(py))
    }

    /// Register the profiler on the current thread. Called by `threading.setprofile`. See
    /// `register_profiler` in `lib.rs`.
    fn register_threading_profiler(
        slf: PyRef<'_, Self>,
        _frame: Py<PyAny>,
        _event: Py<PyAny>,
        _arg: Py<PyAny>,
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
        let config_dict = config_dict.cast::<PyDict>()?;

        // TODO: Let's refactor this to use Config instead of config_dict eventually.

        let config = config::Config::new(config_dict)?;
        let filters = config_dict
            .get_item("filters")
            .expect("config.get(\"filters\") should not raise.");
        let trace_id = py_profiler
            .getattr(intern!(py, "trace_id"))?
            .extract::<String>()?;
        let threading = PyModule::import(py, "threading")?;
        let current_thread_fn = threading.getattr(intern!(py, "current_thread"))?.unbind();
        let current_thread = current_thread_fn.bind(py).call0()?;
        let flush_subtree_bytes: Option<usize> = resolve_flush_subtree_bytes(config_dict)?;

        Ok(Self {
            db_path: py_profiler
                .getattr(intern!(py, "db_path"))?
                .str()?
                .extract()?,
            one_trace_per_test: py_profiler
                .getattr(intern!(py, "one_trace_per_test"))?
                .extract()?,
            trace_id: Mutex::new(trace_id.clone()),
            explicit_trace_name: py_profiler
                .getattr(intern!(py, "trace_name"))?
                .extract::<Option<String>>()?,
            trace_name: Mutex::new(
                py_profiler
                    .getattr(intern!(py, "trace_name"))?
                    .extract::<Option<String>>()?,
            ),
            source: py_profiler
                .getattr(intern!(py, "source"))?
                .extract::<String>()?,
            frames_by_thread: Mutex::new(HashMap::new()),
            threads: Mutex::new(HashMap::new()),
            include_frames: filters::load_filters(&filters, "include_frames")?,
            ignore_frames: filters::load_filters(&filters, "ignore_frames")?,
            default_include_frames: Mutex::new(load_plugins(py, config_dict)?),
            call_frames: ThreadLocal::new(),
            timestamp: utils::timestamp(),
            _frame_ids: ThreadLocal::new(),
            current_thread_id: utils::get_thread_id(current_thread.as_ref(), py)?,
            current_thread_fn,
            timeout: config.get_or(py, "sqlite_busy_timeout", 60)?,
            lightweight_repr: config.get_or(py, "lightweight_repr", false)?,
            serializer: Serializer::new(py)?,
            omit_return_locals: config.get_or(py, "omit_return_locals", false)?,
            flush_subtree_bytes,
            tracking_start_bytes: subtree_flush::tracking_start_bytes(flush_subtree_bytes),
            flush_thread_state: ThreadLocal::new(),
            suspend_hooks: ThreadLocal::new(),
            flush_generation: AtomicU64::new(0),
            flush_barrier: Mutex::new(()),
            subtree_stack: Mutex::new(HashMap::new()),
            flush_in_progress: Mutex::new(HashSet::new()),
            root_trace_id: Mutex::new(trace_id),
            config,
        })
    }

    fn trace_name_for_frames(
        &self,
        py: Python,
        frames_by_thread: &HashMap<String, Vec<SerializedFrame>>,
    ) -> Option<String> {
        self.trace_name_for_thread(py, frames_by_thread, &self.current_thread_id)
    }

    fn trace_name_for_thread(
        &self,
        py: Python,
        frames_by_thread: &HashMap<String, Vec<SerializedFrame>>,
        thread_id: &str,
    ) -> Option<String> {
        let mut trace_name = self
            .trace_name
            .lock_py_attached(py)
            .expect("mutex poisoned");
        utils::resolve_trace_name(
            &mut trace_name,
            frames_by_thread,
            thread_id,
            thread_id == self.current_thread_id.as_str(),
        )
    }

    /// Build the trace as msgpack ready to save to sqlite or upload to the dashboard.
    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let (frames_by_thread, threads, trace_id, root_trace_id) = {
            let _flush_barrier = self
                .flush_barrier
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let frames_by_thread = std::mem::take(
                &mut *self
                    .frames_by_thread
                    .lock_py_attached(py)
                    .expect("mutex poisoned"),
            );
            self.reset_subtree_tracking(py);
            let threads =
                std::mem::take(&mut *self.threads.lock_py_attached(py).expect("mutex poisoned"));
            let trace_id = self
                .trace_id
                .lock_py_attached(py)
                .expect("mutex poisoned")
                .clone();
            let root_trace_id = self
                .root_trace_id
                .lock_py_attached(py)
                .expect("mutex poisoned")
                .clone();
            (frames_by_thread, threads, trace_id, root_trace_id)
        };

        // Extract trace name if one wasn't explicitly set
        let trace_name = self.trace_name_for_frames(py, &frames_by_thread);

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
            false, // use_monitoring
            Some(&root_trace_id),
        )
    }

    /// Save the trace to sqlite.
    ///
    /// We delegate to the Python implementation because the time here is mostly spent in IO with
    /// the filesystem, so there's unlikely to be much of a performance win to justify a Rust
    /// implementation.
    fn save_in_db(&self, py: Python) -> Result<(), PyErr> {
        let kwargs = PyDict::new(py);
        kwargs.set_item("timeout", self.timeout).unwrap();

        let data = self.build_trace_inner(py)?;
        kwargs.set_item("msgpack_data", data).unwrap();

        // Convert db_path string to Path object
        let pathlib = PyModule::import(py, "pathlib")?;
        let path_class = pathlib.getattr(intern!(py, "Path"))?;
        let db_path_obj = path_class.call1((&self.db_path,))?;
        kwargs.set_item("db_path", db_path_obj)?;

        let trace_id = self
            .trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .clone();
        let db = PyModule::import(py, "kolo.db")?;
        let save = db.getattr(intern!(py, "save_trace"))?;
        save.call((&trace_id,), Some(&kwargs))?;
        Ok(())
    }

    fn record_closed_segment(
        &self,
        py: Python,
        thread_id: &str,
        start_index: usize,
        end_index: usize,
        resident_bytes: usize,
        co_name: String,
    ) {
        let mut stacks = self
            .subtree_stack
            .lock_py_attached(py)
            .expect("mutex poisoned");
        subtree_flush::record_closed_segment(
            &mut stacks,
            thread_id,
            start_index,
            end_index,
            resident_bytes,
            co_name,
        );
    }

    fn select_flush_candidate(
        &self,
        py: Python,
        thread_id: &str,
    ) -> Option<(CandidateOwner, FlushCandidate)> {
        let subtree_stack = self
            .subtree_stack
            .lock_py_attached(py)
            .expect("mutex poisoned");
        subtree_flush::select_flush_candidate(
            subtree_stack.get(thread_id).map_or(&[], Vec::as_slice),
        )
    }

    fn shift_flush_state_after_flush(
        &self,
        py: Python,
        thread_id: &str,
        start_index: usize,
        end_index: usize,
        resident_delta: isize,
    ) {
        let mut stacks = self
            .subtree_stack
            .lock_py_attached(py)
            .expect("mutex poisoned");
        subtree_flush::shift_flush_state_after_flush(
            stacks.get_mut(thread_id),
            start_index,
            end_index,
            resident_delta,
        );
    }

    fn maybe_flush_segments(&self, py: Python, thread_id: &str) -> PyResult<()> {
        let current_bytes = self
            .flush_thread_state
            .get_or_default()
            .borrow()
            .cumulative_bytes;
        let low_water_bytes = {
            let mut flush_in_progress = self
                .flush_in_progress
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let Some(low_water_bytes) = subtree_flush::begin_flush(
                self.flush_subtree_bytes,
                current_bytes,
                &mut flush_in_progress,
                thread_id,
            ) else {
                return Ok(());
            };
            low_water_bytes
        };

        let result = (|| -> PyResult<()> {
            loop {
                let current_bytes = self
                    .flush_thread_state
                    .get_or_default()
                    .borrow()
                    .cumulative_bytes;
                if current_bytes <= low_water_bytes {
                    break;
                }

                let Some((owner, candidate)) = self.select_flush_candidate(py, thread_id) else {
                    break;
                };
                self.flush_subtree(py, thread_id, owner, candidate)?;
            }
            Ok(())
        })();

        subtree_flush::finish_flush(
            &mut self
                .flush_in_progress
                .lock_py_attached(py)
                .expect("mutex poisoned"),
            thread_id,
        );
        result
    }

    /// Create a trace frame in msgpack format from a profiling event.
    ///
    /// Analogous to the `KoloProfiler.process_frame` method in Python.
    fn process_frame(
        &self,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        arg: Py<PyAny>,
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
        utils::write_frame_with_serializer(
            &mut buf,
            pyframe,
            &self.serializer,
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

        let current_thread = self.current_thread_fn.bind(py).call0()?;
        let thread_id = utils::get_thread_id(current_thread.as_ref(), py)?;

        self.threads
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .insert(thread_id.clone(), current_thread.unbind());

        let mut drained_count = 0;
        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                match frame_type.as_str() {
                    "start_test" => {
                        frames.drain(..index);
                        drained_count = index;
                        self.start_test(py)?
                    }
                    "end_test" => {
                        let mut before: Vec<SerializedFrame> = frames.drain(..index + 1).collect();
                        drained_count = index + 1;
                        let drained_event = frame_types[..index + 1]
                            .iter()
                            .any(|frame_type| frame_type == "frame")
                            .then_some(event);
                        self.push_frame_data(py, thread_id.clone(), &mut before, drained_event)?;
                        self.save_in_db(py)?;
                        self.reset_subtree_tracking(py);
                    }
                    _ => {}
                }
            }
        }
        let remaining_frame_types = &frame_types[drained_count..];
        let track_event = remaining_frame_types
            .iter()
            .any(|frame_type| frame_type == "frame")
            .then_some(event);
        self.push_frame_data(py, thread_id, frames, track_event)?;
        Ok(())
    }

    fn push_frame_data(
        &self,
        py: Python,
        thread_id: String,
        frames: &mut Vec<SerializedFrame>,
        event: Option<Event>,
    ) -> PyResult<()> {
        if frames.is_empty() {
            return Ok(());
        }

        let (start_index, end_index) = {
            let mut frames_by_thread = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let thread_frames = frames_by_thread.entry(thread_id.clone()).or_default();
            let start_index = thread_frames.len();
            thread_frames.append(frames);
            (start_index, thread_frames.len())
        };

        if self.flush_subtree_bytes.is_none() {
            return Ok(());
        }

        let sum_frame_bytes = |slice_start: usize, slice_end: usize| -> usize {
            let frames_by_thread = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let thread_frames = frames_by_thread
                .get(&thread_id)
                .expect("thread frames missing after append");
            thread_frames[slice_start..slice_end]
                .iter()
                .map(|frame| frame.len())
                .sum()
        };
        let (added_bytes, current_bytes, flush_armed) = {
            let flush_state = self.flush_thread_state.get_or_default();
            let mut state = flush_state.borrow_mut();
            let generation = self.flush_generation.load(Ordering::Relaxed);
            if state.generation != generation {
                state.cumulative_bytes = 0;
                state.armed = false;
                state.generation = generation;
                state.probed_end_index = 0;
                state.next_probe_end_index = 0;
            }

            if state.armed || self.tracking_start_bytes == 0 {
                let added_bytes = sum_frame_bytes(start_index, end_index);
                state.cumulative_bytes += added_bytes;
                state.armed = true;
                (added_bytes, state.cumulative_bytes, true)
            } else {
                if state.next_probe_end_index == 0 {
                    state.next_probe_end_index = TRACKING_PROBE_INTERVAL;
                }
                if end_index < state.next_probe_end_index {
                    return Ok(());
                }

                let probe_start = state.probed_end_index;
                let probed_bytes = sum_frame_bytes(probe_start, end_index);
                state.cumulative_bytes += probed_bytes;
                state.probed_end_index = end_index;
                state.next_probe_end_index = end_index + TRACKING_PROBE_INTERVAL;
                if state.cumulative_bytes < self.tracking_start_bytes {
                    return Ok(());
                }

                let added_bytes = if probe_start == start_index {
                    probed_bytes
                } else {
                    sum_frame_bytes(start_index, end_index)
                };
                state.armed = true;
                (added_bytes, state.cumulative_bytes, true)
            }
        };
        let co_name = matches!(event, Some(Event::Call) | None).then(|| {
            let frames_by_thread = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let thread_frames = frames_by_thread
                .get(&thread_id)
                .expect("thread frames missing after append");
            subtree_flush::extract_co_name(&thread_frames[start_index..end_index])
        });

        if !flush_armed {
            return Ok(());
        }

        match event {
            Some(Event::Call) => {
                subtree_flush::push_open_subtree(
                    &mut self
                        .subtree_stack
                        .lock_py_attached(py)
                        .expect("mutex poisoned"),
                    &thread_id,
                    OpenSubtree {
                        start_index,
                        start_bytes: current_bytes.saturating_sub(added_bytes),
                        co_name: co_name.unwrap_or_else(|| "<unknown>".to_string()),
                        flush_candidate: None,
                    },
                );
            }
            Some(Event::Return) => {
                let subtree = subtree_flush::pop_open_subtree(
                    &mut self
                        .subtree_stack
                        .lock_py_attached(py)
                        .expect("mutex poisoned"),
                    &thread_id,
                );
                if let Some(subtree) = subtree {
                    let subtree_bytes = current_bytes.saturating_sub(subtree.start_bytes);
                    self.record_closed_segment(
                        py,
                        &thread_id,
                        subtree.start_index,
                        end_index,
                        subtree_bytes,
                        subtree.co_name,
                    );
                }
            }
            Some(Event::Unwind | Event::Resume | Event::Yield | Event::Throw) => {}
            None => {
                self.record_closed_segment(
                    py,
                    &thread_id,
                    start_index,
                    end_index,
                    added_bytes,
                    co_name.unwrap_or_else(|| "<unknown>".to_string()),
                );
            }
        }
        self.maybe_flush_segments(py, &thread_id)?;
        Ok(())
    }

    /// Start a new trace because a new test has started.
    fn start_test(&self, py: Python) -> PyResult<()> {
        let _flush_barrier = self
            .flush_barrier
            .lock_py_attached(py)
            .expect("mutex poisoned");
        // Set a new `self.trace_id`.
        let trace_id = utils::trace_id();
        let mut self_trace_id = self.trace_id.lock_py_attached(py).expect("mutex poisoned");
        *self_trace_id = trace_id.clone();
        let mut self_root_trace_id = self
            .root_trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned");
        *self_root_trace_id = trace_id;
        *self
            .trace_name
            .lock_py_attached(py)
            .expect("mutex poisoned") = self.explicit_trace_name.clone();

        // Clear frames by thread
        let mut frames = self
            .frames_by_thread
            .lock_py_attached(py)
            .expect("mutex poisoned");
        *frames = HashMap::new();
        drop(frames);
        self.reset_subtree_tracking(py);
        Ok(())
    }

    fn reset_subtree_tracking(&self, py: Python) {
        self.flush_generation.fetch_add(1, Ordering::Relaxed);
        subtree_flush::reset_tracking(
            &mut self
                .subtree_stack
                .lock_py_attached(py)
                .expect("mutex poisoned"),
            &mut self
                .flush_in_progress
                .lock_py_attached(py)
                .expect("mutex poisoned"),
        );
    }

    fn flush_subtree(
        &self,
        py: Python,
        thread_id: &str,
        owner: CandidateOwner,
        candidate: FlushCandidate,
    ) -> PyResult<()> {
        let _flush_barrier = self
            .flush_barrier
            .lock_py_attached(py)
            .expect("mutex poisoned");
        let mut restore_guard = {
            let mut frames_by_thread = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let frames = match frames_by_thread.get_mut(thread_id) {
                Some(frames) => frames,
                None => return Ok(()),
            };
            if candidate.start_index >= frames.len() || candidate.end_index > frames.len() {
                return Ok(());
            }

            let subtree_frames: Vec<Vec<u8>> = frames
                .drain(candidate.start_index..candidate.end_index)
                .collect();
            RestoreGuard::new(
                &self.frames_by_thread,
                thread_id.to_string(),
                candidate.start_index,
                subtree_frames,
                py,
            )
        };
        let flushed_bytes = restore_guard.flushed_bytes();

        let subtrace_id = utils::trace_id();
        let placeholder_buf = subtree_flush::build_subtree_flushed_placeholder(
            &candidate.co_name,
            &subtrace_id,
            flushed_bytes,
            candidate.segment_count,
            utils::timestamp(),
        );

        let threads: HashMap<String, Py<PyAny>> = {
            let mut threads = HashMap::new();
            let guard = self.threads.lock_py_attached(py).expect("mutex poisoned");
            if let Some(thread) = guard.get(thread_id) {
                threads.insert(thread_id.to_string(), thread.clone_ref(py));
            }
            threads
        };
        let root_trace_id = self
            .root_trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .clone();
        let trace_name =
            self.trace_name_for_thread(py, restore_guard.subtree_by_thread(), thread_id);

        let save_result: PyResult<()> = (|| {
            let data = utils::build_trace_from_parts(
                py,
                restore_guard.subtree_by_thread(),
                &threads,
                &subtrace_id,
                trace_name,
                &self.source,
                thread_id.to_string(),
                utils::timestamp(),
                &self.config,
                false,
                Some(&root_trace_id),
            )?;

            let kwargs = PyDict::new(py);
            kwargs.set_item("timeout", self.timeout)?;
            kwargs.set_item("msgpack_data", data)?;

            let pathlib = PyModule::import(py, "pathlib")?;
            let path_class = pathlib.getattr(intern!(py, "Path"))?;
            let db_path_obj = path_class.call1((&self.db_path,))?;
            kwargs.set_item("db_path", db_path_obj)?;

            let db = PyModule::import(py, "kolo.db")?;
            let save = db.getattr(intern!(py, "save_trace"))?;
            let suspend_hooks = self.suspend_hooks.get_or_default();
            *suspend_hooks.borrow_mut() = true;
            let save_result = save.call((&subtrace_id,), Some(&kwargs));
            *suspend_hooks.borrow_mut() = false;
            save_result?;
            Ok(())
        })();
        if let Err(err) = save_result {
            return Err(err);
        }
        let placeholder_len = placeholder_buf.len();
        let mut frames_by_thread = self
            .frames_by_thread
            .lock_py_attached(py)
            .expect("mutex poisoned");
        let frames = match frames_by_thread.get_mut(thread_id) {
            Some(frames) => frames,
            None => {
                return Err(pyo3::exceptions::PyRuntimeError::new_err(format!(
                    "missing frame buffer while finalizing flushed subtree {subtrace_id}",
                )))
            }
        };
        if candidate.start_index > frames.len() {
            return Err(pyo3::exceptions::PyRuntimeError::new_err(format!(
                "frame buffer changed while finalizing flushed subtree {subtrace_id}",
            )));
        }
        frames.insert(candidate.start_index, placeholder_buf);
        restore_guard.disarm();
        drop(frames_by_thread);

        {
            let flush_state = self.flush_thread_state.get_or_default();
            let mut state = flush_state.borrow_mut();
            state.cumulative_bytes = state.cumulative_bytes.saturating_sub(flushed_bytes);
            state.cumulative_bytes += placeholder_len;
        }

        subtree_flush::clear_flush_candidate(
            owner,
            &mut self
                .subtree_stack
                .lock_py_attached(py)
                .expect("mutex poisoned"),
            thread_id,
        );

        self.shift_flush_state_after_flush(
            py,
            thread_id,
            candidate.start_index,
            candidate.end_index,
            placeholder_len as isize - flushed_bytes as isize,
        );
        Ok(())
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
        arg: &Py<PyAny>,
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
    fn profile(&self, frame: &Py<PyAny>, arg: Py<PyAny>, event: Event, py: Python) {
        if *self.suspend_hooks.get_or_default().borrow() {
            return;
        }

        let pyframe = frame.bind(py);
        let pyframe = pyframe
            .cast::<PyFrame>()
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
        let default_include_frames = self
            .default_include_frames
            .lock_py_attached(py)
            .expect("default_include_frames mutex poisoned");
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
        let logging = PyModule::import(py, "logging").unwrap();
        let logger = logging.call_method1("getLogger", ("kolo",)).unwrap();

        // Convert f_locals to dict for Python 3.13+ FrameLocalsProxy compatibility
        let locals_proxy = pyframe.getattr(intern!(py, "f_locals")).unwrap();
        let dict_type = py.get_type::<PyDict>();
        let locals = dict_type.call1((&locals_proxy,)).unwrap();

        let kwargs = PyDict::new(py);
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
    Python::attach(|py| {
        // Safety:
        //
        // `from_borrowed_ptr` must be called in an unsafe block.
        //
        // `_obj` is a reference to our `KoloProfiler` wrapped up in a Python object, so
        // we can safely convert it from an `ffi::PyObject` to a `Bound<PyAny>`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Bound.html#method.from_borrowed_ptr
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let obj = match unsafe { Bound::from_borrowed_ptr_or_err(py, _obj) } {
            Ok(obj) => obj,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };
        let profiler = match obj.extract::<PyRef<KoloProfiler>>() {
            Ok(profiler) => profiler,
            Err(err) => {
                err.restore(py);
                return -1;
            }
        };

        // Safety:
        //
        // `from_borrowed_ptr` must be called in an unsafe block.
        //
        // `_frame` is an `ffi::PyFrameObject` which can be converted safely
        // to a `Bound<PyAny>`. We can later convert it into a `pyo3::types::PyFrame`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Bound.html#method.from_borrowed_ptr
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let frame = match unsafe { Bound::from_borrowed_ptr_or_err(py, _frame) } {
            Ok(frame) => frame.unbind(),
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
        // NULL (PyTrace_RETURN). The first two can be unwrapped as a Bound<PyAny>. `NULL` we
        // convert to a `py.None()`.
        //
        // We borrow the object so we don't break reference counting.
        //
        // https://docs.rs/pyo3/latest/pyo3/struct.Bound.html#method.from_borrowed_ptr_or_opt
        // https://docs.python.org/3/c-api/init.html#c.Py_tracefunc
        let arg = match unsafe { Bound::from_borrowed_ptr_or_opt(py, _arg) } {
            Some(arg) => arg.unbind(),
            // TODO: Perhaps better exception handling here?
            None => py.None(),
        };

        profiler.profile(&frame, arg, event, py);
        0
    })
}

#[cfg(test)]
mod tests {
    use super::subtree_flush::extract_co_name;
    use super::SerializedFrame;
    use rmpv::Value;

    fn pack_frame(entries: Vec<(&str, Value)>) -> SerializedFrame {
        let value = Value::Map(
            entries
                .into_iter()
                .map(|(key, value)| (Value::String(key.into()), value))
                .collect(),
        );
        let mut frame = Vec::new();
        rmpv::encode::write_value(&mut frame, &value).unwrap();
        frame
    }

    #[test]
    fn test_extract_co_name_prefers_first_frame_with_name() {
        let frames = vec![pack_frame(vec![
            ("type", Value::String("frame".into())),
            ("co_name", Value::String("process".into())),
        ])];

        assert_eq!(extract_co_name(&frames), "process");
    }

    #[test]
    fn test_extract_co_name_skips_plugin_frames_without_name() {
        let frames = vec![
            pack_frame(vec![("type", Value::String("plugin".into()))]),
            pack_frame(vec![
                ("type", Value::String("frame".into())),
                ("co_name", Value::String("process".into())),
            ]),
        ];

        assert_eq!(extract_co_name(&frames), "process");
    }

    #[test]
    fn test_extract_co_name_prefers_frame_over_plugin_name() {
        let frames = vec![
            pack_frame(vec![
                ("type", Value::String("plugin".into())),
                ("co_name", Value::String("plugin_name".into())),
            ]),
            pack_frame(vec![
                ("type", Value::String("frame".into())),
                ("co_name", Value::String("process".into())),
            ]),
        ];

        assert_eq!(extract_co_name(&frames), "process");
    }
}
