mod utils;

use serial_test::serial;
use statsig_rust::{
    ClientInitResponseOptions, GCIRResponseFormat, ObservabilityClient, OpsStatsEventObserver,
    SpecsUpdateListener, Statsig, StatsigOptions, StatsigUser, output_logger::LogLevel,
};
use std::{
    fs,
    path::PathBuf,
    sync::{Arc, Mutex, Weak},
    time::{Duration, Instant},
};

use crate::utils::env_var_guard::EnvVarGuard;
use crate::utils::helpers::load_contents;
use utils::mock_scrapi::{Endpoint, EndpointStub, Method, MockScrapi, StubData};

const SDK_KEY: &str = "secret-key";
const LONG_SDK_KEY: &str = "secret-key-123456789";
const SDK_EXCEPTION_SERVICE_NAME: &str = "sdk-exception-service";

async fn setup(observability_client: &Arc<MockObservabilityClient>) -> (MockScrapi, Statsig) {
    setup_with_sdk_key(observability_client, SDK_KEY).await
}

async fn setup_with_sdk_key(
    observability_client: &Arc<MockObservabilityClient>,
    sdk_key: &str,
) -> (MockScrapi, Statsig) {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    let mock_scrapi = MockScrapi::new().await;

    mock_scrapi
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String("{\"success\": true}".to_string()),
            ..EndpointStub::with_endpoint(Endpoint::LogEvent)
        })
        .await;

    let mut raw_dcs_str = load_contents("eval_proj_dcs.json");
    raw_dcs_str = raw_dcs_str.replace(
        r#""checksum":"8506699639233708000""#,
        r#""IGNORED_CHECKSUM_VALUE":"""#,
    );

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(raw_dcs_str),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let weak_obs_client = Arc::downgrade(observability_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        sdk_key,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            log_event_url: Some(mock_scrapi.url_for_endpoint(Endpoint::LogEvent)),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            output_log_level: Some(LogLevel::Debug),
            specs_sync_interval_ms: Some(1),
            ..StatsigOptions::new()
        })),
    );

    (mock_scrapi, statsig)
}

async fn setup_with_id_lists(
    observability_client: &Arc<MockObservabilityClient>,
) -> (MockScrapi, Statsig) {
    setup_with_id_list_specs(
        observability_client,
        load_contents("eval_proj_dcs.json"),
        StatsigOptions::new(),
    )
    .await
}

async fn setup_with_id_list_specs(
    observability_client: &Arc<MockObservabilityClient>,
    specs: String,
    options: StatsigOptions,
) -> (MockScrapi, Statsig) {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    let mock_scrapi = MockScrapi::new().await;

    let raw_dcs_str = specs.replace(
        r#""checksum":"8506699639233708000""#,
        r#""IGNORED_CHECKSUM_VALUE":"""#,
    );

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(raw_dcs_str),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let manifest_url = format!(
        "{}/{}",
        mock_scrapi.url_for_endpoint(Endpoint::GetIdLists),
        SDK_KEY
    );
    let individual_id_list_url = format!(
        "{}/{}",
        mock_scrapi.url_for_endpoint(Endpoint::DownloadIdListFile),
        "3wHgh0FhoQH0p"
    );
    let id_lists_manifest = format!(
        r#"{{"company_id_list":{{"name":"company_id_list","size":100,"url":"{}","creationTime":1721417546000,"fileID":"4t0BEqak3w1UcidsPcpQXN"}}}}"#,
        individual_id_list_url
    );

    mock_scrapi
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String(id_lists_manifest),
            ..EndpointStub::with_endpoint(Endpoint::GetIdLists)
        })
        .await;

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(load_contents("company_id_list")),
            ..EndpointStub::with_endpoint(Endpoint::DownloadIdListFile)
        })
        .await;

    let weak_obs_client = Arc::downgrade(observability_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            enable_id_lists: Some(true),
            id_lists_url: Some(manifest_url.clone()),
            disable_all_logging: Some(true),
            output_log_level: Some(LogLevel::Debug),
            ..options
        })),
    );

    (mock_scrapi, statsig)
}

async fn setup_with_id_lists_single_list_failure(
    observability_client: &Arc<MockObservabilityClient>,
) -> (MockScrapi, Statsig) {
    std::env::set_var("STATSIG_RUNNING_TESTS", "true");
    let mock_scrapi = MockScrapi::new().await;

    let mut raw_dcs_str = load_contents("eval_proj_dcs.json");
    raw_dcs_str = raw_dcs_str.replace(
        r#""checksum":"8506699639233708000""#,
        r#""IGNORED_CHECKSUM_VALUE":"""#,
    );

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(raw_dcs_str),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let manifest_url = format!(
        "{}/{}",
        mock_scrapi.url_for_endpoint(Endpoint::GetIdLists),
        SDK_KEY
    );
    let individual_id_list_url = format!(
        "{}/{}",
        mock_scrapi.url_for_endpoint(Endpoint::DownloadIdListFile),
        "3wHgh0FhoQH0p"
    );
    let id_lists_manifest = format!(
        r#"{{"company_id_list":{{"name":"company_id_list","size":100,"url":"{}","creationTime":1721417546000,"fileID":"4t0BEqak3w1UcidsPcpQXN"}}}}"#,
        individual_id_list_url
    );

    mock_scrapi
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String(id_lists_manifest),
            ..EndpointStub::with_endpoint(Endpoint::GetIdLists)
        })
        .await;

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String("{\"success\": false}".to_string()),
            status: 500,
            ..EndpointStub::with_endpoint(Endpoint::DownloadIdListFile)
        })
        .await;

    let weak_obs_client = Arc::downgrade(observability_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            enable_id_lists: Some(true),
            id_lists_url: Some(manifest_url.clone()),
            disable_all_logging: Some(true),
            output_log_level: Some(LogLevel::Debug),
            ..StatsigOptions::new()
        })),
    );

    (mock_scrapi, statsig)
}

#[derive(Debug, PartialEq)]
enum RecordedCall {
    Init,
    Increment(
        String,
        f64,
        Option<std::collections::HashMap<String, String>>,
    ),
    Gauge(
        String,
        f64,
        Option<std::collections::HashMap<String, String>>,
    ),
    Dist(
        String,
        f64,
        Option<std::collections::HashMap<String, String>>,
    ),
    Error(String, String),
}

struct MockObservabilityClient {
    pub calls: Mutex<Vec<RecordedCall>>,
}

impl ObservabilityClient for MockObservabilityClient {
    fn init(&self) {
        self.calls.lock().unwrap().push(RecordedCall::Init);
    }

    fn increment(
        &self,
        metric_name: String,
        value: f64,
        tags: Option<std::collections::HashMap<String, String>>,
    ) {
        self.calls
            .lock()
            .unwrap()
            .push(RecordedCall::Increment(metric_name, value, tags));
    }

    fn gauge(
        &self,
        metric_name: String,
        value: f64,
        tags: Option<std::collections::HashMap<String, String>>,
    ) {
        self.calls
            .lock()
            .unwrap()
            .push(RecordedCall::Gauge(metric_name, value, tags));
    }

    fn dist(
        &self,
        metric_name: String,
        value: f64,
        tags: Option<std::collections::HashMap<String, String>>,
    ) {
        self.calls
            .lock()
            .unwrap()
            .push(RecordedCall::Dist(metric_name, value, tags));
    }

    fn error(&self, tag: String, error: String) {
        self.calls
            .lock()
            .unwrap()
            .push(RecordedCall::Error(tag, error));
    }

    fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
        self
    }

    fn should_enable_high_cardinality_for_this_tag(&self, _tag: String) -> Option<bool> {
        Some(true)
    }
}

#[tokio::test]
#[serial]
async fn test_init_called() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (_, statsig) = setup(&obs_client).await;

    statsig.initialize().await.unwrap();

    let calls = obs_client.calls.lock().unwrap();
    // Snapshot gauges may arrive before initialize() returns.
    assert_eq!(
        calls
            .iter()
            .filter(|call| matches!(call, RecordedCall::Init))
            .count(),
        1,
    );
    assert_eq!(calls[0], RecordedCall::Init);
}

#[tokio::test]
#[serial]
async fn test_sdk_initialization_dist_recorded() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (_, statsig) = setup_with_sdk_key(&obs_client, LONG_SDK_KEY).await;

    statsig.initialize().await.unwrap();
    statsig.check_gate(&StatsigUser::with_user_id("test_user"), "test_gate");
    statsig.flush_events().await;

    let calls = obs_client.calls.lock().unwrap();

    let mut found_name = String::new();
    let mut found_value = 0.0;
    let mut found_tags = None;

    for call in calls.iter() {
        if let RecordedCall::Dist(metric_name, value, tags) = call {
            if metric_name == "statsig.sdk.initialization" {
                found_name = metric_name.clone();
                found_value = *value;
                found_tags = tags.clone();
                break;
            }
        }
    }

    let tags = found_tags.unwrap();

    assert_eq!(found_name, "statsig.sdk.initialization");
    assert_ne!(found_value, 0.0);
    assert_eq!(tags.get("source"), Some(&"Network".to_string()));
    assert_eq!(tags.get("init_success"), Some(&"true".to_string()));
    assert_eq!(tags.get("store_populated"), Some(&"true".to_string()));
    assert_eq!(tags.get("sdk_key"), Some(&"secret-key-12".to_string()));
    assert_eq!(
        tags.get("sdk_type"),
        Some(&"statsig-server-core".to_string())
    );
    assert!(tags.get("sdk_version").is_some_and(|v| !v.is_empty()));
}

#[tokio::test]
#[serial]
async fn test_event_logging_metrics_include_request_context() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (mock_scrapi, statsig) = setup(&obs_client).await;

    statsig.initialize().await.unwrap();
    statsig.log_event(
        &StatsigUser::with_user_id("test_user"),
        "test_event",
        None,
        None,
    );
    statsig.flush_events().await;

    let expected_source_api = mock_scrapi.url_for_endpoint(Endpoint::LogEvent);
    let deadline = Instant::now() + Duration::from_secs(1);
    let mut found_success_count = false;
    let mut found_event_count = false;
    let mut found_uncompressed_body_size = false;
    let mut found_max_event_queue_time = false;

    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            found_success_count = calls.iter().any(|call| match call {
                RecordedCall::Increment(metric_name, value, Some(tags)) => {
                    metric_name == "statsig.sdk.events_successfully_sent_count"
                        && *value > 0.0
                        && tags.get("source_api") == Some(&expected_source_api)
                        && tags.get("flush_type").map(String::as_str) == Some("manual")
                }
                _ => false,
            });

            found_event_count = calls.iter().any(|call| match call {
                RecordedCall::Dist(metric_name, value, Some(tags)) => {
                    metric_name == "statsig.sdk.log_event_request_event_count"
                        && *value > 0.0
                        && tags.get("source_api") == Some(&expected_source_api)
                        && tags.get("flush_type").map(String::as_str) == Some("manual")
                }
                _ => false,
            });

            found_uncompressed_body_size = calls.iter().any(|call| match call {
                RecordedCall::Dist(metric_name, value, Some(tags)) => {
                    metric_name == "statsig.sdk.log_event_request_uncompressed_body_size_bytes"
                        && *value > 0.0
                        && tags.get("source_api") == Some(&expected_source_api)
                        && tags.get("flush_type").map(String::as_str) == Some("manual")
                }
                _ => false,
            });

            found_max_event_queue_time = calls.iter().any(|call| match call {
                RecordedCall::Dist(metric_name, value, Some(tags)) => {
                    metric_name == "statsig.sdk.log_event_request_max_event_queue_time_ms"
                        && *value >= 0.0
                        && tags.get("source_api") == Some(&expected_source_api)
                        && tags.get("flush_type").map(String::as_str) == Some("manual")
                }
                _ => false,
            });
        }

        if found_success_count
            && found_event_count
            && found_uncompressed_body_size
            && found_max_event_queue_time
        {
            break;
        }

        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_success_count,
        "Expected events_successfully_sent_count to include source_api and flush_type"
    );
    assert!(
        found_event_count,
        "Expected log_event_request_event_count to include request context"
    );
    assert!(
        found_uncompressed_body_size,
        "Expected log_event_request_uncompressed_body_size_bytes to include request context"
    );
    assert!(
        found_max_event_queue_time,
        "Expected log_event_request_max_event_queue_time_ms to include request context"
    );
}

#[tokio::test]
#[serial]
async fn test_config_propagation_dist_recorded() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (mock_scrapi, statsig) = setup(&obs_client).await;

    statsig.initialize().await.unwrap();
    let has_propagation_metric = || {
        obs_client.calls.lock().unwrap().iter().any(|call| {
            matches!(
                call,
                RecordedCall::Dist(metric_name, _, _)
                    if metric_name == "statsig.sdk.config_propagation_diff"
            )
        })
    };

    // The default fixture intentionally omits a checksum. Re-applying the same
    // checksumless response must not report an old LCUT as new propagation.
    tokio::time::sleep(Duration::from_millis(10)).await;
    assert!(!has_propagation_metric());

    // A changed checksum at the same LCUT is a real reconciliation and should
    // still be reported.
    let repair_test_user = StatsigUser::with_user_id("repair-test-user");
    assert!(!statsig.check_gate(&repair_test_user, "test_country_partial"));

    let mut updated_specs: serde_json::Value =
        serde_json::from_str(&load_contents("eval_proj_dcs.json")).unwrap();
    let initial_lcut = updated_specs["time"].as_u64().unwrap();
    updated_specs["checksum"] = serde_json::json!("equal-lcut-repair-checksum");
    updated_specs["feature_gates"]["test_country_partial"]["enabled"] = serde_json::json!(true);
    updated_specs["feature_gates"]["test_country_partial"]["defaultValue"] =
        serde_json::json!(true);

    mock_scrapi.clear_stubs().await;
    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(updated_specs.to_string()),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let deadline = Instant::now() + Duration::from_secs(1);
    while Instant::now() < deadline
        && (!statsig.check_gate(&repair_test_user, "test_country_partial")
            || !has_propagation_metric())
    {
        tokio::time::sleep(Duration::from_millis(10)).await;
    }
    assert!(statsig.check_gate(&repair_test_user, "test_country_partial"));
    assert!(has_propagation_metric());

    let calls = obs_client.calls.lock().unwrap();

    let mut found_name = String::new();
    let mut found_value = 0.0;
    let mut found_tags = None;

    for call in calls.iter() {
        if let RecordedCall::Dist(metric_name, value, tags) = call {
            if metric_name == "statsig.sdk.config_propagation_diff" {
                found_name = metric_name.clone();
                found_value = *value;
                found_tags = tags.clone();
                break;
            }
        }
    }

    let tags = found_tags.unwrap();

    assert_eq!(found_name, "statsig.sdk.config_propagation_diff");
    assert_ne!(found_value, 0.0);
    assert_eq!(tags.get("source"), Some(&"Network".to_string()));
    assert_eq!(tags.get("sdk_key"), Some(&SDK_KEY.to_string()));
    assert_eq!(tags.get("response_type"), Some(&"full".to_string()));
    assert_eq!(tags.get("lcut"), Some(&initial_lcut.to_string()));
    assert_eq!(tags.get("prev_lcut"), Some(&initial_lcut.to_string()));
}

#[tokio::test]
#[serial]
async fn test_config_no_update_records_response_type() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (mock_scrapi, statsig) = setup(&obs_client).await;
    statsig.initialize().await.unwrap();

    mock_scrapi.clear_stubs().await;
    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String("{\"has_updates\": false}".to_string()),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let deadline = Instant::now() + Duration::from_secs(1);
    let mut found_no_update = false;
    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            found_no_update = calls.iter().any(|call| match call {
                RecordedCall::Increment(metric_name, _, Some(tags)) => {
                    metric_name == "statsig.sdk.config_no_update"
                        && tags.get("response_type").map(String::as_str) == Some("no_update")
                }
                _ => false,
            });
        }

        if found_no_update {
            break;
        }

        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_no_update,
        "Expected config_no_update to include response_type=no_update"
    );
}

#[tokio::test]
#[serial]
async fn test_network_request_latency_tags_recorded_for_dcs_and_id_lists() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (mock_scrapi, statsig) = setup_with_id_lists(&obs_client).await;
    statsig.initialize().await.unwrap();

    let expected_dcs_path = "/v2/download_config_specs";
    let expected_manifest_path = "/v1/get_id_lists";
    let expected_individual_id_list_path = "/v1/download_id_list_file";
    let expected_source_service = mock_scrapi
        .url_for_endpoint(Endpoint::DownloadConfigSpecs)
        .trim_end_matches(expected_dcs_path)
        .to_string();

    let deadline = Instant::now() + Duration::from_secs(1);
    let mut found_all_metrics = false;
    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            let has_dcs_metric = calls.iter().any(|call| match call {
                RecordedCall::Dist(metric_name, _, Some(tags)) => {
                    metric_name == "statsig.sdk.network_request.latency"
                        && tags.get("request_path").map(String::as_str) == Some(expected_dcs_path)
                        && tags.get("status_code").map(String::as_str) == Some("200")
                        && tags.get("is_success").map(String::as_str) == Some("true")
                        && tags.get("deltas_used").map(String::as_str) == Some("false")
                        && tags.get("sdk_key").map(String::as_str) == Some("secret-key")
                        && tags.get("source_service").map(String::as_str)
                            == Some(expected_source_service.as_str())
                }
                _ => false,
            });

            let has_manifest_metric = calls.iter().any(|call| match call {
                RecordedCall::Dist(metric_name, _, Some(tags)) => {
                    metric_name == "statsig.sdk.network_request.latency"
                        && tags.get("request_path").map(String::as_str)
                            == Some(expected_manifest_path)
                        && tags.get("status_code").map(String::as_str) == Some("200")
                        && tags.get("is_success").map(String::as_str) == Some("true")
                        && tags.get("deltas_used").map(String::as_str) == Some("false")
                        && tags.get("sdk_key").map(String::as_str) == Some("secret-key")
                        && tags.get("source_service").map(String::as_str)
                            == Some(expected_source_service.as_str())
                }
                _ => false,
            });

            let has_individual_id_list_metric = calls.iter().any(|call| match call {
                RecordedCall::Dist(metric_name, _, Some(tags)) => {
                    metric_name == "statsig.sdk.network_request.latency"
                        && tags.get("request_path").map(String::as_str)
                            == Some(expected_individual_id_list_path)
                        && tags.get("status_code").map(String::as_str) == Some("200")
                        && tags.get("is_success").map(String::as_str) == Some("true")
                        && tags.get("deltas_used").map(String::as_str) == Some("false")
                        && tags.get("sdk_key").map(String::as_str) == Some("secret-key")
                        && tags.get("source_service").map(String::as_str)
                            == Some(expected_source_service.as_str())
                }
                _ => false,
            });

            found_all_metrics =
                has_dcs_metric && has_manifest_metric && has_individual_id_list_metric;
        }

        if found_all_metrics {
            break;
        }

        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_all_metrics,
        "Expected network_request.latency metrics for DCS, ID list manifest, and individual ID list requests"
    );
}

fn metrics_options() -> StatsigOptions {
    StatsigOptions {
        enable_id_list_access_metrics: Some(true),
        ..StatsigOptions::new()
    }
}

#[tokio::test]
#[serial]
async fn remote_gate_requires_local_metrics_opt_in() {
    for local in [None, Some(false)] {
        let observer = Arc::new(MockObservabilityClient {
            calls: Mutex::new(Vec::new()),
        });
        let (_mock, sdk) = setup_with_id_list_specs(
            &observer,
            id_list_access_specs().to_string(),
            StatsigOptions {
                enable_id_list_access_metrics: local,
                ..StatsigOptions::new()
            },
        )
        .await;
        sdk.initialize().await.unwrap();
        let member = StatsigUser::with_custom_ids(std::collections::HashMap::from([(
            "companyID",
            "marcos_1",
        )]));
        assert!(sdk.check_gate(&member, "segment:company_id_list"));
        sdk.flush_events().await;
        sdk.shutdown().await.unwrap();
        assert!(id_list_sizes(&observer).is_empty());
        assert!(id_list_accesses(&observer).is_empty());
    }
}

fn id_list_access_specs() -> serde_json::Value {
    let mut specs: serde_json::Value =
        serde_json::from_str(&load_contents("eval_proj_dcs.json")).unwrap();
    specs.as_object_mut().unwrap().remove("checksum");
    specs["sdk_configs"]["id_list_access_metrics"] = 1.into();
    specs
}

fn id_list_sizes(observer: &MockObservabilityClient) -> Vec<(String, f64)> {
    let mut sizes = Vec::new();
    for call in observer.calls.lock().unwrap().iter() {
        if let RecordedCall::Gauge(name, size, Some(tags)) = call {
            if name == "statsig.sdk.id_list_size" {
                assert!(tags.contains_key("sdk_type") && tags.contains_key("sdk_version"));
                sizes.push((tags["id_list_name"].clone(), *size));
            }
        }
    }
    sizes.sort_by(|a, b| a.0.cmp(&b.0));
    sizes
}

fn id_list_accesses(observer: &MockObservabilityClient) -> Vec<String> {
    let mut lists = Vec::new();
    for call in observer.calls.lock().unwrap().iter() {
        if let RecordedCall::Increment(name, count, Some(tags)) = call {
            if name == "statsig.sdk.id_list_accessed" {
                assert_eq!(*count, 1.0);
                assert!(tags.contains_key("sdk_type") && tags.contains_key("sdk_version"));
                lists.push(tags["id_list_name"].clone());
            }
        }
    }
    lists.sort();
    lists
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_separate_installed_size_from_first_access() {
    let mut specs = id_list_access_specs();
    let mut repeated_gate = specs["feature_gates"]["segment:company_id_list"].clone();
    repeated_gate["rules"][0]["conditions"] = serde_json::json!(vec!["3614985732"; 32]);
    specs["feature_gates"]["repeated"] = repeated_gate;
    let mut missing_condition = specs["condition_map"]["3614985732"].clone();
    missing_condition["targetValue"] = "missing_list".into();
    specs["condition_map"]["missing"] = missing_condition;
    let mut missing_gate = specs["feature_gates"]["segment:company_id_list"].clone();
    missing_gate["rules"][0]["conditions"] = serde_json::json!(["missing"]);
    specs["feature_gates"]["missing"] = missing_gate;

    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_mock, sdk) =
        setup_with_id_list_specs(&observer, specs.to_string(), metrics_options()).await;
    sdk.initialize().await.unwrap();

    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    let outsider =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "absent")]));
    // The file has 27 distinct IDs. The manifest reports bytes.
    let expected_size = [("company_id_list".to_owned(), 27.0)];
    assert_eventually_eq!(|| id_list_sizes(&observer), expected_size);
    assert!(id_list_accesses(&observer).is_empty());

    assert!(!sdk.check_gate(&member, "missing"));
    assert!(sdk.check_gate(&StatsigUser::with_user_id("1"), "segment:user_id_list"));
    sdk.flush_events().await;
    assert!(sdk.check_gate(&member, "repeated"));
    assert!(!sdk.check_gate(&outsider, "segment:company_id_list"));
    sdk.flush_events().await;
    assert_eventually_eq!(|| id_list_accesses(&observer), ["company_id_list"]);

    sdk.flush_events().await;
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    sdk.flush_events().await;
    tokio::time::sleep(Duration::from_millis(50)).await;
    assert_eq!(id_list_accesses(&observer), ["company_id_list"]);
    assert_eq!(id_list_sizes(&observer), expected_size);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_report_new_size_after_an_incremental_download() {
    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (mock, sdk) = setup_with_id_list_specs(
        &observer,
        id_list_access_specs().to_string(),
        StatsigOptions {
            id_lists_sync_interval_ms: Some(10),
            ..metrics_options()
        },
    )
    .await;
    sdk.initialize().await.unwrap();
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    assert_eventually_eq!(
        || id_list_sizes(&observer),
        [("company_id_list".to_owned(), 27.0)]
    );
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    sdk.flush_events().await;
    assert_eventually_eq!(|| id_list_accesses(&observer), ["company_id_list"]);

    // Delete this member through an append to the same file and creation time.
    let body = format!("{}-34jaY4Sb\n", load_contents("company_id_list"));
    let manifest = serde_json::json!({
        "company_id_list": {
            "name": "company_id_list",
            "size": body.len(),
            "url": format!("{}/3wHgh0FhoQH0p", mock.url_for_endpoint(Endpoint::DownloadIdListFile)),
            "creationTime": 1721417546000_i64,
            "fileID": "4t0BEqak3w1UcidsPcpQXN"
        }
    });
    mock.clear_stubs().await;
    mock.stub(EndpointStub {
        method: Method::GET,
        response: StubData::String(body),
        ..EndpointStub::with_endpoint(Endpoint::DownloadIdListFile)
    })
    .await;
    mock.stub(EndpointStub {
        method: Method::POST,
        response: StubData::String(manifest.to_string()),
        ..EndpointStub::with_endpoint(Endpoint::GetIdLists)
    })
    .await;

    // The install must publish the new size before another lookup or event flush.
    let expected = [
        ("company_id_list".to_owned(), 27.0),
        ("company_id_list".to_owned(), 26.0),
    ];
    assert_eventually_eq!(|| id_list_sizes(&observer), expected);
    assert!(!sdk.check_gate(&member, "segment:company_id_list"));
    sdk.flush_events().await;
    tokio::time::sleep(Duration::from_millis(50)).await;
    assert_eq!(id_list_sizes(&observer), expected);
    assert_eq!(id_list_accesses(&observer), ["company_id_list"]);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_require_numeric_one() {
    for (case, value) in [
        None,
        Some(serde_json::json!(0)),
        Some(serde_json::json!(2)),
        Some(serde_json::json!(-1)),
        Some(serde_json::json!(true)),
        Some(serde_json::json!("1")),
    ]
    .into_iter()
    .enumerate()
    {
        let mut specs = id_list_access_specs();
        match value {
            Some(value) => specs["sdk_configs"]["id_list_access_metrics"] = value,
            None => {
                specs["sdk_configs"]
                    .as_object_mut()
                    .unwrap()
                    .remove("id_list_access_metrics");
            }
        }
        let observer = Arc::new(MockObservabilityClient {
            calls: Mutex::new(Vec::new()),
        });
        let (_mock, sdk) = setup_with_id_list_specs(
            &observer,
            specs.to_string(),
            StatsigOptions {
                sdk_instance_id: Some(format!("id-list-access-disabled-{case}")),
                ..metrics_options()
            },
        )
        .await;
        sdk.initialize().await.unwrap();
        let member = StatsigUser::with_custom_ids(std::collections::HashMap::from([(
            "companyID",
            "marcos_1",
        )]));
        assert!(sdk.check_gate(&member, "segment:company_id_list"));
        sdk.flush_events().await;
        tokio::time::sleep(Duration::from_millis(50)).await;
        assert!(id_list_sizes(&observer).is_empty(), "case {case}");
        assert!(id_list_accesses(&observer).is_empty(), "case {case}");
        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_follow_remote_flag_changes_without_recreation() {
    let mut specs = id_list_access_specs();
    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (mock, sdk) = setup_with_id_list_specs(
        &observer,
        specs.to_string(),
        StatsigOptions {
            sdk_instance_id: Some("id-list-access-remote-toggle".to_owned()),
            specs_sync_interval_ms: Some(10),
            ..metrics_options()
        },
    )
    .await;
    sdk.initialize().await.unwrap();
    let store = sdk.get_context().spec_store;
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    let expected_size = [("company_id_list".to_owned(), 27.0)];
    assert_eventually_eq!(|| id_list_sizes(&observer), expected_size);
    // Queue an access while enabled, then disable before flushing it.
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    for (enabled, check_list, access_reported) in [
        (Some(0.0), true, false),
        (Some(1.0), false, false), // Re-enabling alone must not restore the discarded access.
        (None, true, true),        // An omitted entry retains 1 in the SDK's merged config map.
        (Some(0.0), true, true),
        (Some(1.0), true, true), // A flushed access stays reported across flag changes.
    ] {
        let next_time = specs["time"].as_u64().unwrap() + 1;
        specs["time"] = next_time.into();
        match enabled {
            Some(enabled) => specs["sdk_configs"]["id_list_access_metrics"] = enabled.into(),
            None => {
                specs["sdk_configs"]
                    .as_object_mut()
                    .unwrap()
                    .remove("id_list_access_metrics");
            }
        }
        mock.clear_stubs().await;
        mock.stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(specs.to_string()),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;
        assert_eventually_eq!(|| store.get_current_specs_info().lcut, Some(next_time));

        if check_list {
            assert!(sdk.check_gate(&member, "segment:company_id_list"));
        }
        sdk.flush_events().await;
        if access_reported {
            assert_eventually_eq!(|| id_list_accesses(&observer), ["company_id_list"]);
        } else {
            tokio::time::sleep(Duration::from_millis(50)).await;
            assert!(id_list_accesses(&observer).is_empty());
        }
    }
    tokio::time::sleep(Duration::from_millis(50)).await;
    assert_eq!(id_list_accesses(&observer), ["company_id_list"]);
    assert_eq!(id_list_sizes(&observer), expected_size);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_cover_object_and_string_client_init() {
    let mut specs = id_list_access_specs();
    let mut gate = specs["feature_gates"]["segment:company_id_list"].clone();
    gate["entity"] = "feature_gate".into();
    gate["rules"][0]["conditions"] = serde_json::json!(["3614985732", "3614985732"]);
    specs["feature_gates"] = serde_json::json!({ "membership": gate });
    specs["dynamic_configs"] = serde_json::json!({});
    specs["layer_configs"] = serde_json::json!({});

    for use_string in [false, true] {
        let observer = Arc::new(MockObservabilityClient {
            calls: Mutex::new(Vec::new()),
        });
        let (_mock, sdk) = setup_with_id_list_specs(
            &observer,
            specs.to_string(),
            StatsigOptions {
                sdk_instance_id: Some(format!("id-list-access-client-init-{use_string}")),
                ..metrics_options()
            },
        )
        .await;
        sdk.initialize().await.unwrap();
        let member = StatsigUser::with_custom_ids(std::collections::HashMap::from([(
            "companyID",
            "marcos_1",
        )]));
        if use_string {
            let options = ClientInitResponseOptions {
                response_format: Some(GCIRResponseFormat::InitializeV2),
                ..ClientInitResponseOptions::default()
            };
            let response = sdk.get_client_init_response_with_options_as_string(&member, &options);
            let json: serde_json::Value = serde_json::from_str(&response).unwrap();
            assert_eq!(json["has_updates"], true);
        } else {
            assert!(sdk.get_client_init_response(&member).has_updates);
        }
        sdk.flush_events().await;
        assert_eventually_eq!(|| id_list_accesses(&observer), ["company_id_list"]);
        sdk.shutdown().await.unwrap();
    }
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_use_the_registered_observer() {
    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_mock, mut sdk) = setup_with_id_list_specs(
        &observer,
        id_list_access_specs().to_string(),
        metrics_options(),
    )
    .await;
    sdk.initialize().await.unwrap();

    let options = Arc::make_mut(&mut sdk.options);
    options.observability_client = None;
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    sdk.flush_events().await;
    assert_eventually_eq!(|| id_list_accesses(&observer), ["company_id_list"]);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_stay_local_when_remote_telemetry_is_disabled() {
    let local_observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let ordinary_observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_local_mock, local) = setup_with_id_list_specs(
        &local_observer,
        id_list_access_specs().to_string(),
        StatsigOptions {
            disable_remote_telemetry: Some(true),
            ..metrics_options()
        },
    )
    .await;
    let (_ordinary_mock, ordinary) = setup_with_id_list_specs(
        &ordinary_observer,
        id_list_access_specs().to_string(),
        metrics_options(),
    )
    .await;
    local.initialize().await.unwrap();
    ordinary.initialize().await.unwrap();
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));

    // Both SDKs share an ID. Their distinct remote policies keep samples isolated.
    for (sdk, checks) in [(&local, 1), (&ordinary, 2), (&local, 1)] {
        for _ in 0..checks {
            assert!(sdk.check_gate(&member, "segment:company_id_list"));
        }
        sdk.flush_events().await;
    }
    let expected_size = [("company_id_list".to_owned(), 27.0)];
    for observer in [&local_observer, &ordinary_observer] {
        assert_eventually_eq!(|| id_list_accesses(observer), ["company_id_list"]);
        assert_eventually_eq!(|| id_list_sizes(observer), expected_size);
    }
    tokio::time::sleep(Duration::from_millis(50)).await;
    for observer in [&local_observer, &ordinary_observer] {
        assert_eq!(id_list_accesses(observer), ["company_id_list"]);
        assert_eq!(id_list_sizes(observer), expected_size);
    }
    local.shutdown().await.unwrap();
    ordinary.shutdown().await.unwrap();
}

#[cfg(feature = "testing")]
#[tokio::test]
#[serial]
async fn id_list_access_metrics_flush_periodically() {
    let _tick = EnvVarGuard::set("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "10".into());
    let _min = EnvVarGuard::set("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "10".into());
    let _max = EnvVarGuard::set("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS", "20".into());
    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_mock, sdk) = setup_with_id_list_specs(
        &observer,
        id_list_access_specs().to_string(),
        metrics_options(),
    )
    .await;
    sdk.initialize().await.unwrap();
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    assert_eventually_eq!(|| id_list_accesses(&observer), ["company_id_list"]);
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_respect_silent_client() {
    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_mock, sdk) = setup_with_id_list_specs(
        &observer,
        id_list_access_specs().to_string(),
        metrics_options().suppress_diagnostic_output(true),
    )
    .await;
    sdk.initialize().await.unwrap();
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    sdk.flush_events().await;
    tokio::time::sleep(Duration::from_millis(50)).await;
    assert!(id_list_sizes(&observer).is_empty());
    assert!(id_list_accesses(&observer).is_empty());
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn id_list_access_metrics_publish_pending_sample_on_shutdown() {
    let observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_mock, sdk) = setup_with_id_list_specs(
        &observer,
        id_list_access_specs().to_string(),
        metrics_options(),
    )
    .await;
    sdk.initialize().await.unwrap();
    let sibling_observer = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });
    let (_sibling_mock, sibling) = setup_with_id_lists(&sibling_observer).await;
    let member =
        StatsigUser::with_custom_ids(std::collections::HashMap::from([("companyID", "marcos_1")]));
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    sdk.shutdown().await.unwrap();
    // Keep a subscriber alive after the evaluating SDK shuts down.
    assert_eventually_eq!(|| id_list_accesses(&sibling_observer), ["company_id_list"]);
    sibling.shutdown().await.unwrap();
}

#[tokio::test]
#[serial]
async fn test_id_lists_sync_overall_latency_tags_recorded_for_success() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (_mock_scrapi, statsig) = setup_with_id_lists(&obs_client).await;
    statsig.initialize().await.unwrap();

    let mut found_tags = None;
    let mut found_value = 0.0;

    let deadline = Instant::now() + Duration::from_secs(1);
    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            for call in calls.iter() {
                if let RecordedCall::Dist(metric_name, value, tags) = call {
                    if metric_name == "statsig.sdk.id_lists_sync_overall.latency" {
                        found_tags = tags.clone();
                        found_value = *value;
                        break;
                    }
                }
            }
        }
        if found_tags.is_some() {
            break;
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_tags.is_some(),
        "Expected id_lists_sync_overall.latency metric"
    );
    let tags = found_tags.unwrap();

    assert_eq!(
        tags.get("id_lists_sync_success").map(String::as_str),
        Some("true")
    );
    assert!(found_value > 0.0);
    assert_eq!(
        tags.get("id_list_manifest_success"),
        Some(&"true".to_string())
    );
    assert_eq!(
        tags.get("succeed_single_id_list_number"),
        Some(&"1".to_string())
    );
}

#[tokio::test]
#[serial]
async fn test_id_lists_sync_overall_latency_tags_recorded_for_single_list_failure() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (_mock_scrapi, statsig) = setup_with_id_lists_single_list_failure(&obs_client).await;
    let _ = statsig.initialize().await;

    let mut found_tags = None;
    let mut found_value = 0.0;

    let deadline = Instant::now() + Duration::from_secs(1);
    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            for call in calls.iter() {
                if let RecordedCall::Dist(metric_name, value, tags) = call {
                    if metric_name == "statsig.sdk.id_lists_sync_overall.latency" {
                        found_tags = tags.clone();
                        found_value = *value;
                        break;
                    }
                }
            }
        }
        if found_tags.is_some() {
            break;
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_tags.is_some(),
        "Expected id_lists_sync_overall.latency metric"
    );
    let tags = found_tags.unwrap();

    assert_eq!(
        tags.get("id_lists_sync_success").map(String::as_str),
        Some("false")
    );
    assert!(found_value > 0.0);
    assert_eq!(
        tags.get("id_list_manifest_success"),
        Some(&"true".to_string())
    );
    assert_eq!(
        tags.get("succeed_single_id_list_number"),
        Some(&"0".to_string())
    );
}

#[tokio::test]
#[serial]
async fn test_sdk_error_capture_uses_real_network_failure() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let mock_scrapi = MockScrapi::new().await;
    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String("{\"success\": false}".to_string()),
            status: 500,
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;
    mock_scrapi
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String("{\"success\": true}".to_string()),
            ..EndpointStub::with_endpoint(Endpoint::SdkException)
        })
        .await;

    let _sdk_exception_url_guard = EnvVarGuard::set(
        "STATSIG_SDK_EXCEPTION_URL",
        mock_scrapi.url_for_endpoint(Endpoint::SdkException),
    );
    let weak_obs_client = Arc::downgrade(&obs_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            disable_all_logging: Some(true),
            output_log_level: Some(LogLevel::Debug),
            service_name: Some(SDK_EXCEPTION_SERVICE_NAME.to_string()),
            ..StatsigOptions::new()
        })),
    );

    let _ = statsig.initialize().await;

    let deadline = Instant::now() + Duration::from_secs(2);
    let mut found_error_call = false;
    let mut found_exception_count = false;
    let mut found_network_exception = false;
    let mut found_sdk_exception_post = false;

    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            found_error_call = calls.iter().any(|call| match call {
                RecordedCall::Error(tag, error) => {
                    tag == "NetworkClient"
                        && error.contains("RetriesExhausted")
                        && error.contains("download_config_specs")
                }
                _ => false,
            });

            found_network_exception = calls.iter().any(|call| match call {
                RecordedCall::Error(tag, error) => {
                    tag == "NetworkClient" && error.contains("RetriesExhausted")
                }
                _ => false,
            });

            found_exception_count = calls.iter().any(|call| match call {
                RecordedCall::Increment(metric_name, value, Some(tags)) => {
                    metric_name == "statsig.sdk.sdk_exceptions_count"
                        && *value == 1.0
                        && tags.get("tag").map(String::as_str) == Some("NetworkClient")
                        && tags.get("exception").map(String::as_str) == Some("RetriesExhausted")
                        && tags.get("request_path").map(String::as_str)
                            == Some("/v2/download_config_specs")
                        && tags.get("status_code").map(String::as_str) == Some("500")
                        && tags.get("sdk_type").map(String::as_str) == Some("statsig-server-core")
                        && tags.get("sdk_version").is_some_and(|v| !v.is_empty())
                }
                _ => false,
            });
        }

        found_sdk_exception_post =
            mock_scrapi.times_called_for_endpoint(Endpoint::SdkException) > 0;

        if found_error_call
            && found_network_exception
            && found_exception_count
            && found_sdk_exception_post
        {
            break;
        }

        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_error_call,
        "Expected NetworkClient SDK error callback for a real retry-exhausted request"
    );
    assert!(
        found_network_exception,
        "Expected captured NetworkClient SDK exception name to be RetriesExhausted"
    );
    assert!(
        found_exception_count,
        "Expected sdk_exceptions_count metric for the captured NetworkClient SDK error"
    );
    assert!(
        found_sdk_exception_post,
        "Expected SDK exception post to be routed to MockScrapi"
    );

    let sdk_exception_requests = mock_scrapi.get_requests_for_endpoint(Endpoint::SdkException);
    let sdk_exception_body: serde_json::Value =
        serde_json::from_slice(&sdk_exception_requests[0].body).unwrap();
    let statsig_options_raw = sdk_exception_body
        .get("statsigOptions")
        .and_then(|value| value.as_str())
        .expect("Expected SDK exception body to include statsigOptions");
    let statsig_options: serde_json::Value = serde_json::from_str(statsig_options_raw).unwrap();
    assert_eq!(
        statsig_options
            .get("service_name")
            .and_then(|value| value.as_str()),
        Some(SDK_EXCEPTION_SERVICE_NAME)
    );
}

#[tokio::test]
#[serial]
async fn test_shutdown_drops() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let (_, statsig) = setup(&obs_client).await;

    statsig.initialize().await.unwrap();

    assert_eq!(Arc::strong_count(&obs_client), 1);

    statsig.flush_events().await;
    statsig.shutdown().await.unwrap();
    drop(statsig);

    assert_eq!(Arc::strong_count(&obs_client), 1);
}

#[tokio::test]
#[serial]
async fn test_init_from_network() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let mock_scrapi = MockScrapi::new().await;

    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");
    let dcs = fs::read_to_string(path).expect("Unable to read file");

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(dcs),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    mock_scrapi
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String("{\"success\": true}".to_string()),
            ..EndpointStub::with_endpoint(Endpoint::LogEvent)
        })
        .await;

    let weak_obs_client = Arc::downgrade(&obs_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            log_event_url: Some(mock_scrapi.url_for_endpoint(Endpoint::LogEvent)),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            output_log_level: Some(LogLevel::Debug),
            specs_sync_interval_ms: Some(1),
            ..StatsigOptions::new()
        })),
    );

    let _ = statsig.initialize().await;
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;

    let calls = obs_client.calls.lock().unwrap();

    let mut found_name = String::new();
    let mut found_value = 0.0;
    let mut found_tags = None;

    for call in calls.iter() {
        if let RecordedCall::Dist(metric_name, value, tags) = call {
            if metric_name == "statsig.sdk.initialization" {
                found_name = metric_name.clone();
                found_value = *value;
                found_tags = tags.clone();
                break;
            }
        }
    }

    let tags = found_tags.unwrap();

    assert_eq!(found_name, "statsig.sdk.initialization");
    assert_ne!(found_value, 0.0);
    assert_eq!(tags.get("source"), Some(&"Network".to_string()));
    assert_eq!(tags.get("init_success"), Some(&"true".to_string()));
    assert_eq!(tags.get("store_populated"), Some(&"true".to_string()));
    assert_eq!(tags.get("sdk_key"), Some(&SDK_KEY.to_string()));
    assert_eq!(
        tags.get("sdk_type"),
        Some(&"statsig-server-core".to_string())
    );
    assert!(tags.get("sdk_version").is_some_and(|v| !v.is_empty()));
    assert_eq!(
        tags.get("init_source_api"),
        Some(&mock_scrapi.get_server_api())
    );
}

#[tokio::test]
#[serial]
async fn test_config_sync_overall_latency_recorded_for_network_error() {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let mock_scrapi = MockScrapi::new().await;

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String("{\"success\": false}".to_string()),
            status: 500,
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let weak_obs_client = Arc::downgrade(&obs_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            disable_all_logging: Some(true),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            output_log_level: Some(LogLevel::Debug),
            specs_sync_interval_ms: Some(5),
            ..StatsigOptions::new()
        })),
    );

    let _ = statsig.initialize().await;
    tokio::time::sleep(std::time::Duration::from_millis(20)).await;

    let mut found_tags = None;
    let mut found_value = 0.0;

    let deadline = Instant::now() + Duration::from_secs(1);
    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            for call in calls.iter() {
                if let RecordedCall::Dist(metric_name, value, tags) = call {
                    if metric_name == "statsig.sdk.config_sync_overall.latency" {
                        found_tags = tags.clone();
                        found_value = *value;
                        break;
                    }
                }
            }
        }
        if found_tags.is_some() {
            break;
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_tags.is_some(),
        "Expected config_sync_overall.latency metric"
    );
    let tags = found_tags.unwrap();
    let error = tags.get("error").cloned().unwrap_or_default();

    assert!(found_value > 0.0);
    assert_eq!(tags.get("source_api"), Some(&mock_scrapi.get_server_api()));
    assert_eq!(tags.get("network_success"), Some(&"false".to_string()));
    assert_eq!(tags.get("process_success"), Some(&"false".to_string()));
    assert_eq!(tags.get("deltas_used"), Some(&"false".to_string()));
    assert_eq!(tags.get("format"), Some(&"unknown".to_string()));
    assert!(error.contains("500"));
}

async fn config_sync_full_fallback_tags(
    response_reason: Option<&str>,
    response_source: Option<&str>,
) -> std::collections::HashMap<String, String> {
    let obs_client = Arc::new(MockObservabilityClient {
        calls: Mutex::new(Vec::new()),
    });

    let mock_scrapi = MockScrapi::new().await;
    let mut raw_dcs_str = load_contents("eval_proj_dcs.json");
    raw_dcs_str = raw_dcs_str.replace(
        r#""checksum":"8506699639233708000""#,
        r#""IGNORED_CHECKSUM_VALUE":"""#,
    );

    let mut response_headers = std::collections::HashMap::new();
    if let Some(reason) = response_reason {
        response_headers.insert(
            "x-statsig-delta-fallback-reason".to_string(),
            reason.to_string(),
        );
    }
    if let Some(source) = response_source {
        response_headers.insert(
            "x-statsig-delta-fallback-source".to_string(),
            source.to_string(),
        );
    }

    mock_scrapi
        .stub(EndpointStub {
            method: Method::GET,
            response: StubData::String(raw_dcs_str),
            res_headers: (!response_headers.is_empty()).then_some(response_headers),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let weak_obs_client = Arc::downgrade(&obs_client) as Weak<dyn ObservabilityClient>;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            observability_client: Some(weak_obs_client),
            disable_all_logging: Some(true),
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            enable_dcs_deltas: Some(true),
            specs_sync_interval_ms: Some(5_000),
            output_log_level: Some(LogLevel::Debug),
            ..StatsigOptions::new()
        })),
    );

    statsig.initialize().await.unwrap();

    let deadline = Instant::now() + Duration::from_secs(1);
    let mut found_tags = None;
    while Instant::now() < deadline {
        {
            let calls = obs_client.calls.lock().unwrap();
            for call in calls.iter() {
                if let RecordedCall::Increment(metric_name, value, tags) = call {
                    if metric_name == "statsig.sdk.config_sync_full_fallback.count" && *value == 1.0
                    {
                        found_tags = tags.clone();
                        break;
                    }
                }
            }
        }
        if found_tags.is_some() {
            break;
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }

    assert!(
        found_tags.is_some(),
        "Expected config_sync_full_fallback.count metric"
    );
    let tags = found_tags.unwrap();
    assert_eq!(tags.get("cursor_state"), Some(&"initial".to_string()));
    assert_eq!(tags.get("source_api"), Some(&mock_scrapi.get_server_api()));
    assert_eq!(
        tags.get("sdk_type"),
        Some(&"statsig-server-core".to_string())
    );
    assert!(tags.get("sdk_version").is_some_and(|v| !v.is_empty()));

    statsig.shutdown().await.unwrap();
    tags
}

#[tokio::test]
#[serial]
async fn test_config_sync_full_fallback_count_records_sfp_reason() {
    let tags =
        config_sync_full_fallback_tags(Some("before_earliest_lcut"), Some("local_compute")).await;

    assert_eq!(
        tags.get("fallback_reason"),
        Some(&"before_earliest_lcut".to_string())
    );
    assert_eq!(
        tags.get("fallback_source"),
        Some(&"local_compute".to_string())
    );
}

#[tokio::test]
#[serial]
async fn test_config_sync_full_fallback_count_records_missing_header() {
    let tags = config_sync_full_fallback_tags(None, None).await;

    assert_eq!(
        tags.get("fallback_reason"),
        Some(&"missing_header".to_string())
    );
    assert_eq!(
        tags.get("fallback_source"),
        Some(&"missing_header".to_string())
    );
}

#[tokio::test]
#[serial]
async fn test_config_sync_full_fallback_count_records_invalid_header() {
    let tags =
        config_sync_full_fallback_tags(Some("raw-unbounded-reason"), Some("raw-unbounded-source"))
            .await;

    assert_eq!(
        tags.get("fallback_reason"),
        Some(&"invalid_header".to_string())
    );
    assert_eq!(
        tags.get("fallback_source"),
        Some(&"invalid_header".to_string())
    );
}
