#!/usr/bin/env python3
"""Record a snapshot of every discoverable agent-customization unit.

Enumerates the units an agent-facing client can offer today:

* every ``.github/prompts/agdt.*.prompt.md`` (each backs one ``/agdt.*`` slash command),
* every ``.github/agents/agdt.*.agent.md``,
* every ``.agents/skills/*/SKILL.md`` when that directory exists,

and writes a sorted Markdown table of one row per unit to
``docs/agent-customization/discovery-baseline.md``.

The ``agdt.README.md`` manifests under the prompt and agent directories are not
units, and the ``agdt.*.<suffix>`` globs exclude them by construction.

Regenerate with::

    python scripts/record_discovery_baseline.py

Exit codes:
  0 — write mode: the baseline file was written.
  0 — check mode: the baseline file is up to date.
  1 — check mode: the baseline file is stale or missing.
"""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
from pathlib import Path

PROMPTS_DIR = ".github/prompts"
AGENTS_DIR = ".github/agents"
SKILLS_DIR = ".agents/skills"
OUTPUT_PATH = "docs/agent-customization/discovery-baseline.md"
REGENERATION_COMMAND = "python scripts/record_discovery_baseline.py"

PROMPT_SURFACE = "prompt"
AGENT_SURFACE = "agent"
SKILL_SURFACE = "skill"


@dataclass(frozen=True)
class Unit:
    """One discoverable customization unit."""

    surface: str
    invocation: str
    backing_file: str

    def sort_key(self) -> tuple[str, str, str]:
        """Return the deterministic ordering key for this unit."""
        return (self.surface, self.invocation, self.backing_file)


def _relative_posix(path: Path, repo_root: Path) -> str:
    """Return ``path`` relative to ``repo_root`` using forward slashes."""
    return path.relative_to(repo_root).as_posix()


def discover_prompts(repo_root: Path) -> list[Unit]:
    """Return one unit per ``agdt.*`` prompt file, invoked as a slash command."""
    units = []
    for path in sorted((repo_root / PROMPTS_DIR).glob("agdt.*.prompt.md")):
        slug = path.name.removesuffix(".prompt.md")
        units.append(Unit(PROMPT_SURFACE, f"/{slug}", _relative_posix(path, repo_root)))
    return units


def discover_agents(repo_root: Path) -> list[Unit]:
    """Return one unit per ``agdt.*`` agent file, invoked by its agent name."""
    units = []
    for path in sorted((repo_root / AGENTS_DIR).glob("agdt.*.agent.md")):
        slug = path.name.removesuffix(".agent.md")
        units.append(Unit(AGENT_SURFACE, _discover_agent_name(path, slug), _relative_posix(path, repo_root)))
    return units


def discover_skills(repo_root: Path) -> list[Unit]:
    """Return one unit per skill directory, invoked by its directory name.

    Returns an empty list when ``.agents/skills`` does not exist.
    """
    skills_root = repo_root / SKILLS_DIR
    if not skills_root.is_dir():
        return []
    units = []
    for path in sorted(skills_root.glob("*/SKILL.md")):
        units.append(Unit(SKILL_SURFACE, path.parent.name, _relative_posix(path, repo_root)))
    return units


def discover_units(repo_root: Path) -> list[Unit]:
    """Return every discoverable unit, sorted by surface then invocation name."""
    units = discover_prompts(repo_root) + discover_agents(repo_root) + discover_skills(repo_root)
    return sorted(units, key=Unit.sort_key)


def _discover_agent_name(path: Path, fallback_name: str) -> str:
    """Return the frontmatter ``name`` for an agent file, or ``fallback_name``."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return fallback_name
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("name:"):
            value = line.split(":", maxsplit=1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1].strip()
            if value:
                return value
    return fallback_name


def render_table(units: list[Unit]) -> str:
    """Render the units as a Markdown table with a header row."""
    lines = ["| Surface | Invocation name | Backing file |", "|---|---|---|"]
    for unit in units:
        lines.append(f"| {unit.surface} | `{unit.invocation}` | `{unit.backing_file}` |")
    return "\n".join(lines)


def render_document(units: list[Unit], generated_on: dt.date, footnotes_body: str = "- None recorded.") -> str:
    """Render the full baseline document, preamble included."""
    counts = {
        surface: sum(1 for unit in units if unit.surface == surface)
        for surface in (PROMPT_SURFACE, AGENT_SURFACE, SKILL_SURFACE)
    }
    return "\n".join(
        [
            "# Agent-customization discovery baseline",
            "",
            f"**Generated:** {generated_on.isoformat()}",
            "",
            f"**Regenerate with:** `{REGENERATION_COMMAND}`",
            "",
            "This file is a **snapshot, not a specification**. It records the customization units",
            "that were discoverable on the generation date so that later waves can diff against it.",
            "A row here is not a promise that the unit survives: additions and deletions are both",
            "expected, and the value of the snapshot is that they become visible and named rather",
            "than noticed later.",
            "",
            "Invocation names are recorded as the client offers them: prompt files back `/agdt.*`",
            "slash commands, agent files are selected by their agent name, and a skill is named by",
            "its directory.",
            "",
            "## Counts",
            "",
            "| Surface | Units |",
            "|---|---|",
            f"| prompt | {counts[PROMPT_SURFACE]} |",
            f"| agent | {counts[AGENT_SURFACE]} |",
            f"| skill | {counts[SKILL_SURFACE]} |",
            f"| **total** | **{len(units)}** |",
            "",
            "## Units",
            "",
            render_table(units),
            "",
            "## Footnotes",
            "",
            "Rows listed here but not offered by a client are recorded below, because a baseline",
            "that overstates the starting point makes every later diff look like a regression.",
            "",
            footnotes_body,
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    """Write the discovery baseline and report where it landed."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to scan (defaults to the repository containing this script).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"Output file (defaults to <repo-root>/{OUTPUT_PATH}).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that the current output matches the generated snapshot without writing.",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    output = args.output if args.output is not None else repo_root / OUTPUT_PATH

    units = discover_units(repo_root)
    if args.check:
        if not output.is_file():
            print(f"Baseline is stale: {output} does not exist.")
            return 1
        current = output.read_text(encoding="utf-8")
        generated_on = _extract_generated_date(current) or dt.date.today()
        footnotes_body = _extract_footnotes_body(current)
        expected = render_document(units, generated_on, footnotes_body)
        if current != expected:
            print(
                f"Baseline is stale. Regenerate with: {REGENERATION_COMMAND} --repo-root {repo_root} --output {output}"
            )
            return 1
        print(f"Baseline is up to date: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    existing = output.read_text(encoding="utf-8") if output.is_file() else None
    footnotes_body = _extract_footnotes_body(existing) if existing is not None else "- None recorded."
    output.write_text(render_document(units, dt.date.today(), footnotes_body), encoding="utf-8")
    noun = "unit" if len(units) == 1 else "units"
    print(f"Wrote {len(units)} {noun} to {output}")
    return 0


def _extract_generated_date(document: str) -> dt.date | None:
    """Return the ``Generated`` preamble date when present and parseable."""
    for line in document.splitlines():
        if line.startswith("**Generated:** "):
            try:
                return dt.date.fromisoformat(line.removeprefix("**Generated:** ").strip())
            except ValueError:
                return None
    return None


def _extract_footnotes_body(document: str) -> str:
    """Return the user-editable footnote entries from the Footnotes section.

    The Footnotes section contains a fixed description paragraph followed by the
    editable entries.  This function returns only the entries (the part starting
    at the first list item), so callers can round-trip the file without losing
    manually-recorded discrepancies.  When the section is absent or contains no
    list entries the default placeholder is returned.

    The function assumes that the user-editable content consists solely of list
    items (lines starting with ``- ``).  Any non-list prose added after the first
    list item is collected verbatim; callers must ensure footnote entries follow
    the expected ``- <entry>`` format to avoid round-trip mismatches.
    """
    lines = document.splitlines()
    in_footnotes = False
    collecting = False
    footnote_lines: list[str] = []
    for line in lines:
        if line.strip() == "## Footnotes":
            in_footnotes = True
            continue
        if in_footnotes and line.startswith("## "):
            break
        if in_footnotes:
            if not collecting:
                if line.startswith("- "):
                    collecting = True
                    footnote_lines.append(line)
            else:
                footnote_lines.append(line)
    if not in_footnotes or not collecting:
        return "- None recorded."
    body = "\n".join(footnote_lines).strip()
    return body if body else "- None recorded."


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
