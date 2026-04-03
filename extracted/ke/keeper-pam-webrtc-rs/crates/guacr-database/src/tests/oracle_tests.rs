use crate::oracle::{
    oracle_client_available, oracle_client_path, simulate_oracle_query, OracleConfig,
    OracleHandler, OCI_LIB_DIR_ENV, ORACLE_HOME_ENV,
};
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

#[test]
fn test_simulate_oracle_query() {
    let result = simulate_oracle_query("SELECT SYSDATE FROM DUAL");
    assert!(result.is_ok());
    let output = result.unwrap();
    assert!(
        output.contains("row selected") || output.contains("-"),
        "Expected date output: {}",
        output
    );
}

#[test]
fn test_oracle_client_check() {
    // This will vary based on environment
    let available = oracle_client_available();
    let path = oracle_client_path();

    if available {
        assert!(path.is_some());
    }
}

#[test]
fn test_env_var_names() {
    assert_eq!(ORACLE_HOME_ENV, "ORACLE_HOME");
    assert_eq!(OCI_LIB_DIR_ENV, "OCI_LIB_DIR");
}
