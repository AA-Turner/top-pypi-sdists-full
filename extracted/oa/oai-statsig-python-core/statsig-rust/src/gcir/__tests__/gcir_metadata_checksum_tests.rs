use super::tests::planned_and_unplanned_response_values_with_specs;
use crate::ClientInitResponseOptions;
use serde_json::{Value, json};

fn metadata() -> Value {
    json!({
        "sdk_configs": {"live_values_auto_refresh_interval_seconds": 60},
        "session_replay_info": {
            "sampling_rate": 0.9,
            "recording_blocked": true,
            "session_recording_privacy_settings": {"privacy_mode": "mask-all"}
        }
    })
}

fn response(metadata: &Value, previous: &str) -> Value {
    let (unplanned, planned) = planned_and_unplanned_response_values_with_specs(
        &ClientInitResponseOptions {
            previous_response_hash: Some(previous.to_owned()),
            ..Default::default()
        },
        None,
        |specs| {
            specs.sdk_configs = serde_json::from_value(metadata["sdk_configs"].clone()).unwrap();
            specs.session_replay_info =
                serde_json::from_value(metadata["session_replay_info"].clone()).unwrap();
        },
    );
    assert_eq!(unplanned, planned);
    unplanned
}

#[test]
fn emitted_metadata_invalidates_checksum_and_unchanged_metadata_is_suppressed() {
    let original = metadata();
    let initial = response(&original, "stale");
    let checksum = initial["full_checksum"].as_str().unwrap();
    assert_eq!(response(&original, checksum)["has_updates"], false);

    for (pointer, value) in [
        (
            "/sdk_configs/live_values_auto_refresh_interval_seconds",
            json!("60"),
        ),
        ("/session_replay_info/sampling_rate", json!(1.0)),
        (
            "/session_replay_info/session_recording_privacy_settings/privacy_mode",
            json!("mask-none"),
        ),
    ] {
        let mut changed = original.clone();
        *changed.pointer_mut(pointer).unwrap() = value;
        let updated = response(&changed, checksum);
        assert_eq!(updated["has_updates"], true, "{pointer}");
        assert_ne!(
            updated["full_checksum"], initial["full_checksum"],
            "{pointer}"
        );
        assert_eq!(updated["can_record_session"], initial["can_record_session"]);
        assert_eq!(
            response(&changed, updated["full_checksum"].as_str().unwrap())["has_updates"],
            false
        );
    }
    let absent = json!({"sdk_configs": {}, "session_replay_info": {"recording_blocked": true}});
    let removed = response(&absent, checksum);
    assert_eq!(removed["has_updates"], true);
    assert_eq!(
        response(&original, removed["full_checksum"].as_str().unwrap())["has_updates"],
        true
    );
}

#[test]
fn server_only_sdk_metadata_does_not_invalidate_checksum() {
    let mut original = metadata();
    let initial = response(&original, "stale");
    original["sdk_configs"]["event_queue_size"] = json!(1234);
    assert_eq!(
        response(&original, initial["full_checksum"].as_str().unwrap())["has_updates"],
        false
    );
}
