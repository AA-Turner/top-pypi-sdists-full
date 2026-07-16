use std::{borrow::Cow, sync::Arc};

use ahash::{HashMap, HashMapExt};
use rkyv::{primitive::ArchivedU64, vec::ArchivedVec};
use serde::{
    ser::{SerializeSeq, SerializeStruct},
    Deserialize, Deserializer, Serialize, Serializer,
};
use serde_json::value::RawValue;

use crate::{
    evaluation::evaluation_data::SpecView,
    interned_string::InternedString,
    interned_values::{
        mmap_data_v2::{
            ArchivedMmapDynamicString, ArchivedMmapReturnable, ArchivedMmapRule, ArchivedMmapSpec,
        },
        InternedStore,
    },
    log_e,
    specs_response::spec_types::Spec,
};

const TAG: &str = "SpecsHashMap";

#[derive(PartialEq, Debug, Default)] /* DO_NOT_CLONE */
pub struct SpecsHashMap(pub HashMap<InternedString, SpecPointer>);

impl<'de> Deserialize<'de> for SpecsHashMap {
    fn deserialize<D>(_deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let raw_values: HashMap<InternedString, Box<RawValue>> =
            Deserialize::deserialize(_deserializer)?;

        let mut result = HashMap::with_capacity(raw_values.len());
        for (key, raw_value) in raw_values.into_iter() {
            let json_string = raw_value.get();

            let mut preloaded = None;
            if InternedStore::has_preloaded_mmap_v2() {
                if let Ok(identity) = serde_json::from_str::<SpecIdentity<'_>>(json_string) {
                    preloaded =
                        InternedStore::try_get_preloaded_spec(&key, identity.entity.as_ref());
                    if let Some(spec) = &preloaded {
                        let existing_checksum = spec.view().checksum().map(|value| value.as_str());
                        match (identity.checksum.as_deref(), existing_checksum) {
                            (Some(checksum), Some(existing)) if existing == checksum => {
                                result.insert(key, preloaded.expect("preloaded spec must exist"));
                                continue;
                            }
                            (None, None) => {}
                            _ => preloaded = None,
                        }
                    }
                }
            }

            let spec: Spec = match serde_json::from_str(json_string) {
                Ok(spec) => spec,
                Err(e) => {
                    log_e!(TAG, "Failed to deserialize spec: {}", e);
                    continue;
                }
            };

            if preloaded
                .as_ref()
                .is_some_and(|preloaded| preloaded.matches_owned_spec(&spec))
            {
                result.insert(key, preloaded.take().expect("preloaded spec must exist"));
            } else {
                result.insert(key, SpecPointer::Pointer(Arc::new(spec)));
            }
        }

        Ok(SpecsHashMap(result))
    }
}

#[derive(Deserialize)]
struct SpecIdentity<'a> {
    #[serde(borrow)]
    checksum: Option<Cow<'a, str>>,
    #[serde(borrow)]
    entity: Cow<'a, str>,
}

impl Serialize for SpecsHashMap {
    fn serialize<S>(&self, _serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.0.serialize(_serializer)
    }
}

/// Feel free to add more HashMap pass-through methods here as needed.
impl SpecsHashMap {
    pub fn get(&self, key: &InternedString) -> Option<&SpecPointer> {
        self.0.get(key)
    }

    pub fn keys(&self) -> impl Iterator<Item = &InternedString> {
        self.0.keys()
    }

    pub fn iter(&self) -> impl Iterator<Item = (&InternedString, &SpecPointer)> {
        self.0.iter()
    }

    pub fn insert(&mut self, key: InternedString, value: SpecPointer) {
        self.0.insert(key, value);
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn clear(&mut self) {
        self.0.clear();
    }

    pub fn remove(&mut self, key: &InternedString) -> Option<SpecPointer> {
        self.0.remove(key)
    }
}

#[derive(Clone, Copy)]
struct MmapSpecHandle {
    spec: &'static ArchivedMmapSpec,
}

impl MmapSpecHandle {
    pub(crate) fn new(spec: &'static ArchivedMmapSpec) -> Self {
        Self { spec }
    }

    pub(crate) fn archived(self) -> &'static ArchivedMmapSpec {
        self.spec
    }
}

#[derive(Clone /* Clone Ok because Arc or process-lifetime mmap */)]
pub struct SpecPointer {
    inner: SpecPointerInner,
}

#[derive(Clone)]
enum SpecPointerInner {
    Pointer(Arc<Spec>),
    Static(&'static Spec),
    Mmap(MmapSpecHandle),
}

impl SpecPointer {
    #[allow(non_snake_case)]
    pub fn Pointer(spec: Arc<Spec>) -> Self {
        Self {
            inner: SpecPointerInner::Pointer(spec),
        }
    }

    #[allow(non_snake_case)]
    pub fn Static(spec: &'static Spec) -> Self {
        Self {
            inner: SpecPointerInner::Static(spec),
        }
    }

    pub fn as_spec_ref(&self) -> &Spec {
        match &self.inner {
            SpecPointerInner::Pointer(spec) => spec,
            SpecPointerInner::Static(spec) => spec,
            SpecPointerInner::Mmap(handle) => {
                InternedStore::materialize_mmap_spec(handle.archived())
            }
        }
    }

    pub(crate) fn view(&self) -> SpecView<'_> {
        match &self.inner {
            SpecPointerInner::Pointer(spec) => SpecView::Owned(spec),
            SpecPointerInner::Static(spec) => SpecView::Owned(spec),
            SpecPointerInner::Mmap(handle) => SpecView::Archived(handle.archived()),
        }
    }

    pub(crate) fn from_mmap(spec: &'static ArchivedMmapSpec) -> Self {
        Self {
            inner: SpecPointerInner::Mmap(MmapSpecHandle::new(spec)),
        }
    }

    pub(crate) fn matches_owned_spec(&self, spec: &Spec) -> bool {
        match &self.inner {
            SpecPointerInner::Mmap(handle) => {
                handle.archived().content_hash.to_native()
                    == crate::interned_values::mmap_data_v2::spec_content_hash(spec)
            }
            SpecPointerInner::Pointer(existing) => existing.as_ref() == spec,
            SpecPointerInner::Static(existing) => *existing == spec,
        }
    }

    pub(crate) fn into_pointer(self) -> Option<Arc<Spec>> {
        match self.inner {
            SpecPointerInner::Pointer(spec) => Some(spec),
            SpecPointerInner::Static(_) | SpecPointerInner::Mmap(_) => None,
        }
    }

    #[cfg(test)]
    pub(crate) fn is_mmap(&self) -> bool {
        matches!(self.inner, SpecPointerInner::Mmap(_))
    }
}

impl Serialize for SpecPointer {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match &self.inner {
            SpecPointerInner::Pointer(spec) => spec.serialize(serializer),
            SpecPointerInner::Static(spec) => spec.serialize(serializer),
            SpecPointerInner::Mmap(handle) => handle.serialize(serializer),
        }
    }
}

impl Serialize for MmapSpecHandle {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let spec = self.spec;
        let field_count = 7
            + usize::from(spec.checksum.is_some())
            + usize::from(spec.explicit_parameters.is_some())
            + usize::from(spec.has_shared_params.is_some())
            + usize::from(spec.is_active.is_some())
            + usize::from(spec.version.is_some())
            + usize::from(spec.target_app_ids.is_some())
            + usize::from(spec.forward_all_exposures.is_some())
            + usize::from(spec.fields_used.is_some())
            + usize::from(spec.use_new_layer_eval.is_some());
        let mut state = serializer.serialize_struct("Spec", field_count)?;
        if let Some(checksum) = spec.checksum.as_ref() {
            state.serialize_field("checksum", &MmapString(checksum))?;
        }
        state.serialize_field("type", &MmapString(&spec.spec_type))?;
        state.serialize_field("salt", &MmapString(&spec.salt))?;
        state.serialize_field("defaultValue", &MmapReturnable(&spec.default_value))?;
        state.serialize_field("enabled", &spec.enabled)?;
        state.serialize_field("rules", &MmapRules(&spec.rules))?;
        state.serialize_field("idType", &MmapString(&spec.id_type))?;
        if let Some(parameters) = spec.explicit_parameters.as_ref() {
            state.serialize_field("explicitParameters", &MmapStrings(parameters))?;
        }
        state.serialize_field("entity", &MmapString(&spec.entity))?;
        if let Some(value) = spec.has_shared_params.as_ref() {
            state.serialize_field("hasSharedParams", value)?;
        }
        if let Some(value) = spec.is_active.as_ref() {
            state.serialize_field("isActive", value)?;
        }
        if let Some(value) = spec.version.as_ref() {
            state.serialize_field("version", &value.to_native())?;
        }
        if let Some(values) = spec.target_app_ids.as_ref() {
            state.serialize_field("targetAppIDs", &MmapStrings(values))?;
        }
        if let Some(value) = spec.forward_all_exposures.as_ref() {
            state.serialize_field("forwardAllExposures", value)?;
        }
        if let Some(values) = spec.fields_used.as_ref() {
            state.serialize_field("fieldsUsed", &MmapStrings(values))?;
        }
        if let Some(value) = spec.use_new_layer_eval.as_ref() {
            state.serialize_field("useNewLayerEval", value)?;
        }
        state.end()
    }
}

struct MmapString<'a>(&'a ArchivedU64);

impl Serialize for MmapString<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(mmap_string(self.0))
    }
}

struct MmapStrings<'a>(&'a ArchivedVec<ArchivedU64>);

impl Serialize for MmapStrings<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut sequence = serializer.serialize_seq(Some(self.0.len()))?;
        for value in self.0.iter() {
            sequence.serialize_element(&MmapString(value))?;
        }
        sequence.end()
    }
}

struct MmapRules<'a>(&'a ArchivedVec<ArchivedMmapRule>);

impl Serialize for MmapRules<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut sequence = serializer.serialize_seq(Some(self.0.len()))?;
        for rule in self.0.iter() {
            sequence.serialize_element(&MmapRule(rule))?;
        }
        sequence.end()
    }
}

struct MmapRule<'a>(&'a ArchivedMmapRule);

impl Serialize for MmapRule<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let rule = self.0;
        let field_count = 6
            + usize::from(rule.salt.is_some())
            + usize::from(rule.group_name.is_some())
            + usize::from(rule.config_delegate.is_some())
            + usize::from(rule.is_experiment_group.is_some())
            + usize::from(rule.sampling_rate.is_some());
        let mut state = serializer.serialize_struct("Rule", field_count)?;
        state.serialize_field("name", &MmapString(&rule.name))?;
        state.serialize_field("passPercentage", &rule.pass_percentage.to_native())?;
        state.serialize_field("returnValue", &MmapReturnable(&rule.return_value))?;
        state.serialize_field("id", &MmapString(&rule.id))?;
        if let Some(value) = rule.salt.as_ref() {
            state.serialize_field("salt", &MmapString(value))?;
        }
        state.serialize_field("conditions", &MmapStrings(&rule.conditions))?;
        state.serialize_field("idType", &MmapDynamicString(&rule.id_type))?;
        if let Some(value) = rule.group_name.as_ref() {
            state.serialize_field("groupName", &MmapString(value))?;
        }
        if let Some(value) = rule.config_delegate.as_ref() {
            state.serialize_field("configDelegate", &MmapString(value))?;
        }
        if let Some(value) = rule.is_experiment_group.as_ref() {
            state.serialize_field("isExperimentGroup", value)?;
        }
        if let Some(value) = rule.sampling_rate.as_ref() {
            state.serialize_field("samplingRate", &value.to_native())?;
        }
        state.end()
    }
}

struct MmapDynamicString<'a>(&'a ArchivedMmapDynamicString);

impl Serialize for MmapDynamicString<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let value = mmap_string(&self.0.value);
        match value.parse::<bool>() {
            Ok(value) => serializer.serialize_bool(value),
            Err(_) => serializer.serialize_str(value),
        }
    }
}

struct MmapReturnable<'a>(&'a ArchivedMmapReturnable);

impl Serialize for MmapReturnable<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        InternedStore::get_mmap_returnable(self.0).serialize(serializer)
    }
}

fn mmap_string(hash: &ArchivedU64) -> &'static str {
    InternedStore::get_mmap_string(hash.to_native())
        .expect("validated mmap string reference must exist")
}

impl SpecPointer {
    pub fn from_spec(spec: Spec) -> Self {
        Self::Pointer(Arc::new(spec))
    }
}

impl PartialEq for SpecPointer {
    fn eq(&self, other: &Self) -> bool {
        match (&self.inner, &other.inner) {
            (SpecPointerInner::Mmap(left), SpecPointerInner::Mmap(right))
                if std::ptr::eq(left.archived(), right.archived()) =>
            {
                true
            }
            _ => self.as_spec_ref() == other.as_spec_ref(),
        }
    }
}

impl std::fmt::Debug for SpecPointer {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match &self.inner {
            SpecPointerInner::Pointer(spec) => {
                formatter.debug_tuple("Pointer").field(spec).finish()
            }
            SpecPointerInner::Static(spec) => formatter.debug_tuple("Static").field(spec).finish(),
            SpecPointerInner::Mmap(_) => formatter.write_str("Mmap"),
        }
    }
}
