//! Tests for the public `TubeDataTap` surface.
//!
//! The tap is a hot-path hook with a documented contract — invoked once
//! per `WebRTCDataChannel::send`, byte-exact, and with no slot lock held
//! across the call. These tests pin that contract down so the tap can't
//! silently regress to "consumer sees zero bytes" (the live failure mode
//! that motivated wiring the tube-wide slot at channel construction).

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::mpsc;
use std::sync::Arc;
use std::time::Duration;

use bytes::Bytes;
use parking_lot::Mutex;

use crate::webrtc_data_tap::{self, TapSlot, TubeDataTap};

/// Records every `on_outbound` call so tests can assert call count and
/// the exact bytes/label observed.
#[derive(Default)]
struct CountingTap {
    calls: AtomicUsize,
    seen: Mutex<Vec<(String, Bytes)>>,
}

impl CountingTap {
    fn calls(&self) -> usize {
        self.calls.load(Ordering::SeqCst)
    }
}

impl TubeDataTap for CountingTap {
    fn on_outbound(&self, channel_label: &str, bytes: &Bytes) {
        self.calls.fetch_add(1, Ordering::SeqCst);
        self.seen
            .lock()
            .push((channel_label.to_string(), bytes.clone()));
    }
}

struct NoopTap;
impl TubeDataTap for NoopTap {
    fn on_outbound(&self, _channel_label: &str, _bytes: &Bytes) {}
}

/// Every production data channel is constructed with a CLONE of the
/// tube's `Arc<TapSlot>` (`WebRTCDataChannel::new_with_outbound_tap_slot`),
/// so one write to the tube slot must be observable from each channel's
/// view. This is the invariant that makes per-channel propagation loops
/// in `Tube::set_outbound_tap` / `clear_outbound_tap` unnecessary.
#[test]
fn tap_installed_on_tube_slot_is_visible_through_cloned_slot_views() {
    let tube_slot = webrtc_data_tap::empty_slot();
    let channel_view: Arc<TapSlot> = Arc::clone(&tube_slot);

    assert!(
        webrtc_data_tap::snapshot(&channel_view).is_none(),
        "no tap installed yet"
    );

    webrtc_data_tap::set(&tube_slot, Arc::new(CountingTap::default()));
    assert!(
        webrtc_data_tap::snapshot(&channel_view).is_some(),
        "a tap set on the tube slot must be visible through a channel's cloned slot view"
    );

    webrtc_data_tap::clear(&tube_slot);
    assert!(
        webrtc_data_tap::snapshot(&channel_view).is_none(),
        "clearing the tube slot must be visible through a channel's cloned slot view"
    );
}

/// `set`/`clear` must not run the previous tap's `Drop` while holding the
/// slot's write lock. `parking_lot::RwLock` is NOT reentrant, so a `Drop`
/// that touches the slot (e.g. a recording sink that flushes through its
/// own handle) self-deadlocks; and any slow `Drop` stalls every in-flight
/// `send()` on that tube.
#[test]
fn replacing_a_tap_does_not_drop_the_previous_one_under_the_slot_lock() {
    struct DropTouchesSlot {
        slot: Arc<TapSlot>,
    }
    impl TubeDataTap for DropTouchesSlot {
        fn on_outbound(&self, _channel_label: &str, _bytes: &Bytes) {}
    }
    impl Drop for DropTouchesSlot {
        fn drop(&mut self) {
            // Reading the slot from Drop must not deadlock.
            let _ = webrtc_data_tap::snapshot(&self.slot);
        }
    }

    let slot = webrtc_data_tap::empty_slot();
    webrtc_data_tap::set(
        &slot,
        Arc::new(DropTouchesSlot {
            slot: Arc::clone(&slot),
        }),
    );

    // Run the replacement on a worker thread so a deadlock fails the test
    // with a clear message instead of hanging the suite forever.
    let slot_for_worker = Arc::clone(&slot);
    let (tx, rx) = mpsc::channel();
    std::thread::spawn(move || {
        webrtc_data_tap::set(&slot_for_worker, Arc::new(NoopTap));
        let _ = tx.send(());
    });

    assert!(
        rx.recv_timeout(Duration::from_secs(5)).is_ok(),
        "replacing a tap deadlocked: the previous tap's Drop ran while the slot write lock was held"
    );
}

/// Same hazard on the clear path.
#[test]
fn clearing_a_tap_does_not_drop_it_under_the_slot_lock() {
    struct DropTouchesSlot {
        slot: Arc<TapSlot>,
    }
    impl TubeDataTap for DropTouchesSlot {
        fn on_outbound(&self, _channel_label: &str, _bytes: &Bytes) {}
    }
    impl Drop for DropTouchesSlot {
        fn drop(&mut self) {
            let _ = webrtc_data_tap::snapshot(&self.slot);
        }
    }

    let slot = webrtc_data_tap::empty_slot();
    webrtc_data_tap::set(
        &slot,
        Arc::new(DropTouchesSlot {
            slot: Arc::clone(&slot),
        }),
    );

    let slot_for_worker = Arc::clone(&slot);
    let (tx, rx) = mpsc::channel();
    std::thread::spawn(move || {
        webrtc_data_tap::clear(&slot_for_worker);
        let _ = tx.send(());
    });

    assert!(
        rx.recv_timeout(Duration::from_secs(5)).is_ok(),
        "clearing a tap deadlocked: its Drop ran while the slot write lock was held"
    );
}

/// End-to-end on a real connected data channel: the tap fires exactly
/// once per `send`, sees the exact bytes, and stops firing after `clear`.
#[tokio::test]
async fn send_invokes_the_outbound_tap_once_with_the_exact_bytes() {
    let dc = crate::tests::common_tests::create_test_webrtc_data_channel().await;

    let tap = Arc::new(CountingTap::default());
    webrtc_data_tap::set(&dc.outbound_tap, tap.clone());

    let payload = Bytes::from_static(b"tap-me");
    dc.send(payload.clone())
        .await
        .expect("send on the connected test channel should succeed");

    assert_eq!(tap.calls(), 1, "the tap must fire exactly once per send");
    {
        let seen = tap.seen.lock();
        assert_eq!(
            seen[0].1, payload,
            "the tap must observe the exact bytes handed to send"
        );
        assert!(
            !seen[0].0.is_empty(),
            "the tap must receive the data-channel label"
        );
    }

    // After clear, the hot path returns to the no-tap fast path.
    webrtc_data_tap::clear(&dc.outbound_tap);
    dc.send(Bytes::from_static(b"after-clear"))
        .await
        .expect("send after clear should still succeed");
    assert_eq!(
        tap.calls(),
        1,
        "a cleared tap must not observe any further sends"
    );
}
