use crate::server;
use dashmap::{DashMap, mapref::entry::Entry};
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
#[pyo3::pyfunction]
#[pyo3(signature = (target_url, port=DEFAULT_PORT))]
pub fn run(target_url: String, port: u16) -> pyo3::prelude::PyResult<()> {
    // Use entry() API for atomic check-and-insert to avoid TOCTOU race condition
    match SERVERS.entry(port) {
        Entry::Occupied(_) => {
            return Err(pyo3::exceptions::PyRuntimeError::new_err(format!(
                "Server is already running on port {}. Call stop() first.",
                port
            )));
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
#[pyo3::pyfunction]
#[pyo3(signature = (port=DEFAULT_PORT))]
pub fn stop(port: u16) -> pyo3::prelude::PyResult<()> {
    if let Some((_, state)) = SERVERS.remove(&port) {
        state.shutdown().map_err(|_| {
            pyo3::exceptions::PyRuntimeError::new_err(format!(
                "Failed to join server thread on port {}",
                port
            ))
        })?;
        Ok(())
    } else {
        Err(pyo3::exceptions::PyRuntimeError::new_err(format!(
            "No server is currently running on port {}.",
            port
        )))
    }
}
