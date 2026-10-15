//! Cross-event repr reuse: guard, reuse, deopt.
//!
//! Most of the capture time of template engines and renderers goes into
//! re-running the same expensive `__repr__` on the same, unchanged object in
//! event after event (a Jinja `Context` with its whole render context, a
//! markdown-it `Token`, a Rich `Style`). This module reuses the text of an
//! earlier `repr()` of an object only when it can *prove* the repr would
//! produce byte-identical text again, and otherwise runs the real repr.
//!
//! The proof has three parts.
//!
//! 1. **Certification.** The repr implementation must be fully understood:
//!    exact builtin containers and scalars whose C reprs are pure functions
//!    of their contents, `type`/function/builtin-function/bound-method
//!    reprs, default `object.__repr__`, and Python `__repr__` functions whose
//!    *bytecode* (not name) is identical to an audited reference
//!    implementation or is a straight-line f-string over attributes of
//!    `self` (`kolo/_repr_audit.py`). Each certified implementation has a
//!    native *plan* below that walks exactly what that code reads.
//! 2. **Guards.** Running a plan (recording) emits one guard for every
//!    mutable location the certified code reads: the type pointer of every
//!    heap-type instance (`__class__` assignment), slot values, instance
//!    attributes (re-read through C `PyObject_GenericGetAttr`), the one
//!    entry a name lookup reads (globals, builtins, a type's `__module__`),
//!    the contents of every dict repr'd (3.12/3.13: `ma_version_tag`, a new
//!    interpreter-wide unique version on every mutation; 3.14+, which
//!    removed it: the items; split-table dicts by their items everywhere),
//!    the length, storage and items of
//!    every list, set contents,
//!    a function's `__code__`/globals/builtins/closure/`__qualname__`/
//!    `__dict__`, cell contents, property getters, and the `tp_version_tag`
//!    of every heap type whose attributes are resolved (CPython assigns a
//!    fresh, never-reused tag whenever a type or any base is modified, which
//!    is what its own attribute caches rely on; it also changes on
//!    `__name__`/`__qualname__`/`__module__`/`__bases__` assignment).
//!    Everything else the plan reads is immutable (str/int/float/tuple
//!    contents, a bound method's function and self) or fixed by one of
//!    those guards (descriptors found through a guarded type).
//!
//!    Entries hold **no references** to the program's objects: keeping them
//!    alive would change when the program's objects are freed (finalizers,
//!    weakref callbacks) and which addresses get reused. Validation starts
//!    from the live root, and each guard reads only objects that earlier
//!    guards reached from it (a value held by a live object is live). An
//!    object found at a recorded address may still be a different one (the
//!    old one freed, a new one allocated there), so the type of every object
//!    whose layout the plan reads and the contents of every immutable value
//!    it reads (str, int, float, bytes, tuple items) are guarded too, unless
//!    the object is immortal or provably the same one: held by a dict or
//!    type whose unique, never-reused version is guarded unchanged. Code
//!    objects are matched to their verdicts through weak references.
//! 3. **Validation.** Before reusing, the guards are evaluated in order
//!    against live memory; no plan logic runs and no Python code can run
//!    (plain loads, plus generic attribute reads that the preceding guards
//!    prove reach no Python). If every guard holds, every read the plan made
//!    returns the same value, so the plan would take the same path through
//!    the same objects in the same state; because the certified code is a
//!    deterministic function of exactly those reads, its output is the
//!    cached text. Any failing guard deopts to the real repr, which then
//!    re-records.
//!
//! Context the plans cannot see is checked at the root: the thread's
//! `Py_ReprEnter` list must be empty (otherwise a container being repr'd up
//! the stack would print as `[...]`), recursion-repr guards of the
//! dataclass/`reprlib` wrappers must be idle, and both recursion budgets
//! must have room for the whole repr graph (so the real repr could not have
//! raised `RecursionError` here).
//!
//! Guards are recorded before the real repr runs and checked again right
//! after it. A dependency changed and restored while it ran (by another
//! thread, a signal handler or a finalizer) would leave text that no guard
//! contradicts, so an entry is reused only after a second real repr, run
//! while its guards held, returned the same text (`Entry::confirmed`).
//! Pending signal handlers run before a reuse, as before a real repr (the
//! encoder checks for them before it asks for any repr).
//!
//! Accepted caveats are those of eager capture itself: non-deterministic
//! reprs (none are certified), GC/finalizer timing and thread switches that
//! a real repr could have hit while executing Python, and audit hooks:
//! the dataclass/`reprlib` wrappers call `id()`, whose `builtins.id` audit
//! event does not fire on a reuse (a hook that changes the object being
//! repr'd would make the reuse stale).
//! Code that writes object memory directly (ctypes), or mutates a class's
//! namespace behind `type.__setattr__` (through `gc.get_referents` of its
//! mappingproxy, which also leaves CPython's own attribute caches stale), is
//! out of scope.
//!
//! Only CPython 3.12 to 3.15 with the GIL are supported: the module reads a
//! few documented-but-internal layouts (managed dict pointer, dict key kind,
//! `ma_version_tag`, thread state recursion counters, which move between
//! releases) and checks them at startup, disabling itself if any check
//! fails. Free-threaded builds always run the real repr: validation relies
//! on nothing else running while it reads guarded memory.

use pyo3::prelude::*;
use pyo3::types::PyString;

pub use imp::{configure, preload, stats, ReprReuse};

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED), not(PyPy)))]
mod imp {
    use super::*;
    use hashbrown::{HashMap, HashSet};
    use pyo3::types::PyDict;
    use pyo3::ffi;
    use std::cell::RefCell;
    use std::os::raw::{c_int, c_void};
    use std::ptr;
    use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
    use std::sync::{Arc, Mutex, OnceLock};
    use std::time::Instant;
    use thread_local::ThreadLocal;

    type P = *mut ffi::PyObject;
    type T = *mut ffi::PyTypeObject;

    /// An interned str for a name the plans read, like pyo3's `intern!` but
    /// created without ever detaching from the interpreter: `intern!`'s
    /// first use may release the GIL, and recording and validation rely on
    /// nothing else running (GIL builds only).
    macro_rules! name {
        ($py:expr, $text:literal) => {{
            static CELL: std::sync::atomic::AtomicPtr<Py<PyString>> =
                std::sync::atomic::AtomicPtr::new(std::ptr::null_mut());
            interned_name($py, &CELL, concat!($text, "\0"))
        }};
    }

    fn interned_name<'py>(
        py: Python<'py>,
        cell: &'static std::sync::atomic::AtomicPtr<Py<PyString>>,
        text: &'static str,
    ) -> &'py Bound<'py, PyString> {
        let mut name = cell.load(Ordering::Acquire);
        if name.is_null() {
            // Safety: `text` is NUL-terminated; plain C API call that runs no
            // Python and does not release the GIL.
            let object = unsafe { ffi::PyUnicode_InternFromString(text.as_ptr().cast()) };
            assert!(!object.is_null(), "out of memory interning a name");
            // Safety: a new reference to a str; leaked for the process.
            let created = Box::into_raw(Box::new(unsafe {
                Bound::from_owned_ptr(py, object)
                    .cast_into_unchecked::<PyString>()
                    .unbind()
            }));
            name = match cell.compare_exchange(
                ptr::null_mut(),
                created,
                Ordering::AcqRel,
                Ordering::Acquire,
            ) {
                Ok(_) => created,
                Err(existing) => {
                    // Safety: `created` was never shared.
                    drop(unsafe { Box::from_raw(created) });
                    existing
                }
            };
        }
        // Safety: published once and never freed.
        unsafe { (*name).bind(py) }
    }

    extern "C" {
        fn _PyType_Lookup(type_: T, name: P) -> P;
        fn PyUnstable_Type_AssignVersionTag(type_: T) -> c_int;
        fn _PyObject_GetDictPtr(obj: P) -> *mut P;
        fn PyGC_Disable() -> c_int;
        fn PyGC_Enable() -> c_int;
        fn _PySet_NextEntry(
            set: P,
            position: *mut ffi::Py_ssize_t,
            key: *mut P,
            hash: *mut ffi::Py_hash_t,
        ) -> c_int;
    }

    // `size_t` until 3.13, `int64_t` since 3.14.
    #[cfg(not(Py_3_14))]
    extern "C" {
        fn _PyLong_NumBits(value: P) -> usize;
    }

    #[cfg(Py_3_14)]
    extern "C" {
        fn _PyLong_NumBits(value: P) -> i64;
    }

    /// Whether the exact int `value` has at most `bits` significant bits.
    unsafe fn long_bits_at_most(value: P, bits: u64) -> bool {
        let count = _PyLong_NumBits(value);
        if !ffi::PyErr_Occurred().is_null() {
            ffi::PyErr_Clear();
            return false;
        }
        u64::try_from(count).is_ok_and(|count| count <= bits)
    }

    // The bound method and cell types, taken from live objects at startup:
    // pyo3-ffi does not declare them, and data symbols need DLL import
    // linkage on Windows.
    static METHOD_TYPE: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);
    static CELL_TYPE: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);

    fn method_type() -> T {
        METHOD_TYPE.load(Ordering::Relaxed) as T
    }

    fn cell_type() -> T {
        CELL_TYPE.load(Ordering::Relaxed) as T
    }

    /// Automatic garbage collection is off while it lives. Recording and
    /// validation allocate a little (bound methods for shadowing checks), and
    /// an allocation may otherwise start a collection whose callbacks and
    /// finalizers run Python in the middle of a walk.
    struct NoGc(c_int);

    impl NoGc {
        unsafe fn new() -> Self {
            NoGc(PyGC_Disable())
        }
    }

    impl Drop for NoGc {
        fn drop(&mut self) {
            if self.0 != 0 {
                // Safety: the GIL is held for the guard's whole lifetime.
                unsafe { PyGC_Enable() };
            }
        }
    }

    /// `PyMethodObject` (Include/cpython/classobject.h).
    #[repr(C)]
    struct MethodObject {
        ob_base: ffi::PyObject,
        im_func: P,
        im_self: P,
    }

    static ENABLED: AtomicBool = AtomicBool::new(true);
    static VERIFY: AtomicBool = AtomicBool::new(false);
    static STATS: AtomicBool = AtomicBool::new(false);
    static CONFIG_READ: std::sync::Once = std::sync::Once::new();

    fn read_config() {
        CONFIG_READ.call_once(|| {
            let flag = |name: &str| std::env::var(name).ok();
            if flag("KOLO_REPR_REUSE").as_deref() == Some("0") {
                ENABLED.store(false, Ordering::Relaxed);
            }
            if flag("KOLO_REPR_REUSE_VERIFY").is_some_and(|v| v != "0" && !v.is_empty()) {
                VERIFY.store(true, Ordering::Relaxed);
            }
            if flag("KOLO_REPR_REUSE_STATS").is_some_and(|v| v != "0" && !v.is_empty()) {
                STATS.store(true, Ordering::Relaxed);
            }
        });
    }

    /// Import `kolo._repr_audit` while `kolo._kolo` itself is imported,
    /// before any trace starts: importing it lazily (when the first monitor
    /// probes the interpreter) added a module to `sys.modules` in the middle
    /// of the program, which code that snapshots `sys.modules` can see.
    /// Failures are left to the probe, which then disables reuse.
    pub fn preload(py: Python<'_>) -> PyResult<()> {
        read_config();
        if ENABLED.load(Ordering::Relaxed) {
            init_canon(py)?;
        }
        Ok(())
    }

    /// `kolo._repr_audit`, executed into a module object Kolo keeps to
    /// itself (in `Canon`): it is never entered in `sys.modules`, where a
    /// program that snapshots the loaded modules (Flask's test fixtures do)
    /// would see a module that Kolo without repr reuse does not load.
    fn load_audit_module(py: Python<'_>) -> PyResult<Py<PyModule>> {
        let package_file: String = PyModule::import(py, "kolo")?.getattr("__file__")?.extract()?;
        let path = std::path::Path::new(&package_file).with_file_name("_repr_audit.py");
        let path_text = path.to_string_lossy().into_owned();
        let source = std::fs::read_to_string(&path)
            .map_err(|error| pyo3::exceptions::PyOSError::new_err(error.to_string()))?;
        let to_c = |text: String| {
            std::ffi::CString::new(text)
                .map_err(|error| pyo3::exceptions::PyValueError::new_err(error.to_string()))
        };
        let source = to_c(source)?;
        let file = to_c(path_text.clone())?;
        let module = PyModule::new(py, "kolo._repr_audit")?;
        module.setattr("__file__", &path_text)?;
        module.setattr("__package__", "kolo")?;
        module.setattr("__builtins__", PyModule::import(py, "builtins")?)?;
        // Safety: plain C API calls on owned objects; the module's real file
        // name keeps its frames recognizable as Kolo's own.
        unsafe {
            let code = ffi::Py_CompileString(source.as_ptr(), file.as_ptr(), ffi::Py_file_input);
            if code.is_null() {
                return Err(PyErr::fetch(py));
            }
            let code = Bound::from_owned_ptr(py, code);
            let globals = module.dict();
            let result = ffi::PyEval_EvalCode(code.as_ptr(), globals.as_ptr(), globals.as_ptr());
            if result.is_null() {
                return Err(PyErr::fetch(py));
            }
            ffi::Py_DECREF(result);
        }
        Ok(module.unbind())
    }

    /// Override the environment configuration (tests and A/B runs).
    pub fn configure(enabled: Option<bool>, verify: Option<bool>, stats: Option<bool>) {
        read_config();
        if let Some(enabled) = enabled {
            ENABLED.store(enabled, Ordering::Relaxed);
        }
        if let Some(verify) = verify {
            VERIFY.store(verify, Ordering::Relaxed);
        }
        if let Some(stats) = stats {
            STATS.store(stats, Ordering::Relaxed);
        }
    }

    macro_rules! counters {
        ($($name:ident),* $(,)?) => {
            #[derive(Default)]
            struct Counters { $($name: AtomicU64,)* }
            impl Counters {
                fn snapshot(&self, dict: &Bound<'_, PyDict>) -> PyResult<()> {
                    $(dict.set_item(stringify!($name), self.$name.load(Ordering::Relaxed))?;)*
                    Ok(())
                }
                fn reset(&self) { $(self.$name.store(0, Ordering::Relaxed);)* }
            }
        };
    }

    counters!(
        verify_repr_ns,
        python_reprs,
        hits,
        deopts,
        misses,
        uncertifiable,
        pending_audits,
        negative_skips,
        cheap_skips,
        confirmations,
        changed_during_repr,
        oversized,
        inserted,
        evicted,
        context_refusals,
        verify_checks,
        verify_mismatches,
        hit_validate_ns,
        deopt_validate_ns,
        record_ns,
        miss_repr_ns,
        avoided_ns,
        uncert_repr_ns,
        snapshot_dicts,
    );

    static COUNTERS: OnceLock<Counters> = OnceLock::new();
    static REASONS: Mutex<Option<std::collections::HashMap<String, u64>>> = Mutex::new(None);
    static MISMATCHES: Mutex<Vec<String>> = Mutex::new(Vec::new());

    /// Per type: (count, ns) for each outcome, then the fill cost of hits.
    const PER_TYPE_OUTCOMES: usize = 5;
    const PER_TYPE_COLUMNS: usize = 2 * PER_TYPE_OUTCOMES + 1;
    static PER_TYPE: Mutex<Option<std::collections::HashMap<String, [u64; PER_TYPE_COLUMNS]>>> =
        Mutex::new(None);

    enum Outcome {
        NotPython,
        Hit(u64),
        Deopt,
        Miss,
        Skip,
    }

    impl Outcome {
        fn column(&self) -> usize {
            match self {
                Outcome::Hit(_) => 0,
                Outcome::Deopt => 1,
                Outcome::Miss => 2,
                Outcome::Skip => 3,
                Outcome::NotPython => 4,
            }
        }
    }

    fn counters() -> &'static Counters {
        COUNTERS.get_or_init(Counters::default)
    }

    fn bump(counter: &AtomicU64, by: u64) {
        counter.fetch_add(by, Ordering::Relaxed);
    }

    /// Statistics as a dict; `reset` clears them afterwards.
    pub fn stats(py: Python<'_>, reset: bool) -> PyResult<Bound<'_, PyDict>> {
        let dict = PyDict::new(py);
        counters().snapshot(&dict)?;
        dict.set_item(
            "enabled",
            ENABLED.load(Ordering::Relaxed) && canon(py).is_some(),
        )?;
        dict.set_item("verify", VERIFY.load(Ordering::Relaxed))?;
        // Copied out first: building Python objects can run a GC callback,
        // which could ask for statistics again while a lock is held.
        let reasons_copy = REASONS.lock().expect("poisoned").clone();
        let mismatches = MISMATCHES.lock().expect("poisoned").clone();
        let per_type_copy = PER_TYPE.lock().expect("poisoned").clone();
        let reasons = PyDict::new(py);
        for (reason, count) in reasons_copy.iter().flatten() {
            reasons.set_item(reason, count)?;
        }
        dict.set_item("uncertifiable_reasons", reasons)?;
        dict.set_item("mismatch_examples", mismatches)?;
        let per_type = PyDict::new(py);
        for (name, row) in per_type_copy.iter().flatten() {
            per_type.set_item(name, row.to_vec())?;
        }
        dict.set_item("per_type", per_type)?;
        if reset {
            *PER_TYPE.lock().expect("poisoned") = None;
            counters().reset();
            *REASONS.lock().expect("poisoned") = None;
            MISMATCHES.lock().expect("poisoned").clear();
        }
        Ok(dict)
    }

    fn note_reason(py: Python<'_>, value: P, reason: &str) {
        // Safety: reads a live object's static type name.
        let name = unsafe {
            std::ffi::CStr::from_ptr((*ffi::Py_TYPE(value)).tp_name)
                .to_string_lossy()
                .into_owned()
        };
        let _ = py;
        let mut guard = REASONS.lock().expect("poisoned");
        *guard
            .get_or_insert_with(Default::default)
            .entry(format!("{name}: {reason}"))
            .or_insert(0) += 1;
    }

    /// `PyDictObject`. `watcher_tag` is `ma_version_tag` before 3.14 (and
    /// `_ma_watcher_tag`, unused here, since).
    #[repr(C)]
    struct DictObject {
        ob_refcnt: isize,
        ob_type: *mut c_void,
        ma_used: isize,
        watcher_tag: u64,
        ma_keys: *mut DictKeys,
        ma_values: *mut c_void,
    }

    /// The CPython minor version whose private layouts this build reads.
    #[cfg(not(Py_3_13))]
    const LAYOUT_MINOR: u8 = 12;
    #[cfg(all(Py_3_13, not(Py_3_14)))]
    const LAYOUT_MINOR: u8 = 13;
    #[cfg(all(Py_3_14, not(Py_3_15)))]
    const LAYOUT_MINOR: u8 = 14;
    #[cfg(Py_3_15)]
    const LAYOUT_MINOR: u8 = 15;

    #[repr(C)]
    struct DictKeys {
        dk_refcnt: isize,
        dk_log2_size: u8,
        dk_log2_index_bytes: u8,
        dk_kind: u8,
    }

    const DICT_KEYS_GENERAL: u8 = 0;

    #[cfg(not(Py_3_13))]
    #[repr(C)]
    struct ThreadStatePrefix {
        prev: *mut c_void,
        next: *mut c_void,
        interp: *mut c_void,
        status: u32,
        py_recursion_remaining: c_int,
        py_recursion_limit: c_int,
        c_recursion_remaining: c_int,
    }

    #[cfg(all(Py_3_13, not(Py_3_14)))]
    #[repr(C)]
    struct ThreadStatePrefix {
        prev: *mut c_void,
        next: *mut c_void,
        interp: *mut c_void,
        eval_breaker: usize,
        status: u32,
        whence: c_int,
        state: c_int,
        py_recursion_remaining: c_int,
        py_recursion_limit: c_int,
        c_recursion_remaining: c_int,
    }

    /// 3.14 dropped the C recursion counter (C recursion is measured on the
    /// machine stack) and added `holds_gil`.
    #[cfg(all(Py_3_14, not(Py_3_15)))]
    #[repr(C)]
    struct ThreadStatePrefix {
        prev: *mut c_void,
        next: *mut c_void,
        interp: *mut c_void,
        eval_breaker: usize,
        status: u32,
        holds_gil: c_int,
        whence: c_int,
        state: c_int,
        py_recursion_remaining: c_int,
        py_recursion_limit: c_int,
        recursion_headroom: c_int,
    }

    /// 3.15 inserted `gil_requested` after `holds_gil`.
    #[cfg(Py_3_15)]
    #[repr(C)]
    struct ThreadStatePrefix {
        prev: *mut c_void,
        next: *mut c_void,
        interp: *mut c_void,
        eval_breaker: usize,
        status: u32,
        holds_gil: c_int,
        gil_requested: c_int,
        whence: c_int,
        state: c_int,
        py_recursion_remaining: c_int,
        py_recursion_limit: c_int,
        recursion_headroom: c_int,
    }

    #[cfg(not(Py_3_14))]
    extern "C" {
        fn Py_EnterRecursiveCall(location: *const std::ffi::c_char) -> c_int;
        fn Py_LeaveRecursiveCall();
    }

    #[cfg(Py_3_14)]
    extern "C" {
        fn _Py_ReachedRecursionLimitWithMargin(
            tstate: *mut ffi::PyThreadState,
            margin_count: c_int,
        ) -> c_int;
    }

    /// The smallest stack margin unit of a build for this pointer size
    /// (release builds; debug and sanitizer builds use twice as much).
    #[cfg(Py_3_14)]
    const STACK_MARGIN_UNIT_BYTES: i64 = 2048 * std::mem::size_of::<usize>() as i64;
    /// C stack budgeted per counted recursion level on 3.14+ (where 3.12
    /// and 3.13 counted levels).
    #[cfg(Py_3_14)]
    const STACK_BYTES_PER_LEVEL: i64 = 4096;

    #[repr(C)]
    struct CellObject {
        ob_base: ffi::PyObject,
        ob_ref: P,
    }

    #[repr(C)]
    struct MemberDescr {
        d_common: ffi::PyDescrObject,
        d_member: *mut ffi::PyMemberDef,
    }

    #[repr(C)]
    struct TupleGetter {
        ob_base: ffi::PyObject,
        index: ffi::Py_ssize_t,
    }

    const T_OBJECT: c_int = 6;
    const T_OBJECT_EX: c_int = 16;
    const READ_RESTRICTED: c_int = 2;
    /// `Py_RELATIVE_OFFSET` (3.12+): the offset is into the type's own data
    /// area, not the object.
    const RELATIVE_OFFSET: c_int = 8;

    /// Objects and C function pointers the plans compare against, captured
    /// once from the running interpreter.
    struct Canon {
        slot_tp_repr: usize,
        // `PyObject_GenericGetAttr` as installed in `object`'s slot: on
        // Windows, the address of the imported symbol is a thunk instead.
        generic_getattro: usize,
        slot_tp_descr_get: usize,
        object_repr: usize,
        type_repr: usize,
        object_class: usize,
        c_richcompare: [usize; 7],
        builtin_id: usize,
        /// `sys.is_stack_trampoline_active` (the canonical builtin; 0 when
        /// missing): see `eval_frame_ok`.
        trampoline_active: usize,
        /// The `vectorcall` of a plain Python function: one with another
        /// (`PyFunction_SetVectorcall`) need not run its bytecode.
        function_vectorcall: usize,
        /// A C function that does nothing, the callback of Kolo's weak
        /// references to code objects (see `Rec::verdict`).
        weak_callback: usize,
        builtin_len: usize,
        builtin_repr: usize,
        builtin_isinstance: usize,
        builtin_getattr: usize,
        thread_module: usize,
        get_ident: usize,
        tuplegetter_type: usize,
        property_fget_offset: isize,
        classify: Py<PyAny>,
        _keep: Vec<Py<PyAny>>,
    }

    // Safety: only pointers to immortal/static objects and owned references.
    unsafe impl Send for Canon {}
    unsafe impl Sync for Canon {}

    /// `PyOnceLock`: another thread waiting for the probe (which runs
    /// Python, and so may release the GIL) waits detached.
    static CANON: pyo3::sync::PyOnceLock<Option<Canon>> = pyo3::sync::PyOnceLock::new();

    /// The canonical objects, set up once while `kolo._kolo` is imported
    /// (`preload`). Never initialized later: a first use in the middle of a
    /// program would run Python (the probe) wherever a repr happens to be
    /// needed, and could be cut off by a fork.
    fn canon(py: Python<'_>) -> Option<&'static Canon> {
        CANON.get(py).and_then(Option::as_ref)
    }

    /// Errors turn reuse off, except for `BaseException`s such as
    /// `KeyboardInterrupt`, which reach the program (reuse then stays off).
    fn init_canon(py: Python<'_>) -> PyResult<()> {
        let mut interrupt = None;
        CANON.get_or_init(py, || match Canon::new(py) {
            Ok(canon) => canon,
            Err(error) => {
                if !error.is_instance_of::<pyo3::exceptions::PyException>(py) {
                    interrupt = Some(error);
                }
                None
            }
        });
        interrupt.map_or(Ok(()), Err)
    }

    extern "C" {
        fn _PyEval_EvalFrameDefault();
    }

    /// Whether `evaluator` is CPython's own frame evaluator.
    #[cfg(not(windows))]
    fn is_default_eval_frame(evaluator: usize) -> bool {
        evaluator == _PyEval_EvalFrameDefault as usize
    }

    /// Whether `evaluator` is CPython's own frame evaluator. The address of
    /// an imported function is a thunk on Windows: ask the DLL that
    /// contains `evaluator` for its `_PyEval_EvalFrameDefault` export.
    #[cfg(windows)]
    fn is_default_eval_frame(evaluator: usize) -> bool {
        type Module = *mut c_void;
        const FROM_ADDRESS: u32 = 0x4;
        const UNCHANGED_REFCOUNT: u32 = 0x2;
        #[link(name = "kernel32")]
        extern "system" {
            fn GetModuleHandleExW(flags: u32, name: *const c_void, module: *mut Module) -> i32;
            fn GetProcAddress(module: Module, name: *const std::ffi::c_char) -> *const c_void;
        }
        let _ = _PyEval_EvalFrameDefault as usize;
        let mut module: Module = ptr::null_mut();
        // Safety: plain Win32 queries; the module is not reference counted.
        unsafe {
            GetModuleHandleExW(
                FROM_ADDRESS | UNCHANGED_REFCOUNT,
                evaluator as *const c_void,
                &mut module,
            ) != 0
                && !module.is_null()
                && GetProcAddress(module, c"_PyEval_EvalFrameDefault".as_ptr()) as usize == evaluator
        }
    }

    /// The interpreter's PEP 523 frame evaluator.
    fn current_eval_frame() -> usize {
        // Safety: plain query of the current interpreter.
        unsafe { ffi::_PyInterpreterState_GetEvalFrameFunc(ffi::PyInterpreterState_Get()) as usize }
    }

    /// Whether `evaluator` lives in the binary that holds CPython itself.
    #[cfg(not(windows))]
    fn in_cpython_binary(evaluator: usize) -> bool {
        #[repr(C)]
        struct DlInfo {
            fname: *const std::ffi::c_char,
            fbase: *mut c_void,
            sname: *const std::ffi::c_char,
            saddr: *mut c_void,
        }
        extern "C" {
            fn dladdr(address: *const c_void, info: *mut DlInfo) -> c_int;
        }
        let base = |address: usize| {
            let mut info = DlInfo {
                fname: ptr::null(),
                fbase: ptr::null_mut(),
                sname: ptr::null(),
                saddr: ptr::null_mut(),
            };
            // Safety: plain lookup of a code address.
            let found = unsafe { dladdr(address as *const c_void, &mut info) } != 0;
            found.then_some(info.fbase as usize)
        };
        // A function pointer CPython stored itself (a real address, unlike a
        // reference to an imported function).
        // Safety: reads a static type's slot.
        let cpython = unsafe { (*ptr::addr_of_mut!(ffi::PyType_Type)).tp_repr }
            .map_or(0, |f| f as usize);
        cpython != 0 && base(evaluator).is_some_and(|b| Some(b) == base(cpython))
    }

    #[cfg(windows)]
    fn in_cpython_binary(_evaluator: usize) -> bool {
        false
    }

    /// The last evaluator found to run Python code as CPython does.
    static TRUSTED_EVAL_FRAME: std::sync::atomic::AtomicUsize =
        std::sync::atomic::AtomicUsize::new(0);

    /// Whether the installed frame evaluator runs Python code as CPython
    /// does: its own, or (3.12 to 3.14) its perf trampoline (`-X perf`,
    /// used by profilers such as CodSpeed), which calls it unchanged. Since
    /// 3.15 the trampoline wraps whatever evaluator was installed before,
    /// which cannot be checked, so there only CPython's own is trusted. Any
    /// other PEP 523 evaluator can change what Python code returns: reuse
    /// is off then.
    fn eval_frame_ok(py: Python<'_>, canon: &Canon) -> bool {
        let current = current_eval_frame();
        if current == TRUSTED_EVAL_FRAME.load(Ordering::Relaxed) {
            return true;
        }
        let _ = py;
        trusted_eval_frame(current, canon.trampoline_active)
    }

    /// See `eval_frame_ok`; `trampoline_active` is the canonical
    /// `sys.is_stack_trampoline_active` (0 when missing).
    fn trusted_eval_frame(current: usize, trampoline_active: usize) -> bool {
        let trusted = is_default_eval_frame(current)
            || (cfg!(not(Py_3_15))
                && trampoline_active != 0
                && in_cpython_binary(current)
                && {
                // Safety: the canonical builtin, called with no arguments
                // (C only); a failure counts as "not active".
                let result = unsafe { ffi::PyObject_CallNoArgs(trampoline_active as P) };
                if result.is_null() {
                    unsafe { ffi::PyErr_Clear() };
                    false
                } else {
                    let active = result == unsafe { ffi::Py_True() };
                    unsafe { ffi::Py_DECREF(result) };
                    active
                }
            });
        if trusted {
            TRUSTED_EVAL_FRAME.store(current, Ordering::Relaxed);
        }
        trusted
    }

    /// The callback of Kolo's weak references to code objects.
    unsafe extern "C" fn weak_callback(_module: P, _weakref: P) -> P {
        let none = ffi::Py_None();
        ffi::Py_INCREF(none);
        none
    }

    /// Run with empty builtins: nothing in it can be redirected by
    /// monkeypatching (classes are created by calling `type` directly).
    const PROBE: &std::ffi::CStr = c"
def repr_(self):
    return ''
def get_(self, obj, objtype=None):
    return None
def getter(self):
    return 1
def closure():
    captured = 1
    def inner():
        return captured
    return inner
";

    /// Whether `object` is an instance of a static (non-heap) type named
    /// `name` whose instances are at least `size` bytes, so that a prefix
    /// of `size` bytes may be read.
    unsafe fn static_instance_of(object: P, name: &str, size: usize) -> bool {
        let type_ = ffi::Py_TYPE(object);
        (*type_).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE == 0
            && (*type_).tp_basicsize >= 0
            && (*type_).tp_basicsize as usize >= size
            && std::ffi::CStr::from_ptr((*type_).tp_name).to_bytes() == name.as_bytes()
    }

    /// The recursion fields of `ThreadStatePrefix` are where this build
    /// expects them: moving the recursion limit moves exactly those fields,
    /// and so does entering a C recursion level (3.12/3.13); since 3.14,
    /// the machine-stack limit answers both ways.
    unsafe fn tstate_layout_ok() -> bool {
        let tstate = ffi::PyThreadState_Get();
        let prefix = tstate as *const ThreadStatePrefix;
        let limit = ffi::Py_GetRecursionLimit();
        let remaining = (*prefix).py_recursion_remaining;
        if (*prefix).py_recursion_limit != limit || remaining <= 0 || remaining > limit {
            return false;
        }
        let Some(probe) = limit.checked_add(77) else {
            return false;
        };
        ffi::Py_SetRecursionLimit(probe);
        let moved = (*prefix).py_recursion_limit == probe
            && (*prefix).py_recursion_remaining == remaining + 77;
        ffi::Py_SetRecursionLimit(limit);
        if !(moved
            && (*prefix).py_recursion_limit == limit
            && (*prefix).py_recursion_remaining == remaining)
        {
            return false;
        }
        #[cfg(not(Py_3_14))]
        {
            let c_remaining = (*prefix).c_recursion_remaining;
            if c_remaining <= 0 || c_remaining > 1_000_000 {
                return false;
            }
            if Py_EnterRecursiveCall(c" in a layout check".as_ptr()) != 0 {
                ffi::PyErr_Clear();
                return false;
            }
            let entered = (*prefix).c_recursion_remaining == c_remaining - 1;
            Py_LeaveRecursiveCall();
            entered && (*prefix).c_recursion_remaining == c_remaining
        }
        #[cfg(Py_3_14)]
        {
            (*prefix).holds_gil == 1
                && (*prefix).recursion_headroom == 0
                && _Py_ReachedRecursionLimitWithMargin(tstate, 0) == 0
                && _Py_ReachedRecursionLimitWithMargin(tstate, 1 << 16) != 0
        }
    }

    impl Canon {
        fn new(py: Python<'_>) -> PyResult<Option<Canon>> {
            let version = py.version_info();
            if (version.major, version.minor) != (3, LAYOUT_MINOR) {
                return Ok(None);
            }
            let globals = PyDict::new(py);
            globals.set_item("__builtins__", PyDict::new(py))?;
            py.run(PROBE, Some(&globals), None)?;
            let get = |name: &str| -> PyResult<Bound<'_, PyAny>> {
                globals
                    .get_item(name)?
                    .ok_or_else(|| pyo3::exceptions::PyKeyError::new_err(name.to_owned()))
            };
            // Safety: the static `type` object.
            let type_type =
                unsafe { Bound::from_borrowed_ptr(py, ptr::addr_of_mut!(ffi::PyType_Type) as P) };
            let new_class = |name: &str, entries: &[(&str, Bound<'_, PyAny>)]| {
                let namespace = PyDict::new(py);
                for (key, value) in entries {
                    namespace.set_item(key, value)?;
                }
                type_type.call1((name, pyo3::types::PyTuple::empty(py), namespace))
            };
            let repr_class = new_class("Repr", &[("__repr__", get("repr_")?), ("__get__", get("get_")?)])?;
            let managed_class = new_class("Managed", &[])?;
            let managed = managed_class.call0()?;
            managed.setattr("a", 1)?;
            let probe_instance = repr_class.call0()?;
            let bound = probe_instance.getattr("__repr__")?;
            let cell_tuple = get("closure")?.call0()?.getattr("__closure__")?;
            // Safety: the static `property` type.
            let property = unsafe {
                Bound::from_borrowed_ptr(py, ptr::addr_of_mut!(ffi::PyProperty_Type) as P)
            }
            .call1((get("getter")?,))?;
            let tuplegetter_type = PyModule::import(py, "_collections")?.getattr("_tuplegetter")?;
            let classify = load_audit_module(py)?.into_bound(py);
            if !classify.getattr("SUPPORTED")?.is_truthy()? {
                return Ok(None);
            }
            classify.getattr("_references")?.call0()?;
            let classify = classify.getattr("classify")?.unbind();
            let builtins = PyModule::import(py, "builtins")?;
            let thread = PyModule::import(py, "_thread")?;
            let sys_module = PyModule::import(py, "sys")?;
            let keep = RefCell::new(Vec::new());
            // Safety: a leaked, static method definition and a C function
            // with the METH_O signature.
            let weak_callback = unsafe {
                let def = Box::leak(Box::new(ffi::PyMethodDef {
                    ml_name: c"kolo_code_released".as_ptr(),
                    ml_meth: ffi::PyMethodDefPointer {
                        PyCFunction: weak_callback,
                    },
                    ml_flags: ffi::METH_O,
                    ml_doc: ptr::null(),
                }));
                let function = ffi::PyCFunction_NewEx(def, ptr::null_mut(), ptr::null_mut());
                if function.is_null() {
                    return Err(PyErr::fetch(py));
                }
                Bound::from_owned_ptr(py, function)
            };
            // Safety: the probes above are live objects of the expected
            // types; every read is checked against a value we know.
            unsafe {
                let repr_type = repr_class.as_ptr() as T;
                if ffi::Py_TYPE(repr_class.as_ptr()) != ptr::addr_of_mut!(ffi::PyType_Type)
                    || ffi::Py_TYPE(managed_class.as_ptr()) != ptr::addr_of_mut!(ffi::PyType_Type)
                    || (*(managed_class.as_ptr() as T)).tp_flags & ffi::Py_TPFLAGS_MANAGED_DICT == 0
                    || ffi::Py_TYPE(managed.as_ptr()) != managed_class.as_ptr() as T
                {
                    return Ok(None);
                }
                let builtin = |name: &str, module: &Bound<'_, PyModule>| -> PyResult<usize> {
                    let value = module.getattr(name)?;
                    let object = value.as_ptr();
                    if ffi::Py_TYPE(object) != ptr::addr_of_mut!(ffi::PyCFunction_Type) {
                        return Ok(0);
                    }
                    let function = object as *mut ffi::PyCFunctionObject;
                    let ml_name = std::ffi::CStr::from_ptr((*(*function).m_ml).ml_name);
                    if ml_name.to_bytes() != name.as_bytes()
                        || (*function).m_self != module.as_ptr()
                    {
                        return Ok(0);
                    }
                    keep.borrow_mut().push(value.clone().unbind());
                    Ok(object as usize)
                };
                // Managed dict pointer: values (3.12: tagged pointer, 3.13:
                // NULL) until `__dict__` materializes the dict in place.
                let word = *(managed.as_ptr() as *const usize).offset(-3);
                #[cfg(not(Py_3_13))]
                let values_ok = word & 1 == 1;
                #[cfg(Py_3_13)]
                let values_ok = word == 0;
                let dict = managed.getattr("__dict__")?;
                let word = *(managed.as_ptr() as *const usize).offset(-3);
                let managed_ok = values_ok && word == dict.as_ptr() as usize;
                // Built here, not by the probe: tracing callbacks can rebind
                // the probe's globals while it runs.
                let general = PyDict::new(py);
                general.set_item(1, 2)?;
                let unicode = PyDict::new(py);
                unicode.set_item("a", 1)?;
                unicode.set_item("b", 2)?;
                let kind = |dict: &Bound<'_, PyDict>| -> (u8, isize, bool) {
                    let dict = dict.as_ptr() as *mut DictObject;
                    (
                        (*(*dict).ma_keys).dk_kind,
                        (*dict).ma_used,
                        (*dict).ma_values.is_null(),
                    )
                };
                let kinds_ok = kind(&general) == (DICT_KEYS_GENERAL, 1, true)
                    && matches!(kind(&unicode), (1, 2, true))
                    && exact_dict(dict.as_ptr())
                    && (*(dict.as_ptr() as *mut DictObject)).ma_used == 1;
                let tstate_ok = tstate_layout_ok();
                const IMMUTABLE_TYPE: std::os::raw::c_ulong = 1 << 8;
                let tuplegetter_ok = ffi::Py_TYPE(tuplegetter_type.as_ptr())
                    == ptr::addr_of_mut!(ffi::PyType_Type)
                    && {
                        let type_ = tuplegetter_type.as_ptr() as T;
                        (*type_).tp_flags & IMMUTABLE_TYPE != 0
                            && std::ffi::CStr::from_ptr((*type_).tp_name).to_bytes()
                                == b"collections._tuplegetter"
                            && (*type_).tp_basicsize >= 0
                            && (*type_).tp_basicsize as usize >= std::mem::size_of::<TupleGetter>()
                    };
                if !tuplegetter_ok {
                    return Ok(None);
                }
                let getter = tuplegetter_type.call1((1, py.None()))?;
                let sample = pyo3::types::PyTuple::new(py, [10, 20])?;
                let tuplegetter_ok = ffi::Py_TYPE(getter.as_ptr())
                    == tuplegetter_type.as_ptr() as T
                    && (*(getter.as_ptr() as *mut TupleGetter)).index == 1
                    && getter
                        .call_method1("__get__", (sample, py.None()))?
                        .extract::<i64>()?
                        == 20;
                let fget_member = _PyType_Lookup(
                    ptr::addr_of_mut!(ffi::PyProperty_Type),
                    name!(py, "fget").as_ptr(),
                );
                let property_fget_offset = if !fget_member.is_null()
                    && ffi::Py_TYPE(fget_member) == ptr::addr_of_mut!(ffi::PyMemberDescr_Type)
                {
                    (*(*(fget_member as *mut MemberDescr)).d_member).offset
                } else {
                    0
                };
                let fget_ok = ffi::Py_TYPE(property.as_ptr())
                    == ptr::addr_of_mut!(ffi::PyProperty_Type)
                    && property_fget_offset > 0
                    && (property_fget_offset as usize) + std::mem::size_of::<P>()
                        <= (*ptr::addr_of_mut!(ffi::PyProperty_Type)).tp_basicsize as usize
                    && *((property.as_ptr() as *mut u8).offset(property_fget_offset) as *const P)
                        == get("getter")?.as_ptr();
                let method_ok = static_instance_of(
                    bound.as_ptr(),
                    "method",
                    std::mem::size_of::<MethodObject>(),
                ) && (*(bound.as_ptr() as *mut MethodObject)).im_func == get("repr_")?.as_ptr()
                    && (*(bound.as_ptr() as *mut MethodObject)).im_self == probe_instance.as_ptr();
                let cell = if ffi::PyTuple_CheckExact(cell_tuple.as_ptr()) != 0
                    && ffi::PyTuple_GET_SIZE(cell_tuple.as_ptr()) == 1
                {
                    Bound::from_borrowed_ptr(py, ffi::PyTuple_GET_ITEM(cell_tuple.as_ptr(), 0))
                } else {
                    return Ok(None);
                };
                let one = 1i32.into_pyobject(py)?;
                let cell_ok = static_instance_of(
                    cell.as_ptr(),
                    "cell",
                    std::mem::size_of::<CellObject>(),
                ) && (*(cell.as_ptr() as *mut CellObject)).ob_ref == one.as_ptr();
                let functions_ok = ["repr_", "get_", "getter", "closure"]
                    .iter()
                    .all(|name| get(name).is_ok_and(|f| {
                        ffi::Py_TYPE(f.as_ptr()) == ptr::addr_of_mut!(ffi::PyFunction_Type)
                    }));
                if !(functions_ok
                    && method_ok
                    && cell_ok
                    && managed_ok
                    && kinds_ok
                    && tstate_ok
                    && tuplegetter_ok
                    && fget_ok)
                {
                    return Ok(None);
                }
                METHOD_TYPE.store(ffi::Py_TYPE(bound.as_ptr()) as usize, Ordering::Relaxed);
                CELL_TYPE.store(ffi::Py_TYPE(cell.as_ptr()) as usize, Ordering::Relaxed);
                let none_type = ffi::Py_TYPE(ffi::Py_None());
                let canon = Canon {
                    slot_tp_repr: (*repr_type).tp_repr.map_or(0, |f| f as usize),
                    generic_getattro: (*ptr::addr_of_mut!(ffi::PyBaseObject_Type))
                        .tp_getattro
                        .map_or(0, |f| f as usize),
                    slot_tp_descr_get: (*repr_type).tp_descr_get.map_or(0, |f| f as usize),
                    object_repr: (*ptr::addr_of_mut!(ffi::PyBaseObject_Type))
                        .tp_repr
                        .map_or(0, |f| f as usize),
                    type_repr: (*ptr::addr_of_mut!(ffi::PyType_Type))
                        .tp_repr
                        .map_or(0, |f| f as usize),
                    object_class: _PyType_Lookup(
                        ptr::addr_of_mut!(ffi::PyBaseObject_Type),
                        name!(py, "__class__").as_ptr(),
                    ) as usize,
                    c_richcompare: [
                        ptr::addr_of_mut!(ffi::PyBaseObject_Type),
                        ptr::addr_of_mut!(ffi::PyTuple_Type),
                        ptr::addr_of_mut!(ffi::PyUnicode_Type),
                        ptr::addr_of_mut!(ffi::PyLong_Type),
                        ptr::addr_of_mut!(ffi::PyFloat_Type),
                        ptr::addr_of_mut!(ffi::PyBytes_Type),
                        none_type,
                    ]
                    .map(|t| (*t).tp_richcompare.map_or(0, |f| f as usize)),
                    builtin_id: builtin("id", &builtins)?,
                    weak_callback: weak_callback.as_ptr() as usize,
                    trampoline_active: builtin("is_stack_trampoline_active", &sys_module)?,
                    function_vectorcall: (*(get("repr_")?.as_ptr() as *mut ffi::PyFunctionObject))
                        .vectorcall
                        .map_or(0, |f| f as usize),
                    builtin_len: builtin("len", &builtins)?,
                    builtin_repr: builtin("repr", &builtins)?,
                    builtin_isinstance: builtin("isinstance", &builtins)?,
                    builtin_getattr: builtin("getattr", &builtins)?,
                    thread_module: thread.as_ptr() as usize,
                    get_ident: builtin("get_ident", &thread)?,
                    tuplegetter_type: ffi::Py_TYPE(getter.as_ptr()) as usize,
                    property_fget_offset,
                    classify,
                    _keep: Vec::new(),
                };
                let mut keep = keep.into_inner();
                keep.push(thread.into_any().unbind());
                keep.push(weak_callback.unbind());
                if canon.function_vectorcall == 0
                    || !trusted_eval_frame(current_eval_frame(), canon.trampoline_active)
                {
                    return Ok(None);
                }
                if canon.slot_tp_repr == 0
                    || canon.slot_tp_descr_get == 0
                    || canon.object_class == 0
                    || canon.get_ident == 0
                {
                    return Ok(None);
                }
                Ok(Some(Canon {
                    _keep: keep,
                    ..canon
                }))
            }
        }
    }

    const CONV_FORMAT: u8 = 0;
    const CONV_STR: u8 = 1;
    const CONV_REPR: u8 = 2;
    const CONV_EXACT_STR: u8 = 3;

    struct Field {
        type_root: bool,
        /// Indices into the code's `co_names` (the program's own strings,
        /// kept alive by the code object, which is guarded by `WeakIs`).
        names: Box<[usize]>,
        conv: u8,
    }

    enum Verdict {
        FString {
            uses_type: bool,
            fields: Box<[Field]>,
        },
        DcWrapper312 {
            running: usize,
            user: usize,
        },
        RecursiveRepr {
            running: usize,
            user: usize,
        },
        /// `return self.<co_names[index]>`.
        SimpleGetter(usize),
        NamedTupleRepr {
            fmt: usize,
        },
        JinjaContextRepr,
        JinjaGetAll,
        JinjaMacroRepr,
        RichAutoRepr,
        RichStyleRichRepr,
        RichBitGet,
        RichColorRichRepr,
        RichTextPlain,
        EnumPropertyGet,
    }

    fn parse_verdict(
        result: &Bound<'_, PyAny>,
        code: &Bound<'_, PyAny>,
    ) -> PyResult<Option<Verdict>> {
        if result.is_none() {
            return Ok(None);
        }
        let co_names = code.getattr("co_names")?;
        let name_index = |name: Bound<'_, PyAny>| -> PyResult<usize> {
            co_names.call_method1("index", (name,))?.extract()
        };
        let kind: u32 = result.get_item(0)?.extract()?;
        let extra = result.get_item(1)?;
        let indices = |extra: &Bound<'_, PyAny>| -> PyResult<(usize, usize)> {
            Ok((extra.get_item(0)?.extract()?, extra.get_item(1)?.extract()?))
        };
        Ok(Some(match kind {
            1 => {
                let globals = extra.get_item(0)?;
                let mut uses_type = false;
                for name in globals.try_iter()? {
                    let name: String = name?.extract()?;
                    if name != "type" {
                        return Ok(None);
                    }
                    uses_type = true;
                }
                let mut fields = Vec::new();
                for field in extra.get_item(1)?.try_iter()? {
                    let field = field?;
                    let root: u32 = field.get_item(0)?.extract()?;
                    let names = field
                        .get_item(1)?
                        .try_iter()?
                        .map(|name| name_index(name?))
                        .collect::<PyResult<Vec<_>>>()?;
                    let conv: u8 = field.get_item(2)?.extract()?;
                    if root > 1 || conv > CONV_EXACT_STR {
                        return Ok(None);
                    }
                    fields.push(Field {
                        type_root: root == 1,
                        names: names.into(),
                        conv,
                    });
                }
                Verdict::FString {
                    uses_type,
                    fields: fields.into(),
                }
            }
            2 => {
                let (running, user) = indices(&extra)?;
                Verdict::DcWrapper312 { running, user }
            }
            3 => {
                let (running, user) = indices(&extra)?;
                Verdict::RecursiveRepr { running, user }
            }
            4 => Verdict::SimpleGetter(name_index(extra)?),
            5 => Verdict::NamedTupleRepr {
                fmt: extra.get_item(0)?.extract()?,
            },
            10 => Verdict::JinjaContextRepr,
            11 => Verdict::JinjaGetAll,
            12 => Verdict::JinjaMacroRepr,
            20 => Verdict::RichAutoRepr,
            21 => Verdict::RichStyleRichRepr,
            22 => Verdict::RichBitGet,
            23 => Verdict::RichColorRichRepr,
            26 => Verdict::RichTextPlain,
            30 => Verdict::EnumPropertyGet,
            _ => return Ok(None),
        }))
    }

    /// A verdict for the code object at some address, with a weak
    /// reference to that code object: holding it strongly would change when
    /// the program's code objects are freed. A new code object at a reused
    /// address does not inherit the verdict.
    struct VerdictSlot {
        weakref: Py<PyAny>,
        verdict: Option<Arc<Verdict>>,
    }

    impl VerdictSlot {
        /// Whether this slot is about the (live) code object `code`.
        unsafe fn is_for(&self, code: P) -> bool {
            weak_target(self.weakref.as_ptr()) == code as usize
        }
    }

    /// Verdicts kept for code objects that may have died, before stale
    /// slots are swept.
    const MAX_VERDICTS: usize = 4096;

    /// Verdicts by code object (weakly held), process-wide: a verdict depends only
    /// on the code object, so every monitor and thread shares them.
    static VERDICTS: Mutex<Option<HashMap<usize, VerdictSlot>>> = Mutex::new(None);

    #[derive(Clone, Copy)]
    struct TypeInfo {
        tag: u32,
        mro_safe: bool,
        generic_getattro: bool,
        default_class: bool,
        has_instance_dict: bool,
        c_richcompare: bool,
    }

    unsafe fn dict_lookup_safe(dict: P) -> bool {
        // Lookups in dicts whose keys are all str (unicode or split key
        // tables) never call a key's `__eq__`.
        let dict = dict as *mut DictObject;
        !(*dict).ma_values.is_null() || (*(*dict).ma_keys).dk_kind != DICT_KEYS_GENERAL
    }

    unsafe fn exact_dict(object: P) -> bool {
        ffi::Py_TYPE(object) == ptr::addr_of_mut!(ffi::PyDict_Type)
    }

    impl TypeInfo {
        unsafe fn compute(py: Python<'_>, canon: &Canon, type_: T, tag: u32) -> TypeInfo {
            let mro = (*type_).tp_mro;
            let mut mro_safe = !mro.is_null() && ffi::PyTuple_CheckExact(mro) != 0;
            if mro_safe {
                for index in 0..ffi::PyTuple_GET_SIZE(mro) {
                    let base = ffi::PyTuple_GET_ITEM(mro, index) as T;
                    if (*base).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE == 0 {
                        continue;
                    }
                    let dict = (*base).tp_dict;
                    if dict.is_null() || !exact_dict(dict) || !dict_lookup_safe(dict) {
                        mro_safe = false;
                        break;
                    }
                }
            }
            let richcompare = (*type_).tp_richcompare.map_or(0, |f| f as usize);
            TypeInfo {
                tag,
                mro_safe,
                generic_getattro: mro_safe
                    && (*type_).tp_getattro.map_or(0, |f| f as usize) == canon.generic_getattro,
                default_class: mro_safe
                    && _PyType_Lookup(type_, name!(py, "__class__").as_ptr()) as usize
                        == canon.object_class,
                has_instance_dict: (*type_).tp_flags & ffi::Py_TPFLAGS_MANAGED_DICT != 0
                    || (*type_).tp_dictoffset != 0,
                c_richcompare: canon.c_richcompare.contains(&richcompare),
            }
        }
    }

    /// One check of a recorded dependency. Recording runs a certified
    /// repr's plan and emits one guard per location the plan read; validation
    /// only evaluates the guards, in order, without re-running the plan.
    ///
    /// Entries hold no references to the program's objects (holding them
    /// would change when they are freed and which addresses get reused).
    /// Validation therefore starts from the live root and every guard reads
    /// only an object that an earlier guard reached from it: a value found
    /// in a field of a live object is live. Because such a value can be a
    /// different object than at recording time (the old one freed, a new one
    /// allocated at the same address), every object whose type or immutable
    /// contents the plan relied on gets its type (`Type`) and contents
    /// (`Str`, `Int`, `Tuple`, ...) guarded, unless it is immortal or proven
    /// to be the very same object: held by a dict or type whose unique,
    /// never-reused version is unchanged (`DictVersion`, `Tag`).
    enum Guard {
        /// A pointer-sized field of a live object (a slot, the type of an
        /// object, a function's `__code__`/globals/closure/qualname/
        /// `__dict__`, a cell's content, a property's getter, a set's size).
        Word(*const usize, usize),
        /// `tp_version_tag` of a live heap type: a fresh, never-reused tag
        /// is assigned on any modification, so an equal tag means the very
        /// same, unmodified type.
        Tag(*const u32, u32),
        /// The exact type of a live object.
        Type { object: P, type_: usize },
        /// An exact str equal to a copy taken at recording time.
        Str { object: P, copy: Py<PyAny> },
        /// An exact int equal to a copy taken at recording time.
        Int { object: P, copy: Py<PyAny> },
        /// An exact float with these bits.
        Float { object: P, bits: u64 },
        /// An exact complex with these bits.
        Complex { object: P, real: u64, imag: u64 },
        /// Exact bytes with these contents.
        Bytes { object: P, data: Box<[u8]> },
        /// Size and items of a live tuple (exact or subclass).
        Tuple { tuple: P, items: Box<[usize]> },
        /// A live code object is the one a verdict was computed for: the
        /// weak reference (Kolo's own) still resolves to it.
        WeakIs { weakref: Py<PyAny>, target: usize },
        /// 3.12/3.13: `ma_version_tag` of a live dict with a combined
        /// table: every mutation assigns a new interpreter-wide unique
        /// version, so an unchanged version means the same keys and values
        /// in the same order. (3.14 removed it.)
        #[cfg(not(Py_3_14))]
        DictVersion(*const DictObject, u64),
        /// Length, storage pointer and items of a live list.
        List {
            list: *const ffi::PyListObject,
            ob_item: usize,
            items: Box<[usize]>,
        },
        /// Items of a live set or frozenset, in iteration order (sets have
        /// no version tag).
        Set { set: P, items: Box<[usize]> },
        /// Keys and values of a live dict, in iteration order: every dict on
        /// 3.14+ (which has no `ma_version_tag`), and split-table dicts
        /// (instance `__dict__`s), whose values can be shared with an
        /// object's inline values and written there directly.
        DictItems { dict: P, items: Box<[usize]> },
        /// The value (NULL: absent) stored under an exact-str `key` in a
        /// live, exact dict whose lookups cannot run a key's `__eq__`: a
        /// lookup of one name (globals, builtins, a module's or type's dict,
        /// a function's `__dict__`) depends on that entry only.
        DictItem { dict: P, key: P, value: usize },
        /// An instance attribute with no class descriptor, read through
        /// `PyObject_GenericGetAttr` (pure C once the type's tag guard held
        /// and the instance dict has only str keys).
        Attr { object: P, name: P, value: usize },
        /// A method lookup on an instance is not shadowed by the instance
        /// dict: generic getattr returns the class function bound to it.
        Unshadowed { object: P, name: P, function: usize },
    }

    // Safety: guards are only evaluated under the GIL on the thread owning
    // the cache, in order, from a live root (see `Guard`).
    unsafe impl Send for Guard {}

    unsafe fn instance_dict_safe(object: P) -> bool {
        let type_ = ffi::Py_TYPE(object);
        if (*type_).tp_flags & ffi::Py_TPFLAGS_MANAGED_DICT != 0 {
            let word = *(object as *const usize).offset(-3);
            #[cfg(not(Py_3_13))]
            let values = word & 1 == 1 || word == 0;
            #[cfg(Py_3_13)]
            let values = word == 0;
            values || dict_lookup_safe(word as P)
        } else if (*type_).tp_dictoffset != 0 {
            let dict = _PyObject_GetDictPtr(object);
            dict.is_null() || (*dict).is_null() || dict_lookup_safe(*dict)
        } else {
            true
        }
    }

    /// `dict[key]` as a borrowed pointer (NULL when missing) for an exact
    /// dict whose lookups cannot run Python.
    unsafe fn dict_get(dict: P, key: P) -> P {
        let value = ffi::PyDict_GetItemWithError(dict, key);
        if value.is_null() && !ffi::PyErr_Occurred().is_null() {
            ffi::PyErr_Clear();
        }
        value
    }

    /// `PyObject_GenericGetAttr(object, name)` as a borrowed pointer (NULL
    /// when missing). The value stays referenced by the instance or class.
    unsafe fn generic_getattr(object: P, name: P) -> P {
        let value = ffi::PyObject_GenericGetAttr(object, name);
        if value.is_null() {
            ffi::PyErr_Clear();
            return ptr::null_mut();
        }
        ffi::Py_DECREF(value);
        value
    }

    unsafe fn dict_items(dict: P) -> Vec<usize> {
        let mut items = Vec::with_capacity(2 * ffi::PyDict_Size(dict).max(0) as usize);
        let mut position = 0;
        let (mut key, mut value) = (ptr::null_mut(), ptr::null_mut());
        while ffi::PyDict_Next(dict, &mut position, &mut key, &mut value) != 0 {
            items.push(key as usize);
            items.push(value as usize);
        }
        items
    }

    /// `dict_items(dict) == items`, without allocating.
    unsafe fn dict_items_equal(dict: P, items: &[usize]) -> bool {
        let mut position = 0;
        let (mut key, mut value) = (ptr::null_mut(), ptr::null_mut());
        let mut expected = items.chunks_exact(2);
        while ffi::PyDict_Next(dict, &mut position, &mut key, &mut value) != 0 {
            match expected.next() {
                Some(pair) if pair[0] == key as usize && pair[1] == value as usize => {}
                _ => return false,
            }
        }
        expected.next().is_none()
    }

    /// `set_items(set) == items`, without allocating.
    unsafe fn set_items_equal(set: P, items: &[usize]) -> bool {
        let mut position = 0;
        let (mut key, mut hash) = (ptr::null_mut(), 0);
        let mut expected = items.iter();
        while _PySet_NextEntry(set, &mut position, &mut key, &mut hash) != 0 {
            if expected.next() != Some(&(key as usize)) {
                return false;
            }
        }
        expected.next().is_none()
    }

    unsafe fn set_items(set: P) -> Vec<usize> {
        let mut items = Vec::with_capacity(ffi::PySet_Size(set).max(0) as usize);
        let mut position = 0;
        let (mut key, mut hash) = (ptr::null_mut(), 0);
        while _PySet_NextEntry(set, &mut position, &mut key, &mut hash) != 0 {
            items.push(key as usize);
        }
        items
    }

    impl Guard {
        #[inline]
        unsafe fn holds(&self) -> bool {
            match self {
                Guard::Word(at, value) => **at == *value,
                Guard::Tag(at, tag) => **at == *tag,
                Guard::Type { object, type_ } => ffi::Py_TYPE(*object) as usize == *type_,
                Guard::Str { object, copy } => ffi::PyUnicode_Compare(*object, copy.as_ptr()) == 0,
                Guard::Int { object, copy } => {
                    ffi::PyObject_RichCompareBool(*object, copy.as_ptr(), ffi::Py_EQ) == 1
                }
                Guard::Float { object, bits } => ffi::PyFloat_AsDouble(*object).to_bits() == *bits,
                Guard::Complex { object, real, imag } => {
                    ffi::PyComplex_RealAsDouble(*object).to_bits() == *real
                        && ffi::PyComplex_ImagAsDouble(*object).to_bits() == *imag
                }
                Guard::Bytes { object, data } => {
                    ffi::PyBytes_Size(*object) as usize == data.len()
                        && std::slice::from_raw_parts(
                            ffi::PyBytes_AsString(*object) as *const u8,
                            data.len(),
                        ) == &data[..]
                }
                Guard::Tuple { tuple, items } => {
                    ffi::PyTuple_GET_SIZE(*tuple) as usize == items.len()
                        && items.iter().enumerate().all(|(index, item)| {
                            ffi::PyTuple_GET_ITEM(*tuple, index as ffi::Py_ssize_t) as usize
                                == *item
                        })
                }
                Guard::WeakIs { weakref, target } => weak_target(weakref.as_ptr()) == *target,
                #[cfg(not(Py_3_14))]
                Guard::DictVersion(dict, version) => (**dict).watcher_tag == *version,
                Guard::List {
                    list,
                    ob_item,
                    items,
                } => {
                    (**list).ob_base.ob_size as usize == items.len()
                        && (**list).ob_item as usize == *ob_item
                        && (items.is_empty()
                            || std::slice::from_raw_parts(*ob_item as *const usize, items.len())
                                == &items[..])
                }
                Guard::Set { set, items } => {
                    ffi::PySet_Size(*set) as usize == items.len() && set_items_equal(*set, items)
                }
                Guard::DictItems { dict, items } => {
                    ffi::PyDict_Size(*dict) as usize * 2 == items.len()
                        && dict_items_equal(*dict, items)
                }
                Guard::DictItem { dict, key, value } => {
                    dict_lookup_safe(*dict) && dict_get(*dict, *key) as usize == *value
                }
                Guard::Attr {
                    object,
                    name,
                    value,
                } => {
                    instance_dict_safe(*object)
                        && generic_getattr(*object, *name) as usize == *value
                }
                Guard::Unshadowed {
                    object,
                    name,
                    function,
                } => instance_dict_safe(*object) && bound_to(*object, *name, *function),
            }
        }
    }


    /// Whether every guard holds.
    unsafe fn all_hold(guards: &[Guard]) -> bool {
        guards.iter().all(|guard| guard.holds())
    }

    /// A new str equal to the exact str `text` (Kolo's own object, never
    /// `text` itself unless it is an immortal singleton); NULL on failure.
    unsafe fn copy_str(text: P) -> P {
        let pad = ffi::PyUnicode_FromStringAndSize(c"x".as_ptr(), 1);
        if pad.is_null() {
            ffi::PyErr_Clear();
            return ptr::null_mut();
        }
        let padded = ffi::PyUnicode_Concat(text, pad);
        ffi::Py_DECREF(pad);
        if padded.is_null() {
            ffi::PyErr_Clear();
            return ptr::null_mut();
        }
        let copy = ffi::PyUnicode_Substring(padded, 0, ffi::PyUnicode_GetLength(text));
        ffi::Py_DECREF(padded);
        if copy.is_null() {
            ffi::PyErr_Clear();
        }
        copy
    }

    /// A new int equal to the exact int `value` (or an immortal small
    /// int); NULL on failure.
    unsafe fn copy_int(value: P) -> P {
        let negated = ffi::PyNumber_Negative(value);
        if negated.is_null() {
            ffi::PyErr_Clear();
            return ptr::null_mut();
        }
        let copy = ffi::PyNumber_Negative(negated);
        ffi::Py_DECREF(negated);
        if copy.is_null() {
            ffi::PyErr_Clear();
        }
        copy
    }

    /// The object a weak reference (Kolo's own) resolves to, 0 when dead.
    unsafe fn weak_target(weakref: P) -> usize {
        let mut object = ptr::null_mut();
        if ffi::compat::PyWeakref_GetRef(weakref, &mut object) <= 0 {
            if !ffi::PyErr_Occurred().is_null() {
                ffi::PyErr_Clear();
            }
            return 0;
        }
        ffi::Py_DECREF(object);
        object as usize
    }

    /// Whether generic getattr of `name` on `object` yields the class
    /// function `function` bound to `object` (rather than an instance value).
    unsafe fn bound_to(object: P, name: P, function: usize) -> bool {
        let bound = ffi::PyObject_GenericGetAttr(object, name);
        if bound.is_null() {
            ffi::PyErr_Clear();
            return false;
        }
        let result = ffi::Py_TYPE(bound) == method_type()
            && (*(bound as *mut MethodObject)).im_func as usize == function
            && (*(bound as *mut MethodObject)).im_self == object;
        ffi::Py_DECREF(bound);
        result
    }

    const MAX_DEPTH: u32 = 40;
    const MAX_GUARDS: usize = 1 << 16;
    /// Python frames and C recursion levels a certified repr may use per
    /// level of its graph (wrapper, `__repr__`, helper/getter/generator,
    /// `PyObject_Repr`), plus slack for error handling.
    const RECURSION_PER_LEVEL: i64 = 8;
    const RECURSION_SLACK: i64 = 64;

    /// Immutable leaves whose reprs are pure functions of their identity.
    unsafe fn is_scalar(value: P) -> bool {
        let type_ = ffi::Py_TYPE(value);
        value == ffi::Py_None()
            || type_ == ptr::addr_of_mut!(ffi::PyUnicode_Type)
            || type_ == ptr::addr_of_mut!(ffi::PyLong_Type)
            || type_ == ptr::addr_of_mut!(ffi::PyFloat_Type)
            || type_ == ptr::addr_of_mut!(ffi::PyBool_Type)
            || type_ == ptr::addr_of_mut!(ffi::PyBytes_Type)
            || type_ == ptr::addr_of_mut!(ffi::PyComplex_Type)
    }

    enum Stop {
        /// Recording found something it cannot certify.
        Uncert,
        /// A code object needs auditing first (outside the snapshot window).
        Audit,
    }

    type R<V = ()> = Result<V, Stop>;

    #[derive(Clone, Copy)]
    enum Val {
        Obj(P),
        Type(T),
        /// An exact str/bool/None value, fully determined by the reads
        /// recorded to produce it, whose repr/str/format is pure.
        Pure,
    }

    struct Rec<'a, 'py> {
        py: Python<'py>,
        canon: &'a Canon,
        verdicts: &'a HashMap<usize, VerdictSlot>,
        types: &'a mut HashMap<usize, TypeInfo>,
        pending: &'a mut Vec<Py<PyAny>>,
        guards: Vec<Guard>,
        depth: u32,
        max_depth: u32,
        why: &'static str,
        s: &'a mut Scratch,
    }

    const TYPE_SLOTS: usize = 32;

    /// Facts already established earlier in the current recording, kept in
    /// the cache only to reuse allocations. Recording runs no Python, so a
    /// type's tag, a function's code, a globals dict, a closure cell or an
    /// object's slots cannot change between two reads of one recording;
    /// repeats need no second guard.
    #[derive(Default)]
    struct Scratch {
        type_slots: [Option<(usize, TypeInfo)>; TYPE_SLOTS],
        seen_types: Vec<(usize, TypeInfo)>,
        seen_functions: Vec<(usize, Arc<Verdict>)>,
        /// (function or module dict, name) -> value
        seen_globals: Vec<(usize, usize, P)>,
        seen_cells: Vec<(usize, usize, P)>,
        /// Dicts whose contents are already guarded.
        seen_dicts: Vec<usize>,
        /// Objects whose repr dependencies were already recorded, with the
        /// height of their repr graph.
        seen_reprs: HashMap<usize, u32>,
        /// The last Style whose bit attributes were read: (object,
        /// `_set_attributes`, `_attributes` once read).
        bits: Option<(usize, i64, Option<i64>)>,
        /// (recursion-guard set, object) pairs of the wrappers running on
        /// the current path.
        running: Vec<(usize, usize)>,
        /// Sets repr'd in this recording, checked against recursion-guard
        /// sets met later (a memoized repr of a container holding one is
        /// not visited again).
        repr_sets: Vec<usize>,
        /// Objects whose type and immutable contents are fixed once the
        /// guards emitted so far hold (see `Rec::proven`).
        proven: HashSet<usize>,
        /// Objects whose exact type alone is guarded.
        typed: HashSet<usize>,
    }

    // Safety: the raw pointers are only meaningful during one recording
    // under the GIL and are cleared before the next.
    unsafe impl Send for Scratch {}

    impl Scratch {
        fn clear(&mut self) {
            self.type_slots = [None; TYPE_SLOTS];
            self.seen_types.clear();
            self.seen_functions.clear();
            self.seen_globals.clear();
            self.seen_cells.clear();
            self.seen_dicts.clear();
            self.seen_reprs.clear();
            self.bits = None;
            self.running.clear();
            self.repr_sets.clear();
            self.proven.clear();
            self.typed.clear();
        }
    }

    fn new_rec<'a, 'py>(
        py: Python<'py>,
        canon: &'a Canon,
        verdicts: &'a HashMap<usize, VerdictSlot>,
        cache: &'a mut Cache,
    ) -> Rec<'a, 'py> {
        let Cache {
            types,
            pending,
            scratch,
            ..
        } = cache;
        scratch.clear();
        Rec {
            py,
            canon,
            verdicts,
            types,
            pending,
            guards: Vec::new(),
            depth: 0,
            max_depth: 0,
            why: "",
            s: scratch,
        }
    }

    impl<'a, 'py> Rec<'a, 'py> {
        /// Whether `object`'s type and immutable contents need no guard of
        /// their own: it is immortal (negative 32-bit refcount on 3.12+,
        /// never freed, so its address is never reused), or the guards
        /// emitted so far already fix them (`prove`).
        #[inline]
        unsafe fn proven(&self, object: P) -> bool {
            object.is_null()
                || (ffi::Py_REFCNT(object) as u32 as i32) < 0
                || self.s.proven.contains(&(object as usize))
        }

        /// Record that once the guards emitted so far hold, `object` is the
        /// same object as now (held by a container whose unique version is
        /// guarded) or has had its type and contents guarded.
        #[inline]
        fn prove(&mut self, object: P) {
            if !object.is_null() {
                self.s.proven.insert(object as usize);
            }
        }

        /// Guard what the plan reads of `object` beyond its address: its
        /// exact type and, for an immutable value, its contents. Entries
        /// hold no references, so the object found at a recorded address can
        /// be a new one; equal type and contents make it read the same.
        unsafe fn identify(&mut self, object: P) -> R {
            if self.proven(object) {
                return Ok(());
            }
            let type_ = ffi::Py_TYPE(object);
            self.type_is(object)?;
            if ffi::PyUnicode_Check(object) != 0 {
                let copy = copy_str(object);
                self.require(!copy.is_null(), "could not copy a str")?;
                self.guard(Guard::Str {
                    object,
                    copy: Bound::from_owned_ptr(self.py, copy).unbind(),
                })?;
            } else if type_ == ptr::addr_of_mut!(ffi::PyLong_Type) {
                self.require(long_bits_at_most(object, 2000), "huge int")?;
                let copy = copy_int(object);
                self.require(!copy.is_null(), "could not copy an int")?;
                self.guard(Guard::Int {
                    object,
                    copy: Bound::from_owned_ptr(self.py, copy).unbind(),
                })?;
            } else if type_ == ptr::addr_of_mut!(ffi::PyFloat_Type) {
                let bits = ffi::PyFloat_AsDouble(object).to_bits();
                self.guard(Guard::Float { object, bits })?;
            } else if type_ == ptr::addr_of_mut!(ffi::PyComplex_Type) {
                let real = ffi::PyComplex_RealAsDouble(object).to_bits();
                let imag = ffi::PyComplex_ImagAsDouble(object).to_bits();
                self.guard(Guard::Complex { object, real, imag })?;
            } else if type_ == ptr::addr_of_mut!(ffi::PyBytes_Type) {
                let data = std::slice::from_raw_parts(
                    ffi::PyBytes_AsString(object) as *const u8,
                    ffi::PyBytes_Size(object) as usize,
                );
                self.guard(Guard::Bytes {
                    object,
                    data: data.into(),
                })?;
            } else if type_ == ptr::addr_of_mut!(ffi::PyTuple_Type) {
                self.tuple_items(object)?;
            } else if type_ == ptr::addr_of_mut!(ffi::PyFrozenSet_Type) {
                self.guard(Guard::Set {
                    set: object,
                    items: set_items(object).into(),
                })?;
            } else {
                return Ok(());
            }
            self.prove(object);
            Ok(())
        }

        /// Guard `object`'s exact type (once per recording).
        unsafe fn type_is(&mut self, object: P) -> R {
            if self.proven(object) || !self.s.typed.insert(object as usize) {
                return Ok(());
            }
            self.guard(Guard::Type {
                object,
                type_: ffi::Py_TYPE(object) as usize,
            })
        }

        /// `co_names[index]` of `function`'s code, whose verdict (and its
        /// `WeakIs` guard) was already established.
        unsafe fn code_name(&mut self, function: P, index: usize) -> R<Bound<'py, PyString>> {
            let code = (*(function as *mut ffi::PyFunctionObject)).func_code;
            let names = ffi::PyObject_GetAttrString(code, c"co_names".as_ptr());
            if names.is_null() {
                ffi::PyErr_Clear();
                return self.uncert("code names");
            }
            ffi::Py_DECREF(names);
            self.require(
                ffi::PyTuple_CheckExact(names) != 0 && index < ffi::PyTuple_GET_SIZE(names) as usize,
                "code names",
            )?;
            let name = ffi::PyTuple_GET_ITEM(names, index as ffi::Py_ssize_t);
            self.require(ffi::PyUnicode_CheckExact(name) != 0, "code names")?;
            Ok(Bound::from_borrowed_ptr(self.py, name).cast_into_unchecked::<PyString>())
        }

        /// The items of a tuple (or tuple subclass instance) whose type is
        /// already guarded.
        unsafe fn tuple_items(&mut self, tuple: P) -> R {
            if self.proven(tuple) {
                return Ok(());
            }
            let items = (0..ffi::PyTuple_GET_SIZE(tuple))
                .map(|index| ffi::PyTuple_GET_ITEM(tuple, index) as usize)
                .collect::<Vec<_>>();
            self.guard(Guard::Tuple {
                tuple,
                items: items.into(),
            })?;
            self.prove(tuple);
            Ok(())
        }

        /// Prove every key and value of a dict whose unique version is
        /// guarded: the dict has held them continuously since recording.
        #[cfg(not(Py_3_14))]
        unsafe fn prove_dict_items(&mut self, dict: P) {
            let mut position = 0;
            let (mut key, mut value) = (ptr::null_mut(), ptr::null_mut());
            while ffi::PyDict_Next(dict, &mut position, &mut key, &mut value) != 0 {
                self.prove(key);
                self.prove(value);
            }
        }

        #[inline]
        fn guard(&mut self, guard: Guard) -> R {
            if self.guards.len() >= MAX_GUARDS {
                return self.uncert("graph too large");
            }
            self.guards.push(guard);
            Ok(())
        }

        /// Guard the pointer-sized field `at` of `owner` (live, with its
        /// type guarded), whose value is an object (or NULL), and return that
        /// value.
        #[inline]
        unsafe fn field(&mut self, _owner: P, at: *const P) -> R<P> {
            let value = *at;
            self.guard(Guard::Word(at as *const usize, value as usize))?;
            Ok(value)
        }

        /// The contents of a dict: its version (3.12/3.13, combined-table
        /// dicts), which also proves its keys and values; otherwise its items
        /// (see `Guard::DictItems`). Guarded once per recording: recording
        /// runs no Python.
        unsafe fn dict_version(&mut self, dict: P) -> R {
            if self.s.seen_dicts.contains(&(dict as usize)) {
                return Ok(());
            }
            self.s.seen_dicts.push(dict as usize);
            self.identify(dict)?;
            #[cfg(not(Py_3_14))]
            if (*(dict as *const DictObject)).ma_values.is_null() {
                let raw = dict as *const DictObject;
                self.guard(Guard::DictVersion(raw, (*raw).watcher_tag))?;
                self.prove_dict_items(dict);
                return Ok(());
            }
            bump(&counters().snapshot_dicts, 1);
            let items = dict_items(dict);
            self.guard(Guard::DictItems {
                dict,
                items: items.clone().into(),
            })?;
            for key in items.iter().step_by(2) {
                self.identify(*key as P)?;
            }
            Ok(())
        }

        /// `dict[key]` (NULL when missing) for the live `dict`, guarded by
        /// that one entry.
        unsafe fn dict_item(&mut self, dict: P, key: P) -> R<P> {
            self.require(
                !dict.is_null() && exact_dict(dict) && dict_lookup_safe(dict),
                "dict with non-str keys",
            )?;
            self.identify(dict)?;
            let value = ffi::PyDict_GetItemWithError(dict, key);
            if value.is_null() && !ffi::PyErr_Occurred().is_null() {
                ffi::PyErr_Clear();
                return self.uncert("dict lookup failed");
            }
            self.guard(Guard::DictItem {
                dict,
                key,
                value: value as usize,
            })?;
            Ok(value)
        }

        unsafe fn list_guard(&mut self, list: P) -> R {
            self.identify(list)?;
            let len = ffi::PyList_GET_SIZE(list);
            let mut items = Vec::with_capacity(len as usize);
            for index in 0..len {
                items.push(ffi::PyList_GET_ITEM(list, index) as usize);
            }
            let list = list as *const ffi::PyListObject;
            self.guard(Guard::List {
                list,
                ob_item: (*list).ob_item as usize,
                items: items.into(),
            })
        }

        fn uncert<V>(&mut self, why: &'static str) -> R<V> {
            self.why = why;
            Err(Stop::Uncert)
        }

        #[inline]
        fn require(&mut self, condition: bool, why: &'static str) -> R {
            if condition {
                Ok(())
            } else {
                self.uncert(why)
            }
        }

        fn enter(&mut self) -> R {
            self.depth += 1;
            self.max_depth = self.max_depth.max(self.depth);
            self.require(self.depth <= MAX_DEPTH, "graph too deep")
        }

        fn leave(&mut self) {
            self.depth -= 1;
        }

        /// `type(object)`, guarded: always when `__class__` assignment
        /// could change it (only objects of heap types allow that), and
        /// otherwise unless `object` is proven.
        unsafe fn type_of(&mut self, object: P) -> R<T> {
            let type_ = ffi::Py_TYPE(object);
            // `__class__` can be assigned between heap types, and from
            // `ModuleType` to a subclass of it.
            if (*type_).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE != 0
                || type_ == ptr::addr_of_mut!(ffi::PyModule_Type)
            {
                self.field(object, ptr::addr_of!((*object).ob_type) as *const P)?;
            } else {
                self.type_is(object)?;
            }
            Ok(type_)
        }

        /// A type whose attribute resolution a plan relies on, guarded by
        /// its version tag (a fresh, never-reused tag is assigned whenever
        /// the type or a base is modified). Static types cannot be modified
        /// from Python and need no guard.
        unsafe fn type_guard(&mut self, type_: T) -> R<TypeInfo> {
            let slot = (type_ as usize >> 4) % TYPE_SLOTS;
            if let Some((seen, info)) = self.s.type_slots[slot] {
                if seen == type_ as usize {
                    return Ok(info);
                }
            }
            if let Some((_, info)) = self
                .s
                .seen_types
                .iter()
                .rev()
                .find(|(seen, _)| *seen == type_ as usize)
            {
                return Ok(*info);
            }
            let heap = (*type_).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE != 0;
            let mut tag = (*type_).tp_version_tag;
            if heap {
                if tag == 0 && PyUnstable_Type_AssignVersionTag(type_) != 0 {
                    tag = (*type_).tp_version_tag;
                }
                self.require(tag != 0, "type has no version tag")?;
                self.guard(Guard::Tag(ptr::addr_of!((*type_).tp_version_tag), tag))?;
                self.prove(type_ as P);
            }
            let info = match self.types.get(&(type_ as usize)) {
                Some(info) if info.tag == tag => *info,
                _ => {
                    let info = TypeInfo::compute(self.py, self.canon, type_, tag);
                    if self.types.len() >= MAX_NEGATIVE {
                        self.types.clear();
                    }
                    self.types.insert(type_ as usize, info);
                    info
                }
            };
            self.require(info.mro_safe, "class dict with non-str keys")?;
            self.s.type_slots[slot] = Some((type_ as usize, info));
            self.s.seen_types.push((type_ as usize, info));
            Ok(info)
        }

        /// What a Python function does, from its (guarded) `__code__`.
        unsafe fn verdict(&mut self, function: P) -> R<Arc<Verdict>> {
            if let Some((_, verdict)) = self
                .s
                .seen_functions
                .iter()
                .find(|(seen, _)| *seen == function as usize)
            {
                return Ok(Arc::clone(verdict));
            }
            self.require(
                ffi::Py_TYPE(function) == ptr::addr_of_mut!(ffi::PyFunction_Type),
                "not a Python function",
            )?;
            self.identify(function)?;
            let call = self.field(
                function,
                ptr::addr_of!((*(function as *mut ffi::PyFunctionObject)).vectorcall) as *const P,
            )?;
            self.require(
                call as usize == self.canon.function_vectorcall,
                "custom function vectorcall",
            )?;
            let code = self.field(
                function,
                ptr::addr_of!((*(function as *mut ffi::PyFunctionObject)).func_code),
            )?;
            let slot = self
                .verdicts
                .get(&(code as usize))
                .filter(|slot| slot.is_for(code));
            match slot {
                Some(VerdictSlot {
                    verdict: Some(verdict),
                    weakref,
                }) => {
                    let verdict = Arc::clone(verdict);
                    let weakref = weakref.clone_ref(self.py);
                    // The code at that address is the one audited (a new
                    // code object could reuse a freed one's address).
                    self.guard(Guard::WeakIs {
                        weakref,
                        target: code as usize,
                    })?;
                    self.s
                        .seen_functions
                        .push((function as usize, Arc::clone(&verdict)));
                    Ok(verdict)
                }
                Some(_) => self.uncert("uncertified code"),
                None => {
                    // With a callback, CPython creates a new weak reference rather than reusing one the program holds.
                    // The callback is Kolo's own C no-op (calling `id` would raise an audit event).
                    let weakref = ffi::PyWeakref_NewRef(code, self.canon.weak_callback as P);
                    if weakref.is_null() {
                        ffi::PyErr_Clear();
                        return self.uncert("code without weak references");
                    }
                    // Kolo's own and in no cycle: kept out of
                    // `gc.get_objects()`, which programs inspect.
                    ffi::PyObject_GC_UnTrack(weakref.cast());
                    self.pending
                        .push(Bound::from_owned_ptr(self.py, weakref).unbind());
                    Err(Stop::Audit)
                }
            }
        }

        /// `LOAD_GLOBAL name` in `function`: its globals, then its builtins.
        unsafe fn global(&mut self, function: P, name: &Bound<'py, PyString>) -> R<P> {
            if let Some((_, _, value)) = self
                .s
                .seen_globals
                .iter()
                .find(|(f, n, _)| *f == function as usize && *n == name.as_ptr() as usize)
            {
                return Ok(*value);
            }
            self.identify(function)?;
            let raw = function as *mut ffi::PyFunctionObject;
            let mut found = ptr::null_mut();
            for at in [
                ptr::addr_of!((*raw).func_globals),
                ptr::addr_of!((*raw).func_builtins),
            ] {
                let dict = self.field(function, at)?;
                let value = self.dict_item(dict, name.as_ptr())?;
                if !value.is_null() {
                    found = value;
                    break;
                }
            }
            self.require(!found.is_null(), "global not found")?;
            self.s
                .seen_globals
                .push((function as usize, name.as_ptr() as usize, found));
            Ok(found)
        }

        unsafe fn global_is(
            &mut self,
            function: P,
            name: &Bound<'py, PyString>,
            expected: usize,
        ) -> R {
            let value = self.global(function, name)?;
            self.require(
                value as usize == expected && expected != 0,
                "global rebound",
            )
        }

        unsafe fn cell(&mut self, function: P, index: usize) -> R<P> {
            if let Some((_, _, content)) = self
                .s
                .seen_cells
                .iter()
                .find(|(f, i, _)| *f == function as usize && *i == index)
            {
                return Ok(*content);
            }
            let closure = self.field(
                function,
                ptr::addr_of!((*(function as *mut ffi::PyFunctionObject)).func_closure),
            )?;
            self.require(
                !closure.is_null()
                    && ffi::PyTuple_CheckExact(closure) != 0
                    && index < ffi::PyTuple_GET_SIZE(closure) as usize,
                "closure shape",
            )?;
            self.identify(closure)?;
            let cell = ffi::PyTuple_GET_ITEM(closure, index as ffi::Py_ssize_t);
            self.require(ffi::Py_TYPE(cell) == cell_type(), "not a cell")?;
            self.identify(cell)?;
            let content = self.field(cell, ptr::addr_of!((*(cell as *mut CellObject)).ob_ref))?;
            self.require(!content.is_null(), "empty cell")?;
            self.s.seen_cells.push((function as usize, index, content));
            Ok(content)
        }

        /// An instance attribute that no data descriptor intercepts. With
        /// a plain (no `__get__`) class attribute `fallback`, generic getattr
        /// returns the instance value when present, else `fallback`.
        unsafe fn instance_value(
            &mut self,
            object: P,
            info: &TypeInfo,
            name: P,
            fallback: P,
        ) -> R<Val> {
            if !info.has_instance_dict {
                self.require(!fallback.is_null(), "missing attribute")?;
                self.prove(fallback);
                return Ok(Val::Obj(fallback));
            }
            self.require(instance_dict_safe(object), "instance dict has non-str keys")?;
            let value = generic_getattr(object, name);
            self.require(!value.is_null(), "missing attribute")?;
            if value == fallback {
                self.prove(value);
            }
            self.guard(Guard::Attr {
                object,
                name,
                value: value as usize,
            })?;
            Ok(Val::Obj(value))
        }

        /// `object.<name>` for an instance whose type uses generic attribute
        /// access, following `PyObject_GenericGetAttr` exactly for the
        /// descriptors it understands.
        unsafe fn attr(&mut self, object: P, name: &Bound<'py, PyString>) -> R<Val> {
            let type_ = self.type_of(object)?;
            let info = self.type_guard(type_)?;
            self.require(info.generic_getattro, "custom attribute access")?;
            let descr = _PyType_Lookup(type_, name.as_ptr());
            if descr.is_null() {
                return self.instance_value(object, &info, name.as_ptr(), ptr::null_mut());
            }
            self.prove(descr);
            let descr_type = self.type_of(descr)?;
            self.type_guard(descr_type)?;
            let is_data = (*descr_type).tp_descr_set.is_some();
            if descr_type == ptr::addr_of_mut!(ffi::PyMemberDescr_Type) {
                let member = (*(descr as *mut MemberDescr)).d_member;
                self.require(
                    matches!((*member).type_code, T_OBJECT | T_OBJECT_EX)
                        && (*member).flags & (READ_RESTRICTED | RELATIVE_OFFSET) == 0
                        && ffi::PyObject_TypeCheck(
                            object,
                            (*(descr as *mut MemberDescr)).d_common.d_type,
                        ) != 0,
                    "unsupported member",
                )?;
                let slot = self.field(
                    object,
                    (object as *mut u8).offset((*member).offset) as *const P,
                )?;
                if slot.is_null() {
                    self.require((*member).type_code == T_OBJECT, "unset slot")?;
                    return Ok(Val::Obj(ffi::Py_None()));
                }
                return Ok(Val::Obj(slot));
            }
            if descr_type == ptr::addr_of_mut!(ffi::PyProperty_Type) {
                let fget = self.field(
                    descr,
                    (descr as *mut u8).offset(self.canon.property_fget_offset) as *const P,
                )?;
                self.require(!fget.is_null(), "property without getter")?;
                return self.call_getter(fget, object);
            }
            if descr_type as usize == self.canon.tuplegetter_type {
                let index = (*(descr as *mut TupleGetter)).index;
                self.require(
                    ffi::PyTuple_Check(object) != 0
                        && index >= 0
                        && index < ffi::PyTuple_GET_SIZE(object),
                    "tuple getter out of range",
                )?;
                self.tuple_items(object)?;
                return Ok(Val::Obj(ffi::PyTuple_GET_ITEM(object, index)));
            }
            let descr_get = (*descr_type).tp_descr_get.map_or(0, |f| f as usize);
            if descr_get == self.canon.slot_tp_descr_get && descr_get != 0 {
                self.type_guard(descr_type)?;
                let get = _PyType_Lookup(descr_type, name!(self.py, "__get__").as_ptr());
                self.require(!get.is_null(), "descriptor without __get__")?;
                self.prove(get);
                let verdict = self.verdict(get)?;
                self.enter()?;
                let result = match *verdict {
                    Verdict::EnumPropertyGet if is_data => self.enum_property_get(descr, object),
                    Verdict::RichBitGet if !is_data && !info.has_instance_dict => {
                        self.rich_bit_get(descr, object)
                    }
                    _ => self.uncert("unsupported descriptor"),
                };
                self.leave();
                return result;
            }
            if is_data {
                return self.uncert("unsupported data descriptor");
            }
            if descr_get == 0 {
                return self.instance_value(object, &info, name.as_ptr(), descr);
            }
            self.uncert("attribute is a method or other descriptor")
        }

        /// `object.<name>` for a call: the function a method call runs.
        unsafe fn method(&mut self, object: P, name: &Bound<'py, PyString>) -> R<P> {
            let type_ = self.type_of(object)?;
            let info = self.type_guard(type_)?;
            self.require(info.generic_getattro, "custom attribute access")?;
            let descr = _PyType_Lookup(type_, name.as_ptr());
            self.require(
                !descr.is_null() && ffi::Py_TYPE(descr) == ptr::addr_of_mut!(ffi::PyFunction_Type),
                "method is not a function",
            )?;
            self.prove(descr);
            if info.has_instance_dict {
                self.require(instance_dict_safe(object), "instance dict has non-str keys")?;
                self.require(
                    bound_to(object, name.as_ptr(), descr as usize),
                    "method shadowed by instance attribute",
                )?;
                self.guard(Guard::Unshadowed {
                    object,
                    name: name.as_ptr(),
                    function: descr as usize,
                })?;
            }
            Ok(descr)
        }

        unsafe fn call_getter(&mut self, getter: P, object: P) -> R<Val> {
            self.enter()?;
            let result = self.call_getter_inner(getter, object);
            self.leave();
            result
        }

        unsafe fn call_getter_inner(&mut self, getter: P, object: P) -> R<Val> {
            let verdict = self.verdict(getter)?;
            match &*verdict {
                Verdict::SimpleGetter(index) => {
                    let name = self.code_name(getter, *index)?;
                    self.attr(object, &name)
                }
                Verdict::RichTextPlain => {
                    self.global_is(getter, name!(self.py, "len"), self.canon.builtin_len)?;
                    let Val::Obj(text) = self.attr(object, name!(self.py, "_text"))? else {
                        return self.uncert("text parts");
                    };
                    self.require(
                        ffi::PyList_CheckExact(text) != 0 && ffi::PyList_GET_SIZE(text) == 1,
                        "text parts not joined",
                    )?;
                    self.list_guard(text)?;
                    Ok(Val::Obj(ffi::PyList_GET_ITEM(text, 0)))
                }
                _ => self.uncert("unsupported getter"),
            }
        }

        unsafe fn enum_property_get(&mut self, descr: P, object: P) -> R<Val> {
            let Val::Obj(fget) = self.attr(descr, name!(self.py, "fget"))? else {
                return self.uncert("enum property getter");
            };
            self.require(fget != ffi::Py_None(), "enum property without getter")?;
            self.call_getter(fget, object)
        }

        unsafe fn exact_int(&mut self, value: Val) -> R<i64> {
            let Val::Obj(object) = value else {
                return self.uncert("expected int");
            };
            self.require(ffi::PyLong_CheckExact(object) != 0, "expected exact int")?;
            self.identify(object)?;
            let mut overflow = 0;
            let value = ffi::PyLong_AsLongLongAndOverflow(object, &mut overflow);
            self.require(overflow == 0, "int too large")?;
            Ok(value)
        }

        unsafe fn rich_bit_get(&mut self, descr: P, object: P) -> R<Val> {
            let (set, mut attributes) = match self.s.bits {
                Some((seen, set, attributes)) if seen == object as usize => (set, attributes),
                _ => {
                    let set = self.attr(object, name!(self.py, "_set_attributes"))?;
                    (self.exact_int(set)?, None)
                }
            };
            let bit = self.attr(descr, name!(self.py, "bit"))?;
            let bit = self.exact_int(bit)?;
            if set & bit != 0 && attributes.is_none() {
                let value = self.attr(object, name!(self.py, "_attributes"))?;
                attributes = Some(self.exact_int(value)?);
            }
            self.s.bits = Some((object as usize, set, attributes));
            Ok(Val::Pure)
        }

        /// `type.__name__` / `__qualname__` read through the metaclass
        /// `type` (fixed by the type's tag).
        unsafe fn type_name(&mut self, type_: T, qualname: bool) -> R {
            self.type_guard(type_)?;
            // The metaclass and the names are guarded directly, not through
            // the tag (see `type_names`).
            let metatype = self.type_of(type_ as P)?;
            self.require(metatype == ptr::addr_of_mut!(ffi::PyType_Type), "metaclass")?;
            self.type_names(type_)?;
            if (*type_).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE != 0 {
                let heap = type_ as *mut ffi::PyHeapTypeObject;
                let name = if qualname {
                    (*heap).ht_qualname
                } else {
                    (*heap).ht_name
                };
                self.require(
                    ffi::PyUnicode_CheckExact(name) != 0,
                    "type name is not an exact str",
                )?;
            }
            Ok(())
        }

        /// `__name__`, `__qualname__` and `__module__` of a heap type.
        /// Assigning them goes through data descriptors on `type`, which on
        /// 3.13 does not reassign the version tag, so they are guarded
        /// directly (`__module__` lives in the type's dict).
        unsafe fn type_names(&mut self, type_: T) -> R {
            if (*type_).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE == 0 {
                return Ok(());
            }
            let heap = type_ as *mut ffi::PyHeapTypeObject;
            let name = self.field(type_ as P, ptr::addr_of!((*heap).ht_name))?;
            self.identify(name)?;
            let qualname = self.field(type_ as P, ptr::addr_of!((*heap).ht_qualname))?;
            self.identify(qualname)?;
            let dict = (*type_).tp_dict;
            self.require(
                !dict.is_null() && exact_dict(dict) && dict_lookup_safe(dict),
                "type dict",
            )?;
            self.prove(dict);
            let module = self.dict_item(dict, name!(self.py, "__module__").as_ptr())?;
            if module.is_null() {
                return Ok(());
            }
            self.identify(module)
        }

        /// `self.__class__` with the default `object.__class__`.
        unsafe fn class_of(&mut self, object: P) -> R<T> {
            let type_ = self.type_of(object)?;
            let info = self.type_guard(type_)?;
            self.require(
                info.generic_getattro && info.default_class,
                "custom __class__",
            )?;
            Ok(type_)
        }

        unsafe fn attr_val(&mut self, value: Val, name: &Bound<'py, PyString>) -> R<Val> {
            match value {
                Val::Obj(object) => {
                    if name.as_ptr() == name!(self.py, "__class__").as_ptr() {
                        return Ok(Val::Type(self.class_of(object)?));
                    }
                    self.attr(object, name)
                }
                Val::Type(type_) => {
                    let qualname = if name.as_ptr() == name!(self.py, "__name__").as_ptr() {
                        false
                    } else if name.as_ptr() == name!(self.py, "__qualname__").as_ptr() {
                        true
                    } else {
                        return self.uncert("unsupported type attribute");
                    };
                    self.type_name(type_, qualname)?;
                    Ok(Val::Pure)
                }
                Val::Pure => self.uncert("attribute of a str"),
            }
        }

        unsafe fn repr_val(&mut self, value: Val) -> R {
            match value {
                Val::Obj(object) => self.repr_dep(object),
                Val::Type(type_) => self.repr_dep(type_ as P),
                Val::Pure => Ok(()),
            }
        }

        /// `str(value)` or `format(value, "")` without running Python.
        unsafe fn str_val(&mut self, value: Val) -> R {
            match value {
                Val::Pure => Ok(()),
                Val::Type(_) => self.uncert("str of a type"),
                Val::Obj(object) => {
                    self.identify(object)?;
                    let type_ = ffi::Py_TYPE(object);
                    if type_ == ptr::addr_of_mut!(ffi::PyUnicode_Type)
                        || type_ == ptr::addr_of_mut!(ffi::PyFloat_Type)
                        || type_ == ptr::addr_of_mut!(ffi::PyBool_Type)
                        || object == ffi::Py_None()
                    {
                        return Ok(());
                    }
                    if type_ == ptr::addr_of_mut!(ffi::PyLong_Type) {
                        return self.require(long_bits_at_most(object, 2000), "huge int");
                    }
                    self.uncert("str of a non-builtin")
                }
            }
        }

        unsafe fn exact_str_val(&mut self, value: Val) -> R {
            match value {
                Val::Pure => Ok(()),
                Val::Obj(object) => {
                    self.require(ffi::PyUnicode_CheckExact(object) != 0, "operand not a str")?;
                    self.identify(object)
                }
                Val::Type(_) => self.uncert("operand not a str"),
            }
        }

        /// `None == value`: C only when `value`'s reflected comparison is
        /// one of CPython's builtin ones.
        unsafe fn none_eq_safe(&mut self, value: Val) -> R {
            match value {
                Val::Pure => Ok(()),
                Val::Type(_) => self.uncert("comparison with a type"),
                Val::Obj(object) => {
                    let type_ = self.type_of(object)?;
                    let info = self.type_guard(type_)?;
                    self.require(info.c_richcompare, "custom __eq__")
                }
            }
        }

        /// Record everything `repr(value)` reads. `value` is the root or
        /// was reached through guarded reads, so it is live.
        unsafe fn repr_dep(&mut self, value: P) -> R {
            if self.s.running.iter().any(|(set, _)| *set == value as usize) {
                return self.uncert("recursion guard set repr'd");
            }
            if ffi::Py_TYPE(value) == ptr::addr_of_mut!(ffi::PySet_Type) {
                self.s.repr_sets.push(value as usize);
            }
            if is_scalar(value) {
                self.identify(value)?;
                self.max_depth = self.max_depth.max(self.depth + 1);
                if ffi::Py_TYPE(value) == ptr::addr_of_mut!(ffi::PyLong_Type) {
                    return self.require(long_bits_at_most(value, 2000), "huge int");
                }
                return Ok(());
            }
            // Reused repr dependencies are recorded once, but their graph height still counts toward recursion.
            if let Some(height) = self.s.seen_reprs.get(&(value as usize)) {
                self.max_depth = self.max_depth.max(self.depth + 1 + *height);
                return self.require(self.depth + 1 + *height <= MAX_DEPTH, "graph too deep");
            }
            self.enter()?;
            let start_depth = self.depth;
            let outer_max = std::mem::replace(&mut self.max_depth, self.depth);
            let result = self.repr_dep_inner(value);
            let height = self.max_depth - start_depth;
            self.max_depth = self.max_depth.max(outer_max);
            self.leave();
            result?;
            self.s.seen_reprs.insert(value as usize, height);
            Ok(())
        }

        unsafe fn repr_dep_inner(&mut self, value: P) -> R {
            let type_ = ffi::Py_TYPE(value);
            if type_ == ptr::addr_of_mut!(ffi::PyTuple_Type) {
                self.identify(value)?;
                for index in 0..ffi::PyTuple_GET_SIZE(value) {
                    self.repr_dep(ffi::PyTuple_GET_ITEM(value, index))?;
                }
                return Ok(());
            }
            if type_ == ptr::addr_of_mut!(ffi::PyList_Type) {
                self.list_guard(value)?;
                for index in 0..ffi::PyList_GET_SIZE(value) {
                    self.repr_dep(ffi::PyList_GET_ITEM(value, index))?;
                }
                return Ok(());
            }
            if type_ == ptr::addr_of_mut!(ffi::PyDict_Type) {
                self.dict_version(value)?;
                let mut position = 0;
                let (mut key, mut item) = (ptr::null_mut(), ptr::null_mut());
                while ffi::PyDict_Next(value, &mut position, &mut key, &mut item) != 0 {
                    self.repr_dep(key)?;
                    self.repr_dep(item)?;
                }
                return Ok(());
            }
            if type_ == ptr::addr_of_mut!(ffi::PySet_Type) {
                self.identify(value)?;
                let items = set_items(value);
                self.guard(Guard::Set {
                    set: value,
                    items: items.clone().into(),
                })?;
                for item in items {
                    self.repr_dep(item as P)?;
                }
                return Ok(());
            }
            if type_ == ptr::addr_of_mut!(ffi::PyFrozenSet_Type) {
                self.identify(value)?;
                for item in set_items(value) {
                    self.repr_dep(item as P)?;
                }
                return Ok(());
            }
            if type_ == ptr::addr_of_mut!(ffi::PyFunction_Type) {
                self.identify(value)?;
                let qualname = self.field(
                    value,
                    ptr::addr_of!((*(value as *mut ffi::PyFunctionObject)).func_qualname),
                )?;
                return self.identify(qualname);
            }
            if type_ == ptr::addr_of_mut!(ffi::PyCFunction_Type)
                || type_ == ptr::addr_of_mut!(ffi::PyCMethod_Type)
            {
                self.identify(value)?;
                let raw = value as *mut ffi::PyCFunctionObject;
                self.field(value, ptr::addr_of!((*raw).m_ml) as *const P)?;
                let bound = self.field(value, ptr::addr_of!((*raw).m_self))?;
                if !bound.is_null() {
                    let bound_type = self.type_of(bound)?;
                    self.type_guard(bound_type)?;
                    self.type_names(bound_type)?;
                }
                return Ok(());
            }
            if type_ == method_type() {
                self.identify(value)?;
                let method = value as *mut MethodObject;
                let function = self.field(value, ptr::addr_of!((*method).im_func))?;
                self.require(
                    ffi::Py_TYPE(function) == ptr::addr_of_mut!(ffi::PyFunction_Type),
                    "method of a non-function",
                )?;
                self.identify(function)?;
                let qualname = self.field(
                    function,
                    ptr::addr_of!((*(function as *mut ffi::PyFunctionObject)).func_qualname),
                )?;
                self.identify(qualname)?;
                let bound_self = self.field(value, ptr::addr_of!((*method).im_self))?;
                return self.repr_dep(bound_self);
            }
            let type_ = self.type_of(value)?;
            self.type_guard(type_)?;
            let tp_repr = (*type_).tp_repr.map_or(0, |f| f as usize);
            if tp_repr == self.canon.type_repr {
                self.type_guard(value as T)?;
                return self.type_names(value as T);
            }
            if tp_repr == self.canon.object_repr {
                return self.type_names(type_);
            }
            self.require(tp_repr == self.canon.slot_tp_repr, "C repr")?;
            let function = _PyType_Lookup(type_, name!(self.py, "__repr__").as_ptr());
            self.require(!function.is_null(), "no __repr__")?;
            self.prove(function);
            self.repr_function(function, value)
        }

        /// Record what calling the Python `__repr__` `function` on `object`
        /// reads.
        unsafe fn repr_function(&mut self, function: P, object: P) -> R {
            self.enter()?;
            let result = self.repr_function_inner(function, object);
            self.leave();
            result
        }

        unsafe fn repr_function_inner(&mut self, function: P, object: P) -> R {
            let verdict = self.verdict(function)?;
            match &*verdict {
                Verdict::FString { uses_type, fields } => {
                    self.fstring(function, object, *uses_type, fields)
                }
                Verdict::DcWrapper312 { running, user } => {
                    let py = self.py;
                    self.global_is(function, name!(py, "id"), self.canon.builtin_id)?;
                    let thread = self.global(function, name!(py, "_thread"))?;
                    self.require(
                        thread as usize == self.canon.thread_module,
                        "_thread rebound",
                    )?;
                    let module_type = self.type_of(thread)?;
                    let dict = ffi::PyModule_GetDict(thread);
                    self.require(
                        module_type == ptr::addr_of_mut!(ffi::PyModule_Type)
                            && !dict.is_null()
                            && dict_lookup_safe(dict),
                        "_thread module",
                    )?;
                    let name = name!(py, "get_ident");
                    let key = (dict as usize, name.as_ptr() as usize);
                    if !self.s.seen_globals.iter().any(|(d, n, _)| (*d, *n) == key) {
                        self.prove(dict);
                        let get_ident = self.dict_item(dict, name.as_ptr())?;
                        self.require(
                            get_ident as usize == self.canon.get_ident,
                            "get_ident rebound",
                        )?;
                        self.s.seen_globals.push((key.0, key.1, get_ident));
                    }
                    self.wrapped_repr(function, *running, *user, object)
                }
                Verdict::RecursiveRepr { running, user } => {
                    let py = self.py;
                    self.global_is(function, name!(py, "id"), self.canon.builtin_id)?;
                    self.global_is(function, name!(py, "get_ident"), self.canon.get_ident)?;
                    self.wrapped_repr(function, *running, *user, object)
                }
                Verdict::NamedTupleRepr { fmt } => {
                    let class = self.class_of(object)?;
                    self.type_name(class, false)?;
                    let fmt = self.cell(function, *fmt)?;
                    self.require(ffi::PyUnicode_CheckExact(fmt) != 0, "format not a str")?;
                    self.identify(fmt)?;
                    let text =
                        Bound::from_borrowed_ptr(self.py, fmt).cast_into_unchecked::<PyString>();
                    let only_repr = text.to_str().is_ok_and(|text| {
                        let mut chars = text.chars();
                        while let Some(c) = chars.next() {
                            if c == '%' && !matches!(chars.next(), Some('r' | '%')) {
                                return false;
                            }
                        }
                        true
                    });
                    self.require(only_repr && ffi::PyTuple_Check(object) != 0, "format")?;
                    self.tuple_items(object)?;
                    for index in 0..ffi::PyTuple_GET_SIZE(object) {
                        self.repr_dep(ffi::PyTuple_GET_ITEM(object, index))?;
                    }
                    Ok(())
                }
                Verdict::JinjaContextRepr => self.jinja_context(function, object),
                Verdict::JinjaMacroRepr => {
                    let py = self.py;
                    self.global_is(
                        function,
                        name!(py, "type"),
                        ptr::addr_of_mut!(ffi::PyType_Type) as usize,
                    )?;
                    self.global_is(function, name!(py, "repr"), self.canon.builtin_repr)?;
                    let name = self.attr(object, name!(py, "name"))?;
                    self.repr_val(name)?;
                    let type_ = self.type_of(object)?;
                    self.type_name(type_, false)
                }
                Verdict::RichAutoRepr => self.rich_auto_repr(function, object),
                _ => self.uncert("not a repr"),
            }
        }

        /// The dataclass/`reprlib` recursion guard around `user_function`.
        unsafe fn wrapped_repr(
            &mut self,
            function: P,
            running: usize,
            user: usize,
            object: P,
        ) -> R {
            let running = self.cell(function, running)?;
            // Only certified when no repr of anything is running through
            // this wrapper on any thread; then `key in repr_running` is
            // False and the add/discard pair leaves membership unchanged.
            self.require(
                ffi::PySet_CheckExact(running) != 0 && ffi::PySet_Size(running) == 0,
                "recursive repr in progress",
            )?;
            self.require(
                !self.s.repr_sets.contains(&(running as usize)),
                "recursion guard set repr'd",
            )?;
            self.identify(running)?;
            self.guard(Guard::Word(
                ptr::addr_of!((*(running as *mut ffi::PySetObject)).used) as *const usize,
                0,
            ))?;
            let key = (running as usize, object as usize);
            self.require(!self.s.running.contains(&key), "shared recursion guard")?;
            let user = self.cell(function, user)?;
            self.s.running.push(key);
            let result = self.repr_function(user, object);
            self.s.running.pop();
            result
        }

        unsafe fn fstring(
            &mut self,
            function: P,
            object: P,
            uses_type: bool,
            fields: &[Field],
        ) -> R {
            if uses_type {
                self.global_is(
                    function,
                    name!(self.py, "type"),
                    ptr::addr_of_mut!(ffi::PyType_Type) as usize,
                )?;
            }
            for field in fields.iter() {
                let mut value = if field.type_root {
                    Val::Type(self.type_of(object)?)
                } else {
                    Val::Obj(object)
                };
                for index in field.names.iter() {
                    let name = self.code_name(function, *index)?;
                    value = self.attr_val(value, &name)?;
                }
                match field.conv {
                    CONV_REPR => self.repr_val(value)?,
                    CONV_FORMAT | CONV_STR => self.str_val(value)?,
                    _ => self.exact_str_val(value)?,
                }
            }
            Ok(())
        }

        unsafe fn jinja_context(&mut self, function: P, object: P) -> R {
            let py = self.py;
            let dict_type = ptr::addr_of_mut!(ffi::PyDict_Type) as usize;
            self.global_is(
                function,
                name!(py, "type"),
                ptr::addr_of_mut!(ffi::PyType_Type) as usize,
            )?;
            let type_ = self.type_of(object)?;
            self.type_name(type_, false)?;
            let get_all = self.method(object, name!(py, "get_all"))?;
            let verdict = self.verdict(get_all)?;
            self.require(matches!(*verdict, Verdict::JinjaGetAll), "get_all")?;
            self.global_is(get_all, name!(py, "dict"), dict_type)?;
            let Val::Obj(vars) = self.attr(object, name!(py, "vars"))? else {
                return self.uncert("context vars");
            };
            let Val::Obj(parent) = self.attr(object, name!(py, "parent"))? else {
                return self.uncert("context parent");
            };
            self.require(exact_dict(vars) && exact_dict(parent), "context dicts")?;
            self.dict_version(vars)?;
            self.dict_version(parent)?;
            let (vars_len, parent_len) = (ffi::PyDict_Size(vars), ffi::PyDict_Size(parent));
            if vars_len == 0 {
                self.repr_dep(parent)?;
            } else if parent_len == 0 {
                self.repr_dep(vars)?;
            } else {
                for dict in [parent, vars] {
                    let mut position = 0;
                    let (mut key, mut item) = (ptr::null_mut(), ptr::null_mut());
                    while ffi::PyDict_Next(dict, &mut position, &mut key, &mut item) != 0 {
                        self.require(ffi::PyUnicode_CheckExact(key) != 0, "non-str context key")?;
                    }
                }
                self.repr_dep(parent)?;
                self.repr_dep(vars)?;
            }
            let name = self.attr(object, name!(py, "name"))?;
            self.repr_val(name)
        }

        unsafe fn rich_auto_repr(&mut self, function: P, object: P) -> R {
            let py = self.py;
            self.global_is(function, name!(py, "getattr"), self.canon.builtin_getattr)?;
            self.global_is(
                function,
                name!(py, "isinstance"),
                self.canon.builtin_isinstance,
            )?;
            self.global_is(
                function,
                name!(py, "tuple"),
                ptr::addr_of_mut!(ffi::PyTuple_Type) as usize,
            )?;
            self.global_is(function, name!(py, "len"), self.canon.builtin_len)?;
            self.global_is(function, name!(py, "repr"), self.canon.builtin_repr)?;
            let rich_repr = self.method(object, name!(py, "__rich_repr__"))?;
            let attributes = self.field(
                rich_repr,
                ptr::addr_of!((*(rich_repr as *mut ffi::PyFunctionObject)).func_dict),
            )?;
            if !attributes.is_null() {
                let angular = self.dict_item(attributes, name!(py, "angular").as_ptr())?;
                self.require(
                    angular.is_null()
                        || angular == ffi::Py_True()
                        || angular == ffi::Py_False(),
                    "angular",
                )?;
            }
            let class = self.class_of(object)?;
            self.type_name(class, false)?;
            let verdict = self.verdict(rich_repr)?;
            match *verdict {
                Verdict::RichStyleRichRepr => {
                    for name in [
                        name!(py, "color"),
                        name!(py, "bgcolor"),
                        name!(py, "bold"),
                        name!(py, "dim"),
                        name!(py, "italic"),
                        name!(py, "underline"),
                        name!(py, "blink"),
                        name!(py, "blink2"),
                        name!(py, "reverse"),
                        name!(py, "conceal"),
                        name!(py, "strike"),
                        name!(py, "underline2"),
                        name!(py, "frame"),
                        name!(py, "encircle"),
                        name!(py, "link"),
                    ] {
                        let value = self.attr(object, name)?;
                        self.keyed_item(value)?;
                    }
                    let meta = self.attr(object, name!(py, "_meta"))?;
                    let falsy = match meta {
                        Val::Obj(meta) => {
                            self.identify(meta)?;
                            meta == ffi::Py_None()
                                || ffi::PyBytes_CheckExact(meta) != 0
                                    && ffi::PyBytes_Size(meta) == 0
                        }
                        _ => false,
                    };
                    self.require(falsy, "style meta")
                }
                Verdict::RichColorRichRepr => {
                    let value = self.attr(object, name!(py, "name"))?;
                    self.single_item(value)?;
                    let value = self.attr(object, name!(py, "type"))?;
                    self.single_item(value)?;
                    let value = self.attr(object, name!(py, "number"))?;
                    self.keyed_item(value)?;
                    let value = self.attr(object, name!(py, "triplet"))?;
                    self.keyed_item(value)
                }
                _ => self.uncert("unsupported __rich_repr__"),
            }
        }

        /// A `yield "key", value, None` item of `__rich_repr__`.
        unsafe fn keyed_item(&mut self, value: Val) -> R {
            self.none_eq_safe(value)?;
            self.repr_val(value)
        }

        /// A `yield value` item of `__rich_repr__`, as `auto_repr` handles it.
        unsafe fn single_item(&mut self, value: Val) -> R {
            let Val::Obj(object) = value else {
                return match value {
                    Val::Pure => Ok(()),
                    _ => self.uncert("yielded a type"),
                };
            };
            let type_ = self.type_of(object)?;
            if ffi::PyTuple_Check(object) == 0 {
                let info = self.type_guard(type_)?;
                self.require(
                    info.generic_getattro && info.default_class,
                    "custom __class__",
                )?;
                return self.repr_dep(object);
            }
            self.require(
                type_ == ptr::addr_of_mut!(ffi::PyTuple_Type),
                "tuple subclass item",
            )?;
            self.tuple_items(object)?;
            let len = ffi::PyTuple_GET_SIZE(object);
            if len == 1 {
                return self.repr_dep(ffi::PyTuple_GET_ITEM(object, 0));
            }
            self.require(len >= 2, "empty tuple item")?;
            let key = ffi::PyTuple_GET_ITEM(object, 0);
            let value = ffi::PyTuple_GET_ITEM(object, 1);
            if key != ffi::Py_None() {
                self.require(ffi::PyUnicode_CheckExact(key) != 0, "non-str key")?;
                self.identify(key)?;
                if len >= 3 {
                    let default = ffi::PyTuple_GET_ITEM(object, 2);
                    self.require(default == ffi::Py_None(), "non-None default")?;
                    self.none_eq_safe(Val::Obj(value))?;
                }
            }
            self.repr_dep(value)
        }
    }

    /// The code of `type(object).__repr__` when it is a Python function,
    /// looked up only through MRO dicts whose keys cannot run `__eq__`.
    unsafe fn root_code(py: Python<'_>, object: P) -> Option<(usize, usize)> {
        let type_ = ffi::Py_TYPE(object);
        let mro = (*type_).tp_mro;
        if mro.is_null() || ffi::PyTuple_CheckExact(mro) == 0 {
            return None;
        }
        for index in 0..ffi::PyTuple_GET_SIZE(mro) {
            let base = ffi::PyTuple_GET_ITEM(mro, index) as T;
            if (*base).tp_flags & ffi::Py_TPFLAGS_HEAPTYPE != 0 {
                let dict = (*base).tp_dict;
                if dict.is_null() || !exact_dict(dict) || !dict_lookup_safe(dict) {
                    return None;
                }
            }
        }
        let function = _PyType_Lookup(type_, name!(py, "__repr__").as_ptr());
        if function.is_null() || ffi::Py_TYPE(function) != ptr::addr_of_mut!(ffi::PyFunction_Type) {
            return None;
        }
        Some((
            function as usize,
            (*(function as *mut ffi::PyFunctionObject)).func_code as usize,
        ))
    }

    /// Whether the real repr would run in a neutral context: no container
    /// repr in progress on this thread, and enough recursion budget for a
    /// graph of `depth` levels.
    unsafe fn context_ok(py: Python<'_>, depth: u32) -> bool {
        let tstate = ffi::PyThreadState_Get() as *const ThreadStatePrefix;
        let need = i64::from(depth) * RECURSION_PER_LEVEL + RECURSION_SLACK;
        if i64::from((*tstate).py_recursion_remaining) < need {
            return false;
        }
        #[cfg(not(Py_3_14))]
        if i64::from((*tstate).c_recursion_remaining) < need {
            return false;
        }
        #[cfg(Py_3_14)]
        {
            let bytes = need * STACK_BYTES_PER_LEVEL;
            let units = (bytes + STACK_MARGIN_UNIT_BYTES - 1) / STACK_MARGIN_UNIT_BYTES;
            let units = units.min(i64::from(c_int::MAX)) as c_int;
            if _Py_ReachedRecursionLimitWithMargin(ffi::PyThreadState_Get(), units) != 0 {
                return false;
            }
        }
        let dict = ffi::PyThreadState_GetDict();
        if dict.is_null() {
            return true;
        }
        if !exact_dict(dict) || !dict_lookup_safe(dict) {
            return false;
        }
        let list = ffi::PyDict_GetItemWithError(dict, name!(py, "Py_Repr").as_ptr());
        if list.is_null() {
            if !ffi::PyErr_Occurred().is_null() {
                ffi::PyErr_Clear();
                return false;
            }
            return true;
        }
        ffi::PyList_CheckExact(list) != 0 && ffi::PyList_GET_SIZE(list) == 0
    }

    const MAX_ENTRIES: usize = 8192;
    const MAX_RESIDENT_WORDS: usize = 1 << 22;
    /// Larger entries (a megabyte of text and copies) are not kept.
    const MAX_ENTRY_WORDS: usize = 1 << 17;
    const MAX_NEGATIVE: usize = 16384;

    /// A cached repr of whatever object lives at its key's address. It
    /// holds no reference to that object or anything it reads: the guards
    /// are validated from the live root (see `Guard`).
    struct Entry {
        text: Py<PyString>,
        guards: Box<[Guard]>,
        depth: u32,
        cost_ns: u64,
        last_used: u64,
        /// `entry_words`, counted against `MAX_RESIDENT_WORDS`.
        words: usize,
        /// Whether a second real repr, run while the guards still held,
        /// returned the same text. Guards are recorded before the real repr
        /// runs; if another thread (or a signal handler or finalizer)
        /// changes a dependency while it runs and restores it before the
        /// next event, the text shows the temporary state although every
        /// guard holds. Only a confirmed entry is reused.
        confirmed: bool,
    }

    impl Entry {
        fn resident(&self) -> usize {
            self.words
        }
    }

    /// Words an entry keeps resident: its guards, the copies they hold and
    /// the cached text (str sizes are bounded by 4 bytes per character).
    fn entry_words(text: &Py<PyString>, guards: &[Guard]) -> usize {
        // Safety: Kolo's own exact str objects.
        let str_words = |object: P| unsafe { ffi::PyUnicode_GetLength(object).max(0) as usize / 2 };
        let copies: usize = guards
            .iter()
            .map(|guard| match guard {
                Guard::Str { copy, .. } => str_words(copy.as_ptr()),
                Guard::Bytes { data, .. } => data.len() / 8,
                Guard::Int { .. } => (2000 / 30 + 1) * 4 / 8 + 4,
                Guard::Tuple { items, .. }
                | Guard::List { items, .. }
                | Guard::Set { items, .. }
                | Guard::DictItems { items, .. } => items.len(),
                _ => 0,
            })
            .sum();
        guards.len() * 4 + copies + str_words(text.as_ptr())
    }

    #[derive(Default)]
    struct Cache {
        entries: HashMap<usize, Entry>,
        resident: usize,
        clock: u64,
        /// Objects that recently failed certification, by (address, type),
        /// with exponential backoff: their state may still change (objects
        /// are often repr'd while `__init__` is still filling them in), so
        /// they are retried, just not on every repr. Unpinned on purpose: a
        /// stale key only delays caching for a new object at that address.
        negative: HashMap<(usize, usize), Backoff>,
        /// Types whose `__repr__` code is refused, with the type's
        /// `tp_version_tag` and that function and its code: an unchanged tag
        /// means the same function, and the same code has the same verdict
        /// (`__code__` can be assigned without changing the tag).
        refused_types: HashMap<usize, (u32, usize, usize)>,
        types: HashMap<usize, TypeInfo>,
        pending: Vec<Py<PyAny>>,
        scratch: Scratch,
        /// `ReprReuse::generation` this cache's entries belong to.
        generation: u64,
    }

    #[derive(Clone, Copy)]
    struct Backoff {
        strikes: u8,
        wait: u16,
    }

    impl Cache {
        fn strike(&mut self, object: P) {
            // Safety: reads a live object's type.
            let key = (object as usize, unsafe { ffi::Py_TYPE(object) } as usize);
            if self.negative.len() >= MAX_NEGATIVE && !self.negative.contains_key(&key) {
                self.negative.clear();
            }
            let backoff = self.negative.entry(key).or_insert(Backoff {
                strikes: 0,
                wait: 0,
            });
            backoff.strikes = backoff.strikes.saturating_add(1);
            backoff.wait = 1u16 << backoff.strikes.min(6);
        }

        fn evict(&mut self, graveyard: &mut Vec<Entry>) {
            if self.entries.len() < MAX_ENTRIES && self.resident < MAX_RESIDENT_WORDS {
                return;
            }
            let mut ages: Vec<(u64, usize)> = self
                .entries
                .iter()
                .map(|(key, entry)| (entry.last_used, *key))
                .collect();
            ages.sort_unstable();
            let quarter = ages.len() / 4 + 1;
            for (index, (_, key)) in ages.iter().enumerate() {
                if index >= quarter
                    && self.entries.len() < MAX_ENTRIES
                    && self.resident < MAX_RESIDENT_WORDS
                {
                    break;
                }
                if let Some(entry) = self.entries.remove(key) {
                    self.resident -= entry.resident();
                    graveyard.push(entry);
                }
            }
            bump(&counters().evicted, graveyard.len() as u64);
        }
    }

    /// Per-monitor repr reuse state; one cache per thread.
    pub struct ReprReuse {
        threads: ThreadLocal<RefCell<Cache>>,
        /// Bumped when the monitor stops: every thread's cache drops its
        /// entries before its next use.
        generation: AtomicU64,
    }

    impl Default for ReprReuse {
        fn default() -> Self {
            Self {
                threads: ThreadLocal::new(),
                generation: AtomicU64::new(0),
            }
        }
    }

    enum Lookup {
        Hit(Py<PyString>, u64),
        /// Run the real repr and (re)record; carries a failed entry, dropped
        /// outside the cache borrow.
        Miss(Option<Entry>),
        Skip,
    }

    impl ReprReuse {
        /// Release every entry when a session ends. The calling thread's
        /// cache is cleared now, other threads' on their next use.
        pub fn release(&self) {
            self.generation.fetch_add(1, Ordering::Relaxed);
            if let Some(cell) = self.threads.get() {
                let entries = match cell.try_borrow_mut() {
                    Ok(mut cache) => {
                        cache.resident = 0;
                        cache.negative.clear();
                        cache.types.clear();
                        cache.refused_types.clear();
                        std::mem::take(&mut cache.entries)
                    }
                    Err(_) => return,
                };
                drop(entries);
            }
        }

        /// `PyObject_Repr(value)`, reusing a certified earlier result.
        pub fn repr<'py>(&self, value: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyString>> {
            if !STATS.load(Ordering::Relaxed) {
                return self.repr_inner(value, &mut Outcome::NotPython);
            }
            let start = Instant::now();
            let mut outcome = Outcome::NotPython;
            let result = self.repr_inner(value, &mut outcome);
            let elapsed = start.elapsed().as_nanos() as u64;
            if !matches!(outcome, Outcome::NotPython) {
                // Safety: reads a live object's static type name.
                let name = unsafe {
                    std::ffi::CStr::from_ptr((*ffi::Py_TYPE(value.as_ptr())).tp_name)
                        .to_string_lossy()
                        .into_owned()
                };
                let mut guard = PER_TYPE.lock().expect("poisoned");
                let row = guard
                    .get_or_insert_with(Default::default)
                    .entry(name)
                    .or_insert([0; PER_TYPE_COLUMNS]);
                let column = outcome.column();
                row[2 * column] += 1;
                row[2 * column + 1] += elapsed;
                if let Outcome::Hit(cost) = outcome {
                    row[2 * PER_TYPE_OUTCOMES] += cost;
                }
            }
            result
        }

        fn repr_inner<'py>(
            &self,
            value: &Bound<'py, PyAny>,
            outcome: &mut Outcome,
        ) -> PyResult<Bound<'py, PyString>> {
            let py = value.py();
            if !ENABLED.load(Ordering::Relaxed) {
                return value.repr();
            }
            let object = value.as_ptr();
            // Safety: reads a live object's type slots.
            let python_repr = unsafe { (*ffi::Py_TYPE(object)).tp_repr.map_or(0, |f| f as usize) };
            let Some(canon) = canon(py) else {
                return value.repr();
            };
            if python_repr != canon.slot_tp_repr || !eval_frame_ok(py, canon) {
                return value.repr();
            }
            let stats = STATS.load(Ordering::Relaxed);
            let verify = VERIFY.load(Ordering::Relaxed);
            let counters = counters();
            bump(&counters.python_reprs, 1);
            *outcome = Outcome::Skip;
            let cell = self.threads.get_or_default();
            let mut graveyard = Vec::new();
            let generation = self.generation.load(Ordering::Relaxed);
            if let Ok(mut cache) = cell.try_borrow_mut() {
                if cache.generation != generation {
                    cache.generation = generation;
                    cache.resident = 0;
                    cache.negative.clear();
                    cache.types.clear();
                    cache.refused_types.clear();
                    graveyard.extend(std::mem::take(&mut cache.entries).into_values());
                }
            }
            let lookup = match cell.try_borrow_mut() {
                Ok(mut cache) => self.lookup(py, &mut cache, object, stats),
                Err(_) => Lookup::Skip,
            };
            match lookup {
                Lookup::Hit(text, cost) => {
                    bump(&counters.hits, 1);
                    bump(&counters.avoided_ns, cost);
                    *outcome = Outcome::Hit(cost);
                    if verify {
                        bump(&counters.verify_checks, 1);
                        let repr_start = Instant::now();
                        let real = value.repr();
                        bump(
                            &counters.verify_repr_ns,
                            repr_start.elapsed().as_nanos() as u64,
                        );
                        let equal = match &real {
                            // Safety: both are str objects.
                            Ok(real) => {
                                real.is_exact_instance_of::<PyString>()
                                    && unsafe {
                                        ffi::PyUnicode_Compare(real.as_ptr(), text.as_ptr())
                                    } == 0
                            }
                            Err(_) => false,
                        };
                        if !equal {
                            bump(&counters.verify_mismatches, 1);
                            let shown = match &real {
                                Ok(real) => format!("{:?}", truncate(&real.to_string_lossy())),
                                Err(error) => format!("raised {error}"),
                            };
                            let message = format!(
                                "{}: cached {:?} != real {}",
                                value
                                    .get_type()
                                    .name()
                                    .map(|n| n.to_string())
                                    .unwrap_or_default(),
                                truncate(&text.bind(py).to_string_lossy()),
                                shown,
                            );
                            eprintln!("kolo repr reuse MISMATCH {message}");
                            if let Some(path) = std::env::var_os("KOLO_REPR_REUSE_VERIFY_LOG") {
                                use std::io::Write;
                                if let Ok(mut log) = std::fs::OpenOptions::new()
                                    .create(true)
                                    .append(true)
                                    .open(path)
                                {
                                    let _ = writeln!(log, "{message}");
                                }
                            }
                            let mut examples = MISMATCHES.lock().expect("poisoned");
                            if examples.len() < 20 {
                                examples.push(message);
                            }
                            drop(examples);
                            if let Ok(mut cache) = cell.try_borrow_mut() {
                                if let Some(entry) = cache.entries.remove(&(object as usize)) {
                                    cache.resident -= entry.resident();
                                    graveyard.push(entry);
                                }
                            }
                            drop(graveyard);
                        }
                        return real;
                    }
                    return Ok(text.into_bound(py));
                }
                Lookup::Skip => return value.repr(),
                Lookup::Miss(failed) => {
                    *outcome = if failed.is_some() {
                        Outcome::Deopt
                    } else {
                        Outcome::Miss
                    };
                    drop(failed)
                }
            }
            let record_start = Instant::now();
            let snapshot = match cell.try_borrow_mut() {
                Ok(mut cache) => self.record(py, canon, &mut cache, object, stats),
                Err(_) => None,
            };
            let record_ns = record_start.elapsed().as_nanos() as u64;
            let repr_start = Instant::now();
            let text = value.repr();
            let cost_ns = repr_start.elapsed().as_nanos() as u64;
            if let Ok(mut cache) = cell.try_borrow_mut() {
                bump(&counters.record_ns, record_ns);
                if let (Some((guards, depth)), Ok(text)) = (snapshot, &text) {
                    bump(&counters.miss_repr_ns, cost_ns);
                    // Only exact str results are reused (a str subclass's own
                    // methods would run on every use of a fresh repr).
                    if !text.is_exact_instance_of::<PyString>() {
                        bump(&counters.cheap_skips, 1);
                        cache.strike(object);
                    } else if !unsafe {
                        let _no_gc = NoGc::new();
                        all_hold(&guards)
                    } {
                        bump(&counters.changed_during_repr, 1);
                        cache.strike(object);
                    } else if let Some(copy) = unsafe {
                        // Kolo's own copy: the result may be the program's
                        // own string (`return self.name`), which the entry
                        // must not keep alive.
                        let copy = copy_str(text.as_ptr());
                        (!copy.is_null()).then(|| {
                            Bound::from_owned_ptr(py, copy)
                                .cast_into_unchecked::<PyString>()
                                .unbind()
                        })
                    } {
                        let previous = cache.entries.remove(&(object as usize));
                        let confirmed = previous.as_ref().is_some_and(|old| unsafe {
                            ffi::PyUnicode_Compare(old.text.as_ptr(), copy.as_ptr()) == 0
                        });
                        if let Some(old) = previous {
                            cache.resident -= old.resident();
                            graveyard.push(old);
                        }
                        let words = entry_words(&copy, &guards);
                        if words > MAX_ENTRY_WORDS {
                            bump(&counters.oversized, 1);
                            cache.strike(object);
                        } else {
                            cache.clock += 1;
                            let entry = Entry {
                                words,
                                text: copy,
                                guards: guards.into(),
                                depth,
                                cost_ns,
                                last_used: cache.clock,
                                confirmed,
                            };
                            cache.resident += entry.resident();
                            cache.entries.insert(object as usize, entry);
                            bump(&counters.inserted, 1);
                            cache.evict(&mut graveyard);
                        }
                    } else {
                        cache.strike(object);
                    }
                } else {
                    bump(&counters.uncert_repr_ns, cost_ns);
                }
                let pending = std::mem::take(&mut cache.pending);
                drop(cache);
                if !pending.is_empty() {
                    self.audit(py, canon, cell, pending)?;
                }
            }
            drop(graveyard);
            text
        }

        fn lookup(&self, py: Python<'_>, cache: &mut Cache, object: P, stats: bool) -> Lookup {
            let counters = counters();
            let Some(mut entry) = cache.entries.remove(&(object as usize)) else {
                let key = (object as usize, unsafe { ffi::Py_TYPE(object) } as usize);
                if let Some(backoff) = cache.negative.get_mut(&key) {
                    if backoff.wait > 0 {
                        backoff.wait -= 1;
                        bump(&counters.negative_skips, 1);
                        return Lookup::Skip;
                    }
                }
                // Safety: reads a live object's type and its tag.
                let (type_, tag) = unsafe {
                    let type_ = ffi::Py_TYPE(object);
                    (type_ as usize, (*type_).tp_version_tag)
                };
                if tag != 0 {
                    if let Some(&(seen, function, code)) = cache.refused_types.get(&type_) {
                        // Safety: an unchanged tag keeps `function` in the
                        // type's dict, so it is alive.
                        if seen == tag
                            && unsafe {
                                (*(function as *mut ffi::PyFunctionObject)).func_code as usize
                            } == code
                        {
                            bump(&counters.negative_skips, 1);
                            return Lookup::Skip;
                        }
                    }
                }
                // The lookup happens before taking the lock (only through str-keyed dicts),
                // so no Python code runs while it is held. Safety: GIL held; reads a live type and its MRO dicts.
                let root = unsafe { root_code(py, object) };
                let rejected = root.is_some_and(|(_, code)| {
                    VERDICTS
                        .lock()
                        .expect("poisoned")
                        .as_ref()
                        .is_some_and(|verdicts| {
                            verdicts.get(&code).is_some_and(|slot| {
                                slot.verdict.is_none() && unsafe { slot.is_for(code as P) }
                            })
                        })
                });
                if rejected {
                    if let (true, Some((function, code))) = (tag != 0, root) {
                        if cache.refused_types.len() >= MAX_NEGATIVE {
                            cache.refused_types.clear();
                        }
                        cache.refused_types.insert(type_, (tag, function, code));
                    }
                    bump(&counters.negative_skips, 1);
                    return Lookup::Skip;
                }
                bump(&counters.misses, 1);
                return Lookup::Miss(None);
            };
            let start = stats.then(Instant::now);
            // Safety: GIL held; validation runs no Python.
            let valid = unsafe {
                if !context_ok(py, entry.depth) {
                    bump(&counters.context_refusals, 1);
                    cache.entries.insert(object as usize, entry);
                    return Lookup::Skip;
                }
                let _no_gc = NoGc::new();
                all_hold(&entry.guards)
            };
            let elapsed = start.map_or(0, |start| start.elapsed().as_nanos() as u64);
            if valid && !entry.confirmed {
                bump(&counters.confirmations, 1);
                cache.entries.insert(object as usize, entry);
                Lookup::Miss(None)
            } else if valid {
                bump(&counters.hit_validate_ns, elapsed);
                cache.clock += 1;
                entry.last_used = cache.clock;
                let result = Lookup::Hit(entry.text.clone_ref(py), entry.cost_ns);
                cache.entries.insert(object as usize, entry);
                result
            } else {
                bump(&counters.deopt_validate_ns, elapsed);
                bump(&counters.deopts, 1);
                cache.resident -= entry.resident();
                Lookup::Miss(Some(entry))
            }
        }

        fn record(
            &self,
            py: Python<'_>,
            canon: &Canon,
            cache: &mut Cache,
            object: P,
            stats: bool,
        ) -> Option<(Vec<Guard>, u32)> {
            let counters = counters();
            // Safety: GIL held; recording runs no Python.
            unsafe {
                if !context_ok(py, 0) {
                    bump(&counters.context_refusals, 1);
                    return None;
                }
                let _no_gc = NoGc::new();
                let mut verdicts = VERDICTS.lock().expect("poisoned");
                let verdicts = &*verdicts.get_or_insert_with(HashMap::new);
                let mut rec = new_rec(py, canon, verdicts, cache);
                match rec.repr_dep(object) {
                    Ok(()) => Some((rec.guards, rec.max_depth)),
                    Err(Stop::Audit) => {
                        bump(&counters.pending_audits, 1);
                        None
                    }
                    Err(_) => {
                        bump(&counters.uncertifiable, 1);
                        if stats {
                            note_reason(py, object, rec.why);
                        }
                        cache.strike(object);
                        None
                    }
                }
            }
        }

        /// Classify code objects met while recording. Runs Python, so only
        /// outside any snapshot/repr window.
        /// A `BaseException` such as `KeyboardInterrupt` raised while
        /// classifying is returned (the program gets it); other failures
        /// leave the code uncertified.
        fn audit(
            &self,
            py: Python<'_>,
            canon: &Canon,
            cell: &RefCell<Cache>,
            pending: Vec<Py<PyAny>>,
        ) -> PyResult<()> {
            let classify = canon.classify.bind(py);
            let mut verdicts = Vec::with_capacity(pending.len());
            for weakref in pending {
                // Safety: Kolo's own weak reference.
                let code = unsafe { weak_target(weakref.as_ptr()) };
                if code == 0 {
                    continue;
                }
                // Safety: the code object is alive (held by its function).
                let code_object = unsafe { Bound::from_borrowed_ptr(py, code as P) };
                let verdict = match classify
                    .call1((code_object.clone(),))
                    .and_then(|result| parse_verdict(&result, &code_object))
                {
                    Ok(verdict) => verdict,
                    Err(error) if !error.is_instance_of::<pyo3::exceptions::PyException>(py) => {
                        return Err(error);
                    }
                    Err(_) => None,
                };
                verdicts.push((code, weakref, verdict));
            }
            {
                let mut global = VERDICTS.lock().expect("poisoned");
                let global = global.get_or_insert_with(HashMap::new);
                if global.len() >= MAX_VERDICTS {
                    // Safety: Kolo's own weak references; no Python runs.
                    global.retain(|code, slot| unsafe { slot.is_for(*code as P) });
                }
                for (code, weakref, verdict) in verdicts {
                    // Safety: as above.
                    if unsafe { weak_target(weakref.as_ptr()) } != code {
                        continue;
                    }
                    let current = global
                        .get(&code)
                        .is_some_and(|slot| unsafe { slot.is_for(code as P) });
                    if !current {
                        global.insert(
                            code,
                            VerdictSlot {
                                weakref,
                                verdict: verdict.map(Arc::new),
                            },
                        );
                    }
                }
            }
            if let Ok(mut cache) = cell.try_borrow_mut() {
                cache.negative.clear();
            }
            Ok(())
        }
    }

    fn truncate(text: &str) -> String {
        if text.len() <= 400 {
            return text.to_owned();
        }
        let mut end = 400;
        while !text.is_char_boundary(end) {
            end -= 1;
        }
        format!("{}...", &text[..end])
    }
}

#[cfg(not(all(Py_3_12, not(Py_GIL_DISABLED), not(PyPy))))]
mod imp {
    use super::*;
    use pyo3::types::PyDict;

    /// Repr reuse is only implemented for CPython 3.12+ with the GIL.
    #[derive(Default)]
    pub struct ReprReuse;

    impl ReprReuse {
        pub fn release(&self) {}

        pub fn repr<'py>(&self, value: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyString>> {
            value.repr()
        }
    }

    pub fn configure(_enabled: Option<bool>, _verify: Option<bool>, _stats: Option<bool>) {}

    /// Nothing to import: repr reuse is compiled out.
    pub fn preload(_py: Python<'_>) -> PyResult<()> {
        Ok(())
    }

    pub fn stats(py: Python<'_>, _reset: bool) -> PyResult<Bound<'_, PyDict>> {
        let dict = PyDict::new(py);
        dict.set_item("enabled", false)?;
        Ok(dict)
    }
}
