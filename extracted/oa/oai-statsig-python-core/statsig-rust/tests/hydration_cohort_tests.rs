mod utils;

use std::process::Command;
use std::sync::{Arc, Weak};

use serde_json::json;
use sha2::{Digest, Sha256};
use statsig_rust::{
    DynamicConfigEvaluationOptions, ObservabilityClient, Statsig, StatsigOptions, StatsigUser,
};
use utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use utils::mock_observability_client::MockObservabilityClient;
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

const TELEMETRY_ENV: &str = "STATSIG_HYDRATION_TELEMETRY";
const CHILD: &str = "STATSIG_HYDRATION_COHORT_TEST_CHILD";

#[test]
fn hydration_cohort_labels_are_always_present() {
    if std::env::var(CHILD).as_deref() == Ok("1") {
        tokio::runtime::Runtime::new()
            .unwrap()
            .block_on(check_sdk_cohorts());
        return;
    }

    // Cohort labels are unconditional, including with the former opt-in values.
    // Isolate environments so no concurrent test observes these settings.
    for value in [None, Some("0"), Some("invalid"), Some("true"), Some("1")] {
        let mut command = Command::new(std::env::current_exe().unwrap());
        command
            .args([
                "--exact",
                "hydration_cohort_labels_are_always_present",
                "--nocapture",
            ])
            .env(CHILD, "1")
            .env("STATSIG_RUNNING_TESTS", "true")
            .env_remove(TELEMETRY_ENV);
        if let Some(value) = value {
            command.env(TELEMETRY_ENV, value);
        }
        let output = command.output().unwrap();
        assert!(
            output.status.success(),
            "control {value:?}:\n{}\n{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr),
        );
    }
}

async fn check_sdk_cohorts() {
    let server = MockServer::start().await;
    let value = json!({"marker": "hydrated", "padding": "x".repeat(8192)});
    let body = serde_json::to_vec(&value).unwrap();
    let sha: String = Sha256::digest(&body)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect();
    let blob_path = format!("/v1/dynamic_config_value/{sha}");
    Mock::given(method("GET"))
        .and(path(&blob_path))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(body.clone()),
        )
        .expect(1)
        .mount(&server)
        .await;
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "dynamic_configs": {"large_config": {
                "type": "dynamic_config", "salt": "large", "enabled": true,
                "defaultValue": {"value": blob_path},
                "remoteConfigMetadata": {
                    "sha256": sha, "byteLength": body.len(),
                    "contentType": "application/json", "compression": "none"
                },
                "rules": [], "idType": "userID", "entity": "dynamic_config", "version": 1
            }},
            "feature_gates": {}, "layer_configs": {}, "experiment_to_layer": {},
            "condition_map": {}, "has_updates": true, "time": 1,
            "company_id": "test-company", "response_format": "dcs-v2"
        })))
        .mount(&server)
        .await;
    let observer = Arc::new(MockObservabilityClient::new());
    let sdk = Statsig::new(
        "secret-hydration-control",
        Some(Arc::new(StatsigOptions {
            specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
            remote_config_value_source_url: Some(server.uri()),
            enable_id_lists: Some(false),
            disable_country_lookup: Some(true),
            fallback_to_statsig_api: Some(false),
            event_logging_adapter: Some(Arc::new(
                MockEventLoggingAdapter::new_with_background_flush(false),
            )),
            observability_client: Some(Arc::downgrade(&observer) as Weak<dyn ObservabilityClient>),
            ..StatsigOptions::new()
        })),
    );
    sdk.initialize().await.unwrap();
    assert_eq!(
        serde_json::to_value(
            sdk.get_dynamic_config_with_options(
                &StatsigUser::with_user_id("user"),
                "large_config",
                DynamicConfigEvaluationOptions {
                    disable_exposure_logging: true
                },
            )
            .value
        )
        .unwrap(),
        value
    );
    let names = ["count", "latency", "result", "bytes"];
    let events = tokio::time::timeout(std::time::Duration::from_secs(5), async {
        loop {
            let events = observer
                .increment_calls
                .lock()
                .unwrap()
                .iter()
                .chain(observer.dist_calls.lock().unwrap().iter())
                .filter(|(name, _, _)| {
                    names.iter().any(|suffix| {
                        name == &format!("statsig.sdk.remote_config_hydration.{suffix}")
                    })
                })
                .cloned()
                .collect::<Vec<_>>();
            if events.len() == names.len() {
                break events;
            }
            tokio::time::sleep(std::time::Duration::from_millis(5)).await;
        }
    })
    .await
    .unwrap();
    for (_, _, tags) in events {
        let tags = tags.unwrap_or_default();
        assert_eq!(
            tags.get("config_sync_trigger").map(String::as_str),
            Some("http_adapter_start")
        );
        assert_eq!(
            tags.get("config_payload_type").map(String::as_str),
            Some("full_snapshot")
        );
    }
    sdk.shutdown().await.unwrap();
}
