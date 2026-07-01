use hashbrown::{HashMap, HashSet};
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
use pyo3::types::PyBytes;
use pyo3::types::PyCode;
use pyo3::types::PyDict;
use pyo3::types::PyList;
use std::borrow::Cow;
use std::cell::RefCell;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Mutex;
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
use super::utils;
use super::utils::{Event, LineFrame, SerializedFrame, Serializer};

/// Per-thread flush tracking state stored in ThreadLocal to avoid mutex overhead.
#[derive(Default)]
struct FlushThreadState {
    cumulative_bytes: usize,
    armed: bool,
    generation: u64,
    thread_id: Option<String>,
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
    OnReturn(usize),
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

#[allow(clippy::enum_variant_names)]
enum Opname {
    StoreFast,
    StoreGlobal,
    StoreDeref,
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
    default_include_frames: Mutex<HashMap<String, Vec<PluginProcessor>>>,
    #[pyo3(get)]
    line_events: bool,
    frames_by_thread: Mutex<HashMap<String, Vec<SerializedFrame>>>,
    threads: Mutex<HashMap<String, Py<PyAny>>>,
    current_thread_id: String,
    current_thread_fn: Py<PyAny>,
    sys_getframe_fn: Py<PyAny>,
    lightweight_repr: bool,
    serializer: Serializer,
    // NOTE: `thread_local::ThreadLocal<RefCell<...>>` entries are keyed by
    // the OS thread and persist after that thread exits — they are only
    // reclaimed when the whole `KoloMonitor` is dropped. In practice this
    // is bounded by the number of distinct threads the process ever spawns
    // while tracing is active, which is small enough to ignore. We've
    // decided this is won't-fix; see #2535 item 1.
    call_frames: ThreadLocal<RefCell<utils::CallFrames>>,
    _frame_ids: ThreadLocal<RefCell<utils::FrameIds>>,
    disable: Py<PyAny>,
    instruction_data: ThreadLocal<RefCell<Option<InstructionData>>>,
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
    thread_id: String,
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

        Ok(KoloMonitor {
            active: AtomicBool::new(false),
            tool_id,
            timestamp: Mutex::new(utils::timestamp()),
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
            threads: Mutex::new(HashMap::new()),
            current_thread_id: utils::get_thread_id(current_thread.as_ref(), py)?,
            current_thread_fn,
            sys_getframe_fn: sys.getattr(intern!(py, "_getframe"))?.unbind(),
            lightweight_repr,
            serializer: Serializer::new(py)?,
            call_frames: ThreadLocal::new(),
            _frame_ids: ThreadLocal::new(),
            disable,
            instruction_data: ThreadLocal::new(),
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
        let co_filename = code
            .getattr(intern!(py, "co_filename"))
            .expect("Code objects always define co_filename");
        let co_name = code
            .getattr(intern!(py, "co_name"))
            .expect("Code objects always define co_name");
        let filename = co_filename
            .extract()
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
                if let Some((frame_type, frame_data)) =
                    self.include(py, processor, event, filename, arg.clone())?
                {
                    frames.push(frame_data);
                    frame_types.push(frame_type);
                }
            }
        };
        if self.include_frame(py, filename)? {
            let frame_data = self.process(py, &name, event, arg)?;
            frames.push(frame_data);
            frame_types.push("frame".to_string());
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
                self.push_frames_call(py, &mut frames, frame_types, name.as_ref())?
            }
            Event::Return | Event::Unwind | Event::Yield => {
                self.push_frames_return(py, &mut frames, &mut frame_types)?
            }
        }

        // Trace points: record markers on call, save on return
        if target_frame_appended
            && !self.trace_point_return_targets.is_empty()
            && self.trace_point_return_targets.contains(name.as_ref())
        {
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
                    let fbt = self
                        .frames_by_thread
                        .lock_py_attached(py)
                        .expect("frames mutex");
                    if let Some(all) = fbt.get(&thread_id) {
                        if !all.is_empty() {
                            let start = all.len() - 1;
                            drop(fbt);
                            self.trace_point_markers
                                .lock_py_attached(py)
                                .expect("markers mutex")
                                .entry(thread_id)
                                .or_default()
                                .push(MarkerKind::OnReturn(start));
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
                            Some(MarkerKind::OnReturn(start)) => {
                                let start = *start;
                                stack.pop();
                                Some(start)
                            }
                            _ => None,
                        });
                    drop(markers);
                    if let Some(start) = popped {
                        let fbt = self
                            .frames_by_thread
                            .lock_py_attached(py)
                            .expect("frames mutex");
                        let slice: Option<Vec<Vec<u8>>> = fbt.get(&thread_id).and_then(|all| {
                            if start < all.len() {
                                Some(all[start..].to_vec())
                            } else {
                                None
                            }
                        });
                        drop(fbt);
                        if let Some(slice) = slice {
                            if let Err(err) = self.save_trace_point(py, &thread_id, slice, &name) {
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
                        if matches!(stack.last(), Some(MarkerKind::OnReturn(_))) {
                            stack.pop();
                        }
                    }
                }
                _ => {}
            }
        }

        Ok(None)
    }

    fn process(
        &self,
        py: Python,
        name: &str,
        event: Event,
        arg: utils::Arg,
    ) -> Result<SerializedFrame, PyErr> {
        let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_id = self
            ._frame_ids
            .get_or_default()
            .borrow_mut()
            .get_or_set(event, pyframe_id);
        let pyframe = frame.cast()?;
        let user_code_call_site = self
            .call_frames
            .get_or_default()
            .borrow_mut()
            .get_user_code_call_site(pyframe, event, &frame_id)?;
        let mut buf: Vec<u8> = vec![];
        utils::write_frame_with_serializer(
            &mut buf,
            pyframe,
            &self.serializer,
            user_code_call_site,
            arg,
            event,
            name,
            &frame_id,
            self.lightweight_repr,
            self.omit_return_locals,
        )?;
        Ok(buf)
    }

    /// Save a trace point by delegating to the Python monitoring module's helper.
    fn save_trace_point(
        &self,
        py: Python,
        thread_id: &str,
        frames_slice: Vec<Vec<u8>>,
        func_name: &str,
    ) -> Result<(), PyErr> {
        // Convert frame bytes to Python bytes objects
        let py_frames: Vec<Py<PyBytes>> = frames_slice
            .iter()
            .map(|f| PyBytes::new(py, f).unbind())
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
        let kolo_monitoring = PyModule::import(py, "kolo.monitoring")?;
        let instruction = kolo_monitoring
            .call_method1(intern!(py, "get_instruction"), (code, instruction_offset))?;
        if instruction.is_none() {
            return Ok(Some(self.disable.clone_ref(py)));
        }
        let opname = match instruction.getattr(intern!(py, "opname"))?.extract()? {
            "STORE_FAST" => Opname::StoreFast,
            "STORE_GLOBAL" => Opname::StoreGlobal,
            "STORE_DEREF" => Opname::StoreDeref,
            _ => {
                return Ok(Some(self.disable.clone_ref(py)));
            }
        };
        let argval = instruction.getattr(intern!(py, "argval"))?;
        if !argval.is_none() && argval.extract::<&str>()?.starts_with('@') {
            return Ok(Some(self.disable.clone_ref(py)));
        }

        let co_filename = code
            .getattr(intern!(py, "co_filename"))
            .expect("Code objects always define co_filename");
        let co_name = code
            .getattr(intern!(py, "co_name"))
            .expect("Code objects always define co_name");
        let filename = co_filename
            .extract()
            .expect("`co_filename` is always a string");
        let name = co_name.extract().expect("`co_name` is always a string");

        match self.include_frame(py, filename)? {
            true => {
                self.process_instruction(filename, name, instruction, opname)?;
                Ok(None)
            }
            false => Ok(Some(self.disable.clone_ref(py))),
        }
    }

    fn process_instruction(
        &self,
        filename: &str,
        name: &str,
        instruction: Bound<'_, PyAny>,
        opname: Opname,
    ) -> Result<(), PyErr> {
        let py = instruction.py();
        let frame = self.sys_getframe_fn.bind(py).call1((0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_id = self
            ._frame_ids
            .get_or_default()
            .borrow()
            .get_option(pyframe_id);
        let pyframe = frame.cast()?;

        let variable = instruction.getattr(intern!(py, "argval"))?.extract()?;
        let lineno = frame.getattr(intern!(py, "f_lineno"))?.extract()?;
        let line_frame_data = LineFrame::new(
            utils::format_frame_path(filename, lineno),
            name.to_string(),
            utils::get_qualname(pyframe, py)?.expect("qualname always exists on Python 3.12+"),
            frame_id,
            utils::timestamp(),
        );
        self.instruction_data
            .get_or_default()
            .replace(Some(InstructionData {
                opname,
                variable,
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
        let mut frames = vec![instruction_data.line_frame_data.write_msgpack(
            &self.serializer,
            (&variable, assign),
            self.lightweight_repr,
        )?];
        self.push_frame_data(py, &mut frames, true)?;
        Ok(())
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

    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let (frames_by_thread, trace_id, root_trace_id, timestamp) = {
            let _flush_barrier = self.flush_barrier.lock_py_attached(py).expect("mutex");
            let frames_by_thread = std::mem::take(
                &mut *self
                    .frames_by_thread
                    .lock_py_attached(py)
                    .expect("mutex poisoned"),
            );
            self.reset_subtree_tracking(py);
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
            let timestamp = *self
                .timestamp
                .lock_py_attached(py)
                .expect("timestamp mutex poisoned");
            (frames_by_thread, trace_id, root_trace_id, timestamp)
        };

        // Extract trace name if one wasn't explicitly set
        let trace_name = self.trace_name_for_frames(py, &frames_by_thread);

        let threads: HashMap<String, Py<PyAny>> = self
            .threads
            .lock_py_attached(py)
            .expect("mutex poisoned")
            .iter()
            .map(|(thread_id, thread)| (thread_id.clone(), thread.clone_ref(py)))
            .collect();

        utils::build_trace(
            py,
            frames_by_thread,
            threads,
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            timestamp,
            &self.config,
            true, // use_monitoring
            Some(&root_trace_id),
        )
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
        let push_result = self.push_frame_data(py, frames, false)?;
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
    ) -> Result<(), PyErr> {
        frames.reverse();
        frame_types.reverse();
        let mut drained_count = 0;
        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                if frame_type.as_str() == "end_test" {
                    let mut before: Vec<SerializedFrame> = frames.drain(..index + 1).collect();
                    drained_count = index + 1;
                    self.push_frame_data(py, &mut before, true)?;
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
        let Some(push_result) = self.push_frame_data(py, frames, false)? else {
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
            self.maybe_flush_segments_with_current_bytes(
                py,
                &thread_id,
                push_result.current_bytes,
            )?;
        }
        Ok(())
    }

    fn push_frame_data(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
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
            flush_state.borrow_mut().thread_id = Some(thread_id.clone());
            thread_id
        };

        let flush_enabled = self.flush_subtree_bytes.is_some();
        let added_bytes = if flush_enabled {
            frames.iter().map(|frame| frame.len()).sum()
        } else {
            0
        };
        let (start_index, end_index) = {
            let mut frames_by_thread = self
                .frames_by_thread
                .lock_py_attached(py)
                .expect("mutex poisoned");
            let thread_frames = frames_by_thread
                .entry(thread_id.clone())
                .or_insert_with(Vec::new);
            let start_index = thread_frames.len();
            thread_frames.append(frames);
            (start_index, thread_frames.len())
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

            state.cumulative_bytes += added_bytes;
            if state.armed || self.tracking_start_bytes == 0 {
                state.armed = true;
                (added_bytes, state.cumulative_bytes, true)
            } else if state.cumulative_bytes < self.tracking_start_bytes {
                (0, state.cumulative_bytes, false)
            } else {
                state.armed = true;
                (added_bytes, state.cumulative_bytes, true)
            }
        };

        if record_closed_leaf {
            let co_name = {
                let frames_by_thread = self
                    .frames_by_thread
                    .lock_py_attached(py)
                    .expect("mutex poisoned");
                let thread_frames = frames_by_thread
                    .get(&thread_id)
                    .expect("thread frames missing after append");
                subtree_flush::extract_co_name(&thread_frames[start_index..end_index])
            };
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
        *self_root_trace_id = trace_id;
        *self
            .trace_name
            .lock_py_attached(py)
            .expect("mutex poisoned") = self.explicit_trace_name.clone();

        // Clear `frames_by_thread` of earlier frames.
        let mut frames_by_thread = self
            .frames_by_thread
            .lock_py_attached(py)
            .expect("mutex poisoned");
        *frames_by_thread = HashMap::new();
        drop(frames_by_thread);

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
                    MarkerKind::OnReturn(_) => {
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
        let mut restore_guard = {
            let mut fbt = self.frames_by_thread.lock_py_attached(py).expect("mutex");
            let frames = match fbt.get_mut(thread_id) {
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
        let save_result: PyResult<()> = (|| {
            let root_trace_id = self
                .root_trace_id
                .lock_py_attached(py)
                .expect("mutex")
                .clone();

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
                true,
                Some(&root_trace_id),
            )?;

            let save_kwargs = PyDict::new(py);
            save_kwargs.set_item("timeout", self.sqlite_busy_timeout)?;
            save_kwargs.set_item("msgpack_data", data)?;

            let pathlib = PyModule::import(py, "pathlib")?;
            let path_class = pathlib.getattr(intern!(py, "Path"))?;
            let db_path_obj = path_class.call1((&self.db_path,))?;
            save_kwargs.set_item("db_path", db_path_obj)?;

            let db_module = PyModule::import(py, "kolo.db")?;
            let save_trace_fn = db_module.getattr(intern!(py, "save_trace"))?;
            let save_result = save_trace_fn.call((&subtrace_id,), Some(&save_kwargs));
            save_result?;
            Ok(())
        })();
        *suspend_hooks.borrow_mut() = false;
        if let Err(err) = save_result {
            return Err(err);
        }
        let placeholder_len = placeholder_buf.len();
        let mut fbt = self.frames_by_thread.lock_py_attached(py).expect("mutex");
        let frames = match fbt.get_mut(thread_id) {
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
        drop(fbt);

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
                    MarkerKind::OnReturn(idx) => *idx < start_index || *idx >= end_index,
                });
                for marker in stack.iter_mut() {
                    if let MarkerKind::OnReturn(idx) = marker {
                        if *idx >= end_index {
                            *idx -= shift;
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
            | filters::frozen_filter(co_filename)
            | filters::kolo_filter(co_filename)
            | filters::exec_filter(co_filename)
            | filters::pytest_generated_filter(co_filename)
        {
            Ok(true)
        } else {
            filters::attrs_filter_monitoring(py, co_filename)
        }
    }

    /// Check if we should include the current frame in the trace.
    fn include_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        Ok(self.include_frames.check(filename) | !self.ignore_frame(py, filename)?)
    }

    /// Check if we should exclude the current frame from the trace.
    fn ignore_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        Ok(self.process_default_ignore_frames(py, filename)? | self.ignore_frames.check(filename))
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
                py.None()
            }
        }
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

    fn save(&self, py: Python) -> Result<(), PyErr> {
        let trace = self.build_trace_inner(py)?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("timeout", self.sqlite_busy_timeout)?;
        kwargs.set_item("msgpack_data", trace)?;

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

    fn build_trace(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        self.build_trace_inner(py)
    }

    fn monitor_pystart(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
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
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
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
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Exception(exception), Event::Unwind),
        )
    }

    fn monitor_pyresume(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
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
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
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
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
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
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(py, self._monitor_instruction(code, instruction_offset))
    }
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
