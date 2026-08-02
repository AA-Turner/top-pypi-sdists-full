//! Property-based tests that use **DataFusion itself as the oracle**.
//!
//! The crate's own `validate()` only proves a rendered query *re-parses* — a structural check
//! against a hand-maintained dialect. These tests go one layer deeper: they render to SQL and then
//! **plan and execute** it through real DataFusion, then read the value back. That upgrades "the
//! SQL is well-formed" to "the value survives a real engine round-trip" — the only check that
//! catches *silent* mis-encoding: an under-doubled quote that still parses but decodes wrong, a
//! float that lost its decimal point, a precedence bug that changes the computed result.
//!
//! Gated behind the `datafusion-oracle` feature (which pulls the optional `datafusion`/`tokio`
//! deps) so the default `cargo test` and the wheel build stay light. Run with:
//!   `cargo test --features datafusion-oracle --test properties`
#![cfg(feature = "datafusion-oracle")]

use std::sync::OnceLock;

use datafusion::arrow::datatypes::DataType;
use datafusion::prelude::SessionContext;
use datafusion::scalar::ScalarValue;
use proptest::prelude::*;

use datafusion_query_builder::expr::{BinaryOp, Expr, Scalar, UnaryOp};
use datafusion_query_builder::query::Query;
use datafusion_query_builder::to_sql;

/// One shared Tokio runtime: DataFusion's API is async, but every query here is a synchronous,
/// in-memory `SELECT <literal>` so `block_on` per case is fine.
fn runtime() -> &'static tokio::runtime::Runtime {
    static RT: OnceLock<tokio::runtime::Runtime> = OnceLock::new();
    RT.get_or_init(|| tokio::runtime::Runtime::new().expect("build tokio runtime"))
}

/// Render `SELECT <expr>` (no FROM), then plan + execute it through DataFusion and return the one
/// resulting cell. `Err` means the builder produced SQL DataFusion rejected — a builder bug for any
/// expression built from safe primitives (literals/arithmetic), since those should always be
/// representable.
fn eval_one(expr: Expr) -> Result<ScalarValue, String> {
    let query = Query::empty()
        .select(vec![expr])
        .expect("select on empty query");
    let sql = to_sql(&query).map_err(|e| format!("render: {e}"))?;
    runtime().block_on(async move {
        let ctx = SessionContext::new();
        let frame = ctx
            .sql(&sql)
            .await
            .map_err(|e| format!("plan: {e}\n  sql: {sql}"))?;
        let batches = frame
            .collect()
            .await
            .map_err(|e| format!("exec: {e}\n  sql: {sql}"))?;
        let batch = batches
            .first()
            .ok_or_else(|| format!("no rows\n  sql: {sql}"))?;
        ScalarValue::try_from_array(batch.column(0), 0)
            .map_err(|e| format!("extract: {e}\n  sql: {sql}"))
    })
}

/// The `ScalarValue` a faithful round-trip should yield for a façade literal.
fn expected(scalar: &Scalar) -> ScalarValue {
    match scalar {
        Scalar::Null => ScalarValue::Null,
        Scalar::Bool(b) => ScalarValue::Boolean(Some(*b)),
        Scalar::Int(i) => ScalarValue::Int64(Some(*i)),
        Scalar::Float(f) => ScalarValue::Float64(Some(*f)),
        Scalar::Str(s) => ScalarValue::Utf8(Some(s.clone())),
    }
}

/// Assert `lit(scalar)` round-trips: render -> execute -> read back -> equals the input value.
/// DataFusion is free to pick its own literal type (e.g. `Decimal128` for a fractional literal),
/// so we normalise by casting the result to the expected type before comparing — the question is
/// whether the *value* survived, not which physical type the engine chose.
fn check_round_trip(scalar: &Scalar) -> Result<(), String> {
    let actual = eval_one(Expr::lit(scalar.clone()))?;
    if matches!(scalar, Scalar::Null) {
        if actual.is_null() {
            return Ok(());
        }
        return Err(format!("expected NULL, got {actual:?}"));
    }
    let want = expected(scalar);
    let got = actual
        .cast_to(&want.data_type())
        .map_err(|e| format!("cast {actual:?} -> {:?}: {e}", want.data_type()))?;
    if got == want {
        Ok(())
    } else {
        Err(format!(
            "round-trip mismatch: built {scalar:?}, got back {got:?}"
        ))
    }
}

/// Adversarial free text. Heavily weighted toward the characters that break naive escapers, but
/// crucially does NOT exclude `'`, `\`, `\'`, or `''` — those are exactly the sequences the
/// app-layer tests had to filter out, and proving the library handles them is the whole point.
/// Only the NUL byte is excluded (a lower-layer concern, unrelated to quoting).
fn arb_text() -> impl Strategy<Value = String> {
    let ch = prop_oneof![
        5 => prop_oneof![Just('\''), Just('\\'), Just('"'), Just(';'), Just('-'), Just('/')],
        1 => any::<char>().prop_filter("no NUL", |c| *c != '\0'),
    ];
    proptest::collection::vec(ch, 0..40).prop_map(|cs| cs.into_iter().collect())
}

fn arb_scalar() -> impl Strategy<Value = Scalar> {
    prop_oneof![
        Just(Scalar::Null),
        any::<bool>().prop_map(Scalar::Bool),
        any::<i64>().prop_map(Scalar::Int),
        // Finite only: SQL has no literal syntax for NaN/Infinity (they need an explicit cast), so
        // they're out of scope for *literal* round-tripping. See `non_finite_floats_*` below.
        any::<f64>()
            .prop_filter("finite", |f| f.is_finite())
            .prop_map(Scalar::Float),
        arb_text().prop_map(Scalar::Str),
    ]
}

proptest! {
    // DataFusion-executing properties: keep the case count modest so the suite stays quick while
    // still exploring thousands of inputs across runs.
    #![proptest_config(ProptestConfig { cases: 96, ..ProptestConfig::default() })]

    /// THE headline property: any scalar built with `lit(x)` renders to SQL that DataFusion
    /// executes back to `x`. Covers string escaping (the `\'` / `''` class), float formatting
    /// (the decimal-point logic in `lower.rs`), i64 extremes, bool, and null — in one sweep.
    #[test]
    fn scalar_round_trips_through_datafusion(scalar in arb_scalar()) {
        check_round_trip(&scalar).map_err(TestCaseError::fail)?;
    }
}

/// Pinned regressions for the precise inputs that have bitten the builder (the bugs the host-metrics
/// PR had to exclude) plus the classic injection payloads. Kept as a fixed list so a failure names
/// the exact value, independent of proptest's shrinker.
#[test]
fn known_nasty_scalars_round_trip() {
    let nasties = [
        "\\'", // backslash-then-quote: rendered an unterminated literal pre-#25007
        "a\\'b",
        "''", // run of quotes: silently under-doubled pre-#25007
        "'''",
        "a''b",
        "O'Brien",                   // the ordinary apostrophe
        "'; DROP TABLE metrics; --", // injection payload — must come back as inert text
        "' OR '1'='1",
        "100%\\_test",
        "🔥 unicode 名前",
        "",
    ];
    for s in nasties {
        check_round_trip(&Scalar::Str(s.to_string()))
            .unwrap_or_else(|e| panic!("string literal {s:?} failed to round-trip: {e}"));
    }
    // Float edges that exercise the `lower.rs` decimal-point handling.
    for f in [
        0.0_f64,
        -0.0,
        0.1,
        1.0,
        1e-9,
        1e18,
        f64::MIN_POSITIVE,
        std::f64::consts::PI,
    ] {
        check_round_trip(&Scalar::Float(f))
            .unwrap_or_else(|e| panic!("float literal {f} failed to round-trip: {e}"));
    }
    // Integer edges (i64::MIN is asymmetric and a classic literal-parsing trap).
    for i in [0_i64, -1, i64::MAX, i64::MIN, i64::MIN + 1] {
        check_round_trip(&Scalar::Int(i))
            .unwrap_or_else(|e| panic!("int literal {i} failed to round-trip: {e}"));
    }
}

// ---- Arithmetic precedence, checked by execution -----------------------------------------------

fn arb_arith_op() -> impl Strategy<Value = BinaryOp> {
    prop_oneof![
        Just(BinaryOp::Plus),
        Just(BinaryOp::Minus),
        Just(BinaryOp::Multiply)
    ]
}

/// Arbitrary arithmetic trees over small integer leaves, using only `+ - *` and unary negation so
/// the result is exact (no division/NULL) and overflow is the only failure mode (handled below).
fn arb_arith() -> impl Strategy<Value = Expr> {
    let leaf = (-20i64..=20).prop_map(|n| Expr::lit(Scalar::Int(n)));
    leaf.prop_recursive(5, 40, 2, |inner| {
        prop_oneof![
            3 => (inner.clone(), arb_arith_op(), inner.clone())
                .prop_map(|(l, op, r)| l.binary(op, r)),
            1 => inner.prop_map(|e| Expr::unary(UnaryOp::Neg, e)),
        ]
    })
}

/// Evaluate the façade tree in Rust with i64 semantics. `None` on overflow at any step — exactly
/// the cases DataFusion would error on, which we then skip.
fn eval_int(expr: &Expr) -> Option<i64> {
    match expr {
        Expr::Literal(Scalar::Int(n)) => Some(*n),
        Expr::Unary {
            op: UnaryOp::Neg,
            expr,
        } => eval_int(expr)?.checked_neg(),
        Expr::Binary { left, op, right } => {
            let (l, r) = (eval_int(left)?, eval_int(right)?);
            match op {
                BinaryOp::Plus => l.checked_add(r),
                BinaryOp::Minus => l.checked_sub(r),
                BinaryOp::Multiply => l.checked_mul(r),
                _ => unreachable!("arb_arith only emits + - *"),
            }
        }
        _ => unreachable!("arb_arith only emits int leaves, neg, and + - *"),
    }
}

proptest! {
    #![proptest_config(ProptestConfig { cases: 96, ..ProptestConfig::default() })]

    /// The semantic precedence check: the rendered SQL must *compute the same value* as the tree it
    /// was built from. This catches a missing or misplaced paren — `a - (b - c)` collapsing to
    /// `a - b - c` — that a structural re-parse check could miss, by feeding it through a real
    /// evaluator. Far stronger than pinning a handful of hand-written precedence snapshots.
    #[test]
    fn arithmetic_precedence_matches_execution(expr in arb_arith()) {
        let Some(want) = eval_int(&expr) else {
            return Ok(()); // overflows i64 -> DataFusion would error too; out of scope.
        };
        let actual = eval_one(expr).map_err(TestCaseError::fail)?;
        let got = actual
            .cast_to(&DataType::Int64)
            .map_err(|e| TestCaseError::fail(e.to_string()))?;
        prop_assert_eq!(got, ScalarValue::Int64(Some(want)));
    }
}

// ---- Cheap, DataFusion-free structural properties ----------------------------------------------

fn arb_ident() -> impl Strategy<Value = String> {
    proptest::string::string_regex("[a-z][a-z0-9_]{0,5}").expect("valid identifier regex")
}

/// A broad expression generator (columns, params, raw fragments, casts, calls, predicates) used to
/// prove the builder is *total*: it must never panic, only ever return `Ok`/`Err`.
fn arb_expr() -> impl Strategy<Value = Expr> {
    let leaf = prop_oneof![
        arb_ident().prop_map(Expr::column),
        arb_scalar().prop_map(Expr::lit),
        arb_ident().prop_map(Expr::param),
        // Both well-formed and junk raw fragments, to exercise the parse-or-error escape hatch.
        prop_oneof![
            Just("a + 1"),
            Just("count(*)"),
            Just("!! not sql"),
            Just("")
        ]
        .prop_map(Expr::raw),
    ];
    leaf.prop_recursive(4, 48, 3, |inner| {
        prop_oneof![
            (inner.clone(), arb_arith_op(), inner.clone()).prop_map(|(l, op, r)| l.binary(op, r)),
            inner.clone().prop_map(|e| Expr::unary(UnaryOp::Not, e)),
            (inner.clone(), any::<bool>()).prop_map(|(e, n)| e.is_null(n)),
            (
                inner.clone(),
                proptest::collection::vec(inner.clone(), 0..4),
                any::<bool>()
            )
                .prop_map(|(e, list, n)| e.in_list(list, n)),
            // Cast types: a real one and a bogus one, to drive both branches of `parse_data_type`.
            (
                inner.clone(),
                prop_oneof![Just("Int64"), Just("text"), Just("not a type")]
            )
                .prop_map(|(e, t)| e.cast(t)),
            (arb_ident(), proptest::collection::vec(inner.clone(), 0..3))
                .prop_map(|(name, args)| datafusion_query_builder::functions::call(&name, args)),
        ]
    })
}

proptest! {
    /// Totality: rendering arbitrary expressions never panics. A panic in `lower.rs` (e.g. an
    /// `unreachable!`, a slice index, or a recursion-driven stack issue) would be a crash in a
    /// library that ingests user-controlled column/value/raw input — this asserts it always returns
    /// a `Result` instead.
    #[test]
    fn builder_never_panics_on_arbitrary_expr(expr in arb_expr()) {
        let query = Query::empty().select(vec![expr]).expect("select on empty query");
        let _ = to_sql(&query); // Ok or Err — just must not unwind.
    }

    /// Determinism: identical input renders byte-identical SQL (no set/hash ordering leaks).
    #[test]
    fn render_is_deterministic(scalar in arb_scalar()) {
        let build = || {
            let q = Query::empty()
                .select(vec![Expr::lit(scalar.clone())])
                .expect("select on empty query");
            to_sql(&q)
        };
        prop_assert_eq!(build(), build());
    }
}
