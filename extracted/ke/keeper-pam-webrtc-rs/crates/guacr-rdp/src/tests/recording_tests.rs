// Recording pipeline unit tests for guacr-rdp
//
// Verifies:
// - RecordingConfig is enabled when recording params are present
// - RecordingConfig is disabled when recording params are absent
// - RdpSettings.recording_config reflects the parsed params
// - MultiFormatRecorder initializes and finalizes without error
// - No recorder state leaks when params are absent (recorder stays None)
//
// These are pure unit tests: no network, no RDP server.

use crate::handler::{RdpConfig, RdpSettings};
use guacr_handlers::{MultiFormatRecorder, RecordingConfig};
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

fn recording_params(dir: &std::path::Path) -> HashMap<String, String> {
    let mut p = base_rdp_params();
    p.insert(
        "recording-path".to_string(),
        dir.to_string_lossy().to_string(),
    );
    p.insert("recording-name".to_string(), "rdp-test".to_string());
    p.insert("create-recording-path".to_string(), "true".to_string());
    p
}

fn base_rdp_params() -> HashMap<String, String> {
    let mut p = HashMap::new();
    p.insert("hostname".to_string(), "10.0.0.1".to_string());
    p.insert("username".to_string(), "Administrator".to_string());
    p.insert("password".to_string(), "pass".to_string());
    p
}

fn make_temp_dir() -> TempDirGuard {
    let base = std::env::temp_dir();
    use std::sync::atomic::{AtomicU64, Ordering};
    static CTR: AtomicU64 = AtomicU64::new(0);
    let suffix = CTR.fetch_add(1, Ordering::Relaxed);
    let path = base.join(format!("guacr_rdp_recording_test_{}", suffix));
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
// RecordingConfig parsing via standalone RecordingConfig::from_params
// ---------------------------------------------------------------------------

#[test]
fn test_rdp_recording_config_enabled_when_path_present() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    assert!(
        config.is_enabled(),
        "recording must be enabled when recording-path is in params"
    );
}

#[test]
fn test_rdp_recording_config_disabled_when_no_params() {
    let params = base_rdp_params();
    let config = RecordingConfig::from_params(&params);
    assert!(
        !config.is_enabled(),
        "recording must be disabled when no recording params are present"
    );
}

// ---------------------------------------------------------------------------
// RdpSettings.recording_config reflects the params
// ---------------------------------------------------------------------------

/// When recording-path is in params, RdpSettings.recording_config must report enabled.
#[test]
fn test_rdp_settings_recording_config_enabled_when_path_present() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.recording_config.is_enabled(),
        "RdpSettings.recording_config must be enabled when recording-path is in params"
    );
}

/// When no recording params are present, RdpSettings.recording_config must report disabled.
#[test]
fn test_rdp_settings_recording_config_disabled_when_no_recording_params() {
    let params = base_rdp_params();
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        !settings.recording_config.is_enabled(),
        "RdpSettings.recording_config must be disabled when no recording params are present"
    );
}

// ---------------------------------------------------------------------------
// MultiFormatRecorder lifecycle
// ---------------------------------------------------------------------------

#[test]
fn test_rdp_recorder_initializes_when_config_enabled() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);
    assert!(config.is_enabled());

    // RDP uses 1920×1080 as the session dimensions in the recording header.
    let recorder = MultiFormatRecorder::new(&config, &params, "rdp", 1920, 1080);
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
fn test_rdp_recorder_finalizes_cleanly() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let recorder = MultiFormatRecorder::new(&config, &params, "rdp", 1920, 1080).unwrap();
    // RDP is a graphical protocol; record_output is used for .ses instruction recording.
    // finalize() must flush and close all writers cleanly.
    recorder
        .finalize()
        .expect("finalize must not return an error");
}

#[test]
fn test_rdp_no_recorder_when_params_absent() {
    let params = base_rdp_params();
    let config = RecordingConfig::from_params(&params);

    let recorder: Option<MultiFormatRecorder> = if config.is_enabled() {
        MultiFormatRecorder::new(&config, &params, "rdp", 1920, 1080).ok()
    } else {
        None
    };

    assert!(
        recorder.is_none(),
        "recorder must be None when recording is not configured"
    );
}

/// finalize() after recording .ses instructions must produce a .cast file.
#[test]
fn test_rdp_recorder_cast_file_created_on_finalize() {
    let tmp = make_temp_dir();
    let params = recording_params(tmp.0.as_path());
    let config = RecordingConfig::from_params(&params);

    let recorder = MultiFormatRecorder::new(&config, &params, "rdp", 1920, 1080).unwrap();
    recorder.finalize().unwrap();

    // The asciicast path must exist (empty body, just header)
    let cast_path = tmp.0.join("rdp-test.cast");
    assert!(cast_path.exists(), ".cast file must exist after finalize");
}
