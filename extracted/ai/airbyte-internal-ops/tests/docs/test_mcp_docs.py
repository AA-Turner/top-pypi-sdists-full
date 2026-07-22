# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Smoke tests for the MCP Markdown reference generator integration.

Verifies that `docs.generate.run()` invokes
`fastmcp_extensions.utils.docs.generate_markdown_docs` with the expected
server spec and output directory, and that an end-to-end invocation of the
generator against the repo's MCP server produces a non-empty set of
per-module Markdown files plus an `index.md`.

These tests do not assert on the exact shape of the rendered Markdown —
that is owned by `fastmcp_extensions` and is expected to evolve.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastmcp_extensions.utils.docs import generate_markdown_docs

import docs.generate as docs_generate


@pytest.mark.unit
def test_run_invokes_generate_markdown_docs_with_expected_spec(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`docs.generate.run()` calls `generate_markdown_docs` with the canonical spec/output."""
    captured: dict[str, Any] = {}

    def fake_generate_markdown_docs(*, server_spec: str, output: Path) -> None:
        captured["server_spec"] = server_spec
        captured["output"] = output
        output.mkdir(parents=True, exist_ok=True)
        (output / "index.md").write_text("stub\n")

    # Stub out the three expensive sibling generators so this test stays fast
    # and hermetic. We only care that `run()` invokes `generate_markdown_docs`
    # with the canonical spec + output directory.
    monkeypatch.setattr(
        docs_generate,
        "generate_markdown_docs",
        fake_generate_markdown_docs,
    )
    monkeypatch.setattr(docs_generate, "generate_cli_reference", lambda _path: None)
    monkeypatch.setattr(
        docs_generate, "generate_cli_submodule_references", lambda: None
    )
    monkeypatch.setattr(docs_generate, "_generate_module_docs", lambda: None)

    docs_generate.run()

    assert captured["server_spec"] == docs_generate.MCP_SERVER_SPEC
    assert captured["output"] == docs_generate.MCP_GENERATED_DIR


@pytest.mark.unit
def test_generate_markdown_docs_against_repo_server(tmp_path: Path) -> None:
    """End-to-end: the generator produces per-module Markdown + `index.md` for this repo."""
    output = tmp_path / "mcp-generated"

    generate_markdown_docs(
        server_spec=docs_generate.MCP_SERVER_SPEC,
        output=output,
    )

    assert output.is_dir()
    index = output / "index.md"
    assert index.exists(), "Generator did not write an index.md"
    assert index.read_text().strip(), "Generated index.md is empty"

    module_pages = [p for p in output.glob("*.md") if p.name != "index.md"]
    assert module_pages, "Generator did not emit any per-module Markdown"
    # Spot-check one file we know this repo's MCP server registers.
    assert (output / "github_ops.md").exists()
