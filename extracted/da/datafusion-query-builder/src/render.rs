//! Rendering façade queries to SQL text, plus a cheap round-trip parse self-test.

use sqlparser::parser::Parser;

use crate::dialect::BuilderDialect;
use crate::lower::lower_query;
use crate::query::{BuildError, Query, Result};

/// Render a query to DataFusion SQL text.
pub fn to_sql(query: &Query) -> Result<String> {
    Ok(lower_query(query)?.to_string())
}

/// Render and re-parse the query, returning the SQL on success. Proves *parseability* (catches a
/// malformed `raw(...)` fragment or a structural bug); it does not prove the query will *plan*
/// (unknown columns/functions/types are caught by DataFusion at plan time). Returns the SQL so callers can
/// validate-and-use in one step. Re-parses with [`BuilderDialect`] — the same grammar `raw(...)`
/// fragments are parsed against — so a fragment that lowered cleanly always re-parses.
pub fn validate(query: &Query) -> Result<String> {
    let sql = to_sql(query)?;
    let dialect = BuilderDialect;
    Parser::parse_sql(&dialect, &sql).map_err(|e| {
        // The builder produced SQL that doesn't parse — a bug in the builder, not caller input.
        BuildError::Misuse(format!(
            "generated SQL failed to re-parse: {e}\n  sql: {sql}"
        ))
    })?;
    Ok(sql)
}
