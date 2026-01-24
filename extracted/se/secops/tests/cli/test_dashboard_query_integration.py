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
"""Integration tests for Chronicle Dashboard Query CLI commands.

These tests require valid credentials and API access.
"""
import json
import os
import subprocess
import tempfile
import time
import uuid

import pytest


@pytest.mark.integration
def test_cli_dashboard_query_execute_and_get(cli_env, common_args):
    """Test executing dashboard queries and getting query details."""
    # Generate unique ID for test resources
    unique_id = str(uuid.uuid4())[:8]
    display_name = f"CLI Chart Test Dashboard {unique_id}"
    chart_name = f"CLI Test Chart {unique_id}"
    dashboard_id = None
    chart_query_file_name = None
    executre_query_file_name = None

    try:
        # Create chart query file
        with tempfile.NamedTemporaryFile(
            suffix=".yaral", mode="w+", delete=False
        ) as temp_file:
            temp_file.write(
                """
                metadata.event_type = "NETWORK_DNS"
                match:
                principal.hostname
                outcome:
                $dns_query_count = count(metadata.id)
                order:
                principal.hostname asc
                """
            )
            chart_query_file_name = temp_file.name

        # Create execute query file
        with tempfile.NamedTemporaryFile(
            suffix=".yaral", mode="w+", delete=False
        ) as temp_file:
            temp_file.write(
                """
                metadata.event_type = "USER_LOGIN"
                match:
                principal.user.userid
                outcome:
                $logon_count = count(metadata.id)
                order:
                $logon_count desc
                limit: 10
                """
            )
            executre_query_file_name = temp_file.name

        # Execute Dashboard Query
        execute_interval = (
            '{"relativeTime": {"timeUnit": "DAY", "startTimeVal": "7"}}'
        )
        execute_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard-query",
                "execute",
                "--query-file",
                executre_query_file_name,
                "--interval",
                execute_interval,
            ]
        )

        execute_result = subprocess.run(
            execute_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert execute_result.returncode == 0

        # Load query result
        query_result = json.loads(execute_result.stdout)

        # Verify query execution
        assert query_result is not None
        assert "results" in query_result

        # Create dashboard for charts
        create_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "create",
                "--display-name",
                display_name,
                "--description",
                "CLI chart test dashboard",
                "--access-type",
                "PRIVATE",
            ]
        )

        create_result = subprocess.run(
            create_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert create_result.returncode == 0

        # Load dashboard data
        dashboard_data = json.loads(create_result.stdout)
        dashboard_id = dashboard_data["name"].split("/")[-1]

        query_interval = (
            '{"relativeTime": {"timeUnit": "DAY", "startTimeVal": "7"}}'
        )
        chart_layout = '{"startX": 0, "spanX": 12, "startY": 0, "spanY": 8}'
        chart_datasource = '{"dataSources": ["UDM"]}'
        # Add chart to dashboard
        add_chart_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "add-chart",
                "--dashboard-id",
                dashboard_id,
                "--display-name",
                chart_name,
                "--query-file",
                chart_query_file_name,
                "--interval",
                query_interval,
                "--chart_layout",
                chart_layout,
                "--chart_datasource",
                chart_datasource,
                "--tile-type",
                "VISUALIZATION",
            ]
        )

        add_chart_result = subprocess.run(
            add_chart_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert add_chart_result.returncode == 0

        # Load chart data
        chart_data = json.loads(add_chart_result.stdout)

        # Verify chart was added
        assert chart_data is not None
        assert "dashboardChart" in chart_data
        assert "name" in chart_data["dashboardChart"]
        assert "chartDatasource" in chart_data["dashboardChart"]
        assert (
            "dashboardQuery" in chart_data["dashboardChart"]["chartDatasource"]
        )

        chart_id = chart_data["dashboardChart"]["name"].split("/")[-1]

        query_id = chart_data["dashboardChart"]["chartDatasource"][
            "dashboardQuery"
        ].split("/")[-1]

        # Get Query Details
        get_query_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard-query",
                "get",
                "--id",
                query_id,
            ]
        )

        get_query_result = subprocess.run(
            get_query_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert get_query_result.returncode == 0

        # Load query data
        query_data = json.loads(get_query_result.stdout)

        # Verify query was retrieved
        assert query_data is not None
        assert "name" in query_data
        assert query_id in query_data["name"]
        assert "dashboardChart" in query_data
        assert chart_id in query_data["dashboardChart"]

    finally:
        # Clean up resources
        if dashboard_id:
            delete_cmd = (
                [
                    "secops",
                ]
                + common_args
                + ["dashboard", "delete", "--dashboard-id", dashboard_id]
            )

            subprocess.run(delete_cmd, env=cli_env, check=False)
            print(f"Cleaned up dashboard with ID: {dashboard_id}")

        # Clean up temporary files
        for file in [chart_query_file_name, executre_query_file_name]:
            if os.path.exists(file):
                os.remove(file)
