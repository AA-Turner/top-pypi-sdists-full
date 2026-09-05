mod utils;

use crate::utils::helpers::load_contents;
use crate::utils::mock_specs_listener::MockSpecsListener;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use statsig_rust::{
    SpecsAdapter, SpecsSource, StatsigErr, StatsigLocalFileSpecsAdapter, StatsigRuntime,
};
use std::fs;
use std::sync::Arc;
use utils::mock_scrapi::{Endpoint, EndpointStub, Method, MockScrapi, StubData};
use wiremock::matchers::{method as wiremock_method, path, query_param};
use wiremock::{Mock, MockServer, ResponseTemplate};

const SDK_KEY: &str = "server-local-specs-test";
const SPECS_FILE_NAME: &str = "3099846163_specs.json"; // djb2(SDK_KEY)_specs.json
const DOWNLOAD_PATH_PREFIX: &str = "/v1/dynamic_config_value/";

async fn setup(test_name: &str) -> (MockScrapi, String) {
    let test_path = create_test_path(test_name);

    let mock_scrapi = MockScrapi::new().await;
    let dcs = load_contents("eval_proj_dcs.json");

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(dcs),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    (mock_scrapi, test_path)
}

fn create_test_path(test_name: &str) -> String {
    let test_path = format!("/tmp/{test_name}");
    if std::path::Path::new(&test_path).exists() {
        fs::remove_dir_all(&test_path).unwrap();
    }
    fs::create_dir_all(&test_path).unwrap();
    test_path
}

#[tokio::test]
#[allow(clippy::await_holding_lock)]
async fn test_statsig_local_file_specs_adapter() {
    let (mock_scrapi, test_path) = setup("test_statsig_local_file_specs_adapter").await;
    let url = mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs);
    let adapter = StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, Some(url), false, false);

    adapter.fetch_and_write_to_file().await.unwrap();

    let out_path = format!("{test_path}/{SPECS_FILE_NAME}");
    assert!(
        std::path::Path::new(&out_path).exists(),
        "The specs file was not created."
    );
}

#[tokio::test]
#[allow(clippy::await_holding_lock)]
async fn test_concurrent_access() {
    let (mock_scrapi, test_path) = setup("test_concurrent_access").await;
    let url = mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs);

    let tasks: Vec<_> = (0..10)
        .map(|_| {
            let url = url.clone();
            let test_path = test_path.clone();
            tokio::task::spawn(async move {
                let adapter =
                    StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, Some(url), false, false);
                adapter.fetch_and_write_to_file().await.unwrap();
                let _ = adapter.resync_from_file();
            })
        })
        .collect();

    let results = futures::future::join_all(tasks).await;
    assert_eq!(results.len(), 10);
}

#[tokio::test]
#[allow(clippy::await_holding_lock)]
async fn test_sending_since_time() {
    let (mock_scrapi, test_path) = setup("test_sending_since_time").await;
    let url = mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs);
    let adapter = StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, Some(url), false, false);
    adapter.fetch_and_write_to_file().await.unwrap();

    let reqs = mock_scrapi.get_requests_for_endpoint(Endpoint::DownloadConfigSpecs);
    assert_eq!(reqs.len(), 1);
    assert!(!reqs[0].url.to_string().contains("sinceTime="));

    adapter.fetch_and_write_to_file().await.unwrap();

    let reqs = mock_scrapi.get_requests_for_endpoint(Endpoint::DownloadConfigSpecs);
    assert_eq!(reqs.len(), 2);
    assert!(reqs[1].url.to_string().contains("sinceTime=1767981029384"));
}

#[tokio::test]
#[allow(clippy::await_holding_lock)]
async fn test_sending_checksum() {
    let (mock_scrapi, test_path) = setup("test_sending_checksum").await;
    let url = mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs);
    let adapter = StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, Some(url), false, false);
    adapter.fetch_and_write_to_file().await.unwrap();

    let mock_scrapi = MockScrapi::new().await;
    let dcs = load_contents("dcs_with_checksum.json");

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(dcs),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let url = mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs);
    let adapter = StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, Some(url), false, false);
    adapter.fetch_and_write_to_file().await.unwrap();

    let reqs = mock_scrapi.get_requests_for_endpoint(Endpoint::DownloadConfigSpecs);
    assert_eq!(reqs.len(), 1);
    assert!(!reqs[0].url.to_string().contains("checksum=1767981029384"));

    adapter.fetch_and_write_to_file().await.unwrap();

    let reqs = mock_scrapi.get_requests_for_endpoint(Endpoint::DownloadConfigSpecs);
    assert_eq!(reqs.len(), 2);
    assert!(reqs[1].url.to_string().contains("checksum=1234567890"));
}

#[tokio::test]
#[allow(clippy::await_holding_lock)]
async fn test_syncing_from_file() {
    let (mock_scrapi, test_path) = setup("test_syncing_from_file").await;
    let url = mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs);

    let adapter = Arc::new(StatsigLocalFileSpecsAdapter::new(
        SDK_KEY,
        &test_path,
        Some(url),
        false,
        false,
    ));
    adapter.fetch_and_write_to_file().await.unwrap();

    let statsig_rt = StatsigRuntime::get_runtime();
    let listener = Arc::new(MockSpecsListener::default());
    adapter.initialize(listener.clone());
    adapter.clone().start(&statsig_rt).await.unwrap();

    adapter.resync_from_file().unwrap();

    let update = &listener.nullable_get_most_recent_update().unwrap();
    assert_eq!(update.source, SpecsSource::Adapter("FileBased".to_string()));
}

#[test]
fn sync_from_file_allows_nested_remote_config_metadata_user_json() {
    let test_path = create_test_path("sync_from_file_allows_nested_metadata_user_json");
    let file_path = format!("{test_path}/{SPECS_FILE_NAME}");
    let payload = json!({
        "dynamic_configs": {
            "ordinary_config": {
                "type": "dynamic_config",
                "salt": "salt",
                "defaultValue": {
                    "remoteConfigMetadata": "ordinary user data"
                },
                "enabled": true,
                "rules": [],
                "idType": "userID",
                "entity": "dynamic_config"
            }
        },
        "feature_gates": {},
        "layer_configs": {},
        "has_updates": true,
        "time": 1
    });
    fs::write(&file_path, serde_json::to_vec(&payload).unwrap()).unwrap();

    let adapter = StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, None, false, false);
    let listener = Arc::new(MockSpecsListener::default());
    adapter.initialize(listener.clone());

    adapter.resync_from_file().unwrap();

    let mut update = listener.force_get_most_recent_update();
    let replayed: Value = update.data.deserialize_into().unwrap();
    assert_eq!(
        replayed["dynamic_configs"]["ordinary_config"]["defaultValue"]["remoteConfigMetadata"],
        json!("ordinary user data")
    );
}

#[test]
fn sync_from_file_rejects_remote_metadata_without_decoding_raw_numbers() {
    let test_path = create_test_path("sync_from_file_rejects_raw_number_metadata");
    let file_path = format!("{test_path}/{SPECS_FILE_NAME}");
    // Keep 1e400 as source text so this covers the production Value parse
    // failure that must not hide rule-level producer metadata.
    let payload = r#"{
        "dynamic_configs": {
            "config": {
                "type": "dynamic_config",
                "salt": "salt",
                "defaultValue": {"large": 1e400},
                "enabled": true,
                "rules": [{
                    "name": "rule",
                    "passPercentage": 100,
                    "returnValue": "https://statsigcdn.openai.com/v1/dynamic_config_value/test",
                    "id": "rule",
                    "conditions": [],
                    "idType": "userID",
                    "remoteConfigMetadata": {}
                }],
                "idType": "userID",
                "entity": "dynamic_config"
            }
        },
        "feature_gates": {},
        "layer_configs": {},
        "has_updates": true,
        "time": 1
    }"#;
    fs::write(&file_path, payload).unwrap();

    let adapter = StatsigLocalFileSpecsAdapter::new(SDK_KEY, &test_path, None, false, false);
    let listener = Arc::new(MockSpecsListener::default());
    adapter.initialize(listener);

    assert!(matches!(
        adapter.resync_from_file(),
        Err(StatsigErr::InvalidOperation(message))
            if message.contains("resync_from_file_with_hydration")
    ));
}

#[tokio::test]
async fn start_hydrates_and_rewrites_legacy_remote_value_file() {
    let test_path = create_test_path("start_hydrates_legacy_remote_value_file");
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"from-legacy-file"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let legacy = legacy_remote_dcs(&server, &download_path, &sha, remote_value.len());
    let file_path = format!("{test_path}/{SPECS_FILE_NAME}");
    fs::write(&file_path, legacy.to_string()).unwrap();
    mount_remote_value(&server, &download_path, remote_value).await;

    let adapter = Arc::new(StatsigLocalFileSpecsAdapter::new(
        SDK_KEY,
        &test_path,
        Some(format!("{}/v2/download_config_specs", server.uri())),
        false,
        false,
    ));
    assert!(matches!(
        adapter.resync_from_file(),
        Err(StatsigErr::InvalidOperation(message))
            if message.contains("resync_from_file_with_hydration")
    ));
    let listener = Arc::new(MockSpecsListener::default());
    adapter.initialize(listener.clone());

    adapter
        .clone()
        .start(&StatsigRuntime::get_runtime())
        .await
        .unwrap();

    let mut update = listener.force_get_most_recent_update();
    let hydrated: Value = update.data.deserialize_into().unwrap();
    assert_eq!(
        hydrated["dynamic_configs"]["large_config"]["defaultValue"],
        json!({"large": "from-legacy-file"})
    );
    let rewritten: Value = serde_json::from_str(&fs::read_to_string(file_path).unwrap()).unwrap();
    assert_eq!(
        rewritten["dynamic_configs"]["large_config"]["defaultValue"],
        json!({"large": "from-legacy-file"})
    );
    assert!(
        rewritten["dynamic_configs"]["large_config"]
            .get("remoteConfigMetadata")
            .is_none()
    );
    server.verify().await;
}

#[tokio::test]
async fn fetch_repairs_legacy_file_before_no_update_response() {
    let test_path = create_test_path("fetch_repairs_legacy_file_before_no_update_response");
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"from-legacy-file"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let legacy = legacy_remote_dcs(&server, &download_path, &sha, remote_value.len());
    let file_path = format!("{test_path}/{SPECS_FILE_NAME}");
    fs::write(&file_path, legacy.to_string()).unwrap();
    mount_remote_value(&server, &download_path, remote_value).await;
    Mock::given(wiremock_method("GET"))
        .and(path("/v2/download_config_specs"))
        .and(query_param("sinceTime", "123"))
        .and(query_param("checksum", "cachechecksum"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({"has_updates": false})))
        .expect(1)
        .mount(&server)
        .await;

    let adapter = StatsigLocalFileSpecsAdapter::new(
        SDK_KEY,
        &test_path,
        Some(format!("{}/v2/download_config_specs", server.uri())),
        false,
        false,
    );
    adapter.fetch_and_write_to_file().await.unwrap();

    let rewritten: Value = serde_json::from_str(&fs::read_to_string(file_path).unwrap()).unwrap();
    assert_eq!(
        rewritten["dynamic_configs"]["large_config"]["defaultValue"],
        json!({"large": "from-legacy-file"})
    );
    assert!(
        rewritten["dynamic_configs"]["large_config"]
            .get("remoteConfigMetadata")
            .is_none()
    );
    server.verify().await;
}

fn legacy_remote_dcs(
    server: &MockServer,
    download_path: &str,
    sha: &str,
    byte_length: usize,
) -> Value {
    json!({
        "dynamic_configs": {
            "large_config": {
                "type": "dynamic_config",
                "salt": "salt",
                "enabled": true,
                "defaultValue": {"value": format!("{}{download_path}", server.uri())},
                "remoteConfigMetadata": {
                    "sha256": sha,
                    "byteLength": byte_length,
                    "contentType": "application/json",
                    "compression": "none"
                },
                "rules": [],
                "idType": "userID",
                "entity": "dynamic_config",
                "version": 1,
                "checksum": "config-checksum"
            }
        },
        "feature_gates": {},
        "experiment_to_layer": {},
        "layer_configs": {},
        "has_updates": true,
        "time": 123,
        "checksum": "cachechecksum",
        "company_id": "company",
        "condition_map": {},
        "response_format": "dcs-v2"
    })
}

async fn mount_remote_value(server: &MockServer, download_path: &str, body: &'static [u8]) {
    Mock::given(wiremock_method("GET"))
        .and(path(download_path.to_string()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(body),
        )
        .expect(1)
        .mount(server)
        .await;
}

fn lowercase_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut result = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        result.push(HEX[(byte >> 4) as usize] as char);
        result.push(HEX[(byte & 0x0f) as usize] as char);
    }
    result
}
