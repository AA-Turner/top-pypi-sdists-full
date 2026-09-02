"""Tests for SupervisorEvidence construction and validation."""

import pytest

from agentic_devtools.cli.ci.supervisor import SupervisorEvidence


def test_supervisorevidence_rejects_invalid_pr_number() -> None:
    with pytest.raises(ValueError, match="pr_number"):
        SupervisorEvidence(pr_number=0, head_sha="a" * 40)


def test_supervisorevidence_rejects_empty_head_sha() -> None:
    with pytest.raises(ValueError, match="head_sha"):
        SupervisorEvidence(pr_number=7, head_sha="")


def test_supervisorevidence_rejects_none_head_sha() -> None:
    with pytest.raises(ValueError, match="head_sha"):
        SupervisorEvidence(pr_number=7, head_sha=None)  # type: ignore[arg-type]


def test_supervisorevidence_rejects_negative_unresolved_threads() -> None:
    with pytest.raises(ValueError, match="unresolved_threads"):
        SupervisorEvidence(pr_number=7, head_sha="a" * 40, unresolved_threads=-1)


def test_supervisorevidence_rejects_bool_unresolved_threads() -> None:
    with pytest.raises(ValueError, match="unresolved_threads"):
        SupervisorEvidence(pr_number=7, head_sha="a" * 40, unresolved_threads=True)
