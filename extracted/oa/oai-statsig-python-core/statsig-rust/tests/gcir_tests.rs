mod utils;

use std::{
    collections::HashSet,
    fs,
    path::PathBuf,
    sync::{Arc, atomic::Ordering},
};

use crate::utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use assert_json_diff::assert_json_eq;
use lazy_static::lazy_static;
use serde_json::{Value, json};
use statsig_rust::{
    ClientInitResponseOptions, EvaluationFixtureClient, EvaluationOperation, EvaluationResult,
    HashAlgorithm, InitializeEvaluationResult, Statsig, StatsigOptions, StatsigUser,
    StatsigUserBuilder,
};

lazy_static! {
    static ref USER: StatsigUser =  StatsigUserBuilder::new_with_user_id("9".to_string())
        .app_version(Some("1.3".into()))
        .user_agent(Some(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1".into(),
        ))
        .ip(Some("1.0.0.0".into()))
        .locale(Some("en_US".into()))
        .build();
}

async fn fixture_from_specs(specs_json: String) -> EvaluationFixtureClient {
    let file = tempfile::NamedTempFile::new().expect("fixture file should be created");
    fs::write(file.path(), specs_json).expect("fixture file should be populated");
    EvaluationFixtureClient::from_file(file.path().to_str().expect("fixture path should be UTF-8"))
        .await
        .expect("fixture client should initialize from its public file boundary")
}

async fn evaluate_fixture_request(
    fixture: &EvaluationFixtureClient,
    operation: EvaluationOperation<'_>,
) -> EvaluationResult {
    fixture
        .evaluate("test-company", (*USER).clone(), None, operation)
        .await
        .expect("fixture-backed SDK operation should evaluate")
}

async fn initialize_fixture_request(
    fixture: &EvaluationFixtureClient,
    options: ClientInitResponseOptions,
    live_overlay: bool,
) -> InitializeEvaluationResult {
    let result = evaluate_fixture_request(
        fixture,
        EvaluationOperation::Initialize {
            options: &options,
            live_overlay,
        },
    )
    .await;
    let EvaluationResult::Initialize { response, .. } = result else {
        panic!("initialize operations must return typed initialize results");
    };
    *response
}

async fn setup(hash_algorithm: HashAlgorithm) -> Value {
    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_data(
        "tests/data/eval_proj_dcs.json",
    )));
    options.event_logging_adapter = Some(Arc::new(MockEventLoggingAdapter::new()));

    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    let response = statsig.get_client_init_response_with_options(
        &USER,
        &ClientInitResponseOptions {
            hash_algorithm: Some(hash_algorithm),
            client_sdk_key: None,
            include_local_overrides: Some(false),
            feature_gate_filter: None,
            experiment_filter: None,
            dynamic_config_filter: None,
            layer_filter: None,
            param_store_filter: None,
            response_format: None,
            remove_id_type: Some(false),
            remove_default_value_gates: Some(false),
            previous_response_hash: None,
            remove_experiments_in_layers: Some(false),
            experiments_in_layers_allowlist: None,
        },
    );
    let json = serde_json::to_string(&response).unwrap();
    serde_json::from_str(&json).unwrap()
}

async fn setup_with_specs_data(specs_data: String, hash_algorithm: HashAlgorithm) -> Value {
    setup_with_specs_data_and_user(specs_data, hash_algorithm, &USER).await
}

async fn setup_with_specs_data_and_user(
    specs_data: String,
    hash_algorithm: HashAlgorithm,
    user: &StatsigUser,
) -> Value {
    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_json_data(specs_data)));
    options.event_logging_adapter = Some(Arc::new(MockEventLoggingAdapter::new()));

    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    let response = statsig.get_client_init_response_with_options(
        user,
        &ClientInitResponseOptions {
            hash_algorithm: Some(hash_algorithm),
            client_sdk_key: None,
            include_local_overrides: Some(false),
            feature_gate_filter: None,
            experiment_filter: None,
            dynamic_config_filter: None,
            layer_filter: None,
            param_store_filter: None,
            response_format: None,
            remove_id_type: Some(false),
            remove_default_value_gates: Some(false),
            previous_response_hash: None,
            remove_experiments_in_layers: Some(false),
            experiments_in_layers_allowlist: None,
        },
    );
    let json = serde_json::to_string(&response).unwrap();
    serde_json::from_str(&json).unwrap()
}

fn eval_proj_dcs_with_new_layer_eval(layer_name: &str) -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");

    json.get_mut("layer_configs")
        .unwrap()
        .get_mut(layer_name)
        .unwrap()
        .as_object_mut()
        .unwrap()
        .insert("useNewLayerEval".to_string(), Value::Bool(true));

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

fn eval_proj_dcs_with_shared_control_layer() -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");

    let rules = json
        .get_mut("layer_configs")
        .unwrap()
        .get_mut("test_layer_in_holdout")
        .unwrap()
        .get_mut("rules")
        .unwrap()
        .as_array_mut()
        .unwrap();

    for rule in rules {
        rule.as_object_mut().unwrap().insert(
            "sharedControlExperiments".to_string(),
            json!([{
                "name": "running_exp_in_layer_with_holdout",
                "controlGroupID": "control_group",
            }]),
        );
    }

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

fn eval_proj_dcs_with_nullable_versions() -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");

    json.get_mut("feature_gates")
        .unwrap()
        .get_mut("test_public")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .remove("version");

    json.get_mut("dynamic_configs")
        .unwrap()
        .get_mut("test_custom_config")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .insert("version".to_string(), Value::Null);

    json.get_mut("layer_configs")
        .unwrap()
        .get_mut("layer_with_many_params")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .remove("version");

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

fn eval_proj_dcs_with_launched_group_marked_experiment_group() -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");

    json.get_mut("dynamic_configs")
        .unwrap()
        .get_mut("test_decision_made")
        .unwrap()
        .get_mut("rules")
        .unwrap()
        .as_array_mut()
        .unwrap()[0]
        .as_object_mut()
        .unwrap()
        .insert("isExperimentGroup".to_string(), json!(true));

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

fn eval_proj_dcs_with_experiment_group_gate() -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");

    let experiment_name = "experiment_group_source";
    let gate_name = "gate_targeted_by_experiment_group";
    let condition_name = "experiment_group_condition";

    let mut experiment = json
        .get("dynamic_configs")
        .unwrap()
        .get("test_experiment_no_targeting")
        .unwrap()
        .clone();
    experiment["salt"] = json!("experiment-group-source-salt");
    experiment["rules"] = json!([{
        "name": "experiment-group-source-treatment",
        "groupName": "Treatment",
        "passPercentage": 100,
        "conditions": ["1828919350"],
        "returnValue": {"variant": "treatment"},
        "id": "experiment-group-source-treatment",
        "salt": "experiment-group-source-treatment",
        "idType": "userID",
        "isExperimentGroup": true
    }]);
    json.get_mut("dynamic_configs")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .insert(experiment_name.to_string(), experiment);

    let mut gate = json
        .get("feature_gates")
        .unwrap()
        .get("test_public")
        .unwrap()
        .clone();
    gate["salt"] = json!("experiment-group-gate-salt");
    gate["rules"][0]["name"] = json!("experiment-group-targeted-rule");
    gate["rules"][0]["id"] = json!("experiment-group-targeted-rule");
    gate["rules"][0]["salt"] = json!("experiment-group-targeted-rule");
    gate["rules"][0]["conditions"] = json!([condition_name]);
    json.get_mut("feature_gates")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .insert(gate_name.to_string(), gate);

    json.get_mut("condition_map")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .insert(
            condition_name.to_string(),
            json!({
                "type": "experiment_group",
                "targetValue": ["Treatment"],
                "operator": "any",
                "field": experiment_name,
                "additionalValues": {"experiment_name": experiment_name},
                "idType": "userID"
            }),
        );

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

fn eval_proj_dcs_with_pipeline_override() -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");

    let synthetic_name = "test_custom_config::pipeline_trigger";
    let mut synthetic_config = json
        .get("dynamic_configs")
        .unwrap()
        .get("test_custom_config")
        .unwrap()
        .clone();
    synthetic_config["defaultValue"] = json!({
        "header_text": "pipeline override"
    });
    synthetic_config["rules"] = json!([]);
    synthetic_config["version"] = json!(999);

    json.get_mut("dynamic_configs")
        .unwrap()
        .as_object_mut()
        .unwrap()
        .insert(synthetic_name.to_string(), synthetic_config);

    json.as_object_mut().unwrap().insert(
        "override_rules".to_string(),
        json!({
            "statsig::everyone": {
                "name": "statsig::everyone",
                "passPercentage": 100,
                "conditions": ["1828919350"],
                "returnValue": true,
                "id": "statsig::everyone",
                "salt": "statsig::everyone",
                "idType": "userID"
            }
        }),
    );
    json.as_object_mut().unwrap().insert(
        "overrides".to_string(),
        json!({
            "test_custom_config": [
                {
                    "new_config_name": synthetic_name,
                    "rules": [
                        {
                            "rule_name": "statsig::everyone",
                            "start_time": 0
                        }
                    ]
                }
            ]
        }),
    );

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

fn eval_proj_dcs_with_default_gate_removal() -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests/data/eval_proj_dcs.json");

    let data = fs::read_to_string(path).expect("Unable to read fixture");
    let mut json: Value = serde_json::from_str(&data).expect("Unable to parse fixture");
    json.as_object_mut().unwrap().insert(
        "gcir_config".to_string(),
        json!({ "remove_default_value_gates": true }),
    );

    serde_json::to_string(&json).expect("Unable to serialize fixture")
}

#[tokio::test]
async fn test_feature_gate_filter() {
    let response_options = ClientInitResponseOptions {
        feature_gate_filter: Some(["test_public".to_string()].into_iter().collect()),
        hash_algorithm: Some(HashAlgorithm::None),
        ..Default::default()
    };

    let json_obj = {
        let mut options = StatsigOptions::new();
        options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_data(
            "tests/data/eval_proj_dcs.json",
        )));
        options.event_logging_adapter = Some(Arc::new(MockEventLoggingAdapter::new()));
        let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
        statsig.initialize().await.unwrap();
        let response = statsig.get_client_init_response_with_options(&USER, &response_options);
        let json = serde_json::to_string(&response).unwrap();
        serde_json::from_str::<Value>(&json).unwrap()
    };

    let gates = json_obj.get("feature_gates").unwrap().as_object().unwrap();
    assert_eq!(gates.len(), 1);
    assert!(gates.contains_key("test_public"));
}

#[tokio::test]
async fn test_project_default_gate_removal_policy_is_used_by_default() {
    let mut statsig_options = StatsigOptions::new();
    statsig_options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_json_data(
        eval_proj_dcs_with_default_gate_removal(),
    )));
    statsig_options.event_logging_adapter = Some(Arc::new(MockEventLoggingAdapter::new()));

    let statsig = Statsig::new("secret-key", Some(Arc::new(statsig_options)));
    statsig.initialize().await.unwrap();

    let filtered = statsig.get_client_init_response_with_options(
        &USER,
        &ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            ..Default::default()
        },
    );
    let unfiltered = statsig.get_client_init_response_with_options(
        &USER,
        &ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            remove_default_value_gates: Some(false),
            ..Default::default()
        },
    );

    let expected_removed = unfiltered
        .feature_gates
        .iter()
        .filter(|(_, gate)| {
            gate.base.rule_id == "default"
                && !gate.value
                && gate.base.secondary_exposures.is_empty()
        })
        .collect::<Vec<_>>();

    assert!(!expected_removed.is_empty());
    assert_eq!(
        filtered.feature_gates.len(),
        unfiltered.feature_gates.len() - expected_removed.len()
    );
    let fixture = fixture_from_specs(eval_proj_dcs_with_default_gate_removal()).await;
    let snapshot_filtered = initialize_fixture_request(
        &fixture,
        ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            ..Default::default()
        },
        false,
    )
    .await
    .response;
    assert_eq!(
        snapshot_filtered.feature_gates.len(),
        filtered.feature_gates.len()
    );
    for (name, _) in expected_removed {
        assert!(!filtered.feature_gates.contains_key(name));
        assert!(!snapshot_filtered.feature_gates.contains_key(name));
    }
}

#[tokio::test]
async fn test_nullable_config_versions() {
    let json_obj =
        setup_with_specs_data(eval_proj_dcs_with_nullable_versions(), HashAlgorithm::None).await;

    let gate = json_obj
        .get("feature_gates")
        .unwrap()
        .get("test_public")
        .unwrap();
    let config = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("test_custom_config")
        .unwrap();
    let layer = json_obj
        .get("layer_configs")
        .unwrap()
        .get("layer_with_many_params")
        .unwrap();

    assert!(gate.get("version").unwrap().is_null());
    assert!(config.get("version").unwrap().is_null());
    assert!(layer.get("version").unwrap().is_null());
}

#[tokio::test]
async fn test_launched_group_is_not_user_in_experiment() {
    let json_obj = setup_with_specs_data(
        eval_proj_dcs_with_launched_group_marked_experiment_group(),
        HashAlgorithm::None,
    )
    .await;

    let experiment = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("test_decision_made")
        .unwrap();

    assert_eq!(experiment.get("rule_id").unwrap(), "launchedGroup");
    assert_eq!(experiment.get("is_user_in_experiment").unwrap(), false);
}

#[tokio::test]
async fn test_experiment_group_gate_is_evaluated_in_client_init_response() {
    let json_obj = setup_with_specs_data(
        eval_proj_dcs_with_experiment_group_gate(),
        HashAlgorithm::None,
    )
    .await;

    let gate = json_obj
        .get("feature_gates")
        .unwrap()
        .get("gate_targeted_by_experiment_group")
        .unwrap();

    assert_eq!(gate.get("value").unwrap(), true);
    assert_eq!(
        gate.get("rule_id").unwrap(),
        "experiment-group-targeted-rule"
    );
}

#[tokio::test]
async fn test_experiment_group_gate_gcir_does_not_log_non_exposed_check() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_json_data(
        eval_proj_dcs_with_experiment_group_gate(),
    )));
    options.event_logging_adapter = Some(logging_adapter.clone());

    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    let response = statsig.get_client_init_response_with_options(
        &USER,
        &ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            ..ClientInitResponseOptions::default()
        },
    );
    assert_eq!(
        serde_json::to_value(response).unwrap()["feature_gates"]["gate_targeted_by_experiment_group"]
            ["value"],
        json!(true)
    );

    statsig.shutdown().await.unwrap();
    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        0
    );
}

#[tokio::test]
async fn test_experiment_group_gate_preserves_nested_experiment_exposure() {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let mut options = StatsigOptions::new();
    options.specs_adapter = Some(Arc::new(MockSpecsAdapter::with_json_data(
        eval_proj_dcs_with_experiment_group_gate(),
    )));
    options.event_logging_adapter = Some(logging_adapter.clone());

    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    assert!(statsig.check_gate(&USER, "gate_targeted_by_experiment_group"));

    statsig.shutdown().await.unwrap();
    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        2
    );
    let nested_experiment_exposure = logging_adapter.force_get_event_at(0);
    assert_eq!(
        nested_experiment_exposure["eventName"],
        "statsig::config_exposure"
    );
    assert_eq!(
        nested_experiment_exposure["metadata"]["config"],
        "experiment_group_source"
    );
    assert_eq!(
        logging_adapter.force_get_event_at(1)["eventName"],
        "statsig::gate_exposure"
    );
}

#[tokio::test]
async fn test_scoped_snapshot_session_evaluates_experiment_group_gate() {
    let fixture = fixture_from_specs(eval_proj_dcs_with_experiment_group_gate()).await;

    let EvaluationResult::Gate(gate) = evaluate_fixture_request(
        &fixture,
        EvaluationOperation::Gate("gate_targeted_by_experiment_group"),
    )
    .await
    else {
        panic!("gate operation should return a gate evaluation");
    };
    assert_eq!(
        gate.rule_id.as_deref(),
        Some("experiment-group-targeted-rule")
    );
    assert!(gate.evaluation.unwrap().value);

    let response = initialize_fixture_request(
        &fixture,
        ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            ..ClientInitResponseOptions::default()
        },
        false,
    )
    .await
    .response;
    let response = serde_json::to_value(response).unwrap();
    assert_eq!(
        response["feature_gates"]["gate_targeted_by_experiment_group"]["value"],
        json!(true)
    );
    assert_eq!(
        response["feature_gates"]["gate_targeted_by_experiment_group"]["rule_id"],
        json!("experiment-group-targeted-rule")
    );
}

#[tokio::test]
async fn test_snapshot_session_references_override_rule_condition_fields() {
    let mut specs: Value = serde_json::from_str(&eval_proj_dcs_with_pipeline_override()).unwrap();
    specs["condition_map"]["override_only_field"] = json!({
        "type": "user_field",
        "targetValue": ["yes"],
        "operator": "any",
        "field": "override_only_field",
        "additionalValues": {},
        "idType": "userID"
    });
    specs["override_rules"]["statsig::everyone"]["conditions"] = json!(["override_only_field"]);

    let fixture = fixture_from_specs(serde_json::to_string(&specs).unwrap()).await;
    let request = fixture
        .prepare_evaluation("test-company", (*USER).clone(), None)
        .await
        .expect("fixture should prepare an authenticated evaluation");
    assert!(
        request.references_any_condition_field(&HashSet::from(["override_only_field".to_string()]))
    );
    let options = ClientInitResponseOptions::default();
    let result = request
        .evaluate(EvaluationOperation::Initialize {
            options: &options,
            live_overlay: false,
        })
        .await
        .expect("override-backed initialize should evaluate");
    assert!(matches!(result, EvaluationResult::Initialize { .. }));
}

#[tokio::test]
async fn test_pipeline_override_specs_are_not_returned_in_initialize() {
    let json_obj =
        setup_with_specs_data(eval_proj_dcs_with_pipeline_override(), HashAlgorithm::None).await;

    let configs = json_obj
        .get("dynamic_configs")
        .unwrap()
        .as_object()
        .unwrap();
    assert!(configs.contains_key("test_custom_config"));
    assert!(!configs.contains_key("test_custom_config::pipeline_trigger"));
    assert_json_eq!(
        configs
            .get("test_custom_config")
            .unwrap()
            .get("value")
            .unwrap(),
        &json!({
            "header_text": "pipeline override"
        })
    );
}

#[tokio::test]
async fn test_public_gate() {
    let json_obj = setup(HashAlgorithm::None).await;

    let gate: &Value = json_obj
        .get("feature_gates")
        .unwrap()
        .get("test_public")
        .unwrap();

    assert_json_eq!(
        gate,
        json!({
            "name": "test_public",
            "version": 70,
            "value": true,
            "rule_id": "6X3qJgyfwA81IJ2dxI7lYp",
            "id_type": "userID",
            "secondary_exposures": []
        })
    );
}

#[tokio::test]
async fn test_public_gate_djb2() {
    let json_obj = setup(HashAlgorithm::Djb2).await;
    let test_public_djb2 = "3968762550";
    let gate: &Value = json_obj
        .get("feature_gates")
        .unwrap()
        .get(test_public_djb2)
        .unwrap();

    assert_json_eq!(
        gate,
        json!({
            "name": test_public_djb2,
            "version": 70,
            "value": true,
            "rule_id": "6X3qJgyfwA81IJ2dxI7lYp",
            "id_type": "userID",
            "secondary_exposures": []
        })
    );
}

#[tokio::test]
async fn test_nested_gate_condition() {
    let json_obj = setup(HashAlgorithm::None).await;

    let gate: &Value = json_obj
        .get("feature_gates")
        .unwrap()
        .get("test_nested_gate_condition")
        .unwrap();

    assert_json_eq!(
        gate,
        json!({
            "name": "test_nested_gate_condition",
            "version": 3,
            "value": true,
            "rule_id": "6MlXHRavmo1ujM1NkZNjhQ",
            "id_type": "userID",
            "secondary_exposures": [
                {
                    "gate": "test_email", // todo: hash these
                    "gateValue": "false",
                    "ruleID": "default"
                },
                {
                    "gate": "test_environment_tier", // todo: hash these
                    "gateValue": "false",
                    "ruleID": "default"
                }
            ]
        })
    );
}

#[tokio::test]
async fn test_targeted_exp_in_layer_with_holdout() {
    let json_obj = setup(HashAlgorithm::None).await;

    let experiment: &Value = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("targeted_exp_in_layer_with_holdout")
        .unwrap();

    assert_json_eq!(
        experiment,
        json!({
            "name": "targeted_exp_in_layer_with_holdout",
            "version": 17,
            "value": {
                "exp_val": "shipped_test",
                "layer_val": "layer_default"
            },
            "rule_id": "layerAssignment",
            "is_device_based": false,
            "id_type": "userID",
            "is_experiment_active": true,
            "is_user_in_experiment": false,
            "is_in_layer": true,
            "explicit_parameters": [
                "exp_val"
            ],
            "secondary_exposures": [
                {
                    "gate": "global_holdout",
                    "gateValue": "false",
                    "ruleID": "3QoA4ncNdVGBaMt3N1KYjz:0.50:1"
                },
                {
                    "gate": "layer_holdout",
                    "gateValue": "false",
                    "ruleID": "2bAVp6R3C85vCYrR6be36n:10.00:5"
                }
            ]
        })
    );
}

#[tokio::test]
async fn test_targeted_exp_in_unlayered_with_holdout() {
    let json_obj = setup(HashAlgorithm::None).await;

    let config: &Value = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("targeted_exp_in_unlayered_with_holdout")
        .unwrap();

    assert_json_eq!(
        config,
        json!({
          "id_type": "userID",
          "is_device_based": false,
          "is_experiment_active": true,
          "is_user_in_experiment": false,
          "name": "targeted_exp_in_unlayered_with_holdout",
          "version": 12,
          "rule_id": "targetingGate",
          "secondary_exposures": [
            {
              "gate": "global_holdout",
              "gateValue": "false",
              "ruleID": "3QoA4ncNdVGBaMt3N1KYjz:0.50:1"
            },
            {
              "gate": "exp_holdout",
              "gateValue": "false",
              "ruleID": "1rEqLOpCROaRafv7ubGgax"
            },
            {
              "gate": "test_50_50",
              "gateValue": "false",
              "ruleID": "6U5gYSQ2jRCDWvfPzKSQY9"
            }
          ],
          "value": {}
        })
    );
}

#[tokio::test]
async fn test_exp_5050_targeting() {
    let json_obj = setup(HashAlgorithm::None).await;

    let experiment: &Value = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("test_exp_5050_targeting")
        .unwrap();

    assert_json_eq!(
        experiment,
        json!({
            "name": "test_exp_5050_targeting",
            "version": 10,
            "value": {},
            "rule_id": "targetingGate",
            "is_device_based": false,
            "id_type": "userID",
            "is_experiment_active": true,
            "is_user_in_experiment": false,
            "secondary_exposures": [
                {
                    "gate": "global_holdout",
                    "gateValue": "false",
                    "ruleID": "3QoA4ncNdVGBaMt3N1KYjz:0.50:1"
                },
                {
                    "gate": "test_50_50",
                    "gateValue": "false",
                    "ruleID": "6U5gYSQ2jRCDWvfPzKSQY9"
                }
            ]
        })
    );
}

#[tokio::test]
async fn test_targetting_with_capital_letter_gate() {
    let json_obj = setup(HashAlgorithm::None).await;

    let experiment: &Value = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("test_targetting_with_capital_letter_gate")
        .unwrap();

    assert_json_eq!(
        experiment,
        json!({
            "name": "test_targetting_with_capital_letter_gate",
            "version": 9,
            "value": {
                "Result": "This is right"
            },
            "rule_id": "74pyYBYPZ5Xly55E6J3lEq",
            "group_name": "Test",
            "is_device_based": false,
            "id_type": "userID",
            "is_experiment_active": true,
            "is_user_in_experiment": true,
            "secondary_exposures": [
                {
                    "gate": "global_holdout",
                    "gateValue": "false",
                    "ruleID": "3QoA4ncNdVGBaMt3N1KYjz:0.50:1"
                },
                {
                    "gate": "test_putting_CAPITAL_letters_in_id",
                    "gateValue": "true",
                    "ruleID": "3Gv6T9YIObRmqZV5nAv0fO"
                }
            ]
        })
    );
}

#[tokio::test]
async fn test_layer_with_many_params() {
    let json_obj = setup(HashAlgorithm::None).await;

    let layer: &Value = json_obj
        .get("layer_configs")
        .unwrap()
        .get("layer_with_many_params")
        .unwrap();

    assert_json_eq!(
        layer,
        json!({
            "name": "layer_with_many_params",
            "version": 19,
            "value": {
                "a_string": "layer",
                "another_string": "layer_default",
                "a_number": 799,
                "a_bool": false,
                "an_object": {
                    "value": "layer_default"
                },
                "an_array": [
                    "layer_default"
                ],
                "another_bool": true,
                "another_number": 0
            },
            "id_type": "userID",
            "rule_id": "default",
            "is_device_based": false,
            "explicit_parameters": [],
            "secondary_exposures": [],
            "undelegated_secondary_exposures": []
        })
    );
}

#[tokio::test]
async fn test_new_layer_eval_preserves_delegated_experiment_metadata() {
    let user = StatsigUser::with_user_id("user-in-test");
    let json_obj = setup_with_specs_data_and_user(
        eval_proj_dcs_with_new_layer_eval("test_layer_in_holdout"),
        HashAlgorithm::None,
        &user,
    )
    .await;

    let layer = json_obj
        .get("layer_configs")
        .unwrap()
        .get("test_layer_in_holdout")
        .unwrap();

    assert_eq!(layer.get("rule_id"), Some(&json!("FC34CQnbBwlkcpMxdi8MT")));
    assert_eq!(layer.get("group_name"), Some(&json!("Test")));
    assert_eq!(layer.get("is_experiment_active"), Some(&json!(true)));
    assert_eq!(layer.get("is_user_in_experiment"), Some(&json!(true)));
    assert_eq!(
        layer.get("allocated_experiment_name"),
        Some(&json!("running_exp_in_layer_with_holdout"))
    );
    assert_eq!(
        layer.get("parameter_rule_ids").unwrap().get("exp_val"),
        Some(&json!("FC34CQnbBwlkcpMxdi8MT"))
    );
    assert_eq!(
        layer
            .get("undelegated_secondary_exposures")
            .unwrap()
            .as_array()
            .unwrap()
            .len(),
        2
    );
}

#[tokio::test]
async fn test_shared_control_experiments_are_not_in_client_initialize_response() {
    let user = StatsigUser::with_user_id("user-in-test");
    let json_obj = setup_with_specs_data_and_user(
        eval_proj_dcs_with_shared_control_layer(),
        HashAlgorithm::None,
        &user,
    )
    .await;

    let layer = json_obj
        .get("layer_configs")
        .unwrap()
        .get("test_layer_in_holdout")
        .unwrap();

    assert!(layer.get("allocated_experiment_name").is_none());
    assert!(layer.get("shared_control_experiments").is_none());
}

#[tokio::test]
async fn test_shared_control_layer_preserves_rule_sampling_rate() {
    let mut specs: Value =
        serde_json::from_str(&eval_proj_dcs_with_shared_control_layer()).unwrap();
    for rule in specs["layer_configs"]["test_layer_in_holdout"]["rules"]
        .as_array_mut()
        .unwrap()
    {
        rule["samplingRate"] = json!(201);
    }

    let options = StatsigOptions {
        specs_adapter: Some(Arc::new(MockSpecsAdapter::with_json_data(
            specs.to_string(),
        ))),
        event_logging_adapter: Some(Arc::new(MockEventLoggingAdapter::new())),
        ..StatsigOptions::default()
    };
    let statsig = Statsig::new("secret-key", Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    let layer = statsig.get_layer(
        &StatsigUser::with_user_id("user-in-test"),
        "test_layer_in_holdout",
    );
    assert_eq!(
        layer
            .__exposure_info
            .as_ref()
            .and_then(|info| info.sampling_rate),
        Some(201)
    );
}

#[tokio::test]
async fn test_layer_with_no_exp() {
    let json_obj = setup(HashAlgorithm::None).await;

    let layer: &Value = json_obj
        .get("layer_configs")
        .unwrap()
        .get("test_layer_with_no_exp")
        .unwrap();

    assert_json_eq!(
        layer,
        json!({
            "name": "test_layer_with_no_exp",
            "version": 2,
            "value": {
                "a_param": "foo"
            },
            "id_type": "userID",
            "rule_id": "default",
            "is_device_based": false,
            "explicit_parameters": [],
            "secondary_exposures": [],
            "undelegated_secondary_exposures": []
        })
    );
}

#[tokio::test]
async fn test_autotune() {
    let json_obj = setup(HashAlgorithm::None).await;

    let experiment: &Value = json_obj
        .get("dynamic_configs")
        .unwrap()
        .get("test_autotune")
        .unwrap();

    assert_json_eq!(
        experiment,
        json!({
            "name": "test_autotune",
            "version": 5,
            "value": {},
            "rule_id": "5380HnrABE4p869fZhtUV9",
            "group_name": "black",
            "is_device_based": false,
            "id_type": "userID",
            "secondary_exposures": []
        })
    );
}
