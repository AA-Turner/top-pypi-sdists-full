use super::*;
use crate::networking::NetworkClient;
use crate::observability::ops_stats::OpsStatsEvent;
use crate::specs_adapter::remote_config_value_hydrator::RemoteConfigValueHydrator;
use crate::specs_response::statsig_config_specs::{self as pb, return_value};
use brotli::enc::BrotliEncoderParams;
use prost::Message;
use rusty_fork::rusty_fork_test;
use serde_json::json;
use sha2::{Digest, Sha256};
use std::io::Write;
use tokio::sync::broadcast::Receiver;
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

const METRIC: &str = "remote_config_snapshot.verified_values";

struct Blob {
    body: Vec<u8>,
    sha: String,
}

impl Blob {
    fn new(marker: &str) -> Self {
        let body = serde_json::to_vec(&json!({"marker": marker})).unwrap();
        let sha = Sha256::digest(&body)
            .iter()
            .map(|byte| format!("{byte:02x}"))
            .collect();
        Self { body, sha }
    }

    fn path(&self) -> String {
        format!("/v1/dynamic_config_value/{}", self.sha)
    }

    fn metadata(&self) -> Value {
        json!({
            "sha256": self.sha,
            "byteLength": self.body.len(),
            "contentType": "application/json",
            "compression": "none",
        })
    }

    fn config(&self) -> Value {
        let mut config = inline_config(json!({"value": self.path()}));
        config["remoteConfigMetadata"] = self.metadata();
        config["rules"] = json!([{
            "name": "remote-rule", "id": "remote-rule", "salt": "rule",
            "idType": "userID", "passPercentage": 100, "conditions": [],
            "returnValue": {"value": self.path()},
            "remoteConfigMetadata": self.metadata(),
        }]);
        config
    }

    fn proto_config(&self) -> pb::Spec {
        let metadata = pb::RemoteConfigValueMetadata {
            sha256: self.sha.clone(),
            byte_length: self.body.len() as u64,
            content_type: "application/json".to_string(),
            compression: "none".to_string(),
        };
        let value = raw_return_value(json!({"value": self.path()}));
        pb::Spec {
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            default_value: Some(value.clone()),
            remote_config_metadata: Some(metadata.clone()),
            rules: vec![pb::Rule {
                id: "remote-rule".to_string(),
                name: "remote-rule".to_string(),
                return_value: Some(value),
                remote_config_metadata: Some(metadata),
                ..Default::default()
            }],
            ..Default::default()
        }
    }

    async fn mount(&self, server: &MockServer, requests: u64) {
        Mock::given(method("GET"))
            .and(path(self.path()))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(self.body.clone()),
            )
            .expect(requests)
            .mount(server)
            .await;
    }
}

fn inline_config(value: Value) -> Value {
    json!({
        "type": "dynamic_config", "salt": "snapshot-backing", "enabled": true,
        "defaultValue": value, "rules": [], "idType": "userID",
        "entity": "dynamic_config", "version": 1,
    })
}

fn full(time: u64, configs: Value) -> Value {
    json!({
        "dynamic_configs": configs, "feature_gates": {}, "layer_configs": {},
        "experiment_to_layer": {}, "condition_map": {}, "has_updates": true,
        "time": time, "checksum": format!("snapshot-{time}"),
        "company_id": "snapshot-backing-tests", "response_format": "dcs-v2",
    })
}

fn update(data: ResponseData) -> SpecsUpdate {
    SpecsUpdate {
        data,
        source: SpecsSource::Network,
        received_at: 1,
        source_api: None,
        has_updates: None,
    }
}

fn json_update(value: Value) -> SpecsUpdate {
    update(ResponseData::from_bytes(
        serde_json::to_vec(&value).unwrap(),
    ))
}

fn store(key: &str) -> SpecStore {
    let mut store = SpecStore::new(
        key,
        key.to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    store.release_unused_heap_memory_after_update = false;
    store
}

fn hydration(store: &SpecStore, server: &MockServer) -> SpecsUpdateHydration {
    let hydrator = Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(NetworkClient::new("secret-snapshot-backing", None, None)),
        Arc::clone(&store.ops_stats),
    ));
    SpecsUpdateHydration::new(
        hydrator,
        format!("{}/v2/download_config_specs", server.uri()),
    )
}

async fn apply_json(
    store: &SpecStore,
    hydration: &SpecsUpdateHydration,
    value: Value,
) -> Result<(), StatsigErr> {
    store
        .set_values_with_json_hydration(json_update(value), hydration, None)
        .await
}

fn take_backing_metrics(receiver: &mut Receiver<OpsStatsEvent>) -> Vec<(String, f64)> {
    let mut metrics = Vec::new();
    while let Ok(event) = receiver.try_recv() {
        let OpsStatsEvent::Observability(event) = event else {
            continue;
        };
        if event.metric_name != METRIC {
            continue;
        }
        assert!(matches!(event.metric_type, MetricType::Gauge));
        let tags = event.tags.expect("snapshot gauge should have bounded tags");
        assert_eq!(tags.len(), 2, "no config names, SHAs, or sync labels");
        assert!(tags.contains_key("sdk_key"));
        metrics.push((tags["backing"].clone(), event.value));
    }
    metrics.sort_by(|left, right| left.0.cmp(&right.0));
    metrics
}

fn assert_backing_counts(receiver: &mut Receiver<OpsStatsEvent>, mmap: f64, non_mmap: f64) {
    assert_eq!(
        take_backing_metrics(receiver),
        vec![
            ("mmap".to_string(), mmap),
            ("non_mmap".to_string(), non_mmap)
        ],
    );
}

fn raw_return_value(value: Value) -> pb::ReturnValue {
    pb::ReturnValue {
        value: Some(return_value::Value::RawValue(
            serde_json::to_vec(&value).unwrap(),
        )),
    }
}

fn proto_update(
    time: u64,
    configs: Vec<(&str, u32, pb::Spec)>,
    delta: bool,
    deleted: &[&str],
    config_checksum_sum: u64,
) -> SpecsUpdate {
    let mut envelopes = Vec::new();
    let has_remote_metadata = configs.iter().any(|(_, _, config)| {
        config.remote_config_metadata.is_some()
            || config
                .rules
                .iter()
                .any(|rule| rule.remote_config_metadata.is_some())
    });
    if delta {
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        });
    }
    envelopes.push(pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::TopLevel as i32,
        data: Some(
            pb::SpecsTopLevel {
                has_updates: true,
                time,
                company_id: "snapshot-backing-tests".to_string(),
                response_format: "dcs-v2".to_string(),
                checksum: format!("snapshot-{time}"),
                rest: br#"{"experiment_to_layer":{},"condition_map":{}}"#.to_vec(),
                may_have_remote_config_metadata: Some(has_remote_metadata),
            }
            .encode_to_vec(),
        ),
        ..Default::default()
    });
    for (name, checksum, config) in configs {
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: name.to_string(),
            checksum: checksum.to_string(),
            data: Some(config.encode_to_vec()),
        });
    }
    if !deleted.is_empty() {
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Deletions as i32,
            data: Some(
                pb::RulesetsResponseDeletions {
                    dynamic_configs: deleted.iter().map(|name| (*name).to_string()).collect(),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        });
    }
    if delta {
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Checksums as i32,
            data: Some(
                pb::RulesetsChecksums {
                    field_checksums: HashMap::from([
                        ("dynamic_configs".to_string(), config_checksum_sum),
                        ("feature_gates".to_string(), 0),
                        ("layer_configs".to_string(), 0),
                        ("condition_map".to_string(), 0),
                        ("param_stores".to_string(), 0),
                    ]),
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        });
    }
    envelopes.push(pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Done as i32,
        ..Default::default()
    });
    let mut encoded = Vec::new();
    for envelope in envelopes {
        envelope.encode_length_delimited(&mut encoded).unwrap();
    }
    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::with_params(
            &mut compressed,
            4096,
            &BrotliEncoderParams::default(),
        );
        writer.write_all(&encoded).unwrap();
        writer.flush().unwrap();
    }
    let mut headers = HashMap::from([
        (
            "content-type".to_string(),
            "application/octet-stream".to_string(),
        ),
        ("content-encoding".to_string(), "statsig-br".to_string()),
    ]);
    if delta {
        headers.insert("x-deltas-used".to_string(), "true".to_string());
    }
    update(ResponseData::from_bytes_with_headers(
        compressed,
        Some(headers),
    ))
}

#[tokio::test]
async fn json_snapshot_counts_verified_config_sha_pairs_not_slots_or_inline_values() {
    let server = MockServer::start().await;
    let blob = Blob::new("snapshot-json-dedup");
    let second_blob = Blob::new("snapshot-json-distinct-rule");
    blob.mount(&server, 1).await;
    second_blob.mount(&server, 1).await;
    let mut config_a = blob.config();
    let mut second_rule = second_blob.config()["rules"][0].clone();
    second_rule["id"] = json!("distinct-rule");
    second_rule["name"] = json!("distinct-rule");
    config_a["rules"].as_array_mut().unwrap().push(second_rule);
    let store = store("secret-snapshot-json-counts");
    let mut receiver = store.ops_stats.subscribe_for_test();
    let hydration = hydration(&store, &server);
    apply_json(
        &store,
        &hydration,
        full(
            1,
            json!({
                "a": config_a, "b": blob.config(),
                "inline": inline_config(serde_json::from_slice::<Value>(&blob.body).unwrap()),
            }),
        ),
    )
    .await
    .unwrap();

    assert_eq!(store.load_data().verified_remote_values.len(), 2);
    assert_backing_counts(&mut receiver, 0.0, 3.0);
    server.verify().await;
}

#[tokio::test]
#[ignore = "manual snapshot gauge scan benchmark"]
async fn snapshot_backing_metric_scan_benchmark() {
    let server = MockServer::start().await;
    let blobs: Vec<_> = (0..192)
        .map(|index| {
            let models: Vec<_> = (0..64 + (index % 4) * 32)
                .map(|model| {
                    json!({
                        "name": format!("model-family-{}-variant-{model}", index % 12),
                        "capabilities": {"tools": true, "vision": model % 3 == 0},
                        "limits": {"context_tokens": 131_072, "output_tokens": 16_384},
                        "routing": {"primary": "regional", "fallbacks": ["shared", "overflow"]},
                        "sampling": {"temperature": 0.7, "top_p": 0.95},
                    })
                })
                .collect();
            let body = serde_json::to_vec(&json!({
                "config_id": format!("model-routing-{index}"), "revision": index + 1,
                "models": models,
                "rollout": {"enabled": true, "weights": [0.9, 0.1], "excluded_regions": []},
            }))
            .unwrap();
            let sha = Sha256::digest(&body)
                .iter()
                .map(|byte| format!("{byte:02x}"))
                .collect();
            Blob { body, sha }
        })
        .collect();
    let mut configs = serde_json::Map::new();
    for (index, blob) in blobs.iter().enumerate() {
        blob.mount(&server, 1).await;
        // Each default and first rule share a SHA; additional rules select other blobs.
        let mut config = blob.config();
        for slot in 1..=index % 4 {
            let mut rule = blobs[(index + slot * 37) % blobs.len()].config()["rules"][0].clone();
            rule["id"] = json!(format!("remote-rule-{slot}"));
            rule["name"] = rule["id"].clone();
            config["rules"].as_array_mut().unwrap().push(rule);
        }
        configs.insert(format!("model_routing_{index}"), config);
    }
    let store = store("secret-snapshot-benchmark");
    let hydration = hydration(&store, &server);
    apply_json(&store, &hydration, full(1, Value::Object(configs)))
        .await
        .unwrap();
    let active = store.load_data();
    let proofs: HashMap<_, _> = active
        .verified_remote_values
        .values()
        .flat_map(|values| values.iter())
        .map(|(sha, value)| (sha.clone(), Arc::clone(value)))
        .collect();
    assert_eq!(proofs.len(), blobs.len());
    assert_eq!(
        active
            .verified_remote_values
            .values()
            .map(|values| values.len())
            .sum::<usize>(),
        480,
    );
    eprintln!(
        "snapshot backing corpus: {} distinct blobs, {} bytes, blob sizes {}..{} bytes",
        blobs.len(),
        blobs.iter().map(|blob| blob.body.len()).sum::<usize>(),
        blobs.iter().map(|blob| blob.body.len()).min().unwrap(),
        blobs.iter().map(|blob| blob.body.len()).max().unwrap(),
    );
    let mut receiver = store.ops_stats.subscribe_for_test();
    for (config_count, expected_entries) in [(0usize, 0usize), (120, 300), (26_215, 65_536)] {
        let mut data = active.as_ref().clone();
        data.verified_remote_values = Arc::new(
            (0..config_count)
                .map(|index| {
                    let values = (0..=index % 4)
                        .map(|slot| {
                            let blob = &blobs[(index + slot * 37) % blobs.len()];
                            (blob.sha.clone(), Arc::clone(&proofs[&blob.sha]))
                        })
                        .collect();
                    (
                        InternedString::from_str_ref(&format!("benchmark-{index}")),
                        Arc::new(values),
                    )
                })
                .collect(),
        );
        let entry_count = data
            .verified_remote_values
            .values()
            .map(|values| values.len())
            .sum::<usize>();
        let unique_proofs = data
            .verified_remote_values
            .values()
            .flat_map(|values| values.values())
            .map(Arc::as_ptr)
            .collect::<std::collections::HashSet<_>>()
            .len();
        assert_eq!(entry_count, expected_entries);
        // Hydration and distinct per-config map construction are outside the timed scan.
        let _update_guard = store.update_lock.lock();
        let started = Instant::now();
        for _ in 0..100 {
            store.ops_stats_log_remote_config_snapshot(std::hint::black_box(&data));
        }
        eprintln!(
            "snapshot backing gauge: {config_count} configs, {entry_count} entries, {unique_proofs} distinct proofs, {:?} per scan",
            started.elapsed() / 100
        );
        let metrics = take_backing_metrics(&mut receiver);
        assert_eq!(metrics.len(), 200);
        assert!(metrics.iter().all(|(backing, value)| *value
            == if backing == "mmap" {
                0.0
            } else {
                entry_count as f64
            }));
    }
    server.verify().await;
}

#[tokio::test]
async fn protobuf_deltas_keep_unchanged_proofs_and_clear_replaced_or_deleted_configs() {
    let server = MockServer::start().await;
    let blob = Blob::new("snapshot-protobuf-delta");
    blob.mount(&server, 1).await;
    let store = store("secret-snapshot-proto-delta");
    let mut receiver = store.ops_stats.subscribe_for_test();
    let hydration = hydration(&store, &server);
    store
        .set_values_with_protobuf_hydration(
            proto_update(
                1,
                vec![
                    ("a", 11, blob.proto_config()),
                    ("b", 12, blob.proto_config()),
                ],
                false,
                &[],
                23,
            ),
            &hydration,
        )
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 2.0);

    // An inline value equal to the old body is no longer a tracked blob.
    let inline = pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        default_value: Some(raw_return_value(
            serde_json::from_slice(&blob.body).unwrap(),
        )),
        ..Default::default()
    };
    store
        .set_values_with_protobuf_hydration(
            proto_update(2, vec![("a", 13, inline)], true, &[], 25),
            &hydration,
        )
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    assert_eq!(store.load_data().verified_remote_values.len(), 1);

    store
        .set_values_with_protobuf_hydration(proto_update(3, vec![], true, &["b"], 13), &hydration)
        .await
        .unwrap();
    assert!(store.load_data().verified_remote_values.is_empty());
    assert_backing_counts(&mut receiver, 0.0, 0.0);
    server.verify().await;
}

#[tokio::test]
async fn full_inline_replacement_resets_gauges_and_failed_hydration_keeps_active_counts() {
    let server = MockServer::start().await;
    let blob = Blob::new("snapshot-failure-active-value");
    blob.mount(&server, 1).await;
    let store = store("secret-snapshot-failed-update");
    let mut receiver = store.ops_stats.subscribe_for_test();
    let hydration = hydration(&store, &server);
    apply_json(&store, &hydration, full(1, json!({"a": blob.config()})))
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    let active = store.load_data();

    let invalid = Blob::new("snapshot-failed-new-value");
    Mock::given(method("GET"))
        .and(path(invalid.path()))
        .respond_with(ResponseTemplate::new(200).set_body_bytes(blob.body.clone()))
        .mount(&server)
        .await;
    assert!(
        apply_json(&store, &hydration, full(2, json!({"a": invalid.config()})))
            .await
            .is_err()
    );
    assert!(Arc::ptr_eq(&active, &store.load_data()));
    assert!(take_backing_metrics(&mut receiver).is_empty());

    store
        .set_values(json_update(json!({"has_updates": false})))
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    store
        .set_values(json_update(full(
            3,
            json!({"a": inline_config(json!({"now": "inline"}))}),
        )))
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 0.0);
    server.verify().await;
}

#[tokio::test]
async fn duplicate_and_no_update_refresh_the_current_snapshot_gauges() {
    let server = MockServer::start().await;
    let blob = Blob::new("snapshot-refresh-counts");
    blob.mount(&server, 1).await;
    let store = store("secret-snapshot-repeat-update");
    let mut receiver = store.ops_stats.subscribe_for_test();
    let hydration = hydration(&store, &server);
    let payload = full(1, json!({"a": blob.config()}));
    apply_json(&store, &hydration, payload.clone())
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    let active_snapshot = Arc::clone(&store.load_data().snapshot);

    apply_json(&store, &hydration, payload).await.unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    assert!(Arc::ptr_eq(&active_snapshot, &store.load_data().snapshot));

    store
        .set_values(json_update(json!({"has_updates": false})))
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    assert!(Arc::ptr_eq(&active_snapshot, &store.load_data().snapshot));

    apply_json(&store, &hydration, full(0, json!({"a": blob.config()})))
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    assert!(Arc::ptr_eq(&active_snapshot, &store.load_data().snapshot));
    server.verify().await;
}

#[test]
fn silent_and_config_only_snapshots_do_not_emit_backing_gauges() {
    let silent_options = StatsigOptions::default().suppress_diagnostic_output(true);
    let mut silent = SpecStore::new(
        "secret-snapshot-silent",
        "silent".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&silent_options),
    );
    let mut config_only = SpecStore::new_with_snapshot_evaluation_session_options(
        "secret-snapshot-config-only",
        "config-only".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
        &SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            ..Default::default()
        },
    );
    for store in [&mut silent, &mut config_only] {
        // Observe the store guard directly, independently of its normal disabled emitter.
        store.ops_stats = Arc::new(OpsStatsForInstance::new());
        store.release_unused_heap_memory_after_update = false;
        let mut receiver = store.ops_stats.subscribe_for_test();
        store.set_values(json_update(full(1, json!({})))).unwrap();
        store
            .set_values(json_update(json!({"has_updates": false})))
            .unwrap();
        assert!(take_backing_metrics(&mut receiver).is_empty());
    }
}

#[tokio::test]
async fn json_cursor_advance_emits_one_snapshot_gauge_pair() {
    let server = MockServer::start().await;
    let blob = Blob::new("snapshot-json-cursor");
    blob.mount(&server, 1).await;
    let store = store("secret-snapshot-json-cursor");
    let mut receiver = store.ops_stats.subscribe_for_test();
    let hydration = hydration(&store, &server);
    let initial = full(1, json!({"a": blob.config()}));
    apply_json(&store, &hydration, initial.clone())
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    let previous = store.load_data();

    let mut cursor_update = initial;
    cursor_update["time"] = json!(2);
    apply_json(&store, &hydration, cursor_update).await.unwrap();

    let current = store.load_data();
    assert_eq!(current.lcut(), 2);
    assert_eq!(current.checksum(), Some("snapshot-1"));
    assert!(Arc::ptr_eq(&previous.snapshot, &current.snapshot));
    assert!(Arc::ptr_eq(
        &previous.verified_remote_values,
        &current.verified_remote_values
    ));
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    server.verify().await;
}

#[tokio::test]
async fn protobuf_cursor_advance_emits_one_snapshot_gauge_pair() {
    let server = MockServer::start().await;
    let blob = Blob::new("snapshot-protobuf-cursor");
    blob.mount(&server, 1).await;
    let store = store("secret-snapshot-protobuf-cursor");
    let mut receiver = store.ops_stats.subscribe_for_test();
    let hydration = hydration(&store, &server);
    store
        .set_values_with_protobuf_hydration(
            proto_update(1, vec![("a", 11, blob.proto_config())], false, &[], 11),
            &hydration,
        )
        .await
        .unwrap();
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    let previous = store.load_data();

    store
        .set_values_with_protobuf_hydration(proto_update(2, vec![], true, &[], 11), &hydration)
        .await
        .unwrap();

    let current = store.load_data();
    assert_eq!(current.lcut(), 2);
    assert_eq!(current.checksum(), Some("snapshot-2"));
    assert!(Arc::ptr_eq(&previous.snapshot, &current.snapshot));
    assert!(Arc::ptr_eq(
        &previous.verified_remote_values,
        &current.verified_remote_values
    ));
    assert_backing_counts(&mut receiver, 0.0, 1.0);
    server.verify().await;
}

rusty_fork_test! {
    #[test]
    fn snapshot_backing_reports_by_default_and_ignores_removed_environment_control() {
        const REMOVED_ENV: &str = "STATSIG_ENABLE_BLOB_SNAPSHOT_BACKING_METRICS";
        for input in [
            None,
            Some(""),
            Some("false"),
            Some("0"),
            Some("TRUE"),
            Some(" true"),
            Some("yes"),
            Some("true"),
            Some("1"),
        ] {
            unsafe {
                match input {
                    Some(value) => std::env::set_var(REMOVED_ENV, value),
                    None => std::env::remove_var(REMOVED_ENV),
                }
            }
            let store = SpecStore::new(
                "secret-snapshot-local-control",
                "snapshot-local-control".to_string(),
                StatsigRuntime::get_runtime(),
                Arc::new(SdkEventEmitter::default()),
                None,
            );
            let mut receiver = store.ops_stats.subscribe_for_test();
            store.set_values(json_update(full(
                1,
                json!({"inline": inline_config(json!({"marker": "preserved"}))}),
            ))).unwrap();
            assert_backing_counts(&mut receiver, 0.0, 0.0);
            let snapshot = store.get_current_values().unwrap();
            assert_eq!(
                serde_json::to_value(snapshot).unwrap()["dynamic_configs"]["inline"]["defaultValue"]["marker"],
                json!("preserved"),
            );
            unsafe { std::env::set_var(REMOVED_ENV, "false"); }
            store.set_values(json_update(json!({"has_updates": false}))).unwrap();
            assert_backing_counts(&mut receiver, 0.0, 0.0);
        }
    }

    #[test]
    fn downloaded_blob_that_interns_into_preloaded_mmap_counts_as_mmap() {
        tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap().block_on(async {
            use crate::interned_values::interned_store::{
                preload_mmap_v2_multi_for_test, write_mmap_v2_for_test,
            };
            let key = "secret-snapshot-mmap-backing";
            let blob = Blob::new("snapshot-value-present-in-preloaded-archive");
            let baseline = full(1, json!({"a": inline_config(serde_json::from_slice::<Value>(&blob.body).unwrap())}));
            let directory = tempfile::tempdir().unwrap();
            let path = directory.path().join("snapshot-backing.mmap");
            write_mmap_v2_for_test(&serde_json::to_vec(&baseline).unwrap(), &path).unwrap();
            preload_mmap_v2_multi_for_test(&[(key, &path)]).unwrap();

            let server = MockServer::start().await;
            blob.mount(&server, 1).await;
            let store = store(key);
            let mut receiver = store.ops_stats.subscribe_for_test();
            let hydration = hydration(&store, &server);
            apply_json(&store, &hydration, full(2, json!({"a": blob.config()}))).await.unwrap();
            let current = store.load_data();
            let verified = current.verified_remote_values.values().next().unwrap().values().next().unwrap();
            assert!(verified.value.get_json_archived_ref().is_some());
            assert_backing_counts(&mut receiver, 1.0, 0.0);
            server.verify().await;
        });
    }
}
