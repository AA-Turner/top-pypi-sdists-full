mod utils;
use std::sync::Arc;
use utils::{
    mock_scrapi::{Endpoint, EndpointStub, Method, MockScrapi, StubData},
    mock_specs_adapter::MockSpecsAdapter,
};

use statsig_rust::{
    Statsig, StatsigOptions, StatsigUser,
    networking::{NetworkClient, RequestArgs},
};

const SDK_KEY: &str = "secret-key";

#[tokio::test]
async fn test_initialize_without_timeout_can_exceed_three_seconds() {
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(MockSpecsAdapter::delayed(
                "tests/data/eval_proj_dcs.json",
                3200,
            ))),
            disable_all_logging: Some(true),
            disable_country_lookup: Some(true),
            ..StatsigOptions::new()
        })),
    );

    let details = tokio::time::timeout(
        std::time::Duration::from_secs(10),
        statsig.initialize_with_details(),
    )
    .await
    .expect("initialization must finish")
    .unwrap();
    assert!(details.init_success, "{details:?}");
    assert!(statsig.is_config_spec_ready());
    statsig.shutdown().await.unwrap();
}

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

#[tokio::test]
async fn test_default_initial_http_request_can_exceed_three_seconds() {
    let mock_scrapi = MockScrapi::new().await;
    mock_scrapi
        .stub(EndpointStub {
            delay_ms: 3_200,
            response: StubData::String(
                std::fs::read_to_string("tests/data/eval_proj_dcs.json").unwrap(),
            ),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            disable_all_logging: Some(true),
            disable_country_lookup: Some(true),
            ..StatsigOptions::new()
        })),
    );

    let details = tokio::time::timeout(
        std::time::Duration::from_secs(10),
        statsig.initialize_with_details(),
    )
    .await
    .expect("initial HTTP response must finish within its request budget")
    .unwrap();
    assert!(details.init_success, "{details:?}");
    assert!(statsig.is_config_spec_ready());
    assert_eq!(
        mock_scrapi
            .get_requests_for_endpoint(Endpoint::DownloadConfigSpecs)
            .len(),
        1
    );
    statsig.shutdown().await.unwrap();
}
