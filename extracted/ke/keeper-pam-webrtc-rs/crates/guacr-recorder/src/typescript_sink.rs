// TypescriptSink: streams encrypted typescript + timing files to the Keeper router.
//
// Terminal sessions record in typescript format — not fMP4:
//   .tys file  : raw PTY output bytes concatenated (same as guacd produces)
//   .timing file: one line per write: "elapsed_seconds byte_count\n" (scriptreplay format)
//
// Each stream (tys, timing) gets its own Encryptor instance with its own key/nonce pair,
// both generated from the same resource_key_bytes source via build_recording_params.
//
// Wire format is identical to the video path (see websocket_sink.rs).

use crate::encryptor::Encryptor;
use crate::{RecorderError, Result, KROUTER_FRAME_SIZE};
use bytes::BytesMut;
use futures_util::SinkExt;
use log::{debug, error, info, warn};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use tokio::net::TcpStream;
use tokio_tungstenite::tungstenite::client::IntoClientRequest;
use tokio_tungstenite::tungstenite::Message;
use tokio_tungstenite::{connect_async, MaybeTlsStream, WebSocketStream};

type Ws = WebSocketStream<MaybeTlsStream<TcpStream>>;

/// One WebSocket stream — either the .tys or .timing endpoint.
struct StreamChannel {
    ws: Option<Ws>,
    encryptor: Option<Encryptor>,
    url: String,
    headers: HashMap<String, String>,
    buffer: BytesMut,
    reconnect_buffer: Vec<u8>,
}

impl StreamChannel {
    async fn connect(
        url: String,
        headers: HashMap<String, String>,
        secret: &[u8],
        nonce: &[u8],
        associated: &[u8],
    ) -> Result<Self> {
        let ws = Self::connect_ws(&url, &headers).await?;

        let encryptor =
            Encryptor::new(secret, nonce, associated).map_err(RecorderError::Encryption)?;

        // Write the unencrypted header before ciphertext: [4-byte BE len][assoc][0x3B][12-byte nonce]
        let header = {
            let assoc_len = associated.len() as u32;
            let mut hdr = Vec::with_capacity(4 + associated.len() + 1 + 12);
            hdr.extend_from_slice(&assoc_len.to_be_bytes());
            hdr.extend_from_slice(associated);
            hdr.push(b';');
            hdr.extend_from_slice(nonce);
            hdr
        };

        let mut ch = Self {
            ws: Some(ws),
            encryptor: Some(encryptor),
            url,
            headers,
            buffer: BytesMut::with_capacity(KROUTER_FRAME_SIZE + 65536),
            reconnect_buffer: Vec::new(),
        };
        ch.send_raw(header).await?;
        Ok(ch)
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

    /// Encrypt `data` in-place, buffer it, and auto-flush at KROUTER_FRAME_SIZE.
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

    /// Zero-copy variant: copies `data` directly into the outgoing buffer and
    /// encrypts in-place, avoiding the intermediate Vec allocation.
    async fn write_encrypted_slice(&mut self, data: &[u8]) -> Result<()> {
        let start = self.buffer.len();
        self.buffer.extend_from_slice(data);
        self.encryptor
            .as_mut()
            .expect("encryptor used after finalize")
            .update_in_place(&mut self.buffer[start..]);
        if self.buffer.len() >= KROUTER_FRAME_SIZE {
            self.flush_buffer().await?;
        }
        Ok(())
    }

    async fn flush_buffer(&mut self) -> Result<()> {
        if self.buffer.is_empty() {
            return Ok(());
        }
        let chunk = self.buffer.split().freeze();
        self.send_with_reconnect(chunk).await
    }

    async fn send_with_reconnect(&mut self, data: bytes::Bytes) -> Result<()> {
        if let Some(ws) = &mut self.ws {
            match ws.send(Message::Binary(data.clone())).await {
                Ok(_) => return Ok(()),
                Err(e) => {
                    warn!("TypescriptSink: send failed ({}), reconnecting", e);
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
                    info!(
                        "TypescriptSink: reconnected {} on attempt {}",
                        self.url, attempt
                    );
                    let buffered = bytes::Bytes::from(std::mem::take(&mut self.reconnect_buffer));
                    if !buffered.is_empty() {
                        if let Some(ws) = &mut self.ws {
                            if let Err(e) = ws.send(Message::Binary(buffered)).await {
                                error!("TypescriptSink: re-send after reconnect failed: {}", e);
                                self.ws = None;
                                continue;
                            }
                        }
                    }
                    return Ok(());
                }
                Err(e) => {
                    warn!(
                        "TypescriptSink: reconnect attempt {} failed: {}",
                        attempt, e
                    );
                    delay = (delay * 2).min(Duration::from_secs(30));
                }
            }
        }

        error!("TypescriptSink: all reconnect attempts exhausted");
        Err(RecorderError::Fatal(
            "Recording WebSocket could not reconnect after 5 attempts. Session terminated.".into(),
        ))
    }

    /// Finalize: flush remaining buffer, append GCM tag, close connection.
    async fn finalize(&mut self) -> Result<()> {
        self.flush_buffer().await?;

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
        Ok(())
    }
}

/// Encrypted typescript session recorder.
///
/// Maintains two WebSocket connections to the router:
///   `{base_url}/api/device/recording/{uid}/{protocol}/tys`    — raw PTY bytes
///   `{base_url}/api/device/recording/{uid}/{protocol}/timing` — scriptreplay timing
///
/// Each stream uses a separate `Encryptor` instance (distinct key/nonce pair) so
/// the two ciphertext streams are independent. Created via `build_terminal_sink`.
pub struct TypescriptSink {
    tys_channel: StreamChannel,
    timing_channel: StreamChannel,
    session_start: Instant,
}

impl TypescriptSink {
    /// Connect both channels.
    pub(crate) async fn connect(config: TerminalRecordingConfig) -> Result<Self> {
        info!(
            "TypescriptSink: connecting tys={} timing={}",
            config.tys_url, config.timing_url
        );

        let tys_channel = StreamChannel::connect(
            config.tys_url,
            config.auth_headers.clone(),
            &config.tys_secret,
            &config.tys_nonce,
            &config.tys_associated,
        )
        .await?;

        let timing_channel = StreamChannel::connect(
            config.timing_url,
            config.auth_headers,
            &config.timing_secret,
            &config.timing_nonce,
            &config.timing_associated,
        )
        .await?;

        Ok(Self {
            tys_channel,
            timing_channel,
            session_start: Instant::now(),
        })
    }

    /// Record a chunk of raw PTY output.
    ///
    /// Encrypts the bytes and writes them to the `.tys` stream.
    /// Also records a timing entry `"{elapsed:.4} {len}\n"` on the `.timing` stream.
    pub async fn write_pty_output(&mut self, data: &[u8]) -> Result<()> {
        if data.is_empty() {
            return Ok(());
        }

        // Write raw PTY bytes to the .tys stream — zero-copy: encrypts directly into buffer
        self.tys_channel.write_encrypted_slice(data).await?;

        // Write timing entry: "elapsed_seconds byte_count\n"
        let elapsed = self.session_start.elapsed().as_secs_f64();
        let timing_line = format!("{:.4} {}\n", elapsed, data.len());
        self.timing_channel
            .write_encrypted(timing_line.into_bytes())
            .await?;

        Ok(())
    }

    /// Finalize both streams: flush, append GCM tags, close connections.
    pub async fn finalize(mut self) -> Result<()> {
        self.tys_channel.finalize().await?;
        self.timing_channel.finalize().await?;
        debug!("TypescriptSink: finalized both channels");
        Ok(())
    }
}

/// Configuration for encrypted terminal (typescript) recording.
///
/// Parsed from the same connection params as `VideoRecordingConfig`.
/// Each stream (tys, timing) uses independently generated crypto material.
#[derive(Debug, Clone)]
pub struct TerminalRecordingConfig {
    /// Router WebSocket URL for the .tys stream.
    pub tys_url: String,
    /// Router WebSocket URL for the .timing stream.
    pub timing_url: String,
    /// Auth headers (same for both streams).
    pub auth_headers: HashMap<String, String>,

    // Crypto material for the .tys stream
    pub tys_secret: Vec<u8>,
    pub tys_nonce: Vec<u8>,
    pub tys_associated: Vec<u8>,

    // Crypto material for the .timing stream
    pub timing_secret: Vec<u8>,
    pub timing_nonce: Vec<u8>,
    pub timing_associated: Vec<u8>,
}

impl TerminalRecordingConfig {
    /// Parse from connection params.
    ///
    /// Returns `None` when the params do not contain recording credentials or a
    /// `recording_router_base_url`.  In that case the handler skips upload silently.
    ///
    /// Accepted params (same style as `VideoRecordingConfig::from_params`):
    ///   "resource_key_bytes"           — base64(resource_record.record_key_bytes)
    ///   "user_key_bytes"               — base64(user_record.record_key_bytes)  \[optional\]
    ///   "resource_uid"                 — Keeper vault resource record UID
    ///   "user_uid"                     — Keeper vault user UID  \[optional\]
    ///   "conversation_uid"             — session/conversation identifier
    ///   "recording_router_base_url"    — wss://router.example.com
    ///   "recording_auth_challenge"     — Challenge header
    ///   "recording_auth_signature"     — Signature header
    ///   "recording_auth_authorization" — Authorization header
    ///   "hostname", "port", "username" — already in connection params
    ///   "protocol"                     — "ssh" / "telnet"  (optional, defaults "ssh")
    pub fn from_params(params: &HashMap<String, String>) -> Option<Self> {
        use base64::Engine;
        let b64 = base64::engine::general_purpose::STANDARD;

        let base_url = params.get("recording_router_base_url")?;

        if !params.contains_key("resource_key_bytes") {
            return None;
        }

        let resource_key_bytes = b64.decode(params.get("resource_key_bytes")?).ok()?;
        let user_key_bytes = params
            .get("user_key_bytes")
            .filter(|s| !s.is_empty())
            .and_then(|s| b64.decode(s).ok());

        let conversation_uid = params
            .get("conversation_uid")
            .map(|s| s.as_str())
            .unwrap_or("unknown");
        let resource_uid = params.get("resource_uid").map(|s| s.as_str()).unwrap_or("");
        let user_uid = params
            .get("user_uid")
            .filter(|s| !s.is_empty())
            .map(|s| s.as_str());
        let hostname = params.get("hostname").map(|s| s.as_str()).unwrap_or("");
        let port = params.get("port").map(|s| s.as_str()).unwrap_or("");
        let username = params.get("username").map(|s| s.as_str()).unwrap_or("");
        let protocol = params.get("protocol").map(|s| s.as_str()).unwrap_or("ssh");

        // Generate independent crypto material for each stream.
        let (tys_secret, tys_nonce, tys_associated) = crate::build_recording_params(
            &resource_key_bytes,
            user_key_bytes.as_deref(),
            conversation_uid,
            resource_uid,
            user_uid,
            hostname,
            port,
            username,
            "tys",
        );

        let (timing_secret, timing_nonce, timing_associated) = crate::build_recording_params(
            &resource_key_bytes,
            user_key_bytes.as_deref(),
            conversation_uid,
            resource_uid,
            user_uid,
            hostname,
            port,
            username,
            "timing",
        );

        let auth_headers = Self::parse_auth_headers(params);

        let base = base_url.trim_end_matches('/');
        let uid_safe = make_url_safe(conversation_uid);

        let tys_url = format!(
            "{}/api/device/recording/{}/{}/tys",
            base, uid_safe, protocol
        );
        let timing_url = format!(
            "{}/api/device/recording/{}/{}/timing",
            base, uid_safe, protocol
        );

        Some(Self {
            tys_url,
            timing_url,
            auth_headers,
            tys_secret,
            tys_nonce,
            tys_associated,
            timing_secret,
            timing_nonce,
            timing_associated,
        })
    }

    fn parse_auth_headers(params: &HashMap<String, String>) -> HashMap<String, String> {
        let mut headers = HashMap::new();
        for (param_key, header_name) in &[
            ("recording_auth_challenge", "Challenge"),
            ("recording_auth_signature", "Signature"),
            ("recording_auth_authorization", "Authorization"),
        ] {
            if let Some(v) = params.get(*param_key) {
                headers.insert(header_name.to_string(), v.clone());
            }
        }
        headers
    }
}

/// URL-safe base64 encoding of a string, matching Python's make_urlsafe_base64.
fn make_url_safe(s: &str) -> String {
    use base64::Engine;
    base64::engine::general_purpose::URL_SAFE_NO_PAD.encode(s.as_bytes())
}

/// Build a `TypescriptSink` from connection params.
///
/// Returns `None` when the params do not contain the necessary recording keys
/// (e.g. `resource_key_bytes` or `recording_router_base_url` is absent).
/// Handlers should skip upload silently in that case.
pub async fn build_terminal_sink(
    params: &HashMap<String, String>,
) -> Result<Option<TypescriptSink>> {
    match TerminalRecordingConfig::from_params(params) {
        None => Ok(None),
        Some(config) => {
            let sink = TypescriptSink::connect(config).await?;
            Ok(Some(sink))
        }
    }
}
