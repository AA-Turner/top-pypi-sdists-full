use crate::{
    evaluation::evaluator_value::MemoizedEvaluatorValue,
    specs_response::spec_types::ConditionOperator, unwrap_or_return,
    user::user_value::UserValueRef,
};

pub(crate) fn compare_strings_in_array(
    value: UserValueRef<'_>,
    target_value: &MemoizedEvaluatorValue,
    op: ConditionOperator,
) -> bool {
    let ignore_case = !matches!(
        op,
        ConditionOperator::AnyCaseSensitive | ConditionOperator::NoneCaseSensitive
    );
    let result = compare_strings_in_array_impl(value, target_value, op, ignore_case);

    if matches!(
        op,
        ConditionOperator::NoneOf
            | ConditionOperator::NoneCaseSensitive
            | ConditionOperator::StrContainsNone
    ) {
        return !result;
    }
    result
}

fn compare_strings_in_array_impl(
    value: UserValueRef<'_>,
    target_value: &MemoizedEvaluatorValue,
    op: ConditionOperator,
    ignore_case: bool,
) -> bool {
    if let Some(keyed_lookup) = &target_value.object_value {
        if matches!(op, ConditionOperator::Any | ConditionOperator::NoneOf) {
            let contains = match value.lowercased_lookup_key() {
                Some(key) => keyed_lookup.contains_key(key),
                None => value
                    .lowercased_string_value()
                    .is_some_and(|lowercased_value| {
                        keyed_lookup
                            .keys()
                            .any(|value| value.as_str() == lowercased_value.as_ref())
                    }),
            };
            return contains;
        }
    }

    let array_value = unwrap_or_return!(&target_value.array_value, false);
    if matches!(op, ConditionOperator::Any | ConditionOperator::NoneOf) {
        let contains = match value.lowercased_lookup_key() {
            Some(key) => array_value.contains_key(key),
            None => value
                .lowercased_string_value()
                .is_some_and(|lowercased_value| {
                    array_value
                        .keys()
                        .any(|value| value.as_str() == lowercased_value.as_ref())
                }),
        };
        return contains;
    }

    let value_str = value.string_value().unwrap_or_default();
    let lowercased_value = value.lowercased_string_value().unwrap_or_default();

    let mut comparison_result = false;
    for (lowercase_str, (_, current_str)) in array_value {
        let left = if ignore_case {
            lowercased_value.as_ref()
        } else {
            value_str
        };

        let right = if ignore_case {
            lowercase_str
        } else {
            current_str
        };

        comparison_result = match op {
            ConditionOperator::Any
            | ConditionOperator::NoneOf
            | ConditionOperator::AnyCaseSensitive
            | ConditionOperator::NoneCaseSensitive => left == right.as_str(),
            ConditionOperator::StrStartsWithAny => left.starts_with(right.as_str()),
            ConditionOperator::StrEndsWithAny => left.ends_with(right.as_str()),
            ConditionOperator::StrContainsAny | ConditionOperator::StrContainsNone => {
                left.contains(right.as_str())
            }
            _ => false, // todo: unsupported?
        };

        if comparison_result {
            break;
        }
    }

    comparison_result
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use crate::evaluation::comparisons::compare_strings_in_array;
    use crate::specs_response::spec_types::ConditionOperator;
    use crate::{dyn_value, test_only_make_eval_value};

    #[test]
    fn test_array_contains() {
        let needle = dyn_value!("Foo");
        let haystack = test_only_make_eval_value!(["boo", "bar", "foo", "far", "zoo", "zar"]);

        assert!(compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::Any
        ));
        assert!(!compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::AnyCaseSensitive
        ));
    }

    #[test]
    fn test_array_does_not_contain() {
        let needle = dyn_value!("Foo");
        let haystack = test_only_make_eval_value!(vec!["boo", "bar", "far", "zoo", "zar"]);

        assert!(!compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::Any
        ));

        assert!(!compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::AnyCaseSensitive
        ));
    }

    #[test]
    fn test_str_starting_with() {
        let needle = dyn_value!("daniel@statsig.com");
        let haystack = test_only_make_eval_value!(vec!["tore", "daniel"]);

        assert!(compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::StrStartsWithAny
        ));
    }

    #[test]
    fn test_str_ending_with() {
        let needle = dyn_value!("tore@statsig.com");
        let haystack = test_only_make_eval_value!(vec!["@statsig.io", "@statsig.com"]);

        assert!(compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::StrEndsWithAny
        ));
    }

    #[test]
    fn test_str_contains_any() {
        let needle = dyn_value!("daniel@statsig.io");
        let haystack = test_only_make_eval_value!(vec!["sigstat", "statsig"]);

        assert!(compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::StrContainsAny
        ));
    }

    #[test]
    fn test_str_none_case_sensitive() {
        let haystack = test_only_make_eval_value!(vec!["HELLO", "WORLD"]);

        let upper_needle = dyn_value!("HELLO");
        assert!(!compare_strings_in_array(
            (&upper_needle).into(),
            &haystack,
            ConditionOperator::NoneCaseSensitive
        ));

        let lower_needle = dyn_value!("hello");
        assert!(compare_strings_in_array(
            (&lower_needle).into(),
            &haystack,
            ConditionOperator::NoneCaseSensitive
        ));
    }

    #[test]
    fn test_str_any_case_sensitive() {
        let haystack = test_only_make_eval_value!(vec!["HELLO", "WORLD"]);

        let upper_needle = dyn_value!("HELLO");
        assert!(compare_strings_in_array(
            (&upper_needle).into(),
            &haystack,
            ConditionOperator::AnyCaseSensitive
        ));

        let lower_needle = dyn_value!("hello");
        assert!(!compare_strings_in_array(
            (&lower_needle).into(),
            &haystack,
            ConditionOperator::AnyCaseSensitive
        ));
    }

    #[test]
    fn test_array_contains_any() {
        let needle = dyn_value!(json!(["boo", 1, true]));
        let haystack_positive = test_only_make_eval_value!(vec!["zoo", "boo"]);
        let haystack_negative = test_only_make_eval_value!(vec!["zoo", "bar"]);

        assert!(compare_strings_in_array(
            (&needle).into(),
            &haystack_positive,
            ConditionOperator::StrContainsAny
        ));

        assert!(!compare_strings_in_array(
            (&needle).into(),
            &haystack_negative,
            ConditionOperator::StrContainsAny
        ));
    }
}
