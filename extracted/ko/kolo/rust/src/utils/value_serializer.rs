use hashbrown::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{
    PyAny, PyBool, PyBytes, PyDict, PyFloat, PyInt, PyList, PyModule, PyString, PyTuple,
};
use std::cell::RefCell;
use std::io::{self, Cursor};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use thread_local::ThreadLocal;

use super::super::trace_container::TraceCapture;

pub struct Serializer {
    dump_msgpack: Py<PyAny>,
    dump_msgpack_lightweight_repr: Py<PyAny>,
}

impl Serializer {
    pub fn new(py: Python) -> Result<Self, PyErr> {
        let serialize = PyModule::import(py, "kolo.serialize")?;
        Ok(Self {
            dump_msgpack: serialize.getattr(intern!(py, "dump_msgpack"))?.unbind(),
            dump_msgpack_lightweight_repr: serialize
                .getattr(intern!(py, "dump_msgpack_lightweight_repr"))?
                .unbind(),
        })
    }

    pub fn dump_msgpack<'py>(
        &self,
        py: Python<'py>,
        data: &Bound<'py, PyAny>,
        lightweight_repr: bool,
    ) -> Result<Vec<u8>, PyErr> {
        Ok(self
            .dump_msgpack_bytes(py, data, lightweight_repr)?
            .as_bytes()
            .to_vec())
    }

    pub(super) fn dump_msgpack_bytes<'py>(
        &self,
        py: Python<'py>,
        data: &Bound<'py, PyAny>,
        lightweight_repr: bool,
    ) -> Result<Bound<'py, PyBytes>, PyErr> {
        let serializer = match lightweight_repr {
            false => self.dump_msgpack.bind(py),
            true => self.dump_msgpack_lightweight_repr.bind(py),
        };
        // Both kolo.serialize entry points contractually return bytes.
        Ok(serializer.call1((data,))?.cast_into::<PyBytes>()?)
    }

    pub(super) fn dump_msgpack_into(
        &self,
        py: Python,
        data: &Bound<'_, PyAny>,
        lightweight_repr: bool,
        buf: &mut Vec<u8>,
    ) -> Result<(), PyErr> {
        let serialized = self.dump_msgpack_bytes(py, data, lightweight_repr)?;
        buf.extend_from_slice(serialized.as_bytes());
        Ok(())
    }
}

const MAX_NATIVE_MSGPACK_DEPTH: usize = 64;

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

const INLINE_ACTIVE_CONTAINERS: usize = 8;

#[derive(Default)]
struct ActiveContainers {
    inline: [usize; INLINE_ACTIVE_CONTAINERS],
    inline_len: usize,
    overflow: Vec<usize>,
}

impl ActiveContainers {
    #[cfg(test)]
    fn is_empty(&self) -> bool {
        self.inline_len == 0 && self.overflow.is_empty()
    }

    fn contains(&self, identity: usize) -> bool {
        self.inline[..self.inline_len].contains(&identity) || self.overflow.contains(&identity)
    }

    fn push(&mut self, identity: usize) {
        debug_assert!(self.overflow.is_empty() || self.inline_len == INLINE_ACTIVE_CONTAINERS);
        if self.inline_len < INLINE_ACTIVE_CONTAINERS {
            self.inline[self.inline_len] = identity;
            self.inline_len += 1;
        } else {
            self.overflow.push(identity);
        }
    }

    fn pop(&mut self) {
        debug_assert!(self.overflow.is_empty() || self.inline_len == INLINE_ACTIVE_CONTAINERS);
        if self.overflow.pop().is_none() {
            self.inline_len = self.inline_len.saturating_sub(1);
        }
    }
}

/// Encoder for the exact builtin types handled directly by msgpack with
/// `strict_types=True`. Unsupported data aborts the whole native root; callers
/// must discard the scratch buffer and serialize the complete root in Python.
pub(super) struct NativeMsgpackEncoder<'a> {
    active_containers: ActiveContainers,
    value_interning: Option<ValueInterningContext<'a>>,
    value_interner_cell: Option<&'a RefCell<ValueInterner>>,
    pub(super) writer_circuit_error: Option<String>,
}

impl<'a> NativeMsgpackEncoder<'a> {
    pub(super) fn new() -> Self {
        Self {
            active_containers: ActiveContainers::default(),
            value_interning: None,
            value_interner_cell: None,
            writer_circuit_error: None,
        }
    }

    pub(super) fn with_value_interning(value_interning: ValueInterningContext<'a>) -> Self {
        NativeMsgpackEncoder {
            active_containers: ActiveContainers::default(),
            value_interning: Some(value_interning),
            value_interner_cell: None,
            writer_circuit_error: None,
        }
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

    pub(super) fn write(
        &mut self,
        value: &Bound<'_, PyAny>,
        buf: &mut Vec<u8>,
        depth: usize,
    ) -> bool {
        if depth > MAX_NATIVE_MSGPACK_DEPTH {
            return false;
        }

        if value.is_none() {
            rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
            return true;
        }
        if value.is_exact_instance_of::<PyBool>() {
            let value = value
                .extract::<bool>()
                .expect("an exact bool extracts as bool");
            rmp::encode::write_bool(buf, value).expect("Writing to memory, not I/O");
            return true;
        }
        if value.is_exact_instance_of::<PyInt>() {
            if let Ok(value) = value.extract::<i64>() {
                rmp::encode::write_sint(buf, value).expect("Writing to memory, not I/O");
                return true;
            }
            if let Ok(value) = value.extract::<u64>() {
                rmp::encode::write_uint(buf, value).expect("Writing to memory, not I/O");
                return true;
            }
            return false;
        }
        if value.is_exact_instance_of::<PyFloat>() {
            let value = value
                .extract::<f64>()
                .expect("an exact float extracts as f64");
            rmp::encode::write_f64(buf, value).expect("Writing to memory, not I/O");
            return true;
        }
        if value.is_exact_instance_of::<PyString>() {
            let py_string = value
                .cast::<PyString>()
                .expect("exact string type already checked");
            let Ok(value) = py_string.to_str() else {
                return false;
            };
            if u32::try_from(value.as_bytes().len()).is_err() {
                return false;
            }
            if self.value_interning.is_some()
                && !self
                    .value_interning
                    .is_some_and(|context| context.interning.disabled.load(Ordering::Relaxed))
                && (MIN_INTERNED_VALUE_BYTES..=MAX_INTERNED_VALUE_BYTES).contains(&value.len())
            {
                let identity = py_string.as_ptr() as usize;
                match self.lookup_value(identity, InternedValueKind::String, value.as_bytes(), buf)
                {
                    ValueLookup::ReferenceWritten => return true,
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
                        return true;
                    }
                    ValueLookup::WriterCircuit(error) => {
                        self.writer_circuit_error = Some(error);
                        return false;
                    }
                }
            }
            rmp::encode::write_str(buf, value).expect("Writing to memory, not I/O");
            return true;
        }
        if value.is_exact_instance_of::<PyBytes>() {
            let value = value
                .cast::<PyBytes>()
                .expect("exact bytes type already checked");
            if u32::try_from(value.as_bytes().len()).is_err() {
                return false;
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
                    ValueLookup::ReferenceWritten => return true,
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
                        return true;
                    }
                    ValueLookup::WriterCircuit(error) => {
                        self.writer_circuit_error = Some(error);
                        return false;
                    }
                }
            }
            rmp::encode::write_bin(buf, value.as_bytes()).expect("Writing to memory, not I/O");
            return true;
        }
        if value.is_exact_instance_of::<PyList>() {
            let value = value
                .cast::<PyList>()
                .expect("exact list type already checked");
            let Ok(len) = value.len().try_into() else {
                return false;
            };
            let identity = value.as_ptr() as usize;
            if self.active_containers.contains(identity) {
                return false;
            }
            self.active_containers.push(identity);
            let mut complete = true;
            rmp::encode::write_array_len(buf, len).expect("Writing to memory, not I/O");
            for item in value.iter() {
                if !self.write(&item, buf, depth + 1) {
                    complete = false;
                    break;
                }
            }
            self.active_containers.pop();
            return complete;
        }
        if value.is_exact_instance_of::<PyDict>() {
            let value = value
                .cast::<PyDict>()
                .expect("exact dict type already checked");
            let Ok(len) = value.len().try_into() else {
                return false;
            };
            let identity = value.as_ptr() as usize;
            if self.active_containers.contains(identity) {
                return false;
            }
            self.active_containers.push(identity);
            let mut complete = true;
            rmp::encode::write_map_len(buf, len).expect("Writing to memory, not I/O");
            for (key, item) in value.iter() {
                if !self.write(&key, buf, depth + 1) || !self.write(&item, buf, depth + 1) {
                    complete = false;
                    break;
                }
            }
            self.active_containers.pop();
            return complete;
        }
        // Tuples are less common than the list/dict containers above. Keep
        // this new exact-type probe off their established hot path.
        if value.is_exact_instance_of::<PyTuple>() {
            let value = value
                .cast::<PyTuple>()
                .expect("exact tuple type already checked");
            return self.write_tuple(value, buf, depth).is_some();
        }

        false
    }

    // Keep the uncommon tuple encoder out of this serializer's capture-hot
    // instruction body; inlining it measurably regresses tuple-free traces.
    #[cold]
    #[inline(never)]
    fn write_tuple(
        &mut self,
        value: &Bound<'_, PyTuple>,
        buf: &mut Vec<u8>,
        depth: usize,
    ) -> Option<()> {
        self.write_tuple_with_len(value, buf, depth, value.len())
    }

    fn write_tuple_with_len(
        &mut self,
        value: &Bound<'_, PyTuple>,
        buf: &mut Vec<u8>,
        depth: usize,
        tuple_len: usize,
    ) -> Option<()> {
        let len = checked_msgpack_len(tuple_len)?;
        let identity = value.as_ptr() as usize;
        if self.active_containers.contains(identity) {
            return None;
        }
        const MAX_EXT_HEADER_LEN: usize = 6;
        let tuple_start = buf.len();
        self.active_containers.push(identity);
        buf.resize(tuple_start + MAX_EXT_HEADER_LEN, 0);
        let inner_start = buf.len();
        rmp::encode::write_array_len(buf, len).expect("Writing to memory, not I/O");
        let mut complete = true;
        for item in value.iter() {
            if !self.write(&item, buf, depth + 1) {
                complete = false;
                break;
            }
        }
        self.active_containers.pop();
        if !complete {
            buf.truncate(tuple_start);
            return None;
        }
        let encoded_len = buf.len() - inner_start;
        let Some(inner_len) = checked_msgpack_len(encoded_len) else {
            buf.truncate(tuple_start);
            return None;
        };

        let mut header = [0; MAX_EXT_HEADER_LEN];
        let mut cursor = Cursor::new(&mut header[..]);
        rmp::encode::write_ext_meta(&mut cursor, inner_len, 6)
            .expect("fixed-size extension header always fits");
        let header_len = cursor.position() as usize;
        debug_assert!(header_len <= MAX_EXT_HEADER_LEN);
        let end = buf.len();
        if header_len < MAX_EXT_HEADER_LEN {
            buf.copy_within(inner_start..end, tuple_start + header_len);
            buf.truncate(end - (MAX_EXT_HEADER_LEN - header_len));
        }
        buf[tuple_start..tuple_start + header_len].copy_from_slice(&header[..header_len]);
        Some(())
    }

    #[cfg(test)]
    fn append_tuple_extension(
        buf: &mut Vec<u8>,
        inner: &mut Vec<u8>,
        encoded_len: usize,
    ) -> Option<()> {
        const PY_TUPLE_EXTENSION_TYPE: i8 = 6;

        let inner_len = checked_msgpack_len(encoded_len)?;
        rmp::encode::write_ext_meta(buf, inner_len, PY_TUPLE_EXTENSION_TYPE)
            .expect("Writing to memory, not I/O");
        buf.append(inner);
        Some(())
    }
}

#[cfg(test)]
#[path = "tests.rs"]
mod tests;
