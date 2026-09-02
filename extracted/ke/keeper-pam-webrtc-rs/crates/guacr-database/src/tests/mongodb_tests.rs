use crate::mongodb::{is_mongodb_modifying_command, MongoDbConfig, MongoDbHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_mongodb_handler_new() {
    let handler = MongoDbHandler::with_defaults();
    assert_eq!(
        <MongoDbHandler as ProtocolHandler>::name(&handler),
        "mongodb"
    );
}

#[test]
fn test_mongodb_config_default_port() {
    let config = MongoDbConfig::default();
    assert_eq!(config.default_port, 27017);
}

#[test]
fn test_mongodb_config_tls_off_by_default() {
    let config = MongoDbConfig::default();
    assert!(!config.require_tls);
}

#[test]
fn test_mongodb_config_connection_timeout() {
    let config = MongoDbConfig::default();
    assert!(config.connection_timeout_secs > 0);
}

#[test]
fn test_mongodb_as_event_based() {
    let handler = MongoDbHandler::with_defaults();
    assert!(<MongoDbHandler as ProtocolHandler>::as_event_based(&handler).is_some());
}

#[test]
fn test_mongodb_custom_config() {
    let config = MongoDbConfig {
        default_port: 27018,
        require_tls: true,
        connection_timeout_secs: 60,
    };
    let handler = MongoDbHandler::new(config.clone());
    assert_eq!(
        <MongoDbHandler as ProtocolHandler>::name(&handler),
        "mongodb"
    );
    assert_eq!(config.default_port, 27018);
    assert!(config.require_tls);
    assert_eq!(config.connection_timeout_secs, 60);
}

#[test]
fn test_is_mongodb_modifying_command_insert() {
    assert!(is_mongodb_modifying_command("insert myCollection {...}"));
    assert!(is_mongodb_modifying_command("INSERT myCollection {...}"));
}

#[test]
fn test_is_mongodb_modifying_command_update() {
    assert!(is_mongodb_modifying_command("update myCollection {}"));
    assert!(is_mongodb_modifying_command("UPDATE myCollection {}"));
}

#[test]
fn test_is_mongodb_modifying_command_delete() {
    assert!(is_mongodb_modifying_command("delete myCollection {}"));
    assert!(is_mongodb_modifying_command("DELETE myCollection {}"));
}

#[test]
fn test_is_mongodb_modifying_command_drop() {
    assert!(is_mongodb_modifying_command("drop myCollection"));
    assert!(is_mongodb_modifying_command("DROP myCollection"));
}

#[test]
fn test_is_mongodb_modifying_command_create() {
    assert!(is_mongodb_modifying_command("create myCollection"));
    assert!(is_mongodb_modifying_command("CREATE myCollection"));
}

#[test]
fn test_is_mongodb_modifying_command_rename() {
    assert!(is_mongodb_modifying_command("rename myCollection newName"));
}

#[test]
fn test_is_mongodb_modifying_command_read_only_commands() {
    assert!(!is_mongodb_modifying_command("show collections"));
    assert!(!is_mongodb_modifying_command("db"));
    assert!(!is_mongodb_modifying_command("stats"));
    assert!(!is_mongodb_modifying_command("help"));
    assert!(!is_mongodb_modifying_command("use admin"));
}

#[test]
fn test_is_mongodb_modifying_command_json_insert() {
    assert!(is_mongodb_modifying_command(
        r#"{"insert": "myCol", "documents": []}"#
    ));
}

#[test]
fn test_is_mongodb_modifying_command_json_find_is_readonly() {
    assert!(!is_mongodb_modifying_command(
        r#"{"find": "myCol", "filter": {}}"#
    ));
    assert!(!is_mongodb_modifying_command(
        r#"{"aggregate": "myCol", "pipeline": []}"#
    ));
}

#[test]
fn test_is_mongodb_modifying_command_empty() {
    assert!(!is_mongodb_modifying_command(""));
    assert!(!is_mongodb_modifying_command("   "));
}
