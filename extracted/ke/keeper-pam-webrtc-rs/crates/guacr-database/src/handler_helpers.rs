// Shared helper functions for database handler boilerplate.
//
// These functions extract the identical patterns that appear across all
// database handlers (Redis, Cassandra, DynamoDB, Elasticsearch, ODBC):
//   - Display size parsing
//   - Connection error/success rendering
//   - Help text rendering
//   - Quit handling
//   - Render-and-send shorthand

use bytes::Bytes;
use guacr_handlers::{HandlerError, MultiFormatRecorder};
use std::collections::HashMap;
use tokio::sync::mpsc;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::ThreatDetector;
#[cfg(feature = "threat-detection")]
use std::sync::Arc;

use crate::query_executor::QueryExecutor;
use crate::recording::send_and_record;

/// Parse display size from connection params and calculate terminal dimensions.
///
/// The "size" parameter is formatted as "width,height,dpi" (e.g. "1024,768,96").
/// Returns (pixel_width, pixel_height, cols, rows) where cols/rows are calculated
/// from a 9x18 pixel character cell size.
pub fn parse_display_size(params: &HashMap<String, String>) -> (u32, u32, u16, u16) {
    let size_params = params
        .get("size")
        .map(|s| s.as_str())
        .unwrap_or("1024,768,96");
    let size_parts: Vec<&str> = size_params.split(',').collect();
    let width: u32 = size_parts
        .first()
        .and_then(|s| s.parse().ok())
        .unwrap_or(1024);
    let height: u32 = size_parts
        .get(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(768);

    // Calculate terminal dimensions (9x18 pixels per character cell)
    let cols = (width / 9).max(80) as u16;
    let rows = (height / 18).max(24) as u16;

    (width, height, cols, rows)
}

/// Render connection error with troubleshooting tips, then drain the client channel.
///
/// This is the standard pattern used when a database connection fails:
/// 1. Display the error message
/// 2. List numbered troubleshooting tips
/// 3. Render the screen and send to client
/// 4. Drain remaining client messages (so the handler can exit cleanly)
pub async fn render_connection_error(
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    from_client: &mut mpsc::Receiver<Bytes>,
    error_msg: &str,
    tips: &[&str],
    recorder: &mut Option<MultiFormatRecorder>,
) -> Result<(), HandlerError> {
    let mut msg = format!("ERROR: {}\n\nTroubleshooting:", error_msg);
    for (i, tip) in tips.iter().enumerate() {
        msg.push_str(&format!("\n  {}. {}", i + 1, tip));
    }
    executor
        .write_error(&msg)
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    send_render(executor, to_client, recorder).await?;

    // Drain remaining client messages so the handler can exit cleanly
    while from_client.recv().await.is_some() {}

    Ok(())
}

/// Render connection success banner and initial screen.
///
/// Displays a list of informational lines (e.g. "Connected to X at host:port",
/// "Database: foo", "Type 'help' for available commands."), followed by a prompt,
/// then renders and sends to client.
pub async fn render_connection_success(
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    info_lines: &[&str],
    recorder: &mut Option<MultiFormatRecorder>,
) -> Result<(), HandlerError> {
    let msg = info_lines.join("\n");
    executor
        .write_line(&msg)
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    send_render(executor, to_client, recorder).await?;

    Ok(())
}

/// A section in the help text, consisting of a title and a list of (command, description) pairs.
pub struct HelpSection {
    pub title: &'static str,
    pub commands: Vec<(&'static str, &'static str)>,
}

/// Render help text from structured sections.
///
/// Displays a header line ("HandlerName - Available commands:"), then each
/// section with its commands formatted as "  command_padded  description",
/// followed by "Type 'quit' to disconnect".
pub async fn render_help(
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    handler_name: &str,
    sections: &[HelpSection],
    recorder: &mut Option<MultiFormatRecorder>,
) -> Result<(), HandlerError> {
    let mut help = format!("{} - Available commands:\n", handler_name);
    for section in sections {
        help.push_str(&format!("\n{}:\n", section.title));
        for (cmd, desc) in &section.commands {
            help.push_str(&format!("  {:<20} {}\n", cmd, desc));
        }
    }
    help.push_str("\nType 'quit' to disconnect");

    executor
        .write_line(&help)
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    send_render(executor, to_client, recorder).await?;

    Ok(())
}

/// Handle quit/exit command -- render "Bye" and return a Disconnected error.
///
/// The caller should propagate the returned error to terminate the handler.
/// Each instruction is also recorded to the session file via the recorder.
pub async fn handle_quit(
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    recorder: &mut Option<MultiFormatRecorder>,
) -> HandlerError {
    executor.write_status("Bye");
    if let Ok((_, instructions)) = executor.render_screen().await {
        for instr in instructions {
            let _ = send_and_record(to_client, recorder, instr).await;
        }
    }
    HandlerError::Disconnected("User requested disconnect".to_string())
}

/// Render the screen, send all resulting instructions to the client, and record
/// each instruction to the session file.
///
/// This is a shorthand for the pattern that appears dozens of times across
/// all database handlers:
/// ```ignore
/// let (_, instructions) = executor.render_screen().await
///     .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
/// for instr in instructions {
///     send_and_record(to_client, recorder, instr).await
///         .map_err(HandlerError::ChannelError)?;
/// }
/// ```
pub async fn send_render(
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    recorder: &mut Option<MultiFormatRecorder>,
) -> Result<(), HandlerError> {
    let (_, instructions) = executor
        .render_screen()
        .await
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
    for instr in instructions {
        send_and_record(to_client, recorder, instr)
            .await
            .map_err(HandlerError::ChannelError)?;
    }
    Ok(())
}

/// Check a query/command for threats before executing it.
///
/// If the detector decides the session should terminate, writes an error message
/// to the executor, sends a final render, and returns `Err(Disconnected)`.
/// Returns `Ok(())` if the query is safe (or if threat-detection is not compiled in).
///
/// This eliminates the identical 30-line threat check block that would otherwise
/// appear in each of the 10+ database handlers.
#[cfg(feature = "threat-detection")]
#[allow(clippy::too_many_arguments)]
pub async fn maybe_terminate_on_threat(
    threat_detector: &Arc<ThreatDetector>,
    session_id: &str,
    query: &str,
    username: &str,
    hostname: &str,
    db_type: &str,
    executor: &mut QueryExecutor,
    to_client: &mpsc::Sender<Bytes>,
    recorder: &mut Option<MultiFormatRecorder>,
) -> Result<(), HandlerError> {
    if let Some(threat) = crate::threat::analyze_query(
        threat_detector,
        session_id,
        query,
        username,
        hostname,
        db_type,
    )
    .await
    {
        if threat.should_terminate_session {
            let _ = executor.write_error(&format!(
                "Session terminated by security policy: {}",
                threat.description
            ));
            if let Ok((_, instrs)) = executor.render_screen().await {
                for instr in instrs {
                    let _ = send_and_record(to_client, recorder, instr).await;
                }
            }
            return Err(HandlerError::Disconnected(format!(
                "Threat detected: {}",
                threat.description
            )));
        }
    }
    Ok(())
}
