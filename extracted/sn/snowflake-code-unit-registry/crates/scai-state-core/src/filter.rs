//! SQL WHERE-clause filter for CodeUnit queries.
//!
//! Parses a SQL WHERE expression (Snowflake dialect) and evaluates it against
//! CodeUnit JSON values. Supports dot-notation field access, comparisons,
//! LIKE, IN, IS NULL/IS NOT NULL, AND/OR/NOT, and BETWEEN.
//!
//! # Examples
//!
//! ```ignore
//! let filter = Filter::parse("source.database = 'RETAIL_DB' AND objectType = 'table'")?;
//! let matches = filter.matches(&json_value);
//! ```

use serde_json::Value as JsonValue;
use sqlparser::ast::{BinaryOperator, Expr, Ident, UnaryOperator, Value};
use sqlparser::dialect::SnowflakeDialect;
use sqlparser::parser::Parser;

use crate::error::*;
use snafu::OptionExt;

/// A parsed SQL WHERE filter that can be evaluated against JSON values.
pub struct Filter {
    expr: Expr,
}

impl Filter {
    /// Parse a SQL WHERE expression string.
    ///
    /// The input should be a bare expression (no SELECT, no WHERE keyword),
    /// e.g. `"source.database = 'RETAIL_DB' AND objectType = 'table'"`.
    pub fn parse(filter: &str) -> Result<Self> {
        let sql = format!("SELECT * FROM _ WHERE {}", filter);
        let dialect = SnowflakeDialect {};

        let statements = Parser::parse_sql(&dialect, &sql).map_err(|e| {
            FilterSnafu {
                message: format!("Failed to parse filter expression: {e}"),
            }
            .build()
        })?;

        let statement = statements.into_iter().next().context(FilterSnafu {
            message: "Empty filter expression",
        })?;

        match statement {
            sqlparser::ast::Statement::Query(query) => {
                if let sqlparser::ast::SetExpr::Select(select) = *query.body {
                    select
                        .selection
                        .context(FilterSnafu {
                            message: "No WHERE clause found",
                        })
                        .map(|expr| Filter { expr })
                } else {
                    FilterSnafu {
                        message: "Unexpected query structure",
                    }
                    .fail()
                }
            }
            _ => FilterSnafu {
                message: "Unexpected statement type",
            }
            .fail(),
        }
    }

    /// Evaluate the filter against a JSON value.
    /// Returns true if the value matches the filter expression.
    pub fn matches(&self, value: &JsonValue) -> bool {
        eval_expr(&self.expr, value).is_truthy()
    }
}

/// Internal representation of an evaluated value during filter execution.
#[derive(Debug, Clone)]
enum EvalValue {
    String(String),
    Number(f64),
    Bool(bool),
    Null,
}

impl EvalValue {
    fn is_truthy(&self) -> bool {
        match self {
            EvalValue::Bool(b) => *b,
            EvalValue::Null => false,
            EvalValue::Number(n) => *n != 0.0,
            EvalValue::String(s) => !s.is_empty(),
        }
    }

    fn as_string(&self) -> Option<String> {
        match self {
            EvalValue::String(s) => Some(s.clone()),
            EvalValue::Number(n) => Some(n.to_string()),
            EvalValue::Bool(b) => Some(b.to_string()),
            EvalValue::Null => None,
        }
    }

    fn as_number(&self) -> Option<f64> {
        match self {
            EvalValue::Number(n) => Some(*n),
            EvalValue::String(s) => s.parse::<f64>().ok(),
            EvalValue::Bool(b) => Some(if *b { 1.0 } else { 0.0 }),
            EvalValue::Null => None,
        }
    }

    fn is_null(&self) -> bool {
        matches!(self, EvalValue::Null)
    }
}

impl From<&JsonValue> for EvalValue {
    fn from(v: &JsonValue) -> Self {
        match v {
            JsonValue::String(s) => EvalValue::String(s.clone()),
            JsonValue::Number(n) => EvalValue::Number(n.as_f64().unwrap_or(0.0)),
            JsonValue::Bool(b) => EvalValue::Bool(*b),
            JsonValue::Null => EvalValue::Null,
            // For objects/arrays, convert to their JSON string representation
            other => EvalValue::String(other.to_string()),
        }
    }
}

/// Resolve a dot-notation field path against a JSON value.
/// e.g. ["source", "database"] resolves `value["source"]["database"]`
fn resolve_path<'a>(value: &'a JsonValue, path: &[&str]) -> &'a JsonValue {
    let mut current = value;
    for segment in path {
        match current.get(*segment) {
            Some(v) => current = v,
            None => return &JsonValue::Null,
        }
    }
    current
}

/// Resolve an identifier (possibly compound) to a field path and look up its value.
fn resolve_ident(idents: &[Ident], value: &JsonValue) -> EvalValue {
    let path: Vec<&str> = idents.iter().map(|i| i.value.as_str()).collect();
    EvalValue::from(resolve_path(value, &path))
}

/// Evaluate a SQL expression against a JSON value, returning an EvalValue.
fn eval_expr(expr: &Expr, value: &JsonValue) -> EvalValue {
    match expr {
        // Single identifier: top-level field like `object_type`
        Expr::Identifier(ident) => {
            let path = [ident.value.as_str()];
            EvalValue::from(resolve_path(value, &path))
        }

        // Compound identifier: nested field like `source.database`
        Expr::CompoundIdentifier(idents) => resolve_ident(idents, value),

        // Literal value
        Expr::Value(v) => eval_literal(&v.value),

        // Parenthesized expression
        Expr::Nested(inner) => eval_expr(inner, value),

        // Binary operations: AND, OR, comparisons
        Expr::BinaryOp { left, op, right } => eval_binary_op(left, op, right, value),

        // Unary NOT
        Expr::UnaryOp {
            op: UnaryOperator::Not,
            expr: inner,
        } => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(!result.is_truthy())
        }

        // IS NULL
        Expr::IsNull(inner) => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(result.is_null())
        }

        // IS NOT NULL
        Expr::IsNotNull(inner) => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(!result.is_null())
        }

        // IN list: expr IN ('a', 'b', 'c')
        Expr::InList {
            expr: field,
            list,
            negated,
        } => {
            let field_val = eval_expr(field, value);
            if field_val.is_null() {
                return EvalValue::Bool(false);
            }

            let field_str = field_val.as_string();
            let found = list.iter().any(|item| {
                let item_val = eval_expr(item, value);
                match (&field_str, item_val.as_string()) {
                    (Some(f), Some(i)) => f == &i,
                    _ => false,
                }
            });

            EvalValue::Bool(if *negated { !found } else { found })
        }

        // LIKE pattern matching
        Expr::Like {
            negated,
            expr: field,
            pattern,
            escape_char: _,
            ..
        } => {
            let field_val = eval_expr(field, value);
            let pattern_val = eval_expr(pattern, value);

            let result = match (field_val.as_string(), pattern_val.as_string()) {
                (Some(f), Some(p)) => sql_like_match(&f, &p, false),
                _ => false,
            };

            EvalValue::Bool(if *negated { !result } else { result })
        }

        // ILIKE (case-insensitive LIKE)
        Expr::ILike {
            negated,
            expr: field,
            pattern,
            escape_char: _,
            ..
        } => {
            let field_val = eval_expr(field, value);
            let pattern_val = eval_expr(pattern, value);

            let result = match (field_val.as_string(), pattern_val.as_string()) {
                (Some(f), Some(p)) => sql_like_match(&f, &p, true),
                _ => false,
            };

            EvalValue::Bool(if *negated { !result } else { result })
        }

        // BETWEEN low AND high
        Expr::Between {
            expr: field,
            negated,
            low,
            high,
        } => {
            let field_val = eval_expr(field, value);
            let low_val = eval_expr(low, value);
            let high_val = eval_expr(high, value);

            let result = match (
                field_val.as_number(),
                low_val.as_number(),
                high_val.as_number(),
            ) {
                (Some(f), Some(l), Some(h)) => f >= l && f <= h,
                _ => {
                    // Fall back to string comparison
                    match (
                        field_val.as_string(),
                        low_val.as_string(),
                        high_val.as_string(),
                    ) {
                        (Some(f), Some(l), Some(h)) => f >= l && f <= h,
                        _ => false,
                    }
                }
            };

            EvalValue::Bool(if *negated { !result } else { result })
        }

        // IS TRUE / IS FALSE
        Expr::IsTrue(inner) => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(result.is_truthy())
        }
        Expr::IsFalse(inner) => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(!result.is_truthy())
        }
        Expr::IsNotTrue(inner) => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(!result.is_truthy())
        }
        Expr::IsNotFalse(inner) => {
            let result = eval_expr(inner, value);
            EvalValue::Bool(result.is_truthy())
        }

        // Unsupported expression types
        _ => EvalValue::Null,
    }
}

/// Evaluate a SQL literal value.
fn eval_literal(v: &Value) -> EvalValue {
    match v {
        Value::SingleQuotedString(s) => EvalValue::String(s.clone()),
        Value::DoubleQuotedString(s) => EvalValue::String(s.clone()),
        Value::Number(s, _) => match s.parse::<f64>() {
            Ok(n) => EvalValue::Number(n),
            Err(_) => EvalValue::String(s.clone()),
        },
        Value::Boolean(b) => EvalValue::Bool(*b),
        Value::Null => EvalValue::Null,
        // Treat other string literal types as strings
        Value::EscapedStringLiteral(s) => EvalValue::String(s.clone()),
        Value::NationalStringLiteral(s) => EvalValue::String(s.clone()),
        _ => EvalValue::Null,
    }
}

/// Evaluate a binary operation.
fn eval_binary_op(left: &Expr, op: &BinaryOperator, right: &Expr, value: &JsonValue) -> EvalValue {
    match op {
        // Boolean operators: short-circuit
        BinaryOperator::And => {
            let l = eval_expr(left, value);
            if !l.is_truthy() {
                return EvalValue::Bool(false);
            }
            let r = eval_expr(right, value);
            EvalValue::Bool(r.is_truthy())
        }
        BinaryOperator::Or => {
            let l = eval_expr(left, value);
            if l.is_truthy() {
                return EvalValue::Bool(true);
            }
            let r = eval_expr(right, value);
            EvalValue::Bool(r.is_truthy())
        }

        // Comparison operators
        BinaryOperator::Eq => {
            let l = eval_expr(left, value);
            let r = eval_expr(right, value);
            EvalValue::Bool(eval_compare(&l, &r) == Some(std::cmp::Ordering::Equal))
        }
        BinaryOperator::NotEq => {
            let l = eval_expr(left, value);
            let r = eval_expr(right, value);
            EvalValue::Bool(eval_compare(&l, &r) != Some(std::cmp::Ordering::Equal))
        }
        BinaryOperator::Lt => {
            let l = eval_expr(left, value);
            let r = eval_expr(right, value);
            EvalValue::Bool(eval_compare(&l, &r) == Some(std::cmp::Ordering::Less))
        }
        BinaryOperator::LtEq => {
            let l = eval_expr(left, value);
            let r = eval_expr(right, value);
            EvalValue::Bool(eval_compare(&l, &r).is_some_and(|o| o != std::cmp::Ordering::Greater))
        }
        BinaryOperator::Gt => {
            let l = eval_expr(left, value);
            let r = eval_expr(right, value);
            EvalValue::Bool(eval_compare(&l, &r) == Some(std::cmp::Ordering::Greater))
        }
        BinaryOperator::GtEq => {
            let l = eval_expr(left, value);
            let r = eval_expr(right, value);
            EvalValue::Bool(eval_compare(&l, &r).is_some_and(|o| o != std::cmp::Ordering::Less))
        }

        // Unsupported binary operator
        _ => EvalValue::Null,
    }
}

/// Compare two EvalValues using SQL-like comparison semantics.
/// Returns None if either value is null (SQL three-valued logic).
fn eval_compare(left: &EvalValue, right: &EvalValue) -> Option<std::cmp::Ordering> {
    if left.is_null() || right.is_null() {
        return None;
    }

    // Try numeric comparison first
    if let (Some(l), Some(r)) = (left.as_number(), right.as_number()) {
        return l.partial_cmp(&r);
    }

    // Fall back to string comparison
    match (left.as_string(), right.as_string()) {
        (Some(l), Some(r)) => Some(l.cmp(&r)),
        _ => None,
    }
}

/// SQL LIKE pattern matching.
/// `%` matches any sequence of characters, `_` matches exactly one character.
/// When `case_insensitive` is true, performs ILIKE matching.
fn sql_like_match(input: &str, pattern: &str, case_insensitive: bool) -> bool {
    let input = if case_insensitive {
        input.to_lowercase()
    } else {
        input.to_string()
    };
    let pattern = if case_insensitive {
        pattern.to_lowercase()
    } else {
        pattern.to_string()
    };

    like_match(&input, &pattern)
}

/// Recursive LIKE pattern matching on string slices (UTF-8 safe).
fn like_match(input: &str, pattern: &str) -> bool {
    if pattern.is_empty() {
        return input.is_empty();
    }

    let mut pattern_chars = pattern.chars();
    match pattern_chars.next().unwrap() {
        '%' => {
            // Skip consecutive '%'
            let rest_pattern: String = pattern_chars.collect();
            let rest_pattern = rest_pattern.trim_start_matches('%');

            // '%' at the end matches everything
            if rest_pattern.is_empty() {
                return true;
            }

            // Try matching rest_pattern at every character boundary in input
            let mut remaining = input;
            loop {
                if like_match(remaining, rest_pattern) {
                    return true;
                }
                // Advance by one character
                let mut chars = remaining.chars();
                if chars.next().is_none() {
                    break;
                }
                remaining = chars.as_str();
            }
            false
        }
        '_' => {
            // '_' matches exactly one character (any UTF-8 character)
            let mut chars = input.chars();
            if chars.next().is_none() {
                false
            } else {
                like_match(chars.as_str(), pattern_chars.as_str())
            }
        }
        c => {
            let mut input_chars = input.chars();
            match input_chars.next() {
                Some(ic) if ic == c => like_match(input_chars.as_str(), pattern_chars.as_str()),
                _ => false,
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    use test_case::test_case;

    fn sample_code_unit() -> JsonValue {
        json!({
            "id": "abc123",
            "kind": "databaseObject",
            "objectType": "table",
            "source": {
                "database": "RETAIL_DB",
                "schema": "dbo",
                "name": "Customer"
            },
            "target": {
                "database": "RETAIL",
                "schema": "DBO",
                "name": "CUSTOMER"
            },
            "codeStatus": {
                "registration": { "status": "completed", "sourceId": "primary" },
                "conversion": { "status": "pending" }
            },
            "issues": {
                "summary": {
                    "errors": 0,
                    "warnings": 2,
                    "blocking": false
                }
            },
            "planning": {
                "wave": 1,
                "waveRank": 3
            }
        })
    }

    #[test]
    fn test_simple_equality() {
        let filter = Filter::parse("objectType = 'table'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("objectType = 'view'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_nested_field() {
        let filter = Filter::parse("source.database = 'RETAIL_DB'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("source.schema = 'sales'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_deep_nested_field() {
        let filter = Filter::parse("codeStatus.conversion.status = 'pending'").unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_and() {
        let filter =
            Filter::parse("source.database = 'RETAIL_DB' AND target.schema = 'DBO'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter =
            Filter::parse("source.database = 'RETAIL_DB' AND target.schema = 'SALES'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_or() {
        let filter = Filter::parse("objectType = 'view' OR objectType = 'table'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("objectType = 'view' OR objectType = 'procedure'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_not() {
        let filter = Filter::parse("NOT objectType = 'view'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("NOT objectType = 'table'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_in_list() {
        let filter = Filter::parse("objectType IN ('table', 'view')").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("objectType IN ('view', 'procedure')").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_not_in() {
        let filter = Filter::parse("objectType NOT IN ('view', 'procedure')").unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_like() {
        let filter = Filter::parse("source.name LIKE 'Cust%'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("source.name LIKE '%omer'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("source.name LIKE 'Order%'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_like_underscore() {
        let filter = Filter::parse("source.schema LIKE 'db_'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("source.schema LIKE 'd__'").unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_ilike() {
        let filter = Filter::parse("source.name ILIKE 'customer'").unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_is_null() {
        let filter = Filter::parse("planning IS NOT NULL").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("planning IS NULL").unwrap();
        assert!(!filter.matches(&sample_code_unit()));

        // Non-existent field
        let filter = Filter::parse("nonexistent IS NULL").unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_numeric_comparison() {
        let filter = Filter::parse("issues.summary.errors = 0").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("issues.summary.warnings > 1").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("planning.wave <= 1").unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_between() {
        let filter = Filter::parse("planning.wave BETWEEN 1 AND 3").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("planning.wave BETWEEN 2 AND 5").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_boolean_field() {
        let filter = Filter::parse("issues.summary.blocking = FALSE").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("issues.summary.blocking = TRUE").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_complex_expression() {
        let filter = Filter::parse(
            "(source.database = 'RETAIL_DB' AND objectType = 'table') OR planning.wave > 5",
        )
        .unwrap();
        assert!(filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_not_equal() {
        let filter = Filter::parse("objectType != 'view'").unwrap();
        assert!(filter.matches(&sample_code_unit()));

        let filter = Filter::parse("objectType <> 'table'").unwrap();
        assert!(!filter.matches(&sample_code_unit()));
    }

    #[test]
    fn test_invalid_filter() {
        let result = Filter::parse("this is not valid sql !!!");
        assert!(result.is_err());
    }

    #[test_case("hello", "hello", false => true  ; "exact match")]
    #[test_case("hello", "hel%",  false => true  ; "prefix wildcard")]
    #[test_case("hello", "%llo",  false => true  ; "suffix wildcard")]
    #[test_case("hello", "%ell%", false => true  ; "infix wildcard")]
    #[test_case("hello", "h_llo", false => true  ; "single char wildcard")]
    #[test_case("hello", "%",     false => true  ; "match all")]
    #[test_case("hello", "world", false => false ; "no match")]
    #[test_case("hello", "h_lo",  false => false ; "underscore too short")]
    #[test_case("Hello", "hello", true  => true  ; "case insensitive exact")]
    #[test_case("HELLO", "hel%",  true  => true  ; "case insensitive prefix")]
    fn like_match(input: &str, pattern: &str, case_insensitive: bool) -> bool {
        sql_like_match(input, pattern, case_insensitive)
    }
}
