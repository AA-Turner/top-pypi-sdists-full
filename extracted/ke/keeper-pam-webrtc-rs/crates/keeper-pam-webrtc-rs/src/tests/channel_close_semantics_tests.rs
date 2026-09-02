//! Tests for channel close semantics: which closes are terminal (tube dies) vs retryable
//! (tube survives for ICE restart).
//!
//! These tests prove the fix for the following bug:
//!
//! When a backend TCP connection sends EOF (e.g. guacd crashes, keeperdb proxy disconnects),
//! the Rust side was unconditionally calling `send_connection_close_callback()`, which tells
//! Python to call `close_tube()`. The tube was destroyed even for retryable closures, making
//! ICE restart impossible.
//!
//! The fix: for tunnel/proxy protocols (PortForward, Socks5, DatabaseProxy, PythonHandler)
//! with a retryable close reason and no explicit conn_no=0 close, skip the callback and leave
//! the tube alive.
//!
//! Also documents the TURN CreatePermission failure scenario: when ICE itself fails (no
//! close_reason set), `is_terminal_channel_close` returns true — so a real TURN failure
//! still kills the tube. That failure mode requires a separate fix at the ICE/TURN layer.

use crate::channel::types::ActiveProtocol;
use crate::tube::is_terminal_channel_close;
use crate::tube_protocol::CloseConnectionReason;

// ---------------------------------------------------------------------------
// PortForward
// ---------------------------------------------------------------------------

#[test]
fn test_portforward_connection_lost_is_not_terminal() {
    // Backend TCP connection sent EOF — tube should survive for ICE restart.
    assert!(!is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

#[test]
fn test_portforward_timeout_is_not_terminal() {
    assert!(!is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        Some(CloseConnectionReason::Timeout)
    ));
}

#[test]
fn test_portforward_connection_failed_is_not_terminal() {
    assert!(!is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        Some(CloseConnectionReason::ConnectionFailed)
    ));
}

#[test]
fn test_portforward_server_refuse_is_not_terminal() {
    assert!(!is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        Some(CloseConnectionReason::ServerRefuse)
    ));
}

#[test]
fn test_portforward_control_closed_is_always_terminal() {
    // Client sent CloseConnection(conn_no=0) — always closes the tube regardless of reason.
    assert!(is_terminal_channel_close(
        ActiveProtocol::PortForward,
        true,
        Some(CloseConnectionReason::ConnectionLost)
    ));
    assert!(is_terminal_channel_close(
        ActiveProtocol::PortForward,
        true,
        Some(CloseConnectionReason::Normal)
    ));
    assert!(is_terminal_channel_close(
        ActiveProtocol::PortForward,
        true,
        None
    ));
}

#[test]
fn test_portforward_protocol_error_is_terminal() {
    // Non-retryable (critical) error — tube should close even for tunnel protocols.
    assert!(is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        Some(CloseConnectionReason::ProtocolError)
    ));
}

#[test]
fn test_portforward_proxy_error_is_terminal() {
    assert!(is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        Some(CloseConnectionReason::ProxyError)
    ));
}

#[test]
fn test_portforward_no_reason_is_terminal() {
    // Unknown/missing close reason — conservative: assume terminal.
    // This is the TURN ICE failure case: WebRTC drops without setting a close_reason.
    // See note at bottom of file about the TURN CreatePermission 400 scenario.
    assert!(is_terminal_channel_close(
        ActiveProtocol::PortForward,
        false,
        None
    ));
}

// ---------------------------------------------------------------------------
// Socks5
// ---------------------------------------------------------------------------

#[test]
fn test_socks5_connection_lost_is_not_terminal() {
    assert!(!is_terminal_channel_close(
        ActiveProtocol::Socks5,
        false,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

#[test]
fn test_socks5_control_closed_is_terminal() {
    assert!(is_terminal_channel_close(
        ActiveProtocol::Socks5,
        true,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

// ---------------------------------------------------------------------------
// DatabaseProxy
// ---------------------------------------------------------------------------

#[test]
fn test_databaseproxy_connection_lost_is_not_terminal() {
    // keeperdb-proxy TCP connection EOF — tube should survive.
    assert!(!is_terminal_channel_close(
        ActiveProtocol::DatabaseProxy,
        false,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

#[test]
fn test_databaseproxy_proxy_error_is_terminal() {
    // Handshake timeout (ProxyError) — non-retryable, tube must close.
    // This matches the "DatabaseProxy handshake timed out" error seen in logs.
    assert!(is_terminal_channel_close(
        ActiveProtocol::DatabaseProxy,
        false,
        Some(CloseConnectionReason::ProxyError)
    ));
}

#[test]
fn test_databaseproxy_control_closed_is_terminal() {
    assert!(is_terminal_channel_close(
        ActiveProtocol::DatabaseProxy,
        true,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

// ---------------------------------------------------------------------------
// PythonHandler
// ---------------------------------------------------------------------------

#[test]
fn test_pythonhandler_connection_lost_is_not_terminal() {
    assert!(!is_terminal_channel_close(
        ActiveProtocol::PythonHandler,
        false,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

#[test]
fn test_pythonhandler_control_closed_is_terminal() {
    assert!(is_terminal_channel_close(
        ActiveProtocol::PythonHandler,
        true,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

// ---------------------------------------------------------------------------
// Guacd — EOF always terminal regardless of reason or control_connection_closed
// ---------------------------------------------------------------------------

#[test]
fn test_guacd_connection_lost_is_terminal() {
    // Guacd EOF means the guacamole session is genuinely over. Even if ICE restart
    // brings a new channel, guacd won't re-establish the session on its own.
    assert!(is_terminal_channel_close(
        ActiveProtocol::Guacd,
        false,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

#[test]
fn test_guacd_normal_close_is_terminal() {
    assert!(is_terminal_channel_close(
        ActiveProtocol::Guacd,
        false,
        Some(CloseConnectionReason::Normal)
    ));
}

#[test]
fn test_guacd_no_reason_is_terminal() {
    assert!(is_terminal_channel_close(
        ActiveProtocol::Guacd,
        false,
        None
    ));
}

// ---------------------------------------------------------------------------
// TURN CreatePermission 400 scenario — FIXED
//
// When TURN fails with "fail to refresh permissions: CreatePermission error response
// (error 400: Bad Request)", the ICE transport drops → PeerConnectionState::Disconnected
// fires in webrtc_core.rs.
//
// With trickle_ice=true, the Disconnected handler now calls
// `tube.mark_channels_ice_disconnected()` BEFORE the wait + ICE restart. This stamps
// all active channels with close_reason=ConnectionLost (retryable). When the data
// channel subsequently closes, is_terminal_channel_close sees ConnectionLost and returns
// false → tube survives → ICE restart attaches a new channel.
//
// Guacd is still terminal even with ICE disconnect marking, because even if ICE restarts
// and a new data channel opens, guacd won't re-establish the session automatically.
//
// trickle_ice=false: Disconnected handler does NOT call mark_channels_ice_disconnected
// (it just logs a warning and waits for Failed). So close_reason stays None → terminal.
// That's correct: without trickle ICE, ICE restart isn't possible anyway.
// ---------------------------------------------------------------------------

#[test]
fn test_turn_ice_failure_after_mark_is_not_terminal_for_tunnel_protocols() {
    // After mark_channels_ice_disconnected() runs, close_reason = ConnectionLost.
    // ConnectionLost is retryable so the tube survives for ICE restart.
    for protocol in [
        ActiveProtocol::PortForward,
        ActiveProtocol::Socks5,
        ActiveProtocol::DatabaseProxy,
        ActiveProtocol::PythonHandler,
    ] {
        assert!(
            !is_terminal_channel_close(
                protocol,
                false,
                Some(CloseConnectionReason::ConnectionLost)
            ),
            "{:?} with ConnectionLost should NOT be terminal",
            protocol
        );
    }
}

#[test]
fn test_connection_lost_is_retryable_not_critical() {
    // ConnectionLost is the reason stamped by mark_channels_ice_disconnected.
    // Retryable → tube survives. Not critical → a subsequent real error can still
    // overwrite it (e.g. if the backend also sends a hard error before ICE restart).
    assert!(CloseConnectionReason::ConnectionLost.is_retryable());
    assert!(!CloseConnectionReason::ConnectionLost.is_critical());
}

#[test]
fn test_turn_ice_failure_guacd_still_terminal_after_mark() {
    // Guacd stays terminal even after marking: ICE restart creates a new channel but
    // guacd won't re-establish the remote session on its own.
    assert!(is_terminal_channel_close(
        ActiveProtocol::Guacd,
        false,
        Some(CloseConnectionReason::ConnectionLost)
    ));
}

#[test]
fn test_turn_ice_failure_no_mark_still_terminal() {
    // If mark_channels_ice_disconnected() did NOT run (trickle_ice=false, or channel
    // closed before Disconnected fired), close_reason is None → still terminal.
    for protocol in [
        ActiveProtocol::PortForward,
        ActiveProtocol::Socks5,
        ActiveProtocol::DatabaseProxy,
        ActiveProtocol::PythonHandler,
        ActiveProtocol::Guacd,
    ] {
        assert!(
            is_terminal_channel_close(protocol, false, None),
            "{:?} with no close_reason (mark did not run) should still be terminal",
            protocol
        );
    }
}
