//! Tests proving that gateway private keys and other credentials never appear
//! in log output, whether logged via the `ConnectAsSettings` struct `Debug`
//! impl or via the raw `serde_json::Value` payload received off the wire.

use crate::channel::core::{
    redact_settings_map, redact_settings_value, redact_string_setting, ConnectAsSettings,
};
use std::collections::HashMap;

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

/// Build a `protocol_settings` map shaped like the one logged by the tube
/// verbose-log sites (credential-injected DB connection with ConnectAs).
fn realistic_protocol_settings() -> HashMap<String, serde_json::Value> {
    let mut map = HashMap::new();
    map.insert(
        "db_params".to_string(),
        serde_json::json!({
            "username": "EC2AMAZ-5UQCG0T\\kdbtest",
            "password": "SuperSecret!DbPassword",
            "hostname": "craig-sql-nlb.example.internal",
            "port": "1433",
            "tls_ca_pem": FAKE_PEM
        }),
    );
    map.insert(
        "connect_as_settings".to_string(),
        serde_json::json!({
            "allow_supply_user": true,
            "gateway_private_key": FAKE_PEM
        }),
    );
    map.insert("protocol".to_string(), serde_json::json!("sqlserver"));
    map
}

#[test]
fn redact_settings_map_masks_secrets_and_keeps_diagnostics() {
    let rendered = format!("{:?}", redact_settings_map(&realistic_protocol_settings()));

    assert!(
        !rendered.contains("SuperSecret!DbPassword"),
        "leaked db password: {rendered}"
    );
    assert!(
        !rendered.contains("SECRETKEYMATERIAL0000"),
        "leaked private key material: {rendered}"
    );
    assert!(
        !rendered.contains("BEGIN PRIVATE KEY"),
        "leaked PEM header: {rendered}"
    );
    // Redacted keys stay present so config-shape problems remain diagnosable.
    assert!(
        rendered.contains("password") && rendered.contains("[redacted]"),
        "masked keys should remain visible with a marker: {rendered}"
    );
    // Non-secret diagnostic fields survive untouched.
    for kept in ["kdbtest", "craig-sql-nlb", "1433", "sqlserver", "hostname"] {
        assert!(
            rendered.contains(kept),
            "dropped non-secret diagnostic field {kept}: {rendered}"
        );
    }
}

#[test]
fn redact_settings_map_truncates_ca_pem() {
    let rendered = format!("{:?}", redact_settings_map(&realistic_protocol_settings()));

    assert!(
        !rendered.contains("SECRETKEYMATERIAL0000"),
        "leaked CA PEM contents: {rendered}"
    );
    let marker = format!("[pem: {} bytes]", FAKE_PEM.len());
    assert!(
        rendered.contains(&marker),
        "tls_ca_pem should be summarized as {marker}: {rendered}"
    );
}

#[test]
fn redact_settings_value_masks_public_keys_case_insensitively() {
    let value = serde_json::json!({
        "public-key": "ssh-rsa AAAAB3Nza...",
        "PublicKey": "ssh-ed25519 AAAAC3...",
        "Password": "hunter2",
        "GATEWAY_PRIVATE_KEY": FAKE_PEM,
        "username": "kdbtest"
    });

    let rendered = format!("{:?}", redact_settings_value(&value));

    for leaked in ["ssh-rsa", "ssh-ed25519", "hunter2", "SECRETKEYMATERIAL0000"] {
        assert!(
            !rendered.contains(leaked),
            "case-insensitive masking failed for {leaked}: {rendered}"
        );
    }
    assert!(
        rendered.contains("kdbtest"),
        "dropped non-secret key: {rendered}"
    );
}

#[test]
fn redact_string_setting_covers_guacd_params() {
    // The String→String guacd-params path must apply the same shared allowlist.
    for masked in [
        "password",
        "privatekey",
        "private_key",
        "gateway_private_key",
        "passphrase",
        "public-key",
        "publickey",
    ] {
        assert_eq!(
            redact_string_setting(masked, "secret-value"),
            "[redacted]",
            "guacd param {masked} was not masked"
        );
    }
    assert_eq!(
        redact_string_setting("tls_ca_cert", FAKE_PEM),
        format!("[pem: {} bytes]", FAKE_PEM.len())
    );
    assert_eq!(
        redact_string_setting("hostname", "db.example.internal"),
        "db.example.internal"
    );
    assert_eq!(redact_string_setting("port", "5432"), "5432");
}

#[test]
fn redaction_covers_guacd_accepted_key_variants() {
    // guacr-guacd normalizes connect-param keys (hyphens/underscores stripped,
    // lowercased) before lookup, so all of these spellings functionally carry
    // credentials and must be masked despite not matching any needle exactly.
    for masked in [
        "private-key",      // guacd canonical arg name
        "privateKey",       // camelCase from JSON payloads
        "sftp-private-key", // guacd sftp arg
        "sftp_private_key", // handler param spelling
        "sftp_private_key_passphrase",
        "private_key_passphrase",
        "proxy-password",
        "PASSWORD",
    ] {
        assert_eq!(
            redact_string_setting(masked, "secret-value"),
            "[redacted]",
            "variant key {masked} was not masked"
        );
    }
    // Non-secret guacd args must still pass through.
    for kept in ["hostname", "port", "color-scheme", "username", "protocol"] {
        assert_eq!(
            redact_string_setting(kept, "value"),
            "value",
            "non-secret key {kept} was masked"
        );
    }
}

#[test]
fn redact_settings_map_masks_variant_keys_by_value() {
    // Direct value assertions (not Debug-substring) on a map with variant keys.
    let mut map = HashMap::new();
    map.insert("private-key".to_string(), serde_json::json!(FAKE_PEM));
    map.insert(
        "sftp_private_key_passphrase".to_string(),
        serde_json::json!("open sesame"),
    );
    map.insert("hostname".to_string(), serde_json::json!("db.internal"));

    let redacted = redact_settings_map(&map);

    assert_eq!(redacted["private-key"], serde_json::json!("[redacted]"));
    assert_eq!(
        redacted["sftp_private_key_passphrase"],
        serde_json::json!("[redacted]")
    );
    assert_eq!(redacted["hostname"], serde_json::json!("db.internal"));
}
