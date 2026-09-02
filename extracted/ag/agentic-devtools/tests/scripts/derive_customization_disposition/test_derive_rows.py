"""Tests for derive_rows in derive_customization_disposition."""

from __future__ import annotations

from collections import Counter

import pytest

from tests.scripts.derive_customization_disposition import REPO_ROOT, derive

ROWS = derive.derive_rows(REPO_ROOT)


def test_one_row_per_unit() -> None:
    """Every `agdt.*` file appears exactly once, the two manifests excluded."""
    agents, prompts = derive.count_files(REPO_ROOT)
    assert len(ROWS) == agents + prompts
    assert len({r.path for r in ROWS}) == len(ROWS)


def test_row_count_matches_the_classification_fixture() -> None:
    """266 units is the same corpus `skill_classification_expected.json` describes."""
    import json

    fixture = REPO_ROOT / "tests" / "fixtures" / "skill_classification_expected.json"
    assert len(json.loads(fixture.read_text(encoding="utf-8"))) == len(ROWS)


def test_batches_partition_the_rows() -> None:
    """The complement rule leaves no row without a batch."""
    derive.assert_partition(ROWS, expected_total=len(ROWS))
    counts = Counter(r.batch for r in ROWS)
    assert sum(counts[b] for b in derive.BATCHES) == len(ROWS)


def test_no_target_slug_collisions() -> None:
    """Only the intended merges share a target slug."""
    assert derive.collisions(ROWS) == {}


def test_manifests_are_not_units() -> None:
    """`agdt.README.md` indexes its directory; it is not a customization unit."""
    assert not any(r.path.endswith(derive.MANIFEST_NAME) for r in ROWS)


def test_derived_figures_only_disagree_on_the_documented_figures() -> None:
    """Only the documented reconciliation deltas may disagree with prior analysis."""
    derived = derive.derived_figures(ROWS)
    mismatches = {
        key: (derive.PRIOR_ANALYSIS[key], derived[key])
        for key in derive.PRIOR_ANALYSIS
        if derived[key] != derive.PRIOR_ANALYSIS[key]
    }
    assert mismatches == {
        "Injected files": (259, 266),
        "Agent files": (132, 141),
        "Prompt files": (127, 125),
        "Prompt registration stubs (delete)": (113, 111),
        "Prompt skills (9 plain + 2 `context: fork`)": (11, 8),
        "Prompt subagents": (1, 0),
        "Agent deletions": (90, 89),
        "Agent merges": (15, 23),
        "Agent skills": (11, 12),
        "Agent collapses": (11, 12),
        "Surviving skill names": (24, 23),
        "Surviving subagent names": (6, 5),
        "Retirement batch `stubs`": (113, 111),
        "Retirement batch `wrappers`": (87, 86),
        "Retirement batch `residue`": (59, 69),
    }


def test_prompt_skill_reconciliation_explains_the_net_11_to_8_arithmetic() -> None:
    """The reconciliation text documents both the collapses and the prompt-side reclassification."""
    reconciliation = derive._prompt_skill_reconciliation(ROWS, derive.derived_figures(ROWS))

    assert "11 - 4 + 1 = 8" in reconciliation
    assert ".github/prompts/agdt.suppressed-comment-triage.evaluate.prompt.md" in reconciliation


def test_prompt_skill_reconciliation_omits_zero_reclassification_clause() -> None:
    """The reconciliation stays accurate when no prompt-side subagent becomes a skill."""
    rows_without_promoted_prompt = [
        row for row in ROWS if row.path != ".github/prompts/agdt.suppressed-comment-triage.evaluate.prompt.md"
    ]

    reconciliation = derive._prompt_skill_reconciliation(
        rows_without_promoted_prompt,
        derive.derived_figures(rows_without_promoted_prompt),
    )

    assert "+ 0" not in reconciliation
    assert "0 prompt units now count as skills rather than as subagents" not in reconciliation


@pytest.mark.parametrize(
    ("path", "disposition", "group", "target", "batch"),
    [
        (
            ".github/prompts/agdt.add-jira-comment.prompt.md",
            "delete",
            "-",
            "-",
            "stubs",
        ),
        (
            ".github/agents/agdt.add-jira-comment.agent.md",
            "delete",
            "-",
            "-",
            "wrappers",
        ),
        (
            ".github/agents/agdt.advance-workflow.agent.md",
            "delete",
            "-",
            "-",
            "residue",
        ),
        (
            ".github/agents/agdt.work-on-jira-issue.setup.agent.md",
            "merge",
            "work-on-jira-issue",
            "agdt-work-on-jira-issue",
            "residue",
        ),
        (
            ".github/agents/agdt.pull-request-review.orchestrator.agent.md",
            "subagent",
            "pull-request-review",
            "agdt-pull-request-review-orchestrator",
            "residue",
        ),
        (
            ".github/agents/agdt.squash-commits.agent.md",
            "collapse",
            "git-and-pr",
            "agdt-squash-commits",
            "residue",
        ),
        (
            ".github/prompts/agdt.squash-commits.prompt.md",
            "skill",
            "git-and-pr",
            "agdt-squash-commits",
            "residue",
        ),
    ],
)
def test_representative_rows(path: str, disposition: str, group: str, target: str, batch: str) -> None:
    """One row per rule, so a change of rule order shows up as a failing test."""
    row = next(r for r in ROWS if r.path == path)
    assert (row.disposition, row.group, row.target, row.batch) == (disposition, group, target, batch)


def test_every_delete_row_records_a_reason() -> None:
    """The residue issue retires rows it did not derive, so each states why."""
    assert all(r.reason for r in ROWS if r.disposition == "delete")


def test_singleton_groups_split_alphabetically() -> None:
    """`singleton-a` is the first six standalone procedure skills, alphabetically."""
    singletons = sorted(r.slug for r in ROWS if r.group in {"singleton-a", "singleton-b"})
    in_a = sorted(r.slug for r in ROWS if r.group == "singleton-a")
    assert in_a == singletons[: derive.SINGLETON_A_SIZE]
