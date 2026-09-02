mod logger;
pub mod resource_manager;
pub mod webrtc_core;

#[cfg(test)]
mod tests;

mod buffer_pool;
mod channel;
mod config;
mod error;
#[cfg(feature = "builtin-handlers")]
mod handler_integration;
pub mod hot_path_macros;
mod metrics;
mod models;
#[cfg(feature = "python-support")]
pub mod python;
mod router_helpers;
// Additive widening for external gateway implementations (e.g.
// `pam-gateway-rust`): they need to seed the InstanceId before any
// `relay_access_creds` / `request_turn_credentials` call, else krouter
// rejects with 401 and ICE pairing never gets relay candidates. Python
// bindings already exposed these methods on the `RegistryHandle`
// (`python/tube_registry_binding.rs:744,2309`); these re-exports give
// non-Python gateways the same hooks without widening the whole
// `router_helpers` module.
//
// `post_connection_state` is the wire-level call used by Python's
// `tunnel_helpers.refresh_connections_on_router`. After WS-connect a
// gateway must POST `connection_state="open_connections"` with an
// (initially empty) token array; that handshake is what associates
// the WS-registered InstanceId with subsequent HTTP requests. Skip
// it and `relay_access_creds` 401s.
pub use router_helpers::{initialize_instance_id, post_connection_state};
pub mod runtime;
mod tube;
mod tube_and_channel_helpers;
pub mod tube_protocol;
pub mod tube_registry;
pub mod video_sender;
mod webrtc_circuit_breaker;
mod webrtc_data_channel;
pub mod webrtc_data_tap;
mod webrtc_errors;
mod webrtc_network_monitor;
pub use tube::*;
pub use video_sender::VideoSender;
pub use webrtc_core::*;
pub use webrtc_errors::*;
pub use webrtc_network_monitor::{ConnectionMigrator, NetworkMonitor};

#[cfg(feature = "builtin-handlers")]
pub use handler_integration::{create_handler_registry, invoke_handler};

pub use logger::{initialize_logger, set_verbose_logging};
