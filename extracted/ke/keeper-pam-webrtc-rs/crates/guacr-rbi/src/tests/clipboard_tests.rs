use crate::clipboard::{
    RbiClipboard, CLIPBOARD_DEFAULT_SIZE, CLIPBOARD_MAX_SIZE, CLIPBOARD_MIN_SIZE,
};

#[test]
fn test_clipboard_new() {
    let clipboard = RbiClipboard::new(1024 * 1024);
    assert_eq!(clipboard.buffer_size(), 1024 * 1024);
}

#[test]
fn test_clipboard_size_validation() {
    let clipboard = RbiClipboard::new(1024);
    assert_eq!(clipboard.buffer_size(), CLIPBOARD_MIN_SIZE);

    let clipboard = RbiClipboard::new(100 * 1024 * 1024);
    assert_eq!(clipboard.buffer_size(), CLIPBOARD_MAX_SIZE);
}

#[test]
fn test_browser_clipboard() {
    let mut clipboard = RbiClipboard::new(CLIPBOARD_DEFAULT_SIZE);

    let data = b"Hello, World!";
    let result = clipboard.handle_browser_clipboard(data, "text/plain");

    assert!(result.is_ok());
    assert!(result.unwrap().is_some());
    assert_eq!(clipboard.get_data().unwrap(), data.to_vec());
    assert_eq!(clipboard.mimetype(), "text/plain");
}

#[test]
fn test_client_clipboard() {
    let mut clipboard = RbiClipboard::new(CLIPBOARD_DEFAULT_SIZE);

    let data = b"Paste this!";
    let result = clipboard.handle_client_clipboard(data, "text/plain");

    assert!(result.is_ok());
    let returned_data = result.unwrap().unwrap();
    assert_eq!(returned_data, data.to_vec());
}

#[test]
fn test_copy_disabled() {
    let mut clipboard = RbiClipboard::new(CLIPBOARD_DEFAULT_SIZE);
    clipboard.set_restrictions(true, false);

    let data = b"Secret data";
    let result = clipboard.handle_browser_clipboard(data, "text/plain");

    assert!(result.is_ok());
    assert!(result.unwrap().is_none());
}

#[test]
fn test_paste_disabled() {
    let mut clipboard = RbiClipboard::new(CLIPBOARD_DEFAULT_SIZE);
    clipboard.set_restrictions(false, true);

    let data = b"Paste attempt";
    let result = clipboard.handle_client_clipboard(data, "text/plain");

    assert!(result.is_ok());
    assert!(result.unwrap().is_none());
}
