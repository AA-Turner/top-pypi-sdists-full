"""This is the demo script to show how to manage Integrity Tests

This script will not work without replacing parameters with real values.
Its basic goal is to present what can be done with this module and to
ease its usage.
"""

from mstrio.connection import get_connection
from mstrio.server.test_center.baseline import (
    Baseline,
    BaselineTest,
    list_baseline_results,
    list_baseline_tests,
)
from mstrio.server.test_center.comparison import (
    ComparisonTest,
    ComparisonTestResult,
    list_comparison_test_results,
    list_comparison_tests,
)

# Define variables which can be later used in a script
BASELINE_TEST_ID = $baseline_test_id
COMPARISON_TEST_ID = $comparison_test_id

# Create connection based on workstation data
conn = get_connection(workstationData)


#### Baseline Tests

# List all Baseline Tests
baseline_tests = list_baseline_tests(conn)

# Run a Baseline Test. This will create a Baseline (Baseline Test result)
bl_test = BaselineTest(conn, id=BASELINE_TEST_ID)
bl_result: Baseline = bl_test.execute()

# Check status of the Baseline Test result generation
bl_result.fetch()
print("Status:", bl_result.status)

# List all Baselines (Baseline Test results)
baseline_results = list_baseline_results(conn)


### Comparison Tests

# List all Comparison Tests
comparison_tests = list_comparison_tests(conn)

# Run a Comparison Test. This will create a Comparison (Comparison Test result)
cmp_test = ComparisonTest(conn, id=COMPARISON_TEST_ID)
cmp_result: ComparisonTestResult = cmp_test.execute()

# Check status of the Comparison Test result generation
cmp_result.fetch()
print("Status:", cmp_result.status)

# List all Comparisons (Comparison Test results)
comparison_results = list_comparison_test_results(conn)
