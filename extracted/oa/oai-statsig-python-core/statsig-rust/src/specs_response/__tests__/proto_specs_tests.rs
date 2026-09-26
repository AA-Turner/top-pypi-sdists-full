use rusty_fork::rusty_fork_test;
use std::{
    collections::HashMap,
    io::{Read, Write},
    sync::Arc,
};

use brotli::enc::BrotliEncoderParams;
use prost::Message;

use super::{
    HydratedProtobufDataStoreCapture, ProtobufUpdate, SpecDecodeStats, SpecsFieldChecksums,
    SpecsResponseFull, apply_entity_update, checksum_for_condition, checksum_for_param_store,
    checksum_for_spec, condition_from_pb, deserialize_protobuf,
    deserialize_protobuf_for_store_with_options, deserialize_protobuf_from_reader,
    deserialize_protobuf_with_options, pb, rules_from_pb, spec_from_pb, sum_checksums,
    validate_envelope_data,
};
use crate::{
    StatsigErr,
    interned_string::InternedString,
    networking::ResponseData,
    observability::ops_stats::OpsStatsForInstance,
    specs_response::{
        parse_options::SpecsResponseParseOptions,
        proto_compression::ProtoCompression,
        proto_stream_reader::{BUFFER_SIZE, ProtoStreamReader},
        spec_types::{ConditionOperator, ConditionType},
        specs_hash_map::{SpecPointer, SpecsHashMap},
    },
};

#[test]
fn frozen_envelope_frame_survives_reader_refills() {
    let first = pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
        name: "first".to_string(),
        data: Some(vec![1; BUFFER_SIZE * 2]),
        ..Default::default()
    };
    let second = pb::SpecsEnvelope {
        name: "second".to_string(),
        data: Some(vec![2; BUFFER_SIZE * 4]),
        ..first.clone()
    };
    let mut data = compressed_response([first.clone(), second.clone()]);
    let mut reader = ProtoStreamReader::new_for_response(&mut data).unwrap();
    let raw_frame = reader.read_next_delimited_proto().unwrap().freeze();
    let decoded = pb::SpecsEnvelope::decode_length_delimited(raw_frame.clone()).unwrap();
    assert_eq!(decoded, first);

    let next_frame = reader.read_next_delimited_proto().unwrap().freeze();
    assert_eq!(
        pb::SpecsEnvelope::decode_length_delimited(next_frame).unwrap(),
        second
    );
    assert_eq!(raw_frame.as_ref(), first.encode_length_delimited_to_vec());
    assert_eq!(decoded.data, first.data);
}

#[test]
fn borrowed_envelope_data_preserves_decode_and_missing_data_errors() {
    let spec = pb::Spec {
        salt: "large-config".repeat(BUFFER_SIZE),
        ..Default::default()
    };
    let encoded = spec.encode_to_vec();
    let borrowed = validate_envelope_data("DynamicConfig", Some(encoded.as_slice())).unwrap();
    assert_eq!(borrowed.get_ref().as_ptr(), encoded.as_ptr());
    assert_eq!(pb::Spec::decode(borrowed).unwrap(), spec);
    assert_eq!(
        pb::Spec::decode(validate_envelope_data("DynamicConfig", Some(encoded)).unwrap()).unwrap(),
        spec
    );

    for error in [
        validate_envelope_data::<Vec<u8>>("DynamicConfig", None).unwrap_err(),
        validate_envelope_data::<&[u8]>("DynamicConfig", None).unwrap_err(),
    ] {
        assert!(matches!(error, StatsigErr::ProtobufParseError(tag, message)
            if tag == "SpecsEnvelope" && message == "No data in DynamicConfig envelope"));
    }

    let malformed = vec![0x0a, 0x02, b'x']; // Truncated length-delimited salt.
    let borrowed_error = pb::Spec::decode(
        validate_envelope_data("DynamicConfig", Some(malformed.as_slice())).unwrap(),
    )
    .unwrap_err();
    let owned_error =
        pb::Spec::decode(validate_envelope_data("DynamicConfig", Some(malformed)).unwrap())
            .unwrap_err();
    assert_eq!(borrowed_error, owned_error);
}

#[test]
fn hydrated_data_store_capture_preserves_zstd_compression() {
    let mut capture = HydratedProtobufDataStoreCapture::new(ProtoCompression::Zstd).unwrap();
    capture.mark_remote_metadata();
    capture.write_frame(b"hydrated-protobuf").unwrap();

    let compressed = capture.finish().unwrap().unwrap();
    let mut decoded = Vec::new();
    zstd::stream::Decoder::new(compressed.as_slice())
        .unwrap()
        .read_to_end(&mut decoded)
        .unwrap();

    assert_eq!(decoded, b"hydrated-protobuf");
}

async fn hydrated_store_update(
    current: &SpecsResponseFull,
    next: &mut SpecsResponseFull,
    data: &mut crate::networking::ResponseData,
) -> Result<ProtobufUpdate, StatsigErr> {
    hydrated_store_update_with_mode(current, next, data, false).await
}

async fn hydrated_store_update_with_mode(
    current: &SpecsResponseFull,
    next: &mut SpecsResponseFull,
    data: &mut crate::networking::ResponseData,
    preserve_session_update_mode: bool,
) -> Result<ProtobufUpdate, StatsigErr> {
    let ops_stats = Arc::new(OpsStatsForInstance::new());
    let hydrator = super::RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(crate::networking::NetworkClient::new(
            "secret-key",
            None,
            None,
        )),
        Arc::clone(&ops_stats),
    );
    super::deserialize_protobuf_for_store_with_hydration(
        &ops_stats,
        current,
        SpecDecodeStats::default(),
        next,
        data,
        super::ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
            mmap_project_id: super::MmapProjectId::for_sdk_key("parser-protocol-tests"),
            capture_hydrated_data_store_bytes: false,
            preserve_session_update_mode,
        },
    )
    .await
    .map(|(update, _, _)| update)
}

#[tokio::test]
async fn protobuf_parsers_tolerate_malformed_full_envelopes_but_reject_them_in_deltas() {
    for malformed_kind in [
        pb::SpecsEnvelopeKind::TopLevel as i32,
        pb::SpecsEnvelopeKind::DynamicConfig as i32,
        pb::SpecsEnvelopeKind::Deletions as i32,
        -1, // An unrecognized numeric kind is also tolerated only in full responses.
    ] {
        for is_delta in [false, true] {
            let mut envelopes = Vec::new();
            if is_delta {
                envelopes.push(pb::SpecsEnvelope {
                    kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
                    ..Default::default()
                });
            }
            envelopes.extend([
                pb::SpecsEnvelope {
                    kind: pb::SpecsEnvelopeKind::TopLevel as i32,
                    data: Some(
                        pb::SpecsTopLevel {
                            time: 1,
                            rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                            ..Default::default()
                        }
                        .encode_to_vec(),
                    ),
                    ..Default::default()
                },
                pb::SpecsEnvelope {
                    kind: malformed_kind,
                    ..Default::default()
                },
                entity_envelope(pb::SpecsEnvelopeKind::FeatureGate, "surviving-gate", 7),
                pb::SpecsEnvelope {
                    kind: pb::SpecsEnvelopeKind::Done as i32,
                    ..Default::default()
                },
            ]);
            let current = SpecsResponseFull::default();
            let mut sync_next = SpecsResponseFull::default();
            let mut async_next = SpecsResponseFull::default();
            let sync_result = deserialize_protobuf_for_store_with_options(
                &OpsStatsForInstance::new(),
                &current,
                SpecDecodeStats::default(),
                &SpecsFieldChecksums::default(),
                &mut sync_next,
                &mut compressed_response(envelopes.clone()),
                false,
            );
            let async_result = hydrated_store_update(
                &current,
                &mut async_next,
                &mut compressed_response(envelopes),
            )
            .await;
            assert_eq!(sync_result.is_err(), is_delta, "kind={malformed_kind}");
            assert_eq!(format!("{sync_result:?}"), format!("{async_result:?}"));
            if is_delta {
                assert!(sync_next.feature_gates.is_empty());
                assert!(async_next.feature_gates.is_empty());
            } else {
                assert_eq!(sync_next.feature_gates.len(), 1);
                assert_eq!(sync_next.feature_gates, async_next.feature_gates);
            }
        }
    }
}

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
                    may_have_remote_config_metadata: None,
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

    compressed_response(envelopes)
}

fn full_response_with_unhydrated_remote_config_metadata() -> ResponseData {
    let envelopes = [
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(
                pb::SpecsTopLevel {
                    has_updates: true,
                    time: 1,
                    rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                    ..pb::SpecsTopLevel::default()
                }
                .encode_to_vec(),
            ),
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "remote_config".to_string(),
            checksum: "checksum".to_string(),
            data: Some(
                pb::Spec {
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
                    ..pb::Spec::default()
                }
                .encode_to_vec(),
            ),
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Done as i32,
            ..pb::SpecsEnvelope::default()
        },
    ];

    compressed_response(envelopes)
}

fn compressed_response(envelopes: impl IntoIterator<Item = pb::SpecsEnvelope>) -> ResponseData {
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

fn session_update_mode_envelope(mode: Option<&str>) -> pb::SpecsEnvelope {
    pb::SpecsEnvelope {
        name: "test_gate".to_string(),
        checksum: "checksum".to_string(),
        data: Some(
            pb::Spec {
                entity: pb::EntityType::EntityFeatureGate as i32,
                session_update_mode: mode.map(str::to_string),
                ..pb::Spec::default()
            }
            .encode_to_vec(),
        ),
        ..pb::SpecsEnvelope::default()
    }
}

fn matching_preloaded_spec(_: &InternedString) -> Option<SpecPointer> {
    Some(SpecPointer::from_spec(
        spec_from_pb(
            "checksum".to_string(),
            pb::Spec {
                entity: pb::EntityType::EntityFeatureGate as i32,
                ..pb::Spec::default()
            },
        )
        .unwrap(),
    ))
}

fn no_preloaded_spec(_: &InternedString) -> Option<SpecPointer> {
    None
}

#[test]
fn spec_from_pb_preserves_session_update_mode() {
    let spec = spec_from_pb(
        "checksum".to_string(),
        pb::Spec {
            entity: pb::EntityType::EntityFeatureGate as i32,
            session_update_mode: Some("live".to_string()),
            ..pb::Spec::default()
        },
    )
    .unwrap();

    assert_eq!(spec.session_update_mode.as_deref(), Some("live"));
}

#[test]
fn spec_from_pb_rejects_unhydrated_remote_config_metadata() {
    let result = spec_from_pb(
        "checksum".to_string(),
        pb::Spec {
            entity: pb::EntityType::EntityDynamicConfig as i32,
            remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
            ..pb::Spec::default()
        },
    );

    assert!(matches!(
        result,
        Err(crate::StatsigErr::ProtobufParseError(tag, message))
            if tag == "proto::RemoteConfigMetadata"
                && message.contains("before hydration")
    ));
}

#[test]
fn full_protobuf_response_rejects_unhydrated_remote_config_metadata() {
    let current = SpecsResponseFull::default();
    let mut next = SpecsResponseFull::default();
    let mut data = full_response_with_unhydrated_remote_config_metadata();

    let result = deserialize_protobuf(&OpsStatsForInstance::new(), &current, &mut next, &mut data);

    assert!(matches!(
        result,
        Err(crate::StatsigErr::ProtobufParseError(tag, message))
            if tag == "proto::RemoteConfigMetadata"
                && message.contains("before hydration")
    ));
    assert!(next.dynamic_configs.is_empty());
}

#[test]
fn protobuf_session_update_mode_bypasses_matching_preloaded_spec() {
    let existing = SpecsHashMap::default();
    let mut next = SpecsHashMap::default();

    SpecsResponseFull::handle_individual_spec_update(
        "FeatureGate",
        session_update_mode_envelope(Some("live")),
        &existing,
        &mut next,
        matching_preloaded_spec,
        true,
    )
    .unwrap();

    let spec = next
        .get(&InternedString::from_str_ref("test_gate"))
        .unwrap();
    assert_eq!(spec.session_update_mode(), Some("live"));
}

#[test]
fn protobuf_preserving_parser_reuses_matching_existing_session_update_mode_spec() {
    let name = InternedString::from_str_ref("test_gate");
    let existing_spec = SpecPointer::from_spec(
        spec_from_pb(
            "checksum".to_string(),
            pb::Spec {
                entity: pb::EntityType::EntityFeatureGate as i32,
                session_update_mode: Some("live".to_string()),
                ..pb::Spec::default()
            },
        )
        .unwrap(),
    );
    let existing_pointer = existing_spec.clone().into_pointer().unwrap();
    let mut existing = SpecsHashMap::default();
    existing.insert(name.clone(), existing_spec);
    let mut next = SpecsHashMap::default();

    SpecsResponseFull::handle_individual_spec_update(
        "FeatureGate",
        session_update_mode_envelope(Some("live")),
        &existing,
        &mut next,
        no_preloaded_spec,
        true,
    )
    .unwrap();

    let next_pointer = next.get(&name).unwrap().clone().into_pointer().unwrap();
    assert!(Arc::ptr_eq(&existing_pointer, &next_pointer));
}

#[test]
fn protobuf_default_parser_reuses_matching_preloaded_spec_with_session_update_mode() {
    let existing = SpecsHashMap::default();
    let mut next = SpecsHashMap::default();

    SpecsResponseFull::handle_individual_spec_update(
        "FeatureGate",
        session_update_mode_envelope(Some("live")),
        &existing,
        &mut next,
        matching_preloaded_spec,
        false,
    )
    .unwrap();

    let spec = next
        .get(&InternedString::from_str_ref("test_gate"))
        .unwrap();
    assert_eq!(spec.session_update_mode(), None);
}

#[test]
fn protobuf_preserving_parser_reuses_matching_existing_spec_without_session_update_mode() {
    let name = InternedString::from_str_ref("test_gate");
    let existing_spec = matching_preloaded_spec(&name).unwrap();
    let existing_pointer = existing_spec.clone().into_pointer().unwrap();
    let mut existing = SpecsHashMap::default();
    existing.insert(name.clone(), existing_spec);
    let mut next = SpecsHashMap::default();

    SpecsResponseFull::handle_individual_spec_update(
        "FeatureGate",
        session_update_mode_envelope(None),
        &existing,
        &mut next,
        no_preloaded_spec,
        true,
    )
    .unwrap();

    let next_pointer = next.get(&name).unwrap().clone().into_pointer().unwrap();
    assert!(Arc::ptr_eq(&existing_pointer, &next_pointer));
}

#[test]
fn copy_prev_preserves_owned_session_update_mode_spec() {
    let mut payload: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../../tests/data/eval_proj_dcs.json")).unwrap();
    let gates = payload["feature_gates"].as_object_mut().unwrap();
    let name = gates.keys().next().unwrap().clone();
    gates[&name]["sessionUpdateMode"] = serde_json::Value::String("live".to_string());
    let payload = serde_json::to_vec(&payload).unwrap();
    let current = SpecsResponseFull::deserialize_json_with_options(
        &payload,
        SpecsResponseParseOptions::preserving_session_update_mode(),
    )
    .unwrap();
    let mut data = checksum_only_delta(&current, current.time + 1, "next-checksum");
    let mut next = SpecsResponseFull::default();

    deserialize_protobuf_with_options(
        &OpsStatsForInstance::new(),
        &current,
        &mut next,
        &mut data,
        SpecsResponseParseOptions::preserving_session_update_mode(),
    )
    .unwrap();

    let spec = next
        .feature_gates
        .get(&InternedString::from_str_ref(&name))
        .unwrap();
    assert_eq!(spec.session_update_mode(), Some("live"));
}

fn entity_envelope(kind: pb::SpecsEnvelopeKind, name: &str, checksum: u32) -> pb::SpecsEnvelope {
    let data = match kind {
        pb::SpecsEnvelopeKind::FeatureGate
        | pb::SpecsEnvelopeKind::DynamicConfig
        | pb::SpecsEnvelopeKind::LayerConfig => {
            let entity = match kind {
                pb::SpecsEnvelopeKind::FeatureGate => pb::EntityType::EntityFeatureGate,
                pb::SpecsEnvelopeKind::DynamicConfig => pb::EntityType::EntityDynamicConfig,
                pb::SpecsEnvelopeKind::LayerConfig => pb::EntityType::EntityLayer,
                _ => unreachable!(),
            };
            pb::Spec {
                salt: format!("{name}-salt"),
                enabled: true,
                entity: entity as i32,
                ..pb::Spec::default()
            }
            .encode_to_vec()
        }
        pb::SpecsEnvelopeKind::ParamStore => {
            br#"{"parameters":{},"targetAppIDs":null,"version":null,"checksum":null}"#.to_vec()
        }
        pb::SpecsEnvelopeKind::Condition => pb::Condition {
            condition_type: pb::ConditionType::Public as i32,
            ..pb::Condition::default()
        }
        .encode_to_vec(),
        _ => unreachable!(),
    };

    pb::SpecsEnvelope {
        kind: kind as i32,
        name: name.to_string(),
        checksum: checksum.to_string(),
        data: Some(data),
    }
}

#[test]
fn incremental_field_checksums_track_replacements_and_deletions() {
    let cases = [
        (
            pb::SpecsEnvelopeKind::FeatureGate,
            "checksum-test-gate",
            11,
            101,
        ),
        (
            pb::SpecsEnvelopeKind::DynamicConfig,
            "checksum-test-config",
            12,
            102,
        ),
        (
            pb::SpecsEnvelopeKind::LayerConfig,
            "checksum-test-layer",
            13,
            103,
        ),
        (
            pb::SpecsEnvelopeKind::ParamStore,
            "checksum-test-store",
            14,
            104,
        ),
        (
            pb::SpecsEnvelopeKind::Condition,
            "checksum-test-condition",
            15,
            105,
        ),
    ];
    let empty = SpecsResponseFull::default();
    let mut current = SpecsResponseFull::default();
    let mut field_checksums = SpecsFieldChecksums::default();

    for &(kind, name, old_checksum, _) in &cases {
        apply_entity_update(
            kind,
            entity_envelope(kind, name, old_checksum),
            &empty,
            &mut current,
            false,
            &mut field_checksums,
        )
        .unwrap();
    }

    assert_eq!(field_checksums, SpecsFieldChecksums::from_specs(&current));
    assert_eq!(
        field_checksums,
        SpecsFieldChecksums {
            condition_map: 15,
            dynamic_configs: 12,
            feature_gates: 11,
            layer_configs: 13,
            param_stores: 14,
        }
    );

    let mut next = SpecsResponseFull::default();
    next.copy_previous_values_from(&current);
    for &(kind, name, _, new_checksum) in &cases {
        apply_entity_update(
            kind,
            entity_envelope(kind, name, new_checksum),
            &current,
            &mut next,
            false,
            &mut field_checksums,
        )
        .unwrap();
    }

    assert_eq!(field_checksums, SpecsFieldChecksums::from_specs(&next));
    assert_eq!(
        field_checksums,
        SpecsFieldChecksums {
            condition_map: 105,
            dynamic_configs: 102,
            feature_gates: 101,
            layer_configs: 103,
            param_stores: 104,
        }
    );

    next.apply_deletions(
        pb::RulesetsResponseDeletions {
            dynamic_configs: vec!["checksum-test-config".to_string()],
            feature_gates: vec!["checksum-test-gate".to_string()],
            layer_configs: vec!["checksum-test-layer".to_string()],
            condition_map: vec!["checksum-test-condition".to_string()],
            param_stores: vec!["checksum-test-store".to_string()],
            ..pb::RulesetsResponseDeletions::default()
        },
        &mut field_checksums,
    );

    assert_eq!(field_checksums, SpecsFieldChecksums::default());
    assert_eq!(field_checksums, SpecsFieldChecksums::from_specs(&next));
}

#[tokio::test]
async fn checksum_only_delta_defers_copy_prev_for_the_store() {
    let current: SpecsResponseFull =
        serde_json::from_slice(include_bytes!("../../../tests/data/eval_proj_dcs.json")).unwrap();
    let next_lcut = current.time + 1;
    let mut data = checksum_only_delta(&current, next_lcut, "next-checksum");
    let mut next = SpecsResponseFull::default();

    let update = deserialize_protobuf_for_store_with_options(
        &OpsStatsForInstance::new(),
        &current,
        SpecDecodeStats::default(),
        &SpecsFieldChecksums::from_specs(&current),
        &mut next,
        &mut data,
        false,
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

    let mut hydrated_next = SpecsResponseFull::default();
    let hydrated_update = hydrated_store_update(
        &current,
        &mut hydrated_next,
        &mut checksum_only_delta(&current, next_lcut, "next-checksum"),
    )
    .await
    .unwrap();
    assert_eq!(hydrated_update, update);
    assert!(hydrated_next.feature_gates.is_empty());
    assert!(hydrated_next.dynamic_configs.is_empty());
    assert!(hydrated_next.condition_map.is_empty());
}

#[test]
fn incremental_checksums_match_full_scan_across_update_sequences() {
    let kinds = [
        pb::SpecsEnvelopeKind::FeatureGate,
        pb::SpecsEnvelopeKind::DynamicConfig,
        pb::SpecsEnvelopeKind::LayerConfig,
        pb::SpecsEnvelopeKind::ParamStore,
        pb::SpecsEnvelopeKind::Condition,
    ];
    let mut current = SpecsResponseFull::default();
    let mut checksums = SpecsFieldChecksums::default();
    for kind in kinds {
        apply_entity_update(
            kind,
            entity_envelope(kind, "untouched-entity", 100),
            &SpecsResponseFull::default(),
            &mut current,
            false,
            &mut checksums,
        )
        .unwrap();
    }
    let untouched_checksums = checksums;

    for generation in 1..=20 {
        let mut next = SpecsResponseFull::default();
        next.copy_previous_values_from(&current);
        for kind in kinds {
            for checksum in ["0", "4294967295", "not-numeric", "", "42"] {
                let mut envelope = entity_envelope(kind, "sequence-entity", generation);
                envelope.checksum = checksum.to_string();
                apply_entity_update(kind, envelope, &current, &mut next, false, &mut checksums)
                    .unwrap();
                assert_eq!(checksums, SpecsFieldChecksums::from_specs(&next));
            }

            let mut malformed = entity_envelope(kind, "sequence-entity", generation);
            malformed.data = None;
            let before = checksums;
            assert!(
                apply_entity_update(kind, malformed, &current, &mut next, false, &mut checksums,)
                    .is_err()
            );
            assert_eq!(checksums, before);
            assert_eq!(checksums, SpecsFieldChecksums::from_specs(&next));
        }

        if generation % 2 == 0 {
            let names = vec![
                "sequence-entity".to_string(),
                "sequence-entity".to_string(),
                "missing-entity".to_string(),
            ];
            next.apply_deletions(
                pb::RulesetsResponseDeletions {
                    feature_gates: names.clone(),
                    dynamic_configs: names.clone(),
                    layer_configs: names.clone(),
                    param_stores: names.clone(),
                    condition_map: names,
                    ..pb::RulesetsResponseDeletions::default()
                },
                &mut checksums,
            );
            assert_eq!(checksums, untouched_checksums);
            assert_eq!(checksums, SpecsFieldChecksums::from_specs(&next));
        }
        current = next;
    }
}

#[test]
fn store_decoder_rejects_stale_cached_field_checksums() {
    let current: SpecsResponseFull =
        serde_json::from_slice(include_bytes!("../../../tests/data/eval_proj_dcs.json")).unwrap();
    let mut cached = SpecsFieldChecksums::from_specs(&current);
    cached.dynamic_configs = cached.dynamic_configs.wrapping_add(1);
    let mut data = checksum_only_delta(&current, current.time + 1, "next-checksum");
    let mut next = SpecsResponseFull::default();

    let result = deserialize_protobuf_for_store_with_options(
        &OpsStatsForInstance::new(),
        &current,
        SpecDecodeStats::default(),
        &cached,
        &mut next,
        &mut data,
        false,
    );

    assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
}

struct InterruptingShortReader<'a> {
    source: &'a mut dyn Read,
    chunk_size: usize,
    interrupt_next: bool,
}

impl Read for InterruptingShortReader<'_> {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        self.interrupt_next = !self.interrupt_next;
        if self.interrupt_next {
            return Err(std::io::ErrorKind::Interrupted.into());
        }
        let len = buf.len().min(self.chunk_size);
        self.source.read(&mut buf[..len])
    }
}

#[test]
fn reader_decoder_matches_compressed_snapshot_and_cursor_only_delta() {
    let current: SpecsResponseFull =
        serde_json::from_slice(include_bytes!("../../../tests/data/eval_proj_dcs.json")).unwrap();
    let snapshot = include_bytes!("../../../tests/data/eval_proj_dcs.pb.br").to_vec();
    let delta = checksum_only_delta(&current, current.time + 1, "next-checksum")
        .read_to_bytes()
        .unwrap();
    for compressed in [snapshot, delta] {
        let mut expected = SpecsResponseFull::default();
        deserialize_protobuf(
            &OpsStatsForInstance::new(),
            &current,
            &mut expected,
            &mut ResponseData::from_bytes(compressed.clone()),
        )
        .unwrap();
        for chunk_size in [1, 7, BUFFER_SIZE] {
            let mut decompressor = brotli::Decompressor::new(compressed.as_slice(), BUFFER_SIZE);
            let mut reader = InterruptingShortReader {
                source: &mut decompressor,
                chunk_size,
                interrupt_next: false,
            };
            let mut actual = SpecsResponseFull::default();
            deserialize_protobuf_from_reader(
                &OpsStatsForInstance::new(),
                &current,
                &mut actual,
                &mut reader,
            )
            .unwrap();
            assert_eq!(
                serde_json::to_value(&actual).unwrap(),
                serde_json::to_value(&expected).unwrap()
            );
        }
    }
}

#[test]
fn reader_decoder_returns_errors_for_incomplete_frames_and_io_failures() {
    let mut overflowing_length = Vec::new();
    prost::encode_length_delimiter(usize::MAX, &mut overflowing_length).unwrap();
    let mut failures: Vec<Box<dyn Read>> = vec![
        Box::new(std::io::Cursor::new(overflowing_length)),
        Box::new(std::io::empty()),
        Box::new(std::io::Cursor::new(vec![0x80])),
        Box::new(std::io::Cursor::new(vec![5, 1])),
        Box::new(std::io::Cursor::new(vec![0xff; 10])),
    ];
    struct FailedReader;
    impl Read for FailedReader {
        fn read(&mut self, _: &mut [u8]) -> std::io::Result<usize> {
            Err(std::io::Error::other("reader failed"))
        }
    }
    failures.push(Box::new(FailedReader));
    for mut reader in failures {
        assert!(matches!(
            deserialize_protobuf_from_reader(
                &OpsStatsForInstance::new(),
                &SpecsResponseFull::default(),
                &mut SpecsResponseFull::default(),
                reader.as_mut(),
            ),
            Err(StatsigErr::ProtobufParseError(_, _))
        ));
    }
}

#[test]
fn public_decoder_still_materializes_checksum_only_deltas() {
    let current: SpecsResponseFull =
        serde_json::from_slice(include_bytes!("../../../tests/data/eval_proj_dcs.json")).unwrap();
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
fn rules_from_pb_preserves_shared_control_experiments() {
    let encoded = pb::Rule {
        shared_control_experiments: vec![
            pb::SharedControlExperiment {
                name: "ranking_experiment".to_string(),
                control_group_id: "ranking_control".to_string(),
            },
            pb::SharedControlExperiment {
                name: "pipeline_experiment".to_string(),
                control_group_id: "pipeline_control".to_string(),
            },
        ],
        ..pb::Rule::default()
    }
    .encode_to_vec();

    let rules = rules_from_pb(vec![
        pb::Rule::decode(encoded.as_slice()).expect("protobuf rule should decode"),
        pb::Rule::default(),
    ])
    .expect("protobuf rules should parse");

    let experiments = rules[0]
        .shared_control_experiments
        .as_ref()
        .expect("shared-control experiments should survive protobuf decoding");
    assert_eq!(experiments.len(), 2);
    assert_eq!(experiments[0].name.as_str(), "ranking_experiment");
    assert_eq!(experiments[0].control_group_id.as_str(), "ranking_control");
    assert_eq!(experiments[1].name.as_str(), "pipeline_experiment");
    assert_eq!(experiments[1].control_group_id.as_str(), "pipeline_control");
    assert!(rules[1].shared_control_experiments.is_none());
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
        ..pb::Rule::default()
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
fn condition_from_pb_maps_experiment_group_semantics() {
    let condition = condition_from_pb(pb::Condition {
        condition_type: pb::ConditionType::ExperimentGroup as i32,
        ..pb::Condition::default()
    })
    .expect("experiment group protobuf conditions should parse");

    assert_eq!(condition.condition_type, "experiment_group");
    assert_eq!(
        condition.compiled_condition_type,
        ConditionType::ExperimentGroup
    );
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
        ..pb::Rule::default()
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
        ..pb::Rule::default()
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
        ..pb::Rule::default()
    }])
    .expect("protobuf rule should parse");

    assert_eq!(rules[0].pass_percentage, 42.0);
}

fn full_dynamic_config_response(envelopes: &[pb::SpecsEnvelope], time: u64) -> ResponseData {
    let mut response = vec![pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::TopLevel as i32,
        data: Some(
            pb::SpecsTopLevel {
                time,
                has_updates: true,
                may_have_remote_config_metadata: Some(false),
                rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                ..Default::default()
            }
            .encode_to_vec(),
        ),
        ..Default::default()
    }];
    response.extend_from_slice(envelopes);
    response.push(pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Done as i32,
        ..Default::default()
    });
    compressed_response(response)
}

rusty_fork::rusty_fork_test! {
#[test]
fn async_protobuf_mmap_reuse_preserves_session_mode() {
    use crate::interned_values::interned_store::{preload_mmap_v2_multi_for_test, write_mmap_v2_for_test};
    let mut artifact = SpecsResponseFull::default();
    let mut envelopes = Vec::new();
    for (name, entity) in [("live_config", pb::EntityType::EntityDynamicConfig), ("live_experiment", pb::EntityType::EntityExperiment)] {
        let spec = pb::Spec {
            entity: entity as i32,
            enabled: true,
            version: 8,
            session_update_mode: Some("live".to_string()),
            default_value: Some(pb::ReturnValue { value: Some(pb::return_value::Value::RawValue(br#"{"value":1}"#.to_vec())) }),
            ..Default::default()
        };
        artifact.dynamic_configs.insert(InternedString::from_str_ref(name), SpecPointer::from_spec(spec_from_pb("1".to_string(), spec.clone()).unwrap()));
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: name.to_string(), checksum: "1".to_string(), data: Some(spec.encode_to_vec()),
        });
    }
    let directory = tempfile::tempdir().unwrap();
    let path = directory.path().join("live-configs.mmap");
    write_mmap_v2_for_test(&serde_json::to_vec(&artifact).unwrap(), &path).unwrap();
    preload_mmap_v2_multi_for_test(&[("parser-protocol-tests", &path)]).unwrap();
    tokio::runtime::Runtime::new().unwrap().block_on(async {
        let empty = SpecsResponseFull::default();
        let config_name = InternedString::from_str_ref("live_config");
        let experiment_name = InternedString::from_str_ref("live_experiment");
        let mut ordinary = SpecsResponseFull::default();
        hydrated_store_update(&empty, &mut ordinary, &mut full_dynamic_config_response(&envelopes, 1)).await.unwrap();
        assert_eq!(ordinary.dynamic_configs.get(&config_name).unwrap().session_update_mode(), None);

        let mut live = SpecsResponseFull::default();
        hydrated_store_update_with_mode(&empty, &mut live, &mut full_dynamic_config_response(&envelopes, 1), true).await.unwrap();
        assert!(live.dynamic_configs.get(&config_name).unwrap().is_mmap());
        assert!(live.dynamic_configs.get(&experiment_name).unwrap().is_mmap());
        assert_eq!(live.dynamic_configs.get(&config_name).unwrap().session_update_mode(), Some("live"));
        assert_eq!(live.dynamic_configs.get(&experiment_name).unwrap().session_update_mode(), Some("live"));

        for envelope in &mut envelopes {
            let mut spec = pb::Spec::decode(envelope.data.as_ref().unwrap().as_slice()).unwrap();
            spec.session_update_mode = None;
            envelope.data = Some(spec.encode_to_vec());
        }
        let mut no_longer_live = SpecsResponseFull::default();
        hydrated_store_update_with_mode(&live, &mut no_longer_live, &mut full_dynamic_config_response(&envelopes, 2), true).await.unwrap();
        assert!(no_longer_live.dynamic_configs.get(&config_name).unwrap().is_mmap());
        assert_eq!(no_longer_live.dynamic_configs.get(&config_name).unwrap().session_update_mode(), None);
        assert_eq!(no_longer_live.dynamic_configs.get(&experiment_name).unwrap().session_update_mode(), None);

        let mut changed = pb::Spec::decode(envelopes[0].data.as_ref().unwrap().as_slice()).unwrap();
        changed.version = 9;
        changed.default_value = Some(pb::ReturnValue { value: Some(pb::return_value::Value::RawValue(br#"{"value":2}"#.to_vec())) });
        envelopes[0].checksum = "2".to_string();
        envelopes[0].data = Some(changed.encode_to_vec());
        let mut updated = SpecsResponseFull::default();
        hydrated_store_update(&ordinary, &mut updated, &mut full_dynamic_config_response(&envelopes, 3)).await.unwrap();
        assert!(!updated.dynamic_configs.get(&config_name).unwrap().is_mmap());
        assert_eq!(serde_json::to_value(updated.dynamic_configs.get(&config_name).unwrap()).unwrap()["defaultValue"]["value"], 2);
        assert_eq!(updated.dynamic_configs.get(&config_name).unwrap().as_spec_ref().version, Some(9));
    });
}
}

#[tokio::test]
async fn async_protobuf_reuse_updates_owned_session_mode() {
    let envelope = entity_envelope(pb::SpecsEnvelopeKind::DynamicConfig, "config", 7);
    let mut initial = SpecsResponseFull::default();
    hydrated_store_update_with_mode(
        &SpecsResponseFull::default(),
        &mut initial,
        &mut full_dynamic_config_response(std::slice::from_ref(&envelope), 1),
        true,
    )
    .await
    .unwrap();
    let name = InternedString::from_str_ref("config");
    assert_eq!(
        initial
            .dynamic_configs
            .get(&name)
            .unwrap()
            .session_update_mode(),
        None
    );
    let mut live_envelope = envelope;
    let mut spec = pb::Spec::decode(live_envelope.data.as_ref().unwrap().as_slice()).unwrap();
    spec.session_update_mode = Some("live".to_string());
    live_envelope.data = Some(spec.encode_to_vec());
    let mut live = SpecsResponseFull::default();
    hydrated_store_update_with_mode(
        &initial,
        &mut live,
        &mut full_dynamic_config_response(&[live_envelope], 2),
        true,
    )
    .await
    .unwrap();
    assert_eq!(
        live.dynamic_configs
            .get(&name)
            .unwrap()
            .session_update_mode(),
        Some("live")
    );
}

#[tokio::test]
async fn async_protobuf_preserving_reuse_keeps_full_and_delta_error_policy() {
    let envelope = entity_envelope(pb::SpecsEnvelopeKind::DynamicConfig, "config", 7);
    let name = InternedString::from_str_ref("config");
    let mut initial = SpecsResponseFull::default();
    hydrated_store_update(
        &SpecsResponseFull::default(),
        &mut initial,
        &mut full_dynamic_config_response(std::slice::from_ref(&envelope), 1),
    )
    .await
    .unwrap();
    let mut malformed = envelope;
    malformed.data = Some(vec![0x7a, 0x04, b'l']); // Truncated sessionUpdateMode.
    let mut full = SpecsResponseFull::default();
    hydrated_store_update_with_mode(
        &initial,
        &mut full,
        &mut full_dynamic_config_response(std::slice::from_ref(&malformed), 2),
        true,
    )
    .await
    .unwrap();
    assert!(full.dynamic_configs.get(&name).is_none());
    let mut delta = vec![
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(
                pb::SpecsTopLevel {
                    time: 2,
                    has_updates: true,
                    rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        },
        malformed,
    ];
    delta.push(pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Done as i32,
        ..Default::default()
    });
    let error = hydrated_store_update_with_mode(
        &initial,
        &mut SpecsResponseFull::default(),
        &mut compressed_response(delta),
        true,
    )
    .await
    .unwrap_err();
    assert!(matches!(error, StatsigErr::ProtobufParseError(_, _)));
}
