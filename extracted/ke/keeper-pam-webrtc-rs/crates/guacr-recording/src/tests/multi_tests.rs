use crate::config::RecordingConfig;
use crate::multi::MultiFormatRecorder;
use crate::ses::RecordingDirection;
use bytes::Bytes;
use std::collections::HashMap;
use tempfile::TempDir;

#[test]
fn test_multi_format_recorder_asciicast() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "test-session".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record some output
    recorder.record_output(b"Hello, World!\r\n").unwrap();
    recorder.record_output(b"$ ").unwrap();

    recorder.finalize().unwrap();

    // Check asciicast file exists and has valid format
    let cast_path = tmp_dir.path().join("test-session.cast");
    assert!(cast_path.exists(), "Asciicast file should exist");

    let content = std::fs::read_to_string(&cast_path).unwrap();

    // Check header line
    assert!(
        content.starts_with("{\"version\":2"),
        "Should have v2 header"
    );
    assert!(content.contains("\"width\":80"), "Should have width");
    assert!(content.contains("\"height\":24"), "Should have height");

    // Check output events
    assert!(
        content.contains(r#","o","Hello, World!"#),
        "Should contain output event"
    );
}

#[test]
fn test_multi_format_recorder_ses_and_asciicast() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "dual-format".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record instruction (for .ses) - raw Guacamole protocol
    let instruction = Bytes::from("4.size,1.0,3.800,3.600;");
    recorder
        .record_instruction(RecordingDirection::ServerToClient, &instruction)
        .unwrap();

    // Record output (for .cast)
    recorder.record_output(b"Login successful\r\n").unwrap();

    recorder.finalize().unwrap();

    // Both files should exist
    let ses_path = tmp_dir.path().join("dual-format.ses");
    let cast_path = tmp_dir.path().join("dual-format.cast");

    assert!(ses_path.exists(), ".ses file should exist");
    assert!(cast_path.exists(), ".cast file should exist");

    // Verify .ses content - raw Guacamole protocol format
    let ses_content = std::fs::read_to_string(&ses_path).unwrap();
    assert!(
        ses_content.contains("4.size,1.0,3.800,3.600;"),
        ".ses should have raw instruction without timestamp prefix"
    );

    // Verify .cast content - asciicast v2 format
    let cast_content = std::fs::read_to_string(&cast_path).unwrap();
    assert!(
        cast_content.contains("Login successful"),
        ".cast should have output"
    );
}

#[test]
fn test_asciicast_input_recording() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "input-test".to_string());
    params.insert("recording-include-keys".to_string(), "true".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record input (only if recording_include_keys is true)
    recorder.record_input(b"ls -la").unwrap();
    recorder.finalize().unwrap();

    let cast_path = tmp_dir.path().join("input-test.cast");
    let content = std::fs::read_to_string(&cast_path).unwrap();

    // Input events use "i" type
    assert!(
        content.contains(r#","i","ls -la"#),
        "Should contain input event"
    );
}

#[test]
fn test_asciicast_input_not_recorded_by_default() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "no-input".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    assert!(
        !config.recording_include_keys,
        "Keys should NOT be included by default"
    );

    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record output and input
    recorder.record_output(b"prompt$ ").unwrap();
    recorder.record_input(b"secret_password").unwrap(); // Should be ignored
    recorder.finalize().unwrap();

    let cast_path = tmp_dir.path().join("no-input.cast");
    let content = std::fs::read_to_string(&cast_path).unwrap();

    // Should have output but NOT input
    assert!(content.contains("prompt$"), "Should have output");
    assert!(
        !content.contains("secret_password"),
        "Should NOT have input (security)"
    );
}

#[test]
fn test_asciicast_resize_event() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "resize-test".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record resize
    recorder.record_resize(120, 40).unwrap();
    recorder.finalize().unwrap();

    let cast_path = tmp_dir.path().join("resize-test.cast");
    let content = std::fs::read_to_string(&cast_path).unwrap();

    // Resize events use "r" type
    assert!(
        content.contains(r#","r","120x40"#),
        "Should contain resize event"
    );
}

#[test]
fn test_typescript_recording_with_timing() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "typescript-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("typescript-name".to_string(), "typescript-test".to_string());
    params.insert("create-typescript-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    assert!(
        config.is_typescript_enabled(),
        "Typescript should be enabled"
    );

    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record output
    recorder.record_output(b"Script output here\r\n").unwrap();
    recorder.finalize().unwrap();

    let ts_path = tmp_dir.path().join("typescript-test");
    assert!(ts_path.exists(), "Typescript file should exist");

    let content = std::fs::read_to_string(&ts_path).unwrap();
    assert!(
        content.contains("Script output here"),
        "Should have raw output"
    );
    assert!(content.contains("Script done on"), "Should have footer");

    // Check timing file exists
    let timing_path = tmp_dir.path().join("typescript-test.timing");
    assert!(timing_path.exists(), "Timing file should exist");

    let timing_content = std::fs::read_to_string(&timing_path).unwrap();
    assert!(
        !timing_content.is_empty(),
        "Timing file should have content"
    );
    // Format: elapsed_seconds byte_count
    let line = timing_content.lines().next().unwrap();
    let parts: Vec<&str> = line.split_whitespace().collect();
    assert_eq!(parts.len(), 2, "Timing line should have 2 fields");
    parts[0]
        .parse::<f64>()
        .expect("First field should be elapsed seconds");
    parts[1]
        .parse::<usize>()
        .expect("Second field should be byte count");
}

#[test]
fn test_asciicast_can_be_parsed_as_json() {
    // Verify asciicast output is valid JSON (NDJSON format)
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "json-test".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Record some output
    recorder.record_output(b"Hello, World!\r\n").unwrap();
    recorder.record_output(b"$ ls -la\r\n").unwrap();
    recorder.record_resize(120, 40).unwrap();
    recorder.finalize().unwrap();

    let cast_path = tmp_dir.path().join("json-test.cast");
    let content = std::fs::read_to_string(&cast_path).unwrap();

    // Each line should be valid JSON
    for (i, line) in content.lines().enumerate() {
        let parsed: Result<serde_json::Value, _> = serde_json::from_str(line);
        assert!(
            parsed.is_ok(),
            "Line {} should be valid JSON: {}",
            i + 1,
            line
        );

        if i == 0 {
            // First line is header
            let header = parsed.unwrap();
            assert_eq!(header["version"], 2, "Should be asciicast v2");
            assert_eq!(header["width"], 80);
            assert_eq!(header["height"], 24);
        } else {
            // Other lines are events: [time, type, data]
            let event = parsed.unwrap();
            assert!(event.is_array(), "Event should be array");
            let arr = event.as_array().unwrap();
            assert_eq!(arr.len(), 3, "Event should have 3 elements");
            assert!(arr[0].is_f64(), "First element should be timestamp");
            assert!(arr[1].is_string(), "Second element should be event type");
        }
    }
}

#[test]
fn test_recording_empty_session() {
    // Edge case: session with no recorded content
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "empty".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Immediately finalize without recording anything
    recorder.finalize().unwrap();

    let cast_path = tmp_dir.path().join("empty.cast");
    assert!(cast_path.exists(), "File should exist even if empty");

    let content = std::fs::read_to_string(&cast_path).unwrap();

    // Should have at least the header
    assert!(!content.is_empty(), "Should have header");
    let header: serde_json::Value = serde_json::from_str(content.lines().next().unwrap()).unwrap();
    assert_eq!(header["version"], 2);
}

#[test]
fn test_full_ssh_session_recording() {
    // Simulate a complete SSH session recording
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "ssh-session".to_string());
    params.insert("recording-include-keys".to_string(), "true".to_string());
    params.insert("create-recording-path".to_string(), "true".to_string());
    params.insert("username".to_string(), "testuser".to_string());
    params.insert("hostname".to_string(), "192.168.1.100".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Simulate session flow
    recorder
        .record_instruction(
            RecordingDirection::ServerToClient,
            &Bytes::from("4.size,1.0,2.80,2.24;"),
        )
        .unwrap();

    recorder.record_output(b"login: ").unwrap();
    recorder.record_input(b"testuser").unwrap();
    recorder.record_output(b"testuser\r\n").unwrap();
    recorder.record_output(b"Password: ").unwrap();
    recorder.record_input(b"secret123").unwrap();
    recorder.record_output(b"\r\n").unwrap();
    recorder.record_output(b"testuser@host:~$ ").unwrap();
    recorder.record_input(b"ls -la").unwrap();
    recorder.record_output(b"ls -la\r\n").unwrap();
    recorder.record_output(b"total 32\r\n").unwrap();
    recorder.record_resize(120, 40).unwrap();
    recorder.record_input(b"exit").unwrap();
    recorder.record_output(b"exit\r\nlogout\r\n").unwrap();

    recorder.finalize().unwrap();

    // Verify files exist and have content
    let ses_path = tmp_dir.path().join("ssh-session.ses");
    let cast_path = tmp_dir.path().join("ssh-session.cast");

    assert!(ses_path.exists(), ".ses file should exist");
    assert!(cast_path.exists(), ".cast file should exist");

    let ses_content = std::fs::read_to_string(&ses_path).unwrap();
    let cast_content = std::fs::read_to_string(&cast_path).unwrap();

    assert!(
        ses_content.contains("4.size,"),
        ".ses should have size instruction"
    );

    assert!(
        cast_content.contains("testuser@host"),
        ".cast should have prompt"
    );
    assert!(cast_content.contains("ls -la"), ".cast should have command");
    assert!(
        cast_content.contains("120x40"),
        ".cast should have resize event"
    );
    assert!(
        cast_content.contains(r#","i","#),
        ".cast should have input events"
    );
}
