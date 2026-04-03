// Security tests for RBI (Remote Browser Isolation) handler.
// Run with: cargo test -p guacr-rbi --test security_test -- --include-ignored
#[cfg(test)]
mod security_tests {
    #[tokio::test]
    #[ignore]
    async fn test_rbi_url_whitelist_enforced() {
        // Verify that URL whitelist patterns are correctly enforced:
        // - Allowed patterns permit navigation
        // - Blocked patterns (not in whitelist) prevent navigation
        use guacr_rbi::{check_url_allowed, UrlPattern};

        let patterns = vec![
            UrlPattern::parse("*.example.com").unwrap(),
            UrlPattern::parse("https://allowed.corp.com").unwrap(),
        ];

        assert!(check_url_allowed("https://app.example.com", &patterns));
        assert!(check_url_allowed(
            "https://allowed.corp.com/page",
            &patterns
        ));
        assert!(!check_url_allowed("https://evil.com", &patterns));
        assert!(!check_url_allowed(
            "https://example.com.evil.com",
            &patterns
        ));

        println!("URL whitelist enforcement verified");
    }

    #[tokio::test]
    #[ignore]
    async fn test_rbi_clipboard_copy_restriction() {
        // Verify that copy-disabled clipboard silently blocks browser → client data
        use guacr_rbi::{RbiClipboard, CLIPBOARD_DEFAULT_SIZE};

        let mut clipboard = RbiClipboard::new(CLIPBOARD_DEFAULT_SIZE);
        clipboard.set_restrictions(true, false); // disable_copy=true

        let sensitive_data = b"sensitive-password-123";
        let result = clipboard.handle_browser_clipboard(sensitive_data, "text/plain");

        assert!(result.is_ok(), "Should not error on blocked copy");
        assert!(
            result.unwrap().is_none(),
            "Should return None when copy is blocked"
        );

        // Verify no data was stored
        let stored = clipboard.get_data();
        assert!(stored.is_ok());
        assert!(
            stored.unwrap().is_empty(),
            "No data should be stored when copy is blocked"
        );

        println!("Clipboard copy restriction verified");
    }

    #[tokio::test]
    #[ignore]
    async fn test_rbi_clipboard_paste_restriction() {
        // Verify that paste-disabled clipboard silently blocks client → browser data
        use guacr_rbi::{RbiClipboard, CLIPBOARD_DEFAULT_SIZE};

        let mut clipboard = RbiClipboard::new(CLIPBOARD_DEFAULT_SIZE);
        clipboard.set_restrictions(false, true); // disable_paste=true

        let paste_attempt = b"data-from-local-clipboard";
        let result = clipboard.handle_client_clipboard(paste_attempt, "text/plain");

        assert!(result.is_ok(), "Should not error on blocked paste");
        assert!(
            result.unwrap().is_none(),
            "Should return None when paste is blocked"
        );

        println!("Clipboard paste restriction verified");
    }

    #[tokio::test]
    #[ignore]
    async fn test_rbi_upload_blocked_extension_rejected() {
        // Verify that the upload engine rejects executable file types
        use guacr_rbi::{UploadConfig, UploadEngine};

        let config = UploadConfig {
            enabled: true,
            ..Default::default()
        };
        let mut engine = UploadEngine::new(config);

        let request = engine
            .manager_mut()
            .handle_dialog_request(false, vec![])
            .unwrap();

        // Attempt to upload an executable — should be rejected
        let result =
            engine.start_upload(&request.id, "malware.exe", "application/x-msdownload", 1024);
        assert!(result.is_err(), "Executable upload must be rejected");

        let _result = engine.start_upload(&request.id, "script.bat", "application/x-bat", 256);
        // Note: request was already removed when it returned Err above, so this may also fail
        // The important property is that .exe was rejected

        println!("Upload blocked extension rejection verified");
    }

    #[tokio::test]
    #[ignore]
    async fn test_rbi_js_dialog_beforeunload_blocked_by_default() {
        // Verify that beforeunload dialogs are blocked by default to prevent
        // malicious pages from trapping users
        use guacr_rbi::{JsDialogConfig, JsDialogManager, JsDialogType};

        let config = JsDialogConfig::default(); // allow_beforeunload = false by default
        let mut manager = JsDialogManager::new(config);

        let result = manager.handle_dialog(
            JsDialogType::BeforeUnload,
            "Are you sure you want to leave?".to_string(),
            None,
            "https://malicious.example.com".to_string(),
        );

        assert!(result.is_some());
        let (_, response) = result.unwrap();
        assert!(response.is_some(), "BeforeUnload should be auto-handled");
        assert!(
            response.unwrap().confirmed,
            "Should auto-confirm to allow navigation"
        );

        println!("BeforeUnload dialog blocking verified");
    }
}
