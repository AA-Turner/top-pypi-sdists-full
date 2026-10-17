//! Rendering façade queries to SQL text, plus a cheap round-trip parse self-test.

use std::ops::ControlFlow;

use sqlparser::ast::{Query as AstQuery, VisitMut, VisitorMut};
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
///
/// The re-parse ignores CTE `MATERIALIZED` directives. The generic grammar rejects them, and the
/// builder emits them from a fixed enum, so they cannot make the SQL malformed.
pub fn validate(query: &Query) -> Result<String> {
    let mut lowered = lower_query(query)?;
    let sql = lowered.to_string();
    let _ = lowered.visit(&mut ClearCteMaterialization);
    let dialect = BuilderDialect;
    Parser::parse_sql(&dialect, &lowered.to_string()).map_err(|e| {
        // The builder produced SQL that doesn't parse — a bug in the builder, not caller input.
        BuildError::Misuse(format!(
            "generated SQL failed to re-parse: {e}\n  sql: {sql}"
        ))
    })?;
    Ok(sql)
}

/// Removes the materialization directive from every CTE, nested CTEs included.
struct ClearCteMaterialization;

impl VisitorMut for ClearCteMaterialization {
    type Break = ();

    fn pre_visit_query(&mut self, query: &mut AstQuery) -> ControlFlow<()> {
        if let Some(with) = &mut query.with {
            for cte in &mut with.cte_tables {
                cte.materialized = None;
            }
        }
        ControlFlow::Continue(())
    }
}
