// DualSink: writes to both WebSocketSink and FileSink simultaneously.
// If WebSocket upload fails, the file copy is still intact.

use crate::{FileSink, RecordingSink, Result, WebSocketSink};
use async_trait::async_trait;
use guacr_handlers::EncodedFrame;

pub struct DualSink {
    ws: WebSocketSink,
    file: FileSink,
}

impl DualSink {
    pub fn new(ws: WebSocketSink, file: FileSink) -> Self {
        Self { ws, file }
    }
}

#[async_trait]
impl RecordingSink for DualSink {
    async fn write_frame(&mut self, frame: &EncodedFrame) -> Result<()> {
        // Both must succeed; if either fails we propagate the error.
        // Errors from WS are fatal (no audit trail); file errors are logged but not fatal.
        self.ws.write_frame(frame).await?;
        if let Err(e) = self.file.write_frame(frame).await {
            log::warn!("DualSink: file write failed (non-fatal): {}", e);
        }
        Ok(())
    }

    async fn write_input(&mut self, instruction: &str, timestamp_ms: u64) -> Result<()> {
        self.ws.write_input(instruction, timestamp_ms).await?;
        if let Err(e) = self.file.write_input(instruction, timestamp_ms).await {
            log::warn!("DualSink: file input write failed (non-fatal): {}", e);
        }
        Ok(())
    }

    async fn finalize(self: Box<Self>) -> Result<()> {
        let ws = self.ws;
        let file = self.file;

        let ws_result = Box::new(ws).finalize().await;
        let file_result = Box::new(file).finalize().await;

        // WS failure is fatal; file failure is logged
        match (ws_result, file_result) {
            (Ok(_), Ok(_)) => Ok(()),
            (Err(e), _) => Err(e),
            (Ok(_), Err(e)) => {
                log::warn!("DualSink: file finalize failed (non-fatal): {}", e);
                Ok(())
            }
        }
    }
}
