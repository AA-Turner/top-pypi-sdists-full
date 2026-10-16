// Off-thread recording file writes
//
// Every recording destination the gateway hands us is a FIFO, not a regular file
// (`tunnel_recordings.py` mkfifos the path and reads the other end to encrypt and
// upload). A write to a pipe whose reader has fallen behind blocks once the kernel
// buffer fills — 64 KiB on Linux, 16 KiB on macOS — and the caller is a protocol
// handler running on a tokio worker, so that block parks the worker and stalls the
// live session for as long as the reader takes.
//
// The fix is a dedicated OS thread per recorder that owns the file descriptors and
// does the blocking writes. Handlers hand chunks to a bounded queue and never touch
// the file. When the queue fills the write fails fast with `WouldBlock` instead of
// blocking, which lets the existing `allow_unrecorded` policy decide whether to drop
// the data or end the session.
//
// Not a tokio task: `tokio::fs` is a thread-pool shim around the same blocking
// syscall, and spawn_blocking would consume a pool slot for the life of the session.

use std::fs::File;
use std::io::{self, ErrorKind, Write};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc::{sync_channel, Receiver, SyncSender, TrySendError};
use std::sync::{Arc, Mutex};
use std::thread::JoinHandle;

/// Which recording file a queued chunk belongs to.
///
/// A closed set indexed into a fixed array, so adding a format is a compile error at
/// every match rather than a silently unrouted chunk.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum SinkId {
    /// Guacamole `.ses` protocol stream.
    Ses = 0,
    /// Asciicast v2 event stream.
    Asciicast = 1,
    /// Typescript raw output.
    Typescript = 2,
    /// Typescript companion timing file.
    TypescriptTiming = 3,
}

const SINK_COUNT: usize = 4;

/// Queued chunks before a write fails fast.
///
/// Callers keep their `BufWriter`, so a chunk is normally a full 8 KiB buffer rather
/// than one instruction — this is a queue of buffers, not of writes.
const QUEUE_CAPACITY: usize = 64;

struct Chunk {
    sink: SinkId,
    data: Vec<u8>,
}

/// Where one sink's bytes end up.
///
/// A file on POSIX, where the gateway mkfifos the path. Windows has no FIFO, so there the
/// gateway binds a ZMQ PAIR socket instead and hands guacr its endpoint
/// (`tunnel_recordings.py:1808-1813`); its reader takes raw bytes off that socket, so the
/// two targets carry the identical byte stream and differ only in how it is handed over.
pub(crate) enum SinkTarget {
    /// A regular file or a FIFO.
    File(File),
    /// A ZMQ PAIR socket the gateway has already bound.
    #[cfg(feature = "zmq-transport")]
    Zmq(crate::zmq_transport::ZmqRecordingSender),
}

impl SinkTarget {
    fn write_all(&mut self, data: &[u8]) -> io::Result<()> {
        match self {
            SinkTarget::File(file) => file.write_all(data),
            // Blocking `send`, not `try_send`: this is the writer thread, whose whole
            // purpose is to absorb the block instead of the handler's tokio worker.
            #[cfg(feature = "zmq-transport")]
            SinkTarget::Zmq(sender) => sender.send(data).map_err(io::Error::other),
        }
    }

    /// Release the target once the queue is drained.
    ///
    /// Dropping a `File` is enough — the reader sees EOF. A ZMQ peer disconnect is the
    /// gateway's end-of-recording signal, and `close` waits for the socket to drain first,
    /// so it must not be left to an implicit drop that cannot join the socket thread.
    fn finish(self) {
        match self {
            SinkTarget::File(file) => drop(file),
            #[cfg(feature = "zmq-transport")]
            SinkTarget::Zmq(sender) => sender.close(),
        }
    }
}

/// A write failure the writer thread hit, made visible to the callers.
///
/// The thread cannot return an error to the handler that queued the chunk, and a
/// recording that silently stops writing defeats `allow_unrecorded=false`. The flag is
/// sticky: once the file is broken it stays broken, and every later write reports it.
#[derive(Default)]
struct FailureSlot {
    failed: AtomicBool,
    reason: Mutex<Option<String>>,
}

impl FailureSlot {
    fn set(&self, reason: String) {
        if let Ok(mut slot) = self.reason.lock() {
            if slot.is_none() {
                *slot = Some(reason);
            }
        }
        self.failed.store(true, Ordering::Release);
    }

    /// The recorded reason, or `None` while writes are healthy. The healthy path is a
    /// single atomic load; the mutex is only taken once a failure has been recorded.
    fn reason(&self) -> Option<String> {
        if !self.failed.load(Ordering::Acquire) {
            return None;
        }
        self.reason
            .lock()
            .ok()
            .and_then(|slot| slot.clone())
            .or_else(|| Some("recording write failed".to_string()))
    }
}

/// Owns the writer thread and the file descriptors it writes to.
///
/// Construct with [`RecordingWriter::spawn`], mint one [`OffloadSink`] per file with
/// [`RecordingWriter::sink`], and call [`RecordingWriter::shutdown`] at teardown. The
/// files are closed by the thread, so the reader on the other end of each FIFO sees EOF
/// only after every queued byte has been written.
pub(crate) struct RecordingWriter {
    tx: Option<SyncSender<Chunk>>,
    handle: Option<JoinHandle<()>>,
    failure: Arc<FailureSlot>,
}

impl RecordingWriter {
    /// Spawn the writer thread taking ownership of `targets`. Slots are indexed by
    /// [`SinkId`]; a `None` slot discards chunks addressed to it.
    pub(crate) fn spawn(files: [Option<SinkTarget>; SINK_COUNT]) -> Self {
        let (tx, rx) = sync_channel(QUEUE_CAPACITY);
        let failure = Arc::new(FailureSlot::default());
        let thread_failure = Arc::clone(&failure);

        let handle = std::thread::Builder::new()
            .name("guacr-recording".to_string())
            .spawn(move || run(files, rx, thread_failure))
            .ok();

        if handle.is_none() {
            // No thread means no writer. Fail closed rather than accept chunks that
            // would never reach the file.
            failure.set("recording writer thread could not be started".to_string());
            return Self {
                tx: None,
                handle: None,
                failure,
            };
        }

        Self {
            tx: Some(tx),
            handle,
            failure,
        }
    }

    /// Why the writer thread stopped writing a destination, or `None` while it is healthy.
    ///
    /// Callers buffer, so a destination can be broken for several KiB of recording before a
    /// `write` reaches the queue and reports it. A caller that must not run unrecorded asks
    /// here instead of waiting for its buffer to spill.
    pub(crate) fn failure_reason(&self) -> Option<String> {
        self.failure.reason()
    }

    /// A `Write` handle for one file. Wrap it in a `BufWriter` — every `write` call
    /// becomes one queue entry, so unbuffered use would queue per instruction.
    pub(crate) fn sink(&self, id: SinkId) -> OffloadSink {
        OffloadSink {
            id,
            tx: self.tx.clone(),
            failure: Arc::clone(&self.failure),
        }
    }

    /// Drop the queue and wait for the thread to drain it and close the files.
    ///
    /// Every [`OffloadSink`] must be closed first ([`OffloadSink::close`]) or the queue
    /// keeps a live sender and the thread never sees the disconnect it exits on.
    pub(crate) fn shutdown(&mut self) -> io::Result<()> {
        drop(self.tx.take());
        if let Some(handle) = self.handle.take() {
            if handle.join().is_err() {
                self.failure
                    .set("recording writer thread panicked".to_string());
                log::warn!("recording writer thread panicked");
            }
        }
        match self.failure.reason() {
            Some(reason) => Err(io::Error::other(reason)),
            None => Ok(()),
        }
    }
}

impl Drop for RecordingWriter {
    fn drop(&mut self) {
        let _ = self.shutdown();
    }
}

/// Drains the queue onto the targets until every sender is gone.
///
/// `recv` yields buffered chunks before it reports the disconnect, so the queue is
/// always fully written before the targets close.
fn run(
    mut files: [Option<SinkTarget>; SINK_COUNT],
    rx: Receiver<Chunk>,
    failure: Arc<FailureSlot>,
) {
    while let Ok(chunk) = rx.recv() {
        let slot = &mut files[chunk.sink as usize];
        if let Some(file) = slot.as_mut() {
            if let Err(e) = file.write_all(&chunk.data) {
                // Close this file rather than retry it per chunk: a FIFO whose reader
                // is gone fails every write, and each failure would be another log line
                // for the rest of the session.
                failure.set(format!("{:?} recording write failed: {}", chunk.sink, e));
                log::warn!(
                    "{:?} recording write failed, closing the file: {}",
                    chunk.sink,
                    e
                );
                *slot = None;
            }
        }
    }

    // Queue drained: hand each target its close, so the gateway sees end-of-recording only
    // after the last byte. Ordinary drop would do it for a file but not for a socket.
    for slot in files.iter_mut() {
        if let Some(target) = slot.take() {
            target.finish();
        }
    }
}

/// The caller-side handle: an `io::Write` that queues to the writer thread.
///
/// Errors are the queue's, not the file's — a full queue is `WouldBlock`, a stopped
/// thread is `BrokenPipe`, and a file that failed to write reports that failure on
/// every subsequent call.
pub(crate) struct OffloadSink {
    id: SinkId,
    tx: Option<SyncSender<Chunk>>,
    failure: Arc<FailureSlot>,
}

impl OffloadSink {
    /// Release the queue handle. Required before [`RecordingWriter::shutdown`].
    pub(crate) fn close(&mut self) {
        drop(self.tx.take());
    }
}

impl Write for OffloadSink {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        if let Some(reason) = self.failure.reason() {
            return Err(io::Error::other(reason));
        }

        let Some(tx) = self.tx.as_ref() else {
            return Err(io::Error::new(
                ErrorKind::BrokenPipe,
                "recording sink is closed",
            ));
        };

        match tx.try_send(Chunk {
            sink: self.id,
            data: buf.to_vec(),
        }) {
            Ok(()) => Ok(buf.len()),
            Err(TrySendError::Full(_)) => Err(io::Error::new(
                ErrorKind::WouldBlock,
                "recording queue is full: the reader is not keeping up",
            )),
            Err(TrySendError::Disconnected(_)) => Err(io::Error::new(
                ErrorKind::BrokenPipe,
                "recording writer thread has stopped",
            )),
        }
    }

    /// Nothing to do: the bytes are already queued, and the file's own flush belongs to
    /// the writer thread. Returning an error here would surface a *queue* state as a
    /// flush failure, which callers treat as fatal.
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn shutdown_reports_writer_panic() {
        // Given: a writer thread that exits by panicking without setting the failure slot.
        let mut writer = RecordingWriter {
            tx: None,
            handle: Some(std::thread::spawn(|| panic!("test writer panic"))),
            failure: Arc::new(FailureSlot::default()),
        };

        // When: shutdown joins the writer.
        let result = writer.shutdown();

        // Then: the panic is reported instead of being mistaken for a clean drain.
        assert_eq!(
            result.unwrap_err().to_string(),
            "recording writer thread panicked"
        );
    }
}
