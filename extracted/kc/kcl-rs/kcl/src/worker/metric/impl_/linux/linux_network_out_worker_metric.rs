//! Port of `software.amazon.kinesis.worker.metric.impl.linux.LinuxNetworkOutWorkerMetric`.

use super::linux_network_worker_metric_base::{
    LinuxNetworkWorkerMetricBase, DEFAULT_INTERFACE_NAME, DEFAULT_NETWORK_STAT_FILE,
};
use super::stopwatch::{Stopwatch, Ticker};
use crate::worker::metric::{OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue};

/// Concrete NETWORK_OUT metric (thin wrapper over
/// [`LinuxNetworkWorkerMetricBase`]).
#[derive(Debug)]
pub struct LinuxNetworkOutWorkerMetric {
    base: LinuxNetworkWorkerMetricBase,
}

impl LinuxNetworkOutWorkerMetric {
    /// Full constructor with an explicit interface name, stat file and stopwatch
    /// (Java `@VisibleForTesting` ctor).
    pub fn new(
        operating_range: OperatingRange,
        interface_name: impl Into<String>,
        stat_file: impl Into<String>,
        max_bandwidth_in_mb: f64,
        stopwatch: Stopwatch,
    ) -> Self {
        Self {
            base: LinuxNetworkWorkerMetricBase::new(
                WorkerMetricType::NetworkOut,
                operating_range,
                interface_name,
                stat_file,
                max_bandwidth_in_mb,
                stopwatch,
            ),
        }
    }

    /// Convenience constructor with an explicit interface, default stat file
    /// and a system-ticker stopwatch (Java public ctor).
    pub fn with_interface(
        operating_range: OperatingRange,
        interface_name: impl Into<String>,
        max_bandwidth_in_mb: f64,
    ) -> Self {
        Self::new(
            operating_range,
            interface_name,
            DEFAULT_NETWORK_STAT_FILE,
            max_bandwidth_in_mb,
            Stopwatch::create_unstarted(Ticker::system()),
        )
    }

    /// Convenience constructor with default interface (`eth0`) + stat file (Java
    /// public ctor).
    pub fn with_defaults(operating_range: OperatingRange, max_bandwidth_in_mb: f64) -> Self {
        Self::with_interface(operating_range, DEFAULT_INTERFACE_NAME, max_bandwidth_in_mb)
    }
}

impl WorkerMetric for LinuxNetworkOutWorkerMetric {
    fn short_name(&self) -> String {
        self.base.short_name()
    }
    fn capture(&self) -> WorkerMetricValue {
        self.base.capture()
    }
    fn operating_range(&self) -> OperatingRange {
        self.base.operating_range()
    }
    fn worker_metric_type(&self) -> WorkerMetricType {
        self.base.worker_metric_type()
    }
}
