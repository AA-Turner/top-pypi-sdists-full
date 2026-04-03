use crate::cursor::{CursorManager, StandardCursor};

#[test]
fn test_cursor_manager_new() {
    let mgr = CursorManager::new(true, true, 85);
    assert_eq!(mgr.jpeg_quality, 85);
    assert!(mgr.supports_jpeg);
    assert!(mgr.supports_webp);
}

#[test]
fn test_send_standard_cursor_pointer() {
    let mut mgr = CursorManager::new(false, false, 85);
    let result = mgr.send_standard_cursor(StandardCursor::Pointer);
    assert!(result.is_ok());
    let instructions = result.unwrap();
    assert_eq!(instructions.len(), 5); // size, img, blob, end, cursor
    assert!(instructions[0].starts_with("4.size"));
    assert!(instructions[1].starts_with("3.img"));
    assert!(instructions[2].starts_with("4.blob"));
    assert!(instructions[3].starts_with("3.end"));
    assert!(instructions[4].starts_with("6.cursor"));
    // cursor instruction must reference layer -1 (numeric), not a name string
    assert!(instructions[4].contains("-1"));
}

#[test]
fn test_send_standard_cursor_none() {
    let mut mgr = CursorManager::new(false, false, 85);
    let result = mgr.send_standard_cursor(StandardCursor::None);
    assert!(result.is_ok());
    let instructions = result.unwrap();
    assert_eq!(instructions.len(), 5); // size, img, blob, end, cursor
                                       // Hidden cursor: 1x1 at hotspot (0,0)
    assert!(instructions[4].starts_with("6.cursor"));
}

#[test]
fn test_send_standard_cursor_ibeam() {
    let mut mgr = CursorManager::new(false, false, 85);
    let result = mgr.send_standard_cursor(StandardCursor::IBeam);
    assert!(result.is_ok());
    let instructions = result.unwrap();
    assert_eq!(instructions.len(), 5); // size, img, blob, end, cursor
}

#[test]
fn test_send_standard_cursor_dot() {
    let mut mgr = CursorManager::new(false, false, 85);
    let result = mgr.send_standard_cursor(StandardCursor::Dot);
    assert!(result.is_ok());
    let instructions = result.unwrap();
    assert_eq!(instructions.len(), 5); // size, img, blob, end, cursor
}

#[test]
fn test_send_custom_cursor() {
    let mut mgr = CursorManager::new(false, false, 85);

    // Create a simple 2x2 red cursor
    let rgba_data = vec![
        255, 0, 0, 255, // Red pixel
        255, 0, 0, 255, // Red pixel
        255, 0, 0, 255, // Red pixel
        255, 0, 0, 255, // Red pixel
    ];

    let result = mgr.send_custom_cursor(&rgba_data, 2, 2, 1, 1);
    assert!(result.is_ok());

    let instructions = result.unwrap();
    assert_eq!(instructions.len(), 5); // size, img, blob, end, cursor
    assert!(instructions[0].starts_with("4.size"));
    assert!(instructions[1].starts_with("3.img"));
    assert!(instructions[2].starts_with("4.blob"));
    assert!(instructions[3].starts_with("3.end"));
    assert!(instructions[4].starts_with("6.cursor"));
}
