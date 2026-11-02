"""Tests for pull request diff preservation validation."""

import pytest

from agentic_devtools.cli.ci.pipeline.diff_validation import validate_diff_preservation

_PR_4130_MERGE_COMMIT_HEAD_SHA = "ae19a096be4ac0697a4011d422dd6f354ede1f96"
_PR_4130_MERGE_COMMIT_FILES = [
    ".github/workflows/README.md",
    ".github/workflows/ai-pr-loop-redispatch.yml",
    ".github/workflows/ai-pr-loop.yml",
    "tests/unit/cli/ci/watchdog_command/test_ai_pr_loop_watchdog_command.py",
    "tests/workflows/test_ai_pr_loop_main_workflow.py",
    "tests/workflows/test_ai_pr_loop_redispatch.py",
]


def test_accepts_non_empty_unchanged_diff() -> None:
    """A mutation that preserves files and its fingerprint is valid."""
    result = validate_diff_preservation(
        ["a.py"],
        ["a.py"],
        pre_hash="same",
        post_hash="same",
        fingerprint_supported=True,
    )
    assert result.valid is True


def test_accepts_explicit_noop_diff() -> None:
    """An explicitly empty pre-mutation diff remains a legitimate no-op."""
    result = validate_diff_preservation([], [], intentional_noop=True)
    assert result.valid is True


def test_rejects_implicit_noop_diff() -> None:
    """An empty baseline must declare explicit no-op intent."""
    result = validate_diff_preservation([], [])
    assert result.valid is False
    assert "explicit no-op" in result.reason


def test_rejects_partially_missing_diff() -> None:
    """A mutation missing an intended file is rejected and reports that file."""
    result = validate_diff_preservation(["a.py", "b.py"], ["a.py"])
    assert result.valid is False
    assert result.missing_files == ("b.py",)


def test_allows_intentional_file_removal_for_content_changing_mutation() -> None:
    """A content-changing mutation may remove files while retaining a non-empty diff."""
    result = validate_diff_preservation(["a.py", "b.py"], ["a.py"], allow_file_removal=True)
    assert result.valid is True
    assert result.missing_files == ()


def test_allows_only_scoped_file_removal() -> None:
    """A suggestion-touched file may disappear while unrelated missing files remain blocked."""
    allowed = validate_diff_preservation(["a.py", "b.py"], ["a.py"], allowed_removed_files=("b.py",))
    rejected = validate_diff_preservation(["a.py", "b.py"], [], allowed_removed_files=("b.py",))
    assert allowed.valid is True
    assert rejected.valid is False


def test_rejects_unscoped_file_removal() -> None:
    """A missing file outside the suggestion-touched paths is rejected."""
    result = validate_diff_preservation(["a.py", "b.py"], ["a.py"], allowed_removed_files=("c.py",))
    assert result.valid is False
    assert result.missing_files == ("b.py",)


def test_rejects_empty_diff() -> None:
    """A syntactically valid merge commit with no PR files is rejected."""
    result = validate_diff_preservation(["a.py"], [])
    assert result.valid is False
    assert result.reason == "post-mutation diff is empty"


def test_rejects_empty_diff_for_pr_4130_merge_commit_fixture() -> None:
    """The PR #4130 merge-commit file set is blocked if a later sync drops the diff."""
    assert _PR_4130_MERGE_COMMIT_HEAD_SHA
    result = validate_diff_preservation(_PR_4130_MERGE_COMMIT_FILES, [])
    assert result.valid is False
    assert result.reason == "post-mutation diff is empty"
    assert result.missing_files == tuple(sorted(_PR_4130_MERGE_COMMIT_FILES))


def test_rejects_changed_fingerprint() -> None:
    """A non-empty mutation with a different patch fingerprint is rejected."""
    result = validate_diff_preservation(
        ["a.py"],
        ["a.py"],
        pre_hash="old",
        post_hash="new",
        fingerprint_supported=True,
    )
    assert result.valid is False
    assert "fingerprint" in result.reason


def test_rejects_unavailable_fingerprint_when_supported() -> None:
    """Fingerprint-capable providers fail closed when a mutation hash is unavailable."""
    result = validate_diff_preservation(
        ["a.py"],
        ["a.py"],
        pre_hash="old",
        post_hash="",
        pre_hash_available=True,
        post_hash_available=False,
        fingerprint_supported=True,
    )
    assert result.valid is False
    assert "unavailable" in result.reason


def test_accepts_unavailable_fingerprint_for_identical_snapshot_identity() -> None:
    """Matching non-empty snapshot identity and files prove an unavailable hash is unchanged."""
    result = validate_diff_preservation(
        ["a.py", "b.py"],
        ["b.py", "a.py"],
        pre_hash="",
        post_hash="",
        pre_hash_available=False,
        post_hash_available=False,
        fingerprint_supported=True,
        pre_head_sha="same-head",
        post_head_sha="same-head",
        pre_base_branch="main",
        post_base_branch="main",
        pre_base_sha="base-sha-1",
        post_base_sha="base-sha-1",
    )

    assert result.valid is True


@pytest.mark.parametrize(
    (
        "pre_head_sha",
        "post_head_sha",
        "pre_base_branch",
        "post_base_branch",
        "pre_base_sha",
        "post_base_sha",
        "post_files",
    ),
    [
        ("old-head", "new-head", "main", "main", "base-sha-1", "base-sha-1", ["a.py"]),
        ("same-head", "same-head", "main", "release", "base-sha-1", "base-sha-1", ["a.py"]),
        ("same-head", "same-head", "main", "main", "base-sha-1", "base-sha-1", ["a.py", "b.py"]),
        ("", "same-head", "main", "main", "base-sha-1", "base-sha-1", ["a.py"]),
        ("same-head", "same-head", "", "main", "base-sha-1", "base-sha-1", ["a.py"]),
        ("same-head", "same-head", "main", "main", "", "base-sha-1", ["a.py"]),
        ("same-head", "same-head", "main", "main", "base-sha-1", "base-sha-2", ["a.py"]),
    ],
)
def test_rejects_unavailable_fingerprint_when_snapshot_identity_differs(
    pre_head_sha: str,
    post_head_sha: str,
    pre_base_branch: str,
    post_base_branch: str,
    pre_base_sha: str,
    post_base_sha: str,
    post_files: list[str],
) -> None:
    """An unavailable hash stays fail-closed unless every snapshot identity component matches."""
    result = validate_diff_preservation(
        ["a.py"],
        post_files,
        pre_hash_available=False,
        post_hash_available=False,
        fingerprint_supported=True,
        pre_head_sha=pre_head_sha,
        post_head_sha=post_head_sha,
        pre_base_branch=pre_base_branch,
        post_base_branch=post_base_branch,
        pre_base_sha=pre_base_sha,
        post_base_sha=post_base_sha,
    )

    assert result.valid is False
    assert "unavailable" in result.reason


def test_rejects_unequal_available_fingerprints_with_identical_snapshot_identity() -> None:
    """Matching snapshot identity cannot override two available but unequal fingerprints."""
    result = validate_diff_preservation(
        ["a.py"],
        ["a.py"],
        pre_hash="old",
        post_hash="new",
        fingerprint_supported=True,
        pre_head_sha="same-head",
        post_head_sha="same-head",
        pre_base_branch="main",
        post_base_branch="main",
        pre_base_sha="base-sha-1",
        post_base_sha="base-sha-1",
    )

    assert result.valid is False
    assert result.reason == "post-mutation patch fingerprint changed"


def test_rejects_empty_fingerprint_when_marked_available() -> None:
    """Empty fingerprint strings still count as unavailable for fail-closed validation."""
    result = validate_diff_preservation(
        ["a.py"],
        ["a.py"],
        pre_hash="baseline",
        post_hash="",
        pre_hash_available=True,
        post_hash_available=True,
        fingerprint_supported=True,
    )
    assert result.valid is False
    assert "unavailable" in result.reason
