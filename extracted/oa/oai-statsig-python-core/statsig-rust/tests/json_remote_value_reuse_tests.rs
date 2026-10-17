mod utils;

use std::sync::{
    Arc, Condvar, Mutex,
    atomic::{AtomicBool, Ordering},
};

use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::{
    DynamicConfigEvaluationOptions, SpecAdapterConfig, SpecsAdapterType, SpecsSource, SpecsUpdate,
    Statsig, StatsigOptions, StatsigUser, interned_string::InternedString,
    networking::ResponseData,
};
use tokio::time::{Duration, sleep, timeout};
use utils::{mock_data_store::MockDataStore, mock_event_logging_adapter::MockEventLoggingAdapter};
use wiremock::matchers::{header, method, path};
use wiremock::{Mock, MockServer, Request, Respond, ResponseTemplate};

const SDK_KEY: &str = "secret-json-verified-value-reuse";
const DCS_PATH: &str = "/v2/download_config_specs";
const BLOB_BYTES: usize = 256 * 1024;
const NUMBER_MARKER: &str = "__json_reuse_numeric_lexeme__";
const NUMBER_LEXEME: &str = "123456789012345678901234567890.00001";

struct RemoteValue {
    body: Vec<u8>,
    value: Value,
    sha: String,
}

impl RemoteValue {
    fn new(marker: &str, whitespace: bool) -> Self {
        // Reversed object keys and whitespace make the authenticated wire body
        // different from a serialization of the SDK's parsed map.
        let value = json!({"marker": marker, "nested": {"enabled": true}, "padding": "x".repeat(BLOB_BYTES)});
        let marker = serde_json::to_string(marker).unwrap();
        let padding = serde_json::to_string(&value["padding"]).unwrap();
        let body = if whitespace {
            format!("{{ \"padding\": {padding}, \"nested\": {{ \"enabled\": true }}, \"marker\": {marker} }}")
        } else {
            format!(r#"{{"padding":{padding},"nested":{{"enabled":true}},"marker":{marker}}}"#)
        }
        .into_bytes();
        assert_eq!(serde_json::from_slice::<Value>(&body).unwrap(), value);
        assert_ne!(serde_json::to_vec(&value).unwrap(), body);
        let sha = Sha256::digest(&body)
            .iter()
            .map(|byte| format!("{byte:02x}"))
            .collect();
        Self { body, value, sha }
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
}

#[derive(Clone)]
struct CurrentDcs(Arc<Mutex<(Value, Option<Value>)>>);

impl CurrentDcs {
    fn new(value: Value) -> Self {
        Self(Arc::new(Mutex::new((value, None))))
    }

    fn replace(&self, value: Value) {
        *self.0.lock().unwrap() = (value, None);
    }

    fn once(&self, value: Value, following: Value) {
        *self.0.lock().unwrap() = (value, Some(following));
    }
}

impl Respond for CurrentDcs {
    fn respond(&self, _request: &Request) -> ResponseTemplate {
        let mut current = self.0.lock().unwrap();
        // Construct this unrelated inline number directly on the wire. A Value
        // roundtrip would alter its precision/lexeme before the SDK saw it.
        let body = serde_json::to_string(&current.0)
            .unwrap()
            .replace(&format!("\"{NUMBER_MARKER}\""), NUMBER_LEXEME);
        let template = ResponseTemplate::new(200)
            .insert_header("content-type", "application/json")
            .set_body_bytes(body);
        if let Some(next) = current.1.take() {
            current.0 = next;
        }
        template
    }
}

#[derive(Clone)]
struct CurrentBlob {
    response: Arc<Mutex<ResponseTemplate>>,
    gate: Option<Arc<DownloadGate>>,
}

#[derive(Default)]
struct DownloadGate {
    started: AtomicBool,
    released: Mutex<bool>,
    ready: Condvar,
}

impl DownloadGate {
    fn wait(&self) {
        self.started.store(true, Ordering::SeqCst);
        let (released, _) = self
            .ready
            .wait_timeout_while(
                self.released.lock().unwrap(),
                Duration::from_secs(5),
                |released| !*released,
            )
            .unwrap();
        assert!(*released, "test did not release the local blob response");
    }

    fn release(&self) {
        *self.released.lock().unwrap() = true;
        self.ready.notify_all();
    }
}

impl CurrentBlob {
    async fn mount(server: &MockServer, remote: &RemoteValue) -> Self {
        Self::mount_with_gate(server, remote, None).await
    }

    async fn mount_with_gate(
        server: &MockServer,
        remote: &RemoteValue,
        gate: Option<Arc<DownloadGate>>,
    ) -> Self {
        let response = Self {
            response: Arc::new(Mutex::new(blob_response(remote))),
            gate,
        };
        Mock::given(method("GET"))
            .and(path(remote.path()))
            .and(header("statsig-api-key", SDK_KEY))
            .respond_with(response.clone())
            .mount(server)
            .await;
        response
    }

    fn replace(&self, response: ResponseTemplate) {
        *self.response.lock().unwrap() = response;
    }
}

impl Respond for CurrentBlob {
    fn respond(&self, _request: &Request) -> ResponseTemplate {
        if let Some(gate) = &self.gate {
            gate.wait();
        }
        self.response.lock().unwrap().clone()
    }
}

fn blob_response(remote: &RemoteValue) -> ResponseTemplate {
    ResponseTemplate::new(200)
        .insert_header("content-type", "application/json")
        .set_body_bytes(remote.body.clone())
}

fn inline_config(value: Value) -> Value {
    json!({
        "type": "dynamic_config", "salt": "json-reuse", "enabled": true,
        "defaultValue": value, "rules": [], "idType": "userID",
        "entity": "dynamic_config", "version": 1,
    })
}

fn remote_config(remote: &RemoteValue) -> Value {
    let mut config = inline_config(json!({"value": remote.path()}));
    config["remoteConfigMetadata"] = remote.metadata();
    config
}

fn full(generation: u64, normal_generation: u64, remote: Option<&RemoteValue>) -> Value {
    let mut configs = json!({
        "ordinary_config": inline_config(json!({"generation": generation})),
        "numeric_config": inline_config(json!({"wireNumber": NUMBER_MARKER})),
    });
    if let Some(remote) = remote {
        let mut large = remote_config(remote);
        large["rules"] = json!([
            {
                "name": "remote-rule", "id": "remote-rule", "salt": "remote",
                "idType": "userID", "passPercentage": 100, "conditions": ["remote-user"],
                "returnValue": {"value": remote.path()}, "remoteConfigMetadata": remote.metadata(),
            },
            {
                "name": "normal-rule", "id": "normal-rule", "salt": "normal",
                "idType": "userID", "passPercentage": 100, "conditions": ["normal-user"],
                "returnValue": {"normalGeneration": normal_generation},
            },
        ]);
        configs["large_config"] = large;
        configs["mirror_config"] = remote_config(remote);
    }
    let condition = |user| {
        json!({
            "type": "user_field", "field": "userID", "operator": "any",
            "targetValue": [user], "idType": "userID",
        })
    };
    json!({
        "dynamic_configs": configs, "feature_gates": {}, "layer_configs": {},
        "experiment_to_layer": {}, "has_updates": true, "time": generation,
        "checksum": format!("json-generation-{generation}"), "company_id": "json-reuse-test",
        "condition_map": {"remote-user": condition("remote-user"), "normal-user": condition("normal-user")},
        "response_format": "dcs-v2",
    })
}

fn no_update(generation: u64) -> Value {
    json!({"has_updates": false, "time": generation})
}

async fn initialize(
    server: &MockServer,
    dcs: &CurrentDcs,
    read_only: bool,
) -> (Statsig, Arc<MockDataStore>) {
    let store = Arc::new(MockDataStore::new_with_byte_cache(false).with_read_only(read_only));
    let sdk = initialize_with_store(server, dcs, store.clone()).await;
    (sdk, store)
}

async fn initialize_with_store(
    server: &MockServer,
    dcs: &CurrentDcs,
    store: Arc<MockDataStore>,
) -> Statsig {
    // Permit a short local polling interval, as in the protobuf reuse tests.
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    Mock::given(method("GET"))
        .and(path(DCS_PATH))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(dcs.clone())
        .mount(server)
        .await;
    let sdk = Statsig::new(
        SDK_KEY,
        Some(Arc::new(
            StatsigOptions {
                data_store: Some(store.clone()),
                specs_url: Some(format!("{}{DCS_PATH}", server.uri())),
                remote_config_value_source_url: Some(server.uri()),
                specs_sync_interval_ms: Some(40),
                enable_id_lists: Some(false),
                disable_country_lookup: Some(true),
                fallback_to_statsig_api: Some(false),
                disable_all_logging: Some(true),
                event_logging_adapter: Some(Arc::new(
                    MockEventLoggingAdapter::new_with_background_flush(false),
                )),
                ..StatsigOptions::new()
            }
            .suppress_diagnostic_output(true),
        )),
    );
    sdk.initialize().await.unwrap();
    sdk
}

fn evaluate(sdk: &Statsig, user: &str, config: &str) -> Value {
    let value = sdk.get_dynamic_config_with_options(
        &StatsigUser::with_user_id(user),
        config,
        DynamicConfigEvaluationOptions {
            disable_exposure_logging: true,
        },
    );
    serde_json::to_value(value.value).unwrap()
}

fn generation(sdk: &Statsig) -> u64 {
    sdk.specs_snapshot().time
}

fn assert_values(sdk: &Statsig, remote: &RemoteValue, normal_generation: u64) {
    assert_eq!(evaluate(sdk, "default-user", "large_config"), remote.value);
    assert_eq!(evaluate(sdk, "remote-user", "large_config"), remote.value);
    assert_eq!(evaluate(sdk, "default-user", "mirror_config"), remote.value);
    assert_eq!(
        evaluate(sdk, "normal-user", "large_config"),
        json!({"normalGeneration": normal_generation}),
    );
}

async fn wait_until(check: impl Fn() -> bool) {
    timeout(Duration::from_secs(5), async {
        while !check() {
            sleep(Duration::from_millis(10)).await;
        }
    })
    .await
    .expect("expected SDK state was not published");
}

async fn get_count(server: &MockServer, request_path: &str) -> usize {
    server
        .received_requests()
        .await
        .unwrap()
        .iter()
        .filter(|request| request.url.path() == request_path)
        .count()
}

async fn wait_requests(server: &MockServer, request_path: &str, minimum: usize) {
    timeout(Duration::from_secs(5), async {
        while get_count(server, request_path).await < minimum {
            sleep(Duration::from_millis(10)).await;
        }
    })
    .await
    .expect("expected local request was not received");
}

async fn await_writes(sdk: &Statsig) {
    timeout(
        Duration::from_secs(5),
        sdk.statsig_runtime
            .await_tasks_with_tag("spec_store_update_data_store"),
    )
    .await
    .expect("datastore publication should complete");
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn json_verified_values_survive_full_updates_without_redownload() {
    for whitespace in [false, true] {
        for read_only in [false, true] {
            let server = MockServer::start().await;
            let original = RemoteValue::new("original", whitespace);
            let changed = RemoteValue::new("changed", whitespace);
            let original_blob = CurrentBlob::mount(&server, &original).await;
            CurrentBlob::mount(&server, &changed).await;
            let dcs = CurrentDcs::new(full(1, 1, Some(&original)));
            let (sdk, store) = initialize(&server, &dcs, read_only).await;
            assert_values(&sdk, &original, 1);
            assert_eq!(get_count(&server, &original.path()).await, 1);
            let initial = sdk.specs_snapshot();
            let name = InternedString::from_str_ref("large_config");
            let initial_spec = initial.dynamic_configs.get(&name).unwrap().as_spec_ref();

            original_blob.replace(ResponseTemplate::new(503));
            dcs.replace(full(2, 1, Some(&original)));
            wait_until(|| generation(&sdk) == 2).await;
            assert_values(&sdk, &original, 1);
            assert_eq!(
                evaluate(&sdk, "user", "ordinary_config"),
                json!({"generation": 2})
            );
            dcs.replace(full(3, 2, Some(&original)));
            wait_until(|| generation(&sdk) == 3).await;
            assert_values(&sdk, &original, 2);
            assert_eq!(get_count(&server, &original.path()).await, 1);
            let refreshed = sdk.specs_snapshot();
            let refreshed_spec = refreshed.dynamic_configs.get(&name).unwrap().as_spec_ref();
            assert!(std::ptr::eq(
                initial_spec.default_value.get_json_pointer_ref().unwrap(),
                refreshed_spec.default_value.get_json_pointer_ref().unwrap(),
            ));
            assert!(std::ptr::eq(
                initial_spec.rules[0]
                    .return_value
                    .get_json_pointer_ref()
                    .unwrap(),
                refreshed_spec.rules[0]
                    .return_value
                    .get_json_pointer_ref()
                    .unwrap(),
            ));

            dcs.replace(full(4, 2, Some(&changed)));
            wait_until(|| generation(&sdk) == 4).await;
            assert_values(&sdk, &changed, 2);
            assert_eq!(get_count(&server, &changed.path()).await, 1);
            let polls = get_count(&server, DCS_PATH).await;
            wait_requests(&server, DCS_PATH, polls + 3).await;
            assert_eq!(get_count(&server, &changed.path()).await, 1);
            await_writes(&sdk).await;
            sdk.shutdown().await.unwrap();

            if read_only {
                assert_eq!(store.num_set_bytes_calls(), 0);
                assert_eq!(store.num_set_calls(), 0);
            } else {
                let bytes = store.stored_json_bytes().unwrap();
                assert!(
                    std::str::from_utf8(&bytes).unwrap().contains(NUMBER_LEXEME),
                    "JSON hydration reserialized an unrelated inline number"
                );
                let snapshot: Value = serde_json::from_slice(&bytes).unwrap();
                assert_eq!(snapshot["time"], 4);
                assert_eq!(
                    snapshot["dynamic_configs"]["large_config"]["defaultValue"],
                    changed.value
                );
                assert_eq!(
                    snapshot["dynamic_configs"]["large_config"]["rules"][0]["returnValue"],
                    changed.value
                );
                assert!(
                    snapshot["dynamic_configs"]["large_config"]
                        .get("remoteConfigMetadata")
                        .is_none()
                );
                assert!(
                    snapshot["dynamic_configs"]["large_config"]["rules"][0]
                        .get("remoteConfigMetadata")
                        .is_none()
                );
                assert_offline_follower(&server, &bytes, &changed).await;
            }
        }
    }
}

#[tokio::test]
async fn malformed_remote_rule_configs_do_not_break_offline_json_followers() {
    for malformed_rule_first in [false, true] {
        let server = MockServer::start().await;
        let remote = RemoteValue::new("malformed-neighbor", true);
        CurrentBlob::mount(&server, &remote).await;
        let mut payload = full(2, 2, Some(&remote));
        let remote_rule = payload["dynamic_configs"]["large_config"]["rules"][0].clone();
        let malformed_rule = json!("not-a-rule-object");
        let mut malformed = inline_config(json!({"kept": "inline"}));
        malformed["rules"] = if malformed_rule_first {
            json!([malformed_rule, remote_rule])
        } else {
            json!([remote_rule, malformed_rule])
        };
        payload["dynamic_configs"]["malformed_config"] = malformed;
        let dcs = CurrentDcs::new(payload.clone());
        dcs.once(payload, no_update(2));

        let (sdk, store) = initialize(&server, &dcs, false).await;
        assert_eq!(generation(&sdk), 2);
        assert_values(&sdk, &remote, 2);
        assert_eq!(
            evaluate(&sdk, "user", "ordinary_config"),
            json!({"generation": 2}),
        );
        assert!(
            !sdk.get_dynamic_config_list()
                .iter()
                .any(|name| name == "malformed_config"),
        );
        await_writes(&sdk).await;
        let bytes = store.stored_json_bytes().unwrap();
        sdk.shutdown().await.unwrap();

        // A fresh SDK must use the accepted sidecar without downloading the
        // skipped config's remote rule while its blob endpoint is unavailable.
        assert_offline_follower(&server, &bytes, &remote).await;
        let persisted: Value = serde_json::from_slice(&bytes).unwrap();
        assert!(
            persisted["dynamic_configs"]
                .get("malformed_config")
                .is_none()
        );
    }
}

#[tokio::test]
async fn numeric_remote_values_preserve_writable_sidecars_and_reuse_without_publication() {
    const REMOTE_NUMBER: &str = "18446744073709551617";
    for (read_only, write_once) in [(false, false), (true, false), (false, true)] {
        let server = MockServer::start().await;
        let body = format!(
            r#"{{"n":{REMOTE_NUMBER},"padding":{}}}"#,
            serde_json::to_string(&"x".repeat(BLOB_BYTES)).unwrap(),
        )
        .into_bytes();
        let parsed = serde_json::from_slice::<statsig_rust::DynamicReturnable>(&body).unwrap();
        let remote = RemoteValue {
            value: serde_json::to_value(parsed).unwrap(),
            sha: Sha256::digest(&body)
                .iter()
                .map(|byte| format!("{byte:02x}"))
                .collect(),
            body,
        };
        assert!(
            !serde_json::to_string(&remote.value)
                .unwrap()
                .contains(REMOTE_NUMBER),
            "fixture must expose SDK parsed-map numeric rounding",
        );
        let blob = CurrentBlob::mount(&server, &remote).await;
        let dcs = CurrentDcs::new(full(1, 1, Some(&remote)));
        dcs.once(full(1, 1, Some(&remote)), no_update(1));
        let mut store = MockDataStore::new_with_byte_cache(false).with_read_only(read_only);
        if write_once {
            store = store.with_write_once();
        }
        let store = Arc::new(store);
        let sdk = initialize_with_store(&server, &dcs, store.clone()).await;
        assert_values(&sdk, &remote, 1);
        assert_eq!(get_count(&server, &remote.path()).await, 1);
        await_writes(&sdk).await;
        let initial_sidecar = store.stored_json_bytes();
        if !read_only {
            assert!(
                std::str::from_utf8(initial_sidecar.as_ref().unwrap())
                    .unwrap()
                    .contains(REMOTE_NUMBER),
                "first JSON sidecar changed the authenticated number",
            );
        }

        // Numeric values can reuse their parsed backing when no new sidecar
        // will be written. Continuous writers need the original raw body.
        if read_only || write_once {
            blob.replace(ResponseTemplate::new(503));
        }
        dcs.once(full(2, 2, Some(&remote)), no_update(2));
        wait_until(|| generation(&sdk) == 2).await;
        assert_values(&sdk, &remote, 2);
        assert_eq!(
            evaluate(&sdk, "user", "ordinary_config"),
            json!({"generation": 2}),
        );
        assert_eq!(
            get_count(&server, &remote.path()).await,
            if read_only || write_once { 1 } else { 2 },
        );
        await_writes(&sdk).await;
        sdk.shutdown().await.unwrap();
        if read_only {
            assert_eq!(store.num_set_bytes_calls(), 0);
            assert_eq!(store.num_set_calls(), 0);
        } else if write_once {
            assert_eq!(store.num_set_bytes_calls(), 1);
            assert_eq!(store.stored_json_bytes(), initial_sidecar);
        } else {
            let sidecar = store.stored_json_bytes().unwrap();
            assert!(
                std::str::from_utf8(&sidecar)
                    .unwrap()
                    .contains(REMOTE_NUMBER),
                "reused numeric value rounded the continuously writable sidecar",
            );
            let snapshot: Value = serde_json::from_slice(&sidecar).unwrap();
            assert_eq!(snapshot["time"], 2);
        }
    }

    // Digits inside a string are lossless in the parsed representation. They
    // must not trigger the conservative numeric-token sidecar exception.
    let server = MockServer::start().await;
    let remote = RemoteValue::new(REMOTE_NUMBER, true);
    let blob = CurrentBlob::mount(&server, &remote).await;
    let dcs = CurrentDcs::new(full(1, 1, Some(&remote)));
    dcs.once(full(1, 1, Some(&remote)), no_update(1));
    let (sdk, store) = initialize(&server, &dcs, false).await;
    await_writes(&sdk).await;
    blob.replace(ResponseTemplate::new(503));
    dcs.once(full(2, 2, Some(&remote)), no_update(2));
    wait_until(|| generation(&sdk) == 2).await;
    assert_values(&sdk, &remote, 2);
    assert_eq!(get_count(&server, &remote.path()).await, 1);
    await_writes(&sdk).await;
    let snapshot: Value = serde_json::from_slice(&store.stored_json_bytes().unwrap()).unwrap();
    assert_eq!(snapshot["time"], 2);
    assert_eq!(
        snapshot["dynamic_configs"]["large_config"]["defaultValue"]["marker"],
        REMOTE_NUMBER
    );
    sdk.shutdown().await.unwrap();
}

async fn assert_offline_follower(server: &MockServer, bytes: &[u8], remote: &RemoteValue) {
    server.reset().await;
    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(503))
        .expect(0)
        .mount(server)
        .await;
    let store = Arc::new(
        MockDataStore::with_json_cache(std::str::from_utf8(bytes).unwrap()).with_read_only(true),
    );
    let follower = Statsig::new(
        SDK_KEY,
        Some(Arc::new(
            StatsigOptions {
                data_store: Some(store),
                spec_adapters_config: Some(vec![SpecAdapterConfig {
                    adapter_type: SpecsAdapterType::DataStore,
                    init_timeout_ms: 1_000,
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
            }
            .suppress_diagnostic_output(true),
        )),
    );
    let details = follower.initialize_with_details().await.unwrap();
    assert!(
        details.init_success,
        "offline JSON follower did not initialize"
    );
    assert_eq!(
        details.source,
        SpecsSource::Adapter("DataStore".to_string())
    );
    assert_values(&follower, remote, 2);
    follower.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn json_full_omission_and_inline_replacement_prune_verified_values() {
    let server = MockServer::start().await;
    let remote = RemoteValue::new("prune", true);
    CurrentBlob::mount(&server, &remote).await;
    let dcs = CurrentDcs::new(full(1, 1, Some(&remote)));
    let (sdk, _) = initialize(&server, &dcs, true).await;
    dcs.replace(full(2, 2, None));
    wait_until(|| generation(&sdk) == 2).await;
    assert_eq!(evaluate(&sdk, "default-user", "large_config"), json!({}));
    dcs.replace(full(3, 3, Some(&remote)));
    wait_until(|| generation(&sdk) == 3).await;
    assert_values(&sdk, &remote, 3);
    assert_eq!(get_count(&server, &remote.path()).await, 2);

    let mut inline = full(4, 4, None);
    inline["dynamic_configs"]["large_config"] = inline_config(json!({"inline": true}));
    inline["dynamic_configs"]["mirror_config"] = inline_config(json!({"inline": true}));
    dcs.replace(inline);
    wait_until(|| generation(&sdk) == 4).await;
    assert_eq!(
        evaluate(&sdk, "default-user", "large_config"),
        json!({"inline": true})
    );
    dcs.replace(full(5, 5, Some(&remote)));
    wait_until(|| generation(&sdk) == 5).await;
    assert_values(&sdk, &remote, 5);
    assert_eq!(get_count(&server, &remote.path()).await, 3);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
async fn json_same_sha_with_different_metadata_does_not_reuse_or_advance_cursor() {
    for field in ["byteLength", "compression"] {
        let server = MockServer::start().await;
        let remote = RemoteValue::new("tuple", true);
        let blob = CurrentBlob::mount(&server, &remote).await;
        let dcs = CurrentDcs::new(full(1, 1, Some(&remote)));
        let (sdk, store) = initialize(&server, &dcs, false).await;
        await_writes(&sdk).await;
        let initial_sidecar = store.stored_json_bytes();
        let mut invalid = full(2, 2, Some(&remote));
        let replacement = if field == "byteLength" {
            json!(remote.body.len() - 1)
        } else {
            blob.replace(ResponseTemplate::new(503));
            json!("gzip")
        };
        for config in ["large_config", "mirror_config"] {
            invalid["dynamic_configs"][config]["remoteConfigMetadata"][field] = replacement.clone();
        }
        invalid["dynamic_configs"]["large_config"]["rules"][0]["remoteConfigMetadata"][field] =
            replacement;
        let polls = get_count(&server, DCS_PATH).await;
        dcs.once(invalid, no_update(1));
        wait_requests(&server, DCS_PATH, polls + 3).await;
        assert_eq!(
            generation(&sdk),
            1,
            "rejected {field} metadata advanced the cursor"
        );
        assert_values(&sdk, &remote, 1);
        assert!(
            get_count(&server, &remote.path()).await > 1,
            "incompatible {field} tuple reused provenance"
        );
        assert_eq!(store.stored_json_bytes(), initial_sidecar);
        let failed_gets = get_count(&server, &remote.path()).await;
        blob.replace(ResponseTemplate::new(503));
        dcs.replace(full(3, 3, Some(&remote)));
        wait_until(|| generation(&sdk) == 3).await;
        assert_values(&sdk, &remote, 3);
        assert_eq!(get_count(&server, &remote.path()).await, failed_gets);
        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
async fn failed_json_mixed_downloads_do_not_publish_verified_values() {
    let server = MockServer::start().await;
    let original = RemoteValue::new("original", true);
    let new = RemoteValue::new("unpublished", true);
    let corrupt = RemoteValue::new("wrong-sha", true);
    CurrentBlob::mount(&server, &original).await;
    let new_blob = CurrentBlob::mount(&server, &new).await;
    let corrupt_blob = CurrentBlob::mount(&server, &corrupt).await;
    let corrupt_body = String::from_utf8(corrupt.body.clone())
        .unwrap()
        .replace("wrong-sha", "wrong-SHA")
        .into_bytes();
    assert_eq!(corrupt_body.len(), corrupt.body.len());
    corrupt_blob.replace(
        ResponseTemplate::new(200)
            .insert_header("content-type", "application/json")
            .set_body_bytes(corrupt_body)
            .set_delay(Duration::from_millis(200)),
    );
    let dcs = CurrentDcs::new(full(1, 1, Some(&original)));
    let (sdk, store) = initialize(&server, &dcs, false).await;
    await_writes(&sdk).await;
    let initial_sidecar = store.stored_json_bytes();
    let mut invalid = full(2, 2, Some(&original));
    invalid["dynamic_configs"]["new_config"] = remote_config(&new);
    invalid["dynamic_configs"]["corrupt_config"] = remote_config(&corrupt);
    let polls = get_count(&server, DCS_PATH).await;
    dcs.once(invalid, no_update(1));
    wait_requests(&server, DCS_PATH, polls + 3).await;
    assert_eq!(get_count(&server, &new.path()).await, 1);
    assert_eq!(generation(&sdk), 1);
    assert_values(&sdk, &original, 1);
    assert_eq!(store.stored_json_bytes(), initial_sidecar);

    new_blob.replace(ResponseTemplate::new(503));
    let polls = get_count(&server, DCS_PATH).await;
    dcs.once(full(3, 3, Some(&new)), no_update(1));
    wait_requests(&server, DCS_PATH, polls + 3).await;
    assert!(get_count(&server, &new.path()).await > 1);
    assert_eq!(
        generation(&sdk),
        1,
        "failed update leaked newly verified provenance"
    );
    new_blob.replace(blob_response(&new));
    dcs.replace(full(4, 4, Some(&new)));
    wait_until(|| generation(&sdk) == 4).await;
    assert_values(&sdk, &new, 4);
    sdk.shutdown().await.unwrap();
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn delayed_json_download_does_not_overwrite_newer_bootstrap_or_leak_provenance() {
    let server = MockServer::start().await;
    let original = RemoteValue::new("original", true);
    let delayed = RemoteValue::new("stale-download", true);
    CurrentBlob::mount(&server, &original).await;
    let gate = Arc::new(DownloadGate::default());
    let delayed_blob = CurrentBlob::mount_with_gate(&server, &delayed, Some(gate.clone())).await;
    let dcs = CurrentDcs::new(full(1, 1, Some(&original)));
    let (sdk, _) = initialize(&server, &dcs, true).await;
    dcs.once(full(2, 2, Some(&delayed)), no_update(10));
    // Wiremock's synchronous responder holds one worker until this gate is
    // released. The other worker publishes Bootstrap while the blob cannot
    // finish, so this race does not depend on a chosen response delay.
    wait_until(|| gate.started.load(Ordering::SeqCst)).await;

    let bootstrap = sdk.get_context().spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(serde_json::to_vec(&full(10, 10, None)).unwrap()),
        source: SpecsSource::Bootstrap,
        received_at: 10,
        source_api: None,
        has_updates: None,
    });
    gate.release();
    bootstrap.unwrap();
    assert_eq!(generation(&sdk), 10);
    let polls = get_count(&server, DCS_PATH).await;
    wait_requests(&server, DCS_PATH, polls + 2).await;
    assert_eq!(
        generation(&sdk),
        10,
        "stale hydration overwrote the newer bootstrap"
    );
    assert_eq!(
        evaluate(&sdk, "user", "ordinary_config"),
        json!({"generation": 10})
    );
    let stale_gets = get_count(&server, &delayed.path()).await;
    delayed_blob.replace(ResponseTemplate::new(503));
    let polls = get_count(&server, DCS_PATH).await;
    dcs.once(full(11, 11, Some(&delayed)), no_update(10));
    wait_requests(&server, DCS_PATH, polls + 3).await;
    assert_eq!(
        generation(&sdk),
        10,
        "rejected stale response seeded provenance"
    );
    assert!(get_count(&server, &delayed.path()).await > stale_gets);
    delayed_blob.replace(blob_response(&delayed));
    dcs.replace(full(12, 12, Some(&delayed)));
    wait_until(|| generation(&sdk) == 12).await;
    assert_values(&sdk, &delayed, 12);
    sdk.shutdown().await.unwrap();
}
