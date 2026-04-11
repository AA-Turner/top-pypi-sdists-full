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
use base64::Engine as _;
use bytes::Bytes;
use guacr_handlers::{
    connect_tcp_with_timeout, send_disconnect, send_name, send_ready, ConnectionParameters,
    HandlerError, HandlerStats, HealthStatus, ProtocolHandler, VideoOutput,
};
use guacr_protocol::{
    format_chunked_blobs, format_instruction,
    telnet::{extract_record, DO, IAC, OPT_BINARY, OPT_EOR, OPT_TERMINAL_TYPE, SB, SE, WILL},
    TextProtocolEncoder,
};
use guacr_terminal::{
    current_time_millis, parse_key_instruction, TerminalRenderer, CHAR_HEIGHT, CHAR_WIDTH,
    DEFAULT_COLS, DEFAULT_ROWS, JPEG_QUALITY, RENDER_INTERVAL_MS,
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

        let pixel_width = cols as u32 * CHAR_WIDTH;
        let pixel_height = rows as u32 * CHAR_HEIGHT;

        // Session startup
        send_ready(&to_client, "tn3270").await?;
        send_name(&to_client, &format!("TN3270 \u{2014} {}", hostname)).await?;
        let size_instr = TerminalRenderer::format_size_instruction(0, pixel_width, pixel_height);
        to_client
            .send(Bytes::from(size_instr))
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

        // Connect to TN3270 server
        info!("TN3270: Connecting to {}:{}", hostname, port);
        let addr = format!("{}:{}", hostname, port);
        let mut stream = connect_tcp_with_timeout(addr, 30).await.map_err(|_| {
            HandlerError::ConnectionFailed(format!("Failed to connect to {}:{}", hostname, port))
        })?;

        // TN3270 Telnet negotiation:
        //   WILL TERMINAL-TYPE → SB TERMINAL-TYPE IS <model> SE
        //   WILL EOR, WILL BINARY, DO BINARY
        // Terminal type encodes the model; IBM-3278-2 = 24×80 (Model 2),
        // IBM-3278-3 = 32×80, IBM-3278-4 = 43×80, IBM-3278-5 = 27×132.
        let term_type = match params.get("model").map(|s| s.as_str()) {
            Some("3") => b"IBM-3278-3".as_slice(),
            Some("4") => b"IBM-3278-4".as_slice(),
            Some("5") => b"IBM-3278-5".as_slice(),
            _ => b"IBM-3278-2".as_slice(),
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

        let font_size = CHAR_HEIGHT as f32 * 0.70;
        let term_renderer =
            TerminalRenderer::new_with_dimensions(CHAR_WIDTH, CHAR_HEIGHT, font_size)
                .map_err(|e| HandlerError::ConnectionFailed(e.to_string()))?;

        let mut screen = ScreenBuffer::new(rows, cols);
        let mut protocol_encoder = TextProtocolEncoder::new();
        let mut stream_id = 1u32;
        let mut dirty = false;
        let mut pending: Vec<u8> = Vec::with_capacity(8192);
        let mut net_buf = vec![0u8; 4096];

        let mut render_timer = tokio::time::interval(Duration::from_millis(RENDER_INTERVAL_MS));
        render_timer.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        loop {
            tokio::select! {
                // Data from the TN3270 server
                result = stream.read(&mut net_buf) => {
                    match result {
                        Ok(0) => {
                            info!("TN3270: Server closed connection");
                            break;
                        }
                        Ok(n) => {
                            pending.extend_from_slice(&net_buf[..n]);
                            // Process all complete EOR-terminated records.
                            while let Some(record) = extract_record(&mut pending) {
                                match parse_data_stream(&record) {
                                    Ok(ds) => {
                                        screen.apply_data_stream(&ds);
                                        dirty = true;
                                    }
                                    Err(e) => {
                                        debug!(
                                            "TN3270: Data stream parse error: {} \
                                             (first bytes: {:02X?})",
                                            e,
                                            &record[..record.len().min(8)]
                                        );
                                    }
                                }
                            }
                        }
                        Err(e) => {
                            warn!("TN3270: Read error: {}", e);
                            break;
                        }
                    }
                }

                // Render tick
                _ = render_timer.tick() => {
                    if !dirty {
                        continue;
                    }
                    dirty = false;

                    let jpeg = match renderer::render_with_renderer(&screen, &term_renderer, JPEG_QUALITY) {
                        Ok(j) => j,
                        Err(e) => {
                            warn!("TN3270: Render error: {}", e);
                            continue;
                        }
                    };

                    let b64 = base64::engine::general_purpose::STANDARD.encode(&jpeg);
                    let img = protocol_encoder.format_img_instruction(stream_id, 0, 0, 0, "image/jpeg");
                    if to_client.send(img.freeze()).await.is_err() {
                        break;
                    }
                    for blob in format_chunked_blobs(stream_id, &b64, None) {
                        if to_client.send(Bytes::from(blob)).await.is_err() {
                            break;
                        }
                    }
                    stream_id += 1;

                    let ts = current_time_millis().to_string();
                    let sync = format_instruction("sync", &[&ts]);
                    let _ = to_client.send(Bytes::from(sync)).await;
                }

                // Keyboard input from the Guacamole client
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        debug!("TN3270: Client disconnected");
                        break;
                    };
                    let msg_str = String::from_utf8_lossy(&msg);

                    if let Some(key) = parse_key_instruction(&msg_str) {
                        if !key.pressed {
                            continue;
                        }
                        if let Some(server_bytes) = handle_key(&mut screen, key.keysym) {
                            if let Err(e) = stream.write_all(&server_bytes).await {
                                warn!("TN3270: Write error: {}", e);
                                break;
                            }
                            dirty = true;
                        }
                    }
                    // size instruction: fixed 24×80 for now
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

// -- Key handling ------------------------------------------------------------

/// Convert a Guacamole X11 keysym to bytes to send to the TN3270 server.
///
/// Returns `None` for keys that only affect local state (Tab, character input)
/// and `Some(bytes)` for keys that require a network transmission (Enter, PF, Clear).
fn handle_key(screen: &mut ScreenBuffer, keysym: u32) -> Option<Vec<u8>> {
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

        // PA1–PA3 (program attention — do NOT include modified field data)
        0xFFE1 | 0xFF61 => Some(screen.read_modified_fields(Aid::Pa(1))),
        0xFFE2 | 0xFF62 => Some(screen.read_modified_fields(Aid::Pa(2))),
        0xFFE3 | 0xFF63 => Some(screen.read_modified_fields(Aid::Pa(3))),

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
