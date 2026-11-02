"""Tests for has_verified_non_empty_pr_diff."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.delivery import has_verified_non_empty_pr_diff


def _provider(files: list[str] | None) -> Mock:
    provider = Mock()
    metadata = PRMetadata(
        number=1,
        title="change",
        head_branch="feature",
        head_sha="head",
        base_branch="main",
        changed_files=len(files) if files is not None else 1,
    )
    provider.get_pr_metadata.side_effect = [metadata, metadata]
    provider.get_ref_sha.return_value = "base"
    provider.list_pr_files_complete.return_value = files
    return provider


@pytest.mark.parametrize(("files", "expected"), [(["src/main.py"], True), ([], False), (None, False)])
def test_requires_a_verified_non_empty_inventory(files: list[str] | None, expected: bool) -> None:
    assert has_verified_non_empty_pr_diff(_provider(files), 1) is expected


def test_invalid_pr_identity_fails_closed() -> None:
    assert has_verified_non_empty_pr_diff(Mock(), 0) is False
