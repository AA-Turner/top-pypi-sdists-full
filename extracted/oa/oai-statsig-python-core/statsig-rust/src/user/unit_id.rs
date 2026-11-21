use crate::{DynamicValue, dyn_value, user::user_value::UserValue};

pub(crate) const USER_ID_TYPE: &str = "userID";
const LOWERCASE_USER_ID_TYPE: &str = "userid";

pub(crate) fn is_user_id_type(id_type: &str) -> bool {
    id_type.eq_ignore_ascii_case(LOWERCASE_USER_ID_TYPE)
}

pub(super) fn resolve_unit_id<'a, T>(
    id_type: &str,
    lowercased_id_type: &str,
    primary: Option<&'a T>,
    custom: impl Fn(&str) -> Option<&'a T>,
) -> Option<&'a T> {
    if lowercased_id_type == LOWERCASE_USER_ID_TYPE {
        primary
    } else {
        custom(id_type).or_else(|| custom(lowercased_id_type))
    }
}

pub enum UnitID {
    String(String),
    Float(f64),
    Int(i64),
}

impl From<&str> for UnitID {
    fn from(value: &str) -> Self {
        UnitID::String(value.into())
    }
}

impl From<String> for UnitID {
    fn from(value: String) -> Self {
        UnitID::String(value)
    }
}

impl From<&String> for UnitID {
    fn from(value: &String) -> Self {
        UnitID::String(value.clone())
    }
}

impl From<f64> for UnitID {
    fn from(value: f64) -> Self {
        UnitID::Float(value)
    }
}

impl From<i64> for UnitID {
    fn from(value: i64) -> Self {
        UnitID::Int(value)
    }
}

impl From<UnitID> for DynamicValue {
    fn from(value: UnitID) -> Self {
        match value {
            UnitID::String(s) => dyn_value!(s),
            UnitID::Float(f) => dyn_value!(f),
            UnitID::Int(i) => dyn_value!(i),
        }
    }
}

impl From<UnitID> for UserValue {
    fn from(value: UnitID) -> Self {
        match value {
            UnitID::String(value) => UserValue::from(value),
            UnitID::Float(value) => UserValue::from(value),
            UnitID::Int(value) => UserValue::from(value),
        }
    }
}
