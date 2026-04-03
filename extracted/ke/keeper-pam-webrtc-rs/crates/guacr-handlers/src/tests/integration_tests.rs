use crate::integration::handle_guacd_with_handlers;
use crate::mock::MockProtocolHandler;
use crate::registry::ProtocolHandlerRegistry;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

#[tokio::test]
async fn test_handle_guacd_unsupported_protocol() {
    let registry = Arc::new(ProtocolHandlerRegistry::new());
    // Don't register any handlers

    let (to_webrtc, _webrtc_rx) = mpsc::channel(10);
    let (_webrtc_tx, from_webrtc) = mpsc::channel(10);

    let result = handle_guacd_with_handlers(
        "ssh".to_string(),
        HashMap::new(),
        registry,
        to_webrtc,
        from_webrtc,
    )
    .await;

    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("not supported"));
}

#[test]
fn test_registry_lookup() {
    let registry = Arc::new(ProtocolHandlerRegistry::new());
    registry.register(MockProtocolHandler::new("ssh"));
    registry.register(MockProtocolHandler::new("rdp"));

    assert!(registry.has("ssh"));
    assert!(registry.has("rdp"));
    assert!(!registry.has("vnc"));

    let ssh_handler = registry.get("ssh");
    assert!(ssh_handler.is_some());
    assert_eq!(ssh_handler.unwrap().name(), "ssh");
}
