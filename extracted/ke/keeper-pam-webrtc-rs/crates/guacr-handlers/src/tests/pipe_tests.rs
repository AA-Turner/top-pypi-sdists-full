use crate::pipe::{
    format_end_instruction, format_pipe_blob, format_pipe_instruction, parse_blob_instruction,
    parse_end_instruction, parse_pipe_instruction, PipeStream, PipeStreamManager,
};

#[test]
fn test_pipe_stream_flags() {
    let pipe = PipeStream::stdout();
    assert!(pipe.is_raw());
    assert!(pipe.is_autoflush());
    assert!(pipe.interpret_output());
}

#[test]
fn test_format_pipe_instruction() {
    let pipe = PipeStream::stdout();
    let instr = format_pipe_instruction(&pipe);
    assert!(instr.starts_with("4.pipe,"));
    assert!(instr.contains("STDOUT"));
    assert!(instr.contains("application/octet-stream"));
}

#[test]
fn test_format_pipe_blob() {
    let instr = format_pipe_blob(100, b"hello");
    assert!(instr.starts_with("4.blob,"));
    assert!(instr.contains("100"));
    // "hello" base64 = "aGVsbG8="
    assert!(instr.contains("aGVsbG8="));
}

#[test]
fn test_format_end_instruction() {
    let instr = format_end_instruction(100);
    assert_eq!(instr, "3.end,3.100;");
}

#[test]
fn test_parse_pipe_instruction() {
    let parsed = parse_pipe_instruction("4.pipe,3.100,24.application/octet-stream,6.STDOUT;");
    assert!(parsed.is_some());
    let parsed = parsed.unwrap();
    assert_eq!(parsed.stream_id, 100);
    assert_eq!(parsed.mimetype, "application/octet-stream");
    assert_eq!(parsed.name, "STDOUT");
}

#[test]
fn test_parse_blob_instruction() {
    // "hello" base64 = "aGVsbG8="
    let parsed = parse_blob_instruction("4.blob,3.100,8.aGVsbG8=;");
    assert!(parsed.is_some());
    let parsed = parsed.unwrap();
    assert_eq!(parsed.stream_id, 100);
    assert_eq!(parsed.data, b"hello");
}

#[test]
fn test_parse_end_instruction() {
    let stream_id = parse_end_instruction("3.end,3.100;");
    assert_eq!(stream_id, Some(100));
}

#[test]
fn test_pipe_stream_manager() {
    let mut manager = PipeStreamManager::new();

    // Enable STDOUT
    let instr = manager.enable_stdout();
    assert!(instr.contains("STDOUT"));
    assert!(manager.is_stdout_enabled());

    // Register STDIN
    manager.register_incoming(101, "STDIN", "application/octet-stream");
    assert!(manager.is_stdin_stream(101));
    assert!(!manager.is_stdin_stream(100));

    // Get by name
    assert!(manager.get("STDOUT").is_some());
    assert!(manager.get("STDIN").is_some());
    assert!(manager.get("UNKNOWN").is_none());
}
