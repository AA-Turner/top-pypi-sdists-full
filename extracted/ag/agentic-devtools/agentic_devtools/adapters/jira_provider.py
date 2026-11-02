"""Jira IssueProvider implementation.

Uses the ``requests`` library for REST API calls, with authentication
following the existing patterns from ``agentic_devtools.tools.jira``.

Conforms to the :class:`~agentic_devtools.adapters.issue_provider.IssueProvider`
protocol (8 methods with keyword-only ``dry_run``).  The ``issue_type_map``
constructor parameter allows instance-specific Jira issue-type name overrides
(e.g., German-localized names) without hard-coding English names.
"""

from __future__ import annotations

from agentic_devtools.adapters.jira_provider_config import _JiraProviderConfigMixin
from agentic_devtools.adapters.jira_provider_creation import _JiraProviderCreationMixin
from agentic_devtools.adapters.jira_provider_creation_recovery import _JiraProviderCreationRecoveryMixin
from agentic_devtools.adapters.jira_provider_dependencies import _JiraProviderDependenciesMixin
from agentic_devtools.adapters.jira_provider_dry_run import _JiraProviderDryRunMixin
from agentic_devtools.adapters.jira_provider_hierarchy import _JiraProviderHierarchyMixin
from agentic_devtools.adapters.jira_provider_http import _JiraProviderHttpMixin
from agentic_devtools.adapters.jira_provider_idempotency import _JiraProviderIdempotencyMixin
from agentic_devtools.adapters.jira_provider_issue_types import _JiraProviderIssueTypesMixin
from agentic_devtools.adapters.jira_provider_labels import _JiraProviderLabelsMixin


class JiraProvider(
    _JiraProviderConfigMixin,
    _JiraProviderHttpMixin,
    _JiraProviderCreationRecoveryMixin,
    _JiraProviderCreationMixin,
    _JiraProviderIssueTypesMixin,
    _JiraProviderHierarchyMixin,
    _JiraProviderDependenciesMixin,
    _JiraProviderLabelsMixin,
    _JiraProviderIdempotencyMixin,
    _JiraProviderDryRunMixin,
):
    """Jira IssueProvider using the Jira REST API v2.

    Conforms to the
    :class:`~agentic_devtools.adapters.issue_provider.IssueProvider` protocol.

    Args:
        project_key: Jira project key (e.g., ``"PROJ"``).  Must be non-empty.
        base_url: Jira instance base URL.  Falls back to ``JIRA_BASE_URL`` env.
            Must be resolvable (non-empty after resolution).
        session: Optional ``requests.Session`` for testing injection.
        issue_type_map: Optional mapping of canonical neutral type keys
            (members of ``VALID_ISSUE_TYPES``) to Jira-native issue-type names.
            Overrides default mappings; unspecified keys fall back to built-in
            defaults.  Values must be non-empty, non-whitespace strings.
    """
