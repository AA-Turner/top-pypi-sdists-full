use crate::browser_client::{should_restart_screencast, BrowserClient};
use crate::handler::RbiConfig;
use guacr_handlers::RecordingConfig;
use std::collections::HashMap;
use tempfile::TempDir;

#[test]
fn test_browser_client_new() {
    let config = RbiConfig::default();
    let recording_config = RecordingConfig::default();
    let params = HashMap::new();
    let client = BrowserClient::new(1920, 1080, config, &recording_config, &params)
        .expect("BrowserClient::new should succeed");
    assert_eq!(client.width, 1920);
    assert_eq!(client.height, 1080);
}

/// Small throughput wobbles must not restart CDP's screencast — it has no live quality
/// knob, so a restart briefly disrupts the frame stream and isn't worth it below the
/// threshold.
#[test]
fn should_restart_screencast_ignores_small_changes() {
    assert!(
        !should_restart_screencast(50, 55),
        "5-point change: too small"
    );
    assert!(
        !should_restart_screencast(50, 45),
        "5-point drop: too small"
    );
    assert!(!should_restart_screencast(50, 50), "no change at all");
}

/// A change that clears the threshold must trigger a restart, in either direction.
#[test]
fn should_restart_screencast_honours_large_changes() {
    assert!(
        should_restart_screencast(50, 60),
        "10-point rise clears the threshold"
    );
    assert!(
        should_restart_screencast(50, 40),
        "10-point drop clears the threshold"
    );
    assert!(should_restart_screencast(20, 80), "large rise");
}

/// URL allowlist must use host-based matching, not substring matching.
/// Substring matching allows "evil.com/example.com" to bypass an allowlist
/// containing "example.com".
#[test]
fn test_url_allowlist_rejects_path_confusion_bypass() {
    use crate::browser_client::is_url_allowed_for_patterns;

    let patterns = vec!["example.com".to_string()];

    // Legitimate URLs must be allowed
    assert!(
        is_url_allowed_for_patterns("https://example.com/page", &patterns),
        "exact host must be allowed"
    );
    assert!(
        is_url_allowed_for_patterns("https://sub.example.com/", &patterns),
        "subdomain must be allowed (contains pattern)"
    );

    // Path confusion bypass must be rejected
    assert!(
        !is_url_allowed_for_patterns("https://evil.com/example.com/steal", &patterns),
        "path confusion bypass must be rejected: evil.com/example.com matches via contains()"
    );
    assert!(
        !is_url_allowed_for_patterns("https://evil.com?redirect=example.com", &patterns),
        "query string bypass must be rejected"
    );
}

#[test]
fn test_url_allowlist_wildcard_subdomain_matching() {
    use crate::browser_client::is_url_allowed_for_patterns;

    let patterns = vec!["*.example.com".to_string()];

    // Must allow subdomains
    assert!(is_url_allowed_for_patterns(
        "https://sub.example.com/",
        &patterns
    ));
    assert!(is_url_allowed_for_patterns(
        "https://deep.sub.example.com/",
        &patterns
    ));

    // Must NOT allow path-confused URLs
    assert!(
        !is_url_allowed_for_patterns("https://evil.com/sub.example.com", &patterns),
        "path confusion via wildcard must be rejected"
    );
}

// -- Recording tests ---------------------------------------------------------

/// When no recording params are provided, RecordingConfig must report not enabled
/// and BrowserClient::new must succeed (recording is optional).
#[test]
fn test_browser_client_recording_disabled_by_default() {
    let config = RbiConfig::default();
    let recording_config = RecordingConfig::default();
    let params = HashMap::new();
    assert!(
        !recording_config.is_enabled(),
        "default RecordingConfig must not be enabled"
    );
    let client = BrowserClient::new(1920, 1080, config, &recording_config, &params)
        .expect("BrowserClient::new must succeed without recording params");
    assert_eq!(client.width, 1920);
    assert_eq!(client.height, 1080);
}

/// When a valid recording-path is provided, RecordingConfig must report enabled
/// and BrowserClient::new must initialize the recorder without error.
#[test]
fn test_browser_client_recording_initialized_when_params_present() {
    let tmp = TempDir::new().expect("temp dir must be created");
    let config = RbiConfig::default();

    let mut params = HashMap::new();
    params.insert(
        "recording-path".to_string(),
        tmp.path().to_string_lossy().to_string(),
    );
    params.insert("create-recording-path".to_string(), "true".to_string());
    params.insert("recording-write-existing".to_string(), "true".to_string());

    let recording_config = RecordingConfig::from_params(&params);
    assert!(
        recording_config.is_enabled(),
        "RecordingConfig must be enabled when recording-path is set"
    );

    // BrowserClient::new must succeed — recorder is initialized internally.
    let client = BrowserClient::new(1920, 1080, config, &recording_config, &params)
        .expect("BrowserClient::new must succeed with valid recording params");
    assert_eq!(client.width, 1920);
    assert_eq!(client.height, 1080);
    // (recorder field is private; success of ::new confirms initialization)
}
