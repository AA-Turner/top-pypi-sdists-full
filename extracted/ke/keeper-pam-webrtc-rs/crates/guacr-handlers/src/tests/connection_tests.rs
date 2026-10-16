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

/// A keepalive must fire on every interval deadline, not every other one.
///
/// Every call site drives `check()` from a `tokio::time::interval` of the same period, so
/// the deadlines are at t=5, t=10, t=15 — but a tick is always observed a little *after* its
/// deadline. If the schedule restarts from the moment of sending rather than from the
/// deadline, the next tick is a fraction of a millisecond too early, `check()` rejects it,
/// and the effective keepalive period doubles: 10s instead of the documented 5s. Dead-viewer
/// detection is built on that interval, so the drift is not cosmetic.
#[tokio::test(start_paused = true)]
async fn test_keepalive_manager_fires_on_every_interval_deadline() {
    use std::time::Duration;

    let mut manager = KeepAliveManager::new(5);

    // The first tick, observed 1ms after its deadline.
    tokio::time::advance(Duration::from_secs(5) + Duration::from_millis(1)).await;
    assert!(
        manager.check().is_some(),
        "a keepalive is due at the first interval deadline"
    );

    // The second deadline is at t=10, which is only 4999ms after that send.
    tokio::time::advance(Duration::from_millis(4999)).await;
    assert!(
        manager.check().is_some(),
        "the second deadline must produce a keepalive — rejecting it halves the keepalive rate"
    );

    // And the third, to show the schedule does not accumulate the correction.
    tokio::time::advance(Duration::from_secs(5)).await;
    assert!(
        manager.check().is_some(),
        "the third deadline must produce a keepalive"
    );
}

/// A long stall must not produce a burst of catch-up keepalives.
///
/// Every call site sets `MissedTickBehavior::Skip` on its interval, so missed deadlines are
/// dropped rather than replayed. The manager has to agree: a session that was blocked for a
/// minute owes the client one ping, not twelve.
#[tokio::test(start_paused = true)]
async fn test_keepalive_manager_skips_missed_deadlines() {
    use std::time::Duration;

    let mut manager = KeepAliveManager::new(5);

    tokio::time::advance(Duration::from_secs(60)).await;
    assert!(manager.check().is_some(), "the overdue keepalive is sent");
    assert!(
        manager.check().is_none(),
        "missed deadlines are skipped, not replayed as a burst"
    );

    tokio::time::advance(Duration::from_secs(5)).await;
    assert!(
        manager.check().is_some(),
        "the schedule resumes from the catch-up point"
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
