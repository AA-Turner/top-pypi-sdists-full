use super::*;
use crate::_kolo::config;
use crate::_kolo::utils::frame_path::*;
use crate::_kolo::utils::frame_types::*;
use crate::_kolo::utils::frame_writer::*;
use crate::_kolo::utils::msgpack_encoding::*;
use crate::_kolo::utils::trace_persistence::*;
use pyo3::sync::MutexExt;
use pyo3::types::PyFrame;
use std::env::current_dir;
use std::ffi::CString;
use std::path::{Path, PathBuf};

#[test]
fn module_name_uses_dict_fast_path_and_preserves_mapping_fallback() {
    Python::initialize();
    Python::attach(|py| {
        let globals = PyDict::new(py);
        globals
            .set_item("__name__", "dict_module")
            .expect("dict module name is valid");
        assert_eq!(
            module_name_from_globals(globals.as_any(), py)
                .extract::<String>()
                .expect("module name is text"),
            "dict_module"
        );

        globals
            .del_item("__name__")
            .expect("dict module name is removable");
        assert_eq!(
            module_name_from_globals(globals.as_any(), py)
                .extract::<String>()
                .expect("fallback module name is text"),
            "<unknown>"
        );

        let module = PyModule::from_code(
            py,
            c"class GlobalsMapping:\n    def __init__(self, fail=False): self.fail = fail\n    def __getitem__(self, key):\n        if self.fail: raise RuntimeError('mapping failed')\n        assert key == '__name__'\n        return 'mapping_module'\nclass DictGlobals(dict):\n    def __getitem__(self, key):\n        assert key == '__name__'\n        return 'dict_subclass_module'\n",
            c"globals_mapping.py",
            c"globals_mapping",
        )
        .expect("mapping fixture compiles");
        let mapping_type = module
            .getattr("GlobalsMapping")
            .expect("mapping class exists");
        let mapping = mapping_type.call0().expect("mapping constructs");
        assert_eq!(
            module_name_from_globals(&mapping, py)
                .extract::<String>()
                .expect("mapping module name is text"),
            "mapping_module"
        );

        let dict_subclass = module
            .getattr("DictGlobals")
            .expect("dict subclass exists")
            .call0()
            .expect("dict subclass constructs");
        assert_eq!(
            module_name_from_globals(&dict_subclass, py)
                .extract::<String>()
                .expect("dict subclass module name is text"),
            "dict_subclass_module"
        );

        let failing_mapping = mapping_type
            .call1((true,))
            .expect("failing mapping constructs");
        assert_eq!(
            module_name_from_globals(&failing_mapping, py)
                .extract::<String>()
                .expect("mapping fallback module name is text"),
            "<unknown>"
        );
    });
}

#[test]
fn v3_thread_metadata_tolerates_missing_ids_and_propagates_required_field_errors() {
    Python::initialize();
    Python::attach(|py| {
        let module = PyModule::from_code(
                py,
                c"class Thread:\n    def __init__(self, fail=None): self.fail = fail\n    def __getattribute__(self, name):\n        fail = object.__getattribute__(self, 'fail')\n        if name == fail:\n            raise RuntimeError(f'cannot read {name}')\n        if name != 'is_alive' and fail == f'{name}_value':\n            return object()\n        return object.__getattribute__(self, name)\n    name = 'worker'\n    daemon = False\n    def is_alive(self):\n        if self.fail == 'is_alive_value': return object()\n        return True\n",
                c"streaming_thread_header.py",
                c"streaming_thread_header",
            )
            .expect("thread fixture compiles");
        let thread_type = module.getattr("Thread").expect("Thread is defined");
        let thread = thread_type
            .call0()
            .expect("default thread constructs")
            .unbind();
        let prepare = |thread| {
            let mut threads = HashMap::new();
            threads.insert("thread".to_string(), thread);
            let thread_tokens = HashMap::from([("thread".to_string(), 1)]);
            let config = config::Config::new(&PyDict::new(py)).expect("empty config is valid");
            prepare_v3_trace_from_parts(
                py,
                &threads,
                &thread_tokens,
                "trc_thread_metadata",
                None,
                "test",
                "thread".to_string(),
                1.0,
                &config,
                true,
                None,
            )
        };
        let prepared = prepare(thread).expect("missing optional ids are encoded as nil");
        let metadata = rmpv::decode::read_value(&mut &prepared.thread_meta[0].1[..])
            .expect("metadata decodes");
        let metadata = metadata.as_map().expect("thread metadata is a map");
        for optional_id in ["ident", "native_id"] {
            let value = metadata
                .iter()
                .find(|(key, _)| key.as_str() == Some(optional_id))
                .map(|(_, value)| value)
                .expect("optional id is present");
            assert!(value.is_nil());
        }

        for required_field in [
            "name",
            "name_value",
            "daemon",
            "daemon_value",
            "is_alive",
            "is_alive_value",
        ] {
            let broken = thread_type
                .call1((required_field,))
                .expect("broken thread constructs")
                .unbind();
            assert!(
                prepare(broken).is_err(),
                "required thread metadata failures must propagate"
            );
        }
    });
}

#[test]
fn test_checked_msgpack_len_boundaries() {
    assert_eq!(checked_msgpack_len(0), Some(0));
    assert_eq!(checked_msgpack_len(u32::MAX as usize), Some(u32::MAX));
    #[cfg(target_pointer_width = "64")]
    assert_eq!(checked_msgpack_len(u32::MAX as usize + 1), None);
}

fn assert_native_matches_python(
    py: Python<'_>,
    serializer: &Serializer,
    value: &Bound<'_, PyAny>,
    lightweight_repr: bool,
    label: &str,
) {
    let native = serializer.dump_msgpack(py, value, lightweight_repr);
    let python = serializer.python_dump_msgpack(py, value, lightweight_repr);
    match (native, python) {
        (Ok(native), Ok(python)) => assert_eq!(native, python, "bytes differ for {label}"),
        (Err(native), Err(python)) => {
            assert!(
                native.get_type(py).is(python.get_type(py)),
                "error types differ for {label}: {native} vs {python}"
            );
            // RecursionError wording varies across Python versions.
            if !native.is_instance_of::<pyo3::exceptions::PyRecursionError>(py) {
                assert_eq!(native.to_string(), python.to_string(), "{label}");
            }
        }
        (native, python) => {
            panic!("native and Python disagree for {label}: {native:?} vs {python:?}")
        }
    }
}

#[test]
fn test_native_msgpack_exact_builtin_zoo_matches_python_serializer() {
    Python::initialize();

    Python::attach(|py| {
        let module = PyModule::from_code(
                py,
                c"value = {\n    'none': None,\n    'bools': [False, True],\n    'ints': [-(1 << 63), -33, -1, 0, 127, 128, (1 << 63) - 1, (1 << 64) - 1],\n    'floats': [1.25, -0.0, float('inf'), float('-inf'), float('nan')],\n    'text': 'snowman \\N{SNOWMAN}',\n    'bytes': b'bytes\\x00',\n    'nested': {'list': [1, {'answer': 42}], 'tuple': (1, 'two', (3,))},\n    'mixed_keys': {1: 'int', 1.5: 'float', b'b': 'bytes', ('tuple',): 'tuple'},\n}\n",
                c"native_msgpack_zoo.py",
                c"native_msgpack_zoo",
            )
            .expect("zoo module compiles");
        let value = module.getattr("value").expect("zoo exposes value");
        let serializer = Serializer::new(py).expect("serializer loads");

        let mut native = Vec::new();
        let mut encoder = NativeMsgpackEncoder::new(&serializer, false);
        assert!(encoder.encode(&value, &mut native).is_ok());
        assert!(!encoder.used_default_hook());

        let python = serializer
            .python_dump_msgpack(py, &value, false)
            .expect("Python serializer handles exact builtins");
        assert_eq!(native, python);
    });
}

#[test]
fn serializer_appends_mixed_values_byte_exactly_in_both_repr_modes() {
    Python::initialize();

    Python::attach(|py| {
        let serializer = Serializer::new(py).expect("serializer loads");
        let module = PyModule::from_code(
            py,
            c"class Custom:\n    def __repr__(self): return 'custom-value'\nexact = {'nested': [None, True, 42, 'text', b'bytes']}\nmixed = {'prefix': [1, 2], 'custom': Custom()}\n",
            c"native_mixed_values.py",
            c"native_mixed_values",
        )
        .expect("mixed-value fixtures compile");
        let sentinel = b"existing-bytes";

        for name in ["exact", "mixed"] {
            let value = module.getattr(name).expect("fixture exists");
            for lightweight_repr in [false, true] {
                let expected = serializer
                    .python_dump_msgpack(py, &value, lightweight_repr)
                    .expect("Python serializer handles fixture");
                let mut encoded = sentinel.to_vec();
                serializer
                    .dump_msgpack_into(py, &value, lightweight_repr, &mut encoded)
                    .expect("native encoding succeeds");
                assert_eq!(&encoded[..sentinel.len()], sentinel);
                assert_eq!(&encoded[sentinel.len()..], expected);
            }
        }
    });
}

#[test]
fn value_interner_uses_strong_exact_object_identity_not_equal_content() {
    Python::initialize();
    let destination = std::env::temp_dir().join(format!(
        "kolo-value-identity-reuse-{}-{}.kolo",
        std::process::id(),
        trace_id()
    ));
    let capture = TraceCapture::start(destination, b"\x80".to_vec());
    let interning = ValueInterning::default();
    let serializer = Python::attach(|py| Serializer::new(py).expect("serializer loads"));
    let mut encoder = NativeMsgpackEncoder::with_value_interning(
        &serializer,
        false,
        Some(ValueInterningContext::fixed(&interning, &capture)),
    );
    let payload = vec![b'a'; MIN_INTERNED_VALUE_BYTES];
    let (first, equal_but_distinct) = Python::attach(|py| {
        (
            PyBytes::new(py, &payload).clone().into_any().unbind(),
            PyBytes::new(py, &payload).clone().into_any().unbind(),
        )
    });
    assert_ne!(first.as_ptr(), equal_but_distinct.as_ptr());
    let identity = first.as_ptr() as usize;
    let mut output = Vec::new();

    assert_eq!(
        encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
        ValueLookup::WriteInline
    );
    assert_eq!(
        encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
        ValueLookup::CacheCurrent
    );
    let mut encoded = Vec::new();
    rmp::encode::write_bin(&mut encoded, &payload).unwrap();
    encoder.cache_current_value(
        identity,
        InternedValueKind::Bytes,
        payload.len(),
        first,
        encoded,
        &mut output,
    );
    let reference_start = output.len();
    assert_eq!(
        encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
        ValueLookup::ReferenceWritten
    );
    assert_eq!(&output[reference_start..], b"\xd6\x09\0\0\0\0");
    assert_eq!(interning.snapshot_all().len(), 1);

    // Equal bytes in a different exact object are not aliased. The table
    // retains `first`, so its pointer cannot be recycled while this entry
    // exists and no probabilistic/content-only identity is involved.
    assert_eq!(
        encoder.lookup_value(
            equal_but_distinct.as_ptr() as usize,
            InternedValueKind::Bytes,
            &payload,
            &mut output
        ),
        ValueLookup::WriteInline
    );
}

#[test]
fn value_interning_limits_fail_closed_without_growing_state() {
    Python::initialize();
    let object = Python::attach(|py| PyBytes::new(py, b"x").clone().into_any().unbind());
    let value = Arc::new(InternedValue {
        encoded: Arc::from(&b"x"[..]),
        payload_start: 0,
        kind: InternedValueKind::Bytes,
        object,
    });
    let mut entry_limited = ValueTable {
        entries: vec![Arc::clone(&value); MAX_INTERNED_VALUES],
        resident_bytes: MAX_INTERNED_VALUES,
    };
    assert!(entry_limited.insert_value(Arc::clone(&value)).is_none());
    assert_eq!(entry_limited.entries.len(), MAX_INTERNED_VALUES);

    let mut byte_limited = ValueTable {
        entries: Vec::new(),
        resident_bytes: MAX_VALUE_TABLE_BYTES,
    };
    assert!(byte_limited.insert_value(Arc::clone(&value)).is_none());
    assert!(byte_limited.entries.is_empty());

    let mut table = ValueTable::default();
    assert_eq!(table.insert_value(Arc::clone(&value)), Some(0));
    assert_eq!(table.snapshot_ids(&[0, 99]).len(), 1);
    assert_eq!(table.resident_bytes, value.resident_len());
    table.remove_last(0);
    assert!(table.entries.is_empty());
    assert_eq!(table.resident_bytes, 0);

    let mut interner = ValueInterner::default();
    let global = AtomicUsize::new(0);
    assert!(!interner.make_candidate_room(1, MAX_VALUE_CANDIDATE_BYTES + 1, &global));
    assert_eq!(interner.candidate_bytes, 0);
    assert_eq!(global.load(Ordering::Relaxed), 0);

    interner
        .values
        .insert(1, CachedValue::Candidate(Arc::clone(&value)));
    interner.candidate_bytes = value.resident_len();
    global.store(value.resident_len(), Ordering::Relaxed);
    interner.remove(1, &global);
    assert!(interner.values.is_empty());
    assert_eq!(interner.candidate_bytes, 0);
    assert_eq!(global.load(Ordering::Relaxed), 0);

    for identity in 0..MAX_TRACKED_VALUE_IDENTITIES {
        interner.values.insert(
            identity,
            CachedValue::Seen(ValueSignature::new(InternedValueKind::Bytes, b"x")),
        );
    }
    interner.make_identity_room(MAX_TRACKED_VALUE_IDENTITIES, &global);
    assert_eq!(interner.values.len(), MAX_TRACKED_VALUE_IDENTITIES - 1);
}

#[test]
fn value_interner_rolls_back_promotion_when_capture_is_closed() {
    Python::initialize();
    let destination = std::env::temp_dir().join(format!(
        "kolo-value-closed-capture-{}-{}.kolo",
        std::process::id(),
        trace_id()
    ));
    let capture = TraceCapture::start(destination.clone(), b"\x80".to_vec());
    capture
        .finish(Vec::new(), b"\x80".to_vec(), Vec::new())
        .unwrap();
    let interning = ValueInterning::default();
    let payload = vec![b'x'; MIN_INTERNED_VALUE_BYTES];
    let object = Python::attach(|py| PyBytes::new(py, &payload).clone().into_any().unbind());
    let identity = object.as_ptr() as usize;
    let serializer = Python::attach(|py| Serializer::new(py).expect("serializer loads"));
    let mut encoder = NativeMsgpackEncoder::with_value_interning(
        &serializer,
        false,
        Some(ValueInterningContext::fixed(&interning, &capture)),
    );
    let mut output = Vec::new();

    assert_eq!(
        encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
        ValueLookup::WriteInline
    );
    assert_eq!(
        encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
        ValueLookup::CacheCurrent
    );
    let mut encoded = Vec::new();
    rmp::encode::write_bin(&mut encoded, &payload).unwrap();
    encoder.cache_current_value(
        identity,
        InternedValueKind::Bytes,
        payload.len(),
        object,
        encoded,
        &mut output,
    );
    let before = output.len();
    assert_eq!(
        encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
        ValueLookup::WriteInline
    );
    assert_eq!(output.len(), before);
    assert!(interning.disabled.load(Ordering::Relaxed));
    assert!(interning.snapshot_all().is_empty());
    assert!(capture.published_value_ids().is_empty());
    std::fs::remove_file(destination).unwrap();
}

#[test]
fn value_interner_surfaces_writer_circuit_during_native_encoding() {
    Python::initialize();
    let destination = std::env::temp_dir().join(format!(
        "kolo-value-writer-circuit-{}-{}.kolo",
        std::process::id(),
        trace_id()
    ));
    let capture = TraceCapture::start_with_open_test_circuit(destination, b"\x80".to_vec());
    let interning = ValueInterning::default();
    let payload = vec![b'x'; MIN_INTERNED_VALUE_BYTES];
    let object = Python::attach(|py| PyBytes::new(py, &payload).clone().into_any().unbind());
    let serializer = Python::attach(|py| Serializer::new(py).expect("serializer loads"));
    let mut encoder = NativeMsgpackEncoder::with_value_interning(
        &serializer,
        false,
        Some(ValueInterningContext::fixed(&interning, &capture)),
    );
    let mut output = Vec::new();

    let error = Python::attach(|py| {
        assert!(encoder.encode(object.bind(py), &mut output).is_ok());
        assert!(encoder.encode(object.bind(py), &mut output).is_ok());
        let before = output.len();
        let error = encoder.encode(object.bind(py), &mut output).err();
        assert_eq!(output.len(), before);
        error
    });

    assert!(matches!(
        error,
        Some(EncodeError::WriterCircuit(error)) if error.contains("writer circuit breaker opened")
    ));
    assert!(interning.disabled.load(Ordering::Relaxed));
    assert!(interning.snapshot_all().is_empty());
    assert!(capture.published_value_ids().is_empty());
}

#[test]
fn value_interning_promotes_concurrently_without_cross_thread_aliases() {
    Python::initialize();
    let destination = std::env::temp_dir().join(format!(
        "kolo-value-concurrency-{}-{}.kolo",
        std::process::id(),
        trace_id()
    ));
    let capture = TraceCapture::start(destination, b"\x80".to_vec());
    let interning = Arc::new(ValueInterning::default());
    let serializer = Arc::new(Python::attach(|py| {
        Serializer::new(py).expect("serializer loads")
    }));
    let start = Arc::new(std::sync::Barrier::new(4));
    let values = Python::attach(|py| {
        (0..4)
            .map(|worker| {
                let payload = vec![b'a' + worker; MIN_INTERNED_VALUE_BYTES];
                (
                    payload.clone(),
                    PyBytes::new(py, &payload).clone().into_any().unbind(),
                )
            })
            .collect::<Vec<_>>()
    });
    let workers = values
        .into_iter()
        .map(|(payload, object)| {
            let capture = Arc::clone(&capture);
            let interning = Arc::clone(&interning);
            let serializer = Arc::clone(&serializer);
            let start = Arc::clone(&start);
            std::thread::spawn(move || {
                let identity = object.as_ptr() as usize;
                let mut output = Vec::new();
                let mut encoder = NativeMsgpackEncoder::with_value_interning(
                    &serializer,
                    false,
                    Some(ValueInterningContext::fixed(&interning, &capture)),
                );
                start.wait();
                assert_eq!(
                    encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
                    ValueLookup::WriteInline
                );
                assert_eq!(
                    encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
                    ValueLookup::CacheCurrent
                );
                let mut encoded = Vec::new();
                rmp::encode::write_bin(&mut encoded, &payload).unwrap();
                encoder.cache_current_value(
                    identity,
                    InternedValueKind::Bytes,
                    payload.len(),
                    object,
                    encoded,
                    &mut output,
                );
                assert_eq!(
                    encoder.lookup_value(identity, InternedValueKind::Bytes, &payload, &mut output),
                    ValueLookup::ReferenceWritten
                );
            })
        })
        .collect::<Vec<_>>();
    for worker in workers {
        worker.join().unwrap();
    }
    assert_eq!(interning.snapshot_all().len(), 4);
}

fn python_assign_reference(
    py: Python<'_>,
    serializer: &Serializer,
    variable: &str,
    value: &Bound<'_, PyAny>,
    lightweight_repr: bool,
) -> Result<Vec<u8>, PyErr> {
    const PY_TUPLE_EXTENSION_TYPE: i8 = 6;
    let mut inner = Vec::new();
    rmp::encode::write_array_len(&mut inner, 2).unwrap();
    rmp::encode::write_str(&mut inner, variable).unwrap();
    inner.extend(serializer.python_dump_msgpack(py, value, lightweight_repr)?);

    let mut expected = Vec::new();
    rmp::encode::write_str(&mut expected, "assign").unwrap();
    rmp::encode::write_ext_meta(
        &mut expected,
        inner.len().try_into().unwrap(),
        PY_TUPLE_EXTENSION_TYPE,
    )
    .unwrap();
    expected.extend(inner);
    Ok(expected)
}

#[test]
fn test_assign_exact_scalars_match_python_bytes() {
    Python::initialize();

    Python::attach(|py| {
        let module = PyModule::from_code(
                py,
                c"values = [\n    None, False, True,\n    -(1 << 63), -32769, -32768, -129, -128, -33, -32, -1,\n    0, 127, 128, 255, 256, 65535, 65536, (1 << 32) - 1, 1 << 32,\n    (1 << 63) - 1, 1 << 63, (1 << 64) - 1,\n    -0.0, 1.25, float('inf'), float('-inf'), float('nan'),\n    '', 'x' * 31, 'x' * 32, 'x' * 255, 'x' * 256,\n    'x' * 65535, 'x' * 65536, 'snowman \\N{SNOWMAN}',\n    b'', b'x' * 31, b'x' * 32, b'x' * 255, b'x' * 256,\n    b'x' * 65535, b'x' * 65536,\n]\n",
                c"assign_exact_scalars.py",
                c"assign_exact_scalars",
            )
            .expect("scalar fixtures compile");
        let serializer = Serializer::new(py).expect("serializer loads");

        for value in module
            .getattr("values")
            .expect("scalar fixtures exist")
            .cast::<PyList>()
            .expect("scalar fixtures are a list")
            .iter()
        {
            for lightweight_repr in [false, true] {
                let expected =
                    python_assign_reference(py, &serializer, "boundary", &value, lightweight_repr)
                        .expect("Python reference serializes exact scalar");
                let mut actual = Vec::new();
                write_assign_tuple(
                    &mut actual,
                    &serializer,
                    ("boundary", value.clone()),
                    lightweight_repr,
                )
                .expect("exact scalar encodes");
                assert_eq!(actual, expected);
            }
        }
    });
}

#[test]
fn test_assign_unsupported_values_match_python_bytes_errors_and_repr_calls() {
    Python::initialize();

    Python::attach(|py| {
        let module = PyModule::from_code(
                py,
                c"calls = []\nclass IntSubclass(int): pass\nclass FloatSubclass(float): pass\nclass StrSubclass(str): pass\nclass BytesSubclass(bytes): pass\nclass Custom:\n    def __repr__(self):\n        calls.append('repr')\n        return '<custom>'\nclass BrokenRepr:\n    def __repr__(self):\n        calls.append('broken repr')\n        raise RuntimeError('broken repr')\nvalues = [\n    1 << 80, -(1 << 80), '\\ud800',\n    IntSubclass(1), FloatSubclass(1.5), StrSubclass('text'), BytesSubclass(b'bytes'),\n    Custom(), BrokenRepr(), object(),\n]\n",
                c"assign_unsupported_values.py",
                c"assign_unsupported_values",
            )
            .expect("unsupported fixtures compile");
        let serializer = Serializer::new(py).expect("serializer loads");
        let calls_object = module.getattr("calls").unwrap();
        let calls = calls_object.cast::<PyList>().unwrap();

        for value in module
            .getattr("values")
            .expect("unsupported fixtures exist")
            .cast::<PyList>()
            .expect("unsupported fixtures are a list")
            .iter()
        {
            for lightweight_repr in [false, true] {
                calls.call_method0("clear").unwrap();
                let expected = python_assign_reference(
                    py,
                    &serializer,
                    "unsupported",
                    &value,
                    lightweight_repr,
                );
                let expected_calls = calls.extract::<Vec<String>>().unwrap();
                calls.call_method0("clear").unwrap();

                // The destination is deliberately non-empty: if serialization
                // fails, assignment encoding must not expose a partial
                // extension header or payload to its caller.
                let mut actual_bytes = vec![0xc0];
                let actual = write_assign_tuple(
                    &mut actual_bytes,
                    &serializer,
                    ("unsupported", value.clone()),
                    lightweight_repr,
                );

                match (expected, actual) {
                    (Ok(expected), Ok(())) => assert_eq!(&actual_bytes[1..], expected),
                    (Err(expected), Err(actual)) => {
                        assert_eq!(actual_bytes, [0xc0]);
                        assert_eq!(
                            actual.get_type(py).name().unwrap().to_str().unwrap(),
                            expected.get_type(py).name().unwrap().to_str().unwrap()
                        );
                        assert_eq!(actual.to_string(), expected.to_string());
                    }
                    (expected, actual) => panic!(
                        "Python reference and native encoder disagree: {expected:?} vs {actual:?}"
                    ),
                }
                assert_eq!(calls.extract::<Vec<String>>().unwrap(), expected_calls);
            }
        }
    });
}

#[test]
fn test_serializer_dispatches_to_lightweight_repr() {
    Python::initialize();

    Python::attach(|py| {
        let value = PyModule::from_code(
            py,
            c"class Custom:\n    def __repr__(self): return '<full repr>'\nvalue = Custom()\n",
            c"serializer_lightweight.py",
            c"serializer_lightweight",
        )
        .expect("lightweight serializer module compiles")
        .getattr("value")
        .expect("module exposes a custom value");
        let serializer = Serializer::new(py).expect("serializer loads");
        let serialize = PyModule::import(py, "kolo.serialize").expect("serializer imports");
        let expected = serialize
            .getattr("dump_msgpack_lightweight_repr")
            .expect("lightweight serializer exists")
            .call1((&value,))
            .expect("lightweight serializer accepts the custom value")
            .extract::<Vec<u8>>()
            .expect("lightweight serializer returns bytes");
        let expected_full = serialize
            .getattr("dump_msgpack")
            .expect("full serializer exists")
            .call1((&value,))
            .expect("full serializer accepts the custom value")
            .extract::<Vec<u8>>()
            .expect("full serializer returns bytes");

        let actual = serializer
            .dump_msgpack(py, &value, true)
            .expect("Serializer selects the lightweight implementation");
        assert_eq!(actual, expected);

        let mut appended = vec![0xc0];
        serializer
            .dump_msgpack_into(py, &value, true, &mut appended)
            .expect("lightweight bytes append without conversion through Vec");
        assert_eq!(&appended[1..], expected);

        let mut appended_full = vec![0xc0];
        serializer
            .dump_msgpack_into(py, &value, false, &mut appended_full)
            .expect("full bytes append without conversion through Vec");
        assert_eq!(&appended_full[1..], expected_full);
    });
}

#[test]
fn test_serializer_failures_leave_destination_unchanged() {
    Python::initialize();

    Python::attach(|py| {
        let module = PyModule::from_code(
            py,
            c"import sys\nframe = sys._getframe()\nsurrogate = '\\ud800'\nclass Interrupt(BaseException): pass\nclass Uncatchable:\n    def __repr__(self): raise Interrupt('argument serializer failed')\nuncatchable = Uncatchable()\n",
            c"serializer_failures.py",
            c"serializer_failures",
        )
        .expect("serializer failure fixtures compile");
        let serializer = Serializer::new(py).expect("serializer loads");
        let uncatchable = module.getattr("uncatchable").unwrap();
        let mut direct = vec![0xaa];
        let error = serializer
            .dump_msgpack_into(py, &uncatchable, false, &mut direct)
            .expect_err("a BaseException escapes msgpack_encode_hook");
        assert_eq!(error.to_string(), "Interrupt: argument serializer failed");
        assert_eq!(direct, [0xaa]);

        let frame = module
            .getattr("frame")
            .unwrap()
            .cast_into::<PyFrame>()
            .unwrap();
        let write_frame = |marker, arg| {
            let mut bytes = vec![marker];
            let result = write_frame_with_cached_code_metadata(
                &mut bytes,
                &frame,
                &serializer,
                &FramePathCache::new(),
                None,
                arg,
                Event::Call,
                "fixture",
                "frame-id",
                false,
                false,
                ("serializer_failures.py", Some("fixture"), None),
                None,
            );
            (bytes, result)
        };

        let (frame_bytes, result) = write_frame(0xcc, Arg::Argument(&uncatchable));
        let error = result.expect_err("the argument failure must propagate");
        assert_eq!(error.to_string(), "Interrupt: argument serializer failed");
        assert_eq!(frame_bytes, [0xcc]);

        // The module frame's locals hold a lone surrogate, which msgpack
        // cannot encode outside an extension payload.
        let exact_argument = 42_i64.into_pyobject(py).unwrap().into_any();
        let (frame_bytes, result) = write_frame(0xdd, Arg::Argument(&exact_argument));
        let error = result.expect_err("locals failure after an argument must propagate");
        assert!(error.is_instance_of::<pyo3::exceptions::PyUnicodeEncodeError>(py));
        assert_eq!(frame_bytes, [0xdd]);
    });
}

#[test]
fn test_native_msgpack_matches_python_for_formerly_rejected_shapes() {
    Python::initialize();

    Python::attach(|py| {
        let module = PyModule::from_code(
                py,
                c"class MyInt(int): pass\nclass MyFloat(float): pass\nclass MyStr(str): pass\nclass MyBytes(bytes): pass\nclass MyTuple(tuple): pass\nclass MyList(list): pass\nclass MyDict(dict): pass\nclass Custom: pass\ndeep = None\nfor _ in range(66):\n    deep = [deep]\ndeep_tuple = None\nfor _ in range(66):\n    deep_tuple = (deep_tuple,)\ntoo_deep = None\nfor _ in range(1100):\n    too_deep = [too_deep]\nlist_cycle = []\nlist_cycle.append(list_cycle)\ntuple_cycle_list = []\ntuple_cycle = (tuple_cycle_list,)\ntuple_cycle_list.append(tuple_cycle)\ndict_cycle = {}\ndict_cycle['self'] = dict_cycle\nvalues = {\n    'deep': deep, 'deep_tuple': deep_tuple, 'too_deep': too_deep,\n    'huge_positive': 1 << 80, 'huge_negative': -(1 << 80), 'lone_surrogate': '\\ud800',\n    'surrogate_in_tuple': ('\\ud800',), 'list_cycle': list_cycle, 'tuple_cycle': tuple_cycle,\n    'dict_cycle': dict_cycle, 'unsupported_list_child': [1, object()],\n    'subclasses': [MyInt(1), MyFloat(1), MyStr('x'), MyBytes(b'x'), MyTuple(), MyList([1]), MyDict(a=1)],\n    'custom_key': {Custom(): 1}, 'bytearray': bytearray(b'x'), 'memoryview': memoryview(b'xy'),\n}\n",
                c"native_msgpack_shapes.py",
                c"native_msgpack_shapes",
            )
            .expect("shape fixtures compile");
        let serializer = Serializer::new(py).expect("serializer loads");
        let values = module.getattr("values").unwrap();
        for (name, value) in values.cast::<PyDict>().unwrap().iter() {
            for lightweight_repr in [false, true] {
                let label = format!("{name} (lightweight={lightweight_repr})");
                // Default-address reprs differ between objects, not runs.
                assert_native_matches_python(py, &serializer, &value, lightweight_repr, &label);
            }
        }
    });
}

#[test]
fn test_frame_id_keeps_existing_wire_format_inline() {
    let frame_id = frame_id();

    assert_eq!(frame_id.len(), std::mem::size_of::<FrameId>());
    assert!(frame_id.starts_with("frm_"));
    assert!(ulid::Ulid::from_string(&frame_id[4..]).is_ok());
}

#[test]
fn test_direct_frame_line_number_matches_f_lineno() {
    Python::initialize();
    Python::attach(|py| {
        let module = PyModule::from_code(
            py,
            c"import inspect\nnormal_frame = inspect.currentframe()\n",
            c"missing_line.py",
            c"missing_line",
        )
        .expect("line number fixture compiles");
        let normal_frame = module
            .getattr("normal_frame")
            .expect("normal frame exists")
            .cast_into::<PyFrame>()
            .expect("normal frame is a frame");
        assert_eq!(
            frame_line_number(&normal_frame).expect("normal frames have a line"),
            normal_frame
                .getattr("f_lineno")
                .expect("f_lineno exists")
                .extract::<usize>()
                .expect("normal line number is non-negative")
        );
    });
}

#[test]
fn test_call_site_dicts_preserve_native_and_plugin_frame_ids() {
    Python::initialize();
    Python::attach(|py| {
        let module = PyModule::from_code(
            py,
            c"import inspect\nframe = inspect.currentframe()\nnot_frame = object()\n",
            c"call_site.py",
            c"call_site",
        )
        .expect("call-site fixture compiles");
        let frame = module
            .getattr("frame")
            .expect("frame exists")
            .cast_into::<PyFrame>()
            .expect("frame is a frame");
        let expected_line = frame
            .getattr("f_lineno")
            .expect("f_lineno exists")
            .extract::<i32>()
            .expect("normal line number is an integer");

        let plugin_call_site = user_code_call_site(
            vec![(
                frame.as_any().clone(),
                "external-plugin-frame-id".to_string(),
            )],
            "different-current-frame-id",
        )
        .expect("normal plugin call site builds")
        .expect("a different parent frame is a call site")
        .into_pydict(py);
        assert_eq!(
            plugin_call_site
                .get_item("call_frame_id")
                .expect("dict lookup succeeds")
                .expect("call_frame_id exists")
                .extract::<&str>()
                .expect("call_frame_id is text"),
            "external-plugin-frame-id"
        );
        assert_eq!(
            plugin_call_site
                .get_item("line_number")
                .expect("dict lookup succeeds")
                .expect("line_number exists")
                .extract::<i32>()
                .expect("line_number is an integer"),
            expected_line
        );

        let native_call_site = build_user_code_call_site(
            frame.as_any(),
            FrameId::from_str("frm_00000000000000000000000003"),
        )
        .expect("normal native call site builds")
        .expect("native call site exists")
        .into_pydict(py);
        assert_eq!(
            native_call_site
                .get_item("call_frame_id")
                .expect("dict lookup succeeds")
                .expect("call_frame_id exists")
                .extract::<&str>()
                .expect("call_frame_id is text"),
            "frm_00000000000000000000000003"
        );
        assert_eq!(
            native_call_site
                .get_item("line_number")
                .expect("dict lookup succeeds")
                .expect("line_number exists")
                .extract::<i32>()
                .expect("line_number is an integer"),
            expected_line
        );

        let not_frame = module.getattr("not_frame").expect("not-frame exists");
        let plugin_frame_error = user_code_call_site(
            vec![(not_frame.clone(), "external-plugin-frame-id".to_string())],
            "different-current-frame-id",
        )
        .err()
        .expect("plugin call sites reject non-frame objects");
        assert!(plugin_frame_error.is_instance_of::<pyo3::exceptions::PyTypeError>(py));
        let native_frame_error = build_user_code_call_site(
            &not_frame,
            FrameId::from_str("frm_00000000000000000000000004"),
        )
        .err()
        .expect("native call sites reject non-frame objects");
        assert!(native_frame_error.is_instance_of::<pyo3::exceptions::PyTypeError>(py));
    });
}

#[cfg(Py_3_10)]
#[test]
fn test_direct_frame_line_number_preserves_missing_line_errors() {
    Python::initialize();
    Python::attach(|py| {
        let module = PyModule::from_code(
            py,
            c"import inspect, types\ndef generator():\n    yield inspect.currentframe()\nno_line_frame = next(types.FunctionType(generator.__code__.replace(co_linetable=b''), globals())())\n",
            c"missing_line.py",
            c"missing_line",
        )
        .expect("missing-line fixture compiles");
        let no_line_frame = module
            .getattr("no_line_frame")
            .expect("missing-line frame exists")
            .cast_into::<PyFrame>()
            .expect("missing-line frame is a frame");
        assert!(no_line_frame
            .getattr("f_lineno")
            .expect("f_lineno exists")
            .is_none());
        assert!(frame_line_number(&no_line_frame)
            .expect_err("None cannot be extracted as usize")
            .is_instance_of::<pyo3::exceptions::PyTypeError>(py));
        let missing_line_error = build_user_code_call_site(
            no_line_frame.as_any(),
            FrameId::from_str("frm_00000000000000000000000000"),
        )
        .err()
        .expect("None cannot be extracted as i32");
        assert!(missing_line_error.is_instance_of::<pyo3::exceptions::PyTypeError>(py));

        let frame_path_error = FramePathCache::new()
            .format_frame_path(&no_line_frame)
            .err()
            .expect("missing line propagates through frame path formatting");
        assert!(frame_path_error.is_instance_of::<pyo3::exceptions::PyTypeError>(py));

        let parent_id = FrameId::from_str("frm_00000000000000000000000001");
        let child_id = FrameId::from_str("frm_00000000000000000000000002");
        let mut call_frames = CallFrames::default();
        assert!(call_frames
            .get_user_code_call_site(&no_line_frame, Event::Call, &parent_id)
            .expect("the first frame has no call site")
            .is_none());
        let call_site_error = call_frames
            .get_user_code_call_site(&no_line_frame, Event::Call, &child_id)
            .err()
            .expect("missing parent line propagates through native call sites");
        assert!(call_site_error.is_instance_of::<pyo3::exceptions::PyTypeError>(py));

        let plugin_line_error = user_code_call_site(
            vec![(
                no_line_frame.as_any().clone(),
                "external-plugin-frame-id".to_string(),
            )],
            "different-current-frame-id",
        )
        .err()
        .expect("missing parent line propagates through plugin call sites");
        assert!(plugin_line_error.is_instance_of::<pyo3::exceptions::PyTypeError>(py));
    });
}

#[test]
fn test_user_code_call_site_native_bytes_match_existing_encoding() {
    let call_site = UserCodeCallSite {
        call_frame_id: FrameId::from_str("frm_00000000000000000000000000"),
        line_number: 42,
    };
    let mut expected = Vec::new();
    rmp::encode::write_str(&mut expected, "user_code_call_site").unwrap();
    rmpv::encode::write_value(
        &mut expected,
        &rmpv::Value::Map(vec![
            (
                "call_frame_id".into(),
                "frm_00000000000000000000000000".into(),
            ),
            ("line_number".into(), 42.into()),
        ]),
    )
    .unwrap();

    let mut actual = Vec::new();
    write_user_code_call_site(&mut actual, Some(&call_site));
    assert_eq!(actual, expected);

    let mut expected_none = Vec::new();
    rmp::encode::write_str(&mut expected_none, "user_code_call_site").unwrap();
    rmpv::encode::write_value(&mut expected_none, &rmpv::Value::Nil).unwrap();
    let mut actual_none = Vec::new();
    write_user_code_call_site(&mut actual_none, None);
    assert_eq!(actual_none, expected_none);
}

#[test]
fn test_frame_path_native_bytes_match_existing_encoding() {
    for (relative_path, lineno) in [
        ("", 0),
        ("example.py", 42),
        ("snowman_☃.py", usize::MAX),
        ("path_that_crosses_the_fixstr_boundary.py", 1234),
    ] {
        let mut expected = Vec::new();
        write_str_pair(
            &mut expected,
            "path",
            Some(&format!("{relative_path}:{lineno}")),
        );

        let mut actual = Vec::new();
        write_frame_path_pair(&mut actual, relative_path, lineno);
        assert_eq!(actual, expected);
    }
}

#[test]
fn test_frame_qualname_native_bytes_match_existing_encoding() {
    for (module, co_qualname) in [
        ("", ""),
        ("example", "function"),
        ("snowman_☃", "Class.method"),
        ("module_that_crosses_the_fixstr_boundary", "nested.function"),
    ] {
        let mut expected = Vec::new();
        write_str_pair(
            &mut expected,
            "qualname",
            Some(&format!("{module}.{co_qualname}")),
        );

        let mut actual = Vec::new();
        write_frame_qualname_pair(&mut actual, module, co_qualname);
        assert_eq!(actual, expected);
    }
}

#[test]
fn test_frame_qualname_with_surrogate_uses_existing_serializer_error() {
    Python::initialize();
    Python::attach(|py| {
        let module = PyModule::from_code(
            py,
            c"import inspect\nframe = inspect.currentframe()\n__name__ = '\\ud800'\n",
            c"surrogate_module.py",
            c"surrogate_module",
        )
        .expect("surrogate module compiles");
        let frame = module.getattr("frame").expect("module exposes its frame");
        let frame = frame.cast::<PyFrame>().expect("frame is a Python frame");
        let serializer = Serializer::new(py).expect("serializer loads");
        let native_eligible = AtomicBool::new(true);
        let mut buf = Vec::new();

        let error = write_frame_with_cached_code_metadata(
            &mut buf,
            frame,
            &serializer,
            &FramePathCache::new(),
            None,
            Arg::None,
            Event::Call,
            "<module>",
            "frm_surrogate",
            false,
            false,
            (
                "surrogate_module.py",
                Some("<module>"),
                Some(&native_eligible),
            ),
            None,
        )
        .expect_err("the existing serializer rejects lone surrogates");

        assert!(error.is_instance_of::<pyo3::exceptions::PyUnicodeEncodeError>(py));
        assert!(buf.is_empty());
    });
}

#[test]
fn test_format_frame_path_invalid_path() {
    let frame_path = format_frame_path("<module>", 23);

    assert_eq!(frame_path, "<module>:23");
}

#[test]
fn test_lexical_path_helpers_normalize_without_filesystem_access() {
    assert_eq!(lexical_normalize(Path::new("")), Path::new("."));
    assert_eq!(
        lexical_normalize(Path::new("./package/../example.py")),
        Path::new("example.py")
    );
    assert_eq!(
        lexical_normalize(Path::new("../package/../../example.py")),
        Path::new("../../example.py")
    );

    let root = current_dir().expect("current directory is available");
    assert_eq!(
        lexical_relative_path(&root, &root),
        Some(PathBuf::from("."))
    );
    assert_eq!(
        lexical_relative_path(&root.join("sibling.py"), &root.join("child")),
        Some(PathBuf::from("..").join("sibling.py"))
    );
}

#[cfg(windows)]
#[test]
fn test_lexical_path_helpers_handle_windows_prefixes() {
    let root = Path::new(r"C:\workspace\project");
    assert_eq!(
        lexical_normalize(Path::new(r"C:\workspace\.\package\..\file.py")),
        Path::new(r"C:\workspace\file.py")
    );
    assert_eq!(
        lexical_relative_path(Path::new(r"c:\workspace\project\file.py"), root),
        Some(PathBuf::from("file.py"))
    );
    assert_eq!(
        lexical_relative_path(Path::new(r"D:\workspace\file.py"), root),
        None
    );
    assert_eq!(
        lexical_relative_path(Path::new(r"\workspace\file.py"), root),
        None
    );
    assert_eq!(
        lexical_relative_path(Path::new(r"C:\workspace\file.py"), Path::new(r"\workspace")),
        None
    );
}

#[test]
fn test_frame_path_cache_relativizes_absolute_path_outside_root() {
    Python::initialize();

    let cache = FramePathCache::new();
    let outside_path = cache
        .root
        .parent()
        .expect("tests do not run from the filesystem root")
        .join("kolo_frame_path_cache_test.py");
    assert!(outside_path.is_absolute());
    assert!(!outside_path.starts_with(&cache.root));
    let filename = outside_path.display().to_string();
    let filename_c = CString::new(filename.clone()).expect("filename has no null bytes");

    Python::attach(|py| {
        let frame = PyModule::from_code(
            py,
            c"import inspect\nframe = inspect.currentframe()\n",
            &filename_c,
            c"frame_path_cache_test",
        )
        .expect("test module compiles")
        .getattr("frame")
        .expect("test module exposes its frame");
        let frame = frame.cast::<PyFrame>().expect("frame is a Python frame");
        let (_, lineno) =
            filename_with_lineno(frame, py).expect("frame has a filename and line number");

        let first = cache
            .format_frame_path(frame)
            .expect("frame path can be formatted");
        let second = cache
            .format_frame_path(frame)
            .expect("cached frame path can be formatted");

        let expected_path = Path::new("..").join("kolo_frame_path_cache_test.py");
        assert_eq!(first, format!("{}:{lineno}", expected_path.display()));
        assert_eq!(second, first);
        assert_eq!(
            cache
                .paths
                .lock_py_attached(py)
                .expect("frame path cache mutex poisoned")
                .len(),
            1
        );
    });
}
#[test]
fn test_frame_path_cache_normalizes_relative_path() {
    Python::initialize();

    let cache = FramePathCache::new();
    Python::attach(|py| {
        let frame = PyModule::from_code(
            py,
            c"import inspect\nframe = inspect.currentframe()\n",
            c"package/../example.py",
            c"frame_path_cache_test",
        )
        .expect("test module compiles")
        .getattr("frame")
        .expect("test module exposes its frame");
        let frame = frame.cast::<PyFrame>().expect("frame is a Python frame");
        let (_, lineno) =
            filename_with_lineno(frame, py).expect("frame has a filename and line number");

        assert_eq!(
            cache
                .format_frame_path(frame)
                .expect("frame path can be formatted"),
            format!("example.py:{lineno}")
        );
    });
}
