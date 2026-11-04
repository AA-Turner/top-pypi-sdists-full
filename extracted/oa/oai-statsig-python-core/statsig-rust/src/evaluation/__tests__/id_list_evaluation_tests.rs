use std::collections::HashMap;

use serde_json::json;

use crate::{
    StatsigUser,
    evaluation::{
        evaluator::{Evaluator, Recognition, SpecType},
        evaluator_context::{EvaluatorContext, IdListResolution},
    },
    hashing::HashUtil,
    id_lists_adapter::{IdList, IdListMetadata, IdListUpdate},
    specs_response::spec_types::SpecsResponseFull,
    user::StatsigUserInternal,
};

#[test]
fn id_list_conditions_use_the_same_eight_byte_hash_in_both_resolvers() {
    // Independently computed SHA-256/base64 prefixes, including Unicode and NUL.
    for (user_id, expected) in [
        ("", "47DEQpj8"),
        ("alice", "K9gGyX8O"),
        ("用户🙂\0", "++a+4K87"),
        ("é", "SplVfkAz"),
    ] {
        let public_user = StatsigUser::with_user_id(user_id);
        let user = StatsigUserInternal::new(&public_user, None);
        let hashing = HashUtil::new();
        for (operator, negate) in [("in_segment_list", false), ("not_in_segment_list", true)] {
            let specs: SpecsResponseFull = serde_json::from_value(json!({
                "feature_gates": {"membership": {
                    "name": "membership", "type": "feature_gate", "salt": "fixture",
                    "enabled": true, "defaultValue": false, "entity": "feature_gate",
                    "idType": "userID", "rules": [{
                        "name": "member", "id": "member", "passPercentage": 100,
                        "returnValue": true, "idType": "userID", "conditions": ["member"]
                    }]
                }},
                "condition_map": {"member": {
                    "type": "unit_id", "operator": operator, "targetValue": "members",
                    "idType": "userID", "additionalValues": {}
                }},
                "dynamic_configs": {}, "layer_configs": {}, "experiment_to_layer": {},
                "has_updates": true, "time": 1
            }))
            .unwrap();
            for present in [false, true] {
                let metadata = IdListMetadata {
                    name: "members".into(),
                    url: "https://example.com/members".into(),
                    file_id: Some("fixture".into()),
                    size: 0,
                    creation_time: 1,
                };
                let mut list = IdList::new(metadata.clone());
                let mut body = format!("+{}\n+{expected}-suffix\n", &expected[..7]);
                if present {
                    body.push_str(&format!("+{expected}\n"));
                }
                list.apply_update(IdListUpdate {
                    raw_changeset: Some(body),
                    new_metadata: metadata,
                });
                let lists = HashMap::from([("members".into(), list)]);
                let callback = |name: &str, lookup: &str| {
                    assert_eq!(name, "members");
                    assert_eq!(lookup, expected);
                    present
                };
                for resolver in [
                    IdListResolution::MapLookup(&lists),
                    IdListResolution::Callback(&callback),
                ] {
                    let mut context = EvaluatorContext::new(
                        &user, &specs, resolver, &hashing, None, None, false, false,
                    );
                    assert_eq!(
                        Evaluator::evaluate(&mut context, "membership", &SpecType::Gate).unwrap(),
                        Recognition::Recognized
                    );
                    assert_eq!(
                        context.result.bool_value,
                        present != negate,
                        "user={user_id:?}, operator={operator}"
                    );
                }
            }
        }
    }
}
