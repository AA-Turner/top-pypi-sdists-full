use hashbrown::HashMap;
use pyo3::exceptions::{
    PyException, PyNameError, PyOSError, PyRecursionError, PyRuntimeError, PyTypeError,
    PyValueError,
};
use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::{PyAny, PyBytes, PyDict, PyList, PyModule, PyString, PyTuple};
use pyo3::{ffi, intern};
use std::cell::RefCell;
use std::io::{self, Cursor};
use std::ptr;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use thread_local::ThreadLocal;

use super::super::trace_container::TraceCapture;

extern "C" {
    // Exported by every supported CPython (Cython-generated extensions rely
    // on it), but omitted from pyo3-ffi as underscore-prefixed. The result is
    // borrowed and only compared by address here.
    fn _PyType_Lookup(
        type_: *mut ffi::PyTypeObject,
        name: *mut ffi::PyObject,
    ) -> *mut ffi::PyObject;
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
    // `msgpack.packb`, for the leaf types msgpack packs without calling
    // `default`: ExtType, Timestamp and memoryview. Each call gets its own
    // Packer, as `kolo.serialize` keeps its packers per thread.
    packb: Py<PyAny>,
    recurse_limit: i32,
    object_class: usize,
    object_getattribute: usize,
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
        Ok(Self {
            globals: serialize.dict().unbind(),
            ext_type: msgpack.getattr(intern!(py, "ExtType"))?.unbind(),
            timestamp_type: msgpack.getattr(intern!(py, "Timestamp"))?.unbind(),
            packb: msgpack.getattr(intern!(py, "packb"))?.unbind(),
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

// Large immutable values are the dominant cost in traces with real payloads:
// copying the same request body, rendered template, or model blob into every
// call/return frame consumes callback time, writer bandwidth, and disk space.
// References remain an internal wire detail; every reader expands them back
// into the exact str/bytes value before exposing a frame.
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
    // Exact str/bytes are immutable and cannot run user finalizers. Keeping a
    // bounded strong reference makes their address a permanent identity, so
    // the hot reference path need not reread a multi-kilobyte payload merely
    // to defend against CPython reusing an address after object destruction.
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
}

impl Default for ValueInterning {
    fn default() -> Self {
        Self {
            interners: ThreadLocal::new(),
            table: Mutex::new(ValueTable::default()),
            disabled: AtomicBool::new(false),
            candidate_bytes: AtomicUsize::new(0),
        }
    }
}

impl ValueInterning {
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

fn checked_msgpack_len(len: usize) -> Option<u32> {
    u32::try_from(len).ok()
}

pub(crate) enum EncodeError {
    Python(PyErr),
    WriterCircuit(String),
}

impl EncodeError {
    pub(crate) fn into_pyerr(self) -> PyErr {
        match self {
            EncodeError::Python(error) => error,
            EncodeError::WriterCircuit(error) => PyOSError::new_err(error),
        }
    }
}

/// Failure marker for the recursive encoder; the cause is kept in
/// `NativeMsgpackEncoder::error` so the hot recursion returns a single byte.
struct Fail;

type Packed = Result<(), Fail>;

const MAX_EXT_HEADER_LEN: usize = 6;
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

/// What `msgpack_encode_hook` returned, for the Packer to pack next.
enum Defaulted<'py> {
    Ext(i8, Payload<'py>),
    /// A sequence extension whose items are already encoded after a
    /// reserved header at `start`.
    Sequence(i8, usize),
    /// `dict(obj)` for a dict subclass, packed (outside the hook's `try`)
    /// as a plain map.
    Dict(Bound<'py, PyDict>),
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

/// `value.encode("utf-8")`, checked like `msgpack.ExtType(code, data)`.
fn utf8_payload(value: Bound<'_, PyAny>) -> PyResult<Payload<'_>> {
    if let Ok(text) = value.cast_exact::<PyString>() {
        text.to_str()?;
        return Ok(Payload::Text(text.clone()));
    }
    let py = value.py();
    bytes_payload(value.call_method1(intern!(py, "encode"), (intern!(py, "utf-8"),))?)
}

fn bytes_payload(value: Bound<'_, PyAny>) -> PyResult<Payload<'_>> {
    match value.cast_into::<PyBytes>() {
        Ok(bytes) => Ok(Payload::Bytes(bytes)),
        Err(_) => Err(PyTypeError::new_err("data must be bytes")),
    }
}

/// `repr(obj).encode("utf-8")`, the hook's final branch.
fn repr_payload<'py>(value: &Bound<'py, PyAny>) -> PyResult<Payload<'py>> {
    utf8_payload(value.repr()?.into_any())
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
fn finish_reserved_extension(buf: &mut Vec<u8>, start: usize, code: i8) -> PyResult<()> {
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

/// Next `(key, value)` of an exact dict, as Cython's `for k, v in d.items()`
/// steps `PyDict_Next`.
fn next_dict_item<'py>(
    dict: &Bound<'py, PyDict>,
    position: &mut ffi::Py_ssize_t,
) -> Option<(Bound<'py, PyAny>, Bound<'py, PyAny>)> {
    let mut step = || {
        let mut key = ptr::null_mut();
        let mut value = ptr::null_mut();
        // Safety: `dict` is a live dict; the borrowed results are
        // immediately turned into owned references.
        unsafe {
            (ffi::PyDict_Next(dict.as_ptr(), position, &mut key, &mut value) != 0).then(|| {
                (
                    Bound::from_borrowed_ptr(dict.py(), key),
                    Bound::from_borrowed_ptr(dict.py(), value),
                )
            })
        }
    };
    #[cfg(Py_GIL_DISABLED)]
    {
        pyo3::sync::with_critical_section(dict.as_any(), step)
    }
    #[cfg(not(Py_GIL_DISABLED))]
    {
        step()
    }
}

/// Encoder reproducing `msgpack.Packer(default=msgpack_encode_hook,
/// strict_types=True).pack(value)` byte for byte, including every call into
/// user code (`__repr__`, `__class__`, `isoformat`, ...) in the same order and
/// number, and the same exceptions.
///
/// `pack` mirrors `Packer._pack`: exact builtins are packed directly and
/// everything else goes through `call_default`, a native transcription of
/// `msgpack_encode_hook` (or its lightweight-repr variant). Containers are
/// iterated against their live size exactly as the Cython packer does, so
/// mutations made by a `__repr__` behave identically.
///
/// Large exact str/bytes may additionally be written as value references when
/// interning is enabled; readers expand those before exposing a value.
pub(super) struct NativeMsgpackEncoder<'a> {
    serializer: &'a SerializerState,
    lightweight_repr: bool,
    value_interning: Option<ValueInterningContext<'a>>,
    value_interner_cell: Option<&'a RefCell<ValueInterner>>,
    error: Option<EncodeError>,
    profiler_flag_set: bool,
    used_default_hook: bool,
    extension_depth: i32,
    native_depth: u32,
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
            native_depth: 0,
        }
    }

    pub(super) fn with_value_interning(
        serializer: &'a SerializerState,
        lightweight_repr: bool,
        value_interning: Option<ValueInterningContext<'a>>,
    ) -> Self {
        Self {
            value_interning,
            ..Self::new(serializer, lightweight_repr)
        }
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
        let start = buf.len();
        let packed = self.pack(value, buf, self.serializer.recurse_limit);
        let reset = self.reset_profiler_flag(value.py());
        let result = match packed {
            Ok(()) => reset.map_err(EncodeError::Python),
            Err(Fail) => Err(self
                .error
                .take()
                .expect("a failed encode records its error")),
        };
        if result.is_err() {
            buf.truncate(start);
        }
        result
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
    /// which Kolo's QuerySet `__repr__` patch reads. Set it before the first
    /// call that can run user code; nothing can observe it earlier.
    fn set_profiler_flag(&mut self, py: Python) -> Packed {
        if self.lightweight_repr || self.profiler_flag_set {
            return Ok(());
        }
        let globals = self.serializer.globals.bind(py);
        let result = globals.set_item(intern!(py, "IN_KOLO_PROFILER"), true);
        self.check(result)?;
        self.profiler_flag_set = true;
        Ok(())
    }

    fn reset_profiler_flag(&mut self, py: Python) -> PyResult<()> {
        if !self.profiler_flag_set {
            return Ok(());
        }
        self.profiler_flag_set = false;
        let globals = self.serializer.globals.bind(py);
        globals.set_item(intern!(py, "IN_KOLO_PROFILER"), false)
    }

    /// `Packer._pack`.
    fn pack(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>, nest_limit: i32) -> Packed {
        if nest_limit < 0 {
            return self.fail(PyValueError::new_err("recursion limit exceeded."));
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
                // Outside 64 bits the Packer hands exact ints to `default`.
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
            Err(error) => return self.fail(error),
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
        rmp::encode::write_str(buf, value).expect("Writing to memory, not I/O");
        Ok(())
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

    fn pack_dict(
        &mut self,
        dict: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        self.nested(dict.py(), |encoder| {
            encoder.pack_dict_items(dict, buf, nest_limit)
        })
    }

    fn pack_dict_items(
        &mut self,
        dict: &Bound<'_, PyDict>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let len = dict.len();
        let Some(map_len) = checked_msgpack_len(len) else {
            return self.fail(PyValueError::new_err("dict is too large"));
        };
        rmp::encode::write_map_len(buf, map_len).expect("Writing to memory, not I/O");
        let mut position = 0;
        loop {
            // A `__repr__` may resize the dict being packed.
            if dict.len() != len {
                return self.fail(PyRuntimeError::new_err(
                    "dictionary changed size during iteration",
                ));
            }
            let Some((key, value)) = next_dict_item(dict, &mut position) else {
                return Ok(());
            };
            self.pack(&key, buf, nest_limit)?;
            self.pack(&value, buf, nest_limit)?;
        }
    }

    fn pack_list(
        &mut self,
        list: &Bound<'_, PyList>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        self.nested(list.py(), |encoder| {
            encoder.pack_list_items(list, buf, nest_limit)
        })
    }

    fn pack_list_items(
        &mut self,
        list: &Bound<'_, PyList>,
        buf: &mut Vec<u8>,
        nest_limit: i32,
    ) -> Packed {
        let Some(len) = checked_msgpack_len(list.len()) else {
            return self.fail(PyValueError::new_err("list is too large"));
        };
        rmp::encode::write_array_len(buf, len).expect("Writing to memory, not I/O");
        // Index against the live length like a list iterator: items a
        // `__repr__` appends are packed too, removed ones end the loop.
        let mut index = 0;
        while index < list.len() {
            let item = match list.get_item(index) {
                Ok(item) => item,
                Err(error) => return self.fail(error),
            };
            index += 1;
            self.pack(&item, buf, nest_limit)?;
        }
        Ok(())
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
                // Another thread may resize the bytearray on free-threaded
                // builds; hold its lock across the size read and the copy.
                let copied = pyo3::sync::with_critical_section(value, || {
                    let len = ffi::PyByteArray_Size(object) as usize;
                    let bin_len = checked_msgpack_len(len)?;
                    rmp::encode::write_bin_len(buf, bin_len).expect("Writing to memory, not I/O");
                    let data = ffi::PyByteArray_AsString(object) as *const u8;
                    buf.extend_from_slice(std::slice::from_raw_parts(data, len));
                    Some(())
                });
                return match copied {
                    Some(()) => Ok(()),
                    None => self.fail(PyValueError::new_err("bytearray object is too large")),
                };
            }
            let object_type = ffi::Py_TYPE(object) as *mut ffi::PyObject;
            if object_type == self.serializer.ext_type.as_ptr()
                || object_type == self.serializer.timestamp_type.as_ptr()
                || ffi::PyMemoryView_Check(object) != 0
            {
                // msgpack's own packer is exact for these. Only a bytes
                // subclass's `__len__` in an ExtType can run user code there.
                let py = value.py();
                self.set_profiler_flag(py)?;
                let kwargs = PyDict::new(py);
                let packed = kwargs
                    .set_item(intern!(py, "strict_types"), true)
                    .and_then(|()| self.serializer.packb.bind(py).call((value,), Some(&kwargs)))
                    .and_then(|packed| packed.cast_into::<PyBytes>().map_err(Into::into));
                let packed = self.check(packed)?;
                buf.extend_from_slice(packed.as_bytes());
                return Ok(());
            }
        }
        self.write_unsupported_leaf(value, buf, nest_limit)
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
                buf.truncate(start);
                return self.handle_default_error(value, buf);
            }
        };
        let packed = match defaulted {
            Defaulted::Ext(code, payload) => payload
                .packed_len()
                .and_then(|len| write_ext(buf, code, &payload.as_bytes()[..len])),
            Defaulted::Sequence(code, start) => finish_reserved_extension(buf, start, code),
            Defaulted::Dict(dict) => return self.pack_dict(&dict, buf, nest_limit),
        };
        self.check(packed)
    }

    /// `msgpack_encode_hook`'s `except Exception:` handler.
    #[cold]
    #[inline(never)]
    fn handle_default_error(&mut self, value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) -> Packed {
        let py = value.py();
        let caught = match &self.error {
            Some(EncodeError::Python(error)) => {
                !self.lightweight_repr && error.is_instance_of::<PyException>(py)
            }
            _ => false,
        };
        if !caught {
            return Err(Fail);
        }
        let Some(EncodeError::Python(error)) = self.error.take() else {
            unreachable!("caught errors are Python exceptions");
        };
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
        let payload = (|| {
            let module = format_field(&value.getattr(intern!(py, "__module__"))?)?;
            let qualname = format_field(&value.get_type().getattr(intern!(py, "__qualname__"))?)?;
            utf8_payload(concat_text(&[&module, &PyString::new(py, "."), &qualname])?)
        })();
        // Safety: restores the references taken above.
        unsafe { ffi::PyErr_SetExcInfo(saved_type, saved_value, saved_traceback) };
        match payload {
            Ok(payload) => {
                let written = payload.packed_len().and_then(|len| {
                    write_ext(
                        buf,
                        SERIALIZATION_ERROR_EXTENSION_TYPE,
                        &payload.as_bytes()[..len],
                    )
                });
                self.check(written)
            }
            Err(new_error) => {
                // CPython already chained errors raised by Python code;
                // errors created here in Rust still need the context.
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
            // Exact tuples are the one hook type common enough to skip the
            // ladder for; `isinstance(obj, tuple)` matches them first anyway.
            let start = self.reserve_extension_header(buf);
            self.pack_extension_items(SequenceItems::Tuple(tuple), buf)?;
            return Ok(Defaulted::Sequence(PY_TUPLE_EXTENSION_TYPE, start));
        }
        self.used_default_hook = true;
        self.set_profiler_flag(py)?;

        let mut class_is_type = None;
        let (tuple_type, set_type, frozenset_type, dict_type) = (
            ptr::addr_of_mut!(ffi::PyTuple_Type).cast::<ffi::PyObject>(),
            ptr::addr_of_mut!(ffi::PySet_Type).cast::<ffi::PyObject>(),
            ptr::addr_of_mut!(ffi::PyFrozenSet_Type).cast::<ffi::PyObject>(),
            ptr::addr_of_mut!(ffi::PyDict_Type).cast::<ffi::PyObject>(),
        );
        for (sequence_type, code) in [
            (tuple_type, PY_TUPLE_EXTENSION_TYPE),
            (set_type, PY_SET_EXTENSION_TYPE),
            (frozenset_type, PY_FROZENSET_EXTENSION_TYPE),
        ] {
            let matched = self.isinstance(value, sequence_type, &mut class_is_type);
            if self.check(matched)? {
                let items = self.call_builtin(value, ptr::addr_of_mut!(ffi::PyList_Type).cast());
                let items = self.check(items)?;
                let items = items.cast_into::<PyList>().expect("list() returns a list");
                let start = self.reserve_extension_header(buf);
                self.pack_extension_items(SequenceItems::List(&items), buf)?;
                return Ok(Defaulted::Sequence(code, start));
            }
        }
        let matched = self.isinstance(value, dict_type, &mut class_is_type);
        if self.check(matched)? {
            let copy = self.call_builtin(value, dict_type);
            let copy = self.check(copy)?;
            return Ok(Defaulted::Dict(
                copy.cast_into::<PyDict>().expect("dict() returns a dict"),
            ));
        }
        let payload = self.default_leaf_payload(value, &mut class_is_type);
        self.check(payload)
    }

    /// The hook's remaining branches, each producing an ExtType.
    #[inline(never)]
    fn default_leaf_payload<'py>(
        &self,
        value: &Bound<'py, PyAny>,
        class_is_type: &mut Option<bool>,
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
            let class = value.getattr(intern!(py, "__class__"))?;
            let qualname = class.getattr(intern!(py, "__qualname__"))?;
            let text = concat_text(&[
                &PyString::new(py, "<"),
                &format_field(&qualname)?,
                &PyString::new(py, &format!(" object {}>", value.as_ptr() as usize)),
            ])?;
            return Ok(Defaulted::Ext(0, utf8_payload(text)?));
        }

        let (queryset, imported) = self.queryset_class(py)?;
        if imported {
            // `_get_queryset_class` may have just imported Django.
            *class_is_type = None;
        }
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
        Ok(Defaulted::Ext(0, repr_payload(value)?))
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
    /// Returns whether the Python function had to run.
    fn queryset_class<'py>(&self, py: Python<'py>) -> PyResult<(Bound<'py, PyAny>, bool)> {
        if self.global(intern!(py, "_QuerySet_checked"))?.is_truthy()? {
            return Ok((self.global(intern!(py, "_QuerySet"))?, false));
        }
        Ok((
            self.global(intern!(py, "_get_queryset_class"))?.call0()?,
            true,
        ))
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

    fn reserve_extension_header(&self, buf: &mut Vec<u8>) -> usize {
        let start = buf.len();
        buf.resize(start + MAX_EXT_HEADER_LEN, 0);
        start
    }

    /// `_dump_msgpack(list(obj))`: a fresh Packer, so a fresh recursion
    /// limit, packing the copied items. Python spends stack frames on each
    /// such nesting; a cycle through tuples ends in RecursionError there,
    /// which the hook then reports as a serialization error.
    fn pack_extension_items(&mut self, items: SequenceItems<'_, '_>, buf: &mut Vec<u8>) -> Packed {
        // Safety: reads the interpreter's recursion limit, which is never
        // below 64 frames in practice.
        if self.extension_depth >= 16
            && self.extension_depth
                >= unsafe { ffi::Py_GetRecursionLimit() } / PYTHON_FRAMES_PER_NESTED_EXTENSION
        {
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
                // The list copy would be packed at `limit`, its items one
                // level below.
                tuple
                    .iter()
                    .try_for_each(|item| encoder.pack(&item, buf, limit - 1))
            }),
        };
        self.extension_depth -= 1;
        packed
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
                        // A capture that cannot publish one value will never
                        // accept later references reliably. Disable interning
                        // once instead of re-locking and rolling back the
                        // process-wide table on every subsequent callback.
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

#[cfg(test)]
#[path = "tests.rs"]
mod tests;
