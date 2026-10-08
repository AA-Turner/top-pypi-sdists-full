use ahash::AHashSet;
use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};

use crate::{
    DynamicValue,
    evaluation::{
        comparisons::compare_arrays,
        evaluator_value::{
            EvaluatorValue, EvaluatorValueInner, EvaluatorValueRef, EvaluatorValueType,
            MemoizedEvaluatorValue,
        },
    },
    hashing::ahash_str,
    interned_values::interned_store::{preload_mmap_v2_for_test, write_mmap_v2_for_test},
    specs_response::spec_types::ConditionOperator,
    user::user_value::{UserValue, UserValueRef},
};

// Expected membership results are ordered all, any, none, not-all.
const OPS: [ConditionOperator; 4] = [
    ConditionOperator::ArrayContainsAll,
    ConditionOperator::ArrayContainsAny,
    ConditionOperator::ArrayContainsNone,
    ConditionOperator::NotArrayContainsAll,
];

struct Case {
    name: String,
    input: Option<Value>,
    target: Value,
    membership: Option<[bool; 4]>,
    equal: Option<bool>,
}

fn case(
    name: impl Into<String>,
    input: Option<Value>,
    target: Value,
    membership: Option<[bool; 4]>,
    equal: Option<bool>,
) -> Case {
    Case {
        name: name.into(),
        input,
        target,
        membership,
        equal,
    }
}

fn quantified(all: bool, any: bool) -> [bool; 4] {
    [all, any, !any, !all]
}

fn strings_in_one_scratch_bucket(bucket_count: usize, count: usize) -> Vec<String> {
    let mut buckets: Vec<Vec<(u64, String)>> = (0..bucket_count).map(|_| Vec::new()).collect();
    for index in 0..bucket_count * count * 4 {
        // Lowercase ASCII keeps these distinct after target normalization.
        let value = format!("c{index:x}");
        let hash = ahash_str(&value);
        let bucket = &mut buckets[(hash & (bucket_count - 1) as u64) as usize];
        if bucket
            .iter()
            .any(|(previous_hash, _)| *previous_hash == hash)
        {
            continue;
        }
        bucket.push((hash, value));
        if bucket.len() == count {
            return bucket.iter().map(|(_, value)| value.clone()).collect();
        }
    }
    panic!("could not construct distinct full hashes sharing one scratch bucket");
}

fn cases() -> Vec<Case> {
    let mut cases = Vec::new();
    for (name, input, target, all, any, equal) in [
        ("empty arrays", json!([]), json!([]), true, false, true),
        ("empty input", json!([]), json!(["a"]), false, false, false),
        ("empty target", json!(["a"]), json!([]), true, false, false),
        (
            "singleton hit",
            json!(["a"]),
            json!(["a"]),
            true,
            true,
            true,
        ),
        (
            "singleton miss",
            json!(["z"]),
            json!(["a"]),
            false,
            false,
            false,
        ),
        (
            "partial match",
            json!(["a"]),
            json!(["a", "b"]),
            false,
            true,
            false,
        ),
        (
            "superset",
            json!(["a", "b", "c"]),
            json!(["a", "b"]),
            true,
            true,
            false,
        ),
        (
            "equality preserves order",
            json!(["b", "a"]),
            json!(["a", "b"]),
            true,
            true,
            false,
        ),
        (
            "duplicates in input",
            json!(["a", "a"]),
            json!(["a"]),
            true,
            true,
            false,
        ),
        (
            "target duplicate retains original index",
            json!(["a"]),
            json!(["a", "a"]),
            true,
            true,
            false,
        ),
        (
            "equal raw duplicates are not evaluator equality",
            json!(["a", "a"]),
            json!(["a", "a"]),
            true,
            true,
            false,
        ),
        (
            "target indices must not be compacted",
            json!(["a", "b"]),
            json!(["a", "a", "b"]),
            true,
            true,
            false,
        ),
        (
            "last target index is retained",
            json!(["a", "b"]),
            json!(["a", "b", "a"]),
            true,
            true,
            false,
        ),
        (
            "earlier case spelling is discarded",
            json!(["Foo"]),
            json!(["Foo", "foo"]),
            false,
            false,
            false,
        ),
        (
            "last spelling but original index",
            json!(["foo"]),
            json!(["Foo", "foo"]),
            true,
            true,
            false,
        ),
        (
            "case collision reversed",
            json!(["Foo"]),
            json!(["foo", "Foo"]),
            true,
            true,
            false,
        ),
        (
            "exact case required",
            json!(["foo"]),
            json!(["Foo"]),
            false,
            false,
            false,
        ),
        (
            "number and bool coercions",
            json!([1, true, false, 3.25]),
            json!(["1", "true", "false", "3.25"]),
            true,
            true,
            true,
        ),
        (
            "input integral float normalizes",
            json!([1.0]),
            json!(["1"]),
            true,
            true,
            true,
        ),
        (
            "target integral float keeps JSON spelling",
            json!([1]),
            json!([1.0]),
            false,
            false,
            false,
        ),
        (
            "numeric string target",
            json!(["1.0"]),
            json!([1.0]),
            true,
            true,
            true,
        ),
        (
            "null item defaults to empty only for membership",
            json!([null]),
            json!([""]),
            true,
            true,
            false,
        ),
        (
            "object item defaults to empty only for membership",
            json!([{}]),
            json!([""]),
            true,
            true,
            false,
        ),
        (
            "null target item is literal text",
            json!([null]),
            json!([null]),
            false,
            false,
            false,
        ),
        (
            "null text matches target coercion",
            json!(["null"]),
            json!([null]),
            true,
            true,
            true,
        ),
        (
            "object input does not serialize for matching",
            json!([{"k": 1}]),
            json!([{"k": 1}]),
            false,
            false,
            false,
        ),
        (
            "object text matches target coercion",
            json!(["{\"k\":1}"]),
            json!([{"k": 1}]),
            true,
            true,
            true,
        ),
        (
            "nested arrays serialize",
            json!([["A", 1]]),
            json!([["A", 1]]),
            true,
            true,
            true,
        ),
        (
            "nested array case remains significant",
            json!([["a", 1]]),
            json!([["A", 1]]),
            false,
            false,
            false,
        ),
        (
            "empty nested arrays",
            json!([[]]),
            json!([[]]),
            true,
            true,
            true,
        ),
        (
            "embedded NUL",
            json!(["x\u{0}Y"]),
            json!(["x\u{0}Y"]),
            true,
            true,
            true,
        ),
    ] {
        cases.push(case(
            name,
            Some(input),
            target,
            Some(quantified(all, any)),
            Some(equal),
        ));
    }

    // Invalid operands return false for every membership operator, including the
    // negative operators. They are not the complement of a failed type check.
    for input in [
        None,
        Some(json!(null)),
        Some(json!(true)),
        Some(json!(7)),
        Some(json!("a")),
        Some(json!({"a": 1})),
    ] {
        for target in [json!([]), json!(["a"])] {
            cases.push(case(
                "missing or non-array input",
                input.clone(),
                target,
                Some([false; 4]),
                Some(false),
            ));
        }
    }
    for target in [
        json!(null),
        json!(true),
        json!(7),
        json!("a"),
        json!({}),
        json!({"a": 1}),
    ] {
        for input in [json!([]), json!(["a"])] {
            cases.push(case(
                "non-array target",
                Some(input),
                target.clone(),
                Some([false; 4]),
                Some(false),
            ));
        }
    }

    // These collide under Unicode lowercase, but membership must use the last
    // original spelling. Include contextual sigma and mixed ASCII/Unicode keys.
    for (upper, lower) in [
        ("É", "é"),
        ("İ", "i\u{307}"),
        ("K", "k"),
        ("Σ", "σ"),
        ("ΟΣ", "ος"),
        ("AÉ", "aé"),
        ("aÉ", "aé"),
        ("Aİ", "ai\u{307}"),
        ("aİ", "ai\u{307}"),
        ("AΣ", "aς"),
        ("aΣ", "aς"),
    ] {
        for (input, target, hit, equal) in [
            (upper, json!([upper]), true, true),
            (lower, json!([upper]), false, false),
            (upper, json!([upper, lower]), false, false),
            (lower, json!([upper, lower]), true, false),
            (upper, json!([lower, upper]), true, false),
            (lower, json!([lower, upper]), false, false),
        ] {
            let mut indexed_target = target.as_array().unwrap().clone();
            // Sixteen distinct target keys put a one-item Unicode input on the
            // indexed any/none path under the whole-array ratio check.
            indexed_target.extend((0..15).map(|i| json!(format!("array-test-filler-{i}"))));
            cases.push(case(
                "Unicode exact spelling and collision indices",
                Some(json!([input])),
                target,
                Some(quantified(hit, hit)),
                Some(equal),
            ));
            cases.push(case(
                "Unicode membership through the target index",
                Some(json!([input])),
                json!(indexed_target),
                Some(quantified(false, hit)),
                Some(false),
            ));
        }
    }

    // Cover just below, exactly at, and above 16 targets per input item.
    // The path decision uses the whole input length; the matching numeric or
    // Unicode item can be first, in the middle, or after ASCII-only misses.
    for (kind, probe, matching_target, missing_target) in [
        ("integer", json!(42), json!("42"), json!("42.0")),
        ("integral float", json!(1.0), json!("1"), json!(1.0)),
        ("contextual sigma", json!("ΟΣ"), json!("ΟΣ"), json!("ος")),
        (
            "mixed ASCII and sigma",
            json!("aΣ"),
            json!("aΣ"),
            json!("aς"),
        ),
    ] {
        for input_len in [3, 16] {
            for probe_index in [0, input_len / 2, input_len - 1] {
                for target_len in [
                    input_len,
                    input_len * 16 - 1,
                    input_len * 16,
                    input_len * 16 + 1,
                ] {
                    for hit in [false, true] {
                        let mut input: Vec<_> = (0..input_len)
                            .map(|i| json!(format!("ascii-probe-miss-{i}")))
                            .collect();
                        input[probe_index] = probe.clone();
                        let mut target = vec![if hit {
                            matching_target.clone()
                        } else {
                            missing_target.clone()
                        }];
                        target.extend(
                            (1..target_len).map(|i| json!(format!("adaptive-target-filler-{i}"))),
                        );
                        cases.push(case(
                            format!("ratio {kind}: {input_len}/{target_len}, probe at {probe_index}, hit={hit}"),
                            Some(json!(input)),
                            json!(target),
                            Some(quantified(false, hit)),
                            Some(false),
                        ));
                    }
                }
            }

            // Either ordering must find the ASCII hit, on both the indexed and
            // scratch/set paths. No partially scanned input can be discarded.
            for target_len in [input_len, input_len * 16] {
                for hit_before_probe in [false, true] {
                    let mut input: Vec<_> = (0..input_len)
                        .map(|i| json!(format!("ascii-probe-miss-{i}")))
                        .collect();
                    let (hit_index, probe_index) = if hit_before_probe {
                        (0, input_len - 1)
                    } else {
                        (input_len - 1, 0)
                    };
                    input[hit_index] = json!("early-ascii-hit");
                    input[probe_index] = probe.clone();
                    let mut target = vec![json!("early-ascii-hit")];
                    target.extend(
                        (1..target_len).map(|i| json!(format!("adaptive-target-filler-{i}"))),
                    );
                    cases.push(case(
                        format!("ratio {kind}: {input_len}/{target_len}, ASCII hit before probe={hit_before_probe}"),
                        Some(json!(input)),
                        json!(target),
                        Some(quantified(false, true)),
                        Some(false),
                    ));
                }
            }
        }
    }

    for input in [json!([null]), json!([{}])] {
        cases.push(case(
            "empty-string default in a short target",
            Some(input),
            json!(["", "array-test-filler-one", "array-test-filler-two"]),
            Some(quantified(false, true)),
            Some(false),
        ));
    }

    // Focused short-list cases. Keep coercion and original-index
    // semantics explicit at normalized target sizes 3/4/5 rather than expanding
    // every fixture across another size matrix.
    for len in [3, 4, 5] {
        let numbers: Vec<_> = (0..len).map(|i| json!(i)).collect();
        let numeric_targets: Vec<_> = (0..len).map(|i| json!(i.to_string())).collect();
        let absent_numbers: Vec<_> = (len..len * 2).map(|i| json!(i)).collect();
        let unicode = ["ΟΣ", "İ", "É", "Σ", "aΣ"];
        let unicode_targets: Vec<_> = unicode[..len].iter().map(|value| json!(value)).collect();
        let absent_unicode: Vec<_> = unicode[..len]
            .iter()
            .map(|value| json!(value.to_lowercase()))
            .collect();
        for (name, input, target, hit) in [
            (
                "numeric exact match",
                numbers,
                numeric_targets.clone(),
                true,
            ),
            ("numeric disjoint", absent_numbers, numeric_targets, false),
            (
                "Unicode exact match",
                unicode_targets.clone(),
                unicode_targets.clone(),
                true,
            ),
            (
                "Unicode spelling mismatch",
                absent_unicode,
                unicode_targets,
                false,
            ),
        ] {
            cases.push(case(
                format!("tiny boundary {len}: {name}"),
                Some(json!(input)),
                json!(target),
                Some(quantified(hit, hit)),
                Some(hit),
            ));
        }

        for empty_item in [json!(null), json!({})] {
            let mut input = vec![empty_item];
            let mut target = vec![json!("")];
            for index in 1..len {
                let filler = json!(format!("shared-empty-filler-{index}"));
                input.push(filler.clone());
                target.push(filler);
            }
            cases.push(case(
                format!("tiny boundary {len}: membership defaults absent string to empty"),
                Some(json!(input)),
                json!(target),
                Some(quantified(true, true)),
                // Equality must still compare None against Some("").
                Some(false),
            ));
        }

        let mixed_input = [
            json!(1),
            json!(true),
            json!(["A", 1]),
            json!("ΟΣ"),
            json!(null),
        ];
        let mixed_target = [
            json!("1"),
            json!(true),
            json!(["A", 1]),
            json!("ΟΣ"),
            json!(""),
        ];
        cases.push(case(
            format!("tiny boundary {len}: mixed coercions"),
            Some(json!(mixed_input[..len])),
            json!(mixed_target[..len]),
            Some(quantified(true, true)),
            Some(len < 5),
        ));

        // The raw target has len+1 entries but only len retained keys. A raw
        // cardinality shortcut would reject the surviving spelling incorrectly.
        let mut collision_target = vec![json!("Foo"), json!("foo")];
        collision_target.extend((1..len).map(|i| json!(format!("collision-filler-{i}"))));
        for (spelling, all) in [("foo", true), ("Foo", false)] {
            let mut input = vec![json!(spelling)];
            input.extend((1..len).map(|i| json!(format!("collision-filler-{i}"))));
            cases.push(case(
                format!("tiny boundary {len}: last spelling {spelling}, uncompressed indices"),
                Some(json!(input)),
                json!(collision_target),
                Some(quantified(all, true)),
                Some(false),
            ));
        }

        for (name, probe, retained) in [
            ("numeric", json!(42), json!("42")),
            ("Unicode", json!("ΟΣ"), json!("ΟΣ")),
            ("default empty", json!(null), json!("")),
        ] {
            let mut target = vec![retained];
            target.extend((1..len).map(|i| json!(format!("singleton-filler-{i}"))));
            cases.push(case(
                format!("tiny boundary {len}: singleton user {name}, any but not all"),
                Some(json!([probe])),
                json!(target),
                Some(quantified(false, true)),
                Some(false),
            ));
        }
    }

    for (name, input, target, all) in [
        (
            "more target keys than duplicate user entries",
            json!(["a", "a", "a", "a"]),
            json!(["a", "b", "c", "d", "e"]),
            false,
        ),
        (
            "equal raw lengths do not prove all with duplicate user entries",
            json!(["a", "a", "a", "a"]),
            json!(["a", "b", "c", "d"]),
            false,
        ),
        (
            "raw target larger but normalized target singleton",
            json!(["a", "a", "a", "a"]),
            json!(["a", "a", "a", "a", "a"]),
            true,
        ),
    ] {
        cases.push(case(
            name,
            Some(input),
            target,
            Some(quantified(all, true)),
            Some(false),
        ));
    }

    // Mixed-key short lists must find a last-item hit after ASCII-only misses,
    // or reject a numeric/Unicode spelling mismatch.
    for (input_len, target_len, unicode, hit) in [
        (3, 15, false, true),
        (4, 16, true, false),
        (4, 17, false, false),
        (5, 15, true, true),
        (5, 16, false, false),
        (3, 17, true, true),
    ] {
        let mut input: Vec<_> = (0..input_len - 1)
            .map(|i| json!(format!("bounded-scan-ascii-miss-{i}")))
            .collect();
        input.push(if unicode { json!("ΟΣ") } else { json!(42) });
        let retained = match (unicode, hit) {
            (true, true) => json!("ΟΣ"),
            (true, false) => json!("ος"),
            (false, true) => json!("42"),
            (false, false) => json!("42.0"),
        };
        let mut target = vec![retained];
        target.extend((1..target_len).map(|i| json!(format!("bounded-scan-target-filler-{i}"))));
        cases.push(case(
            format!(
                "mixed short array {input_len}/{target_len}, late Unicode={unicode}, hit={hit}"
            ),
            Some(json!(input)),
            json!(target),
            Some(quantified(false, hit)),
            Some(false),
        ));
    }

    // Check the small and medium scratch-buffer cutoffs independently, including
    // cases just below, at, and above each medium limit. Null/object input items
    // default to empty for membership;
    // a null target item instead represents the literal string "null".
    for (input_len, target_len) in [
        (16, 32),
        (17, 32),
        (16, 33),
        (63, 127),
        (64, 128),
        (65, 128),
        (64, 129),
    ] {
        for (name, retained, hit) in [
            ("Unicode exact hit", json!("ΟΣ"), true),
            ("Unicode case miss", json!("ος"), false),
            ("missing-item empty-string hit", json!(""), true),
            ("missing item is not null text", json!(null), false),
        ] {
            let mut input = vec![json!(null), json!({})];
            input.extend((2..input_len - 1).map(|i| json!(format!("scratch-input-miss-{i}"))));
            input.push(json!("ΟΣ"));
            let mut target = vec![retained];
            target.extend((1..target_len).map(|i| json!(format!("scratch-target-filler-{i}"))));
            cases.push(case(
                format!("scratch cutoff {input_len}/{target_len}: {name}"),
                Some(json!(input)),
                json!(target),
                Some(quantified(false, hit)),
                Some(false),
            ));
        }
    }

    // U=16 or 64/T=2 routes through each scratch buffer for all four operators. Force
    // bucket collisions with different full hashes, so finding a late exact hit
    // requires advancing past mismatching candidates rather than trusting a bit.
    for (user_count, bucket_count) in [(16, 32), (64, 128)] {
        let colliding = strings_in_one_scratch_bucket(bucket_count, user_count + 2);
        let distinct_users = colliding[..user_count].to_vec();
        let last = user_count - 1;
        let mut duplicates_with_late_hit = vec![colliding[0].clone(); last];
        duplicates_with_late_hit.push(colliding[last].clone());
        for (name, input, target, all, any) in [
            (
                "colliding bucket hit at highest user position",
                distinct_users.clone(),
                vec![colliding[user_count].clone(), colliding[last].clone()],
                false,
                true,
            ),
            (
                "colliding bucket without an exact match",
                distinct_users.clone(),
                vec![
                    colliding[user_count].clone(),
                    colliding[user_count + 1].clone(),
                ],
                false,
                false,
            ),
            (
                "colliding bucket all includes highest user position",
                distinct_users,
                vec![colliding[0].clone(), colliding[last].clone()],
                true,
                true,
            ),
            (
                "duplicate positions retain the distinct hit at highest position",
                duplicates_with_late_hit,
                vec![colliding[0].clone(), colliding[last].clone()],
                true,
                true,
            ),
            (
                "all duplicate positions do not satisfy a colliding missing value",
                vec![colliding[0].clone(); user_count],
                vec![colliding[0].clone(), colliding[user_count + 1].clone()],
                false,
                true,
            ),
        ] {
            cases.push(case(
                format!("scratch {user_count} users: {name}"),
                Some(json!(input)),
                json!(target),
                Some(quantified(all, any)),
                Some(false),
            ));
        }
    }

    // Cardinality and helper selection use normalized target length, while
    // equality retains original indices. Duplicate input positions still count
    // toward the scratch buffer's capacity even when their values are identical.
    let retained: Vec<_> = (0..64).map(|i| format!("normalized-value-{i}")).collect();
    let duplicated_target: Vec<_> = retained
        .iter()
        .flat_map(|value| [value.to_uppercase(), value.clone()])
        .collect();
    for duplicate_input in [false, true] {
        let mut input = retained.clone();
        if duplicate_input {
            input.push(retained[0].clone());
        }
        cases.push(case(
            format!("medium normalized target 64/raw 128, input duplicate={duplicate_input}"),
            Some(json!(input)),
            json!(duplicated_target),
            Some(quantified(true, true)),
            Some(false),
        ));
    }
    let mut raw_129_target = vec![json!("NORMALIZED-VALUE-0")];
    raw_129_target.extend((0..128).map(|i| json!(format!("normalized-value-{i}"))));
    cases.push(case(
        "medium normalized target 128/raw 129 preserves last spelling",
        Some(json!(retained)),
        json!(raw_129_target),
        Some(quantified(false, true)),
        Some(false),
    ));

    // Exercise both traversal directions, empty/singleton paths, bounded scratch
    // buffers and larger set-based fallbacks. Expected results use the construction
    // of these unique lists, independently of evaluator lookup helpers.
    for input_len in [0, 1, 2, 3, 4, 7, 8, 9, 16, 32, 64, 128] {
        for target_len in [0, 1, 2, 3, 4, 7, 8, 9, 16, 32, 64, 128] {
            let target: Vec<_> = (0..target_len)
                .map(|i| json!(format!("target-{i}")))
                .collect();
            for mode in ["prefix", "miss", "duplicates"] {
                let input: Vec<_> = (0..input_len)
                    .map(|i| match mode {
                        "prefix" => json!(format!("target-{i}")),
                        "duplicates" => json!("target-0"),
                        _ => json!(format!("absent-{i}")),
                    })
                    .collect();
                let any = mode != "miss" && input_len > 0 && target_len > 0;
                let all = target_len == 0
                    || match mode {
                        "prefix" => input_len >= target_len,
                        "duplicates" => target_len == 1 && input_len > 0,
                        _ => false,
                    };
                let equal = input_len == target_len
                    && (input_len == 0
                        || mode == "prefix"
                        || (mode == "duplicates" && input_len == 1));
                cases.push(case(
                    format!("sizes {input_len}/{target_len}, {mode}"),
                    Some(json!(input)),
                    json!(target),
                    Some(quantified(all, any)),
                    Some(equal),
                ));
            }
        }
    }

    // A reproducible mixed-type corpus catches interactions between coercion,
    // duplicate normalization and index preservation, without a new dependency.
    let pool = [
        json!(null),
        json!(""),
        json!(true),
        json!(false),
        json!(1),
        json!(1.0),
        json!(3.25),
        json!("Foo"),
        json!("foo"),
        json!("ΟΣ"),
        json!("ος"),
        json!("aΣ"),
        json!("aς"),
        json!({}),
        json!({"k": 1}),
        json!([]),
        json!(["A", 1]),
    ];
    let mut seed = 0x71_0a_22_a9_u64;
    for index in 0..192 {
        let mut next = || {
            seed = seed.wrapping_mul(6_364_136_223_846_793_005).wrapping_add(1);
            (seed >> 32) as usize
        };
        let left_len = next() % 13;
        let right_len = next() % 13;
        let input: Vec<_> = (0..left_len)
            .map(|_| pool[next() % pool.len()].clone())
            .collect();
        let target: Vec<_> = (0..right_len)
            .map(|_| pool[next() % pool.len()].clone())
            .collect();
        cases.push(case(
            format!("generated mixed-type case {index}"),
            Some(json!(input)),
            json!(target),
            None,
            None,
        ));
    }
    cases
}

// Deliberately retain the pre-optimization set-and-target-scan algorithm. This
// oracle must not call any new membership or traversal-direction helper.
fn legacy_membership(
    input: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    op: ConditionOperator,
) -> bool {
    if target.array_len().is_none() {
        return false;
    }
    let Some(len) = input.array_len() else {
        return false;
    };
    let values: AHashSet<&str> = AHashSet::from_iter((0..len).map(|index| {
        input
            .array_item(index)
            .and_then(UserValueRef::string_value)
            .unwrap_or_default()
    }));
    let short_circuit = target.any_array_string(false, |item| match op {
        ConditionOperator::ArrayContainsAll | ConditionOperator::NotArrayContainsAll => {
            !values.contains(item)
        }
        ConditionOperator::ArrayContainsAny | ConditionOperator::ArrayContainsNone => {
            values.contains(item)
        }
        _ => true,
    });
    match op {
        ConditionOperator::ArrayContainsAll | ConditionOperator::ArrayContainsNone => {
            !short_circuit
        }
        ConditionOperator::ArrayContainsAny | ConditionOperator::NotArrayContainsAll => {
            short_circuit
        }
        _ => false,
    }
}

// Read the pre-existing materialized representation directly. In particular,
// this does not reuse the new iterator and does not compact duplicate indices.
fn legacy_equality(target: &MemoizedEvaluatorValue, input: UserValueRef<'_>) -> bool {
    match target.value_type {
        EvaluatorValueType::Null => input.is_null(),
        EvaluatorValueType::Bool => target.bool_value == input.bool_value(),
        EvaluatorValueType::Number => target.float_value == input.float_value(),
        EvaluatorValueType::String => {
            target
                .string_value
                .as_ref()
                .map(|value| value.value.as_str())
                == input.string_value()
        }
        EvaluatorValueType::Array => match (&target.array_value, input.array_len()) {
            (None, None) => true,
            (Some(array), Some(len)) if array.len() == len => {
                array.values().all(|(index, expected)| {
                    input
                        .array_item(*index)
                        .and_then(UserValueRef::string_value)
                        == Some(expected.as_str())
                })
            }
            _ => false,
        },
        EvaluatorValueType::Object => match (&target.object_value, input.object_len()) {
            (None, None) => true,
            (Some(object), Some(len)) if object.len() == len => {
                object.iter().all(|(key, expected)| {
                    input
                        .object_get(key.as_str())
                        .and_then(UserValueRef::string_value)
                        == Some(expected.value.as_str())
                })
            }
            _ => false,
        },
    }
}

fn assert_case(
    case: &Case,
    target: EvaluatorValueRef<'_>,
    materialized: &MemoizedEvaluatorValue,
    storage: &str,
) {
    let dynamic = case
        .input
        .clone()
        .map(DynamicValue::from_json_value)
        .unwrap_or_default();
    let user = case
        .input
        .clone()
        .map(UserValue::from_json_value)
        .unwrap_or_default();
    for (representation, input) in [
        ("DynamicValue", UserValueRef::Dynamic(&dynamic)),
        ("UserValue", UserValueRef::User(&user)),
    ] {
        for (index, op) in OPS.into_iter().enumerate() {
            let expected = legacy_membership(input, target, op);
            if let Some(explicit) = case.membership {
                assert_eq!(
                    expected, explicit[index],
                    "legacy membership: {}, {representation}, {storage}, {op:?}, input={:?}, target={:?}",
                    case.name, case.input, case.target
                );
            }
            assert_eq!(
                compare_arrays(input, target, op),
                expected,
                "membership: {}, {representation}, {storage}, {op:?}, input={:?}, target={:?}",
                case.name,
                case.input,
                case.target
            );
        }
        let expected = legacy_equality(materialized, input);
        if let Some(explicit) = case.equal {
            assert_eq!(
                expected, explicit,
                "legacy equality: {}, {representation}, {storage}, input={:?}, target={:?}",
                case.name, case.input, case.target
            );
        }
        let actual = target.is_equal_to_user_value(input);
        assert_eq!(
            actual, expected,
            "equality: {}, {representation}, {storage}, input={:?}, target={:?}",
            case.name, case.input, case.target
        );
    }
}

#[test]
fn array_optimizations_match_legacy_owned_semantics() {
    for case in cases() {
        let target = MemoizedEvaluatorValue::from(case.target.clone());
        assert_case(&case, (&target).into(), &target, "owned");
    }
}

#[test]
fn array_optimizations_preserve_missing_array_storage() {
    let target = MemoizedEvaluatorValue::new(EvaluatorValueType::Array);
    for input in [
        None,
        Some(json!(null)),
        Some(json!("a")),
        Some(json!({})),
        Some(json!([])),
        Some(json!(["a"])),
    ] {
        let equal = input.as_ref().is_none_or(|input| !input.is_array());
        let case = case(
            "array type with absent storage",
            input,
            json!(null),
            Some([false; 4]),
            Some(equal),
        );
        assert_case(&case, (&target).into(), &target, "owned missing array");
    }
}

rusty_fork_test! {
    #[test]
    fn array_optimizations_match_legacy_mmap_semantics() {
        // Preload changes global interned state, so use the established fork
        // harness. Null values use the shared singleton instead of mmap storage.
        let cases: Vec<_> = cases().into_iter().filter(|case| !case.target.is_null()).collect();
        let conditions: serde_json::Map<_, _> = cases.iter().enumerate().map(|(index, case)| {
            (index.to_string(), json!({
                "type": "user_field", "targetValue": case.target,
                "operator": "array_contains_any", "field": "custom",
                "additionalValues": {}, "idType": "userID"
            }))
        }).collect();
        let payload = serde_json::to_vec(&json!({
            "condition_map": conditions, "feature_gates": {}, "dynamic_configs": {},
            "layer_configs": {}, "experiment_to_layer": {}, "has_updates": true, "time": 1
        })).unwrap();
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("array-optimizations.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        for case in cases {
            let target = EvaluatorValue::from_json_value(case.target.clone());
            assert!(matches!(target.inner, EvaluatorValueInner::Mmap(_)), "target={:?}", case.target);
            // Materialization supplies the old owned-map oracle while actual
            // comparisons still use the original, asserted mmap representation.
            assert_case(&case, target.as_value_ref(), target.as_ref(), "mmap");
            assert!(matches!(target.inner, EvaluatorValueInner::Mmap(_)));
        }
    }
}
