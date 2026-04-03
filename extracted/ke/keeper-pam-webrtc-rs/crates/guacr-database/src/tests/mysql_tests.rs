use crate::mysql::{mysql_value_to_string, MySqlConfig, MySqlHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_mysql_handler_new() {
    let handler = MySqlHandler::with_defaults();
    assert_eq!(<MySqlHandler as ProtocolHandler>::name(&handler), "mysql");
}

#[test]
fn test_mysql_config() {
    let config = MySqlConfig::default();
    assert_eq!(config.default_port, 3306);
}

#[test]
fn test_mysql_value_to_string() {
    assert_eq!(mysql_value_to_string(mysql_async::Value::NULL), "NULL");
    assert_eq!(mysql_value_to_string(mysql_async::Value::Int(42)), "42");
    assert_eq!(mysql_value_to_string(mysql_async::Value::UInt(100)), "100");
}
