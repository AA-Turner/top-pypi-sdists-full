// guacr-recorder: Video session recording pipeline
//
// Muxes H.264 frames into fragmented MP4, encrypts with AES-256-GCM using the
// same wire format as the Python gateway's StreamEncryptor, and uploads to the
// Keeper router via WebSocket.
//
// Wire format (matches Python RecordingReader.__init__):
//   [4-byte BE: len(assoc_data)] [assoc_data JSON] [0x3B] [12-byte nonce]
//   [AES-256-GCM ciphertext, streaming...] [16-byte GCM tag]
//
// Sinks flush to their destination when the buffer reaches KROUTER_FRAME_SIZE.

pub mod dual_sink;
mod encryptor;
pub mod file_sink;
mod key_setup;
mod mp4;
pub mod typescript_sink;
pub mod websocket_sink;

pub use key_setup::build_recording_params;

pub use dual_sink::DualSink;
pub use encryptor::Encryptor;
pub use file_sink::FileSink;
pub use mp4::Fmp4Writer;
pub use typescript_sink::{build_terminal_sink, TerminalRecordingConfig, TypescriptSink};
pub use websocket_sink::WebSocketSink;

use async_trait::async_trait;
use guacr_handlers::EncodedFrame;
use std::collections::HashMap;
use thiserror::Error;

/// Must match Python's KROUTER_FRAME_SIZE = 8 * 1024 * 1024
pub const KROUTER_FRAME_SIZE: usize = 8 * 1024 * 1024;

#[derive(Debug, Error)]
pub enum RecorderError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("WebSocket error: {0}")]
    WebSocket(String),
    #[error("Encryption error: {0}")]
    Encryption(String),
    #[error("MP4 muxer error: {0}")]
    Mp4(String),
    #[error("Recording failed, session terminated: {0}")]
    Fatal(String),
}

pub type Result<T> = std::result::Result<T, RecorderError>;

/// Trait for recording sinks. Receives encoded H.264 frames and serialized
/// Guacamole input instructions for embedding in the MP4 data track.
#[async_trait]
pub trait RecordingSink: Send + Sync {
    /// Write an encoded H.264 frame to the recording.
    async fn write_frame(&mut self, frame: &EncodedFrame) -> Result<()>;

    /// Write a Guacamole input instruction (key/mouse) to the embedded data track.
    /// `timestamp_ms` is wall-clock milliseconds since session start.
    async fn write_input(&mut self, instruction: &str, timestamp_ms: u64) -> Result<()>;

    /// Finalize the recording: flush remaining data, append GCM tag, close connection.
    /// Consumes self.
    async fn finalize(self: Box<Self>) -> Result<()>;
}

/// Configuration for video recording, parsed from connection params.
///
/// Python gateway passes these as a flat string map (same style as guacd params).
#[derive(Debug, Clone)]
pub struct VideoRecordingConfig {
    /// AES-256 key for stream encryption (32 bytes, base64-encoded).
    pub recording_secret: Vec<u8>,
    /// AES-GCM nonce (12 bytes, base64-encoded).
    pub recording_nonce: Vec<u8>,
    /// JSON metadata (base64-encoded) — authenticated as GCM AAD.
    pub recording_associated: Vec<u8>,
    /// WebSocket URL for router upload, e.g. "wss://router.example.com/api/device/recording/..."
    pub recording_router_url: Option<String>,
    /// Auth headers for the WebSocket connection (Challenge, Signature, Authorization).
    pub recording_auth_headers: HashMap<String, String>,
    /// Optional local file path for FileSink / DualSink.
    pub recording_file_path: Option<std::path::PathBuf>,
    /// Destination selection.
    pub destination: RecordingDestination,
}

#[derive(Debug, Clone, PartialEq)]
pub enum RecordingDestination {
    Router,
    File,
    Both,
}

impl VideoRecordingConfig {
    /// Parse from connection params (flat string map from Python gateway).
    ///
    /// **Preferred (key-bytes style)** — Python passes raw Vault key bytes;
    /// Rust generates the recording secret and builds all metadata:
    ///
    ///   "resource_key_bytes"           → base64(resource_record.record_key_bytes)
    ///   "user_key_bytes"               → base64(user_record.record_key_bytes)  \[optional\]
    ///   "resource_uid"                 → Keeper vault resource record UID
    ///   "user_uid"                     → Keeper vault user UID  \[optional\]
    ///   "conversation_uid"             → session/conversation identifier
    ///   "recording_router_base_url"    → wss://router.example.com
    ///   "recording_auth_challenge"     → Challenge header
    ///   "recording_auth_signature"     → Signature header
    ///   "recording_auth_authorization" → Authorization header
    ///   "hostname", "port", "username" → already in connection params
    ///   "protocol"                     → "rdp" / "vnc" / "rbi"  (optional, defaults "rdp")
    ///   "recordingpath"                → local file directory  \[optional\]
    ///   "recordingname"                → filename stem  \[optional\]
    ///
    /// **Legacy (pre-computed style)** — Python pre-computes everything and passes:
    ///   "recording_secret", "recording_nonce", "recording_associated",
    ///   "recording_router_url", auth headers.
    pub fn from_params(params: &HashMap<String, String>) -> Option<Self> {
        if params.contains_key("resource_key_bytes") {
            Self::from_key_bytes(params)
        } else if params.contains_key("recording_secret") {
            Self::from_precomputed(params)
        } else {
            None
        }
    }

    /// Key-bytes style: Rust generates the recording secret and builds all metadata.
    fn from_key_bytes(params: &HashMap<String, String>) -> Option<Self> {
        use base64::Engine;
        let b64 = base64::engine::general_purpose::STANDARD;

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
        let protocol = params.get("protocol").map(|s| s.as_str()).unwrap_or("rdp");

        let (recording_secret, recording_nonce, recording_associated) =
            key_setup::build_recording_params(
                &resource_key_bytes,
                user_key_bytes.as_deref(),
                conversation_uid,
                resource_uid,
                user_uid,
                hostname,
                port,
                username,
                "mp4",
            );

        let recording_auth_headers = Self::parse_auth_headers(params);

        let recording_router_url = params.get("recording_router_base_url").map(|base_url| {
            let endpoint_url_safe = make_url_safe(conversation_uid);
            format!(
                "{}/api/device/recording/{}/{}/mp4",
                base_url.trim_end_matches('/'),
                endpoint_url_safe,
                protocol,
            )
        });

        let recording_file_path = params.get("recordingpath").map(|dir| {
            let name = params
                .get("recordingname")
                .map(|s| s.as_str())
                .unwrap_or("recording");
            std::path::PathBuf::from(dir).join(format!("{}.mp4", name))
        });

        let destination = match (
            recording_router_url.is_some(),
            recording_file_path.is_some(),
        ) {
            (true, true) => RecordingDestination::Both,
            (true, false) => RecordingDestination::Router,
            (false, true) => RecordingDestination::File,
            (false, false) => return None,
        };

        Some(Self {
            recording_secret,
            recording_nonce,
            recording_associated,
            recording_router_url,
            recording_auth_headers,
            recording_file_path,
            destination,
        })
    }

    /// Legacy style: Python pre-computed all crypto params.
    fn from_precomputed(params: &HashMap<String, String>) -> Option<Self> {
        use base64::Engine;
        let b64 = base64::engine::general_purpose::STANDARD;

        let recording_secret = b64.decode(params.get("recording_secret")?).ok()?;
        let recording_nonce = b64.decode(params.get("recording_nonce")?).ok()?;
        let recording_associated = b64.decode(params.get("recording_associated")?).ok()?;

        if recording_secret.len() != 32 || recording_nonce.len() != 12 {
            return None;
        }

        let recording_router_url = params.get("recording_router_url").cloned();
        let recording_auth_headers = Self::parse_auth_headers(params);

        let recording_file_path = params.get("recordingpath").map(|dir| {
            let name = params
                .get("recordingname")
                .map(|s| s.as_str())
                .unwrap_or("recording");
            std::path::PathBuf::from(dir).join(format!("{}.mp4", name))
        });

        let destination = match (
            recording_router_url.is_some(),
            recording_file_path.is_some(),
        ) {
            (true, true) => RecordingDestination::Both,
            (true, false) => RecordingDestination::Router,
            (false, true) => RecordingDestination::File,
            (false, false) => return None,
        };

        Some(Self {
            recording_secret,
            recording_nonce,
            recording_associated,
            recording_router_url,
            recording_auth_headers,
            recording_file_path,
            destination,
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

    /// Build the recording header bytes prepended before the ciphertext.
    ///
    /// Format (matches Python RecordingReader.__init__):
    ///   \[4-byte BE: len(assoc)\] \[assoc bytes\] \[0x3B\] \[12-byte nonce\]
    pub fn header_bytes(&self) -> Vec<u8> {
        let assoc_len = self.recording_associated.len() as u32;
        let mut hdr = Vec::with_capacity(4 + assoc_len as usize + 1 + 12);
        hdr.extend_from_slice(&assoc_len.to_be_bytes());
        hdr.extend_from_slice(&self.recording_associated);
        hdr.push(b';');
        hdr.extend_from_slice(&self.recording_nonce);
        hdr
    }
}

/// URL-safe base64 encoding of a string, matching Python's make_urlsafe_base64.
fn make_url_safe(s: &str) -> String {
    use base64::Engine;
    base64::engine::general_purpose::URL_SAFE_NO_PAD.encode(s.as_bytes())
}

/// Build the appropriate RecordingSink from config.
#[cfg(test)]
mod tests;

pub async fn build_sink(config: VideoRecordingConfig) -> Result<Box<dyn RecordingSink>> {
    let dest = config.destination.clone();
    match dest {
        RecordingDestination::File => {
            let path = config.recording_file_path.clone().unwrap();
            let sink = FileSink::new(config, path).await?;
            Ok(Box::new(sink) as Box<dyn RecordingSink>)
        }
        RecordingDestination::Router => {
            let sink = WebSocketSink::connect(config).await?;
            Ok(Box::new(sink) as Box<dyn RecordingSink>)
        }
        RecordingDestination::Both => {
            let path = config.recording_file_path.clone().unwrap();
            let file = FileSink::new(config.clone(), path).await?;
            let ws = WebSocketSink::connect(config).await?;
            Ok(Box::new(DualSink::new(ws, file)) as Box<dyn RecordingSink>)
        }
    }
}
