use std::collections::{BTreeMap, HashMap, HashSet};
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, OnceLock};
use std::time::{Duration, Instant};

use dashmap::DashMap;
use dashmap::mapref::entry::Entry;
use parking_lot::Mutex;
#[cfg(feature = "reqwest")]
use serde::{Deserialize, Serialize};
use tokio::sync::{OnceCell, Semaphore, watch};
use tokio::time::MissedTickBehavior;

#[cfg(feature = "reqwest")]
use crate::log_w;
use crate::{
    StatsigErr, StatsigRuntime,
    observability::{
        observability_client_adapter::{MetricType, ObservabilityEvent},
        ops_stats::OpsStatsForInstance,
    },
};

const REQUEST_TIMEOUT: Duration = Duration::from_millis(200);
const CACHE_FRESHNESS: Duration = Duration::from_secs(5 * 60);
const CACHE_TTL: Duration = Duration::from_secs(10 * 60);
const MAX_CACHE_ENTRIES: usize = 500_000;
const EVICTION_SHARD_COUNT: usize = 32;
const MAX_CACHE_ENTRIES_PER_SHARD: usize = MAX_CACHE_ENTRIES / EVICTION_SHARD_COUNT;
const EXPIRATION_SWEEP_INTERVAL: Duration = Duration::from_secs(30);
const MAX_EXPIRATION_SWEEP_BATCH: usize = 64;
const MAX_CONCURRENT_BACKGROUND_REFRESHES: usize = 16;
#[cfg(feature = "reqwest")]
const MAX_RESPONSE_BYTES: usize = 8 * 1024 * 1024;
const EXPIRATION_TASK: &str = "scoped_id_list_membership_expiration";
const REQUEST_METRIC: &str = "id_list_results.request.count";
#[cfg(feature = "reqwest")]
const FETCH_METRIC: &str = "id_list_results.fetch.count";
#[cfg(feature = "reqwest")]
const FETCH_LATENCY_METRIC: &str = "id_list_results.fetch.latency_ms";
#[cfg(feature = "reqwest")]
const TAG: &str = "ScopedIdListMembershipService";

#[derive(Clone, Copy)]
enum FetchSource {
    Foreground,
    BackgroundRefresh,
}

#[cfg(feature = "reqwest")]
impl FetchSource {
    fn tag_value(self) -> &'static str {
        match self {
            Self::Foreground => "foreground",
            Self::BackgroundRefresh => "background_refresh",
        }
    }
}

#[cfg(feature = "reqwest")]
#[derive(Clone, Copy)]
enum FetchFailure {
    RequestError,
    BadStatus,
    ResponseTooLarge,
    ResponseReadError,
    ParseError,
    Timeout,
}

#[cfg(feature = "reqwest")]
impl FetchFailure {
    fn outcome(self) -> &'static str {
        match self {
            Self::RequestError => "request_error",
            Self::BadStatus => "bad_status",
            Self::ResponseTooLarge => "response_too_large",
            Self::ResponseReadError => "response_read_error",
            Self::ParseError => "parse_error",
            Self::Timeout => "timeout",
        }
    }

    fn message(self) -> &'static str {
        match self {
            Self::RequestError => "ID-list membership request failed",
            Self::BadStatus => "ID-list membership server rejected the request",
            Self::ResponseTooLarge => "ID-list membership response exceeds its limit",
            Self::ResponseReadError => "ID-list membership response could not be read",
            Self::ParseError => "ID-list membership response was malformed",
            Self::Timeout => "ID-list membership request timed out",
        }
    }
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct CacheKey(Arc<CacheKeyData>);

#[derive(Debug, Eq, Hash, PartialEq)]
struct CacheKeyData {
    company_id: String,
    mapping: Vec<(String, String)>,
}

impl CacheKey {
    fn new(company_id: &str, mapping: &HashMap<String, String>) -> Self {
        let mut mapping = mapping
            .iter()
            .map(|(name, lookup)| (name.clone(), lookup.clone()))
            .collect::<Vec<_>>();
        mapping.sort_unstable();

        Self(Arc::new(CacheKeyData {
            company_id: company_id.to_string(),
            mapping,
        }))
    }
}

#[derive(Clone)]
struct CachedResults {
    results: Arc<HashSet<String>>,
    refreshed_at: Instant,
    generation: u64,
}

struct SharedFetch {
    result: OnceCell<Result<Arc<HashSet<String>>, StatsigErr>>,
    waiters: AtomicUsize,
}

struct InFlightWaiter {
    service: Arc<ScopedIdListMembershipService>,
    key: CacheKey,
    shared: Arc<SharedFetch>,
}

impl Drop for InFlightWaiter {
    fn drop(&mut self) {
        if self.shared.waiters.fetch_sub(1, Ordering::AcqRel) == 1 {
            self.service.in_flight.remove_if(&self.key, |_, active| {
                Arc::ptr_eq(active, &self.shared) && active.waiters.load(Ordering::Acquire) == 0
            });
        }
    }
}

struct RefreshMarker {
    service: Arc<ScopedIdListMembershipService>,
    key: CacheKey,
}

impl Drop for RefreshMarker {
    fn drop(&mut self) {
        self.service.refreshing.remove(&self.key);
    }
}

#[cfg(feature = "reqwest")]
#[derive(Serialize)]
struct MembershipRequest<'a> {
    #[serde(rename = "companyID")]
    company_id: &'a str,
    mapping: &'a HashMap<String, String>,
}

#[cfg(feature = "reqwest")]
#[derive(Deserialize)]
struct MembershipResponse {
    #[serde(default)]
    result: Vec<String>,
}

pub(crate) struct ScopedIdListMembershipService {
    server_url: String,
    #[cfg(feature = "reqwest")]
    http_client: reqwest::Client,
    entries: DashMap<CacheKey, CachedResults>,
    in_flight: DashMap<CacheKey, Arc<SharedFetch>>,
    refreshing: DashMap<CacheKey, ()>,
    refresh_permits: Arc<Semaphore>,
    eviction_order: [Mutex<BTreeMap<(Instant, u64), CacheKey>>; EVICTION_SHARD_COUNT],
    next_expiration_shard: AtomicUsize,
    next_generation: AtomicU64,
    runtime: Arc<StatsigRuntime>,
    ops_stats: Option<Arc<OpsStatsForInstance>>,
    shutting_down: AtomicBool,
    shutdown_signal: watch::Sender<bool>,
}

impl ScopedIdListMembershipService {
    pub(crate) fn new(
        server_url: String,
        runtime: Arc<StatsigRuntime>,
        ops_stats: Option<Arc<OpsStatsForInstance>>,
    ) -> Result<Arc<Self>, StatsigErr> {
        let server_url = server_url.trim().trim_end_matches('/').to_string();
        if server_url.is_empty()
            || !(server_url.starts_with("http://") || server_url.starts_with("https://"))
        {
            return Err(StatsigErr::InvalidOperation(
                "ID-list membership server URL must use HTTP or HTTPS".to_string(),
            ));
        }
        require_membership_http_support()?;

        #[cfg(feature = "reqwest")]
        let http_client = reqwest::Client::builder()
            .timeout(REQUEST_TIMEOUT)
            .connect_timeout(REQUEST_TIMEOUT)
            .build()
            .map_err(|_| {
                StatsigErr::InitializationError(
                    "Failed to initialize the ID-list membership HTTP client".to_string(),
                )
            })?;

        let (shutdown_signal, _) = watch::channel(false);
        let service = Arc::new(Self {
            server_url,
            #[cfg(feature = "reqwest")]
            http_client,
            entries: DashMap::new(),
            in_flight: DashMap::new(),
            refreshing: DashMap::new(),
            refresh_permits: Arc::new(Semaphore::new(MAX_CONCURRENT_BACKGROUND_REFRESHES)),
            eviction_order: std::array::from_fn(|_| Mutex::new(BTreeMap::new())),
            next_expiration_shard: AtomicUsize::new(0),
            next_generation: AtomicU64::new(0),
            runtime,
            ops_stats,
            shutting_down: AtomicBool::new(false),
            shutdown_signal,
        });
        service.start_expiration_task()?;
        Ok(service)
    }

    pub(crate) async fn resolve(
        self: &Arc<Self>,
        company_id: &str,
        mapping: HashMap<String, String>,
    ) -> Arc<HashSet<String>> {
        if mapping.is_empty() {
            self.record_request_result("empty_mapping");
            return empty_results();
        }
        if self.shutting_down.load(Ordering::Acquire) {
            self.record_request_result("shutdown");
            return empty_results();
        }

        let key = CacheKey::new(company_id, &mapping);
        if let Some(cached) = self.entries.get(&key).map(|entry| entry.clone()) {
            let elapsed = cached.refreshed_at.elapsed();
            if elapsed < CACHE_TTL {
                if elapsed >= CACHE_FRESHNESS {
                    self.refresh_in_background(
                        key,
                        company_id.to_string(),
                        mapping,
                        cached.generation,
                    );
                    self.record_request_result("stale_cache_hit");
                } else {
                    self.record_request_result("cache_hit");
                }
                return cached.results;
            }
            self.remove_if_generation(&key, cached.generation);
        }

        match self
            .fetch_foreground(key, company_id.to_string(), mapping)
            .await
        {
            Ok(results) => {
                self.record_request_result("cache_miss_success");
                results
            }
            Err(_) => {
                self.record_request_result("cache_miss_failure");
                empty_results()
            }
        }
    }

    pub(crate) fn shutdown(&self) {
        if !self.shutting_down.swap(true, Ordering::AcqRel) {
            self.shutdown_signal.send_replace(true);
        }
    }

    async fn fetch_foreground(
        self: &Arc<Self>,
        key: CacheKey,
        company_id: String,
        mapping: HashMap<String, String>,
    ) -> Result<Arc<HashSet<String>>, StatsigErr> {
        let shared = {
            let active = self.in_flight.entry(key.clone()).or_insert_with(|| {
                Arc::new(SharedFetch {
                    result: OnceCell::new(),
                    waiters: AtomicUsize::new(0),
                })
            });
            let shared = Arc::clone(active.value());
            shared.waiters.fetch_add(1, Ordering::AcqRel);
            shared
        };
        let _waiter = InFlightWaiter {
            service: Arc::clone(self),
            key: key.clone(),
            shared: Arc::clone(&shared),
        };

        shared
            .result
            .get_or_init(|| async {
                let result = self
                    .fetch(&company_id, &mapping, FetchSource::Foreground)
                    .await;
                if let Ok(results) = &result {
                    if !self.shutting_down.load(Ordering::Acquire) {
                        self.insert(key.clone(), None, Arc::clone(results));
                    }
                }
                result
            })
            .await
            .clone()
    }

    fn refresh_in_background(
        self: &Arc<Self>,
        key: CacheKey,
        company_id: String,
        mapping: HashMap<String, String>,
        generation: u64,
    ) {
        if self.shutting_down.load(Ordering::Acquire) {
            return;
        }
        match self.refreshing.entry(key.clone()) {
            Entry::Occupied(_) => return,
            Entry::Vacant(entry) => {
                entry.insert(());
            }
        }

        let marker = RefreshMarker {
            service: Arc::clone(self),
            key: key.clone(),
        };
        let Ok(permit) = Arc::clone(&self.refresh_permits).try_acquire_owned() else {
            return;
        };
        let Ok(runtime) = self.runtime.get_handle() else {
            return;
        };
        let service = Arc::clone(self);
        let mut shutdown = self.shutdown_signal.subscribe();
        runtime.spawn(async move {
            let _permit = permit;
            let _marker = marker;
            if *shutdown.borrow_and_update() {
                return;
            }
            tokio::select! {
                biased;
                _ = shutdown.changed() => {}
                result = service.fetch(&company_id, &mapping, FetchSource::BackgroundRefresh) => {
                    if let Ok(results) = result {
                        if !*shutdown.borrow() {
                            service.insert(key, Some(generation), results);
                        }
                    }
                }
            }
        });
    }

    #[cfg(feature = "reqwest")]
    async fn fetch(
        &self,
        company_id: &str,
        mapping: &HashMap<String, String>,
        source: FetchSource,
    ) -> Result<Arc<HashSet<String>>, StatsigErr> {
        let request = MembershipRequest {
            company_id,
            mapping,
        };
        let started = Instant::now();
        let mut status = None;
        let operation = async {
            let mut response = self
                .http_client
                .post(format!("{}/get_id_list_results", self.server_url))
                .json(&request)
                .send()
                .await
                .map_err(|_| FetchFailure::RequestError)?;

            status = Some(response.status().as_u16());
            if !response.status().is_success() {
                return Err(FetchFailure::BadStatus);
            }
            if response
                .content_length()
                .is_some_and(|length| length > MAX_RESPONSE_BYTES as u64)
            {
                return Err(FetchFailure::ResponseTooLarge);
            }

            let mut bytes = Vec::with_capacity(
                response.content_length().unwrap_or_default().min(64 * 1024) as usize,
            );
            while let Some(chunk) = response
                .chunk()
                .await
                .map_err(|_| FetchFailure::ResponseReadError)?
            {
                if bytes.len().saturating_add(chunk.len()) > MAX_RESPONSE_BYTES {
                    return Err(FetchFailure::ResponseTooLarge);
                }
                bytes.extend_from_slice(&chunk);
            }

            let response: MembershipResponse =
                serde_json::from_slice(&bytes).map_err(|_| FetchFailure::ParseError)?;
            let expected = mapping
                .iter()
                .map(|(name, lookup)| format!("{name}|{lookup}"))
                .collect::<HashSet<_>>();
            Ok(Arc::new(
                response
                    .result
                    .into_iter()
                    .filter(|membership| expected.contains(membership))
                    .collect::<HashSet<_>>(),
            ))
        };

        let result = match tokio::time::timeout(REQUEST_TIMEOUT, operation).await {
            Ok(result) => result,
            Err(_) => Err(FetchFailure::Timeout),
        };
        match result {
            Ok(results) => {
                self.record_fetch_result(source, "success", status, started);
                Ok(results)
            }
            Err(failure) => {
                self.record_fetch_result(source, failure.outcome(), status, started);
                log_w!(
                    TAG,
                    "ID-list membership fetch failed; source={}, result={}, status_code={}",
                    source.tag_value(),
                    failure.outcome(),
                    status_code_tag(status),
                );
                Err(membership_error(failure.message()))
            }
        }
    }

    #[cfg(not(feature = "reqwest"))]
    async fn fetch(
        &self,
        _company_id: &str,
        _mapping: &HashMap<String, String>,
        _source: FetchSource,
    ) -> Result<Arc<HashSet<String>>, StatsigErr> {
        let _ = (&self.server_url, REQUEST_TIMEOUT);
        Err(membership_error(
            "ID-list membership requests require the reqwest feature",
        ))
    }

    fn record_request_result(&self, result: &'static str) {
        let Some(ops_stats) = &self.ops_stats else {
            return;
        };
        ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            REQUEST_METRIC.to_string(),
            1.0,
            Some(HashMap::from([("result".to_string(), result.to_string())])),
        ));
    }

    #[cfg(feature = "reqwest")]
    fn record_fetch_result(
        &self,
        source: FetchSource,
        result: &'static str,
        status: Option<u16>,
        started: Instant,
    ) {
        let Some(ops_stats) = &self.ops_stats else {
            return;
        };
        let tags = HashMap::from([
            ("source".to_string(), source.tag_value().to_string()),
            ("result".to_string(), result.to_string()),
            ("status_code".to_string(), status_code_tag(status)),
        ]);
        ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            FETCH_METRIC.to_string(),
            1.0,
            Some(tags.clone()),
        ));
        ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            FETCH_LATENCY_METRIC.to_string(),
            started.elapsed().as_secs_f64() * 1000.0,
            Some(tags),
        ));
    }

    fn insert(
        &self,
        key: CacheKey,
        expected_generation: Option<u64>,
        results: Arc<HashSet<String>>,
    ) {
        let mut eviction_order = self.eviction_shard(&key).lock();
        if let Some(expected_generation) = expected_generation {
            if self.entries.get(&key).map(|entry| entry.generation) != Some(expected_generation) {
                return;
            }
        }

        let generation = self.next_generation.fetch_add(1, Ordering::Relaxed);
        let refreshed_at = Instant::now();
        if let Some(previous) = self.entries.insert(
            key.clone(),
            CachedResults {
                results,
                refreshed_at,
                generation,
            },
        ) {
            eviction_order.remove(&(previous.refreshed_at, previous.generation));
        }
        eviction_order.insert((refreshed_at, generation), key);

        while eviction_order.len() > MAX_CACHE_ENTRIES_PER_SHARD {
            let Some(((_, oldest_generation), oldest)) = eviction_order.pop_first() else {
                break;
            };
            self.entries
                .remove_if(&oldest, |_, entry| entry.generation == oldest_generation);
        }
    }

    fn remove_if_generation(&self, key: &CacheKey, generation: u64) {
        let mut eviction_order = self.eviction_shard(key).lock();
        if let Some((_, removed)) = self
            .entries
            .remove_if(key, |_, entry| entry.generation == generation)
        {
            eviction_order.remove(&(removed.refreshed_at, removed.generation));
        }
    }

    fn evict_expired(&self, now: Instant, limit: usize) -> usize {
        let mut removed = 0;
        let first_shard =
            self.next_expiration_shard.fetch_add(1, Ordering::Relaxed) % EVICTION_SHARD_COUNT;

        for offset in 0..EVICTION_SHARD_COUNT {
            if removed >= limit {
                break;
            }

            let index = (first_shard + offset) % EVICTION_SHARD_COUNT;
            let mut eviction_order = self.eviction_order[index].lock();
            while removed < limit {
                let Some((&(refreshed_at, _), _)) = eviction_order.first_key_value() else {
                    break;
                };
                if now.saturating_duration_since(refreshed_at) < CACHE_TTL {
                    break;
                }
                let Some(((_, generation), key)) = eviction_order.pop_first() else {
                    break;
                };
                self.entries
                    .remove_if(&key, |_, entry| entry.generation == generation);
                removed += 1;
            }
        }

        removed
    }

    fn eviction_shard(&self, key: &CacheKey) -> &Mutex<BTreeMap<(Instant, u64), CacheKey>> {
        let index = self.entries.hash_usize(key) % EVICTION_SHARD_COUNT;
        &self.eviction_order[index]
    }

    fn start_expiration_task(self: &Arc<Self>) -> Result<(), StatsigErr> {
        let service = Arc::downgrade(self);
        let mut shutdown = self.shutdown_signal.subscribe();
        self.runtime
            .spawn(EXPIRATION_TASK, move |runtime_shutdown| async move {
                let mut interval = tokio::time::interval(EXPIRATION_SWEEP_INTERVAL);
                interval.set_missed_tick_behavior(MissedTickBehavior::Delay);
                interval.tick().await;

                loop {
                    if *shutdown.borrow_and_update() {
                        break;
                    }
                    tokio::select! {
                        biased;
                        _ = shutdown.changed() => break,
                        _ = runtime_shutdown.notified() => break,
                        _ = interval.tick() => {
                            let Some(service) = service.upgrade() else {
                                break;
                            };
                            while service.evict_expired(Instant::now(), MAX_EXPIRATION_SWEEP_BATCH)
                                == MAX_EXPIRATION_SWEEP_BATCH
                            {
                                if *shutdown.borrow() {
                                    break;
                                }
                                tokio::task::yield_now().await;
                            }
                        }
                    }
                }
            })?;

        Ok(())
    }
}

#[cfg(feature = "reqwest")]
fn require_membership_http_support() -> Result<(), StatsigErr> {
    Ok(())
}

#[cfg(not(feature = "reqwest"))]
fn require_membership_http_support() -> Result<(), StatsigErr> {
    Err(StatsigErr::InvalidOperation(
        "ID-list membership requests require the reqwest feature".to_string(),
    ))
}

fn membership_error(message: &'static str) -> StatsigErr {
    StatsigErr::DataStoreFailure(message.to_string())
}

#[cfg(feature = "reqwest")]
fn status_code_tag(status: Option<u16>) -> String {
    status.map_or_else(|| "none".to_string(), |code| code.to_string())
}

fn empty_results() -> Arc<HashSet<String>> {
    static EMPTY: OnceLock<Arc<HashSet<String>>> = OnceLock::new();
    Arc::clone(EMPTY.get_or_init(|| Arc::new(HashSet::new())))
}

#[cfg(all(test, not(feature = "reqwest")))]
mod tests_without_reqwest {
    use super::*;

    #[test]
    fn configured_membership_servers_require_http_support() {
        let service = ScopedIdListMembershipService::new(
            "http://idlist.default.svc.cluster.local:3011".to_string(),
            StatsigRuntime::get_runtime(),
            None,
        );

        assert!(matches!(service, Err(StatsigErr::InvalidOperation(_))));
    }
}

#[cfg(all(test, feature = "reqwest"))]
mod tests {
    use super::*;
    use crate::observability::ops_stats::OpsStatsEvent;
    use mockito::{Matcher, Server};
    use serde_json::json;

    fn service(url: String) -> Arc<ScopedIdListMembershipService> {
        ScopedIdListMembershipService::new(url, StatsigRuntime::get_runtime(), None)
            .expect("membership service should initialize")
    }

    #[test]
    fn cache_keys_are_tenant_scoped_and_mapping_order_independent() {
        let first = HashMap::from([
            ("employees".to_string(), "abcdefgh".to_string()),
            ("testers".to_string(), "12345678".to_string()),
        ]);
        let second = HashMap::from([
            ("testers".to_string(), "12345678".to_string()),
            ("employees".to_string(), "abcdefgh".to_string()),
        ]);

        assert_eq!(
            CacheKey::new("company-a", &first),
            CacheKey::new("company-a", &second)
        );
        assert_ne!(
            CacheKey::new("company-a", &first),
            CacheKey::new("company-b", &first)
        );
    }

    #[tokio::test]
    async fn batches_memberships_once_and_rejects_unrequested_results() {
        let mut server = Server::new_async().await;
        let request = server
            .mock("POST", "/get_id_list_results")
            .match_header(
                "content-type",
                Matcher::Regex("application/json.*".to_string()),
            )
            .match_body(Matcher::Json(json!({
                "companyID": "company-a",
                "mapping": {"employees": "abcdefgh"},
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":["employees|abcdefgh","other|sensitive"]}"#)
            .expect(1)
            .create_async()
            .await;
        let service = service(server.url());
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);

        let first = service.resolve("company-a", mapping.clone()).await;
        let second = service.resolve("company-a", mapping).await;

        assert!(first.contains("employees|abcdefgh"));
        assert!(!first.contains("other|sensitive"));
        assert!(Arc::ptr_eq(&first, &second));
        request.assert_async().await;
        service.shutdown();
    }

    #[tokio::test]
    async fn isolates_companies_and_coalesces_concurrent_requests() {
        let mut server = Server::new_async().await;
        let company_a = server
            .mock("POST", "/get_id_list_results")
            .match_body(Matcher::Json(json!({
                "companyID": "company-a",
                "mapping": {"employees": "abcdefgh"},
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":["employees|abcdefgh"]}"#)
            .expect(1)
            .create_async()
            .await;
        let company_b = server
            .mock("POST", "/get_id_list_results")
            .match_body(Matcher::Json(json!({
                "companyID": "company-b",
                "mapping": {"employees": "abcdefgh"},
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":[]}"#)
            .expect(1)
            .create_async()
            .await;
        let service = service(server.url());
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);

        let (first, second) = tokio::join!(
            service.resolve("company-a", mapping.clone()),
            service.resolve("company-a", mapping.clone())
        );
        let other_company = service.resolve("company-b", mapping).await;

        assert!(first.contains("employees|abcdefgh"));
        assert!(Arc::ptr_eq(&first, &second));
        assert!(other_company.is_empty());
        company_a.assert_async().await;
        company_b.assert_async().await;
        service.shutdown();
    }

    #[tokio::test]
    async fn failed_membership_requests_are_empty_and_never_cached() {
        let mut server = Server::new_async().await;
        let failed = server
            .mock("POST", "/get_id_list_results")
            .with_status(503)
            .expect(2)
            .create_async()
            .await;
        let service = service(server.url());
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);

        assert!(
            service
                .resolve("company-a", mapping.clone())
                .await
                .is_empty()
        );
        assert!(service.resolve("company-a", mapping).await.is_empty());
        assert!(service.entries.is_empty());
        failed.assert_async().await;
        service.shutdown();
    }

    #[tokio::test]
    async fn emits_bounded_membership_metrics_for_success_cache_hits_and_failures() {
        let mut server = Server::new_async().await;
        let success = server
            .mock("POST", "/get_id_list_results")
            .match_body(Matcher::PartialJson(json!({
                "companyID": "sensitive-success-company"
            })))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":["sensitive-list|sensitive-user"]}"#)
            .expect(1)
            .create_async()
            .await;
        let failure = server
            .mock("POST", "/get_id_list_results")
            .match_body(Matcher::PartialJson(json!({
                "companyID": "sensitive-failure-company"
            })))
            .with_status(503)
            .expect(1)
            .create_async()
            .await;
        let ops_stats = Arc::new(OpsStatsForInstance::new());
        let mut events = ops_stats.subscribe_for_test();
        let service = ScopedIdListMembershipService::new(
            server.url(),
            StatsigRuntime::get_runtime(),
            Some(ops_stats),
        )
        .expect("observable membership service should initialize");
        let mapping = HashMap::from([("sensitive-list".to_string(), "sensitive-user".to_string())]);

        let first = service
            .resolve("sensitive-success-company", mapping.clone())
            .await;
        let cached = service
            .resolve("sensitive-success-company", mapping.clone())
            .await;
        let failed = service.resolve("sensitive-failure-company", mapping).await;
        let empty = service
            .resolve("sensitive-success-company", HashMap::new())
            .await;

        assert!(first.contains("sensitive-list|sensitive-user"));
        assert!(Arc::ptr_eq(&first, &cached));
        assert!(failed.is_empty());
        assert!(empty.is_empty());

        let emitted = std::iter::from_fn(|| events.try_recv().ok())
            .filter_map(|event| match event {
                OpsStatsEvent::Observability(event) => Some(event),
                _ => None,
            })
            .collect::<Vec<_>>();
        assert_eq!(emitted.len(), 8);

        for event in &emitted {
            let tags = event.tags.as_ref().expect("membership metrics have tags");
            assert!(
                tags.keys()
                    .all(|tag| matches!(tag.as_str(), "result" | "source" | "status_code"))
            );
            assert!(tags.values().all(|tag| !tag.contains("sensitive")));
        }

        assert!(emitted.iter().any(|event| {
            event.metric_name == FETCH_METRIC
                && matches!(&event.metric_type, MetricType::Increment)
                && event.tags.as_ref().is_some_and(|tags| {
                    tags.get("source")
                        .is_some_and(|source| source == "foreground")
                        && tags.get("result").is_some_and(|result| result == "success")
                        && tags
                            .get("status_code")
                            .is_some_and(|status| status == "200")
                })
        }));
        assert!(emitted.iter().any(|event| {
            event.metric_name == FETCH_METRIC
                && matches!(&event.metric_type, MetricType::Increment)
                && event.tags.as_ref().is_some_and(|tags| {
                    tags.get("result")
                        .is_some_and(|result| result == "bad_status")
                        && tags
                            .get("status_code")
                            .is_some_and(|status| status == "503")
                })
        }));
        assert_eq!(
            emitted
                .iter()
                .filter(|event| {
                    event.metric_name == FETCH_LATENCY_METRIC
                        && matches!(&event.metric_type, MetricType::Dist)
                        && event.value >= 0.0
                })
                .count(),
            2
        );
        for expected in [
            "cache_miss_success",
            "cache_hit",
            "cache_miss_failure",
            "empty_mapping",
        ] {
            assert!(emitted.iter().any(|event| {
                event.metric_name == REQUEST_METRIC
                    && matches!(&event.metric_type, MetricType::Increment)
                    && event
                        .tags
                        .as_ref()
                        .and_then(|tags| tags.get("result"))
                        .is_some_and(|result| result == expected)
            }));
        }

        success.assert_async().await;
        failure.assert_async().await;
        service.shutdown();
    }

    #[tokio::test]
    async fn slow_membership_requests_are_bounded_and_never_cached() {
        let listener = tokio::net::TcpListener::bind("127.0.0.1:0")
            .await
            .expect("the slow membership fixture should bind locally");
        let server_url = format!(
            "http://{}",
            listener
                .local_addr()
                .expect("the slow membership fixture should expose its local address")
        );
        let (accepted, observed) = tokio::sync::oneshot::channel();
        let server_task = tokio::spawn(async move {
            let (connection, _) = listener
                .accept()
                .await
                .expect("the membership client should connect to its configured service");
            let _ = accepted.send(());
            tokio::time::sleep(Duration::from_secs(2)).await;
            drop(connection);
        });
        let service = service(server_url);
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);
        let started = Instant::now();

        let results = tokio::time::timeout(
            Duration::from_secs(1),
            service.resolve("company-a", mapping),
        )
        .await
        .expect("a slow membership service must not exceed its bounded request timeout");

        observed
            .await
            .expect("the membership request must reach the slow service");
        assert!(results.is_empty());
        assert!(service.entries.is_empty());
        assert!(
            started.elapsed() >= REQUEST_TIMEOUT.saturating_sub(Duration::from_millis(25)),
            "the slow-service fixture should exercise the actual membership timeout"
        );
        server_task.abort();
        let _ = server_task.await;
        service.shutdown();
    }

    #[tokio::test]
    async fn empty_mappings_and_shutdown_do_not_query_the_service() {
        let mut server = Server::new_async().await;
        let unexpected = server
            .mock("POST", "/get_id_list_results")
            .expect(0)
            .create_async()
            .await;
        let service = service(server.url());

        assert!(
            service
                .resolve("company-a", HashMap::new())
                .await
                .is_empty()
        );
        service.shutdown();
        assert!(
            service
                .resolve(
                    "company-a",
                    HashMap::from([("employees".to_string(), "abcdefgh".to_string())]),
                )
                .await
                .is_empty()
        );
        unexpected.assert_async().await;
    }

    #[tokio::test]
    async fn stale_entries_refresh_without_blocking_or_duplicate_fetches() {
        let mut server = Server::new_async().await;
        let refreshed = server
            .mock("POST", "/get_id_list_results")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":["employees|abcdefgh"]}"#)
            .expect(1)
            .create_async()
            .await;
        let ops_stats = Arc::new(OpsStatsForInstance::new());
        let mut metrics = ops_stats.subscribe_for_test();
        let service = ScopedIdListMembershipService::new(
            server.url(),
            StatsigRuntime::get_runtime(),
            Some(ops_stats),
        )
        .expect("observable membership service should initialize");
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);
        let key = CacheKey::new("company-a", &mapping);
        service.insert(key.clone(), None, Arc::new(HashSet::new()));

        {
            let mut eviction_order = service.eviction_shard(&key).lock();
            let mut entry = service.entries.get_mut(&key).unwrap();
            eviction_order.remove(&(entry.refreshed_at, entry.generation));
            entry.refreshed_at -= CACHE_FRESHNESS;
            eviction_order.insert((entry.refreshed_at, entry.generation), key.clone());
        }

        let first = service.resolve("company-a", mapping.clone()).await;
        let second = service.resolve("company-a", mapping.clone()).await;
        assert!(first.is_empty());
        assert!(second.is_empty());

        tokio::time::timeout(Duration::from_secs(2), async {
            loop {
                if service
                    .entries
                    .get(&key)
                    .is_some_and(|entry| entry.results.contains("employees|abcdefgh"))
                {
                    break;
                }
                tokio::time::sleep(Duration::from_millis(10)).await;
            }
        })
        .await
        .expect("stale memberships should refresh in the background");

        let emitted = std::iter::from_fn(|| metrics.try_recv().ok())
            .filter_map(|event| match event {
                OpsStatsEvent::Observability(event) => Some(event),
                _ => None,
            })
            .collect::<Vec<_>>();
        assert!(emitted.iter().any(|event| {
            event.metric_name == FETCH_METRIC
                && event.tags.as_ref().is_some_and(|tags| {
                    tags.get("source")
                        .is_some_and(|source| source == "background_refresh")
                        && tags.get("result").is_some_and(|result| result == "success")
                        && tags
                            .get("status_code")
                            .is_some_and(|status| status == "200")
                })
        }));
        assert_eq!(
            emitted
                .iter()
                .filter(|event| {
                    event.metric_name == REQUEST_METRIC
                        && event
                            .tags
                            .as_ref()
                            .and_then(|tags| tags.get("result"))
                            .is_some_and(|result| result == "stale_cache_hit")
                })
                .count(),
            2
        );

        refreshed.assert_async().await;
        service.shutdown();
    }

    #[tokio::test]
    async fn saturated_background_refreshes_never_block_cached_requests() {
        let mut server = Server::new_async().await;
        let refreshed = server
            .mock("POST", "/get_id_list_results")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{"result":["employees|abcdefgh"]}"#)
            .expect(1)
            .create_async()
            .await;
        let service = service(server.url());
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);
        let key = CacheKey::new("company-a", &mapping);
        service.insert(key.clone(), None, Arc::new(HashSet::new()));

        {
            let mut eviction_order = service.eviction_shard(&key).lock();
            let mut entry = service.entries.get_mut(&key).unwrap();
            eviction_order.remove(&(entry.refreshed_at, entry.generation));
            entry.refreshed_at -= CACHE_FRESHNESS;
            eviction_order.insert((entry.refreshed_at, entry.generation), key.clone());
        }

        let permits = Arc::clone(&service.refresh_permits)
            .try_acquire_many_owned(MAX_CONCURRENT_BACKGROUND_REFRESHES as u32)
            .expect("the test should reserve all background refresh capacity");
        let cached = tokio::time::timeout(
            Duration::from_millis(100),
            service.resolve("company-a", mapping.clone()),
        )
        .await
        .expect("saturated refresh capacity must not block a stale cache hit");
        assert!(cached.is_empty());
        assert!(service.refreshing.is_empty());

        drop(permits);
        let cached = service.resolve("company-a", mapping).await;
        assert!(cached.is_empty());

        tokio::time::timeout(Duration::from_secs(2), async {
            loop {
                if service
                    .entries
                    .get(&key)
                    .is_some_and(|entry| entry.results.contains("employees|abcdefgh"))
                {
                    break;
                }
                tokio::time::sleep(Duration::from_millis(10)).await;
            }
        })
        .await
        .expect("a deferred refresh should resume once capacity is available");

        refreshed.assert_async().await;
        service.shutdown();
    }

    #[tokio::test]
    async fn oversized_and_malformed_responses_are_not_cached() {
        let mut server = Server::new_async().await;
        let malformed = server
            .mock("POST", "/get_id_list_results")
            .match_body(Matcher::PartialJson(json!({"companyID":"malformed"})))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body("not-json")
            .expect(1)
            .create_async()
            .await;
        let oversized = server
            .mock("POST", "/get_id_list_results")
            .match_body(Matcher::PartialJson(json!({"companyID":"oversized"})))
            .with_status(200)
            .with_header("content-length", &(MAX_RESPONSE_BYTES + 1).to_string())
            .expect(1)
            .create_async()
            .await;
        let service = service(server.url());
        let mapping = HashMap::from([("employees".to_string(), "abcdefgh".to_string())]);

        assert!(
            service
                .resolve("malformed", mapping.clone())
                .await
                .is_empty()
        );
        assert!(service.resolve("oversized", mapping).await.is_empty());
        assert!(service.entries.is_empty());
        malformed.assert_async().await;
        oversized.assert_async().await;
        service.shutdown();
    }
}
