use crate::{
    evaluation::evaluator_value::MemoizedEvaluatorValue, unwrap_or_return,
    user::user_value::UserValueRef,
};
use std::collections::HashSet;

pub(crate) fn compare_arrays(
    value: UserValueRef<'_>,
    target_value: &MemoizedEvaluatorValue,
    op: &str,
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
            "array_contains_all" => {
                if !value_set.contains(item.as_str()) {
                    return false;
                }
            }
            "array_contains_any" => {
                if value_set.contains(item.as_str()) {
                    return true;
                }
            }
            "array_contains_none" => {
                if value_set.contains(item.as_str()) {
                    return false;
                }
            }
            "not_array_contains_all" => {
                if !value_set.contains(item.as_str()) {
                    return true;
                }
            }

            _ => {
                return false;
            }
        }
    }
    !(op == "array_contains_any" || op == "not_array_contains_all")
}
