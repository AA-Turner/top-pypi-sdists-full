use std::collections::HashMap;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use chalk_remote_call_proto::chalk::common::v1::ChalkError;
use chalk_remote_call_proto::chalk::runtime::v1::async_remote_call_service_server::AsyncRemoteCallService;
use chalk_remote_call_proto::chalk::runtime::v1::{
    remote_call_args, EnqueueRemoteCallRequest, EnqueueRemoteCallResponse, PollRemoteCallRequest,
    PollRemoteCallResponse, PurgeQueueRequest, PurgeQueueResponse, RemoteCallStatus,
};
use tonic::{Request, Response, Status};
use tracing::{debug, error, info, instrument, warn};

use crate::python_bridge::{ChunkBuffer, PythonHandler};
use crate::service::extract_metadata;

/// How often the orphan sweeper runs.
const SWEEP_INTERVAL: Duration = Duration::from_secs(30);
/// How long a *terminal* entry is retained before the sweeper reclaims it. Only
/// matters for orphans — calls the consumer drained are evicted immediately on
/// their terminal poll. Comfortably larger than the consumer's poll cadence so
/// the sweeper never races a live consumer that is about to read a result.
const RETENTION: Duration = Duration::from_mins(30);

/// In-memory execution record for one enqueued call.
///
/// Lives only on the sg pod that accepted the `EnqueueRemoteCall`, and is lost
/// on pod restart. That is the accepted limitation of the base async path:
/// arbitrary user handlers cannot be checkpointed, so an sg-pod death loses the
/// computation regardless. A reclaiming consumer will re-enqueue (and the
/// function re-runs). Durable reattach across *consumer* restarts is a later
/// phase and lives outside this struct.
struct CallState {
    status: RemoteCallStatus,
    /// Result chunks, written directly by the handler's `BufferEmitter` as it
    /// runs and read by `PollRemoteCall` by cursor. Held behind its own lock
    /// (not the registry map lock) so the hot emit path only contends per-call,
    /// and `status`/`error` can be updated without blocking emits.
    chunks: Arc<Mutex<ChunkBuffer>>,
    /// Populated only when `status == Failed`; surfaced as a `ChalkError`.
    error: Option<ChalkError>,
    /// When the call reached a terminal status. Used only by the orphan sweeper
    /// to decide when an un-drained terminal entry is safe to reclaim.
    completed_at: Option<Instant>,
}

impl CallState {
    fn new() -> Self {
        Self {
            status: RemoteCallStatus::Pending,
            chunks: ChunkBuffer::new().into_shared(),
            error: None,
            completed_at: None,
        }
    }
}

type Registry = Arc<Mutex<HashMap<String, CallState>>>;

fn is_terminal(status: RemoteCallStatus) -> bool {
    matches!(
        status,
        RemoteCallStatus::Completed | RemoteCallStatus::Failed
    )
}

/// Async (enqueue + poll) executor for the scaling-group hop.
///
/// `EnqueueRemoteCall` runs the handler in a detached background task that
/// writes result chunks straight into the call's buffer, and returns
/// immediately; `PollRemoteCall` reads those chunks by cursor. This decouples
/// function execution from any single connection's lifetime, so the path is
/// immune to gateway request/stream timeouts — every RPC here is sub-second
/// regardless of how long the function runs.
///
/// Entries are reclaimed two ways: the terminal poll that delivers a result
/// evicts its own entry (the consumer drains a call exactly once, then persists
/// to Redis and stops polling it), and a background sweeper reclaims orphans —
/// calls that finished but whose consumer died before the terminal poll.
pub struct AsyncRemoteCallServiceImpl {
    python_handler: Arc<PythonHandler>,
    registry: Registry,
    next_id: AtomicU64,
    /// True when the server was started with coalescing enabled. In that mode
    /// `python_handler`'s bridge expects the batched calling convention, which
    /// the per-call dispatch does not satisfy, so async enqueue is refused
    /// rather than silently calling the handler with the wrong shape.
    batching_enabled: bool,
    is_remote_function: bool,
}

impl AsyncRemoteCallServiceImpl {
    pub fn new(
        python_handler: Arc<PythonHandler>,
        batching_enabled: bool,
        is_remote_function: bool,
    ) -> Self {
        let registry: Registry = Arc::new(Mutex::new(HashMap::new()));
        // Runs inside the server's tokio runtime (the service is constructed
        // within `run_server`); reclaims orphaned terminal entries.
        spawn_sweeper(registry.clone());
        Self {
            python_handler,
            registry,
            next_id: AtomicU64::new(1),
            batching_enabled,
            is_remote_function,
        }
    }
}

#[tonic::async_trait]
impl AsyncRemoteCallService for AsyncRemoteCallServiceImpl {
    #[instrument(skip_all)]
    async fn enqueue_remote_call(
        &self,
        request: Request<EnqueueRemoteCallRequest>,
    ) -> Result<Response<EnqueueRemoteCallResponse>, Status> {
        if self.batching_enabled {
            return Err(Status::unimplemented(
                "async enqueue/poll is not supported when request coalescing is enabled",
            ));
        }

        let metadata = extract_metadata(request.metadata());
        let peer = request
            .remote_addr()
            .map(|a| a.to_string())
            .unwrap_or_default();
        let req = request.into_inner();
        let function_name = req.name;

        if self.is_remote_function {
            warn!(
                function_name = %function_name,
                "this enqueue is not fronted by the fnq server (CHALK_REMOTE_FUNCTION is set to true)"
            );
        }

        // Only inline feather bytes are supported today; the object-store
        // variant is reserved for large payloads and not wired up here.
        let ipc_bytes = match req.args.and_then(|a| a.args) {
            Some(remote_call_args::Args::FeatherBytes(b)) => b.to_vec(),
            Some(remote_call_args::Args::StorageObjectId(_)) => {
                return Err(Status::unimplemented(
                    "storage_object_id args are not supported by the scaling-group executor",
                ));
            }
            None => Vec::new(),
        };

        // Pod-scoped id: the registry only knows about calls accepted by this
        // pod, so a monotonic per-process counter is sufficient for uniqueness.
        let call_id = format!("sg-{}", self.next_id.fetch_add(1, Ordering::Relaxed));

        let state = CallState::new();
        // The handler writes chunks into this buffer directly; the registry
        // keeps the same Arc so polls can read them back.
        let buffer = state.chunks.clone();
        self.registry
            .lock()
            .expect("registry mutex poisoned")
            .insert(call_id.clone(), state);

        info!(call_id = %call_id, function_name = %function_name, "enqueued async call");

        let handler = self.python_handler.clone();
        let registry = self.registry.clone();
        let id = call_id.clone();
        tokio::spawn(async move {
            set_status(&registry, &id, RemoteCallStatus::Running);

            // The handler appends each chunk straight into `buffer`; completion
            // is signalled purely by this returning, so there is no channel to
            // drain and nothing that waits on Python object teardown.
            let result = handler
                .call_into_buffer(ipc_bytes, function_name, metadata, peer, buffer)
                .await;

            let mut reg = registry.lock().expect("registry mutex poisoned");
            if let Some(s) = reg.get_mut(&id) {
                s.completed_at = Some(Instant::now());
                match result {
                    Ok(()) => {
                        s.status = RemoteCallStatus::Completed;
                        let n = s.chunks.lock().map(|b| b.len()).unwrap_or(0);
                        info!(call_id = %id, chunks = n, "async call completed");
                    }
                    Err(e) => {
                        s.status = RemoteCallStatus::Failed;
                        s.error = Some(e.chalk_error());
                        error!(
                            call_id = %id,
                            exception.stacktrace = e.details(),
                            "async call failed: {}",
                            e.details()
                        );
                    }
                }
            }
        });

        Ok(Response::new(EnqueueRemoteCallResponse { call_id }))
    }

    #[instrument(skip_all)]
    async fn poll_remote_call(
        &self,
        request: Request<PollRemoteCallRequest>,
    ) -> Result<Response<PollRemoteCallResponse>, Status> {
        let req = request.into_inner();
        let cursor: usize = if req.cursor.is_empty() {
            0
        } else {
            req.cursor
                .parse()
                .map_err(|_| Status::invalid_argument(format!("invalid cursor: {}", req.cursor)))?
        };

        // Read status/error and grab the chunk-buffer handle under the map lock.
        // `status` reaches a terminal value only after the handler returns (all
        // chunks already appended), so seeing `Completed`/`Failed` guarantees
        // the buffer is complete — and this poll delivers it in full. Since the
        // consumer drains a call to terminal exactly once (then persists to
        // Redis and never re-polls this call_id), we evict the entry here. The
        // cloned `chunks` Arc keeps the buffer alive for the read below.
        let (status, error, chunks) = {
            let mut reg = self.registry.lock().expect("registry mutex poisoned");
            let state = reg
                .get(&req.call_id)
                .ok_or_else(|| Status::not_found(format!("unknown call_id: {}", req.call_id)))?;
            let snapshot = (state.status, state.error.clone(), state.chunks.clone());
            if is_terminal(snapshot.0) {
                reg.remove(&req.call_id);
            }
            snapshot
        };

        let buf = chunks.lock().expect("chunk buffer poisoned");
        // Clamp so a stale/over-large cursor returns an empty suffix rather than
        // panicking on the slice.
        let total = buf.len();
        let from = cursor.min(total);
        let results = buf.chunks()[from..].to_vec();
        drop(buf);

        let errors = if status == RemoteCallStatus::Failed {
            vec![error.unwrap_or_else(|| ChalkError {
                message: "remote call failed".to_string(),
                ..Default::default()
            })]
        } else {
            Vec::new()
        };

        debug!(
            call_id = %req.call_id,
            status = ?status,
            from,
            returned = results.len(),
            "poll"
        );

        Ok(Response::new(PollRemoteCallResponse {
            status: status as i32,
            results,
            cursor: total.to_string(),
            errors,
        }))
    }

    async fn purge_queue(
        &self,
        _request: Request<PurgeQueueRequest>,
    ) -> Result<Response<PurgeQueueResponse>, Status> {
        // PurgeQueue operates on the tenant's Redis-backed function queues,
        // which live in the function-queue server — not on an individual
        // scaling-group executor pod.
        Err(Status::unimplemented(
            "PurgeQueue is a function-queue-server operation; not supported on the scaling-group executor",
        ))
    }
}

/// Set the status of an in-flight call, if it still exists in the registry.
fn set_status(registry: &Registry, call_id: &str, status: RemoteCallStatus) {
    if let Ok(mut reg) = registry.lock() {
        if let Some(s) = reg.get_mut(call_id) {
            s.status = status;
        }
    }
}

/// Background task: periodically reclaim *orphaned* terminal entries — calls
/// that finished but whose consumer died before issuing the terminal poll that
/// would normally evict them. Entries the consumer drains are removed on their
/// terminal poll and never reach the sweeper; non-terminal entries (still
/// running) are never reclaimed here.
fn spawn_sweeper(registry: Registry) {
    tokio::spawn(async move {
        let mut ticker = tokio::time::interval(SWEEP_INTERVAL);
        ticker.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
        loop {
            ticker.tick().await;
            let Ok(mut reg) = registry.lock() else {
                continue;
            };
            reg.retain(|_, s| {
                !(is_terminal(s.status) && s.completed_at.is_some_and(|t| t.elapsed() > RETENTION))
            });
        }
    });
}
