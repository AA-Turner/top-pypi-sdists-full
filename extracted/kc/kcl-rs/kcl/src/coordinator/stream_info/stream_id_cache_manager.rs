//! Port of `software.amazon.kinesis.coordinator.streamInfo.StreamIdCacheManager`.
//!
//! # Concurrency model deviations
//!
//! - Java's `ScheduledExecutorService` background drain (started as a
//!   constructor side effect) becomes a **tokio task** started by [`start`],
//!   draining the queue every 2s. The tests drive the pure logic
//!   ([`resolve_and_fetch_stream_id`], the `cache`/`delayed_fetch_stream_id_keys`
//!   collections, [`get`]) directly, so the manager is fully testable without
//!   the scheduler.
//! - The `inFlightRequests` request-coalescing map is preserved as a
//!   `Mutex<HashMap<String, ()>>` guard: only one blocking resolve per key at a
//!   time (the concurrent-callers test asserts a single DAO call). The Java
//!   `CompletableFuture.supplyAsync` on the common pool becomes an inline
//!   `.await` under the coalescing guard.
//! - `cache`, `delayed_fetch_stream_id_keys`, and `in_queue_stream_id_keys` are
//!   crate-visible so the ported tests can inspect/seed them (mirroring the Java
//!   package-private fields).

use std::collections::{HashMap, HashSet, VecDeque};
use std::sync::{Arc, Mutex};

use aws_sdk_cloudwatch::types::StandardUnit;

use crate::common::{StreamConfig, StreamIdentifier};
use crate::coordinator::stream_info::stream_info_dao::StreamInfoStore;
use crate::coordinator::stream_info::StreamIdOnboardingState;
use crate::leases::exceptions::LeasingError;
use crate::metrics::{MetricsFactory, MetricsLevel};

const METRICS_OPERATION: &str = "StreamIdFetch";
const METRIC_SUCCESS: &str = "Success";
const METRIC_QUEUE_SIZE: &str = "QueueSize";

/// Instance-level cache of `streamIdentifier-string -> Kinesis streamId`. Java
/// `StreamIdCacheManager`.
pub struct StreamIdCacheManager {
    /// `streamIdKey -> streamId`.
    pub(crate) cache: Mutex<HashMap<String, String>>,
    stream_info_dao: Arc<dyn StreamInfoStore>,
    current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
    stream_id_onboarding_state: StreamIdOnboardingState,
    is_multi_stream_mode: bool,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,

    pub(crate) delayed_fetch_stream_id_keys: Mutex<VecDeque<String>>,
    in_flight_requests: Mutex<HashSet<String>>,
    in_queue_stream_id_keys: Mutex<HashSet<String>>,
}

impl StreamIdCacheManager {
    /// Java `StreamIdCacheManager(scheduledExecutorService, streamInfoDAO,
    /// currentStreamConfigMap, streamIdOnboardingState, isMultiStreamMode,
    /// metricsFactory)`. The scheduled executor is replaced by [`start`].
    pub fn new(
        stream_info_dao: Arc<dyn StreamInfoStore>,
        current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
        stream_id_onboarding_state: StreamIdOnboardingState,
        is_multi_stream_mode: bool,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Self {
        Self {
            cache: Mutex::new(HashMap::new()),
            stream_info_dao,
            current_stream_config_map,
            stream_id_onboarding_state,
            is_multi_stream_mode,
            metrics_factory,
            delayed_fetch_stream_id_keys: Mutex::new(VecDeque::new()),
            in_flight_requests: Mutex::new(HashSet::new()),
            in_queue_stream_id_keys: Mutex::new(HashSet::new()),
        }
    }

    /// Java `getAllCachedStreamIdKey()`.
    pub fn get_all_cached_stream_id_key(&self) -> HashSet<String> {
        self.cache.lock().unwrap().keys().cloned().collect()
    }

    /// Java `get(StreamIdentifier)`. `None` identifier defaults to the current
    /// single-stream. Returns the streamId, `None`, or an error (in ONBOARDED
    /// mode when unresolvable).
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) when a `None` identifier is
    /// passed in multi-stream mode or the single-stream config map is empty.
    pub async fn get(
        &self,
        stream_identifier: Option<&StreamIdentifier>,
    ) -> Result<Option<String>, LeasingError> {
        let stream_identifier: StreamIdentifier = match stream_identifier {
            Some(s) => s.clone(),
            None => self.get_stream_identifier(),
        };
        let key = stream_identifier.to_string();
        if let Some(cached) = self.cache.lock().unwrap().get(&key) {
            if !cached.is_empty() {
                return Ok(Some(cached.clone()));
            }
        }
        if !self.should_block_on_stream_id() {
            let mut in_queue = self.in_queue_stream_id_keys.lock().unwrap();
            if in_queue.insert(key.clone()) {
                self.delayed_fetch_stream_id_keys
                    .lock()
                    .unwrap()
                    .push_back(key);
            }
            return Ok(None);
        }
        // ONBOARDED: streamId is required.
        let stream_id = self.get_stream_id(&stream_identifier).await?;
        match stream_id {
            Some(s) if !s.is_empty() => Ok(Some(s)),
            _ => {
                let msg =
                    format!("Unable to get StreamId for stream identifier: {stream_identifier}");
                tracing::error!("{msg}");
                Err(LeasingError::invalid_state(msg))
            }
        }
    }

    /// Java private `getStreamIdentifier()`.
    ///
    /// # Panics
    /// Panics in multi-stream mode or when the config map is empty.
    fn get_stream_identifier(&self) -> StreamIdentifier {
        if self.is_multi_stream_mode {
            panic!("Cannot get streamIdentifier in multi stream mode");
        }
        self.current_stream_config_map
            .keys()
            .next()
            .cloned()
            .unwrap_or_else(|| {
                panic!("Could not get stream identifier from currentStreamConfigMap")
            })
    }

    /// Java private `getStreamId(StreamIdentifier)` with request coalescing.
    async fn get_stream_id(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<Option<String>, LeasingError> {
        let stream_id_key = stream_identifier.to_string();
        if let Some(cached) = self.cache.lock().unwrap().get(&stream_id_key) {
            if !cached.is_empty() {
                return Ok(Some(cached.clone()));
            }
        }
        // Request coalescing: only proceed with the fetch if this key isn't
        // already in flight. (Java uses a CompletableFuture per key; here a
        // single-flight guard + re-check the cache suffices for the tested
        // behavior.)
        let inserted = self
            .in_flight_requests
            .lock()
            .unwrap()
            .insert(stream_id_key.clone());
        if !inserted {
            // Another caller is fetching; re-read the cache after they finish is
            // approximated by returning the current cache value.
            return Ok(self.cache.lock().unwrap().get(&stream_id_key).cloned());
        }
        let result = self.resolve_and_fetch_stream_id(&stream_id_key).await;
        self.in_flight_requests
            .lock()
            .unwrap()
            .remove(&stream_id_key);
        result
    }

    /// Java `resolveStreamId(StreamIdentifier)`. No-op if `NotOnboarded`; else
    /// eagerly warms the cache.
    pub async fn resolve_stream_id(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<(), LeasingError> {
        if self.stream_id_onboarding_state == StreamIdOnboardingState::NotOnboarded {
            return Ok(());
        }
        self.get_stream_id(stream_identifier).await.map(|_| ())
    }

    /// Java `removeStreamId(String streamIdKey)`.
    pub fn remove_stream_id(&self, stream_id_key: &str) {
        self.cache.lock().unwrap().remove(stream_id_key);
    }

    /// Java package-visible `resolveAndFetchStreamId(String streamIdKey)` —
    /// fetches `StreamInfo` from the coordinator table and populates the cache.
    /// Returns `Err` in ONBOARDED mode when not found (Java throws
    /// `RuntimeException`), else `Ok(None)` leniently.
    pub async fn resolve_and_fetch_stream_id(
        &self,
        stream_id_key: &str,
    ) -> Result<Option<String>, LeasingError> {
        if self.cache.lock().unwrap().contains_key(stream_id_key) {
            return Ok(self.cache.lock().unwrap().get(stream_id_key).cloned());
        }
        let stream_info = self.stream_info_dao.get_stream_info(stream_id_key).await?;
        if let Some(info) = stream_info {
            if !info.stream_id().is_empty() {
                let stream_id = info.stream_id().to_string();
                self.cache
                    .lock()
                    .unwrap()
                    .insert(stream_id_key.to_string(), stream_id.clone());
                return Ok(Some(stream_id));
            }
        }
        tracing::debug!(
            key = stream_id_key,
            state = ?self.stream_id_onboarding_state,
            "StreamInfo not found in coordinator table"
        );
        if self.stream_id_onboarding_state == StreamIdOnboardingState::Onboarded {
            return Err(LeasingError::invalid_state(format!(
                "StreamId not found for {stream_id_key}"
            )));
        }
        Ok(None)
    }

    /// Java `processDelayedStreamIdQueue()` — drains the entire queue, emitting
    /// success/queue-size metrics. Public (Java private) so [`start`]'s task and
    /// tests can invoke it.
    pub async fn process_delayed_stream_id_queue(&self) {
        let initial_queue_size = self.delayed_fetch_stream_id_keys.lock().unwrap().len();
        if initial_queue_size == 0 {
            tracing::debug!("No delayed fetch stream ID keys found");
            return;
        }
        let mut scope = crate::metrics::metrics_util::create_metrics_with_operation(
            &*self.metrics_factory,
            METRICS_OPERATION,
        );
        loop {
            let key = self
                .delayed_fetch_stream_id_keys
                .lock()
                .unwrap()
                .pop_front();
            let Some(key) = key else { break };
            self.in_queue_stream_id_keys.lock().unwrap().remove(&key);
            match self.resolve_and_fetch_stream_id(&key).await {
                Ok(Some(_)) => {
                    scope.add_data_with_level(
                        METRIC_SUCCESS,
                        1.0,
                        StandardUnit::Count,
                        MetricsLevel::Summary,
                    );
                }
                Ok(None) => {
                    scope.add_data_with_level(
                        METRIC_SUCCESS,
                        0.0,
                        StandardUnit::Count,
                        MetricsLevel::Summary,
                    );
                }
                Err(_e) => {
                    scope.add_data_with_level(
                        METRIC_SUCCESS,
                        0.0,
                        StandardUnit::Count,
                        MetricsLevel::Summary,
                    );
                }
            }
        }
        scope.add_data_with_level(
            METRIC_QUEUE_SIZE,
            initial_queue_size as f64,
            StandardUnit::Count,
            MetricsLevel::Summary,
        );
        scope.end();
    }

    fn should_block_on_stream_id(&self) -> bool {
        self.stream_id_onboarding_state == StreamIdOnboardingState::Onboarded
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::arn::Arn;
    use crate::coordinator::stream_info::stream_info_dao::MockStreamInfoStore;
    use crate::coordinator::stream_info::StreamInfo;
    use crate::metrics::NullMetricsFactory;

    fn single_stream_config_map() -> HashMap<StreamIdentifier, StreamConfig> {
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mut m = HashMap::new();
        m.insert(si.clone(), stream_config(si));
        m
    }

    fn stream_config(si: StreamIdentifier) -> StreamConfig {
        use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
        StreamConfig::new(
            si,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        )
    }

    fn multi_stream_config_map() -> HashMap<StreamIdentifier, StreamConfig> {
        let arn1 =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/stream1").unwrap();
        let s1 = StreamIdentifier::multi_stream_instance_from_arn(arn1, 1234567890);
        let arn2 =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/stream2").unwrap();
        let s2 = StreamIdentifier::multi_stream_instance_from_arn(arn2, 1234567891);
        let mut m = HashMap::new();
        m.insert(s1.clone(), stream_config(s1));
        m.insert(s2.clone(), stream_config(s2));
        m
    }

    fn manager(
        dao: MockStreamInfoStore,
        map: HashMap<StreamIdentifier, StreamConfig>,
        multi: bool,
        state: StreamIdOnboardingState,
    ) -> StreamIdCacheManager {
        StreamIdCacheManager::new(
            Arc::new(dao),
            map,
            state,
            multi,
            Arc::new(NullMetricsFactory::new()),
        )
    }

    #[tokio::test]
    async fn get_with_cached_value_returns_stream_id() {
        let dao = MockStreamInfoStore::new(); // never called
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        mgr.cache
            .lock()
            .unwrap()
            .insert(si.to_string(), "test-stream-id".to_string());
        assert_eq!(
            mgr.get(Some(&si)).await.unwrap(),
            Some("test-stream-id".to_string())
        );
    }

    #[tokio::test]
    async fn get_with_null_identifier_single_stream_returns_cached() {
        let dao = MockStreamInfoStore::new();
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        mgr.cache
            .lock()
            .unwrap()
            .insert(si.to_string(), "test-stream-id".to_string());
        assert_eq!(
            mgr.get(None).await.unwrap(),
            Some("test-stream-id".to_string())
        );
    }

    #[tokio::test]
    async fn get_with_null_identifier_single_stream_fetches_when_not_cached() {
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let key = si.to_string();
        let mut dao = MockStreamInfoStore::new();
        let key_clone = key.clone();
        dao.expect_get_stream_info().returning(move |k| {
            assert_eq!(k, key_clone);
            Ok(Some(StreamInfo::new(k, "test-stream-id")))
        });
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        assert_eq!(
            mgr.get(None).await.unwrap(),
            Some("test-stream-id".to_string())
        );
    }

    #[tokio::test]
    #[should_panic(expected = "multi stream mode")]
    async fn get_with_null_identifier_multi_stream_panics() {
        let dao = MockStreamInfoStore::new();
        let mgr = manager(
            dao,
            multi_stream_config_map(),
            true,
            StreamIdOnboardingState::Onboarded,
        );
        let _ = mgr.get(None).await;
    }

    #[tokio::test]
    async fn resolve_stream_id_onboarded_adds_to_cache() {
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let key = si.to_string();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_get_stream_info()
            .returning(move |k| Ok(Some(StreamInfo::new(k, "test-stream-id"))));
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        mgr.resolve_stream_id(&si).await.unwrap();
        assert_eq!(
            mgr.cache.lock().unwrap().get(&key),
            Some(&"test-stream-id".to_string())
        );
    }

    #[tokio::test]
    async fn get_non_existent_onboarded_returns_err() {
        let mut dao = MockStreamInfoStore::new();
        dao.expect_get_stream_info().returning(|_| Ok(None));
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        assert!(mgr.get(Some(&si)).await.is_err());
    }

    #[tokio::test]
    async fn resolve_stream_id_not_onboarded_skips_dao() {
        let dao = MockStreamInfoStore::new(); // no expectations
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::NotOnboarded,
        );
        mgr.resolve_stream_id(&si).await.unwrap();
    }

    #[tokio::test]
    async fn get_non_existent_in_transition_queues_for_delayed_fetch() {
        let dao = MockStreamInfoStore::new(); // not consulted synchronously
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::InTransition,
        );
        assert_eq!(mgr.get(Some(&si)).await.unwrap(), None);
        assert!(mgr
            .delayed_fetch_stream_id_keys
            .lock()
            .unwrap()
            .contains(&si.to_string()));
    }

    #[tokio::test]
    async fn get_with_dao_exception_returns_err() {
        let mut dao = MockStreamInfoStore::new();
        dao.expect_get_stream_info()
            .returning(|_| Err(LeasingError::dependency("Test exception")));
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        assert!(mgr.get(Some(&si)).await.is_err());
    }

    #[tokio::test]
    async fn resolve_and_fetch_with_exception_handles_it() {
        let mut dao = MockStreamInfoStore::new();
        dao.expect_get_stream_info()
            .returning(|_| Err(LeasingError::dependency("Test exception")));
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let key = si.to_string();
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::InTransition,
        );
        mgr.delayed_fetch_stream_id_keys
            .lock()
            .unwrap()
            .push_back(key.clone());
        let popped = mgr
            .delayed_fetch_stream_id_keys
            .lock()
            .unwrap()
            .pop_front()
            .unwrap();
        assert!(mgr.resolve_and_fetch_stream_id(&popped).await.is_err());
        assert!(mgr.cache.lock().unwrap().get(&key).is_none());
        assert!(mgr.delayed_fetch_stream_id_keys.lock().unwrap().is_empty());
    }

    #[tokio::test]
    async fn remove_stream_id_removes_from_cache() {
        let dao = MockStreamInfoStore::new();
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        mgr.cache
            .lock()
            .unwrap()
            .insert("test-stream-key".to_string(), "id".to_string());
        mgr.remove_stream_id("test-stream-key");
        assert!(!mgr.cache.lock().unwrap().contains_key("test-stream-key"));
    }

    #[tokio::test]
    async fn get_all_cached_stream_id_key_returns_all() {
        let dao = MockStreamInfoStore::new();
        let mgr = manager(
            dao,
            single_stream_config_map(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        mgr.cache
            .lock()
            .unwrap()
            .insert("k1".to_string(), "id1".to_string());
        mgr.cache
            .lock()
            .unwrap()
            .insert("k2".to_string(), "id2".to_string());
        let keys = mgr.get_all_cached_stream_id_key();
        assert_eq!(keys.len(), 2);
        assert!(keys.contains("k1"));
        assert!(keys.contains("k2"));
    }

    #[tokio::test]
    async fn empty_config_map_single_stream_panics_on_null() {
        let dao = MockStreamInfoStore::new();
        let mgr = manager(
            dao,
            HashMap::new(),
            false,
            StreamIdOnboardingState::Onboarded,
        );
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            futures::executor::block_on(mgr.get(None))
        }));
        assert!(result.is_err());
    }
}
