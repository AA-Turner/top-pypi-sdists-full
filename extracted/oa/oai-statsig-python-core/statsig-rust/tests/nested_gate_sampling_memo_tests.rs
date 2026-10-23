use std::{collections::HashMap, sync::Arc};

use serde_json::{Value, json};
use statsig_rust::{
    DynamicValue, OverrideAdapter, StatsigLocalOverrideAdapter, StatsigUser,
    evaluation::{
        evaluation_types::ExtraExposureInfo,
        evaluator::{Evaluator, SpecType},
        evaluator_context::{EvaluatorContext, IdListResolution},
        evaluator_result::result_to_extra_exposure_info,
    },
    event_logging::{
        event_queue::queued_event::{EnqueueOperation, QueuedEvent, QueuedExposure},
        exposure_sampling::{
            EvtSamplingDecision, EvtSamplingMode, ExposureSampling, ExposureSamplingKey,
        },
    },
    global_configs::GlobalConfigs,
    hashing::HashUtil,
    specs_response::spec_types::SpecsResponseFull,
    user::StatsigUserInternal,
};

fn condition(kind: &str, target: Value) -> Value {
    json!({"type": kind, "targetValue": target, "operator": null,
        "field": null, "additionalValues": {}, "idType": "userID"})
}

fn rule(conditions: &[&str], value: bool, rate: Option<u64>) -> Value {
    let mut rule = json!({"name": "rule", "id": "rule", "salt": "rule",
        "conditions": conditions, "returnValue": value,
        "passPercentage": 100, "idType": "userID"});
    if let Some(rate) = rate {
        rule["samplingRate"] = json!(rate);
    }
    rule
}

fn gate(entity: &str, rules: Vec<Value>) -> Value {
    json!({"type": "feature_gate", "salt": "gate", "enabled": true,
        "defaultValue": false, "rules": rules, "idType": "userID",
        "entity": entity, "version": 1})
}

fn fixture() -> Value {
    json!({
        "has_updates": true, "time": 1000, "company_id": null,
        "dynamic_configs": {}, "layer_configs": {}, "experiment_to_layer": {},
        "feature_gates": {
            "numeric": gate("feature_gate", vec![rule(&["public"], true, Some(2741))]),
            "analytical": gate("feature_gate", vec![rule(&["public"], true, None)]),
            "segment:none": gate("segment", vec![]),
            "wrapper": gate("feature_gate", vec![rule(&["pass_analytical"], true, Some(101))]),
            "parent": gate("feature_gate", vec![rule(&["pass_numeric"], true, Some(201))]),
            // A missing continuation stops before caller finalization, exposing the
            // metadata left by the nested gate without changing production APIs.
            "probe": gate("feature_gate", vec![rule(&["pass_numeric", "missing"], true, Some(201))])
        },
        "condition_map": {
            "public": condition("public", Value::Null),
            "pass_numeric": condition("pass_gate", json!("numeric")),
            "pass_analytical": condition("pass_gate", json!("analytical")),
            "pass_segment": condition("pass_gate", json!("segment:none")),
            "pass_wrapper": condition("pass_gate", json!("wrapper"))
        }
    })
}

fn with_context(fixture: Value, test: impl FnOnce(&mut EvaluatorContext<'_>)) {
    with_override_context(fixture, None, test);
}

fn with_override_context(
    fixture: Value,
    adapter: Option<Arc<dyn OverrideAdapter>>,
    test: impl FnOnce(&mut EvaluatorContext<'_>),
) {
    let specs: SpecsResponseFull = serde_json::from_value(fixture).unwrap();
    let user = StatsigUser::with_user_id("sampling-memo-user");
    let internal = StatsigUserInternal::new(&user, None);
    let hashing = HashUtil::new();
    let lists = HashMap::new();
    let mut ctx = EvaluatorContext::new(
        &internal,
        &specs,
        IdListResolution::MapLookup(&lists),
        &hashing,
        None,
        adapter.as_ref(),
        false,
        false,
    );
    test(&mut ctx);
}

fn evaluate(ctx: &mut EvaluatorContext<'_>, name: &str) {
    Evaluator::evaluate(ctx, name, &SpecType::Gate).unwrap();
}

fn snapshot(ctx: &EvaluatorContext<'_>) -> Value {
    json!({
        "value": ctx.result.bool_value,
        "rule": ctx.result.rule_id,
        "rate": ctx.result.sampling_rate,
        "forward": ctx.result.forward_all_exposures,
        "analytical": ctx.result.has_seen_analytical_gates == Some(true),
        "exposures": ctx.result.secondary_exposures,
    })
}

#[test]
fn cached_numeric_gate_restores_rate_after_an_unsampled_segment() {
    with_context(fixture(), |ctx| {
        evaluate(ctx, "probe");
        let cold = snapshot(ctx);
        assert_eq!(cold["rate"], json!(2741));
        assert_eq!(cold["analytical"], json!(false));

        ctx.reset_result();
        evaluate(ctx, "segment:none");
        assert_eq!(ctx.result.sampling_rate, None);
        evaluate(ctx, "probe");
        assert_eq!(snapshot(ctx), cold);
    });
}

#[test]
fn cached_analytical_gate_restores_none_after_a_numeric_gate() {
    let mut data = fixture();
    data["feature_gates"]["probe"]["rules"][0]["conditions"] =
        json!(["pass_analytical", "missing"]);
    with_context(data, |ctx| {
        evaluate(ctx, "probe");
        let cold = snapshot(ctx);
        assert_eq!(cold["rate"], Value::Null);
        assert_eq!(cold["analytical"], json!(true));

        ctx.reset_result();
        evaluate(ctx, "numeric");
        evaluate(ctx, "probe");
        assert_eq!(snapshot(ctx), cold);
    });
}

#[test]
fn numeric_gate_memo_preserves_its_analytical_descendant_after_reset() {
    let mut data = fixture();
    data["feature_gates"]["parent"]["rules"][0]["conditions"] = json!(["pass_wrapper"]);
    with_context(data, |ctx| {
        evaluate(ctx, "parent");
        let cold = snapshot(ctx);
        assert_eq!(cold["rate"], json!(201));
        assert_eq!(cold["analytical"], json!(true));

        ctx.reset_result();
        evaluate(ctx, "numeric");
        ctx.result.secondary_exposures.clear();
        evaluate(ctx, "parent");
        assert_eq!(snapshot(ctx), cold);
    });
}

#[test]
fn an_ancestor_analytical_marker_does_not_pollute_a_numeric_gate_memo() {
    let mut data = fixture();
    data["feature_gates"]["parent"]["rules"][0]["conditions"] =
        json!(["pass_analytical", "pass_numeric"]);
    with_context(data, |ctx| {
        evaluate(ctx, "parent");
        assert_eq!(ctx.result.has_seen_analytical_gates, Some(true));
        ctx.reset_result();
        evaluate(ctx, "numeric");
        evaluate(ctx, "probe");
        assert_ne!(ctx.result.has_seen_analytical_gates, Some(true));
    });
}

#[test]
fn cached_gate_keeps_a_parent_analytical_marker() {
    with_context(fixture(), |ctx| {
        evaluate(ctx, "probe");
        ctx.reset_result();
        ctx.result.has_seen_analytical_gates = Some(true);
        evaluate(ctx, "probe");
        assert_eq!(ctx.result.has_seen_analytical_gates, Some(true));
    });
}

#[test]
fn cached_local_override_preserves_the_callers_sampling_metadata() {
    let adapter: Arc<dyn OverrideAdapter> = Arc::new(StatsigLocalOverrideAdapter::new());
    adapter.override_gate("numeric", true, None);
    with_override_context(fixture(), Some(adapter), |ctx| {
        ctx.result.sampling_rate = Some(17);
        ctx.result.forward_all_exposures = Some(true);
        evaluate(ctx, "probe");
        assert_eq!(ctx.result.sampling_rate, Some(17));
        assert_eq!(ctx.result.forward_all_exposures, Some(true));
        ctx.reset_result();
        ctx.result.sampling_rate = Some(201);
        ctx.result.forward_all_exposures = Some(false);
        evaluate(ctx, "probe");
        assert_eq!(ctx.result.sampling_rate, Some(201));
        assert_eq!(ctx.result.forward_all_exposures, Some(false));
        assert_ne!(ctx.result.has_seen_analytical_gates, Some(true));
        assert_eq!(
            ctx.result.secondary_exposures[0].rule_id.as_str(),
            "override"
        );
    });
}

#[test]
fn cached_unrecognized_gate_preserves_the_callers_sampling_metadata() {
    let mut data = fixture();
    data["feature_gates"]
        .as_object_mut()
        .unwrap()
        .remove("numeric");
    with_context(data, |ctx| {
        ctx.result.sampling_rate = Some(17);
        ctx.result.forward_all_exposures = Some(true);
        evaluate(ctx, "probe");
        ctx.reset_result();
        ctx.result.sampling_rate = Some(201);
        ctx.result.forward_all_exposures = Some(false);
        evaluate(ctx, "probe");
        assert_eq!(ctx.result.sampling_rate, Some(201));
        assert_eq!(ctx.result.forward_all_exposures, Some(false));
        assert!(!ctx.result.bool_value);
        assert_eq!(ctx.result.rule_id, None);
        assert!(ctx.result.secondary_exposures.is_empty());
    });
}

#[test]
fn nested_evaluation_errors_keep_the_parent_analytical_marker() {
    with_context(fixture(), |ctx| {
        ctx.result.has_seen_analytical_gates = Some(true);
        ctx.nested_count = 300;
        assert!(Evaluator::evaluate(ctx, "probe", &SpecType::Gate).is_err());
        assert_eq!(ctx.result.has_seen_analytical_gates, Some(true));
        assert_eq!(ctx.nested_count, 300);
    });
}

#[test]
fn recursive_child_errors_restore_the_saved_parent_marker() {
    let mut data = fixture();
    data["feature_gates"]["probe"]["rules"][0]["conditions"] = json!(["pass_wrapper", "missing"]);
    with_context(data, |ctx| {
        ctx.result.has_seen_analytical_gates = Some(true);
        ctx.nested_count = 299;
        // Enter wrapper at depth 300, then fail its analytical child at 301.
        assert!(Evaluator::evaluate(ctx, "probe", &SpecType::Gate).is_err());
        assert_eq!(ctx.result.has_seen_analytical_gates, Some(true));
        assert_eq!(ctx.nested_count, 299);
        assert!(ctx.nested_gate_memo.is_empty());
    });
}

#[test]
fn unsupported_children_are_not_memoized_and_keep_parent_analytics() {
    let mut data = fixture();
    data["feature_gates"]["numeric"]["rules"][0]["conditions"] = json!(["missing"]);
    with_context(data, |ctx| {
        for _ in 0..2 {
            ctx.reset_result();
            ctx.result.has_seen_analytical_gates = Some(true);
            evaluate(ctx, "probe");
            assert!(ctx.result.unsupported);
            assert_eq!(ctx.result.has_seen_analytical_gates, Some(true));
            assert!(ctx.nested_gate_memo.is_empty());
            assert_eq!(ctx.nested_count, 0);
        }
    });
}

#[test]
fn config_mapping_reset_is_replayed_even_when_the_mapped_override_does_not_finalize() {
    let mut data = fixture();
    data["override_rules"] = json!({"mapping": rule(&["public"], true, None)});
    data["overrides"] = json!({"numeric": [{
        "new_config_name": "mapped_child",
        "rules": [{"rule_name": "mapping", "start_time": 0}]
    }]});
    let adapter: Arc<dyn OverrideAdapter> = Arc::new(StatsigLocalOverrideAdapter::new());
    adapter.override_gate("mapped_child", true, None);
    with_override_context(data, Some(adapter), |ctx| {
        ctx.result.sampling_rate = Some(17);
        ctx.result.forward_all_exposures = Some(true);
        evaluate(ctx, "probe");
        let cold = snapshot(ctx);
        assert_eq!(cold["rate"], Value::Null);
        assert_eq!(cold["forward"], Value::Null);
        assert_eq!(cold["analytical"], json!(true));
        ctx.reset_result();
        ctx.result.sampling_rate = Some(201);
        ctx.result.forward_all_exposures = Some(false);
        evaluate(ctx, "probe");
        assert_eq!(snapshot(ctx), cold);
    });
}

#[test]
fn cached_forward_all_exposures_metadata_matches_cold_evaluation() {
    let mut data = fixture();
    data["feature_gates"]["numeric"]["forwardAllExposures"] = json!(true);
    data["feature_gates"]["segment:none"]["forwardAllExposures"] = json!(false);
    with_context(data, |ctx| {
        evaluate(ctx, "probe");
        let cold = snapshot(ctx);
        assert_eq!(cold["forward"], json!(true));
        ctx.reset_result();
        evaluate(ctx, "segment:none");
        evaluate(ctx, "probe");
        assert_eq!(snapshot(ctx), cold);
    });
}

#[test]
fn cached_default_disabled_and_segment_gates_keep_sampling_exceptions() {
    for (name, entity, enabled, forward, analytical, rule_id, exposure_count) in [
        ("child", "feature_gate", true, false, false, "default", 1),
        ("child", "feature_gate", false, false, false, "disabled", 1),
        ("child", "feature_gate", true, true, true, "default", 1),
        ("child", "holdout", true, false, true, "default", 1),
        ("child", "segment", true, false, true, "default", 1),
        ("segment:child", "segment", true, false, false, "default", 0),
    ] {
        let mut data = fixture();
        let mut child = gate(entity, vec![]);
        child["enabled"] = json!(enabled);
        child["forwardAllExposures"] = json!(forward);
        data["feature_gates"][name] = child;
        data["condition_map"]["pass_child"] = condition("pass_gate", json!(name));
        data["feature_gates"]["probe"]["rules"][0]["conditions"] = json!(["pass_child", "missing"]);
        with_context(data, |ctx| {
            evaluate(ctx, "probe");
            let cold = snapshot(ctx);
            assert_eq!(cold["rule"], json!(rule_id), "{name}/{entity}");
            assert_eq!(cold["analytical"], json!(analytical), "{name}/{entity}");
            assert_eq!(ctx.result.secondary_exposures.len(), exposure_count);
            ctx.reset_result();
            evaluate(ctx, "numeric");
            evaluate(ctx, "probe");
            assert_eq!(snapshot(ctx), cold, "{name}/{entity}/{enabled}/{forward}");
        });
    }
}

#[test]
fn cached_pass_and_fail_gate_conditions_preserve_boolean_and_exposures() {
    for value in [false, true] {
        for kind in ["pass_gate", "fail_gate"] {
            let mut data = fixture();
            data["feature_gates"]["numeric"]["rules"][0]["returnValue"] = json!(value);
            data["condition_map"]["pass_numeric"] = condition(kind, json!("numeric"));
            with_context(data, |ctx| {
                evaluate(ctx, "probe");
                let cold = snapshot(ctx);
                assert_eq!(cold["value"], json!(value ^ (kind == "fail_gate")));
                assert_eq!(cold["exposures"][0]["gateValue"], json!(value.to_string()));
                ctx.reset_result();
                evaluate(ctx, "segment:none");
                evaluate(ctx, "probe");
                assert_eq!(snapshot(ctx), cold, "{kind}/{value}");
            });
        }
    }
}

struct SamplingExposure {
    key: ExposureSamplingKey,
    info: ExtraExposureInfo,
}

impl EnqueueOperation for SamplingExposure {
    fn as_exposure(&self) -> Option<&impl QueuedExposure<'_>> {
        Some(self)
    }
    fn into_queued_event(self, _: EvtSamplingDecision) -> QueuedEvent {
        unreachable!("this test only asks for sampling decisions")
    }
}

impl<'a> QueuedExposure<'a> for SamplingExposure {
    fn create_exposure_sampling_key(&self) -> ExposureSamplingKey {
        self.key.clone()
    }
    fn get_rule_id_ref(&'a self) -> &'a str {
        "rule"
    }
    fn get_extra_exposure_info_ref(&'a self) -> Option<&'a ExtraExposureInfo> {
        Some(&self.info)
    }
}

fn sampler(mode: &str) -> ExposureSampling {
    let id = format!("sampling-memo-{}", uuid::Uuid::new_v4());
    let configs = GlobalConfigs::get_instance(&id);
    configs.set_sdk_configs(HashMap::from([
        ("sampling_mode".to_owned(), DynamicValue::from_string(mode)),
        (
            "special_case_sampling_rate".to_owned(),
            DynamicValue::from_i64(101),
        ),
    ]));
    ExposureSampling::new(&id)
}

fn exposure(info: ExtraExposureInfo, user_hash: u64) -> SamplingExposure {
    SamplingExposure {
        key: ExposureSamplingKey {
            spec_name_hash: 123,
            rule_id_hash: 456,
            user_values_hash: user_hash,
            additional_hash: 0,
        },
        info,
    }
}

#[test]
fn cached_numeric_metadata_preserves_on_and_shadow_sampling_decisions() {
    let mut data = fixture();
    data["feature_gates"]["numeric"]["forwardAllExposures"] = json!(true);
    data["feature_gates"]["parent"]["forwardAllExposures"] = json!(false);
    with_context(data, |ctx| {
        evaluate(ctx, "parent");
        let cold = result_to_extra_exposure_info(&ctx.result);
        assert_eq!(cold.sampling_rate, Some(201));
        assert_eq!(cold.forward_all_exposures, Some(false));
        ctx.reset_result();
        evaluate(ctx, "segment:none");
        evaluate(ctx, "parent");
        let warm = result_to_extra_exposure_info(&ctx.result);

        for mode in ["on", "shadow"] {
            let sampler = sampler(mode);
            let first = exposure(cold.clone(), 10_000);
            assert!(matches!(
                sampler.get_sampling_decision(&first, false),
                EvtSamplingDecision::ForceSampled
            ));
            assert!(matches!(
                sampler.get_sampling_decision(&first, false),
                EvtSamplingDecision::Deduped
            ));
            // Both keys deliberately miss the same numeric sampling bucket.
            for info in [&cold, &warm] {
                let payload = exposure(info.clone(), if std::ptr::eq(info, &cold) { 1 } else { 2 });
                assert!(!payload.key.is_sampled(Some(201)));
                let decision = sampler.get_sampling_decision(&payload, false);
                match mode {
                    "on" => assert!(
                        matches!(decision, EvtSamplingDecision::NotSampled),
                        "{decision:?}"
                    ),
                    _ => assert!(
                        matches!(
                            decision,
                            EvtSamplingDecision::Sampled(Some(201), EvtSamplingMode::Shadow, false)
                        ),
                        "{decision:?}"
                    ),
                }
            }
        }
    });
}

#[test]
fn cached_analytical_descendant_forces_sampling_and_as_primary_can_bypass_it() {
    let mut data = fixture();
    data["feature_gates"]["parent"]["rules"][0]["conditions"] = json!(["pass_wrapper"]);
    with_context(data, |ctx| {
        evaluate(ctx, "parent");
        ctx.reset_result();
        evaluate(ctx, "numeric");
        ctx.result.secondary_exposures.clear();
        evaluate(ctx, "parent");
        let info = result_to_extra_exposure_info(&ctx.result);
        let sampler = sampler("on");
        let payload = exposure(info.clone(), 10_000);
        assert!(matches!(
            sampler.get_sampling_decision(&payload, true),
            EvtSamplingDecision::ForceSampled
        ));
        assert!(matches!(
            sampler.get_sampling_decision(&exposure(info.clone(), 1), false),
            EvtSamplingDecision::ForceSampled
        ));
        assert!(matches!(
            sampler.get_sampling_decision(&exposure(info, 2), true),
            EvtSamplingDecision::NotSampled
        ));
    });
}
