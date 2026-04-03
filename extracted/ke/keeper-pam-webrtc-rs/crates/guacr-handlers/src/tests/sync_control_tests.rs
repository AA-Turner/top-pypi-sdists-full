use crate::sync_control::SyncFlowControl;

#[test]
fn test_parse_sync_timestamp() {
    let control = SyncFlowControl::new();

    let result = control.parse_sync_timestamp("4.sync,13.1234567890123;");
    assert_eq!(result, Some(1234567890123));

    let result = control.parse_sync_timestamp("4.sync,1.0;");
    assert_eq!(result, Some(0));

    let result = control.parse_sync_timestamp("invalid");
    assert_eq!(result, None);
}

#[test]
fn test_pending_sync() {
    let mut control = SyncFlowControl::new();
    assert!(!control.is_waiting_for_sync());

    control.set_pending_sync(12345);
    assert!(control.is_waiting_for_sync());
    assert_eq!(control.pending_timestamp(), Some(12345));

    control.clear_pending();
    assert!(!control.is_waiting_for_sync());
}

#[test]
fn test_timeout_count() {
    let mut control = SyncFlowControl::new();
    assert_eq!(control.timeout_count(), 0);

    control.sync_timeout_count = 2;
    assert_eq!(control.timeout_count(), 2);

    control.reset_timeout_count();
    assert_eq!(control.timeout_count(), 0);
}
