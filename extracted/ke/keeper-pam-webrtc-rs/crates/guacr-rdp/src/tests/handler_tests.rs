use crate::handler::{RdpConfig, RdpHandler, RdpSettings};
use guacr_handlers::{HealthStatus, ProtocolHandler};
use std::collections::HashMap;

#[test]
fn test_rdp_handler_new() {
    let handler = RdpHandler::with_defaults();
    assert_eq!(<RdpHandler as ProtocolHandler>::name(&handler), "rdp");
}

#[test]
fn test_rdp_config_defaults() {
    let config = RdpConfig::default();
    assert_eq!(config.default_port, 3389);
    assert_eq!(config.default_width, 1920);
    assert_eq!(config.default_height, 1080);
    assert_eq!(config.security_mode, "nla");
}

#[tokio::test]
async fn test_rdp_handler_health() {
    let handler = RdpHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[tokio::test]
async fn test_rdp_handler_stats() {
    let handler = RdpHandler::with_defaults();
    let stats = handler.stats().await.unwrap();
    assert_eq!(stats.total_connections, 0);
}

#[test]
fn test_rdp_settings_from_params() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "server.example.com".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());

    let defaults = RdpConfig::default();
    let settings = RdpSettings::from_params(&params, &defaults).unwrap();

    assert_eq!(settings.hostname, "server.example.com");
    assert_eq!(settings.port, 3389);
    assert_eq!(settings.width, 1920);
}
