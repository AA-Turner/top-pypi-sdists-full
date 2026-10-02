//! Port of `software.amazon.kinesis.worker.platform.EcsResource`.

use std::collections::HashMap;

use crate::worker::platform::{
    ComputePlatform, OperatingRangeDataProvider, ResourceMetadataProvider,
};

/// ECS metadata v3 env var name (shared constant).
pub const ECS_METADATA_KEY_V3: &str = "ECS_CONTAINER_METADATA_URI";
/// ECS metadata v4 env var name (shared constant; also referenced by
/// [`OperatingRangeDataProvider`](crate::worker::platform::OperatingRangeDataProvider)).
pub const ECS_METADATA_KEY_V4: &str = "ECS_CONTAINER_METADATA_URI_V4";

/// Detects ECS via the presence of the ECS metadata URI env vars (no network
/// I/O). Reports [`OperatingRangeDataProvider::LinuxEcsMetadataKeyV4`].
pub struct EcsResource {
    sys_env: HashMap<String, String>,
}

impl EcsResource {
    /// Construct with an injected environment map (Java `@VisibleForTesting`
    /// ctor).
    pub fn new(sys_env: HashMap<String, String>) -> Self {
        Self { sys_env }
    }

    /// Construct from the real process environment (Java `create()`).
    pub fn create() -> Self {
        Self::new(std::env::vars().collect())
    }

    fn get_or_default<'a>(&'a self, key: &str) -> &'a str {
        self.sys_env.get(key).map(String::as_str).unwrap_or("")
    }
}

impl ResourceMetadataProvider for EcsResource {
    fn is_on_platform(&self) -> bool {
        !self.get_or_default(ECS_METADATA_KEY_V3).is_empty()
            || !self.get_or_default(ECS_METADATA_KEY_V4).is_empty()
    }

    fn get_platform(&self) -> ComputePlatform {
        ComputePlatform::Ecs
    }

    fn get_operating_range_data_provider(&self) -> Option<OperatingRangeDataProvider> {
        Some(OperatingRangeDataProvider::LinuxEcsMetadataKeyV4).filter(|p| p.is_provider())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_ecs() {
        let mut env = HashMap::new();
        env.insert(ECS_METADATA_KEY_V3.to_string(), "v3".to_string());
        assert!(EcsResource::new(env.clone()).is_on_platform());

        env.insert(ECS_METADATA_KEY_V4.to_string(), "v4".to_string());
        assert!(EcsResource::new(env.clone()).is_on_platform());

        env.remove(ECS_METADATA_KEY_V3);
        let ecs = EcsResource::new(env);
        assert!(ecs.is_on_platform());
        assert_eq!(ecs.get_platform(), ComputePlatform::Ecs);
    }

    #[test]
    fn is_not_ecs() {
        assert!(!EcsResource::new(HashMap::new()).is_on_platform());

        let mut env = HashMap::new();
        env.insert(ECS_METADATA_KEY_V3.to_string(), String::new());
        env.insert(ECS_METADATA_KEY_V4.to_string(), String::new());
        assert!(!EcsResource::new(env).is_on_platform());
    }
}
