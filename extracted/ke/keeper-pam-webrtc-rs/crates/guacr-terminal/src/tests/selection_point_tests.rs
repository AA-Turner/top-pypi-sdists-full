use crate::emulator::TerminalEmulator;
use crate::selection_point::{points_enclose_text, ColumnSide, SelectionPoint};

// Helper function to create a test terminal
fn create_test_terminal() -> TerminalEmulator {
    TerminalEmulator::new_with_scrollback(24, 80, 1000)
}

#[test]
fn test_column_side_ordering() {
    // Left comes before Right on same column
    assert!(!(ColumnSide::Left == ColumnSide::Right));
}

#[test]
fn test_point_is_after_same_point() {
    let terminal = create_test_terminal();
    let point1 = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);
    let point2 = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);

    // Same point is not after itself
    assert!(!point1.is_after(&point2));
    assert!(!point2.is_after(&point1));
}

#[test]
fn test_point_is_after_different_rows() {
    let terminal = create_test_terminal();
    let point1 = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);
    let point2 = SelectionPoint::new(2, 1, ColumnSide::Left, &terminal);

    assert!(!point1.is_after(&point2));
    assert!(point2.is_after(&point1));
}

#[test]
fn test_point_is_after_different_columns() {
    let terminal = create_test_terminal();
    let point1 = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);
    let point2 = SelectionPoint::new(1, 2, ColumnSide::Left, &terminal);

    assert!(!point1.is_after(&point2));
    assert!(point2.is_after(&point1));
}

#[test]
fn test_point_is_after_different_sides() {
    let terminal = create_test_terminal();
    let point1 = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);
    let point2 = SelectionPoint::new(1, 1, ColumnSide::Right, &terminal);

    assert!(!point1.is_after(&point2));
    assert!(point2.is_after(&point1));
}

#[test]
fn test_round_up() {
    let _terminal = create_test_terminal();

    // Left side of column - stays at column
    let point = SelectionPoint {
        row: 1,
        column: 1,
        side: ColumnSide::Left,
        char_starting_column: 1,
        char_width: 1,
    };
    assert_eq!(point.round_up(), 1);

    // Right side of column - rounds to next column
    let point = SelectionPoint {
        row: 1,
        column: 1,
        side: ColumnSide::Right,
        char_starting_column: 1,
        char_width: 1,
    };
    assert_eq!(point.round_up(), 2);
}

#[test]
fn test_round_down() {
    let _terminal = create_test_terminal();

    // Right side of column - stays at column
    let point = SelectionPoint {
        row: 1,
        column: 1,
        side: ColumnSide::Right,
        char_starting_column: 1,
        char_width: 1,
    };
    assert_eq!(point.round_down(), 1);

    // Left side of column - rounds to previous column
    let point = SelectionPoint {
        row: 1,
        column: 1,
        side: ColumnSide::Left,
        char_starting_column: 1,
        char_width: 1,
    };
    assert_eq!(point.round_down(), 0);
}

#[test]
fn test_points_enclose_text_different_rows() {
    let terminal = create_test_terminal();
    let start = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);
    let end = SelectionPoint::new(2, 1, ColumnSide::Left, &terminal);

    assert!(points_enclose_text(&start, &end));
}

#[test]
fn test_points_enclose_text_same_position() {
    let terminal = create_test_terminal();
    let start = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);
    let end = SelectionPoint::new(1, 1, ColumnSide::Left, &terminal);

    assert!(!points_enclose_text(&start, &end));
}
