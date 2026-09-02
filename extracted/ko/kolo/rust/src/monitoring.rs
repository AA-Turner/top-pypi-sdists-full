use hashbrown::{HashMap, HashSet};
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
use pyo3::types::PyBytes;
use pyo3::types::PyCode;
use pyo3::types::PyDict;
use pyo3::types::PyList;
use std::cell::{Cell, RefCell};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
use super::trace_container::{FrameStore, TraceCapture};
use super::utils;
use super::utils::{Event, FrameSequence, LineFrame, SerializedFrame, Serializer};

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
    variable: String,
    opname: Opname,
}

struct CodeInstructionMetadata {
    // Keep the code object alive so the pointer used as the map key cannot be
    // reused for different bytecode during this monitoring session.
    _code: Py<PyCode>,
    filename: String,
    name: String,
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
    fn assignment_value<'py>(
        &self,
        variable: &str,
        frame: &Bound<'py, PyAny>,
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        let py = frame.py();
        match self {
            Opname::StoreFast | Opname::StoreDeref => {
                let locals = frame.getattr(intern!(py, "f_locals"))?;
                Ok(locals.get_item(variable)?)
            }
            Opname::StoreGlobal => {
                let globals = frame.getattr(intern!(py, "f_globals"))?;
                Ok(globals.get_item(variable)?)
            }
        }
    }
}

struct InstructionData {
    variable: String,
    opname: Opname,
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
    timestamp: Mutex<f64>,
    db_path: String,
    source: String,
    one_trace_per_test: bool,
    omit_return_locals: bool,
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
    /// `flush_thread_state`, `suspend_hooks`). 0 = not stamped yet.
    tls_owner_token: ThreadLocal<Cell<u64>>,
    disable: Py<PyAny>,
    instruction_data: ThreadLocal<RefCell<Option<InstructionData>>>,
    instruction_cache: Mutex<HashMap<usize, Arc<CodeInstructionMetadata>>>,
    code_metadata_cache: Mutex<CodeMetadataCache>,
    code_metadata_local: ThreadLocal<RefCell<HashMap<usize, Arc<CodeEventMetadata>>>>,
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
    suspend_hooks: ThreadLocal<RefCell<bool>>,
    /// Relaxed is enough here: the generation only invalidates per-thread TLS state,
    /// and every other shared structure in the flush path is synchronized by Mutex.
    flush_generation: AtomicU64,
    flush_barrier: Mutex<()>,
    /// Subtree stack and flush candidates remain mutex-guarded (only accessed when armed).
    subtree_stack: Mutex<HashMap<String, Vec<OpenSubtree>>>,
    flush_in_progress: Mutex<HashSet<String>>,
    root_trace_id: Mutex<String>,
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
        let dis = PyModule::import(py, "dis")?;
        let disable = monitoring.getattr("DISABLE")?.unbind();
        let current_thread_fn = threading.getattr(intern!(py, "current_thread"))?.unbind();
        let current_thread = current_thread_fn.bind(py).call0()?;
        // Kolo uses tool ID 3 (unassigned) to avoid conflicts with profilers (ID 2)
        let tool_id: u8 = 3;

        let omit_return_locals = config.get_or(py, "omit_return_locals", false)?;
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
            if let Ok(trace_points_dict) = trace_points.downcast::<PyDict>() {
                if let Ok(Some(targets)) = trace_points_dict.get_item("on_return") {
                    if let Ok(targets_list) = targets.downcast::<PyList>() {
                        for item in targets_list.iter() {
                            if let Ok(s) = item.extract::<String>() {
                                trace_point_return_targets.insert(s);
                            }
                        }
                    }
                }
            }
        }

        let flush_subtree_bytes: Option<usize> = resolve_flush_subtree_bytes(config_dict)?;
        let root_trace_id = utils::trace_id();
        let timestamp = utils::timestamp();
        let trace_capture = TraceCapture::for_trace(&db_path, &root_trace_id, timestamp);

        Ok(KoloMonitor {
            active: AtomicBool::new(false),
            #[cfg(test)]
            writer_circuit_override: AtomicBool::new(false),
            tool_id,
            timestamp: Mutex::new(timestamp),
            db_path,
            source,
            one_trace_per_test,
            omit_return_locals,
            sqlite_busy_timeout,
            trace_id: Mutex::new(root_trace_id.clone()),
            explicit_trace_name: trace_name.clone(),
            trace_name: Mutex::new(trace_name),
            include_frames: filters::load_filters(&filters, "include_frames")?,
            ignore_frames: filters::load_filters(&filters, "ignore_frames")?,
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
            instruction_data: ThreadLocal::new(),
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
            suspend_hooks: ThreadLocal::new(),
            flush_generation: AtomicU64::new(0),
            flush_barrier: Mutex::new(()),
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
    /// as its open `call_frames`, `_frame_ids`, `instruction_data`, and
    /// `suspend_hooks` flag.
    ///
    /// Detect recycling by stamping each slot with a process-unique
    /// per-OS-thread token (`OS_THREAD_TOKEN`, native `std::thread_local!`
    /// storage, never recycled) and clear all cached per-thread state when
    /// the slot changed hands.
    ///
    /// Must run at the top of every entry point that can execute on an
    /// arbitrary thread — the monitoring callbacks and `set_suspend_hooks`
    /// — before any other per-thread state is read.
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
        if let Some(code_metadata) = self.code_metadata_local.get() {
            code_metadata.borrow_mut().clear();
        }
        if let Some(flush_state) = self.flush_thread_state.get() {
            *flush_state.borrow_mut() = Default::default();
        }
        if let Some(suspend_hooks) = self.suspend_hooks.get() {
            *suspend_hooks.borrow_mut() = false;
        }
        owner.set(token);
    }

    fn include(
        &self,
        py: Python,
        processor: &PluginProcessor,
        event: Event,
        filename: &str,
        arg: utils::Arg,
    ) -> Result<Option<(String, SerializedFrame)>, PyErr> {
        let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
        let arg = arg.into_inner(py);
        if !processor.matches_frame(py, &frame, event, &arg, filename)? {
            return Ok(None);
        }
        let frame = frame.cast()?;
        let call_frames = self.call_frames.get_or_default().borrow().get_bound(py);
        processor.process(py, frame, event, &arg, call_frames, self.lightweight_repr)
    }

    fn monitor(
        &self,
        code: &Bound<'_, PyCode>,
        arg: utils::Arg,
        event: Event,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let py = code.py();
        if *self.suspend_hooks.get_or_default().borrow() {
            return match event {
                Event::Call | Event::Return | Event::Resume | Event::Yield => {
                    Ok(Some(self.disable.clone_ref(py)))
                }
                Event::Unwind | Event::Throw => Ok(None),
            };
        }
        let metadata = match self.code_event_metadata(code)? {
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
                self.track_direct_frame(py, event, name, &push_result, !defer_subtree_flush)?;
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
            if let Some(processors) = default_include_frames.get(name) {
                for processor in processors.iter() {
                    if let Some((frame_type, frame_data)) =
                        self.include(py, processor, event, filename, arg.clone())?
                    {
                        frames.push(frame_data);
                        frame_types.push(frame_type);
                    }
                }
            }
            drop(default_include_frames);
            if include_frame {
                if let Some(frame_data) = self.process(py, name, event, arg, metadata.as_deref())? {
                    frames.push(frame_data);
                    frame_types.push("frame".to_string());
                }
            } else if frames.is_empty() {
                match event {
                    Event::Call | Event::Return | Event::Resume | Event::Yield => {
                        return Ok(Some(self.disable.clone_ref(py)))
                    }
                    Event::Unwind | Event::Throw => return Ok(None),
                }
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
                Event::Return | Event::Unwind | Event::Yield => self.push_frames_return(
                    py,
                    &mut frames,
                    &mut frame_types,
                    !defer_subtree_flush,
                )?,
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
            let suspend_hooks = self.suspend_hooks.get_or_default();
            let hooks_were_suspended = {
                let suspend_hooks = suspend_hooks.borrow();
                *suspend_hooks
            };
            if !hooks_were_suspended {
                *suspend_hooks.borrow_mut() = true;
            }

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

            if !hooks_were_suspended {
                *suspend_hooks.borrow_mut() = false;
            }

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
        trace_point_result.and(flush_result)?;

        Ok(None)
    }

    fn process(
        &self,
        py: Python,
        name: &str,
        event: Event,
        arg: utils::Arg,
        metadata: Option<&CodeEventMetadata>,
    ) -> Result<Option<SerializedFrame>, PyErr> {
        let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_ids = self._frame_ids.get_or_default();
        let frame_id = match event {
            Event::Call | Event::Resume | Event::Throw => {
                frame_ids.borrow_mut().get_or_set(event, pyframe_id)
            }
            Event::Return | Event::Unwind | Event::Yield => {
                let Some(frame_id) = frame_ids.borrow().get_option(pyframe_id) else {
                    return Ok(None);
                };
                frame_id
            }
        };
        let pyframe = frame.cast()?;
        let user_code_call_site = self
            .call_frames
            .get_or_default()
            .borrow_mut()
            .get_user_code_call_site(pyframe, event, &frame_id)?;
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
                true,
                (
                    metadata.relative_path.as_str(),
                    Some(metadata.co_qualname.as_str()),
                    Some(&metadata.native_msgpack_eligible),
                ),
                None,
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
                true,
                None,
            )?,
        }
        Ok(Some(buf))
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
                let Some(frame_id) = frame_ids.borrow().get_option(pyframe_id) else {
                    return Ok(None);
                };
                frame_id
            }
        };
        let pyframe = frame.cast()?;
        let user_code_call_site = self
            .call_frames
            .get_or_default()
            .borrow_mut()
            .get_user_code_call_site(pyframe, event, &frame_id)?;

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
                true,
                (
                    metadata.relative_path.as_str(),
                    Some(metadata.co_qualname.as_str()),
                    Some(&metadata.native_msgpack_eligible),
                ),
                Some(utils::ValueInterningContext::fixed(
                    &self.value_interning,
                    capture,
                )),
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
                true,
                Some(utils::ValueInterningContext::fixed(
                    &self.value_interning,
                    capture,
                )),
            ),
        })
        .map(Some)
    }

    fn code_event_metadata(
        &self,
        code: &Bound<'_, PyCode>,
    ) -> Result<CodeEventMetadataLookup, PyErr> {
        let py = code.py();
        let code_id = code.as_ptr() as usize;
        let local_cache = self.code_metadata_local.get_or_default();
        if let Some(metadata) = local_cache.borrow().get(&code_id).cloned() {
            return Ok(CodeEventMetadataLookup::Full(metadata));
        }
        if let Some(metadata) = self
            .code_metadata_cache
            .lock_py_attached(py)
            .expect("code metadata cache mutex poisoned")
            .lookup(code_id)
        {
            if let CodeEventMetadataLookup::Full(metadata) = &metadata {
                if metadata.include_frame {
                    local_cache.borrow_mut().insert(code_id, metadata.clone());
                }
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
            return Ok(cache.insert_excluded(code_id, code.clone().unbind()));
        }

        let metadata = Arc::new(CodeEventMetadata {
            _code: code.clone().unbind(),
            relative_path: self.frame_paths.relative_path(&filename),
            co_qualname: code
                .getattr(intern!(py, "co_qualname"))?
                .extract::<String>()?,
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
                local_cache.borrow_mut().insert(code_id, metadata.clone());
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
        let suspend_hooks = self.suspend_hooks.get_or_default();
        *suspend_hooks.borrow_mut() = true;
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
        *suspend_hooks.borrow_mut() = false;
        result
    }

    fn _monitor_instruction(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let py = code.py();
        if *self.suspend_hooks.get_or_default().borrow() {
            return Ok(Some(self.disable.clone_ref(py)));
        }
        let metadata = self.instruction_metadata(code)?;
        let Some(instruction) = metadata.instructions.get(&instruction_offset) else {
            return Ok(Some(self.disable.clone_ref(py)));
        };

        match self.include_frame(py, &metadata.filename)? {
            true => {
                self.process_instruction(
                    py,
                    &metadata.name,
                    &instruction.variable,
                    instruction.opname,
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
            let opname = match instruction
                .getattr(intern!(py, "opname"))?
                .extract::<&str>()?
            {
                "STORE_FAST" => Opname::StoreFast,
                "STORE_GLOBAL" => Opname::StoreGlobal,
                "STORE_DEREF" => Opname::StoreDeref,
                _ => continue,
            };
            let argval = instruction.getattr(intern!(py, "argval"))?;
            if argval.is_none() {
                continue;
            }
            let Ok(variable) = argval.extract::<String>() else {
                continue;
            };
            if variable.starts_with('@') {
                continue;
            }
            let offset = instruction
                .getattr(intern!(py, "offset"))?
                .extract::<usize>()?;
            instructions.insert(offset, CachedInstruction { variable, opname });
        }

        let metadata = Arc::new(CodeInstructionMetadata {
            _code: code.clone().unbind(),
            filename: code
                .getattr(intern!(py, "co_filename"))?
                .extract::<String>()?,
            name: code.getattr(intern!(py, "co_name"))?.extract::<String>()?,
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
        variable: &str,
        opname: Opname,
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
            frame_id,
            utils::timestamp(),
        );
        self.instruction_data
            .get_or_default()
            .replace(Some(InstructionData {
                opname,
                variable: variable.to_string(),
                line_frame: frame.unbind(),
                line_frame_data,
            }));
        Ok(())
    }

    fn process_assignment(&self, py: Python) -> Result<(), PyErr> {
        if *self.suspend_hooks.get_or_default().borrow() {
            return Ok(());
        }
        let instruction_data = match self.instruction_data.get_or_default().replace(None) {
            None => return Ok(()),
            Some(instruction_data) => instruction_data,
        };
        let frame = instruction_data.line_frame.bind(py);
        let variable = instruction_data.variable;
        let assign = instruction_data.opname.assignment_value(&variable, frame)?;
        let push_result = self.append_encoded_frame(py, |arena, _capture| {
            instruction_data.line_frame_data.write_msgpack_into(
                arena,
                &self.serializer,
                (&variable, assign),
                self.lightweight_repr,
            )
        })?;
        self.track_direct_leaf(py, &push_result)?;
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
            let _flush_barrier = self.flush_barrier.lock_py_attached(py).expect("mutex");
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
            let suspend_hooks = self.suspend_hooks.get_or_default();
            let hooks_were_suspended = *suspend_hooks.borrow();
            if !hooks_were_suspended {
                *suspend_hooks.borrow_mut() = true;
            }
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
            if !hooks_were_suspended {
                *suspend_hooks.borrow_mut() = false;
            }
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
            let suspend_hooks = self.suspend_hooks.get_or_default();
            let hooks_were_suspended = {
                let suspend_hooks = suspend_hooks.borrow();
                *suspend_hooks
            };
            if !hooks_were_suspended {
                *suspend_hooks.borrow_mut() = true;
            }

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

            if !hooks_were_suspended {
                *suspend_hooks.borrow_mut() = false;
            }

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
        let _flush_barrier = self.flush_barrier.lock_py_attached(py).expect("mutex");
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
        let _flush_barrier = self.flush_barrier.lock_py_attached(py).expect("mutex");
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

        let suspend_hooks = self.suspend_hooks.get_or_default();
        *suspend_hooks.borrow_mut() = true;
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
        *suspend_hooks.borrow_mut() = false;
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

    /// Check if we should exclude the current frame from the trace using Kolo's builtin filters.
    fn process_default_ignore_frames(&self, py: Python, co_filename: &str) -> Result<bool, PyErr> {
        if filters::library_filter(co_filename)
            || filters::frozen_filter(co_filename)
            || filters::kolo_filter(co_filename)
            || filters::exec_filter(co_filename)
            || filters::pytest_generated_filter(co_filename)
        {
            Ok(true)
        } else {
            filters::attrs_filter_monitoring(py, co_filename)
        }
    }

    /// Check if we should include the current frame in the trace.
    fn include_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        Ok(self.include_frames.check(filename) || !self.ignore_frame(py, filename)?)
    }

    /// Check if we should exclude the current frame from the trace.
    fn ignore_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        Ok(self.process_default_ignore_frames(py, filename)? || self.ignore_frames.check(filename))
    }

    fn log_error(&self, py: Python, err: PyErr) {
        let logging = PyModule::import(py, "logging").unwrap();
        let logger = logging.call_method1("getLogger", ("kolo",)).unwrap();

        let kwargs = PyDict::new(py);
        kwargs.set_item("exc_info", err).unwrap();

        logger
            .call_method("warning", ("Unexpected exception in Rust.",), Some(&kwargs))
            .unwrap();
    }

    fn return_or_log(&self, py: Python, value: Result<Option<Py<PyAny>>, PyErr>) -> Py<PyAny> {
        match value {
            Ok(Some(disable)) => disable,
            Ok(None) => py.None(),
            Err(err) => {
                self.log_error(py, err);
                self.disable_events_after_writer_circuit(py);
                py.None()
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
        let _ = PyModule::import(py, "sys")
            .and_then(|sys| sys.getattr("monitoring"))
            .and_then(|monitoring| monitoring.call_method1("set_events", (self.tool_id, 0)));
    }

    fn begin_callback(&self, py: Python, event: Event) -> Option<Py<PyAny>> {
        self.reset_recycled_thread_state();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
            if self.writer_circuit_is_open() {
                self.disable_events_after_writer_circuit(py);
                return Some(match event {
                    Event::Call | Event::Return | Event::Resume | Event::Yield => {
                        self.disable.clone_ref(py)
                    }
                    Event::Unwind | Event::Throw => py.None(),
                });
            }
        }
        None
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
        self.active.store(value, Ordering::Release);
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

    /// Set the per-thread ``suspend_hooks`` flag from Python.
    ///
    /// Needed for the async trace-point save worker: the daemon worker
    /// runs sqlite/msgpack/emit work that would otherwise trip Rust
    /// monitor callbacks on *that* thread (where ``suspend_hooks`` is
    /// false by default). The Python wrapper calls
    /// ``monitor.set_suspend_hooks(True)`` once at worker startup so the
    /// Rust monitor short-circuits any callbacks on that thread for the
    /// worker's entire lifetime — the flag is set once and never cleared.
    ///
    /// Uses ``&self`` for the same reason as ``set_active`` — we can't
    /// require an exclusive borrow on the pyclass while other threads
    /// hold shared borrows via in-flight monitor callbacks.
    fn set_suspend_hooks(&self, value: bool) {
        // Stamp this thread's slot first so a later monitor callback on the
        // same thread doesn't mistake the flag for a dead thread's leftover
        // state and clear it.
        self.reset_recycled_thread_state();
        let cell = self.suspend_hooks.get_or_default();
        *cell.borrow_mut() = value;
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

    /// Paths for code objects whose values made the native frame encoder
    /// fall back to Python serialization. This scans cached metadata only
    /// when requested; tracking eligibility already happens on the event path.
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
                let layouts = frames_by_thread
                    .values_mut()
                    .map(|frames| frames.layout())
                    .collect::<Result<Vec<_>, _>>()
                    .map_err(pyo3::exceptions::PyOSError::new_err)?;
                capture
                    .finish(prepared.thread_meta, prepared.metadata, layouts)
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
                PyModule::import(py, "kolo.db")?
                    .getattr(intern!(py, "logger"))?
                    .call_method1(intern!(py, "warning"), (message,))?;
                Ok(())
            }
            result => result,
        }
    }

    fn build_trace(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        self.build_trace_inner(py)
    }

    fn monitor_pystart(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Call) {
            return disabled;
        }
        self.return_or_log(py, self.monitor(code, utils::Arg::None, Event::Call))
    }

    fn monitor_pyreturn(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        retval: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Return) {
            return disabled;
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Argument(retval), Event::Return),
        )
    }

    fn monitor_pyunwind(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        exception: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Unwind) {
            return disabled;
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Exception(exception), Event::Unwind),
        )
    }

    fn monitor_pyresume(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Resume) {
            return disabled;
        }
        self.return_or_log(py, self.monitor(code, utils::Arg::None, Event::Resume))
    }

    fn monitor_pyyield(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        retval: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Yield) {
            return disabled;
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Argument(retval), Event::Yield),
        )
    }

    fn monitor_pythrow(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        exception: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Throw) {
            return disabled;
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Exception(exception), Event::Throw),
        )
    }

    fn monitor_instruction(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Some(disabled) = self.begin_callback(py, Event::Call) {
            return disabled;
        }
        self.return_or_log(py, self._monitor_instruction(code, instruction_offset))
    }
}

#[cfg(test)]
mod tests {
    use super::subtree_flush::extract_co_name;
    use super::{
        discard_frame_buffers, CachedCodeEventMetadata, CodeEventMetadata, CodeEventMetadataLookup,
        CodeMetadataCache, FrameSequence, FrameStore, InstructionData, KoloMonitor, LineFrame,
        Opname, RestoreGuard, SerializedFrame, TraceCapture,
    };
    use hashbrown::HashMap;
    use pyo3::exceptions::PyRuntimeError;
    use pyo3::sync::MutexExt;
    use pyo3::types::{PyAnyMethods, PyBytes, PyCode, PyCodeInput, PyDict, PyModule};
    use pyo3::{Py, PyResult, Python};
    use rmpv::Value;
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
    use std::sync::{Arc, Mutex};

    static TEST_CAPTURE_ID: AtomicUsize = AtomicUsize::new(0);
    // Hold while a test patches or exercises process-wide sys.monitoring events.
    static MONITORING_PATCH_LOCK: Mutex<()> = Mutex::new(());

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

    fn inject_assignment_error(monitor: &KoloMonitor, py: Python) {
        monitor
            .instruction_data
            .get_or_default()
            .replace(Some(InstructionData {
                variable: "missing".to_string(),
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
    }

    #[test]
    fn writer_circuit_disables_every_monitoring_callback_after_an_error() {
        let _monitoring_patch = MONITORING_PATCH_LOCK
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
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
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyreturn(&code, 0, value.bind(py))
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyunwind(&code, 0, value.bind(py))
                .bind(py)
                .is_none());
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyresume(&code, 0)
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pyyield(&code, 0, value.bind(py))
                .bind(py)
                .is(monitor.disable.bind(py)));
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_pythrow(&code, 0, value.bind(py))
                .bind(py)
                .is_none());
            inject_assignment_error(&monitor, py);
            assert!(monitor
                .monitor_instruction(&code, 0)
                .bind(py)
                .is(monitor.disable.bind(py)));

            // The generic callback error path must also attempt to turn the
            // process-wide event mask off after the circuit opens.
            monitor.return_or_log(py, Err(PyRuntimeError::new_err("writer circuit")));
        });
    }

    #[test]
    fn value_publication_circuit_disables_events_in_the_same_callback() {
        let _monitoring_patch = MONITORING_PATCH_LOCK
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
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
