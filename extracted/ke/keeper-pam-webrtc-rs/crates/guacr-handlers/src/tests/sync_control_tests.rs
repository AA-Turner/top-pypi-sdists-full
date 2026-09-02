use crate::sync_control::{SyncFlowControl, TerminalOutputBuffer};

/// Terminal output is a byte stream; the buffer must never drop bytes and must
/// hand them back in order, chunked to the frame cap. This is the contract the
/// old inline SSH flow control violated (it truncated beyond 16 KB and dropped
/// everything while waiting for a sync ACK), which corrupted the client terminal.
#[test]
fn output_buffer_is_lossless_and_chunked() {
    let mut b = TerminalOutputBuffer::new();
    let data: Vec<u8> = (0..100_000u32).map(|i| (i % 251) as u8).collect();

    // Push in irregular chunks (mimics bursty SSH output).
    let mut i = 0;
    while i < data.len() {
        let n = (data.len() - i).min(1000 + (i % 777));
        b.push(&data[i..i + n]);
        i += n;
    }

    // Drain in 16 KB frames.
    let mut out = Vec::new();
    while let Some(f) = b.take_frame(16 * 1024) {
        assert!(f.len() <= 16 * 1024, "frame must respect the cap");
        out.extend_from_slice(&f);
    }
    assert_eq!(out, data, "every byte preserved, in order — no drops");
    assert!(b.is_empty());
}

#[test]
fn output_buffer_requeue_preserves_order() {
    let mut b = TerminalOutputBuffer::new();
    b.push(b"HELLOWORLD");
    let f = b.take_frame(5).unwrap();
    assert_eq!(&f, b"HELLO");
    // Send queue was full — put it back; order must be restored.
    b.requeue_front(f);
    let all = b.take_frame(100).unwrap();
    assert_eq!(&all, b"HELLOWORLD");
    assert!(b.take_frame(10).is_none());
}

#[test]
fn output_buffer_empty_take_is_none() {
    let mut b = TerminalOutputBuffer::new();
    assert!(b.take_frame(10).is_none());
    assert!(b.is_empty());
    assert_eq!(b.len(), 0);
}

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
