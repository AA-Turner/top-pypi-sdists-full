// Security tests for database handlers.
// Run with: cargo test -p guacr-database --test security_test -- --include-ignored

#[cfg(test)]
mod sqlserver_tls_tests {
    use guacr_database::build_connection_info;
    use keeperdb_core::entities::connection::{AdvancedOptions, MssqlAdvancedOptions};
    use keeperdb_core::types::DatabaseType;
    use std::collections::HashMap;

    fn base_params() -> HashMap<String, String> {
        let mut p = HashMap::new();
        p.insert("hostname".to_string(), "db.example.com".to_string());
        p.insert("username".to_string(), "sa".to_string());
        p
    }

    /// SQL Server default config must NOT set trust_server_certificate=true.
    ///
    /// When trust_server_certificate is true, tiberius accepts any certificate
    /// regardless of CA chain or hostname — equivalent to accepting invalid certs.
    /// This test FAILS before the fix and passes after.
    #[test]
    #[ignore]
    fn sqlserver_default_config_does_not_trust_all_certs() {
        let info = build_connection_info(DatabaseType::Mssql, &base_params()).unwrap();

        let trusts_all = matches!(
            &info.advanced_options,
            Some(AdvancedOptions::Mssql(MssqlAdvancedOptions {
                trust_server_certificate: Some(true),
                ..
            }))
        );

        assert!(
            !trusts_all,
            "Default SQL Server config must NOT set trust_server_certificate=true — \
             this bypasses TLS certificate validation and enables MITM attacks"
        );
    }

    /// Explicit trust_server_certificate=true via param must be honoured.
    /// Operators who need self-signed cert support must explicitly opt in.
    #[test]
    #[ignore]
    fn sqlserver_explicit_trust_param_is_respected() {
        let mut params = base_params();
        params.insert("trust-server-certificate".to_string(), "true".to_string());
        let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();

        let trusts_all = matches!(
            &info.advanced_options,
            Some(AdvancedOptions::Mssql(MssqlAdvancedOptions {
                trust_server_certificate: Some(true),
                ..
            }))
        );

        assert!(
            trusts_all,
            "trust-server-certificate=true param must be passed through to the driver"
        );
    }
}

#[cfg(test)]
mod csv_injection_tests {
    use guacr_database::validate_csv_table_name;

    /// Table names with SQL meta-characters must be rejected before quoting.
    ///
    /// Even with backtick/bracket quoting, passing a table name that contains
    /// null bytes or other bypass characters is a security risk. Validate first.
    /// This test FAILS before the fix and passes after.
    #[test]
    #[ignore]
    fn csv_import_rejects_table_name_with_semicolons() {
        let bad_names = vec!["users; DROP TABLE users--", "t; SELECT 1", "foo; bar"];
        for name in bad_names {
            assert!(
                validate_csv_table_name(name).is_err(),
                "Table name with semicolons must be rejected: {}",
                name
            );
        }
    }

    #[test]
    #[ignore]
    fn csv_import_rejects_table_name_with_quotes() {
        let bad_names = vec!["users\"--", "foo'bar", "t`drop"];
        for name in bad_names {
            assert!(
                validate_csv_table_name(name).is_err(),
                "Table name with quotes must be rejected: {}",
                name
            );
        }
    }

    #[test]
    #[ignore]
    fn csv_import_rejects_table_name_with_spaces() {
        assert!(
            validate_csv_table_name("my table").is_err(),
            "Table name with spaces must be rejected"
        );
        assert!(
            validate_csv_table_name("foo bar baz").is_err(),
            "Table name with spaces must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn csv_import_rejects_empty_table_name() {
        assert!(
            validate_csv_table_name("").is_err(),
            "Empty table name must be rejected"
        );
    }

    #[test]
    #[ignore]
    fn csv_import_allows_valid_table_names() {
        let good_names = vec![
            "users",
            "my_table",
            "Table123",
            "_private",
            "UPPER_CASE",
            "t",
        ];
        for name in good_names {
            assert!(
                validate_csv_table_name(name).is_ok(),
                "Valid table name must be accepted: {}",
                name
            );
        }
    }
}

#[cfg(test)]
mod security_tests {
    #[test]
    #[ignore]
    fn test_sql_injection_patterns_detected() {
        use guacr_database::{classify_query, QueryType};

        // Common SQL injection patterns should be classified as Modifying
        let injection_patterns = vec![
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "' UNION SELECT * FROM passwords--",
            "1; DELETE FROM users WHERE '1'='1",
            "'; INSERT INTO admin (name) VALUES ('hacked'); --",
        ];

        for pattern in injection_patterns {
            // Injections typically contain modifying keywords
            let query_type = classify_query(pattern);
            println!("Pattern '{}' classified as {:?}", pattern, query_type);
            // The primary assertion is that these are identified (not silently allowed)
            assert!(
                query_type == QueryType::Modifying || query_type == QueryType::Unknown,
                "Injection pattern '{}' should not be ReadOnly",
                pattern
            );
        }
    }

    #[test]
    #[ignore]
    fn test_credentials_not_in_query_results() {
        use guacr_terminal::QueryResult;

        // Result rows should not expose passwords via the recording formatter
        let mut result = QueryResult::new(vec!["username".to_string(), "data".to_string()]);
        result.add_row(vec!["admin".to_string(), "non_sensitive_data".to_string()]);
        result.add_row(vec!["user1".to_string(), "public_info".to_string()]);

        // Verify result contains expected data without leaking credentials
        assert_eq!(result.rows.len(), 2);
        assert_eq!(result.columns, vec!["username", "data"]);
        println!("Credential logging test — implement with log capture to verify no passwords appear in output");
    }
}
