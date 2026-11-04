mod utils;

use std::{
    io::{Read, Write},
    sync::Arc,
};

use prost::Message;
use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::{
    DynamicConfigEvaluationOptions, SpecAdapterConfig, SpecsAdapterType, SpecsSource, Statsig,
    StatsigOptions, StatsigUser,
    hashing::djb2,
    interned_values::{InternedStore, MmapPreloadOptions, MmapWriteOutcome},
    specs_response::statsig_config_specs::{self as pb, any_value, return_value},
};
use utils::{mock_data_store::MockDataStore, mock_event_logging_adapter::MockEventLoggingAdapter};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, Request, Respond, ResponseTemplate};

const PREWARM_PATH: &str = "/prewarm_specs";
const DCS_PATH: &str = "/v2/download_config_specs";

#[derive(Clone, Copy)]
enum Format {
    Json,
    Protobuf,
}

#[derive(Clone, Copy)]
enum Change {
    None,
    ProoflessArtifact,
    InlineRule,
    Blob,
    MetadataLength,
    SdkKey,
    WritableDataStore,
    SixHundredBlobs,
}

struct RemoteValue {
    name: String,
    body: Vec<u8>,
    value: Value,
    sha: String,
}

impl RemoteValue {
    fn new(index: usize, changed: bool) -> Self {
        let marker = if changed { "changed" } else { "original" };
        let padding = "a realistic model configuration. ".repeat(4096);
        let encoded_padding = serde_json::to_string(&padding).unwrap();
        let body = match index {
            0 => format!(
                "{{ \"marker\" : \"{marker}\", \"nested\" : {{\"z\":2,\"a\":1}}, \"padding\" : {encoded_padding} }}"
            ),
            1 => format!(
                "{{\"z\":\"{marker}\",\"a\":true,\"nested\":{{\"z\":2,\"a\":1}},\"padding\":{encoded_padding}}}"
            ),
            2 => format!(
                "{{\"marker\":\"{marker}\",\"exponent\":1e0,\"decimal\":2.5000,\"negativeZero\":-0.0,\"padding\":{encoded_padding}}}"
            ),
            _ => unreachable!(),
        }
        .into_bytes();
        let value = serde_json::from_slice(&body).unwrap();
        let sha = hex_sha256(&body);
        Self {
            name: format!("mmap_blob_{index}"),
            body,
            value,
            sha,
        }
    }

    fn path(&self) -> String {
        format!("/v1/dynamic_config_value/{}", self.sha)
    }

    fn small(index: usize) -> Self {
        // Exercise proof-table cardinality without a large payload. Keep the
        // whitespace noncanonical so reuse needs the original-body proof.
        let body = format!(
            "{{ \"marker\": \"blob-{index}\", \"padding\": \"{}\" }}",
            "x".repeat(128),
        )
        .into_bytes();
        Self {
            name: format!("mmap_blob_{index}"),
            value: serde_json::from_slice(&body).unwrap(),
            sha: hex_sha256(&body),
            body,
        }
    }

    fn metadata(&self, invalid_length: bool) -> pb::RemoteConfigValueMetadata {
        pb::RemoteConfigValueMetadata {
            sha256: self.sha.clone(),
            byte_length: (self.body.len() + usize::from(invalid_length)) as u64,
            content_type: "application/json".to_string(),
            compression: "none".to_string(),
        }
    }

    fn json_config(&self, normal_generation: u64, invalid_length: bool) -> Value {
        let metadata = self.metadata(invalid_length);
        let metadata = json!({
            "sha256": metadata.sha256,
            "byteLength": metadata.byte_length,
            "contentType": metadata.content_type,
            "compression": metadata.compression,
        });
        let mut config = json!({
            "type": "dynamic_config", "salt": "mmap-proof", "enabled": true,
            "defaultValue": {"value": self.path()},
            "remoteConfigMetadata": metadata,
            "rules": [
                {
                    "name": "remote-user", "id": "remote-user", "salt": "remote-rule",
                    "idType": "userID", "passPercentage": 100,
                    "conditions": ["remote-user"],
                    "returnValue": {"value": self.path()},
                    "remoteConfigMetadata": metadata,
                },
                {
                    "name": "normal-user", "id": "normal-user", "salt": "normal-rule",
                    "idType": "userID", "passPercentage": 100,
                    "conditions": ["normal-user"],
                    "returnValue": {"generation": normal_generation},
                }
            ],
            "idType": "userID", "entity": "dynamic_config", "version": 1,
        });
        config["checksum"] = json!(crc32(&serde_json::to_vec(&config).unwrap()).to_string());
        config
    }

    fn proto_config(&self, normal_generation: u64, invalid_length: bool) -> pb::Spec {
        pb::Spec {
            salt: "mmap-proof".to_string(),
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            id_type: Some(user_id_type()),
            version: 1,
            default_value: Some(raw(json!({"value": self.path()}))),
            remote_config_metadata: Some(self.metadata(invalid_length)),
            rules: vec![
                pb::Rule {
                    name: "remote-user".to_string(),
                    id: "remote-user".to_string(),
                    salt: Some("remote-rule".to_string()),
                    id_type: Some(user_id_type()),
                    pass_percentage: 100,
                    conditions: vec!["remote-user".to_string()],
                    return_value: Some(raw(json!({"value": self.path()}))),
                    remote_config_metadata: Some(self.metadata(invalid_length)),
                    ..Default::default()
                },
                pb::Rule {
                    name: "normal-user".to_string(),
                    id: "normal-user".to_string(),
                    salt: Some("normal-rule".to_string()),
                    id_type: Some(user_id_type()),
                    pass_percentage: 100,
                    conditions: vec!["normal-user".to_string()],
                    return_value: Some(raw(json!({"generation": normal_generation}))),
                    ..Default::default()
                },
            ],
            ..Default::default()
        }
    }
}

#[derive(Clone)]
struct DcsResponse {
    format: Format,
    body: Vec<u8>,
    generation: u64,
}

impl Respond for DcsResponse {
    fn respond(&self, _request: &Request) -> ResponseTemplate {
        let response = ResponseTemplate::new(200).set_body_bytes(self.body.clone());
        match self.format {
            Format::Json => response.insert_header("content-type", "application/json"),
            Format::Protobuf => response
                .insert_header("content-type", "application/octet-stream")
                .insert_header("content-encoding", "statsig-br")
                .insert_header("x-since-time", self.generation.to_string())
                .insert_header("x-checksum", format!("response-{}", self.generation)),
        }
    }
}

fn response(
    format: Format,
    remotes: &[RemoteValue],
    generation: u64,
    normal_generation: u64,
    invalid_length: bool,
) -> DcsResponse {
    let body = match format {
        Format::Json => {
            let configs: serde_json::Map<String, Value> = remotes
                .iter()
                .enumerate()
                .map(|(index, remote)| {
                    (
                        remote.name.clone(),
                        remote.json_config(normal_generation, invalid_length && index == 0),
                    )
                })
                .collect();
            serde_json::to_vec(&json!({
                "dynamic_configs": configs, "feature_gates": {}, "layer_configs": {},
                "experiment_to_layer": {}, "has_updates": true, "time": generation,
                "checksum": format!("response-{generation}"), "company_id": "mmap-proof-company",
                "response_format": "dcs-v2", "condition_map": {
                    "remote-user": user_condition("remote-user"),
                    "normal-user": user_condition("normal-user"),
                },
            }))
            .unwrap()
        }
        Format::Protobuf => {
            let mut envelopes = vec![
                envelope(
                    pb::SpecsEnvelopeKind::TopLevel,
                    "",
                    "",
                    pb::SpecsTopLevel {
                        has_updates: true,
                        time: generation,
                        company_id: "mmap-proof-company".to_string(),
                        response_format: "dcs-v2".to_string(),
                        checksum: format!("response-{generation}"),
                        rest: br#"{"experiment_to_layer":{},"condition_map":{}}"#.to_vec(),
                        may_have_remote_config_metadata: Some(true),
                    }
                    .encode_to_vec(),
                ),
                condition("remote-user"),
                condition("normal-user"),
            ];
            for (index, remote) in remotes.iter().enumerate() {
                let invalid = invalid_length && index == 0;
                let config = remote.json_config(normal_generation, invalid);
                envelopes.push(envelope(
                    pb::SpecsEnvelopeKind::DynamicConfig,
                    &remote.name,
                    config["checksum"].as_str().unwrap(),
                    remote
                        .proto_config(normal_generation, invalid)
                        .encode_to_vec(),
                ));
            }
            envelopes.push(pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Done as i32,
                ..Default::default()
            });
            let mut encoded = Vec::new();
            for envelope in envelopes {
                envelope.encode_length_delimited(&mut encoded).unwrap();
            }
            let mut compressed = brotli::CompressorWriter::new(Vec::new(), 4096, 2, 22);
            compressed.write_all(&encoded).unwrap();
            compressed.into_inner()
        }
    };
    DcsResponse {
        format,
        body,
        generation,
    }
}

rusty_fork_test! {
    #[test]
    fn protobuf_mmap_proofs_avoid_downloads_for_noncanonical_blob_bytes() {
        run(Format::Protobuf, Change::None);
    }

    #[test]
    fn json_mmap_proofs_avoid_downloads_for_noncanonical_blob_bytes() {
        run(Format::Json, Change::None);
    }

    #[test]
    fn protobuf_mmap_reuse_preserves_download_fallback_for_old_artifacts() {
        run(Format::Protobuf, Change::ProoflessArtifact);
    }

    #[test]
    fn json_mmap_reuse_preserves_download_fallback_for_old_artifacts() {
        run(Format::Json, Change::ProoflessArtifact);
    }

    #[test]
    fn mmap_blob_reuse_survives_an_inline_rule_changing_in_the_same_config() {
        run(Format::Protobuf, Change::InlineRule);
    }

    #[test]
    fn mmap_blob_reuse_downloads_only_a_changed_sha() {
        run(Format::Protobuf, Change::Blob);
    }

    #[test]
    fn mmap_blob_reuse_rejects_conflicting_length_metadata() {
        run(Format::Protobuf, Change::MetadataLength);
    }

    #[test]
    fn mmap_blob_proofs_are_scoped_to_the_loaded_sdk_key() {
        run(Format::Protobuf, Change::SdkKey);
    }

    #[test]
    fn protobuf_mmap_reuse_preserves_writable_datastore_and_offline_followers() {
        run(Format::Protobuf, Change::WritableDataStore);
    }

    #[test]
    fn json_mmap_reuse_downloads_numeric_bodies_for_lossless_writable_sidecars() {
        run(Format::Json, Change::WritableDataStore);
    }

    #[test]
    fn mmap_blob_sidecar_reuses_all_six_hundred_values() {
        run(Format::Protobuf, Change::SixHundredBlobs);
    }
}

fn manifest_path(directory: &std::path::Path, sdk_key: &str) -> std::path::PathBuf {
    directory
        .join("statsig-interned-store")
        .join(format!("{}_interned_store_manifest.json", djb2(sdk_key)))
}

fn proofless_manifest(bytes: &[u8]) -> Vec<u8> {
    let mut manifest: Value = serde_json::from_slice(bytes).unwrap();
    // Older writers omit these optional fields. Keep the exact committed
    // V2 identity so preload still exercises a valid legacy publication.
    assert!(manifest.get("v2").is_some());
    let fields = manifest.as_object_mut().unwrap();
    let had_file = fields.remove("remote_values_file").is_some();
    let had_inline = fields.remove("remote_values").is_some();
    assert!(had_file || had_inline);
    serde_json::to_vec(&manifest).unwrap()
}

fn read_blob_proof_sidecar(manifest_file: &std::path::Path, manifest: &[u8]) -> (Vec<u8>, Value) {
    let manifest: Value = serde_json::from_slice(manifest).unwrap();
    let reference = &manifest["remote_values_file"];
    assert_eq!(reference["version"], json!(1));
    let digest = reference["sha256"].as_str().unwrap();
    let sidecar_file = manifest_file.with_extension("blob-proofs.json");
    let bytes = std::fs::read(sidecar_file).unwrap();
    assert_eq!(hex_sha256(&bytes), digest);
    let sidecar: Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(sidecar["v2"], manifest["v2"]);
    (bytes, sidecar)
}

fn hex_sha256(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn run(format: Format, change: Change) {
    // The reader installs immutable process-global mmap state. Each test runs
    // in its own child process.
    tokio::runtime::Builder::new_multi_thread()
        .worker_threads(2)
        .enable_all()
        .build()
        .unwrap()
        .block_on(run_case(format, change));
}

async fn run_case(format: Format, change: Change) {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    std::env::remove_var("STATSIG_ENABLE_COLD_START_BLOB_FALLBACK");
    let sdk_key = format!("secret-mmap-verified-blob-{}", std::process::id());
    let six_hundred = matches!(change, Change::SixHundredBlobs);
    let fixture = |index| {
        if six_hundred {
            RemoteValue::small(index)
        } else {
            RemoteValue::new(index, false)
        }
    };
    let remotes: Vec<_> = (0..if six_hundred { 600 } else { 3 })
        .map(fixture)
        .collect();
    let server = MockServer::start().await;
    for remote in &remotes {
        mount_blob(&server, remote).await;
    }
    Mock::given(method("GET"))
        .and(path(PREWARM_PATH))
        .respond_with(response(format, &remotes, 1, 1, false))
        .mount(&server)
        .await;

    let outcome = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        &sdk_key,
        &format!("{}{PREWARM_PATH}", server.uri()),
        None,
    )
    .await
    .unwrap();
    assert!(matches!(outcome, MmapWriteOutcome::Published(_)));
    for remote in &remotes {
        assert_eq!(
            count(&server, &remote.path()).await,
            1,
            "writer verifies each unique blob once"
        );
    }

    let manifest_file = manifest_path(&std::env::temp_dir(), &sdk_key);
    let manifest = std::fs::read(&manifest_file).unwrap();
    if six_hundred {
        assert!(
            manifest.len() < 64 * 1024,
            "legacy readers retain their manifest limit"
        );
        let (bytes, sidecar) = read_blob_proof_sidecar(&manifest_file, &manifest);
        assert!(
            bytes.len() > 64 * 1024,
            "the proof table must not be truncated to the manifest budget"
        );
        assert_eq!(
            sidecar["remote_values"]["values"].as_array().unwrap().len(),
            600
        );
    }
    let legacy_manifest = proofless_manifest(&manifest);
    if matches!(change, Change::ProoflessArtifact) {
        std::fs::write(&manifest_file, legacy_manifest).unwrap();
    }

    // Only the writer's on-disk publication is preloaded. The fresh SDK has no
    // previous live snapshot or per-instance verified remote-value registry.
    InternedStore::preload_mmap(&[&sdk_key], &[], &MmapPreloadOptions::default()).unwrap();
    assert!(InternedStore::has_preloaded_mmap_project(&sdk_key));
    let mut incoming: Vec<_> = (0..remotes.len()).map(fixture).collect();
    if matches!(change, Change::Blob) {
        incoming[0] = RemoteValue::new(0, true);
        mount_blob(&server, &incoming[0]).await;
    }
    let normal_generation = if matches!(change, Change::InlineRule) {
        2
    } else {
        1
    };
    let incoming_response = response(
        format,
        &incoming,
        2,
        normal_generation,
        matches!(change, Change::MetadataLength),
    );
    Mock::given(method("GET"))
        .and(path(DCS_PATH))
        .respond_with(incoming_response)
        .mount(&server)
        .await;
    let reader_key = if matches!(change, Change::SdkKey) {
        format!("{sdk_key}-other-project")
    } else {
        sdk_key
    };
    let writable = matches!(change, Change::WritableDataStore);
    let store = Arc::new(MockDataStore::new_with_byte_cache(false).with_read_only(!writable));
    let sdk = Statsig::new(
        &reader_key,
        Some(Arc::new(StatsigOptions {
            data_store: Some(store.clone()),
            specs_url: Some(format!("{}{DCS_PATH}", server.uri())),
            remote_config_value_source_url: Some(server.uri()),
            event_logging_adapter: Some(Arc::new(
                MockEventLoggingAdapter::new_with_background_flush(false),
            )),
            specs_sync_interval_ms: Some(60_000),
            enable_id_lists: Some(false),
            disable_country_lookup: Some(true),
            fallback_to_statsig_api: Some(false),
            disable_all_logging: Some(true),
            ..StatsigOptions::new()
        })),
    );
    let initialization = sdk.initialize().await;
    if matches!(change, Change::MetadataLength) {
        // A same-SHA proof with different metadata must not silently authorize
        // the value. The normal download verifies and rejects the bad length.
        assert!(count(&server, &remotes[0].path()).await > 1);
        assert!(sdk.specs_snapshot().dynamic_configs.is_empty());
    } else {
        initialization.unwrap();
        assert_eq!(sdk.specs_snapshot().time, 2);
        for remote in &incoming {
            for user in ["default-user", "remote-user"] {
                let actual = evaluate(&sdk, user, &remote.name);
                assert_semantic_json_eq(&actual, &remote.value);
            }
            assert_eq!(
                evaluate(&sdk, "normal-user", &remote.name),
                json!({"generation": normal_generation}),
                "current inline rules must not be replaced by stale mmap spec fields",
            );
        }
        let writable_json_numbers = writable && matches!(format, Format::Json);
        let reuse_available =
            !matches!(change, Change::ProoflessArtifact | Change::SdkKey) && !writable_json_numbers;
        for (index, remote) in incoming.iter().enumerate() {
            let changed = index == 0 && matches!(change, Change::Blob);
            let writer_gets = usize::from(!changed);
            let reader_gets = usize::from(changed || !reuse_available);
            let gets = count(&server, &remote.path()).await;
            if index == 1 && !reuse_available && !writable_json_numbers {
                // Hash-map iteration can coincidentally reconstruct this
                // compact fixture's original order. Either conservative
                // outcome is valid; whitespace and numeric fixtures below
                // deterministically require a baseline download.
                assert!((writer_gets..=writer_gets + reader_gets).contains(&gets));
            } else {
                assert_eq!(gets, writer_gets + reader_gets);
            }
        }
    }
    if writable {
        tokio::time::timeout(
            std::time::Duration::from_secs(5),
            sdk.statsig_runtime
                .await_tasks_with_tag("spec_store_update_data_store"),
        )
        .await
        .expect("hydrated datastore publication should complete");
        assert!(store.num_set_bytes_calls() > 0);
        assert_hydrated_sidecar(format, &store, &incoming);
    }
    sdk.shutdown().await.unwrap();
    if writable {
        assert_offline_follower(format, &server, &reader_key, &store, &incoming).await;
    }
}

fn assert_hydrated_sidecar(format: Format, store: &MockDataStore, remotes: &[RemoteValue]) {
    match format {
        Format::Json => {
            let bytes = store.stored_json_bytes().unwrap();
            let text = std::str::from_utf8(&bytes).unwrap();
            assert!(!text.contains("/v1/dynamic_config_value/"));
            // All three fixtures contain numeric JSON. Writable JSON must
            // retain original numeric lexemes rather than serialize mmap data.
            for fragment in [
                "\"exponent\":1e0",
                "\"decimal\":2.5000",
                "\"negativeZero\":-0.0",
            ] {
                assert!(
                    text.contains(fragment),
                    "missing original number {fragment}"
                );
            }
            let sidecar: Value = serde_json::from_slice(&bytes).unwrap();
            for remote in remotes {
                let config = &sidecar["dynamic_configs"][&remote.name];
                assert!(config.get("remoteConfigMetadata").is_none());
                assert!(config["rules"][0].get("remoteConfigMetadata").is_none());
                assert_semantic_json_eq(&config["defaultValue"], &remote.value);
                assert_semantic_json_eq(&config["rules"][0]["returnValue"], &remote.value);
            }
        }
        Format::Protobuf => {
            let compressed = store.stored_proto_bytes().unwrap();
            let mut bytes = Vec::new();
            brotli::Decompressor::new(compressed.as_slice(), 4096)
                .read_to_end(&mut bytes)
                .unwrap();
            let mut remaining = bytes.as_slice();
            let mut checked = 0;
            while !remaining.is_empty() {
                let envelope = pb::SpecsEnvelope::decode_length_delimited(&mut remaining).unwrap();
                let Some(remote) = remotes.iter().find(|remote| remote.name == envelope.name)
                else {
                    continue;
                };
                let config = pb::Spec::decode(envelope.data.as_deref().unwrap()).unwrap();
                assert!(config.remote_config_metadata.is_none());
                assert!(config.rules[0].remote_config_metadata.is_none());
                for value in [
                    config.default_value.as_ref().unwrap(),
                    config.rules[0].return_value.as_ref().unwrap(),
                ] {
                    let Some(return_value::Value::RawValue(bytes)) = &value.value else {
                        panic!("hydrated protobuf sidecar must contain an inline value");
                    };
                    assert_semantic_json_eq(
                        &serde_json::from_slice::<Value>(bytes).unwrap(),
                        &remote.value,
                    );
                }
                checked += 1;
            }
            assert_eq!(checked, remotes.len());
        }
    }
}

async fn assert_offline_follower(
    format: Format,
    server: &MockServer,
    sdk_key: &str,
    store: &MockDataStore,
    remotes: &[RemoteValue],
) {
    server.reset().await;
    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(503))
        .expect(0)
        .mount(server)
        .await;
    let follower_store = match format {
        Format::Json => MockDataStore::with_json_cache(
            std::str::from_utf8(&store.stored_json_bytes().unwrap()).unwrap(),
        ),
        Format::Protobuf => MockDataStore::with_proto_cache(&store.stored_proto_bytes().unwrap()),
    }
    .with_read_only(true);
    let follower = Statsig::new(
        sdk_key,
        Some(Arc::new(StatsigOptions {
            data_store: Some(Arc::new(follower_store)),
            spec_adapters_config: Some(vec![SpecAdapterConfig {
                adapter_type: SpecsAdapterType::DataStore,
                init_timeout_ms: 1000,
                specs_url: None,
                authentication_mode: None,
                ca_cert_path: None,
                client_cert_path: None,
                client_key_path: None,
                domain_name: None,
            }]),
            remote_config_value_source_url: Some(server.uri()),
            enable_id_lists: Some(false),
            disable_country_lookup: Some(true),
            fallback_to_statsig_api: Some(false),
            disable_all_logging: Some(true),
            event_logging_adapter: Some(Arc::new(
                MockEventLoggingAdapter::new_with_background_flush(false),
            )),
            ..StatsigOptions::new()
        })),
    );
    let details = follower.initialize_with_details().await.unwrap();
    assert!(details.init_success);
    assert_eq!(
        details.source,
        SpecsSource::Adapter("DataStore".to_string())
    );
    assert_eq!(follower.specs_snapshot().time, 2);
    for remote in remotes {
        for user in ["default-user", "remote-user"] {
            assert_semantic_json_eq(&evaluate(&follower, user, &remote.name), &remote.value);
        }
        assert_eq!(
            evaluate(&follower, "normal-user", &remote.name),
            json!({"generation": 1})
        );
    }
    follower.shutdown().await.unwrap();
    server.verify().await;
}

async fn mount_blob(server: &MockServer, remote: &RemoteValue) {
    Mock::given(method("GET"))
        .and(path(remote.path()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(remote.body.clone()),
        )
        .mount(server)
        .await;
}

fn evaluate(sdk: &Statsig, user: &str, config: &str) -> Value {
    let evaluation = sdk.get_dynamic_config_with_options(
        &StatsigUser::with_user_id(user),
        config,
        DynamicConfigEvaluationOptions {
            disable_exposure_logging: true,
        },
    );
    serde_json::to_value(evaluation.value).unwrap()
}

fn assert_semantic_json_eq(actual: &Value, expected: &Value) {
    match (actual, expected) {
        (Value::Number(actual), Value::Number(expected)) => {
            assert_eq!(
                actual.as_f64().unwrap().to_bits(),
                expected.as_f64().unwrap().to_bits()
            );
        }
        (Value::Object(actual), Value::Object(expected)) => {
            assert_eq!(actual.len(), expected.len());
            for (key, expected) in expected {
                assert_semantic_json_eq(actual.get(key).unwrap(), expected);
            }
        }
        _ => assert_eq!(actual, expected),
    }
}

async fn count(server: &MockServer, request_path: &str) -> usize {
    server
        .received_requests()
        .await
        .unwrap()
        .iter()
        .filter(|request| request.url.path() == request_path)
        .count()
}

fn user_id_type() -> pb::IdType {
    pb::IdType {
        id_type: Some(pb::id_type::IdType::KnownIdType(
            pb::KnownIdType::UserId as i32,
        )),
    }
}

fn user_condition(name: &str) -> Value {
    json!({"type": "user_field", "field": "userID", "operator": "any", "targetValue": [name], "idType": "userID"})
}

fn condition(name: &str) -> pb::SpecsEnvelope {
    let value = pb::Condition {
        condition_type: pb::ConditionType::UserField as i32,
        id_type: Some(user_id_type()),
        field: Some("userID".to_string()),
        operator: Some(pb::Operator::Any as i32),
        target_value: Some(pb::AnyValue {
            value: Some(any_value::Value::RawValue(
                serde_json::to_vec(&json!([name])).unwrap(),
            )),
        }),
        ..Default::default()
    };
    envelope(
        pb::SpecsEnvelopeKind::Condition,
        name,
        &crc32(&value.encode_to_vec()).to_string(),
        value.encode_to_vec(),
    )
}

fn raw(value: Value) -> pb::ReturnValue {
    pb::ReturnValue {
        value: Some(return_value::Value::RawValue(
            serde_json::to_vec(&value).unwrap(),
        )),
    }
}

fn envelope(
    kind: pb::SpecsEnvelopeKind,
    name: &str,
    checksum: &str,
    data: Vec<u8>,
) -> pb::SpecsEnvelope {
    pb::SpecsEnvelope {
        kind: kind as i32,
        name: name.to_string(),
        checksum: checksum.to_string(),
        data: Some(data),
    }
}

fn crc32(bytes: &[u8]) -> u32 {
    let mut crc = u32::MAX;
    for &byte in bytes {
        crc ^= u32::from(byte);
        for _ in 0..8 {
            crc = (crc >> 1) ^ (0xedb88320 & 0u32.wrapping_sub(crc & 1));
        }
    }
    !crc
}
