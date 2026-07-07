use std::{collections::HashMap, io::Cursor};

use prost::Message;
use serde_json::json;

use crate::{
    evaluation::{
        dynamic_returnable::DynamicReturnable, dynamic_string::DynamicString,
        evaluator_value::EvaluatorValue,
    },
    interned_str,
    interned_string::InternedString,
    interned_values::InternedStore,
    log_error_to_statsig_and_console,
    networking::ResponseData,
    observability::{ops_stats::OpsStatsForInstance, sdk_errors_observer::ErrorBoundaryEvent},
    specs_response::{
        explicit_params::ExplicitParameters,
        param_store_types::ParameterStore,
        proto_stream_reader::ProtoStreamReader,
        spec_types::{
            Condition, ConditionOperator, ConditionType, Rule, Spec, SpecsResponseFull,
            SpecsResponsePartial,
        },
        specs_hash_map::{SpecPointer, SpecsHashMap},
        statsig_config_specs::{self as pb, any_value},
    },
    StatsigErr,
};

const TAG: &str = "ProtoSpecs";

#[derive(Debug, PartialEq, Eq)]
pub(crate) enum ProtobufUpdate {
    Materialized { is_delta: bool },
    CursorOnly { lcut: u64, checksum: String },
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum ParseState {
    Initial,
    Full,
    DeltaAwaitingTopLevel,
    DeltaDeferred,
    DeltaMaterialized,
    DeltaDeferredValidated,
    DeltaMaterializedValidated,
}

impl ParseState {
    fn is_delta(self) -> bool {
        !matches!(self, Self::Initial | Self::Full)
    }

    fn materialize(
        &mut self,
        current_specs: &SpecsResponseFull,
        next_specs: &mut SpecsResponseFull,
    ) {
        if *self == Self::DeltaDeferred {
            next_specs.copy_previous_values_from(current_specs);
            *self = Self::DeltaMaterialized;
        }
    }
}

pub fn deserialize_protobuf(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull, /* Intentionally immutable so we can continue using it if parsing fails */
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
) -> Result<(), StatsigErr> {
    if matches!(
        deserialize_protobuf_for_store(ops_stats, current_specs, next_specs, data)?,
        ProtobufUpdate::CursorOnly { .. }
    ) {
        next_specs.copy_previous_values_from(current_specs);
    }

    Ok(())
}

pub(crate) fn deserialize_protobuf_for_store(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull, /* Intentionally immutable so we can continue using it if parsing fails */
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
) -> Result<ProtobufUpdate, StatsigErr> {
    let mut parsed_envelopes_count = 0;
    let mut state = ParseState::Initial;

    let mut reader = ProtoStreamReader::new(data);

    if !next_specs.is_empty() {
        // We just verify, rather than doing the reset here. The SpecStore is responsible for resetting the next_specs.
        return Err(StatsigErr::ProtobufParseError(
            "SpecsResponseFull".to_string(),
            "Next specs are not empty".to_string(),
        ));
    }

    loop {
        let proto_msg_bytes = reader.read_next_delimited_proto().map_err(|e| {
            let sample = reader.sample_current_buf();
            let err = StatsigErr::ProtobufParseError(
                "SpecsEnvelope".to_string(),
                format!(
                    "Error reading next delimited proto: {e}
                    \n Previous Parsed Envelope Count: {parsed_envelopes_count}
                    \n Current Buffer Sample: {sample}"
                ),
            );
            log_error_to_statsig_and_console!(ops_stats, TAG, err);
            err
        })?;

        parsed_envelopes_count += 1;

        let env: pb::SpecsEnvelope =
            match prost::Message::decode_length_delimited(proto_msg_bytes.as_ref()) {
                Ok(env) => env,
                Err(e) => {
                    let err: StatsigErr = map_decode_err("SpecsEnvelope", e);
                    log_error_to_statsig_and_console!(ops_stats, TAG, err);
                    if state.is_delta() {
                        return Err(err);
                    }
                    continue;
                }
            };

        let envelope_kind = match pb::SpecsEnvelopeKind::try_from(env.kind) {
            Ok(kind) => kind,
            Err(e) => {
                let err: StatsigErr = map_unknown_enum_value("SpecsEnvelopeKind", e);
                log_error_to_statsig_and_console!(ops_stats, TAG, err);
                if state.is_delta() {
                    return Err(err);
                }
                continue;
            }
        };

        match envelope_kind {
            pb::SpecsEnvelopeKind::Done => match state {
                ParseState::Full => return Ok(ProtobufUpdate::Materialized { is_delta: false }),
                ParseState::DeltaMaterializedValidated => {
                    return Ok(ProtobufUpdate::Materialized { is_delta: true })
                }
                ParseState::DeltaDeferredValidated => {
                    if next_specs.has_same_semantic_values_as(current_specs) && next_specs.time > 0
                    {
                        if let Some(checksum) = next_specs
                            .checksum
                            .as_ref()
                            .filter(|checksum| !checksum.is_empty())
                        {
                            return Ok(ProtobufUpdate::CursorOnly {
                                lcut: next_specs.time,
                                checksum: checksum.clone(),
                            });
                        }
                    }

                    next_specs.copy_previous_values_from(current_specs);
                    return Ok(ProtobufUpdate::Materialized { is_delta: true });
                }
                ParseState::Initial | ParseState::DeltaAwaitingTopLevel => {
                    return make_proto_parse_error("SpecsEnvelope", "Missing top-level envelope")
                }
                ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Missing checksums envelope for delta response",
                    )
                }
            },
            pb::SpecsEnvelopeKind::TopLevel => match state {
                ParseState::Initial | ParseState::Full => {
                    if log_parse_result(ops_stats, next_specs.handle_top_level_update(env)).is_ok()
                    {
                        state = ParseState::Full;
                    }
                }
                ParseState::DeltaAwaitingTopLevel => {
                    log_parse_result(ops_stats, next_specs.handle_top_level_update(env))?;
                    state = ParseState::DeltaDeferred;
                }
                _ => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Unexpected top-level envelope in delta response",
                    )
                }
            },
            kind @ (pb::SpecsEnvelopeKind::FeatureGate
            | pb::SpecsEnvelopeKind::DynamicConfig
            | pb::SpecsEnvelopeKind::LayerConfig
            | pb::SpecsEnvelopeKind::ParamStore
            | pb::SpecsEnvelopeKind::Condition) => match state {
                ParseState::Full => {
                    let _ = log_parse_result(
                        ops_stats,
                        apply_entity_update(kind, env, current_specs, next_specs),
                    );
                }
                ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
                    state.materialize(current_specs, next_specs);
                    log_parse_result(
                        ops_stats,
                        apply_entity_update(kind, env, current_specs, next_specs),
                    )?;
                }
                ParseState::Initial | ParseState::DeltaAwaitingTopLevel => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Entity envelope before top-level envelope",
                    )
                }
                ParseState::DeltaDeferredValidated | ParseState::DeltaMaterializedValidated => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Unexpected entity envelope after delta checksums",
                    )
                }
            },
            pb::SpecsEnvelopeKind::Deletions => match state {
                ParseState::Full => {
                    if let Ok(deletions) = log_parse_result(ops_stats, decode_deletions_update(env))
                    {
                        next_specs.apply_deletions(deletions);
                    }
                }
                ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
                    let deletions = log_parse_result(ops_stats, decode_deletions_update(env))?;
                    if !deletions_are_empty(&deletions) {
                        state.materialize(current_specs, next_specs);
                        next_specs.apply_deletions(deletions);
                    }
                }
                _ => {
                    return make_proto_parse_error("SpecsEnvelope", "Unexpected deletions envelope")
                }
            },
            pb::SpecsEnvelopeKind::Checksums => {
                let (target, next_state): (&SpecsResponseFull, ParseState) = match state {
                    ParseState::Full => (next_specs, ParseState::Full),
                    ParseState::DeltaDeferred => {
                        (current_specs, ParseState::DeltaDeferredValidated)
                    }
                    ParseState::DeltaMaterialized => {
                        (next_specs, ParseState::DeltaMaterializedValidated)
                    }
                    _ => {
                        return make_proto_parse_error(
                            "SpecsEnvelope",
                            "Unexpected checksums envelope",
                        )
                    }
                };

                match target.handle_checksums_update(env) {
                    Ok(()) => {
                        state = next_state;
                        ops_stats.log_checksum_validation_result(true);
                    }
                    Err(e) => {
                        ops_stats.log_checksum_validation_result(false);
                        return Err(StatsigErr::ChecksumFailure(format!(
                            "Failed to apply protobuf checksums update: {e}"
                        )));
                    }
                }
            }
            pb::SpecsEnvelopeKind::CopyPrev => {
                if state != ParseState::Initial || parsed_envelopes_count != 1 {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Duplicate or misplaced copy-prev envelope",
                    );
                }
                state = ParseState::DeltaAwaitingTopLevel;
            }
            pb::SpecsEnvelopeKind::Unknown => {
                return make_proto_parse_error("SpecsEnvelope", "Unknown envelope kind");
            }
        };
    }
}

fn apply_entity_update(
    kind: pb::SpecsEnvelopeKind,
    envelope: pb::SpecsEnvelope,
    current_specs: &SpecsResponseFull,
    next_specs: &mut SpecsResponseFull,
) -> Result<(), StatsigErr> {
    match kind {
        pb::SpecsEnvelopeKind::FeatureGate => {
            next_specs.handle_feature_gate_update(envelope, current_specs)
        }
        pb::SpecsEnvelopeKind::DynamicConfig => {
            next_specs.handle_dynamic_config_update(envelope, current_specs)
        }
        pb::SpecsEnvelopeKind::LayerConfig => {
            next_specs.handle_layer_config_update(envelope, current_specs)
        }
        pb::SpecsEnvelopeKind::ParamStore => {
            next_specs.handle_param_store_update(envelope, current_specs)
        }
        pb::SpecsEnvelopeKind::Condition => {
            next_specs.handle_condition_update(envelope, current_specs)
        }
        _ => unreachable!(),
    }
}

fn log_parse_result<T>(
    ops_stats: &OpsStatsForInstance,
    result: Result<T, StatsigErr>,
) -> Result<T, StatsigErr> {
    if let Err(error) = &result {
        log_error_to_statsig_and_console!(ops_stats, TAG, error);
    }

    result
}

impl SpecsResponseFull {
    fn handle_top_level_update(&mut self, envelope: pb::SpecsEnvelope) -> Result<(), StatsigErr> {
        let envelope_data = validate_envelope_data("TopLevel", envelope.data)?;
        let top_level = pb::SpecsTopLevel::decode(envelope_data)
            .map_err(|e| map_decode_err("SpecsTopLevel", e))?;

        self.populate_top_level_from_envelope(top_level)?;

        Ok(())
    }

    fn handle_feature_gate_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
    ) -> Result<(), StatsigErr> {
        Self::handle_individual_spec_update(
            "FeatureGate",
            envelope,
            &existing.feature_gates,
            &mut self.feature_gates,
            InternedStore::try_get_preloaded_feature_gate,
        )
    }

    fn handle_dynamic_config_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
    ) -> Result<(), StatsigErr> {
        Self::handle_individual_spec_update(
            "DynamicConfig",
            envelope,
            &existing.dynamic_configs,
            &mut self.dynamic_configs,
            InternedStore::try_get_preloaded_dynamic_config,
        )
    }

    fn handle_layer_config_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
    ) -> Result<(), StatsigErr> {
        Self::handle_individual_spec_update(
            "LayerConfig",
            envelope,
            &existing.layer_configs,
            &mut self.layer_configs,
            InternedStore::try_get_preloaded_layer_config,
        )
    }

    fn handle_individual_spec_update(
        tag: &str,
        envelope: pb::SpecsEnvelope,
        exiting_map: &SpecsHashMap,
        new_map: &mut SpecsHashMap,
        preload_fetcher: fn(&InternedString) -> Option<SpecPointer>,
    ) -> Result<(), StatsigErr> {
        let name = InternedString::from_string(envelope.name);

        if let Some(spec) = preload_fetcher(&name) {
            if spec.as_spec_ref().checksum.as_deref() == Some(&envelope.checksum) {
                new_map.insert(name, spec);
                return Ok(());
            }
        }

        if let Some(spec_ptr) = exiting_map.get(&name) {
            if spec_ptr.as_spec_ref().checksum.as_deref() == Some(&envelope.checksum) {
                new_map.insert(name, spec_ptr.clone());
                return Ok(());
            }
        }

        let envelope_data = validate_envelope_data(tag, envelope.data)?;
        let pb_spec = pb::Spec::decode(envelope_data).map_err(|e| map_decode_err(tag, e))?;
        let spec = spec_from_pb(envelope.checksum, pb_spec)?;
        new_map.insert(name, SpecPointer::from_spec(spec));

        Ok(())
    }

    fn populate_top_level_from_envelope(
        &mut self,
        top_level: pb::SpecsTopLevel,
    ) -> Result<(), StatsigErr> {
        let partial = serde_json::from_slice::<SpecsResponsePartial>(&top_level.rest)
            .map_err(|e| map_serde_json_err("SpecsResponsePartial", e))?;

        self.merge_from_partial(partial);

        self.checksum = Some(top_level.checksum);
        self.time = top_level.time;
        self.has_updates = top_level.has_updates;
        self.response_format = Some(top_level.response_format);
        self.company_id = Some(top_level.company_id);

        Ok(())
    }

    fn handle_param_store_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
    ) -> Result<(), StatsigErr> {
        let name = InternedString::from_string(envelope.name);

        let existing_param_store = existing
            .param_stores
            .as_ref()
            .and_then(|param_stores| param_stores.get(&name));

        if let Some(param_store) = existing_param_store {
            if param_store.checksum.as_deref() == Some(&envelope.checksum) {
                self.param_stores
                    .get_or_insert_with(HashMap::default)
                    .insert(name, param_store.clone());
                return Ok(());
            }
        }

        let envelope_data = validate_envelope_data("ParamStore", envelope.data)?;

        let mut param_store = serde_json::from_slice::<ParameterStore>(envelope_data.get_ref())
            .map_err(|e| map_serde_json_err("ParameterStore", e))?;

        param_store.checksum = Some(InternedString::from_string(envelope.checksum));

        self.param_stores
            .get_or_insert_with(HashMap::default)
            .insert(name, param_store);
        Ok(())
    }

    fn handle_condition_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
    ) -> Result<(), StatsigErr> {
        let name = InternedString::from_string(envelope.name);

        if let Some(condition) = existing.condition_map.get(&name) {
            if condition.checksum.as_deref() == Some(&envelope.checksum) {
                self.condition_map.insert(name, condition.clone());
                return Ok(());
            }
        }

        let envelope_data = validate_envelope_data("Condition", envelope.data)?;
        let pb_condition =
            pb::Condition::decode(envelope_data).map_err(|e| map_decode_err("Condition", e))?;
        let mut condition = condition_from_pb(pb_condition)?;
        condition.checksum = Some(InternedString::from_string(envelope.checksum));
        self.condition_map.insert(name, condition);

        Ok(())
    }

    fn handle_checksums_update(&self, envelope: pb::SpecsEnvelope) -> Result<(), StatsigErr> {
        let envelope_data = validate_envelope_data("Checksums", envelope.data)?;
        let checksums = pb::RulesetsChecksums::decode(envelope_data)
            .map_err(|e| map_decode_err("RulesetsChecksums", e))?;
        let field_checksums = &checksums.field_checksums;

        let condition_map = sum_checksums(self.condition_map.values().map(checksum_for_condition));
        let dynamic_configs = sum_checksums(self.dynamic_configs.0.values().map(checksum_for_spec));
        let feature_gates = sum_checksums(self.feature_gates.0.values().map(checksum_for_spec));
        let layer_configs = sum_checksums(self.layer_configs.0.values().map(checksum_for_spec));
        let param_stores = sum_checksums(
            self.param_stores
                .as_ref()
                .map(|stores| stores.values().map(checksum_for_param_store))
                .into_iter()
                .flatten(),
        );

        validate_field_checksum("condition_map", field_checksums, condition_map)?;
        validate_field_checksum("dynamic_configs", field_checksums, dynamic_configs)?;
        validate_field_checksum("feature_gates", field_checksums, feature_gates)?;
        validate_field_checksum("layer_configs", field_checksums, layer_configs)?;
        validate_field_checksum("param_stores", field_checksums, param_stores)?;

        Ok(())
    }

    fn has_same_semantic_values_as(&self, existing: &SpecsResponseFull) -> bool {
        self.common_fields_match(existing)
            && self.company_id == existing.company_id
            && self.response_format == existing.response_format
    }

    fn copy_previous_values_from(&mut self, existing: &SpecsResponseFull) {
        self.dynamic_configs = SpecsHashMap(existing.dynamic_configs.0.clone());
        self.feature_gates = SpecsHashMap(existing.feature_gates.0.clone());
        self.layer_configs = SpecsHashMap(existing.layer_configs.0.clone());
        self.condition_map = existing.condition_map.clone();
        self.param_stores = existing.param_stores.clone();
    }

    fn apply_deletions(&mut self, deletions: pb::RulesetsResponseDeletions) {
        let pb::RulesetsResponseDeletions {
            dynamic_configs,
            feature_gates,
            layer_configs,
            experiment_to_layer,
            condition_map,
            sdk_configs,
            param_stores,
            cmab_configs,
            override_rules,
            overrides,
        } = deletions;

        remove_interned_from_specs_map(&mut self.dynamic_configs, dynamic_configs);
        remove_interned_from_specs_map(&mut self.feature_gates, feature_gates);
        remove_interned_from_specs_map(&mut self.layer_configs, layer_configs);
        remove_string_from_map(&mut self.experiment_to_layer, experiment_to_layer);
        remove_interned_from_hash(&mut self.condition_map, condition_map);
        remove_string_from_opt_map(&mut self.sdk_configs, sdk_configs);
        remove_interned_from_opt_map(&mut self.param_stores, param_stores);
        remove_string_from_opt_map(&mut self.cmab_configs, cmab_configs);
        remove_string_from_opt_map(&mut self.override_rules, override_rules);
        remove_string_from_opt_map(&mut self.overrides, overrides);
    }
}

fn decode_deletions_update(
    envelope: pb::SpecsEnvelope,
) -> Result<pb::RulesetsResponseDeletions, StatsigErr> {
    let envelope_data = validate_envelope_data("Deletions", envelope.data)?;
    pb::RulesetsResponseDeletions::decode(envelope_data)
        .map_err(|e| map_decode_err("RulesetsResponseDeletions", e))
}

fn deletions_are_empty(deletions: &pb::RulesetsResponseDeletions) -> bool {
    deletions.dynamic_configs.is_empty()
        && deletions.feature_gates.is_empty()
        && deletions.layer_configs.is_empty()
        && deletions.experiment_to_layer.is_empty()
        && deletions.condition_map.is_empty()
        && deletions.sdk_configs.is_empty()
        && deletions.param_stores.is_empty()
        && deletions.cmab_configs.is_empty()
        && deletions.override_rules.is_empty()
        && deletions.overrides.is_empty()
}

fn remove_interned_from_specs_map(map: &mut SpecsHashMap, names: Vec<String>) {
    for name in names {
        map.remove(&InternedString::from_string(name));
    }
}

fn remove_interned_from_hash<V, S: std::hash::BuildHasher>(
    map: &mut HashMap<InternedString, V, S>,
    names: Vec<String>,
) {
    for name in names {
        map.remove(&InternedString::from_string(name));
    }
}

fn remove_string_from_map<V>(map: &mut HashMap<String, V>, names: Vec<String>) {
    for name in names {
        map.remove(&name);
    }
}

fn remove_interned_from_opt_map<V>(
    map: &mut Option<HashMap<InternedString, V>>,
    names: Vec<String>,
) {
    let Some(map) = map.as_mut() else {
        return;
    };
    remove_interned_from_hash(map, names)
}

fn remove_string_from_opt_map<V>(map: &mut Option<HashMap<String, V>>, names: Vec<String>) {
    let Some(map) = map.as_mut() else {
        return;
    };
    remove_string_from_map(map, names);
}

fn validate_field_checksum(
    field: &str,
    field_checksums: &HashMap<String, u64>,
    computed: u64,
) -> Result<(), StatsigErr> {
    let Some(expected) = field_checksums.get(field) else {
        return Err(StatsigErr::ProtobufParseError(
            "proto::RulesetsChecksums".to_string(),
            format!("Missing checksum for {field}"),
        ));
    };

    if *expected != computed {
        return Err(StatsigErr::ProtobufParseError(
            "proto::RulesetsChecksums".to_string(),
            format!("Checksum mismatch for {field}: expected {expected}, got {computed}"),
        ));
    }

    Ok(())
}

fn sum_checksums(checksums: impl Iterator<Item = Option<u32>>) -> u64 {
    checksums.fold(0u64, |acc, checksum| {
        acc.wrapping_add(checksum.unwrap_or_default() as u64)
    })
}

fn checksum_for_condition(condition: &Condition) -> Option<u32> {
    checksum_to_u32(condition.checksum.as_ref())
}

fn checksum_for_spec(pointer: &SpecPointer) -> Option<u32> {
    let spec: &Spec = pointer.as_spec_ref();
    checksum_to_u32(spec.checksum.as_ref())
}

fn checksum_for_param_store(store: &ParameterStore) -> Option<u32> {
    checksum_to_u32(store.checksum.as_ref())
}

fn checksum_to_u32(checksum: Option<&InternedString>) -> Option<u32> {
    let value = checksum?.as_str();
    value.parse::<u32>().ok()
}

fn validate_envelope_data(
    envelope_tag: &str,
    data: Option<Vec<u8>>,
) -> Result<Cursor<Vec<u8>>, StatsigErr> {
    match data {
        Some(data) => Ok(Cursor::new(data)),
        None => Err(StatsigErr::ProtobufParseError(
            "SpecsEnvelope".to_string(),
            format!("No data in {} envelope", envelope_tag),
        )),
    }
}

fn condition_from_pb(v: pb::Condition) -> Result<Condition, StatsigErr> {
    let condition_type = condition_type_from_pb(
        pb::ConditionType::try_from(v.condition_type)
            .map_err(|e| map_unknown_enum_value("ConditionType", e))?,
    )?;
    let operator = match v.operator {
        Some(operator) => Some(operator_from_pb(
            pb::Operator::try_from(operator).map_err(|e| map_unknown_enum_value("Operator", e))?,
        )?),
        None => None,
    };
    let mut condition = Condition {
        compiled_condition_type: ConditionType::from_str(condition_type.as_str()),
        condition_type,
        target_value: target_value_from_pb(v.target_value)?,
        compiled_operator: ConditionOperator::from_str(operator.as_deref()),
        operator,
        field: v.field.map(DynamicString::from),
        additional_values: additional_values_from_pb(v.additional_values)?,
        id_type: id_type_from_pb_to_dynamic_string(v.id_type)?,
        checksum: None,
    };

    if condition.operator.as_deref() == Some("str_matches") {
        if let Some(ref mut target_value) = condition.target_value {
            target_value.compile_regex();
        }
    }

    Ok(condition)
}

fn additional_values_from_pb(
    additional_values: Option<Vec<u8>>,
) -> Result<Option<HashMap<InternedString, InternedString>>, StatsigErr> {
    let additional_values = match additional_values {
        Some(additional_values) => additional_values,
        None => return Ok(None),
    };

    let map = serde_json::from_slice(&additional_values)
        .map_err(|e| map_serde_json_err("AdditionalValues", e))?;
    Ok(Some(map))
}

fn any_value_to_json_value(
    any_value: Option<pb::AnyValue>,
) -> Result<Option<serde_json::Value>, StatsigErr> {
    let value = match any_value.and_then(|v| v.value) {
        Some(value) => value,
        None => return Ok(None),
    };

    let json_value = match value {
        pb::any_value::Value::BoolValue(value) => serde_json::Value::Bool(value),
        pb::any_value::Value::RawValue(value) => {
            serde_json::from_slice(value.as_ref()).map_err(|e| map_serde_json_err("AnyValue", e))?
        }
        pb::any_value::Value::StringValue(value) => serde_json::Value::String(value),
        pb::any_value::Value::DoubleValue(value) => json!(value),
        pb::any_value::Value::Int64Value(value) => json!(value),
        pb::any_value::Value::Uint64Value(value) => json!(value),
    };

    Ok(Some(json_value))
}

fn target_value_from_pb(
    target_value: Option<pb::AnyValue>,
) -> Result<Option<EvaluatorValue>, StatsigErr> {
    if let Some(any_value) = &target_value {
        if let Some(any_value::Value::RawValue(raw_value)) = &any_value.value {
            if let Some(evaluator_value) =
                InternedStore::try_get_preloaded_evaluator_value(raw_value.as_ref())
            {
                return Ok(Some(evaluator_value));
            }
        }
    }

    match any_value_to_json_value(target_value)? {
        Some(json_value) => {
            let evaluator_value = EvaluatorValue::from_json_value(json_value);
            Ok(Some(evaluator_value))
        }
        None => Ok(None),
    }
}

fn operator_from_pb(operator: pb::Operator) -> Result<InternedString, StatsigErr> {
    match operator {
        pb::Operator::Unknown => Err(StatsigErr::ProtobufParseError(
            "proto::Operator".to_string(),
            "Unknown operator".to_string(),
        )),

        // strict equals
        pb::Operator::Eq => Ok(interned_str!("eq")),
        pb::Operator::Neq => Ok(interned_str!("neq")),

        // numerical comparisons
        pb::Operator::Gt => Ok(interned_str!("gt")),
        pb::Operator::Gte => Ok(interned_str!("gte")),
        pb::Operator::Lte => Ok(interned_str!("lte")),
        pb::Operator::Lt => Ok(interned_str!("lt")),

        // string/array comparisons
        pb::Operator::Any => Ok(interned_str!("any")),
        pb::Operator::None => Ok(interned_str!("none")),
        pb::Operator::StrStartsWithAny => Ok(interned_str!("str_starts_with_any")),
        pb::Operator::StrEndsWithAny => Ok(interned_str!("str_ends_with_any")),
        pb::Operator::StrContainsAny => Ok(interned_str!("str_contains_any")),
        pb::Operator::StrContainsNone => Ok(interned_str!("str_contains_none")),
        pb::Operator::StrMatches => Ok(interned_str!("str_matches")),
        pb::Operator::AnyCaseSensitive => Ok(interned_str!("any_case_sensitive")),
        pb::Operator::NoneCaseSensitive => Ok(interned_str!("none_case_sensitive")),

        // time comparisions
        pb::Operator::Before => Ok(interned_str!("before")),
        pb::Operator::After => Ok(interned_str!("after")),
        pb::Operator::On => Ok(interned_str!("on")),

        // id_lists
        pb::Operator::InSegmentList => Ok(interned_str!("in_segment_list")),
        pb::Operator::NotInSegmentList => Ok(interned_str!("not_in_segment_list")),

        // array comparisons
        pb::Operator::ArrayContainsAny => Ok(interned_str!("array_contains_any")),
        pb::Operator::ArrayContainsNone => Ok(interned_str!("array_contains_none")),
        pb::Operator::ArrayContainsAll => Ok(interned_str!("array_contains_all")),
        pb::Operator::NotArrayContainsAll => Ok(interned_str!("not_array_contains_all")),

        // version comparisons
        pb::Operator::VersionGt => Ok(interned_str!("version_gt")),
        pb::Operator::VersionGte => Ok(interned_str!("version_gte")),
        pb::Operator::VersionLt => Ok(interned_str!("version_lt")),
        pb::Operator::VersionLte => Ok(interned_str!("version_lte")),
        pb::Operator::VersionEq => Ok(interned_str!("version_eq")),
        pb::Operator::VersionNeq => Ok(interned_str!("version_neq")),

        // encoded any
        pb::Operator::EncodedAny => Ok(interned_str!("encoded_any")),
    }
}

fn condition_type_from_pb(condition_type: pb::ConditionType) -> Result<InternedString, StatsigErr> {
    match condition_type {
        pb::ConditionType::Unknown => Err(StatsigErr::ProtobufParseError(
            "proto::ConditionType".to_string(),
            "Unknown condition type".to_string(),
        )),

        pb::ConditionType::CurrentTime => Ok(interned_str!("current_time")),
        pb::ConditionType::Public => Ok(interned_str!("public")),
        pb::ConditionType::FailGate => Ok(interned_str!("fail_gate")),
        pb::ConditionType::PassGate => Ok(interned_str!("pass_gate")),
        pb::ConditionType::UaBased => Ok(interned_str!("ua_based")),
        pb::ConditionType::IpBased => Ok(interned_str!("ip_based")),
        pb::ConditionType::UserField => Ok(interned_str!("user_field")),
        pb::ConditionType::EnvironmentField => Ok(interned_str!("environment_field")),
        pb::ConditionType::UserBucket => Ok(interned_str!("user_bucket")),
        pb::ConditionType::TargetApp => Ok(interned_str!("target_app")),
        pb::ConditionType::UnitId => Ok(interned_str!("unit_id")),
    }
}

fn spec_from_pb(checksum: String, spec: pb::Spec) -> Result<Spec, StatsigErr> {
    let checksum = InternedString::from_string(checksum);
    let entity_type = pb::EntityType::try_from(spec.entity)
        .map_err(|e| map_unknown_enum_value("EntityType", e))?;

    let _type = entity_type.to_legacy_type();

    let mut target_app_ids: Option<Vec<InternedString>> = None;
    if !spec.target_app_ids.is_empty() {
        target_app_ids = Some(
            spec.target_app_ids
                .into_iter()
                .map(InternedString::from_string)
                .collect(),
        );
    }

    let mut fields_used: Option<Vec<InternedString>> = None;
    if !spec.fields_used.is_empty() {
        fields_used = Some(
            spec.fields_used
                .into_iter()
                .map(InternedString::from_string)
                .collect(),
        );
    }

    let spec = Spec {
        checksum: Some(checksum),
        _type,
        salt: InternedString::from_string(spec.salt),
        enabled: spec.enabled,
        rules: rules_from_pb(spec.rules)?,
        id_type: id_type_from_pb(spec.id_type)?,
        explicit_parameters: match spec.explicit_parameters.is_empty() {
            true => None,
            false => Some(ExplicitParameters::from_vec(spec.explicit_parameters)),
        },
        entity: entity_type.to_string_type()?,
        has_shared_params: spec.has_shared_params,
        is_active: spec.is_active,
        version: Some(spec.version),
        target_app_ids,
        forward_all_exposures: spec.forward_all_exposures,
        fields_used,
        default_value: return_value_from_pb(spec.default_value)?,
        use_new_layer_eval: spec.use_new_layer_eval,
    };

    Ok(spec)
}

fn rules_from_pb(rules: Vec<pb::Rule>) -> Result<Vec<Rule>, StatsigErr> {
    rules
        .into_iter()
        .map(|pb_rule| {
            let rule = Rule {
                name: InternedString::from_string(pb_rule.name),
                pass_percentage: pb_rule
                    .pass_percentage_float
                    .unwrap_or(pb_rule.pass_percentage as f64),
                id: InternedString::from_string(pb_rule.id),
                salt: pb_rule.salt.map(InternedString::from_string),
                conditions: pb_rule
                    .conditions
                    .into_iter()
                    .map(InternedString::from_string)
                    .collect(),
                id_type: id_type_from_pb_to_dynamic_string(pb_rule.id_type)?,

                group_name: pb_rule.group_name.map(InternedString::from_string),

                config_delegate: pb_rule.config_delegate.map(InternedString::from_string),

                is_experiment_group: pb_rule.is_experiment_group,

                sampling_rate: sampling_rate_from_pb(pb_rule.sampling_rate)?,
                return_value: return_value_from_pb(pb_rule.return_value)?,
            };

            Ok(rule)
        })
        .collect::<Result<Vec<Rule>, StatsigErr>>()
}

fn sampling_rate_from_pb(sampling_rate: Option<f32>) -> Result<Option<u64>, StatsigErr> {
    let Some(sampling_rate) = sampling_rate else {
        return Ok(None);
    };

    if !sampling_rate.is_finite() || sampling_rate < 0.0 || sampling_rate.fract() != 0.0 {
        return Err(StatsigErr::ProtobufParseError(
            "proto::Rule".to_string(),
            format!(
                "Expected sampling rate to be a non-negative whole number, got {sampling_rate}"
            ),
        ));
    }

    Ok(Some(sampling_rate as u64))
}

fn return_value_from_pb(
    return_value: Option<pb::ReturnValue>,
) -> Result<DynamicReturnable, StatsigErr> {
    let return_value = match return_value {
        Some(return_value) => return_value,
        None => return Ok(DynamicReturnable::empty()),
    };

    let return_value = match return_value.value {
        Some(return_value) => return_value,
        None => {
            return Err(StatsigErr::ProtobufParseError(
                "proto::ReturnValue".to_string(),
                "No return value".to_string(),
            ))
        }
    };

    let bytes = match return_value {
        pb::return_value::Value::BoolValue(value) => {
            return Ok(DynamicReturnable::from_bool(value))
        }
        pb::return_value::Value::RawValue(value) => value,
    };

    if let Some(returnable) = InternedStore::try_get_preloaded_returnable(bytes.as_ref()) {
        return Ok(returnable);
    }

    serde_json::from_slice(bytes.as_ref()).map_err(|e| map_serde_json_err("ReturnValue", e))
}

fn id_type_from_pb_to_dynamic_string(
    id_type: Option<pb::IdType>,
) -> Result<DynamicString, StatsigErr> {
    let id_type = match id_type.and_then(|i| i.id_type) {
        Some(id_type) => id_type,
        None => {
            return Ok(DynamicString {
                value: InternedString::empty(),
                lowercased_value: InternedString::empty(),
                hash_value: 0,
            })
        }
    };

    match id_type {
        pb::id_type::IdType::KnownIdType(id_type) => match pb::KnownIdType::try_from(id_type) {
            Ok(pb::KnownIdType::UserId) => Ok(DynamicString::from("userID".to_string())),
            Ok(pb::KnownIdType::StableId) => Ok(DynamicString::from("stableID".to_string())),
            Ok(pb::KnownIdType::Unknown) => Err(StatsigErr::ProtobufParseError(
                "proto::KnownIdType".to_string(),
                "Expected ID type to be known".to_string(),
            )),
            Err(e) => Err(map_unknown_enum_value("KnownIdType", e)),
        },
        pb::id_type::IdType::CustomIdType(id_type) => Ok(DynamicString::from(id_type)),
    }
}

fn id_type_from_pb(id_type: Option<pb::IdType>) -> Result<InternedString, StatsigErr> {
    let id_type = match id_type.and_then(|i| i.id_type) {
        Some(id_type) => id_type,
        None => return Ok(InternedString::empty()),
    };

    match id_type {
        pb::id_type::IdType::KnownIdType(id_type) => match pb::KnownIdType::try_from(id_type) {
            Ok(pb::KnownIdType::UserId) => Ok(interned_str!("userID")),
            Ok(pb::KnownIdType::StableId) => Ok(interned_str!("stableID")),
            Ok(pb::KnownIdType::Unknown) => Err(StatsigErr::ProtobufParseError(
                "proto::KnownIdType".to_string(),
                "Expected ID type to be known".to_string(),
            )),
            Err(e) => Err(map_unknown_enum_value("KnownIdType", e)),
        },
        pb::id_type::IdType::CustomIdType(id_type) => Ok(InternedString::from_string(id_type)),
    }
}

impl pb::EntityType {
    fn to_legacy_type(self) -> InternedString {
        if self == pb::EntityType::EntityFeatureGate
            || self == pb::EntityType::EntityHoldout
            || self == pb::EntityType::EntitySegment
        {
            return interned_str!("feature_gate");
        }

        if self == pb::EntityType::EntityDynamicConfig
            || self == pb::EntityType::EntityAutotune
            || self == pb::EntityType::EntityExperiment
            || self == pb::EntityType::EntityLayer
        {
            interned_str!("dynamic_config")
        } else {
            interned_str!("unknown")
        }
    }

    fn to_string_type(self) -> Result<InternedString, StatsigErr> {
        match self {
            pb::EntityType::EntityFeatureGate => Ok(interned_str!("feature_gate")),
            pb::EntityType::EntityDynamicConfig => Ok(interned_str!("dynamic_config")),
            pb::EntityType::EntityAutotune => Ok(interned_str!("autotune")),
            pb::EntityType::EntityExperiment => Ok(interned_str!("experiment")),
            pb::EntityType::EntityLayer => Ok(interned_str!("layer")),
            pb::EntityType::EntitySegment => Ok(interned_str!("segment")),
            pb::EntityType::EntityHoldout => Ok(interned_str!("holdout")),
            pb::EntityType::EntityUnknown => Err(StatsigErr::ProtobufParseError(
                "proto::EntityType".to_string(),
                "Expected entity type to be known".to_string(),
            )),
        }
    }
}

fn map_decode_err(tag: &str, e: prost::DecodeError) -> StatsigErr {
    StatsigErr::ProtobufParseError(format!("proto::{}", tag), e.to_string())
}

fn map_unknown_enum_value(tag: &str, value: prost::UnknownEnumValue) -> StatsigErr {
    StatsigErr::ProtobufParseError(
        format!("proto::{}", tag),
        format!("Unknown enum value: {}", value),
    )
}

fn map_serde_json_err(tag: &str, e: serde_json::Error) -> StatsigErr {
    StatsigErr::ProtobufParseError(format!("proto::{}", tag), e.to_string())
}

fn make_proto_parse_error<T>(tag: &str, message: &str) -> Result<T, StatsigErr> {
    Err(StatsigErr::ProtobufParseError(
        format!("proto::{}", tag),
        message.to_string(),
    ))
}

#[cfg(test)]
mod tests {
    use std::{collections::HashMap, io::Write};

    use brotli::enc::BrotliEncoderParams;
    use prost::Message;

    use super::{
        checksum_for_condition, checksum_for_param_store, checksum_for_spec, condition_from_pb,
        deserialize_protobuf, deserialize_protobuf_for_store, pb, rules_from_pb, sum_checksums,
        ProtobufUpdate, SpecsResponseFull,
    };
    use crate::{
        networking::ResponseData,
        observability::ops_stats::OpsStatsForInstance,
        specs_response::{
            proto_stream_reader::BUFFER_SIZE,
            spec_types::{ConditionOperator, ConditionType},
        },
    };

    fn checksum_only_delta(current: &SpecsResponseFull, lcut: u64, checksum: &str) -> ResponseData {
        let mut common_fields = serde_json::to_value(current).unwrap();
        let fields = common_fields.as_object_mut().unwrap();
        for field in [
            "checksum",
            "company_id",
            "condition_map",
            "dynamic_configs",
            "feature_gates",
            "has_updates",
            "layer_configs",
            "param_stores",
            "response_format",
            "time",
        ] {
            fields.remove(field);
        }

        let field_checksums = HashMap::from([
            (
                "condition_map".to_string(),
                sum_checksums(current.condition_map.values().map(checksum_for_condition)),
            ),
            (
                "dynamic_configs".to_string(),
                sum_checksums(current.dynamic_configs.0.values().map(checksum_for_spec)),
            ),
            (
                "feature_gates".to_string(),
                sum_checksums(current.feature_gates.0.values().map(checksum_for_spec)),
            ),
            (
                "layer_configs".to_string(),
                sum_checksums(current.layer_configs.0.values().map(checksum_for_spec)),
            ),
            (
                "param_stores".to_string(),
                sum_checksums(
                    current
                        .param_stores
                        .as_ref()
                        .map(|stores| stores.values().map(checksum_for_param_store))
                        .into_iter()
                        .flatten(),
                ),
            ),
        ]);
        let envelopes = [
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::TopLevel as i32,
                data: Some(
                    pb::SpecsTopLevel {
                        has_updates: true,
                        time: lcut,
                        company_id: current.company_id.clone().unwrap_or_default(),
                        response_format: current.response_format.clone().unwrap_or_default(),
                        checksum: checksum.to_string(),
                        rest: serde_json::to_vec(&common_fields).unwrap(),
                    }
                    .encode_to_vec(),
                ),
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Checksums as i32,
                data: Some(pb::RulesetsChecksums { field_checksums }.encode_to_vec()),
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Done as i32,
                ..pb::SpecsEnvelope::default()
            },
        ];

        let mut encoded = Vec::new();
        for envelope in envelopes {
            envelope.encode_length_delimited(&mut encoded).unwrap();
        }

        let mut compressed = Vec::new();
        {
            let mut writer = brotli::CompressorWriter::with_params(
                &mut compressed,
                BUFFER_SIZE,
                &BrotliEncoderParams::default(),
            );
            writer.write_all(&encoded).unwrap();
            writer.flush().unwrap();
        }
        ResponseData::from_bytes(compressed)
    }

    #[test]
    fn checksum_only_delta_defers_copy_prev_for_the_store() {
        let current: SpecsResponseFull =
            serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
        let next_lcut = current.time + 1;
        let mut data = checksum_only_delta(&current, next_lcut, "next-checksum");
        let mut next = SpecsResponseFull::default();

        let update = deserialize_protobuf_for_store(
            &OpsStatsForInstance::new(),
            &current,
            &mut next,
            &mut data,
        )
        .unwrap();

        assert_eq!(
            update,
            ProtobufUpdate::CursorOnly {
                lcut: next_lcut,
                checksum: "next-checksum".to_string(),
            }
        );
        assert!(next.feature_gates.is_empty());
        assert!(next.dynamic_configs.is_empty());
        assert!(next.condition_map.is_empty());
    }

    #[test]
    fn public_decoder_still_materializes_checksum_only_deltas() {
        let current: SpecsResponseFull =
            serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
        let next_lcut = current.time + 1;
        let mut data = checksum_only_delta(&current, next_lcut, "next-checksum");
        let mut next = SpecsResponseFull::default();

        deserialize_protobuf(&OpsStatsForInstance::new(), &current, &mut next, &mut data).unwrap();

        assert!(next.has_same_semantic_values_as(&current));
        assert_eq!(next.time, next_lcut);
        assert_eq!(next.checksum.as_deref(), Some("next-checksum"));
        assert_eq!(next.feature_gates, current.feature_gates);
        assert_eq!(next.dynamic_configs, current.dynamic_configs);
        assert_eq!(next.condition_map, current.condition_map);
    }

    #[test]
    fn rules_from_pb_preserves_sampling_rate() {
        let rules = rules_from_pb(vec![pb::Rule {
            name: "rule".to_string(),
            pass_percentage: 100,
            id: "rule-id".to_string(),
            salt: None,
            conditions: vec![],
            id_type: None,
            return_value: None,
            group_name: None,
            config_delegate: None,
            is_experiment_group: None,
            is_control_group: None,
            sampling_rate: Some(201.0),
            pass_percentage_float: None,
        }])
        .expect("protobuf rule should parse");

        assert_eq!(rules[0].sampling_rate, Some(201));
    }

    #[test]
    fn condition_from_pb_compiles_dispatch_tags() {
        let condition = condition_from_pb(pb::Condition {
            condition_type: pb::ConditionType::UserField as i32,
            operator: Some(pb::Operator::Any as i32),
            field: Some("email".to_string()),
            ..pb::Condition::default()
        })
        .expect("protobuf condition should parse");

        assert_eq!(condition.compiled_condition_type, ConditionType::UserField);
        assert_eq!(condition.compiled_operator, ConditionOperator::Any);
    }

    #[test]
    fn rules_from_pb_prefers_float_pass_percentage() {
        let rules = rules_from_pb(vec![pb::Rule {
            name: "rule".to_string(),
            pass_percentage: 0,
            id: "rule-id".to_string(),
            salt: None,
            conditions: vec![],
            id_type: None,
            return_value: None,
            group_name: None,
            config_delegate: None,
            is_experiment_group: None,
            is_control_group: None,
            sampling_rate: None,
            pass_percentage_float: Some(0.5),
        }])
        .expect("protobuf rule should parse");

        assert_eq!(rules[0].pass_percentage, 0.5);
    }

    #[test]
    fn rules_from_pb_respects_explicit_zero_float_pass_percentage() {
        let rules = rules_from_pb(vec![pb::Rule {
            name: "rule".to_string(),
            pass_percentage: 100,
            id: "rule-id".to_string(),
            salt: None,
            conditions: vec![],
            id_type: None,
            return_value: None,
            group_name: None,
            config_delegate: None,
            is_experiment_group: None,
            is_control_group: None,
            sampling_rate: None,
            pass_percentage_float: Some(0.0),
        }])
        .expect("protobuf rule should parse");

        assert_eq!(rules[0].pass_percentage, 0.0);
    }

    #[test]
    fn rules_from_pb_falls_back_to_legacy_pass_percentage() {
        let rules = rules_from_pb(vec![pb::Rule {
            name: "rule".to_string(),
            pass_percentage: 42,
            id: "rule-id".to_string(),
            salt: None,
            conditions: vec![],
            id_type: None,
            return_value: None,
            group_name: None,
            config_delegate: None,
            is_experiment_group: None,
            is_control_group: None,
            sampling_rate: None,
            pass_percentage_float: None,
        }])
        .expect("protobuf rule should parse");

        assert_eq!(rules[0].pass_percentage, 42.0);
    }
}
