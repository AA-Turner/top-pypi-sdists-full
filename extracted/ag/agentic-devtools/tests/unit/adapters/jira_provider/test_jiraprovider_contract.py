"""Contract tests for JiraProvider's stable module and method API."""

from __future__ import annotations

import inspect

from agentic_devtools.adapters.jira_provider import JiraProvider

_EXPECTED_SIGNATURES = {
    "add_blocked_by": (
        "(self, issue_id: 'str', blocked_by_id: 'str', *, dry_run: 'bool' = False) -> 'ProviderLinkResult'"
    ),
    "apply_labels": (
        "(self, identifier: 'str', labels: 'list[str]', *, dry_run: 'bool' = False) -> 'ProviderIssueResult'"
    ),
    "create_issue": (
        "(self, title: 'str', body: 'str', issue_type: 'str', *, parent_id: 'str | None' = None, "
        "labels: 'list[str] | None' = None, idempotency_key: 'str | None' = None, "
        "precreate_lookup: 'PreCreateLookup | None' = None, dry_run: 'bool' = False) -> 'ProviderIssueResult'"
    ),
    "create_issue_with_precreate_lookup": (
        "(self, title: 'str', body: 'str', issue_type: 'str', *, parent_id: 'str | None' = None, "
        "labels: 'list[str] | None' = None, idempotency_key: 'str | None' = None, "
        "precreate_lookup: 'PreCreateLookup', dry_run: 'bool' = False) -> 'ProviderIssueResult'"
    ),
    "find_existing_dependency": (
        "(self, issue_provider_id: 'str', blocked_by_provider_id: 'str') -> 'ProviderLinkResult | None'"
    ),
    "find_existing_issue": "(self, orchestration_key: 'str') -> 'ProviderIssueResult | None'",
    "find_existing_link": (
        "(self, parent_provider_id: 'str', child_provider_id: 'str') -> 'ProviderLinkResult | None'"
    ),
    "format_identifier": "(self, identifier: 'str') -> 'str'",
    "get_dry_run_manifest": "(self) -> 'dict[str, Any]'",
    "link_subissue": "(self, parent_id: 'str', child_id: 'str', *, dry_run: 'bool' = False) -> 'ProviderLinkResult'",
    "normalize_identifier": "(self, identifier: 'str') -> 'str'",
    "resolve_identifier": "(self, identifier: 'str', *, dry_run: 'bool' = False) -> 'ProviderIssueResult'",
    "set_issue_type": (
        "(self, identifier: 'str', issue_type: 'str', *, dry_run: 'bool' = False) -> 'ProviderIssueResult'"
    ),
    "validate_hierarchy_pair": "(self, child_type: 'str', parent_type: 'str') -> 'None'",
    "validate_issue_type": "(self, issue_type: 'str') -> 'None'",
}


def test_jiraprovider_keeps_its_public_module_identity() -> None:
    assert JiraProvider.__module__ == "agentic_devtools.adapters.jira_provider"


def test_jiraprovider_constructor_signature_is_unchanged() -> None:
    assert str(inspect.signature(JiraProvider)) == (
        "(project_key: 'str', base_url: 'str | None' = None, "
        "session: 'requests_lib.Session | None' = None, "
        "issue_type_map: 'dict[str, str] | None' = None) -> 'None'"
    )


def test_jiraprovider_public_method_signatures_are_unchanged() -> None:
    actual = {
        name: str(inspect.signature(method))
        for name, method in inspect.getmembers(JiraProvider, inspect.isfunction)
        if not name.startswith("_")
    }
    assert actual == _EXPECTED_SIGNATURES
