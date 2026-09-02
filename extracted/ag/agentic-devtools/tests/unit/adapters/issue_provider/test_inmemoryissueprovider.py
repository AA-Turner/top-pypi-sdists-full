"""Tests for InMemoryIssueProvider (FR-009/SC-001 conformance)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import (
    InMemoryIssueProvider,
    IssueProvider,
    ProviderIssueResult,
    ProviderLinkResult,
)


class TestInMemoryIssueProviderProtocol:
    """Verify InMemoryIssueProvider satisfies the IssueProvider protocol."""

    def test_isinstance_check(self):
        provider = InMemoryIssueProvider()
        assert isinstance(provider, IssueProvider)

    def test_jira_style_isinstance(self):
        provider = InMemoryIssueProvider(identifier_style="jira")
        assert isinstance(provider, IssueProvider)

    def test_invalid_identifier_style_raises_value_error(self):
        with pytest.raises(ValueError, match="identifier_style"):
            InMemoryIssueProvider(identifier_style="invalid")

    def test_invalid_identifier_style_message_lists_valid_options(self):
        with pytest.raises(ValueError, match=r"github.*jira|jira.*github"):
            InMemoryIssueProvider(identifier_style="unknown")


class TestInMemoryIssueProviderCreateIssue:
    """Tests for InMemoryIssueProvider.create_issue."""

    def test_basic_creation(self):
        provider = InMemoryIssueProvider()
        result = provider.create_issue("My Issue", "Body text", "task")
        assert result.status == "created"
        assert result.identifier == "1"
        assert "fake.test" in result.url
        assert isinstance(result, ProviderIssueResult)

    def test_sequential_identifiers(self):
        provider = InMemoryIssueProvider()
        r1 = provider.create_issue("First", "", "task")
        r2 = provider.create_issue("Second", "", "bug")
        assert r1.identifier == "1"
        assert r2.identifier == "2"

    def test_empty_title_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="title"):
            provider.create_issue("", "body", "task")

    def test_whitespace_title_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="title"):
            provider.create_issue("   ", "body", "task")

    def test_unsupported_issue_type_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="Unsupported issue_type"):
            provider.create_issue("Title", "body", "story")

    def test_unsupported_issue_type_shows_sorted_valid_types(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match=r"\['bug', 'epic', 'feature', 'subtask', 'task'\]"):
            provider.create_issue("Title", "body", "invalid")

    def test_empty_parent_id_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="parent_id"):
            provider.create_issue("Title", "body", "task", parent_id="")

    def test_whitespace_parent_id_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="parent_id"):
            provider.create_issue("Title", "body", "task", parent_id="  ")

    def test_idempotency_dedup(self):
        provider = InMemoryIssueProvider()
        r1 = provider.create_issue("Title", "body", "task", idempotency_key="key-1")
        r2 = provider.create_issue("Title", "body", "task", idempotency_key="key-1")
        assert r1.status == "created"
        assert r2.status == "existing"
        assert r1.identifier == r2.identifier

    def test_labels_at_creation(self):
        provider = InMemoryIssueProvider()
        result = provider.create_issue("Title", "body", "task", labels=["urgent", "bug"])
        assert result.metadata["labels"] == ["bug", "urgent"]

    def test_duplicate_labels_at_creation_are_deduplicated(self):
        """FR-011: labels stored and returned as a sorted unique set, consistent with apply_labels."""
        provider = InMemoryIssueProvider()
        result = provider.create_issue("Title", "body", "task", labels=["bug", "bug", "urgent", "bug"])
        assert result.metadata["labels"] == ["bug", "urgent"]
        assert provider.issues["1"]["labels"] == ["bug", "urgent"]

    def test_dry_run(self):
        provider = InMemoryIssueProvider()
        result = provider.create_issue("Title", "body", "task", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == ""
        assert result.url == ""
        assert provider.issues == {}


class TestInMemoryIssueProviderLinkSubissue:
    """Tests for InMemoryIssueProvider.link_subissue."""

    def _create_two_issues(self, provider):
        provider.create_issue("Parent", "", "epic")
        provider.create_issue("Child", "", "task")

    def test_nominal_link(self):
        provider = InMemoryIssueProvider()
        self._create_two_issues(provider)
        result = provider.link_subissue("1", "2")
        assert result.status == "linked"
        assert result.source_id == "1"
        assert result.target_id == "2"
        assert isinstance(result, ProviderLinkResult)

    def test_duplicate_link(self):
        provider = InMemoryIssueProvider()
        self._create_two_issues(provider)
        provider.link_subissue("1", "2")
        result = provider.link_subissue("1", "2")
        assert result.status == "already-linked"

    def test_missing_parent_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Child", "", "task")
        with pytest.raises(ValueError, match="Parent issue"):
            provider.link_subissue("99", "1")

    def test_missing_child_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Parent", "", "epic")
        with pytest.raises(ValueError, match="Child issue"):
            provider.link_subissue("1", "99")

    def test_empty_parent_id_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="parent_id"):
            provider.link_subissue("", "2")

    def test_empty_child_id_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="child_id"):
            provider.link_subissue("1", "")

    def test_dry_run(self):
        provider = InMemoryIssueProvider()
        self._create_two_issues(provider)
        result = provider.link_subissue("1", "2", dry_run=True)
        assert result.status == "dry-run"
        assert provider.parent_child_links == set()

    def test_dry_run_missing_parent_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Child", "", "task")
        with pytest.raises(ValueError, match="Parent issue"):
            provider.link_subissue("99", "1", dry_run=True)

    def test_dry_run_missing_child_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Parent", "", "epic")
        with pytest.raises(ValueError, match="Child issue"):
            provider.link_subissue("1", "99", dry_run=True)


class TestInMemoryIssueProviderAddBlockedBy:
    """Tests for InMemoryIssueProvider.add_blocked_by."""

    def _create_two_issues(self, provider):
        provider.create_issue("Issue", "", "task")
        provider.create_issue("Blocker", "", "task")

    def test_nominal_block(self):
        provider = InMemoryIssueProvider()
        self._create_two_issues(provider)
        result = provider.add_blocked_by("1", "2")
        assert result.status == "linked"
        assert result.source_id == "2"
        assert result.target_id == "1"

    def test_self_blocking_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Issue", "", "task")
        with pytest.raises(ValueError, match="cannot block itself"):
            provider.add_blocked_by("1", "1")

    def test_duplicate_block(self):
        provider = InMemoryIssueProvider()
        self._create_two_issues(provider)
        provider.add_blocked_by("1", "2")
        result = provider.add_blocked_by("1", "2")
        assert result.status == "already-linked"

    def test_missing_issue_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Blocker", "", "task")
        with pytest.raises(ValueError, match="Issue.*not found"):
            provider.add_blocked_by("99", "1")

    def test_missing_blocker_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Issue", "", "task")
        with pytest.raises(ValueError, match="Blocker issue.*not found"):
            provider.add_blocked_by("1", "99")

    def test_empty_issue_id_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="issue_id"):
            provider.add_blocked_by("", "2")

    def test_empty_blocked_by_id_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="blocked_by_id"):
            provider.add_blocked_by("1", "")

    def test_dry_run(self):
        provider = InMemoryIssueProvider()
        self._create_two_issues(provider)
        result = provider.add_blocked_by("1", "2", dry_run=True)
        assert result.status == "dry-run"
        assert provider.blocked_by_links == set()

    def test_dry_run_missing_issue_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Blocker", "", "task")
        with pytest.raises(ValueError, match="Issue.*not found"):
            provider.add_blocked_by("99", "1", dry_run=True)

    def test_dry_run_missing_blocker_raises_value_error(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Issue", "", "task")
        with pytest.raises(ValueError, match="Blocker issue.*not found"):
            provider.add_blocked_by("1", "99", dry_run=True)


class TestInMemoryIssueProviderApplyLabels:
    """Tests for InMemoryIssueProvider.apply_labels."""

    def _create_issue(self, provider):
        provider.create_issue("Issue", "", "task")

    def test_nominal_new_labels(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.apply_labels("1", ["bug", "urgent"])
        assert result.status == "updated"
        assert result.metadata["labels"] == ["bug", "urgent"]

    def test_empty_labels_no_op(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.apply_labels("1", [])
        assert result.status == "no-op"

    def test_all_present_no_op(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Issue", "", "task", labels=["bug"])
        result = provider.apply_labels("1", ["bug"])
        assert result.status == "no-op"

    def test_missing_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="not found"):
            provider.apply_labels("99", ["bug"])

    def test_empty_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.apply_labels("", ["bug"])

    def test_dry_run(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.apply_labels("1", ["bug"], dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["labels"] == ["bug"]
        # Verify no mutation
        assert provider.issues["1"].get("labels", []) == []

    def test_dry_run_with_empty_labels(self):
        """FR-010: dry_run takes precedence — returns dry-run even for empty labels."""
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.apply_labels("1", [], dry_run=True)
        assert result.status == "dry-run"


class TestInMemoryIssueProviderSetIssueType:
    """Tests for InMemoryIssueProvider.set_issue_type."""

    def _create_issue(self, provider):
        provider.create_issue("Issue", "", "task")

    def test_nominal_valid_type(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.set_issue_type("1", "bug")
        assert result.status == "updated"
        assert result.metadata["issue_type"] == "bug"

    def test_invalid_type_raises_value_error(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        with pytest.raises(ValueError, match="Unsupported issue_type"):
            provider.set_issue_type("1", "story")

    def test_invalid_type_shows_sorted_valid_types(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        with pytest.raises(ValueError, match=r"\['bug', 'epic', 'feature', 'subtask', 'task'\]"):
            provider.set_issue_type("1", "invalid")

    def test_missing_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="not found"):
            provider.set_issue_type("99", "bug")

    def test_empty_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.set_issue_type("", "bug")

    def test_dry_run(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.set_issue_type("1", "bug", dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["issue_type"] == "bug"
        # Verify no mutation
        assert provider.issues["1"]["issue_type"] == "task"

    def test_same_type_returns_no_op(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.set_issue_type("1", "task")
        assert result.status == "no-op"
        assert result.metadata["issue_type"] == "task"


class TestInMemoryIssueProviderResolveIdentifier:
    """Tests for InMemoryIssueProvider.resolve_identifier."""

    def _create_issue(self, provider):
        provider.create_issue("Issue", "", "task")

    def test_nominal_existing_identifier(self):
        provider = InMemoryIssueProvider()
        self._create_issue(provider)
        result = provider.resolve_identifier("1")
        assert result.status == "resolved"
        assert result.metadata["internal_id"] == "1"
        assert "fake.test" in result.url

    def test_missing_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="not found"):
            provider.resolve_identifier("99")

    def test_empty_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.resolve_identifier("")

    def test_whitespace_identifier_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.resolve_identifier("   ")

    def test_dry_run(self):
        provider = InMemoryIssueProvider()
        result = provider.resolve_identifier("42", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == "42"
        assert result.url == ""
        assert result.metadata == {}

    def test_dry_run_with_empty_string_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.resolve_identifier("", dry_run=True)


class TestInMemoryIssueProviderNormalizeIdentifier:
    """Tests for InMemoryIssueProvider.normalize_identifier."""

    def test_github_strips_hash(self):
        provider = InMemoryIssueProvider(identifier_style="github")
        assert provider.normalize_identifier("#42") == "42"

    def test_github_already_canonical(self):
        provider = InMemoryIssueProvider(identifier_style="github")
        assert provider.normalize_identifier("42") == "42"

    def test_jira_passthrough(self):
        provider = InMemoryIssueProvider(identifier_style="jira")
        assert provider.normalize_identifier("PROJ-123") == "PROJ-123"

    def test_jira_with_hash_passthrough(self):
        provider = InMemoryIssueProvider(identifier_style="jira")
        assert provider.normalize_identifier("#42") == "#42"

    def test_empty_string_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.normalize_identifier("")

    def test_whitespace_only_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.normalize_identifier("   ")

    def test_github_hash_only_raises_value_error(self):
        provider = InMemoryIssueProvider(identifier_style="github")
        with pytest.raises(ValueError, match="identifier"):
            provider.normalize_identifier("#")


class TestInMemoryIssueProviderFormatIdentifier:
    """Tests for InMemoryIssueProvider.format_identifier."""

    def test_github_prepends_hash(self):
        provider = InMemoryIssueProvider(identifier_style="github")
        assert provider.format_identifier("42") == "#42"

    def test_github_already_formatted(self):
        provider = InMemoryIssueProvider(identifier_style="github")
        assert provider.format_identifier("#42") == "#42"

    def test_jira_passthrough(self):
        provider = InMemoryIssueProvider(identifier_style="jira")
        assert provider.format_identifier("PROJ-123") == "PROJ-123"

    def test_empty_string_raises_value_error(self):
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="identifier"):
            provider.format_identifier("")


class TestInMemoryIssueProviderStateInspection:
    """Tests for InMemoryIssueProvider public inspection properties."""

    def test_issues_property_returns_copy(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Test", "", "task")
        issues = provider.issues
        issues["999"] = {"fake": True}
        assert "999" not in provider.issues

    def test_issues_property_inner_dicts_are_deep_copied(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Test", "", "task", labels=["p0"])
        issues = provider.issues
        issues["1"]["labels"].append("mutated")
        assert "mutated" not in provider.issues["1"]["labels"]

    def test_parent_child_links_property(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Parent", "", "epic")
        provider.create_issue("Child", "", "task")
        provider.link_subissue("1", "2")
        assert ("1", "2") in provider.parent_child_links

    def test_blocked_by_links_property(self):
        provider = InMemoryIssueProvider()
        provider.create_issue("Issue", "", "task")
        provider.create_issue("Blocker", "", "task")
        provider.add_blocked_by("1", "2")
        assert ("1", "2") in provider.blocked_by_links

    def test_end_to_end_scenario(self):
        """Full 5-issue scenario with all relationship types."""
        provider = InMemoryIssueProvider()

        # Create issues
        epic = provider.create_issue("Epic", "desc", "epic")
        feat1 = provider.create_issue("Feature 1", "desc", "feature")
        feat2 = provider.create_issue("Feature 2", "desc", "feature")
        task1 = provider.create_issue("Task 1", "desc", "task")
        bug1 = provider.create_issue("Bug 1", "desc", "bug")

        # Link hierarchy
        provider.link_subissue(epic.identifier, feat1.identifier)
        provider.link_subissue(epic.identifier, feat2.identifier)
        provider.link_subissue(feat1.identifier, task1.identifier)

        # Add blocking
        provider.add_blocked_by(feat2.identifier, feat1.identifier)

        # Apply labels
        provider.apply_labels(bug1.identifier, ["critical", "p0"])

        # Set type
        provider.set_issue_type(bug1.identifier, "subtask")

        # Verify state
        assert len(provider.issues) == 5
        assert len(provider.parent_child_links) == 3
        assert len(provider.blocked_by_links) == 1
        assert provider.issues[bug1.identifier]["issue_type"] == "subtask"
        assert "critical" in provider.issues[bug1.identifier]["labels"]


class TestInMemoryIssueProviderFindExistingIssue:
    """Tests for InMemoryIssueProvider.find_existing_issue (IdempotencyQueryProvider)."""

    def test_find_by_embedded_key_returns_result(self):
        """Return ProviderIssueResult when key is found in issue body."""
        from agentic_devtools.adapters.orchestration_key import (
            embed_orchestration_key,
            generate_orchestration_key,
        )

        provider = InMemoryIssueProvider()
        key = generate_orchestration_key("create_issue", "task-1")
        body = embed_orchestration_key("Task body", key)
        created = provider.create_issue("Task", body, "task", idempotency_key=key)

        result = provider.find_existing_issue(key)
        assert result is not None
        assert result.identifier == created.identifier
        assert result.status == "existing"

    def test_find_by_idempotency_keys_mapping(self):
        """Return result when key is in _idempotency_keys but not in body."""
        provider = InMemoryIssueProvider()
        # Create without embedding key in body
        created = provider.create_issue("Task", "plain body", "task", idempotency_key="mykey123")

        result = provider.find_existing_issue("mykey123")
        assert result is not None
        assert result.identifier == created.identifier

    def test_find_returns_none_when_not_found(self):
        """Return None when no issue matches the key."""
        provider = InMemoryIssueProvider()
        provider.create_issue("Unrelated", "no key", "task")

        result = provider.find_existing_issue("nonexistent-key")
        assert result is None

    def test_find_raises_on_ambiguous_match(self):
        """Raise ValueError when multiple issues have the same embedded key (FR-008)."""
        from agentic_devtools.adapters.orchestration_key import (
            embed_orchestration_key,
            generate_orchestration_key,
        )

        provider = InMemoryIssueProvider()
        key = generate_orchestration_key("create_issue", "dup")
        body = embed_orchestration_key("Body", key)
        # Create two issues with same key in body (bypassing idempotency check
        # by using different idempotency_key values)
        provider.create_issue("Task A", body, "task", idempotency_key="k1")
        provider.create_issue("Task B", body, "task", idempotency_key="k2")

        with pytest.raises(ValueError, match="Ambiguous"):
            provider.find_existing_issue(key)

    def test_find_with_none_body_does_not_raise(self):
        """Non-string body (None) is treated as empty — does not raise TypeError."""
        provider = InMemoryIssueProvider()
        # Force a None body by directly manipulating internal state
        provider._issues["FAKE-1"] = {"title": "Task", "body": None, "issue_type": "task"}

        # Should not raise; the None body is treated as empty (no match)
        result = provider.find_existing_issue("some-key")
        assert result is None


class TestInMemoryIssueProviderFindExistingLink:
    """Tests for InMemoryIssueProvider.find_existing_link (IdempotencyQueryProvider)."""

    def test_find_existing_link_returns_result(self):
        """Return ProviderLinkResult when link exists."""
        provider = InMemoryIssueProvider()
        p = provider.create_issue("Parent", "p body", "feature")
        c = provider.create_issue("Child", "c body", "subtask")
        provider.link_subissue(p.identifier, c.identifier)

        result = provider.find_existing_link(p.identifier, c.identifier)
        assert result is not None
        assert result.status == "already-linked"
        assert result.source_id == p.identifier
        assert result.target_id == c.identifier

    def test_find_existing_link_returns_none(self):
        """Return None when link does not exist."""
        provider = InMemoryIssueProvider()
        p = provider.create_issue("Parent", "p body", "feature")
        c = provider.create_issue("Child", "c body", "subtask")

        result = provider.find_existing_link(p.identifier, c.identifier)
        assert result is None


class TestInMemoryIssueProviderFindExistingDependency:
    """Tests for InMemoryIssueProvider.find_existing_dependency (IdempotencyQueryProvider)."""

    def test_find_existing_dependency_returns_result(self):
        """Return ProviderLinkResult when dependency exists."""
        provider = InMemoryIssueProvider()
        a = provider.create_issue("Issue A", "a body", "task")
        b = provider.create_issue("Issue B", "b body", "task")
        provider.add_blocked_by(a.identifier, b.identifier)

        result = provider.find_existing_dependency(a.identifier, b.identifier)
        assert result is not None
        assert result.status == "already-linked"
        assert result.source_id == b.identifier
        assert result.target_id == a.identifier

    def test_find_existing_dependency_returns_none(self):
        """Return None when dependency does not exist."""
        provider = InMemoryIssueProvider()
        a = provider.create_issue("Issue A", "a body", "task")
        b = provider.create_issue("Issue B", "b body", "task")

        result = provider.find_existing_dependency(a.identifier, b.identifier)
        assert result is None


# ======================================================================
# Shared provider-contract scenarios (T021) — run for both identifier styles
# ======================================================================

from tests.unit.adapters.issue_provider import _contract_scenarios as contract  # noqa: E402


class _InMemoryContractHooks:
    """Hook implementations shared by both InMemory identifier-style legs."""

    def boundary_calls(self, provider):
        # InMemory has no provider boundary (no HTTP / subprocess).
        return 0

    def seed_issue(self, provider):
        return provider.create_issue("Seed", "Seed body", "task").identifier

    def seed_two_issues(self, provider):
        first = provider.create_issue("First", "first body", "task").identifier
        second = provider.create_issue("Second", "second body", "task").identifier
        return first, second


class TestInMemoryContractGithubStyle(
    _InMemoryContractHooks,
    contract.TestContractCreateIssue,
    contract.TestContractCreateIssueDryRun,
    contract.TestContractCreateIssueIdempotent,
    contract.TestContractSetIssueType,
    contract.TestContractSetIssueTypeTransition,
    contract.TestContractSetIssueTypeDryRun,
    contract.TestContractLinkSubissue,
    contract.TestContractLinkSubissueDryRun,
    contract.TestContractAddBlockedBy,
    contract.TestContractAddBlockedByDryRun,
    contract.TestContractApplyLabels,
    contract.TestContractApplyLabelsDryRun,
    contract.TestContractApplyLabelsIdempotent,
    contract.TestContractIdempotentRelink,
    contract.TestContractIdempotentBlockedBy,
    contract.TestContractResolveIdentifier,
    contract.TestContractResolveIdentifierDryRun,
    contract.TestContractNormalizeIdentifier,
    contract.TestContractFormatIdentifier,
):
    """Runs the shared contract suite against InMemoryIssueProvider (github style)."""

    sample_identifier = "1"

    @pytest.fixture()
    def provider(self):
        return InMemoryIssueProvider(identifier_style="github")


class TestInMemoryContractJiraStyle(
    _InMemoryContractHooks,
    contract.TestContractCreateIssue,
    contract.TestContractCreateIssueDryRun,
    contract.TestContractCreateIssueIdempotent,
    contract.TestContractSetIssueType,
    contract.TestContractSetIssueTypeTransition,
    contract.TestContractSetIssueTypeDryRun,
    contract.TestContractLinkSubissue,
    contract.TestContractLinkSubissueDryRun,
    contract.TestContractAddBlockedBy,
    contract.TestContractAddBlockedByDryRun,
    contract.TestContractApplyLabels,
    contract.TestContractApplyLabelsDryRun,
    contract.TestContractApplyLabelsIdempotent,
    contract.TestContractIdempotentRelink,
    contract.TestContractIdempotentBlockedBy,
    contract.TestContractResolveIdentifier,
    contract.TestContractResolveIdentifierDryRun,
    contract.TestContractNormalizeIdentifier,
    contract.TestContractFormatIdentifier,
):
    """Runs the shared contract suite against InMemoryIssueProvider (jira style)."""

    sample_identifier = "PROJ-1"

    @pytest.fixture()
    def provider(self):
        return InMemoryIssueProvider(identifier_style="jira")


class TestInMemoryIssueProviderLinkAndBlockState:
    """T022 — verify parent_child_links and blocked_by_links state after a full
    create -> link -> block sequence.
    """

    def test_create_link_block_sequence_populates_link_state(self):
        provider = InMemoryIssueProvider()

        parent = provider.create_issue("Parent", "p body", "epic")
        child = provider.create_issue("Child", "c body", "task")
        blocker = provider.create_issue("Blocker", "b body", "task")

        provider.link_subissue(parent.identifier, child.identifier)
        provider.add_blocked_by(child.identifier, blocker.identifier)

        assert provider.parent_child_links == {(parent.identifier, child.identifier)}
        assert provider.blocked_by_links == {(child.identifier, blocker.identifier)}


class TestInMemoryHierarchyValidation:
    """Hierarchy-routing validation for the in-memory fake (FR-016)."""

    def test_validate_issue_type_accepts_supported_types(self):
        provider = InMemoryIssueProvider("github")
        for issue_type in ("epic", "feature", "task", "bug", "subtask"):
            assert provider.validate_issue_type(issue_type) is None

    def test_validate_issue_type_is_case_insensitive(self):
        assert InMemoryIssueProvider("github").validate_issue_type("Epic") is None

    def test_validate_issue_type_rejects_unsupported_type(self):
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        with pytest.raises(AdapterValidationError):
            InMemoryIssueProvider("github").validate_issue_type("saga")

    def test_validate_hierarchy_pair_accepts_valid_pairs(self):
        provider = InMemoryIssueProvider("jira")
        assert provider.validate_hierarchy_pair("feature", "epic") is None
        assert provider.validate_hierarchy_pair("subtask", "feature") is None

    def test_validate_hierarchy_pair_rejects_same_level(self):
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        with pytest.raises(AdapterValidationError):
            InMemoryIssueProvider("github").validate_hierarchy_pair("task", "feature")

    def test_validate_hierarchy_pair_rejects_inverted_pair(self):
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        with pytest.raises(AdapterValidationError):
            InMemoryIssueProvider("github").validate_hierarchy_pair("epic", "feature")

    def test_validate_hierarchy_pair_rejects_unsupported_type(self):
        from agentic_devtools.adapters.exceptions import AdapterValidationError

        with pytest.raises(AdapterValidationError):
            InMemoryIssueProvider("github").validate_hierarchy_pair("saga", "epic")

    def test_provider_is_hierarchy_validation_capable(self):
        from agentic_devtools.adapters.issue_provider import HierarchyValidationProvider

        assert isinstance(InMemoryIssueProvider("github"), HierarchyValidationProvider)
