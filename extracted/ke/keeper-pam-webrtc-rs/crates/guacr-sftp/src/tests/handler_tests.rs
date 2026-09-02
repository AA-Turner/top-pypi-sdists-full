use crate::handler::{log_sftp_host_key_result, SftpConfig, SftpHandler};
use guacr_handlers::{HostKeyResult, ProtocolHandler};

#[test]
fn test_sftp_handler_new() {
    let handler = SftpHandler::with_defaults();
    assert_eq!(<_ as ProtocolHandler>::name(&handler), "sftp");
}

#[test]
fn test_sftp_security_defaults() {
    let config = SftpConfig::default();
    assert!(config.chroot_to_home); // Security
    assert!(!config.allow_delete); // Security: No delete by default
}

#[test]
fn test_sftp_port() {
    let config = SftpConfig::default();
    assert_eq!(config.default_port, 22); // Same as SSH
}

/// Path traversal via `..` components must be caught by validate_path even
/// without canonicalize() touching the local filesystem. The old implementation
/// called std::fs::canonicalize which resolves paths on the GATEWAY's local
/// filesystem, not the SFTP server's — making the chroot check unreliable.
#[test]
fn test_sftp_validate_path_rejects_dotdot_traversal() {
    use crate::handler::{SftpConfig, SftpHandler};
    use std::path::Path;

    let config = SftpConfig {
        chroot_to_home: true,
        ..Default::default()
    };
    let handler = SftpHandler::new(config);
    let home = Path::new("/home/user");

    // Path with .. that would escape the home directory
    let traversal = Path::new("/home/user/../../../etc/passwd");
    let result = handler.test_validate_path_lexical(traversal, home);
    assert!(
        result.is_err(),
        "path traversal via .. must be rejected; got: {:?}",
        result
    );
}

#[test]
fn test_sftp_validate_path_allows_subdir() {
    use crate::handler::{SftpConfig, SftpHandler};
    use std::path::Path;

    let config = SftpConfig {
        chroot_to_home: true,
        ..Default::default()
    };
    let handler = SftpHandler::new(config);
    let home = Path::new("/home/user");

    // Legitimate subdirectory must be allowed
    let valid = Path::new("/home/user/documents/file.txt");
    let result = handler.test_validate_path_lexical(valid, home);
    assert!(
        result.is_ok(),
        "valid subdir must be allowed; got: {:?}",
        result
    );
}

/// When no host key verification is configured, the SFTP handler must emit a
/// warn-level log so operators can see that MITM protection is inactive.
///
/// The bug: the current `log_sftp_host_key_result` uses `debug!` for
/// `NotConfigured`, which is invisible in production log levels. SSH does this
/// correctly via `security_warning()` + `warn!`. SFTP must match.
///
/// This test fails until `log_sftp_host_key_result` is fixed to call
/// `security_warning()` and log the result at `warn!`.
#[test]
fn test_sftp_not_configured_logs_at_warn_level() {
    use log::Level;

    testing_logger::setup();
    log_sftp_host_key_result(&HostKeyResult::NotConfigured, "example.com", 22);
    testing_logger::validate(|captured| {
        let warn_logs: Vec<_> = captured.iter().filter(|e| e.level == Level::Warn).collect();
        assert!(
            !warn_logs.is_empty(),
            "NotConfigured must emit at least one warn-level log; got levels: {:?}",
            captured.iter().map(|e| e.level).collect::<Vec<_>>()
        );
        let has_mitm_warning = warn_logs
            .iter()
            .any(|e| e.body.contains("MITM") || e.body.contains("verification"));
        assert!(
            has_mitm_warning,
            "The warn log must mention MITM or verification; got: {:?}",
            warn_logs.iter().map(|e| &e.body).collect::<Vec<_>>()
        );
    });
}

/// Verified, Skipped, UnknownHost, and Mismatch states have their own correct
/// log levels — verify that none of them accidentally emit at debug level where
/// operators might miss them.
#[test]
fn test_sftp_log_levels_for_non_configured_states() {
    use log::Level;

    // Skipped must warn
    testing_logger::setup();
    log_sftp_host_key_result(&HostKeyResult::Skipped, "example.com", 22);
    testing_logger::validate(|captured| {
        assert!(
            captured.iter().any(|e| e.level == Level::Warn),
            "Skipped must log at warn; got: {:?}",
            captured.iter().map(|e| e.level).collect::<Vec<_>>()
        );
    });

    // UnknownHost must warn
    testing_logger::setup();
    log_sftp_host_key_result(&HostKeyResult::UnknownHost, "example.com", 22);
    testing_logger::validate(|captured| {
        assert!(
            captured.iter().any(|e| e.level == Level::Warn),
            "UnknownHost must log at warn; got: {:?}",
            captured.iter().map(|e| e.level).collect::<Vec<_>>()
        );
    });

    // Mismatch must error
    testing_logger::setup();
    log_sftp_host_key_result(
        &HostKeyResult::Mismatch {
            expected: "SHA256:aaa".to_string(),
            actual: "SHA256:bbb".to_string(),
        },
        "example.com",
        22,
    );
    testing_logger::validate(|captured| {
        assert!(
            captured.iter().any(|e| e.level == Level::Error),
            "Mismatch must log at error; got: {:?}",
            captured.iter().map(|e| e.level).collect::<Vec<_>>()
        );
    });
}
