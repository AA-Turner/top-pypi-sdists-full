use crate::server;

use dashmap::{DashMap, mapref::entry::Entry};
use std::{sync::LazyLock, thread};
use tokio::sync::oneshot;

pub const DEFAULT_TIMEOUT: u64 = 4;
pub const DEFAULT_PORT: u16 = 45667;

static SERVERS: LazyLock<DashMap<u16, ServerState>> = LazyLock::new(DashMap::new);

struct ServerState {
    thread_handle: Option<thread::JoinHandle<()>>,
    shutdown_tx: Option<oneshot::Sender<u64>>,
}

impl ServerState {
    pub fn new(thread_handle: thread::JoinHandle<()>, shutdown_tx: oneshot::Sender<u64>) -> Self {
        Self {
            thread_handle: Some(thread_handle),
            shutdown_tx: Some(shutdown_tx),
        }
    }

    pub fn shutdown(&mut self, timeout_secs: u64) -> Result<(), String> {
        // Send shutdown signal with timeout value
        if let Some(tx) = self.shutdown_tx.take() {
            let _ = tx.send(timeout_secs);
        } else {
            return Err("Server already shutting down or shut down".to_string());
        }

        // Take ownership of the thread handle
        let handle = self
            .thread_handle
            .take()
            .ok_or("Server thread handle already consumed".to_string())?;

        handle
            .join()
            .map_err(|_| "Failed to join server thread".to_string())?;

        Ok(())
    }

    pub fn shutdown_with_timeout(&mut self, timeout_secs: u64) -> Result<(), String> {
        // Send shutdown signal with timeout value
        if let Some(tx) = self.shutdown_tx.take() {
            let _ = tx.send(timeout_secs);
        }
        // If tx is None, the shutdown signal has already been sent, that's ok.

        if self.thread_handle.is_none() {
            return Err("Server thread handle already consumed".to_string());
        }

        // Wait for the join with timeout
        let timeout = std::time::Duration::from_secs(timeout_secs);
        let start = std::time::Instant::now();

        loop {
            if self
                .thread_handle
                .as_ref()
                .is_some_and(|handle| handle.is_finished())
            {
                // Only take the handle when we know it's finished, otherwise we risk blocking forever.
                let handle = self.thread_handle.take().unwrap();
                return handle
                    .join()
                    .map_err(|_| "Server thread panicked during shutdown".to_string());
            }

            if start.elapsed() >= timeout {
                return Err(format!(
                    "Server shutdown timed out after {timeout_secs} seconds. Server thread may still be running.",
                ));
            }
            thread::sleep(std::time::Duration::from_millis(50));
        }
    }
}

pub fn run(target_url: String, port: u16) -> Result<(), String> {
    // Use entry() API for atomic check-and-insert to avoid TOCTOU race condition
    match SERVERS.entry(port) {
        Entry::Occupied(_) => {
            return Err(format!(
                "Server is already running on port {port}. Call stop() first.",
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

            entry.insert(ServerState::new(thread_handle, shutdown_tx));

            Ok(())
        }
    }
}

#[deprecated(since = "0.1.12", note = "Use stop_with_timeout instead")]
pub fn stop(port: u16) -> Result<(), String> {
    match SERVERS.entry(port) {
        Entry::Occupied(mut entry) => {
            let result = entry.get_mut().shutdown(DEFAULT_TIMEOUT);
            // Only remove from map if shutdown succeeded
            if result.is_ok() {
                entry.remove();
            }
            result.map_err(|_| format!("Failed to join server thread on port {port}"))
        }
        Entry::Vacant(_) => Err(format!("No server is currently running on port {port}.")),
    }
}

pub fn stop_with_timeout(port: u16, timeout_secs: u64) -> Result<(), String> {
    match SERVERS.entry(port) {
        Entry::Occupied(mut entry) => {
            let result = entry.get_mut().shutdown_with_timeout(timeout_secs);
            // Only remove from map if shutdown succeeded
            if result.is_ok() {
                entry.remove();
            }
            result.map_err(|e| format!("Failed to join server thread on port {port}: {e}"))
        }
        Entry::Vacant(_) => Err(format!("No server is currently running on port {port}.")),
    }
}
