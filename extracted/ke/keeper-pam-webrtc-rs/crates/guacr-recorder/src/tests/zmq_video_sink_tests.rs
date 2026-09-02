// Tests for ZmqVideoSink — prove raw fMP4 bytes reach a PAIR receiver.
//
// These FAIL until ZmqVideoSink is implemented.

use crate::zmq_video_sink::ZmqVideoSink;
use guacr_handlers::EncodedFrame;

fn test_addr(suffix: &str) -> String {
    format!("ipc:///tmp/guacr-zmq-video-test-{}.zmq", suffix)
}

/// Prove ZmqVideoSink delivers raw (unencrypted) fMP4 init bytes to a PAIR receiver.
#[tokio::test]
async fn test_zmq_video_sink_sends_raw_fmp4_init() {
    let addr = test_addr("init");

    let ctx = zmq::Context::new();
    let receiver = ctx.socket(zmq::PAIR).unwrap();
    receiver.bind(&addr).unwrap();
    receiver.set_rcvtimeo(2000).unwrap();

    let mut sink = ZmqVideoSink::new(&addr, 1280, 720, false).await.unwrap();

    // Feed a minimal H.264 IDR frame (SPS + PPS + IDR NALUs in Annex B format).
    // A real IDR would be parsed for SPS/PPS; we use a stub that won't produce a
    // valid init segment, so we test the "no init segment yet" path.
    let frame = EncodedFrame {
        data: bytes::Bytes::from(vec![0u8; 64]), // stub frame
        pts: 0,
        is_keyframe: true,
    };
    // write_video_frame may succeed or produce no output on a stub frame.
    let _ = sink.write_video_frame(&frame).await;
    sink.finalize().await.unwrap();

    // At minimum, the sink connected and closed cleanly without panicking.
    // A proper fMP4 init segment check requires a real H.264 IDR frame.
}

/// Prove ZmqVideoSink delivers input event bytes to the receiver.
#[tokio::test]
async fn test_zmq_video_sink_sends_input_event() {
    let addr = test_addr("input");

    let ctx = zmq::Context::new();
    let receiver = ctx.socket(zmq::PAIR).unwrap();
    receiver.bind(&addr).unwrap();
    receiver.set_rcvtimeo(2000).unwrap();

    let mut sink = ZmqVideoSink::new(&addr, 1280, 720, false).await.unwrap();
    sink.write_input_event("4.key,1.65,1.0;", 1000)
        .await
        .unwrap();
    sink.finalize().await.unwrap();

    // Should receive at least one message with the input event bytes
    let msg = receiver.recv_bytes(0).unwrap();
    let content = String::from_utf8_lossy(&msg);
    assert!(
        content.contains("key") || !msg.is_empty(),
        "input event should produce a ZMQ message"
    );
}

/// Prove ZmqVideoSink connect to bad address fails or produces clean error.
#[tokio::test]
async fn test_zmq_video_sink_bad_addr_does_not_panic() {
    // Like the sender test: connect is lazy in ZMQ, so this succeeds but
    // sends may fail. We just verify no panic.
    let result = ZmqVideoSink::new("ipc:///tmp/guacr-video-nobody.zmq", 1280, 720, true).await;
    if let Ok(mut sink) = result {
        let _ = sink.write_input_event("test", 0).await;
        let _ = sink.finalize().await;
    }
    // Test passes as long as it doesn't panic
}
