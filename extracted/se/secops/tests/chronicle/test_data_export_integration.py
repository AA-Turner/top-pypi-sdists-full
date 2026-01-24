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
"""Integration tests for Chronicle Data Export API functionality."""

import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any

import pytest

from secops import SecOpsClient
from secops.exceptions import APIError
from ..config import CHRONICLE_CONFIG, SERVICE_ACCOUNT_JSON

# Get GCS bucket from environment or use default
GCS_BUCKET_NAME = os.environ.get(
    "TEST_GCS_BUCKET", "gcs-exports-prober-bucket-us"
)


@pytest.mark.integration
def test_fetch_available_log_types():
    """Test fetching available log types for export."""
    if (
        not CHRONICLE_CONFIG["customer_id"]
        or not CHRONICLE_CONFIG["project_id"]
    ):
        pytest.skip(
            "CHRONICLE_CUSTOMER_ID and CHRONICLE_PROJECT_ID environment variables must be set"
        )
    if not SERVICE_ACCOUNT_JSON:
        pytest.skip(
            "CHRONICLE_SERVICE_ACCOUNT environment variable must be set"
        )

    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    chronicle = client.chronicle(**CHRONICLE_CONFIG)

    try:
        # Set up time range for testing
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=14)  # Look back 14 days

        # Fetch available log types
        result = chronicle.fetch_available_log_types(
            start_time=start_time,
            end_time=end_time,
            page_size=10,  # Limit to 10 for testing
        )

        # Verify the response structure
        assert "available_log_types" in result
        assert isinstance(result["available_log_types"], list)

        print(
            f"\nFound {len(result['available_log_types'])} available log types for export"
        )

        # Show some log types if available
        if result["available_log_types"]:
            for log_type in result["available_log_types"][:3]:  # Show first 3
                print(
                    f"  {log_type.display_name} ({log_type.log_type.split('/')[-1]})"
                )
                print(
                    f"  Available from {log_type.start_time} to {log_type.end_time}"
                )

    except APIError as e:
        # If we get API errors unrelated to configuration, fail the test
        pytest.fail(f"API Error during fetch_available_log_types test: {e}")


@pytest.mark.integration
def test_data_export_lifecycle():
    """Test the complete lifecycle of a data export."""
    if (
        not CHRONICLE_CONFIG["customer_id"]
        or not CHRONICLE_CONFIG["project_id"]
    ):
        pytest.skip(
            "CHRONICLE_CUSTOMER_ID and CHRONICLE_PROJECT_ID environment variables must be set"
        )
    if not SERVICE_ACCOUNT_JSON:
        pytest.skip(
            "CHRONICLE_SERVICE_ACCOUNT environment variable must be set"
        )

    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    chronicle = client.chronicle(**CHRONICLE_CONFIG)

    # Variables to track resources we need to clean up
    export_id = None

    try:
        # Set up time range for testing
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=1)  # Look back 1 day
        bucket_path = (
            f"projects/{CHRONICLE_CONFIG['project_id']}/"
            f"buckets/{GCS_BUCKET_NAME}"
        )

        # Step 1: Create a data export with all logs
        print("\nStep 1: Creating data export with all logs")
        export = chronicle.create_data_export(
            gcs_bucket=bucket_path,
            start_time=start_time,
            end_time=end_time,
            export_all_logs=True,  # Using export_all_logs parameter as requested
        )

        # Get the export ID for subsequent operations and cleanup
        export_id = export["name"].split("/")[-1]
        print(f"Created export with ID: {export_id}")

        # Verify the response structure
        assert "name" in export
        if "dataExportStatus" in export:
            assert "stage" in export["dataExportStatus"]
            print(f"Status: {export['dataExportStatus']['stage']}")
        else:
            assert "stage" in export["data_export_status"]
            print(f"Status: {export['data_export_status']['stage']}")

        # Store initial start time for later verification of update
        initial_start_time = start_time

        # Step 2: Get the export details
        print("\nStep 2: Getting export details")
        export_details = chronicle.get_data_export(export_id)

        # Verify the response structure
        assert "name" in export_details
        assert export_details["name"].endswith(export_id)

        # Get status information
        if "dataExportStatus" in export_details:
            stage = export_details["dataExportStatus"]["stage"]
        else:
            stage = export_details["data_export_status"]["stage"]

        print(f"Export status: {stage}")

        # Step 3: List exports
        print("\nStep 3: Listing recent exports")
        list_result = chronicle.list_data_export(page_size=5)

        # Verify the response structure
        assert "dataExports" in list_result
        assert isinstance(list_result["dataExports"], list)

        # Verify our export is in the list
        found_export = False
        for item in list_result["dataExports"]:
            if item["name"].endswith(export_id):
                found_export = True
                break

        if found_export:
            print(f"Successfully found export {export_id} in list results")
        else:
            print(
                f"Export {export_id} not found in list results."
                "Could be in other page of list response"
            )

        # Step 4: Update the export if it's in IN_QUEUE state
        if stage == "IN_QUEUE":
            print("\nStep 4: Updating export (since it's in IN_QUEUE state)")

            # Update the start time to a newer time (2 hours after original start)
            new_start_time = initial_start_time + timedelta(hours=2)

            print(
                f"Updating export to use new start time: {new_start_time.isoformat()}"
            )
            print(f"Previous start time was: {initial_start_time.isoformat()}")

            update_result = chronicle.update_data_export(
                data_export_id=export_id,
                start_time=new_start_time,  # Update the start time instead of log types
            )

            # Verify the response structure
            assert "name" in update_result
            assert update_result["name"].endswith(export_id)

            # Get the updated status
            if "dataExportStatus" in update_result:
                updated_stage = update_result["dataExportStatus"]["stage"]
            else:
                updated_stage = update_result["data_export_status"]["stage"]

            print(f"Updated export status: {updated_stage}")
        else:
            print(
                f"\nSkipping update test - export status is {stage}, not IN_QUEUE"
            )

        # Final Step: Cancel the export (cleanup)
        print("\nFinal Step: Cancelling the export")
        cancel_result = chronicle.cancel_data_export(export_id)

        # Verify the response structure
        assert "name" in cancel_result
        assert cancel_result["name"].endswith(export_id)

        # Get the cancelled status
        if "dataExportStatus" in cancel_result:
            cancelled_stage = cancel_result["dataExportStatus"]["stage"]
        else:
            cancelled_stage = cancel_result["data_export_status"]["stage"]

        print(f"Cancelled export status: {cancelled_stage}")
        assert cancelled_stage in [
            "CANCELLING",
            "CANCELLED",
        ], f"Expected export to be in CANCELLING or CANCELLED state, got {cancelled_stage}"

    except APIError as e:
        print(f"\nAPI Error during data_export_lifecycle test: {e}")
        pytest.fail(f"API Error: {e}")

    finally:
        # Cleanup: Try to cancel the export if we haven't already
        if export_id and stage not in ["CANCELLING", "CANCELLED"]:
            try:
                print(f"\nCleaning up: Cancelling export {export_id}")
                chronicle.cancel_data_export(export_id)
            except APIError as e:
                print(f"Error during cleanup: {e}")
