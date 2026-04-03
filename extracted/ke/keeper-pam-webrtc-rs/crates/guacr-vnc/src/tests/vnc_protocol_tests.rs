use crate::vnc_protocol::{VncPixelFormat, VncProtocol, VncVersion};

#[test]
fn test_vnc_version() {
    let v38 = VncVersion::V38;
    assert_eq!(
        VncVersion::from_bytes(v38.as_bytes()),
        Some(VncVersion::V38)
    );
}

#[test]
fn test_pixel_format_default() {
    let pf = VncPixelFormat::default();
    assert_eq!(pf.bits_per_pixel, 32);
    assert_eq!(pf.depth, 24);
    assert!(pf.true_color);
}

// --- encrypt_vnc_password tests ---

#[test]
fn test_encrypt_vnc_password_returns_16_bytes() {
    let challenge = [0u8; 16];
    let response = VncProtocol::encrypt_vnc_password(&challenge, "password");
    assert_eq!(response.len(), 16, "response must always be 16 bytes");
}

#[test]
fn test_encrypt_vnc_password_deterministic() {
    let challenge = [1u8, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
    let r1 = VncProtocol::encrypt_vnc_password(&challenge, "password");
    let r2 = VncProtocol::encrypt_vnc_password(&challenge, "password");
    assert_eq!(r1, r2, "same inputs must always produce the same output");
}

#[test]
fn test_encrypt_vnc_password_different_passwords_differ() {
    let challenge = [0xABu8; 16];
    let r1 = VncProtocol::encrypt_vnc_password(&challenge, "password");
    let r2 = VncProtocol::encrypt_vnc_password(&challenge, "hunter2");
    assert_ne!(
        r1, r2,
        "different passwords must produce different responses"
    );
}

#[test]
fn test_encrypt_vnc_password_different_challenges_differ() {
    let challenge_a = [0u8; 16];
    let challenge_b = [1u8; 16];
    let r1 = VncProtocol::encrypt_vnc_password(&challenge_a, "secret");
    let r2 = VncProtocol::encrypt_vnc_password(&challenge_b, "secret");
    assert_ne!(
        r1, r2,
        "different challenges must produce different responses with the same password"
    );
}

#[test]
fn test_encrypt_vnc_password_empty_password_all_zero_challenge() {
    // With an empty password the key is still deterministic.
    let challenge = [0u8; 16];
    let response = VncProtocol::encrypt_vnc_password(&challenge, "");
    // Must be 16 bytes and reproducible.
    assert_eq!(response.len(), 16);
    let response2 = VncProtocol::encrypt_vnc_password(&challenge, "");
    assert_eq!(response, response2);
}

// --- parse_tight_length tests ---

#[test]
fn test_tight_length_single_byte_small() {
    // 0x05 has bit 7 clear -> value 5, consumed 1 byte.
    assert_eq!(VncProtocol::parse_tight_length(&[0x05]), Some((5, 1)));
}

#[test]
fn test_tight_length_single_byte_max() {
    // 0x7F has bit 7 clear -> value 127, consumed 1 byte.
    assert_eq!(VncProtocol::parse_tight_length(&[0x7F]), Some((127, 1)));
}

#[test]
fn test_tight_length_two_bytes_minimal() {
    // b0 = 0x80 -> continuation, low 7 bits = 0.
    // b1 = 0x01 -> no continuation, contributes bits 7-13, value = 1 << 7 = 128.
    assert_eq!(
        VncProtocol::parse_tight_length(&[0x80, 0x01]),
        Some((128, 2))
    );
}

#[test]
fn test_tight_length_two_bytes_larger() {
    // b0 = 0xFF -> continuation, low 7 bits = 0x7F = 127.
    // b1 = 0x7F -> no continuation, contributes 127 << 7 = 16256.
    // total = 127 + 16256 = 16383.
    let expected = 0x7F | (0x7Fusize << 7); // 127 | 16256 = 16383
    assert_eq!(
        VncProtocol::parse_tight_length(&[0xFF, 0x7F]),
        Some((expected, 2))
    );
}

#[test]
fn test_tight_length_three_bytes() {
    // b0 = 0x80 (continuation, low7=0), b1 = 0x80 (continuation, low7=0), b2 = 0x01.
    // value = 0 | (0 << 7) | (1 << 14) = 16384.
    assert_eq!(
        VncProtocol::parse_tight_length(&[0x80, 0x80, 0x01]),
        Some((16384, 3))
    );
}

#[test]
fn test_tight_length_empty_input() {
    assert_eq!(VncProtocol::parse_tight_length(&[]), None);
}

#[test]
fn test_tight_length_truncated_two_byte() {
    // First byte has continuation bit set but there is no second byte.
    assert_eq!(VncProtocol::parse_tight_length(&[0x80]), None);
}

#[test]
fn test_tight_length_truncated_three_byte() {
    // First two bytes both have continuation bit; no third byte.
    assert_eq!(VncProtocol::parse_tight_length(&[0x80, 0x80]), None);
}
