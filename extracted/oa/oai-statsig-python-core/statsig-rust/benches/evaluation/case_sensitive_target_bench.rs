use crate::{
    DynamicValue,
    evaluation::{
        comparisons::{compare_case_sensitive_strings_in_array, compare_strings_in_array},
        evaluator_value::{EvaluatorValue, EvaluatorValueInner},
    },
    interned_values::interned_store::{preload_mmap_v2_for_test, write_mmap_v2_for_test},
    specs_response::spec_types::{Condition, ConditionOperator},
    user::user_value::{UserValue, UserValueRef},
};
use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};
use std::{hint::black_box, time::Instant};

fn condition(target: &Value, op: &str) -> Value {
    json!({"type":"user_field","field":"benchmark_field","targetValue":target,"operator":op,"idType":"userID"})
}

fn measure(
    input: UserValueRef<'_>,
    target: &EvaluatorValue,
    exact: bool,
    iterations: usize,
) -> f64 {
    let mut samples = Vec::new();
    for _ in 0..7 {
        let start = Instant::now();
        for _ in 0..iterations {
            let found = if exact {
                compare_case_sensitive_strings_in_array(
                    black_box(input),
                    black_box(target.as_value_ref()),
                    ConditionOperator::AnyCaseSensitive,
                )
            } else {
                compare_strings_in_array(
                    black_box(input),
                    black_box(target.as_value_ref()),
                    ConditionOperator::AnyCaseSensitive,
                )
            };
            black_box(found);
        }
        samples.push(start.elapsed().as_nanos() as f64 / iterations as f64);
    }
    samples.sort_by(f64::total_cmp);
    samples[3]
}

rusty_fork_test! {
    #[test]
    #[ignore = "run in release mode to compare exact membership with the legacy scan"]
    fn benchmark_exact_case_targets() {
        // Non-colliding targets keep both implementations correct. The `any`
        // fixture selects the normalized storage used by the legacy scan.
        let sizes = [1usize, 4, 5, 65, 9000];
        let targets: Vec<_> = sizes
            .iter()
            .map(|n| Value::Array((0..*n).map(|i| json!(format!("Target-{i}"))).collect()))
            .collect();
        let values: Vec<_> = targets
            .iter()
            .flat_map(|t| [condition(t, "any"), condition(t, "any_case_sensitive")])
            .collect();
        let owned: Vec<Condition> = values
            .iter()
            .cloned()
            .map(|c| serde_json::from_value(c).unwrap())
            .collect();
        let map: serde_json::Map<String, Value> = values
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, c)| (i.to_string(), c))
            .collect();
        let payload = serde_json::to_vec(&json!({
            "condition_map": map,
            "feature_gates": {},
            "dynamic_configs": {},
            "layer_configs": {},
            "experiment_to_layer": {},
            "has_updates": true,
            "time": 1
        }))
        .unwrap();
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("exact-target-bench.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();
        let mmap: Vec<Condition> = values
            .iter()
            .cloned()
            .map(|c| serde_json::from_value(c).unwrap())
            .collect();
        assert!(mmap.iter().all(|c| matches!(
            c.target_value.as_ref().unwrap().inner,
            EvaluatorValueInner::Mmap(_)
        )));
        println!("EXACT_BENCH,storage,size,representation,probe,legacy_ns,exact_ns");
        for (storage, conditions) in [("owned", &owned), ("mmap", &mmap)] {
            for (i, size) in sizes.iter().enumerate() {
                let legacy = conditions[2 * i].target_value.as_ref().unwrap();
                let exact = conditions[2 * i + 1].target_value.as_ref().unwrap();
                for (probe, input) in [
                    ("miss", json!("Missing")),
                    ("hit", json!(format!("Target-{}", size - 1))),
                ] {
                    let user = UserValue::from_json_value(input.clone());
                    let dynamic = DynamicValue::from_json_value(input);
                    for (representation, input) in [
                        ("user", UserValueRef::User(&user)),
                        ("dynamic", UserValueRef::Dynamic(&dynamic)),
                    ] {
                        let expected = probe == "hit";
                        assert_eq!(
                            compare_strings_in_array(
                                input,
                                legacy.as_value_ref(),
                                ConditionOperator::AnyCaseSensitive
                            ),
                            expected
                        );
                        assert_eq!(
                            compare_case_sensitive_strings_in_array(
                                input,
                                exact.as_value_ref(),
                                ConditionOperator::AnyCaseSensitive
                            ),
                            expected
                        );
                        let legacy_ns = measure(
                            input,
                            legacy,
                            false,
                            if *size == 9000 { 1000 } else { 100_000 },
                        );
                        let exact_ns = measure(input, exact, true, 100_000);
                        println!(
                            "EXACT_BENCH,{storage},{size},{representation},{probe},{legacy_ns:.2},{exact_ns:.2}"
                        );
                    }
                }
            }
        }
    }
}
