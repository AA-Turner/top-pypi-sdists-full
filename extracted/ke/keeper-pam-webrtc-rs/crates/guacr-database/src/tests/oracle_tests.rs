use crate::oracle::{OracleConfig, OracleHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_oracle_handler_new() {
    let handler = OracleHandler::with_defaults();
    assert_eq!(<OracleHandler as ProtocolHandler>::name(&handler), "oracle");
}

#[test]
fn test_oracle_config() {
    let config = OracleConfig::default();
    assert_eq!(config.default_port, 1521);
    assert_eq!(config.service_name, "ORCL");
    assert!(config.require_encryption);
}
