use crate::security::{
    check_sql_query_allowed, classify_sql_query, is_keyboard_event_allowed_readonly,
    is_mouse_event_allowed_readonly, is_mysql_export_query, is_mysql_import_query,
    is_postgres_copy_in, is_postgres_copy_out, DatabaseSecuritySettings, HandlerSecuritySettings,
    QueryType, RbiSecuritySettings, ReadOnlyBehavior, SftpOperation, SftpSecuritySettings,
    CLIPBOARD_DEFAULT_SIZE, CLIPBOARD_MAX_SIZE, CLIPBOARD_MIN_SIZE,
};
use std::collections::HashMap;

#[test]
fn test_default_settings() {
    let settings = HandlerSecuritySettings::default();
    assert!(!settings.read_only);
    assert!(!settings.disable_copy);
    assert!(!settings.disable_paste);
    assert_eq!(settings.clipboard_buffer_size, CLIPBOARD_DEFAULT_SIZE);
    assert_eq!(
        settings.connection_timeout_secs,
        crate::DEFAULT_CONNECTION_TIMEOUT_SECS
    );
}

#[test]
fn test_from_params() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("disable-copy".to_string(), "1".to_string());
    params.insert("clipboard-buffer-size".to_string(), "2097152".to_string()); // 2MB

    let settings = HandlerSecuritySettings::from_params(&params);

    assert!(settings.read_only);
    assert!(settings.disable_copy);
    assert!(!settings.disable_paste);
    assert_eq!(settings.clipboard_buffer_size, 2097152);
}

#[test]
fn test_clipboard_size_clamping() {
    let mut params = HashMap::new();

    // Too small - should clamp to minimum
    params.insert("clipboard-buffer-size".to_string(), "100".to_string());
    let settings = HandlerSecuritySettings::from_params(&params);
    assert_eq!(settings.clipboard_buffer_size, CLIPBOARD_MIN_SIZE);

    // Too large - should clamp to maximum
    params.insert(
        "clipboard-buffer-size".to_string(),
        "100000000000".to_string(),
    );
    let settings = HandlerSecuritySettings::from_params(&params);
    assert_eq!(settings.clipboard_buffer_size, CLIPBOARD_MAX_SIZE);
}

#[test]
fn test_wol_settings() {
    let mut params = HashMap::new();
    params.insert("wol-send-packet".to_string(), "true".to_string());
    params.insert("wol-mac-addr".to_string(), "AA:BB:CC:DD:EE:FF".to_string());
    params.insert("wol-udp-port".to_string(), "7".to_string());
    params.insert("wol-wait-time".to_string(), "30".to_string());

    let settings = HandlerSecuritySettings::from_params(&params);

    assert!(settings.wol_send_packet);
    assert_eq!(settings.wol_mac_addr, Some("AA:BB:CC:DD:EE:FF".to_string()));
    assert_eq!(settings.wol_udp_port, 7);
    assert_eq!(settings.wol_wait_time, 30);
}

#[test]
fn test_permission_checks() {
    let mut settings = HandlerSecuritySettings::default();

    assert!(settings.is_copy_allowed());
    assert!(settings.is_paste_allowed());
    assert!(settings.is_keyboard_allowed());
    assert!(settings.is_mouse_click_allowed());

    settings.read_only = true;
    assert!(settings.is_copy_allowed()); // Copy still allowed in read-only
    assert!(!settings.is_paste_allowed()); // Paste blocked
    assert!(!settings.is_keyboard_allowed());
    assert!(!settings.is_mouse_click_allowed());

    settings.read_only = false;
    settings.disable_copy = true;
    assert!(!settings.is_copy_allowed());
    assert!(settings.is_paste_allowed());
}

#[test]
fn test_readonly_keyboard_allowed() {
    // Ctrl+C should be allowed
    assert!(is_keyboard_event_allowed_readonly(0x63, true)); // 'c' with Ctrl
    assert!(is_keyboard_event_allowed_readonly(0x43, true)); // 'C' with Ctrl
    assert!(is_keyboard_event_allowed_readonly(0x03, false)); // Raw Ctrl+C

    // Regular keys should be blocked
    assert!(!is_keyboard_event_allowed_readonly(0x61, false)); // 'a'
    assert!(!is_keyboard_event_allowed_readonly(0xFF0D, false)); // Enter
}

#[test]
fn test_readonly_mouse_allowed() {
    // Movement allowed
    assert!(is_mouse_event_allowed_readonly(0x00));

    // Scroll allowed
    assert!(is_mouse_event_allowed_readonly(0x08)); // Scroll up
    assert!(is_mouse_event_allowed_readonly(0x10)); // Scroll down

    // Clicks blocked
    assert!(!is_mouse_event_allowed_readonly(0x01)); // Left click
    assert!(!is_mouse_event_allowed_readonly(0x02)); // Middle click
    assert!(!is_mouse_event_allowed_readonly(0x04)); // Right click
}

#[test]
fn test_protocol_behavior() {
    assert_eq!(
        ReadOnlyBehavior::for_protocol("ssh"),
        ReadOnlyBehavior::TerminalReadOnly
    );
    assert_eq!(
        ReadOnlyBehavior::for_protocol("rdp"),
        ReadOnlyBehavior::GraphicalReadOnly
    );
    assert_eq!(
        ReadOnlyBehavior::for_protocol("mysql"),
        ReadOnlyBehavior::DatabaseReadOnly
    );
    assert_eq!(
        ReadOnlyBehavior::for_protocol("sftp"),
        ReadOnlyBehavior::SftpReadOnly
    );
    assert_eq!(
        ReadOnlyBehavior::for_protocol("rbi"),
        ReadOnlyBehavior::BrowserReadOnly
    );
}

// Database Security Tests

#[test]
fn test_database_security_settings() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("disable-csv-export".to_string(), "true".to_string());

    let settings = DatabaseSecuritySettings::from_params(&params);

    assert!(settings.base.read_only);
    assert!(settings.disable_csv_export);
    assert!(!settings.disable_csv_import);
    assert!(!settings.is_csv_export_allowed());
    assert!(!settings.is_csv_import_allowed()); // read_only blocks import
}

#[test]
fn test_classify_sql_query() {
    assert_eq!(
        classify_sql_query("SELECT * FROM users"),
        QueryType::ReadOnly
    );
    assert_eq!(classify_sql_query("SHOW DATABASES"), QueryType::ReadOnly);
    assert_eq!(
        classify_sql_query("INSERT INTO users VALUES (1)"),
        QueryType::Modifying
    );
    assert_eq!(classify_sql_query("DROP TABLE users"), QueryType::Modifying);
    assert_eq!(classify_sql_query("BEGIN"), QueryType::Modifying);
}

#[test]
fn test_check_sql_query_allowed() {
    let settings = DatabaseSecuritySettings {
        base: HandlerSecuritySettings {
            read_only: true,
            ..Default::default()
        },
        ..Default::default()
    };

    assert!(check_sql_query_allowed("SELECT * FROM users", &settings).is_ok());
    assert!(check_sql_query_allowed("INSERT INTO users VALUES (1)", &settings).is_err());
}

#[test]
fn test_mysql_import_export_detection() {
    assert!(is_mysql_export_query(
        "SELECT * INTO OUTFILE '/tmp/x.csv' FROM users"
    ));
    assert!(!is_mysql_export_query("SELECT * FROM users"));
    assert!(is_mysql_import_query(
        "LOAD DATA INFILE '/tmp/x.csv' INTO TABLE users"
    ));
    assert!(!is_mysql_import_query("SELECT * FROM users"));
}

#[test]
fn test_postgres_copy_detection() {
    assert!(is_postgres_copy_out("COPY users TO STDOUT"));
    assert!(is_postgres_copy_in("COPY users FROM STDIN"));
    assert!(!is_postgres_copy_out("SELECT * FROM users"));
}

// SFTP Security Tests

#[test]
fn test_sftp_security_settings() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("sftp-root-directory".to_string(), "/home/user".to_string());

    let settings = SftpSecuritySettings::from_params(&params);

    assert!(settings.base.read_only);
    assert_eq!(settings.root_directory, Some("/home/user".to_string()));
    assert!(!settings.is_upload_allowed());
    assert!(settings.is_download_allowed());
}

#[test]
fn test_sftp_operation_allowed() {
    let settings = SftpSecuritySettings {
        base: HandlerSecuritySettings {
            read_only: true,
            ..Default::default()
        },
        ..Default::default()
    };

    assert!(settings.is_file_operation_allowed(SftpOperation::Read));
    assert!(settings.is_file_operation_allowed(SftpOperation::List));
    assert!(settings.is_file_operation_allowed(SftpOperation::Download));
    assert!(!settings.is_file_operation_allowed(SftpOperation::Upload));
    assert!(!settings.is_file_operation_allowed(SftpOperation::Delete));
    assert!(!settings.is_file_operation_allowed(SftpOperation::Mkdir));
}

// The guacd handshake keys the params map by the names advertised in
// guacr-guacd/src/args.rs — server.rs zips those names onto the client's connect
// values. The SFTP list advertises `root-directory`, `disable-download` and
// `disable-upload` unprefixed, so a client filling those slots must be honored and
// not just the `sftp-` spellings the gateway happens to send. The prefixed form
// still wins when both are present.

#[test]
fn test_sftp_accepts_advertised_root_directory() {
    let mut params = HashMap::new();
    params.insert("root-directory".to_string(), "/srv/files".to_string());

    let settings = SftpSecuritySettings::from_params(&params);

    assert_eq!(settings.root_directory, Some("/srv/files".to_string()));
}

#[test]
fn test_sftp_prefixed_root_directory_wins() {
    let mut params = HashMap::new();
    params.insert("root-directory".to_string(), "/srv/files".to_string());
    params.insert("sftp-root-directory".to_string(), "/home/user".to_string());

    let settings = SftpSecuritySettings::from_params(&params);

    assert_eq!(settings.root_directory, Some("/home/user".to_string()));
}

#[test]
fn test_sftp_accepts_advertised_disable_download() {
    let mut params = HashMap::new();
    params.insert("disable-download".to_string(), "true".to_string());

    let settings = SftpSecuritySettings::from_params(&params);

    assert!(!settings.is_download_allowed());
}

#[test]
fn test_sftp_accepts_advertised_disable_upload() {
    let mut params = HashMap::new();
    params.insert("disable-upload".to_string(), "true".to_string());

    let settings = SftpSecuritySettings::from_params(&params);

    assert!(!settings.is_upload_allowed());
}

// RBI Security Tests

#[test]
fn test_rbi_accepts_advertised_url_allowlist() {
    let mut params = HashMap::new();
    params.insert("url-allowlist".to_string(), "internal.corp".to_string());

    let settings = RbiSecuritySettings::from_params(&params);

    assert_eq!(settings.url_allowlist, vec!["internal.corp".to_string()]);
}

#[test]
fn test_rbi_accepts_advertised_url_blocklist() {
    let mut params = HashMap::new();
    params.insert(
        "url-blocklist".to_string(),
        "facebook.com, twitter.com".to_string(),
    );

    let settings = RbiSecuritySettings::from_params(&params);

    assert_eq!(settings.url_blocklist.len(), 2);
    assert!(!settings.is_url_allowed("https://facebook.com/page"));
}

#[test]
fn test_rbi_accepts_advertised_disable_print() {
    let mut params = HashMap::new();
    params.insert("disable-print".to_string(), "true".to_string());

    let settings = RbiSecuritySettings::from_params(&params);

    assert!(settings.disable_print);
}

#[test]
fn test_rbi_accepts_advertised_disable_download() {
    let mut params = HashMap::new();
    params.insert("disable-download".to_string(), "true".to_string());

    let settings = RbiSecuritySettings::from_params(&params);

    assert!(!settings.is_download_allowed());
}

#[test]
fn test_rbi_accepts_advertised_disable_upload() {
    let mut params = HashMap::new();
    params.insert("disable-upload".to_string(), "true".to_string());

    let settings = RbiSecuritySettings::from_params(&params);

    assert!(!settings.is_upload_allowed());
}

#[test]
fn test_rbi_prefixed_url_blocklist_wins() {
    let mut params = HashMap::new();
    params.insert("url-blocklist".to_string(), "facebook.com".to_string());
    params.insert(
        "rbi-url-blocklist".to_string(),
        "twitter.com, reddit.com".to_string(),
    );

    let settings = RbiSecuritySettings::from_params(&params);

    assert_eq!(settings.url_blocklist.len(), 2);
    assert!(settings.is_url_allowed("https://facebook.com/page"));
}

#[test]
fn test_rbi_security_settings() {
    let mut params = HashMap::new();
    params.insert("rbi-disable-download".to_string(), "true".to_string());
    params.insert(
        "rbi-url-blocklist".to_string(),
        "facebook.com, twitter.com".to_string(),
    );

    let settings = RbiSecuritySettings::from_params(&params);

    assert!(!settings.is_download_allowed());
    assert!(settings.is_upload_allowed());
    assert_eq!(settings.url_blocklist.len(), 2);
}

#[test]
fn test_rbi_url_filtering() {
    let settings = RbiSecuritySettings {
        url_blocklist: vec!["facebook.com".to_string(), "twitter.com".to_string()],
        ..Default::default()
    };

    assert!(!settings.is_url_allowed("https://facebook.com/page"));
    assert!(!settings.is_url_allowed("https://twitter.com/user"));
    assert!(settings.is_url_allowed("https://google.com"));

    let settings_allowlist = RbiSecuritySettings {
        url_allowlist: vec!["internal.corp".to_string()],
        ..Default::default()
    };

    assert!(settings_allowlist.is_url_allowed("https://internal.corp/app"));
    assert!(!settings_allowlist.is_url_allowed("https://google.com"));
}

// SQL classifier bypass tests — these prove the bugs that DangerousStatementDetector fixes.
// They should FAIL with the naïve first-token classifier and PASS after the fix.

#[test]
fn test_plsql_begin_block_with_delete_is_blocked_in_read_only() {
    // Bug: current classifier returns ReadOnly for "BEGIN" regardless of body.
    // A PL/SQL block that wraps a DELETE must be blocked.
    let settings = DatabaseSecuritySettings {
        base: HandlerSecuritySettings {
            read_only: true,
            ..Default::default()
        },
        ..Default::default()
    };
    assert!(
        check_sql_query_allowed("BEGIN DELETE FROM users; END;", &settings).is_err(),
        "PL/SQL BEGIN block with DELETE must be blocked in read-only mode"
    );
}

#[test]
fn test_plsql_begin_block_with_update_is_blocked_in_read_only() {
    let settings = DatabaseSecuritySettings {
        base: HandlerSecuritySettings {
            read_only: true,
            ..Default::default()
        },
        ..Default::default()
    };
    assert!(
        check_sql_query_allowed("BEGIN UPDATE t SET x=1 WHERE id=1; END;", &settings).is_err(),
        "PL/SQL BEGIN block with UPDATE must be blocked in read-only mode"
    );
}

#[test]
fn test_cte_wrapping_delete_is_blocked_in_read_only() {
    // CTE with a DELETE body must not pass as read-only even though the outer
    // statement starts with WITH … SELECT.
    let settings = DatabaseSecuritySettings {
        base: HandlerSecuritySettings {
            read_only: true,
            ..Default::default()
        },
        ..Default::default()
    };
    assert!(
        check_sql_query_allowed(
            "WITH d AS (DELETE FROM users RETURNING *) SELECT * FROM d",
            &settings,
        )
        .is_err(),
        "CTE wrapping DELETE must be blocked in read-only mode"
    );
}

#[test]
fn test_comment_split_insert_is_not_read_only() {
    // IN/**/SERT splits across a block comment — after stripping, it becomes
    // INSERT and must not be classified as read-only.
    assert!(
        !crate::security::DangerousStatementDetector::is_read_only("IN/**/SERT INTO t VALUES (1)"),
        "comment-split INSERT must not be read-only"
    );
}

#[test]
fn test_begin_standalone_not_read_only() {
    // Bare BEGIN could start a PL/SQL block — under the strict allowlist it is
    // not provably read-only.
    assert!(
        !crate::security::DangerousStatementDetector::is_read_only("BEGIN"),
        "bare BEGIN must not be read-only (it may introduce a write block)"
    );
}

// allow-supply-user tests

/// Default must be false — deny unless explicitly allowed.
#[test]
fn test_allow_supply_user_default_is_false() {
    let settings = HandlerSecuritySettings::default();
    assert!(
        !settings.allow_supply_user,
        "allow_supply_user must default to false (secure default)"
    );
}

/// allow-supply-user=true enables credential supply.
#[test]
fn test_allow_supply_user_true_from_params() {
    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "true".to_string());
    let settings = HandlerSecuritySettings::from_params(&params);
    assert!(
        settings.allow_supply_user,
        "allow-supply-user=true must set allow_supply_user"
    );
    assert!(
        settings.is_credential_supply_allowed(),
        "is_credential_supply_allowed must return true when allow_supply_user is set"
    );
}

/// allow-supply-user=false keeps the gate closed.
#[test]
fn test_allow_supply_user_false_from_params() {
    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "false".to_string());
    let settings = HandlerSecuritySettings::from_params(&params);
    assert!(!settings.allow_supply_user);
    assert!(
        !settings.is_credential_supply_allowed(),
        "is_credential_supply_allowed must return false when allow_supply_user is false"
    );
}

/// Missing param → gate closed (secure default).
#[test]
fn test_allow_supply_user_absent_means_denied() {
    let params = HashMap::new();
    let settings = HandlerSecuritySettings::from_params(&params);
    assert!(
        !settings.is_credential_supply_allowed(),
        "absent allow-supply-user must deny credential supply"
    );
}

/// "1" is accepted as truthy (same pattern as other bool params).
#[test]
fn test_allow_supply_user_numeric_one() {
    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "1".to_string());
    let settings = HandlerSecuritySettings::from_params(&params);
    assert!(settings.allow_supply_user);
}

/// check_credential_supply_allowed returns Ok when flag is set.
#[test]
fn test_check_credential_supply_allowed_ok() {
    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "true".to_string());
    let settings = HandlerSecuritySettings::from_params(&params);
    assert!(
        crate::security::check_credential_supply_allowed(&settings).is_ok(),
        "check_credential_supply_allowed must return Ok when allowed"
    );
}

/// check_credential_supply_allowed returns Err with a descriptive message when flag is absent.
#[test]
fn test_check_credential_supply_allowed_blocked() {
    let settings = HandlerSecuritySettings::default();
    let result = crate::security::check_credential_supply_allowed(&settings);
    assert!(
        result.is_err(),
        "must return Err when allow_supply_user is false"
    );
    let msg = result.unwrap_err();
    assert!(
        msg.contains("not permitted"),
        "error message must say 'not permitted', got: {msg}"
    );
}

// Comprehensive Integration-Style Security Tests

#[test]
fn test_all_sql_query_types_classified() {
    // Read-only queries
    let readonly_queries = [
        "SELECT * FROM users",
        "select id from t",
        "SHOW DATABASES",
        "SHOW TABLES",
        "DESCRIBE users",
        "DESC users",
        "EXPLAIN SELECT 1",
        "USE database_name",
        // PostgreSQL meta-commands
        "\\d",
        "\\dt",
        "\\l",
        "\\c",
        "\\?",
        "\\h",
    ];

    for query in readonly_queries {
        assert_eq!(
            classify_sql_query(query),
            QueryType::ReadOnly,
            "Query '{}' should be classified as ReadOnly",
            query
        );
    }

    // Modifying queries
    let modifying_queries = [
        "INSERT INTO users VALUES (1)",
        "UPDATE users SET name='x'",
        "DELETE FROM users",
        "DROP TABLE users",
        "DROP DATABASE test",
        "ALTER TABLE users ADD col INT",
        "CREATE TABLE new_table (id INT)",
        "CREATE DATABASE test",
        "TRUNCATE TABLE users",
        "REPLACE INTO users VALUES (1)",
        "GRANT SELECT ON users TO 'user'",
        "REVOKE SELECT ON users FROM 'user'",
        "RENAME TABLE old TO new",
        "LOAD DATA INFILE '/tmp/x.csv' INTO TABLE users",
        "CALL stored_proc()",
        "EXEC stored_proc",
        "EXECUTE stored_proc",
        "MERGE INTO users USING source",
        "UPSERT INTO users VALUES (1)",
        // Transaction control — not on the read-only allowlist (BEGIN could be PL/SQL)
        "BEGIN",
        "START TRANSACTION",
        "COMMIT",
        "ROLLBACK",
        "SAVEPOINT test",
        "RELEASE SAVEPOINT test",
        "HELP",
        // Admin commands
        "SET GLOBAL var = 1",
        "RESET QUERY CACHE",
        "KILL 123",
        "FLUSH TABLES",
        "OPTIMIZE TABLE users",
        "ANALYZE TABLE users",
        "REPAIR TABLE users",
        "VACUUM",
        "REINDEX TABLE users",
        "CLUSTER users",
    ];

    for query in modifying_queries {
        assert_eq!(
            classify_sql_query(query),
            QueryType::Modifying,
            "Query '{}' should be classified as Modifying",
            query
        );
    }
}

#[test]
fn test_security_settings_full_workflow() {
    // Simulate a connection with all security parameters
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("disable-copy".to_string(), "true".to_string());
    params.insert("disable-paste".to_string(), "true".to_string());
    params.insert("clipboard-buffer-size".to_string(), "512000".to_string()); // 500KB
    params.insert("connection-timeout".to_string(), "60".to_string());
    params.insert("idle-timeout".to_string(), "300".to_string());
    params.insert("wol-send-packet".to_string(), "true".to_string());
    params.insert("wol-mac-addr".to_string(), "00:11:22:33:44:55".to_string());

    let settings = HandlerSecuritySettings::from_params(&params);

    // Verify all settings were parsed
    assert!(settings.read_only);
    assert!(settings.disable_copy);
    assert!(settings.disable_paste);
    assert_eq!(settings.clipboard_buffer_size, 512000);
    assert_eq!(settings.connection_timeout_secs, 60);
    assert_eq!(settings.idle_timeout_secs, 300);
    assert!(settings.wol_send_packet);
    assert_eq!(settings.wol_mac_addr, Some("00:11:22:33:44:55".to_string()));

    // Verify permission checks
    assert!(!settings.is_copy_allowed());
    assert!(!settings.is_paste_allowed());
    assert!(!settings.is_keyboard_allowed());
    assert!(!settings.is_mouse_click_allowed());
}

#[test]
fn test_database_security_full_workflow() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("disable-copy".to_string(), "true".to_string());
    params.insert("disable-csv-export".to_string(), "true".to_string());
    params.insert("disable-csv-import".to_string(), "true".to_string());
    params.insert("clipboard-buffer-size".to_string(), "2097152".to_string()); // 2MB

    let settings = DatabaseSecuritySettings::from_params(&params);

    // Base settings inherited
    assert!(settings.base.read_only);
    assert!(settings.base.disable_copy);
    assert_eq!(settings.base.clipboard_buffer_size, 2097152);

    // Database-specific settings
    assert!(settings.disable_csv_export);
    assert!(settings.disable_csv_import);
    assert!(!settings.is_csv_export_allowed());
    assert!(!settings.is_csv_import_allowed());

    // Test query blocking
    assert!(check_sql_query_allowed("SELECT * FROM users", &settings).is_ok());
    assert!(check_sql_query_allowed("INSERT INTO users VALUES (1)", &settings).is_err());
    assert!(check_sql_query_allowed("DROP TABLE users", &settings).is_err());

    // Test MySQL import/export detection
    assert!(is_mysql_export_query(
        "SELECT * INTO OUTFILE '/tmp/x.csv' FROM users"
    ));
    assert!(is_mysql_import_query(
        "LOAD DATA INFILE '/tmp/x.csv' INTO TABLE users"
    ));
}

#[test]
fn test_sftp_security_full_workflow() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert(
        "sftp-root-directory".to_string(),
        "/home/restricted".to_string(),
    );
    params.insert("sftp-disable-download".to_string(), "true".to_string());
    params.insert("sftp-max-upload-size".to_string(), "10485760".to_string()); // 10MB

    let settings = SftpSecuritySettings::from_params(&params);

    // Verify settings
    assert!(settings.base.read_only);
    assert_eq!(
        settings.root_directory,
        Some("/home/restricted".to_string())
    );
    assert!(settings.disable_download);
    assert_eq!(settings.max_upload_size, 10485760);

    // Verify operation permissions
    assert!(settings.is_file_operation_allowed(SftpOperation::Read));
    assert!(settings.is_file_operation_allowed(SftpOperation::List));
    assert!(settings.is_file_operation_allowed(SftpOperation::Stat));
    assert!(!settings.is_file_operation_allowed(SftpOperation::Download)); // disabled
    assert!(!settings.is_file_operation_allowed(SftpOperation::Upload)); // read_only
    assert!(!settings.is_file_operation_allowed(SftpOperation::Delete)); // read_only
    assert!(!settings.is_file_operation_allowed(SftpOperation::Rename)); // read_only
    assert!(!settings.is_file_operation_allowed(SftpOperation::Mkdir)); // read_only
    assert!(!settings.is_file_operation_allowed(SftpOperation::Rmdir)); // read_only
}

#[test]
fn test_rbi_security_full_workflow() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("rbi-disable-download".to_string(), "true".to_string());
    params.insert("rbi-disable-print".to_string(), "true".to_string());
    // Use substring patterns (URL matching uses contains, not glob patterns)
    params.insert(
        "rbi-url-allowlist".to_string(),
        "example.com, internal.corp".to_string(),
    );

    let settings = RbiSecuritySettings::from_params(&params);

    // Verify settings
    assert!(settings.base.read_only);
    assert!(settings.disable_download);
    assert!(settings.disable_print);
    assert!(!settings.is_upload_allowed()); // read_only blocks upload

    // Verify URL filtering (uses substring matching)
    assert!(settings.is_url_allowed("https://app.example.com/page"));
    assert!(settings.is_url_allowed("https://internal.corp/dashboard"));
    assert!(!settings.is_url_allowed("https://facebook.com"));
    assert!(!settings.is_url_allowed("https://malware-site.com"));
}

#[test]
fn test_keyboard_readonly_edge_cases() {
    // Navigation keys should be blocked in read-only
    assert!(!is_keyboard_event_allowed_readonly(0xFF08, false)); // Backspace
    assert!(!is_keyboard_event_allowed_readonly(0xFF09, false)); // Tab
    assert!(!is_keyboard_event_allowed_readonly(0xFF0D, false)); // Enter
    assert!(!is_keyboard_event_allowed_readonly(0xFF1B, false)); // Escape
    assert!(!is_keyboard_event_allowed_readonly(0xFFFF, false)); // Delete

    // Arrow keys (for text selection) - currently blocked too
    assert!(!is_keyboard_event_allowed_readonly(0xFF51, false)); // Left
    assert!(!is_keyboard_event_allowed_readonly(0xFF52, false)); // Up
    assert!(!is_keyboard_event_allowed_readonly(0xFF53, false)); // Right
    assert!(!is_keyboard_event_allowed_readonly(0xFF54, false)); // Down

    // Modifier keys alone should be allowed (they don't produce input)
    // Note: This depends on implementation - currently they're blocked
}

#[test]
fn test_mouse_readonly_edge_cases() {
    // Combined button presses should be blocked
    assert!(!is_mouse_event_allowed_readonly(0x03)); // Left + Middle
    assert!(!is_mouse_event_allowed_readonly(0x05)); // Left + Right
    assert!(!is_mouse_event_allowed_readonly(0x07)); // Left + Middle + Right

    // Scroll with buttons should be blocked
    assert!(!is_mouse_event_allowed_readonly(0x09)); // Left + Scroll up
    assert!(!is_mouse_event_allowed_readonly(0x11)); // Left + Scroll down

    // Pure scroll should be allowed
    assert!(is_mouse_event_allowed_readonly(0x08)); // Scroll up only
    assert!(is_mouse_event_allowed_readonly(0x10)); // Scroll down only
    assert!(is_mouse_event_allowed_readonly(0x18)); // Scroll up + down (edge case)
}
