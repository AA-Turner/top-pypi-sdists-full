# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the bump_version module — specifically the no_changelog flag."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from airbyte_ops_mcp.airbyte_repo.bump_version import bump_connector_version

# ---------------------------------------------------------------------------
# bump_connector_version — no_changelog
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_bump_connector_version_no_changelog() -> None:
    """Test that no_changelog prevents changelog updates."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        metadata_content = 'data:\n  dockerImageTag: "1.0.0"\n  name: source-test\n'
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        # Create a doc with changelog table so we can verify it's NOT updated.
        docs_dir = Path(tmpdir) / "docs" / "integrations" / "sources"
        docs_dir.mkdir(parents=True)
        doc_content = (
            "# Source Test\n\n"
            "| Version | Date | Pull Request | Subject |\n"
            "|---------|------|--------------|--------|\n"
            "| 1.0.0 | 2025-01-01 | "
            "[1](https://github.com/airbytehq/airbyte/pull/1) | Init |\n"
        )
        (docs_dir / "source-test.md").write_text(doc_content)

        bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            new_version="1.0.0-preview.abc1234",
            changelog_message="Should be skipped",
            no_changelog=True,
        )

        # Version should be bumped in metadata.
        metadata = (connector_dir / "metadata.yaml").read_text()
        assert "1.0.0-preview.abc1234" in metadata

        # Changelog should NOT have the new entry.
        doc = (docs_dir / "source-test.md").read_text()
        assert "Should be skipped" not in doc
        assert "1.0.0-preview.abc1234" not in doc
