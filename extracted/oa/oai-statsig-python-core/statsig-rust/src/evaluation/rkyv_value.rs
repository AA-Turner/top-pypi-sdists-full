use std::{
    collections::{BTreeMap, HashMap},
    fmt,
};

use rkyv::Archive;
use serde::{
    Deserialize, Deserializer,
    de::{DeserializeSeed, Error, MapAccess, SeqAccess, Visitor},
    ser::{SerializeMap, SerializeSeq},
};
use serde_json::{Number, Value};

use crate::hashing;

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

    fn push_stable_hash(&self, values: &mut hashing::U64HashBuilder) {
        match self {
            Self::Null => values.push(0),
            Self::Bool(value) => {
                values.push(1);
                values.push(u64::from(*value));
            }
            Self::Number(value) => {
                values.push(2);
                match value {
                    RkyvNumber::PosInt(value) => {
                        values.push(0);
                        values.push(*value);
                    }
                    RkyvNumber::NegInt(value) => {
                        values.push(1);
                        values.push(*value as u64);
                    }
                    RkyvNumber::Float(value) => {
                        values.push(2);
                        values.push(value.to_bits());
                    }
                }
            }
            Self::String(value) => {
                values.push(3);
                values.push(hashing::hash_one(value.as_bytes()));
            }
            Self::Array(array) => {
                values.push(4);
                values.push(array.len() as u64);
                for value in array {
                    value.push_stable_hash(values);
                }
            }
            Self::Object(object) => {
                values.push(5);
                push_stable_object_hash(
                    values,
                    object.iter().map(|(key, value)| (key.as_str(), value)),
                );
            }
        }
    }
}

impl ArchivedRkyvValue {
    fn push_stable_hash(&self, values: &mut hashing::U64HashBuilder) {
        match self {
            Self::Null => values.push(0),
            Self::Bool(value) => {
                values.push(1);
                values.push(u64::from(*value));
            }
            Self::Number(value) => {
                values.push(2);
                match value {
                    ArchivedRkyvNumber::PosInt(value) => {
                        values.push(0);
                        values.push(value.to_native());
                    }
                    ArchivedRkyvNumber::NegInt(value) => {
                        values.push(1);
                        values.push(value.to_native() as u64);
                    }
                    ArchivedRkyvNumber::Float(value) => {
                        values.push(2);
                        values.push(value.to_native().to_bits());
                    }
                }
            }
            Self::String(value) => {
                values.push(3);
                values.push(hashing::hash_one(value.as_bytes()));
            }
            Self::Array(array) => {
                values.push(4);
                values.push(array.len() as u64);
                for value in array.iter() {
                    value.push_stable_hash(values);
                }
            }
            Self::Object(object) => {
                values.push(5);
                push_stable_object_hash(
                    values,
                    object.iter().map(|(key, value)| (key.as_str(), value)),
                );
            }
        }
    }
}

pub(crate) trait StableHashValue {
    fn push_hash(&self, values: &mut hashing::U64HashBuilder);
}

impl StableHashValue for RkyvValue {
    fn push_hash(&self, values: &mut hashing::U64HashBuilder) {
        self.push_stable_hash(values);
    }
}

impl StableHashValue for ArchivedRkyvValue {
    fn push_hash(&self, values: &mut hashing::U64HashBuilder) {
        self.push_stable_hash(values);
    }
}

pub(crate) fn stable_object_hash<'a, T: StableHashValue + 'a>(
    entries: impl Iterator<Item = (&'a str, &'a T)>,
) -> u64 {
    let mut values = hashing::U64HashBuilder::new();
    values.push(2);
    push_stable_object_hash(&mut values, entries);
    values.finish()
}

pub(crate) fn push_stable_object_hash<'a, T: StableHashValue + 'a>(
    values: &mut hashing::U64HashBuilder,
    entries: impl Iterator<Item = (&'a str, &'a T)>,
) {
    let mut entries = entries.collect::<Vec<_>>();
    entries.sort_unstable_by_key(|(key, _)| *key);
    values.push(entries.len() as u64);
    for (key, value) in entries {
        values.push(hashing::hash_one(key.as_bytes()));
        value.push_hash(values);
    }
}

impl<'de> Deserialize<'de> for RkyvValue {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        RkyvValueVisitor
            .deserialize(deserializer)?
            .map_err(D::Error::custom)
    }
}

struct RkyvValueVisitor;

impl<'de> DeserializeSeed<'de> for RkyvValueVisitor {
    // Serde errors stop the parse. A number conversion error is a decoded
    // result until we know that a later duplicate key hasn't overwritten it.
    type Value = Result<RkyvValue, String>;

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_any(self)
    }
}

impl<'de> Visitor<'de> for RkyvValueVisitor {
    type Value = Result<RkyvValue, String>;

    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str("any valid JSON value")
    }
    fn visit_unit<E: Error>(self) -> Result<Self::Value, E> {
        Ok(Ok(RkyvValue::Null))
    }
    fn visit_none<E: Error>(self) -> Result<Self::Value, E> {
        self.visit_unit()
    }
    fn visit_some<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        self.deserialize(deserializer)
    }
    fn visit_bool<E: Error>(self, v: bool) -> Result<Self::Value, E> {
        Ok(Ok(RkyvValue::Bool(v)))
    }
    fn visit_u64<E: Error>(self, v: u64) -> Result<Self::Value, E> {
        Ok(Ok(RkyvValue::Number(RkyvNumber::PosInt(v))))
    }
    fn visit_i64<E: Error>(self, v: i64) -> Result<Self::Value, E> {
        // serde_json classifies nonnegative signed integers as unsigned.
        let number = if v < 0 {
            RkyvNumber::NegInt(v)
        } else {
            RkyvNumber::PosInt(v as u64)
        };
        Ok(Ok(RkyvValue::Number(number)))
    }
    fn visit_f64<E: Error>(self, v: f64) -> Result<Self::Value, E> {
        Ok(Number::from_f64(v).map_or(Ok(RkyvValue::Null), decode_number))
    }
    fn visit_i128<E: Error>(self, v: i128) -> Result<Self::Value, E> {
        Number::deserialize(serde::de::value::I128Deserializer::<E>::new(v)).map(decode_number)
    }
    fn visit_u128<E: Error>(self, v: u128) -> Result<Self::Value, E> {
        Number::deserialize(serde::de::value::U128Deserializer::<E>::new(v)).map(decode_number)
    }
    fn visit_str<E: Error>(self, v: &str) -> Result<Self::Value, E> {
        self.visit_string(v.to_owned())
    }
    fn visit_string<E: Error>(self, v: String) -> Result<Self::Value, E> {
        Ok(Ok(RkyvValue::String(v)))
    }
    fn visit_seq<A: SeqAccess<'de>>(self, mut a: A) -> Result<Self::Value, A::Error> {
        let mut values = Vec::new();
        let mut error = None;
        while let Some(v) = a.next_element_seed(RkyvValueVisitor)? {
            match v {
                Ok(v) if error.is_none() => values.push(v),
                Err(e) if error.is_none() => error = Some(e),
                _ => {}
            }
        }
        Ok(error.map_or_else(|| Ok(RkyvValue::Array(values)), Err))
    }
    fn visit_map<A: MapAccess<'de>>(self, mut a: A) -> Result<Self::Value, A::Error> {
        let mut key = match a.next_key_seed(FirstKeyVisitor)? {
            None => return Ok(Ok(RkyvValue::Object(HashMap::new()))),
            Some(FirstKey::Map(key)) => key,
            Some(FirstKey::Marker(marker)) => {
                // Replay fixed markers without allocating their names. Value
                // retains serde_json's feature-sensitive and generic handling:
                // without arbitrary_precision, Number is an ordinary user key.
                let value = Value::deserialize(serde::de::value::MapAccessDeserializer::new(
                    FirstKeyMapAccess {
                        first: Some(marker),
                        rest: a,
                    },
                ))?;
                return Ok(RkyvValue::from_json_value(value));
            }
        };
        let mut values = HashMap::new();
        // Keep errors by key so a later duplicate can replace an invalid value.
        let mut invalid = BTreeMap::new();
        loop {
            match a.next_value_seed(RkyvValueVisitor)? {
                Ok(value) => {
                    invalid.remove(&key);
                    values.insert(key, value);
                }
                Err(error) => {
                    values.remove(&key);
                    invalid.insert(key, error);
                }
            }
            match a.next_key::<String>()? {
                Some(next) => key = next,
                None => break,
            }
        }
        Ok(match invalid.into_iter().next() {
            Some((_, e)) => Err(e),
            None => Ok(RkyvValue::Object(values)),
        })
    }
}
enum FirstKey {
    Marker(&'static str),
    Map(String),
}

impl FirstKey {
    fn marker(value: &str) -> Option<Self> {
        match value {
            "$serde_json::private::Number" => Some(Self::Marker("$serde_json::private::Number")),
            "$serde_json::private::RawValue" => {
                Some(Self::Marker("$serde_json::private::RawValue"))
            }
            _ => None,
        }
    }
}

// Value's first key only accepts string callbacks. Subsequent keys deliberately
// still use String, matching its broader generic-Serde behavior for later keys.
struct FirstKeyVisitor;

impl<'de> DeserializeSeed<'de> for FirstKeyVisitor {
    type Value = FirstKey;

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl<'de> Visitor<'de> for FirstKeyVisitor {
    type Value = FirstKey;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a string key")
    }

    fn visit_str<E: Error>(self, value: &str) -> Result<Self::Value, E> {
        Ok(FirstKey::marker(value).unwrap_or_else(|| FirstKey::Map(value.to_owned())))
    }

    fn visit_string<E: Error>(self, value: String) -> Result<Self::Value, E> {
        Ok(FirstKey::marker(&value).unwrap_or(FirstKey::Map(value)))
    }
}

struct FirstKeyMapAccess<M> {
    first: Option<&'static str>,
    rest: M,
}
impl<'de, M: MapAccess<'de>> MapAccess<'de> for FirstKeyMapAccess<M> {
    type Error = M::Error;
    fn next_key_seed<K: DeserializeSeed<'de>>(
        &mut self,
        seed: K,
    ) -> Result<Option<K::Value>, Self::Error> {
        match self.first.take() {
            Some(key) => seed
                .deserialize(serde::de::value::StrDeserializer::<Self::Error>::new(key))
                .map(Some),
            None => self.rest.next_key_seed(seed),
        }
    }
    fn next_value_seed<VS: DeserializeSeed<'de>>(
        &mut self,
        seed: VS,
    ) -> Result<VS::Value, Self::Error> {
        self.rest.next_value_seed(seed)
    }
}

fn decode_number(number: Number) -> Result<RkyvValue, String> {
    RkyvValue::from_json_value(Value::Number(number))
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
