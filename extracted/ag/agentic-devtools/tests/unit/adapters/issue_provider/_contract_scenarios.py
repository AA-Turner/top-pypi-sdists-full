"""Shared, provider-agnostic contract scenarios for IssueProvider implementations.

This module is intentionally **not** collected by pytest — the leading underscore
in the filename keeps it out of the ``test_*.py`` collection glob.  Concrete
provider test files subclass the ``TestContract*`` mixins below and supply a
``provider`` fixture plus a small set of hook methods:

Required hooks (all providers):
    * ``provider`` — a pytest fixture yielding a ready-to-use provider instance.
    * ``seed_issue(provider) -> str`` — create a ``"task"`` issue and return its
      identifier (must be resolvable and mutable).
    * ``seed_two_issues(provider) -> tuple[str, str]`` — create two distinct
      issues and return ``(first_id, second_id)``.
    * ``boundary_calls(provider) -> int`` — number of provider-boundary calls
      made so far (HTTP requests / subprocess invocations).  In-memory providers
      return ``0``.
    * ``sample_identifier`` — a class attribute holding an identifier valid for
      ``normalize_identifier`` / ``format_identifier``.

Additional hooks for the error-path mixins (jira + github only):
    * ``make_transient_create_provider() -> provider`` — a provider whose
      ``create_issue`` raises a transient error.
    * ``make_non_transient_create_provider() -> provider`` — a provider whose
      ``create_issue`` raises a non-transient error.
    * ``non_transient_exc_type`` — a class attribute naming the expected
      non-transient exception type.

Assertions are deliberately provider-agnostic: they check statuses, non-empty
identifiers, dry-run semantics, and result types.  Provider-native metadata
checks (e.g. ``metadata["issue_type"]`` for Jira/InMemory vs
``metadata["label"]`` for GitHub) belong in the provider-specific test files.
"""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import (
    ProviderIssueResult,
    ProviderLinkResult,
)
from agentic_devtools.adapters.retry import TransientError

# A 64-char hex idempotency key: valid both as a Jira/InMemory dedup cache key
# and as a GitHub orchestration key (the ``embed``/``extract`` marker regex
# requires exactly 64 hex characters).
_IDEMPOTENCY_KEY = "a" * 64

# Patch target for the retry backoff sleep so error-path retries do not block.
_SLEEP_TARGET = "agentic_devtools.adapters.retry.time.sleep"


class TestContractCreateIssue:
    """``create_issue`` returns ``status="created"`` with a non-empty identifier."""

    def test_contract_create_issue_created(self, provider):
        result = provider.create_issue("Contract Title", "Contract body", "task")
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "created"
        assert result.identifier


class TestContractCreateIssueDryRun:
    """``create_issue(dry_run=True)`` previews without any provider call."""

    def test_contract_create_issue_dry_run(self, provider):
        before = self.boundary_calls(provider)
        result = provider.create_issue("Contract Title", "Contract body", "task", dry_run=True)
        assert result.status == "dry-run"
        assert self.boundary_calls(provider) == before


class TestContractCreateIssueIdempotent:
    """A duplicate ``idempotency_key`` returns ``status="existing"`` with the same id."""

    def test_contract_create_issue_idempotent(self, provider):
        first = provider.create_issue("Idem", "Idem body", "task", idempotency_key=_IDEMPOTENCY_KEY)
        second = provider.create_issue("Idem", "Idem body", "task", idempotency_key=_IDEMPOTENCY_KEY)
        assert second.status == "existing"
        assert second.identifier == first.identifier


class TestContractSetIssueType:
    """``set_issue_type`` with an already-set type returns ``status="no-op"``."""

    def test_contract_set_issue_type(self, provider):
        identifier = self.seed_issue(provider)
        provider.set_issue_type(identifier, "task")
        result = provider.set_issue_type(identifier, "task")
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "no-op"
        assert result.identifier


class TestContractSetIssueTypeTransition:
    """Setting a different type returns ``status="updated"``."""

    def test_contract_set_issue_type_transition(self, provider):
        identifier = self.seed_issue(provider)
        provider.set_issue_type(identifier, "task")
        result = provider.set_issue_type(identifier, "bug")
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "updated"
        assert result.identifier


class TestContractSetIssueTypeDryRun:
    """``set_issue_type(dry_run=True)`` returns ``status="dry-run"`` with no provider call."""

    def test_contract_set_issue_type_dry_run(self, provider):
        identifier = self.seed_issue(provider)
        before = self.boundary_calls(provider)
        result = provider.set_issue_type(identifier, "task", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier
        assert self.boundary_calls(provider) == before


class TestContractLinkSubissue:
    """``link_subissue`` returns ``status="linked"`` with domain source/target ids."""

    def test_contract_link_subissue(self, provider):
        parent_id, child_id = self.seed_two_issues(provider)
        result = provider.link_subissue(parent_id, child_id)
        assert isinstance(result, ProviderLinkResult)
        assert result.status == "linked"
        assert result.source_id == parent_id
        assert result.target_id == child_id


class TestContractLinkSubissueDryRun:
    """``link_subissue(dry_run=True)`` returns ``status="dry-run"`` with no provider call."""

    def test_contract_link_subissue_dry_run(self, provider):
        parent_id, child_id = self.seed_two_issues(provider)
        before = self.boundary_calls(provider)
        result = provider.link_subissue(parent_id, child_id, dry_run=True)
        assert result.status == "dry-run"
        assert self.boundary_calls(provider) == before


class TestContractAddBlockedBy:
    """``add_blocked_by`` returns ``status="linked"``."""

    def test_contract_add_blocked_by(self, provider):
        issue_id, blocker_id = self.seed_two_issues(provider)
        result = provider.add_blocked_by(issue_id, blocker_id)
        assert isinstance(result, ProviderLinkResult)
        assert result.status == "linked"


class TestContractAddBlockedByDryRun:
    """``add_blocked_by(dry_run=True)`` returns ``status="dry-run"`` with no provider call."""

    def test_contract_add_blocked_by_dry_run(self, provider):
        issue_id, blocker_id = self.seed_two_issues(provider)
        before = self.boundary_calls(provider)
        result = provider.add_blocked_by(issue_id, blocker_id, dry_run=True)
        assert result.status == "dry-run"
        assert self.boundary_calls(provider) == before


class TestContractApplyLabels:
    """``apply_labels`` returns ``status`` in {"updated", "no-op"} with sorted labels."""

    def test_contract_apply_labels(self, provider):
        identifier = self.seed_issue(provider)
        result = provider.apply_labels(identifier, ["contract-label"])
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "updated"
        assert result.metadata["labels"] == sorted(result.metadata["labels"])
        assert "contract-label" in result.metadata["labels"]


class TestContractApplyLabelsDryRun:
    """``apply_labels(dry_run=True)`` previews sorted requested labels, no mutation call."""

    def test_contract_apply_labels_dry_run(self, provider):
        identifier = self.seed_issue(provider)
        before = self.boundary_calls(provider)
        result = provider.apply_labels(identifier, ["b-label", "a-label"], dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["labels"] == ["a-label", "b-label"]
        assert self.boundary_calls(provider) == before


class TestContractApplyLabelsIdempotent:
    """Re-applying an already-present label returns ``status="no-op"``."""

    def test_contract_apply_labels_idempotent(self, provider):
        identifier = self.seed_issue(provider)
        provider.apply_labels(identifier, ["contract-label"])
        result = provider.apply_labels(identifier, ["contract-label"])
        assert result.status == "no-op"
        assert "contract-label" in result.metadata["labels"]


class TestContractIdempotentRelink:
    """Re-linking an existing parent/child returns ``status="already-linked"``."""

    def test_contract_idempotent_relink(self, provider):
        parent_id, child_id = self.seed_two_issues(provider)
        provider.link_subissue(parent_id, child_id)
        result = provider.link_subissue(parent_id, child_id)
        assert result.status == "already-linked"


class TestContractIdempotentBlockedBy:
    """Re-declaring an existing dependency returns ``status="already-linked"``."""

    def test_contract_idempotent_blocked_by(self, provider):
        issue_id, blocker_id = self.seed_two_issues(provider)
        provider.add_blocked_by(issue_id, blocker_id)
        result = provider.add_blocked_by(issue_id, blocker_id)
        assert result.status == "already-linked"


class TestContractResolveIdentifier:
    """``resolve_identifier`` returns ``status="resolved"`` with a populated internal id."""

    def test_contract_resolve_identifier(self, provider):
        identifier = self.seed_issue(provider)
        result = provider.resolve_identifier(identifier)
        assert result.status == "resolved"
        assert result.metadata["internal_id"]


class TestContractResolveIdentifierDryRun:
    """``resolve_identifier(dry_run=True)`` returns ``status="dry-run"`` with no provider call."""

    def test_contract_resolve_identifier_dry_run(self, provider):
        identifier = self.seed_issue(provider)
        before = self.boundary_calls(provider)
        result = provider.resolve_identifier(identifier, dry_run=True)
        assert result.status == "dry-run"
        assert self.boundary_calls(provider) == before


class TestContractNormalizeIdentifier:
    """``normalize_identifier`` returns a str and is idempotent."""

    def test_contract_normalize_identifier(self, provider):
        normalized = provider.normalize_identifier(self.sample_identifier)
        assert isinstance(normalized, str)
        assert provider.normalize_identifier(normalized) == normalized


class TestContractFormatIdentifier:
    """``format_identifier`` returns a non-empty str."""

    def test_contract_format_identifier(self, provider):
        formatted = provider.format_identifier(self.sample_identifier)
        assert isinstance(formatted, str)
        assert formatted


class TestContractTransientError:
    """``create_issue`` raises ``TransientError`` on a transient API failure.

    Scoped to jira + github only — InMemory has no HTTP boundary or retry layer.
    """

    def test_contract_transient_error(self, monkeypatch):
        monkeypatch.setattr(_SLEEP_TARGET, lambda *a, **k: None)
        provider = self.make_transient_create_provider()
        with pytest.raises(TransientError):
            provider.create_issue("Transient", "Body", "task")


class TestContractNonTransientApiFailure:
    """``create_issue`` raises a non-transient exception on a non-transient failure.

    Scoped to jira + github only (see ``TestContractTransientError``).
    """

    def test_contract_non_transient_api_failure(self, monkeypatch):
        monkeypatch.setattr(_SLEEP_TARGET, lambda *a, **k: None)
        provider = self.make_non_transient_create_provider()
        with pytest.raises(self.non_transient_exc_type) as exc_info:
            provider.create_issue("NonTransient", "Body", "task")
        assert not isinstance(exc_info.value, TransientError)
