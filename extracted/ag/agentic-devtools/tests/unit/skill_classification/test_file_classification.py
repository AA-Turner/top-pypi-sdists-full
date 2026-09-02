"""Structural tests validating platform classification of all agdt.* skill files.

.. deprecated::
    The canonical source of truth for skill classification is now the fixture at
    ``tests/fixtures/skill_classification_expected.json``, validated by
    ``scripts/validate_skill_classification.py`` and the library function in
    ``agentic_devtools/cli/checks/skill_classification.py``.  The hardcoded
    bucket lists in this file are retained for backward compatibility but
    should not be used as the primary classification inventory.

These tests load each agent/prompt file from disk, parse its YAML frontmatter
through ``parse_classification``, and assert that the resulting ``Classification``
falls into the expected bucket.  Every ``agdt.*`` file is accounted for — no file
is left unclassified.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from agentic_devtools.skill_classification import (
    Classification,
    parse_classification,
    should_inject,
)

# ---------------------------------------------------------------------------
# Repository root
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[3]
_AGENTS_DIR = _REPO_ROOT / ".github" / "agents"
_PROMPTS_DIR = _REPO_ROOT / ".github" / "prompts"

# ---------------------------------------------------------------------------
# Hardcoded classification data sets (FR-006, FR-008)
# ---------------------------------------------------------------------------

JIRA_REQUIRED_FILES: list[str] = [
    "add-jira-comment",
    "add-users-to-project-role",
    "add-users-to-project-role-batch",
    "break-down-issue-into-subtasks.initiate",
    "check-user-exists",
    "check-users-exist",
    "create-epic",
    "create-issue",
    "create-jira-epic.initiate",
    "create-jira-issue.initiate",
    "create-jira-subtask.initiate",
    "create-subtask",
    "find-role-id-by-name",
    "get-jira-issue",
    "get-project-role-details",
    "list-project-roles",
    "optimize-issue-for-ai-agent.initiate",
    "parse-jira-error-report",
    "update-jira-issue",
    "update-jira-issue.initiate",
    "work-on-jira-issue.checklist-creation",
    "work-on-jira-issue.commit",
    "work-on-jira-issue.completion",
    "work-on-jira-issue.implementation",
    "work-on-jira-issue.implementation-review",
    "work-on-jira-issue.initiate",
    "work-on-jira-issue.planning",
    "work-on-jira-issue.pull-request",
    "work-on-jira-issue.retrieve",
    "work-on-jira-issue.setup",
    "work-on-jira-issue.verification",
]

AZURE_DEVOPS_REQUIRED_FILES: list[str] = [
    "apply-pr-suggestions.initiate",
    "approve-pull-request",
    "confirm-suggestion-addressed",
    "create-pipeline",
    "create-pull-request",
    "get-pipeline-id",
    "get-pull-request-details",
    "get-pull-request-threads",
    "get-run-details",
    "list-pipelines",
    "mark-pull-request-draft",
    "publish-pull-request",
    "pull-request-review.completion",
    "pull-request-review.decision",
    "pull-request-review.file-reviewer",
    "pull-request-review.initiate",
    "pull-request-review.orchestrator",
    "reject-suggestion-resolution",
    "run-e2e-tests-fabric",
    "run-e2e-tests-synapse",
    "run-wb-patch",
    "update-pipeline",
    "wait-for-run",
]

GITHUB_REQUIRED_FILES: list[str] = [
    "address-copilot-review",
    "address-copilot-review.ci-repair",
    "address-copilot-review.evaluate-and-respond",
    "ai-pr-loop-supervisor",
    "ai-pr-loop-supervisor.inventory",
    "ai-pr-loop-supervisor.issue-triage",
    "ai-pr-loop-supervisor.recovery-planner",
    "ai-pr-loop-supervisor.review-readiness",
    "ai-pr-loop-supervisor.run-forensics",
    "ai-pr-loop-supervisor.task-recovery",
    "ai-pr-loop-supervisor.thread-adjudicator",
    "ai-pr-loop-supervisor.verifier",
    "pr-merge-execute",
    "pr-merge-manager",
]

ALWAYS_INJECT_FILES: list[str] = [
    "create-agdt-bug-issue",
    "create-agdt-documentation-issue",
    "create-agdt-feature-issue",
    "create-agdt-issue",
    "create-agdt-task-issue",
    "report-setup-bug",
    "report-setup-feature",
    "run-setup",
]

UNIVERSAL_FILES: list[str] = [
    "add-pull-request-comment",
    "address-own-review-feedback",
    "address-pr-review-comments",
    "advance-workflow",
    "analyze-workflow",
    "autonomous-issue-refinement",
    "azure-context-current",
    "azure-context-ensure-login",
    "azure-context-status",
    "azure-context-use",
    "clear",
    "clear-workflow",
    "copilot-auto-start",
    "create-checklist",
    "create-issues-from-analysis",
    "delete",
    "fix-workflow",
    "get",
    "get-next-workflow-prompt",
    "get-workflow",
    "git-force-push",
    "git-publish",
    "git-push",
    "git-save-work",
    "git-stage",
    "git-sync",
    "network-status",
    "phase0-reviewing-agent",
    "pull-request-review.rubber-duck",
    "pull-request-review.triage",
    "query-app-insights",
    "query-fabric-dap-errors",
    "query-fabric-dap-provisioning",
    "query-fabric-dap-timeline",
    "release-pypi",
    "resolve-merge-conflicts",
    "resolve-merge-conflicts.cloud-agent",
    "resolve-thread",
    "review-feedback-audit.evaluate",
    "set",
    "setup",
    "setup-certs",
    "setup-check",
    "setup-copilot-cli",
    "setup-gh-cli",
    "setup-worktree-background",
    "show",
    "show-checklist",
    "show-other-incomplete-tasks",
    "squash-commits",
    "suppressed-comment-triage.evaluate",
    "task-log",
    "task-status",
    "task-wait",
    "tasks",
    "tasks-clean",
    "test",
    "test-file",
    "test-pattern",
    "test-quick",
    "test-workflow",
    "update-checklist",
    "vpn-off",
    "vpn-on",
    "vpn-run",
    "vpn-status",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_frontmatter(filepath: Path) -> dict:
    """Load YAML frontmatter from a markdown file.

    Uses a line-based scan so CRLF checkouts and files with a missing closing
    delimiter are handled gracefully rather than raising ``ValueError``.
    """
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    lines = content.splitlines()
    close_idx = next(
        (i for i, line in enumerate(lines) if i > 0 and line == "---"),
        None,
    )
    if close_idx is None:
        return {}
    fm_raw = "\n".join(lines[1:close_idx]).strip()
    result = yaml.safe_load(fm_raw)
    return result if result is not None else {}


def _get_all_files_for_skill(skill: str) -> list[Path]:
    """Return all existing agent/prompt files for a skill name."""
    files = []
    agent = _AGENTS_DIR / f"agdt.{skill}.agent.md"
    prompt = _PROMPTS_DIR / f"agdt.{skill}.prompt.md"
    if agent.exists():
        files.append(agent)
    if prompt.exists():
        files.append(prompt)
    return files


def _get_all_agdt_skills() -> set[str]:
    """Return the set of all agdt.* skill names on disk."""
    skills: set[str] = set()
    for f in _AGENTS_DIR.glob("agdt.*.agent.md"):
        skills.add(f.name[5:-9])
    for f in _PROMPTS_DIR.glob("agdt.*.prompt.md"):
        skills.add(f.name[5:-10])
    return skills


# ---------------------------------------------------------------------------
# T021: Jira-required files (FR-001, FR-006)
# ---------------------------------------------------------------------------


class TestJiraRequiredFiles:
    """Each Jira-required file has requires_issue_adapter='jira'."""

    @pytest.mark.parametrize("skill", JIRA_REQUIRED_FILES)
    def test_jira_classification(self, skill: str) -> None:
        for filepath in _get_all_files_for_skill(skill):
            fm = _load_frontmatter(filepath)
            cls = parse_classification(fm)
            assert cls.requires_issue_adapter == "jira", (
                f"{filepath}: expected requires_issue_adapter='jira', got {cls.requires_issue_adapter!r}"
            )
            assert cls.requires_code_hosting is None, (
                f"{filepath}: expected requires_code_hosting=None, got {cls.requires_code_hosting!r}"
            )
            assert cls.always is False, f"{filepath}: expected always=False"


# ---------------------------------------------------------------------------
# T022: Azure DevOps-required files (FR-001, FR-006)
# ---------------------------------------------------------------------------


class TestAzureDevOpsRequiredFiles:
    """Each Azure DevOps-required file has requires_code_hosting='azure_devops'."""

    @pytest.mark.parametrize("skill", AZURE_DEVOPS_REQUIRED_FILES)
    def test_azure_devops_classification(self, skill: str) -> None:
        for filepath in _get_all_files_for_skill(skill):
            fm = _load_frontmatter(filepath)
            cls = parse_classification(fm)
            assert cls.requires_code_hosting == "azure_devops", (
                f"{filepath}: expected requires_code_hosting='azure_devops', got {cls.requires_code_hosting!r}"
            )
            assert cls.requires_issue_adapter is None, (
                f"{filepath}: expected requires_issue_adapter=None, got {cls.requires_issue_adapter!r}"
            )
            assert cls.always is False, f"{filepath}: expected always=False"


# ---------------------------------------------------------------------------
# T023: GitHub-required files (FR-001, FR-006)
# ---------------------------------------------------------------------------


class TestGitHubRequiredFiles:
    """Each GitHub-required file has requires_code_hosting='github'."""

    @pytest.mark.parametrize("skill", GITHUB_REQUIRED_FILES)
    def test_github_classification(self, skill: str) -> None:
        for filepath in _get_all_files_for_skill(skill):
            fm = _load_frontmatter(filepath)
            cls = parse_classification(fm)
            assert cls.requires_code_hosting == "github", (
                f"{filepath}: expected requires_code_hosting='github', got {cls.requires_code_hosting!r}"
            )
            assert cls.requires_issue_adapter is None, (
                f"{filepath}: expected requires_issue_adapter=None, got {cls.requires_issue_adapter!r}"
            )
            assert cls.always is False, f"{filepath}: expected always=False"


# ---------------------------------------------------------------------------
# T024: Always-inject files (FR-002, FR-006)
# ---------------------------------------------------------------------------


class TestAlwaysInjectFiles:
    """Each always-inject file has always=True and should_inject returns True for all platforms."""

    @pytest.mark.parametrize("skill", ALWAYS_INJECT_FILES)
    def test_always_classification(self, skill: str) -> None:
        for filepath in _get_all_files_for_skill(skill):
            fm = _load_frontmatter(filepath)
            cls = parse_classification(fm)
            assert cls.always is True, f"{filepath}: expected always=True"

    @pytest.mark.parametrize("skill", ALWAYS_INJECT_FILES)
    def test_always_inject_for_all_platforms(self, skill: str) -> None:
        for filepath in _get_all_files_for_skill(skill):
            fm = _load_frontmatter(filepath)
            cls = parse_classification(fm)
            assert should_inject(cls, issue_adapter="github", code_hosting="github") is True
            assert should_inject(cls, issue_adapter="jira", code_hosting="azure_devops") is True
            assert should_inject(cls, issue_adapter=None, code_hosting=None) is True


# ---------------------------------------------------------------------------
# T025: Universal/untagged files (FR-003, FR-006)
# ---------------------------------------------------------------------------


class TestUniversalFiles:
    """Each universal file stays unrestricted, whether agdt is omitted or explicitly empty."""

    @pytest.mark.parametrize("skill", UNIVERSAL_FILES)
    def test_universal_classification(self, skill: str) -> None:
        for filepath in _get_all_files_for_skill(skill):
            fm = _load_frontmatter(filepath)
            assert fm.get("agdt", {}) == {}, (
                f"{filepath}: expected an omitted or empty agdt block, found {fm.get('agdt')!r}"
            )
            cls = parse_classification(fm)
            assert cls.requires_issue_adapter is None, f"{filepath}: expected requires_issue_adapter=None"
            assert cls.requires_code_hosting is None, f"{filepath}: expected requires_code_hosting=None"
            assert cls.always is False, f"{filepath}: expected always=False"


# ---------------------------------------------------------------------------
# T026: Completeness test (FR-006)
# ---------------------------------------------------------------------------


class TestCompletenessAllFilesAccountedFor:
    """Union of all bucket lists equals total set of agdt.* files on disk."""

    def test_all_files_accounted_for(self) -> None:
        all_listed = set(
            JIRA_REQUIRED_FILES
            + AZURE_DEVOPS_REQUIRED_FILES
            + GITHUB_REQUIRED_FILES
            + ALWAYS_INJECT_FILES
            + UNIVERSAL_FILES
        )
        all_on_disk = _get_all_agdt_skills()

        missing_from_lists = all_on_disk - all_listed
        extra_in_lists = all_listed - all_on_disk

        assert not missing_from_lists, f"Files on disk not accounted for in any bucket: {sorted(missing_from_lists)}"
        assert not extra_in_lists, f"Files in bucket lists but not on disk: {sorted(extra_in_lists)}"


# ---------------------------------------------------------------------------
# T027: Agent/prompt pair consistency (FR-005)
# ---------------------------------------------------------------------------


class TestAgentPromptPairConsistency:
    """For every skill with both .agent.md and .prompt.md, agdt blocks must match."""

    def test_pairs_have_matching_agdt_blocks(self) -> None:
        mismatches: list[str] = []
        for skill in sorted(_get_all_agdt_skills()):
            agent = _AGENTS_DIR / f"agdt.{skill}.agent.md"
            prompt = _PROMPTS_DIR / f"agdt.{skill}.prompt.md"
            if not agent.exists() or not prompt.exists():
                continue
            agent_agdt = _load_frontmatter(agent).get("agdt")
            prompt_agdt = _load_frontmatter(prompt).get("agdt")
            if agent_agdt != prompt_agdt:
                mismatches.append(f"{skill}: agent agdt={agent_agdt!r}, prompt agdt={prompt_agdt!r}")
        assert not mismatches, "Agent/prompt agdt block mismatches:\n" + "\n".join(mismatches)


# ---------------------------------------------------------------------------
# T028: Dual-axis classification (FR-006)
# ---------------------------------------------------------------------------


class TestDualAxisClassification:
    """Dual-axis files have both issue_adapter and code_hosting set."""

    def test_should_inject_performs_and_match(self) -> None:
        cls = Classification(
            requires_issue_adapter="jira",
            requires_code_hosting="azure_devops",
        )
        assert should_inject(cls, issue_adapter="jira", code_hosting="azure_devops") is True
        assert should_inject(cls, issue_adapter="jira", code_hosting="github") is False
        assert should_inject(cls, issue_adapter="github", code_hosting="azure_devops") is False
        assert should_inject(cls, issue_adapter="github", code_hosting="github") is False


# ---------------------------------------------------------------------------
# T029: Documentation exists with all 6 required examples (FR-007, SC-005)
# ---------------------------------------------------------------------------


class TestAuthoringConventionDoc:
    """Authoring convention doc exists and contains all required examples."""

    _DOC_PATH = _REPO_ROOT / "docs" / "skill-file-authoring-conventions.md"

    def test_doc_exists(self) -> None:
        assert self._DOC_PATH.exists(), f"Missing: {self._DOC_PATH}"

    def test_doc_contains_jira_example(self) -> None:
        content = self._DOC_PATH.read_text(encoding="utf-8")
        assert "### Jira-Only Skill" in content
        assert 'description: "Add Jira Comment: Add a comment to a Jira issue"' in content

    def test_doc_contains_azure_devops_example(self) -> None:
        content = self._DOC_PATH.read_text(encoding="utf-8")
        assert "### Azure DevOps-Only Skill" in content
        assert 'description: "Add PR Comment: Post a comment on a pull request"' in content

    def test_doc_contains_github_example(self) -> None:
        content = self._DOC_PATH.read_text(encoding="utf-8")
        assert "### GitHub-Only Skill" in content
        assert 'description: "Address Copilot Review:' in content

    def test_doc_contains_always_example(self) -> None:
        content = self._DOC_PATH.read_text(encoding="utf-8")
        assert "### Always-Inject Skill" in content
        assert 'description: "Create Bug Issue:' in content

    def test_doc_contains_universal_example(self) -> None:
        content = self._DOC_PATH.read_text(encoding="utf-8")
        assert "### Universal (Untagged) Skill" in content
        assert 'description: "Git Save Work:' in content

    def test_doc_contains_dual_axis_example(self) -> None:
        content = self._DOC_PATH.read_text(encoding="utf-8")
        assert "### Dual-Axis" in content
        assert 'description: "Example Dual-Axis Skill:' in content
