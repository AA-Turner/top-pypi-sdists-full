use crate::redis::{format_redis_value, RedisConfig, RedisHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_redis_handler_new() {
    let handler = RedisHandler::with_defaults();
    assert_eq!(<RedisHandler as ProtocolHandler>::name(&handler), "redis");
}

#[test]
fn test_redis_config() {
    let config = RedisConfig::default();
    assert_eq!(config.default_port, 6379);
    assert!(config.require_auth);
}

#[test]
fn test_format_redis_value() {
    assert_eq!(format_redis_value(&redis::Value::Nil), "(nil)");
    assert_eq!(format_redis_value(&redis::Value::Int(42)), "(integer) 42");
    assert_eq!(format_redis_value(&redis::Value::Okay), "OK");
}
