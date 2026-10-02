//! Integration tests for the retrieval **polling** layer — ports of the Java
//! `retrieval/polling/*IntegrationTest.java` files.
//!
//! The upstream Java integration tests mock `KinesisAsyncClient` (they exercise
//! the publisher/strategy plumbing against a Mockito data fetcher rather than a
//! live stream). This Rust port takes the integration a step further: it stands
//! up a **real Kinesis stream**, `PutRecords` a known ordered batch, and then
//! drives the actual [`KinesisDataFetcher`] / [`SynchronousGetRecordsRetrievalStrategy`]
//! / [`AsynchronousGetRecordsRetrievalStrategy`] / [`PrefetchRecordsPublisher`]
//! against it — asserting the same observable behavior (records retrieved, in
//! order, delivered over the RecordsPublisher subscription cycle).
//!
//! Every test is `#[ignore]` (see the module doc in `common/mod.rs`). Run with:
//! `cargo test -p kcl -- --ignored` (optionally `AWS_ENDPOINT_URL=...` to
//! redirect to LocalStack).
//!
//! Concurrency note: the tests use a multi-thread runtime because the publisher
//! spawns a background task that must make progress while the test thread awaits
//! deliveries.
//!
//! Teardown note: like the sibling `leases_*_it.rs` suites, teardown
//! (`delete_stream_best_effort`) runs on the success path; a panic before it
//! leaves the uniquely-named (`kclrs-it-`-prefixed) stream for later sweeping.

mod common;

use std::sync::Arc;
use std::time::Duration;

use aws_sdk_kinesis::primitives::Blob;
use aws_sdk_kinesis::types::PutRecordsRequestEntry;

use kcl::common::{InitialPositionInStream, InitialPositionInStreamExtended, StreamIdentifier};
use kcl::metrics::NullMetricsFactory;
use kcl::retrieval::kpl::ExtendedSequenceNumber;
use kcl::retrieval::polling::{
    AsynchronousGetRecordsRetrievalStrategy, DataFetcher, KinesisDataFetcher,
    KinesisSleepTimeController, PrefetchRecordsPublisher, SynchronousGetRecordsRetrievalStrategy,
};
use kcl::retrieval::records_delivery_ack::SimpleRecordsDeliveryAck;
use kcl::retrieval::throttling_reporter::ThrottlingReporter;
use kcl::retrieval::{
    DataFetcherProviderConfig, GetRecordsRetrievalStrategy, KinesisDataFetcherProviderConfig,
    RecordsPublisher,
};

use common::{
    create_stream_and_wait, delete_stream_best_effort, kinesis_client, unique_table_name,
};

const OPERATION: &str = "ProcessTask";
const MAX_RECORDS_PER_CALL: i32 = 10_000;
const KINESIS_REQUEST_TIMEOUT: Duration = Duration::from_secs(30);

/// A stream name unique to this run (reuses the harness's `kclrs-it-` prefix +
/// uuid naming so leaked streams are easy to sweep).
fn unique_stream_name(label: &str) -> String {
    unique_table_name(label)
}

/// Put `count` records with sequential payloads into the single shard of a
/// freshly-created stream, returning the payloads in order.
async fn put_ordered_records(
    client: &aws_sdk_kinesis::Client,
    stream_name: &str,
    count: usize,
) -> Vec<Vec<u8>> {
    let mut entries = Vec::with_capacity(count);
    let mut payloads = Vec::with_capacity(count);
    for i in 0..count {
        let data = format!("record-{i:04}").into_bytes();
        payloads.push(data.clone());
        entries.push(
            PutRecordsRequestEntry::builder()
                // Single-shard stream: a constant partition key keeps ordering
                // deterministic (all records land in the same shard).
                .partition_key("pk")
                .data(Blob::new(data))
                .build()
                .expect("build PutRecordsRequestEntry"),
        );
    }
    // Freshly created streams can transiently RNF on the data plane even
    // after DescribeStreamSummary reports ACTIVE; retry whole-call failures
    // under a deadline (same treatment as the application canaries).
    let deadline = std::time::Instant::now() + Duration::from_secs(90);
    let resp = loop {
        match client
            .put_records()
            .stream_name(stream_name)
            .set_records(Some(entries.clone()))
            .send()
            .await
        {
            Ok(resp) => break resp,
            Err(e) if std::time::Instant::now() < deadline => {
                tracing::info!(
                    "put_records({stream_name}) failed transiently; retrying in 2s: {e}"
                );
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
            Err(e) => panic!("put_records failed after retrying transient errors for 90s: {e}"),
        }
    };
    assert_eq!(
        resp.failed_record_count().unwrap_or(0),
        0,
        "some records failed to put"
    );
    payloads
}

/// Build a [`KinesisDataFetcher`] targeting the single shard of `stream_name`.
async fn build_data_fetcher(
    client: &aws_sdk_kinesis::Client,
    stream_name: &str,
) -> (Arc<KinesisDataFetcher>, String) {
    // Resolve the (single) shard id of the stream.
    let shards = client
        .list_shards()
        .stream_name(stream_name)
        .send()
        .await
        .expect("list_shards failed");
    let shard_id = shards
        .shards()
        .first()
        .expect("stream has at least one shard")
        .shard_id()
        .to_string();

    let cfg: Box<dyn DataFetcherProviderConfig> = Box::new(KinesisDataFetcherProviderConfig::new(
        StreamIdentifier::single_stream_instance(stream_name),
        shard_id.clone(),
        Arc::new(NullMetricsFactory::new()),
        MAX_RECORDS_PER_CALL,
        KINESIS_REQUEST_TIMEOUT,
    ));
    let fetcher = Arc::new(KinesisDataFetcher::new(client.clone(), cfg.as_ref()));
    (fetcher, shard_id)
}

fn trim_horizon() -> InitialPositionInStreamExtended {
    InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::TrimHorizon)
}

// ===========================================================================
// FILE 1: PrefetchRecordsPublisherIntegrationTest
// ===========================================================================
//
// Java mocks the client + fetcher and asserts the rolling/full cache and
// expired-iterator recovery behaviors. Here we drive the *real* publisher over a
// real stream through the RecordsPublisher subscription cycle
// (subscribe -> request(1) -> recv -> notify(ack) -> request(1)) and assert
// records are retrieved in the order they were put.

/// Ports the intent of `testRollingCache` / `testFullCache`: the prefetch
/// publisher, started at TRIM_HORIZON on a stream that already contains records,
/// delivers those records to a single subscriber in order over successive
/// request/ack cycles.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn prefetch_publisher_delivers_records_in_order() {
    common::init_test_tracing();
    let client = kinesis_client().await;
    let stream_name = unique_stream_name("prefetch-in-order");
    create_stream_and_wait(&client, &stream_name, 1).await;

    const RECORD_COUNT: usize = 10;
    let expected = put_ordered_records(&client, &stream_name, RECORD_COUNT).await;

    let (fetcher, shard_id) = build_data_fetcher(&client, &stream_name).await;
    let strategy: Arc<dyn GetRecordsRetrievalStrategy> = Arc::new(
        SynchronousGetRecordsRetrievalStrategy::new(Arc::clone(&fetcher) as Arc<dyn DataFetcher>),
    );

    let publisher = Arc::new(PrefetchRecordsPublisher::new(
        /* max_pending_process_records_input = */ 3,
        /* max_byte_size = */ 5 * 1024 * 1024,
        /* max_records_count = */ 30_000,
        MAX_RECORDS_PER_CALL,
        strategy,
        /* idle_millis_between_calls = */ 500,
        /* millis_behind_latest_threshold_for_reduced_tps = */ 0,
        Arc::new(NullMetricsFactory::new()),
        OPERATION,
        &shard_id,
        ThrottlingReporter::new(5, &shard_id),
        Arc::new(KinesisSleepTimeController),
    ));

    let mut sub = publisher.subscribe();
    publisher
        .start(ExtendedSequenceNumber::trim_horizon(), trim_horizon())
        .await
        .expect("publisher start should succeed");

    // Drain until we've collected all expected payloads (GetRecords may return
    // them across several empty/partial batches; we drive the subscription cycle
    // one batch at a time).
    let mut collected: Vec<Vec<u8>> = Vec::new();
    sub.request(1);
    let deadline = tokio::time::Instant::now() + Duration::from_secs(30);
    while collected.len() < RECORD_COUNT {
        let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
        assert!(!remaining.is_zero(), "timed out collecting records");
        let delivery = tokio::time::timeout(remaining, sub.recv())
            .await
            .expect("recv timed out")
            .expect("delivery channel closed")
            .expect("no retrieval error");
        let input = delivery.process_records_input();
        if let Some(records) = input.records() {
            for r in records {
                collected.push(r.data().map(|d| d.to_vec()).unwrap_or_default());
            }
        }
        // Ack the delivered batch and request the next.
        publisher
            .notify(Box::new(SimpleRecordsDeliveryAck::new(
                delivery.batch_unique_identifier(),
            )))
            .await;
        sub.request(1);
    }

    assert_eq!(
        collected.len(),
        RECORD_COUNT,
        "should have retrieved every put record"
    );
    assert_eq!(
        collected, expected,
        "records must be retrieved in put order"
    );

    publisher.shutdown().await;
    delete_stream_best_effort(&client, &stream_name).await;
}

// ===========================================================================
// FILE 2: AsynchronousGetRecordsRetrievalStrategyIntegrationTest
//         (+ the synchronous strategy over the same fetcher)
// ===========================================================================
//
// Java mocks the CompletionService/executor scheduling. Here we exercise the
// real GetRecords path: initialize the fetcher, then use the strategy to pull
// the records that were put, asserting they come back in order.

/// Ports the intent of the async retrieval-strategy test: a real `GetRecords`
/// via `AsynchronousGetRecordsRetrievalStrategy` over a `KinesisDataFetcher`
/// returns the put records.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn asynchronous_strategy_get_records() {
    common::init_test_tracing();
    let client = kinesis_client().await;
    let stream_name = unique_stream_name("async-getrecords");
    create_stream_and_wait(&client, &stream_name, 1).await;

    const RECORD_COUNT: usize = 10;
    let expected = put_ordered_records(&client, &stream_name, RECORD_COUNT).await;

    let (fetcher, shard_id) = build_data_fetcher(&client, &stream_name).await;
    // Initialize the iterator at TRIM_HORIZON before fetching (Java's
    // dataFetcher.initialize(...) / the publisher's start()).
    fetcher
        .initialize(
            ExtendedSequenceNumber::trim_horizon().sequence_number(),
            &trim_horizon(),
        )
        .await
        .expect("fetcher initialize should succeed");

    let strategy = AsynchronousGetRecordsRetrievalStrategy::new(
        Arc::clone(&fetcher) as Arc<dyn DataFetcher>,
        /* retry_get_records_in_seconds = */ 5,
        shard_id,
    );

    // GetRecords can return the batch across a few calls; loop until we have them
    // all (or time out).
    let mut collected: Vec<Vec<u8>> = Vec::new();
    let deadline = tokio::time::Instant::now() + Duration::from_secs(30);
    while collected.len() < RECORD_COUNT {
        assert!(
            tokio::time::Instant::now() < deadline,
            "timed out collecting records via async strategy"
        );
        let adapter = strategy
            .get_records_adapter(MAX_RECORDS_PER_CALL)
            .await
            .expect("get_records_adapter failed");
        let records = adapter.records();
        let was_empty = records.is_empty();
        for r in records {
            collected.push(r.data().map(|d| d.to_vec()).unwrap_or_default());
        }
        if was_empty {
            tokio::time::sleep(Duration::from_millis(200)).await;
        }
    }

    assert_eq!(
        collected, expected,
        "async strategy must return records in order"
    );
    strategy.shutdown();
    assert!(strategy.is_shutdown());
    delete_stream_best_effort(&client, &stream_name).await;
}

/// Companion: the synchronous strategy over the same real fetcher (mirrors the
/// `SynchronousGetRecordsRetrievalStrategy` the Java prefetch test wraps its
/// spied fetcher in). Confirms the two-phase get/accept advances the iterator so
/// successive calls page forward through the shard.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
#[ignore = "integration: runs against AWS; set AWS_ENDPOINT_URL to redirect to LocalStack"]
async fn synchronous_strategy_pages_forward() {
    common::init_test_tracing();
    let client = kinesis_client().await;
    let stream_name = unique_stream_name("sync-getrecords");
    create_stream_and_wait(&client, &stream_name, 1).await;

    const RECORD_COUNT: usize = 6;
    let expected = put_ordered_records(&client, &stream_name, RECORD_COUNT).await;

    let (fetcher, _shard_id) = build_data_fetcher(&client, &stream_name).await;
    fetcher
        .initialize(
            ExtendedSequenceNumber::trim_horizon().sequence_number(),
            &trim_horizon(),
        )
        .await
        .expect("fetcher initialize should succeed");

    let strategy =
        SynchronousGetRecordsRetrievalStrategy::new(Arc::clone(&fetcher) as Arc<dyn DataFetcher>);

    let mut collected: Vec<Vec<u8>> = Vec::new();
    let deadline = tokio::time::Instant::now() + Duration::from_secs(30);
    while collected.len() < RECORD_COUNT {
        assert!(
            tokio::time::Instant::now() < deadline,
            "timed out collecting records via sync strategy"
        );
        let adapter = strategy
            .get_records_adapter(MAX_RECORDS_PER_CALL)
            .await
            .expect("get_records_adapter failed");
        let records = adapter.records();
        if records.is_empty() {
            tokio::time::sleep(Duration::from_millis(200)).await;
            continue;
        }
        for r in records {
            collected.push(r.data().map(|d| d.to_vec()).unwrap_or_default());
        }
    }

    assert_eq!(
        collected, expected,
        "sync strategy must page forward in order"
    );
    delete_stream_best_effort(&client, &stream_name).await;
}
