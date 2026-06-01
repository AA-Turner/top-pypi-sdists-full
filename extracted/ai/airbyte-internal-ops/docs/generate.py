#!/usr/bin/env python3

# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
"""Generate docs for all public modules, the `airbyte-ops` CLI, and the MCP server.

This emits three kinds of artifacts under `docs/generated/` and
`docs/mcp-generated/` (both gitignored):

- The pdoc-rendered API reference for the `airbyte_ops_mcp` package.
- A Markdown CLI reference for the `airbyte-ops` CLI, generated via the
  `cyclopts` programmatic docs API (equivalent to `cyclopts generate-docs`).
- Per-module MCP reference pages rendered by `fastmcp_extensions.utils.docs`
  against `src/airbyte_ops_mcp/mcp/server.py:app`. Each
  `docs/mcp-generated/<module>.md` artifact is grafted into the corresponding
  `airbyte_ops_mcp.mcp.<module>` pdoc page via a `.. include::` directive.

Usage:
    uv run python -m docs.generate run

Or with Poe-the-Poet:
    poe docs-generate
    poe docs-preview

This module must be invoked via `-m docs.generate` (or the `poe docs-generate`
task, which does the same thing). Running it as `python docs/generate.py`
puts `docs/` on `sys.path[0]` and breaks the `from docs.generate_cli import ...`
absolute import below.
"""

from __future__ import annotations

import pathlib
import shutil

import pdoc
import pdoc.render_helpers
from fastmcp_extensions.utils.docs import generate_markdown_docs

from docs.generate_cli import (
    generate_airbyte_cloud_cli_reference,
    generate_airbyte_cloud_cli_submodule_references,
    generate_cli_reference,
    generate_cli_submodule_references,
)

GENERATED_DIR = pathlib.Path("docs/generated")
CLI_REFERENCE_PATH = GENERATED_DIR / "cli-reference.md"
MCP_GENERATED_DIR = pathlib.Path("docs/mcp-generated")
# File-path spec understood by `fastmcp inspect`. Using the file-path form
# (not the dotted-module form) because `fastmcp inspect` only accepts files.
MCP_SERVER_SPEC = "src/airbyte_ops_mcp/mcp/server.py:app"

# pdoc bundles markdown2 with a hardcoded `toc` extra depth of 2, so only h1/h2
# headings from a module's docstring make it into the left-sidebar "Contents"
# TOC. We raise that so the h3/h4/h5 headings emitted by cyclopts inside the
# grafted per-group CLI reference (command groups / individual commands /
# nested sub-groups) show up as navigable anchors in the sidebar too.
_TOC_DEPTH = 5


def _generate_module_docs() -> None:
    """Render the pdoc-based API reference for `airbyte_ops_mcp`."""
    public_modules = ["airbyte_ops_mcp"]

    pdoc.render_helpers.markdown_extensions["toc"]["depth"] = _TOC_DEPTH

    pdoc.render.configure(
        template_directory=pathlib.Path("docs/templates"),
        show_source=True,
        search=True,
        logo="https://docs.airbyte.com/img/logo-dark.png",
        favicon="https://docs.airbyte.com/img/favicon.png",
        mermaid=True,
        docformat="google",
    )
    pdoc.pdoc(
        *public_modules,
        output_directory=GENERATED_DIR,
    )


def run() -> None:
    """Generate API, CLI, and MCP reference docs into `docs/generated/` / `docs/mcp-generated/`.

    The CLI and MCP reference artifacts are generated first so that pdoc's
    `.. include::` directives in `airbyte_ops_mcp.cli.__init__`, in each
    `airbyte_ops_mcp.cli.<group>` submodule, and in each
    `airbyte_ops_mcp.mcp.<module>` submodule can embed them into the rendered
    HTML pages.
    """
    # Recursively delete the docs/generated and docs/mcp-generated folders if
    # they exist so each run produces a clean artifact set.
    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)
    if MCP_GENERATED_DIR.exists():
        shutil.rmtree(MCP_GENERATED_DIR)

    generate_cli_reference(CLI_REFERENCE_PATH)
    generate_cli_submodule_references()
    generate_airbyte_cloud_cli_reference()
    generate_airbyte_cloud_cli_submodule_references()
    generate_markdown_docs(
        server_spec=MCP_SERVER_SPEC,
        output=MCP_GENERATED_DIR,
    )
    _generate_module_docs()


if __name__ == "__main__":
    run()
