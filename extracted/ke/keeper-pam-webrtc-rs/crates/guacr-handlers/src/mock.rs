use async_trait::async_trait;
use bytes::Bytes;
use std::collections::HashMap;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tokio::sync::mpsc;

use crate::error::Result;
use crate::handler::{HandlerStats, HealthStatus, ProtocolHandler};
use crate::video::VideoOutput;

/// Mock protocol handler for testing
///
/// Useful for testing the handler registry and integration points without
/// needing actual protocol implementations.
pub struct MockProtocolHandler {
    name: String,
    connect_count: Arc<AtomicU64>,
    disconnect_count: Arc<AtomicU64>,
    health_status: Arc<parking_lot::RwLock<HealthStatus>>,
}

impl MockProtocolHandler {
    /// Create a new mock handler with the given protocol name
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            connect_count: Arc::new(AtomicU64::new(0)),
            disconnect_count: Arc::new(AtomicU64::new(0)),
            health_status: Arc::new(parking_lot::RwLock::new(HealthStatus::Healthy)),
        }
    }

    /// Get the number of times connect was called
    pub fn connect_count(&self) -> u64 {
        self.connect_count.load(Ordering::SeqCst)
    }

    /// Get the number of times disconnect was called
    pub fn disconnect_count(&self) -> u64 {
        self.disconnect_count.load(Ordering::SeqCst)
    }

    /// Set the health status this mock will report
    pub fn set_health(&self, status: HealthStatus) {
        *self.health_status.write() = status;
    }
}

#[async_trait]
impl ProtocolHandler for MockProtocolHandler {
    fn name(&self) -> &str {
        &self.name
    }

    async fn connect(
        &self,
        _params: HashMap<String, String>,
        _to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: crate::hooks::SessionHooks,
    ) -> Result<()> {
        self.connect_count.fetch_add(1, Ordering::SeqCst);

        // Simply consume messages until channel closes
        while from_client.recv().await.is_some() {
            // Echo or ignore messages
        }

        Ok(())
    }

    async fn disconnect(&self) -> Result<()> {
        self.disconnect_count.fetch_add(1, Ordering::SeqCst);
        Ok(())
    }

    async fn health_check(&self) -> Result<HealthStatus> {
        Ok(self.health_status.read().clone())
    }

    async fn stats(&self) -> Result<HandlerStats> {
        Ok(HandlerStats {
            active_connections: 0,
            total_connections: self.connect_count.load(Ordering::SeqCst),
            bytes_sent: 0,
            bytes_received: 0,
            errors: 0,
        })
    }
}
