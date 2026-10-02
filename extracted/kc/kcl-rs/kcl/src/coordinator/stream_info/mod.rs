//! Port of `software.amazon.kinesis.coordinator.streamInfo`.
//!
//! StreamInfo metadata tracking: the `StreamInfo` value type, its DAO on top of
//! `CoordinatorStateDAO`, the process-global `StreamIdCache` singleton and its
//! backing `StreamIdCacheManager`, plus the two enums `StreamInfoMode` and
//! `StreamIdOnboardingState`.

pub mod stream_id_cache;
pub mod stream_id_cache_manager;
pub mod stream_id_onboarding_state;
// `stream_info::stream_info` mirrors the Java `StreamInfo` class inside its
// package (1:1 package/class mapping); the repeated name is intentional.
#[allow(clippy::module_inception)]
pub mod stream_info;
pub mod stream_info_dao;
pub mod stream_info_mode;

pub use stream_id_cache::{StreamIdCache, StreamIdCacheResolverBridge, StreamIdResolver};
pub use stream_id_cache_manager::StreamIdCacheManager;
pub use stream_id_onboarding_state::StreamIdOnboardingState;
pub use stream_info::{StreamInfo, STREAM_ID_ATTRIBUTE_NAME};
pub use stream_info_dao::{StreamInfoDAO, StreamInfoStore};
pub use stream_info_mode::StreamInfoMode;

#[cfg(test)]
pub use stream_id_cache::MockStreamIdResolver;
#[cfg(test)]
pub use stream_info_dao::MockStreamInfoStore;
