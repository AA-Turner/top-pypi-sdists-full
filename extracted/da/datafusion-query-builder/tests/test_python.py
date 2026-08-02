"""Smoke tests exercising the Python API against real query shapes from the codebase.

Run after `maturin develop`:  python -m pytest tests/test_python.py   (or run directly).
"""

from datafusion_query_builder import (
    QueryBuilderError,
    UnparsableSqlError,
    and_,
    col,
    f,
    param,
    raw,
    table,
    when,
)


def test_red_metrics():
    q = (
        table('records')
        .filter(col('kind') == 'span')
        .select(
            f.coalesce(col('service_name'), '(unknown)').alias('service'),
            f.approx_distinct(col('trace_id')).alias('request_count'),
            f.approx_percentile_cont(col('duration'), 0.95).alias('p95'),
        )
        .group_by(col('service_name'))
        .order_by(col('request_count').desc())
        .limit(200)
    )
    assert q.to_sql() == (
        "SELECT coalesce(service_name, '(unknown)') AS service, "
        'approx_distinct(trace_id) AS request_count, '
        'approx_percentile_cont(duration, 0.95) AS p95 '
        "FROM records WHERE kind = 'span' "
        'GROUP BY service_name ORDER BY request_count DESC LIMIT 200'
    )


def test_metrics_time_series_with_param():
    q = (
        table('metrics')
        .filter(col('metric_name') == 'http.server.duration')
        .select(
            f.time_bucket(param('resolution'), col('recorded_timestamp')).alias('time'),
            f.metric_quantile(0.99, col('value')).alias('value'),
        )
        .group_by(col('time'))
        .order_by(col('time').asc())
    )
    assert q.validate() == (
        'SELECT time_bucket(${resolution}, recorded_timestamp) AS time, '
        'metric_quantile(0.99, value) AS value '
        "FROM metrics WHERE metric_name = 'http.server.duration' "
        'GROUP BY time ORDER BY time ASC'
    )


def test_count_filter_and_in_list():
    q = (
        table('records')
        .select(
            f.count().alias('total'),
            f.count().filter(col('is_exception')).alias('errors'),
        )
        .filter(col('deployment_environment').is_in(['prod', 'staging']))
    )
    assert q.to_sql() == (
        'SELECT count(*) AS total, count(*) FILTER (WHERE is_exception) AS errors '
        "FROM records WHERE deployment_environment IN ('prod', 'staging')"
    )


def test_boolean_operators_and_case():
    pred = (col('env') == 'prod') & (col('level') >= 40)
    case = when(col('level') >= 40).then('error').when(col('level') >= 30).then('warn').otherwise('ok')
    q = table('records').select(case.alias('sev')).filter(pred)
    assert q.to_sql() == (
        "SELECT CASE WHEN level >= 40 THEN 'error' WHEN level >= 30 THEN 'warn' ELSE 'ok' END AS sev "
        "FROM records WHERE env = 'prod' AND level >= 40"
    )


def test_n_ary_and_with_scalar_promotion():
    # bare ints/strings promote to literals; and_ combines n predicates.
    q = table('t').filter(and_(col('a') == 1, col('b') == 'x', col('c') > 3.5))
    assert q.to_sql() == "SELECT * FROM t WHERE a = 1 AND b = 'x' AND c > 3.5"


def test_cte_cross_join():
    def window(interval: str) -> object:
        return (
            table('records')
            .filter(col('service_name') == 'svc')
            .filter(col('start_timestamp') > raw(f"now() - interval '{interval}'"))
            .select(f.round(f.avg(col('bad')), 2).alias('burn_rate'))
        )

    q = (
        table('long_window')
        .with_cte('long_window', window('1 hour'))
        .with_cte('short_window', window('5 minutes'))
        .cross_join('short_window')
        .select(
            col('burn_rate', 'long_window').alias('long_burn'),
            col('burn_rate', 'short_window').alias('short_burn'),
        )
    )
    sql = q.validate()
    assert 'WITH long_window AS (' in sql
    assert 'CROSS JOIN short_window' in sql


def test_window_function():
    q = table('t').select(
        f.sum(col('v')).over(partition_by=[col('svc')], order_by=[col('t').asc()]).alias('running'),
    )
    assert q.to_sql() == ('SELECT sum(v) OVER (PARTITION BY svc ORDER BY t ASC) AS running FROM t')


def test_subquery_in_from_and_scalar():
    inner = table('records').select(col('trace_id'), col('duration'))
    q = table('x').from_(inner, alias='sub').select(f.avg(col('duration')).alias('avg_dur'))
    assert q.to_sql() == ('SELECT avg(duration) AS avg_dur FROM (SELECT trace_id, duration FROM records) AS sub')


def test_injection_is_escaped():
    # A malicious value is rendered as a quoted, escaped literal, not interpolated SQL.
    evil = "x'); DROP TABLE records; --"
    q = table('records').filter(col('name') == evil)
    sql = q.to_sql()
    assert 'DROP TABLE' in sql  # present, but inside the quoted literal
    assert sql == "SELECT * FROM records WHERE name = 'x''); DROP TABLE records; --'"
    q.validate()  # still a single well-formed statement


def test_json_key_exists_operators():
    # The JSONB key-exists family: `?`, `?|`, `?&`. `has_key` is the cheap presence check the
    # value-extraction fallback (`->> 'k' is not null`) was standing in for.
    q = (
        table('records')
        .select(
            col('attributes').has_key('gen_ai.input.messages').alias('has_msgs'),
            col('attributes').has_any_key(['a', 'b']).alias('has_any'),
            col('attributes').has_all_keys(['a', 'b']).alias('has_all'),
        )
        .filter(col('attributes').has_key('gen_ai.input.messages'))
    )
    assert q.validate() == (
        "SELECT attributes ? 'gen_ai.input.messages' AS has_msgs, "
        "attributes ?| ARRAY['a', 'b'] AS has_any, "
        "attributes ?& ARRAY['a', 'b'] AS has_all "
        "FROM records WHERE attributes ? 'gen_ai.input.messages'"
    )


def test_raw_json_operator_no_longer_silently_truncated():
    # The reported bug: raw() dropped the `?` operator, rendering just `attributes`. It now renders
    # (and re-parses) faithfully.
    q = table('records').select(raw("attributes ? 'gen_ai.input.messages'").alias('x'))
    assert q.validate() == "SELECT attributes ? 'gen_ai.input.messages' AS x FROM records"


def test_raw_fragment_with_trailing_tokens_raises():
    # A fragment that parses a leading expression but leaves tokens behind is now a loud error
    # rather than a silent truncation to the prefix.
    try:
        table('t').select(raw('1 + 1 oops')).to_sql()
    except UnparsableSqlError:
        return
    raise AssertionError('expected UnparsableSqlError for trailing tokens')


def test_unparsable_sql_raises_unparsable_sql_error():
    # A bad raw() fragment or cast type is caller-supplied bad SQL -> UnparsableSqlError.
    assert issubclass(UnparsableSqlError, QueryBuilderError)
    for q in (
        table('t').filter(raw('this is not valid sql')),
        table('t').select(col('x').cast('not a type !!')),
    ):
        try:
            q.to_sql()
        except UnparsableSqlError:
            continue
        raise AssertionError('expected UnparsableSqlError')


def test_api_misuse_raises_query_builder_error_not_unparsable():
    # Using the API wrong (filter() on a non-aggregate) is our bug, not bad SQL: a plain
    # QueryBuilderError, never an UnparsableSqlError.
    try:
        col('x').filter(col('y'))
    except UnparsableSqlError:
        raise AssertionError('misuse should not be UnparsableSqlError')
    except QueryBuilderError:
        return
    raise AssertionError('expected QueryBuilderError for API misuse')


if __name__ == '__main__':
    import sys
    import traceback

    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith('test_') and callable(fn):
            try:
                fn()
                print(f'ok   {name}')
            except (AssertionError, ValueError, TypeError, RuntimeError, QueryBuilderError):
                # The assertions raise AssertionError; the builder surfaces bad input as
                # QueryBuilderError/ValueError/TypeError. Anything else is unexpected.
                failures += 1
                print(f'FAIL {name}')
                traceback.print_exc()
    sys.exit(1 if failures else 0)
