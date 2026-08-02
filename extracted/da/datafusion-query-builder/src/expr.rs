//! Façade expression types.
//!
//! These are ordinary, span-free enums that callers (and the pyo3 layer) build up. They know
//! nothing about `sqlparser`; the [`crate::lower`] module is the only place that translates them
//! into `sqlparser::ast`. Keeping the façade independent means a `sqlparser` version bump touches
//! `lower.rs` and nothing else.

use crate::query::Query;

/// A scalar literal. Values are always rendered safely (strings get their quotes escaped by
/// `sqlparser`'s `Display`), so untrusted input is injection-safe by construction.
#[derive(Debug, Clone, PartialEq)]
pub enum Scalar {
    Null,
    Bool(bool),
    Int(i64),
    /// The f64 is rendered with an explicit decimal point during lowering (see `lower.rs`) so the
    /// engine always reads it as floating point.
    Float(f64),
    Str(String),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BinaryOp {
    Eq,
    NotEq,
    Lt,
    LtEq,
    Gt,
    GtEq,
    Plus,
    Minus,
    Multiply,
    Divide,
    Modulo,
    And,
    Or,
    StringConcat,
    /// JSONB key-exists `?`: does the string on the right exist as a top-level key/element of the
    /// JSON on the left. DataFusion's JSON extension maps it to `json_contains`.
    JsonExists,
    /// JSONB `?|`: does *any* string in the right-hand array exist as a top-level key/element.
    JsonExistsAny,
    /// JSONB `?&`: do *all* strings in the right-hand array exist as top-level keys/elements.
    JsonExistsAll,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UnaryOp {
    Not,
    Neg,
}

/// A window specification for `OVER (PARTITION BY … ORDER BY …)`.
#[derive(Debug, Clone, PartialEq, Default)]
pub struct Window {
    pub partition_by: Vec<Expr>,
    pub order_by: Vec<SortExpr>,
}

/// An expression with an ordering direction, used in `ORDER BY`.
#[derive(Debug, Clone, PartialEq)]
pub struct SortExpr {
    pub expr: Expr,
    pub asc: bool,
    /// `None` lets the engine pick its default null ordering.
    pub nulls_first: Option<bool>,
}

/// A function call. Covers aggregates, scalar functions, and our `metric_*` UDFs uniformly.
#[derive(Debug, Clone, PartialEq)]
pub struct Call {
    pub name: String,
    pub args: Vec<Expr>,
    /// `COUNT(DISTINCT x)`.
    pub distinct: bool,
    /// `COUNT(*)` — when set, `args` is ignored and a wildcard is emitted.
    pub wildcard: bool,
    /// `agg(...) FILTER (WHERE cond)`.
    pub filter: Option<Box<Expr>>,
    /// `fn(...) OVER (...)`.
    pub over: Option<Window>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Column {
        relation: Option<String>,
        name: String,
    },
    Literal(Scalar),
    /// A list literal, e.g. `ARRAY['a', 'b']`.
    Array(Vec<Expr>),
    /// A DataFusion `${...}` placeholder, rendered as `${name}`.
    Param(String),
    /// Raw SQL fragment, emitted verbatim. The sole unescaped path — an explicit escape hatch.
    Raw(String),
    Binary {
        left: Box<Expr>,
        op: BinaryOp,
        right: Box<Expr>,
    },
    Unary {
        op: UnaryOp,
        expr: Box<Expr>,
    },
    IsNull {
        expr: Box<Expr>,
        negated: bool,
    },
    InList {
        expr: Box<Expr>,
        list: Vec<Expr>,
        negated: bool,
    },
    InSubquery {
        expr: Box<Expr>,
        subquery: Box<Query>,
        negated: bool,
    },
    Between {
        expr: Box<Expr>,
        low: Box<Expr>,
        high: Box<Expr>,
        negated: bool,
    },
    Case {
        when_then: Vec<(Expr, Expr)>,
        else_expr: Option<Box<Expr>>,
    },
    Cast {
        expr: Box<Expr>,
        /// Data-type text (e.g. `"Int64"`, `"double precision"`, `"text[]"`), parsed at lower time.
        data_type: String,
    },
    Function(Call),
    Aliased {
        expr: Box<Expr>,
        alias: String,
    },
    ScalarSubquery(Box<Query>),
}

impl Expr {
    pub fn column(name: impl Into<String>) -> Self {
        Expr::Column {
            relation: None,
            name: name.into(),
        }
    }

    pub fn qualified_column(relation: impl Into<String>, name: impl Into<String>) -> Self {
        Expr::Column {
            relation: Some(relation.into()),
            name: name.into(),
        }
    }

    pub fn lit(scalar: Scalar) -> Self {
        Expr::Literal(scalar)
    }

    pub fn param(name: impl Into<String>) -> Self {
        Expr::Param(name.into())
    }

    pub fn raw(sql: impl Into<String>) -> Self {
        Expr::Raw(sql.into())
    }

    #[must_use]
    pub fn binary(self, op: BinaryOp, rhs: Expr) -> Self {
        Expr::Binary {
            left: Box::new(self),
            op,
            right: Box::new(rhs),
        }
    }

    #[must_use]
    pub fn unary(op: UnaryOp, expr: Expr) -> Self {
        Expr::Unary {
            op,
            expr: Box::new(expr),
        }
    }

    #[must_use]
    pub fn is_null(self, negated: bool) -> Self {
        Expr::IsNull {
            expr: Box::new(self),
            negated,
        }
    }

    #[must_use]
    pub fn in_list(self, list: Vec<Expr>, negated: bool) -> Self {
        Expr::InList {
            expr: Box::new(self),
            list,
            negated,
        }
    }

    #[must_use]
    pub fn in_subquery(self, subquery: Query, negated: bool) -> Self {
        Expr::InSubquery {
            expr: Box::new(self),
            subquery: Box::new(subquery),
            negated,
        }
    }

    #[must_use]
    pub fn between(self, low: Expr, high: Expr, negated: bool) -> Self {
        Expr::Between {
            expr: Box::new(self),
            low: Box::new(low),
            high: Box::new(high),
            negated,
        }
    }

    #[must_use]
    pub fn cast(self, data_type: impl Into<String>) -> Self {
        Expr::Cast {
            expr: Box::new(self),
            data_type: data_type.into(),
        }
    }

    #[must_use]
    pub fn alias(self, alias: impl Into<String>) -> Self {
        // Re-aliasing replaces rather than nests.
        let inner = match self {
            Expr::Aliased { expr, .. } => *expr,
            other => other,
        };
        Expr::Aliased {
            expr: Box::new(inner),
            alias: alias.into(),
        }
    }

    #[must_use]
    pub fn sort(self, asc: bool, nulls_first: Option<bool>) -> SortExpr {
        SortExpr {
            expr: self,
            asc,
            nulls_first,
        }
    }

    /// Combine many expressions with `AND` (used for n-ary `and_`). Empty -> `TRUE`.
    #[must_use]
    pub fn all(exprs: Vec<Expr>) -> Expr {
        Self::reduce(exprs, BinaryOp::And, Scalar::Bool(true))
    }

    /// Combine many expressions with `OR` (used for n-ary `or_`). Empty -> `FALSE`.
    #[must_use]
    pub fn any(exprs: Vec<Expr>) -> Expr {
        Self::reduce(exprs, BinaryOp::Or, Scalar::Bool(false))
    }

    fn reduce(exprs: Vec<Expr>, op: BinaryOp, empty: Scalar) -> Expr {
        let mut iter = exprs.into_iter();
        match iter.next() {
            None => Expr::Literal(empty),
            Some(first) => iter.fold(first, |acc, e| acc.binary(op, e)),
        }
    }
}
