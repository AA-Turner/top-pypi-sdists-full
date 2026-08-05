use std::{borrow::Cow, cell::Cell, sync::Arc};

use ahash::{HashMap, HashMapExt};
use rkyv::{primitive::ArchivedU64, vec::ArchivedVec};
use serde::{
    Deserialize, Deserializer, Serialize, Serializer,
    ser::{SerializeSeq, SerializeStruct},
};
use serde_json::value::RawValue;

use crate::{
    evaluation::evaluation_data::SpecView,
    interned_string::InternedString,
    interned_values::{
        InternedStore,
        mmap_data_v2::{
            ArchivedMmapDynamicString, ArchivedMmapReturnable, ArchivedMmapRule, ArchivedMmapSpec,
        },
    },
    log_e,
    specs_response::{parse_options::should_preserve_session_update_mode, spec_types::Spec},
};

const TAG: &str = "SpecsHashMap";

#[derive(PartialEq, Debug, Default)] /* DO_NOT_CLONE */
pub struct SpecsHashMap(pub HashMap<InternedString, SpecPointer>);

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub(crate) struct SpecDecodeStats {
    pub(crate) total: usize,
    pub(crate) mmap: usize,
}

thread_local! {
    // Count representation while maps are already being materialized so telemetry does not
    // require another O(n) walk over production-sized specs. Delta decoding seeds this count from
    // the previous snapshot before applying its changes.
    static ACTIVE_SPEC_DECODE_STATS: Cell<Option<SpecDecodeStats>> = const { Cell::new(None) };
}

struct SpecDecodeStatsGuard {
    previous: Option<SpecDecodeStats>,
}

impl Drop for SpecDecodeStatsGuard {
    fn drop(&mut self) {
        ACTIVE_SPEC_DECODE_STATS.with(|stats| stats.set(self.previous));
    }
}

pub(crate) fn track_spec_decodes<T>(callback: impl FnOnce() -> T) -> (T, SpecDecodeStats) {
    let previous =
        ACTIVE_SPEC_DECODE_STATS.with(|stats| stats.replace(Some(SpecDecodeStats::default())));
    let guard = SpecDecodeStatsGuard { previous };
    let result = callback();
    let stats = ACTIVE_SPEC_DECODE_STATS.with(Cell::get).unwrap_or_default();
    drop(guard);
    (result, stats)
}

pub(crate) fn seed_spec_decode_stats(stats: SpecDecodeStats) {
    ACTIVE_SPEC_DECODE_STATS.with(|active| {
        if active.get().is_some() {
            active.set(Some(stats));
        }
    });
}

fn record_specs_cleared(values: &HashMap<InternedString, SpecPointer>) {
    ACTIVE_SPEC_DECODE_STATS.with(|active| {
        let Some(mut stats) = active.get() else {
            return;
        };

        stats.total -= values.len();
        stats.mmap -= values.values().filter(|value| value.is_mmap()).count();
        active.set(Some(stats));
    });
}

fn record_spec_change(previous_is_mmap: Option<bool>, next_is_mmap: Option<bool>) {
    ACTIVE_SPEC_DECODE_STATS.with(|active| {
        let Some(mut stats) = active.get() else {
            return;
        };

        if let Some(previous_is_mmap) = previous_is_mmap {
            stats.total -= 1;
            stats.mmap -= usize::from(previous_is_mmap);
        }
        if let Some(next_is_mmap) = next_is_mmap {
            stats.total += 1;
            stats.mmap += usize::from(next_is_mmap);
        }
        active.set(Some(stats));
    });
}

#[cfg(test)]
mod decode_stats_tests {
    use super::{SpecDecodeStats, record_spec_change, seed_spec_decode_stats, track_spec_decodes};

    #[test]
    fn seeded_stats_track_replacements_and_deletions() {
        let (_, stats) = track_spec_decodes(|| {
            seed_spec_decode_stats(SpecDecodeStats { total: 3, mmap: 2 });
            record_spec_change(Some(true), Some(false));
            record_spec_change(Some(false), None);
        });

        assert_eq!(stats, SpecDecodeStats { total: 2, mmap: 1 });
    }
}

impl<'de> Deserialize<'de> for SpecsHashMap {
    fn deserialize<D>(_deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let raw_values: HashMap<InternedString, Box<RawValue>> =
            Deserialize::deserialize(_deserializer)?;

        let preserve_session_update_mode = should_preserve_session_update_mode();
        let mut result = SpecsHashMap(HashMap::with_capacity(raw_values.len()));
        for (key, raw_value) in raw_values.into_iter() {
            let json_string = raw_value.get();

            let mut preloaded = None;
            if InternedStore::has_preloaded_mmap_v2() {
                if preserve_session_update_mode {
                    if let Ok(identity) =
                        serde_json::from_str::<SpecIdentityWithSessionUpdateMode<'_>>(json_string)
                    {
                        preloaded =
                            InternedStore::try_get_preloaded_spec(&key, identity.entity.as_ref());
                        if let Some(spec) = &preloaded {
                            let existing_checksum =
                                spec.view().checksum().map(|value| value.as_str());
                            match (identity.checksum.as_deref(), existing_checksum) {
                                (Some(checksum), Some(existing)) if existing == checksum => {
                                    if let Some(spec) = spec.with_session_update_mode(
                                        identity.session_update_mode.as_deref(),
                                    ) {
                                        result.insert(key, spec);
                                        continue;
                                    }
                                }
                                (None, None) => {}
                                _ => preloaded = None,
                            }
                        }
                    }
                } else if let Ok(identity) = serde_json::from_str::<SpecIdentity<'_>>(json_string) {
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
                let preloaded = preloaded.take().expect("preloaded spec must exist");
                if !preserve_session_update_mode {
                    result.insert(key, preloaded);
                    continue;
                }

                if let Some(preloaded) =
                    preloaded.with_session_update_mode(spec.session_update_mode.as_deref())
                {
                    result.insert(key, preloaded);
                    continue;
                }
            }

            result.insert(key, SpecPointer::Pointer(Arc::new(spec)));
        }

        Ok(result)
    }
}

#[derive(Deserialize)]
struct SpecIdentity<'a> {
    #[serde(borrow)]
    checksum: Option<Cow<'a, str>>,
    #[serde(borrow)]
    entity: Cow<'a, str>,
}

#[derive(Deserialize)]
struct SpecIdentityWithSessionUpdateMode<'a> {
    #[serde(borrow)]
    checksum: Option<Cow<'a, str>>,
    #[serde(borrow)]
    entity: Cow<'a, str>,
    #[serde(rename = "sessionUpdateMode", borrow)]
    session_update_mode: Option<Cow<'a, str>>,
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
        let next_is_mmap = value.is_mmap();
        let previous = self.0.insert(key, value);
        record_spec_change(
            previous.as_ref().map(SpecPointer::is_mmap),
            Some(next_is_mmap),
        );
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn clear(&mut self) {
        record_specs_cleared(&self.0);
        self.0.clear();
    }

    pub fn remove(&mut self, key: &InternedString) -> Option<SpecPointer> {
        let previous = self.0.remove(key);
        record_spec_change(previous.as_ref().map(SpecPointer::is_mmap), None);
        previous
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
    MmapLive(MmapSpecHandle),
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
            SpecPointerInner::MmapLive(handle) => {
                InternedStore::materialize_mmap_live_spec(handle.archived())
            }
        }
    }

    /// Reads session update mode without materializing mmap-backed specs.
    pub fn session_update_mode(&self) -> Option<&str> {
        match &self.inner {
            SpecPointerInner::Pointer(spec) => spec.session_update_mode.as_deref(),
            SpecPointerInner::Static(spec) => spec.session_update_mode.as_deref(),
            SpecPointerInner::Mmap(_) => None,
            SpecPointerInner::MmapLive(_) => Some("live"),
        }
    }

    pub(crate) fn view(&self) -> SpecView<'_> {
        match &self.inner {
            SpecPointerInner::Pointer(spec) => SpecView::Owned(spec),
            SpecPointerInner::Static(spec) => SpecView::Owned(spec),
            SpecPointerInner::Mmap(handle) => SpecView::Archived(handle.archived()),
            SpecPointerInner::MmapLive(handle) => SpecView::Archived(handle.archived()),
        }
    }

    pub(crate) fn from_mmap(spec: &'static ArchivedMmapSpec) -> Self {
        Self {
            inner: SpecPointerInner::Mmap(MmapSpecHandle::new(spec)),
        }
    }

    pub(crate) fn with_session_update_mode(&self, mode: Option<&str>) -> Option<Self> {
        match (&self.inner, mode) {
            (SpecPointerInner::Mmap(handle) | SpecPointerInner::MmapLive(handle), None) => {
                Some(Self {
                    inner: SpecPointerInner::Mmap(*handle),
                })
            }
            (SpecPointerInner::Mmap(handle) | SpecPointerInner::MmapLive(handle), Some("live")) => {
                Some(Self {
                    inner: SpecPointerInner::MmapLive(*handle),
                })
            }
            (SpecPointerInner::Pointer(spec), mode)
                if spec.session_update_mode.as_deref() == mode =>
            {
                Some(Self::Pointer(Arc::clone(spec)))
            }
            (SpecPointerInner::Static(spec), mode)
                if spec.session_update_mode.as_deref() == mode =>
            {
                Some(Self::Static(spec))
            }
            _ => None,
        }
    }

    pub(crate) fn matches_owned_spec(&self, spec: &Spec) -> bool {
        match &self.inner {
            SpecPointerInner::Mmap(handle) => {
                handle.archived().content_hash.to_native()
                    == crate::interned_values::mmap_data_v2::spec_content_hash(spec)
            }
            SpecPointerInner::MmapLive(handle) => {
                spec.session_update_mode.as_deref() == Some("live")
                    && handle.archived().content_hash.to_native()
                        == crate::interned_values::mmap_data_v2::spec_content_hash(spec)
            }
            SpecPointerInner::Pointer(existing) => existing.as_ref() == spec,
            SpecPointerInner::Static(existing) => *existing == spec,
        }
    }

    pub(crate) fn into_pointer(self) -> Option<Arc<Spec>> {
        match self.inner {
            SpecPointerInner::Pointer(spec) => Some(spec),
            SpecPointerInner::Static(_)
            | SpecPointerInner::Mmap(_)
            | SpecPointerInner::MmapLive(_) => None,
        }
    }

    pub(crate) fn is_mmap(&self) -> bool {
        matches!(
            self.inner,
            SpecPointerInner::Mmap(_) | SpecPointerInner::MmapLive(_)
        )
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
            SpecPointerInner::MmapLive(handle) => {
                handle.serialize_with_session_update_mode(serializer, Some("live"))
            }
        }
    }
}

impl Serialize for MmapSpecHandle {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.serialize_with_session_update_mode(serializer, None)
    }
}

impl MmapSpecHandle {
    fn serialize_with_session_update_mode<S>(
        &self,
        serializer: S,
        session_update_mode: Option<&str>,
    ) -> Result<S::Ok, S::Error>
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
            + usize::from(spec.use_new_layer_eval.is_some())
            + usize::from(session_update_mode.is_some());
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
        if let Some(value) = session_update_mode {
            state.serialize_field("sessionUpdateMode", value)?;
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
            | (SpecPointerInner::MmapLive(left), SpecPointerInner::MmapLive(right))
                if std::ptr::eq(left.archived(), right.archived()) =>
            {
                true
            }
            (SpecPointerInner::Mmap(left), SpecPointerInner::MmapLive(right))
            | (SpecPointerInner::MmapLive(left), SpecPointerInner::Mmap(right))
                if std::ptr::eq(left.archived(), right.archived()) =>
            {
                false
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
            SpecPointerInner::MmapLive(_) => formatter.write_str("MmapLive"),
        }
    }
}
