"""Test providers with explicit stable PR diff evidence."""

from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import PRMetadata


def verified_pr_provider(
    pr_number: int,
    head_sha: str,
    files: list[str] | None,
    *,
    post_squash_head_sha: str | None = None,
) -> MagicMock:
    """Build a mocked provider with metadata and an inventory tied by file count."""
    provider = MagicMock()
    changed_files = len(files) if files is not None else 1
    metadata = PRMetadata(pr_number, "change", "feature", head_sha, "main", changed_files=changed_files)
    provider.get_pr_metadata.return_value = metadata
    provider.get_ref_sha.return_value = "base-sha"
    provider.list_pr_files_complete.return_value = files
    if post_squash_head_sha is not None:

        def advance_head(**_: object) -> SimpleNamespace:
            provider.get_pr_metadata.return_value = replace(metadata, head_sha=post_squash_head_sha)
            return SimpleNamespace(tree_preserved=True, after_sha=post_squash_head_sha)

        provider.squash_post_repair.side_effect = advance_head
    return provider
