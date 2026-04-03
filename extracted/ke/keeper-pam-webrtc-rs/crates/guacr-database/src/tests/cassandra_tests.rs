use crate::cassandra::{
    format_cql_value, format_tabular_output, is_cql_modifying_command, CassandraConfig,
    CassandraHandler,
};
use guacr_handlers::ProtocolHandler;
use scylla::frame::response::result::CqlValue;

#[test]
fn test_cassandra_handler_new() {
    let handler = CassandraHandler::with_defaults();
    assert_eq!(
        <CassandraHandler as ProtocolHandler>::name(&handler),
        "cassandra"
    );
}

#[test]
fn test_cassandra_config() {
    let config = CassandraConfig::default();
    assert_eq!(config.default_port, 9042);
    assert!(!config.require_auth);
    assert!(!config.require_tls);
}

#[test]
fn test_format_cql_value_primitives() {
    assert_eq!(format_cql_value(&None), "NULL");
    assert_eq!(
        format_cql_value(&Some(CqlValue::Text("hello".to_string()))),
        "hello"
    );
    assert_eq!(format_cql_value(&Some(CqlValue::Int(42))), "42");
    assert_eq!(
        format_cql_value(&Some(CqlValue::BigInt(1234567890))),
        "1234567890"
    );
    assert_eq!(format_cql_value(&Some(CqlValue::Boolean(true))), "true");
    assert_eq!(format_cql_value(&Some(CqlValue::Float(3.25_f32))), "3.25");
    assert_eq!(format_cql_value(&Some(CqlValue::Double(2.5_f64))), "2.5");
    assert_eq!(format_cql_value(&Some(CqlValue::SmallInt(16))), "16");
    assert_eq!(format_cql_value(&Some(CqlValue::TinyInt(8))), "8");
    assert_eq!(
        format_cql_value(&Some(CqlValue::Ascii("ascii".to_string()))),
        "ascii"
    );
    assert_eq!(format_cql_value(&Some(CqlValue::Empty)), "");
}

#[test]
fn test_format_cql_value_blob() {
    assert_eq!(
        format_cql_value(&Some(CqlValue::Blob(vec![0xDE, 0xAD, 0xBE, 0xEF]))),
        "0xdeadbeef"
    );
}

#[test]
fn test_format_cql_value_collections() {
    let list = CqlValue::List(vec![CqlValue::Int(1), CqlValue::Int(2), CqlValue::Int(3)]);
    assert_eq!(format_cql_value(&Some(list)), "[1, 2, 3]");

    let set = CqlValue::Set(vec![
        CqlValue::Text("a".to_string()),
        CqlValue::Text("b".to_string()),
    ]);
    assert_eq!(format_cql_value(&Some(set)), "{a, b}");

    let map = CqlValue::Map(vec![
        (CqlValue::Text("key1".to_string()), CqlValue::Int(100)),
        (CqlValue::Text("key2".to_string()), CqlValue::Int(200)),
    ]);
    assert_eq!(format_cql_value(&Some(map)), "{key1: 100, key2: 200}");
}

#[test]
fn test_format_cql_value_tuple() {
    let tuple = CqlValue::Tuple(vec![
        Some(CqlValue::Int(1)),
        Some(CqlValue::Text("hello".to_string())),
        None,
    ]);
    assert_eq!(format_cql_value(&Some(tuple)), "(1, hello, NULL)");
}

#[test]
fn test_format_cql_value_inet() {
    let addr: std::net::IpAddr = "127.0.0.1".parse().unwrap();
    assert_eq!(format_cql_value(&Some(CqlValue::Inet(addr))), "127.0.0.1");
}

#[test]
fn test_is_cql_modifying_command() {
    assert!(is_cql_modifying_command(
        "INSERT INTO users (id) VALUES (1)"
    ));
    assert!(is_cql_modifying_command("UPDATE users SET name = 'x'"));
    assert!(is_cql_modifying_command("DELETE FROM users WHERE id = 1"));
    assert!(is_cql_modifying_command("DROP TABLE users"));
    assert!(is_cql_modifying_command("TRUNCATE users"));
    assert!(is_cql_modifying_command("ALTER TABLE users ADD col text"));
    assert!(is_cql_modifying_command(
        "CREATE TABLE t (id int PRIMARY KEY)"
    ));
    assert!(is_cql_modifying_command("GRANT SELECT ON users TO user1"));
    assert!(is_cql_modifying_command(
        "REVOKE SELECT ON users FROM user1"
    ));
    assert!(is_cql_modifying_command("BATCH USING TIMESTAMP 1234"));

    assert!(!is_cql_modifying_command("SELECT * FROM users"));
    assert!(!is_cql_modifying_command("DESCRIBE KEYSPACES"));
    assert!(!is_cql_modifying_command("USE mykeyspace"));
    assert!(!is_cql_modifying_command("help"));
}

#[test]
fn test_format_tabular_output_empty() {
    let result = format_tabular_output(&[], &[], 5);
    assert!(result.contains("(0 rows)"));
}

#[test]
fn test_format_tabular_output_with_data() {
    let columns = vec!["id".to_string(), "name".to_string()];
    let rows = vec![
        vec!["1".to_string(), "Alice".to_string()],
        vec!["2".to_string(), "Bob".to_string()],
    ];
    let result = format_tabular_output(&columns, &rows, 10);

    assert!(result.contains("id"));
    assert!(result.contains("name"));
    assert!(result.contains("Alice"));
    assert!(result.contains("Bob"));
    assert!(result.contains("(2 rows)"));
}

#[test]
fn test_format_tabular_output_single_row() {
    let columns = vec!["count".to_string()];
    let rows = vec![vec!["42".to_string()]];
    let result = format_tabular_output(&columns, &rows, 1);

    assert!(result.contains("(1 row)"));
}

#[test]
fn test_format_tabular_output_long_values_truncated() {
    let columns = vec!["data".to_string()];
    let long_value = "x".repeat(100);
    let rows = vec![vec![long_value]];
    let result = format_tabular_output(&columns, &rows, 1);

    // Should be truncated with "..."
    assert!(result.contains("..."));
}
