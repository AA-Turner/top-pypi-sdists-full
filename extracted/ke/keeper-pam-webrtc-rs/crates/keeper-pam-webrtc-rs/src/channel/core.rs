// Core Channel implementation

use super::types::ActiveProtocol;
use crate::buffer_pool::{BufferPool, STANDARD_BUFFER_CONFIG};
pub(crate) use crate::error::ChannelError;
use crate::models::{
    is_database_session, is_guacd_session, Conn, ConversationType, NetworkAccessChecker,
    StreamHalf, TunnelTimeouts,
};
use crate::runtime::get_runtime;
use crate::tube_and_channel_helpers::parse_network_rules_from_settings;
use crate::tube_protocol::{try_parse_frame, CloseConnectionReason, ControlMessage, Frame};
use crate::unlikely;
use crate::webrtc_data_channel::{
    EventDrivenSender, WebRTCDataChannel, SCTP_HIGH_WATER, STANDARD_BUFFER_THRESHOLD,
};
use anyhow::{anyhow, Result};
use bytes::Bytes;
use bytes::{BufMut, BytesMut};
use dashmap::DashMap;
use futures::FutureExt;
use log::{debug, error, info, warn};
use parking_lot::Mutex;
use serde::Deserialize;
use serde_json::Value as JsonValue; // For clarity when matching JsonValue types
use std::collections::HashMap;
use std::sync::Arc;
use tokio::net::tcp::OwnedWriteHalf;
use tokio::net::TcpListener;
use tokio::sync::{mpsc, Mutex as AsyncMutex};
use tokio::task::{AbortHandle, JoinHandle};
// Add this

// Import from sibling modules
use super::assembler::{has_fragment_header, FragmentBuffer, FragmentHeader, FRAGMENT_HEADER_SIZE};
use super::frame_handling::handle_incoming_frame;
use crate::tube_protocol::Capabilities;
use crate::tube_protocol::CloseConnectionReason as TubeCloseReason;
use guacr_handlers::video::VideoOutput;
use guacr_protocol::{GuacdInstruction, GuacdParser};
/// Message types sent from Channel to Python handler
#[derive(Debug, Clone)]
#[allow(dead_code)] // Used by Python bindings
pub enum PythonHandlerMessage {
    /// A new connection was opened
    ConnectionOpened { conn_no: u32 },
    /// Data received on a connection
    Data { conn_no: u32, payload: Bytes },
    /// A connection was closed
    ConnectionClosed {
        conn_no: u32,
        reason: TubeCloseReason,
    },
}

/// Message types sent from Python handler back to WebRTC (outbound)
/// These are queued by send_handler_data and processed by the outbound sender task
#[derive(Debug)]
#[allow(dead_code)] // Used by Python handler infrastructure
pub struct PythonHandlerOutbound {
    pub conversation_id: String,
    pub conn_no: u32,
    pub data: Bytes,
}

// --- Protocol-specific state definitions ---
#[derive(Default, Clone, Debug)]
pub(crate) struct ChannelSocks5State {
    // SOCKS5 handshake and target address are handled directly in server.rs
    // without persistent state storage
}

#[derive(Debug, Default, Clone)]
pub(crate) struct ChannelGuacdState {
    // Add GuacD specific fields, e.g., Guacamole client state, connected things
}

// Potentially, PortForward might also have a state if we need to store target addresses resolved from settings
#[derive(Debug, Default, Clone)]
pub(crate) struct ChannelPortForwardState {
    pub target_host: Option<String>,
    pub target_port: Option<u16>,
}

#[derive(Debug, Default, Clone)]
pub(crate) struct ChannelPythonHandlerState {
    // Track active virtual connections in PythonHandler mode
    // These are connections that have been confirmed via ConnectionOpened
    pub active_connections: std::collections::HashSet<u32>,
}

#[derive(Debug, Default, Clone)]
pub(crate) struct ChannelDatabaseProxyState {
    // Database proxy state - currently minimal as most params passed via guacd_params
    // Can be expanded if needed for connection tracking
}

#[derive(Clone, Debug)]
pub(crate) enum ProtocolLogicState {
    Socks5(ChannelSocks5State),
    Guacd(ChannelGuacdState),
    PortForward(ChannelPortForwardState),
    PythonHandler(ChannelPythonHandlerState),
    DatabaseProxy(ChannelDatabaseProxyState),
}

impl Default for ProtocolLogicState {
    fn default() -> Self {
        ProtocolLogicState::PortForward(ChannelPortForwardState::default()) // Default to PortForward
    }
}
// --- End Protocol-specific state definitions ---

// --- ConnectAs Settings Definition ---
#[derive(Deserialize, Debug, Clone, Default)] // Added Deserialize
pub struct ConnectAsSettings {
    #[serde(alias = "allow_supply_user", default)]
    pub allow_supply_user: bool,
    #[serde(alias = "allow_supply_host", default)]
    pub allow_supply_host: bool,
    #[serde(alias = "gateway_private_key")]
    pub gateway_private_key: Option<String>,
}
// --- End ConnectAs Settings Definition ---

/// Channel instance. Owns the data‑channel and a map of active back‑end TCP streams.
pub struct Channel {
    pub(crate) webrtc: WebRTCDataChannel,
    /// One shared EventDrivenSender per tube — all logical connections (conn_no)
    /// clone this so they share one bounded mpsc channel and one actor task.
    /// Created on first use (setup_outbound_task or start_server).
    pub(crate) event_sender: Option<EventDrivenSender>,
    pub(crate) conns: Arc<DashMap<u32, Conn>>,
    pub(crate) conn_generations: Arc<DashMap<u32, std::sync::atomic::AtomicU64>>,
    pub(crate) rx_from_dc: mpsc::UnboundedReceiver<Bytes>,
    /// Shared sender for rx_from_dc; taken and dropped in on_close when DataChannel closes.
    pub(crate) tx_from_dc: Arc<Mutex<Option<mpsc::UnboundedSender<Bytes>>>>,
    pub(crate) channel_id: String,
    pub(crate) timeouts: TunnelTimeouts,
    pub(crate) network_checker: Option<NetworkAccessChecker>,
    pub(crate) should_exit: Arc<std::sync::atomic::AtomicBool>,
    pub(crate) shutdown_notify: Arc<tokio::sync::Notify>,
    /// Set when the data channel closes unexpectedly (ICE restart in progress).
    /// Cleared when it reopens. Read by the guacd nop keepalive task in connections.rs.
    pub(crate) ice_restart_active: Arc<std::sync::atomic::AtomicBool>,
    pub(crate) server_mode: bool,
    // Server-related fields
    pub(crate) local_listen_addr: Option<String>,
    pub(crate) actual_listen_addr: Option<std::net::SocketAddr>,
    pub(crate) local_client_server: Option<Arc<TcpListener>>,
    pub(crate) local_client_server_task: Option<JoinHandle<()>>,
    pub(crate) local_client_server_conn_tx:
        Option<mpsc::Sender<(u32, OwnedWriteHalf, JoinHandle<()>)>>,
    pub(crate) local_client_server_conn_rx:
        Option<mpsc::Receiver<(u32, OwnedWriteHalf, JoinHandle<()>)>>,

    // Task tracking for proper resource management (not just RAII safety net)
    /// Track server connection handler tasks for explicit cancellation on shutdown
    pub(crate) server_connection_tasks: Arc<Mutex<Vec<AbortHandle>>>,
    /// Track state monitoring tasks for explicit cancellation
    pub(crate) state_monitoring_tasks: Arc<Mutex<Vec<AbortHandle>>>,
    /// Track delayed cleanup tasks for explicit cancellation
    pub(crate) cleanup_tasks: Arc<Mutex<Vec<AbortHandle>>>,

    // Protocol handling integrated into Channel
    pub(crate) active_protocol: ActiveProtocol,
    pub(crate) protocol_state: ProtocolLogicState,
    /// Tunnel protocol handler (SOCKS5 or PortForward) for trait-based dispatch
    pub(crate) tunnel_protocol: Option<Arc<dyn super::tunnel_protocol::TunnelProtocol>>,

    // New fields for Guacd and ConnectAs specific settings
    pub(crate) guacd_host: Option<String>,
    pub(crate) guacd_port: Option<u16>,
    pub(crate) connect_as_settings: ConnectAsSettings,
    pub(crate) guacd_params: Arc<AsyncMutex<HashMap<String, String>>>, // Kept for now for minimal diff
    // Database proxy settings (for DatabaseProxy protocol)
    pub(crate) proxy_host: Option<String>,
    pub(crate) proxy_port: Option<u16>,
    pub(crate) db_params: Arc<AsyncMutex<HashMap<String, String>>>,

    // Protocol handler registry and conversation type (for built-in handlers)
    pub(crate) handler_registry: Option<Arc<guacr_handlers::ProtocolHandlerRegistry>>,
    #[allow(dead_code)]
    pub(crate) conversation_type: Option<ConversationType>,

    // Handler senders for forwarding inbound messages to protocol handlers
    pub(crate) handler_senders: Arc<DashMap<u32, mpsc::Sender<Bytes>>>,

    // Buffer pool for efficient buffer management
    pub(crate) buffer_pool: BufferPool,

    // For signaling connection task closures to the main Channel run loop
    pub(crate) conn_closed_tx: mpsc::UnboundedSender<(u32, String)>, // (conn_no, channel_id)
    conn_closed_rx: Option<mpsc::UnboundedReceiver<(u32, String)>>,
    // Stores the conn_no of the primary Guacd data connection
    pub(crate) primary_guacd_conn_no: Arc<AsyncMutex<Option<u32>>>,

    // Store the close reason when control connection closes
    pub(crate) channel_close_reason: Arc<AsyncMutex<Option<CloseConnectionReason>>>,
    // Store the error message from guacd when it sends an error instruction
    pub(crate) channel_close_message: Arc<AsyncMutex<Option<String>>>,
    /// Set when conn_no 0 (control connection) is closed. Signals the tube to close itself.
    pub(crate) control_connection_closed: Arc<std::sync::atomic::AtomicBool>,
    // Callback token for router communication
    pub(crate) callback_token: Option<String>,
    // KSM config for router communication
    pub(crate) ksm_config: Option<String>,
    // Client version for router communication
    pub(crate) client_version: String,
    /// Capabilities enabled for this channel
    pub(crate) capabilities: Capabilities,
    /// Multi-channel assembler (created when FRAGMENTATION capability is enabled)
    #[allow(dead_code)] // Used at runtime when FRAGMENTATION enabled
    pub(crate) assembler: Option<super::assembler::Assembler>,
    /// Pending fragment buffers for reassembly (seq_id -> buffer)
    /// Used when FRAGMENTATION capability is enabled to reassemble fragmented frames
    pub(crate) pending_fragments: DashMap<u32, FragmentBuffer>,
    // Python handler channel for PythonHandler protocol mode
    pub(crate) python_handler_tx: Option<mpsc::Sender<PythonHandlerMessage>>,

    // Task completion tracking (passed from Tube for handler task monitoring)
    // Handler tasks signal completion via this channel to ensure proper cleanup
    pub(crate) spawned_task_completion_tx: Arc<tokio::sync::mpsc::UnboundedSender<()>>,

    /// H.264 video output handle for graphical protocols (RDP, VNC, RBI).
    /// `None` for terminal protocols, guacd sessions, old vault clients, and encoder failures.
    pub(crate) video_output: Option<Arc<dyn VideoOutput>>,
}

// NOTE: Channel is intentionally NOT Clone because it contains a single-consumer receiver
// (rx_from_dc) that can only be owned by one instance. Cloning would create a broken
// receiver that never receives messages. Use Arc<Channel> for sharing instead.

pub struct ChannelParams {
    pub webrtc: WebRTCDataChannel,
    pub rx_from_dc: mpsc::UnboundedReceiver<Bytes>,
    /// Shared sender for rx_from_dc; taken and dropped in on_close to unblock channel.run().
    /// Wrapped in Arc<Mutex<Option>> because on_message also holds a clone - we need a single
    /// owner to drop so rx_from_dc.recv() returns None when DataChannel closes.
    pub tx_from_dc: Arc<Mutex<Option<mpsc::UnboundedSender<Bytes>>>>,
    pub channel_id: String,
    /// ID of the Tube that owns this channel. Accepted for API compatibility;
    /// not currently stored on Channel (adaptive backpressure removed).
    #[allow(dead_code)]
    pub tube_id: String,
    pub timeouts: Option<TunnelTimeouts>,
    pub protocol_settings: HashMap<String, JsonValue>,
    pub server_mode: bool,
    pub shutdown_notify: Arc<tokio::sync::Notify>, // For async cancellation
    pub callback_token: Option<String>,
    pub ksm_config: Option<String>,
    pub client_version: String,
    /// Capabilities enabled for this channel (e.g., FRAGMENTATION for multi-channel)
    pub capabilities: Capabilities,
    /// Optional Python handler channel for PythonHandler protocol mode
    pub python_handler_tx: Option<mpsc::Sender<PythonHandlerMessage>>,
    pub handler_registry: Option<Arc<guacr_handlers::ProtocolHandlerRegistry>>,
    /// Task completion tracking from Tube (for handler task monitoring)
    pub spawned_task_completion_tx: Arc<tokio::sync::mpsc::UnboundedSender<()>>,
    /// H.264 video output for graphical sessions. `None` for GuacamoleOnly sessions.
    pub video_output: Option<Arc<dyn VideoOutput>>,
}

impl Channel {
    pub async fn new(params: ChannelParams) -> Result<Self> {
        let ChannelParams {
            webrtc,
            rx_from_dc,
            tx_from_dc,
            channel_id,
            tube_id: _,
            timeouts,
            protocol_settings,
            server_mode,
            shutdown_notify,
            callback_token,
            ksm_config,
            client_version,
            capabilities,
            python_handler_tx,
            handler_registry,
            spawned_task_completion_tx,
            video_output,
        } = params;
        debug!("Channel::new called (channel_id: {})", channel_id);
        if unlikely!(crate::logger::is_verbose_logging()) {
            debug!(
                "Initial protocol_settings received by Channel::new (channel_id: {})",
                channel_id
            );
        }

        let (server_conn_tx, server_conn_rx) = mpsc::channel(32);
        let (conn_closed_tx, conn_closed_rx) = mpsc::unbounded_channel::<(u32, String)>();

        // Use standard buffer pool configuration for consistent performance
        let buffer_pool = BufferPool::new(STANDARD_BUFFER_CONFIG);

        let network_checker = parse_network_rules_from_settings(&protocol_settings);

        let determined_protocol; // Declare without initial assignment
        let initial_protocol_state; // Declare without initial assignment

        let mut guacd_host_setting: Option<String> = None;
        let mut guacd_port_setting: Option<u16> = None;
        let mut temp_initial_guacd_params_map = HashMap::new();

        let mut local_listen_addr_setting: Option<String> = None;
        let mut stored_conversation_type: Option<ConversationType> = None;

        // Database proxy settings
        let mut proxy_host_setting: Option<String> = None;
        let mut proxy_port_setting: Option<u16> = None;
        let mut temp_db_params_map: HashMap<String, String> = HashMap::new();

        if let Some(protocol_name_val) = protocol_settings.get("conversationType") {
            if let Some(protocol_name_str) = protocol_name_val.as_str() {
                match protocol_name_str.parse::<ConversationType>() {
                    Ok(parsed_conversation_type) => {
                        // Database sessions can use TWO modes:
                        // 1. DatabaseProxy mode: Rust connects directly to database (KeeperDB Proxy in tunnel mode)
                        //    - Used for: tunnelType == "database" (port forwards to database via KeeperDB Proxy)
                        //    - Configuration: 'proxy' or 'host' block with target database host/port
                        //    - conversationType: 'tunnel' with tunnelType: 'database' and databaseType: 'mysql'
                        //
                        // 2. Guacd mode: Rust connects to guacd, which handles database connection (traditional)
                        //    - Used for: conversationType == mysql/postgresql/sql-server (without proxy config)
                        //    - Configuration: 'guacd' block with guacd server host/port
                        //    - Database credentials in 'guacd_params' are passed to guacd
                        //
                        // Note: KeeperDB (with GUI/RBI) uses conversationType: 'http', not handled here

                        let is_database_tunnel = protocol_settings
                            .get("tunnelType")
                            .and_then(|v| v.as_str())
                            .map(|s| s == "database")
                            .unwrap_or(false);

                        // Check if this is a proxy connection (has 'host' or 'proxy' block)
                        // These are ONLY sent by Vault for:
                        // - Port forward tunnels (conversationType: 'tunnel' with optional tunnelType: 'database')
                        // - The 'host' field specifies the target to proxy to
                        let has_proxy_config = protocol_settings.contains_key("proxy")
                            || protocol_settings.contains_key("host");

                        // Use DatabaseProxy mode ONLY if:
                        // 1. Explicitly marked as database tunnel (tunnelType == "database"), OR
                        // 2. Has explicit proxy/host configuration (tunnel with target host)
                        //
                        // Regular database connections (conversationType == mysql/postgresql/sql-server)
                        // WITHOUT proxy config will fall through to Guacd mode below
                        let use_database_proxy = is_database_tunnel || has_proxy_config;

                        if use_database_proxy {
                            // Determine the database protocol name
                            // If tunnelType == "database", get from databaseType field
                            // Otherwise, use conversationType (legacy path)
                            let db_protocol_name = if is_database_tunnel {
                                protocol_settings
                                    .get("databaseType")
                                    .and_then(|v| v.as_str())
                                    .unwrap_or("mysql")
                                    .to_string()
                            } else {
                                parsed_conversation_type.to_string()
                            };

                            debug!("Configuring for DatabaseProxy protocol (channel_id: {}, tunnelType: {}, databaseType: {}, conversationType: {}, has_proxy_config: {})",
                                channel_id,
                                if is_database_tunnel { "database" } else { "none" },
                                db_protocol_name,
                                protocol_name_str,
                                has_proxy_config);
                            determined_protocol = ActiveProtocol::DatabaseProxy;
                            initial_protocol_state = ProtocolLogicState::DatabaseProxy(
                                ChannelDatabaseProxyState::default(),
                            );

                            // Extract proxy host/port from 'proxy' or 'host' block
                            // These are ONLY sent by Vault for tunnel/port forward connections
                            if let Some(JsonValue::Object(proxy_map)) =
                                protocol_settings.get("proxy")
                            {
                                proxy_host_setting = proxy_map
                                    .get("proxy_host")
                                    .and_then(|v| v.as_str())
                                    .map(String::from);
                                proxy_port_setting = proxy_map
                                    .get("proxy_port")
                                    .and_then(|v| v.as_u64())
                                    .map(|p| p as u16);
                                debug!(
                                    "Parsed proxy settings from 'proxy' block: host={:?}, port={:?} (channel_id: {})",
                                    proxy_host_setting, proxy_port_setting, channel_id
                                );
                            }
                            // Vault format for tunnel target: { "host": { "hostName": "...", "port": 3306 } }
                            else if let Some(JsonValue::Object(host_map)) =
                                protocol_settings.get("host")
                            {
                                proxy_host_setting = host_map
                                    .get("hostName")
                                    .and_then(|v| v.as_str())
                                    .map(String::from);
                                proxy_port_setting = host_map
                                    .get("port")
                                    .and_then(|v| v.as_u64())
                                    .map(|p| p as u16);
                                debug!(
                                    "Parsed proxy settings from 'host' block (tunnel target): host={:?}, port={:?} (channel_id: {})",
                                    proxy_host_setting, proxy_port_setting, channel_id
                                );
                            }

                            // Process db_params for database parameters
                            if let Some(db_params_json_val) = protocol_settings.get("db_params") {
                                if let JsonValue::Object(map) = db_params_json_val {
                                    temp_db_params_map = map
                                        .iter()
                                        .filter_map(|(k, v)| match v {
                                            JsonValue::String(s) => Some((k.clone(), s.clone())),
                                            JsonValue::Bool(b) => Some((k.clone(), b.to_string())),
                                            JsonValue::Number(n) => {
                                                Some((k.clone(), n.to_string()))
                                            }
                                            JsonValue::Null => None,
                                            _ => None,
                                        })
                                        .collect();
                                    // Set protocol name for database type (from databaseType or conversationType)
                                    temp_db_params_map
                                        .insert("protocol".to_string(), db_protocol_name.clone());
                                    debug!("Parsed db_params for DatabaseProxy (channel_id: {}, protocol: {})",
                                        channel_id, db_protocol_name);
                                }
                            } else {
                                warn!("DatabaseProxy: 'db_params' block not found in protocol_settings (channel_id: {})", channel_id);
                            }
                        } else if is_guacd_session(&parsed_conversation_type)
                            || is_database_session(&parsed_conversation_type)
                        {
                            // Guacd mode: handles both traditional guacd sessions (SSH, RDP, VNC, etc.)
                            // AND database sessions that connect through guacd (mysql, postgresql, sql-server)
                            stored_conversation_type = Some(parsed_conversation_type.clone());
                            debug!("Configuring for GuacD protocol (channel_id: {}, protocol_type: {})", channel_id, protocol_name_str);
                            determined_protocol = ActiveProtocol::Guacd;
                            initial_protocol_state =
                                ProtocolLogicState::Guacd(ChannelGuacdState::default());

                            if let Some(guacd_dedicated_settings_val) =
                                protocol_settings.get("guacd")
                            {
                                if unlikely!(crate::logger::is_verbose_logging()) {
                                    debug!("Found 'guacd' block in protocol_settings: {:?} (channel_id: {})", guacd_dedicated_settings_val, channel_id);
                                }
                                if let JsonValue::Object(guacd_map) = guacd_dedicated_settings_val {
                                    guacd_host_setting = guacd_map
                                        .get("guacd_host")
                                        .and_then(|v| v.as_str())
                                        .map(String::from);
                                    guacd_port_setting = guacd_map
                                        .get("guacd_port")
                                        .and_then(|v| v.as_u64())
                                        .map(|p| p as u16);
                                    debug!("Parsed from dedicated 'guacd' settings block. (channel_id: {})", channel_id);
                                } else {
                                    warn!(
                                        "'guacd' block was not a JSON Object. (channel_id: {})",
                                        channel_id
                                    );
                                }
                            } else if unlikely!(crate::logger::is_verbose_logging()) {
                                debug!("No dedicated 'guacd' block found in protocol_settings. Guacd server host/port might come from guacd_params or defaults. (channel_id: {})", channel_id);
                            }

                            if let Some(guacd_params_json_val) =
                                protocol_settings.get("guacd_params")
                            {
                                debug!(
                                    "Found 'guacd_params' in protocol_settings. (channel_id: {})",
                                    channel_id
                                );
                                if unlikely!(crate::logger::is_verbose_logging()) {
                                    debug!("Raw guacd_params value for direct processing. (channel_id: {}, guacd_params_value: {:?})", channel_id, guacd_params_json_val);
                                }

                                if let JsonValue::Object(map) = guacd_params_json_val {
                                    temp_initial_guacd_params_map = map
                                        .iter()
                                        .filter_map(|(k, v)| {
                                            match v {
                                                JsonValue::String(s) => {
                                                    Some((k.clone(), s.clone()))
                                                }
                                                JsonValue::Bool(b) => {
                                                    Some((k.clone(), b.to_string()))
                                                }
                                                JsonValue::Number(n) => {
                                                    Some((k.clone(), n.to_string()))
                                                }
                                                JsonValue::Array(arr) => {
                                                    let str_arr: Vec<String> = arr
                                                        .iter()
                                                        .map(|val| match val {
                                                            JsonValue::String(s) => s.clone(),
                                                            JsonValue::Number(n) => n.to_string(),
                                                            JsonValue::Bool(b) => b.to_string(),
                                                            _ => serde_json::to_string(val)
                                                                .unwrap_or_default(),
                                                        })
                                                        .collect();
                                                    if !str_arr.is_empty() {
                                                        Some((k.clone(), str_arr.join(",")))
                                                    } else {
                                                        Some((k.clone(), "".to_string()))
                                                    }
                                                }
                                                JsonValue::Null => None, // Omit null values by not adding them
                                                // For JsonValue::Object, stringify the nested object.
                                                // This matches the behavior if a struct field was Option<JsonValue> and then stringified.
                                                JsonValue::Object(obj_map) => {
                                                    serde_json::to_string(obj_map)
                                                        .ok()
                                                        .map(|s_val| (k.clone(), s_val))
                                                }
                                            }
                                        })
                                        .collect();
                                    if unlikely!(crate::logger::is_verbose_logging()) {
                                        debug!("Populated guacd_params map directly from JSON Value. (channel_id: {})", channel_id);
                                    }

                                    // Override protocol name with correct guacd protocol name from ConversationType
                                    let guacd_protocol_name = parsed_conversation_type.to_string();
                                    temp_initial_guacd_params_map.insert(
                                        "protocol".to_string(),
                                        guacd_protocol_name.clone(),
                                    );
                                    debug!("Set guacd protocol name from ConversationType (channel_id: {}, guacd_protocol_name: {})", channel_id, guacd_protocol_name);
                                } else {
                                    error!("guacd_params was not a JSON object. Value: {:?} (channel_id: {})", guacd_params_json_val, channel_id);
                                }
                            } else {
                                debug!("'guacd_params' key not found in protocol_settings. (channel_id: {})", channel_id);
                            }
                        } else {
                            // Handle non-Guacd types like Tunnel or SOCKS5 if network rules are present
                            match parsed_conversation_type {
                                ConversationType::Tunnel => {
                                    // Check if we should use SOCKS5 protocol
                                    let should_use_socks5 = network_checker.is_some()
                                        || protocol_settings
                                            .get("socks_mode")
                                            .and_then(|v| v.as_bool())
                                            .unwrap_or(false);

                                    if should_use_socks5 {
                                        debug!("Configuring for SOCKS5 protocol (Tunnel type with network rules or socks_mode) (channel_id: {})", channel_id);
                                        determined_protocol = ActiveProtocol::Socks5;
                                        initial_protocol_state = ProtocolLogicState::Socks5(
                                            ChannelSocks5State::default(),
                                        );
                                    } else {
                                        debug!("Configuring for PortForward protocol (Tunnel type) (channel_id: {})", channel_id);
                                        determined_protocol = ActiveProtocol::PortForward;
                                        if server_mode {
                                            initial_protocol_state =
                                                ProtocolLogicState::PortForward(
                                                    ChannelPortForwardState::default(),
                                                );
                                        } else {
                                            // Try to get the target host / port from either target_host/target_port or guacd field
                                            let mut dest_host = protocol_settings
                                                .get("target_host")
                                                .and_then(|v| v.as_str())
                                                .map(String::from);
                                            let mut dest_port = protocol_settings
                                                .get("target_port")
                                                .and_then(|v| {
                                                    // First, try to get it as an u64 directly
                                                    if let Some(num) = v.as_u64() {
                                                        Some(num as u16)
                                                    }
                                                    // If that fails, try to get it as a string and parse
                                                    else if let Some(s) = v.as_str() {
                                                        s.parse::<u16>().ok()
                                                    }
                                                    // If both approaches fail, return None
                                                    else {
                                                        None
                                                    }
                                                });

                                            // If not found, check the guacd field for tunnel connections
                                            (dest_host, dest_port) =
                                                Self::extract_host_port_from_guacd(
                                                    &protocol_settings,
                                                    dest_host,
                                                    dest_port,
                                                    &channel_id,
                                                    "tunnel connections",
                                                );

                                            initial_protocol_state =
                                                ProtocolLogicState::PortForward(
                                                    ChannelPortForwardState {
                                                        target_host: dest_host,
                                                        target_port: dest_port,
                                                    },
                                                );
                                        }
                                    }
                                    if server_mode {
                                        // For PortForward server, we need a listen address
                                        local_listen_addr_setting = protocol_settings
                                            .get("local_listen_addr")
                                            .and_then(|v| v.as_str())
                                            .map(String::from);
                                    }
                                }
                                ConversationType::PythonHandler => {
                                    // PythonHandler mode: Data goes to Python callback instead of backend
                                    debug!(
                                        "Configuring for PythonHandler protocol (channel_id: {})",
                                        channel_id
                                    );
                                    if python_handler_tx.is_none() {
                                        return Err(anyhow::anyhow!(
                                            "PythonHandler protocol requires python_handler_tx to be set (channel_id: {})",
                                            channel_id
                                        ));
                                    }
                                    determined_protocol = ActiveProtocol::PythonHandler;
                                    initial_protocol_state = ProtocolLogicState::PythonHandler(
                                        ChannelPythonHandlerState::default(),
                                    );
                                }
                                _ => {
                                    // Other non-Guacd types
                                    if network_checker.is_some() {
                                        debug!("Configuring for SOCKS5 protocol (network rules present) (channel_id: {}, protocol_type: {})", channel_id, protocol_name_str);
                                        determined_protocol = ActiveProtocol::Socks5;
                                        initial_protocol_state = ProtocolLogicState::Socks5(
                                            ChannelSocks5State::default(),
                                        );
                                    } else {
                                        debug!("Configuring for PortForward protocol (defaulting) (channel_id: {}, protocol_type: {})", channel_id, protocol_name_str);
                                        determined_protocol = ActiveProtocol::PortForward;
                                        let mut dest_host = protocol_settings
                                            .get("target_host")
                                            .and_then(|v| v.as_str())
                                            .map(String::from);
                                        let mut dest_port = protocol_settings
                                            .get("target_port")
                                            .and_then(|v| v.as_u64())
                                            .map(|p| p as u16);

                                        // If not found, check the guacd field
                                        (dest_host, dest_port) = Self::extract_host_port_from_guacd(
                                            &protocol_settings,
                                            dest_host,
                                            dest_port,
                                            &channel_id,
                                            "default case",
                                        );

                                        initial_protocol_state = ProtocolLogicState::PortForward(
                                            ChannelPortForwardState {
                                                target_host: dest_host,
                                                target_port: dest_port,
                                            },
                                        );
                                    }
                                }
                            }
                        }
                    }
                    Err(_) => {
                        error!("Invalid conversationType string. Erroring out. (channel_id: {}, protocol_type: {})", channel_id, protocol_name_str);
                        return Err(anyhow::anyhow!(
                            "Invalid conversationType string: {}",
                            protocol_name_str
                        ));
                    }
                }
            } else {
                // protocol_name_val is not a string
                error!(
                    "conversationType is not a string. Erroring out. (channel_id: {})",
                    channel_id
                );
                return Err(anyhow::anyhow!("conversationType is not a string"));
            }
        } else {
            // "conversationType" not found
            error!("No specific protocol defined (conversationType missing). Erroring out. (channel_id: {})", channel_id);
            return Err(anyhow::anyhow!(
                "No specific protocol defined (conversationType missing)"
            ));
        }

        let mut final_connect_as_settings = ConnectAsSettings::default();
        if let Some(connect_as_settings_val) = protocol_settings.get("connect_as_settings") {
            debug!(
                "Found 'connect_as_settings' in protocol_settings. (channel_id: {})",
                channel_id
            );
            if unlikely!(crate::logger::is_verbose_logging()) {
                debug!(
                    "Raw connect_as_settings value. (channel_id: {}, cas_value: {:?})",
                    channel_id, connect_as_settings_val
                );
            }
            match serde_json::from_value::<ConnectAsSettings>(connect_as_settings_val.clone()) {
                Ok(parsed_settings) => {
                    final_connect_as_settings = parsed_settings;
                    debug!("Successfully deserialized connect_as_settings into ConnectAsSettings struct. (channel_id: {})", channel_id);
                    if unlikely!(crate::logger::is_verbose_logging()) {
                        debug!("Final connect_as_settings. (channel_id: {}, final_connect_as_settings: {:?})", channel_id, final_connect_as_settings);
                    }
                }
                Err(e) => {
                    error!("CRITICAL: Failed to deserialize connect_as_settings: {}. Value was: {:?} (channel_id: {})", e, connect_as_settings_val, channel_id);
                    // Returning an error here if connect_as_settings are vital
                    return Err(anyhow!("Failed to deserialize connect_as_settings: {}", e));
                }
            }
        } else {
            debug!("'connect_as_settings' key not found in protocol_settings. Using default. (channel_id: {})", channel_id);
        }

        // Construct the tunnel protocol handler based on the determined protocol
        let tunnel_protocol: Option<Arc<dyn super::tunnel_protocol::TunnelProtocol>> =
            match determined_protocol {
                ActiveProtocol::Socks5 => {
                    Some(Arc::new(super::tunnel_protocol::Socks5TunnelProtocol))
                }
                ActiveProtocol::PortForward => {
                    // Extract target from protocol state for client-mode PortForward
                    if let ProtocolLogicState::PortForward(ref pf) = initial_protocol_state {
                        if let (Some(ref host), Some(port)) = (&pf.target_host, pf.target_port) {
                            Some(Arc::new(
                                super::tunnel_protocol::PortForwardTunnelProtocol {
                                    target_host: host.clone(),
                                    target_port: port,
                                },
                            ))
                        } else if server_mode {
                            // Server-mode PortForward: target is resolved on the client side
                            // Still use PortForwardTunnelProtocol for server_handshake (just splits stream)
                            Some(Arc::new(
                                super::tunnel_protocol::PortForwardTunnelProtocol {
                                    target_host: String::new(),
                                    target_port: 0,
                                },
                            ))
                        } else {
                            None
                        }
                    } else {
                        None
                    }
                }
                _ => None, // Guacd, PythonHandler, DatabaseProxy don't use tunnel protocol
            };

        let new_channel = Self {
            webrtc,
            event_sender: None,
            conns: Arc::new(DashMap::new()),
            conn_generations: Arc::new(DashMap::new()),
            rx_from_dc,
            tx_from_dc,
            channel_id,
            timeouts: timeouts.unwrap_or_default(),
            network_checker,
            should_exit: Arc::new(std::sync::atomic::AtomicBool::new(false)),
            shutdown_notify,
            ice_restart_active: Arc::new(std::sync::atomic::AtomicBool::new(false)),
            server_mode,
            local_listen_addr: local_listen_addr_setting,
            actual_listen_addr: None,
            local_client_server: None,
            local_client_server_task: None,
            local_client_server_conn_tx: Some(server_conn_tx),
            local_client_server_conn_rx: Some(server_conn_rx),

            // Initialize task tracking for proper resource management
            server_connection_tasks: Arc::new(Mutex::new(Vec::new())),
            state_monitoring_tasks: Arc::new(Mutex::new(Vec::new())),
            cleanup_tasks: Arc::new(Mutex::new(Vec::new())),

            active_protocol: determined_protocol,
            protocol_state: initial_protocol_state,
            tunnel_protocol,

            guacd_host: guacd_host_setting,
            guacd_port: guacd_port_setting,
            connect_as_settings: final_connect_as_settings,
            guacd_params: Arc::new(AsyncMutex::new(temp_initial_guacd_params_map)),
            proxy_host: proxy_host_setting,
            proxy_port: proxy_port_setting,
            db_params: Arc::new(AsyncMutex::new(temp_db_params_map)),

            handler_registry,
            conversation_type: stored_conversation_type,

            handler_senders: Arc::new(DashMap::new()),

            buffer_pool,
            conn_closed_tx,
            conn_closed_rx: Some(conn_closed_rx),
            primary_guacd_conn_no: Arc::new(AsyncMutex::new(None)),
            channel_close_reason: Arc::new(AsyncMutex::new(None)),
            channel_close_message: Arc::new(AsyncMutex::new(None)),
            control_connection_closed: Arc::new(std::sync::atomic::AtomicBool::new(false)),
            callback_token,
            ksm_config,
            client_version,
            capabilities,
            assembler: None, // Will be created below if FRAGMENTATION enabled
            pending_fragments: DashMap::new(),
            python_handler_tx,
            spawned_task_completion_tx,
            video_output,
        };

        debug!(
            "Channel initialized (channel_id: {}, server_mode: {}, capabilities: {:?})",
            new_channel.channel_id, new_channel.server_mode, new_channel.capabilities
        );

        Ok(new_channel)
    }

    /// Process an incoming fragment, reassembling if all fragments are received.
    /// Returns Some(reassembled_data) when the complete frame is ready,
    /// None if still waiting for more fragments.
    fn process_fragment(&self, data: Bytes) -> Option<Bytes> {
        // Parse fragment header
        let header = match FragmentHeader::decode(&data) {
            Some(h) => h,
            None => {
                warn!("Channel({}): Invalid fragment header", self.channel_id);
                return None;
            }
        };

        // Extract payload (skip header)
        let payload = data.slice(FRAGMENT_HEADER_SIZE..);

        // Get or create fragment buffer
        let mut entry = self
            .pending_fragments
            .entry(header.seq_id)
            .or_insert_with(|| FragmentBuffer::new(header.total_frags));

        // Add fragment
        let complete = entry.add_fragment(header.frag_idx, payload);

        if complete {
            // All fragments received - reassemble
            let result = entry.reassemble();
            drop(entry); // Release the entry reference

            // Remove from pending
            self.pending_fragments.remove(&header.seq_id);

            if crate::logger::is_verbose_logging() {
                debug!(
                    "Channel({}): Reassembled fragmented frame (seq_id: {}, fragments: {})",
                    self.channel_id, header.seq_id, header.total_frags
                );
            }

            result
        } else {
            if crate::logger::is_verbose_logging() {
                debug!(
                    "Channel({}): Received fragment {}/{} (seq_id: {})",
                    self.channel_id,
                    header.frag_idx + 1,
                    header.total_frags,
                    header.seq_id
                );
            }
            None // Still waiting for more fragments
        }
    }

    pub async fn run(mut self) -> Result<(), ChannelError> {
        debug!("Channel.run() started (channel_id: {})", self.channel_id);
        self.setup_webrtc_state_monitoring();

        // Gateway side (server_mode=false): prime SCTP cwnd before screenshot/stream data
        // flows. The SCTP slow-start window opens at ~4380 bytes; each ping+pong round-trip
        // causes the remote peer to ACK ~1 MTU, growing cwnd exponentially. Three pings
        // brings cwnd from ~4 KB to ~35 KB before the first real frame is queued.
        // handle_ping echoes the payload straight back as Pong — no protocol changes needed.
        //
        // The send is retried up to 5 times with a 20ms backoff because webrtc-rs may not
        // accept sends immediately after on_open fires (internal state races). Cycling
        // channels that close before the retries complete are detected via should_exit.
        if !self.server_mode {
            let conn_no_bytes = 0u32.to_be_bytes();
            let padding = [0u8; 1400];
            let mut payload = self.buffer_pool.acquire();
            'warmup: for ping_idx in 0..3usize {
                for attempt in 0..5usize {
                    if self.should_exit.load(std::sync::atomic::Ordering::Acquire) {
                        break 'warmup;
                    }
                    payload.clear();
                    payload.extend_from_slice(&conn_no_bytes);
                    payload.extend_from_slice(&padding);
                    match self
                        .send_control_message(crate::tube_protocol::ControlMessage::Ping, &payload)
                        .await
                    {
                        Ok(()) => break, // this ping sent; move to next
                        Err(_) if attempt < 4 => {
                            tokio::time::sleep(std::time::Duration::from_millis(20)).await;
                        }
                        Err(e) => {
                            debug!(
                                "Warmup ping {} failed after retries (channel_id: {}): {}",
                                ping_idx, self.channel_id, e
                            );
                            break 'warmup;
                        }
                    }
                }
            }
            self.buffer_pool.release(payload);
        }

        let mut buf = BytesMut::with_capacity(64 * 1024);

        // Take the receiver channel for server connections
        let mut server_conn_rx = self.local_client_server_conn_rx.take();

        // Take ownership of conn_closed_rx for the select loop
        let mut local_conn_closed_rx = self.conn_closed_rx.take().ok_or_else(|| {
            error!("conn_closed_rx was already taken or None. Channel cannot monitor connection closures. (channel_id: {})", self.channel_id);
            ChannelError::Internal("conn_closed_rx missing at start of run".to_string())
        })?;

        // Main processing loop - reads from WebRTC and dispatches frames
        while !self.should_exit.load(std::sync::atomic::Ordering::Acquire) {
            // Process any complete frames in the buffer
            while let Some(frame) = try_parse_frame(&mut buf) {
                if let Err(e) = handle_incoming_frame(&mut self, frame).await {
                    error!(
                        "Error handling frame (channel_id: {}, error: {})",
                        self.channel_id, e
                    );
                }
            }

            tokio::select! {
                // Shutdown notification - highest priority, instant wakeup
                _ = self.shutdown_notify.notified() => {
                    info!("Shutdown notification received, exiting channel run loop (channel_id: {})", self.channel_id);
                    // CRITICAL: Send guacd disconnect IMMEDIATELY so guacd closes recording FIFOs
                    // before we proceed to cleanup. This allows Python readers to see EOF and break
                    // out of the upload loop without relying on the 300s drain timeout.
                    if self.active_protocol == ActiveProtocol::Guacd {
                        self.send_guacd_disconnect_immediate().await;
                    }
                    break;
                }

                // Check for any new connections from the server
                // Fair scheduling: random polling order prevents keyboard input starvation
                maybe_conn = async { server_conn_rx.as_mut()?.recv().await }, if server_conn_rx.is_some() => {
                    if let Some((conn_no, writer, task)) = maybe_conn {
                        if unlikely!(crate::logger::is_verbose_logging()) {
                            debug!("Registering connection from server (channel_id: {})", self.channel_id);
                        }

                        // Create a stream half
                        let stream_half = StreamHalf {
                            reader: None,
                            writer,
                        };

                        // Get next generation for this conn_no - prevents reuse race during cleanup
                        // Use Relaxed ordering since generation is per-conn_no and doesn't need synchronization
                        // with other conn_no values
                        let generation = self
                            .conn_generations
                            .entry(conn_no)
                            .or_insert_with(|| std::sync::atomic::AtomicU64::new(0))
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);

                        // Create a lock-free connection with a dedicated backend task
                        let conn = Conn::new_with_backend(
                            Box::new(stream_half),
                            task,
                            conn_no,
                            self.channel_id.clone(),
                            generation,
                        ).await;

                        // Store in our lock-free registry
                        self.conns.insert(conn_no, conn);
                    } else {
                        // server_conn_rx was dropped or closed
                        server_conn_rx = None; // Prevent further polling of this arm
                    }
                }

                // Wait for more data from WebRTC
                maybe_chunk = self.rx_from_dc.recv() => {
                    match tokio::time::timeout(self.timeouts.read, async { maybe_chunk }).await { // Wrap future for timeout
                        Ok(Some(chunk)) => {
                            // Check if this is a fragment that needs reassembly
                            if self.capabilities.contains(Capabilities::FRAGMENTATION)
                                && has_fragment_header(&chunk)
                            {
                                // Process fragment through reassembly
                                if let Some(reassembled) = self.process_fragment(chunk) {
                                    buf.extend_from_slice(&reassembled);
                                    if unlikely!(crate::logger::is_verbose_logging()) {
                                        debug!("Buffer size after reassembled frame (channel_id: {}, buffer_size: {})", self.channel_id, buf.len());
                                    }
                                }
                                // If None, still waiting for more fragments - don't add anything to buf
                            } else {
                                // Not a fragment (or fragmentation disabled), add directly to buffer
                                buf.extend_from_slice(&chunk);
                                if unlikely!(crate::logger::is_verbose_logging()) {
                                    debug!("Buffer size after adding chunk (channel_id: {}, buffer_size: {})", self.channel_id, buf.len());
                                }
                            }

                            // Process pending messages might be triggered by buffer low,
                            // but also good to try after receiving new data if not recently triggered.
                        }
                        Ok(None) => {
                          info!("WebRTC data channel closed or sender dropped. (channel_id: {})", self.channel_id);

                          // CRITICAL: Send guacd disconnect when client disconnects (manual close).
                          // Same flow as shutdown_notify path - guacd must close recording FIFOs so
                          // Python readers see EOF and avoid the 300s drain timeout.
                          if self.active_protocol == ActiveProtocol::Guacd {
                              self.send_guacd_disconnect_immediate().await;
                          }

                          // CRITICAL: Brief delay to allow in-flight connection closure signals to arrive
                          // When WebRTC closes during overload/failure, backend connections may be
                          // closing simultaneously. Without this delay, their signals are lost.
                          tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

                          // Process any pending connection closure signals before exiting
                          let mut critical_conn_no: Option<u32> = None;
                          while let Ok((closed_conn_no, closed_channel_id)) = local_conn_closed_rx.try_recv() {
                              info!("Processing deferred connection closure signal (channel_id: {}, conn_no: {})", closed_channel_id, closed_conn_no);

                              // Same critical closure check as the select arm
                              if self.active_protocol == ActiveProtocol::Guacd {
                                  let primary_opt = self.primary_guacd_conn_no.lock().await;
                                  if let Some(primary_conn_no) = *primary_opt {
                                      if primary_conn_no == closed_conn_no {
                                          warn!("Critical Guacd data connection has closed (deferred processing). (channel_id: {}, conn_no: {})", self.channel_id, closed_conn_no);
                                          critical_conn_no = Some(closed_conn_no);
                                          break; // Stop processing, handle critical closure
                                      }
                                  }
                              }
                          }

                          // If we found a critical closure, run cleanup before exiting
                          if let Some(closed_conn_no) = critical_conn_no {
                              self.should_exit.store(true, std::sync::atomic::Ordering::Release);

                              // Explicitly close the failed data connection first
                              info!("Closing failed data connection ({}) due to critical upstream closure. (channel_id: {})", closed_conn_no, self.channel_id);
                              if let Err(e) = self.close_backend(closed_conn_no, CloseConnectionReason::UpstreamClosed, Some("Critical upstream closure")).await {
                                  warn!("Error closing failed data connection ({}) during critical shutdown. (channel_id: {}, error: {})", closed_conn_no, self.channel_id, e);
                              }

                              // Close control connection (conn_no 0) if needed
                              if closed_conn_no != 0 {
                                  info!("Shutting down control connection (0) due to critical upstream closure. (channel_id: {})", self.channel_id);
                                  if let Err(e) = self.close_backend(0, CloseConnectionReason::UpstreamClosed, Some("Critical upstream closure")).await {
                                      debug!("Error explicitly closing control connection (0) during critical shutdown. (channel_id: {}, error: {})", self.channel_id, e);
                                  }
                              }

                              // Clean up remaining connections
                              self.log_final_stats().await;
                              if let Err(e) = self.cleanup_all_connections().await {
                                  warn!("Error during cleanup after critical closure (channel_id: {}, error: {})", self.channel_id, e);
                              }

                              return Err(ChannelError::CriticalUpstreamClosed(self.channel_id.clone()));
                          }

                          break;
                        }
                        Err(_) => {} // unreachable: timeout is applied to an already-resolved value
                    }
                }

                // Listen for connection closure signals
                maybe_closed_conn_info = local_conn_closed_rx.recv() => {
                    if let Some((closed_conn_no, closed_channel_id)) = maybe_closed_conn_info {
                        info!("Connection task reported exit to Channel run loop. (channel_id: {}, conn_no: {})", closed_channel_id, closed_conn_no);

                        let mut is_critical_closure = false;
                        if self.active_protocol == ActiveProtocol::Guacd {
                            let primary_opt = self.primary_guacd_conn_no.lock().await;
                            if let Some(primary_conn_no) = *primary_opt {
                                if primary_conn_no == closed_conn_no {
                                    warn!("Critical Guacd data connection has closed. Initiating channel shutdown. (channel_id: {}, conn_no: {})", self.channel_id, closed_conn_no);
                                    is_critical_closure = true;
                                }
                            }
                        }

                        if is_critical_closure {
                            self.should_exit.store(true, std::sync::atomic::Ordering::Release);

                            // Read the actual close reason that was stored by the outbound task
                            // This preserves GuacdError vs UpstreamClosed distinction
                            let actual_close_reason = {
                                let guard = self.channel_close_reason.lock().await;
                                guard.unwrap_or(CloseConnectionReason::UpstreamClosed)
                            };

                            // Send Guacamole disconnect instruction then EOF to guacd backend
                            if let Some(conn_ref) = self.conns.get(&closed_conn_no) {
                                if !conn_ref.data_tx.is_closed() {
                                    debug!(
                                        "Critical closure: Sending Guacamole disconnect then EOF (channel_id: {}, conn_no: {})",
                                        self.channel_id, closed_conn_no
                                    );
                                    let disconnect_instr =
                                        GuacdInstruction::new("disconnect".to_string(), vec![]);
                                    let disconnect_bytes =
                                        GuacdParser::guacd_encode_instruction(&disconnect_instr);
                                    let _ = conn_ref
                                        .data_tx
                                        .send(crate::models::ConnectionMessage::Data(disconnect_bytes));
                                    tokio::time::sleep(crate::config::disconnect_to_eof_delay()).await;
                                    let _ = conn_ref.data_tx.send(crate::models::ConnectionMessage::Eof);
                                }
                            }

                            // Now remove from DashMap
                            if let Some((_, mut conn)) = self.conns.remove(&closed_conn_no) {
                                conn.graceful_shutdown(closed_conn_no, &self.channel_id).await;
                                debug!("Removed failed connection {} from registry", closed_conn_no);
                            }

                            // NOTE: Don't call cleanup_all_connections() here - we already closed everything above
                            // Calling it again causes hangs when trying to send over already-closed WebRTC channels

                            // Break out of the select! loop to exit cleanly
                            // The normal cleanup path at lines 730-733 will run after the loop exits
                            info!("Channel run loop exiting due to critical upstream closure (channel_id: {}, reason: {:?})", self.channel_id, actual_close_reason);
                            break;
                        }

                    } else {
                        // Conn_closed_tx was dropped, meaning all senders are gone.
                        // This might happen if the channel is already shutting down and tasks are aborting.
                        info!("Connection closure signal channel (conn_closed_rx) closed. (channel_id: {})", self.channel_id);
                        // If this is unexpected, it might warrant setting should_exit to true.
                    }
                }
            }
        }

        // Log final stats before cleanup
        self.log_final_stats().await;

        self.cleanup_all_connections().await?;

        // Check if we exited due to a critical error and return appropriate result
        // The close reason was stored by the outbound task before signaling closure
        let final_close_reason = {
            let guard = self.channel_close_reason.lock().await;
            *guard
        };

        if let Some(reason) = final_close_reason {
            if reason.is_critical() {
                info!(
                    "Channel run loop completed with critical error (channel_id: {}, reason: {:?})",
                    self.channel_id, reason
                );
                return Err(ChannelError::CriticalUpstreamClosed(
                    self.channel_id.clone(),
                ));
            }
        }

        Ok(())
    }

    pub(crate) async fn cleanup_all_connections(&mut self) -> Result<()> {
        // Stop the server if it's running
        if self.server_mode && self.local_client_server_task.is_some() {
            if let Err(e) = self.stop_server().await {
                warn!(
                    "Failed to stop server during cleanup (channel_id: {}, error: {})",
                    self.channel_id, e
                );
            }
        }

        // CRITICAL: Clean up handler-based connections first
        // Handler-based connections (guacr) don't create Conn entries in the DashMap,
        // they only exist in handler_senders. Dropping their senders signals them to exit.
        {
            let handler_conn_nos: Vec<u32> = self
                .handler_senders
                .iter()
                .map(|entry| *entry.key())
                .collect();

            if !handler_conn_nos.is_empty() {
                debug!(
                    "Cleaning up {} handler-based connections (channel_id: {})",
                    handler_conn_nos.len(),
                    self.channel_id
                );

                for conn_no in handler_conn_nos {
                    // Remove the sender to signal the handler to stop
                    // The handler's from_client.recv() will return None
                    if self.handler_senders.remove(&conn_no).is_some() {
                        debug!(
                            "Signaled handler to stop (channel_id: {}, conn_no: {})",
                            self.channel_id, conn_no
                        );
                    }
                }
            }
        }

        let close_reason = {
            let guard = self.channel_close_reason.lock().await;
            *guard
        }
        .unwrap_or(CloseConnectionReason::Normal);

        // Collect connection numbers from DashMap (TCP-based connections)
        let conn_keys = self.get_connection_ids();
        for conn_no in conn_keys {
            if conn_no != 0 {
                self.close_backend(conn_no, close_reason, None).await?;
            }
        }
        Ok(())
    }

    pub(crate) async fn send_control_message(
        &mut self,
        message: ControlMessage,
        data: &[u8],
    ) -> Result<()> {
        let frame = Frame::new_control_with_pool(message, data, &self.buffer_pool);
        let encoded = frame.encode_with_pool(&self.buffer_pool);

        let buffered_amount = self.webrtc.buffered_amount().await;
        if buffered_amount >= STANDARD_BUFFER_THRESHOLD
            && unlikely!(crate::logger::is_verbose_logging())
        {
            debug!(
                "Control message buffer full, but sending control message anyway (channel_id: {})",
                self.channel_id
            );
        }
        self.webrtc
            .send(encoded)
            .await
            .map_err(|e| anyhow::anyhow!("{}", e))?;
        Ok(())
    }

    pub(crate) async fn close_backend(
        &mut self,
        conn_no: u32,
        reason: CloseConnectionReason,
        error_message: Option<&str>,
    ) -> Result<()> {
        let total_connections = self.conns.len();
        let remaining_connections = self.get_connection_ids_except(conn_no);

        debug!("Closing connection - Connection summary (channel_id: {}, conn_no: {}, reason: {:?}, error_message: {:?}, total_connections: {}, remaining_connections: {:?})",
              self.channel_id, conn_no, reason, error_message, total_connections, remaining_connections);

        let mut buffer = self.buffer_pool.acquire();
        buffer.clear();
        buffer.extend_from_slice(&conn_no.to_be_bytes());
        buffer.put_u8(reason as u8);
        // Add optional error message (backward compatible extension)
        // Format: [msg_len: 2 bytes][msg: N bytes] - only if error_message is Some
        if let Some(msg) = error_message {
            let msg_bytes = msg.as_bytes();
            // Cap at 1KB to prevent oversized messages
            let len = msg_bytes.len().min(1024) as u16;
            buffer.put_u16(len);
            buffer.extend_from_slice(&msg_bytes[..len as usize]);
        }
        let msg_data = buffer.freeze();

        // Mark connection as CLOSING to prevent reuse during cleanup window
        if let Some(conn_ref) = self.conns.get(&conn_no) {
            conn_ref.state.store(
                crate::models::CONN_STATE_CLOSING,
                std::sync::atomic::Ordering::Release,
            );
            debug!(
                "Marked connection {} as CLOSING (channel_id: {})",
                conn_no, self.channel_id
            );
        }

        self.internal_handle_connection_close(conn_no, reason)
            .await?;

        // CRITICAL: Don't fail cleanup if we can't send the control message
        // If WebRTC is already closed/closing, the send will fail, but we MUST
        // still perform cleanup (cancel backend task, shutdown TCP, remove from map)
        if let Err(e) = self
            .send_control_message(ControlMessage::CloseConnection, &msg_data)
            .await
        {
            warn!(
                "Failed to send CloseConnection control message, continuing with cleanup anyway (channel_id: {}, conn_no: {}, error: {})",
                self.channel_id, conn_no, e
            );
        }

        // =========================================================================
        // CONNECTION MODEL:
        //
        // TUNNEL MODE (PortForward, SOCKS5, DatabaseProxy): 2 to N+1 connections.
        //   Each terminal session = one connection (conn 1, 2, 3, ...). conn 0 may exist
        //   but is not special. Closing conn N does NOT close conn 0.
        //
        // GUACD MODE: conn 0 = control, conn 1 = primary Guacd data (always paired).
        //   When closing conn 1 we close 0 to trigger the close of all channels
        //
        // When conn_no 0 (control connection) is closed, the channel sets should_exit.
        // The Tube reacts when the control channel (label "control") exits by closing
        // the tube via REGISTRY.close_tube() - see tube.rs create_channel spawn task.
        // =========================================================================

        self.close_tunnel_channel(conn_no, reason).await;
        Ok(())
    }

    /// Internal method for closing connections without sending a CloseConnection message
    /// This is used when handling received CloseConnection messages to prevent feedback loops
    pub(crate) async fn internal_close_backend_no_message(
        &mut self,
        conn_no: u32,
        reason: CloseConnectionReason,
    ) -> Result<()> {
        let total_connections = self.conns.len();
        let remaining_connections = self.get_connection_ids_except(conn_no);

        debug!("Closing connection (no message) - Connection summary (channel_id: {}, conn_no: {}, reason: {:?}, total_connections: {}, remaining_connections: {:?})",
              self.channel_id, conn_no, reason, total_connections, remaining_connections);

        // Mark connection as CLOSING to prevent reuse during cleanup window
        if let Some(conn_ref) = self.conns.get(&conn_no) {
            conn_ref.state.store(
                crate::models::CONN_STATE_CLOSING,
                std::sync::atomic::Ordering::Release,
            );
            debug!(
                "Marked connection {} as CLOSING (no message) (channel_id: {})",
                conn_no, self.channel_id
            );
        }

        // Now safe to clean up internal state
        self.internal_handle_connection_close(conn_no, reason)
            .await?;

        self.close_tunnel_channel(conn_no, reason).await;
        Ok(())
    }

    pub(crate) async fn internal_handle_connection_close(
        &mut self,
        conn_no: u32,
        reason: CloseConnectionReason,
    ) -> Result<()> {
        debug!(
            "internal_handle_connection_close (channel_id: {})",
            self.channel_id
        );

        // If this is the control connection (conn_no 0) or we're shutting down due to an error,
        // and we're in server mode, stop the server to prevent new connections
        if self.server_mode
            && (conn_no == 0
                || matches!(
                    reason,
                    CloseConnectionReason::UpstreamClosed | CloseConnectionReason::Error
                ))
            && self.local_client_server_task.is_some()
        {
            debug!(
                "Stopping server due to critical connection closure (channel_id: {})",
                self.channel_id
            );
            if let Err(e) = self.stop_server().await {
                warn!(
                    "Failed to stop server during connection close (channel_id: {}, error: {})",
                    self.channel_id, e
                );
            }
        }

        match self.active_protocol {
            ActiveProtocol::Socks5 => {
                // SOCKS5 connections are stateless after handshake, no special cleanup needed
            }
            ActiveProtocol::Guacd => {
                // Check if this was the primary data connection (single lock to avoid deadlock)
                let mut primary_guard = self.primary_guacd_conn_no.lock().await;
                if let Some(primary_conn_no) = *primary_guard {
                    if primary_conn_no == conn_no {
                        debug!("Primary GuacD data connection closed, clearing reference (channel_id: {})", self.channel_id);
                        *primary_guard = None;
                    }
                }
            }
            ActiveProtocol::PortForward => {
                // Port forwarding connections are just TCP streams, no special cleanup needed
            }
            ActiveProtocol::PythonHandler => {
                // PythonHandler connections send close events to Python, no special cleanup needed here
            }
            ActiveProtocol::DatabaseProxy => {
                // DatabaseProxy connections are similar to Guacd - TCP streams with handshake
                // No special cleanup needed beyond what's done for Guacd
            }
        }

        // CRITICAL: Clean up handler senders to signal built-in handlers to stop
        // Dropping the sender causes from_client.recv() to return None in the handler,
        // allowing it to exit gracefully. Without this, handlers block forever waiting
        // for messages that will never come after WebRTC closes.
        {
            if self.handler_senders.remove(&conn_no).is_some() {
                debug!(
                    "Removed handler sender for conn {} to signal handler shutdown (channel_id: {})",
                    conn_no, self.channel_id
                );
            }
        }

        Ok(())
    }

    /// Send Guacamole disconnect to all guacd connections immediately (no EOF, no remove).
    /// Called on shutdown notification so guacd closes recording FIFOs before cleanup runs.
    /// This allows Python readers to see EOF and break out of the upload loop promptly.
    pub(crate) async fn send_guacd_disconnect_immediate(&self) {
        let conn_keys: Vec<u32> = self.get_connection_ids();
        for conn_no in conn_keys {
            if let Some(conn_ref) = self.conns.get(&conn_no) {
                if !conn_ref.data_tx.is_closed() {
                    debug!(
                        "send_guacd_disconnect_immediate: Sending disconnect (channel_id: {}, conn_no: {})",
                        self.channel_id, conn_no
                    );
                    let disconnect_instr = GuacdInstruction::new("disconnect".to_string(), vec![]);
                    let disconnect_bytes = GuacdParser::guacd_encode_instruction(&disconnect_instr);
                    let _ = conn_ref
                        .data_tx
                        .send(crate::models::ConnectionMessage::Data(disconnect_bytes));
                }
            }
        }
    }

    /// Close a single connection: send Guacamole disconnect (guacd only), then EOF, cancel read task, remove from map, graceful shutdown.
    ///
    /// For guacd: sends protocol-level disconnect instruction first so guacd initiates orderly
    /// shutdown (flushes/closes recording FIFOs) before we send TCP FIN. Without this, guacd
    /// may not react until the next read cycle, and ses/tys/tim pipes can hit timeout.
    async fn close_single_connection(&self, conn_no: u32, _reason: CloseConnectionReason) {
        if let Some(conn_ref) = self.conns.get(&conn_no) {
            if self.active_protocol == ActiveProtocol::Guacd {
                // Phase 1: Send Guacamole disconnect instruction - guacd reacts immediately
                debug!(
                    "close_single_connection: Sending Guacamole disconnect instruction (channel_id: {}, conn_no: {})",
                    self.channel_id, conn_no
                );
                let disconnect_instr = GuacdInstruction::new("disconnect".to_string(), vec![]);
                let disconnect_bytes = GuacdParser::guacd_encode_instruction(&disconnect_instr);
                let _ = conn_ref
                    .data_tx
                    .send(crate::models::ConnectionMessage::Data(disconnect_bytes));
                let delay = crate::config::disconnect_to_eof_delay();
                debug!(
                    "close_single_connection: Waiting {:?} for guacd to process disconnect (channel_id: {}, conn_no: {})",
                    delay, self.channel_id, conn_no
                );
                tokio::time::sleep(delay).await;
            }
            // Phase 2: Send EOF for TCP-level shutdown
            debug!(
                "close_single_connection: Sending EOF for TCP shutdown (channel_id: {}, conn_no: {})",
                self.channel_id, conn_no
            );
            let _ = conn_ref.data_tx.send(crate::models::ConnectionMessage::Eof);
            conn_ref.cancel_read_task.cancel();
        }
        if let Some((_, mut conn)) = self.conns.remove(&conn_no) {
            debug!(
                "close_single_connection: Starting graceful_shutdown (channel_id: {}, conn_no: {})",
                self.channel_id, conn_no
            );
            conn.graceful_shutdown(conn_no, &self.channel_id).await;
            debug!(
                "close_single_connection: graceful_shutdown complete (channel_id: {}, conn_no: {})",
                self.channel_id, conn_no
            );
        }
    }

    /// Close tunnel channel(s). For guacd or conn 0: close all connections and set should_exit.
    /// Otherwise: close only the specified connection.
    pub(crate) async fn close_tunnel_channel(&self, conn_no: u32, reason: CloseConnectionReason) {
        let is_guacd = self.active_protocol == ActiveProtocol::Guacd;
        debug!(
            "close_tunnel_channel: entry (channel_id: {}, conn_no: {}, reason: {:?}, is_guacd: {})",
            self.channel_id, conn_no, reason, is_guacd
        );

        if is_guacd || conn_no == 0 {
            self.control_connection_closed
                .store(true, std::sync::atomic::Ordering::Release);
            let channel_id = self.channel_id.clone();
            let close_futures: Vec<_> = self
                .get_connection_ids()
                .into_iter()
                .filter(|&c| c != 0)
                .map(|c| {
                    let channel_id = channel_id.clone();
                    let fut = self.close_single_connection(c, reason);
                    async move {
                        if let Err(e) = std::panic::AssertUnwindSafe(fut).catch_unwind().await {
                            error!(
                                "Panic during close_single_connection (conn_no: {}, channel_id: {}): {:?}",
                                c, channel_id, e
                            );
                        }
                    }
                })
                .collect();
            futures::future::join_all(close_futures).await;
            self.close_single_connection(0, reason).await;
            self.should_exit
                .store(true, std::sync::atomic::Ordering::Release);
            self.shutdown_notify.notify_waiters();
        } else {
            self.close_single_connection(conn_no, reason).await;
        }
    }

    /// Get a list of all active connection IDs
    pub(crate) fn get_connection_ids(&self) -> Vec<u32> {
        Self::extract_connection_ids(&self.conns)
    }

    /// Get a list of all active connection IDs except the specified one
    pub(crate) fn get_connection_ids_except(&self, exclude_conn_no: u32) -> Vec<u32> {
        self.conns
            .iter()
            .map(|entry| *entry.key())
            .filter(|&id| id != exclude_conn_no)
            .collect()
    }

    /// Static helper to extract connection IDs from any DashMap reference
    fn extract_connection_ids(conns: &DashMap<u32, Conn>) -> Vec<u32> {
        conns.iter().map(|entry| *entry.key()).collect()
    }

    /// Helper to extract host/port from guacd settings if not already set
    fn extract_host_port_from_guacd(
        protocol_settings: &HashMap<String, JsonValue>,
        mut dest_host: Option<String>,
        mut dest_port: Option<u16>,
        channel_id: &str,
        context: &str,
    ) -> (Option<String>, Option<u16>) {
        if dest_host.is_none() || dest_port.is_none() {
            if let Some(guacd_obj) = protocol_settings.get("guacd").and_then(|v| v.as_object()) {
                if dest_host.is_none() {
                    dest_host = guacd_obj
                        .get("guacd_host")
                        .and_then(|v| v.as_str())
                        .map(|s| s.trim().to_string()); // Trim whitespace
                }
                if dest_port.is_none() {
                    dest_port = guacd_obj
                        .get("guacd_port")
                        .and_then(|v| v.as_u64())
                        .map(|p| p as u16);
                }
                debug!(
                    "Extracted target from guacd field ({}): host={:?}, port={:?} (channel_id: {})",
                    context, dest_host, dest_port, channel_id
                );
            }
        }
        (dest_host, dest_port)
    }

    /// Log comprehensive WebRTC statistics when a channel closes
    pub async fn log_final_stats(&mut self) {
        let total_connections = self.conns.len();
        let connection_ids = self.get_connection_ids();
        // buffered_amount() at close: shows any data still queued in SCTP at teardown.
        let sctp_at_close = self.webrtc.buffered_amount().await as usize;
        let app_queued = self
            .event_sender
            .as_ref()
            .map(|s| s.queue_depth())
            .unwrap_or(0);
        // Peak SCTP buffer depth is no longer tracked on EventDrivenSender; the metrics
        // collector records it per-pause via record_backpressure_pause().
        let (pacing_pauses, pacing_paused_us, peak_sctp) = crate::metrics::METRICS_COLLECTOR
            .get_pacing_stats(&self.channel_id)
            .unwrap_or((0, 0, 0));

        if sctp_at_close > SCTP_HIGH_WATER {
            warn!(
                "Channel '{}' closed with {} bytes in SCTP send buffer (>{} KB high-water) — \
                 backend data was ahead of the WebRTC link at close time \
                 (protocol: {:?}, app_queued: {} bytes)",
                self.channel_id,
                sctp_at_close,
                SCTP_HIGH_WATER / 1024,
                self.active_protocol,
                app_queued,
            );
        }

        info!(
            "Channel '{}' closing — connections: {}: {:?} | \
             sctp_at_close: {} B, peak_sctp: {} B, app_queued: {} B | \
             pacing: {} pauses, {:.1}ms total \
             (server_mode: {}, protocol: {:?})",
            self.channel_id,
            total_connections,
            connection_ids,
            sctp_at_close,
            peak_sctp,
            app_queued,
            pacing_pauses,
            pacing_paused_us as f64 / 1000.0,
            self.server_mode,
            self.active_protocol,
        );
    }
}

// Ensure all resources are properly cleaned up
impl Drop for Channel {
    fn drop(&mut self) {
        self.should_exit
            .store(true, std::sync::atomic::Ordering::Release);

        // Proper resource handling: Abort all tracked tasks explicitly
        // This provides graceful shutdown instead of relying solely on RAII safety net
        // Using parking_lot::Mutex::lock() which blocks but never poisons
        let mut tasks = self.server_connection_tasks.lock();
        for handle in tasks.drain(..) {
            handle.abort();
        }
        drop(tasks);

        let mut tasks = self.state_monitoring_tasks.lock();
        for handle in tasks.drain(..) {
            handle.abort();
        }
        drop(tasks);

        let mut tasks = self.cleanup_tasks.lock();
        for handle in tasks.drain(..) {
            handle.abort();
        }
        drop(tasks);

        // Abort server task
        if let Some(task) = &self.local_client_server_task {
            task.abort();
        }

        let runtime = get_runtime();
        let webrtc = self.webrtc.clone();
        let channel_id = self.channel_id.clone();
        let conns_clone = Arc::clone(&self.conns); // Clone Arc for use in the spawned task
        let buffer_pool_clone = self.buffer_pool.clone();
        let active_protocol = self.active_protocol;

        runtime.spawn(async move {
            // Collect connection numbers from DashMap
            let conn_keys = Self::extract_connection_ids(&conns_clone);
            for conn_no in conn_keys {
                if conn_no == 0 {
                    continue;
                }

                // Send close frame to remote peer
                let mut close_buffer = buffer_pool_clone.acquire();
                close_buffer.clear();
                close_buffer.extend_from_slice(&conn_no.to_be_bytes());
                close_buffer.put_u8(CloseConnectionReason::Normal as u8);

                let close_frame = Frame::new_control_with_buffer(
                    ControlMessage::CloseConnection,
                    &mut close_buffer,
                );
                let encoded = close_frame.encode_with_pool(&buffer_pool_clone);
                // Silently ignore send errors in Drop - no logging to avoid fd race
                let _ = webrtc.send(encoded).await;
                buffer_pool_clone.release(close_buffer);

                // Send graceful shutdown message before aborting tasks
                if let Some(conn_ref) = conns_clone.get(&conn_no) {
                    if active_protocol == ActiveProtocol::Guacd {
                        debug!(
                            "Channel Drop: Sending Guacamole disconnect instruction (channel_id: {}, conn_no: {})",
                            channel_id, conn_no
                        );
                        let disconnect_instr =
                            GuacdInstruction::new("disconnect".to_string(), vec![]);
                        let disconnect_bytes =
                            GuacdParser::guacd_encode_instruction(&disconnect_instr);
                        let _ = conn_ref
                            .data_tx
                            .send(crate::models::ConnectionMessage::Data(disconnect_bytes));
                        tokio::time::sleep(crate::config::disconnect_to_eof_delay()).await;
                    }
                    debug!(
                        "Channel Drop: Sending EOF for TCP shutdown (channel_id: {}, conn_no: {})",
                        channel_id, conn_no
                    );
                    let _ = conn_ref.data_tx.send(crate::models::ConnectionMessage::Eof);
                }

                // Remove connection from registry with graceful shutdown
                if let Some((_, mut conn)) = conns_clone.remove(&conn_no) {
                    // Gracefully shutdown to ensure TCP cleanup completes (fixes guacd memory leak)
                    conn.graceful_shutdown(conn_no, &channel_id).await;
                    // No logging here - avoid fd race during Python teardown
                }
            }
            // No final log - avoid fd race during Python teardown
        });
    }
}
