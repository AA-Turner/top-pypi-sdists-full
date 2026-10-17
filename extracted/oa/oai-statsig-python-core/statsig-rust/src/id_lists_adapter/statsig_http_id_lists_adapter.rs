use super::IdListMetadata;
use super::id_list_propagation::{IdListManifestEntry, downloaded_range};
use crate::id_lists_adapter::{IdListUpdate, IdListsAdapter, IdListsUpdateListener};
use crate::networking::HttpMethod;
use crate::networking::retry::{
    PrimaryOutcome, RefreshFailureTracker, RetryPolicy, retryable_state_error,
};
use crate::networking::{
    DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, NetworkClient, NetworkError, RequestArgs,
    ResponseData, default_cdn_id_lists_manifest_url, is_default_cdn_id_lists_manifest_url,
    is_default_cdn_url, normalize_default_cdn_id_lists_manifest_url, replace_url_base,
};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::statsig_metadata::StatsigMetadata;
use crate::{
    StatsigErr, StatsigOptions, StatsigRuntime, log_d, log_e, log_error_to_statsig_and_console,
};
use async_trait::async_trait;
use chrono::Utc;
use futures::{StreamExt, stream};
use parking_lot::RwLock;
use std::collections::HashMap;
use std::sync::{Arc, Weak};
use std::time::Duration;
use tokio::sync::Notify;
use tokio::time::sleep;

const DEFAULT_RETRY_POLICY: RetryPolicy = RetryPolicy {
    attempts: 2,
    jitter: true,
};

const DEFAULT_ID_LIST_SYNC_INTERVAL_MS: u32 = 60_000;
const ID_LIST_DOWNLOAD_CONCURRENCY: usize = 4;

type IdListsResponse = HashMap<String, IdListMetadata>;
type IdListsManifest = HashMap<String, IdListManifestEntry>;

const TAG: &str = stringify!(StatsigHttpIdListsAdapter);
const ID_LISTS_SYNC_OVERALL_LATENCY_METRIC: &str = "id_lists_sync_overall.latency";
const ID_LISTS_SYNC_OVERALL_MANIFEST_SUCCESS_TAG: &str = "id_list_manifest_success";
const ID_LISTS_SYNC_OVERALL_SUCCEED_SINGLE_ID_LIST_NUMBER_TAG: &str =
    "succeed_single_id_list_number";

pub struct StatsigHttpIdListsAdapter {
    output_policy: crate::output_policy::OutputPolicy,
    manifest_retry_policy: RetryPolicy,
    file_retry_policy: RetryPolicy,
    id_lists_manifest_url: String,
    download_id_list_file_api: Option<String>,
    fallback_url: Option<String>,
    fallback_to_statsig_api: bool,
    listener: RwLock<Option<Arc<dyn IdListsUpdateListener>>>,
    network: NetworkClient,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    shutdown_notify: Arc<Notify>,
    manifest_failures: RefreshFailureTracker,
    file_failures: RefreshFailureTracker,
}

impl StatsigHttpIdListsAdapter {
    #[must_use]
    pub fn new(sdk_key: &str, options: &StatsigOptions) -> Self {
        let output_policy = crate::output_policy::OutputPolicy::from_options(Some(options));
        let _output_scope = output_policy.enter();
        let id_lists_manifest_url =
            normalize_default_cdn_id_lists_manifest_url(options.id_lists_url.as_deref());

        let mut fallback_url = None;
        if options.fallback_to_statsig_api == Some(true)
            && !id_lists_manifest_url.contains(DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX)
        {
            fallback_url = Some(default_cdn_id_lists_manifest_url());
        }

        let sync_interval_duration = Duration::from_millis(u64::from(
            options
                .id_lists_sync_interval_ms
                .unwrap_or(DEFAULT_ID_LIST_SYNC_INTERVAL_MS),
        ));

        let headers =
            StatsigMetadata::get_constant_request_headers(sdk_key, options.service_name.as_deref());
        let network = NetworkClient::new(sdk_key, Some(headers), Some(options));

        let sdk_instance_id = options.get_sdk_instance_id(sdk_key);
        let retry_override = RetryPolicy::state_read_override(options.state_read_primary_attempts);

        Self {
            output_policy,
            manifest_retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            file_retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            id_lists_manifest_url,
            download_id_list_file_api: options.download_id_list_file_api.clone(),
            fallback_url,
            fallback_to_statsig_api: options.fallback_to_statsig_api == Some(true),
            listener: RwLock::new(None),
            network,
            sync_interval_duration,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            shutdown_notify: Arc::new(Notify::new()),
            manifest_failures: RefreshFailureTracker::default(),
            file_failures: RefreshFailureTracker::default(),
        }
    }

    pub fn force_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.network.shutdown();
        self.shutdown_notify.notify_one();
    }

    async fn fetch_id_list_manifests_from_network(
        &self,
        background: bool,
    ) -> Result<IdListsManifest, StatsigErr> {
        let result = self
            .network
            .retry_executor(self.manifest_retry_policy)
            .run(
                |fallback, index| async move {
                    if fallback {
                        self.network.log_fallback("id_list_manifest", true);
                    }
                    let url = if fallback {
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
                                retries: self.manifest_retry_policy.attempts - 1,
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

    async fn download_id_list_with_retries(
        &self,
        job: &IdListDownloadJob,
        is_fallback: bool,
    ) -> Result<(String, std::ops::Range<u64>), StatsigErr> {
        if is_fallback && !self.file_can_fallback(job) {
            return Err(StatsigErr::NetworkError(NetworkError::RequestNotRetryable(
                job.url.clone(),
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
                self.file_retry_policy
            })
            .run(
                |_, index| {
                    self.download_id_list(
                        job,
                        is_fallback,
                        if is_fallback {
                            self.file_retry_policy.attempts
                        } else {
                            index
                        },
                    )
                },
                |error| retryable_state_error(error).then_some(u32::MAX),
                |_| false,
                || StatsigErr::NetworkError(NetworkError::ShutdownError(job.url.clone())),
            )
            .await
    }

    async fn download_id_list(
        &self,
        job: &IdListDownloadJob,
        is_fallback: bool,
        index: u32,
    ) -> Result<(String, std::ops::Range<u64>), StatsigErr> {
        if is_fallback {
            self.network.log_fallback("id_list_file", true);
        }
        let download_url = if is_fallback {
            &job.metadata.url
        } else {
            &job.url
        };
        let mut request = Self::id_list_file_request_args(
            download_url,
            job.range_start,
            job.metadata.size,
            job.metadata.file_id.clone(),
        );
        request.retries = self.file_retry_policy.attempts - 1;
        // Only the captured trusted CDN may receive fallback credentials; redirects stay disabled.
        let response = self
            .network
            .request_once(HttpMethod::GET, request, None, is_fallback, true, index)
            .await
            .map_err(StatsigErr::NetworkError)?;
        self.add_diagnostics_start_marker(
            KeyType::GetIDList,
            StepType::Process,
            None,
            Some(download_url.clone()),
        );
        let result = match response.data {
            Some(mut body) => body.read_to_string().and_then(|text| {
                normalize_id_list_download(
                    response.status_code,
                    body.get_header_ref("content-range").map(String::as_str),
                    job.range_start,
                    job.metadata.size,
                    text,
                )
                .map_err(|message| StatsigErr::CustomError(message.to_string()))?
                .ok_or_else(|| {
                    StatsigErr::NetworkError(NetworkError::RequestFailed(
                        download_url.clone(),
                        response.status_code,
                        "ID-list download returned no unread bytes".into(),
                    ))
                })
            }),
            None => Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
                download_url.clone(),
                response.status_code,
                "Missing ID list body".into(),
            ))),
        };
        self.add_diagnostics_end_marker(
            KeyType::GetIDList,
            StepType::Process,
            result.is_ok(),
            None,
            Some(download_url.clone()),
        );
        result
    }

    fn file_can_fallback(&self, job: &IdListDownloadJob) -> bool {
        self.fallback_to_statsig_api
            && job.url != job.metadata.url
            && is_default_cdn_url(&job.metadata.url)
    }

    fn id_list_file_request_args(
        list_url: &str,
        start_index: u64,
        new_file_size: u64,
        id_list_file_id: Option<String>,
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

        RequestArgs {
            url: request_url,
            headers: Some(HashMap::from([
                ("Range".into(), format!("bytes={start_index}-")),
                (
                    "statsig-id-list-file-size".into(),
                    new_file_size.to_string(),
                ),
                // Byte offsets refer to the unencoded append log.
                ("Accept-Encoding".into(), "identity".into()),
            ])),
            id_list_file_id,
            // Each request is one attempt in the adapter-owned retry budget.
            diagnostics_key: Some(KeyType::GetIDList),
            retries: 0,
            ..RequestArgs::new()
        }
    }

    fn get_override_id_list_download_url(&self, list_url: &str) -> String {
        let Some(override_api) = &self.download_id_list_file_api else {
            return list_url.to_string();
        };

        replace_url_base(override_api, list_url)
    }

    async fn run_background_sync(weak_self: &Weak<Self>) {
        let strong_self = match weak_self.upgrade() {
            Some(s) => s,
            None => return,
        };

        strong_self
            .ops_stats
            .set_diagnostics_context(ContextType::ConfigSync);

        if let Err(e) = strong_self.sync_id_lists_with_trigger(true).await {
            if let StatsigErr::NetworkError(NetworkError::DisableNetworkOn(_)) = e {
                return;
            }
            log_e!(TAG, "IDList background sync failed {}", e);
        }

        strong_self.ops_stats.enqueue_diagnostics_event(
            Some(KeyType::GetIDListSources),
            Some(ContextType::ConfigSync),
        );
    }

    fn is_cdn_url(&self) -> bool {
        is_default_cdn_id_lists_manifest_url(&self.id_lists_manifest_url)
    }

    fn parse_response(
        &self,
        response: Option<ResponseData>,
    ) -> Result<IdListsManifest, StatsigErr> {
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

        data.deserialize_into::<IdListsManifest>()
    }

    pub(crate) fn set_listener(&self, listener: Arc<dyn IdListsUpdateListener>) {
        match self
            .listener
            .try_write_for(std::time::Duration::from_secs(5))
        {
            Some(mut lock) => *lock = Some(listener),
            None => {
                log_error_to_statsig_and_console!(
                    self.ops_stats.clone(),
                    TAG,
                    StatsigErr::LockFailure("Failed to acquire write lock on listener".to_string())
                );
            }
        }
    }

    fn get_current_id_list_metadata(&self) -> Result<HashMap<String, IdListMetadata>, StatsigErr> {
        let lock = match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => lock,
            None => {
                return Err(StatsigErr::LockFailure(
                    "Failed to acquire read lock on listener".to_string(),
                ));
            }
        };

        match lock.as_ref() {
            Some(listener) => Ok(listener.get_current_id_list_metadata()),
            None => Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
        }
    }

    async fn sync_id_lists(&self) -> Result<(), StatsigErr> {
        self.sync_id_lists_with_trigger(false).await
    }

    async fn sync_id_lists_with_trigger(&self, background: bool) -> Result<(), StatsigErr> {
        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        let mut manifest_success = false;
        let mut successful_downloads = 0;
        let result = self
            .fetch_and_process_id_lists(
                &mut manifest_success,
                &mut successful_downloads,
                background,
            )
            .await;
        self.log_id_lists_sync_overall_latency(
            sync_start_ms,
            manifest_success,
            successful_downloads,
            result.is_ok(),
        );
        result
    }

    async fn fetch_and_process_id_lists(
        &self,
        manifest_success: &mut bool,
        successful_downloads: &mut u64,
        background: bool,
    ) -> Result<(), StatsigErr> {
        let new_manifest = self
            .fetch_id_list_manifests_from_network(background)
            .await?;
        *manifest_success = true;
        // Capture both manifests once; retries never reread committed metadata.
        let curr_manifest = self.get_current_id_list_metadata()?;
        self.add_diagnostics_start_marker(
            KeyType::GetIDListSources,
            StepType::Process,
            Some(new_manifest.len()),
            None,
        );
        let result = self
            .process_id_lists(
                new_manifest,
                curr_manifest,
                successful_downloads,
                background,
            )
            .await;
        self.add_diagnostics_end_marker(
            KeyType::GetIDListSources,
            StepType::Process,
            result.is_ok(),
            None,
            None,
        );
        result
    }

    async fn process_id_lists(
        &self,
        new_manifest: IdListsManifest,
        curr_manifest: IdListsResponse,
        successful_downloads: &mut u64,
        background: bool,
    ) -> Result<(), StatsigErr> {
        let mut jobs = Vec::new();
        let mut updates = HashMap::new();
        let mut propagation = HashMap::with_capacity(new_manifest.len());
        for (name, entry) in new_manifest {
            propagation.insert(name.clone(), entry.propagation_update());
            let metadata = entry.metadata;
            let range_start = match curr_manifest.get(&name) {
                Some(current)
                    if metadata.creation_time > current.creation_time
                        || metadata.file_id != current.file_id =>
                {
                    Some(0)
                }
                Some(current) if metadata.size > current.size => Some(current.size),
                Some(_) => None,
                None => Some(0),
            };
            if let Some(range_start) = range_start {
                jobs.push(IdListDownloadJob {
                    name,
                    url: self.get_override_id_list_download_url(&metadata.url),
                    metadata,
                    range_start,
                });
            } else {
                updates.insert(
                    name,
                    IdListUpdate {
                        raw_changeset: None,
                        new_metadata: metadata,
                    },
                );
            }
        }
        // Stable launch order also makes failures reproducible across manifest map orderings.
        jobs.sort_by(|a, b| a.name.cmp(&b.name));
        if !jobs.is_empty() {
            let pending = parking_lot::Mutex::new(jobs);
            let completed = parking_lot::Mutex::new(Vec::new());
            let result = self
                .network
                .retry_executor(RetryPolicy {
                    attempts: 1,
                    jitter: false,
                })
                .run(
                    |is_fallback, _| {
                        let pending = &pending;
                        let completed = &completed;
                        async move {
                            let jobs = std::mem::take(&mut *pending.lock());
                            let mut downloads =
                                stream::iter(jobs.into_iter().map(|job| async move {
                                    let result =
                                        self.download_id_list_with_retries(&job, is_fallback).await;
                                    (job, result)
                                }))
                                .buffer_unordered(ID_LIST_DOWNLOAD_CONCURRENCY);
                            let mut failure = None;
                            while let Some((job, result)) = downloads.next().await {
                                match result {
                                    Ok(body) => completed.lock().push((job, body)),
                                    Err(error) => {
                                        // A terminal error takes precedence over exhausted retryable files.
                                        if failure.as_ref().is_none_or(retryable_state_error) {
                                            failure = Some(error);
                                        }
                                        pending.lock().push(job);
                                    }
                                }
                            }
                            failure.map_or(Ok(()), Err)
                        }
                    },
                    |error| retryable_state_error(error).then_some(u32::MAX),
                    |outcome| {
                        let eligible = self.file_failures.record(outcome, background);
                        let has_fallback =
                            pending.lock().iter().any(|job| self.file_can_fallback(job));
                        if outcome == PrimaryOutcome::Exhausted && has_fallback && !eligible {
                            self.network.log_fallback("id_list_file", false);
                        }
                        eligible && has_fallback
                    },
                    || {
                        StatsigErr::NetworkError(NetworkError::ShutdownError(
                            self.id_lists_manifest_url.clone(),
                        ))
                    },
                )
                .await;
            let completed = completed.into_inner();
            *successful_downloads += completed.len() as u64;
            result?;
            for (job, (raw_changeset, applied_range)) in completed {
                if let Some(observation) = propagation.get_mut(&job.name) {
                    observation.applied_range = Some(applied_range);
                }
                updates.insert(
                    job.name,
                    IdListUpdate {
                        raw_changeset: Some(raw_changeset),
                        new_metadata: job.metadata,
                    },
                );
            }
        }
        match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => match lock.as_ref() {
                Some(listener) => {
                    listener.did_receive_id_list_updates_with_propagation(updates, propagation);
                    Ok(())
                }
                None => Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
            },
            None => {
                let error = "Failed to acquire read lock on listener".to_string();
                log_error_to_statsig_and_console!(
                    self.ops_stats.clone(),
                    TAG,
                    StatsigErr::LockFailure(error.clone())
                );
                Err(StatsigErr::LockFailure(error))
            }
        }
    }

    // ---- Helper functions for monioring ID List ----
    fn add_diagnostics_start_marker(
        &self,
        key: KeyType,
        step: StepType,
        id_list_count: Option<usize>,
        url: Option<String>,
    ) {
        let mut marker = Marker::new(key, ActionType::Start, Some(step));
        if let Some(count) = id_list_count {
            marker = marker.with_id_list_count(count);
        }
        if let Some(url) = url {
            marker = marker.with_url(url);
        }
        self.ops_stats.add_marker(marker, None);
    }

    fn add_diagnostics_end_marker(
        &self,
        key: KeyType,
        step: StepType,
        success: bool,
        status_code: Option<u16>,
        url: Option<String>,
    ) {
        let mut marker = Marker::new(key, ActionType::End, Some(step)).with_is_success(success);
        if let Some(status_code) = status_code {
            marker = marker.with_status_code(status_code);
        }
        if let Some(url) = url {
            marker = marker.with_url(url);
        }
        self.ops_stats.add_marker(marker, None);
    }

    fn log_id_lists_sync_overall_latency(
        &self,
        sync_start_ms: u64,
        id_list_manifest_success: bool,
        successful_single_id_list_number: u64,
        success: bool,
    ) {
        let latency_ms =
            (Utc::now().timestamp_millis() as u64).saturating_sub(sync_start_ms) as f64;
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            ID_LISTS_SYNC_OVERALL_LATENCY_METRIC.to_string(),
            latency_ms,
            Some(HashMap::from([
                ("id_lists_sync_success".into(), success.to_string()),
                (
                    ID_LISTS_SYNC_OVERALL_MANIFEST_SUCCESS_TAG.to_string(),
                    id_list_manifest_success.to_string(),
                ),
                (
                    ID_LISTS_SYNC_OVERALL_SUCCEED_SINGLE_ID_LIST_NUMBER_TAG.to_string(),
                    successful_single_id_list_number.to_string(),
                ),
            ])),
        ));
    }
}

struct IdListDownloadJob {
    name: String,
    url: String,
    metadata: IdListMetadata,
    range_start: u64,
}

fn normalize_id_list_download(
    status: Option<u16>,
    content_range: Option<&str>,
    requested_start: u64,
    manifest_size: u64,
    mut text: String,
) -> Result<Option<(String, std::ops::Range<u64>)>, &'static str> {
    match status {
        Some(200) if content_range.is_none() => {
            let end = text.len() as u64;
            // SFP may have useful bytes without having reached the manifest size yet.
            if end < requested_start || (end == requested_start && end < manifest_size) {
                return Ok(None);
            }
            let start = usize::try_from(requested_start)
                .map_err(|_| "ID-list download offset is too large")?;
            if !text.is_char_boundary(start) {
                return Err("ID-list download offset splits a UTF-8 character");
            }
            // Applying the whole file as a delta would advance the local offset
            // twice over its existing prefix and skip later membership updates.
            if start != 0 {
                text = text.split_off(start);
            }
            Ok(Some((text, requested_start..end)))
        }
        Some(200 | 206) => {
            let range = content_range
                .and_then(|header| downloaded_range(header, text.len()))
                .ok_or("ID-list download returned an invalid Content-Range")?;
            if range.start != requested_start || range.end <= requested_start {
                return Err("ID-list download returned an unexpected or empty byte range");
            }
            Ok(Some((text, range)))
        }
        _ => Err("ID-list download returned an unexpected response status or Content-Range"),
    }
}
#[async_trait]
impl IdListsAdapter for StatsigHttpIdListsAdapter {
    async fn start(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
        listener: Arc<dyn IdListsUpdateListener + Send + Sync>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.set_listener(listener);
                self.ops_stats
                    .set_diagnostics_context(ContextType::Initialize);
                let result = self.sync_id_lists().await;
                result?;
                Ok(())
            })
            .await
    }

    async fn shutdown(&self, _timeout: Duration) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.shutdown_notify.notify_one();
                Ok(())
            })
            .await
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                let weak_self = Arc::downgrade(&self);
                let interval_duration = self.sync_interval_duration;

                statsig_runtime.spawn(
            "http_id_list_bg_sync",
            move |rt_shutdown_notify| async move {
                loop {
                    tokio::select! {
                        () = sleep(interval_duration) => {
                            Self::run_background_sync(&weak_self).await;
                        }
                        () = rt_shutdown_notify.notified() => {
                            log_d!(TAG, "Runtime shutdown. Shutting down id list background sync");
                            break;
                        },
                        () = self.shutdown_notify.notified() => {
                            log_d!(TAG, "Shutting down id list background sync");
                            break;
                        }
                    }
                }
            },
        )?;

                Ok(())
            })
            .await
    }

    fn get_type_name(&self) -> String {
        TAG.to_string()
    }
}

#[cfg(test)]
#[path = "__tests__/statsig_http_id_lists_adapter_tests.rs"]
mod tests;

#[cfg(test)]
#[path = "__tests__/id_list_download_concurrency_tests.rs"]
mod concurrency_tests;

#[cfg(all(test, feature = "custom_network_provider"))]
#[path = "__tests__/id_lists_refresh_tests.rs"]
mod refresh_tests;

#[cfg(all(test, feature = "custom_network_provider"))]
#[path = "__tests__/id_list_propagation_tests.rs"]
mod propagation_tests;

#[cfg(test)]
#[path = "__tests__/id_list_cursor_tests.rs"]
mod cursor_tests;

#[cfg(test)]
#[path = "__tests__/id_list_range_tests.rs"]
mod range_tests;

#[cfg(test)]
#[path = "__tests__/state_read_retry_tests.rs"]
mod state_read_retry_tests;
