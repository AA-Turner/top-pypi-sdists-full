use super::shared_id_list_store::{ManifestRead, RefreshStatus};
use super::statsig_http_id_lists_adapter::RefreshTrigger;
use super::{
    IdList, IdListMetadata, IdListPropagationUpdate, IdListUpdate, IdListsAdapter,
    IdListsUpdateListener, SharedIdListCatalog, SharedIdListLease, SharedIdListStore,
    StatsigHttpIdListsAdapter,
};
use crate::networking::normalize_default_cdn_id_lists_manifest_url;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::{StatsigErr, StatsigOptions, StatsigRuntime};
use async_trait::async_trait;
use chrono::Utc;
use parking_lot::{Mutex, RwLock};
use std::collections::HashMap;
use std::ops::{Deref, DerefMut};
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Weak};
use std::time::{Duration, Instant};
use tokio::sync::{Mutex as AsyncMutex, MutexGuard, watch};

const DEFAULT_SYNC_MS: u32 = 60_000;
const DEFAULT_INITIAL_WAIT_MS: u64 = 30_000;
const FOLLOWER_POLL: Duration = Duration::from_secs(1);
const METRICS_INTERVAL: Duration = Duration::from_secs(30);

/// Opt-in, process-coordinated ID lists. One SDK publishes and every SDK maps the
/// committed catalog. SDK construction and background work remain post-fork.
pub(crate) struct StatsigSharedIdListsAdapter {
    sdk_key: String,
    options: StatsigOptions,
    partial_refresh: bool,
    store: Option<Arc<SharedIdListStore>>,
    state: AsyncMutex<ControllerState>,
    storage_work: Arc<AsyncMutex<()>>,
    active_http: RwLock<Option<Weak<StatsigHttpIdListsAdapter>>>,
    shutdown: watch::Sender<bool>,
    background_started: AtomicBool,
    sync_interval: Duration,
    poll_interval: Duration,
    initial_wait: Duration,
    stale_after: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    output_policy: crate::output_policy::OutputPolicy,
}

struct ControllerState {
    listener: Option<Arc<dyn IdListsUpdateListener>>,
    role: Role,
    installed_digest: Arc<Mutex<Option<[u8; 32]>>>,
    installed_manifest: Option<Arc<same_file::Handle>>,
    status: RefreshStatus,
    waiting_since: Instant,
    next_sync: Instant,
    next_metrics: Instant,
}

enum PollResult {
    Follower(ManifestRead),
    Elected {
        lease: SharedIdListLease,
        recovered: SharedIdListCatalog,
        cleanup_failed: bool,
    },
}

enum TickResult {
    Ready,
    Waiting,
    Fallback(&'static str),
}

enum Role {
    Follower,
    Leader {
        http: Arc<StatsigHttpIdListsAdapter>,
        publisher: Arc<PublishingListener>,
    },
    HttpFallback(Arc<StatsigHttpIdListsAdapter>),
}

impl Role {
    fn name(&self) -> &'static str {
        match self {
            Self::Follower => "follower",
            Self::Leader { .. } => "leader",
            Self::HttpFallback(_) => "http_fallback",
        }
    }
}

// Cancellation may drop a tick while it is waiting on HTTP. Keep lease cleanup
// in an RAII guard as well as the normal return path, including runtime shutdown.
struct ActiveCycle<'a> {
    state: MutexGuard<'a, ControllerState>,
    shutdown: &'a watch::Sender<bool>,
}

impl Deref for ActiveCycle<'_> {
    type Target = ControllerState;
    fn deref(&self) -> &Self::Target {
        &self.state
    }
}

impl DerefMut for ActiveCycle<'_> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.state
    }
}

impl Drop for ActiveCycle<'_> {
    fn drop(&mut self) {
        if *self.shutdown.borrow() {
            self.state.role = Role::Follower;
            self.state.listener = None;
        }
    }
}

impl StatsigSharedIdListsAdapter {
    #[must_use]
    pub(crate) fn new(sdk_key: &str, options: &StatsigOptions) -> Self {
        let sync_interval = Duration::from_millis(u64::from(
            options.id_lists_sync_interval_ms.unwrap_or(DEFAULT_SYNC_MS),
        ));
        // Telemetry identities deliberately do not change the sharing group.
        let source = serde_json::to_string(&(
            normalize_default_cdn_id_lists_manifest_url(options.id_lists_url.as_deref()),
            options
                .download_id_list_file_api
                .as_deref()
                .map(|value| value.trim_end_matches('/')),
            options.fallback_to_statsig_api.unwrap_or(false),
            sync_interval.as_millis(),
        ))
        .expect("ID-list source options serialize");
        // Old readers interpret a recent success timestamp as a complete catalog.
        // Separate the writer lease as well as the manifest during a mixed rollout.
        let partial_refresh = StatsigHttpIdListsAdapter::partial_refresh_enabled(options);
        let source = if partial_refresh {
            format!("partial-v1:{source}")
        } else {
            source
        };
        let store = options
            .shared_id_lists_dir
            .as_deref()
            .and_then(|directory| {
                SharedIdListStore::new(
                    Path::new(directory),
                    sdk_key,
                    &source,
                    options.enable_id_list_elias_fano.unwrap_or(false),
                )
                .ok()
                .map(Arc::new)
            });
        let now = Instant::now();
        Self {
            sdk_key: sdk_key.to_owned(),
            options: options.clone(),
            partial_refresh,
            store,
            storage_work: Arc::new(AsyncMutex::new(())),
            state: AsyncMutex::new(ControllerState {
                listener: None,
                role: Role::Follower,
                installed_digest: Arc::default(),
                installed_manifest: None,
                status: RefreshStatus::default(),
                waiting_since: now,
                next_sync: now,
                next_metrics: now,
            }),
            active_http: RwLock::new(None),
            shutdown: watch::channel(false).0,
            background_started: AtomicBool::new(false),
            sync_interval,
            poll_interval: FOLLOWER_POLL.min(sync_interval),
            initial_wait: Duration::from_millis(
                options.init_timeout_ms.unwrap_or(DEFAULT_INITIAL_WAIT_MS),
            ),
            // Faster polling must not shorten the default recovery window.
            stale_after: sync_interval
                .max(Duration::from_millis(u64::from(DEFAULT_SYNC_MS)))
                .saturating_mul(3),
            ops_stats: OPS_STATS
                .get_for_instance_with_options(options.get_sdk_instance_id(sdk_key), Some(options)),
            output_policy: crate::output_policy::OutputPolicy::from_options(Some(options)),
        }
    }

    // Background polling can be the first refresh if initialization timed out in specs.
    pub(crate) fn with_listener(mut self, listener: Arc<dyn IdListsUpdateListener>) -> Self {
        self.state.get_mut().listener = Some(listener);
        self
    }

    fn is_stale(&self, last_success: u64) -> bool {
        now_ms().saturating_sub(last_success) > self.stale_after.as_millis() as u64
    }

    fn catalog_expired(&self, status: RefreshStatus) -> bool {
        match (status.successful_refresh_ms, status.incomplete_since_ms) {
            (0, Some(first_partial)) => {
                now_ms().saturating_sub(first_partial) >= self.initial_wait.as_millis() as u64
            }
            (last_success, _) => self.is_stale(last_success),
        }
    }

    #[cfg(test)]
    pub(super) async fn poll_for_test(&self) -> Result<bool, StatsigErr> {
        self.state.lock().await.next_sync = Instant::now();
        self.tick(RefreshTrigger::Background).await
    }

    #[cfg(test)]
    pub(super) fn store_for_test(&self) -> Arc<SharedIdListStore> {
        self.store.as_ref().expect("test shared store").clone()
    }

    #[cfg(test)]
    pub(super) fn stopped_for_test(&self) -> bool {
        *self.shutdown.borrow()
    }

    #[cfg(test)]
    pub(super) async fn pause_ticks_for_test(&self) -> impl Drop + '_ {
        self.state.lock().await
    }

    #[cfg(test)]
    pub(super) async fn role_for_test(&self) -> &'static str {
        self.state.lock().await.role.name()
    }

    pub(crate) fn force_shutdown(&self) {
        self.stop(StatsigHttpIdListsAdapter::force_shutdown);
    }

    fn stop(&self, stop_http: impl FnOnce(&StatsigHttpIdListsAdapter)) {
        self.shutdown.send_replace(true);
        let http = self.active_http.read().as_ref().and_then(Weak::upgrade);
        if let Some(http) = http {
            stop_http(&http);
        }
        if let Ok(mut state) = self.state.try_lock() {
            state.role = Role::Follower;
            state.listener = None;
        }
    }

    async fn cancelled(&self) {
        let mut receiver = self.shutdown.subscribe();
        let _ = receiver.wait_for(|stopped| *stopped).await;
    }

    fn stopped_error() -> StatsigErr {
        StatsigErr::ShutdownFailure("Shared ID-list adapter stopped".to_string())
    }

    fn http(&self) -> Result<Arc<StatsigHttpIdListsAdapter>, StatsigErr> {
        let mut http = StatsigHttpIdListsAdapter::with_partial_refresh(
            &self.sdk_key,
            &self.options,
            self.partial_refresh,
        );
        http.refresh_gate = self.storage_work.clone();
        let http = Arc::new(http);
        // stop() signals first, then reads active_http. Either it sees this adapter,
        // or registration observes that the controller has already stopped.
        *self.active_http.write() = Some(Arc::downgrade(&http));
        if *self.shutdown.borrow() {
            return Err(Self::stopped_error());
        }
        Ok(http)
    }

    fn metric(
        &self,
        kind: MetricType,
        name: &str,
        value: f64,
        tags: Option<HashMap<String, String>>,
    ) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            kind,
            name.to_string(),
            value,
            tags,
        ));
    }

    fn failure(&self, reason: &'static str) {
        self.metric(
            MetricType::Increment,
            "shared_id_lists.failure",
            1.0,
            Some(HashMap::from([("reason".to_string(), reason.to_string())])),
        );
    }

    fn sample(&self, state: &mut ControllerState) {
        if Instant::now() < state.next_metrics {
            return;
        }
        state.next_metrics = Instant::now() + METRICS_INTERVAL;
        for role in ["leader", "follower", "http_fallback"] {
            self.metric(
                MetricType::Gauge,
                "shared_id_lists.role",
                f64::from(state.role.name() == role),
                Some(HashMap::from([("role".to_string(), role.to_string())])),
            );
        }
        if state.status.successful_refresh_ms != 0 {
            self.metric(
                MetricType::Gauge,
                "shared_id_lists.refresh_age_ms",
                now_ms().saturating_sub(state.status.successful_refresh_ms) as f64,
                None,
            );
        }
    }

    /// Returns false if the listener rejects an expired catalog. The caller must
    /// release any lease and resume HTTP from the listener's installed cursor.
    async fn try_install(
        &self,
        state: &mut ControllerState,
        catalog: SharedIdListCatalog,
    ) -> Result<bool, StatsigErr> {
        if *state.installed_digest.lock() != Some(catalog.content_digest) {
            let started = Instant::now();
            let listener = state.listener.clone().ok_or_else(|| {
                StatsigErr::UnstartedAdapter("Shared ID-list listener missing".to_string())
            })?;
            let guard = self.storage_work.clone().lock_owned().await;
            let policy = self.output_policy;
            let installed_digest = state.installed_digest.clone();
            let result = tokio::task::spawn_blocking(move || {
                let _guard = guard;
                let _scope = policy.enter();
                listener.did_receive_id_list_snapshot(catalog.lists, catalog.propagation)?;
                // A cancelled tick can leave this install running. Record what the
                // listener accepted before another tick can acquire storage_work.
                *installed_digest.lock() = Some(catalog.content_digest);
                Ok(())
            })
            .await
            .unwrap_or_else(|error| Err(StatsigErr::FileError(error.to_string())));
            if result.is_err() && self.catalog_expired(catalog.status) {
                return Ok(false);
            }
            result?;
            self.metric(
                MetricType::Dist,
                "shared_id_lists.install.latency_ms",
                started.elapsed().as_secs_f64() * 1000.0,
                None,
            );
        }
        state.status = catalog.status;
        Ok(true)
    }

    async fn fallback(
        &self,
        state: &mut ControllerState,
        reason: &'static str,
        trigger: RefreshTrigger,
    ) -> Result<bool, StatsigErr> {
        self.failure(reason);
        if let Role::Leader { http, .. } = &state.role {
            http.force_shutdown();
        }
        // tick_locked has returned, so replacing the role drops the last leader
        // references before the private request starts.
        state.role = Role::Follower;
        let http = self.http()?;
        state.role = Role::HttpFallback(http.clone());
        state.next_metrics = Instant::now();
        state.next_sync = Instant::now() + self.sync_interval;
        let listener = state.listener.clone().ok_or_else(|| {
            StatsigErr::UnstartedAdapter("Shared ID-list listener missing".to_string())
        })?;
        // The existing store is the baseline, including complete mapped sets and
        // their byte cursors; private recovery continues from what was installed.
        http.set_listener(listener);
        http.refresh(trigger).await?;
        Ok(true)
    }

    async fn tick(&self, trigger: RefreshTrigger) -> Result<bool, StatsigErr> {
        let mut state = ActiveCycle {
            state: self.state.lock().await,
            shutdown: &self.shutdown,
        };
        if *self.shutdown.borrow() {
            return Err(Self::stopped_error());
        }
        // Only the current cycle may consume an explicit initialize refresh.
        if trigger == RefreshTrigger::SharedInitialize {
            state.next_sync = Instant::now();
        }
        let result = tokio::select! {
            biased;
            () = self.cancelled() => Err(Self::stopped_error()),
            result = async {
                match self.tick_locked(&mut state, trigger).await? {
                    TickResult::Ready => Ok(true),
                    TickResult::Waiting => Ok(false),
                    TickResult::Fallback(reason) => self.fallback(&mut state, reason, trigger).await,
                }
            } => result,
        };
        self.sample(&mut state);
        result
    }

    async fn tick_locked(
        &self,
        state: &mut ControllerState,
        trigger: RefreshTrigger,
    ) -> Result<TickResult, StatsigErr> {
        // A cancelled refresh can leave a blocking publication finishing. Await
        // its committed cursor before another HTTP request is allowed to start.
        drop(self.storage_work.lock().await);
        let listener = state.listener.clone().ok_or_else(|| {
            StatsigErr::UnstartedAdapter("Shared ID-list listener missing".to_string())
        })?;
        match &state.role {
            Role::HttpFallback(http) => {
                if Instant::now() >= state.next_sync {
                    state.next_sync = Instant::now() + self.sync_interval;
                    http.refresh(trigger).await?;
                }
                return Ok(TickResult::Ready);
            }
            Role::Leader { http, publisher } => {
                let http = http.clone();
                let publisher = publisher.clone();
                let status = publisher.committed_status().unwrap_or_default();
                if status.has_history() {
                    // A cancelled or rejected install may leave the disk ahead of the owner.
                    if publisher.install_pending.load(Ordering::Acquire) {
                        if !self.try_install(state, publisher.snapshot()).await? {
                            return Ok(TickResult::Fallback("stale"));
                        }
                        publisher.install_pending.store(false, Ordering::Release);
                    }
                    state.status = status;
                    if self.catalog_expired(status) {
                        return Ok(TickResult::Fallback("stale"));
                    }
                } else if state.waiting_since.elapsed() >= self.initial_wait {
                    return Ok(TickResult::Fallback("initial_timeout"));
                }
                if Instant::now() >= state.next_sync {
                    return self
                        .refresh_leader(state, &http, &publisher, trigger, false)
                        .await;
                }
                return status.readiness();
            }
            Role::Follower => {}
        }
        if !listener.supports_id_list_snapshots() {
            return Ok(TickResult::Fallback("unsupported_listener"));
        }
        let Some(store) = &self.store else {
            return Ok(TickResult::Fallback("storage_unavailable"));
        };
        let reader = store.clone();
        let installed = state.installed_manifest.clone();
        let installed_digest = state.installed_digest.clone();
        // Check election first. A successor must always recover the current
        // catalog under its lease, irrespective of the last follower poll.
        let guard = self.storage_work.clone().lock_owned().await;
        let poll = tokio::task::spawn_blocking(move || {
            let _guard = guard;
            let lease = reader.try_acquire_lease().map_err(|_| "lease")?;
            let poll = match lease {
                Some(lease) => {
                    let recovered = reader.load().map_err(|_| "recovery")?.unwrap_or_default();
                    let cleanup_failed = reader.cleanup(&lease).is_err();
                    PollResult::Elected {
                        lease,
                        recovered,
                        cleanup_failed,
                    }
                }
                None => PollResult::Follower(
                    reader
                        .load_if_changed(installed.as_deref(), || {})
                        .map_err(|_| "read")?,
                ),
            };
            if let PollResult::Elected {
                recovered: catalog, ..
            }
            | PollResult::Follower(ManifestRead::Changed(_, catalog)) = &poll
            {
                // Reading a different catalog replaces the store's weak mapping cache,
                // even if this tick is cancelled or the listener rejects the install.
                // Reinstall a restored catalog once so its mappings stay pinned.
                installed_digest
                    .lock()
                    .take_if(|digest| *digest != catalog.content_digest);
            }
            Ok(poll)
        })
        .await
        .unwrap_or(Err("storage_worker"));
        let poll = match poll {
            Ok(poll) => poll,
            Err("read")
                if state.status.successful_refresh_ms != 0
                    && !self.is_stale(state.status.successful_refresh_ms) =>
            {
                self.failure("read");
                return state.status.readiness();
            }
            Err(reason) => return Ok(TickResult::Fallback(reason)),
        };
        let catalog = match poll {
            PollResult::Follower(catalog) => catalog,
            PollResult::Elected {
                lease,
                recovered,
                cleanup_failed,
            } => {
                state.installed_manifest = None;
                if cleanup_failed {
                    self.failure("cleanup");
                }
                let recover = recovered.status.incomplete_since_ms.is_some()
                    || (recovered.status.successful_refresh_ms != 0
                        && !self.is_stale(recovered.status.successful_refresh_ms));
                if recover && !self.try_install(state, recovered.clone()).await? {
                    return Ok(TickResult::Fallback("stale"));
                }
                let publisher = Arc::new(PublishingListener {
                    store: store.clone(),
                    lease,
                    current: Mutex::new(recovered),
                    installed_digest: state.installed_digest.clone(),
                    listener,
                    storage_failed: AtomicBool::new(false),
                    install_pending: AtomicBool::new(false),
                    ops_stats: self.ops_stats.clone(),
                });
                let http = self.http()?;
                state.role = Role::Leader {
                    http: http.clone(),
                    publisher: publisher.clone(),
                };
                state.next_metrics = Instant::now();
                self.metric(
                    MetricType::Increment,
                    "shared_id_lists.leadership.acquired",
                    1.0,
                    None,
                );
                http.set_listener(publisher.clone());
                return self
                    .refresh_leader(state, &http, &publisher, trigger, true)
                    .await;
            }
        };
        let status = match &catalog {
            ManifestRead::Changed(_, catalog) => catalog.status,
            ManifestRead::Unchanged => state.status,
            ManifestRead::Missing => {
                if state.waiting_since.elapsed() >= self.initial_wait {
                    return Ok(TickResult::Fallback("initial_timeout"));
                }
                return Ok(TickResult::Waiting);
            }
        };
        let expired = self.catalog_expired(status);
        if !expired || status.incomplete_since_ms.is_some() {
            if let ManifestRead::Changed(handle, catalog) = catalog {
                if !self.try_install(state, catalog).await? {
                    return Ok(TickResult::Fallback("stale"));
                }
                state.installed_manifest = Some(Arc::new(handle));
            }
        }
        if expired {
            return Ok(TickResult::Fallback("stale"));
        }
        status.readiness()
    }

    async fn refresh_leader(
        &self,
        state: &mut ControllerState,
        http: &StatsigHttpIdListsAdapter,
        publisher: &PublishingListener,
        trigger: RefreshTrigger,
        elected: bool,
    ) -> Result<TickResult, StatsigErr> {
        let result = http.refresh(trigger).await;
        state.next_sync = Instant::now() + self.sync_interval;
        if publisher.take_storage_failure() {
            return Ok(TickResult::Fallback("publish"));
        }
        if publisher.install_pending.load(Ordering::Acquire) {
            // The disk cursor is ahead of the owner. Reconcile it on the next
            // tick before a private fallback can use the owner's older cursor.
            return result.map(|()| TickResult::Ready);
        }
        if let Some(status) = publisher.committed_status() {
            state.status = status;
        }
        if let Err(error) = result {
            self.failure("http_refresh");
            if (!elected || state.status.has_history()) && self.catalog_expired(state.status) {
                return Ok(TickResult::Fallback("stale"));
            }
            return Err(error);
        }
        Ok(TickResult::Ready)
    }
}

impl RefreshStatus {
    fn has_history(self) -> bool {
        self.successful_refresh_ms != 0 || self.incomplete_since_ms.is_some()
    }

    fn readiness(self) -> Result<TickResult, StatsigErr> {
        if self.incomplete_since_ms.is_some() {
            Err(StatsigErr::CustomError(
                "Shared ID-list refresh is incomplete".into(),
            ))
        } else if self.successful_refresh_ms != 0 {
            Ok(TickResult::Ready)
        } else {
            Ok(TickResult::Waiting)
        }
    }
}

#[async_trait]
impl IdListsAdapter for StatsigSharedIdListsAdapter {
    async fn start(
        self: Arc<Self>,
        _runtime: &Arc<StatsigRuntime>,
        listener: Arc<dyn IdListsUpdateListener + Send + Sync>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                {
                    let mut state = self.state.lock().await;
                    if *self.shutdown.borrow() {
                        return Err(Self::stopped_error());
                    }
                    // An initialize retry may arrive after background polling elected a
                    // publisher or entered permanent private fallback for this SDK.
                    state.listener.get_or_insert(listener);
                    state.waiting_since = Instant::now();
                }
                loop {
                    if self.tick(RefreshTrigger::SharedInitialize).await? {
                        return Ok(());
                    }
                    tokio::select! {
                        biased;
                        () = self.cancelled() => return Err(Self::stopped_error()),
                        () = tokio::time::sleep(self.poll_interval) => {},
                    }
                }
            })
            .await
    }

    async fn shutdown(&self, timeout: Duration) -> Result<(), StatsigErr> {
        self.stop(StatsigHttpIdListsAdapter::signal_shutdown);
        tokio::time::timeout(timeout, async {
            let mut state = self.state.lock().await;
            let _storage = self.storage_work.lock().await;
            state.role = Role::Follower;
            state.listener = None;
        })
        .await
        .map_err(|_| StatsigErr::ShutdownFailure("Shared ID-list refresh is stopping".to_string()))
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        if self.background_started.swap(true, Ordering::AcqRel) {
            return Ok(());
        }
        let weak = Arc::downgrade(&self);
        let mut shutdown = self.shutdown.subscribe();
        let poll_interval = self.poll_interval;
        let result = runtime.spawn(
            "shared_id_list_bg_sync",
            move |runtime_shutdown| async move {
                loop {
                    tokio::select! {
                        biased;
                        _ = shutdown.wait_for(|stopped| *stopped) => break,
                        () = runtime_shutdown.notified() => {
                            if let Some(adapter) = weak.upgrade() { adapter.force_shutdown(); }
                            break;
                        }
                        () = async {
                            tokio::time::sleep(poll_interval).await;
                            if let Some(adapter) = weak.upgrade() {
                                let _ = adapter.output_policy.scope(adapter.tick(RefreshTrigger::Background)).await;
                            }
                        } => {},
                    }
                    if weak.strong_count() == 0 {
                        break;
                    }
                }
            },
        );
        if result.is_err() {
            self.background_started.store(false, Ordering::Release);
        }
        result.map(|_| ())
    }

    fn get_type_name(&self) -> String {
        "StatsigSharedIdListsAdapter".to_string()
    }
}

struct PublishingListener {
    store: Arc<SharedIdListStore>,
    lease: SharedIdListLease,
    current: Mutex<SharedIdListCatalog>,
    installed_digest: Arc<Mutex<Option<[u8; 32]>>>,
    listener: Arc<dyn IdListsUpdateListener>,
    storage_failed: AtomicBool,
    install_pending: AtomicBool,
    ops_stats: Arc<OpsStatsForInstance>,
}

impl PublishingListener {
    fn snapshot(&self) -> SharedIdListCatalog {
        self.current.lock().clone()
    }

    fn committed_status(&self) -> Option<RefreshStatus> {
        let current = self.current.lock();
        (!current.generation.is_empty()).then_some(current.status)
    }
    fn take_storage_failure(&self) -> bool {
        self.storage_failed.swap(false, Ordering::AcqRel)
    }
}

impl IdListsUpdateListener for PublishingListener {
    fn requires_blocking_id_list_publication(&self) -> bool {
        true
    }

    fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata> {
        self.current
            .lock()
            .lists
            .iter()
            .map(|(name, list)| (name.clone(), list.metadata.clone()))
            .collect()
    }

    fn did_receive_id_list_updates(&self, updates: HashMap<String, IdListUpdate>) {
        // The elected controller always uses the fallible callback below.
        let _ = self.try_receive_id_list_updates_with_propagation(updates, HashMap::new());
    }

    fn try_receive_id_list_updates_with_propagation(
        &self,
        updates: HashMap<String, IdListUpdate>,
        propagation: HashMap<String, IdListPropagationUpdate>,
    ) -> Result<(), StatsigErr> {
        self.publish(updates, propagation, true)
    }

    fn try_receive_incomplete_id_list_refresh(
        &self,
        updates: HashMap<String, IdListUpdate>,
        propagation: HashMap<String, IdListPropagationUpdate>,
    ) -> Result<(), StatsigErr> {
        self.publish(updates, propagation, false)
    }
}

impl PublishingListener {
    fn publish(
        &self,
        updates: HashMap<String, IdListUpdate>,
        mut propagation: HashMap<String, IdListPropagationUpdate>,
        complete: bool,
    ) -> Result<(), StatsigErr> {
        let mut current = self.current.lock();
        let mut lists = HashMap::with_capacity(updates.len());
        for (name, update) in updates {
            if !complete && !propagation.contains_key(&name) {
                if let Some(previous) = current.propagation.get(&name) {
                    propagation.insert(name.clone(), previous.clone());
                }
            }
            let mut list = current
                .lists
                .get(&name)
                .cloned()
                .unwrap_or_else(|| IdList::new(update.new_metadata.clone()));
            list.apply_update_for_publish(update);
            lists.insert(name, list);
        }
        let propagation = cumulative_propagation(&current, &lists, propagation);
        let published = self
            .store
            .publish_with_clock(
                &self.lease,
                &lists,
                &propagation,
                (!complete).then_some(current.status),
                now_ms,
            )
            .map_err(|_| {
                self.storage_failed.store(true, Ordering::Release);
                StatsigErr::FileError("Shared ID-list publication failed".to_string())
            })?;
        // Disk commit is the cursor authority even if the owner's store closes
        // afterward. A successor reloads this exact materialized state.
        *current = published;
        if *self.installed_digest.lock() != Some(current.content_digest) {
            self.install_pending.store(true, Ordering::Release);
            self.listener
                .did_receive_id_list_snapshot(current.lists.clone(), current.propagation.clone())?;
            *self.installed_digest.lock() = Some(current.content_digest);
            self.install_pending.store(false, Ordering::Release);
        }
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            "shared_id_lists.publish".to_string(),
            1.0,
            Some(HashMap::from([(
                "result".to_string(),
                if complete { "success" } else { "incomplete" }.to_string(),
            )])),
        ));
        Ok(())
    }
}

fn cumulative_propagation(
    current: &SharedIdListCatalog,
    lists: &HashMap<String, IdList>,
    observations: HashMap<String, IdListPropagationUpdate>,
) -> HashMap<String, IdListPropagationUpdate> {
    observations
        .into_iter()
        .filter_map(|(name, mut observation)| {
            let list = lists.get(&name)?;
            // Keep the installed generation's proof when HTTP delivers an older manifest.
            if list.metadata.file_id != observation.file_id
                || list.metadata.creation_time != observation.creation_time
            {
                return current
                    .propagation
                    .get(&name)
                    .cloned()
                    .map(|previous| (name, previous));
            }
            let prior = current.propagation.get(&name).filter(|previous| {
                previous.file_id == observation.file_id
                    && previous.url == observation.url
                    && current.lists.get(&name).is_some_and(|old| {
                        old.metadata.creation_time == list.metadata.creation_time
                    })
            });
            let mut prefix = prior
                .and_then(|previous| previous.applied_range.as_ref())
                .filter(|range| range.start == 0)
                .map(|range| range.end);
            if let Some(range) = &observation.applied_range {
                if range.start <= prefix.unwrap_or(0) {
                    prefix = Some(prefix.unwrap_or(0).max(range.end));
                }
            }
            observation.applied_range = prefix.map(|end| 0..end);
            Some((name, observation))
        })
        .collect()
}

fn now_ms() -> u64 {
    Utc::now().timestamp_millis().max(0) as u64
}
