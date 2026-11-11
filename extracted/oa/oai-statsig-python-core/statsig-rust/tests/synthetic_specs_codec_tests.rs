//! Protocol/semantic tests for the offline benchmark encoder. No production fixtures.
#[path = "../examples/support/synthetic_specs.rs"]
mod codec;

use std::collections::BTreeMap;
use std::path::Path;
use std::sync::Arc;

use prost::Message;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::specs_response::spec_types::SpecsResponseFull;
use statsig_rust::specs_response::statsig_config_specs::{self as pb, SpecsEnvelope};
use statsig_rust::{SpecsUpdateListener, Statsig, StatsigHttpSpecsAdapter, StatsigOptions};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockGuard, MockServer, ResponseTemplate};

const COLLECTIONS: [&str; 3] = ["feature_gates", "dynamic_configs", "layer_configs"];
type Blobs = BTreeMap<String, Vec<u8>>;

struct Client {
    specs_mock: MockGuard,
    server: MockServer,
    adapter: Arc<StatsigHttpSpecsAdapter>,
    sdk: Statsig,
}

impl Client {
    async fn start(response: ResponseTemplate, blobs: &Blobs) -> Self {
        let server = MockServer::start().await;
        for (sha, bytes) in blobs {
            Mock::given(method("GET"))
                .and(path(format!("/v1/dynamic_config_value/{sha}")))
                .respond_with(
                    ResponseTemplate::new(200)
                        .insert_header("content-type", "application/json")
                        .set_body_bytes(bytes.clone()),
                )
                .mount(&server)
                .await;
        }
        let specs_mock = mock_specs(&server, response).await;
        let mut options = StatsigOptions {
            specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
            specs_sync_interval_ms: Some(3_600_000),
            enable_dcs_deltas: Some(true),
            disable_all_logging: Some(true),
            ..StatsigOptions::new()
        };
        let adapter = Arc::new(StatsigHttpSpecsAdapter::new(
            "secret-synthetic-codec-test",
            Some(&options),
            None,
        ));
        options.specs_adapter = Some(adapter.clone());
        let sdk = Statsig::new("secret-synthetic-codec-test", Some(Arc::new(options)));
        sdk.initialize().await.unwrap();
        Self {
            specs_mock,
            server,
            adapter,
            sdk,
        }
    }

    fn snapshot(&self) -> Value {
        normalize(serde_json::to_value(self.sdk.specs_snapshot().as_ref()).unwrap())
    }

    fn assert_cursor(&self, source: &Value) {
        let info = self.sdk.get_context().spec_store.get_current_specs_info();
        assert_eq!(info.lcut, source["time"].as_u64());
        assert_eq!(info.checksum.as_deref(), source["checksum"].as_str());
    }

    async fn apply_delta(&mut self, before: &Value, after: &Value, blobs: &Blobs) {
        self.assert_cursor(before);
        let (previous_contents, previous_cursor) = split_cursor(self.snapshot());
        let bytes = codec::encode_delta(before, after).unwrap();
        let response = protobuf_response(bytes).insert_header("x-deltas-used", "true");
        self.specs_mock = mock_specs(&self.server, response).await;
        self.adapter.clone().run_background_sync().await;
        self.assert_cursor(after);

        let (expected_contents, next_cursor) = split_cursor(oracle(after, blobs));
        let (actual_contents, published_cursor) = split_cursor(self.snapshot());
        assert_eq!(actual_contents, expected_contents);
        // Cursor-only updates advance the sync cursor but keep the published snapshot.
        let expected_cursor = if previous_contents == expected_contents {
            previous_cursor
        } else {
            next_cursor
        };
        assert_eq!(published_cursor, expected_cursor);
    }
}

async fn mock_specs(server: &MockServer, response: ResponseTemplate) -> MockGuard {
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .respond_with(response)
        .mount_as_scoped(server)
        .await
}

fn protobuf_response(bytes: Vec<u8>) -> ResponseTemplate {
    ResponseTemplate::new(200)
        .insert_header("content-type", "application/octet-stream")
        .insert_header("content-encoding", "statsig-zstd")
        .set_body_bytes(bytes)
}

// These protobuf fields have no presence bit for an empty value. Do not normalize
// arbitrary empty values: returnValue/defaultValue and checksums remain exact.
fn normalize(mut value: Value) -> Value {
    let object = value.as_object_mut().unwrap();
    if object.get("company_id") == Some(&json!("")) {
        object.remove("company_id");
    }
    if object.get("param_stores") == Some(&json!({})) {
        object.remove("param_stores");
    }
    for collection in COLLECTIONS {
        for spec in value[collection].as_object_mut().unwrap().values_mut() {
            for field in ["explicitParameters", "targetAppIDs", "fieldsUsed"] {
                if spec.get(field) == Some(&json!([])) {
                    spec.as_object_mut().unwrap().remove(field);
                }
            }
            for rule in spec["rules"].as_array_mut().unwrap() {
                if rule.get("sharedControlExperiments") == Some(&json!([])) {
                    rule.as_object_mut()
                        .unwrap()
                        .remove("sharedControlExperiments");
                }
            }
        }
    }
    value
}

fn hex_digest(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn expand_value(owner: &mut Value, value_field: &str, blobs: &Blobs) {
    if let Some(metadata) = owner
        .as_object_mut()
        .unwrap()
        .remove("remoteConfigMetadata")
    {
        let sha = metadata["sha256"].as_str().unwrap();
        let bytes = &blobs[sha];
        assert_eq!(bytes.len() as u64, metadata["byteLength"].as_u64().unwrap());
        assert_eq!(hex_digest(bytes), sha);
        assert_eq!(
            owner[value_field],
            json!(format!("/v1/dynamic_config_value/{sha}"))
        );
        owner[value_field] = serde_json::from_slice(bytes).unwrap();
    }
}

fn oracle(source: &Value, blobs: &Blobs) -> Value {
    let mut expanded = source.clone();
    for spec in expanded["dynamic_configs"]
        .as_object_mut()
        .unwrap()
        .values_mut()
    {
        expand_value(spec, "defaultValue", blobs);
        for rule in spec["rules"].as_array_mut().unwrap() {
            expand_value(rule, "returnValue", blobs);
        }
    }
    let parsed: SpecsResponseFull = serde_json::from_value(expanded).unwrap();
    let expected = normalize(serde_json::to_value(parsed).unwrap());
    // Full decoders may skip invalid entities. Compare shape against the input,
    // independently of either SDK network decode path.
    for collection in COLLECTIONS {
        assert_eq!(
            expected[collection].as_object().unwrap().len(),
            source[collection].as_object().unwrap().len()
        );
        for (name, spec) in source[collection].as_object().unwrap() {
            assert_eq!(
                expected[collection][name]["rules"]
                    .as_array()
                    .unwrap()
                    .len(),
                spec["rules"].as_array().unwrap().len()
            );
        }
    }
    assert_eq!(
        expected["condition_map"].as_object().unwrap().len(),
        source["condition_map"].as_object().unwrap().len()
    );
    expected
}

async fn start_full(source: &Value, blobs: &Blobs) -> Client {
    let expected = oracle(source, blobs);
    let json_client = Client::start(ResponseTemplate::new(200).set_body_json(source), blobs).await;
    assert_eq!(json_client.snapshot(), expected);
    json_client.assert_cursor(source);
    json_client.sdk.shutdown().await.unwrap();

    let bytes = codec::encode_full(source).unwrap();
    let client = Client::start(protobuf_response(bytes), blobs).await;
    assert_eq!(client.snapshot(), expected);
    client.assert_cursor(source);
    client
}

fn split_cursor(mut snapshot: Value) -> (Value, [Option<Value>; 2]) {
    let fields = snapshot.as_object_mut().unwrap();
    let cursor = ["time", "checksum"].map(|field| fields.remove(field));
    (snapshot, cursor)
}

fn tiny_state() -> Value {
    json!({
        "has_updates": true, "time": 1, "checksum": "cursor-one", "response_format": "dcs-v2",
        "experiment_to_layer": {}, "sdk_flags": {"invented_flag": true}, "default_environment": "test",
        "condition_map": {"public": {"type": "public", "idType": "userID", "checksum": "5"}},
        "feature_gates": {"gate": {
            "type": "feature_gate", "entity": "feature_gate", "salt": "gate", "idType": "userID",
            "enabled": true, "version": 1, "checksum": "7", "defaultValue": false,
            "rules": [{"name": "allow", "id": "allow", "salt": "rule", "idType": "userID",
                "passPercentage": 37.5, "returnValue": true, "conditions": ["public"]}]
        }},
        "dynamic_configs": {"config": {
            "type": "dynamic_config", "entity": "dynamic_config", "salt": "config", "idType": "userID",
            "enabled": true, "version": 2, "checksum": "11", "defaultValue": {"empty": {}, "list": [null, false, -2, 1.25], "encoded": "{\"x\":1}"},
            "rules": []
        }},
        "layer_configs": {}
    })
}

#[tokio::test]
async fn full_and_delta_preserve_values_checksums_and_replace_common_fields() {
    let mut base = tiny_state();
    // JSON's conservative hint may remain true after values were inlined.
    base["may_have_remote_config_metadata"] = json!(true);
    let blobs = Blobs::new();
    let mut client = start_full(&base, &blobs).await;
    let mut common = base.clone();
    common["time"] = json!(2);
    common["checksum"] = json!("cursor-two");
    common
        .as_object_mut()
        .unwrap()
        .remove("default_environment");
    common["sdk_flags"] = json!({"new_flag": false});
    client.apply_delta(&base, &common, &blobs).await;
    let mut changed = common.clone();
    changed["time"] = json!(3);
    changed["checksum"] = json!("cursor-three");
    changed["condition_map"]["public"]["additionalValues"] = json!({"key": "value"});
    changed["condition_map"]["public"]["checksum"] = json!("6");
    changed["dynamic_configs"]["config"]["defaultValue"] = json!({"next": [true, "λ\n"]});
    changed["dynamic_configs"]["config"]["checksum"] = json!("13");
    changed["dynamic_configs"]["config"]["version"] = json!(3);
    changed["feature_gates"] = json!({});
    client.apply_delta(&common, &changed, &blobs).await;
    client.sdk.shutdown().await.unwrap();
}

fn remote_value(value: Value, blobs: &mut Blobs) -> (Value, Value) {
    let bytes = serde_json::to_vec(&value).unwrap();
    let sha = hex_digest(&bytes);
    let metadata = json!({"sha256": sha, "byteLength": bytes.len(), "contentType": "application/json", "compression": "none"});
    blobs.insert(sha.clone(), bytes);
    (json!(format!("/v1/dynamic_config_value/{sha}")), metadata)
}

fn envelopes(encoded: &[u8]) -> Vec<SpecsEnvelope> {
    let decoded = zstd::decode_all(encoded).unwrap();
    let mut remaining = decoded.as_slice();
    let mut envelopes = Vec::new();
    while !remaining.is_empty() {
        envelopes.push(SpecsEnvelope::decode_length_delimited(&mut remaining).unwrap());
    }
    envelopes
}

#[test]
fn same_state_replay_is_a_deterministic_delta_without_entity_frames() {
    use pb::SpecsEnvelopeKind::{Checksums, CopyPrev, Done, TopLevel};

    let state = tiny_state();
    let full = codec::encode_full(&state).unwrap();
    assert_eq!(full, codec::encode_full(&state).unwrap());
    let delta = codec::encode_delta(&state, &state).unwrap();
    assert_eq!(delta, codec::encode_delta(&state, &state).unwrap());
    let frames = envelopes(&delta);
    let kinds: Vec<_> = frames.iter().map(SpecsEnvelope::kind).collect();
    assert_eq!(kinds, [CopyPrev, TopLevel, Checksums, Done]);
    let top = pb::SpecsTopLevel::decode(frames[1].data.as_deref().unwrap()).unwrap();
    assert_eq!(top.time, state["time"].as_u64().unwrap());
    assert_eq!(top.checksum, state["checksum"].as_str().unwrap());
}

#[test]
fn conditions_use_serving_protobuf_fields() {
    let mut state = tiny_state();
    state["condition_map"]["public"]["targetValue"] = Value::Null;
    state["condition_map"]["dependency"] = json!({
        "type": "pass_gate", "idType": "userID", "targetValue": "gate", "checksum": "18"
    });
    let frames = envelopes(&codec::encode_full(&state).unwrap());
    let condition = |name| {
        let frame = frames.iter().find(|frame| frame.name == name).unwrap();
        pb::Condition::decode(frame.data.as_deref().unwrap()).unwrap()
    };
    let dependency = condition("dependency");
    assert_eq!(
        dependency.id_type.unwrap().id_type,
        Some(pb::id_type::IdType::KnownIdType(
            pb::KnownIdType::UserId as i32
        ))
    );
    assert_eq!(
        dependency.target_value.unwrap().value,
        Some(pb::any_value::Value::StringValue("gate".into()))
    );
    assert_eq!(
        condition("public").target_value.unwrap().value,
        Some(pb::any_value::Value::RawValue(b"null".to_vec()))
    );
}

#[test]
fn full_stream_preserves_early_and_late_remote_entity_positions() {
    let (path, metadata) = remote_value(json!({"remote": true}), &mut Blobs::new());
    let mut state = tiny_state();
    let inline = state["dynamic_configs"]["config"].take();
    let mut remote = inline.clone();
    remote["defaultValue"] = path;
    remote["remoteConfigMetadata"] = metadata;
    let last = state.as_object().unwrap().len() - 1;
    for (index, configs, expected) in [
        (
            0,
            json!({"remote": remote, "inline": inline}),
            ["remote", "inline", "public", "gate"],
        ),
        (
            last,
            json!({"inline": inline, "remote": remote}),
            ["public", "gate", "inline", "remote"],
        ),
    ] {
        state
            .as_object_mut()
            .unwrap()
            .shift_insert(index, "dynamic_configs".into(), configs);
        let names: Vec<_> = envelopes(&codec::encode_full(&state).unwrap())
            .into_iter()
            .map(|frame| frame.name)
            .filter(|name| !name.is_empty())
            .collect();
        assert_eq!(names, expected);
    }
}

#[tokio::test]
async fn hydrates_changed_grown_shared_remote_values_through_http_adapter() {
    let mut blobs = Blobs::new();
    let (first, metadata) = remote_value(json!({"invented": [1, true]}), &mut blobs);
    let mut base = tiny_state();
    base["may_have_remote_config_metadata"] = json!(true);
    base["dynamic_configs"]["config"]["defaultValue"] = first;
    base["dynamic_configs"]["config"]["remoteConfigMetadata"] = metadata;
    let (grown, metadata) = remote_value(
        json!({"invented": [2, false], "larger": "x".repeat(2048)}),
        &mut blobs,
    );
    let mut client = start_full(&base, &blobs).await;
    // CopyPrev retains the hydrated references without emitting any remote envelopes.
    let mut cursor = base.clone();
    cursor["time"] = json!(2);
    cursor["checksum"] = json!("remote-cursor");
    client.apply_delta(&base, &cursor, &blobs).await;

    let mut changed = cursor.clone();
    changed["time"] = json!(3);
    changed["checksum"] = json!("remote-three");
    changed["dynamic_configs"]["config"]["defaultValue"] = grown.clone();
    changed["dynamic_configs"]["config"]["remoteConfigMetadata"] = metadata.clone();
    changed["dynamic_configs"]["config"]["checksum"] = json!("17");
    client.apply_delta(&cursor, &changed, &blobs).await;

    let mut shared = changed.clone();
    shared["time"] = json!(4);
    shared["checksum"] = json!("remote-shared");
    let mut other = tiny_state()["dynamic_configs"]["config"].take();
    other["entity"] = json!("experiment");
    other["checksum"] = json!("19");
    // Only the new rule emits metadata. Its value is already hydrated on the existing config.
    other["rules"] = json!([{
        "name": "remote", "id": "remote", "salt": "remote", "idType": "userID",
        "passPercentage": 100, "conditions": ["public"],
        "returnValue": grown, "remoteConfigMetadata": metadata
    }]);
    shared["dynamic_configs"]["other"] = other;
    client.apply_delta(&changed, &shared, &blobs).await;
    client.sdk.shutdown().await.unwrap();
    let full = start_full(&shared, &blobs).await;
    full.sdk.shutdown().await.unwrap();
}

#[test]
fn rejects_unsupported_forms_and_invalid_entity_checksums() {
    let mut missing = tiny_state();
    missing.as_object_mut().unwrap().remove("layer_configs");
    assert!(codec::encode_full(&missing).is_err());
    assert!(codec::encode_delta(&missing, &tiny_state()).is_err());
    for bad in [json!("not-a-number"), json!("4294967296"), json!(-1)] {
        let mut source = tiny_state();
        source["dynamic_configs"]["config"]["checksum"] = bad;
        assert!(codec::encode_full(&source).is_err());
        assert!(codec::encode_delta(&tiny_state(), &source).is_err());
    }
    let mut source = tiny_state();
    source["feature_gates"]["gate"]["defaultValue"] = json!({"not": "a boolean"});
    assert!(codec::encode_full(&source).is_err());
    let mut source = tiny_state();
    source["condition_map"]["public"]["type"] = json!("unsupported_condition");
    assert!(codec::encode_full(&source).is_err());
    let mut source = tiny_state();
    source["dynamic_configs"]["config"]["unsupportedField"] = json!(true);
    assert!(codec::encode_full(&source).is_err());

    let mut source = tiny_state();
    let (path, metadata) = remote_value(json!({"remote": true}), &mut Blobs::new());
    let mut layer = source["feature_gates"]["gate"].clone();
    layer["type"] = json!("dynamic_config");
    layer["entity"] = json!("layer");
    layer["defaultValue"] = path.clone();
    layer["rules"][0]["returnValue"] = path;
    source["layer_configs"]["layer"] = layer;
    for owner in [
        "/layer_configs/layer",
        "/layer_configs/layer/rules/0",
        "/feature_gates/gate",
        "/feature_gates/gate/rules/0",
    ] {
        source.pointer_mut(owner).unwrap()["remoteConfigMetadata"] = metadata.clone();
        assert!(codec::encode_full(&source).is_err(), "{owner}");
        source.pointer_mut(owner).unwrap()["remoteConfigMetadata"] = Value::Null;
    }
    assert!(codec::encode_full(&source).is_ok());
}

#[test]
fn rejects_invalid_condition_additional_values_before_writing_a_delta() {
    let before = tiny_state();
    let mut after = before.clone();
    after["condition_map"]["public"]["checksum"] = json!("6");
    for invalid in [json!([]), json!({"key": 3})] {
        after["condition_map"]["public"]["additionalValues"] = invalid;
        assert!(codec::encode_delta(&before, &after).is_err());
    }
}

#[tokio::test]
#[ignore = "Generate a synthetic suite and set STATSIG_BENCH_MANIFEST to its manifest.json"]
async fn generated_suite_full_and_delta_semantics() {
    let manifest_path =
        std::env::var("STATSIG_BENCH_MANIFEST").expect("set STATSIG_BENCH_MANIFEST");
    let manifest_path = Path::new(&manifest_path);
    let root = manifest_path.parent().unwrap();
    let manifest: Value = serde_json::from_slice(&std::fs::read(manifest_path).unwrap()).unwrap();
    let mut blobs = Blobs::new();
    for blob in manifest["blobs"].as_array().unwrap() {
        blobs.insert(
            blob["sha256"].as_str().unwrap().to_owned(),
            std::fs::read(root.join(blob["file"].as_str().unwrap())).unwrap(),
        );
    }
    let mut states = BTreeMap::new();
    for scenario in manifest["scenarios"].as_array().unwrap() {
        let id = scenario["state_id"].as_str().unwrap();
        states.insert(
            id,
            (root.join(scenario["file"].as_str().unwrap()), Vec::new()),
        );
    }
    for edge in manifest["next_states"].as_array().unwrap() {
        let before = edge["before"].as_str().unwrap();
        let after = edge["after"].as_str().unwrap();
        let path = states[after].0.clone();
        states.get_mut(before).unwrap().1.push((after, path));
    }
    for (name, (path, edges)) in states {
        eprintln!("full {name}");
        let before: Value = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
        let mut client = start_full(&before, &blobs).await;
        for (i, (target, path)) in edges.into_iter().enumerate() {
            if i > 0 {
                // Sibling transitions start from the same full snapshot.
                client.sdk.shutdown().await.unwrap();
                let bytes = codec::encode_full(&before).unwrap();
                client = Client::start(protobuf_response(bytes), &blobs).await;
            }
            eprintln!("delta {name} -> {target}");
            let after = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
            client.apply_delta(&before, &after, &blobs).await;
        }
        client.sdk.shutdown().await.unwrap();
    }
}
