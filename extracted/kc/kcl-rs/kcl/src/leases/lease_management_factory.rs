//! Port of `software.amazon.kinesis.leases.LeaseManagementFactory`.
//!
//! Abstract factory / DI composition root for constructing the concrete
//! lease-management collaborators
//! ([`LeaseCoordinator`](crate::leases::LeaseCoordinator),
//! [`LeaseRefresher`](crate::leases::LeaseRefresher),
//! [`LeaseCleanupManager`](crate::leases::port_stubs::LeaseCleanupManager),
//! [`ShardDetector`](crate::leases::ShardDetector),
//! [`ShardSyncTaskManager`](crate::leases::port_stubs::ShardSyncTaskManager),
//! `StreamIdCacheManager`, `StreamInfoManager`) from a shared config.
//!
//! # Sync
//!
//! Construction is synchronous (no I/O), so this is a **plain sync trait**.
//!
//! # Deviations
//!
//! - **`createLeaseRefresher()` returns `Box<dyn LeaseRefresher>`** rather than
//!   the concrete `DynamoDBLeaseRefresher` (Java's leaky abstraction — the same
//!   pattern flagged on `LeaseCoordinator`); factory consumers only need the
//!   trait. `createLeaseCoordinator` likewise returns
//!   `Box<dyn LeaseCoordinator + Send + Sync>` and `createShardDetector` returns
//!   `Box<dyn ShardDetector>`.
//! - `MetricsFactory` params → `Arc<dyn MetricsFactory + Send + Sync>`.
//! - Java `default` methods that throw `UnsupportedOperationException` (the
//!   deprecated `createLeaseCoordinator`/`createShardSyncTaskManager` overloads,
//!   the deprecated no-arg `createShardDetector`) become default trait-method
//!   bodies returning `Err(`[`LeasingError::dependency`]`)` with the same intent;
//!   `create_shard_detector` (the `StreamConfig` overload) is also a fallible
//!   default (Java throws `UnsupportedOperationException` there too).
//! - `ConcurrentMap<ShardInfo, ShardConsumer>` →
//!   `HashMap<ShardInfo, Arc<lifecycle::ShardConsumer>>` (the real `ShardConsumer`
//!   landed in the lifecycle wave 7b; shared via `Arc` like Java's `ConcurrentMap`);
//!   `Map<StreamIdentifier, StreamConfig>` → `HashMap<StreamIdentifier, StreamConfig>`.
//! - `StreamIdCacheManager` / `StreamInfoManager` and their params are the
//!   `port_stubs` placeholders (owned by the coordinator wave).
//! - The nested `StreamIdOnboardingState` / `StreamInfoMode` enums are stubbed
//!   (see [`port_stubs`](crate::leases::port_stubs)).

use std::collections::HashMap;
use std::sync::Arc;

use crate::common::{StreamConfig, StreamIdentifier};
use crate::coordinator::{
    DeletedStreamListProvider, StreamIdCacheManager, StreamIdOnboardingState, StreamInfoDAO,
    StreamInfoManager, StreamInfoMode,
};
use crate::leases::exceptions::LeasingError;
use crate::leases::lease_cleanup_manager::LeaseCleanupManager;
use crate::leases::shard_sync_task_manager::ShardSyncTaskManager;
use crate::leases::{LeaseCoordinator, LeaseRefresher, ShardDetector, ShardInfo};
use crate::lifecycle::ShardConsumer;
use crate::metrics::MetricsFactory;

/// Constructs the lease-management subsystem's collaborators from a shared
/// config.
#[cfg_attr(test, mockall::automock)]
pub trait LeaseManagementFactory: Send + Sync {
    /// Create a [`LeaseCoordinator`] (Java `createLeaseCoordinator(MetricsFactory)`).
    fn create_lease_coordinator(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Box<dyn LeaseCoordinator + Send + Sync>;

    /// Deprecated overload taking a shard-info→consumer map (Java default:
    /// unsupported).
    fn create_lease_coordinator_with_consumer_map(
        &self,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _shard_info_shard_consumer_map: HashMap<ShardInfo, Arc<ShardConsumer>>,
    ) -> Result<Box<dyn LeaseCoordinator + Send + Sync>, LeasingError> {
        Err(LeasingError::dependency("Not implemented"))
    }

    /// Overload taking a shard-info→consumer map and a stream-id cache manager
    /// (Java default: unsupported).
    fn create_lease_coordinator_with_cache_manager(
        &self,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _shard_info_shard_consumer_map: HashMap<ShardInfo, Arc<ShardConsumer>>,
        _stream_id_cache_manager: StreamIdCacheManager,
    ) -> Result<Box<dyn LeaseCoordinator + Send + Sync>, LeasingError> {
        Err(LeasingError::dependency("Not implemented"))
    }

    /// Deprecated shard-sync-task-manager factory (Java default: unsupported).
    fn create_shard_sync_task_manager(
        &self,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Result<Box<ShardSyncTaskManager>, LeasingError> {
        Err(LeasingError::dependency("Deprecated"))
    }

    /// Deprecated shard-sync-task-manager factory with stream config (Java
    /// default: unsupported).
    fn create_shard_sync_task_manager_with_config(
        &self,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _stream_config: StreamConfig,
    ) -> Result<Box<ShardSyncTaskManager>, LeasingError> {
        Err(LeasingError::dependency("Deprecated"))
    }

    /// Deprecated shard-sync-task-manager factory with a deleted-stream-list
    /// provider (Java default: unsupported). The provider is shared (`Arc`):
    /// the syncer records deleted streams into the Scheduler's own instance so
    /// the Scheduler can purge them during its periodic stream sync.
    fn create_shard_sync_task_manager_with_deleted_streams(
        &self,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _stream_config: StreamConfig,
        _deleted_stream_list_provider: Arc<DeletedStreamListProvider>,
    ) -> Result<Box<ShardSyncTaskManager>, LeasingError> {
        Err(LeasingError::dependency(
            "createShardSyncTaskManager method not implemented",
        ))
    }

    /// Shard-sync-task-manager factory with a stream-info manager (Java default:
    /// unsupported).
    fn create_shard_sync_task_manager_with_stream_info(
        &self,
        _metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        _stream_config: StreamConfig,
        _deleted_stream_list_provider: Arc<DeletedStreamListProvider>,
        _stream_info_manager: StreamInfoManager,
    ) -> Result<Box<ShardSyncTaskManager>, LeasingError> {
        Err(LeasingError::dependency(
            "createShardSyncTaskManager method not implemented",
        ))
    }

    /// Create a [`LeaseRefresher`] (Java `createLeaseRefresher()`; returns the
    /// concrete `DynamoDBLeaseRefresher` in Java — here a boxed trait object).
    fn create_lease_refresher(&self) -> Box<dyn LeaseRefresher>;

    /// Deprecated no-arg shard-detector factory (Java default: unsupported).
    fn create_shard_detector(&self) -> Result<Box<dyn ShardDetector>, LeasingError> {
        Err(LeasingError::dependency("Deprecated"))
    }

    /// Create a [`ShardDetector`] for a stream (Java
    /// `createShardDetector(StreamConfig)`; Java default: unsupported).
    fn create_shard_detector_for_stream(
        &self,
        _stream_config: StreamConfig,
    ) -> Result<Box<dyn ShardDetector>, LeasingError> {
        Err(LeasingError::dependency("Not implemented"))
    }

    /// Create a [`LeaseCleanupManager`].
    fn create_lease_cleanup_manager(
        &self,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> Box<LeaseCleanupManager>;

    /// Create a `StreamIdCacheManager`.
    #[allow(clippy::too_many_arguments)]
    fn create_stream_id_cache_manager(
        &self,
        stream_info_dao: StreamInfoDAO,
        current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
        stream_id_onboarding_state: StreamIdOnboardingState,
        is_multi_stream_mode: bool,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    ) -> StreamIdCacheManager;

    /// Create a `StreamInfoManager`.
    #[allow(clippy::too_many_arguments)]
    fn create_stream_info_manager(
        &self,
        current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
        stream_info_dao: StreamInfoDAO,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        is_multi_stream_mode: bool,
        stream_info_backfill_interval_millis: i64,
        stream_info_mode: StreamInfoMode,
        stream_id_onboarding_state: StreamIdOnboardingState,
    ) -> StreamInfoManager;
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::NullMetricsFactory;

    #[test]
    fn mock_factory_default_methods_are_unsupported() {
        // `mockall::automock` mocks *all* trait methods (including `default`s),
        // so a generated mock's default methods panic if called without an
        // expectation (the automock caveat noted in PORTING.md). We therefore
        // verify the opt-in extension points return `Err(unsupported)` via a
        // hand-written minimal impl exercising the real default bodies.
        struct Minimal;
        impl LeaseManagementFactory for Minimal {
            fn create_lease_coordinator(
                &self,
                _m: Arc<dyn MetricsFactory + Send + Sync>,
            ) -> Box<dyn LeaseCoordinator + Send + Sync> {
                unimplemented!()
            }
            fn create_lease_refresher(&self) -> Box<dyn LeaseRefresher> {
                unimplemented!()
            }
            fn create_lease_cleanup_manager(
                &self,
                _m: Arc<dyn MetricsFactory + Send + Sync>,
            ) -> Box<crate::leases::lease_cleanup_manager::LeaseCleanupManager> {
                unimplemented!()
            }
            fn create_stream_id_cache_manager(
                &self,
                _d: StreamInfoDAO,
                _c: HashMap<StreamIdentifier, StreamConfig>,
                _s: StreamIdOnboardingState,
                _m: bool,
                _mf: Arc<dyn MetricsFactory + Send + Sync>,
            ) -> StreamIdCacheManager {
                unimplemented!()
            }
            fn create_stream_info_manager(
                &self,
                _c: HashMap<StreamIdentifier, StreamConfig>,
                _d: StreamInfoDAO,
                _mf: Arc<dyn MetricsFactory + Send + Sync>,
                _m: bool,
                _b: i64,
                _sm: StreamInfoMode,
                _s: StreamIdOnboardingState,
            ) -> StreamInfoManager {
                unimplemented!()
            }
        }
        let f = Minimal;
        let mf: Arc<dyn MetricsFactory + Send + Sync> = Arc::new(NullMetricsFactory);
        assert!(f.create_shard_sync_task_manager(mf.clone()).is_err());
        assert!(f.create_shard_detector().is_err());
        assert!(f
            .create_shard_detector_for_stream(dummy_stream_config())
            .is_err());
    }

    fn dummy_stream_config() -> StreamConfig {
        use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
        StreamConfig::new(
            StreamIdentifier::single_stream_instance("s"),
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        )
    }
}
