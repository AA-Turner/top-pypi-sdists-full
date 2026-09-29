//! The single boundary between our façade types and `sqlparser::ast`.
//!
//! Nothing outside this module imports `sqlparser::ast`. When a `sqlparser` bump changes the AST
//! (historically the `Function`/`FunctionArguments`, `Value`/`ValueWithSpan`, `GroupByExpr` and
//! `OrderBy`/`LimitClause` shapes have all moved), the break surfaces here and nowhere else. The
//! high-churn nodes are isolated into the small `lower_*` helpers below for exactly that reason.

use sqlparser::ast;
use sqlparser::parser::Parser;
use sqlparser::tokenizer::Span;

use crate::dialect::BuilderDialect;
use crate::expr::{BinaryOp, Call, Expr, Scalar, SortExpr, UnaryOp, Window};
use crate::query::{Body, BuildError, Cte, Join, JoinKind, Query, Result, Select, SetOp, TableRef};

fn ident(name: &str) -> ast::Ident {
    ast::Ident::new(name)
}

fn object_name(name: &str) -> ast::ObjectName {
    ast::ObjectName::from(vec![ident(name)])
}

/// Build a table alias. `explicit` controls the `AS` keyword: tables/derived subqueries read
/// better with it (`(...) AS sub`), but a CTE name must omit it (`WITH name AS (...)`, not
/// `WITH AS name AS (...)`).
fn table_alias(name: &str, explicit: bool) -> ast::TableAlias {
    ast::TableAlias {
        explicit,
        name: ident(name),
        columns: vec![],
        at: None,
    }
}

fn value_expr(value: ast::Value) -> ast::Expr {
    ast::Expr::Value(value.with_empty_span())
}

fn number(text: String) -> ast::Expr {
    value_expr(ast::Value::Number(text, false))
}

/// Lower a scalar literal.
fn lower_scalar(scalar: &Scalar) -> ast::Expr {
    match scalar {
        Scalar::Null => value_expr(ast::Value::Null),
        Scalar::Bool(b) => value_expr(ast::Value::Boolean(*b)),
        Scalar::Int(i) => number(i.to_string()),
        Scalar::Float(f) => {
            // Ensure a decimal point survives so the engine reads it as floating point.
            let mut text = format!("{f}");
            if !text.contains(['.', 'e', 'E', 'n', 'i']) {
                text.push_str(".0");
            }
            number(text)
        }
        Scalar::Str(s) => string_literal(s),
    }
}

/// Render a string value as a DataFusion single-quoted literal.
///
/// We deliberately do *not* route the value through `ast::Value::SingleQuotedString`. That node's
/// `Display` escaper (in the `sqlparser` fork) is backslash-aware: when a `'` is preceded by a
/// `\` it assumes the quote is already backslash-escaped and emits it un-doubled — so the value
/// `\'` renders as `'\''`. DataFusion's dialect does not honor backslash escapes
/// (`supports_string_literal_backslash_escape()` is `false`), so `'\''` is an *unterminated*
/// literal that the query then fails to parse. The only dialect-correct escaping is to double
/// every single quote and leave backslashes untouched (`\'` -> `'\'''`). We build that text
/// ourselves and carry it through `Value::Placeholder`, whose `Display` is verbatim, so the
/// escaper never sees it. On re-parse the text is a perfectly ordinary single-quoted literal.
fn string_literal(s: &str) -> ast::Expr {
    value_expr(ast::Value::Placeholder(format!(
        "'{}'",
        s.replace('\'', "''")
    )))
}

fn parse_data_type(text: &str) -> Result<ast::DataType> {
    let dialect = BuilderDialect;
    let mut parser = Parser::new(&dialect)
        .try_with_sql(text)
        .map_err(|e| BuildError::UnparsableSql(format!("invalid cast type {text:?}: {e}")))?;
    let data_type = parser
        .parse_data_type()
        .map_err(|e| BuildError::UnparsableSql(format!("invalid cast type {text:?}: {e}")))?;
    // `parse_data_type` happily stops at the first valid token, so a string like "not a type"
    // parses as the custom type `not` with trailing garbage. Reject anything left over.
    if parser.peek_token().token != sqlparser::tokenizer::Token::EOF {
        return Err(BuildError::UnparsableSql(format!(
            "invalid cast type {text:?}: trailing tokens"
        )));
    }
    Ok(data_type)
}

// Binding tightness tiers (higher binds tighter), used to decide where to insert parentheses.
// `sqlparser`'s `Display` is purely structural — it never adds precedence parens — so the builder
// must wrap operands itself or a tree like `a / (b - c)` would render as the semantically different
// `a / b - c`.
const OR_PREC: u8 = 10;
const AND_PREC: u8 = 20;
const NOT_PREC: u8 = 30;
/// `IS [NOT] NULL`, `IN`, `BETWEEN`, `LIKE` and friends. Dialects disagree on where these sit
/// relative to comparisons (Postgres binds `LIKE` tighter than `=`, `GenericDialect` looser), so
/// they rank just below comparisons: always wrapped inside a comparison or arithmetic operand,
/// never wrapped under `AND` / `OR` / `NOT`.
const PREDICATE_PREC: u8 = 35;
const COMPARISON_PREC: u8 = 40;
/// Operators outside the builder's own set (`->>`, `@>`, bitwise, custom). Postgres binds these
/// tighter than comparisons and looser than arithmetic.
const OTHER_OP_PREC: u8 = 45;
const ADDITIVE_PREC: u8 = 50;
const MULTIPLICATIVE_PREC: u8 = 60;
const AT_TIME_ZONE_PREC: u8 = 65;
const PREFIX_PREC: u8 = 70;
const ATOM_PREC: u8 = u8::MAX;

fn binary_op_prec(op: BinaryOp) -> u8 {
    match op {
        BinaryOp::Or => OR_PREC,
        BinaryOp::And => AND_PREC,
        BinaryOp::Eq
        | BinaryOp::NotEq
        | BinaryOp::Lt
        | BinaryOp::LtEq
        | BinaryOp::Gt
        | BinaryOp::GtEq => COMPARISON_PREC,
        // JSONB key-exists operators return a boolean and are typically combined with AND/OR/NOT;
        // one comparison-level tier keeps `(a ? 'x') AND (b ? 'y')` and `NOT (a ? 'x')` grouped
        // correctly, which is all realistic usage needs.
        BinaryOp::JsonExists | BinaryOp::JsonExistsAny | BinaryOp::JsonExistsAll => COMPARISON_PREC,
        BinaryOp::Plus | BinaryOp::Minus | BinaryOp::StringConcat => ADDITIVE_PREC,
        BinaryOp::Multiply | BinaryOp::Divide | BinaryOp::Modulo => MULTIPLICATIVE_PREC,
    }
}

/// Binding tightness of an already-lowered expression.
///
/// This reads the `sqlparser` AST rather than the façade, because a `raw(...)` fragment is opaque
/// until it is parsed: `raw("a = 1 OR b = 2")` is an `OR` and must be wrapped like one, or
/// `raw("a = 1 OR b = 2") & c` renders as `a = 1 OR b = 2 AND c`. Anything not recognized as an
/// atom ranks lowest, so an unfamiliar node gets redundant parentheses rather than a wrong grouping.
fn ast_prec(expr: &ast::Expr) -> u8 {
    use ast::BinaryOperator as B;
    use ast::Expr as E;
    match expr {
        E::BinaryOp { op, .. } => match op {
            B::Or => OR_PREC,
            B::And => AND_PREC,
            B::Eq
            | B::NotEq
            | B::Lt
            | B::LtEq
            | B::Gt
            | B::GtEq
            | B::Spaceship
            | B::Question
            | B::QuestionAnd
            | B::QuestionPipe => COMPARISON_PREC,
            B::Plus | B::Minus | B::StringConcat => ADDITIVE_PREC,
            B::Multiply | B::Divide | B::Modulo => MULTIPLICATIVE_PREC,
            _ => OTHER_OP_PREC,
        },
        E::UnaryOp {
            op: ast::UnaryOperator::Not,
            ..
        }
        | E::Exists { negated: true, .. } => NOT_PREC,
        E::UnaryOp { .. } => PREFIX_PREC,
        E::IsFalse(_)
        | E::IsNotFalse(_)
        | E::IsTrue(_)
        | E::IsNotTrue(_)
        | E::IsNull(_)
        | E::IsNotNull(_)
        | E::IsUnknown(_)
        | E::IsNotUnknown(_)
        | E::IsDistinctFrom(..)
        | E::IsNotDistinctFrom(..)
        | E::IsNormalized { .. }
        | E::InList { .. }
        | E::InSubquery { .. }
        | E::InUnnest { .. }
        | E::Between { .. }
        | E::Like { .. }
        | E::ILike { .. }
        | E::SimilarTo { .. }
        | E::RLike { .. }
        | E::AnyOp { .. }
        | E::AllOp { .. }
        | E::MemberOf(_) => PREDICATE_PREC,
        E::AtTimeZone { .. } => AT_TIME_ZONE_PREC,
        E::Identifier(_)
        | E::CompoundIdentifier(_)
        | E::CompoundFieldAccess { .. }
        | E::JsonAccess { .. }
        | E::Value(_)
        | E::TypedString { .. }
        | E::Function(_)
        | E::Cast { .. }
        | E::Convert { .. }
        | E::Case { .. }
        | E::Nested(_)
        | E::Tuple(_)
        | E::Array(_)
        | E::Subquery(_)
        | E::Exists { negated: false, .. }
        | E::Interval(_)
        | E::Extract { .. }
        | E::Ceil { .. }
        | E::Floor { .. }
        | E::Position { .. }
        | E::Substring { .. }
        | E::Trim { .. }
        | E::Overlay { .. }
        | E::Collate { .. }
        | E::Struct { .. }
        | E::Map(_)
        | E::Dictionary(_) => ATOM_PREC,
        _ => 0,
    }
}

fn maybe_paren(expr: ast::Expr, wrap: bool) -> ast::Expr {
    if wrap {
        ast::Expr::Nested(Box::new(expr))
    } else {
        expr
    }
}

fn lower_binary_op(op: BinaryOp) -> ast::BinaryOperator {
    use ast::BinaryOperator as B;
    match op {
        BinaryOp::Eq => B::Eq,
        BinaryOp::NotEq => B::NotEq,
        BinaryOp::Lt => B::Lt,
        BinaryOp::LtEq => B::LtEq,
        BinaryOp::Gt => B::Gt,
        BinaryOp::GtEq => B::GtEq,
        BinaryOp::Plus => B::Plus,
        BinaryOp::Minus => B::Minus,
        BinaryOp::Multiply => B::Multiply,
        BinaryOp::Divide => B::Divide,
        BinaryOp::Modulo => B::Modulo,
        BinaryOp::And => B::And,
        BinaryOp::Or => B::Or,
        BinaryOp::StringConcat => B::StringConcat,
        BinaryOp::JsonExists => B::Question,
        BinaryOp::JsonExistsAny => B::QuestionPipe,
        BinaryOp::JsonExistsAll => B::QuestionAnd,
    }
}

fn lower_order_by_expr(sort: &SortExpr) -> Result<ast::OrderByExpr> {
    Ok(ast::OrderByExpr {
        expr: lower_expr(&sort.expr)?,
        options: ast::OrderByOptions {
            asc: Some(sort.asc),
            nulls_first: sort.nulls_first,
        },
        with_fill: None,
    })
}

fn lower_window(window: &Window) -> Result<ast::WindowType> {
    let partition_by = window
        .partition_by
        .iter()
        .map(lower_expr)
        .collect::<Result<Vec<_>>>()?;
    let order_by = window
        .order_by
        .iter()
        .map(lower_order_by_expr)
        .collect::<Result<Vec<_>>>()?;
    Ok(ast::WindowType::WindowSpec(ast::WindowSpec {
        window_name: None,
        partition_by,
        order_by,
        window_frame: None,
    }))
}

fn lower_call(call: &Call) -> Result<ast::Expr> {
    let args = if call.wildcard {
        vec![ast::FunctionArg::Unnamed(ast::FunctionArgExpr::Wildcard)]
    } else {
        call.args
            .iter()
            .map(|a| {
                Ok(ast::FunctionArg::Unnamed(ast::FunctionArgExpr::Expr(
                    lower_expr(a)?,
                )))
            })
            .collect::<Result<Vec<_>>>()?
    };

    let duplicate_treatment = call.distinct.then_some(ast::DuplicateTreatment::Distinct);

    let filter = match &call.filter {
        Some(f) => Some(Box::new(lower_expr(f)?)),
        None => None,
    };

    let over = match &call.over {
        Some(w) => Some(lower_window(w)?),
        None => None,
    };

    Ok(ast::Expr::Function(ast::Function {
        name: object_name(&call.name),
        uses_odbc_syntax: false,
        parameters: ast::FunctionArguments::None,
        args: ast::FunctionArguments::List(ast::FunctionArgumentList {
            duplicate_treatment,
            args,
            clauses: vec![],
        }),
        filter,
        null_treatment: None,
        over,
        within_group: vec![],
    }))
}

/// Lower an operand, and parenthesize it when its precedence is `<= wrap_at_or_below`.
fn lower_operand(expr: &Expr, wrap_at_or_below: u8) -> Result<ast::Expr> {
    let lowered = lower_expr(expr)?;
    let wrap = ast_prec(&lowered) <= wrap_at_or_below;
    Ok(maybe_paren(lowered, wrap))
}

fn lower_binary(left: &Expr, op: BinaryOp, right: &Expr) -> Result<ast::Expr> {
    let parent = binary_op_prec(op);
    // Left keeps its operator unwrapped while it binds at least as tight (left-associative); the
    // right operand is wrapped even at equal precedence, so `a - (b - c)` and `a / (b - c)` keep
    // their grouping.
    let left_ast = lower_operand(left, parent - 1)?;
    let right_ast = lower_operand(right, parent)?;
    Ok(ast::Expr::BinaryOp {
        left: Box::new(left_ast),
        op: lower_binary_op(op),
        right: Box::new(right_ast),
    })
}

fn lower_unary(op: UnaryOp, operand: &Expr) -> Result<ast::Expr> {
    let (parent, ast_op) = match op {
        UnaryOp::Not => (NOT_PREC, ast::UnaryOperator::Not),
        UnaryOp::Neg => (PREFIX_PREC, ast::UnaryOperator::Minus),
    };
    let lowered = lower_expr(operand)?;
    // A unary minus placed directly in front of an operand that renders with a leading `-` (a
    // negative literal, a nested negation, a `raw("-x")`) emits `--`, which DataFusion lexes as a
    // line comment that swallows the rest of the query.
    let wrap = ast_prec(&lowered) < parent
        || (matches!(op, UnaryOp::Neg) && lowered.to_string().starts_with('-'));
    Ok(ast::Expr::UnaryOp {
        op: ast_op,
        expr: Box::new(maybe_paren(lowered, wrap)),
    })
}

/// Lower a façade expression to a `sqlparser` expression. `Aliased` is handled by the caller in
/// projection position; anywhere else its alias is dropped (an alias is only meaningful there).
pub fn lower_expr(expr: &Expr) -> Result<ast::Expr> {
    Ok(match expr {
        Expr::Column { relation, name } => match relation {
            Some(rel) => ast::Expr::CompoundIdentifier(vec![ident(rel), ident(name)]),
            None => ast::Expr::Identifier(ident(name)),
        },
        Expr::Literal(scalar) => lower_scalar(scalar),
        Expr::Array(items) => ast::Expr::Array(ast::Array {
            elem: items.iter().map(lower_expr).collect::<Result<Vec<_>>>()?,
            named: true,
        }),
        Expr::Param(name) => value_expr(ast::Value::Placeholder(format!("${{{name}}}"))),
        Expr::Raw(sql) => parse_raw_expr(sql)?,
        Expr::Binary { left, op, right } => lower_binary(left, *op, right)?,
        Expr::Unary { op, expr } => lower_unary(*op, expr)?,
        // The operand of a predicate form is wrapped when it is itself a comparison or looser, so
        // `(a = b) IS NULL` and `(a OR b) IN (…)` keep their grouping in every dialect.
        Expr::IsNull { expr, negated } => {
            let inner = Box::new(lower_operand(expr, COMPARISON_PREC)?);
            if *negated {
                ast::Expr::IsNotNull(inner)
            } else {
                ast::Expr::IsNull(inner)
            }
        }
        Expr::InList {
            expr,
            list,
            negated,
        } => ast::Expr::InList {
            expr: Box::new(lower_operand(expr, COMPARISON_PREC)?),
            list: list.iter().map(lower_expr).collect::<Result<Vec<_>>>()?,
            negated: *negated,
        },
        Expr::InSubquery {
            expr,
            subquery,
            negated,
        } => ast::Expr::InSubquery {
            expr: Box::new(lower_operand(expr, COMPARISON_PREC)?),
            subquery: Box::new(lower_query(subquery)?),
            negated: *negated,
        },
        Expr::Between {
            expr,
            low,
            high,
            negated,
        } => ast::Expr::Between {
            expr: Box::new(lower_operand(expr, COMPARISON_PREC)?),
            negated: *negated,
            low: Box::new(lower_operand(low, COMPARISON_PREC)?),
            high: Box::new(lower_operand(high, COMPARISON_PREC)?),
        },
        Expr::Case {
            when_then,
            else_expr,
        } => ast::Expr::Case {
            case_token: ast::helpers::attached_token::AttachedToken::empty(),
            end_token: ast::helpers::attached_token::AttachedToken::empty(),
            operand: None,
            conditions: when_then
                .iter()
                .map(|(cond, result)| {
                    Ok(ast::CaseWhen {
                        condition: lower_expr(cond)?,
                        result: lower_expr(result)?,
                    })
                })
                .collect::<Result<Vec<_>>>()?,
            else_result: match else_expr {
                Some(e) => Some(Box::new(lower_expr(e)?)),
                None => None,
            },
        },
        Expr::Cast { expr, data_type } => ast::Expr::Cast {
            kind: ast::CastKind::Cast,
            expr: Box::new(lower_expr(expr)?),
            data_type: parse_data_type(data_type)?,
            array: false,
            format: None,
        },
        Expr::Function(call) => lower_call(call)?,
        // An alias outside projection position is meaningless SQL; render the inner expression.
        Expr::Aliased { expr, .. } => lower_expr(expr)?,
        Expr::ScalarSubquery(query) => ast::Expr::Subquery(Box::new(lower_query(query)?)),
    })
}

/// Parse a raw fragment into an expression so it composes with the rest of the AST.
///
/// `parse_expr` stops at the first token it can't continue on and returns the partial expression it
/// has so far — so a fragment like `attributes ? 'k'` parsed under a dialect that doesn't know `?`
/// would yield just `attributes`, silently dropping the rest. We parse with [`BuilderDialect`] (which
/// *does* understand the JSONB operators) and then assert the parser reached EOF, turning any
/// leftover tokens into a loud error instead of a truncated query. Mirrors [`parse_data_type`].
fn parse_raw_expr(sql: &str) -> Result<ast::Expr> {
    let dialect = BuilderDialect;
    let mut parser = Parser::new(&dialect)
        .try_with_sql(sql)
        .map_err(|e| BuildError::UnparsableSql(format!("invalid raw expression {sql:?}: {e}")))?;
    let expr = parser
        .parse_expr()
        .map_err(|e| BuildError::UnparsableSql(format!("invalid raw expression {sql:?}: {e}")))?;
    if parser.peek_token().token != sqlparser::tokenizer::Token::EOF {
        return Err(BuildError::UnparsableSql(format!(
            "invalid raw expression {sql:?}: unexpected trailing tokens"
        )));
    }
    Ok(expr)
}

fn lower_select_item(expr: &Expr) -> Result<ast::SelectItem> {
    match expr {
        Expr::Aliased { expr, alias } => Ok(ast::SelectItem::ExprWithAlias {
            expr: lower_expr(expr)?,
            alias: ident(alias),
        }),
        other => Ok(ast::SelectItem::UnnamedExpr(lower_expr(other)?)),
    }
}

fn lower_table_ref(table: &TableRef) -> Result<ast::TableFactor> {
    Ok(match table {
        TableRef::Named { name, alias } => ast::TableFactor::Table {
            name: object_name(name),
            alias: alias.as_deref().map(|a| table_alias(a, true)),
            args: None,
            with_hints: vec![],
            version: None,
            with_ordinality: false,
            partitions: vec![],
            json_path: None,
            sample: None,
            index_hints: vec![],
        },
        TableRef::Subquery { query, alias } => ast::TableFactor::Derived {
            lateral: false,
            subquery: Box::new(lower_query(query)?),
            alias: Some(table_alias(alias, true)),
            sample: None,
        },
    })
}

fn lower_join(join: &Join) -> Result<ast::Join> {
    let constraint = match &join.on {
        Some(on) => ast::JoinConstraint::On(lower_expr(on)?),
        None => ast::JoinConstraint::None,
    };
    let join_operator = match join.kind {
        JoinKind::Inner => ast::JoinOperator::Inner(constraint),
        JoinKind::Left => ast::JoinOperator::LeftOuter(constraint),
        JoinKind::Right => ast::JoinOperator::RightOuter(constraint),
        JoinKind::Full => ast::JoinOperator::FullOuter(constraint),
        JoinKind::Cross => ast::JoinOperator::CrossJoin(ast::JoinConstraint::None),
    };
    Ok(ast::Join {
        relation: lower_table_ref(&join.relation)?,
        global: false,
        join_operator,
    })
}

fn and_combine(filters: &[Expr]) -> Result<Option<ast::Expr>> {
    let mut iter = filters.iter();
    let Some(first) = iter.next() else {
        return Ok(None);
    };
    // A lone filter needs no parentheses. Once filters are AND-combined, each one that binds looser
    // than `AND` is wrapped, or `.filter(a | b).filter(c)` renders as `a OR b AND c`.
    if filters.len() == 1 {
        return Ok(Some(lower_expr(first)?));
    }
    let mut acc = lower_operand(first, AND_PREC - 1)?;
    for f in iter {
        acc = ast::Expr::BinaryOp {
            left: Box::new(acc),
            op: ast::BinaryOperator::And,
            right: Box::new(lower_operand(f, AND_PREC - 1)?),
        };
    }
    Ok(Some(acc))
}

fn lower_select(select: &Select) -> Result<ast::Select> {
    let projection = if select.projection.is_empty() {
        vec![ast::SelectItem::Wildcard(
            ast::WildcardAdditionalOptions::default(),
        )]
    } else {
        select
            .projection
            .iter()
            .map(lower_select_item)
            .collect::<Result<Vec<_>>>()?
    };

    let from = match &select.from {
        Some(table) => vec![ast::TableWithJoins {
            relation: lower_table_ref(table)?,
            joins: select
                .joins
                .iter()
                .map(lower_join)
                .collect::<Result<Vec<_>>>()?,
        }],
        None => {
            if !select.joins.is_empty() {
                return Err(BuildError::Misuse(
                    "cannot JOIN without a FROM source".into(),
                ));
            }
            vec![]
        }
    };

    let group_by = ast::GroupByExpr::Expressions(
        select
            .group_by
            .iter()
            .map(lower_expr)
            .collect::<Result<Vec<_>>>()?,
        vec![],
    );

    let having = match &select.having {
        Some(h) => Some(lower_expr(h)?),
        None => None,
    };

    Ok(ast::Select {
        select_token: ast::helpers::attached_token::AttachedToken::empty(),
        optimizer_hints: vec![],
        distinct: select.distinct.then_some(ast::Distinct::Distinct),
        select_modifiers: None,
        top: None,
        top_before_distinct: false,
        projection,
        exclude: None,
        into: None,
        from,
        lateral_views: vec![],
        prewhere: None,
        selection: and_combine(&select.filters)?,
        connect_by: vec![],
        group_by,
        cluster_by: vec![],
        distribute_by: vec![],
        sort_by: vec![],
        having,
        named_window: vec![],
        qualify: None,
        window_before_qualify: false,
        value_table_mode: None,
        flavor: ast::SelectFlavor::Standard,
    })
}

/// Lower a query body (SELECT or set operation) to a `SetExpr`. The enclosing query's own CTEs /
/// ORDER BY / LIMIT are handled by [`lower_query`], not here — so this never re-wraps the query it
/// belongs to.
fn lower_body(body: &Body) -> Result<ast::SetExpr> {
    match body {
        Body::Select(select) => Ok(ast::SetExpr::Select(Box::new(lower_select(select)?))),
        Body::SetOp {
            op,
            all,
            left,
            right,
        } => Ok(ast::SetExpr::SetOperation {
            op: lower_set_op(*op),
            set_quantifier: if *all {
                ast::SetQuantifier::All
            } else {
                ast::SetQuantifier::None
            },
            left: Box::new(operand_set_expr(left)?),
            right: Box::new(operand_set_expr(right)?),
        }),
    }
}

/// Whether a set-operation operand can be folded inline, or carries its own CTEs / ORDER BY /
/// LIMIT / OFFSET and must be wrapped in a derived subquery to preserve them.
fn is_simple(query: &Query) -> bool {
    query.ctes.is_empty()
        && query.order_by.is_empty()
        && query.limit.is_none()
        && query.offset.is_none()
}

/// Lower a set-operation operand, wrapping it as `SELECT * FROM (<query>) AS _q` only if it has
/// modifiers that a bare set-op arm can't carry.
fn operand_set_expr(query: &Query) -> Result<ast::SetExpr> {
    if is_simple(query) {
        lower_body(&query.body)
    } else {
        let derived = ast::TableFactor::Derived {
            lateral: false,
            subquery: Box::new(lower_query(query)?),
            alias: Some(table_alias("_q", true)),
            sample: None,
        };
        Ok(ast::SetExpr::Select(Box::new(wildcard_select(derived))))
    }
}

fn wildcard_select(relation: ast::TableFactor) -> ast::Select {
    ast::Select {
        select_token: ast::helpers::attached_token::AttachedToken::empty(),
        optimizer_hints: vec![],
        distinct: None,
        select_modifiers: None,
        top: None,
        top_before_distinct: false,
        projection: vec![ast::SelectItem::Wildcard(
            ast::WildcardAdditionalOptions::default(),
        )],
        exclude: None,
        into: None,
        from: vec![ast::TableWithJoins {
            relation,
            joins: vec![],
        }],
        lateral_views: vec![],
        prewhere: None,
        selection: None,
        connect_by: vec![],
        group_by: ast::GroupByExpr::Expressions(vec![], vec![]),
        cluster_by: vec![],
        distribute_by: vec![],
        sort_by: vec![],
        having: None,
        named_window: vec![],
        qualify: None,
        window_before_qualify: false,
        value_table_mode: None,
        flavor: ast::SelectFlavor::Standard,
    }
}

fn lower_set_op(op: SetOp) -> ast::SetOperator {
    match op {
        SetOp::Union => ast::SetOperator::Union,
        SetOp::Intersect => ast::SetOperator::Intersect,
        SetOp::Except => ast::SetOperator::Except,
    }
}

fn lower_cte(cte: &Cte) -> Result<ast::Cte> {
    Ok(ast::Cte {
        alias: table_alias(&cte.name, false),
        query: Box::new(lower_query(&cte.query)?),
        from: None,
        materialized: None,
        closing_paren_token: ast::helpers::attached_token::AttachedToken::empty(),
    })
}

/// Lower a complete façade query to a `sqlparser` query, ready for `.to_string()`.
pub fn lower_query(query: &Query) -> Result<ast::Query> {
    let with = if query.ctes.is_empty() {
        None
    } else {
        Some(ast::With {
            with_token: ast::helpers::attached_token::AttachedToken::empty(),
            recursive: query.recursive,
            cte_tables: query
                .ctes
                .iter()
                .map(lower_cte)
                .collect::<Result<Vec<_>>>()?,
        })
    };

    let order_by = if query.order_by.is_empty() {
        None
    } else {
        Some(ast::OrderBy {
            kind: ast::OrderByKind::Expressions(
                query
                    .order_by
                    .iter()
                    .map(lower_order_by_expr)
                    .collect::<Result<Vec<_>>>()?,
            ),
            interpolate: None,
        })
    };

    let limit_clause = if query.limit.is_some() || query.offset.is_some() {
        Some(ast::LimitClause::LimitOffset {
            limit: query.limit.map(|n| number(n.to_string())),
            offset: query.offset.map(|n| ast::Offset {
                value: number(n.to_string()),
                rows: ast::OffsetRows::None,
            }),
            limit_by: vec![],
        })
    } else {
        None
    };

    Ok(ast::Query {
        with,
        body: Box::new(lower_body(&query.body)?),
        order_by,
        limit_clause,
        fetch: None,
        locks: vec![],
        for_clause: None,
        settings: None,
        format_clause: None,
        pipe_operators: vec![],
    })
}

/// `Span`-free equality is what the round-trip validation in [`crate::render`] needs; expose a
/// helper so it doesn't reach into `sqlparser` either. Not currently used outside tests.
#[allow(dead_code)]
pub(crate) fn empty_span() -> Span {
    Span::empty()
}
