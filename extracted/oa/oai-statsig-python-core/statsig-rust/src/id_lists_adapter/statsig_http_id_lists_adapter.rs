#[path = "http_transport.rs"]
mod http_transport;
use http_transport::IdListHttpTransport;
#[path = "snapshot_http.rs"]
mod snapshot_http;
use super::id_list_load_timing::{self, Phase};
use super::id_list_updates::id_list_range_start;
use super::statsig_shared_id_lists_adapter::PublishingListener;
use super::{
    IdList, IdListManifest, IdListManifestEntry, IdListMetadata, IdListUpdateBatch,
    PreparedIdListUpdate,
};
use super::{SharedInitialBaseCache, UpdateMode};
use crate::id_lists_adapter::{
    IdListPublicationMode, IdListUpdate, IdListsAdapter, IdListsUpdateListener,
};
use crate::networking::retry::{
    PrimaryOutcome, RefreshFailureTracker, RetryPolicy, retryable_state_error,
};
#[cfg(test)]
use crate::networking::{
    DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, HttpMethod, RequestArgs, ResponseData,
};
use crate::networking::{NetworkClient, NetworkError};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::KeyType;
use crate::statsig::remote_id_lists::RemoteIdListResolver;
use crate::{SpecStore, StatsigErr, StatsigOptions, StatsigRuntime, log_d, log_e};
use async_trait::async_trait;
use chrono::Utc;
use dashmap::DashMap;
use futures::{StreamExt, stream};
use parking_lot::{Mutex, ReentrantMutex, RwLock};
use std::collections::HashMap;
use std::future::Future;
use std::ops::{ControlFlow, Range};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, OnceLock, Weak};
use std::time::Duration;
use tokio::sync::{
    Notify, OnceCell, OwnedMutexGuard, OwnedRwLockWriteGuard, RwLock as AsyncRwLock, Semaphore,
};
use tokio::time::sleep;

const DEFAULT_ID_LIST_SYNC_INTERVAL_MS: u32 = 60_000;
const ID_LIST_DOWNLOAD_CONCURRENCY: usize = 4;
const PRIVATE_INDEX_BUILD_CONCURRENCY: usize = 2;

type IdListsResponse = HashMap<String, IdListMetadata>;

const TAG: &str = stringify!(StatsigHttpIdListsAdapter);
const ID_LISTS_SYNC_OVERALL_LATENCY_METRIC: &str = "id_lists_sync_overall.latency";
const ID_LISTS_SYNC_OVERALL_MANIFEST_SUCCESS_TAG: &str = "id_list_manifest_success";
const ID_LISTS_SYNC_OVERALL_SUCCEED_SINGLE_ID_LIST_NUMBER_TAG: &str =
    "succeed_single_id_list_number";

#[cfg(test)]
tokio::task_local! {
    pub(crate) static TEST_CDN_MANIFEST_URL: String;
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
    Publisher(Arc<PublishingListener>),
    Store(Arc<SpecStore>),
    External(Arc<dyn IdListsUpdateListener>),
}

#[derive(Clone, Copy)]
struct BaseSources {
    snapshots: bool,
    cache: bool,
}

impl HttpIdListsListener {
    fn as_ref(&self) -> &dyn IdListsUpdateListener {
        match self {
            Self::Store(store) => store.as_ref(),
            Self::Publisher(publisher) => publisher.as_ref(),
            Self::External(listener) => listener.as_ref(),
        }
    }

    fn publish(
        &self,
        batch: IdListUpdateBatch,
        eager_downloads: Option<u64>,
    ) -> Result<(), StatsigErr> {
        match self {
            Self::Store(store) => store.publish_prepared_id_lists(batch, eager_downloads),
            Self::Publisher(publisher) => publisher.publish_prepared_id_lists(batch),
            Self::External(listener) => {
                batch.publish_to_listener(listener.as_ref(), eager_downloads)
            }
        }
    }
}

pub struct StatsigHttpIdListsAdapter {
    output_policy: crate::output_policy::OutputPolicy,
    partial_refresh: bool,
    initial_base_cache: Option<Arc<SharedInitialBaseCache>>,
    listener: RwLock<Option<HttpIdListsListener>>,
    pub(crate) membership_resolver: OnceLock<Weak<RemoteIdListResolver>>,
    pub(super) membership_publisher: Option<Arc<PublishingListener>>,
    pub(super) refresh_gate: Arc<tokio::sync::Mutex<()>>,
    transport: IdListHttpTransport,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    pub(crate) load_timings_enabled: bool,
    shutdown: Arc<AdapterShutdown>,
    file_failures: RefreshFailureTracker,
    /// Temporary per-list singleflight entries. Concurrent callers for the same
    /// name await one shared load instead of scheduling duplicate body requests.
    in_flight_loads: DashMap<String, Arc<SharedIdListLoad>>,
    lazy_id_lists: Option<LazyIdLists>,
}

fn publication_stopped() -> StatsigErr {
    StatsigErr::ShutdownFailure("ID-list publication stopped".into())
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

    pub(crate) fn with_initial_base_cache(mut self, cache: Option<SharedInitialBaseCache>) -> Self {
        self.initial_base_cache = cache.map(Arc::new);
        self
    }

    pub(super) fn with_partial_refresh(
        sdk_key: &str,
        options: &StatsigOptions,
        partial_refresh: bool,
    ) -> Self {
        let output_policy = crate::output_policy::OutputPolicy::from_options(Some(options));
        let _output_scope = output_policy.enter();
        let sync_interval_duration = Duration::from_millis(u64::from(
            options
                .id_lists_sync_interval_ms
                .unwrap_or(DEFAULT_ID_LIST_SYNC_INTERVAL_MS),
        ));

        let sdk_instance_id = options.get_sdk_instance_id(sdk_key);
        let ops_stats = OPS_STATS.get_for_instance_with_options(sdk_instance_id, Some(options));

        Self {
            output_policy,
            partial_refresh,
            initial_base_cache: None,
            listener: RwLock::new(None),
            membership_resolver: OnceLock::new(),
            membership_publisher: None,
            refresh_gate: Default::default(),
            transport: IdListHttpTransport::new(sdk_key, options, ops_stats.clone()),
            sync_interval_duration,
            ops_stats,
            load_timings_enabled: id_list_load_timing::collection_enabled(Some(options)),
            shutdown: Arc::default(),
            file_failures: RefreshFailureTracker::default(),
            lazy_id_lists: (options.lazy_load_id_lists == Some(true)).then(|| LazyIdLists {
                manifest: Default::default(),
                build_permits: None,
                #[cfg(test)]
                before_build: None,
            }),
            in_flight_loads: DashMap::new(),
        }
    }

    pub(crate) fn network(&self) -> Arc<NetworkClient> {
        Arc::clone(&self.transport.network)
    }

    pub fn force_shutdown(&self) {
        self.signal_shutdown();
        // The listener itself may request shutdown while holding this fence.
        drop(self.shutdown.handoff.lock());
    }

    pub(super) fn signal_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.transport.network.shutdown();
        self.shutdown.notify.notify_waiters();
    }

    #[cfg(test)]
    pub(crate) fn set_network_provider_for_test(
        &mut self,
        provider: std::sync::Weak<dyn crate::networking::NetworkProvider>,
    ) {
        Arc::get_mut(&mut self.transport.network)
            .expect("network provider must be set before sharing the client")
            .set_network_provider_for_test(provider);
    }

    pub(super) fn set_publisher(&self, publisher: Arc<PublishingListener>) {
        let _old = self
            .listener
            .write()
            .replace(HttpIdListsListener::Publisher(publisher));
    }

    pub(crate) fn set_listener(&self, listener: Arc<dyn IdListsUpdateListener>) {
        let _old = self
            .listener
            .write()
            .replace(HttpIdListsListener::External(listener));
    }

    fn is_current_listener(&self, listener: &dyn IdListsUpdateListener) -> bool {
        self.listener
            .read()
            .as_ref()
            .is_some_and(|current| std::ptr::addr_eq(current.as_ref(), listener))
    }

    fn current_listener(&self) -> Result<HttpIdListsListener, StatsigErr> {
        self.listener
            .read()
            .clone()
            .ok_or_else(|| StatsigErr::UnstartedAdapter("Listener not set".to_string()))
    }

    fn ensure_running(&self) -> Result<(), StatsigErr> {
        if self
            .transport
            .network
            .shutdown_flag()
            .load(Ordering::SeqCst)
        {
            return Err(publication_stopped());
        }
        Ok(())
    }

    async fn while_running<T>(&self, work: impl Future<Output = T>) -> Result<T, StatsigErr> {
        let stopped = self.shutdown.notify.notified();
        self.ensure_running()?;
        tokio::select! {
            biased;
            () = stopped => Err(publication_stopped()),
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
        if let Some(listener) =
            listener.filter(|listener| !self.is_current_listener(listener.as_ref()))
        {
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
                self.transport.add_process_end_marker(
                    KeyType::GetIDListSources,
                    summary.success,
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
            .transport
            .fetch_id_list_manifests_from_network(background)
            .await?;
        if let Some(resolver) = self.membership_resolver.get().and_then(Weak::upgrade) {
            let _handoff = self.shutdown.handoff.lock();
            self.ensure_running()?;
            resolver.observe_manifest(&new_manifest);
        }
        if let Some(publisher) = &self.membership_publisher {
            publisher.stage_manifest_revisions(&new_manifest);
        }
        self.transport.add_process_start_marker(
            KeyType::GetIDListSources,
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
        new_manifest: IdListManifest,
        successful_downloads: &mut u64,
        trigger: RefreshTrigger,
        refresh_guard: &Arc<OwnedMutexGuard<()>>,
    ) -> Result<(), StatsigErr> {
        let listener = self.current_listener()?;
        let Some(lazy) = &self.lazy_id_lists else {
            let current = listener.as_ref().get_current_id_list_metadata();
            let update_batch = self
                .fetch_id_list_updates(
                    self.base_sources(&listener),
                    FetchReason::Refresh(trigger),
                    &current,
                    new_manifest,
                    successful_downloads,
                )
                .await?;
            let eager_downloads = (trigger == RefreshTrigger::PrivateInitialize
                && *successful_downloads > 0
                && listener.as_ref().uses_parallel_id_list_init())
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
                listener.as_ref().get_current_id_list_metadata()
            };
            let active_manifest = new_manifest
                .iter()
                .filter(|(name, _entry)| curr_manifest.contains_key(name.as_str()))
                .map(|(name, entry)| (name.clone(), entry.clone()))
                .collect();
            let mut update_batch = self
                .fetch_id_list_updates(
                    self.base_sources(&listener),
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
            let current = listener.as_ref().get_current_id_list_metadata();
            if !update_batch.matches_cursors(&curr_manifest, &current) {
                continue;
            }
            update_batch.preserve_concurrent_loads(current, manifest.as_ref(), &new_manifest);

            let next_manifest = if update_batch.expected.is_some() {
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

    fn base_sources(&self, listener: &HttpIdListsListener) -> BaseSources {
        BaseSources {
            snapshots: self.transport.snapshot_enabled
                && listener.as_ref().supports_id_list_snapshot_updates(),
            cache: self.initial_base_cache.is_some()
                && matches!(listener, HttpIdListsListener::Store(_)),
        }
    }

    async fn fetch_id_list_updates(
        &self,
        sources: BaseSources,
        reason: FetchReason<'_>,
        curr_manifest: &IdListsResponse,
        new_manifest: IdListManifest,
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
        let batch = self.plan_id_list_updates(
            curr_manifest,
            new_manifest,
            successful_downloads,
            publication_mode,
            sources,
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
        new_manifest: IdListManifest,
        successful_downloads: &'a mut u64,
        publication_mode: IdListPublicationMode,
        sources: BaseSources,
    ) -> Result<IdListDownloadBatch<'a>, StatsigErr> {
        let can_download_snapshots = sources.snapshots && self.transport.can_download_snapshots();
        let mut update_batch = IdListUpdateBatch::new(
            curr_manifest,
            &new_manifest,
            publication_mode,
            sources.snapshots || sources.cache,
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
            let Some(range_start) = id_list_range_start(current, &metadata) else {
                update_batch.keep(name, metadata);
                continue;
            };
            match self
                .transport
                .get_override_id_list_download_url(&metadata.url)
            {
                Ok(primary_url) => jobs.push(IdListDownloadJob {
                    name,
                    primary_url,
                    metadata,
                    range_start,
                    can_download_snapshots,
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
            use_base_cache: sources.cache,
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
        self.transport
            .network
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
                        .any(|job| self.transport.file_can_fallback(job));
                    if outcome == PrimaryOutcome::Exhausted && has_fallback && !eligible {
                        self.transport.network.log_fallback("id_list_file", false);
                    }
                    eligible && has_fallback
                },
                || {
                    StatsigErr::NetworkError(NetworkError::ShutdownError(
                        self.transport.id_lists_manifest_url.clone(),
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
        let (jobs, cache) = {
            let mut batch = batch.lock();
            let cache = self
                .initial_base_cache
                .as_ref()
                .filter(|_| !is_fallback && batch.use_base_cache);
            (std::mem::take(&mut batch.pending), cache)
        };
        let mut downloads = stream::iter(
            jobs.into_iter()
                .map(|job| self.materialize_job(job, cache, is_fallback, build)),
        )
        .buffer_unordered(ID_LIST_DOWNLOAD_CONCURRENCY);
        let mut failure = None;
        while let Some(result) = downloads.next().await {
            let mut batch = batch.lock();
            match result {
                Ok((name, body)) => {
                    *batch.successful_downloads += u64::from(body.downloaded);
                    batch.update_batch.record(name, body.update, body.range);
                }
                Err((job, error)) => {
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

    async fn materialize_job(
        &self,
        job: IdListDownloadJob,
        cache: Option<&Arc<SharedInitialBaseCache>>,
        is_fallback: bool,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<(String, MaterializedIdList), (IdListDownloadJob, StatsigErr)> {
        let cache = cache.filter(|_| {
            job.range_start == 0
                && job.name == job.metadata.name
                && SharedInitialBaseCache::eligible(&job.metadata)
        });

        if let Some(cache) = cache {
            let target = job.metadata.clone();
            match self
                .run_cache_task(cache, None, move |cache| cache.lookup(&target))
                .await
            {
                Ok(Some(list)) => return Ok((job.name, MaterializedIdList::base(list, false))),
                Ok(None) => {}
                Err(error) => return Err((job, error)),
            }
        }

        let download = match self.transport.download_job(&job, is_fallback, build).await {
            Ok(download) => download,
            Err(error) => return Err((job, error)),
        };
        let Some(cache) = cache else {
            return Ok((job.name, download.prepare(job.metadata)));
        };
        let body = download.prepare(job.metadata.clone());
        match self
            .run_cache_task(cache, build, move |cache| body.offer(cache))
            .await
        {
            Ok(body) => Ok((job.name, body)),
            Err(error) => Err((job, error)),
        }
    }

    async fn run_cache_task<T: Send + 'static>(
        &self,
        cache: &Arc<SharedInitialBaseCache>,
        build: Option<&PrivateBuildAttempt>,
        task: impl FnOnce(&SharedInitialBaseCache) -> T + Send + 'static,
    ) -> Result<T, StatsigErr> {
        let cache = Arc::clone(cache);
        let permit = cache
            .permits
            .clone()
            .acquire_owned()
            .await
            .map_err(|_| publication_stopped())?;
        let build_permit = match build {
            Some(build) => Some(build.admit_worker().await),
            None => None,
        };
        let stopped = Arc::clone(self.transport.network.shutdown_flag());
        tokio::task::spawn_blocking(id_list_load_timing::with_current_timings(
            Phase::BuildWorkerWait,
            move || {
                let _permits = (permit, build_permit);
                if stopped.load(Ordering::SeqCst) {
                    return Err(publication_stopped());
                }
                Ok(id_list_load_timing::measure(Phase::Processing, || {
                    task(&cache)
                }))
            },
        ))
        .await
        .map_err(|e| StatsigErr::ThreadFailure(e.to_string()))?
    }

    async fn publish_id_list_updates(
        &self,
        listener: HttpIdListsListener,
        mut update_batch: IdListUpdateBatch,
        refresh_guard: Option<&Arc<OwnedMutexGuard<()>>>,
        manifest_guard: Option<LazyManifestPublication>,
        eager_downloads: Option<u64>,
    ) -> Result<(), StatsigErr> {
        let file_failure = update_batch.file_failure.take();
        if file_failure.is_some() {
            update_batch.mode = IdListPublicationMode::IncompleteRefresh;
        }
        let blocking_listener = listener.as_ref().requires_blocking_id_list_publication();
        let offload =
            blocking_listener || eager_downloads.is_some() || self.initial_base_cache.is_some();
        let stopped = self.transport.network.shutdown_flag();
        // Keep the elected listener (and its lease) through installation, even if
        // the refresh future is cancelled while a blocking publication is running.
        let publish = move |stopped: &AtomicBool| {
            id_list_load_timing::measure(Phase::ParsePublish, || {
                if stopped.load(Ordering::SeqCst) {
                    return Err(publication_stopped());
                }
                listener.publish(update_batch, eager_downloads)?;
                if let Some(LazyManifestPublication {
                    mut guard,
                    next: Some(next),
                }) = manifest_guard
                {
                    *guard = Some(next);
                }
                Ok(())
            })
        };
        if offload {
            // An opted-in hash commit runs off-thread but still participates in force_shutdown.
            let shutdown = (!blocking_listener).then(|| Arc::clone(&self.shutdown));
            let stopped = Arc::clone(stopped);
            let guard = refresh_guard.cloned();
            let policy = self.output_policy;
            tokio::task::spawn_blocking(id_list_load_timing::with_current_timings(
                Phase::PublicationWorkerWait,
                move || {
                    let _guard = guard;
                    let _scope = policy.enter();
                    let _handoff = shutdown.as_ref().map(|state| state.handoff.lock());
                    publish(&stopped)
                },
            ))
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
    ) -> Result<bool, StatsigErr> {
        let lazy = self.lazy_id_lists.as_ref().ok_or_else(|| {
            StatsigErr::UnstartedAdapter("ID-list manifest has not been fetched yet".to_string())
        })?;
        let mut attempted = false;
        loop {
            if let Some(build) = parallel {
                build.submitted.store(false, Ordering::Release);
            }
            let Some(load) = self.plan_lazy_load(lazy, name, parallel).await? else {
                return Ok(attempted);
            };

            attempted = true;
            let mut successful_downloads = 0;
            let target = load.entry.metadata.clone();
            let build = match &load.destination {
                LazyLoadDestination::Store(private) => Some(private.build),
                LazyLoadDestination::Listener(_) => None,
            };
            let update_batch = self
                .fetch_id_list_updates(
                    load.sources,
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
                LazyLoadOutcome::Complete => return Ok(true),
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
        let started = id_list_load_timing::start_phase();
        let manifest = lazy.manifest.read().await;
        id_list_load_timing::end_phase(Phase::AdapterLockWait, started);
        let manifest = manifest.as_ref().ok_or_else(|| {
            StatsigErr::UnstartedAdapter("ID-list manifest has not been fetched yet".to_string())
        })?;
        let entry = manifest.get(name).ok_or_else(|| {
            StatsigErr::CustomError(format!("ID list {name} is missing from the manifest"))
        })?;
        let listener = self.current_listener()?;
        let sources = self.base_sources(&listener);
        let (destination, installed_metadata) = match (listener, parallel) {
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
                let metadata = listener.as_ref().get_current_id_list_metadata();
                (LazyLoadDestination::Listener(listener), metadata)
            }
        };
        if self.lazy_list_ready(sources, installed_metadata.get(name), &entry.metadata) {
            return Ok(None);
        }
        Ok(Some(LazyIdListLoad {
            sources,
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
        let (base, list) = lazy
            .build_index(Arc::clone(&store), installed_list, update, build, self)
            .await?;

        let adapter = Arc::clone(self);
        let name = name.to_owned();
        Self::with_manifest_for_private_commit(&lazy.manifest, move |manifest| {
            let _output_scope = adapter.output_policy.enter();
            if !adapter.is_current_lazy_target(manifest, &name, &target, store.as_ref())? {
                return Ok(LazyLoadOutcome::Retry);
            }
            // force_shutdown waits for an in-progress hash handoff.
            let _handoff = (!store.requires_blocking_id_list_publication())
                .then(|| adapter.shutdown.handoff.lock());
            adapter.ensure_running()?;
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
        listener: HttpIdListsListener,
        planned_metadata: &IdListsResponse,
        update_batch: IdListUpdateBatch,
    ) -> Result<LazyLoadOutcome, StatsigErr> {
        let started = id_list_load_timing::start_phase();
        let manifest = lazy.manifest.clone().write_owned().await;
        id_list_load_timing::end_phase(Phase::AdapterLockWait, started);
        if !self.is_current_lazy_target(manifest.as_ref(), name, target, listener.as_ref())? {
            return Ok(LazyLoadOutcome::Retry);
        }
        let installed = listener.as_ref().get_current_id_list_metadata();
        if self.lazy_list_ready(self.base_sources(&listener), installed.get(name), target) {
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
        sources: BaseSources,
        installed: Option<&IdListMetadata>,
        target: &IdListMetadata,
    ) -> bool {
        let Some(update) = target
            .file_version()
            .update_from(installed.map(IdListMetadata::file_version))
        else {
            return true;
        };
        update.start > 0
            && ((sources.cache && SharedInitialBaseCache::eligible(target))
                || (sources.snapshots && self.transport.can_download_snapshots()))
    }

    fn is_current_lazy_target(
        &self,
        manifest: Option<&IdListManifest>,
        name: &str,
        target: &IdListMetadata,
        listener: &dyn IdListsUpdateListener,
    ) -> Result<bool, StatsigErr> {
        let latest = manifest
            .and_then(|entries| entries.get(name))
            .ok_or_else(|| {
                StatsigErr::CustomError(format!("ID list {name} is missing from the manifest"))
            })?;
        Ok(self.is_current_listener(listener)
            && target.file_version() == latest.metadata.file_version())
    }

    async fn with_manifest_for_private_commit(
        manifest: &Arc<AsyncRwLock<Option<IdListManifest>>>,
        mut commit: impl FnOnce(Option<&IdListManifest>) -> Result<LazyLoadOutcome, StatsigErr>
        + Send
        + 'static,
    ) -> Result<LazyLoadOutcome, StatsigErr> {
        loop {
            let lock = Arc::clone(manifest);
            // Take the guard only once the worker is running. If a poll owns it,
            // leave the blocking thread free for the poll's own publication.
            let attempt = tokio::task::spawn_blocking(id_list_load_timing::with_current_timings(
                Phase::PublicationWorkerWait,
                move || {
                    let guard =
                        id_list_load_timing::measure(Phase::AdapterLockWait, || lock.try_read());
                    match guard {
                        Ok(guard) => ControlFlow::Break(id_list_load_timing::measure(
                            Phase::ParsePublish,
                            || commit(guard.as_ref()),
                        )),
                        Err(_) => ControlFlow::Continue(commit),
                    }
                },
            ))
            .await
            .map_err(|e| StatsigErr::ThreadFailure(e.to_string()))?;
            match attempt {
                ControlFlow::Break(result) => return result,
                ControlFlow::Continue(pending) => commit = pending,
            }
            let started = id_list_load_timing::start_phase();
            drop(manifest.read().await);
            id_list_load_timing::end_phase(Phase::AdapterLockWait, started);
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

                self.while_running(shared.result.get_or_init(|| {
                    id_list_load_timing::time_list_load(
                        &self.ops_stats,
                        name,
                        self.load_timings_enabled,
                        self.load_and_publish_id_list(waiter.name, parallel),
                    )
                }))
                .await?
                .clone()
            })
            .await
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
    primary_url: String,
    metadata: IdListMetadata,
    range_start: u64,
    can_download_snapshots: bool,
}

enum DownloadedIdList {
    Raw {
        changeset: String,
        range: Range<u64>,
    },
    Snapshot(IdList),
}

impl DownloadedIdList {
    fn prepare(self, metadata: IdListMetadata) -> MaterializedIdList {
        match self {
            Self::Raw { changeset, range } => MaterializedIdList {
                update: PreparedIdListUpdate::Raw(IdListUpdate {
                    raw_changeset: Some(changeset),
                    new_metadata: metadata,
                }),
                range,
                downloaded: true,
            },
            Self::Snapshot(list) => MaterializedIdList::base(list, true),
        }
    }
}

struct MaterializedIdList {
    update: PreparedIdListUpdate,
    range: Range<u64>,
    downloaded: bool,
}

impl MaterializedIdList {
    fn base(list: IdList, downloaded: bool) -> Self {
        Self {
            range: 0..list.metadata.size,
            update: PreparedIdListUpdate::Base(list),
            downloaded,
        }
    }

    fn offer(self, cache: &SharedInitialBaseCache) -> Self {
        if let PreparedIdListUpdate::Raw(raw) = &self.update {
            if self.range.end > raw.new_metadata.size
                || !raw
                    .raw_changeset
                    .as_deref()
                    .is_some_and(super::id_list::is_complete_record_prefix)
            {
                return self;
            }
        }
        let list = IdList::build(None, self.update, UpdateMode::Private(cache.encoding));
        Self::base(cache.offer(list), self.downloaded)
    }
}

struct IdListDownloadBatch<'a> {
    use_base_cache: bool,
    pending: Vec<IdListDownloadJob>,
    update_batch: IdListUpdateBatch,
    successful_downloads: &'a mut u64,
}

impl IdListDownloadBatch<'_> {
    fn retain_failed_lists(&mut self, installed: &IdListsResponse, error: StatsigErr) {
        // Failed warm downloads retain their installed generation and byte offset.
        for job in self.pending.drain(..) {
            let current = installed.get(&job.name);
            self.update_batch.retain_failed_list(job.name, current);
        }
        self.update_batch.file_failure.get_or_insert(error);
    }
}

struct LazyManifestPublication {
    guard: OwnedRwLockWriteGuard<Option<IdListManifest>>,
    next: Option<IdListManifest>,
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
        let started = id_list_load_timing::start_phase();
        let permit = Arc::clone(&self.permits)
            .acquire_owned()
            .await
            .expect("index build semaphore is never closed");
        id_list_load_timing::end_phase(Phase::BuildPermitWait, started);
        self.submitted.store(true, Ordering::Release);
        permit
    }
}

struct LazyIdListLoad<'a> {
    sources: BaseSources,
    entry: IdListManifestEntry,
    installed_metadata: IdListsResponse,
    destination: LazyLoadDestination<'a>,
}

enum LazyLoadDestination<'a> {
    Store(PrivateIdListLoad<'a>),
    Listener(HttpIdListsListener),
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
    manifest: Arc<AsyncRwLock<Option<IdListManifest>>>,
    build_permits: Option<Arc<Semaphore>>,
    #[cfg(test)]
    before_build: Option<Arc<BeforeIndexBuild>>,
}

impl LazyIdLists {
    async fn build_index(
        &self,
        store: Arc<SpecStore>,
        base: Option<IdList>,
        update: PreparedIdListUpdate,
        build: &PrivateBuildAttempt,
        adapter: &StatsigHttpIdListsAdapter,
    ) -> Result<(Option<IdList>, IdList), StatsigErr> {
        // A full snapshot already completed its index work in the validator.
        if matches!(update, PreparedIdListUpdate::Base(_)) {
            let list = store.updated_id_list(base.as_ref(), update);
            return Ok((base, list));
        }
        let permit = build.admit_worker().await;
        let output_policy = adapter.output_policy;
        let stopped = Arc::clone(adapter.transport.network.shutdown_flag());
        #[cfg(test)]
        let before_build = self.before_build.clone();
        tokio::task::spawn_blocking(id_list_load_timing::with_current_timings(
            Phase::BuildWorkerWait,
            move || {
                let _output_scope = output_policy.enter();
                let _permit = permit;
                if stopped.load(Ordering::SeqCst) {
                    return Err(publication_stopped());
                }
                #[cfg(test)]
                if let Some(before_build) = before_build {
                    before_build(&update.metadata().name);
                }
                let list = id_list_load_timing::measure(Phase::ParsePublish, || {
                    id_list_load_timing::measure(Phase::Processing, || {
                        store.updated_id_list(base.as_ref(), update)
                    })
                });
                Ok((base, list))
            },
        ))
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
                    if let Some(cache) = &self.initial_base_cache {
                        cache.drain().await;
                    }
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
                let stopped = self.transport.network.shutdown_flag().clone();
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
#[path = "__tests__/state_read_retry_tests.rs"]
mod state_read_retry_tests;

#[cfg(all(test, not(feature = "custom_network_provider")))]
#[path = "__tests__/snapshot_http_tests.rs"]
mod snapshot_http_tests;
