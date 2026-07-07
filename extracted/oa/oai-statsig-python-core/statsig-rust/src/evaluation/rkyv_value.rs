use std::collections::HashMap;

use rkyv::Archive;
use serde::ser::{SerializeMap, SerializeSeq};

// A bridging layer between Serde and Rkyv.
// Based on Rkyv Examples: https://github.com/rkyv/rkyv/blob/main/rkyv/examples/json_like_schema.rs
#[derive(
    Archive, Debug, rkyv::Deserialize, rkyv::Serialize, Clone, serde::Serialize, PartialEq,
)]
#[rkyv(serialize_bounds(
    __S: rkyv::ser::Writer + rkyv::ser::Allocator,
    __S::Error: rkyv::rancor::Source,
))]
#[rkyv(deserialize_bounds(__D::Error: rkyv::rancor::Source))]
#[rkyv(bytecheck(
    bounds(
        __C: rkyv::validation::ArchiveContext,
    )
))]
#[rkyv(derive(Debug, PartialEq))]
#[serde(untagged)]
pub enum RkyvValue {
    Null,
    Bool(bool),
    Number(RkyvNumber),
    String(String),
    Array(#[rkyv(omit_bounds)] Vec<RkyvValue>),
    Object(#[rkyv(omit_bounds)] HashMap<String, RkyvValue>),
}

impl RkyvValue {
    fn from_json_value(value: serde_json::Value) -> Result<Self, String> {
        match value {
            serde_json::Value::Null => Ok(Self::Null),
            serde_json::Value::Bool(value) => Ok(Self::Bool(value)),
            serde_json::Value::Number(value) => {
                if let Some(value) = value.as_u64() {
                    return Ok(Self::Number(RkyvNumber::PosInt(value)));
                }
                if let Some(value) = value.as_i64() {
                    return Ok(Self::Number(RkyvNumber::NegInt(value)));
                }
                if let Some(value) = value.as_f64().filter(|value| value.is_finite()) {
                    return Ok(Self::Number(RkyvNumber::Float(value)));
                }

                Err(format!("JSON number {value} cannot be represented"))
            }
            serde_json::Value::String(value) => Ok(Self::String(value)),
            serde_json::Value::Array(values) => values
                .into_iter()
                .map(Self::from_json_value)
                .collect::<Result<_, _>>()
                .map(Self::Array),
            serde_json::Value::Object(values) => values
                .into_iter()
                .map(|(key, value)| Self::from_json_value(value).map(|value| (key, value)))
                .collect::<Result<_, _>>()
                .map(Self::Object),
        }
    }
}

impl<'de> serde::Deserialize<'de> for RkyvValue {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        // serde_json represents numbers as a private marker map while buffering an
        // untagged enum when its arbitrary_precision feature is enabled. Let Value's
        // deserializer consume that representation before mapping into the rkyv schema.
        let value = <serde_json::Value as serde::Deserialize>::deserialize(deserializer)?;
        Self::from_json_value(value).map_err(serde::de::Error::custom)
    }
}

impl serde::Serialize for ArchivedRkyvValue {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        match self {
            ArchivedRkyvValue::Null => serializer.serialize_none(),
            ArchivedRkyvValue::Bool(b) => serializer.serialize_bool(*b),
            ArchivedRkyvValue::Number(n) => n.serialize(serializer),
            ArchivedRkyvValue::String(s) => serializer.serialize_str(s),
            ArchivedRkyvValue::Array(a) => {
                let mut seq = serializer.serialize_seq(Some(a.len()))?;
                for element in a.iter() {
                    seq.serialize_element(&element)?;
                }
                seq.end()
            }
            ArchivedRkyvValue::Object(o) => {
                let mut map = serializer.serialize_map(Some(o.len()))?;

                for (k, v) in o.iter() {
                    map.serialize_entry(k.as_str(), v)?;
                }

                map.end()
            }
        }
    }
}

impl PartialEq<ArchivedRkyvValue> for RkyvValue {
    fn eq(&self, other: &ArchivedRkyvValue) -> bool {
        match (self, other) {
            (RkyvValue::Null, ArchivedRkyvValue::Null) => true,
            (RkyvValue::Bool(a), ArchivedRkyvValue::Bool(b)) => a == b,
            (RkyvValue::Number(a), ArchivedRkyvValue::Number(b)) => a == b,
            (RkyvValue::String(a), ArchivedRkyvValue::String(b)) => a == b.as_str(),
            (RkyvValue::Array(a), ArchivedRkyvValue::Array(b)) => {
                a.len() == b.len() && a.iter().zip(b.iter()).all(|(a, b)| a == b)
            }
            (RkyvValue::Object(a), ArchivedRkyvValue::Object(b)) => {
                a.len() == b.len()
                    && b.iter()
                        .all(|(key, value)| a.get(key.as_str()).is_some_and(|v| v == value))
            }
            _ => false,
        }
    }
}

impl PartialEq<RkyvValue> for ArchivedRkyvValue {
    fn eq(&self, other: &RkyvValue) -> bool {
        other == self
    }
}

// ------------------------------------------------------------------------------- [ RkyvNumber ]

#[derive(
    Archive,
    Debug,
    rkyv::Deserialize,
    rkyv::Serialize,
    Clone,
    serde::Serialize,
    serde::Deserialize,
    PartialEq,
)]
#[rkyv(derive(Debug, PartialEq))]
#[serde(untagged)]
pub enum RkyvNumber {
    PosInt(u64),
    NegInt(i64),
    Float(f64),
}

impl serde::Serialize for ArchivedRkyvNumber {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        match self {
            ArchivedRkyvNumber::PosInt(n) => serializer.serialize_u64(n.to_native()),
            ArchivedRkyvNumber::NegInt(n) => serializer.serialize_i64(n.to_native()),
            ArchivedRkyvNumber::Float(n) => serializer.serialize_f64(n.to_native()),
        }
    }
}

impl PartialEq<ArchivedRkyvNumber> for RkyvNumber {
    fn eq(&self, other: &ArchivedRkyvNumber) -> bool {
        match (self, other) {
            (RkyvNumber::PosInt(a), ArchivedRkyvNumber::PosInt(b)) => a == b,
            (RkyvNumber::NegInt(a), ArchivedRkyvNumber::NegInt(b)) => a == b,
            (RkyvNumber::Float(a), ArchivedRkyvNumber::Float(b)) => a == b,
            _ => false,
        }
    }
}

impl PartialEq<RkyvNumber> for ArchivedRkyvNumber {
    fn eq(&self, other: &RkyvNumber) -> bool {
        other == self
    }
}
