//! Port of `software.amazon.kinesis.worker.metric.impl.container`.
//!
//! Container-host worker metrics (cgroup v1/v2, ECS task metadata).

pub mod cgroupv1_cpu_worker_metric;
pub mod cgroupv2_cpu_worker_metric;
pub mod ecs_cpu_worker_metric;

pub use cgroupv1_cpu_worker_metric::Cgroupv1CpuWorkerMetric;
pub use cgroupv2_cpu_worker_metric::Cgroupv2CpuWorkerMetric;
pub use ecs_cpu_worker_metric::{
    DefaultEcsMetadataFetcher, EcsCpuWorkerMetric, EcsMetadataFetcher,
};
