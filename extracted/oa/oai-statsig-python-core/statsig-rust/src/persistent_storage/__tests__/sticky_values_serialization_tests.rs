use std::collections::HashMap;

use crate::{
    DynamicReturnable, SecondaryExposure, StickyValues, interned_string::InternedString,
    specs_response::explicit_params::ExplicitParameters,
};
use serde_json::{Value, json};

fn persisted_values() -> Value {
    json!({
        "value": true,
        "json_value": {"header_text": "old user test"},
        "rule_id": "3ZCniK9rvnQyXDQlQ1tGD9",
        "group_name": "test_group",
        "secondary_exposures": [{"gate": "test_holdout", "gateValue": "true", "ruleID": "default"}],
        "undelegated_secondary_exposures": [],
        "config_delegate": null,
        "explicit_parameters": null,
        "time": 1757974789243_u64,
        "config_version": 1,
    })
}

#[test]
fn deserializes_sticky_values_from_value_and_string() {
    let raw = persisted_values();
    let from_value = serde_json::from_value::<StickyValues>(raw.clone()).unwrap();
    let from_string = serde_json::from_str::<StickyValues>(&raw.to_string()).unwrap();

    for sticky in [from_value, from_string] {
        assert!(sticky.value);
        assert_eq!(
            sticky.json_value.unwrap().get_json().unwrap(),
            HashMap::from([("header_text".to_owned(), json!("old user test"))])
        );
        assert_eq!(sticky.rule_id.unwrap().as_str(), "3ZCniK9rvnQyXDQlQ1tGD9");
        assert_eq!(sticky.group_name.unwrap().as_str(), "test_group");
        assert_eq!(sticky.secondary_exposures.len(), 1);
        let exposure = &sticky.secondary_exposures[0];
        assert_eq!(exposure.gate.as_str(), "test_holdout");
        assert_eq!(exposure.gate_value.as_str(), "true");
        assert_eq!(exposure.rule_id.as_str(), "default");
        assert!(sticky.undelegated_secondary_exposures.unwrap().is_empty());
        assert!(sticky.config_delegate.is_none());
        assert!(sticky.explicit_parameters.is_none());
        assert_eq!(sticky.time, Some(1757974789243));
        assert_eq!(sticky.config_version, Some(1));
    }
}

#[test]
fn serializes_sticky_values_to_value_and_string() {
    for assignment in [
        HashMap::new(),
        HashMap::from([("header_text".to_owned(), json!("old user test"))]),
    ] {
        let sticky = StickyValues {
            value: true,
            json_value: Some(DynamicReturnable::from_map(assignment.clone())),
            rule_id: Some(InternedString::from_str_ref("3ZCniK9rvnQyXDQlQ1tGD9")),
            group_name: Some(InternedString::from_str_ref("test_group")),
            secondary_exposures: vec![SecondaryExposure {
                gate: InternedString::from_str_ref("test_holdout"),
                gate_value: InternedString::from_str_ref("true"),
                rule_id: InternedString::default_rule_id(),
            }],
            undelegated_secondary_exposures: None,
            config_delegate: Some(InternedString::from_str_ref("test_delegate")),
            explicit_parameters: Some(ExplicitParameters::from_vec(vec!["test_param".to_owned()])),
            time: Some(1757974789243),
            config_version: Some(1),
        };
        let mut expected = persisted_values();
        expected["json_value"] = json!(assignment);
        expected["undelegated_secondary_exposures"] = Value::Null;
        expected["config_delegate"] = json!("test_delegate");
        expected["explicit_parameters"] = json!(["test_param"]);

        assert_eq!(serde_json::to_value(&sticky).unwrap(), expected);
        let serialized = serde_json::to_string(&sticky).unwrap();
        assert_eq!(
            serde_json::from_str::<Value>(&serialized).unwrap(),
            expected
        );
    }
}
