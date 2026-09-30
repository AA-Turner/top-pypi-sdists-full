use crate::sql::SqlHandler;
use guacr_handlers::ProtocolHandler;

#[test]
fn test_sqlserver_handler_name() {
    assert_eq!(SqlHandler::sql_server().name(), "sql-server");
}

/// Missing hostname must fail — same as MySQL/PostgreSQL validation.
#[test]
fn test_sqlserver_missing_hostname_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("username".to_string(), "sa".to_string());
    assert!(
        build_connection_info(DatabaseType::Mssql, &p).is_err(),
        "missing hostname must return an error"
    );
}

/// Missing username must fail.
#[test]
fn test_sqlserver_missing_username_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "mssql.example.com".to_string());
    assert!(
        build_connection_info(DatabaseType::Mssql, &p).is_err(),
        "missing username must return an error"
    );
}

/// trust-server-certificate absent: no override is sent, so keeperdb applies
/// its own default (trust for SQL and Windows logins, validate for Azure AD).
#[test]
fn test_sqlserver_trust_cert_absent_when_param_not_set() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "mssql.example.com".to_string());
    params.insert("username".to_string(), "sa".to_string());
    // trust-server-certificate NOT supplied
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    assert!(
        info.advanced_options.is_none(),
        "no trust override must be sent when the param is absent"
    );
}

/// trust-server-certificate=false must reach keeperdb as Some(false). It is the
/// only way to get strict certificate validation for SQL and Windows logins;
/// dropping it to None would silently fall back to trust.
#[test]
fn test_sqlserver_trust_cert_false_requests_strict_validation() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::AdvancedOptions, types::DatabaseType};
    for value in ["false", "0", "FALSE"] {
        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), "mssql.example.com".to_string());
        params.insert("username".to_string(), "sa".to_string());
        params.insert("trust-server-certificate".to_string(), value.to_string());
        let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
        match info.advanced_options {
            Some(AdvancedOptions::Mssql(opts)) => assert_eq!(
                opts.trust_server_certificate,
                Some(false),
                "trust-server-certificate={value} must be sent as Some(false)"
            ),
            other => panic!("expected Mssql advanced options for {value}, got {other:?}"),
        }
    }
}

/// An unrecognised value is rejected. Falling back to keeperdb's default would
/// turn a mistyped strict request (e.g. "flase") into trust.
#[test]
fn test_sqlserver_trust_cert_invalid_value_is_rejected() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "mssql.example.com".to_string());
    params.insert("username".to_string(), "sa".to_string());
    params.insert("trust-server-certificate".to_string(), "flase".to_string());
    assert!(build_connection_info(DatabaseType::Mssql, &params).is_err());
}

/// An empty value is treated as absent, since unset Guacamole params may arrive
/// as empty strings.
#[test]
fn test_sqlserver_trust_cert_empty_value_is_absent() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "mssql.example.com".to_string());
    params.insert("username".to_string(), "sa".to_string());
    params.insert("trust-server-certificate".to_string(), "".to_string());
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    assert!(info.advanced_options.is_none());
}

/// The param only applies to SQL Server; other databases ignore it.
#[test]
fn test_trust_cert_param_ignored_for_non_mssql() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "pg.example.com".to_string());
    params.insert("username".to_string(), "postgres".to_string());
    params.insert("trust-server-certificate".to_string(), "flase".to_string());
    let info = build_connection_info(DatabaseType::Postgres, &params).unwrap();
    assert!(info.advanced_options.is_none());
}

/// trust-server-certificate=true must set the flag — this is the intentional
/// opt-in path for operators who have self-signed certs on their SQL Server.
#[test]
fn test_sqlserver_trust_cert_true_sets_flag() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::AdvancedOptions, types::DatabaseType};
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "mssql.example.com".to_string());
    params.insert("username".to_string(), "sa".to_string());
    params.insert("trust-server-certificate".to_string(), "true".to_string());
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    let advanced = info
        .advanced_options
        .expect("advanced_options must be Some");
    match advanced {
        AdvancedOptions::Mssql(opts) => {
            assert_eq!(
                opts.trust_server_certificate,
                Some(true),
                "trust_server_certificate must be Some(true) when explicitly requested"
            );
        }
        _ => panic!("expected Mssql advanced options"),
    }
}

#[test]
fn test_sqlserver_tls_verify_false_disables_tls() {
    // tls-verify=false must map to SslMode::Disable so connections to
    // SQL Server instances without TLS succeed.
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "localhost".to_string());
    params.insert("username".to_string(), "sa".to_string());
    params.insert("tls-verify".to_string(), "false".to_string());
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    assert!(matches!(
        info.ssl_mode,
        keeperdb_core::entities::connection::SslMode::Disable
    ));
}

#[test]
fn test_sqlserver_default_ssl_mode_is_prefer() {
    // Without tls-verify param the default is SslMode::Prefer (try TLS, fall back).
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "localhost".to_string());
    params.insert("username".to_string(), "sa".to_string());
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    assert!(matches!(
        info.ssl_mode,
        keeperdb_core::entities::connection::SslMode::Prefer
    ));
}

#[test]
fn test_sqlserver_tls_verify_require_sets_require() {
    // tls-verify=require must map to SslMode::Require (strict TLS, verify cert).
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "localhost".to_string());
    params.insert("username".to_string(), "sa".to_string());
    params.insert("tls-verify".to_string(), "require".to_string());
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    assert!(matches!(
        info.ssl_mode,
        keeperdb_core::entities::connection::SslMode::Require
    ));
}
