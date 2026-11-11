use crate::{
    DynamicValue, evaluation::comparisons::compare_time,
    specs_response::spec_types::ConditionOperator, test_only_make_eval_value,
    user::user_value::UserValue,
};

#[test]
fn compares_minimum_user_timestamp() {
    let user_timestamp = UserValue::from_i64(i64::MIN);
    let rule_timestamp = test_only_make_eval_value!(0_i64);

    assert!(compare_time(
        (&user_timestamp).into(),
        &rule_timestamp,
        ConditionOperator::Before
    ));
}

#[test]
fn compares_days_across_timestamp_boundaries() {
    let user_timestamp = DynamicValue::from_i64(-1);
    let minimum = test_only_make_eval_value!(i64::MIN);
    let epoch = test_only_make_eval_value!(0_i64);

    assert!(!compare_time(
        (&user_timestamp).into(),
        &minimum,
        ConditionOperator::On
    ));
    assert!(compare_time(
        (&user_timestamp).into(),
        &epoch,
        ConditionOperator::On
    ));
}
