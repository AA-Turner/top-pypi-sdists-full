use crate::create_default_registry;

#[test]
fn test_create_default_registry() {
    let registry = create_default_registry();
    // With default features (ssh, telnet), at least those two should be registered
    assert!(registry.count() >= 2);
}
