use guacr_handlers::ProtocolHandler;
use guacr_ssh::SshHandler;

#[test]
fn test_ssh_handler_creation() {
    let handler = SshHandler::with_defaults();
    assert_eq!(handler.name(), "ssh");
}

#[tokio::test]
async fn test_ssh_handler_health_check() {
    let handler = SshHandler::with_defaults();
    let health = handler.health_check().await;
    assert!(health.is_ok());
}
