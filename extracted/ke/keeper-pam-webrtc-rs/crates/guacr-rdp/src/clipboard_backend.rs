// RDP CLIPRDR backend implementation (T-028 to T-031)
//
// Implements CliprdrBackend to enable client-to-server clipboard forwarding.
//
// AC-1: Text from the Guacamole client is forwarded to the RDP session.
// AC-2: Unicode text preserved through the clipboard round-trip (CF_UNICODETEXT/UTF-16LE).
// AC-3: Format negotiation (Format List + Format Data Request/Response) completes.
// AC-4: Graceful fallback if channel unavailable — attach is best-effort.

use ironrdp::cliprdr::backend::{ClipboardMessage, ClipboardMessageProxy, CliprdrBackend};
use ironrdp::cliprdr::pdu::{
    ClipboardFormat, ClipboardFormatId, ClipboardGeneralCapabilityFlags, FileContentsRequest,
    FileContentsResponse, FormatDataRequest, FormatDataResponse, LockDataId,
    OwnedFormatDataResponse,
};
use ironrdp_core::impl_as_any;
use log::{debug, info, warn};
use parking_lot::Mutex;
use std::sync::Arc;

/// CF_UNICODETEXT: Windows clipboard format for UTF-16LE text.
const CF_UNICODETEXT: u32 = 13;

/// Shared clipboard state between the CLIPRDR backend and the main RDP loop.
#[derive(Default, Debug)]
pub struct PendingClipboardData {
    /// UTF-8 text from the Guacamole client, waiting to be forwarded to RDP server.
    pub client_text: Option<String>,
    /// UTF-8 text from the RDP server, waiting to be forwarded to Guacamole client.
    pub server_text: Option<String>,
}

impl PendingClipboardData {
    pub fn new() -> Self {
        Self::default()
    }
}

/// Tokio unbounded mpsc ClipboardMessageProxy — Send + Sync, safe across await points.
#[derive(Debug)]
struct TokioProxy(tokio::sync::mpsc::UnboundedSender<ClipboardMessage>);

impl ClipboardMessageProxy for TokioProxy {
    fn send_clipboard_message(&self, message: ClipboardMessage) {
        // UnboundedSender::send is sync (no await) — safe to call from non-async context.
        let _ = self.0.send(message);
    }
}

/// IronRDP CLIPRDR backend for Guacamole RDP.
#[derive(Debug)]
pub struct GuacrCliprdrBackend {
    /// Shared clipboard state with the main loop.
    data: Arc<Mutex<PendingClipboardData>>,
    /// Proxy to send events to the main loop.
    proxy: Arc<TokioProxy>,
    /// Temp dir for file clipboard (required by the trait).
    temp_dir: String,
}

impl_as_any!(GuacrCliprdrBackend);

impl CliprdrBackend for GuacrCliprdrBackend {
    fn temporary_directory(&self) -> &str {
        &self.temp_dir
    }

    fn client_capabilities(&self) -> ClipboardGeneralCapabilityFlags {
        ClipboardGeneralCapabilityFlags::USE_LONG_FORMAT_NAMES
    }

    fn on_ready(&mut self) {
        info!("CLIPRDR: Channel ready");
        // If we already have client text, advertise it.
        let has_data = self.data.lock().client_text.is_some();
        if has_data {
            self.advertise_client_formats();
        }
    }

    fn on_request_format_list(&mut self) {
        // Server is asking us to (re)advertise our clipboard formats (AC-3).
        debug!("CLIPRDR: Server requested format list — advertising CF_UNICODETEXT");
        self.advertise_client_formats();
    }

    fn on_process_negotiated_capabilities(
        &mut self,
        capabilities: ClipboardGeneralCapabilityFlags,
    ) {
        debug!("CLIPRDR: Negotiated capabilities: {capabilities:?}");
    }

    fn on_remote_copy(&mut self, available_formats: &[ClipboardFormat]) {
        // Server has new clipboard data in these formats.
        debug!(
            "CLIPRDR: Server has {} clipboard formats",
            available_formats.len()
        );
        if available_formats
            .iter()
            .any(|f| f.id().value() == CF_UNICODETEXT)
        {
            // Request the text data from the server.
            let _ = self
                .proxy
                .0
                .send(ClipboardMessage::SendInitiatePaste(ClipboardFormatId::new(
                    CF_UNICODETEXT,
                )));
        }
    }

    fn on_format_data_request(&mut self, request: FormatDataRequest) {
        // Server is requesting clipboard data in a specific format (AC-3).
        let format_id = request.format.value();
        debug!("CLIPRDR: Server requested format data: format_id={format_id}");

        let response = if format_id == CF_UNICODETEXT {
            if let Some(text) = self.data.lock().client_text.clone() {
                // AC-2: Convert UTF-8 → UTF-16LE (Windows CF_UNICODETEXT format).
                let mut utf16: Vec<u8> =
                    text.encode_utf16().flat_map(|c| c.to_le_bytes()).collect();
                // Append null terminator (required by Windows clipboard spec).
                utf16.extend_from_slice(&[0u8, 0u8]);
                info!(
                    "CLIPRDR: Responding with {} UTF-16LE bytes (AC-1)",
                    utf16.len()
                );
                OwnedFormatDataResponse::new_data(utf16)
            } else {
                warn!("CLIPRDR: No client clipboard text available");
                OwnedFormatDataResponse::new_error()
            }
        } else {
            debug!("CLIPRDR: Unsupported format {format_id}");
            OwnedFormatDataResponse::new_error()
        };

        // Route the response through the proxy to the main loop.
        let _ = self
            .proxy
            .0
            .send(ClipboardMessage::SendFormatData(response));
    }

    fn on_format_data_response(&mut self, response: FormatDataResponse<'_>) {
        // Server sent us clipboard data (server-to-client direction).
        let data = response.data();
        if !data.is_empty() {
            // AC-2: Decode UTF-16LE → UTF-8.
            let u16_vals: Vec<u16> = data
                .chunks_exact(2)
                .map(|b| u16::from_le_bytes([b[0], b[1]]))
                .collect();
            let text = String::from_utf16_lossy(&u16_vals);
            let text = text.trim_end_matches('\0').to_string();
            info!(
                "CLIPRDR: Received {} chars from server clipboard",
                text.len()
            );
            self.data.lock().server_text = Some(text);
        }
    }

    fn on_file_contents_request(&mut self, _request: FileContentsRequest) {}

    fn on_file_contents_response(&mut self, _response: FileContentsResponse<'_>) {}

    fn on_lock(&mut self, _data_id: LockDataId) {}

    fn on_unlock(&mut self, _data_id: LockDataId) {}
}

impl GuacrCliprdrBackend {
    fn advertise_client_formats(&self) {
        let formats = vec![ClipboardFormat::new(ClipboardFormatId::new(CF_UNICODETEXT))];
        let _ = self
            .proxy
            .0
            .send(ClipboardMessage::SendInitiateCopy(formats));
    }
}

/// Create a CLIPRDR backend, a message receiver, and shared clipboard state.
///
/// - `GuacrCliprdrBackend` — pass to `CliprdrClient::new(Box::new(backend))`
/// - `UnboundedReceiver<ClipboardMessage>` — poll in main loop (Send, safe across await)
/// - `Arc<Mutex<PendingClipboardData>>` — set `client_text` when Guacamole sends clipboard
pub fn create_backend(
    temp_dir: String,
) -> (
    GuacrCliprdrBackend,
    tokio::sync::mpsc::UnboundedReceiver<ClipboardMessage>,
    Arc<Mutex<PendingClipboardData>>,
) {
    let (tx, rx) = tokio::sync::mpsc::unbounded_channel();
    let proxy = Arc::new(TokioProxy(tx));
    let data = Arc::new(Mutex::new(PendingClipboardData::new()));

    let backend = GuacrCliprdrBackend {
        data: Arc::clone(&data),
        proxy,
        temp_dir,
    };

    (backend, rx, data)
}
