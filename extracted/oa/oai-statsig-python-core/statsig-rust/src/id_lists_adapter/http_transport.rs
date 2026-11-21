//! Manifest and body HTTP requests. A successful body request yields a validated
//! snapshot or complete records and their byte range. The caller owns publication.

#[cfg(test)]
use super::TEST_CDN_MANIFEST_URL;
use super::{
    DownloadedIdList, ID_LIST_DOWNLOAD_CONCURRENCY, IdListDownloadJob, PrivateBuildAttempt,
    publication_stopped, snapshot_http,
};
use crate::id_lists_adapter::{
    IdListManifest,
    id_list_load_timing::{self, Phase},
    id_list_propagation::downloaded_range,
};
use crate::networking::HttpMethod;
use crate::networking::retry::{
    PrimaryOutcome, RefreshFailureTracker, RetryPolicy, retryable_state_error,
};
use crate::networking::{
    DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, NetworkClient, NetworkError, RequestArgs, Response,
    ResponseData, default_cdn_id_lists_manifest_url, is_default_cdn_id_lists_manifest_url,
    is_default_cdn_url, normalize_default_cdn_id_lists_manifest_url, replace_url_base,
};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::portable_id_list_ef;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::{StatsigErr, StatsigOptions};
use std::{collections::HashMap, io::Read, ops::Range, sync::Arc};
use tokio::sync::Semaphore;

const DEFAULT_RETRY_POLICY: RetryPolicy = RetryPolicy {
    attempts: 2,
    jitter: true,
};

// Canonical records need ten bytes including LF, even with one-byte responses.
const MAX_ID_LIST_RECORD_CONTINUATIONS: usize = 64;
const MAX_UNFINISHED_ID_LIST_RECORD_BYTES: usize = 64 * 1024;

pub(super) struct IdListHttpTransport {
    pub(super) network: Arc<NetworkClient>,
    ops_stats: Arc<OpsStatsForInstance>,
    manifest_failures: RefreshFailureTracker,
    pub(super) download_permits: Arc<Semaphore>,
    retry_policy: RetryPolicy,
    pub(super) id_lists_manifest_url: String,
    download_id_list_file_api: Option<Result<url::Url, url::ParseError>>,
    pub(super) snapshot_enabled: bool,
    pub(super) fallback_url: Option<String>,
    fallback_to_statsig_api: bool,
}

impl IdListHttpTransport {
    pub(super) fn new(
        sdk_key: &str,
        options: &StatsigOptions,
        ops_stats: Arc<OpsStatsForInstance>,
    ) -> Self {
        let id_lists_manifest_url =
            normalize_default_cdn_id_lists_manifest_url(options.id_lists_url.as_deref());

        let mut fallback_url = None;
        if options.fallback_to_statsig_api == Some(true)
            && !id_lists_manifest_url.contains(DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX)
        {
            let url = default_cdn_id_lists_manifest_url();
            #[cfg(test)]
            let url = TEST_CDN_MANIFEST_URL.try_with(Clone::clone).unwrap_or(url);
            fallback_url = Some(url);
        }

        let retry_override = RetryPolicy::state_read_override(options.state_read_primary_attempts);

        let download_id_list_file_api = options
            .download_id_list_file_api
            .as_deref()
            .map(url::Url::parse);
        let snapshot_enabled = options.enable_id_list_elias_fano == Some(true)
            && matches!(&download_id_list_file_api, Some(Ok(endpoint)) if snapshot_http::supports_snapshots(endpoint));

        Self {
            network: Arc::new(NetworkClient::with_sdk_headers(sdk_key, options)),
            ops_stats,
            manifest_failures: RefreshFailureTracker::default(),
            download_permits: Arc::new(Semaphore::new(ID_LIST_DOWNLOAD_CONCURRENCY)),
            retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            id_lists_manifest_url,
            download_id_list_file_api,
            snapshot_enabled,
            fallback_url,
            fallback_to_statsig_api: options.fallback_to_statsig_api == Some(true),
        }
    }

    pub(super) fn can_download_snapshots(&self) -> bool {
        self.snapshot_enabled && self.network.supports_response_headers_without_redirects()
    }

    pub(super) async fn fetch_id_list_manifests_from_network(
        &self,
        background: bool,
    ) -> Result<IdListManifest, StatsigErr> {
        let result = self
            .network
            .retry_executor(self.retry_policy)
            .run(
                |fallback, index| async move {
                    let url = if fallback {
                        self.network.log_fallback("id_list_manifest", true);
                        self.fallback_url.as_ref().unwrap()
                    } else {
                        &self.id_lists_manifest_url
                    };
                    let method = if fallback || self.is_cdn_url() {
                        HttpMethod::GET
                    } else {
                        HttpMethod::POST
                    };
                    let response = self
                        .network
                        .request_once(
                            method,
                            RequestArgs {
                                url: url.clone(),
                                accept_gzip_response: true,
                                diagnostics_key: Some(KeyType::GetIDListSources),
                                retries: self.retry_policy.attempts - 1,
                                ..RequestArgs::new()
                            },
                            None,
                            false,
                            true,
                            index,
                        )
                        .await
                        .map_err(StatsigErr::NetworkError)?;
                    self.parse_response(response.data)
                },
                |error| retryable_state_error(error).then_some(u32::MAX),
                |outcome| {
                    let eligible = self.manifest_failures.record(outcome, background);
                    if outcome == PrimaryOutcome::Exhausted
                        && self.fallback_url.is_some()
                        && !eligible
                    {
                        self.network.log_fallback("id_list_manifest", false);
                    }
                    eligible && self.fallback_url.is_some()
                },
                || {
                    StatsigErr::NetworkError(NetworkError::ShutdownError(
                        self.id_lists_manifest_url.clone(),
                    ))
                },
            )
            .await;

        let (metric_name, metric_value) = if result.is_ok() {
            ("id_list_manifest_download_success", 1.0)
        } else {
            ("id_list_manifest_download_failure", 1.0)
        };
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            metric_name.to_string(),
            metric_value,
            None,
        ));

        result
    }

    pub(super) async fn download_job(
        &self,
        job: &IdListDownloadJob,
        is_fallback: bool,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<DownloadedIdList, StatsigErr> {
        if is_fallback && !self.file_can_fallback(job) {
            return Err(StatsigErr::NetworkError(NetworkError::RequestNotRetryable(
                job.primary_url.clone(),
                None,
                "No trusted fallback destination".into(),
            )));
        }
        self.network
            .retry_executor(if is_fallback {
                RetryPolicy {
                    attempts: 1,
                    jitter: false,
                }
            } else {
                self.retry_policy
            })
            .run(
                |_, index| {
                    self.download_id_list(
                        job,
                        is_fallback,
                        if is_fallback {
                            self.retry_policy.attempts
                        } else {
                            index
                        },
                        build,
                    )
                },
                |error| retryable_state_error(error).then_some(u32::MAX),
                |_| false,
                || StatsigErr::NetworkError(NetworkError::ShutdownError(job.primary_url.clone())),
            )
            .await
    }

    pub(super) async fn download_id_list(
        &self,
        job: &IdListDownloadJob,
        is_fallback: bool,
        index: u32,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<DownloadedIdList, StatsigErr> {
        let started = id_list_load_timing::start_phase();
        let download_permit = self.download_permits.clone().acquire_owned().await;
        id_list_load_timing::end_phase(Phase::DownloadPermitWait, started);
        let download_permit = download_permit.map_err(|_| publication_stopped())?;
        let download_url = if is_fallback {
            self.network.log_fallback("id_list_file", true);
            &job.metadata.url
        } else {
            &job.primary_url
        };
        // Only carry a fragment when this attempt has yet to receive a whole record.
        // A retry, fallback, or new manifest starts from the listener's committed cursor.
        let mut pending = PartialIdListRecord::default();
        for _ in 0..=MAX_ID_LIST_RECORD_CONTINUATIONS {
            let start = job.range_start + pending.bytes.len() as u64;
            let offer_snapshot =
                job.can_download_snapshots && !is_fallback && index == 0 && start == 0;
            let request =
                self.id_list_file_request_args(download_url, job, start, &pending, offer_snapshot);
            let started = id_list_load_timing::start_phase();
            let response = self
                .network
                .request_once(
                    HttpMethod::GET,
                    request,
                    None,
                    is_fallback || job.can_download_snapshots,
                    true,
                    index,
                )
                .await;
            id_list_load_timing::end_phase(Phase::HttpBody, started);
            let response = response.map_err(StatsigErr::NetworkError)?;
            if response
                .data
                .as_ref()
                .is_some_and(snapshot_http::is_snapshot_response)
            {
                if !offer_snapshot {
                    return Err(StatsigErr::InvalidOperation(
                        "unsolicited ID-list snapshot".into(),
                    ));
                }
                let list = self
                    .validate_snapshot(job, response, download_permit, build)
                    .await?;
                return Ok(DownloadedIdList::Snapshot(list));
            }
            self.add_process_start_marker(KeyType::GetIDList, None, Some(download_url));
            let started = id_list_load_timing::start_phase();
            let chunk = normalize_id_list_download(
                response,
                download_url,
                job.range_start,
                job.metadata.size,
                job.can_download_snapshots,
                pending,
            );
            id_list_load_timing::end_phase(Phase::Decode, started);
            self.add_process_end_marker(KeyType::GetIDList, chunk.is_ok(), Some(download_url));
            match chunk? {
                RawIdListChunk::Complete(changeset, range) => {
                    return Ok(DownloadedIdList::Raw { changeset, range });
                }
                RawIdListChunk::Incomplete(record) => pending = record,
            }
        }
        Err(StatsigErr::CustomError(
            "Too many partial responses for one ID-list record".into(),
        ))
    }

    pub(super) fn file_can_fallback(&self, job: &IdListDownloadJob) -> bool {
        self.fallback_to_statsig_api
            && job.primary_url != job.metadata.url
            && is_default_cdn_url(&job.metadata.url)
    }

    fn id_list_file_request_args(
        &self,
        list_url: &str,
        job: &IdListDownloadJob,
        start: u64,
        pending: &PartialIdListRecord,
        offer_snapshot: bool,
    ) -> RequestArgs {
        let mut request_url = list_url.to_string();
        // A manifest may contain a legacy query range. Every destination uses
        // one representation URL and the HTTP Range header to slice it.
        if let Ok(mut url) = url::Url::parse(list_url) {
            if url
                .query_pairs()
                .any(|(key, _)| key.eq_ignore_ascii_case("range"))
            {
                let params: Vec<_> = url
                    .query_pairs()
                    .filter(|(key, _)| !key.eq_ignore_ascii_case("range"))
                    .map(|(key, value)| (key.into_owned(), value.into_owned()))
                    .collect();
                url.set_query(None);
                if !params.is_empty() {
                    url.query_pairs_mut().extend_pairs(params);
                }
                request_url = url.to_string();
            }
        }

        let range = format!("bytes={start}-");
        let mut headers = HashMap::from([
            ("Range".into(), range),
            (
                "statsig-id-list-file-size".into(),
                job.metadata.size.to_string(),
            ),
            // Byte offsets refer to the unencoded append log.
            ("Accept-Encoding".into(), "identity".into()),
        ]);
        if offer_snapshot {
            headers.insert("Accept".into(), portable_id_list_ef::MEDIA_TYPE.into());
        }
        if let Some(etag) = pending
            .etag
            .as_ref()
            .filter(|tag| tag.starts_with('"') && tag.ends_with('"'))
        {
            headers.insert("If-Range".into(), etag.clone());
        }
        RequestArgs {
            url: request_url,
            headers: Some(headers),
            id_list_file_id: job.metadata.file_id.clone(),
            diagnostics_key: Some(KeyType::GetIDList),
            retries: self.retry_policy.attempts - 1,
            ..RequestArgs::new()
        }
    }

    pub(super) fn get_override_id_list_download_url(
        &self,
        list_url: &str,
    ) -> Result<String, StatsigErr> {
        match &self.download_id_list_file_api {
            None => Ok(list_url.to_string()),
            Some(Ok(endpoint)) => replace_url_base(endpoint, list_url).map(Into::into),
            Some(Err(_)) => Err(StatsigErr::InvalidOperation(
                "invalid ID-list file endpoint".into(),
            )),
        }
    }

    pub(super) fn is_cdn_url(&self) -> bool {
        is_default_cdn_id_lists_manifest_url(&self.id_lists_manifest_url)
    }

    fn parse_response(&self, response: Option<ResponseData>) -> Result<IdListManifest, StatsigErr> {
        let mut data = match response {
            Some(r) => r,
            None => {
                let msg = "No ID List results from network".to_string();
                return Err(StatsigErr::JsonParseError(
                    "IdListsResponse".to_owned(),
                    msg,
                ));
            }
        };

        data.deserialize_into::<IdListManifest>()
    }

    pub(super) fn add_process_start_marker(
        &self,
        key: KeyType,
        id_list_count: Option<usize>,
        url: Option<&str>,
    ) {
        if self.ops_stats.remote_telemetry_disabled() {
            return;
        }
        let mut marker = Marker::new(key, ActionType::Start, Some(StepType::Process));
        if let Some(count) = id_list_count {
            marker = marker.with_id_list_count(count);
        }
        if let Some(url) = url {
            marker = marker.with_url(url.to_string());
        }
        self.ops_stats.add_marker(marker, None);
    }

    pub(super) fn add_process_end_marker(&self, key: KeyType, success: bool, url: Option<&str>) {
        if self.ops_stats.remote_telemetry_disabled() {
            return;
        }
        let mut marker =
            Marker::new(key, ActionType::End, Some(StepType::Process)).with_is_success(success);
        if let Some(url) = url {
            marker = marker.with_url(url.to_string());
        }
        self.ops_stats.add_marker(marker, None);
    }
}

#[derive(Debug, PartialEq)]
enum RawIdListChunk {
    Complete(String, Range<u64>),
    Incomplete(PartialIdListRecord),
}

#[derive(Default, Debug, PartialEq)]
struct PartialIdListRecord {
    bytes: Vec<u8>,
    total: u64,
    etag: Option<String>,
}

fn normalize_id_list_download(
    response: Response,
    download_url: &str,
    committed_start: u64,
    manifest_size: u64,
    check_snapshot_body: bool,
    mut pending: PartialIdListRecord,
) -> Result<RawIdListChunk, StatsigErr> {
    let status = response.status_code;
    let request_failed = |msg: &str| {
        StatsigErr::NetworkError(NetworkError::RequestFailed(
            download_url.into(),
            status,
            msg.into(),
        ))
    };
    let stale = || request_failed("ID-list response is stale or changed during download");
    let invalid = |msg: &str| StatsigErr::CustomError(msg.into());
    let decode = |bytes| {
        String::from_utf8(bytes)
            .map_err(|err| StatsigErr::JsonParseError("ResponseData".into(), err.to_string()))
    };
    let mut body = response
        .data
        .ok_or_else(|| request_failed("Missing ID list body"))?;
    let mut bytes = if body
        .get_header_ignore_ascii_case("content-encoding")
        .is_some_and(|encoding| encoding.trim().eq_ignore_ascii_case("gzip"))
    {
        // A server that ignores Accept-Encoding: identity can gzip raw records too.
        body.rewind()?;
        let mut bytes = Vec::new();
        flate2::read::MultiGzDecoder::new(body.get_stream_mut())
            .read_to_end(&mut bytes)
            .map_err(|err| request_failed(&err.to_string()))?;
        bytes
    } else {
        body.read_to_bytes()?
    };
    // A proxy can strip the snapshot headers even when the body is valid UTF-8.
    let reject_snapshot = |prefix: &[u8], total| {
        if portable_id_list_ef::matches_v1_prefix(prefix, total) {
            return Err(request_failed(
                "Received a binary ID-list snapshot as raw data",
            ));
        }
        Ok(())
    };
    if check_snapshot_body {
        reject_snapshot(&bytes, bytes.len() as u64)?;
    }
    let content_range = body.get_header_ignore_ascii_case("content-range");
    if status == Some(200) && content_range.is_none() {
        let mut text = decode(bytes)?;
        let end = text.len() as u64;
        // SFP may have useful bytes without having reached the manifest size yet.
        if end < committed_start || (end == committed_start && end < manifest_size) {
            return Err(stale());
        }
        // A whole response also supplies any in-flight fragment. Replay from
        // the committed record boundary using only this representation.
        let start = committed_start as usize; // bounded by the body length above
        if !text.is_char_boundary(start) {
            return Err(invalid("ID-list download offset splits a UTF-8 character"));
        }
        if start != 0 {
            text = text.split_off(start);
        }
        return Ok(RawIdListChunk::Complete(text, committed_start..end));
    }
    if !matches!(status, Some(200 | 206)) {
        return Err(invalid(
            "ID-list download returned an unexpected response status or Content-Range",
        ));
    }
    let (range, total) = content_range
        .and_then(|header| downloaded_range(header, bytes.len()))
        .ok_or_else(|| invalid("ID-list download returned an invalid Content-Range"))?;
    if range.start != committed_start + pending.bytes.len() as u64 || range.is_empty() {
        return Err(invalid(
            "ID-list download returned an unexpected or empty byte range",
        ));
    }

    // Unversioned responses rely on the append-only file named in the manifest.
    // Retry from the committed boundary if the server identifies a different object.
    let etag = || body.get_header_ignore_ascii_case("etag");
    if total < pending.total
        || pending
            .etag
            .as_ref()
            .is_some_and(|old| etag().is_some_and(|new| new != old))
    {
        return Err(stale());
    }

    // A range can split the count itself, which can contain an LF. Inspect the
    // prefix against the whole representation before publishing a line.
    if check_snapshot_body && committed_start == 0 {
        if !pending.bytes.is_empty() && pending.bytes.len() < portable_id_list_ef::V1_COUNT_BYTES {
            bytes.splice(..0, pending.bytes.drain(..));
        }
        let prefix = if pending.bytes.is_empty() {
            &bytes
        } else {
            &pending.bytes
        };
        reject_snapshot(prefix, total)?;
    }

    // A record without LF is complete only at the representation's EOF. Return
    // complete lines now and ask for any trailing fragment again next refresh.
    let complete_len = if range.end == total {
        Some(bytes.len())
    } else {
        memchr::memrchr(b'\n', &bytes)
            .filter(|_| {
                !(check_snapshot_body
                    && committed_start == 0
                    && range.end < portable_id_list_ef::V1_COUNT_BYTES as u64
                    && portable_id_list_ef::matches_partial_v1_count(&bytes, total))
            })
            .map(|i| i + 1)
    };
    if let Some(len) = complete_len {
        bytes.truncate(len);
    } else if pending.bytes.len() + bytes.len() > MAX_UNFINISHED_ID_LIST_RECORD_BYTES {
        return Err(invalid("Unterminated ID-list record is too large"));
    }
    if !pending.bytes.is_empty() {
        pending.bytes.extend_from_slice(&bytes);
        bytes = pending.bytes;
    }
    if complete_len.is_none() {
        return Ok(RawIdListChunk::Incomplete(PartialIdListRecord {
            bytes,
            total,
            etag: pending.etag.or_else(|| etag().cloned()),
        }));
    }
    let end = committed_start + bytes.len() as u64;
    let text = decode(bytes)?;
    Ok(RawIdListChunk::Complete(text, committed_start..end))
}

#[cfg(test)]
#[path = "__tests__/id_list_range_tests.rs"]
mod range_tests;
