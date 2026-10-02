//! Port of `software.amazon.kinesis.worker.metric.impl.container.EcsCpuWorkerMetric`.

use std::sync::{Arc, Mutex};

use serde_json::Value;

use crate::worker::metric::{OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue};

/// Environment variable naming the ECS Task Metadata Endpoint v4 root URI.
pub const SYS_VAR_ECS_METADATA_URI: &str = "ECS_CONTAINER_METADATA_URI_V4";

/// Fetches raw JSON metadata for a URI. Abstracts Java's raw
/// `URL.openStream()`. The default [`DefaultEcsMetadataFetcher`] reads `file://`
/// URIs (used by the ported tests and by fixture-based runs).
///
/// # TODO(port): production HTTP fetch
/// Java performs a blocking HTTP GET against the ECS metadata endpoint
/// (`http://.../stats`, `/task`, root). No HTTP-client crate is a dependency at
/// this wave, so the default fetcher supports only `file://` (and bare paths);
/// an `http(s)://` URI returns an error. The retrieval/coordinator wave (or a
/// small blocking HTTP client) can supply a real fetcher via
/// [`EcsCpuWorkerMetric::with_fetcher`].
pub trait EcsMetadataFetcher: Send + Sync + std::fmt::Debug {
    /// Read the metadata JSON at `uri`. Returns the raw JSON text.
    fn fetch(&self, uri: &str) -> Result<String, String>;
}

/// Default fetcher: reads `file://` URIs (and bare filesystem paths). Errors on
/// `http(s)://` (see the [`EcsMetadataFetcher`] TODO).
#[derive(Debug, Default)]
pub struct DefaultEcsMetadataFetcher;

impl EcsMetadataFetcher for DefaultEcsMetadataFetcher {
    fn fetch(&self, uri: &str) -> Result<String, String> {
        let path = if let Some(rest) = uri.strip_prefix("file://") {
            rest.to_string()
        } else if uri.starts_with("http://") || uri.starts_with("https://") {
            return Err(format!(
                "HTTP ECS metadata fetch not supported in this port (uri: {}); \
                 supply a fetcher via EcsCpuWorkerMetric::with_fetcher",
                uri
            ));
        } else {
            uri.to_string()
        };
        std::fs::read_to_string(&path).map_err(|e| format!("Error reading ECS metadata: {}", e))
    }
}

/// Queries the ECS Task Metadata Endpoint v4 for container CPU stats and
/// computes the container's percent CPU utilization of its proportional share of
/// the task-level CPU limit.
///
/// First call (both `precpu` fields 0) returns `0.0`. Absent metadata endpoint
/// / read error **panics** (Java `IllegalArgumentException`).
#[derive(Debug)]
pub struct EcsCpuWorkerMetric {
    operating_range: OperatingRange,
    container_stats_uri: Option<String>,
    task_metadata_uri: Option<String>,
    container_metadata_uri: Option<String>,
    fetcher: Arc<dyn EcsMetadataFetcher>,
    // Lazily computed once; -1 sentinel = unset.
    cache: Mutex<Cache>,
}

#[derive(Debug, Default)]
struct Cache {
    container_cpu_limit: f64,
    online_cpus: f64,
}

impl EcsCpuWorkerMetric {
    /// Full constructor (Java package-private ctor) with explicit URIs and the
    /// default fetcher.
    pub fn new(
        operating_range: OperatingRange,
        container_stats_uri: impl Into<String>,
        task_metadata_uri: impl Into<String>,
        container_metadata_uri: impl Into<String>,
    ) -> Self {
        Self {
            operating_range,
            container_stats_uri: Some(container_stats_uri.into()),
            task_metadata_uri: Some(task_metadata_uri.into()),
            container_metadata_uri: Some(container_metadata_uri.into()),
            fetcher: Arc::new(DefaultEcsMetadataFetcher),
            cache: Mutex::new(Cache {
                container_cpu_limit: -1.0,
                online_cpus: -1.0,
            }),
        }
    }

    /// Construct from the `ECS_CONTAINER_METADATA_URI_V4` env var (Java public
    /// single-arg ctor). If the env var is absent, all URIs are `None` and
    /// `capture()` will panic at read time (lazy-fail parity).
    pub fn from_env(operating_range: OperatingRange) -> Self {
        Self::from_env_map(operating_range, |k| std::env::var(k).ok())
    }

    /// Testable variant of [`Self::from_env`] with an injectable env lookup.
    pub fn from_env_map(
        operating_range: OperatingRange,
        env: impl Fn(&str) -> Option<String>,
    ) -> Self {
        let root = env(SYS_VAR_ECS_METADATA_URI);
        let (stats, task, container) = match root {
            Some(root) => (
                Some(format!("{}/stats", root)),
                Some(format!("{}/task", root)),
                Some(root),
            ),
            None => (None, None, None),
        };
        Self {
            operating_range,
            container_stats_uri: stats,
            task_metadata_uri: task,
            container_metadata_uri: container,
            fetcher: Arc::new(DefaultEcsMetadataFetcher),
            cache: Mutex::new(Cache {
                container_cpu_limit: -1.0,
                online_cpus: -1.0,
            }),
        }
    }

    /// Override the metadata fetcher (e.g. a real HTTP client). See the
    /// [`EcsMetadataFetcher`] TODO.
    pub fn with_fetcher(mut self, fetcher: Arc<dyn EcsMetadataFetcher>) -> Self {
        self.fetcher = fetcher;
        self
    }

    fn read_ecs_metadata(&self, uri: &Option<String>) -> Value {
        if self.container_metadata_uri.is_none() {
            panic!("No ECS metadata endpoint found from environment variables.");
        }
        let uri = uri
            .as_ref()
            .expect("uri present when metadata endpoint present");
        let text = match self.fetcher.fetch(uri) {
            Ok(t) => t,
            Err(e) => panic!("Error in parsing ECS metadata: {}", e),
        };
        match serde_json::from_str(&text) {
            Ok(v) => v,
            Err(e) => panic!("Error in parsing ECS metadata: {}", e),
        }
    }

    fn calculate_cpu_usage(&self) -> f64 {
        let stats = self.read_ecs_metadata(&self.container_stats_uri);

        let cpu_usage = json_long(&stats, &["cpu_stats", "cpu_usage", "total_usage"]);
        let system_cpu_usage = json_long(&stats, &["cpu_stats", "system_cpu_usage"]);
        let prev_cpu_usage = json_long(&stats, &["precpu_stats", "cpu_usage", "total_usage"]);
        let prev_system_cpu_usage = json_long(&stats, &["precpu_stats", "system_cpu_usage"]);

        let online_cpus;
        let container_cpu_limit;
        {
            let mut cache = self.cache.lock().unwrap_or_else(|e| e.into_inner());
            if cache.container_cpu_limit == -1.0 && cache.online_cpus == -1.0 {
                cache.online_cpus = json_double(&stats, &["cpu_stats", "online_cpus"]);
                let oc = cache.online_cpus;
                // Compute the limit outside the borrow of cache to avoid re-lock.
                drop(cache);
                let limit = self.calculate_container_cpu_limit(oc);
                let mut cache = self.cache.lock().unwrap_or_else(|e| e.into_inner());
                cache.container_cpu_limit = limit;
                container_cpu_limit = limit;
                online_cpus = oc;
            } else {
                container_cpu_limit = cache.container_cpu_limit;
                online_cpus = cache.online_cpus;
            }
        }

        // precpu_stats values are 0 on the first call.
        if prev_cpu_usage == 0 && prev_system_cpu_usage == 0 {
            return 0.0;
        }

        let cpu_usage_diff = cpu_usage - prev_cpu_usage;
        let system_cpu_usage_diff = system_cpu_usage - prev_system_cpu_usage;

        // No system cpu usage => 100% used.
        if system_cpu_usage_diff == 0 {
            return 100.0;
        }

        let cpu_core_time_used = cpu_usage_diff as f64 / system_cpu_usage_diff as f64 * online_cpus;
        (100.0f64).min(cpu_core_time_used / container_cpu_limit * 100.0)
    }

    fn calculate_container_cpu_limit(&self, online_cpus: f64) -> f64 {
        let task = self.read_ecs_metadata(&self.task_metadata_uri);
        let task_cpu_limit = calculate_task_cpu_limit(&task, online_cpus);

        let root = self.read_ecs_metadata(&self.container_metadata_uri);
        let current_container_id = root.get("DockerId").and_then(|v| v.as_str()).unwrap_or("");

        let mut current_container_cpu_share = 2i64; // default per ECS agent >= 1.2.0
        let mut containers_cpu_share_sum = 0i64;
        if let Some(containers) = task.get("Containers").and_then(|v| v.as_array()) {
            for container in containers {
                let container_cpu_share = container
                    .get("Limits")
                    .and_then(|l| l.get("CPU"))
                    .and_then(|c| c.as_i64())
                    .unwrap_or(0);
                let docker_id = container
                    .get("DockerId")
                    .and_then(|v| v.as_str())
                    .unwrap_or("");
                if docker_id == current_container_id {
                    current_container_cpu_share = container_cpu_share;
                }
                containers_cpu_share_sum += container_cpu_share;
            }
        }
        current_container_cpu_share as f64 / containers_cpu_share_sum as f64 * task_cpu_limit
    }
}

/// Java `calculateTaskCpuLimit`: falls back to `online_cpus` when the task has
/// no `Limits`/`Limits.CPU` node (mirrors Jackson `isMissingNode`).
fn calculate_task_cpu_limit(task: &Value, online_cpus: f64) -> f64 {
    let limits = match task.get("Limits") {
        Some(l) if !l.is_null() => l,
        _ => return online_cpus,
    };
    match limits.get("CPU") {
        Some(c) if !c.is_null() => c.as_f64().unwrap_or(online_cpus),
        _ => online_cpus,
    }
}

/// Jackson-`path().asLong()` equivalent: navigate the path, `0` if missing.
fn json_long(root: &Value, path: &[&str]) -> i64 {
    navigate(root, path).and_then(|v| v.as_i64()).unwrap_or(0)
}

/// Jackson-`path().asDouble()` equivalent: navigate the path, `0.0` if missing.
fn json_double(root: &Value, path: &[&str]) -> f64 {
    navigate(root, path).and_then(|v| v.as_f64()).unwrap_or(0.0)
}

fn navigate<'a>(root: &'a Value, path: &[&str]) -> Option<&'a Value> {
    let mut cur = root;
    for key in path {
        cur = cur.get(key)?;
    }
    Some(cur)
}

impl WorkerMetric for EcsCpuWorkerMetric {
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

    // Fixtures are vendored into the repo (copied from the amazon-kinesis-client
    // test data) so the tests are self-contained in any checkout/worktree/CI —
    // resolved via CARGO_MANIFEST_DIR, no dependency on the sibling Java tree.
    fn ecs_data_root() -> std::path::PathBuf {
        let manifest = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        manifest.join("testdata/ecstestdata")
    }

    fn run_worker_metric_test(test_data_dir: &str, expected: f64) {
        let root = ecs_data_root().join(test_data_dir);
        let stats = root.join("stats");
        let task = root.join("task");
        let container = root.join("root");
        let metric = EcsCpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            stats.to_str().unwrap(),
            task.to_str().unwrap(),
            container.to_str().unwrap(),
        );
        assert_eq!(metric.capture().value(), expected);
    }

    #[test]
    fn sanity_capture_no_task_cpu_limit_one_container() {
        run_worker_metric_test("noTaskCpuLimitOneContainer", 50.0);
    }

    #[test]
    fn sanity_capture_no_task_cpu_limit_two_containers() {
        run_worker_metric_test("noTaskCpuLimitTwoContainers", 80.0);
    }

    #[test]
    fn sanity_capture_no_task_cpu_limit_but_has_memory_limit_one_container() {
        run_worker_metric_test("noTaskCpuLimitButHasMemoryLimitOneContainer", 50.0);
    }

    #[test]
    fn sanity_capture_task_cpu_limit_one_container() {
        run_worker_metric_test("taskCpuLimitOneContainer", 25.0);
    }

    #[test]
    fn sanity_capture_no_precpu_stats() {
        run_worker_metric_test("noPrecpuStats", 0.0);
    }

    #[test]
    fn sanity_capture_no_system_cpu_usage() {
        run_worker_metric_test("noSystemCpuUsage", 100.0);
    }

    #[test]
    #[should_panic(expected = "Error in parsing ECS metadata")]
    fn sanity_capture_bad_metadata_url() {
        let metric = EcsCpuWorkerMetric::new(
            OperatingRange::builder().max_utilization(80).build(),
            "/someBadPath",
            "/someBadPath",
            "/someBadPath",
        );
        metric.capture();
    }
}
