//! Snapshot a frame's locals without going through `FrameLocalsProxy`.
//!
//! On CPython 3.13+ (PEP 667) `frame.f_locals` of an optimized frame is a
//! write-through `FrameLocalsProxy`. Copying it with `dict(proxy)` calls the
//! proxy's `keys()`, then looks each key up again by a linear scan over the
//! code's variable names, so every captured event paid for a proxy, a keys
//! list, an O(n²) lookup loop, and the dict. On 3.12 the same attribute
//! returned the frame's own, re-synced locals dict.
//!
//! The snapshot below reads the fast-locals array directly, mirroring
//! `framelocalsproxy_keys` + `framelocalsproxy_getitem` from
//! `Objects/frameobject.c`, so the resulting dict is identical to
//! `dict(frame.f_locals)`: same keys, same order, same values. Anything outside
//! the plain case (non-optimized code, locals added through `f_locals`, a
//! frame layout that fails validation) returns `None` and the caller falls
//! back to the proxy copy.

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyFrame};

#[cfg(all(
    Py_3_13,
    not(Py_GIL_DISABLED),
    not(Py_LIMITED_API),
    not(any(PyPy, GraalPy))
))]
mod layout {
    use pyo3::ffi;
    use std::os::raw::{c_char, c_int, c_void};

    pub const CO_OPTIMIZED: c_int = 0x0001;
    pub const CO_FAST_CELL: u8 = 0x40;
    pub const CO_FAST_FREE: u8 = 0x80;

    /// Prefix of `PyCodeObject` (`_PyCode_DEF` in `Include/cpython/code.h`),
    /// unchanged from 3.13 through 3.15 up to `co_localspluskinds`.
    #[repr(C)]
    pub struct CodePrefix {
        pub ob_base: ffi::PyVarObject,
        pub co_consts: *mut ffi::PyObject,
        pub co_names: *mut ffi::PyObject,
        pub co_exceptiontable: *mut ffi::PyObject,
        pub co_flags: c_int,
        pub co_argcount: c_int,
        pub co_posonlyargcount: c_int,
        pub co_kwonlyargcount: c_int,
        pub co_stacksize: c_int,
        pub co_firstlineno: c_int,
        pub co_nlocalsplus: c_int,
        pub co_framesize: c_int,
        pub co_nlocals: c_int,
        pub co_ncellvars: c_int,
        pub co_nfreevars: c_int,
        pub co_version: u32,
        pub co_localsplusnames: *mut ffi::PyObject,
        pub co_localspluskinds: *mut ffi::PyObject,
    }

    /// Prefix of `PyFrameObject` (`struct _frame` in
    /// `Include/internal/pycore_frame.h`), unchanged from 3.13 through 3.15
    /// up to `f_extra_locals`.
    #[repr(C)]
    pub struct FramePrefix {
        pub ob_base: ffi::PyObject,
        pub f_back: *mut c_void,
        pub f_frame: *mut InterpreterFrame,
        pub f_trace: *mut ffi::PyObject,
        pub f_lineno: c_int,
        pub f_trace_lines: c_char,
        pub f_trace_opcodes: c_char,
        pub f_extra_locals: *mut ffi::PyObject,
    }

    /// `_PyInterpreterFrame` on 3.13 (`Include/internal/pycore_frame.h`).
    #[cfg(not(Py_3_14))]
    #[repr(C)]
    pub struct InterpreterFrame {
        pub f_executable: usize,
        pub previous: *mut c_void,
        pub f_funcobj: usize,
        pub f_globals: *mut ffi::PyObject,
        pub f_builtins: *mut ffi::PyObject,
        pub f_locals: *mut ffi::PyObject,
        pub frame_obj: *mut ffi::PyObject,
        pub instr_ptr: *mut c_void,
        pub stacktop: c_int,
        pub return_offset: u16,
        pub owner: c_char,
        pub localsplus: [usize; 0],
    }

    /// `_PyInterpreterFrame` on 3.14 and 3.15
    /// (`Include/internal/pycore_interpframe_structs.h`, GIL build).
    #[cfg(Py_3_14)]
    #[repr(C)]
    pub struct InterpreterFrame {
        pub f_executable: usize,
        pub previous: *mut c_void,
        pub f_funcobj: usize,
        pub f_globals: *mut ffi::PyObject,
        pub f_builtins: *mut ffi::PyObject,
        pub f_locals: *mut ffi::PyObject,
        pub frame_obj: *mut ffi::PyObject,
        pub instr_ptr: *mut c_void,
        pub stackpointer: *mut c_void,
        pub return_offset: u16,
        pub owner: c_char,
        pub visited: u8,
        pub localsplus: [usize; 0],
    }

    /// `PyStackRef_AsPyObjectBorrow` for the GIL build: 3.14+ tags deferred
    /// and immortal references (and NULL) with the low bit. 3.13 stores plain
    /// `PyObject *`.
    #[inline(always)]
    pub fn borrow_ref(bits: usize) -> *mut ffi::PyObject {
        #[cfg(Py_3_14)]
        let bits = bits & !1usize;
        bits as *mut ffi::PyObject
    }
}

/// Whether the running interpreter is one whose frame layout `layout` mirrors.
#[cfg(all(
    Py_3_13,
    not(Py_GIL_DISABLED),
    not(Py_LIMITED_API),
    not(any(PyPy, GraalPy))
))]
fn layout_supported(py: Python<'_>) -> bool {
    use once_cell::sync::OnceCell;
    static SUPPORTED: OnceCell<bool> = OnceCell::new();
    *SUPPORTED.get_or_init(|| {
        let version = py.version_info();
        version.major == 3 && (13..=15).contains(&version.minor)
    })
}

/// Build `dict(frame.f_locals)` straight from the frame's fast locals.
///
/// Returns `Ok(None)` when the frame is not a plain optimized frame this
/// mirror covers; the caller then copies `frame.f_locals` as before.
#[cfg(all(
    Py_3_13,
    not(Py_GIL_DISABLED),
    not(Py_LIMITED_API),
    not(any(PyPy, GraalPy))
))]
pub(super) fn fast_locals_dict<'py>(
    frame: &Bound<'py, PyFrame>,
) -> PyResult<Option<Bound<'py, PyDict>>> {
    use layout::*;
    use pyo3::ffi;

    let py = frame.py();
    if !layout_supported(py) {
        return Ok(None);
    }
    let frame_ptr = frame.as_ptr();
    // SAFETY: `frame` is a live exact `PyFrameObject` (PyFrame is only bound
    // to frame objects) and the GIL is held, so its interpreter frame cannot
    // be cleared or moved while we read it. Every pointer read below is
    // validated against an independent public accessor before use.
    unsafe {
        let frame_struct = &*(frame_ptr as *const FramePrefix);
        let interp = frame_struct.f_frame;
        if interp.is_null() || (*interp).frame_obj != frame_ptr {
            return Ok(None);
        }
        if !frame_struct.f_extra_locals.is_null() {
            return Ok(None);
        }
        let code = ffi::PyFrame_GetCode(frame_ptr.cast());
        if code.is_null() {
            return Err(PyErr::fetch(py));
        }
        // PyFrame_GetCode returns a new reference; the frame keeps the code
        // alive for the duration of this call.
        ffi::Py_DECREF(code.cast());
        if borrow_ref((*interp).f_executable) != code.cast::<ffi::PyObject>() {
            return Ok(None);
        }
        let code = &*(code as *const CodePrefix);
        if code.co_flags & CO_OPTIMIZED == 0 {
            return Ok(None);
        }
        let names = code.co_localsplusnames;
        let kinds = code.co_localspluskinds;
        let count = code.co_nlocalsplus;
        if ffi::PyTuple_Check(names) == 0
            || ffi::PyBytes_Check(kinds) == 0
            || ffi::PyTuple_GET_SIZE(names) != count as ffi::Py_ssize_t
            || ffi::PyBytes_Size(kinds) != count as ffi::Py_ssize_t
        {
            return Ok(None);
        }
        let kinds = ffi::PyBytes_AsString(kinds) as *const u8;
        // Raw place projection keeps the provenance of the frame pointer for
        // reads past the zero-length array.
        let fast = std::ptr::addr_of!((*interp).localsplus).cast::<usize>();

        let dict =
            Bound::from_owned_ptr_or_err(py, ffi::PyDict_New())?.cast_into_unchecked::<PyDict>();
        let dict_ptr = dict.as_ptr();
        for i in 0..count as usize {
            let mut value = borrow_ref(*fast.add(i));
            if value.is_null() {
                continue;
            }
            let kind = *kinds.add(i);
            if (kind == CO_FAST_FREE || kind & CO_FAST_CELL != 0) && ffi::PyCell_Check(value) != 0 {
                value = (*(value as *const ffi::PyCellObject)).ob_ref;
                if value.is_null() {
                    continue;
                }
            }
            let name = ffi::PyTuple_GET_ITEM(names, i as ffi::Py_ssize_t);
            // A name can repeat (an inlined comprehension variable shadowing a
            // cell); the proxy resolves a name to its first bound slot.
            if ffi::PyDict_SetDefault(dict_ptr, name, value).is_null() {
                return Err(PyErr::fetch(py));
            }
        }
        Ok(Some(dict))
    }
}

#[cfg(not(all(
    Py_3_13,
    not(Py_GIL_DISABLED),
    not(Py_LIMITED_API),
    not(any(PyPy, GraalPy))
)))]
#[cfg(test)]
fn layout_supported(_py: Python<'_>) -> bool {
    false
}

#[cfg(not(all(
    Py_3_13,
    not(Py_GIL_DISABLED),
    not(Py_LIMITED_API),
    not(any(PyPy, GraalPy))
)))]
pub(super) fn fast_locals_dict<'py>(
    _frame: &Bound<'py, PyFrame>,
) -> PyResult<Option<Bound<'py, PyDict>>> {
    Ok(None)
}

#[cfg(test)]
mod tests {
    use super::{fast_locals_dict, layout_supported};
    use pyo3::prelude::*;
    use pyo3::types::{PyCFunction, PyDict, PyFrame, PyList, PyTuple};

    /// Exercise every fast-locals shape against `dict(frame.f_locals)`.
    ///
    /// `snap(kind)` is called from inside the probed frames, so live frames
    /// (and their cells, unbound slots, comprehension temporaries) are read
    /// while executing, exactly as a monitoring callback sees them.
    const SCENARIOS: &std::ffi::CStr = cr#"
import sys

def plain(a, b=2, *args, **kwargs):
    unbound_yet = None
    snap("plain-call")
    later = a + b
    snap("plain-late")
    del unbound_yet
    snap("plain-deleted")

def closures(x):
    captured = [x]
    def inner(y):
        snap("free-vars")
        return captured, x, y
    snap("cell-vars")
    return inner(3)

def unbound_cell():
    snap("unbound-cell")
    late_cell = 1
    def use():
        return late_cell
    snap("bound-cell")
    return use

def comprehension_shadow():
    shadow = "outer"
    def keep():
        return shadow
    values = [snap("inlined-comprehension") or shadow for shadow in range(2)]
    snap("after-comprehension")
    return keep, values

def generator(n):
    total = 0
    for i in range(n):
        total += i
        snap("generator")
        yield total

def builtins_named():
    __builtins__ = {"shadowed": True}
    snap("builtins-local")

def extra_locals():
    frame = sys._getframe()
    frame.f_locals["added_later"] = 41
    snap("extra-locals")

def exception_var():
    try:
        raise ValueError("boom")
    except ValueError as error:
        snap("exception-bound")
    snap("exception-cleared")

class Body:
    attribute = 1
    snap("class-body")

plain(1, 2, 3, key="value")
closures(5)
unbound_cell()
comprehension_shadow()
list(generator(2))
builtins_named()
extra_locals()
exception_var()
snap("module")
"#;

    #[test]
    fn fast_locals_snapshot_matches_frame_locals_copy() {
        Python::initialize();
        Python::attach(|py| {
            let seen = PyList::empty(py);
            let record = seen.clone().unbind();
            let snap = PyCFunction::new_closure(
                py,
                None,
                None,
                move |args: &Bound<'_, PyTuple>, _kwargs: Option<&Bound<'_, PyDict>>| {
                    let py = args.py();
                    let kind = args.get_item(0)?;
                    let sys = py.import("sys")?;
                    let frame = sys.call_method1("_getframe", (0,))?;
                    let frame = frame.cast_into::<PyFrame>()?;
                    let expected = py
                        .get_type::<PyDict>()
                        .call1((frame.getattr("f_locals")?,))?;
                    let fast = fast_locals_dict(&frame)?;
                    record
                        .bind(py)
                        .append((kind, expected, fast, frame.f_code_flags()?))?;
                    PyResult::Ok(py.None())
                },
            )
            .expect("snap function builds");
            let globals = PyDict::new(py);
            globals.set_item("snap", snap).unwrap();
            py.run(SCENARIOS, Some(&globals), None)
                .expect("scenarios run");

            let supported = layout_supported(py);
            let mut fast_hits = 0;
            for entry in seen.iter() {
                let (kind, expected, fast, optimized): (
                    String,
                    Bound<PyDict>,
                    Option<Bound<PyDict>>,
                    bool,
                ) = entry.extract().unwrap();
                let Some(fast) = fast else {
                    // Only non-optimized code, locals added via f_locals, and
                    // interpreters without a mirrored layout take the
                    // proxy-copy fallback.
                    assert!(
                        !optimized || kind == "extra-locals" || !supported,
                        "{kind}: unexpected fallback"
                    );
                    continue;
                };
                fast_hits += 1;
                let expected_items = expected.items();
                let fast_items = fast.items();
                assert!(
                    fast_items.eq(&expected_items).unwrap(),
                    "{kind}: {fast_items} != {expected_items}"
                );
                // Same objects, not just equal ones.
                for (key, value) in expected.iter() {
                    assert!(
                        fast.get_item(&key).unwrap().unwrap().is(&value),
                        "{kind}: {key}"
                    );
                }
            }
            if supported {
                assert!(fast_hits >= 12, "fast path covered only {fast_hits} frames");
            } else {
                assert_eq!(fast_hits, 0, "fast path used without a mirrored layout");
            }
        });
    }

    trait CodeFlags {
        fn f_code_flags(&self) -> PyResult<bool>;
    }

    impl CodeFlags for Bound<'_, PyFrame> {
        fn f_code_flags(&self) -> PyResult<bool> {
            let flags: i32 = self.getattr("f_code")?.getattr("co_flags")?.extract()?;
            Ok(flags & 0x1 != 0)
        }
    }
}
