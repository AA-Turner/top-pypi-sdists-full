use crate::recording::MultiFormatRecorder;
use crate::session::{
    record_client_input, record_server_output, send_and_record, send_bell, send_disconnect,
    send_msg_best_effort, send_name, send_ready,
};
use bytes::Bytes;
use tokio::sync::mpsc;

#[tokio::test]
async fn test_send_ready() {
    let (tx, mut rx) = mpsc::channel(16);
    send_ready(&tx, "ssh-ready").await.unwrap();
    let msg = rx.recv().await.unwrap();
    let s = String::from_utf8(msg.to_vec()).unwrap();
    assert_eq!(s, "5.ready,9.ssh-ready;");
}

#[tokio::test]
async fn test_send_name() {
    let (tx, mut rx) = mpsc::channel(16);
    send_name(&tx, "SSH").await.unwrap();
    let msg = rx.recv().await.unwrap();
    let s = String::from_utf8(msg.to_vec()).unwrap();
    assert_eq!(s, "4.name,3.SSH;");
}

#[tokio::test]
async fn test_send_disconnect() {
    let (tx, mut rx) = mpsc::channel(16);
    send_disconnect(&tx).await;
    let msg = rx.recv().await.unwrap();
    let s = String::from_utf8(msg.to_vec()).unwrap();
    assert_eq!(s, "10.disconnect;");
}

#[tokio::test]
async fn test_send_bell() {
    let (tx, mut rx) = mpsc::channel(16);
    send_bell(&tx, 100).await.unwrap();
    // Should produce 3 instructions: audio, blob, end
    let audio = rx.recv().await.unwrap();
    let blob = rx.recv().await.unwrap();
    let end = rx.recv().await.unwrap();
    let audio_s = String::from_utf8(audio.to_vec()).unwrap();
    let end_s = String::from_utf8(end.to_vec()).unwrap();
    assert!(audio_s.contains("audio"));
    assert!(audio_s.contains("audio/wav"));
    let blob_s = String::from_utf8(blob.to_vec()).unwrap();
    assert!(blob_s.contains("blob"));
    assert!(end_s.contains("end"));
}

#[tokio::test]
async fn test_send_ready_closed_channel() {
    let (tx, rx) = mpsc::channel(16);
    drop(rx);
    let result = send_ready(&tx, "test").await;
    assert!(result.is_err());
}

#[tokio::test]
async fn test_send_disconnect_closed_channel() {
    let (tx, rx) = mpsc::channel(16);
    drop(rx);
    // Should not panic, just log debug
    send_disconnect(&tx).await;
}

#[tokio::test]
async fn test_send_and_record_without_recorder() {
    let (tx, mut rx) = mpsc::channel(16);
    let mut recorder: Option<MultiFormatRecorder> = None;
    let instr = Bytes::from("5.ready,4.test;");
    send_and_record(&tx, &mut recorder, instr).await.unwrap();
    let msg = rx.recv().await.unwrap();
    assert_eq!(&msg[..], b"5.ready,4.test;");
}

#[tokio::test]
async fn test_send_and_record_closed_channel() {
    let (tx, rx) = mpsc::channel(16);
    drop(rx);
    let mut recorder: Option<MultiFormatRecorder> = None;
    let result = send_and_record(&tx, &mut recorder, Bytes::from("test")).await;
    assert!(result.is_err());
}

#[test]
fn test_record_client_input_without_recorder() {
    let mut recorder: Option<MultiFormatRecorder> = None;
    // Should not panic when recorder is None, and no recorder is not a recording failure
    record_client_input(&mut recorder, &Bytes::from("3.key,1.1,5.65536;"))
        .expect("a session with recording disabled is not a session that failed to record");
}

// ---------------------------------------------------------------------------
// Strict recording: a session that must not continue unrecorded
//
// `recording-allow-unrecorded=false` (the default) is the operator saying no recording,
// no session. `MultiFormatRecorder` reports that condition as
// `RecordingError::Unrecordable`; these two functions are the only places a handler
// touches the recorder mid-session, so they are where it has to stop being a log line.
//
// Unix-only: provoking a real write failure needs a FIFO whose reader has gone, which is
// also the production failure (the gateway mkfifos the path and reads the other end).
// ---------------------------------------------------------------------------

/// A recorder whose `.ses` destination has already failed and stays failed.
///
/// The FIFO rendezvous completes, then the reader closes, so every subsequent write gets
/// EPIPE and `writer_thread`'s failure slot latches. Returns once the failure is visible,
/// so the caller's next call to the function under test is the one being tested.
#[cfg(unix)]
fn recorder_with_a_broken_ses_destination(dir: &std::path::Path) -> MultiFormatRecorder {
    broken_ses_recorder(dir, false)
}

/// The same broken destination under `recording-allow-unrecorded=true`.
///
/// Same physical failure, opposite policy: the recorder reports the write error but not
/// `Unrecordable`, so the session is expected to survive it.
#[cfg(unix)]
fn permissive_recorder_with_a_broken_ses_destination(dir: &std::path::Path) -> MultiFormatRecorder {
    broken_ses_recorder(dir, true)
}

#[cfg(unix)]
fn broken_ses_recorder(dir: &std::path::Path, allow_unrecorded: bool) -> MultiFormatRecorder {
    use crate::recording::{RecordingConfig, RecordingDirection};

    let ses_path = dir.join("broken.ses");
    let status = std::process::Command::new("mkfifo")
        .arg(&ses_path)
        .status()
        .expect("mkfifo is available on unix");
    assert!(status.success(), "mkfifo {ses_path:?} failed");

    let reader_path = ses_path.clone();
    let reader = std::thread::spawn(move || {
        drop(std::fs::File::open(&reader_path).expect("read end opens"));
    });

    let mut params = std::collections::HashMap::new();
    params.insert(
        "recording-path".to_string(),
        dir.to_string_lossy().to_string(),
    );
    params.insert("recording-name".to_string(), "broken.ses".to_string());
    params.insert("recording-write-existing".to_string(), "true".to_string());
    if allow_unrecorded {
        params.insert("recording-allow-unrecorded".to_string(), "true".to_string());
    }

    let config = RecordingConfig::from_params(&params);
    assert_eq!(
        config.allow_unrecorded, allow_unrecorded,
        "the policy under test has to be the one the recorder was built with"
    );
    let mut recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24)
        .expect("the fifo exists and a reader arrived, so the recorder starts");
    reader.join().expect("reader thread finished");

    // Instructions large enough to clear the BufWriter, until the asynchronous failure
    // latches.
    let big = Bytes::from(format!("4.blob,1.0,{n}.{};", "x".repeat(16384), n = 16384));
    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(5);
    while std::time::Instant::now() < deadline {
        if recorder
            .record_instruction(RecordingDirection::ServerToClient, &big)
            .is_err()
        {
            return recorder;
        }
        std::thread::sleep(std::time::Duration::from_millis(10));
    }
    panic!("a fifo whose reader is gone must start reporting write failures");
}

/// A strict session must not keep sending to the client once recording has stopped.
///
/// `send_and_record` warned and sent anyway, so a session whose recording died at minute
/// one ran to completion, the client saw every frame, and the uploaded `.ses` stopped at
/// minute one. Callers already map this `Err` to a handler error that ends the session.
#[cfg(unix)]
#[tokio::test]
async fn test_send_and_record_fails_when_a_strict_recording_has_broken() {
    let tmp = tempfile::TempDir::new().unwrap();
    let mut recorder = Some(recorder_with_a_broken_ses_destination(tmp.path()));
    let (tx, _rx) = mpsc::channel(16);

    let result = send_and_record(&tx, &mut recorder, Bytes::from("5.ready,4.test;")).await;

    let err = result.expect_err(
        "a strict session whose recording has broken must not keep streaming to the client",
    );
    assert!(
        err.contains("recording"),
        "the failure must name recording rather than look like a channel error, so the \
         session's disconnect reason is legible; got {err:?}"
    );
}

/// The client-to-server direction has to end the session too.
///
/// Keystrokes are the half of the recording an auditor reads, and this is the only place
/// they are recorded; swallowing the failure here leaves a session whose input log stops
/// silently.
#[cfg(unix)]
#[test]
fn test_record_client_input_fails_when_a_strict_recording_has_broken() {
    let tmp = tempfile::TempDir::new().unwrap();
    let mut recorder = Some(recorder_with_a_broken_ses_destination(tmp.path()));

    let result = record_client_input(&mut recorder, &Bytes::from("3.key,2.97,1.1;"));

    assert!(
        result.is_err(),
        "a strict session whose recording has broken must report the failure to the \
         handler instead of logging it"
    );
}

/// The graphical handlers do not use [`send_and_record`], so the policy needs a seam they
/// can share.
///
/// VNC, RDP and RBI each own a `send_and_record`/`record_server_instruction` because they
/// count frames and pick a per-viewer sender first. Each of those inlined
/// `record_instruction` plus a `warn!`, so a strict RDP session whose recording died kept
/// painting the screen for the rest of the session. They call this instead.
#[cfg(unix)]
#[test]
fn test_record_server_output_fails_when_a_strict_recording_has_broken() {
    let tmp = tempfile::TempDir::new().unwrap();
    let mut recorder = Some(recorder_with_a_broken_ses_destination(tmp.path()));

    let result = record_server_output(&mut recorder, &Bytes::from("4.sync,1.0;"));

    assert!(
        result.is_err(),
        "a strict session whose recording has broken must report the failure to the \
         handler instead of logging it"
    );
}

/// A permissive session keeps running: the same broken destination, opposite verdict.
///
/// This is the half that keeps the strict path honest — without it, "return Err on any
/// recording error" would pass the test above and break every session whose operator chose
/// `recording-allow-unrecorded=true`.
#[cfg(unix)]
#[test]
fn test_record_server_output_tolerates_a_broken_recording_when_unrecorded_is_allowed() {
    let tmp = tempfile::TempDir::new().unwrap();
    let mut recorder = Some(permissive_recorder_with_a_broken_ses_destination(
        tmp.path(),
    ));

    let result = record_server_output(&mut recorder, &Bytes::from("4.sync,1.0;"));

    assert!(
        result.is_ok(),
        "recording-allow-unrecorded=true means the session outlives its recording; got {result:?}"
    );
}

/// `try_recv` rather than `recv().await`: the sender is still in scope, so a channel that never
/// received anything would leave `recv()` awaiting forever and the test would hang instead of
/// failing. The send is already complete when `send_msg_best_effort` returns, so the value is in
/// the buffer by now if it was ever sent.
#[tokio::test]
async fn test_send_msg_best_effort_emits_a_msg_instruction() {
    let (tx, mut rx) = mpsc::channel(16);

    send_msg_best_effort(&tx, guacr_protocol::MSG_SECURITY_WARNING, &["Not verified"]).await;

    let sent = rx.try_recv().expect("a msg instruction must be sent");
    assert_eq!(
        String::from_utf8(sent.to_vec()).unwrap(),
        "3.msg,4.4096,12.Not verified;"
    );
}

/// `msg` exists so the user can be told something without losing the session. If it ever
/// went out as `error` instead, the client would close the connection
/// (`streaming.rs`: `b"error" => OpcodeAction::CloseConnection`) -- the warning would kill
/// the very session it was describing.
#[tokio::test]
async fn test_send_msg_best_effort_does_not_send_an_error_instruction() {
    let (tx, mut rx) = mpsc::channel(16);

    send_msg_best_effort(&tx, guacr_protocol::MSG_SECURITY_WARNING, &["careful"]).await;

    let sent = rx.try_recv().expect("a msg instruction must be sent");
    let s = String::from_utf8(sent.to_vec()).unwrap();
    assert!(
        s.starts_with("3.msg,"),
        "must be a msg instruction, got {s}"
    );
    assert!(
        !s.contains("5.error,"),
        "a non-fatal warning must never be delivered as error: {s}"
    );
}

/// Best-effort: a warning must never be the thing that fails a session.
#[tokio::test]
async fn test_send_msg_best_effort_tolerates_a_closed_client() {
    let (tx, rx) = mpsc::channel::<Bytes>(1);
    drop(rx);

    // No panic, no unwrap on the send result.
    send_msg_best_effort(&tx, guacr_protocol::MSG_SECURITY_WARNING, &["gone"]).await;
}
