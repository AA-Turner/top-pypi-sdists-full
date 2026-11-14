#[path = "utils/partial_blob_publication.rs"]
mod partial_blob_publication;
mod utils;

#[path = "remote_config_value_cold_start/guards_and_logging.rs"]
mod guards_and_logging;

use std::io::Write;
use std::sync::{Arc, Mutex, Weak};

use prost::Message;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::{
    ClientInitResponseOptions, HashAlgorithm, ObservabilityClient, SpecsSource,
    SpecsUpdateListener, Statsig, StatsigOptions, StatsigUser,
    output_logger::{LogLevel, OutputLogProvider},
    specs_response::statsig_config_specs::{
        self as pb, SpecsEnvelopeKind as Kind, any_value, return_value,
    },
};
use tokio::time::{Duration, sleep, timeout};
use utils::{
    mock_data_store::MockDataStore,
    mock_log_provider::{MockLogProvider, RecordedLog},
    mock_observability_client::MockObservabilityClient,
};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, Request, Respond, ResponseTemplate};

const DCS_PATH: &str = "/v2/download_config_specs";
const UNAVAILABLE_BLOB_METRIC: &str = "statsig.sdk.remote_config_hydration.unavailable_blob";
const RESULT_METRIC: &str = "statsig.sdk.remote_config_hydration.result";

const CODECS: [Codec; 2] = [Codec::Json, Codec::Protobuf];

#[derive(Clone, Copy)]
enum Codec {
    Json,
    Protobuf,
}

impl Codec {
    fn name(self) -> &'static str {
        match self {
            Self::Json => "json",
            Self::Protobuf => "protobuf",
        }
    }

    fn response(self, payload: &Value) -> ResponseTemplate {
        match self {
            Self::Json => ResponseTemplate::new(200).set_body_json(payload),
            Self::Protobuf => protobuf_response(&protobuf_envelopes(payload)),
        }
    }
}

struct RemoteValue {
    value: Value,
    body: Vec<u8>,
    sha: String,
}

impl RemoteValue {
    fn new(marker: &str) -> Self {
        Self::from_value(json!({"marker": marker}))
    }

    fn from_value(value: Value) -> Self {
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

    fn metadata(&self) -> Value {
        json!({
            "sha256": self.sha,
            "byteLength": self.body.len(),
            "contentType": "application/json",
            "compression": "none",
        })
    }

    fn response(&self, corrupt: bool) -> ResponseTemplate {
        let mut body = self.body.clone();
        if corrupt {
            // Preserve length and valid JSON so a failed verification has no
            // transport retries and one SHA maps to exactly one failed GET.
            assert_eq!(body[2], b'm');
            body[2] = b'M';
        }
        ResponseTemplate::new(200)
            .insert_header("content-type", "application/json")
            .set_body_bytes(body)
    }
}

#[derive(Clone)]
struct CurrentResponse(Arc<Mutex<(ResponseTemplate, Option<ResponseTemplate>)>>);

impl CurrentResponse {
    fn new(response: ResponseTemplate, following: Option<ResponseTemplate>) -> Self {
        Self(Arc::new(Mutex::new((response, following))))
    }

    fn replace(&self, response: ResponseTemplate) {
        *self.0.lock().unwrap() = (response, None);
    }

    fn once(&self, response: ResponseTemplate, following: ResponseTemplate) {
        *self.0.lock().unwrap() = (response, Some(following));
    }
}

impl Respond for CurrentResponse {
    fn respond(&self, _request: &Request) -> ResponseTemplate {
        let mut current = self.0.lock().unwrap();
        let response = current.0.clone();
        if let Some(next) = current.1.take() {
            current.0 = next;
        }
        response
    }
}

#[tokio::test]
async fn cold_start_keeps_healthy_selected_values_until_identical_payload_recovers() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let healthy = RemoteValue::new("healthy-recovery");
        let failed = RemoteValue::new("recovered-without-config-change");
        mount_blob(&server, &healthy, false).await;
        let blob = mount_blob(&server, &failed, true).await;
        let empty = RemoteValue::from_value(json!({}));
        let mixed_only = RemoteValue::new("verified-only-inside-an-unavailable-config");
        mount_blob(&server, &empty, false).await;
        mount_blob(&server, &mixed_only, false).await;
        let first = RemoteValue::new("repairs-first");
        let first_origin = mount_blob(&server, &first, true).await;
        let mut configs = mixed_configs(&healthy, &failed);
        configs["incremental"] = config_with_remote_rule(remote_config(&failed), &first);
        configs["empty_remote"] = remote_config(&empty);
        configs["empty_inline"] = inline_config(json!({}));
        configs["mixed_only"] = config_with_remote_rule(remote_config(&mixed_only), &failed);
        for (name, target) in [("parent", "large_config"), ("grandparent", "parent")] {
            let mut config = inline_config(json!({"fallback": "must not be selected"}));
            config["rules"] = json!([{"id": "delegate", "name": "delegate", "salt": "delegate",
                "passPercentage": 100, "conditions": [], "idType": "userID",
                "returnValue": {"fallback": "must not be selected"}, "configDelegate": target}]);
            configs[name] = config;
        }
        let payload = full_payload(configs, 1);
        let (sdk, store, observer, dcs) = initialize(&server, codec, "recovery", &payload).await;

        assert_healthy_values(&sdk, &healthy);
        assert!(sdk.get_context().spec_store.needs_blob_hydration_repair());
        assert_unavailable(&sdk, "default-user", "large_config");
        let client = bootstrap_configs_for_user(&sdk, "remote-user");
        for name in [
            "large_config",
            "mirror_config",
            "incremental",
            "parent",
            "grandparent",
            "mixed_only",
        ] {
            assert_unavailable(&sdk, "remote-user", name);
            assert!(client.get(name).is_none());
        }
        let healthy_client = bootstrap_configs_for_user(&sdk, "inline-user");
        for name in ["large_config", "parent", "grandparent"] {
            assert_eq!(
                evaluate(&sdk, "inline-user", name),
                json!({"rule":"healthy"})
            );
            assert_eq!(healthy_client[name]["value"], json!({"rule":"healthy"}));
        }
        assert_eq!(
            evaluate(&sdk, "default-user", "mixed_only"),
            mixed_only.value
        );
        for name in ["empty_remote", "empty_inline"] {
            let result = sdk.get_dynamic_config(&StatsigUser::with_user_id("remote-user"), name);
            assert!(result.details.reason.ends_with(":Recognized"));
            assert!(result.value.is_empty());
            assert_eq!(client[name]["value"], json!({}));
        }
        assert_eq!(
            client["inline_config"]["value"],
            json!({"inline": "healthy"})
        );
        assert_partial_cursor(&sdk);
        assert_degraded_metric(&observer).await;
        await_data_store_writes(&sdk).await;
        assert_eq!(store.num_set_calls() + store.num_set_bytes_calls(), 0);
        assert_eq!(get_count(&server, &failed.path()).await, 1);
        assert_eq!(get_count(&server, &healthy.path()).await, 1);

        dcs.replace(codec.response(&payload));
        wait_for_requests(&server, &failed.path(), 3).await;
        assert_eq!(get_count(&server, &healthy.path()).await, 1);
        assert_unavailable(&sdk, "default-user", "large_config");
        assert_partial_cursor(&sdk);
        await_data_store_writes(&sdk).await;
        assert_eq!(store.num_set_calls() + store.num_set_bytes_calls(), 0);
        assert_eq!(unavailable_blob_count(&observer), 2.0);
        assert_full_polls(&server, 0).await;

        // A blob can recover while another is still unavailable on the same DCS version.
        first_origin.replace(first.response(false));
        assert_eventually!(
            || evaluate(&sdk, "remote-user", "incremental") == first.value,
            Duration::from_secs(8)
        );
        assert_unavailable(&sdk, "default-user", "incremental");
        assert_partial_cursor(&sdk);
        first_origin.replace(first.response(true));
        blob.replace(failed.response(false));
        assert_eventually!(
            || evaluate(&sdk, "default-user", "large_config") == failed.value,
            Duration::from_secs(8)
        );
        assert_eq!(evaluate(&sdk, "remote-user", "incremental"), first.value);
        assert_eq!(evaluate(&sdk, "default-user", "incremental"), failed.value);
        assert!(sdk.is_config_spec_ready());
        let client = bootstrap_configs_for_user(&sdk, "remote-user");
        for name in ["large_config", "mirror_config", "parent", "grandparent"] {
            assert_eq!(evaluate(&sdk, "remote-user", name), failed.value);
            assert_eq!(client[name]["value"], failed.value);
        }
        assert_eq!(
            evaluate(&sdk, "default-user", "mixed_only"),
            mixed_only.value
        );
        assert_eq!(get_count(&server, &mixed_only.path()).await, 1);
        assert_eq!(
            evaluate(&sdk, "inline-user", "large_config"),
            json!({"rule": "healthy"})
        );
        assert!(!sdk.get_context().spec_store.needs_blob_hydration_repair());
        let info = sdk.get_context().spec_store.get_current_specs_info();
        assert_eq!(info.lcut, Some(1));
        assert_eq!(info.checksum.as_deref(), Some("response-1"));
        assert_healthy_values(&sdk, &healthy);
        assert!(get_count(&server, &failed.path()).await >= 4);
        assert_eq!(get_count(&server, &healthy.path()).await, 1);
        await_data_store_writes(&sdk).await;
        assert!(store.num_set_calls() + store.num_set_bytes_calls() > 0);

        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
async fn reads_and_bootstrap_follow_the_selected_blob() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let good = RemoteValue::new("verified");
        let bad = RemoteValue::new("corrupt");
        mount_blob(&server, &good, false).await;
        mount_blob(&server, &bad, true).await;
        let bad_rule = config_with_remote_rule(remote_config(&good), &bad);
        let bad_default = config_with_remote_rule(remote_config(&bad), &good);
        let mut rollouts = bad_rule.clone();
        rollouts["rules"][0]["passPercentage"] = json!(0);
        let mut bad_rollout_default = bad_default.clone();
        bad_rollout_default["rules"][0]["passPercentage"] = json!(0);
        let payload = full_payload(
            json!({
                "bad_rule": bad_rule, "bad_default": bad_default, "missed_bad_rule": rollouts,
                "missed_good_rule": bad_rollout_default, "empty": inline_config(json!({})),
            }),
            1,
        );
        let (sdk, _, _, _) = initialize(&server, codec, "selected-value", &payload).await;
        for (user, config, expected) in [
            ("remote-user", "bad_rule", None),
            ("default-user", "bad_rule", Some(good.value.clone())),
            ("remote-user", "bad_default", Some(good.value.clone())),
            ("default-user", "bad_default", None),
            ("remote-user", "missed_bad_rule", Some(good.value.clone())),
            ("remote-user", "missed_good_rule", None),
            ("inline-user", "bad_rule", Some(json!({"rule":"healthy"}))),
            ("default-user", "empty", Some(json!({}))),
        ] {
            let bootstrap = bootstrap_configs_for_user(&sdk, user);
            let read = sdk.get_dynamic_config(&StatsigUser::with_user_id(user), config);
            if let Some(expected) = expected {
                assert!(read.details.reason.ends_with(":Recognized"), "{config}");
                assert_eq!(json!(read.value), expected, "{config}");
                assert_eq!(bootstrap[config]["value"], expected, "{config}");
            } else {
                assert!(read.details.is_blob_unavailable(), "{config}");
                assert!(bootstrap.get(config).is_none(), "{config}");
            }
        }
        for (user, config, rule) in [
            ("default-user", "bad_rule", "default"),
            ("remote-user", "bad_default", "remote-rule"),
            ("inline-user", "bad_rule", "inline-rule"),
        ] {
            let read = sdk.get_dynamic_config(&StatsigUser::with_user_id(user), config);
            assert_eq!(read.rule_id, rule);
        }
        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
async fn cold_start_settles_slow_blobs_before_initialization_deadline_and_repairs_them() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let healthy = RemoteValue::new("healthy-before-init-deadline");
        let slow = RemoteValue::new("repaired-after-init-deadline");
        mount_blob(&server, &healthy, false).await;
        let blob =
            CurrentResponse::new(slow.response(false).set_delay(Duration::from_secs(2)), None);
        Mock::given(method("GET"))
            .and(path(slow.path()))
            .respond_with(blob.clone())
            .mount(&server)
            .await;
        let default = json!({"inline": "default"});
        let payload = full_payload(
            json!({
                "large_config": config_with_remote_rule(inline_config(default.clone()), &slow),
                "healthy_config": remote_config(&healthy),
            }),
            1,
        );
        let dcs = mount_specs(&server, codec, &payload).await;
        dcs.replace(codec.response(&payload));
        let (sdk, _, observer) = new_sdk(
            &server.uri(),
            codec,
            "slow-init-deadline",
            false,
            None,
            Some(1000),
        );

        let details = sdk.initialize_with_details().await.unwrap();
        assert!(
            details.init_success,
            "blob timeout must not fail initialization"
        );
        assert!(details.failure_details.is_none());
        assert_eq!(details.source, SpecsSource::Network);
        assert!(details.duration_ms < 1000);
        assert_eq!(
            evaluate(&sdk, "default-user", "healthy_config"),
            healthy.value
        );
        assert_eq!(evaluate(&sdk, "default-user", "large_config"), default);
        assert_unavailable(&sdk, "remote-user", "large_config");
        assert_eq!(
            evaluate(&sdk, "inline-user", "large_config"),
            json!({"rule":"healthy"})
        );
        assert_partial_cursor(&sdk);
        assert_eventually!(
            || unavailable_blob_count(&observer) == 1.0,
            Duration::from_secs(8)
        );

        blob.replace(slow.response(false));
        assert_eventually!(
            || evaluate(&sdk, "remote-user", "large_config") == slow.value,
            Duration::from_secs(8)
        );
        assert!(sdk.is_config_spec_ready());
        assert_eq!(get_count(&server, &healthy.path()).await, 1);
        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
async fn degraded_snapshot_rejects_older_full_payloads_before_identical_payload_recovery() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let healthy = RemoteValue::new("healthy-version-2");
        let failed = RemoteValue::new("repaired-version-2");
        let older_remote = RemoteValue::new("healthy-but-older-version-1");
        mount_blob(&server, &healthy, false).await;
        let blob = mount_blob(&server, &failed, true).await;
        mount_blob(&server, &older_remote, false).await;
        let mut newer = mixed_payload(&healthy, &failed, 2);
        newer["dynamic_configs"]["inline_config"]["defaultValue"] = json!({"inline": "new"});
        let (sdk, store, _, dcs) = initialize(&server, codec, "older-full", &newer).await;

        let mut older_with_remote = mixed_payload(&older_remote, &older_remote, 1);
        older_with_remote["dynamic_configs"]["inline_config"]["defaultValue"] =
            json!({"inline": "old-remote"});
        let mut older_without_remote = older_with_remote.clone();
        let mut older_inline = inline_config(json!({"inline": "old-inline"}));
        older_inline["checksum"] = json!("older-inline-config");
        older_without_remote["dynamic_configs"] = json!({"inline_config": older_inline});
        older_without_remote["checksum"] = json!("older-inline-response");

        for older in [older_with_remote, older_without_remote] {
            let requests = get_count(&server, DCS_PATH).await;
            dcs.once(
                codec.response(&older).insert_header("x-since-time", "1"),
                no_update(0),
            );
            // A subsequent poll can begin only after the older full payload
            // has finished processing, avoiding an assertion during parsing.
            wait_for_requests(&server, DCS_PATH, requests + 2).await;
            assert_eq!(
                evaluate(&sdk, "default-user", "inline_config"),
                json!({"inline": "new"}),
                "an older full payload replaced the healthy version-2 inline value",
            );
            assert_eq!(
                evaluate(&sdk, "default-user", "healthy_config"),
                healthy.value
            );
            assert_unavailable(&sdk, "default-user", "large_config");
            assert_eq!(sdk.specs_snapshot().time, 2);
            assert_partial_cursor(&sdk);
            await_data_store_writes(&sdk).await;
            assert_eq!(store.num_set_calls() + store.num_set_bytes_calls(), 0);
            if matches!(codec, Codec::Protobuf) {
                assert_eq!(
                    get_count(&server, &older_remote.path()).await,
                    0,
                    "a known older protobuf version must not start blob hydration",
                );
            }
        }

        blob.replace(failed.response(false));
        dcs.once(
            codec.response(&newer).insert_header("x-since-time", "2"),
            no_update(2),
        );
        assert_eventually!(
            || evaluate(&sdk, "default-user", "large_config") == failed.value,
            Duration::from_secs(8)
        );
        assert!(sdk.is_config_spec_ready());
        let info = sdk.get_context().spec_store.get_current_specs_info();
        assert_eq!(info.lcut, Some(2));
        assert_eq!(info.checksum.as_deref(), Some("response-2"));
        assert_eq!(get_count(&server, &failed.path()).await, 2);
        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
async fn degraded_snapshot_rejects_protobuf_deltas_until_full_repair() {
    for materialized in [false, true] {
        assert_degraded_delta_requires_full_repair(materialized).await;
    }
}

async fn assert_degraded_delta_requires_full_repair(materialized: bool) {
    let server = MockServer::start().await;
    let healthy = RemoteValue::new("healthy-delta-case");
    let failed = RemoteValue::new("full-repair-after-delta");
    mount_blob(&server, &healthy, false).await;
    let blob = mount_blob(&server, &failed, true).await;
    let initial = mixed_payload(&healthy, &failed, 1);
    let scenario = if materialized {
        "materialized-delta"
    } else {
        "cursor-only-delta"
    };
    let (sdk, store, observer, dcs) =
        initialize_with_delta_mode(&server, Codec::Protobuf, scenario, &initial, true).await;
    assert_partial_cursor(&sdk);
    let validations = successful_delta_validations(&observer);
    let requests = get_count(&server, DCS_PATH).await;

    // Wire checksums still cover every rule, including those with an unavailable value.
    // A matching delta cannot repair missing blobs on a partial base.
    dcs.once(
        protobuf_delta_response(&initial, materialized),
        no_update(0),
    );
    assert_eventually!(
        || successful_delta_validations(&observer) > validations,
        Duration::from_secs(8)
    );
    wait_for_requests(&server, DCS_PATH, requests + 2).await;
    assert_partial_cursor(&sdk);
    assert_eq!(sdk.specs_snapshot().time, 1);
    assert_unavailable(&sdk, "default-user", "large_config");
    assert_healthy_values(&sdk, &healthy);
    assert_eq!(get_count(&server, &failed.path()).await, 1);
    assert_eq!(unavailable_blob_count(&observer), 1.0);
    await_data_store_writes(&sdk).await;
    assert_eq!(store.num_set_calls() + store.num_set_bytes_calls(), 0);

    blob.replace(failed.response(false));
    let mut repaired = initial;
    let config = &mut repaired["dynamic_configs"]["large_config"];
    let checksum = config["checksum"].take();
    *config = inline_config(failed.value.clone());
    config["checksum"] = checksum;
    dcs.once(Codec::Protobuf.response(&repaired), no_update(1));
    assert_eventually!(
        || evaluate(&sdk, "default-user", "large_config") == failed.value,
        Duration::from_secs(8)
    );
    assert!(sdk.is_config_spec_ready());
    let info = sdk.get_context().spec_store.get_current_specs_info();
    assert_eq!(info.lcut, Some(1));
    assert_eq!(info.checksum.as_deref(), Some("response-1"));
    assert_eq!(get_count(&server, &failed.path()).await, 2);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
async fn partial_full_update_preserves_the_last_complete_sidecar() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let old = RemoteValue::new("v1");
        let verified = RemoteValue::new("v2-verified");
        let missing = RemoteValue::new("v2-missing");
        mount_blob(&server, &old, false).await;
        mount_blob(&server, &verified, false).await;
        let origin = mount_blob(&server, &missing, true).await;
        let initial = mixed_payload(&old, &old, 1);
        let mut configs = mixed_configs(&verified, &missing);
        configs["inline_config"]["defaultValue"] = json!({"version": 2});
        let next = full_payload(configs, 2);
        let (sdk, store, _, dcs) = initialize(&server, codec, "full-update", &initial).await;
        assert_eq!(evaluate(&sdk, "user", "large_config"), old.value);
        let replay = utils::helpers::bootstrap_from_specs_updated(&sdk).await;
        assert_eq!(evaluate(&replay, "user", "large_config"), old.value);
        await_data_store_writes(&sdk).await;
        let previous = (store.stored_json_bytes(), store.stored_proto_bytes());

        dcs.once(codec.response(&next), no_update(2));
        assert_eventually!(|| sdk.specs_snapshot().time == 2, Duration::from_secs(8));
        assert_eq!(evaluate(&sdk, "user", "healthy_config"), verified.value);
        assert_eq!(
            evaluate(&sdk, "user", "inline_config"),
            json!({"version": 2})
        );
        assert_unavailable(&sdk, "user", "large_config");
        assert_partial_cursor(&sdk);
        await_data_store_writes(&sdk).await;
        assert_eq!(
            (store.stored_json_bytes(), store.stored_proto_bytes()),
            previous
        );

        assert_eq!(evaluate(&replay, "user", "large_config"), old.value);
        let polls = get_count(&server, DCS_PATH).await;
        origin.replace(missing.response(false));
        dcs.once(codec.response(&next), no_update(2));
        assert_eventually!(|| sdk.is_config_spec_ready(), Duration::from_secs(8));
        assert_eq!(evaluate(&sdk, "user", "large_config"), missing.value);
        assert_eventually!(|| evaluate(&replay, "user", "large_config") == missing.value);
        replay.shutdown().await.unwrap();
        assert_full_polls(&server, polls).await;
        sdk.shutdown().await.unwrap();
    }
}

async fn assert_full_polls(server: &MockServer, skip: usize) {
    let requests = server.received_requests().await.unwrap();
    let polls: Vec<_> = requests
        .iter()
        .filter(|r| r.url.path() == DCS_PATH)
        .skip(skip)
        .collect();
    assert!(!polls.is_empty());
    assert!(polls.iter().all(|r| {
        r.url
            .query_pairs()
            .all(|(key, _)| !matches!(key.as_ref(), "sinceTime" | "checksum" | "accept_deltas"))
    }));
}

async fn initialize(
    server: &MockServer,
    codec: Codec,
    scenario: &str,
    payload: &Value,
) -> (
    Statsig,
    Arc<MockDataStore>,
    Arc<MockObservabilityClient>,
    CurrentResponse,
) {
    initialize_with_delta_mode(server, codec, scenario, payload, false).await
}

async fn initialize_with_delta_mode(
    server: &MockServer,
    codec: Codec,
    scenario: &str,
    payload: &Value,
    enable_dcs_deltas: bool,
) -> (
    Statsig,
    Arc<MockDataStore>,
    Arc<MockObservabilityClient>,
    CurrentResponse,
) {
    let dcs = mount_specs(server, codec, payload).await;
    let (sdk, store, observer) = new_sdk(
        &server.uri(),
        codec,
        scenario,
        enable_dcs_deltas,
        None,
        None,
    );
    let details = sdk.initialize_with_details().await.unwrap();
    assert!(details.init_success);
    assert_eq!(
        details.source,
        SpecsSource::Network,
        "{scenario} {}: {:?}",
        codec.name(),
        details.failure_details
    );
    (sdk, store, observer, dcs)
}

async fn mount_specs(server: &MockServer, codec: Codec, payload: &Value) -> CurrentResponse {
    let dcs = CurrentResponse::new(
        codec.response(payload),
        Some(no_update(payload["time"].as_u64().unwrap())),
    );
    Mock::given(method("GET"))
        .and(path(DCS_PATH))
        .respond_with(dcs.clone())
        .mount(server)
        .await;
    dcs
}

fn new_sdk(
    server_uri: &str,
    codec: Codec,
    scenario: &str,
    enable_dcs_deltas: bool,
    provider: Option<Arc<dyn OutputLogProvider>>,
    init_timeout_ms: Option<u64>,
) -> (Statsig, Arc<MockDataStore>, Arc<MockObservabilityClient>) {
    let store = Arc::new(MockDataStore::new_with_byte_cache(false));
    let observer = Arc::new(MockObservabilityClient::new());
    let sdk = Statsig::new(
        &format!("secret-cold-start-{}-{scenario}", codec.name()),
        Some(Arc::new(StatsigOptions {
            data_store: Some(store.clone()),
            output_logger_provider: provider,
            init_timeout_ms,
            enable_dcs_deltas: Some(enable_dcs_deltas),
            ..sdk_options(server_uri, &observer)
        })),
    );
    (sdk, store, observer)
}

fn sdk_options(server_uri: &str, observer: &Arc<MockObservabilityClient>) -> StatsigOptions {
    StatsigOptions {
        observability_client: Some(Arc::downgrade(observer) as Weak<dyn ObservabilityClient>),
        specs_url: Some(format!("{server_uri}{DCS_PATH}")),
        log_event_url: Some(format!("{server_uri}/v1/log_event")),
        remote_config_value_source_url: Some(server_uri.to_string()),
        output_log_level: Some(LogLevel::Warn),
        specs_sync_interval_ms: Some(1000),
        enable_id_lists: Some(false),
        disable_country_lookup: Some(true),
        fallback_to_statsig_api: Some(false),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    }
}

async fn mount_blob(server: &MockServer, remote: &RemoteValue, corrupt: bool) -> CurrentResponse {
    let response = CurrentResponse::new(remote.response(corrupt), None);
    Mock::given(method("GET"))
        .and(path(remote.path()))
        .respond_with(response.clone())
        .mount(server)
        .await;
    response
}

fn inline_config(value: Value) -> Value {
    json!({
        "type": "dynamic_config", "salt": "cold-start", "enabled": true,
        "defaultValue": value, "rules": [], "idType": "userID",
        "entity": "dynamic_config", "version": 1,
    })
}

fn remote_config(remote: &RemoteValue) -> Value {
    let mut config = inline_config(json!({"value": remote.path()}));
    config["remoteConfigMetadata"] = remote.metadata();
    config
}

fn config_with_remote_rule(mut config: Value, remote: &RemoteValue) -> Value {
    config["rules"] = json!([
        {
            "name": "remote-rule", "id": "remote-rule", "salt": "remote",
            "idType": "userID", "passPercentage": 100, "conditions": ["remote-user"],
            "returnValue": {"value": remote.path()}, "remoteConfigMetadata": remote.metadata(),
        },
        {
            "name": "inline-rule", "id": "inline-rule", "salt": "inline",
            "idType": "userID", "passPercentage": 100, "conditions": ["inline-user"],
            "returnValue": {"rule": "healthy"},
        },
    ]);
    config
}

fn mixed_configs(healthy: &RemoteValue, failed: &RemoteValue) -> Value {
    json!({
        "large_config": config_with_remote_rule(remote_config(failed), failed),
        "mirror_config": remote_config(failed),
        "inline_config": inline_config(json!({"inline": "healthy"})),
        "healthy_config": remote_config(healthy),
    })
}

fn mixed_payload(healthy: &RemoteValue, failed: &RemoteValue, time: u64) -> Value {
    full_payload(mixed_configs(healthy, failed), time)
}

fn full_payload(mut configs: Value, time: u64) -> Value {
    let condition = |user| {
        json!({
            "type": "user_field", "field": "userID", "operator": "any",
            "targetValue": [user], "idType": "userID",
        })
    };
    let conditions =
        json!({"remote-user": condition("remote-user"), "inline-user": condition("inline-user")});
    for config in configs.as_object_mut().unwrap().values_mut() {
        config["checksum"] = json!(producer_config_checksum(config, &conditions));
    }
    json!({
        "dynamic_configs": configs,
        "feature_gates": {"healthy_gate": {
            "type": "feature_gate", "salt": "gate", "enabled": true,
            "defaultValue": true, "rules": [], "idType": "userID", "entity": "feature_gate",
        }},
        "layer_configs": {}, "experiment_to_layer": {}, "has_updates": true,
        "time": time, "checksum": format!("response-{time}"), "company_id": "cold-start-test",
        "condition_map": conditions,
        "response_format": "dcs-v2",
    })
}

fn protobuf_envelopes(payload: &Value) -> Vec<pb::SpecsEnvelope> {
    let configs = payload["dynamic_configs"].as_object().unwrap();
    let has_remote_metadata = configs.values().any(|config| {
        !config["remoteConfigMetadata"].is_null()
            || config["rules"]
                .as_array()
                .unwrap()
                .iter()
                .any(|rule| !rule["remoteConfigMetadata"].is_null())
    });
    let top = pb::SpecsTopLevel {
        has_updates: true,
        time: payload["time"].as_u64().unwrap(),
        checksum: payload["checksum"].as_str().unwrap().to_string(),
        company_id: "cold-start-test".to_string(),
        response_format: "dcs-v2".to_string(),
        may_have_remote_config_metadata: Some(has_remote_metadata),
        rest: serde_json::to_vec(&json!({"experiment_to_layer": payload["experiment_to_layer"]}))
            .unwrap(),
    };
    let mut envelopes = vec![envelope(Kind::TopLevel, "", "", top.encode_to_vec())];
    for (name, config) in configs {
        let spec = pb::Spec {
            salt: "cold-start".to_string(),
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            id_type: Some(user_id_type()),
            version: config["version"].as_u64().unwrap() as u32,
            default_value: Some(raw(&config["defaultValue"])),
            remote_config_metadata: metadata(&config["remoteConfigMetadata"]),
            rules: config["rules"]
                .as_array()
                .unwrap()
                .iter()
                .map(|rule| pb::Rule {
                    name: rule["name"].as_str().unwrap().to_string(),
                    id: rule["id"].as_str().unwrap().to_string(),
                    pass_percentage: rule["passPercentage"].as_u64().unwrap() as u32,
                    id_type: Some(user_id_type()),
                    salt: Some(rule["salt"].as_str().unwrap().to_string()),
                    conditions: rule["conditions"]
                        .as_array()
                        .unwrap()
                        .iter()
                        .map(|name| name.as_str().unwrap().to_string())
                        .collect(),
                    return_value: Some(raw(&rule["returnValue"])),
                    remote_config_metadata: metadata(&rule["remoteConfigMetadata"]),
                    config_delegate: rule["configDelegate"].as_str().map(str::to_owned),
                    ..Default::default()
                })
                .collect(),
            ..Default::default()
        };
        envelopes.push(envelope(
            Kind::DynamicConfig,
            name,
            config["checksum"].as_str().unwrap(),
            spec.encode_to_vec(),
        ));
    }
    for name in ["remote-user", "inline-user"] {
        let condition = pb::Condition {
            condition_type: pb::ConditionType::UserField as i32,
            field: Some("userID".to_string()),
            operator: Some(pb::Operator::Any as i32),
            target_value: Some(pb::AnyValue {
                value: Some(any_value::Value::RawValue(
                    serde_json::to_vec(&json!([name])).unwrap(),
                )),
            }),
            ..Default::default()
        };
        envelopes.push(envelope(
            Kind::Condition,
            name,
            name,
            condition.encode_to_vec(),
        ));
    }
    let gate = pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityFeatureGate as i32,
        default_value: Some(pb::ReturnValue {
            value: Some(return_value::Value::BoolValue(true)),
        }),
        ..Default::default()
    };
    envelopes.push(envelope(
        Kind::FeatureGate,
        "healthy_gate",
        "gate",
        gate.encode_to_vec(),
    ));
    envelopes.push(pb::SpecsEnvelope {
        kind: Kind::Done as i32,
        ..Default::default()
    });
    envelopes
}

fn protobuf_response(envelopes: &[pb::SpecsEnvelope]) -> ResponseTemplate {
    let mut uncompressed = Vec::new();
    for envelope in envelopes {
        envelope.encode_length_delimited(&mut uncompressed).unwrap();
    }
    let mut writer = brotli::CompressorWriter::new(Vec::new(), 4096, 1, 22);
    writer.write_all(&uncompressed).unwrap();
    ResponseTemplate::new(200)
        .insert_header("content-type", "application/octet-stream")
        .insert_header("content-encoding", "statsig-br")
        .set_body_bytes(writer.into_inner())
}

fn protobuf_delta_response(initial: &Value, materialized: bool) -> ResponseTemplate {
    let mut configs = initial["dynamic_configs"].clone();
    if materialized {
        configs["inline_config"]["defaultValue"] = json!({"inline": "delta-value"});
    }
    let mut frames = protobuf_envelopes(&full_payload(configs, 2));
    // The delta itself carries no new remote metadata.
    let top = frames.first_mut().unwrap();
    let mut header = pb::SpecsTopLevel::decode(top.data.as_deref().unwrap()).unwrap();
    header.may_have_remote_config_metadata = Some(false);
    top.data = Some(header.encode_to_vec());

    let kinds = [
        ("dynamic_configs", Kind::DynamicConfig),
        ("feature_gates", Kind::FeatureGate),
        ("layer_configs", Kind::LayerConfig),
        ("param_stores", Kind::ParamStore),
        ("condition_map", Kind::Condition),
    ];
    let field_checksums = kinds
        .into_iter()
        .map(|(name, kind)| {
            let sum = frames
                .iter()
                .filter(|f| f.kind == kind as i32)
                .filter_map(|f| f.checksum.parse::<u64>().ok())
                .sum();
            (name.to_owned(), sum)
        })
        .collect();
    let mut delta = vec![pb::SpecsEnvelope {
        kind: Kind::CopyPrev as i32,
        ..Default::default()
    }];
    delta.extend(frames.into_iter().filter(|f| {
        f.kind == Kind::TopLevel as i32 || (materialized && f.name == "inline_config")
    }));
    delta.push(envelope(
        Kind::Checksums,
        "",
        "",
        pb::RulesetsChecksums { field_checksums }.encode_to_vec(),
    ));
    delta.push(pb::SpecsEnvelope {
        kind: Kind::Done as i32,
        ..Default::default()
    });
    protobuf_response(&delta)
        .insert_header("x-deltas-used", "true")
        .insert_header("x-since-time", "2")
        .insert_header("x-checksum", header.checksum)
}

fn producer_config_checksum(config: &Value, condition_map: &Value) -> String {
    let mut api_spec = config.clone();
    api_spec.as_object_mut().unwrap().remove("checksum");
    for rule in api_spec["rules"].as_array_mut().unwrap() {
        for condition in rule["conditions"].as_array_mut().unwrap() {
            *condition = condition_map[condition.as_str().unwrap()].clone();
        }
    }
    // Match the producer's unsigned CRC32 over the API spec before condition
    // extraction and protobuf conversion, retaining remote-link metadata.
    let mut crc = flate2::Crc::new();
    crc.update(&serde_json::to_vec(&api_spec).unwrap());
    crc.sum().to_string()
}

fn envelope(kind: Kind, name: &str, checksum: &str, data: Vec<u8>) -> pb::SpecsEnvelope {
    pb::SpecsEnvelope {
        kind: kind as i32,
        name: name.to_string(),
        checksum: checksum.to_string(),
        data: Some(data),
    }
}

fn raw(value: &Value) -> pb::ReturnValue {
    pb::ReturnValue {
        value: Some(return_value::Value::RawValue(
            serde_json::to_vec(value).unwrap(),
        )),
    }
}

fn user_id_type() -> pb::IdType {
    pb::IdType {
        id_type: Some(pb::id_type::IdType::KnownIdType(
            pb::KnownIdType::UserId as i32,
        )),
    }
}

fn metadata(value: &Value) -> Option<pb::RemoteConfigValueMetadata> {
    if value.is_null() {
        return None;
    }
    Some(pb::RemoteConfigValueMetadata {
        sha256: value["sha256"].as_str().unwrap().to_string(),
        byte_length: value["byteLength"].as_u64().unwrap(),
        content_type: value["contentType"].as_str().unwrap().to_string(),
        compression: value["compression"].as_str().unwrap().to_string(),
    })
}

fn no_update(time: u64) -> ResponseTemplate {
    ResponseTemplate::new(200).set_body_json(json!({"has_updates": false, "time": time}))
}

fn evaluate(sdk: &Statsig, user: &str, config: &str) -> Value {
    json!(
        sdk.get_dynamic_config(&StatsigUser::with_user_id(user), config)
            .value
    )
}

fn assert_unavailable(sdk: &Statsig, user: &str, config: &str) {
    let result = sdk.get_dynamic_config(&StatsigUser::with_user_id(user), config);
    assert!(
        result.details.reason.ends_with(":Unavailable"),
        "{config}: {:?}",
        result.details
    );
    let missing = sdk.get_dynamic_config(&StatsigUser::with_user_id(user), "missing-config");
    assert!(missing.details.reason.ends_with(":Unrecognized"));
    assert_eq!(result.details.lcut, missing.details.lcut);
    assert_eq!(result.rule_id, missing.rule_id);
    assert_eq!(
        result.get_typed_opt("mobile_interval", Some(json!(4320))),
        Some(json!(4320))
    );
}

fn bootstrap_configs_for_user(sdk: &Statsig, user: &str) -> Value {
    let options = ClientInitResponseOptions {
        hash_algorithm: Some(HashAlgorithm::None),
        ..Default::default()
    };
    serde_json::to_value(
        sdk.get_client_init_response_with_options(&StatsigUser::with_user_id(user), &options),
    )
    .unwrap()["dynamic_configs"]
        .clone()
}

fn assert_healthy_values(sdk: &Statsig, healthy: &RemoteValue) {
    assert_eq!(
        evaluate(sdk, "default-user", "inline_config"),
        json!({"inline": "healthy"})
    );
    assert_eq!(
        evaluate(sdk, "default-user", "healthy_config"),
        healthy.value
    );

    assert!(sdk.check_gate(&StatsigUser::with_user_id("default-user"), "healthy_gate"));
}

fn unavailable_blob_count(observer: &MockObservabilityClient) -> f64 {
    observer
        .increment_calls
        .lock()
        .unwrap()
        .iter()
        .filter(|(name, _, _)| name == UNAVAILABLE_BLOB_METRIC)
        .map(|(_, value, _)| value)
        .sum()
}

fn assert_partial_cursor(sdk: &Statsig) {
    let info = sdk.get_context().spec_store.get_current_specs_info();
    assert!(!sdk.is_config_spec_ready());
    assert_eq!(info.lcut, Some(0));
    assert_eq!(info.checksum, None);
}

async fn assert_degraded_metric(observer: &MockObservabilityClient) {
    assert_eventually!(
        || unavailable_blob_count(observer) == 2.0,
        Duration::from_secs(8)
    );
    let calls = observer.increment_calls.lock().unwrap();
    let outcomes: Vec<_> = calls
        .iter()
        .filter(|(name, _, _)| name == RESULT_METRIC)
        .filter_map(|(_, _, tags)| tags.as_ref()?.get("outcome").map(String::as_str))
        .collect();
    assert!(outcomes.contains(&"degraded"));
    assert!(!outcomes.contains(&"success"));
}

fn successful_delta_validations(observer: &MockObservabilityClient) -> usize {
    observer
        .increment_calls
        .lock()
        .unwrap()
        .iter()
        .filter(|(name, _, tags)| {
            name == "statsig.sdk.deltas_checksum_validation.count"
                && tags.as_ref().is_some_and(|tags| {
                    tags.get("result").is_some_and(|result| result == "success")
                })
        })
        .count()
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

async fn wait_for_requests(server: &MockServer, request_path: &str, minimum: usize) {
    timeout(Duration::from_secs(8), async {
        while get_count(server, request_path).await < minimum {
            sleep(Duration::from_millis(10)).await;
        }
    })
    .await
    .expect("expected local request was not received");
}

async fn await_data_store_writes(sdk: &Statsig) {
    timeout(
        Duration::from_secs(5),
        sdk.statsig_runtime
            .await_tasks_with_tag("spec_store_update_data_store"),
    )
    .await
    .expect("datastore publications should complete");
}
