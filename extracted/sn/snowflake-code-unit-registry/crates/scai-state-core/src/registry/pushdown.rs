//! Predicate pushdown: translate registry query predicates into a
//! conservative [`Prefilter`] over the indexed fields.
//!
//! The contract (see [`super::storage::index`]) is **superset**: for every
//! regular document `d`, `predicate(d) ⇒ prefilter(d)`. Backends use the
//! prefilter only to pick candidates; the original predicate still runs on
//! each one. Dropping a condition is therefore always safe (it widens the
//! candidate set), while a prefilter that excludes a real match would be a
//! correctness bug. When nothing useful can be extracted the functions
//! return `None` (no pushdown).
//!
//! The translation mirrors the loose evaluation semantics of
//! [`crate::filter`] exactly where it emits a constraint, and refuses
//! (drops the constraint) everywhere else:
//!
//! - Comparisons convert both sides to numbers when both parse (`str::parse
//!   ::<f64>`, booleans as `1`/`0`), else compare string forms. A text field
//!   compared with a numeric-looking literal (`'01'`, `'1e3'`, `TRUE`, `1`)
//!   can therefore match many stored strings, so only the implied
//!   "is not null" is pushed down.
//! - `NULL <> x`, `NULL NOT LIKE p` and `NULL NOT BETWEEN a AND b` are
//!   **true** in this engine (while `NULL NOT IN (...)` is false), so those
//!   forms are never pushed down positively.
//! - Unsupported expressions (including unary minus: `-1` is not a literal
//!   to the filter engine) evaluate to NULL and are never translated.
//! - `IN` compares string forms (`3` is `"3"`, `TRUE` is `"true"`) with no
//!   numeric path, which makes string-literal lists on text fields exact.
//! - Wave values are compared as `f64`; bounds are pushed down only for
//!   finite literals with magnitude below 2^53, where `f64` comparison of an
//!   `i64` equals exact integer comparison.
//! - Boolean fields (`inScope`, `isMissing`; never NULL) are handled by
//!   evaluating the sub-expression for both possible values, so any
//!   combination of literals, comparisons, `IN`, `BETWEEN`, `NOT`,
//!   `AND`/`OR` over one such field alone translates exactly, in either
//!   polarity.
//! - `LIKE` / `ILIKE` are not translated.

use serde_json::Value as JsonValue;
use sqlparser::ast::{BinaryOperator, Expr, UnaryOperator, Value};

use super::storage::index::{Bound, FieldKind, IndexValue, IndexedField, Prefilter};
use crate::filter::Filter;

/// 2^53: integers of smaller magnitude are exactly representable as `f64`,
/// and no `i64` outside that range rounds to a value inside it.
const F64_EXACT_LIMIT: f64 = 9_007_199_254_740_992.0;

/// Translate a parsed filter into a conservative prefilter.
pub(super) fn from_filter(filter: &Filter) -> Option<Prefilter> {
    translate(filter.expr(), true).map(dedup_in_lists)
}

/// Translate a `find_by_object` partial into a conservative prefilter.
///
/// `matches_partial` requires every partial key to exist in the serialized
/// `CodeUnit` and every leaf to be JSON-equal, so a scalar leaf of the
/// field's own type at an indexed path is an exact equality.
pub(super) fn from_partial(partial: &JsonValue) -> Option<Prefilter> {
    let mut conjuncts = Vec::new();
    let mut path = Vec::new();
    walk_partial(partial, &mut path, &mut conjuncts);
    and(conjuncts.into_iter().map(Some))
}

fn walk_partial<'a>(value: &'a JsonValue, path: &mut Vec<&'a str>, out: &mut Vec<Prefilter>) {
    let JsonValue::Object(map) = value else {
        return;
    };
    for (key, child) in map {
        path.push(key.as_str());
        if let Some(field) = IndexedField::from_path(path.as_slice()) {
            if let Some(p) = partial_leaf(field, child) {
                out.push(p);
            }
        } else {
            walk_partial(child, path, out);
        }
        path.pop();
    }
}

/// Equality constraint for a partial leaf at an indexed path; `None` when the
/// leaf is not a plain scalar of the field's type (always safe to skip).
fn partial_leaf(field: IndexedField, leaf: &JsonValue) -> Option<Prefilter> {
    let value = match (field.kind(), leaf) {
        (FieldKind::Text, JsonValue::String(s)) => IndexValue::Text(s.clone()),
        // `as_i64` is `None` for floats (never equal to a serialized `i64`)
        // and for integers beyond `i64` (likewise never equal).
        (FieldKind::Integer, JsonValue::Number(n)) => IndexValue::Integer(n.as_i64()?),
        (FieldKind::Bool, JsonValue::Bool(b)) => IndexValue::Integer(i64::from(*b)),
        _ => return None,
    };
    Some(Prefilter::In(field, vec![value]))
}

// ── Filter expressions ───────────────────────────────────────────────────

/// Superset condition for the documents on which `truthy(expr) == pos`.
/// `None` means "no constraint" (everything is a candidate).
fn translate(expr: &Expr, pos: bool) -> Option<Prefilter> {
    if let Some((field, table)) = bool_table(expr) {
        return bool_set(field, table, pos);
    }
    match expr {
        Expr::Nested(inner) => translate(inner, pos),
        Expr::UnaryOp {
            op: UnaryOperator::Not,
            expr: inner,
        } => translate(inner, !pos),
        Expr::IsTrue(inner) | Expr::IsNotFalse(inner) => translate(inner, pos),
        Expr::IsFalse(inner) | Expr::IsNotTrue(inner) => translate(inner, !pos),
        Expr::BinaryOp {
            left,
            op: BinaryOperator::And,
            right,
        } => {
            if pos {
                and([translate(left, true), translate(right, true)])
            } else {
                or(translate(left, false), translate(right, false))
            }
        }
        Expr::BinaryOp {
            left,
            op: BinaryOperator::Or,
            right,
        } => {
            if pos {
                or(translate(left, true), translate(right, true))
            } else {
                and([translate(left, false), translate(right, false)])
            }
        }
        Expr::BinaryOp { left, op, right } => comparison(left, op, right, pos),
        // `IS [NOT] NULL` is total, so both polarities are exact.
        Expr::IsNull(inner) => null_test(field_of(inner)?, pos),
        Expr::IsNotNull(inner) => null_test(field_of(inner)?, !pos),
        Expr::InList {
            expr: inner,
            list,
            negated,
        } => {
            let field = field_of(inner)?;
            // A NULL field makes both `IN` and `NOT IN` false.
            match (*negated, pos) {
                (false, true) => in_list(field, list),
                (true, true) => null_test(field, false),
                (true, false) => or(null_test(field, true), in_list(field, list)),
                (false, false) => None,
            }
        }
        // A NULL field makes BETWEEN false and NOT BETWEEN true, so only "the
        // positive form holds" is pushed down. LIKE / ILIKE are deliberately
        // not translated.
        Expr::Between {
            expr: inner,
            negated,
            low,
            high,
        } if pos != *negated => between(field_of(inner)?, low, high),
        Expr::Identifier(_) | Expr::CompoundIdentifier(_) => bare_field(field_of(expr)?, pos),
        _ => None,
    }
}

/// Binary comparison operators (`AND`/`OR` handled by the caller).
fn comparison(left: &Expr, op: &BinaryOperator, right: &Expr, pos: bool) -> Option<Prefilter> {
    use BinaryOperator::*;
    // `a <> b` is false exactly when `a = b` holds; every other comparison is
    // false whenever either side is NULL, so only the positive form helps.
    let op = match (op, pos) {
        (Eq | Lt | LtEq | Gt | GtEq, true) => op.clone(),
        (NotEq, false) => Eq,
        _ => return None,
    };
    match (field_of(left), field_of(right)) {
        (Some(l), Some(r)) => and([null_test(l, false), null_test(r, false)]),
        (Some(field), None) => compare_with(field, &op, right),
        (None, Some(field)) => {
            let swapped = match op {
                Lt => Gt,
                LtEq => GtEq,
                Gt => Lt,
                GtEq => LtEq,
                other => other,
            };
            compare_with(field, &swapped, left)
        }
        (None, None) => None,
    }
}

/// `field <op> other`, where `op` is one of `=`, `<`, `<=`, `>`, `>=`.
fn compare_with(field: IndexedField, op: &BinaryOperator, other: &Expr) -> Option<Prefilter> {
    let Some(lit) = literal_of(other) else {
        // Any comparison with a NULL field is false.
        return null_test(field, false);
    };
    if lit.is_null() {
        return Some(false_());
    }
    match field.kind() {
        FieldKind::Text => match (&lit, lit.as_number()) {
            // A non-numeric string literal forces string comparison against
            // the (string) field value: exact.
            (Lit::Str(s), None) => Some(text_compare(field, op, s)),
            _ => null_test(field, false),
        },
        FieldKind::Integer => match lit.as_number() {
            Some(x) => wave_compare(field, op, x),
            None => null_test(field, false),
        },
        // Handled by `bool_table` when the other side is a literal.
        FieldKind::Bool => None,
    }
}

fn text_compare(field: IndexedField, op: &BinaryOperator, s: &str) -> Prefilter {
    let bound = |inclusive| {
        Some(Bound {
            value: IndexValue::Text(s.to_string()),
            inclusive,
        })
    };
    match op {
        BinaryOperator::Eq => Prefilter::In(field, vec![IndexValue::Text(s.to_string())]),
        BinaryOperator::Lt => range(field, None, bound(false)),
        BinaryOperator::LtEq => range(field, None, bound(true)),
        BinaryOperator::Gt => range(field, bound(false), None),
        BinaryOperator::GtEq => range(field, bound(true), None),
        _ => unreachable!("normalized comparison operator"),
    }
}

/// Integer field compared numerically with `x` (`f64(value) <op> x`).
fn wave_compare(field: IndexedField, op: &BinaryOperator, x: f64) -> Option<Prefilter> {
    if !exact_f64(x) {
        return null_test(field, false);
    }
    // For |x| < 2^53, `f64(w) <op> x` is equivalent to `w <op> x` exactly.
    let ceil = || Some(int_bound(x.ceil(), true));
    let floor = || Some(int_bound(x.floor(), true));
    Some(match op {
        BinaryOperator::Eq if x.fract() == 0.0 => {
            Prefilter::In(field, vec![IndexValue::Integer(x as i64)])
        }
        BinaryOperator::Eq => false_(),
        // w < x ⇔ w < ceil(x)
        BinaryOperator::Lt => range(field, None, Some(int_bound(x.ceil(), false))),
        BinaryOperator::LtEq => range(field, None, floor()),
        // w > x ⇔ w > floor(x)
        BinaryOperator::Gt => range(field, Some(int_bound(x.floor(), false)), None),
        BinaryOperator::GtEq => range(field, ceil(), None),
        _ => unreachable!("normalized comparison operator"),
    })
}

/// `field IN (items)` (the positive form).
fn in_list(field: IndexedField, items: &[Expr]) -> Option<Prefilter> {
    let Some(lits) = items.iter().map(literal_of).collect::<Option<Vec<_>>>() else {
        return null_test(field, false);
    };
    // Membership compares string forms; NULL items never match.
    let strings = lits.iter().filter_map(Lit::as_string);
    let values: Vec<IndexValue> = match field.kind() {
        FieldKind::Text => dedup(strings.map(IndexValue::Text)),
        FieldKind::Integer => {
            let mut values = Vec::new();
            for s in strings {
                match wave_matching_string(&s) {
                    WaveString::Matches(n) => values.push(IndexValue::Integer(n)),
                    WaveString::NoMatch => {}
                    WaveString::Unknown => return null_test(field, false),
                }
            }
            dedup(values.into_iter())
        }
        FieldKind::Bool => return None,
    };
    Some(in_or_false(field, values))
}

enum WaveString {
    /// Only this integer formats (as `f64`) to the string.
    Matches(i64),
    /// No integer formats to the string.
    NoMatch,
    /// Could match integers we cannot pin down exactly.
    Unknown,
}

/// Which `i64` wave values `w` satisfy `(w as f64).to_string() == s`.
fn wave_matching_string(s: &str) -> WaveString {
    // `f64` Display of an integral value is `-?[0-9]+` (never an exponent).
    let digits = s.strip_prefix('-').unwrap_or(s);
    if digits.is_empty() || !digits.bytes().all(|b| b.is_ascii_digit()) {
        return WaveString::NoMatch;
    }
    match s.parse::<i64>() {
        Ok(n) if (n as f64).abs() < F64_EXACT_LIMIT => {
            if (n as f64).to_string() == s {
                WaveString::Matches(n)
            } else {
                // Leading zeros, "-0": never produced by formatting.
                WaveString::NoMatch
            }
        }
        _ => WaveString::Unknown,
    }
}

/// `field BETWEEN low AND high` (the positive form).
fn between(field: IndexedField, low: &Expr, high: &Expr) -> Option<Prefilter> {
    let (Some(low), Some(high)) = (literal_of(low), literal_of(high)) else {
        return null_test(field, false);
    };
    match field.kind() {
        // A non-numeric bound forces string comparison: exact.
        FieldKind::Text if low.as_number().is_none() || high.as_number().is_none() => {
            match (low.as_string(), high.as_string()) {
                (Some(l), Some(h)) => Some(range(
                    field,
                    Some(Bound {
                        value: IndexValue::Text(l),
                        inclusive: true,
                    }),
                    Some(Bound {
                        value: IndexValue::Text(h),
                        inclusive: true,
                    }),
                )),
                _ => Some(false_()),
            }
        }
        FieldKind::Integer => match (low.as_number(), high.as_number()) {
            (Some(l), Some(h)) if exact_f64(l) && exact_f64(h) => Some(range(
                field,
                Some(int_bound(l.ceil(), true)),
                Some(int_bound(h.floor(), true)),
            )),
            _ => null_test(field, false),
        },
        FieldKind::Text | FieldKind::Bool => null_test(field, false),
    }
}

/// A bare field reference, truth-tested.
fn bare_field(field: IndexedField, pos: bool) -> Option<Prefilter> {
    match (field.kind(), pos) {
        // Truthy text = non-empty string, i.e. > ''.
        (FieldKind::Text, true) => Some(range(
            field,
            Some(Bound {
                value: IndexValue::Text(String::new()),
                inclusive: false,
            }),
            None,
        )),
        (FieldKind::Text, false) => or(
            null_test(field, true),
            Some(Prefilter::In(field, vec![IndexValue::Text(String::new())])),
        ),
        (FieldKind::Integer, true) => null_test(field, false),
        (FieldKind::Integer, false) => or(
            null_test(field, true),
            Some(Prefilter::In(field, vec![IndexValue::Integer(0)])),
        ),
        // Handled by `bool_table`.
        (FieldKind::Bool, _) => None,
    }
}

// ── Boolean fields: exhaustive evaluation over {false, true} ────────────

/// Truth of `expr` for the field being `false` and `true`, when `expr`
/// depends on nothing but one boolean indexed field (`inScope`,
/// `isMissing`) and literals. A literal-only expression has no field.
fn bool_table(expr: &Expr) -> Option<(Option<IndexedField>, [bool; 2])> {
    let mut field = None;
    let when_false = eval_bool_field(expr, false, &mut field)?.truthy();
    let when_true = eval_bool_field(expr, true, &mut field)?.truthy();
    Some((field, [when_false, when_true]))
}

fn bool_set(field: Option<IndexedField>, table: [bool; 2], pos: bool) -> Option<Prefilter> {
    match (table[0] == pos, table[1] == pos, field) {
        (true, true, _) => None,
        (false, false, _) => Some(false_()),
        (when_false, _, Some(field)) => {
            let value = IndexValue::Integer(if when_false { 0 } else { 1 });
            Some(Prefilter::In(field, vec![value]))
        }
        // A literal-only expression is constant.
        (_, _, None) => unreachable!("constant expression with a non-constant table"),
    }
}

/// Mirror of `filter::eval_expr` for the expressions whose only identifier
/// is a single boolean indexed field (bound to `value`); `None` for anything
/// else (including LIKE, which is not mirrored). Boolean indexed fields are
/// never NULL in a regular document.
fn eval_bool_field(expr: &Expr, value: bool, field: &mut Option<IndexedField>) -> Option<Lit> {
    use std::cmp::Ordering::*;
    use BinaryOperator::*;
    let mut eval = |e: &Expr| eval_bool_field(e, value, field);
    Some(match expr {
        Expr::Identifier(_) | Expr::CompoundIdentifier(_) => {
            let found = field_of(expr).filter(|f| f.kind() == FieldKind::Bool)?;
            match eval_field_binding(field, found) {
                true => Lit::Bool(value),
                false => return None,
            }
        }
        Expr::Value(v) => literal_value(&v.value)?,
        Expr::Nested(inner) => eval(inner)?,
        Expr::UnaryOp {
            op: UnaryOperator::Not,
            expr: inner,
        } => Lit::Bool(!eval(inner)?.truthy()),
        Expr::BinaryOp { left, op, right } => {
            let (l, r) = (eval(left)?, eval(right)?);
            let ord = || l.compare(&r);
            Lit::Bool(match op {
                And => l.truthy() && r.truthy(),
                Or => l.truthy() || r.truthy(),
                Eq => ord() == Some(Equal),
                NotEq => ord() != Some(Equal),
                Lt => ord() == Some(Less),
                LtEq => ord().is_some_and(|o| o != Greater),
                Gt => ord() == Some(Greater),
                GtEq => ord().is_some_and(|o| o != Less),
                _ => return None,
            })
        }
        Expr::IsNull(inner) => Lit::Bool(eval(inner)?.is_null()),
        Expr::IsNotNull(inner) => Lit::Bool(!eval(inner)?.is_null()),
        Expr::IsTrue(inner) | Expr::IsNotFalse(inner) => Lit::Bool(eval(inner)?.truthy()),
        Expr::IsFalse(inner) | Expr::IsNotTrue(inner) => Lit::Bool(!eval(inner)?.truthy()),
        Expr::InList {
            expr: inner,
            list,
            negated,
        } => {
            let subject = eval(inner)?;
            let items = list.iter().map(&mut eval).collect::<Option<Vec<_>>>()?;
            if subject.is_null() {
                Lit::Bool(false)
            } else {
                let subject = subject.as_string();
                let found = items.iter().any(|i| i.as_string() == subject);
                Lit::Bool(found != *negated)
            }
        }
        Expr::Between {
            expr: inner,
            negated,
            low,
            high,
        } => {
            let (f, l, h) = (eval(inner)?, eval(low)?, eval(high)?);
            let result = match (f.as_number(), l.as_number(), h.as_number()) {
                (Some(f), Some(l), Some(h)) => f >= l && f <= h,
                _ => match (f.as_string(), l.as_string(), h.as_string()) {
                    (Some(f), Some(l), Some(h)) => f >= l && f <= h,
                    _ => false,
                },
            };
            Lit::Bool(result != *negated)
        }
        _ => return None,
    })
}

/// Bind the expression's boolean field on first sight; `false` when a second,
/// different field appears.
fn eval_field_binding(bound: &mut Option<IndexedField>, found: IndexedField) -> bool {
    *bound.get_or_insert(found) == found
}

// ── Literals (mirror of `filter::EvalValue` for constants) ──────────────

#[derive(Debug, Clone)]
enum Lit {
    Str(String),
    Num(f64),
    Bool(bool),
    Null,
}

impl Lit {
    fn truthy(&self) -> bool {
        match self {
            Lit::Bool(b) => *b,
            Lit::Null => false,
            Lit::Num(n) => *n != 0.0,
            Lit::Str(s) => !s.is_empty(),
        }
    }

    fn as_string(&self) -> Option<String> {
        match self {
            Lit::Str(s) => Some(s.clone()),
            Lit::Num(n) => Some(n.to_string()),
            Lit::Bool(b) => Some(b.to_string()),
            Lit::Null => None,
        }
    }

    fn as_number(&self) -> Option<f64> {
        match self {
            Lit::Num(n) => Some(*n),
            Lit::Str(s) => s.parse::<f64>().ok(),
            Lit::Bool(b) => Some(if *b { 1.0 } else { 0.0 }),
            Lit::Null => None,
        }
    }

    fn is_null(&self) -> bool {
        matches!(self, Lit::Null)
    }

    fn compare(&self, other: &Lit) -> Option<std::cmp::Ordering> {
        if self.is_null() || other.is_null() {
            return None;
        }
        if let (Some(l), Some(r)) = (self.as_number(), other.as_number()) {
            return l.partial_cmp(&r);
        }
        Some(self.as_string()?.cmp(&other.as_string()?))
    }
}

/// Mirror of `filter::eval_literal`; `None` for literal kinds the filter
/// maps to NULL (treated as unknown here, which is always safe).
fn literal_value(value: &Value) -> Option<Lit> {
    Some(match value {
        Value::SingleQuotedString(s)
        | Value::DoubleQuotedString(s)
        | Value::EscapedStringLiteral(s)
        | Value::NationalStringLiteral(s) => Lit::Str(s.clone()),
        Value::Number(s, _) => match s.parse::<f64>() {
            Ok(n) => Lit::Num(n),
            Err(_) => Lit::Str(s.clone()),
        },
        Value::Boolean(b) => Lit::Bool(*b),
        Value::Null => Lit::Null,
        _ => return None,
    })
}

fn literal_of(expr: &Expr) -> Option<Lit> {
    match expr {
        Expr::Nested(inner) => literal_of(inner),
        Expr::Value(v) => literal_value(&v.value),
        _ => None,
    }
}

fn field_of(expr: &Expr) -> Option<IndexedField> {
    match expr {
        Expr::Nested(inner) => field_of(inner),
        Expr::Identifier(ident) => IndexedField::from_path(&[ident.value.as_str()]),
        Expr::CompoundIdentifier(idents) => {
            let path: Vec<&str> = idents.iter().map(|i| i.value.as_str()).collect();
            IndexedField::from_path(&path)
        }
        _ => None,
    }
}

// ── Prefilter construction ──────────────────────────────────────────────

/// The always-false prefilter (an empty `Or`).
fn false_() -> Prefilter {
    Prefilter::Or(Vec::new())
}

fn is_false(p: &Prefilter) -> bool {
    matches!(p, Prefilter::Or(v) if v.is_empty())
}

/// Fields whose indexed value is never NULL for a regular document.
fn never_null(field: IndexedField) -> bool {
    field.is_storage_key() || field.default_value().is_some()
}

/// `field IS NULL` (`want_null`) or `field IS NOT NULL`, folded for
/// never-null fields.
fn null_test(field: IndexedField, want_null: bool) -> Option<Prefilter> {
    match (never_null(field), want_null) {
        (true, true) => Some(false_()),
        (true, false) => None,
        (false, _) => Some(Prefilter::IsNull {
            field,
            negated: !want_null,
        }),
    }
}

fn range(field: IndexedField, low: Option<Bound>, high: Option<Bound>) -> Prefilter {
    Prefilter::Range { field, low, high }
}

/// Integer bound from an integral `f64` of magnitude below 2^53.
fn int_bound(x: f64, inclusive: bool) -> Bound {
    Bound {
        value: IndexValue::Integer(x as i64),
        inclusive,
    }
}

fn exact_f64(x: f64) -> bool {
    x.is_finite() && x.abs() < F64_EXACT_LIMIT
}

fn in_or_false(field: IndexedField, values: Vec<IndexValue>) -> Prefilter {
    if values.is_empty() {
        false_()
    } else {
        Prefilter::In(field, values)
    }
}

/// Drop repeated values, keeping first occurrences in order. Linear: `IN`
/// lists can carry tens of thousands of ids.
fn dedup(values: impl Iterator<Item = IndexValue>) -> Vec<IndexValue> {
    #[derive(PartialEq, Eq, Hash)]
    enum Key {
        Text(String),
        Integer(i64),
    }
    let mut seen = std::collections::HashSet::new();
    values
        .filter(|v| {
            seen.insert(match v {
                IndexValue::Text(s) => Key::Text(s.clone()),
                IndexValue::Integer(i) => Key::Integer(*i),
            })
        })
        .collect()
}

/// Remove repeated values from every `IN` list, in one linear pass.
fn dedup_in_lists(prefilter: Prefilter) -> Prefilter {
    match prefilter {
        Prefilter::In(field, values) => Prefilter::In(field, dedup(values.into_iter())),
        Prefilter::And(parts) => Prefilter::And(parts.into_iter().map(dedup_in_lists).collect()),
        Prefilter::Or(parts) => Prefilter::Or(parts.into_iter().map(dedup_in_lists).collect()),
        other => other,
    }
}

/// Conjunction; `None` operands (no constraint) are dropped.
fn and(parts: impl IntoIterator<Item = Option<Prefilter>>) -> Option<Prefilter> {
    let mut out = Vec::new();
    for part in parts.into_iter().flatten() {
        match part {
            p if is_false(&p) => return Some(false_()),
            Prefilter::And(inner) => out.extend(inner),
            p => out.push(p),
        }
    }
    match out.len() {
        0 => None,
        1 => out.pop(),
        _ => Some(Prefilter::And(out)),
    }
}

/// Disjunction; unconstrained if either side is. `IN` lists on the same
/// field are merged (`id = 'a' OR id = 'b'` becomes one `IN`).
fn or(a: Option<Prefilter>, b: Option<Prefilter>) -> Option<Prefilter> {
    let (a, b) = (a?, b?);
    let mut out: Vec<Prefilter> = Vec::new();
    for part in [a, b] {
        let parts = match part {
            Prefilter::Or(inner) => inner,
            p => vec![p],
        };
        for p in parts {
            match p {
                Prefilter::In(field, values) => {
                    let existing = out.iter_mut().find_map(|q| match q {
                        Prefilter::In(f, vs) if *f == field => Some(vs),
                        _ => None,
                    });
                    // Merged without checking for repeats (that would make
                    // long `OR` chains quadratic); `from_filter` dedups once.
                    match existing {
                        Some(vs) => vs.extend(values),
                        None => out.push(Prefilter::In(field, values)),
                    }
                }
                p => out.push(p),
            }
        }
    }
    match out.len() {
        0 => Some(false_()),
        1 => out.pop(),
        _ => Some(Prefilter::Or(out)),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::types::CodeUnit;
    use crate::registry::matches_partial;
    use serde_json::{json, Map};
    use std::cmp::Ordering;
    use IndexedField::*;

    // ── Helpers ──────────────────────────────────────────────────────────

    fn pf(filter: &str) -> Option<Prefilter> {
        from_filter(&Filter::parse(filter).expect("filter parses"))
    }

    fn text_in(field: IndexedField, values: &[&str]) -> Prefilter {
        Prefilter::In(
            field,
            values
                .iter()
                .map(|v| IndexValue::Text(v.to_string()))
                .collect(),
        )
    }

    fn int_in(field: IndexedField, values: &[i64]) -> Prefilter {
        Prefilter::In(
            field,
            values.iter().map(|v| IndexValue::Integer(*v)).collect(),
        )
    }

    fn not_null(field: IndexedField) -> Prefilter {
        Prefilter::IsNull {
            field,
            negated: true,
        }
    }

    fn is_null(field: IndexedField) -> Prefilter {
        Prefilter::IsNull {
            field,
            negated: false,
        }
    }

    fn text_bound(s: &str, inclusive: bool) -> Option<Bound> {
        Some(Bound {
            value: IndexValue::Text(s.to_string()),
            inclusive,
        })
    }

    fn int_bound_(n: i64, inclusive: bool) -> Option<Bound> {
        Some(Bound {
            value: IndexValue::Integer(n),
            inclusive,
        })
    }

    // ── Production filters ───────────────────────────────────────────────

    /// A 40k-id `IN` list (the MCP server sends id lists this long) must
    /// translate in linear time; the quadratic dedup took ~2 s optimized.
    #[test]
    fn large_id_in_list_translates_in_linear_time() {
        let ids: Vec<String> = (0..40_000)
            .map(|i| format!("'id-{}'", i % 30_000))
            .collect();
        let filter = Filter::parse(&format!("id IN ({})", ids.join(", "))).unwrap();
        let start = std::time::Instant::now();
        let prefilter = from_filter(&filter).unwrap();
        let elapsed = start.elapsed();
        match prefilter {
            Prefilter::In(Id, values) => assert_eq!(values.len(), 30_000, "deduplicated"),
            other => panic!("expected one IN on id, got {other:?}"),
        }
        assert!(
            elapsed < std::time::Duration::from_secs(1),
            "took {elapsed:?}"
        );
    }

    #[test]
    fn production_id_equality_and_large_in_list() {
        assert_eq!(pf("id = 'a1-b2'"), Some(text_in(Id, &["a1-b2"])));
        let ids: Vec<String> = (0..300).map(|i| format!("unit-{i:04}-x")).collect();
        let list = ids.iter().map(|i| format!("'{i}'")).collect::<Vec<_>>();
        let filter = format!("id IN ({})", list.join(", "));
        let refs: Vec<&str> = ids.iter().map(String::as_str).collect();
        assert_eq!(pf(&filter), Some(text_in(Id, &refs)));
        // Numeric-looking ids still translate in IN (string membership)...
        assert_eq!(pf("id IN ('1', '01')"), Some(text_in(Id, &["1", "01"])));
        // ...but not with `=` (numeric comparison: '01' = '1').
        assert_eq!(pf("id = '1'"), None);
    }

    #[test]
    fn production_in_scope_and_not_missing() {
        assert_eq!(
            pf("inScope = true AND isMissing = false"),
            Some(Prefilter::And(vec![
                int_in(InScope, &[1]),
                int_in(IsMissing, &[0])
            ]))
        );
    }

    #[test]
    fn production_kind_and_object_type() {
        assert_eq!(pf("kind = 'etl'"), Some(text_in(Kind, &["etl"])));
        assert_eq!(
            pf("source.objectType = 'table'"),
            Some(text_in(SourceObjectType, &["table"]))
        );
    }

    /// Exact shape of `build_name_filter` in SnowConvert's MCP server
    /// (`escape_quote` doubles single quotes).
    fn build_name_filter(canonical: &str, schema: Option<&str>, name: &str) -> String {
        let q = |s: &str| s.replace('\'', "''");
        let canonical = format!("source.canonicalName = '{}'", q(canonical));
        match schema {
            Some(s) => format!(
                "({canonical} OR (source.schema = '{}' AND source.name = '{}'))",
                q(s),
                q(name)
            ),
            None => format!("({canonical} OR source.name = '{}')", q(name)),
        }
    }

    #[test]
    fn production_name_filter() {
        assert_eq!(
            pf(&build_name_filter("dbo.O'Brien", Some("dbo"), "O'Brien")),
            Some(Prefilter::Or(vec![
                text_in(SourceCanonicalName, &["dbo.O'Brien"]),
                Prefilter::And(vec![
                    text_in(SourceSchema, &["dbo"]),
                    text_in(SourceName, &["O'Brien"]),
                ]),
            ]))
        );
        assert_eq!(
            pf(&build_name_filter("Customer", None, "Customer")),
            Some(Prefilter::Or(vec![
                text_in(SourceCanonicalName, &["Customer"]),
                text_in(SourceName, &["Customer"]),
            ]))
        );
        // A numeric-looking name only implies "is not null".
        assert_eq!(
            pf(&build_name_filter("123", None, "123")),
            Some(Prefilter::Or(vec![
                not_null(SourceCanonicalName),
                not_null(SourceName),
            ]))
        );
        // Combined with an id list, as the MCP server does.
        assert_eq!(
            pf(&format!(
                "(id IN ('a', 'b') OR {})",
                build_name_filter("db.s.n", Some("s"), "n")
            )),
            Some(Prefilter::Or(vec![
                text_in(Id, &["a", "b"]),
                text_in(SourceCanonicalName, &["db.s.n"]),
                Prefilter::And(vec![
                    text_in(SourceSchema, &["s"]),
                    text_in(SourceName, &["n"])
                ]),
            ]))
        );
    }

    #[test]
    fn top_level_canonical_name_is_not_the_source_field() {
        // `canonicalName` is not a top-level CodeUnit key: it evaluates as
        // NULL, so the filter matches nothing; it must not map to
        // `source.canonicalName`.
        assert_eq!(pf("canonicalName IN ('a', 'b')"), None);
        assert_eq!(pf("canonicalName = 'a'"), None);
    }

    #[test]
    fn like_and_ilike_stay_untranslated() {
        assert_eq!(pf("source.name LIKE 'Cust%'"), None);
        assert_eq!(pf("source.name ILIKE 'cust%'"), None);
        assert_eq!(pf("source.name NOT LIKE 'Cust%'"), None);
        assert_eq!(
            pf("kind = 'etl' AND source.name ILIKE '%x%'"),
            Some(text_in(Kind, &["etl"]))
        );
    }

    // ── Text fields ──────────────────────────────────────────────────────

    #[test]
    fn text_equality_rules() {
        assert_eq!(
            pf("'table' = source.objectType"),
            Some(text_in(SourceObjectType, &["table"]))
        );
        assert_eq!(
            pf("(source.database) = ('RETAIL')"),
            Some(text_in(SourceDatabase, &["RETAIL"]))
        );
        // Numeric-looking literals of any type only imply "not null".
        for lit in [
            "'01'", "'1e3'", "'inf'", "'NaN'", "'+3'", "'.5'", "1", "TRUE",
        ] {
            assert_eq!(
                pf(&format!("source.database = {lit}")),
                Some(not_null(SourceDatabase)),
                "{lit}"
            );
        }
        assert_eq!(pf("source.database = NULL"), Some(false_()));
        assert_eq!(
            pf("source.database = kind"),
            Some(Prefilter::And(vec![
                not_null(SourceDatabase),
                not_null(Kind),
            ]))
        );
        // `NULL <> x` is true in the filter engine.
        assert_eq!(pf("source.database <> 'x'"), None);
        assert_eq!(pf("source.database != 'x'"), None);
        assert_eq!(
            pf("NOT (source.database <> 'x')"),
            Some(text_in(SourceDatabase, &["x"]))
        );
        assert_eq!(pf("NOT source.database = 'x'"), None);
    }

    #[test]
    fn text_in_list_rules() {
        assert_eq!(
            pf("source.schema IN ('a', 1, 1e3, 2.50, TRUE, NULL, 'a')"),
            Some(text_in(SourceSchema, &["a", "1", "1000", "2.5", "true"]))
        );
        assert_eq!(pf("source.schema IN (NULL)"), Some(false_()));
        assert_eq!(
            pf("source.schema IN ('a', kind)"),
            Some(not_null(SourceSchema))
        );
        assert_eq!(
            pf("source.schema NOT IN ('a')"),
            Some(not_null(SourceSchema))
        );
        assert_eq!(
            pf("NOT source.schema NOT IN ('a')"),
            Some(Prefilter::Or(vec![
                is_null(SourceSchema),
                text_in(SourceSchema, &["a"])
            ]))
        );
        assert_eq!(pf("NOT source.schema IN ('a')"), None);
        assert_eq!(pf("id NOT IN ('a')"), None);
    }

    #[test]
    fn text_ranges_and_between() {
        assert_eq!(
            pf("source.schema < 'm'"),
            Some(range(SourceSchema, None, text_bound("m", false)))
        );
        assert_eq!(
            pf("'m' <= source.schema"),
            Some(range(SourceSchema, text_bound("m", true), None))
        );
        assert_eq!(pf("source.schema > '5'"), Some(not_null(SourceSchema)));
        assert_eq!(
            pf("source.schema BETWEEN 'a' AND 'c'"),
            Some(range(
                SourceSchema,
                text_bound("a", true),
                text_bound("c", true)
            ))
        );
        // One non-numeric bound forces string comparison.
        assert_eq!(
            pf("source.schema BETWEEN 1 AND 'c'"),
            Some(range(
                SourceSchema,
                text_bound("1", true),
                text_bound("c", true)
            ))
        );
        assert_eq!(
            pf("source.schema BETWEEN 1 AND 3"),
            Some(not_null(SourceSchema))
        );
        assert_eq!(pf("source.schema NOT BETWEEN 'a' AND 'c'"), None);
    }

    #[test]
    fn null_tests_and_bare_fields() {
        assert_eq!(pf("source.schema IS NULL"), Some(is_null(SourceSchema)));
        assert_eq!(
            pf("NOT source.schema IS NULL"),
            Some(not_null(SourceSchema))
        );
        assert_eq!(
            pf("source.schema IS NOT NULL"),
            Some(not_null(SourceSchema))
        );
        assert_eq!(pf("id IS NULL"), Some(false_()));
        assert_eq!(pf("id IS NOT NULL"), None);
        assert_eq!(pf("inScope IS NULL"), Some(false_()));
        assert_eq!(
            pf("source.database"),
            Some(range(SourceDatabase, text_bound("", false), None))
        );
        assert_eq!(
            pf("NOT source.database"),
            Some(Prefilter::Or(vec![
                is_null(SourceDatabase),
                text_in(SourceDatabase, &[""])
            ]))
        );
        assert_eq!(pf("planning.wave"), Some(not_null(Wave)));
        assert_eq!(
            pf("planning.wave IS FALSE"),
            Some(Prefilter::Or(vec![is_null(Wave), int_in(Wave, &[0])]))
        );
    }

    // ── Wave ─────────────────────────────────────────────────────────────

    #[test]
    fn wave_comparisons() {
        assert_eq!(pf("planning.wave = 3"), Some(int_in(Wave, &[3])));
        assert_eq!(pf("planning.wave = '3'"), Some(int_in(Wave, &[3])));
        assert_eq!(pf("planning.wave = '3e0'"), Some(int_in(Wave, &[3])));
        assert_eq!(pf("planning.wave = 3.0"), Some(int_in(Wave, &[3])));
        assert_eq!(pf("planning.wave = TRUE"), Some(int_in(Wave, &[1])));
        assert_eq!(pf("planning.wave = 2.5"), Some(false_()));
        assert_eq!(
            pf("planning.wave < 2.5"),
            Some(range(Wave, None, int_bound_(3, false)))
        );
        assert_eq!(
            pf("planning.wave <= 2.5"),
            Some(range(Wave, None, int_bound_(2, true)))
        );
        assert_eq!(
            pf("planning.wave > 2.5"),
            Some(range(Wave, int_bound_(2, false), None))
        );
        assert_eq!(
            pf("2.5 > planning.wave"),
            Some(range(Wave, None, int_bound_(3, false)))
        );
        assert_eq!(
            pf("planning.wave >= 2"),
            Some(range(Wave, int_bound_(2, true), None))
        );
        // Precision / non-finite / non-literal: only "not null".
        for lit in ["9007199254740992", "1e20", "'inf'", "'NaN'", "-1", "'abc'"] {
            assert_eq!(
                pf(&format!("planning.wave = {lit}")),
                Some(not_null(Wave)),
                "{lit}"
            );
        }
        assert_eq!(pf("planning.wave = '-1'"), Some(int_in(Wave, &[-1])));
        assert_eq!(pf("planning.wave <> 3"), None);
    }

    #[test]
    fn wave_in_and_between() {
        assert_eq!(
            pf("planning.wave IN (1, '2', '02', 3.0, 'x', TRUE, '-0', '-4')"),
            Some(int_in(Wave, &[1, 2, 3, -4]))
        );
        assert_eq!(pf("planning.wave IN ('02', 'x')"), Some(false_()));
        assert_eq!(
            pf("planning.wave IN (1, '9007199254740993')"),
            Some(not_null(Wave))
        );
        assert_eq!(
            pf("planning.wave IN ('99999999999999999999')"),
            Some(not_null(Wave))
        );
        assert_eq!(
            pf("planning.wave BETWEEN 0.5 AND '3'"),
            Some(range(Wave, int_bound_(1, true), int_bound_(3, true)))
        );
        assert_eq!(pf("planning.wave BETWEEN 1 AND 'x'"), Some(not_null(Wave)));
    }

    // ── Boolean fields ───────────────────────────────────────────────────

    #[test]
    fn boolean_field_forms() {
        let yes = Some(int_in(InScope, &[1]));
        let no = Some(int_in(InScope, &[0]));
        for f in [
            "inScope",
            "\"inScope\"",
            "inScope = true",
            "inScope = 1",
            "inScope = 'true'",
            "inScope = '1'",
            "inScope = '1e0'",
            "true = inScope",
            "inScope IS TRUE",
            "inScope IS NOT FALSE",
            "inScope <> false",
            "NOT inScope = false",
            "inScope IN ('true')",
            "inScope > 0",
            "inScope BETWEEN 1 AND 2",
            "NOT NOT inScope",
        ] {
            assert_eq!(pf(f), yes, "{f}");
        }
        for f in [
            "NOT inScope",
            "inScope = false",
            "inScope = 0",
            "inScope = 'false'",
            "inScope IS FALSE",
            "inScope IS NOT TRUE",
            "inScope NOT IN ('true', 1)",
        ] {
            assert_eq!(pf(f), no, "{f}");
        }
        // `IN` compares string forms: "true" is not "1".
        assert_eq!(pf("inScope IN (1)"), Some(false_()));
        assert_eq!(pf("inScope = 'yes'"), Some(false_()));
        assert_eq!(pf("inScope OR NOT inScope"), None);
        assert_eq!(pf("inScope OR TRUE"), None);
        assert_eq!(pf("1 = 0"), Some(false_()));
        assert_eq!(pf("isMissing"), Some(int_in(IsMissing, &[1])));
        assert_eq!(pf("NOT isMissing"), Some(int_in(IsMissing, &[0])));
        // Two different boolean fields: not tabulated.
        assert_eq!(pf("inScope = isMissing"), None);
        assert_eq!(
            pf("inScope AND NOT isMissing"),
            Some(Prefilter::And(vec![
                int_in(InScope, &[1]),
                int_in(IsMissing, &[0])
            ]))
        );
        // Case-sensitive keys.
        assert_eq!(pf("INSCOPE"), None);
        assert_eq!(pf("inscope = true"), None);
    }

    // ── Combinators ──────────────────────────────────────────────────────

    #[test]
    fn and_or_not_combinators() {
        assert_eq!(pf("source.name = 'x'"), Some(text_in(SourceName, &["x"])));
        assert_eq!(pf("extensions.foo = 'x'"), None);
        assert_eq!(
            pf("extensions.foo = 'x' AND source.schema = 's'"),
            Some(text_in(SourceSchema, &["s"]))
        );
        assert_eq!(pf("extensions.foo = 'x' OR source.schema = 's'"), None);
        assert_eq!(
            pf("id = 'a' OR id = 'b' OR id IN ('a', 'c')"),
            Some(text_in(Id, &["a", "b", "c"]))
        );
        assert_eq!(
            pf("NOT (source.schema IS NULL OR inScope = false)"),
            Some(Prefilter::And(vec![
                not_null(SourceSchema),
                int_in(InScope, &[1])
            ]))
        );
        assert_eq!(
            pf("NOT (source.schema IS NULL AND inScope)"),
            Some(Prefilter::Or(vec![
                not_null(SourceSchema),
                int_in(InScope, &[0])
            ]))
        );
        assert_eq!(pf("source.schema = 's' AND 1 = 0"), Some(false_()));
        assert_eq!(
            pf("source.schema = 's' OR 1 = 0"),
            Some(text_in(SourceSchema, &["s"]))
        );
        assert_eq!(
            pf("source.schema = 's' AND (TRUE)"),
            Some(text_in(SourceSchema, &["s"]))
        );
        assert_eq!(pf("source.schema = 's' OR TRUE"), None);
        // Unsupported expressions evaluate to NULL: untranslated.
        assert_eq!(pf("planning.wave + 1 = 3"), None);
    }

    // ── Partials ─────────────────────────────────────────────────────────

    #[test]
    fn partial_rules() {
        // Conjunct order follows the JSON map's key order; compare as sets.
        let conjuncts = |partial: JsonValue| {
            let mut parts = match from_partial(&partial) {
                Some(Prefilter::And(parts)) => parts,
                other => panic!("expected a conjunction, got {other:?}"),
            };
            parts.sort_by_key(|p| format!("{p:?}"));
            parts
        };
        let sorted = |mut parts: Vec<Prefilter>| {
            parts.sort_by_key(|p| format!("{p:?}"));
            parts
        };
        assert_eq!(
            conjuncts(json!({"source": {"objectType": "table", "name": "01"}})),
            sorted(vec![
                text_in(SourceObjectType, &["table"]),
                text_in(SourceName, &["01"]),
            ])
        );
        assert_eq!(
            conjuncts(json!({"inScope": false, "planning": {"wave": 3}, "id": "x"})),
            sorted(vec![
                int_in(InScope, &[0]),
                int_in(Wave, &[3]),
                text_in(Id, &["x"]),
            ])
        );
        assert_eq!(
            from_partial(&json!({"kind": "etl", "extensions": {"x": 1}})),
            Some(text_in(Kind, &["etl"]))
        );
        // Type mismatches, nulls, objects, floats: skipped.
        assert_eq!(
            from_partial(&json!({
                "source": {"database": 1, "schema": null, "name": {}},
                "planning": {"wave": 3.0},
                "inScope": "true",
                "extensions": {"x": 1},
            })),
            None
        );
        assert_eq!(from_partial(&json!("table")), None);
        assert_eq!(from_partial(&json!({})), None);
    }

    // ── Differential test ────────────────────────────────────────────────

    /// xorshift64* — deterministic, dependency-free.
    struct Rng(u64);

    impl Rng {
        fn next(&mut self) -> u64 {
            self.0 ^= self.0 >> 12;
            self.0 ^= self.0 << 25;
            self.0 ^= self.0 >> 27;
            self.0.wrapping_mul(0x2545_F491_4F6C_DD1D)
        }
        fn below(&mut self, n: usize) -> usize {
            (self.next() % n as u64) as usize
        }
        fn chance(&mut self, num: u64, den: u64) -> bool {
            self.next() % den < num
        }
        fn pick<'a, T>(&mut self, items: &'a [T]) -> &'a T {
            &items[self.below(items.len())]
        }
    }

    const IDS: &[&str] = &[
        "3f2a9c1e-0000-4000-8000-000000000001",
        "3f2a9c1e-0000-4000-8000-000000000002",
        "1e300000-aaaa-4000-8000-000000000003",
        "1",
        "01",
        "1e3",
        "unit_a",
        "abc",
    ];
    const KINDS: &[&str] = &["databaseObject", "script", "etl", "parameterizedReference"];
    const OBJECT_TYPES: &[&str] = &["table", "view", "procedure", "function", "macro"];
    const TEXTS: &[&str] = &[
        "RETAIL", "dbo", "01", "1", "1e3", "true", "false", "", "abc", "ab", "abd", "a%b", "NaN",
        "inf", "3", "-1", "1.0", "Ab", "é", "zz", "1000",
    ];
    const WAVES: &[i64] = &[
        0,
        1,
        2,
        3,
        10,
        -1,
        9_007_199_254_740_992,
        9_007_199_254_740_993,
        i64::MAX,
        i64::MIN,
    ];

    /// Random text value: absent (`None`), JSON null, or a string.
    fn gen_text(r: &mut Rng, domain: &[&str]) -> Option<JsonValue> {
        match r.below(10) {
            0..=2 => None,
            3 => Some(JsonValue::Null),
            _ => Some(json!(r.pick(domain))),
        }
    }

    fn insert(map: &mut Map<String, JsonValue>, key: &str, value: Option<JsonValue>) {
        if let Some(v) = value {
            map.insert(key.to_string(), v);
        }
    }

    /// A regular stored document (see `IndexedField`).
    fn gen_doc(r: &mut Rng) -> JsonValue {
        let mut doc = Map::new();
        doc.insert("id".into(), json!(r.pick(IDS)));
        if r.chance(3, 4) {
            doc.insert("kind".into(), json!(r.pick(KINDS)));
        }
        for side in ["source", "target"] {
            if r.chance(1, 6) {
                continue;
            }
            let mut m = Map::new();
            let ot = gen_text(r, OBJECT_TYPES).filter(|v| !v.is_null());
            insert(&mut m, "objectType", ot);
            insert(&mut m, "database", gen_text(r, TEXTS));
            insert(&mut m, "schema", gen_text(r, TEXTS));
            insert(&mut m, "name", gen_text(r, TEXTS));
            if side == "source" {
                insert(&mut m, "canonicalName", gen_text(r, TEXTS));
            }
            doc.insert(side.into(), JsonValue::Object(m));
        }
        match r.below(6) {
            0 => {}
            1 => {
                doc.insert("planning".into(), json!({}));
            }
            2 => {
                doc.insert("planning".into(), json!({"wave": null}));
            }
            _ => {
                doc.insert("planning".into(), json!({"wave": r.pick(WAVES)}));
            }
        }
        for key in ["inScope", "isMissing"] {
            match r.below(3) {
                0 => {}
                1 => {
                    doc.insert(key.into(), json!(true));
                }
                _ => {
                    doc.insert(key.into(), json!(false));
                }
            }
        }
        JsonValue::Object(doc)
    }

    /// What the predicate sees: stored JSON → `CodeUnit` → JSON.
    fn as_seen(doc: &JsonValue) -> JsonValue {
        let unit: CodeUnit = serde_json::from_value(doc.clone()).expect("valid CodeUnit");
        serde_json::to_value(unit).expect("serializes")
    }

    /// Indexed value of `field` for a regular stored document (`None` = NULL).
    fn indexed_value(field: IndexedField, doc: &JsonValue) -> Option<IndexValue> {
        let mut v = Some(doc);
        for seg in field.path() {
            v = v.and_then(|x| x.get(*seg));
        }
        match (field.kind(), v) {
            (_, None | Some(JsonValue::Null)) => field.default_value(),
            (FieldKind::Text, Some(JsonValue::String(s))) => Some(IndexValue::Text(s.clone())),
            (FieldKind::Integer, Some(JsonValue::Number(n))) => {
                Some(IndexValue::Integer(n.as_i64().expect("i64")))
            }
            (FieldKind::Bool, Some(JsonValue::Bool(b))) => Some(IndexValue::Integer(i64::from(*b))),
            (_, Some(other)) => panic!("irregular test document: {field:?} = {other}"),
        }
    }

    fn sql_cmp(a: &IndexValue, b: &IndexValue) -> Ordering {
        match (a, b) {
            (IndexValue::Text(a), IndexValue::Text(b)) => a.as_bytes().cmp(b.as_bytes()),
            (IndexValue::Integer(a), IndexValue::Integer(b)) => a.cmp(b),
            _ => panic!("mixed-type comparison {a:?} vs {b:?}"),
        }
    }

    /// Reference evaluation of a prefilter (SQL semantics over indexed values).
    fn eval(p: &Prefilter, doc: &JsonValue) -> bool {
        match p {
            Prefilter::And(ps) => ps.iter().all(|p| eval(p, doc)),
            Prefilter::Or(ps) => ps.iter().any(|p| eval(p, doc)),
            Prefilter::In(field, values) => indexed_value(*field, doc)
                .is_some_and(|v| values.iter().any(|x| sql_cmp(&v, x) == Ordering::Equal)),
            Prefilter::Range { field, low, high } => indexed_value(*field, doc).is_some_and(|v| {
                let ok = |b: &Option<Bound>, want: Ordering| {
                    b.as_ref().is_none_or(|b| {
                        let o = sql_cmp(&v, &b.value);
                        o == want || (b.inclusive && o == Ordering::Equal)
                    })
                };
                ok(low, Ordering::Greater) && ok(high, Ordering::Less)
            }),
            Prefilter::IsNull { field, negated } => {
                indexed_value(*field, doc).is_none() != *negated
            }
        }
    }

    /// Every operand has its field's type (no mixed comparisons in SQL).
    fn assert_well_typed(p: &Prefilter) {
        let check = |field: &IndexedField, v: &IndexValue| {
            let ok = matches!(
                (field.kind(), v),
                (FieldKind::Text, IndexValue::Text(_))
                    | (FieldKind::Integer | FieldKind::Bool, IndexValue::Integer(_))
            );
            assert!(ok, "ill-typed operand {v:?} for {field:?} in {p:?}");
        };
        match p {
            Prefilter::And(ps) | Prefilter::Or(ps) => ps.iter().for_each(assert_well_typed),
            Prefilter::In(f, vs) => vs.iter().for_each(|v| check(f, v)),
            Prefilter::Range { field, low, high } => {
                low.iter().chain(high).for_each(|b| check(field, &b.value))
            }
            Prefilter::IsNull { .. } => {}
        }
    }

    const INDEXED_REFS: &[&str] = &[
        "id",
        "kind",
        "source.objectType",
        "target.objectType",
        "source.database",
        "source.schema",
        "source.name",
        "source.canonicalName",
        "target.database",
        "target.schema",
        "planning.wave",
        "inScope",
        "isMissing",
        "(source.database)",
        "\"inScope\"",
        "planning.\"wave\"",
    ];
    const OTHER_REFS: &[&str] = &[
        "target.name",
        "canonicalName",
        "planning",
        "source",
        "nonexistent",
        "INSCOPE",
        "source.Database",
        "planning.waveRank",
    ];
    const NUMBERS: &[&str] = &[
        "0",
        "1",
        "2",
        "3",
        "10",
        "-1",
        "1.5",
        "2.5",
        "1e3",
        "3.0",
        "0.5",
        "9007199254740992",
        "9007199254740993",
        "9223372036854775807",
        "1e20",
        "-3.5",
    ];
    const EXTRA_STRINGS: &[&str] = &[
        "%", "a%", "t%", "_bo", "1%", "+3", ".5", "02", "-0", "1e0", "Infinity",
    ];

    fn gen_ref(r: &mut Rng) -> String {
        if r.chance(4, 5) {
            r.pick(INDEXED_REFS).to_string()
        } else {
            r.pick(OTHER_REFS).to_string()
        }
    }

    fn gen_lit(r: &mut Rng) -> String {
        match r.below(20) {
            0..=9 => {
                let domains: [&[&str]; 6] = [
                    TEXTS,
                    IDS,
                    OBJECT_TYPES,
                    KINDS,
                    EXTRA_STRINGS,
                    &["true", "false", "1"],
                ];
                {
                    let domain = *r.pick(&domains);
                    format!("'{}'", r.pick(domain))
                }
            }
            10..=16 => r.pick(NUMBERS).to_string(),
            17 => "TRUE".into(),
            18 => "FALSE".into(),
            _ => "NULL".into(),
        }
    }

    fn gen_operand(r: &mut Rng) -> String {
        if r.chance(1, 8) {
            gen_ref(r)
        } else {
            gen_lit(r)
        }
    }

    fn gen_list(r: &mut Rng, ids_only: bool) -> String {
        let n = 1 + r.below(if ids_only { 12 } else { 4 });
        (0..n)
            .map(|_| {
                if ids_only {
                    format!("'{}'", r.pick(IDS))
                } else {
                    gen_operand(r)
                }
            })
            .collect::<Vec<_>>()
            .join(", ")
    }

    fn gen_atom(r: &mut Rng) -> String {
        const CMP: &[&str] = &["=", "<>", "!=", "<", "<=", ">", ">="];
        let not = |r: &mut Rng| if r.chance(1, 3) { "NOT " } else { "" };
        match r.below(14) {
            0..=2 => format!("{} {} {}", gen_ref(r), r.pick(CMP), gen_operand(r)),
            3 => format!("{} {} {}", gen_lit(r), r.pick(CMP), gen_ref(r)),
            4 => format!("{} {} {}", gen_ref(r), r.pick(CMP), gen_ref(r)),
            5 => {
                let f = gen_ref(r);
                let n = not(r);
                format!("{f} {n}IN ({})", gen_list(r, false))
            }
            6 => {
                let n = not(r);
                format!("id {n}IN ({})", gen_list(r, true))
            }
            7 => {
                let f = gen_ref(r);
                let n = not(r);
                let op = if r.chance(1, 2) { "LIKE" } else { "ILIKE" };
                format!("{f} {n}{op} {}", gen_lit(r))
            }
            8 => {
                let f = gen_ref(r);
                let n = not(r);
                format!("{f} {n}BETWEEN {} AND {}", gen_lit(r), gen_lit(r))
            }
            9 => {
                let f = gen_ref(r);
                format!("{f} IS {}NULL", not(r))
            }
            10 => {
                let f = gen_ref(r);
                let n = not(r);
                let b = if r.chance(1, 2) { "TRUE" } else { "FALSE" };
                format!("{f} IS {n}{b}")
            }
            11 => gen_ref(r),
            12 => gen_lit(r),
            _ => {
                let s = r.pick(TEXTS);
                let c = r.pick(TEXTS);
                let n = *r.pick(TEXTS);
                build_name_filter(c, r.chance(1, 2).then_some(*s), n)
            }
        }
    }

    fn gen_expr(r: &mut Rng, depth: u32) -> String {
        if depth == 0 || r.chance(1, 3) {
            return gen_atom(r);
        }
        match r.below(6) {
            0 | 1 => format!("{} AND {}", gen_expr(r, depth - 1), gen_expr(r, depth - 1)),
            2 | 3 => format!("{} OR {}", gen_expr(r, depth - 1), gen_expr(r, depth - 1)),
            4 => format!("NOT {}", gen_expr(r, depth - 1)),
            _ => format!("({})", gen_expr(r, depth - 1)),
        }
    }

    fn doc_pool(seed: u64, n: usize) -> Vec<(JsonValue, JsonValue)> {
        let mut r = Rng(seed);
        (0..n)
            .map(|_| {
                let doc = gen_doc(&mut r);
                let seen = as_seen(&doc);
                (doc, seen)
            })
            .collect()
    }

    #[test]
    fn differential_filters_are_supersets() {
        let docs = doc_pool(0x5EED_D0C5, 200);
        let mut r = Rng(0x0F11_7E25);
        let (mut parsed, mut parse_errors, mut pushed, mut selective) = (0, 0, 0, 0);
        let (mut matched_pairs, mut candidate_pairs, mut checked_pairs) = (0u64, 0u64, 0u64);
        for _ in 0..20_000 {
            let text = gen_expr(&mut r, 3);
            let Ok(filter) = Filter::parse(&text) else {
                parse_errors += 1;
                continue;
            };
            parsed += 1;
            let Some(prefilter) = from_filter(&filter) else {
                continue;
            };
            pushed += 1;
            assert_well_typed(&prefilter);
            let mut candidates = 0;
            for (doc, seen) in &docs {
                let candidate = eval(&prefilter, doc);
                if filter.matches(seen) {
                    matched_pairs += 1;
                    assert!(
                        candidate,
                        "prefilter excludes a match\n filter: {text}\n prefilter: {prefilter:?}\n doc: {doc}"
                    );
                }
                candidates += usize::from(candidate);
            }
            checked_pairs += docs.len() as u64;
            candidate_pairs += candidates as u64;
            if candidates < docs.len() {
                selective += 1;
            }
        }
        let coverage = pushed as f64 / parsed as f64;
        println!(
            "filters: {parsed} parsed ({parse_errors} parse errors), {pushed} pushed down \
             ({:.1}%), {selective} selective on the pool; pairs: {checked_pairs} checked, \
             {matched_pairs} matching, {candidate_pairs} candidates",
            coverage * 100.0
        );
        assert!(
            parse_errors * 20 < parsed,
            "too many parse errors: {parse_errors}"
        );
        assert!(coverage > 0.3, "pushdown coverage too low: {coverage}");
        assert!(
            selective * 4 > pushed,
            "too few selective prefilters: {selective}"
        );
        assert!(
            matched_pairs > 10_000,
            "too few matching pairs: {matched_pairs}"
        );
    }

    /// Random partial: a few leaf paths, mostly copied from a pool document.
    fn gen_partial(r: &mut Rng, base: &JsonValue) -> JsonValue {
        const PATHS: &[&[&str]] = &[
            &["id"],
            &["kind"],
            &["source", "objectType"],
            &["source", "database"],
            &["source", "schema"],
            &["source", "name"],
            &["source", "canonicalName"],
            &["target", "objectType"],
            &["target", "database"],
            &["target", "schema"],
            &["planning", "wave"],
            &["inScope"],
            &["isMissing"],
            &["planning", "waveRank"],
            &["target", "name"],
        ];
        let mut partial = json!({});
        for _ in 0..1 + r.below(3) {
            let path = *r.pick(PATHS);
            let copied = path.iter().try_fold(base, |v, seg| v.get(*seg));
            let value = match (copied, r.below(4)) {
                (Some(v), 0..=2) => v.clone(),
                _ => match r.below(9) {
                    0 => json!(r.pick(TEXTS)),
                    1 => json!(r.pick(IDS)),
                    2 => json!(r.pick(WAVES)),
                    3 => json!(3.0),
                    4 => json!(r.chance(1, 2)),
                    5 => JsonValue::Null,
                    6 => json!({}),
                    7 => json!([]),
                    _ => json!(r.pick(OBJECT_TYPES)),
                },
            };
            let mut node = &mut partial;
            for seg in &path[..path.len() - 1] {
                if !node.get(*seg).is_some_and(JsonValue::is_object) {
                    node[*seg] = json!({});
                }
                node = &mut node[*seg];
            }
            node[path[path.len() - 1]] = value;
        }
        if r.chance(1, 20) {
            partial["source"] = json!({});
        }
        partial
    }

    #[test]
    fn differential_partials_are_supersets() {
        let docs = doc_pool(0xBA5E_D0C5, 300);
        let mut r = Rng(0x9A27_1A15);
        let (mut pushed, mut matched_pairs) = (0, 0u64);
        let total = 3000;
        for _ in 0..total {
            let base = &r.pick(&docs).1.clone();
            let partial = gen_partial(&mut r, base);
            let Some(prefilter) = from_partial(&partial) else {
                continue;
            };
            pushed += 1;
            assert_well_typed(&prefilter);
            for (doc, seen) in &docs {
                if matches_partial(&partial, seen) {
                    matched_pairs += 1;
                    assert!(
                        eval(&prefilter, doc),
                        "prefilter excludes a match\n partial: {partial}\n prefilter: {prefilter:?}\n doc: {doc}"
                    );
                }
            }
        }
        println!(
            "partials: {total} generated, {pushed} pushed down ({:.1}%), {matched_pairs} matching pairs",
            pushed as f64 * 100.0 / total as f64
        );
        assert!(pushed * 2 > total, "pushdown coverage too low: {pushed}");
        assert!(
            matched_pairs > 1000,
            "too few matching pairs: {matched_pairs}"
        );
    }
}
