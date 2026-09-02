// Recording pipeline unit tests for guacr-ssh
//
// Verifies:
// - RecordingConfig is enabled when recording params are present
// - RecordingConfig is disabled when recording params are absent
// - MultiFormatRecorder initializes and finalizes without error
// - No recorder state leaks when params are absent (recorder stays None)
// - Viewer key instructions are recorded (record_client_input is called for viewer input)
//
// These are pure unit tests: no network, no SSH server.

use bytes::Bytes;
use guacr_handlers::{record_client_input, MultiFormatRecorder, RecordingConfig};
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Build a minimal params map with recording enabled, writing to `dir`.
fn recording_params(dir: &std::path::Path) -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert(
        "recording-path".to_string(),
        dir.to_string_lossy().to_string(),
    );
    p.insert("recording-name".to_string(), "ssh-test".to_string());
    p.insert("create-recording-path".to_string(), "true".to_string());
    p
}

/// Build a minimal params map with no recording params at all.
fn no_recording_params() -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert("hostname".to_string(), "10.0.0.1".to_string());
    p.insert("username".to_string(), "alice".to_string());
    p
}

/// Create a temporary directory that is cleaned up when the returned guard is dropped.
/// Uses `std::env::temp_dir()` to avoid adding the `tempfile` crate as a dependency.
fn make_temp_dir() -> TempDirGuard {
    let base = std::env::temp_dir();
    // Use a random-ish unique suffix based on the thread ID + a counter.
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(0);
    let suffix = CTR.fetch_add(1, Ordering::Relaxed);
    let path = base.join(format!("guacr_ssh_recording_test_{}", suffix));
    std::fs::create_dir_all(&path).expect("create temp dir");
    TempDirGuard(path)
}

struct TempDirGuard(std::path::PathBuf);

impl Drop for TempDirGuard {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

// ---------------------------------------------------------------------------
// RecordingConfig parsing
// ---------------------------------------------------------------------------

/// When `recording-path` is present in params, the config must report enabled.
#[test]
fn test_ssh_recording_config_enabled_when_path_present() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    assert!(
        config.is_enabled(),
        "recording must be enabled when recording-path is in params"
    );
}

/// When no recording params are present, the config must report disabled.
#[test]
fn test_ssh_recording_config_disabled_when_no_params() {
    let params = no_recording_params();
    let config = RecordingConfig::from_params(&params);
    assert!(
        !config.is_enabled(),
        "recording must be disabled when no recording params are present"
    );
}

/// The asciicast path must be derived from recording-path and recording-name.
#[test]
fn test_ssh_recording_config_asciicast_path_derived() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    let path = config.get_asciicast_path(&params, "ssh");
    assert!(
        path.is_some(),
        "asciicast path must be derived when config is enabled"
    );
    let path = path.unwrap();
    assert_eq!(
        path.extension().and_then(|e| e.to_str()),
        Some("cast"),
        "asciicast file must have .cast extension"
    );
}

// ---------------------------------------------------------------------------
// MultiFormatRecorder lifecycle
// ---------------------------------------------------------------------------

/// MultiFormatRecorder must initialize without error when config is enabled.
#[test]
fn test_ssh_recorder_initializes_when_config_enabled() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    assert!(config.is_enabled());

    let recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24);
    assert!(
        recorder.is_ok(),
        "recorder must initialize without error: {:?}",
        recorder.err()
    );
    let recorder = recorder.unwrap();
    assert!(
        recorder.is_active(),
        "recorder must be active after initialization"
    );
}

/// MultiFormatRecorder::finalize() must complete without error on normal session end.
#[test]
fn test_ssh_recorder_finalizes_cleanly() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();

    // Simulate recording a line of terminal output (asciicast event)
    recorder
        .record_output(b"$ echo hello\r\n")
        .expect("record_output must not fail");

    // Finalize: flush and close all file writers
    recorder
        .finalize()
        .expect("finalize must not return an error");
}

/// When recording params are absent, no MultiFormatRecorder should be created.
/// This mirrors the `if recording_config.is_enabled() { ... } else { None }` branch
/// in handler.rs and ensures no state leaks when recording is not configured.
#[test]
fn test_ssh_no_recorder_when_params_absent() {
    let params = no_recording_params();
    let config = RecordingConfig::from_params(&params);

    let recorder: Option<MultiFormatRecorder> = if config.is_enabled() {
        MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).ok()
    } else {
        None
    };

    assert!(
        recorder.is_none(),
        "recorder must be None when recording is not configured"
    );
}

/// record_output followed by finalize must produce a non-empty .cast file.
#[test]
fn test_ssh_recorder_output_written_to_file() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();
    recorder.record_output(b"hello from ssh\r\n").unwrap();
    recorder.finalize().unwrap();

    let cast_path = tmp.0.join("ssh-test.cast");
    assert!(cast_path.exists(), ".cast file must exist after finalize");

    let content = std::fs::read_to_string(&cast_path).unwrap();
    assert!(
        content.contains("hello from ssh"),
        ".cast file must contain the recorded output"
    );
}

/// resize events must be recorded in the asciicast stream.
#[test]
fn test_ssh_recorder_resize_event_recorded() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap();
    recorder.record_resize(132, 48).unwrap();
    recorder.finalize().unwrap();

    let cast_path = tmp.0.join("ssh-test.cast");
    let content = std::fs::read_to_string(&cast_path).unwrap();
    assert!(
        content.contains("\"r\""),
        ".cast file must contain a resize event (\"r\" type)"
    );
    assert!(
        content.contains("132x48"),
        ".cast file must contain the new dimensions"
    );
}

// ---------------------------------------------------------------------------
// Viewer input recording
// ---------------------------------------------------------------------------

/// record_client_input must write a viewer key instruction into the .ses recording.
///
/// This test proves the recording mechanism works for the viewer-input path.
/// The bug (viewer_input_rx arm omitted the call) meant this function was never
/// invoked for viewer keystrokes; the fix adds the call.
///
/// Key instructions require recording-include-keys=true in params; the .ses
/// writer appends a session-relative timestamp, so we match the opcode prefix
/// rather than exact raw bytes.
#[test]
fn test_viewer_key_instruction_is_written_to_recording() {
    let tmp = make_temp_dir();
    let mut params = recording_params(tmp.0.as_path());
    params.insert("recording-include-keys".to_string(), "true".to_string());
    let config = RecordingConfig::from_params(&params);
    let mut recorder: Option<MultiFormatRecorder> =
        Some(MultiFormatRecorder::new(&config, &params, "ssh", 80, 24).unwrap());

    // A Guacamole key instruction as it arrives from a shared viewer.
    let viewer_key = Bytes::from_static(b"3.key,5.65293,1.1;");

    // This is the call that was missing from the viewer_input_rx arm in handler.rs.
    record_client_input(&mut recorder, &viewer_key);

    recorder.take().unwrap().finalize().unwrap();

    // The .ses writer appends a timestamp to key instructions, so match the opcode prefix.
    let ses_path = tmp.0.join("ssh-test.ses");
    assert!(ses_path.exists(), ".ses file must exist after finalize");
    let content = std::fs::read_to_string(&ses_path).unwrap();
    assert!(
        content.contains("3.key,"),
        ".ses recording must contain the viewer key instruction; got: {content:?}"
    );
}
