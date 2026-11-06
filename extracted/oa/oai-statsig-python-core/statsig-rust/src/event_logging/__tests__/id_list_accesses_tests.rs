use super::{IdListAccessRecorder, IdListAccesses};
use parking_lot::RwLock;
use std::sync::Barrier;

#[test]
fn repeated_accesses_and_flushes_report_once() {
    let accesses = RwLock::new(IdListAccesses::default());
    for _ in 0..32 {
        accesses.record("members");
    }
    assert_eq!(
        std::mem::take(&mut accesses.write().pending),
        ["members".to_owned()]
    );
    accesses.record("members");
    assert!(accesses.read().pending.is_empty());
}

#[test]
fn list_names_and_instances_have_independent_access_records() {
    let first = RwLock::new(IdListAccesses::default());
    let second = RwLock::new(IdListAccesses::default());
    first.record("first");
    first.record("second");
    second.record("first");
    assert_eq!(
        first.read().pending,
        ["first".to_owned(), "second".to_owned()]
    );
    assert_eq!(second.read().pending, ["first".to_owned()]);
}

#[test]
fn concurrent_first_accesses_emit_once() {
    let accesses = RwLock::new(IdListAccesses::default());
    let barrier = Barrier::new(16);
    std::thread::scope(|scope| {
        for _ in 0..16 {
            scope.spawn(|| {
                barrier.wait();
                accesses.record("members");
            });
        }
    });
    assert_eq!(accesses.read().pending, ["members".to_owned()]);
}

#[test]
fn discarding_pending_allows_retry_without_replaying_flushed_accesses() {
    let accesses = RwLock::new(IdListAccesses::default());
    accesses.record("flushed");
    assert_eq!(
        std::mem::take(&mut accesses.write().pending),
        ["flushed".to_owned()]
    );
    accesses.record("pending-first");
    accesses.record("pending-second");
    accesses.write().discard_pending();
    assert!(accesses.read().pending.is_empty());

    accesses.record("flushed");
    assert!(accesses.read().pending.is_empty());
    accesses.record("pending-first");
    accesses.record("pending-second");
    assert_eq!(
        std::mem::take(&mut accesses.write().pending),
        ["pending-first".to_owned(), "pending-second".to_owned()]
    );

    // Disabling after a flush must retain every already published name.
    accesses.write().discard_pending();
    for name in ["flushed", "pending-first", "pending-second"] {
        accesses.record(name);
    }
    assert!(accesses.read().pending.is_empty());
}
