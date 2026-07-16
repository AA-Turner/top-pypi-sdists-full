use ahash::AHashSet;
use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};

use crate::{
    evaluation::{
        dynamic_returnable::{DynamicReturnable, DynamicReturnableValue},
        dynamic_string::DynamicString,
    },
    specs_response::spec_types::{Rule, Spec},
};

use super::spec_content_hash::spec_content_hash;

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) struct MmapSpec {
    pub(crate) content_hash: u64,
    pub(crate) checksum: Option<u64>,
    pub(crate) spec_type: u64,
    pub(crate) salt: u64,
    pub(crate) default_value: MmapReturnable,
    pub(crate) enabled: bool,
    pub(crate) rules: Vec<MmapRule>,
    pub(crate) id_type: u64,
    pub(crate) explicit_parameters: Option<Vec<u64>>,
    pub(crate) entity: u64,
    pub(crate) has_shared_params: Option<bool>,
    pub(crate) is_active: Option<bool>,
    pub(crate) version: Option<u32>,
    pub(crate) target_app_ids: Option<Vec<u64>>,
    pub(crate) forward_all_exposures: Option<bool>,
    pub(crate) fields_used: Option<Vec<u64>>,
    pub(crate) use_new_layer_eval: Option<bool>,
}

impl MmapSpec {
    pub(crate) fn from_owned(spec: &Spec) -> Self {
        Self {
            content_hash: spec_content_hash(spec),
            checksum: spec.checksum.as_ref().map(|value| value.hash),
            spec_type: spec._type.hash,
            salt: spec.salt.hash,
            default_value: MmapReturnable::from_owned(&spec.default_value),
            enabled: spec.enabled,
            rules: spec.rules.iter().map(MmapRule::from_owned).collect(),
            id_type: spec.id_type.hash,
            explicit_parameters: spec.explicit_parameters.as_ref().map(|parameters| {
                parameters
                    .as_slice()
                    .iter()
                    .map(|value| value.hash)
                    .collect()
            }),
            entity: spec.entity.hash,
            has_shared_params: spec.has_shared_params,
            is_active: spec.is_active,
            version: spec.version,
            target_app_ids: spec
                .target_app_ids
                .as_ref()
                .map(|values| values.iter().map(|value| value.hash).collect()),
            forward_all_exposures: spec.forward_all_exposures,
            fields_used: spec
                .fields_used
                .as_ref()
                .map(|values| values.iter().map(|value| value.hash).collect()),
            use_new_layer_eval: spec.use_new_layer_eval,
        }
    }

    pub(crate) fn collect_references(
        &self,
        string_hashes: &mut AHashSet<u64>,
        returnable_hashes: &mut AHashSet<u64>,
    ) {
        string_hashes.extend(self.checksum);
        string_hashes.insert(self.spec_type);
        string_hashes.insert(self.salt);
        self.default_value.collect_hash(returnable_hashes);
        string_hashes.insert(self.id_type);
        if let Some(values) = &self.explicit_parameters {
            string_hashes.extend(values);
        }
        string_hashes.insert(self.entity);
        if let Some(values) = &self.target_app_ids {
            string_hashes.extend(values);
        }
        if let Some(values) = &self.fields_used {
            string_hashes.extend(values);
        }

        for rule in &self.rules {
            string_hashes.insert(rule.name);
            rule.return_value.collect_hash(returnable_hashes);
            string_hashes.insert(rule.id);
            string_hashes.extend(rule.salt);
            string_hashes.extend(&rule.conditions);
            string_hashes.insert(rule.id_type.value);
            string_hashes.insert(rule.id_type.lowercased_value);
            string_hashes.extend(rule.group_name);
            string_hashes.extend(rule.config_delegate);
        }
    }
}

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) struct MmapRule {
    pub(crate) name: u64,
    pub(crate) pass_percentage: f64,
    pub(crate) return_value: MmapReturnable,
    pub(crate) id: u64,
    pub(crate) salt: Option<u64>,
    pub(crate) conditions: Vec<u64>,
    pub(crate) id_type: MmapDynamicString,
    pub(crate) group_name: Option<u64>,
    pub(crate) config_delegate: Option<u64>,
    pub(crate) is_experiment_group: Option<bool>,
    pub(crate) sampling_rate: Option<u64>,
}

impl MmapRule {
    fn from_owned(rule: &Rule) -> Self {
        Self {
            name: rule.name.hash,
            pass_percentage: rule.pass_percentage,
            return_value: MmapReturnable::from_owned(&rule.return_value),
            id: rule.id.hash,
            salt: rule.salt.as_ref().map(|value| value.hash),
            conditions: rule.conditions.iter().map(|value| value.hash).collect(),
            id_type: MmapDynamicString::from_owned(&rule.id_type),
            group_name: rule.group_name.as_ref().map(|value| value.hash),
            config_delegate: rule.config_delegate.as_ref().map(|value| value.hash),
            is_experiment_group: rule.is_experiment_group,
            sampling_rate: rule.sampling_rate,
        }
    }
}

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) struct MmapDynamicString {
    pub(crate) value: u64,
    pub(crate) lowercased_value: u64,
}

impl MmapDynamicString {
    fn from_owned(value: &DynamicString) -> Self {
        Self {
            value: value.value.hash,
            lowercased_value: value.lowercased_value.hash,
        }
    }
}

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub(crate) enum MmapReturnable {
    Null,
    Bool(bool),
    Json(u64),
}

impl MmapReturnable {
    fn from_owned(value: &DynamicReturnable) -> Self {
        match &value.value {
            DynamicReturnableValue::Null => Self::Null,
            DynamicReturnableValue::Bool(value) => Self::Bool(*value),
            DynamicReturnableValue::JsonPointer(_)
            | DynamicReturnableValue::JsonStatic(_)
            | DynamicReturnableValue::JsonArchived(_) => Self::Json(value.hash),
        }
    }

    fn collect_hash(&self, hashes: &mut AHashSet<u64>) {
        if let Self::Json(hash) = self {
            hashes.insert(*hash);
        }
    }
}
