#[path = "snapshot_http.rs"]
pub(crate) mod snapshot_http;
use super::id_list_propagation::{IdListManifestEntry, downloaded_range};
use super::{IdList, IdListMetadata, IdListUpdateBase};
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
use crate::portable_id_list_ef;
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::statsig_metadata::StatsigMetadata;
use crate::{SpecStore, StatsigErr, StatsigOptions, StatsigRuntime, log_d, log_e};
use async_trait::async_trait;
use chrono::Utc;
use dashmap::DashMap;
use futures::{StreamExt, stream};
use parking_lot::{Mutex, ReentrantMutex, RwLock};
use std::collections::HashMap;
use std::future::Future;
use std::ops::{ControlFlow, Range};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::time::Duration;
use tokio::sync::{
    Notify, OnceCell, OwnedMutexGuard, OwnedRwLockWriteGuard, RwLock as AsyncRwLock, Semaphore,
};
use tokio::time::sleep;

const DEFAULT_RETRY_POLICY: RetryPolicy = RetryPolicy {
    attempts: 2,
    jitter: true,
};

const DEFAULT_ID_LIST_SYNC_INTERVAL_MS: u32 = 60_000;
const ID_LIST_DOWNLOAD_CONCURRENCY: usize = 4;
const PRIVATE_INDEX_BUILD_CONCURRENCY: usize = 2;
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
    PrivateInitialize,
    SharedInitialize,
    Background,
}

#[derive(Default)]
struct AdapterShutdown {
    notify: Notify,
    // Force shutdown waits for entered synchronous listeners, including private hash commits.
    handoff: ReentrantMutex<()>,
}

#[derive(Clone)]
enum HttpIdListsListener {
    Store(Arc<SpecStore>),
    External(Arc<dyn IdListsUpdateListener>),
}

impl HttpIdListsListener {
    fn into_listener(self) -> Arc<dyn IdListsUpdateListener> {
        match self {
            Self::Store(store) => store,
            Self::External(listener) => listener,
        }
    }
}

pub struct StatsigHttpIdListsAdapter {
    output_policy: crate::output_policy::OutputPolicy,
    partial_refresh: bool,
    manifest_retry_policy: RetryPolicy,
    file_retry_policy: RetryPolicy,
    id_lists_manifest_url: String,
    download_id_list_file_api: Option<Result<url::Url, url::ParseError>>,
    snapshot_enabled: bool,
    fallback_url: Option<String>,
    fallback_to_statsig_api: bool,
    listener: RwLock<Option<HttpIdListsListener>>,
    pub(super) refresh_gate: Arc<tokio::sync::Mutex<()>>,
    network: NetworkClient,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    shutdown: Arc<AdapterShutdown>,
    manifest_failures: RefreshFailureTracker,
    file_failures: RefreshFailureTracker,
    /// Temporary per-list singleflight entries. Concurrent callers for the same
    /// name await one shared load instead of scheduling duplicate body requests.
    in_flight_loads: DashMap<String, Arc<SharedIdListLoad>>,
    /// Caps body downloads across distinct list names. This bounds network work
    /// but does not replace the same-name singleflight above.
    download_permits: Arc<Semaphore>,
    lazy_id_lists: Option<LazyIdLists>,
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

    pub(crate) fn new_with_store(
        sdk_key: &str,
        options: &StatsigOptions,
        store: Arc<SpecStore>,
    ) -> Self {
        let mut adapter = Self::new(sdk_key, options);
        if let Some(lazy) = &mut adapter.lazy_id_lists {
            let env = std::env::var_os("STATSIG_PARALLEL_LAZY_ID_LIST_BUILDS");
            if parallel_lazy_builds_enabled(options, env.as_deref()) {
                lazy.build_permits =
                    Some(Arc::new(Semaphore::new(PRIVATE_INDEX_BUILD_CONCURRENCY)));
            }
        }
        *adapter.listener.get_mut() = Some(HttpIdListsListener::Store(store));
        adapter
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

        let download_id_list_file_api = options
            .download_id_list_file_api
            .as_deref()
            .map(url::Url::parse);
        let snapshot_enabled = options.enable_id_list_elias_fano == Some(true)
            && matches!(&download_id_list_file_api, Some(Ok(endpoint)) if snapshot_http::supports_snapshots(endpoint));

        Self {
            output_policy,
            partial_refresh,
            manifest_retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            file_retry_policy: retry_override.unwrap_or(DEFAULT_RETRY_POLICY),
            id_lists_manifest_url,
            download_id_list_file_api,
            snapshot_enabled,
            fallback_url,
            fallback_to_statsig_api: options.fallback_to_statsig_api == Some(true),
            listener: RwLock::new(None),
            refresh_gate: Default::default(),
            network,
            sync_interval_duration,
            ops_stats: OPS_STATS.get_for_instance_with_options(sdk_instance_id, Some(options)),
            shutdown: Arc::default(),
            manifest_failures: RefreshFailureTracker::default(),
            file_failures: RefreshFailureTracker::default(),
            lazy_id_lists: (options.lazy_load_id_lists == Some(true)).then(|| LazyIdLists {
                manifest: Default::default(),
                build_permits: None,
                #[cfg(test)]
                before_build: None,
            }),
            in_flight_loads: DashMap::new(),
            download_permits: Arc::new(Semaphore::new(ID_LIST_DOWNLOAD_CONCURRENCY)),
        }
    }

    pub fn force_shutdown(&self) {
        self.signal_shutdown();
        // The listener itself may request shutdown while holding this fence.
        drop(self.shutdown.handoff.lock());
    }

    pub(super) fn signal_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.network.shutdown();
        self.shutdown.notify.notify_waiters();
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

    async fn download_job(
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
                        build,
                    )
                },
                |error| retryable_state_error(error).then_some(u32::MAX),
                |_| false,
                || StatsigErr::NetworkError(NetworkError::ShutdownError(job.primary_url.clone())),
            )
            .await
    }

    async fn download_id_list(
        &self,
        job: &IdListDownloadJob,
        is_fallback: bool,
        index: u32,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<DownloadedIdList, StatsigErr> {
        let download_permit = self
            .download_permits
            .clone()
            .acquire_owned()
            .await
            .map_err(|_| Self::publication_stopped())?;
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
            let start = job.plan.range_start + pending.bytes.len() as u64;
            let offer_snapshot = job.plan.can_offer_snapshot() && index == 0 && start == 0;
            let mut request = Self::id_list_file_request_args(download_url, job, start, &pending);
            if offer_snapshot {
                request
                    .headers
                    .get_or_insert_with(HashMap::new)
                    .insert("Accept".into(), snapshot_http::accept_header_value());
            }
            request.retries = self.file_retry_policy.attempts - 1;
            let response = self
                .network
                .request_once(
                    HttpMethod::GET,
                    request,
                    None,
                    is_fallback || job.plan.private_file || job.plan.source_changed,
                    true,
                    index,
                )
                .await
                .map_err(StatsigErr::NetworkError)?;
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
            self.add_diagnostics_start_marker(
                KeyType::GetIDList,
                StepType::Process,
                None,
                Some(download_url),
            );
            let chunk = normalize_id_list_download(
                response,
                download_url,
                job.plan.range_start,
                job.metadata.size,
                job.plan.private_file,
                pending,
            );
            self.add_diagnostics_end_marker(
                KeyType::GetIDList,
                StepType::Process,
                chunk.is_ok(),
                None,
                Some(download_url),
            );
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

    fn file_can_fallback(&self, job: &IdListDownloadJob) -> bool {
        !job.plan.private_file
            && self.fallback_to_statsig_api
            && job.primary_url != job.metadata.url
            && is_default_cdn_url(&job.metadata.url)
    }

    fn id_list_file_request_args(
        list_url: &str,
        job: &IdListDownloadJob,
        start: u64,
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

    fn get_override_id_list_download_url(&self, list_url: &str) -> Result<String, StatsigErr> {
        match &self.download_id_list_file_api {
            None => Ok(list_url.to_string()),
            Some(Ok(endpoint)) => replace_url_base(endpoint, list_url).map(Into::into),
            Some(Err(_)) => Err(StatsigErr::InvalidOperation(
                "invalid ID-list file endpoint".into(),
            )),
        }
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
        let _old = self
            .listener
            .write()
            .replace(HttpIdListsListener::External(listener));
    }

    fn is_current_listener(&self, listener: &Arc<dyn IdListsUpdateListener>) -> bool {
        self.listener
            .read()
            .clone()
            .is_some_and(|current| Arc::ptr_eq(&current.into_listener(), listener))
    }

    fn current_listener(&self) -> Result<HttpIdListsListener, StatsigErr> {
        self.listener
            .read()
            .clone()
            .ok_or_else(|| StatsigErr::UnstartedAdapter("Listener not set".to_string()))
    }

    fn publication_stopped() -> StatsigErr {
        StatsigErr::ShutdownFailure("ID-list publication stopped".into())
    }

    async fn while_running<T>(&self, work: impl Future<Output = T>) -> Result<T, StatsigErr> {
        let stopped = self.shutdown.notify.notified();
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
            if let Some(lazy) = &self.lazy_id_lists {
                let mut manifest = self.while_running(lazy.manifest.write()).await?;
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
            .sync_id_lists_with_trigger(trigger, &refresh_guard)
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
        self.refresh(RefreshTrigger::PrivateInitialize).await
    }

    async fn sync_id_lists_with_trigger(
        &self,
        trigger: RefreshTrigger,
        refresh_guard: &Arc<OwnedMutexGuard<()>>,
    ) -> Result<(), StatsigErr> {
        let background = trigger == RefreshTrigger::Background;
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
                trigger,
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
        trigger: RefreshTrigger,
        refresh_guard: &Arc<OwnedMutexGuard<()>>,
    ) -> Result<(), StatsigErr> {
        let listener = self.current_listener()?.into_listener();
        let Some(lazy) = &self.lazy_id_lists else {
            let current = listener.get_current_id_list_metadata();
            let update_batch = self
                .fetch_id_list_updates(
                    listener.as_ref(),
                    FetchReason::Refresh(trigger),
                    &current,
                    new_manifest,
                    successful_downloads,
                )
                .await?;
            let eager_downloads = (trigger == RefreshTrigger::PrivateInitialize
                && *successful_downloads > 0
                && listener.uses_parallel_id_list_init())
            .then_some(*successful_downloads);
            return self
                .publish_id_list_updates(
                    listener,
                    update_batch,
                    Some(refresh_guard),
                    None,
                    eager_downloads,
                )
                .await;
        };
        loop {
            let curr_manifest = {
                let _manifest = self.while_running(lazy.manifest.read()).await?;
                listener.get_current_id_list_metadata()
            };
            let active_manifest = new_manifest
                .iter()
                .filter(|(name, _entry)| curr_manifest.contains_key(name.as_str()))
                .map(|(name, entry)| (name.clone(), entry.clone()))
                .collect();
            let mut update_batch = self
                .fetch_id_list_updates(
                    listener.as_ref(),
                    FetchReason::Refresh(trigger),
                    &curr_manifest,
                    active_manifest,
                    successful_downloads,
                )
                .await?;

            // Commit the fetched generation and its updates atomically with
            // respect to on-demand publication. Downloads remain outside this guard.
            let mut manifest = self
                .while_running(lazy.manifest.clone().write_owned())
                .await?;
            let current = listener.get_current_id_list_metadata();
            if !update_batch.matches_cursors(&curr_manifest, &current) {
                continue;
            }
            // A cold load can install a valid prefix while this poll downloads another list.
            // Compare its advertised targets. The installed size is a consumed byte offset.
            for (name, current) in current {
                let previous = manifest.as_ref().and_then(|cached| cached.get(&name));
                if previous
                    .zip(new_manifest.get(&name))
                    .is_some_and(|(old, new)| same_id_list_generation(&old.metadata, &new.metadata))
                    && !update_batch.updates.contains_key(&name)
                {
                    if let Some(bases) = &mut update_batch.bases {
                        bases
                            .entry(name.clone())
                            .or_insert_with(|| IdListUpdateBase {
                                previous: Some(current.clone()),
                                list: None,
                            });
                    }
                    update_batch.updates.insert(
                        name,
                        IdListUpdate {
                            raw_changeset: None,
                            new_metadata: current,
                        },
                    );
                }
            }

            let next_manifest = if update_batch.bases.is_some() {
                Some(new_manifest)
            } else {
                *manifest = Some(new_manifest);
                None
            };
            return self
                .publish_id_list_updates(
                    listener,
                    update_batch,
                    Some(refresh_guard),
                    Some(LazyManifestPublication {
                        guard: manifest,
                        next: next_manifest,
                    }),
                    None,
                )
                .await;
        }
    }

    async fn fetch_id_list_updates(
        &self,
        listener: &dyn IdListsUpdateListener,
        reason: FetchReason<'_>,
        curr_manifest: &IdListsResponse,
        new_manifest: IdListsManifest,
        successful_downloads: &mut u64,
    ) -> Result<IdListUpdateBatch, StatsigErr> {
        let (publication_mode, background, build) = match reason {
            FetchReason::Refresh(trigger) => (
                IdListPublicationMode::Replace,
                trigger == RefreshTrigger::Background,
                None,
            ),
            FetchReason::Lazy(build) => (IdListPublicationMode::Merge, false, build),
        };
        let allow_snapshot_updates =
            self.snapshot_enabled && listener.supports_id_list_snapshot_updates();
        let batch = self.plan_id_list_updates(
            curr_manifest,
            new_manifest,
            successful_downloads,
            publication_mode,
            allow_snapshot_updates,
        )?;
        if batch.pending.is_empty() {
            return Ok(batch.update_batch);
        }
        let batch = Mutex::new(batch);
        let result = self
            .download_id_lists_with_fallback(&batch, background, build)
            .await;
        let mut batch = batch.into_inner();
        if let Err(error) = result {
            if !self.partial_refresh
                || matches!(
                    error,
                    StatsigErr::NetworkError(NetworkError::ShutdownError(_))
                )
            {
                return Err(error);
            }
            batch.retain_failed_lists(curr_manifest, error);
        }
        Ok(batch.update_batch)
    }

    fn plan_id_list_updates<'a>(
        &self,
        curr_manifest: &IdListsResponse,
        new_manifest: IdListsManifest,
        successful_downloads: &'a mut u64,
        publication_mode: IdListPublicationMode,
        allow_snapshot_updates: bool,
    ) -> Result<IdListDownloadBatch<'a>, StatsigErr> {
        let can_download_snapshots =
            allow_snapshot_updates && self.network.supports_wire_responses_without_redirects();
        let mut update_batch = IdListUpdateBatch::new(
            curr_manifest,
            &new_manifest,
            publication_mode,
            allow_snapshot_updates,
        );
        let mut jobs = Vec::new();
        let mut name_mismatches = 0usize;
        for (name, mut entry) in new_manifest {
            if self.partial_refresh && entry.metadata.name != name {
                // Evaluation and removals use the manifest key; persist that same name.
                entry.metadata.name.clone_from(&name);
                name_mismatches += 1;
            }
            update_batch
                .propagation
                .insert(name.clone(), entry.propagation_update());
            let metadata = entry.metadata;
            let current = curr_manifest.get(&name);
            let Some(plan) =
                IdListDownloadPlan::for_update(current, &metadata, can_download_snapshots)
            else {
                update_batch.updates.insert(
                    name,
                    IdListUpdate {
                        raw_changeset: None,
                        new_metadata: metadata,
                    },
                );
                continue;
            };
            match self.get_override_id_list_download_url(&metadata.url) {
                Ok(primary_url) => jobs.push(IdListDownloadJob {
                    name,
                    primary_url,
                    metadata,
                    plan,
                }),
                Err(error) if self.partial_refresh => {
                    update_batch.file_failure.get_or_insert(error);
                    update_batch.retain_failed_list(name, current);
                }
                Err(error) => return Err(error),
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
        Ok(IdListDownloadBatch {
            pending: jobs,
            update_batch,
            successful_downloads,
        })
    }

    async fn download_id_lists_with_fallback(
        &self,
        batch: &Mutex<IdListDownloadBatch<'_>>,
        background: bool,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<(), StatsigErr> {
        self.network
            .retry_executor(RetryPolicy {
                attempts: 1,
                jitter: false,
            })
            .run(
                |is_fallback, _| self.download_pending_id_lists(batch, is_fallback, build),
                |error| retryable_state_error(error).then_some(u32::MAX),
                |outcome| {
                    let eligible = self.file_failures.record(outcome, background);
                    let has_fallback = batch
                        .lock()
                        .pending
                        .iter()
                        .any(|job| self.file_can_fallback(job));
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
            .await
    }

    async fn download_pending_id_lists(
        &self,
        batch: &Mutex<IdListDownloadBatch<'_>>,
        is_fallback: bool,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<(), StatsigErr> {
        let jobs = std::mem::take(&mut batch.lock().pending);
        let mut downloads = stream::iter(jobs.into_iter().map(|job| async move {
            let result = self.download_job(&job, is_fallback, build).await;
            (job, result)
        }))
        .buffer_unordered(ID_LIST_DOWNLOAD_CONCURRENCY);
        let mut failure = None;
        while let Some((job, result)) = downloads.next().await {
            let mut batch = batch.lock();
            match result {
                Ok(download) => batch.record_download(job, download),
                Err(error) => {
                    // A terminal error takes precedence over exhausted retryable files.
                    if failure.as_ref().is_none_or(retryable_state_error) {
                        failure = Some(error);
                    }
                    batch.pending.push(job);
                }
            }
        }
        failure.map_or(Ok(()), Err)
    }

    async fn publish_id_list_updates(
        &self,
        listener: Arc<dyn IdListsUpdateListener>,
        update_batch: IdListUpdateBatch,
        refresh_guard: Option<&Arc<OwnedMutexGuard<()>>>,
        manifest_guard: Option<LazyManifestPublication>,
        eager_downloads: Option<u64>,
    ) -> Result<(), StatsigErr> {
        let IdListUpdateBatch {
            publication_mode,
            bases,
            updates,
            propagation,
            file_failure,
        } = update_batch;
        let incomplete = file_failure.is_some();
        let blocking_listener = listener.requires_blocking_id_list_publication();
        let offload = blocking_listener || eager_downloads.is_some();
        let stopped = self.network.shutdown_flag();
        // Keep the elected listener (and its lease) through installation, even if
        // the refresh future is cancelled while a blocking publication is running.
        let publish = move |stopped: &AtomicBool| {
            if stopped.load(Ordering::SeqCst) {
                return Err(Self::publication_stopped());
            }
            let mode = if incomplete {
                IdListPublicationMode::IncompleteRefresh
            } else {
                publication_mode
            };
            publish_id_list_batch(
                listener.as_ref(),
                bases,
                updates,
                propagation,
                mode,
                eager_downloads,
            )?;
            if let Some(LazyManifestPublication {
                mut guard,
                next: Some(next),
            }) = manifest_guard
            {
                *guard = Some(next);
            }
            Ok(())
        };
        if offload {
            // An opted-in hash commit runs off-thread but still participates in force_shutdown.
            let shutdown = (!blocking_listener).then(|| Arc::clone(&self.shutdown));
            let stopped = Arc::clone(stopped);
            let guard = refresh_guard.cloned();
            let policy = self.output_policy;
            tokio::task::spawn_blocking(move || {
                let _guard = guard;
                let _scope = policy.enter();
                let _handoff = shutdown.as_ref().map(|state| state.handoff.lock());
                publish(&stopped)
            })
            .await
            .map_err(|error| StatsigErr::FileError(error.to_string()))??;
        } else {
            let _handoff = self.shutdown.handoff.lock();
            publish(stopped)?;
        }
        file_failure.map_or(Ok(()), Err)
    }

    /// Loads the requested name from the cached manifest. A concurrent change to its
    /// generation or installed membership makes us plan again from the current cursor.
    async fn load_and_publish_id_list(
        self: &Arc<Self>,
        name: &str,
        parallel: Option<&PrivateBuildAttempt>,
    ) -> Result<(), StatsigErr> {
        let lazy = self.lazy_id_lists.as_ref().ok_or_else(|| {
            StatsigErr::UnstartedAdapter("ID-list manifest has not been fetched yet".to_string())
        })?;
        loop {
            if let Some(build) = parallel {
                build.submitted.store(false, Ordering::Release);
            }
            let Some(load) = self.plan_lazy_load(lazy, name, parallel).await? else {
                return Ok(());
            };

            let mut successful_downloads = 0;
            let target = load.entry.metadata.clone();
            let (listener, build): (&dyn IdListsUpdateListener, _) = match &load.destination {
                LazyLoadDestination::Store(private) => {
                    (private.store.as_ref(), Some(private.build))
                }
                LazyLoadDestination::Listener(listener) => (listener.as_ref(), None),
            };
            let update_batch = self
                .fetch_id_list_updates(
                    listener,
                    FetchReason::Lazy(build),
                    &load.installed_metadata,
                    HashMap::from([(name.to_owned(), load.entry)]),
                    &mut successful_downloads,
                )
                .await?;

            let outcome = match load.destination {
                LazyLoadDestination::Store(private) => {
                    self.build_and_publish_private_list(lazy, name, target, private, update_batch)
                        .await?
                }
                LazyLoadDestination::Listener(listener) => {
                    self.publish_lazy_list_to_listener(
                        lazy,
                        name,
                        &target,
                        listener,
                        &load.installed_metadata,
                        update_batch,
                    )
                    .await?
                }
            };
            match outcome {
                LazyLoadOutcome::Complete => return Ok(()),
                LazyLoadOutcome::Retry => continue,
            }
        }
    }

    async fn plan_lazy_load<'a>(
        &self,
        lazy: &LazyIdLists,
        name: &str,
        parallel: Option<&'a PrivateBuildAttempt>,
    ) -> Result<Option<LazyIdListLoad<'a>>, StatsigErr> {
        let manifest = lazy.manifest.read().await;
        let manifest = manifest.as_ref().ok_or_else(|| {
            StatsigErr::UnstartedAdapter("ID-list manifest has not been fetched yet".to_string())
        })?;
        let entry = manifest.get(name).ok_or_else(|| {
            StatsigErr::CustomError(format!("ID list {name} is missing from the manifest"))
        })?;
        let (destination, installed_metadata) = match (self.current_listener()?, parallel) {
            (HttpIdListsListener::Store(store), Some(build)) => {
                let installed_list = store.load_data().id_lists.get(name).cloned();
                let metadata = installed_list
                    .iter()
                    .map(|list| (name.to_owned(), list.metadata.clone()))
                    .collect();
                (
                    LazyLoadDestination::Store(PrivateIdListLoad {
                        store,
                        installed_list,
                        build,
                    }),
                    metadata,
                )
            }
            (listener, _) => {
                let listener = listener.into_listener();
                let metadata = listener.get_current_id_list_metadata();
                (LazyLoadDestination::Listener(listener), metadata)
            }
        };
        let listener: &dyn IdListsUpdateListener = match &destination {
            LazyLoadDestination::Store(private) => private.store.as_ref(),
            LazyLoadDestination::Listener(listener) => listener.as_ref(),
        };
        if self.lazy_list_ready(listener, installed_metadata.get(name), &entry.metadata) {
            return Ok(None);
        }
        Ok(Some(LazyIdListLoad {
            entry: entry.clone(),
            installed_metadata,
            destination,
        }))
    }

    async fn build_and_publish_private_list(
        self: &Arc<Self>,
        lazy: &LazyIdLists,
        name: &str,
        target: IdListMetadata,
        private: PrivateIdListLoad<'_>,
        mut update_batch: IdListUpdateBatch,
    ) -> Result<LazyLoadOutcome, StatsigErr> {
        let update = update_batch.updates.remove(name).ok_or_else(|| {
            StatsigErr::InvalidOperation(format!("Missing update for ID list {name}"))
        })?;
        let PrivateIdListLoad {
            store,
            installed_list,
            build,
        } = private;
        let image = update_batch
            .bases
            .and_then(|mut bases| bases.remove(name)?.list);
        let (base, list) = lazy
            .build_index(
                Arc::clone(&store),
                installed_list,
                image,
                update,
                build,
                self,
            )
            .await?;

        let adapter = Arc::clone(self);
        let name = name.to_owned();
        let listener: Arc<dyn IdListsUpdateListener> = store.clone();
        Self::with_manifest_for_private_commit(&lazy.manifest, move |manifest| {
            let _output_scope = adapter.output_policy.enter();
            if !adapter.is_current_lazy_target(manifest, &name, &target, &listener)? {
                return Ok(LazyLoadOutcome::Retry);
            }
            // force_shutdown waits for an in-progress hash handoff.
            let _handoff = (!store.requires_blocking_id_list_publication())
                .then(|| adapter.shutdown.handoff.lock());
            if adapter.network.shutdown_flag().load(Ordering::SeqCst) {
                return Err(Self::publication_stopped());
            }
            if store.commit_lazy_id_list(&name, base.as_ref(), list, update_batch.propagation)? {
                Ok(LazyLoadOutcome::Complete)
            } else {
                Ok(LazyLoadOutcome::Retry)
            }
        })
        .await
    }

    async fn publish_lazy_list_to_listener(
        &self,
        lazy: &LazyIdLists,
        name: &str,
        target: &IdListMetadata,
        listener: Arc<dyn IdListsUpdateListener>,
        planned_metadata: &IdListsResponse,
        update_batch: IdListUpdateBatch,
    ) -> Result<LazyLoadOutcome, StatsigErr> {
        let manifest = lazy.manifest.clone().write_owned().await;
        if !self.is_current_lazy_target(manifest.as_ref(), name, target, &listener)? {
            return Ok(LazyLoadOutcome::Retry);
        }
        let installed = listener.get_current_id_list_metadata();
        if self.lazy_list_ready(listener.as_ref(), installed.get(name), target) {
            return Ok(LazyLoadOutcome::Complete);
        }
        if !update_batch.matches_cursors(planned_metadata, &installed) {
            return Ok(LazyLoadOutcome::Retry);
        }
        self.publish_id_list_updates(
            listener,
            update_batch,
            None,
            Some(LazyManifestPublication {
                guard: manifest,
                next: None,
            }),
            None,
        )
        .await?;
        Ok(LazyLoadOutcome::Complete)
    }

    fn lazy_list_ready(
        &self,
        listener: &dyn IdListsUpdateListener,
        installed: Option<&IdListMetadata>,
        target: &IdListMetadata,
    ) -> bool {
        if self.snapshot_enabled
            && listener.supports_id_list_snapshot_updates()
            && self.network.supports_wire_responses_without_redirects()
        {
            if installed.is_some_and(|old| old.creation_time > target.creation_time) {
                return true;
            }
            let private_file = snapshot_http::private_generation(target);
            if snapshot_http::source_changed(installed, target, private_file) {
                return false;
            }
            if private_file {
                // A negotiated prefix is ready for evaluation. Polls catch it up.
                return installed.is_some_and(|old| {
                    old.file_id == target.file_id
                        && old.creation_time == target.creation_time
                        && (old.size > 0 || target.size == 0)
                });
            }
        }
        id_list_is_at_target(installed, target)
    }

    fn is_current_lazy_target(
        &self,
        manifest: Option<&IdListsManifest>,
        name: &str,
        target: &IdListMetadata,
        listener: &Arc<dyn IdListsUpdateListener>,
    ) -> Result<bool, StatsigErr> {
        let latest = manifest
            .and_then(|entries| entries.get(name))
            .ok_or_else(|| {
                StatsigErr::CustomError(format!("ID list {name} is missing from the manifest"))
            })?;
        Ok(self.is_current_listener(listener) && same_id_list_generation(target, &latest.metadata))
    }

    async fn with_manifest_for_private_commit(
        manifest: &Arc<AsyncRwLock<Option<IdListsManifest>>>,
        mut commit: impl FnOnce(Option<&IdListsManifest>) -> Result<LazyLoadOutcome, StatsigErr>
        + Send
        + 'static,
    ) -> Result<LazyLoadOutcome, StatsigErr> {
        loop {
            let lock = Arc::clone(manifest);
            // Take the guard only once the worker is running. If a poll owns it,
            // leave the blocking thread free for the poll's own publication.
            let attempt = tokio::task::spawn_blocking(move || match lock.try_read() {
                Ok(guard) => ControlFlow::Break(commit(guard.as_ref())),
                Err(_) => ControlFlow::Continue(commit),
            })
            .await
            .map_err(|e| StatsigErr::ThreadFailure(e.to_string()))?;
            match attempt {
                ControlFlow::Break(result) => return result,
                ControlFlow::Continue(pending) => commit = pending,
            }
            drop(manifest.read().await);
        }
    }

    /// Concurrent callers for the same name share the download and installation.
    pub(crate) async fn process_id_list(self: &Arc<Self>, name: &str) -> Result<(), StatsigErr> {
        let Some(permits) = self
            .lazy_id_lists
            .as_ref()
            .and_then(|lazy| lazy.build_permits.as_ref())
        else {
            return self.wait_for_id_list(name, None).await;
        };
        let runtime = tokio::runtime::Handle::current();
        let build = Arc::new(PrivateBuildAttempt {
            permits: Arc::clone(permits),
            submitted: AtomicBool::new(false),
        });
        let adapter = Arc::clone(self);
        let name = name.to_owned();
        let attempt = Arc::clone(&build);
        let load = async move { adapter.wait_for_id_list(&name, Some(&attempt)).await };
        // A blocking build cannot be aborted. Keep its per-name waiter until publication
        // even if the evaluator goes away. Earlier cancellation still drops network work.
        let mut load = scopeguard::guard(Box::pin(load), |load| {
            if build.submitted.load(Ordering::Acquire) {
                runtime.spawn(load);
            }
        });
        let result = load.as_mut().await;
        drop(scopeguard::ScopeGuard::into_inner(load));
        result
    }

    async fn wait_for_id_list(
        self: &Arc<Self>,
        name: &str,
        parallel: Option<&PrivateBuildAttempt>,
    ) -> Result<(), StatsigErr> {
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
                let waiter = IdListLoadWaiter {
                    loads: &self.in_flight_loads,
                    name,
                    shared: Arc::clone(&shared),
                };

                self.while_running(
                    shared
                        .result
                        .get_or_init(|| self.load_and_publish_id_list(waiter.name, parallel)),
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
        url: Option<&str>,
    ) {
        if self.ops_stats.remote_telemetry_disabled() {
            return;
        }
        let mut marker = Marker::new(key, ActionType::Start, Some(step));
        if let Some(count) = id_list_count {
            marker = marker.with_id_list_count(count);
        }
        if let Some(url) = url {
            marker = marker.with_url(url.to_string());
        }
        self.ops_stats.add_marker(marker, None);
    }

    fn add_diagnostics_end_marker(
        &self,
        key: KeyType,
        step: StepType,
        success: bool,
        status_code: Option<u16>,
        url: Option<&str>,
    ) {
        if self.ops_stats.remote_telemetry_disabled() {
            return;
        }
        let mut marker = Marker::new(key, ActionType::End, Some(step)).with_is_success(success);
        if let Some(status_code) = status_code {
            marker = marker.with_status_code(status_code);
        }
        if let Some(url) = url {
            marker = marker.with_url(url.to_string());
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

struct IdListDownloadPlan {
    range_start: u64,
    private_file: bool,
    source_changed: bool,
}

impl IdListDownloadPlan {
    fn can_offer_snapshot(&self) -> bool {
        self.private_file && self.range_start == 0
    }

    fn for_update(
        current: Option<&IdListMetadata>,
        target: &IdListMetadata,
        can_download_snapshots: bool,
    ) -> Option<Self> {
        let private_file = can_download_snapshots && snapshot_http::private_generation(target);
        let source_changed =
            can_download_snapshots && snapshot_http::source_changed(current, target, private_file);
        let range_start = if source_changed {
            // A cursor is scoped to its source. Ignore stale switches and restart newer ones.
            (current?.creation_time <= target.creation_time).then_some(0)?
        } else {
            id_list_range_start(current, target)?
        };
        Some(Self {
            range_start,
            private_file,
            source_changed,
        })
    }
}

struct IdListDownloadJob {
    name: String,
    primary_url: String,
    metadata: IdListMetadata,
    plan: IdListDownloadPlan,
}

enum DownloadedIdList {
    Raw {
        changeset: String,
        range: Range<u64>,
    },
    Snapshot(IdList),
}

struct IdListDownloadBatch<'a> {
    pending: Vec<IdListDownloadJob>,
    update_batch: IdListUpdateBatch,
    successful_downloads: &'a mut u64,
}

impl IdListDownloadBatch<'_> {
    fn record_download(&mut self, job: IdListDownloadJob, download: DownloadedIdList) {
        // Count each completion even if the refresh is cancelled while peers are pending.
        *self.successful_downloads += 1;
        let mut metadata = job.metadata;
        let (changeset, range, list) = match download {
            DownloadedIdList::Raw { changeset, range } => (changeset, range, None),
            DownloadedIdList::Snapshot(list) => {
                metadata.size = list.metadata.size;
                (String::new(), 0..metadata.size, Some(list))
            }
        };
        if let Some(bases) = &mut self.update_batch.bases {
            let base = bases.entry(job.name.clone()).or_insert(IdListUpdateBase {
                previous: None,
                list: None,
            });
            base.list = list.or_else(|| {
                // A file ID is scoped to its source. Raw data from a replacement URL
                // must also start from empty membership.
                job.plan
                    .source_changed
                    .then(|| IdList::new(metadata.clone()))
            });
        }
        if let Some(observation) = self.update_batch.propagation.get_mut(&job.name) {
            observation.applied_range = Some(range);
        }
        self.update_batch.updates.insert(
            job.name,
            IdListUpdate {
                raw_changeset: Some(changeset),
                new_metadata: metadata,
            },
        );
    }

    fn retain_failed_lists(&mut self, installed: &IdListsResponse, error: StatsigErr) {
        // Failed warm downloads retain their installed generation and byte offset.
        for job in self.pending.drain(..) {
            let current = installed.get(&job.name);
            self.update_batch.retain_failed_list(job.name, current);
        }
        self.update_batch.file_failure.get_or_insert(error);
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
    private_file: bool,
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
    let mut bytes = body.read_to_bytes()?;
    // A proxy can strip the snapshot headers even when the body is valid UTF-8.
    let reject_snapshot = |prefix: &[u8], total| {
        if portable_id_list_ef::matches_v1_prefix(prefix, total) {
            return Err(request_failed(
                "Received a binary ID-list snapshot as raw data",
            ));
        }
        Ok(())
    };
    if private_file {
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
    if private_file && committed_start == 0 {
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
                !(private_file
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

struct LazyManifestPublication {
    guard: OwnedRwLockWriteGuard<Option<IdListsManifest>>,
    next: Option<IdListsManifest>,
}

struct IdListUpdateBatch {
    publication_mode: IdListPublicationMode,
    bases: Option<HashMap<String, IdListUpdateBase>>,
    file_failure: Option<StatsigErr>,
    updates: HashMap<String, IdListUpdate>,
    propagation: HashMap<String, IdListPropagationUpdate>,
}

impl IdListUpdateBatch {
    fn new(
        curr_manifest: &IdListsResponse,
        new_manifest: &IdListsManifest,
        publication_mode: IdListPublicationMode,
        allow_snapshot_updates: bool,
    ) -> Self {
        // A replacement can remove installed names, so their cursors must also
        // be captured before downloading and checked at publication.
        let bases = allow_snapshot_updates.then(|| {
            curr_manifest
                .iter()
                .filter(|(name, _)| {
                    publication_mode != IdListPublicationMode::Merge
                        || new_manifest.contains_key(*name)
                })
                .map(|(name, metadata)| {
                    (
                        name.clone(),
                        IdListUpdateBase {
                            previous: Some(metadata.clone()),
                            list: None,
                        },
                    )
                })
                .collect::<HashMap<_, _>>()
        });
        Self {
            publication_mode,
            bases,
            file_failure: None,
            updates: HashMap::new(),
            propagation: HashMap::with_capacity(new_manifest.len()),
        }
    }

    fn retain_failed_list(&mut self, name: String, installed: Option<&IdListMetadata>) {
        self.propagation.remove(&name);
        if let Some(metadata) = installed {
            self.updates.insert(
                name,
                IdListUpdate {
                    raw_changeset: None,
                    new_metadata: metadata.clone(),
                },
            );
        }
    }

    // A poll and a cold load can download from the same partial cursor. Only the
    // first may apply that range. The other prepares again at the committed end.
    fn matches_cursors(&self, planned: &IdListsResponse, installed: &IdListsResponse) -> bool {
        self.updates.iter().all(|(name, update)| {
            id_list_range_start(planned.get(name), &update.new_metadata)
                == id_list_range_start(installed.get(name), &update.new_metadata)
        })
    }
}

fn id_list_range_start(current: Option<&IdListMetadata>, target: &IdListMetadata) -> Option<u64> {
    target
        .file_version()
        .download_from(current.map(IdListMetadata::file_version))
        .map(|update| update.start)
}

fn id_list_is_at_target(current: Option<&IdListMetadata>, target: &IdListMetadata) -> bool {
    target
        .file_version()
        .update_from(current.map(IdListMetadata::file_version))
        .is_none()
}

fn publish_id_list_batch(
    listener: &dyn IdListsUpdateListener,
    bases: Option<HashMap<String, IdListUpdateBase>>,
    updates: HashMap<String, IdListUpdate>,
    propagation: HashMap<String, IdListPropagationUpdate>,
    publication_mode: IdListPublicationMode,
    eager_downloads: Option<u64>,
) -> Result<(), StatsigErr> {
    if let Some(bases) = bases {
        return listener.try_receive_id_list_snapshot_updates(
            updates,
            bases,
            propagation,
            publication_mode,
            eager_downloads,
        );
    }
    if let Some(downloads) = eager_downloads {
        return listener.try_receive_eager_id_list_updates(
            updates,
            propagation,
            publication_mode == IdListPublicationMode::IncompleteRefresh,
            downloads,
        );
    }
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
    name: &'a str,
    shared: Arc<SharedIdListLoad>,
}

impl Drop for IdListLoadWaiter<'_> {
    fn drop(&mut self) {
        if self.shared.waiters.fetch_sub(1, Ordering::AcqRel) == 1 {
            self.loads.remove_if(self.name, |_, active| {
                Arc::ptr_eq(active, &self.shared) && active.waiters.load(Ordering::Acquire) == 0
            });
        }
    }
}

#[cfg(test)]
type BeforeIndexBuild = dyn Fn(&str) + Send + Sync;

fn parallel_lazy_builds_enabled(options: &StatsigOptions, env: Option<&std::ffi::OsStr>) -> bool {
    match env {
        Some(value) => value == "true",
        None => options
            .experimental_flags
            .as_ref()
            .is_some_and(|flags| flags.contains("parallel_lazy_id_list_builds")),
    }
}

enum FetchReason<'a> {
    Refresh(RefreshTrigger),
    Lazy(Option<&'a PrivateBuildAttempt>),
}

struct PrivateBuildAttempt {
    permits: Arc<Semaphore>,
    submitted: AtomicBool,
}

impl PrivateBuildAttempt {
    async fn admit_worker(&self) -> tokio::sync::OwnedSemaphorePermit {
        let permit = Arc::clone(&self.permits)
            .acquire_owned()
            .await
            .expect("index build semaphore is never closed");
        self.submitted.store(true, Ordering::Release);
        permit
    }
}

struct LazyIdListLoad<'a> {
    entry: IdListManifestEntry,
    installed_metadata: IdListsResponse,
    destination: LazyLoadDestination<'a>,
}

enum LazyLoadDestination<'a> {
    Store(PrivateIdListLoad<'a>),
    Listener(Arc<dyn IdListsUpdateListener>),
}

enum LazyLoadOutcome {
    Complete,
    Retry,
}

struct PrivateIdListLoad<'a> {
    build: &'a PrivateBuildAttempt,
    store: Arc<SpecStore>,
    installed_list: Option<IdList>,
}

struct LazyIdLists {
    /// Polls and listener replacements take the write lock. A private lazy load reads
    /// the manifest when planning, then checks it again under a read lock at publication.
    manifest: Arc<AsyncRwLock<Option<IdListsManifest>>>,
    build_permits: Option<Arc<Semaphore>>,
    #[cfg(test)]
    before_build: Option<Arc<BeforeIndexBuild>>,
}

impl LazyIdLists {
    async fn build_index(
        &self,
        store: Arc<SpecStore>,
        base: Option<IdList>,
        image: Option<IdList>,
        update: IdListUpdate,
        build: &PrivateBuildAttempt,
        adapter: &StatsigHttpIdListsAdapter,
    ) -> Result<(Option<IdList>, IdList), StatsigErr> {
        // A full snapshot already completed its index work in the validator.
        if image.is_some() && update.raw_changeset.as_deref() == Some("") {
            let list = store.updated_id_list(base.as_ref(), image, update);
            return Ok((base, list));
        }
        let permit = build.admit_worker().await;
        let output_policy = adapter.output_policy;
        let stopped = Arc::clone(adapter.network.shutdown_flag());
        #[cfg(test)]
        let before_build = self.before_build.clone();
        tokio::task::spawn_blocking(move || {
            let _output_scope = output_policy.enter();
            let _permit = permit;
            if stopped.load(Ordering::SeqCst) {
                return Err(StatsigHttpIdListsAdapter::publication_stopped());
            }
            #[cfg(test)]
            if let Some(before_build) = before_build {
                before_build(&update.new_metadata.name);
            }
            let list = store.updated_id_list(base.as_ref(), image, update);
            Ok((base, list))
        })
        .await
        .map_err(|e| StatsigErr::ThreadFailure(e.to_string()))?
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
            .scope(self.refresh_with_listener(RefreshTrigger::PrivateInitialize, Some(listener)))
            .await
    }

    async fn shutdown(&self, timeout: Duration) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.signal_shutdown();
                tokio::time::timeout(timeout, async {
                    let _refresh = self.refresh_gate.lock().await;
                    if let Some(lazy) = &self.lazy_id_lists {
                        // Blocking builds already in progress finish before graceful shutdown.
                        if let Some(permits) = &lazy.build_permits {
                            drop(
                                permits
                                    .acquire_many(PRIVATE_INDEX_BUILD_CONCURRENCY as u32)
                                    .await,
                            );
                        }
                        drop(lazy.manifest.write().await);
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

                let shutdown = self.shutdown.clone();
                let stopped = self.network.shutdown_flag().clone();
                statsig_runtime.spawn(
                    "http_id_list_bg_sync",
                    move |runtime_shutdown| async move {
                        loop {
                            let notified = shutdown.notify.notified();
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
#[path = "__tests__/lazy_id_list_tests.rs"]
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

#[cfg(all(test, not(feature = "custom_network_provider")))]
#[path = "__tests__/snapshot_http_tests.rs"]
mod snapshot_http_tests;
