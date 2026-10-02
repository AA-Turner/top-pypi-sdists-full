//! The `Scheduler` `#[pyclass]` — the Python control surface for the KCL.
//!
//! # Runtime & GIL model
//!
//! The Rust KCL runs on its **own** multi-threaded tokio runtime, on background
//! threads that are entirely separate from the Python interpreter thread. Python
//! only *controls* it:
//!
//! * [`Scheduler::__new__`] just captures configuration (no I/O, no runtime).
//! * [`Scheduler::start`] builds the runtime + AWS clients + the core
//!   `kcl::coordinator::Scheduler`, spawns the scheduler's run loop **on the
//!   runtime's own threads**, and returns immediately. The GIL is released
//!   (`py.allow_threads`) during the blocking build/`block_on` setup steps.
//! * [`Scheduler::run`] does the same build but then **blocks the calling Python
//!   thread** until shutdown. The run loop executes on the runtime's own
//!   threads; this thread waits in short slices with the GIL released,
//!   re-attaching between slices to deliver pending Python signals — so Ctrl-C
//!   (KeyboardInterrupt) triggers a graceful shutdown and is then re-raised.
//!   Record-processor callbacks re-acquire the GIL transiently (see
//!   [`crate::processor`]).
//! * [`Scheduler::shutdown`] signals graceful shutdown and awaits it (GIL
//!   released while waiting). It may be called from any thread.
//! * Dropping a still-running `Scheduler` (GC / interpreter exit without
//!   `shutdown()`) must not block: pyclass dealloc runs with the GIL held, and
//!   a blocking runtime teardown would deadlock against in-flight callbacks
//!   waiting to attach to that same GIL — see [`RunningState`]'s `Drop`.
//!
//! A live run talks to real AWS (or LocalStack via `endpoint_url`); construction
//! itself does no network I/O.

use std::sync::Arc;
use std::sync::Mutex;

use chrono::{DateTime, TimeZone, Utc};
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyDateTime;

use kcl::common::{ConfigsBuilder, InitialPositionInStream, InitialPositionInStreamExtended};
use kcl::coordinator::Scheduler as CoreScheduler;
use kcl::processor::{ShardRecordProcessorFactory, SingleStreamTracker, StreamTracker};

use crate::processor::PyRecordProcessorFactory;
use crate::stream_tracker::PyMultiStreamTracker;

/// Configuration captured from Python at construction time. No I/O happens here.
struct SchedulerConfig {
    /// The single stream to consume, or `None` in multi-stream mode.
    stream_name: Option<String>,
    /// Serialized multi-stream identifiers (`accountId:streamName:creationEpoch`)
    /// in multi-stream mode; empty in single-stream mode.
    stream_identifiers: Vec<String>,
    application_name: String,
    worker_identifier: String,
    factory: Py<PyAny>,
    region: Option<String>,
    endpoint_url: Option<String>,
    initial_position: String,
    /// The timestamp for `initial_position == "AT_TIMESTAMP"`, already parsed
    /// from the Python `timestamp` argument (epoch seconds or a `datetime`).
    at_timestamp: Option<DateTime<Utc>>,
    /// Explicit static credentials, validated at construction (see `new`) to
    /// come as either all `None` or `access_key_id`+`secret_access_key` (with
    /// `session_token` optional). Override the default credential chain when set.
    access_key_id: Option<String>,
    secret_access_key: Option<String>,
    session_token: Option<String>,
    /// `"fanout"` (default) or `"polling"`, normalized lowercase (validated
    /// case-insensitively in `new`).
    retrieval_mode: String,
    /// Polling-only: `PollingConfig::set_max_records`. `None` uses the
    /// `PollingConfig` default (10000).
    max_records: Option<i32>,
    /// Polling-only: `PollingConfig::set_idle_time_between_reads_in_millis`.
    /// `None` uses the `PollingConfig` default (1500ms).
    idle_time_between_reads_millis: Option<i64>,
    /// `LeaseManagementConfig::shard_sync_interval_millis_set`. `None` uses the
    /// `LeaseManagementConfig` default (60000ms).
    shard_sync_interval_millis: Option<i64>,
}

/// The live runtime + running scheduler handle (populated on `start`/`run`).
struct RunningState {
    /// The tokio runtime. `Some` until an explicit `shutdown()` takes it (for a
    /// graceful, blocking teardown off the GIL) or `Drop` reaps it.
    runtime: Option<tokio::runtime::Runtime>,
    /// The core scheduler. Also mirrored into [`Scheduler::signal`] so
    /// `shutdown()` can signal it without contending on the state lock (which
    /// `run()` may hold for the whole blocking drive).
    scheduler: Arc<CoreScheduler>,
    join_handle: Option<tokio::task::JoinHandle<()>>,
}

impl Drop for RunningState {
    fn drop(&mut self) {
        // Never block here. The pyclass may be deallocated (GC / interpreter
        // exit after `start()` without `shutdown()`) on a thread that holds the
        // GIL; a normal `Runtime` drop waits for in-flight `spawn_blocking`
        // record-processor callbacks, which may themselves be blocked in
        // `Python::attach` waiting for that same GIL — a permanent deadlock.
        // `shutdown_background` releases the runtime without joining its
        // threads, so dealloc always makes progress.
        if let Some(runtime) = self.runtime.take() {
            runtime.shutdown_background();
        }
    }
}

/// The Python-facing KCL scheduler.
///
/// Construct it with the stream/application/worker identity and a Python
/// record-processor factory, then call `start()` (non-blocking) or `run()`
/// (blocking) to drive it, and `shutdown()` to stop.
/// The pyclass is deliberately *not* `unsendable`: `shutdown()` is commonly
/// called from a thread other than the one that constructed the scheduler
/// (e.g. a signal-handler thread while `run()` blocks the main thread), and an
/// unsendable pyclass panics on any cross-thread access. Everything held here
/// is `Send + Sync`.
#[pyclass(module = "kcl_rs", name = "Scheduler")]
pub struct Scheduler {
    config: SchedulerConfig,
    // `Mutex` so the (interior-mutable) running state can be swapped in on
    // `start`/`run`. `run()` holds the state lock for its whole blocking drive,
    // so `shutdown()` must NOT contend on it — it signals via `signal` instead.
    state: Mutex<Option<RunningState>>,
    /// A shutdown-signalling handle set on `start`/`run`, readable without the
    /// `state` lock. Holds an `Arc<CoreScheduler>` + a `Handle` to await on.
    signal: Mutex<Option<ShutdownSignal>>,
}

/// A cross-thread handle that lets `shutdown()` stop a running scheduler even
/// while `run()` holds the `state` lock on another thread.
struct ShutdownSignal {
    scheduler: Arc<CoreScheduler>,
    handle: tokio::runtime::Handle,
}

impl Scheduler {
    /// Build the initial-position value from the string knob (and the parsed
    /// `at_timestamp`, for `AT_TIMESTAMP`).
    fn initial_position(&self) -> PyResult<InitialPositionInStreamExtended> {
        match self.config.initial_position.to_ascii_uppercase().as_str() {
            "LATEST" => Ok(InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::Latest,
            )),
            "TRIM_HORIZON" | "TRIMHORIZON" => {
                Ok(InitialPositionInStreamExtended::new_initial_position(
                    InitialPositionInStream::TrimHorizon,
                ))
            }
            "AT_TIMESTAMP" | "ATTIMESTAMP" => {
                let ts = self.config.at_timestamp.ok_or_else(|| {
                    PyValueError::new_err(
                        "initial_position=\"AT_TIMESTAMP\" requires a `timestamp` argument \
                         (epoch seconds or a datetime)",
                    )
                })?;
                Ok(InitialPositionInStreamExtended::new_initial_position_at_timestamp(ts))
            }
            other => Err(PyValueError::new_err(format!(
                "unsupported initial_position {other:?}; expected LATEST, TRIM_HORIZON, \
                 or AT_TIMESTAMP"
            ))),
        }
    }

    /// Build the tokio runtime, AWS clients, ConfigsBuilder, and the core
    /// Scheduler. Runs with the GIL released. Returns the runtime + scheduler.
    ///
    /// This is the shared heavy-lifting path for both `start` and `run`.
    fn build(&self) -> Result<(tokio::runtime::Runtime, Arc<CoreScheduler>), String> {
        let initial_position = self
            .initial_position()
            .map_err(|e| format!("initial position: {e}"))?;

        // Own the config bits we need across threads.
        let stream_name = self.config.stream_name.clone();
        let stream_identifiers = self.config.stream_identifiers.clone();
        let application_name = self.config.application_name.clone();
        let worker_identifier = self.config.worker_identifier.clone();
        let region = self.config.region.clone();
        let endpoint_url = self.config.endpoint_url.clone();
        let access_key_id = self.config.access_key_id.clone();
        let secret_access_key = self.config.secret_access_key.clone();
        let session_token = self.config.session_token.clone();
        let retrieval_mode = self.config.retrieval_mode.clone();
        let max_records = self.config.max_records;
        let idle_time_between_reads_millis = self.config.idle_time_between_reads_millis;
        let shard_sync_interval_millis = self.config.shard_sync_interval_millis;
        // A separate clone: the tracker-building block below consumes `stream_name`
        // in single-stream mode, but the polling branch also needs it (as the
        // `PollingConfig` stream name).
        let polling_stream_name = self.config.stream_name.clone();

        // The Python factory object is Send (`Py<PyAny>`); clone the handle.
        let py_factory = Python::attach(|py| self.config.factory.clone_ref(py));

        // Multi-thread runtime on its own worker threads.
        let runtime = tokio::runtime::Builder::new_multi_thread()
            .thread_name("kclrs-worker")
            .enable_all()
            .build()
            .map_err(|e| format!("failed to build tokio runtime: {e}"))?;

        // Everything below runs inside the runtime (client construction, the
        // metrics-factory task spawn in `Scheduler::new`, etc.).
        let scheduler = runtime.block_on(async move {
            // AWS config: region + optional endpoint + optional explicit creds.
            let mut loader = aws_config::defaults(aws_config::BehaviorVersion::latest());
            if let Some(region) = region {
                loader = loader.region(aws_config::Region::new(region));
            }
            if let Some(endpoint) = endpoint_url.as_ref() {
                loader = loader.endpoint_url(endpoint.clone());
            }
            // Explicit creds (validated at construction to come together with
            // `secret_access_key`) override the default chain; independent of
            // `endpoint_url` — real AWS callers may want them too.
            if let (Some(key), Some(secret)) = (access_key_id, secret_access_key) {
                loader = loader.credentials_provider(aws_sdk_kinesis::config::Credentials::new(
                    key,
                    secret,
                    session_token,
                    None,
                    "kcl-rs-config",
                ));
            }
            let shared_config = loader.load().await;

            let kinesis_client = aws_sdk_kinesis::Client::new(&shared_config);
            let dynamodb_client = aws_sdk_dynamodb::Client::new(&shared_config);
            let cloudwatch_client = aws_sdk_cloudwatch::Client::new(&shared_config);

            // Stream tracker with the requested initial position: single-stream
            // (a stream name) or multi-stream (a list of serialized identifiers).
            let tracker: Arc<dyn StreamTracker + Send + Sync> = if stream_identifiers.is_empty() {
                let stream_name = stream_name
                    .expect("single-stream mode always has a stream_name (enforced in __new__)");
                Arc::new(SingleStreamTracker::from_stream_name_with_position(
                    &stream_name,
                    initial_position,
                ))
            } else {
                Arc::new(PyMultiStreamTracker::from_serialized(
                    &stream_identifiers,
                    initial_position,
                )?)
            };

            let factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync> =
                Arc::new(PyRecordProcessorFactory::new(py_factory));

            let configs = ConfigsBuilder::new(
                tracker,
                application_name,
                kinesis_client.clone(),
                dynamodb_client,
                cloudwatch_client,
                worker_identifier,
                factory,
            );

            // Retrieval config: fan-out (default) uses `ConfigsBuilder`'s own
            // default; polling wires a `PollingConfig` with the requested knobs
            // (bounds already validated in `new`, so the setters below cannot panic).
            let retrieval_config = if retrieval_mode == "polling" {
                let mut polling = kcl::retrieval::polling::PollingConfig::new(kinesis_client);
                // Stream name only in single-stream mode: `PollingConfig::validate_state`
                // panics if a stream name is set while multi-stream.
                if let Some(name) = polling_stream_name {
                    polling = polling.set_stream_name(name);
                }
                if let Some(v) = max_records {
                    polling = polling.set_max_records(v);
                }
                if let Some(v) = idle_time_between_reads_millis {
                    polling = polling.set_idle_time_between_reads_in_millis(v);
                }
                let mut retrieval_config = configs.retrieval_config();
                retrieval_config.set_retrieval_specific_config(Box::new(polling));
                retrieval_config
            } else {
                configs.retrieval_config()
            };

            // Lease-management config: apply the optional shard-sync interval
            // (defaults to the `LeaseManagementConfig` default of 60000ms).
            let mut lease_management_config = configs.lease_management_config();
            if let Some(v) = shard_sync_interval_millis {
                lease_management_config = lease_management_config.shard_sync_interval_millis_set(v);
            }

            // Materialize the seven sub-configs and construct the core Scheduler.
            CoreScheduler::new(
                configs.checkpoint_config(),
                configs.coordinator_config(),
                lease_management_config,
                configs.lifecycle_config(),
                configs.metrics_config(),
                configs.processor_config(),
                retrieval_config,
            )
            .map_err(|e| format!("Scheduler::new failed: {}", e.0))
        })?;

        Ok((runtime, scheduler))
    }
}

#[pymethods]
impl Scheduler {
    /// Construct a scheduler. Does **no** network I/O and starts no runtime.
    ///
    /// * `stream_name` — the Kinesis stream to consume.
    /// * `application_name` — the KCL application name (also the default lease
    ///   table name and CloudWatch namespace).
    /// * `record_processor_factory` — a Python callable (or object with a
    ///   `shard_record_processor()` method) returning a fresh `RecordProcessor`
    ///   per shard.
    /// * `worker_identifier` — a unique id for this worker (defaults to a uuid).
    /// * `region` — AWS region (e.g. `"us-east-1"`).
    /// * `endpoint_url` — override endpoint for LocalStack (e.g.
    ///   `"http://localhost:4566"`).
    /// * `initial_position` — `"LATEST"` (default), `"TRIM_HORIZON"`, or
    ///   `"AT_TIMESTAMP"` (which requires `timestamp`).
    /// * `timestamp` — required only for `initial_position="AT_TIMESTAMP"`:
    ///   either epoch seconds (an `int`/`float`) or a Python `datetime` (naive
    ///   datetimes are interpreted as UTC).
    /// * `stream_identifiers` — for **multi-stream** mode: a list of serialized
    ///   multi-stream identifiers of the form
    ///   `"accountId:streamName:creationEpoch"`. Mutually exclusive with
    ///   `stream_name`; exactly one of the two must be provided.
    /// * `access_key_id` / `secret_access_key` / `session_token` — explicit
    ///   static credentials (e.g. for a LocalStack account other than the
    ///   ambient one). `access_key_id` and `secret_access_key` must be given
    ///   together; `session_token` requires both. When omitted, the standard
    ///   AWS credential chain (env vars, profile, IMDS, …) is used — prefer
    ///   that over passing static credentials where possible.
    /// * `retrieval_mode` — `"FANOUT"` (default, matching Java KCL 2.x/3.x) or
    ///   `"POLLING"`, case-insensitive. Fan-out subscribes via `SubscribeToShard`
    ///   (EFO); polling uses classic `GetRecords` through the prefetch publisher.
    ///   Unlike the Java multilang daemon's `RetrievalMode`, there is no
    ///   `DEFAULT` auto-detect variant — the mode is always explicit.
    /// * `max_records` / `idle_time_between_reads_millis` — polling-only knobs
    ///   mirroring Java `PollingConfig`'s `maxRecords` / `idleTimeBetweenReadsInMillis`;
    ///   passing either with `retrieval_mode` other than `"POLLING"` is a
    ///   `ValueError`. `max_records` must be `<= 10000` (validated here, same
    ///   bound `PollingConfig::set_max_records` panics on) — an out-of-range
    ///   value is a `ValueError` at construction rather than a crash at
    ///   `start()`/`run()`. `idle_time_between_reads_millis` below 200ms is
    ///   silently clamped up to 200ms by `PollingConfig` (a warning is logged,
    ///   not an error).
    /// * `shard_sync_interval_millis` — mirrors Java
    ///   `LeaseManagementConfig`'s `shardSyncIntervalMillis`: the interval
    ///   between periodic shard syncs. Applies to both retrieval modes. `None`
    ///   uses the default (60000ms).
    #[new]
    #[pyo3(signature = (
        stream_name=None,
        application_name=String::new(),
        record_processor_factory=None,
        worker_identifier=None,
        region=None,
        endpoint_url=None,
        initial_position="LATEST".to_string(),
        timestamp=None,
        stream_identifiers=None,
        access_key_id=None,
        secret_access_key=None,
        session_token=None,
        retrieval_mode="FANOUT".to_string(),
        max_records=None,
        idle_time_between_reads_millis=None,
        shard_sync_interval_millis=None,
    ))]
    #[allow(clippy::too_many_arguments)]
    fn new(
        py: Python<'_>,
        stream_name: Option<String>,
        application_name: String,
        record_processor_factory: Option<Py<PyAny>>,
        worker_identifier: Option<String>,
        region: Option<String>,
        endpoint_url: Option<String>,
        initial_position: String,
        timestamp: Option<Py<PyAny>>,
        stream_identifiers: Option<Vec<String>>,
        access_key_id: Option<String>,
        secret_access_key: Option<String>,
        session_token: Option<String>,
        retrieval_mode: String,
        max_records: Option<i32>,
        idle_time_between_reads_millis: Option<i64>,
        shard_sync_interval_millis: Option<i64>,
    ) -> PyResult<Self> {
        // `application_name` and `record_processor_factory` are logically
        // required; they carry defaults only so the multi-stream `stream_name`
        // can be optional (PyO3 requires optional-then-defaulted ordering).
        if application_name.is_empty() {
            return Err(PyValueError::new_err("application_name is required"));
        }
        let record_processor_factory = record_processor_factory
            .ok_or_else(|| PyValueError::new_err("record_processor_factory is required"))?;

        // Exactly one of `stream_name` / `stream_identifiers` must be provided.
        let stream_identifiers = stream_identifiers.unwrap_or_default();
        match (&stream_name, stream_identifiers.is_empty()) {
            (Some(_), false) => {
                return Err(PyValueError::new_err(
                    "provide either stream_name (single-stream) or stream_identifiers \
                     (multi-stream), not both",
                ))
            }
            (None, true) => {
                return Err(PyValueError::new_err(
                    "one of stream_name (single-stream) or stream_identifiers \
                     (multi-stream) is required",
                ))
            }
            _ => {}
        }

        // Parse the optional AT_TIMESTAMP value eagerly (so a bad value fails at
        // construction, not later at start()).
        let at_timestamp = match timestamp {
            Some(ts) => Some(parse_timestamp(ts.bind(py))?),
            None => None,
        };

        // Explicit credentials must be internally consistent: key+secret come
        // together, and a session token requires both (it is meaningless alone).
        if access_key_id.is_some() != secret_access_key.is_some() {
            return Err(PyValueError::new_err(
                "access_key_id and secret_access_key must be provided together",
            ));
        }
        if session_token.is_some() && (access_key_id.is_none() || secret_access_key.is_none()) {
            return Err(PyValueError::new_err(
                "session_token requires access_key_id and secret_access_key",
            ));
        }

        // `retrieval_mode` mirrors the Java multilang daemon's `RetrievalMode`
        // property, minus its `DEFAULT` auto-detect variant (this API is always
        // explicit). Case-insensitive; normalized to lowercase for `build()`.
        let retrieval_mode = match retrieval_mode.to_ascii_uppercase().as_str() {
            "FANOUT" => "fanout".to_string(),
            "POLLING" => "polling".to_string(),
            other => {
                return Err(PyValueError::new_err(format!(
                    "unknown retrieval_mode {other:?}; available retrieval modes: FANOUT, POLLING"
                )))
            }
        };

        // `max_records` / `idle_time_between_reads_millis` only mean anything
        // for polling retrieval.
        if retrieval_mode != "polling"
            && (max_records.is_some() || idle_time_between_reads_millis.is_some())
        {
            return Err(PyValueError::new_err(
                "max_records and idle_time_between_reads_millis require retrieval_mode=\"POLLING\"",
            ));
        }

        // Pre-validate the bound `PollingConfig::set_max_records` panics on, so
        // a bad value fails here as a ValueError instead of surfacing as a
        // PanicException at start()/run(). (`idleTimeBetweenReadsInMillis` has
        // no such panic — `PollingConfig` clamps it to a 200ms floor instead.)
        if let Some(v) = max_records {
            let limit = kcl::retrieval::polling::polling_config::DEFAULT_MAX_RECORDS;
            if v > limit {
                return Err(PyValueError::new_err(format!(
                    "max_records must be less than or equal to {limit} but current value is {v}"
                )));
            }
        }

        let identity_hint = stream_name
            .clone()
            .unwrap_or_else(|| stream_identifiers.join(","));
        let worker_identifier = worker_identifier
            .unwrap_or_else(|| format!("kclrs-{}", uuid_like(&identity_hint, &application_name)));
        Ok(Scheduler {
            config: SchedulerConfig {
                stream_name,
                stream_identifiers,
                application_name,
                worker_identifier,
                factory: record_processor_factory,
                region,
                endpoint_url,
                initial_position,
                at_timestamp,
                access_key_id,
                secret_access_key,
                session_token,
                retrieval_mode,
                max_records,
                idle_time_between_reads_millis,
                shard_sync_interval_millis,
            },
            state: Mutex::new(None),
            signal: Mutex::new(None),
        })
    }

    /// Start the scheduler in the background and return immediately.
    ///
    /// Builds the tokio runtime + AWS clients + core scheduler (GIL released),
    /// then spawns the scheduler's run loop on the runtime's own threads. After
    /// this returns, the KCL runs GIL-free; callbacks re-acquire the GIL only
    /// transiently. Call [`shutdown`](Self::shutdown) to stop.
    fn start(&self, py: Python<'_>) -> PyResult<()> {
        if self.signal.lock().unwrap().is_some() {
            return Err(PyRuntimeError::new_err("scheduler already started"));
        }
        // Build with the GIL released — the factory clone briefly re-acquires it.
        let built = py.detach(|| self.build());
        let (runtime, scheduler) = built.map_err(PyRuntimeError::new_err)?;

        // Spawn the run loop on the runtime (returns a JoinHandle immediately).
        // `CoreScheduler::start` uses `tokio::spawn`, so this thread must be
        // inside the runtime's context for the spawn.
        let join_handle = {
            let _guard = runtime.enter();
            scheduler.start()
        };

        *self.signal.lock().unwrap() = Some(ShutdownSignal {
            scheduler: Arc::clone(&scheduler),
            handle: runtime.handle().clone(),
        });
        let mut guard = self.state.lock().unwrap();
        *guard = Some(RunningState {
            runtime: Some(runtime),
            scheduler,
            join_handle: Some(join_handle),
        });
        Ok(())
    }

    /// Build and drive the scheduler, **blocking** the calling Python thread
    /// until the scheduler shuts down.
    ///
    /// The run loop executes on the runtime's own threads; this thread waits
    /// for it in ~100ms slices with the GIL released, re-attaching between
    /// slices to deliver pending Python signals. CPython only dispatches signal
    /// handlers on the main thread while it is running Python code, so without
    /// this polling Ctrl-C would be deferred for the entire run. A pending
    /// `KeyboardInterrupt` (or any exception raised by a user signal handler)
    /// triggers a **graceful shutdown** and is then re-raised to the caller.
    /// Alternatively, another thread may call [`shutdown`](Self::shutdown).
    ///
    /// If the scheduler run loop itself crashes (e.g. the record-processor
    /// factory raised), this raises `RuntimeError` instead of returning
    /// silently.
    fn run(&self, py: Python<'_>) -> PyResult<()> {
        if self.signal.lock().unwrap().is_some() {
            return Err(PyRuntimeError::new_err("scheduler already started"));
        }
        let built = py.detach(|| self.build());
        let (runtime, scheduler) = built.map_err(PyRuntimeError::new_err)?;

        // Publish a shutdown signal handle so `shutdown()` (possibly from another
        // thread / signal handler) can stop us without touching `state`.
        *self.signal.lock().unwrap() = Some(ShutdownSignal {
            scheduler: Arc::clone(&scheduler),
            handle: runtime.handle().clone(),
        });

        // Spawn the run loop on the runtime's own threads. We keep `runtime`
        // and `scheduler` as locals (NOT in the `state` lock) so `shutdown()`
        // never blocks on a lock this thread holds.
        let mut join_handle = {
            let _guard = runtime.enter();
            scheduler.start()
        };

        let result = loop {
            // Wait one slice with the GIL released.
            let joined = py.detach(|| {
                runtime.block_on(async {
                    tokio::select! {
                        joined = &mut join_handle => Some(joined),
                        _ = tokio::time::sleep(std::time::Duration::from_millis(100)) => None,
                    }
                })
            });
            match joined {
                Some(joined) => break join_result_to_py(joined),
                None => {
                    // GIL re-acquired: deliver pending Python signals on this
                    // (typically main) thread. The default SIGINT handler
                    // raises KeyboardInterrupt here; a user-installed handler
                    // runs here too and surfaces the same way if it raises.
                    if let Err(signal_exc) = py.check_signals() {
                        let scheduler = Arc::clone(&scheduler);
                        let joined = py.detach(|| {
                            runtime.block_on(async move {
                                scheduler.shutdown().await;
                            });
                            runtime.block_on(&mut join_handle)
                        });
                        // The signal exception is the primary outcome; a crash
                        // during the interrupted teardown is secondary.
                        let _ = join_result_to_py(joined);
                        break Err(signal_exc);
                    }
                }
            }
        };
        // Run finished (shutdown completed); clear the signal.
        *self.signal.lock().unwrap() = None;
        // Tear the runtime down with the GIL released: the (blocking) drop
        // waits for in-flight callbacks, which may need the GIL to finish.
        py.detach(|| drop(runtime));
        result
    }

    /// Initiate a graceful shutdown and block until the scheduler has stopped.
    ///
    /// Works whether the scheduler was launched via [`start`](Self::start)
    /// (background) or [`run`](Self::run) (blocking on another Python thread),
    /// and may be called from **any** thread (the pyclass is sendable). A no-op
    /// if the scheduler was never started. The GIL is released while awaiting
    /// shutdown. Raises `RuntimeError` if the run loop had crashed.
    fn shutdown(&self, py: Python<'_>) -> PyResult<()> {
        // If `start()` owns the runtime + join handle, take and drive them here.
        let owned_state = self.state.lock().unwrap().take();

        if let Some(mut state) = owned_state {
            // Background (`start`) path: we own the runtime — drive shutdown and
            // join the run loop, then drop the runtime, all off the GIL.
            // (Fields are `take`n out because `RunningState` has a `Drop` impl;
            // with the runtime taken, that drop is a no-op.)
            let runtime = state
                .runtime
                .take()
                .expect("runtime is present until RunningState drops");
            let scheduler = Arc::clone(&state.scheduler);
            let join_handle = state.join_handle.take();
            drop(state);
            let joined = py.detach(|| {
                let joined = runtime.block_on(async move {
                    scheduler.shutdown().await;
                    match join_handle {
                        Some(handle) => handle.await,
                        None => Ok(()),
                    }
                });
                drop(runtime);
                joined
            });
            *self.signal.lock().unwrap() = None;
            // Surface a crashed run loop (e.g. a factory that raised) instead
            // of swallowing it.
            return join_result_to_py(joined);
        }

        // Blocking (`run`) path: the run thread owns the runtime and is blocked
        // in `block_on(run())`. Signal shutdown via the runtime handle; the run
        // thread's `block_on` returns once shutdown completes.
        let signal = self.signal.lock().unwrap().take();
        let Some(ShutdownSignal { scheduler, handle }) = signal else {
            return Ok(()); // never started (or already shut down)
        };
        py.detach(|| {
            // `block_on` here would panic (we may be inside/next to a runtime);
            // use the handle to spawn the async shutdown and wait via a channel.
            let (tx, rx) = std::sync::mpsc::channel();
            handle.spawn(async move {
                scheduler.shutdown().await;
                let _ = tx.send(());
            });
            // Wait for shutdown to be signalled (the run loop then unblocks).
            let _ = rx.recv();
        });
        Ok(())
    }

    fn __repr__(&self) -> String {
        match &self.config.stream_name {
            Some(stream_name) => format!(
                "Scheduler(stream_name={:?}, application_name={:?}, worker_identifier={:?})",
                stream_name, self.config.application_name, self.config.worker_identifier
            ),
            None => format!(
                "Scheduler(stream_identifiers={:?}, application_name={:?}, worker_identifier={:?})",
                self.config.stream_identifiers,
                self.config.application_name,
                self.config.worker_identifier
            ),
        }
    }
}

/// Map the run-loop `JoinHandle` outcome to Python: a clean exit (or a
/// cancellation during teardown) is `Ok(())`; a panic inside the scheduler
/// (e.g. a record-processor factory that raised at wiring time) surfaces as a
/// `RuntimeError` instead of being silently swallowed.
fn join_result_to_py(joined: Result<(), tokio::task::JoinError>) -> PyResult<()> {
    match joined {
        Ok(()) => Ok(()),
        Err(e) if e.is_cancelled() => Ok(()),
        Err(e) => Err(PyRuntimeError::new_err(format!(
            "KCL scheduler run loop crashed: {e}"
        ))),
    }
}

/// Parse the Python `timestamp` argument for `AT_TIMESTAMP` into a UTC datetime.
///
/// Accepts either:
/// * a number (`int`/`float`) — epoch **seconds** (fractional seconds allowed), or
/// * a Python `datetime.datetime` — timezone-aware values are converted to UTC;
///   naive values are interpreted as UTC (matching Kinesis's server-side clock).
pub(crate) fn parse_timestamp(ts: &Bound<'_, PyAny>) -> PyResult<DateTime<Utc>> {
    // datetime first (a datetime is not an int, but is truthy for float() coercion).
    if let Ok(dt) = ts.cast::<PyDateTime>() {
        // PyO3's chrono feature converts an aware datetime directly; a naive
        // datetime is interpreted as UTC.
        if let Ok(aware) = dt.extract::<DateTime<Utc>>() {
            return Ok(aware);
        }
        let naive = dt.extract::<chrono::NaiveDateTime>()?;
        return Ok(Utc.from_utc_datetime(&naive));
    }
    // Otherwise treat it as epoch seconds (int or float).
    let secs: f64 = ts.extract().map_err(|_| {
        PyValueError::new_err("timestamp must be epoch seconds (int/float) or a datetime.datetime")
    })?;
    let whole = secs.trunc() as i64;
    let nanos = ((secs - secs.trunc()) * 1_000_000_000.0).round() as u32;
    Utc.timestamp_opt(whole, nanos)
        .single()
        .ok_or_else(|| PyValueError::new_err(format!("timestamp {secs} is out of range")))
}

/// A tiny, dependency-free pseudo-unique suffix for a default worker id (we
/// avoid pulling `uuid` into the bindings crate just for a default).
fn uuid_like(a: &str, b: &str) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    use std::time::{SystemTime, UNIX_EPOCH};
    let mut h = DefaultHasher::new();
    a.hash(&mut h);
    b.hash(&mut h);
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_nanos())
        .unwrap_or(0)
        .hash(&mut h);
    format!("{:016x}", h.finish())
}
