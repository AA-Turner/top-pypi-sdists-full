use crate::{
    evaluation::evaluator_value::EvaluatorValueRef, specs_response::spec_types::ConditionOperator,
    unwrap_or_return, user::user_value::UserValueRef,
};

pub(crate) fn compare_strings_in_array<'a>(
    value: UserValueRef<'_>,
    target_value: impl Into<EvaluatorValueRef<'a>>,
    op: ConditionOperator,
) -> bool {
    let target_value = target_value.into();
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
    target_value: EvaluatorValueRef<'_>,
    op: ConditionOperator,
    ignore_case: bool,
) -> bool {
    if target_value.object_len().is_some()
        && matches!(op, ConditionOperator::Any | ConditionOperator::NoneOf)
    {
        return match value.lowercased_lookup_key() {
            Some(key) => target_value.object_contains_key(key),
            None => value
                .lowercased_string_value()
                .is_some_and(|value| target_value.object_contains_key_str(value.as_ref())),
        };
    }

    unwrap_or_return!(target_value.array_len(), false);
    if matches!(op, ConditionOperator::Any | ConditionOperator::NoneOf) {
        return match value.lowercased_lookup_key() {
            Some(key) => target_value.array_contains_key(key),
            None => value
                .lowercased_string_value()
                .is_some_and(|value| target_value.array_contains_lowercase(value.as_ref())),
        };
    }

    let value_str = value.string_value().unwrap_or_default();
    let lowercased_value = value.lowercased_string_value().unwrap_or_default();

    target_value.any_array_entry(|lowercase_str, _, current_str| {
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

        match op {
            ConditionOperator::Any
            | ConditionOperator::NoneOf
            | ConditionOperator::AnyCaseSensitive
            | ConditionOperator::NoneCaseSensitive => left == right,
            ConditionOperator::StrStartsWithAny => left.starts_with(right),
            ConditionOperator::StrEndsWithAny => left.ends_with(right),
            ConditionOperator::StrContainsAny | ConditionOperator::StrContainsNone => {
                contains_substring(left, right)
            }
            _ => false, // todo: unsupported?
        }
    })
}

#[inline]
fn contains_substring(haystack: &str, needle: &str) -> bool {
    if needle.len() <= 1 {
        return haystack.contains(needle);
    }

    memchr::memmem::find(haystack.as_bytes(), needle.as_bytes()).is_some()
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
    fn test_object_contains() {
        let needle = dyn_value!("Foo");
        let haystack = test_only_make_eval_value!(json!({"foo": true, "bar": true}));

        assert!(compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::Any
        ));
        assert!(!compare_strings_in_array(
            (&needle).into(),
            &haystack,
            ConditionOperator::NoneOf
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
    fn test_str_contains_none() {
        let value = dyn_value!("daniel@statsig.io");
        let matching_targets = test_only_make_eval_value!(vec!["@example.com", "@statsig.io"]);
        let missing_targets = test_only_make_eval_value!(vec!["@example.com", "@statsig.com"]);

        assert!(!compare_strings_in_array(
            (&value).into(),
            &matching_targets,
            ConditionOperator::StrContainsNone
        ));
        assert!(compare_strings_in_array(
            (&value).into(),
            &missing_targets,
            ConditionOperator::StrContainsNone
        ));
    }

    #[test]
    fn test_substring_search_matches_std_for_utf8_and_edge_cases() {
        let haystacks = [
            "",
            "a",
            "daniel@statsig.io",
            "café au lait",
            "東京都",
            "a💖b",
            "Straße",
            "embedded\0null",
        ];
        let needles = [
            "",
            "a",
            "@statsig.io",
            "@example.com",
            "é",
            "京",
            "💖",
            "ss",
            "ß",
            "\0",
            "null",
        ];

        for haystack in haystacks {
            for needle in needles {
                assert_eq!(
                    super::contains_substring(haystack, needle),
                    haystack.contains(needle),
                    "haystack={haystack:?}, needle={needle:?}"
                );
            }
        }
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
