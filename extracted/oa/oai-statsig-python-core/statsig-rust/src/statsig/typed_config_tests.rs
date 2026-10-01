use super::*;
use crate::{SpecsUpdate, networking::ResponseData};

const EVAL_PROJ_JSON: &[u8] = include_bytes!("../../tests/data/eval_proj_dcs.json");

#[test]
fn typed_config_revision_uses_evaluated_snapshot_during_publication() {
    let statsig = Statsig::new("secret-key", None);
    let mut specs: Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
    let name = "test_custom_config";
    specs["dynamic_configs"][name]["version"] = json!(111);
    specs["dynamic_configs"][name]["checksum"] = json!("revision-a");
    specs["dynamic_configs"][name]["rules"][0]["returnValue"] = json!({"number": 1});
    specs["condition_map"]["3576002308"] = json!({
        "type": "experiment_group",
        "field": "test_experiment_no_targeting",
        "operator": "any",
        "targetValue": ["Control", "Test", "Test2"],
        "additionalValues": {"experiment_name": "test_experiment_no_targeting"},
        "idType": "userID"
    });
    statsig
        .spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
            source: SpecsSource::Network,
            received_at: 2_000,
            source_api: None,
            has_updates: None,
        })
        .unwrap();

    specs["time"] = json!(specs["time"].as_u64().unwrap() + 1);
    specs["checksum"] = json!("snapshot-b");
    specs["dynamic_configs"][name]["version"] = json!(112);
    specs["dynamic_configs"][name]["checksum"] = json!("revision-b");
    specs["dynamic_configs"][name]["rules"][0]["returnValue"] = json!({"number": 2});
    let store = Arc::clone(&statsig.spec_store);
    statsig.event_emitter.subscribe(
        crate::sdk_event_emitter::SdkEvent::EXPERIMENT_EVALUATED,
        move |_| {
            store
                .set_values(SpecsUpdate {
                    data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
                    source: SpecsSource::Network,
                    received_at: 3_000,
                    source_api: None,
                    has_updates: None,
                })
                .unwrap();
        },
    );

    let user = StatsigUser::with_user_id("snapshot-user");
    let user = statsig.internalize_user(&user);
    for (version, checksum, number) in [(111, "revision-a", 1), (112, "revision-b", 2)] {
        statsig.use_typed_config(
            &user,
            name,
            DynamicConfigEvaluationOptions {
                disable_exposure_logging: true,
            },
            |raw, source, revisions| {
                assert_eq!(raw.details.version, Some(version));
                assert_eq!(source, "Network");
                assert_eq!(
                    revisions,
                    &[(name.to_string(), Some(version), Some(checksum.to_string()))]
                );
                let result: Value =
                    serde_json::from_str(&raw.unperformant_to_json_string()).unwrap();
                assert_eq!(result["value"], json!({"number": number}));
            },
        );
    }
}
