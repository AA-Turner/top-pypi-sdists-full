use crate::handler::{RbiBackend, RbiConfig, RbiHandler};
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

/// RbiConfig::default() must use RbiBackend::Chrome.
///
/// ServoWithFallback was the old default but Servo is not implemented — it
/// returns an error immediately. Using it as the default would cause every
/// session started with a default config to fail before Chrome is ever tried.
#[test]
fn test_rbi_config_default_backend_is_chrome() {
    let config = RbiConfig::default();
    assert_eq!(
        config.backend,
        RbiBackend::Chrome,
        "default backend must be Chrome; ServoWithFallback is not implemented"
    );
}

#[tokio::test]
async fn test_rbi_handler_health_check() {
    let handler = RbiHandler::with_defaults();
    let health = handler.health_check().await;
    assert!(health.is_ok());
}
