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
    // NotConfigured deliberately fails OPEN (allow + warn): the vault UI does not yet
    // expose a host-key field, so rejecting would break every existing PAM record that
    // has no fingerprint. See the "WHEN TO FLIP THIS" note on HostKeyResult::is_allowed
    // — flip this expectation to `!is_allowed` once vault exposes the field and records
    // are migrated.
    assert!(result.is_allowed(&config));
    // The advisory lives in security_warning() (an allowed-but-unverified connection),
    // NOT error_message() (which is reserved for denied connections).
    assert!(result.security_warning().is_some());
    assert!(result.error_message().is_none());
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
    // [host]:port entries must be preserved as-is — stripping the port would
    // cause a key registered for port 2222 to match any port on that host.
    assert_eq!(
        normalize_hostname("[example.com]:2222"),
        "[example.com]:2222"
    );
    assert_eq!(normalize_hostname("[192.168.1.1]:22"), "[192.168.1.1]:22");
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

/// When no verification is configured, the connection is allowed (fail-open, see
/// HostKeyResult::is_allowed) but a security warning must be available so callers can
/// log that MITM protection is inactive. No error_message() — that is reserved for
/// denied connections.
#[test]
fn test_not_configured_provides_security_warning() {
    let result = HostKeyResult::NotConfigured;
    let config = HostKeyConfig::default();
    assert!(
        result.is_allowed(&config),
        "NotConfigured deliberately fails open (allow + warn) until vault exposes a host-key field"
    );
    assert!(
        result.security_warning().is_some(),
        "NotConfigured must provide a security warning so operators see MITM protection is off"
    );
    assert!(
        result.error_message().is_none(),
        "NotConfigured is allowed, so it has no denial error_message — the advisory is a warning"
    );
}

/// Verified, Skipped, and Mismatch states must not emit a security warning
/// (they have their own appropriate log paths).
#[test]
fn test_other_states_no_spurious_warning() {
    assert!(HostKeyResult::Verified.security_warning().is_none());
    assert!(HostKeyResult::Skipped.security_warning().is_none());
    let mismatch = HostKeyResult::Mismatch {
        expected: "aaa".to_string(),
        actual: "bbb".to_string(),
    };
    assert!(mismatch.security_warning().is_none());
}

/// A known_hosts entry for [host]:2222 must NOT match a connection to host:22.
/// The current normalize_hostname strips the port, causing cross-port matches.
#[test]
fn test_known_hosts_port_specific_entry_does_not_match_other_ports() {
    use crate::host_key::{generate_hostname_variants, normalize_hostname};

    // normalize_hostname("[example.com]:2222") must preserve port info
    // so port-specific entries are stored distinctly from default-port entries.
    let normalized = normalize_hostname("[example.com]:2222");
    assert_eq!(
        normalized, "[example.com]:2222",
        "normalize_hostname must preserve [host]:port format; got: {normalized:?}"
    );

    // Variants for port 22 must NOT include [example.com]:2222
    let variants_22 = generate_hostname_variants("example.com", 22);
    assert!(
        !variants_22.contains(&"[example.com]:2222".to_string()),
        "port-22 variants must not include the :2222 form; got: {variants_22:?}"
    );

    // Variants for port 2222 must include [example.com]:2222
    let variants_2222 = generate_hostname_variants("example.com", 2222);
    assert!(
        variants_2222.contains(&"[example.com]:2222".to_string()),
        "port-2222 variants must include [example.com]:2222; got: {variants_2222:?}"
    );
}
