// TN5250 protocol handler
//
// Connects to an IBM AS/400 / IBM i system over Telnet/TN5250, renders the
// block-mode screen to JPEG using the ratatui buffer pipeline, and forwards
// keyboard input back as 5250 AID codes + inbound field data.
//
// Connection params:
//   hostname  - TN5250 server hostname or IP
//   port      - TCP port (default: 23)

use async_trait::async_trait;
use bytes::Bytes;
use guacr_handlers::{
    connect_tcp_with_timeout, send_disconnect, send_name, send_ready, ConnectionParameters,
    HandlerError, HandlerStats, HealthStatus, ProtocolHandler, VideoOutput,
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
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::mpsc;

use crate::datastream::{
    aid_byte_for_key, build_response_record, encode_address, parse_5250_record,
};
use crate::renderer;
use crate::screen::ScreenBuffer5250;

// 5250 SBA (Set Buffer Address) order byte used when building inbound records
const SBA_ORDER: u8 = 0x11;

// ---------------------------------------------------------------------------

pub struct Tn5250Handler;

impl Tn5250Handler {
    pub fn new() -> Self {
        Self
    }
}

impl Default for Tn5250Handler {
    fn default() -> Self {
        Self::new()
    }
}

#[async_trait]
impl ProtocolHandler for Tn5250Handler {
    fn name(&self) -> &str {
        "tn5250"
    }

    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        // ── GUID-based viewer join (Phase 6b) ────────────────────────────────
        if params.contains_key("share_guid") {
            let conn_id = params.get("client_id").cloned().unwrap_or_default();
            return guacr_handlers::share_viewer::check_viewer_join(
                &params,
                &to_client,
                from_client,
                &conn_id,
            )
            .await
            .unwrap_or(Ok(()));
        }
        let conn = ConnectionParameters::from_params(&params, 23u16)?;
        let hostname = conn.hostname;
        let port = conn.port;

        // AS/400 standard sizes: 24×80 or 27×132 (enhanced model)
        let (rows, cols) = match params.get("model").map(|s| s.as_str()) {
            Some("enhanced") | Some("27x132") => (27u16, 132u16),
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
        send_ready(&to_client, "tn5250").await?;
        send_name(&to_client, &format!("TN5250 \u{2014} {}", hostname)).await?;

        info!("TN5250: Connecting to {}:{}", hostname, port);
        let addr = format!("{}:{}", hostname, port);
        let mut stream = connect_tcp_with_timeout(addr, 30).await.map_err(|_| {
            HandlerError::ConnectionFailed(format!("Failed to connect to {}:{}", hostname, port))
        })?;

        // TN5250 Telnet negotiation — IBM-5251-11 = standard 24×80 5250 terminal
        // IBM-5291-1 = enhanced 27×132
        let term_type: &[u8] = if cols > 80 {
            b"IBM-5292-2"
        } else {
            b"IBM-5251-11"
        };
        let mut negotiation = vec![
            IAC,
            WILL,
            OPT_TERMINAL_TYPE,
            IAC,
            SB,
            OPT_TERMINAL_TYPE,
            0x00,
        ];
        negotiation.extend_from_slice(term_type);
        negotiation.extend_from_slice(&[
            IAC, SE, IAC, WILL, OPT_EOR, IAC, WILL, OPT_BINARY, IAC, DO, OPT_BINARY,
        ]);
        stream
            .write_all(&negotiation)
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

        let mut screen = ScreenBuffer5250::new(rows, cols);
        let mut dirty = false;
        let mut pending: Vec<u8> = Vec::with_capacity(8192);
        let mut net_buf = vec![0u8; 4096];

        let mut render_timer =
            tokio::time::interval(tokio::time::Duration::from_millis(RENDER_INTERVAL_MS));
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
                result = stream.read(&mut net_buf) => {
                    match result {
                        Ok(0) => {
                            info!("TN5250: Server closed connection");
                            break;
                        }
                        Ok(n) => {
                            pending.extend_from_slice(&net_buf[..n]);
                            while let Some(record_bytes) = extract_record(&mut pending) {
                                match parse_5250_record(&record_bytes) {
                                    Ok(record) => {
                                        screen.apply_record(&record);
                                        dirty = true;
                                    }
                                    Err(e) => {
                                        debug!(
                                            "TN5250: Parse error: {} (first bytes: {:02X?})",
                                            e,
                                            &record_bytes[..record_bytes.len().min(8)]
                                        );
                                    }
                                }
                            }
                        }
                        Err(e) => {
                            warn!("TN5250: Read error: {}", e);
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
                            warn!("TN5250: sync ack timed out — resuming render");
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
                    let instr = format_terminal_data_binary(&ansi);
                    let frame_len = instr.len();
                    let _ = to_client.send(instr).await;

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
                        let _ = to_client.send(Bytes::from(sync_instr.into_bytes())).await;
                        sync_pending = Some(ts);
                        sync_sent_at = Some(std::time::Instant::now());
                        sync_bytes_sent = 0;
                    }
                }

                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        debug!("TN5250: Client disconnected");
                        break;
                    };
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
                        if let Some(server_bytes) = handle_key(&mut screen, key.keysym) {
                            // Append IAC EOR to terminate the record
                            let mut framed = server_bytes;
                            framed.push(IAC);
                            framed.push(EOR);
                            if let Err(e) = stream.write_all(&framed).await {
                                warn!("TN5250: Write error: {}", e);
                                break;
                            }
                            dirty = true;
                        }
                    }
                }
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

// ---------------------------------------------------------------------------
// Key handling
// ---------------------------------------------------------------------------

fn handle_key(screen: &mut ScreenBuffer5250, keysym: u32) -> Option<Vec<u8>> {
    match keysym {
        // Enter
        0xFF0D => Some(build_aid_response(screen, 0xF1)),

        // Escape → Clear
        0xFF1B => Some(build_aid_response(screen, 0xBD)),

        // Tab / BackTab
        0xFF09 => {
            screen.tab_forward();
            None
        }
        0xFE20 => {
            screen.tab_backward();
            None
        }

        // F1–F12
        0xFFBE => Some(build_aid_response(screen, aid_byte_for_key("F1").unwrap())),
        0xFFBF => Some(build_aid_response(screen, aid_byte_for_key("F2").unwrap())),
        0xFFC0 => Some(build_aid_response(screen, aid_byte_for_key("F3").unwrap())),
        0xFFC1 => Some(build_aid_response(screen, aid_byte_for_key("F4").unwrap())),
        0xFFC2 => Some(build_aid_response(screen, aid_byte_for_key("F5").unwrap())),
        0xFFC3 => Some(build_aid_response(screen, aid_byte_for_key("F6").unwrap())),
        0xFFC4 => Some(build_aid_response(screen, aid_byte_for_key("F7").unwrap())),
        0xFFC5 => Some(build_aid_response(screen, aid_byte_for_key("F8").unwrap())),
        0xFFC6 => Some(build_aid_response(screen, aid_byte_for_key("F9").unwrap())),
        0xFFC7 => Some(build_aid_response(screen, aid_byte_for_key("F10").unwrap())),
        0xFFC8 => Some(build_aid_response(screen, aid_byte_for_key("F11").unwrap())),
        0xFFC9 => Some(build_aid_response(screen, aid_byte_for_key("F12").unwrap())),

        // F13–F24
        0xFFCA => Some(build_aid_response(screen, aid_byte_for_key("F13").unwrap())),
        0xFFCB => Some(build_aid_response(screen, aid_byte_for_key("F14").unwrap())),
        0xFFCC => Some(build_aid_response(screen, aid_byte_for_key("F15").unwrap())),
        0xFFCD => Some(build_aid_response(screen, aid_byte_for_key("F16").unwrap())),
        0xFFCE => Some(build_aid_response(screen, aid_byte_for_key("F17").unwrap())),
        0xFFCF => Some(build_aid_response(screen, aid_byte_for_key("F18").unwrap())),
        0xFFD0 => Some(build_aid_response(screen, aid_byte_for_key("F19").unwrap())),
        0xFFD1 => Some(build_aid_response(screen, aid_byte_for_key("F20").unwrap())),
        0xFFD2 => Some(build_aid_response(screen, aid_byte_for_key("F21").unwrap())),
        0xFFD3 => Some(build_aid_response(screen, aid_byte_for_key("F22").unwrap())),
        0xFFD4 => Some(build_aid_response(screen, aid_byte_for_key("F23").unwrap())),
        0xFFD5 => Some(build_aid_response(screen, aid_byte_for_key("F24").unwrap())),

        // Page Up / Page Down
        0xFF55 => Some(build_aid_response(
            screen,
            aid_byte_for_key("PageUp").unwrap(),
        )),
        0xFF56 => Some(build_aid_response(
            screen,
            aid_byte_for_key("PageDown").unwrap(),
        )),

        // Printable ASCII
        keysym if (0x20..=0x7E).contains(&keysym) => {
            if let Some(ch) = char::from_u32(keysym) {
                screen.type_character(ch);
            }
            None
        }

        _ => None,
    }
}

/// Build a 5250 inbound record for an AID key press.
///
/// Format: header | AID byte | cursor_row+1 | cursor_col+1
///         | (for each modified field) SBA_ORDER row+1 col+1 data...
fn build_aid_response(screen: &ScreenBuffer5250, aid: u8) -> Vec<u8> {
    let (cursor_row, cursor_col) = screen.cursor_pos();
    let (cr, cc) = encode_address(cursor_row, cursor_col);

    let mut payload = vec![aid, cr, cc];

    for (field_row, field_col, ebcdic_data) in screen.read_modified_fields() {
        let (fr, fc) = encode_address(field_row, field_col);
        payload.push(SBA_ORDER);
        payload.push(fr);
        payload.push(fc);
        payload.extend_from_slice(&ebcdic_data);
    }

    build_response_record(&payload)
}
