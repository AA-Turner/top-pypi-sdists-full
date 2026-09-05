use std::collections::HashMap;
use std::sync::Arc;

use serde::{
    Deserialize, Serialize,
    de::{MapAccess, Visitor},
    ser::SerializeMap,
};
use serde_json::value::{RawValue, to_raw_value};

use crate::StatsigErr;
use crate::networking::ResponseData;

use super::{
    HydrationFailureReason, RemoteConfigValueHydrator, RemoteConfigValueMetadata,
    RemoteConfigValueMetadataWire, RemoteValueReference, TAG, add_raw_value_reference,
    hydrated_value, hydration_error, validate_reference_limits,
};

pub(super) async fn hydrate_response(
    hydrator: &RemoteConfigValueHydrator,
    data: &mut ResponseData,
    source_url: &str,
) -> Result<bool, StatsigErr> {
    if !response_may_contain_remote_metadata(data)? {
        return Ok(false);
    }
    let Some(mut payload) = parse_raw_json_object_from_response(data)? else {
        data.rewind()?;
        return Ok(false);
    };
    let references = collect_json_references(&payload, source_url)?;
    if references.is_empty() {
        data.rewind()?;
        return Ok(false);
    }
    let (reference_count, total_bytes) = validate_reference_limits(&references)?;
    // Reserve the response's concurrency window before any download starts so
    // retained sibling blobs cannot deadlock against another response.
    let _response_budget = hydrator.reserve_response_bytes(total_bytes).await?;
    let hydrated = hydrator.download_all(references).await?;
    apply_json_hydration(&mut payload, &hydrated)?;
    let hydrated_bytes = serde_json::to_vec(&payload)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    data.replace_bytes(hydrated_bytes);

    hydrator.log_hydration_success(reference_count, total_bytes);
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

    fn values(&self) -> impl Iterator<Item = &RawValue> {
        self.0.iter().map(|(_, value)| value.as_ref())
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
    payload: &RawJsonObject,
    source_url: &str,
) -> Result<Vec<RemoteValueReference>, StatsigErr> {
    let Some(configs) = payload.get("dynamic_configs") else {
        return Ok(Vec::new());
    };
    let Some(configs) = parse_optional_raw_json_object(configs)? else {
        return Ok(Vec::new());
    };

    let mut references = HashMap::<String, RemoteValueReference>::new();
    for config in configs.values() {
        let Some(config) = parse_optional_raw_json_object(config)? else {
            continue;
        };

        if let Some(metadata) = raw_json_default_metadata(&config)? {
            add_raw_value_reference(
                &mut references,
                config.get("defaultValue"),
                metadata,
                source_url,
            )?;
        }

        let Some(rules) = config.get("rules") else {
            continue;
        };
        let Some(rules) = parse_optional_raw_json_array(rules)? else {
            continue;
        };
        for rule in rules {
            let Some(rule) = parse_optional_raw_json_object(rule.as_ref())? else {
                continue;
            };
            let Some(metadata_value) = rule.get("remoteConfigMetadata") else {
                continue;
            };
            let metadata = parse_raw_json_metadata(metadata_value)?;
            add_raw_value_reference(
                &mut references,
                rule.get("returnValue"),
                metadata,
                source_url,
            )?;
        }
    }

    Ok(references.into_values().collect())
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

    serde_json::from_reader(data.get_stream_mut())
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

    if !configs_changed {
        return Ok(());
    }
    payload.insert("dynamic_configs".to_string(), raw_json_value(&configs)?);
    Ok(())
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
