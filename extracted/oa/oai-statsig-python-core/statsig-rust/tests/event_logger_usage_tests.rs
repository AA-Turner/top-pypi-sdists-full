mod utils;

use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use more_asserts::{assert_gt, assert_lt};
use serde_json::{Map, Value, json};
use statsig_rust::{FeatureGateEvaluationOptions, Statsig, StatsigOptions, StatsigUser};
use std::collections::HashSet;
use std::sync::{Arc, atomic::Ordering};
use utils::mock_event_logging_adapter::MockEventLoggingAdapter;

const DCS_EVAL_PROJ: &str = "eval_proj_dcs";
const DCS_WITH_SAMPLING: &str = "dcs_with_sampling";
const DCS_ANALYTICAL_EXPOSURE_SAMPLING: &str = "dcs_with_analytical_exposure_sampling";
const SEC_EXPO_AS_PRIMARY_FLAG: &str = "sec_expo_as_primary:abc123";

async fn setup(dcs_file: &str) -> (Statsig, Arc<MockEventLoggingAdapter>) {
    setup_with_sdk_configs_and_flags(dcs_file, None, None).await
}

async fn setup_with_json_data(dcs: Value) -> (Statsig, Arc<MockEventLoggingAdapter>) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_json_data(dcs.to_string())));
    options.event_logging_adapter = Some(logging_adapter.clone());

    let uuid = uuid::Uuid::new_v4();
    let statsig = Statsig::new(&format!("secret-{uuid}"), Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    (statsig, logging_adapter)
}

async fn setup_with_sdk_configs_and_flags(
    dcs_file: &str,
    sdk_configs: Option<Map<String, Value>>,
    experimental_flags: Option<HashSet<String>>,
) -> (Statsig, Arc<MockEventLoggingAdapter>) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let dcs_path = format!("tests/data/{dcs_file}.json");
    let specs_adapter = match sdk_configs {
        Some(sdk_configs) => Arc::new(MockSpecsAdapter::with_data_and_sdk_configs(
            &dcs_path,
            sdk_configs,
        )),
        None => Arc::new(MockSpecsAdapter::with_data(&dcs_path)),
    };

    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(specs_adapter);
    options.event_logging_adapter = Some(logging_adapter.clone());
    options.experimental_flags = experimental_flags;

    let uuid = uuid::Uuid::new_v4();
    let statsig = Statsig::new(&format!("secret-{uuid}"), Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    (statsig, logging_adapter)
}

fn nested_sampling_dcs(
    child_entity: &str,
    child_forward_all_exposures: bool,
    explicit_child_value: Option<bool>,
    child_sampling_rate: Option<u64>,
) -> Value {
    let mut child_rules = explicit_child_value
        .map(|value| {
            vec![json!({
                "name": "child_rule",
                "passPercentage": 100,
                "conditions": ["public"],
                "returnValue": value,
                "id": "child_rule",
                "salt": "child_rule",
                "idType": "userID"
            })]
        })
        .unwrap_or_default();
    if let (Some(rule), Some(sampling_rate)) = (child_rules.first_mut(), child_sampling_rate) {
        rule["samplingRate"] = json!(sampling_rate);
    }
    let mut child = json!({
        "type": "feature_gate",
        "salt": "child_salt",
        "enabled": true,
        "defaultValue": false,
        "rules": child_rules,
        "idType": "userID",
        "entity": child_entity,
        "version": 1
    });
    if child_forward_all_exposures {
        child["forwardAllExposures"] = json!(true);
    }

    json!({
        "dynamic_configs": {},
        "feature_gates": {
            "child": child,
            "parent": {
                "type": "feature_gate",
                "salt": "parent_salt",
                "enabled": true,
                "defaultValue": false,
                "rules": [
                    {
                        "name": "child_path",
                        "passPercentage": 100,
                        "conditions": ["pass_child"],
                        "returnValue": true,
                        "id": "child_path",
                        "salt": "child_path",
                        "idType": "userID",
                        "samplingRate": 201
                    },
                    {
                        "name": "fallback_path",
                        "passPercentage": 100,
                        "conditions": ["public"],
                        "returnValue": true,
                        "id": "fallback_path",
                        "salt": "fallback_path",
                        "idType": "userID",
                        "samplingRate": 201
                    }
                ],
                "idType": "userID",
                "entity": "feature_gate",
                "version": 1
            }
        },
        "layer_configs": {},
        "experiment_to_layer": {},
        "has_updates": true,
        "time": 1000,
        "company_id": null,
        "condition_map": {
            "public": {
                "type": "public",
                "targetValue": null,
                "operator": null,
                "field": null,
                "additionalValues": {},
                "idType": "userID"
            },
            "pass_child": {
                "type": "pass_gate",
                "targetValue": "child",
                "operator": null,
                "field": null,
                "additionalValues": {},
                "idType": "userID"
            }
        },
        "sdk_configs": {
            "event_queue_size": 5000,
            "event_logging_interval_seconds": 1,
            "special_case_sampling_rate": 101,
            "sampling_mode": "on"
        }
    })
}

#[tokio::test]
async fn test_gate_exposures() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let _ = statsig.check_gate(&user, "test_public");
    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        1
    );

    let event = logging_adapter.force_get_first_event();
    assert_eq!(event["eventName"], "statsig::gate_exposure");
}

#[tokio::test]
async fn test_dynamic_config_exposures() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let _ = statsig.get_dynamic_config(&user, "test_email_config");
    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        1
    );

    let event = logging_adapter.force_get_first_event();
    assert_eq!(event["eventName"], "statsig::config_exposure");

    let metadata: &serde_json::Map<String, serde_json::Value> =
        event["metadata"].as_object().unwrap();
    assert_eq!(metadata["config"], "test_email_config");
    assert_eq!(metadata["configVersion"], "1");
    assert_eq!(metadata["rulePassed"], "false");
}

#[tokio::test]
async fn test_experiment_exposure() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let _ = statsig.get_experiment(&user, "experiment_with_many_params");
    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        1
    );

    let event = logging_adapter.force_get_first_event();
    assert_eq!(event["eventName"], "statsig::config_exposure");
}

#[tokio::test]
async fn test_layer_exposure() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let layer = statsig.get_layer(&user, "test_layer_with_holdout");
    let _ = layer.get_f64("shared_number_param", 0.0);
    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        1
    );

    let event = logging_adapter.force_get_first_event();
    assert_eq!(event["eventName"], "statsig::layer_exposure");

    let metadata: &serde_json::Map<String, serde_json::Value> =
        event["metadata"].as_object().unwrap();
    assert_eq!(metadata["config"], "test_layer_with_holdout");
    assert_eq!(metadata["configVersion"], "4");

    let sec_expo = event["secondaryExposures"].as_array().unwrap();
    assert_eq!(sec_expo.len(), 1);
    assert_eq!(sec_expo[0]["gate"], "layer_holdout");
}

#[tokio::test]
async fn test_custom_event() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    statsig.log_event(&user, "test_event", None, None);
    statsig.log_event(&user, "test_event", None, None); // verify we don't dedupe
    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        2
    );

    let event = logging_adapter.force_get_event_at(0);
    assert_eq!(event["eventName"], "test_event");

    let event = logging_adapter.force_get_event_at(1);
    assert_eq!(event["eventName"], "test_event");
}

#[tokio::test]
async fn test_non_exposed_checks() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let _ = statsig.check_gate_with_options(
        &user,
        "test_public",
        FeatureGateEvaluationOptions {
            disable_exposure_logging: true,
        },
    );

    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        1
    );

    let event = logging_adapter.force_get_first_event();
    assert_eq!(event["eventName"], "statsig::non_exposed_checks");
}

#[tokio::test]
async fn test_exposure_dedupe() {
    let (statsig, logging_adapter) = setup(DCS_EVAL_PROJ).await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    for _ in 0..10 {
        let _ = statsig.check_gate(&user, "test_public");
    }

    statsig.shutdown().await.unwrap();

    let event_count = logging_adapter
        .no_diagnostics_logged_event_count
        .load(Ordering::SeqCst);
    assert_eq!(event_count, 1);
}

#[tokio::test]
async fn test_rule_sampling() {
    let (statsig, logging_adapter) = setup(DCS_WITH_SAMPLING).await;

    fn get_for_user(statsig: &Statsig, user_id: &str) {
        let user = StatsigUser::with_user_id(user_id);
        let _ = statsig.check_gate(&user, "test_rule_sampling");
    }

    for i in 0..2010 {
        get_for_user(&statsig, &format!("user_{i}"));
    }

    statsig.shutdown().await.unwrap();

    // first expo exists and contains no sampling metadata
    let first_event = logging_adapter.force_get_event_at(0);
    let first_event_metadata = &first_event["statsigMetadata"];
    let first_event_user = &first_event["user"];
    assert_eq!(first_event["eventName"], "statsig::gate_exposure");
    assert_eq!(first_event_metadata.get("samplingMode"), None);
    assert_eq!(first_event_user.get("userID"), Some(&json!("user_0")));

    // second expo contains the expected metadata
    let second_event = logging_adapter.force_get_event_at(1);
    let second_event_metadata = &second_event["statsigMetadata"];
    assert_eq!(second_event["eventName"], "statsig::gate_exposure");
    assert_eq!(
        second_event_metadata.get("samplingMode"),
        Some(&json!("on"))
    );
    assert_eq!(second_event_metadata.get("samplingRate"), Some(&json!(201)));
    assert_eq!(
        second_event_metadata.get("shadowLogged"),
        Some(&json!("logged"))
    );

    let event_count = logging_adapter
        .no_diagnostics_logged_event_count
        .load(Ordering::SeqCst);

    // 2010 exposures. Sampled at 1 in 201. So we expect ~10 events.
    assert_gt!(event_count, 2);
    assert_lt!(event_count, 20);
}

#[tokio::test]
async fn test_analytical_secondary_gate_forces_sampled_parent_exposures() {
    let (statsig, logging_adapter) = setup(DCS_ANALYTICAL_EXPOSURE_SAMPLING).await;

    let user_count = 40;

    for i in 0..user_count {
        let user = StatsigUser::with_user_id(format!("user_{i}"));
        let _ = statsig.check_gate(&user, "parent_gate");
        let _ = statsig.get_dynamic_config(&user, "parent_config");
        let _ = statsig.get_experiment(&user, "parent_experiment");
        let layer = statsig.get_layer(&user, "parent_layer");
        let _ = layer.get_string("param", String::new());
    }

    statsig.shutdown().await.unwrap();

    let event_count = logging_adapter
        .no_diagnostics_logged_event_count
        .load(Ordering::SeqCst);

    assert_eq!(event_count, user_count * 4);
}

#[tokio::test]
async fn test_nested_gate_sampling_preserves_analytical_paths() {
    let cases = [
        ("ordinary_default", "feature_gate", false, None, None, false),
        (
            "forward_all_default",
            "feature_gate",
            true,
            None,
            None,
            true,
        ),
        (
            "two_arm_targeting_fail",
            "holdout",
            false,
            Some(false),
            Some(101),
            false,
        ),
        (
            "three_group_main_default",
            "holdout",
            false,
            None,
            None,
            true,
        ),
        (
            "three_group_third_default",
            "segment",
            false,
            None,
            None,
            true,
        ),
        (
            "three_group_explicit_true",
            "holdout",
            false,
            Some(true),
            None,
            true,
        ),
        (
            "three_group_explicit_false",
            "holdout",
            false,
            Some(false),
            None,
            true,
        ),
    ];

    for (name, entity, forward_all_exposures, explicit_value, child_sampling_rate, should_force) in
        cases
    {
        let (statsig, logging_adapter) = setup_with_json_data(nested_sampling_dcs(
            entity,
            forward_all_exposures,
            explicit_value,
            child_sampling_rate,
        ))
        .await;
        let user_count = if should_force { 40 } else { 2010 };

        for i in 0..user_count {
            let user = StatsigUser::with_user_id(format!("{name}_user_{i}"));
            let _ = statsig.check_gate(&user, "parent");
        }

        statsig.shutdown().await.unwrap();

        let event_count = logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst);
        if should_force {
            assert_eq!(event_count, user_count, "{name}");
            continue;
        }

        let first_event = logging_adapter.force_get_event_at(0);
        assert_eq!(first_event["statsigMetadata"].get("samplingMode"), None);
        assert_eq!(
            first_event["secondaryExposures"],
            json!([
                {
                    "gate": "child",
                    "gateValue": "false",
                    "ruleID": if explicit_value.is_some() {
                        "child_rule"
                    } else {
                        "default"
                    }
                }
            ])
        );

        let sampled_event = logging_adapter.force_get_event_at(1);
        assert_eq!(
            sampled_event["statsigMetadata"]["samplingMode"],
            json!("on")
        );
        assert_eq!(sampled_event["statsigMetadata"]["samplingRate"], json!(201));
        assert_eq!(
            sampled_event["statsigMetadata"]["shadowLogged"],
            json!("logged")
        );
        assert_gt!(event_count, 2, "{name}");
        assert_lt!(event_count, 40, "{name}");
    }
}

#[tokio::test]
async fn test_sec_expo_as_primary_ignores_analytical_gate_force_sampling() {
    let sdk_configs =
        Map::<String, Value>::from_iter([("sec_expo_number".to_string(), json!(1000))]);
    let (statsig, logging_adapter) = setup_with_sdk_configs_and_flags(
        DCS_ANALYTICAL_EXPOSURE_SAMPLING,
        Some(sdk_configs),
        Some(HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()])),
    )
    .await;

    let user_count = 40;

    for i in 0..user_count {
        let user = StatsigUser::with_user_id(format!("user_{i}"));
        let _ = statsig.check_gate(&user, "parent_gate");
        let _ = statsig.get_dynamic_config(&user, "parent_config");
        let _ = statsig.get_experiment(&user, "parent_experiment");
        let layer = statsig.get_layer(&user, "parent_layer");
        let _ = layer.get_string("param", String::new());
    }

    statsig.shutdown().await.unwrap();

    let event_count = logging_adapter
        .no_diagnostics_logged_event_count
        .load(Ordering::SeqCst);

    assert_gt!(event_count, 0);
    assert_lt!(event_count, user_count * 4);

    let payload = logging_adapter.force_get_received_payloads();
    let events = payload.events.as_array().unwrap();
    let analytics_gate_event_count = events
        .iter()
        .filter(|event| {
            event["eventName"] == json!("statsig::gate_exposure")
                && event["metadata"]["gate"] == json!("analytics_gate")
        })
        .count();
    assert_eq!(analytics_gate_event_count, user_count as usize);
}

#[tokio::test]
async fn test_layer_json_exposure_uses_serialized_sampling_info() {
    let (statsig, logging_adapter) = setup(DCS_ANALYTICAL_EXPOSURE_SAMPLING).await;

    let analytic_layer = statsig.get_layer(&StatsigUser::with_user_id("single"), "parent_layer");
    let analytic_layer_json: serde_json::Value =
        serde_json::from_str(&serde_json::to_string(&analytic_layer).unwrap()).unwrap();
    assert_eq!(
        analytic_layer_json["__exposure_info"]["has_seen_analytical_gates"],
        json!(true)
    );

    for i in 0..80 {
        let user = StatsigUser::with_user_id(format!("user_{i}"));
        let layer = statsig.get_layer(&user, "json_sampled_layer");
        let layer_json = serde_json::to_string(&layer).unwrap();

        let layer_value: serde_json::Value = serde_json::from_str(&layer_json).unwrap();
        assert_eq!(layer_value["__exposure_info"]["sampling_rate"], json!(201));

        statsig.log_layer_param_exposure_with_layer_json(layer_json, "param".to_string());
    }

    statsig.shutdown().await.unwrap();

    let event_count = logging_adapter
        .no_diagnostics_logged_event_count
        .load(Ordering::SeqCst);

    assert_lt!(event_count, 20);
}
