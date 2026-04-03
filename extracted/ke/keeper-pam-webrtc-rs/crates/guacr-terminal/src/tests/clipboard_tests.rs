use crate::clipboard::{
    RdpClipboard, CLIPBOARD_DEFAULT_SIZE, CLIPBOARD_MAX_SIZE, CLIPBOARD_MIN_SIZE,
};

#[test]
fn test_clipboard_new() {
    let clipboard = RdpClipboard::new(1024 * 1024); // 1MB
    assert_eq!(clipboard.buffer_size(), 1024 * 1024);
}

#[test]
fn test_clipboard_size_validation() {
    // Too small - should use minimum
    let clipboard = RdpClipboard::new(1024);
    assert_eq!(clipboard.buffer_size(), CLIPBOARD_MIN_SIZE);

    // Too large - should use maximum
    let clipboard = RdpClipboard::new(100 * 1024 * 1024);
    assert_eq!(clipboard.buffer_size(), CLIPBOARD_MAX_SIZE);

    // Valid size
    let clipboard = RdpClipboard::new(1024 * 1024);
    assert_eq!(clipboard.buffer_size(), 1024 * 1024);
}

#[test]
fn test_clipboard_default() {
    let clipboard = RdpClipboard::default();
    assert_eq!(clipboard.buffer_size(), CLIPBOARD_DEFAULT_SIZE);
}
