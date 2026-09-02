// ZMQ PAIR recording transport.
//
// Rust opens a PAIR socket and connects to an IPC address Python created via
// ZMQProxy. Python's existing RecordingReader receives raw bytes on the backend
// PAIR socket, applies AES-GCM encryption, and uploads to krouter.
//
// The socket runs in a dedicated thread. Each handler session creates one sender
// and one sender only — the socket close signals end-of-recording to Python.
//
// Connection parameter: "recording-zmq-addr" = IPC endpoint Python bound,
// e.g. "ipc:///tmp/session-abc123.ses.zmq"

use crate::ses::RecordingError;
use std::sync::mpsc;
use std::thread;

/// ZMQ PAIR recording sender — one per session.
///
/// Connects to the IPC address Python's ZMQProxy frontend is bound on.
/// Sends raw recording bytes as ZMQ messages. Dropping or calling `close()`
/// terminates the socket, which Python interprets as end-of-recording.
pub struct ZmqRecordingSender {
    tx: mpsc::SyncSender<Option<Vec<u8>>>,
    thread: Option<thread::JoinHandle<()>>,
    /// When true: ZMQ send failures are non-fatal — caller logs and continues.
    /// When false (default): caller must terminate the session on send failure.
    pub allow_unrecorded: bool,
}

impl ZmqRecordingSender {
    /// Connect to a ZMQ PAIR address that Python's ZMQProxy frontend has bound.
    ///
    /// The connection is lazy — ZMQ will not error until the first send if no
    /// peer is bound. `allow_unrecorded` controls LosslessOrDie behavior.
    pub fn connect(addr: &str, allow_unrecorded: bool) -> Result<Self, RecordingError> {
        let ctx = zmq::Context::new();
        let socket = ctx
            .socket(zmq::PAIR)
            .map_err(|e| RecordingError::Zmq(e.to_string()))?;

        // Allow up to 1 second for in-flight messages to drain on close.
        socket
            .set_linger(1000)
            .map_err(|e| RecordingError::Zmq(e.to_string()))?;

        socket
            .connect(addr)
            .map_err(|e| RecordingError::Zmq(e.to_string()))?;

        // Bounded channel: backpressure if the ZMQ thread can't keep up.
        let (tx, rx) = mpsc::sync_channel::<Option<Vec<u8>>>(128);

        let thread = thread::Builder::new()
            .name("guacr-zmq-rec".to_string())
            .spawn(move || {
                while let Ok(Some(data)) = rx.recv() {
                    if socket.send(&data, 0).is_err() {
                        // Drain remaining messages so callers don't block on send.
                        while rx.try_recv().is_ok() {}
                        break;
                    }
                }
                // Socket drops here — ZMQ sends CLOSE_NOTIFY to peer.
            })
            .map_err(|e| RecordingError::Zmq(e.to_string()))?;

        Ok(Self {
            tx,
            thread: Some(thread),
            allow_unrecorded,
        })
    }

    /// Send raw recording bytes. Returns an error if the ZMQ thread has exited
    /// (i.e., a previous send failed or the channel is full).
    pub fn send(&self, payload: &[u8]) -> Result<(), RecordingError> {
        self.tx
            .send(Some(payload.to_vec()))
            .map_err(|_| RecordingError::Zmq("ZMQ sender thread exited".to_string()))
    }

    /// Non-blocking send. Returns `Err(Zmq(...))` immediately if the channel is
    /// full instead of blocking the caller's async Tokio thread.
    pub fn try_send(&self, payload: &[u8]) -> Result<(), RecordingError> {
        self.tx
            .try_send(Some(payload.to_vec()))
            .map_err(|e| match e {
                std::sync::mpsc::TrySendError::Full(_) => {
                    RecordingError::Zmq("ZMQ channel full — event dropped".to_string())
                }
                std::sync::mpsc::TrySendError::Disconnected(_) => {
                    RecordingError::Zmq("ZMQ sender thread exited".to_string())
                }
            })
    }

    /// Signal end-of-recording and wait for the ZMQ thread to flush and close.
    ///
    /// After close, the Python ZMQProxy sees the peer disconnect which it
    /// interprets as end-of-recording for this session.
    pub fn close(mut self) {
        let _ = self.tx.send(None);
        if let Some(t) = self.thread.take() {
            let _ = t.join();
        }
    }
}
