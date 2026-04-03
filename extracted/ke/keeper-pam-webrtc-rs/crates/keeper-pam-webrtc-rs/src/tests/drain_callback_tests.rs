use bytes::Bytes;
use crossbeam_queue::SegQueue;
use std::sync::atomic::{AtomicU32, AtomicUsize, Ordering};

fn make_frame(seq: u32) -> Bytes {
    Bytes::from(seq.to_be_bytes().to_vec())
}

fn seq_of(frame: &Bytes) -> u32 {
    u32::from_be_bytes(frame[..4].try_into().unwrap())
}

/// Simulate the drain callback logic with a controllable "send" function.
/// Returns the sequence numbers in the order they were "sent".
fn simulate_drain_cycle(
    pending: &SegQueue<Bytes>,
    requeue: &SegQueue<Bytes>,
    queue_size: &AtomicUsize,
    batch_size: usize,
    send_fn: &dyn Fn(&Bytes) -> bool,
) -> Vec<u32> {
    let mut to_send = Vec::with_capacity(batch_size);

    // Pop requeue FIRST (priority), then pending
    while to_send.len() < batch_size {
        match requeue.pop() {
            Some(frame) => to_send.push(frame),
            None => break,
        }
    }
    while to_send.len() < batch_size {
        match pending.pop() {
            Some(frame) => to_send.push(frame),
            None => break,
        }
    }

    queue_size.fetch_sub(to_send.len(), Ordering::AcqRel);

    let mut sent = Vec::new();
    let mut failed_at = to_send.len();

    for (i, frame) in to_send.iter().enumerate() {
        if send_fn(frame) {
            sent.push(seq_of(frame));
        } else {
            failed_at = i;
            break;
        }
    }

    // Re-queue unsent frames to the separate requeue
    if failed_at < to_send.len() {
        let unsent = &to_send[failed_at..];
        for frame in unsent {
            requeue.push(frame.clone());
        }
        queue_size.fetch_add(unsent.len(), Ordering::AcqRel);
    }

    sent
}

#[test]
fn test_drain_no_failures_sends_all() {
    let pending = SegQueue::new();
    let requeue = SegQueue::new();
    let queue_size = AtomicUsize::new(5);

    for i in 0..5 {
        pending.push(make_frame(i));
    }

    let sent = simulate_drain_cycle(&pending, &requeue, &queue_size, 10, &|_| true);

    assert_eq!(sent, vec![0, 1, 2, 3, 4]);
    assert_eq!(queue_size.load(Ordering::Acquire), 0);
    assert!(requeue.pop().is_none());
}

#[test]
fn test_drain_partial_failure_requeues_unsent() {
    let pending = SegQueue::new();
    let requeue = SegQueue::new();
    let queue_size = AtomicUsize::new(5);

    for i in 0..5 {
        pending.push(make_frame(i));
    }

    // Fail on frame #2 (seq=2)
    let sent = simulate_drain_cycle(&pending, &requeue, &queue_size, 10, &|f| seq_of(f) < 2);

    assert_eq!(sent, vec![0, 1], "Only F0, F1 should be sent");
    assert_eq!(
        queue_size.load(Ordering::Acquire),
        3,
        "F2, F3, F4 should be requeued"
    );

    // Verify requeue contains F2, F3, F4 in order
    assert_eq!(seq_of(&requeue.pop().unwrap()), 2);
    assert_eq!(seq_of(&requeue.pop().unwrap()), 3);
    assert_eq!(seq_of(&requeue.pop().unwrap()), 4);
    assert!(requeue.pop().is_none());
}

#[test]
fn test_requeue_drained_before_pending_preserves_ordering() {
    let pending = SegQueue::new();
    let requeue = SegQueue::new();
    let queue_size = AtomicUsize::new(0);

    // Simulate: F2, F3, F4 failed previously and are in requeue
    requeue.push(make_frame(2));
    requeue.push(make_frame(3));
    requeue.push(make_frame(4));
    queue_size.fetch_add(3, Ordering::AcqRel);

    // F5, F6, F7 arrived from producer while drain was running
    pending.push(make_frame(5));
    pending.push(make_frame(6));
    pending.push(make_frame(7));
    queue_size.fetch_add(3, Ordering::AcqRel);

    // Next drain: should send F2, F3, F4, F5, F6, F7 IN ORDER
    let sent = simulate_drain_cycle(&pending, &requeue, &queue_size, 10, &|_| true);

    assert_eq!(
        sent,
        vec![2, 3, 4, 5, 6, 7],
        "Requeued frames must precede new frames"
    );
    assert_eq!(queue_size.load(Ordering::Acquire), 0);
}

#[test]
fn test_reorder_bug_with_single_queue() {
    // Demonstrates WHY a separate requeue is needed.
    // If we re-queue to the SAME queue (pending), ordering breaks.
    let pending = SegQueue::new();
    let queue_size = AtomicUsize::new(5);

    for i in 0..5 {
        pending.push(make_frame(i));
    }

    // Pop batch, simulate partial send failure at F2
    let mut batch = Vec::new();
    for _ in 0..5 {
        batch.push(pending.pop().unwrap());
    }
    queue_size.fetch_sub(5, Ordering::AcqRel);

    // F0, F1 sent OK. F2 fails.
    // Meanwhile, producer adds F10, F11 to pending
    pending.push(make_frame(10));
    pending.push(make_frame(11));
    queue_size.fetch_add(2, Ordering::AcqRel);

    // BAD: re-queue F2, F3, F4 to TAIL of same pending queue
    for frame in &batch[2..] {
        pending.push(frame.clone());
    }
    queue_size.fetch_add(3, Ordering::AcqRel);

    // Next drain from pending: F10, F11, F2, F3, F4 — OUT OF ORDER!
    let mut drain_order = Vec::new();
    while let Some(f) = pending.pop() {
        drain_order.push(seq_of(&f));
    }

    assert_eq!(
        drain_order,
        vec![10, 11, 2, 3, 4],
        "Single-queue requeue puts F10 before F2 — REORDERING BUG"
    );

    // F10 appears before F2: this is the security vulnerability
    let idx_f2 = drain_order.iter().position(|&s| s == 2).unwrap();
    let idx_f10 = drain_order.iter().position(|&s| s == 10).unwrap();
    assert!(
        idx_f10 < idx_f2,
        "Security: F10 (new) arrives before F2 (failed) — credential data mixing"
    );
}

#[test]
fn test_multiple_drain_cycles_preserve_ordering() {
    let pending = SegQueue::new();
    let requeue = SegQueue::new();
    let queue_size = AtomicUsize::new(0);

    // Enqueue F0..F19
    for i in 0..20 {
        pending.push(make_frame(i));
        queue_size.fetch_add(1, Ordering::AcqRel);
    }

    let mut all_sent = Vec::new();
    let mut send_budget = 3u32; // Only allow 3 successful sends per cycle

    for _cycle in 0..20 {
        if queue_size.load(Ordering::Acquire) == 0 {
            break;
        }

        let cycle_sent_count = AtomicU32::new(0);
        let budget = send_budget;
        let sent = simulate_drain_cycle(&pending, &requeue, &queue_size, 5, &|_f| {
            if cycle_sent_count.load(Ordering::Acquire) < budget {
                cycle_sent_count.fetch_add(1, Ordering::AcqRel);
                true
            } else {
                false
            }
        });
        all_sent.extend(sent);

        // Increase budget over time (simulates SCTP draining)
        send_budget = (send_budget + 1).min(10);
    }

    // Verify ALL frames sent
    assert_eq!(
        all_sent.len(),
        20,
        "All 20 frames should eventually be sent"
    );

    // Verify strict ordering
    for i in 1..all_sent.len() {
        assert!(
            all_sent[i] > all_sent[i - 1],
            "Ordering violation at index {}: seq {} followed by seq {}",
            i,
            all_sent[i - 1],
            all_sent[i]
        );
    }
}

#[test]
fn test_first_frame_failure_requeues_entire_batch() {
    let pending = SegQueue::new();
    let requeue = SegQueue::new();
    let queue_size = AtomicUsize::new(3);

    pending.push(make_frame(0));
    pending.push(make_frame(1));
    pending.push(make_frame(2));

    // All sends fail
    let sent = simulate_drain_cycle(&pending, &requeue, &queue_size, 10, &|_| false);

    assert!(sent.is_empty(), "No frames should be sent");
    assert_eq!(
        queue_size.load(Ordering::Acquire),
        3,
        "All frames should be requeued"
    );

    // Verify requeue has all 3 in order
    assert_eq!(seq_of(&requeue.pop().unwrap()), 0);
    assert_eq!(seq_of(&requeue.pop().unwrap()), 1);
    assert_eq!(seq_of(&requeue.pop().unwrap()), 2);
}
