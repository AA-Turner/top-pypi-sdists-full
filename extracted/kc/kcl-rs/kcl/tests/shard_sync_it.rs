//! Integration test — port of the Java `leases/ShardSyncTaskIntegrationTest.java`.
//!
//! Runs one real shard-sync pass: create a real Kinesis stream, discover its
//! shards with a real [`KinesisShardDetector`] (`ListShards`), then run a
//! [`ShardSyncTask`] (delegating to [`HierarchicalShardSyncer`]) against a real
//! DynamoDB lease table and assert a lease was created for every shard id.
//!
//! This mirrors the Java `testCall`: `shardDetector.listShards()` collects the
//! shard ids, `new ShardSyncTask(...).call()` bootstraps the leases, and the
//! test asserts `leaseRefresher.listLeases()` has exactly one lease per shard,
//! keyed by shard id.
//!
//! Every test is `#[ignore]` (see the module doc in `common/mod.rs`). Run with:
//! `cargo test -p kcl -- --ignored` (optionally `AWS_ENDPOINT_URL=...` to
//! redirect to LocalStack).

mod common;

use std::collections::HashSet;
use std::sync::Arc;
use std::time::Duration;

use aws_sdk_dynamodb::types::BillingMode;

use kcl::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamIdentifier};
use kcl::leases::{
    HierarchicalShardSyncer, KinesisShardDetector, LeaseRefresher, ShardDetector, ShardSyncTask,
};
use kcl::lifecycle::ConsumerTask;
use kcl::metrics::NullMetricsFactory;

use common::{
    create_stream_and_wait, delete_stream_best_effort, dynamodb_client, kinesis_client,
    unique_table_name, LeaseTableGuard,
};

// Constants mirroring the Java ShardSyncTaskIntegrationTest.
const USE_CONSISTENT_READS: bool = true;
const MAX_CACHE_MISSES_BEFORE_RELOAD: i32 = 1000;
const LIST_SHARDS_CACHE_ALLOWED_AGE_IN_SECONDS: i64 = 30;
const CACHE_MISS_WARNING_MODULUS: i32 = 250;
const LIST_SHARDS_BACKOFF_MILLIS: u64 = 500;
const MAX_LIST_SHARDS_RETRY_ATTEMPTS: i32 = 50;
const KINESIS_REQUEST_TIMEOUT: Duration = Duration::from_secs(5);

/// Port of `ShardSyncTaskIntegrationTest.testCall`.
///
/// Note the deviation from Java's field name: `USE_CONSISTENT_READS` /
/// `MAX_CACHE_MISSES_BEFORE_RELOAD` etc. are threaded straight through to the
/// real detector; the lease table is a per-run unique table (via
/// `LeaseTableGuard`) rather than the Java hard-coded shared table name.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn test_call_creates_leases_for_all_shards() {
    common::init_test_tracing();
    let kinesis = kinesis_client().await;
    let dynamo = dynamodb_client().await;

    let stream_name = unique_table_name("shardsync-stream");
    // Two shards, so the sync creates two leases (a non-trivial count).
    create_stream_and_wait(&kinesis, &stream_name, 2).await;

    // Real DynamoDB lease table (created + cleared by the guard, matching the
    // Java @Before: create-if-not-exists + deleteAll).
    let guard = LeaseTableGuard::setup(
        dynamo.clone(),
        unique_table_name("shardsync-leases"),
        BillingMode::PayPerRequest,
    )
    .await;

    // Real KinesisShardDetector over the live stream.
    let shard_detector: Arc<dyn ShardDetector> = Arc::new(KinesisShardDetector::new(
        kinesis.clone(),
        StreamIdentifier::single_stream_instance(&stream_name),
        LIST_SHARDS_BACKOFF_MILLIS,
        MAX_LIST_SHARDS_RETRY_ATTEMPTS,
        LIST_SHARDS_CACHE_ALLOWED_AGE_IN_SECONDS,
        MAX_CACHE_MISSES_BEFORE_RELOAD,
        CACHE_MISS_WARNING_MODULUS,
        KINESIS_REQUEST_TIMEOUT,
    ));
    let _ = USE_CONSISTENT_READS; // consistency handled by the harness's refresher

    // Java: shardIds = shardDetector.listShards().stream().map(Shard::shardId)...
    let shard_ids: HashSet<String> = shard_detector
        .list_shards()
        .await
        .expect("list_shards failed")
        .into_iter()
        .map(|s| s.shard_id().to_string())
        .collect();
    assert_eq!(shard_ids.len(), 2, "expected two shards on the stream");

    let hierarchical_shard_syncer = Arc::new(HierarchicalShardSyncer::new());

    // ShardSyncTask(shardDetector, leaseRefresher, LATEST, cleanup=false,
    // gc=true, ignoreUnexpectedChildShards=false, idle=0, syncer, nullMetrics).
    let sync_task = ShardSyncTask::new(
        Arc::clone(&shard_detector),
        guard.refresher.clone() as Arc<dyn LeaseRefresher>,
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest),
        /* cleanup_leases_upon_shard_completion = */ false,
        /* garbage_collect_leases = */ true,
        /* ignore_unexpected_child_shards = */ false,
        /* shard_sync_task_idle_time_millis = */ 0,
        hierarchical_shard_syncer,
        Arc::new(NullMetricsFactory::new()),
    );

    let result = sync_task.call().await;
    assert!(
        result.exception().is_none(),
        "shard-sync task reported an error: {:?}",
        result.exception().map(|e| e.to_string())
    );

    // Verify that all shardIds had leases for them.
    let leases = guard
        .refresher
        .list_leases()
        .await
        .expect("list_leases failed");
    let lease_keys: HashSet<String> = leases
        .iter()
        .map(|l| l.lease_key().expect("lease has a key").to_string())
        .collect();

    assert_eq!(
        shard_ids.len(),
        leases.len(),
        "one lease per shard expected"
    );
    // shardIds.removeAll(leaseKeys) should leave nothing.
    let missing: Vec<&String> = shard_ids.difference(&lease_keys).collect();
    assert!(missing.is_empty(), "shards without a lease: {missing:?}");

    guard.teardown().await;
    delete_stream_best_effort(&kinesis, &stream_name).await;
}
