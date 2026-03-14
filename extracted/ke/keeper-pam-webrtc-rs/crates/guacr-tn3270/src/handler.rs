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
    connect_tcp_with_timeout, send_disconnect, send_name, send_ready, HandlerError, HandlerStats,
    HealthStatus, ProtocolHandler, VideoOutput,
};
use guacr_protocol::{format_chunked_blobs, format_instruction, TextProtocolEncoder};
use guacr_terminal::{parse_key_instruction, TerminalRenderer};
use log::{debug, info, warn};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::mpsc;

use crate::datastream::{parse_data_stream, Aid};
use crate::renderer;
use crate::screen::ScreenBuffer;

// -- Display constants -------------------------------------------------------

/// Default IBM 3270 Model 2: 24 rows × 80 columns.
const DEFAULT_ROWS: u16 = 24;
const DEFAULT_COLS: u16 = 80;
const CHAR_WIDTH: u32 = 9;
const CHAR_HEIGHT: u32 = 18;
const JPEG_QUALITY: u8 = 85;
/// 3270 screens change infrequently; 30 FPS is more than enough.
const RENDER_INTERVAL_MS: u64 = 33;

// -- TN3270 Telnet framing bytes ---------------------------------------------

const IAC: u8 = 0xFF;
const WILL: u8 = 0xFB;
const DO: u8 = 0xFD;
const SB: u8 = 0xFA;
const SE: u8 = 0xF0;
/// End-of-record marker: IAC EOR terminates each 3270 data record.
const EOR: u8 = 0xEF;
const OPT_BINARY: u8 = 0x00;
const OPT_TERMINAL_TYPE: u8 = 0x18;
const OPT_EOR: u8 = 0x19;

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
        let hostname = params
            .get("hostname")
            .ok_or_else(|| HandlerError::ConnectionFailed("Missing hostname".to_string()))?
            .clone();
        let port: u16 = params
            .get("port")
            .and_then(|p| p.parse().ok())
            .unwrap_or(3270);

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

                    let jpeg = match renderer::render_to_jpeg(&screen, CHAR_WIDTH, CHAR_HEIGHT, JPEG_QUALITY) {
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

                    let ts = std::time::SystemTime::now()
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap_or_default()
                        .as_millis()
                        .to_string();
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

// -- TN3270 record framing ---------------------------------------------------

/// Extract one complete TN3270 data record from the buffer.
///
/// Records are framed by `IAC EOR` (0xFF 0xEF). Telnet IAC option sequences
/// embedded in the stream are stripped transparently. `IAC IAC` is unescaped
/// to a literal `0xFF` byte inside record data.
///
/// Returns `Some(record_bytes)` and drains those bytes from the buffer, or
/// `None` if no complete record is available yet.
fn extract_record(buf: &mut Vec<u8>) -> Option<Vec<u8>> {
    let mut record = Vec::new();
    let mut i = 0;

    while i < buf.len() {
        if buf[i] != IAC {
            record.push(buf[i]);
            i += 1;
            continue;
        }

        // Need at least one more byte after IAC.
        if i + 1 >= buf.len() {
            return None; // Wait for more data — leave buffer intact.
        }

        match buf[i + 1] {
            EOR => {
                // End of record: drain consumed bytes and return.
                buf.drain(..i + 2);
                return Some(record);
            }
            IAC => {
                // IAC IAC → literal 0xFF inside record data.
                record.push(IAC);
                i += 2;
            }
            SB => {
                // Subnegotiation: IAC SB … IAC SE — skip entirely.
                i += 2;
                loop {
                    if i + 1 >= buf.len() {
                        return None; // Incomplete subnegotiation — wait.
                    }
                    if buf[i] == IAC && buf[i + 1] == SE {
                        i += 2;
                        break;
                    }
                    i += 1;
                }
            }
            _ => {
                // 3-byte IAC option command (DO/DONT/WILL/WONT + option).
                if i + 2 >= buf.len() {
                    return None; // Incomplete command — wait.
                }
                i += 3;
            }
        }
    }

    // No EOR seen yet — leave buffer intact for next call.
    None
}

// -- Tests -------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_handler_name() {
        assert_eq!(Tn3270Handler::new().name(), "tn3270");
    }

    #[test]
    fn test_extract_record_simple() {
        // Single complete record terminated by IAC EOR
        let mut buf = vec![0xF5, 0x40, IAC, EOR];
        let record = extract_record(&mut buf);
        assert_eq!(record, Some(vec![0xF5, 0x40]));
        assert!(buf.is_empty());
    }

    #[test]
    fn test_extract_record_incomplete() {
        // No EOR yet — should return None and leave buffer intact
        let mut buf = vec![0xF5, 0x40, 0xC8];
        assert!(extract_record(&mut buf).is_none());
    }

    #[test]
    fn test_extract_record_iac_escaped() {
        // IAC IAC in data should become a single 0xFF byte in the record
        let mut buf = vec![IAC, IAC, 0x42, IAC, EOR];
        let record = extract_record(&mut buf).unwrap();
        assert_eq!(record, vec![IAC, 0x42]);
        assert!(buf.is_empty());
    }

    #[test]
    fn test_extract_record_strips_telnet_option() {
        // IAC DO BINARY before the actual data — option should be stripped
        let mut buf = vec![IAC, DO, OPT_BINARY, 0xC8, IAC, EOR];
        let record = extract_record(&mut buf).unwrap();
        assert_eq!(record, vec![0xC8]);
    }

    #[test]
    fn test_extract_record_multiple() {
        // Two back-to-back records
        let mut buf = vec![0x01, IAC, EOR, 0x02, IAC, EOR];
        assert_eq!(extract_record(&mut buf), Some(vec![0x01]));
        assert_eq!(extract_record(&mut buf), Some(vec![0x02]));
        assert!(buf.is_empty());
    }

    #[tokio::test]
    async fn test_health_check() {
        let h = Tn3270Handler::new();
        assert!(h.health_check().await.is_ok());
    }
}
