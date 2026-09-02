// Security tests for RBI (Remote Browser Isolation) handler.
// Run with: cargo test -p guacr-rbi --test security_test -- --include-ignored
#[cfg(test)]
mod scheme_validation_tests {
    use guacr_rbi::validate_navigate_scheme;

    /// Non-http/https schemes must be rejected before reaching Chrome.
    ///
    /// javascript: can execute code in the Chrome context.
    /// data: can render attacker-controlled HTML/JS.
    /// file:// can read the local filesystem.
    /// about: and chrome:// access internal Chrome pages.
    #[test]
    #[ignore]
    fn navigate_rejects_javascript_scheme() {
        assert!(
            validate_navigate_scheme("javascript:alert(1)").is_err(),
            "javascript: scheme must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn navigate_rejects_data_scheme() {
        assert!(
            validate_navigate_scheme("data:text/html,<h1>x</h1>").is_err(),
            "data: scheme must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn navigate_rejects_file_scheme() {
        assert!(
            validate_navigate_scheme("file:///etc/passwd").is_err(),
            "file:// scheme must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn navigate_rejects_about_scheme() {
        assert!(
            validate_navigate_scheme("about:blank").is_err(),
            "about: scheme must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn navigate_rejects_chrome_scheme() {
        assert!(
            validate_navigate_scheme("chrome://settings").is_err(),
            "chrome:// scheme must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn navigate_allows_http_scheme() {
        assert!(
            validate_navigate_scheme("http://example.com/page").is_ok(),
            "http:// scheme must be allowed"
        );
    }

    #[test]
    #[ignore]
    fn navigate_allows_https_scheme() {
        assert!(
            validate_navigate_scheme("https://example.com/page?q=1").is_ok(),
            "https:// scheme must be allowed"
        );
    }
}

#[cfg(test)]
mod url_allowlist_bypass_tests {
    use guacr_handlers::RbiSecuritySettings;

    /// is_url_allowed() must use host-based matching, not substring matching.
    ///
    /// With substring matching, pattern "allowed.com" would match
    /// "https://evil.com?ref=allowed.com", bypassing the allowlist.
    #[test]
    #[ignore]
    fn allowlist_rejects_query_string_bypass() {
        let settings = RbiSecuritySettings {
            url_allowlist: vec!["allowed.com".to_string()],
            ..Default::default()
        };

        assert!(
            !settings.is_url_allowed("https://evil.com?ref=allowed.com"),
            "query string bypass must be rejected: evil.com?ref=allowed.com must not pass allowlist 'allowed.com'"
        );
    }

    #[test]
    #[ignore]
    fn allowlist_rejects_path_confusion_bypass() {
        let settings = RbiSecuritySettings {
            url_allowlist: vec!["allowed.com".to_string()],
            ..Default::default()
        };

        assert!(
            !settings.is_url_allowed("https://evil.com/allowed.com/steal"),
            "path confusion bypass must be rejected: evil.com/allowed.com must not pass allowlist 'allowed.com'"
        );
    }

    #[test]
    #[ignore]
    fn allowlist_allows_matching_host() {
        let settings = RbiSecuritySettings {
            url_allowlist: vec!["allowed.com".to_string()],
            ..Default::default()
        };

        assert!(
            settings.is_url_allowed("https://allowed.com/page"),
            "exact host must be allowed"
        );
    }

    #[test]
    #[ignore]
    fn allowlist_allows_subdomain_of_matching_host() {
        let settings = RbiSecuritySettings {
            url_allowlist: vec!["allowed.com".to_string()],
            ..Default::default()
        };

        assert!(
            settings.is_url_allowed("https://sub.allowed.com/page"),
            "subdomain of allowed host must be allowed"
        );
    }
}

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

#[cfg(test)]
mod ssrf_tests {
    use guacr_rbi::validate_download_url;

    /// Requests to the EC2 metadata endpoint must be blocked.
    ///
    /// 169.254.169.254 is the AWS instance metadata service. An attacker who
    /// can control the download URL in an RBI session could exfiltrate IAM
    /// credentials and other sensitive metadata.
    #[test]
    #[ignore]
    fn ssrf_blocks_ec2_metadata_endpoint() {
        let blocked = vec![
            "http://169.254.169.254/latest/meta-data/",
            "https://169.254.169.254/latest/user-data",
            "http://169.254.169.254/",
        ];
        for url in blocked {
            assert!(
                validate_download_url(url).is_err(),
                "EC2 metadata URL must be blocked: {}",
                url
            );
        }
    }

    /// Private IPv4 ranges must be blocked (RFC 1918).
    #[test]
    #[ignore]
    fn ssrf_blocks_private_ipv4_ranges() {
        let blocked = vec![
            "http://10.0.0.1/secret",
            "http://10.255.255.255/data",
            "http://172.16.0.1/internal",
            "http://172.31.255.255/config",
            "http://192.168.1.1/router",
            "http://192.168.0.254/admin",
        ];
        for url in blocked {
            assert!(
                validate_download_url(url).is_err(),
                "Private IPv4 URL must be blocked: {}",
                url
            );
        }
    }

    /// Loopback addresses must be blocked.
    #[test]
    #[ignore]
    fn ssrf_blocks_loopback_addresses() {
        let blocked = vec![
            "http://127.0.0.1/secret",
            "http://localhost/admin",
            "http://[::1]/internal",
        ];
        for url in blocked {
            assert!(
                validate_download_url(url).is_err(),
                "Loopback URL must be blocked: {}",
                url
            );
        }
    }

    /// ULA IPv6 ranges (fd00::/8) must be blocked.
    #[test]
    #[ignore]
    fn ssrf_blocks_ula_ipv6_range() {
        let blocked = vec!["http://[fd00::1]/internal", "http://[fc00::1]/private"];
        for url in blocked {
            assert!(
                validate_download_url(url).is_err(),
                "ULA IPv6 URL must be blocked: {}",
                url
            );
        }
    }

    /// Non-http/https schemes must be blocked.
    #[test]
    #[ignore]
    fn ssrf_blocks_non_http_schemes() {
        let blocked = vec![
            "ftp://example.com/file",
            "file:///etc/passwd",
            "data:text/plain,hello",
            "javascript:alert(1)",
        ];
        for url in blocked {
            assert!(
                validate_download_url(url).is_err(),
                "Non-http scheme must be blocked: {}",
                url
            );
        }
    }

    /// Valid public HTTPS URLs must be allowed.
    #[test]
    #[ignore]
    fn ssrf_allows_valid_public_urls() {
        let allowed = vec![
            "https://example.com/file.pdf",
            "https://cdn.example.com/download/file.zip",
            "http://public-server.example.org/data",
        ];
        for url in allowed {
            assert!(
                validate_download_url(url).is_ok(),
                "Valid public URL must be allowed: {}",
                url
            );
        }
    }
}

// ---------------------------------------------------------------------------
// CVE-2023-30575 audit: tabs.rs format_tabs_instruction uses .len() (bytes)
// instead of .chars().count() (codepoints) for page titles and URLs.
//
// Browser tab titles can contain Unicode (Japanese, Arabic, emoji, etc.).
// URLs can contain punycode or percent-encoded sequences. When the LENGTH
// field counts bytes instead of codepoints, the client receives garbled
// framing for any non-ASCII tab title.
// ---------------------------------------------------------------------------
#[cfg(test)]
mod guac_length_tabs_tests {
    use guacr_rbi::TabManager;

    // Helper: extract the length prefix from the nth comma-separated element
    // in a Guacamole instruction. Element 0 = opcode.
    fn element_len(instruction: &str, n: usize) -> usize {
        let body = instruction.trim_end_matches(';');
        let parts: Vec<&str> = body.splitn(n + 2, ',').collect();
        let element = parts[n];
        let dot = element.find('.').expect("no dot separator in element");
        element[..dot]
            .parse()
            .expect("length prefix is not integer")
    }

    /// format_tabs_instruction page title LENGTH must be codepoint count.
    ///
    /// A Japanese page title "日本語テスト" = 6 codepoints, 18 UTF-8 bytes.
    /// Correct wire: LENGTH = 6. Buggy wire: LENGTH = 18.
    ///
    /// This test fails before the fix and passes after.
    #[test]
    #[ignore]
    fn tabs_instruction_page_title_length_is_codepoints() {
        let mut manager = TabManager::new();
        let tab_id = manager
            .create_tab("https://example.com")
            .expect("tab created");

        // Set a Unicode title — Japanese test string: 6 codepoints, 18 bytes.
        let title = "日本語テスト";
        manager.update_tab_title(tab_id, title);

        let instr = manager.format_tabs_instruction();

        // The instruction format is:
        //   4.tabs,<count>,<id>,<title>,<url>,<active>,...;
        // Element indices: 0=opcode, 1=count, 2=id, 3=title, 4=url, 5=active
        let title_len = element_len(&instr, 3);

        assert_eq!(
            title_len,
            title.chars().count(),
            "tabs instruction title LENGTH must be {} codepoints, not {} bytes. \
             Instruction: {}",
            title.chars().count(),
            title.len(),
            instr
        );
    }

    /// format_tabs_instruction with an emoji page title (4-byte codepoints).
    ///
    /// U+1F525 (FIRE) = 1 codepoint, 4 UTF-8 bytes.
    /// Correct wire: LENGTH = 1. Buggy wire: LENGTH = 4.
    ///
    /// This test fails before the fix and passes after.
    #[test]
    #[ignore]
    fn tabs_instruction_emoji_title_length_is_codepoints() {
        let mut manager = TabManager::new();
        let tab_id = manager
            .create_tab("https://example.com")
            .expect("tab created");

        // U+1F525 FIRE: 1 codepoint, 4 UTF-8 bytes.
        let title = "\u{1F525}";
        assert_eq!(title.len(), 4, "emoji must be 4 UTF-8 bytes");
        assert_eq!(title.chars().count(), 1, "emoji must be 1 codepoint");
        manager.update_tab_title(tab_id, title);

        let instr = manager.format_tabs_instruction();

        let title_len = element_len(&instr, 3);

        assert_eq!(
            title_len,
            title.chars().count(),
            "emoji title LENGTH must be 1 (codepoints), not 4 (bytes). Instruction: {}",
            instr
        );
    }
}
