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
"""Integration tests for rule deployment endpoints in Chronicle API.

These tests require valid credentials and API access.
"""
import pytest
from typing import Dict, Any
from secops import SecOpsClient
from ..config import CHRONICLE_CONFIG, SERVICE_ACCOUNT_JSON


@pytest.fixture(scope="module")
def chronicle(service_account_info=SERVICE_ACCOUNT_JSON) -> SecOpsClient:
    """Fixture to create a Chronicle client."""
    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    return client.chronicle(**CHRONICLE_CONFIG)


@pytest.fixture(scope="module")
def rule(chronicle) -> Dict[str, Any]:
    """Fixture to create an test rule."""
    test_rule_text = """
rule test_rule {
    meta:
        description = "Created by secops-wrapper sdk integration tests - test_rule_integration.py"
        author = "test_rule_integration.py"
        severity = "Low"
    events:
        $e.metadata.product_event_type = "force_no_match"
    condition:
        $e
}
"""
    rule = None
    try:
        rule = chronicle.create_rule(test_rule_text)
        rule["ruleId"] = rule["name"].split("/")[-1]
        yield rule
    except Exception as e:  # pylint: disable=broad-exception-caught
        pytest.fail(f"Failed to create test rule: {e}")
    finally:
        try:
            chronicle.delete_rule(rule["ruleId"], force=True)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(
                f"Cleanup failed - deleting test_rule: {rule['rule_id']}: {e}"
            )


def _restore_rule_deployment(chronicle, rule):
    current = chronicle.get_rule_deployment(rule["ruleId"])
    restore = {}
    for key in ["archived", "alerting", "enabled"]:
        if current.get(key, False):
            restore[key] = False

    run_freq = current.get("runFrequency", None)
    if run_freq != "LIVE":
        restore["runFrequency"] = "LIVE"

    if restore:
        try:
            chronicle.update_rule_deployment(rule_id=rule["ruleId"], **restore)
        except Exception:  # pylint: disable=broad-exception-caught
            pytest.fail("Failed to restore deployment - cannot test further")


@pytest.mark.integration
def test_rule_get_deployment_integration(chronicle, rule):
    """Get deployment for the first available rule."""
    result = chronicle.get_rule_deployment(rule["ruleId"])
    assert isinstance(result, dict)
    assert "name" in result


@pytest.mark.integration
def test_rule_list_deployments_integration(chronicle, rule):
    """List rule deployments"""

    # Small page to force pagination when possible
    first = chronicle.list_rule_deployments(page_size=1)
    assert isinstance(first, dict)
    deployments = first.get("ruleDeployments", [])
    assert isinstance(deployments[0], dict)

    # If there's a next page token, fetch the next page and ensure pagination works
    token = first.get("nextPageToken")
    if token:
        second = chronicle.list_rule_deployments(page_size=1, page_token=token)
        assert isinstance(second, dict)
        deployments2 = second.get("ruleDeployments", [])
        if deployments and deployments2:
            # First items from each page should differ
            assert deployments[0].get("name") != deployments2[0].get("name")


@pytest.mark.integration
def test_rule_update_deployment_archived_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    deployment = chronicle.update_rule_deployment(
        rule_id=rule["ruleId"], archived=True
    )
    assert deployment.get("archived", False) is True
    assert deployment.get("enabled", False) is False
    assert deployment.get("alerting", False) is False


@pytest.mark.integration
def test_rule_update_deployment_alerting_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    deployment = chronicle.update_rule_deployment(
        rule_id=rule["ruleId"], alerting=True
    )
    assert deployment.get("alerting", False) is True
    assert deployment.get("enabled", False) is False
    assert deployment.get("archived", False) is False


@pytest.mark.integration
def test_rule_update_deployment_enabled_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    deployment = chronicle.update_rule_deployment(
        rule_id=rule["ruleId"], enabled=True
    )
    assert deployment.get("enabled", False) is True
    assert deployment.get("alerting", False) is False
    assert deployment.get("archived", False) is False


@pytest.mark.integration
def test_rule_archive_failure_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    with pytest.raises(Exception):
        chronicle.update_rule_deployment(rule_id=rule["ruleId"], enabled=True)
        chronicle.update_rule_deployment(rule_id=rule["ruleId"], archived=True)


@pytest.mark.integration
def test_rule_update_deployment_failure_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    with pytest.raises(Exception):
        chronicle.update_rule_deployment(
            rule_id=rule["ruleId"], archived=True, enabled=True, alerting=False
        )


@pytest.mark.integration
def test_rule_update_deployment_multiple_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    deployment = chronicle.update_rule_deployment(
        rule_id=rule["ruleId"], alerting=True, enabled=True, archived=False
    )
    assert deployment.get("alerting", False) is True
    assert deployment.get("enabled", False) is True
    assert deployment.get("archived", False) is False


@pytest.mark.integration
def test_rule_already_set_deployment_integration(chronicle, rule):
    _restore_rule_deployment(chronicle, rule)
    with pytest.raises(Exception):
        chronicle.update_rule_deployment(
            rule_id=rule["ruleId"],
            alerting=False,
            enabled=False,
            archived=False,
        )


@pytest.mark.integration
@pytest.mark.parametrize("target", ["DAILY", "HOURLY", "LIVE"])
def test_rule_update_deployment_run_frequency_integration(
    target, chronicle, rule
):
    rule_id = rule["ruleId"]
    res = chronicle.update_rule_deployment(
        rule_id=rule_id, run_frequency=target
    )
    assert res.get("runFrequency") == target


@pytest.mark.integration
def test_rule_update_deployment_run_frequency_failure_integration(
    chronicle, rule
):
    with pytest.raises(Exception):
        chronicle.update_rule_deployment(
            rule_id=rule["ruleId"], run_frequency="INVALID"
        )
