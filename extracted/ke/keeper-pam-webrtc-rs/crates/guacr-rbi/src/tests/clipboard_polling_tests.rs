use crate::clipboard_polling::{ClipboardPollingConfig, ClipboardState};

#[test]
fn test_clipboard_state() {
    let mut state = ClipboardState::new();

    assert!(state.has_changed("Hello"));
    assert_eq!(state.last_content(), "Hello");

    assert!(!state.has_changed("Hello"));

    assert!(state.has_changed("World"));
    assert_eq!(state.last_content(), "World");
}

#[test]
fn test_config_default() {
    let config = ClipboardPollingConfig::default();
    assert!(config.enabled);
    assert_eq!(config.interval_ms, 500);
}
