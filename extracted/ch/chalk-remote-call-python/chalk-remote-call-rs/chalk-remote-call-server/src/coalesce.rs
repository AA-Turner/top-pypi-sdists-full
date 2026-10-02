//! Request coalescing queue.
//!
//! Buffers incoming gRPC calls and flushes them as a single coalesced
//! invocation when either the queue hits `max_size` or `max_duration` elapses
//! since the first buffered item. The handler receives all buffered callers'
//! inputs in one Python call, amortising GIL acquisition across the batch.

use std::sync::Arc;
use std::time::Duration;

use tokio::sync::{mpsc, Mutex};
use tokio::task::JoinHandle;
use tonic::Status;
use tracing::error;

#[cfg(target_os = "linux")]
use chalk_metrics::PublishingMetricsPipeline;
use chalk_remote_call_proto::chalk::runtime::v1::CallFunctionResponse;

use crate::python_bridge::{CallerInput, PythonHandler};

/// One buffered caller: the bridge-side `CallerInput` plus its response channel.
pub struct BufferedCall {
    pub input: CallerInput,
    pub response_tx: mpsc::Sender<Result<CallFunctionResponse, Status>>,
}

struct QueueState {
    items: Vec<BufferedCall>,
    /// The in-flight flush-timer task. Aborted when the queue is flushed by
    /// size trigger or when already empty at timer fire.
    flush_task: Option<JoinHandle<()>>,
}

pub struct CoalescingQueue {
    handler: Arc<PythonHandler>,
    max_size: usize,
    max_duration: Duration,
    state: Mutex<QueueState>,
    #[cfg(target_os = "linux")]
    pipeline: Option<Arc<PublishingMetricsPipeline>>,
}

impl CoalescingQueue {
    pub fn new(
        handler: Arc<PythonHandler>,
        max_size: usize,
        max_duration_ms: u64,
        #[cfg(target_os = "linux")] pipeline: Option<Arc<PublishingMetricsPipeline>>,
    ) -> Arc<Self> {
        Arc::new(Self {
            handler,
            max_size,
            max_duration: Duration::from_millis(max_duration_ms),
            state: Mutex::new(QueueState {
                items: Vec::new(),
                flush_task: None,
            }),
            #[cfg(target_os = "linux")]
            pipeline,
        })
    }

    /// Enqueue a call. Flushes immediately if the queue hits `max_size`.
    pub async fn submit(self: Arc<Self>, call: BufferedCall) {
        let should_flush = {
            let mut s = self.state.lock().await;
            let was_empty = s.items.is_empty();
            s.items.push(call);
            let reached_max = s.items.len() >= self.max_size;

            if was_empty && !reached_max {
                // First item — arm the duration timer.
                let me = Arc::clone(&self);
                s.flush_task = Some(tokio::spawn(async move {
                    tokio::time::sleep(me.max_duration).await;
                    me.flush().await;
                }));
            }
            reached_max
        };
        if should_flush {
            self.flush().await;
        }
    }

    /// Drain the queue and dispatch a coalesced call. Cancels any pending
    /// flush timer. No-op if the queue is empty.
    async fn flush(self: Arc<Self>) {
        let items = {
            let mut s = self.state.lock().await;
            if let Some(h) = s.flush_task.take() {
                h.abort();
            }
            std::mem::take(&mut s.items)
        };
        if items.is_empty() {
            return;
        }

        // Dispatch off the queue's critical section — don't block further
        // submissions while Python runs.
        let handler = Arc::clone(&self.handler);
        #[cfg(target_os = "linux")]
        let pipeline = self.pipeline.clone();
        tokio::spawn(async move {
            Self::dispatch(
                handler,
                items,
                #[cfg(target_os = "linux")]
                pipeline,
            )
            .await;
        });
    }

    async fn dispatch(
        handler: Arc<PythonHandler>,
        items: Vec<BufferedCall>,
        #[cfg(target_os = "linux")] pipeline: Option<Arc<PublishingMetricsPipeline>>,
    ) {
        // Split each BufferedCall into its input (for the bridge) and its
        // response channel (for routing the reply back).
        let n = items.len();
        let mut callers: Vec<CallerInput> = Vec::with_capacity(n);
        let mut response_txs = Vec::with_capacity(n);
        #[cfg(target_os = "linux")]
        let function_name = items[0].input.function_name.clone();
        #[cfg(target_os = "linux")]
        let started = std::time::Instant::now();
        for item in items {
            callers.push(item.input);
            response_txs.push(item.response_tx);
        }

        match handler.call_coalesced(callers).await {
            Ok(per_caller_bytes) => {
                if per_caller_bytes.len() != n {
                    // Python side violated contract — report to all callers.
                    let msg = format!(
                        "Coalesced handler returned {} responses for {} callers",
                        per_caller_bytes.len(),
                        n
                    );
                    error!("{}", msg);
                    #[cfg(target_os = "linux")]
                    if let Some(p) = &pipeline {
                        crate::metrics::record_completed_call(
                            p,
                            &function_name,
                            /* success = */ false,
                            started.elapsed(),
                            chalk_metrics::metrics::tags::Mode::Sync,
                        );
                    }
                    for tx in &response_txs {
                        let _ = tx.send(Err(Status::unknown(msg.clone()))).await;
                    }
                    return;
                }
                #[cfg(target_os = "linux")]
                if let Some(p) = &pipeline {
                    crate::metrics::record_completed_call(
                        p,
                        &function_name,
                        /* success = */ true,
                        started.elapsed(),
                        chalk_metrics::metrics::tags::Mode::Sync,
                    );
                }
                for (tx, chunk) in response_txs.into_iter().zip(per_caller_bytes) {
                    let msg = CallFunctionResponse {
                        feather_stream: chunk.into(),
                    };
                    let _ = tx.send(Ok(msg)).await;
                }
            }
            Err(e) => {
                error!(
                    exception.stacktrace = e.details(),
                    "Coalesced handler error: {}",
                    e.details()
                );
                // IPC decode errors are already caught by the service's
                // pre-validation; anything reaching here is a handler error.
                #[cfg(target_os = "linux")]
                if let Some(p) = &pipeline {
                    crate::metrics::record_completed_call(
                        p,
                        &function_name,
                        /* success = */ false,
                        started.elapsed(),
                        chalk_metrics::metrics::tags::Mode::Sync,
                    );
                }
                let status = Status::unknown(e.to_string());
                for tx in response_txs {
                    let _ = tx.send(Err(status.clone())).await;
                }
            }
        }
    }
}
