"""Tests for _collect_diff_state."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.snapshot_builder import _collect_diff_state


def test_collects_diff_metadata_from_the_same_snapshot_inputs(monkeypatch) -> None:
    """The collector passes resolved base data into file and fingerprint lookups."""
    provider = MagicMock()
    metadata = PRMetadata(
        number=3,
        title="Snapshot",
        head_branch="feature",
        head_sha="head",
        base_branch="main",
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder._resolve_base_sha",
        lambda _provider, _number, _branch: ("base", {"base_sha": "base"}),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder._get_file_inventory",
        lambda _provider, _number, _branch, _head, base_kwargs: ["a.py"] if base_kwargs else [],
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder._get_diff_fingerprint",
        lambda _provider, _number, _branch, _head, base_kwargs: ("hash", bool(base_kwargs), True),
    )

    result = _collect_diff_state(provider, 3, metadata)

    assert result == (["a.py"], "base", "hash", True, True)
