//! Programmatic builder for DataFusion SQL — the dialect DataFusion parses.
//!
//! The crate is a thin, immutable façade ([`expr`], [`query`], [`functions`]) over the
//! `sqlparser` AST. Callers build façade values; [`render::to_sql`] lowers them to SQL text via
//! the single [`lower`] boundary. See `plans/2026-06-21-query-builder.md` for the design.
//!
//! The Python bindings live in [`python`], compiled only with the `python` feature.

// The builder's fallible methods uniformly return `BuildError` (unparseable SQL vs. API misuse);
// a per-method `# Errors` paragraph would just restate that, so allow the doc lint here. The two
// style lints are matters of taste that read more clearly the way they're written.
#![allow(
    clippy::missing_errors_doc,
    clippy::must_use_candidate,
    clippy::single_match_else
)]

mod dialect;
pub mod expr;
pub mod functions;
pub mod lower;
pub mod query;
pub mod render;

#[cfg(feature = "python")]
mod python;

pub use expr::{BinaryOp, Call, Expr, Scalar, SortExpr, UnaryOp, Window};
pub use query::{Body, BuildError, Cte, Join, JoinKind, Query, Select, SetOp, TableRef};
pub use render::{to_sql, validate};
