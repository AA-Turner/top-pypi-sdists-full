//! pyo3 bindings: a thin, Pythonic façade over the Rust builder.
//!
//! `PyExpr`/`PyQuery` wrap the core types. Python scalars (`int`/`float`/`str`/`bool`/`None`/`list`)
//! auto-promote to literals via the [`ExprArg`] / [`SortArg`] `FromPyObject` shims, so callers
//! rarely write `lit(...)` by hand. Everything is immutable — methods clone and return new values.

// pyo3 extracts arguments by value (`PyRef`, `ExprArg`, …); taking them by reference isn't part of
// the calling convention, so this lint fights the FFI boundary rather than improving anything.
#![allow(clippy::needless_pass_by_value)]

use pyo3::Borrowed;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyInt, PyList, PyTuple};

use crate::expr::{BinaryOp, Expr, Scalar, SortExpr, UnaryOp, Window};
use crate::query::{BuildError, JoinKind, Query, SetOp, TableRef};
use crate::render;

pyo3::create_exception!(
    datafusion_query_builder,
    QueryBuilderError,
    PyException,
    "Base error for the query builder. Raised directly for API misuse — passing a non-expression \
     argument, applying a method to the wrong query shape, joining without a FROM, etc."
);
pyo3::create_exception!(
    datafusion_query_builder,
    UnparsableSqlError,
    QueryBuilderError,
    "A `raw(...)` fragment or cast-type string that couldn't be parsed as SQL — typically \
     caller-supplied input (e.g. an end user's filter predicate). Subclass of QueryBuilderError."
);

fn py_err(e: BuildError) -> PyErr {
    match e {
        BuildError::UnparsableSql(m) => UnparsableSqlError::new_err(m),
        BuildError::Misuse(m) => QueryBuilderError::new_err(m),
    }
}

/// Coerce an arbitrary Python value into a façade [`Expr`]: existing `Expr` pass through, a
/// `Query` becomes a scalar subquery, and Python scalars/lists become literals.
fn coerce(obj: &Bound<'_, PyAny>) -> PyResult<Expr> {
    if let Ok(e) = obj.extract::<PyRef<'_, PyExpr>>() {
        return Ok(e.inner.clone());
    }
    if let Ok(q) = obj.extract::<PyRef<'_, PyQuery>>() {
        return Ok(Expr::ScalarSubquery(Box::new(q.inner.clone())));
    }
    if obj.is_none() {
        return Ok(Expr::lit(Scalar::Null));
    }
    if let Ok(b) = obj.cast::<PyBool>() {
        return Ok(Expr::lit(Scalar::Bool(b.is_true())));
    }
    if let Ok(seq) = obj.cast::<PyList>() {
        let items = seq
            .iter()
            .map(|v| coerce(&v))
            .collect::<PyResult<Vec<_>>>()?;
        return Ok(Expr::Array(items));
    }
    if let Ok(seq) = obj.cast::<PyTuple>() {
        let items = seq
            .iter()
            .map(|v| coerce(&v))
            .collect::<PyResult<Vec<_>>>()?;
        return Ok(Expr::Array(items));
    }
    // bool is a subclass of int, so this only runs after the PyBool check above. Match `int`
    // explicitly (rather than `extract::<i64>()`) so an out-of-range int errors loudly instead of
    // falling through to the `f64` branch and silently becoming a lossy float literal.
    if let Ok(int_obj) = obj.cast::<PyInt>() {
        return int_obj.extract::<i64>().map(|i| Expr::lit(Scalar::Int(i))).map_err(|_| {
            QueryBuilderError::new_err(
                "integer is out of range for a 64-bit SQL literal; cast it explicitly if you need a \
                 wider type",
            )
        });
    }
    if let Ok(f) = obj.extract::<f64>() {
        if !f.is_finite() {
            return Err(QueryBuilderError::new_err(
                "cannot use a non-finite float (NaN/Infinity) as a SQL literal",
            ));
        }
        return Ok(Expr::lit(Scalar::Float(f)));
    }
    if let Ok(s) = obj.extract::<String>() {
        return Ok(Expr::lit(Scalar::Str(s)));
    }
    Err(QueryBuilderError::new_err(format!(
        "cannot use {} as a SQL expression; pass a column/lit/expr or a scalar",
        obj.get_type().name()?
    )))
}

/// An argument position that accepts any expression-like Python value (auto-coerced).
struct ExprArg(Expr);

impl<'a, 'py> FromPyObject<'a, 'py> for ExprArg {
    type Error = PyErr;

    fn extract(obj: Borrowed<'a, 'py, PyAny>) -> PyResult<Self> {
        Ok(ExprArg(coerce(&obj)?))
    }
}

/// An argument position for `ORDER BY` / window ordering: a `SortExpr`, or any expression
/// (defaulting to ascending).
struct SortArg(SortExpr);

impl<'a, 'py> FromPyObject<'a, 'py> for SortArg {
    type Error = PyErr;

    fn extract(obj: Borrowed<'a, 'py, PyAny>) -> PyResult<Self> {
        if let Ok(s) = obj.extract::<PyRef<'_, PySortExpr>>() {
            return Ok(SortArg(s.inner.clone()));
        }
        Ok(SortArg(SortExpr {
            expr: coerce(&obj)?,
            asc: true,
            nulls_first: None,
        }))
    }
}

// ---------------------------------------------------------------------------
// Expr
// ---------------------------------------------------------------------------

#[pyclass(
    name = "Expr",
    module = "datafusion_query_builder",
    frozen,
    skip_from_py_object
)]
#[derive(Clone)]
pub struct PyExpr {
    inner: Expr,
}

impl PyExpr {
    fn new(inner: Expr) -> Self {
        PyExpr { inner }
    }

    fn bin(&self, op: BinaryOp, other: ExprArg) -> PyExpr {
        PyExpr::new(self.inner.clone().binary(op, other.0))
    }

    fn rbin(&self, op: BinaryOp, other: ExprArg) -> PyExpr {
        PyExpr::new(other.0.binary(op, self.inner.clone()))
    }
}

#[pymethods]
impl PyExpr {
    fn alias(&self, name: &str) -> PyExpr {
        PyExpr::new(self.inner.clone().alias(name))
    }

    fn cast(&self, data_type: &str) -> PyExpr {
        PyExpr::new(self.inner.clone().cast(data_type))
    }

    #[pyo3(signature = (values))]
    fn is_in(&self, values: &Bound<'_, PyAny>) -> PyResult<PyExpr> {
        if let Ok(q) = values.extract::<PyRef<'_, PyQuery>>() {
            return Ok(PyExpr::new(
                self.inner.clone().in_subquery(q.inner.clone(), false),
            ));
        }
        let list = coerce_list(values, "expected a list/tuple of values or a subquery")?;
        Ok(PyExpr::new(self.inner.clone().in_list(list, false)))
    }

    #[pyo3(signature = (values))]
    fn not_in(&self, values: &Bound<'_, PyAny>) -> PyResult<PyExpr> {
        if let Ok(q) = values.extract::<PyRef<'_, PyQuery>>() {
            return Ok(PyExpr::new(
                self.inner.clone().in_subquery(q.inner.clone(), true),
            ));
        }
        let list = coerce_list(values, "expected a list/tuple of values or a subquery")?;
        Ok(PyExpr::new(self.inner.clone().in_list(list, true)))
    }

    fn is_null(&self) -> PyExpr {
        PyExpr::new(self.inner.clone().is_null(false))
    }

    fn is_not_null(&self) -> PyExpr {
        PyExpr::new(self.inner.clone().is_null(true))
    }

    fn between(&self, low: ExprArg, high: ExprArg) -> PyExpr {
        PyExpr::new(self.inner.clone().between(low.0, high.0, false))
    }

    /// JSONB key-exists `?`: does `key` exist as a top-level key/element of this JSON value.
    /// A cheap presence check that (unlike `->> key IS NOT NULL`) never extracts the value.
    fn has_key(&self, key: ExprArg) -> PyExpr {
        self.bin(BinaryOp::JsonExists, key)
    }

    /// JSONB `?|`: does *any* of `keys` exist as a top-level key/element.
    fn has_any_key(&self, keys: &Bound<'_, PyAny>) -> PyResult<PyExpr> {
        let array = Expr::Array(coerce_list(keys, "expected a list/tuple of keys")?);
        Ok(PyExpr::new(
            self.inner.clone().binary(BinaryOp::JsonExistsAny, array),
        ))
    }

    /// JSONB `?&`: do *all* of `keys` exist as top-level keys/elements.
    fn has_all_keys(&self, keys: &Bound<'_, PyAny>) -> PyResult<PyExpr> {
        let array = Expr::Array(coerce_list(keys, "expected a list/tuple of keys")?);
        Ok(PyExpr::new(
            self.inner.clone().binary(BinaryOp::JsonExistsAll, array),
        ))
    }

    #[pyo3(signature = (nulls_first=None))]
    fn asc(&self, nulls_first: Option<bool>) -> PySortExpr {
        PySortExpr {
            inner: self.inner.clone().sort(true, nulls_first),
        }
    }

    #[pyo3(signature = (nulls_first=None))]
    fn desc(&self, nulls_first: Option<bool>) -> PySortExpr {
        PySortExpr {
            inner: self.inner.clone().sort(false, nulls_first),
        }
    }

    /// `agg(...) FILTER (WHERE cond)`. Valid only on a function-call expression.
    fn filter(&self, cond: ExprArg) -> PyResult<PyExpr> {
        let mut inner = self.inner.clone();
        match &mut inner {
            Expr::Function(call) => {
                call.filter = Some(Box::new(cond.0));
                Ok(PyExpr::new(inner))
            }
            _ => Err(QueryBuilderError::new_err(
                "filter() applies only to an aggregate function call",
            )),
        }
    }

    /// `fn(...) OVER (PARTITION BY … ORDER BY …)`. Valid only on a function-call expression.
    #[pyo3(signature = (partition_by=None, order_by=None))]
    fn over(
        &self,
        partition_by: Option<Vec<ExprArg>>,
        order_by: Option<Vec<SortArg>>,
    ) -> PyResult<PyExpr> {
        let mut inner = self.inner.clone();
        match &mut inner {
            Expr::Function(call) => {
                call.over = Some(Window {
                    partition_by: partition_by
                        .unwrap_or_default()
                        .into_iter()
                        .map(|a| a.0)
                        .collect(),
                    order_by: order_by
                        .unwrap_or_default()
                        .into_iter()
                        .map(|a| a.0)
                        .collect(),
                });
                Ok(PyExpr::new(inner))
            }
            _ => Err(QueryBuilderError::new_err(
                "over() applies only to a function call",
            )),
        }
    }

    // Arithmetic.
    fn __add__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Plus, other)
    }
    fn __radd__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::Plus, other)
    }
    fn __sub__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Minus, other)
    }
    fn __rsub__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::Minus, other)
    }
    fn __mul__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Multiply, other)
    }
    fn __rmul__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::Multiply, other)
    }
    fn __truediv__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Divide, other)
    }
    fn __rtruediv__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::Divide, other)
    }
    fn __mod__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Modulo, other)
    }
    fn __rmod__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::Modulo, other)
    }
    fn __neg__(&self) -> PyExpr {
        PyExpr::new(Expr::unary(UnaryOp::Neg, self.inner.clone()))
    }

    // Comparisons -> build expressions (not booleans), like Polars / datafusion-python.
    fn __eq__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Eq, other)
    }
    fn __ne__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::NotEq, other)
    }
    fn __lt__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Lt, other)
    }
    fn __le__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::LtEq, other)
    }
    fn __gt__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Gt, other)
    }
    fn __ge__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::GtEq, other)
    }

    // Boolean combinators: `&` / `|` / `~` (Python `and`/`or`/`not` can't be overloaded).
    fn __and__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::And, other)
    }
    fn __rand__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::And, other)
    }
    fn __or__(&self, other: ExprArg) -> PyExpr {
        self.bin(BinaryOp::Or, other)
    }
    fn __ror__(&self, other: ExprArg) -> PyExpr {
        self.rbin(BinaryOp::Or, other)
    }
    fn __invert__(&self) -> PyExpr {
        PyExpr::new(Expr::unary(UnaryOp::Not, self.inner.clone()))
    }

    fn __repr__(&self) -> String {
        format!("Expr({:?})", self.inner)
    }
}

fn coerce_list(obj: &Bound<'_, PyAny>, expected: &'static str) -> PyResult<Vec<Expr>> {
    let items: Vec<ExprArg> = obj
        .extract()
        .map_err(|_| QueryBuilderError::new_err(expected))?;
    Ok(items.into_iter().map(|a| a.0).collect())
}

// ---------------------------------------------------------------------------
// SortExpr
// ---------------------------------------------------------------------------

#[pyclass(
    name = "SortExpr",
    module = "datafusion_query_builder",
    frozen,
    skip_from_py_object
)]
#[derive(Clone)]
pub struct PySortExpr {
    inner: SortExpr,
}

#[pymethods]
impl PySortExpr {
    fn __repr__(&self) -> String {
        format!(
            "SortExpr({:?}, asc={}, nulls_first={:?})",
            self.inner.expr, self.inner.asc, self.inner.nulls_first
        )
    }
}

// ---------------------------------------------------------------------------
// Query
// ---------------------------------------------------------------------------

#[pyclass(
    name = "Query",
    module = "datafusion_query_builder",
    frozen,
    skip_from_py_object
)]
#[derive(Clone)]
pub struct PyQuery {
    inner: Query,
}

impl PyQuery {
    fn new(inner: Query) -> Self {
        PyQuery { inner }
    }
}

fn args_to_exprs(args: Vec<ExprArg>) -> Vec<Expr> {
    args.into_iter().map(|a| a.0).collect()
}

fn table_ref(obj: &Bound<'_, PyAny>, alias: Option<String>) -> PyResult<TableRef> {
    if let Ok(name) = obj.extract::<String>() {
        return Ok(TableRef::Named { name, alias });
    }
    if let Ok(q) = obj.extract::<PyRef<'_, PyQuery>>() {
        let alias = alias
            .ok_or_else(|| QueryBuilderError::new_err("a subquery source requires an alias"))?;
        return Ok(TableRef::Subquery {
            query: Box::new(q.inner.clone()),
            alias,
        });
    }
    Err(QueryBuilderError::new_err(
        "source must be a table/CTE name or a Query subquery",
    ))
}

fn join_kind(how: &str) -> PyResult<JoinKind> {
    match how {
        "inner" => Ok(JoinKind::Inner),
        "left" => Ok(JoinKind::Left),
        "right" => Ok(JoinKind::Right),
        "full" => Ok(JoinKind::Full),
        "cross" => Ok(JoinKind::Cross),
        other => Err(QueryBuilderError::new_err(format!(
            "unknown join type {other:?}; use inner/left/right/full/cross"
        ))),
    }
}

#[pymethods]
impl PyQuery {
    #[pyo3(signature = (*exprs))]
    fn select(&self, exprs: Vec<ExprArg>) -> PyResult<PyQuery> {
        self.inner
            .clone()
            .select(args_to_exprs(exprs))
            .map(PyQuery::new)
            .map_err(py_err)
    }

    fn filter(&self, predicate: ExprArg) -> PyResult<PyQuery> {
        self.inner
            .clone()
            .filter(predicate.0)
            .map(PyQuery::new)
            .map_err(py_err)
    }

    #[pyo3(name = "where_")]
    fn where_(&self, predicate: ExprArg) -> PyResult<PyQuery> {
        self.filter(predicate)
    }

    #[pyo3(signature = (*exprs))]
    fn group_by(&self, exprs: Vec<ExprArg>) -> PyResult<PyQuery> {
        self.inner
            .clone()
            .group_by(args_to_exprs(exprs))
            .map(PyQuery::new)
            .map_err(py_err)
    }

    fn having(&self, predicate: ExprArg) -> PyResult<PyQuery> {
        self.inner
            .clone()
            .having(predicate.0)
            .map(PyQuery::new)
            .map_err(py_err)
    }

    fn distinct(&self) -> PyResult<PyQuery> {
        self.inner
            .clone()
            .distinct()
            .map(PyQuery::new)
            .map_err(py_err)
    }

    #[pyo3(signature = (source, alias=None))]
    fn from_(&self, source: &Bound<'_, PyAny>, alias: Option<String>) -> PyResult<PyQuery> {
        match table_ref(source, alias)? {
            TableRef::Named { name, alias } => self
                .inner
                .clone()
                .from_named(name, alias)
                .map(PyQuery::new)
                .map_err(py_err),
            TableRef::Subquery { query, alias } => self
                .inner
                .clone()
                .from_subquery(*query, alias)
                .map(PyQuery::new)
                .map_err(py_err),
        }
    }

    #[pyo3(signature = (other, on=None, how="inner", alias=None))]
    fn join(
        &self,
        other: &Bound<'_, PyAny>,
        on: Option<ExprArg>,
        how: &str,
        alias: Option<String>,
    ) -> PyResult<PyQuery> {
        let relation = table_ref(other, alias)?;
        let kind = join_kind(how)?;
        self.inner
            .clone()
            .join(relation, kind, on.map(|a| a.0))
            .map(PyQuery::new)
            .map_err(py_err)
    }

    #[pyo3(signature = (other, alias=None))]
    fn cross_join(&self, other: &Bound<'_, PyAny>, alias: Option<String>) -> PyResult<PyQuery> {
        let relation = table_ref(other, alias)?;
        self.inner
            .clone()
            .join(relation, JoinKind::Cross, None)
            .map(PyQuery::new)
            .map_err(py_err)
    }

    fn with_cte(&self, name: &str, query: PyRef<'_, PyQuery>) -> PyQuery {
        PyQuery::new(self.inner.clone().with_cte(name, query.inner.clone()))
    }

    #[pyo3(signature = (*sorts))]
    fn order_by(&self, sorts: Vec<SortArg>) -> PyQuery {
        let sorts = sorts.into_iter().map(|s| s.0).collect();
        PyQuery::new(self.inner.clone().order_by(sorts))
    }

    fn limit(&self, n: i64) -> PyQuery {
        PyQuery::new(self.inner.clone().limit(n))
    }

    fn offset(&self, n: i64) -> PyQuery {
        PyQuery::new(self.inner.clone().offset(n))
    }

    #[pyo3(signature = (other, all=false))]
    fn union(&self, other: PyRef<'_, PyQuery>, all: bool) -> PyQuery {
        PyQuery::new(
            self.inner
                .clone()
                .set_op(SetOp::Union, all, other.inner.clone()),
        )
    }

    fn union_all(&self, other: PyRef<'_, PyQuery>) -> PyQuery {
        PyQuery::new(
            self.inner
                .clone()
                .set_op(SetOp::Union, true, other.inner.clone()),
        )
    }

    fn intersect(&self, other: PyRef<'_, PyQuery>) -> PyQuery {
        PyQuery::new(
            self.inner
                .clone()
                .set_op(SetOp::Intersect, false, other.inner.clone()),
        )
    }

    #[pyo3(name = "except_")]
    fn except_(&self, other: PyRef<'_, PyQuery>) -> PyQuery {
        PyQuery::new(
            self.inner
                .clone()
                .set_op(SetOp::Except, false, other.inner.clone()),
        )
    }

    /// Use this query as a scalar subquery expression.
    fn scalar(&self) -> PyExpr {
        PyExpr::new(self.inner.clone().scalar())
    }

    /// Render to SQL text.
    fn to_sql(&self) -> PyResult<String> {
        render::to_sql(&self.inner).map_err(py_err)
    }

    /// Render and re-parse to confirm the SQL is well-formed; returns the SQL.
    fn validate(&self) -> PyResult<String> {
        render::validate(&self.inner).map_err(py_err)
    }

    fn __str__(&self) -> PyResult<String> {
        self.to_sql()
    }

    fn __repr__(&self) -> String {
        match render::to_sql(&self.inner) {
            Ok(sql) => format!("Query({sql:?})"),
            Err(e) => format!("Query(<invalid: {e}>)"),
        }
    }
}

// ---------------------------------------------------------------------------
// CASE builder: when(cond).then(result)[.when(...).then(...)].otherwise(result)|.end()
// ---------------------------------------------------------------------------

#[pyclass(module = "datafusion_query_builder", frozen)]
struct WhenThen {
    whens: Vec<(Expr, Expr)>,
    pending: Expr,
}

#[pymethods]
impl WhenThen {
    fn then(&self, result: ExprArg) -> CaseBuilder {
        let mut whens = self.whens.clone();
        whens.push((self.pending.clone(), result.0));
        CaseBuilder { whens }
    }
}

#[pyclass(module = "datafusion_query_builder", frozen)]
struct CaseBuilder {
    whens: Vec<(Expr, Expr)>,
}

#[pymethods]
impl CaseBuilder {
    fn when(&self, condition: ExprArg) -> WhenThen {
        WhenThen {
            whens: self.whens.clone(),
            pending: condition.0,
        }
    }

    fn otherwise(&self, result: ExprArg) -> PyExpr {
        PyExpr::new(Expr::Case {
            when_then: self.whens.clone(),
            else_expr: Some(Box::new(result.0)),
        })
    }

    /// Finish the CASE with no ELSE branch.
    fn end(&self) -> PyExpr {
        PyExpr::new(Expr::Case {
            when_then: self.whens.clone(),
            else_expr: None,
        })
    }
}

// ---------------------------------------------------------------------------
// Free functions
// ---------------------------------------------------------------------------

#[pyfunction]
#[pyo3(signature = (name, relation=None))]
fn col(name: &str, relation: Option<&str>) -> PyExpr {
    match relation {
        Some(rel) => PyExpr::new(Expr::qualified_column(rel, name)),
        None => PyExpr::new(Expr::column(name)),
    }
}

#[pyfunction]
fn lit(value: &Bound<'_, PyAny>) -> PyResult<PyExpr> {
    Ok(PyExpr::new(coerce(value)?))
}

#[pyfunction]
fn param(name: &str) -> PyExpr {
    PyExpr::new(Expr::param(name))
}

#[pyfunction]
fn raw(sql: &str) -> PyExpr {
    PyExpr::new(Expr::raw(sql))
}

#[pyfunction]
fn table(name: &str) -> PyQuery {
    PyQuery::new(Query::table(name))
}

#[pyfunction]
fn query() -> PyQuery {
    PyQuery::new(Query::empty())
}

#[pyfunction]
#[pyo3(signature = (*exprs))]
fn and_(exprs: Vec<ExprArg>) -> PyExpr {
    PyExpr::new(Expr::all(args_to_exprs(exprs)))
}

#[pyfunction]
#[pyo3(signature = (*exprs))]
fn or_(exprs: Vec<ExprArg>) -> PyExpr {
    PyExpr::new(Expr::any(args_to_exprs(exprs)))
}

#[pyfunction]
fn not_(expr: ExprArg) -> PyExpr {
    PyExpr::new(Expr::unary(UnaryOp::Not, expr.0))
}

#[pyfunction]
fn when(condition: ExprArg) -> WhenThen {
    WhenThen {
        whens: vec![],
        pending: condition.0,
    }
}

// ---------------------------------------------------------------------------
// functions submodule (the `f.*` namespace)
// ---------------------------------------------------------------------------

fn func(name: &str, args: Vec<ExprArg>) -> PyExpr {
    PyExpr::new(crate::functions::call(name, args_to_exprs(args)))
}

macro_rules! scalar_fn {
    ($name:ident, $sql:literal) => {
        #[pyfunction]
        #[pyo3(signature = (*args))]
        fn $name(args: Vec<ExprArg>) -> PyExpr {
            func($sql, args)
        }
    };
}

scalar_fn!(sum, "sum");
scalar_fn!(avg, "avg");
scalar_fn!(min, "min");
scalar_fn!(max, "max");
scalar_fn!(round, "round");
scalar_fn!(coalesce, "coalesce");
scalar_fn!(nullif, "nullif");
scalar_fn!(date_bin, "date_bin");
scalar_fn!(date_trunc, "date_trunc");
scalar_fn!(time_bucket, "time_bucket");
scalar_fn!(approx_distinct, "approx_distinct");
scalar_fn!(approx_percentile_cont, "approx_percentile_cont");
scalar_fn!(json_keys, "json_keys");
scalar_fn!(unnest, "unnest");
scalar_fn!(metric_avg, "metric_avg");
scalar_fn!(metric_sum, "metric_sum");
scalar_fn!(metric_count, "metric_count");
scalar_fn!(metric_min, "metric_min");
scalar_fn!(metric_max, "metric_max");
scalar_fn!(metric_quantile, "metric_quantile");
scalar_fn!(metric_rate, "metric_rate");
scalar_fn!(metric_delta, "metric_delta");
scalar_fn!(metric_increase, "metric_increase");
scalar_fn!(metric_merge, "metric_merge");

/// `COUNT(*)` (no args), `COUNT(expr)`, or `COUNT(DISTINCT expr)`.
#[pyfunction]
#[pyo3(signature = (arg=None, *, distinct=false))]
fn count(arg: Option<ExprArg>, distinct: bool) -> PyExpr {
    match arg {
        None => PyExpr::new(crate::functions::count_star()),
        Some(a) => PyExpr::new(crate::functions::count(a.0, distinct)),
    }
}

/// Escape hatch: call any function by name.
#[pyfunction]
#[pyo3(signature = (name, *args))]
fn call(name: &str, args: Vec<ExprArg>) -> PyExpr {
    func(name, args)
}

fn register_functions(parent: &Bound<'_, PyModule>) -> PyResult<()> {
    let m = PyModule::new(parent.py(), "functions")?;
    m.add_function(wrap_pyfunction!(count, &m)?)?;
    m.add_function(wrap_pyfunction!(call, &m)?)?;
    m.add_function(wrap_pyfunction!(sum, &m)?)?;
    m.add_function(wrap_pyfunction!(avg, &m)?)?;
    m.add_function(wrap_pyfunction!(min, &m)?)?;
    m.add_function(wrap_pyfunction!(max, &m)?)?;
    m.add_function(wrap_pyfunction!(round, &m)?)?;
    m.add_function(wrap_pyfunction!(coalesce, &m)?)?;
    m.add_function(wrap_pyfunction!(nullif, &m)?)?;
    m.add_function(wrap_pyfunction!(date_bin, &m)?)?;
    m.add_function(wrap_pyfunction!(date_trunc, &m)?)?;
    m.add_function(wrap_pyfunction!(time_bucket, &m)?)?;
    m.add_function(wrap_pyfunction!(approx_distinct, &m)?)?;
    m.add_function(wrap_pyfunction!(approx_percentile_cont, &m)?)?;
    m.add_function(wrap_pyfunction!(json_keys, &m)?)?;
    m.add_function(wrap_pyfunction!(unnest, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_avg, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_sum, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_count, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_min, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_max, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_quantile, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_rate, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_delta, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_increase, &m)?)?;
    m.add_function(wrap_pyfunction!(metric_merge, &m)?)?;
    parent.add_submodule(&m)?;
    Ok(())
}

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("QueryBuilderError", m.py().get_type::<QueryBuilderError>())?;
    m.add(
        "UnparsableSqlError",
        m.py().get_type::<UnparsableSqlError>(),
    )?;
    m.add_class::<PyExpr>()?;
    m.add_class::<PySortExpr>()?;
    m.add_class::<PyQuery>()?;
    m.add_class::<WhenThen>()?;
    m.add_class::<CaseBuilder>()?;
    m.add_function(wrap_pyfunction!(col, m)?)?;
    m.add_function(wrap_pyfunction!(lit, m)?)?;
    m.add_function(wrap_pyfunction!(param, m)?)?;
    m.add_function(wrap_pyfunction!(raw, m)?)?;
    m.add_function(wrap_pyfunction!(table, m)?)?;
    m.add_function(wrap_pyfunction!(query, m)?)?;
    m.add_function(wrap_pyfunction!(and_, m)?)?;
    m.add_function(wrap_pyfunction!(or_, m)?)?;
    m.add_function(wrap_pyfunction!(not_, m)?)?;
    m.add_function(wrap_pyfunction!(when, m)?)?;
    register_functions(m)?;
    Ok(())
}

// ---------------------------------------------------------------------------
// Coercion-boundary tests (the Python-only layer)
// ---------------------------------------------------------------------------
//
// These exercise `coerce()` — the one piece of logic that can only be tested with real Python
// objects (bool-is-int ordering, None, big ints, non-finite floats, list/tuple). They run inside
// `cargo test` against an embedded interpreter, then *compose* with `tests/properties.rs`: these
// prove "Python value -> correct façade `Scalar`", and the property tests prove "that `Scalar`
// renders to SQL DataFusion executes back to the same value". Together that's Python-type-to-value
// coverage without re-running the engine oracle in a Python-linked build.
//
// Gated behind `test-embed` (which adds pyo3's auto-initialize + libpython) so the default
// `cargo test` fast loop stays Python-free. Run with:
//   PYO3_PYTHON=$PWD/.venv/bin/python cargo test -p datafusion-query-builder --lib --features test-embed
#[cfg(all(test, feature = "test-embed"))]
mod coercion_tests {
    use std::ffi::CStr;

    use super::*;

    /// Evaluate a Python expression and run its result through `coerce`.
    fn coerce_eval(code: &CStr) -> PyResult<Expr> {
        Python::attach(|py| {
            let obj = py.eval(code, None, None)?;
            coerce(&obj)
        })
    }

    fn lit(scalar: Scalar) -> Expr {
        Expr::lit(scalar)
    }

    #[test]
    fn bool_coerces_to_bool_not_int() {
        // The classic trap: Python `bool` is an `int` subclass, so the PyBool check must come first.
        assert_eq!(coerce_eval(c"True").unwrap(), lit(Scalar::Bool(true)));
        assert_eq!(coerce_eval(c"False").unwrap(), lit(Scalar::Bool(false)));
    }

    #[test]
    fn none_coerces_to_null() {
        assert_eq!(coerce_eval(c"None").unwrap(), lit(Scalar::Null));
    }

    #[test]
    fn ints_coerce_including_i64_bounds() {
        assert_eq!(coerce_eval(c"42").unwrap(), lit(Scalar::Int(42)));
        assert_eq!(coerce_eval(c"-7").unwrap(), lit(Scalar::Int(-7)));
        assert_eq!(
            coerce_eval(c"9223372036854775807").unwrap(),
            lit(Scalar::Int(i64::MAX))
        );
        assert_eq!(
            coerce_eval(c"-9223372036854775808").unwrap(),
            lit(Scalar::Int(i64::MIN))
        );
    }

    #[test]
    fn int_beyond_i64_is_rejected_not_silently_floated() {
        // Regression: `2**63` used to fail `extract::<i64>()`, fall through to the `f64` branch, and
        // become a lossy `Float` literal. It must error loudly instead.
        let err = coerce_eval(c"2**63").unwrap_err();
        assert!(
            err.to_string().contains("out of range"),
            "unexpected error: {err}"
        );
    }

    #[test]
    fn finite_floats_coerce_to_float() {
        assert_eq!(coerce_eval(c"3.5").unwrap(), lit(Scalar::Float(3.5)));
        assert_eq!(coerce_eval(c"-0.0").unwrap(), lit(Scalar::Float(-0.0)));
    }

    #[test]
    fn non_finite_floats_are_rejected() {
        // Regression: NaN/Infinity have no SQL literal syntax; coercing them produced a bareword
        // (`NaN`) that DataFusion can't parse. Reject at the boundary with a clear error.
        for code in [c"float('nan')", c"float('inf')", c"float('-inf')"] {
            assert!(
                coerce_eval(code).is_err(),
                "expected {code:?} to be rejected"
            );
        }
    }

    #[test]
    fn str_coerces_to_str() {
        assert_eq!(
            coerce_eval(c"\"O'Brien\"").unwrap(),
            lit(Scalar::Str("O'Brien".into()))
        );
    }

    #[test]
    fn list_and_tuple_coerce_to_array() {
        assert_eq!(
            coerce_eval(c"[1, 'a', True]").unwrap(),
            Expr::Array(vec![
                lit(Scalar::Int(1)),
                lit(Scalar::Str("a".into())),
                lit(Scalar::Bool(true))
            ]),
        );
        assert_eq!(
            coerce_eval(c"(1, 2)").unwrap(),
            Expr::Array(vec![lit(Scalar::Int(1)), lit(Scalar::Int(2))]),
        );
    }

    #[test]
    fn unsupported_types_are_rejected() {
        assert!(coerce_eval(c"{'a': 1}").is_err());
        assert!(coerce_eval(c"object()").is_err());
    }
}
