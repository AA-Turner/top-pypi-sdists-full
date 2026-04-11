use crate::binary::{BinaryEncoder, Opcode};
use bytes::Bytes;

#[test]
fn test_encode_image() {
    let mut encoder = BinaryEncoder::new();
    let data = Bytes::from(vec![1, 2, 3, 4]);

    let msg = encoder.encode_image(10, 20, 100, 200, 1, data.clone());

    // Header: 8 bytes + ImageHeader: 12 bytes + data: 4 bytes = 24 bytes
    assert_eq!(msg.len(), 24);
    assert_eq!(msg[0], Opcode::Image as u8);
    assert_eq!(msg[0], 0x10);
}

#[test]
fn test_encode_image_delta() {
    let mut encoder = BinaryEncoder::new();
    let data = Bytes::from(vec![1, 2, 3, 4]);

    let msg = encoder.encode_image_delta(5, 10, 50, 100, 2, data.clone());

    assert_eq!(msg.len(), 24);
    assert_eq!(msg[0], Opcode::ImageDelta as u8);
    assert_eq!(msg[0], 0x11);
}

#[test]
fn test_encode_size() {
    let mut encoder = BinaryEncoder::new();
    let msg = encoder.encode_size(1920, 1080);

    // Header: 8 bytes + payload: 8 bytes = 16 bytes
    assert_eq!(msg.len(), 16);
    assert_eq!(msg[0], Opcode::Size as u8);
    assert_eq!(msg[0], 0x04);
}

#[test]
fn test_encode_ping_pong() {
    let mut encoder = BinaryEncoder::new();

    let ping = encoder.encode_ping();
    assert_eq!(ping.len(), 8);
    assert_eq!(ping[0], 0xF0);

    let pong = encoder.encode_pong();
    assert_eq!(pong.len(), 8);
    assert_eq!(pong[0], 0xF1);
}
