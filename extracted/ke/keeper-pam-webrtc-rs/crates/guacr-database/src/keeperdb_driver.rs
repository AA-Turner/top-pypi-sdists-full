use std::collections::HashMap;
use std::sync::Arc;

use keeperdb_core::entities::connection::{
    AdvancedOptions, ConnectionInfo, MssqlAdvancedOptions, SslMode,
};
use keeperdb_core::entities::query::{CellValue, ExecutionResult};
use keeperdb_core::error::KeeperDbError;
use keeperdb_core::traits::driver::DatabaseDriver;
use keeperdb_core::types::DatabaseType;
use secrecy::Secret;

use crate::{DatabaseError, Result};
use guacr_terminal::QueryResult;

/// Parse Guacamole connection params into a keeperdb ConnectionInfo.
pub fn build_connection_info(
    db_type: DatabaseType,
    params: &HashMap<String, String>,
) -> Result<ConnectionInfo> {
    let host = params
        .get("hostname")
        .ok_or_else(|| DatabaseError::ConnectionError("hostname required".to_string()))?
        .clone();
    let port = params.get("port").and_then(|p| p.parse().ok());
    let username = params
        .get("username")
        .ok_or_else(|| DatabaseError::ConnectionError("username required".to_string()))?
        .clone();
    let password = params.get("password").cloned().unwrap_or_default();
    let database = params.get("database").cloned().unwrap_or_default();

    let tls_verify = params.get("tls-verify").map(|s| s.as_str());
    let ssl_mode = match tls_verify {
        Some("require") => SslMode::Require,
        Some("false") | Some("none") | Some("disable") => SslMode::Disable,
        _ => SslMode::Prefer,
    };

    // For MSSQL: only set trust_server_certificate when the operator explicitly
    // requests it via the "trust-server-certificate=true" param.
    // Defaulting to trust=true bypasses TLS certificate validation entirely and
    // enables MITM attacks against SQL Server connections.
    let explicit_trust = params
        .get("trust-server-certificate")
        .map(|v| v == "true" || v == "1")
        .unwrap_or(false);

    let advanced_options = if db_type == DatabaseType::Mssql && explicit_trust {
        Some(AdvancedOptions::Mssql(MssqlAdvancedOptions {
            trust_server_certificate: Some(true),
            ..Default::default()
        }))
    } else {
        None
    };

    Ok(ConnectionInfo {
        database_type: db_type,
        host,
        port,
        username,
        password: Secret::new(password),
        database,
        ssl_mode,
        hosts: None,
        advanced_options,
    })
}

/// Connect to a SQL database and return a driver instance.
pub async fn connect(
    db_type: DatabaseType,
    params: &HashMap<String, String>,
) -> Result<Arc<dyn DatabaseDriver>> {
    // SQLite is file-based — hostname param is the file path; no username/password.
    let info = if db_type == DatabaseType::Sqlite {
        let db_path = params
            .get("hostname")
            .cloned()
            .filter(|s| !s.is_empty())
            .unwrap_or_else(|| ":memory:".to_string());
        ConnectionInfo {
            database_type: DatabaseType::Sqlite,
            host: db_path,
            port: None,
            username: String::new(),
            password: secrecy::Secret::new(String::new()),
            database: params.get("database").cloned().unwrap_or_default(),
            ssl_mode: SslMode::Disable,
            hosts: None,
            advanced_options: None,
        }
    } else {
        build_connection_info(db_type, params)?
    };

    // Connect via the unified registry (feature-gated set of built-in factories).
    // Unknown types surface as keeperdb's UnsupportedDatabase error.
    let registry = keeperdb_drivers::with_builtin_factories();
    let driver = registry
        .connect(&info)
        .await
        .map_err(|e| DatabaseError::ConnectionError(e.to_string()))?;
    Ok(Arc::from(driver))
}

/// Execute a SQL statement via a keeperdb driver and return our QueryResult.
pub async fn execute(driver: &dyn DatabaseDriver, sql: &str) -> Result<QueryResult> {
    match driver.execute(sql).await {
        Ok(result) => Ok(execution_result_to_query_result(result)),
        Err(KeeperDbError::ConfirmationRequired { operations, .. }) => {
            let ops: Vec<String> = operations.iter().map(|o| format!("{:?}", o)).collect();
            Err(DatabaseError::QueryError(format!(
                "Dangerous operation requires confirmation: {}. \
                 Prefix your query with CONFIRM: to execute.",
                ops.join(", ")
            )))
        }
        Err(e) => Err(DatabaseError::QueryError(e.to_string())),
    }
}

/// Convert a keeperdb ExecutionResult to our QueryResult type.
pub fn execution_result_to_query_result(result: ExecutionResult) -> QueryResult {
    match result {
        ExecutionResult::Rows(rows) => QueryResult {
            columns: rows.columns.iter().map(|c| c.name.clone()).collect(),
            rows: rows
                .rows
                .iter()
                .map(|row| row.iter().map(cell_to_string).collect())
                .collect(),
            affected_rows: None,
            execution_time_ms: Some(rows.execution_time_ms),
        },
        ExecutionResult::Affected(stmt) => QueryResult {
            columns: vec![],
            rows: vec![],
            affected_rows: Some(stmt.affected_rows),
            execution_time_ms: Some(stmt.execution_time_ms),
        },
        ExecutionResult::Documents(docs) => QueryResult {
            columns: vec!["document".to_string()],
            rows: docs.documents.iter().map(|d| vec![d.to_string()]).collect(),
            affected_rows: None,
            execution_time_ms: Some(docs.execution_time_ms),
        },
    }
}

fn cell_to_string(cell: &CellValue) -> String {
    match cell {
        CellValue::Null => "NULL".to_string(),
        CellValue::Bool(b) => b.to_string(),
        CellValue::Int(i) => i.to_string(),
        CellValue::Float(f) => f.to_string(),
        CellValue::Text(s) => s.clone(),
        CellValue::Json(v) => v.to_string(),
        CellValue::Blob(b) => format!("<binary {} bytes>", b.len()),
    }
}
