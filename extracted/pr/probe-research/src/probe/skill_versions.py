"""One skill, two readers: the main agent's version and the daemon writer's.

A skill with a `versions/` folder (today only `track-work`) is ONE base -- its
SKILL.md, the file the researcher edits -- plus a header per reader and an
optional footer. Each agent sees only its own version (Richard 2026-09-28: "the
plugin should install both versions and only selectively show one specific
version to the correct agent"):

    main agent  = SKILL.md front matter + versions/header.main-agent.md + the base
    writer      = versions/header.writer.md + the base + versions/footer.writer.md

`make sync-plugin-skills` writes the main agent's version into the plugins (and
leaves `versions/` out of them); the daemon's loader (`bite.skills_text`) renders
the writer's from the CLI's own copy. Stdlib only: the Makefile runs this file
directly (`python3 src/probe/skill_versions.py <skill dir> <reader>`).
"""

from __future__ import annotations

import sys
from pathlib import Path

MAIN_AGENT = "main-agent"
WRITER = "writer"
READERS = (MAIN_AGENT, WRITER)
VERSIONS = "versions"


def split_front_matter(text: str) -> tuple[str, str]:
    """`(front matter block with its closing ---, body)`; ("", text) without one."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            cut = text.index("\n", end + 1) + 1 if "\n" in text[end + 1:] else len(text)
            return text[:cut], text[cut:]
    return "", text


def _piece(skill_dir: Path, name: str) -> str:
    path = skill_dir / VERSIONS / name
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def render(skill_dir: Path, reader: str) -> str:
    """The skill as `reader` sees it. A skill without `versions/` is its SKILL.md."""
    if reader not in READERS:
        raise ValueError(f"unknown reader {reader!r}: one of {', '.join(READERS)}")
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if not (skill_dir / VERSIONS).is_dir():
        return text
    front, base = split_front_matter(text)
    base = base.strip()
    if reader == MAIN_AGENT:
        header = _piece(skill_dir, f"header.{MAIN_AGENT}.md")
        return front + "\n" + "\n\n".join(p for p in (header, base) if p) + "\n"
    parts = (_piece(skill_dir, f"header.{WRITER}.md"), base, _piece(skill_dir, f"footer.{WRITER}.md"))
    return "\n\n".join(p for p in parts if p) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: skill_versions.py <skill dir> <main-agent|writer>", file=sys.stderr)
        return 2
    sys.stdout.write(render(Path(argv[0]), argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
