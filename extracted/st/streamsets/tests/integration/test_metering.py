#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
from collections import OrderedDict

import pytest

# fmt: on


@pytest.mark.skip("Skipping test until TLKT-1653 is completed")
def test_get_data_for_time_frame(metering_report):
    """This test will pull metering data for the last 7 days, and verify that it was successfully retrieved.

    The metering_report object contains the response from the Metering API and thus should not have a 'None' type for
    any of the metrics returned.
    """
    assert metering_report.total_units is not None
    assert metering_report.pipeline_hours is not None
    assert metering_report.clock_hours is not None
    assert metering_report.average_units_per_day is not None


@pytest.mark.skip("Skipping test until TLKT-1653 is completed")
def test_get_top_usage(metering_report):
    """This test will check the "top" usage for deployments, environments, jobs and users.

    It will compare the data for the last 7 days, and pull the "top" objects for each type of metric: pipeline_hours,
    total_units, and clock_hours. Finally, it asserts that all of these items were retrievable and are of the
    OrderedDict type.
    """
    usage_metrics = ['pipeline_hours', 'total_units', 'clock_hours']

    for metric in usage_metrics:
        top_deployments = metering_report.get_top_deployments(metric)
        top_environments = metering_report.get_top_environments(metric)
        top_jobs = metering_report.get_top_jobs(metric)
        top_users = metering_report.get_top_users(metric)
        assert top_deployments is not None and isinstance(top_deployments, OrderedDict)
        assert top_environments is not None and isinstance(top_environments, OrderedDict)
        assert top_jobs is not None and isinstance(top_jobs, OrderedDict)
        assert top_users is not None and isinstance(top_users, OrderedDict)


@pytest.mark.skip("Skipping test until TLKT-1653 is completed")
def test_data_in_sorted_order(metering_report):
    # Not testing every metric type since they all share the same utility function for sorting
    metric = 'total_units'

    top_deployments = metering_report.get_top_deployments(metric)
    top_environments = metering_report.get_top_environments(metric)
    top_jobs = metering_report.get_top_jobs(metric)
    top_users = metering_report.get_top_users(metric)

    for result in [top_deployments, top_environments, top_jobs, top_users]:
        result_list = list(result.items())
        # Check that each '(key, metric)' tuple in the list has a metric value greater than the next tuple in the list,
        # indicating reverse sorted order.
        assert all(result_list[i][1] >= result_list[i + 1][1] for i in range(len(result_list) - 1))
