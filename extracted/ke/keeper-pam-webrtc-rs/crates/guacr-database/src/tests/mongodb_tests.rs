use crate::mongodb::{MongoDbConfig, MongoDbHandler};
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
fn test_mongodb_config() {
    let config = MongoDbConfig::default();
    assert_eq!(config.default_port, 27017);
}
