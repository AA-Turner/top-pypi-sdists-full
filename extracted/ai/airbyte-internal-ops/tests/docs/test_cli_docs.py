# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Smoke test for the `airbyte-ops` CLI reference generator.

This verifies that `docs.generate_cli.generate_cli_reference` can produce a
non-empty Markdown document that mentions the CLI's top-level command name.
It does not assert on the exact shape of the output — that is owned by
cyclopts and is expected to evolve.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from docs.generate_cli import generate_cli_reference


@pytest.mark.unit
def test_generate_cli_reference_writes_markdown(tmp_path: Path) -> None:
    """`generate_cli_reference` writes a non-empty Markdown file mentioning `airbyte-ops`."""
    output_path = tmp_path / "cli-reference.md"

    returned_path = generate_cli_reference(output_path)

    assert returned_path == output_path
    assert output_path.exists()

    content = output_path.read_text()
    assert content.strip(), "Generated CLI reference is empty"
    assert "airbyte-ops" in content, (
        "Generated CLI reference is missing the top-level command name"
    )
