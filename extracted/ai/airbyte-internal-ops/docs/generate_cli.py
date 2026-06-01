#!/usr/bin/env python3

# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Generate Markdown CLI reference(s) for Airbyte Ops CLIs.

This uses cyclopts's programmatic documentation API (the same machinery that
powers `cyclopts generate-docs`) to render Markdown covering the root
`airbyte-ops` `cyclopts.App` plus every nested subcommand (full depth,
equivalent to `:nested: full` in the Sphinx extension).

Two artifact sets are produced:

- `docs/generated/cli-reference.md` -- one combined file covering the whole
  command tree. Grafted into the pdoc `airbyte_ops_mcp.cli` module page.
- `docs/generated/cli/<group>.md` -- one file per top-level command group
  (cloud, devin, dockerhub, gh, local, registry, roster). Each group is
  generated from its own `cyclopts.App` object and grafted into the
  corresponding pdoc `airbyte_ops_mcp.cli.<group>` submodule page.
- `docs/generated/airbyte-cloud-cli-reference.md` -- one combined file covering
  the standalone `airbyte-cloud` command tree.
- `docs/generated/airbyte-cloud-cli/<group>.md` -- one file per top-level
  `airbyte-cloud` command group.

Only the top level is split; nested sub-groups (e.g. `cloud connector`,
`registry store`) remain inline in their parent group's file.

Usage:
    uv run python docs/generate_cli.py [OUTPUT_PATH]

Or, invoked as part of the combined docs pipeline:
    poe docs-generate
"""

from __future__ import annotations

import pathlib
import sys

from cyclopts import App
from cyclopts.docs import generate_markdown_docs

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_SOURCE_PATHS = (
    REPO_ROOT / "src",
    REPO_ROOT / "airbyte-cloud-cli",
)
for package_source_path in reversed(PACKAGE_SOURCE_PATHS):
    if str(package_source_path) not in sys.path:
        sys.path.insert(0, str(package_source_path))

# Importing the CLI app modules triggers the import side effects that register
# every domain submodule's App on the root app. It must run before we reference
# any of the per-group App objects below.
from airbyte_cloud_cli.app import app as airbyte_cloud_app  # noqa: E402
from airbyte_cloud_cli.connections import connections_app  # noqa: E402
from airbyte_cloud_cli.destinations import destinations_app  # noqa: E402
from airbyte_cloud_cli.jobs import jobs_app  # noqa: E402
from airbyte_cloud_cli.sources import sources_app  # noqa: E402
from airbyte_cloud_cli.workspaces import workspaces_app  # noqa: E402

from airbyte_ops_mcp.cli.app import app  # noqa: E402
from airbyte_ops_mcp.cli.cloud import cloud_app  # noqa: E402
from airbyte_ops_mcp.cli.devin import devin_app  # noqa: E402
from airbyte_ops_mcp.cli.dockerhub import dockerhub_app  # noqa: E402
from airbyte_ops_mcp.cli.gh import gh_app  # noqa: E402
from airbyte_ops_mcp.cli.local import local_app  # noqa: E402
from airbyte_ops_mcp.cli.registry import registry_app  # noqa: E402
from airbyte_ops_mcp.cli.roster import roster_app  # noqa: E402
from airbyte_ops_mcp.cli.secrets import secrets_app  # noqa: E402

DEFAULT_OUTPUT_PATH = pathlib.Path("docs/generated/cli-reference.md")
DEFAULT_SUBMODULE_OUTPUT_DIR = pathlib.Path("docs/generated/cli")
AIRBYTE_CLOUD_OUTPUT_PATH = pathlib.Path(
    "docs/generated/airbyte-cloud-cli-reference.md"
)
AIRBYTE_CLOUD_SUBMODULE_OUTPUT_DIR = pathlib.Path("docs/generated/airbyte-cloud-cli")

# Maps the `airbyte_ops_mcp.cli.<name>` submodule name to its top-level
# `cyclopts.App`. The order here determines iteration order but not output
# ordering in pdoc.
CLI_SUBMODULE_APPS: tuple[tuple[str, App], ...] = (
    ("cloud", cloud_app),
    ("devin", devin_app),
    ("dockerhub", dockerhub_app),
    ("gh", gh_app),
    ("local", local_app),
    ("registry", registry_app),
    ("roster", roster_app),
    ("secrets", secrets_app),
)

AIRBYTE_CLOUD_SUBMODULE_APPS: tuple[tuple[str, App], ...] = (
    ("workspaces", workspaces_app),
    ("sources", sources_app),
    ("destinations", destinations_app),
    ("connections", connections_app),
    ("jobs", jobs_app),
)


def generate_cli_reference(
    output_path: pathlib.Path = DEFAULT_OUTPUT_PATH,
    *,
    include_hidden: bool = False,
    heading_level: int = 1,
) -> pathlib.Path:
    """Render the combined `airbyte-ops` CLI reference as Markdown.

    This walks the full command tree rooted at `airbyte_ops_mcp.cli.app:app`
    and writes the rendered Markdown to `output_path`, creating parent
    directories as needed.

    Returns the resolved `output_path` for convenience.
    """
    markdown = generate_markdown_docs(
        app,
        include_hidden=include_hidden,
        heading_level=heading_level,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)
    return output_path


def generate_cli_submodule_references(
    output_dir: pathlib.Path = DEFAULT_SUBMODULE_OUTPUT_DIR,
    *,
    include_hidden: bool = False,
    heading_level: int = 2,
    root_command: str = "airbyte-ops",
) -> list[pathlib.Path]:
    """Render one Markdown file per top-level CLI command group.

    For each `(name, group_app)` in `CLI_SUBMODULE_APPS`, writes
    `<output_dir>/<name>.md` covering that group and everything nested
    beneath it. The default `heading_level=2` means the group's own heading
    renders as `##`, leaving room for the grafted pdoc submodule page to own
    the `#` level.

    `command_chain=[root_command, name]` is passed through to cyclopts so the
    usage / heading strings render as `airbyte-ops <group> ...` rather than
    `<group> ...` (the sub-`App` objects don't know they're nested under the
    root `airbyte-ops` entrypoint when generated in isolation).

    Returns the list of written paths in iteration order.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[pathlib.Path] = []
    for name, group_app in CLI_SUBMODULE_APPS:
        markdown = generate_markdown_docs(
            group_app,
            include_hidden=include_hidden,
            heading_level=heading_level,
            command_chain=[root_command, name],
        )
        output_path = output_dir / f"{name}.md"
        output_path.write_text(markdown)
        written.append(output_path)
    return written


def generate_airbyte_cloud_cli_reference(
    output_path: pathlib.Path = AIRBYTE_CLOUD_OUTPUT_PATH,
    *,
    include_hidden: bool = False,
    heading_level: int = 1,
) -> pathlib.Path:
    """Render the combined standalone `airbyte-cloud` CLI reference."""
    markdown = generate_markdown_docs(
        airbyte_cloud_app,
        include_hidden=include_hidden,
        heading_level=heading_level,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)
    return output_path


def generate_airbyte_cloud_cli_submodule_references(
    output_dir: pathlib.Path = AIRBYTE_CLOUD_SUBMODULE_OUTPUT_DIR,
    *,
    include_hidden: bool = False,
    heading_level: int = 2,
    root_command: str = "airbyte-cloud",
) -> list[pathlib.Path]:
    """Render one Markdown file per top-level `airbyte-cloud` command group."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[pathlib.Path] = []
    for name, group_app in AIRBYTE_CLOUD_SUBMODULE_APPS:
        markdown = generate_markdown_docs(
            group_app,
            include_hidden=include_hidden,
            heading_level=heading_level,
            command_chain=[root_command, name],
        )
        output_path = output_dir / f"{name}.md"
        output_path.write_text(markdown)
        written.append(output_path)
    return written


def _main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    output = pathlib.Path(args[0]) if args else DEFAULT_OUTPUT_PATH
    combined_path = generate_cli_reference(output)
    airbyte_cloud_path = generate_airbyte_cloud_cli_reference()
    submodule_paths = generate_cli_submodule_references()
    airbyte_cloud_submodule_paths = generate_airbyte_cloud_cli_submodule_references()
    print(f"Wrote combined CLI reference to {combined_path}")
    print(f"Wrote Airbyte Cloud CLI reference to {airbyte_cloud_path}")
    print(
        f"Wrote {len(submodule_paths)} per-submodule CLI reference files to "
        f"{DEFAULT_SUBMODULE_OUTPUT_DIR}"
    )
    print(
        f"Wrote {len(airbyte_cloud_submodule_paths)} Airbyte Cloud CLI reference files to "
        f"{AIRBYTE_CLOUD_SUBMODULE_OUTPUT_DIR}"
    )


if __name__ == "__main__":
    _main()
