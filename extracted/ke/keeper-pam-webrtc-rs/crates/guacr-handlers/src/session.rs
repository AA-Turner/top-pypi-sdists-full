// Session lifecycle helpers shared across all protocol handlers.
//
// Provides consistent ready, name, disconnect, and bell instructions
// so every handler uses the same wire format for session startup/shutdown.

use bytes::Bytes;
use guacr_protocol::{format_bell_audio, format_instruction};
use log::{debug, warn};
use tokio::sync::mpsc;

use crate::session_sharing::ViewerActor;
use crate::{HandlerError, MultiFormatRecorder, RecordingDirection, RecordingError, Result};

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

/// Send a non-fatal `msg` instruction to the client.
///
/// The counterpart to [`crate::send_error_best_effort`] for things the user should see but
/// which must not end the session: `error` is the only other server-to-client text
/// instruction and it closes the connection.
///
/// Best-effort, and deliberately so — a warning is never worth failing a session that is
/// otherwise fine. A client that does not recognize `code` ignores the instruction.
pub async fn send_msg_best_effort(to_client: &mpsc::Sender<Bytes>, code: u32, args: &[&str]) {
    let instr = guacr_protocol::format_msg(code, args);
    if to_client.send(Bytes::from(instr)).await.is_err() {
        debug!("Session: Failed to send msg code {code} (client may have closed)");
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
///
/// Records first and returns without sending when the session requires a recording it can
/// no longer produce: the client must not receive output that nothing is recording. Every caller
/// already turns this `Err` into a handler error, so the session ends. The error type stays
/// `String` because 90-odd call sites map it themselves.
pub async fn send_and_record(
    to_client: &mpsc::Sender<Bytes>,
    recorder: &mut Option<MultiFormatRecorder>,
    instruction: Bytes,
) -> std::result::Result<(), String> {
    record_server_output(recorder, &instruction).map_err(|e| e.to_string())?;
    to_client
        .send(instruction)
        .await
        .map_err(|e| format!("Send failed: {}", e))
}

/// Record a server-to-client instruction (if recording is enabled).
///
/// The seam for handlers that cannot use [`send_and_record`]: VNC, RDP and RBI each own a
/// send path that counts frames and chooses a per-viewer sender first, so they call this and
/// then send themselves. Recording before sending is the point — a strict session whose
/// recording has stopped must not put another frame on the wire.
///
/// Returns `Err(HandlerError::RecordingFailed)` only when the session may not continue
/// unrecorded (the recording is required and cannot resume).
pub fn record_server_output(
    recorder: &mut Option<MultiFormatRecorder>,
    instruction: &Bytes,
) -> Result<()> {
    if let Some(ref mut rec) = recorder {
        if let Err(e) = rec.record_instruction(RecordingDirection::ServerToClient, instruction) {
            return recording_failure("server output", e);
        }
    }
    Ok(())
}

/// Record a client-to-server instruction (if recording is enabled).
///
/// Shared implementation used by all protocol handlers. Only records; does not send.
///
/// Returns `Err(HandlerError::RecordingFailed)` when the session may not continue
/// unrecorded (the recording is required and cannot resume). Callers propagate it; the session ends.
pub fn record_client_input(
    recorder: &mut Option<MultiFormatRecorder>,
    instruction: &Bytes,
) -> Result<()> {
    if let Some(ref mut rec) = recorder {
        if let Err(e) = rec.record_instruction(RecordingDirection::ClientToServer, instruction) {
            return recording_failure("client input", e);
        }
    }
    Ok(())
}

/// Decide what a recording failure means for the session.
///
/// `MultiFormatRecorder` applies the `recording-allow-unrecorded` policy and reports
/// [`RecordingError::Unrecordable`] when the session may not continue without a recording
/// (`multi.rs`, `classify_write_failure`). Everything else is advisory: a permissive session
/// is allowed to lose recording data, and warning is all that is left to do.
///
/// This is the only place the distinction is made. Handlers used to `warn!` on every
/// recording error, which made `recording-allow-unrecorded=false` unenforceable after the
/// recorder had been constructed: a destination that died one minute into a session left the
/// user working, unrecorded, for the rest of it.
fn recording_failure(what: &str, err: RecordingError) -> Result<()> {
    match err {
        RecordingError::Unrecordable(reason) => Err(HandlerError::RecordingFailed(format!(
            "{what} could not be recorded and this session requires recording: {reason}"
        ))),
        other => {
            warn!("Failed to record {}: {}", what, other);
            Ok(())
        }
    }
}

/// Record a client-to-server instruction that came from a shared-session viewer
/// rather than from the session owner.
///
/// Emits `actor,<guid>,<display name>` immediately before the input, so a reader of the
/// recording can tell whose keystroke it was; the GUID is what an audit correlates on,
/// since display names are neither stable nor unique. Unattributed input stays
/// byte-identical to [`record_client_input`], and Guacamole clients ignore opcodes
/// they do not know, so existing players are unaffected.
pub fn record_client_input_attributed(
    recorder: &mut Option<MultiFormatRecorder>,
    instruction: &Bytes,
    actor: ViewerActor<'_>,
) -> Result<()> {
    if recorder.is_none() {
        return Ok(());
    }
    let guid = actor.guid.to_string();
    let marker = Bytes::from(format_instruction("actor", &[&guid, actor.display_name]));
    record_client_input(recorder, &marker)?;
    record_client_input(recorder, instruction)
}
