use crate::host_key::{
    calculate_fingerprint, generate_hostname_variants, normalize_hostname, HostKeyConfig,
    HostKeyResult, HostKeyVerifier,
};
use std::collections::HashMap;

fn verifier_with_known_hosts(content: &str, allow_unknown_hosts: bool) -> HostKeyVerifier {
    let file = tempfile::NamedTempFile::new().unwrap();
    std::fs::write(file.path(), content).unwrap();
    HostKeyVerifier::new(HostKeyConfig {
        known_hosts_path: Some(file.path().to_string_lossy().into_owned()),
        allow_unknown_hosts,
        ..Default::default()
    })
}

fn hashed_host(host: &str) -> String {
    use base64::{engine::general_purpose::STANDARD, Engine};
    use hmac::{Hmac, Mac};
    let salt = b"fixed known_hosts test salt";
    let mut mac = Hmac::<sha1::Sha1>::new_from_slice(salt).unwrap();
    mac.update(host.as_bytes());
    format!(
        "|1|{}|{}",
        STANDARD.encode(salt),
        STANDARD.encode(mac.finalize().into_bytes())
    )
}

#[test]
fn padded_sha256_host_key_fingerprint_matches_same_key() {
    // Given an OpenSSH SHA256 fingerprint with its optional Base64 padding.
    let key = b"test-key";
    let pinned = format!("SHA256:{}=", calculate_fingerprint(key));
    let verifier = HostKeyVerifier::new(HostKeyConfig {
        host_key_fingerprint: Some(pinned),
        ..Default::default()
    });

    // When checking the matching server key, then padding does not invalidate the pin.
    assert_eq!(
        verifier.verify("example.com", 22, "ssh-ed25519", key),
        HostKeyResult::Verified
    );
}

#[test]
fn test_known_hosts_accepts_second_key_when_first_same_type_differs() {
    // Given two keys of the same type for the same host.
    let content = format!(
        "example.com ssh-ed25519 {}\nexample.com ssh-ed25519 {}\n",
        base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"old"),
        base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"current")
    );
    let verifier = verifier_with_known_hosts(&content, false);

    // When the server presents the second key, then it is verified.
    assert_eq!(
        verifier.verify("example.com", 22, "ssh-ed25519", b"current"),
        HostKeyResult::Verified
    );
}

#[test]
fn test_hashed_known_hosts_accepts_second_key_when_first_same_type_differs() {
    // Given two keys under the same hashed hostname.
    let host = hashed_host("example.com");
    let content = format!(
        "{host} ssh-ed25519 {}\n{host} ssh-ed25519 {}\n",
        base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"old"),
        base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"current")
    );
    let verifier = verifier_with_known_hosts(&content, false);

    // When the server presents the second key, then it is verified.
    assert_eq!(
        verifier.verify("example.com", 22, "ssh-ed25519", b"current"),
        HostKeyResult::Verified
    );
}

#[test]
fn test_revoked_key_denied_despite_matching_ordinary_entry() {
    // Given an ordinary entry followed by a revocation for the same host and key.
    let key = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"revoked");
    let verifier = verifier_with_known_hosts(
        &format!("example.com ssh-ed25519 {key}\n@revoked example.com ssh-ed25519 {key}\n"),
        true,
    );

    // When the revoked key is presented, then the connection is refused.
    let result = verifier.verify("example.com", 22, "ssh-ed25519", b"revoked");
    assert!(
        matches!(result, HostKeyResult::Mismatch { .. }),
        "{result:?}"
    );
    assert!(!result.is_allowed(&verifier.config));
}

#[test]
fn test_hashed_revoked_key_denied_despite_matching_ordinary_entry() {
    // Given a plain acceptance and a hashed revocation for the same host and key.
    let key = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"revoked");
    let verifier = verifier_with_known_hosts(
        &format!(
            "example.com ssh-ed25519 {key}\n@revoked {} ssh-ed25519 {key}\n",
            hashed_host("example.com")
        ),
        true,
    );

    // When the revoked key is presented, then the connection is refused.
    let result = verifier.verify("example.com", 22, "ssh-ed25519", b"revoked");
    assert!(
        matches!(result, HostKeyResult::Mismatch { .. }),
        "{result:?}"
    );
    assert!(!result.is_allowed(&verifier.config));
}

#[test]
fn test_plain_hostname_does_not_pin_nondefault_port() {
    // Given a key pinned only to the default SSH port.
    let key = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"key");
    let verifier = verifier_with_known_hosts(&format!("example.com ssh-ed25519 {key}\n"), false);

    // When connecting on a different port, then the host is unknown.
    assert_eq!(
        verifier.verify("example.com", 2222, "ssh-ed25519", b"key"),
        HostKeyResult::UnknownHost
    );
}

#[test]
fn test_hashed_hostname_matches_only_its_port() {
    // Given a hashed [host]:port entry.
    let key = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"key");
    let verifier = verifier_with_known_hosts(
        &format!("{} ssh-ed25519 {key}\n", hashed_host("[example.com]:2222")),
        false,
    );

    // When connecting on that port, then the hashed host pin is honored.
    assert_eq!(
        verifier.verify("example.com", 2222, "ssh-ed25519", b"key"),
        HostKeyResult::Verified
    );
}

#[test]
fn test_hashed_bare_hostname_does_not_pin_nondefault_port() {
    // Given a hashed bare hostname (the default SSH port).
    let key = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"key");
    let verifier = verifier_with_known_hosts(
        &format!("{} ssh-ed25519 {key}\n", hashed_host("example.com")),
        false,
    );

    // When connecting on another port, then that hashed pin does not match.
    assert_eq!(
        verifier.verify("example.com", 2222, "ssh-ed25519", b"key"),
        HostKeyResult::UnknownHost
    );
}

#[test]
fn test_revocation_overrides_matching_fingerprint_pin() {
    // Given an explicitly configured fingerprint and a revocation of its key.
    let key = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"revoked");
    let file = tempfile::NamedTempFile::new().unwrap();
    std::fs::write(
        file.path(),
        format!("@revoked example.com ssh-ed25519 {key}\n"),
    )
    .unwrap();
    let verifier = HostKeyVerifier::new(HostKeyConfig {
        known_hosts_path: Some(file.path().to_string_lossy().into_owned()),
        host_key_fingerprint: Some(calculate_fingerprint(b"revoked")),
        ..Default::default()
    });

    // When the revoked key is presented, then the pin cannot override the revocation.
    assert!(matches!(
        verifier.verify("example.com", 22, "ssh-ed25519", b"revoked"),
        HostKeyResult::Mismatch { .. }
    ));
}

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
