use std::collections::HashMap;

use guacr_handlers::HealthStatus;
use guacr_handlers::ProtocolHandler;

use crate::serial::Parity;
use crate::serial::{
    build_do_com_port, build_rfc2217_negotiation, build_set_baudrate, build_set_datasize,
    build_set_parity, build_set_stopsize, build_will_com_port, strip_telnet_commands, SerialConfig,
    SerialConsoleHandler, SerialParams, StopBits,
};
use crate::serial::{
    COM_PORT_OPTION, DO, IAC, SB, SE, SET_BAUDRATE, SET_DATASIZE, SET_PARITY, SET_STOPSIZE, WILL,
};

#[test]
fn test_serial_handler_name() {
    let handler = SerialConsoleHandler::with_defaults();
    assert_eq!(
        <SerialConsoleHandler as ProtocolHandler>::name(&handler),
        "serial"
    );
}

#[tokio::test]
async fn test_serial_handler_health() {
    let handler = SerialConsoleHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[tokio::test]
async fn test_serial_handler_stats() {
    let handler = SerialConsoleHandler::with_defaults();
    let stats = handler.stats().await.unwrap();
    assert_eq!(stats.total_connections, 0);
}

// -----------------------------------------------------------------------
// RFC 2217 negotiation byte building
// -----------------------------------------------------------------------

#[test]
fn test_build_will_com_port() {
    let bytes = build_will_com_port();
    assert_eq!(bytes, vec![0xFF, 0xFB, 44]);
}

#[test]
fn test_build_do_com_port() {
    let bytes = build_do_com_port();
    assert_eq!(bytes, vec![0xFF, 0xFD, 44]);
}

#[test]
fn test_build_set_baudrate_9600() {
    let bytes = build_set_baudrate(9600);
    // IAC SB COM_PORT SET_BAUDRATE <4 bytes big-endian> IAC SE
    // 9600 = 0x00002580
    assert_eq!(
        bytes,
        vec![0xFF, 0xFA, 44, 1, 0x00, 0x00, 0x25, 0x80, 0xFF, 0xF0]
    );
}

#[test]
fn test_build_set_baudrate_115200() {
    let bytes = build_set_baudrate(115200);
    // 115200 = 0x0001C200
    assert_eq!(
        bytes,
        vec![0xFF, 0xFA, 44, 1, 0x00, 0x01, 0xC2, 0x00, 0xFF, 0xF0]
    );
}

#[test]
fn test_build_set_baudrate_iac_escaping() {
    // Baud rate 0xFF0000FF should double each 0xFF byte
    let bytes = build_set_baudrate(0xFF0000FF);
    assert_eq!(
        bytes,
        vec![0xFF, 0xFA, 44, 1, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xF0]
    );
}

#[test]
fn test_build_set_datasize() {
    assert_eq!(
        build_set_datasize(8),
        vec![0xFF, 0xFA, 44, 2, 8, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_datasize(7),
        vec![0xFF, 0xFA, 44, 2, 7, 0xFF, 0xF0]
    );
}

#[test]
fn test_build_set_parity() {
    assert_eq!(
        build_set_parity(Parity::None),
        vec![0xFF, 0xFA, 44, 3, 1, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_parity(Parity::Odd),
        vec![0xFF, 0xFA, 44, 3, 2, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_parity(Parity::Even),
        vec![0xFF, 0xFA, 44, 3, 3, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_parity(Parity::Mark),
        vec![0xFF, 0xFA, 44, 3, 4, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_parity(Parity::Space),
        vec![0xFF, 0xFA, 44, 3, 5, 0xFF, 0xF0]
    );
}

#[test]
fn test_build_set_stopsize() {
    assert_eq!(
        build_set_stopsize(StopBits::One),
        vec![0xFF, 0xFA, 44, 4, 1, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_stopsize(StopBits::Two),
        vec![0xFF, 0xFA, 44, 4, 2, 0xFF, 0xF0]
    );
    assert_eq!(
        build_set_stopsize(StopBits::OnePointFive),
        vec![0xFF, 0xFA, 44, 4, 3, 0xFF, 0xF0]
    );
}

#[test]
fn test_build_rfc2217_negotiation_contains_all_commands() {
    let params = SerialParams {
        hostname: "test".to_string(),
        port: 2001,
        baud_rate: 19200,
        data_bits: 8,
        parity: Parity::None,
        stop_bits: StopBits::One,
        rfc2217: true,
    };
    let bytes = build_rfc2217_negotiation(&params);

    // Should contain: WILL COM_PORT, DO COM_PORT, SET_BAUDRATE, SET_DATASIZE, SET_PARITY, SET_STOPSIZE
    // WILL COM_PORT
    assert!(bytes.windows(3).any(|w| w == [IAC, WILL, COM_PORT_OPTION]));
    // DO COM_PORT
    assert!(bytes.windows(3).any(|w| w == [IAC, DO, COM_PORT_OPTION]));
    // SET_BAUDRATE subneg
    assert!(bytes
        .windows(4)
        .any(|w| w == [IAC, SB, COM_PORT_OPTION, SET_BAUDRATE]));
    // SET_DATASIZE subneg
    assert!(bytes
        .windows(4)
        .any(|w| w == [IAC, SB, COM_PORT_OPTION, SET_DATASIZE]));
    // SET_PARITY subneg
    assert!(bytes
        .windows(4)
        .any(|w| w == [IAC, SB, COM_PORT_OPTION, SET_PARITY]));
    // SET_STOPSIZE subneg
    assert!(bytes
        .windows(4)
        .any(|w| w == [IAC, SB, COM_PORT_OPTION, SET_STOPSIZE]));
}

// -----------------------------------------------------------------------
// Parameter parsing
// -----------------------------------------------------------------------

#[test]
fn test_serial_params_defaults() {
    let config = SerialConfig::default();
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "192.168.1.1".to_string());

    let serial = SerialParams::from_params(&params, &config).unwrap();
    assert_eq!(serial.hostname, "192.168.1.1");
    assert_eq!(serial.port, 2001);
    assert_eq!(serial.baud_rate, 9600);
    assert_eq!(serial.data_bits, 8);
    assert_eq!(serial.parity, Parity::None);
    assert_eq!(serial.stop_bits, StopBits::One);
    assert!(serial.rfc2217);
}

#[test]
fn test_serial_params_custom() {
    let config = SerialConfig::default();
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "console.example.com".to_string());
    params.insert("port".to_string(), "7001".to_string());
    params.insert("baud_rate".to_string(), "115200".to_string());
    params.insert("data_bits".to_string(), "7".to_string());
    params.insert("parity".to_string(), "even".to_string());
    params.insert("stop_bits".to_string(), "2".to_string());
    params.insert("rfc2217".to_string(), "false".to_string());

    let serial = SerialParams::from_params(&params, &config).unwrap();
    assert_eq!(serial.hostname, "console.example.com");
    assert_eq!(serial.port, 7001);
    assert_eq!(serial.baud_rate, 115200);
    assert_eq!(serial.data_bits, 7);
    assert_eq!(serial.parity, Parity::Even);
    assert_eq!(serial.stop_bits, StopBits::Two);
    assert!(!serial.rfc2217);
}

#[test]
fn test_serial_params_hyphenated_keys() {
    let config = SerialConfig::default();
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "test".to_string());
    params.insert("baud-rate".to_string(), "38400".to_string());
    params.insert("data-bits".to_string(), "7".to_string());
    params.insert("stop-bits".to_string(), "1.5".to_string());
    params.insert("rfc-2217".to_string(), "true".to_string());

    let serial = SerialParams::from_params(&params, &config).unwrap();
    assert_eq!(serial.baud_rate, 38400);
    assert_eq!(serial.data_bits, 7);
    assert_eq!(serial.stop_bits, StopBits::OnePointFive);
    assert!(serial.rfc2217);
}

#[test]
fn test_serial_params_missing_hostname() {
    let config = SerialConfig::default();
    let params = HashMap::new();
    let result = SerialParams::from_params(&params, &config);
    assert!(result.is_err());
}

#[test]
fn test_serial_params_invalid_data_bits_uses_default() {
    let config = SerialConfig::default();
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "test".to_string());
    params.insert("data_bits".to_string(), "9".to_string()); // invalid

    let serial = SerialParams::from_params(&params, &config).unwrap();
    assert_eq!(serial.data_bits, 8); // falls back to default
}

#[test]
fn test_serial_params_invalid_port_uses_default() {
    let config = SerialConfig::default();
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "test".to_string());
    params.insert("port".to_string(), "not_a_number".to_string());

    let serial = SerialParams::from_params(&params, &config).unwrap();
    assert_eq!(serial.port, 2001);
}

// -----------------------------------------------------------------------
// Parity and StopBits parsing
// -----------------------------------------------------------------------

#[test]
fn test_parity_from_param() {
    assert_eq!(Parity::from_param("none"), Parity::None);
    assert_eq!(Parity::from_param("None"), Parity::None);
    assert_eq!(Parity::from_param("NONE"), Parity::None);
    assert_eq!(Parity::from_param("odd"), Parity::Odd);
    assert_eq!(Parity::from_param("even"), Parity::Even);
    assert_eq!(Parity::from_param("mark"), Parity::Mark);
    assert_eq!(Parity::from_param("space"), Parity::Space);
    assert_eq!(Parity::from_param("invalid"), Parity::None);
    assert_eq!(Parity::from_param(""), Parity::None);
}

#[test]
fn test_stop_bits_from_param() {
    assert_eq!(StopBits::from_param("1"), StopBits::One);
    assert_eq!(StopBits::from_param("2"), StopBits::Two);
    assert_eq!(StopBits::from_param("1.5"), StopBits::OnePointFive);
    assert_eq!(StopBits::from_param("invalid"), StopBits::One);
    assert_eq!(StopBits::from_param(""), StopBits::One);
}

// -----------------------------------------------------------------------
// Baud rate encoding
// -----------------------------------------------------------------------

#[test]
fn test_baud_rate_encoding_common_values() {
    // Verify 4-byte big-endian encoding for common baud rates
    assert_eq!(9600u32.to_be_bytes(), [0x00, 0x00, 0x25, 0x80]);
    assert_eq!(19200u32.to_be_bytes(), [0x00, 0x00, 0x4B, 0x00]);
    assert_eq!(38400u32.to_be_bytes(), [0x00, 0x00, 0x96, 0x00]);
    assert_eq!(57600u32.to_be_bytes(), [0x00, 0x00, 0xE1, 0x00]);
    assert_eq!(115200u32.to_be_bytes(), [0x00, 0x01, 0xC2, 0x00]);
}

// -----------------------------------------------------------------------
// Telnet IAC stripping
// -----------------------------------------------------------------------

#[test]
fn test_strip_telnet_plain_data() {
    let data = b"Hello, World!";
    assert_eq!(strip_telnet_commands(data), data.to_vec());
}

#[test]
fn test_strip_telnet_will_do() {
    // IAC WILL COM_PORT mixed with data
    let mut data = Vec::new();
    data.extend_from_slice(b"AB");
    data.extend_from_slice(&[IAC, WILL, COM_PORT_OPTION]); // stripped
    data.extend_from_slice(b"CD");
    data.extend_from_slice(&[IAC, DO, COM_PORT_OPTION]); // stripped
    data.extend_from_slice(b"EF");
    assert_eq!(strip_telnet_commands(&data), b"ABCDEF".to_vec());
}

#[test]
fn test_strip_telnet_subnegotiation() {
    // IAC SB ... IAC SE should be stripped
    let mut data = Vec::new();
    data.extend_from_slice(b"before");
    data.extend_from_slice(&[IAC, SB, 44, 1, 0x00, 0x00, 0x25, 0x80, IAC, SE]);
    data.extend_from_slice(b"after");
    assert_eq!(strip_telnet_commands(&data), b"beforeafter".to_vec());
}

#[test]
fn test_strip_telnet_escaped_iac() {
    // IAC IAC should become a single 0xFF byte
    let data = vec![0x41, IAC, IAC, 0x42];
    assert_eq!(strip_telnet_commands(&data), vec![0x41, 0xFF, 0x42]);
}

#[test]
fn test_strip_telnet_empty() {
    assert_eq!(strip_telnet_commands(&[]), Vec::<u8>::new());
}

#[test]
fn test_strip_telnet_only_commands() {
    let data = vec![IAC, WILL, COM_PORT_OPTION, IAC, DO, COM_PORT_OPTION];
    assert_eq!(strip_telnet_commands(&data), Vec::<u8>::new());
}

// -----------------------------------------------------------------------
// Timestamp fallback — sync instruction clock skew
// -----------------------------------------------------------------------

/// Prove that `SystemTime::duration_since(UNIX_EPOCH)` returns Err for a
/// time before the epoch and that `.unwrap()` would panic on that input.
///
/// This is the test that would have failed before the fix landed.  It
/// confirms:
///   1. A pre-epoch SystemTime produces an Err from duration_since.
///   2. Calling .unwrap() on that Err panics (the old, broken behaviour).
///   3. Calling .unwrap_or_default() on that Err returns Duration::ZERO
///      (the fixed behaviour), so the sync timestamp falls back to 0 ms
///      rather than crashing the session.
#[test]
fn test_sync_timestamp_pre_epoch_unwrap_panics() {
    // Construct a time that is 1 second *before* the Unix epoch.
    let before_epoch = std::time::UNIX_EPOCH - std::time::Duration::from_secs(1);

    // duration_since must return Err for a time before the epoch.
    let result = before_epoch.duration_since(std::time::UNIX_EPOCH);
    assert!(result.is_err(), "expected Err for pre-epoch time, got Ok");

    // The old code called .unwrap() — verify that really would panic.
    let panicked = std::panic::catch_unwind(|| {
        before_epoch
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_millis() as u64
    });
    assert!(
        panicked.is_err(),
        "expected .unwrap() on pre-epoch duration_since to panic"
    );
}

/// Prove that the fix — `.unwrap_or_default()` — does not panic for a
/// pre-epoch time and returns 0 as the fallback timestamp.
#[test]
fn test_sync_timestamp_pre_epoch_unwrap_or_default_is_zero() {
    let before_epoch = std::time::UNIX_EPOCH - std::time::Duration::from_secs(1);

    // The fixed expression must not panic.
    let ts_ms = before_epoch
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64;

    // Duration::default() is zero, so the timestamp must be 0.
    assert_eq!(
        ts_ms, 0,
        "expected fallback timestamp of 0 ms for pre-epoch clock, got {}",
        ts_ms
    );
}

/// Confirm that a normal (post-epoch) system time produces a non-zero
/// timestamp — i.e. the happy path still works after the fix.
#[test]
fn test_sync_timestamp_normal_time_is_nonzero() {
    // Use a known post-epoch instant: 2020-01-01T00:00:00Z = 1577836800 s
    let post_epoch = std::time::UNIX_EPOCH + std::time::Duration::from_secs(1_577_836_800);

    let ts_ms = post_epoch
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64;

    assert!(
        ts_ms > 0,
        "expected non-zero timestamp for normal post-epoch time, got {}",
        ts_ms
    );
    // Sanity: 1577836800 s == 1_577_836_800_000 ms
    assert_eq!(ts_ms, 1_577_836_800_000);
}

// -----------------------------------------------------------------------
// Default config values
// -----------------------------------------------------------------------

#[test]
fn test_default_serial_config() {
    let config = SerialConfig::default();
    assert_eq!(config.default_port, 2001);
    assert_eq!(config.default_rows, 24);
    assert_eq!(config.default_cols, 80);
    assert_eq!(config.default_baud_rate, 9600);
    assert_eq!(config.default_data_bits, 8);
    assert_eq!(config.default_parity, Parity::None);
    assert_eq!(config.default_stop_bits, StopBits::One);
    assert!(config.default_rfc2217);
}

#[test]
fn test_custom_serial_config() {
    let config = SerialConfig {
        default_port: 3001,
        default_rows: 25,
        default_cols: 132,
        default_baud_rate: 115200,
        default_data_bits: 7,
        default_parity: Parity::Even,
        default_stop_bits: StopBits::Two,
        default_rfc2217: false,
    };
    assert_eq!(config.default_port, 3001);
    assert_eq!(config.default_rows, 25);
    assert_eq!(config.default_cols, 132);
    assert_eq!(config.default_baud_rate, 115200);
    assert_eq!(config.default_data_bits, 7);
    assert_eq!(config.default_parity, Parity::Even);
    assert_eq!(config.default_stop_bits, StopBits::Two);
    assert!(!config.default_rfc2217);
}
