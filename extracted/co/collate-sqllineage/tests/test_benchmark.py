"""

### Benchmarks

results of the tests/test_benchmark.py for tracking the performance.

|Test | Parsing Time in sec. |
|---|---|
| short_query | 0.30 |
| medium_query  | 0.43 |
| long_query  | 1.35 |
| crazy_long_query  | 34.89 |
| avg_query | 0.24 |

"""

import time

from collate_sqllineage.runner import LineageRunner


def assert_time(query_file_name: str, expected_time_sec: int, dialect="ansi"):
    with open(f"tests/queries/{query_file_name}") as query_file:
        start_time = time.time()
        sql = query_file.read()
        lr_sqlfluff = LineageRunner(sql, dialect=dialect)
        lr_sqlfluff.source_tables
        lr_sqlfluff.target_tables
        lr_sqlfluff.get_column_lineage()
        total_time = time.time() - start_time
        return total_time <= expected_time_sec


def test_short_query():
    assert assert_time("query02.sql", 5)


def test_medium_query():
    assert assert_time("query01.sql", 5)


def test_long_query():
    assert assert_time("query03.sql", 10)


def test_crazy_long_query():
    assert assert_time("query04.sql", 200, "snowflake")


def test_compute_avg_time():
    EXPECTED_AVG_TIME = 5
    start_time = time.time()
    for i in range(1, 11):
        with open(
            f"tests/queries/avg_queries/query{str(i).rjust(2, '0')}.sql"
        ) as query_file:
            sql = query_file.read()
            lr_sqlfluff = LineageRunner(sql, dialect="ansi")
            lr_sqlfluff.source_tables
            lr_sqlfluff.target_tables
            lr_sqlfluff.get_column_lineage()
    total_time = time.time() - start_time
    avg_time = total_time / 10
    assert avg_time < EXPECTED_AVG_TIME
