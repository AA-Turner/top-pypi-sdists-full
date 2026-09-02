use crate::throughput::ThroughputTracker;
use std::thread;
use std::time::Duration;

#[test]
fn test_throughput_calculation() {
    let mut tracker = ThroughputTracker::new(10);

    // Simulate sending 1MB over 1 second = 8 Mbps
    tracker.track_sent(1_000_000);
    thread::sleep(Duration::from_millis(100));
    tracker.track_sent(1_000_000);

    let throughput = tracker.throughput_mbps();
    assert!(throughput > 0.0);
}

#[test]
fn test_window_size_limit() {
    let mut tracker = ThroughputTracker::new(3);

    for _ in 0..10 {
        tracker.track_sent(1000);
    }

    assert_eq!(tracker.sample_count(), 3);
}
