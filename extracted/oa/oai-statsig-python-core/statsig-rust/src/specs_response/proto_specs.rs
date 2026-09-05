use std::{
    collections::HashMap,
    io::{Cursor, Write},
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
        specs_hash_map::{SpecDecodeStats, SpecPointer, SpecsHashMap, seed_spec_decode_stats},
        statsig_config_specs::{self as pb, any_value},
    },
};

use crate::specs_adapter::remote_config_value_hydrator::{
    ProtobufHydrationSession, RemoteConfigValueHydrator,
    protobuf_top_level_has_hydrated_sidecar_provenance,
    remote_metadata_marker_without_metadata_error, rewrite_decoded_dynamic_config_envelope,
    rewrite_top_level_envelope,
};

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
    Materialized { is_delta: bool },
    CursorOnly { lcut: u64, checksum: String },
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
                brotli::CompressorWriter::new(Vec::new(), BUFFER_SIZE, 5, 22),
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
///
/// Keeping this state together makes the queueing helpers describe only the
/// envelope they are handling; the parser still owns `data_store_capture`
/// separately because that writer spans every envelope in the response.
struct PendingEntityParserContext<'a, 'h> {
    ops_stats: &'a OpsStatsForInstance,
    current_specs: &'a SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
    next_specs: &'a mut SpecsResponseFull,
    state: ParseState,
    remote_metadata_hint: Option<bool>,
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
        context.remote_metadata_hint != Some(true)
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
        previous_spec_decode_stats: SpecDecodeStats,
    ) {
        if *self == Self::DeltaDeferred {
            seed_spec_decode_stats(previous_spec_decode_stats);
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
        deserialize_protobuf_for_store(
            ops_stats,
            current_specs,
            SpecDecodeStats::default(),
            next_specs,
            data,
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
    if !options.should_preserve_session_update_mode() {
        return deserialize_protobuf(ops_stats, current_specs, next_specs, data);
    }

    if matches!(
        deserialize_protobuf_for_store_with_options(
            ops_stats,
            current_specs,
            SpecDecodeStats::default(),
            next_specs,
            data,
            true,
        )?,
        ProtobufUpdate::CursorOnly { .. }
    ) {
        next_specs.copy_previous_values_from(current_specs);
    }

    Ok(())
}

pub(crate) fn deserialize_protobuf_for_store(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull, /* Intentionally immutable so we can continue using it if parsing fails */
    previous_spec_decode_stats: SpecDecodeStats,
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
) -> Result<ProtobufUpdate, StatsigErr> {
    deserialize_protobuf_for_store_with_options(
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        next_specs,
        data,
        false,
    )
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
    let mut hydration = context
        .hydrator
        .begin_protobuf_hydration(context.source_url);
    let result = deserialize_protobuf_for_store_with_hydration_inner(
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        next_specs,
        data,
        &mut hydration,
        context,
    )
    .await;
    hydration.finish(result.is_ok());
    result
}

async fn deserialize_protobuf_for_store_with_hydration_inner(
    ops_stats: &OpsStatsForInstance,
    current_specs: &SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
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
    let mut parsed_envelopes_count = 0;
    let mut data_store_capture: Option<HydratedProtobufDataStoreCapture> = None;
    let mut pending_entity_batch = PendingEntityBatch::default();
    let data_store_compression =
        ProtoCompression::from_response(data).unwrap_or(ProtoCompression::Brotli);

    if !next_specs.is_empty() {
        return Err(StatsigErr::ProtobufParseError(
            "SpecsResponseFull".to_string(),
            "Next specs are not empty".to_string(),
        ));
    }

    let mut parser_context = PendingEntityParserContext {
        ops_stats,
        current_specs,
        previous_spec_decode_stats,
        next_specs,
        state: ParseState::Initial,
        remote_metadata_hint: None,
        hydrated_sidecar_provenance: false,
        hydration,
        mmap_project_id,
        preserve_session_update_mode,
        spec_decode_stats: SpecDecodeStats::default(),
    };

    data.rewind()?;
    let mut reader = ProtoStreamReader::new_for_response(data)?;

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
            log_error_to_statsig_and_console!(parser_context.ops_stats, TAG, err);
            err
        })?;

        parsed_envelopes_count += 1;

        let env: pb::SpecsEnvelope =
            match prost::Message::decode_length_delimited(proto_msg_bytes.as_ref()) {
                Ok(env) => env,
                Err(e) => {
                    let err: StatsigErr = map_decode_err("SpecsEnvelope", e);
                    log_error_to_statsig_and_console!(parser_context.ops_stats, TAG, err);
                    if parser_context.state.is_delta() {
                        return Err(err);
                    }
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
                }
            };

        let envelope_kind = match pb::SpecsEnvelopeKind::try_from(env.kind) {
            Ok(kind) => kind,
            Err(e) => {
                let err: StatsigErr = map_unknown_enum_value("SpecsEnvelopeKind", e);
                log_error_to_statsig_and_console!(parser_context.ops_stats, TAG, err);
                if parser_context.state.is_delta() {
                    return Err(err);
                }
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
            }
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
                if parser_context.remote_metadata_hint == Some(true)
                    && !parser_context.hydration.saw_remote_metadata()
                {
                    return Err(remote_metadata_marker_without_metadata_error());
                }
                let update = parser_context.spec_decode_stats.with_mmap_project(
                    parser_context.mmap_project_id,
                    || {
                        finish_protobuf_update_at_done(
                            parser_context.current_specs,
                            parser_context.next_specs,
                            parser_context.previous_spec_decode_stats,
                            parser_context.state,
                        )
                    },
                )?;
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
                    && matches!(parser_context.state, ParseState::Initial | ParseState::Full))
                .then(|| rewrite_top_level_envelope(proto_msg_bytes.as_ref(), &env));

                match parser_context.state {
                    ParseState::Initial | ParseState::Full => {
                        let result = parser_context.spec_decode_stats.with_mmap_project(
                            parser_context.mmap_project_id,
                            || {
                                log_parse_result(
                                    parser_context.ops_stats,
                                    parser_context.next_specs.handle_top_level_update(env),
                                )
                            },
                        );
                        if let Ok(hint) = result {
                            parser_context.remote_metadata_hint = hint;
                            parser_context.hydrated_sidecar_provenance =
                                top_level_hydrated_sidecar_provenance;
                            parser_context.state = ParseState::Full;
                            if capture_hydrated_data_store_bytes && hint == Some(true) {
                                if data_store_capture.is_none() {
                                    data_store_capture =
                                        Some(HydratedProtobufDataStoreCapture::new(
                                            data_store_compression,
                                        )?);
                                }
                                data_store_frame = Some(
                                    rewritten_top_level
                                        .expect("full top-level capture was prepared")?,
                                );
                            }
                        }
                    }
                    ParseState::DeltaAwaitingTopLevel => {
                        parser_context.remote_metadata_hint = parser_context
                            .spec_decode_stats
                            .with_mmap_project(parser_context.mmap_project_id, || {
                                log_parse_result(
                                    parser_context.ops_stats,
                                    parser_context.next_specs.handle_top_level_update(env),
                                )
                            })?;
                        parser_context.hydrated_sidecar_provenance =
                            top_level_hydrated_sidecar_provenance;
                        parser_context.state = ParseState::DeltaDeferred;
                    }
                    _ => {
                        return make_proto_parse_error(
                            "SpecsEnvelope",
                            "Unexpected top-level envelope in delta response",
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
            pb::SpecsEnvelopeKind::Deletions => match parser_context.state {
                ParseState::Full => {
                    let result = parser_context
                        .spec_decode_stats
                        .with_mmap_project(parser_context.mmap_project_id, || {
                            log_parse_result(parser_context.ops_stats, decode_deletions_update(env))
                        });
                    if let Ok(deletions) = result {
                        parser_context
                            .spec_decode_stats
                            .with_mmap_project(parser_context.mmap_project_id, || {
                                parser_context.next_specs.apply_deletions(deletions)
                            });
                    }
                }
                ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
                    let deletions = parser_context
                        .spec_decode_stats
                        .with_mmap_project(parser_context.mmap_project_id, || {
                            log_parse_result(parser_context.ops_stats, decode_deletions_update(env))
                        })?;
                    if !deletions_are_empty(&deletions) {
                        parser_context.spec_decode_stats.with_mmap_project(
                            parser_context.mmap_project_id,
                            || {
                                parser_context.state.materialize(
                                    parser_context.current_specs,
                                    parser_context.next_specs,
                                    parser_context.previous_spec_decode_stats,
                                );
                                parser_context.next_specs.apply_deletions(deletions);
                            },
                        );
                    }
                }
                _ => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Unexpected deletions envelope",
                    );
                }
            },
            pb::SpecsEnvelopeKind::Checksums => {
                let (target, next_state): (&SpecsResponseFull, ParseState) =
                    match parser_context.state {
                        ParseState::Full => (parser_context.next_specs, ParseState::Full),
                        ParseState::DeltaDeferred => (
                            parser_context.current_specs,
                            ParseState::DeltaDeferredValidated,
                        ),
                        ParseState::DeltaMaterialized => (
                            parser_context.next_specs,
                            ParseState::DeltaMaterializedValidated,
                        ),
                        _ => {
                            return make_proto_parse_error(
                                "SpecsEnvelope",
                                "Unexpected checksums envelope",
                            );
                        }
                    };

                let checksum_result = parser_context
                    .spec_decode_stats
                    .with_mmap_project(parser_context.mmap_project_id, || {
                        target.handle_checksums_update(env)
                    });
                match checksum_result {
                    Ok(()) => {
                        parser_context.state = next_state;
                        parser_context
                            .ops_stats
                            .log_checksum_validation_result(true);
                    }
                    Err(e) => {
                        parser_context
                            .ops_stats
                            .log_checksum_validation_result(false);
                        return Err(StatsigErr::ChecksumFailure(format!(
                            "Failed to apply protobuf checksums update: {e}"
                        )));
                    }
                }
            }
            pb::SpecsEnvelopeKind::CopyPrev => {
                if parser_context.state != ParseState::Initial || parsed_envelopes_count != 1 {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Duplicate or misplaced copy-prev envelope",
                    );
                }
                parser_context.state = ParseState::DeltaAwaitingTopLevel;
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
    let tolerates_malformed_entity = prepare_entity_update_state(context)?;
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
                .next_specs
                .find_reusable_dynamic_config_update(&envelope, context.current_specs)
        });
    // Hydrated sidecars decode as marker=false after their metadata is
    // stripped, but retain a true-then-false marker history. Their envelope
    // checksum is still the producer checksum, so checksum alone cannot prove
    // that an older mmap pointer contains the hydrated value.
    let reused = match reused {
        Some((name, spec_pointer))
            if !capture_hydrated_frame
                && context.remote_metadata_hint != Some(true)
                && !context.hydrated_sidecar_provenance =>
        {
            return Ok(Some(PendingEntityUpdate::Dynamic(Box::new(
                PendingDynamicConfigUpdate::Reused { name, spec_pointer },
            ))));
        }
        reused => reused,
    };

    let envelope_data = match validate_envelope_data("DynamicConfig", envelope.data.clone()) {
        Ok(data) => data,
        Err(error) => {
            finish_entity_parse_result(context.ops_stats, Err(error), tolerates_malformed_entity)?;
            return Ok(None);
        }
    };
    let spec = match pb::Spec::decode(envelope_data) {
        Ok(spec) => spec,
        Err(error) => {
            finish_entity_parse_result(
                context.ops_stats,
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
        // Remote hydration is an explicit producer opt-in. A missing or false
        // top-level marker must not make a markerless response hydrate.
        if context.remote_metadata_hint != Some(true) {
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

fn prepare_entity_update_state(
    context: &mut PendingEntityParserContext<'_, '_>,
) -> Result<bool, StatsigErr> {
    let tolerates_malformed_entity = match context.state {
        ParseState::Full => true,
        ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
            context
                .spec_decode_stats
                .with_mmap_project(context.mmap_project_id, || {
                    context.state.materialize(
                        context.current_specs,
                        context.next_specs,
                        context.previous_spec_decode_stats,
                    );
                });
            false
        }
        ParseState::Initial | ParseState::DeltaAwaitingTopLevel => {
            return make_proto_parse_error(
                "SpecsEnvelope",
                "Entity envelope before top-level envelope",
            );
        }
        ParseState::DeltaDeferredValidated | ParseState::DeltaMaterializedValidated => {
            return make_proto_parse_error(
                "SpecsEnvelope",
                "Unexpected entity envelope after delta checksums",
            );
        }
    };
    Ok(tolerates_malformed_entity)
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
                                context.current_specs,
                                context.next_specs,
                                context.preserve_session_update_mode,
                            )
                        });
                finish_entity_parse_result(context.ops_stats, result, tolerates_malformed_entity)?;
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
                    context
                        .spec_decode_stats
                        .with_mmap_project(context.mmap_project_id, || {
                            context
                                .next_specs
                                .insert_reused_dynamic_config_update(name, spec_pointer);
                        });
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
                        if verify_reused_against_decoded {
                            let decoded_spec = spec_from_pb(envelope.checksum, spec)?;
                            if spec_pointer.matches_owned_spec(&decoded_spec) {
                                context.spec_decode_stats.with_mmap_project(
                                    context.mmap_project_id,
                                    || {
                                        context.next_specs.insert_reused_dynamic_config_update(
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
                                        .next_specs
                                        .insert_reused_dynamic_config_update(name, spec_pointer);
                                },
                            );
                        }
                    } else {
                        let result = context.spec_decode_stats.with_mmap_project(
                            context.mmap_project_id,
                            || {
                                context
                                    .next_specs
                                    .handle_decoded_dynamic_config_update(envelope, spec)
                            },
                        );
                        finish_entity_parse_result(
                            context.ops_stats,
                            result,
                            tolerates_malformed_entity,
                        )?;
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

fn finish_protobuf_update_at_done(
    current_specs: &SpecsResponseFull,
    next_specs: &mut SpecsResponseFull,
    previous_spec_decode_stats: SpecDecodeStats,
    state: ParseState,
) -> Result<ProtobufUpdate, StatsigErr> {
    match state {
        ParseState::Full => Ok(ProtobufUpdate::Materialized { is_delta: false }),
        ParseState::DeltaMaterializedValidated => {
            Ok(ProtobufUpdate::Materialized { is_delta: true })
        }
        ParseState::DeltaDeferredValidated => {
            if next_specs.has_same_semantic_values_as(current_specs) && next_specs.time > 0 {
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

            seed_spec_decode_stats(previous_spec_decode_stats);
            next_specs.copy_previous_values_from(current_specs);
            Ok(ProtobufUpdate::Materialized { is_delta: true })
        }
        ParseState::Initial | ParseState::DeltaAwaitingTopLevel => {
            make_proto_parse_error("SpecsEnvelope", "Missing top-level envelope")
        }
        ParseState::DeltaDeferred | ParseState::DeltaMaterialized => make_proto_parse_error(
            "SpecsEnvelope",
            "Missing checksums envelope for delta response",
        ),
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
    next_specs: &mut SpecsResponseFull,
    data: &mut ResponseData,
    preserve_session_update_mode: bool,
) -> Result<ProtobufUpdate, StatsigErr> {
    let mut parsed_envelopes_count = 0;
    let mut state = ParseState::Initial;

    let mut reader = ProtoStreamReader::new_for_response(data)?;

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
            pb::SpecsEnvelopeKind::Done => {
                return finish_protobuf_update_at_done(
                    current_specs,
                    next_specs,
                    previous_spec_decode_stats,
                    state,
                );
            }
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
                    );
                }
            },
            kind @ (pb::SpecsEnvelopeKind::FeatureGate
            | pb::SpecsEnvelopeKind::DynamicConfig
            | pb::SpecsEnvelopeKind::LayerConfig
            | pb::SpecsEnvelopeKind::ParamStore
            | pb::SpecsEnvelopeKind::Condition) => match state {
                ParseState::Full => {
                    if let Err(error) = log_parse_result(
                        ops_stats,
                        apply_entity_update(
                            kind,
                            env,
                            current_specs,
                            next_specs,
                            preserve_session_update_mode,
                        ),
                    ) {
                        // Full protobuf responses intentionally tolerate malformed
                        // individual entities for backwards compatibility. Remote
                        // metadata is different: continuing would publish a
                        // placeholder URL as the config value when hydration was
                        // skipped, so make this one decoder error response-fatal.
                        if is_unhydrated_remote_config_metadata_error(&error) {
                            return Err(error);
                        }
                    }
                }
                ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
                    state.materialize(current_specs, next_specs, previous_spec_decode_stats);
                    log_parse_result(
                        ops_stats,
                        apply_entity_update(
                            kind,
                            env,
                            current_specs,
                            next_specs,
                            preserve_session_update_mode,
                        ),
                    )?;
                }
                ParseState::Initial | ParseState::DeltaAwaitingTopLevel => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Entity envelope before top-level envelope",
                    );
                }
                ParseState::DeltaDeferredValidated | ParseState::DeltaMaterializedValidated => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Unexpected entity envelope after delta checksums",
                    );
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
                        state.materialize(current_specs, next_specs, previous_spec_decode_stats);
                        next_specs.apply_deletions(deletions);
                    }
                }
                _ => {
                    return make_proto_parse_error(
                        "SpecsEnvelope",
                        "Unexpected deletions envelope",
                    );
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
                        );
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
    preserve_session_update_mode: bool,
) -> Result<(), StatsigErr> {
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
    pointer
        .view()
        .checksum()
        .and_then(|checksum| checksum.as_str().parse::<u32>().ok())
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
mod tests {
    use std::{
        collections::HashMap,
        io::{Read, Write},
        sync::Arc,
    };

    use brotli::enc::BrotliEncoderParams;
    use prost::Message;

    use super::{
        HydratedProtobufDataStoreCapture, ProtobufUpdate, SpecDecodeStats, SpecsResponseFull,
        checksum_for_condition, checksum_for_param_store, checksum_for_spec, condition_from_pb,
        deserialize_protobuf, deserialize_protobuf_for_store, deserialize_protobuf_with_options,
        pb, rules_from_pb, spec_from_pb, sum_checksums,
    };
    use crate::{
        interned_string::InternedString,
        networking::ResponseData,
        observability::ops_stats::OpsStatsForInstance,
        specs_response::{
            parse_options::SpecsResponseParseOptions,
            proto_compression::ProtoCompression,
            proto_stream_reader::BUFFER_SIZE,
            spec_types::{ConditionOperator, ConditionType},
            specs_hash_map::{SpecPointer, SpecsHashMap},
        },
    };

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

        let result =
            deserialize_protobuf(&OpsStatsForInstance::new(), &current, &mut next, &mut data);

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
            serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
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
            SpecDecodeStats::default(),
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
}
