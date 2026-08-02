//! Function-call constructors.
//!
//! A single generic [`call`] builds any function; the named helpers exist so Rust callers and
//! tests read naturally and so there's one catalog to keep in sync with the Python `f.*`
//! namespace. Functions are not validated against a registry here — unknown names render fine and
//! DataFusion validates them at plan time. `metric_*` are our custom value-struct UDFs.

use crate::expr::{Call, Expr};

/// Build a function call from a name and arguments. The general escape hatch behind `f.call(...)`.
#[must_use]
pub fn call(name: impl Into<String>, args: Vec<Expr>) -> Expr {
    Expr::Function(Call {
        name: name.into(),
        args,
        distinct: false,
        wildcard: false,
        filter: None,
        over: None,
    })
}

/// `COUNT(*)`.
#[must_use]
pub fn count_star() -> Expr {
    Expr::Function(Call {
        name: "count".into(),
        args: vec![],
        distinct: false,
        wildcard: true,
        filter: None,
        over: None,
    })
}

/// `COUNT(expr)` or `COUNT(DISTINCT expr)`.
#[must_use]
pub fn count(arg: Expr, distinct: bool) -> Expr {
    Expr::Function(Call {
        name: "count".into(),
        args: vec![arg],
        distinct,
        wildcard: false,
        filter: None,
        over: None,
    })
}

/// Names of the value-struct metric UDFs, for documentation / catalog parity with the frontend.
pub const METRIC_UDFS: &[&str] = &[
    "metric_avg",
    "metric_sum",
    "metric_count",
    "metric_min",
    "metric_max",
    "metric_quantile",
    "metric_rate",
    "metric_delta",
    "metric_increase",
    "metric_merge",
];
