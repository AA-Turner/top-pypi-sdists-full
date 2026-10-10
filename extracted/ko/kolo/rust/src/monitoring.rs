use hashbrown::{HashMap, HashSet};
use pyo3::exceptions::PyKeyError;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
use pyo3::types::PyBytes;
use pyo3::types::PyCode;
use pyo3::types::PyDict;
use pyo3::types::PyFrame;
use pyo3::types::PyList;
use pyo3::types::PyTuple;
use std::cell::{Cell, RefCell};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::idle_monitor::{
    register_callbacks, release_tool, restart_events, set_idle_monitor, take_idle_monitor,
    IdleFilter, IdleMonitor,
};
use super::plugins::{load_plugins, PluginProcessor};
use super::thread_hooks;
use super::trace_container::{ForkAwareMutex, FrameStore, TraceCapture};
use super::utils;
use super::utils::{
    stopped_after_panic_error, Event, FrameSequence, LineFrame, SerializedFrame, Serializer,
};

/// Monotonic source for `OS_THREAD_TOKEN`. Starts at 1 so 0 can act as the
/// "no owner yet" sentinel in `tls_owner_token`.
static NEXT_OS_THREAD_TOKEN: AtomicU64 = AtomicU64::new(1);

std::thread_local! {
    /// Process-unique token for the current OS thread.
    ///
    /// Native `std::thread_local!` storage is genuinely per-OS-thread and
    /// freshly initialized for every new thread. The `thread_local` crate's
    /// `ThreadLocal<T>` is not: it recycles a dead thread's slot (values
    /// included) for the next thread that starts. Comparing this token
    /// against the one stamped in `KoloMonitor::tls_owner_token` detects a
    /// recycled slot so its stale per-thread state can be discarded — see
    /// `KoloMonitor::reset_recycled_thread_state`.
    static OS_THREAD_TOKEN: u64 = NEXT_OS_THREAD_TOKEN.fetch_add(1, Ordering::Relaxed);
}

/// Counts a running monitoring callback; see `KoloMonitor::end_session`.
/// PY_UNWIND and PY_THROW callbacks are not counted: they can never disable
/// a location.
///
/// Relaxed ordering is enough: the counter and `idle_mode` only matter where
/// a session is kept armed, which requires the GIL, and the GIL orders every
/// callback against `end_session`.
struct CallbackInFlight<'a>(&'a AtomicUsize);

impl<'a> CallbackInFlight<'a> {
    fn enter(counter: &'a AtomicUsize) -> Self {
        counter.fetch_add(1, Ordering::Relaxed);
        CallbackInFlight(counter)
    }
}

impl Drop for CallbackInFlight<'_> {
    fn drop(&mut self) {
        self.0.fetch_sub(1, Ordering::Relaxed);
    }
}

/// Per-thread flush tracking state stored in ThreadLocal to avoid mutex overhead.
#[derive(Default)]
struct FlushThreadState {
    cumulative_bytes: usize,
    armed: bool,
    generation: u64,
    thread_id: Option<Arc<String>>,
    frame_generation: u64,
    frame_buffer: Option<Arc<Mutex<FrameStore>>>,
}

#[path = "subtree_flush.rs"]
mod subtree_flush;
use subtree_flush::{resolve_flush_subtree_bytes, CandidateOwner, FlushCandidate, OpenSubtree};

/// Tagged marker kinds pushed onto per-thread trace-point marker stacks.
///
/// Mirrors the Python `one_trace_per_test` stack-walk model: `start_test`
/// pushes a `Test` sentinel and `end_test` walks back to (and drops) that
/// sentinel, dropping any in-flight `OnReturn` markers above it. Lets future
/// marker kinds coexist on a single stack without forcing every site to
/// drain-and-clear.
#[derive(Clone, Copy, Debug)]
enum MarkerKind {
    /// Sentinel pushed at `start_test`; `end_test` walks back to it.
    Test,
    /// Live trace-point return marker pointing at the start index of the
    /// tracked frame inside `frames_by_thread[thread_id]`.
    OnReturn { start: usize, frame_generation: u64 },
}

struct RestoreGuard<'py> {
    frame_buffer: Arc<Mutex<FrameStore>>,
    thread_id: String,
    start_index: usize,
    subtree_by_thread: Option<HashMap<String, FrameStore>>,
    flushed_bytes: usize,
    py: Python<'py>,
}

impl<'py> RestoreGuard<'py> {
    fn new(
        frame_buffer: Arc<Mutex<FrameStore>>,
        thread_id: String,
        start_index: usize,
        drained_frames: FrameStore,
        py: Python<'py>,
    ) -> Self {
        let flushed_bytes = drained_frames.total_bytes();
        let mut subtree_by_thread = HashMap::new();
        subtree_by_thread.insert(thread_id.clone(), drained_frames);
        Self {
            frame_buffer,
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

impl Drop for RestoreGuard<'_> {
    fn drop(&mut self) {
        let Some(mut subtree_by_thread) = self.subtree_by_thread.take() else {
            return;
        };
        let Some(drained_frames) = subtree_by_thread.remove(&self.thread_id) else {
            return;
        };
        let Ok(mut frames) = self.frame_buffer.lock_py_attached(self.py) else {
            return;
        };
        let restore_index = self.start_index.min(frames.len());
        let _ = frames.insert_store(restore_index, drained_frames);
    }
}

fn discard_frame_buffers(py: Python<'_>, frame_buffers: HashMap<String, Arc<Mutex<FrameStore>>>) {
    for frame_buffer in frame_buffers.into_values() {
        // A retired thread-local slot can retain this Arc after its registry
        // entry is removed. Replace the Vec so those frames and its capacity
        // are released even when the Arc itself remains cached.
        let retired = frame_buffer
            .lock_py_attached(py)
            .expect("thread frame buffer poisoned while starting test")
            .take();
        drop(retired);
    }
}

#[allow(clippy::enum_variant_names)]
#[derive(Clone, Copy)]
enum Opname {
    StoreFast,
    StoreGlobal,
    StoreDeref,
}

struct CachedInstruction {
    /// Variables in store order. Two for `STORE_FAST_STORE_FAST`, else one.
    variables: Arc<[String]>,
    opname: Opname,
}

/// Map a store instruction to the namespace it writes and the variables it
/// binds, in execution order.
///
/// CPython 3.13+ fuses adjacent stores into superinstructions:
/// `STORE_FAST_STORE_FAST` (argval `(first, second)`, stored in that order)
/// and `STORE_FAST_LOAD_FAST` (argval `(stored, loaded)`). Both only write
/// fast locals. `STORE_FAST_MAYBE_NULL` is a compiler pseudo-op that is never
/// emitted, and `STORE_NAME` (module and class bodies) is not captured.
///
/// `@`-prefixed pytest temporaries stay in a double store so its second
/// target keeps its position; `write_assignments` skips them.
fn store_targets(opname: &str, argval: &Bound<'_, PyAny>) -> Option<(Opname, Vec<String>)> {
    let (opname, variables) = match opname {
        "STORE_FAST" | "STORE_GLOBAL" | "STORE_DEREF" => {
            let variable = argval.extract::<String>().ok()?;
            let opname = match opname {
                "STORE_FAST" => Opname::StoreFast,
                "STORE_GLOBAL" => Opname::StoreGlobal,
                _ => Opname::StoreDeref,
            };
            (opname, vec![variable])
        }
        "STORE_FAST_LOAD_FAST" => {
            let (stored, _loaded) = argval.extract::<(String, String)>().ok()?;
            (Opname::StoreFast, vec![stored])
        }
        "STORE_FAST_STORE_FAST" => {
            let (first, second) = argval.extract::<(String, String)>().ok()?;
            (Opname::StoreFast, vec![first, second])
        }
        _ => return None,
    };
    let recorded = variables.iter().any(|variable| !variable.starts_with('@'));
    recorded.then_some((opname, variables))
}

struct CodeInstructionMetadata {
    // Keep the code object alive so the pointer used as the map key cannot be
    // reused for different bytecode during this monitoring session.
    _code: Py<PyCode>,
    filename: String,
    name: String,
    /// `include_frame(filename)`, which depends only on the filename and
    /// this monitor's filters. `None` for an empty filename (attrs-generated
    /// code), whose decision depends on the live parent frame.
    include_frame: Option<bool>,
    instructions: HashMap<usize, CachedInstruction>,
}

/// Immutable metadata shared by every event for one Python code object.
///
/// The code object is held strongly so the pointer key cannot be reused while
/// this monitoring session is alive. Empty filenames deliberately bypass this
/// cache because attrs-generated code requires a dynamic parent-frame check.
struct CodeEventMetadata {
    _code: Py<PyCode>,
    filename: String,
    name: String,
    relative_path: String,
    co_qualname: String,
    lines: Arc<utils::CodeLines>,
    // Diagnostics only: cleared once this code's values need msgpack's
    // default hook (non-builtin values, formerly serialized in Python).
    native_msgpack_eligible: AtomicBool,
    include_frame: bool,
    has_processor_candidates: bool,
}

enum CachedCodeEventMetadata {
    Full(Arc<CodeEventMetadata>),
    // Statically excluded code with no plugin candidates only needs an
    // identity-safe marker. Holding the code strongly prevents pointer reuse
    // without allocating metadata that no event will consume.
    Excluded(Py<PyCode>),
}

/// A thread's copy of a `code_metadata_cache` entry, read without the lock.
#[derive(Clone)]
enum LocalCodeMetadata {
    Full(Arc<CodeEventMetadata>),
    /// Statically excluded with no plugin candidates. Only cached while the
    /// shared cache retains the code object, so its id can't be reused.
    Excluded,
}

enum CodeEventMetadataLookup {
    Full(Arc<CodeEventMetadata>),
    Excluded,
    // Empty filenames require the existing dynamic attrs fallback.
    Dynamic,
}

const MAX_EXCLUDED_CODE_METADATA_ENTRIES: usize = 4096;

#[derive(Default)]
struct CodeMetadataCache {
    entries: HashMap<usize, CachedCodeEventMetadata>,
    excluded_entries: usize,
}

impl CodeMetadataCache {
    fn lookup(&self, code_id: usize) -> Option<CodeEventMetadataLookup> {
        self.entries.get(&code_id).map(|metadata| match metadata {
            CachedCodeEventMetadata::Full(metadata) => {
                CodeEventMetadataLookup::Full(metadata.clone())
            }
            CachedCodeEventMetadata::Excluded(code) => {
                debug_assert_eq!(code.as_ptr(), code_id as *mut _);
                CodeEventMetadataLookup::Excluded
            }
        })
    }

    /// Insert a compact excluded-code marker unless another thread populated
    /// this identity while metadata was being computed without the cache lock.
    fn insert_excluded(&mut self, code_id: usize, code: Py<PyCode>) -> CodeEventMetadataLookup {
        if let Some(cached) = self.lookup(code_id) {
            return cached;
        }
        if self.excluded_entries < MAX_EXCLUDED_CODE_METADATA_ENTRIES {
            self.excluded_entries += 1;
            self.entries
                .insert(code_id, CachedCodeEventMetadata::Excluded(code));
        }
        CodeEventMetadataLookup::Excluded
    }

    /// Insert full metadata unless another thread won the same identity race.
    fn insert_full(
        &mut self,
        code_id: usize,
        metadata: Arc<CodeEventMetadata>,
    ) -> CodeEventMetadataLookup {
        if let Some(cached) = self.lookup(code_id) {
            return cached;
        }
        let cache_excluded_metadata = !metadata.include_frame;
        if cache_excluded_metadata && self.excluded_entries >= MAX_EXCLUDED_CODE_METADATA_ENTRIES {
            return CodeEventMetadataLookup::Full(metadata);
        }
        if cache_excluded_metadata {
            self.excluded_entries += 1;
        }
        self.entries
            .insert(code_id, CachedCodeEventMetadata::Full(metadata.clone()));
        CodeEventMetadataLookup::Full(metadata)
    }
}

impl Opname {
    /// Read the stored value at the next monitoring event, after the store ran.
    ///
    /// Returns `None` when the variable is unbound again by then. An inlined
    /// (PEP 709) comprehension restores its iteration variable's previous,
    /// often unbound, value with a plain `STORE_FAST`, and `except ... as name`
    /// ends with `name = None; del name`. Those assignments are unobservable.
    fn assignment_value<'py>(
        &self,
        variable: &str,
        frame: &Bound<'py, PyAny>,
    ) -> Result<Option<Bound<'py, PyAny>>, PyErr> {
        let py = frame.py();
        let namespace = match self {
            Opname::StoreFast | Opname::StoreDeref => frame.getattr(intern!(py, "f_locals"))?,
            Opname::StoreGlobal => {
                // STORE_GLOBAL writes the underlying dict directly, so read it
                // the same way: a dict subclass's __getitem__/__missing__ must
                // not run (or raise) here.
                let globals = frame.getattr(intern!(py, "f_globals"))?;
                return globals.cast::<PyDict>()?.get_item(variable);
            }
        };
        match namespace.get_item(variable) {
            Ok(value) => Ok(Some(value)),
            Err(err) if err.is_instance_of::<PyKeyError>(py) => Ok(None),
            Err(err) => Err(err),
        }
    }
}

struct InstructionData {
    variables: Arc<[String]>,
    opname: Opname,
    offset: usize,
    line_frame: Py<PyAny>,
    line_frame_data: LineFrame,
}

#[pyclass(module = "kolo._kolo")]
pub struct KoloMonitor {
    #[pyo3(get)]
    tool_id: u8,
    // `active` and `timestamp` are accessed from multiple threads at once.
    // Using atomics / a mutex keeps mutation behind interior mutability so
    // setters only need a shared (&self) borrow, avoiding
    // `RuntimeError: Already borrowed` panics.
    active: AtomicBool,
    #[cfg(test)]
    writer_circuit_override: AtomicBool,
    /// Set once a callback panicked, so we report it only once.
    panicked: AtomicBool,
    timestamp: Mutex<f64>,
    db_path: String,
    source: String,
    one_trace_per_test: bool,
    omit_return_locals: bool,
    /// Bytes one traced value may take before it is replaced by a
    /// truncation marker. None means unlimited.
    max_value_bytes: Option<usize>,
    sqlite_busy_timeout: usize,
    trace_id: Mutex<String>,
    explicit_trace_name: Option<String>,
    trace_name: Mutex<Option<String>>,
    include_frames: filters::Finders,
    ignore_frames: filters::Finders,
    // The map is loaded once, but its processors contain mutable Python
    // context. Keep the mutex for candidate events so free-threaded Python
    // retains the previous serialization semantics. Cached non-candidates
    // skip the lock entirely.
    default_include_frames: Mutex<HashMap<String, Vec<PluginProcessor>>>,
    #[pyo3(get)]
    line_events: bool,
    // Hot callbacks lock only their thread's buffer. The registry mutex is
    // needed on first use per generation; `frame_generation` invalidates TLS
    // handles whenever build_trace/start_test detaches the registry.
    frames_by_thread: Mutex<HashMap<String, Arc<Mutex<FrameStore>>>>,
    trace_capture: Mutex<Arc<TraceCapture>>,
    next_thread_token: AtomicU64,
    frame_generation: AtomicU64,
    threads: Mutex<HashMap<String, Py<PyAny>>>,
    current_thread_id: String,
    current_thread_fn: Py<PyAny>,
    sys_getframe_fn: Py<PyAny>,
    lightweight_repr: bool,
    serializer: Serializer,
    value_interning: utils::ValueInterning,
    frame_paths: utils::FramePathCache,
    // NOTE: `thread_local::ThreadLocal<RefCell<...>>` entries are keyed by
    // the OS thread and persist after that thread exits — they are only
    // reclaimed when the whole `KoloMonitor` is dropped. In practice this
    // is bounded by the number of distinct threads the process ever spawns
    // while tracing is active, which is small enough to ignore. We've
    // decided the memory aspect is won't-fix; see #2535 item 1. The
    // correctness aspect — the crate hands a dead thread's slot (values
    // included) to the next thread that starts — is handled by
    // `reset_recycled_thread_state` via `tls_owner_token`.
    call_frames: ThreadLocal<RefCell<utils::CallFrames>>,
    _frame_ids: ThreadLocal<RefCell<utils::FrameIds>>,
    /// `OS_THREAD_TOKEN` of the thread that owns this slot's per-thread
    /// state (`call_frames`, `_frame_ids`, `instruction_data`,
    /// `flush_thread_state`). 0 = not stamped yet.
    tls_owner_token: ThreadLocal<Cell<u64>>,
    disable: Py<PyAny>,
    /// Set when a callback returned DISABLE for a context-dependent reason.
    context_disabled: AtomicBool,
    /// Session callbacks currently running on any thread.
    callbacks_in_flight: AtomicUsize,
    /// Between sessions, callbacks only disable locations; see `IdleFilter`.
    idle_mode: AtomicBool,
    /// Bumped whenever a session starts or ends; see `owned_result`.
    session_epoch: AtomicU64,
    idle: Arc<IdleFilter>,
    /// This monitor's id in the per-thread assignment bookkeeping
    /// (`thread_hooks::set_assignment`).
    assignment_owner: thread_hooks::AssignmentOwner,
    instruction_data: ThreadLocal<RefCell<Option<InstructionData>>>,
    /// Second targets of `STORE_FAST_STORE_FAST` instructions interrupted by a
    /// nested event before they stored it. Innermost last.
    deferred_stores: ThreadLocal<RefCell<Vec<InstructionData>>>,
    instruction_cache: Mutex<HashMap<usize, Arc<CodeInstructionMetadata>>>,
    code_metadata_cache: Mutex<CodeMetadataCache>,
    code_metadata_local: ThreadLocal<RefCell<HashMap<usize, LocalCodeMetadata>>>,
    get_instructions_fn: Py<PyAny>,
    config: config::Config,
    // Trace points: when one of these functions returns, its subtree is
    // saved as a standalone top-level trace.
    trace_point_return_targets: HashSet<String>,
    trace_point_markers: Mutex<HashMap<String, Vec<MarkerKind>>>,
    #[pyo3(get)]
    /// Maximum buffered bytes before flushing a subtree. None means disabled.
    flush_subtree_bytes: Option<usize>,
    /// Precomputed arming threshold to avoid per-event recomputation.
    tracking_start_bytes: usize,
    /// Per-thread flush state (byte counter + armed flag) in ThreadLocal for zero-mutex hot path.
    flush_thread_state: ThreadLocal<RefCell<FlushThreadState>>,
    /// Relaxed is enough here: the generation only invalidates per-thread TLS state,
    /// and every other shared structure in the flush path is synchronized by Mutex.
    flush_generation: AtomicU64,
    flush_barrier: ForkAwareMutex,
    /// Serializes whole saves on this monitor. A save retires the capture and
    /// then waits on storage detached from the interpreter; without this, a
    /// later save of the same trace ID could publish first and then be
    /// replaced by the older one. Only ever taken with `lock_py_attached`.
    /// Fork-aware because it stays held across that detached wait.
    publish_order: ForkAwareMutex,
    /// Subtree stack and flush candidates remain mutex-guarded (only accessed when armed).
    subtree_stack: Mutex<HashMap<String, Vec<OpenSubtree>>>,
    flush_in_progress: Mutex<HashSet<String>>,
    root_trace_id: Mutex<String>,
}

/// What a monitoring callback fired for, so its result can sometimes be
/// decided before any per-event work.
#[derive(Clone, Copy)]
enum CallbackSource<'a, 'py> {
    Code(&'a Bound<'py, PyCode>),
    /// A `PY_UNWIND`, with its instruction offset.
    Unwind(&'a Bound<'py, PyCode>, usize),
    Instruction(&'a Bound<'py, PyCode>, usize),
    #[cfg_attr(not(test), allow(dead_code))]
    Other,
}

struct PushFrameDataResult {
    thread_id: Arc<String>,
    start_index: usize,
    end_index: usize,
    added_bytes: usize,
    current_bytes: usize,
    flush_tracking_armed: bool,
}

impl KoloMonitor {
    pub fn new(
        db_path: String,
        config_dict: &Bound<'_, PyDict>,
        source: String,
        one_trace_per_test: bool,
        trace_name: Option<String>,
    ) -> Result<Self, PyErr> {
        let py = config_dict.py();
        let config = config::Config::new(config_dict)?;

        let sys = PyModule::import(py, "sys")?;
        let threading = PyModule::import(py, "threading")?;
        let monitoring = sys.getattr("monitoring")?;
        // Run the line table's layout check here, outside any event
        // callback (it enables events on a spare tool id).
        #[cfg(all(kolo_line_table, Py_3_13))]
        utils::check_line_table_layout(py);
        let dis = PyModule::import(py, "dis")?;
        // Needed near the end of the stack, where importing is risky.
        let _ = prefix_end_opcodes(py);
        let disable = monitoring.getattr("DISABLE")?.unbind();
        let current_thread_fn = threading.getattr(intern!(py, "current_thread"))?.unbind();
        let current_thread = current_thread_fn.bind(py).call0()?;
        // Kolo uses tool ID 3 (unassigned) to avoid conflicts with profilers (ID 2)
        let tool_id: u8 = 3;

        let omit_return_locals = config.get_or(py, "omit_return_locals", false)?;
        let max_value_bytes = config::resolve_max_value_bytes(config_dict)?;
        let line_events = config.get_or(py, "line_events", false)?;
        let lightweight_repr = config.get_or(py, "lightweight_repr", false)?;
        let sqlite_busy_timeout = config.get_or(py, "sqlite_busy_timeout", 60)?;

        let filters = config_dict
            .get_item("filters")
            .expect("config.get(\"filters\") should not raise.");
        let plugins = load_plugins(py, config_dict)?;

        // Extract trace point return targets from config
        let mut trace_point_return_targets = HashSet::new();
        if let Ok(Some(trace_points)) = config_dict.get_item("trace_points") {
            if let Ok(trace_points_dict) = trace_points.cast::<PyDict>() {
                if let Ok(Some(targets)) = trace_points_dict.get_item("on_return") {
                    if let Ok(targets_list) = targets.cast::<PyList>() {
                        for item in targets_list.iter() {
                            if let Ok(s) = item.extract::<String>() {
                                trace_point_return_targets.insert(s);
                            }
                        }
                    }
                }
            }
        }

        let include_frames = filters::load_filters(&filters, "include_frames")?;
        let ignore_frames = filters::load_filters(&filters, "ignore_frames")?;
        let idle = Arc::new(IdleFilter::new(
            &include_frames,
            &ignore_frames,
            &plugins,
            disable.clone_ref(py),
        ));

        let flush_subtree_bytes: Option<usize> = resolve_flush_subtree_bytes(config_dict)?;
        let root_trace_id = utils::trace_id();
        let timestamp = utils::timestamp();
        let trace_capture = TraceCapture::for_trace(&db_path, &root_trace_id, timestamp);

        Ok(KoloMonitor {
            active: AtomicBool::new(false),
            #[cfg(test)]
            writer_circuit_override: AtomicBool::new(false),
            panicked: AtomicBool::new(false),
            tool_id,
            timestamp: Mutex::new(timestamp),
            db_path,
            source,
            one_trace_per_test,
            omit_return_locals,
            max_value_bytes,
            sqlite_busy_timeout,
            trace_id: Mutex::new(root_trace_id.clone()),
            explicit_trace_name: trace_name.clone(),
            trace_name: Mutex::new(trace_name),
            include_frames,
            ignore_frames,
            default_include_frames: Mutex::new(plugins),
            line_events,
            frames_by_thread: Mutex::new(HashMap::new()),
            trace_capture: Mutex::new(trace_capture),
            next_thread_token: AtomicU64::new(1),
            frame_generation: AtomicU64::new(1),
            threads: Mutex::new(HashMap::new()),
            current_thread_id: utils::get_thread_id(current_thread.as_ref(), py)?,
            current_thread_fn,
            sys_getframe_fn: sys.getattr(intern!(py, "_getframe"))?.unbind(),
            lightweight_repr,
            serializer: Serializer::new(py)?,
            value_interning: utils::ValueInterning::default(),
            frame_paths: utils::FramePathCache::new(),
            call_frames: ThreadLocal::new(),
            _frame_ids: ThreadLocal::new(),
            tls_owner_token: ThreadLocal::new(),
            disable,
            context_disabled: AtomicBool::new(false),
            callbacks_in_flight: AtomicUsize::new(0),
            idle_mode: AtomicBool::new(false),
            session_epoch: AtomicU64::new(0),
            idle,
            assignment_owner: thread_hooks::AssignmentOwner::new(),
            instruction_data: ThreadLocal::new(),
            deferred_stores: ThreadLocal::new(),
            instruction_cache: Mutex::new(HashMap::new()),
            code_metadata_cache: Mutex::new(CodeMetadataCache::default()),
            code_metadata_local: ThreadLocal::new(),
            get_instructions_fn: dis.getattr(intern!(py, "get_instructions"))?.unbind(),
            config,
            trace_point_return_targets,
            trace_point_markers: Mutex::new(HashMap::new()),
            flush_subtree_bytes,
            tracking_start_bytes: subtree_flush::tracking_start_bytes(flush_subtree_bytes),
            flush_thread_state: ThreadLocal::new(),
            flush_generation: AtomicU64::new(0),
            flush_barrier: ForkAwareMutex::new(),
            publish_order: ForkAwareMutex::new(),
            subtree_stack: Mutex::new(HashMap::new()),
            flush_in_progress: Mutex::new(HashSet::new()),
            root_trace_id: Mutex::new(root_trace_id),
        })
    }

    /// Discard per-thread state inherited from a dead thread.
    ///
    /// The `thread_local` crate recycles its internal per-thread IDs: after
    /// a thread exits, the next thread to start can be handed the dead
    /// thread's slot in every `ThreadLocal`, complete with the values the
    /// dead thread left behind. For `KoloMonitor` that meant a new thread
    /// could inherit a dead thread's cached `FlushThreadState.thread_id` —
    /// silently appending all of its frames to the dead thread's bucket in
    /// `frames_by_thread` (the `test_threading[True]` CI flake) — as well
    /// as its open `call_frames`, `_frame_ids` and `instruction_data`.
    ///
    /// Detect recycling by stamping each slot with a process-unique
    /// per-OS-thread token (`OS_THREAD_TOKEN`, native `std::thread_local!`
    /// storage, never recycled) and clear all cached per-thread state when
    /// the slot changed hands.
    ///
    /// Must run at the top of every monitoring callback before any other
    /// per-thread state is read. The one exception is `code_metadata_local`
    /// (see `local_code_metadata`): its entries are valid for this whole
    /// monitor, whichever thread cached them.
    fn reset_recycled_thread_state(&self) {
        let token = OS_THREAD_TOKEN.with(|token| *token);
        let owner = self.tls_owner_token.get_or(|| Cell::new(0));
        if owner.get() == token {
            return;
        }
        if let Some(call_frames) = self.call_frames.get() {
            *call_frames.borrow_mut() = Default::default();
        }
        if let Some(frame_ids) = self._frame_ids.get() {
            *frame_ids.borrow_mut() = Default::default();
        }
        if let Some(instruction_data) = self.instruction_data.get() {
            *instruction_data.borrow_mut() = None;
        }
        if let Some(deferred_stores) = self.deferred_stores.get() {
            deferred_stores.borrow_mut().clear();
        }
        if let Some(code_metadata) = self.code_metadata_local.get() {
            code_metadata.borrow_mut().clear();
        }
        if let Some(flush_state) = self.flush_thread_state.get() {
            *flush_state.borrow_mut() = Default::default();
        }
        owner.set(token);
    }

    fn include(
        &self,
        py: Python,
        processor: &PluginProcessor,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        arg: &Py<PyAny>,
    ) -> Result<Option<(String, SerializedFrame)>, PyErr> {
        // The caller must prefilter with `matches_filename`; keeping that
        // check outside avoids resolving a Python frame for filename misses.
        if !processor.matches_event(py, pyframe.as_any(), event, arg)? {
            return Ok(None);
        }
        let call_frames = self.call_frames.get_or_default().borrow().get_bound(py);
        processor.process(py, pyframe, event, arg, call_frames, self.lightweight_repr)
    }

    fn monitor(
        &self,
        code: &Bound<'_, PyCode>,
        arg: utils::Arg,
        event: Event,
        // This thread's cached metadata for `code`, if `guarded_callback`
        // already looked it up.
        local: Option<LocalCodeMetadata>,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let mut deferred_interrupt = None;
        let result = self.monitor_event(code, arg, event, local, &mut deferred_interrupt);
        match (deferred_interrupt, result) {
            // A plugin interrupt deferred until the exit was recorded must not
            // be lost to a later failure.
            (Some(interrupt), _) => Err(interrupt),
            (None, result) => result,
        }
    }

    fn monitor_event(
        &self,
        code: &Bound<'_, PyCode>,
        arg: utils::Arg,
        event: Event,
        local: Option<LocalCodeMetadata>,
        deferred_interrupt: &mut Option<PyErr>,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let py = code.py();
        let lookup = match local {
            Some(LocalCodeMetadata::Full(metadata)) => CodeEventMetadataLookup::Full(metadata),
            Some(LocalCodeMetadata::Excluded) => CodeEventMetadataLookup::Excluded,
            None => self.code_event_metadata(code)?,
        };
        let metadata = match lookup {
            CodeEventMetadataLookup::Full(metadata) => Some(metadata),
            CodeEventMetadataLookup::Excluded => {
                return match event {
                    Event::Call | Event::Return | Event::Resume | Event::Yield => {
                        Ok(Some(self.disable.clone_ref(py)))
                    }
                    Event::Unwind | Event::Throw => Ok(None),
                };
            }
            CodeEventMetadataLookup::Dynamic => None,
        };
        let legacy_filename;
        let legacy_name;
        let (filename, name, include_frame, has_processor_candidates) = match &metadata {
            Some(metadata) => (
                metadata.filename.as_str(),
                metadata.name.as_str(),
                Some(metadata.include_frame),
                metadata.has_processor_candidates,
            ),
            None => {
                // Empty filenames are used by attrs-generated code, whose
                // filtering decision depends on the live parent frame.
                legacy_filename = code
                    .getattr(intern!(py, "co_filename"))
                    .expect("Code objects always define co_filename")
                    .extract::<String>()
                    .expect("`co_filename` is always a string");
                legacy_name = code
                    .getattr(intern!(py, "co_name"))
                    .expect("Code objects always define co_name")
                    .extract::<String>()
                    .expect("`co_name` is always a string");
                (
                    legacy_filename.as_str(),
                    legacy_name.as_str(),
                    None,
                    self.default_include_frames
                        .lock_py_attached(py)
                        .expect("default_include_frames mutex poisoned")
                        .contains_key(&legacy_name),
                )
            }
        };

        let include_frame = match include_frame {
            Some(include_frame) => include_frame,
            None => self.include_frame(py, filename)?,
        };
        let defer_subtree_flush = !self.trace_point_return_targets.is_empty()
            && self.flush_subtree_bytes.is_some()
            && matches!(event, Event::Return)
            && self.trace_point_return_targets.contains(name);
        let target_frame_appended = if include_frame && !has_processor_candidates {
            if let Some(push_result) =
                self.process_direct(py, name, event, arg, metadata.as_deref())?
            {
                let tracked =
                    self.track_direct_frame(py, event, name, &push_result, !defer_subtree_flush);
                self.after_recorded_exit(py, event, tracked)?;
                true
            } else {
                false
            }
        } else {
            let mut frames = vec![];
            let mut frame_types = vec![];
            let default_include_frames = self
                .default_include_frames
                .lock_py_attached(py)
                .expect("default_include_frames mutex poisoned");
            let processors = default_include_frames.get(name);
            let has_matching_processor = processors.is_some_and(|processors| {
                processors
                    .iter()
                    .any(|processor| processor.matches_filename(filename))
            });
            if !include_frame && !has_matching_processor {
                if metadata.is_none() {
                    // attrs filtering of empty filenames depends on the caller.
                    return Ok(self.context_dependent_disable(py, event));
                }
                return match event {
                    Event::Call | Event::Return | Event::Resume | Event::Yield => {
                        Ok(Some(self.disable.clone_ref(py)))
                    }
                    Event::Unwind | Event::Throw => Ok(None),
                };
            }
            // Plugin candidates and the ordinary frame describe the same
            // monitoring event. Resolve its live frame once rather than
            // dispatching back through ``sys._getframe`` once per candidate
            // and then again for the ordinary frame.
            let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
            let pyframe = frame.cast::<PyFrame>()?;
            let pyframe_id = pyframe.as_ptr() as usize;
            // On an entry this clears a marker left by an earlier frame here.
            let abandoned = self
                ._frame_ids
                .get_or_default()
                .borrow_mut()
                .take_abandoned(pyframe_id);
            if abandoned && matches!(event, Event::Return | Event::Unwind | Event::Yield) {
                return Ok(None);
            }
            if let Some(processors) = processors {
                // Convert the callback argument at most once, and only when a
                // filename-matched plugin can actually consume it.
                // Plugins get no value an exit was recorded without.
                let plugin_arg = has_matching_processor.then(|| match utils::values_omitted() {
                    true => py.None(),
                    false => arg.clone().into_inner(py),
                });
                for processor in processors.iter() {
                    if !processor.matches_filename(filename) {
                        continue;
                    }
                    let included = self.include(
                        py,
                        processor,
                        pyframe,
                        event,
                        plugin_arg
                            .as_ref()
                            .expect("matched processor has a converted argument"),
                    );
                    let included = match included {
                        // Record the exit first, then raise (see `exit_recorded`):
                        // a repeat would run this plugin, and fail, again. A
                        // generator can catch an interrupt raised at its
                        // yield and carry on, so a yield raises unrecorded.
                        Err(err)
                            if matches!(event, Event::Return | Event::Unwind)
                                && utils::reaches_program(py, &err) =>
                        {
                            if deferred_interrupt.is_none() {
                                *deferred_interrupt = Some(err);
                            }
                            continue;
                        }
                        // Short of stack, a plugin can fail where the frame
                        // itself still records: keep the frame's exit.
                        // Interrupts still reach the program.
                        Err(err)
                            if utils::values_omitted() && !utils::reaches_program(py, &err) =>
                        {
                            self.log_error(py, err);
                            continue;
                        }
                        Err(err) => {
                            self.abandon_entry(py, event, pyframe_id, None, &err);
                            return Err(err);
                        }
                        Ok(included) => included,
                    };
                    if let Some((frame_type, frame_data)) = included {
                        frames.push(frame_data);
                        frame_types.push(frame_type);
                    }
                }
            }
            drop(default_include_frames);
            if include_frame {
                if let Some(frame_data) =
                    self.process(pyframe, name, event, arg, metadata.as_deref())?
                {
                    frames.push(frame_data);
                    frame_types.push("frame".to_string());
                }
            } else if frames.is_empty() {
                if let Some(err) = deferred_interrupt.take() {
                    // Nothing was recorded: let CPython's repeat retry it.
                    return Err(err);
                }
                // Plugin matchers judge the live frame, not just the code.
                return Ok(self.context_dependent_disable(py, event));
            }
            // Capture whether a real target frame ("frame" type) is present
            // before the call branches consume `frame_types`. The trace point
            // guard below must not fire for functions that only produced
            // default_include_frames entries.
            let target_frame_appended = frame_types.iter().any(|t| t == "frame");
            match event {
                Event::Call | Event::Resume | Event::Throw => {
                    self.push_frames_call(py, &mut frames, frame_types, name)?
                }
                Event::Return | Event::Unwind | Event::Yield => {
                    let pushed = self.push_frames_return(
                        py,
                        &mut frames,
                        &mut frame_types,
                        !defer_subtree_flush,
                    );
                    self.after_recorded_exit(py, event, pushed)?
                }
            }
            target_frame_appended
        };

        // Trace points: record markers on call, save on return. Keep this in
        // a result scope so a failed snapshot cannot skip the deferred flush
        // below and leave the thread above its configured memory threshold.
        let trace_point_result = (|| -> PyResult<()> {
            if !(target_frame_appended
                && !self.trace_point_return_targets.is_empty()
                && self.trace_point_return_targets.contains(name))
            {
                return Ok(());
            }
            let suspended = thread_hooks::Suspended::new();

            let resolved_thread_id: PyResult<String> = (|| {
                let current_thread = self.current_thread_fn.bind(py).call0()?;
                let thread_id = utils::get_thread_id(current_thread.as_ref(), py)?;
                self.threads
                    .lock_py_attached(py)
                    .expect("mutex poisoned")
                    .entry(thread_id.clone())
                    .or_insert_with(|| current_thread.into());
                Ok(thread_id)
            })();

            drop(suspended);

            let thread_id = resolved_thread_id?;

            match event {
                Event::Call => {
                    let frame_generation = self.frame_generation.load(Ordering::Acquire);
                    if let Some(frame_buffer) = self.thread_frame_buffer(py, &thread_id) {
                        let all = frame_buffer.lock_py_attached(py).expect("frames mutex");
                        if !all.is_empty()
                            && self.frame_generation.load(Ordering::Acquire) == frame_generation
                        {
                            let start = all.len() - 1;
                            drop(all);
                            self.trace_point_markers
                                .lock_py_attached(py)
                                .expect("markers mutex")
                                .entry(thread_id)
                                .or_default()
                                .push(MarkerKind::OnReturn {
                                    start,
                                    frame_generation,
                                });
                        }
                    }
                }
                Event::Return => {
                    let mut markers = self
                        .trace_point_markers
                        .lock_py_attached(py)
                        .expect("markers mutex");
                    // Pop the topmost OnReturn marker. If the topmost entry is
                    // a Test sentinel (e.g. because an Unwind already dropped
                    // the matching OnReturn), leave the sentinel in place and
                    // skip the save.
                    let popped = markers
                        .get_mut(&thread_id)
                        .and_then(|stack| match stack.last() {
                            Some(MarkerKind::OnReturn {
                                start,
                                frame_generation,
                            }) => {
                                let start = *start;
                                let frame_generation = *frame_generation;
                                stack.pop();
                                Some((start, frame_generation))
                            }
                            _ => None,
                        });
                    drop(markers);
                    if let Some((start, frame_generation)) = popped {
                        let slice = self.thread_frame_buffer(py, &thread_id).and_then(|buffer| {
                            let all = buffer.lock_py_attached(py).ok()?;
                            if self.frame_generation.load(Ordering::Acquire) != frame_generation
                                || start >= all.len()
                            {
                                return None;
                            }
                            let end = all.len();
                            let slice = all.copy_range(start..end).ok()?;
                            let capture = all.capture()?;
                            drop(all);
                            (self.frame_generation.load(Ordering::Acquire) == frame_generation)
                                .then_some((slice, capture))
                        });
                        if let Some((slice, capture)) = slice {
                            if let Err(err) =
                                self.save_trace_point(py, &thread_id, slice, &capture, name)
                            {
                                self.log_error(py, err);
                            }
                        }
                    }
                }
                Event::Unwind => {
                    if let Some(stack) = self
                        .trace_point_markers
                        .lock_py_attached(py)
                        .expect("markers mutex")
                        .get_mut(&thread_id)
                    {
                        // Only pop an OnReturn marker on unwind; never drop
                        // a Test sentinel out from under the test.
                        if matches!(stack.last(), Some(MarkerKind::OnReturn { .. })) {
                            stack.pop();
                        }
                    }
                }
                _ => {}
            }
            Ok(())
        })();

        // Returning from a configured trace point is the one event where
        // subtree persistence must wait: the flush can replace the tracked
        // range and invalidate its marker. The snapshot above owns its own
        // frame bytes, so normal flushing can resume immediately afterward.
        // If this return also closed a one_trace_per_test boundary, save()
        // already reset the subtree stack/generation; the helper may observe
        // stale TLS counters but candidate selection is then empty and the
        // flush is a no-op rather than crossing the boundary.
        let flush_result = if defer_subtree_flush {
            self.maybe_flush_current_thread(py)
        } else {
            Ok(())
        };
        self.after_recorded_exit(py, event, trace_point_result.and(flush_result))?;

        match deferred_interrupt.take() {
            Some(err) => Err(self.exit_recorded(py, event, err)),
            None => Ok(None),
        }
    }

    /// Raise an error that `utils::reaches_program` after this event was
    /// recorded (via `exit_recorded`), except after a Yield: a generator can
    /// catch it at the yield and carry on to a second recorded yield, so it
    /// is logged instead.
    fn after_recorded_exit(&self, py: Python, event: Event, result: PyResult<()>) -> PyResult<()> {
        match result {
            Err(err) if utils::reaches_program(py, &err) => {
                if matches!(event, Event::Yield) {
                    self.log_error(py, err);
                    return Ok(());
                }
                Err(self.exit_recorded(py, event, err))
            }
            result => result,
        }
    }

    /// Raising into a Return makes CPython report the same frame's exit
    /// again (as PY_UNWIND); no source-level handler can catch it at the
    /// return itself. Once Kolo has recorded the return, mark the frame so
    /// that repeat is skipped rather than closing it twice.
    fn exit_recorded(&self, py: Python, event: Event, err: PyErr) -> PyErr {
        if matches!(event, Event::Return) {
            if let Ok(frame) = self.sys_getframe_fn.bind(py).call1((0,)) {
                self._frame_ids
                    .get_or_default()
                    .borrow_mut()
                    .abandon(frame.as_ptr() as usize, true);
            }
        }
        err
    }

    fn process(
        &self,
        pyframe: &Bound<'_, PyFrame>,
        name: &str,
        event: Event,
        arg: utils::Arg,
        metadata: Option<&CodeEventMetadata>,
    ) -> Result<Option<SerializedFrame>, PyErr> {
        let pyframe_id = pyframe.as_ptr() as usize;
        let frame_ids = self._frame_ids.get_or_default();
        let frame_id = match event {
            Event::Call | Event::Resume | Event::Throw => {
                frame_ids.borrow_mut().get_or_set(event, pyframe_id)
            }
            Event::Return | Event::Unwind | Event::Yield => {
                let mut frame_ids = frame_ids.borrow_mut();
                if frame_ids.take_abandoned(pyframe_id) {
                    return Ok(None);
                }
                let Some(frame_id) = frame_ids.get_option(pyframe_id) else {
                    return Ok(None);
                };
                frame_id
            }
        };
        let processed = (|| -> Result<Option<SerializedFrame>, PyErr> {
            let user_code_call_site = self
                .call_frames
                .get_or_default()
                .borrow_mut()
                .get_user_code_call_site(
                    pyframe,
                    event,
                    &frame_id,
                    metadata.map(|metadata| &metadata.lines),
                )?;
            let mut buf: Vec<u8> = vec![];
            match metadata {
                Some(metadata) => utils::write_frame_with_cached_code_metadata(
                    &mut buf,
                    pyframe,
                    &self.serializer,
                    &self.frame_paths,
                    user_code_call_site,
                    arg,
                    event,
                    name,
                    &frame_id,
                    self.lightweight_repr,
                    self.omit_return_locals,
                    (
                        metadata.relative_path.as_str(),
                        Some(metadata.co_qualname.as_str()),
                        Some(&metadata.native_msgpack_eligible),
                        Some(&*metadata.lines),
                    ),
                    None,
                    self.max_value_bytes,
                )?,
                None => utils::write_frame_with_serializer(
                    &mut buf,
                    pyframe,
                    &self.serializer,
                    &self.frame_paths,
                    user_code_call_site,
                    arg,
                    event,
                    name,
                    &frame_id,
                    self.lightweight_repr,
                    self.omit_return_locals,
                    None,
                    self.max_value_bytes,
                )?,
            }
            Ok(Some(buf))
        })();
        if let Err(err) = &processed {
            self.abandon_entry(pyframe.py(), event, pyframe_id, Some(&frame_id), err);
        }
        processed
    }

    /// After an entry event's frame could not be recorded because Kolo is
    /// raising an interrupt into it (see `utils::reaches_program`), forget the
    /// frame: CPython reports its exit (PY_UNWIND), which must then neither
    /// close the caller's call site nor be matched to a call.
    fn abandon_entry(
        &self,
        py: Python,
        event: Event,
        pyframe_id: usize,
        frame_id: Option<&utils::FrameId>,
        err: &PyErr,
    ) {
        if matches!(event, Event::Call | Event::Resume | Event::Throw)
            && utils::reaches_program(py, err)
        {
            self._frame_ids
                .get_or_default()
                .borrow_mut()
                .abandon(pyframe_id, true);
            if let Some(frame_id) = frame_id {
                self.call_frames
                    .get_or_default()
                    .borrow_mut()
                    .abandon(frame_id);
            }
        }
    }

    fn process_direct(
        &self,
        py: Python,
        name: &str,
        event: Event,
        arg: utils::Arg,
        metadata: Option<&CodeEventMetadata>,
    ) -> Result<Option<PushFrameDataResult>, PyErr> {
        let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_ids = self._frame_ids.get_or_default();
        let frame_id = match event {
            Event::Call | Event::Resume | Event::Throw => {
                frame_ids.borrow_mut().get_or_set(event, pyframe_id)
            }
            Event::Return | Event::Unwind | Event::Yield => {
                let mut frame_ids = frame_ids.borrow_mut();
                if frame_ids.take_abandoned(pyframe_id) {
                    return Ok(None);
                }
                let Some(frame_id) = frame_ids.get_option(pyframe_id) else {
                    return Ok(None);
                };
                frame_id
            }
        };
        let processed = (|| -> Result<Option<PushFrameDataResult>, PyErr> {
            let pyframe = frame.cast()?;
            let user_code_call_site = self
                .call_frames
                .get_or_default()
                .borrow_mut()
                .get_user_code_call_site(
                    pyframe,
                    event,
                    &frame_id,
                    metadata.map(|metadata| &metadata.lines),
                )?;

            self.append_encoded_frame(py, |arena, capture| match metadata {
                Some(metadata) => utils::write_frame_with_cached_code_metadata(
                    arena,
                    pyframe,
                    &self.serializer,
                    &self.frame_paths,
                    user_code_call_site,
                    arg,
                    event,
                    name,
                    &frame_id,
                    self.lightweight_repr,
                    self.omit_return_locals,
                    (
                        metadata.relative_path.as_str(),
                        Some(metadata.co_qualname.as_str()),
                        Some(&metadata.native_msgpack_eligible),
                        Some(&*metadata.lines),
                    ),
                    Some(utils::ValueInterningContext::fixed(
                        &self.value_interning,
                        capture,
                    )),
                    self.max_value_bytes,
                ),
                None => utils::write_frame_with_serializer(
                    arena,
                    pyframe,
                    &self.serializer,
                    &self.frame_paths,
                    user_code_call_site,
                    arg,
                    event,
                    name,
                    &frame_id,
                    self.lightweight_repr,
                    self.omit_return_locals,
                    Some(utils::ValueInterningContext::fixed(
                        &self.value_interning,
                        capture,
                    )),
                    self.max_value_bytes,
                ),
            })
            .map(Some)
        })();
        if let Err(err) = &processed {
            self.abandon_entry(py, event, pyframe_id, Some(&frame_id), err);
        }
        processed
    }

    fn code_event_metadata(
        &self,
        code: &Bound<'_, PyCode>,
    ) -> Result<CodeEventMetadataLookup, PyErr> {
        let py = code.py();
        let code_id = code.as_ptr() as usize;
        let local_cache = self.code_metadata_local.get_or_default();
        match local_cache.borrow().get(&code_id) {
            Some(LocalCodeMetadata::Full(metadata)) => {
                return Ok(CodeEventMetadataLookup::Full(metadata.clone()))
            }
            Some(LocalCodeMetadata::Excluded) => return Ok(CodeEventMetadataLookup::Excluded),
            None => {}
        }
        if let Some(metadata) = self
            .code_metadata_cache
            .lock_py_attached(py)
            .expect("code metadata cache mutex poisoned")
            .lookup(code_id)
        {
            match &metadata {
                CodeEventMetadataLookup::Full(metadata) if metadata.include_frame => {
                    local_cache
                        .borrow_mut()
                        .insert(code_id, LocalCodeMetadata::Full(metadata.clone()));
                }
                // A hit means the shared cache retains this code object.
                CodeEventMetadataLookup::Excluded => {
                    local_cache
                        .borrow_mut()
                        .insert(code_id, LocalCodeMetadata::Excluded);
                }
                _ => {}
            }
            return Ok(metadata);
        }

        let filename = code
            .getattr(intern!(py, "co_filename"))?
            .extract::<String>()?;
        if filename.is_empty() {
            return Ok(CodeEventMetadataLookup::Dynamic);
        }

        let name = code.getattr(intern!(py, "co_name"))?.extract::<String>()?;
        let include_frame = self.include_frame(py, &filename)?;
        let has_processor_candidates = self
            .default_include_frames
            .lock_py_attached(py)
            .expect("default_include_frames mutex poisoned")
            .contains_key(&name);

        // An excluded code object with no processor candidates can never emit
        // a frame. Cache only its strong identity marker; paths, qualnames, and
        // native serializer state would be allocated but never read.
        if !include_frame && !has_processor_candidates {
            let mut cache = self
                .code_metadata_cache
                .lock_py_attached(py)
                .expect("code metadata cache mutex poisoned");
            let lookup = cache.insert_excluded(code_id, code.clone().unbind());
            // Past the retention cap the code isn't retained, so its id may be
            // reused by another code object: don't remember it locally.
            if matches!(lookup, CodeEventMetadataLookup::Excluded)
                && cache.entries.contains_key(&code_id)
            {
                local_cache
                    .borrow_mut()
                    .insert(code_id, LocalCodeMetadata::Excluded);
            }
            return Ok(lookup);
        }

        let metadata = Arc::new(CodeEventMetadata {
            _code: code.clone().unbind(),
            relative_path: self.frame_paths.relative_path(&filename),
            co_qualname: code
                .getattr(intern!(py, "co_qualname"))?
                .extract::<String>()?,
            lines: Arc::new(utils::CodeLines::new(code)?),
            native_msgpack_eligible: AtomicBool::new(true),
            include_frame,
            has_processor_candidates,
            filename,
            name,
        });
        let mut cache = self
            .code_metadata_cache
            .lock_py_attached(py)
            .expect("code metadata cache mutex poisoned");
        // Every excluded code object counts toward the retention cap. A matching
        // co_name only makes a plugin frame possible; its path/call predicate may
        // still reject every event, so it is not grounds for unbounded retention.
        let metadata = cache.insert_full(code_id, metadata);
        if let CodeEventMetadataLookup::Full(metadata) = &metadata {
            if metadata.include_frame {
                local_cache
                    .borrow_mut()
                    .insert(code_id, LocalCodeMetadata::Full(metadata.clone()));
            }
        }
        Ok(metadata)
    }

    /// Save a trace point by delegating to the Python monitoring module's helper.
    fn snapshot_value_table_for_capture(&self, capture: &TraceCapture) -> Vec<(u32, Arc<[u8]>)> {
        self.value_interning
            .snapshot_ids(&capture.published_value_ids())
    }

    fn snapshot_current_value_table(&self, py: Python) -> Vec<(u32, Arc<[u8]>)> {
        let capture = self
            .trace_capture
            .lock_py_attached(py)
            .expect("trace capture mutex poisoned")
            .clone();
        self.snapshot_value_table_for_capture(&capture)
    }

    fn save_trace_point(
        &self,
        py: Python,
        thread_id: &str,
        frames_slice: Vec<Vec<u8>>,
        capture: &TraceCapture,
        func_name: &str,
    ) -> Result<(), PyErr> {
        // Convert frame bytes to Python bytes objects
        let py_frames: Vec<Py<PyBytes>> = frames_slice
            .iter()
            .map(|f| PyBytes::new(py, f).unbind())
            .collect();
        let py_value_table: Vec<(u32, Py<PyBytes>)> = self
            .snapshot_value_table_for_capture(capture)
            .iter()
            .map(|(id, value)| (*id, PyBytes::new(py, value).unbind()))
            .collect();

        // Suspend monitoring hooks while we bridge into Python so our own
        // save/emit work is not re-recorded.
        let suspended = thread_hooks::Suspended::new();
        let parent_trace_id = self
            .trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .clone();
        let sqlite_busy_timeout = self.sqlite_busy_timeout;
        let result: PyResult<()> = (|| {
            let config_py_dict = self.config.to_py_dict(py)?;
            let kolo_monitoring = PyModule::import(py, "kolo.monitoring")?;
            let save_fn = kolo_monitoring.getattr("_save_trace_point_from_rust")?;
            save_fn.call1((
                thread_id.to_string(),
                py_frames,
                func_name.to_string(),
                self.db_path.clone(),
                self.source.clone(),
                self.lightweight_repr,
                parent_trace_id,
                config_py_dict,
                sqlite_busy_timeout,
                py_value_table,
            ))?;
            Ok(())
        })();
        drop(suspended);
        result
    }

    fn _monitor_instruction(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let py = code.py();
        let metadata = self.instruction_metadata(code)?;
        let Some(instruction) = metadata.instructions.get(&instruction_offset) else {
            return Ok(Some(self.disable.clone_ref(py)));
        };
        let include_frame = match metadata.include_frame {
            Some(include_frame) => include_frame,
            None => self.include_frame(py, &metadata.filename)?,
        };

        match include_frame {
            true => {
                self.process_instruction(
                    py,
                    &metadata.name,
                    &instruction.variables,
                    instruction.opname,
                    instruction_offset,
                )?;
                Ok(None)
            }
            false => Ok(Some(self.disable.clone_ref(py))),
        }
    }

    fn instruction_metadata(
        &self,
        code: &Bound<'_, PyCode>,
    ) -> Result<Arc<CodeInstructionMetadata>, PyErr> {
        let py = code.py();
        let code_id = code.as_ptr() as usize;
        if let Some(metadata) = self
            .instruction_cache
            .lock_py_attached(py)
            .expect("instruction cache mutex poisoned")
            .get(&code_id)
            .cloned()
        {
            return Ok(metadata);
        }

        let mut instructions = HashMap::new();
        let disassembled = self.get_instructions_fn.bind(py).call1((code,))?;
        for instruction in disassembled.try_iter()? {
            let instruction = instruction?;
            let opname = instruction.getattr(intern!(py, "opname"))?;
            let opname = opname.extract::<&str>()?;
            if !opname.starts_with("STORE_") {
                continue;
            }
            let argval = instruction.getattr(intern!(py, "argval"))?;
            let Some((opname, variables)) = store_targets(opname, &argval) else {
                continue;
            };
            let offset = instruction
                .getattr(intern!(py, "offset"))?
                .extract::<usize>()?;
            instructions.insert(
                offset,
                CachedInstruction {
                    variables: variables.into(),
                    opname,
                },
            );
        }

        let filename = code
            .getattr(intern!(py, "co_filename"))?
            .extract::<String>()?;
        let include_frame = if filename.is_empty() {
            None
        } else {
            Some(self.include_frame(py, &filename)?)
        };
        let metadata = Arc::new(CodeInstructionMetadata {
            _code: code.clone().unbind(),
            filename,
            name: code.getattr(intern!(py, "co_name"))?.extract::<String>()?,
            include_frame,
            instructions,
        });
        let mut cache = self
            .instruction_cache
            .lock_py_attached(py)
            .expect("instruction cache mutex poisoned");
        Ok(cache
            .entry(code_id)
            .or_insert_with(|| metadata.clone())
            .clone())
    }

    fn process_instruction(
        &self,
        py: Python,
        name: &str,
        variables: &Arc<[String]>,
        opname: Opname,
        offset: usize,
    ) -> Result<(), PyErr> {
        let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_id = self
            ._frame_ids
            .get_or_default()
            .borrow()
            .get_option(pyframe_id);
        let pyframe = frame.cast()?;

        let line_frame_data = LineFrame::new(
            self.frame_paths.format_frame_path(pyframe)?,
            name.to_string(),
            utils::get_qualname(pyframe, py)?.expect("qualname always exists on Python 3.12+"),
            frame_id.map(|frame_id| frame_id.as_str().to_owned()),
            utils::timestamp(),
        );
        self.instruction_data
            .get_or_default()
            .replace(Some(InstructionData {
                opname,
                variables: variables.clone(),
                offset,
                line_frame: frame.unbind(),
                line_frame_data,
            }));
        thread_hooks::set_assignment(
            &self.assignment_owner,
            thread_hooks::PENDING_ASSIGNMENT,
            true,
        );
        Ok(())
    }

    /// Record the assignment (and any deferred double-store target) waiting
    /// on this thread.
    ///
    /// `begin_callback` only calls this while the thread's hook state says
    /// one may be waiting, so every other event skips these per-thread
    /// lookups. The state bits are cleared only once nothing is left, so
    /// they may be stale-set (costing one lookup) but never stale-clear.
    fn process_assignment(&self, py: Python) -> Result<(), PyErr> {
        if thread_hooks::assignments_for(&self.assignment_owner) & thread_hooks::DEFERRED_STORE != 0 {
            self.process_deferred_stores(py)?;
        }
        let instruction_data = self.instruction_data.get_or_default().replace(None);
        thread_hooks::set_assignment(
            &self.assignment_owner,
            thread_hooks::PENDING_ASSIGNMENT,
            false,
        );
        let Some(instruction_data) = instruction_data else {
            return Ok(());
        };
        if instruction_data.variables.len() > 1 && self.store_in_progress(py, &instruction_data)? {
            // `STORE_FAST_STORE_FAST` releases the first target's old value
            // before it stores the second, so a finalizer can fire this event
            // in between. Record the second once its frame moves on.
            let (first, rest) = instruction_data.variables.split_at(1);
            self.write_assignments(py, &instruction_data, first)?;
            let rest = Arc::from(rest);
            self.deferred_stores
                .get_or_default()
                .borrow_mut()
                .push(InstructionData {
                    variables: rest,
                    ..instruction_data
                });
            thread_hooks::set_assignment(
                &self.assignment_owner,
                thread_hooks::DEFERRED_STORE,
                true,
            );
            return Ok(());
        }
        self.write_assignments(py, &instruction_data, &instruction_data.variables)
    }

    fn process_deferred_stores(&self, py: Python) -> Result<(), PyErr> {
        let deferred_stores = self.deferred_stores.get_or_default();
        loop {
            let ready = match deferred_stores.borrow().last() {
                None => {
                    thread_hooks::set_assignment(
                        &self.assignment_owner,
                        thread_hooks::DEFERRED_STORE,
                        false,
                    );
                    return Ok(());
                }
                Some(deferred) => !self.store_in_progress(py, deferred)?,
            };
            if !ready {
                return Ok(());
            }
            let deferred = deferred_stores
                .borrow_mut()
                .pop()
                .expect("checked non-empty");
            self.write_assignments(py, &deferred, &deferred.variables)?;
        }
    }

    /// Whether this event fired from inside the store instruction itself: its
    /// frame is not the current one and has not moved past the instruction.
    fn store_in_progress(&self, py: Python, instruction_data: &InstructionData) -> PyResult<bool> {
        let frame = instruction_data.line_frame.bind(py);
        if self.sys_getframe_fn.bind(py).call1((0,))?.is(frame) {
            return Ok(false);
        }
        let lasti = frame.getattr(intern!(py, "f_lasti"))?.extract::<usize>()?;
        Ok(lasti == instruction_data.offset)
    }

    /// Write one line frame per stored variable, in store order.
    ///
    /// A failure to record one variable must not drop the others, so it is
    /// logged and the loop continues unless the writer circuit opened.
    fn write_assignments(
        &self,
        py: Python,
        instruction_data: &InstructionData,
        variables: &[String],
    ) -> PyResult<()> {
        let frame = instruction_data.line_frame.bind(py);
        // Read every target before serializing any: a value's __repr__ could
        // otherwise rebind a later target through the f_locals proxy.
        // A store binds at most two variables; read both without allocating.
        let mut reads = variables
            .iter()
            .filter(|variable| !variable.starts_with('@'))
            .map(|variable| {
                (
                    variable,
                    instruction_data.opname.assignment_value(variable, frame),
                )
            });
        let first = reads.next();
        let second = reads.next();
        debug_assert!(
            reads.next().is_none(),
            "a store binds at most two variables"
        );
        for (variable, value) in first.into_iter().chain(second) {
            let result = (|| {
                let Some(assign) = value? else {
                    return Ok(());
                };
                let push_result = self.append_encoded_frame(py, |arena, _capture| {
                    instruction_data.line_frame_data.write_msgpack_into(
                        arena,
                        &self.serializer,
                        (variable, assign),
                        self.lightweight_repr,
                        self.max_value_bytes,
                    )
                })?;
                self.track_direct_leaf(py, &push_result)
            })();
            if let Err(err) = result {
                if self.writer_circuit_is_open() || utils::reaches_program(py, &err) {
                    return Err(err);
                }
                self.log_error(py, err);
            }
        }
        Ok(())
    }

    fn thread_frame_buffer(&self, py: Python, thread_id: &str) -> Option<Arc<Mutex<FrameStore>>> {
        self.frames_by_thread
            .lock_py_attached(py)
            .expect("frames registry mutex poisoned")
            .get(thread_id)
            .cloned()
    }

    fn register_thread_frame_buffer(
        &self,
        py: Python,
        thread_id: &str,
    ) -> (u64, Arc<Mutex<FrameStore>>) {
        let mut frames_by_thread = self
            .frames_by_thread
            .lock_py_attached(py)
            .expect("frames registry mutex poisoned");
        let generation = self.frame_generation.load(Ordering::Acquire);
        let frame_buffer = frames_by_thread
            .entry(thread_id.to_string())
            .or_insert_with(|| {
                let capture = self
                    .trace_capture
                    .lock_py_attached(py)
                    .expect("trace capture mutex poisoned")
                    .clone();
                let token = u32::try_from(self.next_thread_token.fetch_add(1, Ordering::Relaxed))
                    .expect("Kolo exhausted its per-capture thread token space");
                Arc::new(Mutex::new(FrameStore::new(capture, token)))
            })
            .clone();
        (generation, frame_buffer)
    }

    fn trace_name_for_full_capture(
        &self,
        py: Python,
        frames_by_thread: &HashMap<String, FrameStore>,
    ) -> Option<String> {
        let mut trace_name = self
            .trace_name
            .lock_py_attached(py)
            .expect("mutex poisoned");
        let current_frames = frames_by_thread.get(&self.current_thread_id);
        match current_frames {
            Some(current_frames) => match current_frames.trace_name_observations() {
                // Every plugin frame enters through push_frame_data's typed
                // batch append. Direct append_encoded_frame calls emit only
                // native execution events, none of which names a trace, so a
                // complete empty index is authoritative.
                Some(observations) => utils::resolve_full_trace_name(
                    &mut trace_name,
                    observations,
                    current_frames.len(),
                ),
                None => utils::resolve_trace_name(
                    &mut trace_name,
                    frames_by_thread,
                    &self.current_thread_id,
                    true,
                ),
            },
            None => utils::resolve_full_trace_name(&mut trace_name, &[], 0),
        }
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

    fn take_trace_inputs(
        &self,
        py: Python,
    ) -> PyResult<(
        HashMap<String, FrameStore>,
        HashMap<String, Py<PyAny>>,
        String,
        String,
        f64,
        Arc<TraceCapture>,
        Vec<(u32, Arc<[u8]>)>,
    )> {
        let (frames_by_thread, trace_id, root_trace_id, timestamp, previous_capture) = {
            let flush_barrier = self.flush_barrier.for_this_process();
            let _flush_barrier = flush_barrier.lock_py_attached(py).expect("mutex");
            let mut trace_id_guard = self.trace_id.lock_py_attached(py).expect("mutex poisoned");
            let mut root_trace_id_guard = self
                .root_trace_id
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let timestamp = *self
                .timestamp
                .lock_py_attached(py)
                .expect("timestamp mutex poisoned");
            let frame_buffers = {
                let mut frames_by_thread = self
                    .frames_by_thread
                    .lock_py_attached(py)
                    .expect("mutex poisoned");
                // Bump while holding the registry lock. An appender that
                // already holds an old buffer either completes before we drain
                // it, or observes the new generation and retries below.
                self.frame_generation.fetch_add(1, Ordering::AcqRel);
                let frame_buffers = std::mem::take(&mut *frames_by_thread);
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
                    TraceCapture::for_trace(&self.db_path, &trace_id_guard, timestamp);
                if forked || capture.is_in_memory() {
                    replacement_capture.keep_in_memory();
                }
                let previous_capture = std::mem::replace(&mut *capture, replacement_capture);
                (frame_buffers, previous_capture)
            };
            let trace_id = trace_id_guard.clone();
            let root_trace_id = root_trace_id_guard.clone();
            drop(root_trace_id_guard);
            drop(trace_id_guard);
            let (frame_buffers, previous_capture) = frame_buffers;
            let frames_by_thread = frame_buffers
                .into_iter()
                .map(|(thread_id, buffer)| {
                    let frames = buffer
                        .lock_py_attached(py)
                        .expect("frame buffer poisoned")
                        .take();
                    (thread_id, frames)
                })
                .collect();
            self.reset_subtree_tracking(py);
            (
                frames_by_thread,
                trace_id,
                root_trace_id,
                timestamp,
                previous_capture,
            )
        };

        // `ValueInterning` lives for the monitor lifetime, while captures
        // rotate. Materialized snapshots must carry only IDs actually
        // referenced by the retired capture; otherwise a long-lived monitor
        // would copy its entire bounded table into every later small trace.
        let value_table = self
            .value_interning
            .snapshot_ids(&previous_capture.published_value_ids());

        let threads: HashMap<String, Py<PyAny>> = self
            .threads
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .iter()
            .map(|(thread_id, thread)| (thread_id.clone(), thread.clone_ref(py)))
            .collect();

        Ok((
            frames_by_thread,
            threads,
            trace_id,
            root_trace_id,
            timestamp,
            previous_capture,
            value_table,
        ))
    }

    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let (frames_by_thread, threads, trace_id, root_trace_id, timestamp, _capture, value_table) =
            self.take_trace_inputs(py)?;
        let trace_name = self.trace_name_for_full_capture(py, &frames_by_thread);
        // A callback publishes its Python Thread object before it appends its
        // first frame. A concurrent snapshot can therefore legitimately have
        // thread metadata without a frame store. Give those empty threads a
        // container-local token as well so the snapshot remains complete.
        let thread_tokens = self.snapshot_thread_tokens(&frames_by_thread, &threads)?;
        let prepared = utils::prepare_v3_trace_from_parts(
            py,
            &threads,
            &thread_tokens,
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            timestamp,
            &self.config,
            true, // use_monitoring
            Some(&root_trace_id),
        )?;
        let data = super::trace_container::build_container_bytes(
            &trace_id,
            timestamp,
            &frames_by_thread,
            &thread_tokens,
            prepared.thread_meta,
            prepared.metadata,
            value_table,
        )
        .map_err(pyo3::exceptions::PyOSError::new_err)?;
        Ok(PyBytes::new(py, &data).unbind())
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
        let mut stacks = self.subtree_stack.lock_py_attached(py).expect("mutex");
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
        let subtree_stack = self.subtree_stack.lock_py_attached(py).expect("mutex");
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
        let mut stacks = self.subtree_stack.lock_py_attached(py).expect("mutex");
        subtree_flush::shift_flush_state_after_flush(
            stacks.get_mut(thread_id),
            start_index,
            end_index,
            resident_delta,
        );
    }

    fn maybe_flush_segments_with_current_bytes(
        &self,
        py: Python,
        thread_id: &str,
        current_bytes: usize,
    ) -> PyResult<()> {
        // An exit recorded without its values, or this deep in the stack:
        // leave flushing (Python calls, large allocations) to a later event.
        if utils::values_omitted() || !utils::room_to_flush() {
            return Ok(());
        }
        let low_water_bytes = {
            let mut flush_in_progress = self.flush_in_progress.lock_py_attached(py).expect("mutex");
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
            &mut self.flush_in_progress.lock_py_attached(py).expect("mutex"),
            thread_id,
        );
        result
    }

    fn maybe_flush_current_thread(&self, py: Python) -> PyResult<()> {
        let flush_state = self.flush_thread_state.get_or_default();
        // This runs in the same callback as the append. Trace-point bridging
        // suspends monitoring hooks, so no event on this thread can change the
        // TLS state between the push result and this deferred read.
        let (thread_id, current_bytes, armed) = {
            let state = flush_state.borrow();
            (state.thread_id.clone(), state.cumulative_bytes, state.armed)
        };
        if armed {
            if let Some(thread_id) = thread_id {
                return self.maybe_flush_segments_with_current_bytes(py, &thread_id, current_bytes);
            }
        }
        Ok(())
    }

    fn push_frames_call(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
        frame_types: Vec<String>,
        co_name: &str,
    ) -> Result<(), PyErr> {
        let mut drained_count = 0;
        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                if frame_type.as_str() == "start_test" {
                    frames.drain(..index);
                    drained_count = index;
                    self.start_test(py)?
                }
            }
        }

        let remaining_frame_types = &frame_types[drained_count..];
        let push_result = self.push_frame_data(py, frames, remaining_frame_types, false)?;
        let Some(push_result) = push_result else {
            return Ok(());
        };

        if push_result.flush_tracking_armed
            && remaining_frame_types
                .iter()
                .any(|frame_type| frame_type == "frame")
        {
            subtree_flush::push_open_subtree(
                &mut self.subtree_stack.lock_py_attached(py).expect("mutex"),
                &push_result.thread_id,
                OpenSubtree {
                    start_index: push_result.start_index,
                    start_bytes: push_result
                        .current_bytes
                        .saturating_sub(push_result.added_bytes),
                    co_name: co_name.to_string(),
                    flush_candidate: None,
                },
            );
            self.maybe_flush_segments_with_current_bytes(
                py,
                &push_result.thread_id,
                push_result.current_bytes,
            )?;
        }
        Ok(())
    }

    fn push_frames_return(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
        frame_types: &mut [String],
        flush_after: bool,
    ) -> Result<(), PyErr> {
        frames.reverse();
        frame_types.reverse();
        let mut drained_count = 0;
        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                if frame_type.as_str() == "end_test" {
                    let mut before: Vec<SerializedFrame> = frames.drain(..index + 1).collect();
                    drained_count = index + 1;
                    self.push_frame_data(py, &mut before, &frame_types[..index + 1], true)?;
                    self.save(py)?;
                    self.reset_subtree_tracking(py);
                    // save() drained frames_by_thread via mem::take, so any
                    // surviving OnReturn trace-point markers now index into a
                    // buffer that no longer exists. Walk each thread's marker
                    // stack back to (and including) the Test sentinel pushed
                    // by the matching start_test, dropping the in-flight
                    // OnReturn markers that sat above it. Matches the
                    // stack-walk model the Python monitor uses so any future
                    // marker kinds can coexist on a single stack.
                    self.drop_markers_through_test_sentinel(py);
                }
            }
        }

        let remaining_frame_types = &frame_types[drained_count..];
        let Some(push_result) = self.push_frame_data(py, frames, remaining_frame_types, false)?
        else {
            return Ok(());
        };

        if push_result.flush_tracking_armed
            && remaining_frame_types
                .iter()
                .any(|frame_type| frame_type == "frame")
        {
            let thread_id = push_result.thread_id;
            let subtree = subtree_flush::pop_open_subtree(
                &mut self.subtree_stack.lock_py_attached(py).expect("mutex"),
                &thread_id,
            );
            if let Some(subtree) = subtree {
                let subtree_bytes = push_result
                    .current_bytes
                    .saturating_sub(subtree.start_bytes);
                self.record_closed_segment(
                    py,
                    &thread_id,
                    subtree.start_index,
                    push_result.end_index,
                    subtree_bytes,
                    subtree.co_name,
                );
            }
            if flush_after {
                self.maybe_flush_segments_with_current_bytes(
                    py,
                    &thread_id,
                    push_result.current_bytes,
                )?;
            }
        }
        Ok(())
    }

    fn track_direct_frame(
        &self,
        py: Python,
        event: Event,
        co_name: &str,
        push_result: &PushFrameDataResult,
        flush_after: bool,
    ) -> PyResult<()> {
        if !push_result.flush_tracking_armed {
            return Ok(());
        }
        match event {
            Event::Call | Event::Resume | Event::Throw => {
                subtree_flush::push_open_subtree(
                    &mut self.subtree_stack.lock_py_attached(py).expect("mutex"),
                    &push_result.thread_id,
                    OpenSubtree {
                        start_index: push_result.start_index,
                        start_bytes: push_result
                            .current_bytes
                            .saturating_sub(push_result.added_bytes),
                        co_name: co_name.to_string(),
                        flush_candidate: None,
                    },
                );
            }
            Event::Return | Event::Unwind | Event::Yield => {
                let subtree = subtree_flush::pop_open_subtree(
                    &mut self.subtree_stack.lock_py_attached(py).expect("mutex"),
                    &push_result.thread_id,
                );
                if let Some(subtree) = subtree {
                    self.record_closed_segment(
                        py,
                        &push_result.thread_id,
                        subtree.start_index,
                        push_result.end_index,
                        push_result
                            .current_bytes
                            .saturating_sub(subtree.start_bytes),
                        subtree.co_name,
                    );
                }
            }
        }
        if flush_after {
            self.maybe_flush_segments_with_current_bytes(
                py,
                &push_result.thread_id,
                push_result.current_bytes,
            )?;
        }
        Ok(())
    }

    fn track_direct_leaf(&self, py: Python, push_result: &PushFrameDataResult) -> PyResult<()> {
        if !push_result.flush_tracking_armed {
            return Ok(());
        }
        let Some(frame_buffer) = self.thread_frame_buffer(py, &push_result.thread_id) else {
            return Ok(());
        };
        let co_name = {
            let frames = frame_buffer
                .lock_py_attached(py)
                .expect("thread frame buffer poisoned");
            subtree_flush::extract_co_name_range(
                &*frames,
                push_result.start_index..push_result.end_index,
            )
        };
        self.record_closed_segment(
            py,
            &push_result.thread_id,
            push_result.start_index,
            push_result.end_index,
            push_result.added_bytes,
            co_name,
        );
        self.maybe_flush_segments_with_current_bytes(
            py,
            &push_result.thread_id,
            push_result.current_bytes,
        )
    }

    fn append_encoded_frame<F>(&self, py: Python, encode: F) -> PyResult<PushFrameDataResult>
    where
        F: FnOnce(&mut Vec<u8>, &TraceCapture) -> Result<(), PyErr>,
    {
        let flush_state = self.flush_thread_state.get_or_default();
        let cached_thread_id = {
            let flush_state = flush_state.borrow();
            flush_state.thread_id.clone()
        };
        let thread_id = if let Some(thread_id) = cached_thread_id {
            thread_id
        } else {
            let suspended = thread_hooks::Suspended::new();
            let resolved_thread_id: PyResult<String> = (|| {
                let current_thread = self.current_thread_fn.bind(py).call0()?;
                let thread_id = utils::get_thread_id(current_thread.as_ref(), py)?;
                self.threads
                    .lock_py_attached(py)
                    .expect("mutex poisoned")
                    .entry(thread_id.clone())
                    .or_insert_with(|| current_thread.into());
                Ok(thread_id)
            })();
            drop(suspended);
            let thread_id = resolved_thread_id?;
            let thread_id = Arc::new(thread_id);
            flush_state.borrow_mut().thread_id = Some(thread_id.clone());
            thread_id
        };

        let mut encode = Some(encode);
        let appended = loop {
            let generation = self.frame_generation.load(Ordering::Acquire);
            let cached_buffer = {
                let state = flush_state.borrow();
                if state.frame_generation == generation {
                    state.frame_buffer.clone()
                } else {
                    None
                }
            };
            let (generation, frame_buffer) = if let Some(frame_buffer) = cached_buffer {
                (generation, frame_buffer)
            } else {
                let (generation, frame_buffer) = self.register_thread_frame_buffer(py, &thread_id);
                let mut state = flush_state.borrow_mut();
                state.frame_generation = generation;
                state.frame_buffer = Some(frame_buffer.clone());
                (generation, frame_buffer)
            };
            let mut thread_frames = frame_buffer
                .lock_py_attached(py)
                .expect("thread frame buffer poisoned");
            if self.frame_generation.load(Ordering::Acquire) != generation {
                continue;
            }
            break thread_frames.append_encoded(
                encode
                    .take()
                    .expect("frame encoder is consumed only after generation validation"),
            )?;
        };

        let flush_enabled = self.flush_subtree_bytes.is_some();
        if !flush_enabled {
            return Ok(PushFrameDataResult {
                thread_id,
                start_index: appended.start_index,
                end_index: appended.end_index,
                added_bytes: 0,
                current_bytes: 0,
                flush_tracking_armed: false,
            });
        }

        let (added_bytes, current_bytes, flush_tracking_armed) = {
            let mut state = flush_state.borrow_mut();
            let generation = self.flush_generation.load(Ordering::Relaxed);
            if state.generation != generation {
                state.cumulative_bytes = 0;
                state.armed = false;
                state.generation = generation;
            }
            state.cumulative_bytes += appended.added_bytes;
            if state.armed || self.tracking_start_bytes == 0 {
                state.armed = true;
                (appended.added_bytes, state.cumulative_bytes, true)
            } else if state.cumulative_bytes < self.tracking_start_bytes {
                (0, state.cumulative_bytes, false)
            } else {
                state.armed = true;
                (appended.added_bytes, state.cumulative_bytes, true)
            }
        };
        Ok(PushFrameDataResult {
            thread_id,
            start_index: appended.start_index,
            end_index: appended.end_index,
            added_bytes,
            current_bytes,
            flush_tracking_armed,
        })
    }

    fn push_frame_data(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
        frame_types: &[String],
        record_closed_leaf: bool,
    ) -> PyResult<Option<PushFrameDataResult>> {
        if frames.is_empty() {
            return Ok(None);
        }

        let flush_state = self.flush_thread_state.get_or_default();
        let cached_thread_id = {
            let flush_state = flush_state.borrow();
            flush_state.thread_id.clone()
        };
        let thread_id = if let Some(thread_id) = cached_thread_id {
            thread_id
        } else {
            let suspended = thread_hooks::Suspended::new();

            let resolved_thread_id: PyResult<String> = (|| {
                let current_thread = self.current_thread_fn.bind(py).call0()?;
                let thread_id = utils::get_thread_id(current_thread.as_ref(), py)?;
                self.threads
                    .lock_py_attached(py)
                    .expect("mutex poisoned")
                    .entry(thread_id.clone())
                    .or_insert_with(|| current_thread.into());
                Ok(thread_id)
            })();

            drop(suspended);

            let thread_id = resolved_thread_id?;
            let thread_id = Arc::new(thread_id);
            flush_state.borrow_mut().thread_id = Some(thread_id.clone());
            thread_id
        };

        let flush_enabled = self.flush_subtree_bytes.is_some();
        let (start_index, end_index, appended_bytes, frame_buffer) = loop {
            let generation = self.frame_generation.load(Ordering::Acquire);
            let cached_buffer = {
                let state = flush_state.borrow();
                if state.frame_generation == generation {
                    state.frame_buffer.clone()
                } else {
                    None
                }
            };
            let (generation, frame_buffer) = if let Some(frame_buffer) = cached_buffer {
                (generation, frame_buffer)
            } else {
                let (generation, frame_buffer) = self.register_thread_frame_buffer(py, &thread_id);
                let mut state = flush_state.borrow_mut();
                state.frame_generation = generation;
                state.frame_buffer = Some(frame_buffer.clone());
                (generation, frame_buffer)
            };
            let mut thread_frames = frame_buffer
                .lock_py_attached(py)
                .expect("thread frame buffer poisoned");
            // Recheck after taking the buffer lock so build_trace cannot
            // detach this buffer between validation and append.
            if self.frame_generation.load(Ordering::Acquire) != generation {
                continue;
            }
            let appended = thread_frames
                .append_many_with_frame_types(frames, frame_types)
                .map_err(pyo3::exceptions::PyOSError::new_err)?;
            drop(thread_frames);
            break (
                appended.start_index,
                appended.end_index,
                appended.added_bytes,
                frame_buffer,
            );
        };

        // Fast path: flush disabled — no tracking at all
        if !flush_enabled {
            return Ok(Some(PushFrameDataResult {
                thread_id,
                start_index,
                end_index,
                added_bytes: 0,
                current_bytes: 0,
                flush_tracking_armed: false,
            }));
        }
        let (added_bytes, current_bytes, flush_tracking_armed) = {
            let mut state = flush_state.borrow_mut();
            let generation = self.flush_generation.load(Ordering::Relaxed);
            if state.generation != generation {
                state.cumulative_bytes = 0;
                state.armed = false;
                state.generation = generation;
            }

            state.cumulative_bytes += appended_bytes;
            if state.armed || self.tracking_start_bytes == 0 {
                state.armed = true;
                (appended_bytes, state.cumulative_bytes, true)
            } else if state.cumulative_bytes < self.tracking_start_bytes {
                (0, state.cumulative_bytes, false)
            } else {
                state.armed = true;
                (appended_bytes, state.cumulative_bytes, true)
            }
        };

        if record_closed_leaf {
            let co_name = {
                let thread_frames = frame_buffer
                    .lock_py_attached(py)
                    .expect("thread frame buffer poisoned");
                (start_index < end_index && end_index <= thread_frames.len()).then(|| {
                    subtree_flush::extract_co_name_range(&*thread_frames, start_index..end_index)
                })
            };
            if let Some(co_name) = co_name {
                self.record_closed_segment(
                    py,
                    &thread_id,
                    start_index,
                    end_index,
                    added_bytes,
                    co_name,
                );
                self.maybe_flush_segments_with_current_bytes(py, &thread_id, current_bytes)?;
            }
        }
        Ok(Some(PushFrameDataResult {
            thread_id,
            start_index,
            end_index,
            added_bytes,
            current_bytes,
            flush_tracking_armed,
        }))
    }

    fn start_test(&self, py: Python) -> PyResult<()> {
        let flush_barrier = self.flush_barrier.for_this_process();
        let _flush_barrier = flush_barrier.lock_py_attached(py).expect("mutex");
        // Set a new `self.trace_id`.
        let trace_id = utils::trace_id();
        let mut self_trace_id = self.trace_id.lock_py_attached(py).expect("mutex poisoned");
        *self_trace_id = trace_id.clone();
        let mut self_root_trace_id = self
            .root_trace_id
            .lock_py_attached(py)
            .expect("mutex poisoned");
        *self_root_trace_id = trace_id.clone();
        drop(self_trace_id);
        drop(self_root_trace_id);
        *self
            .trace_name
            .lock_py_attached(py)
            .expect("mutex poisoned") = self.explicit_trace_name.clone();

        // Detach and empty every old buffer. A thread-local slot can retain
        // its Arc after the registry is cleared, including after that OS
        // thread exits, so clearing only the registry would retain the old
        // frames and Vec capacity until the slot is reused or the monitor is
        // dropped.
        let timestamp = *self
            .timestamp
            .lock_py_attached(py)
            .expect("timestamp mutex poisoned");
        let replacement_capture = TraceCapture::for_trace(&self.db_path, &trace_id, timestamp);
        let (frame_buffers, previous_capture) = {
            let mut frames_by_thread = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            self.frame_generation.fetch_add(1, Ordering::AcqRel);
            let frame_buffers = std::mem::take(&mut *frames_by_thread);
            let mut capture = self
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex poisoned");
            if capture.enter_post_fork_mode() || capture.is_in_memory() {
                replacement_capture.keep_in_memory();
            }
            let previous_capture = std::mem::replace(&mut *capture, replacement_capture);
            (frame_buffers, previous_capture)
        };
        discard_frame_buffers(py, frame_buffers);
        drop(previous_capture);

        // Walk each thread's marker stack back through the previous test's
        // Test sentinel (if any), dropping OnReturn markers that point into
        // the frame buffer we just wiped, then push a fresh Test sentinel on
        // every currently-known thread. New threads that push OnReturn
        // markers later in this test will stack above this sentinel, and
        // end_test walks back to it to drop them cleanly.
        {
            let threads_snapshot: Vec<String> = self
                .threads
                .lock_py_attached(py)
                .expect("threads mutex")
                .keys()
                .cloned()
                .collect();
            let mut markers = self
                .trace_point_markers
                .lock_py_attached(py)
                .expect("markers mutex");
            // Drop any leftover markers from the previous test. Frame
            // indices referenced by OnReturn markers were invalidated when
            // start_test wiped frames_by_thread.
            markers.clear();
            for thread_id in threads_snapshot {
                markers.entry(thread_id).or_default().push(MarkerKind::Test);
            }
        }

        self.reset_subtree_tracking(py);
        Ok(())
    }

    /// Walk each thread's marker stack from the top, dropping OnReturn
    /// markers until (and including) the first `MarkerKind::Test` sentinel.
    /// If a thread has no sentinel, the stack is cleared entirely. Matches
    /// the Python `one_trace_per_test` end_test behaviour.
    fn drop_markers_through_test_sentinel(&self, py: Python) {
        let mut markers = self
            .trace_point_markers
            .lock_py_attached(py)
            .expect("markers mutex");
        markers.retain(|_thread_id, stack| {
            while let Some(top) = stack.last() {
                match top {
                    MarkerKind::Test => {
                        stack.pop();
                        break;
                    }
                    MarkerKind::OnReturn { .. } => {
                        stack.pop();
                    }
                }
            }
            !stack.is_empty()
        });
    }

    fn reset_subtree_tracking(&self, py: Python) {
        // Bump generation to invalidate all TLS flush state lazily
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
        let flush_barrier = self.flush_barrier.for_this_process();
        let _flush_barrier = flush_barrier.lock_py_attached(py).expect("mutex");
        let Some(frame_buffer) = self.thread_frame_buffer(py, thread_id) else {
            return Ok(());
        };
        let mut restore_guard = {
            let mut frames = frame_buffer
                .lock_py_attached(py)
                .expect("thread frame buffer poisoned");
            if candidate.start_index >= frames.len() || candidate.end_index > frames.len() {
                return Ok(());
            }

            let subtree_frames = frames
                .drain(candidate.start_index..candidate.end_index)
                .map_err(pyo3::exceptions::PyOSError::new_err)?;
            RestoreGuard::new(
                frame_buffer.clone(),
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
            let guard = self.threads.lock_py_attached(py).expect("mutex");
            if let Some(thread) = guard.get(thread_id) {
                threads.insert(thread_id.to_string(), thread.clone_ref(py));
            }
            threads
        };
        let trace_name =
            self.trace_name_for_thread(py, restore_guard.subtree_by_thread(), thread_id);

        let suspended = thread_hooks::Suspended::new();
        let root_trace_id = self
            .root_trace_id
            .lock_py_attached(py)
            .expect("mutex")
            .clone();
        let value_table = self.snapshot_current_value_table(py);
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
            true,
            Some(&root_trace_id),
            value_table,
            &self.db_path,
            self.sqlite_busy_timeout,
            false,
        );
        drop(suspended);
        if let Err(err) = save_result {
            return Err(err);
        }
        let placeholder_len = placeholder_buf.len();
        let mut frames = frame_buffer
            .lock_py_attached(py)
            .expect("thread frame buffer poisoned");
        if candidate.start_index > frames.len() {
            return Err(pyo3::exceptions::PyRuntimeError::new_err(format!(
                "frame buffer changed while finalizing flushed subtree {subtrace_id}",
            )));
        }
        frames
            .insert_frame(candidate.start_index, placeholder_buf)
            .map_err(pyo3::exceptions::PyOSError::new_err)?;
        restore_guard.disarm();
        drop(frames);

        // Fix up trace point markers for the drained range: drop any
        // OnReturn marker that pointed inside it, shift OnReturn markers past
        // it down to account for the placeholder replacement. Test sentinels
        // carry no frame index so they pass through untouched.
        {
            let mut markers = self
                .trace_point_markers
                .lock_py_attached(py)
                .expect("markers mutex");
            if let Some(stack) = markers.get_mut(thread_id) {
                let start_index = candidate.start_index;
                let end_index = candidate.end_index;
                let shift = end_index - start_index - 1;
                stack.retain(|m| match m {
                    MarkerKind::Test => true,
                    MarkerKind::OnReturn { start, .. } => {
                        *start < start_index || *start >= end_index
                    }
                });
                for marker in stack.iter_mut() {
                    if let MarkerKind::OnReturn { start, .. } = marker {
                        if *start >= end_index {
                            *start -= shift;
                        }
                    }
                }
                if stack.is_empty() {
                    markers.remove(thread_id);
                }
            }
        }

        {
            let flush_state = self.flush_thread_state.get_or_default();
            let mut state = flush_state.borrow_mut();
            state.cumulative_bytes = state.cumulative_bytes.saturating_sub(flushed_bytes);
            state.cumulative_bytes += placeholder_len;
        }

        subtree_flush::clear_flush_candidate(
            owner,
            &mut self.subtree_stack.lock_py_attached(py).expect("mutex"),
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

    /// Check if we should include the current frame in the trace.
    fn include_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        filters::include_frame(py, filename, &self.include_frames, &self.ignore_frames)
    }

    fn log_error(&self, py: Python, err: PyErr) {
        let args = PyTuple::new(py, ["Unexpected exception in Rust."])
            .expect("a one-string tuple always builds");
        utils::log_warning(py, args, Some(err));
    }

    /// Run a `sys.monitoring` callback without letting a Kolo panic escape.
    ///
    /// PyO3 would turn a panic into a `PanicException` raised inside the
    /// user's code. Instead we stop all Kolo events and report it once.
    ///
    /// Everything that can settle an event without Kolo recording anything
    /// runs first, cheapest first: the thread's hook state (Kolo's own
    /// threads and save sections), then, for code this thread already knows
    /// is excluded, a lookup in its own cache. Only events Kolo may record pay
    /// for the stack check and the per-thread bookkeeping.
    /// Only errors which `utils::reaches_program` are raised.
    fn guarded_callback(
        &self,
        py: Python,
        event: Event,
        stack_event: utils::StackEvent,
        source: CallbackSource<'_, '_>,
        callback: impl FnOnce(Option<LocalCodeMetadata>) -> Result<Option<Py<PyAny>>, PyErr>,
    ) -> PyResult<Py<PyAny>> {
        // Every DISABLE goes through `owned_result`, whichever path makes it.
        let session = self.session_epoch.load(Ordering::Relaxed);
        let hooks = thread_hooks::get();
        if hooks & thread_hooks::OFF != 0 {
            let result = self.hooks_off_result(py, event, hooks, source);
            return Ok(self.owned_result(py, result, session));
        }
        if self.panicked.load(Ordering::Relaxed) {
            let result = self.disabled_result(py, event);
            return Ok(self.owned_result(py, result, session));
        }
        // This monitor's assignment bookkeeping waiting on this thread.
        // Another monitor's entries are never ours to process or clear; a
        // dead monitor's are dropped here.
        let waiting = if hooks & thread_hooks::ASSIGNMENTS != 0 {
            let waiting = thread_hooks::assignments_for(&self.assignment_owner);
            if waiting == 0 {
                thread_hooks::drop_dead_assignments();
            }
            waiting
        } else {
            0
        };
        // One lookup in this thread's cache, reused by `monitor`. An
        // assignment waiting to be recorded must be recorded at this event,
        // so only take the excluded shortcut when none is.
        let local = match source {
            CallbackSource::Code(code) | CallbackSource::Unwind(code, _) => {
                self.local_code_metadata(code)
            }
            _ => None,
        };
        if waiting == 0 && matches!(local, Some(LocalCodeMetadata::Excluded)) {
            let result = self.static_disable(py, event);
            return Ok(self.owned_result(py, result, session));
        }
        // Cached-excluded code returned above without the stack check: it is
        // never recorded, and its entries were forgotten when the callback
        // that cached it returned DISABLE (below), so no exit is owed.
        let (stack, stack_event, omitting) = match source {
            CallbackSource::Code(code) => utils::check_stack_with(stack_event, |code_id| {
                Some(near_end_frame_id(code).unwrap_or(code_id))
            }),
            CallbackSource::Unwind(code, offset) => {
                utils::check_stack_with(stack_event, |code_id| {
                    // CPython never reported this frame's start: no entry.
                    if before_first_resume(code, offset) {
                        return None;
                    }
                    Some(near_end_frame_id(code).unwrap_or(code_id))
                })
            }
            _ => utils::check_stack_with(stack_event, Some),
        };
        // Not DISABLE: the same code runs fine again with more stack free.
        if stack == utils::StackDecision::Skip {
            return Ok(py.None());
        }
        let result = catch_unwind(AssertUnwindSafe(|| {
            let interrupt = match self.begin_callback(py, event, waiting) {
                Ok(Some(disabled)) => return Ok(disabled),
                Ok(None) => None,
                // An interrupt from recording the previous assignment. At an
                // entry, record the entry first so the unwind CPython then
                // reports matches it; at an unwind, which CPython does not
                // report again, record it first too. Elsewhere (a return or
                // yield, reported again as an unwind, and INSTRUCTION events,
                // whose instruction then never runs) raise before this event
                // touches any state.
                Err(err)
                    if matches!(stack_event, utils::StackEvent::Enter(_))
                        || matches!(event, Event::Unwind) =>
                {
                    Some(err)
                }
                Err(err) => return Err(err),
            };
            let result = self.return_or_log(py, callback(local));
            match interrupt {
                Some(err) if result.is_ok() => Err(err),
                _ => result,
            }
        }));
        if let Some(omitting) = omitting {
            omitting.restore();
        }
        match result {
            Ok(result) => result.map(|result| {
                if let utils::StackEvent::Enter(id) = stack_event {
                    // Kolo filtered this frame out and its exits will skip
                    // the stack check: forget it, so a later frame at its
                    // address can't match it once it's gone. A PY_THROW
                    // can't be disabled, so look its code up instead.
                    let filtered = result.bind(py).is(self.disable.bind(py))
                        || matches!((event, source), (Event::Throw, CallbackSource::Code(code))
                            if matches!(self.local_code_metadata(code), Some(LocalCodeMetadata::Excluded)));
                    if filtered {
                        utils::forget_entry(id);
                    }
                }
                self.owned_result(py, result, session)
            }),
            Err(payload) => {
                if !self.panicked.swap(true, Ordering::Relaxed) {
                    self.disable_events(py);
                    utils::report_panic(py, payload);
                }
                Ok(py.None())
            }
        }
    }

    /// Drop a DISABLE returned outside the session the callback started in.
    ///
    /// A callback can outlive its session by releasing the GIL (a plugin
    /// matcher or a `__repr__` running on another thread), and one can start
    /// during teardown, between `set_active(false)` and the callbacks being
    /// unregistered. By then the tool ID may belong to another tool, or to
    /// another Kolo session, and CPython applies DISABLE to whichever tool
    /// holds the ID, silently switching the location off for it. Leaving the
    /// location enabled is always sound.
    ///
    /// Both flags are read with the GIL held, and `set_active` needs the GIL
    /// too, so Relaxed is enough. Without the GIL CPython applies DISABLE
    /// after this check, so a teardown on another thread can still slip in
    /// between.
    fn owned_result(&self, py: Python, result: Py<PyAny>, session: u64) -> Py<PyAny> {
        if result.bind(py).is(self.disable.bind(py))
            && (self.session_epoch.load(Ordering::Relaxed) != session
                || !self.active.load(Ordering::Relaxed))
        {
            return py.None();
        }
        result
    }

    fn return_or_log(
        &self,
        py: Python,
        value: Result<Option<Py<PyAny>>, PyErr>,
    ) -> PyResult<Py<PyAny>> {
        match value {
            Ok(Some(disable)) => Ok(disable),
            Ok(None) => Ok(py.None()),
            Err(err) if utils::reaches_program(py, &err) => Err(err),
            Err(err) => {
                self.log_error(py, err);
                self.disable_events_after_writer_circuit(py);
                Ok(py.None())
            }
        }
    }

    fn disable_events_after_writer_circuit(&self, py: Python) {
        if !self.writer_circuit_is_open() {
            return;
        }
        // This runs only on the callback which observes the storage timeout.
        // Turning events off here avoids imposing an atomic circuit check on
        // every healthy callback. Keep `active` true so normal teardown still
        // unregisters callbacks and releases the tool ID.
        self.disable_events(py);
    }

    fn disable_events(&self, py: Python) {
        // A callback that outlived its session (it released the GIL) must not
        // turn off the events of a tool now armed for idle callbacks or for
        // another session.
        if !self.active.load(Ordering::Acquire) {
            return;
        }
        let _ = PyModule::import(py, "sys")
            .and_then(|sys| sys.getattr("monitoring"))
            .and_then(|monitoring| monitoring.call_method1("set_events", (self.tool_id, 0)));
    }

    /// Whether this thread has cached `code` as excluded. Never computes
    /// anything and never blocks.
    #[inline]
    fn cached_excluded(&self, code: &Bound<'_, PyCode>) -> bool {
        matches!(
            self.local_code_metadata(code),
            Some(LocalCodeMetadata::Excluded)
        )
    }

    /// Whether this monitor's filters statically exclude `code`, deciding it
    /// if no thread has yet. Never blocks and never panics out of a callback:
    /// it takes no lock a session callback might hold (the plugin mutex is
    /// held across plugin code, which could wait on this very thread), and
    /// any failure answers "not excluded", which only costs a later callback.
    fn statically_excluded(&self, code: &Bound<'_, PyCode>) -> bool {
        if self.cached_excluded(code) {
            return true;
        }
        // The same decision the idle filter makes between sessions, from
        // this monitor's immutable filters and plugin filenames.
        catch_unwind(AssertUnwindSafe(|| {
            matches!(self.idle.session_may_record(code), Ok(false))
        }))
        .unwrap_or(false)
    }

    /// This thread's cached metadata for `code`. An entry inherited from a
    /// dead thread's recycled slot is as valid as a fresh one: every entry
    /// holds for this whole monitor.
    #[inline]
    fn local_code_metadata(&self, code: &Bound<'_, PyCode>) -> Option<LocalCodeMetadata> {
        let code_id = code.as_ptr() as usize;
        let cache = self.code_metadata_local.get()?;
        let cache = cache.try_borrow().ok()?;
        cache.get(&code_id).cloned()
    }

    /// The result for an event on a thread whose hooks are off.
    fn hooks_off_result(
        &self,
        py: Python,
        event: Event,
        hooks: u8,
        source: CallbackSource<'_, '_>,
    ) -> Py<PyAny> {
        // Code the filters statically exclude is off for every thread, so
        // DISABLE it whichever thread runs it first, without marking the
        // session (the idle filter would disable it too). This is how Kolo's
        // own save/emit/upload code on its workers stops firing.
        if let CallbackSource::Code(code) | CallbackSource::Unwind(code, _) = source {
            if self.statically_excluded(code) {
                return self.static_disable(py, event);
            }
        }
        if hooks & thread_hooks::WORKER == 0 {
            // A save section on a traced thread runs Kolo's own code. That
            // depends on the thread, not the code: the tool must not carry
            // these disabled locations into another session.
            return self.disabled_result(py, event);
        }
        // A Kolo worker can run code the user's threads run too (callbacks,
        // exception hooks), and DISABLE switches a code location off for
        // every thread. Only disable what is off for every thread anyway.
        let disable = match source {
            CallbackSource::Code(_) | CallbackSource::Unwind(..) => false,
            // Statically excluded code first (no lock, no Python), so Kolo's
            // own code stops firing instruction events on its first hit.
            CallbackSource::Instruction(code, offset) => {
                self.statically_excluded(code)
                    || self
                        .instruction_cache
                        .lock_py_attached(py)
                        .ok()
                        .and_then(|cache| cache.get(&(code.as_ptr() as usize)).cloned())
                        .is_some_and(|metadata| {
                            !metadata.instructions.contains_key(&offset)
                                || metadata.include_frame == Some(false)
                        })
            }
            CallbackSource::Other => false,
        };
        if disable {
            self.static_disable(py, event)
        } else {
            py.None()
        }
    }

    /// DISABLE for a decision that depends only on the code object (and this
    /// monitor's filters), which the idle filter makes too, so it doesn't
    /// stop the tool staying armed between sessions.
    fn static_disable(&self, py: Python, event: Event) -> Py<PyAny> {
        match event {
            Event::Call | Event::Return | Event::Resume | Event::Yield => {
                self.disable.clone_ref(py)
            }
            Event::Unwind | Event::Throw => py.None(),
        }
    }

    /// Drop the assignments waiting on this thread unrecorded: with too
    /// little stack to serialize their values, and a store left waiting
    /// would be recorded after the values-free exit about to be.
    #[cold]
    #[inline(never)]
    fn drop_waiting_assignments(&self, waiting: u8) {
        if waiting & thread_hooks::PENDING_ASSIGNMENT != 0 {
            self.instruction_data.get_or_default().replace(None);
            thread_hooks::set_assignment(
                &self.assignment_owner,
                thread_hooks::PENDING_ASSIGNMENT,
                false,
            );
        }
        if waiting & thread_hooks::DEFERRED_STORE != 0 {
            self.deferred_stores.get_or_default().borrow_mut().clear();
            thread_hooks::set_assignment(
                &self.assignment_owner,
                thread_hooks::DEFERRED_STORE,
                false,
            );
        }
    }

    fn begin_callback(
        &self,
        py: Python,
        event: Event,
        waiting: u8,
    ) -> PyResult<Option<Py<PyAny>>> {
        self.reset_recycled_thread_state();
        if waiting == 0 {
            return Ok(None);
        }
        if utils::values_omitted() {
            self.drop_waiting_assignments(waiting);
            return Ok(None);
        }
        if let Err(err) = self.process_assignment(py) {
            if utils::reaches_program(py, &err) {
                return Err(err);
            }
            self.log_error(py, err);
            if self.writer_circuit_is_open() {
                self.disable_events_after_writer_circuit(py);
                return Ok(Some(self.disabled_result(py, event)));
            }
        }
        Ok(None)
    }

    /// DISABLE for a decision that depends on more than the code object.
    ///
    /// sys.monitoring keeps a location disabled until `restart_events`, so
    /// record that this session left such a location behind: the tool must not
    /// carry its disabled locations into another session.
    fn context_dependent_disable(&self, py: Python, event: Event) -> Option<Py<PyAny>> {
        match event {
            Event::Call | Event::Return | Event::Resume | Event::Yield => {
                self.context_disabled.store(true, Ordering::Release);
                Some(self.disable.clone_ref(py))
            }
            Event::Unwind | Event::Throw => None,
        }
    }

    /// `sys.monitoring.DISABLE` is only a valid return for some events.
    fn disabled_result(&self, py: Python, event: Event) -> Py<PyAny> {
        self.context_dependent_disable(py, event)
            .unwrap_or_else(|| py.None())
    }

    fn writer_circuit_is_open(&self) -> bool {
        #[cfg(test)]
        if self.writer_circuit_override.load(Ordering::Acquire) {
            return true;
        }
        super::trace_container::writer_circuit_open()
    }
}

#[pymethods]
impl KoloMonitor {
    #[getter]
    fn trace_id(&self, py: Python) -> PyResult<String> {
        // A caught callback panic may have poisoned this lock; the id itself
        // is still a valid string.
        Ok(self
            .trace_id
            .lock_py_attached(py)
            .unwrap_or_else(|poisoned| poisoned.into_inner())
            .clone())
    }

    #[getter]
    fn root_trace_id(&self, py: Python) -> PyResult<String> {
        // A caught callback panic may have poisoned this lock; the id itself
        // is still a valid string.
        Ok(self
            .root_trace_id
            .lock_py_attached(py)
            .unwrap_or_else(|poisoned| poisoned.into_inner())
            .clone())
    }

    /// Whether a callback panicked and tracing stopped without a trace.
    #[getter]
    fn panicked(&self) -> bool {
        self.panicked.load(Ordering::Relaxed)
    }

    #[getter]
    fn active(&self) -> bool {
        self.active.load(Ordering::Acquire)
    }

    #[getter]
    fn writer_circuit_open(&self) -> bool {
        self.writer_circuit_is_open()
    }

    // Explicit setter method. We intentionally do NOT expose this as a
    // Python attribute setter (via `#[setter]`) because PyO3-generated
    // attribute setters require an exclusive borrow on the pyclass's PyCell,
    // which conflicts with shared borrows held by other threads still
    // running Python-level monitoring callbacks (e.g. a background save
    // thread). Taking `&self` avoids the exclusive-borrow requirement.
    fn set_active(&self, value: bool) {
        if value {
            // A monitor whose last session ended in idle mode but was then
            // torn down records again when it is activated anew.
            self.idle_mode.store(false, Ordering::Relaxed);
        }
        if value {
            // See `end_session`.
            self.assignment_owner.set_live(true);
        }
        self.session_epoch.fetch_add(1, Ordering::Relaxed);
        self.active.store(value, Ordering::Release);
        if !value {
            // The session is over: free the memory of cached reprs.
            self.value_interning.release_repr_reuse();
        }
    }

    // See `set_active` for rationale. Uses a Mutex to store the f64.
    fn set_timestamp(&self, py: Python, value: f64) {
        *self
            .timestamp
            .lock_py_attached(py)
            .expect("timestamp mutex poisoned") = value;
        let trace_id = self
            .trace_id
            .lock_py_attached(py)
            .expect("trace id mutex poisoned")
            .clone();
        let replacement = TraceCapture::for_trace(&self.db_path, &trace_id, value);
        let frames = self
            .frames_by_thread
            .lock_py_attached(py)
            .expect("frames registry mutex poisoned");
        if frames.is_empty() {
            *self
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex poisoned") = replacement;
        }
    }

    /// End the session, keeping Kolo's tool armed with idle callbacks.
    ///
    /// Returns false when that would not be sound; the caller then tears the
    /// session down as before. Like `set_events(tool, 0)` there, the switch
    /// to idle mode is the single step at which the session ends.
    fn end_session(slf: &Bound<'_, Self>, tool_id: u8) -> PyResult<bool> {
        let py = slf.py();
        let idle = {
            let monitor = slf.borrow();
            // Without the GIL a callback can be on its way into session mode
            // after the switch, and line events and trace points disable
            // locations for reasons the idle filter cannot see.
            // After a panic Kolo's events are off and stay off.
            if cfg!(Py_GIL_DISABLED)
                || monitor.line_events
                || !monitor.trace_point_return_targets.is_empty()
                || monitor.panicked.load(Ordering::Relaxed)
            {
                return Ok(false);
            }
            monitor.idle_mode.store(true, Ordering::Release);
            // The session is over, so its waiting assignments will never be
            // recorded: let other monitors' events drop them. A later session
            // starts afresh (`begin_session` / `set_active`).
            monitor.assignment_owner.set_live(false);
            // A session callback still running (it released the GIL) could
            // yet disable a location for a context-dependent reason.
            if monitor.callbacks_in_flight.load(Ordering::Acquire) != 0
                || monitor.context_disabled.load(Ordering::Acquire)
                || monitor.writer_circuit_is_open()
            {
                return Ok(false);
            }
            Bound::new(py, IdleMonitor::new(monitor.idle.clone()))?
        };
        // Both sides are idle, so the order of the swaps does not matter.
        // The idle monitor shares this monitor's filter, which can be dropped.
        // If an audit hook refuses a registration, the caller's teardown
        // releases the tool as before.
        if register_callbacks(idle.as_any(), tool_id).is_err() {
            return Ok(false);
        }
        set_idle_monitor(idle.unbind());
        Ok(true)
    }

    /// Start the session on the tool Kolo kept armed. Restarts events unless
    /// every location disabled between sessions is one this monitor would
    /// disable too.
    fn begin_session(slf: &Bound<'_, Self>, tool_id: u8) -> PyResult<()> {
        let py = slf.py();
        let idle = take_idle_monitor().ok_or_else(|| {
            pyo3::exceptions::PyRuntimeError::new_err("Kolo's monitoring tool is not idle")
        })?;
        slf.borrow().idle_mode.store(true, Ordering::Release);
        let started = (|| {
            register_callbacks(slf.as_any(), tool_id)?;
            let monitor = slf.borrow();
            let previous = idle.get().filter();
            // Read both flags: either side may have disabled a recordable
            // location.
            let previous_dirty = previous.take_dirty();
            let own_dirty = monitor.idle.take_dirty();
            // No Python code runs from here until the session starts, so no
            // other thread can disable anything in between.
            if previous_dirty || own_dirty || !monitor.idle.same_filters(previous) {
                restart_events(py)?;
            }
            monitor.assignment_owner.set_live(true);
            monitor.idle_mode.store(false, Ordering::Release);
            Ok(())
        })();
        if started.is_err() {
            // The tool is no longer idle and this session never started.
            release_tool(py, tool_id);
        }
        started
    }

    /// Whether at least one ``trace_points.on_return`` target is
    /// configured. Used by ``activate_monitoring`` to decide whether to
    /// spawn the daemon save worker — there's no point spinning the
    /// worker if no trace point can ever fire.
    #[getter]
    fn has_trace_points(&self) -> bool {
        !self.trace_point_return_targets.is_empty()
    }

    /// Number of strongly-held code objects in the session metadata cache.
    /// Useful for validating that repeated events hit the same cache entry.
    #[getter]
    fn code_metadata_cache_size(&self, py: Python) -> usize {
        self.code_metadata_cache
            .lock_py_attached(py)
            .expect("code metadata cache mutex poisoned")
            .entries
            .len()
    }

    /// Number of entries that need full frame metadata rather than only an
    /// excluded-code identity marker.
    #[getter]
    fn full_code_metadata_cache_size(&self, py: Python) -> usize {
        self.code_metadata_cache
            .lock_py_attached(py)
            .expect("code metadata cache mutex poisoned")
            .entries
            .values()
            .filter(|entry| matches!(entry, CachedCodeEventMetadata::Full(_)))
            .count()
    }

    /// Paths for code objects whose values needed msgpack's default hook,
    /// which used to route their frames through the Python serializer. This
    /// scans cached metadata only when requested; the event path records it.
    #[getter]
    fn _python_serializer_code_paths(&self, py: Python) -> Vec<String> {
        self.code_metadata_cache
            .lock_py_attached(py)
            .expect("code metadata cache mutex poisoned")
            .entries
            .values()
            .filter_map(|entry| match entry {
                CachedCodeEventMetadata::Full(metadata)
                    if !metadata.native_msgpack_eligible.load(Ordering::Acquire) =>
                {
                    Some(metadata.filename.clone())
                }
                _ => None,
            })
            .collect()
    }

    fn save(&self, py: Python) -> Result<(), PyErr> {
        // After a caught callback panic the capture may be inconsistent and
        // its locks poisoned. The panic was already reported; drop the trace.
        if self.panicked.load(Ordering::Relaxed) {
            return Ok(());
        }
        let publish_order = self.publish_order.for_this_process();
        let _publish_order = publish_order.lock_py_attached(py).expect("mutex");
        let (
            mut frames_by_thread,
            threads,
            trace_id,
            root_trace_id,
            timestamp,
            capture,
            value_table,
        ) = self.take_trace_inputs(py)?;
        let trace_name = self.trace_name_for_full_capture(py, &frames_by_thread);
        // Resolve Python-derived metadata before entering the best-effort
        // persistence boundary. Programming/environment errors must still
        // propagate; only file-system publication errors are logged.
        let thread_tokens = self.snapshot_thread_tokens(&frames_by_thread, &threads)?;
        let prepared = utils::prepare_v3_trace_from_parts(
            py,
            &threads,
            &thread_tokens,
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            timestamp,
            &self.config,
            true,
            Some(&root_trace_id),
        )?;
        #[cfg(target_arch = "wasm32")]
        let result: PyResult<()> = (|| {
            let data = super::trace_container::build_container_bytes(
                &trace_id,
                timestamp,
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
            utils::save_v3_container_bytes(
                py,
                &trace_id,
                &data,
                &self.db_path,
                self.sqlite_busy_timeout,
                true,
            )
        })();
        #[cfg(not(target_arch = "wasm32"))]
        let result: PyResult<()> = if capture.is_in_memory() {
            (|| {
                let data = super::trace_container::build_container_bytes(
                    &trace_id,
                    timestamp,
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
                    self.sqlite_busy_timeout,
                    true,
                )
            })()
        } else {
            (|| {
                // Sealing the last arenas, draining the writer, fsync, rename,
                // and the directory sync touch no Python objects. Detach so
                // the application's other threads keep running while this
                // save thread blocks on storage.
                py.detach(|| -> std::io::Result<()> {
                    let layouts = frames_by_thread
                        .values_mut()
                        .map(|frames| frames.layout())
                        .collect::<Result<Vec<_>, _>>()?;
                    capture.finish(prepared.thread_meta, prepared.metadata, layouts)
                })
                .map_err(pyo3::exceptions::PyOSError::new_err)?;
                utils::save_trace_metadata(
                    py,
                    &trace_id,
                    &self.db_path,
                    self.sqlite_busy_timeout,
                    true,
                )
            })()
        };
        match result {
            Err(error) if error.is_instance_of::<pyo3::exceptions::PyOSError>(py) => {
                let message = format!("Failed to save trace {trace_id} to file: {error}");
                utils::log_warning(py, PyTuple::new(py, [message])?, None);
                Ok(())
            }
            result => result,
        }
    }

    fn build_trace(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        if self.panicked.load(Ordering::Relaxed) {
            return Err(stopped_after_panic_error());
        }
        self.build_trace_inner(py)
    }

    fn monitor_pystart(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(self.idle.idle_event(code));
        }
        let _in_flight = CallbackInFlight::enter(&self.callbacks_in_flight);
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Call,
            utils::StackEvent::Enter(code.as_ptr() as usize),
            CallbackSource::Code(code),
            |local| self.monitor(code, utils::Arg::None, Event::Call, local),
        )
    }

    fn monitor_pyreturn(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        retval: &Bound<'_, PyAny>,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(self.idle.idle_event(code));
        }
        let _in_flight = CallbackInFlight::enter(&self.callbacks_in_flight);
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Return,
            utils::StackEvent::Exit(code.as_ptr() as usize),
            CallbackSource::Code(code),
            |local| self.monitor(code, utils::Arg::Argument(retval), Event::Return, local),
        )
    }

    fn monitor_pyunwind(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
        exception: &Bound<'_, PyAny>,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(code.py().None());
        }
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Unwind,
            utils::StackEvent::Exit(code.as_ptr() as usize),
            CallbackSource::Unwind(code, instruction_offset),
            |local| self.monitor(code, utils::Arg::Exception(exception), Event::Unwind, local),
        )
    }

    fn monitor_pyresume(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(self.idle.idle_event(code));
        }
        let _in_flight = CallbackInFlight::enter(&self.callbacks_in_flight);
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Resume,
            utils::StackEvent::Enter(code.as_ptr() as usize),
            CallbackSource::Code(code),
            |local| self.monitor(code, utils::Arg::None, Event::Resume, local),
        )
    }

    fn monitor_pyyield(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        retval: &Bound<'_, PyAny>,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(self.idle.idle_event(code));
        }
        let _in_flight = CallbackInFlight::enter(&self.callbacks_in_flight);
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Yield,
            utils::StackEvent::Exit(code.as_ptr() as usize),
            CallbackSource::Code(code),
            |local| self.monitor(code, utils::Arg::Argument(retval), Event::Yield, local),
        )
    }

    fn monitor_pythrow(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        exception: &Bound<'_, PyAny>,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(code.py().None());
        }
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Throw,
            utils::StackEvent::Enter(code.as_ptr() as usize),
            CallbackSource::Code(code),
            |local| self.monitor(code, utils::Arg::Exception(exception), Event::Throw, local),
        )
    }

    fn monitor_instruction(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
    ) -> PyResult<Py<PyAny>> {
        if self.idle_mode.load(Ordering::Relaxed) {
            return Ok(code.py().None());
        }
        let _in_flight = CallbackInFlight::enter(&self.callbacks_in_flight);
        let py = code.py();
        self.guarded_callback(
            py,
            Event::Call,
            utils::StackEvent::Within,
            CallbackSource::Instruction(code, instruction_offset),
            |_| self._monitor_instruction(code, instruction_offset),
        )
    }
}

/// This event's frame, for `utils::check_stack` near the end of the stack,
/// where it tells activations apart: recursion repeats the same code, and an
/// exit CPython never reported (it can't call Kolo right at the limit) would
/// otherwise let the remaining exits pair with the wrong activations.
#[cfg(Py_3_12)]
fn near_end_frame_id(code: &Bound<'_, PyCode>) -> Option<usize> {
    // Safety: called with the GIL. Returns a borrowed frame, or NULL (with no
    // error set) when there is none or it can't be created.
    let frame = unsafe { pyo3::ffi::PyEval_GetFrame() };
    if frame.is_null() {
        return None;
    }
    // The current frame is the event's, except for an unwind from a frame
    // that failed before it started (CPython skips such incomplete frames):
    // then this is the caller's.
    // Safety: `frame` is live; this returns a new reference.
    let frame_code = unsafe { pyo3::ffi::PyFrame_GetCode(frame) };
    let is_event_frame = frame_code.cast() == code.as_ptr();
    // Safety: releases the reference taken above.
    unsafe { pyo3::ffi::Py_DECREF(frame_code.cast()) };
    is_event_frame.then_some(frame as usize)
}

#[cfg(not(Py_3_12))]
fn near_end_frame_id(_code: &Bound<'_, PyCode>) -> Option<usize> {
    None
}

/// `RESUME` and `RETURN_GENERATOR`'s opcodes, which differ per version.
/// Looked up when a monitor is created, so not first near the stack end.
fn prefix_end_opcodes(py: Python<'_>) -> Option<(u8, u8)> {
    static OPCODES: pyo3::sync::PyOnceLock<(u8, u8)> = pyo3::sync::PyOnceLock::new();
    OPCODES
        .get_or_try_init(py, || -> PyResult<(u8, u8)> {
            let opmap =
                PyModule::import(py, intern!(py, "opcode"))?.getattr(intern!(py, "opmap"))?;
            Ok((
                opmap.get_item(intern!(py, "RESUME"))?.extract::<u8>()?,
                opmap.get_item(intern!(py, "RETURN_GENERATOR"))?.extract::<u8>()?,
            ))
        })
        .ok()
        .copied()
}

/// `RESUME`'s oparg at the start of a generator expression (3.15+), which
/// runs before the frame starts: CPython's first traceable instruction is
/// past it. Never a function-start `RESUME`'s oparg before 3.15.
const RESUME_AT_GEN_EXPR_START: u8 = 4;

/// Whether `offset` (in bytes) is in the prefix that runs before CPython
/// reports the frame's start (`MAKE_CELL`, `COPY_FREE_VARS`, a 3.15
/// generator expression's first iterator): before the first traceable
/// `RESUME`, as CPython judges a frame incomplete. A generator's frame is
/// never incomplete, so `RETURN_GENERATOR` ends the prefix too (a throw into
/// a fresh generator unwinds at it). An unwind from the prefix is from a
/// frame Kolo never saw start, which `PyEval_GetFrame` skips: in direct
/// recursion `near_end_frame_id` would take its caller for it. Only called
/// near the end of the stack. False when it can't tell.
fn before_first_resume(code: &Bound<'_, PyCode>, offset: usize) -> bool {
    let py = code.py();
    let Some((resume, return_generator)) = prefix_end_opcodes(py) else {
        return false;
    };
    // `co_code` is the unspecialized bytecode, the prefix included.
    let Ok(bytecode) = code.getattr(intern!(py, "co_code")) else {
        return false;
    };
    let Ok(bytecode) = bytecode.cast_into::<PyBytes>() else {
        return false;
    };
    let units = bytecode.as_bytes().chunks_exact(2);
    offset / 2 < units.len()
        && !units.take(offset / 2 + 1).any(|unit| {
            unit[0] == return_generator
                || (unit[0] == resume && unit[1] != RESUME_AT_GEN_EXPR_START)
        })
}

/// Held by every test that patches, exercises or depends on process-wide
/// `sys.monitoring` state (tool ids, event masks, `sys.settrace`), including
/// any `KoloMonitor::new`, which probes a spare tool id for the line-table
/// layout check. Take it before attaching to the interpreter.
#[cfg(test)]
pub(crate) fn monitoring_test_guard() -> std::sync::MutexGuard<'static, ()> {
    static MONITORING_TEST_LOCK: Mutex<()> = Mutex::new(());
    MONITORING_TEST_LOCK
        .lock()
        .unwrap_or_else(std::sync::PoisonError::into_inner)
}

#[cfg(test)]
mod tests {
    use super::monitoring_test_guard;
    use super::subtree_flush::extract_co_name;
    use super::thread_hooks;
    use super::{
        discard_frame_buffers, store_targets, CachedCodeEventMetadata, CodeEventMetadata,
        CodeEventMetadataLookup, CodeMetadataCache, FrameSequence, FrameStore, InstructionData,
        KoloMonitor, LineFrame, Opname, RestoreGuard, SerializedFrame, TraceCapture,
    };
    use crate::_kolo::plugins::load_plugin_data_for_test;
    use hashbrown::HashMap;
    use pyo3::exceptions::PyRuntimeError;
    use pyo3::sync::MutexExt;
    use pyo3::types::{PyAnyMethods, PyBytes, PyCode, PyCodeInput, PyDict, PyList, PyModule};
    use pyo3::{Py, PyResult, Python};
    use rmpv::Value;
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
    use std::sync::{Arc, Mutex};

    static TEST_CAPTURE_ID: AtomicUsize = AtomicUsize::new(0);

    fn test_capture_path(name: &str) -> PathBuf {
        std::env::temp_dir().join(format!(
            "kolo-{name}-{}-{}.kolo",
            std::process::id(),
            TEST_CAPTURE_ID.fetch_add(1, Ordering::Relaxed)
        ))
    }

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

    #[cfg(Py_3_12)]
    #[test]
    fn start_test_preserves_in_memory_capture_mode() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("start-test-in-memory")
                    .display()
                    .to_string(),
                &config,
                "test".to_string(),
                true,
                None,
            )
            .expect("test monitor");
            {
                let capture = monitor
                    .trace_capture
                    .lock_py_attached(py)
                    .expect("trace capture mutex");
                capture.keep_in_memory();
            }

            monitor.start_test(py).expect("start test");

            assert!(
                monitor
                    .trace_capture
                    .lock_py_attached(py)
                    .expect("trace capture mutex")
                    .is_in_memory(),
                "a test boundary must not re-enable inherited writer state"
            );
        });
    }

    #[test]
    fn store_targets_expand_superinstructions_in_store_order() {
        use pyo3::{Bound, IntoPyObject, PyAny};

        Python::initialize();

        Python::attach(|py| {
            let targets = |opname: &str, argval: Bound<'_, PyAny>| {
                store_targets(opname, &argval).map(|(opname, variables)| (opname as u8, variables))
            };
            let pair =
                |first: &str, second: &str| (first, second).into_pyobject(py).unwrap().into_any();
            let name = |name: &str| name.into_pyobject(py).unwrap().into_any();

            assert_eq!(
                targets("STORE_FAST_STORE_FAST", pair("a", "b")),
                Some((Opname::StoreFast as u8, vec!["a".into(), "b".into()]))
            );
            assert_eq!(
                targets("STORE_FAST_LOAD_FAST", pair("x", "y")),
                Some((Opname::StoreFast as u8, vec!["x".into()]))
            );
            assert_eq!(
                targets("STORE_FAST_STORE_FAST", pair("@py_assert0", "b")),
                Some((
                    Opname::StoreFast as u8,
                    vec!["@py_assert0".into(), "b".into()]
                ))
            );
            assert_eq!(
                targets("STORE_DEREF", name("c")),
                Some((Opname::StoreDeref as u8, vec!["c".into()]))
            );
            assert_eq!(
                targets("STORE_GLOBAL", name("g")),
                Some((Opname::StoreGlobal as u8, vec!["g".into()]))
            );
            assert_eq!(
                targets("STORE_FAST_LOAD_FAST", pair("@py_assert0", "x")),
                None
            );
            assert_eq!(targets("STORE_FAST_STORE_FAST", name("a")), None);
            assert_eq!(targets("STORE_FAST", py.None().into_bound(py)), None);
            assert_eq!(targets("STORE_NAME", name("module_level")), None);
        });
    }

    #[cfg(Py_3_12)]
    #[test]
    fn only_the_prefix_before_the_first_resume_is_before_the_frame_starts() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            // Every unwind CPython reports, with whether it reported the
            // frame's entry (start, throw or resume) first. Tool id 5 is
            // unassigned.
            let fixture = PyModule::from_code(
                py,
                cr#"
import dis
import sys

def outer():
    cell = 1
    def inner():
        return cell
    return inner

def fresh():
    cell = 1
    yield cell

def raises():
    cell = 1
    raise ValueError(cell)

mon = sys.monitoring
E = mon.events
names = {"fresh", "raises", "<genexpr>"}
entered = []
unwinds = []

def entry(code, offset, *args):
    if code.co_name in names:
        entered.append(code)

def unwind(code, offset, exception):
    if code.co_name in names:
        unwinds.append((code, offset, code in entered))
        entered.clear()

mon.use_tool_id(5, "kolo-first-resume-test")
try:
    for event in (E.PY_START, E.PY_THROW, E.PY_RESUME):
        mon.register_callback(5, event, entry)
    mon.register_callback(5, E.PY_UNWIND, unwind)
    mon.set_events(5, E.PY_START | E.PY_THROW | E.PY_RESUME | E.PY_UNWIND)
    for run in (
        lambda: fresh().throw(ValueError),
        raises,
        # 3.15+: fails before the generator expression's frame starts.
        lambda: (x for x in 5),
    ):
        try:
            run()
        except (ValueError, TypeError):
            pass
finally:
    mon.set_events(5, 0)
    mon.free_tool_id(5)

prefix = [
    (f.__code__, [(i.opname, i.offset) for i in dis.get_instructions(f)])
    for f in (outer, outer())
]
"#,
                c"first_resume_fixture.py",
                c"first_resume_fixture",
            )
            .expect("fixture runs");

            let unwinds: Vec<(pyo3::Bound<'_, PyCode>, usize, bool)> = fixture
                .getattr("unwinds")
                .expect("unwinds")
                .extract()
                .expect("code, offset and entered");
            // A fresh generator's throw unwinds at RETURN_GENERATOR, before
            // the first RESUME, after a PY_THROW Kolo recorded.
            assert!(unwinds.len() >= 2, "{unwinds:?}");
            for (code, offset, entered) in &unwinds {
                assert_eq!(
                    super::before_first_resume(code, *offset),
                    !entered,
                    "{code:?} at {offset}"
                );
            }

            let prefix: Vec<(pyo3::Bound<'_, PyCode>, Vec<(String, usize)>)> = fixture
                .getattr("prefix")
                .expect("prefix")
                .extract()
                .expect("code and instructions");
            for (code, instructions) in prefix {
                let resume = instructions
                    .iter()
                    .position(|(opname, _)| opname == "RESUME")
                    .expect("a RESUME");
                // `outer` starts with MAKE_CELL, `inner` with COPY_FREE_VARS.
                assert!(resume > 0, "{instructions:?}");
                for (index, (opname, offset)) in instructions.iter().enumerate() {
                    assert_eq!(
                        super::before_first_resume(&code, *offset),
                        index < resume,
                        "{opname} at {offset}"
                    );
                }
                assert!(!super::before_first_resume(&code, usize::MAX - 1));
            }
        });
    }

    #[cfg(Py_3_12)]
    #[test]
    fn prefix_unwind_near_the_stack_end_leaves_the_callers_entry() {
        use crate::_kolo::utils::{
            check_stack, remembered_entries, with_stack_below, StackEvent, NEAR_STACK_END_BYTES,
            STACK_RESERVE_BYTES,
        };
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        std::thread::Builder::new()
            .stack_size(4 << 20)
            .spawn(|| {
                Python::attach(|py| {
                    let fixture = PyModule::from_code(
                        py,
                        c"def descend(n):\n    cell = n\n    def inner():\n        return cell\n    return inner\n",
                        c"prefix_unwind.py",
                        c"prefix_unwind",
                    )
                    .expect("fixture compiles");
                    let code = fixture
                        .getattr("descend")
                        .and_then(|descend| descend.getattr("__code__"))
                        .expect("code")
                        .cast_into::<PyCode>()
                        .expect("a code object");
                    let monitor = KoloMonitor::new(
                        test_capture_path("prefix-unwind").display().to_string(),
                        &PyDict::new(py),
                        "test".to_string(),
                        false,
                        None,
                    )
                    .expect("test monitor");
                    with_stack_below(NEAR_STACK_END_BYTES, &mut || {
                        // `descend` runs, its entry recorded and remembered
                        // (no Python frame here: by its code).
                        let (decision, _) = check_stack(StackEvent::Enter(code.as_ptr() as usize));
                        assert_eq!(decision, crate::_kolo::utils::StackDecision::Record);
                        assert_eq!(remembered_entries(), 1);
                        with_stack_below(STACK_RESERVE_BYTES, &mut || {
                            // It calls itself, and the call fails in
                            // MAKE_CELL: an unwind at offset 0 with no start.
                            monitor
                                .monitor_pyunwind(&code, 0, py.None().bind(py))
                                .expect("callback succeeds");
                            // The caller's entry is still waiting for its exit.
                            assert_eq!(remembered_entries(), 1);
                        });
                    });
                });
            })
            .expect("spawn test thread")
            .join()
            .expect("test thread");
    }

    #[test]
    fn assignment_value_skips_variables_unbound_before_the_next_event() {
        Python::initialize();

        Python::attach(|py| {
            let fixture = PyModule::from_code(
                py,
                c"import sys\n\ndef target():\n    global deleted_global\n    bound = 1\n    deleted = 2\n    del deleted\n    deleted_global = 3\n    del deleted_global\n    return sys._getframe()\n\nframe = target()\n",
                c"assignment_value_fixture.py",
                c"assignment_value_fixture",
            )
            .expect("fixture compiles");
            let frame = fixture.getattr("frame").expect("frame exists");

            let bound = Opname::StoreFast
                .assignment_value("bound", &frame)
                .expect("bound local reads")
                .expect("bound local has a value");
            assert_eq!(bound.extract::<i64>().expect("int"), 1);
            assert!(Opname::StoreFast
                .assignment_value("deleted", &frame)
                .expect("unbound local is not an error")
                .is_none());
            assert!(Opname::StoreGlobal
                .assignment_value("deleted_global", &frame)
                .expect("unbound global is not an error")
                .is_none());
            assert!(Opname::StoreFast
                .assignment_value("bound", &py.None().into_bound(py))
                .is_err());
            assert!(Opname::StoreGlobal
                .assignment_value("bound", &py.None().into_bound(py))
                .is_err());
            let not_a_frame = py
                .eval(
                    c"__import__('types').SimpleNamespace(f_globals=1)",
                    None,
                    None,
                )
                .expect("namespace");
            assert!(Opname::StoreGlobal
                .assignment_value("bound", &not_a_frame)
                .is_err());
        });
    }

    #[test]
    fn double_store_progress_check_reports_unreadable_frames() {
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("store-progress").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.reset_recycled_thread_state();
            let instruction = |frame: &str| InstructionData {
                variables: Arc::from(["first".to_string(), "second".to_string()]),
                offset: 0,
                opname: Opname::StoreFast,
                line_frame: py
                    .eval(&std::ffi::CString::new(frame).unwrap(), None, None)
                    .expect("fake frame")
                    .unbind(),
                line_frame_data: LineFrame::new(
                    "store.py".to_string(),
                    "store".to_string(),
                    "store".to_string(),
                    None,
                    0.0,
                ),
            };
            let no_lasti = "__import__('types').SimpleNamespace()";
            let bad_lasti = "__import__('types').SimpleNamespace(f_lasti='x')";

            assert!(monitor
                .store_in_progress(py, &instruction(no_lasti))
                .is_err());
            assert!(monitor
                .store_in_progress(py, &instruction(bad_lasti))
                .is_err());

            monitor
                .instruction_data
                .get_or_default()
                .replace(Some(instruction(no_lasti)));
            assert!(monitor.process_assignment(py).is_err());

            monitor
                .deferred_stores
                .get_or_default()
                .borrow_mut()
                .push(instruction(no_lasti));
            thread_hooks::set_assignment(
                &monitor.assignment_owner,
                thread_hooks::DEFERRED_STORE,
                true,
            );
            assert!(monitor.process_assignment(py).is_err());
            monitor
                .deferred_stores
                .get_or_default()
                .borrow_mut()
                .clear();
        });
    }

    fn inject_assignment_error(monitor: &KoloMonitor, py: Python) {
        monitor
            .instruction_data
            .get_or_default()
            .replace(Some(InstructionData {
                variables: Arc::from(["missing".to_string()]),
                offset: 0,
                opname: Opname::StoreFast,
                line_frame: py.None(),
                line_frame_data: LineFrame::new(
                    "circuit.py".to_string(),
                    "callback".to_string(),
                    "callback".to_string(),
                    None,
                    0.0,
                ),
            }));
        thread_hooks::set_assignment(
            &monitor.assignment_owner,
            thread_hooks::PENDING_ASSIGNMENT,
            true,
        );
    }

    #[test]
    fn values_free_exit_drops_waiting_assignments_without_recording_them() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let monitor = KoloMonitor::new(
                test_capture_path("values-free-assignment").display().to_string(),
                &PyDict::new(py),
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.reset_recycled_thread_state();
            // A deferred second store target and a pending assignment, both
            // of which would fail to record (and stay queued) if processed.
            inject_assignment_error(&monitor, py);
            let deferred = InstructionData {
                variables: Arc::from(["missing".to_string()]),
                offset: 0,
                opname: Opname::StoreFast,
                line_frame: py.None(),
                line_frame_data: LineFrame::new(
                    "circuit.py".to_string(),
                    "callback".to_string(),
                    "callback".to_string(),
                    None,
                    0.0,
                ),
            };
            monitor
                .deferred_stores
                .get_or_default()
                .borrow_mut()
                .push(deferred);
            thread_hooks::set_assignment(
                &monitor.assignment_owner,
                thread_hooks::DEFERRED_STORE,
                true,
            );
            let waiting = thread_hooks::assignments_for(&monitor.assignment_owner);
            assert_eq!(
                waiting,
                thread_hooks::PENDING_ASSIGNMENT | thread_hooks::DEFERRED_STORE
            );

            // An exit recorded without its values has no stack to serialize
            // them either, and must not leave them to be recorded after it.
            let omitting = crate::_kolo::utils::OmittingValues::start();
            let begun = monitor
                .begin_callback(py, super::Event::Return, waiting)
                .expect("nothing raised");
            omitting.restore();
            assert!(begun.is_none());
            assert_eq!(thread_hooks::assignments_for(&monitor.assignment_owner), 0);
            assert!(monitor
                .instruction_data
                .get()
                .is_none_or(|data| data.borrow().is_none()));
            assert!(monitor.deferred_stores.get_or_default().borrow().is_empty());
        });
    }

    #[test]
    fn one_monitor_never_clears_another_monitors_waiting_assignment() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let monitor = |name: &str| {
                KoloMonitor::new(
                    test_capture_path(name).display().to_string(),
                    &PyDict::new(py),
                    "test".to_string(),
                    false,
                    None,
                )
                .expect("test monitor")
            };
            let first = monitor("assignment-owner-first");
            let second = monitor("assignment-owner-second");
            let code = PyCode::compile(py, c"pass", c"<frozen owner>", PyCodeInput::File)
                .expect("test code");
            let unwind = |monitor: &KoloMonitor| {
                monitor
                    .monitor_pyunwind(&code, 0, py.None().bind(py))
                    .expect("callback succeeds");
            };
            let waiting = |monitor: &KoloMonitor| {
                thread_hooks::assignments_for(&monitor.assignment_owner)
            };
            let holds_data = |monitor: &KoloMonitor| {
                monitor
                    .instruction_data
                    .get()
                    .is_some_and(|data| data.borrow().is_some())
            };
            first.reset_recycled_thread_state();
            second.reset_recycled_thread_state();
            inject_assignment_error(&first, py);
            inject_assignment_error(&second, py);

            // The second monitor's event processes and clears only its own
            // waiting assignment (the injected read error is just logged).
            unwind(&second);
            assert_eq!(waiting(&second), 0);
            assert!(!holds_data(&second));
            assert_eq!(waiting(&first), thread_hooks::PENDING_ASSIGNMENT);
            assert!(holds_data(&first));
            assert_eq!(
                thread_hooks::get() & thread_hooks::ASSIGNMENTS,
                thread_hooks::ASSIGNMENTS
            );
            // With nothing of its own waiting, it leaves the first's alone.
            unwind(&second);
            assert_eq!(waiting(&first), thread_hooks::PENDING_ASSIGNMENT);
            assert!(holds_data(&first));

            // The first monitor still processes its own at its next event.
            unwind(&first);
            assert_eq!(waiting(&first), 0);
            assert!(!holds_data(&first));
            assert_eq!(thread_hooks::get() & thread_hooks::ASSIGNMENTS, 0);

            // A monitor whose session ended retires its leftovers: the next
            // event of another monitor drops them, even while it's alive.
            inject_assignment_error(&first, py);
            first.assignment_owner.set_live(false);
            unwind(&second);
            assert_eq!(thread_hooks::get() & thread_hooks::ASSIGNMENTS, 0);
            assert_eq!(waiting(&first), 0);
            // Toggling `active` mid-session never retires anything.
            first.set_active(true);
            inject_assignment_error(&first, py);
            first.set_active(false);
            unwind(&second);
            first.set_active(true);
            assert_eq!(waiting(&first), thread_hooks::PENDING_ASSIGNMENT);

            // A dead monitor's leftovers are dropped by the next event.
            drop(first);
            unwind(&second);
            assert_eq!(thread_hooks::get() & thread_hooks::ASSIGNMENTS, 0);
        });
    }

    #[test]
    fn hook_state_settles_events_before_any_per_event_work() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("hook-state").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.set_active(true);
            let excluded = PyCode::compile(py, c"pass", c"<frozen hook_state>", PyCodeInput::File)
                .expect("excluded code");
            let included = PyCode::compile(py, c"pass", c"hook_state.py", PyCodeInput::File)
                .expect("included code");
            let none = py.None();
            let disable = monitor.disable.bind(py);
            let start = |code: &pyo3::Bound<'_, PyCode>| {
                monitor.monitor_pystart(code, 0).expect("callback succeeds")
            };

            // A worker that is first to run excluded code (Kolo's own
            // save/emit code) disables it for good...
            thread_hooks::set(thread_hooks::WORKER, true);
            assert!(start(&excluded).bind(py).is(disable));
            // ...but never code a traced thread might still have to record.
            assert!(start(&included).bind(py).is_none());
            thread_hooks::set(thread_hooks::WORKER, false);

            // A traced thread caches the exclusion and reuses it.
            assert!(start(&excluded).bind(py).is(disable));
            assert!(monitor.cached_excluded(&excluded));
            assert!(start(&excluded).bind(py).is(disable));
            assert!(monitor
                .monitor_pyunwind(&excluded, 0, none.bind(py))
                .expect("callback succeeds")
                .bind(py)
                .is_none());
            thread_hooks::set(thread_hooks::WORKER, true);
            assert!(start(&excluded).bind(py).is(disable));
            assert!(start(&included).bind(py).is_none());
            assert!(monitor
                .monitor_instruction(&included, 0)
                .expect("callback succeeds")
                .bind(py)
                .is_none());
            // Instruction events in excluded code are disabled on first hit.
            let excluded_lines =
                PyCode::compile(py, c"x = 1", c"<frozen hook_state_lines>", PyCodeInput::File)
                    .expect("excluded code");
            assert!(monitor
                .monitor_instruction(&excluded_lines, 0)
                .expect("callback succeeds")
                .bind(py)
                .is(disable));

            // A save section on a worker leaves its mark alone.
            {
                let _suspended = thread_hooks::Suspended::new();
                assert!(start(&included).bind(py).is_none());
            }
            assert_eq!(thread_hooks::get() & thread_hooks::WORKER, thread_hooks::WORKER);
            thread_hooks::set(thread_hooks::WORKER, false);
            // Every DISABLE so far depended on the code alone, so the tool
            // could stay armed between sessions.
            assert!(!monitor.context_disabled.load(Ordering::Relaxed));

            // A save section on a traced thread disables statically excluded
            // code without marking the session...
            {
                let _suspended = thread_hooks::Suspended::new();
                let library = PyCode::compile(
                    py,
                    c"pass",
                    c"<frozen hook_state_save>",
                    PyCodeInput::File,
                )
                .expect("excluded code");
                assert!(start(&library).bind(py).is(disable));
            }
            assert!(!monitor.context_disabled.load(Ordering::Relaxed));
            // ...and anything else it runs for the thread's sake, which does.
            {
                let _suspended = thread_hooks::Suspended::new();
                assert!(start(&included).bind(py).is(disable));
                assert!(monitor
                    .monitor_pythrow(&included, 0, none.bind(py))
                    .expect("callback succeeds")
                    .bind(py)
                    .is_none());
            }
            assert_eq!(thread_hooks::get() & thread_hooks::OFF, 0);
            // That one depended on the thread: the session must not hand
            // its disabled locations to the next one.
            assert!(monitor.context_disabled.load(Ordering::Relaxed));
        });
    }

    #[test]
    fn unretained_excluded_code_is_never_cached_per_thread() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let monitor = KoloMonitor::new(
                test_capture_path("retention").display().to_string(),
                &PyDict::new(py),
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.reset_recycled_thread_state();
            let excluded = |filename: &std::ffi::CStr| {
                PyCode::compile(py, c"value = 1", filename, PyCodeInput::File)
                    .expect("excluded code")
            };

            // Under the retention cap the shared cache keeps the code alive,
            // so its address is safe to remember on this thread.
            let retained = excluded(c"<frozen retained>");
            assert!(matches!(
                monitor.code_event_metadata(&retained),
                Ok(CodeEventMetadataLookup::Excluded)
            ));
            assert!(monitor.cached_excluded(&retained));

            // Past the cap it isn't kept alive, so once freed its address may
            // belong to included code: it must never be remembered.
            monitor
                .code_metadata_cache
                .lock()
                .unwrap()
                .excluded_entries = super::MAX_EXCLUDED_CODE_METADATA_ENTRIES;
            let unretained = excluded(c"<frozen unretained>");
            for _ in 0..2 {
                assert!(matches!(
                    monitor.code_event_metadata(&unretained),
                    Ok(CodeEventMetadataLookup::Excluded)
                ));
                assert!(!monitor.cached_excluded(&unretained));
            }
        });
    }

    #[test]
    fn a_panicking_save_section_never_leaves_the_thread_suspended() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("suspend-panic").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            let result = monitor.guarded_callback(
                py,
                super::Event::Return,
                crate::_kolo::utils::StackEvent::Exit(1),
                super::CallbackSource::Other,
                |_| {
                    let _suspended = thread_hooks::Suspended::new();
                    panic!("save failed mid-way")
                },
            );
            assert!(result.expect("a panic is not raised").bind(py).is_none());
            assert_eq!(thread_hooks::get() & thread_hooks::OFF, 0);
        });
    }

    #[test]
    fn writer_circuit_disables_every_monitoring_callback_after_an_error() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("callback-circuit").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.set_active(true);
            monitor.reset_recycled_thread_state();
            monitor
                .writer_circuit_override
                .store(true, Ordering::Release);
            assert!(monitor.writer_circuit_open());

            let code =
                PyCode::compile(py, c"pass", c"circuit.py", PyCodeInput::File).expect("test code");
            let value = py.None();

            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pystart(&code, 0)
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyreturn(&code, 0, value.bind(py))
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyunwind(&code, 0, value.bind(py))
                .expect("callback succeeds")
                .bind(py)
                .is_none());
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyresume(&code, 0)
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyyield(&code, 0, value.bind(py))
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pythrow(&code, 0, value.bind(py))
                .expect("callback succeeds")
                .bind(py)
                .is_none());
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_instruction(&code, 0)
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));

            // The generic callback error path must also attempt to turn the
            // process-wide event mask off after the circuit opens.
            monitor
                .return_or_log(py, Err(PyRuntimeError::new_err("writer circuit")))
                .expect("a logged error is not raised");
        });
    }

    #[test]
    fn callback_panic_is_caught_instead_of_raising_into_user_code() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            if PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .is_err()
            {
                return;
            }
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("callback-panic").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.set_active(true);

            // Panic while holding a lock, as a real mid-callback bug would.
            let result = monitor.guarded_callback(
                py,
                super::Event::Unwind,
                crate::_kolo::utils::StackEvent::Exit(1),
                super::CallbackSource::Other,
                |_| {
                    let _trace_id = monitor.trace_id.lock().unwrap();
                    panic!("kolo bug")
                },
            );
            assert!(result.expect("a panic is not raised").bind(py).is_none());
            assert!(monitor.panicked.load(Ordering::Relaxed));
            assert!(!pyo3::PyErr::occurred(py));

            // Later callbacks no longer run Kolo code at all.
            let result = monitor.guarded_callback(
                py,
                super::Event::Call,
                crate::_kolo::utils::StackEvent::Enter(2),
                super::CallbackSource::Other,
                |_| panic!("callback ran after a panic"),
            );
            assert!(result
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));

            // Teardown neither panics on the poisoned lock nor saves the
            // possibly inconsistent capture.
            assert!(monitor.trace_id(py).is_ok());
            assert!(monitor.save(py).is_ok());
            assert!(monitor.build_trace(py).is_err());
        });
    }

    #[cfg(Py_3_12)]
    #[test]
    fn callbacks_outliving_their_session_leave_the_tool_armed() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            let monitoring = PyModule::import(py, "sys")
                .and_then(|sys| sys.getattr("monitoring"))
                .unwrap();
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("late-callback").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            let tool_id = monitor.tool_id;
            let py_start: u32 = monitoring
                .getattr("events")
                .and_then(|events| events.getattr("PY_START"))
                .and_then(|event| event.extract())
                .unwrap();
            let events = || -> u32 {
                monitoring
                    .call_method1("get_events", (tool_id,))
                    .and_then(|events| events.extract())
                    .unwrap()
            };
            monitoring
                .call_method1("use_tool_id", (tool_id, "next-session"))
                .unwrap();
            monitoring
                .call_method1("set_events", (tool_id, py_start))
                .unwrap();

            // The session ended while these callbacks were still running.
            monitor.set_active(false);
            monitor.idle_mode.store(true, Ordering::Relaxed);
            let result = monitor.guarded_callback(
                py,
                super::Event::Unwind,
                crate::_kolo::utils::StackEvent::Exit(1),
                super::CallbackSource::Other,
                |_| panic!("kolo bug"),
            );
            let after_panic = events();
            monitor
                .writer_circuit_override
                .store(true, Ordering::Release);
            monitor.disable_events_after_writer_circuit(py);
            let after_circuit = events();
            // During its session the monitor still turns its events off.
            monitor.set_active(true);
            monitor.disable_events_after_writer_circuit(py);
            let during_session = events();
            monitoring.call_method1("set_events", (tool_id, 0)).unwrap();
            monitoring.call_method1("free_tool_id", (tool_id,)).unwrap();

            assert!(result.expect("a panic is not raised").bind(py).is_none());
            assert!(monitor.panicked.load(Ordering::Relaxed));
            assert_eq!(after_panic, py_start);
            assert_eq!(after_circuit, py_start);
            assert_eq!(during_session, 0);
        });
    }

    #[cfg(Py_3_12)]
    #[test]
    fn callbacks_outliving_their_session_never_disable_a_location() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                test_capture_path("late-disable").display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            monitor.set_active(true);
            type Outcome = Result<Option<Py<pyo3::PyAny>>, pyo3::PyErr>;
            let disable = || -> Outcome { Ok(Some(monitor.disable.clone_ref(py))) };
            let run = |callback: &dyn Fn() -> Outcome| {
                monitor.guarded_callback(
                    py,
                    super::Event::Call,
                    crate::_kolo::utils::StackEvent::Within,
                    super::CallbackSource::Other,
                    |_| callback(),
                )
                .expect("no error reaches the program")
            };

            let during_session = run(&disable);
            // The session ends, and another starts, while the callback runs.
            let after_teardown = run(&|| {
                monitor.set_active(false);
                disable()
            });
            let after_new_session = run(&|| {
                monitor.set_active(false);
                monitor.set_active(true);
                disable()
            });
            let next_callback = run(&disable);
            // Callbacks can still start during teardown.
            monitor.set_active(false);
            let during_teardown = run(&disable);

            assert!(during_session.bind(py).is(monitor.disable.bind(py)));
            assert!(after_teardown.bind(py).is_none());
            assert!(after_new_session.bind(py).is_none());
            assert!(next_callback.bind(py).is(monitor.disable.bind(py)));
            assert!(during_teardown.bind(py).is_none());
        });
    }

    #[cfg(Py_3_12)]
    #[test]
    fn excluded_plugin_candidate_with_wrong_filename_does_not_resolve_frame() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            let fixture = PyModule::from_code(
                py,
                c"calls = 0\n\nplugin_data = {\n    'co_names': ['target'],\n    'path_fragment': 'never/matches/this.py',\n    'call_type': 'plugin_call',\n    'return_type': 'plugin_return',\n}\n\ndef fake_getframe(depth):\n    global calls\n    calls += 1\n    raise AssertionError('excluded event resolved a frame')\n\ndef target():\n    pass\n",
                c"/tmp/site-packages/example/target.py",
                c"excluded_plugin_fixture",
            )
            .expect("fixture compiles");

            let config = PyDict::new(py);
            let mut monitor = KoloMonitor::new(
                test_capture_path("excluded-plugin-frame-lookup")
                    .display()
                    .to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("monitor builds");
            monitor.set_active(true);
            let plugin_data = fixture.getattr("plugin_data").expect("plugin data exists");
            let plugin_data = PyList::new(py, [plugin_data]).expect("plugin list builds");
            *monitor
                .default_include_frames
                .lock_py_attached(py)
                .expect("plugin map mutex") =
                load_plugin_data_for_test(py, &plugin_data, &config).expect("plugin data loads");
            monitor.sys_getframe_fn = fixture
                .getattr("fake_getframe")
                .expect("fake getframe exists")
                .unbind();
            let code = fixture
                .getattr("target")
                .expect("target exists")
                .getattr("__code__")
                .expect("target code exists");
            let code = code.cast::<PyCode>().expect("target has code");

            let result = monitor.monitor_pystart(code, 0);
            assert!(result
                .expect("callback succeeds")
                .bind(py)
                .is(monitor.disable.bind(py)));
            assert_eq!(
                fixture
                    .getattr("calls")
                    .unwrap()
                    .extract::<usize>()
                    .unwrap(),
                0
            );
        });
    }

    #[test]
    fn value_publication_circuit_disables_events_in_the_same_callback() {
        let _monitoring = monitoring_test_guard();
        Python::initialize();

        Python::attach(|py| {
            let sys = PyModule::import(py, "sys").expect("sys imports");
            let Ok(monitoring) = sys.getattr("monitoring") else {
                return;
            };
            let config = PyDict::new(py);
            let monitor = Py::new(
                py,
                KoloMonitor::new(
                    test_capture_path("value-publication-circuit")
                        .display()
                        .to_string(),
                    &config,
                    "test".to_string(),
                    false,
                    None,
                )
                .expect("test monitor"),
            )
            .expect("monitor pyclass");
            // A live session's callback, which still owns the tool's events.
            monitor.borrow(py).set_active(true);
            let capture = TraceCapture::start_with_open_test_circuit(
                test_capture_path("value-publication-timeout"),
                b"\x80".to_vec(),
            );
            *monitor
                .borrow(py)
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex") = capture;

            let fixture = PyModule::from_code(
                py,
                c"calls = []\ndef fake_set_events(tool_id, events):\n    calls.append((tool_id, events))\ndef invoke(value):\n    return monitor.monitor_pystart(invoke.__code__, 0)\n",
                c"writer_circuit_callback.py",
                c"writer_circuit_callback",
            )
            .expect("callback fixture compiles");
            fixture
                .setattr("monitor", monitor.clone_ref(py))
                .expect("monitor installs");
            let original_set_events = monitoring
                .getattr("set_events")
                .expect("set_events exists")
                .unbind();
            monitoring
                .setattr(
                    "set_events",
                    fixture.getattr("fake_set_events").expect("fake exists"),
                )
                .expect("set_events can be observed");

            let value = PyBytes::new(py, &vec![b'x'; 4 * 1024]);
            let invoke = fixture.getattr("invoke").expect("invoke exists");
            let result: PyResult<(bool, bool, Vec<(u8, u32)>, bool, Vec<(u8, u32)>)> = (|| {
                let first_is_none = invoke.call1((&value,))?.is_none();
                let second_is_none = invoke.call1((&value,))?.is_none();
                let calls_before_circuit = fixture.getattr("calls")?.extract::<Vec<(u8, u32)>>()?;

                // Production captures share the process-global writer runtime.
                // This test capture uses an isolated open runtime so it cannot
                // poison the test process; mirror the production global latch
                // only for the callback's disable-events check.
                monitor
                    .borrow(py)
                    .writer_circuit_override
                    .store(true, Ordering::Release);
                let third_is_none = invoke.call1((&value,))?.is_none();
                let calls_after_circuit = fixture.getattr("calls")?.extract::<Vec<(u8, u32)>>()?;
                Ok((
                    first_is_none,
                    second_is_none,
                    calls_before_circuit,
                    third_is_none,
                    calls_after_circuit,
                ))
            })(
            );
            monitoring
                .setattr("set_events", original_set_events)
                .expect("set_events restores");

            let (first, second, before, third, after) = result.expect("callbacks succeed");
            assert!(first && second && third);
            assert!(before.is_empty());
            assert_eq!(after, vec![(3, 0)]);
        });
    }

    #[cfg(Py_3_12)]
    #[test]
    fn save_detaches_from_the_interpreter_while_finishing_the_trace() {
        use std::time::Duration;

        let _monitoring = monitoring_test_guard();
        Python::initialize();
        let db_dir = std::env::temp_dir().join(format!(
            "kolo-save-detach-{}-{}",
            std::process::id(),
            TEST_CAPTURE_ID.fetch_add(1, Ordering::Relaxed)
        ));
        std::fs::create_dir_all(&db_dir).unwrap();
        let db_path = db_dir.join("db.sqlite3");

        let (monitor, stall) = Python::attach(|py| {
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                db_path.display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            let stall = monitor
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex")
                .stall_writer_for_test()
                .expect("start a stalled writer");
            (monitor, stall)
        });

        // While save() waits for the stalled writer, another thread must be
        // able to attach and run Python. If save() kept the GIL, the other
        // thread could only run after the stall is released.
        let other_thread_ran = Arc::new(AtomicBool::new(false));
        let observer = {
            let other_thread_ran = Arc::clone(&other_thread_ran);
            std::thread::spawn(move || {
                // Release the writer on every exit path so a failed assertion
                // reports instead of leaving save() parked forever.
                struct ReleaseOnDrop(super::super::trace_container::WriterStallForTest);
                impl Drop for ReleaseOnDrop {
                    fn drop(&mut self) {
                        self.0.release();
                    }
                }
                let stall = ReleaseOnDrop(stall);
                let stall = &stall.0;
                assert!(
                    stall.wait_until_entered(Duration::from_secs(10)),
                    "writer never reached the injected stall"
                );
                let deadline = std::time::Instant::now() + Duration::from_secs(10);
                while !stall.finish_started() {
                    assert!(
                        std::time::Instant::now() < deadline,
                        "save() never reached TraceCapture::finish"
                    );
                    std::thread::sleep(Duration::from_millis(1));
                }
                let (ran_tx, ran_rx) = std::sync::mpsc::channel();
                let python_thread = std::thread::spawn(move || {
                    Python::attach(|py| {
                        py.run(c"sum(range(1000))", None, None)
                            .expect("run Python on the other thread");
                    });
                    let _ = ran_tx.send(());
                });
                let ran = ran_rx.recv_timeout(Duration::from_secs(10)).is_ok();
                other_thread_ran.store(ran, Ordering::Release);
                stall.release();
                python_thread.join().expect("python thread");
            })
        };

        Python::attach(|py| {
            // Metadata persistence may fail without a migrated database; only
            // the detach during finalization matters here.
            let _ = monitor.save(py);
        });
        observer.join().expect("observer thread");
        let _ = std::fs::remove_dir_all(&db_dir);

        assert!(
            other_thread_ran.load(Ordering::Acquire),
            "another Python thread could not run while save() waited for the writer"
        );
    }

    #[cfg(all(Py_3_12, unix))]
    #[test]
    fn save_in_a_child_forked_during_a_detached_save_does_not_deadlock() {
        use std::time::{Duration, Instant};

        let _monitoring = monitoring_test_guard();
        Python::initialize();
        let db_dir = std::env::temp_dir().join(format!(
            "kolo-save-fork-{}-{}",
            std::process::id(),
            TEST_CAPTURE_ID.fetch_add(1, Ordering::Relaxed)
        ));
        std::fs::create_dir_all(&db_dir).unwrap();
        let db_path = db_dir.join("db.sqlite3");

        let (monitor, stall) = Python::attach(|py| {
            let config = PyDict::new(py);
            let monitor = KoloMonitor::new(
                db_path.display().to_string(),
                &config,
                "test".to_string(),
                false,
                None,
            )
            .expect("test monitor");
            let stall = monitor
                .trace_capture
                .lock_py_attached(py)
                .expect("trace capture mutex")
                .stall_writer_for_test()
                .expect("start a stalled writer");
            (monitor, stall)
        });

        let child_status = std::thread::scope(|scope| {
            let forker = scope.spawn(|| {
                struct ReleaseOnDrop(super::super::trace_container::WriterStallForTest);
                impl Drop for ReleaseOnDrop {
                    fn drop(&mut self) {
                        self.0.release();
                    }
                }
                let stall = ReleaseOnDrop(stall);
                let stall = &stall.0;
                assert!(
                    stall.wait_until_entered(Duration::from_secs(10)),
                    "writer never reached the injected stall"
                );
                let deadline = Instant::now() + Duration::from_secs(10);
                while !stall.finish_started() {
                    assert!(
                        Instant::now() < deadline,
                        "save() never reached TraceCapture::finish"
                    );
                    std::thread::sleep(Duration::from_millis(1));
                }
                // The parent's save now holds the monitor's save locks while
                // detached on the stalled writer. Fork from another thread.
                let child = Python::attach(|py| {
                    let pid: libc::pid_t = py
                        .import("os")
                        .and_then(|os| os.call_method0("fork"))
                        .and_then(|pid| pid.extract())
                        .expect("os.fork");
                    if pid == 0 {
                        let saved = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                            // Metadata persistence may fail without a migrated
                            // database; only reaching the end matters.
                            let _ = monitor.save(py);
                        }));
                        unsafe { libc::_exit(if saved.is_ok() { 0 } else { 2 }) };
                    }
                    pid
                });
                let mut status = 0;
                let deadline = Instant::now() + Duration::from_secs(20);
                loop {
                    let waited = unsafe { libc::waitpid(child, &mut status, libc::WNOHANG) };
                    if waited == child {
                        return Some(status);
                    }
                    if Instant::now() >= deadline {
                        unsafe {
                            libc::kill(child, libc::SIGKILL);
                            libc::waitpid(child, &mut status, 0);
                        }
                        return None;
                    }
                    std::thread::sleep(Duration::from_millis(10));
                }
            });
            Python::attach(|py| {
                let _ = monitor.save(py);
            });
            forker.join().expect("forker thread")
        });
        let _ = std::fs::remove_dir_all(&db_dir);

        assert_eq!(
            child_status,
            Some(0),
            "a save in the forked child blocked on a lock held by the parent's detached save"
        );
    }

    #[cfg(Py_3_12)]
    #[test]
    fn saving_a_child_artifact_detaches_while_waiting_for_resident_budget() {
        use std::time::{Duration, Instant};

        let _monitoring = monitoring_test_guard();
        let _budget_test = super::super::trace_container::RESIDENT_BUDGET_TEST_LOCK
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner);
        Python::initialize();
        let large = || vec![1u8; 2 * 1024 * 1024];
        let cases: [(
            &str,
            Vec<(u32, Arc<[u8]>)>,
            HashMap<String, Vec<SerializedFrame>>,
        ); 2] = [
            ("value table", vec![(1, Arc::from(large()))], HashMap::new()),
            (
                "copied frames",
                Vec::new(),
                HashMap::from([("thread".to_string(), vec![large(), large()])]),
            ),
        ];
        for (case, value_table, frames) in cases {
            let db_dir = std::env::temp_dir().join(format!(
                "kolo-child-save-detach-{}-{}",
                std::process::id(),
                TEST_CAPTURE_ID.fetch_add(1, Ordering::Relaxed)
            ));
            std::fs::create_dir_all(&db_dir).unwrap();
            let db_path = db_dir.join("db.sqlite3");

            let (monitor, stall, capture) = Python::attach(|py| {
                let config = PyDict::new(py);
                let monitor = KoloMonitor::new(
                    db_path.display().to_string(),
                    &config,
                    "test".to_string(),
                    false,
                    None,
                )
                .expect("test monitor");
                let capture = monitor
                    .trace_capture
                    .lock_py_attached(py)
                    .expect("trace capture mutex")
                    .clone();
                let stall = capture
                    .stall_writer_for_test()
                    .expect("start a stalled writer");
                (monitor, stall, capture)
            });
            struct ReleaseOnDrop(super::super::trace_container::WriterStallForTest);
            impl Drop for ReleaseOnDrop {
                fn drop(&mut self) {
                    self.0.release();
                }
            }

            let other_thread_ran = std::thread::scope(|scope| {
                // Owned by the scope closure so a failed assertion releases the
                // writer before the scope joins the saver; otherwise the saver
                // would wait out the stall timeout and poison the process-wide
                // writer runtime for later tests.
                let stall = ReleaseOnDrop(stall);
                assert!(
                    stall.0.wait_until_entered(Duration::from_secs(10)),
                    "writer never reached the injected stall"
                );
                // Fill the process-wide resident budget behind the stalled writer
                // so the child artifact has to wait for writer progress.
                capture
                    .publish_value(1, Arc::from(vec![0u8; 15 * 1024 * 1024]))
                    .expect("queue a large value behind the stall");
                let saver = scope.spawn(|| {
                    Python::attach(|py| {
                        let _ = crate::_kolo::utils::save_v3_trace_from_parts(
                            py,
                            &frames,
                            &HashMap::new(),
                            "trc_child_detach",
                            None,
                            "test",
                            "thread".to_string(),
                            0.0,
                            &monitor.config,
                            true,
                            None,
                            value_table.clone(),
                            &monitor.db_path,
                            1,
                            true,
                        );
                    });
                });
                let deadline = Instant::now() + Duration::from_secs(10);
                while super::super::trace_container::resident_budget_waiters_for_test() == 0 {
                    assert!(
                        Instant::now() < deadline,
                        "{case}: the child artifact never waited for resident budget"
                    );
                    std::thread::sleep(Duration::from_millis(1));
                }
                let (ran_tx, ran_rx) = std::sync::mpsc::channel();
                let python_thread = scope.spawn(move || {
                    Python::attach(|py| {
                        py.run(c"sum(range(1000))", None, None)
                            .expect("run Python on the other thread");
                    });
                    let _ = ran_tx.send(());
                });
                let ran = ran_rx.recv_timeout(Duration::from_secs(10)).is_ok();
                stall.0.release();
                python_thread.join().expect("python thread");
                saver.join().expect("saver thread");
                ran
            });
            let _ = std::fs::remove_dir_all(&db_dir);

            assert!(
                other_thread_ran,
                "{case}: another Python thread could not run while a child artifact waited for resident budget"
            );
        }
    }

    #[test]
    fn discard_frame_buffers_releases_retained_thread_local_storage() {
        Python::initialize();

        Python::attach(|py| {
            let capture =
                TraceCapture::start(test_capture_path("discard-frame-buffer"), b"\x80".to_vec());
            let mut store = FrameStore::new(capture.clone(), 1);
            store.append_serialized(&vec![1; 4096]).unwrap();
            let retained_buffer = Arc::new(Mutex::new(store));
            let mut frame_buffers = HashMap::new();
            frame_buffers.insert("worker".to_string(), retained_buffer.clone());

            discard_frame_buffers(py, frame_buffers);

            let frames = retained_buffer.lock().expect("frame buffer");
            assert!(frames.is_empty());
            assert_eq!(frames.total_bytes(), 0);
            assert_eq!(Arc::strong_count(&capture), 1);
        });
    }

    #[test]
    fn restore_guard_clamps_a_stale_restore_index() {
        Python::initialize();

        Python::attach(|py| {
            let capture =
                TraceCapture::start(test_capture_path("restore-frame-buffer"), b"\x80".to_vec());
            let mut store = FrameStore::new(capture, 1);
            for frame in [vec![1], vec![2], vec![3]] {
                store.append_serialized(&frame).unwrap();
            }
            let drained = store.drain(1..3).unwrap();
            let frame_buffer = Arc::new(Mutex::new(store));
            {
                let _restore_guard = RestoreGuard::new(
                    frame_buffer.clone(),
                    "worker".to_string(),
                    usize::MAX,
                    drained,
                    py,
                );
            }

            let frames = frame_buffer.lock().expect("frame buffer");
            let mut scratch = Vec::new();
            assert_eq!(frames.frame(0, &mut scratch).unwrap(), &[1]);
            assert_eq!(frames.frame(1, &mut scratch).unwrap(), &[2]);
            assert_eq!(frames.frame(2, &mut scratch).unwrap(), &[3]);
        });
    }

    #[test]
    fn code_metadata_cache_keeps_first_entry_when_metadata_computation_races() {
        Python::initialize();

        Python::attach(|py| {
            let code = PyCode::compile(py, c"pass", c"metadata_race.py", PyCodeInput::File)
                .expect("test code compiles");
            let code_id = code.as_ptr() as usize;
            let full_metadata = Arc::new(CodeEventMetadata {
                _code: code.clone().unbind(),
                filename: "metadata_race.py".to_string(),
                name: "<module>".to_string(),
                relative_path: "metadata_race.py".to_string(),
                co_qualname: "<module>".to_string(),
                lines: Arc::new(
                    super::utils::CodeLines::new(&code).expect("code has a first line"),
                ),
                native_msgpack_eligible: AtomicBool::new(true),
                include_frame: true,
                has_processor_candidates: false,
            });

            let mut full_won = CodeMetadataCache::default();
            full_won.entries.insert(
                code_id,
                CachedCodeEventMetadata::Full(full_metadata.clone()),
            );
            match full_won.insert_excluded(code_id, code.clone().unbind()) {
                CodeEventMetadataLookup::Full(winner) => {
                    assert!(Arc::ptr_eq(&winner, &full_metadata));
                }
                _ => panic!("the first full metadata entry must win"),
            }

            let mut excluded_won = CodeMetadataCache::default();
            excluded_won.entries.insert(
                code_id,
                CachedCodeEventMetadata::Excluded(code.clone().unbind()),
            );
            excluded_won.excluded_entries = 1;
            assert!(matches!(
                excluded_won.insert_full(code_id, full_metadata),
                CodeEventMetadataLookup::Excluded
            ));
            assert_eq!(excluded_won.entries.len(), 1);
            assert_eq!(excluded_won.excluded_entries, 1);
        });
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
