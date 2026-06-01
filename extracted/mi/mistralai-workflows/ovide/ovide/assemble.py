from __future__ import annotations

import re
from collections import defaultdict
from datetime import date

from ovide.config import BUMP_PRIORITY, CHANGELOG_FILE, VALID_KINDS
from ovide.fragment import Fragment


def compute_bump(fragments: list[Fragment]) -> str:
    best = "patch"
    for f in fragments:
        if BUMP_PRIORITY[f.bump] < BUMP_PRIORITY[best]:
            best = f.bump
    return best


def bump_version(current: str, bump: str) -> str:
    parts = current.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def get_latest_version() -> str | None:
    if not CHANGELOG_FILE.exists():
        return None
    content = CHANGELOG_FILE.read_text()
    match = re.search(r"## \[(\d+\.\d+\.\d+)\]", content)
    if match:
        return match.group(1)
    return None


def render_release(version: str, fragments: list[Fragment]) -> str:
    today = date.today().strftime("%Y-%m-%d")
    by_kind: defaultdict[str, list[str]] = defaultdict(list)
    for f in fragments:
        by_kind[f.kind].append(f.body)

    lines = [f"## [{version}] - {today}", ""]
    for kind in VALID_KINDS:
        entries = by_kind.get(kind)
        if not entries:
            continue
        lines.append(f"### {kind}")
        lines.append("")
        for entry in entries:
            for i, line in enumerate(entry.splitlines()):
                if i == 0:
                    lines.append(f"- {line}")
                else:
                    lines.append(f"  {line}")
        lines.append("")

    return "\n".join(lines)


def assemble_changelog(version: str, fragments: list[Fragment]) -> None:
    release_block = render_release(version, fragments)

    if CHANGELOG_FILE.exists():
        content = CHANGELOG_FILE.read_text()
        # Insert after the "# Changelog" header
        header = "# Changelog\n"
        if content.startswith(header):
            rest = content[len(header) :]
            new_content = header + "\n" + release_block + rest
        else:
            new_content = header + "\n" + release_block + "\n" + content
    else:
        new_content = "# Changelog\n\n" + release_block

    CHANGELOG_FILE.write_text(new_content)

    for f in fragments:
        f.path.unlink()
