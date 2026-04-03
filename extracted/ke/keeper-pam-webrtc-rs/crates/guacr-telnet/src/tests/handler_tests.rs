use guacr_handlers::{HealthStatus, ProtocolHandler};

use crate::handler::TelnetHandler;

#[test]
fn test_telnet_handler_new() {
    let handler = TelnetHandler::with_defaults();
    assert_eq!(<TelnetHandler as ProtocolHandler>::name(&handler), "telnet");
}

#[tokio::test]
async fn test_telnet_handler_health() {
    let handler = TelnetHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[tokio::test]
async fn test_telnet_handler_stats() {
    let handler = TelnetHandler::with_defaults();
    let stats = handler.stats().await.unwrap();
    assert_eq!(stats.total_connections, 0);
}
