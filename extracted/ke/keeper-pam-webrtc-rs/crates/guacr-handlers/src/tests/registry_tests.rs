use crate::mock::MockProtocolHandler;
use crate::registry::ProtocolHandlerRegistry;
use std::sync::Arc;

#[test]
fn test_registry_new() {
    let registry = ProtocolHandlerRegistry::new();
    assert_eq!(registry.count(), 0);
    assert!(registry.list().is_empty());
}

#[test]
fn test_register_and_get() {
    let registry = ProtocolHandlerRegistry::new();
    let handler = MockProtocolHandler::new("ssh");

    registry.register(handler);

    assert_eq!(registry.count(), 1);
    assert!(registry.has("ssh"));
    assert!(registry.get("ssh").is_some());
    assert!(registry.get("rdp").is_none());
}

#[test]
fn test_list() {
    let registry = ProtocolHandlerRegistry::new();
    registry.register(MockProtocolHandler::new("ssh"));
    registry.register(MockProtocolHandler::new("rdp"));
    registry.register(MockProtocolHandler::new("vnc"));

    let mut protocols = registry.list();
    protocols.sort();

    assert_eq!(protocols, vec!["rdp", "ssh", "vnc"]);
}

#[test]
fn test_unregister() {
    let registry = ProtocolHandlerRegistry::new();
    registry.register(MockProtocolHandler::new("ssh"));

    assert_eq!(registry.count(), 1);
    assert!(registry.unregister("ssh"));
    assert_eq!(registry.count(), 0);
    assert!(!registry.unregister("ssh")); // Already removed
}

#[test]
fn test_concurrent_access() {
    let registry = Arc::new(ProtocolHandlerRegistry::new());
    registry.register(MockProtocolHandler::new("ssh"));

    // Simulate concurrent access
    let registry_clone = Arc::clone(&registry);
    let handle = std::thread::spawn(move || {
        for _ in 0..1000 {
            assert!(registry_clone.get("ssh").is_some());
        }
    });

    for _ in 0..1000 {
        assert!(registry.get("ssh").is_some());
    }

    handle.join().unwrap();
    assert_eq!(registry.count(), 1);
}
