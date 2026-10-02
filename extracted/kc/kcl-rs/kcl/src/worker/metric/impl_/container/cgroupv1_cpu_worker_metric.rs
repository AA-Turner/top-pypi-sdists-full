//! Port of `software.amazon.kinesis.worker.metric.impl.container.Cgroupv1CpuWorkerMetric`.

use std::sync::{Arc, Mutex};

use crate::utils::cgroup::{get_available_cpus_from_effective_cpu_set, read_single_line_file};
use crate::worker::metric::{
    Clock, OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue,
};

const CGROUP_ROOT: &str = "/sys/fs/cgroup/";

/// Shared static lock, mirroring the Java `private static final Object LOCK_OBJECT`
/// shared across all instances of `Cgroupv1CpuWorkerMetric`.
static LOCK_OBJECT: Mutex<()> = Mutex::new(());

/// CPU utilization on cgroup v1 systems, diffing cumulative CPU-core-nanoseconds
/// usage between `capture()` calls divided by the container's CPU-core quota.
///
/// First `capture()` returns `0.0`. Missing files / parse errors **panic** (Java
/// `IllegalArgumentException`).
#[derive(Debug)]
pub struct Cgroupv1CpuWorkerMetric {
    operating_range: OperatingRange,
    cpu_time_file: String,
    cfs_quota_file: String,
    cfs_period_file: String,
    effective_cpu_set_file: String,
    clock: Clock,
    // cpuLimit lazily computed once; -1 sentinel = unset (matches Java, computed
    // outside the lock).
    cpu_limit: Mutex<f64>,
    state: Mutex<Cgroupv1State>,
}

#[derive(Debug, Default)]
struct Cgroupv1State {
    last_cpu_use_time_nanos: i64,
    last_system_time_nanos: i64,
}

impl Cgroupv1CpuWorkerMetric {
    /// Full constructor (Java package-private ctor) with all file paths + clock.
    pub fn new(
        operating_range: OperatingRange,
        cpu_time_file: impl Into<String>,
        cfs_quota_file: impl Into<String>,
        cfs_period_file: impl Into<String>,
        effective_cpu_set_file: impl Into<String>,
        clock: Clock,
    ) -> Self {
        Self {
            operating_range,
            cpu_time_file: cpu_time_file.into(),
            cfs_quota_file: cfs_quota_file.into(),
            cfs_period_file: cfs_period_file.into(),
            effective_cpu_set_file: effective_cpu_set_file.into(),
            clock,
            cpu_limit: Mutex::new(-1.0),
            state: Mutex::new(Cgroupv1State::default()),
        }
    }

    /// Convenience constructor (Java public single-arg ctor) with default cgroup
    /// v1 paths and the system UTC clock.
    pub fn with_default_paths(operating_range: OperatingRange) -> Self {
        Self::new(
            operating_range,
            format!("{}cpu/cpuacct.usage", CGROUP_ROOT),
            format!("{}cpu/cpu.cfs_quota_us", CGROUP_ROOT),
            format!("{}cpu/cpu.cfs_period_us", CGROUP_ROOT),
            format!("{}cpuset/cpuset.effective_cpus", CGROUP_ROOT),
            Clock::system_utc(),
        )
    }

    fn calculate_cpu_limit(&self) -> f64 {
        let cfs_quota: i64 = read_single_line_file(&self.cfs_quota_file)
            .parse()
            .expect("invalid cfs_quota");
        let cfs_period: i64 = read_single_line_file(&self.cfs_period_file)
            .parse()
            .expect("invalid cfs_period");
        if cfs_quota == -1 {
            // No limit set; container can use all available cores.
            get_available_cpus_from_effective_cpu_set(&read_single_line_file(
                &self.effective_cpu_set_file,
            )) as f64
        } else {
            cfs_quota as f64 / cfs_period as f64
        }
    }

    fn calculate_cpu_usage(&self) -> f64 {
        {
            let mut limit = self.cpu_limit.lock().unwrap_or_else(|e| e.into_inner());
            if *limit == -1.0 {
                *limit = self.calculate_cpu_limit();
            }
        }

        let cpu_time_nanos: i64 = read_single_line_file(&self.cpu_time_file)
            .parse()
            .expect("invalid cpu time");
        // TimeUnit.MILLISECONDS.toNanos(clock.millis())
        let current_time_nanos: i64 = self.clock.millis() * 1_000_000;

        let mut skip = false;
        let cpu_core_time_used;
        {
            let _guard = LOCK_OBJECT.lock().unwrap_or_else(|e| e.into_inner());
            let mut state = self.state.lock().unwrap_or_else(|e| e.into_inner());

            if state.last_cpu_use_time_nanos == 0 && state.last_system_time_nanos == 0 {
                skip = true;
            }
            let nano_time_diff = current_time_nanos - state.last_system_time_nanos;
            let cpu_use_diff = cpu_time_nanos - state.last_cpu_use_time_nanos;
            cpu_core_time_used = cpu_use_diff as f64 / nano_time_diff as f64;

            state.last_cpu_use_time_nanos = cpu_time_nanos;
            state.last_system_time_nanos = current_time_nanos;
        }

        if skip {
            0.0
        } else {
            let limit = *self.cpu_limit.lock().unwrap_or_else(|e| e.into_inner());
            (100.0f64).min(cpu_core_time_used / limit * 100.0)
        }
    }
}

impl WorkerMetric for Cgroupv1CpuWorkerMetric {
    fn short_name(&self) -> String {
        WorkerMetricType::Cpu.short_name().to_string()
    }

    fn capture(&self) -> WorkerMetricValue {
        WorkerMetricValue::builder()
            .value(self.calculate_cpu_usage())
            .build()
    }

    fn operating_range(&self) -> OperatingRange {
        self.operating_range
    }

    fn worker_metric_type(&self) -> WorkerMetricType {
        WorkerMetricType::Cpu
    }
}

// Allow constructing via `Arc<Self>` where the metric list is shared.
impl Cgroupv1CpuWorkerMetric {
    /// Boxed convenience for the selector.
    pub fn into_arc(self) -> Arc<dyn WorkerMetric> {
        Arc::new(self)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::metric::test_util::write_line_to_file;

    fn nanos_of_millis(ms: i64) -> i64 {
        ms * 1_000_000
    }

    #[test]
    fn sanity_capture() {
        let dir = crate::worker::metric::test_util::temp_dir("cg1_sanity");
        let cpu_time = dir.join("cpuTime");
        let cfs_quota = dir.join("cfsQuota");
        let cfs_period = dir.join("cfsPeriod");
        let eff = dir.join("cpuset.effective_cpus");

        write_line_to_file(&cfs_quota, "20000");
        write_line_to_file(&cfs_period, "10000");

        let clock = Clock::mock(vec![1000, 2000]);
        let metric = Cgroupv1CpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            cpu_time.to_str().unwrap(),
            cfs_quota.to_str().unwrap(),
            cfs_period.to_str().unwrap(),
            eff.to_str().unwrap(),
            clock,
        );

        write_line_to_file(&cpu_time, &nanos_of_millis(1000).to_string());
        assert_eq!(metric.capture().value(), 0.0);

        write_line_to_file(&cpu_time, &nanos_of_millis(1500).to_string());
        // 0.5s cpu over 1s wall, quota=2 cores => 25%.
        assert_eq!(metric.capture().value(), 25.0);

        crate::worker::metric::test_util::cleanup(&dir);
    }

    #[test]
    fn capture_no_cpu_limit() {
        let dir = crate::worker::metric::test_util::temp_dir("cg1_nolimit");
        let cpu_time = dir.join("cpuTime");
        let cfs_quota = dir.join("cfsQuota");
        let cfs_period = dir.join("cfsPeriod");
        let eff = dir.join("cpuset.effective_cpus");

        write_line_to_file(&cfs_quota, "-1");
        write_line_to_file(&cfs_period, "10000");

        let clock = Clock::mock(vec![1000, 2000]);
        let metric = Cgroupv1CpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            cpu_time.to_str().unwrap(),
            cfs_quota.to_str().unwrap(),
            cfs_period.to_str().unwrap(),
            eff.to_str().unwrap(),
            clock,
        );

        write_line_to_file(&eff, "0-7");
        write_line_to_file(&cpu_time, &nanos_of_millis(1000).to_string());
        assert_eq!(metric.capture().value(), 0.0);

        write_line_to_file(&cpu_time, &nanos_of_millis(1500).to_string());
        // 0.5s over 1s wall / 8 cores => 6.25%.
        assert_eq!(metric.capture().value(), 6.25);

        crate::worker::metric::test_util::cleanup(&dir);
    }

    #[test]
    #[should_panic(expected = "does not exist")]
    fn sanity_capture_file_not_found() {
        let clock = Clock::mock(vec![1000, 2000]);
        let metric = Cgroupv1CpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            "/someBadPath",
            "/someBadPath",
            "/someBadPath",
            "/someBadPath",
            clock,
        );
        metric.capture();
    }
}
