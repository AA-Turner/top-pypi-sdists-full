use super::*;
use std::sync::{Arc, Barrier, mpsc};
use std::thread;

#[test]
fn updates_coalesce_until_consumed() {
    let updates = ConfigUpdates::default();
    assert_eq!(updates.wait(Duration::ZERO), Some(false));
    updates.notify();
    updates.notify();
    assert_eq!(updates.wait(Duration::ZERO), Some(true));
    assert_eq!(updates.wait(Duration::ZERO), Some(false));
    updates.notify();
    assert_eq!(updates.wait(Duration::ZERO), Some(true));
}

#[test]
fn close_discards_pending_updates_and_is_permanent() {
    let updates = ConfigUpdates::default();
    updates.notify();
    updates.close();
    assert_eq!(updates.wait(Duration::ZERO), None);
    updates.notify();
    updates.close();
    assert_eq!(updates.wait(Duration::ZERO), None);
}

#[test]
fn close_wakes_waiters() {
    let updates = Arc::new(ConfigUpdates::default());
    let ready = Arc::new(Barrier::new(3));
    let (completed, results) = mpsc::channel();
    let waiters: Vec<_> = (0..2)
        .map(|_| {
            let updates = updates.clone();
            let ready = ready.clone();
            let completed = completed.clone();
            thread::spawn(move || {
                ready.wait();
                completed
                    .send(updates.wait(Duration::from_secs(30)))
                    .unwrap();
            })
        })
        .collect();
    ready.wait();
    updates.close();
    for waiter in waiters {
        assert_eq!(results.recv_timeout(Duration::from_secs(1)).unwrap(), None);
        waiter.join().unwrap();
    }
}
