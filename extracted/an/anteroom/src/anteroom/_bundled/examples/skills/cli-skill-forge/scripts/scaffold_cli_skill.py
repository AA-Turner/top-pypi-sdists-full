#!/usr/bin/env python3
"""Scaffold an Anteroom skill from cached CLI discovery output."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


def titleize(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split("-"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool-name", required=True, help="Human tool name, for example jira or confluence.")
    parser.add_argument("--binary", required=True, help="CLI binary or command prefix to show in the skill.")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json from discover_cli.py.")
    parser.add_argument("--summary", help="Optional path to summary.md from discover_cli.py.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Parent directory where the skill directory will be created.",
    )
    parser.add_argument("--skill-name", help="Override generated skill directory name. Defaults to <tool-name>-cli.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing skill directory.")
    return parser.parse_args()


def render_skill_md(
    skill_name: str,
    tool_slug: str,
    tool_title: str,
    binary: str,
    summary_name: str | None,
) -> str:
    resource_lines = ["  - references/cli-manifest.json"]
    if summary_name:
        resource_lines.append(f"  - references/{summary_name}")
    resources_block = "\n".join(resource_lines)
    summary_line = f"- Read `references/{summary_name}` first for the command map" if summary_name else ""
    summary_block = f"{summary_line}\n" if summary_line else ""
    return f"""---
name: {skill_name}
description: Use the cached command manifest for the {tool_title} CLI so
  Anteroom can build correct commands without repeatedly calling --help.
resources:
{resources_block}
---

# {tool_title} CLI

Use this skill when the task should be performed through the `{binary}` CLI.

## First Read

- Read `references/cli-manifest.json` first for the discovered command tree and option set
{summary_block}- Prefer the cached references over live help calls

## Operating Rules

- Do not call `--help` by default.
- Build commands from the cached manifest first.
- If a command fails with a usage or argument error, inspect only the narrowest
  relevant subcommand help, then retry once.
- Avoid rediscovering the full CLI tree during normal task execution.
- If repeated usage mismatches appear, refresh the manifest instead of improvising around drift.

## Command Construction

1. Find the closest command path in the cached references.
2. Match required arguments and likely flags from the manifest.
3. Run the concrete command.
4. If needed, do one narrow help probe for the exact failing subcommand.

## Refresh

Refresh the cached references with:

```bash
python3 ~/.anteroom/skills/cli-skill-forge/scripts/discover_cli.py \\
  --tool {tool_slug} \\
  --output-dir /tmp/{tool_slug}-discovery \\
  -- {binary}
```

Then regenerate this skill with:

```bash
python3 ~/.anteroom/skills/cli-skill-forge/scripts/scaffold_cli_skill.py \\
  --tool-name {tool_slug} \\
  --binary "{binary}" \\
  --manifest /tmp/{tool_slug}-discovery/manifest.json \\
  --summary /tmp/{tool_slug}-discovery/summary.md \\
  --output-dir ~/.anteroom/skills \\
  --force
```
"""


def main() -> int:
    args = parse_args()
    tool_slug = normalize_name(args.tool_name)
    skill_name = normalize_name(args.skill_name or f"{tool_slug}-cli")
    tool_title = args.tool_name.strip() or titleize(tool_slug)

    manifest_path = Path(args.manifest).expanduser().resolve()
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    summary_path = Path(args.summary).expanduser().resolve() if args.summary else None
    if summary_path and not summary_path.exists():
        raise SystemExit(f"Summary not found: {summary_path}")

    output_dir = Path(args.output_dir).expanduser().resolve()
    skill_dir = output_dir / skill_name
    if skill_dir.exists():
        if not args.force:
            raise SystemExit(f"Skill directory already exists: {skill_dir} (use --force to overwrite)")
        shutil.rmtree(skill_dir)

    (skill_dir / "references").mkdir(parents=True, exist_ok=True)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    (skill_dir / "references" / "cli-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    summary_name: str | None = None
    if summary_path:
        summary_name = "command-summary.md"
        (skill_dir / "references" / summary_name).write_text(summary_path.read_text(encoding="utf-8"), encoding="utf-8")

    (skill_dir / "SKILL.md").write_text(
        render_skill_md(skill_name, tool_slug, tool_title, args.binary, summary_name),
        encoding="utf-8",
    )

    print(f"Created skill: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
