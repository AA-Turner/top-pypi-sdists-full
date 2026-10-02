//! Port of `software.amazon.kinesis.worker.metricstats.WorkerMetricStatsManager`.
//!
//! In-process periodic sampler capturing each configured
//! [`WorkerMetric`](crate::worker::metric::WorkerMetric)'s raw value into a
//! bounded ring buffer, exposing [`compute_metrics`](WorkerMetricStatsManager::compute_metrics)
//! / [`get_operating_range`](WorkerMetricStatsManager::get_operating_range) to
//! flush/average that buffer.
//!
//! # Concurrency deviation
//! Java uses a single-thread daemon `ScheduledExecutorService` with
//! `scheduleWithFixedDelay` + random jitter. The port uses a **std background
//! thread** (daemon-equivalent; no tokio runtime required, matching the Java
//! tests that drive the manager from plain threads) with a `sleep`-loop
//! (fixed-delay: sleep is measured after each run) and a random initial jitter.
//! The two `EvictingQueue`s become [`VecDeque`] ring buffers; the raw
//! high-frequency queue is a `Mutex<VecDeque<f64>>` per metric (Guava
//! `synchronizedQueue`), and `compute_metrics` is serialized via a `Mutex`
//! (Java's `synchronized` method).

use std::collections::HashMap;
use std::collections::VecDeque;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use crate::metrics::{metrics_util, MetricsFactory, MetricsLevel};
use crate::worker::metric::WorkerMetric;

pub(crate) const METRICS_IN_MEMORY_REPORTER_FAILURE: &str = "InMemoryMetricStatsReporterFailure";
const METRICS_OPERATION_WORKER_STATS_REPORTER: &str = "WorkerMetricStatsReporter";
const HIGH_FREQUENCY_STATS_COUNT: usize = 300;
const DEFAULT_AVERAGE_VALUES_DIGIT_AFTER_DECIMAL: u32 = 6;

/// Round to `scale` decimal places, half-up (Java
/// `BigDecimal.setScale(scale, RoundingMode.HALF_UP)`).
fn round_half_up(value: f64, scale: u32) -> f64 {
    if !value.is_finite() {
        return value;
    }
    let factor = 10f64.powi(scale as i32);
    let scaled = value * factor;
    // Round half away from zero (HALF_UP applies to the magnitude in Java's
    // BigDecimal; for non-negative metric values this equals round-half-up).
    let rounded = if scaled >= 0.0 {
        (scaled + 0.5).floor()
    } else {
        (scaled - 0.5).ceil()
    };
    rounded / factor
}

/// A bounded ring buffer (Guava `EvictingQueue`): dropping the oldest element on
/// overflow.
#[derive(Debug)]
struct EvictingQueue {
    max_size: usize,
    inner: VecDeque<f64>,
}

impl EvictingQueue {
    fn new(max_size: usize) -> Self {
        Self {
            max_size,
            inner: VecDeque::new(),
        }
    }
    fn add(&mut self, value: f64) {
        if self.max_size == 0 {
            return;
        }
        if self.inner.len() == self.max_size {
            self.inner.pop_front();
        }
        self.inner.push_back(value);
    }
    fn drain(&mut self) -> Vec<f64> {
        self.inner.drain(..).collect()
    }
    fn snapshot(&self) -> Vec<f64> {
        self.inner.iter().copied().collect()
    }
    #[cfg(test)]
    fn len(&self) -> usize {
        self.inner.len()
    }
}

struct Inner {
    /// Per-metric trailing (maxMetricStatsCount) computed averages.
    computed_average_metrics: HashMap<usize, EvictingQueue>,
    /// Per-metric raw high-frequency samples (Guava synchronizedQueue).
    raw_high_freq: HashMap<usize, Mutex<EvictingQueue>>,
}

/// The periodic worker-metric sampler.
pub struct WorkerMetricStatsManager {
    worker_metric_list: Vec<Arc<dyn WorkerMetric>>,
    inner: Mutex<Inner>,
    in_memory_stats_capture_thread_frequency_millis: u64,
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    running: Arc<AtomicBool>,
    join_handle: Mutex<Option<std::thread::JoinHandle<()>>>,
}

impl WorkerMetricStatsManager {
    /// Construct the manager (Java constructor).
    pub fn new(
        max_metric_stats_count: usize,
        worker_metric_list: Vec<Arc<dyn WorkerMetric>>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        in_memory_stats_capture_thread_frequency_millis: u64,
    ) -> Arc<Self> {
        let mut computed_average_metrics = HashMap::new();
        let mut raw_high_freq = HashMap::new();
        for (idx, _) in worker_metric_list.iter().enumerate() {
            computed_average_metrics.insert(idx, EvictingQueue::new(max_metric_stats_count));
            raw_high_freq.insert(
                idx,
                Mutex::new(EvictingQueue::new(HIGH_FREQUENCY_STATS_COUNT)),
            );
        }
        tracing::info!(
            "Completed initialization with maxMetricStatsCount : {} and total WorkerMetricStats : {}",
            max_metric_stats_count,
            worker_metric_list.len()
        );
        Arc::new(Self {
            worker_metric_list,
            inner: Mutex::new(Inner {
                computed_average_metrics,
                raw_high_freq,
            }),
            in_memory_stats_capture_thread_frequency_millis,
            metrics_factory,
            running: Arc::new(AtomicBool::new(false)),
            join_handle: Mutex::new(None),
        })
    }

    /// Start the background sampler (Java `startManager`), with a random initial
    /// jitter delay.
    pub fn start_manager(self: &Arc<Self>) {
        if self.running.swap(true, Ordering::SeqCst) {
            return;
        }
        let this = Arc::clone(self);
        let freq = self.in_memory_stats_capture_thread_frequency_millis;
        // Jitter in [0, freq).
        let jitter = if freq > 0 {
            rand::random::<u64>() % freq
        } else {
            0
        };
        tracing::info!(
            "Started manager process with {} ms initial delay...",
            jitter
        );
        let handle = std::thread::Builder::new()
            .name("worker-metrics-manager".to_string())
            .spawn(move || {
                std::thread::sleep(Duration::from_millis(jitter));
                while this.running.load(Ordering::SeqCst) {
                    this.record_worker_metrics();
                    std::thread::sleep(Duration::from_millis(freq));
                }
            })
            .expect("failed to spawn worker-metrics-manager thread");
        *self.join_handle.lock().unwrap() = Some(handle);
    }

    /// Stop the background sampler (Java `stopManager`).
    pub fn stop_manager(&self) {
        self.running.store(false, Ordering::SeqCst);
        if let Some(handle) = self.join_handle.lock().unwrap().take() {
            let _ = handle.join();
        }
    }

    fn record_worker_metrics(&self) {
        for (idx, worker_metric) in self.worker_metric_list.iter().enumerate() {
            if let Some(value) = self.fetch_worker_metrics_value(worker_metric.as_ref()) {
                let inner = self.inner.lock().unwrap_or_else(|e| e.into_inner());
                if let Some(queue) = inner.raw_high_freq.get(&idx) {
                    queue.lock().unwrap_or_else(|e| e.into_inner()).add(value);
                }
            }
        }
    }

    fn fetch_worker_metrics_value(&self, worker_metric: &dyn WorkerMetric) -> Option<f64> {
        // Java catches Throwable per-metric; a panic in capture() is caught here
        // to keep the sampler alive (mirrors the broad catch).
        let result =
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| worker_metric.capture()));
        match result {
            Ok(value) => Some(value.value()),
            Err(_) => {
                tracing::error!(
                    "WorkerMetricStats {} failure",
                    worker_metric.worker_metric_type().name()
                );
                let mut scope = metrics_util::create_metrics_with_operation(
                    self.metrics_factory.as_ref(),
                    METRICS_OPERATION_WORKER_STATS_REPORTER,
                );
                scope.add_data_with_level(
                    METRICS_IN_MEMORY_REPORTER_FAILURE,
                    1.0,
                    aws_sdk_cloudwatch::types::StandardUnit::Count,
                    MetricsLevel::Summary,
                );
                metrics_util::end_scope(scope.as_mut());
                None
            }
        }
    }

    /// Drain + average the raw queues into the rolling history (Java
    /// `computeMetrics`, `synchronized`). Empty queue => `-1.0` (failure sentinel).
    pub fn compute_metrics(&self) -> HashMap<String, Vec<f64>> {
        let mut inner = self.inner.lock().unwrap_or_else(|e| e.into_inner());
        let mut result = HashMap::new();
        // Collect keys first to avoid borrow conflicts.
        let indices: Vec<usize> = inner.raw_high_freq.keys().copied().collect();
        for idx in indices {
            let current: Vec<f64> = {
                let queue = inner.raw_high_freq.get(&idx).unwrap();
                queue.lock().unwrap_or_else(|e| e.into_inner()).drain()
            };
            let computed = inner.computed_average_metrics.get_mut(&idx).unwrap();
            if current.is_empty() {
                computed.add(-1.0);
            } else {
                computed.add(compute_average(&current));
            }
            let short_name = self.worker_metric_list[idx].short_name();
            result.insert(short_name, computed.snapshot());
        }
        result
    }

    /// The operating range per metric (Java `getOperatingRange`), recomputed
    /// fresh each call. Single-element list `[maxUtilization]`.
    pub fn get_operating_range(&self) -> HashMap<String, Vec<i64>> {
        let mut operating_range = HashMap::new();
        for worker_metric in &self.worker_metric_list {
            operating_range.insert(
                worker_metric.short_name(),
                vec![worker_metric.operating_range().max_utilization() as i64],
            );
        }
        operating_range
    }

    /// Test accessor: number of raw high-freq samples for metric index `idx`.
    #[cfg(test)]
    pub(crate) fn raw_high_freq_len(&self, idx: usize) -> usize {
        let inner = self.inner.lock().unwrap_or_else(|e| e.into_inner());
        inner
            .raw_high_freq
            .get(&idx)
            .map(|q| q.lock().unwrap_or_else(|e| e.into_inner()).len())
            .unwrap_or(0)
    }

    /// Test accessor: snapshot of raw high-freq samples for metric index `idx`.
    #[cfg(test)]
    pub(crate) fn raw_high_freq_snapshot(&self, idx: usize) -> Vec<f64> {
        let inner = self.inner.lock().unwrap_or_else(|e| e.into_inner());
        inner
            .raw_high_freq
            .get(&idx)
            .map(|q| q.lock().unwrap_or_else(|e| e.into_inner()).snapshot())
            .unwrap_or_default()
    }
}

/// Simple mean of the values, rounded HALF_UP to 6 decimals (Java
/// `computeAverage`).
fn compute_average(values: &[f64]) -> f64 {
    if values.is_empty() {
        return 0.0;
    }
    let sum: f64 = values.iter().sum();
    let average = sum / values.len() as f64;
    round_half_up(average, DEFAULT_AVERAGE_VALUES_DIGIT_AFTER_DECIMAL)
}

#[cfg(test)]
mod tests;
