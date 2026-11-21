mod utils;

use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use lazy_static::lazy_static;
use serde_json::json;
use statsig_rust::{
    Statsig, StatsigOptions, StatsigUser, StatsigUserBuilder, StatsigUserDataMap, dyn_value,
};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;

lazy_static! {
    static ref USER: StatsigUser = StatsigUserBuilder::new_with_custom_ids(HashMap::from([(
        "hubID".to_string(),
        "some-service-123".to_string()
    )]))
    .custom(Some(StatsigUserDataMap::from([
        ("flavor".to_string(), dyn_value!("chocolate")),
        ("region".to_string(), dyn_value!("somewhere")),
        ("service".to_string(), dyn_value!("some-service")),
    ])))
    .build();
}

const SDK_KEY: &str = "secret-key";

#[tokio::test]
async fn missing_condition_reference_returns_false_with_unsupported_reason() {
    let specs = json!({
        "time": 1, "has_updates": true, "dynamic_configs": {}, "layer_configs": {}, "experiment_to_layer": {},
        "feature_gates": {
            "gate": {
                "type": "feature_gate", "entity": "feature_gate", "salt": "gate",
                "enabled": true, "defaultValue": false, "idType": "userID",
                "rules": [{
                    "name": "rule", "id": "rule", "idType": "userID", "passPercentage": 100,
                    "returnValue": true, "conditions": ["eligible", "public", "missing"]
                }]
            }
        },
        "condition_map": {
            "eligible": {"type": "unit_id", "idType": "userID", "operator": "eq", "targetValue": "eligible-user"},
            "public": {"type": "public", "idType": "userID"}
        }
    });
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(MockSpecsAdapter::with_json_data(
                specs.to_string(),
            ))),
            disable_network: Some(true),
            ..StatsigOptions::new()
        })),
    );
    statsig.initialize().await.unwrap();

    for user_id in ["other-user", "eligible-user"] {
        let user = StatsigUser::with_user_id(user_id);
        let gate = statsig.get_feature_gate(&user, "gate");
        assert_eq!(gate.details.reason, "Bootstrap:Unsupported");
        assert_eq!(
            (gate.value, statsig.check_gate(&user, "gate")),
            (false, false),
            "{user_id}"
        );
    }

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn test_many_rule_perf() {
    let user = USER.clone();

    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            environment: Some("staging".to_string()),
            specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
                "tests/data/check_gate_perf_dcs.json",
            ))),
            ..StatsigOptions::new()
        })),
    );
    statsig.initialize().await.unwrap();

    let start = Instant::now();
    let mut result = false;
    for _ in 0..1000 {
        result = statsig.check_gate(&user, "many_rules");
    }

    let duration = start.elapsed();
    println!("many_rules: {:.2} ms", duration.as_secs_f64() * 1000.0);

    let _ = statsig.shutdown().await;

    assert!(result);
}

#[tokio::test]
async fn test_single_rule_env_perf() {
    let user = USER.clone();

    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            environment: Some("development".to_string()),
            specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
                "tests/data/check_gate_perf_dcs.json",
            ))),
            ..StatsigOptions::new()
        })),
    );
    statsig.initialize().await.unwrap();

    let start = Instant::now();
    let mut result = false;
    for _ in 0..1000 {
        result = statsig.check_gate(&user, "public_dev_only");
    }

    let duration = start.elapsed();
    println!("public_dev_only: {:.2} ms", duration.as_secs_f64() * 1000.0);

    let _ = statsig.shutdown().await;

    assert!(result);
}

#[tokio::test]
async fn test_no_gate_perf() {
    let user = USER.clone();

    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            environment: Some("development".to_string()),
            specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
                "tests/data/check_gate_perf_dcs.json",
            ))),
            ..StatsigOptions::new()
        })),
    );
    statsig.initialize().await.unwrap();

    let start = Instant::now();
    let mut result = false;
    for _ in 0..1000 {
        result = statsig.check_gate(&user, "not_a_gate");
    }

    let duration = start.elapsed();
    println!("public_dev_only: {:.2} ms", duration.as_secs_f64() * 1000.0);

    let _ = statsig.shutdown().await;

    assert!(!result);
}
