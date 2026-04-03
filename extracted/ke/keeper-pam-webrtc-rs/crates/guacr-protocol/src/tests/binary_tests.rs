use crate::binary::{BinaryEncoder, Opcode};
use bytes::Bytes;

#[test]
fn test_encode_image() {
    let mut encoder = BinaryEncoder::new();
    let data = Bytes::from(vec![1, 2, 3, 4]);

    let msg = encoder.encode_image(1, 0, 10, 20, 100, 200, 1, data.clone());

    // Header: 8 bytes + payload: 22 bytes (includes padding) + data: 4 bytes = 34 bytes
    assert_eq!(msg.len(), 34);

    // Check opcode
    assert_eq!(msg[0], Opcode::Image as u8);
}

#[test]
fn test_encode_sync() {
    let mut encoder = BinaryEncoder::new();
    let msg = encoder.encode_sync(1234567890);

    // Header: 8 bytes + timestamp: 8 bytes = 16 bytes
    assert_eq!(msg.len(), 16);
    assert_eq!(msg[0], Opcode::Sync as u8);
}
