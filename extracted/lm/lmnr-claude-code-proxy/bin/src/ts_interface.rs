use crate::server;
use dashmap::{mapref::entry::Entry, DashMap};
use std::{sync::LazyLock, thread};
use tokio::sync::oneshot;

// Global state to track the running server
struct ServerState {
    _thread_handle: thread::JoinHandle<()>,
    shutdown_tx: oneshot::Sender<()>,
}

impl ServerState {
    fn shutdown(self) -> thread::Result<()> {
        let _ = self.shutdown_tx.send(());
        self._thread_handle.join()?;
        Ok(())
    }
}

const DEFAULT_PORT: u16 = 45667;
static SERVERS: LazyLock<DashMap<u16, ServerState>> = LazyLock::new(DashMap::new);

/// Run the proxy server in a background thread
#[napi_derive::napi]
pub fn run(target_url: String, port: Option<u16>) -> napi::Result<()> {
    let port = port.unwrap_or(DEFAULT_PORT);

    // Use entry() API for atomic check-and-insert to avoid TOCTOU race condition
    match SERVERS.entry(port) {
        Entry::Occupied(_) => {
            return Err(napi::Error::new(
                napi::Status::Cancelled,
                format!("Server is already running on port {}. Call stop() first.", port),
            ));
        }
        Entry::Vacant(entry) => {
            let (shutdown_tx, shutdown_rx) = oneshot::channel();

            let thread_handle = thread::spawn(move || {
                let rt = tokio::runtime::Builder::new_current_thread()
                    .enable_all()
                    .build()
                    .expect("Failed to create Tokio runtime");

                rt.block_on(async {
                    if let Err(e) = server::start_server(target_url, port, shutdown_rx).await {
                        eprintln!("Server error: {}", e);
                    }
                });
            });

            entry.insert(ServerState {
                _thread_handle: thread_handle,
                shutdown_tx,
            });

            Ok(())
        }
    }
}

/// Stop the proxy server on a specific port
#[napi_derive::napi]
pub fn stop(port: Option<u16>) -> napi::Result<()> {
    let port = port.unwrap_or(DEFAULT_PORT);

    if let Some((_, state)) = SERVERS.remove(&port) {
        state.shutdown().map_err(|_| {
            napi::Error::new(
                napi::Status::Cancelled,
                format!("Failed to join server thread on port {}", port),
            )
        })?;
        Ok(())
    } else {
        Err(napi::Error::new(
            napi::Status::Cancelled,
            format!("No server is currently running on port {}.", port),
        ))
    }
}
