use crate::{
    evaluation::evaluator_value::MemoizedEvaluatorValue,
    specs_response::spec_types::ConditionOperator, unwrap_or_return,
    user::user_value::UserValueRef,
};

pub(crate) fn compare_numbers(
    left: UserValueRef<'_>,
    right: &MemoizedEvaluatorValue,
    op: ConditionOperator,
) -> bool {
    let left_num = unwrap_or_return!(left.float_value(), false);
    let right_num = unwrap_or_return!(right.float_value, false);

    match op {
        ConditionOperator::Gt => left_num > right_num,
        ConditionOperator::Gte => left_num >= right_num,
        ConditionOperator::Lt => left_num < right_num,
        ConditionOperator::Lte => left_num <= right_num,
        _ => false,
    }
}

#[cfg(test)]
mod tests {
    use crate::evaluation::comparisons::compare_numbers;
    use crate::specs_response::spec_types::ConditionOperator;
    use crate::{dyn_value, test_only_make_eval_value};

    #[test]
    fn test_number_greater_than() {
        let left = dyn_value!(2.0);
        let right = test_only_make_eval_value!(1.0);

        let result = compare_numbers((&left).into(), &right, ConditionOperator::Gt);
        assert!(result);
    }

    #[test]
    fn test_number_greater_than_equal_string() {
        let left = dyn_value!("1.24");
        let right_smaller = test_only_make_eval_value!("1.23");
        let right_same = test_only_make_eval_value!("1.24");

        assert!(compare_numbers(
            (&left).into(),
            &right_smaller,
            ConditionOperator::Gte
        ));
        assert!(compare_numbers(
            (&left).into(),
            &right_same,
            ConditionOperator::Gte
        ));
    }

    #[test]
    fn test_number_less_than_equal_string() {
        let left = dyn_value!("1.23");
        let right_bigger = test_only_make_eval_value!("1.24");
        let right_same = test_only_make_eval_value!("1.24");

        assert!(compare_numbers(
            (&left).into(),
            &right_bigger,
            ConditionOperator::Lte
        ));
        assert!(compare_numbers(
            (&left).into(),
            &right_same,
            ConditionOperator::Lte
        ));
    }

    #[test]
    fn test_number_less_than() {
        let left = dyn_value!(1.0);
        let right = test_only_make_eval_value!(2.0);

        let result = compare_numbers((&left).into(), &right, ConditionOperator::Lt);
        assert!(result);
    }

    #[test]
    fn test_number_less_than_or_equal() {
        let dyn_one = dyn_value!(1.0);
        let dyn_two = dyn_value!(2.0);
        let eval_one = test_only_make_eval_value!(1.0);
        let eval_two = test_only_make_eval_value!(2.0);

        assert!(compare_numbers(
            (&dyn_one).into(),
            &eval_two,
            ConditionOperator::Lte
        ));
        assert!(compare_numbers(
            (&dyn_two).into(),
            &eval_two,
            ConditionOperator::Lte
        ));
        assert!(!compare_numbers(
            (&dyn_two).into(),
            &eval_one,
            ConditionOperator::Lte
        ));
    }
}
