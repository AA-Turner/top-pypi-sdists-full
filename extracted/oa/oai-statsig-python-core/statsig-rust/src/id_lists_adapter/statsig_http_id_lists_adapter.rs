use super::IdListMetadata;
use super::id_list_propagation::{IdListManifestEntry, downloaded_range};
use crate::id_lists_adapter::{IdListUpdate, IdListsAdapter, IdListsUpdateListener};
use crate::networking::{
    DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, NetworkClient, NetworkError, RequestArgs, Response,
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
    id_lists_manifest_url: String,
    download_id_list_file_api: Option<String>,
    fallback_url: Option<String>,
    fallback_to_statsig_api: bool,
    listener: RwLock<Option<Arc<dyn IdListsUpdateListener>>>,
    network: NetworkClient,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    shutdown_notify: Arc<Notify>,
    download_retry_count: u32,
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

        Self {
            output_policy,
            id_lists_manifest_url,
            download_id_list_file_api: options.download_id_list_file_api.clone(),
            fallback_url,
            fallback_to_statsig_api: options.fallback_to_statsig_api == Some(true),
            listener: RwLock::new(None),
            network,
            sync_interval_duration,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            shutdown_notify: Arc::new(Notify::new()),
            download_retry_count: 2,
        }
    }

    pub fn force_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.shutdown_notify.notify_one();
    }

    async fn fetch_id_list_manifests_from_network(&self) -> Result<IdListsManifest, StatsigErr> {
        let request_args = RequestArgs {
            url: self.id_lists_manifest_url.clone(),
            accept_gzip_response: true,
            diagnostics_key: Some(KeyType::GetIDListSources),
            ..RequestArgs::new()
        };

        let result = if self.is_cdn_url() {
            self.network.get(request_args.clone()).await
        } else {
            self.network.post(request_args.clone(), None).await
        };

        let result = match result {
            Ok(response) => self.parse_response(response.data),
            Err(initial_err) => {
                self.handle_manifest_network_error(request_args, initial_err)
                    .await
            }
        };

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

    async fn download_id_list(
        &self,
        job: &IdListDownloadJob,
    ) -> Result<(String, std::ops::Range<u64>), StatsigErr> {
        let fallback_url = (self.fallback_to_statsig_api
            && job.url != job.metadata.url
            && is_default_cdn_url(&job.metadata.url))
        .then_some(job.metadata.url.as_str());
        let mut download_url = job.url.as_str();
        for attempt in 1..=self.download_retry_count + 1 {
            let request = Self::id_list_file_request_args(
                download_url,
                job.range_start,
                job.metadata.size,
                job.metadata.file_id.clone(),
            );
            let response = if download_url == job.url {
                self.network.get(request).await
            } else {
                // Only the captured default CDN is trusted with SDK credentials.
                // Never forward those credentials through a fallback redirect.
                self.network.get_without_redirects(request).await
            };
            self.add_diagnostics_start_marker(
                KeyType::GetIDList,
                StepType::Process,
                None,
                Some(download_url.to_owned()),
            );
            let result = response
                .map_err(StatsigErr::NetworkError)
                .and_then(|response| {
                    let request_failed = |message| {
                        StatsigErr::NetworkError(NetworkError::RequestFailed(
                            download_url.to_owned(),
                            response.status_code,
                            message,
                        ))
                    };
                    if let Some(error) = response.error {
                        return Err(request_failed(error));
                    }
                    let mut body = response
                        .data
                        .ok_or_else(|| request_failed("Missing ID list body".into()))?;
                    // I/O failures are retryable; malformed UTF-8 is terminal.
                    let text = body.read_to_string()?;
                    normalize_id_list_download(
                        response.status_code,
                        body.get_header_ref("content-range").map(String::as_str),
                        job.range_start,
                        job.metadata.size,
                        text,
                    )
                    .map_err(|message| request_failed(message.into()))
                });
            self.add_diagnostics_end_marker(
                KeyType::GetIDList,
                StepType::Process,
                result.is_ok(),
                None,
                Some(download_url.to_owned()),
            );
            match result {
                Ok(body) => return Ok(body),
                Err(mut error) if !is_retryable_download_error(&error) => {
                    if let StatsigErr::NetworkError(NetworkError::RetriesExhausted(
                        _,
                        _,
                        count,
                        _,
                    )) = &mut error
                    {
                        *count = attempt;
                    }
                    return Err(error);
                }
                Err(error) if attempt > self.download_retry_count => {
                    let status = match &error {
                        StatsigErr::NetworkError(error) => error.status_code(),
                        _ => None,
                    };
                    return Err(StatsigErr::NetworkError(NetworkError::RetriesExhausted(
                        download_url.to_owned(),
                        status,
                        attempt,
                        error.to_string(),
                    )));
                }
                Err(error) => {
                    // Fallback consumes the same per-file retry budget. Explicit zero
                    // retries means one SDK attempt, including when fallback is enabled.
                    if let StatsigErr::NetworkError(NetworkError::RetriesExhausted(..)) = error {
                        download_url = fallback_url.unwrap_or(download_url);
                    }
                    sleep(Duration::from_millis(100 * 2_u64.pow(attempt))).await;
                }
            }
        }
        unreachable!("the initial download attempt always runs")
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

    async fn handle_fallback_request(
        &self,
        fallback_url: &str,
        mut request_args: RequestArgs,
    ) -> Result<Response, StatsigErr> {
        request_args.url = fallback_url.to_owned();

        // TODO add log

        // fallback to cdn, it's a get request
        match self.network.get(request_args.clone()).await {
            Ok(response) => Ok(response),
            Err(e) => Err(StatsigErr::NetworkError(e)),
        }
    }

    async fn handle_manifest_network_error(
        &self,
        request_args: RequestArgs,
        initial_err: NetworkError,
    ) -> Result<IdListsManifest, StatsigErr> {
        if !matches!(initial_err, NetworkError::RetriesExhausted(_, _, _, _)) {
            return Err(StatsigErr::NetworkError(initial_err));
        }

        if let Some(fallback_url) = &self.fallback_url {
            return match self
                .handle_fallback_request(fallback_url, request_args)
                .await
            {
                Ok(response) => self.parse_response(response.data),
                Err(e) => Err(e),
            };
        }

        Err(StatsigErr::NetworkError(initial_err))
    }

    async fn run_background_sync(weak_self: &Weak<Self>) {
        let strong_self = match weak_self.upgrade() {
            Some(s) => s,
            None => return,
        };

        strong_self
            .ops_stats
            .set_diagnostics_context(ContextType::ConfigSync);

        if let Err(e) = strong_self.sync_id_lists().await {
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
            .map_err(|parse_err| {
                let msg = format!("Failed to parse JSON: {parse_err}");
                StatsigErr::JsonParseError(stringify!(IdListsResponse).to_string(), msg)
            })
    }

    fn set_listener(&self, listener: Arc<dyn IdListsUpdateListener>) {
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
        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        let mut manifest_success = false;
        let mut successful_downloads = 0;
        let result = self
            .fetch_and_process_id_lists(&mut manifest_success, &mut successful_downloads)
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
    ) -> Result<(), StatsigErr> {
        let new_manifest = self.fetch_id_list_manifests_from_network().await?;
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
            .process_id_lists(new_manifest, curr_manifest, successful_downloads)
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
        let mut downloads = stream::iter(jobs.into_iter().map(|job| async move {
            let result = self.download_id_list(&job).await;
            (job, result)
        }))
        .buffer_unordered(ID_LIST_DOWNLOAD_CONCURRENCY);
        let mut failures = Vec::new();
        while let Some((job, result)) = downloads.next().await {
            match result {
                Ok((raw_changeset, applied_range)) => {
                    *successful_downloads += 1;
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
                Err(error) => {
                    // Drain every job so independent downloads can finish their retry budgets.
                    failures.push((job.name, error));
                }
            }
        }
        if !failures.is_empty() {
            let summary = failures
                .iter()
                .map(|(name, error)| format!("{name}: {error}"))
                .collect::<Vec<_>>()
                .join("; ");
            log_e!(TAG, "ID list refresh failed: {}", summary);
            return Err(failures.swap_remove(0).1);
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
) -> Result<(String, std::ops::Range<u64>), &'static str> {
    match status {
        Some(200) if content_range.is_none() => {
            let end = text.len() as u64;
            // SFP may have useful bytes without having reached the manifest size yet.
            if end < requested_start || (end == requested_start && end < manifest_size) {
                return Err("ID-list download returned no unread bytes");
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
            Ok((text, requested_start..end))
        }
        Some(200 | 206) => {
            let range = content_range
                .and_then(|header| downloaded_range(header, text.len()))
                .ok_or("ID-list download returned an invalid Content-Range")?;
            if range.start != requested_start || range.end <= requested_start {
                return Err("ID-list download returned an unexpected or empty byte range");
            }
            Ok((text, range))
        }
        _ => Err("ID-list download returned an unexpected response status or Content-Range"),
    }
}

fn is_retryable_download_error(error: &StatsigErr) -> bool {
    match error {
        StatsigErr::SerializationError(_) => true,
        StatsigErr::NetworkError(
            NetworkError::RequestFailed(_, status, _)
            | NetworkError::RetriesExhausted(_, status, _, _),
        ) => !matches!(status, Some(400 | 401 | 403 | 405 | 413 | 429 | 501)),
        _ => false,
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
#[path = "statsig_http_id_lists_adapter_tests.rs"]
mod tests;

#[cfg(test)]
#[path = "id_list_download_concurrency_tests.rs"]
mod concurrency_tests;

#[cfg(all(test, feature = "custom_network_provider"))]
#[path = "id_lists_refresh_tests.rs"]
mod refresh_tests;

#[cfg(all(test, feature = "custom_network_provider"))]
#[path = "id_list_propagation_tests.rs"]
mod propagation_tests;

#[cfg(test)]
#[path = "id_list_cursor_tests.rs"]
mod cursor_tests;

#[cfg(test)]
#[path = "id_list_range_tests.rs"]
mod range_tests;
