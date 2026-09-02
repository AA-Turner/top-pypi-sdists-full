use async_trait::async_trait;
#[allow(unused_imports)] // Engine trait needed for OSC52 .decode() method
use base64::Engine;
use bytes::Bytes;
use guacr_handlers::{
    handle_mouse_event,
    is_keyboard_event_allowed_readonly,
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
    session_sharing,
    share_viewer,
    ConnectionParameters,
    EventBasedHandler,
    EventCallback,
    HandlerError,
    // Security
    HandlerSecuritySettings,
    HandlerStats,
    HealthStatus,
    // Host key verification
    HostKeyConfig,
    HostKeyVerifier,
    // Connection utilities (timeout, keep-alive)
    KeepAliveManager,
    MultiFormatRecorder,
    // DLP filter for terminal data
    PassthroughDlp,
    // Pipe streams (for native terminal display)
    PipeStreamManager,
    ProtocolHandler,
    // Recording
    RecordingConfig,
    SessionOwnerSender,
    // Observability
    SessionStats,
    SessionViewer,
    TerminalDlp,
    VideoOutput,
    DEFAULT_KEEPALIVE_INTERVAL_SECS,
    PIPE_NAME_STDIN,
    PIPE_STREAM_STDOUT,
};
use guacr_protocol::{
    format_instruction, format_size, format_terminal_data_binary, GuacamoleParser,
    STATUS_CLIENT_UNAUTHORIZED, STATUS_UPSTREAM_ERROR, STATUS_UPSTREAM_TIMEOUT,
};
use guacr_terminal::{
    extract_selection_text, format_clear_selection_instructions, format_clipboard_instructions,
    format_selection_overlay_instructions, parse_clipboard_blob, parse_display_size,
    parse_key_instruction, parse_mouse_instruction, x11_keysym_to_bytes_with_modes,
    x11_keysym_to_kitty_sequence, ModifierState, MouseSelection, TerminalConfig, TerminalEmulator,
};
use log::{debug, error, info, trace, warn};
use russh::client;
use russh::Pty;
use russh_keys::key;
use russh_keys::PublicKeyBase64;
use ssh_key::Certificate;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::mpsc;

/// SSH protocol handler
///
/// Connects to SSH servers and provides terminal access via the Guacamole protocol.
///
/// ## Rendering Method
///
/// PTY bytes are forwarded directly to the browser as `terminal-data` Guacamole
/// instructions. The browser uses xterm.js for rendering — no server-side pixel
/// encoding is performed.
pub struct SshHandler {
    config: SshConfig,
    pub dlp: Arc<dyn TerminalDlp>,
}

/// All pure parameters parsed from the connection `params` map before any IO.
/// Extracted from `connect()` so the parsing is testable and the main function
/// starts at the first async operation (TCP connect).
#[derive(Debug)]
pub(crate) struct SshConnectParams {
    pub(crate) security: HandlerSecuritySettings,
    pub(crate) recording_config: RecordingConfig,
    pub(crate) terminal_config: TerminalConfig,
    pub(crate) host_key_config: HostKeyConfig,
    pub(crate) hostname: String,
    pub(crate) port: u16,
    pub(crate) username: String,
    pub(crate) password: Option<String>,
    pub(crate) private_key: Option<String>,
    pub(crate) passphrase: Option<String>,
    pub(crate) public_key_cert: Option<String>,
    pub(crate) rows: u16,
    pub(crate) cols: u16,
    pub(crate) char_width: u32,
    pub(crate) char_height: u32,
    /// Keepalive interval toward the SSH server, in seconds. 0 disables it.
    pub(crate) server_alive_interval: u64,
}

impl SshConnectParams {
    pub(crate) fn from_params(
        params: &HashMap<String, String>,
        default_port: u16,
    ) -> guacr_handlers::Result<Self> {
        let security = HandlerSecuritySettings::from_params(params);
        let recording_config = RecordingConfig::from_params(params);
        let terminal_config = TerminalConfig::from_params(params);
        let host_key_config = HostKeyConfig::from_params(params);

        let conn = ConnectionParameters::from_params(params, default_port)?;
        let username = conn
            .username
            .ok_or_else(|| HandlerError::MissingParameter("username".to_string()))?;
        let (_, _, cols, rows) = parse_display_size(params);

        let password = params.get("password").cloned();
        let private_key = params.get("private_key").cloned();
        let passphrase = params.get("passphrase").cloned();
        let public_key_cert = params.get("public-key").cloned();

        Ok(Self {
            security,
            recording_config,
            terminal_config,
            host_key_config,
            hostname: conn.hostname,
            port: conn.port,
            username,
            password,
            private_key,
            passphrase,
            public_key_cert,
            // Use the negotiated display size for the initial PTY so the shell starts
            // at the correct dimensions. Falls back to DEFAULT_COLS×DEFAULT_ROWS (80×24).
            rows,
            cols,
            char_width: 9,
            char_height: 18,
            server_alive_interval: parse_server_alive_interval(params),
        })
    }
}

#[derive(Debug, Clone)]
pub struct SshConfig {
    pub default_port: u16,
    pub default_rows: u16,
    pub default_cols: u16,
}

impl Default for SshConfig {
    fn default() -> Self {
        Self {
            default_port: 22,
            default_rows: 24,
            default_cols: 80,
        }
    }
}

impl SshHandler {
    pub fn new(config: SshConfig) -> Self {
        Self {
            config,
            dlp: Arc::new(PassthroughDlp),
        }
    }

    pub fn with_defaults() -> Self {
        Self::new(SshConfig::default())
    }

    /// Send error instruction to client and return HandlerError
    ///
    /// This ensures the client sees a user-friendly error message before the connection closes.
    /// Matches guacd's behavior of calling guac_client_abort() which sends error instructions.
    async fn send_error_and_return(
        to_client: &mpsc::Sender<Bytes>,
        error: HandlerError,
    ) -> HandlerError {
        let (message, status_code) = match &error {
            HandlerError::MissingParameter(param) => (
                format!("Missing required parameter: {}", param),
                STATUS_UPSTREAM_ERROR,
            ),
            HandlerError::ConnectionFailed(msg) => {
                if msg.contains("timeout") || msg.contains("timed out") {
                    (
                        format!("Connection timeout: {}", msg),
                        STATUS_UPSTREAM_TIMEOUT,
                    )
                } else {
                    (format!("Connection failed: {}", msg), STATUS_UPSTREAM_ERROR)
                }
            }
            HandlerError::AuthenticationFailed(msg) => {
                if msg.contains("Host key") || msg.contains("fingerprint") {
                    (
                        format!("Host key verification failed: {}", msg),
                        STATUS_UPSTREAM_ERROR,
                    )
                } else if msg.contains("timeout") || msg.contains("timed out") {
                    (
                        format!("Authentication timeout: {}", msg),
                        STATUS_UPSTREAM_TIMEOUT,
                    )
                } else {
                    (
                        format!("Authentication failed: {}", msg),
                        STATUS_CLIENT_UNAUTHORIZED,
                    )
                }
            }
            _ => (error.to_string(), STATUS_UPSTREAM_ERROR),
        };

        send_error_best_effort(to_client, &message, status_code).await;

        error
    }
}

#[async_trait]
impl ProtocolHandler for SshHandler {
    fn name(&self) -> &str {
        "ssh"
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
        info!("[conn={conn_id}] SSH handler starting connection");

        // Transport congestion signal from the WebRTC sender task. When set, the
        // data channel can't keep up with output; we stop byte-exact forwarding and
        // coalesce to current-screen redraws (see the bidirectional loop below).
        // ── 0a. GUID-based viewer join (Phase 6b) ────────────────────────────
        // Guard the move: only consume from_client if share_guid is present.
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

        // ── 0b. Legacy session sharing — handle viewer and owner modes ────────
        let share_id = params.get("share-id").cloned();
        let viewer_mode = params
            .get("viewer-mode")
            .map(|v| v == "true" || v == "1")
            .unwrap_or(false);

        if viewer_mode {
            // Viewer path: look up the active session and forward frames.
            let sid = share_id.as_deref().unwrap_or("");
            info!("[conn={conn_id}] SSH: viewer mode for session {sid:?}");
            let viewer = SessionViewer::join(sid, to_client.clone()).await;
            match viewer {
                Some(v) => {
                    // Discard all input from this viewer (read-only).
                    // Abort the drain task when the viewer session ends so FDs
                    // and task slots are released promptly.
                    let drain_task = tokio::spawn(async move {
                        while from_client.recv().await.is_some() {
                            // intentionally discarded
                        }
                    });
                    v.run().await;
                    drain_task.abort();
                    return Ok(());
                }
                None => {
                    let msg = format!("No active session found for share-id: {sid}");
                    send_error_best_effort(
                        &to_client,
                        &msg,
                        guacr_protocol::STATUS_UPSTREAM_NOT_FOUND,
                    )
                    .await;
                    return Err(HandlerError::ConnectionFailed(msg));
                }
            }
        }

        // Owner path (or standalone — no share-id): register session if share-id present.
        let mut owner_sender = SessionOwnerSender::new(to_client.clone());
        // Viewer input channel: receives key/mouse bytes forwarded by viewers with PRIV_CONTROL.
        // The tx end is registered on the handle so share_viewer.rs can deliver bytes here.
        // For standalone sessions the rx is never sent to, so it idles without cost.
        let (viewer_input_tx, mut viewer_input_rx) =
            tokio::sync::mpsc::unbounded_channel::<Bytes>();
        if let Some(ref sid) = share_id {
            match session_sharing::register(sid) {
                Ok(handle) => {
                    info!("[conn={conn_id}] SSH: registered shared session {sid:?}");
                    handle.set_viewer_input_channel(viewer_input_tx);
                    owner_sender.attach_session(handle);
                }
                Err(e) => {
                    // Non-fatal: log and continue as a standalone session.
                    warn!(
                        "[conn={conn_id}] SSH: failed to register session {sid:?}: {e} — continuing as standalone"
                    );
                }
            }
        }
        // For standalone sessions (no share-id) owner_sender is a passthrough to to_client.

        // ── 1. Parse parameters (pure, no IO) ────────────────────────────────
        let p = SshConnectParams::from_params(&params, self.config.default_port)?;

        let SshConnectParams {
            security,
            recording_config,
            terminal_config,
            host_key_config,
            hostname,
            port,
            username,
            password,
            private_key,
            passphrase,
            public_key_cert,
            rows,
            cols,
            char_width,
            char_height,
            server_alive_interval,
        } = p;

        // Borrow password/key as Option<&str> for the authenticate() call later.
        let password = password.as_deref();
        let private_key = private_key.as_deref();
        let passphrase = passphrase.as_deref();
        let public_key_cert = public_key_cert.as_deref();

        info!(
            "[conn={conn_id}] SSH: read_only={} copy={} paste={} recording={} timeout={}s",
            security.read_only,
            !security.disable_copy,
            !security.disable_paste,
            recording_config.is_enabled(),
            security.connection_timeout_secs,
        );
        info!(
            "[conn={conn_id}] SSH handler: Connecting to {}@{}:{} (PTY {}×{}, timeout {}s)",
            username, hostname, port, cols, rows, security.connection_timeout_secs
        );

        // Create SSH config (see ssh_client_config for the keepalive and FIPS notes).
        if server_alive_interval > 0 {
            info!(
                "[conn={conn_id}] SSH: server keepalive every {server_alive_interval}s (server-alive-interval)"
            );
        }
        let ssh_config = ssh_client_config(server_alive_interval);

        // Create SSH client handler with host key verification
        let ssh_client_handler = SshClientHandler::new(hostname.clone(), port, host_key_config);

        // Connect with timeout (matches guacd's timeout parameter)
        let connection_timeout = Duration::from_secs(security.connection_timeout_secs);
        let sh = tokio::time::timeout(
            connection_timeout,
            client::connect(
                Arc::new(ssh_config),
                (hostname.as_str(), port),
                ssh_client_handler,
            ),
        )
        .await
        .map_err(|_| {
            error!(
                "[conn={conn_id}] SSH handler: Connection timed out after {} seconds",
                security.connection_timeout_secs
            );
            HandlerError::ConnectionFailed(format!(
                "Connection timed out after {} seconds",
                security.connection_timeout_secs
            ))
        })
        .and_then(|r| {
            r.map_err(|e| {
                // Check if this is a host key verification failure
                let error_str = e.to_string();
                if error_str.contains("host key") || error_str.contains("fingerprint") {
                    error!(
                        "[conn={conn_id}] SSH handler: Host key verification failed: {}",
                        e
                    );
                    HandlerError::AuthenticationFailed(format!(
                        "Host key verification failed: {}",
                        e
                    ))
                } else {
                    error!("[conn={conn_id}] SSH handler: Connection failed: {}", e);
                    HandlerError::ConnectionFailed(e.to_string())
                }
            })
        });

        let mut sh = match sh {
            Ok(s) => s,
            Err(e) => return Err(Self::send_error_and_return(&to_client, e).await),
        };

        debug!("[conn={conn_id}] SSH handler: Connected to SSH server, starting authentication");

        // ----------------------------------------------------------------
        // ── 3. Authenticate ───────────────────────────────────────────────────
        let auth_timeout = Duration::from_secs(security.connection_timeout_secs);
        authenticate(
            &mut sh,
            username.clone(),
            password,
            private_key,
            passphrase,
            public_key_cert,
            auth_timeout,
            &to_client,
        )
        .await?;

        // ----------------------------------------------------------------
        // 4. Open session channel
        // ----------------------------------------------------------------
        let mut channel =
            open_session_channel(&mut sh, &terminal_config, rows, cols, &params).await?;

        // Create terminal emulator with browser-requested dimensions and configured scrollback
        let scrollback_size = terminal_config.scrollback_size;
        let mut terminal = TerminalEmulator::new_with_scrollback(rows, cols, scrollback_size);

        // ----------------------------------------------------------------
        // 5. Collect banner
        // ----------------------------------------------------------------
        // CRITICAL: Read any initial data (banner/MOTD) that arrived immediately after shell request
        // SSH servers often send welcome banners right away, before we enter the event loop
        let banner_raw =
            collect_banner(&mut channel, &mut terminal, rows, cols, scrollback_size).await;
        let banner_collected = !banner_raw.is_empty();

        debug!(
            "SSH: Banner collection finished, has_content={}, bytes_received={}, terminal_size={}x{}",
            banner_collected,
            banner_raw.len(),
            cols,
            rows
        );

        // Forward the raw banner bytes to xterm.js as terminal-data before entering
        // the main loop. The bytes were consumed from the SSH channel and would be
        // lost otherwise — xterm.js renders ANSI natively so no JPEG conversion needed.
        if banner_collected {
            let instr = format_terminal_data_binary(&banner_raw);
            if let Err(e) = to_client.send(instr).await {
                warn!(
                    "[conn={conn_id}] SSH: Failed to forward banner bytes: {}",
                    e
                );
            }
        }

        // Make rows/cols mutable for dynamic resizing (guacd-style)
        let mut current_rows = rows;
        let mut current_cols = cols;

        // Store backspace code for key handling (before terminal_config moves)
        let backspace_code = terminal_config.backspace_code;

        // Initialize recording if enabled
        let mut recorder: Option<MultiFormatRecorder> = if recording_config.is_enabled() {
            match MultiFormatRecorder::new(&recording_config, &params, "ssh", cols, rows) {
                Ok(rec) => {
                    info!("[conn={conn_id}] SSH: Session recording initialized");
                    Some(rec)
                }
                Err(e) => {
                    warn!(
                        "[conn={conn_id}] SSH: Failed to initialize recording: {}",
                        e
                    );
                    None
                }
            }
        } else {
            None
        };

        // Initialize threat detection if the feature is enabled and baml endpoint is configured
        #[cfg(feature = "threat-detection")]
        let threat_detector = guacr_threat_detection::ThreatDetector::from_params(&params, "SSH");
        #[cfg(feature = "threat-detection")]
        let threat_session_id = uuid::Uuid::new_v4().to_string();
        #[cfg(feature = "threat-detection")]
        let hostname_for_threat = hostname.clone();
        #[cfg(feature = "threat-detection")]
        let username_for_threat = username.clone();

        // Initialize pipe stream manager for native terminal display support
        // This enables CLI clients to receive raw terminal output (with ANSI codes)
        // instead of rendered images, allowing display in native terminal apps
        let mut pipe_manager = PipeStreamManager::new();

        // Check if pipe streams are enabled (connection parameter)
        let enable_pipe = params
            .get("enable-pipe")
            .map(|v| v == "true" || v == "1")
            .unwrap_or(false);

        if enable_pipe {
            info!("[conn={conn_id}] SSH: Pipe streams enabled - opening STDOUT pipe for native terminal display");
            let pipe_instr = pipe_manager.enable_stdout();
            send_and_record(&to_client, &mut recorder, Bytes::from(pipe_instr))
                .await
                .map_err(HandlerError::ChannelError)?;
        }

        // Send ready and name instructions to signal the connection is established
        send_ready(&to_client, "ssh-ready").await?;
        send_name(&to_client, "SSH").await?;

        // Initialize the display dimensions. Recorded as well as sent: the recorder keeps
        // `size` specifically so playback knows the layer geometry.
        let size_instr = display_size_instruction(cols, rows, char_width, char_height);
        send_and_record(&to_client, &mut recorder, Bytes::from(size_instr))
            .await
            .map_err(HandlerError::ChannelError)?;

        debug!("[conn={conn_id}] SSH: Display initialized");

        // Track modifier key state (Ctrl, Shift, Alt) for Ctrl+C, etc.
        let mut modifier_state = ModifierState::new();

        // Mouse selection tracking
        let mut mouse_selection = MouseSelection::new();

        // Clipboard storage
        // Store clipboard data received from client (via clipboard stream)
        // This data is pasted when user presses Ctrl+Shift+V
        let mut stored_clipboard = String::new();

        // Keep-alive manager (matches guacd's guac_socket_require_keep_alive behavior)
        let mut keepalive = KeepAliveManager::new(DEFAULT_KEEPALIVE_INTERVAL_SECS);
        let mut keepalive_interval =
            tokio::time::interval(Duration::from_secs(DEFAULT_KEEPALIVE_INTERVAL_SECS));
        keepalive_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Per-session observability counters
        let mut stats = SessionStats::new("ssh");

        // 60 fps frame coalescing: accumulate SSH output within each 16ms window
        // and send as a single terminal-data instruction. This avoids the per-frame
        // WebRTC overhead and gives xterm.js one clean batch per paint cycle.
        // Cap at 16 KB per terminal-data frame. Terminal output is a byte STREAM —
        // escape sequences span bytes and xterm.js tracks state across them — so it is
        // NEVER dropped (dropping corrupts the client terminal). We buffer losslessly
        // and backpressure the source instead. See TerminalOutputBuffer.
        const MAX_FRAME_BYTES: usize = 16 * 1024;
        // Stop reading the SSH channel above this buffer depth so russh's channel window
        // backpressures the *server* — bounds memory without dropping bytes.
        const OUTPUT_HIGH_WATERMARK: usize = 256 * 1024;
        let mut output_buf = guacr_handlers::TerminalOutputBuffer::new();
        let mut frame_interval = tokio::time::interval(Duration::from_millis(33));
        frame_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);

        // Sync/ACK backpressure: after sync_threshold bytes we send a sync and pause
        // *sending* until the client echoes it back — render-gating that keeps SCTP from
        // saturating and dropping ICE. Accumulation continues losslessly while paused
        // (bounded by OUTPUT_HIGH_WATERMARK). A lost/late ack must not freeze the session,
        // so sync_pending auto-clears after SYNC_ACK_TIMEOUT (fixes the `yes` + Ctrl-C hang).
        const SYNC_ACK_TIMEOUT: Duration = Duration::from_secs(3);
        let sync_threshold: usize = 65536;
        let mut sync_bytes_sent: usize = 0;
        let mut sync_pending = false;
        let mut sync_sent_at: Option<std::time::Instant> = None;

        // Bidirectional forwarding
        loop {
            tokio::select! {
                // Keep-alive ping to detect dead connections
                _ = keepalive_interval.tick() => {
                    if let Some(sync_instr) = keepalive.check() {
                        trace!("SSH: Sending keep-alive sync");
                        if send_and_record(&to_client, &mut recorder, sync_instr).await.is_err() {
                            info!("[conn={conn_id}] SSH: Client channel closed, ending session");
                            break;
                        }
                    }
                }

                // 30 fps flush: drain one bounded frame from the lossless buffer and send.
                // try_send keeps the select! loop responsive (input/keepalives never block);
                // on a full queue we RETAIN the frame and retry next tick — never drop.
                _ = frame_interval.tick() => {
                    // Auto-resume if the client never acked our sync — a lost/late ack
                    // must not freeze output forever (the `yes` + Ctrl-C hang).
                    if sync_pending
                        && sync_sent_at
                            .map(|t| t.elapsed() >= SYNC_ACK_TIMEOUT)
                            .unwrap_or(false)
                    {
                        warn!("[conn={conn_id}] SSH: sync ack timed out — resuming output");
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
                                    warn!("[conn={conn_id}] SSH: Failed to record frame: {e}");
                                }
                            }
                            match owner_sender.try_send(frame) {
                                Ok(()) => {
                                    sync_bytes_sent += frame_len;
                                    if sync_bytes_sent >= sync_threshold {
                                        let ts = std::time::SystemTime::now()
                                            .duration_since(std::time::UNIX_EPOCH)
                                            .unwrap_or_default()
                                            .as_millis();
                                        let ts_str = ts.to_string();
                                        let sync_instr = Bytes::from(format_instruction("sync", &[&ts_str]));
                                        if owner_sender.try_send(sync_instr).is_ok() {
                                            sync_pending = true;
                                            sync_sent_at = Some(std::time::Instant::now());
                                            sync_bytes_sent = 0;
                                        }
                                    }
                                }
                                Err(mpsc::error::TrySendError::Full(_)) => {
                                    // Retain (lossless) and retry next tick — never drop
                                    // terminal bytes.
                                    output_buf.requeue_front(frame_bytes);
                                    trace!("[conn={conn_id}] SSH: send queue full, retaining frame");
                                }
                                Err(mpsc::error::TrySendError::Closed(_)) => {
                                    info!("[conn={conn_id}] SSH: Client channel closed, ending session");
                                    break;
                                }
                            }
                        }
                    }
                }

                // SSH channel messages -> Terminal -> Client
                // Use `msg = channel.wait()` (not `Some(msg) = ...`) so that a None
                // return — meaning the SSH channel was closed without sending an explicit
                // EOF or ExitStatus message — is detected immediately and the loop exits.
                // With the Some-pattern, a None would silently disable the select arm
                // for that poll while the other arms kept running, delaying cleanup until
                // the next channel.data() write failed on a client keystroke.
                //
                // Gated on buffer depth: when we're OUTPUT_HIGH_WATERMARK behind, stop
                // reading so russh's channel window backpressures the server. Bounds memory
                // losslessly instead of dropping bytes; the SSH window caps how far ahead
                // the server can run while this arm is disabled.
                msg = channel.wait(), if output_buf.len() < OUTPUT_HIGH_WATERMARK => {
                    let msg = match msg {
                        Some(m) => m,
                        None => {
                            info!("[conn={conn_id}] SSH: Channel closed by server (no EOF/ExitStatus received)");
                            send_error_best_effort(&to_client, "SSH connection closed by server", 517).await;
                            break;
                        }
                    };
                    match msg {
                        russh::ChannelMsg::Data { ref data } => {
                            trace!("SSH: Received {} bytes from SSH server", data.len());

                            // If STDOUT pipe is enabled, send raw data to client
                            // This enables native terminal display (with ANSI escape codes)
                            if pipe_manager.is_stdout_enabled() {
                                let blob = pipe_blob_bytes(PIPE_STREAM_STDOUT, data);
                                send_and_record(&to_client, &mut recorder, blob).await
                                    .map_err(HandlerError::ChannelError)?;
                            }

                            // Check for OSC 52 clipboard sequences before processing
                            // Format: ESC ] 52 ; c ; base64_data ESC \ or BEL
                            // This is what tmux/vim use to copy to clipboard
                            if let Some(clipboard_data) = extract_osc52_clipboard(data) {
                                // Security: Check if copy is allowed
                                if !security.is_copy_allowed() {
                                    debug!("[conn={conn_id}] SSH: OSC 52 clipboard copy blocked (copy disabled)");
                                } else {
                                    debug!("[conn={conn_id}] SSH: Detected OSC 52 clipboard copy ({} bytes)", clipboard_data.len());

                                    // Send clipboard using Guacamole stream protocol.
                                    // format_clipboard_instructions counts Unicode codepoints
                                    // (not bytes) for all LENGTH fields, which is required by
                                    // the Guacamole protocol.  The hand-rolled approach that
                                    // used clipboard_data.len() (byte count) would corrupt the
                                    // stream for any non-ASCII clipboard content.
                                    let clipboard_stream_id: u32 = 1;
                                    let instrs = format_clipboard_instructions(&clipboard_data, clipboard_stream_id);
                                    for instr in instrs {
                                        send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                            .map_err(HandlerError::ChannelError)?;
                                    }
                                }
                            }

                            // Record output if recording is enabled
                            if let Some(ref mut rec) = recorder {
                                let _ = rec.record_output(data);
                            }

                            // Threat detection: analyze live terminal output from server
                            #[cfg(feature = "threat-detection")]
                            if let Some(ref detector) = threat_detector {
                                match detector.analyze_terminal_output(
                                    &threat_session_id,
                                    data,
                                    &username_for_threat,
                                    &hostname_for_threat,
                                    "ssh",
                                ).await {
                                    Ok(threat) => {
                                        if threat.should_terminate() {
                                            error!(
                                                "[conn={conn_id}] SSH: TERMINATING SESSION due to threat in terminal output: {}",
                                                threat.description
                                            );
                                            let msg = format!("Session terminated: {}", threat.description);
                                            send_error_best_effort(&to_client, &msg, 517).await;
                                            // Finalize typescript recording before exit (flushes buffer + appends GCM tag)
                                            detector.cleanup_session(&threat_session_id);
                                            return Ok(());
                                        }
                                    }
                                    Err(e) => {
                                        debug!("[conn={conn_id}] SSH: Threat detection error (non-fatal): {}", e);
                                    }
                                }
                            }

                            // Process terminal output (maintains server-side terminal state for
                            // mouse coordinate tracking). vt100 can panic on complex escape
                            // sequences; process_terminal_guarded catches the panic and resets.
                            process_terminal_guarded(
                                &mut terminal,
                                data,
                                current_rows,
                                current_cols,
                                scrollback_size,
                                &conn_id,
                            );

                            // Check for BEL character (0x07) and send audio beep to client
                            if data.contains(&0x07) {
                                debug!("[conn={conn_id}] SSH: BEL detected, sending audio beep");
                                send_bell(&to_client, 100).await?;
                            }

                            // Buffer server output losslessly; the frame timer flushes it in
                            // bounded frames. Terminal output is a byte stream — dropping any
                            // bytes corrupts xterm.js — so backpressure is applied by gating
                            // the channel.wait() arm on OUTPUT_HIGH_WATERMARK, never by dropping.
                            let filtered = self.dlp.filter(Bytes::copy_from_slice(data));
                            if !filtered.is_empty() {
                                output_buf.push(&filtered);
                            }
                        }
                        russh::ChannelMsg::ExitStatus { exit_status } => {
                            if exit_status == 0 {
                                info!("[conn={conn_id}] SSH handler: SSH session ended normally (exit status 0)");
                            } else {
                                warn!("[conn={conn_id}] SSH handler: SSH command exited with status: {}", exit_status);
                            }

                            let error_msg = format!("SSH session ended (exit status: {})", exit_status);
                            send_error_best_effort(&to_client, &error_msg, 517).await; // RESOURCE_CLOSED

                            break;
                        }
                        russh::ChannelMsg::Eof => {
                            info!("[conn={conn_id}] SSH handler: SSH channel EOF received");

                            send_error_best_effort(&to_client, "SSH connection closed by server", 517).await; // RESOURCE_CLOSED

                            break;
                        }
                        other => {
                            debug!("[conn={conn_id}] SSH handler: Received other channel message: {:?}", other);
                        }
                    }
                }

                // Viewer key/mouse input forwarded from a connected viewer with PRIV_CONTROL.
                // Only key opcodes arrive here (share_viewer.rs gates on opcode before forwarding).
                // Processed identically to direct from_client key input.
                viewer_bytes = viewer_input_rx.recv() => {
                    if let Some(msg) = viewer_bytes {
                        record_client_input(&mut recorder, &msg);
                        stats.record_input();
                        let msg_str = String::from_utf8_lossy(&msg);
                        if let Some(key_event) = parse_key_instruction(&msg_str) {
                            let key_out = handle_key_event(
                                key_event,
                                &mut modifier_state,
                                &mut mouse_selection,
                                &security,
                                &stored_clipboard,
                                &terminal,
                                backspace_code,
                                current_rows,
                                current_cols,
                                char_width,
                                char_height,
                            );
                            for instr in key_out.to_client {
                                let _ = send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await;
                            }
                            if let Some(new_cb) = key_out.new_clipboard {
                                stored_clipboard = new_cb;
                            }
                            if !key_out.to_ssh.is_empty()
                                && channel.data(key_out.to_ssh.as_ref()).await.is_err() {
                                    break;
                                }
                        }
                    }
                }

                // Client input -> SSH
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        info!("[conn={conn_id}] SSH handler: Client disconnected");
                        // No need to send error - client already disconnected
                        break;
                    };

                    // Record client-to-server instruction in .ses file
                    record_client_input(&mut recorder, &msg);
                    stats.record_input();

                    // Parse Guacamole instruction
                    let msg_str = String::from_utf8_lossy(&msg);

                    // Log the message opcode only — never log raw message content which may
                    // contain clipboard data (ZK violation).
                    if msg_str.contains("clipboard") || msg_str.contains("blob") {
                        let opcode_len = msg_str.find(',').unwrap_or(msg_str.len());
                        debug!("[conn={conn_id}] SSH: Received clipboard/blob message (opcode={}B, total={}B)",
                            opcode_len, msg.len());
                    } else {
                        trace!("[conn={conn_id}] SSH: Received client message ({}B)", msg.len());
                    }

                    if msg_str.starts_with("4.sync,") {
                        // Sync ACK from client — resume sending. No screen redraw; the
                        // client is just acknowledging our render-gating backpressure.
                        sync_pending = false;
                        sync_sent_at = None;
                    } else if let Some(key_event) = parse_key_instruction(&msg_str) {
                        let key_out = handle_key_event(
                            key_event,
                            &mut modifier_state,
                            &mut mouse_selection,
                            &security,
                            &stored_clipboard,
                            &terminal,
                            backspace_code,
                            current_rows,
                            current_cols,
                            char_width,
                            char_height,
                        );

                        // Send client instructions (overlays, clipboard)
                        for instr in key_out.to_client {
                            send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                .map_err(HandlerError::ChannelError)?;
                        }

                        // Update local clipboard
                        if let Some(new_cb) = key_out.new_clipboard {
                            stored_clipboard = new_cb;
                        }

                        // Send bytes to SSH channel
                        if !key_out.to_ssh.is_empty() {
                            // Record input if enabled
                            if let Some(ref mut rec) = recorder {
                                if recording_config.recording_include_keys {
                                    let _ = rec.record_input(&key_out.to_ssh);
                                }
                            }
                            channel.data(&key_out.to_ssh[..]).await
                                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                        }
                    } else if let Some(clipboard_text) = parse_clipboard_blob(&msg_str) {
                        // Clipboard blob instruction: Store clipboard data from client
                        // This is just synchronization - NOT a paste command!
                        // The actual paste happens when user presses Ctrl+Shift+V (keysym 'V' with ctrl+shift)

                        stored_clipboard = clipboard_text;
                        debug!("[conn={conn_id}] SSH: Clipboard updated - stored {} chars (waiting for Ctrl+Shift+V to paste)", stored_clipboard.len());
                    } else if msg_str.contains(".clipboard,") {
                        // Clipboard instruction received - this is just a SYNC, not a paste command!
                        // The Guacamole protocol sends clipboard instructions to sync clipboard state
                        // between client and server. This does NOT mean the user wants to paste.
                        debug!("[conn={conn_id}] SSH: Clipboard stream opened - syncing clipboard state (not pasting)");
                        trace!("[conn={conn_id}] SSH: Clipboard instruction: {}", msg_str);
                    } else if msg_str.contains(".size,") {
                        handle_resize(
                            &msg_str,
                            &mut terminal,
                            &mut channel,
                            &mut recorder,
                            char_width,
                            char_height,
                            &mut current_rows,
                            &mut current_cols,
                        ).await?;
                    } else if let Some(mouse_event) = parse_mouse_instruction(&msg_str) {
                        let mouse_out = handle_mouse_event(
                            mouse_event,
                            &mut mouse_selection,
                            &terminal,
                            &security,
                            char_width,
                            char_height,
                            current_rows,
                            current_cols,
                            &modifier_state,
                        );

                        // Send client instructions (overlays, clipboard)
                        for instr in mouse_out.to_client {
                            send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await
                                .map_err(HandlerError::ChannelError)?;
                        }

                        // Update local clipboard
                        if let Some(new_cb) = mouse_out.new_clipboard {
                            stored_clipboard = new_cb;
                        }

                        // Send X11 mouse sequences to SSH channel
                        if !mouse_out.server_bytes.is_empty() {
                            channel.data(&mouse_out.server_bytes[..]).await
                                .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                        }
                    } else if let Some(pipe_instr) = parse_pipe_instruction(&msg_str) {
                        // Handle incoming pipe stream (e.g., STDIN from client)
                        if pipe_instr.name == PIPE_NAME_STDIN {
                            debug!("[conn={conn_id}] SSH: STDIN pipe opened by client (stream {})", pipe_instr.stream_id);
                            pipe_manager.register_incoming(
                                pipe_instr.stream_id,
                                &pipe_instr.name,
                                &pipe_instr.mimetype,
                            );
                        } else {
                            debug!("[conn={conn_id}] SSH: Unknown pipe '{}' opened by client", pipe_instr.name);
                        }
                    } else if let Some(blob_instr) = parse_blob_instruction(&msg_str) {
                        // Handle blob data on STDIN pipe
                        if pipe_manager.is_stdin_stream(blob_instr.stream_id) {
                            // Security: Check if input is allowed
                            if security.read_only {
                                debug!("[conn={conn_id}] SSH: STDIN pipe data blocked (read-only mode)");
                            } else {
                                trace!("[conn={conn_id}] SSH: Received {} bytes on STDIN pipe", blob_instr.data.len());
                                channel.data(&blob_instr.data[..]).await
                                    .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
                            }
                        }
                    } else if let Some(end_stream_id) = parse_end_instruction(&msg_str) {
                        // Handle end of pipe stream
                        if pipe_manager.is_stdin_stream(end_stream_id) {
                            debug!("[conn={conn_id}] SSH: STDIN pipe closed by client");
                            pipe_manager.close(PIPE_NAME_STDIN);
                        }
                    } else if let Some(session_id) = share_id.as_deref() {
                        // Share control messages (share_create, share_revoke, etc.)
                        if let Ok(instr) = GuacamoleParser::parse_instruction(&msg) {
                            share_viewer::handle_owner_share_control(
                                session_id,
                                instr.opcode,
                                &instr.args,
                                &to_client,
                            )
                            .await;
                        }
                    }
                }
            }
        }

        // Close any open pipe streams
        let end_instructions = pipe_manager.close_all();
        for instr in end_instructions {
            let _ = send_and_record(&to_client, &mut recorder, Bytes::from(instr)).await;
        }

        // Record a final sync so the recording ends on a sync instruction
        // rather than on a mouse/key event. The ses recorder rewrites the
        // timestamp to session-relative, so the placeholder value here
        // doesn't matter.
        let _ = send_and_record(
            &to_client,
            &mut recorder,
            Bytes::from_static(b"4.sync,1.0;"),
        )
        .await;

        // Finalize recording
        if let Some(rec) = recorder {
            if let Err(e) = rec.finalize() {
                warn!("[conn={conn_id}] SSH: Failed to finalize recording: {}", e);
            } else {
                info!("[conn={conn_id}] SSH: Session recording finalized");
            }
        }

        // Clean up threat detection session state to prevent memory leak
        #[cfg(feature = "threat-detection")]
        if let Some(ref detector) = threat_detector {
            detector.cleanup_session(&threat_session_id);
        }

        // Deregister shared session and notify viewers before final disconnect.
        if let Some(ref sid) = share_id {
            owner_sender.owner_disconnect(sid);
        }

        info!("[conn={conn_id}] session complete: {}", stats.summary());
        send_disconnect(&to_client).await;
        info!("[conn={conn_id}] SSH handler connection ended");
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
// Authentication helper
// ---------------------------------------------------------------------------

/// Smallest keepalive interval libssh2 accepts, and therefore the smallest
/// guacd can be asked for. guacd rounds a requested `1` up to this value.
pub(crate) const MIN_SERVER_ALIVE_INTERVAL_SECS: u64 = 2;

/// Parse `server-alive-interval` (seconds) with guacd's semantics.
///
/// guacd hands the value to `libssh2_keepalive_config()`, where 0 disables
/// keepalive and 2 is the minimum configurable value; negative values are
/// converted to 0 and 1 is rounded up to 2 (guacamole-server
/// `src/common-ssh/ssh.c`). A missing or unparseable value falls back to 0,
/// matching `guac_user_parse_args_int()`'s default rather than failing the
/// connection.
pub(crate) fn parse_server_alive_interval(params: &HashMap<String, String>) -> u64 {
    let raw = match params
        .get("server-alive-interval")
        .or_else(|| params.get("server_alive_interval"))
    {
        Some(value) => value.trim(),
        None => return 0,
    };

    match raw.parse::<i64>() {
        Ok(secs) if secs <= 0 => 0,
        Ok(secs) => (secs as u64).max(MIN_SERVER_ALIVE_INTERVAL_SECS),
        Err(_) => {
            warn!("SSH: ignoring non-numeric server-alive-interval {raw:?}; keepalive disabled");
            0
        }
    }
}

/// Build the russh client config, arming the keepalive timer when
/// `server-alive-interval` requested one.
///
/// russh sends a `keepalive@openssh.com` global request with `want_reply` after
/// `keepalive_interval` of silence and drops the session once `keepalive_max`
/// (3 by default) go unanswered. libssh2 — and so guacd — sends on a fixed
/// interval and never drops the session for missing replies, so guacr detects a
/// wedged server that guacd would hold open.
///
/// russh::Preferred::DEFAULT leads with ChaCha20-Poly1305 (cipher), Curve25519
/// (kex), and Ed25519 (host key) — none are FIPS-approved algorithm choices, and
/// the ring crate used internally is not a FIPS 140-2 certified module. True FIPS
/// compliance requires switching the crypto backend to aws-lc-rs with FIPS mode;
/// algorithm-list filtering alone is insufficient.
pub(crate) fn ssh_client_config(server_alive_interval_secs: u64) -> client::Config {
    let mut config = client::Config::default();
    if server_alive_interval_secs > 0 {
        config.keepalive_interval = Some(Duration::from_secs(server_alive_interval_secs));
    }
    config
}

/// Build the `size` instruction that initializes the terminal display.
///
/// Format is `size,<layer>,<width>,<height>` — layer 0 is the main display layer.
/// The layer argument is not optional: omitting it shifts width into the layer slot
/// and leaves height unset. Pixel dimensions are the character grid scaled by the
/// character cell size, matching `parse_display_size` on the way in.
pub(crate) fn display_size_instruction(
    cols: u16,
    rows: u16,
    char_width: u32,
    char_height: u32,
) -> String {
    format_size(0, cols as u32 * char_width, rows as u32 * char_height)
}

/// Process terminal data with panic recovery.
///
/// Wraps `terminal.process(data)` in `catch_unwind` so that a vt100 panic on
/// a malformed escape sequence (e.g. cmatrix terminal restore) does not crash
/// the handler task.  On panic the terminal is reset to a fresh state so the
/// session can continue; on a non-fatal error the error is logged and the
/// terminal state is left as-is.
///
/// Used in both the main event loop and `collect_banner` to ensure consistent
/// panic handling across all sites that feed server data into the emulator.
pub(crate) fn process_terminal_guarded(
    terminal: &mut TerminalEmulator,
    data: &[u8],
    rows: u16,
    cols: u16,
    scrollback_size: usize,
    conn_id: &str,
) {
    match std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| terminal.process(data))) {
        Ok(Ok(())) => {}
        Ok(Err(e)) => {
            warn!("[conn={conn_id}] SSH: Terminal emulator error (non-fatal): {e}");
        }
        Err(_) => {
            warn!(
                "[conn={conn_id}] SSH: Terminal emulator panicked on escape sequence \
                 (resetting state, session continues)"
            );
            *terminal = TerminalEmulator::new_with_scrollback(rows, cols, scrollback_size);
        }
    }
}

/// Map a HandlerError to a user-facing message and status code, send the error
/// to the client via best-effort, then return the error unchanged.
async fn report_and_fail(to_client: &mpsc::Sender<Bytes>, err: HandlerError) -> HandlerError {
    let (message, status_code) = match &err {
        HandlerError::MissingParameter(p) => (
            format!("Missing required parameter: {}", p),
            STATUS_UPSTREAM_ERROR,
        ),
        HandlerError::ConnectionFailed(msg) => {
            if msg.contains("timeout") || msg.contains("timed out") {
                (
                    format!("Connection timeout: {}", msg),
                    STATUS_UPSTREAM_TIMEOUT,
                )
            } else {
                (format!("Connection failed: {}", msg), STATUS_UPSTREAM_ERROR)
            }
        }
        HandlerError::AuthenticationFailed(msg) => {
            if msg.contains("Host key") || msg.contains("fingerprint") {
                (
                    format!("Host key verification failed: {}", msg),
                    STATUS_UPSTREAM_ERROR,
                )
            } else if msg.contains("timeout") || msg.contains("timed out") {
                (
                    format!("Authentication timeout: {}", msg),
                    STATUS_UPSTREAM_TIMEOUT,
                )
            } else {
                (
                    format!("Authentication failed: {}", msg),
                    STATUS_CLIENT_UNAUTHORIZED,
                )
            }
        }
        _ => (err.to_string(), STATUS_UPSTREAM_ERROR),
    };
    send_error_best_effort(to_client, &message, status_code).await;
    err
}

#[allow(clippy::too_many_arguments)]
async fn authenticate(
    sh: &mut client::Handle<SshClientHandler>,
    username: String,
    password: Option<&str>,
    private_key: Option<&str>,
    passphrase: Option<&str>,
    public_key_cert: Option<&str>,
    auth_timeout: Duration,
    to_client: &mpsc::Sender<Bytes>,
) -> guacr_handlers::Result<()> {
    let auth_result = if let Some(pwd) = password {
        debug!("SSH handler: Authenticating with password");
        let pwd_for_kbi = pwd.to_string();
        let password_result = tokio::time::timeout(
            auth_timeout,
            sh.authenticate_password(username.clone(), pwd),
        )
        .await
        .map_err(|_| {
            error!("SSH handler: Authentication timed out");
            HandlerError::AuthenticationFailed("Authentication timed out".to_string())
        });

        // If password auth was rejected (Ok(Ok(false))), fall back to
        // keyboard-interactive. Many SSH servers (OpenSSH default config)
        // disable the "password" method and only allow "keyboard-interactive",
        // which is functionally equivalent but uses a challenge-response flow.
        // libssh2/libguac handles this transparently; we must do it explicitly.
        match &password_result {
            Ok(Ok(false)) => {
                info!("SSH handler: Password auth rejected, trying keyboard-interactive");
                tokio::time::timeout(auth_timeout, async {
                    use russh::client::KeyboardInteractiveAuthResponse;
                    let mut resp = sh
                        .authenticate_keyboard_interactive_start(username.clone(), None)
                        .await?;
                    loop {
                        match resp {
                            KeyboardInteractiveAuthResponse::Success => return Ok(true),
                            KeyboardInteractiveAuthResponse::Failure => return Ok(false),
                            KeyboardInteractiveAuthResponse::InfoRequest { prompts, .. } => {
                                // Respond to each prompt with the password
                                // (standard PAM password prompt sends one prompt)
                                let responses: Vec<String> =
                                    prompts.iter().map(|_| pwd_for_kbi.clone()).collect();
                                resp = sh
                                    .authenticate_keyboard_interactive_respond(responses)
                                    .await?;
                            }
                        }
                    }
                })
                .await
                .map_err(|_| {
                    error!("SSH handler: Keyboard-interactive authentication timed out");
                    HandlerError::AuthenticationFailed("Authentication timed out".to_string())
                })
            }
            _ => password_result,
        }
    } else if let Some(key_pem) = private_key {
        debug!("SSH handler: Authenticating with private key");

        // Parse private key (supports OpenSSH, PEM, and PKCS#8 formats)
        // russh_keys::decode_secret_key handles all formats and optional passphrase
        debug!(
            "SSH handler: Decoding private key (encrypted: {})",
            passphrase.is_some()
        );
        let key_pair = match russh_keys::decode_secret_key(key_pem, passphrase) {
            Ok(k) => k,
            Err(e) => {
                error!("SSH handler: Failed to decode private key: {}", e);
                let err = if passphrase.is_some() {
                    HandlerError::AuthenticationFailed(format!(
                        "Invalid private key or passphrase: {}",
                        e
                    ))
                } else {
                    HandlerError::AuthenticationFailed(format!("Invalid private key format: {}", e))
                };
                return Err(report_and_fail(to_client, err).await);
            }
        };

        if let Some(cert_str) = public_key_cert {
            debug!("SSH handler: Certificate provided, using certificate-based authentication");

            // Parse OpenSSH certificate
            let certificate = match cert_str.trim().parse::<Certificate>() {
                Ok(cert) => cert,
                Err(e) => {
                    error!("SSH handler: Failed to parse SSH certificate: {}", e);
                    let err = HandlerError::AuthenticationFailed(format!(
                        "Invalid SSH certificate format: {}",
                        e
                    ));
                    return Err(report_and_fail(to_client, err).await);
                }
            };

            debug!("SSH handler: Certificate parsed successfully, authenticating with certificate");
            tokio::time::timeout(
                auth_timeout,
                sh.authenticate_openssh_cert(username.clone(), Arc::new(key_pair), certificate),
            )
            .await
            .map_err(|_| {
                error!("SSH handler: Certificate authentication timed out");
                HandlerError::AuthenticationFailed("Authentication timed out".to_string())
            })
        } else {
            debug!("SSH handler: Private key decoded successfully, authenticating with public key");
            tokio::time::timeout(
                auth_timeout,
                sh.authenticate_publickey(username.clone(), Arc::new(key_pair)),
            )
            .await
            .map_err(|_| {
                error!("SSH handler: Authentication timed out");
                HandlerError::AuthenticationFailed("Authentication timed out".to_string())
            })
        }
    } else {
        error!("SSH handler: No authentication method provided");
        let err = HandlerError::MissingParameter("password or private_key".to_string());
        return Err(report_and_fail(to_client, err).await);
    };

    let auth_result = match auth_result {
        Ok(r) => r,
        Err(e) => return Err(report_and_fail(to_client, e).await),
    };

    let auth_success = match auth_result {
        Ok(success) => success,
        Err(e) => {
            error!("SSH handler: Authentication error: {}", e);
            let err = HandlerError::AuthenticationFailed(e.to_string());
            return Err(report_and_fail(to_client, err).await);
        }
    };

    if !auth_success {
        error!("SSH handler: Authentication failed - wrong credentials");
        let err = HandlerError::AuthenticationFailed("Authentication failed".to_string());
        return Err(report_and_fail(to_client, err).await);
    }

    info!("SSH handler: Authentication successful");
    Ok(())
}

// ---------------------------------------------------------------------------
// Session channel helper
// ---------------------------------------------------------------------------

async fn open_session_channel(
    sh: &mut client::Handle<SshClientHandler>,
    terminal_config: &TerminalConfig,
    rows: u16,
    cols: u16,
    params: &HashMap<String, String>,
) -> guacr_handlers::Result<russh::Channel<russh::client::Msg>> {
    let channel = sh
        .channel_open_session()
        .await
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    channel
        .request_pty(
            false,
            terminal_config.term_type(),
            cols as u32,
            rows as u32,
            0,
            0,
            &[
                (Pty::ECHO, 1),   // echo input characters
                (Pty::ICANON, 1), // canonical (line) mode
                (Pty::ISIG, 1),   // enable signals (Ctrl+C, Ctrl+Z)
                (Pty::IEXTEN, 1), // enable extended input processing
                (Pty::ICRNL, 1),  // map CR to NL on input (Enter key)
                (Pty::OPOST, 1),  // enable output processing
                (Pty::ONLCR, 1),  // map NL to CR+NL on output
                (Pty::ECHOE, 1),  // echo erase character (Backspace)
                (Pty::ECHOK, 1),  // echo kill character
            ],
        )
        .await
        .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

    // Set environment variables (locale/timezone) before shell/command
    // Note: Many SSH servers have AcceptEnv disabled by default, so these may be ignored
    if let Some(locale) = params.get("locale") {
        debug!("SSH: Setting LANG={}", locale);
        let _ = channel.set_env(false, "LANG", locale.as_str()).await;
    }
    if let Some(timezone) = params.get("timezone") {
        debug!("SSH: Setting TZ={}", timezone);
        let _ = channel.set_env(false, "TZ", timezone.as_str()).await;
    }

    // Either execute a specific command or open interactive shell
    if let Some(command) = params.get("command") {
        // Intentionally log only at debug — command strings may contain tokens or credentials.
        // info! would expose them in production logs.
        debug!("SSH: Executing command ({} bytes)", command.len());
        channel
            .exec(false, command.as_str())
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        debug!("SSH handler: Command execution started");
    } else {
        channel
            .request_shell(false)
            .await
            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;
        debug!("SSH handler: SSH shell established");
    }

    Ok(channel)
}

// ---------------------------------------------------------------------------
// Banner collection helper
// ---------------------------------------------------------------------------

/// Collects initial SSH banner/MOTD data from the channel.
///
/// Returns the raw bytes so the caller can forward them as `terminal-data` to
/// xterm.js. The bytes are also processed into `terminal` (TerminalEmulator) so
/// server-side state (dirty tracking, scrollback) stays consistent.
///
/// A single outer `tokio::time::timeout` of 500 ms wraps the entire loop so
/// only one timer is allocated regardless of how many packets arrive.
/// Per-iteration timeouts would allocate a timer on every packet, which on
/// Windows (15–16 ms timer granularity) balloons a 10-packet banner into 2 s+.
async fn collect_banner(
    channel: &mut russh::Channel<russh::client::Msg>,
    terminal: &mut TerminalEmulator,
    rows: u16,
    cols: u16,
    scrollback_size: usize,
) -> Vec<u8> {
    debug!("SSH: Checking for initial banner data...");
    let mut raw: Vec<u8> = Vec::new();

    // One timer for the entire banner window.  If the server sends nothing
    // within 500 ms, we proceed to the interactive loop immediately.
    let result = tokio::time::timeout(std::time::Duration::from_millis(500), async {
        loop {
            match channel.wait().await {
                Some(russh::ChannelMsg::Data { ref data }) => {
                    raw.extend_from_slice(data);
                    trace!(
                        "SSH: Received {} bytes of initial banner data (total: {})",
                        data.len(),
                        raw.len(),
                    );
                    process_terminal_guarded(terminal, data, rows, cols, scrollback_size, "banner");
                }
                Some(_other) => {
                    debug!("SSH: Received non-data message during banner check");
                }
                None => {
                    warn!("SSH: Channel closed during banner check");
                    break;
                }
            }
        }
    })
    .await;

    match result {
        Ok(()) => {
            // Channel closed while collecting banner — raw is as complete as it can be.
        }
        Err(_timeout) => {
            debug!(
                "SSH: Banner collection complete (timeout, total {} bytes)",
                raw.len()
            );
        }
    }
    raw
}

// ---------------------------------------------------------------------------
// Key event helper
// ---------------------------------------------------------------------------

pub(crate) struct KeyEventOutput {
    /// Instructions to send to the Guacamole client (in order)
    pub(crate) to_client: Vec<String>,
    /// Bytes to write to the SSH channel
    pub(crate) to_ssh: Vec<u8>,
    /// New clipboard content (Some if select-all was triggered)
    pub(crate) new_clipboard: Option<String>,
}

impl KeyEventOutput {
    fn empty() -> Self {
        Self {
            to_client: Vec::new(),
            to_ssh: Vec::new(),
            new_clipboard: None,
        }
    }
}

#[allow(clippy::too_many_arguments)]
pub(crate) fn handle_key_event(
    key_event: guacr_terminal::KeyEvent,
    modifier_state: &mut ModifierState,
    mouse_selection: &mut MouseSelection,
    security: &HandlerSecuritySettings,
    stored_clipboard: &str,
    terminal: &TerminalEmulator,
    backspace_code: u8,
    current_rows: u16,
    current_cols: u16,
    char_width: u32,
    char_height: u32,
) -> KeyEventOutput {
    trace!(
        "SSH: Key event - keysym={} (0x{:04X}), pressed={}, ctrl={}, shift={}, alt={}",
        key_event.keysym,
        key_event.keysym,
        key_event.pressed,
        modifier_state.control,
        modifier_state.shift,
        modifier_state.alt
    );

    // Update modifier state (Ctrl, Shift, Alt)
    // Returns true if this was a modifier key (don't send to SSH)
    if modifier_state.update_modifier(key_event.keysym, key_event.pressed) {
        debug!(
            "SSH: Modifier key updated - ctrl={}, shift={}, alt={}",
            modifier_state.control, modifier_state.shift, modifier_state.alt
        );
        return KeyEventOutput::empty();
    }

    let mut out = KeyEventOutput::empty();

    // Clear any active selection overlay on key press (not release)
    if key_event.pressed && mouse_selection.start.is_some() {
        mouse_selection.reset();
        let clear = format_clear_selection_instructions();
        for instr in clear {
            out.to_client.push(instr);
        }
    }

    // Security: Check read-only mode
    if security.read_only
        && !is_keyboard_event_allowed_readonly(key_event.keysym, modifier_state.control)
    {
        trace!("SSH: Keyboard input blocked (read-only mode)");
        return out;
    }

    // Handle paste shortcuts (matching guacd's behavior):
    // - Ctrl+Shift+V (Linux/Windows): keysym 'V' (0x56) with ctrl+shift
    // - Cmd+V (Mac): keysym 'v' (0x76) with meta
    let is_paste = key_event.pressed
        && ((key_event.keysym == 0x56 && modifier_state.control && modifier_state.shift)
            || (key_event.keysym == 0x76 && modifier_state.meta));

    if is_paste {
        if !security.is_paste_allowed() {
            debug!("SSH: Paste blocked (disabled or read-only mode)");
            return out;
        }

        if stored_clipboard.is_empty() {
            debug!("SSH: Paste shortcut pressed but clipboard is empty");
            return out;
        }

        // Check clipboard buffer size limit
        let max_size = security.clipboard_buffer_size;
        let paste_text = if stored_clipboard.len() > max_size {
            warn!(
                "SSH: Clipboard truncated from {} to {} bytes",
                stored_clipboard.len(),
                max_size
            );
            &stored_clipboard[..max_size]
        } else {
            stored_clipboard
        };

        debug!(
            "SSH: Paste shortcut - Pasting {} chars from clipboard",
            paste_text.len()
        );

        // Send using bracketed paste mode for safety
        let mut paste_data = Vec::new();
        paste_data.extend_from_slice(b"\x1b[200~");
        paste_data.extend_from_slice(paste_text.as_bytes());
        paste_data.extend_from_slice(b"\x1b[201~");

        out.to_ssh = paste_data;
        return out;
    }

    // Handle copy shortcuts - ignore them since selection already copies
    // - Ctrl+Shift+C (Linux/Windows): keysym 'C' (0x43) with ctrl+shift
    // - Cmd+C (Mac): keysym 'c' (0x63) with meta
    let is_copy = key_event.pressed
        && ((key_event.keysym == 0x43 && modifier_state.control && modifier_state.shift)
            || (key_event.keysym == 0x63 && modifier_state.meta));

    if is_copy {
        debug!("SSH: Copy shortcut pressed - ignoring (selection already copies)");
        return out;
    }

    // Handle select-all shortcut (selects entire terminal + copies to clipboard)
    // - Ctrl+Shift+A (Linux/Windows): keysym 'A' (0x41) with ctrl+shift
    // - Cmd+A (Mac): keysym 'a' (0x61) with meta
    let is_select_all = key_event.pressed
        && ((key_event.keysym == 0x41 && modifier_state.control && modifier_state.shift)
            || (key_event.keysym == 0x61 && modifier_state.meta));

    if is_select_all {
        let last_row = current_rows.saturating_sub(1);
        let last_col = current_cols.saturating_sub(1);

        // Show selection overlay (entire terminal)
        let overlay = format_selection_overlay_instructions(
            (0, 0),
            (last_row, last_col),
            char_width,
            char_height,
            current_cols,
            current_rows,
        );
        for instr in overlay {
            out.to_client.push(instr);
        }

        // Extract all text and send to clipboard
        let text = extract_selection_text(terminal, (0, 0), (last_row, last_col), current_cols);

        if !text.is_empty() {
            info!("SSH: Select all - {} chars copied to clipboard", text.len());
            let clipboard_stream_id = 10;
            let clipboard_instructions = format_clipboard_instructions(&text, clipboard_stream_id);
            for instr in clipboard_instructions {
                out.to_client.push(instr);
            }
            out.new_clipboard = Some(text);
        }

        // Clear overlay after a brief visual flash
        let clear = format_clear_selection_instructions();
        for instr in clear {
            out.to_client.push(instr);
        }

        return out;
    }

    // Convert to terminal bytes with modifier state, backspace, and application cursor mode
    let application_cursor = terminal.is_application_cursor_mode();
    let kitty_level = terminal.kitty_keyboard_level();

    // Log arrow keys to help debug mode switching
    if matches!(key_event.keysym, 0xFF51..=0xFF54) {
        trace!(
            "SSH: Arrow key 0x{:X} in {} mode, kitty_level={}",
            key_event.keysym,
            if application_cursor {
                "application"
            } else {
                "normal"
            },
            kitty_level
        );
    }

    // Use Kitty keyboard protocol if enabled, otherwise use legacy
    let bytes = if kitty_level > 0 {
        trace!("SSH: Using Kitty keyboard protocol level {}", kitty_level);
        x11_keysym_to_kitty_sequence(
            key_event.keysym,
            key_event.pressed,
            Some(modifier_state),
            backspace_code,
            application_cursor,
            kitty_level,
        )
    } else {
        x11_keysym_to_bytes_with_modes(
            key_event.keysym,
            key_event.pressed,
            Some(modifier_state),
            backspace_code,
            application_cursor,
        )
    };

    trace!("SSH: Key converted to {} bytes: {:?}", bytes.len(), bytes);
    out.to_ssh = bytes;
    out
}

// Resize helper
// ---------------------------------------------------------------------------

#[allow(clippy::too_many_arguments)]
async fn handle_resize(
    msg_str: &str,
    terminal: &mut TerminalEmulator,
    channel: &mut russh::Channel<russh::client::Msg>,
    recorder: &mut Option<MultiFormatRecorder>,
    char_width: u32,
    char_height: u32,
    current_rows: &mut u16,
    current_cols: &mut u16,
) -> guacr_handlers::Result<()> {
    // Handle resize - extract exact pixel dimensions from browser
    // Format: "4.size,4.1057,3.768;" where args are: width, height
    if let Some(args_part) = msg_str.split_once(".size,") {
        let parts: Vec<&str> = args_part.1.split(',').collect();
        if parts.len() >= 2 {
            if let Some((_, width_str)) = parts[0].split_once('.') {
                let height_part = parts[1].trim_end_matches(';');
                if let Some((_, height_str)) = height_part.split_once('.') {
                    if let (Ok(new_width_px), Ok(new_height_px)) =
                        (width_str.parse::<u32>(), height_str.parse::<u32>())
                    {
                        // Validate dimensions
                        if new_width_px == 0 || new_height_px == 0 {
                            warn!(
                                "SSH: Ignoring resize with zero dimensions ({}x{})",
                                new_width_px, new_height_px
                            );
                            return Ok(());
                        }

                        let new_cols = (new_width_px / char_width).clamp(20, 500) as u16;
                        let new_rows = (new_height_px / char_height).clamp(10, 200) as u16;

                        if new_rows == *current_rows && new_cols == *current_cols {
                            debug!(
                                "SSH: Ignoring resize - dimensions unchanged ({}x{} chars)",
                                *current_cols, *current_rows
                            );
                            return Ok(());
                        }

                        // Resize terminal emulator — vt100::set_size can panic on edge cases
                        if std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                            terminal.resize(new_rows, new_cols)
                        }))
                        .is_err()
                        {
                            warn!("SSH: Terminal emulator panicked on resize (session continues with stale state)");
                        }

                        // Update current dimensions
                        *current_rows = new_rows;
                        *current_cols = new_cols;

                        // Send PTY window change to SSH server
                        channel
                            .window_change(new_cols as u32, new_rows as u32, 0, 0)
                            .await
                            .map_err(|e| HandlerError::ProtocolError(e.to_string()))?;

                        info!(
                            "SSH: Resize {}x{} px → {}x{} chars (xterm.js handles display)",
                            new_width_px, new_height_px, new_cols, new_rows,
                        );

                        // Record resize event
                        if let Some(ref mut rec) = *recorder {
                            let _ = rec.record_resize(new_cols, new_rows);
                        }
                    }
                }
            }
        }
    }
    Ok(())
}

/// Extract clipboard data from OSC 52 escape sequence
/// Format: ESC ] 52 ; c ; <base64_data> ESC \ or BEL
/// Returns decoded clipboard data if found
pub(crate) fn extract_osc52_clipboard(data: &[u8]) -> Option<String> {
    // OSC 52: ESC ] 52 ; c ; <base64> ST   where ST = BEL (0x07) or ESC \ (0x1b 0x5c)
    // Scans the entire buffer and returns the LAST complete sequence so that
    // when two sequences arrive in the same chunk (e.g. tmux batching clipboard
    // operations) the most recent clipboard content wins.
    let mut last: Option<String> = None;
    let mut i = 0;
    while i + 1 < data.len() {
        if data[i] != 0x1b || data[i + 1] != 0x5d {
            i += 1;
            continue;
        }
        let osc_start = i + 2;
        let prefix_len = if data[osc_start..].starts_with(b"52;c;") {
            5
        } else if data[osc_start..].starts_with(b"52;;") {
            4
        } else {
            i += 1;
            continue;
        };
        let data_start = osc_start + prefix_len;
        // Find terminator (BEL or ESC \), advancing i past this sequence.
        let mut j = data_start;
        let mut found = false;
        while j < data.len() {
            if data[j] == 0x07 {
                // BEL terminator
                if let Ok(decoded) =
                    base64::engine::general_purpose::STANDARD.decode(&data[data_start..j])
                {
                    if let Ok(text) = String::from_utf8(decoded) {
                        last = Some(text);
                    }
                }
                i = j + 1;
                found = true;
                break;
            } else if j + 1 < data.len() && data[j] == 0x1b && data[j + 1] == 0x5c {
                // ST (ESC \) terminator
                if let Ok(decoded) =
                    base64::engine::general_purpose::STANDARD.decode(&data[data_start..j])
                {
                    if let Ok(text) = String::from_utf8(decoded) {
                        last = Some(text);
                    }
                }
                i = j + 2;
                found = true;
                break;
            }
            j += 1;
        }
        if !found {
            i += 1;
        }
    }
    last
}

/// SSH client handler with host key verification support
struct SshClientHandler {
    verifier: HostKeyVerifier,
    hostname: String,
    port: u16,
}

impl SshClientHandler {
    fn new(hostname: String, port: u16, config: HostKeyConfig) -> Self {
        Self {
            verifier: HostKeyVerifier::new(config),
            hostname,
            port,
        }
    }
}

#[async_trait]
impl client::Handler for SshClientHandler {
    type Error = russh::Error;

    async fn check_server_key(
        &mut self,
        server_public_key: &key::PublicKey,
    ) -> Result<bool, Self::Error> {
        use guacr_handlers::HostKeyResult;

        // Get key type and raw bytes from the public key
        let key_type = server_public_key.name();
        let key_bytes = server_public_key.public_key_bytes();

        // Verify the host key
        let result = self
            .verifier
            .verify(&self.hostname, self.port, key_type, &key_bytes);

        match &result {
            HostKeyResult::Verified => {
                info!("SSH: Host key verified for {}:{}", self.hostname, self.port);
            }
            HostKeyResult::Skipped => {
                warn!(
                    "SSH: Host key verification skipped for {}:{} (INSECURE)",
                    self.hostname, self.port
                );
            }
            HostKeyResult::NotConfigured => {
                if let Some(warning) = result.security_warning() {
                    warn!("SSH [{}:{}]: {}", self.hostname, self.port, warning);
                }
            }
            HostKeyResult::UnknownHost => {
                warn!(
                    "SSH: Unknown host {}:{} - not in known_hosts",
                    self.hostname, self.port
                );
            }
            HostKeyResult::Mismatch { expected, actual } => {
                error!(
                    "SSH: HOST KEY MISMATCH for {}:{}\nExpected: {}\nActual: {}",
                    self.hostname, self.port, expected, actual
                );
            }
        }

        // Check if connection should be allowed based on config
        if result.is_allowed(&self.verifier.config) {
            Ok(true)
        } else {
            // Return error with descriptive message
            if let Some(msg) = result.error_message() {
                error!("SSH: {}", msg);
            }
            Ok(false) // Reject the connection
        }
    }
}

// Event-based handler implementation
#[async_trait]
impl EventBasedHandler for SshHandler {
    fn name(&self) -> &str {
        "ssh"
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
            256,
        )
        .await
    }
}
