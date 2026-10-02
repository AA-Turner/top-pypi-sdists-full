//! Port of `software.amazon.kinesis.metrics.CloudWatchPublisherRunnable`.

use std::sync::{Arc, Mutex};

use async_trait::async_trait;
use rand::RngExt;

use crate::metrics::metric_accumulating_queue::MetricAccumulatingQueue;
use crate::metrics::{CloudWatchMetricKey, CloudWatchMetricsPublisher, MetricDatumWithKey};

/// Abstraction over the CloudWatch publish call so the runnable's timing/batching
/// state machine can be unit-tested against a mock (Java mocks
/// `CloudWatchMetricsPublisher` with Mockito).
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait MetricsPublisher: Send + Sync {
    /// Publishes the given data (Java `publishMetrics`).
    async fn publish_metrics(&self, data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>);
}

#[async_trait]
impl MetricsPublisher for CloudWatchMetricsPublisher {
    async fn publish_metrics(&self, data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>) {
        CloudWatchMetricsPublisher::publish_metrics(self, &data).await;
    }
}

/// Injectable monotonic-millis clock. Java exposes an overridable `getTime()`
/// (wrapping `System.currentTimeMillis()`) that tests override; this is the Rust
/// analog. `LONG_MAX` sentinel logic is handled in the state machine.
pub type Clock = Arc<dyn Fn() -> i64 + Send + Sync>;

/// The default clock: wall-clock milliseconds since the Unix epoch.
pub fn system_clock() -> Clock {
    Arc::new(|| {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_millis() as i64)
            .unwrap_or(0)
    })
}

/// The timing/batching state machine that decides *when* to flush accumulated
/// metrics to CloudWatch, plus the shutdown handshake and optional jitter.
///
/// **Concurrency model (ported to tokio):** Java runs this as a dedicated
/// `Thread` looping `runOnce()` and coordinating with the queue via
/// `synchronized`/`wait`/`notify`. The Rust port folds the queue + timing flags
/// into [`PublisherState`] behind one `tokio::sync::Mutex`, uses a
/// [`tokio::sync::Notify`] in place of `notify()`, and replaces `queue.wait(ms)`
/// with a `tokio::time::timeout` on `Notify::notified()`. A spawned task runs
/// [`run`](Self::run) until shutdown; the network publish happens **outside** the
/// mutex (matching Java releasing the monitor before the blocking call).
pub struct CloudWatchPublisherRunnable {
    publisher: Arc<dyn MetricsPublisher>,
    buffer_time_millis: i64,
    /// Number of metrics that triggers an immediate flush (`flushSize`).
    flush_size: usize,
    max_jitter: i32,
    clock: Clock,
    state: Arc<Mutex<PublisherState>>,
    notify: Arc<tokio::sync::Notify>,
}

/// The state guarded by the single mutex (queue + flags), mirroring the fields
/// Java protects under `synchronized(queue)`.
struct PublisherState {
    queue: MetricAccumulatingQueue<CloudWatchMetricKey>,
    shutting_down: bool,
    shutdown: bool,
    /// `i64::MAX` sentinel means "never flushed yet".
    last_flush_time: i64,
    next_jitter_value_to_use: i32,
}

impl CloudWatchPublisherRunnable {
    /// Constructor without jitter (Java 4-arg ctor: `maxJitter = 0`).
    pub fn new(
        publisher: Arc<dyn MetricsPublisher>,
        buffer_time_millis: i64,
        max_queue_size: usize,
        batch_size: usize,
    ) -> Self {
        Self::with_jitter(publisher, buffer_time_millis, max_queue_size, batch_size, 0)
    }

    /// Constructor with an explicit `max_jitter` (Java 5-arg ctor).
    pub fn with_jitter(
        publisher: Arc<dyn MetricsPublisher>,
        buffer_time_millis: i64,
        max_queue_size: usize,
        batch_size: usize,
        max_jitter: i32,
    ) -> Self {
        Self::with_jitter_and_clock(
            publisher,
            buffer_time_millis,
            max_queue_size,
            batch_size,
            max_jitter,
            system_clock(),
        )
    }

    /// Constructor with an injectable clock (used by timing tests to replace
    /// `getTime()`).
    pub fn with_jitter_and_clock(
        publisher: Arc<dyn MetricsPublisher>,
        buffer_time_millis: i64,
        max_queue_size: usize,
        batch_size: usize,
        max_jitter: i32,
        clock: Clock,
    ) -> Self {
        Self {
            publisher,
            buffer_time_millis,
            flush_size: batch_size,
            max_jitter,
            clock,
            state: Arc::new(Mutex::new(PublisherState {
                queue: MetricAccumulatingQueue::new(max_queue_size),
                shutting_down: false,
                shutdown: false,
                last_flush_time: i64::MAX,
                next_jitter_value_to_use: 0,
            })),
            notify: Arc::new(tokio::sync::Notify::new()),
        }
    }

    /// A cheap handle the [`CloudWatchMetricsScope`](crate::metrics::CloudWatchMetricsScope)
    /// can use to enqueue synchronously (its `end()` is sync) without holding a
    /// reference to the whole runnable.
    pub fn handle(&self) -> PublisherHandle {
        PublisherHandle {
            state: self.state.clone(),
            notify: self.notify.clone(),
            clock: self.clock.clone(),
        }
    }

    fn now(&self) -> i64 {
        (self.clock)()
    }

    /// Loops `run_once()` until shutdown, swallowing per-iteration panics so the
    /// publisher task never dies unexpectedly (Java catches `Throwable`).
    pub async fn run(&self) {
        loop {
            if self.state.lock().unwrap().shutdown {
                break;
            }
            // Ports Java CloudWatchPublisherRunnable.run's catch (Throwable t).
            if let Err(panic) = crate::utils::panic_util::catch_tick(self.run_once()).await {
                tracing::error!("Encountered throwable in CWPublisherRunable: {}", panic);
            }
        }
        tracing::info!("CWPublication thread finished.");
    }

    /// One step of the flush state machine. Exposed for testing (Java `runOnce`
    /// is package-visible for tests).
    pub async fn run_once(&self) {
        let mut data_to_publish: Option<Vec<MetricDatumWithKey<CloudWatchMetricKey>>> = None;
        let notified = self.notify.notified();
        let mut wait_time = 0u64;
        let mut should_wait = false;

        {
            // Short synchronous critical section — never held across `.await`.
            let mut st = self.state.lock().unwrap();
            let time_since_flush = (self.now() - st.last_flush_time).max(0);
            if time_since_flush >= self.buffer_time_millis
                || st.queue.size() >= self.flush_size
                || st.shutting_down
            {
                let drained = st.queue.drain(self.flush_size);
                if st.shutting_down {
                    // We finish shutting down only when the queue is empty.
                    st.shutdown = st.queue.is_empty();
                }
                data_to_publish = Some(drained);
            } else {
                should_wait = true;
                wait_time = (self.buffer_time_millis - time_since_flush).max(0) as u64;
            }
        }

        if should_wait {
            // Wait for enqueues for up to (bufferTimeMillis - timeSinceFlush).
            let _ =
                tokio::time::timeout(std::time::Duration::from_millis(wait_time), notified).await;
            return;
        }

        if let Some(data) = data_to_publish {
            // Publish OUTSIDE the lock (Java releases the monitor first).
            self.publisher.publish_metrics(data).await;

            let mut st = self.state.lock().unwrap();
            st.last_flush_time = self.now() + st.next_jitter_value_to_use as i64;
            if self.max_jitter != 0 {
                // next value in (-maxJitter, +maxJitter].
                let r: i32 = rand::rng().random_range(0..(2 * self.max_jitter));
                st.next_jitter_value_to_use = self.max_jitter - r;
            }
        }
    }

    /// Requests shutdown and wakes the loop (Java `shutdown` sets `shuttingDown`
    /// and `notify`s).
    pub fn shutdown(&self) {
        tracing::info!("Shutting down CWPublication thread.");
        self.state.lock().unwrap().shutting_down = true;
        self.notify.notify_one();
    }

    /// Whether the runnable has fully drained and stopped (Java `isShutdown`).
    pub fn is_shutdown(&self) -> bool {
        self.state.lock().unwrap().shutdown
    }

    /// Enqueues metric data for publication. Port of `enqueue`.
    pub fn enqueue(&self, data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>) {
        enqueue_locked(&self.state, self.now(), data);
        self.notify.notify_one();
    }
}

/// Shared enqueue logic used by both the runnable and its [`PublisherHandle`].
///
/// Drops the data if already shutting down; offers each datum (logging a drop on
/// a full queue); starts the buffering window from the first-ever enqueue (when
/// `last_flush_time` is still the `i64::MAX` sentinel). Mirrors Java `enqueue`.
fn enqueue_locked(
    state: &Mutex<PublisherState>,
    now: i64,
    data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>,
) {
    let mut st = state.lock().unwrap();
    if st.shutting_down {
        tracing::warn!("Dropping metrics because CloudWatchPublisherRunnable is shutting down.");
        return;
    }
    for datum_with_key in data {
        if !st.queue.offer(datum_with_key.key, datum_with_key.datum) {
            tracing::warn!("Metrics queue full - dropping metric");
        }
    }
    if st.last_flush_time == i64::MAX {
        st.last_flush_time = now;
    }
}

/// A synchronous enqueue handle for [`CloudWatchMetricsScope`](crate::metrics::CloudWatchMetricsScope),
/// whose `end()` runs in a synchronous context.
#[derive(Clone)]
pub struct PublisherHandle {
    state: Arc<Mutex<PublisherState>>,
    notify: Arc<tokio::sync::Notify>,
    clock: Clock,
}

impl std::fmt::Debug for PublisherHandle {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PublisherHandle").finish_non_exhaustive()
    }
}

impl PublisherHandle {
    /// Synchronously enqueues metric data (Java `enqueue`), waking the publisher
    /// loop.
    pub fn enqueue(&self, data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>) {
        let now = (self.clock)();
        enqueue_locked(&self.state, now, data);
        self.notify.notify_one();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::test_helper::construct_datum;
    use aws_sdk_cloudwatch::types::StandardUnit;
    use std::sync::atomic::{AtomicI64, Ordering};

    const MAX_QUEUE_SIZE: usize = 5;
    const MAX_BUFFER_TIME_MILLIS: i64 = 1;
    // FLUSH_SIZE should be > 1 and < MAX_QUEUE_SIZE / 2.
    const FLUSH_SIZE: usize = 2;

    /// Test harness mirroring CloudWatchPublisherRunnableTest.TestHarness.
    ///
    /// Records the `publish_metrics` calls (Mockito verify equivalent) and drives
    /// an injectable clock (`getTime()` override equivalent).
    struct TestHarness {
        data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>,
        counter: i64,
        runnable: CloudWatchPublisherRunnable,
        clock: Arc<AtomicI64>,
        published: Arc<std::sync::Mutex<Vec<Vec<MetricDatumWithKey<CloudWatchMetricKey>>>>>,
    }

    struct RecordingPublisher {
        published: Arc<std::sync::Mutex<Vec<Vec<MetricDatumWithKey<CloudWatchMetricKey>>>>>,
    }

    #[async_trait]
    impl MetricsPublisher for RecordingPublisher {
        async fn publish_metrics(&self, data: Vec<MetricDatumWithKey<CloudWatchMetricKey>>) {
            self.published.lock().unwrap().push(data);
        }
    }

    impl TestHarness {
        fn new() -> Self {
            let clock = Arc::new(AtomicI64::new(0));
            let clock_for_closure = clock.clone();
            let published = Arc::new(std::sync::Mutex::new(Vec::new()));
            let publisher = Arc::new(RecordingPublisher {
                published: published.clone(),
            });
            let runnable = CloudWatchPublisherRunnable::with_jitter_and_clock(
                publisher,
                MAX_BUFFER_TIME_MILLIS,
                MAX_QUEUE_SIZE,
                FLUSH_SIZE,
                0,
                Arc::new(move || clock_for_closure.load(Ordering::SeqCst)),
            );
            Self {
                data: Vec::new(),
                counter: 0,
                runnable,
                clock,
                published,
            }
        }

        fn construct_datum(&self, value: i64) -> MetricDatumWithKey<CloudWatchMetricKey> {
            let datum = construct_datum(
                &format!("datum-{}", value),
                StandardUnit::Count,
                value as f64,
                value as f64,
                value as f64,
                1.0,
            );
            MetricDatumWithKey::new(CloudWatchMetricKey::new(&datum), datum)
        }

        async fn enqueue_random(&mut self, count: usize) {
            let mut batch = Vec::new();
            for _ in 0..count {
                let value = self.counter;
                self.counter += 1;
                let d = self.construct_datum(value);
                self.data.push(d.clone());
                batch.push(d);
            }
            self.runnable.enqueue(batch);
        }

        async fn run_and_assert(&self, start_index: usize, count: usize) {
            let before = self.published.lock().unwrap().len();
            self.runnable.run_once().await;
            let calls = self.published.lock().unwrap();
            if count > 0 {
                assert_eq!(calls.len(), before + 1, "expected exactly one publish call");
                let last = calls.last().unwrap();
                let expected = &self.data[start_index..start_index + count];
                assert_eq!(last.as_slice(), expected);
            } else {
                assert_eq!(calls.len(), before, "expected no publish call");
            }
        }

        async fn run_and_assert_all_data(&self) {
            self.run_and_assert(0, self.data.len()).await;
        }

        fn pass_time(&self, time: i64) {
            self.clock.fetch_add(time, Ordering::SeqCst);
        }
    }

    #[tokio::test]
    async fn test_publish_on_flush_size() {
        let mut h = TestHarness::new();
        h.enqueue_random(FLUSH_SIZE).await;
        h.run_and_assert_all_data().await;
    }

    #[tokio::test]
    async fn test_wait_for_batch_timeout() {
        let mut h = TestHarness::new();
        h.enqueue_random(1).await;
        h.run_and_assert(0, 0).await;
        h.pass_time(MAX_BUFFER_TIME_MILLIS);
        h.run_and_assert_all_data().await;

        h.enqueue_random(1).await;
        h.run_and_assert(0, 0).await;
        h.pass_time(MAX_BUFFER_TIME_MILLIS);
        h.run_and_assert(1, 1).await;
    }

    #[tokio::test]
    async fn test_drain_queue() {
        let mut h = TestHarness::new();
        let num_batches = 2;
        h.enqueue_random(FLUSH_SIZE * num_batches).await;
        h.enqueue_random(1).await;
        for i in 0..num_batches {
            h.run_and_assert(i * FLUSH_SIZE, FLUSH_SIZE).await;
        }
        h.run_and_assert(0, 0).await;
        h.pass_time(MAX_BUFFER_TIME_MILLIS);
        h.run_and_assert(num_batches * FLUSH_SIZE, 1).await;
    }

    #[tokio::test]
    async fn test_shutdown() {
        let mut h = TestHarness::new();
        h.enqueue_random(FLUSH_SIZE + 1).await;
        h.runnable.shutdown();

        h.run_and_assert(0, FLUSH_SIZE).await;
        assert!(!h.runnable.is_shutdown());

        h.run_and_assert(FLUSH_SIZE, 1).await;
        assert!(h.runnable.is_shutdown());
    }

    #[tokio::test]
    async fn test_queue_full_drop_data() {
        let mut h = TestHarness::new();
        let num_records = MAX_QUEUE_SIZE + 1;
        h.enqueue_random(num_records).await;
        h.runnable.shutdown();
        let mut i = 0;
        while i < MAX_QUEUE_SIZE {
            let count = (MAX_QUEUE_SIZE - i).min(FLUSH_SIZE);
            h.run_and_assert(i, count).await;
            i += FLUSH_SIZE;
        }
        assert!(h.runnable.is_shutdown());
    }
}
