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
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::mpsc;

use crate::datastream::{
    aid_byte_for_key, build_response_record, encode_address, parse_5250_record,
};
use crate::renderer;
use crate::screen::ScreenBuffer5250;

const CHAR_WIDTH: u32 = 9;
const CHAR_HEIGHT: u32 = 18;
const JPEG_QUALITY: u8 = 85;
const RENDER_INTERVAL_MS: u64 = 33; // 30 FPS

// Standard AS/400 screen sizes
const DEFAULT_ROWS: u16 = 24;
const DEFAULT_COLS: u16 = 80;

// Telnet framing (identical to TN3270)
const IAC: u8 = 0xFF;
const WILL: u8 = 0xFB;
const DO: u8 = 0xFD;
const SB: u8 = 0xFA;
const SE: u8 = 0xF0;
const EOR: u8 = 0xEF;
const OPT_BINARY: u8 = 0x00;
const OPT_TERMINAL_TYPE: u8 = 0x18;
const OPT_EOR: u8 = 0x19;

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
    ) -> guacr_handlers::Result<()> {
        let hostname = params
            .get("hostname")
            .ok_or_else(|| HandlerError::ConnectionFailed("Missing hostname".to_string()))?
            .clone();
        let port: u16 = params
            .get("port")
            .and_then(|p| p.parse().ok())
            .unwrap_or(23); // AS/400 TN5250 default port

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

        let pixel_width = cols as u32 * CHAR_WIDTH;
        let pixel_height = rows as u32 * CHAR_HEIGHT;

        // Session startup
        send_ready(&to_client, "tn5250").await?;
        send_name(&to_client, &format!("TN5250 \u{2014} {}", hostname)).await?;
        let size_instr = TerminalRenderer::format_size_instruction(0, pixel_width, pixel_height);
        to_client
            .send(Bytes::from(size_instr))
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

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
        let mut protocol_encoder = TextProtocolEncoder::new();
        let mut stream_id = 1u32;
        let mut dirty = false;
        let mut pending: Vec<u8> = Vec::with_capacity(8192);
        let mut net_buf = vec![0u8; 4096];

        let mut render_timer =
            tokio::time::interval(tokio::time::Duration::from_millis(RENDER_INTERVAL_MS));
        render_timer.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

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

                _ = render_timer.tick() => {
                    if !dirty {
                        continue;
                    }
                    dirty = false;

                    let jpeg = match renderer::render_to_jpeg(&screen, CHAR_WIDTH, CHAR_HEIGHT, JPEG_QUALITY) {
                        Ok(j) => j,
                        Err(e) => {
                            warn!("TN5250: Render error: {}", e);
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
                    let _ = to_client.send(Bytes::from(format_instruction("sync", &[&ts]))).await;
                }

                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        debug!("TN5250: Client disconnected");
                        break;
                    };
                    let msg_str = String::from_utf8_lossy(&msg);

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

// ---------------------------------------------------------------------------
// TN5250 record framing (identical to TN3270)
// ---------------------------------------------------------------------------

fn extract_record(buf: &mut Vec<u8>) -> Option<Vec<u8>> {
    let mut record = Vec::new();
    let mut i = 0;

    while i < buf.len() {
        if buf[i] != IAC {
            record.push(buf[i]);
            i += 1;
            continue;
        }
        if i + 1 >= buf.len() {
            return None;
        }
        match buf[i + 1] {
            EOR => {
                buf.drain(..i + 2);
                return Some(record);
            }
            IAC => {
                record.push(IAC);
                i += 2;
            }
            SB => {
                i += 2;
                loop {
                    if i + 1 >= buf.len() {
                        return None;
                    }
                    if buf[i] == IAC && buf[i + 1] == SE {
                        i += 2;
                        break;
                    }
                    i += 1;
                }
            }
            _ => {
                if i + 2 >= buf.len() {
                    return None;
                }
                i += 3;
            }
        }
    }
    None
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_handler_name() {
        assert_eq!(Tn5250Handler::new().name(), "tn5250");
    }

    #[test]
    fn test_extract_record_simple() {
        let mut buf = vec![0x00, 0x07, 0x00, 0x00, 0x01, IAC, EOR];
        let record = extract_record(&mut buf).unwrap();
        assert_eq!(record, vec![0x00, 0x07, 0x00, 0x00, 0x01]);
        assert!(buf.is_empty());
    }

    #[test]
    fn test_extract_record_incomplete() {
        let mut buf = vec![0x00, 0x07, 0x00];
        assert!(extract_record(&mut buf).is_none());
    }

    #[tokio::test]
    async fn test_health_check() {
        assert!(Tn5250Handler::new().health_check().await.is_ok());
    }
}
