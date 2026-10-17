mod utils;

use std::sync::{Arc, Mutex};

use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::{
    DynamicConfigEvaluationOptions, Statsig, StatsigOptions, StatsigUser,
    interned_string::InternedString, interned_values::InternedStore,
};
use tokio::time::{Duration, sleep, timeout};
use utils::{mock_data_store::MockDataStore, mock_event_logging_adapter::MockEventLoggingAdapter};
use wiremock::matchers::{header, method, path};
use wiremock::{Mock, MockServer, Request, Respond, ResponseTemplate};

const CONFIG: &str = "remote_mmap_config";
const DCS_PATH: &str = "/v2/download_config_specs";
const PREWARM_PATH: &str = "/prewarm_specs";
const RAW_BODY_MARKER: &str = "__raw_remote_mmap_body__";

struct RemoteValue {
    value: Value,
    body: Vec<u8>,
    sha: String,
}

impl RemoteValue {
    fn new() -> Self {
        let value = json!({
            "model": "conversation-model",
            "routing": {"enabled": true, "regions": ["us-west", "us-east"]},
            "limits": {"maxTokens": 4096, "temperature": 0.75},
            "systemPrompt": "A realistic configuration prompt. ".repeat(2048),
        });
        let body = serde_json::to_vec(&value).unwrap();
        let sha = Sha256::digest(&body)
            .iter()
            .map(|byte| format!("{byte:02x}"))
            .collect();
        Self { value, body, sha }
    }

    fn path(&self) -> String {
        format!("/v1/dynamic_config_value/{}", self.sha)
    }

    fn config(&self) -> Value {
        let mut config = inline_config(json!({"value": self.path()}));
        let metadata = json!({
            "sha256": self.sha, "byteLength": self.body.len(),
            "contentType": "application/json", "compression": "none",
        });
        config["remoteConfigMetadata"] = metadata.clone();
        config["rules"] = json!([{
            "name": "remote-user", "id": "remote-user", "salt": "rule",
            "idType": "userID", "passPercentage": 100,
            "conditions": ["remote-user"], "returnValue": {"value": self.path()},
            "remoteConfigMetadata": metadata,
        }]);
        // The producer checksum remains attached to hydrated artifacts and is
        // therefore insufficient to distinguish them from old placeholders.
        let checksum = crc32(&serde_json::to_vec(&config).unwrap()).to_string();
        config["checksum"] = json!(checksum);
        config
    }
}

fn inline_config(value: Value) -> Value {
    json!({
        "type": "dynamic_config", "salt": "mmap-json-reuse", "enabled": true,
        "defaultValue": value, "rules": [], "idType": "userID",
        "entity": "dynamic_config", "version": 1,
    })
}

fn full(generation: u64, config: Value) -> Value {
    json!({
        "dynamic_configs": {
            CONFIG: config,
            "ordinary_config": inline_config(json!({"generation": generation})),
        },
        "feature_gates": {}, "layer_configs": {}, "experiment_to_layer": {},
        "has_updates": true, "time": generation,
        "checksum": format!("response-{generation}"), "company_id": "mmap-json-test",
        "response_format": "dcs-v2",
        "condition_map": {"remote-user": {
            "type": "user_field", "field": "userID", "operator": "any",
            "targetValue": ["remote-user"], "idType": "userID",
        }},
    })
}

#[derive(Clone)]
struct CurrentDcs(Arc<Mutex<Value>>);

impl Respond for CurrentDcs {
    fn respond(&self, _request: &Request) -> ResponseTemplate {
        ResponseTemplate::new(200)
            .insert_header("content-type", "application/json")
            .set_body_json(self.0.lock().unwrap().clone())
    }
}

#[derive(Clone, Copy)]
enum Artifact {
    Hydrated,
    StalePlaceholder,
    EquivalentDifferentBacking,
    SameBackingDifferentSpec,
}

rusty_fork_test! {
    #[test]
    fn json_hydrated_mmap_spec_survives_initialization_and_full_refresh() {
        run(Artifact::Hydrated);
    }

    #[test]
    fn json_stale_mmap_placeholder_with_same_checksum_is_not_reused() {
        run(Artifact::StalePlaceholder);
    }

    #[test]
    fn json_semantically_equal_mmap_with_different_verified_backing_is_not_reused() {
        run(Artifact::EquivalentDifferentBacking);
    }

    #[test]
    fn json_same_backing_and_checksum_with_changed_spec_content_is_not_reused() {
        run(Artifact::SameBackingDifferentSpec);
    }
}

fn run(artifact: Artifact) {
    // Each case installs immutable process-global mmap state.
    tokio::runtime::Builder::new_multi_thread()
        .worker_threads(2)
        .enable_all()
        .build()
        .unwrap()
        .block_on(run_case(artifact));
}

async fn run_case(artifact: Artifact) {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    let sdk_key = format!("secret-json-mmap-reuse-{}", std::process::id());
    let remote = RemoteValue::new();
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(remote.path()))
        .and(header("statsig-api-key", sdk_key.as_str()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(remote.body.clone()),
        )
        .mount(&server)
        .await;

    let wire_config = remote.config();
    let mut preload_config = wire_config.clone();
    let mut preload_bytes = None;
    match artifact {
        Artifact::Hydrated => {}
        Artifact::SameBackingDifferentSpec => {
            // Keep the authenticated blob body and producer checksum equal;
            // matching only either of them must not reuse a stale spec field.
            preload_config["enabled"] = json!(false);
        }
        Artifact::StalePlaceholder => {
            preload_config
                .as_object_mut()
                .unwrap()
                .remove("remoteConfigMetadata");
            preload_config["rules"][0]
                .as_object_mut()
                .unwrap()
                .remove("remoteConfigMetadata");
        }
        Artifact::EquivalentDifferentBacking => {
            preload_config
                .as_object_mut()
                .unwrap()
                .remove("remoteConfigMetadata");
            preload_config["rules"][0]
                .as_object_mut()
                .unwrap()
                .remove("remoteConfigMetadata");
            preload_config["defaultValue"] = json!(RAW_BODY_MARKER);
            preload_config["rules"][0]["returnValue"] = json!(RAW_BODY_MARKER);
            // Validated wire bytes and this artifact have equal parsed maps
            // but different raw returnable hashes and immutable backing.
            let different_body = serde_json::to_string_pretty(&remote.value).unwrap();
            assert_ne!(different_body.as_bytes(), remote.body);
            preload_bytes = Some(
                serde_json::to_string(&full(1, preload_config.clone()))
                    .unwrap()
                    .replace(&format!("\"{RAW_BODY_MARKER}\""), &different_body)
                    .into_bytes(),
            );
        }
    }
    let preload_bytes =
        preload_bytes.unwrap_or_else(|| serde_json::to_vec(&full(1, preload_config)).unwrap());
    Mock::given(method("GET"))
        .and(path(PREWARM_PATH))
        .and(header("statsig-api-key", sdk_key.as_str()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(preload_bytes),
        )
        .mount(&server)
        .await;
    InternedStore::fetch_and_write_mmap_with_specs_url(
        &sdk_key,
        &format!("{}{PREWARM_PATH}", server.uri()),
    )
    .await
    .unwrap();
    InternedStore::preload_mmap(&sdk_key).unwrap();
    let name = InternedString::from_str_ref(CONFIG);
    let preloaded = InternedStore::try_get_preloaded_dynamic_config(&name).unwrap();
    assert!(
        preloaded
            .as_spec_ref()
            .default_value
            .get_json_archived_ref()
            .is_some()
    );
    assert_eq!(
        preloaded.as_spec_ref().checksum.as_ref().unwrap().as_str(),
        wire_config["checksum"].as_str().unwrap(),
    );
    if matches!(artifact, Artifact::EquivalentDifferentBacking) {
        assert_eq!(
            serde_json::to_value(&preloaded.as_spec_ref().default_value).unwrap(),
            remote.value,
        );
        assert!(InternedStore::try_get_preloaded_returnable(&remote.body).is_none());
    }

    let dcs = CurrentDcs(Arc::new(Mutex::new(full(1, wire_config.clone()))));
    Mock::given(method("GET"))
        .and(path(DCS_PATH))
        .and(header("statsig-api-key", sdk_key.as_str()))
        .respond_with(dcs.clone())
        .mount(&server)
        .await;
    let sdk = Statsig::new(
        &sdk_key,
        Some(Arc::new(StatsigOptions {
            data_store: Some(Arc::new(
                MockDataStore::new_with_byte_cache(false).with_read_only(true),
            )),
            specs_url: Some(format!("{}{DCS_PATH}", server.uri())),
            remote_config_value_source_url: Some(server.uri()),
            event_logging_adapter: Some(Arc::new(
                MockEventLoggingAdapter::new_with_background_flush(false),
            )),
            specs_sync_interval_ms: Some(50),
            enable_id_lists: Some(false),
            disable_country_lookup: Some(true),
            fallback_to_statsig_api: Some(false),
            disable_all_logging: Some(true),
            ..StatsigOptions::new()
        })),
    );
    sdk.initialize().await.unwrap();
    assert_current(&sdk, &remote, &preloaded, artifact);
    let downloads = count(&server, &remote.path()).await;
    assert_eq!(
        downloads,
        if matches!(
            artifact,
            Artifact::Hydrated | Artifact::SameBackingDifferentSpec
        ) {
            2
        } else {
            1
        }
    );

    *dcs.0.lock().unwrap() = full(2, wire_config);
    timeout(Duration::from_secs(5), async {
        while sdk.specs_snapshot().time != 2 {
            sleep(Duration::from_millis(10)).await;
        }
    })
    .await
    .unwrap();
    assert_current(&sdk, &remote, &preloaded, artifact);
    assert_eq!(count(&server, &remote.path()).await, downloads);
    sdk.shutdown().await.unwrap();
}

fn assert_current(
    sdk: &Statsig,
    remote: &RemoteValue,
    preloaded: &statsig_rust::specs_response::specs_hash_map::SpecPointer,
    artifact: Artifact,
) {
    for user in ["default-user", "remote-user"] {
        let value = sdk.get_dynamic_config_with_options(
            &StatsigUser::with_user_id(user),
            CONFIG,
            DynamicConfigEvaluationOptions {
                disable_exposure_logging: true,
            },
        );
        assert_eq!(serde_json::to_value(value.value).unwrap(), remote.value);
    }
    let snapshot = sdk.specs_snapshot();
    assert_eq!(snapshot.dynamic_configs.len(), 2);
    let current = snapshot
        .dynamic_configs
        .get(&InternedString::from_str_ref(CONFIG))
        .unwrap();
    assert!(current.as_spec_ref().enabled);
    assert_eq!(
        std::ptr::eq(current.as_spec_ref(), preloaded.as_spec_ref()),
        matches!(artifact, Artifact::Hydrated),
        "only the exact, verified hydrated mmap spec should be reused",
    );
    if matches!(artifact, Artifact::Hydrated) {
        assert!(std::ptr::eq(
            current
                .as_spec_ref()
                .default_value
                .get_json_archived_ref()
                .unwrap(),
            preloaded
                .as_spec_ref()
                .default_value
                .get_json_archived_ref()
                .unwrap(),
        ));
        assert!(std::ptr::eq(
            current.as_spec_ref().rules[0]
                .return_value
                .get_json_archived_ref()
                .unwrap(),
            preloaded.as_spec_ref().rules[0]
                .return_value
                .get_json_archived_ref()
                .unwrap(),
        ));
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
