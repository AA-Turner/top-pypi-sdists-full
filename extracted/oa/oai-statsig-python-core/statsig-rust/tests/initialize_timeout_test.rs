mod utils;
use std::sync::Arc;
use utils::{
    mock_scrapi::{Endpoint, EndpointStub, Method, MockScrapi},
    mock_specs_adapter::MockSpecsAdapter,
};

use statsig_rust::{
    networking::{NetworkClient, RequestArgs},
    Statsig, StatsigOptions, StatsigUser,
};

const SDK_KEY: &str = "secret-key";

#[tokio::test]
async fn test_initialize_timeout() {
    let user = StatsigUser::with_user_id("my_user".to_string());
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(MockSpecsAdapter::delayed(
                "tests/data/eval_proj_dcs.json",
                200,
            ))),
            environment: Some("development".to_string()),
            init_timeout_ms: Some(20),
            specs_sync_interval_ms: Some(1),
            output_log_level: Some(statsig_rust::output_logger::LogLevel::Debug),
            ..StatsigOptions::new()
        })),
    );

    let res = statsig.initialize().await;
    assert!(res.is_err());
    let err = res.unwrap_err();
    assert!(err.to_string().contains("Initialization Error"), "{err}");

    let result = statsig.get_feature_gate(&user, "public_dev_only");

    assert!(result.details.reason == "Loading:Unrecognized");
}

#[tokio::test]
async fn test_timeout_logic() {
    let mock_scrapi = MockScrapi::new().await;
    let network_client = NetworkClient::new("secret_key", None, None);

    // Test for init request
    let init_request_args = RequestArgs {
        url: mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs),
        timeout_ms: 20,
        ..RequestArgs::new()
    };

    mock_scrapi
        .stub(EndpointStub {
            delay_ms: 200, // 200 ms delay
            method: Method::POST,
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;

    let response = network_client.post(init_request_args, None).await;
    // Assert that the request timed out
    assert!(response.is_err());
}
