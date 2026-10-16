use crate::recorder::{DualFormatRecorder, EventType};
use bytes::Bytes;
use guacr_protocol::GuacamoleParser;

#[test]
fn test_event_types() {
    assert_eq!(EventType::Output.as_char(), 'o');
    assert_eq!(EventType::Input.as_char(), 'i');
    assert_eq!(EventType::Marker.as_char(), 'm');
    assert_eq!(EventType::Resize.as_char(), 'r');
}

#[test]
fn test_dual_format_creates_files() {
    let temp_dir = std::env::temp_dir();
    let cast_path = temp_dir.join("guacr-term-test-dual.cast");
    let ses_path = temp_dir.join("guacr-term-test-dual.ses");

    let mut recorder =
        DualFormatRecorder::new(Some(&cast_path), Some(&ses_path), 80, 24, None).unwrap();

    recorder.record_output(b"$ ").unwrap();
    recorder
        .record_server_to_client(&Bytes::from("4.size,1.0,2.80,2.24;"))
        .unwrap();

    recorder.finalize().unwrap();

    assert!(cast_path.exists());
    assert!(ses_path.exists());

    // Verify .ses format is raw protocol (not timestamp.direction.instruction).
    // Instructions are written back to back with nothing between them, so parsing
    // by length prefix is the only way to recover them — and any stray separator or
    // timestamp prefix fails the parse.
    let ses_content = Bytes::from(std::fs::read(&ses_path).unwrap());
    let instructions = GuacamoleParser::parse_instructions(&ses_content)
        .expect("recording should parse as Guacamole protocol");
    let opcodes: Vec<&str> = instructions.iter().map(|instr| instr.opcode).collect();
    assert_eq!(opcodes, ["size"]);

    std::fs::remove_file(cast_path).ok();
    std::fs::remove_file(ses_path).ok();
}
