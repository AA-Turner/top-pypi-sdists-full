// RfbProxy is retained as a reference implementation for the direct RFB path.
// It is not currently used by the main VNC handler (which uses the direct protocol
// path via VncProtocol), but is kept for future RFB proxy mode work.
#![allow(dead_code)]

use crate::vnc_protocol::VncPixelFormat;
use base64::{engine::general_purpose::STANDARD as BASE64, Engine};
use bytes::Bytes;
use guacr_protocol::format_vnc_data;
use log::info;
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};
use tokio::sync::mpsc;

pub struct RfbProxy<S> {
    stream: S,
    to_client: mpsc::Sender<Bytes>,
    server_width: u16,
    server_height: u16,
    pixel_format: VncPixelFormat,
    server_name: String,
}

impl<S: AsyncRead + AsyncWrite + Unpin + Send> RfbProxy<S> {
    pub fn new(
        stream: S,
        to_client: mpsc::Sender<Bytes>,
        width: u16,
        height: u16,
        pixel_format: VncPixelFormat,
        server_name: String,
    ) -> Self {
        Self {
            stream,
            to_client,
            server_width: width,
            server_height: height,
            pixel_format,
            server_name,
        }
    }

    /// Synthesize the VNC server-side handshake for noVNC.
    /// Called once before run(). Consumes handshake messages from from_client,
    /// sends synthesized responses as vnc-data instructions.
    pub async fn synthesize_handshake(
        &mut self,
        from_client: &mut mpsc::Receiver<Bytes>,
    ) -> Result<(), String> {
        // 1. Send version
        self.send_vnc_data(b"RFB 003.008\n").await?;

        // 2. Read noVNC's version response (12 bytes via vnc-input)
        self.read_vnc_input_bytes(from_client, 12).await?;

        // 3. Send security types: 1 type available, type 1 = None (no auth)
        self.send_vnc_data(&[0x01, 0x01]).await?;

        // 4. Read security type choice (1 byte)
        self.read_vnc_input_bytes(from_client, 1).await?;

        // 5. Send security result: OK
        self.send_vnc_data(&[0x00, 0x00, 0x00, 0x00]).await?;

        // 6. Read ClientInit (1 byte)
        self.read_vnc_input_bytes(from_client, 1).await?;

        // 7. Send ServerInit
        let server_init = self.build_server_init();
        self.send_vnc_data(&server_init).await?;

        info!(
            "RFB: Handshake synthesized for noVNC ({}x{})",
            self.server_width, self.server_height
        );
        Ok(())
    }

    /// Main proxy loop: forward bytes between VNC server and browser.
    pub async fn run(&mut self, from_client: &mut mpsc::Receiver<Bytes>) -> Result<(), String> {
        let mut buf = vec![0u8; 65536];
        loop {
            tokio::select! {
                result = self.stream.read(&mut buf) => {
                    match result {
                        Ok(0) => {
                            info!("RFB: VNC server closed connection");
                            return Ok(());
                        }
                        Ok(n) => {
                            self.send_vnc_data(&buf[..n]).await?;
                        }
                        Err(e) => return Err(format!("RFB: VNC server read error: {}", e)),
                    }
                }
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("RFB: Browser disconnected");
                        return Ok(());
                    };
                    if let Some(rfb_bytes) = parse_vnc_input(&msg) {
                        self.stream
                            .write_all(&rfb_bytes)
                            .await
                            .map_err(|e| format!("RFB: VNC server write error: {}", e))?;
                    }
                }
            }
        }
    }

    async fn send_vnc_data(&self, bytes: &[u8]) -> Result<(), String> {
        self.to_client
            .send(format_vnc_data(bytes))
            .await
            .map_err(|e| format!("RFB: to_client send failed: {}", e))
    }

    /// Read exactly `n` bytes worth of vnc-input content from from_client.
    /// vnc-input messages may not align to expected byte counts, so accumulate.
    async fn read_vnc_input_bytes(
        &self,
        from_client: &mut mpsc::Receiver<Bytes>,
        n: usize,
    ) -> Result<Vec<u8>, String> {
        let mut accumulated = Vec::new();
        while accumulated.len() < n {
            let Some(msg) = from_client.recv().await else {
                return Err("RFB: browser disconnected during handshake".into());
            };
            if let Some(bytes) = parse_vnc_input(&msg) {
                accumulated.extend_from_slice(&bytes);
            }
        }
        Ok(accumulated)
    }

    fn build_server_init(&self) -> Vec<u8> {
        let pf = &self.pixel_format;
        let mut b = Vec::with_capacity(24 + self.server_name.len());
        b.extend_from_slice(&self.server_width.to_be_bytes());
        b.extend_from_slice(&self.server_height.to_be_bytes());
        // pixel format (16 bytes)
        b.push(pf.bits_per_pixel);
        b.push(pf.depth);
        b.push(if pf.big_endian { 1 } else { 0 });
        b.push(if pf.true_color { 1 } else { 0 });
        b.extend_from_slice(&pf.red_max.to_be_bytes());
        b.extend_from_slice(&pf.green_max.to_be_bytes());
        b.extend_from_slice(&pf.blue_max.to_be_bytes());
        b.push(pf.red_shift);
        b.push(pf.green_shift);
        b.push(pf.blue_shift);
        b.extend_from_slice(&[0u8; 3]); // padding
        let name = self.server_name.as_bytes();
        b.extend_from_slice(&(name.len() as u32).to_be_bytes());
        b.extend_from_slice(name);
        b
    }
}

/// Parse a vnc-input Guacamole instruction and return the raw RFB bytes.
/// Format: "9.vnc-input,<len>.<base64>;"
pub(crate) fn parse_vnc_input(msg: &[u8]) -> Option<Vec<u8>> {
    let s = std::str::from_utf8(msg).ok()?;
    // Must contain "vnc-input"
    let after = s.split_once("vnc-input,")?.1;
    // after = "<len>.<base64>;"
    let after_dot = after.split_once('.')?.1;
    let b64 = after_dot.trim_end_matches(';');
    BASE64.decode(b64).ok()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_vnc_input_roundtrip() {
        let input = b"\x01\x02\x03";
        let b64 = BASE64.encode(input);
        let instr = format!("9.vnc-input,{}.{};", b64.len(), b64);
        let parsed = parse_vnc_input(instr.as_bytes()).unwrap();
        assert_eq!(parsed, input);
    }

    #[test]
    fn test_parse_vnc_input_ignores_other_instructions() {
        let instr = b"3.key,2.65,1.1;";
        assert!(parse_vnc_input(instr).is_none());
    }

    #[test]
    fn test_build_server_init_length() {
        // ServerInit = 2+2+16+4+name = 24+name bytes
        let pf = VncPixelFormat::default();
        let name = "test";
        let (tx, _rx) = tokio::sync::mpsc::channel(1);
        let (stream, _other) = tokio::io::duplex(1024);
        let proxy = RfbProxy {
            stream,
            to_client: tx,
            server_width: 1920,
            server_height: 1080,
            pixel_format: pf,
            server_name: name.to_string(),
        };
        let bytes = proxy.build_server_init();
        assert_eq!(bytes.len(), 24 + name.len());
        assert_eq!(&bytes[0..2], &1920u16.to_be_bytes());
        assert_eq!(&bytes[2..4], &1080u16.to_be_bytes());
    }
}
