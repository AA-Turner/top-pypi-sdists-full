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
"""Integration tests for Chronicle Dashboard CLI commands.

These tests require valid credentials and API access.
"""
import os
import json
import subprocess
import tempfile
import time
import uuid

import pytest


@pytest.mark.integration
def test_cli_dashboard_lifecycle(cli_env, common_args):
    """Test the dashboard create, get, update, duplicate and delete commands."""
    # Generate unique IDs for test resources
    unique_id = str(uuid.uuid4())[:8]
    display_name = f"CLI Test Dashboard {unique_id}"
    updated_name = f"Updated CLI Dashboard {unique_id}"
    duplicate_name = f"Duplicate CLI Dashboard {unique_id}"
    dashboard_id = None
    duplicate_id = None

    try:
        # 1. Create dashboard
        create_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "create",
                "--display-name",
                display_name,
                "--description",
                "CLI integration test dashboard",
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

        # Verify dashboard was created
        assert "name" in dashboard_data
        dashboard_id = dashboard_data["name"].split("/")[-1]
        assert dashboard_data["displayName"] == display_name

        print(f"Created dashboard with ID: {dashboard_id}")

        # Wait for dashboard to be fully created
        time.sleep(3)

        # 2. Get dashboard
        get_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "get",
                "--dashboard-id",
                dashboard_id,
                "--view",
                "FULL",
            ]
        )

        get_result = subprocess.run(
            get_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert get_result.returncode == 0

        # Load dashboard data
        get_data = json.loads(get_result.stdout)

        # Verify dashboard details
        assert get_data["name"].split("/")[-1] == dashboard_id
        assert get_data["displayName"] == display_name

        # 3. Update dashboard
        update_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "update",
                "--dashboard-id",
                dashboard_id,
                "--display-name",
                updated_name,
                "--description",
                "Updated CLI test dashboard",
            ]
        )

        update_result = subprocess.run(
            update_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert update_result.returncode == 0

        # Load updated dashboard data
        updated_data = json.loads(update_result.stdout)

        # Verify dashboard was updated
        assert updated_data["displayName"] == updated_name

        # 4. Duplicate dashboard
        duplicate_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "duplicate",
                "--dashboard-id",
                dashboard_id,
                "--display-name",
                duplicate_name,
                "--access-type",
                "PRIVATE",
            ]
        )

        duplicate_result = subprocess.run(
            duplicate_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert duplicate_result.returncode == 0

        # Load duplicated dashboard data
        duplicated_data = json.loads(duplicate_result.stdout)

        # Verify dashboard was duplicated
        assert "name" in duplicated_data
        duplicate_id = duplicated_data["name"].split("/")[-1]
        assert duplicated_data["displayName"] == duplicate_name

        print(f"Duplicated dashboard with ID: {duplicate_id}")

        # Verify both dashboards exist
        get_original_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["dashboard", "get", "--dashboard-id", dashboard_id]
        )

        get_duplicate_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "get",
                "--dashboard-id",
                duplicate_id,
            ]
        )

        get_original_result = subprocess.run(
            get_original_cmd, env=cli_env, capture_output=True, text=True
        )

        get_duplicate_result = subprocess.run(
            get_duplicate_cmd, env=cli_env, capture_output=True, text=True
        )

        assert get_original_result.returncode == 0
        assert get_duplicate_result.returncode == 0

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

        if duplicate_id:
            delete_duplicate_cmd = (
                [
                    "secops",
                ]
                + common_args
                + ["dashboard", "delete", "--dashboard-id", duplicate_id]
            )

            subprocess.run(delete_duplicate_cmd, env=cli_env, check=False)
            print(f"Cleaned up duplicated dashboard with ID: {duplicate_id}")


@pytest.mark.integration
def test_cli_dashboard_list_pagination(cli_env, common_args):
    """Test the dashboard list command with pagination."""
    # Generate unique IDs for test resources
    unique_id = str(uuid.uuid4())[:8]
    dashboard_ids = []

    try:
        # Create multiple dashboards to test pagination
        for i in range(3):
            display_name = f"CLI List Test Dashboard {unique_id} - {i}"
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
                    f"CLI pagination test dashboard {i}",
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

            # Save ID for cleanup
            dashboard_id = dashboard_data["name"].split("/")[-1]
            dashboard_ids.append(dashboard_id)

        # Wait for all dashboards to be fully created
        time.sleep(5)

        # Test list with pagination - page size 2
        list_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["dashboard", "list", "--page-size", "2"]
        )

        list_result = subprocess.run(
            list_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert list_result.returncode == 0

        # Load list data
        list_data = json.loads(list_result.stdout)

        # Verify pagination
        assert "nativeDashboards" in list_data
        assert (
            len(list_data["nativeDashboards"]) <= 2
        )  # Should have at most 2 items
        assert "nextPageToken" in list_data  # Should have a next page token

        # Test list with page token
        page_token = list_data["nextPageToken"]
        list_page2_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "list",
                "--page-size",
                "2",
                "--page-token",
                page_token,
            ]
        )

        list_page2_result = subprocess.run(
            list_page2_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert list_page2_result.returncode == 0

        # Load page 2 data
        page2_data = json.loads(list_page2_result.stdout)

        # Verify second page has data
        assert "nativeDashboards" in page2_data
        assert len(page2_data["nativeDashboards"]) > 0

    finally:
        # Clean up resources
        for dashboard_id in dashboard_ids:
            delete_cmd = (
                [
                    "secops",
                ]
                + common_args
                + ["dashboard", "delete", "--dashboard-id", dashboard_id]
            )

            subprocess.run(delete_cmd, env=cli_env, check=False)
            print(f"Cleaned up dashboard with ID: {dashboard_id}")


@pytest.mark.integration
def test_cli_dashboard_chart_lifecycle(cli_env, common_args):
    """Test full dashboard chart lifecycle via CLI: add, get, edit and remove."""
    # Generate unique ID for test resources
    unique_id = str(uuid.uuid4())[:8]
    display_name = f"CLI Chart Test Dashboard {unique_id}"
    chart_name = f"CLI Test Chart {unique_id}"
    dashboard_id = None

    try:
        # Create dashboard
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
                "CLI chart lifecycle test dashboard",
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

        # Add chart to dashboard
        query = """
        metadata.event_type = "NETWORK_DNS"
        match:
        principal.hostname
        outcome:
        $dns_query_count = count(metadata.id)
        order:
        principal.hostname asc
        """
        query_interval = (
            '{"relativeTime": {"timeUnit": "DAY", "startTimeVal": "1"}}'
        )
        chart_layout = '{"startX": 0, "spanX": 12, "startY": 0, "spanY": 8}'
        chart_datasource = '{"dataSources": ["UDM"]}'

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
                "--query",
                query,
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
        chart_id = chart_data["dashboardChart"]["name"].split("/")[-1]

        # Get chart details
        get_chart_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "get-chart",
                "--id",
                chart_id,
            ]
        )

        get_chart_result = subprocess.run(
            get_chart_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert get_chart_result.returncode == 0

        # Load chart details
        chart_details = json.loads(get_chart_result.stdout)

        # Verify chart details were retrieved
        assert chart_details is not None
        assert "name" in chart_details
        assert chart_id in chart_details["name"]
        assert "etag" in chart_details

        # Edit chart details
        updated_chart_name = "Updated CLI Chart Name"
        updated_dashboard_chart = json.dumps(
            {
                "name": chart_details["name"],
                "displayName": updated_chart_name,
                "etag": chart_details["etag"],
            }
        )

        edit_chart_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "edit-chart",
                "--dashboard-id",
                dashboard_id,
                "--dashboard-chart",
                updated_dashboard_chart,
            ]
        )

        edit_chart_result = subprocess.run(
            edit_chart_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert edit_chart_result.returncode == 0

        # Load updated chart data
        updated_chart = json.loads(edit_chart_result.stdout)

        # Verify chart was updated
        assert updated_chart is not None
        assert "dashboardChart" in updated_chart
        assert "displayName" in updated_chart["dashboardChart"]
        assert (
            updated_chart["dashboardChart"]["displayName"] == updated_chart_name
        )

        # Remove chart from dashboard
        remove_chart_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "dashboard",
                "remove-chart",
                "--dashboard-id",
                dashboard_id,
                "--chart-id",
                chart_id,
            ]
        )

        remove_chart_result = subprocess.run(
            remove_chart_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert remove_chart_result.returncode == 0

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


@pytest.mark.integration
def test_cli_dashboard_export_import(cli_env, common_args):
    """Test the dashboard export and import flow via CLI."""

    # Generate unique IDs for test resources
    unique_id = str(uuid.uuid4())[:8]
    display_name = f"CLI Export Test Dashboard {unique_id}"
    cleanup_ids = []
    export_file_name = None

    try:
        # 1. Create a dashboard to export
        create_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "create",
                "--display-name",
                display_name,
                "--description",
                "CLI test dashboard for export-import",
                "--access-type",
                "PRIVATE",
            ]
        )

        create_result = subprocess.run(
            create_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert create_result.returncode == 0

        # Load dashboard data and get ID
        source_data = json.loads(create_result.stdout)
        source_dashboard_id = source_data["name"].split("/")[-1]
        print(f"Created dashboard with ID: {source_dashboard_id}")
        cleanup_ids.append(source_dashboard_id)

        # Wait for dashboard to be fully created
        time.sleep(3)

        # 2. Export the created dashboard
        export_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "export",
                "--dashboard-names",
                source_dashboard_id,
            ]
        )

        export_result = subprocess.run(
            export_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert export_result.returncode == 0

        # Parse the export result
        export_data = json.loads(export_result.stdout)
        assert "inlineDestination" in export_data
        assert "dashboards" in export_data["inlineDestination"]
        assert len(export_data["inlineDestination"]["dashboards"]) > 0

        # Save the export data to file
        # Write import data to a temporary file
        with tempfile.NamedTemporaryFile(
            suffix=".json", mode="w+", delete=False
        ) as temp_file:
            temp_file.write(
                json.dumps(
                    export_data["inlineDestination"]["dashboards"][0][
                        "dashboard"
                    ]
                )
            )
            export_file_name = temp_file.name

        # 3. Import the dashboard from export file
        import_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "import",
                "--dashboard-data-file",
                export_file_name,
            ]
        )

        import_result = subprocess.run(
            import_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert import_result.returncode == 0

        # Parse the import result
        import_data = json.loads(import_result.stdout)
        assert "results" in import_data
        assert len(import_data["results"]) > 0
        assert "dashboard" in import_data["results"][0]

        # Extract the imported dashboard ID
        imported_dashboard_id = import_data["results"][0]["dashboard"].split(
            "/"
        )[-1]
        print(f"Imported dashboard with ID: {imported_dashboard_id}")
        cleanup_ids.append(imported_dashboard_id)

        # 4. Verify the imported dashboard matches the original
        # Get the source dashboard
        get_source_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "get",
                "--dashboard-id",
                source_dashboard_id,
            ]
        )

        source_result = subprocess.run(
            get_source_cmd, env=cli_env, capture_output=True, text=True
        )

        # Get the imported dashboard
        get_imported_cmd = (
            ["secops"]
            + common_args
            + [
                "dashboard",
                "get",
                "--dashboard-id",
                imported_dashboard_id,
            ]
        )

        imported_result = subprocess.run(
            get_imported_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that both commands executed successfully
        assert source_result.returncode == 0
        assert imported_result.returncode == 0

        # Parse the dashboard details
        source_details = json.loads(source_result.stdout)
        imported_details = json.loads(imported_result.stdout)

        # Verify key properties match
        assert imported_details["displayName"] == source_details["displayName"]
        assert imported_details["description"] == source_details["description"]
        assert imported_details["type"] == source_details["type"]
        assert imported_details["access"] == source_details["access"]

    finally:
        # Clean up resources
        # Delete dashboards
        for dashboard_id in cleanup_ids:
            if dashboard_id:
                delete_cmd = (
                    ["secops"]
                    + common_args
                    + [
                        "dashboard",
                        "delete",
                        "--dashboard-id",
                        dashboard_id,
                    ]
                )
                subprocess.run(delete_cmd, env=cli_env, check=False)
                print(f"Cleaned up dashboard with ID: {dashboard_id}")

        # Clean up temporary files
        try:
            if export_file_name and os.path.exists(export_file_name):
                os.remove(export_file_name)
                print(f"Removed temporary file: {export_file_name}")
        except Exception as e:
            print(f"Error removing temporary file: {str(e)}")
