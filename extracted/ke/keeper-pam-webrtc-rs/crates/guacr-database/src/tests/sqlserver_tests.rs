use crate::sqlserver::{SqlServerConfig, SqlServerHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_sqlserver_handler_new() {
    let handler = SqlServerHandler::with_defaults();
    assert_eq!(
        <SqlServerHandler as ProtocolHandler>::name(&handler),
        "sqlserver"
    );
}

#[test]
fn test_sqlserver_config() {
    let config = SqlServerConfig::default();
    assert_eq!(config.default_port, 1433);
}
