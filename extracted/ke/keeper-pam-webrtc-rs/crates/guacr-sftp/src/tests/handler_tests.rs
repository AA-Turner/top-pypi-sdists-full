use crate::handler::{SftpConfig, SftpHandler};
use guacr_handlers::ProtocolHandler;

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
