//! Port of `software.amazon.kinesis.worker.platform.ResourceMetadataProvider`.

use crate::worker::platform::OperatingRangeDataProvider;

/// The compute platforms a worker may run on (Java nested
/// `ResourceMetadataProvider.ComputePlatform`).
///
/// `Unknown` is declared for API completeness but never returned by any of the
/// three concrete providers (matches Java).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ComputePlatform {
    Ec2,
    Ecs,
    Eks,
    Unknown,
}

/// Common contract for platform-detection providers (EC2/ECS/EKS): determine
/// whether the current process runs on that platform and, if so, which compute
/// platform and operating-range data provider apply.
///
/// Port of the Java `ResourceMetadataProvider` interface. `is_on_platform` may
/// perform I/O (EC2 hits IMDS over HTTP), so it is defined as a plain sync
/// method here (the Java surface is synchronous; the EC2 HTTP call is behind an
/// injectable [`UrlOpener`](crate::worker::platform::UrlOpener)).
pub trait ResourceMetadataProvider: Send + Sync {
    /// Whether the worker is running on this provider's platform.
    fn is_on_platform(&self) -> bool;

    /// The compute platform represented by this provider.
    fn get_platform(&self) -> ComputePlatform;

    /// The operating-range data provider for this platform, if any.
    fn get_operating_range_data_provider(&self) -> Option<OperatingRangeDataProvider>;
}
