//! Public data-tap surface for direct-API consumers (the Rust PAM
//! Gateway). Lets a session-recording / threat-detection / view-only
//! mirror subsystem observe every outbound byte chunk that goes out a
//! WebRTC data channel of a [`crate::Tube`] without modifying the
//! channel's internal `send` path.
//!
//! ## Performance
//!
//! - Storage is `parking_lot::RwLock<Option<Arc<dyn TubeDataTap>>>`.
//!   The hot path takes a read lock, which under no contention is
//!   ~10 ns (uncontended futex-free spin). The slot is touched
//!   write-side only at session start (via
//!   [`crate::Tube::set_outbound_tap`]) and at session end (via
//!   `clear_outbound_tap` or sink drop) — never during steady-state
//!   sending — so contention is structurally absent.
//! - The no-tap fast path is a single read-lock acquire + an
//!   `Option::is_none` check.
//! - When a tap is installed, the cost is one read-lock acquire +
//!   one virtual call to [`TubeDataTap::on_outbound`].
//! - The implementation MUST keep the call cheap; the gateway's
//!   `gateway_framebus::Producer::publish` is wait-free (~1 µs avg
//!   measured at 253 MB/s in `framebus_under_load`).
//!
//! ## Resilience
//!
//! - Implementations MUST NOT block; MUST NOT panic. A panic inside
//!   `on_outbound` aborts the calling task (typically the
//!   `EventDrivenSender` actor) which closes the data
//!   channel — the gateway then sees the channel close and tears the
//!   conversation down.
//! - Implementations SHOULD bridge to non-blocking channels (the
//!   `gateway_framebus::FrameBus` producer is the canonical example:
//!   single atomic store + memcpy + arc swap; if a consumer is
//!   lagging, that consumer's drop counter increments and the
//!   producer is unaffected).
//! - When no tap is installed (the default), there is no allocation,
//!   no virtual call.

use std::sync::Arc;

use bytes::Bytes;
use parking_lot::RwLock;

/// Observes outbound byte chunks on a tube's data channels.
///
/// Registered via [`crate::Tube::set_outbound_tap`] and invoked once
/// per `WebRTCDataChannel::send` call, after the closing
/// check and before the underlying RTCDataChannel write.
///
/// `channel_label` is the data-channel label (e.g. `"control"` or
/// `"tunnel"`). `bytes` is the chunk being sent — the same `Bytes`
/// the gateway handed to `WebRTCDataChannel::send`.
pub trait TubeDataTap: Send + Sync + 'static {
    /// Called for every outbound chunk. MUST NOT block. SHOULD NOT
    /// allocate beyond a refcount bump.
    fn on_outbound(&self, channel_label: &str, bytes: &Bytes);

    /// Called immediately AFTER each successful read of raw bytes
    /// from a backend TCP socket (guacd, direct-target tunnel, DB
    /// proxy) in `channel::connections::setup_outbound_task`,
    /// BEFORE the channel layer applies its framing/multiplexing
    /// envelope.
    ///
    /// This is the right tap for **session recording** and **AI
    /// threat detection** consumers that need raw protocol bytes
    /// (e.g., raw Guacamole instructions for the .ses recording
    /// player). The existing [`Self::on_outbound`] tap fires
    /// AFTER framing — useful for wire-level mirroring but wrong
    /// for protocol-level analysis.
    ///
    /// `conn_no` identifies the per-channel connection slot (one
    /// channel may multiplex multiple TCP backend connections; for
    /// guacd-mode there is typically one primary conn_no).
    ///
    /// **Hot-path contract**: same as `on_outbound` — MUST NOT
    /// block, MUST NOT allocate beyond a refcount bump. The tap is
    /// invoked inside the read loop with TCP_NODELAY semantics; any
    /// delay propagates to user-display latency. Default impl is
    /// no-op so existing TubeDataTap implementors are unaffected.
    fn on_raw_inbound(&self, _channel_label: &str, _conn_no: u32, _bytes: &[u8]) {
        // default: tap not interested in raw inbound; ignore
    }

    /// Called immediately BEFORE each successful write of raw bytes
    /// to a backend TCP socket (guacd, direct-target tunnel, DB
    /// proxy) in `models::backend_task_runner`, AFTER the
    /// channel layer has stripped its framing/multiplexing envelope.
    ///
    /// Symmetric to [`Self::on_raw_inbound`] — that tap observes
    /// bytes the gateway READ from the backend; this one observes
    /// bytes the gateway WRITES to the backend. Both fire on the raw
    /// protocol stream (Guacamole instructions for guacd-backed
    /// sessions), with channel-protocol framing already removed.
    ///
    /// **This is the right tap for keystroke-based AI detection** —
    /// Guacamole `key.<keysym>;` instructions only flow client→server
    /// and only this tap sees them as raw protocol.
    /// `on_outbound` (post-framing wire mirror) and `on_raw_inbound`
    /// (server→client direction) both miss them.
    ///
    /// `conn_no` mirrors `on_raw_inbound`'s — per-channel connection
    /// slot identifier.
    ///
    /// **Hot-path contract**: same as the other taps — MUST NOT
    /// block, MUST NOT allocate beyond a refcount bump. The tap fires
    /// in the backend-write task; any delay throttles user input.
    /// Default impl is no-op so existing TubeDataTap implementors are
    /// unaffected.
    fn on_raw_outbound(&self, _channel_label: &str, _conn_no: u32, _bytes: &[u8]) {
        // default: tap not interested in raw outbound; ignore
    }
}

/// Convenience: a function-based tap. Boxed closures sometimes feel
/// nicer than implementing a trait for a one-off.
pub struct FnTap<F>(F)
where
    F: Fn(&str, &Bytes) + Send + Sync + 'static;

impl<F> FnTap<F>
where
    F: Fn(&str, &Bytes) + Send + Sync + 'static,
{
    /// Wrap a closure as a [`TubeDataTap`].
    pub fn new(f: F) -> Self {
        Self(f)
    }
}

impl<F> TubeDataTap for FnTap<F>
where
    F: Fn(&str, &Bytes) + Send + Sync + 'static,
{
    fn on_outbound(&self, channel_label: &str, bytes: &Bytes) {
        (self.0)(channel_label, bytes);
    }
}

/// Internal storage used by `WebRTCDataChannel` and
/// [`crate::Tube`]. Re-exported for completeness; you generally
/// only need the trait + the `set_outbound_tap` method.
///
/// Cloned `Arc<TapSlot>` views share the same slot across all of a
/// tube's data channels — `Tube::set_outbound_tap` updates the slot
/// in-place and every channel that holds a clone observes the change.
pub type TapSlot = RwLock<Option<Arc<dyn TubeDataTap>>>;

/// Construct a fresh empty slot. Cheap; `Arc<TapSlot>` clones share
/// the same underlying lock.
pub fn empty_slot() -> Arc<TapSlot> {
    Arc::new(RwLock::new(None))
}

/// Set the slot. Cheap (write lock; called at session start).
///
/// The previous tap (if any) is dropped AFTER the write lock is
/// released. `parking_lot::RwLock` is not reentrant, so a tap whose
/// `Drop` touches the slot would self-deadlock, and a slow `Drop`
/// (flush/join) would stall every in-flight `send()` on the tube.
pub fn set(slot: &TapSlot, tap: Arc<dyn TubeDataTap>) {
    let previous = {
        let mut guard = slot.write();
        guard.replace(tap)
    };
    drop(previous);
}

/// Clear the slot. Cheap (write lock; called at session end).
///
/// Same ordering guarantee as [`set`]: the removed tap is dropped
/// outside the write lock.
pub fn clear(slot: &TapSlot) {
    let previous = {
        let mut guard = slot.write();
        guard.take()
    };
    drop(previous);
}

/// Hot-path read: returns a clone of the inner Arc if a tap is
/// installed, None otherwise. The clone is a single atomic refcount
/// bump; the read lock is held only for that bump.
#[inline]
pub fn snapshot(slot: &TapSlot) -> Option<Arc<dyn TubeDataTap>> {
    slot.read().clone()
}
