//! Port of `software.amazon.kinesis.leases.ShardDetector`.
//!
//! Abstraction over Kinesis's shard-discovery APIs (`ListShards`,
//! `GetShardIterator` + `GetRecords` for child-shard discovery), used by
//! shard-sync logic; decouples `HierarchicalShardSyncer` / `LeaseCleanupManager`
//! from the raw `KinesisAsyncClient`.
//!
//! # Async
//!
//! This is an **I/O trait** (`#[async_trait]`): the Java concrete impl
//! (`KinesisShardDetector`, deferred to 6c) blocks on `KinesisAsyncClient`
//! futures via `FutureUtils.resolveOrCancelFuture`; the Rust port stays async
//! and does **not** block. All methods that make Kinesis calls are `async` and
//! return `Result<_, LeasingError>`.
//!
//! # Deviations from the Java interface
//!
//! - Java's checked-exception surface on `getChildShards`
//!   (`InterruptedException` / `ExecutionException` / `TimeoutException`) and
//!   `getListShardsResponse` (`throws Exception`) is collapsed into
//!   [`LeasingError`]; the "throws nothing" Java methods (`shard`,
//!   `listShards`, `streamIdentifier`) also return `Result<_, LeasingError>` so
//!   the whole trait has a uniform fallible async surface (the concrete detector
//!   surfaces SDK/throttling failures on every call).
//! - Method overloads are renamed: `listShards()` → [`list_shards`], the
//!   `consumerId` overloads → `*_for_consumer` variants. The
//!   `WithoutConsumingResourceNotFoundException` variants keep the explicit
//!   name (they are a behavioral toggle: propagate `ResourceNotFound` vs. swallow
//!   into an empty list).
//! - `shard(shardId)` returns `Option<Shard>` — Java returns `Shard` but may
//!   surface a cache miss (documented as nullable in callers); modeled as
//!   `Option`.
//! - Default methods that throw `UnsupportedOperationException` in Java become
//!   default trait-method bodies returning [`LeasingError::dependency`] with the
//!   same "not implemented" message (mirroring the opt-in extension-point
//!   pattern established for `LeaseRefresher`/`LeaseSerializer`).
//!
//! [`list_shards`]: ShardDetector::list_shards

use async_trait::async_trait;
use aws_sdk_kinesis::operation::list_shards::{ListShardsInput, ListShardsOutput};
use aws_sdk_kinesis::types::{ChildShard, Shard, ShardFilter};

use crate::common::StreamIdentifier;
use crate::leases::exceptions::LeasingError;

/// Abstraction over Kinesis shard-discovery APIs.
///
/// The trait is `Send + Sync` so it can be shared as `Arc<dyn ShardDetector>`
/// (e.g. by [`LeasePendingDeletion`](crate::leases::exceptions::LeasePendingDeletion)).
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait ShardDetector: Send + Sync {
    /// Gets shard based on `shard_id` (Java `shard(String)`). Returns `None` on
    /// a cache miss / unknown shard.
    async fn shard(&self, shard_id: &str) -> Result<Option<Shard>, LeasingError>;

    /// List shards (Java `listShards()`).
    async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError>;

    /// List shards for a specific consumer (Java `listShards(String consumerId)`;
    /// default delegates to [`list_shards`](ShardDetector::list_shards)).
    async fn list_shards_for_consumer(
        &self,
        _consumer_id: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        self.list_shards().await
    }

    /// Like [`list_shards`](ShardDetector::list_shards) but does **not** swallow
    /// `ResourceNotFoundException` into an empty list — it propagates instead
    /// (Java `listShardsWithoutConsumingResourceNotFoundException()`).
    async fn list_shards_without_consuming_resource_not_found_exception(
        &self,
    ) -> Result<Vec<Shard>, LeasingError> {
        Err(LeasingError::dependency(
            "listShardsWithoutConsumingResourceNotFoundException not implemented",
        ))
    }

    /// Consumer-scoped variant of
    /// [`list_shards_without_consuming_resource_not_found_exception`](ShardDetector::list_shards_without_consuming_resource_not_found_exception).
    async fn list_shards_without_consuming_resource_not_found_exception_for_consumer(
        &self,
        _consumer_id: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        Err(LeasingError::dependency(
            "listShardsWithoutConsumingResourceNotFoundException not implemented",
        ))
    }

    /// List shards with a shard filter (Java `listShardsWithFilter(ShardFilter)`).
    async fn list_shards_with_filter(
        &self,
        _shard_filter: ShardFilter,
    ) -> Result<Vec<Shard>, LeasingError> {
        Err(LeasingError::dependency(
            "listShardsWithFilter not available.",
        ))
    }

    /// Consumer-scoped variant of
    /// [`list_shards_with_filter`](ShardDetector::list_shards_with_filter).
    async fn list_shards_with_filter_for_consumer(
        &self,
        _shard_filter: ShardFilter,
        _consumer_id: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        Err(LeasingError::dependency(
            "listShardsWithFilter not available.",
        ))
    }

    /// Gets the stream identifier (Java `streamIdentifier()`).
    fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
        Err(LeasingError::dependency("StreamName not available"))
    }

    /// Gets a `ListShards` response based on the request (Java
    /// `getListShardsResponse(ListShardsRequest)`).
    async fn get_list_shards_response(
        &self,
        _request: ListShardsInput,
    ) -> Result<ListShardsOutput, LeasingError> {
        Err(LeasingError::dependency(
            "getListShardsResponse not available.",
        ))
    }

    /// Discover the child shards of `shard_id` (Java `getChildShards(String)`).
    async fn get_child_shards(&self, _shard_id: &str) -> Result<Vec<ChildShard>, LeasingError> {
        Err(LeasingError::dependency("getChildShards not available."))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn mock_shard_detector_default_variants_and_child_shards() {
        let mut mock = MockShardDetector::new();
        mock.expect_get_child_shards()
            .withf(|id| id == "shard-1")
            .returning(|_| Ok(Vec::new()));
        mock.expect_list_shards().returning(|| Ok(Vec::new()));

        assert!(mock.get_child_shards("shard-1").await.unwrap().is_empty());
        assert!(mock.list_shards().await.unwrap().is_empty());
    }
}
