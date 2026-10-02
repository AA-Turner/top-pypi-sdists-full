//! Port of `LeaseCleanupManagerTest`.
//!
//! The Java tests mock `LeaseCoordinator`/`LeaseRefresher`/`ShardDetector` and
//! drive `cleanupLeases()` directly. We reproduce the split/merge deletion-gate
//! scenarios, the "not deleted when child at TRIM_HORIZON/AT_TIMESTAMP" cases,
//! the "not deleted when parents still present" case, the garbage-shard
//! (ResourceNotFound) deletion, and start/shutdown idempotency.

use super::*;
use crate::common::StreamIdentifier;
use crate::leases::{Lease, LeaseRefresher, MockLeaseCoordinator, ShardDetector};
use crate::metrics::NullMetricsFactory;
use crate::retrieval::kpl::ExtendedSequenceNumber;
use async_trait::async_trait;
use aws_sdk_kinesis::types::{ChildShard, HashKeyRange, Shard};
use std::sync::Mutex as StdMutex;

const STREAM_NAME: &str = "streamName";

fn shard_info(parent_shard_ids: Vec<String>) -> ShardInfo {
    ShardInfo::single_stream(
        "shardId",
        Some("concurrencyToken".to_string()),
        parent_shard_ids,
        Some(ExtendedSequenceNumber::latest()),
    )
}

fn create_lease(
    lease_key: &str,
    lease_owner: &str,
    parent_shard_ids: Vec<String>,
    child_shard_ids: Vec<String>,
    checkpoint: ExtendedSequenceNumber,
) -> Lease {
    let mut lease = Lease::default();
    lease.set_lease_key(lease_key);
    lease.set_lease_owner(Some(lease_owner.to_string()));
    lease.set_parent_shard_ids(parent_shard_ids);
    lease.set_child_shard_ids(child_shard_ids);
    lease.set_checkpoint(checkpoint);
    lease
}

fn child(id: &str, parents: &[&str], start: &str, end: &str) -> ChildShard {
    ChildShard::builder()
        .shard_id(id)
        .set_parent_shards(Some(parents.iter().map(|s| s.to_string()).collect()))
        .hash_key_range(
            HashKeyRange::builder()
                .starting_hash_key(start)
                .ending_hash_key(end)
                .build()
                .unwrap(),
        )
        .build()
        .unwrap()
}

fn child_shards_for_split() -> Vec<ChildShard> {
    vec![
        child("leftChild", &["splitParent"], "0", "49"),
        child("rightChild", &["splitParent"], "50", "99"),
    ]
}

fn child_shards_for_merge() -> Vec<ChildShard> {
    vec![child(
        "onlyChild",
        &["mergeParent1", "mergeParent2"],
        "0",
        "99",
    )]
}

/// A `ShardDetector` that returns a fixed set of child shards (or a
/// ResourceNotFound error).
struct FakeDetector {
    children: Vec<ChildShard>,
    resource_not_found: bool,
    calls: StdMutex<usize>,
}

impl FakeDetector {
    fn new(children: Vec<ChildShard>) -> Arc<Self> {
        Arc::new(Self {
            children,
            resource_not_found: false,
            calls: StdMutex::new(0),
        })
    }
    fn not_found() -> Arc<Self> {
        Arc::new(Self {
            children: Vec::new(),
            resource_not_found: true,
            calls: StdMutex::new(0),
        })
    }
    fn child_shard_calls(&self) -> usize {
        *self.calls.lock().unwrap()
    }
}

#[async_trait]
impl ShardDetector for FakeDetector {
    async fn shard(&self, _id: &str) -> Result<Option<Shard>, LeasingError> {
        Ok(None)
    }
    async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
        Ok(Vec::new())
    }
    async fn get_child_shards(&self, _shard_id: &str) -> Result<Vec<ChildShard>, LeasingError> {
        *self.calls.lock().unwrap() += 1;
        if self.resource_not_found {
            // Wrap a message containing "ResourceNotFoundException" so
            // is_resource_not_found detects it.
            Err(LeasingError::dependency(
                "ResourceNotFoundException: shard gone",
            ))
        } else {
            Ok(self.children.clone())
        }
    }
}

/// Build a `MockLeaseRefresher` mapping lease keys to leases, and recording
/// deleted lease keys. `present_leases` maps lease key → lease.
fn build_refresher(
    present_leases: Vec<Lease>,
    deleted: Arc<StdMutex<Vec<String>>>,
) -> crate::leases::MockLeaseRefresher {
    let mut refresher = crate::leases::MockLeaseRefresher::new();
    let map: std::collections::HashMap<String, Lease> = present_leases
        .into_iter()
        .map(|l| (l.lease_key().unwrap().to_string(), l))
        .collect();
    refresher
        .expect_get_lease()
        .returning(move |key| Ok(map.get(key).cloned()));
    let deleted_clone = deleted.clone();
    refresher.expect_delete_lease().returning(move |lease| {
        deleted_clone
            .lock()
            .unwrap()
            .push(lease.lease_key().unwrap().to_string());
        Ok(())
    });
    refresher
        .expect_update_lease_with_meta_info()
        .returning(|_, _| Ok(()));
    refresher
}

fn manager_with(
    refresher: crate::leases::MockLeaseRefresher,
    cleanup_completed: bool,
) -> LeaseCleanupManager {
    let refresher_arc: Arc<dyn LeaseRefresher> = Arc::new(refresher);
    let mut coordinator = MockLeaseCoordinator::new();
    coordinator
        .expect_lease_refresher()
        .returning(move || refresher_arc.clone());
    let coordinator: Arc<dyn LeaseCoordinator> = Arc::new(coordinator);
    LeaseCleanupManager::new(
        coordinator,
        Arc::new(NullMetricsFactory),
        cleanup_completed,
        1000, // lease cleanup interval
        0,    // completed interval (always due)
        0,    // garbage interval (always due)
    )
}

/// Runs the completed-shard deletion scenario and returns the deleted lease keys.
async fn run_completed_shard_case(
    shard_info: ShardInfo,
    child_shards: Vec<ChildShard>,
    child_checkpoint: ExtendedSequenceNumber,
    cleanup_completed: bool,
    child_leases_present: bool,
) -> (Vec<String>, usize) {
    let detector = FakeDetector::new(child_shards.clone());

    // Parent lease being cleaned up (has children set).
    let child_ids: Vec<String> = child_shards
        .iter()
        .map(|c| c.shard_id().to_string())
        .collect();
    let held_lease = create_lease(
        shard_info.shard_id(),
        "leaseOwner",
        shard_info.parent_shard_ids(),
        child_ids.clone(),
        ExtendedSequenceNumber::latest(),
    );

    let mut present = vec![held_lease.clone()];
    if child_leases_present {
        // Child leases: parent = the completed shard, at `child_checkpoint`.
        for c in &child_shards {
            present.push(create_lease(
                &shard_info.lease_key_with_override(c.shard_id()),
                "leaseOwner",
                vec![shard_info.shard_id().to_string()],
                Vec::new(),
                child_checkpoint.clone(),
            ));
        }
    }
    // Parent leases (for the parent-shards-deleted check): if the shard_info has
    // parents, they must be ABSENT for deletion → don't add them.

    let deleted = Arc::new(StdMutex::new(Vec::<String>::new()));
    let refresher = build_refresher(present, deleted.clone());
    let manager = manager_with(refresher, cleanup_completed);

    let lpd = LeasePendingDeletion::new(
        StreamIdentifier::single_stream_instance(STREAM_NAME),
        held_lease,
        shard_info,
        detector.clone(),
    );
    manager.enqueue_for_deletion(lpd);
    manager.cleanup_leases().await;

    let keys = deleted.lock().unwrap().clone();
    (keys, detector.child_shard_calls())
}

#[tokio::test]
async fn subsequent_starts_are_idempotent() {
    let refresher = crate::leases::MockLeaseRefresher::new();
    let manager = Arc::new(manager_with(refresher, true));
    manager.start();
    assert!(manager.is_running());
    manager.start(); // no-op
    assert!(manager.is_running());
    manager.shutdown();
}

#[tokio::test]
async fn subsequent_shutdowns_are_idempotent() {
    let refresher = crate::leases::MockLeaseRefresher::new();
    let manager = Arc::new(manager_with(refresher, true));
    manager.start();
    assert!(manager.is_running());
    manager.shutdown();
    assert!(!manager.is_running());
    manager.shutdown(); // no-op
    assert!(!manager.is_running());
}

#[tokio::test]
async fn parent_shard_lease_deleted_split_case() {
    let (deleted, child_calls) = run_completed_shard_case(
        shard_info(Vec::new()),
        child_shards_for_split(),
        ExtendedSequenceNumber::latest(),
        true,
        true,
    )
    .await;
    assert_eq!(deleted.len(), 1);
    assert_eq!(deleted[0], "shardId");
    assert_eq!(child_calls, 1);
}

#[tokio::test]
async fn parent_shard_lease_deleted_merge_case() {
    let (deleted, child_calls) = run_completed_shard_case(
        shard_info(Vec::new()),
        child_shards_for_merge(),
        ExtendedSequenceNumber::latest(),
        true,
        true,
    )
    .await;
    assert_eq!(deleted.len(), 1);
    assert_eq!(child_calls, 1);
}

#[tokio::test]
async fn no_leases_deleted_when_not_enabled() {
    let (deleted, _) = run_completed_shard_case(
        shard_info(Vec::new()),
        child_shards_for_split(),
        ExtendedSequenceNumber::latest(),
        false, // cleanup disabled
        true,
    )
    .await;
    assert_eq!(deleted.len(), 0);
}

#[tokio::test]
async fn no_cleanup_when_child_shard_leases_missing() {
    // A child lease unexpectedly missing → completed path errors (swallowed),
    // and (garbage path not triggered since we found children) → no deletion.
    let (deleted, _) = run_completed_shard_case(
        shard_info(Vec::new()),
        child_shards_for_split(),
        ExtendedSequenceNumber::latest(),
        true,
        false, // child leases NOT present
    )
    .await;
    assert_eq!(deleted.len(), 0);
}

#[tokio::test]
async fn parent_lease_not_deleted_when_child_at_trim() {
    let (deleted, _) = run_completed_shard_case(
        shard_info(Vec::new()),
        child_shards_for_split(),
        ExtendedSequenceNumber::trim_horizon(),
        true,
        true,
    )
    .await;
    assert_eq!(deleted.len(), 0);
}

#[tokio::test]
async fn parent_lease_not_deleted_when_child_at_timestamp() {
    let (deleted, _) = run_completed_shard_case(
        shard_info(Vec::new()),
        child_shards_for_split(),
        ExtendedSequenceNumber::at_timestamp(),
        true,
        true,
    )
    .await;
    assert_eq!(deleted.len(), 0);
}

#[tokio::test]
async fn lease_not_deleted_when_parents_still_present() {
    // ShardInfo with a parent → the parent lease is present → not deletable.
    let si = shard_info(vec!["parent".to_string()]);
    let detector = FakeDetector::new(child_shards_for_merge());
    let child_ids: Vec<String> = child_shards_for_merge()
        .iter()
        .map(|c| c.shard_id().to_string())
        .collect();
    let held_lease = create_lease(
        si.shard_id(),
        "leaseOwner",
        si.parent_shard_ids(),
        child_ids,
        ExtendedSequenceNumber::latest(),
    );

    let mut present = vec![held_lease.clone()];
    // Child leases present + processed.
    for c in child_shards_for_merge() {
        present.push(create_lease(
            &si.lease_key_with_override(c.shard_id()),
            "leaseOwner",
            vec![si.shard_id().to_string()],
            Vec::new(),
            ExtendedSequenceNumber::latest(),
        ));
    }
    // Parent lease PRESENT (blocks deletion).
    present.push(create_lease(
        &si.lease_key_with_override("parent"),
        "leaseOwner",
        Vec::new(),
        vec![si.shard_id().to_string()],
        ExtendedSequenceNumber::latest(),
    ));

    let deleted = Arc::new(StdMutex::new(Vec::<String>::new()));
    let refresher = build_refresher(present, deleted.clone());
    let manager = manager_with(refresher, true);
    manager.enqueue_for_deletion(LeasePendingDeletion::new(
        StreamIdentifier::single_stream_instance(STREAM_NAME),
        held_lease,
        si,
        detector,
    ));
    manager.cleanup_leases().await;
    assert_eq!(deleted.lock().unwrap().len(), 0);
}

#[tokio::test]
async fn lease_deleted_when_shard_does_not_exist() {
    // Garbage collection: getChildShards throws ResourceNotFound → lease deleted.
    let detector = FakeDetector::not_found();
    let held_lease = create_lease(
        "shardId",
        "leaseOwner",
        vec!["parentShardId".to_string()],
        Vec::new(),
        ExtendedSequenceNumber::latest(),
    );
    let deleted = Arc::new(StdMutex::new(Vec::<String>::new()));
    let refresher = build_refresher(vec![held_lease.clone()], deleted.clone());
    let manager = manager_with(refresher, true);

    manager.enqueue_for_deletion(LeasePendingDeletion::new(
        StreamIdentifier::single_stream_instance(STREAM_NAME),
        held_lease,
        shard_info(Vec::new()),
        detector.clone(),
    ));
    manager.cleanup_leases().await;

    assert_eq!(detector.child_shard_calls(), 1);
    assert_eq!(deleted.lock().unwrap().as_slice(), &["shardId".to_string()]);
}

/// Port of `LeaseCleanupManagerTest.testLeaseDeletedWhenShardDoesNotExistAndCleanupCompletedLeaseDisabled`.
///
/// The garbage-collection path (getChildShards → ResourceNotFound → delete the
/// lease) fires even when completed-lease cleanup is *disabled*.
#[tokio::test]
async fn lease_deleted_when_shard_does_not_exist_and_cleanup_completed_disabled() {
    let detector = FakeDetector::not_found();
    let held_lease = create_lease(
        "shardId",
        "leaseOwner",
        vec!["parentShardId".to_string()],
        Vec::new(),
        ExtendedSequenceNumber::latest(),
    );
    let deleted = Arc::new(StdMutex::new(Vec::<String>::new()));
    let refresher = build_refresher(vec![held_lease.clone()], deleted.clone());
    // cleanup_completed = false — garbage collection must still delete.
    let manager = manager_with(refresher, false);

    manager.enqueue_for_deletion(LeasePendingDeletion::new(
        StreamIdentifier::single_stream_instance(STREAM_NAME),
        held_lease,
        shard_info(Vec::new()),
        detector.clone(),
    ));
    manager.cleanup_leases().await;

    assert_eq!(detector.child_shard_calls(), 1);
    assert_eq!(deleted.lock().unwrap().as_slice(), &["shardId".to_string()]);
}

#[tokio::test]
async fn is_enqueued_for_deletion_by_lease_key() {
    let refresher = crate::leases::MockLeaseRefresher::new();
    let manager = manager_with(refresher, true);
    let detector = FakeDetector::new(Vec::new());
    let held = create_lease(
        "shardId",
        "o",
        Vec::new(),
        Vec::new(),
        ExtendedSequenceNumber::latest(),
    );
    let lpd = LeasePendingDeletion::new(
        StreamIdentifier::single_stream_instance(STREAM_NAME),
        held,
        shard_info(Vec::new()),
        detector,
    );
    assert!(!manager.is_enqueued_for_deletion(&lpd));
    manager.enqueue_for_deletion(lpd.clone());
    assert!(manager.is_enqueued_for_deletion(&lpd));
}
