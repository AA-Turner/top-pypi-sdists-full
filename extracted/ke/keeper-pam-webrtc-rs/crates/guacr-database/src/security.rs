// Database-specific security features
//
// Re-exports security types from guacr-handlers for use by database protocol handlers.
// This module provides backward compatibility for existing code while
// consolidating security logic in the shared guacr-handlers crate.

// Re-export all database security types from the shared security module
pub use guacr_handlers::{
    // Database-specific
    check_sql_query_allowed,
    classify_sql_query,
    is_mysql_export_query,
    is_mysql_import_query,
    is_postgres_copy_in,
    is_postgres_copy_out,
    DatabaseSecuritySettings,
    QueryType,
};

// Convenience aliases for backward compatibility
pub use classify_sql_query as classify_query;

/// Check if a query is allowed - convenience wrapper
pub fn check_query_allowed(query: &str, settings: &DatabaseSecuritySettings) -> Result<(), String> {
    check_sql_query_allowed(query, settings)
}

/// Check if CSV export is allowed
pub fn check_csv_export_allowed(settings: &DatabaseSecuritySettings) -> Result<(), String> {
    if settings.is_csv_export_allowed() {
        Ok(())
    } else {
        Err("CSV export is disabled by your administrator.".to_string())
    }
}

/// Check if CSV import is allowed
pub fn check_csv_import_allowed(settings: &DatabaseSecuritySettings) -> Result<(), String> {
    if settings.is_csv_import_allowed() {
        Ok(())
    } else {
        Err("CSV import is disabled by your administrator.".to_string())
    }
}
