use crate::adaptive_fps::AdaptiveFps;
use std::time::Duration;

#[test]
fn test_adaptive_fps_new() {
    let fps = AdaptiveFps::new(5, 30);
    assert_eq!(fps.current_fps(), 30); // Starts at max
    assert_eq!(fps.min_fps, 5);
    assert_eq!(fps.max_fps, 30);
}

#[test]
#[should_panic(expected = "min_fps must be greater than 0")]
fn test_zero_min_fps_panics() {
    AdaptiveFps::new(0, 30);
}

#[test]
#[should_panic(expected = "max_fps must be >= min_fps")]
fn test_invalid_fps_range_panics() {
    AdaptiveFps::new(30, 5);
}

#[test]
fn test_stays_at_max_fps_when_active() {
    let mut fps = AdaptiveFps::new(5, 30);

    for _ in 0..100 {
        let interval = fps.update(true);
        assert_eq!(fps.current_fps(), 30);
        assert_eq!(interval, Duration::from_millis(33)); // ~30 FPS
    }
}

#[test]
fn test_drops_to_min_fps_when_idle() {
    let mut fps = AdaptiveFps::new(5, 30);

    fps.update(true);
    assert_eq!(fps.current_fps(), 30);

    for _ in 0..91 {
        fps.update(false);
    }

    assert_eq!(fps.current_fps(), 5);
    assert!(fps.is_idle());
}

#[test]
fn test_gradual_fps_reduction() {
    let mut fps = AdaptiveFps::new(5, 30);

    fps.update(true);
    assert_eq!(fps.current_fps(), 30);

    for _ in 0..30 {
        fps.update(false);
    }
    assert_eq!(fps.current_fps(), 30);

    fps.update(false);
    assert!(fps.current_fps() < 30);
    assert!(fps.current_fps() > 5);

    for _ in 0..60 {
        fps.update(false);
    }
    assert_eq!(fps.current_fps(), 5);
}

#[test]
fn test_immediate_recovery_on_activity() {
    let mut fps = AdaptiveFps::new(5, 30);

    fps.update(true);
    for _ in 0..91 {
        fps.update(false);
    }
    assert_eq!(fps.current_fps(), 5);

    fps.update(true);
    assert_eq!(fps.current_fps(), 30);
    assert!(fps.is_active());
}

#[test]
fn test_stats() {
    let mut fps = AdaptiveFps::new(5, 30);

    fps.update(true);
    fps.update(false);
    fps.update(false);

    let stats = fps.stats();
    assert_eq!(stats.total_frames, 3);
    assert_eq!(stats.current_fps, 30);
    assert_eq!(stats.frames_unchanged, 2);
}

#[test]
fn test_fps_changes_tracked() {
    let mut fps = AdaptiveFps::new(5, 30);

    fps.update(true);
    let initial_changes = fps.stats().fps_changes;

    for _ in 0..91 {
        fps.update(false);
    }

    let final_changes = fps.stats().fps_changes;
    assert!(final_changes > initial_changes);
}

#[test]
fn test_interval_calculation() {
    let mut fps = AdaptiveFps::new(10, 30);

    let interval = fps.update(true);
    assert_eq!(interval, Duration::from_millis(33));

    for _ in 0..91 {
        fps.update(false);
    }

    let interval = fps.update(false);
    assert_eq!(interval, Duration::from_millis(100));
}
