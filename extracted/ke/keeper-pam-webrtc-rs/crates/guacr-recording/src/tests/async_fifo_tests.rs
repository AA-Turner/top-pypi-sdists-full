use crate::{MultiFormatRecorder, RecordingConfig, RecordingDirection, RecordingError, SesPayload};
use bytes::Bytes;
use std::collections::HashMap;
use std::io::Read;
use std::os::unix::fs::FileTypeExt;
use std::time::{Duration, Instant};
use tempfile::TempDir;

fn fixture(dir: &TempDir) -> (RecordingConfig, HashMap<String, String>) {
    let config = RecordingConfig {
        recording_path: Some(dir.path().to_string_lossy().into_owned()),
        recording_name: "session.ses".into(),
        ..Default::default()
    };
    (config, HashMap::new())
}

fn fifo(path: &std::path::Path) {
    assert!(std::process::Command::new("mkfifo")
        .arg(path)
        .status()
        .expect("mkfifo available")
        .success());
}

#[tokio::test(flavor = "current_thread")]
async fn strict_admission_fails_when_fifo_has_no_reader() {
    // Given: a configured .ses FIFO without a reader and overwrite disabled.
    let dir = TempDir::new().unwrap();
    let path = dir.path().join("session.ses");
    fifo(&path);
    let (config, params) = fixture(&dir);
    let began = Instant::now();

    // When: admission waits through a short test deadline on a single Tokio worker.
    let result = tokio::time::timeout(
        Duration::from_secs(2),
        MultiFormatRecorder::new_with_payload_async_for(
            &config,
            &params,
            "ssh",
            80,
            24,
            SesPayload::Terminal,
            Duration::from_millis(120),
        ),
    )
    .await
    .expect("Tokio worker remains responsive");

    // Then: strict admission fails at the deadline without replacing the FIFO or making a sibling.
    assert!(matches!(result, Err(RecordingError::Unrecordable(_))));
    assert!(began.elapsed() < Duration::from_secs(2));
    assert!(std::fs::metadata(&path).unwrap().file_type().is_fifo());
    assert!(!dir.path().join("session.ses.1").exists());
}

#[tokio::test(flavor = "current_thread")]
async fn late_reader_receives_real_ses_bytes() {
    // Given: a FIFO with no reader until after recorder admission begins.
    let dir = TempDir::new().unwrap();
    let path = dir.path().join("session.ses");
    fifo(&path);
    let (config, params) = fixture(&dir);
    let reader = std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(80));
        let mut bytes = Vec::new();
        std::fs::File::open(path)
            .unwrap()
            .read_to_end(&mut bytes)
            .unwrap();
        bytes
    });

    // When: the reader arrives before the admission deadline and a frame is recorded.
    let mut recorder = MultiFormatRecorder::new_with_payload_async_for(
        &config,
        &params,
        "ssh",
        80,
        24,
        SesPayload::Terminal,
        Duration::from_secs(2),
    )
    .await
    .unwrap();
    recorder
        .record_instruction(
            RecordingDirection::ServerToClient,
            &Bytes::from_static(b"4.size,1.0,2.80,2.24;"),
        )
        .unwrap();
    recorder.finalize().unwrap();

    // Then: the FIFO receives the marker and the recorded frame, with no substituted file.
    let bytes = reader.join().unwrap();
    assert!(bytes.starts_with(b"5.guacr,8.terminal,1.1;"));
    assert!(bytes
        .windows(b"4.size,1.0,2.80,2.24;".len())
        .any(|s| s == b"4.size,1.0,2.80,2.24;"));
    assert!(!dir.path().join("session.ses.1").exists());
}

#[tokio::test(flavor = "current_thread")]
async fn optional_admission_returns_advisory_failure_for_unread_fifo() {
    // Given: optional recording with an unread .ses FIFO.
    let dir = TempDir::new().unwrap();
    fifo(&dir.path().join("session.ses"));
    let (mut config, params) = fixture(&dir);
    config.allow_unrecorded = true;

    // When: the FIFO cannot be opened by the deadline.
    let result = MultiFormatRecorder::new_with_payload_async_for(
        &config,
        &params,
        "ssh",
        80,
        24,
        SesPayload::Terminal,
        Duration::from_millis(100),
    )
    .await;

    // Then: callers can continue without a recorder, but cannot mistake one for live.
    assert!(matches!(result, Err(RecordingError::Io(_))));
}

#[tokio::test(flavor = "current_thread")]
async fn ordinary_files_keep_ses_and_typescript_output() {
    // Given: ordinary paths with no FIFO.
    let dir = TempDir::new().unwrap();
    let (mut config, params) = fixture(&dir);
    config.typescript_path = config.recording_path.clone();
    config.typescript_name = "session.tys".into();

    // When: a recorder opens files and records terminal output.
    let mut recorder = MultiFormatRecorder::new_with_payload_async_for(
        &config,
        &params,
        "ssh",
        80,
        24,
        SesPayload::Terminal,
        Duration::from_millis(100),
    )
    .await
    .unwrap();
    recorder.record_output(b"ordinary output").unwrap();
    recorder.finalize().unwrap();

    // Then: existing file outputs and the appended timing name remain functional.
    assert!(std::fs::read(dir.path().join("session.ses"))
        .unwrap()
        .starts_with(b"5.guacr"));
    assert!(std::fs::read_to_string(dir.path().join("session.tys"))
        .unwrap()
        .contains("ordinary output"));
    assert!(dir.path().join("session.tys.timing").exists());
}

#[tokio::test(flavor = "current_thread")]
async fn timing_fifo_without_reader_prevents_admission() {
    // Given: a writable typescript file but an unread companion timing FIFO.
    let dir = TempDir::new().unwrap();
    let config = RecordingConfig {
        typescript_path: Some(dir.path().to_string_lossy().into_owned()),
        typescript_name: "session.tys".into(),
        ..Default::default()
    };
    let path = dir.path().join("session.tys.timing");
    fifo(&path);

    // When: the async constructor attempts both typescript destinations.
    let result = MultiFormatRecorder::new_with_payload_async_for(
        &config,
        &HashMap::new(),
        "ssh",
        80,
        24,
        SesPayload::Terminal,
        Duration::from_millis(100),
    )
    .await;

    // Then: the unopened timing FIFO prevents a usable recorder, even though the main file opened.
    assert!(matches!(result, Err(RecordingError::Unrecordable(_))));
    assert!(std::fs::metadata(path).unwrap().file_type().is_fifo());
}
