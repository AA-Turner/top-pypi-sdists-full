use std::collections::{HashMap, hash_map::Entry};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::Instant;

use serde::{
    Deserialize, Serialize,
    de::{MapAccess, Visitor, value::MapDeserializer},
    ser::SerializeMap,
};
use serde_json::value::{RawValue, to_raw_value};

use crate::interned_string::InternedString;
use crate::interned_values::{InternedStore, interned_store::MmapProjectId};
use crate::networking::ResponseData;
use crate::specs_adapter::SpecsSyncTrigger;
use crate::specs_response::parse_options::{SpecsResponseParseOptions, with_parse_options};
use crate::specs_response::proto_specs::VerifiedRemoteConfigValues;
use crate::specs_response::spec_types::{Spec, SpecsResponseFull, SpecsResponseNoUpdates};
use crate::specs_response::specs_hash_map::{
    SpecDecodeStats, SpecPointer, decode_raw_dynamic_configs, track_spec_decodes,
};
use crate::{StatsigErr, log_e};

use super::errors::{HydrationFailureReason, hydration_error};
use super::metadata::{
    RemoteConfigValueMetadata, RemoteConfigValueMetadataWire, RemoteValueReference,
    add_raw_value_reference, hydrated_value, validate_reference_limits,
};
use super::telemetry::{HydrationPhase, HydrationResult};
use super::verified_values::{VerifiedRemoteValue, VerifiedRemoteValues};
use super::{RemoteConfigValueHydrator, TAG};

pub(crate) struct HydratedJsonStoreUpdate {
    pub(crate) values: Box<SpecsResponseFull>,
    pub(crate) spec_decode_stats: SpecDecodeStats,
    pub(crate) verified_remote_values: VerifiedRemoteConfigValues,
}

pub(crate) struct JsonStoreHydrationContext<'a> {
    pub(crate) source_url: &'a str,
    pub(crate) sync_trigger: Option<SpecsSyncTrigger>,
    pub(crate) current_verified_values: &'a VerifiedRemoteConfigValues,
    pub(crate) mmap_project_id: MmapProjectId,
    pub(crate) preserve_session_update_mode: bool,
    pub(crate) capture_data_store_bytes: bool,
    pub(crate) response_has_updates: Option<&'a AtomicBool>,
}

struct JsonConfigEntry {
    name: String,
    raw_spec: Box<RawValue>,
    // Match the decoder's classification: malformed rule arrays alone are not remote.
    use_remote_decoder: bool,
}

struct JsonHydrationInput {
    payload: RawJsonObject,
    configs: Vec<JsonConfigEntry>,
    references: Vec<RemoteValueReference>,
    reference_count: usize,
    total_bytes: u64,
}

fn parse_json_hydration_input(
    data: &mut ResponseData,
    source_url: &str,
    hydration_result: &mut HydrationResult<'_>,
) -> Result<Option<JsonHydrationInput>, StatsigErr> {
    if !response_may_contain_remote_metadata(data)? {
        data.rewind()?;
        return Ok(None);
    }
    let Some(mut payload) = parse_raw_json_object_from_response(data)? else {
        data.rewind()?;
        return Ok(None);
    };
    hydration_result.set_response_type(false);
    // Validate reused references too, before selecting proofs or starting GETs.
    let (references, configs) =
        collect_json_references(&mut payload, source_url, hydration_result)?;
    if references.is_empty() {
        data.rewind()?;
        return Ok(None);
    }
    let (reference_count, total_bytes) = validate_reference_limits(&references)?;
    Ok(Some(JsonHydrationInput {
        payload,
        configs,
        references,
        reference_count,
        total_bytes,
    }))
}

pub(super) async fn hydrate_response_for_store(
    hydrator: &RemoteConfigValueHydrator,
    data: &mut ResponseData,
    context: JsonStoreHydrationContext<'_>,
    hydration_result: &mut HydrationResult<'_>,
) -> Result<Option<HydratedJsonStoreUpdate>, StatsigErr> {
    let started_at = Instant::now();
    let Some(input) = parse_json_hydration_input(data, context.source_url, hydration_result)?
    else {
        return Ok(None);
    };
    if let Some(response_has_updates) = context.response_has_updates {
        // Remote downloads can be cancelled; preserve classification of the original
        // bytes before awaiting them. Ordinary responses never need this fallback.
        let has_updates = data
            .deserialize_into::<SpecsResponseNoUpdates>()
            .map_or(true, |response| response.has_updates);
        let _ = data.rewind();
        response_has_updates.store(has_updates, Ordering::Relaxed);
    }
    let mut incoming_metadata: HashMap<_, _> = input
        .references
        .iter()
        .map(|reference| (reference.metadata.sha256.as_str(), &reference.metadata))
        .collect();
    // Deltas may leave different tuples for one SHA in different configs.
    // Select the first compatible proof before collapsing the per-config registry.
    // Writable JSON sidecars also need original number lexemes. Redownload
    // bodies containing numbers for those writes; read-only updates can reuse
    // every compatible parsed value without retaining original blob bytes.
    let mut verified_values = VerifiedRemoteValues::new();
    'configs: for values in context.current_verified_values.values() {
        for (sha, value) in values.iter() {
            let Some(metadata) = incoming_metadata.get(sha.as_str()) else {
                continue;
            };
            if !value.matches_metadata(metadata)
                || (context.capture_data_store_bytes && !value.can_reuse_json_sidecar())
            {
                continue;
            }
            incoming_metadata.remove(sha.as_str());
            verified_values.insert(sha.clone(), Arc::clone(value));
            if incoming_metadata.is_empty() {
                break 'configs;
            }
        }
    }
    drop(incoming_metadata);
    let missing_references: Vec<_> = input
        .references
        .iter()
        .filter(|reference| !verified_values.contains_key(reference.metadata.sha256.as_str()))
        .cloned()
        .collect();
    hydrator.log_phase_latency(started_at.elapsed(), HydrationPhase::JsonParse);
    // Charge only original bodies that will actually be downloaded. An update
    // composed entirely of verified values must not wait for download capacity.
    let _download_reservation = if missing_references.is_empty() {
        None
    } else {
        let missing_bytes = missing_references
            .iter()
            .map(|reference| reference.metadata.byte_length)
            .sum();
        Some(hydrator.reserve_response_bytes(missing_bytes).await?)
    };
    let downloaded_bodies = hydrator
        .download_all(missing_references)
        .await
        .inspect_err(|error| hydration_result.record_download_error(error))?;
    let started_at = Instant::now();
    let parse_options = if context.preserve_session_update_mode {
        SpecsResponseParseOptions::preserving_session_update_mode()
    } else {
        SpecsResponseParseOptions::default()
    };
    // No thread-local mmap or decode scope crosses an await. The same parsed
    // returnable is installed in both the candidate spec and its provenance.
    let (reference_count, total_bytes) = (input.reference_count, input.total_bytes);
    let (candidate, spec_decode_stats) = track_spec_decodes(|| {
        InternedStore::with_mmap_project(context.mmap_project_id, || {
            with_parse_options(parse_options, || {
                build_hydrated_json_snapshot(
                    input,
                    data,
                    verified_values,
                    downloaded_bodies,
                    context.capture_data_store_bytes,
                )
            })
        })
    });
    let (snapshot, verified_by_config) = candidate?;
    hydrator.log_phase_latency(started_at.elapsed(), HydrationPhase::JsonApply);
    hydration_result.log_hydration_success(reference_count, total_bytes);
    Ok(Some(HydratedJsonStoreUpdate {
        values: snapshot,
        spec_decode_stats,
        verified_remote_values: verified_by_config,
    }))
}

fn build_hydrated_json_snapshot(
    input: JsonHydrationInput,
    data: &mut ResponseData,
    mut verified_values: VerifiedRemoteValues,
    downloaded_bodies: HashMap<String, Arc<Vec<u8>>>,
    capture_data_store_bytes: bool,
) -> Result<(Box<SpecsResponseFull>, VerifiedRemoteConfigValues), StatsigErr> {
    let JsonHydrationInput {
        mut payload,
        configs,
        references,
        ..
    } = input;
    for reference in references {
        let sha = reference.metadata.sha256.to_string();
        if let Entry::Vacant(entry) = verified_values.entry(sha) {
            let body = hydrated_value(&downloaded_bodies, entry.key())?;
            let value = Arc::new(VerifiedRemoteValue::from_verified_json_body(
                reference.metadata,
                body,
            )?);
            entry.insert(value);
        }
    }
    // Parsed values own their backing; only datastore capture needs raw bodies.
    let downloaded_bodies = capture_data_store_bytes.then_some(downloaded_bodies);
    // The store decoder has always appended dynamic_configs after the other fields.
    payload.remove("dynamic_configs");
    let mut ordinary_configs = RawJsonObject::default();
    let mut remote_configs = Vec::new();
    for config in configs {
        if config.use_remote_decoder {
            remote_configs.push(config);
        } else {
            ordinary_configs.0.push((config.name, config.raw_spec));
        }
    }
    payload.insert(
        "dynamic_configs".to_string(),
        raw_json_value(&RawJsonObject::default())?,
    );
    let bytes = serde_json::to_vec(&payload)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    let mut snapshot: Box<SpecsResponseFull> = serde_json::from_slice(&bytes)
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))?;
    drop(bytes);
    // These fragments already passed JSON validation. Reuse the ordinary
    // decoder without rebuilding and reparsing their enclosing raw map.
    snapshot.dynamic_configs = decode_raw_dynamic_configs(
        ordinary_configs
            .0
            .iter()
            .map(|(name, value)| (InternedString::from_str_ref(name), value.as_ref()))
            .collect(),
    )
    .map_err(|error: serde_json::Error| {
        StatsigErr::JsonParseError(TAG.to_string(), error.to_string())
    })?;
    // Read-only updates no longer need either raw snapshot buffer.
    let mut data_store_json = capture_data_store_bytes.then_some((payload, ordinary_configs));
    if let Some((_, ordinary_configs)) = data_store_json.as_mut() {
        // Skipped specs must not leave unresolved links in an offline snapshot.
        ordinary_configs.0.retain(|(name, _)| {
            snapshot
                .dynamic_configs
                .get(&InternedString::from_str_ref(name))
                .is_some()
        });
    }
    let mut verified_by_config = VerifiedRemoteConfigValues::new();
    for config in remote_configs {
        let key = InternedString::from_str_ref(&config.name);
        let Some((spec, provenance, sidecar)) = hydrate_remote_json_spec(
            &key,
            &config.raw_spec,
            &verified_values,
            downloaded_bodies.as_ref(),
        )?
        else {
            continue;
        };
        snapshot.dynamic_configs.insert(key.clone(), spec);
        if !provenance.is_empty() {
            verified_by_config.insert(key, Arc::new(provenance));
        }
        if let (Some(sidecar), Some((_, ordinary_configs))) = (sidecar, data_store_json.as_mut()) {
            ordinary_configs.0.push((config.name, sidecar));
        }
    }
    if let Some((mut payload, ordinary_configs)) = data_store_json {
        payload.insert(
            "dynamic_configs".to_string(),
            raw_json_value(&ordinary_configs)?,
        );
        let bytes = serde_json::to_vec(&payload)
            .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
        data.replace_bytes(bytes);
    }
    Ok((snapshot, verified_by_config))
}

type HydratedJsonSpec = (SpecPointer, VerifiedRemoteValues, Option<Box<RawValue>>);

fn hydrate_remote_json_spec(
    key: &InternedString,
    config: &RawValue,
    verified_values: &VerifiedRemoteValues,
    capture_bodies: Option<&HashMap<String, Arc<Vec<u8>>>>,
) -> Result<Option<HydratedJsonSpec>, StatsigErr> {
    let Some(mut config) = parse_optional_raw_json_object(config)? else {
        return Ok(None);
    };
    let mut provenance = VerifiedRemoteValues::new();
    let mut resolve_verified_value = |metadata: RemoteConfigValueMetadata| {
        let value = verified_values
            .get(metadata.sha256.as_str())
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::MissingHydratedValue,
                    "remote value has no verified parsed value",
                )
            })?;
        if !value.matches_metadata(&metadata) {
            return Err(hydration_error(
                HydrationFailureReason::MetadataConflict,
                "remote value metadata did not match its verified value",
            ));
        }
        provenance.insert(metadata.sha256.to_string(), Arc::clone(value));
        Ok(Arc::clone(value))
    };
    let remote_default_value = raw_json_default_metadata(&config)?
        .map(&mut resolve_verified_value)
        .transpose()?;
    if remote_default_value.is_some() {
        config.insert("defaultValue".to_string(), raw_json_value(&())?);
        config.remove("remoteConfigMetadata");
    }
    let mut rules = config
        .get("rules")
        .map(parse_optional_raw_json_array)
        .transpose()?
        .flatten();
    let mut remote_rule_values = Vec::new();
    if let Some(rules) = rules.as_mut() {
        for (rule_index, rule) in rules.iter_mut().enumerate() {
            let Some(mut rule_object) = parse_optional_raw_json_object(rule)? else {
                continue;
            };
            let value = rule_object
                .get("remoteConfigMetadata")
                .map(parse_raw_json_metadata)
                .transpose()?
                .map(&mut resolve_verified_value)
                .transpose()?;
            if let Some(value) = value {
                rule_object.insert("returnValue".to_string(), raw_json_value(&())?);
                rule_object.remove("remoteConfigMetadata");
                *rule = raw_json_value(&rule_object)?;
                remote_rule_values.push((rule_index, value));
            }
        }
        if !remote_rule_values.is_empty() {
            config.insert("rules".to_string(), raw_json_value(rules)?);
        }
    }
    // Remote specs must bypass mmap's checksum-only shortcut: that pointer may
    // still contain an old URL placeholder. Ordinary configs use the normal parser.
    let fields = config
        .0
        .iter()
        .map(|(name, value)| (name.as_str(), value.as_ref()));
    let mut spec = match Spec::deserialize(MapDeserializer::new(fields)) {
        Ok(spec) => spec,
        Err(error) => {
            log_e!(TAG, "Failed to deserialize spec: {}", error);
            return Ok(None);
        }
    };
    if let Some(value) = &remote_default_value {
        spec.default_value = value.value.clone();
    }
    for (rule_index, value) in &remote_rule_values {
        spec.rules[*rule_index].return_value = value.value.clone();
    }
    let sidecar = if let Some(bodies) = capture_bodies {
        let raw_value_for_datastore =
            |value: &Arc<VerifiedRemoteValue>| match bodies.get(value.sha256()) {
                Some(body) => serde_json::from_slice(body)
                    .map_err(|error| StatsigErr::SerializationError(error.to_string())),
                None => raw_json_value(&value.value),
            };
        if let Some(value) = &remote_default_value {
            config.insert("defaultValue".to_string(), raw_value_for_datastore(value)?);
        }
        if let Some(rules) = rules.as_mut().filter(|_| !remote_rule_values.is_empty()) {
            for (rule_index, value) in &remote_rule_values {
                let rule = &mut rules[*rule_index];
                let mut rule_object =
                    parse_optional_raw_json_object(rule)?.expect("hydrated rule is an object");
                rule_object.insert("returnValue".to_string(), raw_value_for_datastore(value)?);
                *rule = raw_json_value(&rule_object)?;
            }
            config.insert("rules".to_string(), raw_json_value(rules)?);
        }
        Some(raw_json_value(&config)?)
    } else {
        None
    };
    let pointer =
        matching_preloaded_json_spec(key, &spec, &remote_default_value, &remote_rule_values)
            .unwrap_or_else(|| SpecPointer::from_spec(spec));
    Ok(Some((pointer, provenance, sidecar)))
}

fn matching_preloaded_json_spec(
    key: &InternedString,
    spec: &Spec,
    remote_default_value: &Option<Arc<VerifiedRemoteValue>>,
    remote_rule_values: &[(usize, Arc<VerifiedRemoteValue>)],
) -> Option<SpecPointer> {
    let preloaded = InternedStore::try_get_preloaded_spec(key, spec.entity.as_str())?
        .with_session_update_mode(spec.session_update_mode.as_deref())?;
    let view = preloaded.view();
    // The producer checksum alone also matches old URL placeholders. Require
    // the complete hydrated content and the actual verified remote backing;
    // equal parsed JSON with different original bytes cannot inherit a proof.
    if view.checksum().map(|value| value.as_str()) != spec.checksum.as_deref()
        || !preloaded.matches_owned_spec(spec)
        || remote_default_value
            .as_ref()
            .is_some_and(|value| !value.matches_backing_value(&view.default_value().to_owned()))
        || remote_rule_values.iter().any(|(rule_index, value)| {
            !value.matches_backing_value(&view.rule(*rule_index).return_value().to_owned())
        })
    {
        return None;
    }
    Some(preloaded)
}

pub(super) async fn hydrate_response(
    hydrator: &RemoteConfigValueHydrator,
    data: &mut ResponseData,
    source_url: &str,
    hydration_result: &mut HydrationResult<'_>,
) -> Result<bool, StatsigErr> {
    let started_at = Instant::now();
    let Some(input) = parse_json_hydration_input(data, source_url, hydration_result)? else {
        return Ok(false);
    };
    let JsonHydrationInput {
        mut payload,
        configs,
        references,
        reference_count,
        total_bytes,
    } = input;
    hydrator.log_phase_latency(started_at.elapsed(), HydrationPhase::JsonParse);
    // Reserve the response's concurrency window before any download starts so
    // retained sibling blobs cannot deadlock against another response.
    let _download_reservation = hydrator.reserve_response_bytes(total_bytes).await?;
    let downloaded_bodies = hydrator
        .download_all(references)
        .await
        .inspect_err(|error| hydration_result.record_download_error(error))?;
    let started_at = Instant::now();
    let mut configs = RawJsonObject(
        configs
            .into_iter()
            .map(|config| (config.name, config.raw_spec))
            .collect(),
    );
    apply_json_config_hydration(&mut configs, &downloaded_bodies)?;
    payload.insert("dynamic_configs".to_string(), raw_json_value(&configs)?);
    let hydrated_bytes = serde_json::to_vec(&payload)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    data.replace_bytes(hydrated_bytes);
    hydrator.log_phase_latency(started_at.elapsed(), HydrationPhase::JsonApply);

    hydration_result.log_hydration_success(reference_count, total_bytes);
    Ok(true)
}

// serde_json::Map only implements serde for Value. Keep an ordered raw map so
// untouched fields serialize in their original order without ever decoding
// their numbers into serde_json::Number.
#[derive(Default)]
pub(super) struct RawJsonObject(Vec<(String, Box<RawValue>)>);

impl RawJsonObject {
    fn get(&self, key: &str) -> Option<&RawValue> {
        self.0
            .iter()
            .find_map(|(candidate, value)| (candidate == key).then_some(value.as_ref()))
    }

    fn contains_key(&self, key: &str) -> bool {
        self.get(key).is_some()
    }

    fn insert(&mut self, key: String, value: Box<RawValue>) {
        if let Some((_, existing)) = self.0.iter_mut().find(|(candidate, _)| candidate == &key) {
            *existing = value;
            return;
        }
        self.0.push((key, value));
    }

    fn remove(&mut self, key: &str) -> Option<Box<RawValue>> {
        let index = self.0.iter().position(|(candidate, _)| candidate == key)?;
        Some(self.0.remove(index).1)
    }

    fn values_mut(&mut self) -> impl Iterator<Item = &mut Box<RawValue>> {
        self.0.iter_mut().map(|(_, value)| value)
    }

    fn len(&self) -> usize {
        self.0.len()
    }
}

impl<'de> Deserialize<'de> for RawJsonObject {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        struct RawJsonObjectVisitor;

        impl<'de> Visitor<'de> for RawJsonObjectVisitor {
            type Value = RawJsonObject;

            fn expecting(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                formatter.write_str("a JSON object")
            }

            fn visit_map<A>(self, mut map: A) -> Result<Self::Value, A::Error>
            where
                A: MapAccess<'de>,
            {
                let mut entries: Vec<(String, Box<RawValue>)> =
                    Vec::with_capacity(map.size_hint().unwrap_or_default());
                let mut positions = HashMap::<String, usize>::new();
                while let Some((key, value)) = map.next_entry::<String, Box<RawValue>>()? {
                    if let Some(index) = positions.get(&key) {
                        entries[*index].1 = value;
                    } else {
                        positions.insert(key.clone(), entries.len());
                        entries.push((key, value));
                    }
                }
                Ok(RawJsonObject(entries))
            }
        }

        deserializer.deserialize_map(RawJsonObjectVisitor)
    }
}

impl Serialize for RawJsonObject {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let mut map = serializer.serialize_map(Some(self.len()))?;
        for (key, value) in &self.0 {
            map.serialize_entry(key, value)?;
        }
        map.end()
    }
}

// JSON DCS return values are intentionally kept as RawValue fragments while we
// find and patch remote placeholders. Parsing the whole response into Value
// and serializing it again would round or reformat unrelated JSON numbers when
// serde_json is built without arbitrary_precision.
fn collect_json_references(
    payload: &mut RawJsonObject,
    source_url: &str,
    hydration_result: &mut HydrationResult<'_>,
) -> Result<(Vec<RemoteValueReference>, Vec<JsonConfigEntry>), StatsigErr> {
    let Some((_, raw_configs)) = payload
        .0
        .iter_mut()
        .find(|(name, _)| name == "dynamic_configs")
    else {
        return Ok((Vec::new(), Vec::new()));
    };
    let Some(configs) = parse_optional_raw_json_object(raw_configs)? else {
        return Ok((Vec::new(), Vec::new()));
    };
    // Keep the top-level field position, but release the duplicate raw container
    // before downloads. The prepared entries retain each config's original text.
    *raw_configs = raw_json_value(&())?;

    let mut references = HashMap::<String, RemoteValueReference>::new();
    let mut entries = Vec::with_capacity(configs.len());
    for (name, raw_spec) in configs.0 {
        // An escaped metadata key must contain a Unicode escape. Configs with
        // neither spelling cannot have remote references; keep their raw text.
        let raw = raw_spec.get();
        let config = if raw.contains("remoteConfigMetadata") || raw.contains("\\u") {
            parse_optional_raw_json_object(&raw_spec)?
        } else {
            None
        };
        let Some(config) = config else {
            entries.push(JsonConfigEntry {
                name,
                raw_spec,
                use_remote_decoder: false,
            });
            continue;
        };

        let has_remote_default = config.contains_key("remoteConfigMetadata");
        if has_remote_default {
            hydration_result.mark_remote_metadata();
        }
        if let Some(metadata) = raw_json_default_metadata(&config)? {
            add_raw_value_reference(
                &mut references,
                config.get("defaultValue"),
                metadata,
                source_url,
            )?;
        }

        let rules = config
            .get("rules")
            .map(parse_optional_raw_json_array)
            .transpose()?
            .flatten();
        let mut all_rules_are_objects = true;
        let mut has_remote_rule = false;
        if let Some(rules) = rules {
            for rule in rules {
                let Some(rule) = parse_optional_raw_json_object(rule.as_ref())? else {
                    all_rules_are_objects = false;
                    continue;
                };
                let Some(metadata_value) = rule.get("remoteConfigMetadata") else {
                    continue;
                };
                has_remote_rule = true;
                hydration_result.mark_remote_metadata();
                let metadata = parse_raw_json_metadata(metadata_value)?;
                add_raw_value_reference(
                    &mut references,
                    rule.get("returnValue"),
                    metadata,
                    source_url,
                )?;
            }
        }
        // Match the decoder's existing metadata guard: a rule-only remote spec
        // with a non-object rule stays on the tolerant ordinary-spec path.
        entries.push(JsonConfigEntry {
            name,
            raw_spec,
            use_remote_decoder: has_remote_default || (all_rules_are_objects && has_remote_rule),
        });
    }

    Ok((references.into_values().collect(), entries))
}

fn parse_raw_json_object_from_response(
    data: &mut ResponseData,
) -> Result<Option<RawJsonObject>, StatsigErr> {
    data.rewind()?;
    let mut first_non_whitespace = None;
    let mut byte = [0u8; 1];
    loop {
        let bytes_read = data
            .get_stream_mut()
            .read(&mut byte)
            .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
        if bytes_read == 0 {
            break;
        }
        if !byte[0].is_ascii_whitespace() {
            first_non_whitespace = Some(byte[0]);
            break;
        }
    }
    data.rewind()?;

    if first_non_whitespace != Some(b'{') {
        // Validate valid non-object JSON before keeping the previous no-op
        // behavior for responses that only mention the marker in a string.
        serde_json::from_reader::<_, Box<RawValue>>(data.get_stream_mut())
            .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))?;
        return Ok(None);
    }

    // Keep owned raw fields and the same error mapping on both input paths.
    let payload = match data.shared_bytes() {
        Some(bytes) => serde_json::from_slice(bytes),
        None => serde_json::from_reader(data.get_stream_mut()),
    };
    payload
        .map(Some)
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))
}

fn parse_optional_raw_json_object(value: &RawValue) -> Result<Option<RawJsonObject>, StatsigErr> {
    if !value.get().trim_start().starts_with('{') {
        return Ok(None);
    }
    serde_json::from_str(value.get())
        .map(Some)
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))
}

fn parse_optional_raw_json_array(
    value: &RawValue,
) -> Result<Option<Vec<Box<RawValue>>>, StatsigErr> {
    if !value.get().trim_start().starts_with('[') {
        return Ok(None);
    }
    serde_json::from_str(value.get())
        .map(Some)
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))
}

fn raw_json_default_metadata(
    config: &RawJsonObject,
) -> Result<Option<RemoteConfigValueMetadata>, StatsigErr> {
    let Some(metadata_value) = config.get("remoteConfigMetadata") else {
        return Ok(None);
    };
    let Some(metadata) = parse_optional_raw_json_object(metadata_value)? else {
        return Err(hydration_error(
            HydrationFailureReason::InvalidDefaultMetadata,
            "default remoteConfigMetadata was not an object",
        ));
    };
    if metadata.contains_key("sha256") {
        return parse_raw_json_metadata(metadata_value).map(Some);
    }
    match metadata.get("defaultValue") {
        Some(value) => parse_raw_json_metadata(value).map(Some),
        None => Err(hydration_error(
            HydrationFailureReason::InvalidDefaultMetadata,
            "default remoteConfigMetadata was neither flat metadata nor a defaultValue wrapper",
        )),
    }
}

fn parse_raw_json_metadata(value: &RawValue) -> Result<RemoteConfigValueMetadata, StatsigErr> {
    let wire: RemoteConfigValueMetadataWire =
        serde_json::from_str(value.get()).map_err(|error| {
            hydration_error(
                HydrationFailureReason::InvalidMetadata,
                &format!("failed to parse remote value metadata: {error}"),
            )
        })?;
    wire.try_into()
}

fn raw_json_value<T: Serialize>(value: &T) -> Result<Box<RawValue>, StatsigErr> {
    to_raw_value(value).map_err(|error| StatsigErr::SerializationError(error.to_string()))
}

#[cfg(test)]
pub(super) fn apply_json_hydration(
    payload: &mut RawJsonObject,
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
) -> Result<(), StatsigErr> {
    let Some(configs) = payload.get("dynamic_configs") else {
        return Ok(());
    };
    let Some(mut configs) = parse_optional_raw_json_object(configs)? else {
        return Ok(());
    };

    if apply_json_config_hydration(&mut configs, hydrated)? {
        payload.insert("dynamic_configs".to_string(), raw_json_value(&configs)?);
    }
    Ok(())
}

fn apply_json_config_hydration(
    configs: &mut RawJsonObject,
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
) -> Result<bool, StatsigErr> {
    let mut configs_changed = false;
    for config in configs.values_mut() {
        let Some(mut config_object) = parse_optional_raw_json_object(config.as_ref())? else {
            continue;
        };
        let mut config_changed = false;

        if let Some(metadata) = raw_json_default_metadata(&config_object)? {
            let value = hydrated_raw_json_value(hydrated, metadata.sha256.as_str())?;
            config_object.insert("defaultValue".to_string(), value);
            config_object.remove("remoteConfigMetadata");
            config_changed = true;
        }

        let rules = config_object
            .get("rules")
            .map(parse_optional_raw_json_array)
            .transpose()?
            .flatten();
        if let Some(mut rules) = rules {
            let mut rules_changed = false;
            for rule in &mut rules {
                let Some(mut rule_object) = parse_optional_raw_json_object(rule.as_ref())? else {
                    continue;
                };
                let Some(metadata_value) = rule_object.get("remoteConfigMetadata") else {
                    continue;
                };
                let metadata = parse_raw_json_metadata(metadata_value)?;
                let value = hydrated_raw_json_value(hydrated, metadata.sha256.as_str())?;
                rule_object.insert("returnValue".to_string(), value);
                rule_object.remove("remoteConfigMetadata");
                *rule = raw_json_value(&rule_object)?;
                rules_changed = true;
            }
            if rules_changed {
                config_object.insert("rules".to_string(), raw_json_value(&rules)?);
                config_changed = true;
            }
        }

        if config_changed {
            *config = raw_json_value(&config_object)?;
            configs_changed = true;
        }
    }

    Ok(configs_changed)
}

fn hydrated_raw_json_value(
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
    sha256: &str,
) -> Result<Box<RawValue>, StatsigErr> {
    serde_json::from_slice(hydrated_value(hydrated, sha256)?).map_err(|error| {
        hydration_error(
            HydrationFailureReason::InvalidJson,
            &format!("remote value {sha256} was not valid JSON: {error}"),
        )
    })
}

pub(super) fn response_may_contain_remote_metadata(
    data: &mut ResponseData,
) -> Result<bool, StatsigErr> {
    // Producer responses normally use the literal key, but local/bootstrap JSON
    // can escape any part of it. Scan JSON strings just deeply enough to match
    // the decoded key so unrelated unicode escapes keep the no-metadata fast path.
    response_contains_json_key(data, b"remoteConfigMetadata")
}

fn response_contains_json_key(data: &mut ResponseData, key: &[u8]) -> Result<bool, StatsigErr> {
    if key.is_empty() {
        return Ok(true);
    }

    const SCAN_CHUNK_BYTES: usize = 8 * 1024;
    data.rewind()?;
    let mut chunk = [0u8; SCAN_CHUNK_BYTES];
    let mut scanner = JsonKeyScanner::new(key);
    let found = loop {
        let bytes_read = data
            .get_stream_mut()
            .read(&mut chunk)
            .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
        if bytes_read == 0 {
            break scanner.finish();
        }

        if scanner.scan(&chunk[..bytes_read]) {
            break true;
        }
    };
    data.rewind()?;
    Ok(found)
}

#[derive(Clone, Copy)]
enum JsonStringEscape {
    None,
    AfterBackslash,
    Unicode { value: u16, digits: u8 },
}

struct JsonKeyScanner<'a> {
    key: &'a [u8],
    in_string: bool,
    awaiting_colon: bool,
    candidate_matches: bool,
    candidate_index: usize,
    escape: JsonStringEscape,
}

impl<'a> JsonKeyScanner<'a> {
    fn new(key: &'a [u8]) -> Self {
        Self {
            key,
            in_string: false,
            awaiting_colon: false,
            candidate_matches: false,
            candidate_index: 0,
            escape: JsonStringEscape::None,
        }
    }

    fn scan(&mut self, bytes: &[u8]) -> bool {
        for &byte in bytes {
            if self.in_string {
                if self.scan_string_byte(byte) {
                    return true;
                }
                continue;
            }

            if self.awaiting_colon {
                if byte.is_ascii_whitespace() {
                    continue;
                }
                self.awaiting_colon = false;
                if byte == b':' {
                    return true;
                }
            }

            if byte == b'"' {
                self.in_string = true;
                self.candidate_matches = true;
                self.candidate_index = 0;
                self.escape = JsonStringEscape::None;
            }
        }
        false
    }

    fn scan_string_byte(&mut self, byte: u8) -> bool {
        match self.escape {
            JsonStringEscape::None => match byte {
                b'"' => {
                    self.in_string = false;
                    self.awaiting_colon =
                        self.candidate_matches && self.candidate_index == self.key.len();
                }
                b'\\' => self.escape = JsonStringEscape::AfterBackslash,
                _ => self.push_decoded_byte(byte),
            },
            JsonStringEscape::AfterBackslash => {
                self.escape = match byte {
                    b'u' => JsonStringEscape::Unicode {
                        value: 0,
                        digits: 0,
                    },
                    b'"' | b'\\' | b'/' | b'b' | b'f' | b'n' | b'r' | b't' => {
                        self.candidate_matches = false;
                        JsonStringEscape::None
                    }
                    _ => return true,
                };
            }
            JsonStringEscape::Unicode { value, digits } => {
                let Some(nibble) = hex_nibble(byte) else {
                    self.escape = JsonStringEscape::None;
                    return true;
                };
                let value = (value << 4) | u16::from(nibble);
                let digits = digits + 1;
                if digits == 4 {
                    if let Ok(decoded) = u8::try_from(value) {
                        self.push_decoded_byte(decoded);
                    } else {
                        self.candidate_matches = false;
                    }
                    self.escape = JsonStringEscape::None;
                } else {
                    self.escape = JsonStringEscape::Unicode { value, digits };
                }
            }
        }
        false
    }

    fn push_decoded_byte(&mut self, byte: u8) {
        if !self.candidate_matches {
            return;
        }
        if self.key.get(self.candidate_index) == Some(&byte) {
            self.candidate_index += 1;
        } else {
            self.candidate_matches = false;
        }
    }

    fn finish(&self) -> bool {
        self.in_string
            || matches!(
                self.escape,
                JsonStringEscape::AfterBackslash | JsonStringEscape::Unicode { .. }
            )
    }
}

fn hex_nibble(byte: u8) -> Option<u8> {
    match byte {
        b'0'..=b'9' => Some(byte - b'0'),
        b'a'..=b'f' => Some(byte - b'a' + 10),
        b'A'..=b'F' => Some(byte - b'A' + 10),
        _ => None,
    }
}

#[cfg(test)]
#[path = "../__tests__/json_hydration_preparation_tests.rs"]
mod tests;

#[cfg(test)]
#[path = "../__tests__/json_raw_config_handoff_tests.rs"]
mod raw_config_handoff_tests;
