use crate::recorder::{DualFormatRecorder, EventType};
use bytes::Bytes;

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

    // Verify .ses format is raw protocol (not timestamp.direction.instruction)
    let ses_content = std::fs::read_to_string(&ses_path).unwrap();
    for line in ses_content.lines() {
        if line.is_empty() {
            continue;
        }
        assert!(line.ends_with(';'), "Should end with semicolon: {}", line);
        assert!(line.contains('.'), "Should have Guacamole protocol format");
        // Should NOT match the old broken format "TIMESTAMP.DIRECTION.INSTRUCTION"
        let first_char = line.chars().next().unwrap();
        assert!(
            first_char.is_ascii_digit(),
            "Should start with length prefix"
        );
    }

    std::fs::remove_file(cast_path).ok();
    std::fs::remove_file(ses_path).ok();
}
