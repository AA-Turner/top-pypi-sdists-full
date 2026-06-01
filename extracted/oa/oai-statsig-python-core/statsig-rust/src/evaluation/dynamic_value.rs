use serde::{Deserialize, Deserializer, Serialize, Serializer};
use serde_json::{json, Map as JsonMap, Number as JsonNumber, Value as JsonValue};
use std::{collections::HashMap, fmt::Debug};

use crate::{
    hashing::{self, ahash_str},
    log_w,
    value_parsing::{maybe_parse_f64, maybe_parse_i64, try_parse_timestamp},
};

use super::dynamic_string::DynamicString;

const TAG: &str = "DynamicValue";

#[macro_export]
macro_rules! dyn_value {
    ($x:expr) => {{
        $crate::DynamicValue::from_json_value($x)
    }};
}

#[derive(Debug, Clone, Default)]
pub struct DynamicValue {
    pub null: Option<()>,
    pub bool_value: Option<bool>,
    pub int_value: Option<i64>,
    pub float_value: Option<f64>,
    pub timestamp_value: Option<i64>,
    pub string_value: Option<DynamicString>,
    pub array_value: Option<Vec<DynamicValue>>,
    pub object_value: Option<HashMap<String, DynamicValue>>,
    pub json_value: JsonValue,
    pub hash_value: u64,
}

impl DynamicValue {
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    #[must_use]
    pub fn from_json_value(value: impl Serialize) -> Self {
        Self::from(json!(value))
    }

    #[must_use]
    pub fn for_timestamp_evaluation(timestamp: i64) -> DynamicValue {
        DynamicValue {
            int_value: Some(timestamp),
            ..DynamicValue::default()
        }
    }

    #[must_use]
    pub fn from_string(value: impl Into<String>) -> Self {
        let value = value.into();
        let int_value = maybe_parse_i64(&value);
        let float_value = maybe_parse_f64(&value);
        let timestamp_value = try_parse_timestamp(&value, int_value);
        let hash_value = ahash_str(&value);

        DynamicValue {
            string_value: Some(DynamicString::from(value.clone())),
            json_value: JsonValue::String(value),
            timestamp_value,
            int_value,
            float_value,
            hash_value,
            ..DynamicValue::new()
        }
    }

    #[must_use]
    pub fn from_bool(value: bool) -> Self {
        let string_value = if value { "true" } else { "false" };

        DynamicValue {
            bool_value: Some(value),
            string_value: Some(DynamicString::from_bool(value)),
            json_value: JsonValue::Bool(value),
            hash_value: ahash_str(string_value),
            ..DynamicValue::new()
        }
    }

    #[must_use]
    pub fn from_i64(value: i64) -> Self {
        let string_value = value.to_string();

        DynamicValue {
            int_value: Some(value),
            float_value: Some(value as f64),
            string_value: Some(DynamicString::from(string_value.clone())),
            json_value: JsonValue::Number(JsonNumber::from(value)),
            hash_value: ahash_str(&string_value),
            ..DynamicValue::new()
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

        let json_string = JsonValue::Number(num.clone()).to_string();
        let mut float_value = num.as_f64();
        let mut int_value = num.as_i64();
        if let (Some(f), None) = (float_value, int_value) {
            let iv = f as i64;
            if iv as f64 == f {
                int_value = Some(iv);
            }
        } else if let (None, Some(i)) = (float_value, int_value) {
            let fv = i as f64;
            if fv as i64 == i {
                float_value = Some(fv)
            }
        }

        let string_value = float_value
            .map(|f| f.to_string())
            .or_else(|| int_value.map(|i| i.to_string()))
            .unwrap_or_else(|| json_string.clone());

        DynamicValue {
            float_value,
            int_value,
            string_value: Some(DynamicString::from(string_value)),
            json_value: JsonValue::Number(num),
            hash_value: ahash_str(&json_string),
            ..DynamicValue::new()
        }
    }

    #[must_use]
    pub fn from_dynamic_array(value: Vec<DynamicValue>) -> Self {
        let json_value =
            JsonValue::Array(value.iter().map(|value| value.json_value.clone()).collect());
        let string_value = DynamicString::from(json_value.to_string());
        let hash_value = hashing::hash_one(
            value
                .iter()
                .map(|value| value.hash_value)
                .collect::<Vec<_>>(),
        );

        DynamicValue {
            hash_value,
            array_value: Some(value),
            json_value,
            string_value: Some(string_value),
            ..DynamicValue::default()
        }
    }

    #[must_use]
    pub fn from_dynamic_object(value: HashMap<String, DynamicValue>) -> Self {
        let json_value = JsonValue::Object(
            value
                .iter()
                .map(|(key, value)| (key.clone(), value.json_value.clone()))
                .collect::<JsonMap<String, JsonValue>>(),
        );
        let hash_value = hashing::hash_one(
            value
                .values()
                .map(|value| value.hash_value)
                .collect::<Vec<_>>(),
        );

        DynamicValue {
            hash_value,
            object_value: Some(value),
            json_value,
            ..DynamicValue::default()
        }
    }
}

impl PartialEq for DynamicValue {
    fn eq(&self, other: &Self) -> bool {
        self.null == other.null
            && self.bool_value == other.bool_value
            && self.int_value == other.int_value
            && self.float_value == other.float_value
            && self.string_value == other.string_value
            && self.array_value == other.array_value
            && self.object_value == other.object_value
    }
}

// ------------------------------------------------------------------------------- [Serialization]

impl Serialize for DynamicValue {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.json_value.serialize(serializer)
    }
}

impl<'de> Deserialize<'de> for DynamicValue {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let json_value = JsonValue::deserialize(deserializer)?;
        Ok(DynamicValue::from(json_value))
    }
}

// ------------------------------------------------------------------------------- [From<T> Implementations]

impl From<JsonValue> for DynamicValue {
    fn from(json_value: JsonValue) -> Self {
        // perf optimization: avoid stringifying the json value if it's already a string
        let mut stringified_json_value = None;
        let hash_value = if let JsonValue::String(s) = &json_value {
            ahash_str(s)
        } else {
            let actual = json_value.to_string();
            let hash = ahash_str(&actual);
            stringified_json_value = Some(actual);
            hash
        };

        match &json_value {
            JsonValue::Null => DynamicValue {
                null: Some(()),
                json_value,
                hash_value,
                ..DynamicValue::new()
            },

            JsonValue::Bool(b) => DynamicValue {
                bool_value: Some(*b),
                string_value: Some(DynamicString::from(b.to_string())),
                json_value,
                hash_value,
                ..DynamicValue::new()
            },

            JsonValue::Number(n) => {
                let mut float_value = n.as_f64();
                let mut int_value = n.as_i64();
                if let (Some(f), None) = (float_value, int_value) {
                    let iv = f as i64;
                    if iv as f64 == f {
                        int_value = Some(iv);
                    }
                } else if let (None, Some(i)) = (float_value, int_value) {
                    let fv = i as f64;
                    if fv as i64 == i {
                        float_value = Some(fv)
                    }
                }

                let string_value = float_value
                    .map(|f| f.to_string())
                    .or_else(|| int_value.map(|i| i.to_string()))
                    .or(stringified_json_value);

                DynamicValue {
                    float_value,
                    int_value,
                    string_value: string_value.map(DynamicString::from),
                    json_value,
                    hash_value,
                    ..DynamicValue::new()
                }
            }

            JsonValue::String(s) => {
                let int_value = maybe_parse_i64(s);
                let float_value = maybe_parse_f64(s);
                let timestamp_value = try_parse_timestamp(s, int_value);
                DynamicValue {
                    string_value: Some(DynamicString::from(s.clone())),
                    json_value,
                    timestamp_value,
                    int_value,
                    float_value,
                    hash_value,
                    ..DynamicValue::new()
                }
            }

            JsonValue::Array(arr) => DynamicValue {
                array_value: Some(arr.iter().map(|v| DynamicValue::from(v.clone())).collect()),
                string_value: Some(DynamicString::from(
                    stringified_json_value.unwrap_or(json_value.to_string()),
                )),
                json_value,
                hash_value,
                ..DynamicValue::new()
            },

            JsonValue::Object(obj) => DynamicValue {
                object_value: Some(
                    obj.into_iter()
                        .map(|(k, v)| (k.clone(), DynamicValue::from(v.clone())))
                        .collect(),
                ),
                json_value,
                hash_value,
                ..DynamicValue::new()
            },
        }
    }
}

impl From<String> for DynamicValue {
    fn from(value: String) -> Self {
        Self::from_string(value)
    }
}

impl From<&str> for DynamicValue {
    fn from(value: &str) -> Self {
        Self::from_string(value)
    }
}

impl From<usize> for DynamicValue {
    fn from(value: usize) -> Self {
        Self::from(serde_json::Value::Number(serde_json::Number::from(value)))
    }
}

impl From<i64> for DynamicValue {
    fn from(value: i64) -> Self {
        Self::from_i64(value)
    }
}

impl From<i32> for DynamicValue {
    fn from(value: i32) -> Self {
        Self::from_i64(i64::from(value))
    }
}

impl From<f64> for DynamicValue {
    fn from(value: f64) -> Self {
        Self::from_f64(value)
    }
}

impl From<bool> for DynamicValue {
    fn from(value: bool) -> Self {
        Self::from_bool(value)
    }
}

impl From<Vec<JsonValue>> for DynamicValue {
    fn from(value: Vec<JsonValue>) -> Self {
        DynamicValue::from(serde_json::Value::Array(value))
    }
}

impl From<Vec<DynamicValue>> for DynamicValue {
    fn from(value: Vec<DynamicValue>) -> Self {
        Self::from_dynamic_array(value)
    }
}

impl From<HashMap<String, DynamicValue>> for DynamicValue {
    fn from(value: HashMap<String, DynamicValue>) -> Self {
        Self::from_dynamic_object(value)
    }
}
