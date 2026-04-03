use guacr_handlers::{HealthStatus, ProtocolHandler};
use guacr_terminal::parse_key_instruction;

use crate::handler::SshHandler;

#[test]
fn test_ssh_handler_new() {
    let handler = SshHandler::with_defaults();
    assert_eq!(ProtocolHandler::name(&handler), "ssh");
}

#[tokio::test]
async fn test_ssh_handler_health() {
    let handler = SshHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[test]
fn test_parse_key_instruction() {
    // Full Guacamole instruction: "3.key,5.65293,1.1;" (Enter key pressed)
    let instruction = "3.key,5.65293,1.1;";
    let result = parse_key_instruction(instruction);

    assert!(result.is_some());
    let key_event = result.unwrap();
    assert_eq!(key_event.keysym, 65293);
    assert!(key_event.pressed);
}
