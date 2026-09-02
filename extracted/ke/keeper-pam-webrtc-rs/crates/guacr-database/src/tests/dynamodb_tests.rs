use crate::dynamodb::{
    format_attribute_value, is_dynamodb_modifying_statement, DynamoDbConfig, DynamoDbHandler,
};
use aws_sdk_dynamodb::types::AttributeValue;
use guacr_handlers::ProtocolHandler;
use std::collections::HashMap;

#[test]
fn test_dynamodb_handler_new() {
    let handler = DynamoDbHandler::with_defaults();
    assert_eq!(
        <DynamoDbHandler as ProtocolHandler>::name(&handler),
        "dynamodb"
    );
}

#[test]
fn test_dynamodb_config() {
    let config = DynamoDbConfig::default();
    assert_eq!(config.default_port, 8000);
    assert!(!config.require_tls);
}

#[test]
fn test_format_attribute_value_string() {
    let av = AttributeValue::S("hello".to_string());
    assert_eq!(format_attribute_value(&av), "hello");
}

#[test]
fn test_format_attribute_value_number() {
    let av = AttributeValue::N("42".to_string());
    assert_eq!(format_attribute_value(&av), "42");
}

#[test]
fn test_format_attribute_value_bool() {
    let av = AttributeValue::Bool(true);
    assert_eq!(format_attribute_value(&av), "true");

    let av = AttributeValue::Bool(false);
    assert_eq!(format_attribute_value(&av), "false");
}

#[test]
fn test_format_attribute_value_null() {
    let av = AttributeValue::Null(true);
    assert_eq!(format_attribute_value(&av), "NULL");
}

#[test]
fn test_format_attribute_value_list() {
    let av = AttributeValue::L(vec![
        AttributeValue::S("a".to_string()),
        AttributeValue::N("1".to_string()),
    ]);
    assert_eq!(format_attribute_value(&av), "[a, 1]");
}

#[test]
fn test_format_attribute_value_map() {
    let mut map = HashMap::new();
    map.insert("key".to_string(), AttributeValue::S("val".to_string()));
    let av = AttributeValue::M(map);
    assert_eq!(format_attribute_value(&av), "{key: val}");
}

#[test]
fn test_format_attribute_value_string_set() {
    let av = AttributeValue::Ss(vec!["a".to_string(), "b".to_string(), "c".to_string()]);
    assert_eq!(format_attribute_value(&av), "[a, b, c]");
}

#[test]
fn test_format_attribute_value_number_set() {
    let av = AttributeValue::Ns(vec!["1".to_string(), "2".to_string(), "3".to_string()]);
    assert_eq!(format_attribute_value(&av), "[1, 2, 3]");
}

#[test]
fn test_is_dynamodb_modifying_statement() {
    // Modifying statements
    assert!(is_dynamodb_modifying_statement(
        "INSERT INTO \"Users\" VALUE {'id': '1'}"
    ));
    assert!(is_dynamodb_modifying_statement(
        "UPDATE \"Users\" SET name = 'x' WHERE id = '1'"
    ));
    assert!(is_dynamodb_modifying_statement(
        "DELETE FROM \"Users\" WHERE id = '1'"
    ));
    assert!(is_dynamodb_modifying_statement(
        "CREATE TABLE test (id S HASH)"
    ));
    assert!(is_dynamodb_modifying_statement("DROP TABLE test"));

    // Read-only statements
    assert!(!is_dynamodb_modifying_statement("SELECT * FROM \"Users\""));
    assert!(!is_dynamodb_modifying_statement("LIST TABLES"));
    assert!(!is_dynamodb_modifying_statement("\\tables"));
    assert!(!is_dynamodb_modifying_statement("help"));
}

#[test]
fn test_is_dynamodb_modifying_case_insensitive() {
    assert!(is_dynamodb_modifying_statement(
        "insert into \"T\" VALUE {'pk': '1'}"
    ));
    assert!(is_dynamodb_modifying_statement(
        "update \"T\" SET x = 1 WHERE pk = '1'"
    ));
    assert!(is_dynamodb_modifying_statement(
        "delete from \"T\" WHERE pk = '1'"
    ));
}
