"""
This test module contains column lineage tests for dialect-specific queries.
"""

import pytest

from .helpers import TestColumnQualifierTuple, assert_column_lineage_equal


def test_mysql_create_view_union_all_column_lineage():
    sql = """
CREATE ALGORITHM=UNDEFINED DEFINER=`openmetadata_user`@`%` SQL SECURITY DEFINER
VIEW `test_database`.`business_intelligence_summary` AS
select 'Customer Metrics' AS `metric_category`,
       count(distinct `cs`.`customer_id`) AS `total_count`,
       sum(`cs`.`lifetime_value`) AS `total_value`,
       avg(`cs`.`lifetime_value`) AS `avg_value`
from `test_database`.`customer_segments` `cs`
union all
select 'Product Metrics' AS `metric_category`,
       count(distinct `pis`.`product_id`) AS `total_count`,
       sum((`pis`.`total_sold` * `pis`.`price`)) AS `total_value`,
       avg(`pis`.`price`) AS `avg_value`
from `test_database`.`product_inventory_status` `pis`
union all
select 'Employee Metrics' AS `metric_category`,
       sum(`ds`.`employee_count`) AS `total_count`,
       sum(`ds`.`total_payroll`) AS `total_value`,
       avg(`ds`.`avg_salary`) AS `avg_value`
from `test_database`.`department_stats` `ds`
"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple(
                    "lifetime_value", "test_database.customer_segments"
                ),
                TestColumnQualifierTuple(
                    "avg_value", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "avg_salary", "test_database.department_stats"
                ),
                TestColumnQualifierTuple(
                    "avg_value", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "price", "test_database.product_inventory_status"
                ),
                TestColumnQualifierTuple(
                    "avg_value", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "customer_id", "test_database.customer_segments"
                ),
                TestColumnQualifierTuple(
                    "total_count", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "employee_count", "test_database.department_stats"
                ),
                TestColumnQualifierTuple(
                    "total_count", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "product_id", "test_database.product_inventory_status"
                ),
                TestColumnQualifierTuple(
                    "total_count", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "lifetime_value", "test_database.customer_segments"
                ),
                TestColumnQualifierTuple(
                    "total_value", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "total_payroll", "test_database.department_stats"
                ),
                TestColumnQualifierTuple(
                    "total_value", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "price", "test_database.product_inventory_status"
                ),
                TestColumnQualifierTuple(
                    "total_value", "test_database.business_intelligence_summary"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "total_sold", "test_database.product_inventory_status"
                ),
                TestColumnQualifierTuple(
                    "total_value", "test_database.business_intelligence_summary"
                ),
            ),
        ],
        dialect="mysql",
    )


def test_mysql_create_view_union_all_simple():
    sql = """CREATE VIEW `test_database`.`sales_summary` AS
SELECT 'A' AS `metric_category`, SUM(`a`.`amount`) AS `total_value`
FROM `test_database`.`sales_a` `a`
UNION ALL
SELECT 'B' AS `metric_category`, SUM(`b`.`amount`) AS `total_value`
FROM `test_database`.`sales_b` `b`"""
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("amount", "test_database.sales_a"),
                TestColumnQualifierTuple("total_value", "test_database.sales_summary"),
            ),
            (
                TestColumnQualifierTuple("amount", "test_database.sales_b"),
                TestColumnQualifierTuple("total_value", "test_database.sales_summary"),
            ),
        ],
        dialect="mysql",
    )


@pytest.mark.parametrize("dialect", ["postgres"])
def test_create_view_with_variadic_array_function_column_lineage(dialect: str):
    """Test column lineage for CREATE VIEW with json_extract_path_text using VARIADIC ARRAY.
    https://www.postgresql.org/docs/current/functions-json.html
    """
    assert_column_lineage_equal(
        """create or replace view v_tst as
SELECT json_extract_path_text(tbl_tst.col, VARIADIC ARRAY['foo'::text]) AS json_extract_path_text
   FROM tbl_tst""",
        [
            (
                TestColumnQualifierTuple("col", "tbl_tst"),
                TestColumnQualifierTuple("json_extract_path_text", "v_tst"),
            ),
        ],
        dialect=dialect,
        # SqlParse doesn't recognize VARIADIC as a keyword, treating it as a column name
        test_sqlparse=False,
    )
