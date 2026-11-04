mod utils;

use crate::utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use serde_json::{Value, json};
use statsig_rust::interned_string::InternedString;
use statsig_rust::user::StatsigUserInternal;
use statsig_rust::{Statsig, StatsigOptions, StatsigUser};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;

fn fixture() -> Value {
    let mut specs: Value = serde_json::from_str(include_str!("data/perf_proj_dcs.json")).unwrap();
    specs["checksum"] = json!("101");
    for layer in specs["layer_configs"].as_object_mut().unwrap().values_mut() {
        layer["useNewLayerEval"] = json!(true);
    }
    let layer = specs["layer_configs"]["a_layer"].clone();
    for (name, count) in [("small", 1), ("wide", 78), ("mixed", 78)] {
        let mut custom = layer.clone();
        custom["defaultValue"] = Value::Object(
            (0..count)
                .map(|i| {
                    (
                        format!("key_{i}"),
                        json!({"enabled":true, "values":[1,2,3]}),
                    )
                })
                .collect(),
        );
        custom["rules"] = if name == "mixed" {
            json!([
                {"name":"first", "id":"first", "salt":"first", "idType":"userID","conditions":["manual_user"],"passPercentage":100,"returnValue":{"key_0":1}},
                {"name":"second", "id":"second", "salt":"second", "idType":"userID","conditions":[],"passPercentage":100,"returnValue":{"key_0":2,"key_1":2}}
            ])
        } else {
            json!([])
        };
        specs["layer_configs"][name] = custom;
    }
    specs["condition_map"]["manual_user"] = json!({"type":"user_field","field":"userID","operator":"any_case_sensitive","targetValue":["member"],"idType":"userID"});
    specs
}

async fn start(specs: Arc<MockSpecsAdapter>, logs: &Arc<MockEventLoggingAdapter>) -> Statsig {
    let sdk = Statsig::new(
        "secret-manual-layer",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(specs),
            event_logging_adapter: Some(logs.clone()),
            ..StatsigOptions::new()
        })),
    );
    sdk.initialize().await.unwrap();
    sdk
}

#[tokio::test]
async fn manual_layer_events_match_full_evaluation() {
    let file = tempfile::NamedTempFile::new().unwrap();
    let mut specs = fixture();
    std::fs::write(file.path(), serde_json::to_vec(&specs).unwrap()).unwrap();
    let adapter = Arc::new(MockSpecsAdapter::with_data(file.path().to_str().unwrap()));
    let logs = Arc::new(MockEventLoggingAdapter::new());
    let sdk = start(adapter.clone(), &logs).await;
    for (id, requests) in [
        (
            "member",
            &[
                ("big_layer", "key_0"),
                ("big_layer", "key_0"),
                ("mixed", "key_0"),
                ("missing_layer", "missing_key"),
            ][..],
        ),
        ("other", &[("big_layer", "key_0")][..]),
    ] {
        let user = StatsigUser::with_user_id(id);
        let internal = StatsigUserInternal::new(&user, Some(&sdk));
        for &(name, key) in requests {
            sdk.manually_log_layer_parameter_exposure_for_internal_user_with_metadata(
                &internal,
                &InternedString::from_str_ref(name),
                InternedString::from_str_ref(key),
                Some(HashMap::from([("consumer".into(), json!("manual"))])),
            );
        }
        // The full get and automatic exposure must still use the complete value/rule maps.
        let layer = sdk.get_layer(&user, "big_layer");
        assert_ne!(layer.get_string("a_string", "missing".into()), "missing");
    }
    specs["time"] = json!(specs["time"].as_u64().unwrap() + 1000);
    specs["checksum"] = json!("102");
    specs["layer_configs"]["mixed"]["version"] =
        json!(specs["layer_configs"]["mixed"]["version"].as_u64().unwrap() + 1);
    specs["layer_configs"]["mixed"]["rules"] = json!([{
        "name":"Control", "id":"after-update", "salt":"after", "idType":"userID",
        "conditions":[],"passPercentage":100,"returnValue":{"key_0":3},
        "sharedControlExperiments":[{"name":"an_experiment","controlGroupID":"fixture-control"}]
    }]);
    std::fs::write(file.path(), serde_json::to_vec(&specs).unwrap()).unwrap();
    adapter.resync().await.unwrap();
    sdk.manually_log_layer_parameter_exposure(
        &StatsigUser::with_user_id("member"),
        "mixed",
        "after-update".into(),
    );
    sdk.flush_events().await;
    let payloads = logs.logged_payloads.lock().unwrap();
    let mut events = Vec::new();
    for event in payloads.iter().flat_map(|p| p.events.as_array().unwrap()) {
        if event["eventName"].as_str().unwrap().contains("exposure") {
            let mut event = event.clone();
            event.as_object_mut().unwrap().remove("time");
            let metadata = event["metadata"].as_object_mut().unwrap();
            for key in ["receivedAt", "serverTime", "initTime", "configSyncTime"] {
                metadata.remove(key);
            }
            event.sort_all_objects();
            events.push(event);
        }
    }
    events.sort_by_key(Value::to_string);
    // Captured with the full-value evaluator. Only runtime timestamps are excluded.
    let expected: Vec<Value> =
        serde_json::from_str(include_str!("data/manual_layer_events.json")).unwrap();
    assert_eq!(events, expected);
}

#[tokio::test]
#[ignore = "offline timing benchmark"]
async fn benchmark_manual_layer_exposure() {
    let contents = match std::env::var_os("STATSIG_MANUAL_LAYER_BENCH_SPECS") {
        Some(path) => std::fs::read_to_string(path).unwrap(),
        None => fixture().to_string(),
    };
    let cases = std::env::var("STATSIG_MANUAL_LAYER_BENCH_CASES").unwrap_or_else(|_| {
        "small/key_0,wide/key_0,mixed/key_0,a_layer/a_param,big_layer/a_string".to_owned()
    });
    for case in cases.split(',') {
        let (name, key) = case.split_once('/').unwrap();
        let mut first = Vec::new();
        let mut repeated = Vec::new();
        let mut distinct = Vec::new();
        for _ in 0..9 {
            let logs = Arc::new(MockEventLoggingAdapter::new());
            let sdk = start(
                Arc::new(MockSpecsAdapter::with_json_data(contents.clone())),
                &logs,
            )
            .await;
            let user = StatsigUser::with_user_id("member");
            let t = Instant::now();
            sdk.manually_log_layer_parameter_exposure(&user, name, key.into());
            first.push(t.elapsed().as_nanos());
            let t = Instant::now();
            for _ in 0..300 {
                sdk.manually_log_layer_parameter_exposure(&user, name, key.into());
            }
            repeated.push(t.elapsed().as_nanos() / 300);
            let users: Vec<_> = (0..300)
                .map(|i| StatsigUser::with_user_id(format!("distinct-{i}")))
                .collect();
            let t = Instant::now();
            for user in &users {
                sdk.manually_log_layer_parameter_exposure(user, name, key.into());
            }
            distinct.push(t.elapsed().as_nanos() / 300);
            sdk.shutdown().await.unwrap();
        }
        first.sort_unstable();
        repeated.sort_unstable();
        distinct.sort_unstable();
        println!(
            "manual_layer {name}: first={} repeated={} distinct={} ns/op",
            first[4], repeated[4], distinct[4]
        );
    }
}
