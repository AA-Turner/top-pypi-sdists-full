mod utils;

use std::{env, sync::Arc};

use statsig_rust::{Statsig, StatsigOptions};
use utils::helpers::load_contents;
use utils::mock_scrapi::{Endpoint, EndpointStub, MockScrapi, StubData};

fn get_sdk_key() -> String {
    let key = env::var("test_api_key").expect("test_api_key environment variable not set");
    assert!(key.starts_with("secret-9IWf"));
    key
}

#[tokio::test]
async fn test_get_feature_gate_list() {
    let statsig = Statsig::new(&get_sdk_key(), None);
    statsig.initialize().await.unwrap();

    let gate_list = statsig.get_feature_gate_list();

    assert!(!gate_list.is_empty());
    assert!(gate_list.contains(&"test_50_50".to_string()));
}

#[tokio::test]
async fn test_get_dynamic_config_list() {
    let statsig = Statsig::new(&get_sdk_key(), None);
    statsig.initialize().await.unwrap();

    let config_list = statsig.get_dynamic_config_list();

    assert!(!config_list.is_empty());
}

#[tokio::test]
async fn test_get_experiment_list() {
    let statsig = Statsig::new(&get_sdk_key(), None);
    statsig.initialize().await.unwrap();

    let experiment_list = statsig.get_experiment_list();

    assert!(!experiment_list.is_empty());
    assert!(experiment_list.contains(&"running_exp_in_unlayered_with_holdout".to_string()));
}

#[tokio::test]
async fn test_get_parameter_store_list() {
    // Standalone Parameter Store management is deprecated, so use a saved store.
    let server = MockScrapi::new().await;
    server
        .stub(EndpointStub {
            response: StubData::String(load_contents("eval_proj_dcs.json")),
            ..EndpointStub::with_endpoint(Endpoint::DownloadConfigSpecs)
        })
        .await;
    let statsig = Statsig::new(
        "secret-key",
        Some(Arc::new(StatsigOptions {
            disable_all_logging: Some(true),
            specs_url: Some(server.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
            ..Default::default()
        })),
    );
    statsig.initialize().await.unwrap();

    assert_eq!(statsig.get_parameter_store_list(), ["test_parameter_store"]);
}
