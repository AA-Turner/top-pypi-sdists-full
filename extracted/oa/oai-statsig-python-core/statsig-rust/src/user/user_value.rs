#[cfg(feature = "ordered_user_data_maps")]
use ahash::RandomState as AHashState;
#[cfg(feature = "ordered_user_data_maps")]
use indexmap::IndexMap;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use serde_json::{
    Number as JsonNumber, Value as JsonValue,
    value::{RawValue, to_raw_value},
};
use std::borrow::Cow;
#[cfg(not(feature = "ordered_user_data_maps"))]
use std::collections::HashMap;

use crate::{
    DynamicValue,
    hashing::ahash_str,
    interned_string::InternedString,
    log_w,
    value_parsing::{maybe_parse_f64, maybe_parse_i64, try_parse_timestamp},
};

const TAG: &str = "UserValue";

lazy_static::lazy_static! {
    static ref TRUE_HASH: u64 = ahash_str("true");
    static ref FALSE_HASH: u64 = ahash_str("false");
}

#[cfg(feature = "ordered_user_data_maps")]
pub type UserValueMap = IndexMap<String, UserValue, AHashState>;
#[cfg(not(feature = "ordered_user_data_maps"))]
pub type UserValueMap = HashMap<String, UserValue>;

#[derive(Clone, Debug, PartialEq)]
pub struct UserString {
    pub value: InternedString,
    pub lowercased_value: InternedString,
    pub int_value: Option<i64>,
    pub float_value: Option<f64>,
    pub timestamp_value: Option<i64>,
}

impl UserString {
    pub fn new(value: String) -> Self {
        let int_value = maybe_parse_i64(&value);
        let float_value = maybe_parse_f64(&value);
        let timestamp_value = try_parse_timestamp(&value, int_value);
        let value = InternedString::from_string_uninterned(value);
        let lowercased_value = if value.as_str().bytes().any(|byte| byte.is_ascii_uppercase()) {
            InternedString::from_string_uninterned(value.as_str().to_lowercase())
        } else {
            value.clone()
        };

        Self {
            int_value,
            float_value,
            timestamp_value,
            value,
            lowercased_value,
        }
    }
}

/// Eager, evaluation-ready representation for constructor-hot user fields.
///
/// This keeps Python-created `StatsigUser` data off the heavier `DynamicValue`
/// path while preserving the same primitive coercions the evaluator relies on.
#[derive(Clone, Debug)]
pub enum UserValue {
    Null,
    Bool(bool),
    Int {
        value: i128,
        string_value: String,
    },
    Float {
        value: f64,
        int_value: Option<i64>,
        string_value: String,
        hash_string: String,
    },
    String(UserString),
    Array {
        values: Vec<UserValue>,
        string_value: UserString,
    },
    Object {
        values: UserValueMap,
        serialized_value: Box<RawValue>,
    },
}

impl PartialEq for UserValue {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Null, Self::Null) => true,
            (Self::Bool(left), Self::Bool(right)) => left == right,
            (
                Self::Int {
                    value: left_value,
                    string_value: left_string,
                },
                Self::Int {
                    value: right_value,
                    string_value: right_string,
                },
            ) => left_value == right_value && left_string == right_string,
            (
                Self::Float {
                    value: left_value,
                    int_value: left_int,
                    string_value: left_string,
                    hash_string: left_hash,
                },
                Self::Float {
                    value: right_value,
                    int_value: right_int,
                    string_value: right_string,
                    hash_string: right_hash,
                },
            ) => {
                left_value == right_value
                    && left_int == right_int
                    && left_string == right_string
                    && left_hash == right_hash
            }
            (Self::String(left), Self::String(right)) => left == right,
            (
                Self::Array {
                    values: left_values,
                    string_value: left_string,
                },
                Self::Array {
                    values: right_values,
                    string_value: right_string,
                },
            ) => left_values == right_values && left_string == right_string,
            (
                Self::Object {
                    values: left_values,
                    serialized_value: left_serialized,
                },
                Self::Object {
                    values: right_values,
                    serialized_value: right_serialized,
                },
            ) => left_values == right_values && left_serialized.get() == right_serialized.get(),
            _ => false,
        }
    }
}

impl UserValue {
    #[must_use]
    pub fn new() -> Self {
        Self::Null
    }

    #[must_use]
    pub fn from_string(value: impl Into<String>) -> Self {
        Self::String(UserString::new(value.into()))
    }

    #[must_use]
    pub fn from_bool(value: bool) -> Self {
        Self::Bool(value)
    }

    #[must_use]
    pub fn from_i64(value: i64) -> Self {
        Self::from_i128(value.into())
    }

    #[must_use]
    pub fn from_u64(value: u64) -> Self {
        Self::from_i128(value.into())
    }

    #[must_use]
    fn from_i128(value: i128) -> Self {
        Self::Int {
            value,
            string_value: value.to_string(),
        }
    }

    #[must_use]
    pub fn from_f64(value: f64) -> Self {
        let num = match JsonNumber::from_f64(value) {
            Some(num) => num,
            None => {
                log_w!(
                    TAG,
                    "Failed to convert f64 to serde_json::Number: {}",
                    value
                );
                return Self::from_i64(value as i64);
            }
        };

        let mut float_value = num.as_f64().unwrap_or(value);
        let mut int_value = num.as_i64();
        if let Some(i) = int_value {
            float_value = i as f64;
        } else {
            let i = float_value as i64;
            if i as f64 == float_value {
                int_value = Some(i);
            }
        }

        Self::Float {
            value: float_value,
            int_value,
            string_value: float_value.to_string(),
            hash_string: JsonValue::Number(num).to_string(),
        }
    }

    #[must_use]
    pub fn from_array(values: Vec<UserValue>) -> Self {
        let serialized = serde_json::to_string(&values).unwrap_or_else(|_| "[]".to_string());
        Self::Array {
            values,
            string_value: UserString::new(serialized),
        }
    }

    #[must_use]
    pub fn from_object(values: UserValueMap) -> Self {
        let serialized_value = to_raw_value(&values).unwrap_or_else(|error| {
            log_w!(TAG, "Failed to serialize object UserValue: {}", error);
            to_raw_value(&JsonValue::Object(Default::default()))
                .expect("empty JSON object should always serialize")
        });
        Self::Object {
            values,
            serialized_value,
        }
    }

    #[must_use]
    pub fn from_json_value(value: JsonValue) -> Self {
        match value {
            JsonValue::Null => Self::Null,
            JsonValue::Bool(value) => Self::from_bool(value),
            JsonValue::Number(value) => {
                if let Some(value) = value.as_i64() {
                    Self::from_i64(value)
                } else if let Some(value) = value.as_u64() {
                    Self::from_u64(value)
                } else if let Some(value) = value.as_f64() {
                    Self::from_f64(value)
                } else {
                    Self::Null
                }
            }
            JsonValue::String(value) => Self::from_string(value),
            JsonValue::Array(values) => {
                Self::from_array(values.into_iter().map(Self::from_json_value).collect())
            }
            JsonValue::Object(values) => Self::from_object(
                values
                    .into_iter()
                    .map(|(key, value)| (key, Self::from_json_value(value)))
                    .collect(),
            ),
        }
    }

    #[must_use]
    pub fn hash_value(&self) -> u64 {
        match self {
            Self::Null => 0,
            Self::Bool(true) => *TRUE_HASH,
            Self::Bool(false) => *FALSE_HASH,
            Self::Int { string_value, .. } => ahash_str(string_value),
            Self::Float { hash_string, .. } => ahash_str(hash_string),
            Self::String(value)
            | Self::Array {
                string_value: value,
                ..
            } => ahash_str(value.value.as_str()),
            Self::Object {
                serialized_value, ..
            } => ahash_str(serialized_value.get()),
        }
    }

    #[must_use]
    pub fn string_value(&self) -> Option<&str> {
        match self {
            Self::Null | Self::Object { .. } => None,
            Self::Bool(true) => Some("true"),
            Self::Bool(false) => Some("false"),
            Self::Int { string_value, .. } | Self::Float { string_value, .. } => {
                Some(string_value.as_str())
            }
            Self::String(value)
            | Self::Array {
                string_value: value,
                ..
            } => Some(value.value.as_str()),
        }
    }
}

impl Default for UserValue {
    fn default() -> Self {
        Self::new()
    }
}

impl Serialize for UserValue {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Null => serializer.serialize_unit(),
            Self::Bool(value) => serializer.serialize_bool(*value),
            Self::Int { value, .. } => {
                if let Ok(value) = i64::try_from(*value) {
                    serializer.serialize_i64(value)
                } else if let Ok(value) = u64::try_from(*value) {
                    serializer.serialize_u64(value)
                } else {
                    serializer.serialize_i128(*value)
                }
            }
            Self::Float { value, .. } => serializer.serialize_f64(*value),
            Self::String(value) => serializer.serialize_str(value.value.as_str()),
            Self::Array { values, .. } => values.serialize(serializer),
            Self::Object {
                serialized_value, ..
            } => serialized_value.serialize(serializer),
        }
    }
}

impl<'de> Deserialize<'de> for UserValue {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        Ok(Self::from_json_value(JsonValue::deserialize(deserializer)?))
    }
}

impl From<JsonValue> for UserValue {
    fn from(value: JsonValue) -> Self {
        Self::from_json_value(value)
    }
}

impl From<DynamicValue> for UserValue {
    fn from(value: DynamicValue) -> Self {
        Self::from_json_value(value.json_value)
    }
}

impl From<String> for UserValue {
    fn from(value: String) -> Self {
        Self::from_string(value)
    }
}

impl From<&str> for UserValue {
    fn from(value: &str) -> Self {
        Self::from_string(value)
    }
}

impl From<i64> for UserValue {
    fn from(value: i64) -> Self {
        Self::from_i64(value)
    }
}

impl From<i32> for UserValue {
    fn from(value: i32) -> Self {
        Self::from_i64(value as i64)
    }
}

impl From<usize> for UserValue {
    fn from(value: usize) -> Self {
        Self::from_u64(value as u64)
    }
}

impl From<f64> for UserValue {
    fn from(value: f64) -> Self {
        Self::from_f64(value)
    }
}

impl From<bool> for UserValue {
    fn from(value: bool) -> Self {
        Self::from_bool(value)
    }
}

#[derive(Clone, Copy)]
/// Read-only bridge that lets evaluator code consume both legacy `DynamicValue`
/// data and the faster `UserValue` representation without duplicating operators.
pub enum UserValueRef<'a> {
    Dynamic(&'a DynamicValue),
    User(&'a UserValue),
}

impl<'a> From<&'a DynamicValue> for UserValueRef<'a> {
    fn from(value: &'a DynamicValue) -> Self {
        Self::Dynamic(value)
    }
}

impl<'a> From<&'a UserValue> for UserValueRef<'a> {
    fn from(value: &'a UserValue) -> Self {
        Self::User(value)
    }
}

impl<'a> UserValueRef<'a> {
    pub fn is_null(self) -> bool {
        match self {
            Self::Dynamic(value) => value.null.is_some() || value.json_value.is_null(),
            Self::User(UserValue::Null) => true,
            Self::User(_) => false,
        }
    }

    pub fn bool_value(self) -> Option<bool> {
        match self {
            Self::Dynamic(value) => value.bool_value,
            Self::User(UserValue::Bool(value)) => Some(*value),
            Self::User(_) => None,
        }
    }

    pub fn int_value(self) -> Option<i64> {
        match self {
            Self::Dynamic(value) => value.int_value,
            Self::User(UserValue::Int { value, .. }) => i64::try_from(*value).ok(),
            Self::User(UserValue::Float { int_value, .. }) => *int_value,
            Self::User(UserValue::String(value)) => value.int_value,
            Self::User(_) => None,
        }
    }

    pub fn float_value(self) -> Option<f64> {
        match self {
            Self::Dynamic(value) => value.float_value,
            Self::User(UserValue::Int { value, .. }) => Some(*value as f64),
            Self::User(UserValue::Float { value, .. }) => Some(*value),
            Self::User(UserValue::String(value)) => value.float_value,
            Self::User(_) => None,
        }
    }

    pub fn timestamp_value(self) -> Option<i64> {
        match self {
            Self::Dynamic(value) => value.timestamp_value,
            Self::User(UserValue::String(value)) => value.timestamp_value,
            Self::User(_) => None,
        }
    }

    pub fn string_value(self) -> Option<&'a str> {
        match self {
            Self::Dynamic(value) => value
                .string_value
                .as_ref()
                .map(|value| value.value.as_str()),
            Self::User(value) => value.string_value(),
        }
    }

    pub fn lowercased_lookup_key(self) -> Option<&'a InternedString> {
        match self {
            Self::Dynamic(value) => value
                .string_value
                .as_ref()
                .map(|value| &value.lowercased_value),
            Self::User(UserValue::String(value)) => Some(&value.lowercased_value),
            Self::User(UserValue::Array { string_value, .. }) => {
                Some(&string_value.lowercased_value)
            }
            Self::User(_) => None,
        }
    }

    pub fn lowercased_string_value(self) -> Option<Cow<'a, str>> {
        match self {
            Self::Dynamic(value) => value
                .string_value
                .as_ref()
                .map(|value| Cow::Borrowed(value.lowercased_value.as_str())),
            Self::User(UserValue::Bool(true)) => Some(Cow::Borrowed("true")),
            Self::User(UserValue::Bool(false)) => Some(Cow::Borrowed("false")),
            Self::User(UserValue::Int { string_value, .. }) => {
                Some(Cow::Borrowed(string_value.as_str()))
            }
            Self::User(UserValue::Float { string_value, .. }) => {
                Some(Cow::Borrowed(string_value.as_str()))
            }
            Self::User(UserValue::String(value)) => {
                Some(Cow::Borrowed(value.lowercased_value.as_str()))
            }
            Self::User(UserValue::Array { string_value, .. }) => {
                Some(Cow::Borrowed(string_value.lowercased_value.as_str()))
            }
            Self::User(UserValue::Null | UserValue::Object { .. }) => None,
        }
    }

    pub fn serialized_value(self) -> Cow<'a, str> {
        match self {
            Self::Dynamic(value) => match &value.string_value {
                Some(value) => Cow::Borrowed(value.value.as_str()),
                None => Cow::Owned(value.json_value.to_string()),
            },
            Self::User(UserValue::Null) => Cow::Borrowed("null"),
            Self::User(UserValue::Object {
                serialized_value, ..
            }) => Cow::Borrowed(serialized_value.get()),
            Self::User(_) => Cow::Borrowed(self.string_value().unwrap_or_default()),
        }
    }

    pub fn array_len(self) -> Option<usize> {
        match self {
            Self::Dynamic(value) => value.array_value.as_ref().map(Vec::len),
            Self::User(UserValue::Array { values, .. }) => Some(values.len()),
            Self::User(_) => None,
        }
    }

    pub fn array_item(self, index: usize) -> Option<Self> {
        match self {
            Self::Dynamic(value) => value
                .array_value
                .as_ref()?
                .get(index)
                .map(UserValueRef::Dynamic),
            Self::User(UserValue::Array { values, .. }) => {
                values.get(index).map(UserValueRef::User)
            }
            Self::User(_) => None,
        }
    }

    pub fn object_len(self) -> Option<usize> {
        match self {
            Self::Dynamic(value) => value.object_value.as_ref().map(|values| values.len()),
            Self::User(UserValue::Object { values, .. }) => Some(values.len()),
            Self::User(_) => None,
        }
    }

    pub fn object_get(self, key: &str) -> Option<Self> {
        match self {
            Self::Dynamic(value) => value
                .object_value
                .as_ref()?
                .get(key)
                .map(UserValueRef::Dynamic),
            Self::User(UserValue::Object { values, .. }) => values.get(key).map(UserValueRef::User),
            Self::User(_) => None,
        }
    }
}
