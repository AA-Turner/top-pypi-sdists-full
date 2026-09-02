use crate::binary::{
    BinaryEncoder, Opcode, FLAG_FRAGMENTED, FRAGMENT_PAYLOAD_SIZE, FRAME_PROTOCOL_OVERHEAD,
    MAX_SAFE_PAYLOAD_SIZE,
};
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

// ── T-065, T-066, T-067: Fragmentation tests ───────────────────────────────

// AC-1: Sub-limit message → single non-fragmented frame.
#[test]
fn test_fragment_sub_limit_not_fragmented() {
    let mut enc = BinaryEncoder::new();
    let payload = vec![0xABu8; 100]; // well under MAX_SAFE_PAYLOAD_SIZE
    let frames = enc.fragment_message(Opcode::Image, 0, &payload);
    assert_eq!(frames.len(), 1, "sub-limit message must be a single frame");
    // FLAG_FRAGMENTED must NOT be set.
    assert_eq!(
        frames[0][1] & FLAG_FRAGMENTED,
        0,
        "non-fragmented flag must not be set"
    );
    // Opcode must match.
    assert_eq!(frames[0][0], Opcode::Image as u8);
    // AC-5: backward compatibility — reserved field is zero (standard header).
    assert_eq!(
        frames[0][2], 0,
        "reserved[0] must be zero for non-fragmented"
    );
    assert_eq!(
        frames[0][3], 0,
        "reserved[1] must be zero for non-fragmented"
    );
}

// AC-2: Over-limit message → split into multiple frames within the limit.
#[test]
fn test_fragment_over_limit_splits() {
    let mut enc = BinaryEncoder::new();
    let payload_size = FRAGMENT_PAYLOAD_SIZE * 2 + 100; // forces 3 fragments
    let payload = vec![0xBBu8; payload_size];
    let frames = enc.fragment_message(Opcode::Audio, 0, &payload);
    assert_eq!(frames.len(), 3, "should produce exactly 3 fragments");
    // Each fragment must fit within MAX_SAFE_PAYLOAD_SIZE.
    for frame in &frames {
        assert!(
            frame.len() <= MAX_SAFE_PAYLOAD_SIZE,
            "fragment exceeds safe payload size"
        );
    }
}

// AC-3: Each fragment carries FLAG_FRAGMENTED + seq_num (reserved[0]) + total_count (reserved[1]).
#[test]
fn test_fragment_headers_seq_and_total() {
    let mut enc = BinaryEncoder::new();
    let payload = vec![0xCCu8; FRAGMENT_PAYLOAD_SIZE + 1]; // forces 2 fragments
    let frames = enc.fragment_message(Opcode::Cursor, 0, &payload);
    assert_eq!(frames.len(), 2);
    for frame in &frames {
        // FLAG_FRAGMENTED must be set.
        assert_ne!(frame[1] & FLAG_FRAGMENTED, 0, "FLAG_FRAGMENTED must be set");
        // Total count in reserved[1] must be 2.
        assert_eq!(frame[3], 2, "total_count must be 2 in reserved[1]");
    }
    // Seq numbers must be 0 and 1.
    assert_eq!(frames[0][2], 0, "first fragment seq must be 0");
    assert_eq!(frames[1][2], 1, "second fragment seq must be 1");
}

// AC-4: All fragments share the same opcode.
#[test]
fn test_fragment_shares_opcode() {
    let mut enc = BinaryEncoder::new();
    let payload = vec![0u8; FRAGMENT_PAYLOAD_SIZE * 3];
    let frames = enc.fragment_message(Opcode::Audio, 0, &payload);
    for frame in &frames {
        assert_eq!(
            frame[0],
            Opcode::Audio as u8,
            "all fragments must share the Audio opcode"
        );
    }
}

// AC-5: Backward compatibility — non-fragmented message has standard reserved=0 header.
#[test]
fn test_non_fragmented_standard_header() {
    let mut enc = BinaryEncoder::new();
    let payload = vec![42u8; 8];
    let frames = enc.fragment_message(Opcode::Key, 0, &payload);
    assert_eq!(frames.len(), 1);
    // Header bytes: [opcode, flags, reserved_lo, reserved_hi, len_le x4]
    assert_eq!(frames[0][0], Opcode::Key as u8);
    assert_eq!(frames[0][1], 0); // flags: 0
    assert_eq!(frames[0][2], 0); // reserved[0]: 0
    assert_eq!(frames[0][3], 0); // reserved[1]: 0
}

// ── End fragmentation tests ─────────────────────────────────────────────────

// AC-6: Compile-time invariant — a fragment plus its outer Frame must fit the vault's real
// incoming cap. ControlDataChannel.ts drops anything over MAX_INCOMING_MESSAGE_BYTES, which is
// (16 * 1024 - PROTOCOL_BYTE_LENGTH) * 2, where PROTOCOL_BYTE_LENGTH is the full 17-byte outer
// frame: CONNECTION_NUMBER(4) + TIME_STAMP(8) + DATA_LENGTH(4) + TERMINATOR(1). That gives
// 32,734 — deliberately NOT 32 * 1024.
//
// This number has been wrong twice, in both directions, so it is pinned here rather than
// trusted: 60 KiB first (sized against the generic 64 KiB SCTP limit — the browser logged
// "Oversized incoming message (61457 bytes)", and 61,457 == 61,440 + FRAME_PROTOCOL_OVERHEAD),
// then 32,750, which mirrored a vault PROTOCOL_BYTE_LENGTH that omitted the 8 timestamp bytes
// the wire message actually carries. The vault has since corrected that, moving the cap down
// by 16 bytes.
const _: () = assert!(
    MAX_SAFE_PAYLOAD_SIZE + FRAME_PROTOCOL_OVERHEAD <= (16 * 1024 - FRAME_PROTOCOL_OVERHEAD) * 2
);

// AC-6b: the inequality above is necessary but not sufficient — it passed while the constant was
// still 18 bytes too large for a different reason (it was checked against 32 * 1024). This test
// measures what actually goes on the wire for a real multi-fragment RBI-sized screenshot, so an
// off-by-N in the constant fails here regardless of which limit the comment claims.
#[test]
fn test_every_wire_message_fits_vault_incoming_cap() {
    // ControlDataChannel.ts: MAX_MESSAGE_SIZE_BYTES * 2, with the full 17-byte frame subtracted.
    const VAULT_MAX_INCOMING: usize = (16 * 1024 - FRAME_PROTOCOL_OVERHEAD) * 2; // 32,734

    let mut enc = BinaryEncoder::new();
    // ~99 KB, the screenshot size that produced the original "no content received" report.
    let payload = vec![0x7Au8; 99 * 1024];
    let frames = enc.fragment_message(Opcode::Image, 0, &payload);

    assert!(frames.len() > 1, "99 KB payload must fragment");

    for (i, frame) in frames.iter().enumerate() {
        let wire_len = frame.len() + FRAME_PROTOCOL_OVERHEAD;
        assert!(
            wire_len <= VAULT_MAX_INCOMING,
            "fragment {i}/{} goes on the wire at {wire_len} bytes, over the vault's \
             {VAULT_MAX_INCOMING}-byte incoming cap — it will be silently dropped",
            frames.len()
        );
    }
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
