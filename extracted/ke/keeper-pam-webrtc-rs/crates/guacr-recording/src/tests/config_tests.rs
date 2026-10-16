use crate::config::{find_unique_path, RecordingConfig, RecordingFormat};
use std::collections::HashMap;

#[test]
fn test_recording_config_default() {
    let config = RecordingConfig::default();
    assert!(!config.is_enabled());
    assert_eq!(config.recording_name, "recording");
    assert!(!config.recording_include_keys);
}

#[test]
fn test_recording_config_from_params() {
    let mut params = HashMap::new();
    params.insert("recording-path".to_string(), "/tmp/recordings".to_string());
    params.insert(
        "recording-name".to_string(),
        "session-${GUAC_DATE}".to_string(),
    );
    params.insert("recording-include-keys".to_string(), "true".to_string());
    params.insert("create-recording-path".to_string(), "1".to_string());

    let config = RecordingConfig::from_params(&params);

    assert!(config.is_enabled());
    assert!(config.is_ses_enabled());
    assert_eq!(config.recording_path, Some("/tmp/recordings".to_string()));
    assert!(config.recording_include_keys);
    assert!(config.create_recording_path);
}

#[test]
fn test_param_normalization_recordingpath() {
    // Python gateway sends "recordingpath" (no hyphens)
    let mut params = HashMap::new();
    params.insert("recordingpath".to_string(), "/tmp/recordings".to_string());
    params.insert("recordingname".to_string(), "test-session".to_string());
    params.insert("createrecordingpath".to_string(), "true".to_string());

    let config = RecordingConfig::from_params(&params);

    assert!(config.is_enabled());
    assert_eq!(config.recording_path, Some("/tmp/recordings".to_string()));
    assert_eq!(config.recording_name, "test-session");
    assert!(config.create_recording_path);
}

#[test]
fn test_no_double_ses_extension() {
    // Python gateway appends .ses to the name
    let mut params = HashMap::new();
    params.insert("recording-path".to_string(), "/recordings".to_string());
    params.insert("recording-name".to_string(), "session.ses".to_string());

    let config = RecordingConfig::from_params(&params);
    let ses_path = config.get_ses_path(&params, "ssh");

    // Should NOT produce "session.ses.ses"
    assert_eq!(
        ses_path,
        Some(std::path::PathBuf::from("/recordings/session.ses"))
    );
}

#[test]
fn test_no_double_cast_extension() {
    let mut params = HashMap::new();
    params.insert("recording-path".to_string(), "/recordings".to_string());
    params.insert("recording-name".to_string(), "session.ses".to_string());

    let config = RecordingConfig::from_params(&params);
    let cast_path = config.get_asciicast_path(&params, "ssh");

    // Should produce "session.cast" not "session.ses.cast"
    assert_eq!(
        cast_path,
        Some(std::path::PathBuf::from("/recordings/session.cast"))
    );
}

#[test]
fn test_unique_path_base_does_not_exist() {
    let tmp = std::env::temp_dir().join("guacr-recording-test-unique-nonexist.ses");
    // Clean up in case of leftover
    let _ = std::fs::remove_file(&tmp);

    let result = find_unique_path(&tmp, 255);
    assert_eq!(result, Some(tmp));
}

#[test]
fn test_unique_path_with_existing_file() {
    let tmp_dir = tempfile::TempDir::new().unwrap();
    let base = tmp_dir.path().join("test.ses");
    std::fs::File::create(&base).unwrap();

    let result = find_unique_path(&base, 255);
    assert_eq!(result, Some(tmp_dir.path().join("test.ses.1")));
}

#[test]
fn test_filename_expansion() {
    let mut params = HashMap::new();
    params.insert("username".to_string(), "testuser".to_string());
    params.insert("hostname".to_string(), "server.example.com".to_string());

    let template = "${GUAC_USERNAME}-${GUAC_HOSTNAME}-${GUAC_PROTOCOL}";
    let result = RecordingConfig::expand_filename(template, &params, "ssh");

    assert_eq!(result, "testuser-server.example.com-ssh");
}

#[test]
fn test_recording_format_extension() {
    assert_eq!(RecordingFormat::GuacamoleSes.extension(), "ses");
    assert_eq!(RecordingFormat::Asciicast.extension(), "cast");
    assert_eq!(RecordingFormat::Typescript.extension(), "typescript");
}

#[test]
fn test_get_recording_paths() {
    let mut params = HashMap::new();
    params.insert("recording-path".to_string(), "/recordings".to_string());
    params.insert("recording-name".to_string(), "session".to_string());

    let config = RecordingConfig::from_params(&params);

    let ses_path = config.get_ses_path(&params, "ssh");
    assert_eq!(
        ses_path,
        Some(std::path::PathBuf::from("/recordings/session.ses"))
    );

    let cast_path = config.get_asciicast_path(&params, "ssh");
    assert_eq!(
        cast_path,
        Some(std::path::PathBuf::from("/recordings/session.cast"))
    );
}

#[test]
fn test_recording_path_with_template() {
    let mut params = HashMap::new();
    params.insert("recording-path".to_string(), "/recordings".to_string());
    params.insert(
        "recording-name".to_string(),
        "${GUAC_USERNAME}-${GUAC_HOSTNAME}".to_string(),
    );
    params.insert("username".to_string(), "admin".to_string());
    params.insert("hostname".to_string(), "server1".to_string());

    let config = RecordingConfig::from_params(&params);

    let ses_path = config.get_ses_path(&params, "ssh");
    assert_eq!(
        ses_path,
        Some(std::path::PathBuf::from("/recordings/admin-server1.ses"))
    );
}

#[test]
fn test_recording_enabled_flag_false_disables() {
    let mut params = HashMap::new();
    params.insert("recording-path".to_string(), "/recordings".to_string());
    params.insert("recording-enabled".to_string(), "false".to_string());

    let config = RecordingConfig::from_params(&params);
    assert!(!config.is_enabled());
    assert!(config.recording_path.is_none());
}

/// A username or hostname containing path traversal components (../) must not
/// be allowed to escape the recording directory when expanded into the filename.
#[test]
fn test_expand_filename_sanitizes_path_traversal_in_username() {
    use crate::config::RecordingConfig;

    let mut params = std::collections::HashMap::new();
    params.insert("username".to_string(), "../../etc/passwd".to_string());
    params.insert("hostname".to_string(), "server".to_string());

    let result =
        RecordingConfig::expand_filename("${GUAC_USERNAME}-${GUAC_HOSTNAME}.ses", &params, "ssh");

    assert!(
        !result.contains(".."),
        "path traversal in username must be removed from filename; got: {result:?}"
    );
    assert!(
        !result.contains('/'),
        "slashes in username must be removed from filename; got: {result:?}"
    );
}

#[test]
fn test_expand_filename_sanitizes_path_traversal_in_hostname() {
    use crate::config::RecordingConfig;

    let mut params = std::collections::HashMap::new();
    params.insert("username".to_string(), "user".to_string());
    params.insert("hostname".to_string(), "../../../evil".to_string());

    let result =
        RecordingConfig::expand_filename("${GUAC_USERNAME}@${GUAC_HOSTNAME}.ses", &params, "ssh");

    assert!(
        !result.contains(".."),
        "path traversal in hostname must be removed; got: {result:?}"
    );
}

/// The input policy the text recorder enforces, in one reusable predicate so the fMP4
/// data track cannot drift from it.
#[test]
fn test_records_input_opcode_matches_the_ses_policy() {
    use crate::config::RecordingConfig;

    let default_config = RecordingConfig::default();
    assert!(
        !default_config.records_input_opcode("key"),
        "keys are excluded by default because they carry passwords"
    );
    assert!(default_config.records_input_opcode("mouse"));
    assert!(default_config.records_input_opcode("size"));

    let config = RecordingConfig {
        recording_include_keys: true,
        recording_exclude_mouse: true,
        ..RecordingConfig::default()
    };
    assert!(config.records_input_opcode("key"));
    assert!(!config.records_input_opcode("mouse"));
}

/// The Windows gateway hands guacr a ZMQ endpoint in `recordingpath`.
///
/// tunnel_recordings.py:1812-1813 (dr-controller) sets, under WINOS with ZMQ available:
///   recordingname = ZEROMQ_RECORDING_SOCKET_TYPE  ("pair")
///   recordingpath = "ipc://<tmp>/<stamp>.ses"
/// That branch is gated on WINOS only -- not on use_guacr -- so a guacr session on a
/// Windows gateway receives it. `from_params` does no scheme inspection, so the endpoint
/// is treated as a directory and the socket-type string becomes the filename.
///
/// Windows has no FIFO, so there is no filesystem destination to fall back to: an
/// endpoint must not yield a path of any shape, `.ses` or `.cast`.
fn windows_zmq_params() -> HashMap<String, String> {
    let mut params = HashMap::new();
    // Verbatim shape from tunnel_recordings.py:1812-1814.
    params.insert("recordingname".to_string(), "pair".to_string());
    params.insert(
        "recordingpath".to_string(),
        "ipc:///tmp/keeper/2026-09-17_12-00-00-abcd.ses".to_string(),
    );
    params.insert("recordingwriteexisting".to_string(), "true".to_string());
    params
}

#[test]
fn test_windows_zmq_endpoint_in_recording_path_is_not_treated_as_a_directory() {
    let params = windows_zmq_params();
    let config = RecordingConfig::from_params(&params);

    assert_eq!(
        config.get_ses_path(&params, "ssh"),
        None,
        "a ZMQ endpoint must not become a filesystem path"
    );
    assert_eq!(
        config.get_asciicast_path(&params, "ssh"),
        None,
        "the asciicast path falls back to recording_path, so an endpoint must not leak \
         into it either"
    );
}

/// Routing the endpoint away from `recording_path` must not switch recording off.
///
/// The naive fix -- drop a value that does not look like a directory -- makes
/// `is_enabled()` false, and `guacr-database/src/recording.rs:25-27` then returns
/// `Ok(None)`: no recorder, no error, session proceeds unrecorded. That is the bug this
/// work exists to remove, so the endpoint has to remain a live `.ses` destination.
#[test]
fn test_windows_zmq_endpoint_still_counts_as_ses_recording_enabled() {
    let config = RecordingConfig::from_params(&windows_zmq_params());

    assert!(
        config.is_enabled(),
        "recording was requested; an endpoint destination still counts as enabled"
    );
    assert!(
        config.is_ses_enabled(),
        "the endpoint is where the .ses goes, so .ses recording is enabled"
    );
    assert_eq!(
        config.ses_zmq_addr.as_deref(),
        Some("ipc:///tmp/keeper/2026-09-17_12-00-00-abcd.ses"),
        "the endpoint must be preserved verbatim -- the gateway bound this exact string \
         (tunnel_recordings.py:1810-1811), so any rewriting of it fails to connect"
    );
    assert_eq!(
        config.recording_path, None,
        "an endpoint is not a directory"
    );
}

/// The Linux/FIFO shape must keep resolving to a file, not an endpoint.
#[test]
fn test_posix_recording_path_still_resolves_to_a_file() {
    let mut params = HashMap::new();
    params.insert(
        "recordingname".to_string(),
        "2026-09-17_12-00.ses".to_string(),
    );
    params.insert("recordingpath".to_string(), "/tmp/keeper/pipes".to_string());

    let config = RecordingConfig::from_params(&params);

    assert_eq!(
        config.get_ses_path(&params, "ssh"),
        Some(std::path::PathBuf::from(
            "/tmp/keeper/pipes/2026-09-17_12-00.ses"
        )),
        "a plain directory must still produce a filesystem destination"
    );
}
