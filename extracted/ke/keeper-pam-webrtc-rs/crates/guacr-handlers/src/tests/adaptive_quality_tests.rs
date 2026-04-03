use crate::adaptive_quality::AdaptiveQuality;
use std::thread;
use std::time::Duration;

#[test]
fn test_initial_quality() {
    let aq = AdaptiveQuality::new(85);
    assert_eq!(aq.current_quality(), 85);
}

#[test]
fn test_quality_bounds() {
    let aq = AdaptiveQuality::new(200); // Invalid, should clamp
    assert_eq!(aq.max_quality(), 100);
}

#[test]
fn test_rate_limiting() {
    let mut aq = AdaptiveQuality::new(85);

    // Track some frames to simulate low bandwidth
    for _ in 0..5 {
        aq.track_frame_sent(100);
        thread::sleep(Duration::from_millis(10));
    }

    let q1 = aq.calculate_quality();
    let q2 = aq.calculate_quality(); // Should return same due to rate limit

    assert_eq!(q1, q2);
}

#[test]
fn test_reset() {
    let mut aq = AdaptiveQuality::new(85);
    aq.current_quality = 20; // Simulate degraded quality
    aq.reset();
    assert_eq!(aq.current_quality(), 85);
}
