//! The single SQL dialect the builder parses against.
//!
//! Two call sites re-parse SQL: [`crate::lower`] parses `raw(...)` fragments and cast-type strings
//! into AST nodes, and [`crate::render`] re-parses the fully rendered query as a self-test. Both use
//! this one dialect so a `raw` fragment round-trips through the *same* grammar the final query is
//! validated against — otherwise a fragment could parse one way going in and fail (or mean something
//! else) coming out.
//!
//! It is `GenericDialect` plus the handful of capabilities DataFusion's own parser accepts that the
//! generic dialect gates off by default.

use sqlparser::dialect::{Dialect, GenericDialect};

/// Generic SQL plus the DataFusion-flavoured extensions the builder relies on.
#[derive(Debug, Default)]
pub(crate) struct BuilderDialect;

impl Dialect for BuilderDialect {
    fn is_identifier_start(&self, ch: char) -> bool {
        GenericDialect {}.is_identifier_start(ch)
    }

    fn is_identifier_part(&self, ch: char) -> bool {
        GenericDialect {}.is_identifier_part(ch)
    }

    /// `${var}` dollar-brace placeholders (the pydantic `sqlparser` fork extension the DataFusion
    /// planner relies on).
    fn supports_dollar_placeholder(&self) -> bool {
        true
    }

    // Capabilities DataFusion's parser accepts that the generic dialect gates off by default.
    fn supports_filter_during_aggregation(&self) -> bool {
        true
    }

    fn supports_group_by_expr(&self) -> bool {
        true
    }

    /// Parse `?` / `?|` / `?&` as the Postgres-style JSON key-exists operators (the same ones our
    /// engine uses), rather than as prepared-statement `?` placeholders.
    ///
    /// The method name is an `sqlparser` quirk, not our intent: the fork happens to gate `?`-family
    /// tokenization behind `supports_geometric_types` — it's the single lever that flips `?` from a
    /// placeholder to `Token::Question`, and the real Postgres dialect enables the operators through
    /// the same switch. This has nothing to do with geometry; we're here only for the JSON operators.
    /// With it off, `attributes ? 'key'` tokenizes `?` as a placeholder, `parse_expr` stops at
    /// `attributes`, and the operator is silently dropped.
    fn supports_geometric_types(&self) -> bool {
        true
    }
}
