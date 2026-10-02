//! Port of
//! `software.amazon.kinesis.leases.exceptions.LeasePendingDeletion`.
//!
//! Despite living in the `leases.exceptions` Java package, this is a plain
//! immutable DTO (not an exception type) — a package-organization artifact.

use std::collections::HashSet;
use std::sync::Arc;

use crate::common::StreamIdentifier;
use crate::leases::exceptions::LeasingError;
use crate::leases::{Lease, ShardDetector, ShardInfo};

/// Bundles everything the lease-cleanup manager needs to evaluate/execute
/// deletion of one lease: the stream identifier, the lease, its shard info, and
/// a shard-detector handle for live child-shard lookups.
///
/// Java is a Lombok `@Value @Accessors(fluent = true) @EqualsAndHashCode` over
/// all four fields. `ShardDetector` has no value equality (it is a trait object
/// here), so this type is **not** `PartialEq`; the lease-cleanup manager's
/// `isEnqueuedForDeletion` dedup (Java `queue.contains`) will be reimplemented
/// against lease keys in the later cleanup-manager wave rather than relying on
/// structural equality.
#[derive(Clone)]
pub struct LeasePendingDeletion {
    stream_identifier: StreamIdentifier,
    lease: Lease,
    shard_info: ShardInfo,
    shard_detector: Arc<dyn ShardDetector>,
}

impl LeasePendingDeletion {
    pub fn new(
        stream_identifier: StreamIdentifier,
        lease: Lease,
        shard_info: ShardInfo,
        shard_detector: Arc<dyn ShardDetector>,
    ) -> Self {
        Self {
            stream_identifier,
            lease,
            shard_info,
            shard_detector,
        }
    }

    pub fn stream_identifier(&self) -> &StreamIdentifier {
        &self.stream_identifier
    }
    pub fn lease(&self) -> &Lease {
        &self.lease
    }
    pub fn shard_info(&self) -> &ShardInfo {
        &self.shard_info
    }
    pub fn shard_detector(&self) -> &Arc<dyn ShardDetector> {
        &self.shard_detector
    }

    /// Discover the child shards for this lease's shard, collecting their shard
    /// IDs into a set (Java `getChildShardsFromService`).
    ///
    /// Async because [`ShardDetector::get_child_shards`] is an async I/O call
    /// (it hits Kinesis `GetShardIterator` + `GetRecords`).
    pub async fn get_child_shards_from_service(&self) -> Result<HashSet<String>, LeasingError> {
        let child_shards = self
            .shard_detector
            .get_child_shards(self.shard_info.shard_id())
            .await?;
        Ok(child_shards
            .into_iter()
            .map(|c| c.shard_id().to_string())
            .collect())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retrieval::kpl::ExtendedSequenceNumber;
    use async_trait::async_trait;
    use aws_sdk_kinesis::types::{ChildShard, Shard};

    struct FakeDetector {
        children: Vec<ChildShard>,
    }

    #[async_trait]
    impl ShardDetector for FakeDetector {
        async fn shard(&self, _shard_id: &str) -> Result<Option<Shard>, LeasingError> {
            Ok(None)
        }
        async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
            Ok(Vec::new())
        }
        async fn get_child_shards(&self, _shard_id: &str) -> Result<Vec<ChildShard>, LeasingError> {
            Ok(self.children.clone())
        }
    }

    fn child(id: &str) -> ChildShard {
        ChildShard::builder()
            .shard_id(id)
            .parent_shards("parent")
            .hash_key_range(
                aws_sdk_kinesis::types::HashKeyRange::builder()
                    .starting_hash_key("0")
                    .ending_hash_key("100")
                    .build()
                    .unwrap(),
            )
            .build()
            .unwrap()
    }

    #[tokio::test]
    async fn get_child_shards_from_service_collects_ids() {
        let detector = Arc::new(FakeDetector {
            children: vec![child("child-1"), child("child-2")],
        });
        let lpd = LeasePendingDeletion::new(
            StreamIdentifier::single_stream_instance("my-stream"),
            Lease::default(),
            ShardInfo::single_stream(
                "shard-1",
                None,
                Vec::<String>::new(),
                Some(ExtendedSequenceNumber::shard_end()),
            ),
            detector,
        );
        let ids = lpd.get_child_shards_from_service().await.unwrap();
        assert_eq!(ids.len(), 2);
        assert!(ids.contains("child-1"));
        assert!(ids.contains("child-2"));
        assert_eq!(lpd.stream_identifier().stream_name(), "my-stream");
        assert_eq!(lpd.shard_info().shard_id(), "shard-1");
    }
}
