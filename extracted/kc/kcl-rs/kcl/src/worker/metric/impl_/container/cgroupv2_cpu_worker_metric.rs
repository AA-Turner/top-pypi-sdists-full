//! Port of `software.amazon.kinesis.worker.metric.impl.container.Cgroupv2CpuWorkerMetric`.

use std::sync::Mutex;

use crate::utils::cgroup::{get_available_cpus_from_effective_cpu_set, read_single_line_file};
use crate::worker::metric::{
    Clock, OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue,
};

const CGROUP_ROOT: &str = "/sys/fs/cgroup/";

/// Shared static lock, mirroring the Java `private static final Object LOCK_OBJECT`
/// (distinct object from cgroup v1's, same across-instances sharing pattern).
static LOCK_OBJECT: Mutex<()> = Mutex::new(());

/// CPU utilization on cgroup v2 hosts (Amazon Linux 2023), reading `cpu.max`,
/// `cpuset.cpus.effective`, and `cpu.stat` (usage_usec) with microsecond timers.
#[derive(Debug)]
pub struct Cgroupv2CpuWorkerMetric {
    operating_range: OperatingRange,
    cpu_max_file: String,
    effective_cpu_set_file: String,
    cpu_stat_file: String,
    clock: Clock,
    cpu_limit: Mutex<f64>,
    state: Mutex<Cgroupv2State>,
}

#[derive(Debug, Default)]
struct Cgroupv2State {
    last_cpu_use_time_micros: i64,
    last_system_time_micros: i64,
}

impl Cgroupv2CpuWorkerMetric {
    /// Full constructor (Java package-private ctor) with all file paths + clock.
    pub fn new(
        operating_range: OperatingRange,
        cpu_max_file: impl Into<String>,
        effective_cpu_set_file: impl Into<String>,
        cpu_stat_file: impl Into<String>,
        clock: Clock,
    ) -> Self {
        Self {
            operating_range,
            cpu_max_file: cpu_max_file.into(),
            effective_cpu_set_file: effective_cpu_set_file.into(),
            cpu_stat_file: cpu_stat_file.into(),
            clock,
            cpu_limit: Mutex::new(-1.0),
            state: Mutex::new(Cgroupv2State::default()),
        }
    }

    /// Convenience constructor (Java public single-arg ctor) with default cgroup
    /// v2 paths and the system UTC clock.
    pub fn with_default_paths(operating_range: OperatingRange) -> Self {
        Self::new(
            operating_range,
            format!("{}cpu.max", CGROUP_ROOT),
            format!("{}cpuset.cpus.effective", CGROUP_ROOT),
            format!("{}cpu.stat", CGROUP_ROOT),
            Clock::system_utc(),
        )
    }

    fn calculate_cpu_limit(&self) -> f64 {
        // File contains "$MAX $PERIOD"; $MAX is a number or "max".
        let cpu_max = read_single_line_file(&self.cpu_max_file);
        let parts: Vec<&str> = cpu_max.split(' ').collect();
        let max = parts[0];
        let period = parts[1];
        if max == "max" {
            get_available_cpus_from_effective_cpu_set(&read_single_line_file(
                &self.effective_cpu_set_file,
            )) as f64
        } else {
            max.parse::<f64>().expect("invalid cpu.max value")
                / period.parse::<i64>().expect("invalid cpu.max period") as f64
        }
    }

    fn calculate_cpu_usage(&self) -> f64 {
        {
            let mut limit = self.cpu_limit.lock().unwrap_or_else(|e| e.into_inner());
            if *limit == -1.0 {
                *limit = self.calculate_cpu_limit();
            }
        }

        // First line: "usage_usec $MICROSECONDS".
        let cpu_usage_stat = read_single_line_file(&self.cpu_stat_file);
        let cpu_time_micros: i64 = cpu_usage_stat
            .split(' ')
            .nth(1)
            .and_then(|s| s.parse().ok())
            .expect("invalid cpu.stat usage_usec");
        // TimeUnit.MILLISECONDS.toMicros(clock.millis())
        let current_time_micros: i64 = self.clock.millis() * 1_000;

        let mut skip = false;
        let cpu_core_time_used;
        {
            let _guard = LOCK_OBJECT.lock().unwrap_or_else(|e| e.into_inner());
            let mut state = self.state.lock().unwrap_or_else(|e| e.into_inner());

            if state.last_cpu_use_time_micros == 0 && state.last_system_time_micros == 0 {
                skip = true;
            }
            let micro_time_diff = current_time_micros - state.last_system_time_micros;
            let cpu_use_diff = cpu_time_micros - state.last_cpu_use_time_micros;
            cpu_core_time_used = cpu_use_diff as f64 / micro_time_diff as f64;

            state.last_cpu_use_time_micros = cpu_time_micros;
            state.last_system_time_micros = current_time_micros;
        }

        if skip {
            0.0
        } else {
            let limit = *self.cpu_limit.lock().unwrap_or_else(|e| e.into_inner());
            (100.0f64).min(cpu_core_time_used / limit * 100.0)
        }
    }
}

impl WorkerMetric for Cgroupv2CpuWorkerMetric {
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::metric::test_util::write_line_to_file;

    fn micros_of_millis(ms: i64) -> i64 {
        ms * 1_000
    }

    #[test]
    fn sanity_capture() {
        let dir = crate::worker::metric::test_util::temp_dir("cg2_sanity");
        let cpu_max = dir.join("cpu.max");
        let eff = dir.join("cpuset.cpus.effective");
        let cpu_stat = dir.join("cpu.stat");

        let clock = Clock::mock(vec![1000, 2000]);
        let metric = Cgroupv2CpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            cpu_max.to_str().unwrap(),
            eff.to_str().unwrap(),
            cpu_stat.to_str().unwrap(),
            clock,
        );

        write_line_to_file(&cpu_max, "20000 10000");
        write_line_to_file(&cpu_stat, &format!("usage_usec {}", micros_of_millis(1000)));
        assert_eq!(metric.capture().value(), 0.0);

        write_line_to_file(&cpu_stat, &format!("usage_usec {}", micros_of_millis(1500)));
        // 0.5s over 1s wall / 2 cores => 25%.
        assert_eq!(metric.capture().value(), 25.0);

        crate::worker::metric::test_util::cleanup(&dir);
    }

    #[test]
    fn capture_no_cpu_limit() {
        let dir = crate::worker::metric::test_util::temp_dir("cg2_nolimit");
        let cpu_max = dir.join("cpu.max");
        let eff = dir.join("cpuset.cpus.effective");
        let cpu_stat = dir.join("cpu.stat");

        let clock = Clock::mock(vec![1000, 2000]);
        let metric = Cgroupv2CpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            cpu_max.to_str().unwrap(),
            eff.to_str().unwrap(),
            cpu_stat.to_str().unwrap(),
            clock,
        );

        write_line_to_file(&cpu_max, "max 10000");
        write_line_to_file(&eff, "0-7");
        write_line_to_file(&cpu_stat, &format!("usage_usec {}", micros_of_millis(1000)));
        assert_eq!(metric.capture().value(), 0.0);

        write_line_to_file(&cpu_stat, &format!("usage_usec {}", micros_of_millis(1500)));
        // 0.5s over 1s wall / 8 cores => 6.25%.
        assert_eq!(metric.capture().value(), 6.25);

        crate::worker::metric::test_util::cleanup(&dir);
    }

    #[test]
    #[should_panic(expected = "does not exist")]
    fn sanity_capture_file_not_found() {
        let clock = Clock::mock(vec![1000, 2000]);
        let metric = Cgroupv2CpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            "/someBadPath",
            "/someBadPath",
            "/someBadPath",
            clock,
        );
        metric.capture();
    }
}
