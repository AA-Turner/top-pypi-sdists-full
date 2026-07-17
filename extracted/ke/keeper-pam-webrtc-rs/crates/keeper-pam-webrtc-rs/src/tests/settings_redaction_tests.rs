//! Tests proving that gateway private keys and other credentials never appear
//! in log output, whether logged via the `ConnectAsSettings` struct `Debug`
//! impl or via the raw `serde_json::Value` payload received off the wire.

use crate::channel::core::{redact_settings_value, ConnectAsSettings};

const FAKE_PEM: &str =
    "-----BEGIN PRIVATE KEY-----\nSECRETKEYMATERIAL0000\n-----END PRIVATE KEY-----\n";

#[test]
fn connect_as_settings_debug_redacts_private_key() {
    let settings = ConnectAsSettings {
        allow_supply_user: true,
        allow_supply_host: false,
        gateway_private_key: Some(FAKE_PEM.to_string()),
    };

    let rendered = format!("{settings:?}");

    assert!(
        !rendered.contains("SECRETKEYMATERIAL0000"),
        "Debug output leaked private key material: {rendered}"
    );
    assert!(
        !rendered.contains("BEGIN PRIVATE KEY"),
        "Debug output leaked PEM header: {rendered}"
    );
    assert!(
        rendered.contains("[redacted]"),
        "Debug output should mark the key as redacted: {rendered}"
    );
    // Non-secret fields must remain visible for diagnostics.
    assert!(
        rendered.contains("allow_supply_user"),
        "Debug output dropped non-secret fields: {rendered}"
    );
}

#[test]
fn connect_as_settings_debug_omits_absent_key() {
    let settings = ConnectAsSettings {
        allow_supply_user: false,
        allow_supply_host: true,
        gateway_private_key: None,
    };

    let rendered = format!("{settings:?}");
    assert!(
        rendered.contains("None"),
        "Absent key should render as None: {rendered}"
    );
}

#[test]
fn redact_settings_value_strips_private_key() {
    // Mirrors the real payload shape from the deserialization-failure log line.
    let value = serde_json::json!({
        "allow_supply_user": true,
        "allow_supply_host": "",
        "gateway_private_key": FAKE_PEM,
        "nonce": "r/IJqaiC8PNsUL7m3+VUng=="
    });

    let rendered = format!("{:?}", redact_settings_value(&value));

    assert!(
        !rendered.contains("SECRETKEYMATERIAL0000"),
        "Redacted value leaked private key material: {rendered}"
    );
    assert!(
        !rendered.contains("BEGIN PRIVATE KEY"),
        "Redacted value leaked PEM header: {rendered}"
    );
    // Structure and non-secret keys stay intact so the log remains useful.
    assert!(
        rendered.contains("allow_supply_user"),
        "Redaction dropped non-secret keys: {rendered}"
    );
    assert!(
        rendered.contains("allow_supply_host"),
        "Redaction dropped non-secret keys: {rendered}"
    );
}

#[test]
fn redact_settings_value_redacts_nested_credentials() {
    let value = serde_json::json!({
        "outer": {
            "password": "hunter2",
            "passphrase": "correct horse",
            "keep": "visible"
        }
    });

    let rendered = format!("{:?}", redact_settings_value(&value));

    assert!(
        !rendered.contains("hunter2"),
        "leaked nested password: {rendered}"
    );
    assert!(
        !rendered.contains("correct horse"),
        "leaked nested passphrase: {rendered}"
    );
    assert!(
        rendered.contains("visible"),
        "dropped non-secret nested key: {rendered}"
    );
}
