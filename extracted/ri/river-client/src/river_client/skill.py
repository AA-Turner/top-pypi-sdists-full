"""Locate or install the agent skills bundled with river-client.

The package ships agent skills (``SKILL.md`` folders under
``river_client/skills/``) that teach AI coding agents the current
training API. Because they travel inside the wheel, the installed copy
always matches the client version it documents.

Usage::

    python -m river_client.skill              # print bundled skill paths
    python -m river_client.skill --install    # copy into ~/.claude/skills/
    python -m river_client.skill --install --dest .claude/skills
"""

from __future__ import annotations

import argparse
import shutil
from importlib.resources import as_file, files
from pathlib import Path

_NO_SKILLS_MSG = "no bundled skills found in this installation"


def _skill_dirs(root: Path) -> list[Path]:
    return sorted(entry for entry in root.iterdir() if (entry / "SKILL.md").is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m river_client.skill",
        description=(
            "Locate or install the AI-agent skills bundled with river-client."
        ),
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="copy the bundled skill folder(s) into --dest",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path.home() / ".claude" / "skills",
        help="skills directory to install into (default: ~/.claude/skills)",
    )
    args = parser.parse_args(argv)

    root = files("river_client") / "skills"
    if not root.is_dir():
        parser.error(_NO_SKILLS_MSG)

    if args.install:
        # as_file materializes the resources onto the filesystem for
        # non-filesystem loaders (zipapp/onefile); copying must happen
        # inside the context, before any temp copy is cleaned up.
        with as_file(root) as fs_root:
            skill_dirs = _skill_dirs(fs_root)
            if not skill_dirs:
                parser.error(_NO_SKILLS_MSG)
            args.dest.mkdir(parents=True, exist_ok=True)
            for skill_dir in skill_dirs:
                target = args.dest / skill_dir.name
                shutil.copytree(skill_dir, target, dirs_exist_ok=True)
                print(f"installed {skill_dir.name} -> {target}")
        return 0

    # Print mode: only a regular filesystem install has stable paths worth
    # printing — an as_file temp copy would be deleted before the user could
    # look at it.
    if not isinstance(root, Path):
        parser.error(
            "bundled skills are not unpacked on the filesystem in this "
            "environment; use --install to extract a copy"
        )
    skill_dirs = _skill_dirs(root)
    if not skill_dirs:
        parser.error(_NO_SKILLS_MSG)
    for skill_dir in skill_dirs:
        print(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
