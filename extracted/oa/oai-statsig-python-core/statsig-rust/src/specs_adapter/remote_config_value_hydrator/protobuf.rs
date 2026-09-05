use std::collections::{HashMap, HashSet, VecDeque};
use std::sync::Arc;
use std::time::Instant;

use bytes::Buf;
use futures::{FutureExt, StreamExt, future::BoxFuture, stream::FuturesUnordered};
use prost::Message;
use serde_json::value::RawValue;
use tokio::sync::OwnedSemaphorePermit;
use tokio::time::timeout;

#[cfg(test)]
use std::io::Write;

use crate::StatsigErr;
use crate::networking::ResponseData;
use crate::specs_response::proto_stream_reader::ProtoStreamReader;
use crate::specs_response::statsig_config_specs::{self as pb, return_value};

use super::{
    DOWNLOAD_CONCURRENCY, HYDRATION_TIMEOUT, HydrationFailureReason, HydrationOutcome,
    RemoteConfigValueHydrator, RemoteConfigValueMetadata, RemoteConfigValueMetadataWire,
    RemoteValueReference, TAG, add_raw_value_reference, hydrated_value, hydration_error,
    insert_reference, total_timeout_error, validate_reference_limits,
};

const REMOTE_METADATA_MARKER_WITHOUT_METADATA_TAG: &str = "proto::RemoteConfigMetadata";
const REMOTE_METADATA_MARKER_WITHOUT_METADATA_MESSAGE: &str =
    "Top-level remote config metadata marker was true, but no metadata was found";

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum ProtobufResponseMode {
    Full,
    Delta,
}

impl ProtobufResponseMode {
    const fn tolerates_malformed_entities(self) -> bool {
        matches!(self, Self::Full)
    }
}

type RemoteValueDownload<'a> = BoxFuture<'a, Result<(String, Arc<Vec<u8>>), StatsigErr>>;

/// Tracks one protobuf store update while the parser pauses only at dynamic
/// config envelopes that actually reference remote values. Keeping the budget
/// here preserves the per-response concurrency window even though downloads
/// happen at the envelope boundary instead of in a second response-wide scan.
pub(crate) struct ProtobufHydrationSession<'a> {
    hydrator: &'a RemoteConfigValueHydrator,
    source_url: &'a str,
    started_at: Instant,
    references: HashMap<String, RemoteValueReference>,
    // Keep verified bodies only until this update finishes. This preserves
    // same-response SHA deduplication without retaining worker-private blobs
    // for the lifetime of the adapter.
    hydrated_values: HashMap<String, Arc<Vec<u8>>>,
    // Keep the download fanout warm while the parser continues reading entity
    // envelopes. Unlike a batch-wide await, a completed request immediately
    // opens a slot for the next discovered SHA.
    in_flight_downloads: FuturesUnordered<RemoteValueDownload<'a>>,
    in_flight_sha256: HashSet<String>,
    // Charge only discovered bytes. If later metadata cannot immediately
    // extend the base reservation, one separate expansion permit guarantees
    // enough space for the remainder of the response's concurrency window.
    response_budget: Option<OwnedSemaphorePermit>,
    response_expansion_budget: Option<OwnedSemaphorePermit>,
    reference_count: usize,
    total_bytes: u64,
    saw_remote_metadata: bool,
}

struct PreparedProtobufStream {
    bytes: Vec<u8>,
    reference_count: usize,
    total_bytes: u64,
    _response_budget: OwnedSemaphorePermit,
}

enum PreparedProtobufEnvelope {
    Bytes(Vec<u8>),
    RemoteDynamicConfig {
        encoded: Vec<u8>,
        spec_data: Vec<u8>,
        spec: Box<pb::Spec>,
    },
}

// Project only these tags while hydrating an explicitly opted-in protobuf
// response, avoiding decode work for large inline return values.
#[derive(Clone, PartialEq, prost::Message)]
struct RemoteMetadataProbeSpec {
    #[prost(message, repeated, tag = "7")]
    rules: Vec<RemoteMetadataProbeRule>,
    #[prost(bytes = "vec", optional, tag = "16")]
    remote_config_metadata: Option<Vec<u8>>,
}

#[derive(Clone, PartialEq, prost::Message)]
struct RemoteMetadataProbeRule {
    #[prost(bytes = "vec", optional, tag = "14")]
    remote_config_metadata: Option<Vec<u8>>,
}

// Only decode the top-level marker, not `SpecsTopLevel.rest`, which may itself
// contain a large JSON payload. Remote hydration is an explicit wire-level
// contract: `true` must have metadata; `false` and absence take the
// no-remote fast path.
#[derive(Clone, PartialEq, prost::Message)]
struct RemoteMetadataProbeTopLevel {
    #[prost(bool, optional, tag = "8")]
    may_have_remote_config_metadata: Option<bool>,
}

// Hydrated datastore sidecars retain the producer's original `true` marker
// and append a final `false` marker. Normal protobuf readers use the final
// value and see an offline-ready response with no metadata, while the
// integrated parser can use the marker history as durable provenance before
// deciding whether a same-checksum mmap pointer is safe to reuse.
#[derive(Clone, PartialEq, prost::Message)]
struct RemoteMetadataMarkerHistory {
    #[prost(bool, repeated, tag = "8")]
    may_have_remote_config_metadata: Vec<bool>,
}

pub(super) fn begin_session<'a>(
    hydrator: &'a RemoteConfigValueHydrator,
    source_url: &'a str,
) -> ProtobufHydrationSession<'a> {
    ProtobufHydrationSession {
        hydrator,
        source_url,
        started_at: Instant::now(),
        references: HashMap::new(),
        hydrated_values: HashMap::new(),
        in_flight_downloads: FuturesUnordered::new(),
        in_flight_sha256: HashSet::new(),
        response_budget: None,
        response_expansion_budget: None,
        reference_count: 0,
        total_bytes: 0,
        saw_remote_metadata: false,
    }
}

pub(super) async fn hydrate_response(
    hydrator: &RemoteConfigValueHydrator,
    data: &mut ResponseData,
    source_url: &str,
) -> Result<bool, StatsigErr> {
    // Parser compatibility callers still need a rewritten protobuf
    // stream. Text/byte-returning callers negotiate JSON instead; normal
    // adapter-to-SpecStore updates and mmap publishing bypass this path
    // and hydrate inside proto_specs' single compressed reader loop.
    let Some(prepared) = hydrator.prepare_protobuf_stream(data, source_url).await? else {
        data.rewind()?;
        return Ok(false);
    };

    // Preserve the original compressed response while ProtoStreamReader
    // consumes this decompressed hydrated stream during parsing, avoiding a
    // recompress followed by another decompress.
    let PreparedProtobufStream {
        bytes,
        reference_count,
        total_bytes,
        _response_budget,
    } = prepared;
    data.set_prepared_protobuf_stream(bytes);
    hydrator.log_hydration_success(reference_count, total_bytes);
    Ok(true)
}

impl RemoteConfigValueHydrator {
    // For an explicitly opted-in compressed response, consume the stream once,
    // hydrate matching dynamic-config envelopes as they arrive, and hand the
    // parser an uncompressed stream.
    // This keeps the existing wire-preserving patch logic without paying for a
    // second decode or a full-response encode.
    async fn prepare_protobuf_stream(
        &self,
        data: &mut ResponseData,
        source_url: &str,
    ) -> Result<Option<PreparedProtobufStream>, StatsigErr> {
        data.rewind()?;
        let result = async {
            let mut reader = ProtoStreamReader::new_for_response(data)?;
            let first_encoded = reader.read_next_delimited_proto()?;
            let mut buffered = VecDeque::from([first_encoded]);
            let (response_mode, may_have_remote_metadata) = {
                let first = decode_protobuf_envelope(
                    buffered.front().expect("first frame is buffered").as_ref(),
                )
                .ok();
                let first_kind = first
                    .as_ref()
                    .and_then(|envelope| decode_protobuf_envelope_kind(envelope).ok());

                match (first.as_ref(), first_kind) {
                    (Some(first), Some(pb::SpecsEnvelopeKind::TopLevel)) => (
                        ProtobufResponseMode::Full,
                        protobuf_top_level_hint_for_mode(ProtobufResponseMode::Full, first)?,
                    ),
                    (_, Some(pb::SpecsEnvelopeKind::CopyPrev)) => {
                        let second_encoded = reader.read_next_delimited_proto()?;
                        let second = decode_protobuf_envelope(second_encoded.as_ref())?;
                        let second_kind = decode_protobuf_envelope_kind(&second)?;
                        buffered.push_back(second_encoded);
                        if second_kind == pb::SpecsEnvelopeKind::TopLevel {
                            (
                                ProtobufResponseMode::Delta,
                                protobuf_top_level_hint_for_mode(
                                    ProtobufResponseMode::Delta,
                                    &second,
                                )?,
                            )
                        } else {
                            (ProtobufResponseMode::Delta, None)
                        }
                    }
                    _ => (ProtobufResponseMode::Full, None),
                }
            };

            if may_have_remote_metadata != Some(true) {
                return Ok(None);
            }

            let mut references = HashMap::<String, RemoteValueReference>::new();
            let mut envelopes = Vec::new();
            let mut marked_top_level = false;

            loop {
                let encoded = match buffered.pop_front() {
                    Some(encoded) => encoded,
                    None => reader.read_next_delimited_proto()?,
                };
                let Some(envelope) = tolerate_malformed_full_response(
                    response_mode,
                    decode_protobuf_envelope(encoded.as_ref()),
                )?
                else {
                    envelopes.push(PreparedProtobufEnvelope::Bytes(encoded.to_vec()));
                    continue;
                };
                let Some(envelope_kind) = tolerate_malformed_full_response(
                    response_mode,
                    decode_protobuf_envelope_kind(&envelope),
                )?
                else {
                    envelopes.push(PreparedProtobufEnvelope::Bytes(encoded.to_vec()));
                    continue;
                };
                let is_done = envelope_kind == pb::SpecsEnvelopeKind::Done;

                let prepared_envelope = match envelope_kind {
                    pb::SpecsEnvelopeKind::DynamicConfig => self
                        .prepare_dynamic_config_envelope(
                            encoded.as_ref(),
                            &envelope,
                            source_url,
                            response_mode,
                            &mut references,
                        )?
                        .unwrap_or_else(|| PreparedProtobufEnvelope::Bytes(encoded.to_vec())),
                    pb::SpecsEnvelopeKind::TopLevel if !marked_top_level => {
                        let rewritten = tolerate_malformed_full_response(
                            response_mode,
                            rewrite_top_level_envelope(encoded.as_ref(), &envelope),
                        )?;
                        if rewritten.is_some() {
                            marked_top_level = true;
                        }
                        PreparedProtobufEnvelope::Bytes(
                            rewritten.unwrap_or_else(|| encoded.to_vec()),
                        )
                    }
                    _ => PreparedProtobufEnvelope::Bytes(encoded.to_vec()),
                };

                envelopes.push(prepared_envelope);

                if is_done {
                    break;
                }
            }

            if references.is_empty() {
                return Err(remote_metadata_marker_without_metadata_error());
            }

            let (reference_count, total_bytes) = validate_reference_limits(references.values())?;
            let response_budget = self.reserve_response_bytes(total_bytes).await?;
            let hydrated = self.download_all(references.into_values()).await?;
            let mut prepared = Vec::new();
            for envelope in envelopes {
                match envelope {
                    PreparedProtobufEnvelope::Bytes(bytes) => prepared.extend_from_slice(&bytes),
                    PreparedProtobufEnvelope::RemoteDynamicConfig {
                        encoded,
                        spec_data,
                        spec,
                    } => {
                        let rewritten = rewrite_decoded_dynamic_config_envelope(
                            &encoded,
                            &spec_data,
                            spec.as_ref(),
                            &hydrated,
                        )?;
                        prepared.extend_from_slice(&rewritten);
                    }
                }
            }
            Ok(Some(PreparedProtobufStream {
                bytes: prepared,
                reference_count,
                total_bytes,
                _response_budget: response_budget,
            }))
        }
        .await;

        let rewind_result = data.rewind();
        match result {
            Ok(prepared) => {
                rewind_result?;
                Ok(prepared)
            }
            Err(error) => {
                let _ = rewind_result;
                Err(error)
            }
        }
    }

    fn prepare_dynamic_config_envelope(
        &self,
        encoded: &[u8],
        envelope: &pb::SpecsEnvelope,
        source_url: &str,
        response_mode: ProtobufResponseMode,
        references: &mut HashMap<String, RemoteValueReference>,
    ) -> Result<Option<PreparedProtobufEnvelope>, StatsigErr> {
        let Some(spec_data) = tolerate_malformed_full_response(
            response_mode,
            dynamic_config_envelope_data(envelope),
        )?
        else {
            return Ok(None);
        };
        let Some(has_remote_metadata) = tolerate_malformed_full_response(
            response_mode,
            protobuf_spec_has_remote_metadata(spec_data),
        )?
        else {
            return Ok(None);
        };
        if !has_remote_metadata {
            return Ok(None);
        }
        let Some(spec) =
            tolerate_malformed_full_response(response_mode, decode_protobuf_spec(spec_data))?
        else {
            return Ok(None);
        };

        collect_protobuf_spec_references(references, &spec, source_url)?;
        validate_reference_limits(references.values())?;
        Ok(Some(PreparedProtobufEnvelope::RemoteDynamicConfig {
            encoded: encoded.to_vec(),
            spec_data: spec_data.to_vec(),
            spec: Box::new(spec),
        }))
    }
}

impl ProtobufHydrationSession<'_> {
    /// Register one decoded dynamic config without awaiting network I/O. The
    /// parser can register a bounded run of envelopes first, so the session's
    /// download fanout spans configs instead of restarting for every envelope.
    pub(crate) fn register_spec_references(&mut self, spec: &pb::Spec) -> Result<(), StatsigErr> {
        self.saw_remote_metadata = true;

        let mut references = HashMap::<String, RemoteValueReference>::new();
        collect_protobuf_spec_references(&mut references, spec, self.source_url)?;
        for (sha256, reference) in references {
            insert_reference(&mut self.references, sha256, reference)?;
        }
        let (reference_count, total_bytes) = validate_reference_limits(self.references.values())?;
        self.reference_count = reference_count;
        self.total_bytes = total_bytes;

        Ok(())
    }

    /// Atomically accept reused values only when every SHA was registered and
    /// every byte sequence matches its declared length and SHA-256 digest.
    pub(crate) fn seed_verified_values(&mut self, values: HashMap<String, Arc<Vec<u8>>>) -> bool {
        if values.is_empty()
            || values.iter().any(|(sha256, value)| {
                self.references.get(sha256).is_none_or(|reference| {
                    super::verify_body(
                        value.as_slice(),
                        &reference.metadata,
                        reference.metadata.content_type.as_str(),
                    )
                    .is_err()
                })
            })
        {
            return false;
        }

        if !self.try_reserve_response_budget().unwrap_or(false) {
            return false;
        }

        self.hydrated_values.extend(values);
        true
    }

    /// Start newly registered values as soon as a download slot is available.
    /// When the parser discovers more SHAs than the active window can hold,
    /// wait for only one completion before starting the next value.
    pub(crate) async fn advance_download_window(&mut self) -> Result<(), StatsigErr> {
        self.reserve_response_budget().await?;
        self.start_available_downloads();
        while self.has_unstarted_references() {
            self.await_one_download().await?;
            self.start_available_downloads();
        }
        Ok(())
    }

    /// Drain every session reference before the parser publishes its ordered
    /// entity batch. This is reserved for real parser boundaries; ordinary
    /// concurrency backpressure uses `advance_download_window` instead.
    pub(crate) async fn download_registered_references(&mut self) -> Result<(), StatsigErr> {
        self.reserve_response_budget().await?;
        while self.pending_reference_count() > 0 {
            self.start_available_downloads();
            self.await_one_download().await?;
        }
        Ok(())
    }

    async fn reserve_response_budget(&mut self) -> Result<(), StatsigErr> {
        if self.references.is_empty() || self.try_reserve_response_budget()? {
            return Ok(());
        }

        let remaining = HYDRATION_TIMEOUT
            .checked_sub(self.started_at.elapsed())
            .ok_or_else(total_timeout_error)?;
        if let Some(reservation) = &self.response_budget {
            let expansion =
                (self.hydrator.response_budget.capacity - reservation.num_permits()) as u64;
            let permit = timeout(
                remaining,
                self.hydrator.reserve_response_expansion_bytes(expansion),
            )
            .await
            .map_err(|_| total_timeout_error())??;
            self.response_expansion_budget = Some(permit);
        } else {
            let permit = timeout(
                remaining,
                self.hydrator.reserve_response_bytes(self.total_bytes),
            )
            .await
            .map_err(|_| total_timeout_error())??;
            self.response_budget = Some(permit);
        }
        Ok(())
    }

    fn try_reserve_response_budget(&mut self) -> Result<bool, StatsigErr> {
        if self.response_budget.is_none() {
            let Some(permit) = self.hydrator.try_reserve_response_bytes(self.total_bytes)? else {
                return Ok(false);
            };
            self.response_budget = Some(permit);
            return Ok(true);
        }

        let reserved = self
            .response_budget
            .as_ref()
            .expect("an existing response reservation is required")
            .num_permits();
        let budgeted_total = self
            .total_bytes
            .min(self.hydrator.response_budget.capacity as u64);
        if budgeted_total <= reserved as u64 || self.response_expansion_budget.is_some() {
            return Ok(true);
        }

        let additional = budgeted_total - reserved as u64;
        if let Some(permit) = self.hydrator.try_reserve_response_bytes(additional)? {
            self.response_budget
                .as_mut()
                .expect("an existing response reservation is required")
                .merge(permit);
            return Ok(true);
        }

        // Never await more base permits while retaining earlier response
        // bytes: other responses may be in the same state. A single expansion
        // reservation covers the rest of this response's concurrency window.
        let expansion = (self.hydrator.response_budget.capacity - reserved) as u64;
        let Some(permit) = self
            .hydrator
            .try_reserve_response_expansion_bytes(expansion)?
        else {
            return Ok(false);
        };
        self.response_expansion_budget = Some(permit);
        Ok(true)
    }

    fn start_available_downloads(&mut self) {
        while self.in_flight_downloads.len() < DOWNLOAD_CONCURRENCY {
            let Some((sha256, reference)) = self.next_unstarted_reference() else {
                break;
            };
            self.in_flight_sha256.insert(sha256.clone());
            let hydrator = self.hydrator;
            self.in_flight_downloads.push(
                async move {
                    let value = hydrator.download_one(&reference).await?;
                    Ok((sha256, value))
                }
                .boxed(),
            );
        }
    }

    fn next_unstarted_reference(&self) -> Option<(String, RemoteValueReference)> {
        self.references.iter().find_map(|(sha256, reference)| {
            (!self.hydrated_values.contains_key(sha256) && !self.in_flight_sha256.contains(sha256))
                .then(|| (sha256.clone(), reference.clone()))
        })
    }

    fn has_unstarted_references(&self) -> bool {
        self.next_unstarted_reference().is_some()
    }

    async fn await_one_download(&mut self) -> Result<(), StatsigErr> {
        let remaining = HYDRATION_TIMEOUT
            .checked_sub(self.started_at.elapsed())
            .ok_or_else(total_timeout_error)?;
        let download = timeout(remaining, self.in_flight_downloads.next())
            .await
            .map_err(|_| total_timeout_error())?
            .expect("pending remote references must have an active download");
        let (sha256, value) = download?;
        self.in_flight_sha256.remove(&sha256);
        self.hydrated_values.insert(sha256, value);
        Ok(())
    }

    fn pending_reference_count(&self) -> usize {
        self.references
            .keys()
            .filter(|sha256| !self.hydrated_values.contains_key(*sha256))
            .count()
    }

    pub(crate) fn saw_remote_metadata(&self) -> bool {
        self.saw_remote_metadata
    }

    /// Apply already-verified values to one queued spec. This remains
    /// synchronous so mmap and parse-option thread-local scopes never cross an
    /// await boundary.
    pub(crate) fn apply_registered_spec(&self, spec: &mut pb::Spec) -> Result<(), StatsigErr> {
        apply_protobuf_spec_hydration(spec, &self.hydrated_values)
    }

    pub(crate) fn hydrated_values(&self) -> &HashMap<String, Arc<Vec<u8>>> {
        &self.hydrated_values
    }

    pub(crate) fn finish(self, succeeded: bool) {
        if !self.saw_remote_metadata {
            return;
        }

        let outcome = if succeeded {
            HydrationOutcome::Success
        } else {
            HydrationOutcome::Failure
        };
        self.hydrator
            .log_hydration_outcome(self.started_at, outcome);

        if succeeded {
            self.hydrator
                .log_hydration_success(self.reference_count, self.total_bytes);
        }
    }
}

fn collect_protobuf_spec_references(
    references: &mut HashMap<String, RemoteValueReference>,
    spec: &pb::Spec,
    source_url: &str,
) -> Result<(), StatsigErr> {
    if let Some(metadata) = spec.remote_config_metadata.as_ref() {
        let placeholder = protobuf_return_value_raw(&spec.default_value)?;
        add_raw_value_reference(
            references,
            placeholder.as_deref(),
            metadata_from_proto(metadata)?,
            source_url,
        )?;
    }
    for rule in &spec.rules {
        let Some(metadata) = rule.remote_config_metadata.as_ref() else {
            continue;
        };
        let placeholder = protobuf_return_value_raw(&rule.return_value)?;
        add_raw_value_reference(
            references,
            placeholder.as_deref(),
            metadata_from_proto(metadata)?,
            source_url,
        )?;
    }
    Ok(())
}

fn apply_protobuf_spec_hydration(
    spec: &mut pb::Spec,
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
) -> Result<(), StatsigErr> {
    if let Some(metadata) = spec.remote_config_metadata.take() {
        let metadata = metadata_from_proto(&metadata)?;
        let body = hydrated_value(hydrated, metadata.sha256.as_str())?;
        if spec.default_value.is_none() {
            return Err(hydration_error(
                HydrationFailureReason::MetadataWithoutValue,
                "protobuf remote metadata had no matching default value",
            ));
        }
        spec.default_value = Some(pb::ReturnValue {
            value: Some(return_value::Value::RawValue(body.to_vec())),
        });
    }

    for rule in &mut spec.rules {
        let Some(metadata) = rule.remote_config_metadata.take() else {
            continue;
        };
        let metadata = metadata_from_proto(&metadata)?;
        let body = hydrated_value(hydrated, metadata.sha256.as_str())?;
        if rule.return_value.is_none() {
            return Err(hydration_error(
                HydrationFailureReason::MetadataWithoutValue,
                "protobuf remote metadata had no matching rule value",
            ));
        }
        rule.return_value = Some(pb::ReturnValue {
            value: Some(return_value::Value::RawValue(body.to_vec())),
        });
    }

    Ok(())
}

fn metadata_from_proto(
    metadata: &pb::RemoteConfigValueMetadata,
) -> Result<RemoteConfigValueMetadata, StatsigErr> {
    RemoteConfigValueMetadataWire {
        sha256: metadata.sha256.clone(),
        byte_length: metadata.byte_length,
        content_type: metadata.content_type.clone(),
        compression: metadata.compression.clone(),
    }
    .try_into()
}

const ENVELOPE_DATA_TAG: u32 = 4;
const SPEC_DEFAULT_VALUE_TAG: u32 = 3;
const SPEC_RULES_TAG: u32 = 7;
const SPEC_REMOTE_METADATA_TAG: u32 = 16;
const RULE_RETURN_VALUE_TAG: u32 = 7;
const RULE_REMOTE_METADATA_TAG: u32 = 14;
const RETURN_VALUE_BOOL_TAG: u32 = 1;
const RETURN_VALUE_RAW_TAG: u32 = 2;

pub(super) struct RawProtobufField<'a> {
    pub(super) tag: u32,
    raw: &'a [u8],
    pub(super) length_delimited_value: Option<&'a [u8]>,
}

pub(crate) fn rewrite_decoded_dynamic_config_envelope(
    encoded: &[u8],
    spec_data: &[u8],
    spec: &pb::Spec,
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
) -> Result<Vec<u8>, StatsigErr> {
    let patched_spec = patch_dynamic_config_spec(spec_data, spec, hydrated)?;
    let envelope_data = delimited_protobuf_message(encoded)?;
    let patched_envelope =
        replace_length_delimited_field(envelope_data, ENVELOPE_DATA_TAG, &patched_spec)?;
    encode_delimited_message(&patched_envelope)
}

pub(crate) fn rewrite_top_level_envelope(
    encoded: &[u8],
    envelope: &pb::SpecsEnvelope,
) -> Result<Vec<u8>, StatsigErr> {
    let mut top_level_data = envelope.data.clone().ok_or_else(|| {
        hydration_error(
            HydrationFailureReason::MissingProtoData,
            "top-level protobuf envelope had no data",
        )
    })?;

    // Preserve the producer's original `true` field and append `false`.
    // Ordinary protobuf readers use the final value and see an offline-ready
    // response with no metadata. The integrated parser also recognizes the
    // true-then-false history as hydration provenance before reusing mmap.
    top_level_data.extend_from_slice(
        &RemoteMetadataProbeTopLevel {
            may_have_remote_config_metadata: Some(false),
        }
        .encode_to_vec(),
    );

    let envelope_data = delimited_protobuf_message(encoded)?;
    let patched_envelope =
        replace_length_delimited_field(envelope_data, ENVELOPE_DATA_TAG, &top_level_data)?;
    encode_delimited_message(&patched_envelope)
}

fn patch_dynamic_config_spec(
    data: &[u8],
    spec: &pb::Spec,
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
) -> Result<Vec<u8>, StatsigErr> {
    let default_metadata = spec
        .remote_config_metadata
        .as_ref()
        .map(metadata_from_proto)
        .transpose()?;
    let default_body = default_metadata
        .as_ref()
        .map(|metadata| hydrated_value(hydrated, metadata.sha256.as_str()))
        .transpose()?;

    let fields = parse_raw_protobuf_fields(data)?;
    let mut output = Vec::with_capacity(data.len());
    let mut saw_default_value = false;
    for field in fields {
        match field.tag {
            SPEC_DEFAULT_VALUE_TAG if default_body.is_some() => {
                let value =
                    required_length_delimited_value(&field, "dynamic config default value")?;
                let patched = patch_return_value(value, default_body.expect("checked above"))?;
                append_length_delimited_field(&mut output, SPEC_DEFAULT_VALUE_TAG, &patched);
                saw_default_value = true;
            }
            SPEC_RULES_TAG => {
                let value = required_length_delimited_value(&field, "dynamic config rule")?;
                if let Some(patched) = patch_rule(value, hydrated)? {
                    append_length_delimited_field(&mut output, SPEC_RULES_TAG, &patched);
                } else {
                    output.extend_from_slice(field.raw);
                }
            }
            SPEC_REMOTE_METADATA_TAG => {}
            _ => output.extend_from_slice(field.raw),
        }
    }

    if default_body.is_some() && !saw_default_value {
        return Err(hydration_error(
            HydrationFailureReason::MetadataWithoutValue,
            "protobuf remote metadata had no matching default value",
        ));
    }
    Ok(output)
}

fn patch_rule(
    data: &[u8],
    hydrated: &HashMap<String, Arc<Vec<u8>>>,
) -> Result<Option<Vec<u8>>, StatsigErr> {
    let rule = pb::Rule::decode(data)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))?;
    let Some(metadata) = rule.remote_config_metadata.as_ref() else {
        return Ok(None);
    };
    let metadata = metadata_from_proto(metadata)?;
    let body = hydrated_value(hydrated, metadata.sha256.as_str())?;

    let fields = parse_raw_protobuf_fields(data)?;
    let mut output = Vec::with_capacity(data.len());
    let mut saw_return_value = false;
    for field in fields {
        match field.tag {
            RULE_RETURN_VALUE_TAG => {
                let value = required_length_delimited_value(&field, "dynamic config rule value")?;
                let patched = patch_return_value(value, body)?;
                append_length_delimited_field(&mut output, RULE_RETURN_VALUE_TAG, &patched);
                saw_return_value = true;
            }
            RULE_REMOTE_METADATA_TAG => {}
            _ => output.extend_from_slice(field.raw),
        }
    }

    if !saw_return_value {
        return Err(hydration_error(
            HydrationFailureReason::MetadataWithoutValue,
            "protobuf remote metadata had no matching rule value",
        ));
    }
    Ok(Some(output))
}

fn patch_return_value(data: &[u8], body: &[u8]) -> Result<Vec<u8>, StatsigErr> {
    let fields = parse_raw_protobuf_fields(data)?;
    let mut output = Vec::with_capacity(data.len().saturating_add(body.len()));
    for field in fields {
        if field.tag != RETURN_VALUE_BOOL_TAG && field.tag != RETURN_VALUE_RAW_TAG {
            output.extend_from_slice(field.raw);
        }
    }
    append_length_delimited_field(&mut output, RETURN_VALUE_RAW_TAG, body);
    Ok(output)
}

pub(super) fn parse_raw_protobuf_fields(
    data: &[u8],
) -> Result<Vec<RawProtobufField<'_>>, StatsigErr> {
    let mut remaining = data;
    let mut fields = Vec::new();
    while remaining.has_remaining() {
        let start = data.len() - remaining.remaining();
        let (tag, wire_type) =
            prost::encoding::decode_key(&mut remaining).map_err(protobuf_wire_error)?;
        let length_delimited_value = if wire_type == prost::encoding::WireType::LengthDelimited {
            let length =
                prost::encoding::decode_varint(&mut remaining).map_err(protobuf_wire_error)?;
            let length = usize::try_from(length)
                .map_err(|_| protobuf_wire_error("length-delimited field was too large"))?;
            if length > remaining.remaining() {
                return Err(protobuf_wire_error("length-delimited field exceeded input"));
            }
            let value = &remaining[..length];
            remaining.advance(length);
            Some(value)
        } else {
            prost::encoding::skip_field(
                wire_type,
                tag,
                &mut remaining,
                prost::encoding::DecodeContext::default(),
            )
            .map_err(protobuf_wire_error)?;
            None
        };
        let end = data.len() - remaining.remaining();
        fields.push(RawProtobufField {
            tag,
            raw: &data[start..end],
            length_delimited_value,
        });
    }
    Ok(fields)
}

fn required_length_delimited_value<'a>(
    field: &RawProtobufField<'a>,
    label: &str,
) -> Result<&'a [u8], StatsigErr> {
    field.length_delimited_value.ok_or_else(|| {
        hydration_error(
            HydrationFailureReason::InvalidProtoWireType,
            &format!("{label} was not length-delimited"),
        )
    })
}

fn replace_length_delimited_field(
    data: &[u8],
    tag: u32,
    value: &[u8],
) -> Result<Vec<u8>, StatsigErr> {
    let fields = parse_raw_protobuf_fields(data)?;
    let mut output = Vec::with_capacity(data.len().saturating_add(value.len()));
    for field in fields {
        if field.tag != tag {
            output.extend_from_slice(field.raw);
        }
    }
    append_length_delimited_field(&mut output, tag, value);
    Ok(output)
}

pub(super) fn append_length_delimited_field(output: &mut Vec<u8>, tag: u32, value: &[u8]) {
    prost::encoding::encode_key(tag, prost::encoding::WireType::LengthDelimited, output);
    prost::encoding::encode_varint(value.len() as u64, output);
    output.extend_from_slice(value);
}

fn delimited_protobuf_message(encoded: &[u8]) -> Result<&[u8], StatsigErr> {
    let mut remaining = encoded;
    let length = prost::decode_length_delimiter(&mut remaining).map_err(protobuf_wire_error)?;
    if length != remaining.remaining() {
        return Err(protobuf_wire_error(
            "length-delimited protobuf frame had trailing or missing bytes",
        ));
    }
    Ok(&remaining[..length])
}

pub(super) fn encode_delimited_message(message: &[u8]) -> Result<Vec<u8>, StatsigErr> {
    let mut encoded =
        Vec::with_capacity(prost::length_delimiter_len(message.len()) + message.len());
    prost::encode_length_delimiter(message.len(), &mut encoded)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    encoded.extend_from_slice(message);
    Ok(encoded)
}

fn protobuf_wire_error(error: impl std::fmt::Display) -> StatsigErr {
    StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string())
}

fn protobuf_return_value_raw(
    return_value: &Option<pb::ReturnValue>,
) -> Result<Option<Box<RawValue>>, StatsigErr> {
    let Some(return_value) = return_value else {
        return Ok(None);
    };
    let Some(value) = return_value.value.as_ref() else {
        return Ok(None);
    };
    match value {
        return_value::Value::RawValue(bytes) => serde_json::from_slice::<Box<RawValue>>(bytes)
            .map(Some)
            .map_err(|error| {
                hydration_error(
                    HydrationFailureReason::InvalidPlaceholder,
                    &error.to_string(),
                )
            }),
        return_value::Value::BoolValue(_) => Ok(None),
    }
}

fn protobuf_top_level_hint_for_mode(
    response_mode: ProtobufResponseMode,
    top_level: &pb::SpecsEnvelope,
) -> Result<Option<bool>, StatsigErr> {
    let Some(top_level_data) =
        tolerate_malformed_full_response(response_mode, top_level_envelope_data(top_level))?
    else {
        return Ok(None);
    };
    let Some(may_have_remote_metadata) = tolerate_malformed_full_response(
        response_mode,
        protobuf_top_level_may_have_remote_metadata_hint(top_level_data),
    )?
    else {
        return Ok(None);
    };
    Ok(may_have_remote_metadata)
}

fn protobuf_top_level_may_have_remote_metadata_hint(
    data: &[u8],
) -> Result<Option<bool>, StatsigErr> {
    let probe = RemoteMetadataProbeTopLevel::decode(data)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))?;
    Ok(probe.may_have_remote_config_metadata)
}

pub(crate) fn protobuf_top_level_has_hydrated_sidecar_provenance(
    data: &[u8],
) -> Result<bool, StatsigErr> {
    let history = RemoteMetadataMarkerHistory::decode(data)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))?;
    let Some((last, previous)) = history.may_have_remote_config_metadata.split_last() else {
        return Ok(false);
    };

    Ok(!last && previous.contains(&true))
}

pub(super) fn protobuf_spec_has_remote_metadata(data: &[u8]) -> Result<bool, StatsigErr> {
    let probe = RemoteMetadataProbeSpec::decode(data)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))?;
    Ok(probe.remote_config_metadata.is_some()
        || probe
            .rules
            .iter()
            .any(|rule| rule.remote_config_metadata.is_some()))
}

#[cfg(test)]
pub(super) fn parse_protobuf_envelopes(
    data: &mut ResponseData,
) -> Result<Vec<pb::SpecsEnvelope>, StatsigErr> {
    data.rewind()?;
    let mut reader = ProtoStreamReader::new(data);
    let mut envelopes = Vec::new();
    loop {
        let encoded = reader.read_next_delimited_proto()?;
        let envelope = decode_protobuf_envelope(encoded.as_ref())?;
        let is_done = pb::SpecsEnvelopeKind::try_from(envelope.kind).ok()
            == Some(pb::SpecsEnvelopeKind::Done);
        envelopes.push(envelope);
        if is_done {
            return Ok(envelopes);
        }
    }
}

pub(super) fn decode_protobuf_envelope(encoded: &[u8]) -> Result<pb::SpecsEnvelope, StatsigErr> {
    pb::SpecsEnvelope::decode_length_delimited(encoded)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))
}

fn decode_protobuf_envelope_kind(
    envelope: &pb::SpecsEnvelope,
) -> Result<pb::SpecsEnvelopeKind, StatsigErr> {
    pb::SpecsEnvelopeKind::try_from(envelope.kind)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))
}

fn decode_protobuf_spec(data: &[u8]) -> Result<pb::Spec, StatsigErr> {
    pb::Spec::decode(data)
        .map_err(|error| StatsigErr::ProtobufParseError(TAG.to_string(), error.to_string()))
}

fn dynamic_config_envelope_data(envelope: &pb::SpecsEnvelope) -> Result<&[u8], StatsigErr> {
    envelope.data.as_deref().ok_or_else(|| {
        hydration_error(
            HydrationFailureReason::MissingProtoData,
            "dynamic config protobuf envelope had no data",
        )
    })
}

fn top_level_envelope_data(envelope: &pb::SpecsEnvelope) -> Result<&[u8], StatsigErr> {
    envelope.data.as_deref().ok_or_else(|| {
        hydration_error(
            HydrationFailureReason::MissingProtoData,
            "top-level protobuf envelope had no data",
        )
    })
}

fn tolerate_malformed_full_response<T>(
    response_mode: ProtobufResponseMode,
    result: Result<T, StatsigErr>,
) -> Result<Option<T>, StatsigErr> {
    match result {
        Ok(value) => Ok(Some(value)),
        Err(_) if response_mode.tolerates_malformed_entities() => Ok(None),
        Err(error) => Err(error),
    }
}

#[cfg(test)]
pub(super) fn serialize_protobuf_envelopes(
    envelopes: &[pb::SpecsEnvelope],
) -> Result<Vec<u8>, StatsigErr> {
    let mut uncompressed = Vec::new();
    for envelope in envelopes {
        envelope
            .encode_length_delimited(&mut uncompressed)
            .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    }

    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::new(&mut compressed, 4096, 5, 22);
        writer
            .write_all(&uncompressed)
            .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    }
    Ok(compressed)
}

pub(crate) fn remote_metadata_marker_without_metadata_error() -> StatsigErr {
    StatsigErr::ProtobufParseError(
        REMOTE_METADATA_MARKER_WITHOUT_METADATA_TAG.to_string(),
        REMOTE_METADATA_MARKER_WITHOUT_METADATA_MESSAGE.to_string(),
    )
}
