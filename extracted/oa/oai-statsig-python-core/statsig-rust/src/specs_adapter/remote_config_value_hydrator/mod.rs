use std::collections::HashMap;
use std::io::Read;
use std::sync::{
    Arc, OnceLock,
    atomic::{AtomicUsize, Ordering},
};
use std::time::{Duration, Instant};

use dashmap::DashMap;
use futures::{StreamExt, TryStreamExt, stream};
use serde::Deserialize;
use serde_json::value::RawValue;
use sha2::{Digest, Sha256};
use tokio::sync::{OnceCell, OwnedSemaphorePermit, Semaphore, TryAcquireError};
use tokio::time::timeout;
use url::Url;

use crate::networking::{NetworkClient, RequestArgs, ResponseData};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::specs_adapter::response_format::{
    SpecsResponseFormat, get_specs_response_format, is_legacy_json_no_update_under_protobuf_headers,
};
use crate::{StatsigErr, log_d};

mod json;
mod protobuf;

pub(crate) use protobuf::{
    ProtobufHydrationSession, protobuf_top_level_has_hydrated_sidecar_provenance,
    remote_metadata_marker_without_metadata_error, rewrite_decoded_dynamic_config_envelope,
    rewrite_top_level_envelope,
};

const TAG: &str = "RemoteConfigValueHydrator";
const DEFAULT_DOWNLOAD_ORIGIN: &str = "https://statsigcdn.openai.com";
const DOWNLOAD_PATH_PREFIX: &str = "/v1/dynamic_config_value/";

const MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC: usize = 16 * 1024 * 1024;
const MAX_REMOTE_VALUE_BYTES: usize = 10 * 1024 * 1024;
const MAX_IN_FLIGHT_HYDRATION_BYTES: usize = 64 * 1024 * 1024;
// Split response reservations into admission and expansion pools so small
// streaming responses do not each consume an entire concurrency window.
const MAX_ACTIVE_RESPONSE_RESERVATION_BYTES: usize = MAX_IN_FLIGHT_HYDRATION_BYTES * 2;
pub(crate) const DOWNLOAD_CONCURRENCY: usize = 8;
const DOWNLOAD_RETRIES: u32 = 2;
const DOWNLOAD_TIMEOUT_MS: u64 = 2_000;
const HYDRATION_TIMEOUT: Duration = Duration::from_secs(30);

static GLOBAL_DOWNLOAD_SLOTS: Semaphore = Semaphore::const_new(DOWNLOAD_CONCURRENCY);
static GLOBAL_DOWNLOAD_BYTES: Semaphore = Semaphore::const_new(MAX_IN_FLIGHT_HYDRATION_BYTES);
static GLOBAL_RESPONSE_HYDRATION_BUDGET: OnceLock<Arc<ResponseHydrationBudget>> = OnceLock::new();

const HYDRATION_COUNT_METRIC: &str = "remote_config_hydration.count";
const HYDRATION_LATENCY_METRIC: &str = "remote_config_hydration.latency";
const HYDRATION_BYTES_METRIC: &str = "remote_config_hydration.bytes";

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum HydrationOutcome {
    Success,
    Failure,
}

impl HydrationOutcome {
    const fn as_str(self) -> &'static str {
        match self {
            Self::Success => "success",
            Self::Failure => "failure",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum HydrationFailureReason {
    TotalTimeout,
    DownloadFailed,
    EmptyResponse,
    MissingResponseContentType,
    MissingProtoData,
    MetadataWithoutValue,
    MetadataConflict,
    TooManyValues,
    TotalBytesExceeded,
    InvalidDefaultMetadata,
    InvalidMetadata,
    InvalidPlaceholder,
    InvalidSha256,
    InvalidContentType,
    InvalidCompression,
    InvalidSourceUrl,
    InvalidDownloadUrl,
    InvalidDownloadScheme,
    UntrustedDownloadOrigin,
    DownloadPathMismatch,
    ByteLengthMismatch,
    ResponseContentTypeMismatch,
    ChecksumMismatch,
    InvalidJson,
    InvalidProtoWireType,
    MissingHydratedValue,
}

impl HydrationFailureReason {
    const fn as_str(self) -> &'static str {
        match self {
            Self::TotalTimeout => "total_timeout",
            Self::DownloadFailed => "download_failed",
            Self::EmptyResponse => "empty_response",
            Self::MissingResponseContentType => "missing_response_content_type",
            Self::MissingProtoData => "missing_proto_data",
            Self::MetadataWithoutValue => "metadata_without_value",
            Self::MetadataConflict => "metadata_conflict",
            Self::TooManyValues => "too_many_values",
            Self::TotalBytesExceeded => "total_bytes_exceeded",
            Self::InvalidDefaultMetadata => "invalid_default_metadata",
            Self::InvalidMetadata => "invalid_metadata",
            Self::InvalidPlaceholder => "invalid_placeholder",
            Self::InvalidSha256 => "invalid_sha256",
            Self::InvalidContentType => "invalid_content_type",
            Self::InvalidCompression => "invalid_compression",
            Self::InvalidSourceUrl => "invalid_source_url",
            Self::InvalidDownloadUrl => "invalid_download_url",
            Self::InvalidDownloadScheme => "invalid_download_scheme",
            Self::UntrustedDownloadOrigin => "untrusted_download_origin",
            Self::DownloadPathMismatch => "download_path_mismatch",
            Self::ByteLengthMismatch => "byte_length_mismatch",
            Self::ResponseContentTypeMismatch => "response_content_type_mismatch",
            Self::ChecksumMismatch => "checksum_mismatch",
            Self::InvalidJson => "invalid_json",
            Self::InvalidProtoWireType => "invalid_proto_wire_type",
            Self::MissingHydratedValue => "missing_hydrated_value",
        }
    }
}

// Keep the checksum and byte length independent of the untrusted placeholder
// URL, and keep the format fields explicit so future content types or
// compression modes do not require another metadata-envelope change.
#[derive(Clone, Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct RemoteConfigValueMetadataWire {
    sha256: String,
    byte_length: u64,
    content_type: String,
    compression: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct RemoteConfigValueMetadata {
    sha256: Sha256Digest,
    byte_length: u64,
    content_type: RemoteContentType,
    compression: RemoteCompression,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct Sha256Digest(String);

impl Sha256Digest {
    fn as_str(&self) -> &str {
        &self.0
    }
}

impl std::fmt::Display for Sha256Digest {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(self.as_str())
    }
}

impl TryFrom<String> for Sha256Digest {
    type Error = StatsigErr;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        if value.len() != 64
            || !value
                .bytes()
                .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
        {
            return Err(hydration_error(
                HydrationFailureReason::InvalidSha256,
                "remote value sha256 must be 64 lowercase hexadecimal characters",
            ));
        }
        Ok(Self(value))
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum RemoteContentType {
    ApplicationJson,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum RemoteCompression {
    None,
    Gzip,
    Zstd,
}

impl RemoteContentType {
    const fn as_str(self) -> &'static str {
        match self {
            Self::ApplicationJson => "application/json",
        }
    }
}

impl TryFrom<RemoteConfigValueMetadataWire> for RemoteConfigValueMetadata {
    type Error = StatsigErr;

    fn try_from(wire: RemoteConfigValueMetadataWire) -> Result<Self, Self::Error> {
        let sha256 = Sha256Digest::try_from(wire.sha256)?;
        if wire.byte_length > MAX_REMOTE_VALUE_BYTES as u64 {
            return Err(hydration_error(
                HydrationFailureReason::TotalBytesExceeded,
                &format!(
                    "remote value {sha256} declared {} bytes; maximum is {MAX_REMOTE_VALUE_BYTES}",
                    wire.byte_length
                ),
            ));
        }
        let content_type = if wire.content_type == RemoteContentType::ApplicationJson.as_str() {
            RemoteContentType::ApplicationJson
        } else {
            return Err(hydration_error(
                HydrationFailureReason::InvalidContentType,
                &format!(
                    "remote value {} declared unsupported content type {}",
                    sha256, wire.content_type
                ),
            ));
        };
        let compression = match wire.compression.as_str() {
            "none" => RemoteCompression::None,
            "gzip" => RemoteCompression::Gzip,
            "zstd" => RemoteCompression::Zstd,
            _ => {
                return Err(hydration_error(
                    HydrationFailureReason::InvalidCompression,
                    &format!(
                        "remote value {} declared unsupported compression {}",
                        sha256, wire.compression
                    ),
                ));
            }
        };
        Ok(Self {
            sha256,
            byte_length: wire.byte_length,
            content_type,
            compression,
        })
    }
}

#[derive(Clone, Debug)]
struct RemoteValueReference {
    download_url: Url,
    metadata: RemoteConfigValueMetadata,
    occurrences: usize,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct SharedDownloadKey {
    download_url: String,
    sha256: Sha256Digest,
    byte_length: u64,
    content_type: RemoteContentType,
    compression: RemoteCompression,
}

impl SharedDownloadKey {
    fn from_reference(reference: &RemoteValueReference) -> Self {
        Self {
            download_url: reference.download_url.as_str().to_string(),
            sha256: reference.metadata.sha256.clone(),
            byte_length: reference.metadata.byte_length,
            content_type: reference.metadata.content_type,
            compression: reference.metadata.compression,
        }
    }
}

#[derive(Default)]
struct SharedDownload {
    result: OnceCell<Result<Arc<Vec<u8>>, StatsigErr>>,
    waiters: AtomicUsize,
}

struct SharedDownloadWaiter<'hydrator> {
    hydrator: &'hydrator RemoteConfigValueHydrator,
    key: SharedDownloadKey,
    download: Arc<SharedDownload>,
}

impl Drop for SharedDownloadWaiter<'_> {
    fn drop(&mut self) {
        if self.download.waiters.fetch_sub(1, Ordering::AcqRel) == 1 {
            self.hydrator
                .in_flight_downloads()
                .remove_if(&self.key, |_, active| {
                    Arc::ptr_eq(active, &self.download)
                        && active.waiters.load(Ordering::Acquire) == 0
                });
        }
    }
}

struct ResponseHydrationBudget {
    bytes: Arc<Semaphore>,
    expansion: Arc<Semaphore>,
    capacity: usize,
}

impl ResponseHydrationBudget {
    fn new(capacity: usize) -> Self {
        Self {
            bytes: Arc::new(Semaphore::new(capacity)),
            expansion: Arc::new(Semaphore::new(capacity)),
            capacity,
        }
    }

    fn reservation_size(&self, bytes: u64) -> Result<u32, StatsigErr> {
        let requested = u32::try_from(bytes.min(self.capacity as u64).max(1))
            .ok()
            .filter(|requested| {
                *requested as usize <= MAX_IN_FLIGHT_HYDRATION_BYTES
                    && *requested as usize <= self.capacity
            })
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TotalBytesExceeded,
                    "remote value response exceeded the process hydration byte budget",
                )
            })?;
        Ok(requested)
    }

    async fn reserve(&self, bytes: u64) -> Result<OwnedSemaphorePermit, StatsigErr> {
        self.reserve_from(&self.bytes, bytes).await
    }

    async fn reserve_expansion(&self, bytes: u64) -> Result<OwnedSemaphorePermit, StatsigErr> {
        self.reserve_from(&self.expansion, bytes).await
    }

    async fn reserve_from(
        &self,
        pool: &Arc<Semaphore>,
        bytes: u64,
    ) -> Result<OwnedSemaphorePermit, StatsigErr> {
        let requested = self.reservation_size(bytes)?;
        Arc::clone(pool)
            .acquire_many_owned(requested)
            .await
            .map_err(|_| {
                hydration_error(
                    HydrationFailureReason::DownloadFailed,
                    "remote value response byte budget is unavailable",
                )
            })
    }

    fn try_reserve(&self, bytes: u64) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.try_reserve_from(&self.bytes, bytes)
    }

    fn try_reserve_expansion(
        &self,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.try_reserve_from(&self.expansion, bytes)
    }

    fn try_reserve_from(
        &self,
        pool: &Arc<Semaphore>,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        let requested = self.reservation_size(bytes)?;
        match Arc::clone(pool).try_acquire_many_owned(requested) {
            Ok(permit) => Ok(Some(permit)),
            Err(TryAcquireError::NoPermits) => Ok(None),
            Err(TryAcquireError::Closed) => Err(hydration_error(
                HydrationFailureReason::DownloadFailed,
                "remote value response byte budget is unavailable",
            )),
        }
    }
}

/// Hydrates blob-backed dynamic config values in a DCS response before the
/// response is parsed or published.
pub(crate) struct RemoteConfigValueHydrator {
    network: Arc<NetworkClient>,
    ops_stats: Arc<OpsStatsForInstance>,
    in_flight: OnceLock<DashMap<SharedDownloadKey, Arc<SharedDownload>>>,
    response_budget: Arc<ResponseHydrationBudget>,
}

impl RemoteConfigValueHydrator {
    pub(crate) fn new_with_ops_stats(
        network: Arc<NetworkClient>,
        ops_stats: Arc<OpsStatsForInstance>,
    ) -> Self {
        Self {
            network,
            ops_stats,
            in_flight: OnceLock::new(),
            response_budget: Arc::clone(GLOBAL_RESPONSE_HYDRATION_BUDGET.get_or_init(|| {
                Arc::new(ResponseHydrationBudget::new(
                    MAX_ACTIVE_RESPONSE_RESERVATION_BYTES / 2,
                ))
            })),
        }
    }

    fn in_flight_downloads(&self) -> &DashMap<SharedDownloadKey, Arc<SharedDownload>> {
        self.in_flight.get_or_init(DashMap::new)
    }

    async fn reserve_response_bytes(&self, bytes: u64) -> Result<OwnedSemaphorePermit, StatsigErr> {
        self.response_budget.reserve(bytes).await
    }

    fn try_reserve_response_bytes(
        &self,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.response_budget.try_reserve(bytes)
    }

    async fn reserve_response_expansion_bytes(
        &self,
        bytes: u64,
    ) -> Result<OwnedSemaphorePermit, StatsigErr> {
        self.response_budget.reserve_expansion(bytes).await
    }

    fn try_reserve_response_expansion_bytes(
        &self,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.response_budget.try_reserve_expansion(bytes)
    }

    pub(crate) fn begin_protobuf_hydration<'a>(
        &'a self,
        source_url: &'a str,
    ) -> ProtobufHydrationSession<'a> {
        protobuf::begin_session(self, source_url)
    }

    /// Rewrites any remote-backed values in data to their verified JSON
    /// values. Callers must preserve DCS response headers so protobuf payloads
    /// can be detected, and source_url must be the trusted DCS origin used
    /// to resolve relative remote-value paths.
    pub(crate) async fn hydrate_response(
        &self,
        data: &mut ResponseData,
        source_url: &str,
    ) -> Result<(), StatsigErr> {
        // Some legacy DCS responses keep statsig-br headers around a JSON
        // no-update body. Preserve those bytes instead of probing protobuf.
        if is_legacy_json_no_update_under_protobuf_headers(data)? {
            return Ok(());
        }

        let started_at = Instant::now();
        let result = timeout(
            HYDRATION_TIMEOUT,
            self.hydrate_response_within_timeout(data, source_url),
        )
        .await
        .map_err(|_| total_timeout_error())
        .and_then(|result| result);

        match result {
            Ok(false) => Ok(()),
            Ok(true) => {
                self.log_hydration_outcome(started_at, HydrationOutcome::Success);
                Ok(())
            }
            Err(error) => {
                self.log_hydration_outcome(started_at, HydrationOutcome::Failure);
                Err(error)
            }
        }
    }

    async fn hydrate_response_within_timeout(
        &self,
        data: &mut ResponseData,
        source_url: &str,
    ) -> Result<bool, StatsigErr> {
        if get_specs_response_format(data) == SpecsResponseFormat::Protobuf {
            protobuf::hydrate_response(self, data, source_url).await
        } else {
            json::hydrate_response(self, data, source_url).await
        }
    }

    fn log_hydration_success(&self, reference_count: usize, total_bytes: u64) {
        self.log_metric(
            MetricType::Dist,
            HYDRATION_BYTES_METRIC,
            total_bytes as f64,
            None,
        );
        log_d!(
            TAG,
            "Hydrated {} remote dynamic config values ({} bytes)",
            reference_count,
            total_bytes
        );
    }

    fn log_hydration_outcome(&self, started_at: Instant, outcome: HydrationOutcome) {
        let tags = || {
            Some(HashMap::from([(
                "outcome".to_string(),
                outcome.as_str().to_string(),
            )]))
        };
        self.log_metric(MetricType::Increment, HYDRATION_COUNT_METRIC, 1.0, tags());
        self.log_metric(
            MetricType::Dist,
            HYDRATION_LATENCY_METRIC,
            started_at.elapsed().as_secs_f64() * 1000.0,
            tags(),
        );
    }

    async fn download_all(
        &self,
        references: impl IntoIterator<Item = RemoteValueReference>,
    ) -> Result<HashMap<String, Arc<Vec<u8>>>, StatsigErr> {
        stream::iter(references.into_iter().map(|reference| async move {
            let sha256 = reference.metadata.sha256.to_string();
            let value = self.download_one(&reference).await?;
            Ok::<_, StatsigErr>((sha256, value))
        }))
        .buffer_unordered(DOWNLOAD_CONCURRENCY)
        .try_collect::<HashMap<_, _>>()
        .await
    }

    async fn download_one(
        &self,
        reference: &RemoteValueReference,
    ) -> Result<Arc<Vec<u8>>, StatsigErr> {
        let key = SharedDownloadKey::from_reference(reference);
        let download = {
            let active = self
                .in_flight_downloads()
                .entry(key.clone())
                .or_insert_with(|| Arc::new(SharedDownload::default()));
            let download = Arc::clone(active.value());
            download.waiters.fetch_add(1, Ordering::AcqRel);
            download
        };
        let _waiter = SharedDownloadWaiter {
            hydrator: self,
            key,
            download: Arc::clone(&download),
        };

        download
            .result
            .get_or_init(|| self.download_one_uncached(reference))
            .await
            .clone()
    }

    async fn download_one_uncached(
        &self,
        reference: &RemoteValueReference,
    ) -> Result<Arc<Vec<u8>>, StatsigErr> {
        let requested_bytes = u32::try_from(reference.metadata.byte_length)
            .ok()
            .filter(|bytes| *bytes as usize <= MAX_REMOTE_VALUE_BYTES)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TotalBytesExceeded,
                    &format!(
                        "remote value {} exceeded the process hydration byte budget",
                        reference.metadata.sha256
                    ),
                )
            })?;
        let _download_slot = GLOBAL_DOWNLOAD_SLOTS.acquire().await.map_err(|_| {
            hydration_error(
                HydrationFailureReason::DownloadFailed,
                "remote value download concurrency is unavailable",
            )
        })?;
        let _download_bytes = GLOBAL_DOWNLOAD_BYTES
            .acquire_many(requested_bytes)
            .await
            .map_err(|_| {
                hydration_error(
                    HydrationFailureReason::DownloadFailed,
                    "remote value download byte budget is unavailable",
                )
            })?;
        let response = self
            .network
            .get_with_response_limit(
                RequestArgs {
                    url: reference.download_url.to_string(),
                    retries: DOWNLOAD_RETRIES,
                    timeout_ms: DOWNLOAD_TIMEOUT_MS,
                    ..RequestArgs::new()
                },
                reference.metadata.byte_length,
            )
            .await
            .map_err(|error| {
                hydration_error(
                    HydrationFailureReason::DownloadFailed,
                    &format!(
                        "failed to download remote value {}: {}",
                        reference.metadata.sha256, error
                    ),
                )
            })?;

        let response_error = response.error;
        let mut response_data = response.data.ok_or_else(|| {
            let error_suffix = response_error
                .as_deref()
                .map_or(String::new(), |error| format!(": {error}"));
            hydration_error(
                HydrationFailureReason::EmptyResponse,
                &format!(
                    "remote value {} returned no body{error_suffix}",
                    reference.metadata.sha256
                ),
            )
        })?;
        let content_type = response_data
            .get_header_ref("content-type")
            .cloned()
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::MissingResponseContentType,
                    &format!(
                        "remote value {} response omitted Content-Type",
                        reference.metadata.sha256
                    ),
                )
            })?;
        let bytes = read_body_with_limit(&mut response_data, &reference.metadata)?;
        verify_body(&bytes, &reference.metadata, &content_type)?;
        Ok(Arc::new(bytes))
    }

    fn log_metric(
        &self,
        metric_type: MetricType,
        name: &str,
        value: f64,
        tags: Option<HashMap<String, String>>,
    ) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            metric_type,
            name.to_string(),
            value,
            tags,
        ));
    }
}

fn add_raw_value_reference(
    references: &mut HashMap<String, RemoteValueReference>,
    placeholder: Option<&RawValue>,
    metadata: RemoteConfigValueMetadata,
    source_url: &str,
) -> Result<(), StatsigErr> {
    let raw_url = raw_placeholder_url(placeholder.ok_or_else(|| {
        hydration_error(
            HydrationFailureReason::MetadataWithoutValue,
            &format!("remote metadata {} had no matching value", metadata.sha256),
        )
    })?)?;
    let download_url =
        resolve_and_validate_download_url(&raw_url, metadata.sha256.as_str(), source_url)?;
    let sha256 = metadata.sha256.to_string();
    insert_reference(
        references,
        sha256,
        RemoteValueReference {
            download_url,
            metadata,
            occurrences: 1,
        },
    )
}

fn raw_placeholder_url(value: &RawValue) -> Result<String, StatsigErr> {
    if let Ok(url) = serde_json::from_str::<String>(value.get()) {
        return Ok(url);
    }
    if !value.get().trim_start().starts_with('{') {
        return Err(hydration_error(
            HydrationFailureReason::InvalidPlaceholder,
            "remote metadata was attached to a non-URL value",
        ));
    }
    let object: HashMap<String, Box<RawValue>> = serde_json::from_str(value.get())
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))?;
    if object.len() != 1 {
        return Err(hydration_error(
            HydrationFailureReason::InvalidPlaceholder,
            "remote value placeholder must contain only the value field",
        ));
    }
    object
        .get("value")
        .and_then(|value| serde_json::from_str::<String>(value.get()).ok())
        .ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::InvalidPlaceholder,
                "remote value placeholder did not contain a string value field",
            )
        })
}

fn insert_reference(
    references: &mut HashMap<String, RemoteValueReference>,
    sha256: String,
    reference: RemoteValueReference,
) -> Result<(), StatsigErr> {
    let Some(existing) = references.get_mut(&sha256) else {
        references.insert(sha256, reference);
        return Ok(());
    };
    if existing.metadata != reference.metadata {
        return Err(hydration_error(
            HydrationFailureReason::MetadataConflict,
            &format!("remote value {sha256} had conflicting metadata"),
        ));
    }
    existing.occurrences = existing
        .occurrences
        .checked_add(reference.occurrences)
        .ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::TooManyValues,
                "DCS remote value reference count overflowed",
            )
        })?;
    Ok(())
}

fn validate_reference_limits<'a>(
    references: impl IntoIterator<Item = &'a RemoteValueReference>,
) -> Result<(usize, u64), StatsigErr> {
    let mut reference_count = 0usize;
    let mut total_metadata_bytes = 0usize;
    let mut total_bytes = 0u64;

    for reference in references {
        reference_count = reference_count
            .checked_add(reference.occurrences)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TooManyValues,
                    "DCS remote value reference count overflowed",
                )
            })?;
        let reference_metadata_bytes = std::mem::size_of::<RemoteValueReference>()
            .checked_add(reference.download_url.as_str().len())
            .and_then(|bytes| bytes.checked_add(reference.metadata.sha256.as_str().len()))
            .and_then(|bytes| bytes.checked_add(reference.metadata.content_type.as_str().len()))
            .and_then(|bytes| bytes.checked_mul(reference.occurrences))
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TooManyValues,
                    "DCS remote value metadata byte count overflowed",
                )
            })?;
        total_metadata_bytes = total_metadata_bytes
            .checked_add(reference_metadata_bytes)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TooManyValues,
                    "DCS remote value metadata byte count overflowed",
                )
            })?;
        if total_metadata_bytes > MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC {
            return Err(hydration_error(
                HydrationFailureReason::TooManyValues,
                &format!(
                    "DCS remote value metadata totaled {total_metadata_bytes} bytes; maximum is {MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC}"
                ),
            ));
        }

        let reference_bytes = reference
            .metadata
            .byte_length
            .checked_mul(reference.occurrences as u64)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TotalBytesExceeded,
                    "DCS remote value byte count overflowed",
                )
            })?;
        total_bytes = total_bytes.checked_add(reference_bytes).ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::TotalBytesExceeded,
                "DCS remote value byte count overflowed",
            )
        })?;
    }

    Ok((reference_count, total_bytes))
}

fn resolve_and_validate_download_url(
    raw_url: &str,
    sha256: &str,
    source_url: &str,
) -> Result<Url, StatsigErr> {
    let source = Url::parse(source_url).map_err(|error| {
        hydration_error(
            HydrationFailureReason::InvalidSourceUrl,
            &format!("DCS source URL was invalid: {error}"),
        )
    })?;
    let url = source.join(raw_url).map_err(|error| {
        hydration_error(
            HydrationFailureReason::InvalidDownloadUrl,
            &format!("remote value download URL was invalid: {error}"),
        )
    })?;

    if !matches!(url.scheme(), "http" | "https") {
        return Err(hydration_error(
            HydrationFailureReason::InvalidDownloadScheme,
            "remote value download URL must use HTTP or HTTPS",
        ));
    }
    let source_origin = source.origin().ascii_serialization();
    let default_origin = Url::parse(DEFAULT_DOWNLOAD_ORIGIN)
        .expect("default remote value origin must be valid")
        .origin()
        .ascii_serialization();
    let download_origin = url.origin().ascii_serialization();
    if download_origin != source_origin && download_origin != default_origin {
        return Err(hydration_error(
            HydrationFailureReason::UntrustedDownloadOrigin,
            "remote value download URL used an unexpected origin",
        ));
    }

    let expected_path = format!("{DOWNLOAD_PATH_PREFIX}{sha256}");
    if url.path() != expected_path {
        return Err(hydration_error(
            HydrationFailureReason::DownloadPathMismatch,
            &format!(
                "remote value download path did not match metadata {}",
                sha256
            ),
        ));
    }
    if url.query().is_some() || url.fragment().is_some() {
        return Err(hydration_error(
            HydrationFailureReason::InvalidDownloadUrl,
            "remote value download URL must not include a query or fragment",
        ));
    }
    Ok(url)
}

fn verify_body(
    bytes: &[u8],
    metadata: &RemoteConfigValueMetadata,
    response_content_type: &str,
) -> Result<(), StatsigErr> {
    if bytes.len() as u64 != metadata.byte_length {
        return Err(hydration_error(
            HydrationFailureReason::ByteLengthMismatch,
            &format!(
                "remote value {} expected {} bytes but received {}",
                metadata.sha256,
                metadata.byte_length,
                bytes.len()
            ),
        ));
    }
    let normalized = response_content_type
        .split(';')
        .next()
        .unwrap_or_default()
        .trim();
    if normalized != metadata.content_type.as_str() {
        return Err(hydration_error(
            HydrationFailureReason::ResponseContentTypeMismatch,
            &format!(
                "remote value {} expected content type {} but received {}",
                metadata.sha256,
                metadata.content_type.as_str(),
                normalized
            ),
        ));
    }

    let actual_sha = lowercase_hex(&Sha256::digest(bytes));
    if actual_sha != metadata.sha256.as_str() {
        return Err(hydration_error(
            HydrationFailureReason::ChecksumMismatch,
            &format!(
                "remote value {} failed SHA-256 verification",
                metadata.sha256
            ),
        ));
    }
    serde_json::from_slice::<Box<RawValue>>(bytes).map_err(|error| {
        hydration_error(
            HydrationFailureReason::InvalidJson,
            &format!(
                "remote value {} was not valid JSON: {}",
                metadata.sha256, error
            ),
        )
    })?;
    Ok(())
}

fn read_body_with_limit(
    data: &mut ResponseData,
    metadata: &RemoteConfigValueMetadata,
) -> Result<Vec<u8>, StatsigErr> {
    data.rewind()?;

    let read_limit = metadata.byte_length.saturating_add(1);
    let capacity = usize::try_from(metadata.byte_length)
        .unwrap_or(MAX_REMOTE_VALUE_BYTES)
        .min(MAX_REMOTE_VALUE_BYTES);
    let mut bytes = Vec::with_capacity(capacity);
    data.get_stream_mut()
        .take(read_limit)
        .read_to_end(&mut bytes)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;

    if bytes.len() as u64 > metadata.byte_length {
        return Err(hydration_error(
            HydrationFailureReason::ByteLengthMismatch,
            &format!(
                "remote value {} expected {} bytes but received more",
                metadata.sha256, metadata.byte_length
            ),
        ));
    }

    Ok(bytes)
}

fn hydrated_value<'a>(
    hydrated: &'a HashMap<String, Arc<Vec<u8>>>,
    sha256: &str,
) -> Result<&'a [u8], StatsigErr> {
    hydrated
        .get(sha256)
        .map(|value| value.as_slice())
        .ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::MissingHydratedValue,
                &format!("remote value {sha256} was not downloaded"),
            )
        })
}

fn lowercase_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut result = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        result.push(HEX[(byte >> 4) as usize] as char);
        result.push(HEX[(byte & 0x0f) as usize] as char);
    }
    result
}

fn hydration_error(reason: HydrationFailureReason, message: &str) -> StatsigErr {
    StatsigErr::CustomError(format!(
        "Dynamic config hydration failure: {}: {message}",
        reason.as_str()
    ))
}

fn total_timeout_error() -> StatsigErr {
    hydration_error(
        HydrationFailureReason::TotalTimeout,
        "hydration exceeded 30 seconds",
    )
}

#[cfg(test)]
use json::{RawJsonObject, apply_json_hydration, response_may_contain_remote_metadata};
#[cfg(test)]
use protobuf::{
    append_length_delimited_field, decode_protobuf_envelope, encode_delimited_message,
    parse_protobuf_envelopes, parse_raw_protobuf_fields, protobuf_spec_has_remote_metadata,
    serialize_protobuf_envelopes,
};

#[cfg(test)]
#[path = "../__tests__/remote_config_value_hydrator_tests.rs"]
mod tests;
