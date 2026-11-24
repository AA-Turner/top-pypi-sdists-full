"""A tool refusal that names the caller's own values or the person's own setup is never filed.

Red before (2026-11-17): live ``tool_execution_failed`` system_errors were a person's unconnected
Cerbo (``not_connected``), a browser someone else was driving (``controlled_by_other``), a person with
no Cloud Computer yet (``cloud_computer_required``), the records store refusing a non-id value
(``store_22P02``) or a missing referenced row (``store_23503``), and a kind-component patch whose
anchor moved (``kindcomp_patch_code`` / ``patch_no_match``). Each sentence tells the model what to do.
A real fault of the same tools still files."""

from __future__ import annotations

import pytest

from matrx_ai.tools.executor import _is_expected_domain_failure


@pytest.mark.parametrize(
    ("tool_name", "error_type", "message"),
    [
        ("cerbo_get_patient", "not_connected", "Cerbo is not connected for you."),
        ("use_tool", "bundle_not_connected", "The person has not connected Linear, so its tools cannot be loaded."),
        ("cloud_browser", "controlled_by_other", "A person is controlling this browser"),
        ("cloud_browser", "cloud_computer_required", "You don't have a Cloud Computer yet"),
        ("records", "store_22P02", "`records[0].to` must be an id such as 3fa99c97-943a-447b-831b-496b65312afb"),
        ("records", "store_23503", "There is no such form in this organization."),
        ("kindcomp_patch_code", "patch_no_match", "Patch 0 ('patch 1') failed: No match"),
        ("cerbo_list_changes", "connection_credentials_refused", "Cerbo did not accept that API key pair."),
        ("ask_person", "payload_invalid", "That approve request does not match its shape: action: Field required"),
        ("mandate_call", "run_approval_required", "Agent 'Analyst' is on hold (run_approval_required): waits for approval"),
        ("agent", "usage_limit_reached", "Agent 'Analyst' is on hold (usage_limit_reached): limit reached"),
    ],
)
def test_the_callers_or_persons_own_state_is_not_filed(tool_name: str, error_type: str, message: str) -> None:
    assert _is_expected_domain_failure(tool_name=tool_name, error_type=error_type, message=message)


@pytest.mark.parametrize(
    ("tool_name", "error_type"),
    [
        ("cloud_browser", "worker_unreachable"),
        ("cloud_browser", "browser_action_failed"),
        ("records", "store_55P03"),
        ("records", "store_25P02"),
        ("records", "execution"),
        ("cerbo_get_patient", "unavailable"),
        ("cerbo_list_changes", "auth"),
        ("ask_person", "configuration"),
        ("records", "payload_invalid"),
        ("mandate_call", "agent_execution"),
        ("agent", "agent_has_no_model"),
    ],
)
def test_a_real_fault_still_files(tool_name: str, error_type: str) -> None:
    assert not _is_expected_domain_failure(tool_name=tool_name, error_type=error_type, message="x")
