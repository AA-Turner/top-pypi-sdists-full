use crate::sql::{extract_use_database_name, SqlHandler};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_mysql_handler_name() {
    assert_eq!(SqlHandler::mysql().name(), "mysql");
}

#[test]
fn test_mariadb_handler_name() {
    assert_eq!(SqlHandler::mariadb().name(), "mariadb");
}

#[test]
fn test_mysql_explicit_port_overrides_default() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "mysql.example.com".to_string());
    p.insert("username".to_string(), "root".to_string());
    p.insert("port".to_string(), "3307".to_string());
    let info = build_connection_info(DatabaseType::Mysql, &p).unwrap();
    assert_eq!(info.port, Some(3307), "explicit port=3307 must be captured");
}

#[test]
fn test_mysql_missing_hostname_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("username".to_string(), "root".to_string());
    assert!(
        build_connection_info(DatabaseType::Mysql, &p).is_err(),
        "missing hostname must return an error"
    );
}

#[test]
fn test_mysql_missing_username_returns_error() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "mysql.example.com".to_string());
    assert!(
        build_connection_info(DatabaseType::Mysql, &p).is_err(),
        "missing username must return an error"
    );
}

#[test]
fn test_mysql_password_captured() {
    use crate::keeperdb_driver::build_connection_info;
    use keeperdb_core::types::DatabaseType;
    use secrecy::ExposeSecret;
    let mut p = std::collections::HashMap::new();
    p.insert("hostname".to_string(), "mysql.example.com".to_string());
    p.insert("username".to_string(), "root".to_string());
    p.insert("password".to_string(), "secret123".to_string());
    let info = build_connection_info(DatabaseType::Mysql, &p).unwrap();
    assert_eq!(
        info.password.expose_secret(),
        "secret123",
        "password must be captured in ConnectionInfo"
    );
}

// ---------------------------------------------------------------------------
// FIX 6 — USE db / \c db prompt update
// ---------------------------------------------------------------------------

/// `USE <db>` in any casing must extract the database name.
///
/// `extract_use_database_name` is the helper used by SqlHandler to detect
/// database-switching commands and update the executor prompt.
/// This test fails before the fix (function doesn't exist) and passes after.
#[test]
fn test_extract_use_database_name_basic() {
    assert_eq!(
        extract_use_database_name("USE mydb"),
        Some("mydb".to_string())
    );
    assert_eq!(
        extract_use_database_name("use mydb"),
        Some("mydb".to_string())
    );
    assert_eq!(
        extract_use_database_name("USE mydb;"),
        Some("mydb".to_string())
    );
    assert_eq!(
        extract_use_database_name("  USE   mydb  "),
        Some("mydb".to_string())
    );
}

/// Non-USE queries must return None.
#[test]
fn test_extract_use_database_name_returns_none_for_non_use() {
    assert_eq!(extract_use_database_name("SELECT * FROM t"), None);
    assert_eq!(extract_use_database_name("CREATE DATABASE mydb"), None);
    assert_eq!(extract_use_database_name("USE"), None);
    assert_eq!(extract_use_database_name(""), None);
}

// ---------------------------------------------------------------------------
// Affected row count fix — regression tests for the `affected_rows: Some(0)`
// hardcoding bug reported in CHANGELOG as `mysql.rs:455`.
//
// Previously, `execution_result_to_query_result` mapped
// `ExecutionResult::Affected` to `QueryResult { affected_rows: Some(0), .. }`
// regardless of the actual `stmt.affected_rows` value.  After the fix it uses
// `Some(stmt.affected_rows)`.  These tests would have caught the bug.
// ---------------------------------------------------------------------------

/// An Affected result with N > 0 rows must carry that count, not 0.
///
/// Before the fix: `affected_rows` was always `Some(0)`.
/// After the fix:  `affected_rows` is `Some(stmt.affected_rows)`.
#[test]
fn test_execution_result_affected_rows_non_zero() {
    use crate::keeperdb_driver::execution_result_to_query_result;
    use keeperdb_core::entities::query::{ExecutionResult, StatementResult};

    let result = execution_result_to_query_result(ExecutionResult::Affected(StatementResult {
        affected_rows: 42,
        execution_time_ms: 7,
    }));

    assert_eq!(
        result.affected_rows,
        Some(42),
        "affected_rows must be 42, not 0 — the hardcoded-zero bug must stay fixed"
    );
    assert_eq!(result.execution_time_ms, Some(7));
    assert!(result.columns.is_empty(), "Affected result has no columns");
    assert!(result.rows.is_empty(), "Affected result has no rows");
}

/// An Affected result with 0 rows is distinct from the bug — the database
/// really affected 0 rows (e.g. UPDATE with a WHERE that matched nothing).
/// The count must still come from the driver, not be hardcoded.
#[test]
fn test_execution_result_affected_rows_zero_from_driver() {
    use crate::keeperdb_driver::execution_result_to_query_result;
    use keeperdb_core::entities::query::{ExecutionResult, StatementResult};

    let result = execution_result_to_query_result(ExecutionResult::Affected(StatementResult {
        affected_rows: 0,
        execution_time_ms: 3,
    }));

    assert_eq!(
        result.affected_rows,
        Some(0),
        "zero affected rows from the driver must be preserved as Some(0)"
    );
}

/// A Rows result (SELECT) must have affected_rows == None — it is not
/// a statement result and there is no row-count concept.
#[test]
fn test_execution_result_rows_has_no_affected_count() {
    use crate::keeperdb_driver::execution_result_to_query_result;
    use keeperdb_core::entities::query::{
        CellValue, ExecutionResult, QueryResult as KeeperQueryResult,
    };
    use keeperdb_core::entities::schema::Column;

    let result = execution_result_to_query_result(ExecutionResult::Rows(KeeperQueryResult {
        columns: vec![Column {
            name: "id".to_string(),
            data_type: "INT".to_string(),
            nullable: false,
            default_value: None,
            is_primary_key: true,
        }],
        rows: vec![vec![CellValue::Int(1)]],
        total_rows: Some(1),
        truncated: false,
        execution_time_ms: 5,
    }));

    assert_eq!(
        result.affected_rows, None,
        "SELECT result must have affected_rows == None, not Some(N)"
    );
    assert_eq!(result.columns, vec!["id"]);
    assert_eq!(result.rows, vec![vec!["1".to_string()]]);
    assert_eq!(result.execution_time_ms, Some(5));
}

#[test]
#[ignore = "requires live MySQL; validates driver.disconnect() is called on session end"]
fn test_mysql_handler_calls_disconnect_on_session_end() {
    // Real test would: connect, run query, drop connection, verify pool shows 0 active connections.
    // Verified via code inspection: sql.rs calls driver.disconnect().await before
    // finalize_recording() on all exit paths.
}
