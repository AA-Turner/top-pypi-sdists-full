// ClickHouse MySQL-compatibility handler.
//
// ClickHouse exposes a MySQL wire protocol interface on port 9004 by default.
// This handler delegates to MySqlHandler so existing MySQL CLI infrastructure
// works unchanged — the vault record just needs to point at port 9004.

use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    EventBasedHandler, EventCallback, HandlerError, ProtocolHandler, VideoOutput,
};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

use crate::sql::SqlHandler;

/// ClickHouse handler — delegates to SqlHandler (MySQL mode) via MySQL-compat port 9004.
pub struct ClickHouseHandler(SqlHandler);

impl ClickHouseHandler {
    pub fn with_defaults() -> Self {
        Self(SqlHandler::mysql())
    }
}

#[async_trait]
impl ProtocolHandler for ClickHouseHandler {
    fn name(&self) -> &str {
        "clickhouse"
    }

    fn as_event_based(&self) -> Option<&dyn EventBasedHandler> {
        Some(self)
    }

    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        self.0
            .connect(params, to_client, from_client, video_tx, _hooks)
            .await
    }
}

#[async_trait]
impl EventBasedHandler for ClickHouseHandler {
    fn name(&self) -> &str {
        "clickhouse"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
        self.0
            .connect_with_events(params, callback, from_client, video_tx, _hooks)
            .await
    }
}
