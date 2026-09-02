use crate::drag_detector::DragDetector;

#[test]
fn test_no_drag_without_mouse() {
    let mut d = DragDetector::new(1920, 1080);

    // Graphics updates without mouse should not trigger drag
    for _ in 0..10 {
        d.notify_graphics_update(1920, 1080);
    }
    assert!(!d.is_dragging());
}

#[test]
fn test_no_drag_without_movement() {
    let mut d = DragDetector::new(1920, 1080);

    // Button down but no movement
    d.notify_mouse_event(100, 100, 1);
    for _ in 0..10 {
        d.notify_graphics_update(1920, 1080);
    }
    assert!(!d.is_dragging());
}

#[test]
fn test_drag_detected() {
    let mut d = DragDetector::new(1920, 1080);

    // Press button
    d.notify_mouse_event(100, 100, 1);
    // Move past threshold
    d.notify_mouse_event(120, 120, 1);
    assert!(!d.is_dragging()); // Not yet -- need updates

    // Rapid large updates
    d.notify_graphics_update(1920, 1080);
    d.notify_graphics_update(1920, 1080);
    assert!(!d.is_dragging()); // Only 2

    d.notify_graphics_update(1920, 1080);
    assert!(d.is_dragging()); // 3rd update triggers
}

#[test]
fn test_drag_ends_on_release() {
    let mut d = DragDetector::new(1920, 1080);

    // Start drag
    d.notify_mouse_event(100, 100, 1);
    d.notify_mouse_event(120, 120, 1);
    d.notify_graphics_update(1920, 1080);
    d.notify_graphics_update(1920, 1080);
    d.notify_graphics_update(1920, 1080);
    assert!(d.is_dragging());

    // Release
    d.notify_mouse_event(150, 150, 0);
    assert!(!d.is_dragging());
    assert!(d.drag_ended());
}

#[test]
fn test_small_updates_dont_trigger() {
    let mut d = DragDetector::new(1920, 1080);

    d.notify_mouse_event(100, 100, 1);
    d.notify_mouse_event(120, 120, 1);

    // Small updates (100x100 is <1% of 1920x1080)
    for _ in 0..10 {
        d.notify_graphics_update(100, 100);
    }
    assert!(!d.is_dragging());
}

#[test]
fn test_drag_delta() {
    let mut d = DragDetector::new(1920, 1080);

    d.notify_mouse_event(100, 200, 1);
    d.notify_mouse_event(115, 210, 1);

    assert_eq!(d.drag_delta(), (15, 10));
}

#[test]
fn test_resize_resets_state() {
    let mut d = DragDetector::new(1920, 1080);

    // Start drag
    d.notify_mouse_event(100, 100, 1);
    d.notify_mouse_event(120, 120, 1);
    d.notify_graphics_update(1920, 1080);
    d.notify_graphics_update(1920, 1080);
    d.notify_graphics_update(1920, 1080);
    assert!(d.is_dragging());

    // Resize resets
    d.resize(2560, 1440);
    assert!(!d.is_dragging());
}
