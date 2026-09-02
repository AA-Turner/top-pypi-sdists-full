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
use dashmap::DashMap;
use once_cell::sync::Lazy;
use parking_lot::Mutex;
use std::sync::Arc;
use tokio::sync::{broadcast, mpsc};

/// Capacity of the broadcast channel buffer.
/// Viewers that fall behind this many frames will be dropped (T-081 backpressure avoidance).
pub const BROADCAST_CHANNEL_CAPACITY: usize = 256;

/// A handle to a live session.
///
/// Holds the broadcast sender that the owner uses to distribute screen frames
/// to all connected viewers, plus a cache of the most recent frame for late-join
/// state sync (T-087).
#[derive(Clone, Debug)]
pub struct SessionHandle {
    /// Broadcast sender — clone for each new viewer subscription.
    sender: broadcast::Sender<Bytes>,
    /// Most recent frame from the owner, used for late-join state sync (T-087 AC-1).
    last_frame: Arc<Mutex<Option<Bytes>>>,
    /// Input channel registered by the owner's handler so viewers with PRIV_CONTROL
    /// can forward key/mouse events into the owner's processing loop.
    viewer_input_tx: Arc<Mutex<Option<mpsc::UnboundedSender<Bytes>>>>,
}

impl SessionHandle {
    /// Create a new SessionHandle with a fresh broadcast channel.
    pub fn new() -> Self {
        let (sender, _) = broadcast::channel(BROADCAST_CHANNEL_CAPACITY);
        Self {
            sender,
            last_frame: Arc::new(Mutex::new(None)),
            viewer_input_tx: Arc::new(Mutex::new(None)),
        }
    }

    /// Register the owner's input channel so viewers with PRIV_CONTROL can forward
    /// key/mouse events into the owner's handler loop.
    ///
    /// Called once by the owner's handler immediately after session registration.
    /// The owner's handler reads from the corresponding receiver alongside `from_client`.
    pub fn set_viewer_input_channel(&self, tx: mpsc::UnboundedSender<Bytes>) {
        *self.viewer_input_tx.lock() = Some(tx);
    }

    /// Forward a viewer input event (key/mouse) to the owner's handler.
    ///
    /// Returns `true` if the channel is registered and the send succeeded,
    /// `false` if no channel is registered (viewer input silently dropped).
    pub fn forward_viewer_input(&self, input: Bytes) -> bool {
        if let Some(tx) = self.viewer_input_tx.lock().as_ref() {
            tx.send(input).is_ok()
        } else {
            false
        }
    }

    /// Get a receiver that delivers all frames broadcast after this call.
    pub fn subscribe(&self) -> broadcast::Receiver<Bytes> {
        self.sender.subscribe()
    }

    /// Broadcast a frame to all connected viewers and cache it for late-join sync.
    ///
    /// Returns the number of receivers that received it (0 if no viewers).
    pub fn broadcast(&self, frame: Bytes) -> usize {
        // Cache the frame for late-joining viewers (T-087).
        *self.last_frame.lock() = Some(frame.clone());
        self.sender.send(frame).unwrap_or(0)
    }

    /// Get the most recent frame (for late-join state sync, T-087 AC-1).
    pub fn last_frame(&self) -> Option<Bytes> {
        self.last_frame.lock().clone()
    }

    /// Current number of active viewer subscriptions.
    pub fn viewer_count(&self) -> usize {
        self.sender.receiver_count()
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
    let handle = SessionHandle::new();
    if SESSION_REGISTRY
        .insert(session_id.to_string(), handle.clone())
        .is_some()
    {
        return Err(format!("Session {session_id:?} is already registered"));
    }
    Ok(handle)
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
    SESSION_REGISTRY.remove(session_id);
}

/// Return all currently registered session IDs.
/// Intended for diagnostics/metrics only.
pub fn active_session_ids() -> Vec<String> {
    SESSION_REGISTRY.iter().map(|r| r.key().clone()).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use std::thread;

    fn unique_id(prefix: &str) -> String {
        use std::sync::atomic::{AtomicU64, Ordering};
        static CTR: AtomicU64 = AtomicU64::new(0);
        format!("${prefix}{}", CTR.fetch_add(1, Ordering::Relaxed))
    }

    // AC-1: register and look up by ID.
    #[test]
    fn test_register_and_lookup() {
        let id = unique_id("test_rl_");
        let _handle = register(&id).unwrap();
        assert!(lookup(&id).is_some(), "registered session must be findable");
    }

    // AC-2: lookup of unknown ID returns None.
    #[test]
    fn test_lookup_nonexistent_returns_none() {
        assert!(lookup("$nonexistent_xyz_abc").is_none());
    }

    // AC-3: after deregister, lookup returns None.
    #[test]
    fn test_deregister_clears_entry() {
        let id = unique_id("test_dc_");
        register(&id).unwrap();
        deregister(&id);
        assert!(
            lookup(&id).is_none(),
            "deregistered session must not be findable"
        );
    }

    // AC-4: concurrent registration and lookup is race-free.
    #[test]
    fn test_concurrent_register_lookup() {
        let id = Arc::new(unique_id("test_con_"));
        let barrier = Arc::new(std::sync::Barrier::new(4));

        let handles: Vec<_> = (0..4)
            .map(|i| {
                let id_clone = Arc::clone(&id);
                let b = Arc::clone(&barrier);
                thread::spawn(move || {
                    b.wait();
                    if i == 0 {
                        let _ = register(&id_clone);
                    } else {
                        // lookup may return None if registration hasn't happened yet — that's fine.
                        let _ = lookup(&id_clone);
                    }
                })
            })
            .collect();

        for h in handles {
            h.join().expect("thread must not panic");
        }
        // Cleanup.
        deregister(&id);
    }

    // AC-5: session ID without '$' prefix is rejected.
    #[test]
    fn test_session_id_must_have_dollar_prefix() {
        let result = register("no-dollar-prefix");
        assert!(result.is_err(), "missing '$' prefix must return Err");
        let msg = result.unwrap_err();
        assert!(msg.contains('$'), "error must mention the '$' requirement");
    }

    // AC-5: session ID with '$' prefix succeeds.
    #[test]
    fn test_session_id_with_dollar_prefix_succeeds() {
        let id = unique_id("prefix_ok_");
        assert!(register(&id).is_ok(), "'$' prefixed ID must succeed");
        deregister(&id);
    }

    // Broadcast sanity: viewer receives frame.
    #[test]
    fn test_broadcast_reaches_viewer() {
        let id = unique_id("test_bc_");
        let handle = register(&id).unwrap();
        let mut rx = handle.subscribe();

        let frame = Bytes::from_static(b"frame-data");
        let sent = handle.broadcast(frame.clone());
        assert_eq!(sent, 1, "one receiver should have gotten the frame");

        let received = rx.try_recv().expect("receiver must have the frame");
        assert_eq!(received, frame);
        deregister(&id);
    }
}
