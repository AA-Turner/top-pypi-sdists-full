use crate::js_dialog::{
    format_dialog_instruction, JsDialogConfig, JsDialogManager, JsDialogRequest, JsDialogResponse,
    JsDialogType, DIALOG_TIMEOUT_SECS, MAX_MESSAGE_LENGTH,
};
use std::time::Instant;

#[test]
fn test_dialog_type_parsing() {
    assert_eq!(JsDialogType::parse("alert"), Some(JsDialogType::Alert));
    assert_eq!(JsDialogType::parse("CONFIRM"), Some(JsDialogType::Confirm));
    assert_eq!(JsDialogType::parse("prompt"), Some(JsDialogType::Prompt));
    assert_eq!(
        JsDialogType::parse("beforeunload"),
        Some(JsDialogType::BeforeUnload)
    );
    assert_eq!(
        JsDialogType::parse("onbeforeunload"),
        Some(JsDialogType::BeforeUnload)
    );
    assert_eq!(JsDialogType::parse("unknown"), None);
    assert_eq!(JsDialogType::parse(""), None);
}

#[test]
fn test_dialog_type_as_str() {
    assert_eq!(JsDialogType::Alert.as_str(), "alert");
    assert_eq!(JsDialogType::Confirm.as_str(), "confirm");
    assert_eq!(JsDialogType::Prompt.as_str(), "prompt");
    assert_eq!(JsDialogType::BeforeUnload.as_str(), "beforeunload");
}

#[test]
fn test_auto_dismiss_alert() {
    let config = JsDialogConfig {
        show_dialogs: false,
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::Alert,
        "Test alert".to_string(),
        None,
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (_, response) = result.unwrap();
    assert!(response.is_some());
    assert!(response.unwrap().confirmed);
}

#[test]
fn test_auto_confirm_dialog() {
    let config = JsDialogConfig {
        show_dialogs: false,
        auto_confirm: Some(true),
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::Confirm,
        "Delete all files?".to_string(),
        None,
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (_, response) = result.unwrap();
    assert!(response.is_some());
    assert!(response.unwrap().confirmed);
}

#[test]
fn test_auto_deny_confirm_dialog() {
    let config = JsDialogConfig {
        show_dialogs: false,
        auto_confirm: Some(false),
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::Confirm,
        "Delete all files?".to_string(),
        None,
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (_, response) = result.unwrap();
    assert!(response.is_some());
    assert!(!response.unwrap().confirmed);
}

#[test]
fn test_auto_prompt_response() {
    let config = JsDialogConfig {
        show_dialogs: false,
        auto_prompt_response: Some("auto-value".to_string()),
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::Prompt,
        "Enter your name:".to_string(),
        Some("default-name".to_string()),
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (_, response) = result.unwrap();
    assert!(response.is_some());
    let resp = response.unwrap();
    assert!(resp.confirmed);
    assert_eq!(resp.input.as_deref(), Some("auto-value"));
}

#[test]
fn test_prompt_with_default_value() {
    let config = JsDialogConfig {
        show_dialogs: false,
        auto_prompt_response: None,
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::Prompt,
        "Enter value:".to_string(),
        Some("default-123".to_string()),
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (_, response) = result.unwrap();
    assert!(response.is_some());
    let resp = response.unwrap();
    assert!(resp.confirmed);
    assert_eq!(resp.input.as_deref(), Some("default-123"));
}

#[test]
fn test_block_beforeunload() {
    let config = JsDialogConfig {
        allow_beforeunload: false,
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::BeforeUnload,
        "Are you sure?".to_string(),
        None,
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (_, response) = result.unwrap();
    assert!(response.is_some());
    assert!(response.unwrap().confirmed);
}

#[test]
fn test_allow_beforeunload() {
    let config = JsDialogConfig {
        allow_beforeunload: true,
        show_dialogs: true,
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::BeforeUnload,
        "Are you sure?".to_string(),
        None,
        "https://example.com".to_string(),
    );

    assert!(result.is_some());
    let (dialog, response) = result.unwrap();
    assert!(response.is_none());
    assert!(manager.has_pending());
    assert_eq!(dialog.dialog_type, JsDialogType::BeforeUnload);
}

#[test]
fn test_message_truncation() {
    let long_message = "x".repeat(MAX_MESSAGE_LENGTH + 100);
    let dialog = JsDialogRequest {
        id: "test".to_string(),
        dialog_type: JsDialogType::Alert,
        message: long_message.clone(),
        default_value: None,
        origin_url: "https://example.com".to_string(),
        shown_at: Instant::now(),
    };

    assert_eq!(dialog.display_message().len(), MAX_MESSAGE_LENGTH);
    assert_eq!(dialog.message.len(), MAX_MESSAGE_LENGTH + 100);
}

#[test]
fn test_short_message_not_truncated() {
    let message = "Short message";
    let dialog = JsDialogRequest {
        id: "test".to_string(),
        dialog_type: JsDialogType::Alert,
        message: message.to_string(),
        default_value: None,
        origin_url: "https://example.com".to_string(),
        shown_at: Instant::now(),
    };

    assert_eq!(dialog.display_message(), message);
}

#[test]
fn test_dialog_response_handling() {
    let config = JsDialogConfig {
        show_dialogs: true,
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    let result = manager.handle_dialog(
        JsDialogType::Confirm,
        "Proceed?".to_string(),
        None,
        "https://example.com".to_string(),
    );

    let (dialog, _) = result.unwrap();
    assert!(manager.has_pending());

    let response = JsDialogResponse {
        id: dialog.id.clone(),
        confirmed: true,
        input: None,
    };

    assert!(manager.handle_response(response).is_ok());
    assert!(!manager.has_pending());
}

#[test]
fn test_wrong_response_id() {
    let config = JsDialogConfig {
        show_dialogs: true,
        ..Default::default()
    };
    let mut manager = JsDialogManager::new(config);

    manager.handle_dialog(
        JsDialogType::Alert,
        "Test".to_string(),
        None,
        "https://example.com".to_string(),
    );

    let response = JsDialogResponse {
        id: "wrong-id".to_string(),
        confirmed: true,
        input: None,
    };

    assert!(manager.handle_response(response).is_err());
}

#[test]
fn test_no_pending_dialog() {
    let config = JsDialogConfig::default();
    let mut manager = JsDialogManager::new(config);

    assert!(!manager.has_pending());
    assert!(manager.get_pending().is_none());

    let response = JsDialogResponse {
        id: "any".to_string(),
        confirmed: true,
        input: None,
    };

    assert!(manager.handle_response(response).is_err());
}

#[test]
fn test_format_dialog_instruction() {
    let dialog = JsDialogRequest {
        id: "dialog-1".to_string(),
        dialog_type: JsDialogType::Confirm,
        message: "Are you sure?".to_string(),
        default_value: None,
        origin_url: "https://example.com".to_string(),
        shown_at: Instant::now(),
    };

    let instr = format_dialog_instruction(&dialog);
    let instr_str = String::from_utf8_lossy(&instr);

    assert!(instr_str.contains("pipe"));
    assert!(instr_str.contains("js-dialog"));
    assert!(instr_str.contains("confirm"));
    assert!(instr_str.contains("Are you sure?"));
}

#[test]
fn test_dialog_config_defaults() {
    let config = JsDialogConfig::default();

    assert!(config.show_dialogs);
    assert_eq!(config.auto_dismiss_alert_ms, Some(5000));
    assert!(config.auto_confirm.is_none());
    assert!(config.auto_prompt_response.is_none());
    assert!(!config.allow_beforeunload);
    assert_eq!(config.timeout_secs, DIALOG_TIMEOUT_SECS);
}

#[test]
fn test_dialog_timeout_check() {
    let dialog = JsDialogRequest {
        id: "test".to_string(),
        dialog_type: JsDialogType::Alert,
        message: "Test".to_string(),
        default_value: None,
        origin_url: "https://example.com".to_string(),
        shown_at: Instant::now(),
    };

    assert!(!dialog.is_timed_out(60));
    assert!(dialog.is_timed_out(0));
}
