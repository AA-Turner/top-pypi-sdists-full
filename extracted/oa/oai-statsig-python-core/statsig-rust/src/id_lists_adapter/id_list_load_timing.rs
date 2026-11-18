//! Load latency diagnostics for the SDK's configured observer. Store phases
//! are nested in parse_publish; concurrent lists must not be summed into batch time.
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance};
use crate::{StatsigErr, StatsigOptions};
use parking_lot::Mutex;
use std::collections::HashMap;
use std::future::Future;
use std::sync::Arc;
use std::time::{Duration, Instant};

/// Resolve once on the adapter, using the same output policy as observer registration.
/// Only the lazy-load path uses these diagnostics; eager init/polling keeps its own metrics.
pub(crate) fn collection_enabled(options: Option<&StatsigOptions>) -> bool {
    !crate::output_policy::OutputPolicy::from_options(options).is_silent()
        && options
            .and_then(|o| o.observability_client.as_ref())
            .and_then(std::sync::Weak::upgrade)
            .is_some()
}

#[derive(Clone, Copy)]
pub(crate) enum Phase {
    DownloadPermitWait,
    BuildPermitWait,
    BuildWorkerWait,
    PublicationWorkerWait,
    AdapterLockWait,
    HttpBody,
    Decode,
    ParsePublish,
    StoreLockWait,
    Processing,
    Publication,
}
const PHASES: [(Phase, &str); 8] = [
    (Phase::DownloadPermitWait, "download_permit_wait"),
    (Phase::BuildPermitWait, "build_permit_wait"),
    (Phase::BuildWorkerWait, "build_worker_wait"),
    (Phase::PublicationWorkerWait, "publication_worker_wait"),
    (Phase::AdapterLockWait, "adapter_lock_wait"),
    (Phase::HttpBody, "http_body"),
    (Phase::Decode, "decode"),
    (Phase::ParsePublish, "parse_publish"),
];
const STORE_PHASES: [(Phase, &str); 3] = [
    (Phase::StoreLockWait, "store_lock_wait"),
    (Phase::Processing, "processing"),
    (Phase::Publication, "publication"),
];
const PHASE_COUNT: usize = PHASES.len() + STORE_PHASES.len();
pub(crate) const LIST_PHASE_METRIC: &str = "lazy_id_list_load.list_phase_ms";
pub(crate) const STORE_PHASE_METRIC: &str = "lazy_id_list_load.store_phase_ms";

tokio::task_local! {
    // One context per actual singleflight owner, shared only with its workers.
    // The mutex protects duration additions, never SDK work or observer delivery.
    static TIMINGS_CONTEXT: Arc<Mutex<[Option<Duration>; PHASE_COUNT]>>;
}
pub(crate) fn start_phase() -> Option<Instant> {
    TIMINGS_CONTEXT.try_with(|_| Instant::now()).ok()
}
pub(crate) fn end_phase(phase: Phase, started: Option<Instant>) {
    if let Some(started) = started {
        let elapsed = started.elapsed();
        let _ = TIMINGS_CONTEXT
            .try_with(|t| *t.lock()[phase as usize].get_or_insert(Duration::ZERO) += elapsed);
    }
}
pub(crate) fn measure<T>(phase: Phase, operation: impl FnOnce() -> T) -> T {
    let started = start_phase();
    let result = operation();
    end_phase(phase, started);
    result
}
/// Tokio task locals do not follow spawn_blocking; scope the captured context
/// to this callback so it cannot leak to subsequent work on the same thread.
pub(crate) fn with_current_timings<T>(
    phase: Phase,
    operation: impl FnOnce() -> T,
) -> impl FnOnce() -> T {
    let timings = TIMINGS_CONTEXT.try_with(Arc::clone).ok();
    let queued = timings.as_ref().map(|_| Instant::now());
    move || match timings {
        Some(timings) => TIMINGS_CONTEXT.sync_scope(timings, || {
            end_phase(phase, queued);
            operation()
        }),
        None => operation(),
    }
}

/// Internal payload for the existing OpsStats queue. Only the observer expands
/// phases into metrics/tags; list waiters never wait for that loop or callbacks.
#[doc(hidden)]
pub struct IdListLoadSummary {
    name: String,
    outcome: &'static str,
    total: Duration,
    phases: [Option<Duration>; PHASE_COUNT],
}

impl IdListLoadSummary {
    pub(crate) fn for_each_metric(
        &self,
        mut tags: HashMap<String, String>,
        mut emit: impl FnMut(&'static str, f64, HashMap<String, String>),
    ) {
        tags.extend([
            ("list_name".into(), self.name.clone()),
            ("mode".into(), "lazy".into()),
            ("outcome".into(), self.outcome.into()),
        ]);
        let mut phase_metric = |metric: &'static str, phase: &str, elapsed: Duration| {
            tags.insert("phase".into(), phase.into());
            emit(metric, elapsed.as_secs_f64() * 1000.0, tags.clone());
        };
        for (metric, definitions) in [
            (LIST_PHASE_METRIC, PHASES.as_slice()),
            (STORE_PHASE_METRIC, STORE_PHASES.as_slice()),
        ] {
            for &(phase, label) in definitions {
                // Missing means this path did not reach an instrumented stage.
                if let Some(elapsed) = self.phases[phase as usize] {
                    phase_metric(metric, label, elapsed);
                }
            }
        }
        let other = self.total.saturating_sub(
            PHASES
                .iter()
                .map(|(p, _)| self.phases[*p as usize].unwrap_or_default())
                .sum(),
        );
        for (phase, elapsed) in [("other", other), ("total", self.total)] {
            phase_metric(LIST_PHASE_METRIC, phase, elapsed);
        }
    }
}

/// Called inside the OnceCell initializer: coalesced callers share one summary,
/// retries accumulate into it, and a cancelled owner leaves no partial sample.
/// A new initializer after cancellation gets a fresh context. `Ok(false)` means
/// the first plan found the list ready, so this was not a cold load.
pub(crate) async fn time_list_load(
    ops: &OpsStatsForInstance,
    name: &str,
    enabled: bool,
    load: impl Future<Output = Result<bool, StatsigErr>>,
) -> Result<(), StatsigErr> {
    if !enabled {
        return load.await.map(|_| ());
    }
    let started = Instant::now();
    let timings = Arc::new(Mutex::new([None; PHASE_COUNT]));
    let result = TIMINGS_CONTEXT.scope(Arc::clone(&timings), load).await;
    let total = started.elapsed();
    if !matches!(result, Ok(false)) {
        // One compact message, no per-phase allocation/queueing on the load path.
        // try_log never invokes a scoped observer or synchronous log provider.
        ops.try_log(OpsStatsEvent::IdListLoad(Arc::new(IdListLoadSummary {
            name: name.to_owned(),
            outcome: if result.is_ok() { "success" } else { "error" },
            total,
            phases: *timings.lock(),
        })));
    }
    result.map(|_| ())
}

#[cfg(test)]
pub(crate) fn metrics_for_test(event: OpsStatsEvent) -> Vec<ObservabilityEvent> {
    match event {
        OpsStatsEvent::Observability(event) => vec![event],
        OpsStatsEvent::IdListLoad(summary) => {
            let mut events = Vec::new();
            summary.for_each_metric(HashMap::new(), |metric, value, tags| {
                events.push(ObservabilityEvent {
                    metric_type: MetricType::Dist,
                    metric_name: metric.to_owned(),
                    value,
                    tags: Some(tags),
                })
            });
            events
        }
        _ => Vec::new(),
    }
}

pub(crate) fn record_duration(
    ops: &OpsStatsForInstance,
    metric: &str,
    duration: Duration,
    outcome: &str,
) {
    ops.log(ObservabilityEvent::new_event(
        MetricType::Dist,
        metric.to_owned(),
        duration.as_secs_f64() * 1000.0,
        Some(HashMap::from([
            ("mode".into(), "lazy".into()),
            ("outcome".into(), outcome.into()),
        ])),
    ));
}
