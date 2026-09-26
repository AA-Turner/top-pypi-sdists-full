use super::{
    event_logger::{EventLogger, ExposureTrigger, PreparedDelayedExposure},
    event_queue::queued_expo::BorrowedLayerParamExposureOp,
};
use crate::{
    interned_string::InternedString,
    log_d, log_e,
    observability::{
        observability_client_adapter::{MetricType, ObservabilityEvent},
        ops_stats::OpsStatsForInstance,
    },
    statsig_types_raw::PartialLayerRaw,
};
use parking_lot::{Mutex, MutexGuard};
use std::{
    collections::{HashMap, HashSet, VecDeque},
    sync::Arc,
    time::{Duration, Instant},
};
use uuid::Uuid;

const TAG: &str = stringify!(DelayedExposureStore);
const DEFAULT_MAX_TOKENS: usize = 10_000;
const METRICS_EMIT_INTERVAL: Duration = Duration::from_secs(10);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct DelayedExposureStoreStats {
    active_tokens: usize,
    insertion_order_tokens: usize,
    stale_insertion_order_tokens: usize,
}

pub struct DelayedExposureStore {
    inner: Mutex<DelayedExposureStoreInner>,
    max_tokens: usize,
    ops_stats: Arc<OpsStatsForInstance>,
}

struct DelayedExposureStoreInner {
    entries: HashMap<String, DelayedExposureEntry>,
    insertion_order: VecDeque<String>,
    consumed: u64,
    released: u64,
    missing: u64,
    evicted: u64,
    last_metrics_emitted_at: Option<Instant>,
}

enum DelayedExposureEntry {
    Prepared(PreparedDelayedExposure),
    Layer(Box<DelayedLayerExposure>),
}

struct DelayedLayerExposure {
    partial_raw: Arc<PartialLayerRaw>,
    logged_params: HashSet<String>,
}

impl DelayedExposureStore {
    pub fn new(ops_stats: Arc<OpsStatsForInstance>) -> Self {
        Self {
            inner: Mutex::new(DelayedExposureStoreInner {
                entries: HashMap::new(),
                insertion_order: VecDeque::new(),
                consumed: 0,
                released: 0,
                missing: 0,
                evicted: 0,
                last_metrics_emitted_at: None,
            }),
            max_tokens: DEFAULT_MAX_TOKENS,
            ops_stats,
        }
    }

    pub fn insert_prepared(&self, prepared: PreparedDelayedExposure) -> String {
        self.insert(DelayedExposureEntry::Prepared(prepared))
    }

    pub fn insert_layer(&self, partial_raw: PartialLayerRaw) -> String {
        self.insert(DelayedExposureEntry::Layer(Box::new(
            DelayedLayerExposure {
                partial_raw: Arc::new(partial_raw),
                logged_params: HashSet::new(),
            },
        )))
    }

    pub fn log_delayed_exposure(&self, token: &str, event_logger: &Arc<EventLogger>) -> bool {
        let entry = {
            let Some(mut inner) = self.try_lock_inner("log_delayed_exposure") else {
                return false;
            };

            match inner.entries.remove(token) {
                Some(entry) => {
                    inner.consumed += 1;
                    log_d!(
                        TAG,
                        "consumed delayed exposure token; outstanding={}",
                        inner.entries.len()
                    );
                    entry
                }
                None => {
                    inner.missing += 1;
                    return false;
                }
            }
        };

        match entry {
            DelayedExposureEntry::Prepared(prepared) => {
                event_logger.enqueue_prepared(prepared);
                true
            }
            DelayedExposureEntry::Layer(_) => false,
        }
    }

    pub fn log_delayed_layer_parameter_exposure(
        &self,
        token: &str,
        parameter_name: &str,
        event_logger: &Arc<EventLogger>,
    ) -> bool {
        let partial_raw = {
            let Some(mut inner) = self.try_lock_inner("log_delayed_layer_parameter_exposure")
            else {
                return false;
            };

            let Some(DelayedExposureEntry::Layer(layer)) = inner.entries.get_mut(token) else {
                inner.missing += 1;
                return false;
            };

            if !layer.logged_params.insert(parameter_name.to_string()) {
                return true;
            }

            Arc::clone(&layer.partial_raw)
        };

        let operation = BorrowedLayerParamExposureOp::new(
            InternedString::from_str_ref(parameter_name),
            ExposureTrigger::Auto,
            &partial_raw,
            None,
        );
        let prepared = event_logger.prepare_event(operation);
        let shared_control_prepared = partial_raw
            .shared_control_exposures
            .as_ref()
            .filter(|exposures| !exposures.is_empty())
            .map(|exposures| {
                exposures
                    .iter()
                    .filter(|exposure| exposure.explicit_parameters.contains(parameter_name))
                    .filter_map(|exposure| {
                        let operation = BorrowedLayerParamExposureOp::shared_control(
                            InternedString::from_str_ref(parameter_name),
                            ExposureTrigger::Auto,
                            &partial_raw,
                            exposure,
                            None,
                        );
                        event_logger.prepare_event(operation)
                    })
                    .collect::<Vec<_>>()
            });

        if let Some(prepared) = prepared {
            event_logger.enqueue_prepared(prepared);
        }
        if let Some(shared_control_prepared) = shared_control_prepared {
            for prepared in shared_control_prepared {
                event_logger.enqueue_prepared(prepared);
            }
        }

        true
    }

    pub fn release(&self, token: &str) -> bool {
        let Some(mut inner) = self.try_lock_inner("release") else {
            return false;
        };

        match inner.entries.remove(token) {
            Some(_) => {
                inner.released += 1;
                log_d!(
                    TAG,
                    "released delayed exposure token; outstanding={}",
                    inner.entries.len()
                );
                true
            }
            None => {
                inner.missing += 1;
                false
            }
        }
    }

    pub fn release_many(&self, tokens: &[String]) -> usize {
        let released = tokens.iter().filter(|token| self.release(token)).count();
        self.emit_metrics();
        released
    }

    pub fn clear(&self) {
        let Some(mut inner) = self.try_lock_inner("clear") else {
            return;
        };

        let count = inner.entries.len();
        inner.entries.clear();
        inner.insertion_order.clear();
        log_d!(TAG, "cleared delayed exposure store; dropped={count}");
    }

    fn insert(&self, entry: DelayedExposureEntry) -> String {
        let token = Uuid::new_v4().to_string();
        let Some(mut inner) = self.try_lock_inner("insert") else {
            return token;
        };

        inner.entries.insert(token.clone(), entry);
        inner.insertion_order.push_back(token.clone());

        while inner.entries.len() > self.max_tokens {
            let Some(oldest) = inner.insertion_order.pop_front() else {
                break;
            };

            if inner.entries.remove(&oldest).is_some() {
                inner.evicted += 1;
            }
        }

        // Consumed and released tokens leave tombstones in the eviction queue.
        // Compact only after enough insertions to amortize the scan, even when
        // active entries never reach the eviction limit. Retain preserves FIFO
        // order for the remaining live tokens without scanning on every release.
        if inner.insertion_order.len() > self.max_tokens.saturating_mul(2) {
            let DelayedExposureStoreInner {
                entries,
                insertion_order,
                ..
            } = &mut *inner;
            insertion_order.retain(|token| entries.contains_key(token));
        }

        log_d!(
            TAG,
            "created delayed exposure token; outstanding={}",
            inner.entries.len()
        );
        token
    }

    fn stats(inner: &DelayedExposureStoreInner) -> DelayedExposureStoreStats {
        DelayedExposureStoreStats {
            active_tokens: inner.entries.len(),
            insertion_order_tokens: inner.insertion_order.len(),
            stale_insertion_order_tokens: inner
                .insertion_order
                .len()
                .saturating_sub(inner.entries.len()),
        }
    }

    fn take_metrics_snapshot_if_due(
        inner: &mut DelayedExposureStoreInner,
        now: Instant,
    ) -> Option<DelayedExposureStoreStats> {
        if let Some(last_emitted_at) = inner.last_metrics_emitted_at {
            if now.saturating_duration_since(last_emitted_at) < METRICS_EMIT_INTERVAL {
                return None;
            }
        }

        inner.last_metrics_emitted_at = Some(now);
        Some(Self::stats(inner))
    }

    fn emit_metrics(&self) {
        let Some(mut inner) = self.try_lock_inner("emit_metrics") else {
            return;
        };
        let Some(stats) = Self::take_metrics_snapshot_if_due(&mut inner, Instant::now()) else {
            return;
        };
        drop(inner);

        for (metric_name, value) in [
            (
                "delayed_exposure_store_active_token_count",
                stats.active_tokens,
            ),
            (
                "delayed_exposure_store_insertion_order_token_count",
                stats.insertion_order_tokens,
            ),
            (
                "delayed_exposure_store_stale_insertion_order_token_count",
                stats.stale_insertion_order_tokens,
            ),
        ] {
            self.ops_stats.log(ObservabilityEvent::new_event(
                MetricType::Gauge,
                metric_name.to_string(),
                value as f64,
                None,
            ));
        }
    }

    fn try_lock_inner(&self, operation: &str) -> Option<MutexGuard<'_, DelayedExposureStoreInner>> {
        match self.inner.try_lock_for(crate::macros::LOCK_TIMEOUT) {
            Some(inner) => Some(inner),
            None => {
                log_e!(
                    TAG,
                    "Failed to lock delayed exposure store for {}",
                    operation
                );
                None
            }
        }
    }
}

impl Default for DelayedExposureStore {
    fn default() -> Self {
        Self::new(Arc::new(OpsStatsForInstance::new()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        EventLoggingAdapter, StatsigErr, StatsigOptions, StatsigRuntime,
        event_logging::{
            event_queue::queued_passthrough::EnqueuePassthroughOp, statsig_event::StatsigEvent,
            statsig_event_internal::StatsigEventInternal,
        },
        log_event_payload::LogEventRequest,
        user::StatsigUserLoggable,
    };
    use async_trait::async_trait;
    use std::sync::atomic::{AtomicU64, Ordering};

    fn small_store() -> DelayedExposureStore {
        DelayedExposureStore {
            max_tokens: 4,
            ..Default::default()
        }
    }

    fn insert_layer(store: &DelayedExposureStore) -> String {
        let layer = serde_json::from_value(serde_json::json!({
            "name": "test_layer",
            "details": { "reason": "Network:Recognized" },
            "disableExposure": false,
            "user": {},
        }))
        .unwrap();
        store.insert_layer(layer)
    }

    #[derive(Default)]
    struct CountingEventAdapter(AtomicU64);

    #[async_trait]
    impl EventLoggingAdapter for CountingEventAdapter {
        async fn start(&self, _runtime: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
            Ok(())
        }

        async fn log_events(&self, request: LogEventRequest) -> Result<bool, StatsigErr> {
            self.0.fetch_add(request.event_count, Ordering::Relaxed);
            Ok(true)
        }

        async fn shutdown(&self) -> Result<(), StatsigErr> {
            Ok(())
        }

        fn should_schedule_background_flush(&self) -> bool {
            false
        }
    }

    #[test]
    fn released_token_churn_keeps_history_bounded() {
        let store = small_store();
        for _ in 0..100 {
            let token = insert_layer(&store);
            assert!(store.release(&token));
            let inner = store.inner.lock();
            assert!(inner.entries.is_empty());
            assert!(inner.insertion_order.len() <= 2 * store.max_tokens);
            assert_eq!(inner.evicted, 0);
        }
        assert_eq!(store.inner.lock().released, 100);
    }

    #[tokio::test]
    async fn consumed_token_churn_keeps_history_bounded_and_logs_once() {
        let store = small_store();
        let adapter = Arc::new(CountingEventAdapter::default());
        let logging_adapter: Arc<dyn EventLoggingAdapter> = adapter.clone();
        let runtime = StatsigRuntime::get_runtime();
        let logger = EventLogger::new(
            "secret-delayed-exposure-test",
            &Arc::new(StatsigOptions::default()),
            &logging_adapter,
            &runtime,
        );

        for _ in 0..100 {
            let prepared = logger
                .prepare_event(EnqueuePassthroughOp {
                    event: StatsigEventInternal::new(
                        0,
                        StatsigUserLoggable::default(),
                        StatsigEvent {
                            event_name: "delayed_test_event".to_string(),
                            value: None,
                            metadata: None,
                            statsig_metadata: None,
                        },
                        None,
                    ),
                })
                .unwrap();
            let token = store.insert_prepared(prepared);
            assert!(store.log_delayed_exposure(&token, &logger));
            assert!(!store.log_delayed_exposure(&token, &logger));
            let inner = store.inner.lock();
            assert!(inner.entries.is_empty());
            assert!(inner.insertion_order.len() <= 2 * store.max_tokens);
            assert_eq!(inner.evicted, 0);
        }

        logger.flush_all_pending_events().await.unwrap();
        assert_eq!(adapter.0.load(Ordering::Relaxed), 100);
        assert_eq!(store.inner.lock().consumed, 100);
        runtime.shutdown();
    }

    #[test]
    fn compaction_preserves_live_tokens_and_oldest_active_eviction() {
        let store = small_store();
        let oldest = insert_layer(&store);
        let removed = insert_layer(&store);
        let retained = insert_layer(&store);
        assert!(store.release(&removed));

        for _ in 0..100 {
            let token = insert_layer(&store);
            assert!(store.release(&token));
            let inner = store.inner.lock();
            assert!(inner.entries.contains_key(&oldest));
            assert!(inner.entries.contains_key(&retained));
            assert!(inner.insertion_order.len() <= 2 * store.max_tokens);
        }

        let third = insert_layer(&store);
        let fourth = insert_layer(&store);
        let fifth = insert_layer(&store);
        let inner = store.inner.lock();
        assert!(!inner.entries.contains_key(&oldest));
        assert!(!inner.entries.contains_key(&removed));
        assert_eq!(inner.entries.len(), store.max_tokens);
        assert_eq!(inner.evicted, 1);
        let live_order: Vec<_> = inner
            .insertion_order
            .iter()
            .filter(|token| inner.entries.contains_key(*token))
            .collect();
        assert_eq!(live_order, vec![&retained, &third, &fourth, &fifth]);
    }

    #[test]
    fn clear_drops_active_and_stale_history() {
        let store = small_store();
        let active = insert_layer(&store);
        let released = insert_layer(&store);
        assert!(store.release(&released));
        store.clear();
        {
            let inner = store.inner.lock();
            assert!(inner.entries.is_empty());
            assert!(inner.insertion_order.is_empty());
        }
        assert!(!store.release(&active));
        assert!(store.release(&insert_layer(&store)));
    }

    #[test]
    fn empty_store_stats_are_zero() {
        let store = DelayedExposureStore::default();
        let inner = store.inner.lock();
        assert_eq!(
            DelayedExposureStore::stats(&inner),
            DelayedExposureStoreStats {
                active_tokens: 0,
                insertion_order_tokens: 0,
                stale_insertion_order_tokens: 0,
            }
        );
    }

    #[test]
    fn metrics_snapshots_are_throttled() {
        let store = DelayedExposureStore::default();
        let mut inner = store.inner.lock();
        let start = Instant::now();
        let expected = DelayedExposureStoreStats {
            active_tokens: 0,
            insertion_order_tokens: 0,
            stale_insertion_order_tokens: 0,
        };

        assert_eq!(
            DelayedExposureStore::take_metrics_snapshot_if_due(&mut inner, start),
            Some(expected)
        );
        assert_eq!(
            DelayedExposureStore::take_metrics_snapshot_if_due(
                &mut inner,
                start + Duration::from_secs(9),
            ),
            None
        );
        assert_eq!(
            DelayedExposureStore::take_metrics_snapshot_if_due(
                &mut inner,
                start + METRICS_EMIT_INTERVAL,
            ),
            Some(expected)
        );
    }
}
