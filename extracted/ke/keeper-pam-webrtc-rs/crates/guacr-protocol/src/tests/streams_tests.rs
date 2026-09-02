use crate::streams::{
    format_audio, format_bell_audio, format_blob, format_chunked_blobs, format_clipboard,
    format_clipboard_text, format_end, format_terminal_data, format_terminal_data_binary,
    format_video, format_vnc_data, parse_clipboard_blob,
};

#[test]
fn test_format_audio() {
    let instr = format_audio(1, "audio/wav");
    assert_eq!(instr, "5.audio,1.1,9.audio/wav;");
}

#[test]
fn test_format_blob() {
    let instr = format_blob(1, "dGVzdA==");
    // Format: blob,<stream_len>.<stream>,<data_len>.<data>;
    // stream=1 (len=1), data_len=8 (len=1), data="dGVzdA=="
    // Note: This matches TerminalRenderer format: 4.blob,1.1,8.dGVzdA==;
    assert_eq!(instr, "4.blob,1.1,8.dGVzdA==;");
}

#[test]
fn test_format_end() {
    let instr = format_end(1);
    assert_eq!(instr, "3.end,1.1;");
}

#[test]
fn test_format_video() {
    let instr = format_video(2, "video/mp4");
    assert_eq!(instr, "5.video,1.2,9.video/mp4;");
}

#[test]
fn test_format_bell_audio() {
    let instrs = format_bell_audio(1);
    assert_eq!(instrs.len(), 3);
    assert!(instrs[0].contains("audio"));
    assert!(instrs[1].contains("blob"));
    assert!(instrs[2].contains("end"));
}

#[test]
fn test_format_chunked_blobs_small() {
    // Small data - should be 1 blob + 1 end
    let data = "dGVzdA=="; // 8 bytes
    let instrs = format_chunked_blobs(1, data, Some(100)); // 100 byte chunks
    assert_eq!(instrs.len(), 2); // 1 blob + 1 end
    assert!(instrs[0].contains("blob"));
    assert!(instrs[0].contains(data));
    assert!(instrs[1].contains("end"));
}

#[test]
fn test_format_chunked_blobs_large() {
    // Large data - should be multiple blobs + 1 end
    let data = "A".repeat(20000); // 20KB
    let instrs = format_chunked_blobs(1, &data, Some(6144)); // 6KB chunks
    assert_eq!(instrs.len(), 5); // 4 blobs + 1 end (20000 / 6144 = 3.26 -> 4 chunks)

    // Verify all but last are blobs
    for instr in instrs.iter().take(4) {
        assert!(instr.contains("blob"));
    }

    // Verify last is end
    assert!(instrs[4].contains("end"));
}

#[test]
fn test_format_chunked_blobs_default_chunk_size() {
    // Test default chunk size (6KB)
    let data = "B".repeat(20000);
    let instrs = format_chunked_blobs(1, &data, None); // Use default
    assert_eq!(instrs.len(), 5); // 4 blobs + 1 end
}

#[test]
fn test_format_clipboard_text() {
    let instrs = format_clipboard_text(10, "Hello");
    assert_eq!(instrs.len(), 3);
    assert!(instrs[0].contains("clipboard"));
    assert!(instrs[0].contains("text/plain"));
    assert!(instrs[1].contains("blob"));
    assert!(instrs[2].contains("end"));
}

#[test]
fn test_format_clipboard_binary() {
    let instrs = format_clipboard(5, "text/html", b"<b>bold</b>");
    assert_eq!(instrs.len(), 3);
    assert!(instrs[0].contains("clipboard"));
    assert!(instrs[0].contains("text/html"));
}

#[test]
fn test_parse_clipboard_blob() {
    use base64::Engine;
    let data = base64::engine::general_purpose::STANDARD.encode(b"Hello World");
    let msg = format!("4.blob,2.10,{}.{};", data.len(), data);
    let result = parse_clipboard_blob(&msg);
    assert_eq!(result, Some("Hello World".to_string()));
}

#[test]
fn test_parse_clipboard_blob_empty() {
    use base64::Engine;
    let data = base64::engine::general_purpose::STANDARD.encode(b"");
    let msg = format!("4.blob,2.10,{}.{};", data.len(), data);
    let result = parse_clipboard_blob(&msg);
    assert_eq!(result, None); // Empty clipboard returns None
}

#[test]
fn test_parse_clipboard_blob_not_blob() {
    let result = parse_clipboard_blob("3.key,2.65,1.1;");
    assert_eq!(result, None);
}

#[test]
fn test_format_terminal_data_guacamole_framing() {
    let instr = format_terminal_data(b"hello");
    let s = std::str::from_utf8(&instr).unwrap();
    // Opcode "terminal-data" is 13 chars; base64("hello") = "aGVsbG8="
    assert_eq!(s, "13.terminal-data,8.aGVsbG8=;");
}

#[test]
fn test_format_terminal_data_roundtrip() {
    use base64::Engine;
    let input = b"\x1b[32mgreen\x1b[0m";
    let instr = format_terminal_data(input);
    let s = std::str::from_utf8(&instr).unwrap();
    // Extract base64 payload after the last comma
    let b64 = s.split(',').next_back().unwrap().trim_end_matches(';');
    let (_, data) = b64.split_once('.').unwrap();
    let decoded = base64::engine::general_purpose::STANDARD
        .decode(data)
        .unwrap();
    assert_eq!(decoded, input);
}

#[test]
fn test_format_terminal_data_empty() {
    let instr = format_terminal_data(b"");
    let s = std::str::from_utf8(&instr).unwrap();
    // base64("") = ""
    assert_eq!(s, "13.terminal-data,0.;");
}

#[test]
fn test_format_terminal_data_binary_header_and_payload() {
    let msg = format_terminal_data_binary(b"hello");
    assert_eq!(msg.len(), 13); // 8-byte header + 5 bytes
    assert_eq!(msg[0], 0x20); // TerminalData opcode
    assert_eq!(msg[1], 0x00); // flags
    assert_eq!(&msg[2..4], &[0, 0]); // reserved
    assert_eq!(&msg[4..8], &[5, 0, 0, 0]); // payload_len LE
    assert_eq!(&msg[8..], b"hello");
}

#[test]
fn test_format_terminal_data_binary_ansi_passthrough() {
    let ansi = b"\x1b[32mgreen\x1b[0m";
    let msg = format_terminal_data_binary(ansi);
    assert_eq!(msg.len(), 8 + ansi.len());
    assert_eq!(msg[0], 0x20);
    assert_eq!(&msg[8..], ansi);
}

#[test]
fn test_format_terminal_data_binary_empty() {
    let msg = format_terminal_data_binary(b"");
    assert_eq!(msg.len(), 8);
    assert_eq!(msg[0], 0x20);
    assert_eq!(&msg[4..8], &[0, 0, 0, 0]); // payload_len = 0
}

#[test]
fn test_format_vnc_data_guacamole_framing() {
    let instr = format_vnc_data(b"\x00\x01");
    let s = std::str::from_utf8(&instr).unwrap();
    // Opcode "vnc-data" is 8 chars; base64("\x00\x01") = "AAE="
    assert_eq!(s, "8.vnc-data,4.AAE=;");
}
