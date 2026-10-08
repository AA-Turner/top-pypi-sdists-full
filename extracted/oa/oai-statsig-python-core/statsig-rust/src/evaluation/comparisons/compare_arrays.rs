use crate::hashing::ahash_str;
use crate::{
    evaluation::evaluator_value::EvaluatorValueRef, specs_response::spec_types::ConditionOperator,
    unwrap_or_return, user::user_value::UserValueRef,
};
use ahash::AHashSet;

#[inline(always)]
pub(crate) fn compare_arrays<'a>(
    value: UserValueRef<'_>,
    target_value: impl Into<EvaluatorValueRef<'a>>,
    op: ConditionOperator,
) -> bool {
    let target_value = target_value.into();
    let target_len = unwrap_or_return!(target_value.array_len(), false);
    let value_len = unwrap_or_return!(value.array_len(), false);

    // Validate both operands before applying the quantifiers, including negation.
    if target_len == 0 {
        return matches!(
            op,
            ConditionOperator::ArrayContainsAll | ConditionOperator::ArrayContainsNone
        );
    }
    if value_len == 0 {
        return matches!(
            op,
            ConditionOperator::ArrayContainsNone | ConditionOperator::NotArrayContainsAll
        );
    }

    if target_len > value_len
        && matches!(
            op,
            ConditionOperator::ArrayContainsAll | ConditionOperator::NotArrayContainsAll
        )
    {
        // Normalized target entries have distinct original spellings.
        return matches!(op, ConditionOperator::NotArrayContainsAll);
    }

    // A single target needs no temporary user set, for either quantifier.
    if target_len == 1 {
        let found = target_value.any_array_string(false, |target| {
            (0..value_len).any(|index| {
                value
                    .array_item(index)
                    .and_then(UserValueRef::string_value)
                    .unwrap_or_default()
                    == target
            })
        });
        return match op {
            ConditionOperator::ArrayContainsAny | ConditionOperator::ArrayContainsAll => found,
            ConditionOperator::ArrayContainsNone | ConditionOperator::NotArrayContainsAll => !found,
            _ => false,
        };
    }

    if value_len == 1 && target_len < 16 {
        let original = value
            .array_item(0)
            .and_then(UserValueRef::string_value)
            .unwrap_or_default();
        let found = target_value.any_array_string(false, |target| original == target);
        return match op {
            ConditionOperator::ArrayContainsAny => found,
            ConditionOperator::ArrayContainsNone => !found,
            _ => false,
        };
    }

    if value_len <= target_len / 16
        && matches!(
            op,
            ConditionOperator::ArrayContainsAny | ConditionOperator::ArrayContainsNone
        )
    {
        return compare_arrays_indexed(value, target_value, op, value_len);
    }

    if value_len <= 16 && target_len <= 32 {
        return compare_small_arrays(value, target_value, op, value_len);
    }

    if value_len <= 64 && target_len <= 128 {
        return compare_medium_arrays(value, target_value, op, value_len);
    }

    compare_arrays_with_set(value, target_value, op)
}

#[inline(never)]
fn compare_arrays_indexed(
    value: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    op: ConditionOperator,
    value_len: usize,
) -> bool {
    for index in 0..value_len {
        let item = value.array_item(index);
        let original = item
            .and_then(UserValueRef::string_value)
            .unwrap_or_default();
        let lookup_key = item.and_then(UserValueRef::lowercased_lookup_key);
        if target.array_contains_case_sensitive(original, lookup_key) {
            return matches!(op, ConditionOperator::ArrayContainsAny);
        }
    }
    matches!(op, ConditionOperator::ArrayContainsNone)
}

// Keep the original fallback body, including its coercion and short-circuit order.
#[inline(never)]
fn compare_arrays_with_set<'a>(
    value: UserValueRef<'_>,
    target_value: impl Into<EvaluatorValueRef<'a>>,
    op: ConditionOperator,
) -> bool {
    let target_value = target_value.into();
    unwrap_or_return!(target_value.array_len(), false);
    let value_len = unwrap_or_return!(value.array_len(), false);
    let value_set: AHashSet<&str> = AHashSet::from_iter((0..value_len).map(|index| {
        value
            .array_item(index)
            .and_then(UserValueRef::string_value)
            .unwrap_or_default()
    }));

    let short_circuit = target_value.any_array_string(false, |item| match op {
        ConditionOperator::ArrayContainsAll => !value_set.contains(item),
        ConditionOperator::ArrayContainsAny => value_set.contains(item),
        ConditionOperator::ArrayContainsNone => value_set.contains(item),
        ConditionOperator::NotArrayContainsAll => !value_set.contains(item),
        _ => true,
    });

    match op {
        ConditionOperator::ArrayContainsAll => !short_circuit,
        ConditionOperator::ArrayContainsAny => short_circuit,
        ConditionOperator::ArrayContainsNone => !short_circuit,
        ConditionOperator::NotArrayContainsAll => short_circuit,
        _ => false,
    }
}

// Keep the bounded scratch buffer out of the indexed/set paths' stack frame.
#[inline(never)]
fn compare_small_arrays(
    value: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    op: ConditionOperator,
    value_len: usize,
) -> bool {
    let mut originals = [""; 16];
    let mut hashes = [0; 16];
    let mut buckets = [0_u16; 32];
    for (index, original) in originals.iter_mut().enumerate().take(value_len) {
        *original = value
            .array_item(index)
            .and_then(UserValueRef::string_value)
            .unwrap_or_default();
        hashes[index] = ahash_str(original);
        buckets[(hashes[index] & 31) as usize] |= 1 << index;
    }
    let short_circuit = target.any_array_string(false, |target| {
        let hash = ahash_str(target);
        // Buckets hold user-position bits; collisions still require exact spelling.
        let mut candidates = buckets[(hash & 31) as usize];
        let mut found = false;
        while candidates != 0 {
            let index = candidates.trailing_zeros() as usize;
            if hashes[index] == hash && originals[index] == target {
                found = true;
                break;
            }
            candidates &= candidates - 1;
        }
        match op {
            ConditionOperator::ArrayContainsAll | ConditionOperator::NotArrayContainsAll => !found,
            ConditionOperator::ArrayContainsAny | ConditionOperator::ArrayContainsNone => found,
            _ => true,
        }
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

// A separate frame keeps the 64-position index out of the tiny-list path.
#[inline(never)]
fn compare_medium_arrays(
    value: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    op: ConditionOperator,
    value_len: usize,
) -> bool {
    let mut originals = [""; 64];
    let mut hashes = [0; 64];
    let mut buckets = [0_u64; 128];
    for (index, original) in originals.iter_mut().enumerate().take(value_len) {
        *original = value
            .array_item(index)
            .and_then(UserValueRef::string_value)
            .unwrap_or_default();
        hashes[index] = ahash_str(original);
        buckets[(hashes[index] & 127) as usize] |= 1_u64 << index;
    }
    let short_circuit = target.any_array_string(false, |target| {
        let hash = ahash_str(target);
        // Buckets hold user-position bits; collisions still require exact spelling.
        let mut candidates = buckets[(hash & 127) as usize];
        let mut found = false;
        while candidates != 0 {
            let index = candidates.trailing_zeros() as usize;
            if hashes[index] == hash && originals[index] == target {
                found = true;
                break;
            }
            candidates &= candidates - 1;
        }
        match op {
            ConditionOperator::ArrayContainsAll | ConditionOperator::NotArrayContainsAll => !found,
            ConditionOperator::ArrayContainsAny | ConditionOperator::ArrayContainsNone => found,
            _ => true,
        }
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

#[cfg(test)]
mod tests {
    use super::compare_arrays;
    use crate::{
        dyn_value,
        evaluation::evaluator_value::{EvaluatorValueType, MemoizedEvaluatorValue},
        specs_response::spec_types::ConditionOperator,
        test_only_make_eval_value,
    };
    use serde_json::json;

    fn compare(
        value: serde_json::Value,
        target: &MemoizedEvaluatorValue,
        op: ConditionOperator,
    ) -> bool {
        let value = dyn_value!(value);
        compare_arrays((&value).into(), target, op)
    }

    #[test]
    fn array_operators_preserve_quantifier_semantics() {
        let target = test_only_make_eval_value!(["a", "b"]);

        let cases = [
            (json!(["a", "b", "c"]), true, true, false, false),
            (json!(["a"]), false, true, false, true),
            (json!(["z"]), false, false, true, true),
            (json!([]), false, false, true, true),
        ];

        for (value, all, any, none, not_all) in cases {
            assert_eq!(
                compare(value.clone(), &target, ConditionOperator::ArrayContainsAll),
                all
            );
            assert_eq!(
                compare(value.clone(), &target, ConditionOperator::ArrayContainsAny),
                any
            );
            assert_eq!(
                compare(value.clone(), &target, ConditionOperator::ArrayContainsNone),
                none
            );
            assert_eq!(
                compare(value, &target, ConditionOperator::NotArrayContainsAll),
                not_all
            );
        }
    }

    #[test]
    fn empty_and_missing_targets_keep_existing_behavior() {
        let empty = MemoizedEvaluatorValue::from(json!([]));
        let value = json!(["a"]);

        assert!(compare(
            value.clone(),
            &empty,
            ConditionOperator::ArrayContainsAll
        ));
        assert!(!compare(
            value.clone(),
            &empty,
            ConditionOperator::ArrayContainsAny
        ));
        assert!(compare(
            value.clone(),
            &empty,
            ConditionOperator::ArrayContainsNone
        ));
        assert!(!compare(
            value.clone(),
            &empty,
            ConditionOperator::NotArrayContainsAll
        ));

        let missing = MemoizedEvaluatorValue::new(EvaluatorValueType::Array);
        for op in [
            ConditionOperator::ArrayContainsAll,
            ConditionOperator::ArrayContainsAny,
            ConditionOperator::ArrayContainsNone,
            ConditionOperator::NotArrayContainsAll,
        ] {
            assert!(!compare(value.clone(), &missing, op));
        }
    }
}
