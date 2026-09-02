use crate::sql::SqlHandler;
use guacr_handlers::ProtocolHandler;

#[test]
fn test_postgresql_handler_name() {
    assert_eq!(SqlHandler::postgresql().name(), "postgresql");
}

#[test]
fn test_postgresql_explicit_port_overrides_default() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "pg.example.com".to_string());
    p.insert("username".to_string(), "postgres".to_string());
    p.insert("port".to_string(), "5433".to_string());
    let info = build_connection_info(DatabaseType::Postgres, &p).unwrap();
    assert_eq!(
        info.port,
        Some(5433),
        "explicit port=5433 must override the default"
    );
}

#[test]
fn test_postgresql_ssl_prefer_by_default() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::SslMode, types::DatabaseType};
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "pg.example.com".to_string());
    p.insert("username".to_string(), "postgres".to_string());
    let info = build_connection_info(DatabaseType::Postgres, &p).unwrap();
    assert!(
        matches!(info.ssl_mode, SslMode::Prefer),
        "PostgreSQL must default to SslMode::Prefer"
    );
}

#[test]
fn test_postgresql_tls_verify_require() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::SslMode, types::DatabaseType};
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "pg.example.com".to_string());
    p.insert("username".to_string(), "postgres".to_string());
    p.insert("tls-verify".to_string(), "require".to_string());
    let info = build_connection_info(DatabaseType::Postgres, &p).unwrap();
    assert!(
        matches!(info.ssl_mode, SslMode::Require),
        "tls-verify=require must map to SslMode::Require"
    );
}

#[test]
fn test_postgresql_database_param_captured() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "pg.example.com".to_string());
    p.insert("username".to_string(), "postgres".to_string());
    p.insert("database".to_string(), "mydb".to_string());
    let info = build_connection_info(DatabaseType::Postgres, &p).unwrap();
    assert_eq!(
        info.database, "mydb",
        "database param must be captured in ConnectionInfo"
    );
}

#[test]
fn test_postgresql_missing_hostname_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("username".to_string(), "postgres".to_string());
    // hostname intentionally absent
    let result = build_connection_info(DatabaseType::Postgres, &p);
    assert!(result.is_err(), "missing hostname must return an error");
}

#[test]
fn test_postgresql_missing_username_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "pg.example.com".to_string());
    // username intentionally absent
    let result = build_connection_info(DatabaseType::Postgres, &p);
    assert!(result.is_err(), "missing username must return an error");
}
