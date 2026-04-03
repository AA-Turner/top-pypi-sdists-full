use crate::dirty_tracker::{DirtyRect, DirtyTracker};

#[test]
fn test_dirty_rect_empty() {
    let rect = DirtyRect::new();
    assert!(rect.is_empty());
}

#[test]
fn test_dirty_rect_expand() {
    let mut rect = DirtyRect::new();
    rect.expand_to(5, 10);
    rect.expand_to(8, 15);

    assert_eq!(rect.min_row, 5);
    assert_eq!(rect.max_row, 8);
    assert_eq!(rect.min_col, 10);
    assert_eq!(rect.max_col, 15);
    assert_eq!(rect.width(), 6);
    assert_eq!(rect.height(), 4);
    assert_eq!(rect.cell_count(), 24);
}

#[test]
fn test_dirty_tracker() {
    let mut tracker = DirtyTracker::new(24, 80);

    // Create screen via Parser (Screen::new is private)
    let parser = vt100::Parser::new(24, 80, 0);
    let screen = parser.screen();

    // First check - cursor is visible by default at (0,0), so we expect a dirty region
    let dirty = tracker.find_dirty_region(screen);
    assert!(dirty.is_some());

    // Verify cursor position is marked dirty
    if let Some(rect) = dirty {
        assert_eq!(rect.min_row, 0);
        assert_eq!(rect.min_col, 0);
    }

    // Second check - no changes, so no dirty region
    let dirty2 = tracker.find_dirty_region(screen);
    assert!(dirty2.is_none());

    // Note: In real usage, terminal.process(data) modifies the screen
    // and dirty tracker detects those changes
}
