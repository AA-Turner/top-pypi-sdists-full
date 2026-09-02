use hashbrown::{HashMap, HashSet};
use pyo3::ffi;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
use pyo3::types::PyBytes;
use pyo3::types::PyCode;
use pyo3::types::PyDict;
use pyo3::types::PyFrame;
use std::cell::RefCell;
use std::os::raw::c_int;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;
use std::sync::Mutex;
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
#[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
use super::trace_container::ProcessForkGeneration;
use super::trace_container::{FrameStore, TraceCapture};
use super::utils;
use super::utils::{Event, FrameSequence, SerializedFrame, Serializer};

const TRACKING_PROBE_INTERVAL: usize = 1024;
const MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES: usize = 4096;
const MAX_REUSABLE_PROFILER_FRAME_BYTES: usize = 16 * 1024;

// Keep at most one modest frame buffer per live profiler thread. Taking the
// buffer out of TLS before serialization means no RefCell borrow spans Python
// fallback, plugin processing, or another profiling callback. Rust runs TLS
// destructors when a short-lived thread exits, so dead threads do not leave
// buffers retained by a long-lived profiler.
thread_local! {
    static PROFILER_FRAME_SCRATCH: RefCell<Option<Vec<u8>>> = RefCell::new(None);
}

fn take_profiler_frame_buffer() -> Vec<u8> {
    PROFILER_FRAME_SCRATCH.with(|scratch| scratch.borrow_mut().take().unwrap_or_default())
}

fn recycle_profiler_frame_buffer(mut buffer: Vec<u8>) {
    if buffer.capacity() > MAX_REUSABLE_PROFILER_FRAME_BYTES {
        buffer = Vec::new();
    } else {
        buffer.clear();
    }
    PROFILER_FRAME_SCRATCH.with(|scratch| {
        let mut scratch = scratch.borrow_mut();
        if scratch.is_none() {
            *scratch = Some(buffer);
        }
    });
}

#[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
extern "C" {
    // Public CPython API since 3.9. PyO3 0.26 omits this declaration when it
    // is not building against the limited API.
    fn PyThreadState_GetID(thread_state: *mut ffi::PyThreadState) -> u64;
}

#[derive(Clone, Copy)]
enum ProfilerIncludeDecision {
    /// An explicit include filter matched. It must override every exclusion.
    Always,
    /// An immutable builtin or user exclusion matched.
    Never,
    /// The attrs filter depends on the live parent frame and must be rerun.
    DynamicAttrs,
}

struct ProfilerCodeMetadata {
    // Keep the code object alive so its pointer cannot be reused by another
    // code object during this profiler session.
    _code: Py<PyCode>,
    filename: String,
    name: String,
    relative_path: String,
    // Python 3.8-3.10 code objects do not expose co_qualname. None preserves
    // the existing live-frame fallback in utils::get_qualname.
    co_qualname: Option<String>,
    // Monotonic performance hint, not a guard for other state. Relaxed loads
    // and stores are sufficient: a racing event may retry the safe fallback,
    // but it cannot observe or publish an invalid frame.
    native_msgpack_eligible: AtomicBool,
    include_decision: ProfilerIncludeDecision,
    has_processor_candidates: bool,
}

enum CachedProfilerCodeMetadata {
    Full(Arc<ProfilerCodeMetadata>),
    // A statically excluded code object with no plugin candidate can never
    // emit a frame. Retain only its identity, and bound these strong refs.
    Excluded { _code: Py<PyCode> },
}

enum ProfilerCodeMetadataLookup {
    Full(Arc<ProfilerCodeMetadata>),
    Excluded,
}

#[derive(Default)]
struct ProfilerCodeMetadataCache {
    entries: HashMap<usize, CachedProfilerCodeMetadata>,
    excluded_entries: usize,
}

impl ProfilerCodeMetadataCache {
    fn lookup(&self, code_id: usize) -> Option<ProfilerCodeMetadataLookup> {
        self.entries.get(&code_id).map(|metadata| match metadata {
            CachedProfilerCodeMetadata::Full(metadata) => {
                ProfilerCodeMetadataLookup::Full(metadata.clone())
            }
            CachedProfilerCodeMetadata::Excluded { .. } => ProfilerCodeMetadataLookup::Excluded,
        })
    }

    fn insert_excluded(&mut self, code_id: usize, code: Py<PyCode>) -> ProfilerCodeMetadataLookup {
        assert_eq!(code.as_ptr(), code_id as *mut _);
        if let Some(cached) = self.lookup(code_id) {
            return cached;
        }
        if self.excluded_entries < MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES {
            self.excluded_entries += 1;
            self.entries.insert(
                code_id,
                CachedProfilerCodeMetadata::Excluded { _code: code },
            );
        }
        ProfilerCodeMetadataLookup::Excluded
    }

    fn insert_full(
        &mut self,
        code_id: usize,
        metadata: Arc<ProfilerCodeMetadata>,
    ) -> ProfilerCodeMetadataLookup {
        assert_eq!(metadata._code.as_ptr(), code_id as *mut _);
        if let Some(cached) = self.lookup(code_id) {
            return cached;
        }
        let statically_excluded =
            matches!(metadata.include_decision, ProfilerIncludeDecision::Never);
        if statically_excluded
            && self.excluded_entries >= MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES
        {
            return ProfilerCodeMetadataLookup::Full(metadata);
        }
        if statically_excluded {
            self.excluded_entries += 1;
        }
        self.entries
            .insert(code_id, CachedProfilerCodeMetadata::Full(metadata.clone()));
        ProfilerCodeMetadataLookup::Full(metadata)
    }
}

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

struct CachedProfilerThread {
    id: String,
    thread: Py<PyAny>,
    published_generation: u64,
    fork_generation: u64,
    process_id: u32,
    thread_state_id: Option<u64>,
}

enum PendingFrames<'a> {
    One(&'a SerializedFrame),
    Many(&'a mut Vec<SerializedFrame>),
}

impl PendingFrames<'_> {
    fn is_empty(&self) -> bool {
        match self {
            Self::One(_) => false,
            Self::Many(frames) => frames.is_empty(),
        }
    }

    fn append_to(
        self,
        store: &mut FrameStore,
    ) -> std::io::Result<super::trace_container::AppendResult> {
        match self {
            Self::One(frame) => store.append_serialized(frame),
            Self::Many(frames) => store.append_many(frames),
        }
    }
}

struct RestoreGuard<'a, 'py> {
    frames_by_thread: &'a Mutex<HashMap<String, FrameStore>>,
    thread_id: String,
    start_index: usize,
    subtree_by_thread: Option<HashMap<String, FrameStore>>,
    flushed_bytes: usize,
    py: Python<'py>,
}

impl<'a, 'py> RestoreGuard<'a, 'py> {
    fn new(
        frames_by_thread: &'a Mutex<HashMap<String, FrameStore>>,
        thread_id: String,
        start_index: usize,
        drained_frames: FrameStore,
        py: Python<'py>,
    ) -> Self {
        let flushed_bytes = drained_frames.total_bytes();
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

    fn subtree_by_thread(&self) -> &HashMap<String, FrameStore> {
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
        let _ = frames.insert_store(self.start_index, drained_frames);
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
    frames_by_thread: Mutex<HashMap<String, FrameStore>>,
    trace_capture: Mutex<Arc<TraceCapture>>,
    next_thread_token: AtomicU64,
    threads: Mutex<HashMap<String, Py<PyAny>>>,
    /// A list of `Finder`s to check a filepath fragment for inclusion in the trace.
    include_frames: filters::Finders,
    /// A list of `Finder`s to check a filepath fragment for exclusion from the trace.
    ignore_frames: filters::Finders,
    /// A dictionary mapping `co_name` to associated processors. This candidate
    /// set is loaded once during construction and never mutated; processors'
    /// own per-event state remains dynamic.
    default_include_frames: Mutex<HashMap<String, Vec<PluginProcessor>>>,
    code_metadata_cache: Mutex<ProfilerCodeMetadataCache>,
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
    /// One entry per actual thread, retained until this profiler is dropped,
    /// matching the existing `call_frames` and `_frame_ids` lifetime. Trace
    /// keys keep their inherited Python `ident` collision semantics. Although
    /// PyThreadState_GetID is unique only within an interpreter, this Python
    /// KoloProfiler object and both profile hooks are interpreter-owned: its
    /// callback context cannot legally be installed in another interpreter.
    cached_thread: ThreadLocal<RefCell<Option<CachedProfilerThread>>>,
    /// A registered pthread_atfork child hook advances the process generation
    /// without a syscall on each profiler event. If registration ever fails,
    /// the cache falls back to comparing the live PID for correctness.
    #[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
    fork_generation_reliable: bool,
    /// Incremented whenever the thread registry is drained into a completed
    /// trace. A cached live `Thread` object must be published once into every
    /// generation that contains frames from its thread. Rotation and frame
    /// publication both access this tag while holding `frames_by_thread`; the
    /// atomic is only an equality tag for TLS, so Relaxed does not publish or
    /// protect any associated data.
    thread_generation: AtomicU64,
    /// A tag for where the profiler was created. e.g. `kolo.enable` or
    /// `kolo.middleware.KoloMiddleware`.
    source: String,
    /// A timeout for saving the trace to sqlite.
    timeout: usize,
    /// Whether to use the lightweight repr format when serializing frame data.
    lightweight_repr: bool,
    serializer: Serializer,
    value_interning: utils::ValueInterning,
    frame_paths: utils::FramePathCache,
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

#[cfg(not(Py_GIL_DISABLED))]
fn profiler_value_interning_allowed(frame_types: &[String]) -> bool {
    !frame_types
        .iter()
        .any(|frame_type| matches!(frame_type.as_str(), "start_test" | "end_test"))
}

#[pymethods]
impl KoloProfiler {
    #[getter]
    fn trace_id(&self, py: Python) -> PyResult<String> {
        Ok(self
            .trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .clone())
    }

    #[getter]
    fn root_trace_id(&self, py: Python) -> PyResult<String> {
        Ok(self
            .root_trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .clone())
    }

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
        let db_path = py_profiler
            .getattr(intern!(py, "db_path"))?
            .str()?
            .extract::<String>()?;
        let timestamp = utils::timestamp();
        let trace_capture = TraceCapture::for_trace(&db_path, &trace_id, timestamp);
        #[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
        let fork_generation_reliable = ProcessForkGeneration::register();

        Ok(Self {
            db_path,
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
            trace_capture: Mutex::new(trace_capture),
            next_thread_token: AtomicU64::new(1),
            threads: Mutex::new(HashMap::new()),
            include_frames: filters::load_filters(&filters, "include_frames")?,
            ignore_frames: filters::load_filters(&filters, "ignore_frames")?,
            default_include_frames: Mutex::new(load_plugins(py, config_dict)?),
            code_metadata_cache: Mutex::new(ProfilerCodeMetadataCache::default()),
            call_frames: ThreadLocal::new(),
            timestamp,
            _frame_ids: ThreadLocal::new(),
            current_thread_id: utils::get_thread_id(current_thread.as_ref(), py)?,
            current_thread_fn,
            cached_thread: ThreadLocal::new(),
            #[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
            fork_generation_reliable,
            thread_generation: AtomicU64::new(0),
            timeout: config.get_or(py, "sqlite_busy_timeout", 60)?,
            lightweight_repr: config.get_or(py, "lightweight_repr", false)?,
            serializer: Serializer::new(py)?,
            value_interning: utils::ValueInterning::default(),
            frame_paths: utils::FramePathCache::new(),
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

    fn thread_id(&self, py: Python) -> PyResult<String> {
        let cached_thread = self.cached_thread.get_or_default();
        #[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
        // SAFETY: profiler callbacks are attached to Python, so CPython has a
        // current thread state. Its ID is unique for that thread-state
        // lifetime, unlike both OS/Python idents and thread_local's recycled
        // slot index.
        let thread_state_id = Some(unsafe { PyThreadState_GetID(ffi::PyThreadState_Get()) });
        #[cfg(any(not(Py_3_9), PyPy, GraalPy))]
        let thread_state_id = None;
        #[cfg(all(Py_3_9, not(any(PyPy, GraalPy))))]
        let (fork_generation, process_id) =
            ProcessForkGeneration::current(self.fork_generation_reliable);
        #[cfg(any(not(Py_3_9), PyPy, GraalPy))]
        let (fork_generation, process_id) = (0, 0);

        let (forked_child, cached_id) = {
            let cached = cached_thread.borrow();
            let forked_child = cached.as_ref().is_some_and(|cached| {
                cached.fork_generation != fork_generation || cached.process_id != process_id
            });
            let cached_id = cached.as_ref().and_then(|cached| {
                (thread_state_id.is_some()
                    && cached.thread_state_id == thread_state_id
                    && cached.fork_generation == fork_generation
                    && cached.process_id == process_id)
                    .then(|| cached.id.clone())
            });
            (forked_child, cached_id)
        };
        if forked_child {
            Arc::clone(
                &self
                    .trace_capture
                    .lock_py_attached(py)
                    .expect("trace capture mutex poisoned"),
            )
            .enter_post_fork_mode();
        }

        if let Some(cached_id) = cached_id {
            return Ok(cached_id);
        }

        // No RefCell borrow is held while crossing into Python. CPython also
        // suppresses recursive profile callbacks while this callback runs.
        // CPython 3.8 and PyPy preserve the old per-event lookup because they
        // lack PyThreadState_GetID's non-recycled identity.
        let current_thread = self.current_thread_fn.bind(py).call0()?;
        let thread_id = utils::get_thread_id(current_thread.as_ref(), py)?;
        *cached_thread.borrow_mut() = Some(CachedProfilerThread {
            id: thread_id.clone(),
            // Retain the live Thread object, not a metadata snapshot:
            // name/daemon changes remain visible at final serialization.
            thread: current_thread.unbind(),
            // Publication happens together with the first frame append so a
            // concurrent trace rotation cannot split metadata from frames.
            published_generation: u64::MAX,
            // A fork may preserve the current thread-state ID while changing
            // the native thread identity used in Kolo's trace key.
            fork_generation,
            process_id,
            thread_state_id,
        });
        Ok(thread_id)
    }

    fn publish_cached_thread(&self, py: Python) -> PyResult<()> {
        let cached_thread = self.cached_thread.get_or_default();
        let mut cached = cached_thread.borrow_mut();
        let Some(cached) = cached.as_mut() else {
            return Err(pyo3::exceptions::PyRuntimeError::new_err(
                "profiler thread cache was not initialized",
            ));
        };
        let generation = self.thread_generation.load(Ordering::Relaxed);
        if cached.published_generation == generation {
            return Ok(());
        }

        self.threads
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .insert(cached.id.clone(), cached.thread.clone_ref(py));
        cached.published_generation = generation;
        Ok(())
    }

    fn trace_name_for_frames<S: FrameSequence>(
        &self,
        py: Python,
        frames_by_thread: &HashMap<String, S>,
    ) -> Option<String> {
        self.trace_name_for_thread(py, frames_by_thread, &self.current_thread_id)
    }

    fn trace_name_for_thread<S: FrameSequence>(
        &self,
        py: Python,
        frames_by_thread: &HashMap<String, S>,
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

    fn snapshot_thread_tokens(
        &self,
        frames_by_thread: &HashMap<String, FrameStore>,
        threads: &HashMap<String, Py<PyAny>>,
    ) -> PyResult<HashMap<String, u32>> {
        let mut tokens: HashMap<String, u32> = frames_by_thread
            .iter()
            .map(|(thread_id, frames)| (thread_id.clone(), frames.thread_token()))
            .collect();
        for thread_id in threads.keys() {
            if tokens.contains_key(thread_id) {
                continue;
            }
            let token = u32::try_from(self.next_thread_token.fetch_add(1, Ordering::Relaxed))
                .map_err(|_| {
                    pyo3::exceptions::PyRuntimeError::new_err(
                        "Kolo exhausted its per-capture thread token space",
                    )
                })?;
            tokens.insert(thread_id.clone(), token);
        }
        Ok(tokens)
    }

    fn take_trace_inputs(
        &self,
        py: Python,
    ) -> PyResult<(
        HashMap<String, FrameStore>,
        HashMap<String, Py<PyAny>>,
        String,
        String,
        Arc<TraceCapture>,
        Vec<(u32, Arc<[u8]>)>,
    )> {
        {
            let _flush_barrier = self
                .flush_barrier
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let mut trace_id_guard = self.trace_id.lock_py_attached(py).expect("mutex poisoned");
            let mut root_trace_id_guard = self
                .root_trace_id
                .lock_py_attached(py)
                .expect("mutex poisoned");
            // Drain the registry and swap captures under the same guard. A
            // free-threaded callback registers a new FrameStore while holding
            // this mutex and then reads trace_capture; releasing the registry
            // here would let it bind to the old capture after that capture had
            // already been omitted from this save.
            let mut frames_by_thread_guard = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let frames_by_thread = std::mem::take(&mut *frames_by_thread_guard);
            let previous_capture = {
                let mut capture = self
                    .trace_capture
                    .lock_py_attached(py)
                    .expect("trace capture mutex poisoned");
                let forked = capture.enter_post_fork_mode();
                if forked {
                    let child_trace_id = utils::trace_id();
                    *trace_id_guard = child_trace_id.clone();
                    *root_trace_id_guard = child_trace_id;
                }
                let replacement_capture =
                    TraceCapture::for_trace(&self.db_path, &trace_id_guard, self.timestamp);
                if forked || capture.is_in_memory() {
                    replacement_capture.keep_in_memory();
                }
                std::mem::replace(&mut *capture, replacement_capture)
            };
            let trace_id = trace_id_guard.clone();
            let root_trace_id = root_trace_id_guard.clone();
            drop(root_trace_id_guard);
            drop(trace_id_guard);
            let threads = {
                let mut threads = self.threads.lock_py_attached(py).expect("mutex poisoned");
                let threads = std::mem::take(&mut *threads);
                self.thread_generation.fetch_add(1, Ordering::Relaxed);
                threads
            };
            drop(frames_by_thread_guard);
            self.reset_subtree_tracking(py);
            let value_table = self
                .value_interning
                .snapshot_ids(&previous_capture.published_value_ids());
            Ok((
                frames_by_thread,
                threads,
                trace_id,
                root_trace_id,
                previous_capture,
                value_table,
            ))
        }
    }

    /// Build the trace as msgpack ready to save to sqlite or upload to the dashboard.
    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let (frames_by_thread, threads, trace_id, root_trace_id, _capture, value_table) =
            self.take_trace_inputs(py)?;

        // Extract trace name if one wasn't explicitly set
        let trace_name = self.trace_name_for_frames(py, &frames_by_thread);

        let thread_tokens = self.snapshot_thread_tokens(&frames_by_thread, &threads)?;
        let prepared = utils::prepare_v3_trace_from_parts(
            py,
            &threads,
            &thread_tokens,
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            self.timestamp,
            &self.config,
            false,
            Some(&root_trace_id),
        )?;
        let data = super::trace_container::build_container_bytes(
            &trace_id,
            self.timestamp,
            &frames_by_thread,
            &thread_tokens,
            prepared.thread_meta,
            prepared.metadata,
            value_table,
        )
        .map_err(pyo3::exceptions::PyOSError::new_err)?;
        Ok(PyBytes::new(py, &data).unbind())
    }

    /// Stream the trace to its file and then persist metadata through Python.
    fn save_in_db(&self, py: Python) -> Result<(), PyErr> {
        let (mut frames_by_thread, threads, trace_id, root_trace_id, capture, value_table) =
            self.take_trace_inputs(py)?;
        let trace_name = self.trace_name_for_frames(py, &frames_by_thread);
        let thread_tokens = self.snapshot_thread_tokens(&frames_by_thread, &threads)?;
        let prepared = utils::prepare_v3_trace_from_parts(
            py,
            &threads,
            &thread_tokens,
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            self.timestamp,
            &self.config,
            false,
            Some(&root_trace_id),
        )?;
        #[cfg(target_arch = "wasm32")]
        let result: PyResult<()> = (|| {
            let data = super::trace_container::build_container_bytes(
                &trace_id,
                self.timestamp,
                &frames_by_thread,
                &thread_tokens,
                prepared.thread_meta,
                prepared.metadata,
                value_table,
            )
            .map_err(pyo3::exceptions::PyOSError::new_err)?;
            // Keep the capture (and therefore its in-memory chunk handles)
            // alive until materialization has consumed every frame.
            let _capture = capture;
            utils::save_v3_container_bytes(py, &trace_id, &data, &self.db_path, self.timeout, true)
        })();
        #[cfg(not(target_arch = "wasm32"))]
        let result: PyResult<()> = if capture.is_in_memory() {
            (|| {
                let data = super::trace_container::build_container_bytes(
                    &trace_id,
                    self.timestamp,
                    &frames_by_thread,
                    &thread_tokens,
                    prepared.thread_meta,
                    prepared.metadata,
                    value_table,
                )
                .map_err(pyo3::exceptions::PyOSError::new_err)?;
                utils::save_v3_container_bytes(
                    py,
                    &trace_id,
                    &data,
                    &self.db_path,
                    self.timeout,
                    true,
                )
            })()
        } else {
            (|| {
                let layouts = frames_by_thread
                    .values_mut()
                    .map(FrameStore::layout)
                    .collect::<Result<Vec<_>, _>>()
                    .map_err(pyo3::exceptions::PyOSError::new_err)?;
                capture
                    .finish(prepared.thread_meta, prepared.metadata, layouts)
                    .map_err(pyo3::exceptions::PyOSError::new_err)?;
                utils::save_trace_metadata(py, &trace_id, &self.db_path, self.timeout, true)
            })()
        };
        match result {
            Err(error) if error.is_instance_of::<pyo3::exceptions::PyOSError>(py) => {
                let message = format!("Failed to save trace {trace_id} to file: {error}");
                PyModule::import(py, "kolo.db")?
                    .getattr(intern!(py, "logger"))?
                    .call_method1(intern!(py, "warning"), (message,))?;
                Ok(())
            }
            result => result,
        }
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
        metadata: &ProfilerCodeMetadata,
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

        // Resolve the Python thread before native value publication. The
        // cached CPython 3.9+ path stays entirely in Rust; cache misses and
        // compatibility fallbacks may call threading.current_thread(), which
        // can re-enter Kolo and rotate the trace. Once this returns, the GIL
        // exact-native encoder cannot run Python code, and #push_frames uses
        // this already-resolved ID rather than crossing back into Python.
        // publish_cached_thread then publishes the matching live Thread object
        // under the same frame-registry generation barrier as the append.
        let thread_id = self.thread_id(py)?;

        // With the GIL, this callback cannot race an explicit trace rotation:
        // the value record is therefore published to the same capture that
        // receives the frame below. `start_test` rotates before appending this
        // Call frame; on Return, reversal appends this frame before `end_test`
        // saves and rotates. Keep both boundary callbacks inline rather than
        // coupling references to those orderings. Other frames in each test
        // capture can intern normally. Free-threaded callbacks can rotate
        // concurrently and still stay inline.
        #[cfg(not(Py_GIL_DISABLED))]
        let value_interning = profiler_value_interning_allowed(frame_types).then_some(
            utils::ValueInterningContext::current(&self.value_interning, &self.trace_capture),
        );
        #[cfg(Py_GIL_DISABLED)]
        let value_interning: Option<utils::ValueInterningContext<'_>> = None;

        let mut buf = take_profiler_frame_buffer();
        let serialized = utils::write_frame_with_cached_code_metadata(
            &mut buf,
            pyframe,
            &self.serializer,
            &self.frame_paths,
            user_code_call_site,
            utils::Arg::Argument(arg),
            event,
            name,
            &frame_id,
            self.lightweight_repr,
            self.omit_return_locals,
            true,
            (
                metadata.relative_path.as_str(),
                metadata.co_qualname.as_deref(),
                Some(&metadata.native_msgpack_eligible),
            ),
            value_interning,
        );
        if let Err(error) = serialized {
            recycle_profiler_frame_buffer(buf);
            return Err(error);
        }

        if frame_types.is_empty() && !self.one_trace_per_test {
            let result = self.push_single_frame(py, event, &buf, thread_id);
            recycle_profiler_frame_buffer(buf);
            return result;
        }
        frames.push(buf);
        frame_types.push("frame".to_string());
        self.push_frames(py, event, frame_types, frames, Some(thread_id))
    }

    fn push_single_frame(
        &self,
        py: Python,
        event: Event,
        frame: &SerializedFrame,
        thread_id: String,
    ) -> Result<(), PyErr> {
        self.push_frame_data(py, thread_id, PendingFrames::One(frame), Some(event))
    }

    fn push_frames(
        &self,
        py: Python,
        event: Event,
        frame_types: &mut [String],
        frames: &mut Vec<SerializedFrame>,
        resolved_thread_id: Option<String>,
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

        let thread_id = match resolved_thread_id {
            Some(thread_id) => thread_id,
            None => self.thread_id(py)?,
        };

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
                        self.push_frame_data(
                            py,
                            thread_id.clone(),
                            PendingFrames::Many(&mut before),
                            drained_event,
                        )?;
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
        self.push_frame_data(py, thread_id, PendingFrames::Many(frames), track_event)?;
        Ok(())
    }

    fn push_frame_data(
        &self,
        py: Python,
        thread_id: String,
        frames: PendingFrames<'_>,
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
            // The frame registry lock is also the trace-rotation barrier. It
            // keeps this publication in the same generation as these frames,
            // while the generation fast path avoids the threads mutex on
            // ordinary events.
            self.publish_cached_thread(py)?;
            let thread_frames = frames_by_thread
                .entry(thread_id.clone())
                .or_insert_with(|| {
                    let capture = self
                        .trace_capture
                        .lock_py_attached(py)
                        .expect("trace capture mutex poisoned")
                        .clone();
                    let token =
                        u32::try_from(self.next_thread_token.fetch_add(1, Ordering::Relaxed))
                            .expect("Kolo exhausted its per-capture thread token space");
                    FrameStore::new(capture, token)
                });
            let appended = frames
                .append_to(thread_frames)
                .map_err(pyo3::exceptions::PyOSError::new_err)?;
            (appended.start_index, appended.end_index)
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
            (slice_start..slice_end)
                .filter_map(|index| thread_frames.frame_len(index).ok())
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
            subtree_flush::extract_co_name_range(thread_frames, start_index..end_index)
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
        *self_root_trace_id = trace_id.clone();
        *self
            .trace_name
            .lock_py_attached(py)
            .expect("mutex poisoned") = self.explicit_trace_name.clone();

        let replacement_capture = TraceCapture::for_trace(&self.db_path, &trace_id, self.timestamp);
        // Clear frames by thread and retire the old capture together.
        let mut frames = self
            .frames_by_thread
            .lock_py_attached(py)
            .expect("mutex poisoned");
        *frames = HashMap::new();
        let previous_capture = {
            let mut capture = self
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex poisoned");
            if capture.enter_post_fork_mode() || capture.is_in_memory() {
                replacement_capture.keep_in_memory();
            }
            std::mem::replace(&mut *capture, replacement_capture)
        };
        drop(frames);
        drop(previous_capture);
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

            let subtree_frames = frames
                .drain(candidate.start_index..candidate.end_index)
                .map_err(pyo3::exceptions::PyOSError::new_err)?;
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
        let value_table = {
            let capture = self
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex poisoned");
            self.value_interning
                .snapshot_ids(&capture.published_value_ids())
        };

        let suspend_hooks = self.suspend_hooks.get_or_default();
        *suspend_hooks.borrow_mut() = true;
        let save_result = utils::save_v3_trace_from_parts(
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
            value_table,
            &self.db_path,
            self.timeout,
            false,
        );
        *suspend_hooks.borrow_mut() = false;
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
        frames
            .insert_frame(candidate.start_index, placeholder_buf)
            .map_err(pyo3::exceptions::PyOSError::new_err)?;
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

    /// Check immutable builtin filters. The attrs filename check is static; only
    /// its empty-filename parent-frame fallback remains dynamic.
    fn process_static_default_ignore_frames(&self, co_filename: &str) -> bool {
        filters::library_filter(co_filename)
            || filters::frozen_filter(co_filename)
            || filters::kolo_filter(co_filename)
            || filters::exec_filter(co_filename)
            || filters::pytest_generated_filter(co_filename)
            || filters::attrs_generated_filter(co_filename)
    }

    /// Cache only the immutable part of Kolo's include/exclude model.
    fn profiler_include_decision(&self, filename: &str) -> ProfilerIncludeDecision {
        if self.include_frames.check(filename) {
            // Existing Kolo behavior: explicit includes override every exclusion.
            ProfilerIncludeDecision::Always
        } else if self.process_static_default_ignore_frames(filename)
            || self.ignore_frames.check(filename)
        {
            ProfilerIncludeDecision::Never
        } else {
            ProfilerIncludeDecision::DynamicAttrs
        }
    }

    fn profiler_code_metadata(&self, code: &Bound<'_, PyCode>) -> ProfilerCodeMetadataLookup {
        let py = code.py();
        let code_id = code.as_ptr() as usize;
        if let Some(metadata) = self
            .code_metadata_cache
            .lock_py_attached(py)
            .expect("profiler code metadata cache mutex poisoned")
            .lookup(code_id)
        {
            return metadata;
        }

        let filename = code
            .getattr(intern!(py, "co_filename"))
            .expect("code objects always have co_filename")
            .extract::<String>()
            .expect("code.co_filename is always a string");
        let name = code
            .getattr(intern!(py, "co_name"))
            .expect("code objects always have co_name")
            .extract::<String>()
            .expect("code.co_name is always a string");
        let include_decision = self.profiler_include_decision(&filename);
        let has_processor_candidates = self
            .default_include_frames
            .lock_py_attached(py)
            .expect("default_include_frames mutex poisoned")
            .contains_key(&name);

        if matches!(include_decision, ProfilerIncludeDecision::Never) && !has_processor_candidates {
            let mut cache = self
                .code_metadata_cache
                .lock_py_attached(py)
                .expect("profiler code metadata cache mutex poisoned");
            return cache.insert_excluded(code_id, code.clone().unbind());
        }

        let metadata = Arc::new(ProfilerCodeMetadata {
            _code: code.clone().unbind(),
            relative_path: self.frame_paths.relative_path(&filename),
            co_qualname: code
                .getattr(intern!(py, "co_qualname"))
                .ok()
                .map(|qualname| {
                    qualname
                        .extract::<String>()
                        .expect("code.co_qualname is always a string when present")
                }),
            native_msgpack_eligible: AtomicBool::new(true),
            filename,
            name,
            include_decision,
            has_processor_candidates,
        });
        let mut cache = self
            .code_metadata_cache
            .lock_py_attached(py)
            .expect("profiler code metadata cache mutex poisoned");
        cache.insert_full(code_id, metadata)
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
        #[cfg(all(
            not(any(PyPy, GraalPy)),
            any(Py_3_10, all(Py_3_9, not(Py_LIMITED_API)))
        ))]
        let f_code = {
            // SAFETY: `pyframe` is live; this public C API returns a new
            // strong reference to its code object.
            let f_code = unsafe { ffi::PyFrame_GetCode(pyframe.as_ptr().cast()) };
            unsafe { Bound::from_owned_ptr_or_opt(py, f_code.cast()) }
                .expect("A frame always has an `f_code`")
        };

        #[cfg(not(all(
            not(any(PyPy, GraalPy)),
            any(Py_3_10, all(Py_3_9, not(Py_LIMITED_API)))
        )))]
        let f_code = pyframe
            .getattr(intern!(py, "f_code"))
            .expect("A frame always has an `f_code`");
        let code = f_code
            .cast::<PyCode>()
            .expect("f_code is always a code object");
        let metadata = match self.profiler_code_metadata(code) {
            ProfilerCodeMetadataLookup::Full(metadata) => metadata,
            ProfilerCodeMetadataLookup::Excluded => return,
        };
        let filename = metadata.filename.as_str();
        let name = metadata.name.as_str();

        let mut frames = vec![];
        let mut frame_types = vec![];
        if metadata.has_processor_candidates {
            let default_include_frames = self
                .default_include_frames
                .lock_py_attached(py)
                .expect("default_include_frames mutex poisoned");
            let processors = default_include_frames
                .get(name)
                .expect("cached processor candidate must still exist");
            for processor in processors.iter() {
                match self.run_frame_processor(py, processor, pyframe, event, &arg, filename) {
                    Ok(Some((frame_type, data))) => {
                        frames.push(data);
                        frame_types.push(frame_type);
                    }
                    Ok(None) => {}
                    Err(err) => self.log_error(py, err, pyframe, event, filename, name),
                }
            }
        };

        let include_frame = match metadata.include_decision {
            ProfilerIncludeDecision::Always => true,
            ProfilerIncludeDecision::Never => false,
            ProfilerIncludeDecision::DynamicAttrs => !filters::attrs_filter(filename, pyframe),
        };
        let result = match include_frame {
            true => self.process_frame(
                pyframe,
                event,
                arg,
                name,
                &metadata,
                &mut frame_types,
                &mut frames,
            ),
            false => self.push_frames(py, event, &mut frame_types, &mut frames, None),
        };
        if let Err(err) = result {
            self.log_error(py, err, pyframe, event, filename, name);
        }
    }

    /// Log an unexpected error using Python's logging.
    fn log_error(
        &self,
        py: Python,
        err: PyErr,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        co_filename: &str,
        co_name: &str,
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
    // A storage device which has stopped making progress can no longer accept
    // a lossless bounded trace. Check only events Kolo would otherwise handle;
    // C-level events remain on their existing zero-work return path.
    if super::trace_container::writer_circuit_open() {
        return 0;
    }
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
    #[cfg(not(Py_GIL_DISABLED))]
    use super::profiler_value_interning_allowed;
    use super::subtree_flush::extract_co_name;
    use super::{
        recycle_profiler_frame_buffer, take_profiler_frame_buffer, ProfilerCodeMetadata,
        ProfilerCodeMetadataCache, ProfilerCodeMetadataLookup, ProfilerIncludeDecision,
        SerializedFrame, MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES,
        MAX_REUSABLE_PROFILER_FRAME_BYTES,
    };
    use pyo3::prelude::*;
    use pyo3::types::{PyCode, PyModule};
    use rmpv::Value;
    use std::sync::atomic::AtomicBool;
    use std::sync::Arc;

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
    fn test_profiler_frame_buffer_reuse_is_capped_and_cleared() {
        drop(take_profiler_frame_buffer());

        let mut small = Vec::with_capacity(1024);
        small.extend_from_slice(b"stale frame bytes");
        recycle_profiler_frame_buffer(small);
        let recycled = take_profiler_frame_buffer();
        assert!(recycled.is_empty());
        assert!(recycled.capacity() >= 1024);

        let mut oversized = recycled;
        oversized.reserve(MAX_REUSABLE_PROFILER_FRAME_BYTES + 1);
        assert!(oversized.capacity() > MAX_REUSABLE_PROFILER_FRAME_BYTES);
        recycle_profiler_frame_buffer(oversized);
        let recycled = take_profiler_frame_buffer();
        assert!(recycled.is_empty());
        assert!(recycled.capacity() <= MAX_REUSABLE_PROFILER_FRAME_BYTES);
        recycle_profiler_frame_buffer(recycled);
    }

    #[test]
    fn test_profiler_frame_buffer_nested_acquisition_does_not_replace_live_slot() {
        drop(take_profiler_frame_buffer());

        // The outer callback owns its buffer, so a nested callback receives a
        // distinct allocation and may return it to the empty TLS slot first.
        let outer = take_profiler_frame_buffer();
        let nested = take_profiler_frame_buffer();
        assert!(outer.is_empty());
        assert!(nested.is_empty());
        recycle_profiler_frame_buffer(nested);
        recycle_profiler_frame_buffer(outer);

        let recycled = take_profiler_frame_buffer();
        assert!(recycled.is_empty());
        recycle_profiler_frame_buffer(recycled);
    }

    #[test]
    fn test_profiler_frame_buffers_from_short_lived_threads_stay_capped() {
        let threads: Vec<_> = (0..32)
            .map(|_| {
                std::thread::spawn(|| {
                    let mut buffer = take_profiler_frame_buffer();
                    buffer.resize(MAX_REUSABLE_PROFILER_FRAME_BYTES * 2, 0);
                    recycle_profiler_frame_buffer(buffer);

                    let recycled = take_profiler_frame_buffer();
                    assert!(recycled.is_empty());
                    assert!(recycled.capacity() <= MAX_REUSABLE_PROFILER_FRAME_BYTES);
                    recycle_profiler_frame_buffer(recycled);
                    // The standard thread-local destructor releases this
                    // thread's sole retained buffer when the thread returns.
                })
            })
            .collect();

        for thread in threads {
            thread.join().unwrap();
        }
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

    #[cfg(not(Py_GIL_DISABLED))]
    #[test]
    fn test_profiler_value_interning_excludes_only_test_boundary_callbacks() {
        assert!(profiler_value_interning_allowed(&["frame".to_string()]));
        assert!(!profiler_value_interning_allowed(&[
            "frame".to_string(),
            "start_test".to_string(),
        ]));
        assert!(!profiler_value_interning_allowed(&[
            "start_test".to_string()
        ]));
        assert!(!profiler_value_interning_allowed(&["end_test".to_string()]));
    }

    #[test]
    fn test_profiler_code_metadata_bounds_excluded_code_retention() {
        Python::initialize();

        Python::attach(|py| {
            let compile = PyModule::import(py, "builtins")
                .unwrap()
                .getattr("compile")
                .unwrap();
            let mut cache = ProfilerCodeMetadataCache::default();
            let mut first_cached_id = None;
            let mut uncached_id = None;

            for index in 0..=MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES {
                let source = format!("value = {index}");
                let code = compile
                    .call1((source, format!("excluded_{index}.py"), "exec"))
                    .unwrap()
                    .cast_into::<PyCode>()
                    .unwrap();
                let code_id = code.as_ptr() as usize;
                if index == 0 {
                    first_cached_id = Some(code_id);
                }
                if index == MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES {
                    uncached_id = Some(code_id);
                }
                assert!(matches!(
                    cache.insert_excluded(code_id, code.unbind()),
                    ProfilerCodeMetadataLookup::Excluded
                ));
            }

            assert_eq!(
                cache.entries.len(),
                MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES
            );
            assert_eq!(
                cache.excluded_entries,
                MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES
            );
            // The cache's strong code reference keeps the original identity
            // valid even after the caller releases every code object.
            assert!(matches!(
                cache.lookup(first_cached_id.unwrap()),
                Some(ProfilerCodeMetadataLookup::Excluded)
            ));
            assert!(cache.lookup(uncached_id.unwrap()).is_none());

            let code = compile
                .call1(("value = 1", "excluded_with_plugin.py", "exec"))
                .unwrap()
                .cast_into::<PyCode>()
                .unwrap();
            let code_id = code.as_ptr() as usize;
            let metadata = Arc::new(ProfilerCodeMetadata {
                _code: code.unbind(),
                filename: "excluded_with_plugin.py".to_string(),
                name: "<module>".to_string(),
                relative_path: "excluded_with_plugin.py".to_string(),
                co_qualname: Some("<module>".to_string()),
                native_msgpack_eligible: AtomicBool::new(true),
                include_decision: ProfilerIncludeDecision::Never,
                has_processor_candidates: true,
            });
            assert!(matches!(
                cache.insert_full(code_id, metadata),
                ProfilerCodeMetadataLookup::Full(_)
            ));
            assert!(cache.lookup(code_id).is_none());
            assert_eq!(
                cache.entries.len(),
                MAX_EXCLUDED_PROFILER_CODE_METADATA_ENTRIES
            );
        });
    }

    #[cfg(all(
        not(any(PyPy, GraalPy)),
        any(Py_3_10, all(Py_3_9, not(Py_LIMITED_API)))
    ))]
    #[test]
    fn test_pyframe_getcode_matches_f_code_and_owns_its_reference() {
        Python::initialize();

        Python::attach(|py| {
            let locals = pyo3::types::PyDict::new(py);
            py.run(c"import sys\nframe = sys._getframe()", None, Some(&locals))
                .expect("frame fixture executes");
            let frame = locals
                .get_item("frame")
                .expect("frame lookup succeeds")
                .expect("frame fixture exists")
                .cast_into::<pyo3::types::PyFrame>()
                .expect("fixture is a Python frame");
            let python_code = frame.getattr("f_code").expect("frame has f_code");
            let initial_refcount = python_code.get_refcnt();

            // SAFETY: `frame` is live and PyFrame_GetCode is public on CPython
            // 3.9+. It returns a new strong reference.
            let direct_code = unsafe { pyo3::ffi::PyFrame_GetCode(frame.as_ptr().cast()) };
            let direct_code =
                unsafe { Bound::<PyAny>::from_owned_ptr_or_opt(py, direct_code.cast()) }
                    .expect("a live frame always has a code object");

            assert!(direct_code.is(&python_code));
            assert_eq!(python_code.get_refcnt(), initial_refcount + 1);
            drop(direct_code);
            assert_eq!(python_code.get_refcnt(), initial_refcount);
        });
    }
}
