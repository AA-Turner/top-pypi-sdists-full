use crate::connection::{
    connect_tcp_with_timeout, ConnectionOptions, KeepAliveManager, DEFAULT_KEEPALIVE_INTERVAL_SECS,
};
use crate::error::HandlerError;

#[test]
fn test_keepalive_manager_disabled() {
    let mut manager = KeepAliveManager::new(0);
    assert!(manager.check().is_none());
}

#[test]
fn test_keepalive_manager_sync_format() {
    let mut manager = KeepAliveManager::new(5);
    let sync = manager.generate_sync();
    let sync_str = String::from_utf8_lossy(&sync);

    // Should start with "4.sync,"
    assert!(
        sync_str.starts_with("4.sync,"),
        "Sync should start with opcode: {}",
        sync_str
    );
    // Should end with ";"
    assert!(sync_str.ends_with(';'), "Sync should end with semicolon");
    // Should contain frame counter (starts at 1)
    assert!(
        sync_str.contains(",1.1;"),
        "Should have frame counter: {}",
        sync_str
    );
}

#[test]
fn test_keepalive_manager_frame_counter() {
    let mut manager = KeepAliveManager::new(1);

    let sync1 = manager.generate_sync();
    let sync2 = manager.generate_sync();
    let sync3 = manager.generate_sync();

    let s1 = String::from_utf8_lossy(&sync1);
    let s2 = String::from_utf8_lossy(&sync2);
    let s3 = String::from_utf8_lossy(&sync3);

    // Frame counters should increment
    assert!(
        s1.contains(",1.1;"),
        "First sync should have frame 1: {}",
        s1
    );
    assert!(
        s2.contains(",1.2;"),
        "Second sync should have frame 2: {}",
        s2
    );
    assert!(
        s3.contains(",1.3;"),
        "Third sync should have frame 3: {}",
        s3
    );
}

#[test]
fn test_connection_options_default() {
    let opts = ConnectionOptions::default();
    assert_eq!(opts.connection_timeout_secs, 15); // Matches keeper-pam-webrtc-rs
    assert_eq!(
        opts.keepalive_interval_secs,
        DEFAULT_KEEPALIVE_INTERVAL_SECS
    );
}

#[tokio::test]
async fn test_connect_tcp_timeout() {
    // Try to connect to localhost on a port that's very unlikely to be in use
    // This should fail quickly with "connection refused" rather than timeout
    let result = connect_tcp_with_timeout("127.0.0.1:59999", 1).await;

    // Should fail (either refused or timeout)
    assert!(result.is_err(), "Connection to unused port should fail");
    let err = result.unwrap_err();
    match err {
        HandlerError::ConnectionFailed(msg) => {
            // Either "timed out", "refused", or other connection failure is fine
            assert!(
                !msg.is_empty(),
                "Error message should not be empty: {}",
                msg
            );
        }
        _ => panic!("Expected ConnectionFailed error, got: {:?}", err),
    }
}

#[tokio::test]
async fn test_connect_tcp_zero_timeout_uses_os_default() {
    // Zero timeout means use OS default
    // This should still fail quickly on localhost with refused
    let result = connect_tcp_with_timeout("127.0.0.1:59998", 0).await;

    // Should fail with connection refused (OS default timeout won't be hit)
    assert!(result.is_err(), "Connection to unused port should fail");
}
