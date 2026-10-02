use std::collections::HashMap;
use std::sync::Arc;
#[cfg(target_os = "linux")]
use std::time::Instant;

#[cfg(target_os = "linux")]
use chalk_metrics::metrics::tags::Mode;
#[cfg(target_os = "linux")]
use chalk_metrics::PublishingMetricsPipeline;
use chalk_remote_call_proto::chalk::runtime::v1::remote_call_service_server::RemoteCallService;
use chalk_remote_call_proto::chalk::runtime::v1::{CallFunctionRequest, CallFunctionResponse};
use tokio_stream::wrappers::ReceiverStream;
use tonic::{Request, Response, Status, Streaming};
use tracing::{debug, error, instrument};

use crate::coalesce::{BufferedCall, CoalescingQueue};
use crate::python_bridge::{CallerInput, PythonHandler};

/// Maximum total size of accumulated request bytes (32 MB).
const MAX_REQUEST_SIZE: usize = 32 * 1024 * 1024;

pub struct RemoteCallServiceImpl {
    pub python_handler: Arc<PythonHandler>,
    /// Optional coalescing queue. When `Some`, incoming calls are buffered and
    /// dispatched as a single batched handler invocation.
    pub coalescing_queue: Option<Arc<CoalescingQueue>>,
    // Linux-gated metrics pipeline
    #[cfg(target_os = "linux")]
    pub metrics_pipeline: Option<Arc<PublishingMetricsPipeline>>,
}

#[tonic::async_trait]
impl RemoteCallService for RemoteCallServiceImpl {
    type CallFunctionStream = ReceiverStream<Result<CallFunctionResponse, Status>>;

    #[instrument(skip_all)]
    async fn call_function(
        &self,
        request: Request<Streaming<CallFunctionRequest>>,
    ) -> Result<Response<Self::CallFunctionStream>, Status> {
        // Extract metadata from request
        let metadata = extract_metadata(request.metadata());
        let peer = request
            .remote_addr()
            .map(|a| a.to_string())
            .unwrap_or_default();

        let mut stream = request.into_inner();

        // Accumulate all feather_stream bytes from the request stream
        let mut all_bytes: Vec<u8> = Vec::new();
        let mut function_name = String::new();
        while let Some(req) = stream.message().await? {
            if function_name.is_empty() && !req.name.is_empty() {
                function_name = req.name.clone();
            }
            all_bytes.extend_from_slice(&req.feather_stream);
            if all_bytes.len() > MAX_REQUEST_SIZE {
                return Err(Status::resource_exhausted(format!(
                    "Request exceeds maximum size of {} bytes",
                    MAX_REQUEST_SIZE
                )));
            }
        }

        if all_bytes.is_empty() {
            // No data — return empty stream (matches Python behavior)
            let (_tx, rx) = tokio::sync::mpsc::channel(1);
            return Ok(Response::new(ReceiverStream::new(rx)));
        }

        // Validate Arrow IPC with arrow-rs
        if let Err(e) = validate_arrow_ipc(&all_bytes) {
            return Err(Status::internal(format!(
                "Failed to decode Arrow IPC stream: {e}"
            )));
        }

        let (tx, rx) = tokio::sync::mpsc::channel(32);

        if let Some(queue) = &self.coalescing_queue {
            // Batching path: hand off to the queue and return — the queue
            // will send the response once the coalesced handler call
            // completes.
            queue
                .clone()
                .submit(BufferedCall {
                    input: CallerInput {
                        ipc_bytes: all_bytes,
                        function_name,
                        metadata,
                        peer,
                    },
                    response_tx: tx,
                })
                .await;
            return Ok(Response::new(ReceiverStream::new(rx)));
        }

        // Single-request path.
        let handler = self.python_handler.clone();
        #[cfg(target_os = "linux")]
        let metrics_pipeline = self.metrics_pipeline.clone();
        tokio::spawn(async move {
            #[cfg(target_os = "linux")]
            let started = Instant::now();

            let error_tx = tx.clone();
            match handler
                .call_streaming(all_bytes, function_name.clone(), metadata, peer, tx)
                .await
            {
                Ok(()) => {
                    #[cfg(target_os = "linux")]
                    if let Some(p) = &metrics_pipeline {
                        crate::metrics::record_completed_call(
                            p,
                            &function_name,
                            /* success = */ true,
                            started.elapsed(),
                            Mode::Sync,
                        )
                    }
                }
                Err(e) => {
                    #[cfg(target_os = "linux")]
                    if let Some(p) = &metrics_pipeline {
                        crate::metrics::record_completed_call(
                            p,
                            &function_name,
                            /* success = */ false,
                            started.elapsed(),
                            Mode::Sync,
                        )
                    }
                    if error_tx.is_closed() {
                        // The only reason blocking_send fails is a dropped
                        // receiver — the client went away mid-stream. Not a
                        // handler failure; nothing to send.
                        debug!("client disconnected during streaming response");
                    } else {
                        error!(
                            exception.stacktrace = e.details(),
                            "Python handler error: {}",
                            e.details()
                        );
                        let _ = error_tx.send(Err(Status::unknown(e.to_string()))).await;
                    }
                }
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}

/// Extract user-supplied metadata from gRPC headers into a HashMap.
pub(crate) fn extract_metadata(metadata: &tonic::metadata::MetadataMap) -> HashMap<String, String> {
    let mut map = HashMap::new();
    for kv in metadata.iter() {
        if let tonic::metadata::KeyAndValueRef::Ascii(key, value) = kv {
            if let Ok(v) = value.to_str() {
                map.insert(key.as_str().to_string(), v.to_string());
            }
        }
    }
    map
}

/// Validate that the bytes represent a valid Arrow IPC stream.
fn validate_arrow_ipc(data: &[u8]) -> Result<(), arrow::error::ArrowError> {
    use arrow::ipc::reader::StreamReader;
    use std::io::Cursor;

    let cursor = Cursor::new(data);
    let reader = StreamReader::try_new(cursor, None)?;
    // Read through all batches to validate
    for batch in reader {
        batch?;
    }
    Ok(())
}
