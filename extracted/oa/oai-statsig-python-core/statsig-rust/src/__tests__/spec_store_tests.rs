use std::collections::HashMap;
use std::io::Write;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{mpsc, Arc};
use std::time::Duration;

use async_trait::async_trait;
use brotli::enc::BrotliEncoderParams;
use parking_lot::Mutex;
use prost::Message;
use serial_test::serial;

use crate::{
    data_store_interface::{DataStoreResponse, DataStoreTrait, RequestPath},
    id_lists_adapter::{IdListMetadata, IdListUpdate, IdListsUpdateListener},
    networking::ResponseData,
    observability::{
        observability_client_adapter::MetricType,
        ops_stats::{OpsStatsEvent, OPS_STATS},
    },
    output_logger::{
        initialize_output_logger, shutdown_output_logger, LogLevel, OutputLogProvider,
    },
    sdk_event_emitter::{SdkEvent, SdkEventEmitter},
    specs_response::{spec_types::SpecsResponseFull, statsig_config_specs as pb},
    ClientInitResponseOptions, FeatureGateEvaluationOptions, GCIRResponseFormat, SpecStore,
    SpecsSource, SpecsUpdate, SpecsUpdateListener, Statsig, StatsigErr, StatsigOptions,
    StatsigRuntime, StatsigUser,
};

struct TestDataStore {
    get_response: Mutex<Option<DataStoreResponse>>,
    supports_polling: bool,
    set_bytes_error: Option<&'static str>,
    calls: Mutex<Vec<(String, Option<String>)>>,
}

#[derive(Clone, Debug, PartialEq)]
enum RecordedLog {
    Warn(String, String),
    Init,
    Shutdown,
}

struct TestLogProvider {
    logs: Mutex<Vec<RecordedLog>>,
}

impl TestLogProvider {
    fn new() -> Self {
        Self {
            logs: Mutex::new(Vec::new()),
        }
    }
}

impl TestDataStore {
    fn new(supports_polling: bool) -> Self {
        Self {
            get_response: Mutex::new(None),
            supports_polling,
            set_bytes_error: None,
            calls: Mutex::new(vec![]),
        }
    }

    fn new_with_set_bytes_failure(supports_polling: bool) -> Self {
        Self {
            set_bytes_error: Some("set_bytes failed"),
            ..Self::new(supports_polling)
        }
    }
}

#[async_trait]
impl DataStoreTrait for TestDataStore {
    async fn initialize(&self) -> Result<(), StatsigErr> {
        self.calls.lock().push(("initialize".to_string(), None));
        Ok(())
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        self.calls.lock().push(("shutdown".to_string(), None));
        Ok(())
    }

    async fn get(&self, key: &str) -> Result<DataStoreResponse, StatsigErr> {
        self.calls
            .lock()
            .push(("get".to_string(), Some(key.to_string())));

        let mut lock = self.get_response.lock();
        lock.take()
            .ok_or(StatsigErr::DataStoreFailure("Failed to get".to_string()))
    }

    async fn set(&self, key: &str, value: &str, time: Option<u64>) -> Result<(), StatsigErr> {
        self.calls
            .lock()
            .push(("set".to_string(), Some(format!("{key}:{value}:{time:?}"))));
        Ok(())
    }

    async fn set_bytes(
        &self,
        key: &str,
        value: &[u8],
        time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<(), StatsigErr> {
        self.calls.lock().push((
            "set_bytes".to_string(),
            Some(format!("{key}:{}:{time:?}:{checksum:?}", value.len())),
        ));

        match self.set_bytes_error {
            Some(message) => Err(StatsigErr::DataStoreFailure(message.to_string())),
            None => Err(StatsigErr::BytesNotImplemented),
        }
    }

    async fn support_polling_updates_for(&self, path: RequestPath) -> bool {
        self.calls.lock().push((
            "support_polling_updates_for".to_string(),
            Some(path.to_string()),
        ));
        self.supports_polling
    }
}

impl OutputLogProvider for TestLogProvider {
    fn initialize(&self) {
        self.logs.lock().push(RecordedLog::Init);
    }

    fn debug(&self, _tag: &str, _msg: String) {}

    fn info(&self, _tag: &str, _msg: String) {}

    fn warn(&self, tag: &str, msg: String) {
        self.logs
            .lock()
            .push(RecordedLog::Warn(tag.to_string(), msg));
    }

    fn error(&self, _tag: &str, _msg: String) {}

    fn shutdown(&self) {
        self.logs.lock().push(RecordedLog::Shutdown);
    }
}

#[derive(Default)]
struct DeltaOverrides {
    deletions: pb::RulesetsResponseDeletions,
    corrupt_checksums: bool,
}

fn apply_eval_project(spec_store: &SpecStore) {
    spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(
                include_bytes!("../../tests/data/eval_proj_dcs.json").to_vec(),
            ),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: Some("initial".to_string()),
            has_updates: None,
        })
        .unwrap();
}

fn initialized_spec_store(name: &str) -> SpecStore {
    let spec_store = SpecStore::new(
        name,
        name.to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    apply_eval_project(&spec_store);
    spec_store
}

fn common_fields_json(values: &SpecsResponseFull) -> serde_json::Value {
    let mut json = serde_json::to_value(values).unwrap();
    let fields = json.as_object_mut().unwrap();
    for field in [
        "checksum",
        "company_id",
        "condition_map",
        "dynamic_configs",
        "feature_gates",
        "has_updates",
        "layer_configs",
        "param_stores",
        "response_format",
        "time",
    ] {
        fields.remove(field);
    }
    json
}

fn empty_field_checksums() -> HashMap<String, u64> {
    HashMap::from([
        ("condition_map".to_string(), 0),
        ("dynamic_configs".to_string(), 0),
        ("feature_gates".to_string(), 0),
        ("layer_configs".to_string(), 0),
        ("param_stores".to_string(), 0),
    ])
}

fn proto_headers(lcut: u64, checksum: &str) -> HashMap<String, String> {
    HashMap::from([
        (
            "content-type".to_string(),
            "application/octet-stream".to_string(),
        ),
        ("content-encoding".to_string(), "statsig-br".to_string()),
        ("x-since-time".to_string(), lcut.to_string()),
        ("x-checksum".to_string(), checksum.to_string()),
    ])
}

fn protobuf_delta(
    values: &SpecsResponseFull,
    lcut: u64,
    checksum: &str,
    overrides: DeltaOverrides,
) -> ResponseData {
    let DeltaOverrides {
        deletions,
        corrupt_checksums,
    } = overrides;
    let top_level = pb::SpecsTopLevel {
        has_updates: true,
        time: lcut,
        company_id: values.company_id.clone().unwrap_or_default(),
        response_format: values.response_format.clone().unwrap_or_default(),
        checksum: checksum.to_string(),
        rest: serde_json::to_vec(&common_fields_json(values)).unwrap(),
    };
    let mut checksums = empty_field_checksums();
    if corrupt_checksums {
        *checksums.get_mut("dynamic_configs").unwrap() += 1;
    }

    let envelopes = [
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(top_level.encode_to_vec()),
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Deletions as i32,
            data: Some(deletions.encode_to_vec()),
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Checksums as i32,
            data: Some(
                pb::RulesetsChecksums {
                    field_checksums: checksums,
                }
                .encode_to_vec(),
            ),
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Done as i32,
            ..pb::SpecsEnvelope::default()
        },
    ];

    let mut encoded = Vec::new();
    for envelope in envelopes {
        envelope.encode_length_delimited(&mut encoded).unwrap();
    }

    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::with_params(
            &mut compressed,
            crate::specs_response::proto_stream_reader::BUFFER_SIZE,
            &BrotliEncoderParams::default(),
        );
        writer.write_all(&encoded).unwrap();
        writer.flush().unwrap();
    }

    ResponseData::from_bytes_with_headers(
        compressed,
        Some(HashMap::from([
            (
                "content-type".to_string(),
                "application/octet-stream".to_string(),
            ),
            ("content-encoding".to_string(), "statsig-br".to_string()),
        ])),
    )
}

fn apply_delta(
    spec_store: &SpecStore,
    data: ResponseData,
    source: SpecsSource,
    source_api: &str,
) -> Result<(), StatsigErr> {
    spec_store.set_values(SpecsUpdate {
        data,
        source,
        received_at: 3000,
        source_api: Some(source_api.to_string()),
        has_updates: None,
    })
}

async fn receive_proto_outcome(
    receiver: &mut tokio::sync::broadcast::Receiver<OpsStatsEvent>,
    timeout: Duration,
) -> Option<String> {
    tokio::time::timeout(timeout, async {
        loop {
            let OpsStatsEvent::Observability(event) = receiver.recv().await.ok()? else {
                continue;
            };
            if event.metric_name == "config_proto_update.count" {
                return event.tags.and_then(|mut tags| tags.remove("outcome"));
            }
        }
    })
    .await
    .ok()
    .flatten()
}

async fn receive_proto_latency(
    receiver: &mut tokio::sync::broadcast::Receiver<OpsStatsEvent>,
    timeout: Duration,
) -> Option<(String, f64)> {
    tokio::time::timeout(timeout, async {
        loop {
            let OpsStatsEvent::Observability(event) = receiver.recv().await.ok()? else {
                continue;
            };
            if event.metric_name == "config_proto_update.latency" {
                assert!(matches!(&event.metric_type, MetricType::Dist));
                let outcome = event.tags?.remove("outcome")?;
                return Some((outcome, event.value));
            }
        }
    })
    .await
    .ok()
    .flatten()
}

#[tokio::test]
async fn test_spec_store_data_store_updates_forwarded_to_data_store() {
    let data_store = Arc::new(TestDataStore::new(true));

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };

    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(contents.to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok());

    // data store updates are async, so we need to wait for them to complete
    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    let calls = data_store.calls.lock();

    assert_eq!(calls.len(), 2);
    assert_eq!(calls[0].0, "set_bytes");
    assert_eq!(calls[1].0, "set");

    let bytes_call_value = calls[0].1.as_ref().unwrap();
    assert!(bytes_call_value.starts_with("test:"));

    let call_value = calls[1].1.as_ref().unwrap();
    assert!(call_value.len() > 100);
    assert!(call_value.contains("\"feature_gates\""));
}

#[tokio::test]
async fn test_spec_store_data_store_string_fallback_requires_bytes_not_implemented() {
    let data_store = Arc::new(TestDataStore::new_with_set_bytes_failure(true));

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };

    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(contents.to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok());

    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    let calls = data_store.calls.lock();

    assert_eq!(calls.len(), 1);
    assert_eq!(calls[0].0, "set_bytes");
}

#[tokio::test]
async fn test_spec_store_skips_data_store_write_for_delta_responses() {
    let data_store = Arc::new(TestDataStore::new(true));

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };

    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes_with_headers(
            contents.to_vec(),
            Some(HashMap::from([(
                "x-deltas-used".to_string(),
                "true".to_string(),
            )])),
        ),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok());

    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    let calls = data_store.calls.lock();

    assert!(calls.is_empty());
}

#[tokio::test]
#[serial]
async fn test_spec_store_proto_bytes_warning_requires_polling_support() {
    let provider = Arc::new(TestLogProvider::new());
    initialize_output_logger(&Some(LogLevel::Debug), Some(provider.clone()));

    for supports_polling in [false, true] {
        provider.logs.lock().clear();

        let data_store = Arc::new(TestDataStore::new(supports_polling));
        let options = StatsigOptions {
            data_store: Some(data_store),
            ..StatsigOptions::default()
        };

        let spec_store = SpecStore::new(
            "test",
            "test".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            Some(&options),
        );

        let contents = include_bytes!("../../tests/data/eval_proj_dcs.pb.br");
        let update_result = spec_store.set_values(SpecsUpdate {
            data: ResponseData::from_bytes_with_headers(
                contents.to_vec(),
                Some(HashMap::from([
                    (
                        "content-type".to_string(),
                        "application/octet-stream".to_string(),
                    ),
                    ("content-encoding".to_string(), "statsig-br".to_string()),
                ])),
            ),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: None,
            has_updates: None,
        });

        assert!(update_result.is_ok());
        tokio::time::sleep(std::time::Duration::from_millis(100)).await;

        let logged_warning = provider.logs.lock().iter().any(|log| {
            matches!(
                log,
                RecordedLog::Warn(_, msg)
                    if msg.contains(
                        "Failed to write protobuf specs to data store as bytes. Protobuf specs cannot fall back to string writes"
                    )
            )
        });

        assert_eq!(logged_warning, supports_polling);
    }

    shutdown_output_logger();
}

#[test]
fn test_failure_to_update() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(b"test".to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_err())
}

#[test]
fn test_no_updates() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(b"{\"has_updates\": false}".to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok())
}

#[test]
fn test_no_updates_update_field_short_circuit_parse() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(b"invalid".to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: Some(false),
    });

    assert!(update_result.is_ok())
}

#[test]
fn test_spec_store_published_snapshots_preserve_id_lists_and_source() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(contents.to_vec()),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: None,
            has_updates: None,
        })
        .unwrap();

    spec_store.did_receive_id_list_updates(HashMap::from([(
        "employees".to_string(),
        IdListUpdate {
            raw_changeset: Some("+alice\n+bob".to_string()),
            new_metadata: IdListMetadata {
                name: "employees".to_string(),
                url: "https://example.com/employees".to_string(),
                file_id: Some("file-1".to_string()),
                size: 0,
                creation_time: 1,
            },
        },
    )]));

    spec_store.set_source(SpecsSource::Bootstrap);

    let metadata = spec_store.get_current_id_list_metadata();
    assert!(metadata.contains_key("employees"));
    assert_eq!(
        spec_store.get_current_specs_info().source,
        SpecsSource::Bootstrap
    );

    let mut demo_json: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/demo_proj_dcs.json")).unwrap();
    demo_json["time"] = serde_json::json!(9_999_999_999_999_u64);
    demo_json["checksum"] = serde_json::json!("snapshot-preservation-test");
    spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&demo_json).unwrap()),
            source: SpecsSource::Network,
            received_at: 3000,
            source_api: None,
            has_updates: None,
        })
        .unwrap();

    let metadata = spec_store.get_current_id_list_metadata();
    assert!(metadata.contains_key("employees"));
    assert_eq!(
        spec_store.get_current_specs_info().source,
        SpecsSource::Network
    );
}

#[test]
fn test_specs_updated_callback_runs_without_holding_store_lock() {
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let spec_store = Arc::new(SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        event_emitter.clone(),
        None,
    ));
    let callback_store = spec_store.clone();

    event_emitter.subscribe(SdkEvent::SPECS_UPDATED, move |event| {
        let SdkEvent::SpecsUpdated { source, values, .. } = event else {
            panic!("expected a specs updated event");
        };
        assert_eq!(source, &SpecsSource::Network);
        assert!(values.time > 0);

        callback_store.set_source(SpecsSource::Bootstrap);
    });

    let (completed_tx, completed_rx) = mpsc::channel();
    std::thread::spawn(move || {
        let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
        let result = spec_store.set_values(SpecsUpdate {
            data: ResponseData::from_bytes(contents.to_vec()),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: None,
            has_updates: None,
        });
        completed_tx.send(result).unwrap();
    });

    let result = completed_rx
        .recv_timeout(Duration::from_millis(500))
        .expect("specs updated callback deadlocked while re-entering the spec store");
    assert!(result.is_ok());
}

#[test]
#[serial]
fn test_checksum_only_delta_reuses_snapshot_and_suppresses_side_effects() {
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let specs_updated = Arc::new(AtomicUsize::new(0));
    let internal_configs_updated = Arc::new(AtomicUsize::new(0));
    let data_store = Arc::new(TestDataStore::new(true));
    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };
    let spec_store = SpecStore::new(
        "cursor-only-test",
        "cursor-only-test".to_string(),
        StatsigRuntime::get_runtime(),
        event_emitter.clone(),
        Some(&options),
    );
    spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(
                include_bytes!("../../tests/data/eval_proj_dcs.json").to_vec(),
            ),
            source: SpecsSource::Bootstrap,
            received_at: 2000,
            source_api: Some("initial".to_string()),
            has_updates: None,
        })
        .unwrap();

    let specs_updated_for_callback = specs_updated.clone();
    event_emitter.subscribe(SdkEvent::SPECS_UPDATED, move |_| {
        specs_updated_for_callback.fetch_add(1, Ordering::Relaxed);
    });
    let internal_configs_for_callback = internal_configs_updated.clone();
    event_emitter.subscribe(SdkEvent::INTERNAL_SDK_CONFIGS_UPDATED, move |_| {
        internal_configs_for_callback.fetch_add(1, Ordering::Relaxed);
    });

    let before = spec_store.load_data();
    let next_lcut = before.lcut() + 1;
    apply_delta(
        &spec_store,
        protobuf_delta(
            &before.snapshot,
            next_lcut,
            "cursor-only-checksum",
            DeltaOverrides::default(),
        ),
        SpecsSource::Network,
        "cursor-only-api",
    )
    .unwrap();

    let after = spec_store.load_data();
    assert!(Arc::ptr_eq(&before.snapshot, &after.snapshot));
    assert_eq!(after.lcut(), next_lcut);
    assert_eq!(after.source, SpecsSource::Network);
    assert_eq!(after.source_api.as_deref(), Some("cursor-only-api"));
    assert!(after.time_received_at >= before.time_received_at);
    assert_eq!(specs_updated.load(Ordering::Relaxed), 0);
    assert_eq!(internal_configs_updated.load(Ordering::Relaxed), 0);
    assert!(data_store.calls.lock().is_empty());

    let public_values = spec_store.get_current_values().unwrap();
    assert_eq!(public_values.time, next_lcut);
    assert_eq!(
        public_values.checksum.as_deref(),
        Some("cursor-only-checksum")
    );
    assert_eq!(
        public_values.feature_gates.len(),
        before.snapshot.feature_gates.len()
    );
}

#[tokio::test]
#[serial]
async fn test_proto_metrics_classify_processing_and_duplicates() {
    let sdk_instance_id = "proto-outcome-metric-test";
    let ops_stats = OPS_STATS.get_for_instance(sdk_instance_id);
    let mut receiver = ops_stats.subscribe_for_test();
    let mut latency_receiver = ops_stats.subscribe_for_test();

    let full_store = SpecStore::new(
        sdk_instance_id,
        "proto-full-test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    full_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes_with_headers(
                include_bytes!("../../tests/data/eval_proj_dcs.pb.br").to_vec(),
                Some(HashMap::from([
                    (
                        "content-type".to_string(),
                        "application/octet-stream".to_string(),
                    ),
                    ("content-encoding".to_string(), "statsig-br".to_string()),
                ])),
            ),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    assert_eq!(
        receive_proto_outcome(&mut receiver, Duration::from_millis(100)).await,
        None
    );
    assert_eq!(
        receive_proto_latency(&mut latency_receiver, Duration::from_millis(100)).await,
        None
    );

    let current = full_store.get_current_specs_info();
    full_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes_with_headers(
                b"body should not be decoded".to_vec(),
                Some(proto_headers(
                    current.lcut.unwrap(),
                    current.checksum.as_deref().unwrap(),
                )),
            ),
            source: SpecsSource::Network,
            received_at: 2001,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    assert_eq!(
        receive_proto_outcome(&mut receiver, Duration::from_secs(1)).await,
        Some("duplicate".to_string())
    );
    assert_eq!(
        receive_proto_latency(&mut latency_receiver, Duration::from_millis(100)).await,
        None
    );

    let delta_store = SpecStore::new(
        sdk_instance_id,
        "proto-delta-test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    apply_eval_project(&delta_store);
    let before = delta_store.load_data();
    let deleted_name = before
        .snapshot
        .dynamic_configs
        .keys()
        .next()
        .unwrap()
        .as_str()
        .to_string();
    apply_delta(
        &delta_store,
        protobuf_delta(
            &before.snapshot,
            before.lcut() + 1,
            "materialized-delta",
            DeltaOverrides {
                deletions: pb::RulesetsResponseDeletions {
                    dynamic_configs: vec![deleted_name],
                    ..pb::RulesetsResponseDeletions::default()
                },
                ..DeltaOverrides::default()
            },
        ),
        SpecsSource::Network,
        "metric-api",
    )
    .unwrap();
    let materialized = delta_store.load_data();
    apply_delta(
        &delta_store,
        protobuf_delta(
            &materialized.snapshot,
            materialized.lcut() + 1,
            "cursor-only-delta",
            DeltaOverrides::default(),
        ),
        SpecsSource::Network,
        "metric-api",
    )
    .unwrap();

    assert_eq!(
        receive_proto_outcome(&mut receiver, Duration::from_secs(1)).await,
        Some("materialized".to_string())
    );
    assert_eq!(
        receive_proto_outcome(&mut receiver, Duration::from_secs(1)).await,
        Some("cursor_only".to_string())
    );
    let materialized_latency = receive_proto_latency(&mut latency_receiver, Duration::from_secs(1))
        .await
        .expect("materialized delta should emit processing latency");
    assert_eq!(materialized_latency.0, "materialized");
    assert!(materialized_latency.1 > 0.0);
    let cursor_only_latency = receive_proto_latency(&mut latency_receiver, Duration::from_secs(1))
        .await
        .expect("cursor-only delta should emit processing latency");
    assert_eq!(cursor_only_latency.0, "cursor_only");
    assert!(cursor_only_latency.1 > 0.0);
}

#[test]
#[serial]
fn test_duplicate_proto_headers_skip_decode_but_checksum_repairs_do_not() {
    let spec_store = SpecStore::new(
        "proto-duplicate-test",
        "proto-duplicate-test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    apply_eval_project(&spec_store);
    let before = spec_store.load_data();
    let cursor = spec_store.get_current_specs_info();
    let lcut = cursor.lcut.unwrap();
    let checksum = cursor.checksum.unwrap();

    spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes_with_headers(
                b"body should not be decoded".to_vec(),
                Some(proto_headers(lcut, &checksum)),
            ),
            source: SpecsSource::Network,
            received_at: 3000,
            source_api: Some("duplicate-api".to_string()),
            has_updates: None,
        })
        .unwrap();
    assert!(Arc::ptr_eq(
        &before.snapshot,
        &spec_store.load_data().snapshot
    ));

    let repair_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes_with_headers(
            b"body must be validated".to_vec(),
            Some(proto_headers(lcut, "different-checksum")),
        ),
        source: SpecsSource::Network,
        received_at: 3001,
        source_api: Some("repair-api".to_string()),
        has_updates: None,
    });
    assert!(repair_result.is_err());
    assert!(Arc::ptr_eq(
        &before.snapshot,
        &spec_store.load_data().snapshot
    ));
}

#[test]
#[serial]
fn test_cursor_accepts_same_lcut_checksum_repair_and_ignores_stale_or_duplicate_deltas() {
    let spec_store = initialized_spec_store("cursor-ordering-test");

    let initial = spec_store.load_data();
    let lcut = initial.lcut();
    apply_delta(
        &spec_store,
        protobuf_delta(
            &initial.snapshot,
            lcut,
            "same-lcut-repair",
            DeltaOverrides::default(),
        ),
        SpecsSource::Network,
        "repair-api",
    )
    .unwrap();
    let repaired = spec_store.load_data();
    assert!(Arc::ptr_eq(&initial.snapshot, &repaired.snapshot));
    assert_eq!(
        spec_store.get_current_specs_info().checksum.as_deref(),
        Some("same-lcut-repair")
    );
    assert_eq!(repaired.source_api.as_deref(), Some("repair-api"));

    apply_delta(
        &spec_store,
        protobuf_delta(
            &repaired.snapshot,
            lcut - 1,
            "stale-checksum",
            DeltaOverrides::default(),
        ),
        SpecsSource::Bootstrap,
        "stale-api",
    )
    .unwrap();
    apply_delta(
        &spec_store,
        protobuf_delta(
            &repaired.snapshot,
            lcut,
            "same-lcut-repair",
            DeltaOverrides::default(),
        ),
        SpecsSource::Bootstrap,
        "duplicate-api",
    )
    .unwrap();

    let after_ignored = spec_store.load_data();
    assert_eq!(after_ignored.lcut(), lcut);
    assert_eq!(
        spec_store.get_current_specs_info().checksum.as_deref(),
        Some("same-lcut-repair")
    );
    assert_eq!(after_ignored.source, SpecsSource::Network);
    assert_eq!(after_ignored.source_api.as_deref(), Some("repair-api"));
}

#[test]
#[serial]
fn test_checksum_failure_does_not_advance_cursor() {
    let spec_store = initialized_spec_store("checksum-failure-test");

    let before = spec_store.load_data();
    let before_info = spec_store.get_current_specs_info();
    let result = apply_delta(
        &spec_store,
        protobuf_delta(
            &before.snapshot,
            before.lcut() + 1,
            "invalid-checksum",
            DeltaOverrides {
                corrupt_checksums: true,
                ..DeltaOverrides::default()
            },
        ),
        SpecsSource::Network,
        "invalid-api",
    );

    assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
    let after = spec_store.load_data();
    assert!(Arc::ptr_eq(&before.snapshot, &after.snapshot));
    assert_eq!(after.lcut(), before.lcut());
    assert_eq!(
        spec_store.get_current_specs_info().checksum,
        before_info.checksum
    );
    assert_eq!(after.source_api, before.source_api);
}

#[test]
#[serial]
fn test_cursor_only_delta_updates_evaluation_lcut_without_changing_result() {
    let statsig = Statsig::new(
        "evaluation-cursor-test",
        Some(Arc::new(StatsigOptions {
            disable_all_logging: Some(true),
            disable_network: Some(true),
            ..StatsigOptions::default()
        })),
    );
    let spec_store = statsig.get_context().spec_store;
    apply_eval_project(&spec_store);
    let before = spec_store.load_data();
    let gate_name = before
        .snapshot
        .feature_gates
        .keys()
        .next()
        .unwrap()
        .as_str();
    let user = StatsigUser::with_user_id("cursor-user");
    let options = FeatureGateEvaluationOptions {
        disable_exposure_logging: true,
    };
    let before_evaluation =
        statsig.get_feature_gate_with_options(&user, gate_name, options.clone());

    let next_lcut = before.lcut() + 1;
    apply_delta(
        &spec_store,
        protobuf_delta(
            &before.snapshot,
            next_lcut,
            "evaluation-cursor",
            DeltaOverrides::default(),
        ),
        SpecsSource::Network,
        "evaluation-api",
    )
    .unwrap();
    let after_evaluation = statsig.get_feature_gate_with_options(&user, gate_name, options);

    assert_eq!(after_evaluation.value, before_evaluation.value);
    assert_eq!(after_evaluation.rule_id, before_evaluation.rule_id);
    assert_eq!(before_evaluation.details.lcut, Some(before.lcut()));
    assert_eq!(after_evaluation.details.lcut, Some(next_lcut));
    assert_eq!(statsig.get_client_init_response(&user).time, next_lcut);

    for response_format in [
        GCIRResponseFormat::InitializeWithSecondaryExposureMapping,
        GCIRResponseFormat::InitializeV2,
    ] {
        let response = statsig.get_client_init_response_with_options_as_string(
            &user,
            &ClientInitResponseOptions {
                response_format: Some(response_format),
                ..ClientInitResponseOptions::default()
            },
        );
        let response: serde_json::Value = serde_json::from_str(&response).unwrap();
        assert_eq!(response["time"], serde_json::json!(next_lcut));
    }
}

#[test]
#[serial]
fn test_nonempty_delta_applies_after_cursor_only_baseline() {
    let spec_store = initialized_spec_store("cursor-baseline-test");

    let initial = spec_store.load_data();
    apply_delta(
        &spec_store,
        protobuf_delta(
            &initial.snapshot,
            initial.lcut() + 1,
            "cursor-baseline",
            DeltaOverrides::default(),
        ),
        SpecsSource::Network,
        "cursor-api",
    )
    .unwrap();
    let cursor_baseline = spec_store.load_data();
    assert!(Arc::ptr_eq(&initial.snapshot, &cursor_baseline.snapshot));

    let deleted_name = cursor_baseline
        .snapshot
        .dynamic_configs
        .keys()
        .next()
        .unwrap()
        .as_str()
        .to_string();
    let deletions = pb::RulesetsResponseDeletions {
        dynamic_configs: vec![deleted_name.clone()],
        ..pb::RulesetsResponseDeletions::default()
    };
    apply_delta(
        &spec_store,
        protobuf_delta(
            &cursor_baseline.snapshot,
            cursor_baseline.lcut() + 1,
            "post-cursor-deletion",
            DeltaOverrides {
                deletions,
                ..DeltaOverrides::default()
            },
        ),
        SpecsSource::Network,
        "deletion-api",
    )
    .unwrap();

    let after_deletion = spec_store.load_data();
    assert!(!Arc::ptr_eq(
        &cursor_baseline.snapshot,
        &after_deletion.snapshot
    ));
    assert!(!after_deletion
        .snapshot
        .dynamic_configs
        .keys()
        .any(|name| name.as_str() == deleted_name));
    assert_eq!(after_deletion.lcut(), cursor_baseline.lcut() + 1);
}
