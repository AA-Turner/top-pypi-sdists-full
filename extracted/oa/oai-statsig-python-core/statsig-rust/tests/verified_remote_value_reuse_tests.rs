mod utils;

use std::collections::HashMap;
use std::io::{Read, Write};
use std::sync::{Arc, Mutex};

use prost::Message;
use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::{
    DynamicConfigEvaluationOptions, Statsig, StatsigOptions, StatsigUser,
    interned_string::InternedString,
    interned_values::InternedStore,
    output_logger::LogLevel,
    specs_response::statsig_config_specs::{self as pb, any_value, return_value},
};
use tokio::time::{Duration, sleep};
use utils::{
    mock_data_store::MockDataStore, mock_event_logging_adapter::MockEventLoggingAdapter,
    mock_log_provider::MockLogProvider,
};
use wiremock::matchers::{header, method, path};
use wiremock::{Mock, MockServer, Request, Respond, ResponseTemplate};

const SDK_KEY: &str = "secret-verified-remote-value-reuse";
const LARGE_CONFIG: &str = "large_config";
const BLOB_BYTES: usize = 256 * 1024;

#[derive(Clone, Copy)]
enum WireFormat {
    Forward,
    Reversed,
    Whitespace,
}

struct RemoteValue {
    body: Vec<u8>,
    value: Value,
    sha: String,
}

impl RemoteValue {
    fn new(marker: &str, format: WireFormat) -> Self {
        let overhead = format!(r#"{{"marker":"{marker}","padding":""}}"#).len();
        let padding = "x".repeat(BLOB_BYTES - overhead);
        let value = json!({"marker": marker, "padding": padding});
        let body = match format {
            WireFormat::Forward => serde_json::to_vec(&value).unwrap(),
            WireFormat::Reversed => format!(
                r#"{{"padding":{},"marker":{}}}"#,
                serde_json::to_string(&value["padding"]).unwrap(),
                serde_json::to_string(&value["marker"]).unwrap()
            )
            .into_bytes(),
            // Whitespace guarantees that parsed-value reserialization cannot
            // reproduce the authenticated bytes, independently of map order.
            WireFormat::Whitespace => format!(
                "{{ \"marker\": {}, \"padding\": {} }}",
                serde_json::to_string(&value["marker"]).unwrap(),
                serde_json::to_string(&value["padding"]).unwrap()
            )
            .into_bytes(),
        };
        assert_eq!(serde_json::from_slice::<Value>(&body).unwrap(), value);
        let sha = Sha256::digest(&body)
            .iter()
            .map(|byte| format!("{byte:02x}"))
            .collect();
        Self { body, value, sha }
    }

    fn path(&self) -> String {
        format!("/v1/dynamic_config_value/{}", self.sha)
    }
}

struct SpecsResponse {
    body: Vec<u8>,
    generation: u64,
    is_delta: bool,
    after_once: Option<Box<SpecsResponse>>,
}

#[derive(Clone)]
struct CurrentResponse(Arc<Mutex<SpecsResponse>>);

impl Respond for CurrentResponse {
    fn respond(&self, _request: &Request) -> ResponseTemplate {
        let mut response = self.0.lock().unwrap();
        let mut template = ResponseTemplate::new(200)
            .insert_header("content-type", "application/octet-stream")
            .insert_header("content-encoding", "statsig-br")
            .insert_header("x-since-time", response.generation.to_string())
            .insert_header("x-checksum", format!("response-{}", response.generation))
            .set_body_bytes(response.body.clone());
        if response.is_delta {
            template = template.insert_header("x-deltas-used", "true");
        }
        if let Some(next) = response.after_once.take() {
            *response = *next;
        }
        template
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn verified_values_survive_full_updates_and_deltas_without_redownload() {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    for format in [
        WireFormat::Forward,
        WireFormat::Reversed,
        WireFormat::Whitespace,
    ] {
        for read_only in [false, true] {
            run_reuse_case(format, read_only).await;
        }
    }
}

async fn run_reuse_case(format: WireFormat, read_only: bool) {
    let server = MockServer::start().await;
    let original = RemoteValue::new("original", format);
    let changed = RemoteValue::new("changed", format);
    for remote in [&original, &changed] {
        Mock::given(method("GET"))
            .and(path(remote.path()))
            .and(header("statsig-api-key", SDK_KEY))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(remote.body.clone()),
            )
            .mount(&server)
            .await;
    }
    let response = CurrentResponse(Arc::new(Mutex::new(full(1, 1, Some(&original), None))));
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(response.clone())
        .mount(&server)
        .await;

    let store = Arc::new(MockDataStore::new_with_byte_cache(false).with_read_only(read_only));
    let logs = Arc::new(MockLogProvider::new());
    let sdk = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            data_store: Some(store.clone()),
            specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
            remote_config_value_source_url: Some(server.uri()),
            event_logging_adapter: Some(Arc::new(
                MockEventLoggingAdapter::new_with_background_flush(false),
            )),
            specs_sync_interval_ms: Some(50),
            enable_dcs_deltas: Some(true),
            enable_id_lists: Some(false),
            disable_country_lookup: Some(true),
            fallback_to_statsig_api: Some(false),
            disable_all_logging: Some(true),
            output_logger_provider: Some(logs.clone()),
            output_log_level: Some(LogLevel::Error),
            ..StatsigOptions::new()
        })),
    );
    sdk.initialize().await.unwrap();
    assert_values(&sdk, &original, 1);
    assert_eq!(get_count(&server, &original.path()).await, 1);
    let config_name = InternedString::from_str_ref(LARGE_CONFIG);
    // Retain the old snapshot so pointer comparisons cannot observe recycled
    // allocation addresses after publishing a replacement.
    let initial_snapshot = sdk.specs_snapshot();
    let initial_spec = initial_snapshot
        .dynamic_configs
        .get(&config_name)
        .unwrap()
        .as_spec_ref();
    assert_ne!(
        spec_checksum(&large_spec(1, &original, None)),
        spec_checksum(&large_spec(2, &original, None))
    );

    // Different config changed; same rule/default SHA and same entity checksum.
    *response.0.lock().unwrap() = full(2, 1, Some(&original), None);
    wait_generation(&sdk, 2).await;
    assert_values(&sdk, &original, 1);
    assert_eq!(get_count(&server, &original.path()).await, 1);
    let unchanged_snapshot = sdk.specs_snapshot();
    let unchanged_spec = unchanged_snapshot
        .dynamic_configs
        .get(&config_name)
        .unwrap()
        .as_spec_ref();
    assert!(std::ptr::eq(initial_spec, unchanged_spec));

    // The entity checksum changes when another rule in the SAME config changes.
    // Reuse is based on the verified value's SHA, not the enclosing entity CRC.
    *response.0.lock().unwrap() = full(3, 2, Some(&original), None);
    wait_generation(&sdk, 3).await;
    assert_values(&sdk, &original, 2);
    assert_eq!(get_count(&server, &original.path()).await, 1);
    let changed_config_snapshot = sdk.specs_snapshot();
    let changed_config_spec = changed_config_snapshot
        .dynamic_configs
        .get(&config_name)
        .unwrap()
        .as_spec_ref();
    assert!(!std::ptr::eq(initial_spec, changed_config_spec));
    assert!(std::ptr::eq(
        initial_spec.default_value.get_json_pointer_ref().unwrap(),
        changed_config_spec
            .default_value
            .get_json_pointer_ref()
            .unwrap(),
    ));
    assert!(std::ptr::eq(
        initial_spec.rules[0]
            .return_value
            .get_json_pointer_ref()
            .unwrap(),
        changed_config_spec.rules[0]
            .return_value
            .get_json_pointer_ref()
            .unwrap(),
    ));

    *response.0.lock().unwrap() = full(4, 2, Some(&changed), None);
    wait_generation(&sdk, 4).await;
    assert_values(&sdk, &changed, 2);
    assert_eq!(get_count(&server, &changed.path()).await, 1);
    if !read_only {
        wait_snapshot(&store, 4).await;
    }

    let writes = store.num_set_bytes_calls();
    let polls = get_count(&server, "/v2/download_config_specs").await;
    wait_polls(&server, polls + 3).await;
    assert_eq!(get_count(&server, &changed.path()).await, 1);
    assert_eq!(store.num_set_bytes_calls(), writes);

    // Copy-prev delta does not carry the large config. Its verified values
    // must remain available when a subsequent full response includes links.
    *response.0.lock().unwrap() = delta(5, 2, &changed, false);
    wait_generation(&sdk, 5).await;
    assert_values(&sdk, &changed, 2);
    *response.0.lock().unwrap() = full(6, 2, Some(&changed), None);
    wait_generation(&sdk, 6).await;
    assert_values(&sdk, &changed, 2);
    assert_eq!(get_count(&server, &changed.path()).await, 1);

    // Deleted values leave the current snapshot's reuse set.
    *response.0.lock().unwrap() = delta(7, 2, &changed, true);
    wait_generation(&sdk, 7).await;
    assert!(
        !sdk.get_dynamic_config_list()
            .iter()
            .any(|name| name == LARGE_CONFIG)
    );
    *response.0.lock().unwrap() = full(8, 2, Some(&changed), None);
    wait_generation(&sdk, 8).await;
    assert_values(&sdk, &changed, 2);
    assert_eq!(get_count(&server, &changed.path()).await, 2);

    // Same SHA with a conflicting declared length is not trusted reuse.
    // Failed updates cannot publish either new values or new provenance.
    let prior_errors = logs.get_error_logs().len();
    let mut invalid = full(9, 3, Some(&changed), Some(changed.body.len() + 1));
    // Serve the bad update exactly once. Subsequent polls return the last
    // accepted cursor, avoiding a race with another rejected update in flight.
    invalid.after_once = Some(Box::new(full(8, 2, Some(&changed), None)));
    *response.0.lock().unwrap() = invalid;
    wait_until(|| logs.get_error_logs().len() > prior_errors).await;
    assert_eq!(generation(&sdk), 8);
    assert_values(&sdk, &changed, 2);
    let after_failure_gets = get_count(&server, &changed.path()).await;
    assert_eq!(after_failure_gets, 3);
    *response.0.lock().unwrap() = full(10, 2, Some(&changed), None);
    wait_generation(&sdk, 10).await;
    assert_values(&sdk, &changed, 2);
    assert_eq!(
        get_count(&server, &changed.path()).await,
        after_failure_gets
    );

    if read_only {
        assert_eq!(store.num_set_bytes_calls(), 0);
    } else {
        wait_snapshot(&store, 10).await;
        assert_snapshot(&store, &changed);
    }

    // Full-response omission prunes provenance, just like a delta deletion.
    *response.0.lock().unwrap() = full(11, 2, None, None);
    wait_generation(&sdk, 11).await;
    assert!(
        !sdk.get_dynamic_config_list()
            .iter()
            .any(|name| name == LARGE_CONFIG)
    );
    *response.0.lock().unwrap() = full(12, 2, Some(&changed), None);
    wait_generation(&sdk, 12).await;
    assert_values(&sdk, &changed, 2);
    assert_eq!(get_count(&server, &changed.path()).await, 4);
    sdk.shutdown().await.unwrap();
}

rusty_fork_test! {
    #[test]
    fn current_verified_config_wins_over_stale_mmap_placeholder() {
        // Mmap loading installs process-global state, so keep this regression
        // isolated from the other wire-format/datastore cases.
        tokio::runtime::Builder::new_multi_thread()
            .worker_threads(2)
            .enable_all()
            .build()
            .unwrap()
            .block_on(run_stale_mmap_case());
    }
}

async fn run_stale_mmap_case() {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    let sdk_key = format!("secret-verified-stale-mmap-{}", std::process::id());
    let server = MockServer::start().await;
    let remote = RemoteValue::new("mmap-regression", WireFormat::Whitespace);
    let wire_spec = large_spec(1, &remote, None);
    let checksum = spec_checksum(&wire_spec);
    // Emulate an old artifact which kept the link object, but omitted its
    // metadata while retaining the producer's unchanged config checksum.
    let mut placeholder = wire_spec;
    placeholder.remote_config_metadata = None;
    placeholder.rules[0].remote_config_metadata = None;
    let artifact = encode_response(
        1,
        false,
        vec![
            top(1, false),
            condition("remote-user"),
            condition("normal-user"),
            envelope(
                pb::SpecsEnvelopeKind::DynamicConfig,
                LARGE_CONFIG,
                &checksum,
                placeholder.encode_to_vec(),
            ),
            ordinary(1),
        ],
    );
    Mock::given(method("GET"))
        .and(path("/placeholder_specs"))
        .and(header("statsig-api-key", sdk_key.as_str()))
        .respond_with(CurrentResponse(Arc::new(Mutex::new(artifact))))
        .mount(&server)
        .await;
    InternedStore::fetch_and_write_mmap_with_specs_url(
        &sdk_key,
        &format!("{}/placeholder_specs", server.uri()),
    )
    .await
    .unwrap();
    InternedStore::preload_mmap(&sdk_key).unwrap();
    assert!(InternedStore::has_preloaded_mmap_project(&sdk_key));
    let name = InternedString::from_str_ref(LARGE_CONFIG);
    let stale = InternedStore::try_get_preloaded_dynamic_config(&name).unwrap();
    let stale_spec = stale.as_spec_ref();
    assert_eq!(stale_spec.checksum.as_ref().unwrap().as_str(), checksum);
    assert_eq!(
        serde_json::to_value(&stale_spec.default_value).unwrap(),
        json!({"value": remote.path()}),
    );

    let response = CurrentResponse(Arc::new(Mutex::new(full(1, 1, Some(&remote), None))));
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .and(header("statsig-api-key", sdk_key.as_str()))
        .respond_with(response.clone())
        .mount(&server)
        .await;
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
    let sdk = Statsig::new(
        &sdk_key,
        Some(Arc::new(StatsigOptions {
            data_store: Some(Arc::new(
                MockDataStore::new_with_byte_cache(false).with_read_only(true),
            )),
            specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
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
    assert_values(&sdk, &remote, 1);
    assert_eq!(get_count(&server, &remote.path()).await, 1);
    let initial = sdk.specs_snapshot();
    let initial_spec = initial.dynamic_configs.get(&name).unwrap().as_spec_ref();
    assert!(!std::ptr::eq(initial_spec, stale_spec));

    *response.0.lock().unwrap() = full(2, 1, Some(&remote), None);
    wait_generation(&sdk, 2).await;
    assert_values(&sdk, &remote, 1);
    assert_eq!(get_count(&server, &remote.path()).await, 1);
    let updated = sdk.specs_snapshot();
    let updated_spec = updated.dynamic_configs.get(&name).unwrap().as_spec_ref();
    assert!(std::ptr::eq(initial_spec, updated_spec));
    // The stale artifact is still present after both live updates; it has
    // neither displaced the current pointer nor acquired trusted provenance.
    let still_stale = InternedStore::try_get_preloaded_dynamic_config(&name).unwrap();
    assert!(std::ptr::eq(stale_spec, still_stale.as_spec_ref()));
    assert_eq!(
        serde_json::to_value(&still_stale.as_spec_ref().default_value).unwrap(),
        json!({"value": remote.path()}),
    );
    sdk.shutdown().await.unwrap();
}

fn evaluate(sdk: &Statsig, user: &str, name: &str) -> Value {
    let config = sdk.get_dynamic_config_with_options(
        &StatsigUser::with_user_id(user),
        name,
        DynamicConfigEvaluationOptions {
            disable_exposure_logging: true,
        },
    );
    serde_json::to_value(config.value).unwrap()
}

fn assert_values(sdk: &Statsig, remote: &RemoteValue, normal_generation: u64) {
    assert_eq!(evaluate(sdk, "remote-user", LARGE_CONFIG), remote.value);
    assert_eq!(evaluate(sdk, "default-user", LARGE_CONFIG), remote.value);
    assert_eq!(
        evaluate(sdk, "normal-user", LARGE_CONFIG),
        json!({"normalGeneration": normal_generation})
    );
}

fn generation(sdk: &Statsig) -> u64 {
    evaluate(sdk, "user", "ordinary_config")["generation"]
        .as_u64()
        .unwrap_or(0)
}

async fn wait_generation(sdk: &Statsig, expected: u64) {
    wait_until(|| generation(sdk) == expected).await;
}

async fn wait_until(check: impl Fn() -> bool) {
    for _ in 0..250 {
        if check() {
            return;
        }
        sleep(Duration::from_millis(20)).await;
    }
    assert!(check(), "expected background update did not finish");
}

async fn get_count(server: &MockServer, path: &str) -> usize {
    server
        .received_requests()
        .await
        .unwrap()
        .iter()
        .filter(|request| request.url.path() == path)
        .count()
}

async fn wait_polls(server: &MockServer, expected: usize) {
    for _ in 0..250 {
        if get_count(server, "/v2/download_config_specs").await >= expected {
            return;
        }
        sleep(Duration::from_millis(20)).await;
    }
    assert!(get_count(server, "/v2/download_config_specs").await >= expected);
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

fn raw(value: Value) -> pb::ReturnValue {
    pb::ReturnValue {
        value: Some(return_value::Value::RawValue(
            serde_json::to_vec(&value).unwrap(),
        )),
    }
}

fn metadata(remote: &RemoteValue, length: Option<usize>) -> pb::RemoteConfigValueMetadata {
    pb::RemoteConfigValueMetadata {
        sha256: remote.sha.clone(),
        byte_length: length.unwrap_or(remote.body.len()) as u64,
        content_type: "application/json".to_string(),
        compression: "none".to_string(),
    }
}

fn user_id_type() -> pb::IdType {
    pb::IdType {
        id_type: Some(pb::id_type::IdType::KnownIdType(
            pb::KnownIdType::UserId as i32,
        )),
    }
}

fn large_spec(normal_generation: u64, remote: &RemoteValue, length: Option<usize>) -> pb::Spec {
    let link = json!({"value": remote.path()});
    pb::Spec {
        salt: "large".to_string(),
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        id_type: Some(user_id_type()),
        version: 1,
        default_value: Some(raw(link.clone())),
        remote_config_metadata: Some(metadata(remote, length)),
        rules: vec![
            pb::Rule {
                name: "remote-rule".to_string(),
                id: "remote-rule".to_string(),
                pass_percentage: 100,
                conditions: vec!["remote-user".to_string()],
                id_type: Some(user_id_type()),
                return_value: Some(raw(link)),
                remote_config_metadata: Some(metadata(remote, length)),
                ..Default::default()
            },
            pb::Rule {
                name: "normal-rule".to_string(),
                id: "normal-rule".to_string(),
                pass_percentage: 100,
                conditions: vec!["normal-user".to_string()],
                id_type: Some(user_id_type()),
                return_value: Some(raw(json!({"normalGeneration": normal_generation}))),
                ..Default::default()
            },
        ],
        ..Default::default()
    }
}

// Match fastChecksumForAPIConfigSpec: unsigned CRC32 of the API JSON after
// remote-link replacement, before condition extraction/protobuf conversion.
fn spec_checksum(spec: &pb::Spec) -> String {
    let return_value = |value: &pb::ReturnValue| {
        let Some(return_value::Value::RawValue(bytes)) = &value.value else {
            panic!("fixture requires JSON return values");
        };
        serde_json::from_slice::<Value>(bytes).unwrap()
    };
    let metadata = |value: &pb::RemoteConfigValueMetadata| {
        json!({
            "sha256": value.sha256,
            "byteLength": value.byte_length,
            "contentType": value.content_type,
            "compression": value.compression,
        })
    };
    let rules: Vec<Value> = spec.rules.iter().map(|rule| {
        let conditions: Vec<Value> = rule.conditions.iter().map(|name| {
            json!({"type": "user_field", "field": "userID", "operator": "any", "targetValue": [name], "idType": "userID"})
        }).collect();
        let mut api_rule = json!({
            "name": rule.name,
            "id": rule.id,
            "idType": "userID",
            "passPercentage": rule.pass_percentage,
            "conditions": conditions,
            "returnValue": return_value(rule.return_value.as_ref().unwrap()),
        });
        if let Some(value) = &rule.remote_config_metadata {
            api_rule["remoteConfigMetadata"] = metadata(value);
        }
        api_rule
    }).collect();
    let mut api = json!({
        "type": "dynamic_config",
        "salt": spec.salt,
        "enabled": spec.enabled,
        "defaultValue": return_value(spec.default_value.as_ref().unwrap()),
        "rules": rules,
        "entity": "dynamic_config",
        "idType": "userID",
        "version": spec.version,
    });
    if let Some(value) = &spec.remote_config_metadata {
        api["remoteConfigMetadata"] = metadata(value);
    }
    producer_checksum(api)
}

fn producer_checksum(mut api: Value) -> String {
    api.as_object_mut().unwrap().remove("checksum");
    crc32(&serde_json::to_vec(&api).unwrap()).to_string()
}

#[test]
fn producer_checksum_excludes_only_the_root_checksum() {
    assert_eq!(crc32(b"123456789"), 0xcbf43926);
    let spec = json!({"defaultValue": {"checksum": "retained"}, "rules": []});
    let mut with_checksum = spec.clone();
    with_checksum["checksum"] = json!("previous");
    assert_eq!(
        producer_checksum(spec.clone()),
        producer_checksum(with_checksum)
    );
    let mut changed = spec.clone();
    changed["defaultValue"]["checksum"] = json!("changed");
    assert_ne!(producer_checksum(spec), producer_checksum(changed));
}

fn condition(name: &str) -> pb::SpecsEnvelope {
    let condition = pb::Condition {
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
        &crc32(&condition.encode_to_vec()).to_string(),
        condition.encode_to_vec(),
    )
}

fn ordinary(generation: u64) -> pb::SpecsEnvelope {
    let spec = pb::Spec {
        salt: "ordinary".to_string(),
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        id_type: Some(user_id_type()),
        version: 1,
        default_value: Some(raw(json!({"generation": generation}))),
        ..Default::default()
    };
    envelope(
        pb::SpecsEnvelopeKind::DynamicConfig,
        "ordinary_config",
        &spec_checksum(&spec),
        spec.encode_to_vec(),
    )
}

fn top(generation: u64, has_remote: bool) -> pb::SpecsEnvelope {
    envelope(
        pb::SpecsEnvelopeKind::TopLevel,
        "",
        "",
        pb::SpecsTopLevel {
            has_updates: true,
            time: generation,
            company_id: "test-company".to_string(),
            response_format: "dcs-v2".to_string(),
            checksum: format!("response-{generation}"),
            rest: br#"{"experiment_to_layer":{},"condition_map":{}}"#.to_vec(),
            may_have_remote_config_metadata: Some(has_remote),
        }
        .encode_to_vec(),
    )
}

fn full(
    generation: u64,
    normal_generation: u64,
    remote: Option<&RemoteValue>,
    length: Option<usize>,
) -> SpecsResponse {
    let mut frames = vec![
        top(generation, remote.is_some()),
        condition("remote-user"),
        condition("normal-user"),
    ];
    if let Some(remote) = remote {
        let spec = large_spec(normal_generation, remote, length);
        frames.push(envelope(
            pb::SpecsEnvelopeKind::DynamicConfig,
            LARGE_CONFIG,
            &spec_checksum(&spec),
            spec.encode_to_vec(),
        ));
    }
    frames.push(ordinary(generation));
    encode_response(generation, false, frames)
}

fn delta(
    generation: u64,
    normal_generation: u64,
    remote: &RemoteValue,
    delete_large: bool,
) -> SpecsResponse {
    let mut frames = vec![
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        },
        top(generation, false),
        ordinary(generation),
    ];
    if delete_large {
        frames.push(envelope(
            pb::SpecsEnvelopeKind::Deletions,
            "",
            "",
            pb::RulesetsResponseDeletions {
                dynamic_configs: vec![LARGE_CONFIG.to_string()],
                ..Default::default()
            }
            .encode_to_vec(),
        ));
    }
    let sum_conditions = [condition("remote-user"), condition("normal-user")]
        .iter()
        .map(|frame| frame.checksum.parse::<u64>().unwrap())
        .sum();
    let sum_configs = ordinary(generation).checksum.parse::<u64>().unwrap()
        + if delete_large {
            0
        } else {
            spec_checksum(&large_spec(normal_generation, remote, None))
                .parse::<u64>()
                .unwrap()
        };
    frames.push(envelope(
        pb::SpecsEnvelopeKind::Checksums,
        "",
        "",
        pb::RulesetsChecksums {
            field_checksums: HashMap::from([
                ("condition_map".to_string(), sum_conditions),
                ("dynamic_configs".to_string(), sum_configs),
                ("feature_gates".to_string(), 0),
                ("layer_configs".to_string(), 0),
                ("param_stores".to_string(), 0),
            ]),
        }
        .encode_to_vec(),
    ));
    encode_response(generation, true, frames)
}

fn encode_response(
    generation: u64,
    is_delta: bool,
    mut frames: Vec<pb::SpecsEnvelope>,
) -> SpecsResponse {
    frames.push(pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Done as i32,
        ..Default::default()
    });
    let mut bytes = Vec::new();
    for frame in frames {
        frame.encode_length_delimited(&mut bytes).unwrap();
    }
    let mut writer = brotli::CompressorWriter::new(Vec::new(), 4096, 2, 22);
    writer.write_all(&bytes).unwrap();
    SpecsResponse {
        body: writer.into_inner(),
        generation,
        is_delta,
        after_once: None,
    }
}

fn snapshot(store: &MockDataStore) -> Option<Vec<pb::SpecsEnvelope>> {
    let compressed = store.stored_proto_bytes()?;
    let mut bytes = Vec::new();
    brotli::Decompressor::new(compressed.as_slice(), 4096)
        .read_to_end(&mut bytes)
        .ok()?;
    let mut remaining = bytes.as_slice();
    let mut frames = Vec::new();
    while !remaining.is_empty() {
        frames.push(pb::SpecsEnvelope::decode_length_delimited(&mut remaining).ok()?);
    }
    Some(frames)
}

async fn wait_snapshot(store: &MockDataStore, expected_generation: u64) {
    wait_until(|| {
        snapshot(store)
            .and_then(|frames| pb::SpecsTopLevel::decode(frames[0].data.as_deref()?).ok())
            .is_some_and(|top| top.time == expected_generation)
    })
    .await;
}

fn assert_snapshot(store: &MockDataStore, remote: &RemoteValue) {
    let frames = snapshot(store).unwrap();
    let frame = frames
        .iter()
        .find(|frame| frame.name == LARGE_CONFIG)
        .unwrap();
    let expected_spec = large_spec(2, remote, None);
    assert_eq!(frame.checksum, spec_checksum(&expected_spec));
    let spec = pb::Spec::decode(frame.data.as_deref().unwrap()).unwrap();
    assert!(spec.remote_config_metadata.is_none());
    assert!(spec.rules[0].remote_config_metadata.is_none());
    for value in [
        spec.default_value.as_ref().unwrap(),
        spec.rules[0].return_value.as_ref().unwrap(),
    ] {
        let Some(return_value::Value::RawValue(bytes)) = &value.value else {
            panic!("expected JSON bytes");
        };
        assert_eq!(
            serde_json::from_slice::<Value>(bytes).unwrap(),
            remote.value
        );
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
