"""Tests for should_inject function."""

from __future__ import annotations

from agentic_devtools.skill_classification import Classification, should_inject

# ---------------------------------------------------------------------------
# FR-006: always=True overrides everything
# ---------------------------------------------------------------------------


class TestShouldInjectAlways:
    """FR-006: always=True → always inject regardless of requires."""

    def test_always_true_ignores_mismatched_requires(self) -> None:
        cls = Classification(
            requires_issue_adapter="jira",
            requires_code_hosting="azure_devops",
            always=True,
        )
        assert should_inject(cls, issue_adapter="github", code_hosting="github") is True

    def test_always_true_with_none_platforms(self) -> None:
        cls = Classification(always=True)
        assert should_inject(cls, issue_adapter=None, code_hosting=None) is True

    def test_always_true_universal(self) -> None:
        cls = Classification(always=True)
        assert should_inject(cls, issue_adapter="github", code_hosting="github") is True


# ---------------------------------------------------------------------------
# FR-007: Legacy None,None inject-all
# ---------------------------------------------------------------------------


class TestShouldInjectLegacyNoneNone:
    """FR-007: Both platform args None → True (legacy inject-all)."""

    def test_universal_classification(self) -> None:
        cls = Classification()
        assert should_inject(cls, issue_adapter=None, code_hosting=None) is True

    def test_classification_with_requires_but_none_platforms(self) -> None:
        cls = Classification(requires_issue_adapter="jira")
        assert should_inject(cls, issue_adapter=None, code_hosting=None) is True


# ---------------------------------------------------------------------------
# FR-008: None platform arg = unrestricted
# ---------------------------------------------------------------------------


class TestShouldInjectNonePlatformUnrestricted:
    """FR-008: None platform arg means unrestricted for that axis."""

    def test_none_issue_adapter_unrestricted(self) -> None:
        cls = Classification(requires_issue_adapter="jira")
        assert should_inject(cls, issue_adapter=None, code_hosting="github") is True

    def test_none_code_hosting_unrestricted(self) -> None:
        cls = Classification(requires_code_hosting="azure_devops")
        assert should_inject(cls, issue_adapter="jira", code_hosting=None) is True

    def test_requires_set_platform_none(self) -> None:
        cls = Classification(requires_issue_adapter="github", requires_code_hosting="azure_devops")
        # Both platform args None → legacy inject-all (FR-007)
        assert should_inject(cls, issue_adapter=None, code_hosting=None) is True


# ---------------------------------------------------------------------------
# FR-009: AND-combination of axes
# ---------------------------------------------------------------------------


class TestShouldInjectAndCombination:
    """FR-009: AND-combine non-None axes."""

    def test_both_axes_match(self) -> None:
        cls = Classification(requires_issue_adapter="jira", requires_code_hosting="azure_devops")
        assert should_inject(cls, issue_adapter="jira", code_hosting="azure_devops") is True

    def test_issue_adapter_mismatch(self) -> None:
        cls = Classification(requires_issue_adapter="jira", requires_code_hosting="azure_devops")
        assert should_inject(cls, issue_adapter="github", code_hosting="azure_devops") is False

    def test_code_hosting_mismatch(self) -> None:
        cls = Classification(requires_issue_adapter="jira", requires_code_hosting="azure_devops")
        assert should_inject(cls, issue_adapter="jira", code_hosting="github") is False

    def test_both_axes_mismatch(self) -> None:
        cls = Classification(requires_issue_adapter="jira", requires_code_hosting="azure_devops")
        assert should_inject(cls, issue_adapter="github", code_hosting="github") is False


# ---------------------------------------------------------------------------
# Single axis match/mismatch
# ---------------------------------------------------------------------------


class TestShouldInjectSingleAxis:
    """Single-axis scenarios."""

    def test_single_axis_match(self) -> None:
        cls = Classification(requires_issue_adapter="jira")
        assert should_inject(cls, issue_adapter="jira", code_hosting=None) is True

    def test_single_axis_mismatch(self) -> None:
        cls = Classification(requires_issue_adapter="jira")
        assert should_inject(cls, issue_adapter="github", code_hosting=None) is False

    def test_code_hosting_match(self) -> None:
        cls = Classification(requires_code_hosting="github")
        assert should_inject(cls, issue_adapter=None, code_hosting="github") is True

    def test_code_hosting_mismatch(self) -> None:
        cls = Classification(requires_code_hosting="github")
        assert should_inject(cls, issue_adapter=None, code_hosting="azure_devops") is False

    def test_no_requires_with_concrete_platform(self) -> None:
        """Universal classification always injects regardless of platform."""
        cls = Classification()
        assert should_inject(cls, issue_adapter="github", code_hosting="azure_devops") is True


# ---------------------------------------------------------------------------
# Setup agent always-inject (FR-009 / SC-002)
# ---------------------------------------------------------------------------


class TestShouldInjectSetupAgents:
    """Setup agents (always=True, no requires) inject unconditionally."""

    def _setup_agent_classification(self) -> Classification:
        """Return the classification for setup agents (always=True, no requires)."""
        return Classification(
            requires_issue_adapter=None,
            requires_code_hosting=None,
            always=True,
        )

    def test_github_github(self) -> None:
        """Injects with github/github platform combination."""
        cls = self._setup_agent_classification()
        assert should_inject(cls, issue_adapter="github", code_hosting="github") is True

    def test_jira_azure_devops(self) -> None:
        """Injects with jira/azure_devops platform combination."""
        cls = self._setup_agent_classification()
        assert should_inject(cls, issue_adapter="jira", code_hosting="azure_devops") is True

    def test_none_none(self) -> None:
        """Injects with None/None (unresolved) platform combination."""
        cls = self._setup_agent_classification()
        assert should_inject(cls, issue_adapter=None, code_hosting=None) is True
