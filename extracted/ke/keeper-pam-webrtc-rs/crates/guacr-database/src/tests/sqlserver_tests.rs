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

/// trust-server-certificate must NOT be set when the param is absent.
///
/// The CHANGELOG records this as a security fix: defaulting to trust=true
/// bypassed TLS certificate validation entirely. The param must be absent
/// from AdvancedOptions (i.e. None) when the operator has not explicitly
/// requested it, so the driver falls back to its own default (verify).
#[test]
fn test_sqlserver_trust_cert_absent_when_param_not_set() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::AdvancedOptions, types::DatabaseType};
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "mssql.example.com".to_string());
    params.insert("username".to_string(), "sa".to_string());
    // trust-server-certificate NOT supplied
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    match info.advanced_options {
        None => { /* correct: no trust override set */ }
        Some(AdvancedOptions::Mssql(ref opts)) => {
            assert!(
                opts.trust_server_certificate != Some(true),
                "trust_server_certificate must not be true when param is absent"
            );
        }
        Some(_) => {}
    }
}

/// trust-server-certificate=false must NOT set trust=true.
#[test]
fn test_sqlserver_trust_cert_false_does_not_enable_trust() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::AdvancedOptions, types::DatabaseType};
    let mut params = std::collections::HashMap::new();
    params.insert("hostname".to_string(), "mssql.example.com".to_string());
    params.insert("username".to_string(), "sa".to_string());
    params.insert("trust-server-certificate".to_string(), "false".to_string());
    let info = build_connection_info(DatabaseType::Mssql, &params).unwrap();
    match info.advanced_options {
        None => { /* correct */ }
        Some(AdvancedOptions::Mssql(ref opts)) => {
            assert!(
                opts.trust_server_certificate != Some(true),
                "trust_server_certificate must not be true when param is 'false'"
            );
        }
        Some(_) => {}
    }
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
