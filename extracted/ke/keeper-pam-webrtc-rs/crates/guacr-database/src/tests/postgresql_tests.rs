use crate::postgresql::{PostgreSqlConfig, PostgreSqlHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_postgresql_handler_new() {
    let handler = PostgreSqlHandler::with_defaults();
    assert_eq!(
        <PostgreSqlHandler as ProtocolHandler>::name(&handler),
        "postgres"
    );
}

#[test]
fn test_postgresql_config() {
    let config = PostgreSqlConfig::default();
    assert_eq!(config.default_port, 5432);
}
