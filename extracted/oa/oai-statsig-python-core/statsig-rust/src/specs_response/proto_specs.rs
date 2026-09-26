use std::{
    collections::HashMap,
    io::{Cursor, Read, Write},
    sync::Arc,
};

use prost::Message;
use serde_json::json;

use crate::{
    StatsigErr,
    evaluation::{
        dynamic_returnable::DynamicReturnable, dynamic_string::DynamicString,
        evaluation_data::ReturnableRef, evaluator_value::EvaluatorValue,
    },
    interned_str,
    interned_string::InternedString,
    interned_values::{InternedStore, interned_store::MmapProjectId},
    log_error_to_statsig_and_console,
    networking::ResponseData,
    observability::{ops_stats::OpsStatsForInstance, sdk_errors_observer::ErrorBoundaryEvent},
    specs_response::{
        explicit_params::ExplicitParameters,
        param_store_types::ParameterStore,
        parse_options::SpecsResponseParseOptions,
        proto_compression::ProtoCompression,
        proto_stream_reader::{BUFFER_SIZE, ProtoStreamReader},
        spec_types::{
            Condition, ConditionOperator, ConditionType, Rule, SharedControlExperiment, Spec,
            SpecsResponseFull, SpecsResponsePartial,
        },
        specs_hash_map::{SpecDecodeStats, SpecPointer, SpecsHashMap},
        statsig_config_specs::{self as pb, any_value},
    },
};

use crate::specs_adapter::remote_config_value_hydrator::{
    ProtobufHydrationSession, RemoteConfigValueHydrator,
    protobuf_top_level_has_hydrated_sidecar_provenance,
    remote_metadata_marker_without_metadata_error, rewrite_decoded_dynamic_config_envelope,
    rewrite_top_level_envelope,
};

mod parser;

use parser::ProtobufParser;

const TAG: &str = "ProtoSpecs";
const UNHYDRATED_REMOTE_CONFIG_METADATA_TAG: &str = "proto::RemoteConfigMetadata";
const UNHYDRATED_REMOTE_CONFIG_METADATA_MESSAGE: &str =
    "Remote config metadata reached the protobuf decoder before hydration";
// Keep decoded entity envelopes bounded while the hydrator's sliding download
// window keeps the global fanout full without turning the parser back into a
// response-sized buffer.
const MAX_PENDING_HYDRATION_ENVELOPES: usize = 128;
const MAX_PENDING_HYDRATION_BYTES: usize = 8 * 1024 * 1024;

#[derive(Clone, PartialEq, Message)]
struct SessionUpdateModeField {
    #[prost(string, optional, tag = "15")]
    session_update_mode: Option<String>,
}

#[derive(Debug, PartialEq, Eq)]
pub(crate) enum ProtobufUpdate {
    Materialized {
        field_checksums: SpecsFieldChecksums,
        is_delta: bool,
    },
    CursorOnly {
        lcut: u64,
        checksum: String,
    },
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub(crate) struct SpecsFieldChecksums {
    condition_map: u64,
    dynamic_configs: u64,
    feature_gates: u64,
    layer_configs: u64,
    param_stores: u64,
}

impl SpecsFieldChecksums {
    pub(crate) fn from_specs(specs: &SpecsResponseFull) -> Self {
        Self {
            condition_map: sum_checksums(specs.condition_map.values().map(checksum_for_condition)),
            dynamic_configs: sum_checksums(specs.dynamic_configs.0.values().map(checksum_for_spec)),
            feature_gates: sum_checksums(specs.feature_gates.0.values().map(checksum_for_spec)),
            layer_configs: sum_checksums(specs.layer_configs.0.values().map(checksum_for_spec)),
            param_stores: sum_checksums(
                specs
                    .param_stores
                    .as_ref()
                    .map(|stores| stores.values().map(checksum_for_param_store))
                    .into_iter()
                    .flatten(),
            ),
        }
    }

    fn validate_envelope(&self, envelope: pb::SpecsEnvelope) -> Result<(), StatsigErr> {
        let envelope_data = validate_envelope_data("Checksums", envelope.data)?;
        let checksums = pb::RulesetsChecksums::decode(envelope_data)
            .map_err(|e| map_decode_err("RulesetsChecksums", e))?;
        let expected = &checksums.field_checksums;

        validate_field_checksum("condition_map", expected, self.condition_map)?;
        validate_field_checksum("dynamic_configs", expected, self.dynamic_configs)?;
        validate_field_checksum("feature_gates", expected, self.feature_gates)?;
        validate_field_checksum("layer_configs", expected, self.layer_configs)?;
        validate_field_checksum("param_stores", expected, self.param_stores)?;

        Ok(())
    }

    fn replace_for_entity(
        &mut self,
        kind: pb::SpecsEnvelopeKind,
        old_checksum: Option<u32>,
        new_checksum: Option<u32>,
    ) {
        let total = match kind {
            pb::SpecsEnvelopeKind::FeatureGate => &mut self.feature_gates,
            pb::SpecsEnvelopeKind::DynamicConfig => &mut self.dynamic_configs,
            pb::SpecsEnvelopeKind::LayerConfig => &mut self.layer_configs,
            pb::SpecsEnvelopeKind::ParamStore => &mut self.param_stores,
            pb::SpecsEnvelopeKind::Condition => &mut self.condition_map,
            _ => unreachable!(),
        };
        replace_checksum(total, old_checksum, new_checksum);
    }
}

#[derive(Clone, Copy)]
pub(crate) struct ProtobufHydrationContext<'a> {
    pub(crate) hydrator: &'a RemoteConfigValueHydrator,
    pub(crate) source_url: &'a str,
    pub(crate) mmap_project_id: MmapProjectId,
    pub(crate) capture_hydrated_data_store_bytes: bool,
    pub(crate) preserve_session_update_mode: bool,
}

/// Streams a hydrated protobuf copy while the main parser consumes the
/// original compressed body. The copy keeps the original compression format
/// so the codec-specific datastore key and bytes agree; it is discarded when no
/// remote metadata was actually hydrated.
struct HydratedProtobufDataStoreCapture {
    writer: HydratedProtobufDataStoreWriter,
    saw_remote_metadata: bool,
}

enum HydratedProtobufDataStoreWriter {
    Brotli(Box<brotli::CompressorWriter<Vec<u8>>>),
    Zstd(zstd::stream::write::Encoder<'static, Vec<u8>>),
}

impl HydratedProtobufDataStoreCapture {
    fn new(compression: ProtoCompression) -> Result<Self, StatsigErr> {
        let writer = match compression {
            ProtoCompression::Brotli => HydratedProtobufDataStoreWriter::Brotli(Box::new(
                // Rebuilding the hydrated datastore snapshot is on the full-sync
                // path. Favor encoder CPU over compression density while keeping
                // the same Brotli format and decoded protobuf bytes for readers.
                brotli::CompressorWriter::new(Vec::new(), BUFFER_SIZE, 2, 22),
            )),
            ProtoCompression::Zstd => HydratedProtobufDataStoreWriter::Zstd(
                zstd::stream::write::Encoder::new(Vec::new(), 3)
                    .map_err(|error| StatsigErr::SerializationError(error.to_string()))?,
            ),
        };

        Ok(Self {
            writer,
            saw_remote_metadata: false,
        })
    }

    fn write_frame(&mut self, frame: &[u8]) -> Result<(), StatsigErr> {
        let result = match &mut self.writer {
            HydratedProtobufDataStoreWriter::Brotli(writer) => writer.write_all(frame),
            HydratedProtobufDataStoreWriter::Zstd(writer) => writer.write_all(frame),
        };
        result.map_err(|error| StatsigErr::SerializationError(error.to_string()))
    }

    fn mark_remote_metadata(&mut self) {
        self.saw_remote_metadata = true;
    }

    fn finish(self) -> Result<Option<Vec<u8>>, StatsigErr> {
        if !self.saw_remote_metadata {
            return Ok(None);
        }

        let bytes = match self.writer {
            HydratedProtobufDataStoreWriter::Brotli(writer) => writer.into_inner(),
            HydratedProtobufDataStoreWriter::Zstd(writer) => writer
                .finish()
                .map_err(|error| StatsigErr::SerializationError(error.to_string()))?,
        };

        Ok(Some(bytes))
    }
}

/// One bounded, ordered parser entry waiting for a shared remote-value
/// download batch. Non-dynamic entities are queued too, so dynamic configs
/// separated by other entity kinds still share the same download fanout while
/// every mutation and datastore frame remains in wire order.
enum PendingEntityUpdate {
    Dynamic(Box<PendingDynamicConfigUpdate>),
    Other {
        kind: pb::SpecsEnvelopeKind,
        envelope: pb::SpecsEnvelope,
        tolerates_malformed_entity: bool,
        raw_frame: Option<Vec<u8>>,
    },
}

/// Response-wide state shared by pending-entity preparation and publication.
struct PendingEntityParserContext<'a, 'h> {
    parser: ProtobufParser<'a>,
    hydrated_sidecar_provenance: bool,
    hydration: &'a mut ProtobufHydrationSession<'h>,
    mmap_project_id: MmapProjectId,
    preserve_session_update_mode: bool,
    spec_decode_stats: SpecDecodeStats,
}

/// Bounded, ordered entity work waiting for the next shared hydration batch.
#[derive(Default)]
struct PendingEntityBatch {
    updates: Vec<PendingEntityUpdate>,
    bytes: usize,
}

impl PendingEntityBatch {
    fn push(&mut self, update: PendingEntityUpdate, raw_envelope_len: usize) {
        self.updates.push(update);
        self.bytes = self.bytes.saturating_add(raw_envelope_len);
    }

    fn should_flush(&self, context: &PendingEntityParserContext<'_, '_>) -> bool {
        context.parser.remote_metadata_hint() != Some(true)
            || self.updates.len() >= MAX_PENDING_HYDRATION_ENVELOPES
            || self.bytes >= MAX_PENDING_HYDRATION_BYTES
    }
}

enum PendingDynamicConfigUpdate {
    // A matching mmap/current value needs no decode or download when there is
    // no datastore sidecar to rewrite.
    Reused {
        name: InternedString,
        spec_pointer: SpecPointer,
    },
    Decoded(Box<PendingDecodedDynamicConfigUpdate>),
}

struct PendingDecodedDynamicConfigUpdate {
    envelope: pb::SpecsEnvelope,
    spec: pb::Spec,
    reused: Option<(InternedString, SpecPointer)>,
    verify_reused_against_decoded: bool,
    tolerates_malformed_entity: bool,
    has_remote_metadata: bool,
    raw_frame: Option<Vec<u8>>,
}

pub fn deserialize_protobuf(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull, /* Intentionally immutable so we can continue using it if parsing fails */
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
) -> Result<(), StatsigErr> {
    deserialize_protobuf_with_options(
        ops_stats,
        current_specs,
        next_specs,
        data,
        SpecsResponseParseOptions::default(),
    )
}

/// Decodes an uncompressed, length-delimited protobuf specs stream from its
/// current position. Uses the same parsing defaults as `deserialize_protobuf`.
/// The reader may be borrowed and does not need to support seeking.
pub fn deserialize_protobuf_from_reader(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull,
    next_specs: &mut SpecsResponseFull,
    reader: &mut dyn Read,
) -> Result<(), StatsigErr> {
    let current_field_checksums = SpecsFieldChecksums::from_specs(current_specs);
    if matches!(
        deserialize_protobuf_from_stream(
            ops_stats,
            current_specs,
            SpecDecodeStats::default(),
            &current_field_checksums,
            next_specs,
            ProtoStreamReader::from_reader(reader),
            SpecsResponseParseOptions::default(),
        )?,
        ProtobufUpdate::CursorOnly { .. }
    ) {
        next_specs.copy_previous_values_from(current_specs);
    }

    Ok(())
}

pub fn deserialize_protobuf_with_options(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull, /* Intentionally immutable so we can continue using it if parsing fails */
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
    options: SpecsResponseParseOptions,
) -> Result<(), StatsigErr> {
    let current_field_checksums = SpecsFieldChecksums::from_specs(current_specs);
    if matches!(
        deserialize_protobuf_from_stream(
            ops_stats,
            current_specs,
            SpecDecodeStats::default(),
            &current_field_checksums,
            next_specs,
            ProtoStreamReader::new_for_response(data)?,
            options,
        )?,
        ProtobufUpdate::CursorOnly { .. }
    ) {
        next_specs.copy_previous_values_from(current_specs);
    }

    Ok(())
}

/// Parses and hydrates one compressed protobuf response in the same envelope
/// loop. The reader stays on the original compressed body; only the synchronous
/// mutation steps enter mmap/decode-stat thread-local scopes, so no
/// thread-local state survives a remote-value await.
pub(crate) async fn deserialize_protobuf_for_store_with_hydration(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
    context: ProtobufHydrationContext<'_>,
) -> Result<(ProtobufUpdate, SpecDecodeStats, Option<Vec<u8>>), StatsigErr> {
    let current_field_checksums = SpecsFieldChecksums::from_specs(current_specs);
    deserialize_protobuf_for_store_with_hydration_and_checksums(
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        &current_field_checksums,
        next_specs,
        data,
        context,
    )
    .await
}

pub(crate) async fn deserialize_protobuf_for_store_with_hydration_and_checksums(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
    current_field_checksums: &SpecsFieldChecksums,
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
    context: ProtobufHydrationContext<'_>,
) -> Result<(ProtobufUpdate, SpecDecodeStats, Option<Vec<u8>>), StatsigErr> {
    let mut hydration = context
        .hydrator
        .begin_protobuf_hydration(context.source_url);
    let result = deserialize_protobuf_for_store_with_hydration_inner(
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        current_field_checksums,
        next_specs,
        data,
        &mut hydration,
        context,
    )
    .await;
    hydration.finish(result.as_ref().map(|_| ()));
    result
}

#[allow(clippy::too_many_arguments)]
async fn deserialize_protobuf_for_store_with_hydration_inner(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
    current_field_checksums: &SpecsFieldChecksums,
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
    hydration: &mut ProtobufHydrationSession<'_>,
    context: ProtobufHydrationContext<'_>,
) -> Result<(ProtobufUpdate, SpecDecodeStats, Option<Vec<u8>>), StatsigErr> {
    let ProtobufHydrationContext {
        mmap_project_id,
        capture_hydrated_data_store_bytes,
        preserve_session_update_mode,
        ..
    } = context;
    let mut data_store_capture: Option<HydratedProtobufDataStoreCapture> = None;
    let mut pending_entity_batch = PendingEntityBatch::default();
    let data_store_compression =
        ProtoCompression::from_response(data).unwrap_or(ProtoCompression::Brotli);

    let mut parser_context = PendingEntityParserContext {
        parser: ProtobufParser::new(
            ops_stats,
            current_specs,
            previous_spec_decode_stats,
            current_field_checksums,
            next_specs,
        )?,
        hydrated_sidecar_provenance: false,
        hydration,
        mmap_project_id,
        preserve_session_update_mode,
        spec_decode_stats: SpecDecodeStats::default(),
    };

    data.rewind()?;
    let mut reader = ProtoStreamReader::new_for_response(data)?;

    loop {
        let proto_msg_bytes = parser_context.parser.read_frame(&mut reader)?;
        // Keep the raw frame for hydration capture without copying the decoder input.
        let Some((envelope_kind, env)) = parser_context
            .parser
            .decode_envelope(proto_msg_bytes.clone())?
        else {
            flush_pending_entity_updates(
                &mut parser_context,
                &mut pending_entity_batch,
                &mut data_store_capture,
            )
            .await?;
            if let Some(capture) = data_store_capture.as_mut() {
                capture.write_frame(proto_msg_bytes.as_ref())?;
            }
            continue;
        };

        let mut data_store_frame = None;
        let is_entity_envelope = matches!(
            envelope_kind,
            pb::SpecsEnvelopeKind::FeatureGate
                | pb::SpecsEnvelopeKind::DynamicConfig
                | pb::SpecsEnvelopeKind::LayerConfig
                | pb::SpecsEnvelopeKind::ParamStore
                | pb::SpecsEnvelopeKind::Condition
        );

        if !is_entity_envelope {
            // Entity updates batch remote-value downloads for concurrency.
            // Flush before control envelopes so deletions, checksums, and
            // completion observe every preceding entity update.
            flush_pending_entity_updates(
                &mut parser_context,
                &mut pending_entity_batch,
                &mut data_store_capture,
            )
            .await?;
        }

        match envelope_kind {
            pb::SpecsEnvelopeKind::Done => {
                // The producer only sets the marker when this response
                // actually carries remote metadata. Reject a mismatched
                // response before the candidate snapshot can be published.
                if parser_context.parser.remote_metadata_hint() == Some(true)
                    && !parser_context.hydration.saw_remote_metadata()
                {
                    return Err(remote_metadata_marker_without_metadata_error());
                }
                let update = parser_context
                    .spec_decode_stats
                    .with_mmap_project(parser_context.mmap_project_id, || {
                        parser_context.parser.finish()
                    })?;
                if let Some(capture) = data_store_capture.as_mut() {
                    capture.write_frame(proto_msg_bytes.as_ref())?;
                }
                let hydrated_data_store_bytes = data_store_capture
                    .map(HydratedProtobufDataStoreCapture::finish)
                    .transpose()?
                    .flatten();
                return Ok((
                    update,
                    parser_context.spec_decode_stats,
                    hydrated_data_store_bytes,
                ));
            }
            pb::SpecsEnvelopeKind::TopLevel => {
                let top_level_hydrated_sidecar_provenance = env
                    .data
                    .as_deref()
                    .map(protobuf_top_level_has_hydrated_sidecar_provenance)
                    .transpose()?
                    .unwrap_or(false);
                let rewritten_top_level = (capture_hydrated_data_store_bytes
                    && !parser_context.parser.is_delta())
                .then(|| rewrite_top_level_envelope(proto_msg_bytes.as_ref(), &env));

                let accepted = parser_context
                    .spec_decode_stats
                    .with_mmap_project(parser_context.mmap_project_id, || {
                        parser_context.parser.handle_top_level(env)
                    })?;
                if accepted {
                    parser_context.hydrated_sidecar_provenance =
                        top_level_hydrated_sidecar_provenance;
                    if capture_hydrated_data_store_bytes
                        && !parser_context.parser.is_delta()
                        && parser_context.parser.remote_metadata_hint() == Some(true)
                    {
                        if data_store_capture.is_none() {
                            data_store_capture = Some(HydratedProtobufDataStoreCapture::new(
                                data_store_compression,
                            )?);
                        }
                        data_store_frame = Some(
                            rewritten_top_level.expect("full top-level capture was prepared")?,
                        );
                    }
                }
            }
            kind @ (pb::SpecsEnvelopeKind::FeatureGate
            | pb::SpecsEnvelopeKind::DynamicConfig
            | pb::SpecsEnvelopeKind::LayerConfig
            | pb::SpecsEnvelopeKind::ParamStore
            | pb::SpecsEnvelopeKind::Condition) => {
                let pending = prepare_pending_entity_update(
                    &mut parser_context,
                    kind,
                    env,
                    proto_msg_bytes.as_ref(),
                    data_store_capture.is_some(),
                )?;

                let Some(pending) = pending else {
                    // A malformed full-response entity is tolerated, but any
                    // earlier queued entities still need to publish first.
                    flush_pending_entity_updates(
                        &mut parser_context,
                        &mut pending_entity_batch,
                        &mut data_store_capture,
                    )
                    .await?;
                    if let Some(capture) = data_store_capture.as_mut() {
                        capture.write_frame(proto_msg_bytes.as_ref())?;
                    }
                    continue;
                };

                pending_entity_batch.push(pending, proto_msg_bytes.as_ref().len());
                if pending_entity_batch.should_flush(&parser_context) {
                    flush_pending_entity_updates(
                        &mut parser_context,
                        &mut pending_entity_batch,
                        &mut data_store_capture,
                    )
                    .await?;
                } else {
                    // Keep newly discovered remote values moving without
                    // treating a full download window as a parser boundary.
                    parser_context.hydration.advance_download_window().await?;
                }

                // Queued entity frames are written by the ordered flush, not
                // by the generic bottom-of-loop capture path below.
                continue;
            }
            pb::SpecsEnvelopeKind::Deletions => {
                let _ = parser_context
                    .spec_decode_stats
                    .with_mmap_project(parser_context.mmap_project_id, || {
                        parser_context.parser.handle_deletions(env, false)
                    })?;
            }
            pb::SpecsEnvelopeKind::Checksums => {
                parser_context
                    .spec_decode_stats
                    .with_mmap_project(parser_context.mmap_project_id, || {
                        parser_context.parser.handle_checksums(env)
                    })?;
            }
            pb::SpecsEnvelopeKind::CopyPrev => {
                parser_context.parser.handle_copy_prev()?;
            }
            pb::SpecsEnvelopeKind::Unknown => {
                return make_proto_parse_error("SpecsEnvelope", "Unknown envelope kind");
            }
        };

        if let Some(capture) = data_store_capture.as_mut() {
            capture.write_frame(
                data_store_frame
                    .as_deref()
                    .unwrap_or_else(|| proto_msg_bytes.as_ref()),
            )?;
        }
    }
}

fn prepare_pending_entity_update(
    context: &mut PendingEntityParserContext<'_, '_>,
    kind: pb::SpecsEnvelopeKind,
    envelope: pb::SpecsEnvelope,
    raw_envelope: &[u8],
    capture_hydrated_frame: bool,
) -> Result<Option<PendingEntityUpdate>, StatsigErr> {
    // Only the deferred transition copies specs and needs decode accounting.
    let tolerates_malformed_entity = if context.parser.is_deferred_delta() {
        context
            .spec_decode_stats
            .with_mmap_project(context.mmap_project_id, || {
                context.parser.prepare_entity_update()
            })?
    } else {
        context.parser.prepare_entity_update()?
    };
    let raw_frame = capture_hydrated_frame.then(|| raw_envelope.to_vec());

    if kind != pb::SpecsEnvelopeKind::DynamicConfig {
        return Ok(Some(PendingEntityUpdate::Other {
            kind,
            envelope,
            tolerates_malformed_entity,
            raw_frame,
        }));
    }

    let reused = context
        .spec_decode_stats
        .with_mmap_project(context.mmap_project_id, || {
            context
                .parser
                .next_specs
                .find_reusable_dynamic_config_update(&envelope, context.parser.current_specs)
        });
    // Hydrated sidecars decode as marker=false after their metadata is
    // stripped, but retain a true-then-false marker history. Their envelope
    // checksum is still the producer checksum, so checksum alone cannot prove
    // that an older mmap pointer contains the hydrated value.
    let reused = match reused {
        Some((name, spec_pointer))
            if !capture_hydrated_frame
                && context.parser.remote_metadata_hint() != Some(true)
                && !context.hydrated_sidecar_provenance =>
        {
            let spec_pointer = if context.preserve_session_update_mode {
                // mmap specs omit this response metadata. Read only the mode so
                // matching values and rules can still bypass full decoding.
                let mode = match validate_envelope_data("DynamicConfig", envelope.data.as_deref())
                    .and_then(|data| {
                        decode_session_update_mode(data.get_ref())
                            .map_err(|error| map_decode_err("DynamicConfig", error))
                    }) {
                    Ok(mode) => mode,
                    Err(error) => {
                        finish_entity_parse_result(
                            context.parser.ops_stats,
                            Err(error),
                            tolerates_malformed_entity,
                        )?;
                        return Ok(None);
                    }
                };
                spec_pointer.with_session_update_mode(mode.as_deref())
            } else {
                Some(spec_pointer)
            };
            if let Some(spec_pointer) = spec_pointer {
                return Ok(Some(PendingEntityUpdate::Dynamic(Box::new(
                    PendingDynamicConfigUpdate::Reused { name, spec_pointer },
                ))));
            }
            // A pointer that cannot represent the new mode needs full decoding.
            None
        }
        reused => reused,
    };

    let envelope_data = match validate_envelope_data("DynamicConfig", envelope.data.as_deref()) {
        Ok(data) => data,
        Err(error) => {
            finish_entity_parse_result(
                context.parser.ops_stats,
                Err(error),
                tolerates_malformed_entity,
            )?;
            return Ok(None);
        }
    };
    let spec = match pb::Spec::decode(envelope_data) {
        Ok(spec) => spec,
        Err(error) => {
            finish_entity_parse_result(
                context.parser.ops_stats,
                Err(map_decode_err("DynamicConfig", error)),
                tolerates_malformed_entity,
            )?;
            return Ok(None);
        }
    };
    let reused = if context.preserve_session_update_mode {
        reused.and_then(|(name, spec_pointer)| {
            spec_pointer
                .with_session_update_mode(spec.session_update_mode.as_deref())
                .map(|spec_pointer| (name, spec_pointer))
        })
    } else {
        reused
    };

    let has_remote_metadata = protobuf_spec_has_remote_metadata(&spec);
    let mut reuse_verified_remote_values = false;
    if has_remote_metadata {
        context.hydration.mark_remote_metadata();
        // Remote hydration is an explicit producer opt-in. A missing or false
        // top-level marker must not make a markerless response hydrate.
        if context.parser.remote_metadata_hint() != Some(true) {
            return Err(unhydrated_remote_config_metadata_error());
        }
        context.hydration.register_spec_references(&spec)?;
        if let Some(candidate_values) = reused.as_ref().and_then(|(_, spec_pointer)| {
            context
                .spec_decode_stats
                .with_mmap_project(context.mmap_project_id, || {
                    existing_hydrated_values(spec_pointer, &spec)
                })
        }) {
            reuse_verified_remote_values = context.hydration.seed_verified_values(candidate_values);
        }
    }
    // A matching pointer may be an older artifact that still contains the
    // placeholder. Reuse it only when every existing remote-backed value can
    // be reconstructed and independently verified against its full SHA-256.
    let reused = if has_remote_metadata && !reuse_verified_remote_values {
        None
    } else {
        reused
    };

    Ok(Some(PendingEntityUpdate::Dynamic(Box::new(
        PendingDynamicConfigUpdate::Decoded(Box::new(PendingDecodedDynamicConfigUpdate {
            envelope,
            spec,
            reused,
            verify_reused_against_decoded: context.hydrated_sidecar_provenance,
            tolerates_malformed_entity,
            has_remote_metadata,
            raw_frame,
        })),
    ))))
}

fn existing_hydrated_values(
    existing: &SpecPointer,
    incoming: &pb::Spec,
) -> Option<HashMap<String, Arc<Vec<u8>>>> {
    let existing = existing.view();
    if existing.rules_len() != incoming.rules.len() {
        return None;
    }

    let mut verified = HashMap::new();
    if let Some(metadata) = incoming.remote_config_metadata.as_ref() {
        insert_existing_hydrated_value(&mut verified, existing.default_value(), metadata)?;
    }

    for (index, rule) in incoming.rules.iter().enumerate() {
        let existing_rule = existing.rule(index);
        if existing_rule.id().as_str() != rule.id {
            return None;
        }
        if let Some(metadata) = rule.remote_config_metadata.as_ref() {
            insert_existing_hydrated_value(&mut verified, existing_rule.return_value(), metadata)?;
        }
    }

    Some(verified)
}

fn insert_existing_hydrated_value(
    verified: &mut HashMap<String, Arc<Vec<u8>>>,
    value: ReturnableRef<'_>,
    metadata: &pb::RemoteConfigValueMetadata,
) -> Option<()> {
    // Archived returnables retain parsed JSON, not its original wire bytes.
    // Reuse only when serialization exactly reconstructs the producer's
    // authenticated bytes; whitespace, key-order, or numeric-lexeme changes
    // safely fall back to the normal verified download path.
    let bytes = serde_json::to_vec(&value.to_owned()).ok()?;
    if bytes.len() as u64 != metadata.byte_length {
        return None;
    }

    if let Some(existing) = verified.get(&metadata.sha256) {
        return (existing.as_slice() == bytes.as_slice()).then_some(());
    }

    verified.insert(metadata.sha256.clone(), Arc::new(bytes));
    Some(())
}

async fn flush_pending_entity_updates(
    context: &mut PendingEntityParserContext<'_, '_>,
    batch: &mut PendingEntityBatch,
    data_store_capture: &mut Option<HydratedProtobufDataStoreCapture>,
) -> Result<(), StatsigErr> {
    if batch.updates.is_empty() {
        return Ok(());
    }

    context.hydration.download_registered_references().await?;

    for pending in batch.updates.drain(..) {
        match pending {
            PendingEntityUpdate::Other {
                kind,
                envelope,
                tolerates_malformed_entity,
                raw_frame,
            } => {
                let result =
                    context
                        .spec_decode_stats
                        .with_mmap_project(context.mmap_project_id, || {
                            apply_entity_update(
                                kind,
                                envelope,
                                context.parser.current_specs,
                                context.parser.next_specs,
                                context.preserve_session_update_mode,
                                &mut context.parser.next_field_checksums,
                            )
                        });
                finish_entity_parse_result(
                    context.parser.ops_stats,
                    result,
                    tolerates_malformed_entity,
                )?;
                if let Some(capture) = data_store_capture.as_mut() {
                    capture.write_frame(
                        raw_frame
                            .as_deref()
                            .expect("captured entity frame must retain wire bytes"),
                    )?;
                }
            }
            PendingEntityUpdate::Dynamic(pending) => match *pending {
                PendingDynamicConfigUpdate::Reused { name, spec_pointer } => {
                    let checksum_name = name.clone();
                    let old_checksum = entity_checksum(
                        pb::SpecsEnvelopeKind::DynamicConfig,
                        context.parser.next_specs,
                        &checksum_name,
                    );
                    context
                        .spec_decode_stats
                        .with_mmap_project(context.mmap_project_id, || {
                            context
                                .parser
                                .next_specs
                                .insert_reused_dynamic_config_update(name, spec_pointer);
                        });
                    record_entity_checksum_update(
                        pb::SpecsEnvelopeKind::DynamicConfig,
                        context.parser.next_specs,
                        &mut context.parser.next_field_checksums,
                        &checksum_name,
                        old_checksum,
                    );
                }
                PendingDynamicConfigUpdate::Decoded(decoded) => {
                    let PendingDecodedDynamicConfigUpdate {
                        envelope,
                        mut spec,
                        reused,
                        verify_reused_against_decoded,
                        tolerates_malformed_entity,
                        has_remote_metadata,
                        raw_frame,
                    } = *decoded;
                    let mut hydrated_frame = None;
                    if has_remote_metadata {
                        let raw_spec = data_store_capture.is_some().then(|| spec.clone());
                        context.hydration.apply_registered_spec(&mut spec)?;
                        if let (Some(raw_frame), Some(raw_spec)) =
                            (raw_frame.as_deref(), raw_spec.as_ref())
                        {
                            hydrated_frame = Some(rewrite_decoded_dynamic_config_envelope(
                                raw_frame,
                                envelope
                                    .data
                                    .as_deref()
                                    .expect("decoded dynamic config must retain spec bytes"),
                                raw_spec,
                                context.hydration.hydrated_values(),
                            )?);
                        }
                    }

                    // A hydrated sidecar may share an envelope checksum with
                    // an older placeholder-backed mmap artifact. Compare its
                    // decoded content before reusing that pointer; untouched
                    // configs still keep their mmap sharing when they match.
                    if let Some((name, spec_pointer)) = reused {
                        let checksum_name = name.clone();
                        let old_checksum = entity_checksum(
                            pb::SpecsEnvelopeKind::DynamicConfig,
                            context.parser.next_specs,
                            &checksum_name,
                        );
                        if verify_reused_against_decoded {
                            let decoded_spec = spec_from_pb(envelope.checksum, spec)?;
                            if spec_pointer.matches_owned_spec(&decoded_spec) {
                                context.spec_decode_stats.with_mmap_project(
                                    context.mmap_project_id,
                                    || {
                                        context
                                            .parser
                                            .next_specs
                                            .insert_reused_dynamic_config_update(
                                                name,
                                                spec_pointer,
                                            );
                                    },
                                );
                            } else {
                                context.spec_decode_stats.with_mmap_project(
                                    context.mmap_project_id,
                                    || {
                                        context
                                            .parser
                                            .next_specs
                                            .insert_owned_dynamic_config_update(name, decoded_spec);
                                    },
                                );
                            }
                        } else {
                            context.spec_decode_stats.with_mmap_project(
                                context.mmap_project_id,
                                || {
                                    context
                                        .parser
                                        .next_specs
                                        .insert_reused_dynamic_config_update(name, spec_pointer);
                                },
                            );
                        }
                        record_entity_checksum_update(
                            pb::SpecsEnvelopeKind::DynamicConfig,
                            context.parser.next_specs,
                            &mut context.parser.next_field_checksums,
                            &checksum_name,
                            old_checksum,
                        );
                    } else {
                        let checksum_name = InternedString::from_str_ref(&envelope.name);
                        let old_checksum = entity_checksum(
                            pb::SpecsEnvelopeKind::DynamicConfig,
                            context.parser.next_specs,
                            &checksum_name,
                        );
                        let result = context.spec_decode_stats.with_mmap_project(
                            context.mmap_project_id,
                            || {
                                context
                                    .parser
                                    .next_specs
                                    .handle_decoded_dynamic_config_update(envelope, spec)
                            },
                        );
                        let updated = result.is_ok();
                        finish_entity_parse_result(
                            context.parser.ops_stats,
                            result,
                            tolerates_malformed_entity,
                        )?;
                        if updated {
                            record_entity_checksum_update(
                                pb::SpecsEnvelopeKind::DynamicConfig,
                                context.parser.next_specs,
                                &mut context.parser.next_field_checksums,
                                &checksum_name,
                                old_checksum,
                            );
                        }
                    }

                    if let Some(capture) = data_store_capture.as_mut() {
                        if hydrated_frame.is_some() {
                            capture.mark_remote_metadata();
                        }
                        capture.write_frame(
                            hydrated_frame
                                .as_deref()
                                .or(raw_frame.as_deref())
                                .expect("captured dynamic config frame must retain wire bytes"),
                        )?;
                    }
                }
            },
        }
    }

    batch.bytes = 0;

    Ok(())
}

fn finish_entity_parse_result(
    ops_stats: &OpsStatsForInstance,
    result: Result<(), StatsigErr>,
    tolerates_malformed_entity: bool,
) -> Result<(), StatsigErr> {
    match log_parse_result(ops_stats, result) {
        Ok(()) => Ok(()),
        Err(error)
            if tolerates_malformed_entity
                && !is_unhydrated_remote_config_metadata_error(&error) =>
        {
            Ok(())
        }
        Err(error) => Err(error),
    }
}

fn protobuf_spec_has_remote_metadata(spec: &pb::Spec) -> bool {
    spec.remote_config_metadata.is_some()
        || spec
            .rules
            .iter()
            .any(|rule| rule.remote_config_metadata.is_some())
}

pub(crate) fn deserialize_protobuf_for_store_with_options(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull, /* Intentionally immutable so we can continue using it if parsing fails */
    previous_spec_decode_stats: SpecDecodeStats,
    current_field_checksums: &SpecsFieldChecksums,
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
    preserve_session_update_mode: bool,
) -> Result<ProtobufUpdate, StatsigErr> {
    deserialize_protobuf_from_stream(
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        current_field_checksums,
        next_specs,
        ProtoStreamReader::new_for_response(data)?,
        if preserve_session_update_mode {
            SpecsResponseParseOptions::preserving_session_update_mode()
        } else {
            SpecsResponseParseOptions::default()
        },
    )
}

fn deserialize_protobuf_from_stream<R: Read>(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
    current_field_checksums: &SpecsFieldChecksums,
    next_specs: &mut SpecsResponseFull,
    mut reader: ProtoStreamReader<'_, R>,
    options: SpecsResponseParseOptions,
) -> Result<ProtobufUpdate, StatsigErr> {
    let mut parser = ProtobufParser::new(
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        current_field_checksums,
        next_specs,
    )?;

    // The preload snapshot omits remote specs, so their last checksums live
    // separately until a later update or deletion replaces them on the wire.
    let mut skipped_remote_checksums = HashMap::new();

    loop {
        let frame = parser.read_frame(&mut reader)?;
        let Some((kind, envelope)) = parser.decode_envelope(frame)? else {
            continue;
        };

        match kind {
            pb::SpecsEnvelopeKind::Done => return parser.finish(),
            pb::SpecsEnvelopeKind::TopLevel => {
                parser.handle_top_level(envelope)?;
            }
            pb::SpecsEnvelopeKind::FeatureGate
            | pb::SpecsEnvelopeKind::DynamicConfig
            | pb::SpecsEnvelopeKind::LayerConfig
            | pb::SpecsEnvelopeKind::ParamStore
            | pb::SpecsEnvelopeKind::Condition => {
                let tolerates_malformed_entity = parser.prepare_entity_update()?;
                let result = if options.should_skip_unhydrated_dynamic_configs_for_preload()
                    && kind == pb::SpecsEnvelopeKind::DynamicConfig
                {
                    let remote_metadata_hint = parser.remote_metadata_hint();
                    apply_dynamic_config_update_skipping_unhydrated(
                        envelope,
                        parser.next_specs,
                        &mut parser.next_field_checksums,
                        &mut skipped_remote_checksums,
                        remote_metadata_hint,
                    )
                } else {
                    apply_entity_update(
                        kind,
                        envelope,
                        parser.current_specs,
                        parser.next_specs,
                        options.should_preserve_session_update_mode(),
                        &mut parser.next_field_checksums,
                    )
                };
                finish_entity_parse_result(ops_stats, result, tolerates_malformed_entity)?;
            }
            pb::SpecsEnvelopeKind::Deletions => {
                let deleted_dynamic_configs = parser.handle_deletions(
                    envelope,
                    options.should_skip_unhydrated_dynamic_configs_for_preload(),
                )?;
                for name in deleted_dynamic_configs.into_iter().flatten() {
                    if let Some(checksum) =
                        skipped_remote_checksums.remove(&InternedString::from_string(name))
                    {
                        parser.next_field_checksums.replace_for_entity(
                            pb::SpecsEnvelopeKind::DynamicConfig,
                            Some(checksum),
                            None,
                        );
                    }
                }
            }
            pb::SpecsEnvelopeKind::Checksums => parser.handle_checksums(envelope)?,
            pb::SpecsEnvelopeKind::CopyPrev => parser.handle_copy_prev()?,
            pb::SpecsEnvelopeKind::Unknown => {
                return make_proto_parse_error("SpecsEnvelope", "Unknown envelope kind");
            }
        }
    }
}

fn apply_dynamic_config_update_skipping_unhydrated(
    envelope: pb::SpecsEnvelope,
    next_specs: &mut SpecsResponseFull,
    field_checksums: &mut SpecsFieldChecksums,
    skipped_remote_checksums: &mut HashMap<InternedString, u32>,
    remote_metadata_hint: Option<bool>,
) -> Result<(), StatsigErr> {
    let name = InternedString::from_str_ref(&envelope.name);
    let old_checksum = next_specs
        .dynamic_configs
        .get(&name)
        .and_then(checksum_for_spec)
        .or_else(|| skipped_remote_checksums.get(&name).copied());
    let new_checksum = checksum_str_to_u32(&envelope.checksum);
    let data = validate_envelope_data("DynamicConfig", envelope.data)?;
    let pb_spec = pb::Spec::decode(data).map_err(|e| map_decode_err("DynamicConfig", e))?;

    if protobuf_spec_has_remote_metadata(&pb_spec) {
        // Only a producer-declared remote response is eligible for this
        // shared-cache omission. The worker hydrator also requires true.
        if remote_metadata_hint != Some(true) {
            return Err(unhydrated_remote_config_metadata_error());
        }
        // The full payload, including this omitted shared-cache entry, is
        // checked against the producer's field checksum envelope.
        next_specs.dynamic_configs.remove(&name);
        if let Some(checksum) = new_checksum {
            skipped_remote_checksums.insert(name, checksum);
        } else {
            skipped_remote_checksums.remove(&name);
        }
    } else {
        let spec = spec_from_pb(envelope.checksum, pb_spec)?;
        next_specs
            .dynamic_configs
            .insert(name.clone(), SpecPointer::from_spec(spec));
        skipped_remote_checksums.remove(&name);
    }
    field_checksums.replace_for_entity(
        pb::SpecsEnvelopeKind::DynamicConfig,
        old_checksum,
        new_checksum,
    );
    Ok(())
}

fn apply_entity_update(
    kind: pb::SpecsEnvelopeKind,
    envelope: pb::SpecsEnvelope,
    current_specs: &SpecsResponseFull,
    next_specs: &mut SpecsResponseFull,
    preserve_session_update_mode: bool,
    field_checksums: &mut SpecsFieldChecksums,
) -> Result<(), StatsigErr> {
    let name = InternedString::from_str_ref(&envelope.name);
    let old_checksum = entity_checksum(kind, next_specs, &name);
    let new_checksum = checksum_str_to_u32(&envelope.checksum);

    match kind {
        pb::SpecsEnvelopeKind::FeatureGate => next_specs.handle_feature_gate_update(
            envelope,
            current_specs,
            preserve_session_update_mode,
        ),
        pb::SpecsEnvelopeKind::DynamicConfig => next_specs.handle_dynamic_config_update(
            envelope,
            current_specs,
            preserve_session_update_mode,
        ),
        pb::SpecsEnvelopeKind::LayerConfig => next_specs.handle_layer_config_update(
            envelope,
            current_specs,
            preserve_session_update_mode,
        ),
        pb::SpecsEnvelopeKind::ParamStore => {
            next_specs.handle_param_store_update(envelope, current_specs)
        }
        pb::SpecsEnvelopeKind::Condition => {
            next_specs.handle_condition_update(envelope, current_specs)
        }
        _ => unreachable!(),
    }?;

    field_checksums.replace_for_entity(kind, old_checksum, new_checksum);
    Ok(())
}

fn entity_checksum(
    kind: pb::SpecsEnvelopeKind,
    specs: &SpecsResponseFull,
    name: &InternedString,
) -> Option<u32> {
    match kind {
        pb::SpecsEnvelopeKind::FeatureGate => {
            specs.feature_gates.get(name).and_then(checksum_for_spec)
        }
        pb::SpecsEnvelopeKind::DynamicConfig => {
            specs.dynamic_configs.get(name).and_then(checksum_for_spec)
        }
        pb::SpecsEnvelopeKind::LayerConfig => {
            specs.layer_configs.get(name).and_then(checksum_for_spec)
        }
        pb::SpecsEnvelopeKind::ParamStore => specs
            .param_stores
            .as_ref()
            .and_then(|stores| stores.get(name))
            .and_then(checksum_for_param_store),
        pb::SpecsEnvelopeKind::Condition => specs
            .condition_map
            .get(name)
            .and_then(checksum_for_condition),
        _ => unreachable!(),
    }
}

fn record_entity_checksum_update(
    kind: pb::SpecsEnvelopeKind,
    specs: &SpecsResponseFull,
    field_checksums: &mut SpecsFieldChecksums,
    name: &InternedString,
    old_checksum: Option<u32>,
) {
    let new_checksum = entity_checksum(kind, specs, name);
    field_checksums.replace_for_entity(kind, old_checksum, new_checksum);
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
    fn handle_top_level_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
    ) -> Result<Option<bool>, StatsigErr> {
        let envelope_data = validate_envelope_data("TopLevel", envelope.data)?;
        let top_level = pb::SpecsTopLevel::decode(envelope_data)
            .map_err(|e| map_decode_err("SpecsTopLevel", e))?;

        let may_have_remote_config_metadata = top_level.may_have_remote_config_metadata;

        self.populate_top_level_from_envelope(top_level)?;

        Ok(may_have_remote_config_metadata)
    }

    fn handle_feature_gate_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
        preserve_session_update_mode: bool,
    ) -> Result<(), StatsigErr> {
        Self::handle_individual_spec_update(
            "FeatureGate",
            envelope,
            &existing.feature_gates,
            &mut self.feature_gates,
            InternedStore::try_get_preloaded_feature_gate,
            preserve_session_update_mode,
        )
    }

    fn handle_dynamic_config_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
        preserve_session_update_mode: bool,
    ) -> Result<(), StatsigErr> {
        Self::handle_individual_spec_update(
            "DynamicConfig",
            envelope,
            &existing.dynamic_configs,
            &mut self.dynamic_configs,
            InternedStore::try_get_preloaded_dynamic_config,
            preserve_session_update_mode,
        )
    }

    /// Return a matching mmap/current pointer without mutating next_specs; the
    /// bounded async parser queue publishes it later in envelope order. Callers
    /// still decode responses that advertise remote metadata because an older
    /// artifact with the same checksum may contain a placeholder.
    fn find_reusable_dynamic_config_update(
        &self,
        envelope: &pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
    ) -> Option<(InternedString, SpecPointer)> {
        let name = InternedString::from_string(envelope.name.clone());

        if let Some(preloaded) = InternedStore::try_get_preloaded_dynamic_config(&name) {
            if preloaded.view().checksum().map(|value| value.as_str())
                == Some(envelope.checksum.as_str())
            {
                return Some((name, preloaded));
            }
        }

        if let Some(spec_ptr) = existing.dynamic_configs.get(&name) {
            if spec_ptr.view().checksum().map(|value| value.as_str())
                == Some(envelope.checksum.as_str())
            {
                return Some((name, spec_ptr.clone()));
            }
        }

        None
    }

    fn insert_reused_dynamic_config_update(
        &mut self,
        name: InternedString,
        spec_pointer: SpecPointer,
    ) {
        self.dynamic_configs.insert(name, spec_pointer);
    }

    fn handle_decoded_dynamic_config_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        spec: pb::Spec,
    ) -> Result<(), StatsigErr> {
        let name = InternedString::from_string(envelope.name);
        let spec = spec_from_pb(envelope.checksum, spec)?;
        self.insert_owned_dynamic_config_update(name, spec);
        Ok(())
    }

    fn insert_owned_dynamic_config_update(&mut self, name: InternedString, spec: Spec) {
        self.dynamic_configs
            .insert(name, SpecPointer::from_spec(spec));
    }

    fn handle_layer_config_update(
        &mut self,
        envelope: pb::SpecsEnvelope,
        existing: &SpecsResponseFull,
        preserve_session_update_mode: bool,
    ) -> Result<(), StatsigErr> {
        Self::handle_individual_spec_update(
            "LayerConfig",
            envelope,
            &existing.layer_configs,
            &mut self.layer_configs,
            InternedStore::try_get_preloaded_layer_config,
            preserve_session_update_mode,
        )
    }

    fn handle_individual_spec_update(
        tag: &str,
        envelope: pb::SpecsEnvelope,
        exiting_map: &SpecsHashMap,
        new_map: &mut SpecsHashMap,
        preload_fetcher: fn(&InternedString) -> Option<SpecPointer>,
        preserve_session_update_mode: bool,
    ) -> Result<(), StatsigErr> {
        if preserve_session_update_mode {
            return Self::handle_individual_spec_update_preserving_session_update_mode(
                tag,
                envelope,
                exiting_map,
                new_map,
                preload_fetcher,
            );
        }

        let name = InternedString::from_string(envelope.name);

        let mut preloaded = preload_fetcher(&name);
        if let Some(spec) = &preloaded {
            match spec.view().checksum().map(|value| value.as_str()) {
                Some(existing_checksum) if existing_checksum == envelope.checksum => {
                    new_map.insert(name, preloaded.expect("preloaded spec must exist"));
                    return Ok(());
                }
                Some(_) | None => preloaded = None,
            }
        }

        if let Some(spec_ptr) = exiting_map.get(&name) {
            if spec_ptr.view().checksum().map(|value| value.as_str())
                == Some(envelope.checksum.as_str())
            {
                new_map.insert(name, spec_ptr.clone());
                return Ok(());
            }
        }

        let envelope_data = validate_envelope_data(tag, envelope.data)?;
        let pb_spec = pb::Spec::decode(envelope_data).map_err(|e| map_decode_err(tag, e))?;
        let spec = spec_from_pb(envelope.checksum, pb_spec)?;
        debug_assert!(preloaded.is_none());
        new_map.insert(name, SpecPointer::from_spec(spec));

        Ok(())
    }

    fn handle_individual_spec_update_preserving_session_update_mode(
        tag: &str,
        envelope: pb::SpecsEnvelope,
        exiting_map: &SpecsHashMap,
        new_map: &mut SpecsHashMap,
        preload_fetcher: fn(&InternedString) -> Option<SpecPointer>,
    ) -> Result<(), StatsigErr> {
        let name = InternedString::from_string(envelope.name);
        let checksum = envelope.checksum;
        let envelope_data = validate_envelope_data(tag, envelope.data)?;
        let preloaded = preload_fetcher(&name).filter(|spec| {
            spec.view().checksum().map(|value| value.as_str()) == Some(checksum.as_str())
        });
        let existing = exiting_map.get(&name).filter(|spec| {
            spec.view().checksum().map(|value| value.as_str()) == Some(checksum.as_str())
        });

        if preloaded.is_some() || existing.is_some() {
            let session_update_mode = decode_session_update_mode(envelope_data.get_ref())
                .map_err(|e| map_decode_err(tag, e))?;

            if let Some(spec) = preloaded
                .as_ref()
                .and_then(|spec| spec.with_session_update_mode(session_update_mode.as_deref()))
            {
                new_map.insert(name, spec);
                return Ok(());
            }

            if let Some(spec) = existing
                .and_then(|spec| spec.with_session_update_mode(session_update_mode.as_deref()))
            {
                new_map.insert(name, spec);
                return Ok(());
            }
        }

        let pb_spec = pb::Spec::decode(envelope_data).map_err(|e| map_decode_err(tag, e))?;
        let spec = spec_from_pb(checksum, pb_spec)?;
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

    fn apply_deletions(
        &mut self,
        deletions: pb::RulesetsResponseDeletions,
        field_checksums: &mut SpecsFieldChecksums,
    ) {
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

        remove_interned_from_specs_map(
            &mut self.dynamic_configs,
            dynamic_configs,
            &mut field_checksums.dynamic_configs,
        );
        remove_interned_from_specs_map(
            &mut self.feature_gates,
            feature_gates,
            &mut field_checksums.feature_gates,
        );
        remove_interned_from_specs_map(
            &mut self.layer_configs,
            layer_configs,
            &mut field_checksums.layer_configs,
        );
        remove_string_from_map(&mut self.experiment_to_layer, experiment_to_layer);
        remove_conditions(
            &mut self.condition_map,
            condition_map,
            &mut field_checksums.condition_map,
        );
        remove_string_from_opt_map(&mut self.sdk_configs, sdk_configs);
        remove_param_stores(
            &mut self.param_stores,
            param_stores,
            &mut field_checksums.param_stores,
        );
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

fn remove_interned_from_specs_map(map: &mut SpecsHashMap, names: Vec<String>, checksum: &mut u64) {
    for name in names {
        if let Some(removed) = map.remove(&InternedString::from_string(name)) {
            replace_checksum(checksum, checksum_for_spec(&removed), None);
        }
    }
}

fn remove_conditions<S: std::hash::BuildHasher>(
    map: &mut HashMap<InternedString, Condition, S>,
    names: Vec<String>,
    checksum: &mut u64,
) {
    for name in names {
        if let Some(removed) = map.remove(&InternedString::from_string(name)) {
            replace_checksum(checksum, checksum_for_condition(&removed), None);
        }
    }
}

fn remove_string_from_map<V>(map: &mut HashMap<String, V>, names: Vec<String>) {
    for name in names {
        map.remove(&name);
    }
}

fn remove_param_stores(
    map: &mut Option<HashMap<InternedString, ParameterStore>>,
    names: Vec<String>,
    checksum: &mut u64,
) {
    let Some(map) = map.as_mut() else {
        return;
    };
    for name in names {
        if let Some(removed) = map.remove(&InternedString::from_string(name)) {
            replace_checksum(checksum, checksum_for_param_store(&removed), None);
        }
    }
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

fn replace_checksum(total: &mut u64, old_checksum: Option<u32>, new_checksum: Option<u32>) {
    *total = total
        .wrapping_sub(old_checksum.unwrap_or_default() as u64)
        .wrapping_add(new_checksum.unwrap_or_default() as u64);
}

fn checksum_for_condition(condition: &Condition) -> Option<u32> {
    checksum_to_u32(condition.checksum.as_ref())
}

fn checksum_for_spec(pointer: &SpecPointer) -> Option<u32> {
    pointer
        .view()
        .checksum()
        .and_then(|checksum| checksum.as_str().parse::<u32>().ok())
}

fn checksum_for_param_store(store: &ParameterStore) -> Option<u32> {
    checksum_to_u32(store.checksum.as_ref())
}

fn checksum_to_u32(checksum: Option<&InternedString>) -> Option<u32> {
    checksum.and_then(|value| checksum_str_to_u32(value.as_str()))
}

#[inline]
fn checksum_str_to_u32(checksum: &str) -> Option<u32> {
    checksum.parse::<u32>().ok()
}

fn validate_envelope_data<T: AsRef<[u8]>>(
    envelope_tag: &str,
    data: Option<T>,
) -> Result<Cursor<T>, StatsigErr> {
    match data {
        Some(data) => Ok(Cursor::new(data)),
        None => Err(StatsigErr::ProtobufParseError(
            "SpecsEnvelope".to_string(),
            format!("No data in {} envelope", envelope_tag),
        )),
    }
}

fn decode_session_update_mode(data: &[u8]) -> Result<Option<String>, prost::DecodeError> {
    SessionUpdateModeField::decode(data).map(|spec| spec.session_update_mode)
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
        pb::ConditionType::ExperimentGroup => Ok(interned_str!("experiment_group")),
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
    if spec.remote_config_metadata.is_some()
        || spec
            .rules
            .iter()
            .any(|rule| rule.remote_config_metadata.is_some())
    {
        return Err(unhydrated_remote_config_metadata_error());
    }

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
        session_update_mode: spec.session_update_mode.map(InternedString::from_string),
    };

    Ok(spec)
}

fn unhydrated_remote_config_metadata_error() -> StatsigErr {
    StatsigErr::ProtobufParseError(
        UNHYDRATED_REMOTE_CONFIG_METADATA_TAG.to_string(),
        UNHYDRATED_REMOTE_CONFIG_METADATA_MESSAGE.to_string(),
    )
}

fn is_unhydrated_remote_config_metadata_error(error: &StatsigErr) -> bool {
    matches!(
        error,
        StatsigErr::ProtobufParseError(tag, message)
            if tag == UNHYDRATED_REMOTE_CONFIG_METADATA_TAG
                && message == UNHYDRATED_REMOTE_CONFIG_METADATA_MESSAGE
    )
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
                shared_control_experiments: (!pb_rule.shared_control_experiments.is_empty()).then(
                    || {
                        pb_rule
                            .shared_control_experiments
                            .into_iter()
                            .map(shared_control_exp_from_pb)
                            .collect::<Vec<_>>()
                            .into()
                    },
                ),
            };

            Ok(rule)
        })
        .collect::<Result<Vec<Rule>, StatsigErr>>()
}

fn shared_control_exp_from_pb(experiment: pb::SharedControlExperiment) -> SharedControlExperiment {
    SharedControlExperiment {
        name: InternedString::from_string(experiment.name),
        control_group_id: InternedString::from_string(experiment.control_group_id),
    }
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
            ));
        }
    };

    let bytes = match return_value {
        pb::return_value::Value::BoolValue(value) => {
            return Ok(DynamicReturnable::from_bool(value));
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
            });
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
#[path = "__tests__/proto_specs_tests.rs"]
mod tests;
