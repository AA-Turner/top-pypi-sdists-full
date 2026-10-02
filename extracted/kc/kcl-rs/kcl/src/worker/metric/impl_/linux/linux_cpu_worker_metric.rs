//! Port of `software.amazon.kinesis.worker.metric.impl.linux.LinuxCpuWorkerMetric`.

use std::sync::Mutex;

use crate::worker::metric::{OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue};

/// Shared static lock, mirroring the Java `private static final Object LOCK_OBJECT`
/// that is shared **across all instances** of `LinuxCpuWorkerMetric`. This is
/// preserved verbatim (arch-map flags it as a likely-unintentional-but-load-bearing
/// artifact). Per-instance mutable state lives behind its own [`Mutex`]; this
/// static lock serializes the diff-update section across instances.
static LOCK_OBJECT: Mutex<()> = Mutex::new(());

/// Reads CPU usage out of `/proc/stat` and diffs successive reads to yield a
/// utilization percentage.
///
/// First `capture()` returns `0.0` (no baseline). If `/proc/stat` is unchanged
/// since the last read it also returns `0.0`. Missing file / parse error
/// **panics** (Java `IllegalArgumentException`).
#[derive(Debug)]
pub struct LinuxCpuWorkerMetric {
    operating_range: OperatingRange,
    stat_file: String,
    state: Mutex<CpuState>,
}

#[derive(Debug, Default)]
struct CpuState {
    last_usr: i64,
    last_iow: i64,
    last_sys: i64,
    last_idl: i64,
    last_tot: i64,
    last_line: Option<String>,
}

impl LinuxCpuWorkerMetric {
    /// Full constructor (Java package-private `@RequiredArgsConstructor`): the
    /// operating range and the path to the `stat` file.
    pub fn new(operating_range: OperatingRange, stat_file: impl Into<String>) -> Self {
        Self {
            operating_range,
            stat_file: stat_file.into(),
            state: Mutex::new(CpuState::default()),
        }
    }

    /// Convenience constructor defaulting the stat file to `/proc/stat` (Java
    /// public single-arg ctor).
    pub fn with_default_stat_file(operating_range: OperatingRange) -> Self {
        Self::new(operating_range, "/proc/stat")
    }

    fn calculate_cpu_usage(&self) -> f64 {
        if !std::path::Path::new(&self.stat_file).exists() {
            panic!(
                "LinuxCpuWorkerMetric is not configured properly, file : {} does not exists",
                self.stat_file
            );
        }
        let content = match std::fs::read_to_string(&self.stat_file) {
            Ok(c) => c,
            Err(_) => panic!(
                "LinuxCpuWorkerMetric failed to read metric stats or not configured properly."
            ),
        };
        let line = content.lines().next().unwrap_or("").to_string();
        let line_vals: Vec<&str> = line.split_whitespace().collect();

        let parse = |i: usize| -> i64 {
            line_vals
                .get(i)
                .and_then(|s| s.parse::<i64>().ok())
                .unwrap_or_else(|| {
                    panic!(
                        "LinuxCpuWorkerMetric failed to read metric stats or not configured properly."
                    )
                })
        };

        let usr = parse(1) + parse(2);
        let sys = parse(3);
        let idl = parse(4);
        let iow = parse(5);
        let tot = usr + sys + idl + iow;

        let diff_idl;
        let diff_tot;
        let mut skip = false;

        {
            // Shared-across-instances lock, then mutate per-instance state.
            let _guard = LOCK_OBJECT.lock().unwrap_or_else(|e| e.into_inner());
            let mut state = self.state.lock().unwrap_or_else(|e| e.into_inner());

            if state.last_usr == 0 || Some(&line) == state.last_line.as_ref() {
                // First call (no diff baseline) or /proc/stat unchanged.
                skip = true;
            }

            diff_idl = (idl - state.last_idl).abs();
            diff_tot = (tot - state.last_tot).abs();
            if diff_tot < diff_idl {
                tracing::warn!(
                    "diffTot is less than diff_idle. \nPrev cpu line : {:?} and current cpu line : {} ",
                    state.last_line,
                    line
                );
                if iow < state.last_iow {
                    // Rare non-monotonic iowait quirk while idle; treat as skip.
                    skip = true;
                }
            }
            state.last_usr = usr;
            state.last_sys = sys;
            state.last_idl = idl;
            state.last_iow = iow;
            state.last_tot = usr + sys + idl + iow;
            state.last_line = Some(line);
        }

        if skip {
            return 0.0;
        }
        ((diff_tot - diff_idl) as f64 / diff_tot as f64) * 100.0
    }
}

impl WorkerMetric for LinuxCpuWorkerMetric {
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

    #[test]
    fn sanity_capture() {
        let dir = crate::worker::metric::test_util::temp_dir("linux_cpu_sanity");
        let stat_file = dir.join("cpuStat");
        let path = stat_file.to_str().unwrap();

        let metric =
            LinuxCpuWorkerMetric::new(OperatingRange::builder().max_utilization(80).build(), path);

        write_line_to_file(
            &stat_file,
            &format!(
                "cpu  {} {} {} {} {} 0 0 0 0 0",
                20000, 200, 2000, 1500000, 1000
            ),
        );
        let response1 = metric.capture();
        assert_eq!(response1.value(), 0.0);

        write_line_to_file(
            &stat_file,
            &format!(
                "cpu  {} {} {} {} {} 0 0 0 0 0",
                30000, 3000, 30000, 2000000, 2000
            ),
        );
        let response2 = metric.capture();
        assert_eq!(response2.value() as i32, 7);

        crate::worker::metric::test_util::cleanup(&dir);
    }

    #[test]
    #[should_panic(expected = "does not exists")]
    fn sanity_capture_file_not_found() {
        let dir = crate::worker::metric::test_util::temp_dir("linux_cpu_notfound");
        let bad = dir.join("randomPath");
        let metric = LinuxCpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            bad.to_str().unwrap(),
        );
        metric.capture();
    }

    #[test]
    fn capture_rare_iowait_field_decreased_asserts_zero() {
        let dir = crate::worker::metric::test_util::temp_dir("linux_cpu_iowait");
        let stat_file = dir.join("cpuStat");
        let path = stat_file.to_str().unwrap();

        let metric =
            LinuxCpuWorkerMetric::new(OperatingRange::builder().max_utilization(80).build(), path);

        write_line_to_file(
            &stat_file,
            &format!(
                "cpu  {} {} {} {} {} 0 0 0 0 0",
                5469899i64, 773829i64, 2079951i64, 2814572566i64, 52048i64
            ),
        );
        let response1 = metric.capture();
        assert_eq!(response1.value(), 0.0);

        write_line_to_file(
            &stat_file,
            &format!(
                "cpu  {} {} {} {} {} 0 0 0 0 0",
                5469899i64, 773829i64, 2079951i64, 2814575765i64, 52047i64
            ),
        );
        let response2 = metric.capture();
        assert_eq!((response2.value() * 1000.0).round() / 1000.0, 0.0);

        crate::worker::metric::test_util::cleanup(&dir);
    }
}
