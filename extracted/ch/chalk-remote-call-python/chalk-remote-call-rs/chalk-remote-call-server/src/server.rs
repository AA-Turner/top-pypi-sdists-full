use std::net::SocketAddr;
use std::sync::Arc;

#[cfg(target_os = "linux")]
use crate::metrics::CallMetrics;
use chalk_remote_call_proto::chalk::runtime::v1::async_remote_call_service_server::AsyncRemoteCallServiceServer;
use chalk_remote_call_proto::chalk::runtime::v1::remote_call_service_server::RemoteCallServiceServer;
use chalk_remote_call_proto::chalk::runtime::v1::FILE_DESCRIPTOR_SET;
use tonic::transport::Server;
use tracing::info;

use crate::async_service::AsyncRemoteCallServiceImpl;
use crate::coalesce::CoalescingQueue;
use crate::python_bridge::PythonHandler;
use crate::service::RemoteCallServiceImpl;
use crate::ServingState;

const MAX_MESSAGE_SIZE: usize = 32 * 1024 * 1024; // 32 MB

const ENV_REMOTE_FUNCTION: &str = "CHALK_REMOTE_FUNCTION";

pub async fn run_server(
    host: String,
    port: u16,
    python_handler: Arc<PythonHandler>,
    coalescing_queue: Option<Arc<CoalescingQueue>>,
    serving_state: Option<Arc<ServingState>>,
    #[cfg(target_os = "linux")] metrics: Option<Arc<CallMetrics>>,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    // Parse host — ensure IPv6 addresses are bracketed for SocketAddr parsing
    let addr_str = if host.contains(':') && !host.starts_with('[') {
        // Bare IPv6 like :: or ::1 — add brackets
        format!("[{host}]:{port}")
    } else {
        // Already bracketed IPv6 like [::] or IPv4 like 0.0.0.0
        format!("{host}:{port}")
    };

    let addr: SocketAddr = addr_str
        .parse()
        .map_err(|e| format!("Invalid bind address '{addr_str}': {e}"))?;

    // Health service
    let (mut health_reporter, health_service) = tonic_health::server::health_reporter();
    // Subscribe before reading state so a Python update cannot be lost between
    // publishing initial health and starting the watcher.
    let health_changes = serving_state.as_ref().map(|state| state.subscribe());
    let initially_serving = serving_state
        .as_ref()
        .is_none_or(|state| state.is_serving());
    let initial_status = if initially_serving {
        tonic_health::ServingStatus::Serving
    } else {
        tonic_health::ServingStatus::NotServing
    };
    health_reporter
        .set_service_status("chalk.runtime.v1.RemoteCallService", initial_status)
        .await;
    health_reporter.set_service_status("", initial_status).await;

    let health_updates = serving_state
        .as_ref()
        .zip(health_changes)
        .map(|(state, mut changes)| {
            let state = state.clone();
            tokio::spawn(async move {
                let mut reported_serving = initially_serving;
                loop {
                    if state.is_serving() {
                        if let Some(deadline) = state.deadline() {
                            tokio::select! {
                                result = changes.changed() => {
                                    if result.is_err() { break; }
                                    changes.borrow_and_update();
                                }
                                _ = tokio::time::sleep_until(deadline) => {}
                            }
                        } else if changes.changed().await.is_err() {
                            break;
                        } else {
                            changes.borrow_and_update();
                        }
                    } else if changes.changed().await.is_err() {
                        break;
                    } else {
                        changes.borrow_and_update();
                    }

                    let serving = state.is_serving();
                    if serving == reported_serving {
                        continue;
                    }
                    let status = if serving {
                        tonic_health::ServingStatus::Serving
                    } else {
                        tonic_health::ServingStatus::NotServing
                    };
                    health_reporter
                        .set_service_status("chalk.runtime.v1.RemoteCallService", status)
                        .await;
                    health_reporter.set_service_status("", status).await;
                    reported_serving = serving;
                }
            })
        });

    // Reflection service
    let reflection_service = tonic_reflection::server::Builder::configure()
        .register_encoded_file_descriptor_set(FILE_DESCRIPTOR_SET)
        .build_v1()?;

    // Also serve v1alpha for backwards compatibility
    let reflection_service_v1alpha = tonic_reflection::server::Builder::configure()
        .register_encoded_file_descriptor_set(FILE_DESCRIPTOR_SET)
        .build_v1alpha()?;

    // Async (enqueue + poll) executor shares the same Python handler. Read the
    // coalescing flag before `coalescing_queue` is moved into the streaming
    // service below; the async path refuses enqueue when batching is on.
    let batching_enabled = coalescing_queue.is_some();
    // Checks if remote function env var is set or not
    let is_remote_function: bool = std::env::var(ENV_REMOTE_FUNCTION)
        .is_ok_and(|v| v.eq_ignore_ascii_case("true") || v == "1");
    let async_svc = AsyncRemoteCallServiceImpl::new(
        python_handler.clone(),
        batching_enabled,
        is_remote_function,
        serving_state.clone(),
    );

    #[cfg(target_os = "linux")]
    let (shutdown_tx, shutdown_rx) = tokio::sync::watch::channel(false);

    // Self-consume the Redis fn queue when this pod was provisioned with a
    // Redis URL (gRPC-only otherwise). The self-consumer shares the gRPC
    // server's `coalescing_queue`: when batching is on, self-consumed work and
    // inbound gRPC calls feed the same queue so they batch together against the
    // single batch-size/duration the user configured. When batching is off the
    // queue is `None` and the self-consumer dispatches per-call (streaming).

    #[cfg(target_os = "linux")]
    let consumer_task = crate::self_consumer::SelfConsumerConfig::from_env().and_then(|cfg| {
        let drain_on_shutdown = cfg.consumer_endpoint.is_some()
            || cfg.queue_protocol == chalk_queue::QueueProtocol::StreamV1;
        // Share the synchronous gRPC server's function-call metrics pipeline.
        let consumer_handler = python_handler.clone();
        let consumer_metrics = metrics.clone();
        let consumer_coalescing = coalescing_queue.clone();
        let task = tokio::spawn(async move {
            if let Err(e) = crate::self_consumer::run(
                cfg,
                consumer_handler,
                consumer_metrics,
                consumer_coalescing,
                shutdown_rx,
            )
            .await
            {
                tracing::error!(error = %e, "fnq self-consumer failed to start");
            }
        });
        drain_on_shutdown.then_some(task)
    });

    // Main service
    let svc = RemoteCallServiceImpl {
        python_handler,
        coalescing_queue,
        serving_state,
        #[cfg(target_os = "linux")]
        metrics,
    };

    info!("Server starting on {}", addr);

    let shutdown = async {
        shutdown_signal().await;
        #[cfg(target_os = "linux")]
        shutdown_tx.send_replace(true);
    };
    let result = Server::builder()
        .add_service(health_service)
        .add_service(reflection_service)
        .add_service(reflection_service_v1alpha)
        .add_service(
            RemoteCallServiceServer::new(svc)
                .max_decoding_message_size(MAX_MESSAGE_SIZE)
                .max_encoding_message_size(MAX_MESSAGE_SIZE),
        )
        .add_service(
            AsyncRemoteCallServiceServer::new(async_svc)
                .max_decoding_message_size(MAX_MESSAGE_SIZE)
                .max_encoding_message_size(MAX_MESSAGE_SIZE),
        )
        .serve_with_shutdown(addr, shutdown)
        .await;

    #[cfg(target_os = "linux")]
    {
        // Queue workers live outside tonic's request tasks. Keep the runtime
        // and lease renewals alive until their results have been persisted.
        shutdown_tx.send_replace(true);
        if let Some(task) = consumer_task {
            if let Err(error) = task.await {
                tracing::error!(%error, "fnq self-consumer task failed during shutdown");
            }
        }
    }
    result?;

    if let Some(task) = health_updates {
        task.abort();
    }

    info!("Server shut down");
    Ok(())
}

async fn shutdown_signal() {
    let ctrl_c = tokio::signal::ctrl_c();

    #[cfg(unix)]
    {
        use tokio::signal::unix::{signal, SignalKind};
        let mut sigterm =
            signal(SignalKind::terminate()).expect("failed to install SIGTERM handler");

        tokio::select! {
            _ = ctrl_c => {
                info!("Received SIGINT, shutting down...");
            }
            _ = sigterm.recv() => {
                info!("Received SIGTERM, shutting down...");
            }
        }
    }

    #[cfg(not(unix))]
    {
        ctrl_c.await.ok();
        info!("Received Ctrl+C, shutting down...");
    }
}
