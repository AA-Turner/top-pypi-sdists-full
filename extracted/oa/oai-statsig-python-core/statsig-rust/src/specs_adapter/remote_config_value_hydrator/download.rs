use std::collections::HashMap;
use std::io::Read;
use std::sync::{
    Arc, OnceLock,
    atomic::{AtomicUsize, Ordering},
};
use std::time::Instant;

use dashmap::DashMap;
use futures::{StreamExt, TryStreamExt, stream};
use serde_json::value::RawValue;
use sha2::{Digest, Sha256};
use tokio::sync::{OnceCell, OwnedSemaphorePermit, Semaphore, TryAcquireError};

use crate::StatsigErr;
use crate::networking::{RequestArgs, ResponseData};

use super::RemoteConfigValueHydrator;
use super::errors::{HydrationFailureReason, hydration_error};
use super::metadata::{
    MAX_REMOTE_VALUE_BYTES, RemoteCompression, RemoteConfigValueMetadata, RemoteContentType,
    RemoteValueReference, Sha256Digest,
};
use super::telemetry::HydrationPhase;

pub(super) const MAX_IN_FLIGHT_HYDRATION_BYTES: usize = 64 * 1024 * 1024;
// Split response reservations into admission and expansion pools so small
// streaming responses do not each consume an entire concurrency window.
pub(super) const MAX_ACTIVE_RESPONSE_RESERVATION_BYTES: usize = MAX_IN_FLIGHT_HYDRATION_BYTES * 2;
pub(crate) const DOWNLOAD_CONCURRENCY: usize = 8;
const DOWNLOAD_RETRIES: u32 = 2;
const DOWNLOAD_TIMEOUT_MS: u64 = 2_000;

static GLOBAL_DOWNLOAD_SLOTS: Semaphore = Semaphore::const_new(DOWNLOAD_CONCURRENCY);
static GLOBAL_DOWNLOAD_BYTES: Semaphore = Semaphore::const_new(MAX_IN_FLIGHT_HYDRATION_BYTES);
pub(super) static GLOBAL_RESPONSE_HYDRATION_BUDGET: OnceLock<Arc<ResponseHydrationBudget>> =
    OnceLock::new();

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub(super) struct SharedDownloadKey {
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
pub(super) struct SharedDownload {
    result: OnceCell<Result<Arc<Vec<u8>>, StatsigErr>>,
    pub(super) waiters: AtomicUsize,
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

pub(super) struct ResponseHydrationBudget {
    pub(super) bytes: Arc<Semaphore>,
    pub(super) expansion: Arc<Semaphore>,
    pub(super) capacity: usize,
}

impl ResponseHydrationBudget {
    pub(super) fn new(capacity: usize) -> Self {
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

    pub(super) async fn reserve(&self, bytes: u64) -> Result<OwnedSemaphorePermit, StatsigErr> {
        self.reserve_from(&self.bytes, bytes).await
    }

    pub(super) async fn reserve_expansion(
        &self,
        bytes: u64,
    ) -> Result<OwnedSemaphorePermit, StatsigErr> {
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

    pub(super) fn try_reserve(
        &self,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.try_reserve_from(&self.bytes, bytes)
    }

    pub(super) fn try_reserve_expansion(
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

impl RemoteConfigValueHydrator {
    pub(super) fn in_flight_downloads(&self) -> &DashMap<SharedDownloadKey, Arc<SharedDownload>> {
        self.in_flight.get_or_init(DashMap::new)
    }

    pub(super) async fn reserve_response_bytes(
        &self,
        bytes: u64,
    ) -> Result<OwnedSemaphorePermit, StatsigErr> {
        let started_at = Instant::now();
        let result = self.response_budget.reserve(bytes).await;
        self.log_phase_latency(started_at.elapsed(), HydrationPhase::ResponsePermit);
        result
    }

    pub(super) fn try_reserve_response_bytes(
        &self,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.response_budget.try_reserve(bytes)
    }

    pub(super) async fn reserve_response_expansion_bytes(
        &self,
        bytes: u64,
    ) -> Result<OwnedSemaphorePermit, StatsigErr> {
        let started_at = Instant::now();
        let result = self.response_budget.reserve_expansion(bytes).await;
        self.log_phase_latency(
            started_at.elapsed(),
            HydrationPhase::ResponseExpansionPermit,
        );
        result
    }

    pub(super) fn try_reserve_response_expansion_bytes(
        &self,
        bytes: u64,
    ) -> Result<Option<OwnedSemaphorePermit>, StatsigErr> {
        self.response_budget.try_reserve_expansion(bytes)
    }

    pub(super) async fn download_all(
        &self,
        references: impl IntoIterator<Item = RemoteValueReference>,
    ) -> Result<HashMap<String, Arc<Vec<u8>>>, StatsigErr> {
        let started_at = Instant::now();
        let result = stream::iter(references.into_iter().map(|reference| async move {
            let sha256 = reference.metadata.sha256.to_string();
            let value = self.download_one(&reference).await?;
            Ok::<_, StatsigErr>((sha256, value))
        }))
        .buffer_unordered(DOWNLOAD_CONCURRENCY)
        .try_collect::<HashMap<_, _>>()
        .await;
        self.log_phase_latency(started_at.elapsed(), HydrationPhase::DownloadWait);
        result
    }

    pub(super) async fn download_one(
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
        let started_at = Instant::now();
        let slot = GLOBAL_DOWNLOAD_SLOTS.acquire().await;
        self.log_phase_latency(started_at.elapsed(), HydrationPhase::DownloadSlotPermit);
        let _download_slot = slot.map_err(|_| {
            hydration_error(
                HydrationFailureReason::DownloadFailed,
                "remote value download concurrency is unavailable",
            )
        })?;
        let started_at = Instant::now();
        let bytes_permit = GLOBAL_DOWNLOAD_BYTES.acquire_many(requested_bytes).await;
        self.log_phase_latency(started_at.elapsed(), HydrationPhase::DownloadBytesPermit);
        let _download_bytes = bytes_permit.map_err(|_| {
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
        let started_at = Instant::now();
        let result = (|| {
            let bytes = read_body_with_limit(&mut response_data, &reference.metadata)?;
            verify_body(&bytes, &reference.metadata, &content_type)?;
            Ok(Arc::new(bytes))
        })();
        self.log_phase_latency(started_at.elapsed(), HydrationPhase::Verify);
        result
    }
}

pub(super) fn verify_body(
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

pub(super) fn read_body_with_limit(
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

pub(super) fn lowercase_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut result = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        result.push(HEX[(byte >> 4) as usize] as char);
        result.push(HEX[(byte & 0x0f) as usize] as char);
    }
    result
}
