// Unit tests for HostKeyConfig, HostKeyResult, and HostKeyVerifier.
//
// These cover the SSH host key verification path that protects against MITM
// attacks. All tests are pure — no network I/O, no SSH server required.
//
// Gaps filled by this file (Phase 4):
//   - HostKeyConfig::from_params parameter parsing
//   - HostKeyConfig::has_verification() logic
//   - HostKeyResult::is_allowed() for all six variants
//   - HostKeyResult::security_warning() presence/absence
//   - HostKeyResult::error_message() presence/absence
//   - HostKeyVerifier::verify() with ignore_host_key=true (Skipped path)
//   - HostKeyVerifier::verify() with no configuration (NotConfigured path)
//   - HostKeyVerifier::verify() with a correct pinned fingerprint (Verified)
//   - HostKeyVerifier::verify() with a wrong pinned fingerprint (Mismatch)
//   - SshConnectParams display-size parsing from the "size" param

use guacr_handlers::{calculate_fingerprint, HostKeyConfig, HostKeyResult, HostKeyVerifier};
use std::collections::HashMap;

use crate::handler::SshConnectParams;

// ---------------------------------------------------------------------------
// HostKeyConfig::from_params — parameter parsing
// ---------------------------------------------------------------------------

/// Defaults: ignore_host_key=false, allow_unknown_hosts=false, no path or fingerprint.
#[test]
fn test_host_key_config_defaults_are_secure() {
    let params = HashMap::new();
    let cfg = HostKeyConfig::from_params(&params);

    assert!(
        !cfg.ignore_host_key,
        "ignore_host_key must default to false — MITM protection must be on"
    );
    assert!(
        cfg.known_hosts_path.is_none(),
        "known_hosts_path must be None when not set"
    );
    assert!(
        !cfg.allow_unknown_hosts,
        "allow_unknown_hosts must default to false"
    );
    assert!(
        cfg.host_key_fingerprint.is_none(),
        "host_key_fingerprint must be None when not set"
    );
}

/// ignore-host-key=true must set the ignore flag.
#[test]
fn test_host_key_config_ignore_flag_true() {
    let mut params = HashMap::new();
    params.insert("ignore-host-key".to_string(), "true".to_string());
    let cfg = HostKeyConfig::from_params(&params);
    assert!(
        cfg.ignore_host_key,
        "ignore-host-key=true must set ignore_host_key"
    );
}

/// ignore-host-key=1 (numeric form) must also set the ignore flag.
#[test]
fn test_host_key_config_ignore_flag_numeric() {
    let mut params = HashMap::new();
    params.insert("ignore-host-key".to_string(), "1".to_string());
    let cfg = HostKeyConfig::from_params(&params);
    assert!(
        cfg.ignore_host_key,
        "ignore-host-key=1 must set ignore_host_key (numeric form)"
    );
}

/// known-hosts path must be captured when present.
#[test]
fn test_host_key_config_known_hosts_path_captured() {
    let mut params = HashMap::new();
    params.insert(
        "known-hosts".to_string(),
        "/etc/ssh/known_hosts".to_string(),
    );
    let cfg = HostKeyConfig::from_params(&params);
    assert_eq!(
        cfg.known_hosts_path.as_deref(),
        Some("/etc/ssh/known_hosts"),
        "known-hosts path must be captured"
    );
}

/// allow-unknown-hosts=true must set the flag.
#[test]
fn test_host_key_config_allow_unknown_hosts_true() {
    let mut params = HashMap::new();
    params.insert("allow-unknown-hosts".to_string(), "true".to_string());
    let cfg = HostKeyConfig::from_params(&params);
    assert!(
        cfg.allow_unknown_hosts,
        "allow-unknown-hosts=true must set allow_unknown_hosts"
    );
}

/// host-key fingerprint must be captured when present.
#[test]
fn test_host_key_config_fingerprint_captured() {
    let mut params = HashMap::new();
    let fp = "SHA256:abc123def456".to_string();
    params.insert("host-key".to_string(), fp.clone());
    let cfg = HostKeyConfig::from_params(&params);
    assert_eq!(
        cfg.host_key_fingerprint.as_deref(),
        Some(fp.as_str()),
        "host-key param must be captured into host_key_fingerprint"
    );
}

// ---------------------------------------------------------------------------
// HostKeyConfig::has_verification() logic
// ---------------------------------------------------------------------------

/// No verification configured: has_verification must return false.
#[test]
fn test_host_key_config_has_verification_false_when_nothing_set() {
    let cfg = HostKeyConfig {
        ignore_host_key: false,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: None,
    };
    assert!(
        !cfg.has_verification(),
        "has_verification must be false when no path or fingerprint is configured"
    );
}

/// A pinned fingerprint alone is sufficient for has_verification to return true.
#[test]
fn test_host_key_config_has_verification_true_when_fingerprint_set() {
    let cfg = HostKeyConfig {
        ignore_host_key: false,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: Some("SHA256:abc".to_string()),
    };
    assert!(
        cfg.has_verification(),
        "has_verification must be true when fingerprint is configured"
    );
}

/// ignore_host_key=true overrides the fingerprint: has_verification must be false.
#[test]
fn test_host_key_config_has_verification_false_when_ignored() {
    let cfg = HostKeyConfig {
        ignore_host_key: true,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: Some("SHA256:abc".to_string()),
    };
    assert!(
        !cfg.has_verification(),
        "has_verification must be false when ignore_host_key=true even with fingerprint"
    );
}

// ---------------------------------------------------------------------------
// HostKeyResult::is_allowed() — connection allow/deny decisions
// ---------------------------------------------------------------------------

fn any_config() -> HostKeyConfig {
    HostKeyConfig {
        ignore_host_key: false,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: None,
    }
}

fn allow_unknown_config() -> HostKeyConfig {
    HostKeyConfig {
        allow_unknown_hosts: true,
        ..any_config()
    }
}

/// Verified key must always be allowed.
#[test]
fn test_host_key_result_verified_is_allowed() {
    assert!(
        HostKeyResult::Verified.is_allowed(&any_config()),
        "Verified result must always be allowed"
    );
}

/// Skipped (ignore-host-key=true) must always be allowed.
#[test]
fn test_host_key_result_skipped_is_allowed() {
    assert!(
        HostKeyResult::Skipped.is_allowed(&any_config()),
        "Skipped result must always be allowed"
    );
}

/// NotConfigured must be allowed (no fingerprint = TOFU / no verification; guacd parity).
#[test]
fn test_host_key_result_not_configured_is_allowed() {
    assert!(
        HostKeyResult::NotConfigured.is_allowed(&any_config()),
        "NotConfigured must be allowed — matches guacd/KCM TOFU behavior"
    );
}

/// Mismatch must NEVER be allowed regardless of config — this is the MITM case.
#[test]
fn test_host_key_result_mismatch_is_never_allowed() {
    let mismatch = HostKeyResult::Mismatch {
        expected: "SHA256:expected".to_string(),
        actual: "SHA256:actual".to_string(),
    };
    // Must be denied even with allow_unknown_hosts=true — mismatch is stronger than "unknown"
    assert!(
        !mismatch.is_allowed(&allow_unknown_config()),
        "Mismatch must never be allowed — MITM protection must reject mismatched fingerprints"
    );
}

/// UnknownHost with allow_unknown_hosts=false must be denied.
#[test]
fn test_host_key_result_unknown_host_denied_by_default() {
    assert!(
        !HostKeyResult::UnknownHost.is_allowed(&any_config()),
        "UnknownHost must be denied when allow_unknown_hosts=false"
    );
}

/// UnknownHost with allow_unknown_hosts=true must be allowed.
#[test]
fn test_host_key_result_unknown_host_allowed_when_flag_set() {
    assert!(
        HostKeyResult::UnknownHost.is_allowed(&allow_unknown_config()),
        "UnknownHost must be allowed when allow_unknown_hosts=true"
    );
}

// ---------------------------------------------------------------------------
// HostKeyResult::security_warning() and error_message()
// ---------------------------------------------------------------------------

/// NotConfigured must produce a security warning (no verification is active).
#[test]
fn test_host_key_result_not_configured_has_security_warning() {
    let warning = HostKeyResult::NotConfigured.security_warning();
    assert!(
        warning.is_some(),
        "NotConfigured must produce a security warning"
    );
    let msg = warning.unwrap();
    assert!(
        msg.contains("MITM") || msg.contains("verification"),
        "security warning must mention MITM or verification; got: {msg}"
    );
}

/// Verified has no security warning.
#[test]
fn test_host_key_result_verified_has_no_warning() {
    assert!(
        HostKeyResult::Verified.security_warning().is_none(),
        "Verified must produce no security warning"
    );
}

/// Mismatch must produce an error message containing fingerprint information.
#[test]
fn test_host_key_result_mismatch_has_error_message() {
    let mismatch = HostKeyResult::Mismatch {
        expected: "SHA256:expected-fp".to_string(),
        actual: "SHA256:actual-fp".to_string(),
    };
    let msg = mismatch.error_message();
    assert!(
        msg.is_some(),
        "Mismatch must produce an error message for the log"
    );
    let msg = msg.unwrap();
    assert!(
        msg.contains("expected-fp") && msg.contains("actual-fp"),
        "error message must contain both fingerprints; got: {msg}"
    );
}

/// NotConfigured::error_message returns None (it is allowed, just warned).
#[test]
fn test_host_key_result_not_configured_has_no_error_message() {
    assert!(
        HostKeyResult::NotConfigured.error_message().is_none(),
        "NotConfigured must not produce an error message (connection is allowed)"
    );
}

// ---------------------------------------------------------------------------
// HostKeyVerifier::verify() — no I/O, pure logic paths
// ---------------------------------------------------------------------------

/// With ignore_host_key=true the verifier must return Skipped regardless of key.
#[test]
fn test_host_key_verifier_ignores_when_flag_set() {
    let cfg = HostKeyConfig {
        ignore_host_key: true,
        ..any_config()
    };
    let verifier = HostKeyVerifier::new(cfg);
    let result = verifier.verify("example.com", 22, "ssh-ed25519", b"fake-key-bytes");
    assert_eq!(
        result,
        HostKeyResult::Skipped,
        "verify with ignore_host_key=true must return Skipped"
    );
}

/// With no configuration (no fingerprint, no known_hosts path) the verifier
/// must return NotConfigured — this allows the connection with a warning.
#[test]
fn test_host_key_verifier_returns_not_configured_when_nothing_set() {
    let cfg = HostKeyConfig {
        ignore_host_key: false,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: None,
    };
    let verifier = HostKeyVerifier::new(cfg);
    let result = verifier.verify("example.com", 22, "ssh-ed25519", b"some-key-bytes");
    assert_eq!(
        result,
        HostKeyResult::NotConfigured,
        "verify with no configuration must return NotConfigured"
    );
}

/// With a correct pinned fingerprint the verifier must return Verified.
///
/// We use `calculate_fingerprint` (exported from guacr-handlers) to compute
/// the expected fingerprint from the same key bytes, then supply it as the
/// pinned fingerprint. The verifier must match and return Verified.
#[test]
fn test_host_key_verifier_correct_fingerprint_returns_verified() {
    let key_data = b"test-key-data-for-fingerprint";
    // calculate_fingerprint returns the base64-encoded SHA-256 hash without padding.
    let expected_fp = calculate_fingerprint(key_data);

    let cfg = HostKeyConfig {
        ignore_host_key: false,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: Some(format!("SHA256:{}", expected_fp)),
    };
    let verifier = HostKeyVerifier::new(cfg);
    let result = verifier.verify("example.com", 22, "ssh-ed25519", key_data);
    assert_eq!(
        result,
        HostKeyResult::Verified,
        "correct pinned fingerprint must return Verified"
    );
}

/// With a wrong pinned fingerprint the verifier must return Mismatch.
#[test]
fn test_host_key_verifier_wrong_fingerprint_returns_mismatch() {
    let cfg = HostKeyConfig {
        ignore_host_key: false,
        known_hosts_path: None,
        allow_unknown_hosts: false,
        host_key_fingerprint: Some(
            "SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=".to_string(),
        ),
    };
    let verifier = HostKeyVerifier::new(cfg);
    // Use completely different key data — fingerprint will not match
    let result = verifier.verify(
        "example.com",
        22,
        "ssh-ed25519",
        b"completely-different-key",
    );
    assert!(
        matches!(result, HostKeyResult::Mismatch { .. }),
        "wrong fingerprint must return Mismatch, got {result:?}"
    );
}

// ---------------------------------------------------------------------------
// SshConnectParams::from_params — display size via "size" param
//
// parse_display_size reads "size" as "width,height,dpi" and divides by the
// fixed CHAR_WIDTH=9 / CHAR_HEIGHT=18 cell size to produce cols/rows.
// ---------------------------------------------------------------------------

/// When "size" is present, cols and rows reflect the pixel dimensions divided
/// by the character cell size.
#[test]
fn test_ssh_params_display_size_from_size_param() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "10.0.0.1".to_string());
    params.insert("username".to_string(), "alice".to_string());
    // No password, no private_key — credential-less params are OK (auth happens later)
    // "size" = 1440,900,96 → cols = 1440/9 = 160, rows = 900/18 = 50
    params.insert("size".to_string(), "1440,900,96".to_string());
    let result = SshConnectParams::from_params(&params, 22).unwrap();
    assert_eq!(
        result.cols, 160,
        "cols must be 1440/9 = 160 when size=1440,900,96"
    );
    assert_eq!(
        result.rows, 50,
        "rows must be 900/18 = 50 when size=1440,900,96"
    );
}

// When "size" is absent, cols and rows fall back to the defaults (80×24).
// ---------------------------------------------------------------------------
// Future behavior: NotConfigured must DENY (failing test, ignored until ready)
// ---------------------------------------------------------------------------

/// Proves that NotConfigured currently ALLOWS connections (fail-open).
///
/// This test asserts the DESIRED future behavior — deny when no host-key is
/// configured — which currently FAILS because the vault does not yet expose a
/// host-key field and existing PAM records have no fingerprint.
///
/// To flip:
///   1. Vault exposes host-key / known-hosts field and existing records are migrated.
///   2. Remove `#[ignore]` from this test.
///   3. Change `HostKeyResult::NotConfigured => true` to `false` in is_allowed().
///   4. This test will pass; existing tests that assert the old allow behavior
///      (test_host_key_result_not_configured_*) must be updated or removed.
///
/// See: host_key.rs is_allowed() comment at line 85.
#[test]
#[ignore = "vault does not yet expose host-key field; flip when PAM records are migrated"]
fn test_not_configured_must_deny_once_vault_exposes_host_key() {
    let config = HostKeyConfig::default();
    let result = HostKeyResult::NotConfigured;
    assert!(
        !result.is_allowed(&config),
        "NotConfigured must deny the connection once vault exposes host-key field. \
         Currently fail-open (returns true) — see is_allowed() comment."
    );
}

#[test]
fn test_ssh_params_display_size_defaults_when_size_absent() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "10.0.0.1".to_string());
    params.insert("username".to_string(), "alice".to_string());
    // No size param — must fall back to DEFAULT_COLS=80, DEFAULT_ROWS=24
    let result = SshConnectParams::from_params(&params, 22).unwrap();
    // parse_display_size default is 1024×768 → cols=max(1024/9,80)=113, rows=max(768/18,24)=42
    // The fallback logic clamps to at least DEFAULT_COLS×DEFAULT_ROWS.
    assert!(
        result.cols >= 80,
        "cols must be at least DEFAULT_COLS=80 when size is absent; got {}",
        result.cols
    );
    assert!(
        result.rows >= 24,
        "rows must be at least DEFAULT_ROWS=24 when size is absent; got {}",
        result.rows
    );
}
