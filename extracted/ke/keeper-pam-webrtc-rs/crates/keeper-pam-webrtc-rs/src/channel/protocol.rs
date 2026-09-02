use crate::runtime::get_runtime;
use crate::unlikely;

/// Parses an `otpauth://totp/...?algorithm=...&digits=...&period=...&secret=...` URI.
/// Returns `(algorithm, digits, period, secret)` only if all four params are present;
/// returns `None` if the URI has no query string or any required param is missing.
fn parse_totp_uri(uri: &str) -> Option<(String, String, String, String)> {
    let params_str = uri.split_once('?')?.1;
    let mut algorithm = None;
    let mut digits = None;
    let mut period = None;
    let mut secret = None;
    for kv in params_str.split('&') {
        if let Some((k, v)) = kv.split_once('=') {
            match k {
                "algorithm" => algorithm = Some(v.to_string()),
                "digits" => digits = Some(v.to_string()),
                "period" => period = Some(v.to_string()),
                "secret" => secret = Some(v.to_string()),
                _ => {}
            }
        }
    }
    Some((algorithm?, digits?, period?, secret?))
}
use anyhow::{anyhow, Result};
use bytes::{Buf, BufMut};
use log::{debug, error, info, warn};
use std::sync::Arc;

use super::core::Channel;
use super::types::ActiveProtocol;
use crate::tube_protocol::{CloseConnectionReason, ControlMessage, CONN_NO_LEN};

// Import from the new connect_as module
use super::connect_as::{decrypt_connect_as_payload, patch_keeperdb_url_credentials};

// Constants for ConnectAs, similar to those in connections.rs
const CONNECT_AS_DETAILS_LEN_FIELD_BYTES: usize = 4;
const CONNECT_AS_PUBLIC_KEY_BYTES: usize = 65; // As per Python: 65-byte public key
const CONNECT_AS_NONCE_BYTES: usize = 12; // As per Python: 12 byte nonce

// Re-export SOCKS5 success response constant from pam-socks5 crate (used by tests)
#[cfg(test)]
pub(crate) const SOCKS5_SUCCESS_RESPONSE: [u8; 10] = pam_socks5::SOCKS5_SUCCESS_RESPONSE;
use p256::pkcs8::DecodePrivateKey; // Trait for from_pkcs8_pem
use p256::SecretKey as P256SecretKey;

impl Channel {
    pub(crate) fn setup_webrtc_state_monitoring(&mut self) {
        let webrtc = self.webrtc.clone();
        let channel_id_base = self.channel_id.clone(); // Base clone for the function scope
        let conversation_id_base = self.conversation_id.clone();

        let last_state = webrtc.ready_state();
        let (state_tx, mut state_rx) = tokio::sync::mpsc::channel(8);

        let data_channel = webrtc.data_channel.clone();

        let state_tx_open = state_tx.clone();
        let channel_id_for_open = channel_id_base.clone(); // Clone for on_open
        let conversation_id_for_open = conversation_id_base.clone();

        // Clone the WebRTCDataChannel's shared notification mechanism so we can
        // notify waiters when the channel opens. This is important because we're
        // overwriting the on_open callback set in WebRTCDataChannel::new().
        let is_open_flag = webrtc.is_open.clone();
        let open_notify = webrtc.open_notify.clone();

        // Clone task tracking for proper resource management
        let state_tasks_for_open = self.state_monitoring_tasks.clone();
        let ice_restart_active_for_open = self.ice_restart_active.clone();

        data_channel.on_open(Box::new(move || {
            // Update the shared is_open flag and notify waiters
            // This ensures wait_for_channel_open() works even though we replaced the callback
            is_open_flag.store(true, std::sync::atomic::Ordering::Release);
            open_notify.notify_waiters();
            // ICE restart completed — stop sending nops to guacd.
            ice_restart_active_for_open.store(false, std::sync::atomic::Ordering::Release);

            let tx = state_tx_open.clone();
            let channel_id_log = channel_id_for_open.clone(); // Clone for async block
            let conversation_id_log = conversation_id_for_open.clone();

            // Proper resource handling: Store AbortHandle for explicit lifecycle management
            let handle = tokio::spawn(async move {
                if let Err(e) = tx.send("Open".to_string()).await {
                    warn!(
                        "Failed to send open state notification (channel_id: {}, conversation_id: {}, error: {})",
                        channel_id_log, conversation_id_log, e
                    );
                }
            });

            // Store abort handle synchronously - no race condition possible
            let abort_handle = handle.abort_handle();
            state_tasks_for_open.lock().push(abort_handle);

            Box::pin(async {})
        }));

        let state_tx_close = state_tx.clone();
        let channel_id_for_close = channel_id_base.clone(); // Clone for on_close
        let conversation_id_for_close = conversation_id_base.clone();
        let state_tasks_for_close = self.state_monitoring_tasks.clone();
        let ice_restart_active_for_close = self.ice_restart_active.clone();
        let should_exit_for_close = self.should_exit.clone();
        let active_protocol_for_close = self.active_protocol;

        // KCM-style teardown: take and drop tx_from_dc when DataChannel closes so rx_from_dc.recv()
        // returns None and channel.run() can exit. The sender is shared with on_message; we take
        // the single owner here so dropping it closes the channel.
        let tx_from_dc_for_close = self.tx_from_dc.clone();

        data_channel.on_close(Box::new(move || {
            // Take and drop the sender so rx_from_dc.recv() returns None and channel.run() exits
            let _ = tx_from_dc_for_close.lock().take();

            let tx = state_tx_close.clone();
            let channel_id_log = channel_id_for_close.clone(); // Clone for async block
            let conversation_id_log = conversation_id_for_close.clone();

            // Proper resource handling: Store AbortHandle for explicit lifecycle management
            let handle = tokio::spawn(async move {
                if let Err(e) = tx.send("Closed".to_string()).await {
                    warn!(
                        "Failed to send close state notification (channel_id: {}, conversation_id: {}, error: {})",
                        channel_id_log, conversation_id_log, e
                    );
                }
            });

            // Store abort handle synchronously - no race condition possible
            let abort_handle = handle.abort_handle();
            state_tasks_for_close.lock().push(abort_handle);

            // Data channel closed unexpectedly — signal the guacd nop keepalive task to
            // start sending nops so guacd doesn't time out the TCP connection during the
            // ICE restart window. Guard: skip if teardown is already in progress.
            if active_protocol_for_close == ActiveProtocol::Guacd
                && !should_exit_for_close.load(std::sync::atomic::Ordering::Acquire)
            {
                ice_restart_active_for_close.store(true, std::sync::atomic::Ordering::Release);
            }

            Box::pin(async {})
        }));

        let state_tx_error = state_tx.clone();
        let channel_id_for_error = channel_id_base.clone(); // Clone for on_error
        let conversation_id_for_error = conversation_id_base.clone();
        let state_tasks_for_error = self.state_monitoring_tasks.clone();

        data_channel.on_error(Box::new(move |err| {
            let tx = state_tx_error.clone();
            let err_str = format!("Error: {err}");
            let channel_id_log = channel_id_for_error.clone(); // Clone for async block
            let conversation_id_log = conversation_id_for_error.clone();

            // Proper resource handling: Store AbortHandle for explicit lifecycle management
            let handle = tokio::spawn(async move {
                if let Err(e) = tx.send(err_str).await {
                    warn!(
                        "Failed to send error state notification (channel_id: {}, conversation_id: {}, error: {})",
                        channel_id_log, conversation_id_log, e
                    );
                }
            });

            // Store abort handle synchronously - no race condition possible
            let abort_handle = handle.abort_handle();
            state_tasks_for_error.lock().push(abort_handle);

            Box::pin(async {})
        }));

        let runtime = get_runtime();
        let channel_id_for_runtime_spawn = channel_id_base.clone(); // Clone for runtime spawn
        let conversation_id_for_runtime_spawn = conversation_id_base.clone();
        runtime.spawn(async move {
            let mut last_state_in_task = last_state;
            let channel_id_log = channel_id_for_runtime_spawn.clone(); // Clone for use in loop
            let conversation_id_log = conversation_id_for_runtime_spawn.clone();
            while let Some(current_state) = state_rx.recv().await {
                if current_state != last_state_in_task {
                    debug!("Endpoint WebRTC state changed: {} -> {} (channel_id: {}, conversation_id: {})", last_state_in_task, current_state, channel_id_log, conversation_id_log);
                    last_state_in_task = current_state.clone();
                }

                let lower_current_state = current_state.to_lowercase();
                if lower_current_state == "closed" || lower_current_state.starts_with("error") {
                    debug!("Endpoint WebRTC state, stopping state monitoring task. (channel_id: {}, conversation_id: {}, state: {})", channel_id_log, conversation_id_log, current_state);
                    break;
                }
            }
        });
        debug!(
            "Channel WebRTC state change monitoring set up. (channel_id: {}, conversation_id: {})",
            channel_id_base, conversation_id_base
        );
    }

    /// Process a control message received from the data channel
    // **BOLD WARNING: HOT PATH - CALLED FOR EVERY CONTROL MESSAGE**
    // **NO STRING ALLOCATIONS IN DEBUG LOGS UNLESS ENABLED**
    pub(crate) async fn process_control_message(
        &mut self,
        message_type: ControlMessage,
        data: &[u8],
    ) -> Result<()> {
        if log::log_enabled!(log::Level::Debug) {
            let active_connections = self.conns.len();
            let connection_list = self.get_connection_ids();

            debug!("Processing control message - Channel stats (channel_id: {}, conversation_id: {}, message_type: {:?}, active_connections: {}, connection_list: {:?})",
                   self.channel_id, self.conversation_id, message_type, active_connections, connection_list);
        }

        match message_type {
            ControlMessage::CloseConnection => {
                self.handle_close_connection(data).await?;
            }
            ControlMessage::OpenConnection => {
                self.handle_open_connection(data).await?;
            }
            ControlMessage::Ping => {
                self.handle_ping(data).await?;
            }
            ControlMessage::Pong => {
                self.handle_pong(data).await?;
            }
            ControlMessage::SendEOF => {
                self.handle_send_eof(data).await?;
            }
            ControlMessage::ConnectionOpened => {
                // In server mode, this completes protocol handshakes like SOCKS5
                // In client mode, we just log and continue
                self.handle_connection_opened(data).await?;
            }
            ControlMessage::MetricsRequest => {
                self.handle_metrics_request(data).await?;
            }
            ControlMessage::MetricsResponse => {
                self.handle_metrics_response(data).await?;
            }
            ControlMessage::MetricsConfig => {
                self.handle_metrics_config(data).await?;
            }
        }

        Ok(())
    }

    /// Handle a CloseConnection control message.
    /// Wire format: [conn_no: 4 bytes][reason: 1 byte][optional msg_len: 2][optional msg].
    /// When the remote (e.g. gateway) closes due to guacd disconnect, the channel may be
    /// torn down before the full payload is received. We treat short payloads as graceful
    /// close (conn_no=0, Normal) to avoid GuacdError and MPSC cascade on the receiver.
    async fn handle_close_connection(&mut self, data: &[u8]) -> Result<()> {
        let (target_connection_no, reason) = if data.len() < CONN_NO_LEN {
            // Short payload: remote likely closed before sending full 4-byte conn_no + 1-byte reason.
            // Treat as control connection closed normally to avoid error propagation and MPSC failure.
            warn!(
                "Channel({}): CloseConnection payload shorter than {} bytes (got {}), treating as conn_no=0, reason=Normal (conversation_id: {})",
                self.channel_id, CONN_NO_LEN, data.len(), self.conversation_id
            );
            (0u32, CloseConnectionReason::Normal)
        } else {
            let target_connection_no = u32::from_be_bytes([data[0], data[1], data[2], data[3]]);
            let reason = if data.len() > CONN_NO_LEN {
                let reason_code = data[CONN_NO_LEN] as u16;
                CloseConnectionReason::from_code(reason_code)
            } else {
                CloseConnectionReason::Normal
            };
            (target_connection_no, reason)
        };

        // Extract optional error message (backward compatible extension)
        // Format after reason byte: [msg_len: 2 bytes][msg: N bytes]
        let error_message = if data.len() > CONN_NO_LEN + 1 + 2 {
            // 4 (conn_no) + 1 (reason) + 2 (len) = 7 minimum for message
            let msg_len = u16::from_be_bytes([data[5], data[6]]) as usize;
            if data.len() >= 7 + msg_len {
                Some(String::from_utf8_lossy(&data[7..7 + msg_len]).to_string())
            } else {
                None
            }
        } else {
            None
        };

        // Log closure: error level only for critical reasons, debug otherwise
        if let Some(ref msg) = error_message {
            if reason.is_critical() {
                error!(
                    "Connection {} closed with error: {} (reason: {:?}, channel_id: {}, conversation_id: {})",
                    target_connection_no, msg, reason, self.channel_id, self.conversation_id
                );
            } else if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Connection {} closed: {} (reason: {:?}, channel_id: {}, conversation_id: {})",
                    target_connection_no, msg, reason, self.channel_id, self.conversation_id
                );
            }
        } else if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Endpoint Closing connection {} (reason: {:?}) (channel_id: {}, conversation_id: {})",
                target_connection_no, reason, self.channel_id, self.conversation_id
            );
        }

        // CRITICAL: Send guacd disconnect FIRST when frontend closes from UI.
        // Do this before any other processing so guacd closes recording FIFOs and Python
        // readers see EOF. Prevents session cleanup from hanging on 300s drain timeout.
        if self.active_protocol == super::types::ActiveProtocol::Guacd {
            self.send_guacd_disconnect_immediate().await;
        }

        // Handle PythonHandler mode - notify Python and clean up virtual connection
        if self.active_protocol == super::types::ActiveProtocol::PythonHandler {
            // Notify Python handler of connection closure
            if let Some(ref tx) = self.python_handler_tx {
                let msg = super::core::PythonHandlerMessage::ConnectionClosed {
                    conn_no: target_connection_no,
                    reason,
                };
                if tx.send(msg).await.is_err() {
                    warn!(
                        "Channel({}): Failed to send ConnectionClosed to Python handler for conn_no {} (conversation_id: {})",
                        self.channel_id, target_connection_no, self.conversation_id
                    );
                }
            }

            // Clean up the virtual connection from our state
            if let super::core::ProtocolLogicState::PythonHandler(ref mut state) =
                self.protocol_state
            {
                if state.active_connections.remove(&target_connection_no) {
                    debug!(
                        "Channel({}): PythonHandler removed virtual connection {} (remaining: {}, conversation_id: {})",
                        self.channel_id,
                        target_connection_no,
                        state.active_connections.len(),
                        self.conversation_id
                    );
                } else {
                    debug!(
                        "Channel({}): PythonHandler conn_no {} was not in active_connections (may have been unconfirmed) (conversation_id: {})",
                        self.channel_id, target_connection_no, self.conversation_id
                    );
                }
            }

            // For PythonHandler, connection 0 still means channel close
            if target_connection_no == 0 {
                self.control_connection_closed
                    .store(true, std::sync::atomic::Ordering::Release);
                self.should_exit
                    .store(true, std::sync::atomic::Ordering::Release);
                if let Ok(mut guard) = self.channel_close_reason.try_lock() {
                    *guard = Some(reason);
                }
            }
            // No TCP backend to close for PythonHandler virtual connections
            return Ok(());
        }

        // Special case for connection 0 (control connection)
        if target_connection_no == 0 {
            self.control_connection_closed
                .store(true, std::sync::atomic::Ordering::Release);
            self.should_exit
                .store(true, std::sync::atomic::Ordering::Release);
            // Store the close reason for the channel - use try_lock to avoid blocking
            // Don't overwrite a critical error reason with Normal.
            // GuacdError without an error message means guacd disconnected cleanly (e.g. logout);
            // downgrade to Normal so it is not treated as a critical failure upstream.
            let effective_reason =
                if reason == CloseConnectionReason::GuacdError && error_message.is_none() {
                    CloseConnectionReason::Normal
                } else {
                    reason
                };
            if let Ok(mut guard) = self.channel_close_reason.try_lock() {
                let should_store = match &*guard {
                    None => true,
                    Some(existing) => !existing.is_critical() || effective_reason.is_critical(),
                };
                if should_store {
                    *guard = Some(effective_reason);
                }
            }
            // CRITICAL: When frontend closes from UI, it sends CloseConnection(conn 0).
            // We must send guacd disconnect so guacd closes recording FIFOs and Python
            // readers see EOF. Without this, guacd stays open and session cleanup hangs.
            if self.active_protocol == super::types::ActiveProtocol::Guacd {
                self.close_tunnel_channel(0, reason).await;
            }
            // Even if we can't store the reason, we still need to exit
            return Ok(());
        }

        // Close the connection WITHOUT sending another CloseConnection message
        // This prevents feedback loops where both sides keep sending CloseConnection messages
        self.internal_close_backend_no_message(target_connection_no, reason)
            .await?;

        Ok(())
    }

    /// Handle an OpenConnection control message
    async fn handle_open_connection(&mut self, data: &[u8]) -> Result<()> {
        if data.len() < CONN_NO_LEN {
            return Err(anyhow!(
                "OpenConnection message too short, expected at least {} bytes for conn_no",
                CONN_NO_LEN
            ));
        }

        let mut cursor = std::io::Cursor::new(data);
        let target_connection_no = cursor.get_u32(); // Consumes first 4 bytes

        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!("Endpoint Received OpenConnection request (channel_id: {}, conversation_id: {}, conn_no: {}, payload_len: {}, server_mode: {}, active_protocol: {:?})", self.channel_id, self.conversation_id, target_connection_no, cursor.remaining(), self.server_mode, self.active_protocol);
        }

        // Initialize effective host/port with channel defaults
        let mut effective_guacd_host = self.guacd_host.clone();
        let mut effective_guacd_port = self.guacd_port;

        // --- ConnectAs Logic (integrated from connections.rs) ---
        if self.active_protocol == super::types::ActiveProtocol::Guacd
            && (self.connect_as_settings.allow_supply_user
                || self.connect_as_settings.allow_supply_host)
        {
            if let Some(gateway_private_key_pem) =
                self.connect_as_settings.gateway_private_key.as_ref()
            {
                debug!(
                    "Channel({}): Attempting ConnectAs for Guacd target_conn_no {} (conversation_id: {})",
                    self.channel_id, target_connection_no, self.conversation_id
                );

                if cursor.remaining() >= CONNECT_AS_DETAILS_LEN_FIELD_BYTES {
                    let connect_as_payload_len = cursor.get_u32() as usize; // Consumes 4 bytes
                    let required_crypto_block_len = CONNECT_AS_PUBLIC_KEY_BYTES
                        + CONNECT_AS_NONCE_BYTES
                        + connect_as_payload_len;

                    if cursor.remaining() >= required_crypto_block_len {
                        let mut crypto_buffer = self.buffer_pool.acquire();
                        crypto_buffer.clear();
                        crypto_buffer.resize(required_crypto_block_len, 0);

                        cursor.copy_to_slice(&mut crypto_buffer[..]); // Consumes required_crypto_block_len bytes

                        let client_public_key_bytes = &crypto_buffer[..CONNECT_AS_PUBLIC_KEY_BYTES];
                        let nonce_bytes = &crypto_buffer[CONNECT_AS_PUBLIC_KEY_BYTES
                            ..CONNECT_AS_PUBLIC_KEY_BYTES + CONNECT_AS_NONCE_BYTES];
                        let encrypted_data_bytes =
                            &crypto_buffer[CONNECT_AS_PUBLIC_KEY_BYTES + CONNECT_AS_NONCE_BYTES..];

                        // 1. Parse PKCS#8 PEM to P256SecretKey
                        let p256_secret_key = P256SecretKey::from_pkcs8_pem(
                            gateway_private_key_pem,
                        )
                        .map_err(|e| {
                            error!(
                                "Channel({}): Failed to parse gateway private key PKCS#8 PEM: {} (conversation_id: {})",
                                self.channel_id, e, self.conversation_id
                            );
                            anyhow!("Failed to parse gateway private key PKCS#8 PEM: {}", e)
                        })?;

                        // 2. Get the raw scalar bytes of the P256SecretKey
                        let secret_key_scalar_bytes = p256_secret_key.to_bytes(); // This returns FieldBytes<NistP256>

                        // 3. Convert raw scalar bytes to hex string
                        // FieldBytes<C> (which is GenericArray<u8, C::FieldSize>) implements AsRef<[u8]>,
                        // so it can be passed directly to hex::encode.
                        let gateway_private_key_hex = hex::encode(secret_key_scalar_bytes);

                        match decrypt_connect_as_payload(
                            &gateway_private_key_hex, // Use the hex string of raw scalar bytes
                            client_public_key_bytes,
                            nonce_bytes,
                            encrypted_data_bytes,
                        ) {
                            Ok(decrypted_payload) => {
                                info!("Channel({}): Successfully decrypted ConnectAs payload for target_conn_no {} (conversation_id: {})", self.channel_id, target_connection_no, self.conversation_id);
                                let mut guacd_params_locked = self.guacd_params.lock().await;

                                // Apply user credentials if EITHER allow_supply_user OR allow_supply_host is true (matches Python logic)
                                if self.connect_as_settings.allow_supply_user
                                    || self.connect_as_settings.allow_supply_host
                                {
                                    if let Some(user_details) = decrypted_payload.user {
                                        debug!(
                                            "Channel({}): Applying ConnectAs user details (conversation_id: {})",
                                            self.channel_id, self.conversation_id
                                        );

                                        // Capture before moving into guacd_params so we can
                                        // patch the KeeperDB auto-login URL blob afterward.
                                        let ca_username = user_details.username.clone();
                                        let ca_password = user_details.password.clone();
                                        let ca_connect_database =
                                            user_details.connect_database.clone();

                                        if let Some(val) = user_details.username {
                                            guacd_params_locked.insert("username".to_string(), val);
                                        }
                                        if let Some(val) = user_details.password {
                                            guacd_params_locked.insert("password".to_string(), val);
                                        }
                                        if let Some(val) = user_details.private_key {
                                            guacd_params_locked
                                                .insert("privatekey".to_string(), val);
                                        }
                                        if let Some(val) = user_details.public_key {
                                            guacd_params_locked
                                                .insert("public-key".to_string(), val);
                                        }
                                        if let Some(val) = user_details.private_key_passphrase {
                                            guacd_params_locked
                                                .insert("passphrase".to_string(), val);
                                        }
                                        if let Some(val) = user_details.passphrase {
                                            guacd_params_locked
                                                .insert("passphrase".to_string(), val);
                                        }
                                        if let Some(val) = user_details.domain {
                                            guacd_params_locked.insert("domain".to_string(), val);
                                        }
                                        if let Some(val) = user_details.connect_database {
                                            guacd_params_locked
                                                .insert("connectdatabase".to_string(), val);
                                        }
                                        if let Some(val) = user_details.distinguished_name {
                                            guacd_params_locked
                                                .insert("distinguishedname".to_string(), val);
                                        }
                                        if let Some(totp_uri) = user_details.totp {
                                            if let Some((alg, dig, per, sec)) =
                                                parse_totp_uri(&totp_uri)
                                            {
                                                guacd_params_locked
                                                    .insert("totpalgorithm".to_string(), alg);
                                                guacd_params_locked
                                                    .insert("totpdigits".to_string(), dig);
                                                guacd_params_locked
                                                    .insert("totpperiod".to_string(), per);
                                                guacd_params_locked
                                                    .insert("totpsecret".to_string(), sec);
                                            }
                                        }

                                        // For KeeperDB RBI sessions, guacd navigates to an
                                        // auto-login URL whose `credentials=` query param is a
                                        // base64 JSON blob built before ConnectAs credentials
                                        // arrive. Patch it now so the embedded username/password/
                                        // database match the ConnectAs-supplied values.
                                        if ca_username.is_some()
                                            || ca_password.is_some()
                                            || ca_connect_database.is_some()
                                        {
                                            if let Some(existing_url) =
                                                guacd_params_locked.get("url").cloned()
                                            {
                                                use base64::{
                                                    engine::general_purpose::URL_SAFE_NO_PAD,
                                                    Engine as _,
                                                };
                                                let auth_key: Option<Vec<u8>> = guacd_params_locked
                                                    .get("keeperdb_url_auth_key")
                                                    .and_then(|k| URL_SAFE_NO_PAD.decode(k).ok());
                                                let patched = patch_keeperdb_url_credentials(
                                                    &existing_url,
                                                    ca_username.as_deref(),
                                                    ca_password.as_deref(),
                                                    ca_connect_database.as_deref(),
                                                    auth_key.as_deref(),
                                                );
                                                guacd_params_locked
                                                    .insert("url".to_string(), patched);
                                            }
                                        }
                                    }
                                }
                                if self.connect_as_settings.allow_supply_host {
                                    if let Some(host) = decrypted_payload.host {
                                        debug!(
                                            "Channel({}): ConnectAs supplied host: {} (conversation_id: {})",
                                            self.channel_id, host, self.conversation_id
                                        );
                                        effective_guacd_host = Some(host);
                                    }
                                    if let Some(port) = decrypted_payload.port {
                                        debug!(
                                            "Channel({}): ConnectAs supplied port: {} (conversation_id: {})",
                                            self.channel_id, port, self.conversation_id
                                        );
                                        effective_guacd_port = Some(port);
                                    }
                                }
                                // Guacd params are updated, effective_guacd_host/port is set.
                            }
                            Err(e) => {
                                error!("Channel({}): Failed to decrypt or parse ConnectAs payload for target_conn_no {}: {} (conversation_id: {})", self.channel_id, target_connection_no, e, self.conversation_id);
                                self.buffer_pool.release(crypto_buffer);
                                // Unlike original connections.rs, we might not want to immediately return Err here.
                                // Consider if connection should proceed with default Guacd params if ConnectAs fails.
                                // For now, maintaining strict behavior: if ConnectAs is attempted and fails, the connection attempt fails.
                                return Err(anyhow!("ConnectAs decryption/parsing failed: {}", e));
                            }
                        }
                        self.buffer_pool.release(crypto_buffer);
                    } else {
                        warn!("Channel({}): ConnectAs payload too short for PK, Nonce, and encrypted data (expected {}, got {}) for target_conn_no {} (conversation_id: {})",
                              self.channel_id, required_crypto_block_len, cursor.remaining(), target_connection_no, self.conversation_id);
                        return Err(anyhow!(
                            "ConnectAs payload too short for PK, Nonce, and encrypted data"
                        ));
                    }
                } else {
                    warn!("Channel({}): ConnectAs payload too short for connect_as_payload_len field (expected {} bytes, got {}) for target_conn_no {} (conversation_id: {})",
                          self.channel_id, CONNECT_AS_DETAILS_LEN_FIELD_BYTES, cursor.remaining(), target_connection_no, self.conversation_id);
                    // If ConnectAs was expected but the payload is too short even for its length, it's an error.
                    // If ConnectAs was optional and this path is reached, it implies no ConnectAs data was provided.
                    // The original connections.rs returned Err. Here, we might just log and proceed if ConnectAs is not mandatory.
                    // For now, assuming if ConnectAs is configured, its presence is expected if data follows conn_no.
                    // However, the cursor.remaining() might be 0 if only conn_no was sent.
                    // This needs careful consideration of whether ConnectAs data is mandatory or optional if settings allow it.
                    // The original logic in connections.rs would bail out. Let's stick to that for now if ConnectAs settings are enabled.
                    if cursor.remaining() > 0 {
                        // If there was some data beyond conn_no but not enough for ConnectAs header
                        return Err(anyhow!(
                            "ConnectAs payload present but too short for its own length field"
                        ));
                    }
                    // If cursor.remaining() is 0, it means no ConnectAs payload was sent, proceed without it.
                    debug!("Channel({}): No additional payload for ConnectAs provided after target_conn_no {} (conversation_id: {}).", self.channel_id, target_connection_no, self.conversation_id);
                }
            }
        }
        // --- End of ConnectAs Logic ---

        if unlikely!(crate::logger::is_verbose_logging()) {
            // Build a redacted copy of the params map for logging — strip keys that
            // carry credentials so that verbose logs never contain plaintext secrets.
            let redacted: std::collections::HashMap<String, String> = {
                let guacd_params_locked = self.guacd_params.lock().await;
                guacd_params_locked
                    .iter()
                    .map(|(k, v)| (k.clone(), super::core::redact_string_setting(k, v)))
                    .collect()
            };
            debug!("Channel state for OpenConnection (after potential ConnectAs) (channel_id: {}, conversation_id: {}, conn_no: {}, effective_guacd_host: {:?}, effective_guacd_port: {:?}, connect_as_settings: {:?}, guacd_params_map: {:?})",
                self.channel_id, self.conversation_id, target_connection_no, effective_guacd_host, effective_guacd_port, self.connect_as_settings, redacted
            );
        }

        if self.server_mode && self.active_protocol == super::types::ActiveProtocol::PortForward {
            debug!("Server-mode PortForward received OpenConnection for conn_no {}. Acknowledging with ConnectionOpened. (channel_id: {}, conversation_id: {})", target_connection_no, self.channel_id, self.conversation_id);
            self.send_control_message(
                ControlMessage::ConnectionOpened,
                &target_connection_no.to_be_bytes(),
            )
            .await?;
            return Ok(());
        }

        // Check if connection exists AND is in active state (prevents conn_no reuse race)
        // NOTE: SOCKS5 protocol is not currently used and is not a focus of this project.
        // The following check prevents a race condition where conn_no could be reused during
        // the 600ms-2.7s cleanup window, which is primarily an issue for SOCKS5 proxy workloads.
        //
        // Memory ordering: Uses Acquire to pair with Release stores in handle_connection_close()
        // and internal_handle_connection_close(). This ensures we see the CLOSING/CLOSED state
        // after it's been set, preventing conn_no reuse during cleanup.
        let conn_state = self
            .conns
            .get(&target_connection_no)
            .map(|conn_ref| conn_ref.state.load(std::sync::atomic::Ordering::Acquire));

        if let Some(state) = conn_state {
            match state {
                crate::models::CONN_STATE_ACTIVE => {
                    // Connection is genuinely active - duplicate request
                    debug!(
                        "Active connection {} already exists. Sending ConnectionOpened. (channel_id: {}, conversation_id: {})",
                        target_connection_no, self.channel_id, self.conversation_id
                    );
                    self.send_control_message(
                        ControlMessage::ConnectionOpened,
                        &target_connection_no.to_be_bytes(),
                    )
                    .await?;
                    return Ok(());
                }
                crate::models::CONN_STATE_CLOSING | crate::models::CONN_STATE_CLOSED => {
                    // Connection is in cleanup - reject reuse
                    let error_str = format!(
                        "Connection {} is closing (state: {}), cannot reuse conn_no during cleanup window",
                        target_connection_no, state
                    );
                    error!(
                        "Rejected conn_no reuse during cleanup (channel_id: {}, conversation_id: {}, conn_no: {}, state: {})",
                        self.channel_id, self.conversation_id, target_connection_no, state
                    );

                    // Send CloseConnection with ConnectionFailed reason
                    let mut buffer = self.buffer_pool.acquire();
                    buffer.clear();
                    buffer.put_u32(target_connection_no);
                    buffer.put_u8(CloseConnectionReason::ConnectionFailed as u8);
                    let error_bytes = error_str.as_bytes();
                    let error_len = error_bytes.len().min(1024) as u16;
                    buffer.put_u16(error_len);
                    buffer.extend_from_slice(&error_bytes[..error_len as usize]);

                    if let Err(e) = self
                        .send_control_message(ControlMessage::CloseConnection, &buffer)
                        .await
                    {
                        error!("Failed to send CloseConnection for reuse rejection: {} (channel_id: {}, conversation_id: {})", e, self.channel_id, self.conversation_id);
                    }
                    self.buffer_pool.release(buffer);
                    return Ok(());
                }
                _ => {
                    warn!(
                        "Unknown connection state: {} (channel_id: {}, conversation_id: {}, conn_no: {})",
                        state, self.channel_id, self.conversation_id, target_connection_no
                    );
                    // Treat as closing to be safe
                    return Ok(());
                }
            }
        }

        let open_result = match self.active_protocol {
            super::types::ActiveProtocol::Guacd => {
                // Check if we should use built-in handlers based on use_guacr parameter
                {
                    // Read use_guacr parameter from guacd_params
                    let guacd_params = self.guacd_params.lock().await;
                    let use_guacr = guacd_params
                        .get("use_guacr")
                        .and_then(|v| v.parse::<bool>().ok())
                        .unwrap_or(false);
                    drop(guacd_params); // Release lock

                    // Only use built-in handlers if use_guacr=true
                    if use_guacr {
                        if let (Some(registry), Some(conv_type)) =
                            (&self.handler_registry, &self.conversation_type)
                        {
                            // Use built-in protocol handlers instead of external guacd

                            // Spawn handler and return result - will fall through to send ConnectionOpened
                            return match super::handler_connections::invoke_builtin_handler(
                                self,
                                conv_type,
                                registry,
                                target_connection_no,
                                Arc::clone(&self.spawned_task_completion_tx),
                            )
                            .await
                            {
                                Ok(()) => {
                                    debug!("Handler spawned successfully, sending ConnectionOpened (channel: {}, conversation_id: {}, conn: {})",
                                    self.channel_id, self.conversation_id, target_connection_no);
                                    let mut payload = self.buffer_pool.acquire();
                                    payload.put_u32(target_connection_no);
                                    let result = self
                                        .send_control_message(
                                            ControlMessage::ConnectionOpened,
                                            &payload,
                                        )
                                        .await;
                                    self.buffer_pool.release(payload);
                                    result
                                }
                                Err(e) => {
                                    error!(
                                        "Handler failed to start (channel: {}, conversation_id: {}, conn: {}): {}",
                                        self.channel_id, self.conversation_id, target_connection_no, e
                                    );
                                    let mut payload = self.buffer_pool.acquire();
                                    payload.put_u32(target_connection_no);
                                    payload.put_u8(CloseConnectionReason::ConnectionFailed as u8);
                                    let result = self
                                        .send_control_message(
                                            ControlMessage::CloseConnection,
                                            &payload,
                                        )
                                        .await;
                                    self.buffer_pool.release(payload);
                                    result.and(Err(e))
                                }
                            };
                        }
                    }
                }

                // Original: Connect to external guacd server
                if let (Some(host), Some(port)) =
                    (effective_guacd_host.as_deref(), effective_guacd_port)
                {
                    match tokio::net::lookup_host(format!("{host}:{port}")).await {
                        Ok(mut addrs) => {
                            if let Some(socket_addr) = addrs.next() {
                                debug!("Channel({}): Guacd OpenConnection for target_conn_no {} to {}:{} (resolved to {}, conversation_id: {}).",
                                    self.channel_id, target_connection_no, host, port, socket_addr, self.conversation_id);
                                // Use super::connections to call open_backend
                                super::connections::open_backend(
                                    self,
                                    target_connection_no,
                                    socket_addr,
                                    super::types::ActiveProtocol::Guacd,
                                )
                                .await
                            } else {
                                Err(anyhow!(
                                    "Could not resolve Guacd host {}:{} to any SocketAddr",
                                    host,
                                    port
                                ))
                            }
                        }
                        Err(e) => Err(anyhow!(
                            "DNS lookup failed for Guacd host {}:{}: {}",
                            host,
                            port,
                            e
                        )),
                    }
                } else {
                    Err(anyhow!("Guacd host/port not configured or supplied via ConnectAs for OpenConnection"))
                }
            }
            super::types::ActiveProtocol::PortForward => {
                // This logic is mostly for client mode PortForward. Server mode is handled above.
                if let super::core::ProtocolLogicState::PortForward(pf_state) = &self.protocol_state
                {
                    if let (Some(host), Some(port)) =
                        (pf_state.target_host.as_deref(), pf_state.target_port)
                    {
                        match tokio::net::lookup_host(format!("{host}:{port}")).await {
                            Ok(mut addrs) => {
                                if let Some(socket_addr) = addrs.next() {
                                    debug!("Channel({}): PortForward OpenConnection for target_conn_no {} to {}:{} (resolved to {}, conversation_id: {}).",
                                        self.channel_id, target_connection_no, host, port, socket_addr, self.conversation_id);
                                    super::connections::open_backend(
                                        self,
                                        target_connection_no,
                                        socket_addr,
                                        super::types::ActiveProtocol::PortForward,
                                    )
                                    .await
                                } else {
                                    Err(anyhow!("Could not resolve PortForward host {}:{} to any SocketAddr", host, port))
                                }
                            }
                            Err(e) => Err(anyhow!(
                                "DNS lookup failed for PortForward host {}:{}: {}",
                                host,
                                port,
                                e
                            )),
                        }
                    } else {
                        Err(anyhow!(
                            "PortForward target host/port not configured in channel protocol state"
                        ))
                    }
                } else {
                    Err(anyhow!(
                        "Channel is in PortForward mode, but protocol state is not PortForward"
                    ))
                }
            }
            super::types::ActiveProtocol::Socks5 => {
                // SOCKS5 parsing via tunnel protocol trait
                if !self.server_mode && self.network_checker.is_some() {
                    if let Some(ref protocol) = self.tunnel_protocol {
                        let remaining = &data[std::mem::size_of::<u32>()..]; // Skip conn_no already consumed
                        let target = protocol.parse_open_connection(remaining)?;

                        if let Some(ref checker) = self.network_checker {
                            match checker.resolve_if_allowed(&target.host).await {
                                Some(resolved_ips) => {
                                    if !checker.is_port_allowed(target.port) {
                                        error!(
                                            "SOCKS5 port {} not allowed (channel_id: {}, conversation_id: {})",
                                            target.port, self.channel_id, self.conversation_id
                                        );
                                        return Err(anyhow!(
                                            "SOCKS5 port {} not allowed",
                                            target.port
                                        ));
                                    }

                                    debug!(
                                        "SOCKS5 connection allowed to {}:{} (channel_id: {}, conversation_id: {})",
                                        target.host, target.port, self.channel_id, self.conversation_id
                                    );

                                    if let Some(&first_ip) = resolved_ips.first() {
                                        let socket_addr =
                                            std::net::SocketAddr::new(first_ip, target.port);
                                        super::connections::open_backend(
                                            self,
                                            target_connection_no,
                                            socket_addr,
                                            super::types::ActiveProtocol::Socks5,
                                        )
                                        .await
                                    } else {
                                        Err(anyhow!(
                                            "SOCKS5 host {} resolved to empty IP list",
                                            target.host
                                        ))
                                    }
                                }
                                None => {
                                    error!("SOCKS5 destination {} not allowed or unresolvable (channel_id: {}, conversation_id: {})", target.host, self.channel_id, self.conversation_id);
                                    Err(anyhow!(
                                        "SOCKS5 destination {} not allowed or unresolvable",
                                        target.host
                                    ))
                                }
                            }
                        } else {
                            Err(anyhow!("SOCKS5 network checker not configured"))
                        }
                    } else {
                        Err(anyhow!("SOCKS5 tunnel protocol not configured"))
                    }
                } else {
                    warn!("SOCKS5 OpenConnection received but not in client mode with network checker (channel_id: {}, conversation_id: {})", self.channel_id, self.conversation_id);
                    Err(anyhow!("SOCKS5 OpenConnection not supported in this mode"))
                }
            }
            super::types::ActiveProtocol::PythonHandler => {
                // PythonHandler mode: connections are virtual - notify Python and acknowledge
                debug!(
                    "Channel({}): PythonHandler OpenConnection for virtual conn_no {} (conversation_id: {})",
                    self.channel_id, target_connection_no, self.conversation_id
                );

                // Send ConnectionOpened event to Python handler
                if let Some(ref tx) = self.python_handler_tx {
                    if tx
                        .send(super::core::PythonHandlerMessage::ConnectionOpened {
                            conn_no: target_connection_no,
                        })
                        .await
                        .is_err()
                    {
                        warn!(
                            "Channel({}): Failed to send ConnectionOpened to Python handler (conversation_id: {})",
                            self.channel_id, self.conversation_id
                        );
                    }
                }

                // Return Ok - no TCP backend needed for PythonHandler
                Ok(())
            }
            super::types::ActiveProtocol::DatabaseProxy => {
                // Database proxy mode: route to proxy host/port instead of guacd
                if unlikely!(crate::logger::is_verbose_logging()) {
                    debug!(
                        "Channel({}): DatabaseProxy OpenConnection requested, proxy_host={:?}, proxy_port={:?} (conversation_id: {})",
                        self.channel_id, self.proxy_host, self.proxy_port, self.conversation_id
                    );
                }
                if let (Some(host), Some(port)) = (self.proxy_host.as_deref(), self.proxy_port) {
                    match tokio::net::lookup_host(format!("{host}:{port}")).await {
                        Ok(mut addrs) => {
                            if let Some(socket_addr) = addrs.next() {
                                if unlikely!(crate::logger::is_verbose_logging()) {
                                    debug!("Channel({}): DatabaseProxy OpenConnection for target_conn_no {} to {}:{} (resolved to {}, conversation_id: {}).",
                                        self.channel_id, target_connection_no, host, port, socket_addr, self.conversation_id);
                                }
                                super::connections::open_backend(
                                    self,
                                    target_connection_no,
                                    socket_addr,
                                    super::types::ActiveProtocol::DatabaseProxy,
                                )
                                .await
                            } else {
                                Err(anyhow!(
                                    "Could not resolve DatabaseProxy host {}:{} to any SocketAddr",
                                    host,
                                    port
                                ))
                            }
                        }
                        Err(e) => Err(anyhow!(
                            "DNS lookup failed for DatabaseProxy host {}:{}: {}",
                            host,
                            port,
                            e
                        )),
                    }
                } else {
                    Err(anyhow!(
                        "DatabaseProxy host/port not configured for OpenConnection"
                    ))
                }
            }
        };

        // --- Post OpenConnection Attempt ---
        let mut temp_payload_buffer = self.buffer_pool.acquire(); // Used for ConnectionOpened/CloseConnection
        temp_payload_buffer.clear();

        if let Err(e) = open_result {
            let error_str = e.to_string();
            error!("Channel({}): Failed to process OpenConnection for target_conn_no {}: {}. Sending CloseConnection back. (conversation_id: {})",
                self.channel_id, target_connection_no, error_str, self.conversation_id);
            temp_payload_buffer.put_u32(target_connection_no);
            temp_payload_buffer.put_u8(CloseConnectionReason::ConnectionFailed as u8);
            // Add error message (backward compatible extension)
            let error_bytes = error_str.as_bytes();
            let error_len = error_bytes.len().min(1024) as u16; // Cap at 1KB
            temp_payload_buffer.put_u16(error_len);
            temp_payload_buffer.extend_from_slice(&error_bytes[..error_len as usize]);
            // Use self.send_control_message for sending
            if let Err(send_err) = self
                .send_control_message(ControlMessage::CloseConnection, &temp_payload_buffer)
                .await
            {
                error!(
                    "Channel({}): Failed to send CloseConnection for failed OpenConnection {}: {} (conversation_id: {})",
                    self.channel_id, target_connection_no, send_err, self.conversation_id
                );
            }
        } else {
            debug!("Channel({}): Successfully processed OpenConnection for target_conn_no {}, sending ConnectionOpened. (conversation_id: {})", self.channel_id, target_connection_no, self.conversation_id);
            temp_payload_buffer.put_u32(target_connection_no);
            if let Err(e) = self
                .send_control_message(ControlMessage::ConnectionOpened, &temp_payload_buffer)
                .await
            {
                error!(
                    "Channel({}): Error sending ConnectionOpened for conn_no {}: {} (conversation_id: {})",
                    self.channel_id, target_connection_no, e, self.conversation_id
                );
            }
        }
        self.buffer_pool.release(temp_payload_buffer);
        Ok(())
    }

    /// Handle a Ping control message
    async fn handle_ping(&mut self, data: &[u8]) -> Result<()> {
        if data.len() < CONN_NO_LEN {
            // Basic ping without connection info
            if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Endpoint Received basic Ping request (channel_id: {}, conversation_id: {})",
                    self.channel_id, self.conversation_id
                );
            }
            self.send_control_message(
                ControlMessage::Pong,
                &[0, 0, 0, 0], // connection 0
            )
            .await?;
            return Ok(());
        }

        // Extract connection number
        let conn_no = u32::from_be_bytes([data[0], data[1], data[2], data[3]]);

        // Connection 0 is a special control connection that doesn't need to exist in the connection's map
        if conn_no != 0 {
            // Validate non-control connection exists with single lookup
            if self.conns.get(&conn_no).is_none() {
                error!(
                    "Endpoint Connection {} not found for Ping (channel_id: {}, conversation_id: {})",
                    conn_no, self.channel_id, self.conversation_id
                );
                return Ok(());
            }
        }

        // Build response - include connection number
        // **PERFORMANCE: Use buffer pool instead of Vec allocation**
        let mut response = self.buffer_pool.acquire();
        response.clear();
        response.extend_from_slice(&conn_no.to_be_bytes());

        // Handle timing information if present
        if data.len() > CONN_NO_LEN {
            response.extend_from_slice(&data[CONN_NO_LEN..]);
            if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Endpoint Received ACK request with timing data for {} (channel_id: {}, conversation_id: {})",
                    conn_no, self.channel_id, self.conversation_id
                );
            }
        } else if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Endpoint Received ACK request for {} (channel_id: {}, conversation_id: {})",
                conn_no, self.channel_id, self.conversation_id
            );
        }

        // Send response - using buffer pool data
        self.send_control_message(ControlMessage::Pong, &response)
            .await?;
        self.buffer_pool.release(response);

        Ok(())
    }

    /// Handle a Pong control message
    async fn handle_pong(&mut self, data: &[u8]) -> Result<()> {
        if data.len() < CONN_NO_LEN {
            if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Endpoint Received basic pong (channel_id: {}, conversation_id: {})",
                    self.channel_id, self.conversation_id
                );
            }
            return Ok(());
        }

        // Extract connection number
        let conn_no = u32::from_be_bytes([data[0], data[1], data[2], data[3]]);

        // Simplified pong handling - no complex stats tracking
        if let Some(_conn_ref) = self.conns.get(&conn_no) {
            if conn_no == 0 {
                if unlikely!(crate::logger::is_verbose_logging()) {
                    debug!(
                        "Endpoint Received pong (channel_id: {}, conversation_id: {})",
                        self.channel_id, self.conversation_id
                    );
                }
            } else if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Endpoint Received ACK response for {} (channel_id: {}, conversation_id: {})",
                    conn_no, self.channel_id, self.conversation_id
                );
            }
        } else if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Endpoint Received pong for unknown connection {} (channel_id: {}, conversation_id: {})",
                conn_no, self.channel_id, self.conversation_id
            );
        }

        Ok(())
    }

    /// Handle a SendEOF control message
    async fn handle_send_eof(&mut self, data: &[u8]) -> Result<()> {
        if data.len() < CONN_NO_LEN {
            return Err(anyhow!("SendEOF message too short"));
        }

        // Extract connection number
        let conn_no = u32::from_be_bytes([data[0], data[1], data[2], data[3]]);

        // Check if the connection exists and handle EOF
        if let Some(conn_ref) = self.conns.get(&conn_no) {
            if unlikely!(crate::logger::is_verbose_logging()) {
                debug!("Endpoint Received EOF from remote for connection {}, signaling backend to shutdown write side (channel_id: {}, conversation_id: {})", conn_no, self.channel_id, self.conversation_id);
            }

            // SendEOF means the remote side closed their writing end
            // Send EOF signal to the backend task which will call backend.shutdown() (perfect for RDP!)
            match conn_ref.data_tx.send(crate::models::ConnectionMessage::Eof) {
                Ok(_) => {
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!("Endpoint Successfully sent EOF signal to backend for conn {} (channel_id: {}, conversation_id: {})", conn_no, self.channel_id, self.conversation_id);
                    }
                }
                Err(_) => {
                    // Channel is closed, connection is already dead
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!("Endpoint EOF signal failed, connection {} already closed (channel_id: {}, conversation_id: {})", conn_no, self.channel_id, self.conversation_id);
                    }
                }
            }
        } else {
            error!(
                "Endpoint Connection for EOF {} not found (channel_id: {}, conversation_id: {})",
                conn_no, self.channel_id, self.conversation_id
            );
        }

        Ok(())
    }

    /// Handle a ConnectionOpened control message
    async fn handle_connection_opened(&mut self, data: &[u8]) -> Result<()> {
        // This is called when we receive a ConnectionOpened control message from WebRTC
        // In server_mode, this completes the connection setup
        // In PythonHandler mode, this is the lazy initialization point for virtual connections

        if data.len() < CONN_NO_LEN {
            return Err(anyhow!("ConnectionOpened message too short"));
        }

        let connection_no = u32::from_be_bytes([data[0], data[1], data[2], data[3]]);

        // Handle PythonHandler mode specially - lazy initialization of virtual connections
        if self.active_protocol == super::types::ActiveProtocol::PythonHandler {
            debug!(
                "Channel({}): PythonHandler received ConnectionOpened for conn_no {} (conversation_id: {})",
                self.channel_id, connection_no, self.conversation_id
            );

            // Register the virtual connection in our state
            if let super::core::ProtocolLogicState::PythonHandler(ref mut state) =
                self.protocol_state
            {
                if state.active_connections.contains(&connection_no) {
                    warn!(
                        "Channel({}): PythonHandler conn_no {} already registered, ignoring duplicate ConnectionOpened (conversation_id: {})",
                        self.channel_id, connection_no, self.conversation_id
                    );
                    return Ok(());
                }
                state.active_connections.insert(connection_no);
                debug!(
                    "Channel({}): PythonHandler registered virtual connection {} (total active: {}, conversation_id: {})",
                    self.channel_id, connection_no, state.active_connections.len(), self.conversation_id
                );
            }

            // Notify Python handler that the connection is now open and ready for data
            if let Some(ref tx) = self.python_handler_tx {
                if tx
                    .send(super::core::PythonHandlerMessage::ConnectionOpened {
                        conn_no: connection_no,
                    })
                    .await
                    .is_err()
                {
                    warn!(
                        "Channel({}): Failed to send ConnectionOpened to Python handler for conn_no {} (conversation_id: {})",
                        self.channel_id, connection_no, self.conversation_id
                    );
                    // Clean up the registration since Python won't know about it
                    if let super::core::ProtocolLogicState::PythonHandler(ref mut state) =
                        self.protocol_state
                    {
                        state.active_connections.remove(&connection_no);
                    }
                    return Err(anyhow!("Python handler channel closed"));
                }
            } else {
                error!(
                    "Channel({}): PythonHandler mode but python_handler_tx is None (conversation_id: {})",
                    self.channel_id, self.conversation_id
                );
                return Err(anyhow!("PythonHandler mode missing python_handler_tx"));
            }

            return Ok(());
        }

        // Non-PythonHandler modes: require server_mode and pre-existing connection
        if !self.server_mode {
            if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Endpoint Received ConnectionOpened in client mode (ignoring) (channel_id: {}, conversation_id: {})",
                    self.channel_id, self.conversation_id
                );
            }
            return Ok(());
        }

        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Endpoint Starting reader for connection {} (channel_id: {}, conversation_id: {})",
                connection_no, self.channel_id, self.conversation_id
            );
        }

        // Get the connection
        if let Some(conn_ref) = self.conns.get(&connection_no) {
            // If the tunnel protocol has a deferred response, send it now
            if let Some(ref protocol) = self.tunnel_protocol {
                if let Some(response_bytes) = protocol.deferred_response() {
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!(
                            "{} Connection opened, sending deferred response (channel_id: {}, conversation_id: {}, conn_no: {})",
                            protocol.name(), self.channel_id, self.conversation_id, connection_no
                        );
                    }

                    match conn_ref
                        .data_tx
                        .send(crate::models::ConnectionMessage::Data(response_bytes))
                    {
                        Ok(_) => {
                            if unlikely!(crate::logger::is_verbose_logging()) {
                                debug!(
                                    "Endpoint {} deferred response queued for connection {} (channel_id: {}, conversation_id: {})",
                                    protocol.name(), connection_no, self.channel_id, self.conversation_id
                                );
                            }
                        }
                        Err(e) => {
                            error!(
                                "Endpoint Failed to queue {} deferred response: {} (channel_id: {}, conversation_id: {})",
                                protocol.name(), e, self.channel_id, self.conversation_id
                            );
                        }
                    }
                }
            }

            // The conn.to_webrtc and backend tasks are already set up by the connection creation
            // to handle reading from the backend and sending to WebRTC. No need to spawn more tasks here.
            let task_finished = conn_ref
                .to_webrtc
                .as_ref()
                .map(|t| t.is_finished())
                .unwrap_or(true);
            if task_finished {
                warn!("In ConnectionOpened, to_webrtc task was already finished. This is unexpected. (channel_id: {}, conversation_id: {}, conn_no: {})", self.channel_id, self.conversation_id, connection_no);
            }

            debug!(
                "Connection fully opened and ready. (channel_id: {}, conversation_id: {}, conn_no: {})",
                self.channel_id, self.conversation_id, connection_no
            );
        } else {
            error!(
                "Endpoint Connection {} not found for ConnectionOpened (channel_id: {}, conversation_id: {})",
                connection_no, self.channel_id, self.conversation_id
            );
            return Ok(());
        }

        Ok(())
    }

    /// Build the vault-compatible GatewayMetrics JSON payload from this connection's live stats.
    /// The schema matches the TypeScript GatewayMetrics type in useStatsHistory.ts.
    fn build_vault_metrics_response(&self) -> Vec<u8> {
        let uptime_secs = crate::metrics::METRICS_COLLECTOR.get_uptime().as_secs();
        let active_count = crate::metrics::METRICS_COLLECTOR.active_connection_count();

        let json = if let Some(m) =
            crate::metrics::METRICS_COLLECTOR.get_live_stats(&self.conversation_id)
        {
            let sctp = &m.webrtc_metrics.sctp_stats;
            let legs = &m.webrtc_metrics.connection_legs;
            let quality_str = match m.connection_quality {
                crate::metrics::ConnectionQuality::Excellent => "Excellent",
                crate::metrics::ConnectionQuality::Good => "Good",
                crate::metrics::ConnectionQuality::Fair => "Fair",
                crate::metrics::ConnectionQuality::Poor => "Poor",
            };
            serde_json::json!({
                "schema_version": 1,
                "transport_type": "WebRTC",
                "gateway_version": env!("CARGO_PKG_VERSION"),
                "gateway_uptime_seconds": uptime_secs,
                "active_connections_on_tube": active_count,
                "bytes": {
                    "sent_total": m.total_bytes_sent,
                    "received_total": m.total_bytes_received,
                    "messages_sent_total": m.messages_sent,
                    "messages_received_total": m.messages_received,
                },
                "sctp_live": {
                    "buffered_amount": sctp.message_queue_depth,
                    "buffer_utilization": sctp.buffer_utilization,
                    "cwnd": sctp.cwnd,
                    "rwnd": sctp.rwnd,
                    "fast_retransmits": sctp.fast_retransmits,
                    "timeout_retransmits": sctp.timeout_retransmits,
                    "supported": {
                        "cwnd": sctp.cwnd > 0,
                        "rwnd": sctp.rwnd > 0,
                        "fast_retransmits": true,
                    },
                },
                "connection_legs": {
                    "client_to_krelay_latency_ms": legs.client_to_krelay_latency_ms,
                    "krelay_to_gateway_latency_ms": legs.krelay_to_gateway_latency_ms,
                    "end_to_end_latency_ms": legs.end_to_end_latency_ms,
                    "stun_response_time_ms": legs.stun_response_time_ms,
                    "turn_allocation_latency_ms": legs.turn_allocation_latency_ms,
                },
                "quality": {
                    "connection_quality": quality_str,
                    "active_alert_count": m.active_alert_count,
                    "active_alerts": [],
                },
                "errors": {
                    "error_rate": m.error_rate,
                    "total_errors": m.total_errors,
                    "retry_count": m.retry_count,
                },
            })
        } else {
            // Connection not yet tracked — return a minimal envelope so vault knows we're alive.
            serde_json::json!({
                "schema_version": 1,
                "transport_type": "WebRTC",
                "gateway_version": env!("CARGO_PKG_VERSION"),
                "gateway_uptime_seconds": uptime_secs,
                "active_connections_on_tube": active_count,
            })
        };

        serde_json::to_vec(&json).unwrap_or_default()
    }

    /// Handle a MetricsRequest control message
    async fn handle_metrics_request(&mut self, _data: &[u8]) -> Result<()> {
        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Processing metrics request (channel_id: {}, conversation_id: {})",
                self.channel_id, self.conversation_id
            );
        }

        // Build a vault-compatible GatewayMetrics response from live per-connection stats.
        let response_data = self.build_vault_metrics_response();

        // Send metrics response
        self.send_control_message(ControlMessage::MetricsResponse, &response_data)
            .await?;

        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Sent metrics response (channel_id: {}, conversation_id: {}, response_bytes: {})",
                self.channel_id,
                self.conversation_id,
                response_data.len()
            );
        }

        Ok(())
    }

    /// Handle a MetricsResponse control message
    async fn handle_metrics_response(&mut self, data: &[u8]) -> Result<()> {
        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Received metrics response (channel_id: {}, conversation_id: {}, response_bytes: {})",
                self.channel_id,
                self.conversation_id,
                data.len()
            );
        }

        // Parse and process metrics response
        if !data.is_empty() && unlikely!(crate::logger::is_verbose_logging()) {
            match serde_json::from_slice::<serde_json::Value>(data) {
                Ok(metrics) => {
                    debug!(
                        "Parsed metrics response (channel_id: {}, conversation_id: {}, metrics: {:?})",
                        self.channel_id, self.conversation_id, metrics
                    );
                }
                Err(e) => {
                    debug!(
                        "Failed to parse metrics response (channel_id: {}, conversation_id: {}, error: {})",
                        self.channel_id, self.conversation_id, e
                    );
                }
            }
        }

        Ok(())
    }

    /// Handle a MetricsConfig control message
    async fn handle_metrics_config(&mut self, data: &[u8]) -> Result<()> {
        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Processing metrics config (channel_id: {}, conversation_id: {}, config_bytes: {})",
                self.channel_id,
                self.conversation_id,
                data.len()
            );
        }

        // Parse metrics configuration
        if !data.is_empty() {
            match serde_json::from_slice::<serde_json::Value>(data) {
                Ok(config) => {
                    debug!(
                        "Received metrics configuration (channel_id: {}, conversation_id: {}, config: {:?})",
                        self.channel_id, self.conversation_id, config
                    );

                    // Process configuration settings
                    if let Some(enable_collection) = config.get("enable_collection") {
                        if let Some(enabled) = enable_collection.as_bool() {
                            debug!(
                                "Metrics collection setting (channel_id: {}, conversation_id: {}, enabled: {})",
                                self.channel_id, self.conversation_id, enabled
                            );
                        }
                    }

                    if let Some(collection_interval) = config.get("collection_interval_ms") {
                        if let Some(interval) = collection_interval.as_u64() {
                            debug!(
                                "Metrics collection interval (channel_id: {}, conversation_id: {}, interval_ms: {})",
                                self.channel_id, self.conversation_id, interval
                            );
                        }
                    }

                    // Could update metrics collection settings here
                    // For now, just acknowledge we received the config
                }
                Err(e) => {
                    debug!(
                        "Failed to parse metrics config (channel_id: {}, conversation_id: {}, error: {})",
                        self.channel_id, self.conversation_id, e
                    );
                }
            }
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::parse_totp_uri;

    #[test]
    fn parse_totp_uri_all_fields_returns_tuple() {
        let uri = "otpauth://totp/Example:user@host?algorithm=SHA1&digits=6&period=30&secret=JBSWY3DPEHPK3PXP";
        let result = parse_totp_uri(uri);
        assert!(result.is_some());
        let (alg, dig, per, sec) = result.unwrap();
        assert_eq!(alg, "SHA1");
        assert_eq!(dig, "6");
        assert_eq!(per, "30");
        assert_eq!(sec, "JBSWY3DPEHPK3PXP");
    }

    #[test]
    fn parse_totp_uri_missing_field_returns_none() {
        // missing 'period' — all four must be present or we insert nothing
        let uri = "otpauth://totp/Example?algorithm=SHA1&digits=6&secret=JBSWY3DPEHPK3PXP";
        assert!(parse_totp_uri(uri).is_none());
    }

    #[test]
    fn parse_totp_uri_no_query_string_returns_none() {
        let uri = "otpauth://totp/Example";
        assert!(parse_totp_uri(uri).is_none());
    }
}
