mod utils;

use crate::utils::helpers::{enforce_array, enforce_object, enforce_string, enforce_u64};
use crate::utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use assert_json_diff::assert_json_include;
use chrono::Utc;
use serde_json::{Map, Value, json};
#[cfg(feature = "ffi-support")]
use statsig_rust::{BulkEvaluationOptions, statsig_types_raw::PartialLayerRaw};
use statsig_rust::{Statsig, StatsigOptions, StatsigUser, StatsigUserBuilder};
use std::collections::HashSet;
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

const SEC_EXPO_AS_PRIMARY_FLAG: &str = "sec_expo_as_primary:abc123";
const SEC_EXPO_AS_PRIMARY_FLAG_BUCKET: u64 = 307;

#[tokio::test]
async fn test_gate_exposures_initialized() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_public");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let reason = get_reason_from_adapter(&logging_adapter).await;
    assert_eq!(reason, "Bootstrap:Recognized");
}

#[tokio::test]
async fn test_gate_exposures_formatting() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_50_50");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let received = logging_adapter.force_get_received_payloads();

    let statsig_meta = enforce_object(&received.statsig_metadata);
    assert_eq!(statsig_meta["sdkType"], "statsig-server-core");
    assert!(statsig_meta["sdkVersion"].as_str().is_some());

    let exposure = logging_adapter.force_get_first_event();
    assert_eq!(exposure["eventName"], "statsig::gate_exposure");

    let sec_expos = enforce_array(&exposure["secondaryExposures"]);
    let holdout_exposure = enforce_object(&sec_expos[0]);
    assert_eq!(holdout_exposure["gate"], "global_holdout");
    assert_eq!(holdout_exposure["gateValue"], "false");
    assert_eq!(holdout_exposure["ruleID"], "3QoA4ncNdVGBaMt3N1KYjz:0.50:1");
}

#[tokio::test]
async fn shared_control_layer_parameter_logs_layer_and_control_exposures() {
    for use_new_layer_eval in [false, true] {
        assert_shared_control_layer_parameter_exposures(use_new_layer_eval).await;
    }
}

async fn assert_shared_control_layer_parameter_exposures(use_new_layer_eval: bool) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = Arc::new(MockSpecsAdapter::with_json_data(
        json!({
            "feature_gates": {},
            "dynamic_configs": {
                "ranking_experiment": {
                    "type": "dynamic_config",
                    "salt": "experiment_salt",
                    "enabled": true,
                    "defaultValue": {},
                    "rules": [{
                        "name": "Control",
                        "groupName": "Control",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {"ranking_model": "default"},
                        "id": "control_group",
                        "salt": "control_group",
                        "idType": "userID",
                        "isExperimentGroup": true
                    }],
                    "idType": "userID",
                    "entity": "experiment",
                    "isActive": true,
                    "hasSharedParams": true,
                    "explicitParameters": ["ranking_model"]
                },
                "treatment_experiment": {
                    "type": "dynamic_config",
                    "salt": "treatment_experiment_salt",
                    "enabled": true,
                    "defaultValue": {},
                    "rules": [{
                        "name": "Treatment",
                        "groupName": "Treatment",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {"ranking_model": "treatment"},
                        "id": "treatment_group",
                        "idType": "userID",
                        "isExperimentGroup": true
                    }],
                    "idType": "userID",
                    "entity": "experiment",
                    "isActive": true,
                    "hasSharedParams": true,
                    "explicitParameters": ["ranking_model"]
                },
                "untargeted_experiment": {
                    "type": "dynamic_config",
                    "salt": "untargeted_experiment_salt",
                    "enabled": true,
                    "defaultValue": {},
                    "rules": [{
                        "name": "Control",
                        "groupName": "Control",
                        "passPercentage": 100,
                        "conditions": ["only_other_user"],
                        "returnValue": {"ranking_model": "default"},
                        "id": "untargeted_control",
                        "idType": "userID",
                        "isExperimentGroup": true
                    }],
                    "idType": "userID",
                    "entity": "experiment",
                    "isActive": true,
                    "hasSharedParams": true,
                    "explicitParameters": ["ranking_model"]
                },
                "other_parameter_experiment": {
                    "type": "dynamic_config",
                    "salt": "other_parameter_experiment_salt",
                    "enabled": true,
                    "defaultValue": {},
                    "rules": [{
                        "name": "Control",
                        "groupName": "Control",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {"other_parameter": "default"},
                        "id": "other_parameter_control",
                        "idType": "userID",
                        "isExperimentGroup": true
                    }],
                    "idType": "userID",
                    "entity": "experiment",
                    "isActive": true,
                    "hasSharedParams": true,
                    "explicitParameters": ["other_parameter"]
                }
            },
            "layer_configs": {
                "ads_layer": {
                    "type": "layer",
                    "salt": "layer_salt",
                    "enabled": true,
                    "defaultValue": {"ranking_model": "default"},
                    "rules": [{
                        "name": "Shared Control",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {"ranking_model": "cohort_control"},
                        "id": "sharedControl",
                        "idType": "userID",
                        "sharedControlExperiments": [{
                            "name": "ranking_experiment",
                            "controlGroupID": "control_group"
                        }, {
                            "name": "treatment_experiment",
                            "controlGroupID": "treatment_control"
                        }, {
                            "name": "untargeted_experiment",
                            "controlGroupID": "untargeted_control"
                        }, {
                            "name": "other_parameter_experiment",
                            "controlGroupID": "other_parameter_control"
                        }]
                    }, {
                        "name": "Lower-Priority Treatment",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {},
                        "id": "lower_priority_treatment",
                        "idType": "userID",
                        "configDelegate": "ranking_experiment"
                    }],
                    "idType": "userID",
                    "entity": "layer",
                    "useNewLayerEval": use_new_layer_eval
                },
                "holdout_layer": {
                    "type": "layer",
                    "salt": "holdout_layer_salt",
                    "enabled": true,
                    "defaultValue": {"ranking_model": "default"},
                    "rules": [{
                        "name": "Higher-Priority Holdout",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {"ranking_model": "default"},
                        "id": "holdout",
                        "idType": "userID"
                    }, {
                        "name": "Shared Control",
                        "passPercentage": 100,
                        "conditions": [],
                        "returnValue": {},
                        "id": "sharedControl",
                        "idType": "userID",
                        "sharedControlExperiments": [{
                            "name": "ranking_experiment",
                            "controlGroupID": "control_group"
                        }]
                    }],
                    "idType": "userID",
                    "entity": "layer",
                    "useNewLayerEval": use_new_layer_eval
                }
            },
            "conditions": {},
            "experiment_to_layer": {},
            "condition_map": {
                "only_other_user": {
                    "type": "user_field",
                    "targetValue": ["other-user"],
                    "operator": "any",
                    "field": "userID",
                    "idType": "userID"
                }
            },
            "time": 1,
            "has_updates": true,
            "response_format": "dcs-v2"
        })
        .to_string(),
    ));
    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let layer = statsig.get_layer(
        &StatsigUser::with_user_id("shared-control-user"),
        "ads_layer",
    );
    assert_eq!(
        layer.get_string("ranking_model", "fallback".to_string()),
        "cohort_control"
    );

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let mut layer_exposures: Vec<Value> = Vec::new();
    for payload in logging_adapter.logged_payloads.lock().unwrap().iter() {
        for event in enforce_array(&payload.events) {
            if event["eventName"] == "statsig::layer_exposure" {
                layer_exposures.push(event.clone());
            }
        }
    }

    assert_eq!(layer_exposures.len(), 2);
    assert_eq!(layer_exposures[0]["metadata"]["config"], "ads_layer");
    assert_eq!(layer_exposures[0]["metadata"]["ruleID"], "sharedControl");
    assert_eq!(layer_exposures[0]["metadata"]["allocatedExperiment"], "");
    assert_eq!(
        layer_exposures[1]["metadata"]["allocatedExperiment"],
        "ranking_experiment"
    );
    assert_eq!(layer_exposures[1]["metadata"]["ruleID"], "control_group");
    assert_eq!(
        layer_exposures[1]["metadata"]["parameterName"],
        "ranking_model"
    );

    logging_adapter.logged_payloads.lock().unwrap().clear();
    statsig.manually_log_layer_parameter_exposure(
        &StatsigUser::with_user_id("shared-control-user"),
        "ads_layer",
        "ranking_model".to_string(),
    );
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let mut manual_layer_exposures: Vec<Value> = Vec::new();
    for payload in logging_adapter.logged_payloads.lock().unwrap().iter() {
        for event in enforce_array(&payload.events) {
            if event["eventName"] == "statsig::layer_exposure" {
                manual_layer_exposures.push(event.clone());
            }
        }
    }
    assert_eq!(manual_layer_exposures.len(), 2);
    assert_eq!(
        manual_layer_exposures[1]["metadata"]["allocatedExperiment"],
        "ranking_experiment"
    );
    assert_eq!(
        manual_layer_exposures[1]["metadata"]["isManualExposure"],
        "true"
    );

    logging_adapter.logged_payloads.lock().unwrap().clear();
    let holdout_layer = statsig.get_layer(
        &StatsigUser::with_user_id("shared-control-user"),
        "holdout_layer",
    );
    let _ = holdout_layer.get_string("ranking_model", "fallback".to_string());
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let mut holdout_layer_exposures: Vec<Value> = Vec::new();
    for payload in logging_adapter.logged_payloads.lock().unwrap().iter() {
        for event in enforce_array(&payload.events) {
            if event["eventName"] == "statsig::layer_exposure" {
                holdout_layer_exposures.push(event.clone());
            }
        }
    }
    assert_eq!(holdout_layer_exposures.len(), 1);
    assert_eq!(
        holdout_layer_exposures[0]["metadata"]["allocatedExperiment"],
        ""
    );

    #[cfg(feature = "ffi-support")]
    {
        logging_adapter.logged_payloads.lock().unwrap().clear();

        let (_, token) = statsig.use_raw_layer_with_delayed_exposure(
            &StatsigUser::with_user_id("delayed-shared-control-user"),
            "ads_layer",
            Default::default(),
            |_| (),
        );
        let token = token.expect("expected delayed shared-control layer token");
        assert!(statsig.log_delayed_layer_parameter_exposure(&token, "ranking_model"));

        sleep(Duration::from_millis(1)).await;
        statsig.flush_events().await;

        let mut delayed_layer_exposures: Vec<Value> = Vec::new();
        for payload in logging_adapter.logged_payloads.lock().unwrap().iter() {
            for event in enforce_array(&payload.events) {
                if event["eventName"] == "statsig::layer_exposure" {
                    delayed_layer_exposures.push(event.clone());
                }
            }
        }

        assert_eq!(delayed_layer_exposures.len(), 2);
        assert_eq!(
            delayed_layer_exposures[0]["metadata"]["allocatedExperiment"],
            ""
        );
        assert_eq!(
            delayed_layer_exposures[1]["metadata"]["allocatedExperiment"],
            "ranking_experiment"
        );
        assert_eq!(
            delayed_layer_exposures[1]["metadata"]["ruleID"],
            "control_group"
        );

        for use_borrowed_raw in [false, true] {
            logging_adapter.logged_payloads.lock().unwrap().clear();
            let user_id = if use_borrowed_raw {
                "borrowed-raw-shared-control-user"
            } else {
                "owned-raw-shared-control-user"
            };
            let partial_raw = statsig.use_raw_layer_with_options(
                &StatsigUser::with_user_id(user_id),
                "ads_layer",
                Default::default(),
                |raw| PartialLayerRaw::from(raw),
            );
            if use_borrowed_raw {
                statsig.log_layer_param_exposure_from_partial_raw_ref_with_metadata(
                    &partial_raw,
                    "ranking_model".to_string(),
                    None,
                );
            } else {
                statsig.log_layer_param_exposure_from_partial_raw(
                    partial_raw,
                    "ranking_model".to_string(),
                );
            }
            statsig.flush_events().await;

            let raw_layer_exposures = logging_adapter
                .logged_payloads
                .lock()
                .unwrap()
                .iter()
                .flat_map(|payload| enforce_array(&payload.events))
                .filter(|event| event["eventName"] == "statsig::layer_exposure")
                .collect::<Vec<_>>();
            assert_eq!(raw_layer_exposures.len(), 2);
            assert_eq!(
                raw_layer_exposures[1]["metadata"]["allocatedExperiment"],
                "ranking_experiment"
            );
            assert_eq!(
                raw_layer_exposures[1]["metadata"]["ruleID"],
                "control_group"
            );
        }

        statsig.use_raw_layer_with_options(
            &StatsigUser::with_user_id("ordinary-layer-user"),
            "holdout_layer",
            Default::default(),
            |raw| {
                let serialized = serde_json::to_value(raw).unwrap();
                assert!(
                    serialized.get("sharedControlExposures").is_none(),
                    "{serialized}"
                );
            },
        );

        logging_adapter.logged_payloads.lock().unwrap().clear();
        statsig.override_experiment(
            "ranking_experiment",
            std::collections::HashMap::from([("ranking_model".to_string(), json!("overridden"))]),
            None,
        );
        let bulk_result = statsig.bulk_evaluate_with_delayed_exposures(
            &StatsigUser::with_user_id("override-disabled-shared-control-user"),
            BulkEvaluationOptions {
                feature_gate_filter: Some(Vec::new()),
                dynamic_config_filter: Some(Vec::new()),
                experiment_filter: Some(Vec::new()),
                layer_filter: Some(vec!["ads_layer".to_string()]),
                include_local_override: false,
            },
        );
        let token = bulk_result.layer_configs["ads_layer"]
            .common
            .exposure_token
            .as_deref()
            .expect("expected delayed shared-control layer token without overrides");
        assert!(statsig.log_delayed_layer_parameter_exposure(token, "ranking_model"));
        statsig.flush_events().await;

        let override_disabled_exposures = logging_adapter
            .logged_payloads
            .lock()
            .unwrap()
            .iter()
            .flat_map(|payload| enforce_array(&payload.events))
            .filter(|event| event["eventName"] == "statsig::layer_exposure")
            .collect::<Vec<_>>();
        assert_eq!(override_disabled_exposures.len(), 2);
        assert_eq!(
            override_disabled_exposures[1]["metadata"]["ruleID"],
            "control_group"
        );
    }
}

#[tokio::test]
async fn test_gate_exposures_uninitialized() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);

    let _ = statsig.check_gate(&user, "test_public");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let reason = get_reason_from_adapter(&logging_adapter).await;
    assert_eq!(reason, "Uninitialized");
}

#[tokio::test]
async fn test_gate_exposures_unrecognized() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "not_a_gate");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let reason = get_reason_from_adapter(&logging_adapter).await;
    assert_eq!(reason, "Bootstrap:Unrecognized");
}

#[tokio::test]
async fn test_gate_exposures_bad_network() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_trowing_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    let _ = statsig.initialize().await;

    let _ = statsig.check_gate(&user, "not_a_gate");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let reason = get_reason_from_adapter(&logging_adapter).await;
    assert_eq!(reason, "NoValues");
}

#[tokio::test]
async fn test_gate_exposures_not_awaited() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_delayed_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = Arc::new(create_statsig(&specs_adapter, &logging_adapter));

    let shared_statsig = statsig.clone();
    tokio::task::spawn(async move {
        shared_statsig.initialize().await.unwrap();
    });

    sleep(Duration::from_millis(1)).await;

    let _ = statsig.check_gate(&user, "not_a_gate");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let reason = get_reason_from_adapter(&logging_adapter).await;
    assert_eq!(reason, "Loading:Unrecognized");
}

#[tokio::test]
async fn test_check_gate_exposure_with_secondary_exposures() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let event = logging_adapter.force_get_first_event();
    let secondary_expo = enforce_array(&event["secondaryExposures"]);

    let one = enforce_object(&secondary_expo[0]);
    assert_eq!(one["gate"], "test_email");
    assert_eq!(one["ruleID"], "default");
    assert_eq!(one["gateValue"], "false");

    let two = enforce_object(&secondary_expo[1]);
    assert_eq!(two["gate"], "test_environment_tier");
    assert_eq!(two["ruleID"], "default");
    assert_eq!(two["gateValue"], "false");
}

#[tokio::test]
async fn test_get_feature_gate_exposure_with_secondary_exposures() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let _ = statsig.get_feature_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let event = logging_adapter.force_get_first_event();
    let secondary_expo = enforce_array(&event["secondaryExposures"]);

    let one = enforce_object(&secondary_expo[0]);
    assert_eq!(one["gate"], "test_email");
    assert_eq!(one["ruleID"], "default");
    assert_eq!(one["gateValue"], "false");

    let two = enforce_object(&secondary_expo[1]);
    assert_eq!(two["gate"], "test_environment_tier");
    assert_eq!(two["ruleID"], "default");
    assert_eq!(two["gateValue"], "false");
}

#[tokio::test]
async fn test_secondary_exposures_logged_as_primary_when_flag_enabled() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(1000);
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_experimental_flags(
        "secret-shhh-sec-expo-enabled",
        &specs_adapter,
        &logging_adapter,
        HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()]),
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();
    assert_eq!(events.len(), 3);

    for event in &events {
        assert!(enforce_array(&event["secondaryExposures"]).is_empty());
    }

    assert_json_include!(
        actual: events[0],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [],
        })
    );
    assert_json_include!(
        actual: events[1],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_email",
                "gateValue": "false",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        })
    );
    assert_json_include!(
        actual: events[2],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_environment_tier",
                "gateValue": "false",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        })
    );
}

#[tokio::test]
async fn test_gate_dynamic_config_experiment_and_layer_log_secondary_exposures_as_primary() {
    assert_secondary_exposures_logged_as_primary_for_eval(
        "secret-shhh-sec-expo-gate-kind",
        StatsigUser::with_user_id("a_user_id"),
        |statsig, user| {
            let _ = statsig.check_gate(user, "test_nested_gate_condition");
        },
        json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [],
        }),
        vec![
            json!({
                "eventName": "statsig::gate_exposure",
                "metadata": {
                    "gate": "test_email",
                    "gateValue": "false",
                    "ruleID": "default",
                },
                "secondaryExposures": [],
            }),
            json!({
                "eventName": "statsig::gate_exposure",
                "metadata": {
                    "gate": "test_environment_tier",
                    "gateValue": "false",
                    "ruleID": "default",
                },
                "secondaryExposures": [],
            }),
        ],
    )
    .await;

    assert_secondary_exposures_logged_as_primary_for_eval(
        "secret-shhh-sec-expo-config-kind",
        StatsigUser::with_user_id("a_user_id"),
        |statsig, user| {
            let _ = statsig.get_dynamic_config(user, "operating_system_config");
        },
        json!({
            "eventName": "statsig::config_exposure",
            "metadata": {
                "config": "operating_system_config",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        }),
        vec![json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_email",
                "gateValue": "false",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        })],
    )
    .await;

    assert_secondary_exposures_logged_as_primary_for_eval(
        "secret-shhh-sec-expo-experiment-kind",
        StatsigUserBuilder::new_with_user_id("a-user".to_string())
            .email(Some("daniel@statsig.com".to_string()))
            .build(),
        |statsig, user| {
            let _ = statsig.get_experiment(user, "running_exp_in_unlayered_with_holdout");
        },
        json!({
            "eventName": "statsig::config_exposure",
            "metadata": {
                "config": "running_exp_in_unlayered_with_holdout",
                "ruleID": "5suobe8yyvznqasn9Ph1dI",
            },
            "secondaryExposures": [],
        }),
        vec![
            json!({
                "eventName": "statsig::gate_exposure",
                "metadata": {
                    "gate": "global_holdout",
                    "gateValue": "false",
                    "ruleID": "3QoA4ncNdVGBaMt3N1KYjz:0.50:1",
                },
                "secondaryExposures": [],
            }),
            json!({
                "eventName": "statsig::gate_exposure",
                "metadata": {
                    "gate": "exp_holdout",
                    "gateValue": "false",
                    "ruleID": "1rEqLOpCROaRafv7ubGgax",
                },
                "secondaryExposures": [],
            }),
        ],
    )
    .await;

    assert_secondary_exposures_logged_as_primary_for_eval(
        "secret-shhh-sec-expo-layer-kind",
        StatsigUser::with_user_id("a_user_id"),
        |statsig, user| {
            let layer = statsig.get_layer(user, "layer_in_global_holdout");
            let _ = layer.get_string("shared_param", String::new());
        },
        json!({
            "eventName": "statsig::layer_exposure",
            "metadata": {
                "config": "layer_in_global_holdout",
                "parameterName": "shared_param",
            },
            "secondaryExposures": [],
        }),
        vec![json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "global_holdout",
                "gateValue": "false",
                "ruleID": "3QoA4ncNdVGBaMt3N1KYjz:0.50:1",
            },
            "secondaryExposures": [],
        })],
    )
    .await;
}

#[tokio::test]
async fn test_secondary_exposures_remain_on_primary_when_sec_expo_number_is_zero() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(0);
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_experimental_flags(
        "secret-shhh-sec-expo-threshold-off",
        &specs_adapter,
        &logging_adapter,
        HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()]),
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();
    assert_eq!(events.len(), 1);

    assert_json_include!(
        actual: events[0],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [
                {
                    "gate": "test_email",
                    "gateValue": "false",
                    "ruleID": "default",
                },
                {
                    "gate": "test_environment_tier",
                    "gateValue": "false",
                    "ruleID": "default",
                },
            ],
        })
    );
}

#[tokio::test]
async fn test_secondary_exposures_remain_on_primary_when_sec_expo_number_is_missing() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_experimental_flags(
        "secret-shhh-sec-expo-missing-config",
        &specs_adapter,
        &logging_adapter,
        HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()]),
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();
    assert_eq!(events.len(), 1);

    assert_json_include!(
        actual: events[0],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [
                {
                    "gate": "test_email",
                    "gateValue": "false",
                    "ruleID": "default",
                },
                {
                    "gate": "test_environment_tier",
                    "gateValue": "false",
                    "ruleID": "default",
                },
            ],
        })
    );
}

#[tokio::test]
async fn test_secondary_exposures_roll_out_from_zero_to_thousand() {
    assert_sec_expo_rollout_result(0, "secret-shhh-sec-expo-rollout-0", false).await;
    assert_sec_expo_rollout_result(
        SEC_EXPO_AS_PRIMARY_FLAG_BUCKET,
        "secret-shhh-sec-expo-rollout-equal-bucket",
        false,
    )
    .await;
    assert_sec_expo_rollout_result(
        SEC_EXPO_AS_PRIMARY_FLAG_BUCKET + 1,
        "secret-shhh-sec-expo-rollout-after-bucket",
        true,
    )
    .await;
    assert_sec_expo_rollout_result(1000, "secret-shhh-sec-expo-rollout-1000", true).await;
}

#[tokio::test]
async fn test_secondary_exposures_remain_on_primary_when_flag_not_enabled() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(300);
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_sdk_key(
        "secret-shhh-sec-expo-no-flag",
        &specs_adapter,
        &logging_adapter,
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();
    assert_eq!(events.len(), 1);
    assert_eq!(enforce_array(&events[0]["secondaryExposures"]).len(), 2);

    assert_json_include!(
        actual: events[0],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [
                {
                    "gate": "test_email",
                    "gateValue": "false",
                    "ruleID": "default",
                },
                {
                    "gate": "test_environment_tier",
                    "gateValue": "false",
                    "ruleID": "default",
                },
            ],
        })
    );
}

#[tokio::test]
async fn test_secondary_exposures_logged_as_primary_are_deduped() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(1000);
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_experimental_flags(
        "secret-shhh-sec-expo-deduped",
        &specs_adapter,
        &logging_adapter,
        HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()]),
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    let _ = statsig.get_dynamic_config(&user, "operating_system_config");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();
    assert_eq!(events.len(), 4);

    for event in &events {
        assert!(enforce_array(&event["secondaryExposures"]).is_empty());
    }

    assert_json_include!(
        actual: events[0],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [],
        })
    );
    assert_json_include!(
        actual: events[1],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_email",
                "gateValue": "false",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        })
    );
    assert_json_include!(
        actual: events[2],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_environment_tier",
                "gateValue": "false",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        })
    );
    assert_json_include!(
        actual: events[3],
        expected: json!({
            "eventName": "statsig::config_exposure",
            "metadata": {
                "config": "operating_system_config",
                "ruleID": "default",
            },
            "secondaryExposures": [],
        })
    );
}

#[tokio::test]
async fn test_secondary_exposures_on_primary_are_not_deduped_when_flag_not_enabled() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(300);
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_sdk_key(
        "secret-shhh-sec-expo-no-flag-dedupe",
        &specs_adapter,
        &logging_adapter,
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    let _ = statsig.get_dynamic_config(&user, "operating_system_config");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();
    assert_eq!(events.len(), 2);
    assert_eq!(enforce_array(&events[0]["secondaryExposures"]).len(), 2);
    assert_eq!(enforce_array(&events[1]["secondaryExposures"]).len(), 1);

    assert_json_include!(
        actual: events[0],
        expected: json!({
            "eventName": "statsig::gate_exposure",
            "metadata": {
                "gate": "test_nested_gate_condition",
                "gateValue": "true",
                "ruleID": "6MlXHRavmo1ujM1NkZNjhQ",
            },
            "secondaryExposures": [
                {
                    "gate": "test_email",
                    "gateValue": "false",
                    "ruleID": "default",
                },
                {
                    "gate": "test_environment_tier",
                    "gateValue": "false",
                    "ruleID": "default",
                },
            ],
        })
    );
    assert_json_include!(
        actual: events[1],
        expected: json!({
            "eventName": "statsig::config_exposure",
            "metadata": {
                "config": "operating_system_config",
                "ruleID": "default",
            },
            "secondaryExposures": [
                {
                    "gate": "test_email",
                    "gateValue": "false",
                    "ruleID": "default",
                },
            ],
        })
    );
}

#[tokio::test]
async fn test_get_layer_copies_undelegated_exposures() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let layer = statsig.get_layer(&user, "layer_in_global_holdout");
    let _ = layer.get_string("shared_param", String::new());

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let event = logging_adapter.force_get_first_event();
    let secondary_expo = enforce_array(&event["secondaryExposures"]);

    let one = enforce_object(&secondary_expo[0]);
    assert_eq!(one["gate"], "global_holdout");
    assert_eq!(one["ruleID"], "3QoA4ncNdVGBaMt3N1KYjz:0.50:1");
    assert_eq!(one["gateValue"], "false");
}

#[tokio::test]
async fn test_get_layer_with_holdouts() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("user-in-layer-holdout-4");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let layer = statsig.get_layer(&user, "test_layer_in_holdout");
    let _ = layer.get_string("layer_val", String::new());

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let event = logging_adapter.force_get_first_event();
    let secondary_expo = enforce_array(&event["secondaryExposures"]);

    let one = enforce_object(&secondary_expo[0]);
    assert_eq!(one["gate"], "global_holdout");
    assert_eq!(one["ruleID"], "3QoA4ncNdVGBaMt3N1KYjz:0.50:1");
    assert_eq!(one["gateValue"], "false");

    let two = enforce_object(&secondary_expo[1]);
    assert_eq!(two["gate"], "layer_holdout");
    assert_eq!(two["ruleID"], "2bAVp6R3C85vCYrR6be36n:10.00:5");
    assert_eq!(two["gateValue"], "true");
}

#[tokio::test]
async fn test_exposures_with_environment() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("user-in-layer-holdout-4");

    let statsig =
        create_statsig_with_environment(&specs_adapter, &logging_adapter, Some("dev".to_string()));
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_public");
    let _ = statsig.get_dynamic_config(&user, "test_dynamic_config");
    let layer = statsig.get_layer(&user, "test_layer_in_holdout");
    let _ = layer.get_string("layer_val", String::new());

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let events = logging_adapter.force_get_received_payloads();
    let event = enforce_object(&events.events[0]);
    let user = enforce_object(&event["user"]);
    assert_eq!(user["statsigEnvironment"]["tier"], "dev");
}

#[tokio::test]
async fn test_exposure_time() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("user-in-layer-holdout-4");

    let statsig =
        create_statsig_with_environment(&specs_adapter, &logging_adapter, Some("dev".to_string()));
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_public");
    let _ = statsig.get_dynamic_config(&user, "test_email_config");
    let _ = statsig.get_experiment(&user, "test_experiment_no_targeting");
    let _ = statsig
        .get_layer(&user, "layer_with_many_params")
        .get_string("a_string", String::new());

    let was = Utc::now().timestamp_millis() as u64;
    sleep(Duration::from_millis(100)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events = enforce_array(&payload.events);

    let gate_expo = enforce_object(&events[0]);
    assert_eq!(gate_expo["eventName"], "statsig::gate_exposure");
    assert!(enforce_u64(&gate_expo["time"]) <= was);

    let config_expo = enforce_object(&events[1]);
    assert_eq!(config_expo["eventName"], "statsig::config_exposure");
    assert!(enforce_u64(&config_expo["time"]) <= was);

    let experiment_expo = enforce_object(&events[2]);
    assert_eq!(experiment_expo["eventName"], "statsig::config_exposure");
    assert!(enforce_u64(&experiment_expo["time"]) <= was);

    let layer_expo = enforce_object(&events[3]);
    assert_eq!(layer_expo["eventName"], "statsig::layer_exposure");
    assert!(enforce_u64(&layer_expo["time"]) <= was);
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_delayed_gate_exposure_logs_exactly_once() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let (value, token) =
        statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |raw| raw.value);
    assert!(value);
    let token = token.expect("expected delayed exposure token");

    assert!(statsig.log_delayed_exposure(&token));
    assert!(!statsig.log_delayed_exposure(&token));

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let event = logging_adapter.force_get_first_event();
    assert_eq!(event["eventName"], "statsig::gate_exposure");
    assert_eq!(event["metadata"]["gate"], "test_public");
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_bulk_evaluate_returns_typed_response() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let response = statsig.bulk_evaluate_with_delayed_exposures(
        &user,
        BulkEvaluationOptions {
            feature_gate_filter: Some(vec!["test_public".to_string()]),
            dynamic_config_filter: Some(vec!["test_email_config".to_string()]),
            experiment_filter: Some(vec!["test_experiment_no_targeting".to_string()]),
            layer_filter: Some(vec!["layer_with_many_params".to_string()]),
            include_local_override: true,
        },
    );

    let gate = response.feature_gates.get("test_public").unwrap();
    assert!(gate.value);
    assert!(gate.common.exposure_token.is_some());

    let config = response.dynamic_configs.get("test_email_config").unwrap();
    assert_eq!(config.value["header_text"], "everyone else");

    let experiment = response
        .experiments
        .get("test_experiment_no_targeting")
        .unwrap();
    assert!(experiment.common.exposure_token.is_some());

    let layer = response
        .layer_configs
        .get("layer_with_many_params")
        .unwrap();
    assert!(layer.value.contains_key("a_string"));
    assert!(layer.common.exposure_token.is_some());
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_bulk_evaluate_options_can_skip_local_overrides() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();
    statsig.override_gate("test_public", false, None);

    let options = BulkEvaluationOptions {
        feature_gate_filter: Some(vec!["test_public".to_string()]),
        dynamic_config_filter: Some(vec![]),
        experiment_filter: Some(vec![]),
        layer_filter: Some(vec![]),
        include_local_override: true,
    };

    let with_override = statsig.bulk_evaluate_with_delayed_exposures(&user, options.clone());
    let without_override = statsig.bulk_evaluate_with_delayed_exposures(
        &user,
        BulkEvaluationOptions {
            include_local_override: false,
            ..options
        },
    );

    assert!(!with_override.feature_gates["test_public"].value);
    assert!(without_override.feature_gates["test_public"].value);
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_release_delayed_exposure_drops_token() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let (_, token) =
        statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());
    let token = token.expect("expected delayed exposure token");

    assert!(statsig.release_delayed_exposure(&token));
    assert!(!statsig.log_delayed_exposure(&token));

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;
    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(std::sync::atomic::Ordering::SeqCst),
        0
    );
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_deduped_delayed_exposure_returns_no_second_token() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let (_, first) =
        statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());
    let (_, second) =
        statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());

    assert!(first.is_some());
    assert!(second.is_none());
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_delayed_layer_token_logs_distinct_params_once() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let (layer_name, token) = statsig.use_raw_layer_with_delayed_exposure(
        &user,
        "layer_with_many_params",
        Default::default(),
        |raw| raw.name.to_string(),
    );
    assert_eq!(layer_name, "layer_with_many_params");
    let token = token.expect("expected delayed layer exposure token");

    assert!(statsig.log_delayed_layer_parameter_exposure(&token, "a_string"));
    assert!(statsig.log_delayed_layer_parameter_exposure(&token, "a_string"));
    assert!(statsig.log_delayed_layer_parameter_exposure(&token, "another_string"));

    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let layer_events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] == "statsig::layer_exposure")
        .collect();

    assert_eq!(layer_events.len(), 2);

    let params: HashSet<String> = layer_events
        .iter()
        .map(|event| enforce_string(&event["metadata"]["parameterName"]))
        .collect();
    assert_eq!(
        params,
        HashSet::from(["a_string".to_string(), "another_string".to_string()])
    );

    assert!(statsig.release_delayed_exposure(&token));
    assert!(!statsig.log_delayed_layer_parameter_exposure(&token, "a_string"));
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_delayed_exposure_disable_all_logging_returns_no_tokens() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_disable_all_logging(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let (_, gate_token) =
        statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());
    let (_, layer_token) = statsig.use_raw_layer_with_delayed_exposure(
        &user,
        "layer_with_many_params",
        Default::default(),
        |_| (),
    );

    assert!(gate_token.is_none());
    assert!(layer_token.is_none());
}

#[cfg(feature = "ffi-support")]
#[tokio::test]
async fn test_shutdown_clears_delayed_exposure_storage() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter();
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig(&specs_adapter, &logging_adapter);
    statsig.initialize().await.unwrap();

    let (_, token) =
        statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());
    let token = token.expect("expected delayed exposure token");

    statsig.shutdown().await.unwrap();

    assert!(!statsig.log_delayed_exposure(&token));
}

fn create_bootrapped_specs_adapter() -> Arc<MockSpecsAdapter> {
    Arc::new(MockSpecsAdapter::with_data("tests/data/eval_proj_dcs.json"))
}

fn create_bootrapped_specs_adapter_with_sec_expo_number(
    sec_expo_number: u64,
) -> Arc<MockSpecsAdapter> {
    let sdk_configs =
        Map::<String, Value>::from_iter([("sec_expo_number".to_string(), json!(sec_expo_number))]);

    Arc::new(MockSpecsAdapter::with_data_and_sdk_configs(
        "tests/data/eval_proj_dcs.json",
        sdk_configs,
    ))
}

fn create_trowing_specs_adapter() -> Arc<MockSpecsAdapter> {
    Arc::new(MockSpecsAdapter::throwing())
}

fn create_delayed_specs_adapter() -> Arc<MockSpecsAdapter> {
    Arc::new(MockSpecsAdapter::delayed(
        "tests/data/eval_proj_dcs.json",
        100,
    ))
}

fn create_statsig(
    specs_adapter: &Arc<MockSpecsAdapter>,
    logging_adapter: &Arc<MockEventLoggingAdapter>,
) -> Statsig {
    create_statsig_with_sdk_key("secret-shhh", specs_adapter, logging_adapter)
}

fn create_statsig_with_sdk_key(
    sdk_key: &str,
    specs_adapter: &Arc<MockSpecsAdapter>,
    logging_adapter: &Arc<MockEventLoggingAdapter>,
) -> Statsig {
    Statsig::new(
        sdk_key,
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(specs_adapter.clone()),
            event_logging_adapter: Some(logging_adapter.clone()),
            ..StatsigOptions::new()
        })),
    )
}

fn create_statsig_with_environment(
    specs_adapter: &Arc<MockSpecsAdapter>,
    logging_adapter: &Arc<MockEventLoggingAdapter>,
    environment: Option<String>,
) -> Statsig {
    Statsig::new(
        "secret-shhh",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(specs_adapter.clone()),
            event_logging_adapter: Some(logging_adapter.clone()),
            environment,
            ..StatsigOptions::new()
        })),
    )
}

#[cfg(feature = "ffi-support")]
fn create_statsig_with_disable_all_logging(
    specs_adapter: &Arc<MockSpecsAdapter>,
    logging_adapter: &Arc<MockEventLoggingAdapter>,
) -> Statsig {
    Statsig::new(
        "secret-shhh",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(specs_adapter.clone()),
            event_logging_adapter: Some(logging_adapter.clone()),
            disable_all_logging: Some(true),
            ..StatsigOptions::new()
        })),
    )
}

fn create_statsig_with_experimental_flags(
    sdk_key: &str,
    specs_adapter: &Arc<MockSpecsAdapter>,
    logging_adapter: &Arc<MockEventLoggingAdapter>,
    experimental_flags: HashSet<String>,
) -> Statsig {
    Statsig::new(
        sdk_key,
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(specs_adapter.clone()),
            event_logging_adapter: Some(logging_adapter.clone()),
            experimental_flags: Some(experimental_flags),
            ..StatsigOptions::new()
        })),
    )
}

async fn assert_sec_expo_rollout_result(
    sec_expo_number: u64,
    sdk_key: &str,
    should_log_as_primary: bool,
) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(sec_expo_number);
    let user = StatsigUser::with_user_id("a_user_id");

    let statsig = create_statsig_with_experimental_flags(
        sdk_key,
        &specs_adapter,
        &logging_adapter,
        HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()]),
    );
    statsig.initialize().await.unwrap();

    let _ = statsig.check_gate(&user, "test_nested_gate_condition");
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<_> = enforce_array(&payload.events)
        .into_iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .collect();

    if should_log_as_primary {
        assert_eq!(events.len(), 3);
        for event in &events {
            assert!(enforce_array(&event["secondaryExposures"]).is_empty());
        }
    } else {
        assert_eq!(events.len(), 1);
        assert_eq!(enforce_array(&events[0]["secondaryExposures"]).len(), 2);
    }
}

async fn assert_secondary_exposures_logged_as_primary_for_eval(
    sdk_key: &str,
    user: StatsigUser,
    evaluate: impl FnOnce(&Statsig, &StatsigUser),
    expected_primary_event: Value,
    expected_secondary_events: Vec<Value>,
) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let specs_adapter = create_bootrapped_specs_adapter_with_sec_expo_number(1000);

    let statsig = create_statsig_with_experimental_flags(
        sdk_key,
        &specs_adapter,
        &logging_adapter,
        HashSet::from([SEC_EXPO_AS_PRIMARY_FLAG.to_string()]),
    );
    statsig.initialize().await.unwrap();

    evaluate(&statsig, &user);
    sleep(Duration::from_millis(1)).await;
    statsig.flush_events().await;

    let payload = logging_adapter.force_get_received_payloads();
    let events: Vec<Value> = enforce_array(&payload.events)
        .iter()
        .filter(|event| event["eventName"] != "statsig::diagnostics")
        .cloned()
        .collect();

    assert_eq!(events.len(), 1 + expected_secondary_events.len());

    for event in &events {
        assert!(enforce_array(&event["secondaryExposures"]).is_empty());
    }

    assert_json_include!(
        actual: events[0],
        expected: expected_primary_event,
    );

    for (event, expected) in events.iter().skip(1).zip(expected_secondary_events) {
        assert_json_include!(
            actual: event,
            expected: expected,
        );
    }
}

async fn get_reason_from_adapter(logging_adapter: &MockEventLoggingAdapter) -> String {
    let event = logging_adapter.force_get_first_event();
    let metadata = enforce_object(&event["metadata"]);

    enforce_string(&metadata["reason"])
}
