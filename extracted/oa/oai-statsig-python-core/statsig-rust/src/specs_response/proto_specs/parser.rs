use std::io::Read;

use bytes::Bytes;
use prost::Message;

use crate::{
    StatsigErr, log_error_to_statsig_and_console,
    observability::{ops_stats::OpsStatsForInstance, sdk_errors_observer::ErrorBoundaryEvent},
    specs_response::{
        proto_stream_reader::ProtoStreamReader,
        spec_types::SpecsResponseFull,
        specs_hash_map::{SpecDecodeStats, seed_spec_decode_stats},
        statsig_config_specs as pb,
    },
};

use super::{
    ProtobufUpdate, SpecsFieldChecksums, TAG, decode_deletions_update, deletions_are_empty,
    log_parse_result, make_proto_parse_error, map_decode_err, map_unknown_enum_value,
};

/// Protocol state shared by the synchronous and hydrating parsers. Methods are
/// synchronous so callers can scope mmap accounting without crossing an await.
pub(super) struct ProtobufParser<'a> {
    pub(super) ops_stats: &'a OpsStatsForInstance,
    pub(super) current_specs: &'a SpecsResponseFull,
    current_field_checksums: &'a SpecsFieldChecksums,
    previous_spec_decode_stats: SpecDecodeStats,
    pub(super) next_specs: &'a mut SpecsResponseFull,
    pub(super) next_field_checksums: SpecsFieldChecksums,
    state: ParseState,
    parsed_envelopes_count: usize,
    remote_metadata_hint: Option<bool>,
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

impl<'a> ProtobufParser<'a> {
    pub(super) fn new(
        ops_stats: &'a OpsStatsForInstance,
        current_specs: &'a SpecsResponseFull,
        previous_spec_decode_stats: SpecDecodeStats,
        current_field_checksums: &'a SpecsFieldChecksums,
        next_specs: &'a mut SpecsResponseFull,
    ) -> Result<Self, StatsigErr> {
        // The caller is responsible for resetting the candidate snapshot.
        if !next_specs.is_empty() {
            return Err(StatsigErr::ProtobufParseError(
                "SpecsResponseFull".to_string(),
                "Next specs are not empty".to_string(),
            ));
        }
        Ok(Self {
            ops_stats,
            current_specs,
            current_field_checksums,
            previous_spec_decode_stats,
            next_specs,
            next_field_checksums: SpecsFieldChecksums::default(),
            state: ParseState::Initial,
            parsed_envelopes_count: 0,
            remote_metadata_hint: None,
        })
    }

    pub(super) fn is_delta(&self) -> bool {
        self.state.is_delta()
    }

    pub(super) fn is_deferred_delta(&self) -> bool {
        self.state == ParseState::DeltaDeferred
    }

    pub(super) fn remote_metadata_hint(&self) -> Option<bool> {
        self.remote_metadata_hint
    }

    pub(super) fn read_frame<R: Read>(
        &mut self,
        reader: &mut ProtoStreamReader<'_, R>,
    ) -> Result<Bytes, StatsigErr> {
        let frame = reader.read_next_delimited_proto().map_err(|e| {
            let sample = reader.sample_current_buf();
            let parsed_envelopes_count = self.parsed_envelopes_count;
            let err = StatsigErr::ProtobufParseError(
                "SpecsEnvelope".to_string(),
                format!(
                    "Error reading next delimited proto: {e}
                    \n Previous Parsed Envelope Count: {parsed_envelopes_count}
                    \n Current Buffer Sample: {sample}"
                ),
            );
            log_error_to_statsig_and_console!(self.ops_stats, TAG, err);
            err
        })?;
        self.parsed_envelopes_count += 1;
        Ok(frame.freeze())
    }

    pub(super) fn decode_envelope(
        &self,
        frame: Bytes,
    ) -> Result<Option<(pb::SpecsEnvelopeKind, pb::SpecsEnvelope)>, StatsigErr> {
        let result = pb::SpecsEnvelope::decode_length_delimited(frame)
            .map_err(|e| map_decode_err("SpecsEnvelope", e))
            .and_then(|envelope| {
                pb::SpecsEnvelopeKind::try_from(envelope.kind)
                    .map(|kind| (kind, envelope))
                    .map_err(|e| map_unknown_enum_value("SpecsEnvelopeKind", e))
            });
        match log_parse_result(self.ops_stats, result) {
            Ok(envelope) => Ok(Some(envelope)),
            Err(error) if self.state.is_delta() => Err(error),
            Err(_) => Ok(None),
        }
    }

    /// Returns whether this top-level was accepted. A malformed full-response
    /// top-level is tolerated without changing the state or metadata hint.
    pub(super) fn handle_top_level(
        &mut self,
        envelope: pb::SpecsEnvelope,
    ) -> Result<bool, StatsigErr> {
        let next_state = match self.state {
            ParseState::Initial | ParseState::Full => ParseState::Full,
            ParseState::DeltaAwaitingTopLevel => ParseState::DeltaDeferred,
            _ => {
                return make_proto_parse_error(
                    "SpecsEnvelope",
                    "Unexpected top-level envelope in delta response",
                );
            }
        };
        match log_parse_result(
            self.ops_stats,
            self.next_specs.handle_top_level_update(envelope),
        ) {
            Ok(hint) => {
                self.remote_metadata_hint = hint;
                self.state = next_state;
                Ok(true)
            }
            Err(error) if self.state.is_delta() => Err(error),
            Err(_) => Ok(false),
        }
    }

    pub(super) fn prepare_entity_update(&mut self) -> Result<bool, StatsigErr> {
        match self.state {
            ParseState::Full => Ok(true),
            ParseState::DeltaDeferred | ParseState::DeltaMaterialized => {
                self.state.materialize(
                    self.current_specs,
                    self.next_specs,
                    self.previous_spec_decode_stats,
                );
                Ok(false)
            }
            ParseState::Initial | ParseState::DeltaAwaitingTopLevel => {
                make_proto_parse_error("SpecsEnvelope", "Entity envelope before top-level envelope")
            }
            ParseState::DeltaDeferredValidated | ParseState::DeltaMaterializedValidated => {
                make_proto_parse_error(
                    "SpecsEnvelope",
                    "Unexpected entity envelope after delta checksums",
                )
            }
        }
    }

    /// Return successfully applied dynamic-config deletions when requested;
    /// malformed full-response deletions and empty delta deletions return none.
    pub(super) fn handle_deletions(
        &mut self,
        envelope: pb::SpecsEnvelope,
        collect_dynamic_config_names: bool,
    ) -> Result<Option<Vec<String>>, StatsigErr> {
        let is_full = match self.state {
            ParseState::Full => true,
            ParseState::DeltaDeferred | ParseState::DeltaMaterialized => false,
            _ => return make_proto_parse_error("SpecsEnvelope", "Unexpected deletions envelope"),
        };
        let deletions = match log_parse_result(self.ops_stats, decode_deletions_update(envelope)) {
            Ok(deletions) => deletions,
            Err(_) if is_full => return Ok(None),
            Err(error) => return Err(error),
        };
        if !is_full && deletions_are_empty(&deletions) {
            return Ok(None);
        }
        if !is_full {
            self.state.materialize(
                self.current_specs,
                self.next_specs,
                self.previous_spec_decode_stats,
            );
        }
        let deleted_dynamic_configs =
            collect_dynamic_config_names.then(|| deletions.dynamic_configs.clone());
        self.next_specs
            .apply_deletions(deletions, &mut self.next_field_checksums);
        Ok(deleted_dynamic_configs)
    }

    pub(super) fn handle_checksums(
        &mut self,
        envelope: pb::SpecsEnvelope,
    ) -> Result<(), StatsigErr> {
        let (checksums, next_state) = match self.state {
            ParseState::Full => (&self.next_field_checksums, ParseState::Full),
            ParseState::DeltaDeferred => (
                self.current_field_checksums,
                ParseState::DeltaDeferredValidated,
            ),
            ParseState::DeltaMaterialized => (
                &self.next_field_checksums,
                ParseState::DeltaMaterializedValidated,
            ),
            _ => return make_proto_parse_error("SpecsEnvelope", "Unexpected checksums envelope"),
        };
        match checksums.validate_envelope(envelope) {
            Ok(()) => {
                self.state = next_state;
                self.ops_stats.log_checksum_validation_result(true);
                Ok(())
            }
            Err(e) => {
                self.ops_stats.log_checksum_validation_result(false);
                Err(StatsigErr::ChecksumFailure(format!(
                    "Failed to apply protobuf checksums update: {e}"
                )))
            }
        }
    }

    pub(super) fn handle_copy_prev(&mut self) -> Result<(), StatsigErr> {
        if self.state != ParseState::Initial || self.parsed_envelopes_count != 1 {
            return make_proto_parse_error(
                "SpecsEnvelope",
                "Duplicate or misplaced copy-prev envelope",
            );
        }
        self.next_field_checksums = *self.current_field_checksums;
        self.state = ParseState::DeltaAwaitingTopLevel;
        Ok(())
    }

    pub(super) fn finish(self) -> Result<ProtobufUpdate, StatsigErr> {
        match self.state {
            ParseState::Full => Ok(ProtobufUpdate::Materialized {
                field_checksums: self.next_field_checksums,
                is_delta: false,
            }),
            ParseState::DeltaMaterializedValidated => Ok(ProtobufUpdate::Materialized {
                field_checksums: self.next_field_checksums,
                is_delta: true,
            }),
            ParseState::DeltaDeferredValidated => {
                if self
                    .next_specs
                    .has_same_semantic_values_as(self.current_specs)
                    && self.next_specs.time > 0
                {
                    if let Some(checksum) = self
                        .next_specs
                        .checksum
                        .as_ref()
                        .filter(|checksum| !checksum.is_empty())
                    {
                        return Ok(ProtobufUpdate::CursorOnly {
                            lcut: self.next_specs.time,
                            checksum: checksum.clone(),
                        });
                    }
                }

                seed_spec_decode_stats(self.previous_spec_decode_stats);
                self.next_specs
                    .copy_previous_values_from(self.current_specs);
                Ok(ProtobufUpdate::Materialized {
                    field_checksums: self.next_field_checksums,
                    is_delta: true,
                })
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
}
