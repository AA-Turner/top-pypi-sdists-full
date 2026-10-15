use hashbrown::HashMap;
use pyo3::exceptions::{
    PyException, PyNameError, PyOSError, PyRecursionError, PyTypeError, PyUnicodeEncodeError,
    PyValueError,
};
use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::{PyAny, PyBytes, PyDict, PyInt, PyList, PyModule, PyString, PyTuple};
use pyo3::{ffi, intern, Borrowed};
use std::cell::{Cell, RefCell};
use std::io::{self, Cursor};
use std::ops::Range;
use std::ptr;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use thread_local::ThreadLocal;

use super::super::trace_container::TraceCapture;
use super::construction;

extern "C" {
    // Exported by every supported CPython (Cython-generated extensions rely
    // on it), but omitted from pyo3-ffi as underscore-prefixed. The result is
    // borrowed and only compared by address here.
    fn _PyType_Lookup(
        type_: *mut ffi::PyTypeObject,
        name: *mut ffi::PyObject,
    ) -> *mut ffi::PyObject;

    fn PyMethod_New(function: *mut ffi::PyObject, self_: *mut ffi::PyObject) -> *mut ffi::PyObject;
    /// Borrowed reference to a bound method's `__func__`.
    fn PyMethod_Function(method: *mut ffi::PyObject) -> *mut ffi::PyObject;
    /// Borrowed reference to a bound method's `__self__`.
    fn PyMethod_Self(method: *mut ffi::PyObject) -> *mut ffi::PyObject;

    // `PyObject_GetOptionalAttr` before it became public API in 3.13.
    #[cfg(not(Py_3_13))]
    fn _PyObject_LookupAttr(
        value: *mut ffi::PyObject,
        name: *mut ffi::PyObject,
        result: *mut *mut ffi::PyObject,
    ) -> std::os::raw::c_int;
}

std::thread_local! {
    /// Native encodes running on this OS thread. Kolo's Django query guard
    /// (`kolo.serialize._install_query_guard`) reads it through
    /// `_native_encode_in_progress`, so marking an encode costs a counter
    /// update rather than Python attribute writes. Being per OS thread, a
    /// `__repr__` that yields to another gevent greenlet mid-encode blocks
    /// that greenlet's queries until the encode resumes.
    static NATIVE_ENCODES: Cell<u32> = const { Cell::new(0) };
}

/// Whether this thread is inside a native encode.
pub fn native_encode_in_progress() -> bool {
    NATIVE_ENCODES.with(|count| count.get() > 0)
}

/// Kolo's value serializer.
///
/// Frames and plugin data are encoded natively with the exact semantics of
/// `kolo.serialize.dump_msgpack` (and `dump_msgpack_lightweight_repr`):
/// `msgpack.Packer(default=msgpack_encode_hook, strict_types=True)`. See
/// `NativeMsgpackEncoder` for how each part of that pipeline is mirrored.
///
/// Every monitor, profiler and plugin processor shares one process-wide
/// state, so registering many of them stays cheap.
#[derive(Clone)]
pub struct Serializer(Arc<SerializerState>);

static SERIALIZER: PyOnceLock<Serializer> = PyOnceLock::new();

impl std::ops::Deref for Serializer {
    type Target = SerializerState;

    fn deref(&self) -> &SerializerState {
        &self.0
    }
}

pub struct SerializerState {
    // `msgpack_encode_hook` resolves `datetime`, `Decimal`, the QuerySet
    // cache, and `IN_KOLO_PROFILER` through these globals on every call, so
    // the native hook reads them live too (freezegun, for example, rebinds
    // `datetime` in loaded modules while time is frozen).
    globals: Py<PyDict>,
    ext_type: Py<PyAny>,
    timestamp_type: Py<PyAny>,
    packb: Py<PyAny>,
    // The bound method type (`PyMethod_Type`), whose reprs are composed
    // natively. Taken from a real bound method: `types.MethodType` is a
    // rebindable module attribute.
    method_type: usize,
    recurse_limit: i32,
    object_class: usize,
    object_getattribute: usize,
    // `tp_getattro` of `type` and of bound methods, whose `__class__` read
    // is as side-effect free as `object.__getattribute__`'s.
    #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
    type_getattro: usize,
    #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
    method_getattro: usize,
    /// Whether `kolo.serialize`'s globals are watched, which the per-type
    /// ladder cache needs to notice a rebound `datetime`/`Decimal`/QuerySet.
    #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
    globals_watched: bool,
    /// CPython's own `tp_repr` slots whose output `builtin_repr` writes.
    #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
    builtin_reprs: BuiltinReprs,
    #[cfg(test)]
    python_dump_msgpack: Py<PyAny>,
    #[cfg(test)]
    python_dump_msgpack_lightweight_repr: Py<PyAny>,
}

impl Serializer {
    pub fn new(py: Python) -> Result<Self, PyErr> {
        SERIALIZER
            .get_or_try_init(py, || {
                SerializerState::new(py).map(|state| Serializer(Arc::new(state)))
            })
            .cloned()
    }
}

impl SerializerState {
    fn new(py: Python) -> Result<Self, PyErr> {
        let serialize = PyModule::import(py, "kolo.serialize")?;
        let msgpack = PyModule::import(py, "msgpack")?;
        let version = msgpack.getattr(intern!(py, "version"))?;
        let version: (u32, u32) = (
            version.get_item(0)?.extract()?,
            version.get_item(1)?.extract()?,
        );
        // msgpack 1.2 raised Packer's DEFAULT_RECURSE_LIMIT from 511.
        let recurse_limit = if version >= (1, 2) { 1024 } else { 511 };
        let object_type = ptr::addr_of_mut!(ffi::PyBaseObject_Type);
        // Safety: `object` is a static type and both names are interned str.
        let (object_class, object_getattribute) = unsafe {
            (
                _PyType_Lookup(object_type, intern!(py, "__class__").as_ptr()) as usize,
                _PyType_Lookup(object_type, intern!(py, "__getattribute__").as_ptr()) as usize,
            )
        };
        assert!(object_class != 0 && object_getattribute != 0);
        let method_type = {
            // Safety: binds None to None; the method only lives here.
            let method = unsafe {
                Bound::from_owned_ptr_or_err(
                    py,
                    PyMethod_New(py.None().as_ptr(), py.None().as_ptr()),
                )?
            };
            method.get_type()
        };
        let globals = serialize.dict();
        Ok(Self {
            #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
            type_getattro: unsafe { (*ptr::addr_of!(ffi::PyType_Type)).tp_getattro }
                .map_or(0, |getattro| getattro as usize),
            #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
            method_getattro: unsafe { (*method_type.as_type_ptr()).tp_getattro }
                .map_or(0, |getattro| getattro as usize),
            #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
            globals_watched: type_ladder::watch_globals(&globals),
            #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
            builtin_reprs: BuiltinReprs::new(py),
            globals: globals.unbind(),
            ext_type: msgpack.getattr(intern!(py, "ExtType"))?.unbind(),
            timestamp_type: msgpack.getattr(intern!(py, "Timestamp"))?.unbind(),
            packb: msgpack.getattr(intern!(py, "packb"))?.unbind(),
            method_type: method_type.as_ptr() as usize,
            recurse_limit,
            object_class,
            object_getattribute,
            #[cfg(test)]
            python_dump_msgpack: serialize.getattr(intern!(py, "dump_msgpack"))?.unbind(),
            #[cfg(test)]
            python_dump_msgpack_lightweight_repr: serialize
                .getattr(intern!(py, "dump_msgpack_lightweight_repr"))?
                .unbind(),
        })
    }

    pub fn dump_msgpack(
        &self,
        py: Python,
        data: &Bound<'_, PyAny>,
        lightweight_repr: bool,
    ) -> Result<Vec<u8>, PyErr> {
        let mut buf = Vec::new();
        self.dump_msgpack_into(py, data, lightweight_repr, &mut buf)?;
        Ok(buf)
    }

    /// Append `data` exactly as `kolo.serialize.dump_msgpack` would encode it.
    /// On error `buf` is left unchanged.
    pub(crate) fn dump_msgpack_into(
        &self,
        _py: Python,
        data: &Bound<'_, PyAny>,
        lightweight_repr: bool,
        buf: &mut Vec<u8>,
    ) -> Result<(), PyErr> {
        NativeMsgpackEncoder::new(self, lightweight_repr)
            .encode(data, buf)
            .map_err(EncodeError::into_pyerr)
    }

    /// `dump_msgpack(data)` under the value budget: a dict over budget as a
    /// whole is capped per value instead (see
    /// `NativeMsgpackEncoder::encode_capped_map`), as
    /// `kolo.serialize.dump_frame_msgpack` does for plugin frames.
    pub(crate) fn dump_msgpack_capped(
        &self,
        data: &Bound<'_, PyAny>,
        lightweight_repr: bool,
        max_value_bytes: Option<usize>,
    ) -> Result<Vec<u8>, PyErr> {
        let mut buf = Vec::new();
        let mut encoder = NativeMsgpackEncoder::new(self, lightweight_repr);
        encoder.set_value_budget(max_value_bytes);
        encoder.encode_capped_map(data, &mut buf)?;
        Ok(buf)
    }

    /// The Python reference implementation the native encoder mirrors.
    #[cfg(test)]
    pub(crate) fn python_dump_msgpack(
        &self,
        py: Python,
        data: &Bound<'_, PyAny>,
        lightweight_repr: bool,
    ) -> Result<Vec<u8>, PyErr> {
        let serializer = match lightweight_repr {
            false => self.python_dump_msgpack.bind(py),
            true => self.python_dump_msgpack_lightweight_repr.bind(py),
        };
        Ok(serializer
            .call1((data,))?
            .cast_into::<PyBytes>()?
            .as_bytes()
            .to_vec())
    }
}

const VALUE_REFERENCE_EXTENSION_TYPE: i8 = 9;
const MIN_INTERNED_VALUE_BYTES: usize = 4 * 1024;
const MAX_INTERNED_VALUE_BYTES: usize = 16 * 1024 * 1024;
const MAX_INTERNED_VALUES: usize = 4096;
const MAX_VALUE_TABLE_BYTES: usize = 16 * 1024 * 1024;
const MAX_TRACKED_VALUE_IDENTITIES: usize = 2048;
const MAX_VALUE_CANDIDATE_BYTES: usize = 4 * 1024 * 1024;

#[derive(Default)]
struct ValueInterner {
    values: HashMap<usize, CachedValue>,
    candidate_bytes: usize,
}

enum CachedValue {
    Seen(ValueSignature),
    Candidate(Arc<InternedValue>),
    Interned { value: Arc<InternedValue>, id: u32 },
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum InternedValueKind {
    String,
    Bytes,
}

#[derive(Clone, Copy, PartialEq, Eq)]
struct ValueSignature {
    kind: InternedValueKind,
    len: usize,
    prefix: u64,
    suffix: u64,
}

impl ValueSignature {
    fn new(kind: InternedValueKind, payload: &[u8]) -> Self {
        fn fragment(payload: &[u8]) -> u64 {
            let mut bytes = [0; 8];
            let len = payload.len().min(bytes.len());
            bytes[..len].copy_from_slice(&payload[..len]);
            u64::from_le_bytes(bytes)
        }

        Self {
            kind,
            len: payload.len(),
            prefix: fragment(payload),
            suffix: fragment(&payload[payload.len().saturating_sub(8)..]),
        }
    }
}

struct InternedValue {
    encoded: Arc<[u8]>,
    payload_start: usize,
    kind: InternedValueKind,
    // A strong reference makes the address a permanent identity: CPython cannot reuse it.
    object: Py<PyAny>,
}

impl InternedValue {
    fn matches(&self, identity: usize, kind: InternedValueKind, payload: &[u8]) -> bool {
        let matches = self.kind == kind && self.object.as_ptr() as usize == identity;
        debug_assert!(!matches || self.encoded[self.payload_start..] == *payload);
        matches
    }

    fn resident_len(&self) -> usize {
        self.encoded
            .len()
            .saturating_add(self.encoded.len().saturating_sub(self.payload_start))
    }
}

#[derive(Debug, PartialEq, Eq)]
enum ValueLookup {
    ReferenceWritten,
    WriteInline,
    CacheCurrent,
    WriterCircuit(String),
}

impl ValueInterner {
    fn remove(&mut self, identity: usize, global_candidate_bytes: &AtomicUsize) {
        if let Some(CachedValue::Candidate(value)) = self.values.remove(&identity) {
            self.candidate_bytes = self.candidate_bytes.saturating_sub(value.resident_len());
            global_candidate_bytes.fetch_sub(value.resident_len(), Ordering::Relaxed);
        }
    }

    fn evict_one(
        &mut self,
        except: usize,
        candidates_only: bool,
        global_candidate_bytes: &AtomicUsize,
    ) -> bool {
        let victim = self.values.iter().find_map(|(identity, cached)| {
            (*identity != except
                && (!candidates_only || matches!(cached, CachedValue::Candidate(_))))
            .then_some(*identity)
        });
        if let Some(victim) = victim {
            self.remove(victim, global_candidate_bytes);
            true
        } else {
            false
        }
    }

    fn make_identity_room(&mut self, identity: usize, global_candidate_bytes: &AtomicUsize) {
        if !self.values.contains_key(&identity) && self.values.len() >= MAX_TRACKED_VALUE_IDENTITIES
        {
            self.evict_one(identity, false, global_candidate_bytes);
        }
    }

    fn make_candidate_room(
        &mut self,
        identity: usize,
        encoded_len: usize,
        global_candidate_bytes: &AtomicUsize,
    ) -> bool {
        while self.candidate_bytes.saturating_add(encoded_len) > MAX_VALUE_CANDIDATE_BYTES {
            if !self.evict_one(identity, true, global_candidate_bytes) {
                return false;
            }
        }
        loop {
            if global_candidate_bytes
                .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |current| {
                    current
                        .checked_add(encoded_len)
                        .filter(|next| *next <= MAX_VALUE_CANDIDATE_BYTES)
                })
                .is_ok()
            {
                return true;
            }
            if !self.evict_one(identity, true, global_candidate_bytes) {
                return false;
            }
        }
    }
}

#[derive(Default)]
struct ValueTable {
    entries: Vec<Arc<InternedValue>>,
    resident_bytes: usize,
}

impl ValueTable {
    fn insert_value(&mut self, value: Arc<InternedValue>) -> Option<u32> {
        if self.entries.len() >= MAX_INTERNED_VALUES
            || self.resident_bytes.saturating_add(value.resident_len()) > MAX_VALUE_TABLE_BYTES
        {
            return None;
        }
        let id = u32::try_from(self.entries.len()).expect("value table is bounded");
        self.resident_bytes += value.resident_len();
        self.entries.push(Arc::clone(&value));
        Some(id)
    }

    fn remove_last(&mut self, id: u32) {
        assert_eq!(
            self.entries.len().checked_sub(1),
            Some(id as usize),
            "value-table rollback must remove its newest unpublished entry"
        );
        let value = self
            .entries
            .pop()
            .expect("value-table entry was just inserted");
        self.resident_bytes = self.resident_bytes.saturating_sub(value.resident_len());
    }

    #[cfg(test)]
    fn snapshot_all(&self) -> Vec<(u32, Arc<[u8]>)> {
        self.entries
            .iter()
            .enumerate()
            .map(|(id, value)| {
                (
                    u32::try_from(id).expect("value table is bounded"),
                    Arc::clone(&value.encoded),
                )
            })
            .collect()
    }

    fn snapshot_ids(&self, ids: &[u32]) -> Vec<(u32, Arc<[u8]>)> {
        ids.iter()
            .filter_map(|id| {
                self.entries
                    .get(*id as usize)
                    .map(|value| (*id, Arc::clone(&value.encoded)))
            })
            .collect()
    }
}

pub struct ValueInterning {
    interners: ThreadLocal<RefCell<ValueInterner>>,
    table: Mutex<ValueTable>,
    disabled: AtomicBool,
    candidate_bytes: AtomicUsize,
    repr_reuse: super::repr_reuse::ReprReuse,
}

impl Default for ValueInterning {
    fn default() -> Self {
        Self {
            interners: ThreadLocal::new(),
            table: Mutex::new(ValueTable::default()),
            disabled: AtomicBool::new(false),
            candidate_bytes: AtomicUsize::new(0),
            repr_reuse: super::repr_reuse::ReprReuse::default(),
        }
    }
}

impl ValueInterning {
    /// Free cached reprs at session end (they hold no program objects).
    pub fn release_repr_reuse(&self) {
        self.repr_reuse.release();
    }

    #[cfg(test)]
    pub fn snapshot_all(&self) -> Vec<(u32, Arc<[u8]>)> {
        self.table
            .lock()
            .expect("value table mutex poisoned")
            .snapshot_all()
    }

    pub fn snapshot_ids(&self, ids: &[u32]) -> Vec<(u32, Arc<[u8]>)> {
        self.table
            .lock()
            .expect("value table mutex poisoned")
            .snapshot_ids(ids)
    }
}

#[derive(Clone, Copy)]
enum ValueCapture<'a> {
    Fixed(&'a TraceCapture),
    #[cfg(not(Py_GIL_DISABLED))]
    Current(&'a Mutex<Arc<TraceCapture>>),
}

#[derive(Clone, Copy)]
pub(crate) struct ValueInterningContext<'a> {
    interning: &'a ValueInterning,
    capture: ValueCapture<'a>,
}

impl<'a> ValueInterningContext<'a> {
    pub(crate) fn fixed(interning: &'a ValueInterning, capture: &'a TraceCapture) -> Self {
        Self {
            interning,
            capture: ValueCapture::Fixed(capture),
        }
    }

    #[cfg(not(Py_GIL_DISABLED))]
    pub(crate) fn current(
        interning: &'a ValueInterning,
        capture: &'a Mutex<Arc<TraceCapture>>,
    ) -> Self {
        Self {
            interning,
            capture: ValueCapture::Current(capture),
        }
    }

    fn publish_value(&self, id: u32, value: Arc<[u8]>) -> io::Result<()> {
        match self.capture {
            ValueCapture::Fixed(capture) => capture.publish_value(id, value),
            #[cfg(not(Py_GIL_DISABLED))]
            ValueCapture::Current(capture) => {
                let capture = Arc::clone(&capture.lock().expect("trace capture mutex poisoned"));
                capture.publish_value(id, value)
            }
        }
    }

    fn writer_circuit_is_open(&self) -> bool {
        match self.capture {
            ValueCapture::Fixed(capture) => capture.writer_circuit_is_open(),
            #[cfg(not(Py_GIL_DISABLED))]
            ValueCapture::Current(capture) => {
                Arc::clone(&capture.lock().expect("trace capture mutex poisoned"))
                    .writer_circuit_is_open()
            }
        }
    }
}

fn write_value_reference(buf: &mut Vec<u8>, id: u32) {
    rmp::encode::write_ext_meta(buf, 4, VALUE_REFERENCE_EXTENSION_TYPE)
        .expect("Writing to memory, not I/O");
    buf.extend_from_slice(&id.to_be_bytes());
}

// Repeated lists/dicts in one root are written as back-references; this rule must match
// `_replay_shared_reference_rule` in kolo/serialize.py.
const SHARED_REFERENCE_EXTENSION_TYPE: i8 = 11;
const SHARED_TRACKING_THRESHOLD: u32 = 1024;
// Cap remembered containers because their pins and table entries can dwarf the encoded value.
const MAX_SHARED_CONTAINERS: usize = 1 << 18;
const TRUNCATED_VALUE_EXTENSION_TYPE: i8 = 12;
// Check scalar runs periodically; the interval bounds budget overshoot.
const BUDGET_CHECK_MASK: usize = 0xff;
const MAX_MARKER_TYPE_NAME_CHARS: usize = 200;
// Frame fields `encode_capped_map` never caps, as `_ENVELOPE_KEYS` in
// kolo/serialize.py.
const ENVELOPE_KEYS: [&str; 9] = [
    "path",
    "co_name",
    "qualname",
    "event",
    "frame_id",
    "timestamp",
    "type",
    "user_code_call_site",
    "subtype",
];
// How to raise the budget, appended to every truncation marker (as
// `TRUNCATION_MARKER_HINT` in kolo/serialize.py).
pub(super) const TRUNCATION_MARKER_HINT: &str =
    "; raise max_value_mb in .kolo/config.toml or set it to false";

/// Identity tracking for one root once it has packed
/// `SHARED_TRACKING_THRESHOLD` plain containers.
#[derive(Default)]
struct SharedContainers {
    /// Arrays and maps completed in the root's stream since tracking began.
    completed: u64,
    /// The completion number of each remembered container.
    numbers: HashMap<usize, u64>,
    /// Strong references, so a remembered identity cannot be reused by a new
    /// object while the root is packed.
    pins: Vec<SnapshotRef>,
}

fn checked_msgpack_len(len: usize) -> Option<u32> {
    u32::try_from(len).ok()
}

pub(crate) enum EncodeError {
    Python(PyErr),
    WriterCircuit(String),
    OverBudget,
}

impl EncodeError {
    pub(crate) fn into_pyerr(self) -> PyErr {
        match self {
            EncodeError::Python(error) => error,
            EncodeError::WriterCircuit(error) => PyOSError::new_err(error),
            EncodeError::OverBudget => PyValueError::new_err("value exceeds max_value_mb"),
        }
    }
}

/// Whether `NativeMsgpackEncoder::encode_value` wrote the value itself or,
/// because it exceeded the value budget, a truncation marker.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Encoded {
    Complete,
    OverBudget,
}

/// Failure marker for the recursive encoder; the cause is kept in
/// `NativeMsgpackEncoder::error` so the hot recursion returns a single byte.
struct Fail;

type Packed = Result<(), Fail>;

pub(super) const MAX_EXT_HEADER_LEN: usize = 6;
// Containers nested natively before Pyodide's WebAssembly stack runs out
// well below msgpack's own nesting limit.
#[cfg(target_family = "wasm")]
const WASM_MAX_NATIVE_DEPTH: u32 = 128;
const PY_TUPLE_EXTENSION_TYPE: i8 = 6;
const PY_SET_EXTENSION_TYPE: i8 = 7;
const PY_FROZENSET_EXTENSION_TYPE: i8 = 8;
const SERIALIZATION_ERROR_EXTENSION_TYPE: i8 = 127;
// `msgpack_encode_hook` -> `_dump_msgpack` -> `_pack_with_msgpack` are the
// Python frames each nested tuple/set/frozenset costs the Python serializer.
const PYTHON_FRAMES_PER_NESTED_EXTENSION: i32 = 3;
const PYTHON_FRAMES_PER_CAREFUL_NESTED_EXTENSION: i32 = 4;
const FIRST_PASS_CYCLE_CHECK_DEPTH: i32 = 8;
const REPR_EXTENSION_TYPE: i8 = 0;
/// A str with lone surrogates, as `str.encode("utf-8", "surrogatepass")`.
const SURROGATE_STR_EXTENSION_TYPE: i8 = 10;
const LIST_CYCLE_MARKER: &[u8] = b"[...]";
const DICT_CYCLE_MARKER: &[u8] = b"{...}";
const TUPLE_CYCLE_MARKER: &[u8] = b"(...)";
const SET_CYCLE_MARKER: &[u8] = b"set(...)";
const FROZENSET_CYCLE_MARKER: &[u8] = b"frozenset(...)";
// msgpack's own messages, which `kolo.serialize._needs_careful` matches.
const RECURSION_LIMIT_MESSAGE: &str = "recursion limit exceeded.";
// msgpack's pure-Python packer's wording (no period).
const FALLBACK_RECURSION_LIMIT_MESSAGE: &str = "recursion limit exceeded";
const RELEASED_MEMORYVIEW_MESSAGE: &str = "operation forbidden on released memoryview object";

/// `kolo.serialize._needs_careful`: whether a root that failed with `error`
/// is encoded again carefully. Exact types only, so deciding runs no user
/// code.
fn needs_careful(py: Python<'_>, error: &PyErr) -> bool {
    let value = error.value(py);
    // Safety: compares a live exception's type with static exception types.
    let error_type = unsafe { ffi::Py_TYPE(value.as_ptr()).cast::<ffi::PyObject>() };
    if error_type == unsafe { ffi::PyExc_RecursionError } {
        return true;
    }
    if error_type == unsafe { ffi::PyExc_ValueError } {
        return exact_value_error_is(py, error, RECURSION_LIMIT_MESSAGE)
            || exact_value_error_is(py, error, FALLBACK_RECURSION_LIMIT_MESSAGE)
            || exact_value_error_is(py, error, RELEASED_MEMORYVIEW_MESSAGE);
    }
    if error_type == unsafe { ffi::PyExc_UnicodeEncodeError } {
        return value
            .getattr(intern!(py, "reason"))
            .ok()
            .is_some_and(|reason| exact_str_is(&reason, "surrogates not allowed"));
    }
    false
}

/// Whether `error` is an exact `ValueError(message)`.
fn exact_value_error_is(py: Python<'_>, error: &PyErr, message: &str) -> bool {
    let value = error.value(py);
    // Safety: compares a live exception's type with a static exception type.
    if unsafe { ffi::Py_TYPE(value.as_ptr()).cast::<ffi::PyObject>() != ffi::PyExc_ValueError } {
        return false;
    }
    let Ok(args) = value.getattr(intern!(py, "args")) else {
        return false;
    };
    let Ok(args) = args.cast_exact::<PyTuple>() else {
        return false;
    };
    args.len() == 1
        && args
            .get_item(0)
            .is_ok_and(|argument| exact_str_is(&argument, message))
}

fn exact_str_is(value: &Bound<'_, PyAny>, expected: &str) -> bool {
    value
        .cast_exact::<PyString>()
        .is_ok_and(|text| text.to_str().is_ok_and(|text| text == expected))
}

/// What `msgpack_encode_hook` returned, for the Packer to pack next.
enum Defaulted<'py> {
    Ext(i8, Payload<'py>),
    /// An ExtType whose data is natively written repr text in
    /// `ReprMemo::arena`.
    NativeExt(i8, Range<usize>),
    /// A sequence extension whose items are already encoded after a
    /// reserved header at `start`.
    Sequence(i8, usize),
    /// `dict(obj)` for a dict subclass, packed (outside the hook's `try`)
    /// as a plain map.
    Dict(Bound<'py, PyDict>),
    /// The careful pass's repr-text marker for a container already being
    /// packed.
    CycleMarker(&'static [u8]),
    /// A payload known to end past the budget before it was built.
    OverBudget,
}

/// Extension payload bytes, validated as `msgpack.ExtType` requires.
enum Payload<'py> {
    /// An exact str whose UTF-8 form (`.encode("utf-8")`) is known to exist.
    Text(Bound<'py, PyString>),
    Bytes(Bound<'py, PyBytes>),
}

impl Payload<'_> {
    /// The Packer takes an ExtType's length from `len(data)`, which a bytes
    /// subclass may override.
    fn packed_len(&self) -> PyResult<usize> {
        let actual = self.as_bytes().len();
        let Payload::Bytes(bytes) = self else {
            return Ok(actual);
        };
        if bytes.is_exact_instance_of::<PyBytes>() {
            return Ok(actual);
        }
        let len = bytes.len()?;
        if len > actual {
            return Err(PyValueError::new_err("EXT data length exceeds its buffer"));
        }
        Ok(len)
    }

    fn as_bytes(&self) -> &[u8] {
        match self {
            Payload::Text(text) => text
                .to_str()
                .expect("payload text was validated as UTF-8")
                .as_bytes(),
            Payload::Bytes(bytes) => bytes.as_bytes(),
        }
    }
}

/// A `repr()` result: a Python str, or the text CPython's builtin `tp_repr`
/// would have produced (an exact str's contents), written natively into the
/// encoder's `ReprMemo::arena`.
#[derive(Clone)]
enum ReprText<'py> {
    Py(Bound<'py, PyAny>),
    Native(Range<usize>),
}

/// `value.encode("utf-8")`, checked like `msgpack.ExtType(code, data)`.
fn utf8_payload(value: Bound<'_, PyAny>) -> PyResult<Payload<'_>> {
    if let Ok(text) = value.cast_exact::<PyString>() {
        text.to_str()?;
        return Ok(Payload::Text(text.clone()));
    }
    let py = value.py();
    bytes_payload(value.call_method1(intern!(py, "encode"), (intern!(py, "utf-8"),))?)
}

/// `value.encode("utf-8", "backslashreplace")` for a str: the error marker's
/// type path, which can hold lone surrogates.
fn escaped_utf8_payload(value: Bound<'_, PyAny>) -> PyResult<Payload<'_>> {
    if let Ok(text) = value.cast_exact::<PyString>() {
        if text.to_str().is_ok() {
            return Ok(Payload::Text(text.clone()));
        }
    }
    let py = value.py();
    bytes_payload(value.call_method1(
        intern!(py, "encode"),
        (intern!(py, "utf-8"), intern!(py, "backslashreplace")),
    )?)
}

fn bytes_payload(value: Bound<'_, PyAny>) -> PyResult<Payload<'_>> {
    match value.cast_into::<PyBytes>() {
        Ok(bytes) => Ok(Payload::Bytes(bytes)),
        Err(_) => Err(PyTypeError::new_err("data must be bytes")),
    }
}

/// `PyObject_GetOptionalAttr`: `None` when the attribute is missing. Unlike
/// `getattr` plus catching AttributeError, a generic lookup raises nothing
/// and a suppressed AttributeError is never annotated with `name`/`obj`.
fn optional_attr<'py>(
    value: &Bound<'py, PyAny>,
    name: &Bound<'py, PyString>,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    let py = value.py();
    let mut result = ptr::null_mut();
    // Safety: live object and str; `result` receives a new reference or NULL.
    let found = unsafe {
        #[cfg(Py_3_13)]
        let found = ffi::PyObject_GetOptionalAttr(value.as_ptr(), name.as_ptr(), &mut result);
        #[cfg(not(Py_3_13))]
        let found = _PyObject_LookupAttr(value.as_ptr(), name.as_ptr(), &mut result);
        found
    };
    match found {
        -1 => Err(PyErr::fetch(py)),
        // Safety: a found attribute is a new reference.
        1 => Ok(Some(unsafe { Bound::from_owned_ptr(py, result) })),
        _ => Ok(None),
    }
}

/// One f-string replacement field: `f"{value}"`.
fn format_field<'py>(value: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyString>> {
    if let Ok(text) = value.cast_exact::<PyString>() {
        return Ok(text.clone());
    }
    // Safety: a NULL format spec is the f-string conversion-free default.
    unsafe {
        Bound::from_owned_ptr_or_err(
            value.py(),
            ffi::PyObject_Format(value.as_ptr(), ptr::null_mut()),
        )?
        .cast_into::<PyString>()
        .map_err(Into::into)
    }
}

fn concat_text<'py>(parts: &[&Bound<'py, PyString>]) -> PyResult<Bound<'py, PyAny>> {
    let py = parts[0].py();
    let mut joined = parts[0].clone().into_any();
    for part in &parts[1..] {
        // Safety: both operands are str objects.
        joined = unsafe {
            Bound::from_owned_ptr_or_err(py, ffi::PyUnicode_Concat(joined.as_ptr(), part.as_ptr()))?
        };
    }
    Ok(joined)
}

fn write_ext(buf: &mut Vec<u8>, code: i8, payload: &[u8]) -> PyResult<()> {
    let Some(len) = checked_msgpack_len(payload.len()) else {
        return Err(PyValueError::new_err("EXT data is too large"));
    };
    rmp::encode::write_ext_meta(buf, len, code).expect("Writing to memory, not I/O");
    buf.extend_from_slice(payload);
    Ok(())
}

/// Replace the reserved header at `start` with the real extension header
/// for the bytes encoded after it.
pub(super) fn finish_reserved_extension(
    buf: &mut Vec<u8>,
    start: usize,
    code: i8,
) -> PyResult<()> {
    let inner_start = start + MAX_EXT_HEADER_LEN;
    let Some(inner_len) = checked_msgpack_len(buf.len() - inner_start) else {
        return Err(PyValueError::new_err("EXT data is too large"));
    };
    let mut header = [0; MAX_EXT_HEADER_LEN];
    let mut cursor = Cursor::new(&mut header[..]);
    rmp::encode::write_ext_meta(&mut cursor, inner_len, code)
        .expect("fixed-size extension header always fits");
    let header_len = cursor.position() as usize;
    let end = buf.len();
    if header_len < MAX_EXT_HEADER_LEN {
        buf.copy_within(inner_start..end, start + header_len);
        buf.truncate(end - (MAX_EXT_HEADER_LEN - header_len));
    }
    buf[start..start + header_len].copy_from_slice(&header[..header_len]);
    Ok(())
}

/// A strong reference held on the snapshot stack, released by
/// `NativeMsgpackEncoder::release_snapshot`. Raw rather than `Py<PyAny>`,
/// whose drop checks thread attachment through a thread-local per item.
type SnapshotRef = *mut ffi::PyObject;

/// The encoder's snapshot stack. The first entries live inline, so the
/// common frame (a locals dict holding `self` or a tuple) never allocates;
/// deeper or larger snapshots spill to a `Vec`.
struct SnapshotStack {
    inline: [std::mem::MaybeUninit<SnapshotRef>; SNAPSHOT_INLINE],
    spill: Vec<SnapshotRef>,
    len: usize,
}

const SNAPSHOT_INLINE: usize = 16;

impl SnapshotStack {
    #[inline(always)]
    fn new() -> Self {
        Self {
            inline: [std::mem::MaybeUninit::uninit(); SNAPSHOT_INLINE],
            spill: Vec::new(),
            len: 0,
        }
    }

    #[inline(always)]
    fn len(&self) -> usize {
        self.len
    }

    #[inline(always)]
    fn is_empty(&self) -> bool {
        self.len == 0
    }

    #[inline]
    fn push(&mut self, object: SnapshotRef) {
        if self.len < SNAPSHOT_INLINE {
            self.inline[self.len].write(object);
        } else {
            self.spill.push(object);
        }
        self.len += 1;
    }

    /// Forget the entries from `len` on, which the caller has released.
    #[inline]
    fn truncate(&mut self, len: usize) {
        if len < self.len {
            self.spill.truncate(len.saturating_sub(SNAPSHOT_INLINE));
            self.len = len;
        }
    }

    #[inline]
    fn get(&self, index: usize) -> SnapshotRef {
        assert!(index < self.len, "snapshot index out of range");
        if index < SNAPSHOT_INLINE {
            // Safety: entries below `len` were written by `push`.
            unsafe { self.inline[index].assume_init() }
        } else {
            self.spill[index - SNAPSHOT_INLINE]
        }
    }
}

/// Push owned references to an exact list's items from `start` on onto
/// `snapshot` and return how many. Runs no Python code, so nothing can
/// resize the list while its items are copied.
fn snapshot_list_items(
    list: &Bound<'_, PyList>,
    start: usize,
    snapshot: &mut SnapshotStack,
) -> usize {
    pyo3::sync::critical_section::with_critical_section(list.as_any(), || {
        // Safety: `list` is a live exact list, locked on free-threaded
        // builds; each borrowed item becomes an owned reference before
        // anything else can run.
        unsafe {
            let len = ffi::PyList_GET_SIZE(list.as_ptr()) as usize;
            let copied = len.saturating_sub(start);
            for index in start..len {
                let item = ffi::PyList_GET_ITEM(list.as_ptr(), index as ffi::Py_ssize_t);
                ffi::Py_INCREF(item);
                snapshot.push(item);
            }
            copied
        }
    })
}

/// Push owned references to an exact dict's keys and values, interleaved,
/// from `PyDict_Next` position `position` on onto `snapshot` and return the
/// number of entries. Like `snapshot_list_items`, runs no Python code.
fn snapshot_dict_items(
    dict: &Bound<'_, PyDict>,
    mut position: ffi::Py_ssize_t,
    snapshot: &mut SnapshotStack,
) -> usize {
    pyo3::sync::critical_section::with_critical_section(dict.as_any(), || {
        let mut len = 0;
        let mut key = ptr::null_mut();
        let mut value = ptr::null_mut();
        // Safety: `dict` is a live dict, locked on free-threaded builds;
        // the borrowed results become owned references immediately.
        unsafe {
            while ffi::PyDict_Next(dict.as_ptr(), &mut position, &mut key, &mut value) != 0 {
                ffi::Py_INCREF(key);
                ffi::Py_INCREF(value);
                snapshot.push(key);
                snapshot.push(value);
                len += 1;
            }
        }
        len
    })
}

/// The recursion guard `PyObject_Repr` enters, entered and left at once:
/// fails exactly where a repr at this depth would.
fn recursion_check(py: Python<'_>) -> PyResult<()> {
    // Python 3.8's guard is a macro over thread state; bound methods are not
    // composed there, so nothing calls this.
    #[cfg(Py_3_9)]
    // Safety: plain C API calls; a successful enter is always left.
    unsafe {
        if ffi::Py_EnterRecursiveCall(c" while getting the repr of an object".as_ptr()) != 0 {
            return Err(PyErr::fetch(py));
        }
        ffi::Py_LeaveRecursiveCall();
    }
    #[cfg(not(Py_3_9))]
    let _ = py;
    Ok(())
}

/// `repr()` results already computed while encoding one event, by object
/// identity. Each entry holds a strong reference to its object so the
/// identity cannot be reused before the encoder is dropped. Events repr only
/// a handful of objects, so the first entries live inline (no allocation per
/// event) and are scanned linearly until there are enough to be worth hashing.
/// Past `REPR_MEMO_CAPACITY` entries nothing more is memoized, which bounds
/// how many objects (such as temporaries a user `__iter__` creates) an event
/// keeps alive; later objects are repr'd on every occurrence.
#[derive(Default)]
struct ReprMemo {
    /// Natively written repr texts, back to back, so they need no
    /// allocation of their own. Always valid UTF-8.
    arena: Vec<u8>,
    inline: [Option<ReprMemoEntry>; REPR_MEMO_INLINE],
    spilled: Vec<ReprMemoEntry>,
    index: Option<HashMap<usize, usize>>,
    len: usize,
}

type ReprMemoEntry = (usize, Py<PyAny>, MemoText);

enum MemoText {
    Py(Py<PyString>),
    Native(Range<usize>),
}

const REPR_MEMO_INLINE: usize = 8;
const REPR_TEXT_RESERVE: usize = 128;
const REPR_MEMO_SCAN_LIMIT: usize = 16;
const REPR_MEMO_CAPACITY: usize = 1024;

impl ReprMemo {
    fn entry(&self, position: usize) -> &ReprMemoEntry {
        match self.inline.get(position) {
            Some(entry) => entry.as_ref().expect("inline entries below len are set"),
            None => &self.spilled[position - REPR_MEMO_INLINE],
        }
    }

    fn get<'py>(&self, py: Python<'py>, identity: usize) -> Option<ReprText<'py>> {
        let position = match &self.index {
            None => (0..self.len).find(|&position| self.entry(position).0 == identity)?,
            Some(index) => *index.get(&identity)?,
        };
        Some(match &self.entry(position).2 {
            MemoText::Py(text) => ReprText::Py(text.bind(py).clone().into_any()),
            MemoText::Native(text) => ReprText::Native(text.clone()),
        })
    }

    fn insert(&mut self, value: &Bound<'_, PyAny>, text: MemoText) {
        if self.len == REPR_MEMO_CAPACITY {
            return;
        }
        let identity = value.as_ptr() as usize;
        let entry = (identity, value.clone().unbind(), text);
        match self.inline.get_mut(self.len) {
            Some(slot) => *slot = Some(entry),
            None => self.spilled.push(entry),
        }
        self.len += 1;
        match &mut self.index {
            Some(index) => {
                index.insert(identity, self.len - 1);
            }
            None if self.len > REPR_MEMO_SCAN_LIMIT => {
                let index = (0..self.len)
                    .map(|position| (self.entry(position).0, position))
                    .collect();
                self.index = Some(index);
            }
            None => {}
        }
    }
}

/// Encoder reproducing `msgpack.Packer(default=msgpack_encode_hook,
/// strict_types=True).pack(value)` byte for byte, including every call into
/// user code (`__repr__`, `__class__`, `isoformat`, ...) in the same order and
/// number, and the same exceptions.
///
/// `pack` mirrors `Packer._pack`: exact builtins are packed directly and
/// everything else goes through `call_default`, a native transcription of
/// `msgpack_encode_hook` (or its lightweight-repr variant).
///
/// One deliberate divergence: an exact list or dict is packed as it was when
/// packing it started. Its items are snapshotted before any of them is
/// packed, because packing one can run user code that resizes the container
/// itself. msgpack writes the array/map header from the starting length and
/// then iterates the live container, so a `__repr__` that appends to or
/// removes from it makes the header disagree with the items written, and the
/// whole trace becomes undecodable (a dict that changes size instead raises
/// RuntimeError, losing the frame). The snapshot keeps the header and items
/// consistent and records the container's state at the event. A `__repr__`
/// that replaces an entry not yet packed (`parent[1] = x`) is likewise not
/// seen. Values whose user code does not change the list or dict it is being
/// packed from encode byte for byte as in Python.
///
/// Large exact str/bytes may additionally be written as value references when
/// interning is enabled; readers expand those before exposing a value.
///
/// Within one root, a list or dict packed again after identity tracking
/// started is written as a shared reference (see
/// `SHARED_REFERENCE_EXTENSION_TYPE`), exactly as `kolo.serialize` writes it.
/// A reference repeats the container as it was packed the first time, so a
/// `__repr__` that changes it in between is not seen.
///
/// One deliberate exception to "same number of calls": an encoder lives for
/// one trace event (both its `arg` and `locals` roots), and `repr()` runs at
/// most once per object identity in it. A repeated object, or the `__self__`
/// of a bound method (composed natively as `method_repr` does), reuses the
/// earlier result. Only Kolo's encoder and the user code the hook itself
/// runs (`__repr__`, `__class__`, `isoformat`, ...) execute between two such
/// reprs, so the bytes differ only if that user code changes what a repr
/// within the same event returns, or a repr is non-deterministic. Memoized
/// objects also stay alive until the encoder is dropped, which delays the
/// finalizers of objects that would otherwise die mid-encode (temporaries
/// from a user `__iter__`, or values a repr removes from their container),
/// though they still run with the query guard on (see `Drop`).
/// The rest of the hook ladder still runs per value.
///
/// Likewise, the first pass stops following a cycle through tuple, set or
/// frozenset payloads, or through dict subclass copies, once it repeats
/// (from `FIRST_PASS_CYCLE_CHECK_DEPTH` levels on), where Python follows it
/// until RecursionError or msgpack's nesting limit. User code those repeats
/// would run (a set subclass's `__iter__`, say) runs fewer times; both then
/// record the value in the careful pass (see `careful`).
pub(super) struct NativeMsgpackEncoder<'a> {
    serializer: &'a SerializerState,
    lightweight_repr: bool,
    value_interning: Option<ValueInterningContext<'a>>,
    value_interner_cell: Option<&'a RefCell<ValueInterner>>,
    error: Option<EncodeError>,
    profiler_flag_set: bool,
    used_default_hook: bool,
    extension_depth: i32,
    repr_memo: ReprMemo,
    native_depth: u32,
    /// Set while re-encoding a root that failed on a cycle (as nesting past
    /// msgpack's limit or a RecursionError), a str with lone surrogates, or a
    /// released memoryview: `kolo.serialize`'s careful pass. Each container
    /// already being packed is then written as Python's repr writes a
    /// recursive reference (`[...]`), such a str as a
    /// `SURROGATE_STR_EXTENSION_TYPE` extension, and such a memoryview as its
    /// repr. Only failing roots pay for this; the first pass is unchanged.
    careful: bool,
    /// Identities of the containers being packed during the careful pass.
    active: Vec<usize>,
    /// Stack of owned references to the items of the lists and dicts being
    /// packed: each container pushes its snapshot on top, packs it, and
    /// releases back to where it started. Only allocated once a container
    /// actually needs a snapshot.
    snapshot: SnapshotStack,
    /// Plain containers the current root entered before tracking started.
    shared_entered: u32,
    shared: Option<Box<SharedContainers>>,
    /// Nesting inside dicts made by the default hook, whose containers are
    /// never referenced.
    hook_depth: u32,
    /// Cycle markers the careful pass has written: a container whose
    /// encoding holds one depends on what encloses it, so it is not shared.
    cycle_markers: u64,
    /// Bytes one root may take before it is replaced by a truncation marker.
    value_budget: Option<usize>,
    /// `buf` length past which the current root is over budget.
    budget_end: usize,
    /// Bytes of `buf` held by extension headers reserved at their largest
    /// size and not yet finished, which the wire format will not keep.
    reserved_header_bytes: usize,
    /// The objects whose constructor is running, found when the event first
    /// packs a value that could be one: the stack below Kolo does not change
    /// during an event.
    construction: Option<construction::UnderConstruction>,
}

impl Drop for NativeMsgpackEncoder<'_> {
    fn drop(&mut self) {
        // Still counted only if a panic unwound through the encode, skipping
        // `reset_profiler_flag`.
        let counted = std::mem::take(&mut self.profiler_flag_set);
        if !counted && self.repr_memo.len == 0 && self.snapshot.is_empty() && self.shared.is_none()
        {
            return;
        }
        // Releasing memoized objects (or, after a panic, a snapshot or pins)
        // can run their finalizers, so keep the query guard on until they
        // are gone, as Python's serializer drops its temporaries inside the
        // encode.
        if !counted {
            NATIVE_ENCODES.with(|count| count.set(count.get() + 1));
        }
        if !self.snapshot.is_empty() {
            self.release_snapshot(0);
        }
        self.release_shared();
        self.repr_memo = ReprMemo::default();
        NATIVE_ENCODES.with(|count| count.set(count.get() - 1));
    }
}

impl<'a> NativeMsgpackEncoder<'a> {
    pub(super) fn new(serializer: &'a SerializerState, lightweight_repr: bool) -> Self {
        Self {
            serializer,
            lightweight_repr,
            value_interning: None,
            value_interner_cell: None,
            error: None,
            profiler_flag_set: false,
            used_default_hook: false,
            extension_depth: 0,
            repr_memo: ReprMemo::default(),
            native_depth: 0,
            careful: false,
            active: Vec::new(),
            snapshot: SnapshotStack::new(),
            shared_entered: 0,
            shared: None,
            hook_depth: 0,
            cycle_markers: 0,
            value_budget: None,
            budget_end: usize::MAX,
            reserved_header_bytes: 0,
            construction: None,
        }
    }

    /// Replace any root whose encoding exceeds `value_budget` bytes by a
    /// truncation marker (see `encode_value`).
    // Set in place, not a by-value builder: the encoder is large and built per event,
    // so a move would be a memcpy on the hot path.
    pub(super) fn set_value_budget(&mut self, value_budget: Option<usize>) {
        self.value_budget = value_budget;
    }

    pub(super) fn with_value_interning(
        serializer: &'a SerializerState,
        lightweight_repr: bool,
        value_interning: Option<ValueInterningContext<'a>>,
    ) -> Self {
        let mut encoder = Self::new(serializer, lightweight_repr);
        encoder.value_interning = value_interning;
        encoder
    }

    /// Whether any value so far needed `msgpack_encode_hook` (other than an
    /// exact tuple, which the native encoder always supported).
    pub(super) fn used_default_hook(&self) -> bool {
        self.used_default_hook
    }

    /// Append one root exactly as `dump_msgpack(value)` would return it. On
    /// error `buf` is left unchanged.
    pub(super) fn encode(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
    ) -> Result<(), EncodeError> {
        self.encode_value(value, buf).map(|_| ())
    }

    /// Encode as the payload of a tuple extension, which never holds shared
    /// references (an assignment's `(name, value)` tuple).
    pub(super) fn enter_extension_payload(&mut self) {
        self.extension_depth += 1;
    }

    /// Encode `value` under the value budget. When it is an exact dict over
    /// budget as a whole, the budget applies to each of its values instead
    /// (keys are encoded without it), so one oversized plugin field becomes
    /// a truncation marker without losing the others. The frame writer's
    /// `encode_locals` does the same for locals; it stays a separate copy
    /// there because routing locals through this call measurably slowed the
    /// per-event hot path on CodSpeed.
    pub(crate) fn encode_capped_map(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
    ) -> Result<(), PyErr> {
        let start = buf.len();
        let encoded = self
            .encode_value(value, buf)
            .map_err(EncodeError::into_pyerr)?;
        if encoded == Encoded::Complete {
            return Ok(());
        }
        let Ok(dict) = value.cast_exact::<PyDict>() else {
            return Ok(());
        };
        buf.truncate(start);
        let items = dict.items();
        let Some(len) = checked_msgpack_len(items.len()) else {
            return Err(PyValueError::new_err("dict is too large"));
        };
        rmp::encode::write_map_len(buf, len).expect("Writing to memory, not I/O");
        for item in items.iter() {
            let (key, item) = item.extract::<(Bound<'_, PyAny>, Bound<'_, PyAny>)>()?;
            self.encode_unbudgeted(&key, buf)
                .map_err(EncodeError::into_pyerr)?;
            // A plugin frame's envelope is never capped: readers pair and
            // dispatch frames by it.
            let envelope = key
                .cast_exact::<PyString>()
                .ok()
                .and_then(|key| key.to_str().ok().map(|key| ENVELOPE_KEYS.contains(&key)))
                .unwrap_or(false);
            if envelope {
                self.encode_unbudgeted(&item, buf)
                    .map_err(EncodeError::into_pyerr)?;
            } else {
                self.encode_value(&item, buf)
                    .map_err(EncodeError::into_pyerr)?;
            }
        }
        Ok(())
    }

    /// `encode` without the value budget, for a local variable's name.
    pub(super) fn encode_unbudgeted(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
    ) -> Result<(), EncodeError> {
        let budget = self.value_budget.take();
        let encoded = self.encode(value, buf);
        self.value_budget = budget;
        encoded
    }

    /// `encode`, except that a root whose encoding exceeds the value budget
    /// is replaced by a truncation marker. Packing stops as soon as the
    /// budget is exceeded, so the cost of an oversized value is bounded too.
    pub(super) fn encode_value(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
    ) -> Result<Encoded, EncodeError> {
        let start = buf.len();
        self.budget_end = self
            .value_budget
            .map_or(usize::MAX, |budget| start.saturating_add(budget));
        self.reserved_header_bytes = 0;
        let mut packed = self.pack(value, buf, self.serializer.recurse_limit);
        if packed.is_err() && self.retry_carefully(value) {
            buf.truncate(start);
            self.release_shared();
            self.reserved_header_bytes = 0;
            self.careful = true;
            packed = self.pack(value, buf, self.serializer.recurse_limit);
            self.careful = false;
            self.active.clear();
        }
        if packed.is_ok() && buf.len() > self.budget_end {
            packed = self.over_budget();
        }
        self.release_shared();
        let reset = self.reset_profiler_flag(value.py());
        let result = match packed {
            Ok(()) => reset
                .map(|()| Encoded::Complete)
                .map_err(EncodeError::Python),
            Err(Fail) => match self
                .error
                .take()
                .expect("a failed encode records its error")
            {
                EncodeError::OverBudget => {
                    buf.truncate(start);
                    self.write_truncation_marker(value, buf);
                    reset
                        .map(|()| Encoded::OverBudget)
                        .map_err(EncodeError::Python)
                }
                error => Err(error),
            },
        };
        if result.is_err() {
            buf.truncate(start);
        }
        result
    }

    /// `ExtType(12, f"{type(value).__qualname__} exceeded max_value_mb
    /// ({budget} bytes){hint}")`, as `kolo.serialize.truncation_marker`
    /// builds it.
    #[cold]
    #[inline(never)]
    fn write_truncation_marker(&self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) {
        let py = value.py();
        let qualname = value
            .get_type()
            .qualname()
            .ok()
            .and_then(|name| {
                // Safety: PyUnicode_Substring on a live str returns a new
                // reference to an exact str, or NULL with an exception set.
                let head = unsafe {
                    Bound::from_owned_ptr_or_err(
                        py,
                        ffi::PyUnicode_Substring(
                            name.as_ptr(),
                            0,
                            MAX_MARKER_TYPE_NAME_CHARS as ffi::Py_ssize_t,
                        ),
                    )
                }
                .ok()?;
                let encoded = head
                    .call_method1(
                        intern!(py, "encode"),
                        (intern!(py, "utf-8"), intern!(py, "backslashreplace")),
                    )
                    .ok()?;
                Some(encoded.cast_into::<PyBytes>().ok()?.as_bytes().to_vec())
            })
            .unwrap_or_else(|| b"object".to_vec());
        let budget = self.value_budget.unwrap_or(usize::MAX);
        let mut text = qualname;
        text.extend_from_slice(
            format!(" exceeded max_value_mb ({budget} bytes){TRUNCATION_MARKER_HINT}").as_bytes(),
        );
        write_ext(buf, TRUNCATED_VALUE_EXTENSION_TYPE, &text)
            .expect("a marker is far below the msgpack ext limit");
    }

    #[cold]
    #[inline(never)]
    fn over_budget(&mut self) -> Packed {
        self.error = Some(EncodeError::OverBudget);
        Err(Fail)
    }

    /// Fail once the current root has written more than its budget. Only
    /// ever fails when the finished root would be larger than the budget too.
    #[cfg_attr(debug_assertions, inline(never))]
    #[cfg_attr(not(debug_assertions), inline(always))]
    fn check_budget(&mut self, buf: &[u8], additional: usize) -> Packed {
        if buf
            .len()
            .saturating_add(additional)
            .saturating_sub(self.reserved_header_bytes)
            > self.budget_end
        {
            return self.over_budget();
        }
        Ok(())
    }

    /// Called on entering an exact list or dict outside tuple/set payloads
    /// and hook-made dicts. Counts it towards starting identity tracking, or
    /// once tracking, writes a back-reference if the same object was already
    /// packed in this root, returning whether it did.
    ///
    /// Only counters are touched inline: this sits on the container
    /// recursion path, whose stack use bounds the nesting a small (Windows
    /// main thread) stack can encode.
    #[cfg_attr(debug_assertions, inline(never))]
    #[cfg_attr(not(debug_assertions), inline(always))]
    fn enter_shared(&mut self, object: *mut ffi::PyObject, buf: &mut Vec<u8>) -> bool {
        if self.shared.is_none() {
            self.shared_entered += 1;
            if self.shared_entered >= SHARED_TRACKING_THRESHOLD {
                self.start_shared_tracking();
            }
            return false;
        }
        self.write_shared_reference(object, buf)
    }

    #[cold]
    #[inline(never)]
    fn start_shared_tracking(&mut self) {
        self.shared = Some(Box::default());
    }

    #[inline(never)]
    fn write_shared_reference(&mut self, object: *mut ffi::PyObject, buf: &mut Vec<u8>) -> bool {
        let Some(shared) = self.shared.as_deref() else {
            return false;
        };
        let Some(number) = shared.numbers.get(&(object as usize)) else {
            return false;
        };
        let Ok(distance) = u32::try_from(shared.completed - 1 - number) else {
            return false;
        };
        rmp::encode::write_ext_meta(buf, 4, SHARED_REFERENCE_EXTENSION_TYPE)
            .expect("Writing to memory, not I/O");
        buf.extend_from_slice(&distance.to_be_bytes());
        true
    }

    /// Called after packing any exact list or dict. Readers number every
    /// array and map of the root's own stream (not those inside tuple/set
    /// payloads) in completion order, so every one counts; only containers
    /// `enter_shared` saw, of at least two items when done, are remembered.
    #[cfg_attr(debug_assertions, inline(never))]
    #[cfg_attr(not(debug_assertions), inline(always))]
    fn complete_container(&mut self, object: *mut ffi::PyObject, len: usize) {
        if self.extension_depth == 0 && self.shared.is_some() {
            let remember = self.hook_depth == 0 && len >= 2;
            self.record_completed_container(object, remember);
        }
    }

    /// `complete_container` for the careful pass, where a container whose
    /// encoding holds a cycle marker (`context_free` false) is counted but
    /// never shared: packed again elsewhere it would mark other containers.
    #[cold]
    #[inline(never)]
    fn complete_careful_container(
        &mut self,
        object: *mut ffi::PyObject,
        len: usize,
        context_free: bool,
    ) {
        if self.extension_depth == 0 && self.shared.is_some() {
            let remember = context_free && self.hook_depth == 0 && len >= 2;
            self.record_completed_container(object, remember);
        }
    }

    #[inline(never)]
    fn record_completed_container(&mut self, object: *mut ffi::PyObject, remember: bool) {
        let Some(shared) = self.shared.as_deref_mut() else {
            return;
        };
        let number = shared.completed;
        shared.completed += 1;
        if remember && shared.numbers.len() < MAX_SHARED_CONTAINERS {
            // Safety: `object` was just packed, so it is alive; the new
            // reference is released by `release_shared`.
            unsafe { ffi::Py_INCREF(object) };
            shared.pins.push(object);
            shared.numbers.insert(object as usize, number);
        }
    }

    /// Forget the current root's shared containers.
    fn release_shared(&mut self) {
        self.shared_entered = 0;
        if let Some(shared) = self.shared.take() {
            for object in shared.pins {
                // Safety: each pin is a strong reference taken by
                // `complete_container`.
                unsafe { ffi::Py_DECREF(object) };
            }
        }
    }

    /// Whether the first pass failed in a way the careful pass records
    /// instead; if so, forgets the failure.
    #[cold]
    #[inline(never)]
    fn retry_carefully(&mut self, value: &Bound<'_, PyAny>) -> bool {
        let py = value.py();
        let retry = match &self.error {
            Some(EncodeError::Python(error)) => !self.careful && needs_careful(py, error),
            _ => false,
        };
        if retry {
            self.error = None;
        }
        retry
    }

    /// Whether the careful pass is already packing `value` further up.
    fn is_active(&self, value: &Bound<'_, PyAny>) -> bool {
        self.careful && self.active.contains(&(value.as_ptr() as usize))
    }

    fn fail<T>(&mut self, error: PyErr) -> Result<T, Fail> {
        self.error = Some(EncodeError::Python(error));
        Err(Fail)
    }

    fn check<T>(&mut self, result: PyResult<T>) -> Result<T, Fail> {
        match result {
            Ok(value) => Ok(value),
            Err(error) => self.fail(error),
        }
    }

    /// `dump_msgpack` sets `kolo.serialize.IN_KOLO_PROFILER` while it packs,
    /// which Kolo's QuerySet `__repr__` patch reads, and both serializers
    /// mark the encode for the query guard. Set them before the first call
    /// that can run user code; nothing can observe them earlier.
    fn set_profiler_flag(&mut self, py: Python) -> Packed {
        if self.profiler_flag_set {
            return Ok(());
        }
        if !self.lightweight_repr {
            let globals = self.serializer.globals.bind(py);
            let result = globals.set_item(intern!(py, "IN_KOLO_PROFILER"), true);
            self.check(result)?;
        }
        self.profiler_flag_set = true;
        NATIVE_ENCODES.with(|count| count.set(count.get() + 1));
        Ok(())
    }

    fn reset_profiler_flag(&mut self, py: Python) -> PyResult<()> {
        if !self.profiler_flag_set {
            return Ok(());
        }
        self.profiler_flag_set = false;
        NATIVE_ENCODES.with(|count| count.set(count.get() - 1));
        if self.lightweight_repr {
            return Ok(());
        }
        let globals = self.serializer.globals.bind(py);
        globals.set_item(intern!(py, "IN_KOLO_PROFILER"), false)
    }

    /// `Packer._pack`.
    fn pack(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>, nest_limit: i32) -> Packed {
        if nest_limit < 0 {
            return self.fail(PyValueError::new_err(RECURSION_LIMIT_MESSAGE));
        }
        let nest_limit = nest_limit - 1;
        let object = value.as_ptr();
        // Safety: these compare a live object's type against static types.
        unsafe {
            if object == ffi::Py_None() {
                rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
                return Ok(());
            }
            if object == ffi::Py_True() {
                rmp::encode::write_bool(buf, true).expect("Writing to memory, not I/O");
                return Ok(());
            }
            if object == ffi::Py_False() {
                rmp::encode::write_bool(buf, false).expect("Writing to memory, not I/O");
                return Ok(());
            }
            let object_type = ffi::Py_TYPE(object);
            if object_type == ptr::addr_of_mut!(ffi::PyLong_Type) {
                if let Ok(value) = value.extract::<i64>() {
                    rmp::encode::write_sint(buf, value).expect("Writing to memory, not I/O");
                    return Ok(());
                }
                if let Ok(value) = value.extract::<u64>() {
                    rmp::encode::write_uint(buf, value).expect("Writing to memory, not I/O");
                    return Ok(());
                }
                return self.write_unsupported_leaf(value, buf, nest_limit);
            }
            if object_type == ptr::addr_of_mut!(ffi::PyFloat_Type) {
                rmp::encode::write_f64(buf, ffi::PyFloat_AS_DOUBLE(object))
                    .expect("Writing to memory, not I/O");
                return Ok(());
            }
            if object_type == ptr::addr_of_mut!(ffi::PyUnicode_Type) {
                return self.pack_str(value.cast_unchecked::<PyString>(), buf);
            }
            if object_type == ptr::addr_of_mut!(ffi::PyBytes_Type) {
                return self.pack_bytes(value.cast_unchecked::<PyBytes>(), buf);
            }
            if object_type == ptr::addr_of_mut!(ffi::PyDict_Type) {
                return self.pack_dict(value.cast_unchecked::<PyDict>(), buf, nest_limit);
            }
            if object_type == ptr::addr_of_mut!(ffi::PyList_Type) {
                return self.pack_list(value.cast_unchecked::<PyList>(), buf, nest_limit);
            }
        }
        self.pack_uncommon(value, buf, nest_limit)
    }

    fn pack_str(&mut self, py_string: &Bound<'_, PyString>, buf: &mut Vec<u8>) -> Packed {
        let value = match py_string.to_str() {
            Ok(value) => value,
            Err(error) => return self.pack_unencodable_str(py_string, error, buf),
        };
        if u32::try_from(value.len()).is_err() {
            return self.fail(PyValueError::new_err("unicode string is too large"));
        }
        if self.value_interning.is_some()
            && !self
                .value_interning
                .is_some_and(|context| context.interning.disabled.load(Ordering::Relaxed))
            && (MIN_INTERNED_VALUE_BYTES..=MAX_INTERNED_VALUE_BYTES).contains(&value.len())
        {
            let identity = py_string.as_ptr() as usize;
            match self.lookup_value(identity, InternedValueKind::String, value.as_bytes(), buf) {
                ValueLookup::ReferenceWritten => return Ok(()),
                ValueLookup::WriteInline => {}
                ValueLookup::CacheCurrent => {
                    self.check_budget(buf, value.len())?;
                    let mut encoded = Vec::with_capacity(value.len() + 5);
                    rmp::encode::write_str(&mut encoded, value)
                        .expect("Writing to memory, not I/O");
                    self.cache_current_value(
                        identity,
                        InternedValueKind::String,
                        value.len(),
                        py_string.clone().into_any().unbind(),
                        encoded,
                        buf,
                    );
                    return Ok(());
                }
                ValueLookup::WriterCircuit(error) => {
                    self.error = Some(EncodeError::WriterCircuit(error));
                    return Err(Fail);
                }
            }
        }
        self.check_budget(buf, value.len())?;
        rmp::encode::write_str(buf, value).expect("Writing to memory, not I/O");
        Ok(())
    }

    /// An exact str with no UTF-8 form: the careful pass writes a str with
    /// lone surrogates losslessly, as `_pack_careful` does.
    #[cold]
    #[inline(never)]
    fn pack_unencodable_str(
        &mut self,
        py_string: &Bound<'_, PyString>,
        error: PyErr,
        buf: &mut Vec<u8>,
    ) -> Packed {
        let py = py_string.py();
        if !self.careful || !error.is_instance_of::<PyUnicodeEncodeError>(py) {
            return self.fail(error);
        }
        let chars = self.check(py_string.len())?;
        self.check_budget(buf, chars)?;
        let payload = py_string
            .call_method1(
                intern!(py, "encode"),
                (intern!(py, "utf-8"), intern!(py, "surrogatepass")),
            )
            .and_then(bytes_payload);
        let payload = self.check(payload)?;
        self.check_budget(buf, payload.as_bytes().len())?;
        let written = write_ext(buf, SURROGATE_STR_EXTENSION_TYPE, payload.as_bytes());
        self.check(written)
    }

    fn pack_bytes(&mut self, value: &Bound<'_, PyBytes>, buf: &mut Vec<u8>) -> Packed {
        if u32::try_from(value.as_bytes().len()).is_err() {
            return self.fail(PyValueError::new_err("bytes object is too large"));
        }
        if self.value_interning.is_some()
            && !self
                .value_interning
                .is_some_and(|context| context.interning.disabled.load(Ordering::Relaxed))
            && (MIN_INTERNED_VALUE_BYTES..=MAX_INTERNED_VALUE_BYTES)
                .contains(&value.as_bytes().len())
        {
            let identity = value.as_ptr() as usize;
            match self.lookup_value(identity, InternedValueKind::Bytes, value.as_bytes(), buf) {
                ValueLookup::ReferenceWritten => return Ok(()),
                ValueLookup::WriteInline => {}
                ValueLookup::CacheCurrent => {
                    self.check_budget(buf, value.as_bytes().len())?;
                    let mut encoded = Vec::with_capacity(value.as_bytes().len() + 5);
                    rmp::encode::write_bin(&mut encoded, value.as_bytes())
                        .expect("Writing to memory, not I/O");
                    self.cache_current_value(
                        identity,
                        InternedValueKind::Bytes,
                        value.as_bytes().len(),
                        value.clone().into_any().unbind(),
                        encoded,
                        buf,
                    );
                    return Ok(());
                }
                ValueLookup::WriterCircuit(error) => {
                    self.error = Some(EncodeError::WriterCircuit(error));
                    return Err(Fail);
                }
            }
        }
        self.check_budget(buf, value.as_bytes().len())?;
        rmp::encode::write_bin(buf, value.as_bytes()).expect("Writing to memory, not I/O");
        Ok(())
    }

    /// Run one level of container recursion behind CPython's own C-stack
    /// guard (on Python 3.14+ a real stack-headroom check), so deep values
    /// end in RecursionError instead of overflowing a small thread stack.
    /// Before 3.12 that guard counts Python frames instead, and would reject
    /// nesting msgpack's packer accepts, so it is only used from 3.12.
    /// WebAssembly stacks are much smaller than msgpack's nesting limit
    /// assumes, so they also get a fixed native depth cap.
    fn nested(&mut self, py: Python, pack: impl FnOnce(&mut Self) -> Packed) -> Packed {
        #[cfg(target_family = "wasm")]
        if self.native_depth >= WASM_MAX_NATIVE_DEPTH {
            return self.fail(PyRecursionError::new_err(
                "maximum recursion depth exceeded while serializing a Kolo value",
            ));
        }
        #[cfg(Py_3_12)]
        // Safety: paired with Py_LeaveRecursiveCall below.
        if unsafe { ffi::Py_EnterRecursiveCall(c" while serializing a Kolo value".as_ptr()) } != 0 {
            return self.fail(PyErr::fetch(py));
        }
        #[cfg(not(Py_3_12))]
        let _ = py;
        self.native_depth += 1;
        let packed = pack(self);
        self.native_depth -= 1;
        #[cfg(Py_3_12)]
        // Safety: paired with the successful Py_EnterRecursiveCall above.
        unsafe {
            ffi::Py_LeaveRecursiveCall()
        };
        packed
    }

    // Inlined into `pack` in release builds; out of line in debug builds to keep recursion frames small.
    #[cfg_attr(not(debug_assertions), inline(always))]
    fn pack_dict(
        &mut self,
        dict: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        if self.hook_depth == 0
            && self.extension_depth == 0
            && self.enter_shared(dict.as_ptr(), buf)
        {
            return Ok(());
        }
        self.check_budget(buf, 2 * dict.len())?;
        if self.careful {
            return self.pack_dict_carefully(dict, buf, nest_limit);
        }
        self.nested(dict.py(), |encoder| {
            encoder.pack_dict_items(dict, buf, nest_limit)
        })?;
        self.complete_container(dict.as_ptr(), dict.len());
        Ok(())
    }

    /// The careful pass's exact dict. Out of line, like the other careful
    /// paths, so the first pass's recursive frames stay as small.
    #[cold]
    #[inline(never)]
    fn pack_dict_carefully(
        &mut self,
        dict: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        if !self.enter_container(dict.as_any(), DICT_CYCLE_MARKER, buf)? {
            return Ok(());
        }
        let markers = self.cycle_markers;
        let packed = self.nested(dict.py(), |encoder| {
            encoder.pack_dict_items(dict, buf, nest_limit)
        });
        self.active.pop();
        packed?;
        let context_free = self.cycle_markers == markers;
        self.complete_careful_container(dict.as_ptr(), dict.len(), context_free);
        Ok(())
    }

    /// The careful pass's exact list.
    #[cold]
    #[inline(never)]
    fn pack_list_carefully(
        &mut self,
        list: &Bound<'_, PyList>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        if !self.enter_container(list.as_any(), LIST_CYCLE_MARKER, buf)? {
            return Ok(());
        }
        let markers = self.cycle_markers;
        let packed = self.nested(list.py(), |encoder| {
            encoder.pack_list_items(list, buf, nest_limit)
        });
        self.active.pop();
        packed?;
        let context_free = self.cycle_markers == markers;
        self.complete_careful_container(list.as_ptr(), list.len(), context_free);
        Ok(())
    }

    /// Marks `container` as being packed, or, if it already is further up,
    /// writes `cycle_marker` instead and returns false.
    fn enter_container(
        &mut self,
        container: &Bound<'_, PyAny>,
        cycle_marker: &'static [u8],
        buf: &mut Vec<u8>,
    ) -> Result<bool, Fail> {
        let identity = container.as_ptr() as usize;
        if self.active.contains(&identity) {
            self.cycle_markers += 1;
            let written = write_ext(buf, REPR_EXTENSION_TYPE, cycle_marker);
            self.check(written)?;
            return Ok(false);
        }
        self.active.push(identity);
        Ok(true)
    }

    fn pack_dict_items(
        &mut self,
        dict: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        #[cfg(not(Py_GIL_DISABLED))]
        match self.pack_inert_dict_prefix(dict, buf, nest_limit)? {
            None => Ok(()),
            Some((position, pending_value)) => {
                self.pack_dict_snapshot(dict, position, pending_value, buf, nest_limit)
            }
        }
        #[cfg(Py_GIL_DISABLED)]
        {
            // Another thread may resize the dict at any time: take the
            // snapshot first and size the header from it.
            let base = self.snapshot.len();
            let len = snapshot_dict_items(dict, 0, &mut self.snapshot);
            let packed = match checked_msgpack_len(len) {
                Some(map_len) => {
                    rmp::encode::write_map_len(buf, map_len).expect("Writing to memory, not I/O");
                    self.pack_snapshot(dict.py(), base, 2 * len, buf, nest_limit)
                }
                None => self.fail(PyValueError::new_err("dict is too large")),
            };
            self.release_snapshot(base);
            packed
        }
    }

    /// Write the map header and pack leading entries directly while packing
    /// them cannot run Python code, so the dict cannot change. Returns where
    /// the snapshot must take over (the `PyDict_Next` position, and the
    /// entry's value if its key is already packed), or `None` when done.
    /// Kept out of line so its frame is not on the recursion path.
    #[cfg(not(Py_GIL_DISABLED))]
    #[inline(never)]
    fn pack_inert_dict_prefix(
        &mut self,
        dict: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Result<Option<(ffi::Py_ssize_t, Option<*mut ffi::PyObject>)>, Fail> {
        let Some(map_len) = checked_msgpack_len(dict.len()) else {
            return self.fail(PyValueError::new_err("dict is too large"));
        };
        rmp::encode::write_map_len(buf, map_len).expect("Writing to memory, not I/O");
        let py = dict.py();
        let mut position = 0;
        let mut key = ptr::null_mut();
        let mut value = ptr::null_mut();
        let mut entries = 0usize;
        loop {
            let entry_position = position;
            // Safety: `dict` is a live dict. No Python code has run since its
            // size was read, so the borrowed entries are still owned by it
            // while they are packed.
            unsafe {
                if ffi::PyDict_Next(dict.as_ptr(), &mut position, &mut key, &mut value) == 0 {
                    return Ok(None);
                }
                match self.try_pack_inert(py, key, buf, nest_limit) {
                    Some(packed) => packed?,
                    None => return Ok(Some((entry_position, None))),
                }
                match self.try_pack_inert(py, value, buf, nest_limit) {
                    Some(packed) => packed?,
                    None => return Ok(Some((position, Some(value)))),
                }
            }
            entries += 1;
            if entries & BUDGET_CHECK_MASK == 0 {
                self.check_budget(buf, 0)?;
            }
        }
    }

    /// Snapshot a dict's entries from `position` on and pack them, after
    /// `pending_value` when the current entry's key is already packed. The
    /// map header is already written.
    #[cfg(not(Py_GIL_DISABLED))]
    fn pack_dict_snapshot(
        &mut self,
        dict: &Bound<'_, PyDict>,
        position: ffi::Py_ssize_t,
        pending_value: Option<*mut ffi::PyObject>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let base = self.snapshot.len();
        if let Some(value) = pending_value {
            // Safety: borrowed from `dict`, and no Python code has run since.
            unsafe { ffi::Py_INCREF(value) };
            self.snapshot.push(value);
        }
        let len = snapshot_dict_items(dict, position, &mut self.snapshot);
        let items = 2 * len + usize::from(pending_value.is_some());
        let packed = self.pack_snapshot(dict.py(), base, items, buf, nest_limit);
        self.release_snapshot(base);
        packed
    }

    /// `pack(object)` for the leaves it writes without running any Python
    /// code: `None`, bools, exact floats, str, bytes and ints within 64 bits.
    /// Returns `None`, having written nothing, for anything else (including
    /// larger ints, which go through the `default` hook). A container's items
    /// are packed through this while nothing can have resized it.
    ///
    /// Safety: `object` must be a live object.
    #[cfg(not(Py_GIL_DISABLED))]
    #[inline(always)]
    unsafe fn try_pack_inert(
        &mut self,
        py: Python,
        object: *mut ffi::PyObject,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Option<Packed> {
        if nest_limit < 0 {
            return None;
        }
        if object == ffi::Py_None() {
            rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
            return Some(Ok(()));
        }
        if object == ffi::Py_True() || object == ffi::Py_False() {
            rmp::encode::write_bool(buf, object == ffi::Py_True())
                .expect("Writing to memory, not I/O");
            return Some(Ok(()));
        }
        let object_type = ffi::Py_TYPE(object);
        if object_type == ptr::addr_of_mut!(ffi::PyLong_Type) {
            let mut overflow = 0;
            let value = ffi::PyLong_AsLongLongAndOverflow(object, &mut overflow);
            if overflow != 0 {
                return None;
            }
            rmp::encode::write_sint(buf, value).expect("Writing to memory, not I/O");
            return Some(Ok(()));
        }
        if object_type == ptr::addr_of_mut!(ffi::PyFloat_Type) {
            rmp::encode::write_f64(buf, ffi::PyFloat_AS_DOUBLE(object))
                .expect("Writing to memory, not I/O");
            return Some(Ok(()));
        }
        if object_type == ptr::addr_of_mut!(ffi::PyUnicode_Type) {
            let value = Borrowed::from_ptr(py, object).cast_unchecked::<PyString>();
            return Some(self.pack_str(&value, buf));
        }
        if object_type == ptr::addr_of_mut!(ffi::PyBytes_Type) {
            let value = Borrowed::from_ptr(py, object).cast_unchecked::<PyBytes>();
            return Some(self.pack_bytes(&value, buf));
        }
        None
    }

    /// Drop the snapshot references above `base`. A decref can run a
    /// finalizer, which never sees this encoder.
    fn release_snapshot(&mut self, base: usize) {
        // Release in push order, as dropping a Vec's tail would, since
        // finalizers can observe the order.
        let end = self.snapshot.len();
        for index in base..end {
            let object = self.snapshot.get(index);
            // Safety: each entry is a strong reference pushed by a snapshot.
            unsafe { ffi::Py_DECREF(object) };
        }
        self.snapshot.truncate(base);
    }

    /// Pack the `len` snapshotted items at `self.snapshot[base..]`. The
    /// caller truncates the snapshot back to `base` afterwards, on success
    /// or failure.
    fn pack_snapshot(
        &mut self,
        py: Python,
        base: usize,
        len: usize,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        for index in base..base + len {
            // Safety: `self.snapshot.get(index)` owns a reference to the item
            // until the caller releases back to `base`, after this loop.
            // Nested containers only push and release above `base + len`;
            // a reallocation moves the reference, not the object.
            let item = unsafe { Borrowed::from_ptr(py, self.snapshot.get(index)) };
            self.pack(&item, buf, nest_limit)?;
            if index & BUDGET_CHECK_MASK == BUDGET_CHECK_MASK {
                self.check_budget(buf, 0)?;
            }
        }
        Ok(())
    }

    #[cfg_attr(not(debug_assertions), inline(always))]
    fn pack_list(
        &mut self,
        list: &Bound<'_, PyList>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        if self.hook_depth == 0
            && self.extension_depth == 0
            && self.enter_shared(list.as_ptr(), buf)
        {
            return Ok(());
        }
        self.check_budget(buf, list.len())?;
        if self.careful {
            return self.pack_list_carefully(list, buf, nest_limit);
        }
        self.nested(list.py(), |encoder| {
            encoder.pack_list_items(list, buf, nest_limit)
        })?;
        self.complete_container(list.as_ptr(), list.len());
        Ok(())
    }

    fn pack_list_items(
        &mut self,
        list: &Bound<'_, PyList>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        #[cfg(not(Py_GIL_DISABLED))]
        match self.pack_inert_list_prefix(list, buf, nest_limit)? {
            None => Ok(()),
            Some(index) => {
                let base = self.snapshot.len();
                let copied = snapshot_list_items(list, index, &mut self.snapshot);
                let packed = self.pack_snapshot(list.py(), base, copied, buf, nest_limit);
                self.release_snapshot(base);
                packed
            }
        }
        #[cfg(Py_GIL_DISABLED)]
        {
            let base = self.snapshot.len();
            let len = snapshot_list_items(list, 0, &mut self.snapshot);
            let packed = match checked_msgpack_len(len) {
                Some(array_len) => {
                    rmp::encode::write_array_len(buf, array_len)
                        .expect("Writing to memory, not I/O");
                    self.pack_snapshot(list.py(), base, len, buf, nest_limit)
                }
                None => self.fail(PyValueError::new_err("list is too large")),
            };
            self.release_snapshot(base);
            packed
        }
    }

    /// As `pack_inert_dict_prefix`, for a list: returns the index of the
    /// first item that could run Python code, or `None` when done.
    #[cfg(not(Py_GIL_DISABLED))]
    #[inline(never)]
    fn pack_inert_list_prefix(
        &mut self,
        list: &Bound<'_, PyList>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Result<Option<usize>, Fail> {
        let len = list.len();
        let Some(array_len) = checked_msgpack_len(len) else {
            return self.fail(PyValueError::new_err("list is too large"));
        };
        rmp::encode::write_array_len(buf, array_len).expect("Writing to memory, not I/O");
        let py = list.py();
        for index in 0..len {
            // Safety: no Python code has run since `len` was read, so the
            // list still owns `len` items while they are packed.
            unsafe {
                let item = ffi::PyList_GET_ITEM(list.as_ptr(), index as ffi::Py_ssize_t);
                match self.try_pack_inert(py, item, buf, nest_limit) {
                    Some(packed) => packed?,
                    None => return Ok(Some(index)),
                }
            }
            if index & BUDGET_CHECK_MASK == BUDGET_CHECK_MASK {
                self.check_budget(buf, 0)?;
            }
        }
        Ok(None)
    }

    /// The rest of `Packer._pack_inner` after the hot exact types: leaves
    /// msgpack packs without `default`, then `default` itself.
    #[cold]
    #[inline(never)]
    fn pack_uncommon(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let object = value.as_ptr();
        // Safety: type checks and bytearray accessors on a live object.
        unsafe {
            if ffi::PyTuple_CheckExact(object) != 0 {
                return self.write_unsupported_leaf(value, buf, nest_limit);
            }
            if ffi::PyByteArray_CheckExact(object) != 0 {
                return self.pack_bytearray(value, buf);
            }
            let object_type = ffi::Py_TYPE(object) as *mut ffi::PyObject;
            if object_type == self.serializer.ext_type.as_ptr()
                || object_type == self.serializer.timestamp_type.as_ptr()
                || ffi::PyMemoryView_Check(object) != 0
            {
                return self.pack_with_msgpack(value, buf);
            }
        }
        self.write_unsupported_leaf(value, buf, nest_limit)
    }

    /// An exact bytearray. Kept out of line, like `pack_with_msgpack`, so
    /// `pack_uncommon`'s frame on the tuple recursion path stays small.
    #[inline(never)]
    fn pack_bytearray(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) -> Packed {
        let object = value.as_ptr();
        // Another thread may resize the bytearray on free-threaded builds;
        // hold its lock across the size read, the budget check and the copy.
        let room = self
            .budget_end
            .saturating_add(self.reserved_header_bytes)
            .saturating_sub(buf.len());
        // Safety: bytearray accessors on a live exact bytearray.
        let copied = pyo3::sync::with_critical_section(value, || unsafe {
            let len = ffi::PyByteArray_Size(object) as usize;
            if len > room {
                return Some(false);
            }
            let bin_len = checked_msgpack_len(len)?;
            rmp::encode::write_bin_len(buf, bin_len).expect("Writing to memory, not I/O");
            let data = ffi::PyByteArray_AsString(object) as *const u8;
            buf.extend_from_slice(std::slice::from_raw_parts(data, len));
            Some(true)
        });
        match copied {
            Some(true) => Ok(()),
            Some(false) => self.over_budget(),
            None => self.fail(PyValueError::new_err("bytearray object is too large")),
        }
    }

    /// ExtType, Timestamp and memoryview, which msgpack's own packer packs
    /// exactly. Only a bytes subclass's `__len__` in an ExtType can run user
    /// code there.
    #[inline(never)]
    fn pack_with_msgpack(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) -> Packed {
        let py = value.py();
        let object = value.as_ptr();
        // Refuse an oversized payload before msgpack copies it. Both reads
        // run no user code; a failing one is left to msgpack.
        // Safety: type checks and tuple/bytes accessors on a live object.
        let payload_len = unsafe {
            if ffi::Py_TYPE(object) as *mut ffi::PyObject == self.serializer.ext_type.as_ptr() {
                let data = ffi::PyTuple_GET_ITEM(object, 1);
                // A bytes subclass's `__len__` decides what msgpack packs,
                // so only exact bytes are measured here.
                (ffi::PyBytes_CheckExact(data) != 0).then(|| ffi::PyBytes_Size(data) as usize)
            } else if ffi::PyMemoryView_Check(object) != 0 {
                value
                    .getattr(intern!(py, "nbytes"))
                    .and_then(|nbytes| nbytes.extract::<usize>())
                    .ok()
            } else {
                None
            }
        };
        self.check_budget(buf, payload_len.unwrap_or(0))?;
        self.set_profiler_flag(py)?;
        let kwargs = PyDict::new(py);
        let packed = kwargs
            .set_item(intern!(py, "strict_types"), true)
            .and_then(|()| self.serializer.packb.bind(py).call((value,), Some(&kwargs)))
            .and_then(|packed| packed.cast_into::<PyBytes>().map_err(Into::into));
        let packed = match packed {
            // Safety: a type check on a live object.
            Err(error)
                if self.careful
                    && unsafe { ffi::PyMemoryView_Check(object) } != 0
                    && exact_value_error_is(py, &error, RELEASED_MEMORYVIEW_MESSAGE) =>
            {
                return self.pack_released_memoryview(value, buf);
            }
            packed => self.check(packed)?,
        };
        self.check_budget(buf, packed.as_bytes().len())?;
        buf.extend_from_slice(packed.as_bytes());
        Ok(())
    }

    /// The careful pass records a released memoryview as its repr, as
    /// `_pack_careful` does.
    #[cold]
    #[inline(never)]
    fn pack_released_memoryview(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) -> Packed {
        let written = match self.repr(value, true) {
            Ok(ReprText::Py(text)) => utf8_payload(text).and_then(|payload| {
                payload
                    .packed_len()
                    .and_then(|len| write_ext(buf, REPR_EXTENSION_TYPE, &payload.as_bytes()[..len]))
            }),
            Ok(ReprText::Native(text)) => {
                write_ext(buf, REPR_EXTENSION_TYPE, &self.repr_memo.arena[text])
            }
            Err(error) => Err(error),
        };
        self.check(written)
    }

    /// Every value msgpack hands to `default`: `o = default(o)` followed by
    /// packing the result without `default`, or the hook's error handler.
    /// The single entry point for unsupported leaves (and exact tuples).
    #[cold]
    #[inline(never)]
    fn write_unsupported_leaf(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let start = buf.len();
        let defaulted = match self.call_default(value, buf) {
            Ok(defaulted) => defaulted,
            Err(Fail) => {
                // Abandoned reservation accounting is lenient; encode_value performs the exact final check.
                buf.truncate(start);
                return self.handle_default_error(value, buf);
            }
        };
        self.write_defaulted(value, defaulted, buf, nest_limit)
    }

    /// Write what the default hook produced. Out of line, so the frame that
    /// is live across `call_default` (the tuple recursion path) stays small
    /// in unoptimized builds.
    #[cfg_attr(debug_assertions, inline(never))]
    fn write_defaulted(
        &mut self,
        value: &Bound<'_, PyAny>,
        defaulted: Defaulted<'_>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let packed = match defaulted {
            Defaulted::Ext(code, payload) => {
                let len = self.check(payload.packed_len())?;
                self.check_budget(buf, len)?;
                write_ext(buf, code, &payload.as_bytes()[..len])
            }
            Defaulted::NativeExt(code, text) => {
                self.check_budget(buf, text.len())?;
                write_ext(buf, code, &self.repr_memo.arena[text])
            }
            Defaulted::Sequence(code, start) => {
                self.reserved_header_bytes = self
                    .reserved_header_bytes
                    .saturating_sub(MAX_EXT_HEADER_LEN);
                finish_reserved_extension(buf, start, code)
            }
            Defaulted::Dict(dict)
                if self.careful
                    || nest_limit
                        <= self.serializer.recurse_limit - FIRST_PASS_CYCLE_CHECK_DEPTH =>
            {
                self.hook_depth += 1;
                let packed = self.pack_dict_copy_tracked(value, &dict, buf, nest_limit);
                self.hook_depth -= 1;
                return packed;
            }
            Defaulted::Dict(dict) => {
                self.hook_depth += 1;
                let packed = self.pack_dict(&dict, buf, nest_limit);
                self.hook_depth -= 1;
                return packed;
            }
            Defaulted::CycleMarker(marker) => {
                self.cycle_markers += 1;
                self.check_budget(buf, marker.len())?;
                write_ext(buf, REPR_EXTENSION_TYPE, marker)
            }
            Defaulted::OverBudget => return self.over_budget(),
        };
        self.check(packed)?;
        self.check_budget(buf, 0)
    }

    /// The `dict(obj)` copy of a dict subclass, which stands for `value` (what
    /// a cycle comes back to), in the careful pass or nested deep enough for
    /// the first pass to look for a cycle. There, `value` already being packed
    /// further up is a cycle, which msgpack follows until its nesting limit:
    /// fail the same way at once, for the careful pass to record.
    #[cold]
    #[inline(never)]
    fn pack_dict_copy_tracked(
        &mut self,
        value: &Bound<'_, PyAny>,
        copy: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let identity = value.as_ptr() as usize;
        if !self.careful && self.active.contains(&identity) {
            return self.fail(PyValueError::new_err(RECURSION_LIMIT_MESSAGE));
        }
        self.active.push(identity);
        let packed = self.pack_dict(copy, buf, nest_limit);
        self.active.pop();
        packed
    }

    /// `msgpack_encode_hook`'s `except DatabaseAccessBlocked:` and
    /// `except Exception:` handlers, or the lightweight hook's
    /// `except DatabaseAccessBlocked:`.
    #[cold]
    #[inline(never)]
    fn handle_default_error(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) -> Packed {
        let py = value.py();
        if !matches!(self.error, Some(EncodeError::Python(_))) {
            return Err(Fail);
        }
        let Some(EncodeError::Python(error)) = self.error.take() else {
            unreachable!("checked above");
        };
        // Python evaluates the first handler's target for any exception.
        let blocked = match self.global(intern!(py, "DatabaseAccessBlocked")) {
            Ok(class) => error.is_instance(py, &class),
            Err(lookup_error) => {
                // Safety: SetContext steals the reference to `error`.
                unsafe {
                    ffi::PyException_SetContext(
                        lookup_error.value(py).as_ptr(),
                        error.into_value(py).into_ptr(),
                    );
                }
                return self.fail(lookup_error);
            }
        };
        let caught = blocked
            || (!self.lightweight_repr
                && error.is_instance_of::<PyException>(py)
                && (self.careful || !needs_careful(py, &error)));
        if !caught {
            self.error = Some(EncodeError::Python(error));
            return Err(Fail);
        }
        // Run the handler with `error` as the handled exception, as inside
        // Python's `except` block: user code sees it via `sys.exception()`,
        // and CPython chains it into anything raised there.
        let (mut saved_type, mut saved_value, mut saved_traceback) =
            (ptr::null_mut(), ptr::null_mut(), ptr::null_mut());
        // Safety: GetExcInfo returns new references that SetExcInfo steals
        // back below; the handled value is a new reference SetExcInfo steals.
        unsafe {
            ffi::PyErr_GetExcInfo(&mut saved_type, &mut saved_value, &mut saved_traceback);
            let handled = error.value(py);
            ffi::PyErr_SetExcInfo(
                handled.get_type().into_ptr(),
                handled.clone().into_ptr(),
                error
                    .traceback(py)
                    .map_or(ptr::null_mut(), |traceback| traceback.into_ptr()),
            );
        }
        let payload = (|| -> PyResult<(i8, Payload<'_>)> {
            if blocked {
                let text = self
                    .global(intern!(py, "_query_free_repr"))?
                    .call1((value,))?;
                return Ok((0, utf8_payload(text)?));
            }
            let module = format_field(&value.getattr(intern!(py, "__module__"))?)?;
            let qualname = format_field(&value.get_type().getattr(intern!(py, "__qualname__"))?)?;
            let path = concat_text(&[&module, &PyString::new(py, "."), &qualname])?;
            Ok((
                SERIALIZATION_ERROR_EXTENSION_TYPE,
                escaped_utf8_payload(path)?,
            ))
        })();
        // Safety: restores the references taken above.
        unsafe { ffi::PyErr_SetExcInfo(saved_type, saved_value, saved_traceback) };
        match payload {
            Ok((code, payload)) => {
                let len = self.check(payload.packed_len())?;
                self.check_budget(buf, len)?;
                let written = write_ext(buf, code, &payload.as_bytes()[..len]);
                self.check(written)
            }
            Err(new_error) => {
                let new_value = new_error.value(py).as_ptr();
                // Safety: GetContext returns a new reference (or NULL), and
                // SetContext steals the reference to `error`.
                unsafe {
                    let context = ffi::PyException_GetContext(new_value);
                    if context.is_null() {
                        if new_value != error.value(py).as_ptr() {
                            ffi::PyException_SetContext(new_value, error.into_value(py).into_ptr());
                        }
                    } else {
                        ffi::Py_DECREF(context);
                    }
                }
                self.fail(new_error)
            }
        }
    }

    /// The body of `msgpack_encode_hook` (inside its `try`), or of
    /// `msgpack_encode_hook_lightweight_repr`.
    fn call_default<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
        buf: &mut Vec<u8>,
    ) -> Result<Defaulted<'py>, Fail> {
        let py = value.py();
        if let Ok(tuple) = value.cast_exact::<PyTuple>() {
            if self.is_active(value) {
                return Ok(Defaulted::CycleMarker(TUPLE_CYCLE_MARKER));
            }
            let start = self.reserve_extension_header(buf);
            self.pack_extension_items(value, SequenceItems::Tuple(tuple), buf)?;
            return Ok(Defaulted::Sequence(PY_TUPLE_EXTENSION_TYPE, start));
        }
        self.used_default_hook = true;
        self.set_profiler_flag(py)?;

        // Fall through only when no handler matches and reading __class__ runs no code.
        #[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
        let falls_through = self
            .serializer
            .falls_through_ladder(value, self.lightweight_repr);
        #[cfg(not(all(Py_3_12, not(Py_GIL_DISABLED))))]
        let falls_through = false;

        if construction::worth_checking(
            value.as_ptr(),
            falls_through,
            self.lightweight_repr,
            self.serializer.method_type,
        ) && !matches!(&self.construction, Some(found) if found.is_empty())
        {
            if let Some(defaulted) = self.construction_default(value, falls_through)? {
                return Ok(defaulted);
            }
        }

        if falls_through {
            let payload = self.unmatched_leaf_payload(value);
            return self.check(payload);
        }

        let mut class_is_type = None;
        let (tuple_type, set_type, frozenset_type, dict_type) = (
            ptr::addr_of_mut!(ffi::PyTuple_Type).cast::<ffi::PyObject>(),
            ptr::addr_of_mut!(ffi::PySet_Type).cast::<ffi::PyObject>(),
            ptr::addr_of_mut!(ffi::PyFrozenSet_Type).cast::<ffi::PyObject>(),
            ptr::addr_of_mut!(ffi::PyDict_Type).cast::<ffi::PyObject>(),
        );
        for (sequence_type, code, cycle_marker) in [
            (tuple_type, PY_TUPLE_EXTENSION_TYPE, TUPLE_CYCLE_MARKER),
            (set_type, PY_SET_EXTENSION_TYPE, SET_CYCLE_MARKER),
            (
                frozenset_type,
                PY_FROZENSET_EXTENSION_TYPE,
                FROZENSET_CYCLE_MARKER,
            ),
        ] {
            let matched = self.isinstance(value, sequence_type, &mut class_is_type);
            if self.check(matched)? {
                if self.is_active(value) {
                    return Ok(Defaulted::CycleMarker(cycle_marker));
                }
                // Every item takes at least a byte: refuse an oversized exact
                // set before `list()` copies it (a subclass's `__len__` could
                // run user code, so only exact sets are measured).
                // Safety: a type check and a size read on a live object.
                unsafe {
                    if ffi::PyAnySet_CheckExact(value.as_ptr()) != 0 {
                        let len = ffi::PySet_Size(value.as_ptr()).max(0) as usize;
                        self.check_budget(buf, len)?;
                    }
                }
                let items = self.call_builtin(value, ptr::addr_of_mut!(ffi::PyList_Type).cast());
                let items = self.check(items)?;
                let items = items.cast_into::<PyList>().expect("list() returns a list");
                let start = self.reserve_extension_header(buf);
                self.pack_extension_items(value, SequenceItems::List(&items), buf)?;
                return Ok(Defaulted::Sequence(code, start));
            }
        }
        let matched = self.isinstance(value, dict_type, &mut class_is_type);
        if self.check(matched)? {
            if self.is_active(value) {
                return Ok(Defaulted::CycleMarker(DICT_CYCLE_MARKER));
            }
            let copy = self.call_builtin(value, dict_type);
            let copy = self.check(copy)?;
            return Ok(Defaulted::Dict(
                copy.cast_into::<PyDict>().expect("dict() returns a dict"),
            ));
        }
        let room = (self.budget_end != usize::MAX).then(|| {
            self.budget_end
                .saturating_add(self.reserved_header_bytes)
                .saturating_sub(buf.len())
        });
        let payload = self.default_leaf_payload(value, &mut class_is_type, room);
        self.check(payload)
    }

    /// What the hook returns for a value under construction, or None.
    #[inline(never)]
    fn construction_default<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
        falls_through: bool,
    ) -> Result<Option<Defaulted<'py>>, Fail> {
        let placeholder = self.construction_placeholder(value, falls_through);
        match self.check(placeholder)? {
            Some(text) => {
                let payload = escaped_utf8_payload(text);
                Ok(Some(Defaulted::Ext(0, self.check(payload)?)))
            }
            None => Ok(None),
        }
    }

    /// `kolo.serialize._under_construction_ext`: the text recorded for an
    /// object whose constructor is still running (or a method bound to
    /// one), whose `repr()` could change it. None for any other value.
    fn construction_placeholder<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
        falls_through: bool,
    ) -> PyResult<Option<Bound<'py, PyAny>>> {
        let object = value.as_ptr();
        // Safety: reads a live object's type; an exact bound method's
        // `__self__` is set at creation, never NULL and kept alive by it.
        let (is_method, subject) = unsafe {
            if ffi::Py_TYPE(object) as usize == self.serializer.method_type {
                (true, PyMethod_Self(object))
            } else {
                (false, object)
            }
        };
        if (is_method && self.lightweight_repr)
            || ((is_method || !falls_through || self.lightweight_repr)
                && !construction::may_run_user_code(
                    value.py(),
                    subject,
                    self.lightweight_repr,
                    self.serializer.object_class,
                ))
        {
            return Ok(None);
        }
        self.placeholder_if_under_construction(value, subject, is_method)
    }

    #[inline(never)]
    fn placeholder_if_under_construction<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
        subject: *mut ffi::PyObject,
        is_method: bool,
    ) -> PyResult<Option<Bound<'py, PyAny>>> {
        let py = value.py();
        if self.construction.is_none() {
            let found = construction::find(py, || {
                self.global(intern!(py, "_objects_under_construction"))
            })?;
            self.construction = Some(found);
        }
        let under_construction = self
            .construction
            .as_ref()
            .is_some_and(|found| found.contains(subject));
        if !under_construction {
            return Ok(None);
        }
        if is_method {
            let describe = self.global(intern!(py, "_method_under_construction_repr"))?;
            let text = describe.call1((value,))?;
            return Ok((!text.is_none()).then_some(text));
        }
        let lightweight_repr = self.lightweight_repr;
        construction::placeholder_text(value, lightweight_repr, || {
            self.global(intern!(py, "_under_construction_repr"))?
                .call1((value, false, lightweight_repr))
        })
    }

    /// The hook's remaining branches, each producing an ExtType.
    #[inline(never)]
    fn default_leaf_payload<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
        class_is_type: &mut Option<bool>,
        room: Option<usize>,
    ) -> PyResult<Defaulted<'py>> {
        let py = value.py();
        for (name, code) in [
            (intern!(py, "datetime"), 1),
            (intern!(py, "date"), 2),
            (intern!(py, "time"), 3),
        ] {
            let class = self.global(name)?;
            if self.isinstance(value, class.as_ptr(), class_is_type)? {
                let text = value.call_method0(intern!(py, "isoformat"))?;
                return Ok(Defaulted::Ext(code, utf8_payload(text)?));
            }
        }
        let int_type = ptr::addr_of_mut!(ffi::PyLong_Type).cast::<ffi::PyObject>();
        if self.isinstance(value, int_type, class_is_type)? {
            let bit_length = value.call_method0(intern!(py, "bit_length"))?;
            if let (Some(room), true) = (room, value.is_exact_instance_of::<PyInt>()) {
                if let Ok(bits) = bit_length.extract::<u64>() {
                    if !usize::try_from(bits / 8).is_ok_and(|bytes| bytes <= room) {
                        return Ok(Defaulted::OverBudget);
                    }
                }
            }
            let num_bytes = bit_length.add(7)?.floor_div(8)?.add(1)?;
            let kwargs = PyDict::new(py);
            kwargs.set_item(intern!(py, "signed"), true)?;
            let data = value.call_method(
                intern!(py, "to_bytes"),
                (num_bytes, intern!(py, "big")),
                Some(&kwargs),
            )?;
            return Ok(Defaulted::Ext(4, bytes_payload(data)?));
        }
        let decimal = self.global(intern!(py, "Decimal"))?;
        if self.isinstance(value, decimal.as_ptr(), class_is_type)? {
            return Ok(Defaulted::Ext(5, utf8_payload(value.str()?.into_any())?));
        }

        if self.lightweight_repr {
            return self.unmatched_leaf_payload(value);
        }

        // Truth-testing `_QuerySet_checked` or calling `_get_queryset_class`
        // (which may import Django) can run user code that changes the type.
        let queryset = self.queryset_class(py)?;
        *class_is_type = None;
        if !queryset.is_none()
            && self.isinstance(value, queryset.as_ptr(), class_is_type)?
            && value.getattr(intern!(py, "_result_cache"))?.is_none()
        {
            let model = value.getattr(intern!(py, "model"))?;
            let text = concat_text(&[
                &PyString::new(py, "Unevaluated queryset for: "),
                &format_field(&model)?,
            ])?;
            return Ok(Defaulted::Ext(0, utf8_payload(text)?));
        }
        self.unmatched_leaf_payload(value)
    }

    /// The hook's last branch, for a value no `isinstance` check matched (or
    /// an unevaluated-QuerySet check rejected): the lightweight
    /// `<qualname object id>` text, or `repr(value)`.
    fn unmatched_leaf_payload<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
    ) -> PyResult<Defaulted<'py>> {
        let py = value.py();
        if self.lightweight_repr {
            let class = value.getattr(intern!(py, "__class__"))?;
            let qualname = class.getattr(intern!(py, "__qualname__"))?;
            let text = concat_text(&[
                &PyString::new(py, "<"),
                &format_field(&qualname)?,
                &PyString::new(py, &format!(" object {}>", value.as_ptr() as usize)),
            ])?;
            return Ok(Defaulted::Ext(0, utf8_payload(text)?));
        }
        match self.repr(value, true)? {
            ReprText::Py(text) => Ok(Defaulted::Ext(0, utf8_payload(text)?)),
            ReprText::Native(text) => Ok(Defaulted::NativeExt(0, text)),
        }
    }

    /// `repr(value)`, reusing the result for an object already repr'd while
    /// encoding this event (see `NativeMsgpackEncoder` for why that is
    /// sound). With `compose_methods`, a bound method's repr is built as
    /// CPython's `method_repr` builds it, so the repr of its `__self__`
    /// comes from the memo too. Without it (that `__self__` repr), a memo
    /// hit still applies the recursion guard `PyObject_Repr` would enter.
    fn repr<'py>(
        &mut self,
        value: &Bound<'py, PyAny>,
        compose_methods: bool,
    ) -> PyResult<ReprText<'py>> {
        if let Some(text) = self.repr_memo.get(value.py(), value.as_ptr() as usize) {
            if !compose_methods {
                // `method_repr`'s `PyObject_Repr(__self__)` enters the
                // recursion guard one level below the method's own guard.
                recursion_check(value.py())?;
            }
            return Ok(text);
        }
        // Safety: reads a live object's type.
        let value_type = unsafe { ffi::Py_TYPE(value.as_ptr()) };
        // Python 3.8's recursion guard is a macro over thread state that
        // can't be mirrored from Rust, so methods there go through CPython.
        let is_method = cfg!(Py_3_9) && value_type as usize == self.serializer.method_type;
        let text = match compose_methods && is_method {
            true => self.guarded_method_repr(value)?,
            false => match self
                .serializer
                .builtin_repr(value, &mut self.repr_memo.arena)?
            {
                Some(text) => text,
                None => ReprText::Py(self.plain_repr(value)?.into_any()),
            },
        };
        match &text {
            ReprText::Native(native) => self
                .repr_memo
                .insert(value, MemoText::Native(native.clone())),
            ReprText::Py(text) => {
                if let Ok(text) = text.cast_exact::<PyString>() {
                    self.repr_memo
                        .insert(value, MemoText::Py(text.clone().unbind()));
                }
            }
        }
        Ok(text)
    }

    /// `PyObject_Repr(value)`, reusing an earlier result of a certified
    /// repr across events when its dependencies are provably unchanged (see
    /// `repr_reuse`).
    fn plain_repr<'py>(&self, value: &Bound<'py, PyAny>) -> PyResult<Bound<'py, PyString>> {
        match self.value_interning {
            Some(context) => context.interning.repr_reuse.repr(value),
            None => value.repr(),
        }
    }

    /// `PyObject_Repr` around `method_repr`: the signal check and the
    /// recursion guard it applies before calling `tp_repr`.
    #[cfg(Py_3_9)]
    fn guarded_method_repr<'py>(&mut self, method: &Bound<'py, PyAny>) -> PyResult<ReprText<'py>> {
        let py = method.py();
        /// Leaves the recursion guard even if a Python `PanicException`
        /// unwinds through the composition.
        struct LeaveRecursiveCall;
        impl Drop for LeaveRecursiveCall {
            fn drop(&mut self) {
                // Safety: only constructed after a successful enter.
                unsafe { ffi::Py_LeaveRecursiveCall() };
            }
        }
        // Safety: plain C API calls.
        unsafe {
            if ffi::PyErr_CheckSignals() != 0 {
                return Err(PyErr::fetch(py));
            }
            if ffi::Py_EnterRecursiveCall(c" while getting the repr of an object".as_ptr()) != 0 {
                return Err(PyErr::fetch(py));
            }
        }
        let _guard = LeaveRecursiveCall;
        self.bound_method_repr(method)
    }

    #[cfg(not(Py_3_9))]
    fn guarded_method_repr<'py>(&mut self, _method: &Bound<'py, PyAny>) -> PyResult<ReprText<'py>> {
        unreachable!("bound methods are not composed on Python 3.8")
    }

    /// CPython's `method_repr` (identical in 3.8 through 3.14):
    /// `"<bound method %V of %R>"` with `__qualname__`, else `__name__`, of
    /// `__func__` (missing or non-str gives `"?"`) and `repr(__self__)`.
    #[cold]
    #[inline(never)]
    fn bound_method_repr<'py>(&mut self, method: &Bound<'py, PyAny>) -> PyResult<ReprText<'py>> {
        let py = method.py();
        // Safety: `method` is an exact bound method, whose function and self
        // are set at creation, never NULL and kept alive by the method.
        let (function, bound_self) = unsafe {
            (
                Bound::from_borrowed_ptr(py, PyMethod_Function(method.as_ptr())),
                Bound::from_borrowed_ptr(py, PyMethod_Self(method.as_ptr())),
            )
        };
        let name = match optional_attr(&function, intern!(py, "__qualname__"))? {
            Some(name) => Some(name),
            None => optional_attr(&function, intern!(py, "__name__"))?,
        };
        let name = name.and_then(|name| name.cast_into::<PyString>().ok());
        let self_repr = self.repr(&bound_self, false)?;
        let name_text = match &name {
            Some(name) => name.to_str().ok(),
            None => Some("?"),
        };
        if let Some(name) = name_text {
            let arena = &mut self.repr_memo.arena;
            arena.reserve(REPR_TEXT_RESERVE);
            let start = arena.len();
            arena.extend_from_slice(b"<bound method ");
            arena.extend_from_slice(name.as_bytes());
            arena.extend_from_slice(b" of ");
            let composed = match &self_repr {
                ReprText::Native(text) => {
                    arena.extend_from_within(text.clone());
                    true
                }
                ReprText::Py(text) => match text.cast::<PyString>().ok().map(|t| t.to_str()) {
                    Some(Ok(text)) => {
                        arena.extend_from_slice(text.as_bytes());
                        true
                    }
                    _ => false,
                },
            };
            if composed {
                arena.push(b'>');
                return Ok(ReprText::Native(start..arena.len()));
            }
            arena.truncate(start);
        }
        let self_repr = match self_repr {
            ReprText::Py(text) => text
                .cast_into::<PyString>()
                .expect("PyObject_Repr returns a str"),
            ReprText::Native(text) => PyString::new(
                py,
                std::str::from_utf8(&self.repr_memo.arena[text])
                    .expect("native repr text is UTF-8"),
            ),
        };
        let name = name.as_ref().map_or(ptr::null_mut(), |name| name.as_ptr());
        // Safety: `%V` takes a str or NULL plus a C string fallback, `%U` a
        // str; the format is `method_repr`'s with `%R` already applied.
        unsafe {
            Bound::from_owned_ptr_or_err(
                py,
                ffi::PyUnicode_FromFormat(
                    c"<bound method %V of %U>".as_ptr(),
                    name,
                    c"?".as_ptr(),
                    self_repr.as_ptr(),
                ),
            )
            .map(ReprText::Py)
        }
    }

    /// A global of `kolo.serialize`, as the hook's `LOAD_GLOBAL` sees it.
    fn global<'py>(&self, name: &Bound<'py, PyString>) -> PyResult<Bound<'py, PyAny>> {
        let py = name.py();
        match self.serializer.globals.bind(py).get_item(name)? {
            Some(value) => Ok(value),
            None => {
                let message = format!("name '{name}' is not defined");
                let kwargs = PyDict::new(py);
                kwargs.set_item(intern!(py, "name"), name)?;
                // NameError takes `name=` since Python 3.10.
                match py
                    .get_type::<PyNameError>()
                    .call((&message,), Some(&kwargs))
                {
                    Ok(error) => Err(PyErr::from_value(error)),
                    Err(_) => Err(PyNameError::new_err(message)),
                }
            }
        }
    }

    /// `_get_queryset_class()`, reading its cache directly once populated.
    fn queryset_class<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        if self.global(intern!(py, "_QuerySet_checked"))?.is_truthy()? {
            return self.global(intern!(py, "_QuerySet"));
        }
        self.global(intern!(py, "_get_queryset_class"))?.call0()
    }

    /// `isinstance(value, class)`.
    ///
    /// `PyObject_IsInstance` falls back to reading `value.__class__` whenever
    /// the real type is not a subclass, and that read can run user code
    /// (Django's `LazyObject` evaluates itself there). When the type provably
    /// has the default `__class__` and `__getattribute__`, that read returns
    /// `type(value)` without side effects and the subtype test is the answer.
    fn isinstance(
        &self,
        value: &Bound<'_, PyAny>,
        class: *mut ffi::PyObject,
        class_is_type: &mut Option<bool>,
    ) -> PyResult<bool> {
        let py = value.py();
        // Safety: live objects; only static type objects are dereferenced.
        unsafe {
            let value_type = ffi::Py_TYPE(value.as_ptr());
            if value_type.cast() == class {
                return Ok(true);
            }
            if ffi::PyType_CheckExact(class) != 0 {
                if ffi::PyType_IsSubtype(value_type, class.cast()) != 0 {
                    return Ok(true);
                }
                if *class_is_type.get_or_insert_with(|| {
                    _PyType_Lookup(value_type, intern!(py, "__getattribute__").as_ptr()) as usize
                        == self.serializer.object_getattribute
                        && _PyType_Lookup(value_type, intern!(py, "__class__").as_ptr()) as usize
                            == self.serializer.object_class
                }) {
                    return Ok(false);
                }
            }
            // This can run user code (`__class__`, `__instancecheck__`)
            // that changes what the proof above relied on.
            *class_is_type = None;
            match ffi::PyObject_IsInstance(value.as_ptr(), class) {
                -1 => Err(PyErr::fetch(py)),
                matched => Ok(matched == 1),
            }
        }
    }

    /// `list(value)` or `dict(value)`.
    fn call_builtin<'py>(
        &self,
        value: &Bound<'py, PyAny>,
        builtin: *mut ffi::PyObject,
    ) -> PyResult<Bound<'py, PyAny>> {
        // Safety: `builtin` is a static type object. (pyo3's
        // `PyObject_CallOneArg` shim crashes on Python 3.8, so call through
        // `Bound::call1`.)
        unsafe { Bound::from_borrowed_ptr(value.py(), builtin) }.call1((value,))
    }

    fn reserve_extension_header(&mut self, buf: &mut Vec<u8>) -> usize {
        let start = buf.len();
        buf.resize(start + MAX_EXT_HEADER_LEN, 0);
        self.reserved_header_bytes += MAX_EXT_HEADER_LEN;
        start
    }

    /// `_dump_msgpack(list(obj))`: a fresh Packer, so a fresh recursion
    /// limit, packing the copied items. Python spends stack frames on each
    /// such nesting; a cycle through tuples ends in RecursionError there,
    /// which the hook then reports as a serialization error (in the careful
    /// pass; the first pass leaves it to that pass). `owner` is the value
    /// the items came from.
    fn pack_extension_items(
        &mut self,
        owner: &Bound<'_, PyAny>,
        items: SequenceItems<'_, '_>,
        buf: &mut Vec<u8>,
    ) -> Packed {
        let base_frames = if self.careful {
            PYTHON_FRAMES_PER_CAREFUL_NESTED_EXTENSION
        } else {
            PYTHON_FRAMES_PER_NESTED_EXTENSION
        };
        let frames_per_extension = base_frames + i32::from(self.lightweight_repr);
        // Safety: reads the interpreter's recursion limit, which is never
        // below 64 frames in practice.
        if self.extension_depth >= 16
            && self.extension_depth >= unsafe { ffi::Py_GetRecursionLimit() } / frames_per_extension
        {
            return self.fail(PyRecursionError::new_err(
                "maximum recursion depth exceeded",
            ));
        }
        let tracked = self.careful || self.extension_depth >= FIRST_PASS_CYCLE_CHECK_DEPTH;
        if tracked && !self.enter_extension(owner) {
            return self.fail(PyRecursionError::new_err(
                "maximum recursion depth exceeded",
            ));
        }
        self.extension_depth += 1;
        let limit = self.serializer.recurse_limit;
        let packed = match items {
            SequenceItems::List(list) => self.pack(list.as_any(), buf, limit),
            SequenceItems::Tuple(tuple) => self.nested(tuple.py(), |encoder| {
                let Some(len) = checked_msgpack_len(tuple.len()) else {
                    return encoder.fail(PyValueError::new_err("list is too large"));
                };
                rmp::encode::write_array_len(buf, len).expect("Writing to memory, not I/O");
                tuple.iter().enumerate().try_for_each(|(index, item)| {
                    encoder.pack(&item, buf, limit - 1)?;
                    if index & BUDGET_CHECK_MASK == BUDGET_CHECK_MASK {
                        encoder.check_budget(buf, 0)?;
                    }
                    Ok(())
                })
            }),
        };
        if tracked {
            self.active.pop();
        }
        self.extension_depth -= 1;
        packed
    }

    /// Records that `owner`'s payload is being packed. In the first pass, an
    /// owner already being packed further up is a cycle, which the Python
    /// serializer follows until RecursionError: return false to fail the
    /// same way at once, for the careful pass to record.
    #[inline(never)]
    fn enter_extension(&mut self, owner: &Bound<'_, PyAny>) -> bool {
        let identity = owner.as_ptr() as usize;
        if !self.careful && self.active.contains(&identity) {
            return false;
        }
        self.active.push(identity);
        true
    }

    fn value_interner_cell(&mut self) -> Option<&'a RefCell<ValueInterner>> {
        if self.value_interner_cell.is_none() {
            self.value_interner_cell =
                Some(self.value_interning?.interning.interners.get_or_default());
        }
        self.value_interner_cell
    }

    fn lookup_value(
        &mut self,
        identity: usize,
        kind: InternedValueKind,
        payload: &[u8],
        buf: &mut Vec<u8>,
    ) -> ValueLookup {
        let Some(value_context) = self.value_interning else {
            return ValueLookup::WriteInline;
        };
        let value_interning = value_context.interning;
        let Some(value_interner_cell) = self.value_interner_cell() else {
            return ValueLookup::WriteInline;
        };
        let mut value_interner = value_interner_cell.borrow_mut();
        let global_candidate_bytes = &value_interning.candidate_bytes;
        let signature = ValueSignature::new(kind, payload);
        value_interner.make_identity_room(identity, global_candidate_bytes);
        let mut reset_to_seen = false;
        let lookup = match value_interner.values.get_mut(&identity) {
            Some(CachedValue::Seen(seen_signature)) => {
                if *seen_signature == signature {
                    ValueLookup::CacheCurrent
                } else {
                    *seen_signature = signature;
                    ValueLookup::WriteInline
                }
            }
            Some(CachedValue::Candidate(value)) => {
                if value.matches(identity, kind, payload) {
                    let value = Arc::clone(value);
                    let value_len = value.resident_len();
                    let mut table = value_interning
                        .table
                        .lock()
                        .expect("value table mutex poisoned");
                    let Some(id) = table.insert_value(Arc::clone(&value)) else {
                        value_interning.disabled.store(true, Ordering::Relaxed);
                        return ValueLookup::WriteInline;
                    };
                    if let Err(error) = value_context.publish_value(id, Arc::clone(&value.encoded))
                    {
                        table.remove_last(id);
                        // A capture that cannot publish one value will never accept later references reliably;
                        // disable interning once rather than re-locking the process-wide table on every callback.
                        value_interning.disabled.store(true, Ordering::Relaxed);
                        if value_context.writer_circuit_is_open() {
                            return ValueLookup::WriterCircuit(error.to_string());
                        }
                        return ValueLookup::WriteInline;
                    }
                    drop(table);
                    value_interner.candidate_bytes =
                        value_interner.candidate_bytes.saturating_sub(value_len);
                    global_candidate_bytes.fetch_sub(value_len, Ordering::Relaxed);
                    value_interner
                        .values
                        .insert(identity, CachedValue::Interned { value, id });
                    write_value_reference(buf, id);
                    ValueLookup::ReferenceWritten
                } else {
                    reset_to_seen = true;
                    ValueLookup::WriteInline
                }
            }
            Some(CachedValue::Interned { value, id }) => {
                if value.matches(identity, kind, payload) {
                    if let Err(error) = value_context.publish_value(*id, Arc::clone(&value.encoded))
                    {
                        value_interning.disabled.store(true, Ordering::Relaxed);
                        if value_context.writer_circuit_is_open() {
                            return ValueLookup::WriterCircuit(error.to_string());
                        }
                        return ValueLookup::WriteInline;
                    }
                    write_value_reference(buf, *id);
                    ValueLookup::ReferenceWritten
                } else {
                    reset_to_seen = true;
                    ValueLookup::WriteInline
                }
            }
            None => {
                value_interner
                    .values
                    .insert(identity, CachedValue::Seen(signature));
                ValueLookup::WriteInline
            }
        };
        if reset_to_seen {
            // CPython can reuse a dead object's address. Only a complete byte
            // comparison is allowed to produce a reference; a mismatch starts
            // this address over as a fresh observation.
            value_interner.remove(identity, global_candidate_bytes);
            value_interner
                .values
                .insert(identity, CachedValue::Seen(signature));
        }
        lookup
    }

    fn cache_current_value(
        &mut self,
        identity: usize,
        kind: InternedValueKind,
        payload_len: usize,
        object: Py<PyAny>,
        encoded: Vec<u8>,
        buf: &mut Vec<u8>,
    ) {
        let Some(value_context) = self.value_interning else {
            buf.extend_from_slice(&encoded);
            return;
        };
        let value_interning = value_context.interning;
        let Some(value_interner_cell) = self.value_interner_cell() else {
            buf.extend_from_slice(&encoded);
            return;
        };
        let mut value_interner = value_interner_cell.borrow_mut();
        let global_candidate_bytes = &value_interning.candidate_bytes;
        let payload_start = encoded
            .len()
            .checked_sub(payload_len)
            .expect("encoded msgpack value contains its payload");
        let resident_len = encoded.len().saturating_add(payload_len);
        if !value_interner.make_candidate_room(identity, resident_len, global_candidate_bytes) {
            buf.extend_from_slice(&encoded);
            return;
        }
        let value = Arc::new(InternedValue {
            encoded: encoded.into(),
            payload_start,
            kind,
            object,
        });
        value_interner.candidate_bytes += value.resident_len();
        buf.extend_from_slice(&value.encoded);
        value_interner
            .values
            .insert(identity, CachedValue::Candidate(value));
    }
}

enum SequenceItems<'b, 'py> {
    Tuple(&'b Bound<'py, PyTuple>),
    List(&'b Bound<'py, PyList>),
}

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
struct BuiltinReprs {
    object: usize,
    class: usize,
    function: usize,
    builtin: usize,
    /// How this C library prints `%p`; `None` (unrecognized) leaves every
    /// repr to CPython.
    pointer: Option<PointerFormat>,
}

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
impl BuiltinReprs {
    fn new(py: Python<'_>) -> Self {
        let slot = |type_: *const ffi::PyTypeObject| {
            // Safety: reads a slot of a static type object.
            unsafe { (*type_).tp_repr }.map_or(0, |repr| repr as usize)
        };
        Self {
            object: slot(ptr::addr_of!(ffi::PyBaseObject_Type)),
            class: slot(ptr::addr_of!(ffi::PyType_Type)),
            function: slot(ptr::addr_of!(ffi::PyFunction_Type)),
            builtin: slot(ptr::addr_of!(ffi::PyCFunction_Type)),
            pointer: PointerFormat::probe(py),
        }
    }
}

/// `%p` in `PyUnicode_FromFormat`: the C library's `%p`, with a `0x`
/// prefix ensured. C libraries differ: glibc and Apple's libc print
/// lowercase hex without padding, musl (and so Emscripten) pads it to the
/// pointer width, MSVC prints uppercase hex padded to the pointer width. The
/// format in use is recognized once by asking CPython.
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub(super) struct PointerFormat {
    min_digits: usize,
    alphabet: &'static [u8; 16],
}

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
impl PointerFormat {
    pub(super) fn probe(py: Python<'_>) -> Option<Self> {
        let width = 2 * std::mem::size_of::<usize>();
        let candidates = [
            (1, b"0123456789abcdef"),
            (width, b"0123456789abcdef"),
            (width, b"0123456789ABCDEF"),
            (1, b"0123456789ABCDEF"),
        ]
        .map(|(min_digits, alphabet)| Self {
            min_digits,
            alphabet,
        });
        let probes = [0x1, 0xab, 0x1234_abcd, usize::MAX >> 4, usize::MAX];
        let expected = probes.map(|address| {
            // Safety: `%p` formats the pointer value without dereferencing it.
            unsafe {
                Bound::from_owned_ptr_or_err(
                    py,
                    ffi::PyUnicode_FromFormat(c"%p".as_ptr(), address as *mut std::ffi::c_void),
                )
            }
            .ok()
            .and_then(|text| text.cast_into::<PyString>().ok())
            .and_then(|text| text.to_str().ok().map(str::to_owned))
        });
        candidates.into_iter().find(|format| {
            probes.iter().zip(&expected).all(|(&address, expected)| {
                let mut text = Vec::new();
                format.push(&mut text, address as *mut ffi::PyObject);
                expected.as_deref().map(str::as_bytes) == Some(&text[..])
            })
        })
    }

    pub(super) fn push(&self, text: &mut Vec<u8>, pointer: *mut ffi::PyObject) {
        let address = pointer as usize;
        let digits =
            ((usize::BITS - address.leading_zeros()).div_ceil(4) as usize).max(self.min_digits);
        text.extend_from_slice(b"0x");
        for digit in (0..digits).rev() {
            text.push(self.alphabet[(address >> (4 * digit)) & 0xf]);
        }
    }
}

/// The head of `PyCFunctionObject`, unchanged from 3.9 through 3.14.
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
#[repr(C)]
struct CFunctionHead {
    ob_base: ffi::PyObject,
    m_ml: *mut ffi::PyMethodDef,
    m_self: *mut ffi::PyObject,
}

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
fn extend<const N: usize>(text: &mut Vec<u8>, parts: [&str; N]) {
    for part in parts {
        text.extend_from_slice(part.as_bytes());
    }
}

/// A type's `__module__` and `__qualname__` as `object_repr`/`type_repr`
/// read them, or `None` where they fall back to `tp_name`.
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
enum ClassName<'py> {
    /// A static type's dotted `tp_name`, split at its last dot.
    Static(&'py str, &'py str),
    Qualified(Bound<'py, PyString>, Bound<'py, PyString>),
    TpName,
}

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
impl SerializerState {
    /// `repr(value)` for the exact CPython `tp_repr` slots of plain objects,
    /// classes, functions and builtin functions, written natively instead
    /// of through `PyUnicode_FromFormat`. `None` when `value`'s repr is not
    /// one of those slots (or would fail): the caller runs `repr()`.
    ///
    /// Mirrors `PyObject_Repr` around the slot: the pending-signal check and
    /// the recursion guard. The slots themselves run no Python code, except
    /// that a heap type's `__module__` is read from its dict as CPython reads
    /// it. Where the text is not valid UTF-8 (lone surrogates in a name) the
    /// slot's own `PyUnicode_FromFormat` call is made.
    ///
    /// Not on free-threaded builds: the names read here (`func_qualname`,
    /// `ht_qualname`, `tp_name`) are borrowed, and another thread assigning
    /// `__qualname__`/`__name__` could free them before they are used.
    fn builtin_repr<'py>(
        &self,
        value: &Bound<'py, PyAny>,
        arena: &mut Vec<u8>,
    ) -> PyResult<Option<ReprText<'py>>> {
        let py = value.py();
        // `PyObject_Repr` checks signals before it looks at the type: a
        // handler may change which repr runs. Checking again in a fallback
        // `repr()` finds nothing pending.
        // Safety: plain C API call.
        if unsafe { ffi::PyErr_CheckSignals() } != 0 {
            return Err(PyErr::fetch(py));
        }
        let object = value.as_ptr();
        let reprs = &self.builtin_reprs;
        let Some(pointer) = reprs.pointer else {
            return Ok(None);
        };
        // Safety: reads a live object's type and the type's slot.
        let (value_type, slot) = unsafe {
            let value_type = ffi::Py_TYPE(object);
            (
                value_type,
                (*value_type).tp_repr.map_or(0, |repr| repr as usize),
            )
        };
        let kind = if slot == reprs.object {
            BuiltinRepr::Object(value_type)
        } else if slot == reprs.class && unsafe { ffi::PyType_Check(object) } != 0 {
            let class = object.cast::<ffi::PyTypeObject>();
            if unsafe { (*class).tp_name }.is_null() {
                return Ok(None);
            }
            BuiltinRepr::Class(class)
        } else if slot == reprs.function {
            BuiltinRepr::Function
        } else if slot == reprs.builtin {
            BuiltinRepr::Builtin
        } else {
            return Ok(None);
        };
        if let BuiltinRepr::Object(class) | BuiltinRepr::Class(class) = kind {
            // Safety: a live type object.
            let static_type =
                unsafe { ffi::PyType_GetFlags(class) } & ffi::Py_TPFLAGS_HEAPTYPE == 0;
            if static_type && tp_name(class).is_none() {
                return Ok(None);
            }
        }

        /// Leaves the recursion guard even if a Python `PanicException`
        /// unwinds through the repr.
        struct LeaveRecursiveCall;
        impl Drop for LeaveRecursiveCall {
            fn drop(&mut self) {
                // Safety: only constructed after a successful enter.
                unsafe { ffi::Py_LeaveRecursiveCall() };
            }
        }
        // Safety: plain C API call.
        if unsafe { ffi::Py_EnterRecursiveCall(c" while getting the repr of an object".as_ptr()) }
            != 0
        {
            return Err(PyErr::fetch(py));
        }
        let _guard = LeaveRecursiveCall;

        arena.reserve(REPR_TEXT_RESERVE);
        let start = arena.len();
        let text = &mut *arena;
        let formatted = match kind {
            BuiltinRepr::Object(class) => match class_name(py, class)? {
                ClassName::Static(module, name) => {
                    extend(text, ["<", module, ".", name, " object at "]);
                    None
                }
                ClassName::Qualified(module, name) => {
                    match (module.to_str(), name.to_str()) {
                        (Ok(module), Ok(name)) => {
                            extend(text, ["<", module, ".", name, " object at "]);
                            None
                        }
                        // Safety: two str objects and the object, as
                        // `object_repr` passes them.
                        _ => Some(unsafe {
                            ffi::PyUnicode_FromFormat(
                                c"<%U.%U object at %p>".as_ptr(),
                                module.as_ptr(),
                                name.as_ptr(),
                                object,
                            )
                        }),
                    }
                }
                ClassName::TpName => match tp_name(class) {
                    Some(name) => {
                        extend(text, ["<", name, " object at "]);
                        None
                    }
                    // Safety: the type's C name and the object.
                    None => Some(unsafe {
                        ffi::PyUnicode_FromFormat(
                            c"<%s object at %p>".as_ptr(),
                            (*class).tp_name,
                            object,
                        )
                    }),
                },
            },
            BuiltinRepr::Class(class) => {
                let formatted = match class_name(py, class)? {
                    ClassName::Static(module, name) => {
                        extend(text, ["<class '", module, ".", name, "'>"]);
                        None
                    }
                    ClassName::Qualified(module, name) => {
                        match (module.to_str(), name.to_str()) {
                            (Ok(module), Ok(name)) => {
                                extend(text, ["<class '", module, ".", name, "'>"]);
                                None
                            }
                            // Safety: two str objects, as `type_repr` passes them.
                            _ => Some(unsafe {
                                ffi::PyUnicode_FromFormat(
                                    c"<class '%U.%U'>".as_ptr(),
                                    module.as_ptr(),
                                    name.as_ptr(),
                                )
                            }),
                        }
                    }
                    ClassName::TpName => match tp_name(class) {
                        Some(name) => {
                            extend(text, ["<class '", name, "'>"]);
                            None
                        }
                        // Safety: the type's C name.
                        None => Some(unsafe {
                            ffi::PyUnicode_FromFormat(c"<class '%s'>".as_ptr(), (*class).tp_name)
                        }),
                    },
                };
                if formatted.is_none() {
                    return Ok(Some(ReprText::Native(start..text.len())));
                }
                formatted
            }
            BuiltinRepr::Function => {
                // Safety: an exact function object; `func_qualname` is a
                // str (its setter requires one) kept alive by the function.
                let qualname = unsafe {
                    Bound::from_borrowed_ptr(
                        py,
                        (*object.cast::<ffi::PyFunctionObject>()).func_qualname,
                    )
                };
                match qualname
                    .cast::<PyString>()
                    .ok()
                    .and_then(|q| q.to_str().ok())
                {
                    Some(qualname) => {
                        extend(text, ["<function ", qualname, " at "]);
                        None
                    }
                    // Safety: the function's qualname and the function.
                    None => Some(unsafe {
                        ffi::PyUnicode_FromFormat(
                            c"<function %U at %p>".as_ptr(),
                            qualname.as_ptr(),
                            object,
                        )
                    }),
                }
            }
            BuiltinRepr::Builtin => {
                // Safety: `builtin_function_or_method` (or its PyCMethod
                // subclass) starts with `CFunctionHead`; `ml_name` is a C
                // string and `m_self` NULL or a live object.
                unsafe {
                    let function = object.cast::<CFunctionHead>();
                    let ml_name = (*(*function).m_ml).ml_name;
                    let bound_self = (*function).m_self;
                    let name = std::ffi::CStr::from_ptr(ml_name).to_str().ok();
                    if bound_self.is_null() || ffi::PyModule_Check(bound_self) != 0 {
                        match name {
                            Some(name) => {
                                extend(text, ["<built-in function ", name, ">"]);
                                return Ok(Some(ReprText::Native(start..text.len())));
                            }
                            None => Some(ffi::PyUnicode_FromFormat(
                                c"<built-in function %s>".as_ptr(),
                                ml_name,
                            )),
                        }
                    } else {
                        let self_type = ffi::Py_TYPE(bound_self);
                        match (name, tp_name(self_type)) {
                            (Some(name), Some(type_name)) => {
                                extend(
                                    text,
                                    ["<built-in method ", name, " of ", type_name, " object at "],
                                );
                                pointer.push(text, bound_self);
                                text.push(b'>');
                                return Ok(Some(ReprText::Native(start..text.len())));
                            }
                            _ => Some(ffi::PyUnicode_FromFormat(
                                c"<built-in method %s of %s object at %p>".as_ptr(),
                                ml_name,
                                (*self_type).tp_name,
                                bound_self,
                            )),
                        }
                    }
                }
            }
        };
        if let Some(formatted) = formatted {
            text.truncate(start);
            // Safety: `PyUnicode_FromFormat` returns a new str or NULL.
            return unsafe { Bound::from_owned_ptr_or_err(py, formatted) }
                .map(|formatted| Some(ReprText::Py(formatted)));
        }
        pointer.push(text, object);
        text.push(b'>');
        Ok(Some(ReprText::Native(start..text.len())))
    }
}

#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
#[derive(Clone, Copy)]
enum BuiltinRepr {
    Object(*mut ffi::PyTypeObject),
    Class(*mut ffi::PyTypeObject),
    Function,
    Builtin,
}

/// A type's `tp_name`, when it is valid UTF-8 (as `%s` would decode it).
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
fn tp_name<'a>(class: *mut ffi::PyTypeObject) -> Option<&'a str> {
    // Safety: a ready type's `tp_name` is a NUL-terminated C string that
    // lives as long as the type.
    unsafe { std::ffi::CStr::from_ptr((*class).tp_name) }
        .to_str()
        .ok()
}

/// `type_module` and `type_qualname` as `object_repr` and `type_repr` use
/// them: a module that is missing, not a str, or `"builtins"` means the
/// repr uses `tp_name` instead.
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
fn class_name<'py>(py: Python<'py>, class: *mut ffi::PyTypeObject) -> PyResult<ClassName<'py>> {
    // Safety: a live type object; heap types' `tp_dict` and `ht_qualname`
    // are set once ready.
    unsafe {
        if ffi::PyType_GetFlags(class) & ffi::Py_TPFLAGS_HEAPTYPE == 0 {
            let full = tp_name(class).expect("checked by the caller");
            return Ok(match full.rsplit_once('.') {
                Some((module, name)) if module != "builtins" => ClassName::Static(module, name),
                _ => ClassName::TpName,
            });
        }
        let mut module = ptr::null_mut();
        if ffi::compat::PyDict_GetItemRef(
            (*class).tp_dict,
            intern!(py, "__module__").as_ptr(),
            &mut module,
        ) < 0
        {
            drop(PyErr::fetch(py));
        }
        let module = Bound::from_owned_ptr_or_opt(py, module);
        let name =
            Bound::from_borrowed_ptr(py, (*class.cast::<ffi::PyHeapTypeObject>()).ht_qualname)
                .cast_into::<PyString>()
                .expect("__qualname__ is always a str");
        Ok(
            match module.and_then(|module| module.cast_into::<PyString>().ok()) {
                Some(module)
                    if ffi::PyUnicode_CompareWithASCIIString(
                        module.as_ptr(),
                        c"builtins".as_ptr(),
                    ) != 0 =>
                {
                    ClassName::Qualified(module, name)
                }
                _ => ClassName::TpName,
            },
        )
    }
}

#[cfg(any(not(Py_3_12), Py_GIL_DISABLED))]
impl SerializerState {
    fn builtin_repr<'py>(
        &self,
        _value: &Bound<'py, PyAny>,
        _arena: &mut Vec<u8>,
    ) -> PyResult<Option<ReprText<'py>>> {
        Ok(None)
    }
}

/// A per-type answer to "does `msgpack_encode_hook`'s `isinstance` ladder
/// match nothing for this type?", so values of common types (functions,
/// methods, classes, plain objects) skip straight to the `repr` the ladder
/// ends in.
///
/// The answer is cached only when it is a function of the type alone:
/// every ladder class is an exact `type` (so no `__instancecheck__`), and
/// the value's type provably reads `__class__` as `type(value)` (so
/// `isinstance` is the subtype test on that type's MRO). It is keyed by the
/// type's `tp_version_tag`, which CPython clears whenever the type or one of
/// its bases changes (`__bases__`, `__getattribute__`, `__class__`) and
/// never reissues, and by a generation bumped whenever a `kolo.serialize`
/// global other than `IN_KOLO_PROFILER` changes (`datetime` rebound by
/// freezegun, `_QuerySet` set by Django's first import, ...). GIL builds
/// only: the watcher runs before the dict changes, which another thread
/// could observe in between on a free-threaded build.
#[cfg(all(Py_3_12, not(Py_GIL_DISABLED)))]
mod type_ladder {
    use super::*;
    use pyo3::types::PyBool;
    use std::cell::Cell;
    use std::ffi::c_int;
    use std::sync::atomic::AtomicU64;

    extern "C" {
        fn PyDict_AddWatcher(callback: DictWatchCallback) -> c_int;
        fn PyDict_Watch(watcher_id: c_int, dict: *mut ffi::PyObject) -> c_int;
    }

    type DictWatchCallback = unsafe extern "C" fn(
        event: c_int,
        dict: *mut ffi::PyObject,
        key: *mut ffi::PyObject,
        new_value: *mut ffi::PyObject,
    ) -> c_int;

    static GLOBALS_GENERATION: AtomicU64 = AtomicU64::new(0);
    /// The generation `GLOBALS_STR_KEYS` was computed for (+1, so 0 is
    /// "never").
    static STR_KEYS_GENERATION: AtomicU64 = AtomicU64::new(0);
    static GLOBALS_STR_KEYS: AtomicBool = AtomicBool::new(false);
    static PROFILER_FLAG_KEY: AtomicUsize = AtomicUsize::new(0);

    unsafe extern "C" fn globals_changed(
        _event: c_int,
        _dict: *mut ffi::PyObject,
        key: *mut ffi::PyObject,
        _new_value: *mut ffi::PyObject,
    ) -> c_int {
        // Every encode sets and resets IN_KOLO_PROFILER, which the ladder
        // never reads. Any other key, or a whole-dict event, invalidates.
        if key as usize != PROFILER_FLAG_KEY.load(Ordering::Relaxed) {
            GLOBALS_GENERATION.fetch_add(1, Ordering::Release);
        }
        0
    }

    /// Watch `kolo.serialize`'s globals; `false` leaves the cache unused.
    pub(super) fn watch_globals(globals: &Bound<'_, PyDict>) -> bool {
        let py = globals.py();
        PROFILER_FLAG_KEY.store(
            intern!(py, "IN_KOLO_PROFILER").as_ptr() as usize,
            Ordering::Relaxed,
        );
        // Safety: registers a static callback and watches a live dict. Both
        // fail only when the interpreter's watcher slots are all taken, in
        // which case the ladder simply always runs.
        unsafe {
            let watcher_id = PyDict_AddWatcher(globals_changed);
            if watcher_id < 0 {
                drop(PyErr::fetch(py));
                return false;
            }
            if PyDict_Watch(watcher_id, globals.as_ptr()) < 0 {
                drop(PyErr::fetch(py));
                return false;
            }
        }
        true
    }

    #[derive(Clone, Copy)]
    struct Entry {
        value_type: usize,
        version: u32,
        generation: u64,
        lightweight_repr: bool,
        falls_through: bool,
    }

    const ENTRIES: usize = 256;

    thread_local! {
        static CACHE: [Cell<Entry>; ENTRIES] = const {
            [const {
                Cell::new(Entry {
                    value_type: 0,
                    version: 0,
                    generation: 0,
                    lightweight_repr: false,
                    falls_through: false,
                })
            }; ENTRIES]
        };
    }

    /// Whether the type's version tag is valid, so any change to the type
    /// or its bases replaces it. On 3.12 a nonzero tag is not enough: tag
    /// exhaustion while tagging the bases leaves the type's own tag set
    /// without the flag, and `PyType_Modified` then leaves it in place.
    /// From 3.13 bases are tagged first and the flag is no longer set.
    fn has_valid_version(value_type: *mut ffi::PyTypeObject) -> bool {
        // Safety: a live type object.
        unsafe {
            (*value_type).tp_version_tag != 0
                && (cfg!(Py_3_13)
                    || ffi::PyType_HasFeature(value_type, ffi::Py_TPFLAGS_VALID_VERSION_TAG) != 0)
        }
    }

    impl SerializerState {
        /// Whether a value of `value_type` provably matches none of the
        /// hook's `isinstance` checks in this mode.
        pub(super) fn falls_through_ladder(
            &self,
            value: &Bound<'_, PyAny>,
            lightweight_repr: bool,
        ) -> bool {
            if !self.globals_watched {
                return false;
            }
            // Read before the globals the classification depends on, so a
            // change made meanwhile leaves the entry stale, never wrong.
            let generation = GLOBALS_GENERATION.load(Ordering::Acquire);
            let value_type = value.get_type_ptr();
            let key = value_type as usize;
            let slot = (key >> 4 ^ key >> 12 ^ usize::from(lightweight_repr)) % ENTRIES;
            // Safety: a live type object's version tag.
            let version = unsafe { (*value_type).tp_version_tag };
            let cached = CACHE.with(|cache| cache[slot].get());
            if has_valid_version(value_type)
                && cached.value_type == key
                && cached.version == version
                && cached.generation == generation
                && cached.lightweight_repr == lightweight_repr
            {
                return cached.falls_through;
            }
            if !self.globals_have_str_keys(value.py(), generation) {
                return false;
            }
            let Some((version, falls_through)) =
                self.classify(value.py(), value_type, lightweight_repr)
            else {
                return false;
            };
            CACHE.with(|cache| {
                cache[slot].set(Entry {
                    value_type: key,
                    version,
                    generation,
                    lightweight_repr,
                    falls_through,
                })
            });
            falls_through
        }

        /// Whether every key of `kolo.serialize`'s globals is an exact str,
        /// so the hook's global lookups that a cache hit skips cannot run a
        /// key's `__eq__`. Any key change bumps the generation.
        fn globals_have_str_keys(&self, py: Python<'_>, generation: u64) -> bool {
            if STR_KEYS_GENERATION.load(Ordering::Acquire) == generation + 1 {
                return GLOBALS_STR_KEYS.load(Ordering::Relaxed);
            }
            let globals = self.globals.bind(py);
            let all_str = globals
                .keys()
                .iter()
                .all(|key| key.is_exact_instance_of::<PyString>());
            GLOBALS_STR_KEYS.store(all_str, Ordering::Relaxed);
            STR_KEYS_GENERATION.store(generation + 1, Ordering::Release);
            all_str
        }

        /// Whether the ladder in this mode provably matches nothing for
        /// `value_type` (false: run the ladder), with the version tag that
        /// holds for, or `None` when the type has no version tag to key it
        /// by. Runs no Python code, and reads only globals the hook reads in
        /// this mode (the lightweight hook never looks at the QuerySet).
        pub(super) fn classify(
            &self,
            py: Python<'_>,
            value_type: *mut ffi::PyTypeObject,
            lightweight_repr: bool,
        ) -> Option<(u32, bool)> {
            // Safety: lookups on a live type, which also assign it a
            // version tag; only the results' addresses are compared.
            let (version, class_is_type) = unsafe {
                let class = _PyType_Lookup(value_type, intern!(py, "__class__").as_ptr()) as usize;
                let getattribute =
                    _PyType_Lookup(value_type, intern!(py, "__getattribute__").as_ptr()) as usize;
                let getattro = (*value_type)
                    .tp_getattro
                    .map_or(0, |getattro| getattro as usize);
                let class_is_type = class == self.object_class
                    && (getattribute == self.object_getattribute
                        || getattro == ffi::PyObject_GenericGetAttr as usize
                        || getattro == self.type_getattro
                        || getattro == self.method_getattro);
                ((*value_type).tp_version_tag, class_is_type)
            };
            if !has_valid_version(value_type) {
                return None;
            }
            if !class_is_type {
                return Some((version, false));
            }
            let globals = self.globals.bind(py);
            let global = |name| globals.get_item(name).ok().flatten();
            let mut classes = vec![
                ptr::addr_of_mut!(ffi::PyTuple_Type).cast::<ffi::PyObject>(),
                ptr::addr_of_mut!(ffi::PySet_Type).cast(),
                ptr::addr_of_mut!(ffi::PyFrozenSet_Type).cast(),
                ptr::addr_of_mut!(ffi::PyDict_Type).cast(),
                ptr::addr_of_mut!(ffi::PyLong_Type).cast(),
            ];
            let named = [
                intern!(py, "datetime"),
                intern!(py, "date"),
                intern!(py, "time"),
                intern!(py, "Decimal"),
            ]
            .map(|name| global(name));
            for class in &named {
                let Some(class) = class else {
                    return Some((version, false));
                };
                classes.push(class.as_ptr());
            }
            // Safety: subtype tests between live type objects.
            let matches = |class: *mut ffi::PyObject| unsafe {
                ffi::PyType_CheckExact(class) == 0
                    || ffi::PyType_IsSubtype(value_type, class.cast()) != 0
            };
            if classes.into_iter().any(matches) {
                return Some((version, false));
            }
            if lightweight_repr {
                return Some((version, true));
            }
            let queryset_checked = global(intern!(py, "_QuerySet_checked"))
                .is_some_and(|checked| checked.is(&PyBool::new(py, true)));
            if !queryset_checked {
                return Some((version, false));
            }
            let falls_through = global(intern!(py, "_QuerySet"))
                .is_some_and(|queryset| queryset.is_none() || !matches(queryset.as_ptr()));
            Some((version, falls_through))
        }
    }

    #[cfg(test)]
    pub(super) fn globals_generation() -> u64 {
        GLOBALS_GENERATION.load(Ordering::Acquire)
    }
}

#[cfg(test)]
#[path = "tests.rs"]
mod tests;
