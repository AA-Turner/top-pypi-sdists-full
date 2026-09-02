use crate::scroll_detector::{
    format_scroll_instruction, ScrollDetector, ScrollPosition, ScrollStats,
};
use std::thread;
use std::time::Duration;

#[test]
fn test_scroll_position() {
    let pos = ScrollPosition::new(100, 200, 1000, 2000);
    assert_eq!(pos.x, 100);
    assert_eq!(pos.y, 200);
    assert!(!pos.is_at_top());
    assert!(!pos.is_at_bottom());
    assert!(!pos.is_at_left());
    assert!(!pos.is_at_right());
}

#[test]
fn test_scroll_position_edges() {
    let pos = ScrollPosition::new(0, 0, 1000, 2000);
    assert!(pos.is_at_top());
    assert!(pos.is_at_left());

    let pos = ScrollPosition::new(1000, 2000, 1000, 2000);
    assert!(pos.is_at_bottom());
    assert!(pos.is_at_right());
}

#[test]
fn test_scroll_delta() {
    let pos1 = ScrollPosition::new(100, 200, 1000, 2000);
    let pos2 = ScrollPosition::new(150, 250, 1000, 2000);

    let (dx, dy) = pos2.delta_from(&pos1);
    assert_eq!(dx, 50);
    assert_eq!(dy, 50);
}

#[test]
fn test_scroll_detector() {
    let mut detector = ScrollDetector::new();

    let pos1 = ScrollPosition::new(0, 0, 1000, 2000);
    assert_eq!(detector.update(pos1), None);

    let pos2 = ScrollPosition::new(0, 100, 1000, 2000);
    assert_eq!(detector.update(pos2), Some((0, 100)));

    assert_eq!(detector.update(pos2), None);

    let pos3 = ScrollPosition::new(50, 150, 1000, 2000);
    assert_eq!(detector.update(pos3), Some((50, 50)));

    let stats = detector.stats();
    assert_eq!(stats.scroll_events, 2);
    assert_eq!(stats.total_distance_x, 50);
    assert_eq!(stats.total_distance_y, 150);
}

#[test]
fn test_scroll_stats() {
    let stats = ScrollStats {
        scroll_events: 4,
        total_distance_x: 200,
        total_distance_y: 400,
    };

    let (avg_x, avg_y) = stats.avg_distance_per_scroll();
    assert_eq!(avg_x, 50.0);
    assert_eq!(avg_y, 100.0);
}

#[test]
fn test_format_scroll_instruction() {
    let instr = format_scroll_instruction(0, 0, -100);
    assert!(instr.contains("8")); // Scroll up

    let instr = format_scroll_instruction(0, 0, 100);
    assert!(instr.contains("16")); // Scroll down

    let instr = format_scroll_instruction(0, 0, 0);
    assert!(instr.is_empty()); // No scroll
}

#[test]
fn test_scroll_velocity() {
    let mut detector = ScrollDetector::new();

    let pos1 = ScrollPosition::new(0, 0, 1000, 2000);
    detector.update(pos1);

    thread::sleep(Duration::from_millis(100));

    let pos2 = ScrollPosition::new(0, 100, 1000, 2000);
    detector.update(pos2);

    let velocity = detector.velocity();
    assert!(velocity > 500.0 && velocity < 1500.0);
}

#[test]
fn test_is_scrolling() {
    let mut detector = ScrollDetector::new();

    assert!(!detector.is_scrolling());

    let pos1 = ScrollPosition::new(0, 0, 1000, 2000);
    detector.update(pos1);
    let pos2 = ScrollPosition::new(0, 100, 1000, 2000);
    detector.update(pos2);

    assert!(detector.is_scrolling());
}

#[test]
fn test_scroll_heuristics() {
    let detector = ScrollDetector::new();

    assert!(!detector.is_significant_scroll(5, 1000));
    assert!(detector.is_significant_scroll(60, 1000));
    assert!(detector.is_page_scroll(850, 1000));
    assert!(!detector.is_page_scroll(500, 1000));
}
