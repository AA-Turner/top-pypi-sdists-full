//! Port of `software.amazon.kinesis.worker.metric.WorkerMetricType`.

/// The supported worker-metric kinds and their DDB/short-name codes.
///
/// Note the `THROUGHPUT` asymmetry preserved from Java: it has no `WorkerMetric`
/// implementation, and `WorkerMetricStats::is_using_default_worker_metric`
/// checks the metricStats map for a key equal to the enum **name**
/// (`"THROUGHPUT"`, via [`WorkerMetricType::name`]) — NOT its short name
/// (`"T"`, via [`WorkerMetricType::short_name`]).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum WorkerMetricType {
    Cpu,
    Memory,
    NetworkIn,
    NetworkOut,
    Throughput,
}

impl WorkerMetricType {
    /// The short name used as the attribute/map key in storage (Java
    /// `getShortName`).
    pub fn short_name(&self) -> &'static str {
        match self {
            Self::Cpu => "C",
            Self::Memory => "M",
            Self::NetworkIn => "NI",
            Self::NetworkOut => "NO",
            Self::Throughput => "T",
        }
    }

    /// The Java enum constant name (`name()`), e.g. `"THROUGHPUT"`. Distinct
    /// from [`Self::short_name`] — see the type-level note.
    pub fn name(&self) -> &'static str {
        match self {
            Self::Cpu => "CPU",
            Self::Memory => "MEMORY",
            Self::NetworkIn => "NETWORK_IN",
            Self::NetworkOut => "NETWORK_OUT",
            Self::Throughput => "THROUGHPUT",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn short_names_match_java() {
        assert_eq!(WorkerMetricType::Cpu.short_name(), "C");
        assert_eq!(WorkerMetricType::Memory.short_name(), "M");
        assert_eq!(WorkerMetricType::NetworkIn.short_name(), "NI");
        assert_eq!(WorkerMetricType::NetworkOut.short_name(), "NO");
        assert_eq!(WorkerMetricType::Throughput.short_name(), "T");
    }

    #[test]
    fn names_differ_from_short_names() {
        assert_eq!(WorkerMetricType::Throughput.name(), "THROUGHPUT");
        assert_ne!(
            WorkerMetricType::Throughput.name(),
            WorkerMetricType::Throughput.short_name()
        );
    }
}
