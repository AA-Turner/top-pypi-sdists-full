use crate::redis::{format_redis_value, is_redis_modifying_command, RedisConfig, RedisHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_redis_handler_new() {
    let handler = RedisHandler::with_defaults();
    assert_eq!(<RedisHandler as ProtocolHandler>::name(&handler), "redis");
}

#[test]
fn test_redis_config_default_port() {
    let config = RedisConfig::default();
    assert_eq!(config.default_port, 6379);
}

#[test]
fn test_redis_config_require_auth() {
    let config = RedisConfig::default();
    assert!(config.require_auth);
}

#[test]
fn test_redis_config_tls_off_by_default() {
    let config = RedisConfig::default();
    assert!(!config.require_tls);
}

#[test]
fn test_redis_config_connection_timeout() {
    let config = RedisConfig::default();
    assert!(config.connection_timeout_secs > 0);
}

#[test]
fn test_redis_as_event_based() {
    let handler = RedisHandler::with_defaults();
    assert!(<RedisHandler as ProtocolHandler>::as_event_based(&handler).is_some());
}

#[test]
fn test_redis_custom_config() {
    let config = RedisConfig {
        default_port: 6380,
        require_tls: true,
        require_auth: false,
        connection_timeout_secs: 30,
    };
    let handler = RedisHandler::new(config.clone());
    assert_eq!(<RedisHandler as ProtocolHandler>::name(&handler), "redis");
    assert_eq!(config.default_port, 6380);
    assert!(config.require_tls);
    assert!(!config.require_auth);
}

#[test]
fn test_format_redis_value_nil() {
    assert_eq!(format_redis_value(&redis::Value::Nil), "(nil)");
}

#[test]
fn test_format_redis_value_integer() {
    assert_eq!(format_redis_value(&redis::Value::Int(42)), "(integer) 42");
    assert_eq!(format_redis_value(&redis::Value::Int(-1)), "(integer) -1");
    assert_eq!(format_redis_value(&redis::Value::Int(0)), "(integer) 0");
}

#[test]
fn test_format_redis_value_ok() {
    assert_eq!(format_redis_value(&redis::Value::Okay), "OK");
}

#[test]
fn test_format_redis_value_simple_string() {
    assert_eq!(
        format_redis_value(&redis::Value::SimpleString("PONG".to_string())),
        "PONG"
    );
}

#[test]
fn test_format_redis_value_bulk_string_utf8() {
    assert_eq!(
        format_redis_value(&redis::Value::BulkString(b"hello".to_vec())),
        "\"hello\""
    );
}

#[test]
fn test_format_redis_value_bulk_string_binary() {
    // Non-UTF-8 bytes fall back to binary display
    let binary = vec![0xff, 0xfe, 0x00];
    let result = format_redis_value(&redis::Value::BulkString(binary));
    assert!(result.starts_with("(binary)"));
    assert!(result.contains("3 bytes"));
}

#[test]
fn test_format_redis_value_empty_array() {
    assert_eq!(
        format_redis_value(&redis::Value::Array(vec![])),
        "(empty array)"
    );
}

#[test]
fn test_format_redis_value_array() {
    let arr = vec![
        redis::Value::BulkString(b"foo".to_vec()),
        redis::Value::BulkString(b"bar".to_vec()),
    ];
    let result = format_redis_value(&redis::Value::Array(arr));
    assert!(result.contains("1) \"foo\""));
    assert!(result.contains("2) \"bar\""));
}

#[test]
fn test_format_redis_value_double() {
    let result = format_redis_value(&redis::Value::Double(2.72));
    assert!(result.starts_with("(double)"));
    assert!(result.contains("2.72"));
}

#[test]
fn test_format_redis_value_boolean() {
    assert_eq!(
        format_redis_value(&redis::Value::Boolean(true)),
        "(boolean) true"
    );
    assert_eq!(
        format_redis_value(&redis::Value::Boolean(false)),
        "(boolean) false"
    );
}

#[test]
fn test_is_redis_modifying_command_write_ops() {
    assert!(is_redis_modifying_command("SET key value"));
    assert!(is_redis_modifying_command("set key value"));
    assert!(is_redis_modifying_command("DEL key"));
    assert!(is_redis_modifying_command("HSET myhash field value"));
    assert!(is_redis_modifying_command("LPUSH mylist value"));
    assert!(is_redis_modifying_command("SADD myset member"));
    assert!(is_redis_modifying_command("ZADD myzset 1.0 member"));
    assert!(is_redis_modifying_command("FLUSHDB"));
    assert!(is_redis_modifying_command("FLUSHALL"));
}

#[test]
fn test_is_redis_modifying_command_read_ops() {
    assert!(!is_redis_modifying_command("GET key"));
    assert!(!is_redis_modifying_command("HGET myhash field"));
    assert!(!is_redis_modifying_command("LRANGE mylist 0 -1"));
    assert!(!is_redis_modifying_command("SMEMBERS myset"));
    assert!(!is_redis_modifying_command("KEYS *"));
    assert!(!is_redis_modifying_command("INFO"));
    assert!(!is_redis_modifying_command("PING"));
    assert!(!is_redis_modifying_command("TTL key"));
}

#[test]
fn test_is_redis_modifying_command_empty() {
    assert!(!is_redis_modifying_command(""));
    assert!(!is_redis_modifying_command("   "));
}
