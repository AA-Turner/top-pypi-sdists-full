"""Verify a release is complete before it ships.

Checks, for a given ``vX.Y.Z`` tag:
  * ``CHANGELOG.md`` has a ``## [<tag>]`` section with at least one entry;
  * (unless ``--no-release-notes``) each user-facing release-notes file under
    ``docs/release-notes/`` carries a section for the version. Which files are
    expected is driven by ``.pysae-ai-tools.yaml (release.notes/stores)`` (the same config
    ``code release-notes`` generates from): only the configured ``languages`` ×
    ``variants`` are checked. With no config — or no restriction — that's the
    full default of three languages (fr/en/it) × three formats (markdown,
    Google Play, Apple).

Run it in the release flow (after the pipeline generated ``CHANGELOG.md`` and
the release notes were committed) to refuse shipping a release whose changelog
is empty or whose release notes are missing.

Usage:
    pysae-ai-tools ci release verify v1.4.0 [--root .] [--no-release-notes] [--json]
"""

import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from ...code.release_notes import (
    release_config,
    release_notes_apple_app_store_file,
    release_notes_file,
    release_notes_google_play_file,
)
from ...code.versioning import RELEASE_TAG_RE, is_store_skipping_prerelease


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


def _md_section(text: str, tag: str) -> bool:
    """Markdown release/changelog section: ``## [<tag>] …``."""
    return re.search(rf"(?m)^##\s*\[{re.escape(tag)}\]", text) is not None


def _txt_section(text: str, tag: str) -> bool:
    """Plain-text store-notes section: ``> <tag> — …``."""
    return re.search(rf"(?m)^>\s*{re.escape(tag)}\b", text) is not None


def _changelog_has_version(text: str, tag: str) -> tuple[bool, str]:
    """Whether CHANGELOG.md has a non-empty ``## [<tag>]`` section."""
    match = re.search(rf"(?m)^##\s*\[{re.escape(tag)}\][^\n]*\n(?P<body>.*?)(?=^##\s|\Z)", text, re.DOTALL)
    if not match:
        return False, f"no '## [{tag}]' section"
    if not re.search(r"(?m)^\s*[*-]\s+\S", match.group("body")):
        return False, f"'## [{tag}]' section is empty (no entries)"
    return True, ""


# Maps a config ``variant`` to its file-name suffix, the path resolver, and the
# section detector. Keyed by the variant names used in ``.pysae-ai-tools.yaml``.
_VARIANT_TARGETS: dict[str, tuple[str, Callable[[Path, str], Path], Callable[[str, str], bool]]] = {
    "markdown": ("md", release_notes_file, _md_section),
    "google-play": ("google-play", release_notes_google_play_file, _txt_section),
    "apple-app-store": ("apple-app-store", release_notes_apple_app_store_file, _txt_section),
}


def verify_release(repo_root: Path, tag: str, check_release_notes: bool = True) -> list[Check]:
    """Return one :class:`Check` per verified artefact.

    Release-notes checks honour ``.pysae-ai-tools.yaml (release.notes/stores)`` — only the
    configured ``languages`` × ``variants`` are verified, mirroring what
    ``code release-notes`` actually generates. With no config (or no
    restriction), all three languages × three formats are checked.
    """
    checks: list[Check] = []

    changelog = repo_root / "CHANGELOG.md"
    if not changelog.exists():
        checks.append(Check("changelog", False, "CHANGELOG.md missing"))
    else:
        ok, detail = _changelog_has_version(changelog.read_text(encoding="utf-8", errors="replace"), tag)
        checks.append(Check("changelog", ok, detail))

    if check_release_notes:
        config = release_config(repo_root)
        # Betas ship only the markdown webapp notes — the store variants are produced
        # at the final release, so don't require them for a beta. A hotfix
        # (``-hotfix.N`` / ``-N``) is store-bound like a final release, so it still
        # requires every variant.
        markdown_only = is_store_skipping_prerelease(tag)
        variants = [v for v in config.variants if v == "markdown"] if markdown_only else config.variants
        for lang in config.languages:
            for variant in variants:
                suffix, resolve_path, detector = _VARIANT_TARGETS[variant]
                name = f"release-notes.{lang}.{suffix}"
                path = resolve_path(repo_root, lang)
                if not path.exists():
                    checks.append(Check(name, False, "file missing"))
                elif not detector(path.read_text(encoding="utf-8", errors="replace"), tag):
                    checks.append(Check(name, False, f"no section for {tag}"))
                else:
                    checks.append(Check(name, True))

    return checks


app = typer.Typer()


@app.command()
def main(
    tag: Annotated[str, typer.Argument(help="Release tag (vMAJOR.MINOR.PATCH)")],
    root: Annotated[Path, typer.Option("--root", help="Project root (defaults to current directory)")] = Path("."),
    no_release_notes: Annotated[
        bool,
        typer.Option(
            "--no-release-notes",
            help="Skip the docs/release-notes/ checks (only for repos without that convention).",
        ),
    ] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the checks as JSON.")] = False,
) -> None:
    """Verify the changelog + release notes are in place for ``tag``. Exit 1 on any failure."""
    if not RELEASE_TAG_RE.match(tag):
        print(
            f"FAILED: invalid tag '{tag}' (expected vMAJOR.MINOR.PATCH or vMAJOR.MINOR.PATCH-label.N)", file=sys.stderr
        )
        raise typer.Exit(code=1)

    checks = verify_release(root, tag, check_release_notes=not no_release_notes)
    failures = [c for c in checks if not c.ok]

    if as_json:
        print(
            json.dumps(
                {
                    "tag": tag,
                    "ok": not failures,
                    "checks": [{"name": c.name, "ok": c.ok, "detail": c.detail} for c in checks],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for c in checks:
            mark = "✓" if c.ok else "✗"
            print(f"  {mark} {c.name}" + (f" — {c.detail}" if c.detail else ""))
        verdict = "OK" if not failures else f"{len(failures)} problème(s)"
        print(f"\nRelease {tag} : {verdict}", file=sys.stderr)

    if failures:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
