// Recording pipeline unit tests for guacr-telnet
//
// Verifies:
// - RecordingConfig is enabled when recording params are present
// - RecordingConfig is disabled when recording params are absent
// - MultiFormatRecorder initializes and finalizes without error
// - No recorder state leaks when params are absent (recorder stays None)
//
// These are pure unit tests: no network, no Telnet server.

use guacr_handlers::{MultiFormatRecorder, RecordingConfig};
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

fn recording_params(dir: &std::path::Path) -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert(
        "recording-path".to_string(),
        dir.to_string_lossy().to_string(),
    );
    p.insert("recording-name".to_string(), "telnet-test".to_string());
    p.insert("create-recording-path".to_string(), "true".to_string());
    p
}

fn no_recording_params() -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert("hostname".to_string(), "10.0.0.1".to_string());
    p
}

fn make_temp_dir() -> TempDirGuard {
    let base = std::env::temp_dir();
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(0);
    let suffix = CTR.fetch_add(1, Ordering::Relaxed);
    let path = base.join(format!("guacr_telnet_recording_test_{}", suffix));
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

#[test]
fn test_telnet_recording_config_enabled_when_path_present() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    assert!(
        config.is_enabled(),
        "recording must be enabled when recording-path is in params"
    );
}

#[test]
fn test_telnet_recording_config_disabled_when_no_params() {
    let params = no_recording_params();
    let config = RecordingConfig::from_params(&params);
    assert!(
        !config.is_enabled(),
        "recording must be disabled when no recording params are present"
    );
}

// ---------------------------------------------------------------------------
// MultiFormatRecorder lifecycle
// ---------------------------------------------------------------------------

#[test]
fn test_telnet_recorder_initializes_when_config_enabled() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    assert!(config.is_enabled());

    let recorder = MultiFormatRecorder::new(&config, &params, "telnet", 80, 24);
    assert!(
        recorder.is_ok(),
        "recorder must initialize without error: {:?}",
        recorder.err()
    );
    assert!(
        recorder.unwrap().is_active(),
        "recorder must be active after initialization"
    );
}

#[test]
fn test_telnet_recorder_finalizes_cleanly() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let mut recorder = MultiFormatRecorder::new(&config, &params, "telnet", 80, 24).unwrap();
    recorder
        .record_output(b"Connected to 10.0.0.1\r\n")
        .expect("record_output must not fail");
    recorder
        .finalize()
        .expect("finalize must not return an error");
}

#[test]
fn test_telnet_no_recorder_when_params_absent() {
    let params = no_recording_params();
    let config = RecordingConfig::from_params(&params);

    let recorder: Option<MultiFormatRecorder> = if config.is_enabled() {
        MultiFormatRecorder::new(&config, &params, "telnet", 80, 24).ok()
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
fn test_telnet_recorder_output_written_to_file() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let mut recorder = MultiFormatRecorder::new(&config, &params, "telnet", 80, 24).unwrap();
    recorder.record_output(b"telnet session data\r\n").unwrap();
    recorder.finalize().unwrap();

    let cast_path = tmp.0.join("telnet-test.cast");
    assert!(cast_path.exists(), ".cast file must exist after finalize");

    let content = std::fs::read_to_string(&cast_path).unwrap();
    assert!(
        content.contains("telnet session data"),
        ".cast file must contain the recorded output"
    );
}

/// Drop-based finalization must not double-finalize or panic when files are
/// already written by an explicit finalize() call. The Drop impl is the safety
/// net for abnormal session termination (panic, early return, error path).
#[test]
fn test_telnet_recorder_drop_after_finalize_is_safe() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let mut recorder = MultiFormatRecorder::new(&config, &params, "telnet", 80, 24).unwrap();
    recorder.record_output(b"data\r\n").unwrap();
    // Explicit finalize: takes the internal writers, leaving None behind.
    recorder.finalize().unwrap();
    // recorder drops here — Drop impl must see all writers as None and skip the
    // finalize_internal call. No double-write, no panic.
}
