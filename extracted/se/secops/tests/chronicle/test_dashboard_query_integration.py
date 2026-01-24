# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Integration tests for Chronicle Dashboard Query API.

These tests require valid credentials and API access.
"""
import uuid

import pytest

from secops import SecOpsClient

from secops.exceptions import APIError
from ..config import CHRONICLE_CONFIG, SERVICE_ACCOUNT_JSON


@pytest.mark.integration
def test_dashboard_query_execute_get():
    """Test adding a chart to a dashboard and running a query."""
    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    chronicle = client.chronicle(**CHRONICLE_CONFIG)

    # Generate unique dashboard name
    unique_id = str(uuid.uuid4())[:8]
    display_name = f"Chart Test Dashboard {unique_id}"
    chart_name = f"Test Chart {unique_id}"

    created_dashboard = None

    try:

        # Execute Dashboard Query

        query_execute = """
        metadata.event_type = "USER_LOGIN"
        match:
          principal.user.userid
        outcome:
          $logon_count = count(metadata.id)
        order:
          $logon_count desc
        limit: 10
        """
        query_execute_interval = {
            "relativeTime": {"timeUnit": "DAY", "startTimeVal": "1"}
        }
        # Execute the query directly
        query_result = chronicle.execute_dashboard_query(
            query=query_execute, interval=query_execute_interval
        )

        assert query_result is not None
        assert "results" in query_result
        print(f"Query executed successfully")

        # Create the dashboard and add chart for fetching query
        created_dashboard = chronicle.create_dashboard(
            display_name=display_name, access_type="PRIVATE"
        )
        dashboard_id = created_dashboard["name"].split("/")[-1]
        print(f"Dashboard created for chart test: {dashboard_id}")

        # Query for chart
        query = """
        metadata.event_type = "NETWORK_DNS"
        match:
          principal.hostname
        outcome:
          $dns_query_count = count(metadata.id)
        order:
          principal.hostname asc
        """
        # Chart Layout
        chart_layout = {"startX": 0, "spanX": 12, "startY": 0, "spanY": 8}
        # Chart Datasource
        chart_datasource = {"dataSources": ["UDM"]}
        # Chart Interval
        interval = {"relativeTime": {"timeUnit": "DAY", "startTimeVal": "1"}}
        # Add chart with query to dashboard
        chart_result = chronicle.add_chart(
            dashboard_id=dashboard_id,
            display_name=chart_name,
            query=query,
            chart_layout=chart_layout,
            chart_datasource=chart_datasource,
            interval=interval,
        )

        assert chart_result is not None
        assert "dashboardChart" in chart_result
        assert "name" in chart_result["dashboardChart"]
        assert "chartDatasource" in chart_result["dashboardChart"]
        assert (
            "dashboardQuery"
            in chart_result["dashboardChart"]["chartDatasource"]
        )
        chart_id = chart_result["dashboardChart"]["name"].split("/")[-1]

        print(f"Chart added successfully to dashboard")

        query_id = chart_result["dashboardChart"]["chartDatasource"][
            "dashboardQuery"
        ].split("/")[-1]
        query_result = chronicle.get_dashboard_query(query_id=query_id)

        assert query_result is not None
        assert query_id in query_result["name"]
        assert chart_id in query_result["dashboardChart"]
        print(f"Query retrieved successfully")

    except APIError as e:
        print(f"API Error: {str(e)}")
        pytest.fail(f"Dashboard query test failed: {str(e)}")

    finally:
        # Clean up
        if created_dashboard:
            try:
                dashboard_id = created_dashboard["name"].split("/")[-1]
                chronicle.delete_dashboard(dashboard_id=dashboard_id)
                print(f"Cleaned up test dashboard: {dashboard_id}")
            except Exception as e:
                print(f"Clean up failed: {str(e)}")
