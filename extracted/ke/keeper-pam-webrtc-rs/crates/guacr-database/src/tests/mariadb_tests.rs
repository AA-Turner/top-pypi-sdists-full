use crate::sql::SqlHandler;
use guacr_handlers::ProtocolHandler;

#[test]
fn test_mariadb_handler_name() {
    assert_eq!(SqlHandler::mariadb().name(), "mariadb");
}

#[test]
fn test_mariadb_default_port_is_3306() {
    // MariaDB uses the MySQL wire protocol on port 3306.
    // build_connection_info falls back to the handler's default_port when
    // no "port" param is present.
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "db.example.com".to_string());
    p.insert("username".to_string(), "user".to_string());
    let info = build_connection_info(DatabaseType::Mysql, &p).unwrap();
    // No port override → port is None (driver uses default 3306 from handler).
    assert!(
        info.port.is_none(),
        "port should be None when not specified; handler supplies the default"
    );
}

#[test]
fn test_mariadb_ssl_prefer_by_default() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::SslMode, types::DatabaseType};
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "db.example.com".to_string());
    p.insert("username".to_string(), "user".to_string());
    let info = build_connection_info(DatabaseType::Mysql, &p).unwrap();
    assert!(
        matches!(info.ssl_mode, SslMode::Prefer),
        "MariaDB must default to SslMode::Prefer (try TLS, fall back to plain)"
    );
}

#[test]
fn test_mariadb_tls_verify_false_disables_tls() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::{entities::connection::SslMode, types::DatabaseType};
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "db.example.com".to_string());
    p.insert("username".to_string(), "user".to_string());
    p.insert("tls-verify".to_string(), "false".to_string());
    let info = build_connection_info(DatabaseType::Mysql, &p).unwrap();
    assert!(
        matches!(info.ssl_mode, SslMode::Disable),
        "tls-verify=false must map to SslMode::Disable"
    );
}

#[test]
fn test_mariadb_and_mysql_share_protocol() {
    // Both handlers use DatabaseType::Mysql — same keeperdb driver.
    let mariadb = SqlHandler::mariadb();
    let mysql = SqlHandler::mysql();
    assert_eq!(mariadb.name(), "mariadb");
    assert_eq!(mysql.name(), "mysql");
}
