// WebSocketSink: streams encrypted fMP4 to the Keeper router.
//
// Buffers ciphertext until KROUTER_FRAME_SIZE (8MB) then flushes.
// On WebSocket disconnect, reconnects with exponential backoff.
// If reconnect fails after all retries, the session is terminated
// (recording failure is a hard stop for PAM — no audit trail = no session).

use crate::encryptor::Encryptor;
use crate::{
    Fmp4Writer, RecorderError, RecordingSink, Result, VideoRecordingConfig, KROUTER_FRAME_SIZE,
};
use async_trait::async_trait;
use bytes::BytesMut;
use futures_util::SinkExt;
use guacr_handlers::EncodedFrame;
use log::{debug, error, info, warn};
use std::collections::HashMap;
use std::time::Duration;
use tokio::net::TcpStream;
use tokio_tungstenite::tungstenite::client::IntoClientRequest;
use tokio_tungstenite::tungstenite::Message;
use tokio_tungstenite::{connect_async, MaybeTlsStream, WebSocketStream};

type Ws = WebSocketStream<MaybeTlsStream<TcpStream>>;

pub struct WebSocketSink {
    ws: Option<Ws>,
    // Option so we can take() it in finalize() to avoid partial-move issues
    encryptor: Option<Encryptor>,
    muxer: Fmp4Writer,
    url: String,
    headers: HashMap<String, String>,
    // BytesMut: pre-allocated, grows in-place, splits to Bytes (zero-copy send) at flush
    buffer: BytesMut,
    pending_events: Vec<(u64, String)>,
    session_start_ms: u64,
    reconnect_buffer: Vec<u8>,
}

impl WebSocketSink {
    pub async fn connect(config: VideoRecordingConfig) -> Result<Self> {
        let url = config
            .recording_router_url
            .clone()
            .ok_or_else(|| RecorderError::WebSocket("no router URL".into()))?;

        let ws = Self::connect_ws(&url, &config.recording_auth_headers).await?;

        let encryptor = Encryptor::new(
            &config.recording_secret,
            &config.recording_nonce,
            &config.recording_associated,
        )
        .map_err(|e: String| RecorderError::Encryption(e))?;

        let header = config.header_bytes();
        let session_start_ms = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis() as u64;

        let mut sink = Self {
            ws: Some(ws),
            encryptor: Some(encryptor),
            muxer: Fmp4Writer::new(1920, 1080),
            url,
            headers: config.recording_auth_headers,
            // Pre-allocate slightly above KROUTER_FRAME_SIZE to avoid realloc at flush boundary
            buffer: BytesMut::with_capacity(KROUTER_FRAME_SIZE + 65536),
            pending_events: Vec::new(),
            session_start_ms,
            reconnect_buffer: Vec::new(),
        };
        sink.send_raw(header).await?;
        info!("WebSocketSink: connected to {}", &sink.url);
        Ok(sink)
    }

    async fn connect_ws(url: &str, headers: &HashMap<String, String>) -> Result<Ws> {
        let mut req = url
            .into_client_request()
            .map_err(|e| RecorderError::WebSocket(e.to_string()))?;
        for (k, v) in headers {
            req.headers_mut().insert(
                k.parse::<tokio_tungstenite::tungstenite::http::HeaderName>()
                    .map_err(|e| RecorderError::WebSocket(e.to_string()))?,
                v.parse().map_err(
                    |e: tokio_tungstenite::tungstenite::http::header::InvalidHeaderValue| {
                        RecorderError::WebSocket(e.to_string())
                    },
                )?,
            );
        }
        let (ws, _) = connect_async(req)
            .await
            .map_err(|e| RecorderError::WebSocket(e.to_string()))?;
        Ok(ws)
    }

    async fn send_raw(&mut self, data: Vec<u8>) -> Result<()> {
        if let Some(ws) = &mut self.ws {
            ws.send(Message::Binary(bytes::Bytes::from(data)))
                .await
                .map_err(|e| RecorderError::WebSocket(e.to_string()))
        } else {
            Err(RecorderError::WebSocket("not connected".into()))
        }
    }

    /// Encrypt `data` in-place, then append to the outgoing buffer.
    /// Flushes automatically when the buffer reaches KROUTER_FRAME_SIZE.
    async fn write_encrypted(&mut self, mut data: Vec<u8>) -> Result<()> {
        self.encryptor
            .as_mut()
            .expect("encryptor used after finalize")
            .update_in_place(&mut data);
        self.buffer.extend_from_slice(&data);
        if self.buffer.len() >= KROUTER_FRAME_SIZE {
            self.flush_buffer().await?;
        }
        Ok(())
    }

    async fn flush_buffer(&mut self) -> Result<()> {
        if self.buffer.is_empty() {
            return Ok(());
        }
        // split_to gives us a zero-copy Bytes view; the BytesMut retains its capacity.
        let chunk = self.buffer.split().freeze();
        self.send_with_reconnect(chunk).await
    }

    async fn send_with_reconnect(&mut self, data: bytes::Bytes) -> Result<()> {
        if let Some(ws) = &mut self.ws {
            // Clone is O(1) — Bytes is Arc-backed; the underlying bytes are shared, not copied.
            match ws.send(Message::Binary(data.clone())).await {
                Ok(_) => return Ok(()),
                Err(e) => {
                    warn!("WebSocketSink: send failed ({}), reconnecting", e);
                    self.ws = None;
                    self.reconnect_buffer.extend_from_slice(&data);
                }
            }
        } else {
            self.reconnect_buffer.extend_from_slice(&data);
        }

        let mut delay = Duration::from_secs(1);
        for attempt in 1..=5 {
            tokio::time::sleep(delay).await;
            match Self::connect_ws(&self.url, &self.headers).await {
                Ok(new_ws) => {
                    self.ws = Some(new_ws);
                    info!("WebSocketSink: reconnected on attempt {}", attempt);
                    let buffered = bytes::Bytes::from(std::mem::take(&mut self.reconnect_buffer));
                    if !buffered.is_empty() {
                        if let Some(ws) = &mut self.ws {
                            if let Err(e) = ws.send(Message::Binary(buffered)).await {
                                error!("WebSocketSink: re-send after reconnect failed: {}", e);
                                self.ws = None;
                                continue;
                            }
                        }
                    }
                    return Ok(());
                }
                Err(e) => {
                    warn!("WebSocketSink: reconnect attempt {} failed: {}", attempt, e);
                    delay = (delay * 2).min(Duration::from_secs(30));
                }
            }
        }

        error!("WebSocketSink: all reconnect attempts exhausted");
        Err(RecorderError::Fatal(
            "Recording WebSocket could not reconnect after 5 attempts. Session terminated.".into(),
        ))
    }
}

#[async_trait]
impl RecordingSink for WebSocketSink {
    async fn write_frame(&mut self, frame: &EncodedFrame) -> Result<()> {
        if !self.muxer.is_initialized() {
            if !frame.is_keyframe {
                return Ok(());
            }
            match self.muxer.init_segment(&frame.data) {
                Some(init) => self.write_encrypted(init).await?,
                None => {
                    warn!("WebSocketSink: could not extract SPS/PPS from first IDR, dropping");
                    return Ok(());
                }
            }
        }

        if !self.pending_events.is_empty() {
            let events = std::mem::take(&mut self.pending_events);
            let data_frag = self.muxer.write_data_fragment(&events);
            if !data_frag.is_empty() {
                self.write_encrypted(data_frag).await?;
            }
        }

        let pts = frame.pts;
        let is_keyframe = frame.is_keyframe;
        if let Some(mp4_frame) = self.muxer.prepare_frame(&frame.data, pts, is_keyframe) {
            let video_frag = self.muxer.write_video_fragment(&mp4_frame);
            self.write_encrypted(video_frag).await?;
        }

        Ok(())
    }

    async fn write_input(&mut self, instruction: &str, timestamp_ms: u64) -> Result<()> {
        let relative_ms = timestamp_ms.saturating_sub(self.session_start_ms);
        self.pending_events
            .push((relative_ms, instruction.to_string()));
        Ok(())
    }

    async fn finalize(mut self: Box<Self>) -> Result<()> {
        // Flush remaining events
        if !self.pending_events.is_empty() {
            let events = std::mem::take(&mut self.pending_events);
            let data_frag = self.muxer.write_data_fragment(&events);
            if !data_frag.is_empty() {
                self.write_encrypted(data_frag).await?;
            }
        }

        self.flush_buffer().await?;

        // Take encryptor to finalize it (avoids partial-move on Box<Self>)
        let tag = self
            .encryptor
            .take()
            .expect("encryptor already consumed")
            .finalize();
        self.send_with_reconnect(bytes::Bytes::copy_from_slice(&tag))
            .await?;

        if let Some(mut ws) = self.ws.take() {
            let _ = ws.close(None).await;
        }

        debug!("WebSocketSink: finalized and closed");
        Ok(())
    }
}
