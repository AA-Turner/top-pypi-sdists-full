// Live Session Registry for multi-viewer session sharing (T-039 to T-041)
//
// Maps active session IDs ($ prefixed, per Guacamole convention) to
// session handles. The registry is globally accessible and concurrent-safe
// via DashMap, which provides per-shard lock-free reads.
//
// Session IDs MUST start with '$' (AC-5, T-041).
//
// The registry holds broadcast::Sender<Bytes> handles. The owner session
// sends to all current and future viewers by cloning the sender. Viewers
// subscribe by calling subscribe() on the sender to get a Receiver.
//
// Cleanup: call deregister() when the owner disconnects (AC-3).

use bytes::Bytes;
use dashmap::{mapref::entry::Entry, DashMap};
use once_cell::sync::Lazy;
use parking_lot::RwLock;
use std::sync::{Arc, Weak};
use tokio::sync::{broadcast, mpsc, watch};
use uuid::Uuid;

/// Capacity of the broadcast channel buffer.
/// Viewers that fall behind this many frames will be dropped (T-081 backpressure avoidance).
pub const BROADCAST_CHANNEL_CAPACITY: usize = 256;

/// A key/mouse instruction forwarded from a viewer into the owner's handler loop.
///
/// The identity travels with the bytes so the owner's handler can attribute the
/// input in session recordings. Without it, a viewer's keystrokes are recorded as
/// though the session owner had typed them, which defeats the point of recording
/// a shared session.
#[derive(Clone, Debug)]
pub struct ViewerInput {
    /// The raw Guacamole instruction as the viewer sent it.
    pub bytes: Bytes,
    /// Share participant GUID — stable identifier for audit correlation.
    pub guid: Uuid,
    /// Participant display name, recorded alongside the instruction.
    pub display_name: String,
}

impl ViewerInput {
    /// The identity to attribute this input to in recordings.
    pub fn actor(&self) -> ViewerActor<'_> {
        ViewerActor {
            guid: self.guid,
            display_name: &self.display_name,
        }
    }
}

/// Who produced a forwarded input, as recorded.
///
/// The GUID is the stable, unique identifier an audit correlates on; display names
/// are neither, so the name is recorded only alongside it, never instead of it.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ViewerActor<'a> {
    pub guid: Uuid,
    pub display_name: &'a str,
}

/// A sticky, receiver-only lifetime signal. Closing the last signal sender also ends it.
#[derive(Clone, Debug)]
pub(crate) struct SessionCancellation {
    rx: watch::Receiver<bool>,
}

impl SessionCancellation {
    pub(crate) fn subscribe(sender: &watch::Sender<bool>) -> Self {
        Self {
            rx: sender.subscribe(),
        }
    }

    pub(crate) async fn cancelled(&mut self) {
        while !*self.rx.borrow_and_update() {
            if self.rx.changed().await.is_err() {
                return;
            }
        }
    }
}

#[derive(Debug)]
struct SessionState {
    sender: Option<broadcast::Sender<Bytes>>,
    last_frame: Option<Bytes>,
    viewer_input_tx: Option<ViewerInputSender>,
    ended: watch::Sender<bool>,
}

/// An owner capability for a live session. All clones share one terminal state.
#[derive(Clone, Debug)]
pub struct SessionHandle {
    state: Arc<RwLock<SessionState>>,
}

/// Weak identity for one frame generation; invitations must never rebind by session ID.
#[derive(Clone, Debug)]
pub(crate) struct SessionGeneration {
    state: Weak<RwLock<SessionState>>,
}

impl SessionGeneration {
    pub(crate) fn is_live(&self) -> bool {
        self.state
            .upgrade()
            .is_some_and(|state| state.read().sender.is_some())
    }

    pub(crate) fn matches(&self, handle: &SessionHandle) -> bool {
        self.state.ptr_eq(&Arc::downgrade(&handle.state))
    }

    pub(crate) fn subscribe_viewer(
        &self,
        update: Bytes,
    ) -> Option<(SessionSubscription, Option<Bytes>)> {
        let handle = SessionHandle {
            state: self.state.upgrade()?,
        };
        handle.broadcast_control(update);
        handle.subscribe_viewer()
    }
}

/// Receiver-only viewer capability: it never keeps the owner/frame/input channel alive.
pub(crate) struct SessionSubscription {
    pub(crate) rx: broadcast::Receiver<Bytes>,
    pub(crate) ended: SessionCancellation,
    state: Weak<RwLock<SessionState>>,
}

impl SessionSubscription {
    pub(crate) fn forward_viewer_input(&self, input: ViewerInput) -> bool {
        self.state.upgrade().is_some_and(|state| {
            let state = state.read();
            state
                .viewer_input_tx
                .as_ref()
                .is_some_and(|tx| tx.send(input).is_ok())
        })
    }

    pub(crate) fn broadcast_control(&self, msg: Bytes) -> usize {
        self.state.upgrade().map_or(0, |state| {
            let state = state.read();
            state
                .sender
                .as_ref()
                .map_or(0, |sender| sender.send(msg).unwrap_or(0))
        })
    }
}

/// Sender half of the viewer → owner input channel.
pub type ViewerInputSender = mpsc::UnboundedSender<ViewerInput>;

/// Receiver half of the viewer → owner input channel, held by protocol handlers.
pub type ViewerInputReceiver = mpsc::UnboundedReceiver<ViewerInput>;

impl SessionHandle {
    pub fn new() -> Self {
        let (sender, _) = broadcast::channel(BROADCAST_CHANNEL_CAPACITY);
        let (ended, _) = watch::channel(false);
        Self {
            state: Arc::new(RwLock::new(SessionState {
                sender: Some(sender),
                last_frame: None,
                viewer_input_tx: None,
                ended,
            })),
        }
    }

    pub(crate) fn generation(&self) -> SessionGeneration {
        SessionGeneration {
            state: Arc::downgrade(&self.state),
        }
    }

    /// Register input only while this generation is live.
    pub fn set_viewer_input_channel(&self, tx: ViewerInputSender) {
        let mut state = self.state.write();
        if state.sender.is_some() {
            state.viewer_input_tx = Some(tx);
        }
    }

    /// Forward attributed input, or return false when input is unavailable/ended.
    pub fn forward_viewer_input(&self, input: ViewerInput) -> bool {
        self.state
            .read()
            .viewer_input_tx
            .as_ref()
            .is_some_and(|tx| tx.send(input).is_ok())
    }

    /// Subscribe to future output. An ended handle returns an already-closed receiver.
    pub fn subscribe(&self) -> broadcast::Receiver<Bytes> {
        let state = self.state.read();
        match &state.sender {
            Some(sender) => sender.subscribe(),
            None => {
                let (_, rx) = broadcast::channel(BROADCAST_CHANNEL_CAPACITY);
                rx
            }
        }
    }

    /// Subscribe and take the existing late-join cache atomically against broadcast/end.
    pub(crate) fn subscribe_viewer(&self) -> Option<(SessionSubscription, Option<Bytes>)> {
        let state = self.state.read();
        let sender = state.sender.as_ref()?;
        Some((
            SessionSubscription {
                rx: sender.subscribe(),
                ended: SessionCancellation::subscribe(&state.ended),
                state: Arc::downgrade(&self.state),
            },
            state.last_frame.clone(),
        ))
    }

    /// Broadcast display output and cache it for late join; ended handles cannot send.
    pub fn broadcast(&self, frame: Bytes) -> usize {
        let mut state = self.state.write();
        if state.sender.is_none() {
            return 0;
        }
        state.last_frame = Some(frame.clone());
        state.sender.as_ref().unwrap().send(frame).unwrap_or(0)
    }

    /// Broadcast control traffic without changing the display cache.
    pub fn broadcast_control(&self, msg: Bytes) -> usize {
        self.state
            .read()
            .sender
            .as_ref()
            .map_or(0, |sender| sender.send(msg).unwrap_or(0))
    }

    pub fn last_frame(&self) -> Option<Bytes> {
        self.state.read().last_frame.clone()
    }

    pub fn viewer_count(&self) -> usize {
        self.state
            .read()
            .sender
            .as_ref()
            .map_or(0, |sender| sender.receiver_count())
    }

    /// Terminal close releases cached bytes/input and the sender even with surviving handles.
    pub(crate) fn end(&self) {
        let mut state = self.state.write();
        state.ended.send_replace(true);
        state.sender = None;
        state.last_frame = None;
        state.viewer_input_tx = None;
    }
}

impl Default for SessionHandle {
    fn default() -> Self {
        Self::new()
    }
}

// ============================================================================
// Global session registry
// ============================================================================

/// Global concurrent-safe session registry (AC-4).
///
/// Uses DashMap so concurrent register/lookup from multiple Tokio tasks is
/// race-free without a global Mutex.
static SESSION_REGISTRY: Lazy<DashMap<String, SessionHandle>> = Lazy::new(DashMap::new);

/// Register a new session with the given ID.
///
/// Returns `Err` if:
/// - The ID does not start with '$' (AC-5)
/// - A session with this ID already exists
///
/// On success returns the new SessionHandle (AC-1).
pub fn register(session_id: &str) -> Result<SessionHandle, String> {
    // AC-5: enforce '$' prefix convention (T-041).
    if !session_id.starts_with('$') {
        return Err(format!(
            "Session ID must start with '$', got: {session_id:?}"
        ));
    }
    match SESSION_REGISTRY.entry(session_id.to_string()) {
        Entry::Occupied(_) => Err(format!("Session {session_id:?} is already registered")),
        Entry::Vacant(entry) => {
            let handle = SessionHandle::new();
            entry.insert(handle.clone());
            Ok(handle)
        }
    }
}

/// Look up a session by ID.
///
/// Returns `Some(SessionHandle)` if found, `None` if not (AC-2).
/// Never panics.
pub fn lookup(session_id: &str) -> Option<SessionHandle> {
    SESSION_REGISTRY.get(session_id).map(|r| r.clone())
}

/// Remove a session from the registry after the owner disconnects (AC-3).
///
/// After this call, looking up the session_id returns `None`.
pub fn deregister(session_id: &str) {
    if let Some((_, handle)) = SESSION_REGISTRY.remove(session_id) {
        handle.end();
        crate::share_registry::retire_frame_share(session_id, &handle);
    }
}

/// End this owner's generation without removing a replacement registered under the same ID.
pub(crate) fn deregister_owner(session_id: &str, handle: &SessionHandle) {
    SESSION_REGISTRY.remove_if(session_id, |_, current| {
        Arc::ptr_eq(&current.state, &handle.state)
    });
    handle.end();
    crate::share_registry::retire_frame_share(session_id, handle);
}

/// Return all currently registered session IDs.
/// Intended for diagnostics/metrics only.
pub fn active_session_ids() -> Vec<String> {
    SESSION_REGISTRY.iter().map(|r| r.key().clone()).collect()
}
