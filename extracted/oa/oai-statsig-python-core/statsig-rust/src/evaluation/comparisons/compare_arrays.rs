use crate::{
    evaluation::evaluator_value::EvaluatorValueRef, specs_response::spec_types::ConditionOperator,
    unwrap_or_return, user::user_value::UserValueRef,
};
use ahash::AHashSet;

pub(crate) fn compare_arrays<'a>(
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

    let short_circuit = target_value.any_array_entry(|_, _, item| match op {
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
