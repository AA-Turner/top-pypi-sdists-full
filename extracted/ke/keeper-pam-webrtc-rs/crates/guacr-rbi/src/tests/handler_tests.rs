use crate::handler::{RbiConfig, RbiHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_rbi_handler_new() {
    let handler = RbiHandler::with_defaults();
    assert_eq!(<_ as ProtocolHandler>::name(&handler), "http");
}

#[test]
fn test_rbi_config() {
    let config = RbiConfig::default();
    assert_eq!(config.default_width, 1920);
    assert_eq!(config.default_height, 1080);
}

#[tokio::test]
async fn test_rbi_handler_health_check() {
    let handler = RbiHandler::with_defaults();
    let health = handler.health_check().await;
    assert!(health.is_ok());
}
