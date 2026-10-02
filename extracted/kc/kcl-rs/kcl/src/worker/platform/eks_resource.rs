//! Port of `software.amazon.kinesis.worker.platform.EksResource`.

use std::path::Path;

use crate::worker::platform::{
    ComputePlatform, OperatingRangeDataProvider, ResourceMetadataProvider,
};

const K8S_TOKEN_PATH: &str = "/var/run/secrets/kubernetes.io/serviceaccount/token";

/// Detects EKS via the existence of the Kubernetes service-account token file,
/// then selects cgroup v2-before-v1 as the operating-range provider.
pub struct EksResource {
    k8s_token_path: String,
}

impl EksResource {
    /// Construct with an injected token path (Java `@VisibleForTesting` ctor).
    pub fn new(k8s_token_path: impl Into<String>) -> Self {
        Self {
            k8s_token_path: k8s_token_path.into(),
        }
    }

    /// Construct with the default K8s token path (Java `create()`).
    pub fn create() -> Self {
        Self::new(K8S_TOKEN_PATH)
    }
}

impl ResourceMetadataProvider for EksResource {
    fn is_on_platform(&self) -> bool {
        Path::new(&self.k8s_token_path).exists()
    }

    fn get_platform(&self) -> ComputePlatform {
        ComputePlatform::Eks
    }

    fn get_operating_range_data_provider(&self) -> Option<OperatingRangeDataProvider> {
        // Only one of cgroup v1/v2 is mounted; check v2 first (preserve order).
        [
            OperatingRangeDataProvider::LinuxEksCgroupV2,
            OperatingRangeDataProvider::LinuxEksCgroupV1,
        ]
        .into_iter()
        .find(|p| p.is_provider())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::metric::test_util::{cleanup, temp_dir};

    #[test]
    fn is_eks() {
        let dir = temp_dir("eks");
        let token = dir.join("k8sToken");
        std::fs::write(&token, "").unwrap();
        let eks = EksResource::new(token.to_str().unwrap());
        assert!(eks.is_on_platform());
        assert_eq!(eks.get_platform(), ComputePlatform::Eks);
        cleanup(&dir);
    }

    #[test]
    fn is_not_eks() {
        let eks = EksResource::new("");
        assert!(!eks.is_on_platform());
    }
}
