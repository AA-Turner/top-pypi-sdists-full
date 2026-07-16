mod utils;

use crate::utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use assert_json_diff::assert_json_eq;
use serde_json::json;
use statsig_rust::{Statsig, StatsigOptions, StatsigUser};
use std::sync::Arc;

async fn setup(
    options_overrides: Option<StatsigOptions>,
) -> (Statsig, Arc<MockEventLoggingAdapter>) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());

    let options = StatsigOptions {
        specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
            "tests/data/dcs_missing_gates.json",
        ))),
        event_logging_adapter: Some(logging_adapter.clone()),
        ..options_overrides.unwrap_or_default()
    };

    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();
    (statsig, logging_adapter)
}

#[tokio::test]
async fn test_fail_gate_passes_when_target_gate_does_not_exist() {
    let (statsig, logging_adapter) = setup(None).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let fail_gate = statsig.check_gate(&user, "test_fail_gate_not_found");

    assert!(fail_gate);

    statsig.shutdown().await.unwrap();

    assert_json_eq!(
        json!(&logging_adapter.force_get_first_event()["secondaryExposures"]),
        json!([])
    );
}

#[tokio::test]
async fn test_fail_gate_passes_when_target_gate_name_is_empty() {
    let (statsig, logging_adapter) = setup(None).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let fail_gate = statsig.check_gate(&user, "test_fail_gate_not_set");

    assert!(fail_gate);

    statsig.shutdown().await.unwrap();

    assert_json_eq!(
        json!(&logging_adapter.force_get_first_event()["secondaryExposures"]),
        json!([])
    );
}

#[tokio::test]
async fn test_pass_gate_passes_when_target_gate_does_not_exist() {
    let (statsig, logging_adapter) = setup(None).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let pass_gate = statsig.check_gate(&user, "test_pass_gate_not_found");

    assert!(!pass_gate);

    statsig.shutdown().await.unwrap();

    assert_json_eq!(
        json!(&logging_adapter.force_get_first_event()["secondaryExposures"]),
        json!([])
    );
}

#[tokio::test]
async fn test_pass_gate_passes_when_target_gate_name_is_empty() {
    let (statsig, logging_adapter) = setup(None).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let pass_gate = statsig.check_gate(&user, "test_pass_gate_not_set");

    assert!(!pass_gate);

    statsig.shutdown().await.unwrap();

    assert_json_eq!(
        json!(&logging_adapter.force_get_first_event()["secondaryExposures"]),
        json!([])
    );
}

#[tokio::test]
async fn test_dangling_segment_preserves_layer_holdout_exposure() {
    let (statsig, logging_adapter) = setup(None).await;

    let holdout_layer = statsig.get_layer(
        &StatsigUser::with_user_id("holdout-user".to_string()),
        "test_layer",
    );
    assert_eq!(
        holdout_layer.get_string("variant", "missing".to_string()),
        "generic"
    );

    let no_holdout_layer = statsig.get_layer(
        &StatsigUser::with_user_id("no-holdout-user".to_string()),
        "test_layer",
    );
    assert_eq!(
        no_holdout_layer.get_string("variant", "missing".to_string()),
        "test"
    );

    statsig.shutdown().await.unwrap();

    let holdout_event = logging_adapter.force_get_event_at(0);
    assert_eq!(holdout_event["metadata"]["ruleID"], "holdout-id");
    assert_json_eq!(
        json!(&holdout_event["secondaryExposures"]),
        json!([{
            "gate": "test_holdout",
            "gateValue": "true",
            "ruleID": "holdout-rule"
        }])
    );

    let no_holdout_event = logging_adapter.force_get_event_at(1);
    assert_eq!(
        no_holdout_event["metadata"]["allocatedExperiment"],
        "child_experiment"
    );
    assert_json_eq!(
        json!(&no_holdout_event["secondaryExposures"]),
        json!([{
            "gate": "test_holdout",
            "gateValue": "false",
            "ruleID": "default"
        }])
    );
}
