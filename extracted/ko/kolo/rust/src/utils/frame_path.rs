use hashbrown::HashMap;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
#[cfg(kolo_line_table)]
use pyo3::sync::PyOnceLock;
use pyo3::types::{PyAny, PyCode, PyFrame};
use pyo3::{ffi, intern};
use std::env::current_dir;
use std::path::{Component, Path, PathBuf};
use std::sync::Mutex;

/// The line of every instruction of one code object.
///
/// `PyFrame_GetLineNumber` scans the code's line table from the start on
/// every call (`PyCode_Addr2Line`), which dominates frame metadata for long
/// functions. The table is built once, on first use, from `co_lines()`, the
/// same address ranges `PyCode_Addr2Line` walks. The code object is held so
/// its address identifies it for as long as the table exists.
///
/// Built only where `kolo_line_table` is set (GIL builds of CPython
/// 3.12-3.15, see `build.rs`). From 3.13, `PyCode_Addr2Line` answers from
/// the code's LINE instrumentation data instead once that exists, so the
/// table is consulted only while it does not (see `co_monitoring`).
pub struct CodeLines {
    #[cfg_attr(not(kolo_line_table), allow(dead_code))]
    code: Py<PyCode>,
    #[cfg(kolo_line_table)]
    first_line: i32,
    #[cfg(kolo_line_table)]
    lines: PyOnceLock<Box<[i32]>>,
}

impl CodeLines {
    pub fn new(code: &Bound<'_, PyCode>) -> Result<Self, PyErr> {
        Ok(Self {
            code: code.clone().unbind(),
            #[cfg(kolo_line_table)]
            first_line: code
                .getattr(intern!(code.py(), "co_firstlineno"))?
                .extract()?,
            #[cfg(kolo_line_table)]
            lines: PyOnceLock::new(),
        })
    }

    /// Lines indexed by code unit; -1 where an instruction has no line,
    /// as `PyCode_Addr2Line` reports it for uninstrumented code.
    #[cfg(kolo_line_table)]
    pub(super) fn lines(&self, py: Python<'_>) -> Result<&[i32], PyErr> {
        self.lines
            .get_or_try_init(py, || {
                let mut lines = Vec::new();
                for range in self
                    .code
                    .bind(py)
                    .call_method0(intern!(py, "co_lines"))?
                    .try_iter()?
                {
                    let (start, end, line): (usize, usize, Option<i32>) = range?.extract()?;
                    let (start, end) = (start / CODE_UNIT, end / CODE_UNIT);
                    if lines.len() < end {
                        lines.resize(end, -1);
                    }
                    lines[start..end].fill(line.unwrap_or(-1));
                }
                Ok(lines.into_boxed_slice())
            })
            .map(|lines| &lines[..])
    }

    /// `PyFrame_GetLineNumber(frame)` for a frame running this code, when
    /// it is the table lookup: `None` defers to CPython. CPython only scans
    /// the table while the frame's `f_lineno` field is 0; other values come
    /// from line tracing or a `f_lineno` jump (or, from 3.13, -1: not yet
    /// computed) and are CPython's to resolve.
    #[cfg(kolo_line_table)]
    pub(super) fn frame_line(&self, frame: &Bound<'_, PyFrame>) -> Result<Option<i32>, PyErr> {
        /// The head of `struct _frame`, unchanged from 3.11 through 3.15
        /// (GIL builds).
        #[repr(C)]
        struct FrameHead {
            ob_base: ffi::PyObject,
            f_back: *mut ffi::PyObject,
            f_frame: *mut std::ffi::c_void,
            f_trace: *mut ffi::PyObject,
            f_lineno: std::ffi::c_int,
        }
        // The one-time layout check runs Python code; finish it before
        // reading any frame state.
        #[cfg(Py_3_13)]
        if !co_monitoring::verified(frame.py()) {
            return Ok(None);
        }
        let frame_ptr = frame.as_ptr();
        // Safety: `frame` is an exact frame object (frames cannot be
        // subclassed), whose layout starts with `FrameHead`; the code is a
        // new reference released immediately, only its address is compared.
        let lasti = unsafe {
            if (*frame_ptr.cast::<FrameHead>()).f_lineno != 0 {
                return Ok(None);
            }
            let code = ffi::PyFrame_GetCode(frame_ptr.cast());
            let same_code = code.cast::<ffi::PyObject>() == self.code.as_ptr();
            ffi::Py_DECREF(code.cast());
            if !same_code {
                return Ok(None);
            }
            ffi::PyFrame_GetLasti(frame_ptr.cast())
        };
        // `PyCode_Addr2Line` answers a negative offset (no instruction run
        // yet) with `co_firstlineno`, before looking at instrumentation.
        let Ok(offset) = usize::try_from(lasti) else {
            return Ok(Some(self.first_line).filter(|line| *line >= 0));
        };
        #[cfg(Py_3_13)]
        if !co_monitoring::answers_from_line_table(frame.py(), &self.code) {
            return Ok(None);
        }
        let line = self
            .lines(frame.py())?
            .get(offset / CODE_UNIT)
            .copied()
            .unwrap_or(-1);
        Ok((line >= 0).then_some(line))
    }
}

/// From 3.13, `PyCode_Addr2Line` (codeobject.c) answers from
/// `code->_co_monitoring->lines` whenever both pointers are non-NULL, i.e.
/// once any tool (including `sys.settrace`, which runs on `sys.monitoring`)
/// has enabled LINE or INSTRUCTION events on the code; that data stays
/// allocated after the events are turned off again. Only while it is
/// absent does CPython walk the `co_lines()` ranges the table holds.
///
/// Neither pointer is reachable through a public API, so this reads them at
/// byte offsets pinned per minor release (GIL builds; derived from the
/// release headers with `offsetof`). `verified` checks the layout once per
/// process against a live interpreter before any read is trusted; if it
/// fails, every lookup defers to `PyFrame_GetLineNumber`.
#[cfg(all(kolo_line_table, Py_3_13))]
pub(crate) mod co_monitoring {
    use pyo3::prelude::*;
    use pyo3::types::{PyCode, PyDict};
    use std::sync::atomic::{AtomicU8, Ordering};

    /// `offsetof(PyCodeObject, _co_monitoring)`.
    pub(super) const CO_MONITORING: usize = 176;
    /// `offsetof(_PyCoMonitoringData, lines)`; it follows two
    /// `_Py_LocalMonitors` (10 bytes on 3.13, 11 on 3.14, 16 on 3.15),
    /// `tools` and, from 3.14, `tool_versions[8]`.
    #[cfg(not(Py_3_14))]
    pub(super) const LINES: usize = 32;
    #[cfg(all(Py_3_14, not(Py_3_15)))]
    pub(super) const LINES: usize = 96;
    #[cfg(Py_3_15)]
    pub(super) const LINES: usize = 104;
    /// `types.CodeType.__basicsize__` (`offsetof(PyCodeObject,
    /// co_code_adaptive)`), a fingerprint of the layout before it.
    #[cfg(not(Py_3_14))]
    pub(super) const CODE_BASICSIZE: usize = 200;
    #[cfg(Py_3_14)]
    pub(super) const CODE_BASICSIZE: usize = 208;

    /// Offsets of the code-object fields the check compares with the
    /// objects Python exposes: `co_filename`, `co_name`, `co_qualname`,
    /// `co_linetable`, then `co_weakreflist`. In 3.13-3.15 they are
    /// followed by `co_executors`, `_co_cached`,
    /// `_co_instrumentation_version` and `_co_monitoring`.
    const CO_FILENAME: usize = 112;
    const CO_WEAKREFLIST: usize = 144;

    const UNCHECKED: u8 = 0;
    const CHECKING: u8 = 1;
    const VERIFIED: u8 = 2;
    const REJECTED: u8 = 3;
    /// Another tool had LINE events on everything when the check ran: the
    /// table stays off until the next monitor start checks again.
    const RETRY: u8 = 4;
    static STATE: AtomicU8 = AtomicU8::new(UNCHECKED);
    /// Undecided checks per process before the table stays off for good, so
    /// a process that keeps another tool's LINE events on (coverage, a
    /// tracer) and starts many monitors stops probing.
    const MAX_UNDECIDED: u8 = 8;
    static UNDECIDED: AtomicU8 = AtomicU8::new(0);

    /// What `verify` found.
    #[derive(Debug, PartialEq, Eq)]
    pub(crate) enum Layout {
        Verified,
        Rejected,
        /// CPython already answered the probe from LINE data before the
        /// check enabled LINE (another tool's global LINE events, e.g. a
        /// tracer or coverage), so nothing could be confirmed.
        Undecided,
    }

    /// Whether `code`'s lines come from the `co_lines()` ranges, as they do
    /// until LINE instrumentation data exists for it. `false` when the
    /// layout could not be verified.
    #[inline]
    pub(crate) fn answers_from_line_table(py: Python<'_>, code: &Py<PyCode>) -> bool {
        // Safety: the layout was verified for this interpreter; `code` is
        // alive and the GIL is held, so neither pointer changes under us.
        verified(py) && unsafe { line_data(code.as_ptr()).is_null() }
    }

    /// The layout check, run once per process. Called eagerly when a
    /// monitor is created so it normally never first runs inside an event
    /// callback. Never blocks: while the check runs (it calls into Python,
    /// so a callback or another thread can get here meanwhile), lookups
    /// answer `false` and defer to CPython. Fail closed: if the check
    /// cannot run (e.g. sys.monitoring refused a call), the table stays off.
    pub(crate) fn verified(py: Python<'_>) -> bool {
        match STATE.load(Ordering::Acquire) {
            VERIFIED => true,
            UNCHECKED => run_check(py, UNCHECKED),
            _ => false,
        }
    }

    /// `verified`, also re-running a check that was undecided because of
    /// another tool's LINE events. Called when a monitor starts.
    pub(crate) fn check_on_monitor_start(py: Python<'_>) -> bool {
        match STATE.load(Ordering::Acquire) {
            VERIFIED => true,
            state @ (UNCHECKED | RETRY) => run_check(py, state),
            _ => false,
        }
    }

    fn run_check(py: Python<'_>, from: u8) -> bool {
        if STATE
            .compare_exchange(from, CHECKING, Ordering::AcqRel, Ordering::Acquire)
            .is_err()
        {
            return STATE.load(Ordering::Acquire) == VERIFIED;
        }
        let layout = verify(py).unwrap_or(Layout::Rejected);
        STATE.store(
            match layout {
                Layout::Verified => VERIFIED,
                Layout::Rejected => REJECTED,
                Layout::Undecided
                    if UNDECIDED.fetch_add(1, Ordering::Relaxed) + 1 < MAX_UNDECIDED =>
                {
                    RETRY
                }
                Layout::Undecided => REJECTED,
            },
            Ordering::Release,
        );
        layout == Layout::Verified
    }

    /// `code` read as `count` pointer-sized fields from byte `offset`.
    ///
    /// Safety: `code` is a live code object at least `offset + 8 * count`
    /// bytes long (checked through `__basicsize__`).
    unsafe fn fields(code: *mut pyo3::ffi::PyObject, offset: usize, count: usize) -> Vec<usize> {
        (0..count)
            .map(|i| unsafe {
                code.cast::<u8>()
                    .add(offset + i * std::mem::size_of::<usize>())
                    .cast::<usize>()
                    .read()
            })
            .collect()
    }

    /// `code->_co_monitoring`.
    ///
    /// Safety: `code` is a live code object of this interpreter, whose
    /// layout matches the constants above.
    unsafe fn monitoring_data(code: *mut pyo3::ffi::PyObject) -> *const u8 {
        unsafe {
            code.cast::<u8>()
                .add(CO_MONITORING)
                .cast::<*const u8>()
                .read()
        }
    }

    /// `code->_co_monitoring->lines`, NULL while `_co_monitoring` is.
    ///
    /// Safety: as for `monitoring_data`.
    unsafe fn line_data(code: *mut pyo3::ffi::PyObject) -> *const u8 {
        unsafe {
            let data = monitoring_data(code);
            if data.is_null() {
                return data;
            }
            data.add(LINES).cast::<*const u8>().read()
        }
    }

    /// `code->_co_monitoring->local_monitors.tools[event]`.
    ///
    /// Safety: as for `monitoring_data`, with `_co_monitoring` non-NULL and
    /// `event` a local event (below 10).
    unsafe fn local_tools(code: *mut pyo3::ffi::PyObject, event: usize) -> u8 {
        unsafe { monitoring_data(code).add(event).read() }
    }

    /// Confirms the pinned offsets against this interpreter before any
    /// pointer is followed: the code type's size matches the release, the
    /// probe's `co_filename`/`co_name`/`co_qualname`/`co_linetable` sit at
    /// their offsets, `co_weakreflist` (the field 32 bytes before
    /// `_co_monitoring`) fills in when the probe is weakly referenced, and a
    /// never-run code object has no monitoring data. Only then is
    /// `_co_monitoring` followed: enabling local events on a spare `sys.monitoring` tool
    /// allocates it with the expected per-event tool bits, `lines` staying
    /// NULL for PY_START and appearing for LINE. The probe code object is
    /// private to this check, and the tool is released afterwards.
    pub(crate) fn verify(py: Python<'_>) -> PyResult<Layout> {
        let basicsize: usize = py
            .get_type::<PyCode>()
            .getattr("__basicsize__")?
            .extract()?;
        if basicsize != CODE_BASICSIZE {
            return Ok(Layout::Rejected);
        }
        let globals = PyDict::new(py);
        py.run(
            c"import sys, types
monitoring = sys.monitoring
probe = next(c for c in compile('def probe(a, b):\\n    x = (a +\\n         b)\\n    return x\\n', '<kolo line table check>', 'exec').co_consts if isinstance(c, types.CodeType))
probe = probe.replace(co_qualname='kolo.line_table_probe')
tool = next((t for t in (5, 4, 3, 2, 1, 0) if monitoring.get_tool(t) is None), None)
ambient_line = sys.gettrace() is not None or any(
    monitoring.get_events(t) & monitoring.events.LINE for t in range(6))
",
            Some(&globals),
            None,
        )?;
        let monitoring = globals.get_item("monitoring")?.expect("set above");
        let probe = globals.get_item("probe")?.expect("set above");
        let Some(tool) = globals
            .get_item("tool")?
            .expect("set above")
            .extract::<Option<u8>>()?
        else {
            // Every tool id is taken: nothing to probe with.
            return Ok(Layout::Rejected);
        };
        // Another tool's global LINE events (or `sys.settrace`) would give
        // the probe LINE data from the start: undecided, without taking a
        // tool id or bumping the monitoring version.
        if globals
            .get_item("ambient_line")?
            .expect("set above")
            .is_truthy()?
        {
            return Ok(Layout::Undecided);
        }
        let events = monitoring.getattr("events")?;
        let py_start: u32 = events.getattr("PY_START")?.extract()?;
        let line: u32 = events.getattr("LINE")?.extract()?;
        let index = |event: u32| event.trailing_zeros() as usize;
        let tool_bit = 1u8 << tool;
        let code = probe.as_ptr();
        // Safety (all reads): `probe` is alive for the whole check and at
        // least `CODE_BASICSIZE` bytes long; each read below happens only
        // after the previous one matched, and `_co_monitoring` is followed
        // only once the fields around it are confirmed and it is non-NULL.
        let identities = ["co_filename", "co_name", "co_qualname", "co_linetable"]
            .iter()
            .map(|name| Ok(probe.getattr(*name)?.as_ptr() as usize))
            .collect::<PyResult<Vec<_>>>()?;
        if unsafe { fields(code, CO_FILENAME, 4) } != identities
            || unsafe { fields(code, CO_WEAKREFLIST, 5) } != [0; 5]
        {
            return Ok(Layout::Rejected);
        }
        let weakref = py.import("weakref")?.call_method1("ref", (&probe,))?;
        let weakref_ok =
            unsafe { fields(code, CO_WEAKREFLIST, 5) } == [weakref.as_ptr() as usize, 0, 0, 0, 0];
        drop(weakref);
        if !weakref_ok || unsafe { fields(code, CO_WEAKREFLIST, 5) } != [0; 5] {
            return Ok(Layout::Rejected);
        }
        // CPython's own answers, which the gate must predict: the
        // `co_lines()` table until LINE data exists, then -1 at the
        // instructions that do not start a line.
        let table = super::CodeLines::new(probe.cast::<PyCode>()?)?;
        let table = table.lines(py)?.to_vec();
        let cpython_uses_table = || {
            table.iter().enumerate().all(|(unit, line)| {
                // Safety: a live code object and an in-range byte offset.
                let offset = (unit * super::CODE_UNIT) as std::ffi::c_int;
                unsafe { pyo3::ffi::PyCode_Addr2Line(code.cast(), offset) == *line }
            })
        };
        if !cpython_uses_table() {
            return Ok(Layout::Rejected);
        }
        // `_co_monitoring` must look like a heap pointer, and the field
        // before it like `_co_instrumentation_version` (a counter, here
        // below 1 MiB), before it is followed: a layout with the two swapped
        // fails one of these. A process that has changed global events
        // ~4096 times fails closed here.
        let plausible = || {
            const POINTER_FLOOR: usize = 1 << 20;
            let [executors, cached, version, candidate] =
                <[usize; 4]>::try_from(unsafe { fields(code, CO_WEAKREFLIST + 8, 4) })
                    .expect("four fields");
            candidate >= POINTER_FLOOR
                && candidate % std::mem::align_of::<usize>() == 0
                && version < POINTER_FLOOR
                && executors == 0
                && cached == 0
        };
        monitoring.call_method1("use_tool_id", (tool, "kolo line table check"))?;
        let checked = (|| -> PyResult<Layout> {
            monitoring.call_method1("set_local_events", (tool, &probe, py_start))?;
            // Independent of the offsets: CPython answering from LINE data
            // already means another tool's LINE events instrumented the
            // probe, which leaves nothing to tell `lines` apart by.
            if !cpython_uses_table() {
                return Ok(Layout::Undecided);
            }
            let start_ok = plausible()
                && unsafe {
                    line_data(code).is_null()
                        && local_tools(code, index(py_start)) == tool_bit
                        && local_tools(code, index(line)) == 0
                };
            if !start_ok {
                return Ok(Layout::Rejected);
            }
            monitoring.call_method1("set_local_events", (tool, &probe, line))?;
            let line_ok = plausible()
                && unsafe {
                    !line_data(code).is_null()
                        && local_tools(code, index(line)) == tool_bit
                        && local_tools(code, index(py_start)) == 0
                }
                && !cpython_uses_table();
            Ok(if line_ok {
                Layout::Verified
            } else {
                Layout::Rejected
            })
        })();
        // Release the tool id even if clearing its events fails.
        let cleared = monitoring.call_method1("set_local_events", (tool, &probe, 0));
        let freed = monitoring.call_method1("free_tool_id", (tool,));
        let checked = checked?;
        cleared?;
        freed?;
        Ok(checked)
    }
}

#[cfg(kolo_line_table)]
const CODE_UNIT: usize = 2;

/// `frame_line_number` through `lines` when they belong to the frame's code.
/// A frame with no line (CPython's -1) never comes from the table: it
/// always defers, so it stays `None` exactly as CPython reports it.
pub(super) fn frame_line_number_with(
    frame: &Bound<'_, PyFrame>,
    lines: Option<&CodeLines>,
) -> Result<Option<usize>, PyErr> {
    #[cfg(kolo_line_table)]
    if let Some(line) = lines
        .map(|lines| lines.frame_line(frame))
        .transpose()?
        .flatten()
    {
        return Ok(Some(line as usize));
    }
    #[cfg(not(kolo_line_table))]
    let _ = lines;
    frame_line_number(frame)
}

/// `frame_line_number` as an `i32`, through `lines` when they belong to the
/// frame's code.
pub(super) fn frame_line_number_i32_with(
    frame: &Bound<'_, PyFrame>,
    lines: Option<&CodeLines>,
) -> Result<Option<i32>, PyErr> {
    #[cfg(kolo_line_table)]
    if let Some(line) = lines
        .map(|lines| lines.frame_line(frame))
        .transpose()?
        .flatten()
    {
        return Ok(Some(line));
    }
    #[cfg(not(kolo_line_table))]
    let _ = lines;
    let lineno = unsafe { ffi::PyFrame_GetLineNumber(frame.as_ptr().cast()) };
    if lineno >= 0 {
        return Ok(Some(lineno));
    }

    frame
        .getattr(intern!(frame.py(), "f_lineno"))?
        .extract::<Option<i32>>()
}

/// The frame's current line, or `None` when it has no source line (CPython's
/// `f_lineno is None`, e.g. code with an empty line table).
pub(super) fn frame_line_number(frame: &Bound<'_, PyFrame>) -> Result<Option<usize>, PyErr> {
    let lineno = unsafe { ffi::PyFrame_GetLineNumber(frame.as_ptr().cast()) };
    if lineno >= 0 {
        return Ok(Some(lineno as usize));
    }

    // CPython returns -1 when a frame has no current source line. Defer to
    // `f_lineno`, which reports that as `None`.
    frame
        .getattr(intern!(frame.py(), "f_lineno"))?
        .extract::<Option<usize>>()
}

/// Format a frame path as `path:line`, or `path:None` when the line is
/// unknown, matching the pure-Python backends' `f"{path}:{frame.f_lineno}"`.
pub(super) fn format_path_with_line(relative_path: &str, lineno: Option<usize>) -> String {
    match lineno {
        Some(lineno) => format!("{relative_path}:{lineno}"),
        None => format!("{relative_path}:None"),
    }
}

/// Session-scoped cache for paths relative to the directory tracing started in.
///
/// The Python code object is held strongly alongside the pointer key.  This
/// prevents pointer reuse from returning metadata for a dead code object while
/// bounding the cache lifetime to the profiler/monitor session.
pub struct FramePathCache {
    pub(super) root: PathBuf,
    pub(super) paths: Mutex<HashMap<usize, (Py<PyAny>, String, bool)>>,
}

impl FramePathCache {
    pub fn new() -> Self {
        Self {
            root: current_dir().expect("Current directory is invalid"),
            paths: Mutex::new(HashMap::new()),
        }
    }

    pub(super) fn frame_path_and_native_eligibility(
        &self,
        frame: &Bound<'_, PyFrame>,
    ) -> Result<(String, usize, bool), PyErr> {
        let py = frame.py();
        let code = frame.getattr(intern!(py, "f_code"))?;
        let code_id = code.as_ptr() as usize;
        let (relative_path, native_eligible) = {
            let mut paths = self
                .paths
                .lock_py_attached(py)
                .expect("frame path cache mutex poisoned");
            match paths.get(&code_id) {
                Some((_, relative_path, native_eligible)) => {
                    (relative_path.clone(), *native_eligible)
                }
                None => {
                    let filename = code
                        .getattr(intern!(py, "co_filename"))?
                        .extract::<String>()?;
                    let relative_path = self.relative_path(&filename);
                    paths.insert(code_id, (code.unbind(), relative_path.clone(), true));
                    (relative_path, true)
                }
            }
        };
        let lineno = frame_line_number(frame)?;
        Ok((
            format_path_with_line(&relative_path, lineno),
            code_id,
            native_eligible,
        ))
    }

    pub fn format_frame_path(&self, frame: &Bound<'_, PyFrame>) -> Result<String, PyErr> {
        Ok(self.frame_path_and_native_eligibility(frame)?.0)
    }

    pub(super) fn mark_native_msgpack_unsupported(&self, py: Python, code_id: usize) {
        if let Some((_, _, native_eligible)) = self
            .paths
            .lock_py_attached(py)
            .expect("frame path cache mutex poisoned")
            .get_mut(&code_id)
        {
            *native_eligible = false;
        }
    }

    /// Format a filename relative to the directory in which tracing started.
    ///
    /// This is kept separate from `format_frame_path` so callers which already
    /// cache immutable code-object metadata do not need to recover `f_code` or
    /// lock the path cache on every event.
    pub fn relative_path(&self, filename: &str) -> String {
        let path = lexical_normalize(Path::new(filename));
        if path.is_absolute() {
            lexical_relative_path(&path, &self.root)
                .unwrap_or(path)
                .display()
                .to_string()
        } else {
            path.display().to_string()
        }
    }
}

/// Normalize `.` and `..` components without touching the filesystem.
///
/// Code filenames do not have to exist, so canonicalization is not an option.
/// This mirrors the lexical behavior Kolo's Python backends get from
/// `os.path.normpath` while keeping Python execution out of monitoring hooks.
pub(super) fn lexical_normalize(path: &Path) -> PathBuf {
    let mut normalized = PathBuf::new();
    let mut rooted = false;

    for component in path.components() {
        match component {
            Component::Prefix(prefix) => normalized.push(prefix.as_os_str()),
            Component::RootDir => {
                normalized.push(Path::new(std::path::MAIN_SEPARATOR_STR));
                rooted = true;
            }
            Component::CurDir => {}
            Component::ParentDir => {
                let can_pop = normalized
                    .file_name()
                    .is_some_and(|name| name != std::ffi::OsStr::new(".."));
                if can_pop {
                    normalized.pop();
                } else if !rooted {
                    normalized.push("..");
                }
            }
            Component::Normal(part) => normalized.push(part),
        }
    }

    if normalized.as_os_str().is_empty() {
        normalized.push(".");
    }
    normalized
}

pub(super) fn path_component_eq(left: Component<'_>, right: Component<'_>) -> bool {
    #[cfg(windows)]
    {
        left.as_os_str()
            .to_string_lossy()
            .eq_ignore_ascii_case(&right.as_os_str().to_string_lossy())
    }
    #[cfg(not(windows))]
    {
        left == right
    }
}

/// Return `path` relative to `root`, or `None` when Windows prefixes differ.
pub(super) fn lexical_relative_path(path: &Path, root: &Path) -> Option<PathBuf> {
    let normalized_root = lexical_normalize(root);
    let path_components: Vec<_> = path.components().collect();
    let root_components: Vec<_> = normalized_root.components().collect();

    if matches!(path_components.first(), Some(Component::Prefix(_)))
        && !matches!(root_components.first(), Some(Component::Prefix(_)))
        || matches!(root_components.first(), Some(Component::Prefix(_)))
            && !matches!(path_components.first(), Some(Component::Prefix(_)))
    {
        return None;
    }
    if let (Some(Component::Prefix(path_prefix)), Some(Component::Prefix(root_prefix))) =
        (path_components.first(), root_components.first())
    {
        if !path_component_eq(
            Component::Prefix(*path_prefix),
            Component::Prefix(*root_prefix),
        ) {
            return None;
        }
    }

    let common = path_components
        .iter()
        .zip(&root_components)
        .take_while(|(left, right)| path_component_eq(**left, **right))
        .count();
    let mut relative = PathBuf::new();
    for component in &root_components[common..] {
        if matches!(component, Component::Normal(_)) {
            relative.push("..");
        }
    }
    for component in &path_components[common..] {
        relative.push(component.as_os_str());
    }
    if relative.as_os_str().is_empty() {
        relative.push(".");
    }
    Some(relative)
}
