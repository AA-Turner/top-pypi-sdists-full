use crate::sql::SqlHandler;
use guacr_handlers::ProtocolHandler;

#[test]
fn test_oracle_handler_name() {
    assert_eq!(SqlHandler::oracle().name(), "oracle");
}

#[test]
fn test_oracle_explicit_port_overrides_default() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "oracle.example.com".to_string());
    p.insert("username".to_string(), "system".to_string());
    p.insert("port".to_string(), "1522".to_string());
    let info = build_connection_info(DatabaseType::Oracle, &p).unwrap();
    assert_eq!(info.port, Some(1522), "explicit port must be captured");
}

#[test]
fn test_oracle_ssl_prefer_by_default() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::SslMode, types::DatabaseType};
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "oracle.example.com".to_string());
    p.insert("username".to_string(), "system".to_string());
    let info = build_connection_info(DatabaseType::Oracle, &p).unwrap();
    assert!(
        matches!(info.ssl_mode, SslMode::Prefer),
        "Oracle must default to SslMode::Prefer"
    );
}

#[test]
fn test_oracle_missing_hostname_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("username".to_string(), "system".to_string());
    assert!(
        build_connection_info(DatabaseType::Oracle, &p).is_err(),
        "missing hostname must return an error"
    );
}
