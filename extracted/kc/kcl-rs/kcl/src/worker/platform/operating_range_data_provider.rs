//! Port of `software.amazon.kinesis.worker.platform.OperatingRangeDataProvider`.

use std::path::Path;

use crate::worker::platform::ecs_resource::ECS_METADATA_KEY_V4;

/// The concrete data-source strategies for CPU operating-range/metrics on Linux,
/// each with its own platform-detection logic ([`Self::is_provider`]).
///
/// Java models these as an "enum with abstract method + per-constant body";
/// ported as a Rust enum + a `match` in [`Self::is_provider`]. All checks are
/// read-only and re-evaluated on every call (no caching), matching Java.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum OperatingRangeDataProvider {
    LinuxEksCgroupV1,
    LinuxEksCgroupV2,
    LinuxEcsMetadataKeyV4,
    LinuxProc,
}

impl OperatingRangeDataProvider {
    fn is_linux() -> bool {
        std::env::consts::OS == "linux"
    }

    /// Whether this provider is supported on the current host (Java
    /// `isProvider`).
    pub fn is_provider(&self) -> bool {
        match self {
            Self::LinuxEksCgroupV1 => {
                if !Self::is_linux() {
                    return false;
                }
                // cgroup v1 excludes when the v2 marker is present.
                if Path::new("/sys/fs/cgroup/cgroup.controllers").exists() {
                    return false;
                }
                Path::new("/sys/fs/cgroup/memory").exists()
                    || Path::new("/sys/fs/cgroup/cpu").exists()
            }
            Self::LinuxEksCgroupV2 => {
                Self::is_linux() && Path::new("/sys/fs/cgroup/cgroup.controllers").exists()
            }
            Self::LinuxEcsMetadataKeyV4 => {
                Self::is_linux()
                    && !std::env::var(ECS_METADATA_KEY_V4)
                        .unwrap_or_default()
                        .is_empty()
            }
            Self::LinuxProc => Self::is_linux() && Path::new("/proc").exists(),
        }
    }
}
