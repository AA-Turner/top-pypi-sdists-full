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
    mut shutdown_rx: oneshot::Receiver<()>,
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

    loop {
        tokio::select! {
            _ = &mut shutdown_rx => {
                break;
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
    }

    // Wait for all active connections to complete
    let active_count = connection_tasks.len();
    if active_count > 0 {
        while let Some(result) = connection_tasks.join_next().await {
            if let Err(e) = result {
                eprintln!("Connection task panicked: {:?}", e);
            }
        }
    }

    // Wait for all background tasks (trace sending) to complete
    let background_count = match background_tasks.lock() {
        Ok(join_set) => join_set.len(),
        Err(e) => {
            eprintln!("Failed to lock background tasks: {}", e);
            0
        }
    };
    if background_count > 0 {
        loop {
            let result = match background_tasks.lock() {
                Ok(mut join_set) => join_set.join_next().await,
                Err(e) => {
                    eprintln!("Failed to lock background tasks: {}", e);
                    None
                }
            };
            if let Some(result) = result {
                if let Err(e) = result {
                    eprintln!("Background task panicked: {:?}", e);
                }
            } else {
                break;
            }
        }
    }

    Ok(())
}
