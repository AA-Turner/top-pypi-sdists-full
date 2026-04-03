use crate::host_key::{
    calculate_fingerprint, generate_hostname_variants, normalize_hostname, HostKeyConfig,
    HostKeyResult, HostKeyVerifier,
};
use std::collections::HashMap;

#[test]
fn test_host_key_config_default() {
    let config = HostKeyConfig::default();
    assert!(!config.ignore_host_key);
    assert!(config.known_hosts_path.is_none());
    assert!(!config.allow_unknown_hosts);
    assert!(config.host_key_fingerprint.is_none());
}

#[test]
fn test_host_key_config_from_params() {
    let mut params = HashMap::new();
    params.insert("ignore-host-key".to_string(), "true".to_string());
    params.insert(
        "known-hosts".to_string(),
        "/path/to/known_hosts".to_string(),
    );
    params.insert("allow-unknown-hosts".to_string(), "true".to_string());
    params.insert("host-key".to_string(), "AAAA...".to_string());

    let config = HostKeyConfig::from_params(&params);
    assert!(config.ignore_host_key);
    assert_eq!(
        config.known_hosts_path,
        Some("/path/to/known_hosts".to_string())
    );
    assert!(config.allow_unknown_hosts);
    assert_eq!(config.host_key_fingerprint, Some("AAAA...".to_string()));
}

#[test]
fn test_verify_skipped() {
    let config = HostKeyConfig {
        ignore_host_key: true,
        ..Default::default()
    };
    let verifier = HostKeyVerifier::new(config.clone());

    let result = verifier.verify("example.com", 22, "ssh-ed25519", b"key_data");
    assert_eq!(result, HostKeyResult::Skipped);
    assert!(result.is_allowed(&config));
}

#[test]
fn test_verify_not_configured() {
    let config = HostKeyConfig::default();
    let verifier = HostKeyVerifier::new(config.clone());

    let result = verifier.verify("example.com", 22, "ssh-ed25519", b"key_data");
    assert_eq!(result, HostKeyResult::NotConfigured);
    assert!(result.is_allowed(&config));
}

#[test]
fn test_fingerprint_calculation() {
    let key_data = b"test_key_data";
    let fp = calculate_fingerprint(key_data);
    // Should be base64 SHA256 without trailing =
    assert!(!fp.contains('='));
    assert!(!fp.is_empty());
}

#[test]
fn test_hostname_normalization() {
    assert_eq!(normalize_hostname("example.com"), "example.com");
    assert_eq!(normalize_hostname("[example.com]:2222"), "example.com");
    assert_eq!(normalize_hostname("[192.168.1.1]:22"), "192.168.1.1");
}

#[test]
fn test_hostname_variants() {
    let variants = generate_hostname_variants("Example.COM", 22);
    assert!(variants.contains(&"Example.COM".to_string()));
    assert!(variants.contains(&"example.com".to_string()));
    assert!(!variants.iter().any(|v: &String| v.contains(":22")));

    let variants_nonstandard = generate_hostname_variants("Example.COM", 2222);
    assert!(variants_nonstandard.contains(&"[Example.COM]:2222".to_string()));
    assert!(variants_nonstandard.contains(&"[example.com]:2222".to_string()));
}

#[test]
fn test_result_error_messages() {
    let mismatch = HostKeyResult::Mismatch {
        expected: "SHA256:abc".to_string(),
        actual: "SHA256:xyz".to_string(),
    };
    assert!(mismatch.error_message().is_some());
    assert!(mismatch.error_message().unwrap().contains("MITM"));

    let unknown = HostKeyResult::UnknownHost;
    assert!(unknown.error_message().is_some());

    let verified = HostKeyResult::Verified;
    assert!(verified.error_message().is_none());
}

#[test]
fn test_pinned_fingerprint_verification() {
    let key_data = b"test_key_data_12345";
    let fingerprint = calculate_fingerprint(key_data);

    let config = HostKeyConfig {
        host_key_fingerprint: Some(fingerprint.clone()),
        ..Default::default()
    };
    let verifier = HostKeyVerifier::new(config.clone());

    // Should verify with matching fingerprint
    let result = verifier.verify("example.com", 22, "ssh-ed25519", key_data);
    assert_eq!(result, HostKeyResult::Verified);

    // Should fail with different key
    let result2 = verifier.verify("example.com", 22, "ssh-ed25519", b"different_key");
    assert!(matches!(result2, HostKeyResult::Mismatch { .. }));
}
