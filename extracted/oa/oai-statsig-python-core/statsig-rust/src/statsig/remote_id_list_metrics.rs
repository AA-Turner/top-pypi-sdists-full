use std::collections::HashMap;
use std::sync::Arc;
use std::sync::atomic::{AtomicU32, Ordering};
use std::time::{Duration, Instant};

use crate::StatsigOptions;
use crate::id_lists_adapter::membership_client::{MembershipAnswer, MembershipLookupError};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;

pub(super) struct RemoteIdListMetrics {
    observer: Option<Arc<OpsStatsForInstance>>,
}

impl RemoteIdListMetrics {
    pub(super) fn new(options: &StatsigOptions, ops: &Arc<OpsStatsForInstance>) -> Self {
        Self {
            observer: options
                .active_observability_client()
                .map(|_| Arc::clone(ops)),
        }
    }

    pub(super) fn is_enabled(&self) -> bool {
        self.observer.is_some()
    }

    fn record_count(&self, list: &str, result: &str, count: u32) {
        let Some(observer) = &self.observer else {
            return;
        };
        if count == 0 {
            return;
        }
        observer.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            "id_list_membership_lookup".into(),
            f64::from(count),
            Some(HashMap::from([
                ("mode".into(), "compare".into()),
                ("result".into(), result.into()),
                ("list".into(), list.into()),
            ])),
        ));
    }

    pub(super) fn record_cache_miss(
        &self,
        list: &str,
        local: Option<bool>,
        remote: Option<Option<bool>>,
    ) {
        let result = match remote {
            None => "local_fallback_pending",
            Some(None) => "local_fallback_unavailable",
            Some(Some(member)) => comparison(local, member),
        };
        self.record_count(list, "cache_miss", 1);
        self.record_count(list, result, 1);
    }

    pub(super) fn record_cache_hit(
        &self,
        list: &str,
        local_membership: Option<bool>,
        member: bool,
    ) {
        self.record_count(list, "cache_hit", 1);
        self.record_count(list, comparison(local_membership, member), 1);
    }

    pub(super) fn record_completed_fallbacks(
        &self,
        list: &str,
        checks: &LocalFallbackCounts,
        member: bool,
    ) {
        if !self.is_enabled() {
            return;
        }
        let hits = checks.hits.swap(0, Ordering::AcqRel);
        let misses = checks.misses.swap(0, Ordering::AcqRel);
        let missing = checks.missing.swap(0, Ordering::AcqRel);
        let (matches, mismatches) = if member {
            (hits, misses)
        } else {
            (misses, hits)
        };
        self.record_count(list, "before_ready_match", matches);
        self.record_count(list, "before_ready_mismatch", mismatches);
        self.record_count(list, "before_ready_local_missing", missing);
    }

    pub(super) fn rpc_start(&self) -> Option<Instant> {
        self.observer.as_ref().map(|_| Instant::now())
    }

    pub(super) fn record_rpc_latency(&self, list: &str, elapsed: Option<Duration>, outcome: &str) {
        let (Some(observer), Some(elapsed)) = (&self.observer, elapsed) else {
            return;
        };
        observer.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            "id_list_membership_rpc_latency_ms".into(),
            elapsed.as_secs_f64() * 1000.0,
            Some(HashMap::from([
                ("operation".into(), "on_demand".into()),
                ("list".into(), list.into()),
                ("result".into(), outcome.into()),
            ])),
        ));
    }
}

pub(super) fn rpc_result_label(
    result: &Result<Option<MembershipAnswer>, MembershipLookupError>,
) -> &'static str {
    match result {
        Ok(Some(_)) => "answered",
        Ok(None) => "unknown",
        Err(MembershipLookupError::Unavailable) => "unavailable",
        Err(MembershipLookupError::Rejected) => "rejected",
    }
}

fn comparison(local_membership: Option<bool>, member: bool) -> &'static str {
    match local_membership {
        Some(local) if local == member => "ready_match",
        Some(_) => "ready_mismatch",
        None => "ready_local_missing",
    }
}

/// Local outcomes to compare when this lookup's SFP response arrives.
#[derive(Default)]
pub(super) struct LocalFallbackCounts {
    hits: AtomicU32,
    misses: AtomicU32,
    missing: AtomicU32,
}

impl LocalFallbackCounts {
    pub(super) fn add(&self, local_membership: Option<bool>) {
        let count = match local_membership {
            Some(true) => &self.hits,
            Some(false) => &self.misses,
            None => &self.missing,
        };
        // If completion drained first, acquire its published answer before rechecking it.
        let _ = count.fetch_update(Ordering::AcqRel, Ordering::Relaxed, |n| {
            Some(n.saturating_add(1))
        });
    }
}

#[cfg(test)]
#[path = "__tests__/remote_id_list_metrics_tests.rs"]
mod tests;
