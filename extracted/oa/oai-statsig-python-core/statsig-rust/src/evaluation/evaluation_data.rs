use crate::{
    evaluation::{dynamic_returnable::DynamicReturnable, dynamic_string::DynamicString},
    interned_string::InternedString,
    interned_values::mmap_data_v2::{
        ArchivedMmapDynamicString, ArchivedMmapReturnable, ArchivedMmapRule, ArchivedMmapSpec,
    },
    interned_values::InternedStore,
    specs_response::{
        explicit_params::ExplicitParameters,
        spec_types::{Rule, Spec},
    },
};
use serde_json::Value;
use std::{collections::HashMap, hash::BuildHasher};

#[derive(Clone, Copy)]
pub(crate) enum InternedStrRef<'a> {
    Owned(&'a InternedString),
    Mmap(u64),
}

impl<'a> InternedStrRef<'a> {
    pub(crate) fn as_str(self) -> &'a str {
        match self {
            Self::Owned(value) => value.as_str(),
            Self::Mmap(hash) => InternedStore::get_mmap_string(hash)
                .expect("validated mmap string reference must exist"),
        }
    }

    pub(crate) fn get_from<V, S>(self, values: &HashMap<InternedString, V, S>) -> Option<&V>
    where
        S: BuildHasher,
    {
        match self {
            Self::Owned(value) => values.get(value),
            Self::Mmap(hash) => values.get(&InternedString::from_static(
                hash,
                InternedStore::get_mmap_string(hash)?,
            )),
        }
    }

    pub(crate) fn to_interned(self) -> InternedString {
        match self {
            Self::Owned(value) => value.clone(),
            Self::Mmap(hash) => InternedString::from_static(
                hash,
                InternedStore::get_mmap_string(hash)
                    .expect("validated mmap string reference must exist"),
            ),
        }
    }

    pub(crate) fn from_mmap(hash: u64) -> Self {
        Self::Mmap(hash)
    }
}

impl<'a> From<&'a InternedString> for InternedStrRef<'a> {
    fn from(value: &'a InternedString) -> Self {
        Self::Owned(value)
    }
}

#[derive(Clone, Copy)]
pub(crate) struct DynamicStringRef<'a> {
    value: InternedStrRef<'a>,
    lowercased_value: InternedStrRef<'a>,
}

impl<'a> DynamicStringRef<'a> {
    pub(crate) fn value(self) -> &'a str {
        self.value.as_str()
    }

    pub(crate) fn lowercased_value(self) -> &'a str {
        self.lowercased_value.as_str()
    }

    pub(crate) fn from_mmap(value: &'a ArchivedMmapDynamicString) -> Self {
        Self {
            value: InternedStrRef::from_mmap(value.value.to_native()),
            lowercased_value: InternedStrRef::from_mmap(value.lowercased_value.to_native()),
        }
    }
}

impl<'a> From<&'a DynamicString> for DynamicStringRef<'a> {
    fn from(value: &'a DynamicString) -> Self {
        Self {
            value: (&value.value).into(),
            lowercased_value: (&value.lowercased_value).into(),
        }
    }
}

#[derive(Clone, Copy)]
pub(crate) enum ReturnableRef<'a> {
    Owned(&'a DynamicReturnable),
    Mmap(&'a ArchivedMmapReturnable),
}

impl ReturnableRef<'_> {
    pub(crate) fn bool_value(self) -> Option<bool> {
        match self {
            Self::Owned(value) => value.get_bool(),
            Self::Mmap(ArchivedMmapReturnable::Bool(value)) => Some(*value),
            Self::Mmap(_) => None,
        }
    }

    pub(crate) fn json_value(self) -> Option<HashMap<String, Value>> {
        match self {
            Self::Owned(value) => value.get_json(),
            Self::Mmap(value) => InternedStore::get_mmap_returnable(value).get_json(),
        }
    }

    pub(crate) fn to_owned(self) -> DynamicReturnable {
        match self {
            Self::Owned(value) => value.clone(),
            Self::Mmap(value) => InternedStore::get_mmap_returnable(value),
        }
    }
}

pub(crate) enum SpecAccess<'a> {
    Borrowed(&'a Spec),
    Materialized(&'static Spec),
}

impl SpecAccess<'_> {
    pub(crate) fn as_ref(&self) -> &Spec {
        match self {
            Self::Borrowed(spec) => spec,
            Self::Materialized(spec) => spec,
        }
    }
}

#[derive(Clone, Copy)]
pub(crate) enum SpecView<'a> {
    Owned(&'a Spec),
    Archived(&'a ArchivedMmapSpec),
}

impl<'a> SpecView<'a> {
    pub(crate) fn materialize(self) -> SpecAccess<'a> {
        match self {
            Self::Owned(spec) => SpecAccess::Borrowed(spec),
            Self::Archived(spec) => {
                SpecAccess::Materialized(InternedStore::materialize_mmap_spec(spec))
            }
        }
    }

    pub(crate) fn salt(self) -> InternedStrRef<'a> {
        match self {
            Self::Owned(spec) => (&spec.salt).into(),
            Self::Archived(spec) => InternedStrRef::from_mmap(spec.salt.to_native()),
        }
    }

    pub(crate) fn checksum(self) -> Option<InternedStrRef<'a>> {
        match self {
            Self::Owned(spec) => spec.checksum.as_ref().map(Into::into),
            Self::Archived(spec) => spec
                .checksum
                .as_ref()
                .map(|value| InternedStrRef::from_mmap(value.to_native())),
        }
    }

    pub(crate) fn entity(self) -> InternedStrRef<'a> {
        match self {
            Self::Owned(spec) => (&spec.entity).into(),
            Self::Archived(spec) => InternedStrRef::from_mmap(spec.entity.to_native()),
        }
    }

    pub(crate) fn fields_used(self) -> Vec<String> {
        match self {
            Self::Owned(spec) => spec
                .fields_used
                .as_ref()
                .map(|fields| {
                    fields
                        .iter()
                        .map(InternedString::unperformant_to_string)
                        .collect()
                })
                .unwrap_or_default(),
            Self::Archived(spec) => spec
                .fields_used
                .as_ref()
                .map(|fields| {
                    fields
                        .iter()
                        .map(|hash| {
                            InternedStrRef::from_mmap(hash.to_native())
                                .as_str()
                                .to_string()
                        })
                        .collect()
                })
                .unwrap_or_default(),
        }
    }

    pub(crate) fn target_app_ids_contains(self, app_id: &str) -> Option<bool> {
        match self {
            Self::Owned(spec) => spec
                .target_app_ids
                .as_ref()
                .map(|ids| ids.iter().any(|id| id == app_id)),
            Self::Archived(spec) => spec.target_app_ids.as_ref().map(|ids| {
                ids.iter()
                    .any(|hash| InternedStrRef::from_mmap(hash.to_native()).as_str() == app_id)
            }),
        }
    }

    pub(crate) fn target_app_ids(self) -> Option<Vec<InternedString>> {
        match self {
            Self::Owned(spec) => spec.target_app_ids.clone(),
            Self::Archived(spec) => spec.target_app_ids.as_ref().map(|ids| {
                ids.iter()
                    .map(|hash| InternedStrRef::from_mmap(hash.to_native()).to_interned())
                    .collect()
            }),
        }
    }

    pub(crate) fn default_value(self) -> ReturnableRef<'a> {
        match self {
            Self::Owned(spec) => ReturnableRef::Owned(&spec.default_value),
            Self::Archived(spec) => ReturnableRef::Mmap(&spec.default_value),
        }
    }

    pub(crate) fn enabled(self) -> bool {
        match self {
            Self::Owned(spec) => spec.enabled,
            Self::Archived(spec) => spec.enabled,
        }
    }

    pub(crate) fn rules_len(self) -> usize {
        match self {
            Self::Owned(spec) => spec.rules.len(),
            Self::Archived(spec) => spec.rules.len(),
        }
    }

    pub(crate) fn rule(self, index: usize) -> RuleRef<'a> {
        match self {
            Self::Owned(spec) => RuleRef::Owned(&spec.rules[index]),
            Self::Archived(spec) => RuleRef::Mmap(&spec.rules[index]),
        }
    }

    pub(crate) fn id_type(self) -> InternedStrRef<'a> {
        match self {
            Self::Owned(spec) => (&spec.id_type).into(),
            Self::Archived(spec) => InternedStrRef::from_mmap(spec.id_type.to_native()),
        }
    }

    pub(crate) fn explicit_parameters(self) -> Option<ExplicitParameters> {
        match self {
            Self::Owned(spec) => spec.explicit_parameters.clone(),
            Self::Archived(spec) => spec
                .explicit_parameters
                .as_ref()
                .map(InternedStore::get_mmap_explicit_parameters),
        }
    }

    pub(crate) fn has_shared_params(self) -> Option<bool> {
        match self {
            Self::Owned(spec) => spec.has_shared_params,
            Self::Archived(spec) => spec.has_shared_params.as_ref().copied(),
        }
    }

    pub(crate) fn is_active(self) -> Option<bool> {
        match self {
            Self::Owned(spec) => spec.is_active,
            Self::Archived(spec) => spec.is_active.as_ref().copied(),
        }
    }

    pub(crate) fn version(self) -> Option<u32> {
        match self {
            Self::Owned(spec) => spec.version,
            Self::Archived(spec) => spec.version.as_ref().map(|value| value.to_native()),
        }
    }

    pub(crate) fn forward_all_exposures(self) -> Option<bool> {
        match self {
            Self::Owned(spec) => spec.forward_all_exposures,
            Self::Archived(spec) => spec.forward_all_exposures.as_ref().copied(),
        }
    }

    pub(crate) fn uses_new_layer_eval(self) -> bool {
        match self {
            Self::Owned(spec) => spec.use_new_layer_eval == Some(true),
            Self::Archived(spec) => spec.use_new_layer_eval.as_ref() == Some(&true),
        }
    }
}

impl<'a> From<&'a Spec> for SpecView<'a> {
    fn from(value: &'a Spec) -> Self {
        Self::Owned(value)
    }
}

#[derive(Clone, Copy)]
pub(crate) enum RuleRef<'a> {
    Owned(&'a Rule),
    Mmap(&'a ArchivedMmapRule),
}

impl<'a> RuleRef<'a> {
    pub(crate) fn id(self) -> InternedStrRef<'a> {
        match self {
            Self::Owned(rule) => (&rule.id).into(),
            Self::Mmap(rule) => InternedStrRef::from_mmap(rule.id.to_native()),
        }
    }

    pub(crate) fn pass_percentage(self) -> f64 {
        match self {
            Self::Owned(rule) => rule.pass_percentage,
            Self::Mmap(rule) => rule.pass_percentage.to_native(),
        }
    }

    pub(crate) fn return_value(self) -> ReturnableRef<'a> {
        match self {
            Self::Owned(rule) => ReturnableRef::Owned(&rule.return_value),
            Self::Mmap(rule) => ReturnableRef::Mmap(&rule.return_value),
        }
    }

    pub(crate) fn salt(self) -> Option<InternedStrRef<'a>> {
        match self {
            Self::Owned(rule) => rule.salt.as_ref().map(Into::into),
            Self::Mmap(rule) => rule
                .salt
                .as_ref()
                .map(|value| InternedStrRef::from_mmap(value.to_native())),
        }
    }

    pub(crate) fn conditions_len(self) -> usize {
        match self {
            Self::Owned(rule) => rule.conditions.len(),
            Self::Mmap(rule) => rule.conditions.len(),
        }
    }

    pub(crate) fn condition_id(self, index: usize) -> InternedStrRef<'a> {
        match self {
            Self::Owned(rule) => (&rule.conditions[index]).into(),
            Self::Mmap(rule) => InternedStrRef::from_mmap(rule.conditions[index].to_native()),
        }
    }

    pub(crate) fn id_type(self) -> DynamicStringRef<'a> {
        match self {
            Self::Owned(rule) => (&rule.id_type).into(),
            Self::Mmap(rule) => DynamicStringRef::from_mmap(&rule.id_type),
        }
    }

    pub(crate) fn group_name(self) -> Option<InternedStrRef<'a>> {
        match self {
            Self::Owned(rule) => rule.group_name.as_ref().map(Into::into),
            Self::Mmap(rule) => rule
                .group_name
                .as_ref()
                .map(|value| InternedStrRef::from_mmap(value.to_native())),
        }
    }

    pub(crate) fn config_delegate(self) -> Option<InternedStrRef<'a>> {
        match self {
            Self::Owned(rule) => rule.config_delegate.as_ref().map(Into::into),
            Self::Mmap(rule) => rule
                .config_delegate
                .as_ref()
                .map(|value| InternedStrRef::from_mmap(value.to_native())),
        }
    }

    pub(crate) fn is_experiment_group(self) -> bool {
        match self {
            Self::Owned(rule) => rule.is_experiment_group.unwrap_or(false),
            Self::Mmap(rule) => rule.is_experiment_group.as_ref() == Some(&true),
        }
    }

    pub(crate) fn sampling_rate(self) -> Option<u64> {
        match self {
            Self::Owned(rule) => rule.sampling_rate,
            Self::Mmap(rule) => rule.sampling_rate.as_ref().map(|value| value.to_native()),
        }
    }
}

impl<'a> From<&'a Rule> for RuleRef<'a> {
    fn from(value: &'a Rule) -> Self {
        Self::Owned(value)
    }
}
