use crate::interface::DEFAULT_TIMEOUT;
use crate::proxy;
use crate::spans::SpanProcessor;
use crate::state;

use http_body_util::combinators::BoxBody;
use hyper::{body::Bytes, server::conn::http1, service::service_fn};
use hyper_util::{client::legacy::Client, rt::TokioIo};
use std::error::Error as StdError;
use std::net::SocketAddr;
use std::sync::{Arc, Mutex};
use tokio::{net::TcpListener, sync::oneshot, task::JoinSet};

pub async fn start_server(
    target_url: String,
    port: u16,
    mut shutdown_rx: oneshot::Receiver<u64>,
) -> Result<(), Box<dyn std::error::Error>> {
    // Install default crypto provider for rustls
    let _ = rustls::crypto::ring::default_provider().install_default();

    let addr = SocketAddr::from(([127, 0, 0, 1], port));
    let listener = TcpListener::bind(addr).await?;

    // Build HTTPS-capable client
    let https_connector = hyper_rustls::HttpsConnectorBuilder::new()
        .with_webpki_roots()
        .https_or_http()
        .enable_http1()
        .enable_http2()
        .build();

    let client: Client<_, BoxBody<Bytes, hyper::Error>> =
        Client::builder(hyper_util::rt::TokioExecutor::new()).build(https_connector);

    let state = state::new_state();
    let span_processor = Arc::new(SpanProcessor::new());
    let background_tasks = Arc::new(Mutex::new(JoinSet::new()));

    // Track active connections for graceful shutdown
    let mut connection_tasks = JoinSet::new();

    let shutdown_timeout_secs = loop {
        tokio::select! {
            timeout_result = &mut shutdown_rx => {
                // Receive the timeout value from the shutdown signal
                break timeout_result.unwrap_or(DEFAULT_TIMEOUT);
            }
            accept_result = listener.accept() => {
                let (stream, _) = accept_result?;
                let client = client.clone();
                let target_url = target_url.clone();
                let state = state.clone();
                let span_processor = span_processor.clone();
                let background_tasks = background_tasks.clone();

                connection_tasks.spawn(async move {
                    // Handle HTTP connection
                    let io = TokioIo::new(stream);
                    let result = http1::Builder::new()
                        .half_close(true) // Allow half-closed connections for streaming
                        .preserve_header_case(true)
                        .serve_connection(
                            io,
                            service_fn(move |req| {
                                proxy::handle(req, client.clone(), target_url.clone(), state.clone(), span_processor.clone(), background_tasks.clone())
                            }),
                        )
                        .await;

                    if let Err(err) = result {
                        // Filter out expected errors during streaming
                        let is_broken_pipe = err.source()
                            .and_then(|e| e.downcast_ref::<std::io::Error>())
                            .map(|e| e.kind() == std::io::ErrorKind::BrokenPipe)
                            .unwrap_or(false);

                        // Only log unexpected errors
                        if !err.is_incomplete_message() && !err.is_closed() && !is_broken_pipe {
                            eprintln!("Error serving connection: {:?}", err);
                        }
                    }
                });
            }
        }
    };

    // Graceful shutdown with timeout
    // Give active connections and background tasks time to complete naturally
    // Use half of the stop timeout to ensure we can clean up before the outer timeout
    let shutdown_timeout = tokio::time::Duration::from_secs(shutdown_timeout_secs / 2);
    let shutdown_start = tokio::time::Instant::now();

    // Wait for active connections with timeout
    let active_count = connection_tasks.len();
    if active_count > 0 {
        loop {
            let remaining = shutdown_timeout.saturating_sub(shutdown_start.elapsed());
            if remaining.is_zero() {
                // Timeout reached - abort remaining connections
                let aborted = connection_tasks.len();
                if aborted > 0 {
                    connection_tasks.abort_all();
                }
                break;
            }

            match tokio::time::timeout(remaining, connection_tasks.join_next()).await {
                Ok(Some(result)) => {
                    if let Err(e) = result {
                        // Only log if not aborted
                        if !e.is_cancelled() {
                            eprintln!("Connection task panicked: {:?}", e);
                        }
                    }
                }
                Ok(None) => break, // All done
                Err(_) => {
                    // Timeout - abort remaining
                    let aborted = connection_tasks.len();
                    if aborted > 0 {
                        connection_tasks.abort_all();
                    }
                    break;
                }
            }
        }
    }

    // Wait for background tasks (trace sending) with remaining timeout
    let background_count = match background_tasks.lock() {
        Ok(join_set) => join_set.len(),
        Err(e) => {
            eprintln!("Failed to lock background tasks: {}", e);
            0
        }
    };
    if background_count > 0 {
        loop {
            let remaining = shutdown_timeout.saturating_sub(shutdown_start.elapsed());
            if remaining.is_zero() {
                // Timeout reached - abort remaining background tasks
                if let Ok(mut join_set) = background_tasks.lock() {
                    let aborted = join_set.len();
                    if aborted > 0 {
                        join_set.abort_all();
                    }
                }
                break;
            }

            let result = match background_tasks.lock() {
                Ok(mut join_set) => {
                    match tokio::time::timeout(remaining, join_set.join_next()).await {
                        Ok(result) => result,
                        Err(_) => {
                            // Timeout - abort remaining
                            let aborted = join_set.len();
                            if aborted > 0 {
                                join_set.abort_all();
                            }
                            break;
                        }
                    }
                }
                Err(e) => {
                    eprintln!("Failed to lock background tasks: {}", e);
                    None
                }
            };

            if let Some(result) = result {
                if let Err(e) = result {
                    // Only log if not aborted
                    if !e.is_cancelled() {
                        eprintln!("Background task panicked: {:?}", e);
                    }
                }
            } else {
                break;
            }
        }
    }

    Ok(())
}
