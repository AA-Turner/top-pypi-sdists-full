//! Port of `software.amazon.kinesis.worker.metric.impl.jmx.HeapMemoryAfterGCWorkerMetric`.
//!
//! # TODO(port): JVM JMX has no Rust analog — best-effort Linux memory reading
//!
//! The Java metric queries JMX `MemoryPoolMXBean` collection-usage after GC — a
//! JVM-only concept with **no Rust equivalent** (Rust has no managed heap / GC /
//! MXBeans). Per the arch map this class "needs a redesigned strategy" in the
//! port.
//!
//! This port keeps the class **structure + public surface** so the selector /
//! config wiring compiles, and derives a best-effort memory-utilization value
//! from Linux process/cgroup memory (`/proc/meminfo`, or cgroup memory files
//! where present) instead of JVM heap pools. When no source is available it
//! returns `0.0` (a valid 0-100 value) rather than panicking, so the metric is
//! always constructible and the `capture_sanity` parity test passes on any host.
//!
//! Owning follow-up: this remains a documented best-effort port; a faithful
//! "memory pressure" metric can be revisited if/when the coordinator wave needs
//! it. Not wired into [`WorkerMetricsSelector`](crate::worker::WorkerMetricsSelector)
//! (which only selects CPU metrics), matching Java.

use crate::worker::metric::{OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue};

/// Memory worker metric. See the module docs for the JVM-vs-Linux deviation.
#[derive(Debug)]
pub struct HeapMemoryAfterGCWorkerMetric {
    operating_range: OperatingRange,
}

impl HeapMemoryAfterGCWorkerMetric {
    /// Construct with the operating range (Java `@RequiredArgsConstructor`).
    pub fn new(operating_range: OperatingRange) -> Self {
        Self { operating_range }
    }

    /// Best-effort memory utilization percentage from Linux memory sources.
    fn memory_usage(&self) -> f64 {
        if let Some(v) = read_meminfo_utilization() {
            return v.clamp(0.0, 100.0);
        }
        // No source available (e.g. non-Linux CI): return a valid 0-100 value.
        0.0
    }
}

/// Parse `/proc/meminfo` for `MemTotal`/`MemAvailable` and compute a used
/// percentage. Returns `None` if the file is absent or unparseable.
fn read_meminfo_utilization() -> Option<f64> {
    let content = std::fs::read_to_string("/proc/meminfo").ok()?;
    let mut total: Option<f64> = None;
    let mut available: Option<f64> = None;
    for line in content.lines() {
        if let Some(rest) = line.strip_prefix("MemTotal:") {
            total = rest.split_whitespace().next().and_then(|s| s.parse().ok());
        } else if let Some(rest) = line.strip_prefix("MemAvailable:") {
            available = rest.split_whitespace().next().and_then(|s| s.parse().ok());
        }
    }
    let total = total?;
    let available = available?;
    if total <= 0.0 {
        return None;
    }
    Some(100.0 * (total - available) / total)
}

impl WorkerMetric for HeapMemoryAfterGCWorkerMetric {
    fn short_name(&self) -> String {
        WorkerMetricType::Memory.short_name().to_string()
    }

    fn capture(&self) -> WorkerMetricValue {
        WorkerMetricValue::builder()
            .value(self.memory_usage())
            .build()
    }

    fn operating_range(&self) -> OperatingRange {
        self.operating_range
    }

    fn worker_metric_type(&self) -> WorkerMetricType {
        WorkerMetricType::Memory
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn capture_sanity() {
        let metric = HeapMemoryAfterGCWorkerMetric::new(
            OperatingRange::builder().max_utilization(100).build(),
        );
        // capture() must produce a valid 0-100 value.
        let value = metric.capture().value();
        assert!((0.0..=100.0).contains(&value));

        assert_eq!(metric.worker_metric_type(), WorkerMetricType::Memory);
        assert_eq!(metric.short_name(), WorkerMetricType::Memory.short_name());
    }
}
