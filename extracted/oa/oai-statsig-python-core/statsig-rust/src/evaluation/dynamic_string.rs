use serde::{Deserialize, Deserializer, Serialize, Serializer};
use serde_json::Value;

use crate::{hashing::ahash_str, interned_string::InternedString};

lazy_static::lazy_static! {
    static ref USER_ID: DynamicString = DynamicString::from("userID".to_string());
    static ref STABLE_ID: DynamicString = DynamicString::from("stableID".to_string());
}

#[derive(Clone, Eq, Debug)]
pub struct DynamicString {
    pub value: InternedString,
    pub lowercased_value: InternedString,
    pub hash_value: u64,
}

impl DynamicString {
    pub fn user_id() -> Self {
        USER_ID.clone()
    }

    pub fn stable_id() -> Self {
        STABLE_ID.clone()
    }

    pub fn from_bool(value: bool) -> Self {
        let raw = if value { "true" } else { "false" };
        Self {
            value: InternedString::from_bool(value),
            lowercased_value: InternedString::from_bool(value),
            hash_value: ahash_str(raw),
        }
    }
}

// ------------------------------------------------------------------------------- [Serialization]

impl Serialize for DynamicString {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        if let Ok(bool_value) = self.value.parse::<bool>() {
            return serializer.serialize_bool(bool_value);
        }

        serializer.serialize_str(&self.value)
    }
}

impl<'de> Deserialize<'de> for DynamicString {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let value = String::deserialize(deserializer)?;
        Ok(DynamicString::from(value))
    }
}

// ------------------------------------------------------------------------------- [PartialEq]

impl PartialEq for DynamicString {
    fn eq(&self, other: &Self) -> bool {
        self.value == other.value
    }
}

impl PartialEq<&str> for DynamicString {
    fn eq(&self, other: &&str) -> bool {
        self.value.as_str() == *other
    }
}

impl PartialEq<String> for DynamicString {
    fn eq(&self, other: &String) -> bool {
        self.value == *other
    }
}

impl PartialEq<&String> for DynamicString {
    fn eq(&self, other: &&String) -> bool {
        self.value.as_str() == other.as_str()
    }
}

// ------------------------------------------------------------------------------- [From<T> Implementations]

impl From<Value> for DynamicString {
    fn from(value: Value) -> Self {
        let str_value = match value.as_str() {
            Some(value) => value.to_string(),
            None => value.to_string(),
        };
        DynamicString::from(str_value)
    }
}

impl From<String> for DynamicString {
    fn from(value: String) -> Self {
        let hash_value = ahash_str(&value);
        let value = InternedString::from_string(value);
        let lowercased_value = if value.as_str().bytes().any(|byte| byte.is_ascii_uppercase()) {
            InternedString::from_string(value.as_str().to_lowercase())
        } else {
            value.clone()
        };

        Self {
            value,
            lowercased_value,
            hash_value,
        }
    }
}
