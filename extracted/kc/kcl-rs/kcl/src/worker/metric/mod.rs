//! Port of `software.amazon.kinesis.worker.metric`.
//!
//! The [`WorkerMetric`] trait + its value/config types ([`WorkerMetricValue`],
//! [`WorkerMetricType`], [`OperatingRange`]) and all concrete implementations
//! under [`impl_`].

pub mod clock;
pub mod impl_;
pub mod operating_range;
pub mod worker_metric;
pub mod worker_metric_type;

#[cfg(test)]
pub mod test_util;

pub use clock::Clock;
pub use operating_range::{OperatingRange, OperatingRangeBuilder};
pub use worker_metric::{WorkerMetric, WorkerMetricValue, WorkerMetricValueBuilder};
pub use worker_metric_type::WorkerMetricType;
