mod utils;

use serde_json::{Value, json};
use statsig_rust::{
    ExperimentEvaluationOptions, FeatureGateEvaluationOptions, Statsig,
    StatsigLocalOverrideAdapter, StatsigOptions, StatsigUser, sdk_event_emitter::SdkEvent,
    statsig_types::Experiment,
};
use std::sync::{Arc, Mutex};
use utils::{
    mock_event_logging_adapter::MockEventLoggingAdapter, mock_specs_adapter::MockSpecsAdapter,
};

const SOURCE: &str = "nested_reporting_source";
const INNER: &str = "nested_reporting_inner";
const GATE: &str = "nested_reporting_gate";

#[derive(Debug, Clone, PartialEq)]
struct ExperimentEvent {
    name: String,
    reason: String,
    rule_id: Option<String>,
    value_hash: Option<u64>,
    value: Option<Value>,
    group_name: Option<String>,
}

impl ExperimentEvent {
    fn from_event(event: SdkEvent<'_>) -> Option<Self> {
        let SdkEvent::ExperimentEvaluated {
            experiment_name,
            reason,
            rule_id,
            value,
            group_name,
        } = event
        else {
            return None;
        };
        Some(Self {
            name: experiment_name.to_string(),
            reason: reason.to_string(),
            rule_id: rule_id.map(str::to_string),
            value_hash: value.map(|value| value.get_hash()),
            // A listener may still request JSON; the SDK should not decode a
            // second, unused public Experiment.value before invoking it.
            value: value.map(|value| serde_json::to_value(value.get_json()).unwrap()),
            group_name: group_name.map(str::to_string),
        })
    }

    fn from_experiment(experiment: &Experiment) -> Self {
        Self {
            name: experiment.name.clone(),
            reason: experiment.details.reason.clone(),
            rule_id: Some(experiment.rule_id.clone()),
            value_hash: experiment
                .__evaluation
                .as_ref()
                .map(|evaluation| evaluation.value.get_hash()),
            value: experiment
                .__evaluation
                .as_ref()
                .map(|_| serde_json::to_value(&experiment.value).unwrap()),
            group_name: experiment.group_name.clone(),
        }
    }
}

#[derive(Debug, Clone, Copy)]
enum Scenario {
    Treatment,
    Default,
    Unrecognized,
    ValueOverride,
    GroupOverride,
    Nested,
}

fn specs(scenario: Scenario) -> String {
    let mut specs: Value = serde_json::from_str(include_str!("data/eval_proj_dcs.json")).unwrap();
    let mut experiment = specs["dynamic_configs"]["test_experiment_no_targeting"].clone();
    experiment["salt"] = json!(SOURCE);
    experiment["defaultValue"] = json!({"default": [null, {"text": "默认", "enabled": false}]});
    experiment["rules"] = json!([{
        "name": "nested-reporting-treatment",
        "id": "nested-reporting-treatment",
        "salt": "nested-reporting-treatment",
        "idType": "userID",
        "groupName": "Treatment",
        "passPercentage": 100,
        "conditions": ["1828919350"],
        "returnValue": {"variant": "treatment", "nested": [1, null, {"text": "✓"}]},
        "isExperimentGroup": true
    }]);
    if matches!(scenario, Scenario::Default) {
        experiment["rules"] = json!([]);
    }
    if matches!(scenario, Scenario::Nested) {
        specs["dynamic_configs"][INNER] = experiment.clone();
        specs["condition_map"]["inner-experiment-group"] = json!({
            "type": "experiment_group", "field": INNER,
            "targetValue": ["Treatment"], "operator": "any", "idType": "userID"
        });
        experiment["rules"][0]["conditions"] = json!(["inner-experiment-group"]);
    }
    if !matches!(scenario, Scenario::Unrecognized) {
        specs["dynamic_configs"][SOURCE] = experiment;
    }
    let mut gate = specs["feature_gates"]["test_public"].clone();
    gate["rules"][0]["conditions"] = json!(["source-experiment-group"]);
    specs["feature_gates"][GATE] = gate;
    specs["condition_map"]["source-experiment-group"] = json!({
        "type": "experiment_group", "field": SOURCE,
        "targetValue": ["Treatment"], "operator": "any", "idType": "userID"
    });
    specs.to_string()
}

async fn setup(scenario: Scenario) -> (Statsig, Arc<MockEventLoggingAdapter>) {
    let logging = Arc::new(MockEventLoggingAdapter::new_with_background_flush(false));
    let options = StatsigOptions {
        specs_adapter: Some(Arc::new(MockSpecsAdapter::with_json_data(specs(scenario)))),
        event_logging_adapter: Some(logging.clone()),
        override_adapter: Some(Arc::new(StatsigLocalOverrideAdapter::new())),
        disable_network: Some(true),
        ..StatsigOptions::default()
    };
    let statsig = Statsig::new("secret-nested-reporting", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();
    match scenario {
        Scenario::ValueOverride => statsig.override_experiment(
            SOURCE,
            serde_json::from_value(json!({"override": [true, "✓", 42]})).unwrap(),
            None,
        ),
        Scenario::GroupOverride => {
            statsig.override_experiment_by_group_name(SOURCE, "Treatment", None)
        }
        _ => {}
    }
    (statsig, logging)
}

#[tokio::test]
async fn nested_reporting_preserves_public_experiment_callback_fields() {
    let user = StatsigUser::with_user_id("reporting-user".to_string());
    for scenario in [
        Scenario::Treatment,
        Scenario::Default,
        Scenario::Unrecognized,
        Scenario::ValueOverride,
        Scenario::GroupOverride,
    ] {
        let (statsig, _) = setup(scenario).await;
        let events = Arc::new(Mutex::new(Vec::new()));
        let observed = events.clone();
        statsig.subscribe(SdkEvent::EXPERIMENT_EVALUATED, move |event| {
            observed
                .lock()
                .unwrap()
                .push(ExperimentEvent::from_event(event).unwrap());
        });
        statsig.get_feature_gate_with_options(
            &user,
            GATE,
            FeatureGateEvaluationOptions {
                disable_exposure_logging: true,
            },
        );
        let nested = events.lock().unwrap().clone();
        assert_eq!(nested.len(), 1, "{scenario:?}");

        // Nested unrecognized experiments historically report no evaluation,
        // unlike the public getter's empty, unrecognized evaluation object.
        if matches!(scenario, Scenario::Unrecognized) {
            assert_eq!(
                nested[0],
                ExperimentEvent {
                    name: SOURCE.to_string(),
                    reason: "Bootstrap:Unrecognized".to_string(),
                    rule_id: Some("default".to_string()),
                    value_hash: None,
                    value: None,
                    group_name: None,
                }
            );
            statsig.shutdown().await.unwrap();
            continue;
        }

        let direct = statsig.get_experiment_with_options(
            &user,
            SOURCE,
            ExperimentEvaluationOptions {
                disable_exposure_logging: true,
                ..ExperimentEvaluationOptions::default()
            },
        );
        assert_eq!(
            nested[0],
            ExperimentEvent::from_experiment(&direct),
            "{scenario:?}"
        );
        assert_eq!(events.lock().unwrap()[1], nested[0], "{scenario:?}");
        statsig.shutdown().await.unwrap();
    }
}

#[tokio::test]
async fn nested_reporting_preserves_callback_order_and_exposure_accounting() {
    let user = StatsigUser::with_user_id("reporting-user".to_string());
    for with_listeners in [false, true] {
        for disable_exposure_logging in [false, true] {
            let (statsig, logging) = setup(Scenario::Nested).await;
            let callbacks = Arc::new(Mutex::new(Vec::new()));
            if with_listeners {
                for (kind, internal) in [("public", false), ("internal", true)] {
                    let observed = callbacks.clone();
                    let record = move |event: SdkEvent<'_>| {
                        let name = match event {
                            SdkEvent::ExperimentEvaluated {
                                experiment_name, ..
                            } => experiment_name,
                            SdkEvent::GateEvaluated { gate_name, .. } => gate_name,
                            _ => return,
                        };
                        observed.lock().unwrap().push((kind, name.to_string()));
                    };
                    if internal {
                        statsig.subscribe_internal(SdkEvent::ALL, move |event| {
                            record(event);
                            true
                        });
                    } else {
                        statsig.subscribe(SdkEvent::ALL, record);
                    }
                }
            }
            for _ in 0..2 {
                assert!(
                    statsig
                        .get_feature_gate_with_options(
                            &user,
                            GATE,
                            FeatureGateEvaluationOptions {
                                disable_exposure_logging
                            },
                        )
                        .value
                );
            }
            if with_listeners {
                let expected: Vec<_> = [INNER, SOURCE, GATE, INNER, SOURCE, GATE]
                    .into_iter()
                    .flat_map(|name| [("public", name.to_string()), ("internal", name.to_string())])
                    .collect();
                assert_eq!(*callbacks.lock().unwrap(), expected);
            }
            statsig.flush_events().await;
            let events: Vec<_> = logging
                .logged_payloads
                .lock()
                .unwrap()
                .iter()
                .flat_map(|payload| payload.events.as_array().unwrap().clone())
                .collect();
            assert!(
                !events
                    .iter()
                    .any(|event| event["eventName"] == "statsig::config_exposure")
            );
            if disable_exposure_logging {
                let counts = events
                    .iter()
                    .find(|event| event["eventName"] == "statsig::non_exposed_checks")
                    .unwrap();
                let checks: Value =
                    serde_json::from_str(counts["metadata"]["checks"].as_str().unwrap()).unwrap();
                assert_eq!(checks, json!({INNER: 2, SOURCE: 2, GATE: 2}));
            } else {
                assert_eq!(
                    events
                        .iter()
                        .filter(|event| event["eventName"] == "statsig::gate_exposure")
                        .count(),
                    1
                );
            }
            statsig.shutdown().await.unwrap();
        }
    }
}
