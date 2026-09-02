// TN3270 protocol handler
//
// Connects to an IBM 3270 mainframe over Telnet/TN3270, renders the block-mode
// screen to JPEG using the ratatui buffer pipeline, and forwards keyboard input
// back as 3270 AID codes + Read Modified field data.
//
// Connection params:
//   hostname  - TN3270 server hostname or IP
//   port      - TCP port (default: 3270)

use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    connect_tcp_with_timeout, record_client_input, send_and_record, send_disconnect, send_name,
    send_ready, ConnectionParameters, HandlerError, HandlerStats, HealthStatus,
    MultiFormatRecorder, ProtocolHandler, RecordingConfig, VideoOutput,
};
use guacr_protocol::{
    format_terminal_data_binary,
    telnet::{extract_record, DO, EOR, IAC, OPT_BINARY, OPT_EOR, OPT_TERMINAL_TYPE, SB, SE, WILL},
};
use guacr_terminal::{
    buffer_to_ansi, parse_key_instruction, DEFAULT_COLS, DEFAULT_ROWS, RENDER_INTERVAL_MS,
};
use log::{debug, info, warn};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::mpsc;

use crate::datastream::{parse_data_stream, Aid};
use crate::renderer;
use crate::screen::ScreenBuffer;

// -- Handler -----------------------------------------------------------------

pub struct Tn3270Handler;

impl Tn3270Handler {
    pub fn new() -> Self {
        Self
    }
}

impl Default for Tn3270Handler {
    fn default() -> Self {
        Self::new()
    }
}

#[async_trait]
impl ProtocolHandler for Tn3270Handler {
    fn name(&self) -> &str {
        "tn3270"
    }

    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        let conn = ConnectionParameters::from_params(&params, 3270u16)?;
        let hostname = conn.hostname;
        let port = conn.port;

        // Screen dimensions — IBM 3270 model sizes:
        //   Model 2: 24×80 (default)   Model 3: 32×80
        //   Model 4: 43×80             Model 5: 27×132
        let (rows, cols) = match params.get("model").map(|s| s.as_str()) {
            Some("3") => (32u16, 80u16),
            Some("4") => (43u16, 80u16),
            Some("5") => (27u16, 132u16),
            _ => {
                let r = params
                    .get("rows")
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(DEFAULT_ROWS);
                let c = params
                    .get("cols")
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(DEFAULT_COLS);
                (r, c)
            }
        };

        // Session startup
        send_ready(&to_client, "tn3270").await?;
        send_name(&to_client, &format!("TN3270 \u{2014} {}", hostname)).await?;

        let conn_id = params.get("client_id").cloned().unwrap_or_default();

        // Initialize recording
        // ── GUID-based viewer join (Phase 6b) ────────────────────────────────
        if params.contains_key("share_guid") {
            return guacr_handlers::share_viewer::check_viewer_join(
                &params,
                &to_client,
                from_client,
                &conn_id,
            )
            .await
            .unwrap_or(Ok(()));
        }
        // Initialize recording if enabled
        let recording_config = RecordingConfig::from_params(&params);
        if recording_config.is_enabled() {
            info!(
                "[conn={conn_id}] TN3270: Recording enabled - ses={}, asciicast={}, typescript={}",
                recording_config.is_ses_enabled(),
                recording_config.is_asciicast_enabled(),
                recording_config.is_typescript_enabled()
            );
        }
        let mut recorder: Option<MultiFormatRecorder> = if recording_config.is_enabled() {
            match MultiFormatRecorder::new(&recording_config, &params, "tn3270", cols, rows) {
                Ok(rec) => {
                    info!("[conn={conn_id}] TN3270: Session recording initialized");
                    Some(rec)
                }
                Err(e) => {
                    warn!(
                        "[conn={conn_id}] TN3270: Failed to initialize recording: {}",
                        e
                    );
                    None
                }
            }
        } else {
            None
        };

        // Connect to TN3270 server
        info!(
            "[conn={conn_id}] TN3270: Connecting to {}:{}",
            hostname, port
        );
        let addr = format!("{}:{}", hostname, port);
        let mut stream = connect_tcp_with_timeout(addr, 30).await.map_err(|_| {
            HandlerError::ConnectionFailed(format!("Failed to connect to {}:{}", hostname, port))
        })?;

        // TN3270 Telnet negotiation — must be done in strict order.
        // Servers like Hercules/TK4- perform a challenge-response handshake:
        //   Server: IAC DO TERMINAL-TYPE
        //   Client: IAC WILL TERMINAL-TYPE
        //   Server: IAC SB TERMINAL-TYPE SEND IAC SE
        //   Client: IAC SB TERMINAL-TYPE IS <model> IAC SE
        //           + WILL EOR + DO EOR + WILL BINARY + DO BINARY
        // Sending SB IS before the server asks (one-shot) causes Hercules to
        // ignore the terminal type and never send the initial screen.
        let term_type = match params.get("model").map(|s| s.as_str()) {
            Some("3") => b"IBM-3278-3".as_slice(),
            Some("4") => b"IBM-3278-4".as_slice(),
            Some("5") => b"IBM-3278-5".as_slice(),
            _ => b"IBM-3278-2".as_slice(),
        };

        // Step 1: announce WILL TERMINAL-TYPE, then pause briefly so Hercules can
        // process it and enter the "waiting for SB IS" state before we respond.
        // Hercules sends DO TERMINAL-TYPE + SB SEND together in a single burst on
        // connect; without a pause, our SB IS arrives before Hercules is ready.
        stream
            .write_all(&[IAC, WILL, OPT_TERMINAL_TYPE])
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        tokio::time::sleep(Duration::from_millis(200)).await;

        // Step 2: read server negotiation into the pending buffer so any
        // screen data that arrives in the same TCP segment is not discarded.
        // We need to see IAC SB TERMINAL-TYPE SEND before responding with SB IS.
        let mut screen = ScreenBuffer::new(rows, cols);
        let mut dirty = false;
        let mut pending: Vec<u8> = Vec::with_capacity(8192);
        let mut net_buf = vec![0u8; 4096];

        // Read until we have seen the SB TERMINAL-TYPE SEND (ff fa 18 01 ff f0)
        let sb_send_marker = &[IAC, SB, OPT_TERMINAL_TYPE, 0x01, IAC, SE];
        tokio::time::timeout(Duration::from_secs(5), async {
            loop {
                let n = stream.read(&mut net_buf).await?;
                if n == 0 {
                    break;
                }
                pending.extend_from_slice(&net_buf[..n]);
                // Check if the pending buffer contains the SB SEND marker
                if pending
                    .windows(sb_send_marker.len())
                    .any(|w| w == sb_send_marker)
                {
                    break;
                }
            }
            Ok::<(), std::io::Error>(())
        })
        .await
        .map_err(|_| {
            HandlerError::ConnectionFailed("TN3270 negotiation timeout waiting for SB SEND".into())
        })?
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        // Strip the negotiation bytes from pending — keep any data record bytes
        // that may have arrived in the same TCP segment as the SB SEND.
        // The simplest approach: drain everything up to and including SB SEND.
        if let Some(pos) = pending
            .windows(sb_send_marker.len())
            .position(|w| w == sb_send_marker)
        {
            pending.drain(..pos + sb_send_marker.len());
        }

        // Step 3a: respond with terminal type (SB IS … SE) as its own TCP segment.
        // Hercules needs to see SB IS before the EOR/BINARY negotiations.
        let mut sb_is = vec![IAC, SB, OPT_TERMINAL_TYPE, 0x00];
        sb_is.extend_from_slice(term_type);
        sb_is.extend_from_slice(&[IAC, SE]);
        stream
            .write_all(&sb_is)
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        // Step 3b: negotiate EOR and BINARY in a separate TCP segment after a brief
        // pause, matching the timing the Hercules server expects.
        tokio::time::sleep(Duration::from_millis(300)).await;
        stream
            .write_all(&[
                IAC, WILL, OPT_EOR, IAC, DO, OPT_EOR, IAC, WILL, OPT_BINARY, IAC, DO, OPT_BINARY,
            ])
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        // Read Hercules's response to our SB IS + options. Hercules sends option
        // confirmations (DO EOR + WILL EOR + DO BINARY + WILL BINARY) followed by
        // the initial screen, all within ~1-2 seconds. We read with a 3-second
        // total deadline so the data lands in `pending` before we enter the
        // select loop — avoiding a permanent stream.read block on a socket that
        // already has everything buffered at the OS level.
        let read_deadline = tokio::time::Instant::now() + Duration::from_secs(3);
        loop {
            let remaining = read_deadline.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            net_buf.fill(0);
            match tokio::time::timeout(remaining, stream.read(&mut net_buf)).await {
                Ok(Ok(0)) => {
                    debug!("[conn={conn_id}] TN3270: Server closed during post-negotiation read");
                    break;
                }
                Ok(Ok(n)) => {
                    debug!(
                        "[conn={conn_id}] TN3270: Post-negotiation read: {} bytes",
                        n
                    );
                    pending.extend_from_slice(&net_buf[..n]);
                    // If we have a complete EOR-terminated record, stop reading.
                    if pending.windows(2).any(|w| w == [IAC, EOR]) {
                        break;
                    }
                }
                Ok(Err(e)) => {
                    warn!(
                        "[conn={conn_id}] TN3270: Read error during post-negotiation: {}",
                        e
                    );
                    break;
                }
                Err(_) => {
                    debug!(
                        "[conn={conn_id}] TN3270: Post-negotiation read timed out, pending={} bytes",
                        pending.len()
                    );
                    break;
                }
            }
        }

        debug!("[conn={conn_id}] TN3270: Negotiation complete, waiting for initial screen");

        // Hercules often sends option confirmations + initial screen in the same TCP
        // burst as SB SEND, so those bytes are already in `pending` before we enter
        // the select loop. Process them now so stream.read doesn't block on a socket
        // that has nothing new to give us while pending holds a complete record.
        {
            while let Some(record) = extract_record(&mut pending) {
                let is_wsf = matches!(record.first().copied(), Some(0x11) | Some(0xF3));
                if is_wsf {
                    debug!(
                        "[conn={conn_id}] TN3270: WSF query received — sending null Query Reply"
                    );
                    let reply: [u8; 6] = [0x00, 0x04, 0x81, 0xFF, IAC, EOR];
                    if let Err(e) = stream.write_all(&reply).await {
                        warn!(
                            "[conn={conn_id}] TN3270: Failed to send WSF Query Reply: {}",
                            e
                        );
                    }
                    continue;
                }
                match parse_data_stream(&record) {
                    Ok(ds) => {
                        screen.apply_data_stream(&ds);
                        dirty = true;
                    }
                    Err(e) => warn!(
                        "[conn={conn_id}] TN3270: Initial pending parse error: {} ({} bytes)",
                        e,
                        record.len()
                    ),
                }
            }
        }

        // Auto-logon is not implemented for TN3270 — users log in manually after connect.

        let mut render_timer = tokio::time::interval(Duration::from_millis(RENDER_INTERVAL_MS));
        render_timer.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Sync flow control — prevents overwhelming slow clients (same as guacd behavior).
        // After sending SYNC_BYTE_THRESHOLD bytes, we send a text sync instruction and
        // pause rendering until the client ACKs. Server data continues to accumulate in
        // `pending` while paused. The from_client arm remains active so key input still works.
        let mut sync_bytes_sent: usize = 0;
        let mut sync_pending: Option<u64> = None;
        // A lost/late sync ack must not freeze rendering forever — auto-resume after this.
        let mut sync_sent_at: Option<std::time::Instant> = None;
        const SYNC_BYTE_THRESHOLD: usize = 4096;
        const SYNC_ACK_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(3);

        loop {
            tokio::select! {
                // Data from the TN3270 server
                result = stream.read(&mut net_buf) => {
                    match result {
                        Ok(0) => {
                            info!("[conn={conn_id}] TN3270: Server closed connection");
                            break;
                        }
                        Ok(n) => {
                            pending.extend_from_slice(&net_buf[..n]);
                            // Process all complete EOR-terminated records.
                            while let Some(record) = extract_record(&mut pending) {
                                // WSF Query (0x11 standard / 0xF3 SNA): Hercules sends this
                                // before the initial screen to probe terminal capabilities.
                                // Respond with a null Query Reply so it sends the logon screen.
                                let is_wsf = record.first().copied() == Some(0x11)
                                    || record.first().copied() == Some(0xF3);
                                if is_wsf {
                                    debug!("[conn={conn_id}] TN3270: WSF query detected — sending null Query Reply");
                                    // Null Query Reply: length=4, ID=0x81, code=0xFF (no features)
                                    let reply: [u8; 6] = [0x00, 0x04, 0x81, 0xFF, IAC, EOR];
                                    if let Err(e) = stream.write_all(&reply).await {
                                        warn!("[conn={conn_id}] TN3270: Failed to send WSF Query Reply: {}", e);
                                        break;
                                    }
                                    continue;
                                }
                                match parse_data_stream(&record) {
                                    Ok(ds) => {
                                        screen.apply_data_stream(&ds);
                                        dirty = true;
                                    }
                                    Err(e) => {
                                        warn!(
                                            "[conn={conn_id}] TN3270: Data stream parse error: {} \
                                             ({} bytes)",
                                            e,
                                            record.len()
                                        );
                                    }
                                }
                            }
                        }
                        Err(e) => {
                            warn!("[conn={conn_id}] TN3270: Read error: {}", e);
                            break;
                        }
                    }
                }

                // Render tick. While waiting for a client sync ACK we pause rendering, but a
                // lost/late ack must not freeze the screen forever — auto-resume on timeout.
                _ = render_timer.tick() => {
                    if sync_pending.is_some() {
                        if sync_sent_at
                            .map(|t| t.elapsed() >= SYNC_ACK_TIMEOUT)
                            .unwrap_or(false)
                        {
                            warn!("[conn={conn_id}] TN3270: sync ack timed out — resuming render");
                            sync_pending = None;
                            sync_sent_at = None;
                        } else {
                            continue;
                        }
                    }
                    if !dirty {
                        continue;
                    }
                    dirty = false;

                    let buffer = renderer::screen_to_buffer(&screen);
                    let ansi = buffer_to_ansi(&buffer);
                    if let Some(ref mut rec) = recorder {
                        let _ = rec.record_output(&ansi);
                    }
                    let instr = format_terminal_data_binary(&ansi);
                    let frame_len = instr.len();
                    if send_and_record(&to_client, &mut recorder, instr).await.is_err() {
                        info!("[conn={conn_id}] TN3270: Client channel closed during render");
                        break;
                    }

                    // Flow control: after SYNC_BYTE_THRESHOLD bytes, send a sync
                    // instruction and pause rendering until client ACKs.
                    sync_bytes_sent += frame_len;
                    if sync_bytes_sent >= SYNC_BYTE_THRESHOLD {
                        let ts = std::time::SystemTime::now()
                            .duration_since(std::time::UNIX_EPOCH)
                            .unwrap_or_default()
                            .as_millis() as u64;
                        let ts_str = ts.to_string();
                        let sync_instr = format!("4.sync,{}.{};", ts_str.len(), ts_str);
                        if to_client
                            .send(Bytes::from(sync_instr.into_bytes()))
                            .await
                            .is_err()
                        {
                            info!("[conn={conn_id}] TN3270: Client channel closed sending sync");
                            break;
                        }
                        sync_pending = Some(ts);
                        sync_sent_at = Some(std::time::Instant::now());
                        sync_bytes_sent = 0;
                    }
                }

                // Keyboard input from the Guacamole client
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        debug!("[conn={conn_id}] TN3270: Client disconnected");
                        break;
                    };
                    record_client_input(&mut recorder, &msg);
                    let msg_str = String::from_utf8_lossy(&msg);

                    // Sync ACK from client — re-enable rendering.
                    if msg_str.starts_with("4.sync,") {
                        if let Some(pending_ts) = sync_pending {
                            // Parse: "4.sync,<len>.<ts>;"
                            if let Some(client_ts) = msg_str
                                .strip_prefix("4.sync,")
                                .and_then(|s| s.find('.').map(|i| &s[i+1..]))
                                .and_then(|s| s.strip_suffix(';'))
                                .and_then(|s| s.parse::<u64>().ok())
                            {
                                if client_ts >= pending_ts {
                                    sync_pending = None;
                                    sync_sent_at = None;
                                }
                            }
                        }
                        // Don't process sync as a key event — it's flow control only.
                        continue;
                    }

                    if let Some(key) = parse_key_instruction(&msg_str) {
                        if !key.pressed {
                            continue;
                        }
                        // Always mark dirty on any key press — local operations
                        // (typing, cursor movement, Tab) update the ScreenBuffer
                        // without sending bytes to the server, so we must still
                        // re-render so the user sees their input reflected.
                        dirty = true;
                        if let Some(mut server_bytes) = handle_key(&mut screen, key.keysym) {
                            // TN3270 records sent to the host must be terminated with IAC EOR.
                            server_bytes.extend_from_slice(&[IAC, EOR]);
                            if let Err(e) = stream.write_all(&server_bytes).await {
                                warn!("[conn={conn_id}] TN3270: Write error: {}", e);
                                break;
                            }
                        }
                    }
                    // size instruction: fixed 24×80 for now
                }
            }
        }

        if let Some(rec) = recorder.take() {
            if let Err(e) = rec.finalize() {
                warn!(
                    "[conn={conn_id}] TN3270: Failed to finalize recording: {}",
                    e
                );
            } else {
                info!("[conn={conn_id}] TN3270: Session recording finalized");
            }
        }

        send_disconnect(&to_client).await;
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

// -- Key handling ------------------------------------------------------------

/// Convert a Guacamole X11 keysym to bytes to send to the TN3270 server.
///
/// Returns `None` for keys that only affect local state (Tab, character input)
/// and `Some(bytes)` for keys that require a network transmission (Enter, PF, Clear).
pub(crate) fn handle_key(screen: &mut ScreenBuffer, keysym: u32) -> Option<Vec<u8>> {
    match keysym {
        // Enter — transmit modified fields to server
        0xFF0D => Some(screen.read_modified_fields(Aid::Enter)),

        // Escape — 3270 Clear key (clears screen, sends AID to server)
        0xFF1B => Some(screen.read_modified_fields(Aid::Clear)),

        // Tab — advance to next unprotected field (local, no server message)
        0xFF09 => {
            screen.tab_forward();
            None
        }

        // BackTab (shift-tab) — previous unprotected field (local)
        0xFE20 => {
            screen.tab_backward();
            None
        }

        // PF1–PF12 (F1–F12)
        0xFFBE => Some(screen.read_modified_fields(Aid::Pf(1))),
        0xFFBF => Some(screen.read_modified_fields(Aid::Pf(2))),
        0xFFC0 => Some(screen.read_modified_fields(Aid::Pf(3))),
        0xFFC1 => Some(screen.read_modified_fields(Aid::Pf(4))),
        0xFFC2 => Some(screen.read_modified_fields(Aid::Pf(5))),
        0xFFC3 => Some(screen.read_modified_fields(Aid::Pf(6))),
        0xFFC4 => Some(screen.read_modified_fields(Aid::Pf(7))),
        0xFFC5 => Some(screen.read_modified_fields(Aid::Pf(8))),
        0xFFC6 => Some(screen.read_modified_fields(Aid::Pf(9))),
        0xFFC7 => Some(screen.read_modified_fields(Aid::Pf(10))),
        0xFFC8 => Some(screen.read_modified_fields(Aid::Pf(11))),
        0xFFC9 => Some(screen.read_modified_fields(Aid::Pf(12))),

        // PF13–PF24 (F13–F24, or Shift+F1–F12 on some keyboards)
        0xFFCA => Some(screen.read_modified_fields(Aid::Pf(13))),
        0xFFCB => Some(screen.read_modified_fields(Aid::Pf(14))),
        0xFFCC => Some(screen.read_modified_fields(Aid::Pf(15))),
        0xFFCD => Some(screen.read_modified_fields(Aid::Pf(16))),
        0xFFCE => Some(screen.read_modified_fields(Aid::Pf(17))),
        0xFFCF => Some(screen.read_modified_fields(Aid::Pf(18))),
        0xFFD0 => Some(screen.read_modified_fields(Aid::Pf(19))),
        0xFFD1 => Some(screen.read_modified_fields(Aid::Pf(20))),
        0xFFD2 => Some(screen.read_modified_fields(Aid::Pf(21))),
        0xFFD3 => Some(screen.read_modified_fields(Aid::Pf(22))),
        0xFFD4 => Some(screen.read_modified_fields(Aid::Pf(23))),
        0xFFD5 => Some(screen.read_modified_fields(Aid::Pf(24))),

        // PA1–PA3 (program attention — do NOT include modified field data).
        // IBM 3270-specific X11 keysyms: PA1=0xFD11, PA2=0xFD12, PA3=0xFD13.
        // 0xFFE1/0xFFE2/0xFFE3 are Shift_L/Shift_R/Control_L — NOT PA keys.
        0xFD11 => Some(screen.read_modified_fields(Aid::Pa(1))),
        0xFD12 => Some(screen.read_modified_fields(Aid::Pa(2))),
        0xFD13 => Some(screen.read_modified_fields(Aid::Pa(3))),

        // Arrow keys — cursor movement (local, no server message)
        0xFF51 => {
            // Left
            let size = screen.size();
            let pos = (screen.cursor_pos() + size - 1) % size;
            screen.set_cursor_position(pos);
            None
        }
        0xFF53 => {
            // Right
            let size = screen.size();
            let pos = (screen.cursor_pos() + 1) % size;
            screen.set_cursor_position(pos);
            None
        }
        0xFF52 => {
            // Up
            let cols = screen.cols();
            let size = screen.size();
            let pos = (screen.cursor_pos() + size - cols) % size;
            screen.set_cursor_position(pos);
            None
        }
        0xFF54 => {
            // Down
            let cols = screen.cols();
            let size = screen.size();
            let pos = (screen.cursor_pos() + cols) % size;
            screen.set_cursor_position(pos);
            None
        }

        // Backspace — move cursor left and clear the character there
        0xFF08 => {
            let size = screen.size();
            let pos = (screen.cursor_pos() + size - 1) % size;
            screen.set_cursor_position(pos);
            screen.delete_at_cursor();
            None
        }

        // Delete — clear character at current cursor position
        0xFFFF => {
            screen.delete_at_cursor();
            None
        }

        // Printable ASCII — type into current field (local, sent on Enter)
        keysym if (0x20..=0x7E).contains(&keysym) => {
            if let Some(ch) = char::from_u32(keysym) {
                screen.input_char(ch);
            }
            None
        }

        // All other keys ignored
        _ => None,
    }
}
