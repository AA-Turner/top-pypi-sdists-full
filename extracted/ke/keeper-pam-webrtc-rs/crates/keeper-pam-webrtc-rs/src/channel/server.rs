// Server functionality for the Channel implementation

use crate::tube_protocol::{ControlMessage, Frame};
use crate::unlikely;
use crate::webrtc_data_channel::{EventDrivenSender, WebRTCDataChannel, ACTOR_BYTE_BUDGET};
use anyhow::{anyhow, Result};
use bytes::BufMut;
use log::{debug, error, info, warn};
use socket2::{Domain, Protocol, Socket, Type};
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::io::AsyncReadExt;
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::oneshot;

use super::core::Channel;
use super::tunnel_protocol::TunnelProtocol;
use super::types::ActiveProtocol;

impl Channel {
    /// Start a server listening on the given address for the given protocol
    /// Returns the actual SocketAddr it bound to.
    pub async fn start_server(&mut self, addr_str: &str) -> Result<SocketAddr, anyhow::Error> {
        if !self.server_mode {
            return Err(anyhow!("Cannot start server in client mode"));
        }

        let parsed_addr = addr_str
            .parse::<SocketAddr>()
            .map_err(|e| anyhow!("Invalid server address '{}': {}", addr_str, e))?;

        // Create the TCP listener with SO_REUSEADDR for immediate reuse after shutdown
        let domain = if parsed_addr.is_ipv6() {
            Domain::IPV6
        } else {
            Domain::IPV4
        };

        let socket = Socket::new(domain, Type::STREAM, Some(Protocol::TCP))
            .map_err(|e| anyhow!("Failed to create socket: {}", e))?;

        socket
            .set_reuse_address(true)
            .map_err(|e| anyhow!("Failed to set SO_REUSEADDR: {}", e))?;

        // On Unix systems, also set SO_REUSEPORT for more immediate reuse
        #[cfg(unix)]
        socket
            .set_reuse_port(true)
            .map_err(|e| anyhow!("Failed to set SO_REUSEPORT: {}", e))?;

        socket
            .set_nonblocking(true)
            .map_err(|e| anyhow!("Failed to set socket as non-blocking: {}", e))?;

        socket
            .bind(&parsed_addr.into())
            .map_err(|e| anyhow!("Failed to bind to {}: {}", parsed_addr, e))?;

        socket
            .listen(128)
            .map_err(|e| anyhow!("Failed to listen on {}: {}", parsed_addr, e))?;

        let listener = TcpListener::from_std(socket.into())
            .map_err(|e| anyhow!("Failed to convert socket to TcpListener: {}", e))?;

        let actual_addr = listener
            .local_addr()
            .map_err(|e| anyhow!("Failed to get local address after bind: {}", e))?;

        debug!(
            "Channel({}): Server listening on {} (conversation_id: {})",
            self.channel_id, actual_addr, self.conversation_id
        );

        // Store the listener for cleanup
        let listener_arc = Arc::new(listener);
        self.local_client_server = Some(listener_arc.clone());
        self.actual_listen_addr = Some(actual_addr);

        // Get the connection sender - required for server mode
        let connection_tx = self
            .local_client_server_conn_tx
            .clone()
            .ok_or_else(|| anyhow!("Connection sender not initialized for server mode"))?;

        // Spawn a task to accept connections
        let (tx, _rx) = oneshot::channel();
        let channel_id = self.channel_id.clone();
        let conversation_id = self.conversation_id.clone();
        let webrtc = self.webrtc.clone();
        let active_protocol = self.active_protocol;
        let buffer_pool = self.buffer_pool.clone();
        let should_exit = self.should_exit.clone();
        let listener_clone = listener_arc;
        // Clone task tracking for proper resource management
        let server_connection_tasks = self.server_connection_tasks.clone();
        let tunnel_protocol = self.tunnel_protocol.clone();

        // Shared sender: create once, cloned for each accepted connection.
        if self.event_sender.is_none() {
            self.event_sender = Some(
                EventDrivenSender::new(Arc::new(self.webrtc.clone()), ACTOR_BYTE_BUDGET).await,
            );
        }
        let shared_event_sender = self.event_sender.as_ref().unwrap().clone();

        let server_task = tokio::spawn(async move {
            // Signal that we're ready to accept connections
            let _ = tx.send(());

            // Wait for the WebRTC data channel to be open before accepting TCP connections
            // This prevents race conditions where TCP clients connect before the data channel is ready
            debug!(
                "Channel({}): Waiting for data channel to be open before accepting connections (conversation_id: {})",
                channel_id, conversation_id
            );
            match webrtc
                .wait_for_channel_open(Some(std::time::Duration::from_secs(30)))
                .await
            {
                Ok(true) => {
                    debug!(
                        "Channel({}): Data channel is open, ready to accept TCP connections (conversation_id: {})",
                        channel_id, conversation_id
                    );
                }
                Ok(false) => {
                    warn!("Channel({}): Data channel did not open (closed or timed out), server task exiting (conversation_id: {})", channel_id, conversation_id);
                    return;
                }
                Err(e) => {
                    error!("Channel({}): Error waiting for data channel to open: {}, server task exiting (conversation_id: {})", channel_id, e, conversation_id);
                    return;
                }
            }

            let mut next_conn_no = 1;

            while !should_exit.load(std::sync::atomic::Ordering::Acquire) {
                // Accept a new connection
                match listener_clone.accept().await {
                    Ok((stream, peer_addr)) => {
                        debug!(
                            "Channel({}): New connection from {} (conversation_id: {})",
                            channel_id, peer_addr, conversation_id
                        );

                        // Check if peer_addr is localhost
                        let is_localhost = match peer_addr.ip() {
                            std::net::IpAddr::V4(ip) => ip.is_loopback(),
                            std::net::IpAddr::V6(ip) => ip.is_loopback(),
                        };

                        if !is_localhost {
                            // Delegate rejection to the tunnel protocol (if present)
                            if let Some(ref protocol) = tunnel_protocol {
                                if let Err(e) = protocol.reject_non_localhost(stream).await {
                                    error!(
                                        "Channel({}): Error sending rejection: {} (conversation_id: {})",
                                        channel_id, e, conversation_id
                                    );
                                }
                            } else {
                                drop(stream);
                            }

                            error!(
                                "Channel({}): Connection from non-localhost address rejected (conversation_id: {})",
                                channel_id, conversation_id
                            );
                            continue;
                        }

                        // Dispatch based on protocol
                        if let Some(ref protocol) = tunnel_protocol {
                            // SOCKS5 and PortForward: use trait-based dispatch
                            let conn_tx_clone = connection_tx.clone();
                            let webrtc_clone = webrtc.clone();
                            let buffer_pool_clone = buffer_pool.clone();
                            let task_channel_id = channel_id.clone();
                            let task_conversation_id = conversation_id.clone();
                            let error_log_channel_id = channel_id.clone();
                            let error_log_conversation_id = conversation_id.clone();
                            let protocol_clone = protocol.clone();
                            let protocol_name = protocol.name().to_string();
                            let current_conn_no = next_conn_no;
                            next_conn_no += 1;

                            let event_sender_clone = shared_event_sender.clone();
                            let handle = tokio::spawn(async move {
                                if let Err(e) = handle_tunnel_server_connection(
                                    stream,
                                    current_conn_no,
                                    protocol_clone,
                                    conn_tx_clone,
                                    webrtc_clone,
                                    buffer_pool_clone,
                                    task_channel_id,
                                    task_conversation_id,
                                    event_sender_clone,
                                )
                                .await
                                {
                                    error!(
                                        "Channel({}): {} connection error: {} (conversation_id: {})",
                                        error_log_channel_id, protocol_name, e, error_log_conversation_id
                                    );
                                }
                            });

                            let abort_handle = handle.abort_handle();
                            server_connection_tasks.lock().push(abort_handle);
                        } else {
                            match active_protocol {
                                ActiveProtocol::Guacd | ActiveProtocol::DatabaseProxy => {
                                    let conn_tx_clone = connection_tx.clone();
                                    let webrtc_clone = webrtc.clone();
                                    let buffer_pool_clone = buffer_pool.clone();
                                    let task_channel_id = channel_id.clone();
                                    let task_conversation_id = conversation_id.clone();
                                    let error_log_channel_id = channel_id.clone();
                                    let error_log_conversation_id = conversation_id.clone();
                                    let current_conn_no = next_conn_no;
                                    next_conn_no += 1;

                                    let event_sender_clone = shared_event_sender.clone();
                                    let handle = tokio::spawn(async move {
                                        if let Err(e) = handle_generic_server_connection(
                                            stream,
                                            current_conn_no,
                                            active_protocol,
                                            conn_tx_clone,
                                            webrtc_clone,
                                            buffer_pool_clone,
                                            task_channel_id,
                                            task_conversation_id,
                                            event_sender_clone,
                                        )
                                        .await
                                        {
                                            error!("Channel({}): Generic server connection error for {:?}: {} (conversation_id: {})", error_log_channel_id, active_protocol, e, error_log_conversation_id);
                                        }
                                    });

                                    let abort_handle = handle.abort_handle();
                                    server_connection_tasks.lock().push(abort_handle);
                                }
                                ActiveProtocol::PythonHandler => {
                                    warn!("Channel({}): PythonHandler protocol does not support server mode (conversation_id: {})", channel_id, conversation_id);
                                }
                                _ => {
                                    warn!(
                                        "Channel({}): No tunnel protocol configured for {:?} (conversation_id: {})",
                                        channel_id, active_protocol, conversation_id
                                    );
                                }
                            }
                        }
                    }
                    Err(e) => {
                        error!(
                            "Channel({}): Error accepting connection: {} (conversation_id: {})",
                            channel_id, e, conversation_id
                        );
                    }
                }
            }

            debug!(
                "Channel({}): Server task exiting (conversation_id: {})",
                channel_id, conversation_id
            );
        });

        self.local_client_server_task = Some(server_task);

        Ok(actual_addr)
    }

    // Stop the server
    pub async fn stop_server(&mut self) -> Result<()> {
        if let Some(task) = self.local_client_server_task.take() {
            task.abort();

            // Give it some time to clean up
            match tokio::time::timeout(std::time::Duration::from_secs(5), task).await {
                Ok(_) => {
                    debug!(
                        "Endpoint {}: Server task shutdown cleanly (conversation_id: {})",
                        self.channel_id, self.conversation_id
                    );
                }
                Err(_) => {
                    warn!(
                        "Endpoint {}: Server task did not shutdown in time (conversation_id: {})",
                        self.channel_id, self.conversation_id
                    );
                }
            }
        }

        // Explicitly drop the listener reference to ensure immediate socket release
        if let Some(listener) = self.local_client_server.take() {
            drop(listener);
        }

        // Give the system a brief moment to fully release the socket
        tokio::time::sleep(std::time::Duration::from_millis(200)).await;

        info!(
            "Endpoint {}: Server stopped (conversation_id: {})",
            self.channel_id, self.conversation_id
        );
        Ok(())
    }
}

/// Handle a tunnel server connection using the TunnelProtocol trait.
/// Used for SOCKS5 and PortForward protocols.
/// Performs the protocol handshake, sends OpenConnection over WebRTC,
/// then spawns a read loop with EventDrivenSender for backpressure.
#[allow(clippy::too_many_arguments)]
async fn handle_tunnel_server_connection(
    stream: TcpStream,
    conn_no: u32,
    protocol: Arc<dyn TunnelProtocol>,
    conn_tx: tokio::sync::mpsc::Sender<(
        u32,
        tokio::net::tcp::OwnedWriteHalf,
        tokio::task::JoinHandle<()>,
    )>,
    webrtc: WebRTCDataChannel,
    buffer_pool: crate::buffer_pool::BufferPool,
    channel_id: String,
    conversation_id: String,
    event_sender: EventDrivenSender,
) -> Result<()> {
    debug!(
        "Channel({}): New {} connection {} (conversation_id: {})",
        channel_id,
        protocol.name(),
        conn_no,
        conversation_id
    );

    // 1. Perform protocol-specific handshake (SOCKS5 greeting/auth/request, or no-op for PortForward)
    let (mut reader, writer, handshake_result) = protocol
        .server_handshake(stream, conn_no, &buffer_pool)
        .await?;

    // 2. Send OpenConnection control message over WebRTC
    let open_frame = Frame::new_control_with_pool(
        ControlMessage::OpenConnection,
        &handshake_result.open_connection_payload,
        &buffer_pool,
    );
    // Release the buffer pool buffer used for the payload (if acquired from pool)
    buffer_pool.release(handshake_result.open_connection_payload);

    webrtc
        .send(open_frame.encode_with_pool(&buffer_pool))
        .await
        .map_err(|e| {
            anyhow!(
                "Failed to send OpenConnection for {} stream {}: {}",
                protocol.name(),
                conn_no,
                e
            )
        })?;

    debug!(
        "Channel({}): Sent OpenConnection for {} stream {} (conversation_id: {})",
        channel_id,
        protocol.name(),
        conn_no,
        conversation_id
    );

    // 3. Spawn read loop with EventDrivenSender for proper backpressure
    let buffer_pool_clone = buffer_pool.clone();
    let channel_id_clone = channel_id.clone();
    let conversation_id_clone = conversation_id.clone();
    let protocol_name = protocol.name().to_string();

    let read_task = tokio::spawn(async move {
        let mut read_buffer = buffer_pool_clone.acquire();
        let mut encode_buffer = buffer_pool_clone.acquire();

        const MAX_READ_SIZE: usize = 8 * 1024; // Match WebRTC RECEIVE_MTU

        // Use the shared per-tube sender passed in from start_server.
        let event_sender = event_sender;

        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Server-side TCP reader task started for conn_no: {} ({}) with EventDrivenSender (channel_id: {}, conversation_id: {})",
                conn_no, protocol_name, channel_id_clone, conversation_id_clone
            );
        }

        loop {
            read_buffer.clear();
            if read_buffer.capacity() < MAX_READ_SIZE {
                read_buffer.reserve(MAX_READ_SIZE - read_buffer.capacity());
            }

            let max_to_read = std::cmp::min(read_buffer.capacity(), MAX_READ_SIZE);

            let ptr = read_buffer.chunk_mut().as_mut_ptr();
            let current_chunk_len = read_buffer.chunk_mut().len();
            let slice_len = std::cmp::min(current_chunk_len, max_to_read);
            let read_slice = unsafe { std::slice::from_raw_parts_mut(ptr, slice_len) };

            match reader.read(read_slice).await {
                Ok(0) => {
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!(
                            "Channel({}): Client on server port (conn_no {}, {}) sent EOF. (conversation_id: {})",
                            channel_id_clone, conn_no, protocol_name, conversation_id_clone
                        );
                    }
                    let eof_payload = conn_no.to_be_bytes();
                    let eof_frame = Frame::new_control_with_pool(
                        ControlMessage::SendEOF,
                        &eof_payload,
                        &buffer_pool_clone,
                    );
                    if let Err(e) = event_sender
                        .send_with_natural_backpressure(
                            eof_frame.encode_with_pool(&buffer_pool_clone),
                        )
                        .await
                    {
                        error!(
                            "Channel({}): Failed to send EOF via EventDrivenSender for conn_no {}: {} (conversation_id: {})",
                            channel_id_clone, conn_no, e, conversation_id_clone
                        );
                    }
                    break;
                }
                Ok(n) if n > 0 => {
                    unsafe {
                        read_buffer.advance_mut(n);
                    }

                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!(
                            "Server-side TCP reader received {} bytes for conn_no: {} (channel_id: {}, conversation_id: {})",
                            n, conn_no, channel_id_clone, conversation_id_clone
                        );
                    }

                    let data_frame =
                        Frame::new_data_with_pool(conn_no, &read_buffer[0..n], &buffer_pool_clone);

                    encode_buffer.clear();
                    let bytes_written = data_frame.encode_into(&mut encode_buffer);
                    let encoded_frame_bytes = encode_buffer.split_to(bytes_written).freeze();

                    let send_start = std::time::Instant::now();
                    match event_sender
                        .send_with_natural_backpressure(encoded_frame_bytes.clone())
                        .await
                    {
                        Ok(_) => {
                            let send_latency = send_start.elapsed();
                            crate::metrics::METRICS_COLLECTOR.record_message_sent(
                                &channel_id_clone,
                                encoded_frame_bytes.len() as u64,
                                Some(send_latency),
                            );
                        }
                        Err(e) => {
                            crate::metrics::METRICS_COLLECTOR
                                .record_error(&channel_id_clone, "webrtc_send_failed");
                            if unlikely!(crate::logger::is_verbose_logging()) {
                                debug!("Failed to send data frame via EventDrivenSender for conn_no {}: {} (channel_id: {}, conversation_id: {})", conn_no, e, channel_id_clone, conversation_id_clone);
                            }
                            break;
                        }
                    }
                }
                Ok(_) => {}
                Err(e) => {
                    error!(
                        "Channel({}): Error reading from client on server port (conn_no {}): {} (conversation_id: {})",
                        channel_id_clone, conn_no, e, conversation_id_clone
                    );
                    break;
                }
            }
        }
        buffer_pool_clone.release(read_buffer);
        buffer_pool_clone.release(encode_buffer);
        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Channel({}): Server-side TCP reader task for conn_no {} ({}) exited. (conversation_id: {})",
                channel_id_clone, conn_no, protocol_name, conversation_id_clone
            );
        }
    });

    // 4. Send the writer half and reader task to the channel's main loop
    conn_tx
        .send((conn_no, writer, read_task))
        .await
        .map_err(|e| {
            anyhow!(
                "Failed to send new server connection {} to channel: {}",
                conn_no,
                e
            )
        })?;

    Ok(())
}

/// Handle a generic server-side accepted TCP connection (for Guacd, DatabaseProxy server mode)
#[allow(clippy::too_many_arguments)]
async fn handle_generic_server_connection(
    stream: TcpStream,
    conn_no: u32,
    active_protocol: ActiveProtocol,
    conn_tx: tokio::sync::mpsc::Sender<(
        u32,
        tokio::net::tcp::OwnedWriteHalf,
        tokio::task::JoinHandle<()>,
    )>,
    webrtc: WebRTCDataChannel,
    buffer_pool: crate::buffer_pool::BufferPool,
    channel_id: String,
    conversation_id: String,
    event_sender: EventDrivenSender,
) -> Result<()> {
    debug!(
        "Channel({}): New generic {:?} connection {} (conversation_id: {})",
        channel_id, active_protocol, conn_no, conversation_id
    );

    let open_conn_payload = conn_no.to_be_bytes();
    let open_frame = Frame::new_control_with_pool(
        ControlMessage::OpenConnection,
        &open_conn_payload,
        &buffer_pool,
    );
    webrtc
        .send(open_frame.encode_with_pool(&buffer_pool))
        .await
        .map_err(|e| {
            anyhow!(
                "Failed to send OpenConnection for new server stream {}: {}",
                conn_no,
                e
            )
        })?;

    debug!(
        "Channel({}): Sent OpenConnection for new server stream {} ({:?}) (conversation_id: {})",
        channel_id, conn_no, active_protocol, conversation_id
    );

    let (mut reader, writer) = stream.into_split();

    let buffer_pool_clone = buffer_pool.clone();
    let channel_id_clone = channel_id.clone();
    let conversation_id_clone = conversation_id.clone();

    let read_task = tokio::spawn(async move {
        let mut read_buffer = buffer_pool_clone.acquire();
        let mut encode_buffer = buffer_pool_clone.acquire();

        const MAX_READ_SIZE: usize = 8 * 1024; // Match WebRTC RECEIVE_MTU

        // Use the shared per-tube sender passed in from start_server.
        let event_sender = event_sender;

        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Server-side TCP reader task started for conn_no: {} with EventDrivenSender (channel_id: {}, conversation_id: {})",
                conn_no, channel_id_clone, conversation_id_clone
            );
        }

        loop {
            read_buffer.clear();
            if read_buffer.capacity() < MAX_READ_SIZE {
                read_buffer.reserve(MAX_READ_SIZE - read_buffer.capacity());
            }

            let max_to_read = std::cmp::min(read_buffer.capacity(), MAX_READ_SIZE);

            let ptr = read_buffer.chunk_mut().as_mut_ptr();
            let current_chunk_len = read_buffer.chunk_mut().len();
            let slice_len = std::cmp::min(current_chunk_len, max_to_read);
            let read_slice = unsafe { std::slice::from_raw_parts_mut(ptr, slice_len) };

            match reader.read(read_slice).await {
                Ok(0) => {
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!(
                            "Channel({}): Client on server port (conn_no {}) sent EOF. (conversation_id: {})",
                            channel_id_clone, conn_no, conversation_id_clone
                        );
                    }
                    let eof_payload = conn_no.to_be_bytes();
                    let eof_frame = Frame::new_control_with_pool(
                        ControlMessage::SendEOF,
                        &eof_payload,
                        &buffer_pool_clone,
                    );
                    if let Err(e) = event_sender
                        .send_with_natural_backpressure(
                            eof_frame.encode_with_pool(&buffer_pool_clone),
                        )
                        .await
                    {
                        error!(
                            "Channel({}): Failed to send EOF via EventDrivenSender for conn_no {}: {} (conversation_id: {})",
                            channel_id_clone, conn_no, e, conversation_id_clone
                        );
                    }
                    break;
                }
                Ok(n) if n > 0 => {
                    unsafe {
                        read_buffer.advance_mut(n);
                    }

                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!(
                            "Server-side TCP reader received {} bytes for conn_no: {} (channel_id: {}, conversation_id: {})",
                            n, conn_no, channel_id_clone, conversation_id_clone
                        );

                        if n <= 100 {
                            debug!(
                                "Data: {:?} (channel_id: {}, conversation_id: {})",
                                &read_buffer[0..n],
                                channel_id_clone,
                                conversation_id_clone
                            );
                        } else {
                            debug!(
                                "Data (first 50 bytes): {:?} (channel_id: {}, conversation_id: {})",
                                &read_buffer[0..50],
                                channel_id_clone,
                                conversation_id_clone
                            );
                        }
                    }

                    let current_payload_bytes_slice = &read_buffer[0..n];

                    let data_frame = Frame::new_data_with_pool(
                        conn_no,
                        current_payload_bytes_slice,
                        &buffer_pool_clone,
                    );

                    encode_buffer.clear();
                    let bytes_written = data_frame.encode_into(&mut encode_buffer);

                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!("Encoded frame with conn_no {} and {} bytes payload into {} total bytes (channel_id: {}, conversation_id: {})",
                            conn_no, n, bytes_written, channel_id_clone, conversation_id_clone);
                    }

                    let encoded_frame_bytes = encode_buffer.split_to(bytes_written).freeze();

                    let send_start = std::time::Instant::now();
                    match event_sender
                        .send_with_natural_backpressure(encoded_frame_bytes.clone())
                        .await
                    {
                        Ok(_) => {
                            let send_latency = send_start.elapsed();

                            crate::metrics::METRICS_COLLECTOR.record_message_sent(
                                &channel_id_clone,
                                encoded_frame_bytes.len() as u64,
                                Some(send_latency),
                            );

                            if unlikely!(crate::logger::is_verbose_logging()) {
                                debug!("Successfully sent data frame via EventDrivenSender for conn_no {} (channel_id: {}, conversation_id: {})", conn_no, channel_id_clone, conversation_id_clone);
                            }
                        }
                        Err(e) => {
                            crate::metrics::METRICS_COLLECTOR
                                .record_error(&channel_id_clone, "webrtc_send_failed");

                            if unlikely!(crate::logger::is_verbose_logging()) {
                                debug!("Failed to send data frame via EventDrivenSender for conn_no {}: {} (channel_id: {}, conversation_id: {})", conn_no, e, channel_id_clone, conversation_id_clone);
                            }
                            break;
                        }
                    }
                }
                Ok(_) => {}
                Err(e) => {
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!(
                            "Error reading from client on server port (conn_no {}): {} (channel_id: {}, conversation_id: {})",
                            conn_no, e, channel_id_clone, conversation_id_clone
                        );
                    }
                    error!(
                        "Channel({}): Error reading from client on server port (conn_no {}): {} (conversation_id: {})",
                        channel_id_clone, conn_no, e, conversation_id_clone
                    );
                    break;
                }
            }
        }
        buffer_pool_clone.release(read_buffer);
        buffer_pool_clone.release(encode_buffer);
        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!("Server-side TCP reader task for conn_no {} exited (channel_id: {}, conversation_id: {})", conn_no, channel_id_clone, conversation_id_clone);
            debug!(
                "Channel({}): Server-side TCP reader task for conn_no {} ({:?}) exited. (conversation_id: {})",
                channel_id_clone, conn_no, active_protocol, conversation_id_clone
            );
        }
    });

    conn_tx
        .send((conn_no, writer, read_task))
        .await
        .map_err(|e| {
            anyhow!(
                "Failed to send new server connection {} to channel: {}",
                conn_no,
                e
            )
        })?;

    Ok(())
}
