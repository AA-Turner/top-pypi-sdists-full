use super::*;
use crate::gcir::gcir_formatter::GCIRHashable;
use crate::interned_values::interned_store::{
    preload_mmap_v2_multi_for_test, write_mmap_v2_for_test,
};
use crate::{GCIRResponseFormat, HashAlgorithm, SpecsUpdate, networking::ResponseData};
use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};

const LAYER: &str = "test-layer";

fn client(reuse: bool) -> Statsig {
    let mut options = StatsigOptions::new();
    if reuse {
        options.experimental_flags = Some(["reuse_default_only_layer_values".to_owned()].into());
    }
    Statsig::new("secret-key", Some(Arc::new(options)))
}

fn rule(id: &str, conditions: &[&str], value: Value) -> Value {
    json!({
        "name": id, "id": id, "groupName": id, "salt": "s", "passPercentage": 100,
        "conditions": conditions, "returnValue": value, "idType": "userID"
    })
}

fn specs(default: Value, rules: Vec<Value>, time: u64) -> Value {
    json!({
        "time": time, "has_updates": true, "dynamic_configs": {}, "id_lists": {}, "experiment_to_layer": {},
        "condition_map": {
            "public": {"type": "public", "idType": "userID"},
            "parent": {"type": "pass_gate", "targetValue": "gate", "idType": "userID"}
        },
        "feature_gates": {"gate": {
            "type": "feature_gate", "salt": "g", "enabled": true, "defaultValue": false,
            "idType": "userID", "entity": "feature_gate", "rules": [rule("gate-rule", &["public"], json!(true))]
        }},
        "layer_configs": {LAYER: {
            "type": "dynamic_config", "salt": "l", "enabled": true, "entity": "layer",
            "defaultValue": default, "useNewLayerEval": true, "idType": "userID", "version": 7, "rules": rules
        }}
    })
}

fn refresh(client: &Statsig, specs: &Value) {
    client
        .spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec_pretty(specs).unwrap()),
            source: SpecsSource::Network,
            received_at: specs["time"].as_u64().unwrap(),
            source_api: None,
            has_updates: None,
        })
        .unwrap();
}

fn evaluate_layer_raw(
    client: &Statsig,
    user: &StatsigUserInternal,
) -> (EvaluationDetails, Option<EvaluatorResult>) {
    client.evaluate_spec(
        user,
        LAYER,
        |details| (details, None),
        |result, details| (details, Some(result)),
        &SpecType::Layer,
        Some(true),
        None,
        false,
    )
}

fn evaluate(client: &Statsig) -> EvaluatorResult {
    let user = StatsigUser::with_user_id("u");
    evaluate_layer_raw(client, &client.internalize_user(&user))
        .1
        .unwrap()
}

fn fields(result: &EvaluatorResult) -> Value {
    json!({"value":result.json_value,"rule":result.rule_id,"group":result.group_name,
        "id_type":result.id_type,"bool":result.bool_value,"delegate":result.config_delegate,
        "active":result.is_experiment_active,"is_experiment_group":result.is_experiment_group,"explicit":result.explicit_parameters,
        "version":result.version,"unsupported":result.unsupported,"shared":result.shared_control_experiments,
        "sampling_rate":result.sampling_rate,"forward_all_exposures":result.forward_all_exposures,"ids":result.parameter_rule_ids,"exposures":result.secondary_exposures,
        "undelegated":result.undelegated_secondary_exposures})
}

fn compare_after_refresh(
    old: &Statsig,
    new: &Statsig,
    specs: &Value,
) -> (EvaluatorResult, EvaluatorResult) {
    refresh(old, specs);
    refresh(new, specs);
    let baseline = evaluate(old);
    let result = evaluate(new);
    assert_eq!(fields(&result), fields(&baseline));
    (baseline, result)
}

fn v2_hashes(client: &Statsig) -> (u64, Vec<u64>) {
    let user = StatsigUser::with_user_id("u");
    let user = client.internalize_user(&user);
    let data = client.spec_store.load_data();
    let options = ClientInitResponseOptions {
        hash_algorithm: Some(HashAlgorithm::None),
        response_format: Some(GCIRResponseFormat::InitializeWithSecondaryExposureMapping),
        previous_response_hash: Some("previous".to_owned()),
        feature_gate_filter: Some(Default::default()),
        ..Default::default()
    };
    let mut context = client.create_gcir_eval_context(&user, &data, &options);
    let response = GCIRFormatter::generate_v2_format(&mut context, &options).unwrap();
    let layer_hash =
        response.layer_configs[LAYER].create_hash(&InternedString::from_str_ref(LAYER));
    assert!(!context.gcir_hashes.is_empty());
    (layer_hash, context.gcir_hashes)
}

#[test]
fn default_layer_reuse_preserves_assignment_and_refreshes_converted_value_keys() {
    let old = client(false);
    let new = client(true);
    let mut previous_hash = None;
    let mut converted = std::collections::HashMap::new();
    // One top-level key gives the legacy assembly a deterministic raw v2 hash.
    for (time, name, nested) in [(1000, "a", 1), (1001, "a", 2), (1002, "b", 2)] {
        let spec = specs(
            json!({name: {"nested": [nested, null]}}),
            vec![rule("empty", &["parent"], json!({}))],
            time,
        );
        let (baseline, result) = compare_after_refresh(&old, &new, &spec);
        let expected = fields(&baseline);
        assert_eq!(expected["ids"], json!({name:"default"}));
        assert!(!result.secondary_exposures.is_empty());
        let value = result.json_value.unwrap();
        let hash = value.get_hash();
        assert_ne!(
            hash,
            baseline.json_value.unwrap().get_hash(),
            "the source and rebuilt raw keys must differ for this v2 parity check"
        );
        let cached = converted
            .entry(hash)
            .or_insert_with(|| value.get_json().unwrap());
        assert_eq!(serde_json::to_value(cached).unwrap(), expected["value"]);
        assert_eq!(evaluate(&new).json_value.unwrap().get_hash(), hash);
        assert_ne!(Some(hash), previous_hash);
        previous_hash = Some(hash);
        assert_eq!(v2_hashes(&old), v2_hashes(&new));
    }
}

#[test]
fn default_layer_reuse_keeps_contributions_and_non_object_fallback() {
    let old = client(false);
    let new = client(true);
    let default = json!({"a":null,"b":[1,2],"c":{"d":3}});
    let winner = vec![
        rule("first", &["public"], json!({"a":null})),
        rule("later", &["parent"], json!({"a":42,"b":[3]})),
    ];
    for (time, defaults, rules, ids) in [
        (
            1000,
            default.clone(),
            vec![],
            json!({"a":"default","b":"default","c":"default"}),
        ),
        (
            1001,
            default,
            winner,
            json!({"a":"first","b":"later","c":"default"}),
        ),
        (1002, json!(true), vec![], json!({})),
        (1003, json!({}), vec![], json!({})),
    ] {
        let spec = specs(defaults, rules, time);
        let (_, result) = compare_after_refresh(&old, &new, &spec);
        assert_eq!(fields(&result)["ids"], ids);
    }
}

#[test]
fn default_layer_reuse_preserves_shared_control_delegate_and_unsupported_results() {
    let old = client(false);
    let new = client(true);
    let check = |spec| fields(&compare_after_refresh(&old, &new, &spec).1);

    let mut experiment = rule("assigned", &["parent"], json!({}));
    experiment["isExperimentGroup"] = json!(true);
    let experiment = json!({
        "type":"dynamic_config", "entity":"experiment", "enabled":true, "isActive":true,
        "idType":"userID", "salt":"e", "defaultValue":{}, "explicitParameters":["a"], "rules":[experiment]
    });

    let mut shared = rule("shared", &["parent"], json!({}));
    shared["sharedControlExperiments"] = json!([{"name":"exp","controlGroupID":"control"}]);
    let later = rule("later", &["public"], json!({"a":42}));
    let mut spec = specs(json!({"a":1}), vec![shared, later], 1000);
    spec["dynamic_configs"]["exp"] = experiment.clone();
    let result = check(spec);
    assert_eq!(result["rule"], "shared");
    assert_eq!(result["shared"][0]["controlGroupID"], "control");
    assert_eq!(result["value"], json!({"a":1}));

    let mut delegate = rule("allocated", &["parent"], json!({}));
    delegate["configDelegate"] = json!("exp");
    let mut spec = specs(json!({"a":1}), vec![delegate], 1001);
    spec["dynamic_configs"]["exp"] = experiment;
    let result = check(spec);
    assert_eq!(result["delegate"], "exp");
    assert_eq!(result["rule"], "assigned");
    assert_eq!(result["is_experiment_group"], true);
    assert_eq!(result["ids"], json!({"a":"default"}));

    let unknown = rule("unsupported", &["unknown"], json!({}));
    let mut spec = specs(json!({"a":1}), vec![unknown], 1002);
    spec["condition_map"]["unknown"] = json!({"type":"unknown-test-type","idType":"userID"});
    assert_eq!(check(spec)["unsupported"], true);
}

rusty_fork_test! {
    #[test]
    fn default_layer_reuse_borrows_archived_defaults_without_materialization() {
        let spec = specs(json!({"a": {"nested": [1, null]}, "b": null}), vec![], 1000);
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("default-layer.mmap");
        write_mmap_v2_for_test(&serde_json::to_vec_pretty(&spec).unwrap(), &path).unwrap();
        preload_mmap_v2_multi_for_test(&[("secret-key", &path)]).unwrap();
        let old = client(false);
        let new = client(true);
        let (_, result) = compare_after_refresh(&old, &new, &spec);
        assert_eq!(fields(&result)["ids"], json!({"a": "default", "b": "default"}));
        let archived = result.json_value.unwrap();
        let rule_ids = result.parameter_rule_ids.unwrap();
        for key in archived.get_json_archived_ref().unwrap().keys() {
            let lookup = InternedString::from_str_ref(key.as_str());
            let (name, _) = rule_ids.get_key_value(&lookup).unwrap();
            assert!(std::ptr::eq(name.as_str(), key.as_str()));
        }

        // A newer default at the same layer version must not reuse the old converted payload.
        let next = specs(json!({"a": {"nested": [2, null]}}), vec![], 1001);
        let (_, result) = compare_after_refresh(&old, &new, &next);
        assert_eq!(fields(&result)["value"], json!({"a": {"nested": [2, null]}}));
        assert_ne!(result.json_value.unwrap().get_hash(), archived.get_hash());
    }
}

#[test]
#[ignore = "manual release-mode performance comparison"]
fn benchmark_default_layer_value_reuse() {
    use std::{hint::black_box, time::Instant};
    // A fixture is an array of {"name": ..., "params": {...}}. Without one, use simple shape controls.
    let fixtures: Vec<Value> = match std::env::var_os("STATSIG_BENCHMARK_LAYER_DEFAULTS") {
        Some(path) => serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap(),
        None => [6, 19, 78]
            .map(|n| {
                let values = (0..n)
                    .map(|i| (format!("parameter_{i}"), json!({"setting":[i,null]})))
                    .collect::<serde_json::Map<_, _>>();
                json!({"name":format!("{n}-parameter synthetic layer"),"params":values})
            })
            .to_vec(),
    };
    let user = StatsigUser::with_user_id("u");
    let measure = |client: &Statsig| {
        let user = client.internalize_user(&user);
        let start = Instant::now();
        for _ in 0..500 {
            black_box(evaluate_layer_raw(client, &user));
        }
        start.elapsed().as_secs_f64() * 1e6 / 500.0
    };
    for fixture in fixtures {
        let defaults = &fixture["params"];
        let keys = defaults.as_object().unwrap();
        let Some(first_key) = keys.keys().next() else {
            continue;
        };
        for (mode, rules) in [
            ("defaults", vec![]),
            ("empty-match", vec![rule("empty", &["parent"], json!({}))]),
            (
                "contributing-match",
                vec![rule("partial", &["parent"], json!({first_key:42}))],
            ),
        ] {
            let data = specs(defaults.clone(), rules, 1000);
            let clients = [client(false), client(true)];
            for client in &clients {
                refresh(client, &data);
                black_box(measure(client));
            }
            let mut results = [vec![], vec![]];
            for round in 0..9 {
                for index in [round % 2, 1 - round % 2] {
                    results[index].push(measure(&clients[index]));
                }
            }
            for result in &mut results {
                result.sort_by(f64::total_cmp);
            }
            println!(
                "layer={} keys={} mode={mode} off_us={:.3} on_us={:.3}",
                fixture["name"],
                keys.len(),
                results[0][4],
                results[1][4]
            );
        }
    }
}
