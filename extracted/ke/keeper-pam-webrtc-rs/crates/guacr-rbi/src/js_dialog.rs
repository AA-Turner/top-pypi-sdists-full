// JavaScript Dialog Handling for RBI
//
// Handles JavaScript alerts, confirms, prompts, and beforeunload dialogs
// in the isolated browser session.
// Based on KCM's KCM-504-javascript-alerts branch.
//
// These dialogs would block the browser event loop if not handled,
// causing the session to become unresponsive.

use bytes::Bytes;
use log::{debug, info, warn};
use std::time::{Duration, Instant};

/// Maximum time to wait for user response to a dialog
pub const DIALOG_TIMEOUT_SECS: u64 = 60;

/// Maximum length of dialog message to display
pub const MAX_MESSAGE_LENGTH: usize = 2048;

/// Types of JavaScript dialogs
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum JsDialogType {
    /// window.alert() - informational, user acknowledges
    Alert,
    /// window.confirm() - yes/no question
    Confirm,
    /// window.prompt() - text input request
    Prompt,
    /// beforeunload event - leave page warning
    BeforeUnload,
}

impl JsDialogType {
    pub fn as_str(&self) -> &'static str {
        match self {
            JsDialogType::Alert => "alert",
            JsDialogType::Confirm => "confirm",
            JsDialogType::Prompt => "prompt",
            JsDialogType::BeforeUnload => "beforeunload",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "alert" => Some(JsDialogType::Alert),
            "confirm" => Some(JsDialogType::Confirm),
            "prompt" => Some(JsDialogType::Prompt),
            "beforeunload" | "onbeforeunload" => Some(JsDialogType::BeforeUnload),
            _ => None,
        }
    }
}

/// JavaScript dialog configuration
#[derive(Debug, Clone)]
pub struct JsDialogConfig {
    /// Whether to show dialogs to user (vs auto-dismiss)
    pub show_dialogs: bool,
    /// Auto-dismiss alerts after this duration
    pub auto_dismiss_alert_ms: Option<u64>,
    /// Auto-confirm (true/false) for confirm dialogs
    pub auto_confirm: Option<bool>,
    /// Auto-response for prompt dialogs
    pub auto_prompt_response: Option<String>,
    /// Allow beforeunload dialogs (can be abused by malicious sites)
    pub allow_beforeunload: bool,
    /// Maximum dialog timeout in seconds
    pub timeout_secs: u64,
}

impl Default for JsDialogConfig {
    fn default() -> Self {
        Self {
            show_dialogs: true,
            auto_dismiss_alert_ms: Some(5000), // Auto-dismiss alerts after 5s
            auto_confirm: None,                // Show confirm dialogs to user
            auto_prompt_response: None,        // Show prompt dialogs to user
            allow_beforeunload: false,         // Block beforeunload by default
            timeout_secs: DIALOG_TIMEOUT_SECS,
        }
    }
}

/// A JavaScript dialog request from the browser
#[derive(Debug, Clone)]
pub struct JsDialogRequest {
    /// Unique identifier for this dialog
    pub id: String,
    /// Type of dialog
    pub dialog_type: JsDialogType,
    /// Dialog message text
    pub message: String,
    /// Default value (for prompts)
    pub default_value: Option<String>,
    /// URL of page showing the dialog
    pub origin_url: String,
    /// When the dialog was shown
    pub shown_at: Instant,
}

impl JsDialogRequest {
    /// Check if dialog has timed out
    pub fn is_timed_out(&self, timeout_secs: u64) -> bool {
        self.shown_at.elapsed() > Duration::from_secs(timeout_secs)
    }

    /// Get truncated message for display
    pub fn display_message(&self) -> &str {
        if self.message.len() > MAX_MESSAGE_LENGTH {
            &self.message[..MAX_MESSAGE_LENGTH]
        } else {
            &self.message
        }
    }
}

/// Response to a JavaScript dialog
#[derive(Debug, Clone)]
pub struct JsDialogResponse {
    /// Dialog ID this response is for
    pub id: String,
    /// Whether user confirmed (OK) or cancelled
    pub confirmed: bool,
    /// User's text input (for prompts)
    pub input: Option<String>,
}

/// JavaScript dialog manager
pub struct JsDialogManager {
    config: JsDialogConfig,
    /// Currently pending dialog (only one at a time per browser)
    pending_dialog: Option<JsDialogRequest>,
    /// Counter for generating dialog IDs
    next_id: u64,
}

impl JsDialogManager {
    pub fn new(config: JsDialogConfig) -> Self {
        Self {
            config,
            pending_dialog: None,
            next_id: 1,
        }
    }

    /// Handle a new JavaScript dialog from the browser
    /// Returns the dialog to show to user, or None if auto-handled
    pub fn handle_dialog(
        &mut self,
        dialog_type: JsDialogType,
        message: String,
        default_value: Option<String>,
        origin_url: String,
    ) -> Option<(JsDialogRequest, Option<JsDialogResponse>)> {
        // beforeunload can be used maliciously, optionally block
        if dialog_type == JsDialogType::BeforeUnload && !self.config.allow_beforeunload {
            info!("RBI: Blocked beforeunload dialog from {}", origin_url);
            return Some((
                JsDialogRequest {
                    id: "blocked".to_string(),
                    dialog_type,
                    message,
                    default_value,
                    origin_url,
                    shown_at: Instant::now(),
                },
                Some(JsDialogResponse {
                    id: "blocked".to_string(),
                    confirmed: true, // Allow navigation
                    input: None,
                }),
            ));
        }

        // Check for auto-handling
        if !self.config.show_dialogs {
            return self.auto_handle(dialog_type, message, default_value, origin_url);
        }

        // Create dialog request
        let dialog = JsDialogRequest {
            id: format!("jsdialog-{}", self.next_id),
            dialog_type,
            message,
            default_value,
            origin_url,
            shown_at: Instant::now(),
        };
        self.next_id += 1;

        info!(
            "RBI: JavaScript {} dialog - id={}, origin={}",
            dialog.dialog_type.as_str(),
            dialog.id,
            dialog.origin_url
        );

        // Check for type-specific auto-handling
        let auto_response = match dialog_type {
            JsDialogType::Alert if self.config.auto_dismiss_alert_ms.is_some() => {
                // Will auto-dismiss after timeout
                None
            }
            JsDialogType::Confirm if self.config.auto_confirm.is_some() => Some(JsDialogResponse {
                id: dialog.id.clone(),
                confirmed: self.config.auto_confirm.unwrap(),
                input: None,
            }),
            JsDialogType::Prompt if self.config.auto_prompt_response.is_some() => {
                Some(JsDialogResponse {
                    id: dialog.id.clone(),
                    confirmed: true,
                    input: self.config.auto_prompt_response.clone(),
                })
            }
            _ => None,
        };

        self.pending_dialog = Some(dialog.clone());
        Some((dialog, auto_response))
    }

    /// Auto-handle dialog without user interaction
    fn auto_handle(
        &mut self,
        dialog_type: JsDialogType,
        message: String,
        default_value: Option<String>,
        origin_url: String,
    ) -> Option<(JsDialogRequest, Option<JsDialogResponse>)> {
        let id = format!("jsdialog-{}", self.next_id);
        self.next_id += 1;

        let dialog = JsDialogRequest {
            id: id.clone(),
            dialog_type,
            message,
            default_value: default_value.clone(),
            origin_url,
            shown_at: Instant::now(),
        };

        let response = match dialog_type {
            JsDialogType::Alert => {
                debug!("RBI: Auto-dismissing alert");
                JsDialogResponse {
                    id,
                    confirmed: true,
                    input: None,
                }
            }
            JsDialogType::Confirm => {
                let confirmed = self.config.auto_confirm.unwrap_or(false);
                debug!("RBI: Auto-responding to confirm: {}", confirmed);
                JsDialogResponse {
                    id,
                    confirmed,
                    input: None,
                }
            }
            JsDialogType::Prompt => {
                let input = self.config.auto_prompt_response.clone().or(default_value);
                debug!("RBI: Auto-responding to prompt");
                JsDialogResponse {
                    id,
                    confirmed: input.is_some(),
                    input,
                }
            }
            JsDialogType::BeforeUnload => {
                debug!("RBI: Auto-confirming beforeunload");
                JsDialogResponse {
                    id,
                    confirmed: true,
                    input: None,
                }
            }
        };

        Some((dialog, Some(response)))
    }

    /// Handle user response to a dialog
    pub fn handle_response(&mut self, response: JsDialogResponse) -> Result<(), String> {
        match &self.pending_dialog {
            Some(dialog) if dialog.id == response.id => {
                info!(
                    "RBI: Dialog response - id={}, confirmed={}",
                    response.id, response.confirmed
                );
                self.pending_dialog = None;
                Ok(())
            }
            Some(_) => Err("Response ID doesn't match pending dialog".to_string()),
            None => Err("No pending dialog".to_string()),
        }
    }

    /// Check for timed-out dialogs
    pub fn check_timeout(&mut self) -> Option<JsDialogResponse> {
        if let Some(ref dialog) = self.pending_dialog {
            // Auto-dismiss alerts after configured time
            if dialog.dialog_type == JsDialogType::Alert {
                if let Some(dismiss_ms) = self.config.auto_dismiss_alert_ms {
                    if dialog.shown_at.elapsed() > Duration::from_millis(dismiss_ms) {
                        let response = JsDialogResponse {
                            id: dialog.id.clone(),
                            confirmed: true,
                            input: None,
                        };
                        self.pending_dialog = None;
                        info!("RBI: Auto-dismissed alert after {}ms", dismiss_ms);
                        return Some(response);
                    }
                }
            }

            // General timeout
            if dialog.is_timed_out(self.config.timeout_secs) {
                let response = JsDialogResponse {
                    id: dialog.id.clone(),
                    confirmed: false,
                    input: None,
                };
                self.pending_dialog = None;
                warn!("RBI: Dialog timed out - id={}", response.id);
                return Some(response);
            }
        }
        None
    }

    /// Get currently pending dialog
    pub fn get_pending(&self) -> Option<&JsDialogRequest> {
        self.pending_dialog.as_ref()
    }

    /// Check if a dialog is pending
    pub fn has_pending(&self) -> bool {
        self.pending_dialog.is_some()
    }
}

/// Generate Guacamole instruction to show dialog to client
pub fn format_dialog_instruction(dialog: &JsDialogRequest) -> Bytes {
    // Use Guacamole's pipe instruction for JS dialog
    // The client-side JavaScript will render this as a dialog
    let dialog_json = serde_json::json!({
        "id": dialog.id,
        "type": dialog.dialog_type.as_str(),
        "message": dialog.display_message(),
        "defaultValue": dialog.default_value,
        "origin": dialog.origin_url,
    });

    let json_str = dialog_json.to_string();
    let instr = format!(
        "4.pipe,0.{},16.application/json,9.js-dialog,{}.{};",
        dialog.id.len(),
        json_str.len(),
        json_str
    );
    Bytes::from(instr)
}

/// JavaScript to inject for intercepting dialogs via CDP
pub const DIALOG_INTERCEPTOR_JS: &str = r#"
(function() {
    // Store original functions
    const originalAlert = window.alert;
    const originalConfirm = window.confirm;
    const originalPrompt = window.prompt;

    // Track intercepted calls for CDP event handler
    window.__guac_dialog_pending = null;

    // These will be handled by CDP Page.javascriptDialogOpening event
    // This script just ensures we can track dialog state

    console.log('Guacamole: Dialog interceptor installed');
})();
"#;
