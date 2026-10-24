use crate::config::RecordingConfig;
use crate::ses::{GuacamoleSesRecorder, RecordingDirection, SesPayload, TERMINAL_SES_MARKER};
use bytes::Bytes;
use guacr_protocol::{format_terminal_data_binary, GuacamoleParser};
use std::io::Read;
use tempfile::TempDir;

/// Split a recording into `(opcode, args)` pairs.
///
/// Doubles as an assertion: a recording is one unbroken byte stream, so the parser
/// finds instruction boundaries from the declared element lengths alone. Any byte
/// between one instruction's `;` and the next one's length prefix is read as part of
/// that prefix and fails here.
fn parse_instructions(content: &str) -> Vec<(String, Vec<String>)> {
    let bytes = Bytes::from(content.to_owned());
    GuacamoleParser::parse_instructions(&bytes)
        .expect("recording should parse as Guacamole protocol")
        .into_iter()
        .map(|instr| {
            (
                instr.opcode.to_string(),
                instr.args.iter().map(|arg| arg.to_string()).collect(),
            )
        })
        .collect()
}

#[derive(Debug, PartialEq)]
pub(super) enum RecordedEvent<'a> {
    Instruction(String, Vec<String>),
    Output(&'a [u8]),
}

pub(super) fn parse_recording(mut bytes: &[u8]) -> Vec<RecordedEvent<'_>> {
    let mut events = Vec::new();
    while !bytes.is_empty() {
        if bytes[0].is_ascii_digit() {
            let instruction = guacr_protocol::StreamingParser::peek_instruction(bytes)
                .expect("recording text must have valid codepoint lengths and boundaries");
            events.push(RecordedEvent::Instruction(
                instruction.opcode.to_string(),
                instruction.args.iter().map(|arg| arg.to_string()).collect(),
            ));
            bytes = &bytes[instruction.total_length_in_buffer..];
        } else {
            assert!(bytes.len() >= 8, "binary frame header must be complete");
            assert_eq!(bytes[0], guacr_protocol::Opcode::TerminalData as u8);
            let length = u32::from_le_bytes(bytes[4..8].try_into().unwrap()) as usize;
            assert!(8 + length <= bytes.len(), "binary payload must be complete");
            events.push(RecordedEvent::Output(&bytes[8..8 + length]));
            bytes = &bytes[8 + length..];
        }
    }
    events
}

fn opcodes(parsed: &[(String, Vec<String>)]) -> Vec<&str> {
    parsed.iter().map(|(opcode, _)| opcode.as_str()).collect()
}

/// The vault has to pick a player before it decodes anything, and for a terminal
/// recording it cannot do that by sniffing byte 0: a text `size` or `name` may precede
/// the first binary frame, so the file can open with an ASCII digit exactly like a guacd
/// one. A marker instruction at a fixed offset makes the test exact.
#[test]
fn test_terminal_ses_opens_with_the_format_marker() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("terminal.ses");

    let config = RecordingConfig::default();
    let mut recorder =
        GuacamoleSesRecorder::new_with_payload(&ses_path, &config, SesPayload::Terminal).unwrap();
    recorder
        .record(
            RecordingDirection::ServerToClient,
            &format_terminal_data_binary(b"output"),
        )
        .unwrap();
    recorder.finalize().unwrap();

    let bytes = std::fs::read(&ses_path).unwrap();
    assert!(
        bytes.starts_with(TERMINAL_SES_MARKER.as_bytes()),
        "the marker has to be at offset 0 for a fixed-prefix check to work"
    );

    // Well-formed Guacamole, so guacenc and guaclog skip it as an unknown opcode
    // (`/* Ignore any unknown instructions */`) instead of failing the parse.
    let (opcode, args) = parse_instructions(TERMINAL_SES_MARKER)
        .into_iter()
        .next()
        .expect("the marker should parse as one instruction");
    assert_eq!(opcode, "guacr");
    assert_eq!(args, ["terminal", "1"]);
}

/// A graphical `.ses` stays byte-for-byte guacd-shaped. The marker is what routes a
/// recording away from `GuacamolePlayer`, so writing one here would send every VNC
/// recording to a player that cannot read it.
#[test]
fn test_guacamole_ses_carries_no_marker() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("graphical.ses");

    let config = RecordingConfig::default();
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();
    recorder
        .record(
            RecordingDirection::ServerToClient,
            &Bytes::from("4.size,1.0,4.1024,3.768;"),
        )
        .unwrap();
    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();
    assert!(!content.contains("guacr"), "unexpected marker: {content:?}");
    assert_eq!(opcodes(&parse_instructions(&content)), ["size"]);
}

#[test]
fn test_recording_direction() {
    assert_eq!(RecordingDirection::ServerToClient as u8, 0);
    assert_eq!(RecordingDirection::ClientToServer as u8, 1);
}

#[test]
fn test_ses_recorder_creates_file() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("test.ses");

    let config = RecordingConfig::default();
    let recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();
    recorder.finalize().unwrap();

    assert!(ses_path.exists());
}

#[test]
fn test_ses_recorder_writes_raw_instruction() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("test.ses");

    let config = RecordingConfig::default();
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Use a non-sync instruction to verify raw pass-through.
    // sync instructions are intentionally rewritten to session-relative
    // timestamps so they are excluded from this raw-passthrough test.
    let instruction = Bytes::from("4.size,1.0,4.1920,4.1080;");
    recorder
        .record(RecordingDirection::ServerToClient, &instruction)
        .unwrap();
    recorder.finalize().unwrap();

    // Read and verify
    let mut content = String::new();
    std::fs::File::open(&ses_path)
        .unwrap()
        .read_to_string(&mut content)
        .unwrap();

    // Format: raw Guacamole protocol instruction (NO timestamp prefix)
    assert!(
        content.contains("4.size,1.0,4.1920,4.1080;"),
        "Should contain raw instruction without timestamp prefix"
    );
    // Should NOT have old format with timestamp prefix
    assert!(
        !content.starts_with("0."),
        "Should NOT start with timestamp prefix"
    );
}

/// guacd writes instructions back to back and nothing between them — a real
/// 48,044-instruction guacd recording contains zero newlines. A separator guacr adds
/// is a byte the format does not define, so a strict reader takes it for the start of
/// the next length prefix and rejects the file.
#[test]
fn test_ses_recording_has_no_separator_between_instructions() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("no-separator.ses");

    let config = RecordingConfig {
        recording_include_keys: true,
        ..Default::default()
    };
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // One instruction down each of the three write paths: raw pass-through, the
    // rewritten server-to-client sync, and timestamp-injected client input.
    for (direction, instruction) in [
        (
            RecordingDirection::ServerToClient,
            "4.size,1.0,4.1024,3.768;",
        ),
        (
            RecordingDirection::ServerToClient,
            "4.sync,13.1234567890123,1.0;",
        ),
        (RecordingDirection::ClientToServer, "3.key,2.65,1.1;"),
        (
            RecordingDirection::ClientToServer,
            "5.mouse,3.100,3.200,1.0;",
        ),
    ] {
        recorder
            .record(direction, &Bytes::from(instruction))
            .unwrap();
    }
    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();
    assert!(
        !content.contains('\n'),
        "recording should carry no bytes between instructions: {content:?}"
    );
    assert_eq!(
        opcodes(&parse_instructions(&content)),
        ["size", "sync", "key", "mouse"]
    );
}

/// Terminal-family handlers record binary opcode frames, and the recording is the only
/// timeline a player has. Those handlers emit `sync` on the 5s keepalive and the 64 KiB
/// flow-control threshold — neither is a frame clock — so without a marker per frame a
/// player replaying by sync deltas dumps up to five seconds of output at once. The
/// marker is written to the recording only and never sent, so it costs nothing on the
/// wire.
#[test]
fn test_binary_output_frames_each_get_a_timing_sync() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("frame-timing.ses");

    let config = RecordingConfig::default();
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    let payloads: [&[u8]; 2] = [b"first frame", b"second frame"];
    for payload in payloads {
        recorder
            .record(
                RecordingDirection::ServerToClient,
                &format_terminal_data_binary(payload),
            )
            .unwrap();
    }
    recorder.finalize().unwrap();

    // Structure: frame, sync, frame, sync — and nothing else.
    let bytes = std::fs::read(&ses_path).unwrap();
    let mut cursor = 0;
    for payload in payloads {
        let frame = format_terminal_data_binary(payload);
        assert_eq!(
            &bytes[cursor..cursor + frame.len()],
            &frame[..],
            "frame should be written byte for byte"
        );
        cursor += frame.len();

        let tail = &bytes[cursor..];
        let end = tail
            .iter()
            .position(|&byte| byte == b';')
            .expect("a timing sync should follow every frame")
            + 1;
        let sync = std::str::from_utf8(&tail[..end]).expect("the sync should be text");
        let (opcode, args) = &parse_instructions(sync)[0];
        assert_eq!(opcode, "sync");
        assert!(
            args[0].parse::<u64>().is_ok(),
            "the sync should carry a session-relative millisecond count, got {:?}",
            args[0]
        );
        cursor += end;
    }
    assert_eq!(
        cursor,
        bytes.len(),
        "recording should hold nothing but frames and their timing syncs"
    );
}

/// `recording_exclude_output` has to filter the terminal family too. Its frames are
/// binary, so classifying them by running `is_drawing_instruction` over a lossy UTF-8
/// view finds no length prefix and matches nothing — the setting was a silent no-op for
/// every terminal protocol. Classification comes from the opcode byte instead.
///
/// The timing sync is dropped along with the frame. Keeping one per excluded frame would
/// publish the exact cadence of every keystroke and every line of output to a recording
/// whose whole point is to hold no session content.
#[test]
fn test_recording_exclude_output_filters_binary_terminal_frames() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("exclude-binary.ses");

    let config = RecordingConfig {
        recording_exclude_output: true,
        ..Default::default()
    };
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    for instruction in [
        format_terminal_data_binary(b"secret output"),
        Bytes::from("4.size,1.0,2.80,2.24;"),
        format_terminal_data_binary(b"more secret output"),
    ] {
        recorder
            .record(RecordingDirection::ServerToClient, &instruction)
            .unwrap();
    }
    recorder.finalize().unwrap();

    let bytes = std::fs::read(&ses_path).unwrap();
    assert!(
        !bytes.windows(6).any(|window| window == b"secret"),
        "terminal output must not survive recording-exclude-output"
    );
    let content = String::from_utf8(bytes).expect("only the kept text instruction remains");
    assert_eq!(opcodes(&parse_instructions(&content)), ["size"]);
}

#[test]
fn test_ses_recorder_records_multiple_instructions() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("test.ses");

    // Enable key recording to test client-to-server direction
    let config = RecordingConfig {
        recording_include_keys: true,
        ..Default::default()
    };

    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Server to client - size instruction
    let instr1 = Bytes::from("4.size,1.0,3.800,3.600;");
    recorder
        .record(RecordingDirection::ServerToClient, &instr1)
        .unwrap();

    // Server to client - sync instruction (provides timing)
    let instr2 = Bytes::from("4.sync,13.1234567890123,1.0;");
    recorder
        .record(RecordingDirection::ServerToClient, &instr2)
        .unwrap();

    // Client to server - key event (with timestamp as per protocol)
    let instr3 = Bytes::from("3.key,2.65,1.1,13.1234567890200;");
    recorder
        .record(RecordingDirection::ClientToServer, &instr3)
        .unwrap();

    recorder.finalize().unwrap();

    let mut content = String::new();
    std::fs::File::open(&ses_path)
        .unwrap()
        .read_to_string(&mut content)
        .unwrap();

    // Verify raw instructions are recorded (Guacamole protocol format)
    assert!(
        content.contains("4.size,1.0,3.800,3.600;"),
        "Should contain size instruction"
    );
    // sync is rewritten to session-relative timestamp — check format only
    assert!(
        content.contains("4.sync,"),
        "Should contain sync instruction (session-relative timestamp)"
    );
    // Key instruction gets a timestamp injected
    assert!(
        content.contains("3.key,2.65,1.1,13.1234567890200"),
        "Should contain key instruction"
    );
}

#[test]
fn test_ses_recorder_filters_keys_by_default() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("test.ses");

    // Default config - keys NOT included (security: don't record passwords)
    let config = RecordingConfig::default();
    assert!(!config.recording_include_keys);

    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Server to client (should be recorded)
    let instr1 = Bytes::from("4.size,1.0,3.800,3.600;");
    recorder
        .record(RecordingDirection::ServerToClient, &instr1)
        .unwrap();

    // Client to server key event (should be FILTERED for security)
    let instr2 = Bytes::from("3.key,2.65,1.1,13.1234567890200;");
    recorder
        .record(RecordingDirection::ClientToServer, &instr2)
        .unwrap();

    recorder.finalize().unwrap();

    let mut content = String::new();
    std::fs::File::open(&ses_path)
        .unwrap()
        .read_to_string(&mut content)
        .unwrap();

    // Only the first instruction should be recorded
    assert!(
        content.contains("4.size,1.0,3.800,3.600;"),
        "Should contain size instruction"
    );
    assert!(
        !content.contains("3.key,"),
        "Should NOT contain key event (filtered for security)"
    );

    assert_eq!(
        opcodes(&parse_instructions(&content)),
        ["size"],
        "Should have exactly 1 recorded instruction (key filtered)"
    );
}

#[test]
fn test_ses_format_compatible_with_guacenc() {
    // Test that output matches what guacenc/guaclog expect
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("session.ses");

    let config = RecordingConfig::default();
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Typical recording instructions
    let instructions = [
        // Size instruction (defines display dimensions)
        Bytes::from("4.size,1.0,4.1024,3.768;"),
        // Name instruction (optional metadata)
        Bytes::from("4.name,1.0,12.Test Session;"),
        // Sync instruction (timing marker - timestamp in milliseconds)
        Bytes::from("4.sync,10.1000000000,1.1;"),
        // Another sync to show time passing
        Bytes::from("4.sync,10.1000000100,1.2;"),
    ];

    for instr in &instructions {
        recorder
            .record(RecordingDirection::ServerToClient, instr)
            .unwrap();
    }
    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();

    // Non-sync instructions should be raw; sync timestamps are rewritten
    // to session-relative values so we only check format, not exact content.
    for instr in &instructions {
        let instr_str = String::from_utf8_lossy(instr);
        if instr_str.starts_with("4.sync,") {
            assert!(
                content.contains("4.sync,"),
                "Recording should contain a sync instruction"
            );
        } else {
            assert!(
                content.contains(instr_str.as_ref()),
                "Recording should contain: {}",
                instr_str
            );
        }
    }

    // Verify the file can be parsed as Guacamole protocol: every instruction is
    // recovered from its length prefixes, in order, with nothing left over.
    assert_eq!(
        opcodes(&parse_instructions(&content)),
        ["size", "name", "sync", "sync"]
    );
}

#[test]
fn test_ses_recording_can_be_parsed() {
    // Verify that recorded .ses files can be parsed back as valid Guacamole protocol
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("parseable.ses");

    let config = RecordingConfig::default();
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Record typical session instructions
    let instructions = vec![
        "4.size,1.0,4.1024,3.768;",
        "4.name,1.0,7.Session;",
        "4.sync,13.1000000000000,1.0;",
        "3.img,1.0,1.2,9.image/png,1.0,1.0;",
        "4.sync,13.1000000100000,1.1;",
    ];

    for instr in &instructions {
        recorder
            .record(RecordingDirection::ServerToClient, &Bytes::from(*instr))
            .unwrap();
    }
    recorder.finalize().unwrap();

    // Parse the file and verify each instruction
    let content = std::fs::read_to_string(&ses_path).unwrap();

    // Every instruction comes back out, in order and with its arguments intact.
    let parsed = parse_instructions(&content);
    assert_eq!(opcodes(&parsed), ["size", "name", "sync", "img", "sync"]);
    for (opcode, args) in &parsed {
        assert!(
            !args.is_empty(),
            "{opcode} should have parsed at least one argument"
        );
    }
}

#[test]
fn test_ses_recording_binary_safe() {
    // Guacamole instructions can contain binary blob data
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("binary.ses");

    let config = RecordingConfig::default();
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Simulate a blob instruction with base64 data (how Guacamole handles binary)
    let blob_instr = "4.blob,1.1,16.SGVsbG8gV29ybGQh;"; // "Hello World!" in base64
    recorder
        .record(RecordingDirection::ServerToClient, &Bytes::from(blob_instr))
        .unwrap();

    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();
    assert!(
        content.contains("SGVsbG8gV29ybGQh"),
        "Base64 data should be preserved"
    );
}

#[test]
fn test_recording_exclude_output_filters_all_drawing() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("exclude-output.ses");

    let config = RecordingConfig {
        recording_exclude_output: true,
        ..Default::default()
    };
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Drawing instructions -- should all be filtered
    let drawing_instrs = vec![
        Bytes::from("3.img,1.0,9.image/png,1.0,1.0;"),
        Bytes::from("4.blob,1.1,16.SGVsbG8gV29ybGQh;"),
        Bytes::from("3.end,1.1;"),
        Bytes::from("4.copy,1.0,1.0,1.0,3.100,3.100,1.1,1.0,1.0;"),
        Bytes::from("4.rect,1.0,1.0,1.0,3.100,3.100;"),
        Bytes::from("5.cfill,1.0,1.0,3.255,1.0,1.0,3.255;"),
        Bytes::from("6.cursor,1.0,1.0,1.0,3.100,3.100,2.10,2.10;"),
        Bytes::from("5.audio,1.0,9.audio/ogg;"),
    ];

    // Non-drawing instructions -- should be kept
    let kept_instrs = vec![
        Bytes::from("4.size,1.0,3.800,3.600;"),
        Bytes::from("4.sync,13.1234567890123,1.0;"),
        Bytes::from("4.name,1.0,7.Session;"),
    ];

    for instr in &drawing_instrs {
        recorder
            .record(RecordingDirection::ServerToClient, instr)
            .unwrap();
    }
    for instr in &kept_instrs {
        recorder
            .record(RecordingDirection::ServerToClient, instr)
            .unwrap();
    }

    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();

    // Should only have the 3 non-drawing instructions
    assert_eq!(
        opcodes(&parse_instructions(&content)),
        ["size", "sync", "name"],
        "Should only have non-drawing instructions"
    );
    assert!(content.contains("4.size,"));
    assert!(content.contains("4.sync,"));
    assert!(content.contains("4.name,"));

    // Drawing instructions should NOT be present
    assert!(!content.contains("3.img,"));
    assert!(!content.contains("4.blob,"));
    assert!(!content.contains("6.cursor,"));
}

/// A `.ses` is replayed as a stream of *server* instructions, so a client instruction that
/// is only valid in the client->server direction must not be copied into it verbatim.
///
/// `size` is exactly that case: the browser sends two arguments, `size,<width>,<height>`
/// (see `display_size_instruction`'s caller in guacr-ssh), while a server `size` is
/// `size,<layer>,<width>,<height>`. Written through unchanged, a player reads the width as
/// the layer index — sizing a nonexistent off-screen buffer and leaving layer 0 at 0x0,
/// which renders as a blank screen for the whole recording. `sync` is already dropped for
/// the same reason; client `size` needs the same treatment.
#[test]
fn test_client_size_is_not_recorded_as_a_server_instruction() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("client_size.ses");

    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &RecordingConfig::default()).unwrap();

    // The server's own geometry, then a browser resize in the client's 2-arg form.
    recorder
        .record(
            RecordingDirection::ServerToClient,
            &Bytes::from("4.size,1.0,4.1012,3.760;"),
        )
        .unwrap();
    recorder
        .record(
            RecordingDirection::ClientToServer,
            &Bytes::from("4.size,4.1062,3.774;"),
        )
        .unwrap();
    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();
    for (opcode, args) in parse_instructions(&content) {
        if opcode == "size" {
            assert_eq!(
                args.len(),
                3,
                "every recorded size must carry (layer, width, height), got {args:?}"
            );
        }
    }
    assert!(
        !content.contains("4.size,4.1062,3.774;"),
        "the client's 2-arg size must not reach the recording: {content:?}"
    );
}

#[test]
fn test_timestamp_injection_on_mouse_key() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("timestamp.ses");

    let config = RecordingConfig {
        recording_include_keys: true,
        ..Default::default()
    };
    let mut recorder = GuacamoleSesRecorder::new(&ses_path, &config).unwrap();

    // Mouse instruction (client-to-server)
    let mouse = Bytes::from("5.mouse,3.100,3.200,1.0;");
    recorder
        .record(RecordingDirection::ClientToServer, &mouse)
        .unwrap();

    // Key instruction (client-to-server)
    let key = Bytes::from("3.key,2.65,1.1;");
    recorder
        .record(RecordingDirection::ClientToServer, &key)
        .unwrap();

    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&ses_path).unwrap();
    let parsed = parse_instructions(&content);
    assert_eq!(opcodes(&parsed), ["mouse", "key"]);

    // Each carries one argument more than it arrived with: the injected timestamp,
    // last, as a session-relative millisecond count.
    let expected_arg_counts = [4, 3];
    for ((opcode, args), expected) in parsed.iter().zip(expected_arg_counts) {
        assert_eq!(
            args.len(),
            expected,
            "{opcode} should have gained a timestamp argument: {args:?}"
        );
        let timestamp = args.last().unwrap();
        assert!(
            timestamp.parse::<u64>().is_ok(),
            "{opcode} timestamp should be numeric: {timestamp:?}"
        );
    }
}
