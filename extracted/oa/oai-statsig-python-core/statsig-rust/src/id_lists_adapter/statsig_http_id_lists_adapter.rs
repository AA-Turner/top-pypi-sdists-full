use super::IdListMetadata;
use super::id_list_propagation::{IdListManifestEntry, downloaded_range};
use crate::id_lists_adapter::{
    IdListPropagationUpdate, IdListPublicationMode, IdListUpdate, IdListsAdapter,
    IdListsUpdateListener,
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
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::statsig_metadata::StatsigMetadata;
use crate::{StatsigErr, StatsigOptions, StatsigRuntime, log_d, log_e};
use async_trait::async_trait;
use chrono::Utc;
use dashmap::DashMap;
use futures::{StreamExt, stream};
use parking_lot::{ReentrantMutex, RwLock};
use std::collections::HashMap;
use std::future::Future;
use std::ops::Range;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::sync::{Notify, OnceCell, OwnedMutexGuard, RwLock as AsyncRwLock, Semaphore};
use tokio::time::sleep;

const DEFAULT_RETRY_POLICY: RetryPolicy = RetryPolicy {
    attempts: 2,
    jitter: true,
};

const DEFAULT_ID_LIST_SYNC_INTERVAL_MS: u32 = 60_000;
const ID_LIST_DOWNLOAD_CONCURRENCY: usize = 4;
// Canonical records need ten bytes including LF, even with one-byte responses.
const MAX_ID_LIST_RECORD_CONTINUATIONS: usize = 64;
const MAX_UNFINISHED_ID_LIST_RECORD_BYTES: usize = 64 * 1024;

type IdListsResponse = HashMap<String, IdListMetadata>;
type IdListsManifest = HashMap<String, IdListManifestEntry>;

const TAG: &str = stringify!(StatsigHttpIdListsAdapter);
const ID_LISTS_SYNC_OVERALL_LATENCY_METRIC: &str = "id_lists_sync_overall.latency";
const ID_LISTS_SYNC_OVERALL_MANIFEST_SUCCESS_TAG: &str = "id_list_manifest_success";
const ID_LISTS_SYNC_OVERALL_SUCCEED_SINGLE_ID_LIST_NUMBER_TAG: &str =
    "succeed_single_id_list_number";

#[cfg(test)]
tokio::task_local! {
    pub(super) static TEST_CDN_MANIFEST_URL: String;
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub(super) enum RefreshTrigger {
    Initialize,
    Background,
}

pub struct StatsigHttpIdListsAdapter {
    output_policy: crate::output_policy::OutputPolicy,
    partial_refresh: bool,
    manifest_retry_policy: RetryPolicy,
    file_retry_policy: RetryPolicy,
    id_lists_manifest_url: String,
    download_id_list_file_api: Option<String>,
    fallback_url: Option<String>,
    fallback_to_statsig_api: bool,
    listener: RwLock<Option<Arc<dyn IdListsUpdateListener>>>,
    inline_handoff: ReentrantMutex<()>,
    pub(super) refresh_gate: Arc<tokio::sync::Mutex<()>>,
    network: NetworkClient,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    shutdown_notify: Arc<Notify>,
    manifest_failures: RefreshFailureTracker,
    file_failures: RefreshFailureTracker,
    // Compact listeners can leave a worker running when a cold load is cancelled.
    lazy_blocking_publication: Option<Arc<tokio::sync::Mutex<()>>>,
    /// Temporary per-list singleflight entries. Concurrent callers for the same
    /// name await one shared load instead of scheduling duplicate body requests.
    in_flight_loads: DashMap<String, Arc<SharedIdListLoad>>,
    /// Caps body downloads across distinct list names. This bounds network work
    /// but does not replace the same-name singleflight above.
    download_permits: Semaphore,
    /// Polling syncs take the write side while replacing the manifest and
    /// publishing updates; on-demand loads take the read side. Thus a load uses
    /// either the complete previous snapshot or the complete new snapshot.
    latest_manifest: AsyncRwLock<Option<IdListsManifest>>,
}

impl StatsigHttpIdListsAdapter {
    pub(super) fn partial_refresh_enabled(options: &StatsigOptions) -> bool {
        if options.lazy_load_id_lists == Some(true) {
            return false;
        }
        match std::env::var_os("STATSIG_PARTIAL_ID_LIST_REFRESH") {
            Some(value) => value == "true",
            None => options
                .experimental_flags
                .as_ref()
                .is_some_and(|flags| flags.contains("partial_id_list_refresh")),
        }
    }

    #[must_use]
    pub fn new(sdk_key: &str, options: &StatsigOptions) -> Self {
        Self::with_partial_refresh(sdk_key, options, Self::partial_refresh_enabled(options))
    }

    pub(super) fn with_partial_refresh(
        sdk_key: &str,
        options: &StatsigOptions,
        partial_refresh: bool,
    ) -> Self {
        let output_policy = crate::output_policy::OutputPolicy::from_options(Some(options));
        let _output_scope = output_policy.enter();
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
            partial_refresh,
            manifest_retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            file_retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            id_lists_manifest_url,
            download_id_list_file_api: options.download_id_list_file_api.clone(),
            fallback_url,
            fallback_to_statsig_api: options.fallback_to_statsig_api == Some(true),
            listener: RwLock::new(None),
            inline_handoff: ReentrantMutex::default(),
            refresh_gate: Default::default(),
            network,
            sync_interval_duration,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            shutdown_notify: Arc::new(Notify::new()),
            manifest_failures: RefreshFailureTracker::default(),
            file_failures: RefreshFailureTracker::default(),
            lazy_blocking_publication: (options.lazy_load_id_lists == Some(true))
                .then(Default::default),
            in_flight_loads: DashMap::new(),
            download_permits: Semaphore::new(ID_LIST_DOWNLOAD_CONCURRENCY),
            latest_manifest: AsyncRwLock::new(None),
        }
    }

    pub fn force_shutdown(&self) {
        self.signal_shutdown();
        // The listener itself may request shutdown while holding this fence.
        drop(self.inline_handoff.lock());
    }

    pub(super) fn signal_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.network.shutdown();
        self.shutdown_notify.notify_waiters();
    }

    #[cfg(test)]
    pub(crate) fn set_network_provider_for_test(
        &mut self,
        provider: std::sync::Weak<dyn crate::networking::NetworkProvider>,
    ) {
        self.network.set_network_provider_for_test(provider);
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
                    Self::parse_response(response.data)
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
    ) -> Result<(String, Range<u64>), StatsigErr> {
        if is_fallback && !self.file_can_fallback(job) {
            return Err(StatsigErr::NetworkError(NetworkError::RequestNotRetryable(
                job.url.clone(),
                None,
                "No trusted fallback destination".into(),
            )));
        }
        let _permit =
            self.download_permits.acquire().await.map_err(|_| {
                StatsigErr::NetworkError(NetworkError::ShutdownError(job.url.clone()))
            })?;
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
    ) -> Result<(String, Range<u64>), StatsigErr> {
        if is_fallback {
            self.network.log_fallback("id_list_file", true);
        }
        // Only carry a fragment when this attempt has yet to receive a whole record.
        // A retry, fallback, or new manifest starts from the listener's committed cursor.
        let mut pending = PartialIdListRecord::default();
        for _ in 0..=MAX_ID_LIST_RECORD_CONTINUATIONS {
            match self
                .download_id_list_chunk(job, is_fallback, index, pending)
                .await?
            {
                IdListDownload::Complete(text, range) => return Ok((text, range)),
                IdListDownload::Incomplete(record) => pending = record,
            }
        }
        Err(StatsigErr::CustomError(
            "Too many partial responses for one ID-list record".into(),
        ))
    }

    async fn download_id_list_chunk(
        &self,
        job: &IdListDownloadJob,
        is_fallback: bool,
        index: u32,
        pending: PartialIdListRecord,
    ) -> Result<IdListDownload, StatsigErr> {
        let download_url = if is_fallback {
            &job.metadata.url
        } else {
            &job.url
        };
        let mut request = Self::id_list_file_request_args(download_url, job, &pending);
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
        let result = normalize_id_list_download(
            response,
            download_url,
            job.range_start,
            job.metadata.size,
            pending,
        );
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
        job: &IdListDownloadJob,
        pending: &PartialIdListRecord,
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

        let start = job.range_start + pending.bytes.len() as u64;
        let mut headers = HashMap::from([
            ("Range".into(), format!("bytes={start}-")),
            (
                "statsig-id-list-file-size".into(),
                job.metadata.size.to_string(),
            ),
            // Byte offsets refer to the unencoded append log.
            ("Accept-Encoding".into(), "identity".into()),
        ]);
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

    fn is_cdn_url(&self) -> bool {
        is_default_cdn_id_lists_manifest_url(&self.id_lists_manifest_url)
    }

    fn parse_response(response: Option<ResponseData>) -> Result<IdListsManifest, StatsigErr> {
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
        let _old = self.listener.write().replace(listener);
    }

    fn is_current_listener(&self, listener: &Arc<dyn IdListsUpdateListener>) -> bool {
        self.listener
            .read()
            .as_ref()
            .is_some_and(|current| Arc::ptr_eq(current, listener))
    }

    fn current_listener(&self) -> Result<Arc<dyn IdListsUpdateListener>, StatsigErr> {
        self.listener
            .read()
            .clone()
            .ok_or_else(|| StatsigErr::UnstartedAdapter("Listener not set".to_string()))
    }

    fn publication_stopped() -> StatsigErr {
        StatsigErr::ShutdownFailure("ID-list publication stopped".into())
    }

    async fn while_running<T>(&self, work: impl Future<Output = T>) -> Result<T, StatsigErr> {
        let stopped = self.shutdown_notify.notified();
        if self.network.shutdown_flag().load(Ordering::SeqCst) {
            return Err(Self::publication_stopped());
        }
        tokio::select! {
            biased;
            () = stopped => Err(Self::publication_stopped()),
            result = work => Ok(result),
        }
    }

    pub(super) async fn refresh(&self, trigger: RefreshTrigger) -> Result<(), StatsigErr> {
        self.refresh_with_listener(trigger, None).await
    }

    async fn refresh_with_listener(
        &self,
        trigger: RefreshTrigger,
        listener: Option<Arc<dyn IdListsUpdateListener>>,
    ) -> Result<(), StatsigErr> {
        // Keep the scope through diagnostics enqueue. A detached worker holds a share through publication.
        let refresh_guard = Arc::new(
            self.while_running(self.refresh_gate.clone().lock_owned())
                .await?,
        );
        if let Some(listener) = listener.filter(|listener| !self.is_current_listener(listener)) {
            if let Some(publication) = &self.lazy_blocking_publication {
                // A cold load may still be publishing into the old listener.
                let _worker = self.while_running(publication.lock()).await?;
                let mut manifest = self.while_running(self.latest_manifest.write()).await?;
                *manifest = None;
                self.set_listener(listener);
            } else {
                self.set_listener(listener);
            }
        }
        let background = trigger == RefreshTrigger::Background;
        self.ops_stats.set_diagnostics_context(if background {
            ContextType::ConfigSync
        } else {
            ContextType::Initialize
        });
        let result = self
            .sync_id_lists_with_trigger(background, &refresh_guard)
            .await;
        if background
            && !matches!(
                result,
                Err(StatsigErr::NetworkError(NetworkError::DisableNetworkOn(_)))
            )
        {
            self.ops_stats.enqueue_diagnostics_event(
                Some(KeyType::GetIDListSources),
                Some(ContextType::ConfigSync),
            );
        }
        result
    }

    #[cfg(test)]
    async fn sync_id_lists(&self) -> Result<(), StatsigErr> {
        self.refresh(RefreshTrigger::Initialize).await
    }

    async fn sync_id_lists_with_trigger(
        &self,
        background: bool,
        refresh_guard: &Arc<OwnedMutexGuard<()>>,
    ) -> Result<(), StatsigErr> {
        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        let mut summary = scopeguard::guard(RefreshSummary::default(), |summary| {
            if summary.manifest_success {
                self.add_diagnostics_end_marker(
                    KeyType::GetIDListSources,
                    StepType::Process,
                    summary.success,
                    None,
                    None,
                );
            }
            self.log_id_lists_sync_overall_latency(
                sync_start_ms,
                summary.manifest_success,
                summary.successful_downloads,
                summary.success,
            );
        });
        let new_manifest = self
            .fetch_id_list_manifests_from_network(background)
            .await?;
        self.add_diagnostics_start_marker(
            KeyType::GetIDListSources,
            StepType::Process,
            Some(new_manifest.len()),
            None,
        );
        summary.manifest_success = true;
        let result = self
            .process_id_lists(
                new_manifest,
                &mut summary.successful_downloads,
                background,
                refresh_guard,
            )
            .await;
        summary.success = result.is_ok();
        result
    }

    async fn process_id_lists(
        &self,
        new_manifest: IdListsManifest,
        successful_downloads: &mut u64,
        background: bool,
        refresh_guard: &Arc<OwnedMutexGuard<()>>,
    ) -> Result<(), StatsigErr> {
        if self.lazy_blocking_publication.is_none() {
            let prepared = self
                .prepare_id_lists(new_manifest, successful_downloads, background)
                .await?;
            return self
                .publish_id_list_updates(
                    prepared,
                    IdListPublicationMode::Replace,
                    Some(refresh_guard),
                )
                .await;
        }
        let curr_manifest = self.current_listener()?.get_current_id_list_metadata();
        let active_manifest = new_manifest
            .iter()
            .filter(|(name, _entry)| curr_manifest.contains_key(name.as_str()))
            .map(|(name, entry)| (name.clone(), entry.clone()))
            .collect();
        let mut prepared = self
            .prepare_id_lists(active_manifest, successful_downloads, background)
            .await?;

        // Commit the fetched generation and its prepared updates atomically with
        // respect to on-demand publication. Downloads remain outside this guard.
        let mut manifest = self.while_running(self.latest_manifest.write()).await?;
        // A list may have materialized while this poll was downloading other
        // bodies. Preserve it only when it still matches the new manifest.
        // A changed generation is omitted from the replacement so the next
        // dependent evaluation observes it as missing and loads it.
        for (name, current) in self.current_listener()?.get_current_id_list_metadata() {
            if new_manifest
                .get(&name)
                .is_some_and(|entry| same_id_list_generation(&current, &entry.metadata))
                && !prepared.updates.contains_key(&name)
            {
                prepared.updates.insert(
                    name,
                    IdListUpdate {
                        raw_changeset: None,
                        new_metadata: current,
                    },
                );
            }
        }

        *manifest = Some(new_manifest);
        self.publish_id_list_updates(
            prepared,
            IdListPublicationMode::Replace,
            Some(refresh_guard),
        )
        .await
    }

    async fn prepare_id_lists(
        &self,
        new_manifest: IdListsManifest,
        successful_downloads: &mut u64,
        background: bool,
    ) -> Result<PreparedIdListUpdates, StatsigErr> {
        let listener = self.current_listener()?;
        let blocking = listener.requires_blocking_id_list_publication();
        let publication = match &self.lazy_blocking_publication {
            Some(gate) if blocking => Some(self.while_running(gate.clone().lock_owned()).await?),
            _ => None,
        };
        let mut curr_manifest: IdListsResponse = listener.get_current_id_list_metadata();
        let mut jobs = Vec::new();
        let mut updates = HashMap::new();
        let mut propagation = HashMap::with_capacity(new_manifest.len());
        let mut name_mismatches = 0usize;
        for (name, mut entry) in new_manifest {
            if self.partial_refresh && entry.metadata.name != name {
                // Evaluation and removals use the manifest key; persist that same name.
                entry.metadata.name.clone_from(&name);
                name_mismatches += 1;
            }
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
        if name_mismatches > 0 {
            self.ops_stats.log(ObservabilityEvent::new_event(
                MetricType::Increment,
                "id_list_manifest_name_mismatch".into(),
                name_mismatches as f64,
                None,
            ));
        }
        // Stable launch order also makes failures reproducible across manifest map orderings.
        jobs.sort_by(|a, b| a.name.cmp(&b.name));
        let mut file_failure = None;
        if !jobs.is_empty() {
            let pending = parking_lot::Mutex::new(jobs);
            let completed = parking_lot::Mutex::new(Vec::new());
            // This also counts finished file jobs if pending peers are cancelled.
            let count = scopeguard::guard(&completed, |files| {
                *successful_downloads += files.lock().len() as u64;
            });
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
            drop(count);
            let completed = completed.into_inner();
            if let Err(error) = result {
                if !self.partial_refresh
                    || matches!(
                        error,
                        StatsigErr::NetworkError(NetworkError::ShutdownError(_))
                    )
                {
                    return Err(error);
                }
                // A missing name is a removal only if the full manifest omits it.
                // Keep the installed generation and cursor for failed warm downloads.
                for job in pending.into_inner() {
                    propagation.remove(&job.name);
                    if let Some(installed) = curr_manifest.remove(&job.name) {
                        updates.insert(
                            job.name,
                            IdListUpdate {
                                raw_changeset: None,
                                new_metadata: installed,
                            },
                        );
                    }
                }
                file_failure = Some(error);
            }
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
        Ok(PreparedIdListUpdates {
            file_failure,
            updates,
            propagation,
            listener,
            blocking,
            publication,
        })
    }

    async fn publish_id_list_updates(
        &self,
        prepared: PreparedIdListUpdates,
        publication_mode: IdListPublicationMode,
        refresh_guard: Option<&Arc<OwnedMutexGuard<()>>>,
    ) -> Result<(), StatsigErr> {
        let PreparedIdListUpdates {
            updates,
            propagation,
            listener,
            blocking,
            publication,
            file_failure,
        } = prepared;
        let publication_mode = if file_failure.is_some() {
            IdListPublicationMode::IncompleteRefresh
        } else {
            publication_mode
        };
        if blocking {
            let guard = (refresh_guard.cloned(), publication);
            let stopped = self.network.shutdown_flag().clone();
            let policy = self.output_policy;
            tokio::task::spawn_blocking(move || {
                let _guard = guard;
                let _scope = policy.enter();
                // Owning the elected listener keeps its lease alive through fsync
                // and installation even if the refresh future is cancelled.
                let result = if stopped.load(Ordering::SeqCst) {
                    Err(Self::publication_stopped())
                } else {
                    publish_prepared_id_lists(
                        listener.as_ref(),
                        updates,
                        propagation,
                        publication_mode,
                    )
                };
                drop(listener);
                result
            })
            .await
            .map_err(|error| StatsigErr::FileError(error.to_string()))??;
        } else {
            let _handoff = self.inline_handoff.lock();
            if self.network.shutdown_flag().load(Ordering::SeqCst) {
                return Err(Self::publication_stopped());
            }
            publish_prepared_id_lists(listener.as_ref(), updates, propagation, publication_mode)?;
        }
        file_failure.map_or(Ok(()), Err)
    }

    /// Performs one named-list load after the caller has acquired the
    /// singleflight entry. "Uncached" refers only to that temporary in-flight
    /// result: this still uses the cached manifest and skips a list which is
    /// already at the manifest's target generation.
    async fn process_id_list_uncached(&self, name: &str) -> Result<(), StatsigErr> {
        loop {
            // Polling and initialization populate this metadata-only snapshot.
            // Hold the barrier only long enough to clone one generation.
            let entry = {
                let manifest = self.latest_manifest.read().await;
                let manifest = manifest.as_ref().ok_or_else(|| {
                    StatsigErr::UnstartedAdapter(
                        "ID-list manifest has not been fetched yet".to_string(),
                    )
                })?;
                manifest.get(name).cloned().ok_or_else(|| {
                    StatsigErr::CustomError(format!("ID list {name} is missing from the manifest"))
                })?
            };
            if self.id_list_is_at_target(name, &entry.metadata)? {
                return Ok(());
            }

            // Reuse the normal download and retry pipeline without holding the
            // publication barrier across network I/O.
            let mut successful_downloads = 0;
            let prepared = self
                .prepare_id_lists(
                    HashMap::from([(name.to_owned(), entry.clone())]),
                    &mut successful_downloads,
                    false,
                )
                .await?;

            // Publish only if the cached manifest still names the generation we
            // downloaded. Otherwise retry against the newer metadata.
            let manifest = self.latest_manifest.read().await;
            let latest = manifest
                .as_ref()
                .and_then(|manifest| manifest.get(name))
                .ok_or_else(|| {
                    StatsigErr::CustomError(format!("ID list {name} is missing from the manifest"))
                })?;
            if !self.is_current_listener(&prepared.listener)
                || !same_id_list_generation(&entry.metadata, &latest.metadata)
            {
                continue;
            }
            if self.id_list_is_at_target(name, &entry.metadata)? {
                return Ok(());
            }
            return self
                .publish_id_list_updates(prepared, IdListPublicationMode::Merge, None)
                .await;
        }
    }

    fn id_list_is_at_target(
        &self,
        name: &str,
        target: &IdListMetadata,
    ) -> Result<bool, StatsigErr> {
        let current = self.current_listener()?.get_current_id_list_metadata();
        Ok(current.get(name).is_some_and(|current| {
            current.creation_time > target.creation_time
                || (current.creation_time == target.creation_time
                    && current.file_id == target.file_id
                    && current.size >= target.size)
        }))
    }

    /// Materializes one cached manifest entry through the existing
    /// `process_id_lists` pipeline. This stays specific to the built-in HTTP
    /// adapter so custom adapter implementations do not gain a new contract.
    pub(crate) async fn process_id_list(&self, name: &str) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                let shared = {
                    let active = self
                        .in_flight_loads
                        .entry(name.to_owned())
                        .or_insert_with(|| Arc::new(SharedIdListLoad::default()));
                    let shared = Arc::clone(active.value());
                    shared.waiters.fetch_add(1, Ordering::AcqRel);
                    shared
                };
                let _waiter = IdListLoadWaiter {
                    loads: &self.in_flight_loads,
                    name: name.to_owned(),
                    shared: Arc::clone(&shared),
                };

                self.while_running(
                    shared
                        .result
                        .get_or_init(|| self.process_id_list_uncached(name)),
                )
                .await?
                .clone()
            })
            .await
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

#[derive(Default)]
struct RefreshSummary {
    manifest_success: bool,
    successful_downloads: u64,
    success: bool,
}

struct IdListDownloadJob {
    name: String,
    url: String,
    metadata: IdListMetadata,
    range_start: u64,
}

#[derive(Debug, PartialEq)]
enum IdListDownload {
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
    mut pending: PartialIdListRecord,
) -> Result<IdListDownload, StatsigErr> {
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
    let mut bytes = body.read_to_bytes()?;
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
        return Ok(IdListDownload::Complete(text, committed_start..end));
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

    // A record without LF is complete only at the representation's EOF. Return
    // complete lines now and ask for any trailing fragment again next refresh.
    let complete_len = if range.end == total {
        Some(bytes.len())
    } else {
        memchr::memrchr(b'\n', &bytes).map(|i| i + 1)
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
        return Ok(IdListDownload::Incomplete(PartialIdListRecord {
            bytes,
            total,
            etag: pending.etag.or_else(|| etag().cloned()),
        }));
    }
    let end = committed_start + bytes.len() as u64;
    let text = decode(bytes)?;
    Ok(IdListDownload::Complete(text, committed_start..end))
}

struct PreparedIdListUpdates {
    file_failure: Option<StatsigErr>,
    updates: HashMap<String, IdListUpdate>,
    propagation: HashMap<String, IdListPropagationUpdate>,
    /// The listener and optional blocking-publication lease are captured before
    /// reading byte cursors, so a cancelled or concurrent refresh cannot publish
    /// downloaded deltas against a different committed snapshot.
    listener: Arc<dyn IdListsUpdateListener>,
    blocking: bool,
    publication: Option<OwnedMutexGuard<()>>,
}

fn publish_prepared_id_lists(
    listener: &dyn IdListsUpdateListener,
    updates: HashMap<String, IdListUpdate>,
    propagation: HashMap<String, IdListPropagationUpdate>,
    publication_mode: IdListPublicationMode,
) -> Result<(), StatsigErr> {
    match publication_mode {
        IdListPublicationMode::Replace => {
            listener.try_receive_id_list_updates_with_propagation(updates, propagation)
        }
        IdListPublicationMode::IncompleteRefresh => {
            listener.try_receive_incomplete_id_list_refresh(updates, propagation)
        }
        IdListPublicationMode::Merge => {
            listener.did_receive_partial_id_list_updates_with_propagation(updates, propagation);
            Ok(())
        }
    }
}

fn same_id_list_generation(left: &IdListMetadata, right: &IdListMetadata) -> bool {
    left.file_id == right.file_id
        && left.creation_time == right.creation_time
        && left.size == right.size
        && left.url == right.url
}

#[derive(Default)]
struct SharedIdListLoad {
    /// The one load result shared by every concurrent caller for a list name.
    /// `OnceCell` is async and cancellation-safe: if the initializing future is
    /// cancelled, another waiter may perform the load.
    result: OnceCell<Result<(), StatsigErr>>,
    /// Number of callers currently using this singleflight entry.
    waiters: AtomicUsize,
}

/// Removes a completed or cancelled singleflight entry after its last caller
/// leaves, allowing a future call to re-check the latest cached manifest.
struct IdListLoadWaiter<'a> {
    loads: &'a DashMap<String, Arc<SharedIdListLoad>>,
    name: String,
    shared: Arc<SharedIdListLoad>,
}

impl Drop for IdListLoadWaiter<'_> {
    fn drop(&mut self) {
        if self.shared.waiters.fetch_sub(1, Ordering::AcqRel) == 1 {
            self.loads.remove_if(&self.name, |_, active| {
                Arc::ptr_eq(active, &self.shared) && active.waiters.load(Ordering::Acquire) == 0
            });
        }
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
            .scope(self.refresh_with_listener(RefreshTrigger::Initialize, Some(listener)))
            .await
    }

    async fn shutdown(&self, timeout: Duration) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.signal_shutdown();
                tokio::time::timeout(timeout, async {
                    let _refresh = self.refresh_gate.lock().await;
                    if let Some(publication) = &self.lazy_blocking_publication {
                        drop(publication.lock().await);
                        // Drain any ordinary cold-list callback as well.
                        drop(self.latest_manifest.write().await);
                    }
                })
                .await
                .map_err(|_| StatsigErr::ShutdownFailure("ID-list publication timed out".into()))?;
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

                let shutdown = self.shutdown_notify.clone();
                let stopped = self.network.shutdown_flag().clone();
                statsig_runtime.spawn(
                    "http_id_list_bg_sync",
                    move |runtime_shutdown| async move {
                        loop {
                            let notified = shutdown.notified();
                            if weak_self.strong_count() == 0 || stopped.load(Ordering::SeqCst) {
                                break;
                            }
                            tokio::select! {
                                biased;
                                () = notified => {
                                    log_d!(TAG, "Shutting down id list background sync");
                                    break;
                                }
                                () = runtime_shutdown.notified() => {
                                    log_d!(TAG, "Runtime shutdown. Shutting down id list background sync");
                                    break;
                                }
                                () = sleep(interval_duration) => {}
                            }
                            let Some(adapter) = weak_self.upgrade() else {
                                break;
                            };
                            if let Err(error) = adapter.refresh(RefreshTrigger::Background).await {
                                if !matches!(
                                    error,
                                    StatsigErr::NetworkError(NetworkError::DisableNetworkOn(_))
                                ) {
                                    log_e!(TAG, "IDList background sync failed {}", error);
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

#[cfg(all(test, feature = "custom_network_provider"))]
#[path = "lazy_id_list_tests.rs"]
mod lazy_id_list_tests;

#[cfg(test)]
#[path = "__tests__/id_list_cursor_tests.rs"]
mod cursor_tests;

#[cfg(test)]
#[path = "__tests__/id_list_range_tests.rs"]
mod range_tests;

#[cfg(test)]
#[path = "__tests__/state_read_retry_tests.rs"]
mod state_read_retry_tests;
