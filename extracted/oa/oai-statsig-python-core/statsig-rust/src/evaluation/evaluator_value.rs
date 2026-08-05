use ahash::HashMap as AHashMap;
use fancy_regex::Regex as FancyRegex;
use serde::{
    Deserialize, Deserializer, Serialize, Serializer,
    ser::{SerializeMap, SerializeSeq},
};
use serde_json::{
    Value as JsonValue, Value,
    value::{RawValue, to_raw_value},
};
use std::{borrow::Cow, sync::Arc};

use crate::{DynamicValue, user::user_value::UserValueRef};
use crate::{
    evaluation::evaluation_data::InternedStrRef,
    hashing,
    interned_string::InternedString,
    interned_values::{
        InternedStore,
        mmap_data_v2::{ArchivedMmapEvaluatorValue, ArchivedMmapEvaluatorValueType},
    },
    log_e,
    value_parsing::try_parse_timestamp,
};

use super::dynamic_string::DynamicString;

lazy_static::lazy_static! {
    pub(crate) static ref EMPTY_EVALUATOR_VALUE: EvaluatorValue = EvaluatorValue {
        hash: 0,
        inner: EvaluatorValueInner::Pointer(Arc::new(MemoizedEvaluatorValue::new(EvaluatorValueType::Null))),
    };
}

const TAG: &str = "EvaluatorValue";

#[derive(Clone)]
#[non_exhaustive]
pub enum EvaluatorValueInner {
    Pointer(Arc<MemoizedEvaluatorValue>),
    Static(&'static MemoizedEvaluatorValue),
    Mmap(MmapEvaluatorValueHandle),
}

#[derive(Clone, Copy)]
pub struct MmapEvaluatorValueHandle {
    value: &'static ArchivedMmapEvaluatorValue,
    regex: Option<&'static FancyRegex>,
}

impl MmapEvaluatorValueHandle {
    pub(crate) fn new(
        value: &'static ArchivedMmapEvaluatorValue,
        regex: Option<&'static FancyRegex>,
    ) -> Self {
        Self { value, regex }
    }
}

impl std::fmt::Debug for EvaluatorValueInner {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Pointer(value) => formatter.debug_tuple("Pointer").field(value).finish(),
            Self::Static(value) => formatter.debug_tuple("Static").field(value).finish(),
            Self::Mmap(_) => formatter.write_str("Mmap"),
        }
    }
}

#[derive(Clone, Debug)]
pub struct EvaluatorValue {
    pub hash: u64,
    pub inner: EvaluatorValueInner,
}

impl EvaluatorValue {
    pub fn empty() -> &'static Self {
        &EMPTY_EVALUATOR_VALUE
    }

    pub fn from_json_value(value: Value) -> Self {
        let raw_value = match to_raw_value(&value) {
            Ok(raw_value) => raw_value,
            Err(e) => {
                log_e!(TAG, "Failed to convert map to raw value: {}", e);
                return Self::empty().clone();
            }
        };

        InternedStore::get_or_intern_evaluator_value(Cow::Owned(raw_value))
    }

    pub fn compile_regex(&mut self) {
        match &mut self.inner {
            EvaluatorValueInner::Pointer(inner) => {
                if inner.regex_value.is_some() {
                    return;
                }

                let mut_inner = Arc::make_mut(inner);
                mut_inner.compile_regex();
                InternedStore::replace_evaluator_value(self.hash, inner.clone());
            }
            EvaluatorValueInner::Static(inner) => {
                if inner.regex_value.is_some() {
                    return;
                }

                // static values are immutable and should already be compiled during `InternedStore::preload(..)`
                log_e!(TAG, "Cannot compile regex for static EvaluatorValue");
            }
            EvaluatorValueInner::Mmap(handle) => {
                if handle.regex.is_some() {
                    return;
                }

                let handle = *handle;
                let mut materialized = InternedStore::materialize_mmap_evaluator_value_owned(
                    handle.value,
                    handle.regex,
                );
                materialized.compile_regex();
                let inner = Arc::new(materialized);
                InternedStore::replace_mmap_evaluator_value(self.hash, inner.clone());
                self.inner = EvaluatorValueInner::Pointer(inner);
            }
        }
    }
}

impl AsRef<MemoizedEvaluatorValue> for EvaluatorValue {
    fn as_ref(&self) -> &MemoizedEvaluatorValue {
        match &self.inner {
            EvaluatorValueInner::Pointer(inner) => inner,
            EvaluatorValueInner::Static(inner) => inner,
            EvaluatorValueInner::Mmap(handle) => InternedStore::materialize_mmap_evaluator_value(
                self.hash,
                handle.value,
                handle.regex,
            ),
        }
    }
}

#[derive(Clone, Copy)]
pub(crate) enum EvaluatorValueRef<'a> {
    Owned(&'a MemoizedEvaluatorValue),
    Mmap(&'a ArchivedMmapEvaluatorValue, Option<&'a FancyRegex>),
}

impl<'a> From<&'a MemoizedEvaluatorValue> for EvaluatorValueRef<'a> {
    fn from(value: &'a MemoizedEvaluatorValue) -> Self {
        Self::Owned(value)
    }
}

impl EvaluatorValue {
    pub(crate) fn as_value_ref(&self) -> EvaluatorValueRef<'_> {
        match &self.inner {
            EvaluatorValueInner::Pointer(value) => EvaluatorValueRef::Owned(value),
            EvaluatorValueInner::Static(value) => EvaluatorValueRef::Owned(value),
            EvaluatorValueInner::Mmap(handle) => {
                EvaluatorValueRef::Mmap(handle.value, handle.regex)
            }
        }
    }
}

impl<'a> EvaluatorValueRef<'a> {
    pub(crate) fn bool_value(self) -> Option<bool> {
        match self {
            Self::Owned(value) => value.bool_value,
            Self::Mmap(value, _) => value.bool_value.as_ref().copied(),
        }
    }

    pub(crate) fn float_value(self) -> Option<f64> {
        match self {
            Self::Owned(value) => value.float_value,
            Self::Mmap(value, _) => value.float_value.as_ref().map(|value| value.to_native()),
        }
    }

    pub(crate) fn string_value(self) -> Option<&'a str> {
        match self {
            Self::Owned(value) => value
                .string_value
                .as_ref()
                .map(|value| value.value.as_str()),
            Self::Mmap(value, _) => {
                let hash = value.string_value.as_ref().map(|hash| hash.to_native())?;
                InternedStore::get_mmap_string(hash)
            }
        }
    }

    pub(crate) fn interned_string_value(self) -> Option<InternedStrRef<'a>> {
        match self {
            Self::Owned(value) => value
                .string_value
                .as_ref()
                .map(|value| (&value.value).into()),
            Self::Mmap(value, _) => value
                .string_value
                .as_ref()
                .map(|hash| InternedStrRef::from_mmap(hash.to_native())),
        }
    }

    pub(crate) fn regex_value(self) -> Option<&'a FancyRegex> {
        match self {
            Self::Owned(value) => value.regex_value.as_ref(),
            Self::Mmap(_, regex) => regex,
        }
    }

    pub(crate) fn timestamp_value(self) -> Option<i64> {
        match self {
            Self::Owned(value) => value.timestamp_value,
            Self::Mmap(value, _) => value
                .timestamp_value
                .as_ref()
                .map(|value| value.to_native()),
        }
    }

    pub(crate) fn array_len(self) -> Option<usize> {
        match self {
            Self::Owned(value) => value.array_value.as_ref().map(AHashMap::len),
            Self::Mmap(value, _) => value.array_value.as_ref().map(|value| value.len()),
        }
    }

    pub(crate) fn object_len(self) -> Option<usize> {
        match self {
            Self::Owned(value) => value.object_value.as_ref().map(AHashMap::len),
            Self::Mmap(value, _) => value.object_value.as_ref().map(|value| value.len()),
        }
    }

    pub(crate) fn array_contains_key(self, key: &InternedString) -> bool {
        match self {
            Self::Owned(value) => value
                .array_value
                .as_ref()
                .is_some_and(|array| array.contains_key(key)),
            Self::Mmap(value, _) => value.array_value.as_ref().is_some_and(|array| {
                array.contains_key(&rkyv::primitive::ArchivedU64::from_native(key.hash))
            }),
        }
    }

    pub(crate) fn array_contains_lowercase(self, key: &str) -> bool {
        match self {
            Self::Owned(value) => value
                .array_value
                .as_ref()
                .is_some_and(|array| array.keys().any(|candidate| candidate.as_str() == key)),
            Self::Mmap(value, _) => value.array_value.as_ref().is_some_and(|array| {
                let hash = hashing::hash_one(key.as_bytes());
                array.contains_key(&rkyv::primitive::ArchivedU64::from_native(hash))
            }),
        }
    }

    pub(crate) fn object_contains_key(self, key: &InternedString) -> bool {
        match self {
            Self::Owned(value) => value
                .object_value
                .as_ref()
                .is_some_and(|object| object.contains_key(key)),
            Self::Mmap(value, _) => value.object_value.as_ref().is_some_and(|object| {
                object.contains_key(&rkyv::primitive::ArchivedU64::from_native(key.hash))
            }),
        }
    }

    pub(crate) fn object_contains_key_str(self, key: &str) -> bool {
        match self {
            Self::Owned(value) => value
                .object_value
                .as_ref()
                .is_some_and(|object| object.keys().any(|candidate| candidate.as_str() == key)),
            Self::Mmap(value, _) => value.object_value.as_ref().is_some_and(|object| {
                let hash = hashing::hash_one(key.as_bytes());
                object.contains_key(&rkyv::primitive::ArchivedU64::from_native(hash))
            }),
        }
    }

    pub(crate) fn any_array_entry(
        self,
        mut predicate: impl FnMut(&str, usize, &str) -> bool,
    ) -> bool {
        match self {
            Self::Owned(value) => value.array_value.as_ref().is_some_and(|array| {
                array.iter().any(|(lowercase, (index, original))| {
                    predicate(lowercase.as_str(), *index, original.as_str())
                })
            }),
            Self::Mmap(value, _) => value.array_value.as_ref().is_some_and(|array| {
                array.iter().any(|(lowercase, entry)| {
                    let Some(lowercase) = InternedStore::get_mmap_string(lowercase.to_native())
                    else {
                        return false;
                    };
                    let Some(original) = InternedStore::get_mmap_string(entry.1.to_native()) else {
                        return false;
                    };
                    predicate(lowercase, entry.0.to_native() as usize, original)
                })
            }),
        }
    }

    fn all_array_entries(self, mut predicate: impl FnMut(&str, usize, &str) -> bool) -> bool {
        match self {
            Self::Owned(value) => value.array_value.as_ref().is_some_and(|array| {
                array.iter().all(|(lowercase, (index, original))| {
                    predicate(lowercase.as_str(), *index, original.as_str())
                })
            }),
            Self::Mmap(value, _) => value.array_value.as_ref().is_some_and(|array| {
                array.iter().all(|(lowercase, entry)| {
                    let Some(lowercase) = InternedStore::get_mmap_string(lowercase.to_native())
                    else {
                        return false;
                    };
                    let Some(original) = InternedStore::get_mmap_string(entry.1.to_native()) else {
                        return false;
                    };
                    predicate(lowercase, entry.0.to_native() as usize, original)
                })
            }),
        }
    }

    fn all_object_entries(self, mut predicate: impl FnMut(&str, &str) -> bool) -> bool {
        match self {
            Self::Owned(value) => value.object_value.as_ref().is_some_and(|object| {
                object
                    .iter()
                    .all(|(key, value)| predicate(key.as_str(), value.value.as_str()))
            }),
            Self::Mmap(value, _) => value.object_value.as_ref().is_some_and(|object| {
                object.iter().all(|(key, value)| {
                    let Some(key) = InternedStore::get_mmap_string(key.to_native()) else {
                        return false;
                    };
                    let Some(value) = InternedStore::get_mmap_string(value.to_native()) else {
                        return false;
                    };
                    predicate(key, value)
                })
            }),
        }
    }

    fn value_type(self) -> EvaluatorValueType {
        match self {
            Self::Owned(value) => value.value_type,
            Self::Mmap(value, _) => match value.value_type {
                ArchivedMmapEvaluatorValueType::Null => EvaluatorValueType::Null,
                ArchivedMmapEvaluatorValueType::Bool => EvaluatorValueType::Bool,
                ArchivedMmapEvaluatorValueType::Number => EvaluatorValueType::Number,
                ArchivedMmapEvaluatorValueType::String => EvaluatorValueType::String,
                ArchivedMmapEvaluatorValueType::Array => EvaluatorValueType::Array,
                ArchivedMmapEvaluatorValueType::Object => EvaluatorValueType::Object,
            },
        }
    }

    pub(crate) fn is_equal_to_user_value(self, other: UserValueRef<'_>) -> bool {
        match self.value_type() {
            EvaluatorValueType::Null => other.is_null(),
            EvaluatorValueType::Bool => self.bool_value() == other.bool_value(),
            EvaluatorValueType::Number => self.float_value() == other.float_value(),
            EvaluatorValueType::String => self.string_value() == other.string_value(),
            EvaluatorValueType::Array => {
                let Some(len) = self.array_len() else {
                    return other.array_len().is_none();
                };
                if other.array_len() != Some(len) {
                    return false;
                }
                self.all_array_entries(|_, index, expected| {
                    other.array_item(index).and_then(UserValueRef::string_value) == Some(expected)
                })
            }
            EvaluatorValueType::Object => {
                let Some(len) = self.object_len() else {
                    return other.object_len().is_none();
                };
                if other.object_len() != Some(len) {
                    return false;
                }
                self.all_object_entries(|key, expected| {
                    other.object_get(key).and_then(UserValueRef::string_value) == Some(expected)
                })
            }
        }
    }

    fn array_entry(self, lowercase: &str) -> Option<(usize, &'a str)> {
        match self {
            Self::Owned(value) => {
                value
                    .array_value
                    .as_ref()?
                    .iter()
                    .find_map(|(candidate, (index, original))| {
                        (candidate.as_str() == lowercase).then_some((*index, original.as_str()))
                    })
            }
            Self::Mmap(value, _) => {
                let hash = hashing::hash_one(lowercase.as_bytes());
                let entry = value
                    .array_value
                    .as_ref()?
                    .get(&rkyv::primitive::ArchivedU64::from_native(hash))?;
                Some((
                    entry.0.to_native() as usize,
                    InternedStore::get_mmap_string(entry.1.to_native())?,
                ))
            }
        }
    }

    fn object_entry(self, key: &str) -> Option<&'a str> {
        match self {
            Self::Owned(value) => {
                value
                    .object_value
                    .as_ref()?
                    .iter()
                    .find_map(|(candidate, value)| {
                        (candidate.as_str() == key).then_some(value.value.as_str())
                    })
            }
            Self::Mmap(value, _) => {
                let hash = hashing::hash_one(key.as_bytes());
                let value = value
                    .object_value
                    .as_ref()?
                    .get(&rkyv::primitive::ArchivedU64::from_native(hash))?;
                InternedStore::get_mmap_string(value.to_native())
            }
        }
    }

    fn is_equal_to_evaluator_value(self, other: EvaluatorValueRef<'_>) -> bool {
        if let (EvaluatorValueRef::Owned(left), EvaluatorValueRef::Owned(right)) = (self, other) {
            return left == right;
        }
        let iterate_other = matches!(
            (self, other),
            (EvaluatorValueRef::Mmap(_, _), EvaluatorValueRef::Owned(_))
        );

        if self.value_type() != other.value_type() {
            return false;
        }

        match self.value_type() {
            EvaluatorValueType::Null => true,
            EvaluatorValueType::Bool => self.bool_value() == other.bool_value(),
            EvaluatorValueType::Number => self.float_value() == other.float_value(),
            EvaluatorValueType::String => self.string_value() == other.string_value(),
            EvaluatorValueType::Array => match (self.array_len(), other.array_len()) {
                (None, None) => true,
                (Some(left), Some(right)) if left == right => {
                    if iterate_other {
                        other.all_array_entries(|lowercase, index, original| {
                            self.array_entry(lowercase) == Some((index, original))
                        })
                    } else {
                        self.all_array_entries(|lowercase, index, original| {
                            other.array_entry(lowercase) == Some((index, original))
                        })
                    }
                }
                _ => false,
            },
            EvaluatorValueType::Object => match (self.object_len(), other.object_len()) {
                (None, None) => true,
                (Some(left), Some(right)) if left == right => {
                    if iterate_other {
                        other.all_object_entries(|key, value| self.object_entry(key) == Some(value))
                    } else {
                        self.all_object_entries(|key, value| other.object_entry(key) == Some(value))
                    }
                }
                _ => false,
            },
        }
    }
}

struct SerializedDynamicString<'a>(&'a str);

impl Serialize for SerializedDynamicString<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self.0.parse::<bool>() {
            Ok(value) => serializer.serialize_bool(value),
            Err(_) => serializer.serialize_str(self.0),
        }
    }
}

impl Serialize for EvaluatorValueRef<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let value = match *self {
            Self::Owned(value) => return value.serialize(serializer),
            Self::Mmap(value, _) => value,
        };

        match value.value_type {
            ArchivedMmapEvaluatorValueType::Null => serializer.serialize_unit(),
            ArchivedMmapEvaluatorValueType::Bool => {
                value.bool_value.as_ref().copied().serialize(serializer)
            }
            ArchivedMmapEvaluatorValueType::Number => value
                .float_value
                .as_ref()
                .map(|value| value.to_native())
                .serialize(serializer),
            ArchivedMmapEvaluatorValueType::String => {
                let Some(hash) = value.string_value.as_ref() else {
                    return serializer.serialize_none();
                };
                let raw = mmap_string_for_serialization::<S>(hash.to_native())?;
                SerializedDynamicString(raw).serialize(serializer)
            }
            ArchivedMmapEvaluatorValueType::Array => {
                let Some(array) = value.array_value.as_ref() else {
                    return serializer.serialize_none();
                };
                let mut entries = Vec::with_capacity(array.len());
                for (_, entry) in array.iter() {
                    let raw = mmap_string_for_serialization::<S>(entry.1.to_native())?;
                    entries.push((entry.0.to_native(), raw));
                }
                entries.sort_unstable_by_key(|(index, _)| *index);

                let mut sequence = serializer.serialize_seq(Some(entries.len()))?;
                for (_, raw) in entries {
                    sequence.serialize_element(raw)?;
                }
                sequence.end()
            }
            ArchivedMmapEvaluatorValueType::Object => {
                let Some(object) = value.object_value.as_ref() else {
                    return serializer.serialize_none();
                };
                let mut map = serializer.serialize_map(Some(object.len()))?;
                for (key, value) in object.iter() {
                    let key = mmap_string_for_serialization::<S>(key.to_native())?;
                    let value = mmap_string_for_serialization::<S>(value.to_native())?;
                    map.serialize_entry(key, &SerializedDynamicString(value))?;
                }
                map.end()
            }
        }
    }
}

fn mmap_string_for_serialization<S: Serializer>(hash: u64) -> Result<&'static str, S::Error> {
    InternedStore::get_mmap_string(hash).ok_or_else(|| {
        serde::ser::Error::custom(format!(
            "Interned mmap evaluator value references missing string hash {hash}"
        ))
    })
}

impl<'de> Deserialize<'de> for EvaluatorValue {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let raw_value_ref: Box<RawValue> = Deserialize::deserialize(deserializer)?;
        Ok(InternedStore::get_or_intern_evaluator_value(Cow::Owned(
            raw_value_ref,
        )))
    }
}

impl Serialize for EvaluatorValue {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.as_value_ref().serialize(serializer)
    }
}

impl PartialEq for EvaluatorValue {
    fn eq(&self, other: &Self) -> bool {
        self.as_value_ref()
            .is_equal_to_evaluator_value(other.as_value_ref())
    }
}

// ------------------------------------------------------------------------------- [ MemoizedEvaluatorValue ]

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum EvaluatorValueType {
    Null,

    Bool,
    Number,
    String,
    Array,
    Object,
}

#[derive(Debug, Clone)]
pub struct MemoizedEvaluatorValue {
    pub value_type: EvaluatorValueType,
    pub bool_value: Option<bool>,
    pub float_value: Option<f64>,
    pub string_value: Option<DynamicString>,
    pub regex_value: Option<FancyRegex>,
    pub timestamp_value: Option<i64>,
    pub object_value: Option<AHashMap<InternedString, DynamicString>>,

    // - Note on Array Value ------------------------------------------------------------
    // - Keyed by lowercase string so we can lookup with O(1) during evaluation.
    // - Format is `{ lower_case_str: (index, str) }` i.e: ["Apple", "Banana"] becomes { "apple": (0, "Apple"), "banana": (1, "Banana") }
    // - The index is what position in the array it is, currently this is only used to serialzie back to the original JSON.
    // ----------------------------------------------------------------------------------
    pub array_value: Option<AHashMap<InternedString, (usize, InternedString)>>,
}

impl MemoizedEvaluatorValue {
    pub fn from_raw_value(raw_value: Cow<'_, RawValue>) -> Self {
        match serde_json::from_str(raw_value.get()) {
            Ok(value) => value,
            Err(e) => {
                log_e!(
                    TAG,
                    "Failed to convert raw value to MemoizedEvaluatorValue: {}",
                    e
                );
                Self::null()
            }
        }
    }
}

impl MemoizedEvaluatorValue {
    pub fn new(value_type: EvaluatorValueType) -> Self {
        Self {
            value_type,
            bool_value: None,
            float_value: None,
            string_value: None,
            regex_value: None,
            timestamp_value: None,
            array_value: None,
            object_value: None,
        }
    }

    pub fn null() -> Self {
        Self::new(EvaluatorValueType::Null)
    }

    pub fn compile_regex(&mut self) {
        let str_value = match &self.string_value {
            Some(dyn_str) => &dyn_str.value,
            None => return,
        };

        if let Ok(regex) = FancyRegex::new(str_value) {
            self.regex_value = Some(regex);
        }
    }

    pub fn is_equal_to_user_value(&self, other: UserValueRef<'_>) -> bool {
        EvaluatorValueRef::from(self).is_equal_to_user_value(other)
    }

    pub fn is_equal_to_dynamic_value(&self, other: &DynamicValue) -> bool {
        self.is_equal_to_user_value(UserValueRef::Dynamic(other))
    }
}

// Used during evaluation:
// - ua_parser
impl From<String> for MemoizedEvaluatorValue {
    fn from(value: String) -> Self {
        let int_value = value.parse::<i64>().ok();
        MemoizedEvaluatorValue {
            timestamp_value: try_parse_timestamp(&value, int_value),
            float_value: value.parse::<f64>().ok(),
            string_value: Some(DynamicString::from(value)),
            ..MemoizedEvaluatorValue::new(EvaluatorValueType::String)
        }
    }
}

// Used during Deserialization
impl From<JsonValue> for MemoizedEvaluatorValue {
    fn from(value: JsonValue) -> Self {
        match value {
            JsonValue::Null => MemoizedEvaluatorValue::new(EvaluatorValueType::Null),

            JsonValue::Bool(b) => MemoizedEvaluatorValue {
                bool_value: Some(b),
                ..MemoizedEvaluatorValue::new(EvaluatorValueType::Bool)
            },

            JsonValue::Number(n) => MemoizedEvaluatorValue {
                float_value: n.as_f64(),
                ..MemoizedEvaluatorValue::new(EvaluatorValueType::Number)
            },

            JsonValue::String(s) => MemoizedEvaluatorValue::from(s),

            JsonValue::Array(arr) => {
                let keyed_array: AHashMap<InternedString, (usize, InternedString)> = arr
                    .into_iter()
                    .enumerate()
                    .map(|(idx, val)| {
                        let str_value = match val.as_str() {
                            Some(s) => s.to_string(), // Value is a String
                            None => val.to_string(),  // Value was not a String, but can be made one
                        };

                        let interned_lowercased_str =
                            InternedString::from_string(str_value.to_lowercase());
                        let interned_str = InternedString::from_string(str_value);

                        (interned_lowercased_str, (idx, interned_str))
                    })
                    .collect();

                MemoizedEvaluatorValue {
                    array_value: Some(keyed_array),
                    ..MemoizedEvaluatorValue::new(EvaluatorValueType::Array)
                }
            }

            JsonValue::Object(obj) => MemoizedEvaluatorValue {
                object_value: Some(
                    obj.into_iter()
                        .map(|(k, v)| (InternedString::from_string(k), DynamicString::from(v)))
                        .collect(),
                ),
                ..MemoizedEvaluatorValue::new(EvaluatorValueType::Object)
            },
        }
    }
}

impl Serialize for MemoizedEvaluatorValue {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match &self.value_type {
            EvaluatorValueType::Null => JsonValue::Null.serialize(serializer),
            EvaluatorValueType::Bool => self.bool_value.serialize(serializer),
            EvaluatorValueType::Number => self.float_value.serialize(serializer),
            EvaluatorValueType::String => self.string_value.serialize(serializer),
            EvaluatorValueType::Array => {
                let array_map = match &self.array_value {
                    Some(a) => a,
                    None => return JsonValue::Null.serialize(serializer),
                };

                let mut entries: Vec<(usize, String)> = array_map
                    .values()
                    .map(|(idx, val)| (*idx, val.unperformant_to_string()))
                    .collect();
                entries.sort_by_key(|(idx, _)| *idx);
                let result: Vec<String> = entries.into_iter().map(|(_, val)| val).collect();

                result.serialize(serializer)
            }
            EvaluatorValueType::Object => self.object_value.serialize(serializer),
        }
    }
}

impl<'de> Deserialize<'de> for MemoizedEvaluatorValue {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let json_value = JsonValue::deserialize(deserializer)?;
        Ok(MemoizedEvaluatorValue::from(json_value))
    }
}

impl PartialEq for MemoizedEvaluatorValue {
    fn eq(&self, other: &Self) -> bool {
        self.value_type == other.value_type
            && self.bool_value == other.bool_value
            && self.float_value == other.float_value
            && self.string_value == other.string_value
            && self.array_value == other.array_value
            && self.object_value == other.object_value
    }
}

#[macro_export]
macro_rules! test_only_make_eval_value {
    ($x:expr) => {
        $crate::evaluation::evaluator_value::MemoizedEvaluatorValue::from(serde_json::json!($x))
    };
}

#[cfg(test)]
mod tests {
    use super::MemoizedEvaluatorValue;
    use serde_json::json;

    #[test]
    fn serialize_array_with_case_collision_is_safe() {
        let value = MemoizedEvaluatorValue::from(json!(["A", "a"]));
        let serialized = serde_json::to_value(&value).expect("serialize MemoizedEvaluatorValue");
        assert_eq!(serialized, json!(["a"]));
    }
}
