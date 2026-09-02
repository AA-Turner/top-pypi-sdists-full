use crate::dirty_tracker::RbiDirtyTracker;

#[test]
fn test_dirty_tracker_new() {
    let tracker = RbiDirtyTracker::new();
    assert_eq!(tracker.frames_captured, 0);
    assert_eq!(tracker.frames_sent, 0);
    assert_eq!(tracker.frames_skipped, 0);
}

#[test]
fn test_first_frame_always_changes() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot = vec![1, 2, 3, 4];
    assert!(tracker.has_changed(&screenshot));
    assert_eq!(tracker.frames_captured, 1);
    assert_eq!(tracker.frames_sent, 1);
    assert_eq!(tracker.frames_skipped, 0);
}

#[test]
fn test_identical_frames_skipped() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot = vec![1, 2, 3, 4];

    assert!(tracker.has_changed(&screenshot));

    assert!(!tracker.has_changed(&screenshot));
    assert_eq!(tracker.frames_captured, 2);
    assert_eq!(tracker.frames_sent, 1);
    assert_eq!(tracker.frames_skipped, 1);

    assert!(!tracker.has_changed(&screenshot));
    assert_eq!(tracker.frames_captured, 3);
    assert_eq!(tracker.frames_sent, 1);
    assert_eq!(tracker.frames_skipped, 2);
}

#[test]
fn test_changed_frames_detected() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot1 = vec![1, 2, 3, 4];
    let screenshot2 = vec![1, 2, 3, 5];

    assert!(tracker.has_changed(&screenshot1));
    assert!(tracker.has_changed(&screenshot2));
    assert_eq!(tracker.frames_sent, 2);
    assert_eq!(tracker.frames_skipped, 0);
}

#[test]
fn test_compression_ratio() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot = vec![1, 2, 3, 4];

    tracker.has_changed(&screenshot);

    for _ in 0..9 {
        tracker.has_changed(&screenshot);
    }

    assert_eq!(tracker.compression_ratio(), 90.0);
}

#[test]
fn test_change_percentage() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot1 = vec![1, 2, 3, 4];
    let screenshot2 = vec![1, 2, 3, 5];

    tracker.has_changed(&screenshot1);
    let change_pct = tracker.change_percentage(&screenshot2);
    assert_eq!(change_pct, Some(25.0));
}

#[test]
fn test_stats() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot = vec![1, 2, 3, 4];

    tracker.has_changed(&screenshot);
    tracker.has_changed(&screenshot);
    tracker.has_changed(&screenshot);

    let stats = tracker.stats();
    assert_eq!(stats.frames_captured, 3);
    assert_eq!(stats.frames_sent, 1);
    assert_eq!(stats.frames_skipped, 2);
}

#[test]
fn test_reset_stats() {
    let mut tracker = RbiDirtyTracker::new();
    let screenshot = vec![1, 2, 3, 4];

    tracker.has_changed(&screenshot);
    tracker.has_changed(&screenshot);

    tracker.reset_stats();

    let stats = tracker.stats();
    assert_eq!(stats.frames_captured, 0);
    assert_eq!(stats.frames_sent, 0);
    assert_eq!(stats.frames_skipped, 0);
}
