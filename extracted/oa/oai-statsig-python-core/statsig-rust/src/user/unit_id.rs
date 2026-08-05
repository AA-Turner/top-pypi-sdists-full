use crate::{DynamicValue, dyn_value, user::user_value::UserValue};

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
