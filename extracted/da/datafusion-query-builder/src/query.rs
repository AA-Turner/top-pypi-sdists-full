//! Façade query/plan types — a generative (immutable) SELECT builder.
//!
//! Every mutating method takes `self` by value and returns a new `Query`, mirroring
//! datafusion-python / Polars / SQLAlchemy and sidestepping pyo3 `&mut self` friction. Cloning is
//! cheap relative to building and rendering SQL.

use crate::expr::{Expr, SortExpr};

/// Why a query couldn't be built. The two cases map to distinct Python exceptions: caller-supplied
/// SQL that won't parse (often end-user input) vs. the builder being driven into an invalid state
/// (a programming error).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BuildError {
    /// A `raw(...)` fragment or cast-type string that couldn't be parsed as SQL. Surfaced to
    /// Python as `UnparsableSqlError`.
    UnparsableSql(String),
    /// The builder was used incorrectly — a method applied to the wrong query shape, a JOIN with
    /// no FROM, or a query that re-parse-validation rejected. Surfaced as `QueryBuilderError`.
    Misuse(String),
}

impl BuildError {
    #[must_use]
    pub fn message(&self) -> &str {
        match self {
            BuildError::UnparsableSql(m) | BuildError::Misuse(m) => m,
        }
    }
}

impl std::fmt::Display for BuildError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.message())
    }
}

impl std::error::Error for BuildError {}

pub type Result<T> = std::result::Result<T, BuildError>;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum JoinKind {
    Inner,
    Left,
    Right,
    Full,
    Cross,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SetOp {
    Union,
    Intersect,
    Except,
}

/// Something that can appear in a `FROM` / `JOIN` slot.
#[derive(Debug, Clone, PartialEq)]
pub enum TableRef {
    /// A bare table name, or a CTE reference by name.
    Named {
        name: String,
        alias: Option<String>,
    },
    Subquery {
        query: Box<Query>,
        alias: String,
    },
}

#[derive(Debug, Clone, PartialEq)]
pub struct Join {
    pub relation: TableRef,
    pub kind: JoinKind,
    pub on: Option<Expr>,
}

#[derive(Debug, Clone, PartialEq, Default)]
pub struct Select {
    /// Empty -> `SELECT *`.
    pub projection: Vec<Expr>,
    pub distinct: bool,
    pub from: Option<TableRef>,
    pub joins: Vec<Join>,
    /// AND-combined at lower time.
    pub filters: Vec<Expr>,
    pub group_by: Vec<Expr>,
    pub having: Option<Expr>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Body {
    Select(Box<Select>),
    SetOp {
        op: SetOp,
        all: bool,
        left: Box<Query>,
        right: Box<Query>,
    },
}

#[derive(Debug, Clone, PartialEq)]
pub struct Cte {
    pub name: String,
    pub query: Query,
}

/// A complete query: optional `WITH` CTEs, a body (SELECT or set op), and outer
/// `ORDER BY` / `LIMIT` / `OFFSET`.
#[derive(Debug, Clone, PartialEq)]
pub struct Query {
    pub ctes: Vec<Cte>,
    pub body: Body,
    pub order_by: Vec<SortExpr>,
    pub limit: Option<i64>,
    pub offset: Option<i64>,
}

impl Query {
    /// Start a query selecting from a named table (or a CTE defined with [`Query::with_cte`]).
    #[must_use]
    pub fn table(name: impl Into<String>) -> Self {
        Query::from_select(Select {
            from: Some(TableRef::Named {
                name: name.into(),
                alias: None,
            }),
            ..Select::default()
        })
    }

    /// Start a query with no `FROM` (e.g. `SELECT 1`).
    #[must_use]
    pub fn empty() -> Self {
        Query::from_select(Select::default())
    }

    fn from_select(select: Select) -> Self {
        Query {
            ctes: vec![],
            body: Body::Select(Box::new(select)),
            order_by: vec![],
            limit: None,
            offset: None,
        }
    }

    /// Mutate the inner `Select`, erroring if the body is a set operation.
    fn map_select(mut self, f: impl FnOnce(&mut Select)) -> Result<Self> {
        match &mut self.body {
            Body::Select(select) => {
                f(select);
                Ok(self)
            }
            Body::SetOp { .. } => Err(BuildError::Misuse(
                "this method applies to a SELECT, but the query is a set operation; \
                 wrap it as a subquery first"
                    .into(),
            )),
        }
    }

    pub fn select(self, projection: Vec<Expr>) -> Result<Self> {
        self.map_select(|s| s.projection = projection)
    }

    pub fn distinct(self) -> Result<Self> {
        self.map_select(|s| s.distinct = true)
    }

    /// Add a `WHERE` predicate. Multiple calls are AND-combined.
    pub fn filter(self, predicate: Expr) -> Result<Self> {
        self.map_select(|s| s.filters.push(predicate))
    }

    pub fn group_by(self, exprs: Vec<Expr>) -> Result<Self> {
        self.map_select(|s| s.group_by.extend(exprs))
    }

    pub fn having(self, predicate: Expr) -> Result<Self> {
        self.map_select(|s| s.having = Some(predicate))
    }

    /// Replace the `FROM` source with a table/CTE name.
    pub fn from_named(self, name: impl Into<String>, alias: Option<String>) -> Result<Self> {
        let name = name.into();
        self.map_select(|s| {
            s.from = Some(TableRef::Named { name, alias });
        })
    }

    /// Replace the `FROM` source with a subquery.
    pub fn from_subquery(self, query: Query, alias: impl Into<String>) -> Result<Self> {
        let alias = alias.into();
        self.map_select(|s| {
            s.from = Some(TableRef::Subquery {
                query: Box::new(query),
                alias,
            });
        })
    }

    pub fn join(self, relation: TableRef, kind: JoinKind, on: Option<Expr>) -> Result<Self> {
        self.map_select(|s| s.joins.push(Join { relation, kind, on }))
    }

    #[must_use]
    pub fn order_by(mut self, mut sort: Vec<SortExpr>) -> Self {
        self.order_by.append(&mut sort);
        self
    }

    #[must_use]
    pub fn limit(mut self, n: i64) -> Self {
        self.limit = Some(n);
        self
    }

    #[must_use]
    pub fn offset(mut self, n: i64) -> Self {
        self.offset = Some(n);
        self
    }

    /// Add a CTE; reference it later by name in a `FROM` slot.
    #[must_use]
    pub fn with_cte(mut self, name: impl Into<String>, query: Query) -> Self {
        self.ctes.push(Cte {
            name: name.into(),
            query,
        });
        self
    }

    /// Combine with another query via a set operation. The new outer query starts with no
    /// CTEs/ORDER BY/LIMIT (add them afterward to apply to the whole result); each operand keeps
    /// its own, and any operand carrying them is wrapped in a derived subquery during lowering.
    #[must_use]
    pub fn set_op(self, op: SetOp, all: bool, other: Query) -> Self {
        Query {
            ctes: vec![],
            body: Body::SetOp {
                op,
                all,
                left: Box::new(self),
                right: Box::new(other),
            },
            order_by: vec![],
            limit: None,
            offset: None,
        }
    }

    /// Use this query as a scalar subquery expression.
    #[must_use]
    pub fn scalar(self) -> Expr {
        Expr::ScalarSubquery(Box::new(self))
    }
}
