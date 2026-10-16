// Tests for off-thread recording writes.
//
// The behaviour under test only exists on a pipe: a regular file never blocks, so these
// are `#[cfg(unix)]` and build a real FIFO with `mkfifo`, which is what the gateway does
// (`tunnel_recordings.py` mkfifos the recording path and reads the other end).

#![cfg(unix)]

use bytes::Bytes;
use std::io::{BufRead, Read};
use std::path::Path;
use std::sync::mpsc;
use std::time::Duration;
use tempfile::TempDir;

use crate::config::RecordingConfig;
use crate::multi::MultiFormatRecorder;
use crate::ses::{GuacamoleSesRecorder, RecordingDirection, RecordingError, SesPayload};
use std::collections::HashMap;

/// Longest a `record()` call may take. Generous: the point is to separate "returned" from
/// "blocked until the reader drains", not to measure the write.
const WRITE_DEADLINE: Duration = Duration::from_secs(5);

fn make_fifo(path: &Path) {
    let status = std::process::Command::new("mkfifo")
        .arg(path)
        .status()
        .expect("mkfifo is available on unix");
    assert!(status.success(), "mkfifo {:?} failed", path);
}

/// A binary `TerminalData` frame: `[opcode][flags][reserved u16][len u32][payload]`.
fn terminal_frame(payload: &[u8]) -> Bytes {
    let mut frame = Vec::with_capacity(8 + payload.len());
    frame.push(guacr_protocol::Opcode::TerminalData as u8);
    frame.push(0);
    frame.extend_from_slice(&0u16.to_le_bytes());
    frame.extend_from_slice(&(payload.len() as u32).to_le_bytes());
    frame.extend_from_slice(payload);
    Bytes::from(frame)
}

/// Holds the read end of a FIFO open without draining it, then drains on demand.
struct StalledReader {
    ready: mpsc::Receiver<()>,
    release: Option<mpsc::Sender<()>>,
    handle: std::thread::JoinHandle<Vec<u8>>,
}

impl StalledReader {
    /// Opens the read end on its own thread. Blocks there until a writer arrives, which is
    /// the FIFO rendezvous — so this must be called *before* the recorder is constructed.
    fn spawn(path: &Path) -> Self {
        let (ready_tx, ready) = mpsc::channel();
        let (release, release_rx) = mpsc::channel::<()>();
        let path = path.to_path_buf();

        let handle = std::thread::spawn(move || {
            let mut fifo = std::fs::File::open(&path).expect("read end of the fifo opens");
            ready_tx.send(()).ok();

            // Hold the pipe open and read nothing: the kernel buffer fills (64 KiB on
            // Linux, 16 KiB on macOS) and every further write to it blocks.
            release_rx.recv().ok();

            let mut drained = Vec::new();
            fifo.read_to_end(&mut drained).expect("fifo drains to EOF");
            drained
        });

        Self {
            ready,
            release: Some(release),
            handle,
        }
    }

    fn wait_until_open(&self) {
        self.ready
            .recv_timeout(WRITE_DEADLINE)
            .expect("reader opened the fifo");
    }

    /// Start draining, without waiting. Separate from [`StalledReader::collect`] because
    /// the reader only reaches EOF once the recorder closes the write end, and the
    /// recorder's teardown only completes once the pipe is being drained — so the two have
    /// to overlap.
    fn release(&mut self) {
        drop(self.release.take());
    }

    /// Wait for EOF and return everything the reader saw.
    fn collect(self) -> Vec<u8> {
        self.handle.join().expect("reader thread finished")
    }
}

fn reader_departing(
    path: &Path,
    read_header: bool,
) -> (
    mpsc::Receiver<()>,
    mpsc::Sender<()>,
    std::thread::JoinHandle<()>,
) {
    let (ready_tx, ready) = mpsc::channel();
    let (leave, departing) = mpsc::channel::<()>();
    let path = path.to_path_buf();
    let handle = std::thread::spawn(move || {
        let fifo = std::fs::File::open(path).expect("read end opens");
        if read_header {
            let mut header = Vec::new();
            std::io::BufReader::new(&fifo)
                .read_until(b'\n', &mut header)
                .expect("asciicast header arrives");
            assert!(!header.is_empty(), "asciicast header must arrive");
        }
        ready_tx.send(()).expect("recorder waits for reader");
        departing.recv().expect("recorder releases reader");
    });
    (ready, leave, handle)
}

#[test]
fn test_owned_ses_finalize_reports_last_queued_fifo_failure_when_required() {
    // Given: a FIFO whose reader leaves after the writer opens it.
    let tmp = TempDir::new().unwrap();
    let path = tmp.path().join("owned.ses");
    make_fifo(&path);
    let (ready, leave, reader) = reader_departing(&path, false);
    let config = RecordingConfig {
        recording_write_existing: true,
        ..Default::default()
    };
    let mut recorder = GuacamoleSesRecorder::new(&path, &config).unwrap();
    ready.recv_timeout(WRITE_DEADLINE).unwrap();
    leave.send(()).unwrap();
    reader.join().unwrap();
    recorder
        .record(
            RecordingDirection::ServerToClient,
            &Bytes::from_static(b"4.size,1.0,2.80,2.24;"),
        )
        .unwrap();

    // When: finalize flushes the only buffered instruction and drains the queue.
    let result = recorder.finalize();

    // Then: the off-thread EPIPE is a policy-fatal failure, not success.
    assert!(
        matches!(&result, Err(RecordingError::Unrecordable(reason)) if reason.contains("Ses recording write failed")),
        "got {result:?}"
    );
}

#[test]
fn test_shared_writer_finalize_reports_last_queued_fifo_failure_when_required() {
    // Given: an asciicast FIFO with its header consumed before reader loss.
    let tmp = TempDir::new().unwrap();
    let path = tmp.path().join("shared.cast");
    make_fifo(&path);
    let (ready, leave, reader) = reader_departing(&path, true);
    let config = RecordingConfig {
        asciicast_path: Some(tmp.path().to_string_lossy().into_owned()),
        asciicast_name: Some("shared".to_string()),
        recording_write_existing: true,
        ..Default::default()
    };
    let mut recorder = MultiFormatRecorder::new(&config, &HashMap::new(), "ssh", 80, 24).unwrap();
    ready.recv_timeout(WRITE_DEADLINE).unwrap();
    leave.send(()).unwrap();
    reader.join().unwrap();
    recorder.record_output(b"last buffered output").unwrap();

    // When: the final buffered event is queued and the writer thread drains.
    let result = recorder.finalize();

    // Then: required recording loss is classified as Unrecordable.
    assert!(
        matches!(&result, Err(RecordingError::Unrecordable(reason)) if reason.contains("Asciicast recording write failed")),
        "got {result:?}"
    );
}

#[test]
fn test_shared_writer_finalize_keeps_fifo_failure_advisory_when_permissive() {
    // Given: the same reader loss with unrecorded sessions allowed.
    let tmp = TempDir::new().unwrap();
    let path = tmp.path().join("permissive.cast");
    make_fifo(&path);
    let (ready, leave, reader) = reader_departing(&path, true);
    let config = RecordingConfig {
        asciicast_path: Some(tmp.path().to_string_lossy().into_owned()),
        asciicast_name: Some("permissive".to_string()),
        recording_write_existing: true,
        allow_unrecorded: true,
        ..Default::default()
    };
    let mut recorder = MultiFormatRecorder::new(&config, &HashMap::new(), "ssh", 80, 24).unwrap();
    ready.recv_timeout(WRITE_DEADLINE).unwrap();
    leave.send(()).unwrap();
    reader.join().unwrap();
    recorder.record_output(b"last buffered output").unwrap();

    // When: finalization drains the write to a readerless FIFO.
    let result = recorder.finalize();

    // Then: the I/O failure is advisory rather than policy-fatal.
    assert!(
        matches!(&result, Err(RecordingError::Io(error)) if error.to_string().contains("Asciicast recording write failed")),
        "got {result:?}"
    );
}

/// A blocked recording reader must not stall the session.
///
/// Every recording destination the gateway supplies is a FIFO, and the handler that calls
/// `record()` is on a tokio worker. Writing the file inline means a reader that pauses for
/// a second parks that worker for a second, and the live session freezes with it. With the
/// writes on a dedicated OS thread, `record()` only queues.
#[test]
fn test_ses_writes_do_not_block_on_a_stalled_reader() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("stalled.ses");
    make_fifo(&ses_path);

    let mut reader = StalledReader::spawn(&ses_path);

    let config = RecordingConfig {
        recording_write_existing: true,
        ..Default::default()
    };
    let mut recorder =
        GuacamoleSesRecorder::new_with_payload(&ses_path, &config, SesPayload::Terminal).unwrap();
    reader.wait_until_open();

    // 192 KiB: past any platform's pipe buffer, so an inline write is guaranteed to
    // block, and well inside the queue so this is not also testing the full-queue path.
    let frame = terminal_frame(&[b'x'; 1024]);
    let (done_tx, done) = mpsc::channel();
    let writer = std::thread::spawn(move || {
        for _ in 0..192 {
            recorder
                .record(RecordingDirection::ServerToClient, &frame)
                .expect("queueing a frame succeeds");
        }
        done_tx.send(()).ok();
        recorder
    });

    done.recv_timeout(WRITE_DEADLINE)
        .expect("record() must not block on a reader that is not draining");

    // Teardown drains: finalize joins the writer thread, which is parked on the full pipe
    // until the reader consumes it.
    let recorder = writer.join().expect("writer thread finished");
    reader.release();
    recorder.finalize().expect("finalize succeeds");
    let drained = reader.collect();

    assert!(
        drained.len() >= 192 * 1032,
        "every queued frame must reach the fifo, got {} bytes",
        drained.len()
    );
}

/// A reader that never drains must not let the queue grow without bound.
///
/// Unbounded buffering trades the stall for memory: a session producing faster than the
/// reader consumes would grow until the process is killed. The bound makes it a reported
/// error instead, which is what `allow_unrecorded` is there to decide on.
#[test]
fn test_queue_full_reports_an_error_rather_than_blocking() {
    let tmp_dir = TempDir::new().unwrap();
    let ses_path = tmp_dir.path().join("overrun.ses");
    make_fifo(&ses_path);

    let mut reader = StalledReader::spawn(&ses_path);

    let config = RecordingConfig {
        recording_write_existing: true,
        ..Default::default()
    };
    let mut recorder =
        GuacamoleSesRecorder::new_with_payload(&ses_path, &config, SesPayload::Terminal).unwrap();
    reader.wait_until_open();

    // 4 MiB — far past the queue's capacity with the pipe blocked.
    let frame = terminal_frame(&[b'x'; 4096]);
    let (done_tx, done) = mpsc::channel();
    let writer = std::thread::spawn(move || {
        let mut error = None;
        for _ in 0..1024 {
            if let Err(e) = recorder.record(RecordingDirection::ServerToClient, &frame) {
                error = Some(e);
                break;
            }
        }
        done_tx.send(()).ok();
        (recorder, error)
    });

    done.recv_timeout(WRITE_DEADLINE)
        .expect("an overrun must fail fast, not block");
    let (recorder, error) = writer.join().expect("writer thread finished");

    let error = error.expect("writing past the queue capacity must report an error");
    assert!(
        error.to_string().contains("queue is full"),
        "the error must name the overrun, got: {}",
        error
    );

    // Unblock the pipe before teardown so the writer thread's join can complete.
    reader.release();
    drop(recorder);
    reader.collect();
}
