use crate::asciicast::{AsciicastHeader, AsciicastRecorder, EventType};

#[test]
fn test_asciicast_header() {
    let header = AsciicastHeader {
        version: 2,
        width: 80,
        height: 24,
        timestamp: Some(1234567890),
        duration: None,
        idle_time_limit: None,
        command: None,
        title: None,
        env: None,
    };

    let json = serde_json::to_string(&header).unwrap();
    assert!(json.contains("\"version\":2"));
    assert!(json.contains("\"width\":80"));
    assert!(json.contains("\"height\":24"));
}

#[test]
fn test_event_types() {
    assert_eq!(EventType::Output.as_char(), 'o');
    assert_eq!(EventType::Input.as_char(), 'i');
    assert_eq!(EventType::Marker.as_char(), 'm');
    assert_eq!(EventType::Resize.as_char(), 'r');
}

#[test]
fn test_recorder_creates_file_with_header() {
    let tmp_dir = tempfile::TempDir::new().unwrap();
    let path = tmp_dir.path().join("test.cast");

    let mut recorder = AsciicastRecorder::new(&path, 80, 24, None).unwrap();
    recorder.record_output(b"$ ").unwrap();
    recorder.finalize().unwrap();

    assert!(path.exists());
    let content = std::fs::read_to_string(&path).unwrap();
    let lines: Vec<&str> = content.lines().collect();
    assert!(lines.len() >= 2); // Header + 1 event

    // Parse header
    let header: AsciicastHeader = serde_json::from_str(lines[0]).unwrap();
    assert_eq!(header.version, 2);
    assert_eq!(header.width, 80);
    assert_eq!(header.height, 24);

    // Check event
    assert!(lines[1].contains("\"o\""));
}

#[test]
fn test_recorder_resize() {
    let tmp_dir = tempfile::TempDir::new().unwrap();
    let path = tmp_dir.path().join("resize.cast");

    let mut recorder = AsciicastRecorder::new(&path, 80, 24, None).unwrap();
    recorder.record_resize(100, 30).unwrap();
    recorder.finalize().unwrap();

    let content = std::fs::read_to_string(&path).unwrap();
    assert!(content.contains("\"r\""));
    assert!(content.contains("100x30"));
}
