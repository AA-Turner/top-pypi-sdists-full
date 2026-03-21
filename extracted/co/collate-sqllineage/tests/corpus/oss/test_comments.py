"""Tests for OSS comment edge cases."""

from tests.helpers import assert_table_lineage_equal


def test_double_slash_at_start_usage_sql():
    # SqlParse can trim leading '//' usage comments, while SqlGlot and SqlFluff
    # currently treat them as syntax errors.
    assert_table_lineage_equal(
        """
        //LA2 TO/PO fulfill
WITH t AS
(SELECT to_no AS order_number,part_no,date(date_last_fulfillment) AS fulfill_date,
YEAR(date_last_fulfillment) AS fulfill_year,toWeek(date_last_fulfillment,9) AS week,
CASE WHEN ship_location_group LIKE '%LA2%' THEN 'LA2'
WHEN ship_location_group LIKE '%EC1%' THEN 'EC1'
END AS location_group
FROM ods.fb_to ft
LEFT JOIN ods.fb_to_line ftl
ON ft.to_no =ftl.to_no
WHERE (ship_location_group LIKE '%LA2%' OR ship_location_group LIKE '%EC1%') AND from_location_group='YW1'
AND year(date_last_fulfillment)>=year(today())-1 AND toYearWeek(date_last_fulfillment,9)<toYearWeek(today(),9)
AND date_last_fulfillment IS NOT NULL),
s as
(SELECT po_no AS order_number,part_no,date(po_line_date_last_fulfillment) AS fulfill_date,
year(po_line_date_last_fulfillment) AS fulfill_year,toWeek(po_line_date_last_fulfillment,9) AS week,
CASE WHEN po_location_group LIKE '%LA2%' THEN 'LA2'
WHEN po_location_group LIKE '%EC1%' THEN 'EC1'
END AS location_group
FROM ods.fb_po fp
LEFT JOIN ods.fb_po_line fpl
ON fp.po_no=fpl.po_no
WHERE (po_location_group LIKE '%LA2%' OR po_location_group LIKE '%EC1%')
AND year(po_line_date_last_fulfillment)>=year(today())-1
AND toYearWeek(po_line_date_last_fulfillment,9)<toYearWeek(today(),9)
AND po_line_date_last_fulfillment IS NOT NULL)
SELECT order_number,part_no,fulfill_date,fulfill_year,week,location_group
FROM t
UNION ALL
SELECT order_number,part_no,fulfill_date,fulfill_year,week,location_group
FROM s
        """,
        {"ods.fb_to", "ods.fb_to_line", "ods.fb_po", "ods.fb_po_line"},
        test_sqlglot=False,
        test_sqlfluff=False,
        test_sqlparse=True,
    )


def test_double_slash_at_start_usage_sql_simple():
    # SqlParse can trim leading '//' usage comments, while SqlGlot and SqlFluff
    # currently treat them as syntax errors.
    assert_table_lineage_equal(
        """
        //LA2 TO/PO fulfill
        SELECT * FROM my_schema.my_table
        """,
        {"my_schema.my_table"},
        test_sqlglot=False,
        test_sqlfluff=False,
        test_sqlparse=True,
    )
