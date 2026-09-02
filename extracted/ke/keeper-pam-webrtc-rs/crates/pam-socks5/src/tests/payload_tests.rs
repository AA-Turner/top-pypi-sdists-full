use crate::payload::{
    decode_open_connection_payload, encode_open_connection_payload, Socks5Target,
};
use bytes::{BufMut, BytesMut};

#[test]
fn test_encode_decode_roundtrip() {
    let target = Socks5Target {
        host: "example.com".to_string(),
        port: 80,
    };
    let encoded = encode_open_connection_payload(42, &target);

    // Skip conn_no (first 4 bytes) - caller handles that
    let decoded = decode_open_connection_payload(&encoded[4..]).unwrap();
    assert_eq!(decoded, target);
}

#[test]
fn test_encode_format() {
    let target = Socks5Target {
        host: "example.com".to_string(),
        port: 80,
    };
    let encoded = encode_open_connection_payload(42, &target);

    // Verify layout
    assert_eq!(
        encoded.len(),
        4 + 4 + "example.com".len() + 2 // conn_no + host_len + host + port
    );

    use bytes::Buf;
    let mut cursor = std::io::Cursor::new(&encoded[..]);
    assert_eq!(cursor.get_u32(), 42); // conn_no
    assert_eq!(cursor.get_u32(), 11); // host_len
    let mut host = vec![0u8; 11];
    cursor.copy_to_slice(&mut host);
    assert_eq!(String::from_utf8(host).unwrap(), "example.com");
    assert_eq!(cursor.get_u16(), 80); // port
}

#[test]
fn test_decode_empty_host() {
    let target = Socks5Target {
        host: String::new(),
        port: 80,
    };
    let encoded = encode_open_connection_payload(1, &target);
    let decoded = decode_open_connection_payload(&encoded[4..]).unwrap();
    assert_eq!(decoded.host, "");
    assert_eq!(decoded.port, 80);
}

#[test]
fn test_decode_long_host() {
    let target = Socks5Target {
        host: "a".repeat(255),
        port: 443,
    };
    let encoded = encode_open_connection_payload(2, &target);
    let decoded = decode_open_connection_payload(&encoded[4..]).unwrap();
    assert_eq!(decoded, target);
}

#[test]
fn test_decode_max_port() {
    let target = Socks5Target {
        host: "localhost".to_string(),
        port: 65535,
    };
    let encoded = encode_open_connection_payload(3, &target);
    let decoded = decode_open_connection_payload(&encoded[4..]).unwrap();
    assert_eq!(decoded.port, 65535);
}

#[test]
fn test_decode_zero_port() {
    let target = Socks5Target {
        host: "localhost".to_string(),
        port: 0,
    };
    let encoded = encode_open_connection_payload(3, &target);
    let decoded = decode_open_connection_payload(&encoded[4..]).unwrap();
    assert_eq!(decoded.port, 0);
}

#[test]
fn test_decode_too_short_for_host_len() {
    let data = [0u8; 2]; // Only 2 bytes, need 4 for host_len
    assert!(decode_open_connection_payload(&data).is_err());
}

#[test]
fn test_decode_too_short_for_host_data() {
    let mut data = BytesMut::new();
    data.put_u32(10); // host_len = 10
    data.extend_from_slice(b"short"); // Only 5 bytes + no port
    assert!(decode_open_connection_payload(&data).is_err());
}

#[test]
fn test_decode_missing_port() {
    let mut data = BytesMut::new();
    data.put_u32(5);
    data.extend_from_slice(b"hello"); // Exact host but no port bytes
    assert!(decode_open_connection_payload(&data).is_err());
}
