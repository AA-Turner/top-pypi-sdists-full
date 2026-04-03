use crate::streams::{
    format_audio, format_bell_audio, format_blob, format_chunked_blobs, format_clipboard,
    format_clipboard_text, format_end, format_video, parse_clipboard_blob,
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
