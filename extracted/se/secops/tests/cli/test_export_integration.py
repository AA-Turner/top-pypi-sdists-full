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
"""Integration tests for the SecOps CLI data export commands."""

import pytest
import subprocess
import json
import os
from datetime import datetime, timedelta, timezone

from ..config import CHRONICLE_CONFIG


@pytest.mark.integration
def test_cli_export_list_available_types(cli_env, common_args):
    """Test the export list-types command."""

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)  # Look back 1 day
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    # Execute the CLI command
    cmd = (
        [
            "secops",
        ]
        + common_args
        + [
            "export",
            "log-types",
            "--start-time",
            start_time_str,
            "--end-time",
            end_time_str,
        ]
    )

    result = subprocess.run(cmd, env=cli_env, capture_output=True, text=True)

    # Check that the command executed successfully
    assert result.returncode == 0

    # Try to parse the output as JSON
    try:
        output = json.loads(result.stdout)
        assert "log_types" in output

        # If log types are available, verify their structure
        if len(output["log_types"]) > 0:
            assert output["log_types"]
    except json.JSONDecodeError:
        # If not valid JSON, check for expected error messages
        assert "Error:" not in result.stdout


@pytest.mark.integration
def test_cli_export_lifecycle(cli_env, common_args):
    """Test the complete export command lifecycle.

    This test covers:
    - Creating a data export
    - Listing exports
    - Getting export details
    - Updating an export (if possible)
    - Cancelling the export
    """
    # Variables to track resources we create
    export_id = None

    try:
        # Set up time range for testing
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=1)  # Look back 1 day
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Store initial start time for later verification of update
        initial_start_time = start_time

        # Step 1: Create a data export with all logs
        print("\nStep 1: Creating data export with all logs")

        # Get the bucket from environment or use a test one
        bucket_name = os.environ.get(
            "TEST_GCS_BUCKET",
            "gcs-exports-prober-bucket-us",
        )

        bucket_path = (
            f"projects/{CHRONICLE_CONFIG['project_id']}/buckets/{bucket_name}"
        )

        # Create the export
        cmd_create = (
            [
                "secops",
            ]
            + common_args
            + [
                "export",
                "create",
                "--gcs-bucket",
                bucket_path,
                "--all-logs",  # Use all logs instead of specific log type
                "--start-time",
                start_time_str,
                "--end-time",
                end_time_str,
            ]
        )

        result_create = subprocess.run(
            cmd_create, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            result_create.returncode == 0
        ), f"Create export failed: {result_create.stderr}"

        # Parse the output to get the export ID
        try:
            create_data = json.loads(result_create.stdout)
            export_id = create_data["name"].split("/")[-1]
            print(f"Created export with ID: {export_id}")

            # Print the export status
            if "dataExportStatus" in create_data:
                print(
                    f"Initial status: {create_data['dataExportStatus']['stage']}"
                )
            else:
                print(
                    f"Initial status: {create_data['data_export_status']['stage']}"
                )

        except (json.JSONDecodeError, KeyError) as e:
            pytest.fail(
                f"Could not parse export ID from creation response: {str(e)}"
            )

        # Step 3: List exports and verify our export is in the list
        print("\nListing exports")
        cmd_list = (
            [
                "secops",
            ]
            + common_args
            + ["export", "list", "--page-size", "10"]
        )

        result_list = subprocess.run(
            cmd_list, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            result_list.returncode == 0
        ), f"List exports failed: {result_list.stderr}"

        # Parse the output and verify our export is in the list
        list_data = json.loads(result_list.stdout)
        assert "dataExports" in list_data
        assert list_data["dataExports"] is not None

        # Find our export in the list
        found_in_list = False
        for export_item in list_data["dataExports"]:
            if export_item["name"].split("/")[-1] == export_id:
                found_in_list = True
                break

        if found_in_list:
            print(f"Successfully found export {export_id} in list results")
        else:
            print(
                f"Export {export_id} not found in list results."
                "Could be in other page of list response"
            )

        # Step 4: Get export details
        print("\nGetting export details")
        cmd_get = (
            [
                "secops",
            ]
            + common_args
            + ["export", "status", "--id", export_id]
        )

        result_get = subprocess.run(
            cmd_get, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            result_get.returncode == 0
        ), f"Get export failed: {result_get.stderr}"

        # Parse the output and verify details
        get_data = json.loads(result_get.stdout)
        assert get_data["name"].split("/")[-1] == export_id

        # Get the current status
        if "dataExportStatus" in get_data:
            current_status = get_data["dataExportStatus"]["stage"]
        else:
            current_status = get_data["data_export_status"]["stage"]

        print(f"Current export status: {current_status}")

        # Step 5: Try to update the export if it's in IN_QUEUE state
        if current_status == "IN_QUEUE":
            print("\nUpdating export (since it's in IN_QUEUE state)")

            # Update the start time to a newer time (2 hours after original start)
            new_start_time = initial_start_time + timedelta(hours=2)
            new_start_time_str = new_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            print(
                f"Updating export to use new start time: {new_start_time_str}"
            )
            print(f"Previous start time was: {start_time_str}")

            cmd_update = (
                [
                    "secops",
                ]
                + common_args
                + [
                    "export",
                    "update",
                    "--id",
                    export_id,
                    "--start-time",
                    new_start_time_str,  # Update the start time instead of log types
                ]
            )

            result_update = subprocess.run(
                cmd_update, env=cli_env, capture_output=True, text=True
            )

            # Check that the command executed successfully
            assert (
                result_update.returncode == 0
            ), f"Update export failed: {result_update.stderr}"

            # Parse the output and verify the update
            update_data = json.loads(result_update.stdout)
            assert update_data["name"].split("/")[-1] == export_id

            print("Successfully updated export with new start time")
        else:
            print(
                f"Skipping update test - export status is {current_status}, not IN_QUEUE"
            )

        # Step 6: Cancel the export (cleanup)
        print("\nCancelling export")
        cmd_cancel = (
            [
                "secops",
            ]
            + common_args
            + ["export", "cancel", "--id", export_id]
        )

        result_cancel = subprocess.run(
            cmd_cancel, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            result_cancel.returncode == 0
        ), f"Cancel export failed: {result_cancel.stderr}"

        # Parse the output and verify the cancellation
        cancel_data = json.loads(result_cancel.stdout)
        assert cancel_data["name"].split("/")[-1] == export_id

        # Get the cancelled status
        if "dataExportStatus" in cancel_data:
            cancelled_status = cancel_data["dataExportStatus"]["stage"]
        else:
            cancelled_status = cancel_data["data_export_status"]["stage"]

        print(f"Cancelled export status: {cancelled_status}")
        assert cancelled_status in ["CANCELLING", "CANCELLED"]

    except Exception as e:
        pytest.fail(f"Test failed with error: {str(e)}")

    finally:
        # Cleanup: Try to cancel the export if we haven't already and we have an ID
        if export_id:
            try:
                print(f"\nCleaning up: Cancelling export {export_id}")
                cmd_cleanup = (
                    [
                        "secops",
                    ]
                    + common_args
                    + [
                        "export",
                        "cancel",
                        "--id",
                        export_id,
                    ]
                )
                subprocess.run(
                    cmd_cleanup, env=cli_env, capture_output=True, text=True
                )
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")
