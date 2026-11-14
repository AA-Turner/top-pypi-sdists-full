use super::tests::planned_and_unplanned_response_values_with_specs;
use crate::ClientInitResponseOptions;
use serde_json::{Value, json};

fn response(value: &str, previous: &str) -> Value {
    let options = ClientInitResponseOptions {
        previous_response_hash: Some(previous.to_owned()),
        ..Default::default()
    };
    let (unplanned, planned) =
        planned_and_unplanned_response_values_with_specs(&options, None, |specs| {
            specs.cmab_configs = serde_json::from_value(json!({
                "checksum_cmab": {
                    "salt": "checksum-cmab", "defaultValue": {"value": value},
                    "idType": "userID", "enabled": false, "version": 1,
                    "sampleRate": 0.0, "higherIsBetter": true, "groups": []
                }
            }))
            .unwrap();
        });
    assert_eq!(unplanned, planned);
    unplanned
}

#[test]
fn cmab_value_changes_invalidate_v1_checksum() {
    let first = response("before", "");
    let changed = response("after", first["full_checksum"].as_str().unwrap());
    assert_eq!(changed["has_updates"], true);
    assert_ne!(first["dynamic_configs"], changed["dynamic_configs"]);
    assert_ne!(first["full_checksum"], changed["full_checksum"]);

    let unchanged = response("after", changed["full_checksum"].as_str().unwrap());
    assert_eq!(unchanged["has_updates"], false);
}
