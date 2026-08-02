//! Rendering tests built from real query shapes in our codebase (RED metrics, metrics
//! time-series, SLO burn-rate CTEs). Each renders, asserts the exact SQL via an inline snapshot,
//! and (where it goes through `validate`) confirms the SQL re-parses.

use insta::assert_snapshot;

use datafusion_query_builder::expr::{BinaryOp, Expr, Scalar, UnaryOp};
use datafusion_query_builder::functions::{call, count_star};
use datafusion_query_builder::query::{BuildError, JoinKind, Query, SetOp, TableRef};
use datafusion_query_builder::{to_sql, validate};

fn lit_str(s: &str) -> Expr {
    Expr::lit(Scalar::Str(s.into()))
}

fn eq(col: &str, val: &str) -> Expr {
    Expr::column(col).binary(BinaryOp::Eq, lit_str(val))
}

#[test]
fn red_metrics_query() {
    let q = Query::table("records")
        .filter(eq("kind", "span"))
        .unwrap()
        .select(vec![
            call(
                "coalesce",
                vec![Expr::column("service_name"), lit_str("(unknown)")],
            )
            .alias("service"),
            call("approx_distinct", vec![Expr::column("trace_id")]).alias("request_count"),
            call(
                "approx_percentile_cont",
                vec![Expr::column("duration"), Expr::lit(Scalar::Float(0.95))],
            )
            .alias("p95"),
        ])
        .unwrap()
        .group_by(vec![Expr::column("service_name")])
        .unwrap()
        .order_by(vec![Expr::column("request_count").sort(false, None)])
        .limit(200);

    assert_snapshot!(validate(&q).unwrap(), @"SELECT coalesce(service_name, '(unknown)') AS service, approx_distinct(trace_id) AS request_count, approx_percentile_cont(duration, 0.95) AS p95 FROM records WHERE kind = 'span' GROUP BY service_name ORDER BY request_count DESC LIMIT 200");
}

#[test]
fn metrics_time_series_with_param() {
    // SELECT time_bucket('${resolution}', recorded_timestamp) AS time,
    //        metric_quantile(0.99, value) AS value
    // FROM metrics WHERE metric_name = '...' GROUP BY time ORDER BY time
    let q = Query::table("metrics")
        .filter(eq("metric_name", "http.server.duration"))
        .unwrap()
        .select(vec![
            call(
                "time_bucket",
                vec![
                    Expr::param("resolution"),
                    Expr::column("recorded_timestamp"),
                ],
            )
            .alias("time"),
            call(
                "metric_quantile",
                vec![Expr::lit(Scalar::Float(0.99)), Expr::column("value")],
            )
            .alias("value"),
        ])
        .unwrap()
        .group_by(vec![Expr::column("time")])
        .unwrap()
        .order_by(vec![Expr::column("time").sort(true, None)]);

    assert_snapshot!(validate(&q).unwrap(), @"SELECT time_bucket(${resolution}, recorded_timestamp) AS time, metric_quantile(0.99, value) AS value FROM metrics WHERE metric_name = 'http.server.duration' GROUP BY time ORDER BY time ASC");
}

#[test]
fn count_distinct_filter_and_in_list() {
    let q = Query::table("records")
        .select(vec![count_star().alias("total"), {
            // count(*) FILTER (WHERE is_exception)
            let mut c = count_star();
            if let Expr::Function(call) = &mut c {
                call.filter = Some(Box::new(Expr::column("is_exception")));
            }
            c.alias("errors")
        }])
        .unwrap()
        .filter(
            Expr::column("deployment_environment")
                .in_list(vec![lit_str("prod"), lit_str("staging")], false),
        )
        .unwrap();

    assert_snapshot!(validate(&q).unwrap(), @"SELECT count(*) AS total, count(*) FILTER (WHERE is_exception) AS errors FROM records WHERE deployment_environment IN ('prod', 'staging')");
}

#[test]
fn slo_burn_rate_ctes_cross_join() {
    // Two windowed burn-rate CTEs cross-joined — the SLO query shape.
    fn window_cte(env_secs: &str) -> Query {
        Query::table("records")
            .filter(eq("service_name", "my-service"))
            .unwrap()
            .filter(Expr::column("start_timestamp").binary(
                BinaryOp::Gt,
                Expr::raw(format!("now() - INTERVAL '{env_secs}'")),
            ))
            .unwrap()
            .select(vec![
                call(
                    "round",
                    vec![
                        call("avg", vec![Expr::column("bad")]),
                        Expr::lit(Scalar::Int(2)),
                    ],
                )
                .alias("burn_rate"),
            ])
            .unwrap()
    }

    let q = Query::table("long_window")
        .with_cte("long_window", window_cte("1 hour"))
        .with_cte("short_window", window_cte("5 minutes"))
        .join(
            TableRef::Named {
                name: "short_window".into(),
                alias: None,
            },
            JoinKind::Cross,
            None,
        )
        .unwrap()
        .select(vec![
            Expr::qualified_column("long_window", "burn_rate").alias("long_burn"),
            Expr::qualified_column("short_window", "burn_rate").alias("short_burn"),
        ])
        .unwrap();

    assert_snapshot!(validate(&q).unwrap(), @"WITH long_window AS (SELECT round(avg(bad), 2) AS burn_rate FROM records WHERE service_name = 'my-service' AND start_timestamp > now() - INTERVAL '1 hour'), short_window AS (SELECT round(avg(bad), 2) AS burn_rate FROM records WHERE service_name = 'my-service' AND start_timestamp > now() - INTERVAL '5 minutes') SELECT long_window.burn_rate AS long_burn, short_window.burn_rate AS short_burn FROM long_window CROSS JOIN short_window");
}

#[test]
fn union_all_distinct_keys() {
    let attr = Query::table("metrics")
        .select(vec![
            call("json_keys", vec![Expr::column("attributes")]).alias("key"),
        ])
        .unwrap();
    let resource = Query::table("metrics")
        .select(vec![
            call("json_keys", vec![Expr::column("otel_resource_attributes")]).alias("key"),
        ])
        .unwrap();

    let q = attr.set_op(SetOp::Union, true, resource).limit(100);
    assert_snapshot!(validate(&q).unwrap(), @"SELECT json_keys(attributes) AS key FROM metrics UNION ALL SELECT json_keys(otel_resource_attributes) AS key FROM metrics LIMIT 100");
}

#[test]
fn defaults_to_select_star() {
    let q = Query::table("records").limit(10);
    assert_snapshot!(to_sql(&q).unwrap(), @"SELECT * FROM records LIMIT 10");
}

#[test]
fn precedence_parens_preserve_grouping() {
    // `sqlparser` Display adds no precedence parens, so the builder must. A burn-rate-shaped
    // expression: bad / total / (1 - goal) must NOT collapse to `bad / total / 1 - goal`.
    let bad = Expr::column("bad");
    let total = call(
        "nullif",
        vec![Expr::column("total"), Expr::lit(Scalar::Int(0))],
    );
    let goal =
        Expr::lit(Scalar::Float(1.0)).binary(BinaryOp::Minus, Expr::lit(Scalar::Float(0.99)));
    let ratio = bad
        .binary(BinaryOp::Divide, total)
        .binary(BinaryOp::Divide, goal);
    let q = Query::table("t").select(vec![ratio.alias("burn")]).unwrap();
    assert_snapshot!(to_sql(&q).unwrap(), @"SELECT bad / nullif(total, 0) / (1.0 - 0.99) AS burn FROM t");

    // NOT over a disjunction, and negation of a sum, both need parens.
    let not_expr = Expr::unary(
        UnaryOp::Not,
        Expr::column("a").binary(BinaryOp::Or, Expr::column("b")),
    );
    let neg_sum = Expr::unary(
        UnaryOp::Neg,
        Expr::column("x").binary(BinaryOp::Plus, Expr::column("y")),
    );
    let q2 = Query::table("t")
        .select(vec![not_expr.alias("n"), neg_sum.alias("m")])
        .unwrap();
    assert_snapshot!(to_sql(&q2).unwrap(), @"SELECT NOT (a OR b) AS n, -(x + y) AS m FROM t");
}

#[test]
fn negation_of_negative_literal_does_not_emit_comment_token() {
    // Regression (found by the DataFusion round-trip property test): a unary minus directly in
    // front of a negative literal rendered `--1`, which DataFusion lexes as a line comment that
    // swallows the rest of the query. The operand must be parenthesized.
    let q = Query::table("t")
        .select(vec![
            Expr::unary(UnaryOp::Neg, Expr::lit(Scalar::Int(-1))).alias("a"),
            Expr::column("x")
                .binary(
                    BinaryOp::Plus,
                    Expr::unary(UnaryOp::Neg, Expr::lit(Scalar::Float(-1.5))),
                )
                .alias("b"),
        ])
        .unwrap();
    assert_snapshot!(validate(&q).unwrap(), @"SELECT -(-1) AS a, x + -(-1.5) AS b FROM t");
}

#[test]
fn invalid_raw_fragment_is_rejected() {
    let q = Query::table("t")
        .filter(Expr::raw("this is not && valid sql"))
        .unwrap();
    assert!(to_sql(&q).is_err());
}

#[test]
fn raw_json_key_exists_no_longer_truncates() {
    // Regression: `raw("attributes ? '...'")` used to render as just `attributes` — the JSONB `?`
    // key-exists operator was silently dropped because the raw fragment was parsed with a dialect
    // that tokenized `?` as a prepared-statement placeholder and `parse_expr` stopped early. It now
    // parses (and re-parses) faithfully.
    let q = Query::table("records")
        .select(vec![
            Expr::raw("attributes ? 'gen_ai.input.messages'").alias("x"),
        ])
        .unwrap();
    assert_snapshot!(
        validate(&q).unwrap(),
        @"SELECT attributes ? 'gen_ai.input.messages' AS x FROM records"
    );
}

#[test]
fn raw_fragment_with_trailing_tokens_is_rejected() {
    // The other half of the truncation bug: a fragment that parses a valid leading expression but
    // leaves tokens behind must error, not silently keep only the prefix. Pre-fix `1 + 1 oops`
    // rendered as `1 + 1`.
    let q = Query::table("t")
        .select(vec![Expr::raw("1 + 1 oops").alias("x")])
        .unwrap();
    let err = to_sql(&q).unwrap_err();
    assert!(
        matches!(&err, BuildError::UnparsableSql(m) if m.contains("trailing")),
        "unexpected error: {err:?}"
    );
}

#[test]
fn json_key_exists_operators_render_natively() {
    // The three JSONB key-exists operators as first-class `BinaryOp`s, so callers don't need `raw()`.
    let exists = Expr::column("attributes")
        .binary(BinaryOp::JsonExists, lit_str("gen_ai.input.messages"))
        .alias("has_msgs");
    let any = Expr::column("attributes")
        .binary(
            BinaryOp::JsonExistsAny,
            Expr::Array(vec![lit_str("a"), lit_str("b")]),
        )
        .alias("has_any");
    let all = Expr::column("attributes")
        .binary(
            BinaryOp::JsonExistsAll,
            Expr::Array(vec![lit_str("a"), lit_str("b")]),
        )
        .alias("has_all");
    let q = Query::table("records")
        .select(vec![exists, any, all])
        .unwrap();
    assert_snapshot!(
        validate(&q).unwrap(),
        @"SELECT attributes ? 'gen_ai.input.messages' AS has_msgs, attributes ?| ARRAY['a', 'b'] AS has_any, attributes ?& ARRAY['a', 'b'] AS has_all FROM records"
    );
}

#[test]
fn json_key_exists_combines_with_boolean_ops_without_losing_grouping() {
    // Combined with AND / NOT: the key-exists operands must stay grouped so the meaning survives a
    // round-trip through the parser.
    let pred = Expr::unary(
        UnaryOp::Not,
        Expr::column("attributes").binary(BinaryOp::JsonExists, lit_str("a")),
    )
    .binary(
        BinaryOp::And,
        Expr::column("resource").binary(BinaryOp::JsonExists, lit_str("b")),
    );
    let q = Query::table("records").filter(pred).unwrap();
    assert_snapshot!(
        validate(&q).unwrap(),
        @"SELECT * FROM records WHERE NOT attributes ? 'a' AND resource ? 'b'"
    );
}

#[test]
fn string_literal_with_backslash_quote_round_trips() {
    // Regression: a value of `\'` (backslash + single quote) must render as a properly escaped
    // literal that re-parses. DataFusion does not honor backslash escapes, so the embedded quote
    // has to be doubled (`\'` -> `'\'''`); rendering `'\''` instead leaves a dangling quote that
    // `validate` rejects as an unterminated string literal.
    let q = Query::table("records")
        .filter(eq("host_name", "\\'"))
        .unwrap();

    assert_snapshot!(validate(&q).unwrap(), @"SELECT * FROM records WHERE host_name = '\\'''");
}

#[test]
fn string_literals_escape_quotes_and_keep_backslashes() {
    // A bare apostrophe is doubled; a lone backslash stays literal (no backslash escaping).
    let q = Query::table("records")
        .filter(eq("service_name", "O'Brien"))
        .unwrap()
        .filter(eq("path", "C:\\logs"))
        .unwrap();

    assert_snapshot!(
        validate(&q).unwrap(),
        @"SELECT * FROM records WHERE service_name = 'O''Brien' AND path = 'C:\\logs'"
    );
}
