use std::collections::HashMap;

use guacr_handlers::{HealthStatus, ProtocolHandler};

use crate::handler::{VncConfig, VncHandler, VncSettings};

#[test]
fn test_vnc_handler_new() {
    let handler = VncHandler::with_defaults();
    assert_eq!(<VncHandler as ProtocolHandler>::name(&handler), "vnc");
}

#[test]
fn test_vnc_config_defaults() {
    let config = VncConfig::default();
    assert_eq!(config.default_port, 5900);
    assert_eq!(config.default_width, 1920);
    assert_eq!(config.default_height, 1080);
}

#[tokio::test]
async fn test_vnc_handler_health() {
    let handler = VncHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[test]
fn test_vnc_settings_from_params() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "server.example.com".to_string());

    let defaults = VncConfig::default();
    let settings = VncSettings::from_params(&params, &defaults).unwrap();

    assert_eq!(settings.hostname, "server.example.com");
    assert_eq!(settings.port, 5900);
    assert_eq!(settings.width, 1920);
}
