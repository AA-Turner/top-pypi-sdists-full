//! Port of `software.amazon.kinesis.worker.metric.impl.linux.LinuxNetworkWorkerMetricBase`.
//!
//! Shared implementation for the Linux network bandwidth metrics. Rust has no
//! inheritance, so the base is a concrete struct parameterized by its
//! [`WorkerMetricType`] (NETWORK_IN vs NETWORK_OUT); the concrete
//! [`LinuxNetworkInWorkerMetric`](super::LinuxNetworkInWorkerMetric) /
//! [`LinuxNetworkOutWorkerMetric`](super::LinuxNetworkOutWorkerMetric) newtypes
//! wrap it.

use std::sync::Mutex;

use super::stopwatch::Stopwatch;
#[cfg(test)]
use super::stopwatch::Ticker;
use crate::worker::metric::{OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue};

pub(crate) const DEFAULT_NETWORK_STAT_FILE: &str = "/proc/net/dev";
pub(crate) const DEFAULT_INTERFACE_NAME: &str = "eth0";

/// Base network worker metric. Parses `/proc/net/dev` for a named interface's
/// cumulative RX/TX byte counters, computes bytes/sec via elapsed wall time,
/// converts to MBps, and normalizes against a configured max bandwidth.
///
/// Uses an **instance-level** lock (unlike the CPU metrics' static locks —
/// preserved from Java). First `capture()` returns `0.0` (no baseline). Missing
/// file / interface / parse error **panics** (Java `IllegalArgumentException`).
#[derive(Debug)]
pub struct LinuxNetworkWorkerMetricBase {
    metric_type: WorkerMetricType,
    operating_range: OperatingRange,
    interface_name: String,
    stat_file: String,
    max_bandwidth_in_mbps: f64,
    // Guava Stopwatch + instance-level lock (guards lastRx/lastTx + stopwatch).
    inner: Mutex<Inner>,
}

#[derive(Debug)]
struct Inner {
    stopwatch: Stopwatch,
    last_rx: i64,
    last_tx: i64,
}

impl LinuxNetworkWorkerMetricBase {
    /// Full constructor (Java public ctor). Panics if `max_bandwidth_in_mbps <= 0`
    /// (Java `IllegalArgumentException`, message
    /// `"maxBandwidthInMBps should be greater than 0."`).
    pub fn new(
        metric_type: WorkerMetricType,
        operating_range: OperatingRange,
        interface_name: impl Into<String>,
        stat_file: impl Into<String>,
        max_bandwidth_in_mbps: f64,
        stopwatch: Stopwatch,
    ) -> Self {
        // Faithful to Java `checkArgument(maxBandwidthInMBps > 0)`: throw when
        // NOT `> 0` (also covers NaN, which Java `> 0` treats as false).
        #[allow(clippy::neg_cmp_op_on_partial_ord)]
        if !(max_bandwidth_in_mbps > 0.0) {
            panic!("maxBandwidthInMBps should be greater than 0.");
        }
        Self {
            metric_type,
            operating_range,
            interface_name: interface_name.into(),
            stat_file: stat_file.into(),
            max_bandwidth_in_mbps,
            inner: Mutex::new(Inner {
                stopwatch,
                last_rx: -1,
                last_tx: -1,
            }),
        }
    }

    fn capture_value(&self) -> f64 {
        let bytes = self.calculate_network_usage_for_type();
        let mbps = self.convert_to_mbps(bytes);
        let percentage = mbps / self.max_bandwidth_in_mbps * 100.0;
        (100.0f64).min(percentage)
    }

    fn convert_to_mbps(&self, bytes: i64) -> f64 {
        let mut inner = self.inner.lock().unwrap_or_else(|e| e.into_inner());
        let elapsed_time_in_second = if !inner.stopwatch.is_running() {
            // First request: assume 1 second (bytes diff is 0 anyway).
            1.0
        } else {
            inner.stopwatch.elapsed_nanos() as f64 / 1_000_000_000.0
        };
        inner.stopwatch.reset().start();
        let total_data_mb = bytes as f64 / (1024.0 * 1024.0);
        if elapsed_time_in_second == 0.0 {
            panic!("elapsedTimeInSecond is zero which in incorrect");
        }
        total_data_mb / elapsed_time_in_second
    }

    /// Returns the diff bytes for this instance's metric type. Reads/parses
    /// `/proc/net/dev` and updates lastRx/lastTx under the instance lock.
    fn calculate_network_usage_for_type(&self) -> i64 {
        let (diff_rx, diff_tx) = self.calculate_network_usage();
        match self.metric_type {
            WorkerMetricType::NetworkIn => diff_rx,
            WorkerMetricType::NetworkOut => diff_tx,
            _ => unreachable!("network base only used for NETWORK_IN/NETWORK_OUT"),
        }
    }

    fn calculate_network_usage(&self) -> (i64, i64) {
        if !std::path::Path::new(&self.stat_file).exists() {
            panic!(
                "NetworkWorkerMetrics is not configured properly, file : {} does not exists",
                self.stat_file
            );
        }
        let content = match std::fs::read_to_string(&self.stat_file) {
            Ok(c) => c,
            Err(_) => panic!("Cannot read/parse {}", self.stat_file),
        };

        let mut lines = content.lines();
        // Skip 2 header lines.
        lines.next();
        lines.next();

        // Find the interface row: matches `^\s*<iface>:.*`.
        let prefix = format!("{}:", self.interface_name);
        let iface_line = lines.find(|l| l.trim_start().starts_with(&prefix));
        let line = match iface_line {
            Some(l) => l,
            None => panic!(
                "Failed to parse the file and find interface : {}",
                self.interface_name
            ),
        };

        // Substring after the first ':' then split on whitespace.
        let n = line.find(':').unwrap() + 1;
        let rest = line[n..].trim();
        let parts: Vec<&str> = rest.split_whitespace().collect();
        let rx: i64 = parts[0].parse().expect("invalid rx bytes");
        let tx: i64 = parts[8].parse().expect("invalid tx bytes");

        let mut inner = self.inner.lock().unwrap_or_else(|e| e.into_inner());
        let (diff_rx, diff_tx) = if inner.last_rx == -1 {
            (0, 0)
        } else {
            ((rx - inner.last_rx).abs(), (tx - inner.last_tx).abs())
        };
        inner.last_rx = rx;
        inner.last_tx = tx;
        (diff_rx, diff_tx)
    }
}

impl WorkerMetric for LinuxNetworkWorkerMetricBase {
    fn short_name(&self) -> String {
        self.metric_type.short_name().to_string()
    }

    fn capture(&self) -> WorkerMetricValue {
        WorkerMetricValue::builder()
            .value(self.capture_value())
            .build()
    }

    fn operating_range(&self) -> OperatingRange {
        self.operating_range
    }

    fn worker_metric_type(&self) -> WorkerMetricType {
        self.metric_type
    }
}

// The base's `calculate_network_usage` is intentionally called once per capture
// even though it computes both directions (matches Java's inefficiency where
// each In/Out instance re-reads the file independently).

/// Test-only accessor used by the network unit test to build a stopwatch with a
/// controlled ticker.
#[cfg(test)]
pub(crate) fn mocked_stopwatch(tick_millis: i64) -> Stopwatch {
    Stopwatch::create_unstarted(Ticker::one_second_style(tick_millis))
}
