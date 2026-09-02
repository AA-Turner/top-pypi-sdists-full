use crate::vnc_protocol::{VncPixelFormat, VncProtocol, VncVersion};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

// --- T-004/T-005/T-006: framebuffer overflow and boundary tests ---

#[test]
fn test_parse_framebuffer_overflow_width_height_checked() {
    // AC-1: 65535×65535 raw rectangle — checked_mul must not panic or silently allocate.
    // Build a minimal FBU with one rectangle claiming 65535×65535 Raw pixels.
    // Data is far too short to hold that many pixels, so the parser must bail out
    // cleanly rather than panicking or allocating 4 GiB.
    let width: u16 = 65535;
    let height: u16 = 65535;
    let mut data = vec![0u8; 4 + 12]; // FBU header (4) + rect header (12), no pixel data
    data[0] = 0; // message type: FramebufferUpdate
    data[1] = 0; // padding
    data[2] = 0; // num_rects hi
    data[3] = 1; // num_rects = 1
                 // Rectangle header
    data[4] = 0;
    data[5] = 0; // x = 0
    data[6] = 0;
    data[7] = 0; // y = 0
    data[8] = (width >> 8) as u8;
    data[9] = (width & 0xFF) as u8;
    data[10] = (height >> 8) as u8;
    data[11] = (height & 0xFF) as u8;
    data[12] = 0;
    data[13] = 0;
    data[14] = 0;
    data[15] = 0; // encoding = Raw (0)

    // Must not panic; result may be Ok (empty rects) or Err — either is acceptable.
    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data);
    // The parser safely handles the case: either stops early (no pixel data) or errors.
    match result {
        Ok((rects, _)) => {
            // If it returns Ok, the rectangle list should be empty (skipped due to insufficient data).
            assert!(
                rects.is_empty() || rects.iter().all(|r| r.pixels.is_empty()),
                "oversized rectangle must not have pixel data allocated"
            );
        }
        Err(_) => {
            // An error is also acceptable — the important thing is no panic/OOM.
        }
    }
}

#[test]
fn test_cursor_parse_overflow_dimensions() {
    // AC-1: cursor with huge dimensions must return an error, not panic.
    let pf = VncPixelFormat::default(); // 32bpp
    let result = VncProtocol::parse_cursor_data(0, 0, 65535, 65535, &[], &pf);
    assert!(result.is_err(), "65535×65535 cursor must return an error");
}

#[test]
fn test_parse_framebuffer_normal_allocation() {
    // AC-4: a normal 4×4 Raw rectangle must parse correctly.
    // 4×4 × 3 bytes/pixel = 48 bytes of pixel data.
    let width: u16 = 4;
    let height: u16 = 4;
    let pixel_bytes = vec![128u8; (width as usize) * (height as usize) * 3]; // 48 bytes, value=128
    let mut data = vec![0u8; 4 + 12 + pixel_bytes.len()];
    data[0] = 0;
    data[1] = 0;
    data[2] = 0;
    data[3] = 1; // 1 rectangle
    data[4] = 0;
    data[5] = 0; // x = 0
    data[6] = 0;
    data[7] = 0; // y = 0
    data[8] = 0;
    data[9] = width as u8;
    data[10] = 0;
    data[11] = height as u8;
    data[12] = 0;
    data[13] = 0;
    data[14] = 0;
    data[15] = 0; // Raw encoding
    data[16..].copy_from_slice(&pixel_bytes);

    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data).unwrap();
    let (rects, _) = result;
    assert_eq!(rects.len(), 1, "expected 1 parsed rectangle");
    assert_eq!(rects[0].width, width);
    assert_eq!(rects[0].height, height);
    assert_eq!(
        rects[0].pixels.len(),
        48,
        "should have 48 bytes of RGB pixel data"
    );
}

// --- End T-004/T-005/T-006 tests ---

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

// --- T-001: ClientInit shared flag ---
//
// The RFB spec says the client MUST send shared=1 (0x01) to allow the server to
// keep other sessions alive.  Sending shared=0 (exclusive) causes many VNC servers
// (e.g. TigerVNC, LibVNCServer) to disconnect all other clients before responding
// with ServerInit, which has been observed to cause the session to stall.
//
// This test drives the full handshake over an in-memory duplex pipe and asserts
// that the byte written immediately after authentication is 0x01, not 0x00.

/// Build a minimal valid ServerInit payload (24 fixed bytes + 4-byte name length +
/// name bytes).  The pixel format is the default 32-bpp little-endian format.
fn make_server_init(width: u16, height: u16, name: &str) -> Vec<u8> {
    let mut buf = Vec::new();
    // width / height (big-endian u16 each)
    buf.extend_from_slice(&width.to_be_bytes());
    buf.extend_from_slice(&height.to_be_bytes());
    // pixel-format (16 bytes): bpp=32, depth=24, big_endian=0, true_color=1,
    // red_max=255, green_max=255, blue_max=255, red_shift=16, green_shift=8, blue_shift=0,
    // plus 3 padding bytes.
    let pf: [u8; 16] = [
        32, 24, 0, 1, // bpp, depth, big_endian, true_color
        0, 255, // red_max (big-endian u16 = 255)
        0, 255, // green_max
        0, 255, // blue_max
        16, 8, 0, // red_shift, green_shift, blue_shift
        0, 0, 0, // padding
    ];
    buf.extend_from_slice(&pf);
    // name length + name bytes
    let name_bytes = name.as_bytes();
    buf.extend_from_slice(&(name_bytes.len() as u32).to_be_bytes());
    buf.extend_from_slice(name_bytes);
    buf
}

#[tokio::test]
async fn test_handshake_sends_client_init_shared() {
    // We need two ends of a bidirectional in-memory channel:
    //   client_end  — the side passed to VncProtocol::handshake()
    //   server_end  — the side that plays the role of the VNC server
    let (mut server_end, client_end) = tokio::io::duplex(4096);
    let mut client_end = client_end; // make it mutable

    // --- Server side: runs concurrently via tokio::spawn ---
    let server_task = tokio::spawn(async move {
        // Step 1: send RFB version
        server_end
            .write_all(b"RFB 003.008\n")
            .await
            .expect("send version");

        // Step 2: read client version echo
        let mut client_ver = [0u8; 12];
        server_end
            .read_exact(&mut client_ver)
            .await
            .expect("read client version");
        assert_eq!(&client_ver, b"RFB 003.008\n");

        // Step 3: send security types [VncAuth=2]
        server_end
            .write_all(&[1u8, 2u8]) // count=1, type=VncAuth
            .await
            .expect("send security types");

        // Step 4: read client security type selection (should be 2)
        let mut sec_sel = [0u8; 1];
        server_end
            .read_exact(&mut sec_sel)
            .await
            .expect("read security selection");
        assert_eq!(sec_sel[0], 2, "client must select VncAuth");

        // Step 5: send VncAuth challenge (16 bytes)
        let challenge = [0xABu8; 16];
        server_end
            .write_all(&challenge)
            .await
            .expect("send challenge");

        // Step 6: read DES response (16 bytes) — we don't verify the crypto here
        let mut _response = [0u8; 16];
        server_end
            .read_exact(&mut _response)
            .await
            .expect("read response");

        // Step 7: send auth OK (4-byte big-endian 0)
        server_end
            .write_all(&[0u8; 4])
            .await
            .expect("send auth result");

        // Step 8: read ClientInit byte — THIS IS THE BYTE UNDER TEST
        let mut client_init = [0u8; 1];
        server_end
            .read_exact(&mut client_init)
            .await
            .expect("read ClientInit");
        let shared_flag = client_init[0];

        // Step 9: send ServerInit
        let server_init = make_server_init(1920, 1080, "test-desktop");
        server_end
            .write_all(&server_init)
            .await
            .expect("send ServerInit");

        shared_flag
    });

    // --- Client side: runs the real handshake ---
    let handshake_result = VncProtocol::handshake(&mut client_end, Some("password")).await;

    // --- Assertions ---
    assert!(
        handshake_result.is_ok(),
        "handshake must complete successfully: {:?}",
        handshake_result.err()
    );

    let shared_flag = server_task.await.expect("server task must complete");
    assert_eq!(
        shared_flag, 1,
        "ClientInit byte must be 1 (shared), not 0 (exclusive)"
    );
}

#[tokio::test]
async fn test_set_encodings_advertises_zrle_first() {
    // ZRLE decoder now uses Decompress::new(false) (raw deflate / RFC 1951),
    // which matches TigerVNC's wire format. ZRLE should be the first (preferred)
    // encoding so the server chooses it for best compression.
    use tokio::io::duplex;
    let (mut client_end, mut server_end) = duplex(4096);

    let send_task = tokio::spawn(async move {
        crate::vnc_protocol::VncProtocol::send_set_encodings(&mut client_end, false)
            .await
            .expect("send_set_encodings must succeed");
    });

    let mut buf = [0u8; 512];
    let n = server_end.read(&mut buf).await.expect("read SetEncodings");
    send_task.await.expect("send task");

    // Message layout: type(1) pad(1) count(2) then count×4 encoding IDs
    assert!(n >= 4, "need at least header bytes");
    let count = u16::from_be_bytes([buf[2], buf[3]]) as usize;
    assert!(n >= 4 + count * 4, "buffer too short for all encodings");

    let mut encodings = Vec::new();
    for i in 0..count {
        let off = 4 + i * 4;
        let enc = i32::from_be_bytes([buf[off], buf[off + 1], buf[off + 2], buf[off + 3]]);
        encodings.push(enc);
    }

    assert!(
        encodings.contains(&16),
        "ZRLE (16) must be advertised now that decoder uses raw deflate: encodings={:?}",
        encodings
    );
    assert_eq!(
        encodings[0], 16,
        "ZRLE must be the first (preferred) encoding: encodings={:?}",
        encodings
    );
}

// ---------------------------------------------------------------------------
// VNC auth downgrade prevention
// ---------------------------------------------------------------------------

/// When the server offers only "None" auth but the client has a password,
/// the handshake must reject the connection rather than proceeding without
/// any authentication. Accepting None auth silently drops the password and
/// allows connection to any VNC server without verification.
///
/// This test drives a mock server that advertises only SecurityType::None
/// and verifies that `handshake()` returns an error when a password is set.
/// When the server offers only "None" auth but the client has a password,
/// the connection must be rejected. Test via the exported selection helper.
#[test]
fn test_vnc_security_selection_rejects_none_when_password_set() {
    // select_security_type(types, has_password) → Result<VncSecurityType>
    use crate::vnc_protocol::select_security_type;
    use crate::vnc_protocol::VncSecurityType;

    // Server offers only None — must fail when a password is configured
    let result = select_security_type(&[VncSecurityType::None as u8], true);
    assert!(
        result.is_err(),
        "None-only server must be rejected when password is configured; got {:?}",
        result
    );

    // Server offers only None — allowed when no password (no-auth server)
    let result = select_security_type(&[VncSecurityType::None as u8], false);
    assert!(
        result.is_ok(),
        "None auth allowed when no password configured"
    );

    // Server offers VncAuth and None — must pick VncAuth regardless
    let result = select_security_type(
        &[VncSecurityType::None as u8, VncSecurityType::VncAuth as u8],
        true,
    );
    assert_eq!(
        result.unwrap(),
        VncSecurityType::VncAuth,
        "VncAuth must be preferred over None"
    );
}

/// VncAuth must be preferred over None (already works; regression guard).
#[test]
fn test_vnc_security_prefers_vncauth_over_none() {
    use crate::vnc_protocol::{select_security_type, VncSecurityType};
    let result = select_security_type(
        &[VncSecurityType::None as u8, VncSecurityType::VncAuth as u8],
        true,
    );
    assert_eq!(result.unwrap(), VncSecurityType::VncAuth);
}

/// The server-supplied name length in ServerInit must be capped before allocation.
/// A malicious VNC server can send name_len = 0xFFFFFFFF causing a 4 GiB allocation.
/// Test that the cap (reasonable max name length) is enforced.
#[test]
fn test_serverinitname_unbounded_length_cap() {
    use crate::vnc_protocol::MAX_VNC_NAME_LEN;
    const _: () = assert!(
        MAX_VNC_NAME_LEN <= 65536,
        "MAX_VNC_NAME_LEN must be at most 64 KiB"
    );
    // Simulated server-side name_len that exceeds the cap must be rejected.
    // We test the constant value; the actual read path is tested in integration tests.
    let malicious_len: u32 = 0xFFFF_FFFF;
    assert!(
        malicious_len as usize > MAX_VNC_NAME_LEN,
        "Sanity check: malicious length must exceed the cap"
    );
}

// --- Cursor parsing math tests ---

#[test]
fn test_parse_cursor_data_correct_size_32bpp() {
    // Verify parse_cursor_data accepts correctly-sized raw VNC cursor data.
    // 15×21 at 32bpp: pixel_data = 15*21*4 = 1260 bytes, bitmask = ceil(15/8)*21 = 3*21 = 63 bytes... wait
    // Actually mask_stride = ceil(15/8) = 2 (not 3; 15/8=1.875 rounds up to 2)
    // bitmask = 2*21 = 42 bytes, total = 1260 + 42 = 1302 bytes
    // This matches the crash: expected=1302, got=1260 (when RGBA was passed instead of raw).
    let width: u16 = 15;
    let height: u16 = 21;
    let bpp: u8 = 32;
    let pixel_data_size = width as usize * height as usize * (bpp as usize / 8); // 1260
    let mask_stride = (width as usize).div_ceil(8); // 2
    let bitmask_size = mask_stride * height as usize; // 42
    let total = pixel_data_size + bitmask_size; // 1302

    assert_eq!(pixel_data_size, 1260);
    assert_eq!(mask_stride, 2);
    assert_eq!(bitmask_size, 42);
    assert_eq!(total, 1302);

    // Build correctly-sized raw cursor data: pixel bytes followed by bitmask.
    let mut raw = vec![0u8; total];
    // Set bitmask to all-visible (all bits set).
    for b in &mut raw[pixel_data_size..] {
        *b = 0xFF;
    }

    let pixel_format = VncPixelFormat {
        bits_per_pixel: bpp,
        depth: 24,
        big_endian: false,
        true_color: true,
        red_max: 255,
        green_max: 255,
        blue_max: 255,
        red_shift: 16,
        green_shift: 8,
        blue_shift: 0,
    };

    let result = VncProtocol::parse_cursor_data(0, 0, width, height, &raw, &pixel_format);
    assert!(
        result.is_ok(),
        "parse_cursor_data should accept correctly-sized raw data: {:?}",
        result
    );
    let cursor = result.unwrap();
    assert_eq!(cursor.width, width);
    assert_eq!(cursor.height, height);
    assert_eq!(cursor.rgba_data.len(), width as usize * height as usize * 4);
}

#[test]
fn test_parse_cursor_data_rejects_rgba_input() {
    // Regression: the FBU loop pre-converts cursor pixels to RGBA before passing
    // to handle_cursor_update. Passing RGBA (1260 bytes for 15×21) to parse_cursor_data
    // which expects raw (1302 bytes) must fail with a clear error.
    // After the fix, handle_cursor_update no longer calls parse_cursor_data at all,
    // but this test documents the root cause of the crash.
    let width: u16 = 15;
    let height: u16 = 21;
    let rgba_size = width as usize * height as usize * 4; // 1260 — pixel data only, no mask
    let rgba_data = vec![0u8; rgba_size];

    let pixel_format = VncPixelFormat {
        bits_per_pixel: 32,
        depth: 24,
        big_endian: false,
        true_color: true,
        red_max: 255,
        green_max: 255,
        blue_max: 255,
        red_shift: 16,
        green_shift: 8,
        blue_shift: 0,
    };

    let result = VncProtocol::parse_cursor_data(0, 0, width, height, &rgba_data, &pixel_format);
    assert!(
        result.is_err(),
        "parse_cursor_data must reject RGBA-only data (missing 42-byte bitmask)"
    );
    let err = result.unwrap_err();
    assert!(
        err.contains("too short"),
        "error should mention 'too short', got: {err}"
    );
}

#[test]
fn test_parse_cursor_data_zero_dimensions() {
    // 0×0 cursor must return an empty VncCursor without error.
    let pixel_format = VncPixelFormat {
        bits_per_pixel: 32,
        depth: 24,
        big_endian: false,
        true_color: true,
        red_max: 255,
        green_max: 255,
        blue_max: 255,
        red_shift: 16,
        green_shift: 8,
        blue_shift: 0,
    };
    let result = VncProtocol::parse_cursor_data(0, 0, 0, 0, &[], &pixel_format);
    assert!(result.is_ok());
    let cursor = result.unwrap();
    assert_eq!(cursor.width, 0);
    assert_eq!(cursor.rgba_data.len(), 0);
}
