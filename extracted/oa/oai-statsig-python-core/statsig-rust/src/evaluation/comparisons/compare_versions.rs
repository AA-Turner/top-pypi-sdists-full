use crate::{
    evaluation::evaluator_value::EvaluatorValueRef, specs_response::spec_types::ConditionOperator,
    unwrap_or_return, user::user_value::UserValueRef,
};

pub(crate) fn compare_versions<'a>(
    left: UserValueRef<'_>,
    right: impl Into<EvaluatorValueRef<'a>>,
    op: ConditionOperator,
) -> bool {
    let right = right.into();
    let left_str = unwrap_or_return!(left.string_value(), false);
    let right_str = unwrap_or_return!(right.string_value(), false);

    let result = match compare_versions_impl(left_str, right_str) {
        ComparisonResult::Ok(result) => result,
        ComparisonResult::NumericParseFailure => return false,
    };

    match op {
        ConditionOperator::VersionGt => result > 0,
        ConditionOperator::VersionGte => result >= 0,
        ConditionOperator::VersionLt => result < 0,
        ConditionOperator::VersionLte => result <= 0,
        ConditionOperator::VersionEq => result == 0,
        ConditionOperator::VersionNeq => result != 0,
        _ => false,
    }
}

enum ComparisonResult {
    NumericParseFailure,
    Ok(i32),
}

fn compare_versions_impl(left_str: &str, right_str: &str) -> ComparisonResult {
    let left_version = left_str.split('-').next().unwrap_or("");
    let right_version = right_str.split('-').next().unwrap_or("");

    let mut left_parts = left_version.split('.');
    let mut right_parts = right_version.split('.');

    loop {
        let left_num = match next_num(left_parts.next()) {
            Ok(v) => v,
            Err(_) => return ComparisonResult::NumericParseFailure,
        };

        let right_num = match next_num(right_parts.next()) {
            Ok(v) => v,
            Err(_) => return ComparisonResult::NumericParseFailure,
        };

        if left_num.is_none() && right_num.is_none() {
            break;
        }

        let left_num = left_num.unwrap_or(0);
        let right_num = right_num.unwrap_or(0);

        if left_num < right_num {
            return ComparisonResult::Ok(-1);
        }

        if left_num > right_num {
            return ComparisonResult::Ok(1);
        }
    }

    ComparisonResult::Ok(0)
}

fn next_num(part: Option<&str>) -> Result<Option<i128>, std::num::ParseIntError> {
    part.map(|s| s.trim().parse::<i128>()).transpose()
}

#[cfg(test)]
mod tests {
    use crate::evaluation::comparisons::compare_versions;
    use crate::specs_response::spec_types::ConditionOperator;
    use crate::{dyn_value, test_only_make_eval_value};

    #[test]
    fn test_version_comparison_equal() {
        let left = dyn_value!("1.2.3");
        let right = test_only_make_eval_value!("1.2.3");

        let result = compare_versions((&left).into(), &right, ConditionOperator::VersionEq);
        assert!(result);
    }

    #[test]
    fn test_version_comparison_greater_than() {
        let left = dyn_value!("1.2.4");
        let right = test_only_make_eval_value!("1.2.3");

        let result = compare_versions((&left).into(), &right, ConditionOperator::VersionGt);
        assert!(result);
    }

    #[test]
    fn test_version_comparison_less_than() {
        let left = dyn_value!("1.2.3");
        let right = test_only_make_eval_value!("1.2.4");

        let result = compare_versions((&left).into(), &right, ConditionOperator::VersionLt);
        assert!(result);
    }
}
