// Session lifecycle helpers shared across all protocol handlers.
//
// Provides consistent ready, name, disconnect, and bell instructions
// so every handler uses the same wire format for session startup/shutdown.

use bytes::Bytes;
use guacr_protocol::{format_bell_audio, format_instruction};
use log::{debug, warn};
use tokio::sync::mpsc;

use crate::{HandlerError, MultiFormatRecorder, RecordingDirection, Result};

/// Send a `ready` instruction to the client.
///
/// This signals that the backend is connected and ready to process instructions.
/// Propagates errors because if the client is gone at startup, the session should abort.
pub async fn send_ready(to_client: &mpsc::Sender<Bytes>, connection_id: &str) -> Result<()> {
    let instr = format_instruction("ready", &[connection_id]);
    debug!("Session: Sending ready instruction: {}", instr);
    to_client
        .send(Bytes::from(instr))
        .await
        .map_err(|e| HandlerError::ChannelError(e.to_string()))
}

/// Send a `name` instruction to the client.
///
/// Tells the client the display name for this connection (e.g., "SSH", "RDP", "VNC").
/// Propagates errors.
pub async fn send_name(to_client: &mpsc::Sender<Bytes>, protocol_name: &str) -> Result<()> {
    let instr = format_instruction("name", &[protocol_name]);
    to_client
        .send(Bytes::from(instr))
        .await
        .map_err(|e| HandlerError::ChannelError(e.to_string()))
}

/// Send a `disconnect` instruction to the client.
///
/// Best-effort: swallows send errors since the client may already be gone
/// when we're shutting down.
pub async fn send_disconnect(to_client: &mpsc::Sender<Bytes>) {
    let instr = format_instruction("disconnect", &[]);
    if to_client.send(Bytes::from(instr)).await.is_err() {
        debug!("Session: Failed to send disconnect (client may have closed)");
    }
}

/// Send a bell/beep audio notification to the client.
///
/// Sends the standard Guacamole audio sequence: audio + blob + end instructions.
/// Propagates errors.
pub async fn send_bell(to_client: &mpsc::Sender<Bytes>, stream_id: u32) -> Result<()> {
    let bell_instrs = format_bell_audio(stream_id);
    for instr in bell_instrs {
        to_client
            .send(Bytes::from(instr))
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
    }
    Ok(())
}

/// Send a Guacamole instruction to the client and record it (if recording is enabled).
///
/// This is the shared implementation used by all protocol handlers (SSH, Telnet,
/// Serial, Database, RDP, VNC). Records the instruction as server-to-client
/// direction before sending.
pub async fn send_and_record(
    to_client: &mpsc::Sender<Bytes>,
    recorder: &mut Option<MultiFormatRecorder>,
    instruction: Bytes,
) -> std::result::Result<(), String> {
    if let Some(ref mut rec) = recorder {
        if let Err(e) = rec.record_instruction(RecordingDirection::ServerToClient, &instruction) {
            warn!("Failed to record server instruction: {}", e);
        }
    }
    to_client
        .send(instruction)
        .await
        .map_err(|e| format!("Send failed: {}", e))
}

/// Record a client-to-server instruction (if recording is enabled).
///
/// Shared implementation used by all protocol handlers. Only records; does not send.
pub fn record_client_input(recorder: &mut Option<MultiFormatRecorder>, instruction: &Bytes) {
    if let Some(ref mut rec) = recorder {
        if let Err(e) = rec.record_instruction(RecordingDirection::ClientToServer, instruction) {
            warn!("Failed to record client input: {}", e);
        }
    }
}
