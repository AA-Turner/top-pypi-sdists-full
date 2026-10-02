//! Self-consume the Redis function queue on the scaling-group (sg) pod.
//!
//! This runs *alongside* the gRPC server, which is untouched: the synchronous
//! / direct `CallFunction` path keeps serving inbound calls.
//!
//! Work is read from the revision's advertised Redis List or Stream transport.
//! Stream deliveries are acknowledged only after result writes complete and
//! reclaimed after a crashed owner stops heartbeating. Concurrency is capped
//! by a Redis-backed distributed semaphore (per function,
//! across every pod in the scaling group). The dispatch loop dispatches as fast
//! as it can acquire a slot and pop work; in-flight worker tasks are therefore
//! bounded by `max_concurrent`, not by traffic. A single per-pod renewer task
//! heartbeats every live lease in one round-trip via
//! [`renew_many`](chalk_queue::semaphore::renew_many) — never a task per call.
//!
//! ## Dispatch modes
//!
//! There are two ways a popped call reaches the Python handler, selected by
//! whether the pod was started with request coalescing enabled:
//!
//! - **Streaming (no coalescing):** [`run_one_call`] hands the call straight to
//!   the handler via `call_into_buffer`, streaming generator yields to the
//!   result stream chunk-by-chunk as they are produced.
//! - **Coalesced (batching on):** [`run_one_coalesced_call`] submits the call
//!   into the *shared* [`CoalescingQueue`] — the same queue inbound gRPC
//!   `CallFunction` requests use — so self-consumed work and inbound calls batch
//!   together under the single batch-size/duration the user configured. A
//!   coalesced call yields exactly one result blob (the batched bridge is not a
//!   streaming convention), written as one chunk + `end`. This mirrors the old
//!   catalog-consumer path, where coalescing also produced one response per
//!   caller. The semaphore still admits one slot per call, so it remains the
//!   producer of the concurrency the coalescer batches.

use std::collections::HashMap;
use std::panic::AssertUnwindSafe;
use std::str::FromStr;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use chalk_queue::semaphore::renew_many;
use chalk_queue::stream_writer;
use chalk_queue::types::{DeliveryAttempt, QueuedCall};
use chalk_queue::{
    BoundFunctionQueue, DequeuedCall, FunctionQueue, QueueProtocol, QueueReceipt, SemaphoreLease,
};
use dashmap::DashMap;
use futures_util::FutureExt;
use redis::aio::ConnectionManager;
use redis::Client;
use tokio::sync::mpsc;
use tracing::{error, info, warn};
use uuid::Uuid;

use chalk_metrics::metrics::tags::Mode;
use chalk_metrics::PublishingMetricsPipeline;

use crate::coalesce::{BufferedCall, CoalescingQueue};
use crate::python_bridge::{CallerInput, ChunkBuffer, PythonHandler};

const ENV_REDIS_URL: &str = "CHALK_FNQ_REDIS_URL";
const ENV_TENANT: &str = "CHALK_FNQ_TENANT";
const ENV_FUNCTION_NAME: &str = "CHALK_FNQ_FUNCTION_NAME";
const ENV_MAX_CONCURRENT: &str = "CHALK_FNQ_MAX_CONCURRENT";
const ENV_SEM_TTL_SECS: &str = "CHALK_FNQ_SEM_TTL_SECS";
const ENV_POLL_BACKOFF_INITIAL_MS: &str = "CHALK_FNQ_POLL_BACKOFF_INITIAL_MS";
const ENV_POLL_BACKOFF_MAX_SECS: &str = "CHALK_FNQ_POLL_BACKOFF_MAX_SECS";
const ENV_FLUSH_TIMEOUT_MS: &str = "CHALK_FNQ_FLUSH_TIMEOUT_MS";
const ENV_QUEUE_PROTOCOL: &str = "CHALK_FNQ_QUEUE_PROTOCOL";
const ENV_STREAM_READ_COUNT: &str = "CHALK_FNQ_STREAM_READ_COUNT";

/// Lease lifetime (default). Intentionally short relative to how long a call may run: the
/// per-pod renewer keeps a live call's lease alive (see module docs), so the
/// TTL bounds only how long a *crashed* holder's slot stays occupied — not the
/// job length. Must stay comfortably larger than `SEM_RENEW_INTERVAL`.
/// Configurable via `CHALK_FNQ_SEM_TTL_SECS`.
const DEFAULT_SEM_TTL_SECS: u64 = 30;
/// How often the per-pod renewer heartbeats all live leases. Several renews fit
/// inside one SEM_TTL so a single dropped tick never loses a slot.
const SEM_RENEW_INTERVAL: Duration = Duration::from_secs(10);
/// Initial backoff when the queue is empty or the semaphore is at capacity (default).
/// Exponential backoff starts here and doubles on each failure up to POLL_BACKOFF_MAX.
/// Configurable via `CHALK_FNQ_POLL_BACKOFF_INITIAL_MS`.
const DEFAULT_POLL_BACKOFF_INITIAL_MS: u64 = 100;
/// Cap on exponential backoff (default).
/// Configurable via `CHALK_FNQ_POLL_BACKOFF_MAX_SECS`.
const DEFAULT_POLL_BACKOFF_MAX_SECS: u64 = 2;
/// Fallback timeout for waiting on buffer notification (default). Ensures we make progress
/// even if the notification pipeline breaks, and handles the rare case where a
/// chunk append races with the wait setup.
/// Configurable via `CHALK_FNQ_FLUSH_TIMEOUT_MS`.
const DEFAULT_FLUSH_TIMEOUT_MS: u64 = 100;
/// A bounded prefetch window for Redis Streams. This is deliberately much
/// smaller than a logical handler batch: several reads can feed the shared
/// coalescer, while one read remains cheap to reserve, decode and recover.
const DEFAULT_STREAM_READ_COUNT: usize = 64;
/// Recovery does not belong on the normal dequeue path. A dead consumer is
/// still recovered promptly, while healthy traffic avoids an XAUTOCLAIM RPC
/// for every read window.
const STREAM_RECLAIM_INTERVAL: Duration = Duration::from_secs(10);

/// `peer` recorded in the handler context for queue-consumed calls; there is no
/// inbound network peer on this path.
const PEER: &str = "fnq-self-consumer";

/// Selects where a queued call publishes its result without allowing a shared
/// batch stream to lose the call identity needed by the collector.
#[derive(Debug, PartialEq, Eq)]
enum ResultDestination {
    PerCall {
        stream_key: String,
        result_ttl: Duration,
    },
    Batch {
        stream_key: String,
        call_id: String,
        row_index: u64,
    },
}

impl ResultDestination {
    fn for_call(queue: &FunctionQueue, work: &QueuedCall, call_uuid: Uuid) -> Self {
        let batch = work.batch_result.as_ref().map(|batch_result| {
            (
                queue.batch_stream_key_for(&batch_result.batch_id),
                work.call_id.clone(),
                batch_result.row_index,
            )
        });
        Self::from_routing(
            queue.stream_key_for(call_uuid),
            Duration::from_secs(work.result_ttl_seconds),
            batch,
        )
    }

    fn from_routing(
        per_call_stream_key: String,
        result_ttl: Duration,
        batch: Option<(String, String, u64)>,
    ) -> Self {
        match batch {
            Some((stream_key, call_id, row_index)) => Self::Batch {
                stream_key,
                call_id,
                row_index,
            },
            None => Self::PerCall {
                stream_key: per_call_stream_key,
                result_ttl,
            },
        }
    }

    async fn write_chunk(
        &self,
        conn: &mut ConnectionManager,
        seq: u64,
        data: &[u8],
    ) -> Result<(), redis::RedisError> {
        match self {
            Self::PerCall { stream_key, .. } => {
                stream_writer::write_chunk(conn, stream_key, seq, data).await
            }
            Self::Batch {
                stream_key,
                call_id,
                row_index,
            } => {
                stream_writer::BatchStreamWriter::new(stream_key, call_id, *row_index)
                    .write_chunk(conn, seq, data)
                    .await
            }
        }
    }

    async fn write_end(
        &self,
        conn: &mut ConnectionManager,
        seq: u64,
    ) -> Result<(), redis::RedisError> {
        match self {
            Self::PerCall {
                stream_key,
                result_ttl,
            } => stream_writer::write_end_with_ttl(conn, stream_key, seq, *result_ttl).await,
            Self::Batch {
                stream_key,
                call_id,
                row_index,
            } => {
                stream_writer::BatchStreamWriter::new(stream_key, call_id, *row_index)
                    .write_end(conn, seq)
                    .await
            }
        }
    }

    async fn write_error(
        &self,
        conn: &mut ConnectionManager,
        seq: u64,
        exc_type: &str,
        message: &str,
        traceback: Option<&str>,
    ) -> Result<(), redis::RedisError> {
        match self {
            Self::PerCall {
                stream_key,
                result_ttl,
            } => {
                stream_writer::write_error_with_ttl(
                    conn,
                    stream_key,
                    seq,
                    exc_type,
                    message,
                    traceback,
                    *result_ttl,
                )
                .await
            }
            Self::Batch {
                stream_key,
                call_id,
                row_index,
            } => {
                stream_writer::BatchStreamWriter::new(stream_key, call_id, *row_index)
                    .write_error(conn, seq, exc_type, message, traceback)
                    .await
            }
        }
    }
}

/// Configuration for the self-consumer, read from the environment.
///
/// [`from_env`](Self::from_env) returns `None` when `CHALK_FNQ_REDIS_URL` is
/// unset — the pod then runs gRPC-only (the synchronous path) and does not
/// self-consume. That is the contract that lets a single shim binary serve both
/// roles depending on how the pod was provisioned.
pub struct SelfConsumerConfig {
    pub redis_url: String,
    pub tenant: String,
    pub function_name: String,
    pub max_concurrent: u32,
    pub sem_ttl: Duration,
    pub poll_backoff_initial: Duration,
    pub poll_backoff_max: Duration,
    pub flush_timeout: Duration,
    pub queue_protocol: QueueProtocol,
    pub stream_read_count: usize,
}

impl SelfConsumerConfig {
    pub fn from_env() -> Option<Self> {
        // No Redis URL → not provisioned to self-consume. Silent: this is the
        // ordinary gRPC-only pod, not a misconfiguration.
        let redis_url = std::env::var(ENV_REDIS_URL)
            .ok()
            .filter(|s| !s.is_empty())?;

        // Redis URL present means we intend to self-consume, so tenant + fn are
        // now required; missing them is a real misconfiguration worth surfacing.
        let tenant = match std::env::var(ENV_TENANT) {
            Ok(t) if !t.is_empty() => t,
            _ => {
                warn!("{ENV_REDIS_URL} is set but {ENV_TENANT} is missing; self-consumer disabled");
                return None;
            }
        };
        let function_name = match std::env::var(ENV_FUNCTION_NAME) {
            Ok(f) if !f.is_empty() => f,
            _ => {
                warn!(
                    "{ENV_REDIS_URL} is set but {ENV_FUNCTION_NAME} is missing; self-consumer disabled"
                );
                return None;
            }
        };
        let max_concurrent = std::env::var(ENV_MAX_CONCURRENT)
            .ok()
            .and_then(|s| s.parse::<u32>().ok())
            .filter(|&n| n > 0)
            .unwrap_or(1);

        let sem_ttl_secs = std::env::var(ENV_SEM_TTL_SECS)
            .ok()
            .and_then(|s| s.parse::<u64>().ok())
            .filter(|&n| n > 0)
            .unwrap_or(DEFAULT_SEM_TTL_SECS);
        let sem_ttl = Duration::from_secs(sem_ttl_secs);

        let poll_backoff_initial_ms = std::env::var(ENV_POLL_BACKOFF_INITIAL_MS)
            .ok()
            .and_then(|s| s.parse::<u64>().ok())
            .filter(|&n| n > 0)
            .unwrap_or(DEFAULT_POLL_BACKOFF_INITIAL_MS);
        let poll_backoff_initial = Duration::from_millis(poll_backoff_initial_ms);

        let poll_backoff_max_secs = std::env::var(ENV_POLL_BACKOFF_MAX_SECS)
            .ok()
            .and_then(|s| s.parse::<u64>().ok())
            .filter(|&n| n > 0)
            .unwrap_or(DEFAULT_POLL_BACKOFF_MAX_SECS);
        let poll_backoff_max = Duration::from_secs(poll_backoff_max_secs);

        let flush_timeout_ms = std::env::var(ENV_FLUSH_TIMEOUT_MS)
            .ok()
            .and_then(|s| s.parse::<u64>().ok())
            .filter(|&n| n > 0)
            .unwrap_or(DEFAULT_FLUSH_TIMEOUT_MS);
        let flush_timeout = Duration::from_millis(flush_timeout_ms);
        let queue_protocol = std::env::var(ENV_QUEUE_PROTOCOL)
            .ok()
            .filter(|value| !value.is_empty())
            .map(|value| {
                QueueProtocol::from_str(&value).unwrap_or_else(|error| {
                    warn!(%error, "invalid queue protocol; using legacy List transport");
                    QueueProtocol::ListV1
                })
            })
            .unwrap_or_default();
        let stream_read_count = std::env::var(ENV_STREAM_READ_COUNT)
            .ok()
            .and_then(|s| s.parse::<usize>().ok())
            .filter(|&n| n > 0)
            .unwrap_or(DEFAULT_STREAM_READ_COUNT)
            .min(max_concurrent as usize);

        Some(Self {
            redis_url,
            tenant,
            function_name,
            max_concurrent,
            sem_ttl,
            poll_backoff_initial,
            poll_backoff_max,
            flush_timeout,
            queue_protocol,
            stream_read_count,
        })
    }
}

/// Set of lease tokens this pod currently holds. The dispatch loop inserts a
/// token when it admits a call; the worker removes it on completion. The
/// renewer heartbeats whatever is in the set on each tick.
type LiveCalls = Arc<DashMap<String, QueueReceipt>>;

/// Connect to Redis and run the consume loop until the process exits. Returns
/// `Err` only on a fatal setup failure (bad URL / unreachable Redis at startup);
/// transient per-iteration Redis errors are logged and retried so a Redis blip
/// does not tear the consumer down.
pub async fn run(
    config: SelfConsumerConfig,
    handler: Arc<PythonHandler>,
    metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
    coalescing_queue: Option<Arc<CoalescingQueue>>,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let client = Client::open(config.redis_url.clone())?;
    let conn = ConnectionManager::new(client).await?;
    let queue = FunctionQueue::new(conn.clone(), config.tenant.clone());
    let input_queue = queue.bind(&config.function_name, config.queue_protocol);
    let sem = queue.semaphore(&config.function_name, config.max_concurrent, config.sem_ttl);
    let sem_key = queue.sem_key_for(&config.function_name);
    let live_calls: LiveCalls = Arc::new(DashMap::new());
    let consumer_name = format!(
        "{}:{}",
        std::env::var("HOSTNAME").unwrap_or_else(|_| "fnq-shim".to_string()),
        Uuid::new_v4()
    );

    if config.queue_protocol == QueueProtocol::StreamV1 {
        // XGROUP CREATE is a startup operation. Keeping it out of every XREAD
        // and XAUTOCLAIM avoids two avoidable Redis round trips per dispatch
        // window.
        input_queue.initialize_consumer_group().await?;
    }

    spawn_renewer(
        input_queue.clone(),
        conn.clone(),
        sem_key,
        live_calls.clone(),
        config.sem_ttl,
    );

    info!(
        function = %config.function_name,
        tenant = %config.tenant,
        max_concurrent = config.max_concurrent,
        queue_protocol = config.queue_protocol.as_str(),
        stream_read_count = config.stream_read_count,
        consumer = %consumer_name,
        "fnq self-consumer started"
    );

    if config.queue_protocol == QueueProtocol::StreamV1 {
        let legacy_queue = queue.bind(&config.function_name, QueueProtocol::ListV1);
        return run_stream_dispatch_loop(
            &config,
            queue,
            input_queue,
            Some(legacy_queue),
            sem,
            conn,
            consumer_name,
            live_calls,
            handler,
            metrics_pipeline,
            coalescing_queue,
        )
        .await;
    }

    run_list_dispatch_loop(
        &config,
        queue,
        input_queue,
        sem,
        conn,
        consumer_name,
        live_calls,
        handler,
        metrics_pipeline,
        coalescing_queue,
    )
    .await
}

/// Consume the legacy Redis List queue one call at a time. Streams use their
/// own batched dispatch loop above so they never fall through this path.
#[allow(clippy::too_many_arguments)]
async fn run_list_dispatch_loop(
    config: &SelfConsumerConfig,
    queue: FunctionQueue,
    input_queue: BoundFunctionQueue,
    sem: chalk_queue::DistributedSemaphore,
    conn: ConnectionManager,
    consumer_name: String,
    live_calls: LiveCalls,
    handler: Arc<PythonHandler>,
    metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
    coalescing_queue: Option<Arc<CoalescingQueue>>,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let mut backoff = config.poll_backoff_initial;
    loop {
        // Idle-gate: if there is no work, don't take (then immediately release)
        // a semaphore slot — that churn would race genuine acquirers on other
        // pods.
        match input_queue.current_depth().await {
            Ok(0) => {
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
            Ok(_) => backoff = config.poll_backoff_initial,
            Err(e) => {
                warn!(error = %e, "queue depth check failed; backing off");
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
        }

        let lease = match sem.try_acquire().await {
            Ok(Some(lease)) => lease,
            // At capacity across the scaling group: wait for a slot to free.
            Ok(None) => {
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
            Err(e) => {
                warn!(error = %e, "semaphore acquire failed; backing off");
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
        };

        let delivery = match input_queue.dequeue(&consumer_name).await {
            Ok(Some(delivery)) => delivery,
            // Raced another consumer (or our own idle-gate) to an empty queue:
            // give the slot back and retry.
            Ok(None) => {
                let _ = lease.release().await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
            Err(e) => {
                warn!(error = %e, "dequeue failed; releasing slot");
                let _ = lease.release().await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
        };

        backoff = config.poll_backoff_initial;

        dispatch_delivery(
            queue.clone(),
            input_queue.clone(),
            coalescing_queue.clone(),
            handler.clone(),
            conn.clone(),
            delivery,
            lease,
            live_calls.clone(),
            config.flush_timeout,
            metrics_pipeline.clone(),
        );
        // Loop immediately — dispatch as fast as we can acquire + pop. The
        // semaphore (not this loop) is what bounds in-flight work.
    }
}

#[allow(clippy::too_many_arguments)]
async fn run_stream_dispatch_loop(
    config: &SelfConsumerConfig,
    queue: FunctionQueue,
    input_queue: BoundFunctionQueue,
    legacy_queue: Option<BoundFunctionQueue>,
    sem: chalk_queue::DistributedSemaphore,
    conn: ConnectionManager,
    consumer_name: String,
    live_calls: LiveCalls,
    handler: Arc<PythonHandler>,
    metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
    coalescing_queue: Option<Arc<CoalescingQueue>>,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let mut backoff = config.poll_backoff_initial;
    // Reclaim once immediately to recover work from a prior crashed pod, then
    // periodically. Healthy messages are kept alive by `spawn_renewer`.
    let mut last_reclaim = Instant::now() - STREAM_RECLAIM_INTERVAL;

    loop {
        // Capacity must be reserved before XREADGROUP. Reading first would put
        // a potentially huge number of messages into this consumer's PEL while
        // they wait for semaphore slots.
        let mut leases = match sem.try_acquire_many(config.stream_read_count).await {
            Ok(leases) if !leases.is_empty() => leases,
            Ok(_) => {
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
            Err(error) => {
                warn!(%error, "batch semaphore acquire failed; backing off");
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(config.poll_backoff_max);
                continue;
            }
        };

        let mut deliveries = Vec::with_capacity(leases.len());
        if last_reclaim.elapsed() >= STREAM_RECLAIM_INTERVAL {
            last_reclaim = Instant::now();
            match input_queue
                .reclaim_stale(&consumer_name, config.sem_ttl, leases.len())
                .await
            {
                Ok(reclaimed) => deliveries.extend(reclaimed),
                Err(error) => {
                    warn!(%error, "Stream recovery scan failed; continuing with new work")
                }
            }
        }

        // During the one-way List → Stream migration, drain old List entries
        // before reading new Stream traffic. This is one bounded operation per
        // read window, not an LLEN on every Stream message.
        if deliveries.len() < leases.len() {
            if let Some(legacy_queue) = &legacy_queue {
                match legacy_queue
                    .dequeue_many(&consumer_name, leases.len() - deliveries.len())
                    .await
                {
                    Ok(legacy) if !legacy.is_empty() => {
                        info!(function = %input_queue.function_name(), count = legacy.len(), "draining legacy List items during Stream migration");
                        deliveries.extend(legacy);
                    }
                    Ok(_) => {}
                    Err(error) => {
                        warn!(%error, "legacy List dequeue failed; continuing with Stream work")
                    }
                }
            }
        }
        if deliveries.len() < leases.len() {
            match input_queue
                .dequeue_many(&consumer_name, leases.len() - deliveries.len())
                .await
            {
                Ok(new_deliveries) => deliveries.extend(new_deliveries),
                Err(error) => warn!(%error, "batched Stream dequeue failed"),
            }
        }

        if deliveries.is_empty() {
            for lease in leases {
                let _ = lease.release().await;
            }
            tokio::time::sleep(backoff).await;
            backoff = (backoff * 2).min(config.poll_backoff_max);
            continue;
        }

        backoff = config.poll_backoff_initial;
        // `dequeue_many` can return fewer records than requested. Only retain
        // one lease per record and immediately return the unneeded capacity.
        let used = deliveries.len().min(leases.len());
        let unused = leases.split_off(used);
        for lease in unused {
            let _ = lease.release().await;
        }
        for (delivery, lease) in deliveries.into_iter().zip(leases) {
            dispatch_delivery(
                queue.clone(),
                input_queue.clone(),
                coalescing_queue.clone(),
                handler.clone(),
                conn.clone(),
                delivery,
                lease,
                live_calls.clone(),
                config.flush_timeout,
                metrics_pipeline.clone(),
            );
        }
    }
}

#[allow(clippy::too_many_arguments)]
fn dispatch_delivery(
    queue: FunctionQueue,
    input_queue: BoundFunctionQueue,
    coalescing_queue: Option<Arc<CoalescingQueue>>,
    handler: Arc<PythonHandler>,
    conn: ConnectionManager,
    delivery: DequeuedCall,
    lease: SemaphoreLease,
    live_calls: LiveCalls,
    flush_timeout: Duration,
    metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
) {
    live_calls.insert(lease.token().to_string(), delivery.receipt.clone());
    match coalescing_queue {
        Some(cq) => {
            tokio::spawn(run_one_coalesced_call(
                queue,
                input_queue,
                cq,
                conn,
                delivery,
                lease,
                live_calls,
                metrics_pipeline,
            ));
        }
        None => {
            tokio::spawn(run_one_call(
                handler,
                queue,
                input_queue,
                conn,
                delivery,
                lease,
                live_calls,
                flush_timeout,
                metrics_pipeline,
            ));
        }
    }
}

/// Run a single queued call to completion, write its results to the call's
/// stream, then deregister + release its lease. Always releases the lease,
/// even if execution or stream writes fail or panic.
#[allow(clippy::too_many_arguments)]
async fn run_one_call(
    handler: Arc<PythonHandler>,
    queue: FunctionQueue,
    input_queue: BoundFunctionQueue,
    mut conn: ConnectionManager,
    delivery: DequeuedCall,
    lease: SemaphoreLease,
    live_calls: LiveCalls,
    flush_timeout: Duration,
    metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
) {
    let attempt = match input_queue.delivery_attempt(&delivery).await {
        Ok(attempt) => attempt,
        Err(error) => {
            error!(call_id = %delivery.call.call_id, %error, "failed to resolve delivery attempt");
            finish_delivery(
                &input_queue,
                &delivery.receipt,
                false,
                &delivery.call.call_id,
                lease,
                &live_calls,
            )
            .await;
            return;
        }
    };
    let DequeuedCall {
        call: work,
        receipt,
    } = delivery;
    let call_id = work.call_id.clone();
    let final_attempt = match attempt {
        DeliveryAttempt::Ready {
            attempt,
            max_attempts,
        } => {
            info!(%call_id, attempt, max_attempts, "executing queued call attempt");
            attempt == max_attempts
        }
        DeliveryAttempt::Exhausted {
            attempts,
            max_attempts,
        } => {
            let message = format!(
                "retry attempts exhausted after {attempts} deliveries ({max_attempts} executions allowed)"
            );
            let completed = write_terminal_error(
                &queue,
                &mut conn,
                &work,
                "RetryAttemptsExhausted",
                &message,
                None,
            )
            .await
            .is_ok();
            finish_delivery(
                &input_queue,
                &receipt,
                completed,
                &call_id,
                lease,
                &live_calls,
            )
            .await;
            return;
        }
        DeliveryAttempt::OwnershipLost => {
            finish_delivery(&input_queue, &receipt, false, &call_id, lease, &live_calls).await;
            return;
        }
    };
    let completed = match AssertUnwindSafe(execute_and_write(
        &handler,
        &queue,
        &mut conn,
        work.clone(),
        flush_timeout,
        final_attempt,
        metrics_pipeline.as_ref(),
    ))
    .catch_unwind()
    .await
    {
        Ok(Ok(completed)) => completed,
        Ok(Err(e)) => {
            // The call's result stream may be incomplete; the enqueue safety TTL
            // and the meta status are the backstop for a stuck poller.
            error!(call_id = %call_id, error = %e, "failed to execute/write queued call");
            false
        }
        Err(panic_payload) => {
            let panic_message = panic_payload
                .downcast_ref::<&'static str>()
                .copied()
                .or_else(|| panic_payload.downcast_ref::<String>().map(String::as_str))
                .unwrap_or("non-string panic payload");
            error!(
                call_id = %call_id,
                panic = %panic_message,
                "panic while executing/writing queued call"
            );
            if final_attempt {
                write_terminal_error(
                    &queue,
                    &mut conn,
                    &work,
                    "RemoteFunctionPanic",
                    panic_message,
                    None,
                )
                .await
                .is_ok()
            } else {
                false
            }
        }
    };

    finish_delivery(
        &input_queue,
        &receipt,
        completed,
        &call_id,
        lease,
        &live_calls,
    )
    .await;
}

async fn finish_delivery(
    queue: &BoundFunctionQueue,
    receipt: &QueueReceipt,
    completed: bool,
    call_id: &str,
    lease: SemaphoreLease,
    live_calls: &LiveCalls,
) {
    // Stop renewing before ack. If completion or ack failed, the Stream item
    // becomes reclaimable after the idle timeout; List behavior is unchanged.
    live_calls.remove(lease.token());
    if completed {
        match queue.acknowledge(receipt).await {
            Ok(true) => {}
            Ok(false) => warn!(%call_id, "delivery ownership was lost before acknowledgement"),
            Err(error) => {
                warn!(%call_id, %error, "delivery acknowledgement failed; item will be reclaimed")
            }
        }
    }
    if let Err(e) = lease.release().await {
        warn!(call_id = %call_id, error = %e, "failed to release semaphore slot (will auto-recover after ttl)");
    }
}

/// Coalesced counterpart to [`run_one_call`]: submit the call into the shared
/// [`CoalescingQueue`], write its single result blob to the call's stream, then
/// deregister + release its lease (always, even on failure).
#[allow(clippy::too_many_arguments)]
async fn run_one_coalesced_call(
    queue: FunctionQueue,
    input_queue: BoundFunctionQueue,
    coalescing_queue: Arc<CoalescingQueue>,
    mut conn: ConnectionManager,
    delivery: DequeuedCall,
    lease: SemaphoreLease,
    live_calls: LiveCalls,
    metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
) {
    let attempt = match input_queue.delivery_attempt(&delivery).await {
        Ok(attempt) => attempt,
        Err(error) => {
            error!(call_id = %delivery.call.call_id, %error, "failed to resolve delivery attempt");
            finish_delivery(
                &input_queue,
                &delivery.receipt,
                false,
                &delivery.call.call_id,
                lease,
                &live_calls,
            )
            .await;
            return;
        }
    };
    let DequeuedCall {
        call: work,
        receipt,
    } = delivery;
    let call_id = work.call_id.clone();
    let final_attempt = match attempt {
        DeliveryAttempt::Ready {
            attempt,
            max_attempts,
        } => {
            info!(%call_id, attempt, max_attempts, "executing coalesced queued call attempt");
            attempt == max_attempts
        }
        DeliveryAttempt::Exhausted {
            attempts,
            max_attempts,
        } => {
            let message = format!(
                "retry attempts exhausted after {attempts} deliveries ({max_attempts} executions allowed)"
            );
            let completed = write_terminal_error(
                &queue,
                &mut conn,
                &work,
                "RetryAttemptsExhausted",
                &message,
                None,
            )
            .await
            .is_ok();
            finish_delivery(
                &input_queue,
                &receipt,
                completed,
                &call_id,
                lease,
                &live_calls,
            )
            .await;
            return;
        }
        DeliveryAttempt::OwnershipLost => {
            finish_delivery(&input_queue, &receipt, false, &call_id, lease, &live_calls).await;
            return;
        }
    };
    let completed = match coalesced_execute_and_write(
        &coalescing_queue,
        &queue,
        &mut conn,
        work,
        final_attempt,
        metrics_pipeline.as_ref(),
    )
    .await
    {
        Ok(completed) => completed,
        Err(e) => {
            // The call's result stream may be incomplete; the enqueue safety TTL
            // and the meta status are the backstop for a stuck poller.
            error!(call_id = %call_id, error = %e, "failed to execute/write coalesced queued call");
            false
        }
    };

    finish_delivery(
        &input_queue,
        &receipt,
        completed,
        &call_id,
        lease,
        &live_calls,
    )
    .await;
}

/// Submit one call into the shared coalescing queue and relay its single
/// response to the call's result stream. The batched bridge returns exactly one
/// blob per caller (no incremental streaming), so the outcome is one `chunk`
/// followed by `end` — or an `error` entry. Mirrors the catalog-consumer
/// coalescing path, which likewise produced one response per caller.
async fn coalesced_execute_and_write(
    coalescing_queue: &Arc<CoalescingQueue>,
    queue: &FunctionQueue,
    conn: &mut ConnectionManager,
    work: QueuedCall,
    final_attempt: bool,
    metrics_pipeline: Option<&Arc<PublishingMetricsPipeline>>,
) -> Result<bool, Box<dyn std::error::Error + Send + Sync>> {
    let call_uuid = Uuid::parse_str(&work.call_id)?;
    let result_destination = ResultDestination::for_call(queue, &work, call_uuid);
    let ipc_bytes = work.call.feather_bytes()?;
    let function_name = work.call.name.clone();
    let mut metadata = work.metadata.otel_headers.clone();
    let processing_trace_id = ensure_traceparent(&mut metadata);
    let started = Instant::now();

    let _ = queue.update_status(call_uuid, "running").await;
    info!(call_id = %work.call_id, function = %function_name, "running coalesced queued call");

    // Capacity 1: the coalescing dispatch sends exactly one message per caller.
    let (tx, mut rx) = mpsc::channel(1);
    coalescing_queue
        .clone()
        .submit(BufferedCall {
            input: CallerInput {
                ipc_bytes,
                function_name: function_name.clone(),
                metadata,
                peer: PEER.to_string(),
            },
            response_tx: tx,
        })
        .await;

    let response = rx.recv().await;

    // Record metrics once the batch has produced this caller's result, before
    // stream writes below — parity with the streaming path.
    let success = matches!(response, Some(Ok(_)));
    if let Some(p) = metrics_pipeline {
        crate::metrics::record_completed_call(
            p,
            &function_name,
            success,
            started.elapsed(),
            Mode::Async,
        );
    }

    match response {
        Some(Ok(resp)) => {
            result_destination
                .write_chunk(conn, 1, &resp.feather_stream)
                .await?;
            result_destination.write_end(conn, 2).await?;
            let _ = queue
                .complete_status(
                    call_uuid,
                    "completed",
                    "1 chunk(s)",
                    Some(processing_trace_id),
                )
                .await;
            info!(call_id = %work.call_id, "coalesced queued call completed");
        }
        Some(Err(status)) => {
            if !final_attempt {
                warn!(call_id = %work.call_id, error = %status, "coalesced queued call failed; leaving delivery pending for retry");
                return Ok(false);
            }
            // Parity with the enqueue/poll path: only a message string is
            // available, so exc_type is a fixed placeholder.
            result_destination
                .write_error(conn, 1, "RemoteFunctionError", status.message(), None)
                .await?;
            let summary: String = status.message().chars().take(200).collect();
            let _ = queue
                .complete_status(call_uuid, "failed", &summary, Some(processing_trace_id))
                .await;
            error!(call_id = %work.call_id, error = %status, "coalesced queued call failed");
        }
        None => {
            // The dispatch task dropped our sender without sending — should not
            // happen (it always sends one Ok/Err per caller), but treat a
            // missing response as a failure rather than leaving the poller hung.
            let msg = "coalesced dispatch produced no response";
            if !final_attempt {
                warn!(call_id = %work.call_id, "{msg}; leaving delivery pending for retry");
                return Ok(false);
            }
            result_destination
                .write_error(conn, 1, "RemoteFunctionError", msg, None)
                .await?;
            let _ = queue
                .complete_status(call_uuid, "failed", msg, Some(processing_trace_id))
                .await;
            error!(call_id = %work.call_id, "{msg}");
        }
    }
    Ok(true)
}

// Insert trace ID into headers if none already present
fn ensure_traceparent(headers: &mut HashMap<String, String>) -> String {
    if let Some(tp) = headers.get("traceparent") {
        if let Some(trace_id) = tp.split('-').nth(1).filter(|s| s.len() == 32) {
            return trace_id.to_string();
        }
    }
    let trace_id = Uuid::new_v4().simple().to_string();
    let span_id = &Uuid::new_v4().simple().to_string()[..16];
    headers.insert(
        "traceparent".to_string(),
        format!("00-{trace_id}-{span_id}-01"),
    );
    trace_id
}

/// Decode the payload, invoke the handler, and write the outcome (chunks then
/// `end`, or `error`) to the call's result stream, updating meta status along
/// the way.
async fn execute_and_write(
    handler: &PythonHandler,
    queue: &FunctionQueue,
    conn: &mut ConnectionManager,
    work: QueuedCall,
    flush_timeout: Duration,
    final_attempt: bool,
    metrics_pipeline: Option<&Arc<PublishingMetricsPipeline>>,
) -> Result<bool, Box<dyn std::error::Error + Send + Sync>> {
    let call_uuid = Uuid::parse_str(&work.call_id)?;
    let result_destination = ResultDestination::for_call(queue, &work, call_uuid);
    let ipc_bytes = work.call.feather_bytes()?;
    let function_name = work.call.name.clone();
    let mut metadata = work.metadata.otel_headers.clone();
    let processing_trace_id = ensure_traceparent(&mut metadata);
    let started = Instant::now();

    let _ = queue.update_status(call_uuid, "running").await;
    info!(call_id = %work.call_id, function = %function_name, "running queued call");

    // The Python bridge appends each generator yield into `buffer`. Calls
    // without retries flush incrementally; retry-enabled calls retain chunks
    // until the attempt succeeds so a later attempt cannot duplicate output.
    let buffer = ChunkBuffer::new().into_shared();
    let handler_fut = handler.call_into_buffer(
        ipc_bytes,
        function_name.clone(),
        metadata,
        PEER.to_string(),
        buffer.clone(),
    );
    tokio::pin!(handler_fut);

    // `seq` starts at 1: the producer pre-seeds the stream with a `sentinel` at
    // seq 0. `flushed` is the count of chunks already written to the stream.
    let mut seq: u64 = 1;
    let mut flushed: usize = 0;
    // A retry must not duplicate generator chunks. Retry-enabled calls buffer
    // output until the handler succeeds or reaches its final attempt.
    let buffer_until_terminal = work.max_retries.is_some();

    // Completion is driven by the handler future resolving, NOT by the buffer
    // emitter being torn down — so a handler that pins its emitter (e.g. via a
    // retained exception traceback) cannot wedge this loop. `biased` checks
    // completion before the wait so a finished call exits promptly.
    let result = loop {
        let notify_handle = {
            let buf = buffer
                .lock()
                .expect("chunk buffer: mutex poisoned (emitter task panicked)");
            buf.notify_handle()
        };
        tokio::select! {
            biased;
            res = &mut handler_fut => break res,
            _ = tokio::time::timeout(flush_timeout, notify_handle.notified()) => {
                if !buffer_until_terminal {
                    if let Err(e) = flush_new(conn, &result_destination, &buffer, &mut flushed, &mut seq).await {
                        // Non-fatal: keep draining; the cursor didn't advance past the
                        // failed chunk, so the next wait retries it without duplicating.
                        warn!(call_id = %work.call_id, error = %e, "failed to flush partial results; retrying");
                    }
                }
            }
        }
    };

    // Emit metrics as soon as execution finishes, before result-stream writes,
    // so every executed call is recorded regardless of downstream Redis write
    // failure. Mirrors the catalog consumer's per-call emission.
    if let Some(p) = metrics_pipeline {
        crate::metrics::record_completed_call(
            p,
            &function_name,
            result.is_ok(),
            started.elapsed(),
            Mode::Async,
        );
    }

    if result.is_err() && !final_attempt {
        warn!(call_id = %work.call_id, "queued call failed; leaving delivery pending for retry");
        return Ok(false);
    }

    // Flush whatever the handler produced after the loop exits (on the fast path
    // this is everything). This happens even if the handler panicked mid-execution,
    // so partial output is always preserved. Parity with the enqueue/poll path: a
    // generator that yields then raises surfaces its chunks followed by the error.
    if let Err(e) = flush_new(conn, &result_destination, &buffer, &mut flushed, &mut seq).await {
        warn!(call_id = %work.call_id, error = %e, "failed to flush final chunks");
    }

    match result {
        Ok(()) => {
            result_destination.write_end(conn, seq).await?;
            let _ = queue
                .complete_status(
                    call_uuid,
                    "completed",
                    &format!("{flushed} chunk(s)"),
                    Some(processing_trace_id),
                )
                .await;
            info!(call_id = %work.call_id, chunks = flushed, "queued call completed");
        }
        Err(e) => {
            result_destination
                .write_error(
                    conn,
                    seq,
                    "RemoteFunctionError",
                    &e.to_string(),
                    Some(e.details()),
                )
                .await?;
            let summary: String = e.to_string().chars().take(200).collect();
            let _ = queue
                .complete_status(call_uuid, "failed", &summary, Some(processing_trace_id))
                .await;
            error!(
                call_id = %work.call_id,
                exception.stacktrace = e.details(),
                "queued call failed: {}",
                e.details()
            );
        }
    }
    Ok(true)
}

async fn write_terminal_error(
    queue: &FunctionQueue,
    conn: &mut ConnectionManager,
    work: &QueuedCall,
    exc_type: &str,
    message: &str,
    traceback: Option<&str>,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let call_uuid = Uuid::parse_str(&work.call_id)?;
    let result_destination = ResultDestination::for_call(queue, work, call_uuid);
    result_destination
        .write_error(conn, 1, exc_type, message, traceback)
        .await?;
    let summary: String = message.chars().take(200).collect();
    let processing_trace_id = work
        .metadata
        .otel_headers
        .get("traceparent")
        .and_then(|value| value.split('-').nth(1))
        .filter(|value| value.len() == 32)
        .map(str::to_string);
    let _ = queue
        .complete_status(call_uuid, "failed", &summary, processing_trace_id)
        .await;
    error!(call_id = %work.call_id, %message, "queued call reached terminal failure");
    Ok(())
}

/// Write the chunks appended to `buffer` since the last flush to the result
/// stream, advancing `flushed`/`seq` per successful write. Snapshots the new
/// chunks under a short lock, then writes them unlocked so the handler's emitter
/// is never blocked on Redis I/O. On a write error the cursor stops at the
/// failed chunk, so a retry re-sends only the unwritten tail (no gaps, no dupes).
async fn flush_new(
    conn: &mut ConnectionManager,
    result_destination: &ResultDestination,
    buffer: &Arc<Mutex<ChunkBuffer>>,
    flushed: &mut usize,
    seq: &mut u64,
) -> Result<(), redis::RedisError> {
    let new: Vec<Vec<u8>> = {
        let buf = buffer
            .lock()
            .expect("chunk buffer: mutex poisoned (emitter panicked while holding lock)");
        buf.chunks()[*flushed..]
            .iter()
            .map(|c| c.feather_stream.to_vec())
            .collect()
    };
    for chunk in &new {
        result_destination.write_chunk(conn, *seq, chunk).await?;
        *seq += 1;
        *flushed += 1;
    }
    Ok(())
}

/// Spawn the single per-pod renewer: every `SEM_RENEW_INTERVAL` it heartbeats
/// all currently-held lease tokens in one `renew_many` round-trip. A reclaimed
/// token means this pod stalled past `sem_ttl` without renewing. Stream
/// receipts are renewed in grouped round trips too; ownership loss is surfaced
/// because a GIL-blocked handler cannot be aborted, while the reclaimed call may
/// already be running on another pod.
fn spawn_renewer(
    queue: BoundFunctionQueue,
    mut conn: ConnectionManager,
    sem_key: String,
    live_calls: LiveCalls,
    sem_ttl: Duration,
) {
    tokio::spawn(async move {
        let mut ticker = tokio::time::interval(SEM_RENEW_INTERVAL);
        ticker.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
        loop {
            ticker.tick().await;
            let active: Vec<(String, QueueReceipt)> = live_calls
                .iter()
                .map(|entry| (entry.key().clone(), entry.value().clone()))
                .collect();
            let tokens: Vec<String> = active.iter().map(|(token, _)| token.clone()).collect();
            if tokens.is_empty() {
                continue;
            }
            match renew_many(&mut conn, &sem_key, sem_ttl, &tokens).await {
                Ok(lost) if !lost.is_empty() => {
                    warn!(
                        count = lost.len(),
                        "semaphore leases reclaimed mid-flight (pod stalled past ttl)"
                    );
                }
                Ok(_) => {}
                Err(e) => warn!(error = %e, "batch lease renew failed"),
            }
            let receipts: Vec<QueueReceipt> =
                active.into_iter().map(|(_, receipt)| receipt).collect();
            match queue.heartbeat_many(&receipts).await {
                Ok(lost) if !lost.is_empty() => warn!(
                    count = lost.len(),
                    "Stream deliveries reclaimed while calls were still running"
                ),
                Ok(_) => {}
                Err(error) => warn!(%error, "batch Stream delivery renewal failed"),
            }
        }
    });
}

#[cfg(test)]
mod tests {
    use super::*;

    static ENV_LOCK: std::sync::Mutex<()> = std::sync::Mutex::new(());

    fn lock_env() -> std::sync::MutexGuard<'static, ()> {
        ENV_LOCK.lock().expect("env lock poisoned")
    }

    #[test]
    fn test_default_constants() {
        assert_eq!(DEFAULT_SEM_TTL_SECS, 30);
        assert_eq!(DEFAULT_POLL_BACKOFF_INITIAL_MS, 100);
        assert_eq!(DEFAULT_POLL_BACKOFF_MAX_SECS, 2);
        assert_eq!(DEFAULT_FLUSH_TIMEOUT_MS, 100);
    }

    #[test]
    fn result_destination_preserves_per_call_stream() {
        assert_eq!(
            ResultDestination::from_routing(
                "tenant:gen:call-1:stream".to_string(),
                Duration::from_secs(60),
                None,
            ),
            ResultDestination::PerCall {
                stream_key: "tenant:gen:call-1:stream".to_string(),
                result_ttl: Duration::from_secs(60),
            }
        );
    }

    #[test]
    fn result_destination_routes_batch_call_with_correlation() {
        assert_eq!(
            ResultDestination::from_routing(
                "unused-per-call-stream".to_string(),
                Duration::from_secs(60),
                Some((
                    "tenant:batch:batch-1:results".to_string(),
                    "call-1".to_string(),
                    42,
                )),
            ),
            ResultDestination::Batch {
                stream_key: "tenant:batch:batch-1:results".to_string(),
                call_id: "call-1".to_string(),
                row_index: 42,
            }
        );
    }

    #[test]
    fn test_config_from_env_returns_none_when_redis_url_unset() {
        let _env = lock_env();

        std::env::remove_var(ENV_REDIS_URL);
        assert!(SelfConsumerConfig::from_env().is_none());
    }

    #[test]
    fn test_timeout_parsing_with_defaults() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");
        std::env::remove_var(ENV_SEM_TTL_SECS);
        std::env::remove_var(ENV_POLL_BACKOFF_INITIAL_MS);
        std::env::remove_var(ENV_POLL_BACKOFF_MAX_SECS);
        std::env::remove_var(ENV_FLUSH_TIMEOUT_MS);
        std::env::remove_var(ENV_QUEUE_PROTOCOL);
        std::env::remove_var(ENV_STREAM_READ_COUNT);
        std::env::remove_var(ENV_MAX_CONCURRENT);

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.sem_ttl, Duration::from_secs(DEFAULT_SEM_TTL_SECS));
        assert_eq!(
            config.poll_backoff_initial,
            Duration::from_millis(DEFAULT_POLL_BACKOFF_INITIAL_MS)
        );
        assert_eq!(
            config.poll_backoff_max,
            Duration::from_secs(DEFAULT_POLL_BACKOFF_MAX_SECS)
        );
        assert_eq!(
            config.flush_timeout,
            Duration::from_millis(DEFAULT_FLUSH_TIMEOUT_MS)
        );
        assert_eq!(config.queue_protocol, QueueProtocol::ListV1);
        assert_eq!(config.stream_read_count, 1);
    }

    #[test]
    fn test_timeout_parsing_with_custom_values() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");
        std::env::set_var(ENV_SEM_TTL_SECS, "60");
        std::env::set_var(ENV_POLL_BACKOFF_INITIAL_MS, "200");
        std::env::set_var(ENV_POLL_BACKOFF_MAX_SECS, "5");
        std::env::set_var(ENV_FLUSH_TIMEOUT_MS, "250");

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.sem_ttl, Duration::from_secs(60));
        assert_eq!(config.poll_backoff_initial, Duration::from_millis(200));
        assert_eq!(config.poll_backoff_max, Duration::from_secs(5));
        assert_eq!(config.flush_timeout, Duration::from_millis(250));
    }

    #[test]
    fn test_max_concurrent_defaults_to_one() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");
        std::env::remove_var(ENV_MAX_CONCURRENT);

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.max_concurrent, 1);
    }

    #[test]
    fn test_stream_queue_protocol_from_env() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");
        std::env::set_var(ENV_QUEUE_PROTOCOL, "stream_v1");
        std::env::set_var(ENV_MAX_CONCURRENT, "128");
        std::env::remove_var(ENV_STREAM_READ_COUNT);

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.queue_protocol, QueueProtocol::StreamV1);
        assert_eq!(config.stream_read_count, DEFAULT_STREAM_READ_COUNT);
        std::env::remove_var(ENV_QUEUE_PROTOCOL);
        std::env::remove_var(ENV_STREAM_READ_COUNT);
    }

    #[test]
    fn test_stream_read_count_is_configurable_and_capped_by_concurrency() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");
        std::env::set_var(ENV_MAX_CONCURRENT, "32");
        std::env::set_var(ENV_STREAM_READ_COUNT, "128");

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.stream_read_count, 32);
        std::env::remove_var(ENV_STREAM_READ_COUNT);
    }

    #[test]
    fn test_invalid_timeout_values_use_defaults() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");
        std::env::set_var(ENV_SEM_TTL_SECS, "not_a_number");
        std::env::set_var(ENV_POLL_BACKOFF_INITIAL_MS, "0");
        std::env::set_var(ENV_POLL_BACKOFF_MAX_SECS, "-5");

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.sem_ttl, Duration::from_secs(DEFAULT_SEM_TTL_SECS));
        assert_eq!(
            config.poll_backoff_initial,
            Duration::from_millis(DEFAULT_POLL_BACKOFF_INITIAL_MS)
        );
        assert_eq!(
            config.poll_backoff_max,
            Duration::from_secs(DEFAULT_POLL_BACKOFF_MAX_SECS)
        );
    }

    #[test]
    fn test_chunk_buffer_locking_and_access() {
        use bytes::Bytes;
        use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

        let buffer = {
            let mut buf = ChunkBuffer::new();
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("chunk1"),
            });
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("chunk2"),
            });
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("chunk3"),
            });
            buf.into_shared()
        };

        // Lock and verify chunks can be accessed
        let buf_guard = buffer.lock().expect("chunk buffer: mutex poisoned");
        assert_eq!(buf_guard.len(), 3);
        let chunks = buf_guard.chunks();
        assert_eq!(chunks.len(), 3);
        assert_eq!(chunks[0].feather_stream, Bytes::from("chunk1"));
        assert_eq!(chunks[1].feather_stream, Bytes::from("chunk2"));
        assert_eq!(chunks[2].feather_stream, Bytes::from("chunk3"));
    }

    #[test]
    fn test_chunk_buffer_slice_extraction() {
        use bytes::Bytes;
        use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

        let buffer = {
            let mut buf = ChunkBuffer::new();
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("chunk1"),
            });
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("chunk2"),
            });
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("chunk3"),
            });
            buf.into_shared()
        };

        // Test slicing behavior used in flush_new
        let buf_guard = buffer.lock().expect("chunk buffer: mutex poisoned");

        // Extract from start
        let slice = &buf_guard.chunks()[0..];
        assert_eq!(slice.len(), 3);

        // Extract from middle (mimicking flushed cursor)
        let flushed = 1;
        let slice = &buf_guard.chunks()[flushed..];
        assert_eq!(slice.len(), 2);
        assert_eq!(slice[0].feather_stream, Bytes::from("chunk2"));

        // Extract from near end
        let flushed = 2;
        let slice = &buf_guard.chunks()[flushed..];
        assert_eq!(slice.len(), 1);
        assert_eq!(slice[0].feather_stream, Bytes::from("chunk3"));
    }

    #[test]
    fn test_chunk_buffer_notification() {
        use bytes::Bytes;
        use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

        let buffer = {
            let mut buf = ChunkBuffer::new();
            buf.push(CallFunctionResponse {
                feather_stream: Bytes::from("test"),
            });
            buf.into_shared()
        };

        let buf_guard = buffer.lock().expect("chunk buffer: mutex poisoned");
        let notify_handle = buf_guard.notify_handle();

        // Verify notify_handle can be cloned (Arc behavior)
        let _notify_handle_clone = notify_handle.clone();
        assert!(!std::ptr::eq(&notify_handle, &_notify_handle_clone));
        // But they should point to the same underlying Notify
    }

    #[test]
    fn test_exponential_backoff_doubles() {
        let mut backoff = Duration::from_millis(100);
        let max_backoff = Duration::from_secs(2);

        // First doubling: 100ms * 2 = 200ms
        backoff = (backoff * 2).min(max_backoff);
        assert_eq!(backoff, Duration::from_millis(200));

        // Second: 200ms * 2 = 400ms
        backoff = (backoff * 2).min(max_backoff);
        assert_eq!(backoff, Duration::from_millis(400));

        // Third: 400ms * 2 = 800ms
        backoff = (backoff * 2).min(max_backoff);
        assert_eq!(backoff, Duration::from_millis(800));

        // Fourth: 800ms * 2 = 1600ms
        backoff = (backoff * 2).min(max_backoff);
        assert_eq!(backoff, Duration::from_millis(1600));

        // Fifth: would be 3200ms, capped at 2000ms (max_backoff)
        backoff = (backoff * 2).min(max_backoff);
        assert_eq!(backoff, Duration::from_secs(2));

        // Stay capped
        backoff = (backoff * 2).min(max_backoff);
        assert_eq!(backoff, Duration::from_secs(2));
    }

    #[test]
    fn test_missing_tenant_disables_consumer() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::remove_var(ENV_TENANT);
        std::env::set_var(ENV_FUNCTION_NAME, "test_fn");

        let config = SelfConsumerConfig::from_env();
        assert!(
            config.is_none(),
            "should be disabled when tenant is missing"
        );
    }

    #[test]
    fn test_missing_function_name_disables_consumer() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost");
        std::env::set_var(ENV_TENANT, "test_tenant");
        std::env::remove_var(ENV_FUNCTION_NAME);

        let config = SelfConsumerConfig::from_env();
        assert!(
            config.is_none(),
            "should be disabled when function_name is missing"
        );
    }

    #[test]
    fn test_config_all_required_fields() {
        let _env = lock_env();

        std::env::set_var(ENV_REDIS_URL, "redis://localhost:6379");
        std::env::set_var(ENV_TENANT, "my_tenant");
        std::env::set_var(ENV_FUNCTION_NAME, "my_function");
        std::env::set_var(ENV_MAX_CONCURRENT, "10");

        let config = SelfConsumerConfig::from_env().expect("config should parse");
        assert_eq!(config.redis_url, "redis://localhost:6379");
        assert_eq!(config.tenant, "my_tenant");
        assert_eq!(config.function_name, "my_function");
        assert_eq!(config.max_concurrent, 10);
    }

    // Integration tests for live token tracking and core dispatch logic
    #[tokio::test]
    async fn test_live_tokens_insert_and_remove() {
        let live_calls: LiveCalls = Arc::new(DashMap::new());
        let token1 = "lease-token-1";
        let token2 = "lease-token-2";

        // Simulate dispatch: register tokens as calls are admitted
        live_calls.insert(token1.to_string(), QueueReceipt::ListV1);
        live_calls.insert(token2.to_string(), QueueReceipt::ListV1);

        assert!(live_calls.contains_key(token1));
        assert!(live_calls.contains_key(token2));
        assert_eq!(live_calls.iter().count(), 2, "should track both tokens");

        // Simulate cleanup: remove as calls complete
        live_calls.remove(token1);
        assert!(!live_calls.contains_key(token1));
        assert!(live_calls.contains_key(token2));
        assert_eq!(live_calls.iter().count(), 1);

        // Final cleanup
        live_calls.remove(token2);
        assert_eq!(live_calls.iter().count(), 0, "all tokens cleaned up");
    }

    #[tokio::test]
    async fn test_live_tokens_concurrent_access() {
        let live_calls: LiveCalls = Arc::new(DashMap::new());
        let mut handles = vec![];

        // Spawn 10 tasks that each insert and remove a token
        for i in 0..10 {
            let calls = live_calls.clone();
            let handle = tokio::spawn(async move {
                let token = format!("token-{}", i);
                calls.insert(token.clone(), QueueReceipt::ListV1);
                tokio::time::sleep(Duration::from_millis(1)).await;
                calls.remove(&token);
            });
            handles.push(handle);
        }

        // Wait for all tasks
        for handle in handles {
            handle.await.expect("task should complete");
        }

        // All tokens should be cleaned up
        assert_eq!(
            live_calls.iter().count(),
            0,
            "concurrent inserts/removes should leave set empty"
        );
    }

    #[test]
    fn test_chunk_buffer_new_and_basic_operations() {
        use bytes::Bytes;
        use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

        let mut buffer = ChunkBuffer::new();
        assert_eq!(buffer.len(), 0);

        // Add chunks
        buffer.push(CallFunctionResponse {
            feather_stream: Bytes::from("chunk1"),
        });
        buffer.push(CallFunctionResponse {
            feather_stream: Bytes::from("chunk2"),
        });

        assert_eq!(buffer.len(), 2);
        let chunks = buffer.chunks();
        assert_eq!(chunks.len(), 2);
        assert_eq!(chunks[0].feather_stream, Bytes::from("chunk1"));
        assert_eq!(chunks[1].feather_stream, Bytes::from("chunk2"));
    }

    #[test]
    fn test_chunk_buffer_into_shared_and_access() {
        use bytes::Bytes;
        use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

        let mut buffer = ChunkBuffer::new();
        buffer.push(CallFunctionResponse {
            feather_stream: Bytes::from("test"),
        });

        let shared = buffer.into_shared();

        // Lock and verify access
        let guard = shared.lock().expect("mutex not poisoned");
        assert_eq!(guard.len(), 1);
        assert_eq!(guard.chunks()[0].feather_stream, Bytes::from("test"));
    }

    #[test]
    fn test_chunk_buffer_slicing_for_flush() {
        use bytes::Bytes;
        use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

        let mut buffer = ChunkBuffer::new();
        for i in 0..5 {
            buffer.push(CallFunctionResponse {
                feather_stream: Bytes::from(format!("chunk{}", i)),
            });
        }

        // Simulate flush_new: extract chunks starting at index 2
        let flushed = 2;
        let chunks = buffer.chunks();
        let remaining = &chunks[flushed..];

        assert_eq!(remaining.len(), 3);
        assert_eq!(remaining[0].feather_stream, Bytes::from("chunk2"));
        assert_eq!(remaining[1].feather_stream, Bytes::from("chunk3"));
        assert_eq!(remaining[2].feather_stream, Bytes::from("chunk4"));
    }
}
