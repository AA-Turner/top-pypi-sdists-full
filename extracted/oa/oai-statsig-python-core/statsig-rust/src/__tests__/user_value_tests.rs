use crate::{
    user::user_value::{UserValue, UserValueMap},
    DynamicValue,
};

#[test]
fn float_hash_matches_dynamic_value_json_representation() {
    assert_eq!(
        UserValue::from_f64(1.0).hash_value(),
        DynamicValue::from_f64(1.0).hash_value,
    );
    assert_eq!(
        UserValue::from_f64(1.25).hash_value(),
        DynamicValue::from_f64(1.25).hash_value,
    );
}

#[test]
fn object_user_value_serializes_from_cached_raw_json() {
    let mut values = UserValueMap::default();
    values.insert("enabled".to_string(), UserValue::from_bool(true));
    values.insert("count".to_string(), UserValue::from_i64(3));

    let serialized = serde_json::to_value(UserValue::from_object(values)).unwrap();
    assert_eq!(serialized["enabled"], serde_json::json!(true));
    assert_eq!(serialized["count"], serde_json::json!(3));
}

#[test]
fn unsigned_json_integer_user_value_stays_integer() {
    let value = UserValue::from_json_value(serde_json::json!(9_223_372_036_854_775_808u64));

    assert_eq!(
        serde_json::to_value(&value).unwrap(),
        serde_json::json!(9_223_372_036_854_775_808u64)
    );
    assert!(matches!(
        value,
        UserValue::Int { value, .. } if value == 9_223_372_036_854_775_808i128
    ));
}

#[test]
fn direct_unsigned_user_value_stays_integer() {
    let value = UserValue::from_u64(9_223_372_036_854_775_808u64);

    assert_eq!(
        serde_json::to_value(&value).unwrap(),
        serde_json::json!(9_223_372_036_854_775_808u64)
    );
    assert!(matches!(
        value,
        UserValue::Int { value, .. } if value == 9_223_372_036_854_775_808i128
    ));
}
