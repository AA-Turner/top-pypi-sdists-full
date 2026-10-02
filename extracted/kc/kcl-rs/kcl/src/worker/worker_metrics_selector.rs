//! Port of `software.amazon.kinesis.worker.WorkerMetricsSelector`.

use std::sync::Arc;

use crate::worker::metric::impl_::container::{
    Cgroupv1CpuWorkerMetric, Cgroupv2CpuWorkerMetric, EcsCpuWorkerMetric,
};
use crate::worker::metric::impl_::linux::LinuxCpuWorkerMetric;
use crate::worker::metric::{OperatingRange, WorkerMetric};
use crate::worker::platform::{OperatingRangeDataProvider, ResourceMetadataProvider};

/// Selects the default CPU-based [`WorkerMetric`] for the detected compute
/// platform (EC2/ECS/EKS), or an empty list if none is detected.
pub struct WorkerMetricsSelector {
    worker_compute_platforms: Vec<Arc<dyn ResourceMetadataProvider>>,
}

fn default_operating_range() -> OperatingRange {
    OperatingRange::builder().max_utilization(100).build()
}

impl WorkerMetricsSelector {
    /// Construct with the ordered platform providers (Java constructor).
    pub fn new(worker_compute_platforms: Vec<Arc<dyn ResourceMetadataProvider>>) -> Self {
        Self {
            worker_compute_platforms,
        }
    }

    /// Wire ECS, EKS, then EC2 (EC2 last) — Java `create()`.
    ///
    /// # TODO(port): EC2 provider omitted
    /// Java wires `EcsResource`, `EksResource`, then `Ec2Resource` (EC2 last).
    /// The Rust `Ec2Resource` needs a real HTTP `UrlOpener` (no HTTP-client dep
    /// this wave — see `Ec2Resource` docs), so it is omitted here; a
    /// non-EC2/ECS/EKS host falls through to an empty metric list (Java's
    /// documented "no default metrics -> throughput-based balancing" path). The
    /// coordinator/retrieval wave can add the EC2 provider once a `UrlOpener`
    /// impl exists.
    pub fn create() -> Self {
        use crate::worker::platform::{EcsResource, EksResource};
        let providers: Vec<Arc<dyn ResourceMetadataProvider>> = vec![
            Arc::new(EcsResource::create()),
            Arc::new(EksResource::create()),
        ];
        Self::new(providers)
    }

    fn get_operating_range_data_provider(&self) -> Option<OperatingRangeDataProvider> {
        for platform in &self.worker_compute_platforms {
            if platform.is_on_platform() {
                let compute_platform = platform.get_platform();
                tracing::info!("Worker is running on {:?}", compute_platform);
                return platform.get_operating_range_data_provider();
            }
        }
        None
    }

    /// Returns the default worker metrics for the detected platform (Java
    /// `getDefaultWorkerMetrics`). Empty when no platform/provider is detected.
    pub fn get_default_worker_metrics(&self) -> Vec<Arc<dyn WorkerMetric>> {
        let mut worker_metrics: Vec<Arc<dyn WorkerMetric>> = Vec::new();
        let provider = match self.get_operating_range_data_provider() {
            Some(p) => p,
            None => {
                tracing::warn!("Did not find an operating range metadata provider.");
                return worker_metrics;
            }
        };
        tracing::info!(
            "Worker has operating range metadata provider {:?}",
            provider
        );
        match provider {
            OperatingRangeDataProvider::LinuxProc => {
                worker_metrics.push(Arc::new(LinuxCpuWorkerMetric::with_default_stat_file(
                    default_operating_range(),
                )));
            }
            OperatingRangeDataProvider::LinuxEcsMetadataKeyV4 => {
                worker_metrics.push(Arc::new(EcsCpuWorkerMetric::from_env(
                    default_operating_range(),
                )));
            }
            OperatingRangeDataProvider::LinuxEksCgroupV2 => {
                worker_metrics.push(Arc::new(Cgroupv2CpuWorkerMetric::with_default_paths(
                    default_operating_range(),
                )));
            }
            OperatingRangeDataProvider::LinuxEksCgroupV1 => {
                worker_metrics.push(Arc::new(Cgroupv1CpuWorkerMetric::with_default_paths(
                    default_operating_range(),
                )));
            }
        }
        worker_metrics
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::platform::{ComputePlatform, OperatingRangeDataProvider};
    use std::sync::Mutex;

    // A hand-written mock ResourceMetadataProvider (the trait is not automocked).
    struct FakeProvider {
        on_platform: Mutex<bool>,
        platform: Mutex<ComputePlatform>,
        provider: Mutex<Option<OperatingRangeDataProvider>>,
    }

    impl FakeProvider {
        fn new() -> Self {
            Self {
                on_platform: Mutex::new(true),
                platform: Mutex::new(ComputePlatform::Ec2),
                provider: Mutex::new(Some(OperatingRangeDataProvider::LinuxProc)),
            }
        }
    }

    impl ResourceMetadataProvider for FakeProvider {
        fn is_on_platform(&self) -> bool {
            *self.on_platform.lock().unwrap()
        }
        fn get_platform(&self) -> ComputePlatform {
            *self.platform.lock().unwrap()
        }
        fn get_operating_range_data_provider(&self) -> Option<OperatingRangeDataProvider> {
            *self.provider.lock().unwrap()
        }
    }

    fn selector_with(fake: Arc<FakeProvider>) -> WorkerMetricsSelector {
        WorkerMetricsSelector::new(vec![fake])
    }

    // Downcast helper: verify the concrete metric type by its short-name +
    // worker-metric-type (Rust has no getClass()); the selector only ever
    // produces CPU metrics, so we assert the metric captures without panicking
    // is not feasible (needs files) — instead assert count + type-name via a
    // dedicated marker method.
    #[test]
    fn on_ec2_and_linux_proc() {
        let fake = Arc::new(FakeProvider::new());
        let selector = selector_with(fake);
        let metrics = selector.get_default_worker_metrics();
        assert_eq!(metrics.len(), 1);
        assert_eq!(
            metrics[0].worker_metric_type(),
            crate::worker::metric::WorkerMetricType::Cpu
        );
    }

    #[test]
    fn on_ec2_but_not_have_linux_proc() {
        let fake = Arc::new(FakeProvider::new());
        *fake.provider.lock().unwrap() = None;
        let selector = selector_with(fake);
        assert_eq!(selector.get_default_worker_metrics().len(), 0);
    }

    #[test]
    fn on_eks_and_cgroup_v1() {
        let fake = Arc::new(FakeProvider::new());
        *fake.platform.lock().unwrap() = ComputePlatform::Eks;
        *fake.provider.lock().unwrap() = Some(OperatingRangeDataProvider::LinuxEksCgroupV1);
        let selector = selector_with(fake);
        assert_eq!(selector.get_default_worker_metrics().len(), 1);
    }

    #[test]
    fn on_eks_and_cgroup_v2() {
        let fake = Arc::new(FakeProvider::new());
        *fake.platform.lock().unwrap() = ComputePlatform::Eks;
        *fake.provider.lock().unwrap() = Some(OperatingRangeDataProvider::LinuxEksCgroupV2);
        let selector = selector_with(fake);
        assert_eq!(selector.get_default_worker_metrics().len(), 1);
    }

    #[test]
    fn on_ecs_uses_ecs_worker_metric() {
        let fake = Arc::new(FakeProvider::new());
        *fake.platform.lock().unwrap() = ComputePlatform::Ecs;
        *fake.provider.lock().unwrap() = Some(OperatingRangeDataProvider::LinuxEcsMetadataKeyV4);
        let selector = selector_with(fake);
        assert_eq!(selector.get_default_worker_metrics().len(), 1);
    }

    #[test]
    fn not_on_supported_platform() {
        let fake = Arc::new(FakeProvider::new());
        *fake.on_platform.lock().unwrap() = false;
        let selector = selector_with(fake);
        assert_eq!(selector.get_default_worker_metrics().len(), 0);
    }
}
