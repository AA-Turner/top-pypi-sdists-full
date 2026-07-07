use crate::{
    evaluation::evaluator_value::MemoizedEvaluatorValue,
    specs_response::spec_types::ConditionOperator, unwrap_or_return,
    user::user_value::UserValueRef,
};
use std::collections::HashSet;

pub(crate) fn compare_arrays(
    value: UserValueRef<'_>,
    target_value: &MemoizedEvaluatorValue,
    op: ConditionOperator,
) -> bool {
    let target_array = unwrap_or_return!(&target_value.array_value, false);
    let value_len = unwrap_or_return!(value.array_len(), false);
    let value_set: HashSet<&str> = HashSet::from_iter((0..value_len).map(|index| {
        value
            .array_item(index)
            .and_then(UserValueRef::string_value)
            .unwrap_or_default()
    }));

    for (_, item) in target_array.values() {
        match op {
            ConditionOperator::ArrayContainsAll => {
                if !value_set.contains(item.as_str()) {
                    return false;
                }
            }
            ConditionOperator::ArrayContainsAny => {
                if value_set.contains(item.as_str()) {
                    return true;
                }
            }
            ConditionOperator::ArrayContainsNone => {
                if value_set.contains(item.as_str()) {
                    return false;
                }
            }
            ConditionOperator::NotArrayContainsAll => {
                if !value_set.contains(item.as_str()) {
                    return true;
                }
            }

            _ => {
                return false;
            }
        }
    }
    !matches!(
        op,
        ConditionOperator::ArrayContainsAny | ConditionOperator::NotArrayContainsAll
    )
}
