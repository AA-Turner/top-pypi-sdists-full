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
    test_store(key, None)
}

fn test_store(key: &str, enable_dcs_deltas: Option<bool>) -> SpecStore {
    let options = StatsigOptions {
        enable_dcs_deltas,
        ..StatsigOptions::default()
    };
    let mut store = SpecStore::new(
        key,
        key.to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );
    store.enable_partial_blob_publication = true;
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

async fn apply_background(
    store: &SpecStore,
    server: &MockServer,
    update: SpecsUpdate,
) -> Result<(), StatsigErr> {
    let hydration = hydration(store, server).with_sync_trigger(SpecsSyncTrigger::Background);
    store
        .did_receive_specs_update_async(update, Some(hydration))
        .await
}

fn inline_proto(value: Value) -> pb::Spec {
    pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        default_value: Some(raw_return_value(value)),
        ..Default::default()
    }
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

fn assert_delta_failure_counts(receiver: &mut Receiver<OpsStatsEvent>, expected: &[f64]) {
    let mut counts = Vec::new();
    while let Ok(event) = receiver.try_recv() {
        let OpsStatsEvent::Observability(event) = event else {
            continue;
        };
        if event.metric_name == "remote_config_hydration.unavailable_blob" {
            assert!(matches!(event.metric_type, MetricType::Increment));
            assert_eq!(
                event.tags.unwrap(),
                HashMap::from([
                    ("format".into(), "protobuf".into()),
                    ("failure_reason".into(), "download_failed".into()),
                ])
            );
            counts.push(event.value);
        }
    }
    assert_eq!(counts, expected);
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
    proto_update_with_rest(
        time,
        configs,
        delta,
        deleted,
        config_checksum_sum,
        json!({"experiment_to_layer": {}, "condition_map": {}}),
    )
}

fn proto_update_with_rest(
    time: u64,
    configs: Vec<(&str, u32, pb::Spec)>,
    delta: bool,
    deleted: &[&str],
    config_checksum_sum: u64,
    rest: Value,
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
                rest: serde_json::to_vec(&rest).unwrap(),
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
async fn partial_delta_requires_opt_in_and_a_warm_sync_trigger() {
    for (opt_in, trigger) in [
        (None, SpecsSyncTrigger::Background),
        (Some(false), SpecsSyncTrigger::Background),
        (Some(true), SpecsSyncTrigger::Initial),
    ] {
        let server = MockServer::start().await;
        let store = test_store("ineligible-partial-delta", opt_in);
        store.set_values(json_update(full(1, json!({})))).unwrap();
        let installed = store.load_data();
        let missing = Blob::new("missing").proto_config();
        let update = proto_update(2, vec![("missing", 13, missing)], true, &[], 13);
        let hydration = hydration(&store, &server).with_sync_trigger(trigger);
        let error = store
            .did_receive_specs_update_async(update, Some(hydration))
            .await
            .unwrap_err();
        assert!(error.to_string().contains("download_failed"), "{error}");
        assert!(Arc::ptr_eq(&installed, &store.load_data()));
        assert_eq!(store.get_current_specs_info().lcut, Some(1));
    }
}

#[tokio::test]
async fn incomplete_delta_releases_superseded_id_lists() -> Result<(), StatsigErr> {
    let server = MockServer::start().await;
    let store = test_store("partial-delta-id-lists", Some(true));
    store.set_values(json_update(full(1, json!({}))))?;
    let metadata = serde_json::from_value(json!({
        "name": "members", "url": "", "size": 0, "creationTime": 1
    }))
    .unwrap();
    let list = IdList::new(metadata);
    let old_ids = Arc::downgrade(&list.ids);
    let lists = HashMap::from([("members".into(), list)]);
    store.did_receive_id_list_snapshot(lists, HashMap::new())?;

    let missing = Blob::new("missing").proto_config();
    let delta = proto_update(2, vec![("new", 13, missing)], true, &[], 13);
    apply_background(&store, &server, delta).await?;
    assert_eq!(store.get_current_specs_info().lcut, Some(2));
    assert!(old_ids.upgrade().is_some());
    store.did_receive_id_list_snapshot(HashMap::new(), HashMap::new())?;
    assert!(old_ids.upgrade().is_none());
    Ok(())
}

#[tokio::test]
async fn pending_blob_retains_a_config_only_for_the_same_target_apps() {
    for (config_apps, client_app, retained) in [
        (vec!["b", "a", "a"], "a", true),
        (vec!["a", "c"], "a", false),
        (vec![], "a", false),
        (vec!["a", "b"], "c", false),
    ] {
        let server = MockServer::start().await;
        let store = test_store("pending-app-scope", Some(true));
        let mut old = inline_proto(json!({"private": true}));
        old.target_app_ids = vec!["a".into(), "b".into()];
        let routing =
            |app| json!({"experiment_to_layer": {}, "sdk_keys_to_app_ids": {"client": app}});
        store
            .set_values(proto_update_with_rest(
                1,
                vec![("scoped", 7, old)],
                false,
                &[],
                7,
                routing("a"),
            ))
            .unwrap();
        let mut next = Blob::new("missing").proto_config();
        next.target_app_ids = config_apps.into_iter().map(str::to_owned).collect();
        let metadata = routing(client_app);
        apply_background(
            &store,
            &server,
            proto_update_with_rest(2, vec![("scoped", 13, next)], true, &[], 13, metadata),
        )
        .await
        .unwrap();
        let current = store.load_data();
        assert_eq!(current.lcut(), 2);
        assert_eq!(
            current
                .snapshot
                .dynamic_configs
                .get(&InternedString::from_str_ref("scoped"))
                .is_some(),
            retained
        );
    }
}

#[tokio::test]
async fn failed_new_config_at_either_end_of_an_old_or_new_mapping_rejects_the_delta() {
    let server = MockServer::start().await;
    let missing = Blob::new("missing");
    for (source, destination) in [("working", "pending"), ("pending", "working")] {
        let mapping = json!({(source): [{
            "new_config_name": destination,
            "rules": [{"rule_name": "all"}],
        }]});
        let unmapped = json!({});
        for (old, new) in [(&unmapped, &mapping), (&mapping, &unmapped)] {
            let store = test_store("pending-mapping", Some(true));
            store
                .set_values(proto_update_with_rest(
                    1,
                    vec![("working", 7, inline_proto(json!({"v": 1})))],
                    false,
                    &[],
                    7,
                    json!({"experiment_to_layer": {}, "overrides": old}),
                ))
                .unwrap();
            let previous = store.load_data();
            let delta = proto_update_with_rest(
                2,
                vec![
                    ("pending", 13, missing.proto_config()),
                    ("working", 11, inline_proto(json!({"v": 2}))),
                ],
                true,
                &[],
                24,
                json!({"experiment_to_layer": {}, "overrides": new}),
            );
            let err = apply_background(&store, &server, delta).await.unwrap_err();
            assert!(
                err.to_string().contains("routing for a mapped config"),
                "{err}"
            );
            assert!(Arc::ptr_eq(&previous, &store.load_data()));
            assert_eq!(store.get_current_specs_info().lcut, Some(1));
        }
    }
}

#[tokio::test]
async fn removing_a_withheld_roots_mapping_keeps_its_destination_private() {
    let server = MockServer::start().await;
    let store = test_store("pending-route-privacy", Some(true));
    store.set_values(json_update(full(1, json!({})))).unwrap();
    let delta = |time, mappings| {
        proto_update_with_rest(
            time,
            vec![
                ("root", 13, Blob::new("missing").proto_config()),
                ("private_a", 11, inline_proto(json!({"private": true}))),
                ("private_b", 17, inline_proto(json!({"private": true}))),
            ],
            true,
            &[],
            41,
            json!({"experiment_to_layer": {}, "overrides": mappings}),
        )
    };
    let mapping = |names: &[&str]| {
        let routes: Vec<_> = names
            .iter()
            .map(|name| json!({"new_config_name": name, "rules": []}))
            .collect();
        json!({"root": routes})
    };
    for (time, names) in [
        (2, &["private_a", "private_b"][..]),
        (3, &["private_b", "private_a", "private_a"][..]),
    ] {
        apply_background(&store, &server, delta(time, mapping(names)))
            .await
            .unwrap();
    }
    let serving = store.load_data();
    assert!(
        serving
            .gcir_evaluation_plan(&HashUtil::new())
            .dynamic_configs
            .is_empty()
    );
    let err = apply_background(&store, &server, delta(4, mapping(&["private_b"])))
        .await
        .unwrap_err();
    assert!(err.to_string().contains("routing for a mapped config"));
    assert!(Arc::ptr_eq(&serving, &store.load_data()));
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
async fn partial_full_snapshot_reports_only_verified_values_until_same_revision_repair() {
    let server = MockServer::start().await;
    let store = store("partial-snapshot");
    let hydration = hydration(&store, &server);
    let mut metrics = store.ops_stats.subscribe_for_test();
    let healthy = Blob::new("healthy");
    let missing = Blob::new("missing");
    healthy.mount(&server, 1).await;
    let old = full(1, json!({"a": healthy.config(), "b": healthy.config()}));
    apply_json(&store, &hydration, old.clone()).await.unwrap();
    assert_backing_counts(&mut metrics, 0.0, 2.0);

    let updates = Arc::new(Mutex::new(Vec::new()));
    let seen = Arc::clone(&updates);
    store
        .event_emitter
        .subscribe(SdkEvent::SPECS_UPDATED, move |event| {
            if let SdkEvent::SpecsUpdated { values, .. } = event {
                seen.lock().push((values.time, values.checksum.clone()));
            }
        });
    let mut missing_config = missing.config();
    missing_config["checksum"] = json!("13");
    let payload = full(2, json!({"a": missing_config, "b": healthy.config()}));
    apply_json(&store, &hydration, payload.clone())
        .await
        .unwrap();
    let partial = store.load_data();
    let a = InternedString::from_str_ref("a");
    assert_eq!(partial.snapshot.time, 2);
    assert!(partial.snapshot.checksum.is_none());
    assert_eq!(
        partial.unavailable_values().unwrap()[&a],
        HashSet::from([None, Some(0)])
    );
    assert_eq!(
        store.get_published_specs_info().checksum.as_deref(),
        Some("snapshot-2")
    );
    assert_eq!(store.get_current_specs_info().lcut, Some(0));
    assert!(store.get_current_values().is_none());
    assert_backing_counts(&mut metrics, 0.0, 1.0);

    store
        .set_values(json_update(json!({"has_updates": false})))
        .unwrap();
    assert_backing_counts(&mut metrics, 0.0, 1.0);
    apply_json(&store, &hydration, payload.clone())
        .await
        .unwrap();
    apply_json(&store, &hydration, old).await.unwrap();
    assert!(Arc::ptr_eq(&partial.snapshot, &store.load_data().snapshot));
    assert!(updates.lock().is_empty());

    // The producer can inline the repaired value without changing its entity checksum.
    let expected = json!({"marker": "missing"});
    let inline = pb::Spec {
        entity: pb::EntityType::EntityDynamicConfig as i32,
        enabled: true,
        default_value: Some(raw_return_value(expected.clone())),
        ..Default::default()
    };
    store
        .set_values_with_protobuf_hydration(
            proto_update(2, vec![("a", 13, inline)], false, &[], 13),
            &hydration,
        )
        .await
        .unwrap();
    assert_eq!(
        json!(
            store
                .load_data()
                .snapshot
                .dynamic_configs
                .get(&a)
                .unwrap()
                .view()
                .default_value()
                .json_value()
                .unwrap()
        ),
        expected
    );
    assert_eq!(
        store.get_current_values().unwrap().checksum.as_deref(),
        Some("snapshot-2")
    );
    assert_eq!(*updates.lock(), vec![(2, Some("snapshot-2".to_owned()))]);
    let mut metrics = store.ops_stats.subscribe_for_test();
    store
        .set_values(json_update(full(
            3,
            json!({"a":inline_config(json!({"now":"inline"}))}),
        )))
        .unwrap();
    assert_backing_counts(&mut metrics, 0.0, 0.0);
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
async fn pending_config_retains_proofs_from_deleted_configs_and_incomplete_repairs() {
    let server = MockServer::start().await;
    let store = test_store("pending-config-proofs", Some(true));
    let mut metrics = store.ops_stats.subscribe_for_test();
    let x = Blob::new("shared-with-deleted-config");
    let y = Blob::new("recovered-first");
    let z = Blob::new("recovered-last");

    x.mount(&server, 1).await;
    let full = proto_update(1, vec![("b", 11, x.proto_config())], false, &[], 11);
    apply_background(&store, &server, full).await.unwrap();
    server.verify().await;
    server.reset().await;

    let mut a = x.proto_config();
    a.rules = y.proto_config().rules;
    let mut last_rule = z.proto_config().rules.pop().unwrap();
    last_rule.id = "last".into();
    a.rules.push(last_rule);
    let delta = proto_update(2, vec![("a", 13, a)], true, &["b"], 13);
    apply_background(&store, &server, delta).await.unwrap();
    assert_delta_failure_counts(&mut metrics, &[2.0]);
    let snapshot = store.load_data();
    assert_eq!(snapshot.lcut(), 2);
    assert!(snapshot.snapshot.dynamic_configs.0.is_empty());

    y.mount(&server, 1).await;
    let no_change = || json_update(json!({"has_updates": false}));
    apply_background(&store, &server, no_change())
        .await
        .unwrap();
    assert_delta_failure_counts(&mut metrics, &[]);
    assert!(store.get_current_values().is_none());
    server.verify().await;
    server.reset().await;

    // Only Z is online now. The original snapshot supplied X and the first retry supplied Y.
    z.mount(&server, 1).await;
    apply_background(&store, &server, no_change())
        .await
        .unwrap();
    assert_delta_failure_counts(&mut metrics, &[]);
    let export = store
        .get_current_values()
        .expect("all three values verified");
    let config = export
        .dynamic_configs
        .get(&InternedString::from_str_ref("a"))
        .unwrap()
        .as_spec_ref();
    let values = [
        &config.default_value,
        &config.rules[0].return_value,
        &config.rules[1].return_value,
    ];
    for (value, blob) in values.into_iter().zip([&x, &y, &z]) {
        assert_eq!(serde_json::to_vec(value).unwrap(), blob.body);
    }
    assert_eq!(server.received_requests().await.unwrap().len(), 1);
    server.verify().await;
    server.reset().await;

    // Removing A releases the recovered SHA. When it fails again in two new
    // configs, the publication counts the recurrence once.
    let delete = proto_update(3, vec![], true, &["a"], 0);
    apply_background(&store, &server, delete).await.unwrap();
    let configs = vec![("c", 17, z.proto_config()), ("d", 19, z.proto_config())];
    let recurrence = proto_update(4, configs, true, &[], 36);
    apply_background(&store, &server, recurrence).await.unwrap();
    assert_delta_failure_counts(&mut metrics, &[1.0]);
    apply_background(&store, &server, no_change())
        .await
        .unwrap();
    assert_delta_failure_counts(&mut metrics, &[]);
}

#[tokio::test]
async fn metadata_conflicting_with_a_carried_config_rejects_the_new_delta() {
    let server = MockServer::start().await;
    let store = test_store("pending-metadata-conflict", Some(true));
    store.set_values(json_update(full(1, json!({})))).unwrap();

    let mut config = Blob::new("missing").proto_config();
    config.rules.clear();
    let first = proto_update(2, vec![("pending", 13, config.clone())], true, &[], 13);
    apply_background(&store, &server, first).await.unwrap();
    let previous = store.load_data();
    assert_eq!(previous.lcut(), 2);

    // Only the definition carried from the earlier delta conflicts with this one.
    config.remote_config_metadata.as_mut().unwrap().byte_length += 1;
    let next = proto_update(3, vec![("new", 17, config)], true, &[], 30);
    let err = apply_background(&store, &server, next).await.unwrap_err();
    assert!(err.to_string().contains("metadata_conflict"), "{err}");
    assert!(Arc::ptr_eq(&previous, &store.load_data()));
    assert_eq!(store.get_current_specs_info().lcut, Some(2));
}

#[tokio::test]
async fn partial_delta_applies_sdk_settings_without_exporting_an_incomplete_cursor() {
    for delete in [false, true] {
        let server = MockServer::start().await;
        let store = test_store("partial-delta-settings", Some(true));
        store.set_values(json_update(full(1, json!({})))).unwrap();
        let mut metrics = store.ops_stats.subscribe_for_test();
        let missing = Blob::new("missing");
        let delta = proto_update_with_rest(
            2,
            vec![("pending", 13, missing.proto_config())],
            true,
            &[],
            13,
            json!({"experiment_to_layer": {}, "sdk_configs": {"exposure_dedupe_ttl_ms": 2000}}),
        );
        apply_background(&store, &server, delta).await.unwrap();
        assert_delta_failure_counts(&mut metrics, &[1.0]);
        assert_eq!(store.get_current_specs_info().lcut, Some(2));
        assert_eq!(store.readiness_specs_info().lcut, Some(0));
        assert_eq!(
            store
                .global_configs
                .as_ref()
                .unwrap()
                .get_exposure_dedupe_ttl_ms(),
            2000
        );
        assert!(store.get_current_values().is_none());

        for version in [3, 4] {
            let healthy = inline_proto(json!({"version":version}));
            let checksum = version as u32;
            let configs = vec![("healthy", checksum, healthy)];
            let delta = proto_update(version, configs, true, &[], 13 + version);
            apply_background(&store, &server, delta).await.unwrap();
            assert_delta_failure_counts(&mut metrics, &[]);
            let data = store.load_data();
            assert_eq!(data.lcut(), version);
            assert_eq!(data.spec_decode_stats.total, 2);
            let name = InternedString::from_str_ref("healthy");
            let healthy = data.snapshot.dynamic_configs.get(&name).unwrap();
            assert_eq!(
                serde_json::to_value(&healthy.as_spec_ref().default_value).unwrap(),
                json!({"version":version})
            );
            assert!(
                data.unavailable_values()
                    .unwrap()
                    .contains_key(&InternedString::from_str_ref("pending"))
            );
        }

        // Pause the retry after its GET arrives. Apply the replacement or
        // deletion before letting that older response reach the store.
        let started = Arc::new(tokio::sync::Notify::new());
        let notify = started.clone();
        let old_body = missing.body.clone();
        Mock::given(method("GET"))
            .and(path(missing.path()))
            .respond_with(move |_: &wiremock::Request| {
                notify.notify_one();
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(old_body.clone())
                    .set_delay(std::time::Duration::from_millis(100))
            })
            .expect(1)
            .mount(&server)
            .await;
        let repair = apply_background(&store, &server, json_update(json!({"has_updates": false})));
        tokio::pin!(repair);
        tokio::select! {
            result = &mut repair => panic!("repair returned before issuing the GET: {result:?}"),
            timeout = tokio::time::timeout(std::time::Duration::from_secs(3), started.notified()) => {
                timeout.expect("repair did not request the pending blob");
            }
        }
        let replacement = inline_proto(json!({"replacement": true}));
        let newer = if delete {
            proto_update(5, vec![], true, &["pending"], 4)
        } else {
            proto_update(5, vec![("pending", 17, replacement)], true, &[], 21)
        };
        apply_background(&store, &server, newer).await.unwrap();
        let _stale_result = repair.await;
        let export = store.get_current_values().unwrap();
        assert_eq!(export.time, 5);
        assert!(store.load_data().unavailable_values().is_none());
        let name = InternedString::from_str_ref("pending");
        let value = export
            .dynamic_configs
            .get(&name)
            .map(|spec| serde_json::to_value(&spec.as_spec_ref().default_value).unwrap());
        assert_eq!(value, (!delete).then(|| json!({"replacement": true})));
    }
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
    fn partial_blob_publication_is_latched_when_the_store_is_created() {
        const ENV: &str = "STATSIG_ENABLE_PARTIAL_BLOB_PUBLICATION";
        tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap().block_on(async {
            let server = MockServer::start().await;
            for (setting, enabled) in [(None, false), (Some("false"), false), (Some("yes"), false), (Some("true"), true), (Some("1"), true)] {
                match setting {
                    Some(value) => std::env::set_var(ENV, value),
                    None => std::env::remove_var(ENV),
                }
                let store = SpecStore::new("local-policy", "local-policy".into(), StatsigRuntime::get_runtime(),
                    Arc::new(SdkEventEmitter::default()), None);
                std::env::set_var(ENV, if enabled { "false" } else { "true" });
                let hydration = hydration(&store, &server);
                let inline = json!({"a": inline_config(json!({"v": 1}))});
                apply_json(&store, &hydration, full(1, inline.clone())).await.unwrap();
                let pending = full(2, json!({"a": Blob::new("missing").config()}));
                assert_eq!(apply_json(&store, &hydration, pending).await.is_ok(), enabled);
                assert_eq!(store.get_current_values().is_none(), enabled);
                apply_json(&store, &hydration, full(2, inline)).await.unwrap();
                assert_eq!(store.get_current_values().unwrap().time, 2);
            }
        });
    }

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
