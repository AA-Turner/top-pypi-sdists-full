use super::ses_tests::{parse_recording, RecordedEvent};
use crate::config::RecordingConfig;
use crate::multi::MultiFormatRecorder;
use crate::ses::{RecordingDirection, RecordingError, SesPayload};
use bytes::Bytes;
use std::collections::HashMap;
use tempfile::TempDir;

#[test]
fn test_terminal_geometry_precedes_output_and_tracks_resizes_once() {
    let dir = TempDir::new().unwrap();
    let params = HashMap::from([
        ("recording-path".into(), dir.path().display().to_string()),
        ("recording-name".into(), "geometry".into()),
    ]);
    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new_with_payload(
        &config,
        &params,
        "ssh",
        163,
        51,
        SesPayload::Terminal,
    )
    .unwrap();
    recorder.record_resize(163, 51).unwrap();
    recorder
        .record_instruction(
            RecordingDirection::ServerToClient,
            &guacr_protocol::format_terminal_data_binary(b"first\xff\x00;screen"),
        )
        .unwrap();
    recorder.record_resize(194, 58).unwrap();
    recorder.record_resize(194, 58).unwrap();
    recorder
        .record_instruction(
            RecordingDirection::ServerToClient,
            &guacr_protocol::format_terminal_data_binary(b"second screen"),
        )
        .unwrap();
    recorder.finalize().unwrap();

    let bytes = std::fs::read(dir.path().join("geometry.ses")).unwrap();
    let events = parse_recording(&bytes);
    assert_eq!(events.len(), 7);
    assert_eq!(
        events[0],
        RecordedEvent::Instruction("guacr".into(), vec!["terminal".into(), "1".into()])
    );
    assert_eq!(
        events[1],
        RecordedEvent::Instruction(
            "guacr".into(),
            vec![
                "terminal-size".into(),
                "163".into(),
                "51".into(),
                "0".into()
            ]
        )
    );
    assert_eq!(events[2], RecordedEvent::Output(b"first\xff\x00;screen"));
    assert_eq!(events[5], RecordedEvent::Output(b"second screen"));
    let timestamp = |event: &RecordedEvent<'_>, opcode: &str, index: usize| {
        let RecordedEvent::Instruction(actual, args) = event else {
            panic!("expected timestamp instruction")
        };
        assert_eq!(actual, opcode);
        args[index].parse::<u64>().unwrap()
    };
    let first_time = timestamp(&events[3], "sync", 0);
    let RecordedEvent::Instruction(opcode, size) = &events[4] else {
        panic!("expected resize")
    };
    assert_eq!(opcode, "guacr");
    assert_eq!(&size[..3], ["terminal-size", "194", "58"]);
    let resized_time = timestamp(&events[4], "guacr", 3);
    assert!(first_time <= resized_time);
    assert!(resized_time <= timestamp(&events[6], "sync", 0));

    let cast = std::fs::read_to_string(dir.path().join("geometry.cast")).unwrap();
    let lines: Vec<serde_json::Value> = cast
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    assert_eq!(
        lines.len(),
        2,
        "unchanged sizes must not duplicate asciicast events"
    );
    assert_eq!(lines[0]["width"], 163);
    assert_eq!(lines[0]["height"], 51);
    assert_eq!(lines[1][1], "r");
    assert_eq!(lines[1][2], "194x58");
}

#[test]
fn test_graphical_ses_is_unchanged_by_terminal_geometry() {
    let dir = TempDir::new().unwrap();
    let params = HashMap::from([
        ("recording-path".into(), dir.path().display().to_string()),
        ("recording-name".into(), "graphical".into()),
    ]);
    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "vnc", 80, 24).unwrap();
    recorder.record_resize(120, 40).unwrap();
    let instruction = Bytes::from_static(b"4.size,1.0,4.1024,3.768;");
    recorder
        .record_instruction(RecordingDirection::ServerToClient, &instruction)
        .unwrap();
    recorder.record_resize(120, 40).unwrap();
    recorder.finalize().unwrap();
    assert_eq!(
        std::fs::read(dir.path().join("graphical.ses")).unwrap(),
        instruction.as_ref()
    );
}

#[test]
fn test_geometry_survives_output_exclusion_without_frames_or_keys() {
    let dir = TempDir::new().unwrap();
    let params = HashMap::from([
        ("recording-path".into(), dir.path().display().to_string()),
        ("recording-name".into(), "excluded".into()),
        ("recording-exclude-output".into(), "true".into()),
    ]);
    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new_with_payload(
        &config,
        &params,
        "mysql",
        80,
        24,
        SesPayload::Terminal,
    )
    .unwrap();
    recorder
        .record_instruction(
            RecordingDirection::ServerToClient,
            &guacr_protocol::format_terminal_data_binary(b"secret output"),
        )
        .unwrap();
    recorder
        .record_instruction(
            RecordingDirection::ClientToServer,
            &Bytes::from_static(b"3.key,2.97,1.1;"),
        )
        .unwrap();
    recorder.record_resize(120, 40).unwrap();
    recorder.finalize().unwrap();
    let bytes = std::fs::read(dir.path().join("excluded.ses")).unwrap();
    let events = parse_recording(&bytes);
    assert_eq!(
        events.len(),
        3,
        "excluded frames must not retain their timing sync or keys"
    );
    for event in &events[1..] {
        let RecordedEvent::Instruction(opcode, args) = event else {
            panic!("output must be excluded")
        };
        assert_eq!(opcode, "guacr");
        assert_eq!(args[0], "terminal-size");
    }
}

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
    assert!(content.contains("[END TYPESCRIPT]"), "Should have footer");

    // Timing file is the typescript filename with ".timing" appended.
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

/// guacd builds the timing filename by appending (`"%s.%s"`,
/// `src/terminal/typescript.c:133`), so a typescript named `<stamp>.tys` gets
/// `<stamp>.tys.timing`. The gateway mkfifos exactly that name
/// (`tunnel_recordings.py:1828`) and the FIFO has no other writer, so replacing the
/// extension instead of appending leaves the gateway's reader blocked on a pipe that
/// nothing ever opens.
#[test]
fn test_timing_filename_appends_to_typescript_name() {
    let tmp_dir = TempDir::new().unwrap();

    let mut params = HashMap::new();
    params.insert(
        "typescript-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    // The gateway's spelling: recording name plus the ".tys" type suffix.
    params.insert("typescript-name".to_string(), "20260915-120000.tys".into());
    params.insert("create-typescript-path".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();
    recorder.record_output(b"output\r\n").unwrap();
    recorder.finalize().unwrap();

    assert!(
        tmp_dir.path().join("20260915-120000.tys").exists(),
        "typescript file should exist"
    );
    assert!(
        tmp_dir.path().join("20260915-120000.tys.timing").exists(),
        "timing file should be the typescript name with .timing appended, found: {:?}",
        std::fs::read_dir(tmp_dir.path())
            .unwrap()
            .filter_map(|entry| Some(entry.ok()?.file_name()))
            .collect::<Vec<_>>()
    );
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

#[cfg(feature = "zmq-transport")]
#[test]
fn test_zmq_only_recorder_is_active() {
    let config = RecordingConfig {
        zmq_addr: Some("tcp://127.0.0.1:15555".to_string()),
        ..Default::default()
    };
    let params = HashMap::new();
    let recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();
    assert!(
        recorder.is_active(),
        "ZMQ-only recorder must report active so Drop calls finalize"
    );
}

/// A strict session whose recorder cannot be created must be refusable.
///
/// `recording-allow-unrecorded=false` (the default, config.rs:165) is the operator saying
/// "no recording, no session". When the destination cannot be opened, `new_with_payload`
/// reports `PathCreation` -- indistinguishable from an ordinary I/O hiccup. Both handler
/// call sites read it that way and continue unrecorded: guacr-ssh/src/handler.rs:481-487
/// and guacr-rdp/src/handler.rs:1058-1064 each `warn!` and fall through to `None`, without
/// consulting `allow_unrecorded`. So the strict promise has no enforcement point and the
/// session runs to completion with no recording and no user-visible failure.
///
/// `Unrecordable` is this crate's own signal for the condition (ses.rs:80-85: "no retry can
/// help: the session itself has to end"), and the video path already uses it that way
/// (guacr-recorder/src/video_sink.rs:166). Terminal recorder construction does not.
///
/// The vehicle is a missing directory with `create-recording-path` off, which is the
/// platform-independent form of the condition. (This test previously used the Windows
/// gateway's `ipc://` parameter shape, which reached the same failure by accident of that
/// endpoint being treated as a directory; an endpoint is now a supported `.ses` destination
/// in its own right, so it no longer demonstrates an unopenable one.)
#[test]
fn test_strict_recording_reports_recorder_init_failure_as_fatal() {
    let mut params = HashMap::new();
    params.insert("recordingname".to_string(), "session.ses".to_string());
    params.insert(
        "recordingpath".to_string(),
        "/nonexistent-guacr-strict-recording-test/nested".to_string(),
    );
    params.insert("recordingwriteexisting".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    assert!(
        !config.create_recording_path,
        "create-recording-path is off, so the missing directory is not created for us"
    );
    assert!(
        !config.allow_unrecorded,
        "recording-allow-unrecorded defaults to false, so this session is strict"
    );

    let init = MultiFormatRecorder::new_with_payload(
        &config,
        &params,
        "ssh",
        80,
        24,
        SesPayload::Terminal,
    );

    let err = init
        .err()
        .expect("the destination directory does not exist, so init must fail");

    assert!(
        matches!(err, RecordingError::Unrecordable(_)),
        "a strict session whose recorder cannot be created must report Unrecordable so a \
         handler cannot mistake it for an ignorable I/O error; got {err:?}"
    );
}

/// A `.ses` must reach the ZMQ endpoint the gateway bound, byte for byte.
///
/// This is the Windows recording path end to end. There is no FIFO on Windows, so
/// `tunnel_recordings.py:1808-1813` binds a PAIR socket and passes its endpoint in
/// `recordingpath`; the gateway's reader then streams **raw bytes** off that socket
/// (`recv_into` with a fixed `memoryview`), encrypts them and uploads the `.ses`. So the
/// recorder has to put the protocol stream on the socket unmodified -- the existing
/// `zmq_addr` sender is not a substitute, it carries asciicast v2 JSON lines for the
/// separate `-guacr.cast` stream (`tunnel_recordings.py:2018`).
///
/// Feature-gated because the sink is: `zmq-transport` is off by default, and the wheel
/// that ships to Windows turns it on (`build-release-publish-wheels.yml:438`).
#[cfg(feature = "zmq-transport")]
#[test]
fn test_ses_bytes_reach_the_zmq_endpoint_given_in_recording_path() {
    // The gateway binds first and guacr connects, so bind before constructing.
    let ctx = zmq::Context::new();
    let backend = ctx.socket(zmq::PAIR).expect("PAIR socket");
    let socket_path = std::env::temp_dir().join(format!(
        "guacr-ses-zmq-{}-{}.ses",
        std::process::id(),
        line!()
    ));
    let _ = std::fs::remove_file(&socket_path);
    let addr = format!("ipc://{}", socket_path.display());
    backend.bind(&addr).expect("gateway binds the frontend");
    backend
        .set_rcvtimeo(5_000)
        .expect("bounded wait so a missing sink fails instead of hanging");

    // Verbatim shape from tunnel_recordings.py:1812-1814, plus include-keys because the
    // recorded instruction is a key (production enables it).
    let mut params = HashMap::new();
    params.insert("recordingname".to_string(), "pair".to_string());
    params.insert("recordingpath".to_string(), addr.clone());
    params.insert("recordingwriteexisting".to_string(), "true".to_string());
    params.insert("recordingincludekeys".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    let mut recorder = MultiFormatRecorder::new_with_payload(
        &config,
        &params,
        "ssh",
        80,
        24,
        SesPayload::Terminal,
    )
    .expect("an endpoint the gateway has bound is a valid .ses destination");

    recorder
        .record_instruction(
            RecordingDirection::ClientToServer,
            &Bytes::from_static(b"3.key,2.97,1.1;"),
        )
        .expect("recording a keystroke must succeed");
    recorder.finalize().expect("finalize must flush and close");

    // Concatenate every message: the writer buffers, so the split into ZMQ messages is
    // not part of the contract -- the byte stream is.
    let mut received: Vec<u8> = Vec::new();
    while let Ok(msg) = backend.recv_bytes(0) {
        received.extend_from_slice(&msg);
    }
    let _ = std::fs::remove_file(&socket_path);

    assert!(
        received.starts_with(b"5.guacr,8.terminal,1.1;"),
        "the stream must open with TERMINAL_SES_MARKER (ses.rs:51) or the vault dispatches \
         playback to the wrong player; got {:?}",
        String::from_utf8_lossy(&received)
    );
    assert!(
        String::from_utf8_lossy(&received).contains("3.key,"),
        "the recorded keystroke must reach the endpoint; got {:?}",
        String::from_utf8_lossy(&received)
    );
    let events = parse_recording(&received);
    assert_eq!(
        events[1],
        RecordedEvent::Instruction(
            "guacr".into(),
            vec!["terminal-size".into(), "80".into(), "24".into(), "0".into()]
        )
    );
}

/// A strict session whose recording breaks mid-session must be endable.
///
/// The init path already reports [`RecordingError::Unrecordable`]
/// (`multi.rs:91-100`), but nothing covered the far more common case: the recording
/// starts fine and stops working later. The gateway's reader dies, or falls behind far
/// enough to fill the queue, and `writer_thread.rs:171-181` closes that destination. The
/// error the handler sees is an ordinary `Io`, both call sites in `session.rs:74-76` and
/// `:90-92` `warn!` and continue, and the user keeps working with
/// `recording-allow-unrecorded=false` set and a `.ses` truncated at that instant.
///
/// Unix-only for the same reason as `writer_thread_tests`: a regular file does not fail a
/// write, so provoking one needs a FIFO whose reader has gone.
#[cfg(unix)]
#[test]
fn test_strict_session_reports_a_mid_session_write_failure_as_unrecordable() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("midsession.ses");
    let status = std::process::Command::new("mkfifo")
        .arg(&ses_path)
        .status()
        .expect("mkfifo is available on unix");
    assert!(status.success(), "mkfifo {ses_path:?} failed");

    // The gateway's reader: completes the FIFO rendezvous, then goes away. Every write
    // after that fails with EPIPE, which is exactly what a crashed reader looks like.
    let reader_path = ses_path.clone();
    let reader = std::thread::spawn(move || {
        let fifo = std::fs::File::open(&reader_path).expect("read end opens");
        drop(fifo);
    });

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp_dir.path().to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "midsession.ses".to_string());
    params.insert("recording-write-existing".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);
    assert!(
        !config.allow_unrecorded,
        "recording-allow-unrecorded defaults to false, so this session is strict"
    );

    let mut recorder = MultiFormatRecorder::new_with_payload(
        &config,
        &params,
        "ssh",
        80,
        24,
        SesPayload::Terminal,
    )
    .expect("the fifo exists and a reader arrived, so the recorder starts");
    reader.join().expect("reader thread finished");

    // 8 KiB payloads so each instruction clears the BufWriter and reaches the fifo; the
    // failure is asynchronous (the writer thread hits it), so keep recording until it
    // surfaces rather than assuming which call sees it.
    let frame = {
        let payload = [b'x'; 8192];
        let mut bytes = Vec::with_capacity(8 + payload.len());
        bytes.push(guacr_protocol::Opcode::TerminalData as u8);
        bytes.push(0);
        bytes.extend_from_slice(&0u16.to_le_bytes());
        bytes.extend_from_slice(&(payload.len() as u32).to_le_bytes());
        bytes.extend_from_slice(&payload);
        Bytes::from(bytes)
    };

    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(5);
    let mut failure = None;
    while std::time::Instant::now() < deadline {
        match recorder.record_instruction(RecordingDirection::ServerToClient, &frame) {
            Ok(()) => std::thread::yield_now(),
            Err(e) => {
                // Keys are excluded here, so this probes sticky health without enqueueing.
                if recorder.record_input(b"").is_err() {
                    failure = Some(e);
                    break;
                }
            }
        }
    }

    let failure = failure.expect(
        "writes to a fifo whose reader is gone must be reported, not absorbed \
         indefinitely",
    );
    assert!(
        matches!(failure, RecordingError::Unrecordable(_)),
        "a strict session whose recording stopped working must report Unrecordable, or the \
         handler treats it as an ignorable I/O error and the session continues unrecorded; \
         got {failure:?}"
    );
    assert!(
        matches!(
            recorder.record_resize(80, 24),
            Err(RecordingError::Unrecordable(_))
        ),
        "unchanged geometry must still observe required destination failure"
    );
}
