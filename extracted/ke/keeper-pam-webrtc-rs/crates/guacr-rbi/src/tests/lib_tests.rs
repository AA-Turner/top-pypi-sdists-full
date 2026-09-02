// Tests from src/lib.rs - cover the public API of the guacr-rbi crate.
use crate::audio::{float_to_pcm, AudioConfig};
use crate::autofill::{
    generate_autofill_js, generate_totp, AutofillCredentials, AutofillManager, AutofillRule,
    TotpAlgorithm, TotpConfig,
};
use crate::check_url_allowed;
use crate::clipboard::{RbiClipboard, CLIPBOARD_MIN_SIZE};
use crate::cursor::CursorType;
use crate::events::{
    DisplayEvent, DisplayEventType, DisplayRect, DisplaySurface, InputEvent, UrlPattern,
};
use crate::file_upload::{detect_mime_type, UploadConfig, UploadEngine};
use crate::handler::{RbiConfig, RbiHandler};
use crate::input::{
    keysym_to_js_keycode, keysym_to_unicode, KeyboardShortcut, MouseButton, RbiInputHandler,
    KEYSYM_CTRL_LEFT, MOUSE_BUTTON_LEFT,
};
use crate::js_dialog::{JsDialogConfig, JsDialogManager, JsDialogType};
use crate::tabs::TabManager;
use guacr_handlers::ProtocolHandler;

// =========================================================================
// Core Handler Tests
// =========================================================================

#[test]
fn test_rbi_handler_new() {
    let handler = RbiHandler::with_defaults();
    assert_eq!(<_ as ProtocolHandler>::name(&handler), "http");
}

#[test]
fn test_rbi_config() {
    let config = RbiConfig::default();
    assert_eq!(config.default_width, 1920);
    assert_eq!(config.default_height, 1080);
    assert!(!config.upload_config.enabled);
}

#[tokio::test]
async fn test_rbi_handler_health_check() {
    let handler = RbiHandler::with_defaults();
    let health = handler.health_check().await;
    assert!(health.is_ok());
}

// =========================================================================
// Input Handler Tests
// =========================================================================

#[test]
fn test_input_handler_keyboard() {
    let mut handler = RbiInputHandler::new();

    let event = handler.handle_keyboard(0xFF0D, true);
    assert!(event.pressed);
    assert_eq!(event.js_key_code, 13);

    let event = handler.handle_keyboard(0xFF0D, false);
    assert!(!event.pressed);
}

#[test]
fn test_input_handler_mouse() {
    let mut handler = RbiInputHandler::new();

    let event = handler.handle_mouse(100, 200, MOUSE_BUTTON_LEFT);
    assert_eq!(event.x, 100);
    assert_eq!(event.y, 200);
    assert!(event.buttons_pressed.contains(&MouseButton::Left));
}

#[test]
fn test_input_handler_shortcuts() {
    let mut handler = RbiInputHandler::new();

    handler.handle_keyboard(KEYSYM_CTRL_LEFT, true);
    handler.handle_keyboard('c' as u32, true);

    let shortcut = handler.check_shortcut('c' as u32, true);
    assert_eq!(shortcut, Some(KeyboardShortcut::Copy));
}

#[test]
fn test_keysym_to_unicode() {
    assert_eq!(keysym_to_unicode(0xFF0D), Some('\r'));
    assert_eq!(keysym_to_unicode(0xFF09), Some('\t'));
}

#[test]
fn test_keysym_to_js_keycode() {
    assert_eq!(keysym_to_js_keycode(0xFF0D), 13);
    assert_eq!(keysym_to_js_keycode(0xFF08), 8);
    assert_eq!(keysym_to_js_keycode(0xFF09), 9);
    assert_eq!(keysym_to_js_keycode(0xFF1B), 27);
}

// =========================================================================
// Clipboard Tests
// =========================================================================

#[test]
fn test_clipboard() {
    let mut clipboard = RbiClipboard::with_defaults();
    let data = b"Test clipboard data";

    let result = clipboard.handle_browser_clipboard(data, "text/plain");
    assert!(result.is_ok());

    let stored = clipboard.get_data().unwrap();
    assert_eq!(stored, data.to_vec());
}

#[test]
fn test_clipboard_restrictions() {
    let mut clipboard = RbiClipboard::new(1024 * 1024);

    clipboard.set_restrictions(true, false);
    let result = clipboard.handle_browser_clipboard(b"test", "text/plain");
    assert!(result.is_ok());
    assert!(result.unwrap().is_none());

    clipboard.set_restrictions(false, true);
    let result = clipboard.handle_client_clipboard(b"test", "text/plain");
    assert!(result.is_ok());
    assert!(result.unwrap().is_none());
}

#[test]
fn test_clipboard_size_limits() {
    let mut clipboard = RbiClipboard::new(CLIPBOARD_MIN_SIZE);
    clipboard.set_restrictions(false, false);

    let small_data = vec![0u8; 1000];
    let result = clipboard.handle_browser_clipboard(&small_data, "text/plain");
    assert!(result.is_ok());

    let stored = clipboard.get_data();
    assert!(stored.is_ok());
    assert_eq!(stored.unwrap().len(), 1000);
}

// =========================================================================
// URL Pattern Tests
// =========================================================================

#[test]
fn test_url_patterns() {
    let patterns = vec![
        UrlPattern::parse("*.google.com").unwrap(),
        UrlPattern::parse("https://github.com").unwrap(),
    ];

    assert!(check_url_allowed("https://www.google.com", &patterns));
    assert!(check_url_allowed("https://github.com/rust-lang", &patterns));
    assert!(!check_url_allowed("https://evil.com", &patterns));
}

// =========================================================================
// Display Event Tests
// =========================================================================

#[test]
fn test_display_events() {
    let event = DisplayEvent::draw(DisplaySurface::View, DisplayRect::new(10, 20, 100, 200));
    assert_eq!(event.event_type, DisplayEventType::Draw);
    assert_eq!(event.rect.x, 10);
    assert_eq!(event.rect.width, 100);
}

#[test]
fn test_input_event_creation() {
    let event = InputEvent::keyboard(0xFF0D, true);

    if let InputEvent::Keyboard(details) = event {
        assert_eq!(details.keysym, 0xFF0D);
        assert!(details.pressed);
    } else {
        panic!("Expected keyboard event");
    }
}

// =========================================================================
// Upload Tests
// =========================================================================

#[test]
fn test_upload_config_validation() {
    let config = UploadConfig {
        enabled: true,
        allowed_extensions: vec!["pdf".to_string(), "txt".to_string()],
        blocked_extensions: vec!["exe".to_string()],
        max_size: 1024,
        max_concurrent: 3,
    };

    assert!(config.is_extension_allowed("pdf"));
    assert!(!config.is_extension_allowed("exe"));
    assert!(config.is_size_allowed(512));
    assert!(config.is_size_allowed(1024));
    assert!(!config.is_size_allowed(2048));
}

#[test]
fn test_upload_engine_workflow() {
    let config = UploadConfig {
        enabled: true,
        allowed_extensions: vec![],
        blocked_extensions: vec![],
        max_size: 1024,
        max_concurrent: 2,
    };

    let mut engine = UploadEngine::new(config);

    let request = engine.manager_mut().handle_dialog_request(false, vec![]);
    assert!(request.is_some());

    let request = request.unwrap();

    let upload_id = engine
        .start_upload(&request.id, "test.txt", "text/plain", 100)
        .unwrap();

    let progress = engine.handle_chunk(&upload_id, &[0u8; 50]).unwrap();
    assert_eq!(progress, 50.0);

    let progress = engine.handle_chunk(&upload_id, &[1u8; 50]).unwrap();
    assert_eq!(progress, 100.0);

    let (info, data) = engine.complete_upload(&upload_id).unwrap();
    assert_eq!(info.filename, "test.txt");
    assert_eq!(data.len(), 100);
}

#[test]
fn test_mime_type_detection() {
    assert_eq!(detect_mime_type("file.pdf"), "application/pdf");
    assert_eq!(detect_mime_type("image.png"), "image/png");
    assert_eq!(
        detect_mime_type("doc.docx"),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    );
    assert_eq!(detect_mime_type("unknown.xyz"), "application/octet-stream");
}

// =========================================================================
// JS Dialog Tests
// =========================================================================

#[test]
fn test_js_dialog_auto_dismiss() {
    let config = JsDialogConfig {
        show_dialogs: true,
        auto_confirm: Some(true),
        ..Default::default()
    };

    let mut manager = JsDialogManager::new(config);

    let (_, response) = manager
        .handle_dialog(
            JsDialogType::Confirm,
            "Proceed?".to_string(),
            None,
            "https://example.com".to_string(),
        )
        .unwrap();

    assert!(response.is_some());
    assert!(response.unwrap().confirmed);
}

// =========================================================================
// Autofill Tests
// =========================================================================

#[test]
fn test_autofill_rule_parsing() {
    let json = r##"{
        "page-pattern": "login.example.com",
        "username-field": "#user",
        "password-field": "//input[@type='password']",
        "submit": "button[type=submit]"
    }"##;

    let rule: AutofillRule = serde_json::from_str(json).unwrap();
    assert!(rule.page_pattern.is_some());
    assert_eq!(rule.username_field.as_deref(), Some("#user"));
    assert!(rule.password_field.as_deref().unwrap().starts_with("//"));
}

#[test]
fn test_autofill_js_generation() {
    let rules = vec![AutofillRule {
        page_pattern: Some("example.com".to_string()),
        username_field: Some("#user".to_string()),
        password_field: Some("#pass".to_string()),
        totp_field: None,
        submit: None,
        cannot_submit: None,
    }];

    let credentials = AutofillCredentials {
        username: Some("admin".to_string()),
        password: Some("secret".to_string()),
        totp_config: None,
    };

    let js = generate_autofill_js(&rules, &credentials, None, None);

    assert!(js.contains("admin"));
    assert!(js.contains("#user"));

    assert!(js.contains("iframe"));
    assert!(js.contains("contentDocument"));
}

#[test]
fn test_totp_generation() {
    let config = TotpConfig {
        secret: "JBSWY3DPEHPK3PXP".to_string(),
        digits: 6,
        period: 30,
        algorithm: TotpAlgorithm::Sha1,
    };

    let result = generate_totp(&config);
    assert!(result.is_ok());

    let (code, expiration) = result.unwrap();
    assert_eq!(code.len(), 6);
    assert!(code.chars().all(|c| c.is_ascii_digit()));
    assert!(expiration > 0);
}

// =========================================================================
// Tab Manager Tests
// =========================================================================

#[test]
fn test_tab_manager() {
    let mut manager = TabManager::new();

    let tab1 = manager.create_tab("https://example.com");
    assert!(tab1.is_some());

    let tab2 = manager.create_tab("https://google.com");
    assert!(tab2.is_some());

    assert_eq!(manager.count(), 2);

    assert!(manager.switch_to_tab(tab2.unwrap()));
    assert!(manager.active_tab().is_some());

    assert!(manager.close_tab(tab1.unwrap()));
    assert_eq!(manager.count(), 1);
}

// =========================================================================
// Cursor Tests
// =========================================================================

#[test]
fn test_cursor_type_parsing() {
    assert_eq!(CursorType::from_css("pointer"), CursorType::Pointer);
    assert_eq!(CursorType::from_css("text"), CursorType::Text);
    assert_eq!(CursorType::from_css("wait"), CursorType::Wait);
    assert_eq!(CursorType::from_css("unknown"), CursorType::Default);
}

// =========================================================================
// Audio Tests
// =========================================================================

#[test]
fn test_audio_config_defaults() {
    let config = AudioConfig::default();
    assert_eq!(config.channels, 2);
    assert_eq!(config.sample_rate, 44100);
    assert_eq!(config.bits_per_sample, 16);
    assert!(!config.enabled);
}

#[test]
fn test_float_to_pcm() {
    let samples = [0.0f32, 1.0, -1.0];
    let pcm = float_to_pcm(&samples, 1, 16);

    assert_eq!(pcm.len(), 6);

    let sample0 = i16::from_le_bytes([pcm[0], pcm[1]]);
    assert_eq!(sample0, 0);

    let sample1 = i16::from_le_bytes([pcm[2], pcm[3]]);
    assert_eq!(sample1, 32767);

    let sample2 = i16::from_le_bytes([pcm[4], pcm[5]]);
    assert!(sample2 <= -32767);
}

// =========================================================================
// AutofillManager Tests
// =========================================================================

#[test]
fn test_autofill_manager_configured_via_lib() {
    let mut manager = AutofillManager::new();
    assert!(!manager.is_configured());

    manager.set_rules(vec![AutofillRule {
        page_pattern: None,
        username_field: Some("#user".to_string()),
        password_field: None,
        totp_field: None,
        submit: None,
        cannot_submit: None,
    }]);
    manager.set_credentials(AutofillCredentials {
        username: Some("user".to_string()),
        password: None,
        totp_config: None,
    });

    assert!(manager.is_configured());
}
