//! Encoder for the deliberately small synthetic benchmark JSON vocabulary.
use prost::Message;
use serde::{Deserialize, Serializer, ser::SerializeMap};
use serde_json::{Map, Value};
use statsig_rust::specs_response::statsig_config_specs as pb;
use std::io::Write;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

const COLLECTIONS: [(&str, pb::SpecsEnvelopeKind); 5] = [
    ("condition_map", pb::SpecsEnvelopeKind::Condition),
    ("dynamic_configs", pb::SpecsEnvelopeKind::DynamicConfig),
    ("feature_gates", pb::SpecsEnvelopeKind::FeatureGate),
    ("layer_configs", pb::SpecsEnvelopeKind::LayerConfig),
    ("param_stores", pb::SpecsEnvelopeKind::ParamStore),
];

pub fn encode_full(state: &Value) -> Result<Vec<u8>> {
    encode(None, state)
}

pub fn encode_delta(before: &Value, after: &Value) -> Result<Vec<u8>> {
    encode(Some(before), after)
}

fn object(value: &Value) -> Result<&Map<String, Value>> {
    value.as_object().ok_or_else(|| "expected an object".into())
}

fn field<'a, T: Deserialize<'a>>(value: &'a Value, key: &str) -> Result<T> {
    let value = value.get(key).ok_or_else(|| format!("missing {key}"))?;
    T::deserialize(value).map_err(|error| format!("{key}: {error}").into())
}

fn optional<'a, T: Deserialize<'a>>(value: &'a Value, key: &str) -> Result<Option<T>> {
    Ok(Option::<T>::deserialize(&value[key])?)
}

fn only_fields(value: &Value, allowed: &[&str]) -> Result<()> {
    for key in object(value)?.keys() {
        if !allowed.contains(&key.as_str()) {
            return Err(format!("unsupported field {key}").into());
        }
    }
    Ok(())
}

fn entity_checksum(value: &Value) -> Result<(&str, u32)> {
    let checksum: &str = field(value, "checksum")?;
    if checksum.is_empty() || !checksum.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err("entity checksum must be a decimal u32 string".into());
    }
    Ok((checksum, checksum.parse()?))
}

fn id_type(value: &Value) -> Result<Option<pb::IdType>> {
    let id: &str = field(value, "idType")?;
    let id = match id {
        "userID" => pb::id_type::IdType::KnownIdType(pb::KnownIdType::UserId as i32),
        custom => pb::id_type::IdType::CustomIdType(custom.to_owned()),
    };
    Ok(Some(pb::IdType { id_type: Some(id) }))
}

fn return_value(value: &Value, kind: pb::SpecsEnvelopeKind) -> Result<Option<pb::ReturnValue>> {
    let value = if kind == pb::SpecsEnvelopeKind::FeatureGate {
        pb::return_value::Value::BoolValue(
            value
                .as_bool()
                .ok_or("feature gate return values must be boolean")?,
        )
    } else {
        pb::return_value::Value::RawValue(serde_json::to_vec(value)?)
    };
    Ok(Some(pb::ReturnValue { value: Some(value) }))
}

fn remote_metadata(
    value: &Value,
    kind: pb::SpecsEnvelopeKind,
) -> Result<Option<pb::RemoteConfigValueMetadata>> {
    let Some(metadata) = value.get("remoteConfigMetadata").filter(|v| !v.is_null()) else {
        return Ok(None);
    };
    if kind != pb::SpecsEnvelopeKind::DynamicConfig {
        return Err(format!("remoteConfigMetadata is unsupported in {kind:?} envelopes").into());
    }
    only_fields(
        metadata,
        &["sha256", "byteLength", "contentType", "compression"],
    )?;
    Ok(Some(pb::RemoteConfigValueMetadata {
        sha256: field(metadata, "sha256")?,
        byte_length: field(metadata, "byteLength")?,
        content_type: field(metadata, "contentType")?,
        compression: field(metadata, "compression")?,
    }))
}

fn rule(value: &Value, kind: pb::SpecsEnvelopeKind) -> Result<pb::Rule> {
    only_fields(
        value,
        &[
            "name",
            "id",
            "salt",
            "idType",
            "passPercentage",
            "returnValue",
            "conditions",
            "groupName",
            "configDelegate",
            "isExperimentGroup",
            "remoteConfigMetadata",
        ],
    )?;
    Ok(pb::Rule {
        name: field(value, "name")?,
        id: field(value, "id")?,
        salt: optional(value, "salt")?,
        id_type: id_type(value)?,
        pass_percentage_float: Some(field(value, "passPercentage")?),
        return_value: return_value(value.get("returnValue").ok_or("missing returnValue")?, kind)?,
        conditions: field(value, "conditions")?,
        group_name: optional(value, "groupName")?,
        config_delegate: optional(value, "configDelegate")?,
        is_experiment_group: optional(value, "isExperimentGroup")?,
        remote_config_metadata: remote_metadata(value, kind)?,
        ..Default::default()
    })
}

fn spec(value: &Value, kind: pb::SpecsEnvelopeKind) -> Result<pb::Spec> {
    only_fields(
        value,
        &[
            "checksum",
            "type",
            "entity",
            "salt",
            "idType",
            "enabled",
            "version",
            "defaultValue",
            "rules",
            "isActive",
            "hasSharedParams",
            "explicitParameters",
            "targetAppIDs",
            "forwardAllExposures",
            "fieldsUsed",
            "useNewLayerEval",
            "sessionUpdateMode",
            "remoteConfigMetadata",
        ],
    )?;
    let entity: &str = field(value, "entity")?;
    let entity = match (kind, entity) {
        (pb::SpecsEnvelopeKind::FeatureGate, "feature_gate") => pb::EntityType::EntityFeatureGate,
        (pb::SpecsEnvelopeKind::DynamicConfig, "dynamic_config") => {
            pb::EntityType::EntityDynamicConfig
        }
        (pb::SpecsEnvelopeKind::DynamicConfig, "experiment") => pb::EntityType::EntityExperiment,
        (pb::SpecsEnvelopeKind::LayerConfig, "layer") => pb::EntityType::EntityLayer,
        _ => return Err(format!("unsupported entity {entity} in {kind:?}").into()),
    };
    let legacy_type: &str = field(value, "type")?;
    if legacy_type
        != if kind == pb::SpecsEnvelopeKind::FeatureGate {
            "feature_gate"
        } else {
            "dynamic_config"
        }
    {
        return Err("type does not match entity".into());
    }
    let rules = value
        .get("rules")
        .and_then(Value::as_array)
        .ok_or("missing rules array")?;
    Ok(pb::Spec {
        salt: field(value, "salt")?,
        enabled: field(value, "enabled")?,
        default_value: return_value(
            value.get("defaultValue").ok_or("missing defaultValue")?,
            kind,
        )?,
        entity: entity as i32,
        id_type: id_type(value)?,
        version: field(value, "version")?,
        rules: rules
            .iter()
            .map(|value| rule(value, kind))
            .collect::<Result<_>>()?,
        is_active: optional(value, "isActive")?,
        has_shared_params: optional(value, "hasSharedParams")?,
        explicit_parameters: optional(value, "explicitParameters")?.unwrap_or_default(),
        target_app_ids: optional(value, "targetAppIDs")?.unwrap_or_default(),
        forward_all_exposures: optional(value, "forwardAllExposures")?,
        fields_used: optional(value, "fieldsUsed")?.unwrap_or_default(),
        use_new_layer_eval: optional(value, "useNewLayerEval")?,
        session_update_mode: optional(value, "sessionUpdateMode")?,
        remote_config_metadata: remote_metadata(value, kind)?,
    })
}

fn condition(value: &Value) -> Result<pb::Condition> {
    only_fields(
        value,
        &[
            "checksum",
            "type",
            "idType",
            "targetValue",
            "operator",
            "field",
            "additionalValues",
        ],
    )?;
    let condition_type: &str = field(value, "type")?;
    let condition_type = match condition_type {
        "public" => pb::ConditionType::Public,
        "pass_gate" => pb::ConditionType::PassGate,
        "user_field" => pb::ConditionType::UserField,
        _ => return Err(format!("unsupported condition type {condition_type}").into()),
    };
    let operator = match optional::<&str>(value, "operator")? {
        None => None,
        Some("any") => Some(pb::Operator::Any as i32),
        Some(other) => return Err(format!("unsupported operator {other}").into()),
    };
    let target = value.get("targetValue").unwrap_or(&Value::Null);
    let target = match target {
        Value::String(text) => pb::any_value::Value::StringValue(text.clone()),
        other => pb::any_value::Value::RawValue(serde_json::to_vec(other)?),
    };
    let additional_values = match value.get("additionalValues") {
        None | Some(Value::Null) => None,
        Some(Value::Object(map)) if map.values().all(Value::is_string) => {
            Some(serde_json::to_vec(map)?)
        }
        _ => return Err("additionalValues must be an object with string values".into()),
    };
    Ok(pb::Condition {
        condition_type: condition_type as i32,
        id_type: id_type(value)?,
        target_value: Some(pb::AnyValue {
            value: Some(target),
        }),
        operator,
        field: optional(value, "field")?,
        additional_values,
    })
}

fn top_level(state: &Value) -> Result<pb::SpecsTopLevel> {
    const DEDICATED: &[&str] = &[
        "has_updates",
        "time",
        "company_id",
        "response_format",
        "checksum",
        "may_have_remote_config_metadata",
    ];
    const COMMON: &[&str] = &[
        "app_id",
        "cmab_configs",
        "default_environment",
        "diagnostics",
        "experiment_to_layer",
        "hashed_sdk_keys_to_app_ids",
        "id_lists",
        "override_rules",
        "overrides",
        "sdk_configs",
        "sdk_flags",
        "sdk_keys_to_app_ids",
        "session_replay_info",
        "auto_capture_settings",
        "gcir_config",
    ];
    let mut rest = Vec::new();
    let mut serializer = serde_json::Serializer::new(&mut rest);
    let mut common = serializer.serialize_map(None)?;
    for (key, value) in object(state)? {
        if COMMON.contains(&key.as_str()) {
            common.serialize_entry(key, value)?;
        } else if !DEDICATED.contains(&key.as_str())
            && !COLLECTIONS.iter().any(|(name, _)| name == key)
        {
            return Err(format!("unsupported top-level field {key}").into());
        }
    }
    common.end()?;
    // Validate types without reserializing them through SDK types (which may omit empty fields).
    serde_json::from_slice::<statsig_rust::specs_response::spec_types::SpecsResponsePartial>(
        &rest,
    )?;
    Ok(pb::SpecsTopLevel {
        has_updates: field(state, "has_updates")?,
        time: field(state, "time")?,
        company_id: optional(state, "company_id")?.unwrap_or_default(),
        response_format: field(state, "response_format")?,
        checksum: field(state, "checksum")?,
        rest,
        may_have_remote_config_metadata: optional(state, "may_have_remote_config_metadata")?,
    })
}

fn collection<'a>(
    state: Option<&'a Value>,
    name: &str,
    empty: &'a Map<String, Value>,
) -> Result<&'a Map<String, Value>> {
    let Some(state) = state else { return Ok(empty) };
    match state.get(name) {
        None | Some(Value::Null) if name == "param_stores" => Ok(empty),
        Some(value) => object(value),
        None => Err(format!("missing collection {name}").into()),
    }
}

fn envelope(
    writer: &mut impl Write,
    kind: pb::SpecsEnvelopeKind,
    entity: Option<(&str, &str)>,
    data: Option<Vec<u8>>,
) -> Result<()> {
    let (name, checksum) = entity.unwrap_or_default();
    let frame = pb::SpecsEnvelope {
        kind: kind as i32,
        name: name.into(),
        checksum: checksum.into(),
        data,
    };
    writer.write_all(&frame.encode_length_delimited_to_vec())?;
    Ok(())
}

fn config_has_remote_metadata(config: &Value) -> bool {
    let has_metadata = |value: &Value| !value["remoteConfigMetadata"].is_null();
    has_metadata(config)
        || config["rules"]
            .as_array()
            .is_some_and(|rules| rules.iter().any(has_metadata))
}

fn encode(before: Option<&Value>, after: &Value) -> Result<Vec<u8>> {
    let mut writer = zstd::stream::write::Encoder::new(Vec::new(), 3)?;
    if let Some(before) = before {
        top_level(before)?;
        envelope(&mut writer, pb::SpecsEnvelopeKind::CopyPrev, None, None)?;
    }
    let mut top = top_level(after)?;
    let empty = Map::new();
    let previous_configs = collection(before, "dynamic_configs", &empty)?;
    let configs = collection(Some(after), "dynamic_configs", &empty)?;
    // CopyPrev retains unchanged configs. Only emitted configs contribute to the hint.
    let emits_remote_metadata = configs.iter().any(|(name, config)| {
        config_has_remote_metadata(config) && previous_configs.get(name) != Some(config)
    });
    top.may_have_remote_config_metadata = Some(emits_remote_metadata);
    envelope(
        &mut writer,
        pb::SpecsEnvelopeKind::TopLevel,
        None,
        Some(top.encode_to_vec()),
    )?;
    let mut checksums = Vec::new();
    let mut deletions = pb::RulesetsResponseDeletions::default();
    let fields = object(after)?;
    // Emit entities in source order across collections as well as within each collection.
    let present = fields
        .keys()
        .filter_map(|key| COLLECTIONS.iter().find(|(name, _)| name == key));
    // Visit absent collections too: required ones must fail and optional ones need a zero checksum.
    let absent = COLLECTIONS
        .iter()
        .filter(|(name, _)| !fields.contains_key(*name));
    for &(name, kind) in present.chain(absent) {
        let next = collection(Some(after), name, &empty)?;
        let previous = collection(before, name, &empty)?;
        let mut sum = 0u64;
        for (key, value) in next {
            let (checksum, numeric_checksum) = entity_checksum(value)?;
            sum = sum.wrapping_add(u64::from(numeric_checksum));
            if let Some(old) = previous.get(key) {
                if old == value {
                    continue;
                }
                if entity_checksum(old)?.0 == checksum {
                    return Err(format!("changed {name}.{key} reuses its old checksum").into());
                }
            }
            let data = match kind {
                pb::SpecsEnvelopeKind::Condition => condition(value)?.encode_to_vec(),
                pb::SpecsEnvelopeKind::ParamStore => {
                    return Err("nonempty param_stores are outside the synthetic subset".into());
                }
                _ => spec(value, kind)?.encode_to_vec(),
            };
            envelope(&mut writer, kind, Some((key, checksum)), Some(data))?;
        }
        // A singleton map has no random iteration order; concatenation merges map entries.
        pb::RulesetsChecksums {
            field_checksums: [(name.to_owned(), sum)].into(),
        }
        .encode(&mut checksums)?;
        let mut removed: Vec<_> = previous
            .keys()
            .filter(|key| !next.contains_key(*key))
            .cloned()
            .collect();
        removed.sort();
        match kind {
            pb::SpecsEnvelopeKind::Condition => deletions.condition_map = removed,
            pb::SpecsEnvelopeKind::DynamicConfig => deletions.dynamic_configs = removed,
            pb::SpecsEnvelopeKind::FeatureGate => deletions.feature_gates = removed,
            pb::SpecsEnvelopeKind::LayerConfig => deletions.layer_configs = removed,
            pb::SpecsEnvelopeKind::ParamStore => deletions.param_stores = removed,
            _ => unreachable!(),
        }
    }
    if deletions != pb::RulesetsResponseDeletions::default() {
        envelope(
            &mut writer,
            pb::SpecsEnvelopeKind::Deletions,
            None,
            Some(deletions.encode_to_vec()),
        )?;
    }
    envelope(
        &mut writer,
        pb::SpecsEnvelopeKind::Checksums,
        None,
        Some(checksums),
    )?;
    envelope(&mut writer, pb::SpecsEnvelopeKind::Done, None, None)?;
    Ok(writer.finish()?)
}
