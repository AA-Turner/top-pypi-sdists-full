mod utils;

use crate::utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use serde_json::{Value, json};
use statsig_rust::{Statsig, StatsigOptions, StatsigUser};
use std::collections::HashMap;
use std::sync::Arc;

async fn setup() -> Statsig {
    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_data(
        "tests/data/big_number_dcs.json",
    )));
    options.event_logging_adapter = Some(Arc::new(MockEventLoggingAdapter::new()));

    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();
    statsig
}

#[tokio::test]
async fn test_dynamic_config_getters() {
    let statsig = setup().await;
    let user = StatsigUser::with_user_id("a_user_id");

    let config = statsig.get_dynamic_config(&user, "big_number");

    let expected = 0.999_999_999_999_999_1;
    assert_eq!(config.get_f64("f64", 111f64), expected);
}

#[tokio::test]
async fn parameter_store_references_preserve_explicit_null() {
    let sdk = setup().await;
    let user = StatsigUser::with_user_id("user");
    let values = HashMap::from([("nullable".to_owned(), Value::Null)]);
    sdk.override_dynamic_config("dynamic_config", values.clone(), None);
    sdk.override_experiment("experiment", values.clone(), None);
    sdk.override_layer("layer", values, None);

    let mut parameters = HashMap::new();
    for (kind, field) in [
        ("dynamic_config", "config_name"),
        ("experiment", "experiment_name"),
        ("layer", "layer_name"),
    ] {
        parameters.insert(
            kind.to_owned(),
            json!({"ref_type": kind, "param_type":"string", field: kind, "param_name":"nullable"}),
        );
    }
    parameters.insert(
        "missing_field".to_owned(),
        json!({"ref_type":"dynamic_config", "param_type":"string", "config_name":"dynamic_config", "param_name":"absent"}),
    );
    sdk.override_parameter_store("store", parameters, Some("user"));
    let store = sdk.get_parameter_store_for_user(&user, "store");
    for name in ["dynamic_config", "experiment", "layer"] {
        assert_eq!(
            store.get_opt::<Value>(&user, name),
            Some(Value::Null),
            "{name}"
        );
        assert_eq!(store.get_opt::<String>(&user, name), None, "{name}");
    }
    assert_eq!(store.get_opt::<Value>(&user, "missing_field"), None);
    assert_eq!(store.get_opt::<Value>(&user, "missing"), None);
    sdk.shutdown().await.unwrap();
}
