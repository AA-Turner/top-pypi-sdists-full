use crate::serial::{
    build_initial_telnet_negotiation, build_naws_subneg, parse_size_instruction,
    strip_telnet_commands,
};
use async_trait::async_trait;
use bytes::Bytes;
#[cfg(feature = "threat-detection")]
use guacr_handlers::parse_threat_detection_risk_levels;
use guacr_handlers::{
    // Connection utilities (timeout, keep-alive)
    connect_tcp_with_timeout,
    is_mouse_event_allowed_readonly,
    parse_blob_instruction,
    parse_end_instruction,
    parse_pipe_instruction,
    pipe_blob_bytes,
    // Recording helpers
    record_client_input,
    send_and_record,
    // Session lifecycle
    send_bell,
    send_disconnect,
    send_error_best_effort,
    send_name,
    send_ready,
    ConnectionParameters,
    EventBasedHandler,
    EventCallback,
    HandlerError,
    // Security
    HandlerSecuritySettings,
    HandlerStats,
    HealthStatus,
    KeepAliveManager,
    MultiFormatRecorder,
    // DLP filter for terminal data
    PassthroughDlp,
    // Pipe streams (for native terminal display)
    PipeStreamManager,
    ProtocolHandler,
    // Recording
    RecordingConfig,
    // Observability
    SessionStats,
    TerminalDlp,
    VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
    PIPE_NAME_STDIN,
    PIPE_STREAM_STDOUT,
};
use guacr_protocol::{format_instruction, format_terminal_data_binary};
use guacr_terminal::{
    format_clipboard_instructions, handle_mouse_selection, mouse_event_to_x11_sequence,
    parse_clipboard_blob, parse_key_instruction, parse_mouse_instruction, ModifierState,
    MouseSelection, SelectionResult, TerminalConfig, TerminalEmulator,
};
#[cfg(feature = "threat-detection")]
use log::error;
use log::{debug, info, trace, warn};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::mpsc;

#[cfg(feature = "threat-detection")]
use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig};

/// Telnet protocol handler
///
/// Simpler than SSH - just TCP connection with terminal emulation.
///
/// ## Rendering Method
///
/// PTY bytes are forwarded directly to the browser as `terminal-data` Guacamole
/// instructions. The browser uses xterm.js for rendering — no server-side pixel
/// encoding is performed.
pub struct TelnetHandler {
    config: TelnetConfig,
    pub dlp: Arc<dyn TerminalDlp>,
}

#[derive(Debug, Clone)]
pub struct TelnetConfig {
    pub default_port: u16,
    pub default_rows: u16,
    pub default_cols: u16,
}

impl Default for TelnetConfig {
    fn default() -> Self {
        Self {
            default_port: 23,
            default_rows: 24,
            default_cols: 80,
        }
    }
}

impl TelnetHandler {
    pub fn new(config: TelnetConfig) -> Self {
        Self {
            config,
            dlp: Arc::new(PassthroughDlp),
        }
    }

    pub fn with_defaults() -> Self {
        Self::new(TelnetConfig::default())
    }
}

// ---------------------------------------------------------------------------
// Key event helper
// ---------------------------------------------------------------------------

pub(crate) struct TelnetKeyOutput {
    /// Bytes to write to the telnet server (empty if nothing to send)
    pub(crate) server_bytes: Vec<u8>,
    /// Updated clipboard if paste occurred (to surface the paste_text used)
    /// None means no change to stored_clipboard
    pub(crate) new_clipboard: Option<String>,
}

pub(crate) fn handle_key_event(
    key_event: guacr_terminal::KeyEvent,
    modifier_state: &mut guacr_terminal::ModifierState,
    security: &guacr_handlers::HandlerSecuritySettings,
    stored_clipboard: &str,
    terminal: &guacr_terminal::TerminalEmulator,
    backspace_code: u8,
) -> Option<TelnetKeyOutput> {
    use guacr_handlers::is_keyboard_event_allowed_readonly;
    use guacr_terminal::{x11_keysym_to_bytes_with_backspace, x11_keysym_to_kitty_sequence};

    // Update modifier state; return None (skip) if this is a modifier key alone
    if modifier_state.update_modifier(key_event.keysym, key_event.pressed) {
        return None;
    }

    // Security: Check read-only mode
    if security.read_only
        && !is_keyboard_event_allowed_readonly(key_event.keysym, modifier_state.control)
    {
        trace!("Telnet: Keyboard input blocked (read-only mode)");
        return None;
    }

    // Handle paste shortcuts (matching guacd's behavior):
    // - Ctrl+Shift+V (Linux/Windows): keysym 'V' (0x56) with ctrl+shift
    // - Cmd+V (Mac): keysym 'v' (0x76) with meta
    let is_paste = key_event.pressed
        && ((key_event.keysym == 0x56 && modifier_state.control && modifier_state.shift)
            || (key_event.keysym == 0x76 && modifier_state.meta));

    if is_paste {
        // Security: Check if paste is allowed
        if !security.is_paste_allowed() {
            debug!("Telnet: Paste blocked (disabled or read-only mode)");
            return None;
        }

        if stored_clipboard.is_empty() {
            debug!("Telnet: Paste shortcut pressed but clipboard is empty");
            return None;
        }

        // Check clipboard buffer size limit
        let max_size = security.clipboard_buffer_size;
        let paste_text = if stored_clipboard.len() > max_size {
            warn!(
                "Telnet: Clipboard truncated from {} to {} bytes",
                stored_clipboard.len(),
                max_size
            );
            &stored_clipboard[..max_size]
        } else {
            stored_clipboard
        };

        debug!(
            "Telnet: Paste shortcut - Pasting {} chars from clipboard",
            paste_text.len()
        );

        // Send using bracketed paste mode for safety
        let mut paste_data = Vec::new();
        paste_data.extend_from_slice(b"\x1b[200~"); // Start bracketed paste
        paste_data.extend_from_slice(paste_text.as_bytes());
        paste_data.extend_from_slice(b"\x1b[201~"); // End bracketed paste

        return Some(TelnetKeyOutput {
            server_bytes: paste_data,
            new_clipboard: None,
        });
    }

    // Handle copy shortcuts - ignore them since selection already copies
    // - Ctrl+Shift+C (Linux/Windows): keysym 'C' (0x43) with ctrl+shift
    // - Cmd+C (Mac): keysym 'c' (0x63) with meta
    let is_copy = key_event.pressed
        && ((key_event.keysym == 0x43 && modifier_state.control && modifier_state.shift)
            || (key_event.keysym == 0x63 && modifier_state.meta));

    if is_copy {
        debug!("Telnet: Copy shortcut pressed - ignoring (selection already copies)");
        return None;
    }

    // Check if Kitty keyboard protocol is enabled
    let kitty_level = terminal.kitty_keyboard_level();

    // Convert to terminal bytes with current modifier state and configured backspace
    // Use Kitty keyboard protocol if enabled, otherwise use legacy
    let bytes = if kitty_level > 0 {
        trace!(
            "Telnet: Using Kitty keyboard protocol level {}",
            kitty_level
        );
        x11_keysym_to_kitty_sequence(
            key_event.keysym,
            key_event.pressed,
            Some(modifier_state),
            backspace_code,
            false, // Telnet doesn't use application cursor mode
            kitty_level,
        )
    } else {
        x11_keysym_to_bytes_with_backspace(
            key_event.keysym,
            key_event.pressed,
            Some(modifier_state),
            backspace_code,
        )
    };

    if bytes.is_empty() {
        return None;
    }

    Some(TelnetKeyOutput {
        server_bytes: bytes,
        new_clipboard: None,
    })
}

// ---------------------------------------------------------------------------

#[async_trait]
impl ProtocolHandler for TelnetHandler {
    fn name(&self) -> &str {
        "telnet"
    }

    fn as_event_based(&self) -> Option<&dyn EventBasedHandler> {
        Some(self)
    }

    async fn connect(
        &self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> guacr_handlers::Result<()> {
        let conn_id = params.get("client_id").cloned().unwrap_or_default();
        info!("[conn={conn_id}] Telnet handler starting connection");

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

        // Parse security settings
        let security = HandlerSecuritySettings::from_params(&params);
        info!(
            "[conn={conn_id}] Telnet: Security settings - read_only={}, disable_copy={}, disable_paste={}",
            security.read_only, security.disable_copy, security.disable_paste
        );

        // Parse recording configuration
        let recording_config = RecordingConfig::from_params(&params);
        if recording_config.is_enabled() {
            info!(
                "[conn={conn_id}] Telnet: Recording enabled - ses={}, asciicast={}, typescript={}",
                recording_config.is_ses_enabled(),
                recording_config.is_asciicast_enabled(),
                recording_config.is_typescript_enabled()
            );
        }

        // Parse terminal configuration (font, color-scheme, terminal-type, scrollback, backspace)
        let terminal_config = TerminalConfig::from_params(&params);
        info!(
            "[conn={conn_id}] Telnet: Terminal config - type={}, scrollback={}, color_scheme={}, backspace={}",
            terminal_config.terminal_type,
            terminal_config.scrollback_size,
            terminal_config.color_scheme.name(),
            terminal_config.backspace_code
        );

        // Extract connection parameters
        let conn = ConnectionParameters::from_params(&params, self.config.default_port)?;
        let hostname = conn.hostname;
        let port = conn.port;

        // Fixed cell dimensions used for mouse coordinate mapping.
        // xterm.js manages actual display sizing.
        const CHAR_W: u32 = 9;
        const CHAR_H: u32 = 18;

        let mut rows = self.config.default_rows;
        let mut cols = self.config.default_cols;

        info!(
            "[conn={conn_id}] Telnet: Connecting to {}:{} (timeout: {}s)",
            hostname, port, security.connection_timeout_secs
        );

        // Connect via TCP with timeout (matches guacd behavior)
        let stream =
            connect_tcp_with_timeout((hostname.as_str(), port), security.connection_timeout_secs)
                .await?;

        info!("[conn={conn_id}] Telnet connection established");

        let (mut read_half, mut write_half) = stream.into_split();

        // Send initial Telnet option negotiation (DO ECHO, DO SGA, WILL TERMINAL-TYPE, WILL NAWS).
        // This must happen before any data exchange so servers that require ECHO/SGA negotiation
        // do not stall waiting for it.
        let init_negotiation = build_initial_telnet_negotiation(cols, rows);
        write_half.write_all(&init_negotiation).await.map_err(|e| {
            HandlerError::ProtocolError(format!("Telnet initial negotiation failed: {}", e))
        })?;
        debug!(
            "[conn={conn_id}] Telnet: Initial negotiation sent ({} bytes)",
            init_negotiation.len()
        );

        // Create terminal emulator with browser-requested dimensions and configured scrollback
        let scrollback_size = terminal_config.scrollback_size;
        let mut terminal = TerminalEmulator::new_with_scrollback(rows, cols, scrollback_size);

        // Store backspace code for key handling
        let backspace_code = terminal_config.backspace_code;

        // Initialize recording if enabled
        let mut recorder: Option<MultiFormatRecorder> = if recording_config.is_enabled() {
            match MultiFormatRecorder::new(&recording_config, &params, "telnet", cols, rows) {
                Ok(rec) => {
                    info!("[conn={conn_id}] Telnet: Session recording initialized");
                    Some(rec)
                }
                Err(e) => {
                    warn!(
                        "[conn={conn_id}] Telnet: Failed to initialize recording: {}",
                        e
                    );
                    None
                }
            }
        } else {
            None
        };

        // Initialize pipe stream manager for native terminal display support
        let mut pipe_manager = PipeStreamManager::new();

        // Check if pipe streams are enabled (connection parameter)
        let enable_pipe = params
            .get("enable-pipe")
            .map(|v| v == "true" || v == "1")
            .unwrap_or(false);

        if enable_pipe {
            info!("[conn={conn_id}] Telnet: Pipe streams enabled - opening STDOUT pipe for native terminal display");
            let pipe_instr = pipe_manager.enable_stdout();
            send_and_record(&to_client, &mut recorder, Bytes::from(pipe_instr))
                .await
                .map_err(HandlerError::ChannelError)?;
        }

        // Initialize threat detection if enabled
        #[cfg(feature = "threat-detection")]
        let threat_detector = {
            if let Some(baml_endpoint) = params.get("threat_detection_baml_endpoint") {
                let config = ThreatDetectorConfig {
                    baml_endpoint: baml_endpoint.clone(),
                    baml_api_key: params.get("threat_detection_baml_api_key").cloned(),
                    enabled: true,
                    auto_terminate: params
                        .get("threat_detection_auto_terminate")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    min_log_level: params
                        .get("threat_detection_min_log_level")
                        .and_then(|s| match s.as_str() {
                            "critical" => Some(guacr_threat_detection::ThreatLevel::Critical),
                            "high" => Some(guacr_threat_detection::ThreatLevel::High),
                            "medium" => Some(guacr_threat_detection::ThreatLevel::Medium),
                            "low" => Some(guacr_threat_detection::ThreatLevel::Low),
                            _ => None,
                        })
                        .unwrap_or(guacr_threat_detection::ThreatLevel::Low),
                    command_history_size: params
                        .get("threat_detection_command_history_size")
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(10),
                    timeout_seconds: params
                        .get("threat_detection_timeout_seconds")
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(5),
                    deny_tags: {
                        let (deny, _) = parse_threat_detection_risk_levels(&params);
                        deny
                    },
                    allow_tags: {
                        let (_, allow) = parse_threat_detection_risk_levels(&params);
                        allow
                    },
                    enable_tag_checking: true,
                    proactive_mode: params
                        .get("threat_detection_proactive_mode")
                        .map(|s| s == "true")
                        .unwrap_or(false),
                    approval_timeout_ms: params
                        .get("threat_detection_approval_timeout_ms")
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(2000),
                    fail_closed_on_error: params
                        .get("threat_detection_fail_closed_on_error")
                        .map(|s| s == "true")
                        .unwrap_or(false),
                    show_approval_status: params
                        .get("threat_detection_show_approval_status")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    auto_approve_safe_commands: params
                        .get("threat_detection_auto_approve_safe_commands")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    config_allow_ai_session_terminate: params
                        .get("threat_detection_config_allow_ai_session_terminate")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    resource_ai_session_terminate_enabled: params
                        .get("threat_detection_resource_ai_session_terminate_enabled")
                        .map(|s| s == "true")
                        .unwrap_or(true),
                    level_terminate_flags: HashMap::new(),
                };

                match ThreatDetector::new(config) {
                    Ok(detector) => {
                        info!(
                            "[conn={conn_id}] Telnet: Threat detection enabled with BAML endpoint: {}",
                            baml_endpoint
                        );
                        Some(Arc::new(detector))
                    }
                    Err(e) => {
                        warn!(
                            "[conn={conn_id}] Telnet: Failed to initialize threat detection: {}",
                            e
                        );
                        None
                    }
                }
            } else {
                None
            }
        };
        // Threat detection variables used when feature is enabled
        #[cfg(not(feature = "threat-detection"))]
        let _threat_detector: Option<()> = None;
        #[cfg(feature = "threat-detection")]
        let session_id = uuid::Uuid::new_v4().to_string();
        #[cfg(not(feature = "threat-detection"))]
        let _session_id = String::new();
        #[cfg(feature = "threat-detection")]
        let hostname_for_threat = hostname.clone();
        #[cfg(feature = "threat-detection")]
        let username_for_threat = params.get("username").cloned().unwrap_or_default();

        // Send ready and name instructions
        send_ready(&to_client, "telnet-ready").await?;
        send_name(&to_client, "Telnet").await?;

        // Bidirectional forwarding
        let mut buf = vec![0u8; 4096];
        let mut modifier_state = ModifierState::new();
        let mut mouse_selection = MouseSelection::new();

        // Clipboard storage
        // Store clipboard data received from client (via clipboard stream)
        // This data is pasted when user presses Ctrl+Shift+V
        let mut stored_clipboard = String::new();

        // Keep-alive manager (matches guacd's guac_socket_require_keep_alive behavior)
        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval = tokio::time::interval(std::time::Duration::from_secs(
            DEFAULT_KEEPALIVE_INTERVAL_SECS,
        ));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Per-session observability counters
        let mut stats = SessionStats::new("telnet");

        // 30fps frame coalescing: accumulate server output for 33ms then flush as one
        // terminal-data instruction. Terminal output is a byte STREAM — dropping bytes
        // corrupts xterm.js — so it is buffered losslessly and the source is backpressured
        // (stop reading the socket) instead of dropped. See TerminalOutputBuffer.
        const MAX_FRAME_BYTES: usize = 16 * 1024;
        // Stop reading the socket above this buffer depth so TCP backpressures the server.
        const OUTPUT_HIGH_WATERMARK: usize = 256 * 1024;
        let mut output_buf = guacr_handlers::TerminalOutputBuffer::new();
        let mut frame_interval = tokio::time::interval(std::time::Duration::from_millis(33));
        frame_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Sync/ACK backpressure: pause *sending* after sync_threshold bytes until the client
        // acks (render-gating vs SCTP saturation). Accumulation continues losslessly while
        // paused (bounded by OUTPUT_HIGH_WATERMARK). A lost/late ack auto-clears after
        // SYNC_ACK_TIMEOUT so the session can't freeze under sustained output.
        const SYNC_ACK_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(3);
        let sync_threshold: usize = 65536;
        let mut sync_bytes_sent: usize = 0;
        let mut sync_pending = false;
        let mut sync_sent_at: Option<std::time::Instant> = None;

        loop {
            tokio::select! {
                // Keep-alive ping to detect dead connections
                _ = keepalive_interval.tick() => {
                    if let Some(sync_instr) = keepalive.check() {
                        trace!("[conn={conn_id}] Telnet: Sending keep-alive sync");
                        if send_and_record(&to_client, &mut recorder, sync_instr).await.is_err() {
                            info!("[conn={conn_id}] Telnet: Client channel closed, ending session");
                            break;
                        }
                    }
                }
                // 30fps flush: drain one bounded frame from the lossless buffer and send.
                _ = frame_interval.tick() => {
                    // Auto-resume if the client never acked our sync (prevents a freeze
                    // under sustained output).
                    if sync_pending
                        && sync_sent_at
                            .map(|t| t.elapsed() >= SYNC_ACK_TIMEOUT)
                            .unwrap_or(false)
                    {
                        warn!("[conn={conn_id}] Telnet: sync ack timed out — resuming output");
                        sync_pending = false;
                        sync_sent_at = None;
                    }
                    if !sync_pending {
                        if let Some(frame_bytes) = output_buf.take_frame(MAX_FRAME_BYTES) {
                            let frame = format_terminal_data_binary(&frame_bytes);
                            let frame_len = frame.len();
                            stats.record_frame(frame_len);
                            if let Some(ref mut rec) = recorder {
                                if let Err(e) = rec.record_instruction(
                                    guacr_handlers::RecordingDirection::ServerToClient,
                                    &frame,
                                ) {
                                    warn!("[conn={conn_id}] Telnet: Failed to record frame: {e}");
                                }
                            }
                            match to_client.try_send(frame) {
                                Ok(()) => {
                                    sync_bytes_sent += frame_len;
                                    if sync_bytes_sent >= sync_threshold {
                                        let ts = std::time::SystemTime::now()
                                            .duration_since(std::time::UNIX_EPOCH)
                                            .unwrap_or_default()
                                            .as_millis();
                                        let ts_str = ts.to_string();
                                        let sync_instr = Bytes::from(format_instruction("sync", &[&ts_str]));
                                        if to_client.try_send(sync_instr).is_ok() {
                                            sync_pending = true;
                                            sync_sent_at = Some(std::time::Instant::now());
                                            sync_bytes_sent = 0;
                                        }
                                    }
                                }
                                Err(mpsc::error::TrySendError::Full(_)) => {
                                    // Retain (lossless) and retry next tick — never drop.
                                    output_buf.requeue_front(frame_bytes);
                                    trace!("[conn={conn_id}] Telnet: send queue full, retaining frame");
                                }
                                Err(mpsc::error::TrySendError::Closed(_)) => {
                                    info!("[conn={conn_id}] Telnet: Client channel closed, ending session");
                                    break;
                                }
                            }
                        }
                    }
                }

                // Telnet output -> Terminal -> Client
                // Gated on buffer depth: stop reading when OUTPUT_HIGH_WATERMARK behind so
                // TCP backpressures the server (lossless). Keyboard input stays active.
                result = read_half.read(&mut buf), if output_buf.len() < OUTPUT_HIGH_WATERMARK => {
                    match result {
                        Ok(0) => {
                            info!("[conn={conn_id}] Telnet connection closed");

                            send_error_best_effort(&to_client, "Telnet connection closed by server", 517).await; // RESOURCE_CLOSED

                            break;
                        }
                        Ok(n) => {
                            // If STDOUT pipe is enabled, send raw data to client
                            // This enables native terminal display (with ANSI escape codes)
                            if pipe_manager.is_stdout_enabled() {
                                let blob = pipe_blob_bytes(PIPE_STREAM_STDOUT, &buf[..n]);
                                send_and_record(&to_client, &mut recorder, blob).await
                                    .map_err(HandlerError::ChannelError)?;
                            }

                            // Threat detection: Analyze live terminal output from server
                            #[cfg(feature = "threat-detection")]
                            if let Some(ref detector) = threat_detector {
                                match detector.analyze_terminal_output(&session_id, &buf[..n], &username_for_threat, &hostname_for_threat, "telnet").await {
                                    Ok(threat) => {
                                        if threat.should_terminate() {
                                            error!("[conn={conn_id}] Telnet: TERMINATING SESSION due to threat in terminal output: {}", threat.description);
                                            let msg = format!("Session terminated: {}", threat.description);
                                            send_error_best_effort(&to_client, &msg, 517).await;
                                            detector.cleanup_session(&session_id);
                                            break;
                                        }
                                    }
                                    Err(e) => {
                                        debug!("[conn={conn_id}] Telnet: Threat detection error (non-fatal): {}", e);
                                    }
                                }
                            }

                            // Record output if recording is enabled
                            if let Some(ref mut rec) = recorder {
                                let _ = rec.record_output(&buf[..n]);
                            }

                            // Strip Telnet IAC sequences before feeding data to the vt100 parser.
                            // Servers may interleave option-negotiation responses with terminal data;
                            // without stripping, those IAC bytes reach xterm.js as garbage characters.
                            // Note: the raw buf[..n] is still used for PIPE output (pre-strip) and for
                            // the terminal-data instruction sent to xterm.js (post-strip).
                            let clean = strip_telnet_commands(&buf[..n]);

                            // Process terminal output (maintains terminal state for mouse events).
                            // Catch vt100 panics so a bad escape sequence can't end the session.
                            if !clean.is_empty() {
                                match std::panic::catch_unwind(
                                    std::panic::AssertUnwindSafe(|| terminal.process(&clean))
                                ) {
                                    Ok(Ok(())) => {}
                                    Ok(Err(e)) => warn!("[conn={conn_id}] Telnet: Terminal emulator error (non-fatal): {}", e),
                                    Err(_) => {
                                        warn!("[conn={conn_id}] Telnet: Terminal emulator panicked on escape sequence (resetting, session continues)");
                                        terminal = TerminalEmulator::new_with_scrollback(rows, cols, scrollback_size);
                                    }
                                }
                            }

                            // Check for BEL character (0x07) and send audio beep to client
                            if buf[..n].contains(&0x07) {
                                debug!("[conn={conn_id}] Telnet: BEL detected, sending audio beep");
                                send_bell(&to_client, 100).await?;
                            }

                            // Buffer cleaned bytes losslessly; the 30fps timer flushes them in
                            // bounded frames. Never drop terminal bytes (that corrupts xterm.js);
                            // backpressure is applied by gating the read arm on the watermark.
                            let filtered = self.dlp.filter(Bytes::from(clean));
                            if !filtered.is_empty() {
                                output_buf.push(&filtered);
                            }
                        }
                        Err(e) => {
                            warn!("[conn={conn_id}] Telnet read error: {}", e);

                            let error_msg = format!("Telnet connection error: {}", e);
                            send_error_best_effort(&to_client, &error_msg, 512).await; // UPSTREAM_ERROR

                            break;
                        }
                    }
                }

                // Client input -> Telnet
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("[conn={conn_id}] Telnet: Client disconnected");
                        break;
                    };
                    // Record client-to-server instruction
                    record_client_input(&mut recorder, &msg);
                    stats.record_input();
                    // Parse Guacamole instruction
                    let msg_str = String::from_utf8_lossy(&msg);

                    // Sync ACK from client — resume sending. No screen redraw.
                    if msg_str.starts_with("4.sync,") {
                        sync_pending = false;
                        sync_sent_at = None;
                        continue;
                    }

                    if let Some(key_event) = parse_key_instruction(&msg_str) {
                        let Some(key_out) = handle_key_event(
                            key_event,
                            &mut modifier_state,
                            &security,
                            &stored_clipboard,
                            &terminal,
                            backspace_code,
                        ) else {
                            continue;
                        };
                        if let Some(clip) = key_out.new_clipboard {
                            stored_clipboard = clip;
                        }
                        if !key_out.server_bytes.is_empty() {
                            // Threat detection: Analyze live keyboard input before sending to server
                            #[cfg(feature = "threat-detection")]
                            if let Some(ref detector) = threat_detector {
                                if let Ok(seq) = String::from_utf8(key_out.server_bytes.clone()) {
                                    match detector.analyze_keystroke_sequence(&session_id, &seq, &username_for_threat, &hostname_for_threat, "telnet").await {
                                        Ok(threat) => {
                                            if threat.should_terminate() {
                                                error!("[conn={conn_id}] Telnet: TERMINATING SESSION due to threat in keyboard input: {}", threat.description);
                                                let msg = format!("Session terminated: {}", threat.description);
                                                send_error_best_effort(&to_client, &msg, 517).await;
                                                detector.cleanup_session(&session_id);
                                                break;
                                            }
                                        }
                                        Err(e) => {
                                            debug!("[conn={conn_id}] Telnet: Threat detection error (non-fatal): {}", e);
                                        }
                                    }
                                }
                            }
                            // Record input if enabled
                            if let Some(ref mut rec) = recorder {
                                if recording_config.recording_include_keys {
                                    let _ = rec.record_input(&key_out.server_bytes);
                                }
                            }
                            write_half.write_all(&key_out.server_bytes).await
                                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                        }
                    } else if let Some((new_width_px, new_height_px)) = parse_size_instruction(&msg_str) {
                        // Handle window resize — send NAWS sub-negotiation to server (RFC 1073).
                        let new_cols = (new_width_px / CHAR_W).clamp(20, 500) as u16;
                        let new_rows = (new_height_px / CHAR_H).clamp(10, 200) as u16;

                        if new_rows != rows || new_cols != cols {
                            // Resize terminal emulator — catch panics from vt100 edge cases
                            if std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                                terminal.resize(new_rows, new_cols)
                            }))
                            .is_err()
                            {
                                warn!("[conn={conn_id}] Telnet: Terminal emulator panicked on resize (session continues)");
                            } else {
                                rows = new_rows;
                                cols = new_cols;
                                // Send NAWS sub-negotiation to notify the server of the new size
                                let naws = build_naws_subneg(cols, rows);
                                write_half
                                    .write_all(&naws)
                                    .await
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                                info!(
                                    "[conn={conn_id}] Telnet: Resize {}x{} px -> {}x{} chars (NAWS sent)",
                                    new_width_px, new_height_px, cols, rows
                                );
                                // Record resize event
                                if let Some(ref mut rec) = recorder {
                                    let _ = rec.record_resize(cols, rows);
                                }
                            }
                        }
                    } else if msg_str.contains(".clipboard,") {
                        // Clipboard instruction received - this is just a SYNC, not a paste command!
                        // The Guacamole protocol sends clipboard instructions to sync clipboard state
                        // between client and server. This does NOT mean the user wants to paste.
                        debug!("[conn={conn_id}] Telnet: Clipboard stream opened - syncing clipboard state (not pasting)");
                    } else if let Some(clipboard_text) = parse_clipboard_blob(&msg_str) {
                        // Clipboard blob instruction: Store clipboard data from client
                        // This is just synchronization - NOT a paste command!
                        // The actual paste happens when user presses Ctrl+Shift+V (keysym 'V' with ctrl+shift)

                        stored_clipboard = clipboard_text;
                        debug!("[conn={conn_id}] Telnet: Clipboard updated - stored {} chars (waiting for Ctrl+Shift+V to paste)", stored_clipboard.len());
                    } else if let Some(mouse_event) = parse_mouse_instruction(&msg_str) {
                        // Security: Check read-only mode for mouse clicks
                        if security.read_only && !is_mouse_event_allowed_readonly(mouse_event.button_mask) {
                            trace!("[conn={conn_id}] Telnet: Mouse click blocked (read-only mode)");
                            continue;
                        }

                        // Handle mouse events intelligently:
                        // 1. If terminal has mouse mode enabled (vim/tmux) - send X11 sequences
                        // 2. Otherwise, left-click drag = text selection (copy to clipboard)
                        // 3. Hover with no buttons = ignored (prevents garbage)

                        // Check if terminal has mouse mode enabled (vim :set mouse=a, tmux mouse mode)
                        if terminal.is_mouse_enabled() && mouse_event.button_mask != 0 {
                            // Terminal wants mouse events - send X11 sequences
                            let mouse_seq = mouse_event_to_x11_sequence(
                                mouse_event.x_px,
                                mouse_event.y_px,
                                mouse_event.button_mask as u8,
                                CHAR_W,
                                CHAR_H
                            );

                            if !mouse_seq.is_empty() {
                                trace!("[conn={conn_id}] Telnet: Mouse X11 sequence (button={}) at ({}, {})",
                                    mouse_event.button_mask, mouse_event.x_px, mouse_event.y_px);
                                write_half.write_all(&mouse_seq).await
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                        }
                        // Try text selection (only when mouse mode is disabled)
                        else {
                            match handle_mouse_selection(
                                mouse_event,
                                &mut mouse_selection,
                                &terminal,
                                CHAR_W,
                                CHAR_H,
                                cols,
                                rows,
                                modifier_state.shift, // Pass shift key state for extend selection
                            ) {
                                SelectionResult::InProgress(overlay_instructions) => {
                                    // Send visual feedback (blue overlay) to client
                                    trace!("[conn={conn_id}] Telnet: Selection in progress, sending {} overlay instructions", overlay_instructions.len());
                                    for instr in overlay_instructions {
                                        send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                            .map_err(HandlerError::ChannelError)?;
                                    }
                                }
                                SelectionResult::Complete { text: selected_text, clear_instructions } => {
                                    // Security: Check if copy is allowed
                                    if !security.is_copy_allowed() {
                                        debug!("[conn={conn_id}] Telnet: Selection copy blocked (copy disabled)");

                                        // Still clear the overlay even if copy is blocked
                                        for instr in clear_instructions {
                                            send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                                .map_err(HandlerError::ChannelError)?;
                                        }
                                        continue;
                                    }

                                    debug!("[conn={conn_id}] Telnet: Selection complete, copying {} chars", selected_text.len());

                                    // CRITICAL: Update local clipboard immediately to avoid race condition
                                    // If user pastes immediately after selecting, they expect the selected text
                                    // Without this, there's a race where the clipboard blob from client arrives
                                    // after the user has already pressed Ctrl+Shift+V
                                    stored_clipboard = selected_text.clone();
                                    debug!("[conn={conn_id}] Telnet: Local clipboard updated immediately with {} chars", stored_clipboard.len());

                                    // Clear the overlay
                                    for instr in clear_instructions {
                                        send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                            .map_err(HandlerError::ChannelError)?;
                                    }

                                    // Send to client as clipboard
                                    let clipboard_stream_id = 10;
                                    let clipboard_instructions = format_clipboard_instructions(&selected_text, clipboard_stream_id);

                                    for instr in clipboard_instructions {
                                        send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                            .map_err(HandlerError::ChannelError)?;
                                    }
                                }
                                SelectionResult::None => {
                                    // No selection action (hovering, etc.) - ignore
                                }
                            }
                        }
                    } else if let Some(pipe_instr) = parse_pipe_instruction(&msg_str) {
                        // Handle incoming pipe stream (e.g., STDIN from client)
                        if pipe_instr.name == PIPE_NAME_STDIN {
                            debug!("[conn={conn_id}] Telnet: STDIN pipe opened by client (stream {})", pipe_instr.stream_id);
                            pipe_manager.register_incoming(
                                pipe_instr.stream_id,
                                &pipe_instr.name,
                                &pipe_instr.mimetype,
                            );
                        } else {
                            debug!("[conn={conn_id}] Telnet: Unknown pipe '{}' opened by client", pipe_instr.name);
                        }
                    } else if let Some(blob_instr) = parse_blob_instruction(&msg_str) {
                        // Handle blob data on STDIN pipe
                        if pipe_manager.is_stdin_stream(blob_instr.stream_id) {
                            // Security: Check if input is allowed
                            if security.read_only {
                                debug!("[conn={conn_id}] Telnet: STDIN pipe data blocked (read-only mode)");
                            } else {
                                debug!("[conn={conn_id}] Telnet: Received {} bytes on STDIN pipe", blob_instr.data.len());
                                write_half.write_all(&blob_instr.data).await
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                        }
                    } else if let Some(end_stream_id) = parse_end_instruction(&msg_str) {
                        // Handle end of pipe stream
                        if pipe_manager.is_stdin_stream(end_stream_id) {
                            debug!("[conn={conn_id}] Telnet: STDIN pipe closed by client");
                            pipe_manager.close(PIPE_NAME_STDIN);
                        }
                    }
                }

                else => {
                    debug!("[conn={conn_id}] Telnet session ending");
                    break;
                }
            }
        }

        // Close any open pipe streams
        let end_instructions = pipe_manager.close_all();
        for instr in end_instructions {
            let _ = to_client.send(Bytes::from(instr)).await;
        }

        // Record a final sync with the real wall-clock timestamp so the
        // recording end marker is accurate (serial.rs uses the same approach).
        let final_ts_ms = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis() as u64;
        let final_sync = guacr_protocol::format_instruction("sync", &[&final_ts_ms.to_string()]);
        let _ = send_and_record(&to_client, &mut recorder, bytes::Bytes::from(final_sync)).await;

        // Finalize recording
        if let Some(rec) = recorder {
            if let Err(e) = rec.finalize() {
                warn!(
                    "[conn={conn_id}] Telnet: Failed to finalize recording: {}",
                    e
                );
            } else {
                info!("[conn={conn_id}] Telnet: Session recording finalized");
            }
        }

        // Unconditional threat-detector session cleanup (matches SSH handler behavior).
        // When the threat-detection feature is disabled this compiles to nothing.
        #[cfg(feature = "threat-detection")]
        if let Some(ref detector) = threat_detector {
            detector.cleanup_session(&session_id);
            debug!("[conn={conn_id}] Telnet: Threat detection session cleaned up");
        }

        info!("[conn={conn_id}] session complete: {}", stats.summary());
        send_disconnect(&to_client).await;
        info!("[conn={conn_id}] Telnet handler connection ended");
        Ok(())
    }

    async fn health_check(&self) -> guacr_handlers::Result<HealthStatus> {
        Ok(HealthStatus::Healthy)
    }

    async fn stats(&self) -> guacr_handlers::Result<HandlerStats> {
        Ok(HandlerStats::default())
    }
}

// Event-based handler implementation for zero-copy integration
#[async_trait]
impl EventBasedHandler for TelnetHandler {
    fn name(&self) -> &str {
        "telnet"
    }

    async fn connect_with_events(
        &self,
        params: HashMap<String, String>,
        callback: Arc<dyn EventCallback>,
        from_client: mpsc::Receiver<Bytes>,
        _video_tx: Option<Arc<dyn VideoOutput>>,
        _hooks: guacr_handlers::SessionHooks,
    ) -> Result<(), HandlerError> {
        guacr_handlers::connect_with_event_adapter(
            |params, to_client, from_client, _video_tx, _hooks| {
                self.connect(params, to_client, from_client, _video_tx, _hooks)
            },
            params,
            callback,
            from_client,
            _video_tx,
            _hooks,
            4096, // channel capacity
        )
        .await
    }
}
