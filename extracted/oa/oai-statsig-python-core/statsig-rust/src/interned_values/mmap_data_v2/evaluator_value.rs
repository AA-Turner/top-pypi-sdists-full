use std::collections::HashMap;

use ahash::AHashSet;
use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};

use crate::{
    evaluation::evaluator_value::{EvaluatorValueType, MemoizedEvaluatorValue},
    StatsigErr,
};

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) struct MmapEvaluatorValue {
    pub(crate) value_type: MmapEvaluatorValueType,
    pub(crate) bool_value: Option<bool>,
    pub(crate) float_value: Option<f64>,
    pub(crate) string_value: Option<u64>,
    pub(crate) regex_value: Option<u64>,
    pub(crate) timestamp_value: Option<i64>,
    pub(crate) object_value: Option<HashMap<u64, u64>>,
    pub(crate) array_value: Option<HashMap<u64, (u32, u64)>>,
}

impl MmapEvaluatorValue {
    pub(crate) fn from_owned(value: &MemoizedEvaluatorValue) -> Result<Self, StatsigErr> {
        let array_value = value
            .array_value
            .as_ref()
            .map(|array| {
                array
                    .iter()
                    .map(|(lowercase, (index, original))| {
                        let index = u32::try_from(*index).map_err(|_| {
                            StatsigErr::SerializationError(
                                "Evaluator array index exceeds mmap format limit".to_string(),
                            )
                        })?;
                        Ok((lowercase.hash, (index, original.hash)))
                    })
                    .collect::<Result<HashMap<_, _>, StatsigErr>>()
            })
            .transpose()?;

        Ok(Self {
            value_type: value.value_type.into(),
            bool_value: value.bool_value,
            float_value: value.float_value,
            string_value: value.string_value.as_ref().map(|value| value.value.hash),
            regex_value: value
                .regex_value
                .as_ref()
                .and_then(|_| value.string_value.as_ref().map(|value| value.value.hash)),
            timestamp_value: value.timestamp_value,
            object_value: value.object_value.as_ref().map(|object| {
                object
                    .iter()
                    .map(|(key, value)| (key.hash, value.value.hash))
                    .collect()
            }),
            array_value,
        })
    }

    pub(crate) fn collect_string_hashes(&self, hashes: &mut AHashSet<u64>) {
        hashes.extend(self.string_value);
        hashes.extend(self.regex_value);
        if let Some(object) = &self.object_value {
            for (key, value) in object {
                hashes.insert(*key);
                hashes.insert(*value);
            }
        }
        if let Some(array) = &self.array_value {
            for (key, (_, value)) in array {
                hashes.insert(*key);
                hashes.insert(*value);
            }
        }
    }
}

#[derive(Archive, RkyvDeserialize, RkyvSerialize, Clone, Copy)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) enum MmapEvaluatorValueType {
    Null,
    Bool,
    Number,
    String,
    Array,
    Object,
}

impl From<EvaluatorValueType> for MmapEvaluatorValueType {
    fn from(value: EvaluatorValueType) -> Self {
        match value {
            EvaluatorValueType::Null => Self::Null,
            EvaluatorValueType::Bool => Self::Bool,
            EvaluatorValueType::Number => Self::Number,
            EvaluatorValueType::String => Self::String,
            EvaluatorValueType::Array => Self::Array,
            EvaluatorValueType::Object => Self::Object,
        }
    }
}
