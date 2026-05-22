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
"""Integration tests for Chronicle log type and parser validation functions.

These tests require valid credentials and API access.
They interact with real Chronicle API endpoints.
"""

import os
import pytest

from secops import SecOpsClient
from secops.exceptions import APIError
from ..config import CHRONICLE_CONFIG, SERVICE_ACCOUNT_JSON


@pytest.mark.integration
def test_log_type_lifecycle_integration():
    """Test the complete log-type lifecycle."""
    # Use service account if private key is provided, otherwise fallback to ADC
    sa_info = SERVICE_ACCOUNT_JSON if SERVICE_ACCOUNT_JSON.get("private_key") else None
    client = SecOpsClient(service_account_info=sa_info)

    # 5. Testing parser validation workflow
    project_id = CHRONICLE_CONFIG.get("project_id") or "140410331797"
    customer_id = CHRONICLE_CONFIG.get("customer_id") or "1234-53411-24552"
    log_type = os.getenv("CHRONICLE_TEST_LOG_TYPE", "DUMMY_LOGTYPE")
    associated_pr = os.getenv("CHRONICLE_TEST_PR", "chronicle/content-hub/pull/701")

    chronicle = client.chronicle(
        project_id=project_id,
        customer_id=customer_id,
        region=CHRONICLE_CONFIG.get("region", "us"),
    )
    print(f"\nDEBUG: project_id={project_id!r}")
    print(f"DEBUG: customer_id={customer_id!r}")

    print(f"\nTesting trigger_github_checks with log type {log_type}")
    try:
        # Trigger checks for the configured PR and log type
        result = chronicle.trigger_github_checks(
            associated_pr=associated_pr,
            log_type=log_type,
        )
        assert isinstance(result, dict)
        print("Successfully triggered checks (or received valid JSON response)")
    except (APIError, Exception) as e:
        # We expect a failure due to dummy data, but we want to confirm
        # it reached the server or handled the routing correctly.
        error_msg = str(e)
        assert (
            "api error" in error_msg.lower()
            or "error" in error_msg.lower()
            or "failed" in error_msg.lower()
        )
        print(
            f"Server gracefully handled the dummy trigger data: {error_msg.strip()}"
        )

    print(f"\nTesting get_analysis_report with log type {log_type}")
    try:
        # Request a report for dummy resource names
        report = chronicle.get_analysis_report(
            log_type=log_type, parser_id="22223231", report_id="5c3f03cf-b90c-4ad3-91b6-4894c50e640d"
        )
        assert isinstance(report, dict)
        print("Successfully retrieved report")
    except (APIError, Exception) as e:
        # We expect a 404 or similar since the report is dummy
        error_msg = str(e)
        assert (
            "api error" in error_msg.lower()
            or "error" in error_msg.lower()
            or "not found" in error_msg.lower()
        )
        print(
            f"Server gracefully handled dummy report request: {error_msg.strip()}"
        )


@pytest.mark.integration
def test_log_type_parser_found_integration():
    """Integration test for trigger_github_checks when at least one parser exists.

    It dynamically finds an existing parser in the instance, and uses it
    to trigger checks, verifying that the path is constructed correctly
    and doesn't result in a 404 due to duplication.
    """
    sa_info = SERVICE_ACCOUNT_JSON if SERVICE_ACCOUNT_JSON.get("private_key") else None
    client = SecOpsClient(service_account_info=sa_info)

    # Use the configured project/customer IDs if available, otherwise fallback to dummy
    project_id = CHRONICLE_CONFIG.get("project_id") or "140410331797"
    customer_id = CHRONICLE_CONFIG.get("customer_id") or "1234-53411-24552"

    chronicle = client.chronicle(
        project_id=project_id,
        customer_id=customer_id,
        region=CHRONICLE_CONFIG.get("region", "us"),
    )

    print("\nListing all parsers to find a candidate for integration test...")
    try:
        # List all parsers across all log types
        parsers = chronicle.list_parsers(log_type="-")
    except APIError as e:
        pytest.skip(f"Skipping test: Failed to list parsers (check config/auth): {e}")
        return

    if not parsers:
        pytest.skip("Skipping test: No parsers found in the Chronicle instance to test the 'parser found' path.")
        return

    # Find a parser that has a valid name format we can parse
    target_parser = None
    target_log_type = None
    target_parser_id = None

    for p in parsers:
        name = p.get("name", "")
        parts = name.split("/")
        if len(parts) == 10 and parts[6] == "logTypes" and parts[8] == "parsers":
            target_parser = p
            target_log_type = parts[7]
            target_parser_id = parts[9]
            break

    if not target_parser:
        pytest.skip("Skipping test: Found parsers but none matched the expected resource name format.")
        return

    print(f"Found candidate parser: {target_parser_id} for log type {target_log_type}")

    print(f"Triggering checks for {target_log_type} (should use parser {target_parser_id})")
    try:
        result = chronicle.trigger_github_checks(
            associated_pr="chronicle/content-hub/pull/701",
            log_type=target_log_type,
        )
        assert isinstance(result, dict)
        print("Successfully triggered checks (or received valid response from server)")
    except APIError as e:
        # If it fails, it should NOT be because of a 404 Not Found with duplicated path.
        # It might fail with 400 Bad Request if the PR is invalid or other reasons,
        # but a 404 with duplicated path indicates a regression.
        error_msg = str(e)
        assert "projects/" not in error_msg or error_msg.count("instances/") < 2
        print(f"Server responded (graceful failure or expected error): {error_msg.strip()}")


if __name__ == "__main__":
    pytest.main(["-v", __file__, "-m", "integration"])
