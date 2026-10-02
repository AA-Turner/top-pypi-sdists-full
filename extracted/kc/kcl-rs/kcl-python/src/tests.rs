//! Rust `#[test]`s validating the GIL bridge WITHOUT any AWS dependency.
//!
//! These use PyO3's `auto-initialize` dev-feature to spin up an in-process
//! Python interpreter, define a small Python `RecordProcessor` via
//! `PyModule::from_code`, wrap it in [`PyRecordProcessor`], and drive the
//! lifecycle callbacks from Rust — asserting the Python side observed the calls
//! and could call `checkpointer.checkpoint()`. Also covers the factory bridge
//! and the `Checkpointer` -> `CheckpointError` error mapping.

use std::ffi::CString;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};

use pyo3::prelude::*;
use pyo3::types::PyModule;

use kcl::exceptions::KinesisClientLibError;
use kcl::lifecycle::events::{
    InitializationInput, LeaseLostInput, ProcessRecordsInput, ShardEndedInput,
};
use kcl::processor::{
    Checkpointer as KclCheckpointer, PreparedCheckpointer, RecordProcessorCheckpointer,
    ShardRecordProcessor, ShardRecordProcessorFactory,
};
use kcl::retrieval::kpl::ExtendedSequenceNumber;
use kcl::retrieval::KinesisClientRecord;

use crate::processor::{PyRecordProcessor, PyRecordProcessorFactory};

/// Shared recording state: the ordered list of calls seen, plus an optional
/// error to inject on the *next* call. Shared (via `Arc`) between a
/// [`RecordingCheckpointer`] and any [`RecordingPreparedCheckpointer`] it hands
/// out, so a prepared checkpointer's commit records into the same list.
#[derive(Default)]
struct RecordingState {
    calls: Mutex<Vec<String>>,
    fail_with: Mutex<Option<KinesisClientLibError>>,
}

impl RecordingState {
    fn result(&self, tag: &str) -> Result<(), KinesisClientLibError> {
        self.calls.lock().unwrap().push(tag.to_string());
        match self.fail_with.lock().unwrap().take() {
            Some(e) => Err(e),
            None => Ok(()),
        }
    }
}

/// A test `RecordProcessorCheckpointer` that records the calls it received and
/// can be configured to fail with a specific [`KinesisClientLibError`].
struct RecordingCheckpointer {
    state: Arc<RecordingState>,
}

impl RecordingCheckpointer {
    fn new() -> Arc<Self> {
        Arc::new(Self {
            state: Arc::new(RecordingState::default()),
        })
    }

    fn failing(err: KinesisClientLibError) -> Arc<Self> {
        let state = RecordingState::default();
        *state.fail_with.lock().unwrap() = Some(err);
        Arc::new(Self {
            state: Arc::new(state),
        })
    }

    /// The recorded calls (a snapshot).
    fn calls(&self) -> Vec<String> {
        self.state.calls.lock().unwrap().clone()
    }

    fn result(&self, tag: &str) -> Result<(), KinesisClientLibError> {
        self.state.result(tag)
    }

    /// Record a `prepare_*` call and return a prepared checkpointer (or the
    /// configured error). The prepared checkpointer shares this recorder's state
    /// so its commit records into the same list.
    fn prepare_result(
        &self,
        tag: &str,
        pending_seq: &str,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.state.calls.lock().unwrap().push(tag.to_string());
        if let Some(e) = self.state.fail_with.lock().unwrap().take() {
            return Err(e);
        }
        Ok(Box::new(RecordingPreparedCheckpointer {
            state: Arc::clone(&self.state),
            pending: ExtendedSequenceNumber::from_sequence_number(pending_seq),
        }))
    }
}

impl RecordProcessorCheckpointer for RecordingCheckpointer {
    fn checkpoint(&self) -> Result<(), KinesisClientLibError> {
        self.result("checkpoint")
    }
    fn checkpoint_record(
        &self,
        _record: &aws_sdk_kinesis::types::Record,
    ) -> Result<(), KinesisClientLibError> {
        self.result("checkpoint_record")
    }
    fn checkpoint_sequence(&self, seq: &str) -> Result<(), KinesisClientLibError> {
        self.result(&format!("checkpoint_sequence:{seq}"))
    }
    fn checkpoint_sequence_sub(&self, seq: &str, sub: i64) -> Result<(), KinesisClientLibError> {
        self.result(&format!("checkpoint_sequence_sub:{seq}:{sub}"))
    }
    fn prepare_checkpoint(
        &self,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_result("prepare_checkpoint", "last")
    }
    fn prepare_checkpoint_state(
        &self,
        _s: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        unimplemented!()
    }
    fn prepare_checkpoint_record(
        &self,
        _r: &aws_sdk_kinesis::types::Record,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        unimplemented!()
    }
    fn prepare_checkpoint_record_state(
        &self,
        _r: &aws_sdk_kinesis::types::Record,
        _s: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        unimplemented!()
    }
    fn prepare_checkpoint_sequence(
        &self,
        seq: &str,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_result(&format!("prepare_checkpoint_sequence:{seq}"), seq)
    }
    fn prepare_checkpoint_sequence_state(
        &self,
        _seq: &str,
        _s: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        unimplemented!()
    }
    fn prepare_checkpoint_sequence_sub(
        &self,
        seq: &str,
        sub: i64,
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        self.prepare_result(&format!("prepare_checkpoint_sequence_sub:{seq}:{sub}"), seq)
    }
    fn prepare_checkpoint_sequence_sub_state(
        &self,
        _seq: &str,
        _sub: i64,
        _s: &[u8],
    ) -> Result<Box<dyn PreparedCheckpointer + Send + Sync>, KinesisClientLibError> {
        unimplemented!()
    }
    fn checkpointer(&self) -> Box<dyn KclCheckpointer + Send + Sync> {
        unimplemented!()
    }
}

/// A [`PreparedCheckpointer`] that records its `checkpoint()` (commit) call into
/// the shared [`RecordingState`] and can be configured to fail via that state.
struct RecordingPreparedCheckpointer {
    state: Arc<RecordingState>,
    pending: ExtendedSequenceNumber,
}

impl PreparedCheckpointer for RecordingPreparedCheckpointer {
    fn pending_checkpoint(&self) -> ExtendedSequenceNumber {
        self.pending.clone()
    }
    fn checkpoint(&self) -> Result<(), KinesisClientLibError> {
        self.state.result("prepared.checkpoint")
    }
}

/// Define a Python `RecordProcessor` class in a fresh module and return an
/// *instance* of it. The class records each callback into a shared `events`
/// list and, on `process_records`, iterates the records and checkpoints.
fn make_python_processor(py: Python<'_>) -> Py<PyAny> {
    let code = CString::new(
        r#"
class TestProcessor:
    version = 3
    def __init__(self):
        self.events = []
    def initialize(self, initialize_input):
        self.events.append(("initialize", initialize_input.shard_id,
                            initialize_input.sequence_number))
    def process_records(self, process_records_input):
        recs = process_records_input.records
        payloads = [r.binary_data for r in recs]
        self.events.append(("process_records", len(recs), payloads,
                            process_records_input.millis_behind_latest))
        # Exercise the checkpointer bridge.
        process_records_input.checkpointer.checkpoint()
    def lease_lost(self, lease_lost_input):
        self.events.append(("lease_lost",))
    def shard_ended(self, shard_ended_input):
        self.events.append(("shard_ended",))
        shard_ended_input.checkpointer.checkpoint()
    def shutdown_requested(self, shutdown_requested_input):
        self.events.append(("shutdown_requested",))

def make():
    return TestProcessor()
"#,
    )
    .unwrap();
    let module = PyModule::from_code(py, code.as_c_str(), c"test_processor.py", c"test_processor")
        .expect("python module compiles");
    module
        .getattr("TestProcessor")
        .unwrap()
        .call0()
        .unwrap()
        .unbind()
}

#[test]
fn initialize_and_process_records_bridge() {
    Python::attach(|py| {
        let py_obj = make_python_processor(py);
        // Keep a handle to read back its `events` after the callbacks.
        let handle = py_obj.clone_ref(py);
        let mut processor = PyRecordProcessor::new(py_obj);

        // initialize
        let init = InitializationInput::builder()
            .shard_id("shard-0001")
            .extended_sequence_number(
                kcl::retrieval::kpl::ExtendedSequenceNumber::from_sequence_number("42"),
            )
            .build();
        processor.initialize(init);

        // process_records with two records + a recording checkpointer
        let cp = RecordingCheckpointer::new();
        let cp_dyn: Arc<dyn RecordProcessorCheckpointer + Send + Sync> = cp.clone();
        let records = vec![
            KinesisClientRecord::builder()
                .sequence_number("seq-1")
                .partition_key("pk-1")
                .data(bytes::Bytes::from_static(b"hello"))
                .build(),
            KinesisClientRecord::builder()
                .sequence_number("seq-2")
                .partition_key("pk-2")
                .data(bytes::Bytes::from_static(b"world"))
                .build(),
        ];
        let pri = ProcessRecordsInput::builder()
            .records(records)
            .millis_behind_latest(123)
            .checkpointer(cp_dyn)
            .build();
        processor.process_records(pri);

        // Read back the Python-side observed events.
        let events = handle.bind(py).getattr("events").unwrap();
        let events: Vec<Py<PyAny>> = events.extract().unwrap();
        assert_eq!(events.len(), 2, "two callbacks observed");

        // event[0] == ("initialize", "shard-0001", "42")
        let e0: (String, String, String) = events[0].extract(py).unwrap();
        assert_eq!(e0.0, "initialize");
        assert_eq!(e0.1, "shard-0001");
        assert_eq!(e0.2, "42");

        // event[1] == ("process_records", 2, [b"hello", b"world"], 123)
        let e1: (String, usize, Vec<Vec<u8>>, i64) = events[1].extract(py).unwrap();
        assert_eq!(e1.0, "process_records");
        assert_eq!(e1.1, 2);
        assert_eq!(e1.2, vec![b"hello".to_vec(), b"world".to_vec()]);
        assert_eq!(e1.3, 123);

        // The Python `checkpoint()` call reached the Rust checkpointer.
        assert_eq!(cp.calls().as_slice(), &["checkpoint".to_string()]);
    });
}

#[test]
fn shard_ended_and_lease_lost_and_shutdown_requested_bridge() {
    Python::attach(|py| {
        let py_obj = make_python_processor(py);
        let handle = py_obj.clone_ref(py);
        let mut processor = PyRecordProcessor::new(py_obj);

        processor.lease_lost(LeaseLostInput::new());

        let cp = RecordingCheckpointer::new();
        let cp_dyn: Arc<dyn RecordProcessorCheckpointer + Send + Sync> = cp.clone();
        let se = ShardEndedInput::builder().checkpointer(cp_dyn).build();
        processor.shard_ended(se);

        let events: Vec<Py<PyAny>> = handle
            .bind(py)
            .getattr("events")
            .unwrap()
            .extract()
            .unwrap();
        assert_eq!(events.len(), 2);
        let e0: (String,) = events[0].extract(py).unwrap();
        assert_eq!(e0.0, "lease_lost");
        let e1: (String,) = events[1].extract(py).unwrap();
        assert_eq!(e1.0, "shard_ended");
        // shard_ended's checkpoint() reached Rust.
        assert_eq!(cp.calls().as_slice(), &["checkpoint".to_string()]);
    });
}

#[test]
fn factory_bridge_makes_a_processor_via_callable_and_method() {
    Python::attach(|py| {
        // (a) factory as a plain callable (the class itself).
        let module = PyModule::from_code(
            py,
            &CString::new(
                r#"
class P:
    version = 3
    def initialize(self, i): pass
    def process_records(self, p): pass
    def lease_lost(self, l): pass
    def shard_ended(self, s): pass
    def shutdown_requested(self, s): pass

class Factory:
    def shard_record_processor(self):
        return P()
"#,
            )
            .unwrap(),
            c"factory.py",
            c"factory",
        )
        .unwrap();

        // Callable factory (the class P): factory() -> P()
        let callable = module.getattr("P").unwrap().unbind();
        let f1 = PyRecordProcessorFactory::new(callable);
        let _p1: Box<dyn ShardRecordProcessor + Send + Sync> = f1.shard_record_processor();

        // Object with a shard_record_processor() method.
        let factory_obj = module.getattr("Factory").unwrap().call0().unwrap().unbind();
        let f2 = PyRecordProcessorFactory::new(factory_obj);
        let _p2: Box<dyn ShardRecordProcessor + Send + Sync> = f2.shard_record_processor();
    });
}

#[test]
fn checkpointer_maps_error_to_checkpoint_error() {
    Python::attach(|py| {
        let cp = RecordingCheckpointer::failing(KinesisClientLibError::shutdown("shut down"));
        let cp_dyn: Arc<dyn RecordProcessorCheckpointer + Send + Sync> = cp.clone();
        let py_cp = Py::new(py, crate::checkpointer::Checkpointer::new(cp_dyn)).unwrap();

        // Call checkpoint() from Python; expect a CheckpointError with value
        // "ShutdownException" (mirrors amazon_kclpy's e.value comparison).
        let result = py_cp.bind(py).call_method0("checkpoint");
        let err = result.expect_err("checkpoint should raise");
        // The exception message is the Java-style name.
        let msg = err.value(py).str().unwrap().to_string();
        assert_eq!(msg, "ShutdownException");
        // amazon_kclpy parity: `e.value` is the Java-style name too (its
        // CheckpointError.__init__ stores the name on `.value`, and ported
        // retry logic compares `e.value == 'ShutdownException'`).
        let value: String = err
            .value(py)
            .getattr("value")
            .expect("CheckpointError exposes .value")
            .extract()
            .unwrap();
        assert_eq!(value, "ShutdownException");
        // And it is our CheckpointError type.
        assert!(err.is_instance_of::<crate::checkpointer::CheckpointError>(py));
    });
}

#[test]
fn checkpointer_success_dispatches_variants() {
    Python::attach(|py| {
        // no args -> checkpoint()
        let cp = RecordingCheckpointer::new();
        let cp_dyn: Arc<dyn RecordProcessorCheckpointer + Send + Sync> = cp.clone();
        let py_cp = Py::new(py, crate::checkpointer::Checkpointer::new(cp_dyn)).unwrap();
        py_cp.bind(py).call_method0("checkpoint").unwrap();

        // seq only -> checkpoint_sequence(seq)
        py_cp
            .bind(py)
            .call_method1("checkpoint", ("seq-9",))
            .unwrap();

        // seq + sub -> checkpoint_sequence_sub(seq, sub)
        py_cp
            .bind(py)
            .call_method1("checkpoint", ("seq-9", 3i64))
            .unwrap();

        assert_eq!(
            cp.calls().as_slice(),
            &[
                "checkpoint".to_string(),
                "checkpoint_sequence:seq-9".to_string(),
                "checkpoint_sequence_sub:seq-9:3".to_string(),
            ]
        );
    });
}

/// `Checkpointer.prepare_checkpoint(...)` returns a `PreparedCheckpointer` whose
/// `.checkpoint()` commits it. Covers the three arg shapes and the commit path.
#[test]
fn prepare_checkpoint_returns_committable_prepared_checkpointer() {
    Python::attach(|py| {
        let cp = RecordingCheckpointer::new();
        let cp_dyn: Arc<dyn RecordProcessorCheckpointer + Send + Sync> = cp.clone();
        let py_cp = Py::new(py, crate::checkpointer::Checkpointer::new(cp_dyn)).unwrap();

        // no args -> prepare_checkpoint(); then commit.
        let prepared = py_cp.bind(py).call_method0("prepare_checkpoint").unwrap();
        // The pending sequence is exposed.
        let pending: (String, i64) = prepared
            .getattr("pending_checkpoint")
            .unwrap()
            .extract()
            .unwrap();
        assert_eq!(pending, ("last".to_string(), 0));
        prepared.call_method0("checkpoint").unwrap();

        // seq only -> prepare_checkpoint_sequence(seq); then commit.
        let prepared = py_cp
            .bind(py)
            .call_method1("prepare_checkpoint", ("seq-7",))
            .unwrap();
        prepared.call_method0("checkpoint").unwrap();

        // seq + sub -> prepare_checkpoint_sequence_sub(seq, sub); then commit.
        let prepared = py_cp
            .bind(py)
            .call_method1("prepare_checkpoint", ("seq-7", 4i64))
            .unwrap();
        prepared.call_method0("checkpoint").unwrap();

        assert_eq!(
            cp.calls().as_slice(),
            &[
                "prepare_checkpoint".to_string(),
                "prepared.checkpoint".to_string(),
                "prepare_checkpoint_sequence:seq-7".to_string(),
                "prepared.checkpoint".to_string(),
                "prepare_checkpoint_sequence_sub:seq-7:4".to_string(),
                "prepared.checkpoint".to_string(),
            ]
        );
    });
}

/// A failure while committing a prepared checkpoint maps to `CheckpointError`
/// (with the Java-style name as its value), mirroring `checkpoint`.
#[test]
fn prepared_checkpointer_commit_maps_error() {
    Python::attach(|py| {
        let cp = RecordingCheckpointer::new();
        let cp_dyn: Arc<dyn RecordProcessorCheckpointer + Send + Sync> = cp.clone();
        let py_cp = Py::new(py, crate::checkpointer::Checkpointer::new(cp_dyn)).unwrap();

        // Prepare succeeds; then arm the shared state to fail the commit.
        let prepared = py_cp.bind(py).call_method0("prepare_checkpoint").unwrap();
        *cp.state.fail_with.lock().unwrap() = Some(KinesisClientLibError::throttling("slow down"));

        let err = prepared
            .call_method0("checkpoint")
            .expect_err("commit should raise");
        assert_eq!(
            err.value(py).str().unwrap().to_string(),
            "ThrottlingException"
        );
        assert!(err.is_instance_of::<crate::checkpointer::CheckpointError>(py));
    });
}

/// AT_TIMESTAMP `timestamp` parsing accepts epoch seconds (int/float) and a
/// Python `datetime` (aware or naive→UTC).
#[test]
fn parse_timestamp_accepts_epoch_and_datetime() {
    use chrono::{Datelike, TimeZone, Timelike, Utc};

    Python::attach(|py| {
        // int epoch seconds
        let v = 1_000_000i64.into_pyobject(py).unwrap().into_any();
        let dt = crate::scheduler::parse_timestamp(&v).unwrap();
        assert_eq!(dt, Utc.timestamp_opt(1_000_000, 0).unwrap());

        // float epoch seconds (with fractional seconds)
        let v = 1_000_000.5f64.into_pyobject(py).unwrap().into_any();
        let dt = crate::scheduler::parse_timestamp(&v).unwrap();
        assert_eq!(dt, Utc.timestamp_opt(1_000_000, 500_000_000).unwrap());

        // an aware datetime built in Python (UTC)
        let datetime_mod = py.import("datetime").unwrap();
        let tz_utc = datetime_mod
            .getattr("timezone")
            .unwrap()
            .getattr("utc")
            .unwrap();
        let aware = datetime_mod
            .getattr("datetime")
            .unwrap()
            .call1((2021, 5, 6, 7, 8, 9, 0, &tz_utc))
            .unwrap();
        let dt = crate::scheduler::parse_timestamp(&aware).unwrap();
        assert_eq!((dt.year(), dt.month(), dt.day()), (2021, 5, 6));
        assert_eq!((dt.hour(), dt.minute(), dt.second()), (7, 8, 9));

        // a naive datetime is interpreted as UTC
        let naive = datetime_mod
            .getattr("datetime")
            .unwrap()
            .call1((2021, 5, 6, 7, 8, 9))
            .unwrap();
        let dt = crate::scheduler::parse_timestamp(&naive).unwrap();
        assert_eq!((dt.year(), dt.hour(), dt.second()), (2021, 7, 9));

        // a bad value (a string) is a clean error, not a panic
        let bad = "not-a-timestamp".into_pyobject(py).unwrap().into_any();
        assert!(crate::scheduler::parse_timestamp(&bad).is_err());
    });
}

/// The `Scheduler` pyclass must be usable from a thread other than the one
/// that constructed it: `shutdown()` is documented as callable from any thread
/// (e.g. a signal-handler thread while `run()` blocks the main thread). With
/// `unsendable` on the pyclass this panics
/// ("...is unsendable, but sent to another thread").
#[test]
fn scheduler_is_usable_from_another_thread() {
    let sched: Py<PyAny> = Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = pyo3::types::PyDict::new(py);
        kwargs.set_item("stream_name", "test-stream").unwrap();
        kwargs.set_item("application_name", "test-app").unwrap();
        // Any callable works as a factory; it is never invoked here.
        let object_cls = py.import("builtins").unwrap().getattr("object").unwrap();
        kwargs
            .set_item("record_processor_factory", object_cls)
            .unwrap();
        cls.call((), Some(&kwargs)).unwrap().unbind()
    });

    std::thread::spawn(move || {
        Python::attach(|py| {
            let bound = sched.bind(py);
            // Borrowing the pyclass from this (non-creating) thread is the
            // operation an unsendable class panics on.
            bound.repr().unwrap();
            // Never started -> shutdown() is a no-op Ok(()).
            bound.call_method0("shutdown").unwrap();
        });
    })
    .join()
    .expect("Scheduler methods must not panic when called from another thread");
}

/// Build the base kwargs every `Scheduler` construction needs
/// (`stream_name`/`application_name`/`record_processor_factory`), so each
/// credential-validation test only has to add the credential kwargs under test.
fn base_scheduler_kwargs<'py>(py: Python<'py>) -> Bound<'py, pyo3::types::PyDict> {
    let kwargs = pyo3::types::PyDict::new(py);
    kwargs.set_item("stream_name", "test-stream").unwrap();
    kwargs.set_item("application_name", "test-app").unwrap();
    // Any callable works as a factory; it is never invoked here.
    let object_cls = py.import("builtins").unwrap().getattr("object").unwrap();
    kwargs
        .set_item("record_processor_factory", object_cls)
        .unwrap();
    kwargs
}

/// `access_key_id` without `secret_access_key` must raise `ValueError` at
/// construction (they are required together).
#[test]
fn scheduler_access_key_id_without_secret_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("access_key_id", "AKIDEXAMPLE").unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// `secret_access_key` without `access_key_id` must raise `ValueError` at
/// construction (they are required together).
#[test]
fn scheduler_secret_access_key_without_key_id_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs
            .set_item("secret_access_key", "secretexample")
            .unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// `session_token` alone (without `access_key_id`/`secret_access_key`) must
/// raise `ValueError` at construction.
#[test]
fn scheduler_session_token_alone_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("session_token", "sessiontoken").unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// All three credential kwargs together (plus the required args) construct
/// fine — construction does no network I/O, so no credential is ever
/// validated against AWS here.
#[test]
fn scheduler_with_full_credentials_constructs() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("access_key_id", "AKIDEXAMPLE").unwrap();
        kwargs
            .set_item("secret_access_key", "secretexample")
            .unwrap();
        kwargs.set_item("session_token", "sessiontoken").unwrap();
        cls.call((), Some(&kwargs))
            .expect("access_key_id + secret_access_key + session_token must construct fine");
    });
}

/// `retrieval_mode` accepts `"FANOUT"`/`"POLLING"` case-insensitively.
#[test]
fn scheduler_retrieval_mode_accepts_polling_case_insensitively() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        for mode in ["polling", "POLLING", "Polling"] {
            let kwargs = base_scheduler_kwargs(py);
            kwargs.set_item("retrieval_mode", mode).unwrap();
            cls.call((), Some(&kwargs))
                .unwrap_or_else(|e| panic!("retrieval_mode={mode:?} should construct: {e}"));
        }
    });
}

/// An unrecognized `retrieval_mode` is a `ValueError`.
#[test]
fn scheduler_retrieval_mode_garbage_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("retrieval_mode", "garbage").unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// `max_records` with the default (fan-out) retrieval mode is a `ValueError`
/// (the knob is polling-only).
#[test]
fn scheduler_max_records_without_polling_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("max_records", 100).unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// `idle_time_between_reads_millis` with an explicit `retrieval_mode="FANOUT"`
/// is a `ValueError`.
#[test]
fn scheduler_idle_time_without_polling_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("retrieval_mode", "FANOUT").unwrap();
        kwargs
            .set_item("idle_time_between_reads_millis", 500)
            .unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// The full polling combo (`retrieval_mode="polling"` + both knobs) constructs
/// fine — construction does no network I/O, so no `PollingConfig` setter runs
/// yet.
#[test]
fn scheduler_polling_with_knobs_constructs() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("retrieval_mode", "polling").unwrap();
        kwargs.set_item("max_records", 100).unwrap();
        kwargs
            .set_item("idle_time_between_reads_millis", 500)
            .unwrap();
        cls.call((), Some(&kwargs))
            .expect("retrieval_mode=polling with max_records + idle_time_between_reads_millis must construct");
    });
}

/// `shard_sync_interval_millis` is not gated on the retrieval mode — it wires
/// `LeaseManagementConfig::shard_sync_interval_millis_set` and applies to both
/// fan-out and polling. Construction does no network I/O, so it just captures
/// the value.
#[test]
fn scheduler_shard_sync_interval_constructs_in_both_modes() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        for mode in ["FANOUT", "POLLING"] {
            let kwargs = base_scheduler_kwargs(py);
            kwargs.set_item("retrieval_mode", mode).unwrap();
            kwargs
                .set_item("shard_sync_interval_millis", 30_000)
                .unwrap();
            cls.call((), Some(&kwargs)).unwrap_or_else(|e| {
                panic!(
                    "shard_sync_interval_millis with retrieval_mode={mode:?} should construct: {e}"
                )
            });
        }
    });
}

/// `max_records` above `PollingConfig`'s 10000 cap is a `ValueError` at
/// construction (mirrors the panic `PollingConfig::set_max_records` would
/// otherwise raise at `start()`/`run()`).
#[test]
fn scheduler_max_records_out_of_range_is_value_error() {
    Python::attach(|py| {
        let cls = py.get_type::<crate::scheduler::Scheduler>();
        let kwargs = base_scheduler_kwargs(py);
        kwargs.set_item("retrieval_mode", "polling").unwrap();
        kwargs.set_item("max_records", 10_001).unwrap();
        let err = cls.call((), Some(&kwargs)).unwrap_err();
        assert!(err.is_instance_of::<pyo3::exceptions::PyValueError>(py));
    });
}

/// A bad Python callback must not crash the worker — the exception is swallowed.
#[test]
fn bad_callback_is_swallowed() {
    static SENTINEL: AtomicUsize = AtomicUsize::new(0);
    Python::attach(|py| {
        let module = PyModule::from_code(
            py,
            &CString::new(
                r#"
class Boom:
    version = 3
    def initialize(self, i):
        raise RuntimeError("boom in initialize")
    def process_records(self, p): pass
    def lease_lost(self, l): pass
    def shard_ended(self, s): pass
    def shutdown_requested(self, s): pass
"#,
            )
            .unwrap(),
            c"boom.py",
            c"boom",
        )
        .unwrap();
        let obj = module.getattr("Boom").unwrap().call0().unwrap().unbind();
        let mut processor = PyRecordProcessor::new(obj);
        // Should NOT panic / propagate.
        processor.initialize(InitializationInput::builder().shard_id("s").build());
        SENTINEL.fetch_add(1, Ordering::SeqCst);
    });
    assert_eq!(SENTINEL.load(Ordering::SeqCst), 1);
}
