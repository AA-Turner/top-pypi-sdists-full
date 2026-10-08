use std::{collections::HashMap, io::Cursor};

use prost::Message;
use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};

use crate::{
    DynamicValue, StatsigUser,
    evaluation::{
        comparisons::{compare_case_sensitive_strings_in_array, compare_strings_in_array},
        evaluator::{Evaluator, Recognition, SpecType},
        evaluator_context::{EvaluatorContext, IdListResolution},
        evaluator_value::{EvaluatorValue, EvaluatorValueInner, EvaluatorValueRef},
    },
    hashing::HashUtil,
    interned_string::InternedString,
    interned_values::{
        InternedStore,
        interned_store::{preload_mmap_v2_for_test, write_mmap_v2_for_test},
    },
    observability::ops_stats::OpsStatsForInstance,
    specs_response::{
        proto_specs::deserialize_protobuf_from_reader,
        spec_types::{Condition, ConditionOperator, SpecsResponseFull},
        statsig_config_specs as pb,
    },
    user::{
        StatsigUserInternal,
        fast_statsig_user::{FastStatsigUser, FastUserData},
        user_value::{UserValue, UserValueRef},
    },
};

fn condition_json(operator: &str, target: &Value) -> Value {
    json!({
        "type": "user_field",
        "field": "userID",
        "operator": operator,
        "targetValue": target,
        "idType": "userID",
        "additionalValues": {}
    })
}

fn parsed_condition<'a>(specs: &'a SpecsResponseFull, name: &str) -> &'a Condition {
    specs
        .condition_map
        .get(&InternedString::from_str_ref(name))
        .unwrap()
}

fn json_condition(operator: &str, target: &Value) -> Condition {
    // The target precedes the operator on the wire. Parsing it eagerly would
    // irreversibly merge different spellings before the key mode is known.
    serde_json::from_str(&format!(
        r#"{{"targetValue":{target},"operator":"{operator}","type":"user_field","field":"userID","idType":"userID","additionalValues":{{}}}}"#
    ))
    .unwrap()
}

fn protobuf_conditions(conditions: &[(&str, Value)]) -> SpecsResponseFull {
    let mut frames = Vec::new();
    pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::TopLevel as i32,
        data: Some(
            pb::SpecsTopLevel {
                has_updates: true,
                time: 1,
                rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                ..Default::default()
            }
            .encode_to_vec(),
        ),
        ..Default::default()
    }
    .encode_length_delimited(&mut frames)
    .unwrap();
    for (index, (operator, target)) in conditions.iter().enumerate() {
        let operator = match *operator {
            "any" => pb::Operator::Any,
            "none" => pb::Operator::None,
            "any_case_sensitive" => pb::Operator::AnyCaseSensitive,
            "none_case_sensitive" => pb::Operator::NoneCaseSensitive,
            _ => unreachable!(),
        };
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Condition as i32,
            name: index.to_string(),
            data: Some(
                pb::Condition {
                    condition_type: pb::ConditionType::UserField as i32,
                    field: Some("userID".into()),
                    operator: Some(operator as i32),
                    target_value: Some(pb::AnyValue {
                        value: Some(pb::any_value::Value::RawValue(
                            serde_json::to_vec(target).unwrap(),
                        )),
                    }),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        }
        .encode_length_delimited(&mut frames)
        .unwrap();
    }
    pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Done as i32,
        ..Default::default()
    }
    .encode_length_delimited(&mut frames)
    .unwrap();
    let mut specs = SpecsResponseFull::default();
    deserialize_protobuf_from_reader(
        &OpsStatsForInstance::new(),
        &SpecsResponseFull::default(),
        &mut specs,
        &mut Cursor::new(frames),
    )
    .unwrap();
    assert_eq!(specs.condition_map.len(), conditions.len());
    specs
}

fn target_with_fillers(first: &str, second: &str, len: usize) -> Value {
    let mut target = vec![json!(first), json!(second)];
    target.extend((2..len).map(|index| json!(format!("exact-target-filler-{index}"))));
    Value::Array(target)
}

fn assert_exact_membership(
    target: EvaluatorValueRef<'_>,
    input: Option<Value>,
    expected_hit: bool,
) {
    let dynamic = input
        .clone()
        .map(DynamicValue::from_json_value)
        .unwrap_or_default();
    let eager = input
        .clone()
        .map(UserValue::from_json_value)
        .unwrap_or_default();
    for value in [UserValueRef::Dynamic(&dynamic), UserValueRef::User(&eager)] {
        for (operator, expected) in [
            (ConditionOperator::AnyCaseSensitive, expected_hit),
            (ConditionOperator::NoneCaseSensitive, !expected_hit),
        ] {
            assert_eq!(
                compare_case_sensitive_strings_in_array(value, target, operator),
                expected,
                "input={input:?}, operator={operator:?}"
            );
        }
    }
}

#[test]
fn exact_target_spellings_survive_json_and_protobuf_in_either_order() {
    for (first, second, miss) in [
        ("ios", "iOS", "IOS"),
        ("É", "é", "Éé"),
        ("İ", "i\u{307}", "I"),
        ("ΟΣ", "ος", "οσ"),
    ] {
        for (first, second) in [(first, second), (second, first)] {
            for len in [2, 5, 65] {
                let target = target_with_fillers(first, second, len);
                for operator in ["any_case_sensitive", "none_case_sensitive"] {
                    let condition = json_condition(operator, &target);
                    let proto = protobuf_conditions(&[(operator, target.clone())]);
                    let proto_condition = parsed_condition(&proto, "0");
                    for condition in [&condition, proto_condition] {
                        let parsed = condition.target_value.as_ref().unwrap();
                        assert_eq!(parsed.as_value_ref().array_len(), Some(len));
                        assert_eq!(serde_json::to_value(parsed).unwrap(), target);
                        for (input, hit) in [(first, true), (second, true), (miss, false)] {
                            assert_exact_membership(parsed.as_value_ref(), Some(json!(input)), hit);
                        }
                    }
                }
            }
        }
    }
    let repeated = json_condition("any_case_sensitive", &json!(["ios", "ios", "iOS"]));
    let target = repeated.target_value.as_ref().unwrap();
    assert_eq!(target.as_value_ref().array_len(), Some(2));
    assert_eq!(serde_json::to_value(target).unwrap(), json!(["ios", "iOS"]));
    for input in ["ios", "iOS"] {
        assert_exact_membership(target.as_value_ref(), Some(json!(input)), true);
    }
}

#[test]
fn exact_target_coercions_and_defaults_keep_existing_semantics() {
    for (input, candidate, expected) in [
        (None, json!(""), true),
        (Some(json!("")), json!(""), true),
        (Some(Value::Null), json!(""), true),
        (Some(json!({"a": 1})), json!(""), true),
        (Some(json!(42)), json!(42), true),
        (Some(json!(true)), json!(true), true),
        (Some(json!(3.25)), json!(3.25), true),
        (Some(json!(1.0)), json!(1.0), false),
        (Some(json!(["iOS", 1])), json!(["iOS", 1]), true),
        (Some(json!("x\u{0}Y")), json!("x\u{0}Y"), true),
    ] {
        // 4/5 exercise the cached-string cutoff; 64/65 exercise the eager
        // numeric/bool/default path that must construct its own lookup key.
        for len in [4, 5, 64, 65] {
            let mut target = vec![candidate.clone()];
            target.extend((1..len).map(|index| json!(format!("coercion-filler-{index}"))));
            let condition = json_condition("any_case_sensitive", &Value::Array(target));
            assert_exact_membership(
                condition.target_value.as_ref().unwrap().as_value_ref(),
                input.clone(),
                expected,
            );
        }
    }
    for target in [
        json!([]),
        Value::Null,
        json!({"iOS": true}),
        json!("iOS"),
        json!(42),
        json!(true),
    ] {
        let value = EvaluatorValue::from_json_value(target);
        assert_exact_membership(value.as_value_ref(), Some(json!("iOS")), false);
    }
}

#[test]
fn normalized_and_exact_target_caches_are_isolated_in_both_parse_orders() {
    let target = json!(["cache-ios", "CACHE-IOS"]);
    for operators in [["any", "any_case_sensitive"], ["any_case_sensitive", "any"]] {
        let json_conditions: Vec<_> = operators
            .iter()
            .map(|operator| json_condition(operator, &target))
            .collect();
        let protobuf = protobuf_conditions(&[
            (operators[0], target.clone()),
            (operators[1], target.clone()),
        ]);
        let proto_conditions = [
            parsed_condition(&protobuf, "0"),
            parsed_condition(&protobuf, "1"),
        ];
        for conditions in [[&json_conditions[0], &json_conditions[1]], proto_conditions] {
            let exact_index = usize::from(operators[0] != "any_case_sensitive");
            let exact = conditions[exact_index].target_value.as_ref().unwrap();
            let normalized = conditions[1 - exact_index].target_value.as_ref().unwrap();
            assert_ne!(exact.hash, normalized.hash);
            assert_eq!(exact.as_value_ref().array_len(), Some(2));
            assert_eq!(normalized.as_value_ref().array_len(), Some(1));
            assert_eq!(serde_json::to_value(exact).unwrap(), target);
            assert_eq!(
                serde_json::to_value(normalized).unwrap(),
                json!(["CACHE-IOS"])
            );
            for input in ["cache-ios", "CACHE-IOS"] {
                assert_exact_membership(exact.as_value_ref(), Some(json!(input)), true);
            }
            let input = UserValue::from("CaChE-IoS");
            assert!(compare_strings_in_array(
                (&input).into(),
                normalized.as_value_ref(),
                ConditionOperator::Any
            ));
            assert!(!compare_strings_in_array(
                (&input).into(),
                normalized.as_value_ref(),
                ConditionOperator::NoneOf
            ));
        }
    }
}

fn specs_json(conditions: serde_json::Map<String, Value>) -> Value {
    json!({
        "condition_map": conditions,
        "feature_gates": {},
        "dynamic_configs": {},
        "layer_configs": {},
        "experiment_to_layer": {},
        "has_updates": true,
        "time": 1
    })
}

fn gate_json(gate: &str, condition: &str) -> Value {
    json!({
        "name": gate,
        "type": "feature_gate",
        "salt": "exact-membership",
        "enabled": true,
        "defaultValue": false,
        "entity": "feature_gate",
        "idType": "userID",
        "rules": [{
            "name": "exact-rule", "id": "exact-rule", "conditions": [condition],
            "passPercentage": 100, "returnValue": true, "idType": "userID"
        }]
    })
}

fn evaluate_gate(
    specs: &SpecsResponseFull,
    user: &StatsigUserInternal<'_, '_>,
    gate: &str,
) -> bool {
    let lists = HashMap::new();
    let hashing = HashUtil::new();
    let mut context = EvaluatorContext::new(
        user,
        specs,
        IdListResolution::MapLookup(&lists),
        &hashing,
        None,
        None,
        false,
        false,
    );
    assert_eq!(
        Evaluator::evaluate(&mut context, gate, &SpecType::Gate).unwrap(),
        Recognition::Recognized
    );
    context.result.bool_value
}

#[test]
fn scalar_gate_dispatch_uses_exact_membership_for_public_and_fast_users() {
    let mut conditions = serde_json::Map::new();
    conditions.insert(
        "exact-any".into(),
        condition_json("any_case_sensitive", &json!(["ios", "iOS"])),
    );
    conditions.insert(
        "exact-none".into(),
        condition_json("none_case_sensitive", &json!(["ios", "iOS"])),
    );
    let mut payload = specs_json(conditions);
    for (gate, condition) in [("any-gate", "exact-any"), ("none-gate", "exact-none")] {
        payload["feature_gates"][gate] = gate_json(gate, condition);
    }
    let specs: SpecsResponseFull = serde_json::from_value(payload).unwrap();
    for (input, hit) in [("ios", true), ("iOS", true), ("IOS", false)] {
        let public = StatsigUser::with_user_id(input);
        let fast = FastStatsigUser::new(FastUserData {
            user_id: Some(UserValue::from(input)),
            ..Default::default()
        });
        for user in [
            StatsigUserInternal::new(&public, None),
            StatsigUserInternal::from_fast_user(&fast, None),
        ] {
            assert_eq!(evaluate_gate(&specs, &user, "any-gate"), hit);
            assert_eq!(evaluate_gate(&specs, &user, "none-gate"), !hit);
        }
    }
}

rusty_fork_test! {
    #[test]
    fn exact_and_normalized_targets_remain_distinct_in_immutable_preload() {
        let target = json!(["preload-ios", "PRELOAD-IOS"]);
        let mut conditions = serde_json::Map::new();
        conditions.insert(
            "exact".into(),
            condition_json("any_case_sensitive", &target),
        );
        conditions.insert("normalized".into(), condition_json("any", &target));
        let payload = serde_json::to_vec(&specs_json(conditions)).unwrap();
        InternedStore::preload(&payload).unwrap();
        let specs: SpecsResponseFull = serde_json::from_slice(&payload).unwrap();
        let exact = parsed_condition(&specs, "exact")
            .target_value
            .as_ref()
            .unwrap();
        let normalized = parsed_condition(&specs, "normalized")
            .target_value
            .as_ref()
            .unwrap();
        assert!(matches!(exact.inner, EvaluatorValueInner::Static(_)));
        assert!(matches!(normalized.inner, EvaluatorValueInner::Static(_)));
        assert_ne!(exact.hash, normalized.hash);
        assert_eq!(exact.as_value_ref().array_len(), Some(2));
        assert_eq!(normalized.as_value_ref().array_len(), Some(1));
        for input in ["preload-ios", "PRELOAD-IOS"] {
            assert_exact_membership(exact.as_value_ref(), Some(json!(input)), true);
        }
    }

    #[test]
    fn exact_target_spellings_use_actual_mmap_and_round_trip() {
        let mut conditions = serde_json::Map::new();
        let mut cases = Vec::new();
        for (first, second) in [("ios", "iOS"), ("İ", "i\u{307}")] {
            for (first, second) in [(first, second), (second, first)] {
                for len in [2, 5, 65] {
                    let target = target_with_fillers(first, second, len);
                    let id = cases.len().to_string();
                    conditions.insert(id.clone(), condition_json("any_case_sensitive", &target));
                    conditions.insert(format!("normalized-{id}"), condition_json("any", &target));
                    cases.push((id, target, first, second));
                }
            }
        }
        let mut empty_target = vec![json!("")];
        empty_target.extend((1..65).map(|index| json!(format!("empty-filler-{index}"))));
        let empty_target = Value::Array(empty_target);
        conditions.insert(
            "indexed-empty".into(),
            condition_json("any_case_sensitive", &empty_target),
        );
        conditions.insert(
            "normalized-indexed-empty".into(),
            condition_json("any", &empty_target),
        );
        cases.push(("indexed-empty".into(), empty_target, "", ""));
        let payload = serde_json::to_vec(&specs_json(conditions)).unwrap();
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("exact-targets.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();
        let specs: SpecsResponseFull = serde_json::from_slice(&payload).unwrap();
        for (id, target, first, second) in cases {
            let exact = parsed_condition(&specs, &id).target_value.as_ref().unwrap();
            let normalized = parsed_condition(&specs, &format!("normalized-{id}"))
                .target_value
                .as_ref()
                .unwrap();
            assert!(matches!(exact.inner, EvaluatorValueInner::Mmap(_)));
            assert!(matches!(normalized.inner, EvaluatorValueInner::Mmap(_)));
            assert_ne!(exact.hash, normalized.hash);
            assert_eq!(serde_json::to_value(exact).unwrap(), target);
            let protobuf = protobuf_conditions(&[
                ("any_case_sensitive", target.clone()),
                ("none_case_sensitive", target.clone()),
                ("any", target.clone()),
            ]);
            for condition in protobuf.condition_map.values() {
                assert!(matches!(
                    condition.target_value.as_ref().unwrap().inner,
                    EvaluatorValueInner::Mmap(_)
                ));
            }
            for exact in [
                exact,
                parsed_condition(&protobuf, "0")
                    .target_value
                    .as_ref()
                    .unwrap(),
                parsed_condition(&protobuf, "1")
                    .target_value
                    .as_ref()
                    .unwrap(),
            ] {
                for input in [first, second] {
                    assert_exact_membership(exact.as_value_ref(), Some(json!(input)), true);
                }
                if first.is_empty() {
                    for input in [None, Some(Value::Null), Some(json!({"a": 1}))] {
                        assert_exact_membership(exact.as_value_ref(), input, true);
                    }
                }
                assert_exact_membership(exact.as_value_ref(), Some(json!("absent")), false);
            }
        }
    }

    #[test]
    fn legacy_normalized_mmap_target_does_not_shadow_exact_json_or_protobuf() {
        // The untagged normalized value has the same storage/hash shape as a
        // snapshot built before exact targets were introduced. Raw payloads
        // remain available, so the exact parser can rebuild both spellings.
        let target = json!(["legacy-ios", "LEGACY-IOS"]);
        let mut conditions = serde_json::Map::new();
        conditions.insert("0".into(), condition_json("any", &target));
        conditions.insert("1".into(), condition_json("none", &target));
        let mut legacy_payload = specs_json(conditions);
        for (gate, condition) in [("legacy-any-gate", "0"), ("legacy-none-gate", "1")] {
            legacy_payload["feature_gates"][gate] = gate_json(gate, condition);
        }
        let payload = serde_json::to_vec(&legacy_payload).unwrap();
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("legacy-normalized.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();
        let normalized = EvaluatorValue::from_json_value(target.clone());
        assert!(matches!(normalized.inner, EvaluatorValueInner::Mmap(_)));
        assert_eq!(normalized.as_value_ref().array_len(), Some(1));

        // The archived gate graph remains reusable because it contains only
        // condition IDs. Each current decoder must rebuild exact targets even
        // while the evaluator traverses those archived rules.
        let mut current_payload = legacy_payload;
        current_payload["condition_map"]["0"]["operator"] = json!("any_case_sensitive");
        current_payload["condition_map"]["1"]["operator"] = json!("none_case_sensitive");
        let current: SpecsResponseFull = serde_json::from_value(current_payload.clone()).unwrap();
        let mut protobuf = protobuf_conditions(&[
            ("any_case_sensitive", target.clone()),
            ("none_case_sensitive", target.clone()),
        ]);
        protobuf.feature_gates = serde_json::from_value::<SpecsResponseFull>(current_payload)
            .unwrap()
            .feature_gates;
        for specs in [&current, &protobuf] {
            for gate in ["legacy-any-gate", "legacy-none-gate"] {
                assert!(
                    specs
                        .feature_gates
                        .get(&InternedString::from_str_ref(gate))
                        .unwrap()
                        .is_mmap()
                );
            }
            for id in ["0", "1"] {
                let exact = parsed_condition(specs, id).target_value.as_ref().unwrap();
                assert!(!matches!(exact.inner, EvaluatorValueInner::Mmap(_)));
                assert_ne!(exact.hash, normalized.hash);
                assert_eq!(serde_json::to_value(exact).unwrap(), target);
                for input in ["legacy-ios", "LEGACY-IOS"] {
                    assert_exact_membership(exact.as_value_ref(), Some(json!(input)), true);
                }
            }
            for (input, hit) in [
                ("legacy-ios", true),
                ("LEGACY-IOS", true),
                ("Legacy-Ios", false),
            ] {
                let public = StatsigUser::with_user_id(input);
                let fast = FastStatsigUser::new(FastUserData {
                    user_id: Some(UserValue::from(input)),
                    ..Default::default()
                });
                for user in [
                    StatsigUserInternal::new(&public, None),
                    StatsigUserInternal::from_fast_user(&fast, None),
                ] {
                    assert_eq!(evaluate_gate(specs, &user, "legacy-any-gate"), hit);
                    assert_eq!(evaluate_gate(specs, &user, "legacy-none-gate"), !hit);
                }
            }
        }
    }
}
