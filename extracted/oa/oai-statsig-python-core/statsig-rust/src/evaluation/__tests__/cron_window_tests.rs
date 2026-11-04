use std::collections::HashMap;

use serde_json::json;

use crate::{
    StatsigUser,
    evaluation::{
        evaluator::{Evaluator, Recognition, SpecType},
        evaluator_context::{EvaluatorContext, IdListResolution},
    },
    hashing::HashUtil,
    specs_response::{
        parse_options::SpecsResponseParseOptions,
        spec_types::{ConditionOperator, SpecsResponseFull},
    },
    user::StatsigUserInternal,
};

#[test]
fn current_time_cron_window_evaluates_through_a_gate() {
    let payload = serde_json::to_vec(&json!({
        "condition_map": {
            "cron-condition": {
                "type": "current_time",
                "operator": "in_cron_window",
                "targetValue": "* * * * *|60",
                "field": null,
                "additionalValues": {},
                "idType": "userID"
            }
        },
        "feature_gates": {
            "cron-gate": {
                "name": "cron-gate",
                "type": "feature_gate",
                "salt": "cron-window",
                "enabled": true,
                "defaultValue": false,
                "entity": "feature_gate",
                "idType": "userID",
                "rules": [{
                    "name": "cron-rule",
                    "id": "cron-rule",
                    "conditions": ["cron-condition"],
                    "passPercentage": 100,
                    "returnValue": true,
                    "idType": "userID"
                }]
            }
        },
        "dynamic_configs": {},
        "layer_configs": {},
        "experiment_to_layer": {},
        "has_updates": true,
        "time": 1
    }))
    .unwrap();
    let specs = SpecsResponseFull::deserialize_json_with_options(
        &payload,
        SpecsResponseParseOptions::default(),
    )
    .unwrap();
    let condition = specs.condition_map.values().next().unwrap();
    assert_eq!(condition.compiled_operator, ConditionOperator::InCronWindow);

    let user = StatsigUser::with_user_id("cron-user");
    let internal_user = StatsigUserInternal::new(&user, None);
    let id_lists = HashMap::new();
    let hashing = HashUtil::new();
    let mut context = EvaluatorContext::new(
        &internal_user,
        &specs,
        IdListResolution::MapLookup(&id_lists),
        &hashing,
        None,
        None,
        false,
        false,
    );

    assert_eq!(
        Evaluator::evaluate(&mut context, "cron-gate", &SpecType::Gate).unwrap(),
        Recognition::Recognized
    );
    assert!(context.result.bool_value);
    assert!(!context.result.unsupported);
}
