use std::collections::HashMap;

use crate::StatsigUser;
use crate::evaluation::evaluator::{Evaluator, Recognition, SpecType};
use crate::evaluation::evaluator_context::{EvaluatorContext, IdListResolution};
use crate::hashing::HashUtil;
use crate::specs_response::spec_types::SpecsResponseFull;
use crate::user::StatsigUserInternal;

#[test]
#[serial_test::serial]
fn only_top_level_manual_layer_exposures_omit_values() {
    let specs: SpecsResponseFull = serde_json::from_str(
        r#"{
        "feature_gates": {}, "dynamic_configs": {}, "experiment_to_layer": {},
        "condition_map": {}, "has_updates": true, "time": 1,
        "layer_configs": {"layer": {"type":"layer","salt":"s","enabled":true,"rules":[],
            "entity":"layer","idType":"userID","useNewLayerEval":true,"defaultValue":{"flag":true}}}
    }"#,
    )
    .unwrap();
    let user = StatsigUser::with_user_id("member");
    let internal = StatsigUserInternal::new(&user, None);
    let ids = HashMap::new();
    let hashing = HashUtil::new();
    for (manual, nested, expect_values) in [(false, 0, true), (true, 0, false), (true, 1, true)] {
        let mut ctx = EvaluatorContext::new(
            &internal,
            &specs,
            IdListResolution::MapLookup(&ids),
            &hashing,
            None,
            None,
            false,
            false,
        );
        ctx.manual_layer_exposure_only = manual;
        ctx.reuse_default_only_layer_values = true;
        ctx.nested_count = nested;
        assert_eq!(
            Evaluator::evaluate(&mut ctx, "layer", &SpecType::Layer).unwrap(),
            Recognition::Recognized
        );
        assert_eq!(ctx.result.json_value.is_some(), expect_values);
        assert_eq!(ctx.result.parameter_rule_ids.is_some(), expect_values);
        assert_eq!(ctx.result.rule_id.as_ref().unwrap().as_str(), "default");
    }
}
