#!/usr/bin/env python3
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
"""Integration test for the SecOps CLI rule deployment commands."""

import json
import os
import subprocess
import tempfile
import time
import uuid

import pytest


@pytest.mark.integration
def test_cli_rule_deployment_workflow(cli_env, common_args):
    """Test the rule deployment CLI commands workflow.

    This test covers the following flow:
    1. Create a rule
    2. Update it to enable it
    3. List deployments
    4. Identify our created rule in the deployments list
    5. Set alerting for the rule to True
    6. Get deployment details for the created rule
    7. Clean up the created rule

    Args:
        cli_env: Environment variables for CLI execution.
        common_args: Common CLI arguments.
    """

    # YARA-L rule text
    rule_text = """
rule test_cli_rule {
    meta:
        description = "Updated test rule for CLI testing"
        author = "CLI Test"
        severity = "Medium"
        yara_version = "YL2.0"
        rule_version = "1.1"
    events:
        $e.metadata.event_type = "NETWORK_CONNECTION"
    condition:
        $e
}
"""

    rule_id = None

    # Create a temporary file for the rule text
    rule_file = None

    try:
        # Create a temporary file with the rule text
        rule_file_name = None
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".yaral"
        ) as rf:
            rf.write(rule_text)
            rule_file_name = rf.name

        # 1. Create a rule
        print("\n1. Creating test rule")
        create_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "rule",
                "create",
                "--file",
                rule_file_name,
            ]
        )

        create_result = subprocess.run(
            create_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            create_result.returncode == 0
        ), f"Command failed: {create_result.stderr}"

        # Parse the output to get the rule ID
        rule_data = json.loads(create_result.stdout)
        assert "name" in rule_data, "Missing rule name in create response"
        rule_id = rule_data["name"].split("/")[-1]
        print(f"Created rule with ID: {rule_id}")

        # Wait briefly for the rule to be fully created
        time.sleep(5)

        # 2. Update rule to enable it
        print("\n2. Enabling the rule")
        enable_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "rule",
                "update-deployment",
                "--id",
                rule_id,
                "--enabled",
                "true",
            ]
        )

        enable_result = subprocess.run(
            enable_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            enable_result.returncode == 0
        ), f"Command failed: {enable_result.stderr}"

        # Verify rule was enabled
        enable_data = json.loads(enable_result.stdout)
        assert enable_data.get("enabled") is True, "Rule was not enabled"
        print("Successfully enabled the rule")

        # Wait briefly for the deployment update to take effect
        time.sleep(2)

        # 3. List deployments
        print("\n3. Listing rule deployments")
        list_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "rule",
                "list-deployments",
            ]
        )

        list_result = subprocess.run(
            list_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            list_result.returncode == 0
        ), f"Command failed: {list_result.stderr}"

        # Parse the output
        list_data = json.loads(list_result.stdout)
        assert (
            "ruleDeployments" in list_data
        ), "Missing ruleDeployments in response"

        # 4. Identify our rule in the deployments list
        print("\n4. Finding our rule in the deployments list")
        deployment_found = False
        for deployment in list_data.get("ruleDeployments", []):
            if rule_id in deployment.get("name", ""):
                deployment_found = True
                print(f"Found deployment for rule: {rule_id}")
                break

        assert (
            deployment_found
        ), f"Could not find deployment for rule: {rule_id}"

        # 5. Set alerting for the rule to True
        print("\n5. Setting alerting for the rule")
        alert_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "rule",
                "alerting",
                "--id",
                rule_id,
                "--enabled",
                "true",
            ]
        )

        alert_result = subprocess.run(
            alert_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            alert_result.returncode == 0
        ), f"Command failed: {alert_result.stderr}"

        # Verify alerting was set
        alert_data = json.loads(alert_result.stdout)
        print(alert_data)
        assert alert_data.get("alerting", False), "Alerting was not enabled"
        print("Successfully set alerting for the rule")

        # Wait briefly for the alerting update to take effect
        time.sleep(2)

        # 6. Get deployment details for the created rule
        print("\n6. Getting specific rule deployment")
        get_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "rule",
                "get-deployment",
                "--id",
                rule_id,
            ]
        )

        get_result = subprocess.run(
            get_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert (
            get_result.returncode == 0
        ), f"Command failed: {get_result.stderr}"

        # Parse and verify the output
        deployment_data = json.loads(get_result.stdout)

        # Verify the deployment data has expected fields
        assert rule_id in deployment_data.get(
            "name", ""
        ), f"Rule ID {rule_id} not found in deployment data"
        assert deployment_data.get(
            "enabled", False
        ), "Rule not showing as enabled"
        assert deployment_data.get(
            "alerting", False
        ), "Alerting not showing as enabled"

        print("Successfully verified deployment details")

    finally:
        # 7. Clean up: Delete the rule and temporary file
        if rule_id:
            print("\n7. Cleaning up: Deleting rule")
            delete_cmd = (
                [
                    "secops",
                ]
                + common_args
                + [
                    "rule",
                    "delete",
                    "--id",
                    rule_id,
                    "--force",  # Force deletion even if rule has associated resources
                ]
            )

            delete_result = subprocess.run(
                delete_cmd, env=cli_env, capture_output=True, text=True
            )

            if delete_result.returncode == 0:
                print(f"Successfully deleted rule: {rule_id}")
            else:
                print(f"Warning: Failed to delete rule: {delete_result.stderr}")

        # Clean up the temporary rule file
        if rule_file_name and os.path.exists(rule_file_name):
            try:
                os.unlink(rule_file_name)
                print(f"Temporary rule file removed: {rule_file_name}")
            except Exception as e:
                print(f"Warning: Failed to remove temporary file: {e}")
