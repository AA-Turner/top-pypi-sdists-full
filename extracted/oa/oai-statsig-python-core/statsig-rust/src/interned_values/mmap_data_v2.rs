mod evaluator_value;
mod spec;
mod spec_content_hash;

use std::{collections::HashMap, sync::Arc};

use rkyv::{
    Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize,
    with::{Identity, Unshare},
};

use crate::evaluation::rkyv_value::RkyvValue;

use super::interned_store::MapKVVec;

#[cfg(test)]
pub(crate) use evaluator_value::MmapEvaluatorValueType;
pub(crate) use evaluator_value::{
    ArchivedMmapEvaluatorValue, ArchivedMmapEvaluatorValueType, MmapEvaluatorValue,
};
#[cfg(test)]
pub(crate) use spec::MmapReturnable;
pub(crate) use spec::{
    ArchivedMmapDynamicString, ArchivedMmapReturnable, ArchivedMmapRule, ArchivedMmapSpec, MmapSpec,
};
pub(crate) use spec_content_hash::spec_content_hash;

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) struct MmapDataV2 {
    pub(crate) format_version: u32,
    #[rkyv(with = MapKVVec<Identity, Unshare>)]
    pub(crate) strings: Vec<(u64, Arc<String>)>,
    #[rkyv(with = MapKVVec<Identity, Unshare>)]
    pub(crate) returnables: Vec<(u64, Arc<HashMap<String, RkyvValue>>)>,
    pub(crate) evaluator_values: HashMap<u64, MmapEvaluatorValue>,
    pub(crate) feature_gates: HashMap<u64, MmapSpec>,
    pub(crate) dynamic_configs: HashMap<u64, MmapSpec>,
    pub(crate) layer_configs: HashMap<u64, MmapSpec>,
}

impl MmapDataV2 {
    pub(crate) const FORMAT_VERSION: u32 = 2;
}

#[cfg(test)]
impl ArchivedMmapDataV2 {
    pub(crate) fn find_returnable_value_for_test(
        &self,
        key: &str,
    ) -> Option<&crate::evaluation::rkyv_value::ArchivedRkyvValue> {
        self.returnables
            .iter()
            .find_map(|(_, returnable)| returnable.get(key))
    }
}

impl Default for MmapDataV2 {
    fn default() -> Self {
        Self {
            format_version: Self::FORMAT_VERSION,
            strings: Vec::new(),
            returnables: Vec::new(),
            evaluator_values: HashMap::new(),
            feature_gates: HashMap::new(),
            dynamic_configs: HashMap::new(),
            layer_configs: HashMap::new(),
        }
    }
}
