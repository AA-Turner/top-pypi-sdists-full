//! Objects whose constructor is still running, which the encoder must not
//! `repr()` (see `kolo._construction` for why, and for the rules).
//!
//! `kolo._construction.objects_under_construction` is the reference: it walks
//! `frame.f_back` and decides every case. Walking a deep stack in Python for
//! each event would cost far more than the event itself, and a long-lived
//! constructor is common (`socketserver` handles a whole request inside
//! `BaseRequestHandler.__init__`), so `native::walk` answers the usual stack
//! itself: it follows the interpreter's own frame chain and reads each
//! constructor's first local. It declines, and the reference decides, when a
//! `__new__` is running (whose arguments need its bytecode).
//!
//! The native walk reads private CPython structures. It runs only on the
//! releases whose layout it knows, finds `co_name` in the code object by
//! looking for it, and is used only after it has agreed with the reference
//! on every constructor shape in this process (`probe_native_walk`).
//! `KOLO_CONSTRUCTION_NATIVE=0` keeps it from ever running.

use pyo3::ffi;
use pyo3::prelude::*;
use std::sync::atomic::{AtomicBool, Ordering};

/// `KOLO_CONSTRUCTION_CHECK=0`: nothing is looked for, and no placeholder
/// recorded. `KOLO_CONSTRUCTION_NATIVE=0`: the reference decides every
/// stack. Both are read once, when `kolo._kolo` is imported.
static CHECK_OFF: AtomicBool = AtomicBool::new(false);
static NATIVE_OFF: AtomicBool = AtomicBool::new(false);

pub fn read_switches() {
    let off = |name: &str| std::env::var_os(name).is_some_and(|value| value == "0");
    CHECK_OFF.store(off("KOLO_CONSTRUCTION_CHECK"), Ordering::Relaxed);
    NATIVE_OFF.store(off("KOLO_CONSTRUCTION_NATIVE"), Ordering::Relaxed);
}

fn native_walk(py: Python<'_>) -> PyResult<Option<Vec<usize>>> {
    if NATIVE_OFF.load(Ordering::Relaxed) {
        return Ok(None);
    }
    native::walk(py)
}

/// `objects_under_construction()`'s flat list: `[n, object * n, (class,
/// returning, k, argument * k) * m]`, or empty when there is nothing.
pub(super) struct UnderConstruction(Vec<usize>);

impl UnderConstruction {
    /// Whether no value can be under construction: the answer for nearly
    /// every event.
    #[inline]
    pub(super) fn is_empty(&self) -> bool {
        self.0.len() <= 1
    }

    /// `kolo._construction.is_under_construction`.
    pub(super) fn contains(&self, object: *mut ffi::PyObject) -> bool {
        let found = &self.0;
        if found.len() <= 1 {
            return false;
        }
        let object_id = object as usize;
        let objects_end = found[0].saturating_add(1).min(found.len());
        if found[1..objects_end].contains(&object_id) {
            return true;
        }
        // Safety: reads a live object's type.
        let class = unsafe { ffi::Py_TYPE(object) };
        let mut start = objects_end;
        while start + 2 < found.len() {
            let end = found[start + 2].saturating_add(start + 3).min(found.len());
            if !found[start + 3..end].contains(&object_id) {
                // Safety: `PyType_IsSubtype` only compares its second
                // argument with the types in the first one's MRO; it is a
                // class the running `__new__` holds.
                let instance = unsafe {
                    ffi::PyType_IsSubtype(class, found[start] as *mut ffi::PyTypeObject) != 0
                };
                // A returning `__new__` leaves the object to its `__init__`.
                if instance && !(found[start + 1] != 0 && inherits_object_init(class)) {
                    return true;
                }
            }
            start = end;
        }
        false
    }
}

/// Whether no `__init__` runs on instances of `class` (`tp_init` is
/// `object`'s).
#[cfg(not(any(PyPy, GraalPy)))]
fn inherits_object_init(class: *mut ffi::PyTypeObject) -> bool {
    // Safety: reads a live type object and a static type.
    unsafe {
        (*class).tp_init.map(|slot| slot as usize)
            == (*std::ptr::addr_of!(ffi::PyBaseObject_Type))
                .tp_init
                .map(|slot| slot as usize)
    }
}

/// Type slots say less on these interpreters: assume one does.
#[cfg(any(PyPy, GraalPy))]
fn inherits_object_init(_class: *mut ffi::PyTypeObject) -> bool {
    false
}

/// A first, cheap answer to `may_run_user_code` for the hook's hot path.
/// `falls_through` is the value serializer's cached verdict that the hook's
/// ladder matches nothing for this type and that reading `__class__` runs
/// no code: such a value is only ever `repr()`'d, which is safe when the
/// repr is `object`'s.
#[cfg(not(any(PyPy, GraalPy)))]
#[inline(always)]
pub(super) fn worth_checking(
    object: *mut ffi::PyObject,
    falls_through: bool,
    lightweight_repr: bool,
    method_type: usize,
) -> bool {
    // Safety: reads a live object's type and a static type.
    unsafe {
        let class = ffi::Py_TYPE(object);
        if class as usize == method_type {
            return !lightweight_repr;
        }
        if ffi::PyType_HasFeature(class, ffi::Py_TPFLAGS_HEAPTYPE) == 0 {
            return false;
        }
        // `lightweight_repr`, which is not the hot configuration, always
        // takes the full look at the type.
        lightweight_repr
            || !(falls_through
                && (*class).tp_repr.map(|slot| slot as usize)
                    == (*std::ptr::addr_of!(ffi::PyBaseObject_Type))
                        .tp_repr
                        .map(|slot| slot as usize))
    }
}

#[cfg(any(PyPy, GraalPy))]
#[inline(always)]
pub(super) fn worth_checking(
    _object: *mut ffi::PyObject,
    _falls_through: bool,
    _lightweight_repr: bool,
    _method_type: usize,
) -> bool {
    true
}

#[cfg(not(any(PyPy, GraalPy)))]
extern "C" {
    // As in the value serializer: borrowed, and only compared by address.
    fn _PyType_Lookup(
        type_: *mut ffi::PyTypeObject,
        name: *mut ffi::PyObject,
    ) -> *mut ffi::PyObject;
}

/// Whether serializing `object` can run user code that a constructor written
/// in Python could be in the middle of: only instances of heap types reach
/// one, and for a plain object with `object`'s `__repr__`, attribute lookup
/// and `__class__` (`object_class`) the hook reads nothing from the instance.
#[cfg(not(any(PyPy, GraalPy)))]
#[inline]
pub(super) fn may_run_user_code(
    py: Python<'_>,
    object: *mut ffi::PyObject,
    lightweight_repr: bool,
    object_class: usize,
) -> bool {
    // Safety: reads live type objects and a static type.
    unsafe {
        let class = ffi::Py_TYPE(object);
        if ffi::PyType_HasFeature(class, ffi::Py_TPFLAGS_HEAPTYPE) == 0 {
            return false;
        }
        let object_type = std::ptr::addr_of_mut!(ffi::PyBaseObject_Type);
        // The builtin type the class is laid out as: anything but `object`
        // may be one the hook serializes through methods (`isoformat`,
        // iteration), which the reference checks.
        let mut base = class;
        while !base.is_null() && ffi::PyType_HasFeature(base, ffi::Py_TPFLAGS_HEAPTYPE) != 0 {
            base = (*base).tp_base;
        }
        if base != object_type {
            return true;
        }
        // A plain object is only ever `repr()`'d, and not at all with
        // `lightweight_repr`; the hook's `isinstance()` checks before that
        // read `obj.__class__`.
        let default_repr = lightweight_repr
            || (*class).tp_repr.map(|slot| slot as usize)
                == (*object_type).tp_repr.map(|slot| slot as usize);
        let default_lookup = (*class).tp_getattro.map(|slot| slot as usize)
            == (*object_type).tp_getattro.map(|slot| slot as usize)
            && _PyType_Lookup(class, pyo3::intern!(py, "__class__").as_ptr()) as usize
                == object_class;
        !(default_repr && default_lookup)
    }
}

/// Type slots say less on these interpreters: the reference decides.
#[cfg(any(PyPy, GraalPy))]
#[inline]
pub(super) fn may_run_user_code(
    _py: Python<'_>,
    _object: *mut ffi::PyObject,
    _lightweight_repr: bool,
    _object_class: usize,
) -> bool {
    true
}

/// `describe()` (`kolo._construction.under_construction_repr(value)`: the
/// placeholder text, or None), remembered per type while the type is
/// unchanged: every `__init__` call records one, and the Python helper
/// costs many times a `repr()`.
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED), not(any(PyPy, GraalPy))))]
pub(super) fn placeholder_text<'py>(
    value: &Bound<'py, PyAny>,
    lightweight_repr: bool,
    describe: impl FnOnce() -> PyResult<Bound<'py, PyAny>>,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    use pyo3::types::PyString;
    use std::cell::RefCell;

    struct Entry {
        class: usize,
        version: u32,
        // The version tag does not change with `__qualname__`, which the
        // text holds: its address and hash, so that no reference to an
        // object of the program is kept.
        qualname: usize,
        qualname_hash: isize,
        lightweight_repr: bool,
        text: Option<Py<PyAny>>,
    }
    const ENTRIES: usize = 64;
    thread_local! {
        static PLACEHOLDERS: RefCell<[Option<Entry>; ENTRIES]> =
            RefCell::new(std::array::from_fn(|_| None));
    }
    /// The type's version tag, which any change to the type or its bases
    /// replaces; 0 if it has none to rely on (see `has_valid_version` in
    /// the value serializer).
    fn version(class: *mut ffi::PyTypeObject) -> u32 {
        // Safety: a live type object.
        unsafe {
            if cfg!(Py_3_13)
                || ffi::PyType_HasFeature(class, ffi::Py_TPFLAGS_VALID_VERSION_TAG) != 0
            {
                (*class).tp_version_tag
            } else {
                0
            }
        }
    }

    let py = value.py();
    // Held across `describe`, which runs Python: the value's class can be
    // reassigned and its old type and name released meanwhile.
    let class_object = value.get_type();
    let class = class_object.as_type_ptr();
    let tag = version(class);
    // Safety: only heap types get here (`may_run_user_code`), and their
    // qualified name is never NULL.
    let qualname_object = unsafe {
        Bound::from_borrowed_ptr(py, (*(class as *mut ffi::PyHeapTypeObject)).ht_qualname)
    };
    let qualname = qualname_object.as_ptr();
    let slot = ((class as usize >> 4) ^ lightweight_repr as usize) % ENTRIES;
    if tag != 0 {
        let hit = PLACEHOLDERS.with(|entries| match &entries.borrow()[slot] {
            Some(entry)
                if entry.class == class as usize
                    && entry.version == tag
                    && entry.qualname == qualname as usize
                    // Safety: a live str; an exact str's hash runs no code.
                    && unsafe {
                        ffi::PyUnicode_CheckExact(qualname) != 0
                            && ffi::PyObject_Hash(qualname) == entry.qualname_hash
                    }
                    && entry.lightweight_repr == lightweight_repr =>
            {
                Some(entry.text.as_ref().map(|text| text.clone_ref(py)))
            }
            _ => None,
        });
        if let Some(text) = hit {
            return Ok(text.map(|text| text.into_bound(py)));
        }
    }
    let text = describe()?;
    let text = (!text.is_none()).then_some(text);
    // `describe` ran Python: only remember what still describes the type.
    let exact = text
        .as_ref()
        .map_or(true, |text| text.is_exact_instance_of::<PyString>());
    // Safety: reads the live type again, and checks a live object's type.
    let unchanged = unsafe {
        ffi::Py_TYPE(value.as_ptr()) == class
            && version(class) == tag
            && (*(class as *mut ffi::PyHeapTypeObject)).ht_qualname == qualname
            && ffi::PyUnicode_CheckExact(qualname) != 0
    };
    if tag != 0 && exact && unchanged {
        let entry = Entry {
            class: class as usize,
            version: tag,
            qualname: qualname as usize,
            // Safety: an exact str, checked above.
            qualname_hash: unsafe { ffi::PyObject_Hash(qualname) },
            lightweight_repr,
            text: text.as_ref().map(|text| text.clone().unbind()),
        };
        // The replaced entry holds at most an exact str Kolo made, whose
        // release runs no code.
        PLACEHOLDERS.with(|entries| entries.borrow_mut()[slot] = Some(entry));
    }
    Ok(text)
}

#[cfg(not(all(Py_3_12, not(Py_GIL_DISABLED), not(any(PyPy, GraalPy)))))]
pub(super) fn placeholder_text<'py>(
    _value: &Bound<'py, PyAny>,
    _lightweight_repr: bool,
    describe: impl FnOnce() -> PyResult<Bound<'py, PyAny>>,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    let text = describe()?;
    Ok((!text.is_none()).then_some(text))
}

/// The objects under construction on this thread's stack. `reference` is
/// `kolo.serialize._objects_under_construction`, looked up only if needed.
pub(super) fn find<'py>(
    py: Python<'py>,
    reference: impl FnOnce() -> PyResult<Bound<'py, PyAny>>,
) -> PyResult<UnderConstruction> {
    // Once per event, and only for one with a value worth checking.
    if CHECK_OFF.load(Ordering::Relaxed) {
        return Ok(UnderConstruction(Vec::new()));
    }
    if let Some(found) = native_walk(py)? {
        return Ok(UnderConstruction(found));
    }
    Ok(UnderConstruction(reference()?.call0()?.extract()?))
}

/// The native walk's result in the reference's shape, for
/// `probe_native_walk` and the tests. None where it declines.
pub fn native_objects_under_construction(py: Python<'_>) -> Option<Vec<usize>> {
    let found = native::walk_unchecked(py)?;
    Some(if found.is_empty() { vec![0] } else { found })
}

/// One local variable of a frame, as a 1-tuple, or None if it is unbound,
/// without `frame.f_locals`, which on CPython 3.12 copies every local into a
/// dict the frame keeps.
#[cfg(all(Py_3_12, not(any(PyPy, GraalPy))))]
pub fn frame_local<'py>(
    frame: &Bound<'py, PyAny>,
    name: &Bound<'py, pyo3::types::PyString>,
) -> PyResult<Option<(Bound<'py, PyAny>,)>> {
    use pyo3::exceptions::{PyNameError, PyTypeError};
    let py = frame.py();
    // Safety: `frame` is checked to be a frame; `PyFrame_GetVar` returns a
    // new reference, or NULL with an error set.
    unsafe {
        if ffi::PyFrame_Check(frame.as_ptr()) == 0 {
            return Err(PyTypeError::new_err("expected a frame"));
        }
        let value = ffi::PyFrame_GetVar(frame.as_ptr().cast(), name.as_ptr());
        match Bound::from_owned_ptr_or_err(py, value) {
            Ok(value) => Ok(Some((value,))),
            Err(error) if error.is_instance_of::<PyNameError>(py) => Ok(None),
            Err(error) => Err(error),
        }
    }
}

#[cfg(not(all(Py_3_12, not(any(PyPy, GraalPy)))))]
pub fn frame_local<'py>(
    _frame: &Bound<'py, PyAny>,
    _name: &Bound<'py, pyo3::types::PyString>,
) -> PyResult<Option<(Bound<'py, PyAny>,)>> {
    Err(pyo3::exceptions::PyNotImplementedError::new_err(
        "reading one frame local needs CPython 3.12 or newer",
    ))
}

/// The native walk's result once it is validated (which the first call
/// starts), for the Python serializer. None where the reference must decide.
pub fn validated_objects_under_construction(py: Python<'_>) -> PyResult<Option<Vec<usize>>> {
    let found = native_walk(py)?;
    Ok(found.map(|found| if found.is_empty() { vec![0] } else { found }))
}

/// "valid" once the native walk has agreed with the reference in this
/// process, "invalid" if it did not, "unsupported" on interpreters it does
/// not know, else "unknown" (as it stays under
/// `KOLO_CONSTRUCTION_NATIVE=0`, where it is never compared).
pub fn native_walk_state() -> &'static str {
    native::state()
}

#[cfg(not(all(
    Py_3_11,
    not(Py_GIL_DISABLED),
    not(any(PyPy, GraalPy)),
    target_pointer_width = "64"
)))]
mod native {
    use pyo3::prelude::*;

    pub(super) fn walk(_py: Python<'_>) -> PyResult<Option<Vec<usize>>> {
        Ok(None)
    }

    pub(super) fn walk_unchecked(_py: Python<'_>) -> Option<Vec<usize>> {
        None
    }

    pub(super) fn state() -> &'static str {
        "unsupported"
    }
}

#[cfg(all(
    Py_3_11,
    not(Py_GIL_DISABLED),
    not(any(PyPy, GraalPy)),
    target_pointer_width = "64"
))]
mod native {
    use pyo3::exceptions::PyException;
    use pyo3::prelude::*;
    use pyo3::types::PyCode;
    use pyo3::{ffi, intern};
    use std::ptr;
    use std::sync::atomic::{AtomicU8, AtomicUsize, Ordering};

    const UNKNOWN: u8 = 0;
    const PROBING: u8 = 1;
    const VALID: u8 = 2;
    const INVALID: u8 = 3;
    static STATE: AtomicU8 = AtomicU8::new(UNKNOWN);
    /// Index of `co_name` in a code object, in pointer-sized words. Zero
    /// until found.
    static CO_NAME_WORD: AtomicUsize = AtomicUsize::new(0);
    static INCONCLUSIVE_PROBES: AtomicUsize = AtomicUsize::new(0);
    const MAX_INCONCLUSIVE_PROBES: usize = 64;
    /// Newest CPython 3.x whose frame layout is known to match.
    const NEWEST_MINOR: u8 = 15;
    /// Far deeper than any stack; a longer chain is not one we understand.
    const MAX_FRAMES: usize = 1 << 22;

    /// `PyFrameObject.f_frame`: after the object header and `f_back`.
    const FRAME_WORD: usize = std::mem::size_of::<ffi::PyObject>() / 8 + 1;
    // `_PyInterpreterFrame`, in words. 3.11 starts with `f_func`,
    // `f_globals`, `f_builtins`, `f_locals`, `f_code`, `frame_obj`,
    // `previous`; 3.12 and later with the code (`f_code`, then
    // `f_executable`) and `previous`.
    #[cfg(not(Py_3_12))]
    const CODE_WORD: usize = 4;
    #[cfg(not(Py_3_12))]
    const PREVIOUS_WORD: usize = 6;
    #[cfg(Py_3_12)]
    const CODE_WORD: usize = 0;
    #[cfg(Py_3_12)]
    const PREVIOUS_WORD: usize = 1;
    // `frame_obj`: the frame object, once something has asked for it.
    #[cfg(not(Py_3_12))]
    const FRAME_OBJECT_WORD: usize = 5;
    #[cfg(Py_3_12)]
    const FRAME_OBJECT_WORD: usize = 6;
    // `localsplus`: eight pointers, then `stacktop` and the small fields
    // (3.11 to 3.13) or `stackpointer` and the small fields (3.14, 3.15).
    #[cfg(not(Py_3_14))]
    const LOCALS_WORD: usize = 9;
    #[cfg(Py_3_14)]
    const LOCALS_WORD: usize = 10;
    // `co_localsplusnames`, `co_localspluskinds`, `co_filename`, `co_name`.
    const NAMES_BEFORE_CO_NAME: usize = 3;
    const KINDS_BEFORE_CO_NAME: usize = 2;
    const CO_FAST_LOCAL: u8 = 0x20;
    const CO_FAST_CELL: u8 = 0x40;
    /// `kolo._construction._RETURN_OPCODES`: two opcodes, 16 bits each
    /// (`NO_OPCODE` where there is only one).
    static RETURN_OPCODES: AtomicUsize = AtomicUsize::new(NO_OPCODE | NO_OPCODE << 16);
    const NO_OPCODE: usize = 0xffff;

    extern "C" {
        // Public since 3.11, but not in pyo3-ffi. A new reference to the
        // code's original bytecode, which the code object caches.
        fn PyCode_GetCode(code: *mut ffi::PyObject) -> *mut ffi::PyObject;
    }

    /// The object a frame slot refers to, or NULL. 3.14 and later store
    /// `_PyStackRef`: the pointer with tag bits, which also mark NULL and
    /// tagged ints.
    #[cfg(Py_3_14)]
    #[inline(always)]
    fn slot_object(bits: usize) -> *mut ffi::PyObject {
        if bits & 3 == 3 {
            return ptr::null_mut();
        }
        (bits & !3) as *mut ffi::PyObject
    }

    #[cfg(not(Py_3_14))]
    #[inline(always)]
    fn slot_object(bits: usize) -> *mut ffi::PyObject {
        bits as *mut ffi::PyObject
    }

    pub(super) fn state() -> &'static str {
        match STATE.load(Ordering::Relaxed) {
            VALID => "valid",
            INVALID => "invalid",
            _ => "unknown",
        }
    }

    pub(super) fn walk(py: Python<'_>) -> PyResult<Option<Vec<usize>>> {
        match STATE.load(Ordering::Relaxed) {
            // Safety: validated against the reference in this process.
            VALID => Ok(unsafe { walk_frames(py, CO_NAME_WORD.load(Ordering::Relaxed)) }),
            UNKNOWN => {
                // The probe's own frames are on the stack while it runs, so
                // this event is left to the reference.
                probe(py)?;
                Ok(None)
            }
            _ => Ok(None),
        }
    }

    pub(super) fn walk_unchecked(py: Python<'_>) -> Option<Vec<usize>> {
        if !known_release(py) {
            return None;
        }
        let mut word = CO_NAME_WORD.load(Ordering::Relaxed);
        if word == 0 {
            word = find_co_name(py).ok().flatten()?;
            CO_NAME_WORD.store(word, Ordering::Relaxed);
        }
        // Safety: a release whose frame layout is known, and `co_name` was
        // found where the walk reads it.
        unsafe { walk_frames(py, word) }
    }

    fn known_release(py: Python<'_>) -> bool {
        let version = py.version_info();
        version.major == 3 && version.minor <= NEWEST_MINOR
    }

    /// Compare the native walk with the reference, once per process.
    fn probe(py: Python<'_>) -> PyResult<()> {
        if STATE
            .compare_exchange(UNKNOWN, PROBING, Ordering::Relaxed, Ordering::Relaxed)
            .is_err()
        {
            return Ok(());
        }
        let outcome = (|| -> PyResult<Option<bool>> {
            if !known_release(py) {
                return Ok(Some(false));
            }
            if CO_NAME_WORD.load(Ordering::Relaxed) == 0 {
                match find_co_name(py)? {
                    Some(word) => CO_NAME_WORD.store(word, Ordering::Relaxed),
                    None => return Ok(Some(false)),
                }
            }
            let native = PyModule::import(py, "kolo._kolo")?
                .getattr(intern!(py, "_native_objects_under_construction"))?;
            PyModule::import(py, "kolo._construction")?
                .getattr(intern!(py, "probe_native_walk"))?
                .call1((native,))?
                .extract()
        })();
        let (state, result) = match outcome {
            Ok(Some(true)) => (VALID, Ok(())),
            Ok(None)
                if INCONCLUSIVE_PROBES.fetch_add(1, Ordering::Relaxed)
                    < MAX_INCONCLUSIVE_PROBES =>
            {
                (UNKNOWN, Ok(()))
            }
            Ok(_) => (INVALID, Ok(())),
            // An interrupt that arrived during the probe belongs to the
            // program; the probe runs again on a later event.
            Err(error) if !error.is_instance_of::<PyException>(py) => (UNKNOWN, Err(error)),
            Err(_) => (INVALID, Ok(())),
        };
        STATE.store(state, Ordering::Relaxed);
        result
    }

    /// Find `co_name` in two of Kolo's own code objects, and check that the
    /// locals' names and kinds sit where they do on every known release.
    fn find_co_name(py: Python<'_>) -> PyResult<Option<usize>> {
        let module = PyModule::import(py, "kolo._construction")?;
        let mut opcodes = [NO_OPCODE; 2];
        let returns = module.getattr(intern!(py, "_RETURN_OPCODES"))?;
        for (slot, opcode) in opcodes.iter_mut().zip(returns.try_iter()?) {
            *slot = opcode?.extract::<u8>()? as usize;
        }
        if returns.len()? > opcodes.len() || opcodes[0] == NO_OPCODE {
            return Ok(None);
        }
        RETURN_OPCODES.store(opcodes[0] | opcodes[1] << 16, Ordering::Relaxed);
        let mut word = None;
        for function in ["objects_under_construction", "under_construction_repr"] {
            let code = module.getattr(function)?.getattr(intern!(py, "__code__"))?;
            if !code.is_exact_instance_of::<PyCode>() {
                return Ok(None);
            }
            let name = code.getattr(intern!(py, "co_name"))?;
            let filename = code.getattr(intern!(py, "co_filename"))?;
            let qualname = code.getattr(intern!(py, "co_qualname"))?;
            let varnames = code.getattr(intern!(py, "co_varnames"))?;
            let first_local = varnames.get_item(0)?;
            let local_count = varnames.len()?;
            // Safety: `code` is an exact code object of a known release and
            // every word read is inside it. Words are only compared until
            // `co_filename`, `co_name`, `co_qualname` are found in a row;
            // the two before them, then treated as objects, are
            // `co_localsplusnames` and `co_localspluskinds` on each release.
            let found = unsafe {
                let words = code.as_ptr() as *const usize;
                let size = (*ffi::Py_TYPE(code.as_ptr())).tp_basicsize as usize / 8;
                let Some(found) =
                    (NAMES_BEFORE_CO_NAME + 2..size.saturating_sub(1)).find(|&index| {
                        *words.add(index - 1) == filename.as_ptr() as usize
                            && *words.add(index) == name.as_ptr() as usize
                            && *words.add(index + 1) == qualname.as_ptr() as usize
                    })
                else {
                    return Ok(None);
                };
                let names = *words.add(found - NAMES_BEFORE_CO_NAME) as *mut ffi::PyObject;
                let kinds = *words.add(found - KINDS_BEFORE_CO_NAME) as *mut ffi::PyObject;
                if names.is_null()
                    || kinds.is_null()
                    || ffi::PyTuple_CheckExact(names) == 0
                    || ffi::PyBytes_CheckExact(kinds) == 0
                    || (ffi::PyTuple_Size(names) as usize) < local_count
                    || ffi::PyTuple_GetItem(names, 0) != first_local.as_ptr()
                    || ffi::PyBytes_Size(kinds) != ffi::PyTuple_Size(names)
                {
                    return Ok(None);
                }
                found
            };
            if word.is_some_and(|word| word != found) {
                return Ok(None);
            }
            word = Some(found);
        }
        Ok(word)
    }

    /// `kolo._construction._returning`. None if the bytecode could not be
    /// read.
    ///
    /// Safety: `frame` must be a live frame object running `code`.
    unsafe fn returning(frame: *mut ffi::PyFrameObject, code: *mut ffi::PyObject) -> Option<bool> {
        unsafe {
            let lasti = ffi::PyFrame_GetLasti(frame);
            if lasti < 0 {
                return Some(false);
            }
            let bytecode = PyCode_GetCode(code);
            if bytecode.is_null() {
                ffi::PyErr_Clear();
                return None;
            }
            let mut found = false;
            if (lasti as isize) < ffi::PyBytes_Size(bytecode) {
                let opcode =
                    *(ffi::PyBytes_AsString(bytecode) as *const u8).add(lasti as usize) as usize;
                let returns = RETURN_OPCODES.load(Ordering::Relaxed);
                found = opcode == returns & NO_OPCODE || opcode == returns >> 16;
            }
            ffi::Py_DECREF(bytecode);
            Some(found)
        }
    }

    /// `objects_under_construction()` for a stack with no `__new__` on it.
    /// Empty when no object is under construction.
    ///
    /// Safety: the interpreter's frame layout must be the one the constants
    /// above describe, and `co_name_word` must be `co_name`'s index.
    unsafe fn walk_frames(py: Python<'_>, co_name_word: usize) -> Option<Vec<usize>> {
        unsafe {
            let top = ffi::PyEval_GetFrame() as *const usize;
            if top.is_null() {
                return Some(Vec::new());
            }
            let new = intern!(py, "__new__").as_ptr() as usize;
            let initializers = [
                intern!(py, "__init__").as_ptr() as usize,
                intern!(py, "__post_init__").as_ptr() as usize,
                intern!(py, "__setstate__").as_ptr() as usize,
            ];
            let mut objects = Vec::new();
            let mut frame = *top.add(FRAME_WORD) as *const usize;
            // A build that stores something else in these words (stack
            // references as handles, say) must not get as far as reading
            // one as an object: the innermost frame's code is known.
            let expected = ffi::PyFrame_GetCode(top as *mut ffi::PyFrameObject);
            // The frame keeps its code alive.
            ffi::Py_DECREF(expected.cast());
            if frame.is_null() || slot_object(*frame.add(CODE_WORD)) != expected.cast() {
                return None;
            }
            let mut innermost = true;
            let mut frames = 0;
            while !frame.is_null() {
                frames += 1;
                if frames > MAX_FRAMES {
                    return None;
                }
                let code = slot_object(*frame.add(CODE_WORD));
                if !known_code::seen(code) && is_code(code) {
                    let name = *(code as *const usize).add(co_name_word);
                    let kind = if name == new {
                        Constructor::New
                    } else if initializers.contains(&name) {
                        Constructor::Initializer
                    } else {
                        other_name(name as *mut ffi::PyObject)
                    };
                    if kind == Constructor::No {
                        known_code::remember(py, code);
                    }
                    // Which instances of its class are a running
                    // `__new__`'s arguments takes its bytecode to tell: the
                    // reference decides, now, before the event serializes
                    // anything that could change what it would find.
                    if kind == Constructor::New {
                        return None;
                    }
                    // A frame can only have reached its `return` with a
                    // callback on top of it: native (then it is innermost) or
                    // Python, which got hold of its frame object.
                    let finished = kind == Constructor::Initializer && {
                        let object = if innermost {
                            top as *mut ffi::PyFrameObject
                        } else {
                            *frame.add(FRAME_OBJECT_WORD) as *mut ffi::PyFrameObject
                        };
                        !object.is_null() && returning(object, code)?
                    };
                    if kind == Constructor::Initializer && !finished {
                        match first_local(code, frame, co_name_word) {
                            Ok(Some(object)) => objects.push(object as usize),
                            Ok(None) => {}
                            Err(()) => return None,
                        }
                    }
                }
                // The innermost frame, from `PyEval_GetFrame`, runs code.
                innermost = false;
                frame = *frame.add(PREVIOUS_WORD) as *const usize;
            }
            if !objects.is_empty() {
                objects.insert(0, objects.len());
            }
            Some(objects)
        }
    }

    /// Code objects whose name is no constructor's, by address. Reading a
    /// code object's name is a likely cache miss, and the same few dozen
    /// frames are walked for every event. No reference is held: a code
    /// watcher forgets a code object when it is destroyed, so an address is
    /// never taken for a later object's.
    #[cfg(Py_3_12)]
    mod known_code {
        use pyo3::prelude::*;
        use pyo3::{ffi, PyErr};
        use std::os::raw::c_int;
        use std::sync::atomic::{AtomicU8, AtomicUsize, Ordering};

        const SLOTS: usize = 256;
        static TABLE: [AtomicUsize; SLOTS] = [const { AtomicUsize::new(0) }; SLOTS];
        /// 0: not asked yet, 1: watching, 2: no watcher slot was free.
        static WATCHING: AtomicU8 = AtomicU8::new(0);

        extern "C" {
            // Public since 3.12, but not in pyo3-ffi.
            fn PyCode_AddWatcher(
                callback: unsafe extern "C" fn(c_int, *mut ffi::PyObject) -> c_int,
            ) -> c_int;
        }

        fn slot(code: *mut ffi::PyObject) -> &'static AtomicUsize {
            &TABLE[(code as usize >> 4 ^ code as usize >> 12) % SLOTS]
        }

        /// The code object last seen being destroyed. Other watchers still
        /// get to run after this one, and code they run must not put it back.
        static DYING: AtomicUsize = AtomicUsize::new(0);
        const PY_CODE_EVENT_DESTROY: c_int = 1;

        unsafe extern "C" fn watch(event: c_int, code: *mut ffi::PyObject) -> c_int {
            // Forget on creation as well as destruction: whatever this
            // address was remembered as, it is another code object now.
            let _ =
                slot(code).compare_exchange(code as usize, 0, Ordering::Relaxed, Ordering::Relaxed);
            let dying = if event == PY_CODE_EVENT_DESTROY {
                code as usize
            } else {
                0
            };
            DYING.store(dying, Ordering::Relaxed);
            0
        }

        #[inline(always)]
        pub(super) fn seen(code: *mut ffi::PyObject) -> bool {
            !code.is_null() && slot(code).load(Ordering::Relaxed) == code as usize
        }

        pub(super) fn remember(py: Python<'_>, code: *mut ffi::PyObject) {
            let mut watching = WATCHING.load(Ordering::Relaxed);
            if watching == 0 {
                // Safety: registers a static callback, with the GIL.
                watching = if unsafe { PyCode_AddWatcher(watch) } < 0 {
                    drop(PyErr::fetch(py));
                    2
                } else {
                    1
                };
                WATCHING.store(watching, Ordering::Relaxed);
            }
            if watching == 1 && DYING.load(Ordering::Relaxed) != code as usize {
                slot(code).store(code as usize, Ordering::Relaxed);
            }
        }
    }

    /// 3.11 has no code watchers: every frame's name is read.
    #[cfg(not(Py_3_12))]
    mod known_code {
        use pyo3::ffi;
        use pyo3::prelude::*;

        #[inline(always)]
        pub(super) fn seen(_code: *mut ffi::PyObject) -> bool {
            false
        }

        pub(super) fn remember(_py: Python<'_>, _code: *mut ffi::PyObject) {}
    }

    #[derive(PartialEq)]
    enum Constructor {
        No,
        New,
        Initializer,
    }

    /// Whether a frame's executable is a code object: the frames the
    /// interpreter pushes around C calls hold None from 3.13 on, which is
    /// told apart without loading anything. Each object a step of the walk
    /// loads is likely a cache miss, and the walk is deep.
    #[cfg(Py_3_13)]
    #[inline(always)]
    unsafe fn is_code(code: *mut ffi::PyObject) -> bool {
        !code.is_null() && code != unsafe { ffi::Py_None() }
    }

    #[cfg(not(Py_3_13))]
    #[inline(always)]
    unsafe fn is_code(code: *mut ffi::PyObject) -> bool {
        !code.is_null() && unsafe { ffi::Py_TYPE(code) } == ptr::addr_of_mut!(ffi::PyCode_Type)
    }

    /// 3.13 interns the name of every code object, so one that is not the
    /// interned string itself is no constructor's.
    #[cfg(Py_3_13)]
    #[inline(always)]
    unsafe fn other_name(_name: *mut ffi::PyObject) -> Constructor {
        Constructor::No
    }

    /// Before 3.13 a code object built by hand (`code.replace(co_name=...)`)
    /// keeps the str it was given: compare the text.
    ///
    /// Safety: `name` must be a str.
    #[cfg(not(Py_3_13))]
    #[inline]
    unsafe fn other_name(name: *mut ffi::PyObject) -> Constructor {
        unsafe {
            let (text, kind) = match ffi::PyUnicode_GET_LENGTH(name) {
                7 => (c"__new__", Constructor::New),
                8 => (c"__init__", Constructor::Initializer),
                12 => (c"__setstate__", Constructor::Initializer),
                13 => (c"__post_init__", Constructor::Initializer),
                _ => return Constructor::No,
            };
            if ffi::PyUnicode_CompareWithASCIIString(name, text.as_ptr()) == 0 {
                kind
            } else {
                Constructor::No
            }
        }
    }

    /// `kolo._construction._first_local`, with `def __init__(*args)` taken
    /// as `args[0]`. `Err` if the code object is not laid out as expected.
    unsafe fn first_local(
        code: *mut ffi::PyObject,
        frame: *const usize,
        co_name_word: usize,
    ) -> Result<Option<*mut ffi::PyObject>, ()> {
        unsafe {
            let words = code as *const usize;
            let names = *words.add(co_name_word - NAMES_BEFORE_CO_NAME) as *mut ffi::PyObject;
            let kinds = *words.add(co_name_word - KINDS_BEFORE_CO_NAME) as *mut ffi::PyObject;
            if names.is_null()
                || kinds.is_null()
                || ffi::PyTuple_CheckExact(names) == 0
                || ffi::PyBytes_CheckExact(kinds) == 0
            {
                return Err(());
            }
            if ffi::PyTuple_Size(names) < 1 || ffi::PyBytes_Size(kinds) < 1 {
                return Ok(None);
            }
            let kind = *(ffi::PyBytes_AsString(kinds) as *const u8);
            // The first slot of a frame without locals is a closure variable.
            if kind & CO_FAST_LOCAL == 0 {
                return Ok(None);
            }
            let mut object = slot_object(*frame.add(LOCALS_WORD));
            if object.is_null() {
                return Ok(None);
            }
            if kind & CO_FAST_CELL != 0
                && ffi::Py_TYPE(object) == ptr::addr_of_mut!(ffi::PyCell_Type)
            {
                // A new reference, or NULL for an empty cell.
                let contents = ffi::PyCell_Get(object);
                if contents.is_null() {
                    ffi::PyErr_Clear();
                    return Ok(None);
                }
                // The cell keeps its contents alive.
                ffi::Py_DECREF(contents);
                object = contents;
            }
            if ffi::PyTuple_CheckExact(object) != 0 {
                if ffi::PyTuple_Size(object) < 1 {
                    return Ok(None);
                }
                object = ffi::PyTuple_GetItem(object, 0);
            }
            Ok(Some(object))
        }
    }
}
