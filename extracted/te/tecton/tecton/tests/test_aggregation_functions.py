from dataclasses import dataclass

import pytest

from tecton.aggregation_functions import AggregationFunction
from tecton.aggregation_functions import approx_count_distinct
from tecton.aggregation_functions import approx_percentile
from tecton.aggregation_functions import first
from tecton.aggregation_functions import first_distinct
from tecton.aggregation_functions import last
from tecton.aggregation_functions import last_distinct


@dataclass
class TestAggregationFunctions__TestCase:
    aggregation: AggregationFunction
    expected_resolved_name: str


TEST_AGGREGATION_FUNCTIONS_TEST_CASES = (
    TestAggregationFunctions__TestCase(
        aggregation=AggregationFunction(base_name="count", resolved_name="count", params={}),
        expected_resolved_name="count",
    ),
    TestAggregationFunctions__TestCase(aggregation=last(3), expected_resolved_name="last_3"),
    TestAggregationFunctions__TestCase(aggregation=last(1003), expected_resolved_name="last_1003"),
    TestAggregationFunctions__TestCase(aggregation=last_distinct(3), expected_resolved_name="last_distinct_3"),
    TestAggregationFunctions__TestCase(aggregation=first(3), expected_resolved_name="first_3"),
    TestAggregationFunctions__TestCase(aggregation=first_distinct(3), expected_resolved_name="first_distinct_3"),
    TestAggregationFunctions__TestCase(
        aggregation=approx_percentile(percentile=0.0, precision=100), expected_resolved_name="approx_percentile_p0_0"
    ),
    TestAggregationFunctions__TestCase(
        aggregation=approx_percentile(percentile=0.0, precision=50), expected_resolved_name="approx_percentile_p0_0"
    ),
    TestAggregationFunctions__TestCase(
        aggregation=approx_percentile(percentile=0.5), expected_resolved_name="approx_percentile_p0_5"
    ),
    TestAggregationFunctions__TestCase(
        aggregation=approx_percentile(percentile=0.99, precision=50), expected_resolved_name="approx_percentile_p0_99"
    ),
    TestAggregationFunctions__TestCase(
        aggregation=approx_percentile(percentile=1.0, precision=50), expected_resolved_name="approx_percentile_p1_0"
    ),
    TestAggregationFunctions__TestCase(
        aggregation=approx_count_distinct(), expected_resolved_name="approx_count_distinct"
    ),
    TestAggregationFunctions__TestCase(
        aggregation=approx_count_distinct(precision=12), expected_resolved_name="approx_count_distinct"
    ),
)


@pytest.mark.parametrize("test_case", TEST_AGGREGATION_FUNCTIONS_TEST_CASES)
def test_aggregation_groups(test_case: TestAggregationFunctions__TestCase):
    assert test_case.aggregation.resolved_name == test_case.expected_resolved_name
