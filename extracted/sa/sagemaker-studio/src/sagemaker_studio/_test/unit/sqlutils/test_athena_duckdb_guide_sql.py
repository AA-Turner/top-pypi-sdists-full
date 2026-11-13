"""The SQL of the Athena DuckDB guide (AthenaBetaDocs ``topics/duckdb-sql.md``) reaches Athena as written.

The SDK sends each statement to StartQueryExecution as its own query, byte for byte: it neither rewrites
the DuckDB syntax (``CREATE TABLE ... WITH (type = 'HIVE', ...)``, FROM-first, ``lambda x:``, ``::``) nor
splits it anywhere but on real semicolons. Athena alone parses it.
"""

import unittest
from unittest import mock

from sagemaker_studio.sql_engine.sql_executor import ErrorStrategy, SqlExecutor
from sagemaker_studio.utils.athena_v4 import (
    AthenaV4Executor,
    execute_query_statements,
    split_query,
)

QID = "11111111-2222-3333-4444-555555555555"
DUCKDB = "Athena DuckDB"

# The guide's tutorial, one statement per query, as the guide runs them.
TUTORIAL = [
    "CREATE SCHEMA duckdb_tutorial",
    """CREATE TABLE duckdb_tutorial.sales_parquet (
    order_id INTEGER,
    customer VARCHAR,
    region VARCHAR,
    amount DECIMAL(10,2),
    order_date DATE
)
WITH (
    type = 'HIVE',
    format = 'parquet',
    location = 's3://amzn-s3-demo-bucket/duckdb-tutorial/sales_parquet/'
)""",
    """INSERT INTO duckdb_tutorial.sales_parquet VALUES
    (1, 'alice', 'east', 120.50, DATE '2026-10-01'),
    (2, 'bob', 'west', 75.00, DATE '2026-10-01'),
    (3, 'carol', 'east', 42.25, DATE '2026-10-02')""",
    """CREATE TABLE duckdb_tutorial.sales_by_region
WITH (
    type = 'HIVE',
    format = 'parquet',
    location = 's3://amzn-s3-demo-bucket/duckdb-tutorial/sales_by_region/'
)
AS SELECT region, count(*) AS order_count, sum(amount) AS revenue
FROM duckdb_tutorial.sales_parquet
GROUP BY region""",
    """CREATE TABLE duckdb_tutorial.orders (
    order_id INTEGER,
    customer VARCHAR,
    region VARCHAR,
    amount DECIMAL(10,2),
    order_date DATE
)
WITH (
    type = 'ICEBERG',
    location = 's3://amzn-s3-demo-bucket/duckdb-tutorial/orders/',
    'format-version' = '2'
)""",
    """INSERT INTO duckdb_tutorial.orders
SELECT order_id, customer, region, amount, order_date
FROM duckdb_tutorial.sales_parquet""",
    "UPDATE duckdb_tutorial.orders SET amount = 80.00 WHERE order_id = 2",
    "DELETE FROM duckdb_tutorial.orders WHERE order_id = 3",
    """COPY (
    SELECT region, order_count, revenue
    FROM duckdb_tutorial.sales_by_region
    ORDER BY region
) TO 's3://amzn-s3-demo-bucket/duckdb-tutorial/export/by_region.parquet' (FORMAT parquet)""",
    "DROP TABLE duckdb_tutorial.sales_by_region",
    "DROP SCHEMA duckdb_tutorial CASCADE",
]

# The guide's DuckDB SQL features and naming rules.
FEATURES = [
    "FROM duckdb_tutorial.orders SELECT region, amount WHERE amount > 50",
    "SELECT * EXCLUDE (customer) FROM duckdb_tutorial.orders",
    "SELECT region, sum(amount) FROM duckdb_tutorial.orders GROUP BY ALL ORDER BY ALL",
    "SELECT * FROM duckdb_tutorial.orders QUALIFY row_number() OVER (PARTITION BY region ORDER BY amount DESC) = 1",
    "SELECT list_transform([1, 2, 3], lambda x: x + 1) AS plus_one",
    "SELECT CAST(sum(order_id) AS BIGINT), amount::VARCHAR FROM duckdb_tutorial.orders GROUP BY amount",
    'SELECT * FROM "s3tablescatalog/amzn-s3-demo-table-bucket".tutorial_ns.daily_orders',
    "SELECT * FROM awsdatacatalog.duckdb_tutorial.orders",
]


def _executor(**kwargs):
    client = mock.Mock()
    client.start_query_execution.return_value = {"QueryExecutionId": QID}
    client.get_query_execution.return_value = {
        "QueryExecution": {
            "QueryExecutionId": QID,
            "StatementType": "DDL",
            "SubstatementType": "CREATE_TABLE",
            "Status": {"State": "SUCCEEDED"},
            "EngineVersion": {"EffectiveEngineVersion": DUCKDB},
        }
    }
    return AthenaV4Executor(client, "wg", selected_engine_version=DUCKDB, **kwargs), client


class AthenaDuckDBGuideSqlTest(unittest.TestCase):
    def test_each_statement_is_sent_as_written(self):
        for statement in TUTORIAL + FEATURES:
            with self.subTest(statement=statement.splitlines()[0]):
                executor, client = _executor()
                executor.start(statement)
                request = client.start_query_execution.call_args.kwargs
                self.assertEqual(request["QueryString"], statement)
                self.assertEqual(request["EngineVersion"], DUCKDB)

    def test_each_statement_is_one_query(self):
        for statement in TUTORIAL + FEATURES:
            with self.subTest(statement=statement.splitlines()[0]):
                self.assertEqual([s.statement for s in split_query(statement)], [statement])

    def test_a_cell_of_tutorial_statements_runs_one_query_per_statement(self):
        # A cell takes at most SqlExecutor.MAX_STATEMENTS, so the tutorial is run as two cells.
        half = len(TUTORIAL) // 2
        for cell in (TUTORIAL[:half], TUTORIAL[half:]):
            with self.subTest(first=cell[0].splitlines()[0]):
                executor, client = _executor()
                results = list(
                    execute_query_statements(
                        executor, ";\n\n".join(cell) + ";", ErrorStrategy.STOP_ON_ERROR
                    )
                )
                self.assertEqual(len(results), len(cell))
                sent = [
                    c.kwargs["QueryString"] for c in client.start_query_execution.call_args_list
                ]
                self.assertEqual(sent, cell)

    def test_a_cell_of_the_whole_tutorial_is_over_the_statement_limit(self):
        # Eleven statements, one more than a cell takes: refused before any query starts.
        self.assertGreater(len(TUTORIAL), SqlExecutor.MAX_STATEMENTS)
        executor, client = _executor()
        with self.assertRaisesRegex(ValueError, "Too many statements"):
            list(
                execute_query_statements(
                    executor, ";\n\n".join(TUTORIAL) + ";", ErrorStrategy.STOP_ON_ERROR
                )
            )
        client.start_query_execution.assert_not_called()

    def test_named_parameters_leave_the_lambda_colon_alone(self):
        statement = "SELECT list_transform([1, 2, 3], lambda x: x + :step) AS stepped"
        executor, client = _executor(execution_parameters={"step": 2})
        executor.start(statement)
        self.assertEqual(
            client.start_query_execution.call_args.kwargs["QueryString"],
            "SELECT list_transform([1, 2, 3], lambda x: x + 2) AS stepped",
        )

    def test_create_table_with_hive_options_reads_no_result_stream(self):
        executor, client = _executor()
        result = executor.execute(TUTORIAL[1])
        self.assertEqual(result.result, -1)
        client.get_query_result_stream.assert_not_called()
        client.get_query_results.assert_not_called()


if __name__ == "__main__":
    unittest.main()
