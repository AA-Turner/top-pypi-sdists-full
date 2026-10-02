//! Shared integration-test harness for the KCL Rust port.
//!
//! These tests are ports of the Java `*IntegrationTest` files that the upstream
//! project runs against **real AWS** (via Maven Failsafe / the
//! `run_integ_tests.yml` CI). They exercise behaviors the mock-based unit tests
//! cannot: real DynamoDB conditional writes (optimistic concurrency), read-back
//! verification, table creation, GSI creation, etc.
//!
//! # Targeting AWS (default) and redirecting to LocalStack
//!
//! The clients are built from the **ambient AWS config** —
//! `aws_config::defaults(BehaviorVersion::latest())` — which already honors the
//! standard environment (`AWS_PROFILE`, `AWS_REGION`, and the full credential
//! chain). If the standard `AWS_ENDPOINT_URL` env var is set, it is applied to
//! every service client (`endpoint_url(...)`). Nothing here is LocalStack-
//! specific; pointing `AWS_ENDPOINT_URL` at a LocalStack instance is just one
//! use of that standard variable.
//!
//! # Running
//!
//! Every integration `#[test]`/`#[tokio::test]` is annotated
//! `#[ignore = "integration: ..."]`, so the default `cargo test` skips them and
//! stays hermetic/offline. Run them with:
//!
//! ```bash
//! cargo test -p kcl -- --ignored
//! # redirect to LocalStack:
//! AWS_ENDPOINT_URL=http://localhost:4566 AWS_REGION=us-east-1 \
//! AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test \
//!   cargo test -p kcl -- --ignored
//! ```
//!
//! There is no credential/endpoint short-circuit: running `--ignored` is an
//! explicit request to exercise these tests, so on a machine with neither real
//! AWS credentials nor `AWS_ENDPOINT_URL` the tests run and fail loudly (the
//! SDK errors on the missing credential chain) rather than passing vacuously.
//! This also applies when `AWS_ENDPOINT_URL` is set: a redirected endpoint gets
//! no implicit credentials either, so pointing at LocalStack without exporting
//! `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` (or an equivalent profile) fails
//! the same way. Keep them out of a run by simply not passing `--ignored`.

// The harness is `mod common;`-included by several integration test binaries.
// Not every binary uses every helper, so silence the per-binary dead-code
// warnings (a helper unused by one test file is used by another).
#![allow(dead_code)]

use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::time::Duration;

use aws_sdk_dynamodb::types::BillingMode;

use aws_sdk_dynamodb::Client as DynamoDbClient;
use kcl::leases::dynamodb::{
    DynamoDBLeaseRefresher, DynamoDBLeaseSerializer, NoopTableCreatorCallback, RefresherTableConfig,
};
use kcl::leases::{Lease, LeaseRefresher};
use kcl::retrieval::kpl::ExtendedSequenceNumber;

/// Prefix for every resource (table) this harness creates, so leaked resources
/// are easy to identify and sweep.
pub const RESOURCE_PREFIX: &str = "kclrs-it-";

/// Default DynamoDB request timeout used by the refreshers in these tests
/// (mirrors `LeaseManagementConfig.DEFAULT_REQUEST_TIMEOUT` = 60s).
pub const DEFAULT_REQUEST_TIMEOUT: Duration = Duration::from_secs(60);

// ---------------------------------------------------------------------------
// Test observability
// ---------------------------------------------------------------------------

/// Install a `tracing` subscriber for an integration test.
///
/// Without this every `tracing::info!/warn!` emitted by the harness *and the
/// KCL itself* is silently dropped, so a failed AWS run produces no evidence.
/// Timestamped `fmt` output goes through the test writer (visible on failure or
/// with `--nocapture`); the filter honors `RUST_LOG` and defaults to `info`.
///
/// Call at the top of every `#[tokio::test]`; `try_init` makes repeated calls
/// (tests sharing one process) a no-op.
pub fn init_test_tracing() {
    use tracing_subscriber::EnvFilter;
    let _ = tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .with_test_writer()
        .try_init();
}

/// The record-consumption wait budget for the end-to-end canaries.
///
/// Java's `TestConsumer.run()` sleeps a fixed **15 minutes**; the ported driver
/// polls instead, bounded by this timeout. 300s proved too tight under
/// account-parallel cold starts (5 canaries sharing API quotas), so the default
/// is 600s, overridable via `KCLRS_IT_AWAIT_SECS`.
pub fn await_records_timeout() -> Duration {
    let secs = std::env::var("KCLRS_IT_AWAIT_SECS")
        .ok()
        .and_then(|v| v.parse::<u64>().ok())
        .unwrap_or(600);
    Duration::from_secs(secs)
}

// ---------------------------------------------------------------------------
// Client factory + env-redirect logic
// ---------------------------------------------------------------------------

/// Load the ambient shared AWS config.
///
/// Honors `AWS_PROFILE`, `AWS_REGION`, and the standard credential chain via
/// `aws_config::defaults` — the only credential source, with or without
/// `AWS_ENDPOINT_URL` set. The endpoint itself is applied per-client (see
/// [`kinesis_client`] / [`dynamodb_client`] / [`cloudwatch_client`]).
async fn shared_config() -> aws_config::SdkConfig {
    let mut loader = aws_config::defaults(aws_config::BehaviorVersion::latest());
    if endpoint_url().is_some() {
        // Default region for a bare redirected target (only if the ambient env
        // did not already set one).
        if std::env::var("AWS_REGION").is_err() && std::env::var("AWS_DEFAULT_REGION").is_err() {
            loader = loader.region(aws_config::Region::new("us-east-1"));
        }
    }
    loader.load().await
}

/// The standard `AWS_ENDPOINT_URL` override, if set (and non-empty).
pub fn endpoint_url() -> Option<String> {
    std::env::var("AWS_ENDPOINT_URL")
        .ok()
        .filter(|s| !s.is_empty())
}

/// Build a Kinesis client from the ambient config, applying `AWS_ENDPOINT_URL`
/// if present.
pub async fn kinesis_client() -> aws_sdk_kinesis::Client {
    let shared = shared_config().await;
    match endpoint_url() {
        Some(ep) => {
            let conf = aws_sdk_kinesis::config::Builder::from(&shared)
                .endpoint_url(ep)
                .build();
            aws_sdk_kinesis::Client::from_conf(conf)
        }
        None => aws_sdk_kinesis::Client::new(&shared),
    }
}

/// Build a DynamoDB client from the ambient config, applying `AWS_ENDPOINT_URL`
/// if present.
pub async fn dynamodb_client() -> aws_sdk_dynamodb::Client {
    let shared = shared_config().await;
    match endpoint_url() {
        Some(ep) => {
            let conf = aws_sdk_dynamodb::config::Builder::from(&shared)
                .endpoint_url(ep)
                .build();
            aws_sdk_dynamodb::Client::from_conf(conf)
        }
        None => aws_sdk_dynamodb::Client::new(&shared),
    }
}

/// Build a CloudWatch client from the ambient config, applying `AWS_ENDPOINT_URL`
/// if present.
pub async fn cloudwatch_client() -> aws_sdk_cloudwatch::Client {
    let shared = shared_config().await;
    match endpoint_url() {
        Some(ep) => {
            let conf = aws_sdk_cloudwatch::config::Builder::from(&shared)
                .endpoint_url(ep)
                .build();
            aws_sdk_cloudwatch::Client::from_conf(conf)
        }
        None => aws_sdk_cloudwatch::Client::new(&shared),
    }
}

// ---------------------------------------------------------------------------
// Unique resource naming
// ---------------------------------------------------------------------------

/// A globally-unique table name: `kclrs-it-<label>-<uuid>`.
///
/// The `label` (usually the test name) makes leaked resources easy to trace;
/// the uuid suffix guarantees uniqueness across concurrent test runs.
pub fn unique_table_name(label: &str) -> String {
    let sanitized: String = label
        .chars()
        .map(|c| if c.is_ascii_alphanumeric() { c } else { '-' })
        .collect();
    format!(
        "{RESOURCE_PREFIX}{sanitized}-{}",
        uuid::Uuid::new_v4().simple()
    )
}

// ---------------------------------------------------------------------------
// Refresher construction (ports `LeaseIntegrationTest.getLeaseRefresher`)
// ---------------------------------------------------------------------------

/// Build a [`DynamoDBLeaseRefresher`] for `table_name` with the given billing
/// mode, mirroring the Java `LeaseIntegrationTest.getLeaseRefresher` (and its
/// PayPerRequest override): single-stream `DynamoDBLeaseSerializer`, consistent
/// reads, a no-op table-creator callback, the default request timeout, deletion
/// protection + PITR disabled, and no tags.
pub fn build_refresher(
    client: aws_sdk_dynamodb::Client,
    table_name: impl Into<String>,
    billing_mode: BillingMode,
) -> Arc<DynamoDBLeaseRefresher> {
    let table_config = RefresherTableConfig {
        billing_mode,
        ..RefresherTableConfig::default()
    };
    Arc::new(DynamoDBLeaseRefresher::new(
        table_name.into(),
        client,
        Arc::new(DynamoDBLeaseSerializer::new()),
        /* consistent_reads = */ true,
        Arc::new(NoopTableCreatorCallback),
        DEFAULT_REQUEST_TIMEOUT,
        table_config,
        /* deletion_protection_enabled = */ false,
        /* pitr_enabled = */ false,
        /* tags = */ Vec::new(),
    ))
}

/// Build a PayPerRequest refresher (the common case for these tests).
pub fn build_pay_per_request_refresher(
    client: aws_sdk_dynamodb::Client,
    table_name: impl Into<String>,
) -> Arc<DynamoDBLeaseRefresher> {
    build_refresher(client, table_name, BillingMode::PayPerRequest)
}

// ---------------------------------------------------------------------------
// Table setup / teardown (RAII-ish guard; Drop can't be async → explicit)
// ---------------------------------------------------------------------------

/// Guards a lease table's lifecycle for one test.
///
/// Ports the Java `LeaseIntegrationTest` `@Before` flow: create the table if it
/// does not exist, wait until it is active, then clear any leftover leases so
/// the test starts from an empty table. Because `Drop` cannot be async, callers
/// must `teardown().await` at the end (typically on both the success and error
/// paths). If a test panics before teardown, the uniquely-named table is simply
/// left behind (prefixed `kclrs-it-` for easy sweeping) — a best-effort abort
/// note is logged.
pub struct LeaseTableGuard {
    pub refresher: Arc<DynamoDBLeaseRefresher>,
    pub table_name: String,
    client: DynamoDbClient,
    torn_down: bool,
}

impl LeaseTableGuard {
    /// Create + wait-active + clear-leases for a freshly-named table.
    pub async fn setup(
        client: DynamoDbClient,
        table_name: impl Into<String>,
        billing_mode: BillingMode,
    ) -> Self {
        let table_name = table_name.into();
        let refresher = build_refresher(client.clone(), table_name.clone(), billing_mode);
        Self::setup_with_refresher(refresher, client, table_name).await
    }

    /// Like [`setup`](Self::setup) but with a caller-provided refresher (so the
    /// test can share the exact refresher instance with a coordinator/taker).
    /// `client` is used only for teardown (`delete_table`).
    pub async fn setup_with_refresher(
        refresher: Arc<DynamoDBLeaseRefresher>,
        client: DynamoDbClient,
        table_name: impl Into<String>,
    ) -> Self {
        let table_name = table_name.into();
        if !refresher
            .lease_table_exists()
            .await
            .expect("lease_table_exists failed")
        {
            refresher
                .create_lease_table_if_not_exists_with_capacity(10, 10)
                .await
                .expect("create_lease_table_if_not_exists failed");
            refresher
                .wait_until_lease_table_exists(1, 60)
                .await
                .expect("wait_until_lease_table_exists failed");
        }
        // Clear any leftover leases so the test starts empty.
        for lease in refresher.list_leases().await.expect("list_leases failed") {
            refresher
                .delete_lease(&lease)
                .await
                .expect("delete_lease failed");
        }
        Self {
            refresher,
            table_name,
            client,
            torn_down: false,
        }
    }

    /// Explicitly delete the table. Best-effort — errors are logged, not
    /// propagated, so teardown never masks a test assertion failure.
    pub async fn teardown(mut self) {
        self.torn_down = true;
        delete_table_best_effort(&self.client, &self.table_name).await;
    }
}

impl Drop for LeaseTableGuard {
    fn drop(&mut self) {
        if !self.torn_down {
            eprintln!(
                "WARNING: LeaseTableGuard for table `{}` dropped without teardown().await — \
                 the table may be leaked (sweep tables prefixed `{RESOURCE_PREFIX}`).",
                self.table_name
            );
        }
    }
}

/// Delete a DynamoDB table, ignoring `ResourceNotFound` and other errors
/// (best-effort teardown).
pub async fn delete_table_best_effort(client: &aws_sdk_dynamodb::Client, table_name: &str) {
    match client.delete_table().table_name(table_name).send().await {
        Ok(_) => {}
        Err(e) => {
            eprintln!("WARNING: best-effort delete_table({table_name}) failed: {e}");
        }
    }
}

// ---------------------------------------------------------------------------
// Kinesis stream setup / teardown
// ---------------------------------------------------------------------------

/// Create a Kinesis stream and wait until it is ACTIVE **and data-plane
/// visible**.
///
/// `DescribeStreamSummary` reporting ACTIVE does not guarantee the data plane
/// knows the stream yet — a `PutRecords`/`GetShardIterator` seconds after
/// creation can still get `ResourceNotFoundException` (observed repeatedly on
/// real AWS, especially with several streams created concurrently). After the
/// control-plane wait, probe the data plane with a non-mutating
/// `GetShardIterator` until it succeeds.
pub async fn create_stream_and_wait(
    client: &aws_sdk_kinesis::Client,
    stream_name: &str,
    shard_count: i32,
) {
    client
        .create_stream()
        .stream_name(stream_name)
        .shard_count(shard_count)
        .send()
        .await
        .expect("create_stream failed");
    // Poll for ACTIVE.
    let mut active = false;
    for _ in 0..60 {
        if let Ok(resp) = client
            .describe_stream_summary()
            .stream_name(stream_name)
            .send()
            .await
        {
            if let Some(desc) = resp.stream_description_summary() {
                if matches!(
                    desc.stream_status(),
                    aws_sdk_kinesis::types::StreamStatus::Active
                ) {
                    active = true;
                    break;
                }
            }
        }
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
    assert!(active, "stream {stream_name} did not become ACTIVE in time");

    // Data-plane readiness probe: ListShards + GetShardIterator, retried
    // under a deadline. Non-mutating, so streams whose tests assert on record
    // counts/contents are unaffected.
    let deadline = std::time::Instant::now() + Duration::from_secs(90);
    let mut last_err = String::new();
    while std::time::Instant::now() < deadline {
        let probe = async {
            let shards = client
                .list_shards()
                .stream_name(stream_name)
                .send()
                .await
                .map_err(|e| format!("list_shards: {e}"))?;
            let shard_id = shards
                .shards()
                .first()
                .map(|s| s.shard_id().to_string())
                .ok_or_else(|| "list_shards returned no shards".to_string())?;
            client
                .get_shard_iterator()
                .stream_name(stream_name)
                .shard_id(shard_id)
                .shard_iterator_type(aws_sdk_kinesis::types::ShardIteratorType::TrimHorizon)
                .send()
                .await
                .map_err(|e| format!("get_shard_iterator: {e}"))?;
            Ok::<(), String>(())
        }
        .await;
        match probe {
            Ok(()) => return,
            Err(e) => {
                tracing::info!(
                    "stream {stream_name} is ACTIVE but not data-plane visible yet ({e}); retrying"
                );
                last_err = e;
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
        }
    }
    panic!("stream {stream_name} never became data-plane visible: {last_err}");
}

/// Delete a Kinesis stream, best-effort.
///
/// `enforce_consumer_deletion(true)` mirrors the Java harness
/// (`StreamExistenceManager.deleteResourceCall`): without it, a stream with a
/// registered EFO consumer fails deletion with `ResourceInUseException` and
/// leaks.
pub async fn delete_stream_best_effort(client: &aws_sdk_kinesis::Client, stream_name: &str) {
    if let Err(e) = client
        .delete_stream()
        .stream_name(stream_name)
        .enforce_consumer_deletion(true)
        .send()
        .await
    {
        eprintln!("WARNING: best-effort delete_stream({stream_name}) failed: {e}");
    }
}

// ---------------------------------------------------------------------------
// Virtual nanosecond clock (ports the Java `Callable<Long>` time-provider seam)
// ---------------------------------------------------------------------------

/// A shared, advanceable nanosecond clock, used to drive the
/// `DynamoDBLeaseTaker` time-provider seam deterministically (Java's
/// `takeLeases(Callable<Long>)` + `TestHarnessBuilder.passTime`).
///
/// Starts at a fixed base so lease-age math is stable, and `pass_time_millis`
/// advances it forward (as `TestHarnessBuilder.passTime` does).
#[derive(Clone)]
pub struct VirtualClock {
    now_nanos: Arc<AtomicU64>,
}

impl VirtualClock {
    /// Start the clock at a large fixed base (so `now - lease_duration` never
    /// underflows) and return it.
    pub fn new() -> Self {
        // 1e15 ns ≈ 11.6 days; comfortably larger than any lease duration used.
        Self {
            now_nanos: Arc::new(AtomicU64::new(1_000_000_000_000_000)),
        }
    }

    /// Current value in nanos.
    pub fn now_nanos(&self) -> i64 {
        self.now_nanos.load(Ordering::SeqCst) as i64
    }

    /// Advance the clock by `millis` (Java `passTime`).
    pub fn pass_time_millis(&self, millis: i64) {
        self.now_nanos
            .fetch_add((millis as u64) * 1_000_000, Ordering::SeqCst);
    }

    /// A `NanoTimeProvider`-compatible closure returning the current nanos.
    pub fn provider(&self) -> Arc<dyn Fn() -> i64 + Send + Sync> {
        let clock = self.now_nanos.clone();
        Arc::new(move || clock.load(Ordering::SeqCst) as i64)
    }
}

impl Default for VirtualClock {
    fn default() -> Self {
        Self::new()
    }
}

// ---------------------------------------------------------------------------
// Lease builders (port `TestHarnessBuilder.createLease` / `LeaseHelper`)
// ---------------------------------------------------------------------------

/// Build a lease exactly as the Java `TestHarnessBuilder.createLease(shardId,
/// owner)` does: checkpoint = "checkpoint", ownerSwitchesSinceCheckpoint = 0,
/// leaseCounter = 0, the given owner, parentShardIds = {"parentShardId"},
/// empty childShardIds, leaseKey = shardId.
pub fn harness_lease(shard_id: &str, owner: Option<&str>) -> Lease {
    let mut lease = Lease::default();
    lease.set_checkpoint(ExtendedSequenceNumber::from_sequence_number("checkpoint"));
    lease.set_owner_switches_since_checkpoint(0);
    lease.set_lease_counter(0);
    lease.set_lease_owner(owner.map(str::to_string));
    lease.set_parent_shard_ids(["parentShardId".to_string()]);
    lease.set_child_shard_ids(std::iter::empty::<String>());
    lease.set_lease_key(shard_id);
    lease
}
