// guacr-database: Database protocol handlers for MySQL, PostgreSQL, SQL Server, Oracle, MongoDB, Redis, Elasticsearch, and Cassandra
//
// Provides SQL/NoSQL terminal access via WebRTC for database administration.
// All handlers use the shared QueryExecutor with ratatui-based rendering.

mod cassandra;
mod clickhouse;
mod csv_export;
mod csv_import;
#[cfg(feature = "dynamodb")]
mod dynamodb;
mod elasticsearch;
pub mod handler_helpers;
pub mod keeperdb_driver;
mod mongodb;
mod odbc;
mod query_executor;
mod ratatui_db_ui;
mod recording;
mod redis;
mod security;
mod sql;
mod threat;

pub use cassandra::CassandraHandler;
pub use clickhouse::ClickHouseHandler;
pub use csv_export::{generate_csv_filename, CsvExporter};
pub use csv_import::{validate_csv_table_name, CsvData, CsvImporter, ImportState};
#[cfg(feature = "dynamodb")]
pub use dynamodb::DynamoDbHandler;
pub use elasticsearch::ElasticsearchHandler;
pub use keeperdb_driver::build_connection_info;
pub use mongodb::MongoDbHandler;
pub use odbc::OdbcHandler;
pub use query_executor::{QueryExecutor, QueryResultData};
pub use ratatui_db_ui::DatabaseRatatuiApp;
pub use redis::RedisHandler;
pub use security::{
    check_csv_export_allowed, check_csv_import_allowed, check_query_allowed, classify_query,
    DatabaseSecuritySettings, QueryType,
};
pub use sql::{sql_handlers, SqlHandler};

// Re-export shared types from guacr-terminal
pub use guacr_terminal::QueryResult;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("Database connection failed: {0}")]
    ConnectionFailed(String),

    #[error("Connection error: {0}")]
    ConnectionError(String),

    #[error("Authentication failed: {0}")]
    AuthenticationFailed(String),

    #[error("Query error: {0}")]
    QueryError(String),

    #[error("Terminal error: {0}")]
    TerminalError(#[from] guacr_terminal::TerminalError),

    #[error("Handler error: {0}")]
    HandlerError(#[from] guacr_handlers::HandlerError),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, DatabaseError>;

#[cfg(test)]
mod tests;
