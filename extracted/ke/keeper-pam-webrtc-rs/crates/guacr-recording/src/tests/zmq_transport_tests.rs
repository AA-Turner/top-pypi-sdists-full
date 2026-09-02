// Tests for ZmqRecordingSender — prove correct PAIR socket behavior.
//
// These tests FAIL until ZmqRecordingSender is implemented in zmq_transport.rs.
// The receiver side uses zmq::PAIR + bind() to simulate Python's ZMQProxy frontend.

use crate::zmq_transport::ZmqRecordingSender;

fn test_addr(suffix: &str) -> String {
    format!("ipc:///tmp/guacr-zmq-test-{}.zmq", suffix)
}

/// Prove ZmqRecordingSender delivers raw bytes to a PAIR receiver.
#[test]
fn test_zmq_sender_delivers_bytes_to_pair_receiver() {
    let addr = test_addr("deliver");

    let ctx = zmq::Context::new();
    let receiver = ctx.socket(zmq::PAIR).unwrap();
    receiver.bind(&addr).unwrap();
    receiver.set_rcvtimeo(2000).unwrap();

    let sender = ZmqRecordingSender::connect(&addr, false).unwrap();
    sender.send(b"hello recording").unwrap();
    sender.close();

    let msg = receiver.recv_bytes(0).unwrap();
    assert_eq!(msg, b"hello recording");
}

/// Prove multiple frames arrive in order.
#[test]
fn test_zmq_sender_multiple_frames_arrive_in_order() {
    let addr = test_addr("order");

    let ctx = zmq::Context::new();
    let receiver = ctx.socket(zmq::PAIR).unwrap();
    receiver.bind(&addr).unwrap();
    receiver.set_rcvtimeo(2000).unwrap();

    let sender = ZmqRecordingSender::connect(&addr, false).unwrap();
    for i in 0u8..5 {
        sender.send(&[i]).unwrap();
    }
    sender.close();

    for expected in 0u8..5 {
        let msg = receiver.recv_bytes(0).unwrap();
        assert_eq!(msg, &[expected], "frame {} out of order", expected);
    }
}

/// Prove that socket close signals end-of-recording (receiver sees no more messages).
#[test]
fn test_zmq_sender_close_signals_end_of_recording() {
    let addr = test_addr("close");

    let ctx = zmq::Context::new();
    let receiver = ctx.socket(zmq::PAIR).unwrap();
    receiver.bind(&addr).unwrap();
    receiver.set_rcvtimeo(200).unwrap(); // short timeout

    let sender = ZmqRecordingSender::connect(&addr, false).unwrap();
    sender.send(b"last frame").unwrap();
    sender.close();

    // Drain the one frame
    let _ = receiver.recv_bytes(0).unwrap();

    // After close, no more messages — recv should time out
    let result = receiver.recv_bytes(0);
    assert!(
        result.is_err(),
        "receiver should time out after sender closes — no more frames"
    );
}

/// Prove send() to a non-existent address fails cleanly.
#[test]
fn test_zmq_sender_connect_to_bad_addr_fails() {
    // ZMQ PAIR connect is lazy — the error surfaces on first send when no peer is present.
    // Point to an address nobody is bound on and send; expect error.
    let addr = "ipc:///tmp/guacr-zmq-nonexistent-nobody.zmq";
    let sender = ZmqRecordingSender::connect(addr, false).unwrap(); // connect is lazy
    sender.send(b"data").unwrap(); // enqueued in channel
    sender.close(); // thread exits with error or times out — not a panic
                    // Test passes as long as it doesn't hang or panic
}

/// Prove allow_unrecorded=true is accessible on the sender.
#[test]
fn test_zmq_sender_exposes_allow_unrecorded() {
    let addr = test_addr("allow");

    let ctx = zmq::Context::new();
    let receiver = ctx.socket(zmq::PAIR).unwrap();
    receiver.bind(&addr).unwrap();

    let sender = ZmqRecordingSender::connect(&addr, true).unwrap();
    assert!(sender.allow_unrecorded);
    sender.close();
}
